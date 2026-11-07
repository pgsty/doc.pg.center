---
title: Paths
linkTitle: Paths
description: A fixed pattern asks a question whose shape you already know. (a)-[]->(b)-[]->(c) is two hops, always.
type: docs
weight: 40
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/querying/paths.html
upstream_source: agensgraph
upstream_modified: true
---


A fixed pattern asks a question whose shape you already know. `(a)-[]->(b)-[]->(c)` is two
hops, always. The questions a graph is for are the ones where you do not know the shape: how
are these two people connected, what is reachable from here, what is the cheapest route.

Three tools answer those, and they are different from each other. A variable-length edge
enumerates every path in a range of lengths. `shortestpath` finds one path of minimum length.
`dijkstra` finds one path of minimum *weight*, which is often not the same path.

Everything runs against [the example dataset](/agensgraph/get-started/example-dataset/), whose
`related_to` edges carry a `weight`. Two sections below also need a small four-stop graph, so
create it now. It has a direct A → B leg costing 10, a three-leg detour costing 1 each, and a
return leg that makes A → B → A a cycle:

```cypher
CREATE GRAPH routelab;
SET graph_path = routelab;
CREATE VLABEL stop;
CREATE ELABEL leg;
CREATE (:stop {name: 'A'}), (:stop {name: 'B'}), (:stop {name: 'C'}), (:stop {name: 'D'});
MATCH (a:stop {name:'A'}), (b:stop {name:'B'}) CREATE (a)-[:leg {cost: 10}]->(b);
MATCH (a:stop {name:'A'}), (c:stop {name:'C'}) CREATE (a)-[:leg {cost: 1}]->(c);
MATCH (c:stop {name:'C'}), (d:stop {name:'D'}) CREATE (c)-[:leg {cost: 1}]->(d);
MATCH (d:stop {name:'D'}), (b:stop {name:'B'}) CREATE (d)-[:leg {cost: 1}]->(b);
MATCH (b:stop {name:'B'}), (a:stop {name:'A'}) CREATE (b)-[:leg {cost: 1}]->(a);
```

Each block below sets `graph_path` to whichever of the two graphs it needs.

## A variable number of hops {#a-variable-number-of-hops}

`*` after an edge's label makes its length a range. The bounds go after the asterisk:

| Written | Means |
| --- | --- |
| `-[:related_to*2]->` | exactly two edges |
| `-[:related_to*1..3]->` | one, two or three edges |
| `-[:related_to*2..]->` | two or more |
| `-[:related_to*..3]->` | up to three, and at least one |
| `-[:related_to*]->` | one or more, no upper bound |
| `-[:related_to*0..1]->` | the vertex itself, or one edge away |

A fixed length behaves like the pattern written out longhand:

```cypher
SET graph_path = moviekb;
MATCH (a:movie {title: 'The Matrix'})-[:related_to*2]->(b:movie) RETURN b.title AS reached ORDER BY reached;
```

```
           reached            
------------------------------
 "Inception"
 "Terminator 2: Judgment Day"
 "The Matrix Revolutions"
```

A range unions the lengths in it, so the shorter reaches come back too:

```cypher
MATCH (a:movie {title: 'The Matrix'})-[:related_to*1..2]->(b:movie) RETURN b.title AS reached ORDER BY reached;
```

```
           reached            
------------------------------
 "Inception"
 "Terminator 2: Judgment Day"
 "The Matrix Reloaded"
 "The Matrix Revolutions"
 "The Terminator"
 "Total Recall"
```

A lower bound of zero includes the starting vertex, matched against nothing at all:

```cypher
MATCH (a:movie {title: 'The Matrix'})-[:related_to*0..1]->(b:movie) RETURN b.title AS reached ORDER BY reached;
```

```
        reached        
-----------------------
 "The Matrix"
 "The Matrix Reloaded"
 "The Terminator"
 "Total Recall"
```

Leaving the upper bound off means "as far as the edges go":

