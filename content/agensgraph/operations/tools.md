---
title: Server-side tools
linkTitle: Server-side tools
description: The tools that come with AgensGraph are PostgreSQL's, so PostgreSQL's reference for them applies in
  full and is not repeated here.
type: docs
weight: 50
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/operations/tools.html
upstream_source: agensgraph
upstream_modified: true
---


The tools that come with AgensGraph are PostgreSQL's, so
[PostgreSQL's reference for them](https://www.postgresql.org/docs/18/reference-server.html)
applies in full and is not repeated here. This page covers what is different, and what a
graph adds to the ones you use most.

For the interactive client and its graph meta-commands, see [The agens
client](/agensgraph/reference/agens/).

## What AgensGraph adds to the tool set {#what-agensgraph-adds-to-the-tool-set}

Two tools ship under a second name:

| AgensGraph name | PostgreSQL name | Difference |
| --- | --- | --- |
| `agens` | `psql` | Branding only. Both are installed, and the graph meta-commands work in either. |
| `ag_ctl` | `pg_ctl` | Branding only. Both are installed. |

```shell
agens --version
```

```
agens (PostgreSQL) 18.6 (AgensGraph 2.18.6.1)
```

> [!NOTE]
> A build from a development branch reports a `-devel` suffix instead.

```shell
psql --version
```

```
psql (PostgreSQL) 18.6 (AgensGraph 2.18.6.1)
```

Everything else — `initdb`, `pg_dump`, `pg_dumpall`, `pg_restore`, `pg_upgrade`,
`pg_basebackup`, `pg_controldata`, `pg_checksums`, `vacuumdb`, `reindexdb`, `createdb` and
the rest — keeps its PostgreSQL name and its PostgreSQL behaviour.

`AGDATA` works alongside `PGDATA` as the default data directory, so
`export AGDATA=/path/to/data` lets you drop `-D`. Exactly three binaries read it — `initdb`,
`pg_ctl` and `ag_ctl` — and they disagree on precedence: `initdb` prefers `AGDATA` over
`PGDATA`, while `pg_ctl` and `ag_ctl` prefer `PGDATA`. Every other tool takes `PGDATA` only.

## Starting and stopping {#starting-and-stopping}

```shell
ag_ctl -D /path/to/data -l /path/to/data/server.log start
ag_ctl -D /path/to/data status
ag_ctl -D /path/to/data reload
ag_ctl -D /path/to/data stop -m fast
```

Under systemd, use PostgreSQL's own unit conventions and point them at the AgensGraph
binaries; there is nothing graph-specific about it. See
[Deployment](/agensgraph/operations/deployment/).

## Dumping a graph {#dumping-a-graph}

`pg_dump` and `pg_dumpall` handle a graph without any special option, because a graph is a
schema and its labels are tables. A dump therefore contains the `CREATE GRAPH`,
`CREATE VLABEL` and `CREATE ELABEL` statements and the label data.

```shell
pg_dump -d mydb -f mydb.sql
pg_dump -d mydb -Fc -f mydb.dump
```

To dump one graph, name its schema:

```shell
pg_dump -d mydb --schema=moviekb -f moviekb.sql
```

Four things to know that are specific to graphs:

* **Neither tool checks the AgensGraph version.** Only PostgreSQL's own `server_version`
  range check applies, so restoring a newer dump into an older server shows up as a parse
  failure partway through rather than as a refusal up front.
* **A dump of a label that carries ordinary columns brackets its `ALTER TABLE` statements
  with `SET enable_graph_ddl = on`.** That setting is writable by any role, so an ordinary
  user can restore it — unless the role has it forced off with `ALTER ROLE … SET`.
* **A 2.18 dump will not restore into 2.17** if any graph uses [promoted
  columns](/agensgraph/querying/typed-columns/): the emitted `CREATE VLABEL` form is not one a 2.17
  parser accepts, and in a plain-text stream everything after that statement is lost.
* **A view defined over a Cypher query is dumped as the SQL that the Cypher lowered to**, not
  as your Cypher. It restores and works, but the definition you get back is not the
  definition you wrote. See [Combining SQL and
  Cypher](/agensgraph/querying/combining-sql-and-cypher/).

After a restore, rebuild the graph metadata and re-analyze — see
[Upgrading to 2.18](/agensgraph/release-notes/upgrade-to-2.18/#step-6-post-upgrade-tasks) for the
exact commands, which apply to any restore, not just an upgrade.

## Upgrading between major versions {#upgrading-between-major-versions}

`pg_upgrade` works on a graph with no special handling, with two AgensGraph-specific
conditions:

* It refuses a graph whose label carries a column beyond `id`, `start`, `end` and
  `properties`, rather than corrupting the physical column layout.
* Afterwards, `ag_graphmeta` is empty and the graph is marked invalid, so the planner's scan
  pruning is off until you run `regather_graphmeta()`.

[Upgrading to 2.18](/agensgraph/release-notes/upgrade-to-2.18/) is the full procedure, and
[Upgrade walkthrough](/agensgraph/release-notes/upgrade-walkthrough/) is a worked example with real
output.

## Base backups and WAL {#base-backups-and-wal}

`pg_basebackup`, WAL archiving, `pg_receivewal`, `pg_verifybackup` and `pg_rewind` all treat a
graph as what it is — schemas and tables in the same cluster — so a physical backup captures
graph and relational data together and at the same point in time. See
[Backup and recovery](/agensgraph/operations/backup/).
