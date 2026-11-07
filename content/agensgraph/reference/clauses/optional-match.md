---
title: OPTIONAL MATCH
linkTitle: OPTIONAL MATCH
description: Matches a pattern the way MATCH does, but keeps an input row whose pattern finds nothing, binding the
  pattern's variables to null for it.
type: docs
weight: 20
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/optional-match.html
upstream_source: agensgraph
upstream_modified: true
---


**GQL clause**

Matches a pattern the way `MATCH` does, but keeps an input row whose pattern
finds nothing, binding the pattern's variables to null for it.

## Synopsis {#synopsis}

```text
OPTIONAL MATCH pattern [, pattern ] ... [ WHERE condition ]
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`OPTIONAL MATCH` takes the same patterns as [`MATCH`](/agensgraph/reference/clauses/match/) and matches them
the same way. The difference is what happens when a pattern finds no match. A
plain `MATCH` drops the row. `OPTIONAL MATCH` keeps it and binds every variable
the pattern introduces to null. It is the graph counterpart of a `LEFT JOIN`.

- Variables already in scope keep their values. Only the variables the optional
  pattern introduces can become null.
- A `WHERE` attached to an `OPTIONAL MATCH` is **part of the optional match**. A
  row whose pattern matched but whose condition failed is kept with nulls, not
  dropped. To drop it, filter after the clause with [`WITH`](/agensgraph/reference/clauses/with/) or
  [`FILTER`](/agensgraph/reference/clauses/filter/).
- Leading a query with `OPTIONAL MATCH` yields one all-null row when the pattern
  matches nothing, rather than no rows.
- Several comma-separated patterns in one clause are optional together: they
  either all match or the whole clause contributes nulls.

## Parameters {#parameters}

pattern
: A path pattern, in the same syntax `MATCH` uses. See
  [`MATCH`](/agensgraph/reference/clauses/match/) for the node, edge, path and `ONLY` forms.

condition
: A boolean expression evaluated as part of the match. A row that fails it is
  kept, with the pattern's variables null.

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).

### List people whether or not they directed anything {#list-people-whether-or-not-they-directed-anything}

```cypher
MATCH (p:person) WHERE p.born > 1974
OPTIONAL MATCH (p)-[:directed]->(m:movie)
RETURN p.name AS person, m.title AS directed
ORDER BY person;
```

```
      person       | directed
-------------------+-----------
 "Neill Blomkamp"  | "Elysium"
 "Ryan Gosling"    |
 "Sam Worthington" |
(3 rows)
```

Two of the three directed nothing, so `m` is null for them, and therefore
`m.title` is null too. The same query with a plain `MATCH` on the second line
returns one row:

```cypher
MATCH (p:person) WHERE p.born > 1974
MATCH (p)-[:directed]->(m:movie)
RETURN p.name AS person, m.title AS directed
ORDER BY person;
```

```
      person      | directed
------------------+-----------
 "Neill Blomkamp" | "Elysium"
(1 row)
```

### Keep only the rows that failed to match {#keep-only-the-rows-that-failed-to-match}

Test the optional variable for null after the clause. This finds the science
fiction films with no outgoing `related_to` edge:

```cypher
MATCH (m:movie) WHERE m.genre = 'Sci-Fi'
OPTIONAL MATCH (m)-[:related_to]->(n:movie)
WITH m, n WHERE n IS NULL
RETURN m.title AS film
ORDER BY film;
```

```
        film
---------------------
 "Avatar"
 "Blade Runner 2049"
 "Elysium"
 "Gattaca"
 "Inception"
 "The Fifth Element"
(6 rows)
```

### See where the WHERE goes {#see-where-the-where-goes}

`Jurassic Park` has one actor, Sam Neill, born 1947. With the condition inside the
optional match, the film survives with a null actor:

```cypher
MATCH (m:movie) WHERE m.genre = 'Adventure'
OPTIONAL MATCH (p:person)-[:acted_in]->(m) WHERE p.born > 1950
RETURN m.title AS film, p.name AS actor
ORDER BY film, actor;
```

```
      film       | actor
-----------------+-------
 "Jurassic Park" |
(1 row)
```

With the same condition applied after the clause, the film is dropped:

```cypher
MATCH (m:movie) WHERE m.genre = 'Adventure'
OPTIONAL MATCH (p:person)-[:acted_in]->(m)
WITH m, p WHERE p.born > 1950
RETURN m.title AS film, p.name AS actor
ORDER BY film, actor;
```

```
 film | actor
------+-------
(0 rows)
```

### Lead a query with an optional match {#lead-a-query-with-an-optional-match}

```cypher
OPTIONAL MATCH (m:movie {title: 'Nope'})
RETURN m;
```

```
 m
---

(1 row)
```

One row, with `m` null. A plain `MATCH` here returns no rows at all.

## Notes {#notes}

Reading a property of a null vertex gives null rather than an error, so
`m.title` is safe on a row the pattern did not match. Testing the variable
itself, `WHERE n IS NULL`, is the reliable way to detect that row. A matched
vertex may legitimately be missing the property you would otherwise test.

## Compatibility {#compatibility}

### Optional blocks (ISO/IEC 39075 §14.4) {#optional-blocks-isoiec-39075-144}

The standard's `<optional match statement>` also allows a braced or parenthesized
block of match statements, `OPTIONAL { MATCH ... MATCH ... }`. AgensGraph accepts
`OPTIONAL` only directly in front of `MATCH`; the block form is a syntax error.
`OPTIONAL` also prefixes [`CALL`](/agensgraph/reference/clauses/call-subquery/).

## See also {#see-also}

- [`MATCH`](/agensgraph/reference/clauses/match/) — the pattern syntax, and the non-optional form
- [`WHERE`](/agensgraph/reference/clauses/where/) — conditions, and where they take effect
- [`WITH`](/agensgraph/reference/clauses/with/) — the clause that filters after an optional match
- [`CALL { subquery }`](/agensgraph/reference/clauses/call-subquery/) — `OPTIONAL` prefixes this clause too
