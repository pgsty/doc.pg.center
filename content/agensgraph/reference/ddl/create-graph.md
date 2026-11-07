---
title: CREATE GRAPH
linkTitle: CREATE GRAPH
description: Creates a graph — a schema, the two base labels that every label inherits from, and the sequence that
  hands out label ids.
type: docs
weight: 10
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/ddl/create-graph.html
upstream_source: agensgraph
upstream_modified: true
---


Creates a graph — a schema, the two base labels that every label inherits from, and the
sequence that hands out label ids.

## Synopsis {#synopsis}

```text
CREATE GRAPH [ IF NOT EXISTS ] graph_name [ AUTHORIZATION role_specification ]CREATE GRAPH ONLY graph_name
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

A graph is a schema. `CREATE GRAPH` creates that schema and puts three objects in it:

- `ag_vertex`, the base vertex label,
- `ag_edge`, the base edge label,
- `ag_label_seq`, the sequence that assigns label ids.

Every label you create afterwards inherits from `ag_vertex` or `ag_edge`. That inheritance
gives an unlabelled pattern like `MATCH (n)` its meaning.
[How a graph is stored](/agensgraph/concepts/graph-on-postgresql/) describes the
objects and the identifier scheme in full.

- The name has to be free as a graph name and as a schema name, because the graph owns a
  schema of that name.
- If the session's `graph_path` is empty, `CREATE GRAPH` sets it to the new graph. A
  `graph_path` that is already set is left alone.
- `CREATE GRAPH ONLY` creates the schema and the catalog row and nothing else. It is the
  form `pg_dump` emits, so that a restore can recreate the base labels itself with their
  original label ids. A graph created this way cannot hold a label until those base labels
  exist.

## Parameters {#parameters}

IF NOT EXISTS
: Issue a notice instead of an error when a graph of that name already exists. Nothing is
  created and nothing existing is changed.

graph_name
: Name of the graph to create.

AUTHORIZATION role_specification
: Role that owns the graph and the objects created with it. Write a role name,
  `CURRENT_ROLE`, `CURRENT_USER` or `SESSION_USER`. Without this clause the graph belongs to
  the role that runs the statement.

ONLY
: Create the schema and the catalog row without `ag_vertex`, `ag_edge` or `ag_label_seq`.
  Unlike the plain form, it does not touch `graph_path`.

## Examples {#examples}

The examples build their own graph, `boxoffice`, rather than using
[the example dataset](/agensgraph/get-started/example-dataset/), and drop it at the end.

### Create a graph {#create-a-graph}

```cypher
CREATE GRAPH boxoffice;
```

```
CREATE GRAPH
```

The statement claimed an empty `graph_path`:

```sql
SHOW graph_path;
```

```
 graph_path
------------
 boxoffice
(1 row)
```

The graph is listed by `\dG`:

```psql
\dG boxoffice
```

```
  List of graphs
   Name    | Owner
-----------+-------
 boxoffice | agens
(1 row)
```

And it already holds the two base labels:

```psql
\dGl boxoffice.*
```

```
             List of labels
   Graph   |   Name    |  Type  | Owner
-----------+-----------+--------+-------
 boxoffice | ag_edge   | edge   | agens
 boxoffice | ag_vertex | vertex | agens
(2 rows)
```

### Create a graph only if it is not there {#create-a-graph-only-if-it-is-not-there}

```cypher
CREATE GRAPH IF NOT EXISTS boxoffice;
```

```
NOTICE:  graph "boxoffice" already exists, skipping
CREATE GRAPH
```

The existing graph is untouched. This is not a "create or replace".

### Create a graph owned by another role {#create-a-graph-owned-by-another-role}

```sql
CREATE ROLE curator;
```

```cypher
CREATE GRAPH festival AUTHORIZATION curator;
```

```
CREATE GRAPH
```

```psql
\dG festival
```

```
   List of graphs
   Name   |  Owner
----------+---------
 festival | curator
(1 row)
```

### Create the schema without the base labels {#create-the-schema-without-the-base-labels}

```cypher
CREATE GRAPH ONLY skeleton;
```

```
CREATE GRAPH
```

The graph exists but holds nothing:

```psql
\dGl skeleton.*
```

```
No matching labels found.
```

Because `ag_vertex` is missing, a label cannot be created in it:

```cypher
SET graph_path = skeleton;
CREATE VLABEL film;
```

```
ERROR:  relation "skeleton.ag_vertex" does not exist
```

Clean up the three graphs and the role:

```cypher
DROP GRAPH boxoffice CASCADE;
DROP GRAPH festival CASCADE;
DROP GRAPH skeleton;
```

```sql
DROP ROLE curator;
```

`skeleton` needs no `CASCADE` because nothing was created inside it. A graph made by the
plain form always does. See [`DROP GRAPH`](/agensgraph/reference/ddl/drop-graph/).

## Notes {#notes}

`graph_path` names the graph that unqualified label names belong to. It is a per-session
setting; set it in each new session, or attach it to a database or a role:

```sql
ALTER DATABASE <database> SET graph_path = boxoffice;
```

Two more statements act on a graph as a whole. Neither has an `IF EXISTS` form:

```cypher
CREATE GRAPH receipts;
ALTER GRAPH receipts RENAME TO takings;
ALTER GRAPH takings OWNER TO CURRENT_USER;
SHOW graph_path;
```

```
 graph_path
------------
 takings
(1 row)
```

A rename moves the underlying schema with the graph, and the session's `graph_path` follows
it. So it reads `takings` above rather than `receipts`.

```cypher
DROP GRAPH takings CASCADE;
```

## Compatibility {#compatibility}

### ISO/IEC 39075 (GQL) {#isoiec-39075-gql}

GQL defines `<create graph statement>` (§12.4) as
`CREATE [PROPERTY] GRAPH <name> {<open graph type> | <of graph type>}`. A graph is created
either as `ANY`, which accepts any content, or against a *graph type* that constrains its
node types, edge types and properties. AgensGraph's graphs are always open, so no graph type
is written and none can be. The `PROPERTY` spelling is not accepted:
`CREATE PROPERTY GRAPH boxoffice` is a syntax error. Graph types are tracked as planned in
the [GQL conformance matrix](/agensgraph/appendix/gql-conformance/).

`AUTHORIZATION` and `ONLY` are AgensGraph's own; GQL has neither. GQL's `OR REPLACE` form is
not accepted either.

### PostgreSQL {#postgresql}

`CREATE GRAPH` corresponds to `CREATE SCHEMA`, and `IF NOT EXISTS` and `AUTHORIZATION` mean
what they mean there. The difference is the contents. `CREATE SCHEMA` creates an empty
schema. `CREATE GRAPH` also creates the base labels and the label-id sequence, and registers
the schema in `ag_graph` so that Cypher can find it. `CREATE SCHEMA` on its own does not
produce a graph.

## See also {#see-also}

- [`DROP GRAPH`](/agensgraph/reference/ddl/drop-graph/)
- [`CREATE VLABEL`](/agensgraph/reference/ddl/create-vlabel/)
- [`CREATE ELABEL`](/agensgraph/reference/ddl/create-elabel/)
- [How a graph is stored](/agensgraph/concepts/graph-on-postgresql/)
