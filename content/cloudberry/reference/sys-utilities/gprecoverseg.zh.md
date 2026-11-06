---
title: "gprecoverseg"
description: "恢复标记为停机的主 Segment 或镜像 Segment 实例（已启用镜像时）。"
weight: 240
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gprecoverseg.md"
---

## 概要 {#synopsis}

```shell
gprecoverseg [[-p <new_recover_host>[,...]] | -i <recover_config_file>] [-d <coordinator_data_directory>] 
             [-b <segment_batch_size>] [-B <batch_size>] [-F [-s]] [-a] [-q] [--differential]
	           [--hba-hostnames <boolean>] 
             [--no-progress] [-l <logfile_directory>]

gprecoverseg -r [--replay-lag <replay_lag>] [--disable-replay-lag]

gprecoverseg -o <output_recover_config_file> 
             [-p <new_recover_host>[,...]]

gprecoverseg -? | -h | --help
        
gprecoverseg -v | --verbose

gprecoverseg --version
```

## 说明 {#description}

在启用了镜像的系统中，`gprecoverseg` 工具重新激活故障 Segment 实例，并识别需要重新同步的已更改数据库文件。`gprecoverseg` 完成此过程后，系统进入 `Not in Sync` 模式，直到恢复的 Segment 更新到最新状态。重新同步期间，系统保持在线并可正常运行。

增量恢复期间（未指定 `-F` 选项），如果 `gprecoverseg` 在已启用镜像的系统中检测到某个 Segment 实例禁用了镜像，此工具会报告该 Segment 已禁用镜像，不尝试恢复该实例，并继续恢复过程。

Segment 实例可能因主机故障、网络故障或磁盘故障等多种原因失败。Segment 实例发生故障时，其在 Apache Cloudberry 系统目录中的状态被标记为 `d`（停机），其镜像以 `Not in Sync` 模式激活。要使故障 Segment 实例重新运行，必须先修复导致故障的问题，再使用 `gprecoverseg` 在 Apache Cloudberry 中恢复该实例。

使用 `gprecoverseg` 恢复 Segment 时，必须有可作为恢复来源的活动镜像。如果系统未启用镜像，或发生双重故障（一对主实例和镜像同时停机），必须手动恢复故障 Segment 实例，然后重启系统，使这些 Segment 重新上线。例如，以下命令重启系统。

```shell
gpstop -r
```

默认情况下，故障 Segment 会就地恢复，即在最初配置的同一主机和同一数据目录位置重新上线。此时，恢复配置文件（使用 `-i`）应采用以下格式。注意，`failed_host_name` 是可选参数。

```shell
<failed_host_name>|<failed_host_address>|<port>|<data_directory> 
```

某些情况下，可能无法就地恢复（例如主机遭到物理损坏且无法修复）。此时，`gprecoverseg` 允许将故障 Segment 恢复到全新的主机（使用 `-p`），或现存正常 Segment 主机上的其他数据目录位置（使用 `-s`），也可以提供如下格式的恢复配置文件（使用 `-i`）。`<SPACE>` 表示必需的空格位置，不要添加额外空格。参数 `failed_host_name` 是可选的。

```shell
<failed_host_name>|<failed_host_address>|<port>|<data_directory><SPACE><recovery_host_name>|<recovery_host_address>|<port>|<data_directory>
```

有关恢复配置文件的详细信息和示例，请参阅下面的 `-i` 选项。

`gp_segment_configuration` 系统目录表可以帮助确定当前 Segment 配置，以便规划镜像恢复配置。例如，运行以下查询：

```sql
=# SELECT dbid, content, address, port, datadir 
   FROM gp_segment_configuration
   ORDER BY dbid;
```

新的恢复 Segment 主机必须预先安装 Apache Cloudberry 软件，并且配置必须与现有 Segment 主机完全相同。所有当前配置的 Segment 主机上都必须有备用数据目录位置，且磁盘空间足以容纳故障 Segment。

恢复过程会在 Apache Cloudberry 系统目录中将 Segment 重新标记为运行状态，然后启动重新同步，使该 Segment 的事务状态更新到最新。处于 `Not in Sync` 模式期间，系统仍然在线可用。

## 选项 {#options}

**`-a (do not prompt)`**

