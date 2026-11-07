---
title: CREATE CONSTRAINT
linkTitle: CREATE CONSTRAINT
description: Requires a property of a label to be unique, or requires every element of the label to satisfy a condition.
type: docs
weight: 100
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/ddl/create-constraint.html
upstream_source: agensgraph
upstream_modified: true
---


Requires a property of a label to be unique, or requires every element of the label to
satisfy a condition.

## Synopsis {#synopsis}

```text
CREATE CONSTRAINT [ constraint_name ] ON label_name ASSERT property IS UNIQUECREATE CONSTRAINT [ constraint_name ] ON label_name ASSERT condition
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

There are two forms, and they become two different things on disk.

**`ASSERT property IS UNIQUE`** becomes an exclusion constraint over the property read:
`EXCLUDE USING btree ((properties.'title') WITH =)`. A write whose value already exists is
rejected as a conflict.

**`ASSERT condition`** becomes a check constraint over the same kind of read:
`CHECK ((properties.'age')::integer > 9)`. A write whose row fails the condition is
rejected.

**The name is optional in both forms.** Left out, one is derived: `<label>_unique_constraint`
for the unique form and `<label>_properties_check` for the check form. A numeric suffix is
added if that name is taken. A name you supply has to be free in the graph's schema, because
the unique form creates an index of that name.

Other rules:

- The label is looked up in the graph named by `graph_path`; its name cannot be qualified.
- Both forms work on a vertex label and on an edge label.
- `CREATE OR REPLACE CONSTRAINT` is parsed and then refused with
  `CREATE OR REPLACE CONSTRAINT is not supported`. To change a constraint, drop it and
  create it again.
- A constraint is created over the rows already in the label, so an existing row that
  violates it makes the statement fail.
- A check constraint is a SQL check constraint, so **a missing property satisfies it.** The
  condition evaluates to unknown for an absent property, and a check constraint accepts
  unknown. Use the constraint to restrict values, not to require a key.

[How a graph is stored](/agensgraph/concepts/graph-on-postgresql/#what-a-property-index-and-a-constraint-become)
covers the on-disk mapping in one screen.

## Parameters {#parameters}

constraint_name
: Name for the constraint. Optional; a name is derived from the label and the form when you
  leave it out. For the unique form it also names the index, so it must not collide with an
  existing relation in the graph.

label_name
: Label the constraint applies to, in the graph named by `graph_path`.

property
: The property that must be unique, written the way Cypher writes it: `title`, or
  `name.first` for a key inside a nested map.

condition
: A Cypher condition over the label's properties. It is evaluated once per written element.

## Examples {#examples}

The examples build their own graph, `constrain`, rather than using
[the example dataset](/agensgraph/get-started/example-dataset/), and drop it at the end.

```cypher
CREATE GRAPH constrain;
SET graph_path = constrain;
CREATE VLABEL film;
CREATE ELABEL rated;
```

### Require a property to be unique {#require-a-property-to-be-unique}

```cypher
CREATE CONSTRAINT film_title_uniq ON film ASSERT title IS UNIQUE;
```

```
CREATE CONSTRAINT
```

That produced an exclusion constraint over the property read:

```psql
\d constrain.film
```

```
                                                          Table "constrain.film"
   Column   |  Type   | Collation | Nullable |                                           Default                                           
