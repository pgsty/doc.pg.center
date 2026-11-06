---
title: "初始化 Apache Cloudberry"
description: "Apache Cloudberry 是分布式系统，因此初始化 Apache Cloudberry 数据库管理系统时，需要初始化多个独立的 PostgreSQL 数据库实例（在 Cloudberry 中称为 *Segment 实例*）。"
weight: 80
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/deployment/init_cloudberry.md"
---

必须初始化系统所有主机上的各个数据库实例（Coordinator 和所有 Segment），使它们能够协同工作，构成统一的 DBMS。Cloudberry 提供了自己的 `initdb` 版本，即 [gpinitsystem](/cloudberry/reference/sys-utilities/gpinitsystem/)，负责初始化 Coordinator 和每个 Segment 实例上的数据库，并按正确顺序启动各个实例。

Apache Cloudberry 数据库系统初始化并启动后，即可连接到 Cloudberry Coordinator，像使用普通 PostgreSQL DBMS 一样创建和管理数据库。

执行以下初始化任务时，必须以 `gpadmin` 用户身份登录 Coordinator 主机。要运行 Apache Cloudberry 工具，必须使用 source 加载 `cloudberry-env.sh` 文件，设置 Apache Cloudberry 环境变量。例如，登录 Coordinator 后，运行以下命令。

```
$ su - gpadmin
$ source /usr/local/cloudberry-db/cloudberry-env.sh
```

## 创建初始化主机文件 {#creating-the-initialization-host-file}

[gpinitsystem](/cloudberry/reference/sys-utilities/gpinitsystem/) 工具需要一个主机文件，其中包含各台 Segment 主机的地址列表。初始化工具将每台主机列出的主机地址数量，乘以 `gpinitsystem_config` 文件中指定的数据目录位置数量，以此确定每台主机上的 Segment 实例数量。

此文件只应包含 Segment 主机的地址，不应包含 Coordinator 或 Standby Coordinator。对于具有多个未绑定网络接口的 Segment 机器，此文件应列出每个接口的主机地址名，每行一个。

> [!NOTE] 说明
> Apache Cloudberry Segment 主机的命名约定为 sdwN，其中 sdw 为前缀，N 为整数，例如 `sdw2` 等。如果主机具有多块未绑定的网卡，惯例是在主机名后追加连字符（`-`）和数字。例如，`sdw1-1` 和 `sdw1-2` 是主机 `sdw1` 的两个接口名。不过，建议采用网卡绑定，以构建具备负载均衡和容错能力的网络。

### 创建初始化主机文件的步骤 {#to-create-the-initialization-host-file}

1.  创建名为 `hostfile_gpinitsystem` 的文件。在文件中添加 *Segment* 主机接口的主机地址名，每行一个名称，不要有多余的行或空格。例如，有四台 Segment 主机，每台有两个未绑定的网络接口时：

    ```
    sdw1-1
    sdw1-2
    sdw2-1
    sdw2-2
    sdw3-1
    sdw3-2
    sdw4-1
    sdw4-2
    ```

2.  保存并关闭文件。

> [!NOTE] 说明
> 如果不确定机器使用的主机名或接口地址名，请查看 `/etc/hosts` 文件。

## 创建 Apache Cloudberry 配置文件 {#creating-the-apache-cloudberry-configuration-file}

Cloudberry 配置文件用于告知 [gpinitsystem](/cloudberry/reference/sys-utilities/gpinitsystem/) 工具，应如何配置 Apache Cloudberry 系统。示例配置文件位于 `$GPHOME/docs/cli_help/gpconfigs/gpinitsystem_config`。

### 创建 gpinitsystem_config 文件的步骤 {#to-create-a-gpinitsystem_config-file}

1.  复制 `gpinitsystem_config` 文件，作为配置起点。例如：

    ```
    $ mkdir -p gpconfigs
    $ cp $GPHOME/docs/cli_help/gpconfigs/gpinitsystem_config \
         /home/gpadmin/gpconfigs/gpinitsystem_config
    ```

