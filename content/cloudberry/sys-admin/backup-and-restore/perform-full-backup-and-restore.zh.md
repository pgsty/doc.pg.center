---
title: "执行全量备份与恢复"
description: "Apache Cloudberry 支持并行备份和恢复整个数据库。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/backup-and-restore/perform-full-backup-and-restore.md"
---

无论系统中 Segment 的数量是多少，并行操作都可以扩展，因为每个 Segment 主机会同时将数据写入本地磁盘存储。

`gpbackup` 和 `gprestore` 是 Apache Cloudberry 的命令行工具，用于创建和恢复 Apache Cloudberry 的备份集。默认情况下，`gpbackup` 仅将备份所需的对象元数据文件和 DDL 文件存储在 Apache Cloudberry Coordinator 数据目录中。Apache Cloudberry Segment 使用 `COPY ... ON SEGMENT` 命令，将备份表的数据存储在压缩的 CSV 数据文件中，这些文件位于每个 Segment 的备份目录中。

备份元数据文件包含 `gprestore` 并行恢复完整备份集所需的全部信息。每个 `gpbackup` 任务在 Apache Cloudberry 中使用一个事务。在该事务期间，元数据在 Coordinator 主机上备份；每个 Segment 主机上每张表的数据则通过 `COPY ... ON SEGMENT` 命令并行写入 CSV 备份文件。备份过程会对每张被备份的表获取 `ACCESS SHARE` 锁。

## 安装 `gpbackup` 和 `gprestore` 工具 {#install-the-gpbackup-and-gprestore-utilities}

