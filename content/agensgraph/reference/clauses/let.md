---
title: LET
linkTitle: LET
description: Adds computed values to the working record without dropping columns already in scope.
type: docs
weight: 70
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/let.html
upstream_source: agensgraph
upstream_modified: true
---


**GQL clause**  **Added in 2.18**

Adds computed values to the working record without dropping columns already in
scope. It is the GQL-standard counterpart to Cypher's `WITH *, expr AS v`.

## Synopsis {#synopsis}

```text
LET variable = expression [, variable = expression ] ...
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`LET` introduces one or more new variables into the current row, computed from
expressions over variables already in scope. Unlike `WITH`, it is **additive**:
every binding in scope is carried forward automatically, so `LET` can never
accidentally drop a variable from the pipeline.

- Each variable is **introduce-only**. A name already in scope cannot be rebound,
  inside the body of a subquery expression or of an importing `CALL { }` as much
  as at the top level.
- Expressions are evaluated **row-by-row**; aggregates are not allowed.
- `LET` may **lead** a query or sit in the middle, but cannot terminate one. It is the
  clause to open a statement with, because [`WITH`](/agensgraph/reference/clauses/with/) in that position is SQL's
  common table expression.

## Parameters {#parameters}

variable
: Name of the new binding. Must not already be in scope. Visible to every clause
  that follows.

expression
: Any row-wise value expression: property access, arithmetic, function calls,
  `CASE`, list/map constructors. Evaluated once per input row.

## Examples {#examples}

These examples run against [the example dataset](/agensgraph/get-started/example-dataset/).

### Add a derived value and keep everything in scope {#add-a-derived-value-and-keep-everything-in-scope}

The GQL and Cypher forms are equivalent. Switch tabs to compare:

{{< tabs >}}
{{< tab label="GQL — LET" >}}
```cypher
MATCH (p:person)
LET age_in_2026 = 2026 - p.born
RETURN p.name AS name, age_in_2026
ORDER BY age_in_2026 LIMIT 3;
```
{{< /tab >}}
{{< tab label="Cypher — WITH" >}}
```cypher
MATCH (p:person)
WITH *, 2026 - p.born AS age_in_2026
RETURN p.name AS name, age_in_2026
ORDER BY age_in_2026 LIMIT 3;
```
{{< /tab >}}
{{< /tabs >}}
```
       name        | age_in_2026
-------------------+-------------
 "Ryan Gosling"    | 46
 "Neill Blomkamp"  | 47
 "Sam Worthington" | 50
(3 rows)
```

The difference is what happens to `p`. `LET` carries it forward automatically.
The `WITH` form has to ask for it with `*`, and a `WITH` that forgets the `*`
drops `p`, so the `RETURN` then fails.

### Lead a query with computed values {#lead-a-query-with-computed-values}

Because `LET` is additive it can open a statement, seeding values with nothing yet in scope:

```cypher
LET radius = 7, area = 3.14159 * 7 * 7
RETURN radius, area;
```

```
 radius |   area
--------+-----------
 7      | 153.93791
(1 row)
```

### Introduce-only {#introduce-only}

A name already in scope cannot be rebound:

```cypher
MATCH (p:person) LET p = 1 RETURN p;
```

```
ERROR:  variable "p" already exists
HINT:  LET cannot redefine an existing variable; use a different name.
```

> [!NOTE] GQL conformance
> :class: gql-conformance
>
> Implements the GQL *LET statement* (ISO/IEC 39075:2024 §14.7).
>
> - **Supported** — variable definition, multiple bindings, leading position, and row-wise expressions.
> - **Not supported** — `LET` over aggregate expressions. Track status in the [conformance matrix](/agensgraph/appendix/gql-conformance/).

> [!NOTE]
> `LET` became a **reserved keyword** in 2.18. If you used `let` as a label or
> variable name in an earlier version, quote it (`"let"` — double quotes, not
> backticks) or rename it. Property
> keys and `RETURN` aliases are unaffected.

## See also {#see-also}

- [`WITH`](/agensgraph/reference/clauses/with/) — the Cypher analogue
- [`NEXT`](/agensgraph/reference/clauses/next/) **GQL**
- [`RETURN`](/agensgraph/reference/clauses/return/)
- [GQL conformance matrix](/agensgraph/appendix/gql-conformance/)
