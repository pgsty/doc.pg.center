---
title: DROP GRAPH
linkTitle: DROP GRAPH
description: Removes a graph, and with CASCADE every label, vertex and edge in it.
type: docs
weight: 20
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/ddl/drop-graph.html
upstream_source: agensgraph
upstream_modified: true
---


Removes a graph, and with `CASCADE` every label, vertex and edge in it.

## Synopsis {#synopsis}

```text
DROP GRAPH [ IF EXISTS ] graph_name [, ... ] [ CASCADE | RESTRICT ]
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`DROP GRAPH` drops the graph's catalog row and its schema. Everything the graph holds
depends on that schema: labels, the tables behind them, their rows, indexes, constraints and
sequences. So `RESTRICT`, which is the default, refuses while any of it is there.

A graph made by the plain [`CREATE GRAPH`](/agensgraph/reference/ddl/create-graph/) is never empty: `ag_vertex`,
`ag_edge` and `ag_label_seq` are created with it. So every such graph needs `CASCADE`. Only
a graph made with `CREATE GRAPH ONLY`, which creates none of those, can be dropped without
it.

- Dropping a graph does not require its labels to be empty. `CASCADE` takes the rows with
  the tables.
- If the dropped graph is the session's `graph_path`, the setting is cleared.
- The graph's schema cannot be dropped on its own: `DROP SCHEMA` on it is refused and points
  you here.

## Parameters {#parameters}

IF EXISTS
: Issue a notice instead of an error for a graph that does not exist. Other names in the
  same statement are still dropped.

graph_name
: Name of the graph to drop. Several names may be given, separated by commas.

CASCADE
: Drop the objects that depend on the graph: its labels, their tables and rows, and the
  label-id sequence.

RESTRICT
: Refuse if anything depends on the graph. This is the default.

## Examples {#examples}

### Drop a graph and everything in it {#drop-a-graph-and-everything-in-it}

```cypher
CREATE GRAPH clearance;
SET graph_path = clearance;
CREATE VLABEL film;
CREATE (:film {title: 'Arrival'});
```

Without `CASCADE` the drop is refused, and the message lists what stands in the way:

```cypher
DROP GRAPH clearance;
```

```
ERROR:  cannot drop graph clearance because other objects depend on it
DETAIL:  sequence clearance.ag_label_seq depends on schema clearance
vlabel ag_vertex depends on schema clearance
elabel ag_edge depends on schema clearance
vlabel film depends on schema clearance
HINT:  Use DROP ... CASCADE to drop the dependent objects too.
```

`CASCADE` takes all four, and the vertex in `film` with them:

```cypher
DROP GRAPH clearance CASCADE;
```

```
NOTICE:  drop cascades to 4 other objects
DETAIL:  drop cascades to sequence clearance.ag_label_seq
drop cascades to vlabel ag_vertex
drop cascades to elabel ag_edge
drop cascades to vlabel film
DROP GRAPH
```

`clearance` was the session's `graph_path`, so the setting is now empty:

```sql
SHOW graph_path;
```

```
 graph_path
------------

(1 row)
```

### Drop several graphs, skipping the ones that are gone {#drop-several-graphs-skipping-the-ones-that-are-gone}

```cypher
CREATE GRAPH archive_2024;
CREATE GRAPH archive_2025;
DROP GRAPH IF EXISTS archive_2024, archive_2025, archive_2026 CASCADE;
```

```
NOTICE:  graph "archive_2026" does not exist, skipping
NOTICE:  drop cascades to 6 other objects
DETAIL:  drop cascades to sequence archive_2025.ag_label_seq
drop cascades to vlabel ag_vertex
drop cascades to elabel ag_edge
drop cascades to sequence archive_2024.ag_label_seq
drop cascades to vlabel ag_vertex
drop cascades to elabel ag_edge
DROP GRAPH
```

The missing name is reported and the two that exist are dropped:

```psql
\dG archive*
```

```
No matching graphs found.
```

## Notes {#notes}

To empty a graph without dropping it, run `MATCH (n) DETACH DELETE n` and then drop the
labels you no longer want. The schema and the base labels stay in place. A label has to be
empty before [`DROP VLABEL`](/agensgraph/reference/ddl/drop-label/) will remove it, so that delete is the usual
first step. `DROP GRAPH ... CASCADE` skips the requirement altogether, because it drops the
tables rather than the labels one at a time.

## Compatibility {#compatibility}

### ISO/IEC 39075 (GQL) {#isoiec-39075-gql}

GQL's `<drop graph statement>` (§12.5) is
`DROP [PROPERTY] GRAPH [IF EXISTS] <name>`. AgensGraph accepts the `DROP GRAPH` and
`IF EXISTS` parts of that. It adds a name list and the `CASCADE`/`RESTRICT` choice, which
GQL does not have. The `PROPERTY` spelling is not accepted: `DROP PROPERTY GRAPH clearance`
is a syntax error.

### PostgreSQL {#postgresql}

`DROP GRAPH` corresponds to `DROP SCHEMA`, and `IF EXISTS`, the name list and
`CASCADE`/`RESTRICT` behave as they do there. It differs in refusing to leave a half-dropped
graph behind. `DROP SCHEMA` on a graph's schema fails with
`cannot drop schema clearance because graph clearance requires it`, so the catalog row and
the schema always go together.

## See also {#see-also}

- [`CREATE GRAPH`](/agensgraph/reference/ddl/create-graph/)
- [`DROP VLABEL` and `DROP ELABEL`](/agensgraph/reference/ddl/drop-label/)
- [How a graph is stored](/agensgraph/concepts/graph-on-postgresql/)
