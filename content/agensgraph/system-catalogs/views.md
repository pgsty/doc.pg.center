---
title: Graph views
linkTitle: Graph views
description: Two views in pg_catalog present the graph catalogs in a readable form, resolving oids and label ids
  to names.
type: docs
weight: 20
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/system_catalogs/views.html
upstream_source: agensgraph
upstream_modified: true
---


Two views in `pg_catalog` present the graph catalogs in a readable form, resolving oids and
label ids to names. Both are ordinary views, so you can join and filter them.

## ag_property_indexes {#ag_property_indexes}

One row per property index, with the statement that would recreate it.

| Column | Type | Description |
| --- | --- | --- |
| `graphname` | `name` | The graph the index belongs to. |
| `labelname` | `name` | The label the index is on. |
| `indexname` | `name` | The index's name. |
| `tablespace` | `name` | The tablespace, or null for the default. |
| `unique` | `boolean` | Whether the index is unique. |
| `indexdef` | `text` | A `CREATE PROPERTY INDEX` statement that recreates it. |
| `owner` | `name` | The role that owns the index. |
| `size` | `text` | The index's size, already formatted. |
| `description` | `text` | The comment on the index, if any. |

The [example dataset](/agensgraph/get-started/example-dataset/) has no property indexes, so create
two to have something to look at:

```cypher
CREATE PROPERTY INDEX ON movie (title);
CREATE PROPERTY INDEX ON person (name);
```

```sql
SELECT labelname, indexname, indexdef, size
FROM pg_catalog.ag_property_indexes
WHERE graphname = 'moviekb' ORDER BY labelname, indexname;
```

```
 labelname |    indexname    |                              indexdef                              |  size
-----------+-----------------+--------------------------------------------------------------------+-------
 movie     | movie_title_idx | CREATE PROPERTY INDEX movie_title_idx ON movie USING btree (title) | 16 kB
 person    | person_name_idx | CREATE PROPERTY INDEX person_name_idx ON person USING btree (name) | 16 kB
```

Drop them again with `DROP PROPERTY INDEX movie_title_idx;` when you are done.

The `indexdef` column is the useful one. It gives back the property-level statement rather
than the expression index the server built, and that is the form you want when scripting a
schema. `\dGi` in [the agens client](/agensgraph/reference/agens/) prints the same information.

The view lists indexes on [promoted columns](/agensgraph/querying/typed-columns/) as well as
indexes over the property bag. So it is the single place to look for "what is indexed on this
label".

## ag_graphmeta_view {#ag_graphmeta_view}

One row per edge shape that occurs in a graph, with names instead of label ids.

| Column | Type | Description |
| --- | --- | --- |
| `graphname` | `name` | The graph. |
| `start` | `name` | The label of the edge's start vertex. |
| `edge` | `name` | The edge label. |
| `end` | `name` | The label of the edge's end vertex. |
| `edgecount` | `bigint` | How many edges of that shape exist. |

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

This is the clearest picture of a graph's actual shape that AgensGraph can give you. Read it
before tuning a query: it tells you which traversals exist and how big each one is. The
planner uses the same rows.

The view is empty unless the metadata has been gathered. See [Graph
metadata](/agensgraph/system-catalogs/graph-metadata/) for `auto_gather_graphmeta` and `regather_graphmeta()`, and
check `ag_graph.graphmeta_valid` if the numbers look wrong.
