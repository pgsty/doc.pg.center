---
title: Path functions
linkTitle: Path functions
description: Functions over a graphpath, and the three path-finding forms that produce one.
type: docs
weight: 80
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/functions/path.html
upstream_source: agensgraph
upstream_modified: true
---


Functions over a `graphpath`, and the three path-finding forms that produce one. A
`graphpath` is the alternating sequence of vertices and edges that a `MATCH p = (...)`
binds.

A path is bound by naming it: `MATCH p = (a)-[r]->(b)`. These functions take the *variable*,
not the pattern.

Examples run against [the example dataset](/agensgraph/get-started/example-dataset/).

## allshortestpaths {#allshortestpaths}

```
allshortestpaths ( pattern ) -> graphpath
```

Finds every shortest path between two vertices. It returns one row per path when it names a
path variable, and an array of paths when it is used as an expression.

**Considerations**

- The pattern must hold exactly one relationship, or the parser raises
  `only one relationship is allowed`. Give that relationship a length range, such as `*..4`,
  rather than writing more hops.
- Multi-type relationship patterns are not supported anywhere, `allshortestpaths` included.
  Match an untyped edge and filter with `WHERE label(r) IN [...]`.
- As an expression it yields `graphpath[]`, so `length()` over it counts the paths found,
  not the edges in one path.

```cypher
MATCH (a:movie {title:'The Matrix'}), (b:movie {title:'Inception'})
RETURN length(allshortestpaths((a)-[:related_to*..4]->(b))) AS paths_found;
```

```
 paths_found
-------------
 1
```

## dijkstra {#dijkstra}

```
dijkstra ( pattern, weight ) -> graphpath
dijkstra ( pattern, weight, condition ) -> graphpath
dijkstra ( pattern, weight, LIMIT count ) -> graphpath
dijkstra ( pattern, weight, condition, LIMIT count ) -> graphpath
```

Finds the cheapest path between two vertices, where each edge costs what `weight` evaluates
to.

| Name | Type | Description |
| --- | --- | --- |
| `pattern` | path chain | Exactly one relationship between two vertices, for example `(a)-[e:related_to]->(b)`. Give the relationship a variable if `weight` reads a property of it. |
| `weight` | numeric expression | Cost of traversing one edge. Must be greater than 0 for every edge considered. |
| `condition` | boolean expression | Optional filter on the edge. Only edges satisfying it are traversed. |
| `count` | integer | Optional. Number of alternative paths to return, cheapest first. Must be greater than 0. |

**Considerations**

- Written as a pattern part it binds a path: `p = dijkstra(...)`. Written as
  `(p, w) = dijkstra(...)` it binds the path *and* its total weight, which is otherwise not
  available.
- Without `LIMIT` the count defaults to 1, so one path comes back.
- The pattern accepts neither a property constraint nor a variable-length relationship.
  Filter in `WHERE` instead.

```cypher
MATCH (a:movie {title:'The Matrix'}), (b:movie {title:'Inception'}),
      p = dijkstra((a:movie {title:'The Matrix'})-[e:related_to]->(b), e.weight)
RETURN p;
```

```
ERROR:  property constraint is not supported
LINE 2:       p = dijkstra((a:movie {title:'The Matrix'})-[e:related...
                            ^
```

```cypher
MATCH (a:movie {title:'The Matrix'}), (b:movie {title:'Inception'}),
      p = dijkstra((a)-[e:related_to*]->(b), e.weight)
RETURN p;
```

```
ERROR:  variable length relationship is not supported
```

- The third positional argument is a condition, so a number there raises
  `cannot cast 1 (jsonb type numeric) to boolean`.
- Two more refusals come at run time, once an edge is reached, so they depend on the data
  rather than on the query alone. A weight that evaluates to 0 or less reports
  `WEIGHT must be larger than 0`, and `LIMIT 0` reports `LIMIT must be larger than 0`.
- Used as a bare expression rather than assigned, it yields `graphpath[]`.