------------+---------+-----------+----------+---------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('constrain.film'::cstring), nextval('constrain.film_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "film_pkey" PRIMARY KEY, btree (id)
    "film_title_uniq" EXCLUDE USING btree ((properties.'title') WITH =)
Inherits: constrain.ag_vertex
```

The first write goes in:

```cypher
CREATE (:film {title: 'Arrival', year: 2016});
```

```
UPDATE 1
```

The second is rejected, and the message names the constraint and the value:

```cypher
CREATE (:film {title: 'Arrival', year: 2021});
```

```
ERROR:  conflicting key value violates exclusion constraint "film_title_uniq"
DETAIL:  Key ((properties.'title'))=("Arrival") conflicts with existing key ((properties.'title'))=("Arrival").
```

### Leave the constraint unnamed {#leave-the-constraint-unnamed}

```cypher
CREATE CONSTRAINT ON film ASSERT year IS UNIQUE;
```

`\dGv` shows both constraints in the terms they were written in, and the derived name the
second one was given:

```psql
\dGv constrain.film
```

```
          List of labels
   Graph   | Name |  Type  | Owner
-----------+------+--------+-------
 constrain | film | vertex | agens
(1 row)

Vertex label "constrain.film"
--
Constraints:
    "film_title_uniq" ASSERT (title) IS UNIQUE
    "film_unique_constraint" ASSERT (year) IS UNIQUE
Inherits: constrain.ag_vertex
```

### Restrict what a property may hold {#restrict-what-a-property-may-hold}

```cypher
CREATE VLABEL teen;
CREATE CONSTRAINT teen_age ON teen ASSERT (10 <= age::int AND age::int <= 19);
```

```psql
\d constrain.teen
```

```
                                                          Table "constrain.teen"
   Column   |  Type   | Collation | Nullable |                                           Default                                           
------------+---------+-----------+----------+---------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('constrain.teen'::cstring), nextval('constrain.teen_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "teen_pkey" PRIMARY KEY, btree (id)
Check constraints:
    "teen_age" CHECK (10 <= ((properties.'age')::integer) AND ((properties.'age')::integer) <= 19)
Inherits: constrain.ag_vertex
```

A row inside the range is written:

```cypher
CREATE (:teen {name: 'Kim', age: 15});
```

```
UPDATE 1
```

One outside it is not:

```cypher
CREATE (:teen {name: 'Lee', age: 20});
```

```
ERROR:  new row for relation "teen" violates check constraint "teen_age"
DETAIL:  Failing row contains (5.2, {"age": 20, "name": "Lee"}).
```

A vertex with **no** `age` at all is accepted, because the condition is unknown rather than
false:

```cypher
CREATE (:teen {name: 'Bo'});
MATCH (t:teen) RETURN t.name AS name, t.age AS age ORDER BY name;
```

```
 name  | age 
-------+-----
 "Bo"  | 
 "Kim" | 15
(2 rows)
```

### Compare without a cast {#compare-without-a-cast}

Writing the comparison against the raw property compares `jsonb` values instead of
integers:

```cypher
CREATE CONSTRAINT ON teen ASSERT age > 9;
```

```psql
\dGv constrain.teen
```

```
          List of labels
   Graph   | Name |  Type  | Owner
-----------+------+--------+-------
 constrain | teen | vertex | agens
(1 row)

Vertex label "constrain.teen"
--
Constraints:
    "teen_age" ASSERT (10 <= ((age)::integer) AND ((age)::integer) <= 19)
    "teen_properties_check" ASSERT ((age) > cypher_to_jsonb(9))
Inherits: constrain.ag_vertex
```

Both forms reject `{age: 'twelve'}`, but they report it differently. The cast form raises
`invalid input syntax for type integer: "twelve"`. The uncast form reports a violated check
constraint. Cast when you want the property's type enforced as well as its range.

### Constrain an edge label {#constrain-an-edge-label}

```cypher
CREATE CONSTRAINT rated_pair ON rated ASSERT source IS UNIQUE;
```

```psql
\d constrain.rated
```

```
                                                           Table "constrain.rated"
   Column   |  Type   | Collation | Nullable |                                            Default                                            
------------+---------+-----------+----------+-----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('constrain.rated'::cstring), nextval('constrain.rated_id_seq'::regclass))
 start      | graphid |           | not null | 
 end        | graphid |           | not null | 
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "rated_end_idx" btree ("end", start)
    "rated_id_idx" brin (id)
    "rated_pair" EXCLUDE USING btree ((properties.'source') WITH =)
    "rated_start_idx" btree (start, "end")
Inherits: constrain.ag_edge
```

The constraint sits beside the label's three ordinary indexes.

### Add a constraint to a label that already has rows {#add-a-constraint-to-a-label-that-already-has-rows}

The constraint is checked against what is there, so it cannot be created over rows that
break it. The two forms report that differently:

```cypher
CREATE VLABEL rerun;
CREATE (:rerun {title: 'Arrival'}), (:rerun {title: 'Arrival'});
CREATE CONSTRAINT rerun_t ON rerun ASSERT title IS UNIQUE;
```

```
ERROR:  could not create exclusion constraint "rerun_t"
DETAIL:  Key ((properties.'title'))=("Arrival") conflicts with key ((properties.'title'))=("Arrival").
```

```cypher
CREATE VLABEL adult;
CREATE (:adult {age: 40});
CREATE CONSTRAINT adult_a ON adult ASSERT (age::int < 20);
```

```
ERROR:  check constraint "adult_a" of relation "adult" is violated by some row
```

### Refusals worth recognizing {#refusals-worth-recognizing}

There is no replace:

```cypher
CREATE OR REPLACE CONSTRAINT film_title_uniq ON film ASSERT title IS UNIQUE;
```

```
ERROR:  CREATE OR REPLACE CONSTRAINT is not supported
```

A unique constraint's name is an index name, so it collides with one:

```cypher
CREATE CONSTRAINT film_title_uniq ON film ASSERT year IS UNIQUE;
```

```
ERROR:  relation "film_title_uniq" already exists
```

And the label has to exist. Cypher does not create one here the way `CREATE (:film)` does:

```cypher
CREATE CONSTRAINT c ON nosuch ASSERT a IS UNIQUE;
```

```
ERROR:  label "nosuch" does not exist
```

Finally, drop the graph the examples built:

```cypher
DROP GRAPH constrain CASCADE;
```

## Notes {#notes}

A unique constraint is an exclusion constraint, not a unique index, so it is not
interchangeable with `CREATE UNIQUE PROPERTY INDEX`. Both reject a duplicate. The error
differs: `conflicting key value violates exclusion constraint` against
`duplicate key value violates unique constraint`. What `\dGv` reports differs. And so does
the statement that removes it: a constraint is dropped by
[`DROP CONSTRAINT`](/agensgraph/reference/ddl/drop-constraint/), a unique index by
[`DROP PROPERTY INDEX`](/agensgraph/reference/ddl/drop-property-index/).

The two forms differ over
[label inheritance](/agensgraph/concepts/label-inheritance/), and the difference catches people
out. A check constraint is inherited: a child label created after it carries the constraint
and is checked by it. A unique constraint is not. A child label gets no exclusion
constraint, so the same value can be written once through the parent and once through the
child. `MATCH` on the parent then returns both.

> [!NOTE]
> To make a property unique across a hierarchy, create the constraint on each label in it.
> There is nothing that makes one value unique across several labels; a constraint, like the
> index behind it, covers one table.

## Compatibility {#compatibility}

### ISO/IEC 39075 (GQL) {#isoiec-39075-gql}

GQL has no constraint DDL. It constrains a graph with a graph type
(`<create graph type statement>`, §12.6), which declares which labels and properties a
graph's elements may have. A graph type has no per-property uniqueness rule and no check
condition. And a graph is only constrained at all if it references a graph type.
AgensGraph's graphs are open, so `CREATE CONSTRAINT` is its own. Graph types are tracked as
planned in the [GQL conformance matrix](/agensgraph/appendix/gql-conformance/).

### PostgreSQL {#postgresql}

The check form corresponds to `ALTER TABLE ... ADD CONSTRAINT ... CHECK`, and the unique
form to `ALTER TABLE ... ADD CONSTRAINT ... EXCLUDE USING btree (... WITH =)`. It does not
correspond to `UNIQUE`, which cannot be written over an expression. The condition is a
Cypher expression rather than a SQL one, so `age` means the property, not a column.
`NOT NULL`, `PRIMARY KEY`, `FOREIGN KEY`, `DEFERRABLE` and `NOT VALID`, which
`ADD CONSTRAINT` offers, have no spelling here.

## See also {#see-also}

- [`DROP CONSTRAINT`](/agensgraph/reference/ddl/drop-constraint/)
- [`CREATE PROPERTY INDEX`](/agensgraph/reference/ddl/create-property-index/)
- [`CREATE VLABEL`](/agensgraph/reference/ddl/create-vlabel/)
- [How a graph is stored](/agensgraph/concepts/graph-on-postgresql/#what-a-property-index-and-a-constraint-become)
