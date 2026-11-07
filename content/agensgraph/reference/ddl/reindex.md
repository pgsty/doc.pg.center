---
title: REINDEX VLABEL and REINDEX ELABEL
linkTitle: REINDEX VLABEL and REINDEX ELABEL
description: Rebuilds every index on a label, which is also how a label whose indexes were disabled gets them back.
type: docs
weight: 90
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/ddl/reindex.html
upstream_source: agensgraph
upstream_modified: true
---


Rebuilds every index on a label, which is also how a label whose indexes were disabled gets
them back.

## Synopsis {#synopsis}

```text
REINDEX [ ( option [, ... ] ) ] VLABEL label_nameREINDEX [ ( option [, ... ] ) ] ELABEL label_namewhere option is one of:    CONCURRENTLY [ boolean ]    TABLESPACE new_tablespace    VERBOSE [ boolean ]
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`REINDEX VLABEL` rebuilds every index on a vertex label and `REINDEX ELABEL` every index on
an edge label. That covers the label's own indexes, every property index on it, and the
index on its TOAST relation. Rebuilding marks an invalid index valid again, which makes this
statement the counterpart to `DISABLE INDEX`.

There is no `ENABLE INDEX`. The load-then-build sequence is
`ALTER VLABEL <label> DISABLE INDEX`, then the load, then `REINDEX VLABEL <label>`.

- The label is looked up in the graph named by `graph_path`. The name **cannot be
  qualified**: `REINDEX VLABEL rebuildme.movie` is a syntax error.
- Each statement takes one kind of label. `REINDEX VLABEL` on an edge label fails with
  `REINDEX VLABEL cannot REINDEX edge label`, and the reverse with the matching message.
- Options go in parentheses before the label keyword. `REINDEX VLABEL CONCURRENTLY movie`
  is a syntax error here, though `REINDEX TABLE` accepts that bare-keyword spelling.
- The old spelling `REINDEX LABEL` does not exist. It is a syntax error at `LABEL`.

## Parameters {#parameters}

option
: `CONCURRENTLY`, `TABLESPACE` or `VERBOSE`, in parentheses and separated by commas. They
  mean what they mean for `REINDEX`: build without locking writes out, move the rebuilt
  indexes to another tablespace, and report each index as it is finished. `CONCURRENTLY` and
  `VERBOSE` also accept an explicit boolean, so `(VERBOSE false)` is the same as leaving
  `VERBOSE` out.

label_name
: Label whose indexes are rebuilt, in the graph named by `graph_path`.

## Examples {#examples}

The examples build their own graph, `rebuildme`, rather than using
[the example dataset](/agensgraph/get-started/example-dataset/), and drop it at the end.

```cypher
CREATE GRAPH rebuildme;
SET graph_path = rebuildme;
CREATE VLABEL movie;
CREATE ELABEL directed;
CREATE PROPERTY INDEX movie_title_idx ON movie (title);
CREATE (:movie {title: 'Arrival'});
```

### Build a label's indexes after a bulk load {#build-a-labels-indexes-after-a-bulk-load}

Turning the indexes off leaves them in place but invalid, so the load does not maintain
them:

```cypher
ALTER VLABEL movie DISABLE INDEX;
```

```psql
\d rebuildme.movie
```

```
                                                           Table "rebuildme.movie"
   Column   |  Type   | Collation | Nullable |                                            Default                                            
