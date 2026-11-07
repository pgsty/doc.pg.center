---
title: OPTIONAL CALL
linkTitle: OPTIONAL CALL
description: Keeps an input row whose call produced no rows, binding everything the call would have returned to
  null.
type: docs
weight: 250
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/optional-call.html
upstream_source: agensgraph
upstream_modified: true
---


**GQL clause**  **Added in 2.18**

Keeps an input row whose call produced no rows, binding everything the call would
have returned to null. It is the `CALL` counterpart of `OPTIONAL MATCH`.

## Synopsis {#synopsis}

```text
OPTIONAL CALL [ variable_scope ] { subquery }
OPTIONAL CALL function( [ argument [, argument ] ... ] ) YIELD yield_list
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`OPTIONAL` applies to both forms of [`CALL`](/agensgraph/reference/clauses/call/): the inline subquery and the
named function. A plain `CALL` joins the call's rows onto the pipeline, so an input
row that produced none drops out. `OPTIONAL CALL` lowers to a **left join**
instead, which preserves that row.

- Preservation is decided **per input row**. A correlated call that finds nothing
  for one row nulls only that row and leaves the others alone.
- Every variable the call would have bound is nulled together, whatever its type:
  vertex, edge, path, list, map or scalar.
- The binding is a real SQL null, not a jsonb `null`, so `IS NULL` is the way to
  test it.
- `OPTIONAL` preserves rows; it does not invent them. An empty input still produces
  no output.
- A preserved row is an ordinary row afterwards, so a later clause multiplies it
  like any other.

## Parameters {#parameters}

variable_scope
: Which outer variables the subquery may see, exactly as for
  [`CALL { subquery }`](/agensgraph/reference/clauses/call-subquery/): `(v, w)`, `(*)`, `()`, or an importing
  `WITH` inside the braces. The import rule applies unchanged. A bare
  `OPTIONAL CALL { … }` imports nothing.

subquery
: A read-only query ending in `RETURN`.

function, argument, yield_list
: As for [`CALL … YIELD`](/agensgraph/reference/clauses/call-yield/). `YIELD` is still mandatory.

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).

Three people: Keanu Reeves has four acting credits, Ryan Gosling one, Christopher
Nolan none. `OPTIONAL CALL` keeps the director:

```cypher
MATCH (p:person) WHERE p.name IN ['Keanu Reeves', 'Ryan Gosling', 'Christopher Nolan']
OPTIONAL CALL (p) { MATCH (p)-[:acted_in]->(m:movie) RETURN m.title AS film }
RETURN p.name AS person, film ORDER BY person, film;
```

```
       person        |            film
---------------------+----------------------------
 "Christopher Nolan" |
 "Keanu Reeves"      | "The Matrix"
 "Keanu Reeves"      | "The Matrix Reloaded"
 "Keanu Reeves"      | "The Matrix Resurrections"
 "Keanu Reeves"      | "The Matrix Revolutions"
 "Ryan Gosling"      | "Blade Runner 2049"
(6 rows)
```

Drop the `OPTIONAL` and the same body loses that row entirely, while the other two
people are unaffected:

```cypher
MATCH (p:person) WHERE p.name IN ['Keanu Reeves', 'Ryan Gosling', 'Christopher Nolan']
CALL (p) { MATCH (p)-[:acted_in]->(m:movie) RETURN m.title AS film }
RETURN p.name AS person, film ORDER BY person, film;
```

```
     person     |            film
----------------+----------------------------
 "Keanu Reeves" | "The Matrix"
 "Keanu Reeves" | "The Matrix Reloaded"
 "Keanu Reeves" | "The Matrix Resurrections"
 "Keanu Reeves" | "The Matrix Revolutions"
 "Ryan Gosling" | "Blade Runner 2049"
(5 rows)
```

Four rows, one row and one preserved row: the multiplicity is per input row, not a
property of the query.

### Preserve a row a function yielded nothing for {#preserve-a-row-a-function-yielded-nothing-for}

`OPTIONAL` sits in the same place on the named form, where it covers a function
that returns an empty set for some rows:

```cypher
MATCH (m:movie) WHERE m.title IN ['The Matrix', 'Avatar']
OPTIONAL CALL generate_series(1, CASE WHEN m.title = 'Avatar' THEN 0 ELSE 2 END)
         YIELD generate_series AS n
