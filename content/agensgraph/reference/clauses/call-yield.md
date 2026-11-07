---
title: CALL … YIELD
linkTitle: CALL … YIELD
description: Invokes a named function and adds the columns it produces to the working row, joining its rows onto
  the pipeline.
type: docs
weight: 230
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/call-yield.html
upstream_source: agensgraph
upstream_modified: true
---


**GQL clause**  **Added in 2.18**

Invokes a named function and adds the columns it produces to the working row,
joining its rows onto the pipeline.

## Synopsis {#synopsis}

```text
[ OPTIONAL ] CALL function( [ argument [, argument ] ... ] ) YIELD *
[ OPTIONAL ] CALL function( [ argument [, argument ] ... ] ) YIELD column [ AS alias ] [, column ] ...
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

The clause becomes a function scan joined onto the preceding clause's rows, like a
lateral `SELECT * FROM function(arguments)`, and the `YIELD` list picks from that
result. A yield item is resolved against the function's result and nothing else, so
a name the function does not return is an error even when the query binds a
variable of that name.

- `YIELD` is **mandatory**. `CALL f(x)` with no `YIELD` is a syntax error.
- The clause can neither open a query nor end one. `CALL` at the start of a
  statement is read as PostgreSQL's SQL `CALL`, so a leading
  `CALL f() YIELD …` is a syntax error.
- If the arguments reference variables bound earlier, the call is **correlated** and
  runs once per input row. With constant arguments the function runs once and its
  rows cross-join onto the pipeline.
- Yielded columns are ordinary bindings afterwards: filter them, aggregate them,
  order by them, or feed them to a following `MATCH`.
- An input row for which the function yields no rows is **dropped**, exactly as an
  inner join drops it. Use [`OPTIONAL CALL`](/agensgraph/reference/clauses/optional-call/) to keep it.

## Parameters {#parameters}

function
: Name of the function to invoke, schema-qualified if `search_path` does not reach
  it. The parentheses are required even with no arguments. A procedure is refused
  with `<name>() is a procedure`.

argument
: A value expression evaluated per input row. A property access produces `jsonb`,
  so a function whose parameter is another type needs an explicit cast.

column
: An output column of the function. A scalar or single-column set-returning
  function has one, named after the function itself; a composite or
  `RETURNS TABLE` function has one per output field, under the field names.
  `YIELD *` takes all of them. The function's own name, when no column has it,
  stands for the whole row, which is how a function declared `RETURNS SETOF
  vertex` or `RETURNS SETOF edge` is yielded as vertices or edges. Any other name
  is refused with `function f has no output column "x"`.

alias
: New name for the yielded column. Required when the column's own name is already
  bound in the query.

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).

Expand one film's properties into rows. `jsonb_each_text` returns two columns, and
`YIELD` names both:

```cypher
MATCH (m:movie {title: 'The Matrix'})
CALL jsonb_each_text(jsonb_build_object('title', m.title, 'year', m.year, 'genre', m.genre))
     YIELD key, value
RETURN key AS property, value ORDER BY property;
```

```
 property |    value
----------+--------------
 "genre"  | "Action"
 "title"  | "The Matrix"
 "year"   | "1999"
(3 rows)
```

### Rename a yielded column {#rename-a-yielded-column}

`AS` renames it for every clause that follows:

```cypher
MATCH (m:movie {title: 'The Matrix'})
CALL jsonb_each_text(properties(m)) YIELD key AS property
RETURN property ORDER BY property;
```

```
  property
-------------
 "embedding"
 "genre"
 "plot"
 "title"
 "year"
(5 rows)
```

Yielding a subset is allowed. `value` is not bound here.

### Take every column with YIELD * {#take-every-column-with-yield}

A single-column set-returning function names its column after itself:

```cypher
MATCH (m:movie) WHERE m.genre = 'Adventure'
CALL generate_series(1, 2) YIELD *
RETURN m.title AS film, generate_series AS n ORDER BY n;
```

```
      film       | n
-----------------+---
 "Jurassic Park" | 1
 "Jurassic Park" | 2
(2 rows)
```

The arguments are constants, so `generate_series` runs once and its two rows
cross-join onto the film.

### Correlate the call with the matched row {#correlate-the-call-with-the-matched-row}

Pass a value from the row and the function runs per row. `m.year` is `jsonb`, so it
needs a cast:

```cypher
MATCH (m:movie {title: 'The Matrix'})
CALL generate_series(1, (m.year)::int) YIELD generate_series AS n
RETURN count(n) AS years;
```

```
 years
-------
 1999
