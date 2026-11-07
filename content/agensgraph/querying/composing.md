---
title: Composing a query
linkTitle: Composing a query
description: A Cypher or GQL statement is a pipeline.
type: docs
weight: 30
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/querying/composing.html
upstream_source: agensgraph
upstream_modified: true
---


A Cypher or GQL statement is a pipeline. Each clause takes a stream of rows, does one thing
to it, and hands the result to the next clause. `MATCH` produces rows, `WHERE` removes some,
`WITH` reshapes them, `RETURN` ends the statement.

That is a different mental model from SQL, where a `SELECT` is a single block with named
parts evaluated in a fixed order. Here the order is the order you wrote. A query can match,
aggregate, filter the aggregate, match again from the survivors, and aggregate again, with no
subquery, no CTE and no `HAVING`.

Everything runs against [the example dataset](/agensgraph/get-started/example-dataset/).

## WITH is the divider {#with-is-the-divider}

`WITH` ends one part of a pipeline and begins the next. It takes a projection list exactly
like `RETURN`, and only what it lists stays in scope:

```cypher
MATCH (d:person)-[:directed]->(m:movie)
WITH d, count(m) AS films
WHERE films > 2
RETURN d.name AS director, films ORDER BY films DESC, director;
```

```
     director      | films 
-------------------+-------
 "Lana Wachowski"  | 4
 "James Cameron"   | 3
 "Lilly Wachowski" | 3
```

`m` is gone after the `WITH`; `d` and `films` are what is left. The `WHERE` after it filters
the aggregate, the job SQL needs `HAVING` for.

Order inside a `WITH` is fixed and worth committing to memory: `WHERE` first, then
`ORDER BY`, then `SKIP` and `LIMIT`. So this filters to five films and then takes two of
them, rather than taking two films and then filtering:

```cypher
MATCH (m:movie) WITH m.year AS y WHERE y > 2010 ORDER BY y LIMIT 2 RETURN y;
```

```
  y   
------
 2012
 2013
```

A name may be passed on only once:

```cypher
MATCH (m:movie) WITH m.year AS y, m.genre AS y RETURN y;
```

```
ERROR:  WITH passes on "y" more than once
```

### How it differs from a CTE {#how-it-differs-from-a-cte}

Both `WITH` keywords divide a query, and they are not the same keyword.

A SQL CTE is *named and referenced*: you declare `WITH films AS (...)` and then mention
`films` wherever you want it, as many times as you like, in any order.

A Cypher `WITH` is *positional*: it has no name, it is referenced by being next, and it is
consumed exactly once. There is no way to fork a Cypher pipeline into two branches and rejoin
them.

They do not mix. Cypher's `WITH` cannot introduce a named subquery: `WITH d AS (MATCH ...)`
is a syntax error. But a SQL CTE can hold a Cypher query, which is the way to get the CTE
behaviour when you want it:

```psql
WITH films AS (MATCH (m:movie) WHERE m.year > 2010 RETURN m.title AS title, m.year AS year)
SELECT f.title #>> '{}' AS title, r.score
FROM films f JOIN rating r ON r.title = f.title #>> '{}'
WHERE r.source = 'critics' ORDER BY r.score DESC;
```

```
          title           | score 
--------------------------+-------
 Interstellar             |   8.7
 Blade Runner 2049        |   8.0
 The Avengers             |   8.0
 Elysium                  |   6.6
 The Matrix Resurrections |   5.7
```

The outer statement there is SQL, because a statement that begins with a SQL CTE is a SQL
statement. [Combining SQL and Cypher](/agensgraph/querying/combining-sql-and-cypher/) is the page for that
boundary.

That is also why a Cypher pipeline cannot *begin* with `WITH`. A leading `WITH` is read as a
CTE, so the parser is looking for a name and a parenthesised query:

```cypher
WITH 1 AS x RETURN x;
```

```
ERROR:  syntax error at or near "1"
LINE 1: WITH 1 AS x RETURN x;
             ^
```

