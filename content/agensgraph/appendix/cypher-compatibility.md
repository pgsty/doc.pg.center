---
title: Cypher compatibility
linkTitle: Cypher compatibility
description: AgensGraph's Cypher is close enough to other implementations that most queries move across unchanged.
type: docs
weight: 20
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/appendix/cypher-compatibility.html
upstream_source: agensgraph
upstream_modified: true
---


AgensGraph's Cypher is close enough to other implementations that most queries move across
unchanged. It is different enough that a handful fail, or, worse, succeed with a different
answer. This appendix lists those differences, with the error the server raises or the result
it returns, so you can recognize one when a ported query misbehaves.

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/) with
`graph_path` set to `moviekb`.

Two structural facts explain most of what follows. A vertex has exactly one label, because a
label is a table and a row lives in one table. And a Cypher query is a PostgreSQL query, so
the lexer, the type system and the error codes are PostgreSQL's.

## Constructs that do not exist {#constructs-that-do-not-exist}

### Several types on one relationship pattern {#several-types-on-one-relationship-pattern}

A relationship pattern takes at most one type:

```cypher
MATCH (p:person)-[r:acted_in|directed]->(m:movie) RETURN count(r);
```

```
ERROR:  multiple types for relationship not supported
```

The same error comes back with a variable length (`-[r:acted_in|directed*1..2]->`) and inside
`shortestpath()`. The `-[r:acted_in|:directed]->` spelling is a plain syntax error. Match an
untyped edge and test the label instead:

```cypher
MATCH (p:person)-[r]->(m:movie)
WHERE label(r) IN ['acted_in','directed']
RETURN count(r);
```

```
 count 
-------
 46
```

Node label alternation fails the same way. `MATCH (n:person|movie)` is a syntax error at the
`|`, and so are the other label-expression operators the GQL standard defines: `:person&movie`,
`:!person` and `:%`.

### A label set on a vertex {#a-label-set-on-a-vertex}

There is no set of labels and no way to change the one a vertex has. Each of these is a
syntax error at the second colon:

```cypher
MATCH (n:person {name:'Keanu Reeves'}) SET n:actor RETURN n;
MATCH (n:person {name:'Keanu Reeves'}) REMOVE n:actor RETURN n;
MATCH (n:person:movie) RETURN count(n);
CREATE (:aa:bb);
```

```
ERROR:  syntax error at or near ":"
```

Label inheritance is the substitute. `CREATE VLABEL actor INHERITS (person)` makes a
separate label that a match on the parent also returns. So `MATCH (n:person)` finds actors
too, and `MATCH (n:person ONLY)` excludes them. A vertex is created as an actor rather than
promoted to one. See [Label inheritance](/agensgraph/concepts/label-inheritance/).

### FOREACH {#foreach}

```cypher
FOREACH (x IN [1,2] | CREATE (:zz {v:x}));
```

```
ERROR:  syntax error at or near "FOREACH"
```

`UNWIND` and the GQL `FOR` statement both iterate a list:

```cypher
UNWIND [1,2] AS x RETURN x;
```

```
 x 
---
 1
 2
```

A write clause may follow either of them, so `UNWIND list AS x CREATE (…)` covers what a
`FOREACH` body carries.

### CREATE UNIQUE {#create-unique}

```cypher
MATCH (a:person {name:'Keanu Reeves'}), (b:movie {title:'Avatar'})
CREATE UNIQUE (a)-[:acted_in]->(b);
```

```
ERROR:  syntax error at or near "UNIQUE"
```

Use `MERGE`, which matches the pattern and creates it only if no match exists. Here the edge
already exists, so `MERGE` returns the existing one rather than adding a second:

```cypher
MATCH (a:person {name:'Sam Worthington'}), (b:movie {title:'Avatar'})
MERGE (a)-[r:acted_in]->(b)
RETURN id(r);
```

```
  id  
------
 5.21
```

### LOAD CSV {#load-csv}

```cypher
LOAD CSV WITH HEADERS FROM 'file:///tmp/movies.csv' AS row RETURN row;
```

```
ERROR:  syntax error at or near "CSV"
```

