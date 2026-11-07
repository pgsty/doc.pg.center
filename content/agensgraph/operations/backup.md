---
title: Backup and recovery
linkTitle: Backup and recovery
description: A graph is stored as PostgreSQL schemas and tables, so every PostgreSQL backup method covers it, and
  covers it at the same point in time as your relational data.
type: docs
weight: 40
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/operations/backup.html
upstream_source: agensgraph
upstream_modified: true
---


A graph is stored as PostgreSQL schemas and tables, so every PostgreSQL backup method covers
it, and covers it at the same point in time as your relational data. There is no separate
graph backup to take and no separate restore to coordinate.

That means [PostgreSQL's backup chapter](https://www.postgresql.org/docs/18/backup.html) is
the reference, and this page covers the choices and the graph-specific details.

## Which method {#which-method}

| Method | What it gives you | When to use it |
| --- | --- | --- |
| `pg_dump` / `pg_dumpall` | A logical copy: SQL statements, or an archive. Portable across major versions and platforms. | Moving a database, copying one graph, keeping a version-independent copy. |
| `pg_basebackup` | A physical copy of the whole cluster. | The base of a point-in-time-recovery setup, and for seeding a replica. |
| Continuous archiving | A base backup plus every WAL segment since, so you can recover to any moment. | Production, where losing an hour of writes is not acceptable. |
| A filesystem snapshot | A physical copy taken by the storage layer. | Only if the snapshot is atomic across every filesystem the cluster uses. |

Copying the data directory with `cp` while the server is running is not a backup. Copying
individual table files is never a backup — the commit log is cluster-wide, so a file taken
on its own has no way to say which of its rows are committed.

## Logical backup {#logical-backup}

```shell
pg_dump -d mydb -Fc -f mydb.dump          # one database, archive format
pg_dumpall -f cluster.sql                  # every database plus roles
pg_dump -d mydb --schema=moviekb -f g.sql  # one graph
```

Restoring:

```shell
pg_restore --exit-on-error -d mydb mydb.dump
psql -d postgres -f cluster.sql
```

> [!WARNING]
> Both tools carry on past an error by default, and `psql` exits 0 having done so, so a restore
> can report success with objects missing — a constraint the server refuses leaves the table
> without it, and rows that reference nothing are then accepted. `--exit-on-error` makes
> `pg_restore` stop at the first one.
>
> `psql` has `ON_ERROR_STOP`, but it cannot be used on a `pg_dumpall` file: the file re-creates
> the bootstrap superuser, which already exists, so the restore would stop on line 14 and load
> nothing. Read the output of that one, or dump each database separately with `pg_dump -Fc` and
> restore it with `pg_restore --exit-on-error`.

Naming the schema is how you dump a single graph, since a graph *is* a schema. The dump
contains the `CREATE GRAPH`, `CREATE VLABEL` and `CREATE ELABEL` statements as well as the
data, so a restore rebuilds the graph structure.

Four graph-specific points, all covered in more detail in [Server-side
tools](/agensgraph/operations/tools/#dumping-a-graph):

* Neither tool checks the AgensGraph version, only PostgreSQL's.
* A dump of a label carrying ordinary columns needs `enable_graph_ddl` during the restore,
  and brackets its own statements with it.
* A 2.18 dump will not restore into 2.17 if any graph uses promoted columns.
* A view over a Cypher query is dumped as the SQL the Cypher lowered to.

After any restore, rebuild the graph metadata and the statistics:

```sql
SET graph_path = <your graph>;
SELECT regather_graphmeta();
```

```shell
vacuumdb -d mydb --analyze-in-stages
```

## Physical backup and point-in-time recovery {#physical-backup-and-point-in-time-recovery}

The mechanics are PostgreSQL's, unchanged. In outline:

Set the server up for archiving, then restart:

```
wal_level = replica
archive_mode = on
archive_command = 'test ! -f /mnt/archive/%f && cp %p /mnt/archive/%f'
```

`wal_level = minimal` does not record enough to recover from an archive, so it rules this
method out.

Take a base backup:

```shell
pg_basebackup -D /mnt/backup/base -Ft -z -P -X stream
```

To recover, restore the base backup into an empty data directory, then tell the server where
to fetch the archived WAL:

```
restore_command = 'cp /mnt/archive/%f %p'
recovery_target_time = '2026-09-02 14:30:00'
```

Those go in `postgresql.conf`, and an empty file named `recovery.signal` in the data
directory is what puts the server into recovery. When recovery finishes, the server removes
the signal file and starts accepting connections.

> [!NOTE]
> If you are working from older AgensGraph or PostgreSQL notes, three things have moved.
> Recovery settings live in `postgresql.conf` with a `recovery.signal` file, not in a
> `recovery.conf` — that file was removed in PostgreSQL 12, and a server will refuse to start
> if it finds one. The WAL directory is `pg_wal`, not `pg_xlog`, and the commit log is
> `pg_xact`, not `pg_clog`; both were renamed in PostgreSQL 10.

Verify a base backup before you rely on it:

```shell
pg_verifybackup /mnt/backup/base
```

## Higher-level tools {#higher-level-tools}

`pgBackRest` and `Barman` both manage retention, parallel compression, incremental backups
and restore orchestration, and both work on an AgensGraph cluster with no graph-specific
configuration. If you are running more than one server, either is a better answer than a
hand-written `archive_command`.

## What to check {#what-to-check}

A backup you have not restored is a hope, not a backup. For a graph specifically, a restore
test should confirm more than that the server starts:

```cypher
SET graph_path = <your graph>;
MATCH (n) RETURN label(n) AS label, count(*) ORDER BY label;
MATCH ()-[e]->() RETURN label(e) AS label, count(*) ORDER BY label;
```

```sql
SELECT graphname, graphmeta_valid FROM pg_catalog.ag_graph;
SELECT * FROM pg_catalog.ag_property_indexes;
```

Counts that match the source, plus the indexes and constraints being present, is what tells
you the graph came back whole.
