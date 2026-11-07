---
title: Graph catalogs
linkTitle: Graph catalogs
description: AgensGraph adds seven tables to pg_catalog.
type: docs
weight: 10
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/system_catalogs/catalogs.html
upstream_source: agensgraph
upstream_modified: true
---


AgensGraph adds seven tables to `pg_catalog`. Four of them describe the graph structure, and
those are the ones you will query. Three are the shared parent relations that every label
inherits from. PostgreSQL's own catalogs are unchanged and are documented in [its catalogs
chapter](https://www.postgresql.org/docs/18/catalogs.html).

| Catalog | What it holds |
| --- | --- |
| [`ag_graph`](#ag_graph) | One row per graph. |
| [`ag_label`](#ag_label) | One row per label, vertex and edge alike. |
| [`ag_label_property`](#ag_label_property) | One row per property promoted to a typed column. |
| [`ag_graphmeta`](#ag_graphmeta) | Edge counts per (start label, edge label, end label) triple. |
| `ag_vertex`, `ag_edge` | The parent relation of every vertex or edge label in a graph. One pair exists inside each graph's schema, not in `pg_catalog`. |
| `ag_graphpath` | The composite that backs the `graphpath` type. |

Two views present the same information in a readable form: see [Graph
views](/agensgraph/system-catalogs/views/).

## ag_graph {#ag_graph}

One row per graph. A graph is a schema, so `nspid` points at the schema that carries its
labels.

| Column | Type | Description |
| --- | --- | --- |
| `oid` | `oid` | Row identifier. |
| `graphname` | `name` | The graph's name. Unique across the database. |
| `nspid` | `oid` | The `pg_namespace` row for the graph's schema. |
| `graphmeta_valid` | `boolean` | Whether `ag_graphmeta` is up to date for this graph. False means the planner cannot use it for scan pruning. |

```sql
SELECT oid, graphname, nspid, graphmeta_valid FROM pg_catalog.ag_graph;
```

```
  oid  | graphname | nspid | graphmeta_valid
-------+-----------+-------+-----------------
 16386 | g         | 16385 | t
 16434 | moviekb   | 16433 | f
```

`graphmeta_valid` is set false when the metadata is known to be stale, after a binary
upgrade for example. `SELECT regather_graphmeta();` rebuilds it and sets the flag. See
[Graph metadata](/agensgraph/system-catalogs/graph-metadata/).

## ag_label {#ag_label}

One row per label. Both vertex and edge labels live here, distinguished by `labkind`.

| Column | Type | Description |
| --- | --- | --- |
| `oid` | `oid` | Row identifier. |
| `labname` | `name` | The label's name. Unique within a graph. |
| `graphid` | `oid` | The `ag_graph` row this label belongs to. |
| `labid` | `integer` | The label's id within the graph, and the high 16 bits of every `graphid` in it. |
| `relid` | `oid` | The `pg_class` row for the label's table. |
| `labkind` | `"char"` | `v` for a vertex label, `e` for an edge label. |

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

`labid` 1 and 2 are always the graph's `ag_vertex` and `ag_edge`, which are created with the
graph. Because `labid` is 16 bits and 0 is not valid, a graph holds at most 65,535 labels.
See [Limits](/agensgraph/appendix/limits/).

Joining `relid` to `pg_class` gets you from a label to its table. That join is what makes
the ordinary PostgreSQL introspection work on a graph:

```sql
SELECT l.labname, pg_size_pretty(pg_total_relation_size(l.relid)) AS size
FROM pg_catalog.ag_label l
  JOIN pg_catalog.ag_graph g ON g.oid = l.graphid
WHERE g.graphname = 'moviekb' AND l.labkind = 'v'
ORDER BY 1;
```

## ag_label_property {#ag_label_property}

One row per property that has been [promoted to a typed
column](/agensgraph/querying/typed-columns/). This catalog is new in 2.18.

| Column | Type | Description |
| --- | --- | --- |
| `laboid` | `oid` | The `ag_label` row the promoted column belongs to. |
| `propname` | `name` | The property key the column carries. |
| `attnum` | `smallint` | The column's attribute number in the label's table. |
| `semantics` | `"char"` | How the column relates to the property. |

The primary key is `(laboid, propname)`, so a label promotes a given key at most once.

A property read resolves to a promoted column only when a row exists here. That mechanism is
behind the promotion form that surprises people. `GENERATED ALWAYS AS (expr) STORED` creates
a column but registers no row in this catalog. So the column is readable from SQL and
invisible to a Cypher property read.

## ag_graphmeta {#ag_graphmeta}

One row per (start label, edge label, end label) triple that actually occurs in a graph, with
how many edges make it up. The planner uses it two ways: to estimate a traversal, and to
prune scans of labels that cannot participate in a pattern.

| Column | Type | Description |
| --- | --- | --- |
| `graph` | `oid` | The `ag_graph` row. |
| `edge` | `smallint` | The edge label's `labid`. |
| `start` | `smallint` | The start vertex label's `labid`. |
| `end` | `smallint` | The end vertex label's `labid`. |
| `edgecount` | `bigint` | How many edges of that shape exist. |

Read it through [`ag_graphmeta_view`](/agensgraph/system-catalogs/views/#ag_graphmeta_view), which resolves the label
ids to names. The table is maintained only when `auto_gather_graphmeta` is on, and
`regather_graphmeta()` rebuilds it from scratch. [Graph metadata](/agensgraph/system-catalogs/graph-metadata/) covers
both.

## ag_vertex and ag_edge {#ag_vertex-and-ag_edge}

These are not in `pg_catalog`. Every graph's schema contains its own pair, and every label
you create inherits from one of them. That inheritance is what gives an unlabelled pattern
its meaning. See [How a graph is stored](/agensgraph/concepts/graph-on-postgresql/).

`<graph>.ag_vertex` has the vertex column pair, `(id graphid, properties jsonb)`.
`<graph>.ag_edge` adds the endpoints, `(id, start, end, properties)`.

## ag_graphpath {#ag_graphpath}

The composite type behind [`graphpath`](/agensgraph/reference/types/). It is an implementation
detail. Build and read a path with the pattern syntax and the path functions rather than
touching this directly.
