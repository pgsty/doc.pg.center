---
title: Your first query
linkTitle: Your first query
description: This page walks the example dataset — 18 films, 28 people, and the edges between them.
type: docs
weight: 40
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/get_started/first-query.html
upstream_source: agensgraph
upstream_modified: true
---


This page walks the [example dataset](/agensgraph/get-started/example-dataset/) — 18 films, 28 people, and the
edges between them. Load it first, then work down the page: each query builds on the one
before it.

Everything here is Cypher. The equivalent GQL spellings are noted in the
[reference](/agensgraph/reference/clauses/); [Combining SQL and
Cypher](/agensgraph/querying/combining-sql-and-cypher/) is where SQL comes back in.

## Say which graph you mean {#say-which-graph-you-mean}

```cypher
SET graph_path = moviekb;
```

That is the one piece of session state Cypher needs. Without it every label name is
unresolvable. Now count everything in the graph:

```cypher
MATCH (n) RETURN count(n) AS elements;
```

```
 elements
----------
       46
```

`MATCH (n)` is the emptiest possible pattern — one vertex, no label, no properties — so it
matches every vertex. 46 is 18 films plus 28 people.

## Find one thing {#find-one-thing}

A pattern narrows in two ways: by label, and by property.

```cypher
MATCH (m:movie {title: 'The Matrix'}) RETURN m.year AS year, m.genre AS genre;
```

```
 year |  genre
------+----------
 1999 | "Action"
```

`(m:movie {title: 'The Matrix'})` reads as: a vertex, labelled `movie`, whose `title`
property is `'The Matrix'`, bound to the variable `m`. `RETURN` then projects out of `m`.

