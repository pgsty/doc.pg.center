---
title: NEXT
linkTitle: NEXT
description: 'Chains two queries end to end: the rows the first query returns become the input rows of the second.'
type: docs
weight: 190
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/next.html
upstream_source: agensgraph
upstream_modified: true
---


**GQL clause**  **Added in 2.18**

Chains two queries end to end: the rows the first query returns become the input
rows of the second.

## Synopsis {#synopsis}

```text
query NEXT query [ NEXT query ] ...
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`NEXT` turns the result table of the query on its left into the driving table of
the query on its right. It is the composition operator `WITH` performs inside a
single query, promoted to a boundary between two whole queries.

- The query left of `NEXT` must end with `RETURN`.
- The boundary **resets scope**: only the columns that `RETURN` produced are
  visible on the right. Every other variable is gone.
- Columns cross the boundary with their own types. A vertex is still a vertex, an
  edge still an edge, a path still a path.
- `NEXT` is left-associative, so `A NEXT B NEXT C` composes as `(A NEXT B) NEXT C`.
- A [`UNION`](/agensgraph/reference/clauses/union/), `INTERSECT` or `EXCEPT` composite may stand on either side.
- `NEXT` is accepted at the start of a statement and inside `EXPLAIN` and
  `PREPARE`. It is not accepted inside a subquery, in either the `CALL { }` body
  or a subquery value expression.

## Parameters {#parameters}

query
: A complete query. The one on the left of `NEXT` must end with `RETURN`, and every
  column it returns must be named. An unaliased expression raises `expression in
  WITH must be aliased (use AS)`. The query on the right is a fresh one. It begins
  with a clause that can open a query (`MATCH`, `OPTIONAL MATCH`, `CREATE`,
  `INSERT`, `MERGE`, `LOAD FROM`, `UNWIND`, `FOR`, `CALL`, `LET`, `RETURN` or
  `FINISH`). It can also begin with a clause that operates on the carried table
  (`WITH`, `FILTER`, `ORDER BY`, `SKIP`, `OFFSET` or `LIMIT`). It ends the way any
  query ends: with `RETURN`, `FINISH` or a write clause.

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).

Carry the films one director made into a second query that finds their casts.
`NEXT` and an intermediate `WITH` compose the same two steps. Switch tabs to
compare:

{{< tabs >}}
{{< tab label="GQL — NEXT" >}}
```cypher
MATCH (p:person {name: 'Christopher Nolan'})-[:directed]->(m:movie)
RETURN m
NEXT
MATCH (a:person)-[:acted_in]->(m)
RETURN m.title AS film, a.name AS actor ORDER BY film;
```
{{< /tab >}}
{{< tab label="Cypher — WITH" >}}
```cypher
MATCH (p:person {name: 'Christopher Nolan'})-[:directed]->(m:movie)
WITH m
MATCH (a:person)-[:acted_in]->(m)
RETURN m.title AS film, a.name AS actor ORDER BY film;
```
{{< /tab >}}
{{< /tabs >}}
```
      film      |         actor
----------------+-----------------------
 "Inception"    | "Leonardo DiCaprio"
 "Interstellar" | "Matthew McConaughey"
(2 rows)
```

`m` crosses the boundary as a vertex, so the second query re-traverses from it.

### Filter an aggregate computed by the first query {#filter-an-aggregate-computed-by-the-first-query}

`FILTER` cannot open a standalone query, but it can open the query after `NEXT`.
That gives an aggregate a `HAVING`-style filter without an extra `WITH`:

```cypher
MATCH (p:person)-[:acted_in]->(m:movie)
RETURN p.name AS actor, count(m) AS films
NEXT
FILTER films > 2
RETURN actor, films ORDER BY actor;
```

```
          actor          | films
-------------------------+-------
 "Arnold Schwarzenegger" | 3
 "Keanu Reeves"          | 4
(2 rows)
```

### Chain three queries {#chain-three-queries}

Each `NEXT` is another boundary, evaluated left to right:

```cypher
MATCH (m:movie) RETURN m.genre AS genre
NEXT
RETURN DISTINCT genre AS g
NEXT
RETURN count(g) AS genres;
```

```
 genres
--------
 3
(1 row)
```

### Reach a variable the first query did not return {#reach-a-variable-the-first-query-did-not-return}

Only returned columns survive the boundary, so a reference to anything else fails
at parse time:

```cypher
MATCH (p:person {name: 'Christopher Nolan'})-[:directed]->(m:movie)
RETURN m
NEXT
RETURN p.name;
```

```
ERROR:  variable does not exist
LINE 4: RETURN p.name;
               ^
```

## Notes {#notes}

`NEXT` costs nothing at run time. The boundary is built by rewriting the left
query's `RETURN` into the `WITH` the clause pipeline already places between clause
groups. The two tab-set queries above therefore plan identically.

Two guards report the misuse directly rather than as a syntax error. A left query
that does not end with `RETURN` raises `a query statement before NEXT must end
with RETURN`. A left query ending in `FINISH` raises
`FINISH cannot be followed by NEXT`.

The last query in a chain still has to end the statement properly. `ORDER BY`,
`SKIP`, `OFFSET` and `LIMIT` are clauses in their own right, but none of them can
terminate a query. A chain that stops on one raises `Cypher query must end with
RETURN, FINISH or update clause`. Follow it with `RETURN` or `FINISH`.

`next` is an unreserved keyword, so it remains usable as a variable, label or
property name.

## Compatibility {#compatibility}

> [!NOTE] GQL conformance
> :class: gql-conformance
>
> Implements the GQL `<next statement>` of the *procedure body* (ISO/IEC 39075:2024
> §9.2), Feature GQ20, "Advanced linear composition with NEXT".
>
> - **Supported** — chaining query statements, left-associative multi-chaining, the
>   scope reset at the boundary, and a set-operation composite on either side.
> - **Not supported** — the optional `YIELD` clause the standard allows between
>   `NEXT` and the following statement (`NEXT YIELD a, b …`), which raises a syntax
>   error. Project and rename in the preceding `RETURN` instead.
>
> Track status in the [GQL conformance matrix](/agensgraph/appendix/gql-conformance/).

### openCypher {#opencypher}

openCypher has no `NEXT`. Composition there is always the `WITH` form shown in the
tab set above, which AgensGraph accepts unchanged.

## See also {#see-also}

- [`WITH`](/agensgraph/reference/clauses/with/) — the Cypher analogue, inside one query
- [`LET`](/agensgraph/reference/clauses/let/) **GQL** — add columns without a boundary
- [`FILTER`](/agensgraph/reference/clauses/filter/) **GQL** — the clause `NEXT` makes available first
- [`FINISH`](/agensgraph/reference/clauses/finish/) **GQL**
- [`RETURN`](/agensgraph/reference/clauses/return/) — what the left query has to end with
- [GQL conformance matrix](/agensgraph/appendix/gql-conformance/)
