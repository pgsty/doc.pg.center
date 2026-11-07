---
title: jsonb operators and functions
linkTitle: jsonb operators and functions
description: Properties are jsonb.
type: docs
weight: 100
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/functions/jsonb.html
upstream_source: agensgraph
upstream_modified: true
---


Properties **are** `jsonb`. A vertex is the composite `(id graphid, properties jsonb)`, and
an edge adds `start` and `end`. So every property you read in Cypher, and every property
column you touch in SQL, is a value of PostgreSQL's `jsonb` type. That has two consequences
to take in before anything else on this page. A string property comes back quoted, and the
whole `jsonb` operator set applies to it.

Examples run against [the example dataset](/agensgraph/get-started/example-dataset/).

## Property access operators {#property-access-operators}

These four take a `jsonb` value on the left. The two with a doubled arrow return `text`; the
two with a single arrow return `jsonb`.

| Operator | Right operand | Returns | Result |
| --- | --- | --- | --- |
| `->` | `text` key or `integer` index | `jsonb` | The value at that key or index |
| `->>` | `text` key or `integer` index | `text` | The same value, with a string unquoted |
| `#>` | `text[]` path | `jsonb` | The value at that path |
| `#>>` | `text[]` path | `text` | The same value, with a string unquoted |

```sql
SELECT properties -> 'name' AS quoted, properties ->> 'name' AS plain
FROM moviekb.person ORDER BY id LIMIT 1;
```

```
     quoted     |    plain
----------------+--------------
 "Keanu Reeves" | Keanu Reeves
```

```psql
SELECT '{"a":{"b":[1,2]}}'::jsonb #> '{a,b}' AS at_path,
       '{"a":{"b":[1,2]}}'::jsonb #>> '{a,b,0}' AS at_path_text;
```

```
 at_path | at_path_text
---------+--------------
 [1, 2]  | 1
```

## Getting an unquoted scalar out {#getting-an-unquoted-scalar-out}

A Cypher `RETURN` boxes a scalar output column to `jsonb`. So `RETURN m.title` prints
`"Inception"`, quotes included, and so does `RETURN m.title::text`. The quotes are part of
the JSON, not an artefact of `psql`.

The way out is `#>> '{}'`: an empty path selects the whole document, and `#>>` returns it as
`text`. Wrap the Cypher in SQL and apply it there:

```cypher
SELECT t AS boxed, t #>> '{}' AS unboxed
FROM (MATCH (m:movie {title:'Inception'}) RETURN m.title AS t) q;
```

```
    boxed    |  unboxed
-------------+-----------
 "Inception" | Inception
```

Reach for this idiom whenever a Cypher result has to join against, or be compared with,
ordinary `text`. A join onto a relational table is one such case.

## Containment and existence operators {#containment-and-existence-operators}

| Operator | Right operand | Returns true when |
| --- | --- | --- |
| `@>` | `jsonb` | The left document contains the right one |
| `<@` | `jsonb` | The left document is contained in the right one |
| `?` | `text` | The key or string element is present |
| `?\|` | `text[]` | Any of the keys is present |
| `?&` | `text[]` | All of the keys are present |

```psql
SELECT properties @> '{"name":"Keanu Reeves"}' AS contains,
       properties ? 'born' AS has_born,
       properties ?& ARRAY['name','born'] AS has_both
FROM moviekb.person ORDER BY id LIMIT 1;
```

```
 contains | has_born | has_both
----------+----------+----------
 t        | t        | t
```

A property index cannot serve any of these; each is a containment test over the whole bag
rather than a comparison against one key. A GIN index on `properties` can.

## Modification operators {#modification-operators}

| Operator | Right operand | Result |
| --- | --- | --- |
| `\|\|` | `jsonb` | The two documents merged, the right winning on a shared key |
| `-` | `text` key or `integer` index | The document without that key or element |
| `#-` | `text[]` path | The document without the value at that path |

```psql
SELECT '{"a":1}'::jsonb || '{"b":2}'::jsonb AS merged,
       '{"a":1,"b":2}'::jsonb - 'a' AS without_a,
       '{"a":{"b":1}}'::jsonb #- '{a,b}' AS without_path;
```

```
      merged      | without_a | without_path
------------------+-----------+--------------
 {"a": 1, "b": 2} | {"b": 2}  | {"a": {}}
```

In Cypher these are spelled as clauses instead: `SET n += {city:'Seoul'}` merges, and
`REMOVE n.city` deletes a key.

