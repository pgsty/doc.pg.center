---
title: Promoting a property to a column
linkTitle: Promoting a property to a column
description: A label is schemaless because a property lives in a per-element jsonb document.
type: docs
weight: 60
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/querying/typed-columns.html
upstream_source: agensgraph
upstream_modified: true
---


A label is schemaless because a property lives in a per-element `jsonb` document. That costs
you two things.

Reading `m.year` means finding the `year` key inside a JSON document, for every row the query
touches. And the value the read produces is a jsonb value, so an index over it is an index
over jsonb. It is never an index over an `integer` or a `vector`.

Promotion removes both costs for one chosen key. `ALTER VLABEL film ADD COLUMN year int
GENERATED` gives the `year` property a real `integer` column, stored beside the bag and
maintained by the server. It also teaches the Cypher compiler to answer `f.year` from that
column.

Queries do not change. Nothing about the property changes either: it is still a property, the
label is still schemaless in every other key, and the promotion can be undone.

This page is about when that trade is worth making and what you take on with it. The DDL
syntax is in [`ALTER VLABEL`](/agensgraph/reference/ddl/alter-label/) and
[`CREATE VLABEL`](/agensgraph/reference/ddl/create-vlabel/).

## A label of your own to promote on {#a-label-of-your-own-to-promote-on}

Promotion is a change to a label's shape, so work on a copy rather than on the manual's
shared graph. `LOAD FROM` over a label table copies its property bags straight across:

```cypher
CREATE GRAPH promolab;
SET graph_path = promolab;
CREATE VLABEL film;
LOAD FROM moviekb.movie AS r CREATE (:film = r.properties);
```

That gives you the 18 films of [the example
dataset](/agensgraph/get-started/example-dataset/) in a graph you can reshape freely. The whole page
runs there and drops it at the end.

## What promotion does {#what-promotion-does}

Before promoting, a filter on `year` reaches into the bag. `EXPLAIN (VERBOSE)` shows the
property reads as `properties.'key'`:

```cypher
EXPLAIN (VERBOSE, COSTS OFF) MATCH (f:film) WHERE f.year > 2010 RETURN f.title;
```

```
                   QUERY PLAN                    
-------------------------------------------------
 Seq Scan on promolab.film f
   Output: f.properties.'title'
   Filter: (f.properties.'year' > '2010'::jsonb)
```

Promote it:

```cypher
ALTER VLABEL film ADD COLUMN year int GENERATED;
```

```psql
\d promolab.film
```

```
                                                            Table "promolab.film"
   Column   |  Type   | Collation | Nullable |                                            Default                                            
------------+---------+-----------+----------+-----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('promolab.film'::cstring), nextval('promolab.film_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
 year       | integer |           |          | generated always as (ag_property_text(properties, 'year'::text, 'n'::"char")::integer) stored
Indexes:
    "film_pkey" PRIMARY KEY, btree (id)
Inherits: promolab.ag_vertex
```

The column is `GENERATED ALWAYS AS ... STORED`: an ordinary PostgreSQL generated column whose
expression pulls one key out of the bag. `ag_property_text(properties, 'year', 'n')` returns
the key's text only when the value is of the kind the column can hold: `'n'` for a number,
`'s'` for a string, `'b'` for a boolean.

The cast to `integer` does the rest. Nobody writes to it; the server computes it on every
insert and update.

The same query now filters on the column:

```cypher
EXPLAIN (VERBOSE, COSTS OFF) MATCH (f:film) WHERE f.year > 2010 RETURN f.title;
```

```
           QUERY PLAN           
--------------------------------
 Seq Scan on promolab.film f
   Output: f.properties.'title'
   Filter: (f.year > 2010)
```

`f.title` is still a bag read, because only `year` was promoted. The answers are unchanged:

```cypher
MATCH (f:film) WHERE f.year > 2010 RETURN f.title AS title, f.year AS year ORDER BY year;
```

```
           title            | year 
----------------------------+------
 "The Avengers"             | 2012
 "Elysium"                  | 2013
 "Interstellar"             | 2014
 "Blade Runner 2049"        | 2017
 "The Matrix Resurrections" | 2021
```

Existing rows are filled in as part of the `ALTER`, so the column is complete the moment it
exists. And the value is in **both** places. The bag still holds it:

```sql
SELECT properties->>'title' AS title, year, properties->>'year' AS in_the_bag
FROM promolab.film ORDER BY year LIMIT 3;
```

```
     title      | year | in_the_bag 
----------------+------+------------
 Blade Runner   | 1982 | 1982
 The Terminator | 1984 | 1984
 Total Recall   | 1990 | 1990
```

