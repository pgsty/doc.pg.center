---
title: Indexes and constraints
linkTitle: Indexes and constraints
description: A property index is a PostgreSQL btree over an expression that reads one key out of a label's jsonb
  property bag.
type: docs
weight: 50
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/querying/indexes-and-constraints.html
upstream_source: agensgraph
upstream_modified: true
---


A property index is a PostgreSQL btree over an expression that reads one key out of a
label's `jsonb` property bag. That single sentence explains almost everything about when one
helps. It helps exactly when the planner can match your predicate against that expression.
It does nothing at all when it cannot.

This page determines, by experiment, which predicates qualify. The answers are not
symmetrical and several of them are surprising, so the tables below are the point of the
page. [How a graph is stored](/agensgraph/concepts/graph-on-postgresql/#what-a-property-index-and-a-constraint-become)
shows what an index looks like on disk. The full syntax is in
[`CREATE PROPERTY INDEX`](/agensgraph/reference/ddl/create-property-index/) and
[`CREATE CONSTRAINT`](/agensgraph/reference/ddl/create-constraint/).

## A graph to measure on {#a-graph-to-measure-on}

[The example dataset](/agensgraph/get-started/example-dataset/) has 18 films, which is too few for
the planner to prefer any index over reading the table. Build a bigger label to work on, and
drop it at the end of the page:

```sql
CREATE TABLE seed_film AS
SELECT 'Film ' || lpad(g::text, 6, '0') AS title,
       1900 + (g % 130) AS year,
       (ARRAY['Action','Sci-Fi','Drama','Comedy'])[1 + (g % 4)] AS genre
FROM generate_series(1, 50000) g;
```

```cypher
CREATE GRAPH idxlab;
SET graph_path = idxlab;
CREATE VLABEL film;
LOAD FROM seed_film AS r CREATE (:film {title: r.title, year: r.year, genre: r.genre});
CREATE PROPERTY INDEX ON film (title);
CREATE PROPERTY INDEX ON film (year);
```

```sql
ANALYZE idxlab.film;
```

`ANALYZE` matters as much as the index. An index the planner has no statistics for is an
index the planner will decline to use.

Every plan below is the planner's own unforced choice on 50,000 rows. Nothing is turned off
to make a point.

## What an index can serve {#what-an-index-can-serve}

Equality is the case everything else is measured against:

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.title = 'Film 000042' RETURN f.year;
```

```
                         QUERY PLAN                          
-------------------------------------------------------------
 Index Scan using film_title_idx on film f
   Index Cond: (properties.'title' = '"Film 000042"'::jsonb)
```

`Index Cond` is the word to look for. It means the predicate became a search of the index.
A predicate that appears as `Filter` instead was evaluated on rows the scan had already
fetched. That is the thing the index was supposed to avoid.

A property map in the pattern compiles to the same equality and gets the same plan:

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film {title: 'Film 000042'}) RETURN f.year;
```

```
                         QUERY PLAN                          
-------------------------------------------------------------
 Index Scan using film_title_idx on film f
   Index Cond: (properties.'title' = '"Film 000042"'::jsonb)
```

A range works, because a btree is ordered:

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.year >= 2025 AND f.year < 2030 RETURN f.title;
```

```
                                             QUERY PLAN                                             
----------------------------------------------------------------------------------------------------
 Bitmap Heap Scan on film f
   Recheck Cond: ((properties.'year' >= '2025'::jsonb) AND (properties.'year' < '2030'::jsonb))
   ->  Bitmap Index Scan on film_year_idx
         Index Cond: ((properties.'year' >= '2025'::jsonb) AND (properties.'year' < '2030'::jsonb))
```

The comparison happens in jsonb's own ordering, which orders numbers numerically, so
`>= 2025` means what you want. But jsonb sorts *types* before values: a property holding the
string `"2025"` is not between two numbers.

An `IN` list of literals becomes an array search:

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.title IN ['Film 000042', 'Film 000043'] RETURN f.year;
```

```
                                         QUERY PLAN                                          
---------------------------------------------------------------------------------------------
 Index Scan using film_title_idx on film f
   Index Cond: (properties.'title' = ANY ('{"\"Film 000042\"","\"Film 000043\""}'::jsonb[]))
```

## What an index cannot serve {#what-an-index-cannot-serve}

`<>` cannot use an index, for the ordinary reason that "not this one value" is most of the
table:

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.year <> 2020 RETURN f.title;
```

```
                   QUERY PLAN                   
------------------------------------------------
 Seq Scan on film f
   Filter: (properties.'year' <> '2020'::jsonb)
```

The string predicates are the ones that catch people, because `STARTS WITH` looks like it
should be a prefix range:

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.title STARTS WITH 'Film 00004' RETURN f.year;
```

```
                               QUERY PLAN                                
-------------------------------------------------------------------------
 Seq Scan on film f
   Filter: string_starts_with(properties.'title', '"Film 00004"'::jsonb)
```

It is not. `STARTS WITH` compiles to a function call, `string_starts_with`, and a btree over
`properties.'title'` has no operator class entry for that function. So there is no index path
at all, not merely a rejected one. Turning `enable_seqscan` off does not produce one; the
plan stays a sequential scan and is marked `Disabled: true`.

`CONTAINS`, `ENDS WITH` and `=~` behave identically, each compiling to its own function:

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.title CONTAINS '00042' RETURN f.year;
```

```
                           QUERY PLAN                            
-----------------------------------------------------------------
 Seq Scan on film f
   Filter: string_contains(properties.'title', '"00042"'::jsonb)
```

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.title =~ '^Film 00004' RETURN f.year;
```

```
                             QUERY PLAN                             
--------------------------------------------------------------------
 Seq Scan on film f
   Filter: string_regex(properties.'title', '"^Film 00004"'::jsonb)
```

`IS NULL` and `IS NOT NULL` also fall back to a scan on an unpromoted property:

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.director IS NULL RETURN f.title;
```

```
                QUERY PLAN                 
-------------------------------------------
 Seq Scan on film f
   Filter: (properties.'director' IS NULL)
```

The reason is worth understanding, because it also tells you why `IS NULL` behaves
*differently* after promotion. `properties.'director'` is null for a row whose bag has no
`director` key at all. An expression index over that key stores a null for every such row, so
the index would have to be read almost end to end.

On a promoted column the same test is a real `IS NULL` on a real column, and the btree answers
it directly.

### The table {#the-table}

Measured on 50,000 rows with `film_title_idx` on `title` and `film_year_idx` on `year`, and
with `ANALYZE` run:

| Predicate | Index used |
| --- | --- |
| `f.title = 'x'` | Yes — `Index Cond` |
| `(f:film {title: 'x'})` in the pattern | Yes — `Index Cond` |
| `f.year >= 2025 AND f.year < 2030` | Yes — `Bitmap Index Scan` |
| `f.title IN ['x', 'y']` | Yes — `Index Cond` with `= ANY` |
| `f.year <> 2020` | No — `Seq Scan` |
| `f.title STARTS WITH 'x'` | No — `string_starts_with` filter |
| `f.title CONTAINS 'x'` | No — `string_contains` filter |
| `f.title ENDS WITH 'x'` | No — `string_ends_with` filter |
| `f.title =~ '^x'` | No — `string_regex` filter |
| `f.director IS NULL` | No — `Seq Scan` |
| `f.title IS NOT NULL` | No — `Seq Scan` |
| `ORDER BY f.title LIMIT n` | Yes — `Index Scan`, no sort |

No index type rescues the string predicates for a Cypher predicate: they are function calls,
and no operator class claims them. If you need prefix or substring search, [full-text
search](/agensgraph/guides/search/full-text/) is the tool. You can also reach the column from SQL;
see [below](#what-promotion-changes).

## Ordering {#ordering}

An index serves an `ORDER BY` on the same property. So a "top N by property" query needs no
sort at all:

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) RETURN f.title AS t ORDER BY t LIMIT 5;
```

```
                   QUERY PLAN                    
-------------------------------------------------
 Limit
   ->  Index Scan using film_title_idx on film f
```

This works because a sort key is ordered as the value it is rather than as a jsonb rendering
of it. Ordering by an expression the index does not hold still sorts.

## Composite and partial indexes {#composite-and-partial-indexes}

A property index takes several keys, and the leftmost-prefix rule is PostgreSQL's:

```cypher
CREATE PROPERTY INDEX ON film (genre, year);
```

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.genre = 'Comedy' AND f.year >= 2025 RETURN f.title;
```

```
                                               QUERY PLAN                                                
---------------------------------------------------------------------------------------------------------
 Bitmap Heap Scan on film f
   Recheck Cond: ((properties.'genre' = '"Comedy"'::jsonb) AND (properties.'year' >= '2025'::jsonb))
   ->  Bitmap Index Scan on film_genre_year_idx
         Index Cond: ((properties.'genre' = '"Comedy"'::jsonb) AND (properties.'year' >= '2025'::jsonb))
```

A query on `year` alone cannot use it and goes back to the single-key index on `year`. So
order the keys equality-first, as you would in SQL.

A `WHERE` clause on the index makes it partial. That is how you index a small, hot subset of
a large label:

```cypher
CREATE PROPERTY INDEX film_comedy_year_idx ON film (year) WHERE genre = 'Comedy';
```

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.genre = 'Comedy' AND f.year >= 2025 RETURN f.title;
```

```
                                             QUERY PLAN                                              
-----------------------------------------------------------------------------------------------------
 Bitmap Heap Scan on film f
   Recheck Cond: ((properties.'year' >= '2025'::jsonb) AND (properties.'genre' = '"Comedy"'::jsonb))
   ->  Bitmap Index Scan on film_comedy_year_idx
         Index Cond: (properties.'year' >= '2025'::jsonb)
```

The `genre` test has left the index condition, because every entry in this index is a comedy
already; it survives only in the recheck. The index is a quarter of the size of the full one
on `year`: 524,288 bytes against 2,056,192. The planner picked it over both alternatives.

`CREATE PROPERTY INDEX` also takes `USING btree | hash | gin | brin | gist | spgist`,
`CONCURRENTLY`, `IF NOT EXISTS`, `INCLUDE` and a tablespace. All of them mean what they mean
in PostgreSQL.

> [!NOTE]
> Every bare name inside `CREATE PROPERTY INDEX (...)` is a *property key*, including the word
> `properties`. `CREATE PROPERTY INDEX ON film USING gin (properties)` indexes a property
> named `properties`, which no film has. To index the bag itself, use plain SQL —
> `CREATE INDEX film_bag_idx ON idxlab.film USING gin (properties)` — and note that only a SQL
> predicate such as `properties @> '{"genre": "Comedy"}'` can use it. A Cypher property read
> compiles to `properties.'genre'`, which a GIN index on the bag does not match.

## What promotion changes {#what-promotion-changes}

Promoting a property gives it a real typed column, and every predicate is then compiled
against that column instead of against the bag. [Promoting a property to a
column](/agensgraph/querying/typed-columns/) is the page for why and how. What matters here is that it changes
the answers in the table above, in both directions.

```cypher
ALTER VLABEL film ADD COLUMN year int GENERATED;
ALTER VLABEL film ADD COLUMN title text GENERATED;
```

Start with what promotion does to the indexes you already have. An index over
`properties.'year'` is matched by nothing, because no query compiles to that expression any
more:

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.year >= 2025 AND f.year < 2030 RETURN f.title;
```

```
                  QUERY PLAN                  
----------------------------------------------
 Seq Scan on film f
   Filter: ((year >= 2025) AND (year < 2030))
```

The index is still there, still being maintained on every write, and no longer used by
anything. Promotion is therefore always two steps: promote, then rebuild the index on the
column.

Rebuilding as a property index works for a bare key, which is the common case and the one
below. An *expression* over the key needs the other form. `CREATE PROPERTY INDEX` compiles a
bare key to the promoted column, but an expression over that key to the jsonb bag, which is
not what the query reads. Write that one as SQL over the column, which `\dGi` still lists:

```sql
CREATE INDEX film_lower_idx ON idxlab.film (lower(title));
```

See [An expression property index is built over the
bag](/agensgraph/querying/typed-columns/#an-expression-property-index-is-built-over-the-bag).

```cypher
DROP PROPERTY INDEX film_year_idx;
DROP PROPERTY INDEX film_title_idx;
DROP PROPERTY INDEX film_genre_year_idx;
DROP PROPERTY INDEX film_comedy_year_idx;
CREATE PROPERTY INDEX ON film (year);
CREATE PROPERTY INDEX ON film (title);
```

The label now looks like this. The new indexes are ordinary column indexes, not expression
indexes:

```psql
\d idxlab.film
```

```
                                                             Table "idxlab.film"
   Column   |  Type   | Collation | Nullable |                                            Default                                            
------------+---------+-----------+----------+-----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('idxlab.film'::cstring), nextval('idxlab.film_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
 year       | integer |           |          | generated always as (ag_property_text(properties, 'year'::text, 'n'::"char")::integer) stored
 title      | text    |           |          | generated always as (ag_property_text(properties, 'title'::text, 's'::"char")) stored
Indexes:
    "film_pkey" PRIMARY KEY, btree (id)
    "film_bag_idx" gin (properties)
    "film_title_idx" btree (title)
    "film_year_idx" btree (year)
Inherits: idxlab.ag_vertex
```

Equality and range now compare native values rather than jsonb:

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.title = 'Film 000042' RETURN f.year;
```

```
                 QUERY PLAN                  
---------------------------------------------
 Index Scan using film_title_idx on film f
   Index Cond: (title = 'Film 000042'::text)
```

`IS NULL` becomes sargable, which it was not before:

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.title IS NULL RETURN f.year;
```

```
                QUERY PLAN                 
-------------------------------------------
 Index Scan using film_title_idx on film f
   Index Cond: (title IS NULL)
```

`ORDER BY` improves from an index scan to an index-only scan, because the value the query
wants is in the index:

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) RETURN f.title AS t ORDER BY t LIMIT 5;
```

```
                      QUERY PLAN                      
------------------------------------------------------
 Limit
   ->  Index Only Scan using film_title_idx on film f
```

And two predicates get *worse*. `IN` no longer uses the index, because the column is boxed
back to jsonb to be compared against a jsonb list:

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.title IN ['Film 000042', 'Film 000043'] RETURN f.year;
```

```
                                         QUERY PLAN                                          
---------------------------------------------------------------------------------------------
 Seq Scan on film f
   Filter: (cypher_to_jsonb(title) = ANY ('{"\"Film 000042\"","\"Film 000043\""}'::jsonb[]))
```

`STARTS WITH` is boxed the same way, so promotion does not rescue it either:

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.title STARTS WITH 'Film 00004' RETURN f.year;
```

```
                                 QUERY PLAN                                  
-----------------------------------------------------------------------------
 Seq Scan on film f
   Filter: string_starts_with(cypher_to_jsonb(title), '"Film 00004"'::jsonb)
```

But the column is a real `text` column, so SQL can reach it with a real `text` operator, and
that *is* a prefix range:

```sql
EXPLAIN (COSTS OFF) SELECT count(*) FROM idxlab.film WHERE title LIKE 'Film 00004%';
```

```
                                      QUERY PLAN                                      
--------------------------------------------------------------------------------------
 Aggregate
   ->  Index Only Scan using film_title_idx on film
         Index Cond: ((title >= 'Film 00004'::text) AND (title < 'Film 00005'::text))
         Filter: (title ~~ 'Film 00004%'::text)
```

That is the practical answer for prefix search on a hot key: promote the property and write
the prefix predicate in SQL, wrapping the Cypher part if you need one. See
[Combining SQL and Cypher](/agensgraph/querying/combining-sql-and-cypher/).

### The table, after promotion {#the-table-after-promotion}

| Predicate | Unpromoted (jsonb) | Promoted (typed column) |
| --- | --- | --- |
| `f.title = 'x'` | Yes | Yes |
| `f.year >= a AND f.year < b` | Yes | Yes |
| `f.title IN ['x', 'y']` | Yes | **No** — boxed to jsonb |
| `f.year <> 2020` | No | No |
| `f.title STARTS WITH 'x'` | No | No |
| `f.title CONTAINS 'x'` | No | No |
| `f.title =~ '^x'` | No | No |
| `f.title IS NULL` | No | **Yes** |
| `ORDER BY f.title LIMIT n` | Yes — index scan | Yes — index-only scan |
| SQL `title LIKE 'x%'` | Not applicable | Yes — prefix range |

## Across a label hierarchy {#across-a-label-hierarchy}

An index belongs to one table. A pattern on a parent label scans the parent and every label
below it, and each of those needs its own index. Build a family to see it:

```sql
CREATE TABLE seed_work AS SELECT g FROM generate_series(1, 10000) g;
```

```cypher
CREATE VLABEL work;
CREATE VLABEL short INHERITS (work);
CREATE VLABEL feature INHERITS (work);
LOAD FROM seed_work AS r CREATE (:short {code: 'S' || lpad((r.g)::text, 6, '0')});
LOAD FROM seed_work AS r CREATE (:feature {code: 'F' || lpad((r.g)::text, 6, '0')});
CREATE PROPERTY INDEX ON work (code);
```

```sql
ANALYZE idxlab.work; ANALYZE idxlab.short; ANALYZE idxlab.feature;
```

Only `work` is indexed, and every child is read in full:

```cypher
EXPLAIN (COSTS OFF) MATCH (w:work) WHERE w.code = 'F000042' RETURN w;
```

```
                           QUERY PLAN                           
----------------------------------------------------------------
 Result
   ->  Append
         ->  Seq Scan on work w_1
               Filter: (properties.'code' = '"F000042"'::jsonb)
         ->  Seq Scan on short w_2
               Filter: (properties.'code' = '"F000042"'::jsonb)
         ->  Seq Scan on feature w_3
               Filter: (properties.'code' = '"F000042"'::jsonb)
```

Index each child and every branch of the `Append` gets one:

```cypher
CREATE PROPERTY INDEX ON short (code);
CREATE PROPERTY INDEX ON feature (code);
```

```
                             QUERY PLAN                             
--------------------------------------------------------------------
 Result
   ->  Append
         ->  Seq Scan on work w_1
               Filter: (properties.'code' = '"F000042"'::jsonb)
         ->  Index Scan using short_code_idx on short w_2
               Index Cond: (properties.'code' = '"F000042"'::jsonb)
         ->  Index Scan using feature_code_idx on feature w_3
               Index Cond: (properties.'code' = '"F000042"'::jsonb)
```

`work` itself keeps its sequential scan because it holds no rows of its own, and reading an
empty table is cheaper than opening an index. That is the right decision. It is also the
shape to watch for: a hierarchy costs you one index per label, forever, for every property
you search a family by.

## Constraints {#constraints}

Two forms exist, and they are the two PostgreSQL forms underneath.

`ASSERT <key> IS UNIQUE` builds an exclusion constraint over the key's expression:

```cypher
CREATE VLABEL account;
CREATE CONSTRAINT account_email_uq ON account ASSERT email IS UNIQUE;
```

```cypher
CREATE (:account {email: 'a@example.com', age: 30});
CREATE (:account {email: 'a@example.com', age: 31});
```

```
ERROR:  conflicting key value violates exclusion constraint "account_email_uq"
DETAIL:  Key ((properties.'email'))=("a@example.com") conflicts with existing key ((properties.'email'))=("a@example.com").
```

`ASSERT <predicate>` builds a check constraint:

```cypher
CREATE CONSTRAINT account_age_ck ON account ASSERT age > 0;
CREATE (:account {email: 'b@example.com', age: -1});
```

```
ERROR:  new row for relation "account" violates check constraint "account_age_ck"
DETAIL:  Failing row contains (7.3, {"age": -1, "email": "b@example.com"}).
```

Both are visible as ordinary constraints, and the unique one is backed by a real btree over
the expression, so it doubles as an index for lookups on that key:

```sql
SELECT conname, pg_get_constraintdef(oid) FROM pg_constraint
WHERE conrelid = 'idxlab.account'::regclass AND contype IN ('c', 'x') ORDER BY conname;
```

```
     conname      |               pg_get_constraintdef                
------------------+---------------------------------------------------
 account_age_ck   | CHECK ((properties.'age' > cypher_to_jsonb(0)))
 account_email_uq | EXCLUDE USING btree ((properties.'email') WITH =)
```

Neither constraint says anything about a vertex that lacks the property. A missing key reads
as null, a null is not equal to another null, and a check constraint on an unknown value
passes:

```cypher
CREATE (:account {email: 'c@example.com'});
CREATE (:account {age: 44});
CREATE (:account {age: 45});
MATCH (a:account) RETURN a.email AS email, a.age AS age ORDER BY email NULLS LAST, age;
```

```
      email      | age 
-----------------+-----
 "a@example.com" | 30
 "c@example.com" | 
                 | 44
                 | 45
```

Two accounts with no email at all coexist happily. If a key must be present as well as
unique, add a second constraint asserting that it is not null. A property bag will not do it
for you.

`CREATE UNIQUE PROPERTY INDEX` is the other way to spell uniqueness, and it produces a
unique index rather than an exclusion constraint:

```cypher
CREATE VLABEL member;
CREATE UNIQUE PROPERTY INDEX ON member (card);
CREATE (:member {card: '0001'});
CREATE (:member {card: '0001'});
```

```
ERROR:  duplicate key value violates unique constraint "member_card_idx"
DETAIL:  Key ((properties.'card'))=("0001") already exists.
```

Prefer it for a fast unique lookup. Prefer the named constraint for a rule you want to see in
`pg_constraint` and in a dump under a name you chose. Neither is inherited by a child label:
a constraint on a parent constrains only the parent's own rows.

## Practical order of work {#practical-order-of-work}

The sequence that answers most "why is this slow" questions, in order:

1. `ANALYZE` the labels involved, edge labels included. An unanalysed edge label costs more
   than a missing index; see [Tuning a query](/agensgraph/querying/performance/#statistics-on-edge-labels).
2. Index the property your pattern is *anchored* on: the one selective equality that picks
   the starting vertices. Everything downstream is a join through the edge indexes that
   already exist.
3. Check with `EXPLAIN` that the predicate arrives as `Index Cond` and not as `Filter`.
4. Only then consider promoting the property, which is the answer when the read itself is the
   cost rather than the search.

## Clean up {#clean-up}

```cypher
DROP GRAPH idxlab CASCADE;
```

```sql
DROP TABLE seed_film;
DROP TABLE seed_work;
```

## Where to go next {#where-to-go-next}

* [Promoting a property to a column](/agensgraph/querying/typed-columns/) — the other half of the story above.
* [Tuning a query](/agensgraph/querying/performance/) — plan shape, statistics and the settings that change
  them.
* [Full-text search](/agensgraph/guides/search/full-text/) — the indexable answer to substring and
  prefix matching.
