---
title: CREATE
linkTitle: CREATE
description: Adds vertices and edges to the graph, one for every element of its pattern.
type: docs
weight: 100
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/create.html
upstream_source: agensgraph
upstream_modified: true
---


Adds vertices and edges to the graph, one for every element of its pattern.

## Synopsis {#synopsis}

```text
CREATE pattern [, pattern ] ...
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`CREATE` writes the pattern you give it into the graph. It takes the same pattern
syntax [`MATCH`](/agensgraph/reference/clauses/match/) reads with, but every element is built rather than
looked for.

- `CREATE` **always creates**. It does not check whether an identical vertex or
  edge is already there. To create only what is missing, use
  [`MERGE`](/agensgraph/reference/clauses/merge/).
- An element that names a **variable already in scope** is reused, not rebuilt.
  That is how an edge is attached to vertices a `MATCH` found: the endpoints are
  bound variables, so only the edge is new.
- An element that names a **new variable, or none**, is created. A pattern can
  therefore create a vertex and its edge in one step.
- Every element needs enough information to be built. An edge needs a label and a
  direction; a vertex without a label becomes a bare `ag_vertex`.
- A property map may be a **map literal**, a query parameter, or `= expression`
  where the expression yields a jsonb object. That last form is how a whole table
  row becomes a property bag. See [`LOAD FROM`](/agensgraph/reference/clauses/load-from/).
- `CREATE` runs once per incoming row. With no clause in front of it, it runs
  once.
- `CREATE` may lead a query or follow another clause, and it may end one. Add a
  [`RETURN`](/agensgraph/reference/clauses/return/) to see what it built.

[`INSERT`](/agensgraph/reference/clauses/insert/) is an exact synonym, the spelling ISO/IEC 39075 uses.

## Parameters {#parameters}

pattern
: A path pattern in [`MATCH`](/agensgraph/reference/clauses/match/) syntax. Several may be listed, separated
  by commas; they are created in order and may share variables.

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).
The last example undoes them.

### Create one vertex {#create-one-vertex}

```cypher
CREATE (:movie {title: 'Tenet', year: 2020, genre: 'Action'});
```

```
UPDATE 1
```

A graph write reports the number of graph elements it touched under the `UPDATE`
tag, whatever the clause was.

### Create a vertex and see what you made {#create-a-vertex-and-see-what-you-made}

```cypher
CREATE (p:person {name: 'John David Washington', born: 1984})
RETURN p.name AS person, p.born AS born;
```

```
         person          | born
-------------------------+------
 "John David Washington" | 1984
(1 row)
```

### Create an edge between two existing vertices {#create-an-edge-between-two-existing-vertices}

Find both endpoints, then create only the edge:

```cypher
MATCH (d:person {name: 'Christopher Nolan'}), (m:movie {title: 'Tenet'})
CREATE (d)-[r:directed]->(m)
RETURN d.name AS director, label(r) AS edge, m.title AS film;
```

```
      director       |    edge    |  film
---------------------+------------+---------
 "Christopher Nolan" | "directed" | "Tenet"
(1 row)
```

`d` and `m` are already bound, so they are reused. Had the pattern written
`(d:person {name: 'Christopher Nolan'})` again inside the `CREATE`, a second
Christopher Nolan would have been created.

### Create a vertex and its edge together {#create-a-vertex-and-its-edge-together}

Anything in the pattern that is not already bound is built:

```cypher
MATCH (m:movie {title: 'Tenet'})
CREATE (a:person {name: 'Elizabeth Debicki', born: 1990})-[r:acted_in {role: 'Kat'}]->(m)
RETURN a.name AS actor, r.role AS role, m.title AS film;
```

```
        actor        | role  |  film
---------------------+-------+---------
 "Elizabeth Debicki" | "Kat" | "Tenet"
(1 row)
```

### Create several patterns at once {#create-several-patterns-at-once}

Comma-separated patterns are built in one clause and can share variables:

```cypher
MATCH (p:person {name: 'John David Washington'}), (m:movie {title: 'Tenet'})
CREATE (p)-[:acted_in {role: 'The Protagonist'}]->(m),
       (m)-[:related_to {weight: 2}]->(:movie {title: 'Memento', year: 2000, genre: 'Thriller'});
```

```
UPDATE 3
```

Three elements: one `acted_in` edge, one `related_to` edge, and the `Memento`
vertex. `Tenet` now has four edges:

```cypher
MATCH (m:movie {title: 'Tenet'})-[r]-(x)
RETURN label(r) AS edge, label(x) AS other, coalesce(x.name, x.title) AS name
ORDER BY edge, name;
```

```
     edge     |  other   |          name
--------------+----------+-------------------------
 "acted_in"   | "person" | "Elizabeth Debicki"
 "acted_in"   | "person" | "John David Washington"
 "directed"   | "person" | "Christopher Nolan"
 "related_to" | "movie"  | "Memento"
(4 rows)
```

### Watch CREATE duplicate {#watch-create-duplicate}

Nothing about `CREATE` is idempotent:

```cypher
CREATE (:person {name: 'Duplicate', born: 1}), (:person {name: 'Duplicate', born: 1});
```

```
UPDATE 2
```

```cypher
MATCH (p:person {name: 'Duplicate'}) RETURN count(*) AS rows;
```

```
 rows
------
 2
(1 row)
```

Running the first statement again would make four. Use [`MERGE`](/agensgraph/reference/clauses/merge/), or a
unique constraint, when a key has to stay unique.

### Undo the examples {#undo-the-examples}

```cypher
MATCH (p:person {name: 'Duplicate'}) DELETE p;
MATCH (m:movie) WHERE m.title IN ['Tenet', 'Memento'] DETACH DELETE m;
MATCH (p:person) WHERE p.name IN ['John David Washington', 'Elizabeth Debicki'] DETACH DELETE p;
```

```
UPDATE 2
UPDATE 6
UPDATE 2
```

## Notes {#notes}

A vertex's id is assigned from the label's own sequence, so the number a new
vertex gets depends on what has been created in that label before. Read it with
`id(v)`; do not depend on a particular value.

> [!NOTE]
> A `CREATE` with no label — `CREATE ()` — is legal and produces a vertex of the
> graph's base label `ag_vertex`. Such a vertex is invisible to every
> `MATCH (n:label)` and easy to lose track of. Always give a label.

## Compatibility {#compatibility}

### The clause name (ISO/IEC 39075 §13.2) {#the-clause-name-isoiec-39075-132}

The standard's data-inserting statement is `INSERT`, not `CREATE`. AgensGraph
accepts both spellings for the same clause; see [`INSERT`](/agensgraph/reference/clauses/insert/). SQL's
`CREATE` statements, such as `CREATE GRAPH` and `CREATE VLABEL`, are separate
statements and are unaffected.

## See also {#see-also}

- [`INSERT`](/agensgraph/reference/clauses/insert/) **GQL** — the standard spelling of this clause
- [`MERGE`](/agensgraph/reference/clauses/merge/) — create only what is not already there
- [`MATCH`](/agensgraph/reference/clauses/match/) — the pattern syntax, and how to bind endpoints first
- [`SET`](/agensgraph/reference/clauses/set/) — change properties after creating
- [`DELETE`](/agensgraph/reference/clauses/delete/) — remove what you created
- [`LOAD FROM`](/agensgraph/reference/clauses/load-from/) — create from the rows of a table