安装 `gpbackup` 和 `gprestore` 工具前，请确保已安装 [Golang](https://golang.org/doc/)（v1.21 或更高版本），并设置了 [Go `PATH` 环境变量](https://go.dev/doc/install)：
variable](https://go.dev/doc/install):

  ```
  ## Set the Go `PATH` environment variable
  export GOPATH=$HOME/go
  export PATH=$PATH:/usr/local/go/bin:$GOPATH/bin
  ```

1. 将 `apache/cloudberry-backup` GitHub 仓库拉取到目标机器。

    ```bash
    go install github.com/apache/cloudberry-backup@latest
    ```

    仓库位于 `$GOPATH/pkg/mod/github.com/apache/cloudberry-backup`。

2. 进入 `apache/cloudberry-backup` 目录，然后构建并安装源代码：

    ```bash
    cd <$GOPATH/pkg/mod/github.com/apache/cloudberry-backup>
    make depend
    make build
    ```

    运行 `make depend` 后，可能会遇到 `fatal: Not a git repository (or any of the parent directories): .git` 提示。可以忽略该提示，因为它不会影响构建。

    `build` 目标会将 `gpbackup` 和 `gprestore` 二进制文件放入 `$HOME/go/bin`。该操作还会尝试将 `gpbackup_helper` 复制到 Apache Cloudberry Segment（通过从 `gp_segment_configuration` 获取主机名）。

3. 检查 `$HOME/go/bin` 目录是否包含 `gpback`、`gprestore` 和 `gpbackup_helper`，以确认构建成功。

    ```bash
    ls $HOME/go/bin
    ```

4. 验证安装是否成功：

    ```bash
    gpbackup --version
    gprestore --version
    ```

## 备份整个数据库 {#back-up-the-full-database}

要备份完整数据库以及 Apache Cloudberry 系统元数据，请使用命令：

```bash
gpbackup --dbname <database_name>
```

例如：

```bash
$ gpbackup --dbname test_04

20240108:17:17:18 gpbackup:gpadmin:cbdb-coordinator:001945-[INFO]:-gpbackup version = 1.2.7-beta1+dev.7
20240108:17:17:18 gpbackup:gpadmin:cbdb-coordinator:001945-[INFO]:-Apache Cloudberry Version = oudberry Database 1.0.0 build 5551471267
20240108:17:17:18 gpbackup:gpadmin:cbdb-coordinator:001945-[INFO]:-Starting backup of database test_04
20240108:17:17:18 gpbackup:gpadmin:cbdb-coordinator:001945-[INFO]:-Backup Timestamp = 20240108171718
20240108:17:17:18 gpbackup:gpadmin:cbdb-coordinator:001945-[INFO]:-Backup Database = test_04
20240108:17:17:18 gpbackup:gpadmin:cbdb-coordinator:001945-[INFO]:-Gathering table state information
20240108:17:17:18 gpbackup:gpadmin:cbdb-coordinator:001945-[INFO]:-Acquiring ACCESS SHARE locks on tables
20240108:17:17:18 gpbackup:gpadmin:cbdb-coordinator:001945-[INFO]:-Gathering additional table metadata
20240108:17:17:18 gpbackup:gpadmin:cbdb-coordinator:001945-[INFO]:-Getting storage information
20240108:17:17:18 gpbackup:gpadmin:cbdb-coordinator:001945-[WARNING]:-No tables in backup set contain data. Performing metadata-only backup instead.
20240108:17:17:18 gpbackup:gpadmin:cbdb-coordinator:001945-[INFO]:-Metadata will be written to /data0/coordinator/gpseg-1/backups/20240108/20240108171718/gpbackup_20240108171718_metadata.sql
20240108:17:17:18 gpbackup:gpadmin:cbdb-coordinator:001945-[INFO]:-Writing global database metadata
20240108:17:17:18 gpbackup:gpadmin:cbdb-coordinator:001945-[INFO]:-Global database metadata backup complete
20240108:17:17:18 gpbackup:gpadmin:cbdb-coordinator:001945-[INFO]:-Writing pre-data metadata
20240108:17:17:18 gpbackup:gpadmin:cbdb-coordinator:001945-[INFO]:-Pre-data metadata metadata backup complete
20240108:17:17:18 gpbackup:gpadmin:cbdb-coordinator:001945-[INFO]:-Writing post-data metadata
20240108:17:17:18 gpbackup:gpadmin:cbdb-coordinator:001945-[INFO]:-Post-data metadata backup complete
20240108:17:17:19 gpbackup:gpadmin:cbdb-coordinator:001945-[INFO]:-Found neither /usr/local/cloudberry-1.0.0/bin/gp_email_contacts.yaml nor /home/gpadmin//gp_email_contacts.yaml
20240108:17:17:19 gpbackup:gpadmin:cbdb-coordinator:001945-[INFO]:-Email containing gpbackup report /data0/coordinator/gpseg-1/backups/20240108/20240108171718/gpbackup_20240108171718_report will not be sent
20240108:17:17:19 gpbackup:gpadmin:cbdb-coordinator:001945-[INFO]:-Backup completed successfully
```

以上命令会在默认目录 `$COORDINATOR_DATA_DIRECTORY/backups/<YYYYMMDD>/<YYYYMMDDHHMMSS>/` 中的 Apache Cloudberry Coordinator 主机上创建包含全局元数据和数据库专属元数据的文件。例如：

```bash
ls $COORDINATOR_DATA_DIRECTORY/backups/20240108/20240108171718

gpbackup_20240108171718_config.yaml   gpbackup_20240108171718_report
gpbackup_20240108171718_metadata.sql  gpbackup_20240108171718_toc.yaml
```

默认情况下，每个 Segment 会将备份中每张表的数据分别存储在 `<seg_dir>/backups/<YYYYMMDD>/<YYYYMMDDHHMMSS>/` 中的压缩 CSV 文件内。例如：

```bash
ls /data1/primary/gpseg1/backups/20240108/20240108171718/

gpbackup_0_20240108171718_17166.gz  gpbackup_0_20240108171718_26303.gz
gpbackup_0_20240108171718_21816.gz
```

要将所有备份文件集中到一个目录，请包含 `--backup-dir` 选项。注意，必须为此选项指定绝对路径：

```bash
$ gpbackup --dbname test_04 --backup-dir /home/gpadmin/backups

20240108:17:34:10 gpbackup:gpadmin:cbdb-coordinator:003348-[INFO]:-gpbackup version = 1.2.7-beta1+dev.7
20240108:17:34:10 gpbackup:gpadmin:cbdb-coordinator:003348-[INFO]:-Apache Cloudberry Version = oudberry Database 1.0.0 build 5551471267
...
20240108:17:34:12 gpbackup:gpadmin:cbdb-coordinator:003348-[INFO]:-Backup completed successfully

$ find /home/gpadmin/backups/ -type f

/home/gpadmin/backups/gpseg0/backups/20240108/20240108173410/gpbackup_0_20240108173410_16593.gz
/home/gpadmin/backups/gpseg-1/backups/20240108/20240108173410/gpbackup_20240108173410_config.yaml
/home/gpadmin/backups/gpseg-1/backups/20240108/20240108173410/gpbackup_20240108173410_report
/home/gpadmin/backups/gpseg-1/backups/20240108/20240108173410/gpbackup_20240108173410_toc.yaml
/home/gpadmin/backups/gpseg-1/backups/20240108/20240108173410/gpbackup_20240108173410_metadata.sql
/home/gpadmin/backups/gpseg1/backups/20240108/20240108173410/gpbackup_1_20240108173410_16593.gz
```

执行备份操作时，如果多个文件产生的额外开销可能过大，可以使用 `--single-data-file`。例如，在使用 Data Domain 等第三方存储方案保存备份时。

> [!TIP]
> 备份物化视图不会备份物化视图数据，只会备份物化视图定义。

## 恢复整个数据库 {#restore-the-full-database}

要使用 `gprestore` 从备份集恢复，必须使用 `--timestamp` 选项指定要恢复的精确时间戳值（`YYYYMMDDHHMMSS`）。如果数据库不存在于集群中，请包含 `--create-db` 选项。例如：

```bash
$ dropdb demo
$ gprestore --timestamp 20240108171718 --create-db

20240108:17:42:26 gprestore:gpadmin:cbdb-coordinator:004115-[INFO]:-Restore Key = 20240108171718
20240108:17:42:26 gprestore:gpadmin:cbdb-coordinator:004115-[INFO]:-gpbackup version = 1.2.7-beta1+dev.7
20240108:17:42:26 gprestore:gpadmin:cbdb-coordinator:004115-[INFO]:-gprestore version = 1.2.7-beta1+dev.7
20240108:17:42:26 gprestore:gpadmin:cbdb-coordinator:004115-[INFO]:-Apache Cloudberry Version = oudberry Database 1.0.0 build 5551471267
20240108:17:42:26 gprestore:gpadmin:cbdb-coordinator:004115-[INFO]:-Creating database
20240108:17:42:26 gprestore:gpadmin:cbdb-coordinator:004115-[INFO]:-Database creation complete for: test_04
20240108:17:42:26 gprestore:gpadmin:cbdb-coordinator:004115-[INFO]:-Restoring pre-data metadata
Pre-data objects restored:  3 / 3 [=================================] 100.00% 0s
20240108:17:42:26 gprestore:gpadmin:cbdb-coordinator:004115-[INFO]:-Pre-data metadata restore complete
20240108:17:42:26 gprestore:gpadmin:cbdb-coordinator:004115-[INFO]:-Restoring post-data metadata
20240108:17:42:26 gprestore:gpadmin:cbdb-coordinator:004115-[INFO]:-Post-data metadata restore complete
20240108:17:42:26 gprestore:gpadmin:cbdb-coordinator:004115-[INFO]:-Found neither /usr/local/cloudberry-1.0.0/bin/gp_email_contacts.yaml nor /home/gpadmin//gp_email_contacts.yaml
20240108:17:42:26 gprestore:gpadmin:cbdb-coordinator:004115-[INFO]:-Email containing gprestore report /data0/coordinator/gpseg-1/backups/20240108/20240108171718/gprestore_20240108171718_20240108174226_report will not be sent
20240108:17:42:26 gprestore:gpadmin:cbdb-coordinator:004115-[INFO]:-Restore completed successfully
```

如果指定了自定义 `--backup-dir` 来集中备份文件，使用 `gprestore` 时也要包含相同的 `--backup-dir` 选项，以定位备份文件：

```bash
$ dropdb test_04
$ gprestore --backup-dir /home/gpadmin/backups/ --timestamp 20240109102646 --create-db

20240109:10:33:17 gprestore:gpadmin:cbdb-coordinator:017112-[INFO]:-Restore Key = 20240109102646
...
20240109:10:33:17 gprestore:gpadmin:cbdb-coordinator:017112-[INFO]:-Restore completed successfully
```

默认情况下，`gprestore` 不会尝试恢复 Apache Cloudberry 系统的全局元数据。如果需要恢复，请包含 `--with-globals` 参数。

默认情况下，`gprestore` 使用 1 个连接恢复表数据和元数据。如果备份集较大，可以使用 `--jobs` 选项增加并行连接数，以提高恢复性能。例如：

```bash
$ gprestore --backup-dir /home/gpadmin/backups/ --timestamp 20240109102646 --create-db --jobs 4
```

使用备份集测试并行连接数，以确定快速恢复所需的理想数量。

> [!TIP]
> 如果备份使用 gpbackup 的 `--single-data-file` 选项，将每个 Segment 的表备份合并为一个文件，则不能使用 `gprestore` 执行并行恢复操作。

恢复物化视图不会恢复物化视图数据，只会恢复物化视图定义。要使用数据填充物化视图，请使用 `REFRESH MATERIALIZED VIEW`。刷新物化视图时，物化视图定义引用的表必须可用。`gprestore` 日志文件会列出已恢复的物化视图，以及用于向物化视图填充数据的 `REFRESH MATERIALIZED VIEW` 命令。

## 过滤备份或恢复的内容 {#filter-the-contents-of-a-backup-or-restore}

### 按模式过滤 {#filter-by-schema}

`gpbackup` 会备份指定数据库中的所有模式和表，除非使用模式级或表级过滤选项排除或包含单独的模式或表对象。

模式级选项是 gpbackup 的 `--include-schema`、`--include-schema-file`、`--exclude-schema` 或 `--exclude-schema-file` 命令行选项。例如，如果 `test_04` 数据库只包含 `schema1` 和 `schema2` 两个模式，以下两个命令都会只备份 `schema1` 模式：

```bash
$ gpbackup --dbname test_04 --include-schema schema1
$ gpbackup --dbname test_04 --exclude-schema schema2
```

可以在 `gpbackup` 中多次指定 `--include-schema`，也可以多次指定 `--exclude-schema`。例如：

```bash
$ gpbackup --dbname test_04 --include-schema schema1 --include-schema schema2
```

如果模式数量很多，可以将模式列在文本文件中，并在 `gpbackup` 命令中使用 `--include-schema-file` 或 `--exclude-schema-file` 选项指定该文件。文件每行必须定义一个模式，且不能包含尾随行。例如，以下命令使用 `gpadmin` 主目录中的文件来包含一组模式。

```bash
$ gpbackup --dbname test_04 --include-schema-file /home/gpadmin/backup-schemas.txt --backup-dir /home/gpadmin/backups
```

> [!TIP]
> 备份时间戳（`YYYYMMDDHHMMSS`）的精度为一秒，`gpbackup` 不能使用相同时间戳启动两个备份。如果在脚本中逐个备份模式，且新备份在前一个备份开始后的同一秒内启动，则会失败并显示错误 `A backup with timestamp <timestamp> is already in progress. Wait 1 second and try the backup again.`。为避免此问题，请在 `gpbackup` 命令之间增加延迟（例如 `sleep 1`），或像上面那样在一个 `gpbackup` 命令中包含所有目标模式。

### 按表过滤 {#filter-by-table}

要过滤备份集中包含或排除的单个表，请使用 `--include-table` 或 `--exclude-table` 选项指定单个表。表必须限定模式名，格式为 `<schema-name>.<table-name>`。单表过滤选项可以多次指定。但是，`--include-table` 和 `--exclude-table` 不能在同一个命令中同时使用。

> [!TIP]
> 如果在 `gpbackup` 命令中使用了 `--include-table` 选项，则不会备份所指定目标表相关的数据库、模式和序列。恢复备份集前，必须手动创建数据库、模式和序列。
>
> 例如，如果使用 `gpbackup --dbname test_04 --include-table schema1.table1 --backup-dir /home/gpadmin/backups` 备份 `test_04` 数据库，则必须在恢复备份集前手动创建 `test_04` 数据库、`schema1` 模式和 `schema1.table1_id_seq` 序列。否则，恢复操作会失败，并显示数据库、模式或序列不存在的错误消息。

如果表名或模式名包含小写字母、数字或下划线以外的字符，则必须将名称放在双引号中。例如：

```bash
gpbackup --dbname test1 --include-table "schema1"."ComplexName Table" --backup-dir /home/gpadmin/backups
```

可以在文本文件中创建限定表名列表。列出表时，文本文件的每一行必须使用 `<schema-name>.<table-name>` 格式定义一张表。即使表名或模式名包含小写字母、数字或下划线以外的字符，文件也不能包含尾随行或双引号。例如：

```
schema1.table1
schema2.table2
schema1.ComplexName Table
```

创建文件后，可以使用 gpbackup 的 `--include-table-file` 或 `--exclude-table-file` 选项来包含或排除表。例如：

```bash
$ gpbackup --dbname test_04 --include-table-file /home/gpadmin/table-list.txt
```

可以在备份时将 `--include schema` 与 `--exclude-table` 或 `--exclude-table-file` 组合使用。以下示例使用 `--include-schema` 和 `--exclude-table` 备份一个模式，但排除其中一张表。

```bash
$ gpbackup --dbname test_04 --include-schema schema1 --exclude-table schema2.table2
```

不能将 `--include-schema` 与 `--include-table` 或 `--include-table-file` 组合使用，也不能将 `--exclude-schema` 与任何表过滤选项（例如 `--exclude-table` 或 `--include-table`）组合使用。

使用 `--include-table` 或 `--include-table-file` 时，不会自动备份或恢复依赖对象，必须明确指定所需的依赖对象。例如，备份或恢复视图或物化视图时，还必须指定该视图或物化视图使用的表。备份或恢复使用序列的表时，也必须指定该序列。

### 使用 `gprestore` 过滤 {#filter-with-gprestore}

使用 `gpbackup` 创建备份集后，可以使用 `gprestore --include-schema` 和 `--include-table-file` 选项，过滤要从备份集中恢复的模式和表。这些选项的工作方式与 `gpbackup` 对应选项相同，但存在以下限制：

- 要尝试恢复的表不能已存在于数据库中。
- 如果尝试恢复备份集中不存在的模式或表，`gprestore` 不会执行。
- 如果使用 `--include-schema` 选项，`gprestore` 无法恢复依赖多个模式的对象。
- 如果使用 `--include-table-file` 选项，`gprestore` 不会创建角色，也不会设置表的所有者。工具会恢复表索引和规则。触发器也会恢复，但 Apache Cloudberry 不支持触发器。
- 使用 `--include-table-file` 指定的文件不能包含叶分区名称，而使用 `gpbackup` 指定该选项时可以包含叶分区名称。如果备份集中指定了叶分区，请指定分区表来恢复叶分区数据。

    恢复包含分区表部分叶分区数据的备份集时，会同时恢复分区表以及这些叶分区的数据。例如，使用 `gpbackup` 的 `--include-table-file` 选项创建备份，文本文件列出分区表的一些叶分区。恢复备份会创建分区表，并且只恢复文件中列出的叶分区数据。

### 按叶分区过滤 {#filter-by-leaf-partition}

默认情况下，`gpbackup` 为 Segment 上的每张表创建一个文件。可以指定 `--leaf-partition-data` 选项，为分区表的每个叶分区创建一个数据文件，而不是单个文件。还可以通过将要包含的叶分区名称列在文本文件中，将备份过滤到特定叶分区。例如，考虑使用以下语句创建的表：

```sql
CREATE TABLE sales (id int, date date, amt decimal(10,2))
DISTRIBUTED BY (id)
PARTITION BY RANGE (date)
( PARTITION Jan23 START (date '2023-01-01') INCLUSIVE ,
  PARTITION Feb23 START (date '2023-02-01') INCLUSIVE ,
  PARTITION Mar23 START (date '2023-03-01') INCLUSIVE ,
  PARTITION Apr23 START (date '2023-04-01') INCLUSIVE ,
  PARTITION May23 START (date '2023-05-01') INCLUSIVE ,
  PARTITION Jun23 START (date '2023-06-01') INCLUSIVE ,
  PARTITION Jul23 START (date '2023-07-01') INCLUSIVE ,
  PARTITION Aug23 START (date '2023-08-01') INCLUSIVE ,
  PARTITION Sep23 START (date '2023-09-01') INCLUSIVE ,
  PARTITION Oct23 START (date '2023-10-01') INCLUSIVE ,
  PARTITION Nov23 START (date '2023-11-01') INCLUSIVE ,
  PARTITION Dec23 START (date '2023-12-01') INCLUSIVE
  END (date '2024-01-01') EXCLUSIVE );

NOTICE:  CREATE TABLE will create partition "sales_1_prt_jan23" for table "sales"
NOTICE:  CREATE TABLE will create partition "sales_1_prt_feb23" for table "sales"
NOTICE:  CREATE TABLE will create partition "sales_1_prt_mar23" for table "sales"
NOTICE:  CREATE TABLE will create partition "sales_1_prt_apr23" for table "sales"
NOTICE:  CREATE TABLE will create partition "sales_1_prt_may23" for table "sales"
NOTICE:  CREATE TABLE will create partition "sales_1_prt_jun23" for table "sales"
NOTICE:  CREATE TABLE will create partition "sales_1_prt_jul23" for table "sales"
NOTICE:  CREATE TABLE will create partition "sales_1_prt_aug23" for table "sales"
NOTICE:  CREATE TABLE will create partition "sales_1_prt_sep23" for table "sales"
NOTICE:  CREATE TABLE will create partition "sales_1_prt_oct23" for table "sales"
NOTICE:  CREATE TABLE will create partition "sales_1_prt_nov23" for table "sales"
NOTICE:  CREATE TABLE will create partition "sales_1_prt_dec23" for table "sales"
CREATE TABLE
```

要只备份该年度最后一个季度的数据，首先创建一个列出这些叶分区名称的文本文件，而不是列出完整表名：

```
public.sales_1_prt_oct23
public.sales_1_prt_nov23
public.sales_1_prt_dec23
```

然后使用 `--include-table-file` 选项指定该文件，为每个叶分区生成一个数据文件：

```bash
$ gpbackup --dbname test_04 --include-table-file last-quarter.txt --leaf-partition-data
```

指定 `--leaf-partition-data` 时，`gpbackup` 备份分区表时会为每个叶分区生成一个数据文件。例如，以下命令为每个叶分区生成一个数据文件：

```bash
$ gpbackup --dbname test_04 --include-table public.sales --leaf-partition-data
```

备份叶分区时，会同时备份叶分区数据和整个分区表的元数据。

## 检查报告文件 {#check-report-files}

执行备份或恢复操作时，`gpbackup` 和 `gprestore` 会生成包含操作详细信息的报告文件。配置电子邮件通知后，发送的邮件会包含报告文件内容。有关电子邮件通知的信息，请参见[配置电子邮件通知](#configure-email-notifications)。

报告文件位于 Apache Cloudberry Coordinator 备份目录中。报告文件名包含操作时间戳。以下是 `gpbackup` 和 `gprestore` 报告文件名的格式。

```
gpbackup_<backup_timestamp>_report
gprestore_<backup_timestamp>_<restore_timesamp>_report
```

对于示例报告文件名，`20240109111719` 是备份时间戳，`20240109112545` 是恢复操作的时间戳。

```
gpbackup_20240109111719_report
gprestore_20240109111719_20240109112545_report
```

Apache Cloudberry Coordinator 主机上的此备份目录包含 `gpbackup` 和 `gprestore` 报告文件。

```bash
$ ls -l /data0/coordinator/gpseg-1/backups/20240109/20240109111719/
total 24

-r--r--r-- 1 gpadmin gpadmin  715 Jan  9 11:17 gpbackup_20240109111719_config.yaml
-r--r--r-- 1 gpadmin gpadmin  895 Jan  9 11:17 gpbackup_20240109111719_metadata.sql
-r--r--r-- 1 gpadmin gpadmin 1441 Jan  9 11:17 gpbackup_20240109111719_report
-r--r--r-- 1 gpadmin gpadmin 1226 Jan  9 11:17 gpbackup_20240109111719_toc.yaml
-r--r--r-- 1 gpadmin gpadmin  569 Jan  9 11:21 gprestore_20240109111719_20240109112128_report
-r--r--r-- 1 gpadmin gpadmin  514 Jan  9 11:25 gprestore_20240109111719_20240109112545_report
```

报告文件的内容相似。以下是 `gprestore` 报告文件内容的示例。

```
Apache Cloudberry Restore Report

timestamp key:           20240109111719
gpdb version:            oudberry Database 1.0.0 build 5551471267
gprestore version:       1.2.7-beta1+dev.7

database name:           test_04
command line:            gprestore --timestamp 20240109111719 --create-db

backup segment count:    2
restore segment count:   2
start time:              Tue Jan 09 2024 11:25:45
end time:                Tue Jan 09 2024 11:25:46
duration:                0:00:01

restore status:          Success
```

## 配置电子邮件通知 {#configure-email-notifications}

`gpbackup` 和 `gprestore` 可以在备份或恢复操作完成后发送电子邮件通知。

要让 `gpbackup` 或 `gprestore` 发送状态电子邮件通知，需要将名为 `gp_email_contacts.yaml` 的文件放在运行 `gpbackup` 或 `gprestore` 的用户主目录中，以及工具所在的 `$GPHOME/bin` 目录中。工具在任一位置找不到 `gp_email_contacts.yaml` 文件时会发出消息。如果两个位置都包含 `.yaml` 文件，工具使用用户 `$HOME` 中的文件。

电子邮件主题行包含工具名称、时间戳、作业状态（Success 或 Failure）以及调用 `gpbackup` 或 `gprestore` 的 Apache Cloudberry 主机名。以下是 `gpbackup` 邮件主题行的示例。

```shell
gpbackup 20180202133601 on gp-master completed: Success
```

or

```shell
gpbackup 20200925140738 on mdw completed: Failure
```

电子邮件包含操作摘要信息，包括选项、持续时间以及备份或恢复的对象数量。有关通知邮件内容的信息，请参见报告文件。

> [!TIP]
> UNIX mail 工具必须在 Apache Cloudberry 主机上运行，并且必须配置为允许 Apache Cloudberry 超级用户（`gpadmin`）发送邮件。同时确保通过 `gpadmin` 用户的 `$PATH` 可以定位邮件程序可执行文件。

### gpbackup 和 gprestore 电子邮件文件格式 {#gpbackup-and-gprestore-email-file-format}

`gpbackup` 和 `gprestore` 的电子邮件通知 YAML 文件 `gp_email_contacts.yaml` 使用缩进（空格）确定文档层级以及各节之间的关系。空白字符具有重要意义，不应仅为格式化而使用空白，也完全不能使用制表符。

如果状态参数指定不正确，工具不会发出警告。例如，如果将 success 参数拼写错误并设为 true，不会发出警告，操作成功后也不会向电子邮件地址发送邮件。为确保电子邮件通知配置正确，请在配置电子邮件通知后运行测试。

以下是 gpbackup 电子邮件通知使用的 `gp_email_contacts.yaml` YAML 文件格式：

```yaml
contacts:
  gpbackup:
  - address: <user>@<domain>
    status:
         success: [true | false]
         success_with_errors: [true | false]
         failure: [true | false]
  gprestore:
  - address: <user>@<domain>
    status:
         success: [true | false]
         success_with_errors: [true | false]
         failure: [true | false]
```

### 电子邮件 YAML 文件各节 {#email-yaml-file-sections}

**`contacts`**

必需。包含 gpbackup 和 gprestore 节的部分。YAML 文件可以包含 gpbackup 节、gprestore 节，或各包含一个。

**`gpbackup`**

可选。开始 gpbackup 电子邮件部分。

**`address`**

必需。至少必须指定一个电子邮件地址，也可以指定多个电子邮件地址参数。每个地址都需要一个 status 节。`user@domain` 是单个有效的电子邮件地址。

**`status`**

必需。指定工具何时向指定电子邮件地址发送邮件。默认不发送电子邮件通知。可以根据备份或恢复操作的完成状态指定是否发送通知。至少必须指定以下参数中的一个，每个参数最多出现一次。

**`success`**

可选。指定操作无错误完成时是否发送邮件。如果值为 `true`，操作无错误完成时会发送邮件。如果值为 `false`（默认值），则不发送邮件。

**`success_with_errors`**

可选。指定操作带错误完成时是否发送邮件。如果值为 `true`，操作带错误完成时会发送邮件。如果值为 `false`（默认值），则不发送邮件。

**`failure`**

可选。指定操作失败时是否发送邮件。如果值为 `true`，操作失败时会发送邮件。如果值为 `false`（默认值），则不发送邮件。

**`gprestore`**

可选。开始 gprestore 电子邮件部分。此部分包含在 gprestore 操作后发送电子邮件通知所使用的地址和状态参数。语法与 gpbackup 部分相同。

### 电子邮件示例 {#email-examples}

以下 YAML 文件示例根据操作成功或失败向不同的电子邮件地址发送邮件。对于备份操作，会根据备份操作成功或失败向不同地址发送邮件。对于恢复操作，只有操作成功或带错误完成时，才会向 `gpadmin@example.com` 发送邮件。

```yaml
contacts:
  gpbackup:
  - address: gpadmin@example.com
    status:
      success: true
      success_with_errors: true
      failure: true  
  gprestore:
  - address: gpadmin@example.com
    status:
      success: true
      success_with_errors: true
      failure: true
```
