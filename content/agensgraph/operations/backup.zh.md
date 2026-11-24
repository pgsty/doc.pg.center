---
title: "备份与恢复"
linkTitle: "备份与恢复"
description: "图存储在 PostgreSQL 的模式和表中。使用 PostgreSQL 的备份工具即可将图和关系数据恢复到同一时间点。"
type: docs
weight: 40
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/operations/backup.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: translated
---


AgensGraph 将图存储在 PostgreSQL 的模式和表中。因此，PostgreSQL 的各种备份方法都会同时备份图和关系数据，二者对应同一时间点。无需单独备份图，也无需在恢复时协调两套数据。

具体操作以 [PostgreSQL 的备份章节](https://www.postgresql.org/docs/18/backup.html)为准。本页说明如何选择备份方法，以及备份图时要注意的细节。

## 如何选择备份方法 {#which-method}

| 方法 | 备份内容 | 适用场景 |
| --- | --- | --- |
| `pg_dump` / `pg_dumpall` | 逻辑副本，可以是 SQL 语句，也可以是归档文件，可跨大版本和平台使用。 | 迁移数据库、复制单个图，或保留与版本无关的副本。 |
| `pg_basebackup` | 整个集群的物理副本。 | 为时间点恢复准备基础备份，或初始化副本。 |
| 连续归档 | 基础备份及此后所有 WAL 段，可恢复到这段时间内的任一时刻。 | 无法承受丢失一小时写入数据的生产环境。 |
| 文件系统快照 | 存储层创建的物理副本。 | 仅适用于能对集群使用的所有文件系统同时做原子快照的情形。 |

服务器运行时，用 `cp` 直接复制数据目录不能用于备份。单独复制表文件也不能构成备份。事务提交日志属于整个集群，仅凭单个表文件无法判定哪些行已经提交。

## 逻辑备份 {#logical-backup}

```shell
pg_dump -d mydb -Fc -f mydb.dump          # one database, archive format
pg_dumpall -f cluster.sql                  # every database plus roles
pg_dump -d mydb --schema=moviekb -f g.sql  # one graph
```

用以下命令恢复备份。

```shell
pg_restore --exit-on-error -d mydb mydb.dump
psql -d postgres -f cluster.sql
```

> [!WARNING]
> 默认情况下，两种恢复工具遇错都会继续执行，`psql` 此时仍以状态码 0 退出。因此，恢复可能报告成功，但实际缺少对象。例如，如果服务器拒绝创建某个外键约束，表中就缺少该约束，之后引用不存在记录的行也能插入。加上 `--exit-on-error` 可让 `pg_restore` 遇到第一个错误就停止。
>
> `psql` 有 `ON_ERROR_STOP` 选项，但不适用于这里的 `pg_dumpall` 脚本。脚本会尝试重新创建已经存在的初始超级用户，导致恢复在第 14 行就停止，尚未加载任何数据。请检查这次恢复的输出，或者用 `pg_dump -Fc` 逐库转储，再用 `pg_restore --exit-on-error` 恢复。

每个图本身就是一个*模式*，因此指定模式名即可转储单个图。除数据外，转储还包含 `CREATE GRAPH`、`CREATE VLABEL` 和 `CREATE ELABEL` 语句，恢复时会据此重建图结构。

转储图时还要注意以下四点，详见[服务端工具](/zh/agensgraph/operations/tools/#dumping-a-graph)。

* 两种转储工具都只检查 PostgreSQL 版本，不检查 AgensGraph 版本。
* 对含普通列的标签进行转储后，恢复时需要启用 `enable_graph_ddl`。转储脚本会在相关语句前开启该设置，在语句后将其还原。
* 只要有一个图使用了提升列，就无法将 2.18 的转储恢复到 2.17。
* 基于 Cypher 查询的视图会以该查询转换后的 SQL 形式导出。

每次恢复后，都应重建图元数据并重新收集统计信息。

```sql
SET graph_path = <your graph>;
SELECT regather_graphmeta();
```

```shell
vacuumdb -d mydb --analyze-in-stages
```

## 物理备份与时间点恢复 {#physical-backup-and-point-in-time-recovery}

操作流程与 PostgreSQL 相同，主要步骤如下。

在服务器上配置 WAL 归档，然后重启服务器。

```
wal_level = replica
archive_mode = on
archive_command = 'test ! -f /mnt/archive/%f && cp %p /mnt/archive/%f'
```

`wal_level = minimal` 记录的信息不足以从归档恢复，因此无法使用这种备份方法。

创建基础备份。

```shell
pg_basebackup -D /mnt/backup/base -Ft -z -P -X stream
```

恢复时，将基础备份还原到空的数据目录，再指定服务器从何处取得已归档的 WAL。

```
restore_command = 'cp /mnt/archive/%f %p'
recovery_target_time = '2026-09-02 14:30:00'
```

将这些设置写入 `postgresql.conf`，并在数据目录中创建名为 `recovery.signal` 的空文件，使服务器进入恢复模式。恢复结束后，服务器会删除该文件并开始接受连接。

> [!NOTE]
> 查阅较早的 AgensGraph 或 PostgreSQL 文档时，注意三处变化。现在应将恢复设置写入 `postgresql.conf`，并创建 `recovery.signal`。PostgreSQL 12 已移除 `recovery.conf`，发现该文件时服务器会拒绝启动。另两处变化始于 PostgreSQL 10：WAL 目录由 `pg_xlog` 改名为 `pg_wal`，事务提交日志目录由 `pg_clog` 改名为 `pg_xact`。

使用基础备份前，先验证其完整性。

```shell
pg_verifybackup /mnt/backup/base
```

## 备份管理工具 {#higher-level-tools}

`pgBackRest` 和 `Barman` 都能管理备份保留策略、并行压缩、增量备份和恢复流程。两者都可以直接用于 AgensGraph 集群，无需针对图单独配置。管理多台服务器时，任选其中一种都比手写 `archive_command` 更合适。

## 如何验证恢复结果 {#what-to-check}

只有实际恢复过，才能知道备份是否可用。对于图，恢复测试除了确认服务器能启动，还要运行以下检查。

```cypher
SET graph_path = <your graph>;
MATCH (n) RETURN label(n) AS label, count(*) ORDER BY label;
MATCH ()-[e]->() RETURN label(e) AS label, count(*) ORDER BY label;
```

```sql
SELECT graphname, graphmeta_valid FROM pg_catalog.ag_graph;
SELECT * FROM pg_catalog.ag_property_indexes;
```

核对各标签的顶点数和边数是否与源库一致，再确认索引和约束均已恢复，才能判断图是否完整。
