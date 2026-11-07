---
title: CREATE PROPERTY INDEX
linkTitle: CREATE PROPERTY INDEX
description: Builds an index on one or more properties of a label.
type: docs
weight: 70
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/ddl/create-property-index.html
upstream_source: agensgraph
upstream_modified: true
---


Builds an index on one or more properties of a label.

## Synopsis {#synopsis}

```text
CREATE [ UNIQUE ] PROPERTY INDEX [ CONCURRENTLY ] [ [ IF NOT EXISTS ] index_name ]    ON [ ONLY ] label_name [ USING method ]    ( { property | ( expression ) } [ COLLATE collation ] [ opclass ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [, ... ] )    [ NULLS [ NOT ] DISTINCT ]    [ WITH ( storage_parameter [= value] [, ... ] ) ]    [ TABLESPACE tablespace_name ]    [ WHERE condition ]
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

There is no separate kind of index behind this statement. A property index is an ordinary
PostgreSQL index over an *expression* that reads the property out of the label's `jsonb`
bag. `CREATE PROPERTY INDEX ON movie (title)` builds a btree whose key is
`(properties.'title')`. That is how `\d` reports it, and the planner must be able to see the
predicate in that form to use the index.

That expression is the whole story of the statement's limits:

- **The indexed value is of type `jsonb`,** so the access method has to have a default
  operator class for `jsonb`. `btree` (the default), `hash` and `gin` do. `gist`, `spgist`
  and `brin` do not, and asking for one of them fails with
  `data type jsonb has no default operator class for access method "gist"`.
- **A collation cannot be applied to it.** `jsonb` carries no collation, so
  `COLLATE` on a bag read fails with `collations are not supported by type jsonb`.
- **The value can never be an included column.** `INCLUDE` is refused with
  `expressions are not supported in included columns`, and a property read is always an
  expression, so `INCLUDE` does not apply to one.

An index on a **promoted** property is different, because the value is then the column, not
the expression. `\d` reports `btree (year)` rather than `btree ((properties.'year'))`. The
access method, the operator class and the collation are limited only by the column's own
type, so `brin (year)` on an `int` column and `btree (name COLLATE "C")` on a `text` column
both work. [Promoting a property to a column](/agensgraph/querying/typed-columns/) covers when
to promote in the first place.

Three more rules:

- The label is looked up in the graph named by `graph_path`; its name cannot be qualified.
- An index on a parent label covers that label's own rows only. Child labels are not
  indexed, with or without `ONLY`. See
  [Label inheritance](/agensgraph/concepts/label-inheritance/#what-it-costs).
- `IF NOT EXISTS` needs a name to check, so it cannot be combined with an unnamed index.

## Parameters {#parameters}

UNIQUE
: Reject a row whose indexed value duplicates an existing one, checking the rows already
  there when the index is built. For a uniqueness rule expressed in Cypher's own terms, see
  [`CREATE CONSTRAINT`](/agensgraph/reference/ddl/create-constraint/).

CONCURRENTLY
: Build the index without locking out writes to the label, at the cost of a longer build and
  two table scans.

IF NOT EXISTS index_name
: Issue a notice instead of an error when a relation of that name already exists. Nothing is
  built, and nothing checks that the existing index is the one you asked for.

index_name
: Name for the index. Left out, a name is derived from the label and the indexed properties:
  `movie` and `year` give `movie_year_idx`.

ONLY
: Accepted, and without effect on an ordinary label. It suppresses recursion into
  partitions, and a label is an inheritance parent rather than a partitioned table.

label_name
: Label whose rows are indexed, in the graph named by `graph_path`.

USING method
: Index access method. Over a property read from the bag the choice is `btree` (the default),
  `hash` or `gin`. Over a promoted column, any method with a default operator class for that
  column's type.

property
: A property of the label, written the way Cypher writes it: `title`, or `name.first` for a
  key inside a nested map.

( expression )
: A parenthesised Cypher expression over the label's properties, for example `(year / 10)`.

COLLATE collation
: Collation for the indexed value. Usable only where that value is a promoted column of a
  collatable type.

opclass
: Operator class for the indexed value, for example `jsonb_path_ops` for a `gin` index.
  Operator class *parameters* are not accepted.

ASC | DESC | NULLS FIRST | NULLS LAST
: Sort order stored in the index. `ASC` and `NULLS LAST` are the defaults, and
  `NULLS FIRST` is the default under `DESC`.

NULLS [ NOT ] DISTINCT
: For a unique index, whether two nulls count as different values. `NULLS DISTINCT`, the
  default, lets an index hold many nulls.

WITH ( storage_parameter [= value] [, ...] )
: Storage parameters for the index, such as `fillfactor` for btree or `fastupdate` for gin.

TABLESPACE tablespace_name
: Tablespace for the index. Without it, `default_tablespace` decides.

WHERE condition
: Build a partial index, covering only the rows the condition accepts.

## Examples {#examples}

The examples build their own graph, `indexdemo`, rather than using
[the example dataset](/agensgraph/get-started/example-dataset/), and drop it at the end.

```cypher
CREATE GRAPH indexdemo;
SET graph_path = indexdemo;
CREATE VLABEL movie;
CREATE VLABEL person;
CREATE (:movie {title: 'Arrival', year: 2016, genre: 'Sci-Fi'}),
       (:movie {title: 'Dune', year: 2021, genre: 'Sci-Fi'}),
       (:movie {title: 'Gattaca', year: 1997, genre: 'Sci-Fi'}),
       (:movie {title: 'Sicario', year: 2015, genre: 'Thriller'}),
       (:movie {title: 'Prisoners', year: 2013, genre: 'Thriller'}),
       (:movie {title: 'Enemy', year: 2013, genre: 'Thriller'});