```cypher
MATCH (a:movie {title: 'The Matrix'})-[:related_to*]->(b:movie) RETURN count(*) AS reachable;
```

```
 reachable 
-----------
         7
```

### It cannot loop forever {#it-cannot-loop-forever}

An unbounded traversal on a cyclic graph terminates, because no path may use the same edge
twice. `routelab` has a cycle in it, A → B → A. So ask for paths of up to eight edges from A
back to A:

```cypher
SET graph_path = routelab;
MATCH p = (a:stop {name: 'A'})-[:leg*..8]->(a)
RETURN length(p) AS hops, [x IN nodes(p) | x.name] AS route ORDER BY hops;
```

```
 hops |           route           
------+---------------------------
 2    | ["A", "B", "A"]
 4    | ["A", "C", "D", "B", "A"]
```

Two paths, not an infinite number: each is a walk that reuses no edge. A *vertex* may repeat,
as `A` does at both ends here.

That guarantee is about correctness, not about cost. An unbounded search over a dense graph
can still enumerate an enormous number of paths before it runs out of edges. Give the range
an upper bound whenever you have any idea what it should be.

## Binding the path {#binding-the-path}

`p = ` in front of the pattern binds the whole path, and three functions take it apart:
`length(p)` is the edge count, `nodes(p)` the vertices in order, `relationships(p)` the edges.

```cypher
SET graph_path = moviekb;
MATCH p = (a:movie {title: 'The Matrix'})-[:related_to*2]->(b:movie)
RETURN length(p) AS hops,
       [x IN nodes(p) | x.title] AS route,
       [r IN relationships(p) | r.weight] AS weights
ORDER BY route;
```

```
 hops |                              route                              | weights 
------+-----------------------------------------------------------------+---------
 2    | ["The Matrix", "The Matrix Reloaded", "The Matrix Revolutions"] | [1, 1]
 2    | ["The Matrix", "The Terminator", "Terminator 2: Judgment Day"]  | [3, 1]
 2    | ["The Matrix", "Total Recall", "Inception"]                     | [4, 2]
```

The `[x IN list | expression]` form is a list comprehension, and it is how you render a route
readably. `edges(p)` is a synonym for `relationships(p)`.

A path crossing two labels needs one comprehension per property, because a `person` has no
`title` and a `movie` has no `name`:

```cypher
MATCH p = shortestpath((a:person {name: 'Keanu Reeves'})-[e:acted_in*..6]-(b:person {name: 'Carrie-Anne Moss'}))
RETURN length(p) AS hops, [x IN nodes(p) | x.name] AS people, [x IN nodes(p) | x.title] AS films;
```

```
 hops |                   people                   |           films            
------+--------------------------------------------+----------------------------
 2    | ["Keanu Reeves", null, "Carrie-Anne Moss"] | [null, "The Matrix", null]
```

Returning the path itself prints every element in full, which is useful when exploring and
too much for anything else. `label(x)` is the compact way to see a route's shape.

## The shortest path {#the-shortest-path}

`shortestpath` takes a pattern with one variable-length edge and returns one path of minimum
length, or no row if there is none. It is not "the paths, sorted by length, limit 1". It is a
bidirectional search that stops as soon as the two frontiers meet, so it does not enumerate
the paths it rejects.

```cypher
MATCH p = shortestpath((a:person {name: 'Keanu Reeves'})-[e*..6]-(b:person {name: 'Arnold Schwarzenegger'}))
RETURN length(p) AS hops,
       [x IN nodes(p) | label(x)] AS labels,
       [r IN relationships(p) | label(r)] AS via;
```

```
 hops |                 labels                 |                  via                   
------+----------------------------------------+----------------------------------------
 3    | ["person", "movie", "movie", "person"] | ["acted_in", "related_to", "acted_in"]
```

Three things about that query are deliberate. The edge is untyped and undirected, because the
route crosses two different edge labels, forwards along one and backwards along the other.