The import route goes through a table. `COPY` or a foreign table gets the CSV into a
relation, and `LOAD FROM` turns its rows into graph elements:

```sql
CREATE TABLE people_src (name text, age int);
INSERT INTO people_src VALUES ('Ann', 30), ('Bo', 41);
```

```cypher
LOAD FROM people_src AS r CREATE (:person {name: r.name, age: r.age});
```

```
UPDATE 2
```

```sql
DROP TABLE people_src;
```

See [Loading data](/agensgraph/guides/loading-data/) for the whole procedure, including the
foreign-table wrapper.

### The anonymous arrows `-->` and `--` {#the-anonymous-arrows----and---}

`--` starts a comment, as it does in SQL, so an anonymous arrow silently ends the statement:

```cypher
MATCH (a:movie)-->(b) RETURN count(*);
```

```
ERROR:  Cypher query must end with RETURN, FINISH or update clause
```

`<--` fails differently, because the `<` is consumed before the comment starts:

```cypher
MATCH (a:movie)<--(b) RETURN count(*);
```

```
ERROR:  syntax error at end of input
```

Write the bracketed forms. `-[]->`, `<-[]-` and `-[]-` all work:

```cypher
MATCH (a:movie)-[]->(b) RETURN count(*);
```

```
 count 
-------
 11
```

### Map projection {#map-projection}

```cypher
MATCH (m:movie {title:'Avatar'}) RETURN m {.title, .year};
```

```
ERROR:  syntax error at or near "{"
```

Build the map explicitly. A map constructor is an ordinary expression:

```cypher
MATCH (m:movie {title:'Avatar'}) RETURN {title: m.title, year: m.year};
```

```
             ?column?              
-----------------------------------
 {"year": 2009, "title": "Avatar"}
```

`properties(m)` returns the whole map, which covers `m {.*}`.

### Pattern comprehension {#pattern-comprehension}

```cypher
MATCH (m:movie {title:'Avatar'}) RETURN [(m)<-[:acted_in]-(p) | p.name];
```

```
ERROR:  syntax error at or near ":"
```

A subquery expression does the same job, and reads more like the rest of the language:

```cypher
MATCH (m:movie {title:'Avatar'})
RETURN COLLECT { MATCH (m)<-[:acted_in]-(p) RETURN p.name };
```

```
        array        
---------------------
 ["Sam Worthington"]
```

### `reduce()`, `extract()` and `filter()` {#reduce-extract-and-filter}

None of the three exists.

```cypher
RETURN reduce(acc = 0, x IN [1,2,3] | acc + x);
```

```
ERROR:  variable does not exist
```

`extract()` and `filter()` are syntax errors instead, because `extract` and `filter` are
already taken. `extract` is taken by SQL's `EXTRACT(field FROM source)`, and `filter` by the
GQL `FILTER` statement.

List comprehensions cover `extract()` and `filter()` and all three of their spellings work:

```cypher
RETURN [x IN [1,2,3] | x * 10], [x IN [1,2,3] WHERE x > 1], [x IN [1,2,3] WHERE x > 1 | x * 10];
```

```
   ?column?   | ?column? | ?column? 
--------------+----------+----------
 [10, 20, 30] | [2, 3]   | [20, 30]
```

For a fold, aggregate in SQL over the Cypher result, or use `sum()` where the fold is a sum.

### A bare pattern as a predicate {#a-bare-pattern-as-a-predicate}

A pattern is not a boolean expression:

```cypher
MATCH (m:movie) WHERE (m)<-[:acted_in]-() RETURN count(m);
```

```
ERROR:  syntax error at or near ":"
```

Wrap it in `exists()`, or in the GQL `EXISTS { }` subquery expression:

```cypher
MATCH (m:movie) WHERE exists((m)<-[:acted_in]-()) RETURN count(m);
```

```
 count 
-------
 18
```

### Backtick-quoted identifiers {#backtick-quoted-identifiers}

A backtick is not a quote character:

```cypher
MATCH (m:`movie`) RETURN count(m);
```

