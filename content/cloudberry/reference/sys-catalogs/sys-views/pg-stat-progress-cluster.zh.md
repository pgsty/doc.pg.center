---
title: "pg_stat_progress_cluster"
description: "`pg_stat_progress_cluster` 视图显示 `CLUSTER` 和 `VACUUM FULL` 操作的进度。"
weight: 280
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/pg-stat-progress-cluster.md"
---

每一行表示一个当前正在执行其中某个命令的后端进程，提供当前阶段、已扫描和写入的堆块数量、已重建的索引等详情。此视图有助于监控和管理长时间运行的表重组任务。

|列|类型|说明|
|------|----|-----------|
|`gp_segment_id`|integer|Segment（或 Coordinator）实例的唯一标识符。（`gp_stat_progress_cluster_summary` 视图中没有此列。）|
| `pid` | integer |后端的进程标识符；在 `gp_stat_progress_cluster_summary` 视图中，则为 Coordinator 进程标识符。|
| `datid` | oid |此后端所连接数据库的对象标识符。|
| `datname` | name |此后端所连接数据库的名称。|
| `relid` | `oid` |正在聚簇的表的对象标识符。|
| `command` | text |正在运行的命令名称，为 `CLUSTER` 或 `VACUUM FULL`。|
| `phase` | text |当前处理阶段。|
| `cluster_index_relid` | oid |如果正在使用索引扫描表，则为所用索引的对象标识符；否则为零。此字段不适用于 AO/CO 表。|
| `heap_tuples_scanned` | bigint |对于堆表，`heap_tuples_scanned` 记录已扫描的元组数量，包括存活和死亡元组。对于 AO 表，`heap_tuples_scanned` 记录已扫描的存活元组数量，不包括死亡元组。此计数器仅在 `seq scanning append-optimized`、`seq scanning heap`、`index scanning heap` 或 `writing new heap` 阶段递增。对于 AO/CO 表，Apache Cloudberry 会将字节大小换算成等效大小的堆块数。|
| `heap_tuples_written` | bigint |已写入的元组数量。此计数器仅在 `seq scanning heap`、`index scanning heap`、`writing new append-optimized` 或 `writing new heap` 阶段递增。|
| `heap_blks_total` | bigint |表中的堆块总数。此值在 `seq scanning heap` 开始时报告。对于 AO/CO 表，Apache Cloudberry 会将字节大小换算成等效大小的堆块数。|
| `heap_blks_scanned` | bigint |已扫描的堆块数量。此计数器仅在 `seq scanning heap` 阶段递增。对于 AO/CO 表，Apache Cloudberry 会将字节大小换算成等效大小的堆块数。|
| `index_rebuild_count` | bigint |已重建的索引数量。此计数器仅在 `rebuilding index` 阶段递增，不适用于 AO/CO 表。|
