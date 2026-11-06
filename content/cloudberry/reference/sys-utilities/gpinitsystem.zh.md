---
title: "gpinitsystem"
description: "使用 `gpinitsystem_config` 文件中指定的配置参数初始化 Apache Cloudberry 系统。"
weight: 150
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpinitsystem.md"
---

## 概要 {#synopsis}

```shell
gpinitsystem -c <cluster_configuration_file> 
            [-h <hostfile_gpinitsystem>]
            [-B <parallel_processes>] 
            [-p <postgresql_conf_param_file>]
            [-s <standby_coordinator_host>
                [-P <standby_coordinator_port>]
                [-S <standby_coordinator_datadir> | --standby_datadir=<standby_coordinator_datadir>]]
            [-m <number> | --max_connections=number>]
            [-b <size> | --shared_buffers=<size>]
            [-n <locale> | --locale=<locale>] [--lc-collate=<locale>] 
            [--lc-ctype=<locale>] [--lc-messages=<locale>] 
            [--lc-monetary=<locale>] [--lc-numeric=<locale>] 
            [--lc-time=<locale>] [-e <password> | --su_password=<password>] 
            [--mirror-mode={group|spread}] [-a] [-q] [-l <logfile_directory>] [-D]
            [-I <input_configuration_file>]
            [-O <output_configuration_file>]

gpinitsystem -v | --version

gpinitsystem -? | --help
```

## 说明 {#description}