2.  在文本编辑器中打开刚复制的文件。

    根据实际环境设置所有必需参数。更多信息请参阅 [gpinitsystem](/cloudberry/reference/sys-utilities/gpinitsystem/)。Apache Cloudberry 系统必须包含一个 Coordinator 实例和*至少两个* Segment 实例，即使搭建单节点系统也是如此。

    `DATA_DIRECTORY` 参数决定每台主机创建多少个 Segment。如果 Segment 主机具有多个网络接口，并且主机文件中使用了这些接口的地址名，Segment 将均匀分布到各个可用接口上。

    `COORDINATOR_HOSTNAME` 是 Coordinator 节点的主机名。

    `COORDINATOR_DIRECTORY` 是 Coordinator 节点的数据目录。

    指定 `PORT_BASE` 时，请先查看 `/etc/sysctl.conf` 文件中 `net.ipv4.ip_local_port_range` 参数指定的端口范围。

    以下是 `gpinitsystem_config` 文件中*必需*参数的示例：

    ```
    SEG_PREFIX=gpseg
    PORT_BASE=6000 
    declare -a DATA_DIRECTORY=(/data1/primary /data1/primary /data1/primary /data2/primary /data2/primary /data2/primary)
    COORDINATOR_HOSTNAME=cdw 
    COORDINATOR_DIRECTORY=/data/coordinator 
    COORDINATOR_PORT=5432 
    TRUSTED SHELL=ssh
    CHECK_POINT_SEGMENTS=8
    ENCODING=UNICODE
    ```

3. （可选）如果要部署镜像 Segment，请取消镜像参数的注释，并根据实际环境设置这些参数。指定 `MIRROR_PORT_BASE` 时，请先查看 `/etc/sysctl.conf` 文件中 `net.ipv4.ip_local_port_range` 参数指定的端口范围。以下是 `gpinitsystem_config` 文件中*可选*镜像参数的示例：

    ```
    MIRROR_PORT_BASE=7000
    declare -a MIRROR_DATA_DIRECTORY=(/data1/mirror /data1/mirror /data1/mirror /data2/mirror /data2/mirror /data2/mirror)
    ```

    > [!NOTE] 说明
    > 可以在初始化 Cloudberry 系统时只配置主 Segment，之后再使用 [gpaddmirrors](/cloudberry/reference/sys-utilities/gpaddmirrors/) 工具部署镜像。

4. 要在初始化期间创建默认数据库，需要填写数据库名称。在本例中，初始化期间会创建 `warehouse` 数据库：

    ```
    DATABASE_NAME=warehouse
    ```

5.  保存并关闭文件。

## 运行初始化工具 {#running-the-initialization-utility}

[gpinitsystem](/cloudberry/reference/sys-utilities/gpinitsystem/) 工具会使用配置文件中定义的值创建 Apache Cloudberry 系统。

以下步骤假定已以 `gpadmin` 用户身份登录，并已使用 source 加载 `cloudberry-env.sh` 文件，设置好 Apache Cloudberry 环境变量。

### 运行初始化工具的步骤 {#to-run-the-initialization-utility}

1.  运行以下命令，指定初始化配置文件（`gpinitsystem_config`）和主机文件（`hostfile_gpinitsystem`）的路径及文件名。例如：

    ```
    $ cd ~
    $ gpinitsystem -c gpconfigs/gpinitsystem_config -h gpconfigs/hostfile_gpinitsystem
    ```

    在上述命令中，`-c` 指定配置文件，`-h` 指定计算节点列表。

    要配置完全冗余的系统（包含 Standby Coordinator 和*分散式*镜像配置），请添加 `-s` 和 `--mirror-mode=spread` 选项。例如：

    ```
    $ gpinitsystem -c gpconfigs/gpinitsystem_config -h gpconfigs/hostfile_gpinitsystem \
      -s <standby_coordinator_hostname> --mirror-mode=spread
    ```

    创建新集群时，可以使用 `-O output_configuration_file` 选项，将集群配置详情保存到文件中。例如：

    ```
    $ gpinitsystem -c gpconfigs/gpinitsystem_config -O gpconfigs/config_template 
    ```

    可以编辑此输出文件，并在以后将其作为 `-I` 选项的输入文件，用于创建新集群或从备份恢复。详情请参阅 [gpinitsystem](/cloudberry/reference/sys-utilities/gpinitsystem/)。

    > [!NOTE] 说明
    > 使用 `-O` 选项调用 `gpinitsystem` 不会初始化 Apache Cloudberry 系统，只会生成并保存包含集群配置详情的文件。

