---
title: Upgrade walkthrough
linkTitle: Upgrade walkthrough
description: '<!-- check-examples: skip because the examples need a 2.17 cluster and a freshly initialised 2.18
  cluster.'
type: docs
weight: 30
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/release_notes/upgrade-walkthrough.html
upstream_source: agensgraph
upstream_modified: true
---


<!-- check-examples: skip because the examples need a 2.17 cluster and a freshly
     initialised 2.18 cluster. The output was captured from a real upgrade. -->

# Upgrade walkthrough

A complete 2.17 to 2.18 upgrade on a small cluster, with the commands and the output they
produced. [Upgrading to 2.18](/agensgraph/release-notes/upgrade-to-2.18/) is the reference; this page is what it
looks like when you do it.

The cluster here holds one graph and one ordinary table, so you can see that both come
across:

```cypher
CREATE GRAPH social;
SET graph_path = social;
CREATE VLABEL person;
CREATE ELABEL knows;
CREATE (:person {name: 'Ann', age: 30}), (:person {name: 'Bo', age: 41});
MATCH (a:person {name: 'Ann'}), (b:person {name: 'Bo'}) CREATE (a)-[:knows {since: 2019}]->(b);
CREATE PROPERTY INDEX ON person (name);
```

```sql
CREATE TABLE audit (id serial primary key, note text);
INSERT INTO audit(note) VALUES ('before upgrade');
```

On 2.17 that reads back as:

```cypher
MATCH (n:person)-[r:knows]->(m:person) RETURN n.name, r.since, m.name;
```

```
 name  | since | name
-------+-------+------
 "Ann" | 2019  | "Bo"
```

## 1. Note the old cluster's checksum setting {#1-note-the-old-clusters-checksum-setting}

This decides one flag in the next step, and getting it wrong stops the upgrade before it
starts.

```shell
$OLD/bin/pg_controldata -D $OLDDATA | grep checksum
```

```
Data page checksum version:           0
```

Zero means checksums are off, which is the PostgreSQL 17 default.

## 2. Stop the old server {#2-stop-the-old-server}

```shell
$OLD/bin/ag_ctl -D $OLDDATA stop
```

## 3. Initialize the 2.18 cluster {#3-initialize-the-218-cluster}

Because the old cluster reported `0`, the new one has to be initialised with
`--no-data-checksums`. PostgreSQL 18 turns checksums on by default, so leaving the flag off
is what produces the failure in the next section.

```shell
$NEW/bin/initdb -D $NEWDATA -U postgres --encoding=UTF8 --no-data-checksums
```

```shell
$NEW/bin/pg_controldata -D $NEWDATA | grep checksum
```

```
Data page checksum version:           0
```

Both clusters now agree.

### What it looks like when they do not {#what-it-looks-like-when-they-do-not}

This is the whole output of `pg_upgrade --check` against a 2.18 cluster initialised without
that flag:

```
Performing Consistency Checks
-----------------------------
Checking cluster versions                                     ok

old cluster does not use data checksums but the new one does
Failure, exiting
```

It stops at the second check and changes nothing, so recovering is just a matter of
re-initialising the new cluster.

## 4. Check compatibility {#4-check-compatibility}

```shell
$NEW/bin/pg_upgrade -b $OLD/bin -B $NEW/bin -d $OLDDATA -D $NEWDATA -U postgres --check
```

```
Performing Consistency Checks
-----------------------------
Checking cluster versions                                     ok
Checking database connection settings                         ok
Checking database user is the install user                    ok
Checking for prepared transactions                            ok
Checking for contrib/isn with bigint-passing mismatch          ok
Checking for valid logical replication slots                  ok
Checking for subscription state                               ok
Checking data type usage                                      ok
Checking for objects affected by Unicode update               ok
Checking for not-null constraint inconsistencies              ok
Checking for presence of required libraries                   ok
Checking database user is the install user                    ok
Checking for prepared transactions                            ok
Checking for new cluster tablespace directories               ok

*Clusters are compatible*
```

## 5. Run the upgrade {#5-run-the-upgrade}

```shell
$NEW/bin/pg_upgrade -b $OLD/bin -B $NEW/bin -d $OLDDATA -D $NEWDATA -U postgres
```

