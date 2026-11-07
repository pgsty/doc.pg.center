---
title: Reading a graph
linkTitle: Reading a graph
description: Every read starts with a pattern.
type: docs
weight: 10
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/querying/reading.html
upstream_source: agensgraph
upstream_modified: true
---


Every read starts with a pattern. A pattern is a drawing of the shape you are looking for,
written in ASCII: parentheses for vertices, brackets and dashes for edges. `MATCH` hands that
drawing to the planner, which turns it into scans and joins, and returns one row for every
way the drawing fits the data.

This page is about the drawing and about what the planner does with it. The formal syntax is
in [`MATCH`](/agensgraph/reference/clauses/match/) and [`WHERE`](/agensgraph/reference/clauses/where/);
everything here runs against [the example dataset](/agensgraph/get-started/example-dataset/).

## One vertex {#one-vertex}

The smallest pattern is a pair of parentheses. Add a label to narrow it to one table:

```cypher
MATCH (m:movie) RETURN m.title AS title ORDER BY title LIMIT 3;
```

```
        title        
---------------------
 "Avatar"
 "Blade Runner"
 "Blade Runner 2049"
```

`m` is a variable bound to each matching vertex; `movie` is the label. Either may be left
out. `(m)` matches every vertex, `(:movie)` matches every film without naming it, and `()`
matches every vertex without naming it.

Naming a label includes the labels that inherit from it. `ONLY` excludes them:

```cypher
MATCH (m:movie ONLY) RETURN count(m) AS films;
```

```
 films 
-------
 18
```

Nothing inherits from `movie` here, so the count is the same either way. On a hierarchy the
difference is the whole `Append`. See [Label
inheritance](/agensgraph/concepts/label-inheritance/).

## Two ways to narrow {#two-ways-to-narrow}

A property map inside the pattern tests properties for equality:

```cypher
MATCH (m:movie {genre: 'Adventure'}) RETURN m.title AS title, m.year AS year;
```

```
      title      | year 
-----------------+------
 "Jurassic Park" | 1993
```

`WHERE` takes any predicate, so anything that is not equality goes there:

```cypher
MATCH (m:movie) WHERE m.year >= 2017 RETURN m.title AS title, m.year AS year ORDER BY year;
```

```
           title            | year 
----------------------------+------
 "Blade Runner 2049"        | 2017
 "The Matrix Resurrections" | 2021
```

The two combine, and for a plain `MATCH` they mean exactly the same thing. The planner
receives one conjunction either way:

```cypher
MATCH (m:movie {genre: 'Action'}) WHERE m.year < 2000
RETURN m.title AS title, m.year AS year ORDER BY year;
```

```
            title             | year 
------------------------------+------
 "The Terminator"             | 1984
 "Terminator 2: Judgment Day" | 1991
 "The Matrix"                 | 1999
```

