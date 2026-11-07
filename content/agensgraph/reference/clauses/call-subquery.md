---
title: CALL { subquery }
linkTitle: CALL { subquery }
description: Runs a read-only subquery as a clause in the pipeline, once per input row when the subquery imports
  a variable from the enclosing query.
type: docs
weight: 240
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/call-subquery.html
upstream_source: agensgraph
upstream_modified: true
---


**GQL clause**  **Added in 2.18**

Runs a read-only subquery as a clause in the pipeline, once per input row when the
subquery imports a variable from the enclosing query.

> [!IMPORTANT]
> **A bare `CALL { … }` imports nothing.** A pattern inside the braces *declares* its
> variable names, so an outer variable's name written in the body binds a fresh,
> unconstrained variable of the same name rather than referring to the outer one.
> Name the variables you need: `CALL (v) { … }`, `CALL (*) { … }` or
> `CALL { WITH v … }`.

## Synopsis {#synopsis}

```text
[ OPTIONAL ] CALL { subquery }
[ OPTIONAL ] CALL ( [ variable [, variable ] ... ] ) { subquery }
[ OPTIONAL ] CALL ( * ) { subquery }
[ OPTIONAL ] CALL { WITH variable [, variable ] ... subquery }
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`CALL { … }` evaluates the subquery and joins its result onto the working table.
The import list decides entirely what the body can see.

- With an import list, the body runs **per input row** with those variables bound,
  and the rows it returns are joined to that row.
- With no imports the body is **uncorrelated**: it runs once and its result
  cross-joins onto every input row.
- The body is read-only and must end with `RETURN`. Write clauses are rejected at
  parse time, and a body ending in `FINISH` raises `CALL subquery must RETURN at
  least one variable`.
- The names the body returns become bindings in the enclosing query. A name already
  bound outside is rejected rather than shadowed. Inside the body the imported
  variables keep their names as well: a `LET`, `UNWIND`, `FOR` or renaming `WITH`
  that would bind one of them again is refused.
- An input row for which the body returns nothing is dropped. Use
  [`OPTIONAL CALL`](/agensgraph/reference/clauses/optional-call/) to keep it.

### The forms that import {#the-forms-that-import}

Five spellings are accepted. The first two import nothing. The difference
between them and the last three is the whole point of the warning above:

| Form | Body sees |
| --- | --- |
| `CALL { … }` | Nothing |
| `CALL () { … }` | Nothing |
| `CALL (v, w) { … }` | `v` and `w` |
| `CALL (*) { … }` | Every variable in scope |
| `CALL { WITH v, w … }` | `v` and `w` |

A scope clause and an importing `WITH` may be combined. `CALL (v) { WITH w … }`
imports both. Three near-misses are syntax errors rather than alternatives:
`CALL (*) { WITH v … }`, `CALL (*, v) { … }`, and any importing `WITH` that is not
a plain list of names (`WITH *` and `WITH v AS x` are both refused).

## Parameters {#parameters}

variable
: A variable bound in the enclosing query, to be made visible inside the braces.
  One that does not exist raises `variable "<name>" to import into CALL does not
  exist`. A scope clause with no preceding clause raises `CALL has no preceding
  clause to import variables from`.

subquery
: A read-only query ending in `RETURN`. `MATCH`, `OPTIONAL MATCH`, `WITH`, `LET`,
  `UNWIND`, `FOR`, `LOAD FROM`, a nested `CALL`, `DISTINCT`, `ORDER BY`,
  `SKIP`/`LIMIT` and the set operators are all allowed. [`NEXT`](/agensgraph/reference/clauses/next/) is not.

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).

### Why the import list matters {#why-the-import-list-matters}

The subquery form is made for a question like this one: for each film that
somebody directed, how large was the cast? Written without an import list, it
answers a different question:

```cypher
MATCH (d:person)-[:directed]->(m:movie)
CALL { MATCH (a:person)-[:acted_in]->(m) RETURN count(a) AS cast_size }
RETURN m.title AS film, cast_size ORDER BY film LIMIT 4;
```

```
        film         | cast_size
---------------------+-----------
 "Avatar"            | 25
 "Blade Runner"      | 25
 "Blade Runner 2049" | 25
 "Elysium"           | 25
(4 rows)
```

Every film has the same cast size, and 25 is the number of `acted_in` edges in the
whole graph:

```cypher
MATCH ()-[r:acted_in]->() RETURN count(r) AS acted_in_edges;
```

```
 acted_in_edges
----------------
 25
(1 row)
```

The `m` inside the braces is not the `m` matched outside. It is a brand-new
variable that the body's own pattern declares, constrained only by the `acted_in`
edge. So the body counts every `acted_in` edge in the graph, once and
uncorrelated, and then cross-joins that one number onto every row.

Naming the import asks the question that was intended:

```cypher
MATCH (d:person)-[:directed]->(m:movie)
CALL (m) { MATCH (a:person)-[:acted_in]->(m) RETURN count(a) AS cast_size }
RETURN m.title AS film, cast_size ORDER BY film LIMIT 4;
```

```
        film         | cast_size
---------------------+-----------
 "Avatar"            | 1
 "Blade Runner"      | 1
 "Blade Runner 2049" | 2
 "Elysium"           | 1
