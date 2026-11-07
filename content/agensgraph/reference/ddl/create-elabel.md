---
title: CREATE ELABEL
linkTitle: CREATE ELABEL
description: Creates an edge label — a table of (id, start, end, properties) that inherits the graph's base edge
  label, optionally with properties promoted to typed columns.
type: docs
weight: 40
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/ddl/create-elabel.html
upstream_source: agensgraph
upstream_modified: true
---


Creates an edge label — a table of `(id, start, end, properties)` that inherits the graph's
base edge label, optionally with properties promoted to typed columns.

## Synopsis {#synopsis}

```text
CREATE [ UNLOGGED ] ELABEL [ IF NOT EXISTS ] label_name [ ( promoted_property [, ... ] ) ]    [ DISABLE INDEX ]    [ INHERITS ( parent_label [, ... ] ) ]    [ WITH ( storage_parameter [= value] [, ... ] ) ]    [ TABLESPACE tablespace_name ]CREATE [ UNLOGGED ] ELABEL ONLY label_name ( label_id ) [ option ... ]where promoted_property is one of:    column_name data_type GENERATED    column_name data_type GENERATED ( property_key )    column_name data_type GENERATED ALWAYS AS ( expression ) [ STORED ]
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

An edge label is a table with four columns: an `id` of type `graphid`, the `graphid` of the
edge's `start` and `end` vertices, and a `properties` column of type `jsonb`. It inherits the
graph's `ag_edge` unless you name a parent.

Creating one also creates the sequence that numbers its ids and three indexes. Two are btree
indexes, on `(start, "end")` and `("end", start)`, which make a traversal fast in either
direction. The third is a BRIN index on `id`. An edge label gets no primary key on `id`,
because edges are reached through their endpoints.
[How a graph is stored](/agensgraph/concepts/graph-on-postgresql/) covers that layout.

The label is created in the graph named by `graph_path`.

- **The options are position-sensitive.** They have to appear in the order shown:
  `DISABLE INDEX`, then `INHERITS`, then `WITH`, then `TABLESPACE`. Any other order is a
  syntax error.
- A parent named in `INHERITS` must be in the same graph and must be an edge label. Naming a
  vertex label is refused.
- `IF NOT EXISTS` and `ONLY` belong to separate forms and cannot be combined.
- An edge label puts no restriction on which labels its endpoints have. `start` and `end`
  are plain `graphid` columns, not foreign keys.
- Cypher creates a label on demand: `CREATE (a)-[:directed]->(b)` against a graph with no
  `directed` label creates one. Use `CREATE ELABEL` when you want options, promoted columns
  or a parent.

### Promoted properties {#promoted-properties}

A promoted property is a typed column beside the `properties` bag, computed from the bag and
stored. Reads of that property go to the column rather than into the JSON document.
The three forms and their restrictions are the same as for a vertex label, and
[`CREATE VLABEL`](/agensgraph/reference/ddl/create-vlabel/#promoted-properties) sets them out. On an edge label the
reserved column names are `id`, `properties`, `start` and `end`.

## Parameters {#parameters}

UNLOGGED
: Create the label's table as unlogged: its contents are not written to the write-ahead log
  and are lost after a crash.

IF NOT EXISTS
: Issue a notice instead of an error when a label of that name already exists. Nothing is
  created; the existing label's options are not changed.

label_name
: Name of the label to create, in the graph named by `graph_path`.

promoted_property
: A property to mirror into a typed column. Columns are added after `properties`, in the
  order written.

DISABLE INDEX
: Create the label's three indexes but leave them invalid, so that loading rows does not
  maintain them. Reads and writes still work; the planner ignores an invalid index. Rebuild
  with [`REINDEX ELABEL`](/agensgraph/reference/ddl/reindex/). There is no `ENABLE INDEX`.

INHERITS ( parent_label [, ...] )
: Parent labels, replacing the default parent `ag_edge`. Each must be an edge label in the
  same graph. See [Label inheritance](/agensgraph/concepts/label-inheritance/).

WITH ( storage_parameter [= value] [, ...] )
: Storage parameters for the label's table, as for `CREATE TABLE`.

TABLESPACE tablespace_name
: Tablespace for the label's table. Without it, `default_tablespace` decides.

ONLY label_name ( label_id )
: Create the label with the given label id and without the default parent, the id default or
  the endpoint indexes. This is the form `pg_dump` emits so that a restore preserves the ids
  in a dumped graph. Write it only when reproducing a dump.

## Examples {#examples}

The examples build their own graph, `castlists`, rather than using
[the example dataset](/agensgraph/get-started/example-dataset/), and drop it at the end.

### Create an edge label {#create-an-edge-label}

```cypher
CREATE GRAPH castlists;
SET graph_path = castlists;
CREATE VLABEL person;
CREATE VLABEL film;
CREATE ELABEL worked_on;
```

```
CREATE ELABEL
```

```psql
\d castlists.worked_on
```

```
                                                             Table "castlists.worked_on"
   Column   |  Type   | Collation | Nullable |                                                Default                                                
