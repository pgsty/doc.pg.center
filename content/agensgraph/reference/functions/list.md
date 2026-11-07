---
title: List functions
linkTitle: List functions
description: Functions over lists and maps.
type: docs
weight: 50
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/functions/list.html
upstream_source: agensgraph
upstream_modified: true
---


Functions over lists and maps. A Cypher list is a `jsonb` array, so these functions take and
return `jsonb`. `collect()` over a graph element instead produces a native array, and the
functions that have an array overload work on both.

Cypher subscripts a list from 0, and a slice `list[a..b]` excludes the upper bound.

Examples run against [the example dataset](/agensgraph/get-started/example-dataset/).

## array_size {#array_size}

```
array_size ( list jsonb ) -> integer
array_size ( list json ) -> integer
array_size ( list anyarray ) -> integer
```

Returns the number of elements in an array.

**Considerations**

- Arrays only. Unlike [`cardinality`](#cardinality) it does not count a map's keys.
- The three overloads let the same name work on a Cypher list, a `json` value and a
  PostgreSQL array.

```cypher
RETURN array_size([1,2,3]) AS n;
```

```
 n
---
 3
```

## cardinality {#cardinality}

**Added in 2.18**

```
cardinality ( value jsonb ) -> jsonb
cardinality ( p graphpath ) -> jsonb
```

Returns the number of elements in a list, entries in a map, or vertices and edges in a path.

**Considerations**

- A string is refused. Use [`length`](/agensgraph/reference/functions/scalar/#length) for a string.

```cypher
RETURN cardinality('abc');
```

```
ERROR:  cardinality(): list or map is expected but "abc"
```
- Over a path this counts vertices *and* edges, so a one-edge path gives 3, while
  [`length`](/agensgraph/reference/functions/path/#length) over the same path gives 1.
- PostgreSQL's own `cardinality(anyarray)` still applies to a native array and returns
  `integer` rather than `jsonb`.

```cypher
RETURN cardinality([1,2,3]) AS list, cardinality({a:1,b:2}) AS map;
```

```
 list | map
------+-----
 3    | 2
```

```cypher
MATCH p=(:person {name:'Christopher Nolan'})-[:directed]->(:movie {title:'Inception'})
RETURN cardinality(p) AS elements;
```

```
 elements
----------
 3
```

## head {#head}

```
head ( list jsonb ) -> jsonb
head ( list anyarray ) -> anyelement
```

Returns the first element of a list.

**Considerations**

- An empty list returns null rather than raising.
- The array overload returns the element's own type, so `head(collect(n))` over vertices
  returns a `vertex`.

```cypher
RETURN head([10,20,30]) AS first, last([10,20,30]) AS final, tail([10,20,30]) AS rest;
```

```
 first | final |   rest
-------+-------+----------
 10    | 30    | [20, 30]
```

## keys {#keys}

```
keys ( map jsonb ) -> jsonb
```

Returns a list of the key names of a map, or of a graph element's properties.

**Considerations**

- The order is `jsonb`'s own key order: by key length, then bytewise. It is not insertion
  order and not alphabetical. Sort the result if you need a fixed order.
- A vertex or edge argument is accepted because it coerces to its property map.

```cypher
MATCH (p:person {name:'Keanu Reeves'}) RETURN keys(p) AS property_names;
```

```
  property_names
------------------
 ["born", "name"]
```

```cypher
RETURN keys({title:'Inception', year:2010}) AS map_keys;
```

```
     map_keys
-------------------
 ["year", "title"]
```

## last {#last}

```
last ( list jsonb ) -> jsonb
last ( list anyarray ) -> anyelement
```

Returns the final element of a list. An empty list returns null. See [`head`](#head) for a
worked example.

## range {#range}

```
range ( start integer, stop integer ) -> jsonb
range ( start integer, stop integer, step integer ) -> jsonb
```

Returns a list of integers from `start` to `stop`, inclusive at both ends.

| Name | Type | Description |
| --- | --- | --- |
| `start` | `integer` | First value in the list. |
| `stop` | `integer` | Last value the list may reach. Included when the step lands on it. |
| `step` | `integer` | Increment. Omitted, it is 1 counting up and −1 counting down. |

**Considerations**

- The result is `jsonb`, not a PostgreSQL array, so it can be subscripted and iterated like
  any Cypher list.
- Both ends are inclusive. `stop` appears in the list only when the step lands on it:
  `range(1,10,3)` ends at 10, while `range(1,9,3)` ends at 7.
- `stop` below `start` counts down without needing a negative step.

```cypher
RETURN range(1,5) AS up, range(1,10,3) AS step, range(5,1) AS down, range(5,1,-2) AS down_step;
```

```
       up        |     step      |      down       | down_step
-----------------+---------------+-----------------+-----------
 [1, 2, 3, 4, 5] | [1, 4, 7, 10] | [5, 4, 3, 2, 1] | [5, 3, 1]
```

## tail {#tail}

```
tail ( list jsonb ) -> jsonb
tail ( list anyarray ) -> anyarray
```

Returns every element of a list except the first.

**Considerations**

- An empty list returns an empty list, not null, unlike `head` and `last`.

```cypher
RETURN head([]) AS first, tail([]) AS rest;
```

```
 first | rest
-------+------
       | []
```

## unnest {#unnest}

**Added in 2.18**

```
unnest ( from_json jsonb ) -> setof jsonb
```

Expands a list into one row per element.

**Considerations**

- This is a set-returning function. In Cypher it multiplies the rows of the clause it sits
  in. `FOR x IN list` is the clause form of the same idea, and it is easier to read when you
  need the element bound to a name.
- The output column is named `value`, so in SQL you write `SELECT value FROM unnest(...)`.
- PostgreSQL's `unnest(anyarray)` still applies to a native array.

```cypher
MATCH (m:movie {title:'The Matrix'}) RETURN unnest(m.embedding) AS component;
```

```
  component
-------------
 -0.07594558
 0.04081754
 0.29592122
 -0.11921061
```

## Reversing and splitting {#reversing-and-splitting}

Two functions that produce lists are documented with the strings they come from:
[`reverse`](/agensgraph/reference/functions/string/#reverse), which reverses a list as well as a string, and
[`split`](/agensgraph/reference/functions/string/#split), which cuts a string into a list. The type-conversion page has
the three list-typed conversions: [`toStringList`](/agensgraph/reference/functions/type-conversion/#tostringlist),
[`toIntegerList`](/agensgraph/reference/functions/type-conversion/#tointegerlist) and
[`toFloatList`](/agensgraph/reference/functions/type-conversion/#tofloatlist).

## Compatibility {#compatibility}

### openCypher {#opencypher}

`range()` is inclusive of `stop` here, as in openCypher. openCypher's `reduce()` is not
supported; use a list comprehension or `FOR`. Pattern comprehensions are not supported.

## See also {#see-also}

- [All functions](/agensgraph/reference/functions/all-functions/) — every function in one table
- [Aggregate functions](/agensgraph/reference/functions/aggregate/) — `collect`, which builds the lists
- [Predicate functions](/agensgraph/reference/functions/predicate/) — `all`, `any`, `none`, `single`, `isEmpty`
- [jsonb operators and functions](/agensgraph/reference/functions/jsonb/) — the operators underneath a list
