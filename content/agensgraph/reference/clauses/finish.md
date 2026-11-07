---
title: FINISH
linkTitle: FINISH
description: 'Ends a query without projecting anything: the work runs, and the query returns an empty result.'
type: docs
weight: 200
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/finish.html
upstream_source: agensgraph
upstream_modified: true
---


**GQL clause**  **Added in 2.18**

Ends a query without projecting anything: the work runs, and the query returns an
empty result.

## Synopsis {#synopsis}

```text
FINISH
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

Every query has to end with `RETURN`, `FINISH` or a write clause. `FINISH` is the
ending that says "produce no result": it takes no arguments, projects no columns
and closes the statement.

- `FINISH` must be the **last** clause. Anything after it raises `FINISH must be at
  the end of the query`.
- After a read, `FINISH` discards the rows. The planner applies it as `LIMIT 0`, so
  the scan is opened but no row is fetched.
- After a write, the write still happens. `FINISH` only suppresses the projection.
- A query ending in `FINISH` returns an **empty result**: no columns and no rows.
  `psql` prints it as a `--` header followed by `(0 rows)`, and `\gdesc` reports
  `The command has no result, or the result has no columns.`
- A write that ends in `FINISH` reports its ordinary command tag instead of a
  result, such as `UPDATE 1` for one created vertex.

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).

Run a read for its plan and nothing else. There is no Cypher spelling of this. A
Cypher query with no `RETURN` and no write clause is rejected:

```cypher
MATCH (m:movie) FINISH;
```

```
--
(0 rows)
```

### Perform a write without reading the result back {#perform-a-write-without-reading-the-result-back}

`CREATE … FINISH` is the form to reach for when you do not want the created
elements shipped to the client:

```cypher
CREATE (:movie {title: 'Tenet', year: 2020, genre: 'Action'}) FINISH;
```

```
UPDATE 1
```

The vertex is there:

```cypher
MATCH (m:movie {title: 'Tenet'}) RETURN m.title AS film, m.year AS year;
```

```
  film   | year
---------+------
 "Tenet" | 2020
(1 row)
```

### Confirm that a read costs nothing after FINISH {#confirm-that-a-read-costs-nothing-after-finish}

The plan shows the `LIMIT 0` the clause compiles to, above the scan it never
draws from:

```cypher
EXPLAIN (COSTS OFF) MATCH (m:movie) FINISH;
```

```
        QUERY PLAN
---------------------------
 Limit
   ->  Seq Scan on movie m
(2 rows)
```

A write plan keeps its write node, because the write is not optional:

```cypher
EXPLAIN (COSTS OFF) CREATE (:movie {title: 'Tenet'}) FINISH;
```

```
  QUERY PLAN
--------------
 Graph Create
   ->  Result
(2 rows)
```

### End a sorted query that projects nothing {#end-a-sorted-query-that-projects-nothing}

`ORDER BY`, `SKIP`, `OFFSET` and `LIMIT` are clauses in their own right, but none
of them can end a query. `FINISH` closes a pipeline that ends on one:

```cypher
MATCH (m:movie) ORDER BY m.year LIMIT 3 FINISH;
```

```
--
(0 rows)
```

Without the `FINISH` the same query raises `Cypher query must end with RETURN,
FINISH or update clause`.

## Notes {#notes}

`FINISH` is not accepted where a result is required. A `CALL { }` body must
project something, so a body ending in `FINISH` raises
`CALL subquery must RETURN at least one variable`. A query ending in `FINISH`
cannot be the left operand of [`NEXT`](/agensgraph/reference/clauses/next/) either. That raises
`FINISH cannot be followed by NEXT`.

> [!NOTE]
> `finish` became a reserved keyword in 2.18. It is still accepted unquoted as a
> label name in a pattern, `MATCH (n:finish)`, which is what an upgraded database
> needs. It is not accepted as a variable name, a `CREATE VLABEL` name or a SQL
> identifier; write `"finish"` there, or rename. Property keys and `RETURN` aliases
> are unaffected.

## Compatibility {#compatibility}

> [!NOTE] GQL conformance
> :class: gql-conformance
>
> Implements `FINISH` of the GQL *primitive result statement* (ISO/IEC 39075:2024
> §14.10). The standard specifies that `FINISH` has "the empty type" and sets the
> execution outcome to "a successful outcome with an omitted result", which is what
> the empty, column-less result above represents.
>
> - **Supported** — `FINISH` as the terminal statement of a read query and of a
>   data-modifying query, in which case the standard makes it implicit anyway
>   (§13.1).
> - **Not supported** — `FINISH` as a branch of a set operation, which the standard
>   also forbids (§14.2, Syntax Rule 5). AgensGraph rejects it as a column-count
>   mismatch: `each UNION query must have the same number of columns`.
>
> Track status in the [GQL conformance matrix](/agensgraph/appendix/gql-conformance/).

### openCypher {#opencypher}

openCypher has no `FINISH`. There, a read query must end with `RETURN`, and a write
query may end with its write clause. AgensGraph accepts that second form too, so
`FINISH` adds the read case rather than replacing anything.

## See also {#see-also}

- [`RETURN`](/agensgraph/reference/clauses/return/) — the other way to end a query
- [`ORDER BY`](/agensgraph/reference/clauses/order-by/) and [`SKIP` and `LIMIT`](/agensgraph/reference/clauses/skip-and-limit/) — clauses that need a terminator
- [`NEXT`](/agensgraph/reference/clauses/next/) **GQL** — the one clause `FINISH` may not precede
- [`INSERT`](/agensgraph/reference/clauses/insert/) **GQL** — a write worth ending with `FINISH`
- [GQL conformance matrix](/agensgraph/appendix/gql-conformance/)