------------+---------+-----------+----------+-----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('rebuildme.movie'::cstring), nextval('rebuildme.movie_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "movie_pkey" PRIMARY KEY, btree (id) INVALID
    "movie_title_idx" btree ((properties.'title')) INVALID
Inherits: rebuildme.ag_vertex
```

Both indexes are marked `INVALID`: the label's primary key and the property index alike.
One statement builds them:

```cypher
REINDEX VLABEL movie;
```

```
REINDEX
```

```psql
\d rebuildme.movie
```

```
                                                           Table "rebuildme.movie"
   Column   |  Type   | Collation | Nullable |                                            Default                                            
------------+---------+-----------+----------+-----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('rebuildme.movie'::cstring), nextval('rebuildme.movie_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "movie_pkey" PRIMARY KEY, btree (id)
    "movie_title_idx" btree ((properties.'title'))
Inherits: rebuildme.ag_vertex
```

### Watch each index as it is rebuilt {#watch-each-index-as-it-is-rebuilt}

```cypher
ALTER ELABEL directed DISABLE INDEX;
REINDEX (VERBOSE) ELABEL directed;
```

```
INFO:  index "pg_toast_60285_index" was reindexed
DETAIL:  CPU: user: 0.00 s, system: 0.00 s, elapsed: 0.00 s
INFO:  index "directed_id_idx" was reindexed
DETAIL:  CPU: user: 0.00 s, system: 0.00 s, elapsed: 0.00 s
INFO:  index "directed_start_idx" was reindexed
DETAIL:  CPU: user: 0.00 s, system: 0.00 s, elapsed: 0.00 s
INFO:  index "directed_end_idx" was reindexed
DETAIL:  CPU: user: 0.00 s, system: 0.00 s, elapsed: 0.00 s
REINDEX
```

An edge label's three indexes are all rebuilt, and so is the index on the TOAST relation
that holds oversized property maps. The TOAST index name carries the table's OID, so it
differs from run to run.

### Rebuild without locking writes out {#rebuild-without-locking-writes-out}

```cypher
REINDEX (CONCURRENTLY) VLABEL movie;
```

```
REINDEX
```

```cypher
REINDEX (TABLESPACE pg_default) VLABEL movie;
```

```
REINDEX
```

### Refusals worth recognizing {#refusals-worth-recognizing}

Each statement takes one kind of label:

```cypher
REINDEX VLABEL directed;
```

```
ERROR:  REINDEX VLABEL cannot REINDEX edge label
```

```cypher
REINDEX ELABEL movie;
```

```
ERROR:  REINDEX ELABEL cannot REINDEX vertex label
```

There is no `REINDEX LABEL`:

```cypher
REINDEX LABEL movie;
```

```
ERROR:  syntax error at or near "LABEL"
LINE 1: REINDEX LABEL movie;
                ^
```

The name cannot carry the graph:

```cypher
REINDEX VLABEL rebuildme.movie;
```

```
ERROR:  syntax error at or near "."
LINE 1: REINDEX VLABEL rebuildme.movie;
                                ^
```

And `CONCURRENTLY` belongs inside the parentheses:

```cypher
REINDEX VLABEL CONCURRENTLY movie;
```

```
ERROR:  syntax error at or near "CONCURRENTLY"
LINE 1: REINDEX VLABEL CONCURRENTLY movie;
                       ^
```

A label that is not there is reported by its qualified name, because `graph_path` has
already been applied to it:

```cypher
REINDEX VLABEL nosuch;
```

```
ERROR:  relation "rebuildme.nosuch" does not exist
```

Finally, drop the graph the examples built:

```cypher
DROP GRAPH rebuildme CASCADE;
```

## Notes {#notes}

`REINDEX TABLE` on a label's table does the same job and needs no setting to do it, so
`REINDEX TABLE rebuildme.movie` also brings a disabled label's indexes back. Prefer the
label spellings anyway. They check that the label is of the kind you named, and they take a
name resolved in `graph_path` rather than a schema-qualified one.

`REINDEX SCHEMA` on a graph's schema rebuilds every index in the graph, and `REINDEX INDEX`
rebuilds one by name. Both are the ordinary SQL statements, with no label-aware form.

## Compatibility {#compatibility}

### ISO/IEC 39075 (GQL) {#isoiec-39075-gql}

GQL has no index DDL and nothing that rebuilds one. Its catalog-modifying statements are
limited to schemas, graphs and graph types (§12), so these two spellings are AgensGraph's
own.

### PostgreSQL {#postgresql}

`REINDEX VLABEL` and `REINDEX ELABEL` are `REINDEX TABLE` with a label-aware target. The
options are `REINDEX`'s own options and mean the same things. Two spelling differences
matter. The target name is resolved in `graph_path` and cannot be schema-qualified. And
`CONCURRENTLY` is only accepted as a parenthesised option, never as a bare keyword after the
label keyword.

## See also {#see-also}

- [`ALTER VLABEL` and `ALTER ELABEL`](/agensgraph/reference/ddl/alter-label/)
- [`CREATE PROPERTY INDEX`](/agensgraph/reference/ddl/create-property-index/)
- [`DROP PROPERTY INDEX`](/agensgraph/reference/ddl/drop-property-index/)
- [`CREATE VLABEL`](/agensgraph/reference/ddl/create-vlabel/)
