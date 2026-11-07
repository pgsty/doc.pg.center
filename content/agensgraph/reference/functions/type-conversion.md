---
title: Type conversion functions
linkTitle: Type conversion functions
description: Functions that turn a value into another type.
type: docs
weight: 90
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/functions/type-conversion.html
upstream_source: agensgraph
upstream_modified: true
---


Functions that turn a value into another type. Two families sit here. The `to…` functions
read a value and return null when it does not name one. The `to…OrNull` variants do the same
but never raise.

A cast is the other way to convert, and Cypher accepts `::` with most type names:

```cypher
RETURN '42'::int AS i, 42::numeric AS n, 'true'::boolean AS b, '2020-01-01'::date AS d;
```

```
 i  | n  | b |      d
----+----+---+--------------
 42 | 42 | t | "2020-01-01"
```

`::timestamp` and `::time` are the exceptions:

```cypher
RETURN pg_typeof('2020-01-01 10:00'::timestamp);
```

```
ERROR:  syntax error at or near "timestamp"
LINE 1: RETURN pg_typeof('2020-01-01 10:00'::timestamp);
                                             ^
```

A Cypher cast accepts an ordinary type name, and it has rules of its own for the numeric,
character, bit, json and interval spellings. It has no rule for the date and time spellings.
`TIMESTAMP` and `TIME` are keywords, so a cast to either needs such a rule and there is none.
`date`, `timestamptz` and `timetz` are not keywords, so they arrive as ordinary type names
and work. `::timestamptz` is the usual way round it, and wrapping the Cypher in SQL is the
other.

Examples run against [the example dataset](/agensgraph/get-started/example-dataset/).

## toBoolean {#toboolean}

```
toBoolean ( value text ) -> boolean
toBoolean ( value "any" ) -> boolean
```

Returns the boolean a value names, or null when it names none.

**Considerations**

- Accepts `true`, `false`, `t`, `f`, `on`, `off`, `1` and `0`, in any case. Anything else
  returns null rather than raising.
- It is stricter than the cast: `toBoolean('yes')` is null, while `'yes'::boolean` is true.
- A `RETURN` leaves a boolean unboxed, so it prints as `t` or `f` and null prints as blank.

```cypher
RETURN toBoolean('TRUE') AS t, toBoolean('false') AS f, toBoolean(true) AS already;
```

```
 t | f | already
---+---+---------
 t | f | t
```

## toBooleanOrNull {#tobooleanornull}

```
toBooleanOrNull ( value text ) -> boolean
toBooleanOrNull ( value "any" ) -> boolean
```

