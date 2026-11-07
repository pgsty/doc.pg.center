---
title: ORDER BY
linkTitle: ORDER BY
description: Sorts the working rows.
type: docs
weight: 80
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/order-by.html
upstream_source: agensgraph
upstream_modified: true
---


**GQL clause**

Sorts the working rows. It is a clause of its own, so it can sort anywhere in a
pipeline, not only at the end.

## Synopsis {#synopsis}

```text
ORDER BY sort_key [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [, ...]
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`ORDER BY` sorts the rows currently in the pipeline. It is written after the
clause whose rows it sorts, and it applies to that clause's output. That clause
is a [`RETURN`](/agensgraph/reference/clauses/return/), a [`WITH`](/agensgraph/reference/clauses/with/) or a [`MATCH`](/agensgraph/reference/clauses/match/).

- Rows are compared by the first sort key; ties go to the next, and so on.
- Each key sorts ascending unless you write `DESC`. `ASC` is the explicit
  default.
- Nulls sort **last** under `ASC` and **first** under `DESC`, unless
  `NULLS FIRST` or `NULLS LAST` says otherwise.
- A sort key is an expression, not a column number. `ORDER BY 2` sorts by the
  constant 2, which orders nothing. See [Compatibility](#compatibility).
- `ORDER BY` cannot **lead** a query and cannot **end** one.
- After `RETURN DISTINCT`, every sort key has to appear in the projection.

It is a standalone clause, so it can also sort in the middle of a pipeline. A
[`LIMIT`](/agensgraph/reference/clauses/skip-and-limit/) usually follows, to cut the rows a later clause has
to process.

## Parameters {#parameters}

sort_key
: An expression over the bindings in scope. After a `RETURN` or `WITH` this
  includes that clause's aliases; it may also be an expression that was not
  projected at all.

ASC, DESC
: Ascending or descending. `ASC` is the default.

NULLS FIRST, NULLS LAST
: Where null values go. The default is `NULLS LAST` for an ascending key and
  `NULLS FIRST` for a descending one.

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).

### Sort by a projected column {#sort-by-a-projected-column}

```cypher
MATCH (m:movie) WHERE m.year > 2015
RETURN m.title AS film, m.year AS year
ORDER BY year;
```

```
            film            | year
----------------------------+------
 "Blade Runner 2049"        | 2017
 "The Matrix Resurrections" | 2021
(2 rows)
```

### Sort by something you did not project {#sort-by-something-you-did-not-project}

The sort key is an ordinary expression, so it need not be a result column:

```cypher
MATCH (m:movie)
RETURN m.title AS film
ORDER BY m.year
LIMIT 3;
```

```
       film
------------------
 "Blade Runner"
 "The Terminator"
 "Total Recall"
(3 rows)
```

```cypher
MATCH (p:person)
RETURN p.name AS person
ORDER BY length(p.name) DESC
LIMIT 3;
```

```
         person
-------------------------
 "Arnold Schwarzenegger"
 "Matthew McConaughey"
 "Laurence Fishburne"
(3 rows)
```

### Sort by several keys, in different directions {#sort-by-several-keys-in-different-directions}

```cypher
MATCH (m:movie)
RETURN m.genre AS genre, m.year AS year, m.title AS film
ORDER BY genre, year DESC
LIMIT 5;
```

```
  genre   | year |            film
----------+------+----------------------------
 "Action" | 2021 | "The Matrix Resurrections"
 "Action" | 2012 | "The Avengers"
 "Action" | 2003 | "The Matrix Reloaded"
 "Action" | 2003 | "The Matrix Revolutions"
 "Action" | 1999 | "The Matrix"
(5 rows)
```

`genre` ascending, `year` descending within each genre.

### Place the nulls {#place-the-nulls}

An `OPTIONAL MATCH` leaves nulls behind, which makes the default visible.
Ascending puts them last:

```cypher
MATCH (p:person) WHERE p.born > 1974
OPTIONAL MATCH (p)-[:directed]->(m:movie)
RETURN p.name AS person, m.title AS directed
ORDER BY directed;
```

```
      person       | directed
