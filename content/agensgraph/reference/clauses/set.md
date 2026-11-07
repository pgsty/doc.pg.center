---
title: SET
linkTitle: SET
description: Changes the properties of vertices and edges the query has bound.
type: docs
weight: 130
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/set.html
upstream_source: agensgraph
upstream_modified: true
---


**GQL clause**

Changes the properties of vertices and edges the query has bound.

## Synopsis {#synopsis}

```text
SET { target = expression | target += expression } [, ...]
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`SET` writes properties onto elements already bound by an earlier clause. The
effect depends on what is on the left of the operator and which operator you use:

| Written as | Effect |
| --- | --- |
| `n.key = expression` | Sets one property, adding the key if it is not there. |
| `n.key = NULL` | Removes that key. |
| `n = {…}` | **Replaces** the whole property bag with the map. Keys not in the map are lost. |
| `n = other` | Replaces `n`'s bag with `other`'s. |
| `n += {…}` | **Merges** the map into the bag: listed keys are set, the rest are kept. |

- Assignments in one `SET` are separated by commas and applied left to right.
- `SET` runs once per incoming row, so a `MATCH` that finds 10 vertices updates
  10 of them.
- `SET` needs a bound variable. It cannot introduce one, and it cannot lead a
  query. It always follows a `MATCH`, a `MERGE` or another clause that binds
  something.
- `SET` may end a query. Add a [`RETURN`](/agensgraph/reference/clauses/return/) to see the result.
- `SET` writes properties only. It cannot add or change a label.
- `ON CREATE SET` and `ON MATCH SET` on a [`MERGE`](/agensgraph/reference/clauses/merge/) take this same
  assignment syntax.

## Parameters {#parameters}

target
: A property reference, `variable.key`, optionally nested as
  `variable.key.subkey`; or a bare element variable when you are replacing or
  merging the whole bag.

expression
: The value to store. Any Cypher expression: a literal, a property of another
  element, an arithmetic or `CASE` expression, a list, a map. For `+=`, and for
  `=` against a bare variable, it must be a map or another graph element.

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).
The last example undoes them.

### Set one property {#set-one-property}

```cypher
CREATE (:movie {title: 'Tenet', year: 2020, genre: 'Action'});
```

```
UPDATE 1
```

```cypher
MATCH (m:movie {title: 'Tenet'})
SET m.runtime = 150
RETURN properties(m) AS props;
```

```
                                props
---------------------------------------------------------------------
 {"year": 2020, "genre": "Action", "title": "Tenet", "runtime": 150}
(1 row)
```

`properties()` returns the whole bag, which is the easiest way to see what a
`SET` did.

### Set several properties in one clause {#set-several-properties-in-one-clause}

```cypher
MATCH (m:movie {title: 'Tenet'})
SET m.genre = 'Sci-Fi', m.runtime = 151
RETURN properties(m) AS props;
```

```
                                props
---------------------------------------------------------------------
 {"year": 2020, "genre": "Sci-Fi", "title": "Tenet", "runtime": 151}
(1 row)
```

### Remove a property with NULL {#remove-a-property-with-null}

Assigning null deletes the key rather than storing a null:

```cypher
MATCH (m:movie {title: 'Tenet'})
SET m.runtime = NULL
RETURN properties(m) AS props;
```

```
                        props
-----------------------------------------------------
 {"year": 2020, "genre": "Sci-Fi", "title": "Tenet"}
(1 row)
```

[`REMOVE`](/agensgraph/reference/clauses/remove/) says the same thing more plainly.

### Merge a map with += {#merge-a-map-with}

`+=` sets the keys the map lists and leaves the others alone:

```cypher
MATCH (m:movie {title: 'Tenet'})
SET m += {runtime: 150, imax: true}
RETURN properties(m) AS props;
```

```
                                       props
-----------------------------------------------------------------------------------
 {"imax": true, "year": 2020, "genre": "Sci-Fi", "title": "Tenet", "runtime": 150}
(1 row)
```

### Replace the whole bag with = {#replace-the-whole-bag-with}

`=` against a bare variable throws away everything not in the map. `genre`,
`runtime` and `imax` are gone:

```cypher
MATCH (m:movie {title: 'Tenet'})
SET m = {title: 'Tenet', year: 2020}
RETURN properties(m) AS props;
```

```
              props
----------------------------------
 {"year": 2020, "title": "Tenet"}
