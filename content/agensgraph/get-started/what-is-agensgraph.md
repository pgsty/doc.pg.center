---
title: What AgensGraph is
linkTitle: What AgensGraph is
description: AgensGraph is a multi-model database.
type: docs
weight: 10
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/get_started/what-is-agensgraph.html
upstream_source: agensgraph
upstream_modified: true
---


AgensGraph is a multi-model database. One server, one database, one connection. Your data
lives there as a **property graph** and as **relational tables** at the same time, and you
query it with **Cypher**, **GQL** or **SQL**. You can use two of them in one statement.

It is built on PostgreSQL. Release 2.18 is PostgreSQL 18 plus the graph model, so everything
PostgreSQL gives you comes with it unchanged. That is transactions, roles and row-level
security, `pg_dump` and `pg_basebackup`, streaming replication, the planner and `EXPLAIN`,
the extension ecosystem, and the wire protocol every PostgreSQL driver already speaks.

## What makes it different {#what-makes-it-different}

**A graph is stored as PostgreSQL objects, not beside them.** A graph is a schema, a label is
a table, a vertex is a row. There is no separate graph store to keep in step, and no bridge to
cross. A Cypher write and a SQL write in one transaction commit together, because both are
writes to tables in the same database. [How a graph is stored](/agensgraph/concepts/graph-on-postgresql/) is the page that makes the rest of this manual
make sense.

**Traversal is a first-class query, not a recursive join you write yourself.** "Which films
share an actor with this one", "how far apart are these two people" and "what is reachable in
three hops" are patterns:

```cypher
MATCH (:person {name: 'Keanu Reeves'})-[:acted_in]->(:movie)<-[:acted_in]-(co:person)
RETURN DISTINCT co.name AS co_actor ORDER BY co_actor;
```

```
       co_actor
----------------------
 "Carrie-Anne Moss"
 "Laurence Fishburne"
```

**Extensions apply to graph data.** A property is `jsonb` in an ordinary table. So `pgvector`
will index an embedding stored on a vertex, and PostgreSQL's full-text search will index a
text property. One query can then find semantically similar documents and walk the graph out
from them. See [vector search](/agensgraph/guides/search/vector/).

**GQL, the ISO standard, is part of the same language.** 2.18 adds a substantial part of
ISO/IEC 39075, with no separate mode and no separate parser. `LET`, `NEXT`, `FILTER`,
`FINISH`, `INSERT`, `FOR`, `CALL { }` and the subquery value expressions are accepted wherever
Cypher is. See [GQL conformance](/agensgraph/appendix/gql-conformance/).

## Who it is for {#who-it-is-for}

Teams that have relational data, have a graph-shaped question about it, and do not want to run
a second database to ask it. The common shapes are recommendation and similarity, fraud and
risk chains, permission and ownership hierarchies, network and dependency topologies, and
knowledge graphs behind retrieval-augmented generation.

It is a good fit in three cases. When the graph and the tables belong to the same system of
record. When you already operate PostgreSQL and want to keep those skills and tools. And when
your queries mix traversal with aggregation, joins or window functions.

It is the wrong tool if you need a distributed graph store that shards one graph across
machines, or a graph-analytics engine for whole-graph algorithms such as PageRank or community
detection at scale. AgensGraph scales the way PostgreSQL scales: one primary, read replicas,
and vertical growth.

## What is in this release {#what-is-in-this-release}

* PostgreSQL 18 as the base.
* A large step toward GQL conformance.
* Typed-column property promotion, which turns a hot `jsonb` property into a real indexable
  column without changing how you write queries. See [Promoting a property to a
  column](/agensgraph/querying/typed-columns/).
* Planner and estimation work on graph traversal.

Several changes need an application's attention before you upgrade, including new reserved
words and a stricter rule about what may appear in a `WHERE`. [Release
notes](/agensgraph/release-notes/2.18/) lists them, and [Upgrading to
2.18](/agensgraph/release-notes/upgrade-to-2.18/) has the procedure.

## Next {#next}

[Install AgensGraph](/agensgraph/get-started/install/), then [load the example dataset](/agensgraph/get-started/example-dataset/) that
every page in this manual uses, then [run your first query](/agensgraph/get-started/first-query/).