不提示用户确认。

**`-b segment_batch_size`**

每台主机并行操作的最大 Segment 数量。有效值为 `1` 到 `128`。如果未指定，此工具会在每台主机上并行恢复最多 64 个 Segment。

**`-B batch_size`**

并行处理的主机数。如果未指定，此工具会并行处理最多 16 台主机。有效值为 `1` 到 `64`。

**`-d coordinator_data_directory`**

可选。Coordinator 主机的数据目录。如果未指定，将使用 `$COORDINATOR_DATA_DIRECTORY` 的值。

**`-F (full recovery)`**

可选。完整复制活动 Segment 实例以恢复故障 Segment，而非采用默认行为，仅复制 Segment 停机期间发生的更改。

>**小心**
>完整恢复会先删除停机 Segment 实例的数据目录，再从活动（当前主）Segment 实例复制数据。执行完整恢复前，确保 Segment 故障未造成数据损坏，且主机 Segment 的所有磁盘问题都已修复。

此外，完整恢复不会还原 Segment 实例数据目录中存储的自定义文件，即使活动 Segment 实例中也有这些文件。必须手动还原自定义文件。例如，使用 `gpfdists` 协议（启用 SSL 加密的 `gpfdist`）管理外部数据时，需要在 Segment 实例的 `$PGDATA/gpfdists` 目录中存放客户端证书文件。这些文件不会被还原。

<!-- For information about configuring `gpfdists`, see [Encrypting gpfdist Connections](/cloudberry/security/encrypt-data-and-db-connections/). -->

使用 `-s` 选项可为每个 Segment 每秒输出一个新行，也可以使用 `--no-progress` 选项完全禁用进度报告。如果先前完整恢复失败，想在再次完整恢复时避免复制整个数据目录，可使用 `gprecoverseg` 的 `--differential` 选项，跳过自上次 `gprecoverseg` 运行以来未更改的文件和目录，缩短完整恢复耗时。

**`--differential (Differential recovery)`**

可选。对活动 Segment 实例执行差异复制，以恢复故障 Segment。默认仅复制 Segment 停机期间发生的增量更改。

**`--hba-hostnames boolean`**

可选。控制此工具更新 `pg_hba.conf` 文件中可连接 Apache Cloudberry 的地址时使用 IP 地址还是主机名。设为 0（默认值）时，使用 IP 地址更新文件；设为 1 时，使用主机名更新文件。为保持一致，应使用初始化 Apache Cloudberry 系统时为 `HBA_HOSTNAMES` 指定的相同值。

<!-- For information about how Apache Cloudberry resolves host names in the `pg_hba.conf` file, see [Configuring Client Authentication](/cloudberry/security/client-auth/). -->

**`-i recover_config_file`**

指定包含待恢复故障 Segment 详细信息的文件名。

配置文件中每行指定一个待恢复的 Segment。每行可采用两种格式之一。就地（增量）恢复时，在行中输入一组以竖线分隔的字段。例如：

```shell
failedAddress|failedPort|failedDataDirectory
```

或者

```shell
failedHostname|failedAddress|failedPort|failedDataDirectory
``` 

恢复到新位置时，在行中输入两组字段，中间用一个空格分隔。必需的空格用 `<SPACE>` 表示。不要添加额外空格。

```shell
failedAddress|failedPort|failedDataDirectory<SPACE>newAddress|newPort|newDataDirectory
```

或者

```shell
failedHostname|failedAddress|failedPort|failedDataDirectory<SPACE>newHostname|newAddress|newPort|newDataDirectory
```

> **注意** 以 `#` 开头的行被视为注释并忽略。

### 示例 {#examples}

**就地（增量）恢复单个镜像**

```shell
sdw1-1|50001|/data1/mirror/gpseg16
```

**将单个镜像恢复到新主机**

```shell
sdw1-1|50001|/data1/mirror/gpseg16<SPACE>sdw4-1|50001|/data1/recover1/gpseg16
```

### 获取示例文件 {#obtain-a-sample-file}

可以使用 `-o` 选项输出示例恢复配置文件作为起点。输出文件列出当前无效的 Segment 及其默认恢复位置。此文件格式可配合 `-i` 选项用于就地（增量）恢复。

