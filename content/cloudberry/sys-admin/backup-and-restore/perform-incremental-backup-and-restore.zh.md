---
title: "执行增量备份与恢复"
description: "使用 gpbackup 创建一致的增量备份集，并使用 gprestore 恢复这些备份。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/backup-and-restore/perform-incremental-backup-and-restore.md"
---

阅读本文前，应先阅读[执行全量备份与恢复](/cloudberry/sys-admin/backup-and-restore/perform-full-backup-and-restore/)。

要增量备份和恢复表，请使用 `gpbackup` 和 `gprestore` 工具。增量备份包含所有指定的堆表，以及发生变化的追加优化表（包括列存表）。即使只更改一行，也会触发整个追加优化表的备份。对于分区追加优化表，只备份已修改的叶分区。

当发生变化的追加优化表或表分区中的数据总量，相对于上次备份以来未发生变化的数据量较小时，增量备份更高效。

只有在上次全量备份或增量备份之后对追加优化表执行以下操作之一时，增量备份才会备份该表：

- `ALTER TABLE`
- `DELETE`
- `INSERT`
- `TRUNCATE`
- `UPDATE`
- `DROP`，然后重新创建表

要从增量备份恢复数据，需要完整的增量备份集。

## 关于增量备份集 {#about-incremental-backup-sets}

增量备份集包含以下备份：

- 一个全量备份。这是增量备份所基于的全量备份。
- 捕获全量备份之后数据库变更的一组增量备份。