Returns the boolean a value names, or null. Where [`toBoolean`](#toboolean) may raise on a
type it cannot read at all, this returns null.

```cypher
RETURN toBooleanOrNull('yes') AS unrecognised, toBooleanOrNull('true') AS recognised;
```

```
 unrecognised | recognised
--------------+------------
              | t
```

## toFloat {#tofloat}

**Added in 2.18**

```
toFloat ( value "any" ) -> double precision
```

Returns the floating-point number a value names, or null.

**Considerations**

- One overload, taking `"any"`, so it accepts a string, an integer or a `jsonb` property
  without a cast.
- A value that is not a number returns null rather than raising.
- The result is `double precision`. A Cypher `RETURN` boxes it to a `jsonb` number.

```cypher
RETURN toFloat('3.5') AS from_string, toFloat(7) AS from_integer, toFloat('abc') AS unreadable;
```

```
 from_string | from_integer | unreadable
-------------+--------------+------------
 3.5         | 7            |
```

## toFloatList {#tofloatlist}

```
toFloatList ( list jsonb ) -> jsonb
toFloatList ( list anyarray ) -> double precision[]
```

Converts every element of a list to a floating-point number.

**Considerations**

- **Which overload you get decides the return type.** A Cypher list is `jsonb`, so
  `toFloatList([...])` returns `jsonb`. Only a PostgreSQL array argument gives
  `double precision[]`, and that form is reachable from SQL.
- An element that is not a number becomes null; the list keeps its length.

```cypher
RETURN toFloatList(['1.4','2.5','true']) AS floats, pg_typeof(toFloatList(['1.4'])) AS type;
```

```
      floats      |  type
------------------+---------
 [1.4, 2.5, null] | "jsonb"
```

```sql
SELECT toFloatList(ARRAY['1.5','2']) AS floats, pg_typeof(toFloatList(ARRAY['1.5','2'])) AS type;
```

```
 floats  |        type
---------+--------------------
 {1.5,2} | double precision[]
```

## toInteger {#tointeger}

**Added in 2.18**

```
toInteger ( value "any" ) -> bigint
```

Returns the integer a value names, or null.

**Considerations**

- Truncates towards zero rather than rounding: `toInteger(3.7)` is 3.
- A boolean converts, with true becoming 1.
- A value that is not a number returns null rather than raising.
- The result is `bigint`.

```cypher
RETURN toInteger('42') AS from_string, toInteger(3.7) AS truncated,
       toInteger('abc') AS unreadable, toInteger(true) AS from_boolean;
```

```
 from_string | truncated | unreadable | from_boolean
-------------+-----------+------------+--------------
 42          | 3         |            | 1
```

## toIntegerList {#tointegerlist}

```
toIntegerList ( list jsonb ) -> jsonb
toIntegerList ( list anyarray ) -> bigint[]
```

Converts every element of a list to an integer. Which overload applies decides the return
type, exactly as for [`toFloatList`](#tofloatlist): a Cypher list gives `jsonb`, a
PostgreSQL array gives `bigint[]`.

```cypher
RETURN toIntegerList(['1','2','x']) AS integers;
```

```
   integers
--------------
 [1, 2, null]
```

## toString {#tostring}

```
toString ( value jsonb ) -> jsonb
```

Returns the string form of a value.

**Considerations**

- A value that is already a string comes back unchanged.
- A number, a boolean, a list and a map all convert. The result is a `jsonb` string, so a
  `RETURN` prints it with quotes.

```cypher
RETURN toString(11.5) AS number, toString('already a string') AS string, toString(true) AS boolean;
```

```
 number |       string       | boolean
--------+--------------------+---------
 "11.5" | "already a string" | "true"
```

## toStringList {#tostringlist}

```
toStringList ( list jsonb ) -> jsonb
toStringList ( list anyarray ) -> text[]
```

Converts every element of a list to a string. Which overload applies decides the return
type, as for [`toFloatList`](#tofloatlist): a Cypher list gives `jsonb`, a PostgreSQL array
gives `text[]`.

```cypher
RETURN toStringList([1, 2.5, true]) AS strings;
```

```
       strings
----------------------
 ["1", "2.5", "true"]
```

## toStringOrNull {#tostringornull}

```
toStringOrNull ( value "any" ) -> text
```

Returns the string form of a value, or null when the value has no string form.

**Considerations**

- Returns `text`, not `jsonb`, unlike [`toString`](#tostring). A Cypher `RETURN` boxes it
  back to a `jsonb` string, so on the page the two look alike; in SQL they do not.
- A list returns null: a list has no single string form.

```cypher
RETURN toStringOrNull(11.5) AS number, toStringOrNull([1,2]) AS list,
       pg_typeof(toStringOrNull(1)) AS type;
```

```
 number | list |  type
--------+------+--------
 "11.5" |      | "text"
```

## What is not converted {#what-is-not-converted}

`::timestamp` and `::time` cannot be written in Cypher, as above. There is also no `toMap`,
no `toList` and no `toDate`. Build a map with `{...}`, a list with `[...]`, and read a date
with `::date`.

A graph element converts to its property bag and nothing else. `v::jsonb` gives the map, the
same value as [`properties(v)`](/agensgraph/reference/functions/scalar/#properties). There is no conversion from a map back
to a vertex.

## Compatibility {#compatibility}

### openCypher {#opencypher}

`toInteger`, `toFloat`, `toString` and `toBoolean` are openCypher's names and behave as
openCypher describes. The one exception is that a value they cannot read returns null rather
than raising. The `…OrNull` variants and the three list conversions are extensions.

openCypher's `toInteger` rounds; this one truncates.

## See also {#see-also}

- [All functions](/agensgraph/reference/functions/all-functions/) — every function in one table
- [String functions](/agensgraph/reference/functions/string/) — `split`, `toLower`, `toUpper`
- [List functions](/agensgraph/reference/functions/list/) — the lists these conversions produce
- [jsonb operators and functions](/agensgraph/reference/functions/jsonb/) — `to_jsonb` and the `#>> '{}'` idiom
