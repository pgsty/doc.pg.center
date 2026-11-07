---
title: DROP PROPERTY INDEX
linkTitle: DROP PROPERTY INDEX
description: Removes a property index.
type: docs
weight: 80
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/ddl/drop-property-index.html
upstream_source: agensgraph
upstream_modified: true
---


Removes a property index.

## Synopsis {#synopsis}

```text
DROP PROPERTY INDEX [ IF EXISTS ] index_name [, ... ] [ CASCADE | RESTRICT ]
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`DROP PROPERTY INDEX` drops one or more indexes created by
[`CREATE PROPERTY INDEX`](/agensgraph/reference/ddl/create-property-index/), and nothing else.

- The name is resolved in the graph named by `graph_path`, and **cannot be qualified**. A
  name with a schema on it is rejected with `improper property index name`. To drop an index
  in another graph, change `graph_path` first.
- Only a property index is accepted. Any other index on the label is refused with
  `"<name>" is not property index`: its primary key, an edge label's endpoint indexes, an
  index created with SQL.
- `DROP INDEX`, by contrast, takes any index of a label, a property index included, so an
  index made by either statement can be dropped by either.
- An index that belongs to a constraint is dropped with the constraint, by
  [`DROP CONSTRAINT`](/agensgraph/reference/ddl/drop-constraint/).

## Parameters {#parameters}

IF EXISTS
: Issue a notice instead of an error for an index that does not exist. Other names in the
  same statement are still dropped.

index_name
: Unqualified name of the property index to drop. Several names may be given, separated by
  commas, and they need not be on the same label.

CASCADE
: Drop the objects that depend on the index.

RESTRICT
: Refuse if anything depends on the index. This is the default. An index rarely has
  dependents, so the two behave alike most of the time.

## Examples {#examples}

The examples build their own graph, `unindexed`, rather than using
[the example dataset](/agensgraph/get-started/example-dataset/), and drop it at the end.

```cypher
CREATE GRAPH unindexed;
SET graph_path = unindexed;
CREATE VLABEL movie;
CREATE VLABEL person;
CREATE (:movie {title: 'Arrival', year: 2016}), (:person {name: 'Denis Villeneuve'});
CREATE PROPERTY INDEX movie_title_idx ON movie (title);
CREATE PROPERTY INDEX movie_year_idx ON movie (year);
CREATE PROPERTY INDEX person_name_idx ON person (name);
```

```psql
\dGi unindexed.*
```

```
                                                   List of property indexes
   Graph   | LabelName |    IndexName    | Unique | Owner |                              Indexdef
-----------+-----------+-----------------+--------+-------+--------------------------------------------------------------------
 unindexed | movie     | movie_title_idx | f      | agens | CREATE PROPERTY INDEX movie_title_idx ON movie USING btree (title)
 unindexed | movie     | movie_year_idx  | f      | agens | CREATE PROPERTY INDEX movie_year_idx ON movie USING btree (year)
 unindexed | person    | person_name_idx | f      | agens | CREATE PROPERTY INDEX person_name_idx ON person USING btree (name)
(3 rows)
```

### Drop one index {#drop-one-index}

```cypher
DROP PROPERTY INDEX movie_title_idx;
```

```
DROP PROPERTY INDEX
```

A second attempt is an error, because the index is gone:

```cypher
DROP PROPERTY INDEX movie_title_idx;
```

```
ERROR:  index "movie_title_idx" does not exist
```

`IF EXISTS` turns that into a notice:

```cypher
DROP PROPERTY INDEX IF EXISTS movie_title_idx;
```

```
NOTICE:  index "movie_title_idx" does not exist, skipping
DROP PROPERTY INDEX
```

### Drop several indexes at once {#drop-several-indexes-at-once}

The names need not belong to the same label:

```cypher
DROP PROPERTY INDEX movie_year_idx, person_name_idx;
```

```
DROP PROPERTY INDEX
```

```psql
\dGi unindexed.*
```

```
No matching property indexes found.
```

### Refusals worth recognizing {#refusals-worth-recognizing}

The name cannot carry the graph:

```cypher
CREATE PROPERTY INDEX movie_title_idx ON movie (title);
DROP PROPERTY INDEX unindexed.movie_title_idx;
```

```
ERROR:  improper property index name
```

An index the statement does not own is refused. A label's primary key is one:

```cypher
DROP PROPERTY INDEX movie_pkey;
```

```
ERROR:  "movie_pkey" is not property index
```

`DROP INDEX` takes a property index as well, under its schema-qualified name:

```sql
DROP INDEX unindexed.movie_title_idx;
```

```
DROP INDEX
```

Finally, drop the graph the examples built:

```cypher
DROP GRAPH unindexed CASCADE;
```

## Notes {#notes}

Because the name is resolved in `graph_path`, an index that exists in another graph reads as
missing rather than as belonging to someone else:

```cypher
CREATE GRAPH oneplace;
SET graph_path = oneplace;
CREATE VLABEL movie;
CREATE PROPERTY INDEX movie_title_idx ON movie (title);
CREATE GRAPH otherplace;
SET graph_path = otherplace;
DROP PROPERTY INDEX movie_title_idx;
```

```
ERROR:  index "movie_title_idx" does not exist
```

Two graphs may hold indexes of the same name, so check `\dGi` before assuming which one a
bare name will reach.

```cypher
DROP GRAPH oneplace CASCADE;
DROP GRAPH otherplace CASCADE;
```

To turn a label's indexes off without dropping them, for a bulk load say, use
`ALTER VLABEL ... DISABLE INDEX` and [`REINDEX VLABEL`](/agensgraph/reference/ddl/reindex/) instead. That keeps the
definitions and only invalidates them.

## Compatibility {#compatibility}

### ISO/IEC 39075 (GQL) {#isoiec-39075-gql}

GQL has no index DDL. Its catalog-modifying statements are limited to schemas, graphs and
graph types (§12), so `DROP PROPERTY INDEX` is AgensGraph's own.

### PostgreSQL {#postgresql}

`DROP PROPERTY INDEX` corresponds to `DROP INDEX`, and `IF EXISTS`, the name list and
`CASCADE`/`RESTRICT` behave as they do there. It differs in three ways. The name is resolved
in `graph_path` rather than `search_path` and may not be schema-qualified. `CONCURRENTLY` is
not accepted. And the two statements are strictly partitioned: each refuses the other's
indexes, so a property index can only be dropped by this statement.

## See also {#see-also}

- [`CREATE PROPERTY INDEX`](/agensgraph/reference/ddl/create-property-index/)
- [`REINDEX VLABEL` and `REINDEX ELABEL`](/agensgraph/reference/ddl/reindex/)
- [`DROP CONSTRAINT`](/agensgraph/reference/ddl/drop-constraint/)
- [How a graph is stored](/agensgraph/concepts/graph-on-postgresql/#what-a-property-index-and-a-constraint-become)
