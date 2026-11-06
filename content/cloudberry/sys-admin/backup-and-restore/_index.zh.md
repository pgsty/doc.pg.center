---
title: "备份与恢复概述"
linkTitle: "备份与恢复"
description: "Apache Cloudberry 提供并行和非并行的数据库备份与恢复方法。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/backup-and-restore/index.md"
---

并行操作会同时将数据写入每个 Segment 主机的本地磁盘，因此能够高效处理大型系统。非并行操作则通过网络将所有数据传输到 Coordinator，再由 Coordinator 将数据写入自己的存储。这种方法不仅会把 I/O 集中到一台主机上，还要求 Coordinator 有足够的本地磁盘空间来保存整个数据库。

## 使用 `gpbackup` 和 `gprestore` 进行并行备份 {#parallel-backup-with-gpbackup-and-gprestore}

Apache Cloudberry 提供 `gpbackup` 和 `gprestore` 这两个用于并行备份和恢复的工具。`gpbackup` 在 `pg_class` 目录表上使用表级 `ACCESS SHARE` 锁，而不是 `EXCLUSIVE` 锁。因此，只要 DDL 语句的目标不属于当前备份集，就可以在备份期间执行 `CREATE`、`ALTER`、`DROP` 和 `TRUNCATE` 等 DDL 语句。

`gpbackup` 创建的备份文件旨在支持未来恢复单个数据库对象及其依赖对象，例如函数和所需的用户定义数据类型。

有关使用 `gpbackup` 和 `gprestore` 进行备份与恢复的详细信息，请参见[执行全量备份与恢复](/cloudberry/sys-admin/backup-and-restore/perform-full-backup-and-restore/)和[执行增量备份与恢复](/cloudberry/sys-admin/backup-and-restore/perform-incremental-backup-and-restore/)。

## 使用 `pg_dump` 进行非并行备份 {#non-parallel-backup-with-pg_dump}

还可以使用 PostgreSQL 的非并行备份工具 `pg_dump` 和 `pg_dumpall`，在 Coordinator 主机上创建一个包含所有活动 Segment 中全部数据的单个转储文件。

PostgreSQL 非并行工具只能用于特殊情况。由于所有数据都必须经过 Coordinator，它们的速度远低于 `gpbackup` 和 `gprestore`。此外，Coordinator 主机通常没有足够的磁盘空间来保存整个分布式 Apache Cloudberry 的备份。

`pg_restore` 工具要求使用 `pg_dump` 或 `pg_dumpall` 创建压缩的转储文件。开始恢复前，应修改转储文件中的 `CREATE TABLE` 语句，使其包含 Apache Cloudberry 的 `DISTRIBUTED` 子句。如果不包含 `DISTRIBUTED` 子句，Apache Cloudberry 会分配默认值，而默认值可能不是最优的。

要使用并行备份文件执行非并行恢复，可以将各 Segment 主机上的备份文件复制到 Coordinator 主机，然后通过 Coordinator 加载这些文件。

备份 Apache Cloudberry 数据的另一种非并行方法是使用 `COPY TO` SQL 命令，将表的全部或部分数据复制到 Coordinator 主机上的分隔文本文件中。