2.  该工具会验证配置信息，确保能够连接到每台主机，并访问配置中指定的数据目录。如果所有预检查均成功，工具会提示确认配置。例如：

    ```
    => Continue with Cloudberry creation? Yy/Nn
    ```

3.  按 `y` 开始初始化。
4.  随后，工具将开始配置和初始化系统中的 Coordinator 实例及每个 Segment 实例。各个 Segment 实例会并行配置。根据 Segment 数量的多少，此过程可能需要一段时间。
5.  配置成功完成后，工具将启动 Apache Cloudberry 系统。应看到以下信息：

    ```
    => Apache Cloudberry instance successfully created.
    ```

### （可选）初始化 Standby Coordinator {#optional-initializing-a-standby-coordinator}

> [!NOTE] 说明
> 如果在 `gpinitsystem` 命令中指定了 `-s <standby_coordinator_hostname>` 选项，Standby Coordinator 已完成初始化，可以跳过此步骤。

如果运行 `gpinitsystem` 时没有指定 `-s` 选项，可以在集群启动并运行后，使用 `gpinitstandby` 工具单独初始化 Standby Coordinator。

Standby Coordinator 充当 Coordinator 实例的温备。如果主 Coordinator 不可用，可以激活 Standby Coordinator 接管。

1. 确保已在 Standby Coordinator 主机上创建相同的数据目录，且所有者为 `gpadmin`：

    ```bash
    $ gpssh -h scdw -e 'sudo mkdir -p /data/coordinator'
    $ gpssh -h scdw -e 'sudo chown gpadmin:gpadmin /data/coordinator'
    ```

2. 在 Coordinator 主机上，以 `gpadmin` 身份运行 `gpinitstandby`：

    ```bash
    $ gpinitstandby -s scdw
    ```

3. 验证 Standby Coordinator 已同步：

    ```bash
    $ gpstate -f
    ```

    输出中 Standby Coordinator 的状态应显示为 `Sync state: sync`。

### 排查初始化问题 {#troubleshooting-initialization-problems}

如果工具在配置实例时遇到任何错误，整个过程都会失败，并可能留下一个只创建了一部分的系统。请根据错误消息和日志，确定失败原因及其发生的阶段。日志文件创建在 `~/gpAdminLogs` 中。

根据错误发生的阶段，可能需要先清理，再重试 `gpinitsystem` 工具。例如，如果部分 Segment 实例创建成功，另一些创建失败，可能需要停止 `postgres` 进程，并从数据存储区域中移除工具创建的数据目录。必要时，工具会创建回退脚本来协助清理。

#### 使用回退脚本 {#using-the-backout-script}

如果 gpinitsystem 工具失败，并使系统处于部分安装状态，工具会创建以下回退脚本：

`~/gpAdminLogs/backout_gpinitsystem_<user>_<timestamp>`

可以使用此脚本清理只创建了一部分的 Apache Cloudberry 系统。回退脚本会移除工具创建的数据目录、`postgres` 进程和日志文件。修正导致 `gpinitsystem` 失败的错误并运行回退脚本后，即可重试初始化 Apache Cloudberry 阵列。

以下示例说明如何运行回退脚本：

```
$ bash ~/gpAdminLogs/backout_gpinitsystem_gpadmin_20071031_121053
```

