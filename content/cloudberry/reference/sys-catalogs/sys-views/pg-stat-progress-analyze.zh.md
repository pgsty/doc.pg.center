---
title: "pg_stat_progress_analyze"
description: "`pg_stat_progress_analyze` 视图显示当前正在运行的 `ANALYZE` 命令的进度。"
weight: 260
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/pg-stat-progress-analyze.md"
---

每一行表示一个正在执行 `ANALYZE` 的后端进程，提供当前阶段、已采样块数、已计算的统计信息等详情。此视图有助于监控长时间运行的 `ANALYZE` 操作。

|列|类型|说明|
|------|----|-----------|
|`gp_segment_id`|integer|Segment（或 Coordinator）实例的唯一标识符。（`gp_stat_progress_analyze_summary` 视图中没有此列。）|
| `pid` | integer |后端的进程标识符；在 `gp_stat_progress_analyze_summary` 视图中，则为 Coordinator 进程标识符。|
| `datid` | oid |此后端所连接数据库的对象标识符。|
| `datname` | name |此后端所连接数据库的名称。|
| `relid` | oid |正在分析的表的对象标识符。|
| `phase` | text |当前处理阶段。|
| `sample_blks_total` | bigint |将要采样的堆块总数。|
| `sample_blks_scanned` | bigint |已扫描的堆块数量。|
| `ext_stats_total` | bigint |扩展统计信息的数量。|
| `ext_stats_computed` | bigint |已计算的扩展统计信息数量。此计数器仅在计算扩展统计信息阶段递增。|
| `child_tables_total` | bigint |子表数量。|
| `child_tables_done` | bigint |已扫描的子表数量。此计数器仅在获取继承采样行阶段递增。|
| `current_child_table_relid` | oid |当前正在扫描的子表的对象标识符。此字段仅在获取继承采样行阶段有效。（`gp_stat_progress_analyze_summary` 视图中没有此列。）|
