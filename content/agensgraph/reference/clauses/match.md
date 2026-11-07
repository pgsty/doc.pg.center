---
title: MATCH
linkTitle: MATCH
description: Finds every place in the graph where a pattern fits, and binds one row of variables per match.
type: docs
weight: 10
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/match.html
upstream_source: agensgraph
upstream_modified: true
---


**GQL clause**

Finds every place in the graph where a pattern fits, and binds one row of
variables per match.

## Synopsis {#synopsis}

```text
[ OPTIONAL ] MATCH pattern [, pattern ] ... [ WHERE condition ]
```

where *pattern* is a chain of node and edge patterns, optionally named:

```text
[ path_variable = ] node [ edge node ] ...
```

*node* is written in parentheses:

```text
( [ variable ] [ : label [ ONLY ] ] [ { property_map } ] )
```

*edge* is written in square brackets between two dashes, with *edge_body*:

```text
[ variable ] [ : label [ ONLY ] ] [ * [ min ] [ .. [ max ] ] ] [ { property_map } ]
```

The dashes and arrowheads around it give the direction. There are three:

```text
-[ edge_body ]->      left to right<-[ edge_body ]-      right to left-[ edge_body ]-       either direction
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`MATCH` reads the graph. It emits one row for every way its pattern can be laid
over the stored vertices and edges. Each named element of the pattern is bound
to the vertex, edge or path it matched. Later clauses in the pipeline see those
bindings. A `MATCH` in the middle of a pipeline runs once per incoming row and
joins its matches to that row, the way a join adds rows to a relational query.

- A pattern element with **no variable** is still matched. It just cannot be
  referred to later. Leave the variable out when you only need the element to
  constrain the shape.
- A **label** restricts an element to that label and its child labels; `ONLY`
  restricts it to the label itself. Without a label, an element matches every
  vertex or every edge in the graph.
- A **property map** in the pattern is an equality test on each key it lists. It
  is shorthand: `(m:movie {year: 1999})` and
  `(m:movie) WHERE m.year = 1999` match the same vertices.
- **Commas** separate independent patterns inside one `MATCH`. Patterns that
  share a variable are joined on it; patterns that share nothing produce their
  Cartesian product.
- Within one pattern match **no edge is used twice**. Node bindings may repeat,
  so a pattern can close a triangle, but a two-hop pattern never doubles back
  along the edge it arrived on.
- An **edge variable** may be used once per pattern; reusing it raises
  `duplicate variable`. A **node variable** may be repeated, which constrains
  both positions to the same vertex.
- `MATCH` may lead a query or sit anywhere after the first clause. It never ends
  one: a query has to finish with `RETURN`, `FINISH` or a write clause.

`OPTIONAL MATCH` keeps input rows for which the pattern finds nothing, binding
the pattern's variables to null instead of dropping the row. It has its own page,
[`OPTIONAL MATCH`](/agensgraph/reference/clauses/optional-match/).

## Parameters {#parameters}

pattern
: One path pattern, optionally preceded by `path_variable =`. Several patterns
  may be listed, separated by commas.

path_variable
: Name bound to the whole matched path, as a value carrying its vertices and
  edges in order. Read it with the path functions `length()`, `nodes()` and
  `edges()`. The name must be an identifier: an unreserved keyword such as `path`
  is rejected here unless you quote it (`` "path" ``).

variable
: Name bound to the matched vertex or edge. Optional. Visible to every clause
  after this one.

label
: A vertex label on a node pattern, an edge label on an edge pattern. One label
  per element.

ONLY
: Excludes child labels, so the element matches rows of that label's own table
  and nothing that inherits from it. Requires a label.

property_map
: A map literal, or a query parameter holding one. Each key is compared for
  equality against the element's property of that name.

min, max
: Bounds on the number of edges a variable-length edge pattern traverses. `*n`
  is exactly *n* hops; `*m..n` is between *m* and *n*; `*m..` is *m* or more;
  `*..n` is up to *n*; a bare `*` is one or more.

condition
: A boolean expression filtering the matches, evaluated with every variable in
  the pattern bound. See [`WHERE`](/agensgraph/reference/clauses/where/).

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).

### Find one vertex by a property {#find-one-vertex-by-a-property}

```cypher
MATCH (p:person {name: 'Keanu Reeves'})
RETURN p;
```

```
                         p
---------------------------------------------------
 person[4.1]{"born": 1964, "name": "Keanu Reeves"}
(1 row)
```

A vertex prints as `label[id]{properties}`. `4.1` is its graph id, which you read
with `id(p)`. `p.id` would read a property named `id`, and there is none.

### Follow an edge in one direction {#follow-an-edge-in-one-direction}

```cypher
MATCH (p:person)-[r:acted_in]->(m:movie {title: 'The Matrix'})
RETURN p.name AS actor, r.role AS role
ORDER BY actor;
```

```
        actor         |    role
