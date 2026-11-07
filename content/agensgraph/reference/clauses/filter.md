---
title: FILTER
linkTitle: FILTER
description: Keeps only the rows that satisfy a condition.
type: docs
weight: 180
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/filter.html
upstream_source: agensgraph
upstream_modified: true
---


**GQL clause**  **Added in 2.18**

Keeps only the rows that satisfy a condition. It is a standalone filter that
needs no projection, unlike Cypher's `WITH … WHERE`.

## Synopsis {#synopsis}

```text
FILTER [ WHERE ] condition
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`FILTER` discards every row whose condition is not true, and changes nothing else:
the columns in scope before it are exactly the columns in scope after it. The
optional `WHERE` is noise words. `FILTER x > 1` and `FILTER WHERE x > 1` parse to
the same clause.

- `FILTER` is a **middle** clause. It cannot open a query and it cannot end one.
- It applies to whatever the preceding clause produced, including the output of an
  aggregating `WITH`. It is therefore the `HAVING` of a Cypher pipeline.
- Chained `FILTER`s apply in order, each narrowing the rows the last one kept.
- A row whose condition evaluates to null is discarded, as in SQL.

## Parameters {#parameters}

condition
: A predicate over the variables in scope. Any boolean expression `WHERE` accepts,
  including a [subquery value expression](/agensgraph/reference/clauses/subquery-expressions/) such as
  `EXISTS { }` or `COUNT { }`. The condition must be a boolean: a bare number is
  rejected with `argument of FILTER must be type boolean, not type integer`, and a
  bare property with `cannot cast 2003 (jsonb type numeric) to boolean`.

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).

Keep the films from 2014 onwards. `FILTER` after a pattern and Cypher's `WHERE`
attached to it are the same test. Switch tabs to compare:

{{< tabs >}}
{{< tab label="GQL — FILTER" >}}
```cypher
MATCH (m:movie)
FILTER m.year >= 2014
RETURN m.title AS film, m.year AS year ORDER BY year;
```
{{< /tab >}}
{{< tab label="Cypher — WHERE" >}}
```cypher
MATCH (m:movie)
WHERE m.year >= 2014
RETURN m.title AS film, m.year AS year ORDER BY year;
```
{{< /tab >}}
{{< /tabs >}}
```
            film            | year
----------------------------+------
 "Interstellar"             | 2014
 "Blade Runner 2049"        | 2017
 "The Matrix Resurrections" | 2021
(3 rows)
```

Both forms plan identically, down to the same
`Filter: (properties.'year' >= '2014'::jsonb)` on the scan of `movie`.

### Filter an aggregate {#filter-an-aggregate}

`WHERE` cannot follow an aggregating `RETURN`, and attaching it to `WITH` forces
you to restate the projection. `FILTER` tests the aggregate directly:

```cypher
MATCH (p:person)-[:acted_in]->(m:movie)
WITH p.name AS actor, count(m) AS films
FILTER films >= 3
RETURN actor, films ORDER BY actor;
```

```
          actor          | films
-------------------------+-------
 "Arnold Schwarzenegger" | 3
 "Keanu Reeves"          | 4
(2 rows)
```

### Narrow rows in two stages {#narrow-rows-in-two-stages}

Each `FILTER` sees only the rows the one before it kept:

```cypher
MATCH (m:movie)
FILTER m.genre = 'Sci-Fi'
FILTER m.year < 1998
RETURN m.title AS film ORDER BY film;
```

```
        film
---------------------
 "Blade Runner"
 "Gattaca"
 "The Fifth Element"
 "Total Recall"
(4 rows)
```

### Filter the rows a write clause produced {#filter-the-rows-a-write-clause-produced}

A `FILTER` after a write runs the write first, then restricts the rows that flow
on. Here `SET` touches the film and `FILTER` decides whether the row is reported:

```cypher
MATCH (m:movie {title: 'The Matrix'})
SET m.reviewed = true
FILTER m.year = 1999
RETURN m.title AS film, m.reviewed AS reviewed;
```

```
     film     | reviewed
--------------+----------
 "The Matrix" | true
(1 row)
```

## Notes {#notes}

Because `FILTER` cannot open a query, a statement that begins with it is a syntax
error rather than a clause-placement error:

```cypher
FILTER true;
```

```
ERROR:  syntax error at or near "FILTER"
LINE 1: FILTER true;
        ^
```

The one place `FILTER` does come first is after [`NEXT`](/agensgraph/reference/clauses/next/), where it
operates on the table carried across the boundary. Ending a query on `FILTER`
raises `Cypher query must end with RETURN, FINISH or update clause`.

`filter` is an unreserved keyword, so it remains usable as a variable, label or
property name.

## Compatibility {#compatibility}

> [!NOTE] GQL conformance
> :class: gql-conformance
>
> Implements the GQL *FILTER statement* (ISO/IEC 39075:2024 §14.6), Feature GQ08,
> "FILTER statement".
>
> - **Supported** — both spellings the standard defines, `FILTER <search condition>`
>   and `FILTER WHERE <search condition>`, in every non-leading, non-terminal
>   position.
> - **Not supported** — nothing in the subclause. `FILTER` is complete.
>
> Track status in the [GQL conformance matrix](/agensgraph/appendix/gql-conformance/).

### openCypher {#opencypher}

openCypher has no `FILTER` statement; the equivalent is a `WHERE` attached to
`MATCH` or to `WITH`, both of which AgensGraph accepts unchanged. The unrelated
openCypher list function `filter(x IN list WHERE predicate)` is not accepted
either. The `WHERE` inside the parentheses is a syntax error. Write a list
comprehension instead: `[x IN m.embedding WHERE x > 0]`.

## See also {#see-also}

- [`WHERE`](/agensgraph/reference/clauses/where/) — the Cypher analogue, attached to a clause
- [`WITH`](/agensgraph/reference/clauses/with/) — project and filter in one clause
- [`LET`](/agensgraph/reference/clauses/let/) **GQL** — add columns without dropping any
- [`NEXT`](/agensgraph/reference/clauses/next/) **GQL** — the one place `FILTER` may come first
- [Subquery value expressions](/agensgraph/reference/clauses/subquery-expressions/) **GQL** — predicates a `FILTER` can use
- [GQL conformance matrix](/agensgraph/appendix/gql-conformance/)
