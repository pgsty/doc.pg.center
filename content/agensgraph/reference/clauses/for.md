---
title: FOR
linkTitle: FOR
description: Expands a list into rows, one row per element, optionally binding each element's position.
type: docs
weight: 170
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/for.html
upstream_source: agensgraph
upstream_modified: true
---


**GQL clause**  **Added in 2.18**

Expands a list into rows, one row per element, optionally binding each element's
position. It is the GQL counterpart of Cypher's `UNWIND`.

## Synopsis {#synopsis}

```text
FOR variable IN list [ WITH OFFSET [ AS offset_variable ] ]
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`FOR` joins each input row with the elements of a list, so an input row that meets
an *n*-element list becomes *n* output rows. When the list depends on the row,
the expansion runs per row.

- The element variable must be a **new** name. Reusing one in scope raises
  `duplicate variable "<name>"`.
- `WITH OFFSET` binds each element's position. The offset is **0-based**.
- An empty list, a null list and a missing property all produce **zero rows**, so
  a `FOR` over nothing drops its input row.
- A scalar is not a list and is refused, not wrapped in one.
- `FOR` may open a query, sit in the middle of one, or drive a write clause. It
  cannot end one.

## Parameters {#parameters}

variable
: Name bound to one element per output row. Must not already be in scope.

list
: Any expression producing a list: a literal, `range()`, a list-valued property, a
  list built by an earlier `collect()`, or two lists concatenated with `+`.

offset_variable
: Name bound to the element's 0-based position. Omit the `AS` clause and the
  position is bound to `offset`. That is a reserved word, so it has to be written
  `"offset"` everywhere afterwards. Prefer the `AS` form.

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).

Expand a list of titles and look each one up. `FOR` and Cypher's `UNWIND` expand
the same list. Switch tabs to compare:

{{< tabs >}}
{{< tab label="GQL — FOR" >}}
```cypher
FOR t IN ['The Matrix', 'Inception', 'Gattaca']
MATCH (m:movie {title: t})
RETURN t AS title, m.year AS year ORDER BY year;
```
{{< /tab >}}
{{< tab label="Cypher — UNWIND" >}}
```cypher
UNWIND ['The Matrix', 'Inception', 'Gattaca'] AS t
MATCH (m:movie {title: t})
RETURN t AS title, m.year AS year ORDER BY year;
```
{{< /tab >}}
{{< /tabs >}}
```
    title     | year
--------------+------
 "Gattaca"    | 1997
 "The Matrix" | 1999
 "Inception"  | 2010
(3 rows)
```

### Number the elements as they expand {#number-the-elements-as-they-expand}

`WITH OFFSET AS` names the position. You want that when the list order is the
answer, as in a ranked list of titles:

```cypher
FOR t IN ['The Matrix', 'Inception', 'Gattaca'] WITH OFFSET AS i
MATCH (m:movie {title: t})
RETURN i, t AS title ORDER BY i;
```

```
 i |    title
---+--------------
 0 | "The Matrix"
 1 | "Inception"
 2 | "Gattaca"
(3 rows)
```

The first element is at 0, not 1.

### Reach the offset without naming it {#reach-the-offset-without-naming-it}

Leaving off the `AS` clause still binds the position, but under the name `offset`,
which is a reserved keyword. Every later reference has to be quoted:

```cypher
FOR t IN ['The Matrix', 'Inception'] WITH OFFSET RETURN "offset", t;
```

```
 offset |      t
--------+--------------
 0      | "The Matrix"
 1      | "Inception"
(2 rows)
```

Drop the quotes and the query does not parse:

```cypher
FOR t IN ['The Matrix'] WITH OFFSET RETURN offset, t;
```

```
ERROR:  syntax error at or near "offset"
LINE 1: FOR t IN ['The Matrix'] WITH OFFSET RETURN offset, t;
                                                   ^
```

### Expand a list-valued property {#expand-a-list-valued-property}

The list can come from the matched row, in which case the expansion runs per row:

```cypher
MATCH (m:movie {title: 'The Matrix'})
FOR e IN m.embedding
RETURN e ORDER BY e;
```

```
      e
-------------
 -0.11921061
 -0.07594558
 0.04081754
 0.29592122
(4 rows)
```

### Generate the rows a query needs {#generate-the-rows-a-query-needs}

`range()` is a list like any other, so `FOR` can drive a lookup over generated
keys:

```cypher
FOR y IN range(1999, 2001)
MATCH (m:movie {year: y})
RETURN y, m.title AS film ORDER BY y, film;
```

```
  y   |     film
------+--------------
 1999 | "The Matrix"
(1 row)
```

## Notes {#notes}

`FOR` compiles to a lateral `unnest()`, while `UNWIND` compiles to a `ProjectSet`.
The two are interchangeable in meaning, but they are not the same plan:

```cypher
EXPLAIN (COSTS OFF) FOR x IN [1, 2, 3] RETURN x;
```

```
                 QUERY PLAN
--------------------------------------------
 Function Scan on unnest _agens_default_for
(1 row)
```

Because the expansion goes through `unnest()`, a scalar source is a type error
rather than a one-element list. An integer raises `function unnest(integer) does
not exist` and a scalar property raises `cannot extract elements from a scalar`. A
null, by contrast, is treated as an empty list and yields no rows.

> [!NOTE]
> `FOR` is a reserved keyword in PostgreSQL, so the clause puts no new restriction on
> identifier names. `offset` is reserved as well, which is why the bare `WITH OFFSET`
> form has to be quoted where it is read back.

## Compatibility {#compatibility}

> [!NOTE] GQL conformance
> :class: gql-conformance
>
> Implements the GQL *FOR statement* (ISO/IEC 39075:2024 §14.8), Feature GQ10, "FOR
> statement: list value support", and Feature GQ24, "FOR statement: WITH OFFSET".
>
> - **Supported** — expansion of a list value expression, per-input-row evaluation,
>   a null source treated as an empty list, and `WITH OFFSET` with the 0-based
>   position the standard specifies (`j−1` in §14.8, General Rule 2).
> - **Not supported** — `WITH ORDINALITY` (Feature GQ11), the 1-based counterpart;
>   add one to the offset instead. Also not supported is a `<binding table
>   reference value expression>` as the source (Feature GQ23), since AgensGraph has
>   no named binding tables.
> - **Deviation** — the standard writes the position variable without `AS`
>   (`WITH OFFSET i`). AgensGraph requires `WITH OFFSET AS i`, and a bare
>   `WITH OFFSET` defaults the name to `offset`.
>
> Track status in the [GQL conformance matrix](/agensgraph/appendix/gql-conformance/).

### openCypher {#opencypher}

openCypher spells this clause [`UNWIND … AS x`](/agensgraph/reference/clauses/unwind/), which AgensGraph accepts
unchanged and which has no offset form.

## See also {#see-also}

- [`UNWIND`](/agensgraph/reference/clauses/unwind/) — the Cypher analogue, without an offset
- [`INSERT`](/agensgraph/reference/clauses/insert/) **GQL** — a write `FOR` can drive
- [`LET`](/agensgraph/reference/clauses/let/) **GQL**
- [`FILTER`](/agensgraph/reference/clauses/filter/) **GQL** — narrow the expanded rows
- [`ORDER BY`](/agensgraph/reference/clauses/order-by/) — sort the rows a `FOR` produced
- [GQL conformance matrix](/agensgraph/appendix/gql-conformance/)
