---
title: "pg_stat_progress_create_index"
description: "通过 pg_stat_progress_create_index 系统视图监控 CREATE INDEX 和 REINDEX 的进度。"
weight: 300
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/pg-stat-progress-create-index.md"
---

## pg_stat_progress_create_index {#pg_stat_progress_create_index}

`pg_stat_progress_create_index` 是一个系统视图，显示当前数据库中正在进行的 `CREATE INDEX` 或 `REINDEX` 操作的实时进度。

此视图显示每个正在构建索引的后端进程的详细状态信息，包括当前执行阶段、已处理的元组数、已扫描的块数等。操作完成后，相应条目会自动从视图中移除。

在 Apache Cloudberry 中，此视图也支持追加优化表（AO 表），可用于观察此类表上索引创建的各阶段进度。

典型使用场景包括：

- 实时监控索引创建或重建操作。
- 分析长时间运行的 `CREATE INDEX` 或 `REINDEX` 命令的性能瓶颈。
- 检查当前是否有索引操作正在消耗系统资源。
- 与 `pg_stat_activity` 关联，以追踪后端进程详情。

示例查询：

```sql
-- Views all ongoing index creation tasks
SELECT * FROM pg_stat_progress_create_index;

-- Views index progress for a specific table
SELECT * FROM pg_stat_progress_create_index
WHERE relid = 'ao_test'::regclass;
```

### 字段说明 {#field-descriptions}

| 字段                 | 说明 |
|-----------------------|-------------|
| `gp_segment_id`       |此条目所在 Segment 的 ID。仅适用于分布式环境。|
| `pid`                 |后端的进程 ID。可以与 `pg_stat_activity` 连接以获取会话详情。|
| `datid`               |数据库的 OID，对应 `pg_database.oid`。|
| `datname`             |数据库的名称。|
| `relid`               |正在为其创建索引的表的 OID，对应 `pg_class.oid`。|
| `index_relid`         |正在构建的索引的 OID。|
| `command`             |正在执行的命令：`CREATE INDEX` 或 `REINDEX`。|
| `phase`               |当前执行阶段，例如：<br /> `initializing`：初始化阶段 <br /> `scanning heap`：扫描表数据 <br /> `sorting`：排序阶段 <br /> `building index: loading tuples in tree`：构建索引结构 <br /> `waiting for locks`：等待表锁或元数据锁|
| `lockers_total`       |持有冲突锁的会话总数（如果有）。|
| `lockers_done`        |已释放锁的会话数量。|
| `current_locker_pid`  |当前持有该锁的会话的进程 ID（如果正在等待）。|
| `blocks_total`        |要扫描的数据块总数（如果未知或尚未开始，可能为 0）。|
| `blocks_done`         |已扫描的数据块数量。|
| `tuples_total`        |要处理的元组总数的估计值（如果可用）。|
| `tuples_done`         |已处理的元组数量。|
| `partitions_total`    |分区总数（如果适用）。|
| `partitions_done`     |已处理的分区数量（如果适用）。|

> [!NOTE]
> - 此视图仅显示当前正在运行的索引操作。操作完成后，条目就会消失。
> - 对于小表，索引创建可能瞬间完成，视图可能不返回任何行。
> - 为了更好地观察进度，可以尝试在大表上创建索引，或使用复杂的列（例如大段文本）来减慢执行速度。
> - 在追加优化表（AO 表）上构建索引时，也会报告进度。
> - 可以使用 ``pid`` 字段将此视图与 ``pg_stat_activity`` 连接。
>
>     ```sql
>     SELECT a.usename, a.query, p.phase, p.blocks_done, p.blocks_total
>     FROM pg_stat_activity a
>     JOIN pg_stat_progress_create_index p ON a.pid = p.pid;
>     ```