(1 row)
```

This is the difference between the two operators, and the one to be careful
about: `=` is a replacement, `+=` is an update.

### Copy one element's properties to another {#copy-one-elements-properties-to-another}

The right-hand side can be another element, which copies its whole bag:

```cypher
CREATE (:person {name: 'Stand-in'});
```

```
UPDATE 1
```

```cypher
MATCH (p:person {name: 'Stand-in'}), (k:person {name: 'Keanu Reeves'})
SET p = k
RETURN properties(p) AS props;
```

```
                 props
----------------------------------------
 {"born": 1964, "name": "Keanu Reeves"}
(1 row)
```

There are now two vertices whose `name` is `Keanu Reeves`:

```cypher
MATCH (p:person {name: 'Keanu Reeves'}) RETURN count(*) AS keanus;
```

```
 keanus
--------
 2
(1 row)
```

Copying a bag copies the identifying properties too. It does not copy edges, and
it does not merge the two vertices.

### Set a property on an edge {#set-a-property-on-an-edge}

An edge takes properties exactly as a vertex does:

```cypher
MATCH (:person {name: 'Keanu Reeves'})-[r:acted_in]->(:movie {title: 'The Matrix'})
SET r.credited = true
RETURN properties(r) AS props;
```

```
               props
-----------------------------------
 {"role": "Neo", "credited": true}
(1 row)
```

```cypher
MATCH (:person {name: 'Keanu Reeves'})-[r:acted_in]->(:movie {title: 'The Matrix'})
SET r.credited = NULL
RETURN properties(r) AS props;
```

```
      props
-----------------
 {"role": "Neo"}
(1 row)
```

The `MATCH` finds the one edge that belongs to the original Keanu Reeves, because
the copy created above has no edges.

### Empty a bag {#empty-a-bag}

An empty map removes every property, leaving the element in place:

```cypher
MATCH (m:movie {title: 'Tenet'})
SET m = {}
RETURN properties(m) AS props;
```

```
 props
-------
 {}
(1 row)
```

The vertex is now unreachable by any property. The cleanup below therefore looks
for a missing `title` rather than for `Tenet`.

### Undo the examples {#undo-the-examples}

```cypher
MATCH (m:movie) WHERE m.title IS NULL DETACH DELETE m;
MATCH (p:person) WHERE p.name = 'Keanu Reeves' AND NOT EXISTS { MATCH (p)-[]->() } DETACH DELETE p;
```

```
UPDATE 1
UPDATE 1
```

## Notes {#notes}

The default setting `allow_null_properties = off` makes `SET n.key = NULL` a
deletion. Turn it on and the key is kept with a JSON null value instead:

```cypher
SET allow_null_properties = true;
CREATE (m:movie {title: 'Tenet', year: 2020})
SET m.runtime = NULL
RETURN properties(m) AS props;
```

```
SET
                       props
---------------------------------------------------
 {"year": 2020, "title": "Tenet", "runtime": null}
(1 row)
```

```cypher
SET allow_null_properties = false;
MATCH (m:movie {title: 'Tenet'}) DETACH DELETE m;
```

```
SET
UPDATE 1
```

A stored null is not the same as an absent key: `m.runtime IS NULL` is true
either way, but the key shows up in `properties()` and in a `jsonb` key test.

## Compatibility {#compatibility}

### Setting a label (ISO/IEC 39075 §13.3) {#setting-a-label-isoiec-39075-133}

The standard's `<set label item>` adds a label to an element, written
`SET n:blockbuster` or `SET n IS blockbuster`. AgensGraph accepts neither:

```cypher
MATCH (m:movie {title: 'Inception'}) SET m:blockbuster RETURN m.title;
```

```
ERROR:  syntax error at or near ":"
LINE 1: MATCH (m:movie {title: 'Inception'}) SET m:blockbuster RETUR...
                                                  ^
```

An element's label is the table it lives in, so it is fixed when the element is
created. To move a vertex to another label, create it there and delete the
original.

## See also {#see-also}

- [`REMOVE`](/agensgraph/reference/clauses/remove/) — remove properties by name
- [`MERGE`](/agensgraph/reference/clauses/merge/) — `ON CREATE SET` and `ON MATCH SET`
- [`MATCH`](/agensgraph/reference/clauses/match/) — binding the elements a `SET` writes to
- [`DELETE`](/agensgraph/reference/clauses/delete/) — remove elements rather than properties
