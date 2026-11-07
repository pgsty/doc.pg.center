---
title: Server settings
linkTitle: Server settings
description: AgensGraph adds eleven settings to PostgreSQL's several hundred.
type: docs
weight: 60
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/guc.html
upstream_source: agensgraph
upstream_modified: true
---


AgensGraph adds eleven settings to PostgreSQL's several hundred. This page documents those
eleven. Every other setting is PostgreSQL's, unchanged, and
[PostgreSQL's server-configuration chapter](https://www.postgresql.org/docs/18/runtime-config.html)
describes it. For *how* and *where* to set something, see
[Configuration](/agensgraph/operations/configuration/), which covers `postgresql.conf`,
`ALTER SYSTEM`, `ALTER DATABASE`, `ALTER ROLE` and `SET`.

One of the eleven, `graph_path`, is needed by every session that runs Cypher. The rest have
working defaults and you can ignore them until you have a reason not to.

## The settings {#the-settings}

Every default below is `pg_settings.boot_val`, read from a running server:

```sql
SELECT name, vartype AS type, boot_val AS default, coalesce(unit,'') AS unit, context
FROM pg_settings
WHERE name IN ('allow_null_properties','auto_gather_graphmeta','cypher_allow_unsafe_ddl',
               'eager_mem','enable_eager','enable_graph_ddl','enable_graph_dml',
               'enable_graph_endpoint_elision','enable_multiple_update',
               'enable_property_promotion','graph_path')
ORDER BY name;
```

```
             name              |  type   | default | unit |  context
-------------------------------+---------+---------+------+-----------
 allow_null_properties         | bool    | off     |      | user
 auto_gather_graphmeta         | bool    | off     |      | superuser
 cypher_allow_unsafe_ddl       | bool    | off     |      | user
 eager_mem                     | integer | 4096    | kB   | user
 enable_eager                  | bool    | on      |      | user
 enable_graph_ddl              | bool    | off     |      | user
 enable_graph_dml              | bool    | off     |      | superuser
 enable_graph_endpoint_elision | bool    | on      |      | user
 enable_multiple_update        | bool    | on      |      | user
 enable_property_promotion     | bool    | on      |      | user
 graph_path                    | string  |         |      | user
```

Read the two context values this way:

`user`
: Any role can change it, in any session, at any time. It can also be set in
  `postgresql.conf`, per database or per role.

`superuser`
: Only a superuser can change it in a session, or a role that has been granted `SET` on that
  parameter. Everyone else gets `permission denied to set parameter`.

Query `pg_settings` rather than reading `postgresql.conf.sample`. The sample file shipped in
the installation directory lists `enable_eager` and `enable_multiple_update` as `off`. Both
really default to `on`, so a table copied from that file would be wrong in two rows.

## agversion, a preset rather than a setting {#agversion-a-preset-rather-than-a-setting}

`agversion` reports the AgensGraph version. Its context is `internal`, which makes it a
*preset*: something the server tells you, not something you configure. It cannot appear in
`postgresql.conf`, and setting it is refused:

```sql
SET agversion = '1';
```

```
ERROR:  parameter "agversion" cannot be changed
```

```sql
SELECT name, setting, context, category FROM pg_settings WHERE name = 'agversion';
```

```
   name    |  setting   | context  |    category
-----------+------------+----------+----------------
 agversion | 2.18.6.1 | internal | Preset Options
```

Read it with `SHOW`, which is the usual way to check what you are connected to:

```sql
SHOW agversion;
```

```
 agversion
------------
 2.18.6.1
```

`version()` and `server_version` report the PostgreSQL version the release is built on. A
client that needs to know both should read both.

## graph_path {#graph_path}

```
string · default '' (empty) · context user
```

Names the graph a session works in. Every unqualified label name in a Cypher or GQL statement
resolves in that graph. Every graph DDL statement creates or alters a label there. It is the
graph analogue of `search_path`, and the one setting you cannot skip.

Nothing resolves without it:

```cypher
RESET graph_path;
MATCH (n:person) RETURN count(n);
```

```
ERROR:  graph_path is NULL
HINT:  Use SET graph_path
```

Set it and the same statement runs:

```sql
SET graph_path = moviekb;
SHOW graph_path;
```

```
 graph_path
------------
 moviekb
```

`CURRENT_GRAPH` reads the same value as a bare keyword inside a statement:

```cypher
SELECT CURRENT_GRAPH;
```

```
 current_graph
---------------
 moviekb
```

### Exactly one graph name {#exactly-one-graph-name}

Unlike `search_path`, `graph_path` is not a list. A comma-separated value is not parsed as two
names. It is taken as one name, and that name does not exist:

```sql
SET graph_path = 'moviekb, twins';
```

```
ERROR:  invalid value for parameter "graph_path": "moviekb, twins"
DETAIL:  graph "moviekb, twins" does not exist.
```

So a session reads and writes one graph. To reach two graphs in one statement, use SQL, which
sees them as two schemas. [Combining SQL and
Cypher](/agensgraph/querying/combining-sql-and-cypher/) has the patterns.

### When the value is checked {#when-the-value-is-checked}

A graph that does not exist is refused at `SET` time rather than at query time:

```sql
SET graph_path = nosuchgraph;
```

```
ERROR:  invalid value for parameter "graph_path": "nosuchgraph"
DETAIL:  graph "nosuchgraph" does not exist.
```

The name is an identifier, so it folds to lower case unless you quote it. A graph created with
a mixed-case name needs the quotes:

```cypher
CREATE GRAPH "MixedCase";
SET graph_path = MixedCase;
```

```
ERROR:  invalid value for parameter "graph_path": "mixedcase"
DETAIL:  graph "mixedcase" does not exist.
```

```sql
SET graph_path = "MixedCase";
SHOW graph_path;
```

```
 graph_path
------------
 MixedCase
```

```cypher
DROP GRAPH "MixedCase" CASCADE;
SET graph_path = moviekb;
```

### One value for a database or a role {#one-value-for-a-database-or-a-role}

`SET` lasts for the session. Two wider scopes save repeating it, and both take effect on the
next connection rather than the current one.

For everyone who connects to a database:

```sql
ALTER DATABASE docs SET graph_path = moviekb;
```

```
ALTER DATABASE
```

For one role, whichever database it connects to:

```sql
ALTER ROLE analyst SET graph_path = moviekb;
```

```
ALTER ROLE
```

Either is visible in `pg_db_role_setting`, and a role setting wins over a database setting:

```sql
SELECT r.rolname, s.setconfig FROM pg_db_role_setting s
JOIN pg_roles r ON r.oid = s.setrole WHERE r.rolname = 'analyst';
```

```
 rolname |      setconfig
---------+----------------------
 analyst | {graph_path=moviekb}
```

A role that connects afterwards has it already:

```sql
SHOW graph_path;
```

```
 graph_path
------------
 moviekb
```

`ALTER DATABASE … RESET graph_path` and `ALTER ROLE … RESET graph_path` remove them again. A
cluster-wide default in `postgresql.conf` works too, but it is rarely what you want. It makes
every database in the cluster claim to have that graph.

The value is checked against the catalog, so `ALTER DATABASE db SET graph_path` has to be run
while connected to `db`. The check looks for the graph in the *current* database. From
anywhere else it fails:

```sql
ALTER DATABASE docs SET graph_path = moviekb;
```

```
ERROR:  invalid value for parameter "graph_path": "moviekb"
DETAIL:  graph "moviekb" does not exist.
```

## allow_null_properties {#allow_null_properties}

```
bool · default off · context user
```

Decides whether a null property value is stored or dropped.

Off, assigning null removes the property. A property set to null and a property that was never
there are then the same thing. On, the null is stored as a JSON null and the key stays.

```cypher
CREATE GRAPH nulls;
SET graph_path = nulls;
CREATE VLABEL t;
CREATE (:t {name: 'a', extra: null});
SET allow_null_properties = on;
CREATE (:t {name: 'b', extra: null});
MATCH (n:t) RETURN n ORDER BY id(n);
```

```
                 n
------------------------------------
 t[3.1]{"name": "a"}
 t[3.2]{"name": "b", "extra": null}
```

Turn it on when you are loading data whose absent and null values mean different things and
you need to keep the distinction. That is typically an import from a relational source.

The cost is that a stored null is a key that is present without a value. The tests disagree
about it:

```cypher
MATCH (n:t) RETURN exists(n.extra) AS exists, n.extra IS NULL AS is_null,
                   properties(n) ? 'extra' AS key_present;
```

```
 exists | is_null | key_present
--------+---------+-------------
 f      | t       | t
```

`REMOVE n.extra` removes the key whatever the setting says. It is still the way to get rid of
a property.

```cypher
RESET allow_null_properties;
DROP GRAPH nulls CASCADE;
SET graph_path = moviekb;
```

## auto_gather_graphmeta {#auto_gather_graphmeta}

```
bool · default off · context superuser
```

Keeps `ag_graphmeta` up to date as a side effect of every graph write.

For each (start label, edge label, end label) triple in a graph, `ag_graphmeta` records how
many edges there are. The planner uses it to prune scans: a `MATCH` that cannot possibly match
a label is not scanned at all. With this setting off, the table is only as current as the last
`regather_graphmeta()` call.

Turning it on triggers an immediate full gather, so the table is correct from that point:

```sql
SET auto_gather_graphmeta = on;
```

```
NOTICE:  regathering graphmeta...
SET
```

```sql
SELECT g.graphname, se.labname AS start, e.labname AS edge, ee.labname AS "end", m.edgecount
FROM pg_catalog.ag_graphmeta m
JOIN pg_catalog.ag_graph g ON g.oid = m.graph
JOIN pg_catalog.ag_label e  ON e.graphid  = m.graph AND e.labid  = m.edge
JOIN pg_catalog.ag_label se ON se.graphid = m.graph AND se.labid = m.start
JOIN pg_catalog.ag_label ee ON ee.graphid = m.graph AND ee.labid = m."end"
WHERE g.graphname = 'moviekb' ORDER BY 3;
```

```
 graphname | start  |    edge    |  end  | edgecount
-----------+--------+------------+-------+-----------
 moviekb   | person | acted_in   | movie |        25
 moviekb   | person | directed   | movie |        21
 moviekb   | movie  | related_to | movie |        11
```

```cypher
RESET auto_gather_graphmeta;
```

Turn it on for a read-mostly graph, where accurate metadata is worth a little work on each
write. Leave it off for a write-heavy load and call `regather_graphmeta()` afterwards. You
must call it after `pg_upgrade` or a restore too. [Graph
metadata](/agensgraph/system-catalogs/graph-metadata/) covers the table and the pruning it enables.

## cypher_allow_unsafe_ddl {#cypher_allow_unsafe_ddl}

```
bool · default off · context user
```

Skips two catalog checks that normally stand between you and a graph the catalog no longer
describes. It exists to repair a graph, not to work in.

**It lets `graph_path` name a graph that does not exist.** The check moves from `SET` time to
query time, where the message is different:

```sql
SET cypher_allow_unsafe_ddl = on;
SET graph_path = nosuchgraph;
SHOW graph_path;
```

```
 graph_path
-------------
 nosuchgraph
```

```cypher
MATCH (n) RETURN count(n);
```

```
ERROR:  current graph_path "nosuchgraph" is invalid
HINT:  Use SET graph_path
```

```cypher
RESET cypher_allow_unsafe_ddl;
SET graph_path = moviekb;
```

**It lets a label be dropped as the wrong kind.** `DROP VLABEL` on an edge label is normally
refused. With the setting on it succeeds:

```cypher
CREATE GRAPH unsafe;
SET graph_path = unsafe;
CREATE ELABEL e;
DROP VLABEL e;
```

```
ERROR:  DROP VLABEL cannot DROP edge label
```

```cypher
SET cypher_allow_unsafe_ddl = on;
DROP VLABEL e;
```

```
DROP VLABEL
```

```cypher
RESET cypher_allow_unsafe_ddl;
DROP GRAPH unsafe CASCADE;
SET graph_path = moviekb;
```

Both are useful in exactly one situation: a graph whose catalog and tables disagree, which you
are trying to take apart. Set it for the statement that needs it and reset it immediately.

## eager_mem {#eager_mem}

```
integer · default 4096 · unit kB · context user · minimum 1024
```

How much memory one eager plan node may use before it spills to disk. It is `work_mem` for
eager plans, and like `work_mem` it is per node, not per query or per connection.

```sql
SHOW eager_mem;
SET eager_mem = '64MB';
SHOW eager_mem;
```

```
 eager_mem
-----------
 4MB
(1 row)

SET
 eager_mem
-----------
 64MB
(1 row)
```

The minimum is 1 MB, and a smaller value is refused rather than clamped:

```sql
SET eager_mem = '512kB';
```

```
ERROR:  512 kB is outside the valid range for parameter "eager_mem" (1024 kB .. 2147483647 kB)
```

```sql
RESET eager_mem;
```

Raise it when a write that reads what it writes is spilling; see
[`enable_eager`](#enable_eager). The default of 4 MB is the same conservative starting point
as `work_mem`'s. A statement that materialises a large intermediate result will beat it.

## enable_eager {#enable_eager}

```
bool · default on · context user
```

Allows the planner to build an *eager* plan: one that materialises a write's output before a
later clause reads it.

Some statements need one. Take a `CREATE` followed by a `MERGE` that could match what the
`CREATE` just made. The two cannot be interleaved row by row, because the second clause would
see a half-written graph. So the planner puts the first clause's result in a buffer. `EXPLAIN`
marks the node `eager`:

```cypher
CREATE GRAPH eager;
SET graph_path = eager;
CREATE VLABEL src;
CREATE VLABEL dst;
CREATE (:src {n: 1}), (:src {n: 2});
EXPLAIN (COSTS OFF) MATCH (a:src) CREATE (:dst {n: a.n}) MERGE (:dst {n: a.n + 10});
```

```
                                                   QUERY PLAN
----------------------------------------------------------------------------------------------------------------
 Graph Merge
   ->  Nested Loop CypherMerge Join
         Join Filter: ("<0000000000>".properties.'n' = ((_agens_default_s_1.a).properties.'n' `+` '10'::jsonb))
         ->  Subquery Scan on _agens_default_s_1
               ->  Graph Create eager
                     ->  Seq Scan on src a
         ->  Seq Scan on dst "<0000000000>"
```

Turning it off does not make such a statement run a different way. It makes it fail:

```cypher
SET enable_eager = off;
MATCH (a:src) CREATE (:dst {n: a.n}) MERGE (:dst {n: a.n + 10});
```

```
ERROR:  eagerness plan is not allowed.
```

```cypher
RESET enable_eager;
DROP GRAPH eager CASCADE;
SET graph_path = moviekb;
```

So this is not a cost-based toggle like PostgreSQL's `enable_hashjoin`. Leave it on. Turn it
off only to find out whether a statement depends on an eager plan, which matters when you are
trying to make a large write cheaper.

## enable_graph_ddl {#enable_graph_ddl}

```
bool · default off · context user
```

Allows SQL DDL to reshape a graph label.

A label's columns make it a graph label, and the graph catalog describes them. `ALTER TABLE`
does not update that catalog. Reshaping a label with it can leave the graph describing
something that is no longer true. Off, the attempts are refused, with a hint at the statement
that does keep the catalog in step:

```sql
ALTER TABLE moviekb.movie ADD COLUMN note text;
```

```
ERROR:  cannot add a column to graph label "movie" with ALTER TABLE
HINT:  Use ALTER VLABEL or ALTER ELABEL instead, which keeps the graph catalog in step.
```

```sql
ALTER TABLE moviekb.movie DROP COLUMN properties;
```

```
ERROR:  cannot drop a column of graph label "movie" with ALTER TABLE
HINT:  Use ALTER VLABEL or ALTER ELABEL instead, which keeps the graph catalog in step.
```

```sql
ALTER TABLE moviekb.movie NO INHERIT moviekb.ag_vertex;
```

```
ERROR:  cannot remove a parent label from graph label "movie" with ALTER TABLE
HINT:  A label's parents are fixed when it is created.
```

The full list of what is refused: adding, dropping or retyping a column; detaching or changing
a column's generation expression; dropping a not-null constraint, named either as the column or
as the constraint; adding or removing a parent label. The same setting also refuses renaming a
label's column and moving a label to another schema.

Turning it on lifts all of those. It does not grant anything: whoever may alter the label
still decides what happens to it. It only asks that the reshaping be deliberate.

Two things it never lifts. The type of `id`, `start`, `end` or `properties` cannot be changed
at all, because every vertex and edge is made of those columns:

```sql
SET enable_graph_ddl = on;
ALTER TABLE moviekb.movie ALTER COLUMN properties TYPE text;
```

```
ERROR:  cannot change the type of column "properties" of graph label "movie"
DETAIL:  Every vertex and edge is made of that column.
```

```sql
RESET enable_graph_ddl;
```

And renaming or dropping the table itself stays refused, with its own message
(`cannot rename table "movie"`, `cannot drop table … because vlabel … requires it`). Use
`ALTER VLABEL … RENAME TO` and `DROP VLABEL`.

You will meet this setting whether or not you set it yourself. For a label that carries
ordinary columns, `pg_dump` brackets the `ALTER TABLE` statements with
`SET enable_graph_ddl = on`, so that a restore works. See [Server-side
tools](/agensgraph/operations/tools/).

## enable_graph_dml {#enable_graph_dml}

```
bool · default off · context superuser
```

Allows SQL `INSERT`, `UPDATE`, `DELETE` and `MERGE` against a graph label.

Reading a label with SQL needs no setting. Writing one does, because Cypher's write path keeps
a graph consistent: endpoints that exist, an id that matches the label, and the metadata that
goes with them. Off, every SQL write is refused:

```psql
INSERT INTO moviekb.movie (properties) VALUES ('{"title": "x"}');
```

```
ERROR:  DML query to graph objects is not allowed
```

```psql
UPDATE moviekb.movie SET properties = '{}';
```

```
ERROR:  DML query to graph objects is not allowed
```

```sql
DELETE FROM moviekb.movie;
```

```
ERROR:  DML query to graph objects is not allowed
```

Turning it on gives up the guarantee that the graph means what it says. An `INSERT` into an
edge label does not check that the endpoints exist, so it can create a dangling edge. Cypher
cannot produce one:

```psql
CREATE GRAPH dangling;
SET graph_path = dangling;
CREATE VLABEL v;
CREATE ELABEL e;
CREATE (:v {n: 1});
SET enable_graph_dml = on;
INSERT INTO dangling.e (start, "end", properties)
VALUES ('3.1'::graphid, '99.99'::graphid, '{}');
RESET enable_graph_dml;
```

```
INSERT 0 1
```

The result is an edge that two different queries disagree about. A pattern that binds both
endpoints finds nothing, because the join to the missing vertex fails:

```cypher
MATCH (a)-[r:e]->(b) RETURN a, r, b;
```

```
 a | r | b
---+---+---
(0 rows)
```

A pattern that binds neither endpoint counts it, because nothing has to be joined:

```cypher
MATCH ()-[r:e]->() RETURN count(r) AS edges;
```

```
 edges
-------
 1
```

```cypher
DROP GRAPH dangling CASCADE;
SET graph_path = moviekb;
```

Turn it on for a bulk load you have written carefully, or to repair rows that Cypher cannot
reach, and turn it off again. It is one of the two `superuser` settings. An ordinary role that
tries `SET enable_graph_dml = on` gets
`ERROR:  permission denied to set parameter "enable_graph_dml"`, and cannot enable it for
itself.

## enable_graph_endpoint_elision {#enable_graph_endpoint_elision}

```
bool · default on · context user
```

Lets the planner drop the scan for a pattern endpoint that the query never uses.

An anonymous endpoint such as `->()` contributes nothing but a join. If the endpoint carries
no label and no property filter, that join cannot remove a row either. The planner removes it.
It removes a named endpoint too when the name is only used to constrain a label. A label test
on an edge's endpoint id is a `graphid` range check on the edge itself:

```cypher
EXPLAIN (COSTS OFF) MATCH (p:person)-[r:acted_in]->() RETURN count(r);
```

```
                                       QUERY PLAN
-----------------------------------------------------------------------------------------
 Aggregate
   ->  Seq Scan on acted_in r
         Filter: ((start >= '4.0'::graphid) AND (start <= '4.281474976710655'::graphid))
```

Without it, the same query joins three relations and scans the whole vertex hierarchy for the
endpoint it will not look at:

```cypher
SET enable_graph_endpoint_elision = off;
EXPLAIN (COSTS OFF) MATCH (p:person)-[r:acted_in]->() RETURN count(r);
```

```
                                             QUERY PLAN
-----------------------------------------------------------------------------------------------------
 Aggregate
   ->  Hash Join
         Hash Cond: (r."end" = "<0000000001>".id)
         ->  Hash Join
               Hash Cond: (r.start = p.id)
               ->  Seq Scan on acted_in r
                     Filter: ((start >= '4.0'::graphid) AND (start <= '4.281474976710655'::graphid))
               ->  Hash
                     ->  Seq Scan on person p
         ->  Hash
               ->  Append
                     ->  Seq Scan on ag_vertex "<0000000001>_1"
                     ->  Seq Scan on movie "<0000000001>_2"
                     ->  Seq Scan on person "<0000000001>_3"
```

```sql
RESET enable_graph_endpoint_elision;
```

This is the only one of the eleven that `EXPLAIN (SETTINGS)` reports, so a plan taken from a
session that changed it says so. Turn it off only to compare plans.

## enable_multiple_update {#enable_multiple_update}

```
bool · default on · context user
```

Decides whether writing the same element more than once in one statement is silent or warned
about.

A statement whose pattern matches an element several times writes it once per match. On, that
happens quietly. Off, the server warns for each repeat. The write still happens, so this is a
diagnostic rather than a restriction:

```cypher
CREATE GRAPH repeats;
SET graph_path = repeats;
CREATE VLABEL t;
CREATE (:t {n: 0}), (:t {n: 0});
MATCH (a:t) MATCH (b:t) SET b.n = b.n + 1 RETURN count(b) AS rows;
MATCH (n:t) RETURN n ORDER BY id(n);
```

```
 rows
------
 4
```

```
       n
----------------
 t[3.1]{"n": 1}
 t[3.2]{"n": 1}
```

The cross join produced four rows and each vertex was reached twice, but `n` went up by one.
With the setting off, the same statement says so:

```cypher
SET enable_multiple_update = off;
MATCH (a:t) MATCH (b:t) SET b.n = b.n + 1 RETURN count(b) AS rows;
```

```
WARNING:  graph element(3,1) has been SET multiple times
WARNING:  graph element(3,2) has been SET multiple times
 rows
------
 4
```

```cypher
RESET enable_multiple_update;
DROP GRAPH repeats CASCADE;
SET graph_path = moviekb;
```

Turn it off while you are working out why a `SET` did not do what you expected. A repeated
write is usually a sign that the pattern matches more than you meant. The warning names the
label id and local id, which is the element's `graphid`.

## enable_property_promotion {#enable_property_promotion}

```
bool · default on · context user
```

Decides whether a Cypher property read is answered from a promoted typed column when one
exists.

A property can be materialised as a real column of a real type; see [Promoting a property to
a column](/agensgraph/querying/typed-columns/). On, `n.key` reads that column and comes back in the
column's type. Off, every read goes to the `jsonb` bag and comes back as `jsonb`:

```cypher
CREATE GRAPH promoted;
SET graph_path = promoted;
CREATE VLABEL item (score int GENERATED);
CREATE (:item {score: 3}), (:item {score: 20}), (:item {score: 100});
MATCH (n:item) RETURN n.score AS score, pg_typeof(n.score) AS type ORDER BY n.score;
```

```
 score |   type
-------+-----------
     3 | "integer"
    20 | "integer"
   100 | "integer"
```

```cypher
SET enable_property_promotion = off;
MATCH (n:item) RETURN n.score AS score, pg_typeof(n.score) AS type ORDER BY n.score;
```

```
 score |  type
-------+---------
 3     | "jsonb"
 20    | "jsonb"
 100   | "jsonb"
```

> [!WARNING]
> Unlike the cost-only planner toggles, turning this off can change query **results**. A
> resolved `n.key` uses the typed column's native semantics — numeric or collation ordering, and
> type-aware comparison — while the `jsonb` fallback uses `jsonb` ordering and comparison. A
> sort, a range predicate or a comparison across types can come out differently.

```cypher
RESET enable_property_promotion;
DROP GRAPH promoted CASCADE;
SET graph_path = moviekb;
```

Leave it on. Turn it off to establish whether a promoted column changed a query's answer. Then
turn it back on and fix the query or the column instead.

## See also {#see-also}

- [Configuration](/agensgraph/operations/configuration/) — where a setting can be set, and the
  PostgreSQL settings that matter for a graph workload
- [Syntax](/agensgraph/reference/syntax/) — the lexical rules `graph_path`'s value follows
- [Data types](/agensgraph/reference/types/) — what `allow_null_properties` and `enable_property_promotion` change
  about a property's type
- [Graph metadata](/agensgraph/system-catalogs/graph-metadata/) — the table
  `auto_gather_graphmeta` maintains
- [Server-side tools](/agensgraph/operations/tools/) — `pg_dump`, `pg_upgrade` and the settings they
  rely on
- [PostgreSQL: server configuration](https://www.postgresql.org/docs/18/runtime-config.html) —
  every other setting
