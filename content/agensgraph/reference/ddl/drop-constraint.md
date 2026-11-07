---
title: DROP CONSTRAINT
linkTitle: DROP CONSTRAINT
description: Removes a constraint from a label.
type: docs
weight: 110
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/ddl/drop-constraint.html
upstream_source: agensgraph
upstream_modified: true
---


Removes a constraint from a label.

## Synopsis {#synopsis}

```text
DROP CONSTRAINT constraint_name ON label_name
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`DROP CONSTRAINT` removes one constraint from one label. It takes both forms that
[`CREATE CONSTRAINT`](/agensgraph/reference/ddl/create-constraint/) creates: the exclusion constraint behind
`IS UNIQUE`, and the check constraint behind a condition. It also drops the index a unique
constraint owns.

The statement is deliberately small. These are the things it does not have:

- **The name is required.** There is no way to say "whatever constraint is on this
  property".
- **There is no `IF EXISTS`.** `DROP CONSTRAINT IF EXISTS ...` is a syntax error, so a
  constraint that is not there is always an error.
- **There is no `CASCADE` or `RESTRICT`,** and no name list.
- The name cannot be qualified, and neither can the label's. The label is looked up in the
  graph named by `graph_path`.
- It reaches any named constraint on the label's table, not only the ones Cypher created.
  The label's primary key is one of them. Read the name before you run it.
- A property index is not a constraint. Drop one with
  [`DROP PROPERTY INDEX`](/agensgraph/reference/ddl/drop-property-index/).

## Parameters {#parameters}

constraint_name
: Name of the constraint to drop. Unqualified. `\dGv`, `\dGe` and `\d` all report it; so
  does `pg_constraint`.

label_name
: Label the constraint is on, in the graph named by `graph_path`.

## Examples {#examples}

The examples build their own graph, `rulebooks`, rather than using
[the example dataset](/agensgraph/get-started/example-dataset/), and drop it at the end.

```cypher
CREATE GRAPH rulebooks;
SET graph_path = rulebooks;
CREATE VLABEL film;
CREATE CONSTRAINT film_title_uniq ON film ASSERT title IS UNIQUE;
CREATE CONSTRAINT ON film ASSERT year IS UNIQUE;
CREATE VLABEL teen;
CREATE CONSTRAINT teen_age ON teen ASSERT (10 <= age::int AND age::int <= 19);
CREATE CONSTRAINT ON teen ASSERT age > 9;
```

### Drop a unique constraint {#drop-a-unique-constraint}

```cypher
DROP CONSTRAINT film_title_uniq ON film;
```

```
DROP CONSTRAINT
```

The constraint and its index are both gone; the unnamed one created afterwards is not:

```psql
\d rulebooks.film
```

```
                                                          Table "rulebooks.film"
   Column   |  Type   | Collation | Nullable |                                           Default                                           