例如，可以创建一个全量备份，然后创建 3 个每日增量备份。全量备份和这 3 个增量备份共同构成备份集。有关如何使用增量备份集的信息，请参见[使用增量备份集的示例](#example-using-incremental-backup-sets)。

创建增量备份集或向其添加备份时，`gpbackup` 会确保备份集中的备份使用一致的备份选项创建，从而确保备份集可以用于恢复操作。有关备份集一致性的信息，请参见[使用增量备份](#use-incremental-backups)。

创建增量备份时，将以下选项与其他 `gpbackup` 选项一起指定，以创建备份：

- `--leaf-partition-data`：备份集中的所有备份都必须指定。

    - 创建将作为增量备份集基础备份的全量备份时必须指定。
    - 创建增量备份时必须指定。

- `--incremental`：创建增量备份时必须指定。

    不能将 `--data-only` 或 `--metadata-only` 与 `--incremental` 组合使用。

- `--from-timestamp`：可选。该选项可与 `--incremental` 一起使用。指定的时间戳对应一个现有备份，可以是全量备份或增量备份。正在创建的备份必须与 `--from-timestamp` 选项指定的备份兼容。

## 使用增量备份 {#use-incremental-backups}

向备份集添加增量备份时，`gpbackup` 会检查以下 `gpbackup` 选项，确保全量备份与增量备份一致：

- `--dbname`：数据库必须相同。
- `--backup-dir`：目录必须相同。备份集、全量备份和增量备份必须位于同一位置。
- `--single-data-file`：备份集中的所有备份必须都指定或都不指定此选项。
- `--include-table-file`、`--include-schema` 或其他过滤表和模式的选项必须相同。检查模式过滤器时，只检查模式名称，不检查模式中包含的对象。
- `--no-compression`：如果指定此选项，则备份集中的所有备份都必须指定。

    如果全量备份使用压缩，增量备份也必须使用压缩。备份集中的备份可以使用不同的压缩级别。默认情况下，备份的压缩级别为 1。

如果尝试向备份集添加增量备份时，`gpbackup` 选项不一致，备份操作会失败。

### 使用增量备份集的示例 {#example-using-incremental-backup-sets}

每个备份都有创建时获取的时间戳。例如，如果在 2023 年 5 月 14 日创建备份，备份文件名会包含 `20230514hhmmss`。`hhmmss` 表示时间，即小时、分钟和秒。

本例假定你已经创建了数据库 `mytest` 的两个全量备份和增量备份。创建全量备份时使用以下命令：

```shell
gpbackup --dbname mytest --backup-dir /mybackup --leaf-partition-data
```

使用以下命令创建增量备份：

```shell
gpbackup --dbname mytest --backup-dir /mybackup --leaf-partition-data --incremental
```

指定 `--backup-dir` 选项后，备份会在每台 Apache Cloudberry 主机的 `/mybackup` 目录中创建。

本例中，全量备份的时间戳键为 `20230514054532` 和 `20231114064330`，其他备份均为增量备份。本例包含两个备份集：第一个备份集有两个增量备份，第二个有一个增量备份。以下按从早到晚的顺序列出备份。

- `20230514054532`（全量备份）
- `20230714095512`
- `20230914081205`
- `20231114064330`（全量备份）
- `20230114051246`

要基于最新增量备份创建新的增量备份，必须包含与该增量备份相同的 `--backup-dir` 选项，以及 `--leaf-partition-data` 和 `--incremental` 选项。

```shell
gpbackup --dbname mytest --backup-dir /mybackup --leaf-partition-data --incremental
```

可以指定 `--from-timestamp` 选项，基于现有增量备份或全量备份创建增量备份。根据本例，以下命令向包含 `20230914081205`（作为增量备份）的备份集添加第四个增量备份，并使用 `20230514054532` 作为全量备份。

```shell
gpbackup --dbname mytest --backup-dir /mybackup --leaf-partition-data --incremental --from-timestamp 20230914081205
```

此命令创建一个基于全量备份 `20231114064330` 的增量备份集，该备份集与包含增量备份 `20230114051246` 的备份集相互独立。

```shell
gpbackup --dbname mytest --backup-dir /mybackup --leaf-partition-data --incremental --from-timestamp 20231114064330
```

要使用增量备份 `20230914081205` 恢复数据库，需要增量备份 `20120914081205` 和 `20230714095512`，以及全量备份 `20230514054532`。对应的 `gprestore` 命令为：

```shell
gprestore --backup-dir /backupdir --timestamp 20230914081205
```

### 使用 `gpbackup` 创建增量备份 {#create-an-incremental-backup-with-gpbackup}

`gpbackup` 输出会显示增量备份所基于的备份时间戳。本例中，增量备份基于时间戳为 `20230802171642` 的备份。`20230802171642` 可以是增量备份或全量备份。

```shell
$ gpbackup --dbname test --backup-dir /backups --leaf-partition-data --incremental

20230803:15:40:51 gpbackup:gpadmin:mdw:002907-[INFO]:-Starting backup of database test
20230803:15:40:52 gpbackup:gpadmin:mdw:002907-[INFO]:-Backup Timestamp = 20230803154051
20230803:15:40:52 gpbackup:gpadmin:mdw:002907-[INFO]:-Backup Database = test
20230803:15:40:52 gpbackup:gpadmin:mdw:002907-[INFO]:-Gathering list of tables for backup
20230803:15:40:52 gpbackup:gpadmin:mdw:002907-[INFO]:-Acquiring ACCESS SHARE locks on tables
Locks acquired:  5 / 5 [================================================================] 100.00% 0s
20230803:15:40:52 gpbackup:gpadmin:mdw:002907-[INFO]:-Gathering additional table metadata
20230803:15:40:52 gpbackup:gpadmin:mdw:002907-[INFO]:-Metadata will be written to /backups/gpseg-1/backups/20230803/20230803154051/gpbackup_20230803154051_metadata.sql
20230803:15:40:52 gpbackup:gpadmin:mdw:002907-[INFO]:-Writing global database metadata
20230803:15:40:52 gpbackup:gpadmin:mdw:002907-[INFO]:-Global database metadata backup complete
20230803:15:40:52 gpbackup:gpadmin:mdw:002907-[INFO]:-Writing pre-data metadata
20230803:15:40:52 gpbackup:gpadmin:mdw:002907-[INFO]:-Pre-data metadata backup complete
20230803:15:40:52 gpbackup:gpadmin:mdw:002907-[INFO]:-Writing post-data metadata
20230803:15:40:52 gpbackup:gpadmin:mdw:002907-[INFO]:-Post-data metadata backup complete
20230803:15:40:52 gpbackup:gpadmin:mdw:002907-[INFO]:-Basing incremental backup off of backup with timestamp = 20230802171642
20230803:15:40:52 gpbackup:gpadmin:mdw:002907-[INFO]:-Writing data to file
Tables backed up:  4 / 4 [==============================================================] 100.00% 0s
20230803:15:40:52 gpbackup:gpadmin:mdw:002907-[INFO]:-Data backup complete
20230803:15:40:53 gpbackup:gpadmin:mdw:002907-[INFO]:-Found neither /usr/local/greenplum-db/./bin/gp_email_contacts.yaml nor /home/gpadmin/gp_email_contacts.yaml
20230803:15:40:53 gpbackup:gpadmin:mdw:002907-[INFO]:-Email containing gpbackup report /backups/gpseg-1/backups/20230803/20230803154051/gpbackup_20230803154051_report will not be sent
20230803:15:40:53 gpbackup:gpadmin:mdw:002907-[INFO]:-Backup completed successfully
```

### 使用 `gprestore` 从增量备份恢复 {#restore-from-an-incremental-backup-with-gprestore}

从增量备份恢复时，可以指定 `--verbose` 选项，在命令行显示恢复操作使用的备份。例如，以下 `gprestore` 命令使用时间戳为 `20230807092740` 的增量备份恢复备份。输出包含用于恢复数据库数据的备份。

```shell
$ gprestore --create-db --timestamp 20230807162904 --verbose
...
20230807:16:31:56 gprestore:gpadmin:mdw:008603-[INFO]:-Pre-data metadata restore complete
20230807:16:31:56 gprestore:gpadmin:mdw:008603-[DEBUG]:-Verifying backup file count
20230807:16:31:56 gprestore:gpadmin:mdw:008603-[DEBUG]:-Restoring data from backup with timestamp: 20230807162654
20230807:16:31:56 gprestore:gpadmin:mdw:008603-[DEBUG]:-Reading data for table public.tbl_ao from file (table 1 of 1)
20230807:16:31:56 gprestore:gpadmin:mdw:008603-[DEBUG]:-Checking whether segment agents had errors during restore
20230807:16:31:56 gprestore:gpadmin:mdw:008603-[DEBUG]:-Restoring data from backup with timestamp: 20230807162819
20230807:16:31:56 gprestore:gpadmin:mdw:008603-[DEBUG]:-Reading data for table public.test_ao from file (table 1 of 1)
20230807:16:31:56 gprestore:gpadmin:mdw:008603-[DEBUG]:-Checking whether segment agents had errors during restore
20230807:16:31:56 gprestore:gpadmin:mdw:008603-[DEBUG]:-Restoring data from backup with timestamp: 20230807162904
20230807:16:31:56 gprestore:gpadmin:mdw:008603-[DEBUG]:-Reading data for table public.homes2 from file (table 1 of 4)
20230807:16:31:56 gprestore:gpadmin:mdw:008603-[DEBUG]:-Reading data for table public.test2 from file (table 2 of 4)
20230807:16:31:56 gprestore:gpadmin:mdw:008603-[DEBUG]:-Reading data for table public.homes2a from file (table 3 of 4)
20230807:16:31:56 gprestore:gpadmin:mdw:008603-[DEBUG]:-Reading data for table public.test2a from file (table 4 of 4)
20230807:16:31:56 gprestore:gpadmin:mdw:008603-[DEBUG]:-Checking whether segment agents had errors during restore
20230807:16:31:57 gprestore:gpadmin:mdw:008603-[INFO]:-Data restore complete
20230807:16:31:57 gprestore:gpadmin:mdw:008603-[INFO]:-Restoring post-data metadata
20230807:16:31:57 gprestore:gpadmin:mdw:008603-[INFO]:-Post-data metadata restore complete
...
```

输出显示恢复操作使用了三个备份。

从增量备份恢复时，`gprestore` 也会在 `gprestore` 日志文件中列出恢复操作使用的备份。

恢复操作期间，如果全量备份或其他所需的增量备份不可用，`gprestore` 会显示错误。

## 增量备份注意事项 {#incremental-backup-notes}

要创建增量备份，或从增量备份集恢复数据，需要完整的备份集。归档增量备份时，必须归档完整的备份集。必须归档在 Coordinator 和所有 Segment 上创建的全部文件。

创建增量备份时，如果不指定 `--from-timestamp` 选项，`gpbackup` 会使用选项集一致的最新备份。

创建增量备份时，如果指定 `--from-timestamp` 选项，`gpbackup` 会确保正在创建的备份选项与指定备份的选项一致。

备份集中的所有备份不要求都使用 `gpbackup` 的 `--with-stats` 选项。但是，要使用 `gprestore` 的 `--with-stats` 选项恢复统计信息，指定的备份在创建时必须使用 --with-stats。

可以从备份集中的任意备份执行恢复操作。但是，用于恢复数据库数据的备份之后的增量备份所捕获的变更不会被恢复。

从增量备份集恢复时，`gprestore` 会检查备份，并从备份集中追加优化表的最新版本恢复每张追加优化表，从最新备份恢复堆表。

增量备份集（一个全量备份及其关联的增量备份）必须位于单个设备上。例如，备份集中的所有备份必须全部位于文件系统上，或全部位于 Data Domain 系统上。

如果指定 `gprestore` 的 `--incremental` 选项从特定增量备份恢复数据，还必须指定 `--data-only` 选项。恢复操作前，`gprestore` 会确保待恢复的表存在。如果表不存在，`gprestore` 会返回错误并退出。

> [!WARNING]
> Apache Cloudberry Segment 配置的变化会使增量备份失效。更改 Segment 配置（添加或删除 Segment 实例）后，必须先创建全量备份，才能创建增量备份。
