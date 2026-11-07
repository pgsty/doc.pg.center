---
title: Data types
linkTitle: Data types
description: 'AgensGraph adds five types to PostgreSQL''s set: graphid, vertex, edge, graphpath and rowid.'
type: docs
weight: 20
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/types.html
upstream_source: agensgraph
upstream_modified: true
---


AgensGraph adds five types to PostgreSQL's set: `graphid`, `vertex`, `edge`, `graphpath` and
`rowid`. Everything else a graph stores is `jsonb`, in the `properties` column of a label.
Every PostgreSQL type is still available and behaves as PostgreSQL documents it.

The five are defined in `pg_type` with fixed OIDs, so they are the same in every database and
need no extension.

| Type | Storage | What it holds |
| --- | --- | --- |
| `graphid` | 8 bytes, by value | The identity of one vertex or edge. |
| `vertex` | Composite, variable | An id, a property map, and the row's physical location. |
| `edge` | Composite, variable | An id, two endpoint ids, a property map, and the row's location. |
| `graphpath` | Composite, variable | An array of vertices and an array of edges. |
| `rowid` | 10 bytes, by reference | A table OID and a row pointer. Internal. |

## graphid {#graphid}

`graphid` is the identity of a vertex or an edge. An edge stores them to name its endpoints.
It is a 64-bit value in two parts: the top 16 bits are the **label id**, the low
48 bits are the **local id**, a per-label sequence. It prints as *labid*`.`*locid*.

