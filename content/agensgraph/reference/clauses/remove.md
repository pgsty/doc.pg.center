---
title: REMOVE
linkTitle: REMOVE
description: Deletes properties from vertices and edges the query has bound.
type: docs
weight: 140
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/remove.html
upstream_source: agensgraph
upstream_modified: true
---


**GQL clause**

Deletes properties from vertices and edges the query has bound.

## Synopsis {#synopsis}

```text
REMOVE property_reference [, property_reference ] ...
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`REMOVE` takes property references and deletes those keys. It is the plain
spelling of `SET n.key = NULL`, and does exactly the same thing.

- Removing a key that is **not there** is not an error. The element is left as it
  was.
- Several references may be listed, separated by commas.
- A reference may be **nested**. `n.key.subkey` removes the inner key and leaves
  the outer map.
- `REMOVE` runs once per incoming row, so a `MATCH` that finds many elements
  strips them all. There is no `WHERE` on the clause itself; filter in the
  `MATCH`.
- `REMOVE` needs a bound variable and cannot lead a query. It may end one; add a
  [`RETURN`](/agensgraph/reference/clauses/return/) to see the result.
- `REMOVE` removes properties only. It cannot remove a label, and it cannot
  remove an element. Removing an element is [`DELETE`](/agensgraph/reference/clauses/delete/).

## Parameters {#parameters}

property_reference
: A property of a bound element, `variable.key`, optionally nested as
  `variable.key.subkey`. A bare element variable is rejected.

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).
The last example undoes them.

### Remove one property {#remove-one-property}

```cypher
CREATE (:movie {title: 'Tenet', year: 2020, genre: 'Action', runtime: 150, imax: true});
```

```
UPDATE 1
```

```cypher
MATCH (m:movie {title: 'Tenet'})
REMOVE m.runtime
RETURN properties(m) AS props;
```

```
                               props
-------------------------------------------------------------------
 {"imax": true, "year": 2020, "genre": "Action", "title": "Tenet"}
(1 row)
```

### Remove several at once {#remove-several-at-once}

```cypher
MATCH (m:movie {title: 'Tenet'})
REMOVE m.imax, m.genre
RETURN properties(m) AS props;
```

```
              props
----------------------------------
 {"year": 2020, "title": "Tenet"}
(1 row)
```

### Remove a key that is not there {#remove-a-key-that-is-not-there}

Nothing happens, and nothing complains:

```cypher
MATCH (m:movie {title: 'Tenet'})
REMOVE m.nosuchkey
RETURN properties(m) AS props;
```

```
              props
----------------------------------
 {"year": 2020, "title": "Tenet"}
(1 row)
```

### Remove a key inside a nested map {#remove-a-key-inside-a-nested-map}

A property may itself be a map:

```cypher
MATCH (m:movie {title: 'Tenet'})
SET m.crew = {dop: 'Hoyte van Hoytema', editor: 'Jennifer Lame'}
RETURN properties(m) AS props;
```

```
                                               props
---------------------------------------------------------------------------------------------------
 {"crew": {"dop": "Hoyte van Hoytema", "editor": "Jennifer Lame"}, "year": 2020, "title": "Tenet"}
(1 row)
```

A dotted reference reaches into it, leaving the rest of the map alone:

```cypher
MATCH (m:movie {title: 'Tenet'})
REMOVE m.crew.dop
RETURN properties(m) AS props;
```

```
                                 props
-----------------------------------------------------------------------
 {"crew": {"editor": "Jennifer Lame"}, "year": 2020, "title": "Tenet"}
(1 row)
```

Naming the outer key removes the whole map:

```cypher
MATCH (m:movie {title: 'Tenet'})
REMOVE m.crew
RETURN properties(m) AS props;
```

```
              props
----------------------------------
 {"year": 2020, "title": "Tenet"}
(1 row)
```

### Remove a property from an edge {#remove-a-property-from-an-edge}

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
REMOVE r.credited
RETURN properties(r) AS props;
```

```
      props
-----------------
 {"role": "Neo"}
(1 row)
```

### Undo the examples {#undo-the-examples}

```cypher
MATCH (m:movie {title: 'Tenet'}) DETACH DELETE m;
```

```
UPDATE 1
```

## Notes {#notes}

`REMOVE` will not take a bare element variable. Asking it to strip everything
that way is refused, with a hint pointing at the `SET` form instead:

```cypher
MATCH (m:movie {title: 'Tenet'}) REMOVE m RETURN m.title;
```

```
ERROR:  cannot set property map to NULL
HINT:  use {} instead of NULL to remove all properties
```

`SET m = {}` empties the bag and keeps the element; `DETACH DELETE m` removes the
element altogether.

## Compatibility {#compatibility}

### Removing a label (ISO/IEC 39075 §13.4) {#removing-a-label-isoiec-39075-134}

The standard's `<remove label item>` takes a label off an element, written
`REMOVE n:blockbuster` or `REMOVE n IS blockbuster`. AgensGraph accepts neither
spelling:

```cypher
MATCH (m:movie {title: 'Tenet'}) REMOVE m:movie RETURN m.title;
```

```
ERROR:  syntax error at or near ":"
LINE 1: MATCH (m:movie {title: 'Tenet'}) REMOVE m:movie RETURN m.tit...
                                                 ^
```

A label is the table an element lives in, so it is fixed at creation. See
[`SET`](/agensgraph/reference/clauses/set/) for the same restriction on adding one.

## See also {#see-also}

- [`SET`](/agensgraph/reference/clauses/set/) — the assignment form, including `= NULL` and `= {}`
- [`DELETE`](/agensgraph/reference/clauses/delete/) — remove elements instead of properties
- [`MATCH`](/agensgraph/reference/clauses/match/) — binding the elements to strip
