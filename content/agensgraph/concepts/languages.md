---
title: Cypher, GQL and SQL
linkTitle: Cypher, GQL and SQL
description: AgensGraph answers questions in three languages.
type: docs
weight: 40
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/concepts/languages.html
upstream_source: agensgraph
upstream_modified: true
---


AgensGraph answers questions in three languages. They are not three products, three modes or
three connections. There is one parser, one planner, one set of tables, and one wire
protocol, and you choose per statement — or mix two in one statement.

**Cypher** is the graph language, and the most complete surface. Everything the graph can do
is reachable from Cypher.

**GQL** is ISO/IEC 39075, the standard graph query language. In AgensGraph it is not a
separate dialect. The GQL statements are accepted wherever a Cypher statement is accepted:
`LET`, `NEXT`, `FILTER`, `FINISH`, `INSERT`, `FOR`, `CALL { }`, and the subquery value
expressions `EXISTS { }` and `VALUE { }`. There is no switch to flip and no separate
parser.
[GQL conformance](/agensgraph/appendix/gql-conformance/) records which parts of the standard are in.

**SQL** is PostgreSQL's, unchanged. Every table, view, function, extension, role and
transaction you know from PostgreSQL is here, and a graph is visible to SQL as ordinary
tables.

## Choosing {#choosing}

Pick by the shape of the question, not by preference:

* **Following relationships** — how a person connects to a film, how far apart two films are,
  what is reachable in three hops — is what a graph pattern is for. A join chain in SQL says
  the same thing at several times the length, and cannot express "any number of hops" at all.
* **Aggregating, windowing, set operations, joining against ordinary tables, and anything
  administrative** is SQL's, and Cypher does not try to replace it.
* **GQL** where you want the standard's spelling, or where you are writing against more than
  one graph database and want the portable form. `INSERT` and `CREATE` do the same work;
  `FILTER` and `WHERE` do the same work.

You do not have to choose once. [Combining SQL and
Cypher](/agensgraph/querying/combining-sql-and-cypher/) is a full page on the crossing points, and
it is the most useful thing in this manual for a reader who already knows SQL.

## If you know SQL {#if-you-know-sql}

The vocabularies line up more closely than the syntax suggests, because
[a graph is a schema and a label is a table](/agensgraph/concepts/graph-on-postgresql/):

| SQL | Cypher | Note |
| --- | --- | --- |
| `CREATE SCHEMA s` | `CREATE GRAPH s` | The graph *is* the schema. |
| `CREATE TABLE t` | `CREATE VLABEL t` | A vertex label. `CREATE ELABEL` for edges. |
| `INSERT INTO t VALUES (…)` | `CREATE (:t {…})` | `INSERT (:t {…})` is the GQL spelling. |
| `SELECT … FROM t WHERE …` | `MATCH (n:t) WHERE … RETURN …` | `RETURN` is the projection, and it comes last. |
| `SELECT … FROM a JOIN b ON …` | `MATCH (a)-[:e]->(b)` | A pattern is a join along an edge. |
| `LEFT JOIN` | `OPTIONAL MATCH` | Unmatched rows come back with nulls. |
| `UPDATE t SET c = …` | `MATCH (n:t) SET n.c = …` | Find first, then write. |
| `DELETE FROM t WHERE …` | `MATCH (n:t) WHERE … DELETE n` | `DETACH DELETE` removes the edges too. |
| `WITH cte AS (…)` | `WITH …` / `NEXT` | Cypher's `WITH` divides a pipeline; it is not a CTE. |
| `ORDER BY` / `LIMIT` / `OFFSET` | `ORDER BY` / `LIMIT` / `SKIP` | `SKIP` and `OFFSET` are synonyms. |
| `CREATE INDEX ON t ((c))` | `CREATE PROPERTY INDEX ON t (c)` | Becomes an expression index. |
| `count(*)`, `sum`, `avg` | the same | Aggregates are PostgreSQL's. |
| `information_schema`, `pg_catalog` | `ag_graph`, `ag_label` | See [System catalogs](/agensgraph/system-catalogs/). |

Three differences catch SQL users early, and all three are silent rather than loud:

**A property read returns `jsonb`, not text.** `RETURN m.title` prints `"The Matrix"` with
the quotes, and casting inside the query does not change it. To get a plain scalar, unwrap it
outside: `SELECT t #>> '{}' FROM (MATCH (m:movie) RETURN m.title AS t) q`.

**`ORDER BY 2` does not mean "the second column".** In Cypher the `2` is a constant, so every
row compares equal and nothing sorts. Order by the alias or the expression.

**`n.id` is not the id.** `id(n)` returns the `graphid`; `n.id` looks for a property called
`id` and returns nothing if there isn't one.

## One statement, two languages {#one-statement-two-languages}

A Cypher query can appear where SQL expects a table:

```psql
SELECT q.title #>> '{}' AS film, r.score
FROM (MATCH (:person {name: 'Christopher Nolan'})-[:directed]->(m:movie)
      RETURN m.title AS title) q
JOIN rating r ON r.title = q.title #>> '{}'
WHERE r.source = 'critics'
ORDER BY r.score DESC;
```

```
     film     | score
--------------+-------
 Inception    |   8.8
 Interstellar |   8.7
```

And SQL can appear where Cypher expects a value:

```cypher
MATCH (m:movie)
WHERE m.title = (SELECT to_jsonb(title) FROM rating
                 WHERE source = 'critics' ORDER BY score DESC LIMIT 1)
RETURN m.title AS best;
```

```
    best
-------------
 "Inception"
```

Both of those run against [the example dataset](/agensgraph/get-started/example-dataset/).

## What "GQL support" means in this release {#what-gql-support-means-in-this-release}

GQL arrived in AgensGraph as added statements on the existing grammar rather than as a
second language, which has two consequences worth stating plainly.

A GQL statement can be mixed with Cypher in one query — `MATCH … LET … RETURN` is a valid
statement, and so is `MATCH … FILTER … NEXT RETURN …`. Nothing marks a query as "GQL".

And conformance is partial, by feature rather than by mode.
[GQL conformance](/agensgraph/appendix/gql-conformance/) lists it feature by feature against the
subclauses of ISO/IEC 39075:2024, and each clause page in the
[reference](/agensgraph/reference/clauses/) repeats the same statement for that clause under
its own *Compatibility* heading.