**`-l logfile_directory`**

写入日志文件的目录。默认为 `~/gpAdminLogs`。

**`-o output_recover_config_file`**

指定输出示例恢复配置文件的文件名和位置。如有需要，可编辑此文件以提供其他恢复位置。以下示例输出默认恢复配置文件：

```shell
$ gprecoverseg -o /home/gpadmin/recover_config_file
```

**`-p new_recover_host[,...]`**

指定当前配置的 Apache Cloudberry 阵列之外的新主机，用于恢复无效 Segment。

新主机必须已安装并配置 Apache Cloudberry 软件，且硬件和操作系统配置与当前 Segment 主机相同（操作系统版本、区域设置、`gpadmin` 用户账户、已创建的数据目录位置、已交换的 ssh 密钥、网络接口数量及命名约定等）。具体而言，必须安装 Apache Cloudberry 二进制文件，新主机必须能够免密连接所有 Segment 及 Cloudberry Coordinator，并应用所有其他 Apache Cloudberry 特有的操作系统配置参数。

> **注意** 如果多台 Segment 主机发生故障，可以使用逗号分隔的列表指定要恢复的主机。不过，强烈建议一次只恢复一台主机。如果必须同时恢复多台主机，则务必确保不会出现主 Segment 及其对应镜像同时离线的双重故障情况。

**`-q (no screen output)`**

以静默模式运行。命令输出不显示在屏幕上，但仍会写入日志文件。

**`-r (rebalance segments)`**

恢复 Segment 后，Segment 实例可能未回到系统初始化时赋予的首选角色。这可能使系统处于不均衡状态，因为某些 Segment 主机上的活动 Segment 数量可能超过实现最佳系统性能所需的数量。此选项通过使主 Segment 和镜像 Segment 返回首选角色来重新平衡它们。运行 `gprecoverseg -r` 前，所有 Segment 必须有效且已完成重新同步。如果有查询正在执行，这些查询将被取消并回滚。

**`--replay-lag`**

重新平衡 Segment 时，允许镜像存在的重放延迟（GB）。默认值为 10 GB。如果 replay_lag（flush_lsn-replay_lsn）大于此选项指定的值，将中止重新平衡。

**`--disable-replay-lag`**

重新平衡 Segment 时禁用重放延迟检查。

**`-s (sequential progress)`**

按顺序显示 `pg_basebackup` 或 `pg_rewind` 的进度，而不是原地刷新。写入文件或 tty 不支持转义序列时，此选项很有用。默认原地显示进度。

**`--no-progress`**

不显示 `pg_basebackup`、`pg_rewind` 或 `rsync` 工具的进度报告。默认显示进度。

**`--differential`**

可选。完整恢复期间，仅将自 Segment 故障以来发生更改的文件和目录从主 Segment 复制到镜像 Segment。`--differential` 选项仅适用于就地完整恢复。

<!-- See [Recovery Scenarios](/cloudberry/sys-admin/high-availability/recover-from-segment-failures/) for more information on in-place recovery versus recovery to a different host. -->

>**注意**
> `--differential` 选项不能与以下任一 `gprecoverseg` 选项组合使用：`-i`、`-o`、`-F` 或 `-p`。

**`-v | --verbose`**

将日志输出级别设为 verbose。

**`--version`**

显示此工具的版本。

**`-? | -h | --help`**

显示在线帮助。

## 示例 {#examples-1}

**示例 1：就地恢复故障 Segment**

就地恢复所有故障 Segment 实例：

```shell
$ gprecoverseg
```

**示例 2：重新平衡未处于首选角色的故障 Segment**

首先验证所有 Segment 均已启动并运行、重新同步已完成，且存在**未**处于首选角色的 Segment：

```shell
$ gpstate -e
```

然后，如有必要，重新平衡 Segment：

```shell
$ gprecoverseg -r
```

**示例 3：将故障 Segment 恢复到独立主机**

将所有故障 Segment 实例恢复到新配置的 Segment 主机：

```shell
$ gprecoverseg -i <recover_config_file>
```

## 另请参阅 {#see-also}

[gpstart](/cloudberry/reference/sys-utilities/gpstart/), [gpstop](/cloudberry/reference/sys-utilities/gpstop/)
