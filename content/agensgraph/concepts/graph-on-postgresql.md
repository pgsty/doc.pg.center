---
title: How a graph is stored
linkTitle: How a graph is stored
description: AgensGraph does not bolt a graph engine onto PostgreSQL.
type: docs
weight: 20
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/concepts/graph-on-postgresql.html
upstream_source: agensgraph
upstream_modified: true
---


AgensGraph does not bolt a graph engine onto PostgreSQL. It stores a graph *as* PostgreSQL
objects, using the schemas, tables, indexes and inheritance that are already there. Once you
know the mapping, most of what you know about running PostgreSQL applies unchanged. It also
stops being surprising that one statement can mix Cypher with SQL: there is only ever one set
of tables.

The mapping is three sentences long.

**A graph is a schema.** `CREATE GRAPH moviekb` creates a schema named `moviekb`.

**A label is a table.** `CREATE VLABEL movie` creates a table `moviekb.movie`.

**A vertex or an edge is a row** in that table.

## What a label table looks like {#what-a-label-table-looks-like}

A vertex label has two columns:

```psql
\d moviekb.movie
```

```
                                              Table "moviekb.movie"
   Column   |  Type   | Nullable |                                   Default
------------+---------+----------+-------------------------------------------------------------------------
 id         | graphid | not null | graphid(graph_labid('moviekb.movie'::cstring), nextval('moviekb.movie_id_seq'))
 properties | jsonb   | not null | jsonb_build_object()
Indexes:
    "movie_pkey" PRIMARY KEY, btree (id)
Inherits: moviekb.ag_vertex
```

An edge label has the same two columns plus the ids of its endpoints:

```psql
\d moviekb.acted_in
```

```
                                              Table "moviekb.acted_in"
   Column   |  Type   | Nullable |                                     Default
------------+---------+----------+---------------------------------------------------------------------------
 id         | graphid | not null | graphid(graph_labid('moviekb.acted_in'::cstring), nextval('moviekb.acted_in_id_seq'))
 start      | graphid | not null |
 end        | graphid | not null |
 properties | jsonb   | not null | jsonb_build_object()
Indexes:
    "acted_in_end_idx" btree ("end", start)
    "acted_in_id_idx" brin (id)
    "acted_in_start_idx" btree (start, "end")
Inherits: moviekb.ag_edge
```

A label can carry more than those columns. [Promoting a
property](/agensgraph/querying/typed-columns/) adds a real typed column beside the bag, filled at
write time. A hot property is then stored twice: once as a jsonb key, and once as a column the
planner can index and compare natively. The catalog `ag_label_property` records which property
key answers from which column. Cypher keeps naming the key, so the column name never appears
in a query.

So an edge is a row that names two vertices, and traversing an edge is a join on `graphid`.
The two btree indexes on `(start, "end")` and `("end", start)` are what make that join fast
in either direction, and AgensGraph creates them for you when you create the label. The BRIN
index on `id` is small and helps range scans over a label's ids.

Note which indexes each kind of label gets. A vertex label has a primary key on `id`; an
edge label does not, because edges are reached through their endpoints rather than by id.

Because `properties` is a single `jsonb` column, a label imposes no column list on its rows.
Two `movie` vertices may carry entirely different keys. That is what "schemaless properties"
means here. It is also why reading a property means reading into a JSON document.
[Promoting a property to a column](/agensgraph/querying/typed-columns/) covers when that cost
matters and what to do about it.

## Identity: the graphid {#identity-the-graphid}

`graphid` is a 64-bit identifier with two parts. The top 16 bits are the *label id*; the
low 48 bits are the *local id*, a per-label sequence. It prints as `labid.locid`:

```sql
SELECT id, graphid_labid(id) AS labid, graphid_locid(id) AS locid
FROM moviekb.movie ORDER BY id LIMIT 3;
```

```
 id  | labid | locid
-----+-------+-------
 3.1 |     3 |     1
 3.2 |     3 |     2
 3.3 |     3 |     3
```

That layout has two consequences, and both matter.

First, an id carries its own label. Nothing has to be looked up to know which table a vertex
came from.

Second, the label id is the *high* bits, so all the ids of one label form a single contiguous
range of `graphid` values. A plain btree index on `id` can therefore answer "is this vertex a
`movie`?" without touching the `movie` table at all.

The label ids themselves live in `ag_label`:

```sql
SELECT labname, labid, labkind FROM pg_catalog.ag_label
WHERE graphid = (SELECT oid FROM pg_catalog.ag_graph WHERE graphname = 'moviekb')
ORDER BY labid;
```

```
  labname   | labid | labkind
------------+-------+---------
 ag_vertex  |     1 | v
 ag_edge    |     2 | e
 movie      |     3 | v
 person     |     4 | v
 acted_in   |     5 | e
 directed   |     6 | e
 related_to |     7 | e
```

