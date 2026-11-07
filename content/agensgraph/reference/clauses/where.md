---
title: WHERE
linkTitle: WHERE
description: 'Constrains a pattern or filters a projection: rows for which the condition is not true are dropped.'
type: docs
weight: 30
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/where.html
upstream_source: agensgraph
upstream_modified: true
---


**GQL clause**

Constrains a pattern or filters a projection: rows for which the condition is not
true are dropped.

## Synopsis {#synopsis}

```text
WHERE condition
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`WHERE` is not a clause of its own. It attaches to one of three clauses and takes
its meaning from the one it attaches to:

- On [`MATCH`](/agensgraph/reference/clauses/match/) it is part of the match. Every variable in the pattern is
  bound when the condition runs, and a match that fails it is not produced.
- On [`OPTIONAL MATCH`](/agensgraph/reference/clauses/optional-match/) it is part of the optional match. A row
  that fails the condition is **kept**, with the pattern's variables null.
- On [`WITH`](/agensgraph/reference/clauses/with/) it filters the projected rows, after any aggregation. This
  is where a condition over an aggregate goes.

The condition must be a boolean expression. A value of another type is not
coerced: a jsonb string or number in a condition raises an error rather than
being treated as true. Aggregates are not allowed in a `WHERE`. Put them in a
`WITH` and filter the result.

`WHERE` on its own is a syntax error, and a query cannot end with it. The
standalone, chainable filter is [`FILTER`](/agensgraph/reference/clauses/filter/), which takes both
`FILTER condition` and `FILTER WHERE condition`.

## Parameters {#parameters}

condition
: An expression of type boolean. Combine tests with `AND`, `OR`, `XOR` and `NOT`.

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).

### Compare a property {#compare-a-property}

```cypher
MATCH (m:movie) WHERE m.year > 2015
RETURN m.title AS film, m.year AS year
ORDER BY year, film;
```

```
            film            | year
----------------------------+------
 "Blade Runner 2049"        | 2017
 "The Matrix Resurrections" | 2021
(2 rows)
```

### Combine conditions {#combine-conditions}

```cypher
MATCH (m:movie) WHERE m.genre = 'Action' AND m.year < 1995
RETURN m.title AS film
ORDER BY film;
```

```
             film
------------------------------
 "Terminator 2: Judgment Day"
 "The Terminator"
(2 rows)
```

`XOR` is available alongside `AND`, `OR` and `NOT`:

```cypher
MATCH (m:movie) WHERE m.genre = 'Action' XOR m.year < 1995
RETURN count(*) AS n;
```

```
 n
---
 8
(1 row)
```

### Test a label {#test-a-label}

`label()` returns an element's label as a string, for vertices and edges alike:

```cypher
MATCH (n) WHERE label(n) = 'person'
RETURN count(*) AS n;
```

```
 n
----
 28
(1 row)
```

`IN` over a list of names is how a pattern matches several edge labels, which an
edge pattern cannot express:

```cypher
MATCH (p:person)-[r]->(m:movie)
WHERE label(r) IN ['acted_in', 'directed']
RETURN count(r) AS edges;
```

```
 edges
-------
 46
(1 row)
```

### Match on a substring or a pattern {#match-on-a-substring-or-a-pattern}

`STARTS WITH`, `ENDS WITH` and `CONTAINS` test a string property:

```cypher
MATCH (m:movie) WHERE m.title STARTS WITH 'The Matrix'
RETURN count(*) AS n;
```

```
 n
---
 4
(1 row)
```

```cypher
MATCH (m:movie) WHERE m.title ENDS WITH 'Runner'
RETURN m.title AS film;
```

```
      film
----------------
 "Blade Runner"
(1 row)
```

`=~` matches a POSIX regular expression:

```cypher
MATCH (m:movie) WHERE m.title =~ '^Blade.*'
RETURN m.title AS film
ORDER BY film;
```

```
        film
---------------------
 "Blade Runner"
 "Blade Runner 2049"
(2 rows)
```

Negate with `NOT`; there is no `!~` for a property and no `NOT LIKE`:

```cypher
MATCH (m:movie) WHERE NOT m.title STARTS WITH 'The'
RETURN count(*) AS n;
```

```
 n