```
ERROR:  syntax error at or near "`"
```

Identifiers are quoted the SQL way, with double quotes: `MATCH (m:"movie")`. This matters
for the words that became reserved in 2.18. See [Keywords](/agensgraph/appendix/keywords/).

### Temporal, spatial and geodistance constructors {#temporal-spatial-and-geodistance-constructors}

`duration()`, `distance()` and `haversin()` do not exist:

```cypher
RETURN haversin(1.0);
```

```
ERROR:  function haversin(numeric) does not exist
HINT:  No function matches the given name and argument types. You might need to add explicit type casts.
```

`point()` and `timestamp()` fail more confusingly, because each collides with a PostgreSQL
name. `point({x:1, y:2})` finds PostgreSQL's geometric `point`, whose overloads take pairs of
floats and other geometries, so the call is ambiguous rather than absent:

```cypher
RETURN point({x:1, y:2});
```

```
ERROR:  function point(jsonb) is not unique
HINT:  Could not choose a best candidate function. You might need to add explicit type casts.
```

`timestamp()` is a syntax error, because `timestamp` is a type name.

`datetime()` exists but is a different function, and it is the one to watch. It takes a
time zone or a list of date parts, never an ISO-8601 string. Handing it a timestamp string
reads that string as a time zone:

```cypher
RETURN datetime('2020-01-01T00:00:00');
```

```
ERROR:  time zone "2020-01-01T00:00:00" not recognized
```

It does accept a zone name, or nine date parts:

```cypher
RETURN datetime(2020, 1, 1, 0, 0, 0, 0, 0, 'UTC');
```

```
       datetime        
-----------------------
 "2020-01-01T00:00:00"
```

For a timestamp from a string, cast: `'2020-01-01'::date`, `'2020-01-01 00:00'::timestamptz`.
`CURRENT_DATE` and `CURRENT_TIMESTAMP` work as bare keywords. Durations are PostgreSQL
intervals, reachable with `::interval` from SQL. Spatial work goes through a PostgreSQL
extension, reached from a graph query the same way vector search is. See [vector
search](/agensgraph/guides/search/vector/).

### The `db.*` procedures {#the-db-procedures}

There is no `db` namespace:

```cypher
CALL db.labels();
```

```
ERROR:  schema "db" does not exist
```

The catalogs answer the same questions. `ag_label` lists the labels of a graph. See [Graph
catalogs](/agensgraph/system-catalogs/catalogs/).

### PROFILE {#profile}

```cypher
PROFILE MATCH (m:movie) RETURN count(m);
```

```
ERROR:  syntax error at or near "PROFILE"
```

`EXPLAIN` works, with PostgreSQL's options: `EXPLAIN (ANALYZE, BUFFERS) MATCH …`.

## Behaviour that differs {#behaviour-that-differs}

### Every column a RETURN produces is jsonb {#every-column-a-return-produces-is-jsonb}

A property read is a `jsonb` value, and it stays one through the projection. A string
therefore prints with its JSON quotes:

```cypher
MATCH (m:movie {title:'Avatar'}) RETURN m.title, pg_typeof(m.title);
```

```
  title   | pg_typeof 
----------+-----------
 "Avatar" | "jsonb"
```

`::text` does not remove the quotes. It renders the jsonb value, quotes included. To get a
plain scalar, extract it in SQL around the Cypher:

```psql
SELECT t #>> '{}' AS title
FROM (MATCH (m:movie) RETURN m.title AS t) q
ORDER BY title LIMIT 1;
```

```
  title   
----------
 Avatar
```

See [SQL and Cypher](/agensgraph/querying/combining-sql-and-cypher/).

### `ORDER BY 2` sorts nothing {#order-by-2-sorts-nothing}

An integer in a sort key is a constant, not an output-column number. Sorting every row by
the same constant leaves the order untouched, and nothing warns you:

```cypher
MATCH (m:movie) RETURN m.title AS t, m.year AS y ORDER BY 2 LIMIT 5;
```

```
             t              |  y   
----------------------------+------
 "The Matrix Resurrections" | 2021
 "Inception"                | 2010
 "Interstellar"             | 2014
 "Avatar"                   | 2009
 "Blade Runner"             | 1982
