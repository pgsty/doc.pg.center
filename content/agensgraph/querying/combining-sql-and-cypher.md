---
title: Combining SQL and Cypher
linkTitle: Combining SQL and Cypher
description: There is no bridge between SQL and Cypher in AgensGraph, because there is nothing to bridge.
type: docs
weight: 70
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/querying/combining-sql-and-cypher.html
upstream_source: agensgraph
upstream_modified: true
---


There is no bridge between SQL and Cypher in AgensGraph, because there is nothing to bridge.
A graph is a set of PostgreSQL tables in the same database as your ordinary tables, and both
languages compile to the same plan tree.

So the two mix by nesting: a Cypher query goes where SQL expects a table, and a SQL query goes
where Cypher expects a value.

This page walks the crossing points, in the order you are likely to need them, and then the
one rule that surprises everybody: what a Cypher `RETURN` hands back.

Everything runs against [the example dataset](/agensgraph/get-started/example-dataset/), which
includes an ordinary table, `rating`, that is not part of the graph.

## Reading a label with plain SQL {#reading-a-label-with-plain-sql}

A label is a table, so no Cypher is needed to read one:

```sql
SELECT id, properties->>'title' AS title, properties->>'year' AS year
FROM moviekb.movie ORDER BY (properties->>'year')::int LIMIT 3;
```

```
  id  |     title      | year 
------+----------------+------
 3.8  | Blade Runner   | 1982
 3.15 | The Terminator | 1984
 3.11 | Total Recall   | 1990
```