`gpinitsystem` 工具使用集群配置文件中定义的值及所提供的命令行选项，创建 Apache Cloudberry 实例或写出输入配置文件。有关配置文件的更多信息，请参阅[初始化配置文件格式](#initialization-configuration-file-format)。运行此工具前，确保阵列中的所有主机都已安装 Apache Cloudberry 软件。

使用 `<-O output_configuration_file>` 选项时，`gpinitsystem` 会将提供的全部配置信息写入指定输出文件。该文件可配合 `-I` 选项创建新集群，或从备份配置重新创建集群。更多信息请参阅[初始化配置文件格式](#initialization-configuration-file-format)。

在 Apache Cloudberry 数据库管理系统中，必须在系统所有主机上初始化各数据库实例（Coordinator 实例和所有 Segment 实例），使它们能够作为统一的数据库管理系统协同工作。`gpinitsystem` 工具负责初始化 Cloudberry Coordinator 和每个 Segment 实例，并配置整个系统。

运行 `gpinitsystem` 前，必须将 `$GPHOME` 环境变量设为 Coordinator 主机上 Apache Cloudberry 的安装位置，并使用 `gpssh-exkeys` 在阵列的所有主机地址之间交换 SSH 密钥。

此工具执行以下任务：

- 验证配置文件中的参数是否正确。
- 确保能够连接到每个主机地址。如果某个地址无法访问，工具会退出。
- 验证区域设置。
- 显示将要使用的配置，并提示用户确认。
- 初始化 Coordinator 实例。
- 初始化 Standby Coordinator 实例（如果指定）。
- 初始化主 Segment 实例。
- 初始化镜像 Segment 实例（如果配置了镜像）。
- 配置 Apache Cloudberry 系统，并检查错误。
- 启动 Apache Cloudberry 系统。

> **注意** 此工具通过系统之间的安全 shell（SSH）连接执行任务。在大型 Apache Cloudberry 部署、云部署，或每台主机包含大量 Segment 的部署中，此工具可能超过主机对未认证连接设置的最大阈值。可以考虑更新 SSH 的 `MaxStartups` 和 `MaxSessions` 配置参数以提高此阈值。有关 SSH 配置选项的更多信息，请参阅 Linux 发行版的 SSH 文档。

## 选项 {#options}

**`-a`**

不提示用户确认。

**`-B parallel_processes`**

并行创建的 Segment 数量。如果未指定，此工具一次最多启动 4 个并行进程。

**`-c cluster_configuration_file`**

必需。配置文件的完整路径和文件名，其中包含配置和初始化新 Apache Cloudberry 系统所需的全部已定义参数。文件说明请参阅[初始化配置文件格式](#initialization-configuration-file-format)。必须为 `gpinitsystem` 提供 `-c <cluster_configuration_file>` 或 `-I <input_configuration_file>` 选项之一。

**`-D`**

将日志输出级别设为 debug。

**`-h hostfile_gpinitsystem`**

可选。包含 Segment 主机地址的文件的完整路径和文件名。如果未在命令行指定，可以通过 gpinitsystem_config 文件中的 `MACHINE_LIST_FILE` 参数指定主机文件。

**`-I input_configuration_file`**

输入配置文件的完整路径和文件名。该文件使用 `QD_PRIMARY_ARRAY`、`PRIMARY_ARRAY` 和 `MIRROR_ARRAY` 参数定义 Apache Cloudberry 主机系统，以及主机上的 Coordinator 和 Segment 实例。通常使用 `gpinitsystem` 的 `-O output_configuration_file` 选项创建输入配置文件。编辑这些参数，即可初始化新集群或从备份配置重新创建集群。必须为 `gpinitsystem` 提供 `-c <cluster_configuration_file>` 或 `-I <input_configuration_file>` 选项之一。

**`-n locale | --locale=locale`**

设置 Apache Cloudberry 使用的默认区域设置。如果未指定，默认为 `en_US.utf8`。区域设置标识符由语言标识符、地区标识符以及可选的字符集编码组成。例如，`sv_SE` 表示瑞典使用的瑞典语，`en_US` 表示美国英语，`fr_CA` 表示加拿大法语。如果一个区域设置可以使用多种字符集，其写法如下：`en_US.UTF-8`（区域设置与字符集编码）。在大多数系统上，`locale` 命令显示当前区域环境设置，`locale -a` 显示所有可用区域设置的列表。

**`--lc-collate=locale`**

类似于 `--locale`，但设置排序规则（数据排序）所用的区域设置。Apache Cloudberry 初始化后无法更改排序顺序，因此必须选择与计划用于数据的字符集编码兼容的排序规则区域设置。有一种特殊排序规则名称为 `C` 或 `POSIX`（按字节顺序而非字典顺序排序）。`C` 排序规则可以与任何字符编码一起使用。

**`--lc-ctype=locale`**

类似于 `--locale`，但设置字符分类所用的区域设置（哪些字符序列有效，以及如何解释这些序列）。Apache Cloudberry 初始化后无法更改此设置，因此必须选择与计划存储的数据兼容的字符分类区域设置。

**`--lc-messages=locale`**

类似于 `--locale`，但设置 Apache Cloudberry 输出消息所用的区域设置。当前版本的 Apache Cloudberry 不支持多种输出消息区域设置（所有消息均为英文），因此更改此设置不会产生影响。

**`--lc-monetary=locale`**

类似于 `--locale`，但设置货币金额格式所用的区域设置。

**`--lc-numeric=locale`**

类似于 `--locale`，但设置数字格式所用的区域设置。

**`--lc-time=locale`**

类似于 `--locale`，但设置日期和时间格式所用的区域设置。

**`-l logfile_directory`**

写入日志文件的目录。默认为 `~/gpAdminLogs`。

**`-m number | --max_connections=number`**

设置允许连接 Coordinator 的最大客户端连接数。默认为 250。

**`-O output_configuration_file`**

可选，用于初始化新集群。此选项将 `cluster_configuration_file`（配合 -c 使用）中的信息写入指定的 `output_configuration_file`。该文件使用 `QD_PRIMARY_ARRAY`、`PRIMARY_ARRAY` 和 `MIRROR_ARRAY` 参数定义 Apache Cloudberry 成员。可将其作为 `-I` `input_configuration_file` 选项所用文件的模板。更多信息请参阅[示例](#examples)。

**`-p postgresql_conf_param_file`**

可选。指定一个文件名，其中包含希望为 Apache Cloudberry 设置的 `postgresql.conf` 参数值。初始化各 Coordinator 和 Segment 实例时会使用这些设置。也可以在初始化后通过 `gpconfig` 工具设置参数。

**`-q`**

以静默模式运行。命令输出不显示在屏幕上，但仍会写入日志文件。

**`-b size | --shared_buffers=size`**

设置 Cloudberry 服务器实例用于共享内存缓冲区的内存量。可以使用千字节（kB）、兆字节（MB）或吉字节（GB）指定大小。默认为 125MB。

**`-s standby_coordinator_host`**

可选。如果希望配置备用 Coordinator 实例，请通过此选项指定主机名。该主机必须已安装并配置 Apache Cloudberry 软件。

**`-P standby_coordinator_port`**

如果通过 `-s` 配置 Standby Coordinator 实例，请通过此选项指定其端口号。默认与 Coordinator 端口相同。要在同一主机上运行备用和主 Coordinator，必须使用此选项为备用实例指定不同的端口。备用主机必须已安装并配置 Apache Cloudberry 软件。

**`-S standby_coordinator_datadir | --standby_dir=standby_coordinator_datadir`**

如果通过 `-s` 配置 Standby Coordinator 主机，请使用此选项指定其数据目录。如果备用实例与 Coordinator 实例位于同一主机上，两者必须使用不同的数据目录。

**`-e superuser_password | --su_password=superuser_password`**

使用此选项指定 Apache Cloudberry 超级用户账户（如 `gpadmin`）的密码。如果未指定，将为超级用户账户设置默认密码 `gparray`。之后可以使用 `ALTER ROLE` 命令更改密码。

建议遵循的安全最佳实践：

- 生产环境不要使用默认密码选项。
- 安装后立即更改密码。

**`--mirror-mode={group|spread}`**

使用此选项指定镜像 Segment 实例在 Segment 主机上的放置方式。默认值 `group` 将某台主机上所有主 Segment 的镜像集中放在另一台主机上。`spread` 将该主机上各主 Segment 的镜像分散到 Apache Cloudberry 阵列中的不同主机。只有主机数量大于每台主机的 Segment 实例数量时，才允许分散放置。

**`-v | --version`**

打印 `gpinitsystem` 版本并退出。

**`-? | --help`**

显示 `gpinitsystem` 命令行参数的帮助并退出。

## 初始化配置文件格式 {#initialization-configuration-file-format}

`gpinitsystem` 要求提供定义了以下参数的集群配置文件。初始化配置文件示例位于 `$GPHOME/docs/cli_help/gpconfigs/gpinitsystem_config`。

为避免 Apache Cloudberry 与其他应用程序发生端口冲突，Apache Cloudberry 端口号不应位于操作系统参数 `net.ipv4.ip_local_port_range` 指定的范围内。例如，如果 `net.ipv4.ip_local_port_range = 10000 65535`，可以将 Apache Cloudberry 的基础端口号设为以下值。

```shell
PORT_BASE = 6000
MIRROR_PORT_BASE = 7000
```

**`MACHINE_LIST_FILE`**

**可选。** 可以代替 `-h` 选项使用。指定一个文件，其中列出组成 Apache Cloudberry 系统的 Segment 主机地址名。工具假定运行它的主机就是 Coordinator 主机，因此不应将其列入此文件。如果 Segment 主机有多个网络接口，则文件应包含该主机的所有地址。请提供文件的绝对路径。

**`SEG_PREFIX`**

**必需。** 指定用于命名 Coordinator 和 Segment 实例数据目录的前缀。Apache Cloudberry 系统的数据目录命名约定为 SEG_PREFIXnumber，其中 Segment 实例的 number 从 0 开始（Coordinator 始终为 -1）。例如，如果选择前缀 `gpseg`，Coordinator 实例的数据目录名为 `gpseg-1`，Segment 实例的数据目录名依次为 `gpseg0`、`gpseg1`、`gpseg2`、`gpseg3` 等。

**`PORT_BASE`**

**必需。** 指定计算主 Segment 端口号的基础值。主机上的第一个主 Segment 端口设为 `PORT_BASE`，每增加一个主 Segment，端口号递增 1。有效值为 1 到 65535。

**`DATA_DIRECTORY`**

**必需。** 指定工具创建主 Segment 数据目录的数据存储位置。列表中的位置数量决定每台物理主机创建的主 Segment 数量（如果主机文件中列出了某台主机的多个地址，Segment 将均匀分布在指定接口地址上）。如果希望在同一位置创建数据目录，可以多次列出同一数据存储区域。运行 `gpinitsystem` 的用户（如 `gpadmin`）必须具有这些目录的写权限。例如，以下配置将在每台主机上创建六个主 Segment：

```shell
declare -a DATA_DIRECTORY=(/data1/primary /data1/primary 
/data1/primary /data2/primary /data2/primary /data2/primary)
```

**`COORDINATOR_HOSTNAME`**

**必需。** Coordinator 实例的主机名，必须与机器配置的主机名完全一致（运行 `hostname` 命令确定正确的主机名）。

**`COORDINATOR_DIRECTORY`**

**必需。** 指定在 Coordinator 主机上创建数据目录的位置。必须确保运行 `gpinitsystem` 的用户（如 `gpadmin`）具有此目录的写权限。

**`COORDINATOR_PORT`**

**必需。** Coordinator 实例的端口号。用户和客户端连接访问 Apache Cloudberry 系统时使用此端口。

**`TRUSTED_SHELL`**

**必需。** `gpinitsystem` 工具在远程主机上运行命令所用的 shell。允许的值为 `ssh`。运行 `gpinitsystem` 工具前，必须建立主机间的信任关系（可使用 `gpssh-exkeys` 完成）。

**`ENCODING`**

**必需。** 要使用的字符集编码。该字符集必须与所用的 `--locale` 设置兼容，尤其是 `--lc-collate` 和 `--lc-ctype`。Apache Cloudberry 支持的字符集与 PostgreSQL 相同。

**`DATABASE_NAME`**

**可选。** 系统初始化后要创建的 Apache Cloudberry 数据库名称。也可以之后再使用 `CREATE DATABASE` 命令或 `createdb` 工具创建数据库。

**`MIRROR_PORT_BASE`**

**可选。** 指定计算镜像 Segment 端口号的基础值。主机上的第一个镜像 Segment 端口设为 `MIRROR_PORT_BASE`，每增加一个镜像 Segment，端口号递增 1。有效值为 1 到 65535，且不能与根据 `PORT_BASE` 计算的端口冲突。

**`MIRROR_DATA_DIRECTORY`**

**可选。** 指定工具创建镜像 Segment 数据目录的数据存储位置。为镜像 Segment 实例声明的数据目录数量必须与主 Segment 实例相同（参阅 `DATA_DIRECTORY` 参数）。运行 `gpinitsystem` 的用户（如 `gpadmin`）必须具有这些目录的写权限。例如：

```shell
declare -a MIRROR_DATA_DIRECTORY=(/data1/mirror 
/data1/mirror /data1/mirror /data2/mirror /data2/mirror 
/data2/mirror)
```

**`QD_PRIMARY_ARRAY, PRIMARY_ARRAY, MIRROR_ARRAY`**

使用 `-I` 选项配合 `input_configuration file` 时**必需**。这些参数分别指定 Apache Cloudberry Coordinator 主机、主 Segment 主机和镜像 Segment 主机。初始化新集群时，使用 `gpinitsystem` 的 `-O output_configuration_file` 填充 `QD_PRIMARY_ARRAY`、`PRIMARY_ARRAY` 和 `MIRROR_ARRAY`。

要初始化新集群或从备份配置重新创建集群，请编辑配合 `gpinitsystem` 的 `-I input_configuration_file` 选项使用的输入配置文件中的这些值。使用以下任一格式指定主机信息：

```shell
<hostname>~<address>~<port>~<data_directory>/<seg_prefix<segment_id>~<dbid>~<content_id>
```

或者

```shell
<host>~<port>~<data_directory>/<seg_prefix<segment_id>~<dbid>~<content_id>
```

第一种格式使用输入配置文件提供的 hostname 和 address 值填充 `gp_segment_configuration` 目录表的 `hostname` 和 `address` 字段。第二种格式将 `hostname` 和 `address` 字段填为相同的值，该值取自 host。

Apache Cloudberry Coordinator 的 Segment ID 和 content ID 始终为 -1。例如，`QD_PRIMARY_ARRAY` 的 seg_prefix `<segment_id>` 和 dbid 值使用 `-1` 表示 Coordinator 实例：

```shell
QD_PRIMARY_ARRAY=cdw~cdw~5432~/gpdata/coordinator/gpseg-1~1~-1
declare -a PRIMARY_ARRAY=(
sdw1~sdw1~40000~/gpdata/data1/gpseg0~2~0
sdw1~sdw1~40001~/gpdata/data2/gpseg1~3~1
sdw2~sdw2~40000~/gpdata/data1/gpseg2~4~2
sdw2~sdw2~40001~/gpdata/data2/gpseg3~5~3
)
declare -a MIRROR_ARRAY=(
sdw2~sdw2~50000~/gpdata/mirror1/gpseg0~6~0
sdw2~sdw2~50001~/gpdata/mirror2/gpseg1~7~1
sdw1~sdw1~50000~/gpdata/mirror1/gpseg2~8~2
sdw1~sdw1~50001~/gpdata/mirror2/gpseg3~9~3
)
```

要使用已知的 Apache Cloudberry 系统配置重新创建集群，可以编辑 Segment ID 和 content ID，使其与该系统的值一致。

**`HEAP_CHECKSUM`**

**可选。** 指定是否为堆数据启用校验和。启用后，会为所有数据库的堆存储计算校验和，使 Apache Cloudberry 能检测 I/O 系统中的损坏。此选项在系统初始化时设置，之后不能更改。

`HEAP_CHECKSUM` 选项默认开启，强烈建议不要关闭。如果将其设为 off，存储中的数据损坏可能无法被检测到，并使恢复困难得多。

要确定 Apache Cloudberry 系统是否启用了堆校验和，可以使用 `gpconfig` 管理工具查询 `data_checksums` 服务器配置参数：

```shell
$ gpconfig -s data_checksums
```

**`HBA_HOSTNAMES`**

**可选。** 此参数控制 `gpinitsystem` 更新 `pg_hba.conf` 文件中可连接 Apache Cloudberry 的地址时使用 IP 地址还是主机名。默认值为 `0`，即使用 IP 地址更新文件。初始化 Apache Cloudberry 系统时，指定 `HBA_HOSTNAMES=1` 可使工具在 `pg_hba.conf` 文件中使用主机名。

<!--For information about how Apache Cloudberry resolves host names in the `pg_hba.conf` file, see [Configuring Client Authentication](/cloudberry/security/client-auth/). -->

## 使用主机名或 IP 地址指定主机 {#specify-hosts-using-hostnames-or-ip-addresses}

使用 `gpinitsystem` 初始化 Apache Cloudberry 系统时，可以用主机名或 IP 地址指定 Segment 主机。例如，在 `-h` 选项指定的文件中，可以使用主机名或 IP 地址。

- 如果指定主机名，为安全起见，应在本地完成主机名到 IP 地址的解析。例如，应使用本地 `/etc/hosts` 文件中的条目将主机名映射到 IP 地址。不应通过公共 DNS 服务器等外部服务解析主机名。更改主机名到不同 IP 地址的映射前，必须停止 Cloudberry 系统。
- 如果指定 IP 地址，初始配置后不应更改该地址。启用 Segment 镜像后，如果 IP 地址与配置值不同，主 Segment 到镜像 Segment 的复制将失败。因此，除非有特定要求使用 IP 地址，否则初始化 Apache Cloudberry 系统时应使用主机名。

初始化 Apache Cloudberry 系统时，`gpinitsystem` 使用初始化信息填充 `gp_segment_configuration` 目录表，并将主机添加到 `pg_hba.conf` 文件中。默认添加主机 IP 地址。指定 `gpinitsystem` 配置文件参数 `HBA_HOSTNAMES=1`，可向文件中添加主机名。

Apache Cloudberry 使用 `gp_segment_configuration` 目录表的 `address` 值查找主机系统，以进行 Coordinator 与 Segment 实例之间、以及 Segment 实例之间的 Cloudberry Interconnect（内部）通信和其他内部通信。

## 示例 {#examples}

提供集群配置文件和 Segment 主机地址文件来初始化 Apache Cloudberry 系统，并设置分散镜像（`--mirror-mode=spread`）配置：

```shell
$ gpinitsystem -c gpinitsystem_config -h hostfile_gpinitsystem --mirror-mode=spread
```

初始化 Apache Cloudberry 系统，并设置超级用户远程访问密码：

```shell
$ gpinitsystem -c gpinitsystem_config -h hostfile_gpinitsystem --su-password=mypassword
```

初始化 Apache Cloudberry 系统，配置可选的 Standby Coordinator 主机：

```shell
$ gpinitsystem -c gpinitsystem_config -h hostfile_gpinitsystem -s host09
```

初始化 Apache Cloudberry 系统，并将提供的配置写入输出文件，例如 `cluster_init.config`：

```shell
$ gpinitsystem -c gpinitsystem_config -h hostfile_gpinitsystem -O cluster_init.config
```

输出文件使用 `QD_PRIMARY_ARRAY` 和 `PRIMARY_ARRAY` 参数定义 Coordinator 和 Segment 主机：

```shell
TRUSTED_SHELL=ssh
CHECK_POINT_SEGMENTS=8
ENCODING=UNICODE
SEG_PREFIX=gpseg
HEAP_CHECKSUM=on
HBA_HOSTNAMES=0
QD_PRIMARY_ARRAY=cdw~cdw.local~5433~/data/coordinator1/gpseg-1~1~-1
declare -a PRIMARY_ARRAY=(
cdw~cdw.local~6001~/data/primary1/gpseg0~2~0
)
declare -a MIRROR_ARRAY=(
cdw~cdw.local~7001~/data/mirror1/gpseg0~3~0
)
```

使用包含 `QD_PRIMARY_ARRAY` 和 `PRIMARY_ARRAY` 参数的输入配置文件（定义 Apache Cloudberry 集群的文件）初始化 Apache Cloudberry：

```shell
$ gpinitsystem -I cluster_init.config
```

以下示例使用配置了多个 NIC 的主机系统。如果主机系统配置了多个 NIC，可以初始化 Apache Cloudberry 系统，让每个 NIC 都作为 Cloudberry 主机系统使用。必须确保主机系统配置了足够的资源，以支持要添加到主机上的所有 Segment 实例。此外，如果启用了高可用，必须确保 Cloudberry 系统配置支持主机系统发生故障时的故障切换。

在这个简单的 Coordinator 和 Segment 实例配置中，主机系统 `gp7c` 配置了两个 NIC：`gp7c-1` 和 `gp7c-2`。`QD_PRIMARY_ARRAY` 参数通过 `gp7c-1` 定义 Coordinator Segment，`PRIMARY_ARRAY` 和 `MIRROR_ARRAY` 参数通过 `gp7c-2` 定义一个主 Segment 和一个镜像 Segment 实例。

```shell
QD_PRIMARY_ARRAY=gp7c~gp7c-1~5432~/data/coordinator/gpseg-1~1~-1
declare -a PRIMARY_ARRAY=(
gp7c~gp7c-2~40000~/data/data1/gpseg0~2~0
gp7s~gp7s~40000~/data/data1/gpseg1~3~1
)
declare -a MIRROR_ARRAY=(
gp7s~gp7s~50000~/data/mirror1/gpseg0~4~0
gp7c~gp7c-2~50000~/data/mirror1/gpseg1~5~1
)
```

## 另请参阅 {#see-also}

[gpssh-exkeys](/cloudberry/reference/sys-utilities/gpssh-exkeys/)、[gpdeletesystem](/cloudberry/reference/sys-utilities/gpdeletesystem/)、[启动和停止 Apache Cloudberry](/cloudberry/database-basic/start-and-stop-cbdb-database/)
