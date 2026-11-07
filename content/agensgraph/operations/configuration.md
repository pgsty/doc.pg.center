---
title: Configuration
linkTitle: Configuration
description: AgensGraph's configuration is PostgreSQL's, plus eleven settings of its own.
type: docs
weight: 20
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/operations/configuration.html
upstream_source: agensgraph
upstream_modified: true
---


AgensGraph's configuration is PostgreSQL's, plus eleven settings of its own. This page covers
how to set things and which settings matter for a graph workload. For the settings AgensGraph
adds, see [Server settings](/agensgraph/reference/guc/). For the several hundred PostgreSQL settings
this page does not list, see [PostgreSQL's server-configuration
chapter](https://www.postgresql.org/docs/18/runtime-config.html) — it applies unchanged.

## Where a setting can be set {#where-a-setting-can-be-set}

The scopes go from widest to narrowest, and the narrowest one that applies wins.

| How | Scope | Notes |
| --- | --- | --- |
| `postgresql.conf` | The whole cluster | Edit the file, then `ag_ctl reload` — or restart, for a setting whose context is `postmaster`. |
| `ALTER SYSTEM SET` | The whole cluster | Writes `postgresql.auto.conf`; still needs a reload or restart. |
| `ALTER DATABASE db SET` | One database | Takes effect on the next connection. |
| `ALTER ROLE r SET` | One role | Takes effect on the next connection. |
| `SET` | The current session | Reverts on disconnect. `SET LOCAL` reverts at the end of the transaction. |

`graph_path` is the setting you will meet first, and it is per-session by nature. Set it for
the database if every session wants the same graph:

```sql
ALTER DATABASE mydb SET graph_path = moviekb;
```

To see what a setting is now, and where the value came from:

```sql
SELECT name, setting, source, sourcefile, sourceline
FROM pg_settings WHERE name = 'work_mem';
```

`SHOW ALL` lists everything. `pg_settings` is the same information as a table you can filter,
which is more useful — its `boot_val` column is the built-in default, `reset_val` is what a
`RESET` would give you, and `context` tells you whether a change needs a restart.

> [!NOTE]
> Read a setting's built-in default from `pg_settings.boot_val` rather than from the commented
> `postgresql.conf.sample` in the installation directory. `boot_val` is the value the server
> actually starts with.

## Memory {#memory}

These four decide most of a server's behaviour, and PostgreSQL's defaults are deliberately
small enough to start anywhere.

**`shared_buffers`** — the server's own page cache. The default is 128 MB. On a dedicated
machine, 25% of RAM is a reasonable starting point. Going far above 40% is usually
counterproductive, because the operating system's cache is also holding those pages. Needs a
restart.

**`work_mem`** — how much memory one sort or hash may use before it spills to disk. The
default is 4 MB. It is per-operation, not per-connection: a graph query can hold several
hashes at once, and a query with many joins can use a multiple of this value. So raise it in
steps, and watch for the server running out of memory.

**`maintenance_work_mem`** — for `VACUUM`, `ANALYZE`, `CREATE INDEX` and `REINDEX`. Worth
raising substantially and temporarily when you build indexes after a bulk load, because it
is only used by one command at a time.

**`effective_cache_size`** — not an allocation, a hint. It tells the planner roughly how much
memory the machine has for caching. That estimate is what makes an index scan look
affordable. Set it to about 50-75% of RAM. Leaving it at the 4 GB default on a large machine
is the most common reason a graph traversal chooses a sequential scan when an index scan
would win.

## Planner settings that matter for traversal {#planner-settings-that-matter-for-traversal}

**`random_page_cost`** — the planner's estimate of a random page read relative to a
sequential one, default 4. That ratio describes a spinning disk. On SSD or NVMe the real
ratio is far closer to 1, and a graph traversal is almost all random access: it follows edges
by index into scattered heap pages. Lowering it to around 1.1 on flash storage is the single
change most likely to make traversal plans better.

Do not take that on faith and do not push it to an extreme. Measure it: run your slowest
traversal with `EXPLAIN (ANALYZE, BUFFERS)` at 4 and at 1.1 and compare, then keep the value
that wins on your data. A value near zero tells the planner that random I/O is free, which is
not true even in memory, and it will happily choose a plan that thrashes.

**`max_parallel_workers_per_gather`** — default 2. Graph writes do not run in parallel, and a
traversal is largely serial, so most of the benefit is on the sequential and bitmap scans a
`MATCH` lowers to. Raising it helps analytical queries over whole labels.

**`jit`** — on by default. It pays for itself on long-running analytical queries and costs
compile time on short ones. If your workload is many small traversals, measure it off.

## Asynchronous I/O on PostgreSQL 18 {#asynchronous-io-on-postgresql-18}

PostgreSQL 18 introduced asynchronous I/O, and graph queries get some of it for free. This is
worth understanding because the win is a configuration change rather than a query change.

A fixed-length `MATCH` lowers to ordinary sequential, bitmap and index scans over the label
tables, and PostgreSQL 18's read-ahead is used by **sequential scans and bitmap heap scans**.
Those therefore benefit automatically. Two things do not: a plain index scan's heap fetches
get no read-ahead in PostgreSQL 18, and the variable-length, shortest-path and Dijkstra
engines walk one vertex at a time by design.

Two settings control it:

**`effective_io_concurrency`** — defaults to 16 in PostgreSQL 18, up from 1. It gates the
whole mechanism, so if you carried a `postgresql.conf` forward from an older release and it
pins this to 1, you have turned asynchronous I/O off.

**`io_method`** — `worker` by default, which performs the reads in background workers.
`io_uring` is faster on Linux for cold scans, sometimes substantially, but it is only
available if the server was built with liburing. Check before you try to set it:

```sql
SELECT enumvals FROM pg_settings WHERE name = 'io_method';
```

```
 enumvals
---------------
 {sync,worker}
```

That build has no `io_uring`; one built with it lists three values. Changing `io_method`
needs a restart.

The benefit is largest when the data does not fit in cache, and near zero when it does. So
test with a cold cache if you want to see it. Do not expect it to help a shortest-path query,
which is bounded by serial probes rather than by I/O.

## Logging {#logging}

**`log_statement`** — `none` by default. Note the 2.18 change: `mod` now records Cypher
writes. Before 2.18 a Cypher statement counted as loggable only at `all`, so a server asked
to log data-modifying statements logged a SQL `INSERT` and silently skipped the
`CREATE` beside it.

**`log_min_duration_statement`** — the setting to reach for when a graph workload is slow but
you do not know which query. It logs any statement over the threshold, Cypher included.

**`auto_explain`** — a contrib module, and the most useful diagnostic on a graph workload,
because a slow traversal usually means the plan changed rather than the data grew:

```
shared_preload_libraries = 'auto_explain'
auto_explain.log_min_duration = '3s'
auto_explain.log_analyze = on
```

## Settings AgensGraph adds {#settings-agensgraph-adds}

Eleven, covered in [Server settings](/agensgraph/reference/guc/):
`allow_null_properties`, `auto_gather_graphmeta`, `cypher_allow_unsafe_ddl`, `eager_mem`,
`enable_eager`, `enable_graph_ddl`, `enable_graph_dml`, `enable_graph_endpoint_elision`,
`enable_multiple_update`, `enable_property_promotion`, `graph_path`.

The ones with an operational bearing:

* **`graph_path`** — the graph a session works in. Nothing resolves without it.
* **`auto_gather_graphmeta`** — keeps `ag_graphmeta` current so the planner can prune scans.
  It costs something on every write, so it is off by default; see [Graph
  metadata](/agensgraph/system-catalogs/graph-metadata/) for the trade-off and for
  `regather_graphmeta()`.
* **`enable_graph_dml`** and **`enable_graph_ddl`** — off by default, and they gate writing to
  and reshaping a label with SQL. Leave them off outside of maintenance work.
* **`eager_mem`** — the memory an eager graph-write plan may use, alongside `work_mem`.

## Where to go next {#where-to-go-next}

* [Deployment](/agensgraph/operations/deployment/) — sizing, the data directory, and running under systemd.
* [Security](/agensgraph/operations/security/) — authentication, roles, and permissions on a graph.
* [Query performance](/agensgraph/querying/performance/) — plan-shaped tuning, which is a different
  problem from this page.