The cheapest route is not the shortest one. Two hops through *Total Recall* cost 4 + 2,
which beats the single-hop alternatives on this graph:

```cypher
MATCH (a:movie {title:'The Matrix'}), (b:movie {title:'Inception'}),
      (p, w) = dijkstra((a)-[e:related_to]->(b), e.weight)
RETURN [x IN nodes(p) | x.title] AS route, w AS weight;
```

```
                    route                    | weight
---------------------------------------------+--------
 ["The Matrix", "Total Recall", "Inception"] | 6
```

Leaving the far endpoint unconstrained gives the cheapest route to every reachable film:

```cypher
MATCH p = dijkstra((a:movie)-[e:related_to]->(b:movie), e.weight, LIMIT 1)
WHERE a.title = 'The Matrix'
RETURN [x IN nodes(p) | x.title] AS route ORDER BY route;
```

```
                                            route
---------------------------------------------------------------------------------------------
 ["The Matrix"]
 ["The Matrix", "The Matrix Reloaded"]
 ["The Matrix", "The Terminator"]
 ["The Matrix", "Total Recall"]
 ["The Matrix", "The Matrix Reloaded", "The Matrix Revolutions"]
 ["The Matrix", "The Terminator", "Terminator 2: Judgment Day"]
 ["The Matrix", "Total Recall", "Inception"]
 ["The Matrix", "The Matrix Reloaded", "The Matrix Revolutions", "The Matrix Resurrections"]
```

The rows come back in no particular order without an `ORDER BY`; the sort above only makes
the page reproducible.

> [!NOTE]
> A path found by `dijkstra` is a `graphpath` like any other, so `nodes()`, `relationships()`
> and `length()` all read it. What no other path carries is the total weight, and only the
> `(p, w) =` form exposes it.

## edges {#edges}

```
edges ( p graphpath ) -> edge[]
```

