---
title: SKIP and LIMIT
linkTitle: SKIP and LIMIT
description: 'Pages the working rows: SKIP discards rows from the front, LIMIT caps how many are kept.'
type: docs
weight: 90
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/skip-and-limit.html
upstream_source: agensgraph
upstream_modified: true
---


**GQL clause**

Pages the working rows: `SKIP` discards rows from the front, `LIMIT` caps how
many are kept. `OFFSET` is a synonym for `SKIP`.

## Synopsis {#synopsis}

```text
{ SKIP | OFFSET } count
```

```text
LIMIT count
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`SKIP` and `LIMIT` are clauses of their own, so either can page the rows
anywhere in a pipeline. Write one after a [`RETURN`](/agensgraph/reference/clauses/return/) or a
[`WITH`](/agensgraph/reference/clauses/with/), or straight after a [`MATCH`](/agensgraph/reference/clauses/match/). Each may be used
without the other.

- `SKIP` **and** `OFFSET` are the same clause. Use whichever spelling you
  prefer; `OFFSET` is the one ISO/IEC 39075 lists first.
- *count* is an expression, not just a literal, and is evaluated once.
- A negative count is an error. A count larger than the number of rows is not:
  `SKIP` past the end gives no rows, and `LIMIT` beyond the end gives all of
  them.
- A fractional count is rounded to the nearest integer.
- Neither clause can **lead** a query, and neither can end one on its own. A
  query still has to finish with `RETURN`, `FINISH` or a write clause.
- Without an [`ORDER BY`](/agensgraph/reference/clauses/order-by/), which rows you get is not defined. Sort
  first whenever the page has to be stable.
- Written after a projection, the modifiers have to be in the order
  `ORDER BY`, `SKIP`/`OFFSET`, `LIMIT`. See [Notes](#notes).

## Parameters {#parameters}

count
: A non-negative integer expression. `SKIP` discards that many leading rows;
  `LIMIT` keeps at most that many.

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).

### Take the first few rows {#take-the-first-few-rows}

```cypher
MATCH (m:movie)
RETURN m.title AS film
ORDER BY film
LIMIT 2;
```

```
      film
----------------
 "Avatar"
 "Blade Runner"
(2 rows)
```

### Take a page from the middle {#take-a-page-from-the-middle}

```cypher
MATCH (m:movie)
RETURN m.title AS film
ORDER BY film
SKIP 2
LIMIT 3;
```

```
        film
---------------------
 "Blade Runner 2049"
 "Elysium"
 "Gattaca"
(3 rows)
```

`OFFSET` reads the same:

```cypher
MATCH (m:movie)
RETURN m.title AS film
ORDER BY film
OFFSET 2
LIMIT 3;
```

```
        film
---------------------
 "Blade Runner 2049"
 "Elysium"
 "Gattaca"
(3 rows)
```

### Compute the count {#compute-the-count}

Any expression will do:

```cypher
MATCH (m:movie)
RETURN m.title AS film
ORDER BY film
SKIP 1+1
LIMIT 2;
```

```
        film
---------------------
 "Blade Runner 2049"
 "Elysium"
(2 rows)
```

A fraction rounds. `LIMIT 1.5` keeps two rows:

```cypher
MATCH (m:movie)
RETURN m.title AS film
ORDER BY film
LIMIT 1.5;
```

```
      film
----------------
 "Avatar"
 "Blade Runner"
(2 rows)
```

### Page past the end {#page-past-the-end}

```cypher
MATCH (m:movie)
RETURN m.title AS film
ORDER BY film
SKIP 20;
```

```
 film
------
(0 rows)
```

There are 18 films, so nothing is left. A `LIMIT 100` on the same query returns
all 18 rather than failing.

### Cut the pipeline down mid-query {#cut-the-pipeline-down-mid-query}

`LIMIT` after a `MATCH` reduces the rows a later clause has to join:

```cypher
MATCH (m:movie)
ORDER BY m.year DESC LIMIT 2
MATCH (p:person)-[:directed]->(m)
RETURN m.title AS film, p.name AS director
ORDER BY film;
```

```
            film            |      director
----------------------------+--------------------
 "Blade Runner 2049"        | "Denis Villeneuve"
 "The Matrix Resurrections" | "Lana Wachowski"
(2 rows)
```

### Reject a negative count {#reject-a-negative-count}

```cypher
MATCH (m:movie) RETURN m.title AS film ORDER BY film LIMIT -1;
```

```
ERROR:  LIMIT must not be negative
```

```cypher
MATCH (m:movie) RETURN m.title AS film ORDER BY film SKIP -1;
```

```
ERROR:  OFFSET must not be negative
```

`SKIP` reports itself as `OFFSET` because the two are one clause.

### Where they cannot go {#where-they-cannot-go}

Neither clause can open a query:

```cypher
LIMIT 3;
```

```
ERROR:  syntax error at or near "LIMIT"
LINE 1: LIMIT 3;
        ^
```

And neither closes one:

```cypher
MATCH (m:movie) LIMIT 3;
```

```
ERROR:  Cypher query must end with RETURN, FINISH or update clause
```

## Notes {#notes}

After a projection, write the modifiers in the order `ORDER BY`, then
`SKIP`/`OFFSET`, then `LIMIT`. Only that order folds into the projection. Put
`LIMIT` before `SKIP` and the trailing `SKIP` is read as a clause of its own, so
the query no longer ends on a projection. That is what the error reports:

```cypher
MATCH (m:movie) RETURN m.title AS film ORDER BY film LIMIT 3 SKIP 2;
```

```
ERROR:  Cypher query must end with RETURN, FINISH or update clause
```

Mid-pipeline both orders parse, and they mean different things. Each clause
applies to the rows the one before it produced. Skipping first takes rows three
to six:

```cypher
MATCH (m:movie) ORDER BY m.title SKIP 2 LIMIT 4 RETURN m.title AS film;
```

```
        film
---------------------
 "Blade Runner 2049"
 "Elysium"
 "Gattaca"
 "Inception"
(4 rows)
```

Limiting first cuts to four rows and then skips two of them, leaving two:

```cypher
MATCH (m:movie) ORDER BY m.title LIMIT 4 SKIP 2 RETURN m.title AS film;
```

```
        film
---------------------
 "Blade Runner 2049"
 "Elysium"
(2 rows)
```

## Compatibility {#compatibility}

### SKIP and OFFSET (ISO/IEC 39075 §16.19) {#skip-and-offset-isoiec-39075-1619}

The standard's `<offset synonym>` is `OFFSET | SKIP`, so both spellings conform.
openCypher has only `SKIP`.

## See also {#see-also}

- [`ORDER BY`](/agensgraph/reference/clauses/order-by/) — sort first, so a page is reproducible
- [`RETURN`](/agensgraph/reference/clauses/return/), [`WITH`](/agensgraph/reference/clauses/with/) — the projections these clauses page
- [`MATCH`](/agensgraph/reference/clauses/match/) — paging mid-pipeline to cut work
