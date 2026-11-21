---
title: 在 2.x 系列内升级
description: 将 Apache Cloudberry 2.x 集群升级到后续 2.x 版本的操作步骤、验证、回退及故障排查。
weight: 500
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/sys-admin/migration-and-upgrade/upgrade-within-2x.md
---

本指南介绍如何将 Apache Cloudberry 2.x 集群升级到后续的 2.x 版本，例如从 2.0 或 2.1 升级到 2.2。

所有 2.x 版本使用相同的磁盘格式。升级时，先停止集群，替换每台主机上的 Apache Cloudberry 软件，再启动集群。无需移动或重新加载数据。这种过程也称为二进制替换。

> [!CAUTION]
> 此过程仅适用于使用 Apache Cloudberry 2.x 版本初始化的集群。使用 Cloudberry 1.x 初始化的集群采用不同的磁盘格式。这类集群请参阅[迁移与升级](/cloudberry/sys-admin/migration-and-upgrade/migration-and-upgrade/)。

## 开始之前 {#before-you-begin}

- **停机。** 升级期间集群停止服务。无法滚动升级，因为所有主机必须运行同一版本。
- **所有主机。** 必须替换 Coordinator 主机、Standby Coordinator 主机及每台 Segment 主机上的软件。
- **相同的构建选项。** 如果从源码构建 Apache Cloudberry，请使用与当前安装相同的 `configure` 选项。例如，不要更改块大小。
- **旧版本软件包。** 保留当前运行版本的软件包文件。安装新软件包会删除旧版本的文件，因此回退时需要旧软件包。
- **主机健康状况。** 确保所有主机的硬件正常，并且仍满足[软硬件要求](/cloudberry/deployment/platform-requirements/)。
- **发行说明。** 阅读目标版本的[发行说明](https://cloudberry.apache.org/releases)。新的 2.x 版本可能包含更新的 PostgreSQL 14 小版本。例如，2.2 将内核从 PostgreSQL 14.4 更新到 14.10。

## 在升级日之前检查系统目录 {#check-the-system-catalog-before-the-upgrade-day}

在升级前几天或几周的维护时段运行 `gpcheckcat` 工具。这样就有时间在计划升级前修复工具发现的问题。

1. 以受限模式启动集群。在此模式下，只有超级用户可以连接，避免其他活动造成误报。

    ```shell
    gpstop -a
    gpstart -a -R
    ```

2. 检查所有数据库的系统目录。

    ```shell
    gpcheckcat -A
    ```

3. 如果 `gpcheckcat` 报告不一致，请加上 `-g` 选项再次运行。工具会将修复这些不一致的 SQL 脚本写入指定目录。

    ```shell
    gpcheckcat -A -g <directory for the repair scripts>
    ```

    运行这些 SQL 脚本，然后再次运行 `gpcheckcat`。重复这些步骤，直到工具不再报告不一致。

4. 重新以正常模式启动集群。

    ```shell
    gpstop -a
    gpstart -a
    ```

如果无法限制对集群的访问，请运行 `gpcheckcat -A -O`。使用 `-O` 选项时，工具只运行在集群使用期间可以安全执行的检查。更多信息请参阅 [gpcheckcat](/cloudberry/reference/sys-utilities/gpcheckcat/)。

## 步骤 1：检查当前集群 {#step-1-check-the-current-cluster}

在 Coordinator 主机上以 `gpadmin` 用户执行以下步骤。

1. 记录当前版本。

    ```shell
    psql -d postgres -c "SELECT version();"
    ```

2. 确保所有 Segment 均已启动，且所有镜像均已同步。

    ```shell
    gpstate -e
    ```

    如果输出显示有 Segment 已停止或未同步，请先恢复它们。参阅[从 Segment 故障中恢复](/cloudberry/sys-admin/high-availability/recover-from-segment-failures/)。

3. 记录每个数据库中安装的扩展。

    ```sql
    SELECT extname, extversion FROM pg_extension ORDER BY 1;
    ```

4. 备份数据。参阅[备份与恢复](/cloudberry/sys-admin/backup-and-restore/)。

5. 记录当前软件的安装位置。

    ```shell
    echo $GPHOME
    ls -ld /usr/local/cloudberry-db*
    ```

6. 将环境文件的副本保存到安装目录之外。安装新软件包会删除或替换此文件，您对它所做的修改也会丢失。

    ```shell
    cp $GPHOME/cloudberry-env.sh ~/cloudberry-env.sh.before-upgrade
    ```

    如果从 2.0 升级，文件名为 `greenplum_path.sh`。如果也修改过其他主机上的此文件，请在每台相应主机上保存副本。

7. 在 `gpadmin` 用户的主目录中创建名为 `hostfile_all` 的文件。文件列出集群中的每台主机，每行一个主机名。本指南中的 `gpssh` 命令使用此文件。

    ```shell
    psql -d postgres -Atc "SELECT DISTINCT hostname FROM gp_segment_configuration ORDER BY 1;" > ~/hostfile_all
    cat ~/hostfile_all
    ```

## 步骤 2：停止集群 {#step-2-stop-the-cluster}

1. 停止连接集群的服务和作业，避免它们在升级期间失败或启动。例如：

    - `gpadmin` 用户的定时作业，例如用于备份、`VACUUM` 或 `ANALYZE` 的 `cron` 作业。
    - 数据加载作业及其使用的 `gpfdist` 进程。
    - PXF 服务（如果使用 PXF）。在 Coordinator 主机上运行 `pxf cluster stop`。
    - 监控工具和应用程序。

2. 确认没有客户端会话连接后，停止集群。`gpstop -a` 命令执行智能关闭：如果仍有客户端连接，它会等待，然后失败退出。

    ```shell
    gpstop -a
    ```

3. 确认所有主机上都没有遗留的 `postgres` 进程。

    ```shell
    gpssh -f ~/hostfile_all -e 'pgrep -u gpadmin -l postgres || echo "no postgres process"'
    ```

## 步骤 3：在每台主机上安装新版本 {#step-3-install-the-new-release-on-every-host}

选择与当前安装方式相符的方法。

### 获取软件包 {#get-the-package}

1. 从[发布页面](https://github.com/apache/cloudberry/releases)下载适用于当前操作系统的新版本软件包。

    某些版本提供的下载文件为 `.tar.gz`，其中包含软件包、签名（`.asc`）和校验和（`.sha512`）。解压文件，然后校验软件包。

    ```shell
    tar xzf <downloaded file>.tar.gz
    sha512sum -c <package file>.sha512
    ```

2. 将软件包文件复制到每台主机。

### RPM 软件包 {#rpm-package}

1. 在每台主机上以 `root` 用户或使用 `sudo` 安装软件包。

    ```shell
    sudo dnf install ./<new RPM package file>
    ```

    软件包将软件安装到带版本号的目录 `/usr/local/cloudberry-db-<version>`。

    从 2.1 升级到 2.2 时，由于软件包名称改变，`dnf` 还会删除 2.1 软件包。目录 `/usr/local/cloudberry-db-2.1.0` 会保留在磁盘上，但其中只剩下不属于软件包的文件。安装期间可能出现以下消息，可以忽略。

    ```
    Warning: /usr/local/cloudberry-db points to Cloudberry major version 2.1; leaving it unchanged so major versions can coexist
    ```

2. 在每台主机上将符号链接 `/usr/local/cloudberry-db` 指向新目录。从 2.1 升级到 2.2 后，该链接不存在，必须重新创建。

    ```shell
    sudo ln -sfn /usr/local/cloudberry-db-<version> /usr/local/cloudberry-db
    ls -ld /usr/local/cloudberry-db
    ```

3. 在每台主机上将新目录的所有权授予 `gpadmin` 用户。

    ```shell
    sudo chown -R gpadmin:gpadmin /usr/local/cloudberry-db*
    ```

> [!NOTE]
> `rpm --prefix` 选项的含义在 2.2 中发生了变化。在 2.2 中，前缀表示父目录。软件安装到 `<prefix>/cloudberry-db-<version>`，符号链接为 `<prefix>/cloudberry-db`。如果安装 2.1 时使用了 `--prefix`，请使用 `rpm -U --prefix=<parent directory>` 安装 2.2，然后更新 `gpadmin` 用户的 shell 启动文件中的 `source` 行，因为软件路径发生了变化。

### DEB 软件包 {#deb-package}

DEB 软件包将软件安装到不带版本号的目录 `/usr/cloudberry-db`。新软件包会替换旧版本的文件。

1. 保留旧版本的 DEB 软件包文件，回退时需要使用。

2. 在每台主机上以 `root` 用户或使用 `sudo` 安装软件包。

    ```shell
    sudo apt install ./<new DEB package file>
    ```

3. 将目录的所有权授予 `gpadmin` 用户。

    ```shell
    sudo chown -R gpadmin:gpadmin /usr/cloudberry-db /usr/local/cloudberry-db
    ```

### 从源码构建 {#build-from-source}

1. 使用与当前安装相同的 `configure` 选项构建新版本，但使用新的 `--prefix`，例如 `/usr/local/cloudberry-db-<version>`。参阅[从源码构建](/cloudberry/build/source/)。

2. 将构建结果安装到每台主机的相同路径。

3. 在每台主机上将符号链接指向新目录。

    ```shell
    sudo ln -sfn /usr/local/cloudberry-db-<version> /usr/local/cloudberry-db
    ```

### 更新环境文件 {#update-the-environment-file}

新安装包含新的 `cloudberry-env.sh` 文件。如果修改过旧版本的环境文件，请将新文件与[步骤 1](#step-1-check-the-current-cluster) 中保存的副本进行比较，然后在新文件中做相同修改。在每台修改过此文件的主机上执行此操作。例如：

- 如果集群使用 LDAP 认证，可能有 `export LDAPCONF=/etc/openldap/ldap.conf` 这样的行。
- 如果集群使用 PL/Java，可能设置了 `JAVA_HOME` 和 `LD_LIBRARY_PATH` 变量。

```shell
diff ~/cloudberry-env.sh.before-upgrade /usr/local/cloudberry-db/cloudberry-env.sh
```

某些扩展软件包在安装时也会修改环境文件。因此，旧文件中可能包含并非您手动添加的行。

### 补充不属于软件包的文件 {#add-the-files-that-are-not-part-of-the-package}

新安装目录仅包含 Apache Cloudberry 软件包中的文件。如果曾向旧安装目录添加文件，请在每台主机上将它们补充到新目录。例如：

- 单独构建和安装的扩展，例如 PXF 或其他第三方扩展。使用新版本重新构建它们，或安装与新版本匹配的软件包。
- 扩展使用的文件，例如 JAR 文件、共享对象文件和库。
- 复制到 `$GPHOME` 的自定义库、JDBC 驱动程序或脚本。

RPM 升级后，可以在旧版本目录（例如 `/usr/local/cloudberry-db-2.1.0`）中找到这类文件。

## 步骤 4：启动集群 {#step-4-start-the-cluster}

1. 在新的 shell 中加载新版本的环境，避免残留旧版本的变量。

    ```shell
    source /usr/local/cloudberry-db/cloudberry-env.sh
    ```

    > [!NOTE]
    > Apache Cloudberry 2.0 使用文件名 `greenplum_path.sh`，后续版本使用 `cloudberry-env.sh`。如果从 2.0 升级，请在每台主机上修改 `gpadmin` 用户的 shell 启动文件（例如 `~/.bashrc`）中的 `source` 行。

2. 启动集群。

    ```shell
    gpstart -a
    ```

## 步骤 5：验证升级 {#step-5-verify-the-upgrade}

1. 确认 Coordinator 运行新版本。

    ```shell
    psql -d postgres -c "SELECT version();"
    ```

2. 确认所有 Segment 运行同一版本。

    ```shell
    gpstate -i
    ```

    输出的最后一行必须为 `All segments are running the same software version`。

3. 确认所有 Segment 均已启动，且所有镜像均已同步。

    ```shell
    gpstate -e
    ```

4. 确认使用的功能正常工作。例如：

    - 运行一些日常查询。
    - 调用自定义函数。
    - 使用已安装的扩展，例如 PostGIS 或 MADlib。
    - 对一张小表执行备份与恢复。

## 步骤 6：执行升级后任务 {#step-6-do-the-post-upgrade-tasks}

1. 找出新版本中版本号更高的扩展。在每个数据库中运行此查询。

    ```sql
    SELECT e.extname, e.extversion AS installed, a.default_version AS available
    FROM pg_extension e
    JOIN pg_available_extensions a ON a.name = e.extname
    WHERE e.extversion <> a.default_version;
    ```

    更新查询返回的每个扩展。例如，2.2 包含的 `gp_toolkit` 版本高于 2.1。

    ```sql
    ALTER EXTENSION <extension name> UPDATE;
    ```

2. 如果目标版本的发行说明要求重新收集统计信息，请执行此操作。

    ```shell
    analyzedb -a -d <database name>
    ```

3. 重新启动[步骤 2](#step-2-stop-the-cluster) 中停止的服务和作业，例如 `cron` 作业和 PXF 服务（`pxf cluster start`）。

4. 确认不再需要回退后，从每台主机删除旧版本的目录或软件包。

## 回退 {#roll-back}

由于磁盘格式相同，可以用相同方式回退到之前的 2.x 版本。

1. 停止集群。

    ```shell
    gpstop -a
    ```

2. 在每台主机上启用旧版本。

    - **RPM 软件包。** 删除新版本的软件包，然后安装旧版本的软件包。必须先删除新软件包，因为它会替换旧软件包。`--noautoremove` 选项会在主机上保留依赖项。

        ```shell
        sudo dnf remove --noautoremove apache-cloudberry-db-incubating-2
        sudo dnf install ./<previous RPM package file>
        sudo chown -R gpadmin:gpadmin /usr/local/cloudberry-db*
        ls -ld /usr/local/cloudberry-db
        ```

        确认符号链接指向旧版本目录。如果没有，请使用 `ln -sfn` 重新创建。

    - **DEB 软件包。** 使用允许降级的选项安装旧版本的软件包。

        ```shell
        sudo apt install --allow-downgrades ./<previous DEB package file>
        sudo chown -R gpadmin:gpadmin /usr/cloudberry-db /usr/local/cloudberry-db
        ```

    - **从源码构建。** 将符号链接重新指向旧版本目录。

        ```shell
        sudo ln -sfn /usr/local/cloudberry-db-<previous version> /usr/local/cloudberry-db
        ```

3. 在新的 shell 中加载旧版本的环境，然后启动集群。

    ```shell
    gpstart -a
    ```

如果在步骤 6 中更新了扩展，旧版本不包含该扩展版本的文件。请先在测试环境中测试回退，或在更新扩展之前回退。

## 限制 {#limitations}

二进制替换会替换软件，但不会更改现有集群的系统目录。后续 2.x 版本新增的内置目录对象（例如新的内置函数）仅在使用该版本初始化的集群中可用。软件中的错误修复及其他变更照常适用于现有集群。

## 故障排查 {#troubleshooting}

### shell 找不到 `cloudberry-env.sh` 或 `gpstart` {#the-shell-cannot-find-cloudberry-envsh-or-gpstart}

`gpadmin` 用户的新 shell 显示类似以下消息，并且找不到 `gpstart` 等命令：

```
/usr/local/cloudberry-db/cloudberry-env.sh: No such file or directory
```

符号链接 `/usr/local/cloudberry-db` 不存在。这是从 2.1 通过 RPM 升级到 2.2 后的常见情况。按照[步骤 3](#step-3-install-the-new-release-on-every-host) 在每台主机上创建链接，然后打开新的 shell。

### `gpstart` 在运行 `pg_controldata` 时失败 {#gpstart-fails-in-pg_controldata}

`gpstart` 显示类似以下消息后停止：

```
gpstart:...-[CRITICAL]:-Error occurred: non-zero rc: -11
 Command was: '$GPHOME/bin/pg_controldata /data/coordinator/gpseg-1'
```

手动运行 `pg_controldata` 命令时，输出包含以下警告：

```
WARNING: Calculated CRC checksum does not match value stored in file.
Either the file is corrupt, or it has a different layout than this program
is expecting.  The results below are untrustworthy.

WARNING: invalid WAL segment size
```

最常见的原因是集群并非使用 2.x 版本初始化。例如，数据目录来自 Cloudberry 1.x。新软件无法读取该集群的控制文件。

`gpstart` 在启动实例之前就会停止，因此数据目录未被更改。恢复步骤如下：

1. 按照[回退](#roll-back) 中的说明，在每台主机上重新启用旧软件。
2. 使用旧软件启动集群。
3. 将数据迁移到新的 2.x 集群。参阅[迁移与升级](/cloudberry/sys-admin/migration-and-upgrade/migration-and-upgrade/)。

### 服务器报告数据库文件不兼容 {#the-server-reports-that-the-database-files-are-incompatible}

实例无法启动，日志中包含类似以下消息：

```
FATAL:  database files are incompatible with server
```

消息的详情行会指出哪个值不同，例如块大小。新软件的构建选项与初始化该集群的软件不同。请安装使用相同选项构建的软件。

### `gpstart` 报告各主机版本不同 {#gpstart-reports-different-versions-on-the-hosts}

部分主机仍在运行旧版本。在每台主机（包括 Standby Coordinator 主机）上执行[步骤 3](#step-3-install-the-new-release-on-every-host)，然后确认所有主机上的符号链接都指向新目录。

```shell
gpssh -f ~/hostfile_all -e 'ls -ld /usr/local/cloudberry-db; /usr/local/cloudberry-db/bin/postgres --gp-version'
```

### 获取帮助 {#get-help}

如果无法解决问题，请向社区求助。邮件列表和 GitHub 等渠道见[支持](https://cloudberry.apache.org/support)。报告中请提供以下信息：

- 升级前的版本、升级后的版本、操作系统和软件包类型。
- 本指南中已完成的步骤及失败的步骤。
- 完整错误消息，以及 `gpstop`、`gpstart` 和 `gpcheckcat` 工具的日志文件。这些日志位于 Coordinator 主机上 `gpadmin` 用户的 `~/gpAdminLogs` 目录。
- 未能启动的实例的日志文件。它位于该实例数据目录下的 `log` 目录（部分安装使用 `pg_log`）。
