---
title: CALL
linkTitle: CALL
description: Runs a routine from inside a query pipeline.
type: docs
weight: 220
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/call.html
upstream_source: agensgraph
upstream_modified: true
---


**GQL clause**  **Added in 2.18**

Runs a routine from inside a query pipeline. The routine is either a named
function whose rows join onto the working table, or a subquery written inline.

## Synopsis {#synopsis}

```text
[ OPTIONAL ] CALL function( [ argument [, argument ] ... ] ) YIELD yield_list
[ OPTIONAL ] CALL [ variable_scope ] { subquery }
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`CALL` has two forms, and which one you get is decided by the token after the
keyword:

- `CALL` followed by a **name** is the named-routine form. It invokes a function
  and adds the columns named in the mandatory `YIELD` list to the working row. See
  [`CALL … YIELD`](/agensgraph/reference/clauses/call-yield/).
- `CALL` followed by `(` or `{` is the inline form. It runs the subquery between
  the braces, optionally once per input row. See [`CALL { subquery }`](/agensgraph/reference/clauses/call-subquery/).

`OPTIONAL` may prefix either form. It keeps an input row whose routine or subquery
produced no rows, binding everything the call would have returned to null. See
[`OPTIONAL CALL`](/agensgraph/reference/clauses/optional-call/).

### What CALL invokes {#what-call-invokes}

In GQL the thing `CALL` invokes is a *procedure*. AgensGraph has no procedure catalog of its
own. `CALL … YIELD` resolves the name against PostgreSQL's ordinary functions, and a stock
installation registers no procedures at all.

```sql
SELECT count(*) AS procedures FROM pg_proc WHERE prokind = 'p';
```

```
 procedures
------------
          0
(1 row)
```

So "call a procedure" means "call a function" here. Any function works, and its
shape decides what `YIELD` can name:

| Function shape | What `YIELD` sees |
| --- | --- |
| Scalar, e.g. `length(text)` | One column named after the function |
| Set-returning, e.g. `generate_series(int, int)` | One column named after the function, one row per element |
| Composite or `RETURNS TABLE`, e.g. `jsonb_each_text(jsonb)` | One column per output field, under the field names |
| Any of these, under the function's own name | The whole row, when no output column has that name; a function `RETURNS SETOF vertex` yields vertices this way |

A yield item is one of these and nothing else. A name the function does not return
is refused, even when a variable of that name is bound earlier in the query.

PostgreSQL's own `CALL` statement is a different thing: it is a top-level SQL
statement, it requires a real procedure, and it is not a Cypher clause. The two do
not overlap, and each rejects the other's target.

## Parameters {#parameters}

function
: Name of a function to invoke. Schema-qualify it if `search_path` does not reach
  it. A procedure is refused: `<name>() is a procedure`, with the hint `To call a
  procedure, use CALL`.

argument
: A value expression, evaluated per input row. Arguments may reference variables
  bound earlier, which makes the call correlated. A property access produces
  `jsonb`, so cast it when the parameter is another type.

variable_scope
: Which outer variables the inline subquery may see: `(v, w)` for those named,
  `(*)` for all of them, `()` for none. **Omitting it imports nothing**. See
  [`CALL { subquery }`](/agensgraph/reference/clauses/call-subquery/), which leads with that rule.

yield_list
: `*`, or one or more of the function's output columns, each optionally renamed
  with `AS`. Mandatory. See [`CALL … YIELD`](/agensgraph/reference/clauses/call-yield/).

subquery
: A read-only query ending in `RETURN`. Write clauses are rejected.

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).

Call a set-returning function and join its rows onto the matched film:

```cypher
MATCH (m:movie {title: 'The Matrix'})
CALL jsonb_array_elements_text(m.embedding) YIELD jsonb_array_elements_text AS d
RETURN d ORDER BY d;
```

```
       d
---------------
 "-0.07594558"
 "-0.11921061"
 "0.04081754"
 "0.29592122"
(4 rows)
```

### Compute a value per row with a subquery {#compute-a-value-per-row-with-a-subquery}

The inline form answers a question per input row, keeping the body out of the main
pattern:

```cypher
MATCH (m:movie {genre: 'Adventure'})
CALL (m) { MATCH (p:person)-[:acted_in]->(m) RETURN count(p) AS cast_size }
RETURN m.title AS film, cast_size;
```

```
      film       | cast_size
-----------------+-----------
 "Jurassic Park" | 1
(1 row)
```

### Try to call a procedure {#try-to-call-a-procedure}

A procedure is the one routine kind `CALL … YIELD` will not take:

```sql
CREATE PROCEDURE noop() LANGUAGE sql AS 'SELECT 1';
```

```
CREATE PROCEDURE
```

```cypher
MATCH (m:movie) CALL noop() YIELD * RETURN count(*);
```

```
ERROR:  noop() is a procedure
LINE 1: MATCH (m:movie) CALL noop() YIELD * RETURN count(*);
                        ^
HINT:  To call a procedure, use CALL.
```

And a function is the one routine kind the SQL `CALL` statement will not take:

```sql
CALL generate_series(1, 3);
```

```
ERROR:  generate_series(integer, integer) is not a procedure
LINE 1: CALL generate_series(1, 3);
             ^
HINT:  To call a function, use SELECT.
```

## Notes {#notes}

The lexer decides between the two forms by looking one token ahead. That keeps
`call` usable as an ordinary identifier: `MATCH (call:movie) RETURN count(call)`
still works, and so does the SQL statement `CALL myproc()`.

The named-routine form is a **middle** clause: it cannot open a query and cannot
end one. The inline form may open a query, but only without a scope clause. A
scope clause with nothing before it raises `CALL has no preceding clause to import
variables from`.

## Compatibility {#compatibility}

> [!NOTE] GQL conformance
> :class: gql-conformance
>
> Implements the GQL *call procedure statement* and *procedure call* (ISO/IEC
> 39075:2024 §15.1) in the query position of §14.5, *call query statement*.
>
> - **Supported** — both procedure-call forms the standard defines, the inline call
>   of §15.2 and the named call of §15.3, each with the optional `OPTIONAL` prefix.
> - **Not supported** — the *call data-modifying procedure statement* (§13.6): a
>   called routine or subquery may not write to the graph. Also not supported is a
>   catalog of GQL procedures — §17.5 procedure references resolve to PostgreSQL
>   functions, and the standard's `QUERY PROCEDURE` indication has no counterpart.
> - **Deviation** — the standard makes the `YIELD` clause optional on a named call
>   (§15.3). AgensGraph requires it.
>
> Track status in the [GQL conformance matrix](/agensgraph/appendix/gql-conformance/).

### openCypher {#opencypher}

openCypher's `CALL db.labels()` style of procedure call maps onto the named form,
but the names differ: there is no `db.*` or `dbms.*` namespace here. Use the
PostgreSQL catalogs and the `\dGv` / `\dGe` meta-commands instead, or read
[ag_label](/agensgraph/system-catalogs/catalogs/) directly.

Drop the routines the examples created:

```sql
DROP PROCEDURE noop();
```

## See also {#see-also}

- [`CALL … YIELD`](/agensgraph/reference/clauses/call-yield/) **GQL** — the named-routine form in detail
- [`CALL { subquery }`](/agensgraph/reference/clauses/call-subquery/) **GQL** — the inline form, and its import list
- [`OPTIONAL CALL`](/agensgraph/reference/clauses/optional-call/) **GQL** — the input-preserving form
- [Subquery value expressions](/agensgraph/reference/clauses/subquery-expressions/) **GQL** — a subquery in an expression rather than a clause
- [GQL conformance matrix](/agensgraph/appendix/gql-conformance/)
