---
title: WITH
linkTitle: WITH
description: Projects the working rows into a new set of columns and passes them to the next clause.
type: docs
weight: 60
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/with.html
upstream_source: agensgraph
upstream_modified: true
---


Projects the working rows into a new set of columns and passes them to the next
clause. It is a `RETURN` in the middle of a pipeline.

## Synopsis {#synopsis}

```text
WITH [ DISTINCT | ALL ] { * | expression [ AS alias ] } [, ...] [ WHERE condition ]
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`WITH` closes one section of a pipeline and opens the next. It evaluates its
expressions per row exactly as [`RETURN`](/agensgraph/reference/clauses/return/) does, then hands the
resulting columns to the clause that follows. Three jobs need it:

- **Aggregating, then filtering or matching further.** An aggregate cannot appear
  in a `WHERE`, so aggregate in a `WITH` and filter its output.
- **Computing a value once** and using it in several later clauses.
- **Cutting the pipeline down** with `DISTINCT`, `ORDER BY` and `LIMIT` before
  the expensive part of a query runs.

Rules that follow from it being a projection:

- `WITH` **replaces** the scope. Only what it projects survives; a variable it
  omits is gone, and mentioning it later raises `variable does not exist`. Write
  `WITH *, expr AS v`, or use [`LET`](/agensgraph/reference/clauses/let/), to add without dropping.
- Each output name must be **unique within the clause**. Projecting the same name
  twice raises `WITH passes on "..." more than once`. `RETURN` has no such rule.
- Its `WHERE` runs **after** the projection and after any aggregation, so it can
  test an aggregate's alias.
- `ORDER BY`, `SKIP`/`OFFSET` and `LIMIT` are separate clauses that follow the
  `WITH`, and therefore follow its `WHERE` too. The filter runs first, and the
  paging applies to what survives.
- `WITH` cannot **lead** a query and cannot end one. At the start of a statement
  `WITH` is SQL's common table expression, which is a different clause taking a name
  and a parenthesised query. [`LET`](/agensgraph/reference/clauses/let/) has no such collision and may lead.

## Parameters {#parameters}

DISTINCT
: Removes duplicate rows from the projection before passing them on.

ALL
: Keeps duplicate rows. This is the default.

\*
: Carries every named binding in scope through unchanged. Combine it with further
  items, as in `WITH *, expr AS v`, to add columns without dropping any.

expression
: Any Cypher expression over the bindings in scope, including an aggregate.

alias
: The name the next clause uses. Required for anything that is not a plain
  variable reference, because the following clauses have to be able to name it.

condition
: A boolean expression filtering the projected rows. Evaluated after the
  projection, so it can reference an alias defined in this clause.

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).

### Filter on a count {#filter-on-a-count}

```cypher
MATCH (p:person)-[:acted_in]->(m:movie)
WITH p.name AS actor, count(m) AS films
WHERE films > 1
RETURN actor, films
ORDER BY films DESC, actor;
```

```
          actor          | films
-------------------------+-------
 "Keanu Reeves"          | 4
 "Arnold Schwarzenegger" | 3
 "Carrie-Anne Moss"      | 2
 "Harrison Ford"         | 2
 "Laurence Fishburne"    | 2
 "Linda Hamilton"        | 2
(6 rows)
```

`count(m)` groups by `p.name`, and the `WHERE` tests the resulting `films`. The
same condition in a `MATCH ... WHERE` would be refused with
`aggregate functions are not allowed in WHERE`.

### Add a column without losing the others {#add-a-column-without-losing-the-others}

```cypher
MATCH (p:person)-[:directed]->(m:movie)
WITH *, m.year - p.born AS age_at_release
RETURN p.name AS director, m.title AS film, age_at_release
ORDER BY age_at_release
LIMIT 3;
```

```
     director      |       film       | age_at_release