-------------------+-----------
 "Neill Blomkamp"  | "Elysium"
 "Ryan Gosling"    |
 "Sam Worthington" |
(3 rows)
```

Descending puts them first:

```cypher
MATCH (p:person) WHERE p.born > 1974
OPTIONAL MATCH (p)-[:directed]->(m:movie)
RETURN p.name AS person, m.title AS directed
ORDER BY directed DESC;
```

```
      person       | directed
-------------------+-----------
 "Ryan Gosling"    |
 "Sam Worthington" |
 "Neill Blomkamp"  | "Elysium"
(3 rows)
```

`NULLS FIRST` asks for that placement without reversing the sort:

```cypher
MATCH (p:person) WHERE p.born > 1974
OPTIONAL MATCH (p)-[:directed]->(m:movie)
RETURN p.name AS person, m.title AS directed
ORDER BY directed NULLS FIRST;
```

```
      person       | directed
-------------------+-----------
 "Ryan Gosling"    |
 "Sam Worthington" |
 "Neill Blomkamp"  | "Elysium"
(3 rows)
```

### Sort in the middle of a pipeline {#sort-in-the-middle-of-a-pipeline}

`ORDER BY` after a `MATCH`, with a `LIMIT`, narrows what the rest of the query
sees:

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

The second `MATCH` runs against two rows, not eighteen.

### Where ORDER BY cannot go {#where-order-by-cannot-go}

It cannot open a query:

```cypher
ORDER BY 1;
```

```
ERROR:  syntax error at or near "ORDER"
LINE 1: ORDER BY 1;
        ^
```

And it cannot close one, because a sort produces no result on its own:

```cypher
MATCH (m:movie) ORDER BY m.title;
```

```
ERROR:  Cypher query must end with RETURN, FINISH or update clause
```

## Notes {#notes}

Sorting a property sorts a jsonb value. jsonb orders by type before value: a
number sorts above every string, and both above null. So a key whose values have
mixed types groups by type first. Cast the key when the stored types are mixed
and you want one ordering across them.

## Compatibility {#compatibility}

### A number is a sort key, not a column reference {#a-number-is-a-sort-key-not-a-column-reference}

In SQL, `ORDER BY 2` sorts by the second output column. Here the sort key is a
value expression, so the integer is a constant: every row compares equal, nothing
is reordered, and no error is raised.

```cypher
MATCH (m:movie) WHERE m.year > 2015
RETURN m.title AS film, m.year AS year
ORDER BY 2;
```

```
            film            | year
----------------------------+------
 "The Matrix Resurrections" | 2021
 "Blade Runner 2049"        | 2017
(2 rows)
```

The rows come back in scan order, not by year. Naming the key sorts correctly, as
the first example on this page shows. This follows ISO/IEC 39075 §16.17, whose
`<sort key>` is an `<aggregating value expression>` with no ordinal form; the
deviation is from SQL. Always name the sort key.

### ASCENDING and DESCENDING (ISO/IEC 39075 §16.17) {#ascending-and-descending-isoiec-39075-1617}

The standard accepts `ASCENDING` and `DESCENDING` alongside `ASC` and `DESC`.
AgensGraph accepts only the short spellings; `ORDER BY film ASCENDING` is a
syntax error.

## See also {#see-also}

- [`SKIP` and `LIMIT`](/agensgraph/reference/clauses/skip-and-limit/) — the paging clauses that usually follow a sort
- [`RETURN`](/agensgraph/reference/clauses/return/), [`WITH`](/agensgraph/reference/clauses/with/) — the projections a sort applies to
- [`MATCH`](/agensgraph/reference/clauses/match/) — sorting mid-pipeline to cut work
