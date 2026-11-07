---
title: Scalar functions
linkTitle: Scalar functions
description: Functions that take a value and return a single value.
type: docs
weight: 40
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/functions/scalar.html
upstream_source: agensgraph
upstream_modified: true
---


Functions that take a value and return a single value. They cover the parts of a graph
element, the pieces of a `graphid`, and the length of a string or list. The
server-information functions here report what a build is and what the last write did.

Examples run against [the example dataset](/agensgraph/get-started/example-dataset/).

## agversion {#agversion}

```
agversion ( ) -> text
```

Returns the AgensGraph version of the running server, without the PostgreSQL part that
`version()` also carries.

**Considerations**

- `agversion` is also a read-only setting, so `SHOW agversion` returns the same string. The
  function is the form you can use inside an expression.
- The value is the fork's own version, not PostgreSQL's. Read `version()` for both.

```sql
SELECT agversion();
```

```
 agversion
------------
 2.18.6.1
```

## ag_get_graphconstraintdef {#ag_get_graphconstraintdef}

```
ag_get_graphconstraintdef ( constraint oid ) -> text
```

Reconstructs the `CREATE CONSTRAINT` command for a graph constraint, given its OID. This is
the graph counterpart of `pg_get_constraintdef` and is what `pg_dump` uses.

## ag_get_propindexdef {#ag_get_propindexdef}

```
ag_get_propindexdef ( index oid ) -> text
```

Reconstructs the `CREATE PROPERTY INDEX` command for a property index, given its OID.

**Considerations**

- A property index is an expression index over the `properties` column, so
  `pg_get_indexdef` prints it as SQL. This function prints the Cypher form instead.

## coalesce {#coalesce}

```
coalesce ( value [, value ] ... ) -> jsonb
```

Returns the first argument that is not null.

**Considerations**

- This is an expression form rather than a function, so it will not appear in a catalog
  listing of functions.
- A property reference is always `jsonb`. If any argument is `jsonb`, every argument is
  coerced to `jsonb` and the result is `jsonb`. Otherwise the arguments settle on a common
  type and keep it, so `coalesce(v1, v2)` over two vertices returns a `vertex`.
- Mixing a graph element with anything else therefore fails, because the element cannot be
  boxed. Pass `m::jsonb` instead.
- Arguments after the first non-null one are not evaluated.

```cypher
MATCH (m:movie {title:'Inception'}) RETURN coalesce(m, 0);
```

```
ERROR:  COALESCE types vertex and integer cannot be matched
LINE 1: MATCH (m:movie {title:'Inception'}) RETURN coalesce(m, 0);
                                                               ^
```

```cypher
MATCH (m:movie {title:'Inception'}) RETURN coalesce(m.budget, m.year, 0) AS first_present;
```

```
 first_present
---------------
 2010
```

## datetime {#datetime}

```
datetime ( ) -> timestamp with time zone
datetime ( timezone "any" ) -> timestamp without time zone
datetime ( year integer, month integer, mday integer, hour integer, min integer, sec integer, millisec integer, nanosec integer, timezone "any" ) -> timestamp without time zone
```

Returns the current transaction timestamp, the current time in a named zone, or a timestamp
built from its parts.

| Name | Type | Description |
| --- | --- | --- |
| `year`, `month`, `mday` | `integer` | Calendar date. |
| `hour`, `min`, `sec` | `integer` | Time of day. |
| `millisec`, `nanosec` | `integer` | Sub-second parts. Nanoseconds beyond microsecond resolution are truncated. |
| `timezone` | `"any"` | Zone name or abbreviation, for example `'Asia/Seoul'`. |

**Considerations**

- The no-argument form is stable, so every row of one query sees the same instant, and it
  changes between transactions.
- The zone forms return `timestamp without time zone`: the wall-clock reading in that zone,
  with the zone itself discarded.
- A `RETURN` boxes the result to a `jsonb` string in ISO 8601 form.

```sql
SELECT datetime('Asia/Seoul'), datetime(2020, 1, 2, 3, 4, 5, 0, 0, 'UTC');
```

```
          datetime          |      datetime
----------------------------+---------------------
 2026-09-02 16:52:34.625259 | 2020-01-02 03:04:05
```

## endNode {#endnode}