-------------------+------------------+----------------
 "James Cameron"   | "The Terminator" | 30
 "Lilly Wachowski" | "The Matrix"     | 32
 "Andrew Niccol"   | "Gattaca"        | 33
(3 rows)
```

`WITH *` keeps `p` and `m` in scope so `RETURN` can still read their properties.
[`LET`](/agensgraph/reference/clauses/let/) does the same thing without the `*`.

### Watch what a WITH drops {#watch-what-a-with-drops}

Anything the projection omits is out of scope afterwards:

```cypher
MATCH (p:person)-[:acted_in]->(m:movie)
WITH m
RETURN p.name;
```

```
ERROR:  variable does not exist
LINE 1: ...ATCH (p:person)-[:acted_in]->(m:movie) WITH m RETURN p.name;
                                                                ^
```

### Deduplicate mid-pipeline {#deduplicate-mid-pipeline}

```cypher
MATCH (p:person)-[:acted_in]->(m:movie)
WITH DISTINCT m.genre AS genre
RETURN genre
ORDER BY genre;
```

```
    genre
-------------
 "Action"
 "Adventure"
 "Sci-Fi"
(3 rows)
```

### Cut the pipeline down before matching further {#cut-the-pipeline-down-before-matching-further}

`ORDER BY` and `LIMIT` after a `WITH` reduce the rows the next clause has to
work on:

```cypher
MATCH (m:movie)
WITH m ORDER BY m.year DESC LIMIT 2
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

Only the two newest films reach the second `MATCH`.

### See that paging follows the filter {#see-that-paging-follows-the-filter}

`WHERE` belongs to the `WITH`; `ORDER BY` and `LIMIT` are the clauses after it.
So the `LIMIT` counts rows that passed the filter:

```cypher
MATCH (m:movie)
WITH m.title AS film, m.genre AS genre WHERE genre = 'Action'
ORDER BY film LIMIT 3
RETURN film, genre;
```

```
             film             |  genre
------------------------------+----------
 "Terminator 2: Judgment Day" | "Action"
 "The Avengers"               | "Action"
 "The Matrix"                 | "Action"
(3 rows)
```

Drop the filter and the same paging picks entirely different rows, because now
the first three by title are the ones it keeps:

```cypher
MATCH (m:movie)
WITH m.title AS film, m.genre AS genre
ORDER BY film LIMIT 3
RETURN film, genre;
```

```
        film         |  genre
---------------------+----------
 "Avatar"            | "Sci-Fi"
 "Blade Runner"      | "Sci-Fi"
 "Blade Runner 2049" | "Sci-Fi"
(3 rows)
```

### Reject a repeated output name {#reject-a-repeated-output-name}

```cypher
MATCH (m:movie)
WITH m.title AS film, m.genre AS film
RETURN film;
```

```
ERROR:  WITH passes on "film" more than once
LINE 1: MATCH (m:movie) WITH m.title AS film, m.genre AS film RETURN...
                                              ^
```

Carrying a variable and then aliasing something else to its name collides the
same way: `WITH m, m.title AS m` raises `WITH passes on "m" more than once`.

## Notes {#notes}

`WHERE` has to be written directly after the projection list, before any
`ORDER BY`, `SKIP` or `LIMIT`. Putting it later is a syntax error:
`WITH ... ORDER BY film WHERE genre = 'Action'` does not parse.

## See also {#see-also}

- [`RETURN`](/agensgraph/reference/clauses/return/) — the same projection, ending the query
- [`LET`](/agensgraph/reference/clauses/let/) **GQL** — add bindings without dropping any
- [`WHERE`](/agensgraph/reference/clauses/where/) — the condition a `WITH` can carry
- [`ORDER BY`](/agensgraph/reference/clauses/order-by/), [`SKIP` and `LIMIT`](/agensgraph/reference/clauses/skip-and-limit/) — the clauses that follow a `WITH`
- [`UNWIND`](/agensgraph/reference/clauses/unwind/) — the usual partner for undoing a `collect()`