## Arithmetic operators on jsonb {#arithmetic-operators-on-jsonb}

PostgreSQL already gives `-` and `||` a meaning on `jsonb`, so AgensGraph could not reuse
them for arithmetic. It adds eight operators whose names are wrapped in backticks. The
Cypher parser emits those when you write `+`, `-`, `*`, `/`, `%` or `^` on properties.

| Operator | Implemented by | OID | Meaning |
| --- | --- | --- | --- |
| ``` `+` ``` | `jsonb_add` | 7176 | Addition; concatenation for two strings or two lists |
| ``` `-` ``` | `jsonb_sub` | 7178 | Subtraction |
| ``` `*` ``` | `jsonb_mul` | 7180 | Multiplication |
| ``` `/` ``` | `jsonb_div` | 7182 | Division, integer when both operands are integers |
| ``` `%` ``` | `jsonb_mod` | 7184 | Modulo |
| ``` `^` ``` | `jsonb_pow` | 7186 | Exponentiation |
| ``` `+` ``` (prefix) | `jsonb_uplus` | 7190 | Unary plus |
| ``` `-` ``` (prefix) | `jsonb_uminus` | 7191 | Unary minus |

Backtick is an operator character in this fork's lexer (`scan.l:369`), so these names are
typeable in SQL as well. Both operands must be `jsonb`:

```sql
SELECT '"a"'::jsonb `+` '"b"'::jsonb AS strings, '[1]'::jsonb `+` '[2]'::jsonb AS lists;
```

```
 strings | lists
---------+--------
 "ab"    | [1, 2]
```

> [!NOTE]
> Write Cypher arithmetic with the ordinary operators — `n.a + n.b` — and let the parser choose
> these. The backtick names are here so you can recognise them in an `EXPLAIN` plan, in an
> error message, or in a `pg_operator` listing. The implementation functions can also be called
> directly: `jsonb_add('1'::jsonb, '2'::jsonb)` returns 3.

## ag_property_text {#ag_property_text}

**Added in 2.18**

```
ag_property_text ( properties jsonb, key text, expected_kind "char" ) -> text
```

Returns a property's value as `text`, but only when the stored value is of the JSON kind
asked for.

| Name | Type | Description |
| --- | --- | --- |
| `properties` | `jsonb` | The property bag to read. |
| `key` | `text` | Name of the property. |
| `expected_kind` | `"char"` | `'n'` for a number, `'s'` for a string, `'b'` for a boolean. |

**Considerations**

- This backs typed-column property promotion. `->>` returns the text of a value, and text
  carries no kind, so the string `"5"` and the number `5` are indistinguishable through it.
  A column of integers would answer 5 for a property that holds a string. This function asks
  the kind first.
- A kind mismatch **raises**, it does not return null:
  `property "n" holds a number` with the detail `A column promoting this property holds strings.`
- A property that is absent, or present and JSON null, returns null.
- It is not intended to be written by hand. Read a property with `n.key` in Cypher or
  `properties ->> 'key'` in SQL.

```psql
SELECT ag_property_text('{"name":"x","n":5}'::jsonb, 'n', 'n') AS number,
       ag_property_text('{"name":"x"}'::jsonb, 'missing', 's') AS absent;
```

```
 number | absent
--------+--------
 5      |
```

## cypher_to_jsonb {#cypher_to_jsonb}

```
cypher_to_jsonb ( value anyelement ) -> jsonb
```

Boxes a value to `jsonb` using Cypher's rules, which differ from `to_jsonb`'s for string
types.

**Considerations**

- This is the function a Cypher `RETURN` inserts around a scalar output column. It appears
  in a plan at the point where the boxing happens.
