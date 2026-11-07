---
title: Loading data
linkTitle: Loading data
description: There are three ways to get data into a graph, and the right one depends on how much data there is.
type: docs
weight: 10
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/guides/loading-data.html
upstream_source: agensgraph
upstream_modified: true
---


There are three ways to get data into a graph, and the right one depends on how much data
there is.

| Route | Good for | Speed |
| --- | --- | --- |
| Cypher `CREATE` / `MERGE` | Up to a few hundred thousand elements; anything where you want Cypher's checks | Slowest per row, safest |
| `LOAD FROM` a table | Data already in a table, or in a file exposed as a foreign table | Fast, and stays inside Cypher |
| `COPY` into the label tables | Millions of elements, from files you control | Fastest by a wide margin |

Whichever you use, the section on [indexes during a bulk
load](#indexes-during-a-bulk-load) applies, and so does the [after the
load](#after-the-load) checklist. Skipping the second one is the usual reason a freshly
loaded graph queries badly.

## Cypher CREATE {#cypher-create}

The obvious route, and the one to use until it is too slow. Batch it: one statement creating
many elements beats many statements creating one:

```cypher
CREATE (:person {name: 'Ann', born: 1990}),
       (:person {name: 'Bo',  born: 1985}),
       (:person {name: 'Cy',  born: 1979});
```

Edges need both endpoints found first, so match them in the same statement:

```cypher
MATCH (a:person {name: 'Ann'}), (b:person {name: 'Bo'})
CREATE (a)-[:knows {since: 2019}]->(b);
```

Loading edges one `MATCH` at a time is the reason this route is slow: each statement re-finds
its endpoints. If you are loading edges in bulk, use one of the other two routes and let the
server do the lookup as a join.

`MERGE` instead of `CREATE` when the load may run twice and you want it to be idempotent, but
be aware it costs a lookup per element.

## LOAD FROM a table {#load-from-a-table}

`LOAD FROM` reads rows from an ordinary table and hands them to a Cypher write clause, so the
endpoint lookup becomes a single join rather than one query per row. It is the natural route
when the data is already relational. That includes a file, once `file_fdw` has exposed it
as a foreign table.

Say the rows have already landed in two staging tables:

```sql
CREATE TABLE staging_people (name text, born int);
INSERT INTO staging_people VALUES ('Ann', 1990), ('Bo', 1985);

CREATE TABLE staging_knows (from_name text, to_name text, since int);
INSERT INTO staging_knows VALUES ('Ann', 'Bo', 2019);
```

Then one statement turns each row into a vertex:

```cypher
LOAD FROM staging_people AS row
CREATE (:person {name: row.name, born: row.born});
```

Or take the whole row as the property map:

```cypher
LOAD FROM staging_people AS row
CREATE (:person = to_jsonb(row_to_json(row)));
```

Edges are the case that matters, because the join is where the speed comes from:

```cypher
LOAD FROM staging_knows AS row
MATCH (a:person {name: row.from_name}), (b:person {name: row.to_name})
CREATE (a)-[:knows {since: row.since}]->(b);
```

Index the properties you match on before running that; see below.

### Reading a file as a table {#reading-a-file-as-a-table}

`file_fdw` turns a file on the server's filesystem into a read-only table. It is a contrib
module, so it needs `make install-world` at build time (see [Install
AgensGraph](/agensgraph/get-started/install/#build-and-install)):

> [!NOTE]
> The two blocks below need `file_fdw`, so they are the one part of this page you cannot run
> without having built the contrib modules.

<!-- check-examples: skip-next needs the file_fdw contrib module -->
```sql
CREATE EXTENSION file_fdw;
CREATE SERVER import FOREIGN DATA WRAPPER file_fdw;

CREATE FOREIGN TABLE staging_people (name text, born int)
SERVER import
OPTIONS (filename '/data/people.csv', format 'csv', header 'true');
```

Then `LOAD FROM staging_people AS row …` as above. The file is read on the server, so the
path is a server path and the server's user must be able to read it.

If the file is on your machine rather than the server's, load it into an ordinary table with
`\copy` in [the agens client](/agensgraph/reference/agens/) first, and `LOAD FROM` that.

## COPY into the label tables {#copy-into-the-label-tables}

The fastest route, and the one to use for millions of elements. [A label is a
table](/agensgraph/concepts/graph-on-postgresql/), so you can `COPY` straight into it. You are
writing the `properties` column directly and letting the `id` column default fill itself in.

Writing to a label with SQL is gated, so turn the gate on for the load:

```psql
SET enable_graph_dml = on;

COPY moviekb.person (properties) FROM STDIN;
{"name": "Ann", "born": 1990}
{"name": "Bo", "born": 1985}
\.
```

For edges, supply the two endpoint ids as well, in `labid.locid` form:

```psql
SET enable_graph_dml = on;

COPY moviekb.acted_in (start, "end", properties) FROM STDIN;
4.1	3.1	{"role": "Neo"}
4.2	3.1	{"role": "Trinity"}
\.
```

So the work is in producing those ids. Two ways:

**Build them arithmetically.** If you control the numbering, `graphid()` composes an id from
a label id and a local id:

```sql
SELECT graphid(graph_labid('moviekb.person'::cstring), 100::int8);
```

```
 made_id
---------
 4.100
```

So a loader that assigns row numbers can emit both vertex ids and the edge endpoints
referring to them, with no lookup at all. This is the fastest possible load.

**Or resolve them with a join.** Load the vertices first, then build the edge rows from a
staging table by joining on the business key:

```sql
CREATE TABLE staging_roles (person_name text, movie_title text, role text);
INSERT INTO staging_roles VALUES ('Keanu Reeves', 'The Matrix', 'Neo (again)');

SET enable_graph_dml = on;

INSERT INTO moviekb.acted_in (start, "end", properties)
SELECT p.id, m.id, jsonb_build_object('role', s.role)
FROM staging_roles s
  JOIN moviekb.person p ON p.properties->>'name'  = s.person_name
  JOIN moviekb.movie  m ON m.properties->>'title' = s.movie_title;
```

That is one set-based statement rather than a query per edge, which is the whole point.
Index the keys you join on first.

```sql
DROP TABLE staging_roles;
```

> [!WARNING]
> `COPY` and `INSERT` bypass the checks Cypher performs. Nothing stops you writing an edge
> whose `start` names a vertex that does not exist, and the result is a graph that no query can
> traverse correctly. Verify the endpoints before you load, and turn `enable_graph_dml` off
> again afterwards.

## Indexes during a bulk load {#indexes-during-a-bulk-load}

Maintaining an index while millions of rows arrive is expensive. A label can be created with
its indexes switched off:

```cypher
CREATE VLABEL bulk_person DISABLE INDEX;
```

or switched off later:

```cypher
ALTER VLABEL bulk_person DISABLE INDEX;
```

Load the data, then rebuild:

```cypher
REINDEX VLABEL bulk_person;
```

> [!NOTE]
> There is no `ENABLE INDEX`. `ALTER VLABEL person ENABLE INDEX` is a syntax error; `REINDEX`
> is what brings the indexes back. Until you run it, the label's indexes exist but are not
> usable, so queries will fall back to sequential scans and any unique constraint is not being
> enforced.

Two more things that help a large load:

**Create the property indexes after the data, not before** — building an index once over a
full label is much cheaper than maintaining it row by row. The same goes for [promoting a
property to a column](/agensgraph/querying/typed-columns/): the `ALTER` rewrites the whole label, so
promote once after the load rather than before it.

**Consider an unlogged label** for data you can reload. It skips the WAL entirely:

```cypher
CREATE UNLOGGED VLABEL staging_person;
```

An unlogged label does not survive a crash and is not replicated. So this is for staging and
for graphs you can rebuild, not for the final data.

Raise `maintenance_work_mem` before the reindex; it is used by one command at a time, so a
large temporary value is safe. See [Configuration](/agensgraph/operations/configuration/#memory).

## After the load {#after-the-load}

Three steps, none optional.

**Rebuild the indexes** if you disabled them, as above.

**Promote the properties you filter and sort on**, if you are going to. `ALTER VLABEL person
ADD COLUMN age int GENERATED` gives the property `age` a real `int` column beside the jsonb
bag, filled at write time, and an index over it is a plain column index. The property key is
what a query keeps naming — `p.age` still reads `age`, and the column name never appears in
Cypher. Use `GENERATED (sourceKey)` when the column should be named differently from the key.
See [Promoting a property to a column](/agensgraph/querying/typed-columns/).

**Analyze.** The planner has no statistics for a freshly loaded label, and a graph traversal
plan is very sensitive to them:

```sql
ANALYZE moviekb.person;
ANALYZE moviekb.acted_in;
```

**Gather the graph metadata.** `ag_graphmeta` records which start-label, edge-label,
end-label triples occur in the graph and how many edges make up each. That lets the planner
prune scans of labels a pattern cannot reach:

```cypher
SELECT regather_graphmeta();
```

```sql
SELECT graphname, graphmeta_valid FROM pg_catalog.ag_graph;
```

Then check the shape of what you loaded, which is also the quickest way to catch a load that
went wrong:

```sql
SELECT * FROM pg_catalog.ag_graphmeta_view WHERE graphname = 'moviekb';
```

```
 graphname | start  |    edge    |  end  | edgecount
-----------+--------+------------+-------+-----------
 moviekb   | movie  | related_to | movie |        11
 moviekb   | person | directed   | movie |        21
 moviekb   | person | acted_in   | movie |        25
```

An edge shape you did not expect, or a count that is a multiple of what it should be, shows up
here immediately.

Clean up the staging tables and the scratch label when the load is done:

```sql
DROP TABLE staging_people, staging_knows;
```

```cypher
DROP VLABEL bulk_person;
DROP VLABEL IF EXISTS staging_person;
```

## Exporting {#exporting}

`pg_dump` covers a graph, and naming the schema exports one graph. See
[Backup and recovery](/agensgraph/operations/backup/). For data rather than structure, `COPY … TO`
works on a label table, and a Cypher query wrapped in SQL exports exactly the shape you want:

```psql
\copy (SELECT p.properties->>'name' AS name, m.properties->>'title' AS film
       FROM moviekb.acted_in r
         JOIN moviekb.person p ON p.id = r.start
         JOIN moviekb.movie  m ON m.id = r."end") TO 'roles.csv' CSV HEADER
```
