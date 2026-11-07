---
title: UNION
linkTitle: UNION
description: Combines the results of two or more queries into one.
type: docs
weight: 210
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/union.html
upstream_source: agensgraph
upstream_modified: true
---


**GQL clause**

Combines the results of two or more queries into one. `INTERSECT` and `EXCEPT`
are the same construct with the other two set operations.

## Synopsis {#synopsis}

```text
query { UNION | INTERSECT | EXCEPT } [ ALL | DISTINCT ] query [ ... ]
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

A set operator joins two complete queries, each with its own `RETURN`, into a
single result:

| Operator | Result |
| --- | --- |
| `UNION` | Rows in either query. |
| `INTERSECT` | Rows in both queries. |
| `EXCEPT` | Rows in the first query and not in the second. |

Rules that apply to all three:

- Every query must return the **same number of columns**, and corresponding
  columns must be comparable. Their names need not match; the result takes the
  names from the first query.
- `DISTINCT` is the default: duplicate rows are removed. `ALL` keeps them.
  `UNION` and `UNION DISTINCT` mean the same thing.
- Operators **chain**, and a chain is evaluated left to right.
- Row order is not defined. An `ORDER BY` written after a set operation does
  **not** sort the combined result. See [Notes](#notes) for what does.
- Each query must be a complete query ending in `RETURN`. An arm cannot end in a
  write clause or a bare `MATCH`.

## Parameters {#parameters}

query
: A complete query ending in a `RETURN` with the same number of columns as every
  other query in the chain.

ALL
: Keep duplicate rows.

DISTINCT
: Remove duplicate rows. This is the default.

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).

### Combine two result sets {#combine-two-result-sets}

Everyone connected to `Inception`, whichever way they are connected:

```cypher
MATCH (p:person)-[:directed]->(:movie {title: 'Inception'}) RETURN p.name AS name
UNION
MATCH (p:person)-[:acted_in]->(:movie {title: 'Inception'}) RETURN p.name AS name;
```

```
        name
---------------------
 "Christopher Nolan"
 "Leonardo DiCaprio"
(2 rows)
```

### Keep or drop the duplicates {#keep-or-drop-the-duplicates}

Both arms here return the same 18 genres, one per film. `UNION` reduces them to
three:

```cypher
MATCH (m:movie) RETURN m.genre AS genre
UNION
MATCH (m:movie) RETURN m.genre AS genre;
```

```
    genre
-------------
 "Action"
 "Sci-Fi"
 "Adventure"
(3 rows)
```

`UNION DISTINCT` is the same statement written out in full. `UNION ALL` keeps
every row from both arms:

```cypher
MATCH (m:movie {genre: 'Adventure'}) RETURN m.title AS film
UNION ALL
MATCH (m:movie) WHERE m.year = 2021 RETURN m.title AS film;
```

```
            film
----------------------------
 "Jurassic Park"
 "The Matrix Resurrections"
(2 rows)
```

Those two rows are distinct anyway, so `ALL` shows only in its cost. It skips
the deduplication.

### Take the rows in both queries {#take-the-rows-in-both-queries}

```cypher
MATCH (m:movie {genre: 'Action'}) RETURN m.title AS film
INTERSECT
MATCH (m:movie) WHERE m.year < 1995 RETURN m.title AS film;
```

```
             film
------------------------------
 "The Terminator"
 "Terminator 2: Judgment Day"
(2 rows)
```

### Subtract one query from another {#subtract-one-query-from-another}

The people who directed something but never acted:

```cypher
MATCH (p:person)-[:directed]->(m:movie) RETURN p.name AS name
EXCEPT
MATCH (p:person)-[:acted_in]->(m:movie) RETURN p.name AS name;
```

```
        name
---------------------
 "Andrew Niccol"
 "Neill Blomkamp"
 "Lana Wachowski"
 "Lilly Wachowski"
 "Joss Whedon"
 "James Cameron"
 "Luc Besson"
 "Denis Villeneuve"
 "Christopher Nolan"
 "Paul Verhoeven"
 "Ridley Scott"
 "Steven Spielberg"
(12 rows)
```

The rows come back in no particular order.

### Sort and page the combined result {#sort-and-page-the-combined-result}

Put the set operation in a [`NEXT`](/agensgraph/reference/clauses/next/) chain and sort the second half of the
chain, which receives the combined rows:

```cypher
MATCH (m:movie) WHERE m.genre = 'Adventure' RETURN m.title AS film
UNION
MATCH (m:movie) WHERE m.genre = 'Sci-Fi' RETURN m.title AS film
NEXT ORDER BY film LIMIT 3 RETURN film;
```

```
        film
