---
title: "pg_stat_progress_basebackup"
description: "`pg_stat_progress_basebackup` 视图显示由 `pg_basebackup` 等工具发起的基础备份的进度。"
weight: 270
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/pg-stat-progress-basebackup.md"
---

每一行表示一个当前正在执行 `BASE_BACKUP` 命令的 WAL 发送进程，详细列出当前阶段、估计的数据总量、已流式传输的数据量以及已处理的表空间等信息。此视图有助于监控和管理正在进行的基础备份操作。

|列|类型|说明|
|------|----|-----------|
|`gp_segment_id`|integer|Segment（或 Coordinator）实例的唯一标识符。（`gp_stat_progress_basebackup_summary` 视图中没有此列。）|
| `pid` | integer |WAL 发送进程的进程标识符；在 `gp_stat_progress_basebackup_summary` 视图中，则为 Coordinator 进程标识符。|
| `phase` | text |当前处理阶段。|
| `backup_total` | bigint |将要流式传输的数据总量。此值在流式传输数据库文件阶段开始时估算并报告。请注意，这只是近似值，因为数据库在该阶段可能发生变化，且稍后可能会将 WAL 日志包含在备份中。一旦已传输的数据量超过估计总量，此值就始终与 backup_streamed 相同。如果在 `pg_basebackup` 中禁用了估算，则为 NULL。|
| `backup_streamed` | bigint |已流式传输的数据量。此计数器仅在流式传输数据库文件或传输 WAL 文件阶段递增。|
| `tablespaces_total` | bigint |将要流式传输的表空间总数。|
| `tablespaces_streamed` | bigint |已流式传输的表空间数量。此计数器仅在流式传输数据库文件阶段递增。|