`labid` is 16 bits and 0 is not a valid label, so a database holds at most 65,535 labels.
A single label holds at most 2<sup>48</sup> − 1 rows. See [Limits](/agensgraph/appendix/limits/).

## Every graph has two labels you did not create {#every-graph-has-two-labels-you-did-not-create}

`ag_vertex` and `ag_edge` are created with the graph, and every label you create inherits
from one of them:

```sql
SELECT c.relname AS child, p.relname AS parent
FROM pg_inherits i
  JOIN pg_class c ON c.oid = i.inhrelid
  JOIN pg_class p ON p.oid = i.inhparent
  JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'moviekb' ORDER BY 1;
```

```
   child    |  parent
------------+-----------
 acted_in   | ag_edge
 directed   | ag_edge
 movie      | ag_vertex
 person     | ag_vertex
 related_to | ag_edge
```

That inheritance is what gives an unlabelled pattern its meaning. `MATCH (n)` does not scan
a special index of everything; it scans `ag_vertex` and, through inheritance, every table
below it:

```cypher
EXPLAIN (COSTS OFF) MATCH (n) RETURN n;
```

```
              QUERY PLAN
---------------------------------------
 Result
   ->  Append
         ->  Seq Scan on ag_vertex n_1
         ->  Seq Scan on movie n_2
         ->  Seq Scan on person n_3
```

Naming a label narrows the scan to that table and its children, and the `ONLY` modifier
narrows it to exactly that table. [Label inheritance](/agensgraph/concepts/label-inheritance/) covers what you
can build with that.

## What a property index and a constraint become {#what-a-property-index-and-a-constraint-become}

A Cypher property index is a PostgreSQL expression index over the `properties` column:

```cypher
CREATE PROPERTY INDEX ON movie (title);
```

```psql
\d moviekb.movie
```

```
Indexes:
    "movie_pkey" PRIMARY KEY, btree (id)
    "movie_title_idx" btree ((properties.'title'))
```

A uniqueness constraint becomes an exclusion constraint over the same expression:

```cypher
CREATE CONSTRAINT movie_title_uq ON movie ASSERT title IS UNIQUE;
```

```
Indexes:
    "movie_title_uq" EXCLUDE USING btree ((properties.'title') WITH =)
```

The `properties.'title'` form in those definitions is how the Cypher parser writes a property
read. It is not syntax you type in SQL.

For tuning, the ordinary part is what matters. These are btree indexes over an expression.
The planner picks them by the usual rules, and they only help a predicate it can match
against that expression. [Indexes and
constraints](/agensgraph/querying/indexes-and-constraints/) covers which predicates qualify.

## What this buys you {#what-this-buys-you}

Everything PostgreSQL does to a table, it does to a label. That is not a slogan; it is the
list of things you do not have to learn twice:

* **Transactions.** A Cypher write and a SQL write in one transaction commit or roll back
  together, because they are writes to tables in the same database.
* **Access control.** `GRANT SELECT ON moviekb.movie TO analyst` works, and so does row-level
  security on a label. See [Security](/agensgraph/operations/security/).
* **Backup and replication.** `pg_dump`, `pg_basebackup`, WAL archiving and streaming
  replication treat a graph as what it is — schemas and tables.
* **Extensions.** `pgvector` stores an embedding next to a graph because a property is
  `jsonb` in a table an extension can index. That is the whole basis of the
  [vector search](/agensgraph/guides/search/vector/) guide.
* **The planner.** `EXPLAIN` on a Cypher query shows sequential scans, index scans and joins,
  and you tune them the way you tune any PostgreSQL query.

And it is why SQL and Cypher compose in one statement rather than needing a bridge:
[Combining SQL and Cypher](/agensgraph/querying/combining-sql-and-cypher/).

## What is deliberately closed off {#what-is-deliberately-closed-off}

The mapping is real, but it is not an invitation to edit a graph as if it were an ordinary
table. Two gates stand in the way, both off by default, because either operation can leave
the graph catalog describing something that is no longer true.

Writing rows directly is refused:

```psql
INSERT INTO moviekb.movie (properties) VALUES ('{"title": "x"}');
```

```
ERROR:  DML query to graph objects is not allowed
```

So is reshaping a label:

```sql
ALTER TABLE moviekb.movie ADD COLUMN foo int;
```

```
ERROR:  cannot add a column to graph label "movie" with ALTER TABLE
HINT:  Use ALTER VLABEL or ALTER ELABEL instead, which keeps the graph catalog in step.
```

`enable_graph_dml` and `enable_graph_ddl` open them respectively, and
[Server settings](/agensgraph/reference/guc/) says what you take on by doing so. Reading a label
with SQL needs no setting at all — every `SELECT` on this page runs as it stands.
