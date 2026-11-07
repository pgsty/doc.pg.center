---
title: Predicate functions
linkTitle: Predicate functions
description: Functions that answer yes or no.
type: docs
weight: 30
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/functions/predicate.html
upstream_source: agensgraph
upstream_modified: true
---


Functions that answer yes or no. The four list quantifiers, `all`, `any`, `none` and
`single`, are grammar forms rather than ordinary calls. Each takes a variable, a list and a
`WHERE` clause. Each reduces the per-element results with three-valued logic, so a list
holding a null can make the answer null rather than false.

Examples run against [the example dataset](/agensgraph/get-started/example-dataset/).

## all {#all}

```
all ( variable IN list WHERE predicate ) -> boolean
```

Returns true when the predicate holds for every element of the list.

**Considerations**

- An empty list returns true.
- If the predicate is null for some element and true for all the rest, the result is null.
  One false element makes the result false whatever else is null.
- The predicate is evaluated for every element; nothing short-circuits.
- The call is lowered to `cypher_all()`. An error message from inside the predicate carries
  that name.

```cypher
MATCH (m:movie) WHERE all(x IN m.embedding WHERE x > -0.1) RETURN m.title ORDER BY m.title;
```

```
        title
---------------------
 "Blade Runner 2049"
```

## any {#any}

```
any ( variable IN list WHERE predicate ) -> boolean
```

Returns true when the predicate holds for at least one element of the list.

**Considerations**

- An empty list returns false.
- One true element makes the result true even when other elements are null.
- If no element is true and any is null, the result is null.

```cypher
MATCH (p:person)-[:acted_in]->(m:movie)
WITH p, collect(m.genre) AS genres
WHERE any(g IN genres WHERE g = 'Adventure')
RETURN p.name AS actor;
```

```
    actor
-------------
 "Sam Neill"
```

## exists {#exists}

```
exists ( pattern ) -> boolean
exists ( property_reference ) -> boolean
```

With a pattern, returns true when the pattern matches at least once. With a property
reference, returns true when that property is present and not null.

**Considerations**

- The two forms are different constructs, not overloads of one function. The pattern form
  becomes an `EXISTS` subquery, and the property form becomes an `IS NOT NULL` test.
- The argument of the property form has to be a property reference such as `m.year`. An
  arbitrary expression is read as a pattern and fails to parse.
- A pattern inside `exists()` may bind variables from the enclosing query, as `(p)` does
  below, but any variable it introduces is not visible outside.

```cypher
MATCH (m:movie {title:'Inception'}) RETURN exists(m.year) AS has_year, exists(m.budget) AS has_budget;
```

```
 has_year | has_budget
----------+------------
 t        | f
```

```cypher
MATCH (p:person) WHERE exists((p)-[:directed]->()) RETURN p.name ORDER BY p.name LIMIT 3;
```

```
        name
---------------------
 "Andrew Niccol"
 "Christopher Nolan"
 "Denis Villeneuve"
```

## isEmpty {#isempty}

```
isEmpty ( value jsonb ) -> boolean
```

Returns true when a list has no elements or a map has no keys.

**Considerations**

- The argument must resolve to `jsonb`. A bare string literal is `unknown` and matches the
  range and multirange `isempty` as well:

```cypher
RETURN isEmpty('');
```

```
ERROR:  function isempty(unknown) is not unique
LINE 1: RETURN isEmpty('');
               ^
HINT:  Could not choose a best candidate function. You might need to add explicit type casts.
```

  Cast it: `isEmpty(''::jsonb)`.
- A property reference is already `jsonb`, so `isEmpty(n.tags)` needs no cast.
- Returns true for an empty string, which is the empty `jsonb` scalar.

```cypher
RETURN isEmpty([]) AS empty_list, isEmpty([1]) AS one_element, isEmpty({}) AS empty_map;
```

```
 empty_list | one_element | empty_map
------------+-------------+-----------
 t          | f           | t
```

## none {#none}

```
none ( variable IN list WHERE predicate ) -> boolean
```

Returns true when the predicate holds for no element of the list. It is the negation of
[`any`](#any).

**Considerations**

- An empty list returns true.
- One true element makes the result false. If no element is true and any is null, the result
  is null.

```cypher
MATCH (m:movie) WHERE none(x IN m.embedding WHERE x > 0.4) RETURN count(*) AS films;
```

```
 films
-------
 15
```

## single {#single}

```
single ( variable IN list WHERE predicate ) -> boolean
```

Returns true when the predicate holds for exactly one element of the list.

**Considerations**

- An empty list returns false.
- A null result for any element makes the whole answer null, because a null could have been
  the second match.

```cypher
MATCH (p:person)-[:directed]->(m:movie)
WITH p, collect(m.year) AS years
WHERE single(y IN years WHERE y > 2010)
RETURN p.name AS director, years ORDER BY p.name;
```

```
      director       |          years
---------------------+--------------------------
 "Christopher Nolan" | [2010, 2014]
 "Denis Villeneuve"  | [2017]
 "Joss Whedon"       | [2012]
 "Lana Wachowski"    | [2003, 1999, 2021, 2003]
 "Neill Blomkamp"    | [2013]
```

## Three-valued results side by side {#three-valued-results-side-by-side}

The quantifiers differ most where the list holds a null and where the list is empty. Both
rows below are real output:

```cypher
RETURN all(x IN [1, null] WHERE x > 0) AS every, any(x IN [1, null] WHERE x > 0) AS some,
       none(x IN [null] WHERE x > 0) AS not_any, single(x IN [1, null] WHERE x > 0) AS exactly_one;
```

```
 every | some | not_any | exactly_one
-------+------+---------+-------------
       | t    |         |
```

```cypher
RETURN all(x IN [] WHERE x = 0) AS every, any(x IN [] WHERE x = 0) AS some,
       none(x IN [] WHERE x = 0) AS not_any, single(x IN [] WHERE x = 0) AS exactly_one;
```

```
 every | some | not_any | exactly_one
-------+------+---------+-------------
 t     | f    | t       | f
```

A `RETURN` leaves a boolean column as `boolean` rather than boxing it to `jsonb`. So these
print as `t`, `f` and blank for null, not as `true`, `false` and `null`.

## Compatibility {#compatibility}

### openCypher {#opencypher}

`exists()` over a property is openCypher's older spelling of `IS NOT NULL`. The
pattern-comprehension and `exists { ... }` block forms are not supported; use the pattern
form above or a [subquery expression](/agensgraph/reference/clauses/subquery-expressions/).

## See also {#see-also}

- [All functions](/agensgraph/reference/functions/all-functions/) — every function in one table
- [Subquery expressions](/agensgraph/reference/clauses/subquery-expressions/) — `EXISTS`, `COUNT`, `COLLECT`
- [List functions](/agensgraph/reference/functions/list/) — building the lists these quantify over
