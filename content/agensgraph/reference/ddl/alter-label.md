---
title: ALTER VLABEL and ALTER ELABEL
linkTitle: ALTER VLABEL and ALTER ELABEL
description: Renames a label, changes its storage, attaches or detaches a parent, turns its indexes off, or adds
  and removes promoted typed columns.
type: docs
weight: 50
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/ddl/alter-label.html
upstream_source: agensgraph
upstream_modified: true
---


Renames a label, changes its storage, attaches or detaches a parent, turns its indexes off,
or adds and removes promoted typed columns.

## Synopsis {#synopsis}

```text
ALTER VLABEL [ IF EXISTS ] label_name action [, ... ]ALTER VLABEL [ IF EXISTS ] label_name RENAME TO new_label_nameALTER ELABEL [ IF EXISTS ] label_name action [, ... ]ALTER ELABEL [ IF EXISTS ] label_name RENAME TO new_label_namewhere action is one of:    ADD [ COLUMN ] promoted_property    DROP [ COLUMN ] column_name [ CASCADE | RESTRICT ]    DISABLE INDEX    SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN }    SET TABLESPACE tablespace_name    SET { LOGGED | UNLOGGED }    CLUSTER ON index_name    SET WITHOUT CLUSTER    INHERIT parent_label    NO INHERIT parent_label    REPLICA IDENTITY { DEFAULT | USING INDEX index_name | FULL | NOTHING }    OWNER TO role_specification
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`ALTER VLABEL` acts on a vertex label and `ALTER ELABEL` on an edge label. Apart from the
keyword, the two statements are the same: **every action listed above is accepted on both
kinds.** The difference is what each kind of label has for an action to act on.

- The indexes a label is created with differ: a vertex label gets a primary key on `id`, an
  edge label gets btree indexes on `(start, "end")` and `("end", start)` plus a BRIN index
  on `id`. `DISABLE INDEX` invalidates all of a label's indexes either way, so it has one to
  invalidate on a new vertex label and three on a new edge label. `CLUSTER ON` also has
  different names to choose from.
- The structural columns that `DROP COLUMN` refuses are `id` and `properties` on a vertex
  label, plus `start` and `end` on an edge label.
- `INHERIT` and `NO INHERIT` require a parent of the same kind as the label, and in the same
  graph.

The label is looked up in the graph named by `graph_path`; the name cannot be qualified.

- `RENAME TO` is its own form. It cannot be combined with any other action, and a list of
  several actions cannot contain it.
- Several actions in one statement are separated by commas and applied in order.
- The base labels `ag_vertex` and `ag_edge` cannot be altered at all.
- `ALTER VLABEL` refuses an edge label and `ALTER ELABEL` refuses a vertex label.

Reshaping a label with `ALTER TABLE` instead is refused unless `enable_graph_ddl` is on.
The graph catalog describes a label's columns, and `ALTER TABLE` does not update it.
[How a graph is stored](/agensgraph/concepts/graph-on-postgresql/#what-is-deliberately-closed-off)
covers that gate.

## Parameters {#parameters}

IF EXISTS
: Issue a notice instead of an error when the label does not exist.

label_name
: Label to alter, in the graph named by `graph_path`.

RENAME TO new_label_name
: Give the label a new name. Vertices and edges keep their ids, so `label()` reports the new
  name for rows created before the rename. The table's sequence and indexes keep the names
  they were given, so check those before you write `CLUSTER ON`.

ADD [ COLUMN ] promoted_property
: Add a promoted typed column and backfill it from the existing rows. `promoted_property`
  takes the same three forms as in [`CREATE VLABEL`](/agensgraph/reference/ddl/create-vlabel/#promoted-properties),
  under the same restrictions. A property already promoted on the label is refused, as is
  promoting the same key twice in one statement.

DROP [ COLUMN ] column_name [ CASCADE | RESTRICT ]
: Drop a column and, for a promoted property, forget its mapping. A structural column of the
  label is refused. Indexes built on the dropped column go with it.

DISABLE INDEX
: Mark every index on the label invalid, so that a bulk load does not maintain them. Reads
  and writes keep working and the planner ignores an invalid index. There is no
  `ENABLE INDEX`; the way back is [`REINDEX VLABEL`](/agensgraph/reference/ddl/reindex/).

SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN }
: Set the storage mode of the label's `properties` column. The mode decides whether a large
  property map is held inline or in the table's TOAST relation, and whether it is compressed.
  A label starts with `EXTENDED`, which is out of line and compressed. The statement changes
  the strategy for future writes; it does not rewrite what is already stored.

SET TABLESPACE tablespace_name
: Move the label's table to another tablespace. Its indexes stay where they are.

SET { LOGGED | UNLOGGED }
: Turn write-ahead logging for the label's table on or off. The label's id sequence changes
  persistence with it.

CLUSTER ON index_name
: Record an index as the one a later `CLUSTER` should use. It does not reorder anything now.

SET WITHOUT CLUSTER
: Forget that record.

INHERIT parent_label
: Add the label as a child of another label of the same kind in the same graph, so that a
  pattern on the parent starts matching this label's rows.

NO INHERIT parent_label
: Remove that relationship.

REPLICA IDENTITY { DEFAULT | USING INDEX index_name | FULL | NOTHING }
: Choose which old values a write writes to the WAL to identify a row, for logical
  replication.

OWNER TO role_specification
: Give the label to another role. Write a role name, `CURRENT_ROLE`, `CURRENT_USER` or
  `SESSION_USER`.

## Examples {#examples}

The examples build their own graph, `catalogue`, rather than using
[the example dataset](/agensgraph/get-started/example-dataset/), and drop it at the end.

```cypher
CREATE GRAPH catalogue;
SET graph_path = catalogue;
CREATE VLABEL film;
CREATE (:film {title: 'Arrival', year: 2016}), (:film {title: 'Dune', year: 2021});
```

### Rename a label {#rename-a-label}

```cypher
ALTER VLABEL film RENAME TO movie;
```

```psql
\dGl catalogue.mov*
```

```
           List of labels
   Graph   | Name  |  Type  | Owner