CREATE (:person {name: 'Denis Villeneuve'}), (:person {name: 'Roger Deakins'});
```

### Index a property {#index-a-property}

```cypher
CREATE PROPERTY INDEX movie_title_idx ON movie (title);
```

```
CREATE PROPERTY INDEX
```

That produced a btree over an expression:

```psql
\d indexdemo.movie
```

```
                                                           Table "indexdemo.movie"
   Column   |  Type   | Collation | Nullable |                                            Default                                            
------------+---------+-----------+----------+-----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('indexdemo.movie'::cstring), nextval('indexdemo.movie_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "movie_pkey" PRIMARY KEY, btree (id)
    "movie_title_idx" btree ((properties.'title'))
Inherits: indexdemo.ag_vertex
```

`\dGi` lists the same index as the statement that would recreate it:

```psql
\dGi indexdemo.*
```

```
                                                   List of property indexes
   Graph   | LabelName |    IndexName    | Unique | Owner |                              Indexdef
-----------+-----------+-----------------+--------+-------+--------------------------------------------------------------------
 indexdemo | movie     | movie_title_idx | f      | agens | CREATE PROPERTY INDEX movie_title_idx ON movie USING btree (title)
(1 row)
```

The planner matches an equality on `title` to that expression. Six vertices are far too few
for it to prefer an index scan, so the setting below makes the plan visible:

```cypher
SET enable_seqscan = off;
EXPLAIN (COSTS OFF) MATCH (m:movie {title: 'Dune'}) RETURN m.year;
```

```
                      QUERY PLAN                      
------------------------------------------------------
 Index Scan using movie_title_idx on movie m
   Index Cond: (properties.'title' = '"Dune"'::jsonb)
(2 rows)
```

```cypher
RESET enable_seqscan;
```

### Let the index name itself {#let-the-index-name-itself}

```cypher
CREATE PROPERTY INDEX ON movie (year);
```

```psql
\dGi indexdemo.movie_year_idx
```

```
                                                  List of property indexes
   Graph   | LabelName |   IndexName    | Unique | Owner |                             Indexdef
-----------+-----------+----------------+--------+-------+------------------------------------------------------------------
 indexdemo | movie     | movie_year_idx | f      | agens | CREATE PROPERTY INDEX movie_year_idx ON movie USING btree (year)
(1 row)
```

### Choose an access method {#choose-an-access-method}

`gin` and `hash` are the alternatives to btree over a property read:

```cypher
CREATE PROPERTY INDEX movie_genre_gin ON movie USING gin (genre);
CREATE PROPERTY INDEX movie_genre_hash ON movie USING hash (genre);
```

```
CREATE PROPERTY INDEX
CREATE PROPERTY INDEX
```

The other three access methods have nothing to do with AgensGraph. They have no default
operator class for `jsonb`:

```cypher
CREATE PROPERTY INDEX movie_genre_gist ON movie USING gist (genre);
```

```
ERROR:  data type jsonb has no default operator class for access method "gist"
HINT:  You must specify an operator class for the index or define a default operator class for the data type.
```

`spgist` and `brin` fail the same way.

### Reject duplicate values {#reject-duplicate-values}

```cypher
CREATE UNIQUE PROPERTY INDEX movie_title_uniq ON movie (title);
CREATE (:movie {title: 'Dune', year: 1984});
```

```
ERROR:  duplicate key value violates unique constraint "movie_title_uniq"
DETAIL:  Key ((properties.'title'))=("Dune") already exists.
```

The `Key` in that message is the index expression, which is how you tell a unique property
index apart from a unique constraint on a column.

### Index part of a label {#index-part-of-a-label}

```cypher
CREATE PROPERTY INDEX movie_recent_idx ON movie (title) WHERE (year > 2010);
```

```
CREATE PROPERTY INDEX
```

### Index several properties, and an expression {#index-several-properties-and-an-expression}

```cypher
CREATE PROPERTY INDEX movie_genre_year_idx ON movie (genre, year DESC NULLS LAST);
CREATE PROPERTY INDEX movie_decade_idx ON movie ((year / 10));
CREATE PROPERTY INDEX movie_title_ops ON movie USING gin (title jsonb_path_ops);
```

Every one of them is an expression index, and `\d` shows exactly what was built, including
the Cypher operator that the arithmetic index carries:

```psql
\d indexdemo.movie
```

```
                                                           Table "indexdemo.movie"
   Column   |  Type   | Collation | Nullable |                                            Default                                            
------------+---------+-----------+----------+-----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('indexdemo.movie'::cstring), nextval('indexdemo.movie_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "movie_pkey" PRIMARY KEY, btree (id)
    "movie_decade_idx" btree (((properties.'year') `/` cypher_to_jsonb(10)))
    "movie_genre_gin" gin ((properties.'genre'))
    "movie_genre_hash" hash ((properties.'genre'))
    "movie_genre_year_idx" btree ((properties.'genre'), (properties.'year') DESC NULLS LAST)
    "movie_recent_idx" btree ((properties.'title')) WHERE (properties.'year') > cypher_to_jsonb(2010)
    "movie_title_idx" btree ((properties.'title'))
    "movie_title_ops" gin ((properties.'title') jsonb_path_ops)
    "movie_title_uniq" UNIQUE, btree ((properties.'title'))
    "movie_year_idx" btree ((properties.'year'))
Inherits: indexdemo.ag_vertex
```

### Index a promoted property {#index-a-promoted-property}

A label whose property is promoted to a column indexes the column instead:

```cypher
CREATE VLABEL title (year int GENERATED, name text GENERATED);
CREATE (:title {name: 'Arrival', year: 2016}), (:title {name: 'Dune', year: 2021}), (:title {name: 'Gattaca', year: 1997});
CREATE PROPERTY INDEX title_year_idx ON title (year);
```

```psql
\d indexdemo.title
```

```
                                                           Table "indexdemo.title"
   Column   |  Type   | Collation | Nullable |                                            Default                                            
------------+---------+-----------+----------+-----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('indexdemo.title'::cstring), nextval('indexdemo.title_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
 year       | integer |           |          | generated always as (ag_property_text(properties, 'year'::text, 'n'::"char")::integer) stored
 name       | text    |           |          | generated always as (ag_property_text(properties, 'name'::text, 's'::"char")) stored
Indexes:
    "title_pkey" PRIMARY KEY, btree (id)
    "title_year_idx" btree (year)
Inherits: indexdemo.ag_vertex
```

`btree (year)`, not `btree ((properties.'year'))`. The plan reads the same way, comparing
integers rather than `jsonb`:

```cypher
SET enable_seqscan = off;
EXPLAIN (COSTS OFF) MATCH (t:title) WHERE t.year > 2010 RETURN t.name;
```

```
                 QUERY PLAN                 
--------------------------------------------
 Index Scan using title_year_idx on title t
   Index Cond: (year > 2010)
(2 rows)
```

```cypher
RESET enable_seqscan;
```

Because the indexed value is the column, a collation, an operator class and an access
method the column's type supports all become available:

```cypher
CREATE PROPERTY INDEX title_name_coll ON title (name COLLATE "C");
CREATE PROPERTY INDEX title_name_pat ON title (name text_pattern_ops);
CREATE PROPERTY INDEX title_year_brin ON title USING brin (year);
```

```psql
\d indexdemo.title
```

```
                                                           Table "indexdemo.title"
   Column   |  Type   | Collation | Nullable |                                            Default                                            
------------+---------+-----------+----------+-----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('indexdemo.title'::cstring), nextval('indexdemo.title_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
 year       | integer |           |          | generated always as (ag_property_text(properties, 'year'::text, 'n'::"char")::integer) stored
 name       | text    |           |          | generated always as (ag_property_text(properties, 'name'::text, 's'::"char")) stored
Indexes:
    "title_pkey" PRIMARY KEY, btree (id)
    "title_name_coll" btree (name COLLATE "C")
    "title_name_pat" btree (name text_pattern_ops)
    "title_year_brin" brin (year)
    "title_year_idx" btree (year)
Inherits: indexdemo.ag_vertex
```

None of those three is accepted over a property read from the bag.

### Refusals worth recognizing {#refusals-worth-recognizing}

`INCLUDE` cannot be used at all, promoted column or not, because a property is always
written as an expression:

```cypher
CREATE PROPERTY INDEX title_name_incl ON title (name) INCLUDE (year);
```

```
ERROR:  expressions are not supported in included columns
```

Operator class parameters are not part of the statement:

```cypher
CREATE PROPERTY INDEX movie_title_op ON movie USING gin (title jsonb_ops (fastupdate = off));
```

```
ERROR:  syntax error at or near "("
LINE 1: ...ovie_title_op ON movie USING gin (title jsonb_ops (fastupdat...
                                                             ^
```

A nested path works only where the property holds a map. `person.name` is a string here, so
reaching into it fails while the index is being built:

```cypher
CREATE PROPERTY INDEX person_first_idx ON person (name.first);
```

```
ERROR:  map or list is expected but scalar value
```

And a name already taken is reported, not replaced:

```cypher
CREATE PROPERTY INDEX IF NOT EXISTS movie_title_idx ON movie (title);
```

```
NOTICE:  relation "movie_title_idx" already exists, skipping
CREATE PROPERTY INDEX
```

Finally, drop the graph the examples built:

```cypher
DROP GRAPH indexdemo CASCADE;
```

## Notes {#notes}

`CONCURRENTLY` is accepted and does what it does for `CREATE INDEX`: it builds without
locking writes out. `ONLY` is accepted too and changes nothing on an ordinary label. An
index on a parent covers the parent's rows only either way, so a hierarchy needs one index
per label that will be scanned.

### How a promoted key resolves here {#how-a-promoted-key-resolves-here}

On a label with [promoted properties](/agensgraph/querying/typed-columns/), the two forms of
`( ... )` resolve differently:

| What you write | What is indexed |
| --- | --- |
| `( year )`, a bare key | The promoted column `year` |
| `( (lower(title)) )`, an expression | `lower(properties.'title')`, over the jsonb bag |

A query over a promoted key reads the column in both cases, so the bare form is the one that
gives the query an index to use. To index an expression over a promoted key, write it as SQL
over the column — `CREATE INDEX ON g.film (lower(title))` — which `\dGi` still lists.

`\dGi` renders its `Indexdef` column in Cypher form, so both spell the key the same way. Read
`pg_get_indexdef`, or `\d` on the label's table, to see which of the two an index is over:
there a bare promoted key reads `btree (year)` and the property form reads
`btree ((properties.'year'))`.

## Compatibility {#compatibility}

### ISO/IEC 39075 (GQL) {#isoiec-39075-gql}

GQL has no index DDL. Its catalog-modifying statements are limited to schemas, graphs and
graph types (§12). An index has no standard spelling there, so `CREATE PROPERTY INDEX` is
AgensGraph's own.

### PostgreSQL {#postgresql}

`CREATE PROPERTY INDEX` corresponds to `CREATE INDEX` on an expression, and `UNIQUE`,
`CONCURRENTLY`, `USING`, `COLLATE`, the operator class, the sort order, `NULLS [NOT]
DISTINCT`, `WITH`, `TABLESPACE` and `WHERE` all mean what they mean there.
Three differences matter. The index target is written as a Cypher property rather than a
column or a parenthesised SQL expression, so the parser builds the `properties` read for
you. `INCLUDE` and operator class parameters, which `CREATE INDEX` accepts, cannot be used.
And [`DROP PROPERTY INDEX`](/agensgraph/reference/ddl/drop-property-index/) takes only a property index, while
`DROP INDEX` takes any index of a label, a property index included.

## See also {#see-also}

- [`DROP PROPERTY INDEX`](/agensgraph/reference/ddl/drop-property-index/)
- [`REINDEX VLABEL` and `REINDEX ELABEL`](/agensgraph/reference/ddl/reindex/)
- [`CREATE CONSTRAINT`](/agensgraph/reference/ddl/create-constraint/)
- [Promoting a property to a column](/agensgraph/querying/typed-columns/)
- [How a graph is stored](/agensgraph/concepts/graph-on-postgresql/#what-a-property-index-and-a-constraint-become)
