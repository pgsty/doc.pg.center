---
title: Deployment
linkTitle: Deployment
description: What to decide before an AgensGraph server carries production traffic.
type: docs
weight: 10
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/operations/deployment.html
upstream_source: agensgraph
upstream_modified: true
---


What to decide before an AgensGraph server carries production traffic. The mechanics of
getting the software onto a machine are in [Install AgensGraph](/agensgraph/get-started/install/);
this page is about the choices around it.

## Platforms {#platforms}

AgensGraph builds and runs on Linux and on Windows, and on macOS for development. Most
deployments are on Linux. The tested distributions are the current releases of Rocky Linux,
RHEL, Debian and Ubuntu. The [container
images](/agensgraph/get-started/install/#docker) are built on Debian trixie and bookworm, Rocky 9
and 10, and Alpine.

Nothing about AgensGraph narrows PostgreSQL's platform support, so
[PostgreSQL's supported-platforms notes](https://www.postgresql.org/docs/18/installation-platform-notes.html)
apply.

## Sizing {#sizing}

Start from the data, not from a table of recommendations.

**Memory is the lever that matters most.** A graph traversal follows edges by index into
scattered pages, so it is random-access work. Random access out of cache is slow. Aim for the
working set to fit in the operating system's cache: the labels a query walks, plus their
indexes. Size `shared_buffers` and
`effective_cache_size` against that, as described in [Configuration](/agensgraph/operations/configuration/#memory).

To see what you are dealing with:

```sql
SELECT l.labname,
       pg_size_pretty(pg_total_relation_size(l.relid)) AS total
FROM pg_catalog.ag_label l
  JOIN pg_catalog.ag_graph g ON g.oid = l.graphid
WHERE g.graphname = 'moviekb'
ORDER BY pg_total_relation_size(l.relid) DESC;
```

An edge label is usually the largest object in a graph, and it carries three indexes of its
own, so budget for the indexes as well as the rows.

**Storage should be flash.** Not for throughput, but for random-read latency. That is where
traversal spends its time. It also changes how you configure the planner — see
`random_page_cost` in [Configuration](/agensgraph/operations/configuration/#planner-settings-that-matter-for-traversal).

**CPU matters less than you would expect** for traversal, which is largely serial, and more
than you would expect for analytical queries over whole labels, which parallelise.

A minimum for anything real is 4 GB of RAM. For disk, allow for the data, its indexes, the
WAL, and room to build an index. A base install itself needs about 2.5 GB.

## Before the first start {#before-the-first-start}

**Run the server as its own unprivileged user.** Not root, and not a login account shared
with an application:

```shell
useradd --system --home /var/lib/agensgraph --shell /usr/sbin/nologin agens
```

**Put the data directory on its own filesystem** if you can, so filling it cannot take the
rest of the machine with it, and so you can snapshot it independently.

```shell
install -o agens -g agens -m 0700 -d /var/lib/agensgraph/18/data
sudo -u agens initdb -D /var/lib/agensgraph/18/data
```

`initdb` insists on mode 0700 or 0750 on the data directory. On PostgreSQL 18 it also enables
data page checksums by default — worth keeping, and worth knowing about, because it decides a
flag if you later upgrade into this cluster. See [Upgrading to
2.18](/agensgraph/release-notes/upgrade-to-2.18/#step-2-initialize-the-new-cluster).

**Kernel resources** rarely need touching. AgensGraph, like PostgreSQL since 9.3, uses
anonymous mmap for its main shared memory and only a tiny System V segment, so the old
`SHMMAX` tuning is not needed. What can still bite is `vm.overcommit_memory` and the OOM
killer on a memory-constrained host, and the open-file limit on a server with many
connections. [PostgreSQL's kernel-resources
section](https://www.postgresql.org/docs/18/kernel-resources.html) is the reference.

## Running under systemd {#running-under-systemd}

A unit for a single instance:

```ini
[Unit]
Description=AgensGraph 2.18
After=network-online.target
Wants=network-online.target

[Service]
Type=notify
User=agens
Group=agens
Environment=AGDATA=/var/lib/agensgraph/18/data
ExecStart=/usr/local/agensgraph/bin/postgres -D ${AGDATA}
ExecReload=/bin/kill -HUP $MAINPID
KillMode=mixed
KillSignal=SIGINT
TimeoutStopSec=120
OOMScoreAdjust=-900

[Install]
WantedBy=multi-user.target
```

`Type=notify` with `postgres` started directly is the arrangement systemd handles best —
it lets systemd know when the server is actually accepting connections, and it keeps
`systemctl stop` doing a clean shutdown. `OOMScoreAdjust` makes the kernel prefer to kill a
backend rather than the postmaster.

Use `ag_ctl` for ad-hoc work, and systemd for the service. Mixing them — starting by hand and
stopping with systemd — is how you end up with a stale postmaster.

## Connections {#connections}

**`listen_addresses`** is `localhost` after `initdb`. Widen it deliberately, and only
together with the authentication rules below.

**`max_connections`** defaults to 100. Every connection costs memory, and a graph query can
use several `work_mem` allocations at once, so raising this is not free. Put a connection
pooler in front of an application that opens many short-lived connections;
AgensGraph speaks the PostgreSQL protocol, so PgBouncer and Pgpool-II work unchanged.

**Authentication** is `pg_hba.conf`, and the default `trust` for local connections is not
something to leave in place. See [Security](/agensgraph/operations/security/).

## Replication and high availability {#replication-and-high-availability}

Streaming replication, logical replication and synchronous commit all work on a graph,
because a graph is tables and the WAL does not know the difference. So a standby carries
graph data with no extra configuration, and read-only graph queries run on a hot standby.

Two AgensGraph-specific notes:

* Graph writes are not parallelised, so a write-heavy graph workload will not use more than
  one core per statement on the primary. This affects how you plan for write throughput,
  not how replication behaves.
* After promoting a standby, or after any physical restore, check
  `ag_graph.graphmeta_valid` and run `regather_graphmeta()` if it is false — see [Graph
  metadata](/agensgraph/system-catalogs/graph-metadata/).

Patroni is the usual choice for automated failover and works with AgensGraph as it does with
PostgreSQL.

## A pre-production checklist {#a-pre-production-checklist}

* `postgresql.conf` reviewed against [Configuration](/agensgraph/operations/configuration/), in particular
  `shared_buffers`, `work_mem`, `effective_cache_size` and `random_page_cost`.
* `pg_hba.conf` has no `trust` rule, and `listen_addresses` is no wider than it needs to be.
* Backups running, and a restore tested — including the graph counts, per [Backup and
  recovery](/agensgraph/operations/backup/#what-to-check).
* WAL archiving on, if losing recent writes is not acceptable.
* `log_min_duration_statement` set, and `auto_explain` loaded, so a slow query leaves
  evidence.
* Monitoring on connection count, replication lag, cache hit ratio and disk headroom.
* `autovacuum` left on. An edge label churns, and turning autovacuum off is how a graph
  database ends up with a table twice the size of its data.
* `auto_gather_graphmeta` decided deliberately: on, and pay a little on every write for
  planner scan pruning, or off, and re-gather on a schedule.
* Statistics targets on edge labels checked, especially if the cluster was upgraded from
  2.17 — see [Upgrading to
  2.18](/agensgraph/release-notes/upgrade-to-2.18/#step-6-post-upgrade-tasks).