```
endNode ( e edge ) -> vertex
```

Returns the vertex an edge points at. `end_vertex` is the same function under a different
name; see [`end_vertex`](/agensgraph/reference/functions/path/#end_vertex) on the path page.

## end_id {#end_id}

```
end_id ( e edge ) -> graphid
```

Returns the `graphid` of the vertex an edge points at, without reading that vertex.

**Considerations**

- An edge table stores `start` and `end` as columns, so this costs nothing beyond the edge
  row itself, while `endNode()` has to fetch the vertex.
- Use it whenever you only need to compare or group identities.

```cypher
MATCH ()-[e:acted_in]->() WITH e ORDER BY id(e) LIMIT 1
RETURN start_id(e) AS from_id, end_id(e) AS to_id;
```

```
 from_id | to_id
---------+-------
 4.1     | 3.1
```

## get_last_graph_write_stats {#get_last_graph_write_stats}

```
get_last_graph_write_stats ( ) -> record
```

Reports what the most recent graph write in this session changed, as one row of five
counters: `insertedvertices`, `insertededges`, `deletedvertices`, `deletededges` and
`updatedproperties`.

**Considerations**

- The counters describe the last graph-writing statement only, not the session total.
- A statement that writes nothing leaves the previous statement's counters in place rather
  than zeroing them, so read the row immediately after the write you care about.
- Call it from SQL: it returns a record, and Cypher has no way to expand one.

```sql
SELECT * FROM get_last_graph_write_stats();
```

```
 insertedvertices | insertededges | deletedvertices | deletededges | updatedproperties
------------------+---------------+-----------------+--------------+-------------------
                1 |             0 |               0 |            0 |                 0
```

## get_time {#get_time}

```
get_time ( ) -> time without time zone
get_time ( timezone "any" ) -> time without time zone
```

Returns the current time of day, either locally or in a named zone.

**Considerations**

- Both forms are marked immutable, so the planner folds the call to a constant. Every row of
  a query sees the same time, and so does every execution of a prepared statement. Read the
  time from `localdatetime()`, which is stable, or from SQL's `localtime`, when you need it
  to advance.

```sql
SELECT get_time(), get_time('Asia/Seoul');
```

```
    get_time    |    get_time
----------------+-----------------
 12:52:34.62488 | 16:52:34.625259
```

## graphid {#graphid}

```
graphid ( labid integer, locid bigint ) -> graphid
graphid ( id numeric ) -> graphid
```

Builds a `graphid` from a label id and a local id, or from the `labid.locid` number that a
`graphid` prints as.

**Considerations**

- This is how a label's `id` column default is written; see
  [how a graph maps onto PostgreSQL](/agensgraph/concepts/graph-on-postgresql/).
- The numeric form is a convenience for hand-written SQL. It does not check that the label
  exists.

```sql
SELECT graphid(4, 1), graphid(4.1::numeric);
```

```
 graphid | graphid
---------+---------
 4.1     | 4.1
```

## graph_labid {#graph_labid}

```
graph_labid ( qualified_label cstring ) -> integer
```

Returns the label id of a label named as `graph.label`.

```sql
SELECT graph_labid('moviekb.person');
```

```
 graph_labid
-------------
           4
```

## graphid_labid {#graphid_labid}

```
graphid_labid ( id graphid ) -> integer
```

Returns the label part of a `graphid`: the number before the dot.

**Considerations**

- A `graphid` packs the label id into its top 16 bits and the local id into the rest. A
  whole label therefore occupies one contiguous range of `graphid` values, and a label test
  can be answered by an index range scan without touching a catalog.

## graphid_locid {#graphid_locid}

```
graphid_locid ( id graphid ) -> bigint
```

Returns the local part of a `graphid`: the number after the dot, taken from the label's
sequence.

```cypher
MATCH (n:person {name:'Keanu Reeves'})
RETURN id(n) AS id, graphid_labid(id(n)) AS label_id, graphid_locid(id(n)) AS local_id;
```

```
 id  | label_id | local_id
-----+----------+----------
 4.1 | 4        | 1
```

## id {#id}

```
id ( v vertex ) -> graphid
id ( e edge ) -> graphid
```

Returns a graph element's identity.

**Considerations**

- This is not a catalog function. A `vertex` is the composite type `(id, properties)` and an
  `edge` is `(id, start, end, properties)`. So `id(v)` is PostgreSQL's functional spelling of
  field selection (`parse_func.c:1961`). The same mechanism gives you `properties(v)`.
- `n.id` is **not** the same thing. It reads a *property* named `id`, which the example
  dataset does not have, so it returns null. Write `id(n)`.
- A `RETURN` leaves the result as `graphid`, not boxed to `jsonb`. Aggregating it does box
  it: `min(id(n))` comes back as the `jsonb` string `"4.1"`.

```cypher
MATCH (n:person {name:'Keanu Reeves'}) RETURN id(n) AS identity, n.id AS property_named_id;
```

```
 identity | property_named_id
----------+-------------------
 4.1      |
```

## label {#label}

```
label ( v vertex ) -> jsonb
label ( e edge ) -> jsonb
```

Returns the name of the label a graph element was created with, as a `jsonb` string.

**Considerations**

- `label` and [`labels`](#labels) are different functions, not spellings of one. `label`
  returns one string, the element's own label. `labels` returns a list of that label
  followed by the labels it inherits from.
- `label` works on edges as well as vertices; `labels` does not. For an edge, `label(e)` and
  [`type(e)`](#type) are the same call.

```cypher
MATCH (n:person {name:'Keanu Reeves'}) RETURN label(n) AS own, labels(n) AS own_and_inherited;
```

```
   own    | own_and_inherited
----------+-------------------
 "person" | ["person"]
```

The two answers diverge only where a label inherits. Add a label with a parent:

```cypher
CREATE VLABEL creature;
CREATE VLABEL dragon INHERITS (creature);
CREATE (:dragon {name: 'Smaug'});
```

```cypher
MATCH (d:dragon) RETURN label(d) AS own, labels(d) AS own_and_inherited;
```

```
   own    |   own_and_inherited
----------+------------------------
 "dragon" | ["dragon", "creature"]
```

Then take it back out:

```cypher
MATCH (d:dragon) DETACH DELETE d;
DROP VLABEL dragon;
DROP VLABEL creature;
```

An edge has no `labels()`:

```cypher
MATCH ()-[e:acted_in]->() WITH e LIMIT 1 RETURN labels(e);
```

```
ERROR:  function labels(edge) does not exist
LINE 1: MATCH ()-[e:acted_in]->() WITH e LIMIT 1 RETURN labels(e);
                                                        ^
HINT:  No function matches the given name and argument types. You might need to add explicit type casts.
```

## labels {#labels}

```
labels ( v vertex ) -> jsonb
```

Returns a list holding the vertex's own label and every label it inherits from, nearest
first.

**Considerations**

- Vertices only. There is no `labels(edge)`.
- The list has one element for a label with no parent, which is the common case.

## length {#length}

```
length ( value jsonb ) -> jsonb
```

Returns the number of characters in a string, elements in a list, or keys in a map.

**Considerations**

- [`size`](#size) is the Cypher spelling of this function; the parser rewrites it, so the
  result column is named `length`.
- Over a path or an array of graph elements, `length` is a different function with a
  different meaning: the number of edges in the path. See [`length`](/agensgraph/reference/functions/path/#length) on the
  path page.
- A number returns the length of its text form rather than raising.

```cypher
RETURN length('The Matrix') AS characters, length([1,2,3]) AS elements, length({a:1,b:2}) AS keys;
```

```
 characters | elements | keys
------------+----------+------
 10         | 3        | 2
```

## localdatetime {#localdatetime}

```
localdatetime ( ) -> timestamp with time zone
localdatetime ( timezone "any" ) -> timestamp without time zone
```

Returns the current transaction timestamp, or the current wall-clock reading in a named
zone.

**Considerations**

- The no-argument form returns the same value as `datetime()`, including the same type. The
  two names exist for GQL compatibility; neither drops the zone.
- The zone form returns `timestamp without time zone`, as `datetime(zone)` does.
- Both forms are stable, so a value taken from them does advance between transactions,
  unlike [`get_time`](#get_time).

## properties {#properties}

```
properties ( v vertex ) -> jsonb
properties ( e edge ) -> jsonb
```

Returns a graph element's whole property bag as a map.

**Considerations**

- Like [`id`](#id), this is field selection on the composite type rather than a catalog
  function, so it costs no more than reading the column.
- `vertex_to_jsonb` and `edge_to_jsonb` return the same map, and are the functions the cast
  `v::jsonb` uses.
- Reading the bag detoasts it in full. If you only want one key, read that key.

```cypher
MATCH (n:person {name:'Keanu Reeves'}) RETURN properties(n) AS bag;
```

```
                  bag
----------------------------------------
 {"born": 1964, "name": "Keanu Reeves"}
```

## regather_graphmeta {#regather_graphmeta}

```
regather_graphmeta ( ) -> boolean
```

Empties `ag_graphmeta` and rebuilds it by scanning every edge label in the current graph.
`ag_graphmeta` records which label triples occur and how many edges make up each, and the
planner uses it to skip label tables a pattern cannot match.

**Considerations**

- The scan reads every edge in the graph, so the cost grows with the graph.
- `auto_gather_graphmeta` keeps the table current as writes happen. Rebuild by hand after a
  bulk load done with that setting off.
- Emits `NOTICE: regathering graphmeta...` and returns true.

```sql
SELECT regather_graphmeta();
```

```
NOTICE:  regathering graphmeta...
 regather_graphmeta
--------------------
 t
```

## size {#size}

```
size ( value ) -> jsonb
size ( pattern ) -> bigint
```

With a value, returns its length. With a pattern, returns the number of times the pattern
matches.

**Considerations**

- The two forms are told apart by the opening character. A pattern always starts with `(`,
  so anything that cannot is read as a value. The value form becomes [`length`](#length), so
  the result column is named `length`. The pattern form becomes a counting subquery, so it is
  named `count`.
- A `shortestpath` or `allshortestpaths` argument keeps its established meaning, the number
  of paths found, rather than being read as a pattern.

```cypher
MATCH (a:person {name:'Keanu Reeves'}) RETURN size((a)-[]->()) AS edges, size(a.name) AS name_length;
```

```
 edges | name_length
-------+-------------
 4     | 12
```

## startNode {#startnode}

```
startNode ( e edge ) -> vertex
```

Returns the vertex an edge leaves. `start_vertex` is the same function under a different
name; see [`start_vertex`](/agensgraph/reference/functions/path/#start_vertex) on the path page.

## start_id {#start_id}

```
start_id ( e edge ) -> graphid
```

Returns the `graphid` of the vertex an edge leaves, without reading that vertex. The
considerations for [`end_id`](#end_id) apply.

## type {#type}

```
type ( e edge ) -> jsonb
```

Returns the name of an edge's label, as a `jsonb` string. It is the same value as
`label(e)`, under the name Cypher uses for relationship types.

**Considerations**

- Edges only. Over a vertex it is refused; use [`label`](#label).

```cypher
MATCH (m:movie {title:'Inception'}) RETURN type(m);
```

```
ERROR:  function type(vertex) does not exist
LINE 1: MATCH (m:movie {title:'Inception'}) RETURN type(m);
                                                   ^
HINT:  No function matches the given name and argument types. You might need to add explicit type casts.
```

```cypher
MATCH ()-[e:acted_in]->() WITH e LIMIT 1 RETURN type(e) AS relationship_type;
```

```
 relationship_type
-------------------
 "acted_in"
```

## Compatibility {#compatibility}

### openCypher {#opencypher}

`id()` returns a `graphid`, a label id and a sequence number, not the integer openCypher
returns. It is stable for the life of the element and unique across the graph. But it is not
a small dense integer, and arithmetic on it is meaningless.

openCypher's `labels()` returns every label a node carries, because a node there may carry
several. A vertex here has exactly one label, and `labels()` returns that label plus the
labels it inherits from.

## See also {#see-also}

- [All functions](/agensgraph/reference/functions/all-functions/) — every function in one table
- [Path functions](/agensgraph/reference/functions/path/) — `nodes`, `relationships`, `length` over a path
- [jsonb operators and functions](/agensgraph/reference/functions/jsonb/) — reading the map `properties()` returns
- [Graph metadata functions](/agensgraph/system-catalogs/graph-metadata/) — the `meta.*` schema