## 设置 Apache Cloudberry 时区 {#setting-the-apache-cloudberry-timezone}

作为最佳实践，应将 Apache Cloudberry 和主机系统配置为使用一个已知且受支持的时区。Apache Cloudberry 使用的时区来自内部保存的一组 PostgreSQL 时区。设置 Apache Cloudberry 时区，可以避免每次重启集群时都重新选择时区，并为 Apache Cloudberry 的 Coordinator 和 Segment 实例设定时区。

使用 [gpconfig](/cloudberry/reference/sys-utilities/gpconfig/) 工具查看和设置 Apache Cloudberry 时区。例如，以下命令先显示 Apache Cloudberry 时区，再将时区设置为 `US/Pacific`。

```
$ gpconfig -s TimeZone
$ gpconfig -c TimeZone -v 'US/Pacific'
```

更改时区后，必须重启 Apache Cloudberry。`gpstop -ra` 命令可以重启 Apache Cloudberry。系统目录视图 `pg_timezone_names` 提供 Apache Cloudberry 的时区信息。

## 设置 Apache Cloudberry 环境变量 {#setting-apache-cloudberry-environment-variables}

必须在 Apache Cloudberry 的 Coordinator 和 Standby Coordinator 主机上，为运行 Apache Cloudberry 的用户（`gpadmin`）设置环境变量。Apache Cloudberry 安装目录中提供了 `cloudberry-env.sh` 文件，其中包含 Apache Cloudberry 的环境变量设置。

Apache Cloudberry 管理工具还要求设置 `COORDINATOR_DATA_DIRECTORY` 环境变量。该变量应指向 `gpinitsystem` 工具在 Coordinator 数据目录位置下创建的目录。

> [!NOTE] 说明
> `cloudberry-env.sh` 脚本会修改运行环境，以支持运行 Apache Cloudberry 专用工具。这些环境更改可能会对其他系统级工具（例如 `ps` 或 `yum`）的运行产生不利影响。应使用不同的账户分别执行系统管理和数据库管理，而不要尝试以 `gpadmin` 身份同时执行这两类工作。

以下步骤可确保系统重启后，`gpadmin` 用户的环境变量仍已设置好。

### 为 Apache Cloudberry 设置 gpadmin 环境的步骤 {#to-set-up-the-gpadmin-environment-for-apache-cloudberry}

1.  在文本编辑器中打开 `gpadmin` 的配置文件（例如 `.bashrc`）。例如：

    ```
    $ vi ~/.bashrc
    ```

2.  在文件中添加相应行，以加载 `cloudberry-env.sh` 文件并设置 `COORDINATOR_DATA_DIRECTORY` 环境变量。例如：

    ```
    source /usr/local/cloudberry-db/cloudberry-env.sh
    export COORDINATOR_DATA_DIRECTORY=/data/coordinator/gpseg-1
    ```

3.  （可选）为方便使用，还可以设置一些客户端会话环境变量，例如 `PGPORT`、`PGUSER` 和 `PGDATABASE`。例如：

    ```
    export PGPORT=5432
    export PGUSER=gpadmin
    export PGDATABASE=warehouse
    ```

4.  （可选）如果使用 RHEL/Oracle/Rocky Linux，请将以下行添加到 `.bashrc` 文件末尾，以便在 `cloudberry-env.sh` 环境中使用 `ps` 命令：

    ```
    export LD_PRELOAD=/lib64/libz.so.1 ps
    ```

5.  保存并关闭文件。
6.  编辑配置文件后，使用 source 加载，使更改生效。例如：

    ```
    $ source ~/.bashrc
    ```

7.  如果有 Standby Coordinator 主机，还应将环境文件复制到 Standby Coordinator。例如：

    ```
    $ cd ~
    $ scp .bashrc <standby_hostname>:`pwd`
    ```

> [!NOTE] 说明
> `.bashrc` 文件不应产生任何输出。如果希望用户登录时显示一条消息，请改用 `.bash_profile` 文件。
