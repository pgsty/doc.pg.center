---
title: LOAD FROM
linkTitle: LOAD FROM
description: Reads an ordinary table or view into a Cypher pipeline, one working row per table row.
type: docs
weight: 40
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/load-from.html
upstream_source: agensgraph
upstream_modified: true
---


Reads an ordinary table or view into a Cypher pipeline, one working row per table
row.

## Synopsis {#synopsis}

```text
LOAD FROM table_name AS alias
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`LOAD FROM` is the relational source clause. It scans a table and binds each row
to *alias*, whose columns are then readable as `alias.column` anywhere later in
the pipeline. Because a graph and a table live in the same database, this needs
no import step and no foreign-data wrapper.

- The alias's columns keep their **SQL types**. `r.score` on a `numeric(3,1)`
  column is a numeric, so `r.score > 8.5` is a numeric comparison, not a jsonb
  one.
- The alias itself is a **row value**. Projecting it gives the row as a jsonb
  object, so `CREATE (:label = to_jsonb(alias))` is a whole-row load.
- `LOAD FROM` may **lead** a query or follow another clause, and several may
  appear in one query. It never ends one.
- The clause has **no `WHERE` of its own**. Filter with a following
  [`MATCH`](/agensgraph/reference/clauses/match/) `WHERE`, a [`WITH`](/agensgraph/reference/clauses/with/) `WHERE`, or a
  [`FILTER`](/agensgraph/reference/clauses/filter/).
- Anything a `SELECT` can read works: a table, a view, a schema-qualified name.

## Parameters {#parameters}

table_name
: Name of the table or view to read, optionally schema-qualified. It must exist
  and be readable; an unknown name raises `relation "..." does not exist`.

alias
: Name bound to each row. Read a column as `alias.column`, and the whole row as
  `alias`.

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/),
which includes the ordinary table `rating`.

### Read a table {#read-a-table}

```cypher
LOAD FROM rating AS r
RETURN r.title AS title, r.source AS source, r.score AS score
ORDER BY title, source
LIMIT 4;
```

```
        title        |  source   | score
---------------------+-----------+-------
 "Avatar"            | "critics" | 7.9
 "Blade Runner"      | "critics" | 8.1
 "Blade Runner 2049" | "critics" | 8.0
 "Elysium"           | "critics" | 6.6
(4 rows)
```

The values are quoted because a Cypher `RETURN` boxes its output columns to
jsonb, not because the columns are jsonb. Their SQL types are unchanged:

```cypher
LOAD FROM rating AS r RETURN pg_typeof(r.score) AS t LIMIT 1;
```

```
     t
-----------
 "numeric"
(1 row)
```

### Join a table to the graph {#join-a-table-to-the-graph}

Load the table, then match against it. The relational column and the graph
property are compared directly:

```cypher
LOAD FROM rating AS r
MATCH (m:movie {title: r.title})
WHERE r.source = 'critics' AND r.score > 8.5
RETURN m.title AS film, m.year AS year, r.score AS score
ORDER BY score DESC;
```

```
             film             | year | score
------------------------------+------+-------
 "Inception"                  | 2010 | 8.8
 "The Matrix"                 | 1999 | 8.7
 "Interstellar"               | 2014 | 8.7
 "Terminator 2: Judgment Day" | 1991 | 8.6
(4 rows)
```

### Read a whole row {#read-a-whole-row}

Project the alias by itself to get the row as a map:

```cypher
LOAD FROM rating AS r RETURN r LIMIT 2;
```

```
                              r
-------------------------------------------------------------
 {"score": 8.7, "title": "The Matrix", "source": "critics"}
 {"score": 9.1, "title": "The Matrix", "source": "audience"}
(2 rows)
```

### Read a view {#read-a-view}

Any relation a `SELECT` can read is a valid source:

```cypher
CREATE VIEW critic AS SELECT title, score FROM rating WHERE source = 'critics';
```

```
CREATE VIEW
```

```cypher
LOAD FROM critic AS c
RETURN c.title AS film, c.score AS score
ORDER BY score DESC
LIMIT 3;
```

```
      film      | score
----------------+-------
 "Inception"    | 8.8
 "Interstellar" | 8.7
 "The Matrix"   | 8.7
(3 rows)
```

```cypher
DROP VIEW critic;
```

```
DROP VIEW
```

### Build vertices from table rows {#build-vertices-from-table-rows}

Name the properties you want:

```cypher
CREATE TABLE tmp_people (name text, born int);
INSERT INTO tmp_people VALUES ('Ana Lily Amirpour', 1980), ('Rian Johnson', 1973);
```

```
CREATE TABLE
INSERT 0 2
```

```cypher
LOAD FROM tmp_people AS t
CREATE (:person {name: t.name, born: t.born});
```

```
UPDATE 2
```

Or take the whole row as the property map, using `= expression` in place of a map
literal:

```cypher
LOAD FROM tmp_people AS t
CREATE (:person = to_jsonb(t));
```

```
UPDATE 2
```

Undo both loads and drop the table:

```cypher
MATCH (p:person) WHERE p.name IN ['Ana Lily Amirpour', 'Rian Johnson'] DETACH DELETE p;
```

```
UPDATE 4
```

```cypher
DROP TABLE tmp_people;
```

```
DROP TABLE
```

## Notes {#notes}

`LOAD FROM` reads. It has no bulk-load machinery of its own, no parallel writer
and no error routing. The `CREATE` that follows it inserts row by row through the
graph write path. For loading a large table, and for the index and logging
settings that make it faster, see
[loading data](/agensgraph/guides/loading-data/).

## See also {#see-also}

- [`CREATE`](/agensgraph/reference/clauses/create/) — the clause that turns loaded rows into vertices and edges
- [`MATCH`](/agensgraph/reference/clauses/match/) — joining loaded rows to the graph
- [`WITH`](/agensgraph/reference/clauses/with/) — filtering and aggregating loaded rows
- [Combining SQL and Cypher](/agensgraph/querying/combining-sql-and-cypher/) — the other direction, a Cypher query inside SQL
- [Loading data](/agensgraph/guides/loading-data/) — the practical loading guide