That duplication is deliberate. The property stays a property, so a client reading
`properties` sees what it always saw. A dump carries the data once in the bag and regenerates
the column. Dropping the column loses nothing. The price is storage: you are paying for the
value twice.

The mapping from property key to column is recorded in `ag_label_property`:

```sql
SELECT l.labname, p.propname, a.attname, format_type(a.atttypid, a.atttypmod) AS type
FROM pg_catalog.ag_label l
  JOIN pg_catalog.ag_label_property p ON p.laboid = l.oid
  JOIN pg_attribute a ON a.attrelid = l.relid AND a.attnum = p.attnum
WHERE l.relid = 'promolab.film'::regclass;
```

```
 labname | propname | attname |  type   
---------+----------+---------+---------
 film    | year     | year    | integer
```

That row makes the read resolve to the column. Without it the column would exist, but Cypher
would not know about it. See [The long form registers
nothing](#the-long-form-registers-nothing-unless-it-is-a-single-key).

### A promoted read has the column's type {#a-promoted-read-has-the-columns-type}

A Cypher `RETURN` hands back a property read as jsonb, so `RETURN f.title` prints
`"The Matrix"` with the quotes. Reading a promoted key is the exception: it comes back as the
column's declared type. Here `year` is promoted and `title` is not.

```cypher
SELECT pg_typeof(t) AS title_type, pg_typeof(y) AS year_type
FROM (MATCH (f:film) RETURN f.title AS t, f.year AS y LIMIT 1) q;
```

```
 title_type | year_type 
------------+-----------
 jsonb      | integer
```

Values and orderings are the same either way; the *type* the client receives is not. A driver
that expects every Cypher column to arrive as JSON will see an `integer` here.

This is usually a simplification, because it is the shortest route to [a plain
value](/agensgraph/querying/combining-sql-and-cypher/#getting-a-plain-value-out). But it is a change in the
result's shape, and worth checking against whatever consumes it.

## Indexing a promoted column {#indexing-a-promoted-column}

`CREATE PROPERTY INDEX` on a promoted key builds a plain btree over the column rather than an
expression index over the bag. The planner uses it as it would any column index. [Indexes and
constraints](/agensgraph/querying/indexes-and-constraints/#what-promotion-changes) measures which predicates it
can serve, and the two that get *worse* after promotion. The short version:

* Equality, ranges and `ORDER BY` are served, and `ORDER BY` improves to an index-only scan.
* `IS NULL` becomes indexable, which it was not on the bag.
* `IN` and `STARTS WITH` stop using the index, because the column is boxed back to jsonb to
  meet the jsonb operand.

One rule follows, and it is easy to miss: **an index over the bag is dead the moment you
promote the key.** Nothing compiles to `properties.'year'` any more, so an index over that
expression is never matched. It is still maintained on every write. Promoting is always two
steps: promote, then rebuild the index on the column.

## Declaring promoted columns with the label {#declaring-promoted-columns-with-the-label}

At creation time the columns go in the label definition:

```cypher
CREATE VLABEL doc (words int GENERATED, tag text GENERATED (category));
```

`words int GENERATED` promotes the property `words` to a column of the same name. The
parenthesised form promotes a *different* key: `tag text GENERATED (category)` says "column
`tag`, filled from the property `category`". Use it when the key you want is not a legal or
sensible column name.

The catalog records the key, not the column name:

```sql
SELECT l.labname, p.propname, a.attname, format_type(a.atttypid, a.atttypmod) AS type
FROM pg_catalog.ag_label l
  JOIN pg_catalog.ag_label_property p ON p.laboid = l.oid
  JOIN pg_attribute a ON a.attrelid = l.relid AND a.attnum = p.attnum
WHERE l.relid = 'promolab.doc'::regclass ORDER BY p.propname;
```

```
 labname | propname | attname |  type   
---------+----------+---------+---------
 doc     | category | tag     | text
 doc     | words    | words   | integer
```

So the Cypher read that resolves to the column is `d.category`, the key. `d.tag` is a
property nobody has ever set:

```cypher
CREATE (:doc {title: 'a note', words: 12, category: 'news'});
MATCH (d:doc) RETURN d.words AS words, d.category AS category, d.tag AS tag;
```

```
 words | category | tag 
-------+----------+-----
    12 | news     | 
```

`ALTER ELABEL` promotes an edge property the same way. It is worth doing for a weight you
traverse on.

## Extension types {#extension-types}

The column's type can come from an extension. That is the case that makes promotion more than
a micro-optimisation. An embedding stored as a property is a JSON array, so every similarity
query has to cast it: `p.emb::vector(4)`, on every row, every time. Promote it and the cast
happens once, at write time:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

```cypher
CREATE VLABEL page (emb vector(4) GENERATED);
```

```psql
\d promolab.page
```

```
                                                           Table "promolab.page"
   Column   |   Type    | Collation | Nullable |                                          Default                                          
------------+-----------+-----------+----------+-------------------------------------------------------------------------------------------
 id         | graphid   |           | not null | graphid(graph_labid('promolab.page'::cstring), nextval('promolab.page_id_seq'::regclass))
 properties | jsonb     |           | not null | jsonb_build_object()
 emb        | vector(4) |           |          | generated always as (((properties ->> 'emb'::text))::vector(4)) stored
Indexes:
    "page_pkey" PRIMARY KEY, btree (id)
Inherits: promolab.ag_vertex
```

Note the generation expression. For a type with no JSON counterpart the server uses plain
`->>` rather than `ag_property_text`, and leaves the type's own input function to accept or
refuse the text. `vector(4)` refuses anything that is not four numbers in brackets.

The column can then carry a real vector index. The index definition needs no cast expression,
because there is no cast left to make. Load enough rows for an index to be worth choosing
first:

```sql
CREATE TABLE seed_page AS
SELECT 'page ' || g AS title, jsonb_build_array(random(), random(), random(), random()) AS emb
FROM generate_series(1, 5000) g;
```

```cypher
LOAD FROM seed_page AS r CREATE (:page {title: r.title, emb: r.emb});
CREATE PROPERTY INDEX ON page USING hnsw (emb vector_cosine_ops);
```

```sql
ANALYZE promolab.page;
```

and a Cypher similarity search uses it:

```cypher
EXPLAIN (COSTS OFF)
MATCH (p:page) RETURN p.title AS title
ORDER BY p.emb <=> '[0.1,0.2,0.3,0.4]'::vector(4) LIMIT 3;
```

```
                         QUERY PLAN                         
------------------------------------------------------------
 Limit
   ->  Index Scan using page_emb_idx on page p
         Order By: (emb <=> '[0.1,0.2,0.3,0.4]'::vector(4))
```

The unpromoted form of the same query has to compute a distance for every row and sort them:

```cypher
SET enable_property_promotion = off;
EXPLAIN (COSTS OFF)
MATCH (p:page) RETURN p.title AS title
ORDER BY p.emb::vector(4) <=> '[0.1,0.2,0.3,0.4]'::vector(4) LIMIT 3;
RESET enable_property_promotion;
```

```
                                        QUERY PLAN                                        
------------------------------------------------------------------------------------------
 Limit
   ->  Sort
         Sort Key: (((p.properties.'emb')::vector(4) <=> '[0.1,0.2,0.3,0.4]'::vector(4)))
         ->  Seq Scan on page p
```

An `::vector(4)` you leave in place on a promoted column is folded away rather than refused,
so existing queries keep working and keep using the index.

Prefer promotion to a property index over a *cast expression* such as
`((emb::vector(4)) vector_cosine_ops)`. Over a promoted column the index is an ordinary
column index, which is the more durable form across a dump and restore. See [Vector
search](/agensgraph/guides/search/vector/).

## What promotion costs you {#what-promotion-costs-you}

### A promoted key is no longer schemaless {#a-promoted-key-is-no-longer-schemaless}

This is the real trade. Every other key on the label still accepts any JSON value. The
promoted one accepts only what the column can hold, and a write that does not fit aborts:

```cypher
CREATE (:film {title: 'Bad Year', year: 'nineteen ninety nine'});
```

```
ERROR:  property "year" holds a string
DETAIL:  A column promoting this property holds numbers.
CONTEXT:  while computing the promoted typed columns of graph label "film"
```

```cypher
CREATE (:film {title: 'Fractional', year: 1999.5});
```

```
ERROR:  invalid input syntax for type integer: "1999.5"
CONTEXT:  while computing the promoted typed columns of graph label "film"
```

Two different checks are visible there. The first is the kind check: a string is not a number,
whatever it says. The second is the column type's own. For an extension type only the second
applies:

```cypher
CREATE (:page {title: 'wrong dims', emb: [1, 2, 3]});
```

```
ERROR:  expected 4 dimensions, not 3
CONTEXT:  while computing the promoted typed columns of graph label "page"
```

Leaving the key out entirely is always fine. An absent property makes a null column, exactly
as an absent property reads as null:

```cypher
CREATE (:film {title: 'Undated'});
MATCH (f:film {title: 'Undated'}) RETURN f.year AS year;
```

```
 year 
------
     
```

Promoting is therefore a decision about data quality as much as about speed. Before you
promote a key on a live label, find out whether every existing value fits. The `ALTER` applies
the same checks to the rows already there, and fails on the first one that does not:

```cypher
CREATE VLABEL city;
CREATE (:city {name: 'Seoul', pop: 9700000}), (:city {name: 'Nowhere', pop: 'many'});
```

```cypher
ALTER VLABEL city ADD COLUMN pop bigint GENERATED;
```

```
ERROR:  property "pop" holds a string
DETAIL:  A column promoting this property holds numbers.
```

That failure is the useful kind: it tells you the label's data is not what you thought before
anything is committed.

### The ALTER rewrites the table {#the-alter-rewrites-the-table}

Adding a stored generated column rewrites the label's heap and takes an `ACCESS EXCLUSIVE`
lock while it does. On this 18-row label it is instant. On a large label, plan for it as you
would plan any `ALTER TABLE` rewrite. Check the relation's file number if you want to see it
happen:

```sql
SELECT relfilenode FROM pg_class WHERE oid = 'promolab.film'::regclass;
```

The number before the `ALTER` and the number after it are different.

### A promoted column cannot have a collation of its own {#a-promoted-column-cannot-have-a-collation-of-its-own}

A property map compares strings with the database default collation. A column collated any
other way would order and compare the same values differently. That would make "which of the
two answers this read" a decision about results rather than about speed.

So it is refused, including when the collation arrives through a domain rather than being
written down:

```sql
CREATE DOMAIN sortkey AS text COLLATE "C";
```

```cypher
CREATE VLABEL note;
ALTER VLABEL note ADD COLUMN k sortkey GENERATED;
```

```
ERROR:  a promoted property cannot have a collation of its own
DETAIL:  Column "k" is collated "C", while a property map compares strings with the database default.
HINT:  Leave the collation unspecified, or use a type that does not carry one.
```

### A view over a Cypher query pins the column {#a-view-over-a-cypher-query-pins-the-column}

A view is compiled once, and a view over a Cypher query that resolved a property to a column
holds a dependency on that column:

```cypher
CREATE VIEW recent_films AS
SELECT title #>> '{}' AS title, year
FROM (MATCH (f:film) WHERE f.year > 2010 RETURN f.title AS title, f.year AS year) q;
```

```cypher
ALTER VLABEL film DROP COLUMN year;
```

```
ERROR:  cannot drop column year of table promolab.film because other objects depend on it
DETAIL:  view recent_films depends on column year of table promolab.film
HINT:  Use DROP ... CASCADE to drop the dependent objects too.
```

That is correct: the view would otherwise silently start reading the bag. But it means a view
is a commitment. Drop the view, drop the column, recreate the view. The dependency is visible
in `pg_get_viewdef`, which shows the lowered SQL naming `f.year`: [what a view over a Cypher
query looks like](/agensgraph/querying/combining-sql-and-cypher/#a-view-over-a-cypher-query).

```sql
DROP VIEW recent_films;
```

### An expression property index is built over the bag {#an-expression-property-index-is-built-over-the-bag}

A bare key and the same key inside an expression are resolved differently by
`CREATE PROPERTY INDEX`. A bare key becomes the promoted column. An expression over that key
becomes an expression over the jsonb bag:

```cypher
ALTER VLABEL film ADD COLUMN title text GENERATED;
CREATE PROPERTY INDEX film_title_idx ON film (title);
CREATE PROPERTY INDEX film_lower_idx ON film ((lower(title)));
```

```sql
SELECT c.relname, pg_get_indexdef(c.oid) AS real_definition
FROM pg_class c JOIN pg_index i ON i.indexrelid = c.oid
WHERE i.indrelid = 'promolab.film'::regclass AND c.relname LIKE 'film_%idx'
ORDER BY 1;
```

```
    relname     |                                   real_definition
----------------+--------------------------------------------------------------------------------------
 film_lower_idx | CREATE INDEX film_lower_idx ON promolab.film USING btree (lower(properties.'title'))
 film_title_idx | CREATE INDEX film_title_idx ON promolab.film USING btree (title)
```

A query reads the column in both cases, so it is the bare form that gives an index the query
can use.

`\dGi` reports both in Cypher form, which spells each one as `title`:

```psql
\dGi promolab.*
```

```
                                                       List of property indexes
  Graph   | LabelName |   IndexName    | Unique | Owner |                                  Indexdef
----------+-----------+----------------+--------+-------+-----------------------------------------------------------------------------
 promolab | film      | film_lower_idx | f      | agens | CREATE PROPERTY INDEX film_lower_idx ON film USING btree ((lower((title))))
 promolab | film      | film_title_idx | f      | agens | CREATE PROPERTY INDEX film_title_idx ON film USING btree (title)
```

So read `pg_get_indexdef` when you want to know which of the two a label's index is over.

There are two ways to index a promoted key. Index it bare, and the query uses the column
directly. Or, when the expression itself is what you need indexed, write it as SQL over the
column, which matches what the query reads:

```sql
CREATE INDEX film_lower_col_idx ON promolab.film (lower(title));
```

Either way, drop an expression index before promoting the key it reads, and rebuild it in one
of these two forms.

### The long form registers nothing unless it is a single key {#the-long-form-registers-nothing-unless-it-is-a-single-key}

A generated column written the long way is an ordinary generated column. It is recognised as a
promotion only when its expression is exactly one key out of the bag:
`(properties ->> 'key')::type`, or the `ag_property_text` form a dump emits. Anything derived
from more than one key, or computed, registers no mapping:

```cypher
CREATE VLABEL post;
ALTER VLABEL post ADD COLUMN body_len int GENERATED ALWAYS AS (length(properties->>'body')) STORED;
CREATE (:post {body: 'hello there'});
```

The column is there and SQL can read it:

```sql
SELECT id, body_len, properties FROM promolab.post;
```

```
 id  | body_len |       properties        
-----+----------+-------------------------
 8.1 |       11 | {"body": "hello there"}
```

Cypher cannot:

```cypher
MATCH (p:post) RETURN p.body_len AS body_len;
```

```
 body_len 
----------
 
```

`p.body_len` reads a property named `body_len`, which no post has, and there is no key such a
column could be the value of. So the column looks promoted without being promoted. Use the
`GENERATED` shorthand for a promotion, and the long form for a derived column you intend to
read from SQL only.

## Turning resolution off {#turning-resolution-off}

`enable_property_promotion` controls whether a Cypher property read resolves to a column. It
is on by default. Turned off, the same query goes back to the bag:

```cypher
SET enable_property_promotion = off;
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.year > 2010 RETURN f.title;
RESET enable_property_promotion;
```

```
                  QUERY PLAN                   
-----------------------------------------------
 Seq Scan on film f
   Filter: (properties.'year' > '2010'::jsonb)
```

and gives the same answers, because the bag still holds the value. That is the setting's
purpose: to establish whether a promotion is responsible for a plan you did not expect,
without dropping the column. It does not stop the column being maintained.

## Undoing a promotion {#undoing-a-promotion}

```cypher
ALTER VLABEL film DROP COLUMN year;
```

The column and its catalog row go, any index on it goes with it, and reads fall back to the
bag with the same results:

```cypher
MATCH (f:film) WHERE f.year > 2010 RETURN count(f) AS films;
```

```
 films 
-------
 5
```

Nothing is lost, because nothing was ever stored only in the column. The one thing to clear
first is any view that pinned it.

## When to promote {#when-to-promote}

Promote a key when all four are true:

* **Queries filter, join or order on it**, rather than merely projecting it. A key you only
  ever return gains nothing. The bag read is already the cheapest way to get it.
* **Its values are uniform.** If some rows hold a number and some a string, the `ALTER` will
  refuse, and forcing them into one type is a data change, not a tuning change.
* **You want an index over the value's own type** — a range on a real `integer`, an
  index-only `ORDER BY`, an HNSW index on a `vector`.
* **The label is big enough for the read to matter.** On 18 rows nothing here is measurable.

Do not promote a key because it appears in every vertex. Uniformity is a precondition, not a
reason. And check the two predicates that get worse, `IN` and `STARTS WITH`, against what your
application sends.

## Clean up {#clean-up}

```cypher
DROP GRAPH promolab CASCADE;
```

```sql
DROP TABLE seed_page;
DROP DOMAIN sortkey;
```

## Where to go next {#where-to-go-next}

* [Indexes and constraints](/agensgraph/querying/indexes-and-constraints/) — the sargability tables, before and
  after promotion.
* [Tuning a query](/agensgraph/querying/performance/) — where promotion sits among the other plan-shaping
  choices.
* [Vector search](/agensgraph/guides/search/vector/) — embeddings, with and without a promoted
  column.