(1 row)
```

Without the cast the function cannot be resolved:

```cypher
MATCH (m:movie {title: 'The Matrix'})
CALL generate_series(1, m.year) YIELD generate_series AS n
RETURN count(n);
```

```
ERROR:  function generate_series(integer, jsonb) does not exist
LINE 2: CALL generate_series(1, m.year) YIELD generate_series AS n
        ^
HINT:  No function matches the given name and argument types. You might need to add explicit type casts.
```

### Chain two calls {#chain-two-calls}

The second call may correlate on the first one's yielded column:

```cypher
MATCH (m:movie {title: 'The Matrix'})
CALL generate_series(1, 2) YIELD generate_series AS n
CALL generate_series(1, n) YIELD generate_series AS k
RETURN n, k ORDER BY n, k;
```

```
 n | k
---+---
 1 | 1
 2 | 1
 2 | 2
(3 rows)
```

### Yield the whole row {#yield-the-whole-row}

When no output column carries the function's own name, that name stands for the
whole row. `jsonb_each_text` returns `(key, value)` rows:

```cypher
MATCH (m:movie {title: 'The Matrix'})
CALL jsonb_each_text(jsonb_build_object('title', m.title, 'year', m.year))
     YIELD jsonb_each_text AS pair
RETURN pair ORDER BY pair;
```

```
                  pair
-----------------------------------------
 {"key": "title", "value": "The Matrix"}
 {"key": "year", "value": "1999"}
(2 rows)
```

A function declared `RETURNS SETOF vertex` yields its vertices the same way, under
its own name.

## Notes {#notes}

The plan shows which of the two execution shapes you got. A correlated call is a
`Nested Loop` whose inner side is the function scan. An uncorrelated call puts the
function scan on the outer side and materializes the graph scan:

```cypher
EXPLAIN (COSTS OFF)
MATCH (m:movie) CALL generate_series(1, (m.year)::int) YIELD generate_series AS n
RETURN m.title, n;
```

```
               QUERY PLAN
----------------------------------------
 Nested Loop
   ->  Seq Scan on movie m
   ->  Function Scan on generate_series
(3 rows)
```

A yielded name that collides with a binding already in scope is rejected rather
than shadowing it. The error is `variable "m" yielded by CALL is already bound in
the outer query`. Rename it with `AS`.

The reverse is rejected too: a yield item that is not an output column of the
function is refused even when a variable of that name is bound earlier. The earlier
binding is never what `YIELD` means.

```cypher
MATCH (m:movie {title: 'The Matrix'})
CALL generate_series(1, 2) YIELD m AS n
RETURN n;
```

```
ERROR:  function generate_series has no output column "m"
LINE 2: CALL generate_series(1, 2) YIELD m AS n
                                         ^
```

> [!NOTE]
> A function returning the pseudo-type `record` cannot be called: the clause has
> nowhere to put the column definition list PostgreSQL requires, so
> `CALL jsonb_to_recordset(…) YIELD *` raises `a column definition list is required
> for functions returning "record"`. Wrap such a call in a SQL subquery instead.

## Compatibility {#compatibility}

> [!NOTE] GQL conformance
> :class: gql-conformance
>
> Implements the GQL *named procedure call* (ISO/IEC 39075:2024 §15.3) with the
> *yield clause* of §16.14, under the *call procedure statement* of §15.1.
>
> - **Supported** — argument lists, correlated arguments, the `YIELD *` and
>   `YIELD column [AS alias]` forms, the rule of §16.14 Syntax Rule 7 that a yield
>   item names a column of the procedure's result, the duplicate-alias rejection of
>   Syntax Rule 6, and the `OPTIONAL` prefix.
> - **Not supported** — calling a GQL procedure. §15.3 resolves a *procedure
>   reference* against the catalog described in §17.5, which AgensGraph does not
>   have; names resolve to PostgreSQL functions instead.
> - **Deviation** — §15.3 makes the `YIELD` clause optional. AgensGraph requires it,
>   because the clause has to contribute columns to the working table.
>
> Track status in the [GQL conformance matrix](/agensgraph/appendix/gql-conformance/).

### openCypher {#opencypher}

openCypher writes the same clause but resolves the name against a procedure
registry (`db.labels()`, `dbms.components()`), and allows `CALL proc()` with no
`YIELD` as a standalone statement. Neither the registry nor the standalone form
exists here: names resolve to PostgreSQL functions, and `YIELD` is required.

## See also {#see-also}

- [`CALL`](/agensgraph/reference/clauses/call/) **GQL** — both call forms, and what a routine is here
- [`CALL { subquery }`](/agensgraph/reference/clauses/call-subquery/) **GQL** — the inline form
- [`OPTIONAL CALL`](/agensgraph/reference/clauses/optional-call/) **GQL** — keep a row the function yielded nothing for
- [GQL conformance matrix](/agensgraph/appendix/gql-conformance/)