The upper bound of 6 is there because an unbounded shortest-path search over an unlabelled
edge is the most expensive query in this manual. And both endpoints are bound to variables.

That last one is a hard requirement:

```cypher
MATCH p = shortestpath((:person {name: 'Keanu Reeves'})-[e*..6]-(:person {name: 'Arnold Schwarzenegger'}))
RETURN length(p);
```

```
ERROR:  node must be a reference to a specific node
```

Name both ends even when you never use the names. This is the one place where leaving a
variable out is not merely wasteful but refused.

`allshortestpaths` is the same search returning every path of that minimum length rather
than one of them:

```cypher
MATCH p = allshortestpaths((a:movie {title: 'The Matrix'})-[:related_to*..4]->(b:movie {title: 'Inception'}))
RETURN length(p) AS hops, [x IN nodes(p) | x.title] AS route;
```

```
 hops |                    route                    
------+---------------------------------------------
 2    | ["The Matrix", "Total Recall", "Inception"]
```

One route here, because this dataset's `related_to` edges form a tree. On a graph with
several equally short routes you get one row each. You want that when the tie is the
interesting part.

Neither function accepts an alternation of edge labels. `[:acted_in|directed*..4]` raises
`ERROR: multiple types for relationship not supported`. Leave the edge untyped and filter
afterwards; see [Reading a graph](/agensgraph/querying/reading/#one-label-per-edge).

## The cheapest path {#the-cheapest-path}

`shortestpath` counts edges. The edges are not always interchangeable: they may carry
distance, latency, price or similarity. Counting them then answers the wrong question.
`dijkstra` takes a weight expression and minimises the total.

The difference is easiest to see on `routelab`, which has two useful routes from A to B:

```cypher
SET graph_path = routelab;
MATCH p = (a:stop {name: 'A'})-[:leg*..3]->(b:stop {name: 'B'})
RETURN length(p) AS hops, [x IN nodes(p) | x.name] AS route, [r IN relationships(p) | r.cost] AS costs
ORDER BY hops;
```

```
 hops |        route         |   costs   
------+----------------------+-----------
 1    | ["A", "B"]           | [10]
 3    | ["A", "C", "D", "B"] | [1, 1, 1]
```

`shortestpath` picks the one-hop route:

```cypher
MATCH p = shortestpath((a:stop {name: 'A'})-[:leg*..5]->(b:stop {name: 'B'}))
RETURN length(p) AS hops, [x IN nodes(p) | x.name] AS route;
```

```
 hops |   route    
------+------------
 1    | ["A", "B"]
```

`dijkstra` picks the three-hop one, because it costs 3 rather than 10:

```cypher
MATCH (a:stop {name: 'A'}), (b:stop {name: 'B'})
MATCH (p, total) = dijkstra((a)-[e:leg]->(b), e.cost)
RETURN total AS cost, length(p) AS hops, [x IN nodes(p) | x.name] AS route;
```

```
 cost | hops |        route         
------+------+----------------------
 3    | 3    | ["A", "C", "D", "B"]
```

Two things about the syntax are easy to get wrong.

**The pattern holds one edge, not a variable-length one.** `dijkstra` does its own expansion,
so you write a single hop and it walks as far as it needs to. A `*` in there is refused with
`ERROR: variable length relationship is not supported`, and more than one edge with
`ERROR: only one relationship is allowed`.

**The weight expression names the edge variable.** `e.cost` refers to the `e` bound inside
the pattern, and is evaluated per edge as the search expands.

`(p, total) = dijkstra(...)` binds two things: the path, and the total weight along it. The
one-variable form `p = dijkstra(...)` gives you the path alone.

On the manual's own dataset the weights are on `related_to`:

```cypher
SET graph_path = moviekb;
MATCH (a:movie {title: 'The Matrix'}), (b:movie {title: 'Inception'})
MATCH (p, total) = dijkstra((a)-[e:related_to]->(b), e.weight)
RETURN total AS weight, [x IN nodes(p) | x.title] AS route, [r IN relationships(p) | r.weight] AS legs;
```

```
 weight |                    route                    |  legs  
--------+---------------------------------------------+--------
 6      | ["The Matrix", "Total Recall", "Inception"] | [4, 2]
```

A third argument is a qualifier: a boolean the search applies to each candidate edge, so you
can exclude edges rather than pre-filter the graph. Here nothing survives, because the only
route out of *The Matrix* towards *Inception* runs over a weight-4 edge:

```cypher
MATCH (a:movie {title: 'The Matrix'}), (b:movie {title: 'Inception'})
MATCH (p, total) = dijkstra((a)-[e:related_to]->(b), e.weight, e.weight < 3)
RETURN total AS weight, [x IN nodes(p) | x.title] AS route;
```

```
 weight | route 
--------+-------
(0 rows)
```

The qualifier must be a boolean, as every condition must. `LIMIT n` inside the parentheses
caps how many paths are returned. Both are described in
[`dijkstra`](/agensgraph/reference/functions/path/).

## What a path costs {#what-a-path-costs}

The plan for a variable-length edge has a node of its own, and it names the label it walks
and the range it walks it over:

```cypher
EXPLAIN (COSTS OFF) MATCH (a:movie {title: 'The Matrix'})-[r:related_to*1..3]->(b:movie) RETURN b.title;
```

```
                          QUERY PLAN                          
--------------------------------------------------------------
 Nested Loop
   ->  Seq Scan on movie a
         Filter: (properties.'title' = '"The Matrix"'::jsonb)
   ->  Hash Join
         Hash Cond: (r."end" = b.id)
         ->  Subquery Scan on r
               ->  Graph VLE on related_to [1..3]
                     ->  Result
         ->  Hash
               ->  Seq Scan on movie b
```

`Graph VLE on related_to [1..3]` is the thing to read. Leave the label off and it becomes
`Graph VLE on ag_edge`, which walks every edge label in the graph at every hop:

```cypher
EXPLAIN (COSTS OFF) MATCH (a:movie {title: 'The Matrix'})-[r*1..2]->(b:movie) RETURN b.title;
```

```
                          QUERY PLAN                          
--------------------------------------------------------------
 Nested Loop
   ->  Seq Scan on movie a
         Filter: (properties.'title' = '"The Matrix"'::jsonb)
   ->  Hash Join
         Hash Cond: (r."end" = b.id)
         ->  Subquery Scan on r
               ->  Graph VLE on ag_edge [1..2]
                     ->  Result
         ->  Hash
               ->  Seq Scan on movie b
```

`shortestpath` shows as `Shortestpath VLE [min..max]` over a pair of `Hash2Side` nodes, the
two frontiers of the bidirectional search. `dijkstra` shows as a `Dijkstra` node. In all three
cases the work per hop is an index lookup on the edge label's `(start, "end")` or
`("end", start)` index. So the cost of a path query is the number of edges the frontier
touches. Four things reduce it, in order of effect:

1. **Anchor one end** on a selective, indexed property. A traversal from one known vertex is
   a different query from a traversal from all of them.
2. **Name the edge label.** It is the difference between one table per hop and all of them.
3. **Bound the length.** An upper bound is a promise the executor can use.
4. **`ANALYZE` the edge labels.** Traversal costing is degree estimation, and an unanalysed
   edge label has no degrees to estimate from. See [Tuning a
   query](/agensgraph/querying/performance/#statistics-on-edge-labels).

## Clean up {#clean-up}

```cypher
DROP GRAPH routelab CASCADE;
```

## Where to go next {#where-to-go-next}

* [Tuning a query](/agensgraph/querying/performance/) — reading a plan, and the settings that reshape one.
* [Reading a graph](/agensgraph/querying/reading/) — the fixed patterns these build on.
* [Vector search](/agensgraph/guides/search/vector/) — using a similarity match as the anchor of a
  traversal.
