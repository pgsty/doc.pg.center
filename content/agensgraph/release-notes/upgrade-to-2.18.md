---
title: Upgrading to 2.18
linkTitle: Upgrading to 2.18
description: '<!-- check-examples: skip because the examples act on two clusters and on a graph the reader names.'
type: docs
weight: 20
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/release_notes/upgrade-to-2.18.html
upstream_source: agensgraph
upstream_modified: true
---


<!-- check-examples: skip because the examples act on two clusters and on a graph
     the reader names. The walkthrough page carries a transcript of a real run. -->

# Upgrading to 2.18

AgensGraph 2.18 is built on PostgreSQL 18, so moving to it is a major-version upgrade: the
data directory format changed and a 2.17 data directory cannot be started by 2.18 binaries.
You have two routes — `pg_upgrade`, which reuses the existing data files and is fast, or a
dump and reload.

Before either one, read [what changed](/agensgraph/release-notes/2.18/#migrating-to-218) and check your
application against it. Several changes will break queries that work on 2.17, and none of
them are caught by the upgrade tooling.

## Check your application first {#check-your-application-first}

Work through this list against your codebase. Each item is a change that turns working 2.17
code into an error or a different answer on 2.18.

* **Identifiers named `xor`, `current_graph` or `current_property_graph`** — now reserved
  words. Rename them, or quote them with **double quotes** (`MATCH (n:"xor")`); a backtick is
  not a quoting character here. `let` and `finish` as a variable name, and `let` as a label,
  are also refused, and `CREATE VLABEL insert;` needs quoting even though the pattern spelling
  `MATCH (n:insert)` still works. See [Keywords](/agensgraph/appendix/keywords/) for the matrix of
  which word fails in which position.
* **`call(...)` or `(call { ... })`** — a function literally named `call`, or a node pattern
  whose variable is `call` carrying a property map and no label. Both change meaning; quote
  the name.
* **A condition that is not a boolean** — `WHERE n.count`, `FILTER n.name`. These used to
  select on non-zero or non-empty and now raise a cast error. Add `::boolean` or compare
  explicitly.
* **`collect()` over a vertex, edge or path** — now returns a native array rather than a
  jsonb array of pictures. Client code that parsed the jsonb form must change; code that
  reads properties off the collected elements starts working.
* **`min()` / `max()` over a vertex or edge** — now ambiguous and therefore an error. Use
  `min(v::jsonb)` or `min(id(v))`.
* **`range()`, `toStringList`, `toIntegerList`, `toFloatList`** — changed return types.
* **`WITH … WHERE` with `SKIP` or `LIMIT`** — pages after the filter now, which changes
  result sets.
* **Row-level security over a graph** — RLS is now actually enforced on graph writes. If you
  have policies on labels, re-test them: writes that used to slip through will be refused.
* **`ALTER TABLE` against a label** — refused for anything structural. Use the label DDL, or
  set `enable_graph_ddl`.
* **`EXPLAIN` regression baselines** — plan text changed for `count()` over an element, for
  property reads, and for variable-length traversal nodes.
* **A foreign key whose two sides are collated differently** — refused (`42P21`) when either
  collation is nondeterministic. 2.17 built it. Both sides carrying the *same*
  nondeterministic collation is still fine, and so are two different deterministic ones.
  `NOT VALID` does not defer it, and a foreign key on a label column is refused the same way.
  This one is not only an application change: a 2.17 dump restores the table **without the
  constraint**. Find the pairs before you upgrade — see [Foreign keys with a nondeterministic
  collation](#foreign-keys-with-a-nondeterministic-collation).

## Foreign keys with a nondeterministic collation {#foreign-keys-with-a-nondeterministic-collation}

Run this on the **2.17** cluster, in every database, before you dump or upgrade:

```sql
SELECT c.conrelid::regclass AS referencing, c.conname, fa.attname AS col,
       fc.collname AS referencing_collation, pc.collname AS referenced_collation
  FROM pg_constraint c
  CROSS JOIN LATERAL unnest(c.conkey, c.confkey) AS k(fkatt, pkatt)
  JOIN pg_attribute fa ON fa.attrelid = c.conrelid AND fa.attnum = k.fkatt
  JOIN pg_attribute pa ON pa.attrelid = c.confrelid AND pa.attnum = k.pkatt
  JOIN pg_collation fc ON fc.oid = fa.attcollation
  JOIN pg_collation pc ON pc.oid = pa.attcollation
 WHERE c.contype = 'f'
   AND fa.attcollation <> pa.attcollation
   AND NOT (fc.collisdeterministic AND pc.collisdeterministic);
```

Every row is a constraint 2.18 will refuse. Give the two columns the same collation on 2.17,
then dump. The condition is the one the server applies, read from the same catalog column, so
it selects neither more nor fewer constraints than the upgrade will refuse.

> [!WARNING]
> Neither route warns you. `pg_upgrade --check` ends with `*Clusters are compatible*` and the
> upgrade then fails when it rebuilds the constraint. A dump and reload is worse: the restore
> reports success and the table arrives **without its foreign key**, after which rows that
> reference nothing are accepted.

## Route 1. Using pg_upgrade {#route-1-using-pg_upgrade}

`pg_upgrade` creates the new cluster's catalogs and then reuses the existing user data files,
so it does not rewrite your data. Because a graph is stored as ordinary schemas and tables,
graph data migrates exactly as relational data does.

### Before you begin {#before-you-begin}

* **Install 2.18 in a separate location.** Do not overwrite the 2.17 installation:
  `pg_upgrade` needs both sets of binaries, and keeping 2.17 in place is what makes rollback
  possible.
* **Disk space.** By default the data files are copied, so you need room for a second copy.
  `--link` hard-links them instead — almost instant, little extra space — but both data
  directories must be on one filesystem and rollback becomes impossible once the new server
  starts.
* **Install the same external modules** in the 2.18 installation that the 2.17 cluster uses,
  `pgvector` for example. AgensGraph's own graph features are built into the server, so there
  is no graph extension to recreate.
* **A label carrying an ordinary column blocks the upgrade.** `pg_upgrade` delegates to
  `pg_dump --binary-upgrade`, which refuses a graph label that has a column beyond `id`,
  `start`, `end` and `properties`, rather than silently corrupting the physical column
  layout. Find them before you start:

  ```sql
  SELECT c.relname, a.attname
  FROM pg_catalog.ag_label l
    JOIN pg_class c ON c.oid = l.relid
    JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum > 0 AND NOT a.attisdropped
  WHERE a.attname NOT IN ('id', 'start', 'end', 'properties');
  ```

  Drop those columns, or move the data elsewhere, before upgrading.
* Run every command as the operating-system user that owns the data directory.

The commands below use these variables:

```shell
export OLD=/usr/local/agensgraph-2.17
export NEW=/usr/local/agensgraph-2.18
export OLDDATA=$OLD/data
export NEWDATA=$NEW/data
```

### Step 1. Stop the old server {#step-1-stop-the-old-server}

Both clusters must be down while `pg_upgrade` runs.

```shell
$OLD/bin/ag_ctl -D $OLDDATA stop
```

### Step 2. Initialize the new cluster {#step-2-initialize-the-new-cluster}

Use the same superuser, encoding and locale as the old cluster — and match its data-checksum
setting.

```shell
$NEW/bin/initdb -D $NEWDATA -U postgres --encoding=UTF8 --no-data-checksums
```

> [!WARNING]
> **`--no-data-checksums` is not optional for most upgrades.** PostgreSQL 18 turns data page
> checksums on by default, and PostgreSQL 17 turned them off. So unless your 2.17 cluster was
> initialised with `-k`, the two clusters disagree and `pg_upgrade` stops before it does
> anything:
>
>     Performing Consistency Checks
>     -----------------------------
>     Checking cluster versions                                     ok
>
>     old cluster does not use data checksums but the new one does
>     Failure, exiting
>
> Check which side you are on before initialising:
>
>     $OLD/bin/pg_controldata -D $OLDDATA | grep checksum
>
> If it reports `Data page checksum version: 0`, pass `--no-data-checksums`. If it reports `1`,
> leave the flag off. Turning checksums on is a separate operation — see
> [`pg_checksums`](https://www.postgresql.org/docs/18/app-pgchecksums.html) — and it is worth
> doing, but do it after the upgrade, not as part of it.

### Step 3. Check compatibility {#step-3-check-compatibility}

`--check` validates both clusters and changes nothing.

```shell
$NEW/bin/pg_upgrade \
  -b $OLD/bin -B $NEW/bin \
  -d $OLDDATA -D $NEWDATA \
  -U postgres --check
```

A successful check ends with `*Clusters are compatible*`.

> [!WARNING]
> A green check does not mean the upgrade will succeed. It does not look for [foreign keys with
> a nondeterministic collation](#foreign-keys-with-a-nondeterministic-collation), which Step 4
> then fails on while rebuilding the constraint. Run that query yourself.

Pass the database superuser with `-U`. By default `pg_upgrade` connects as your
operating-system user, which is usually not a database role.

### Step 4. Run the upgrade {#step-4-run-the-upgrade}

The same command without `--check`:

```shell
$NEW/bin/pg_upgrade \
  -b $OLD/bin -B $NEW/bin \
  -d $OLDDATA -D $NEWDATA \
  -U postgres
```

It finishes with `Upgrade Complete`. Add `--link` to both the check and the upgrade to
hard-link the data files instead of copying them.

### Step 5. Start the new server {#step-5-start-the-new-server}

```shell
$NEW/bin/ag_ctl -D $NEWDATA -l $NEW/logfile start
```

Confirm you are on the new server, and that the graph came across:

```sql
SELECT version();
```

```cypher
SET graph_path = <your graph>;
MATCH (n) RETURN count(n);
```

### Step 6. Post-upgrade tasks {#step-6-post-upgrade-tasks}

Three of these are AgensGraph-specific and none of them are optional.

**Rebuild statistics.** `pg_upgrade` does not carry optimizer statistics across, so plans
will be poor until they are rebuilt:

```shell
$NEW/bin/vacuumdb -U postgres --all --analyze-in-stages
```

**Re-gather graph metadata.** `ag_graphmeta` drives the planner's scan pruning. A
binary upgrade leaves it empty and marks the graph invalid, so pruning is off until you
rebuild it, once per graph:

```sql
SET graph_path = <your graph>;
SELECT regather_graphmeta();
```

Check that it took:

```sql
SELECT graphname, graphmeta_valid FROM pg_catalog.ag_graph;
```

**Re-tune edge label statistics.** 2.18 lowered the statistics target on a new edge label's
`start` and `end` columns from 10000 to 1000. Labels created on 2.17 keep the old value and
pay a large planning cost on every edge join — hundreds of milliseconds on a big label. For
each edge label:

```sql
ALTER TABLE <graph>.<elabel> ALTER COLUMN start SET STATISTICS 1000;
ALTER TABLE <graph>.<elabel> ALTER COLUMN "end" SET STATISTICS 1000;
ANALYZE <graph>.<elabel>;
```

Then, once you have confirmed the upgraded cluster is working, remove the old data files with
the script `pg_upgrade` wrote in the directory you ran it from:

```shell
./delete_old_cluster.sh
```

### Rolling back {#rolling-back}

In copy mode, and before you run `delete_old_cluster.sh`, the 2.17 data directory is
untouched. Stop the new server and start the old one:

```shell
$NEW/bin/ag_ctl -D $NEWDATA stop
$OLD/bin/ag_ctl -D $OLDDATA -l $OLD/logfile start
```

After a `--link` upgrade, rollback is not possible once the new server has started, because
the two clusters share data files. Restore from a backup.

## Route 2. Dump and reload {#route-2-dump-and-reload}

Slower, but it rewrites everything and needs no second copy of the binaries at runtime.

```shell
$OLD/bin/pg_dumpall -U postgres -f cluster.sql
# start the 2.18 cluster, then:
$NEW/bin/psql -U postgres -d postgres -f cluster.sql
```

> [!WARNING]
> `psql` does not stop on error, and exits 0 even when statements failed. Anything the new
> server refuses — a [foreign key with a nondeterministic
> collation](#foreign-keys-with-a-nondeterministic-collation), for instance — is one line in the
> output and the restore carries on without it. Read the log before you believe the restore.

To have the restore stop instead, dump the roles apart from the data. The roles cannot be
restored under `ON_ERROR_STOP`: `pg_dumpall` writes `CREATE ROLE` for the bootstrap superuser,
which already exists on the new cluster, and `--clean --if-exists` only moves the failure to
the `DROP ROLE` of the role you are connected as.

```shell
$OLD/bin/pg_dumpall -U postgres --globals-only -f globals.sql
$OLD/bin/pg_dump    -U postgres -Fc -d mydb -f mydb.dump       # once per database
# start the 2.18 cluster, then:
$NEW/bin/psql -U postgres -d postgres -f globals.sql           # roles; errors here are benign
$NEW/bin/createdb -U postgres mydb
$NEW/bin/pg_restore -U postgres --exit-on-error -d mydb mydb.dump
```

Two things to know:

* **A restore may need `enable_graph_ddl`.** A dump of a label that carries ordinary columns
  emits `SET enable_graph_ddl = on` around its `ALTER TABLE … ADD COLUMN` statements. That
  setting is writable by any role, so an ordinary user can restore — unless the role has it
  forced off by `ALTER ROLE … SET`.
* **The graph metadata and statistics tasks above still apply.**

## Downgrading is not supported {#downgrading-is-not-supported}

A 2.18 dump will not restore into 2.17 if any graph uses [promoted
columns](/agensgraph/querying/typed-columns/). The dump contains a `CREATE VLABEL` form that a 2.17
parser rejects, and in a plain-text stream everything after that statement is lost. Keep a
2.17 backup taken before the upgrade if you need a way back.

Note also that `pg_dump` and `pg_restore` do not check the AgensGraph version. Only
PostgreSQL's `server_version` range check applies. So a mismatch shows up as a parse failure
partway through a restore, rather than as a refusal up front.

## A worked example {#a-worked-example}

[Upgrade walkthrough](/agensgraph/release-notes/upgrade-walkthrough/) runs the whole procedure on a small cluster
with real commands and output.
