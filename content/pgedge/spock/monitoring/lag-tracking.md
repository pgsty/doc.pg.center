---
title: Lag Tracking
description: The Spock extension's lag tracking feature shows how far behind a subscriber is when compared to a
  provider node in terms of write-ahead log (WAL) replication.
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/monitoring/lag_tracking.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
---



The Spock extension's lag tracking feature shows how far behind a subscriber
is when compared to a provider node in terms of write-ahead log (WAL)
replication. You can use this feature to understand replication delays and
monitor streaming health.

Tracking is implemented via a SQL view named `spock.lag_tracker`, which
exposes key metrics for replication lag on a per-node basis. For example:

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

The following table describes the columns displayed by `spock.lag_tracker`:

| Column Name | Description |
|-------------|-------------|
| origin_name | Name of the provider node. |
| receiver_name | Name of the subscriber node. |
| commit_timestamp | Commit time of the last transaction received from the provider. |
| commit_lsn | Log sequence number (LSN) of the commit on the provider. |
| remote_insert_lsn | WAL insert position on the provider when the commit was sent. |
| received_lsn | Last acknowledged log sequence number (LSN) received from the provider. |
| replication_lag_bytes | The amount of data the subscriber is behind. |
| replication_lag | Time delay between when the transaction was committed on the provider and when processed locally. |
{.wide .expand}


---

[Upstream source](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/monitoring/lag_tracking.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