Nothing needs enabling for that. Writing rows into a label with SQL does; see [What is
deliberately closed
off](/agensgraph/concepts/graph-on-postgresql/#what-is-deliberately-closed-off). Reading is just
reading.

Direct SQL is the right tool when the question is relational: counts per label, a join to a
reference table on a property value, a window function over a property. It is the wrong tool
for anything with a variable number of hops. The rest of this page covers those.

## A Cypher query in a SQL FROM {#a-cypher-query-in-a-sql-from}

Put a Cypher query in parentheses where a SQL `FROM` expects a table, and give it an alias.
Its `RETURN` list becomes the columns:

```psql
SELECT * FROM (MATCH (m:movie) WHERE m.year > 2015 RETURN m.title AS title, m.year AS year) q
ORDER BY year;
```

```
           title            | year 
----------------------------+------
 "Blade Runner 2049"        | 2017
 "The Matrix Resurrections" | 2021
```

The alias is required:

```psql
SELECT count(*) FROM (MATCH (m:movie) RETURN m.title AS title);
```

```
ERROR:  Cypher in FROM must have an alias
HINT:  For example, FROM (...) [AS] foo.
```

Two more rules. Every column needs a name, because the outer query has to be able to refer to
it. So `RETURN m.title` without `AS` is refused. And the nested query must be a read: a write
clause inside a `FROM` is a syntax error.

You can nest more than one, and join them like any two subqueries:

```psql
SELECT d.name #>> '{}' AS director, a.name #>> '{}' AS actor
FROM (MATCH (p:person)-[:directed]->(:movie {title: 'The Matrix'}) RETURN p.name AS name) d
CROSS JOIN (MATCH (p:person)-[:acted_in]->(:movie {title: 'The Matrix'}) RETURN p.name AS name) a
ORDER BY director, actor LIMIT 4;
```

```
    director     |       actor        
-----------------+--------------------
 Lana Wachowski  | Carrie-Anne Moss
 Lana Wachowski  | Keanu Reeves
 Lana Wachowski  | Laurence Fishburne
 Lilly Wachowski | Carrie-Anne Moss
```

## Joining a graph to an ordinary table {#joining-a-graph-to-an-ordinary-table}

This is the reason most people come to this page. Ask the graph a graph question, then join
its answer to relational data:

```psql
SELECT q.title #>> '{}' AS film, r.score
FROM (MATCH (:person {name: 'Christopher Nolan'})-[:directed]->(m:movie) RETURN m.title AS title) q
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

The `#>> '{}'` on both sides is the whole trick, and [the next
section](#getting-a-plain-value-out) explains it. Without it you are comparing a `jsonb`
string against a `text` column, which does not type-check.

A graph and a table have no foreign keys between them, so the join key is a value: a title, a
code, an external id. If you control the model, store that id as a property and index it.

If the join is hot, promote it to a column: a `text` column joins to a `text` column with no
casting at all. See [Promoting a property to a column](/agensgraph/querying/typed-columns/).

## A Cypher query in a CTE {#a-cypher-query-in-a-cte}

A `WITH` clause takes a Cypher query as easily as a `SELECT`. That gives you a name you can
reference more than once:

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

Note which language the *statement* is in. A statement beginning with `WITH cte AS (...)` is
SQL, and its body has to be SQL. This is not Cypher's `WITH`, which is a pipeline divider and
cannot name a subquery. See [How they
differ](/agensgraph/querying/composing/#how-it-differs-from-a-cte).

The pattern generalises to aggregating a traversal relationally. Here Cypher counts each
film's cast and SQL averages the scores:

```psql
WITH cast_size AS (
  MATCH (p:person)-[:acted_in]->(m:movie) RETURN m.title AS title, count(p) AS players
)
SELECT c.title #>> '{}' AS film, c.players #>> '{}' AS players, round(avg(r.score), 2) AS mean_score
FROM cast_size c JOIN rating r ON r.title = c.title #>> '{}'
GROUP BY 1, 2 ORDER BY 3 DESC LIMIT 4;
```

```
            film            | players | mean_score 
----------------------------+---------+------------
 The Matrix                 | 3       |       8.90
 Inception                  | 1       |       8.90
 Interstellar               | 1       |       8.65
 Terminator 2: Judgment Day | 2       |       8.60
```

## SQL inside a Cypher query {#sql-inside-a-cypher-query}

The nesting works in the other direction too. A SQL scalar subquery is an expression, so it
goes anywhere Cypher wants one: in a `WHERE`, in a `RETURN`, in a property value being
written:

```cypher
MATCH (m:movie)
WHERE m.title = (SELECT title FROM rating WHERE source = 'critics' ORDER BY score DESC LIMIT 1)
RETURN m.title AS title, m.year AS year;
```

```
    title    | year 
-------------+------
 "Inception" | 2010
```

The subquery must return one row and one column, as in SQL. No cast was needed here: the
subquery's `text` was compared against a `jsonb` property, and the comparison resolved. The
other direction is the one that needs `#>> '{}'`: a `jsonb` property into a `text` column.

A user-defined function is an expression as well, so a SQL function can be called from a
Cypher `RETURN`:

```sql
CREATE FUNCTION decade(y int) RETURNS int AS 'SELECT (y / 10) * 10' LANGUAGE sql IMMUTABLE;
```

```cypher
MATCH (m:movie) RETURN decade(m.year::int) AS decade, count(*) AS films ORDER BY decade;
```

```
 decade | films 
--------+-------
 1980   | 2
 1990   | 6
 2000   | 4
 2010   | 5
 2020   | 1
```

The `::int` on `m.year` turns the jsonb property into an argument the function's signature
accepts. Any language works: PL/pgSQL, PL/Python, C. So does any aggregate or window
function, because Cypher's aggregates *are* PostgreSQL's.

## Getting a plain value out {#getting-a-plain-value-out}

Anything a Cypher `RETURN` derives from a property comes back as `jsonb`. That is not a
display quirk; it is the column's type. Casting or unwrapping *inside* the query does not
change it, because the projection re-boxes the result.

This is the single most common source of confusion at this boundary, so here it is from every
angle.

Not every column is boxed, only the property-derived ones. Checking the outer types of a
Cypher subquery's columns shows the rule exactly:

```psql
SELECT pg_typeof(raw) AS raw, pg_typeof(cast_text) AS cast_text,
       pg_typeof(unwrapped) AS unwrapped, pg_typeof(is_modern) AS boolean_expr,
       pg_typeof(gid) AS gid, pg_typeof(v) AS vertex
FROM (MATCH (m:movie {title: 'The Matrix'})
      RETURN m.title AS raw, m.title::text AS cast_text, m.title #>> '{}' AS unwrapped,
             m.year > 1990 AS is_modern, id(m) AS gid, m AS v) q;
```

```
  raw  | cast_text | unwrapped | boolean_expr |   gid   | vertex
-------+-----------+-----------+--------------+---------+--------
 jsonb | jsonb     | jsonb     | boolean      | graphid | vertex
```

So a boolean expression stays `boolean`, `id(m)` stays `graphid`, and a graph element stays
`vertex`, `edge` or `graphpath`. The three property-derived columns arrive as `jsonb`. That
includes the one that was cast to `text` and the one that was already unwrapped.

A string property comes back JSON-quoted:

```cypher
MATCH (m:movie {title: 'The Matrix'}) RETURN m.title AS t;
```

```
      t       
--------------
 "The Matrix"
```

Casting inside the Cypher query does not help, because the outer projection re-boxes the
result:

```cypher
MATCH (m:movie {title: 'The Matrix'}) RETURN m.title::text AS t;
```

```
      t       
--------------
 "The Matrix"
```

```psql
SELECT pg_typeof(t) AS type FROM (MATCH (m:movie {title: 'The Matrix'}) RETURN m.title::text AS t) q;
```

```
 type  
-------
 jsonb
```

Neither does extracting the text with `#>> '{}'` inside Cypher, for the same reason:

```cypher
MATCH (m:movie {title: 'The Matrix'}) RETURN m.title #>> '{}' AS t;
```

```
      t       
--------------
 "The Matrix"
```

**The way out is to do the unwrapping in SQL, one level up.** Wrap the Cypher query and apply
`#>> '{}'` outside it. That operator is jsonb's "extract the value at the empty path as
text":

```psql
SELECT t #>> '{}' AS t FROM (MATCH (m:movie {title: 'The Matrix'}) RETURN m.title AS t) q;
```

```
     t      
------------
 The Matrix
```

```psql
SELECT pg_typeof(t #>> '{}') AS type FROM (MATCH (m:movie {title: 'The Matrix'}) RETURN m.title AS t) q;
```

```
 type 
------
 text
```

From there the value behaves like any `text`: compare it to a column, pass it to a function,
cast it onwards with `(q.year #>> '{}')::int` for a number.

Three notes on this rule.

It applies to the outermost projection only. A property read *within* a Cypher expression
keeps its type all the way through. So `decade(m.year::int)` above works.

A **promoted** property is the exception. A property with a typed column behind it comes back
as that column's type, not as jsonb. So `RETURN m.year` on a promoted `year` is already an
`integer` and needs no unwrapping. See [A promoted read has the column's
type](/agensgraph/querying/typed-columns/#a-promoted-read-has-the-columns-type).

A vertex or an edge comes back as its own composite type, not as jsonb, and SQL can take it
apart with field notation:

```psql
SELECT pg_typeof(m) AS type, (m).id AS id, (m).properties->>'title' AS title
FROM (MATCH (m:movie {title: 'The Matrix'}) RETURN m) q;
```

```
  type  | id  |   title    
--------+-----+------------
 vertex | 3.1 | The Matrix
```

The parentheses around `m` are SQL's, required whenever you read a field of a composite
column.

## A view over a Cypher query {#a-view-over-a-cypher-query}

A view cannot begin with a Cypher clause:

```psql
CREATE VIEW film_rating AS MATCH (m:movie) RETURN m.title AS title;
```

```
ERROR:  syntax error at or near "MATCH"
```

Wrap it in a `SELECT` and it works. So a graph traversal can be published as a relational
view for anything that speaks SQL: a BI tool, an ORM, a foreign data wrapper:

```psql
CREATE VIEW film_rating AS
SELECT q.title #>> '{}' AS title, (q.year #>> '{}')::int AS year, r.score
FROM (MATCH (m:movie) RETURN m.title AS title, m.year AS year) q
JOIN rating r ON r.title = q.title #>> '{}'
WHERE r.source = 'critics';
```

```sql
SELECT * FROM film_rating ORDER BY score DESC LIMIT 4;
```

```
           title            | year | score 
----------------------------+------+-------
 Inception                  | 2010 |   8.8
 Interstellar               | 2014 |   8.7
 The Matrix                 | 1999 |   8.7
 Terminator 2: Judgment Day | 1991 |   8.6
```

The view is an ordinary view, so it lands in the SQL search path rather than in the graph.
`graph_path` says which graph a label name belongs to; it says nothing about where a view goes:

```sql
SELECT schemaname, viewname FROM pg_views WHERE viewname = 'film_rating';
```

```
 schemaname |  viewname   
------------+-------------
 public     | film_rating
```

### What the server stored {#what-the-server-stored}

A view holds a parsed query tree, not your text. Ask for the definition back and you get the
*lowered SQL* the Cypher compiled to, not the Cypher you wrote:

```sql
SELECT pg_get_viewdef('public.film_rating'::regclass, true);
```

```
                            pg_get_viewdef                             
-----------------------------------------------------------------------
  SELECT q.title #>> '{}'::text[] AS title,                           +
     (q.year #>> '{}'::text[])::integer AS year,                      +
     r.score                                                          +
    FROM ( SELECT (_agens_default_s.m).properties.'title' AS title,   +
             (_agens_default_s.m).properties.'year' AS year           +
            FROM ( SELECT ROW(m.id, m.properties, m.ctid)::vertex AS m+
                    FROM moviekb.movie m) _agens_default_s) q         +
      JOIN rating r ON r.title = (q.title #>> '{}'::text[])           +
   WHERE r.source = 'critics'::text;
```

That is worth reading once, because it is the clearest possible statement of what a Cypher
query *is* on this engine. `MATCH (m:movie)` became a scan of `moviekb.movie` whose rows are
assembled into a `vertex` value. `m.title` became `(m).properties.'title'`. The names
beginning `_agens_default_s` are the generated aliases for the pipeline's stages.

Two consequences follow.

**Your Cypher is not recoverable from the catalog.** Keep the source of a view under version
control, the way you would any other schema object. This is not specific to views. Anything
built on a stored query tree records the lowered form: a rule, a materialised view.

**It round-trips.** `pg_dump` emits that same lowered SQL, and restoring it rebuilds a working
view. The definition after a dump and restore into a fresh database is identical, character
for character, and the view returns the same rows.

So a view over a Cypher query is safe to rely on operationally, even though it does not read
back as you wrote it.

One thing to watch: if the Cypher resolved a property to a [promoted
column](/agensgraph/querying/typed-columns/), the view holds a dependency on that column. Dropping the column is
refused until the view goes. That is deliberate, because the view would otherwise silently
change meaning.

## Clean up {#clean-up}

```sql
DROP VIEW film_rating;
DROP FUNCTION decade(int);
```

## Where to go next {#where-to-go-next}

* [How a graph is stored](/agensgraph/concepts/graph-on-postgresql/) — why any of this
  works, and the two gates on writing to a label with SQL.
* [Composing a query](/agensgraph/querying/composing/) — Cypher's own pipeline, and where its `WITH` differs from
  a CTE.
* [Loading data](/agensgraph/guides/loading-data/) — `LOAD FROM`, which reads an ordinary table into
  a graph.
* [Promoting a property to a column](/agensgraph/querying/typed-columns/) — for a join key you use constantly.
