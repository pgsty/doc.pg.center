---
title: "跟踪复制延迟"
description: "查看订阅方相对于提供方的 WAL 复制延迟。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/monitoring/lag_tracking.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



Spock 的延迟跟踪功能显示订阅方在预写日志（WAL）复制方面落后提供方多少，可据此了解复制延迟并监控传输状态。

按节点的主要延迟指标由 SQL 视图 `spock.lag_tracker` 提供。例如：

```sql
-[ RECORD 1 ]---------+------------------------------
origin_name           | node1
receiver_name         | node2
commit_timestamp      | 2025-06-30 09:27:57.317779+00
commit_lsn            | 0/15A2780
remote_insert_lsn     | 0/15A2780
received_lsn          | 0/15A2780
replication_lag_bytes | 0
replication_lag       | 00:00:04.014177
```

下表说明 `spock.lag_tracker` 中的列。

| 列名 | 说明 |
|-------------|-------------|
| origin_name | 提供方节点的名称。 |
| receiver_name | 订阅方节点的名称。 |
| commit_timestamp | 从提供方收到的最近一笔事务的提交时间。 |
| commit_lsn | 事务在提供方提交的日志序列号（LSN）。 |
| remote_insert_lsn | 发送提交时，提供方的 WAL 插入位置。 |
| received_lsn | 从提供方接收并已确认的最近一个日志序列号（LSN）。 |
| replication_lag_bytes | 订阅方落后的数据量。 |
| replication_lag | 从事务在提供方提交到在本地处理之间的时间差。 |
{.wide .expand}


---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/monitoring/lag_tracking.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