----------------------+------------
 "Carrie-Anne Moss"   | "Trinity"
 "Keanu Reeves"       | "Neo"
 "Laurence Fishburne" | "Morpheus"
(3 rows)
```

Both endpoints and the edge carry a label, and the edge is bound to `r` so its
`role` property can be projected. String values come back quoted because a Cypher
`RETURN` produces jsonb.

### Leave out the elements you do not need {#leave-out-the-elements-you-do-not-need}

```cypher
MATCH (p:person {name: 'Christopher Nolan'})-[:directed]->(m)
RETURN m.title AS film
ORDER BY film;
```

```
      film
----------------
 "Inception"
 "Interstellar"
(2 rows)
```

The edge has no variable and the far endpoint has no label. Both still constrain
the match; neither costs a binding.

### Match an edge in either direction {#match-an-edge-in-either-direction}

An edge pattern with no arrowhead matches the edge whichever way it points:

```cypher
MATCH (m:movie {title: 'Total Recall'})-[:related_to]-(n:movie)
RETURN n.title AS neighbour
ORDER BY neighbour;
```

```
  neighbour
--------------
 "Inception"
 "The Matrix"
(2 rows)
```

`Total Recall` has one outgoing `related_to` edge and one incoming one. Writing
arrowheads at both ends, `<-[:related_to]->`, means the same thing.

### Join two patterns on a shared variable {#join-two-patterns-on-a-shared-variable}

```cypher
MATCH (a:person)-[:acted_in]->(m:movie), (d:person)-[:directed]->(m)
WHERE m.title = 'The Matrix'
RETURN a.name AS actor, d.name AS director
ORDER BY actor, director;
```

```
        actor         |     director
----------------------+-------------------
 "Carrie-Anne Moss"   | "Lana Wachowski"
 "Carrie-Anne Moss"   | "Lilly Wachowski"
 "Keanu Reeves"       | "Lana Wachowski"
 "Keanu Reeves"       | "Lilly Wachowski"
 "Laurence Fishburne" | "Lana Wachowski"
 "Laurence Fishburne" | "Lilly Wachowski"
(6 rows)
```

Both patterns mention `m`, so they are joined on it. Two consecutive `MATCH`
clauses would give the same result; so would one pattern that meets in the
middle, `(a:person)-[:acted_in]->(m:movie)<-[:directed]-(d:person)`.

### Name the whole path {#name-the-whole-path}

Put `variable =` in front of a pattern to bind the path itself:

```cypher
MATCH p = (a:movie {title: 'The Matrix'})-[:related_to*1..3]->(b:movie)
RETURN length(p) AS hops, [x IN nodes(p) | x.title] AS route
ORDER BY hops, route;
```

```
 hops |                                            route
------+---------------------------------------------------------------------------------------------
 1    | ["The Matrix", "The Matrix Reloaded"]
 1    | ["The Matrix", "The Terminator"]
 1    | ["The Matrix", "Total Recall"]
 2    | ["The Matrix", "The Matrix Reloaded", "The Matrix Revolutions"]
 2    | ["The Matrix", "The Terminator", "Terminator 2: Judgment Day"]
 2    | ["The Matrix", "Total Recall", "Inception"]
 3    | ["The Matrix", "The Matrix Reloaded", "The Matrix Revolutions", "The Matrix Resurrections"]
(7 rows)
```

### Walk a variable number of edges {#walk-a-variable-number-of-edges}

`*` on an edge pattern repeats it. Each bound is optional:

```cypher
MATCH (m:movie {title: 'The Matrix'})-[:related_to*2]->(n:movie)
RETURN n.title AS reached
ORDER BY reached;
```

```
           reached
------------------------------
 "Inception"
 "Terminator 2: Judgment Day"
 "The Matrix Revolutions"
(3 rows)
```

A lower bound of `0` includes the zero-length path, so the starting vertex is one
of the answers:

```cypher
MATCH (m:movie {title: 'The Matrix'})-[:related_to*0..1]->(n:movie)
RETURN n.title AS reached
ORDER BY reached;
```

```
        reached
-----------------------
 "The Matrix"
 "The Matrix Reloaded"
 "The Terminator"
 "Total Recall"
(4 rows)
```

### Exclude child labels with ONLY {#exclude-child-labels-with-only}

A label matches its child labels too, because a label is a table and a child
label inherits from it. `ONLY` narrows the match to the one label. Give `person` a
child label to see the difference:

```cypher
CREATE VLABEL crew INHERITS (person);
CREATE (:crew {name: 'Bill Pope', born: 1952});
```

```
CREATE VLABEL
UPDATE 1
```

```cypher
MATCH (p:person) RETURN count(*) AS people;
```

```
 people