```

Name the key. `ORDER BY y` sorts as expected. The integer form does work in SQL, where an
integer sort key means the output column at that position. So wrapping the Cypher in a
`SELECT … ORDER BY 2` sorts too.

```cypher
MATCH (m:movie) RETURN m.title AS t, m.year AS y ORDER BY y LIMIT 5;
```

```
              t               |  y   
------------------------------+------
 "Blade Runner"               | 1982
 "The Terminator"             | 1984
 "Total Recall"               | 1990
 "Terminator 2: Judgment Day" | 1991
 "Jurassic Park"              | 1993
```

### `n.id` is not the identity {#nid-is-not-the-identity}

`id` is an ordinary property name. Unless something wrote one, it is absent:

```cypher
MATCH (m:movie {title:'Avatar'}) RETURN m.id, id(m);
```

```
 id | id  
----+-----
    | 3.7
```

`id(m)` returns the identity, a `graphid` printed as *labid*`.`*locid*. See
[Limits](/agensgraph/appendix/limits/) for what those two halves hold.

### A bare `CALL { }` answers a different question {#a-bare-call---answers-a-different-question}

A subquery body does not see the outer variables. The name is rebound to a fresh,
unconstrained variable, so the body runs over the whole graph rather than the current row:

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

25 is every `acted_in` edge in the graph. With an import list the same query is correct:

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

> [!IMPORTANT]
> Always give a `CALL` subquery an import list — `CALL (v) { … }`, `CALL (*) { … }` or
> `CALL { WITH v … }`. All three are correct and agree. The bare form is the one shape of this
> divergence that answers a different question rather than raising an error.

### `shortestpath` endpoints must be named variables {#shortestpath-endpoints-must-be-named-variables}

An inline pattern in an endpoint is refused:

```cypher
MATCH p = shortestpath((:movie {title:'The Matrix'})-[:related_to*..4]->(:movie {title:'Inception'}))
RETURN length(p);
```

```
ERROR:  node must be a reference to a specific node
```

Bind both ends first:

```cypher
MATCH (a:movie {title:'The Matrix'}), (b:movie {title:'Inception'})
MATCH p = shortestpath((a)-[:related_to*..4]->(b))
RETURN length(p);
```

```
 length 
--------
 2
```

The same rule applies to `allshortestpaths()` and `dijkstra()`.

### An unquoted label folds to lower case {#an-unquoted-label-folds-to-lower-case}

Identifiers follow SQL's folding rule, so a label written in mixed case is looked up in
lower case:

```cypher
MATCH (m:Movie) RETURN count(m);
```

```
 count 
-------
 18
```

`Movie`, `MOVIE` and `movie` are the same label. A label created with a quoted mixed-case
name has to be quoted at every use.

### A condition takes only a boolean {#a-condition-takes-only-a-boolean}

Reading a property for truthiness raises a cast error rather than testing for non-empty:

```cypher
MATCH (m:movie {year: 1999}) WHERE m.title RETURN count(m);
```

```
ERROR:  cannot cast "The Matrix" (jsonb type string) to boolean
```

The message names the first value the executor reached, so an unconstrained `MATCH` over
several rows reports whichever one it happened to read first.

This holds in `WHERE`, `FILTER`, `AND`, `OR`, `NOT`, `XOR`, `CASE WHEN` and `dijkstra()`'s
qualifier. Write the test you mean, as in `WHERE m.title IS NOT NULL` or
`WHERE m.count <> 0`. Or cast explicitly with `::boolean`.

### A missing label is not an error {#a-missing-label-is-not-an-error}

A pattern naming a label that does not exist matches nothing and returns a row count of
zero:

```cypher
MATCH (n:no_such_label) RETURN count(n);
```

```
 count 
-------
 0
```

A typo in a label name therefore looks like an empty result. Check the label list in
`ag_label` when a query returns nothing you expected.

### `size()` and `length()` are the same function {#size-and-length-are-the-same-function}

`size()` is another spelling of `length()`, and the output column is named `length` whichever
you write:

```cypher
RETURN size([1,2,3]), size('abcd'), length('abcd');
```

```
 length | length | length 
--------+--------+--------
 3      | 4      | 4
```

`size()` over a pattern counts matches, and names its column `count`:

```cypher
MATCH (m:movie {title:'Avatar'}) RETURN size((m)<-[:acted_in]-());
```

```
 count 