- It is strict, so a null stays null.
- The parser refuses to wrap a graph element in it. That refusal makes `coalesce(m, 0)` and
  a `jsonb` list of vertices fail. It lives in the parser's `coerce_to_jsonb()`, not in the
  function. Called by name on a `vertex`, the function returns the whole composite, `id` and
  `tid` included, which is *not* the property bag that `v::jsonb` gives you. Use
  [`vertex_to_jsonb`](#vertex_to_jsonb) or the cast for that.

```sql
SELECT cypher_to_jsonb('abc'::text) AS from_text, cypher_to_jsonb(42) AS from_integer;
```

```
 from_text | from_integer
-----------+--------------
 "abc"     | 42
```

## edge_to_jsonb {#edge_to_jsonb}

```
edge_to_jsonb ( e edge ) -> jsonb
```

Returns an edge's property bag. This is the function the cast `e::jsonb` uses, and it
returns the same value as [`properties(e)`](/agensgraph/reference/functions/scalar/#properties).

**Considerations**

- The endpoints are not included — only the properties. Read them with
  [`start_id`](/agensgraph/reference/functions/scalar/#start_id) and [`end_id`](/agensgraph/reference/functions/scalar/#end_id).

```cypher
MATCH ()-[e:related_to]->() WITH e LIMIT 1 RETURN edge_to_jsonb(e) AS bag;
```

```
      bag
---------------
 {"weight": 1}
```

## graphid_in_jsonb_array {#graphid_in_jsonb_array}

```
graphid_in_jsonb_array ( id graphid, elements jsonb ) -> boolean
```

Returns true when a `graphid` is one of the graph elements in a `jsonb` array.

**Considerations**

- The parser emits this for `id(n) IN [...]` so that a list of elements can be tested without
  unboxing each one. A `graphid` boxes to a `jsonb` string, and this compares against that
  form.
- Written by hand it is a plain membership test.

```sql
SELECT graphid_in_jsonb_array('4.1'::graphid, '["4.1","4.2"]'::jsonb) AS present;
```

```
 present
---------
 t
```

## jsonb_array_length {#jsonb_array_length}

```
jsonb_array_length ( list jsonb ) -> integer
```

Returns the number of elements in a `jsonb` array, as an `integer`.

**Considerations**

- PostgreSQL's own function. [`cardinality`](/agensgraph/reference/functions/list/#cardinality) and
  [`length`](/agensgraph/reference/functions/scalar/#length) are the Cypher spellings and return `jsonb`; this one returns
  a native `integer` and raises on a value that is not an array.

```sql
SELECT jsonb_array_length('[1,2,3]');
```

```
 jsonb_array_length
--------------------
                  3
```

## to_jsonb {#to_jsonb}

```
to_jsonb ( value anyelement ) -> jsonb
```

Converts any SQL value to `jsonb`, mapping a composite to an object and an array to an
array.

**Considerations**

- This is how you get relational rows into a graph. `LOAD FROM t AS r CREATE (:label =
  to_jsonb(row_to_json(r)))` turns each row into a property bag.
- On a graph element it converts the whole composite, not the property bag. `v::jsonb` and
  [`vertex_to_jsonb`](#vertex_to_jsonb) give the bag.

```sql
SELECT to_jsonb(42) AS number, to_jsonb('x'::text) AS string;
```

```
 number | string
--------+--------
 42     | "x"
```

## vertex_to_jsonb {#vertex_to_jsonb}

```
vertex_to_jsonb ( v vertex ) -> jsonb
```

Returns a vertex's property bag. This is the function the cast `v::jsonb` uses, and it
returns the same value as [`properties(v)`](/agensgraph/reference/functions/scalar/#properties).

```cypher
MATCH (n:person {name:'Keanu Reeves'}) RETURN vertex_to_jsonb(n) AS bag;
```

```
                  bag
----------------------------------------
 {"born": 1964, "name": "Keanu Reeves"}
```

## Ordering and comparison {#ordering-and-comparison}

`jsonb` has its own total order, and it is not the order the values would have in their own
types. Kind comes first: null, then string, then number, then boolean, then array, then
object. Only values of the same kind compare by value:

```psql
SELECT v FROM (VALUES ('1'::jsonb),('"a"'),('true'),('null'),('[1]'),('{"k":1}')) t(v) ORDER BY v;
```

```
    v
----------
 null
 "a"
 1
 true
 [1]
 {"k": 1}
```

This matters wherever a Cypher result is sorted or aggregated. `min()` and `max()` over a
`jsonb` column follow that order, so a property that holds numbers in some rows and strings
in others will not sort the way a reader expects. Read it through a typed column, or cast it,
when the order has to be the type's own.

Two integers also divide as integers, because `jsonb` keeps the distinction:

```cypher
RETURN 7 / 2 AS integer_division, 7.0 / 2 AS real_division;
```

```
 integer_division |   real_division
------------------+--------------------
 3                | 3.5000000000000000
```

## See also {#see-also}

- [All functions](/agensgraph/reference/functions/all-functions/) — every function in one table
- [Scalar functions](/agensgraph/reference/functions/scalar/) — `properties`, `keys`, `length`
- [Type conversion functions](/agensgraph/reference/functions/type-conversion/) — the `to…` family
- [Combining SQL and Cypher](/agensgraph/querying/combining-sql-and-cypher/) — where `#>> '{}'` earns its keep