------------+---------+-----------+----------+-------------------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('castlists.worked_on'::cstring), nextval('castlists.worked_on_id_seq'::regclass))
 start      | graphid |           | not null | 
 end        | graphid |           | not null | 
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "worked_on_end_idx" btree ("end", start)
    "worked_on_id_idx" brin (id)
    "worked_on_start_idx" btree (start, "end")
Inherits: castlists.ag_edge
```

Creating the label also set the statistics target of `start` and `end` to 1000, because a
traversal's row estimate depends on how those two columns are distributed:

```sql
SELECT attname, attstattarget FROM pg_attribute
 WHERE attrelid = 'castlists.worked_on'::regclass AND attnum > 0;
```

```
  attname   | attstattarget 
------------+---------------
 id         |              
 start      |          1000
 end        |          1000
 properties |              
(4 rows)
```

### Group several edge types under one parent {#group-several-edge-types-under-one-parent}

```cypher
CREATE ELABEL acted_in INHERITS (worked_on);
CREATE ELABEL directed INHERITS (worked_on);
```

```psql
\dGe castlists.acted_in
```

```
           List of labels
   Graph   |   Name   | Type | Owner
-----------+----------+------+-------
 castlists | acted_in | edge | agens
(1 row)

Edge label "castlists.acted_in"
--
Inherits: castlists.worked_on
```

A pattern on the parent now matches either kind of edge, and `label()` still reports the one
the edge was created with:

```cypher
CREATE (:person {name: 'Denis Villeneuve'})-[:directed {credited: true}]->(:film {title: 'Arrival'});
MATCH (p)-[e:worked_on]->(f) RETURN label(e) AS type, e.credited AS credited;
```

```
    type    | credited 
------------+----------
 "directed" | true
(1 row)
```

### Create a label only if it is not there {#create-a-label-only-if-it-is-not-there}

```cypher
CREATE ELABEL IF NOT EXISTS acted_in;
```

```
NOTICE:  label "acted_in" already exists, skipping
CREATE ELABEL
```

### Load an edge label before building its indexes {#load-an-edge-label-before-building-its-indexes}

All three indexes are created invalid, and the table itself is unlogged:

```cypher
CREATE UNLOGGED ELABEL staged DISABLE INDEX WITH (fillfactor = 70) TABLESPACE pg_default;
```

```psql
\d castlists.staged
```

```
                                                       Unlogged table "castlists.staged"
   Column   |  Type   | Collation | Nullable |                                             Default                                             
------------+---------+-----------+----------+-------------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('castlists.staged'::cstring), nextval('castlists.staged_id_seq'::regclass))
 start      | graphid |           | not null | 
 end        | graphid |           | not null | 
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "staged_end_idx" btree ("end", start) INVALID
    "staged_id_idx" brin (id) INVALID
    "staged_start_idx" btree (start, "end") INVALID