Returns the edges of a path, in order. [`relationships`](#relationships) is the same
function under the name Cypher uses.

## end_vertex {#end_vertex}

```
end_vertex ( e edge ) -> vertex
```

Returns the vertex an edge points at. `endNode` is the same function under the name Cypher
uses; both are listed on the [scalar page](/agensgraph/reference/functions/scalar/#endnode).

**Considerations**

- Reading the vertex means fetching its row. When the identity is enough, use
  [`end_id`](/agensgraph/reference/functions/scalar/#end_id), which reads a column of the edge itself.

## length {#length}

```
length ( p graphpath ) -> jsonb
length ( vs vertex[] ) -> jsonb
length ( es edge[] ) -> jsonb
length ( ps graphpath[] ) -> jsonb
```

Over a path, returns the number of edges in it. Over an array, returns the number of
elements.

**Considerations**

- The number of edges, not of elements: a one-edge path has length 1 while
  [`cardinality`](/agensgraph/reference/functions/list/#cardinality) of the same path is 3.
- Because `allshortestpaths()` and an unassigned `dijkstra()` yield `graphpath[]`,
  `length()` over one of those counts paths.
- Over a string, a list or a map, `length` is a different function; see
  [`length`](/agensgraph/reference/functions/scalar/#length) on the scalar page.

```cypher
MATCH (a:movie {title:'The Matrix'}), (b:movie {title:'The Matrix Resurrections'})
RETURN length(shortestpath((a)-[:related_to*]->(b))) AS hops;
```

```
 hops
------
 3
```

## nodes {#nodes}

```
nodes ( p graphpath ) -> vertex[]
```

Returns the vertices of a path, in order, starting with the one the path starts at.

**Considerations**

- The result is `vertex[]`, a native array, so a Cypher `RETURN` does not box it to `jsonb`.
  Subscripting is still 0-based.
- `vertices` is the same function under another name.
- Pass the path *variable*. A pattern written inline is not an expression and will not parse.
- Printing whole vertices is rarely what you want, since each carries its full property bag.
  Project the field you need with a list comprehension, as below.

```cypher
MATCH p=(:person {name:'Christopher Nolan'})-[:directed]->(:movie {title:'Inception'})
RETURN [x IN nodes(p) | x.name] AS names, [x IN nodes(p) | x.title] AS titles;
```

```
            names            |       titles
-----------------------------+---------------------
 ["Christopher Nolan", null] | [null, "Inception"]
```

Every vertex of the path is projected, so the key a given vertex does not carry comes back
as null.

## relationships {#relationships}

```
relationships ( p graphpath ) -> edge[]
```

Returns the edges of a path, in order. Identical to [`edges`](#edges).

```cypher
MATCH p=(:person {name:'Christopher Nolan'})-[:directed]->(:movie {title:'Inception'})
RETURN relationships(p) AS edges;
```

```
           edges
----------------------------
 [directed[6.8][4.8,3.5]{}]
```

## shortestpath {#shortestpath}

```
shortestpath ( pattern ) -> graphpath
```

Finds one shortest path between two vertices, by number of edges. If several are equally
short, one of them is returned.

**Considerations**

- The pattern must hold exactly one relationship, and that relationship carries the length
  range. Writing the hops out is refused:

```cypher
MATCH (a:movie {title:'The Matrix'}), (b:movie {title:'Inception'})
RETURN shortestpath((a)-[:related_to]->()-[:related_to]->(b));
```

```
ERROR:  only one relationship is allowed
LINE 2: RETURN shortestpath((a)-[:related_to]->()-[:related_to]->(b)...
                            ^
```
- Which of several equally short paths you get is not defined. Use
  [`allshortestpaths`](#allshortestpaths) when you need them all.
- Returns no row when no path exists, rather than a null path.
- Multi-type relationship patterns are not supported here either.

```cypher
MATCH (a:movie {title:'The Matrix'}), (b:movie {title:'The Matrix Resurrections'})
RETURN [x IN nodes(shortestpath((a)-[:related_to*]->(b))) | x.title] AS route;
```

```
                                            route
---------------------------------------------------------------------------------------------
 ["The Matrix", "The Matrix Reloaded", "The Matrix Revolutions", "The Matrix Resurrections"]
```

## start_vertex {#start_vertex}

```
start_vertex ( e edge ) -> vertex
```

Returns the vertex an edge leaves. `startNode` is the same function under the name Cypher
uses; see [`startNode`](/agensgraph/reference/functions/scalar/#startnode).

A vertex is a composite, so a property can be read straight off the result:

```cypher
MATCH (:person {name:'Keanu Reeves'})-[e:acted_in]->(:movie {title:'The Matrix'})
RETURN start_vertex(e).name AS actor, end_vertex(e).title AS film;
```

```
     actor      |     film
----------------+--------------
 "Keanu Reeves" | "The Matrix"
```

## vertices {#vertices}

```
vertices ( p graphpath ) -> vertex[]
```

Returns the vertices of a path, in order. Identical to [`nodes`](#nodes).

## Compatibility {#compatibility}

### openCypher {#opencypher}

`shortestPath` and `allShortestPaths` are spelled without regard to case, so openCypher's
capitalisation works. openCypher has no `dijkstra`; weighted shortest paths there come from
a procedure library.

openCypher allows a relationship pattern to name several types, as
`-[r:acted_in|directed]->`. That raises `multiple types for relationship not supported` at
every length and inside every path-finding form. Match an untyped relationship and test the
label instead:

```cypher
MATCH (p:person)-[r]->(m:movie) WHERE label(r) IN ['acted_in','directed'] RETURN count(r) AS n;
```

```
 n
----
 46
```

## See also {#see-also}

- [All functions](/agensgraph/reference/functions/all-functions/) — every function in one table
- [Scalar functions](/agensgraph/reference/functions/scalar/) — `startNode`, `endNode`, `start_id`, `end_id`
- [List functions](/agensgraph/reference/functions/list/) — `cardinality` over a path
- [Syntax](/agensgraph/reference/syntax/) — path patterns and flexible length