[How a graph is stored](/agensgraph/concepts/graph-on-postgresql/#identity-the-graphid)
explains why that layout matters to the planner. This section is the formal detail.

Two functions take the parts back apart:

```sql
SELECT id, graphid_labid(id) AS labid, graphid_locid(id) AS locid
FROM moviekb.person WHERE properties->>'name' = 'Keanu Reeves';
```

```
 id  | labid | locid
-----+-------+-------
 4.1 |     4 |     1
```

`graphid(`*labid*`, `*locid*`)` builds one from its parts. It is the same function a label's
`id` column calls in its default expression.

### Range {#range}

The label id is 16 bits and the local id 48, so the largest `graphid` is:

```sql
SELECT graphid(65535, 281474976710655) AS highest;
```

```
        highest
-----------------------
 65535.281474976710655
```

Either part out of range is refused rather than truncated:

```sql
SELECT graphid(65536, 1);
```

```
ERROR:  labid out of range: 65536
```

```sql
SELECT graphid(3, 281474976710656);
```

```
ERROR:  locid out of range: 281474976710656
```

0 is reserved as *no label*, so a database holds at most 65,535 labels and a label at most
2<sup>48</sup> − 1 elements. The reservation is a convention rather than a check, and
`graphid(0, 1)` builds `0.1`. But nothing ever assigns label id 0.
[Limits](/agensgraph/appendix/limits/) collects these alongside PostgreSQL's own.

### Casts {#casts}

There is exactly one cast into `graphid`, from `numeric`, and it is implicit. There is none
from `integer`, so a whole number written without a decimal point does not convert:

```sql
SELECT 1::graphid;
```

```
ERROR:  cannot cast type integer to graphid
LINE 1: SELECT 1::graphid;
                ^
```

Write the two parts. A numeric literal with a decimal point casts, and a string in
*labid*`.`*locid* form parses:

```sql
SELECT 1.1::graphid AS from_numeric, '3.1'::graphid AS from_text;
```

```
 from_numeric | from_text
--------------+-----------
 1.1          | 3.1
```

The `numeric` cast reads the number the way the type prints. So `1.1` is label 1, element 1,
not the number one point one. A numeric with no fractional digits has no local id and is
rejected: `1::numeric::graphid` raises `invalid input syntax for type graphid: "1"`.

There is no cast out of `graphid`. Use `graphid_labid()` and `graphid_locid()` for the parts,
or let it print.

## vertex and edge {#vertex-and-edge}

A `vertex` is a composite value of three fields: `id graphid`, `properties jsonb`, and a
`tid` holding the row's physical location. A write uses that `tid` to find the row again. An
`edge` has the same three fields plus `start graphid` and `end graphid`.

They print in a form that shows the label, the id and the properties:

```cypher
MATCH (p:person {name: 'Keanu Reeves'}) RETURN p;
```

```
                         p
---------------------------------------------------
 person[4.1]{"born": 1964, "name": "Keanu Reeves"}
```

An edge prints its endpoints between its id and its properties, start first:

```cypher
MATCH (:person {name: 'Keanu Reeves'})-[r:acted_in]->(:movie {title: 'The Matrix'}) RETURN r;
```

```
                   r
---------------------------------------
 acted_in[5.1][4.1,3.1]{"role": "Neo"}
```

So the shapes are `label[id]{properties}` for a vertex and
`label[id][start,end]{properties}` for an edge. An element with no properties prints an empty
map: `directed[6.8][4.8,3.5]{}`.

The `tid` field is not part of either printed form, and it is not something to depend on. It
changes when the row is updated.

### What you can do with them {#what-you-can-do-with-them}

`vertex` and `edge` each have the six comparison operators, and nothing else:

| Type | Operators |
| --- | --- |
| `graphid` | `=` `<>` `<` `<=` `>` `>=` |
| `vertex` | `=` `<>` `<` `<=` `>` `>=` |
| `edge` | `=` `<>` `<` `<=` `>` `>=` |
| `rowid` | `=` `<>` `<` `<=` `>` `>=` |
| `graphpath` | None |

**Comparison is on identity alone.** `vertex_eq` and its siblings compare the `id` field and
ignore properties entirely. Two vertices with identical properties and different ids are not
equal:

```cypher
CREATE GRAPH twins;
SET graph_path = twins;
CREATE VLABEL pair;
CREATE (:pair {k: 1}), (:pair {k: 1});
MATCH (a:pair), (b:pair) WHERE id(a) < id(b)
RETURN a, b, a = b AS equal, properties(a) = properties(b) AS same_properties;
```

```
         a         |         b         | equal | same_properties
-------------------+-------------------+-------+-----------------
 pair[3.1]{"k": 1} | pair[3.2]{"k": 1} | f     | t
```

Ordering follows from the same rule. `a < b` compares `graphid` values, so it is label order
first and then insertion order within a label. The order is total and stable, which makes it
a good tie-breaker in `ORDER BY`. It is not a meaningful ordering of your data.

```cypher
MATCH (a:person {name: 'Keanu Reeves'}), (b:person {name: 'Carrie-Anne Moss'})
RETURN a = b AS equal, a < b AS less, id(a) AS id_a, id(b) AS id_b;
```

```
 equal | less | id_a | id_b
-------+------+------+------
 f     | t    | 4.1  | 4.3
```

To compare properties instead, compare the properties: `properties(a) = properties(b)`, or
name the keys you mean.

Both types cast implicitly to `jsonb`. The cast keeps the property map and drops the
identity: `vertex_to_jsonb` and `edge_to_jsonb` in `pg_cast`. So `m::jsonb` is
`properties(m)`. There is no cast in the other direction.

## graphpath {#graphpath}

A `graphpath` is a composite of two arrays: `vertices vertex[]` and `edges edge[]`. A path of
*n* edges holds *n* + 1 vertices, so a path bound to a single vertex has one vertex and no
edges:

```cypher
MATCH p = (a:person {name: 'Keanu Reeves'}) RETURN p;
```

```
                          p
-----------------------------------------------------
 [person[4.1]{"born": 1964, "name": "Keanu Reeves"}]
```

It prints as a bracketed, comma-separated list of its members in walk order, alternating
vertex, edge, vertex. The two arrays are interleaved rather than printed as two arrays. So a
one-edge path prints three members, and a path of *n* edges prints 2*n* + 1.

Reach the members with `nodes()` and `edges()`, which hand back the two arrays. `length()`
is the edge count:

```cypher
MATCH p = (:person {name: 'Keanu Reeves'})-[:acted_in]->(:movie {title: 'The Matrix'})
RETURN length(p) AS hops, nodes(p)[0] AS first_vertex, edges(p)[0] AS only_edge;
```

```
 hops |                   first_vertex                    |               only_edge
------+---------------------------------------------------+---------------------------------------
 1    | person[4.1]{"born": 1964, "name": "Keanu Reeves"} | acted_in[5.1][4.1,3.1]{"role": "Neo"}
```

`graphpath` has **no operators of its own**, not equality and not ordering. In Cypher,
comparing two paths is refused. With no operator to call, the expression falls back to
`jsonb`, and a path is not a `jsonb` value:

```cypher
MATCH p1 = (:person {name:'Keanu Reeves'})-[:acted_in]->(:movie {title:'The Matrix'}),
      p2 = (:person {name:'Keanu Reeves'})-[:acted_in]->(:movie {title:'The Matrix'})
RETURN p1 = p2;
```

```
ERROR:  graph object cannot be jsonb
LINE 3: RETURN p1 = p2;
               ^
```

In SQL it does compare, through PostgreSQL's generic operators on composite values, which
walk the two arrays field by field:

```psql
SELECT a = b AS equal, a < b AS less
FROM (MATCH p = (:person {name:'Keanu Reeves'})-[:acted_in]->(:movie {title:'The Matrix'})
      RETURN p AS a) x,
     (MATCH p = (:person {name:'Keanu Reeves'})-[:acted_in]->(:movie {title:'The Matrix Reloaded'})
      RETURN p AS b) y;
```

```
 equal | less
-------+------
 f     | t
```

That comparison includes the `tid` fields, so it is an identity comparison of the whole walk
rather than a comparison of what the path means. Compare `nodes(p)` or the ids if you want
something you can reason about.

`to_jsonb()` converts a path, in Cypher and in SQL alike. The result exposes the internal
structure: both arrays, and the `tid` of every member. There is no `graphpath` to `jsonb`
cast in `pg_cast`. So `p::jsonb` works in Cypher, which lowers it, and fails in SQL with
`cannot cast type graphpath to jsonb`.

## rowid {#rowid}

`rowid` pairs a table OID with a row pointer. The shortest-path executor uses it internally
to carry edge identities. It has the six comparison operators and a btree operator class, and
it has **no output function**:

```sql
SELECT rowid('moviekb.person'::regclass, ctid) FROM moviekb.person LIMIT 1;
```

```
ERROR:  "rowid" type does not support output function
```

`rowid_tableoid()` and `rowid_ctid()` read the two halves, which is the only way to see a
value:

```sql
SELECT rowid_tableoid(rowid('moviekb.person'::regclass, '(0,1)')) AS tableoid,
       rowid_ctid(rowid('moviekb.person'::regclass, '(0,1)')) AS ctid;
```

```
 tableoid | ctid
----------+-------
    16482 | (0,1)
```

The OID is whatever `moviekb.person` happens to be in that database, so it differs from
installation to installation.

Nothing in Cypher produces a `rowid`, and there is no reason to use one in application code.
It is documented here because it appears in `pg_type` and in `\dT`.

## Arrays of graph types {#arrays-of-graph-types}

`vertex[]`, `edge[]` and `graphpath[]` are ordinary PostgreSQL array types with their own
output functions, so they print in the same bracketed style as their elements.

`collect()` over a vertex, an edge or a path returns one of these native arrays.
`collect()` over anything else returns `jsonb`:

```cypher
MATCH (:person {name: 'Keanu Reeves'})-[:acted_in]->(m:movie)
RETURN pg_typeof(collect(m)) AS collect_vertex, pg_typeof(collect(m.title)) AS collect_property;
```

```
 collect_vertex | collect_property
----------------+------------------
 "vertex[]"     | "jsonb"
```

A native array holds the elements themselves rather than a `jsonb` copy of each one, so its
members keep their identity. `films[0]` is a `vertex`, and you can read a property off it or
follow it in a later clause.

Several list functions carry one overload for `jsonb` and one for a native array. Which one
you get follows from the argument. From Cypher the argument is usually `jsonb`, so the result
is `jsonb`. Hand the same function a real array in SQL and you get a real array back.
[Type conversion functions](/agensgraph/reference/functions/type-conversion/) gives the signatures.

### Array index origin {#array-index-origin}

Cypher indexes a list from 0 and accepts negative indexes, and it applies that rule to a
native array too:

```cypher
MATCH (:person {name: 'Keanu Reeves'})-[:acted_in]->(m:movie)
WITH collect(m) AS films
RETURN films[0].title AS cypher_index_0, films[1].title AS cypher_index_1, size(films) AS n;
```

```
 cypher_index_0 |    cypher_index_1     | n
----------------+-----------------------+---
 "The Matrix"   | "The Matrix Reloaded" | 4
```

The same array reached from SQL follows PostgreSQL's rule and starts at 1, and index 0 is out
of bounds:

```psql
SELECT (films[1]).properties ->> 'title' AS sql_index_1,
       (films[0]).properties ->> 'title' AS sql_index_0
FROM (MATCH (:person {name: 'Keanu Reeves'})-[:acted_in]->(m:movie)
      RETURN collect(m) AS films) q;
```

```
 sql_index_1 | sql_index_0
-------------+-------------
 The Matrix  | null
```

`unnest()` turns one back into rows, which is usually what you want in SQL:

```psql
SELECT (v).id AS id, (v).properties ->> 'title' AS title
FROM (MATCH (:person {name: 'Keanu Reeves'})-[:acted_in]->(m:movie)
      RETURN collect(m) AS films) q,
     unnest(q.films) AS v ORDER BY id;
```

```
 id  |          title
-----+--------------------------
 3.1 | The Matrix
 3.2 | The Matrix Reloaded
 3.3 | The Matrix Revolutions
 3.4 | The Matrix Resurrections
```

## Properties: jsonb {#properties-jsonb}

A label has one `properties` column of type `jsonb`, and every property of every vertex or
edge in that label lives in it. So a property has no declared type: its type is whatever JSON
type its value is.

### What a property value may be {#what-a-property-value-may-be}

All six JSON types:

| JSON type | Written in Cypher as | Notes |
| --- | --- | --- |
| string | `'text'` | Single quotes. Escapes follow JSON's rules. |
| number | `42`, `1.5`, `1e3` | One JSON number type; no separate integer and float. |
| boolean | `true`, `false` | |
| array | `[1, 'two', null]` | May mix types and nest. |
| object | `{a: {b: 1}}` | Keys fold to lower case unless quoted. |
| null | `null` | Assigning null **removes** the property, unless [`allow_null_properties`](/agensgraph/reference/guc/#allow_null_properties) is on. |

```cypher
MATCH (m:movie {title: 'The Matrix'})-[r:related_to]->()
RETURN jsonb_typeof(m.title) AS title, jsonb_typeof(m.embedding) AS embedding,
       jsonb_typeof(r.weight) AS weight, jsonb_typeof(m.no_such_key) AS absent
LIMIT 1;
```

```
  title   | embedding |  weight  | absent
----------+-----------+----------+--------
 "string" | "array"   | "number" | null
```

An absent property and a null property are the same thing. So `jsonb_typeof` of a missing
key is null rather than `"null"`.

There is one number type, but the scale you wrote is stored, and it decides whether division
truncates:

```cypher
CREATE GRAPH demo;
SET graph_path = demo;
CREATE VLABEL t;
CREATE (:t {a: 7, b: 7.0});
MATCH (n:t) RETURN n.a AS a, n.b AS b, n.a / 2 AS a_div, n.b / 2 AS b_div;
```

```
 a |  b  | a_div |       b_div
---+-----+-------+--------------------
 7 | 7.0 | 3     | 3.5000000000000000
```

`n.a` and `n.b` are both `jsonb_typeof` `number` and they compare equal, so this is not two
types. It is one type that remembers how many decimal places it was given.

Because there is no declared type, `jsonb` comparison decides how values of different types
order: null, then string, then number, then boolean, then array, then object. That order is
PostgreSQL's. It is the reason a property promoted to a typed column can sort differently
from the same property read out of the bag.

### What a RETURN hands back {#what-a-return-hands-back}

A Cypher `RETURN` boxes each scalar output column to `jsonb`. A `boolean` stays a boolean, and
a graph type stays itself:

```psql
SELECT pg_typeof(a) AS property, pg_typeof(b) AS property_cast_to_text,
       pg_typeof(c) AS string_literal, pg_typeof(d) AS number_literal,
       pg_typeof(e) AS boolean, pg_typeof(f) AS id, pg_typeof(g) AS vertex,
       pg_typeof(h) AS path
FROM (MATCH p = (:person {name: 'Keanu Reeves'})-[:acted_in]->(m:movie {title: 'The Matrix'})
      RETURN m.title AS a, m.title::text AS b, 'x' AS c, 1 AS d, true AS e,
             id(m) AS f, m AS g, p AS h) q;
```

```
 property | property_cast_to_text | string_literal | number_literal | boolean |   id    | vertex |   path
----------+-----------------------+----------------+----------------+---------+---------+--------+-----------
 jsonb    | jsonb                 | jsonb          | jsonb          | boolean | graphid | vertex | graphpath
```

Note the second column: a `::text` cast inside a `RETURN` is undone by the boxing, so it
changes nothing. A string therefore prints with its JSON quotes:

```cypher
MATCH (m:movie {title: 'The Matrix'}) RETURN m.title AS title;
```

```
    title
--------------
 "The Matrix"
```

To get a plain scalar, take the value out of `jsonb` in SQL. `#>> '{}'` extracts the whole
document as text:

```psql
SELECT title #>> '{}' AS title
FROM (MATCH (m:movie {title: 'The Matrix'}) RETURN m.title AS title) q;
```

```
   title
------------
 The Matrix
```

[Combining SQL and Cypher](/agensgraph/querying/combining-sql-and-cypher/) covers the wrapping in
full. Boxing applies to property-derived columns only. A boolean expression stays
`boolean`, `id(n)` stays `graphid`, and a graph element stays `vertex`, `edge` or
`graphpath`. A property that has been promoted to a typed column is also exempt:
that read is answered from the column and comes back in the column's own type.

### The :: cast {#the--cast}

Cypher's `::` accepts a smaller set of type names than SQL's does. It takes a bare type or
function name, such as `text`, `date`, `uuid`, `jsonb` or `inet`. It also takes the grouped
spellings the SQL grammar treats specially. Those are the numeric names (`int`, `integer`,
`smallint`, `bigint`, `real`, `float`, `double precision`, `decimal`, `numeric`, `boolean`)
and the character names (`char`, `varchar`, `character varying`), plus `bit`, `bit varying`,
`json` and `interval`.

```cypher
RETURN '42'::int AS i, '4.2'::numeric AS n, 'x'::text AS t, '101'::bit(3) AS b,
       '1 day'::interval AS iv, 'true'::boolean AS bo, '2020-01-01'::date AS d;
```

```
 i  |  n  |  t  |   b   |   iv    | bo |      d
----+-----+-----+-------+---------+----+--------------
 42 | 4.2 | "x" | "101" | "1 day" | t  | "2020-01-01"
```

The reason is how a cast names its type. A Cypher cast takes an ordinary type name. It also
takes the numeric, character, bit, json and interval spellings, which the language treats
specially. `TIMESTAMP` and `TIME` are special spellings too, and they are the two that were
left out. So both are refused:

```cypher
RETURN '2020-01-01 10:00'::timestamp;
```

```
ERROR:  syntax error at or near "timestamp"
LINE 1: RETURN '2020-01-01 10:00'::timestamp;
                                   ^
```

```cypher
RETURN '10:00'::time;
```

```
ERROR:  syntax error at or near "time"
LINE 1: RETURN '10:00'::time;
                        ^
```

Quote the type name. A quoted name is an identifier rather than a keyword, so it goes through
the rule that does work. It names the same type:

```cypher
RETURN '2020-01-01 10:00'::"timestamp" AS ts, '10:00'::"time" AS t;
```

```
          ts           |     t
-----------------------+------------
 "2020-01-01T10:00:00" | "10:00:00"
```

Everything else temporal is an ordinary name and needs no quoting, `date` and `timestamptz`
included:

```cypher
RETURN pg_typeof('2020-01-01'::date) AS d, pg_typeof('2020-01-01'::timestamptz) AS tz;
```

```
   d    |             tz
--------+----------------------------
 "date" | "timestamp with time zone"
```

The other route is to cast outside the Cypher, where the whole SQL grammar is available:

```psql
SELECT (t #>> '{}')::timestamp AS released FROM (RETURN '2020-01-01 10:00' AS t) q;
```

```
      released
---------------------
 2020-01-01 10:00:00
```

Note the difference in the two results. Inside Cypher the value is boxed back to `jsonb`, so
it prints in JSON's ISO form with quotes. The SQL cast gives a real `timestamp`, printed by
that type's output function.

One more asymmetry to know. `'…'::jsonb` on a string literal produces a `jsonb` **string**,
not a parsed document, because the literal is already a JSON string. To build a `jsonb`
object in Cypher, write a map literal:

```cypher
RETURN '{"a": 1}'::jsonb AS as_string, {a: 1} AS as_map;
```

```
  as_string   |  as_map
--------------+----------
 "{\"a\": 1}" | {"a": 1}
```

## Which PostgreSQL types you can use {#which-postgresql-types-you-can-use}

All of them. A graph lives in the same database as your tables, so every type in
[PostgreSQL's data-type chapter](https://www.postgresql.org/docs/18/datatype.html) is
available unchanged. That covers numeric, character, date/time, boolean, enumerated,
geometric, network address, bit string, text search, UUID, XML, JSON, array, composite,
range, domain and object identifier. Any type an extension adds is available too.

Three places a PostgreSQL type meets a graph:

* **An ordinary table** beside the graph, joined to it in one statement. This is where a
  `timestamptz`, a `numeric(10,2)` or a `tsvector` belongs when you need its semantics and
  its operators.
* **A promoted column** on a label, which materialises one property as a real column of a
  real type, so that property gets that type's ordering, comparison and index support.
* **An extension type** stored in a property or a promoted column. `vector` from `pgvector`
  is the case [vector search](/agensgraph/guides/search/vector/) builds on.

A property itself cannot be any of those types. A property is `jsonb`, and a value put into
one is converted to a JSON type on the way in.

## Compatibility {#compatibility}

### openCypher {#opencypher}

`vertex`, `edge` and `graphpath` are the node, relationship and path of openCypher's type
system. The scalar types are not separate here: string, number, boolean, list and map are all
`jsonb`. So a number's integer-or-decimal character comes from the value rather than from a
declared type.

Temporal values are not graph types. `date`, `timestamptz` and `interval` are PostgreSQL's,
reached through a cast, an ordinary column or a promoted one. There is no graph-level
`datetime` or `duration`. [Cypher compatibility](/agensgraph/appendix/cypher-compatibility/) is the
full list of differences.

### ISO/IEC 39075 {#isoiec-39075}

The standard's property graph types line up with `vertex`, `edge` and `graphpath` in the same
way. A promoted column provides its typed-value model, in which a property carries a
declared type. See [GQL conformance](/agensgraph/appendix/gql-conformance/).

## See also {#see-also}

- [Syntax](/agensgraph/reference/syntax/) — literals, operators and how a value is written
- [Server settings](/agensgraph/reference/guc/) — `allow_null_properties` and `enable_property_promotion`
- [How a graph is stored](/agensgraph/concepts/graph-on-postgresql/) — what a label table
  is made of
- [Combining SQL and Cypher](/agensgraph/querying/combining-sql-and-cypher/) — getting values across
  the boundary
- [System catalogs](/agensgraph/system-catalogs/catalogs/) — `ag_graph`, `ag_label` and the rest
- [PostgreSQL: data types](https://www.postgresql.org/docs/18/datatype.html) — every other
  type you can use