-------
 1
```

### `labels()` always returns one label {#labels-always-returns-one-label}

`labels()` exists and returns a list, but the list has exactly one element, because a vertex
has one label:

```cypher
MATCH (n:person) RETURN labels(n) LIMIT 1;
```

```
   labels   
------------
 ["person"]
```

`label(n)` returns that one label as a scalar and is the form to prefer. `type(r)` and
`label(r)` both work on an edge.

### `collect()` over a graph element returns a native array {#collect-over-a-graph-element-returns-a-native-array}

Collecting vertices gives a `vertex[]`, not a list of pictures, so the collected elements
stay usable:

```cypher
MATCH (m:movie) RETURN pg_typeof(collect(m));
```

```
 pg_typeof  
------------
 "vertex[]"
```

```cypher
MATCH (m:movie) WITH collect(m) AS ms RETURN ms[0].title;
```

```
           title            
----------------------------
 "The Matrix Resurrections"
```

Collecting a *property* still returns a jsonb list.

### A vertex with edges will not delete {#a-vertex-with-edges-will-not-delete}

`DELETE` refuses to leave a dangling edge:

```cypher
MATCH (m:movie {title:'Avatar'}) DELETE m;
```

```
ERROR:  Vertex with connected edges cannot be removed
HINT:  Use DETACH DELETE or remove connected edges before deleting the vertex.
```

### A query needs a graph to run against {#a-query-needs-a-graph-to-run-against}

There is no default graph. With `graph_path` unset, every graph statement is refused:

```cypher
RESET graph_path;
MATCH (m:movie) RETURN count(m);
```

```
ERROR:  graph_path is NULL
HINT:  Use SET graph_path
```

Set it for the session, or set it in `postgresql.conf` or per role. See
[Configuration](/agensgraph/operations/configuration/):

```cypher
SET graph_path = moviekb;
```

## AgensGraph additions {#agensgraph-additions}

These have no counterpart in other Cypher implementations, so a query using them does not
port outward.

`MATCH (n:label ONLY)` restricts a match to one label, excluding the labels that inherit from
it. Without `ONLY` a match on a parent label returns its children too.

`SET n += map` merges a map into the properties rather than replacing them:

```cypher
MATCH (n:person {name:'Keanu Reeves'}) SET n += {city:'Seoul'} RETURN properties(n);
```

```
                       properties                        
---------------------------------------------------------
 {"born": 1964, "city": "Seoul", "name": "Keanu Reeves"}
```

`LOAD FROM table AS r CREATE (…)` creates graph elements from the rows of a relation, which
is how bulk loading works.

`dijkstra((a)-[e:related_to]->(b), e.weight)` finds a weighted shortest path. It respects the
weights, so the cheapest route need not be the shortest one in hops:

```cypher
MATCH (a:movie {title:'The Matrix'}), (b:movie {title:'Inception'})
MATCH p = dijkstra((a)-[e:related_to]->(b), e.weight)
RETURN [x IN nodes(p) | x.title];
```

```
                  ?column?                   
---------------------------------------------
 ["The Matrix", "Total Recall", "Inception"]
```

A Cypher query is a table expression and a label is a table, so SQL and Cypher can be mixed
in one statement:

```psql
SELECT q.title #>> '{}' AS film, r.score
FROM (MATCH (p:person)-[:directed]->(m:movie)
      WHERE p.name = 'Christopher Nolan'
      RETURN m.title AS title) q
JOIN rating r ON r.title = q.title #>> '{}'
WHERE r.source = 'critics'
ORDER BY r.score DESC;
```

```
     film     | score 
--------------+-------
 Inception    |   8.8
 Interstellar |   8.7
```

## See also {#see-also}

- [GQL conformance](/agensgraph/appendix/gql-conformance/) — which parts of ISO/IEC 39075 are supported
- [Keywords](/agensgraph/appendix/keywords/) — the words 2.18 reserved, and what breaks
- [SQL and Cypher](/agensgraph/querying/combining-sql-and-cypher/) — the crossing, in full
- [Cypher, GQL and SQL](/agensgraph/concepts/languages/) — how the three languages relate