---------------------
 "Avatar"
 "Blade Runner"
 "Blade Runner 2049"
(3 rows)
```

A [`CALL { subquery }`](/agensgraph/reference/clauses/call-subquery/) wrapper does the same job:

```cypher
CALL { MATCH (m:movie) WHERE m.genre = 'Adventure' RETURN m.title AS film
       UNION
       MATCH (m:movie) WHERE m.genre = 'Sci-Fi' RETURN m.title AS film }
RETURN film ORDER BY film LIMIT 3;
```

```
        film
---------------------
 "Avatar"
 "Blade Runner"
 "Blade Runner 2049"
(3 rows)
```

### Reject a mismatched column count {#reject-a-mismatched-column-count}

```cypher
MATCH (m:movie) RETURN m.title AS t
UNION
MATCH (p:person) RETURN p.name AS n, p.born AS b;
```

```
ERROR:  each UNION query must have the same number of columns
```

The message names `UNION` for all three operators.

## Notes {#notes}

An `ORDER BY`, `SKIP` or `LIMIT` written after a set operation attaches to the
**last query in the chain**, not to the combined result. It therefore sorts or
pages that one arm before the sets are combined. `LIMIT 1` here does not produce
one row:

```cypher
MATCH (m:movie) WHERE m.genre = 'Adventure' RETURN m.title AS film
UNION
MATCH (m:movie) WHERE m.genre = 'Sci-Fi' RETURN m.title AS film
LIMIT 1;
```

```
      film
-----------------
 "Inception"
 "Jurassic Park"
(2 rows)
```

One row survived the `LIMIT` in the Sci-Fi arm, which returns 10 films without
it. The single Adventure film joined that row afterwards. Alias resolution
follows the same rule, so a sort key must name a column of the last arm:

```cypher
MATCH (m:movie) RETURN m.title AS first_col
UNION
MATCH (p:person) RETURN p.name AS second_col
ORDER BY first_col LIMIT 2;
```

```
ERROR:  variable does not exist
LINE 4: ORDER BY first_col LIMIT 2;
                 ^
```

Use the `NEXT` or `CALL` form shown above whenever you need to sort or page the
combined rows. In SQL, a `SELECT` over the set operation does it too:

```psql
SELECT * FROM (
  MATCH (m:movie) WHERE m.genre = 'Adventure' RETURN m.title AS film
  UNION
  MATCH (m:movie) WHERE m.genre = 'Sci-Fi' RETURN m.title AS film
) q ORDER BY film LIMIT 3;
```

```
        film
---------------------
 "Avatar"
 "Blade Runner"
 "Blade Runner 2049"
(3 rows)
```

## Compatibility {#compatibility}

### Set operators (ISO/IEC 39075 §14.2) {#set-operators-isoiec-39075-142}

The standard's `<set operator>` is
`UNION [ <set quantifier> ] | EXCEPT [ <set quantifier> ] | INTERSECT [ <set quantifier> ]`,
with `DISTINCT` implicit when no quantifier is given. AgensGraph implements all
three operators and both quantifiers, on exactly those rules. openCypher has only
`UNION` and `UNION ALL`, so `INTERSECT` and `EXCEPT` are available here and not
there.

The standard's `OTHERWISE` conjunction, which takes the second query's rows only
when the first returns none, is not implemented.

### Sorting a combined result (ISO/IEC 39075 §14.9) {#sorting-a-combined-result-isoiec-39075-149}

The standard applies an `<order by and page statement>` to the current working
table, which after a composite query is the combined result. AgensGraph attaches
it to the last query of the chain instead, as shown in
[Notes](#notes). Wrap the set operation in `NEXT`, in a `CALL { }`, or in a SQL
`SELECT` to sort or page what the operation produced.

## See also {#see-also}

- [`RETURN`](/agensgraph/reference/clauses/return/) — every arm of a set operation ends with one
- [`NEXT`](/agensgraph/reference/clauses/next/) **GQL** — chain a further query onto the combined rows
- [`CALL { subquery }`](/agensgraph/reference/clauses/call-subquery/) — the other way to wrap a set operation
- [`ORDER BY`](/agensgraph/reference/clauses/order-by/), [`SKIP` and `LIMIT`](/agensgraph/reference/clauses/skip-and-limit/) — what they attach to here
- [Combining SQL and Cypher](/agensgraph/querying/combining-sql-and-cypher/) — sorting a set operation from SQL