Note the quotes around `"Action"` and their absence around `1999`. A `RETURN` hands a
property back as `jsonb`, so a string arrives JSON-quoted. That is worth knowing before
you compare a result against a client-side string — see [Combining SQL and
Cypher](/agensgraph/querying/combining-sql-and-cypher/#getting-a-plain-value-out) for how to get a
plain value.

Every vertex also has an identity, which is not a property:

```cypher
MATCH (m:movie {title: 'The Matrix'}) RETURN m.title AS title, id(m) AS id;
```

```
    title     | id
--------------+-----
 "The Matrix" | 3.1
```

`3.1` is a `graphid`: label 3, row 1. It is the vertex's identity, and `id(m)` is how you ask
for it — `m.id` would look for a *property* called `id`, which no film has.

## Follow an edge {#follow-an-edge}

The point of a graph is what comes next. Add an edge to the pattern:

```cypher
MATCH (p:person)-[r:acted_in]->(:movie {title: 'The Matrix'})
RETURN p.name AS actor, r.role AS role
ORDER BY actor;
```

```
        actor         |    role
----------------------+------------
 "Carrie-Anne Moss"   | "Trinity"
 "Keanu Reeves"       | "Neo"
 "Laurence Fishburne" | "Morpheus"
```

Three things are new. `-[r:acted_in]->` is an edge, labelled `acted_in`, pointing from the
person to the film. It is bound to `r`, so its properties are available: `r.role` is a
property of the *relationship*, not of either endpoint. And `(:movie {title: 'The Matrix'})`
has no variable, because the pattern needs to reach that film but the projection never
mentions it.

## Follow two {#follow-two}

Extend the pattern in the other direction and you have asked a question SQL would need a
self-join for:

```cypher
MATCH (:person {name: 'Keanu Reeves'})-[:acted_in]->(:movie)<-[:acted_in]-(co:person)
RETURN DISTINCT co.name AS co_actor
ORDER BY co_actor;
```

```
       co_actor
----------------------
 "Carrie-Anne Moss"
 "Laurence Fishburne"
```

Read the pattern left to right: from Keanu Reeves, out along an `acted_in` edge to a film,
then *backwards* along another `acted_in` edge to a second person. `DISTINCT` is needed
because two people who share three films produce three rows.

## Aggregate {#aggregate}

Aggregates are PostgreSQL's, and they work the way you expect:

```cypher
MATCH (d:person)-[:directed]->(m:movie)
RETURN d.name AS director, count(m) AS films
ORDER BY films DESC, director
LIMIT 5;
```

```
      director       | films
---------------------+-------
 "Lana Wachowski"    | 4
 "James Cameron"     | 3
 "Lilly Wachowski"   | 3
 "Christopher Nolan" | 2
 "Steven Spielberg"  | 2
```

Anything in `RETURN` that is not inside an aggregate becomes a grouping key, again as in SQL.

## Ask for something that might not be there {#ask-for-something-that-might-not-be-there}

`MATCH` drops a row when the pattern fails. `OPTIONAL MATCH` keeps it and fills the missing
variables with null — a left join:

```cypher
MATCH (d:person)-[:directed]->(:movie)
WITH DISTINCT d
OPTIONAL MATCH (d)-[:acted_in]->(m:movie)
RETURN d.name AS director, m.title AS also_acted_in
ORDER BY director
LIMIT 6;
```

```
      director       | also_acted_in
---------------------+---------------
 "Andrew Niccol"     |
 "Christopher Nolan" |
 "Denis Villeneuve"  |
 "James Cameron"     |
 "Joss Whedon"       |
 "Lana Wachowski"    |
```

Nobody in this dataset both directed and acted, so every `also_acted_in` is null — which is
the point: with a plain `MATCH`, all six rows would have vanished.

`WITH` in the middle there is a pipeline divider. It ends one part of the query and starts
the next, which is what lets `DISTINCT` apply to the directors before the optional match runs.

## Walk an unknown number of hops {#walk-an-unknown-number-of-hops}

Ask how two people connect without knowing the route:

```cypher
MATCH p = shortestpath((a:person {name: 'Keanu Reeves'})-[*..6]-(b:person {name: 'Arnold Schwarzenegger'}))
RETURN length(p) AS hops;
```

```
 hops
------
 3
```

`[*..6]` is a variable-length edge: up to six of them, of any label, in either direction.
`p = ...` binds the whole path, and `length(p)` is its edge count. This is the query that has
no reasonable SQL form.

Both endpoints of a `shortestpath` need a variable, even if you never use it. Leaving them
anonymous gives `ERROR: node must be a reference to a specific node`.

[Paths](/agensgraph/querying/paths/) covers the rest — bounded ranges, `allshortestpaths`, and
weighted search with `dijkstra`.

## Write something {#write-something}

Writing looks like reading with a different verb. `CREATE` makes a vertex:

```cypher
CREATE (p:person {name: 'Hugo Weaving', born: 1960}) RETURN p;
```

```
                         p
----------------------------------------------------
 person[4.63]{"born": 1960, "name": "Hugo Weaving"}
```

To connect it to something, find both ends first and then create the edge:

```cypher
MATCH (p:person {name: 'Hugo Weaving'}), (m:movie {title: 'The Matrix'})
CREATE (p)-[r:acted_in {role: 'Agent Smith'}]->(m)
RETURN r;
```

```
                        r
-------------------------------------------------
 acted_in[5.60][4.63,3.1]{"role": "Agent Smith"}
```

An edge prints as `label[id][start,end]{properties}`, so you can see both endpoints in the
result.

`SET` adds or replaces a property:

```cypher
MATCH (p:person {name: 'Hugo Weaving'}) SET p.nationality = 'Australian' RETURN p;
```

```
                                        p
---------------------------------------------------------------------------------
 person[4.63]{"born": 1960, "name": "Hugo Weaving", "nationality": "Australian"}
```

`REMOVE` takes one away:

```cypher
MATCH (p:person {name: 'Hugo Weaving'}) REMOVE p.nationality RETURN p;
```

```
                         p
----------------------------------------------------
 person[4.63]{"born": 1960, "name": "Hugo Weaving"}
```

And `DETACH DELETE` removes a vertex together with its edges. A plain `DELETE` on a vertex
that still has edges is refused, because AgensGraph will not keep an edge with a missing
endpoint:

```cypher
MATCH (p:person {name: 'Hugo Weaving'}) DETACH DELETE p;
```

That puts the dataset back to 46 elements, so the rest of the manual's examples still match.

## Mix in SQL {#mix-in-sql}

The `rating` table you created with the dataset is an ordinary table, not part of the graph.
Join it to a Cypher query by putting the Cypher where SQL expects a table:

```psql
SELECT q.film #>> '{}' AS film, r.score
FROM (MATCH (:person {name: 'Christopher Nolan'})-[:directed]->(m:movie)
      RETURN m.title AS film) q
JOIN rating r ON r.title = q.film #>> '{}'
WHERE r.source = 'critics'
ORDER BY r.score DESC;
```

```
     film     | score
--------------+-------
 Inception    |   8.8
 Interstellar |   8.7
```

`#>> '{}'` is what turns the `jsonb` title into plain `text` so it can be compared to a
`text` column — and note the film names come back unquoted here, because this is a SQL
projection rather than a Cypher one.

## Where to go next {#where-to-go-next}

* [Querying](/agensgraph/querying/) takes each of these ideas properly: reading, writing,
  pipelines, paths, indexes.
* [Reference](/agensgraph/reference/clauses/) has a page per clause with the full syntax.
* [How a graph is stored](/agensgraph/concepts/graph-on-postgresql/) explains what the
  server actually did with everything you just created.
* [Vector search](/agensgraph/guides/search/vector/), [full-text
  search](/agensgraph/guides/search/full-text/) and [hybrid
  search](/agensgraph/guides/search/hybrid/) use the `plot` and `embedding` properties this page
  ignored.