Inherits: castlists.ag_edge
```

Load the edges, then run `REINDEX ELABEL staged` to build the three indexes.

### Promote an edge property to a typed column {#promote-an-edge-property-to-a-typed-column}

```cypher
CREATE ELABEL scored (rating numeric GENERATED, source text GENERATED (site));
```

```psql
\d castlists.scored
```

```
                                                           Table "castlists.scored"
   Column   |  Type   | Collation | Nullable |                                             Default                                             
------------+---------+-----------+----------+-------------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('castlists.scored'::cstring), nextval('castlists.scored_id_seq'::regclass))
 start      | graphid |           | not null | 
 end        | graphid |           | not null | 
 properties | jsonb   |           | not null | jsonb_build_object()
 rating     | numeric |           |          | generated always as (ag_property_text(properties, 'rating'::text, 'n'::"char")::numeric) stored
 source     | text    |           |          | generated always as (ag_property_text(properties, 'site'::text, 's'::"char")) stored
Indexes:
    "scored_end_idx" btree ("end", start)
    "scored_id_idx" brin (id)
    "scored_start_idx" btree (start, "end")
Inherits: castlists.ag_edge
```

Writing the edge fills both columns:

```cypher
MATCH (p:person), (f:film) CREATE (p)-[:scored {rating: 8.5, site: 'critics'}]->(f);
```

```
UPDATE 1
```

SQL reads them under the column names:

```sql
SELECT rating, source FROM castlists.scored;
```

```
 rating | source  
--------+---------
    8.5 | critics
(1 row)
```

Cypher reads them under the property keys, so the second one is `e.site`, not `e.source`:

```cypher
MATCH ()-[e:scored]->() RETURN e.rating AS rating, e.site AS site;
```

```
 rating |  site   
--------+---------
    8.5 | critics
(1 row)
```

### Refusals worth recognizing {#refusals-worth-recognizing}

An edge label can only inherit an edge label:

```cypher
CREATE ELABEL wrong INHERITS (person);
```

```
ERROR:  parent graph label "person" is not edge label.
```

Finally, drop the graph the examples built:

```cypher
DROP GRAPH castlists CASCADE;
```

## Notes {#notes}

The label name cannot be qualified. `CREATE ELABEL castlists.directed` is a syntax error,
and the graph always comes from `graph_path`. With none set, the statement stops with
`graph_path is NULL`.

`\dGe` lists edge labels and describes each one it matches; `\dGl` lists labels of both
kinds without the detail.

## Compatibility {#compatibility}

### ISO/IEC 39075 (GQL) {#isoiec-39075-gql}

GQL has no label DDL. An edge is described by an *edge type* inside a graph type,
`<create graph type statement>` (§12.6). An edge type names the edge's endpoint node types
and its properties, and constrains a graph that references it. AgensGraph declares edge
labels one at a time, and an edge label constrains neither its endpoints nor its properties.
Graph types are tracked as planned in the
[GQL conformance matrix](/agensgraph/appendix/gql-conformance/).

### PostgreSQL {#postgresql}

`CREATE ELABEL` corresponds to `CREATE TABLE`. `UNLOGGED`, `IF NOT EXISTS`, `INHERITS`,
`WITH` and `TABLESPACE` mean what they mean there, and the promoted-property forms become
`GENERATED ALWAYS AS ... STORED` generated columns. The differences are the fixed
four-column shape, the three indexes created for you, the registration in `ag_label`, the
automatic parent, and the position-sensitive option order. `start` and `end` are not
declared as foreign keys, so nothing at the table level stops an edge from pointing at a
vertex that has been deleted. [`DROP VLABEL`](/agensgraph/reference/ddl/drop-label/) handles that.

## See also {#see-also}

- [`CREATE VLABEL`](/agensgraph/reference/ddl/create-vlabel/)
- [`ALTER VLABEL` and `ALTER ELABEL`](/agensgraph/reference/ddl/alter-label/)
- [`DROP VLABEL` and `DROP ELABEL`](/agensgraph/reference/ddl/drop-label/)
- [`REINDEX VLABEL` and `REINDEX ELABEL`](/agensgraph/reference/ddl/reindex/)
- [Label inheritance](/agensgraph/concepts/label-inheritance/)