(4 rows)
```

`CALL (*) { … }` and `CALL { WITH m … }` give the same numbers.

Nothing is reported because only *expressions* reference a variable, while
*patterns* declare one. Move the same mistake into a `WHERE` and it is caught:

```cypher
MATCH (d:person)-[:directed]->(m:movie)
CALL { MATCH (a:person) WHERE a.name = m.title RETURN count(a) AS n }
RETURN n;
```

```
ERROR:  variable does not exist
LINE 2: CALL { MATCH (a:person) WHERE a.name = m.title RETURN count(...
                                               ^
```

So the silence is specific to a name reused in a pattern. That is the common
case, and the reason to write the import list every time.

### Aggregate per row without collapsing the pipeline {#aggregate-per-row-without-collapsing-the-pipeline}

An aggregating body returns exactly one row for every input row, even when the
value it computes is zero, so the outer row count is unchanged:

```cypher
MATCH (p:person) WHERE p.name IN ['Keanu Reeves', 'Christopher Nolan']
CALL (p) { MATCH (p)-[:acted_in]->(m:movie) RETURN count(m) AS films }
RETURN p.name AS person, films ORDER BY person;
```

```
       person        | films
---------------------+-------
 "Christopher Nolan" | 0
 "Keanu Reeves"      | 4
(2 rows)
```

### Compute one number once {#compute-one-number-once}

An empty scope clause states plainly that the body is uncorrelated. Write it
when the body is a constant of the query:

```cypher
MATCH (p:person {name: 'Keanu Reeves'})
CALL () { MATCH (m:movie) RETURN count(m) AS movies }
RETURN p.name AS person, movies;
```

```
     person     | movies
----------------+--------
 "Keanu Reeves" | 18
(1 row)
```

### Import several variables {#import-several-variables}

Every named variable is visible, and the body may use only some of them:

```cypher
MATCH (p:person {name: 'Keanu Reeves'}), (q:person {name: 'Carrie-Anne Moss'})
CALL (p, q) { MATCH (p)-[:acted_in]->(m:movie)<-[:acted_in]-(q) RETURN count(m) AS shared }
RETURN shared;
```

```
 shared
--------
 2
(1 row)
```

## Notes {#notes}

A correlated body is not a per-row subquery in the plan. The planner pulls it up,
so the query above plans as the same join an inline pattern would produce. That
is a `Hash Join` over `person`, `acted_in` and `movie`, identical to
`MATCH (p:person)-[:acted_in]->(m:movie)`. Only a body the planner cannot flatten,
such as an aggregating one, stays a per-row lateral join with an `Aggregate` under
a `Nested Loop`.

Write clauses are refused as a syntax error at the write keyword, one for each
kind: `CREATE`, `INSERT`, `MERGE`, `SET`, `REMOVE`, `DELETE` and `DETACH DELETE`.

A body that returns a name the outer query already binds raises `variable "<name>"
returned by the CALL subquery is already bound in the outer query`. It would
shadow the outer binding for everything that follows. Alias it in the body's
`RETURN`.

## Compatibility {#compatibility}

> [!NOTE] GQL conformance
> :class: gql-conformance
>
> Implements the GQL *inline procedure call* (ISO/IEC 39075:2024 §15.2) under the
> *call procedure statement* of §15.1, in the query position of §14.5.
>
> - **Supported** — the *variable scope clause* with a binding-variable list and in
>   its empty `()` form, nesting, and the `OPTIONAL` prefix.
> - **Not supported** — a data-modifying body (§13.6, *call data-modifying procedure
>   statement*).
> - **Deviation, and the one to know** — §15.2 Syntax Rule 3 says that when the
>   variable scope clause is *absent*, the call is rewritten with a scope clause
>   listing **every** field of the incoming working record. Under the standard a bare
>   `CALL { … }` therefore imports everything, exactly like `CALL (*) { … }`.
>   AgensGraph treats an absent scope clause as importing nothing, like `CALL () { … }`.
> - **Extension** — `(*)` is not in the standard's *binding variable reference list*,
>   and neither is the importing `WITH`. Both come from openCypher.
>
> Track status in the [GQL conformance matrix](/agensgraph/appendix/gql-conformance/).

### openCypher {#opencypher}

openCypher requires the same import list, but reports its absence: referring to an
undeclared outer variable inside `CALL { }` is an error there, not a silent
rebinding. Code moved from openCypher keeps working, since `CALL (v) { }`,
`CALL (*) { }` and `CALL { WITH v … }` all mean what they do there. A bare
`CALL { }` that openCypher rejected will run here and answer differently.

## See also {#see-also}

- [`CALL`](/agensgraph/reference/clauses/call/) **GQL** — both call forms
- [`OPTIONAL CALL`](/agensgraph/reference/clauses/optional-call/) **GQL** — keep a row the body returned nothing for
- [`CALL … YIELD`](/agensgraph/reference/clauses/call-yield/) **GQL** — call a named function instead
- [Subquery value expressions](/agensgraph/reference/clauses/subquery-expressions/) **GQL** — a subquery in an expression
- [GQL conformance matrix](/agensgraph/appendix/gql-conformance/)
