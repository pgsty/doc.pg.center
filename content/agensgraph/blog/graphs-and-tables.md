---
title: Graphs and tables in one engine
linkTitle: Graphs and tables in one engine
description: Why AgensGraph keeps property graphs, relational tables, and PostgreSQL operations inside one transaction
  boundary.
type: docs
date: 2026-11-07
tags:
- AgensGraph
- PostgreSQL
- graph
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/get_started/what-is-agensgraph.html
upstream_source: agensgraph
upstream_modified: true
summary: A source-linked explanation of the multi-model boundary in AgensGraph.
---

A graph database often becomes a second system of record. The application then has to decide where a fact lives, how it crosses the boundary, and which transaction commits first.

AgensGraph takes a different route: the graph is made of PostgreSQL objects. A graph is a schema, a label is a table, and a vertex or edge is a row. The property graph model gives queries a language for patterns and paths while PostgreSQL keeps the operational boundary familiar.

## The useful boundary

A Cypher write and a SQL write commit together because both write to tables in the same database. Roles, row-level security, `EXPLAIN`, backups, streaming replication, and the PostgreSQL wire protocol remain part of the same system.

That boundary matters when the question crosses models:

```sql
SELECT f.title, r.stars
FROM (MATCH (:person {name: 'Keanu Reeves'})-[:acted_in]->(m:movie)
      RETURN m.title AS title) AS f
JOIN my_ratings r ON r.title = f.title #>> '{}'
ORDER BY r.stars DESC;
```

The graph pattern finds the films; SQL joins the result to relational ratings. There is no export job between the two operations.

## Where the model fits

This is a good fit when the graph and tables belong to the same system of record, the team already operates PostgreSQL, and queries combine traversal with aggregation or joins. It is a poor fit for a distributed graph store that shards one graph across machines or for a graph analytics engine that runs whole-graph algorithms at very large scale.

The [What AgensGraph is](/agensgraph/get-started/what-is-agensgraph/) page covers the model, trade-offs, and the 2.18 additions. The [graph storage guide](/agensgraph/concepts/graph-on-postgresql/) goes one layer deeper into tables and identities.