----
 11
(1 row)
```

### Test for a missing property {#test-for-a-missing-property}

A property that was never set reads as null, so `IS NULL` is the test for its
absence:

```cypher
MATCH (m:movie) WHERE m.runtime IS NULL
RETURN count(*) AS n;
```

```
 n
----
 18
(1 row)
```

### Test for a pattern {#test-for-a-pattern}

A subquery expression tests whether a pattern exists without binding anything
from it:

```cypher
MATCH (p:person) WHERE EXISTS { MATCH (p)-[:directed]->() }
RETURN p.name AS director
ORDER BY director
LIMIT 4;
```

```
      director
---------------------
 "Andrew Niccol"
 "Christopher Nolan"
 "Denis Villeneuve"
 "James Cameron"
(4 rows)
```

### Filter an aggregate with WITH {#filter-an-aggregate-with-with}

An aggregate in a `WHERE` is refused:

```cypher
MATCH (p:person)-[:acted_in]->(m:movie) WHERE count(m) > 1
RETURN p.name;
```

```
ERROR:  aggregate functions are not allowed in WHERE
```

Aggregate in a `WITH`, then filter the result. The `WITH` clause's own `WHERE`
runs after the grouping:

```cypher
MATCH (p:person)-[:acted_in]->(m:movie)
WITH p, count(m) AS films WHERE films >= 3
RETURN p.name AS actor, films
ORDER BY actor;
```

```
          actor          | films
-------------------------+-------
 "Arnold Schwarzenegger" | 3
 "Keanu Reeves"          | 4
(2 rows)
```

## Notes {#notes}

A property holds a jsonb value, and comparing it to a literal compares jsonb
values. In jsonb ordering a number sorts above every string, so a quoted number
compared against a numeric property is not the comparison you meant:

```cypher
MATCH (m:movie {title: 'The Matrix'})
RETURN m.year > '9999' AS num_gt_str, m.year > 1990 AS num_gt_num;
```

```
 num_gt_str | num_gt_num
------------+------------
 t          | t
(1 row)
```

Write the literal in the property's own type, or cast the property with
`m.year::int > 1990`, when the stored type is not the one you expect.

> [!NOTE]
> `WHERE` takes a boolean and nothing else. `WHERE m.title` raises
> `cannot cast "The Matrix" (jsonb type string) to boolean`, where a language with
> truthiness would treat a non-empty string as true. Compare explicitly, or use
> `IS NOT NULL`.

## Compatibility {#compatibility}

### Labeled predicate (ISO/IEC 39075 §19.9) {#labeled-predicate-isoiec-39075-199}

The standard writes a label test as `n IS LABELED movie`, with `n:movie` as a
shorthand. AgensGraph accepts neither; use `label(n) = 'movie'`.

### Pattern predicates {#pattern-predicates}

A bare pattern is not an expression, so it cannot be used as a predicate:
`WHERE (m)-[:related_to]->(:movie)` is a syntax error, and so is the unlabelled
`WHERE (m)-[]->()`. Wrap it in `EXISTS { MATCH ... }`, which the standard defines
in §19.4 and AgensGraph supports.

### SQL string operators {#sql-string-operators}

`LIKE` and `NOT LIKE` are not part of a Cypher condition.
`WHERE m.title LIKE 'Blade%'` is a syntax error, with or without a cast. Use
`STARTS WITH`, `ENDS WITH`, `CONTAINS` or `=~`. To use the SQL operators, wrap the
Cypher in SQL; see
[combining SQL and Cypher](/agensgraph/querying/combining-sql-and-cypher/).

## See also {#see-also}

- [`MATCH`](/agensgraph/reference/clauses/match/) — the clause `WHERE` most often attaches to
- [`OPTIONAL MATCH`](/agensgraph/reference/clauses/optional-match/) — where a failed condition keeps the row
- [`WITH`](/agensgraph/reference/clauses/with/) — filtering after a projection or an aggregate
- [`FILTER`](/agensgraph/reference/clauses/filter/) — the standalone filter clause
- [Subquery expressions](/agensgraph/reference/clauses/subquery-expressions/) — `EXISTS`, `COUNT`, `COLLECT` and the rest