RETURN m.title AS film, n ORDER BY film, n;
```

```
     film     | n
--------------+---
 "Avatar"     |
 "The Matrix" | 1
 "The Matrix" | 2
(3 rows)
```

`generate_series(1, 0)` is empty, so Avatar's row survives with `n` null. Without
`OPTIONAL` that row is gone and only The Matrix's two rows remain.

### Test a preserved binding {#test-a-preserved-binding}

Every variable the body would have returned is null on a preserved row, and it is
a SQL null:

```cypher
MATCH (p:person {name: 'Christopher Nolan'})
OPTIONAL CALL (p) { MATCH (p)-[:acted_in]->(m:movie) RETURN m.title AS film, m.year AS year }
RETURN film IS NULL AS film_is_null, year IS NULL AS year_is_null;
```

```
 film_is_null | year_is_null
--------------+--------------
 t            | t
(1 row)
```

### Confirm that no row is invented {#confirm-that-no-row-is-invented}

`OPTIONAL` preserves input rows. With no input row there is nothing to preserve:

```cypher
MATCH (p:person {name: 'Nobody'})
OPTIONAL CALL (p) { MATCH (p)-[:acted_in]->(m:movie) RETURN m.title AS film }
RETURN p.name AS person, film;
```

```
 person | film
--------+------
(0 rows)
```

## Notes {#notes}

The plan states the mechanism outright. The `generate_series` scan is the nullable
side of a `Nested Loop Left Join`. That join preserves Avatar's row:

```cypher
EXPLAIN (COSTS OFF)
MATCH (m:movie) WHERE m.title IN ['The Matrix', 'Avatar']
OPTIONAL CALL generate_series(1, CASE WHEN m.title = 'Avatar' THEN 0 ELSE 2 END)
         YIELD generate_series AS n
RETURN m.title AS film, n;
```

```
                                       QUERY PLAN
-----------------------------------------------------------------------------------------
 Nested Loop Left Join
   ->  Seq Scan on movie m
         Filter: (properties.'title' = ANY ('{"\"The Matrix\"","\"Avatar\""}'::jsonb[]))
   ->  Function Scan on generate_series
(4 rows)
```

Some bodies always yield at least one row, and for those `OPTIONAL` changes
nothing. An ungrouped aggregate is the common case: it always produces one row,
so a person with no credits gets `0`, not null. Compare the `films` column in
[`CALL { subquery }`](/agensgraph/reference/clauses/call-subquery/#aggregate-per-row-without-collapsing-the-pipeline).

`OPTIONAL` relaxes nothing else. A write clause in the body is still a syntax
error, a body that returns an outer name is still rejected, and a bare
`OPTIONAL CALL { … }` still imports nothing.

## Compatibility {#compatibility}

> [!NOTE] GQL conformance
> :class: gql-conformance
>
> Implements the `OPTIONAL` prefix of the GQL *call procedure statement* (ISO/IEC
> 39075:2024 §15.1), which covers both the *inline procedure call* of §15.2 and the
> *named procedure call* of §15.3.
>
> - **Supported** — `OPTIONAL` on both call forms, with per-input-row preservation
>   and null binding of every returned variable.
> - **Not supported** — `OPTIONAL` on a data-modifying call (§13.6), since a call
>   cannot write to the graph at all.
>
> Track status in the [GQL conformance matrix](/agensgraph/appendix/gql-conformance/).

### openCypher {#opencypher}

`OPTIONAL CALL` is a GQL construct; openCypher has only `OPTIONAL MATCH`. The two
agree wherever both can express the same thing, because the standard defines
`OPTIONAL MATCH p` as `OPTIONAL CALL (imports) { MATCH p RETURN vars }`. So
`OPTIONAL CALL` is the more general primitive, not a second mechanism.

## See also {#see-also}

- [`OPTIONAL MATCH`](/agensgraph/reference/clauses/optional-match/) — the same preservation, on a pattern
- [`CALL`](/agensgraph/reference/clauses/call/) **GQL** — both call forms
- [`CALL { subquery }`](/agensgraph/reference/clauses/call-subquery/) **GQL** — the inline form and its import list
- [`CALL … YIELD`](/agensgraph/reference/clauses/call-yield/) **GQL** — the named-function form
- [GQL conformance matrix](/agensgraph/appendix/gql-conformance/)