--------
 29
(1 row)
```

```cypher
MATCH (p:person ONLY) RETURN count(*) AS people;
```

```
 people
--------
 28
(1 row)
```

`ONLY` goes after the label and before the property map, as in
`(p:person ONLY {name: 'Keanu Reeves'})`. It works the same on an edge pattern,
`-[r:acted_in ONLY]->`. Undo the setup with:

```cypher
MATCH (p:crew) DETACH DELETE p;
DROP VLABEL crew;
```

```
UPDATE 1
DROP VLABEL
```

### Filter the matches with WHERE {#filter-the-matches-with-where}

`WHERE` attached to a `MATCH` is part of the match, not a later step:

```cypher
MATCH (m:movie) WHERE m.year > 2015
RETURN m.title AS film, m.year AS year
ORDER BY year, film;
```

```
            film            | year
----------------------------+------
 "Blade Runner 2049"        | 2017
 "The Matrix Resurrections" | 2021
(2 rows)
```

### Match edges of several labels {#match-edges-of-several-labels}

An edge pattern carries at most one label. Listing two raises an error:

```cypher
MATCH (p:person)-[r:acted_in|directed]->(m:movie) RETURN count(r);
```

```
ERROR:  multiple types for relationship not supported
```

Match an unlabelled edge instead and test its label in `WHERE`:

```cypher
MATCH (p:person)-[r]->(m:movie)
WHERE label(r) IN ['acted_in', 'directed']
RETURN count(r) AS edges;
```

```
 edges
-------
 46
(1 row)
```

`label()` returns the element's label as a string. `IN` over a list of names is
therefore the general form, and the only way to match a set of edge labels.

## Notes {#notes}

A label test belongs in `label(n) = '...'`, not in a colon in `WHERE`. Writing
`WHERE n:movie` is a syntax error, and so is a bare pattern used as a predicate:
`WHERE (m)-[:related_to]->(:movie)` does not parse. Use
`WHERE EXISTS { MATCH (m)-[:related_to]->(:movie) }` to test for a pattern's
existence.

A property map compares jsonb values, and so does a comparison against a
property. That matters when the literal's type does not match the stored one.
See [`WHERE`](/agensgraph/reference/clauses/where/).

> [!NOTE]
> The named-path variable is parsed more narrowly than an element variable. `(path)`
> is an acceptable node variable, but `MATCH path = ...` is a syntax error because
> `path` is a keyword; write `MATCH p = ...` or quote the name.

## Compatibility {#compatibility}

### Label expressions (ISO/IEC 39075 §16.8) {#label-expressions-isoiec-39075-168}

The standard's `<label expression>` combines label names with `|` for
disjunction, `&` for conjunction and `!` for negation. AgensGraph accepts a
single label name per pattern element, so none of the three is available.
`-[r:acted_in|directed]->` raises `multiple types for relationship not supported`,
and `-[r:acted_in|:directed]->` is a syntax error. openCypher spells the
disjunction with a pipe too, and it is refused here on a fixed-length edge, on a
variable-length one and inside `shortestpath` alike. Use
`WHERE label(r) IN [...]` as shown above.

### Labeled predicate (ISO/IEC 39075 §19.9) {#labeled-predicate-isoiec-39075-199}

The standard writes a label test as `n IS LABELED movie` or `n:movie`. AgensGraph
accepts neither spelling; use `label(n) = 'movie'`.

### The ONLY modifier (ISO/IEC 39075 §16.7) {#the-only-modifier-isoiec-39075-167}

The standard's `<element pattern filler>` holds a variable declaration, a label
expression and a predicate, and nothing else. There is no `ONLY`. AgensGraph
adds it because a label here is a table that child labels inherit from, so a
label match is a match over an inheritance tree. See
[label inheritance](/agensgraph/concepts/label-inheritance/).

## See also {#see-also}

- [`OPTIONAL MATCH`](/agensgraph/reference/clauses/optional-match/) — keep the rows a pattern does not match
- [`WHERE`](/agensgraph/reference/clauses/where/) — the conditions a match can carry
- [`CREATE`](/agensgraph/reference/clauses/create/) and [`MERGE`](/agensgraph/reference/clauses/merge/) — the same pattern syntax, used to write
- [`LOAD FROM`](/agensgraph/reference/clauses/load-from/) — read a table into the same pipeline
- [Functions](/agensgraph/reference/functions/) — `length()`, `nodes()`, `edges()` and the other path functions
- [Querying](/agensgraph/querying/) — path queries, including the `shortestpath`, `allshortestpaths` and `dijkstra` forms