The tail of the output:

```
Copying old pg_multixact/offsets to new server                ok
Deleting files from new pg_multixact/members                  ok
Copying old pg_multixact/members to new server                ok
Setting next multixact ID and offset for new cluster          ok
Resetting WAL archives                                        ok
Setting frozenxid and minmxid counters in new cluster         ok
Restoring global objects in the new cluster                   ok
Restoring database schemas in the new cluster                 ok
Copying user relation files                                   ok
Setting next OID for new cluster                              ok
Sync data directory to disk                                   ok
Creating script to delete old cluster                         ok
Checking for extension updates                                ok

Upgrade Complete
----------------
Some statistics are not transferred by pg_upgrade.
Once you start the new server, consider running these two commands:
    .../bin/vacuumdb -U postgres --all --analyze-in-stages --missing-stats-only
    .../bin/vacuumdb -U postgres --all --analyze-only
Running this script will delete the old cluster's data files:
    ./delete_old_cluster.sh
```

## 6. Start the new server and check what came across {#6-start-the-new-server-and-check-what-came-across}

```shell
$NEW/bin/ag_ctl -D $NEWDATA -l $NEW/logfile start
```

```sql
SELECT version();
```

```
 PostgreSQL 18.6 (AgensGraph 2.18.6.1) on x86_64-pc-linux-gnu, compiled by gcc ...
```

The graph, including the edge property:

```cypher
SET graph_path = social;
MATCH (n:person)-[r:knows]->(m:person) RETURN n.name, r.since, m.name;
```

```
 name  | since | name
-------+-------+------
 "Ann" | 2019  | "Bo"
```

The property index:

```psql
\d social.person
```

```
                              Table "social.person"
   Column   |  Type   | Nullable |                     Default
------------+---------+----------+-------------------------------------------------
 id         | graphid | not null | graphid(graph_labid('social.person'), nextval(…))
 properties | jsonb   | not null | jsonb_build_object()
Indexes:
    "person_pkey" PRIMARY KEY, btree (id)
    "person_name_idx" btree ((properties.'name'))
```

And the ordinary table:

```sql
SELECT * FROM audit;
```

```
 id |      note
----+----------------
  1 | before upgrade
```

## 7. The three post-upgrade tasks {#7-the-three-post-upgrade-tasks}

### Statistics {#statistics}

```shell
$NEW/bin/vacuumdb -U postgres --all --analyze-in-stages
```

### Graph metadata {#graph-metadata}

A binary upgrade leaves `ag_graphmeta` empty and the graph marked invalid, so the planner's
scan pruning is off:

```sql
SELECT graphname, graphmeta_valid FROM pg_catalog.ag_graph;
```

```
 graphname | graphmeta_valid
-----------+-----------------
 social    | f
```

Rebuild it, once per graph:

```sql
SET graph_path = social;
SELECT regather_graphmeta();
```

```
NOTICE:  regathering graphmeta...
 regather_graphmeta
--------------------
 t
```

```sql
SELECT graphname, graphmeta_valid FROM pg_catalog.ag_graph;
```

```
 graphname | graphmeta_valid
-----------+-----------------
 social    | t
```

### Edge label statistics {#edge-label-statistics}

The upgrade carries the old statistics target across, which is the value 2.17 used:

```sql
SELECT attname, attstattarget FROM pg_attribute
WHERE attrelid = 'social.knows'::regclass AND attname IN ('start', 'end')
ORDER BY 1;
```

```
 attname | attstattarget
---------+---------------
 end     |         10000
 start   |         10000
```

10000 is high enough to cost real planning time on a large edge label, and 2.18 creates new
edge labels with 1000. Bring the upgraded labels into line:

```sql
ALTER TABLE social.knows ALTER COLUMN start SET STATISTICS 1000;
ALTER TABLE social.knows ALTER COLUMN "end" SET STATISTICS 1000;
ANALYZE social.knows;
```

## 8. Remove the old cluster {#8-remove-the-old-cluster}

Only after you are satisfied the new one is working:

```shell
./delete_old_cluster.sh
```

Until you run that, the 2.17 data directory is untouched and you can roll back by stopping
the new server and starting the old one — provided you did not use `--link`.
