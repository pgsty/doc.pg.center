---
title: RETURN
linkTitle: RETURN
description: Ends a query and names the columns of its result.
type: docs
weight: 50
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/return.html
upstream_source: agensgraph
upstream_modified: true
---


**GQL clause**

Ends a query and names the columns of its result.

## Synopsis {#synopsis}

```text
RETURN [ DISTINCT | ALL ] { * | expression [ AS alias ] } [, ...]
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`RETURN` is the terminal projection. It evaluates its expressions once per
working row and emits them as the query's result columns. A read query must end
with `RETURN` or [`FINISH`](/agensgraph/reference/clauses/finish/); a write query may end with either of
those or with the write clause itself.

- **A property-derived column comes back as jsonb.** `RETURN m.title` prints
  `"The Matrix"`, with the quotes, and so does `RETURN m.title::text`. To get a
  plain scalar, wrap the query in SQL. See [Notes](#notes).
- `*` projects every **named** binding in scope. Pattern elements you left
  unnamed are not projected.
- An **aggregate** in the list groups implicitly: the non-aggregated expressions
  become the grouping key, as they would in SQL with a `GROUP BY`.
- `DISTINCT` removes duplicate result rows. `ALL` is the explicit spelling of the
  default and keeps them.
- `ORDER BY`, `SKIP`/`OFFSET` and `LIMIT` are **separate clauses** that follow a
  `RETURN`, not parts of it. They have their own pages,
  [`ORDER BY`](/agensgraph/reference/clauses/order-by/) and [`SKIP` and `LIMIT`](/agensgraph/reference/clauses/skip-and-limit/).
- Unlike [`WITH`](/agensgraph/reference/clauses/with/), `RETURN` allows the same output name twice, because
  nothing downstream has to resolve it.

## Parameters {#parameters}

DISTINCT
: Removes duplicate rows from the result.

ALL
: Keeps duplicate rows. This is the default.

\*
: Projects every named binding currently in scope.

expression
: Any Cypher expression over the bindings in scope. That includes a vertex or
  edge variable, a property reference, a path variable, a function call, an
  aggregate, an arithmetic or `CASE` expression, a list or map constructor, and a
  constant.

alias
: The result column's name. Without double quotes it folds to lower case; quote
  it to keep the case you wrote. With no alias, a property reference takes the
  property's name and anything else becomes `?column?`.

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).

### Return a whole vertex {#return-a-whole-vertex}

```cypher
MATCH (p:person {name: 'Keanu Reeves'})
RETURN p;
```

```
                         p
---------------------------------------------------
 person[4.1]{"born": 1964, "name": "Keanu Reeves"}
(1 row)
```

A vertex prints as `label[id]{properties}`. An edge adds its endpoints:

```cypher
MATCH (:person {name: 'Keanu Reeves'})-[r:acted_in]->(:movie {title: 'The Matrix'})
RETURN r;
```

```
                   r
---------------------------------------
 acted_in[5.1][4.1,3.1]{"role": "Neo"}
(1 row)
```

### Return properties, with and without an alias {#return-properties-with-and-without-an-alias}

```cypher
MATCH (p:person {name: 'Keanu Reeves'})
RETURN p.born;
```

```
 born
------
 1964
(1 row)
```

An unaliased property reference takes the property's name; a computed expression
has no name to take:

```cypher
MATCH (p:person {name: 'Keanu Reeves'})
RETURN p.born + 1;
```

```
 ?column?
----------
 1965
(1 row)
```

An unquoted alias folds to lower case, a quoted one does not:

```cypher
MATCH (p:person {name: 'Keanu Reeves'})
RETURN p.born AS BornIn;
```

```
 bornin
--------
 1964
(1 row)
```

```cypher
MATCH (p:person {name: 'Keanu Reeves'})
RETURN p.born AS "BornIn";
```

```
 BornIn
--------
 1964
(1 row)
```

### Return everything that has a name {#return-everything-that-has-a-name}

```cypher
MATCH (p:person {name: 'Ryan Gosling'})-[r:acted_in]->(m:movie)
RETURN *;
```

```
                         p                          |                   r                   |                                                                                                                                     m
