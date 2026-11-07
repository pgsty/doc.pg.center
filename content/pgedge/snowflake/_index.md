---
title: Snowflake
description: Using a Snowflake sequence allows you to take full advantage of the benefits offered by a distributed,
  multi-master replication solution.
weight: 30
upstream_source: pgedge-snowflake
upstream_link: https://github.com/pgEdge/snowflake/blob/429a16803c8c6336fcfede7cce0ccd3de05216d8/docs/index.md
upstream_modified: true
upstream_ref: 429a16803c8c
source_kind: pinned-main-snapshot
linkTitle: Snowflake
icon: fa-solid fa-book-open
sidebar_root_for: self
no_list: true
type: docs
sidebar_root_menu: false
---


> [!NOTE] Source version
> This is a pinned snapshot of upstream `main`; it may differ from the versioned documentation website. Check [versions and sources](/pgedge/about/attribution/) before deploying.


Using a [`Snowflake` sequence](https://github.com/pgEdge/snowflake?tab=readme-ov-file#snowflake-sequences-for-postgresql) allows you to take full advantage of the benefits offered by a distributed, multi-master replication solution. Snowflake is a Postgres extension that provides an int8 and sequence based unique ID solution to optionally replace the Postgres built-in bigserial data type. 

Internally, snowflakes are 64 bit integers represented externally as bigint values. The 64 bits are divided into bit fields:

* bit  63    - unused (sign of int8)
* bits 22-62 - timestamp with millisecond precision
* bits 12-21 - unique pgEdge Distributed Postgres node number
* bits 0-11   - counter within one millisecond
* The timestamp is a 41-bit unsigned value representing millisecond precision and an epoch of 2023-01-01.
* The counter is a 12-bit unsigned value that increments per ID allocation. This provides for 4096 unique IDs per millisecond, or 4 million IDs per second.
* The node number is a 10-bit unique identifier for the Postgres instance inside a global cluster. This value is set with the `snowflake.node` GUC in the `postgresql.conf` file.

Snowflake sequences let you:

* add or modify data in different regions while ensuring a unique transaction sequence.
* preserve unique transaction identifiers without manual/administrative management of a numbering scheme.
* accurately identify the order in which globally distributed transactions are performed.

Snowflake sequences also alleviate concerns that network lag could disrupt sequences in distributed transactions.

A Snowflake sequence is made up of a timestamp, a counter, and a unique node identifier; these components are sized to ensure over 18 trillion unique sequence numbers. The extension supports versatile commands and [functions](/pgedge/snowflake/snowflake-functions/) that simplify [creating a new Snowflake sequence](/pgedge/snowflake/creating/) or [converting an existing sequence](/pgedge/snowflake/converting/).

## Continue reading {#continue-reading}

- [Changelog](/pgedge/snowflake/changelog/)
- [Converting a PostgreSQL Sequence to a Snowflake Sequence](/pgedge/snowflake/converting/)
- [Creating a Snowflake Sequence in a New Cluster](/pgedge/snowflake/creating/)
- [Reviewing Sequence Definitions in your Table Meta-data](/pgedge/snowflake/review-seq/)
- [Snowflake Functions](/pgedge/snowflake/snowflake-functions/)

---

[Upstream source](https://github.com/pgEdge/snowflake/blob/429a16803c8c6336fcfede7cce0ccd3de05216d8/docs/index.md) · `429a16803c8c` · Copyright (c) 2023–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
