---
title: UNWIND
linkTitle: UNWIND
description: 'Turns a list into rows: one working row per element.'
type: docs
weight: 160
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/unwind.html
upstream_source: agensgraph
upstream_modified: true
---


Turns a list into rows: one working row per element.

## Synopsis {#synopsis}

```text
UNWIND list_expression AS variable
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`UNWIND` expands a list into the pipeline. For each element it emits one row,
binding *variable* to that element; everything else already in scope is carried
along unchanged. It is the inverse of `collect()`, and the way to get from one
row holding a list to many rows holding its parts.

- `AS variable` is **required**. There is no unnamed form.
- The list may be a **literal**, a **list-valued property**, a variable a
  `collect()` produced, or any expression that yields a jsonb array or a
  PostgreSQL array. A scalar is refused.
- An **empty list** produces no rows, so the whole input row disappears.
- **Nulls inside** the list are elements like any other and produce rows.
- `UNWIND` runs once per incoming row, and the rows it produces multiply out:
  three input rows over a two-element list give six.
- `UNWIND` may lead a query or follow another clause. It cannot end one.
- Nest two `UNWIND` clauses to flatten a list of lists.

[`FOR`](/agensgraph/reference/clauses/for/) is the GQL counterpart and does the same job, with an optional
ordinal.

## Parameters {#parameters}

list_expression
: An expression yielding a jsonb array or a PostgreSQL array.

variable
: Name bound to each element. Visible to every clause after this one.

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).

### Expand a list literal {#expand-a-list-literal}

```cypher
UNWIND [1, 91, 203, 1, 7, 91] AS n
RETURN n;
```

```
  n
-----
 1
 91
 203
 1
 7
 91
(6 rows)
```

Six rows, in list order, duplicates included.

### Deduplicate and sort a list {#deduplicate-and-sort-a-list}

There is no way to apply `DISTINCT` to a list in place. Unwind it, deduplicate
the rows, and collect them back:

```cypher
UNWIND [1, 91, 203, 1, 7, 91] AS n
WITH DISTINCT n
ORDER BY n
RETURN collect(n) AS uniq;
```

```
      uniq
-----------------
 [1, 7, 91, 203]
(1 row)
```

### Drive a MATCH from a list {#drive-a-match-from-a-list}

One row per element, each matched in turn:

```cypher
UNWIND ['The Matrix', 'Inception'] AS t
MATCH (m:movie {title: t})
RETURN m.title AS film, m.year AS year;
```

```
     film     | year
--------------+------
 "The Matrix" | 1999
 "Inception"  | 2010
(2 rows)
```

This is the usual way to run a query over a client-supplied list of keys, with
the list passed as one parameter.

### Expand a list-valued property {#expand-a-list-valued-property}

A property may hold a list, and `UNWIND` opens it:

```cypher
MATCH (m:movie {title: 'The Matrix'})
UNWIND m.embedding AS component
RETURN component;
```

```
  component
-------------
 -0.07594558
 0.04081754
 0.29592122
 -0.11921061
(4 rows)
```

### Undo a collect {#undo-a-collect}

`collect()` folds rows into a list; `UNWIND` unfolds it again. The pair is how
you aggregate, then go back to rows:

```cypher
MATCH (p:person)-[:acted_in]->(m:movie)
WITH collect(DISTINCT m.genre) AS genres
UNWIND genres AS genre
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

### Flatten a list of lists {#flatten-a-list-of-lists}

Two `UNWIND` clauses, the second over the variable the first bound:

```cypher
UNWIND [[1, 2], [3]] AS pair
UNWIND pair AS x
RETURN pair, x;
```

```
  pair  | x
--------+---
 [1, 2] | 1
 [1, 2] | 2
 [3]    | 3
(3 rows)
```

### Expand an empty list {#expand-an-empty-list}

No rows come out, and the input row goes with them:

```cypher
UNWIND [] AS x RETURN x;
```

```
 x
---
(0 rows)
```

Use [`OPTIONAL MATCH`](/agensgraph/reference/clauses/optional-match/) or a `CASE` guard when a row must
survive an empty list.

### Keep the nulls {#keep-the-nulls}

A null element is still an element:

```cypher
UNWIND [1, NULL, 3] AS x RETURN x;
```

```
  x
------
 1
 null
 3
(3 rows)
```

The value prints as `null` because the output column is jsonb, and a jsonb null
is a value rather than a missing one.

## Notes {#notes}

`UNWIND` requires a list. Neither a scalar nor a bare `NULL` is treated as a
one-element or zero-element list:

```cypher
UNWIND 3 AS x RETURN x;
```

```
ERROR:  expression must be jsonb or array, but integer
LINE 1: UNWIND 3 AS x RETURN x;
               ^
```

```cypher
UNWIND NULL AS x RETURN x;
```

```
ERROR:  expression must be jsonb or array, but unknown
LINE 1: UNWIND NULL AS x RETURN x;
               ^
```

Wrap a value that might not be a list, as in
`UNWIND coalesce(m.tags, []) AS tag`, when the property is not guaranteed to be
there.

## Compatibility {#compatibility}

### UNWIND is not a GQL clause {#unwind-is-not-a-gql-clause}

ISO/IEC 39075 has no `UNWIND`. Its list-expanding statement is
`<for statement>` (§14.8), which AgensGraph also implements as
[`FOR`](/agensgraph/reference/clauses/for/). `FOR` adds a `WITH OFFSET` clause that gives each element its
0-based position, something `UNWIND` cannot do.

## See also {#see-also}

- [`FOR`](/agensgraph/reference/clauses/for/) **GQL** — the standard clause, with an ordinal
- [`WITH`](/agensgraph/reference/clauses/with/) — where `collect()` goes, and how to deduplicate the rows
- [`MATCH`](/agensgraph/reference/clauses/match/) — driving a match from the expanded rows
- [Functions](/agensgraph/reference/functions/) — `collect()` and the other list functions