----------------------------------------------------+---------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 person[4.10]{"born": 1980, "name": "Ryan Gosling"} | acted_in[5.13][4.10,3.9]{"role": "K"} | movie[3.9]{"plot": "A new blade runner unearths a long-buried secret that has the potential to plunge what's left of society into chaos.", "year": 2017, "genre": "Sci-Fi", "title": "Blade Runner 2049", "embedding": [0.21560573, -0.07505179, -0.01331814, 0.13403069]}
(1 row)
```

Three columns, one per named element. Had the pattern been written
`(p:person {name: 'Ryan Gosling'})-[:acted_in]->(m:movie)`, `RETURN *` would give
two.

### Remove duplicate rows {#remove-duplicate-rows}

Twenty-five `acted_in` edges point at films of three genres:

```cypher
MATCH (p:person)-[:acted_in]->(m:movie)
RETURN DISTINCT m.genre AS genre
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

Without `DISTINCT` the same query returns 25 rows. `ALL` is the explicit form of
that default.

### Aggregate {#aggregate}

An aggregate with no other expression collapses the whole input to one row:

```cypher
MATCH (m:movie)
RETURN count(*) AS films, min(m.year) AS earliest, max(m.year) AS latest;
```

```
 films | earliest | latest
-------+----------+--------
 18    | 1982     | 2021
(1 row)
```

List any other expression alongside it and that expression becomes the grouping
key:

```cypher
MATCH (p:person)-[:acted_in]->(m:movie)
RETURN m.genre AS genre, count(*) AS roles
ORDER BY genre;
```

```
    genre    | roles
-------------+-------
 "Action"    | 13
 "Adventure" | 1
 "Sci-Fi"    | 11
(3 rows)
```

`collect()` gathers a group into a list:

```cypher
MATCH (p:person)-[:acted_in]->(m:movie {title: 'The Matrix'})
RETURN collect(p.name) AS cast;
```

```
                            cast
------------------------------------------------------------
 ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss"]
(1 row)
```

### Return a constant {#return-a-constant}

`RETURN` needs no pattern in front of it:

```cypher
RETURN 1 + 2 AS sum, 'Hello' AS greeting;
```

```
 sum | greeting
-----+----------
 3   | "Hello"
(1 row)
```

## Notes {#notes}

Because a property-derived column comes back as jsonb, a `RETURN` is a poor
interface for an application that wants native types. Put the Cypher in a
`SELECT` subquery and unbox there. The jsonb operators do it: `->>` reads a key
as text, and `#>> '{}'` extracts a jsonb scalar column as text.

```psql
SELECT d.props ->> 'title' AS film, r.score
FROM (MATCH (p:person)-[:directed]->(m:movie)
      WHERE p.name = 'Christopher Nolan'
      RETURN properties(m) AS props) d
JOIN rating r ON r.title = d.props ->> 'title'
WHERE r.source = 'critics'
ORDER BY r.score DESC;
```

```
     film     | score
--------------+-------
 Inception    |   8.8
 Interstellar |   8.7
(2 rows)
```

The film titles are unquoted text here, and `score` is the table's own numeric.
[Combining SQL and Cypher](/agensgraph/querying/combining-sql-and-cypher/) covers the
pattern in full.

## Compatibility {#compatibility}

### Column types {#column-types}

ISO/IEC 39075 §14.11 `<return statement>` gives a result column the declared type
of its expression. AgensGraph returns every Cypher result column as jsonb
regardless of the expression's type, including after an explicit cast. Unbox in
SQL, as above.

### DISTINCT and ORDER BY {#distinct-and-order-by}

An `ORDER BY` after `RETURN DISTINCT` may only sort by expressions that appear in
the projection:

```cypher
MATCH (m:movie) RETURN DISTINCT m.genre AS genre ORDER BY m.year;
```

```
ERROR:  for SELECT DISTINCT, ORDER BY expressions must appear in select list
```

This matches SQL's rule for `SELECT DISTINCT`. Project the sort key, or drop
`DISTINCT` and deduplicate with a grouping aggregate instead.

## See also {#see-also}

- [`WITH`](/agensgraph/reference/clauses/with/) — the same projection, in the middle of a pipeline
- [`ORDER BY`](/agensgraph/reference/clauses/order-by/), [`SKIP` and `LIMIT`](/agensgraph/reference/clauses/skip-and-limit/) — the clauses that follow a `RETURN`
- [`FINISH`](/agensgraph/reference/clauses/finish/) — end a query without returning rows
- [`UNION`](/agensgraph/reference/clauses/union/) — combine the results of several queries
- [Combining SQL and Cypher](/agensgraph/querying/combining-sql-and-cypher/) — getting native types out
