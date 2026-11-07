---
title: DROP VLABEL and DROP ELABEL
linkTitle: DROP VLABEL and DROP ELABEL
description: Removes a vertex label or an edge label, and with CASCADE the rows in it.
type: docs
weight: 60
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/ddl/drop-label.html
upstream_source: agensgraph
upstream_modified: true
---


Removes a vertex label or an edge label, and with `CASCADE` the rows in it.

## Synopsis {#synopsis}

```text
DROP VLABEL [ IF EXISTS ] label_name [, ... ] [ CASCADE | RESTRICT ]DROP ELABEL [ IF EXISTS ] label_name [, ... ] [ CASCADE | RESTRICT ]
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`DROP VLABEL` drops a vertex label and `DROP ELABEL` an edge label; each refuses the other
kind. Dropping a label drops the table behind it, along with its id sequence, its indexes
and its constraints.

`RESTRICT`, which is the default, has two things to object to:

- **Rows.** A label that still holds vertices or edges is refused with
  `cannot drop <label> because it is not empty.` This is stricter than the dependency check
  PostgreSQL applies to a table, and it catches people out.
- **Children.** A label with a child label is refused, and the message names the child.

`CASCADE` overrides both. It drops a label whatever it holds, and:

- dropping a **vertex** label deletes the edges attached to its vertices, whatever labels
  those edges have. The edge labels themselves survive.
- dropping an **edge** label deletes only its own edges. The vertices they connected
  survive.

The label is looked up in the graph named by `graph_path`; the name cannot be qualified.

- The base labels `ag_vertex` and `ag_edge` cannot be dropped.
- The table behind a label cannot be dropped on its own: `DROP TABLE` on it is refused and
  points you here.
- To empty a graph without dropping its labels, use `MATCH (n) DETACH DELETE n` instead.

## Parameters {#parameters}

IF EXISTS
: Issue a notice instead of an error for a label that does not exist. Other names in the
  same statement are still dropped.

label_name
: Name of the label to drop. Several names may be given, separated by commas.

CASCADE
: Drop the label along with its rows and its child labels. For a vertex label, also drop the
  edges attached to its vertices.

RESTRICT
: Refuse if the label holds any rows or has a child label. This is the default.

## Examples {#examples}

The examples build their own graph, `tidygraph`, rather than using
[the example dataset](/agensgraph/get-started/example-dataset/), and drop it at the end.

```cypher
CREATE GRAPH tidygraph;
SET graph_path = tidygraph;
CREATE VLABEL film;
CREATE VLABEL person;
CREATE ELABEL directed;
CREATE (:person {name: 'Denis Villeneuve'})-[:directed]->(:film {title: 'Arrival'});
CREATE VLABEL draft;
```

### Drop an empty label {#drop-an-empty-label}

```cypher
DROP VLABEL draft;
```

```
DROP VLABEL
```

Nothing else is reported, because nothing else was affected.

### Drop a label that still holds vertices {#drop-a-label-that-still-holds-vertices}

`film` has a vertex in it, so the default refuses:

```cypher
DROP VLABEL film;
```

```
ERROR:  cannot drop film because it is not empty.
```

`CASCADE` takes the label, its vertex, and the `directed` edge that pointed at it:

```cypher
DROP VLABEL film CASCADE;
```

```
DROP VLABEL
```

```cypher
MATCH ()-[e:directed]->() RETURN count(e) AS directed_edges;
```

```
 directed_edges 
----------------
 0
(1 row)
```

The edge is gone but its label is not. `directed` is still there, empty:

```psql
\dGl tidygraph.dir*
```

```
           List of labels
   Graph   |   Name   | Type | Owner
-----------+----------+------+-------
 tidygraph | directed | edge | agens
(1 row)
```

### Drop a parent label {#drop-a-parent-label}

```cypher
CREATE VLABEL work;
CREATE VLABEL documentary INHERITS (work);
DROP VLABEL work;
```

```
ERROR:  cannot drop vlabel work because other objects depend on it
DETAIL:  vlabel documentary depends on vlabel work
HINT:  Use DROP ... CASCADE to drop the dependent objects too.
```

`CASCADE` names the child it takes with it:

```cypher
DROP VLABEL work CASCADE;
```

```
NOTICE:  drop cascades to vlabel documentary
DROP VLABEL
```

### Drop several labels, skipping the ones that are gone {#drop-several-labels-skipping-the-ones-that-are-gone}

```cypher
CREATE VLABEL a;
CREATE VLABEL b;
DROP VLABEL IF EXISTS a, b, c;
```

```
NOTICE:  vlabel "c" does not exist, skipping
DROP VLABEL
```

### Refusals worth recognizing {#refusals-worth-recognizing}

Each statement drops one kind of label:

```cypher
DROP ELABEL person;
```

```
ERROR:  DROP ELABEL cannot DROP vertex label
```

The base labels stay:

```cypher
DROP VLABEL ag_vertex;
```

```
ERROR:  DROP base vertex label is prohibited
```

And the table cannot be dropped out from under the label:

```sql
DROP TABLE tidygraph.person;
```

```
ERROR:  cannot drop table tidygraph.person because vlabel person requires it
HINT:  You can drop vlabel person instead.
```

Finally, drop the graph the examples built:

```cypher
DROP GRAPH tidygraph CASCADE;
```

## Notes {#notes}

An edge whose endpoint vertex is deleted is deleted with it, both here and in
`DETACH DELETE`. `start` and `end` are plain `graphid` columns rather than foreign keys. The
graph write path does this, not a referential action on the table.

> [!NOTE]
> `cypher_allow_unsafe_ddl` switches off the kind check and the base-label check, so with it
> on `DROP ELABEL` will drop a vertex label and `ag_vertex` can be dropped. It exists to
> repair a graph whose catalog is already wrong. Leave it off otherwise.

## Compatibility {#compatibility}

### ISO/IEC 39075 (GQL) {#isoiec-39075-gql}

GQL has no statement that drops a label. Element types belong to a graph type, which is
dropped whole by `<drop graph type statement>` (§12.7), and dropping one does not delete any
data. Graph types are tracked as planned in the
[GQL conformance matrix](/agensgraph/appendix/gql-conformance/).

### PostgreSQL {#postgresql}

`DROP VLABEL` and `DROP ELABEL` correspond to `DROP TABLE`, and `IF EXISTS`, the name list
and `CASCADE`/`RESTRICT` behave as they do there. One addition has no `DROP
TABLE` counterpart. `DROP TABLE` does not care how many rows a table has; these statements
refuse a label that is not empty unless you write `CASCADE`. And for a vertex label, `CASCADE` also
deletes edges in *other* labels. Read `CASCADE` here as "and the graph data that depends on
it", not only "and the dependent catalog objects".

## See also {#see-also}

- [`CREATE VLABEL`](/agensgraph/reference/ddl/create-vlabel/)
- [`CREATE ELABEL`](/agensgraph/reference/ddl/create-elabel/)
- [`ALTER VLABEL` and `ALTER ELABEL`](/agensgraph/reference/ddl/alter-label/)
- [`DROP GRAPH`](/agensgraph/reference/ddl/drop-graph/)
- [Label inheritance](/agensgraph/concepts/label-inheritance/)