------------+---------+-----------+----------+---------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('rulebooks.film'::cstring), nextval('rulebooks.film_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "film_pkey" PRIMARY KEY, btree (id)
    "film_unique_constraint" EXCLUDE USING btree ((properties.'year') WITH =)
Inherits: rulebooks.ag_vertex
```

Running it a second time is an error, because there is no `IF EXISTS` to soften it:

```cypher
DROP CONSTRAINT film_title_uniq ON film;
```

```
ERROR:  constraint "film_title_uniq" of relation "film" does not exist
```

```cypher
DROP CONSTRAINT IF EXISTS film_title_uniq ON film;
```

```
ERROR:  syntax error at or near "EXISTS"
LINE 1: DROP CONSTRAINT IF EXISTS film_title_uniq ON film;
                           ^
```

### Find the name of a constraint you did not name {#find-the-name-of-a-constraint-you-did-not-name}

A constraint created without a name has a derived one. `pg_constraint` lists every
constraint on the label's table:

```sql
SELECT conname FROM pg_constraint WHERE conrelid = 'rulebooks.teen'::regclass ORDER BY conname;
```

```
         conname          
--------------------------
 teen_age
 teen_id_not_null
 teen_pkey
 teen_properties_check
 teen_properties_not_null
(5 rows)
```

`teen_age` is the named check constraint and `teen_properties_check` the derived one. The
other three belong to the label's own shape.

### Drop a check constraint {#drop-a-check-constraint}

```cypher
DROP CONSTRAINT teen_properties_check ON teen;
DROP CONSTRAINT teen_age ON teen;
```

Both are gone, and `\dGv` says so by having nothing to report:

```psql
\dGv rulebooks.teen
```

```
          List of labels
   Graph   | Name |  Type  | Owner
-----------+------+--------+-------
 rulebooks | teen | vertex | agens
(1 row)

Vertex label "rulebooks.teen"
--
Inherits: rulebooks.ag_vertex
```

### Refusals worth recognizing {#refusals-worth-recognizing}

A property index is not a constraint, whatever it is named:

```cypher
CREATE PROPERTY INDEX film_year_idx ON film (year);
DROP CONSTRAINT film_year_idx ON film;
```

```
ERROR:  constraint "film_year_idx" of relation "film" does not exist
```

And the name cannot carry the graph:

```cypher
DROP CONSTRAINT rulebooks.film_unique_constraint ON film;
```

```
ERROR:  syntax error at or near "."
LINE 1: DROP CONSTRAINT rulebooks.film_unique_constraint ON film;
                                 ^
```

Finally, drop the graph the examples built:

```cypher
DROP GRAPH rulebooks CASCADE;
```

## Notes {#notes}

> [!WARNING]
> `DROP CONSTRAINT` takes any named constraint on the label's table, and a label's primary key
> is one. `DROP CONSTRAINT film_pkey ON film` succeeds and leaves the label without its
> primary key on `id`, and no statement puts that back. Check the name
> against `\dGv` or `pg_constraint` first, and keep to the names
> [`CREATE CONSTRAINT`](/agensgraph/reference/ddl/create-constraint/) produced.

To change a constraint, drop it and create it again;
`CREATE OR REPLACE CONSTRAINT` is refused.

A check constraint that a child label inherited can only be dropped from the label that
declares it:

```cypher
CREATE GRAPH hierarchy;
SET graph_path = hierarchy;
CREATE VLABEL work;
CREATE CONSTRAINT work_y ON work ASSERT (year::int > 1900);
CREATE VLABEL feature INHERITS (work);
```

Naming the child is refused:

```cypher
DROP CONSTRAINT work_y ON feature;
```

```
ERROR:  cannot drop inherited constraint "work_y" of relation "feature"
```

Dropping it from the parent removes it from the whole family:

```cypher
DROP CONSTRAINT work_y ON work;
DROP GRAPH hierarchy CASCADE;
```

## Compatibility {#compatibility}

### ISO/IEC 39075 (GQL) {#isoiec-39075-gql}

GQL has no constraint DDL, so nothing corresponds to this statement. Its way of constraining
a graph is a graph type, dropped whole by `<drop graph type statement>` (§12.7). Graph types
are tracked as planned in the
[GQL conformance matrix](/agensgraph/appendix/gql-conformance/).

### PostgreSQL {#postgresql}

`DROP CONSTRAINT ... ON <label>` corresponds to
`ALTER TABLE <table> DROP CONSTRAINT <name>`, with the label name after the constraint name
instead of before it. It offers less: no `IF EXISTS`, no `CASCADE`/`RESTRICT`, and no way to
drop several constraints in one statement. It reaches exactly as far, though: any named
constraint on the label's table, the same set `ALTER TABLE` would reach.

## See also {#see-also}

- [`CREATE CONSTRAINT`](/agensgraph/reference/ddl/create-constraint/)
- [`DROP PROPERTY INDEX`](/agensgraph/reference/ddl/drop-property-index/)
- [`ALTER VLABEL` and `ALTER ELABEL`](/agensgraph/reference/ddl/alter-label/)
- [How a graph is stored](/agensgraph/concepts/graph-on-postgresql/#what-a-property-index-and-a-constraint-become)