Use the map for the keys that identify the thing you want and `WHERE` for the conditions on
it. The one place the choice matters is `OPTIONAL MATCH`, [below](#a-pattern-that-may-not-fit).

A condition has to be a boolean. `WHERE m.title` does not mean "has a title"; it raises
`ERROR: cannot cast "The Matrix" (jsonb type string) to boolean`. Write the test you mean:
`WHERE m.title IS NOT NULL`.

## An edge {#an-edge}

An edge is a pair of brackets between two dashes, with an arrowhead for direction:

```cypher
MATCH (p:person)-[]->(m:movie {title: 'Blade Runner 2049'})
RETURN p.name AS person ORDER BY person;
```

```
       person       
--------------------
 "Denis Villeneuve"
 "Harrison Ford"
 "Ryan Gosling"
```

Note the empty brackets. The brackets are not optional: `-->` and `--` are not patterns,
because `--` begins a SQL line comment. `MATCH (p:person)-->(m:movie) RETURN count(p)`
comments away everything from the first dash onwards and fails with `ERROR: Cypher query
must end with RETURN, FINISH or update clause`. Write `-[]->` and `-[]-`.

Bind the edge to a variable and its label and properties become available:

```cypher
MATCH (p:person)-[r]->(m:movie {title: 'Blade Runner 2049'})
RETURN p.name AS person, label(r) AS via, r.role AS role ORDER BY person;
```

```
       person       |    via     |      role      
--------------------+------------+----------------
 "Denis Villeneuve" | "directed" | 
 "Harrison Ford"    | "acted_in" | "Rick Deckard"
 "Ryan Gosling"     | "acted_in" | "K"
```

`label(r)` is the edge's label and `r.role` is a property of the edge itself. `directed`
edges carry no `role`, so that cell is null.

### Direction {#direction}

`-[]->` follows the edge as stored, `<-[]-` follows it backwards, and `-[]-` ignores
direction. Direction is a property of the query, not of the data: you store an edge one way
round and decide per pattern whether it matters.

```cypher
MATCH (a:movie {title: 'The Matrix Reloaded'})-[:related_to]->(b:movie)
RETURN b.title AS neighbour ORDER BY neighbour;
```

```
        neighbour         
--------------------------
 "The Matrix Revolutions"
```

```cypher
MATCH (a:movie {title: 'The Matrix Reloaded'})-[:related_to]-(b:movie)
RETURN b.title AS neighbour ORDER BY neighbour;
```

```
        neighbour         
--------------------------
 "The Matrix"
 "The Matrix Revolutions"
```

### One label per edge {#one-label-per-edge}

An edge pattern names at most one label. There is no alternation:

```cypher
MATCH (p:person)-[r:acted_in|directed]->(m:movie) RETURN count(r);
```

```
ERROR:  multiple types for relationship not supported
```

This holds at every length and inside `shortestpath`. Leave the edge untyped and test the
label with a predicate:

```cypher
MATCH (p:person)-[r]->(m:movie {title: 'Blade Runner'})
WHERE label(r) IN ['acted_in', 'directed']
RETURN p.name AS person, label(r) AS via ORDER BY person;
```

```
     person      |    via     
-----------------+------------
 "Harrison Ford" | "acted_in"
 "Ridley Scott"  | "directed"
```

That form costs something: an untyped edge scans every edge label in the graph, and the
label test is applied afterwards. Two patterns joined with
[`UNION`](/agensgraph/reference/clauses/union/) keep each scan narrow when the alternation is over
few labels and the graph is large.

## A whole path {#a-whole-path}

`p = ` before a pattern binds the path itself, not just its ends:

```cypher
MATCH p = (a:person {name: 'Ryan Gosling'})-[:acted_in]->(m:movie)
RETURN length(p) AS hops,
       [x IN nodes(p) | label(x)] AS labels,
       [r IN relationships(p) | label(r)] AS edges;
```

```
 hops |       labels        |    edges     
------+---------------------+--------------
 1    | ["person", "movie"] | ["acted_in"]
```

`length(p)` is the edge count, `nodes(p)` the vertices in order and `relationships(p)` the
edges. A path is a value: you can return it, order by its length, or collect it.
[Paths](/agensgraph/querying/paths/) does the rest, including patterns whose length you do not know.

## More than one pattern {#more-than-one-pattern}

`MATCH` takes a comma-separated list of patterns. A variable that appears in two of them
joins them:

```cypher
MATCH (d:person)-[:directed]->(m:movie), (a:person)-[:acted_in]->(m)
RETURN d.name AS director, a.name AS actor, m.title AS film
ORDER BY film, actor LIMIT 5;
```

```
      director      |       actor       |        film         
--------------------+-------------------+---------------------
 "James Cameron"    | "Sam Worthington" | "Avatar"
 "Ridley Scott"     | "Harrison Ford"   | "Blade Runner"
 "Denis Villeneuve" | "Harrison Ford"   | "Blade Runner 2049"
 "Denis Villeneuve" | "Ryan Gosling"    | "Blade Runner 2049"
 "Neill Blomkamp"   | "Matt Damon"      | "Elysium"
```

`m` is bound by the first pattern and reused by the second. That makes this an inner join on
the film rather than a product. Two patterns with no variable in common *are* a product, and
that is legal and occasionally what you want:

```cypher
MATCH (p:person {name: 'Keanu Reeves'}), (m:movie {genre: 'Adventure'})
RETURN p.name AS person, m.title AS film;
```

```
     person     |      film       
----------------+-----------------
 "Keanu Reeves" | "Jurassic Park"
```

Writing the two patterns as two consecutive `MATCH` clauses means the same thing. The comma
form and the two-clause form both produce 31 rows for the director-and-actor query above, and
the same plan shape. Use whichever reads better: a comma for "these things together", a
second `MATCH` for "and then".

## A pattern that may not fit {#a-pattern-that-may-not-fit}

`MATCH` drops a row whose pattern finds nothing:

```cypher
MATCH (p:person {name: 'Ridley Scott'})-[:acted_in]->(m:movie)
RETURN p.name AS person, m.title AS film;
```

```
 person | film 
--------+------
(0 rows)
```

`OPTIONAL MATCH` keeps the row and leaves the pattern's variables null. It is a left join,
and it behaves like one in every respect:

```cypher
MATCH (p:person {name: 'Ridley Scott'})
OPTIONAL MATCH (p)-[:acted_in]->(m:movie)
RETURN p.name AS person, m.title AS film;
```

```
     person     | film 
----------------+------
 "Ridley Scott" | 
```

This is where the property map and `WHERE` stop agreeing. A `WHERE` written *on* an
`OPTIONAL MATCH` belongs to the join condition, so a row that fails it survives with nulls:

```cypher
MATCH (m:movie {title: 'The Matrix'})
OPTIONAL MATCH (m)<-[r:acted_in]-(p:person) WHERE r.role = 'Agent Smith'
RETURN m.title AS film, p.name AS actor;
```

```
     film     | actor 
--------------+-------
 "The Matrix" | 
```

The same predicate one clause later is a filter on the joined result, and drops the row:

```cypher
MATCH (m:movie {title: 'The Matrix'})
OPTIONAL MATCH (m)<-[r:acted_in]-(p:person)
WITH m, p, r WHERE r.role = 'Agent Smith'
RETURN m.title AS film, p.name AS actor;
```

```
 film | actor 
------+-------
(0 rows)
```

If you know SQL, you have met this before: it is the difference between a condition in `ON`
and the same condition in `WHERE` after a `LEFT JOIN`. See
[`OPTIONAL MATCH`](/agensgraph/reference/clauses/optional-match/).

## Asking whether a pattern exists {#asking-whether-a-pattern-exists}

A pattern is not a predicate on its own. `WHERE (p)-[:acted_in]->(:movie)` is a syntax
error. Put it in an `EXISTS { }` subquery:

```cypher
MATCH (p:person)
WHERE EXISTS { MATCH (p)-[:acted_in]->(:movie {title: 'The Matrix'}) }
RETURN p.name AS actor ORDER BY actor;
```

```
        actor         
----------------------
 "Carrie-Anne Moss"
 "Keanu Reeves"
 "Laurence Fishburne"
```

`EXISTS`, `COUNT`, `COLLECT`, `ARRAY`, `VALUE` and `IN` all take a subquery like this.
[Composing a query](/agensgraph/querying/composing/#subqueries-as-values) covers them together.

## How a pattern becomes a plan {#how-a-pattern-becomes-a-plan}

A pattern is not executed as a walk. It is compiled into ordinary relational algebra over the
label tables, and `EXPLAIN` shows exactly that:

```cypher
EXPLAIN (COSTS OFF) MATCH (p:person)-[r:acted_in]->(m:movie) RETURN p.name, m.title;
```

```
                                                                               QUERY PLAN                                                                                
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Hash Join
   Hash Cond: (r.start = p.id)
   ->  Hash Join
         Hash Cond: (r."end" = m.id)
         ->  Seq Scan on acted_in r
               Filter: ((start >= '4.0'::graphid) AND (start <= '4.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
         ->  Hash
               ->  Seq Scan on movie m
   ->  Hash
         ->  Seq Scan on person p
```

Three things are worth reading out of that.

Each pattern element is a scan. `person`, `acted_in` and `movie` are three tables, and the
pattern is two joins between them: `r.start = p.id` and `r."end" = m.id`. Traversing an edge
*is* a join on `graphid`. The `(start, "end")` and `("end", start)` indexes that come with
every edge label therefore matter a great deal.

The label test on an endpoint is answered on the edge. `p` is a `person`, so `r.start` can
only be a `person`'s id. A label id lives in the high bits of a `graphid`, so all of one
label's ids form a contiguous range.

The planner turns "`start` is a person" into
`start >= '4.0' AND start <= '4.281474976710655'`, a range test it can push into the edge
scan or an index on it, with no visit to `person` at all. See
[Identity: the graphid](/agensgraph/concepts/graph-on-postgresql/#identity-the-graphid).

Anchoring the pattern changes the join order. Pin one end to a single vertex and the plan
stops hashing whole tables:

```cypher
EXPLAIN (COSTS OFF)
MATCH (p:person {name: 'Keanu Reeves'})-[r:acted_in]->(m:movie) RETURN m.title;
```

```
                                                                                              QUERY PLAN                                                                                              
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Nested Loop
   ->  Nested Loop
         ->  Seq Scan on person p
               Filter: (properties.'name' = '"Keanu Reeves"'::jsonb)
         ->  Bitmap Heap Scan on acted_in r
               Recheck Cond: ((p.id = start) AND (start >= '4.0'::graphid) AND (start <= '4.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
               ->  Bitmap Index Scan on acted_in_start_idx
                     Index Cond: ((start = p.id) AND (start >= '4.0'::graphid) AND (start <= '4.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
   ->  Index Scan using movie_pkey on movie m
         Index Cond: (id = r."end")
```

Now `acted_in` is reached through `acted_in_start_idx` for the one person, and `movie`
through its primary key for each edge found.

This is the shape you want for a traversal from a known starting point. It is also the reason
a selective anchor, a property with an index on it, is usually worth more than any other
tuning. [Indexes and constraints](/agensgraph/querying/indexes-and-constraints/) covers which predicates can
serve as one.

## What an endpoint you do not use costs {#what-an-endpoint-you-do-not-use-costs}

An endpoint whose value the query never reads does not have to be fetched at all. Here `m`
is bound and labelled, and nothing in the projection asks for it:

```cypher
EXPLAIN (COSTS OFF) MATCH (p:person)-[r:acted_in]->(m:movie) RETURN p.name;
```

```
                                                                            QUERY PLAN                                                                             
-------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Hash Join
   Hash Cond: (r.start = p.id)
   ->  Seq Scan on acted_in r
         Filter: (("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid) AND (start >= '4.0'::graphid) AND (start <= '4.281474976710655'::graphid))
   ->  Hash
         ->  Seq Scan on person p
```

There is no scan for `m`. Its only remaining contribution is the second half of that filter:
`"end"` must be in the `movie` range. So the whole of `(m:movie)` has collapsed into two
comparisons on a column the edge scan was reading anyway.

Switch the elision off and the vertex the query never asked about is fetched across the
whole `ag_vertex` family:

```cypher
SET enable_graph_endpoint_elision = off;
EXPLAIN (COSTS OFF) MATCH (p:person)-[r:acted_in]->(m) RETURN p.name;
```

```
                                          QUERY PLAN                                           
-----------------------------------------------------------------------------------------------
 Hash Join
   Hash Cond: (r."end" = m.id)
   ->  Hash Join
         Hash Cond: (r.start = p.id)
         ->  Seq Scan on acted_in r
               Filter: ((start >= '4.0'::graphid) AND (start <= '4.281474976710655'::graphid))
         ->  Hash
               ->  Seq Scan on person p
   ->  Hash
         ->  Append
               ->  Seq Scan on ag_vertex m_1
               ->  Seq Scan on movie m_2
               ->  Seq Scan on person m_3
```

The setting is on by default and there is no reason to turn it off outside an experiment like
this one.

The comparison shows the size of the saving, and where it stops. Add `m.title` to that
`RETURN` and the `Append` comes back, because the query really does need the film. Project the
endpoints you use and no more.

> [!NOTE]
> Name every element of a pattern whose plan you intend to keep. An element you leave unnamed
> is given a synthetic alias like `"<0000000002>"`, and the counter behind it advances on every
> statement — so the same query prints a different plan the second time you run it.

> [!NOTE]
> Anonymity is not free everywhere. Both endpoints of a `shortestpath` must be named
> variables, even ones you never use — an anonymous endpoint there gives
> `ERROR: node must be a reference to a specific node`.

## Where to go next {#where-to-go-next}

* [Composing a query](/agensgraph/querying/composing/) — `WITH`, aggregation, subqueries, and the rest of the
  pipeline that follows a `MATCH`.
* [Paths](/agensgraph/querying/paths/) — variable-length edges, shortest paths and weighted search.
* [Writing a graph](/agensgraph/querying/writing/) — the same patterns with a write clause after them.
* [Indexes and constraints](/agensgraph/querying/indexes-and-constraints/) — which predicates an index can
  serve.