[`LET`](#the-gql-clauses) has no such collision, so it is the clause to open a statement with
a computed value:

```cypher
LET x = 1 RETURN x;
```

```
 x
---
 1
```

## Aggregation {#aggregation}

Aggregates are PostgreSQL's aggregates, and grouping is implicit: anything in the projection
list that is not inside an aggregate becomes a grouping key.

```cypher
MATCH (m:movie) RETURN m.genre AS genre, count(*) AS films, min(m.year) AS earliest ORDER BY genre;
```

```
    genre    | films | earliest 
-------------+-------+----------
 "Action"    | 7     | 1984
 "Adventure" | 1     | 1993
 "Sci-Fi"    | 10    | 1982
```

`count(*)` counts rows; `count(x)` counts rows where `x` is not null. That makes `count(x)`
useful after an `OPTIONAL MATCH`. `count(DISTINCT x)` counts distinct values, and the gap
between the two is usually the fan-out of your pattern:

```cypher
MATCH (:person)-[:acted_in]->(m:movie) RETURN count(m) AS rows, count(DISTINCT m) AS films;
```

```
 rows | films 
------+-------
 25   | 18
```

`collect()` is the aggregate you will reach for most, because it turns a fan-out back into
one row. Over a vertex, an edge or a path it builds a native array of those elements, so the
collected elements stay usable:

```cypher
MATCH (p:person)-[:acted_in]->(m:movie {title: 'The Matrix'})
WITH collect(p) AS players
RETURN pg_typeof(players) AS type, cardinality(players) AS n, players[1].name AS first;
```

```
    type    | n |        first         
------------+---+----------------------
 "vertex[]" | 3 | "Laurence Fishburne"
```

`collect()` over a *property* still returns a jsonb list, so stored data keeps its shape.

`DISTINCT` on the projection as a whole deduplicates rows, and is what you want after a
pattern that reaches the same thing by several routes:

```cypher
MATCH (:person {name: 'Keanu Reeves'})-[:acted_in]->(:movie)<-[:acted_in]-(co:person)
RETURN DISTINCT co.name AS co_actor ORDER BY co_actor;
```

```
       co_actor
----------------------
 "Carrie-Anne Moss"
 "Laurence Fishburne"
```

## UNWIND {#unwind}

`UNWIND` is the opposite of `collect()`: it takes a list and produces one row per element.

```cypher
UNWIND [1999, 2010, 2014] AS y MATCH (m:movie {year: y}) RETURN y, m.title AS title ORDER BY y, title;
```

```
  y   |     title      
------+----------------
 1999 | "The Matrix"
 2010 | "Inception"
 2014 | "Interstellar"
```

It also unpacks a list you built earlier in the same pipeline, which is how you filter on an
aggregate and then get back to one row per element:

```cypher
MATCH (m:movie)<-[:acted_in]-(p:person)
WITH m, collect(p) AS players
WHERE cardinality(players) > 2
UNWIND players AS actor
RETURN m.title AS film, actor.name AS actor ORDER BY actor;
```

```
     film     |        actor         
--------------+----------------------
 "The Matrix" | "Carrie-Anne Moss"
 "The Matrix" | "Keanu Reeves"
 "The Matrix" | "Laurence Fishburne"
```

[`FOR`](/agensgraph/reference/clauses/for/) is the GQL spelling, and it adds `WITH OFFSET` for the
element's 0-based index. See [`UNWIND`](/agensgraph/reference/clauses/unwind/).

## Ordering and paging {#ordering-and-paging}

`ORDER BY`, `SKIP`, `OFFSET` and `LIMIT` are clauses in their own right. They can sit at the
end of a `RETURN` or a `WITH`, as in SQL:

```cypher
MATCH (m:movie) RETURN m.title AS title, m.year AS year ORDER BY year SKIP 2 LIMIT 3;
```

```
            title             | year 
------------------------------+------
 "Total Recall"               | 1990
 "Terminator 2: Judgment Day" | 1991
 "Jurassic Park"              | 1993
```

or stand alone in the middle of a pipeline, which the `RETURN` form cannot do:

```cypher
MATCH (m:movie) LET y = m.year ORDER BY y LIMIT 3 RETURN m.title AS title, y;
```

```
      title       |  y   
------------------+------
 "Blade Runner"   | 1982
 "The Terminator" | 1984
 "Total Recall"   | 1990
```

They cannot *end* a statement: a query still has to finish with `RETURN`, `FINISH` or a
write clause.

A sort key is ordered as the value it is, not as its jsonb picture, so an index on the
property can serve the ordering. That is the whole reason to care:
[Indexes and constraints](/agensgraph/querying/indexes-and-constraints/#ordering).

## UNION {#union}

`UNION` stacks two result sets that have the same column names, and deduplicates.
`UNION ALL` keeps duplicates.

```cypher
MATCH (m:movie {title: 'The Matrix'}) RETURN m.title AS name
UNION
MATCH (p:person {name: 'Keanu Reeves'}) RETURN p.name AS name;
```

```
      name      
----------------
 "Keanu Reeves"
 "The Matrix"
```

This is also the tidy way round the missing edge-label alternation: two narrow patterns
unioned scan two edge tables, where one untyped pattern scans them all. See
[Reading a graph](/agensgraph/querying/reading/#one-label-per-edge).

## The GQL clauses {#the-gql-clauses}

Four ISO/IEC 39075 clauses do jobs that Cypher needs several clauses for. They are accepted
in the same statements as everything else, and there is no separate mode.

`LET` adds computed values without dropping anything in scope. Where `WITH` makes you list
every variable you still want, `LET` keeps them all:

```cypher
MATCH (m:movie) LET decade = (m.year / 10) * 10 FILTER decade = 2010
RETURN m.title AS title, m.year AS year, decade ORDER BY year;
```

```
        title        | year | decade 
---------------------+------+--------
 "Inception"         | 2010 | 2010
 "The Avengers"      | 2012 | 2010
 "Elysium"           | 2013 | 2010
 "Interstellar"      | 2014 | 2010
 "Blade Runner 2049" | 2017 | 2010
```

`FILTER` filters rows and nothing else, so a filter no longer has to be attached to a
`WITH`. It takes a bare predicate or the `FILTER WHERE` spelling.

`NEXT` chains one query onto the result of another, which is how you filter after a
projection without a `WITH`:

```cypher
MATCH (m:movie) RETURN m.genre AS genre, count(*) AS films
NEXT FILTER films > 3
RETURN genre, films ORDER BY genre;
```

```
  genre   | films 
----------+-------
 "Action" | 7
 "Sci-Fi" | 10
```

`FINISH` ends a query that projects nothing. It is the counterpart of `RETURN` for a statement
run for its effect:

```cypher
MATCH (m:movie {title: 'The Matrix'}) FINISH;
```

```
--
(0 rows)
```

Each has a reference page: [`LET`](/agensgraph/reference/clauses/let/),
[`FILTER`](/agensgraph/reference/clauses/filter/), [`NEXT`](/agensgraph/reference/clauses/next/),
[`FINISH`](/agensgraph/reference/clauses/finish/).

## Subqueries {#subqueries}

`CALL { }` runs a subquery once per incoming row and joins its result back. Use it when the
thing you want per row is a whole query rather than an expression: a per-row aggregate, a
per-row top-N.

Everything about it is ordinary except one thing, and it changes the answer rather than
raising an error.

> [!IMPORTANT]
> A `CALL { }` with no import list does **not** import the outer variables. A name used inside
> the body that also exists outside is rebound to a fresh, unconstrained variable, so the
> subquery runs over the whole graph instead of over the current row. Always write the import
> list.

Here is the difference. `m` is bound outside, the body mentions `m`, and the answer is the
same for every film:

```cypher
MATCH (d:person)-[:directed]->(m:movie)
CALL { MATCH (a:person)-[:acted_in]->(m) RETURN count(a) AS cast_size }
RETURN m.title AS film, cast_size ORDER BY film LIMIT 3;
```

```
        film         | cast_size 
---------------------+-----------
 "Avatar"            | 25
 "Blade Runner"      | 25
 "Blade Runner 2049" | 25
```

25 is every `acted_in` edge in the graph. The subquery's `m` was not the outer `m`.

Naming the import fixes it:

```cypher
MATCH (d:person)-[:directed]->(m:movie)
CALL (m) { MATCH (a:person)-[:acted_in]->(m) RETURN count(a) AS cast_size }
RETURN m.title AS film, cast_size ORDER BY film LIMIT 3;
```

```
        film         | cast_size 
---------------------+-----------
 "Avatar"            | 1
 "Blade Runner"      | 1
 "Blade Runner 2049" | 2
```

`CALL (*) { ... }` imports everything in scope, and `CALL { WITH m ... }` is the older
spelling of the same thing. All three agree.

A subquery may not hand back a name that is already bound outside it:

```cypher
MATCH (m:movie) CALL (m) { MATCH (p:person)-[:acted_in]->(m) RETURN m AS m } RETURN count(*);
```

```
ERROR:  variable "m" returned by the CALL subquery is already bound in the outer query
```

Write clauses are not allowed in a subquery body. `OPTIONAL CALL` is the left-join form,
producing a row even when the body yields nothing. See
[`CALL { }`](/agensgraph/reference/clauses/call-subquery/) and
[`OPTIONAL CALL`](/agensgraph/reference/clauses/optional-call/).

### Subqueries as values {#subqueries-as-values}

Six value expressions take a subquery and reduce it to something you can put in a `WHERE` or
a `RETURN`. They need no import list, because the outer variables are in scope as
expressions rather than as a separate query.

`EXISTS { }` is true when the subquery returns any row:

```cypher
MATCH (p:person) WHERE EXISTS { MATCH (p)-[:directed]->(:movie) } RETURN count(p) AS directors;
```

```
 directors 
-----------
 12
```

`COUNT { }` is how many rows it returns:

```cypher
MATCH (m:movie) WHERE COUNT { MATCH (:person)-[:acted_in]->(m) } > 2
RETURN m.title AS title ORDER BY title;
```

```
    title     
--------------
 "The Matrix"
```

`COLLECT { }` and `ARRAY { }` gather its single column into a list:

```cypher
MATCH (m:movie {title: 'The Matrix'})
RETURN COLLECT { MATCH (p:person)-[:acted_in]->(m) RETURN p.name ORDER BY p.name } AS players;
```

```
                          players                           
------------------------------------------------------------
 ["Carrie-Anne Moss", "Keanu Reeves", "Laurence Fishburne"]
```

`VALUE { }` takes its single value:

```cypher
MATCH (m:movie {title: 'The Matrix'})
RETURN VALUE { MATCH (p:person)-[:directed]->(m) RETURN p.name ORDER BY p.name LIMIT 1 } AS a_director;
```

```
    a_director    
------------------
 "Lana Wachowski"
```

and `x IN { }` tests membership of its result:

```cypher
MATCH (p:person)
WHERE p.name IN { MATCH (d:person)-[:directed]->(:movie {title: 'Inception'}) RETURN d.name }
RETURN p.name AS name;
```

```
        name         
---------------------
 "Christopher Nolan"
```

`EXISTS { }` is the one you will use most, because a bare pattern is not a predicate. See
[Reading a graph](/agensgraph/querying/reading/#asking-whether-a-pattern-exists). All six are defined in
[Subquery expressions](/agensgraph/reference/clauses/subquery-expressions/).

## Where to go next {#where-to-go-next}

* [Paths](/agensgraph/querying/paths/) — the patterns whose length you do not know in advance.
* [Combining SQL and Cypher](/agensgraph/querying/combining-sql-and-cypher/) — CTEs, joins to ordinary tables,
  views.
* [Tuning a query](/agensgraph/querying/performance/) — what a pipeline looks like as a plan.