-----------+-------+--------+-------
 catalogue | movie | vertex | agens
(1 row)
```

The rows came with it:

```cypher
MATCH (m:movie) RETURN count(m) AS movies;
```

```
 movies 
--------
 2
(1 row)
```

The sequence and the primary key still carry the old name:

```psql
\d catalogue.movie
```

```
                                                          Table "catalogue.movie"
   Column   |  Type   | Collation | Nullable |                                           Default                                            
------------+---------+-----------+----------+----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('catalogue.movie'::cstring), nextval('catalogue.film_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "film_pkey" PRIMARY KEY, btree (id)
Inherits: catalogue.ag_vertex
```

So `ALTER VLABEL movie CLUSTER ON movie_pkey` fails with
`index "movie_pkey" for table "movie" does not exist`, and the name to write is `film_pkey`.

### Turn a label's indexes off for a bulk load {#turn-a-labels-indexes-off-for-a-bulk-load}

```cypher
ALTER VLABEL movie DISABLE INDEX;
```

```psql
\d catalogue.movie
```

```
                                                          Table "catalogue.movie"
   Column   |  Type   | Collation | Nullable |                                           Default                                            
------------+---------+-----------+----------+----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('catalogue.movie'::cstring), nextval('catalogue.film_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "film_pkey" PRIMARY KEY, btree (id) INVALID
Inherits: catalogue.ag_vertex
```

Load the rows, then build the indexes again:

```cypher
REINDEX VLABEL movie;
```

```
REINDEX
```

### Promote a property on a label that already holds rows {#promote-a-property-on-a-label-that-already-holds-rows}

```cypher
ALTER VLABEL movie ADD COLUMN year int GENERATED;
```

```psql
\d catalogue.movie
```

```
                                                           Table "catalogue.movie"
   Column   |  Type   | Collation | Nullable |                                            Default                                            
------------+---------+-----------+----------+-----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('catalogue.movie'::cstring), nextval('catalogue.film_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
 year       | integer |           |          | generated always as (ag_property_text(properties, 'year'::text, 'n'::"char")::integer) stored
Indexes:
    "film_pkey" PRIMARY KEY, btree (id)
Inherits: catalogue.ag_vertex
```

The existing rows are backfilled, so the column is complete the moment the statement returns:

```sql
SELECT year FROM catalogue.movie ORDER BY year;
```

```
 year 
------
 2016
 2021
(2 rows)
```

### Look up what a label promotes {#look-up-what-a-label-promotes}

`ag_label_property` maps a property key to the column that answers for it:

```cypher
ALTER VLABEL movie ADD COLUMN released text GENERATED (releaseDate);
```

```sql
SELECT p.propname, p.attnum FROM pg_catalog.ag_label_property p
  JOIN pg_catalog.ag_label l ON l.oid = p.laboid
  JOIN pg_catalog.ag_graph g ON g.oid = l.graphid
 WHERE g.graphname = 'catalogue' AND l.labname = 'movie' ORDER BY p.attnum;
```

```
  propname   | attnum 
-------------+--------
 year        |      3
 releasedate |      4
(2 rows)
```

`attnum` is the column's position in the table. Join the query to `pg_attribute` on it when
you want the column name as well. The two differ whenever the explicit-key form was used.

### Drop a promoted column {#drop-a-promoted-column}

```cypher
ALTER VLABEL movie DROP COLUMN released;
```

The mapping goes with the column:

```sql
SELECT p.propname, p.attnum FROM pg_catalog.ag_label_property p
  JOIN pg_catalog.ag_label l ON l.oid = p.laboid
  JOIN pg_catalog.ag_graph g ON g.oid = l.graphid
 WHERE g.graphname = 'catalogue' AND l.labname = 'movie' ORDER BY p.attnum;
```

```
 propname | attnum 
----------+--------
 year     |      3
(1 row)
```

Reads of `releasedate` go back to the property bag; nothing was deleted from it.

### Change how the property map is stored {#change-how-the-property-map-is-stored}

```cypher
ALTER VLABEL movie SET STORAGE external;
```

The mode is set on `properties`, whichever column you might have expected:

```sql
SELECT attname, attstorage FROM pg_attribute
 WHERE attrelid = 'catalogue.movie'::regclass AND attnum > 0 AND NOT attisdropped;
```

```
  attname   | attstorage 
------------+------------
 id         | p
 properties | e
 year       | p
(3 rows)
```

### Attach and detach a parent {#attach-and-detach-a-parent}

```cypher
CREATE VLABEL work;
ALTER VLABEL movie INHERIT work;
```

```psql
\dGv catalogue.movie
```

```
           List of labels
   Graph   | Name  |  Type  | Owner
-----------+-------+--------+-------
 catalogue | movie | vertex | agens
(1 row)

Vertex label "catalogue.movie"
--
Inherits: catalogue.ag_vertex,
          catalogue.work
```

`movie` now has two parents: the base label it started with, and `work`. Detaching leaves
the base label alone:

```cypher
ALTER VLABEL movie NO INHERIT work;
```

```
ALTER VLABEL
```

### Refusals worth recognizing {#refusals-worth-recognizing}

A structural column cannot be dropped:

```cypher
ALTER VLABEL movie DROP COLUMN properties;
```

```
ERROR:  cannot drop column "properties" of graph label "movie"
HINT:  It is a structural column of the graph label.
```

An added column has to be generated from the bag:

```cypher
ALTER VLABEL movie ADD COLUMN rank int;
```

```
ERROR:  a non-generated promoted column is not supported yet
HINT:  Use GENERATED to mirror the property from the jsonb bag.
```

A property already promoted cannot be promoted a second time:

```cypher
ALTER VLABEL movie ADD COLUMN yr2 int GENERATED (year);
```

```
ERROR:  property "year" is already promoted on graph label "movie"
HINT:  Drop the existing promoted column first, or promote the property to a different column name.
```

The base labels are off limits, as parents and as targets:

```cypher
ALTER VLABEL movie INHERIT ag_vertex;
```

```
ERROR:  cannot ALTER inheritance with base label
```

```cypher
ALTER VLABEL ag_vertex SET STORAGE main;
```

```
ERROR:  ALTER base vertex label is prohibited
```

Each statement acts on one kind of label:

```cypher
CREATE ELABEL directed;
ALTER VLABEL directed RENAME TO helmed;
```

```
ERROR:  RENAME VLABEL cannot RENAME edge label
```

And `RENAME TO` stands alone:

```cypher
ALTER VLABEL movie RENAME TO film, SET STORAGE main;
```

```
ERROR:  syntax error at or near ","
LINE 1: ALTER VLABEL movie RENAME TO film, SET STORAGE main;
                                         ^
```

Reshaping the label's table with SQL is refused while `enable_graph_ddl` is off:

```sql
ALTER TABLE catalogue.movie ADD COLUMN rank int;
```

```
ERROR:  cannot add a column to graph label "movie" with ALTER TABLE
HINT:  Use ALTER VLABEL or ALTER ELABEL instead, which keeps the graph catalog in step.
```

Finally, drop the graph the examples built:

```cypher
DROP GRAPH catalogue CASCADE;
```

## Notes {#notes}

`SET STORAGE` takes four keywords, not five. `DEFAULT` is reserved and is a syntax error
here. To go back to the mode a label starts with, write `SET STORAGE extended`. An
unrecognized word is reported as `invalid storage type "..."`.

The `IF EXISTS` notice differs between the two forms: `label "nosuch" does not exist,
skipping` from `RENAME TO`, and `graph label "nosuch" does not exist, skipping` from an
action list. Both then report success and do nothing.

## Compatibility {#compatibility}

### ISO/IEC 39075 (GQL) {#isoiec-39075-gql}

GQL has no statement that alters a label, because it has no labels to alter. An element
type belongs to a graph type, and a graph type is created and dropped whole
(`<create graph type statement>`, §12.6). Nothing in GQL corresponds to renaming a label,
promoting a property, or turning an index off. Graph types are tracked as planned in the
[GQL conformance matrix](/agensgraph/appendix/gql-conformance/).

### PostgreSQL {#postgresql}

Every action here is an `ALTER TABLE` action, and each one means what it means there, with
two adjustments. `SET STORAGE` names no column. The only column whose storage is worth
choosing is `properties`, and the mode is applied to that one. `DISABLE INDEX` has no
`ALTER TABLE` counterpart at all: it marks the label's indexes invalid, which SQL can
otherwise only do by interrupting `CREATE INDEX CONCURRENTLY`.

Going the other way, `ALTER TABLE` on a label's table is refused for the actions that would
reshape it, unless `enable_graph_ddl` is on. Adding, dropping or retyping a column is such
an action. The example above shows the refusal. The actions on this page never need that
setting, because they update the graph catalog themselves.

## See also {#see-also}

- [`CREATE VLABEL`](/agensgraph/reference/ddl/create-vlabel/)
- [`CREATE ELABEL`](/agensgraph/reference/ddl/create-elabel/)
- [`DROP VLABEL` and `DROP ELABEL`](/agensgraph/reference/ddl/drop-label/)
- [`REINDEX VLABEL` and `REINDEX ELABEL`](/agensgraph/reference/ddl/reindex/)
- [Promoting a property to a column](/agensgraph/querying/typed-columns/)
- [Label inheritance](/agensgraph/concepts/label-inheritance/)
