---
title: DELETE
linkTitle: DELETE
description: Removes vertices and edges from the graph.
type: docs
weight: 150
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/delete.html
upstream_source: agensgraph
upstream_modified: true
---


**GQL clause**

Removes vertices and edges from the graph. `DETACH DELETE` removes a vertex's
edges along with it.

## Synopsis {#synopsis}

```text
[ DETACH ] DELETE expression [, expression ] ...
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`DELETE` removes the graph elements its expressions evaluate to. It needs them
bound first, so it always follows a clause that found them.

- A **plain `DELETE` refuses a vertex that still has edges**. Deleting it would
  leave edges pointing at nothing, so the clause raises an error and the
  transaction rolls back.
- **`DETACH DELETE`** deletes the vertex's edges first and then the vertex. Use
  it whenever the vertex might be connected.
- Deleting an **edge** never needs `DETACH`, and never touches its endpoints.
- Several expressions may be listed. They are deleted in the order given, so
  listing an edge before its endpoints works without `DETACH`.
- `DELETE` runs once per incoming row. An element already deleted by an earlier
  row is not an error.
- Each expression must be a vertex, an edge or a path. A property reference is
  not accepted: to remove a property, use [`REMOVE`](/agensgraph/reference/clauses/remove/).
- `DELETE` may end a query. Add a [`RETURN`](/agensgraph/reference/clauses/return/) to see what went.

## Parameters {#parameters}

DETACH
: Delete each vertex's connected edges along with it.

expression
: An expression yielding a vertex, an edge or a path, usually a variable bound
  by a [`MATCH`](/agensgraph/reference/clauses/match/).

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).
The first example builds the subgraph the rest remove, so the dataset ends as it
began.

### Build something to delete {#build-something-to-delete}

```cypher
CREATE (:movie {title: 'Tenet', year: 2020, genre: 'Action'});
MATCH (d:person {name: 'Christopher Nolan'}), (m:movie {title: 'Tenet'})
CREATE (d)-[:directed]->(m);
MATCH (m:movie {title: 'Tenet'})
CREATE (a:person {name: 'Elizabeth Debicki', born: 1990})-[:acted_in {role: 'Kat'}]->(m);
```

```
UPDATE 1
UPDATE 1
UPDATE 2
```

`Tenet` now has two edges:

```cypher
MATCH (m:movie {title: 'Tenet'})-[r]-(x)
RETURN label(r) AS edge, count(*) AS n
ORDER BY edge;
```

```
    edge    | n
------------+---
 "acted_in" | 1
 "directed" | 1
(2 rows)
```

### See a plain DELETE refuse a connected vertex {#see-a-plain-delete-refuse-a-connected-vertex}

```cypher
MATCH (m:movie {title: 'Tenet'}) DELETE m;
```

```
ERROR:  Vertex with connected edges cannot be removed
HINT:  Use DETACH DELETE or remove connected edges before deleting the vertex.
```

Nothing is deleted. The graph never holds an edge whose endpoint is gone.

### Delete an edge {#delete-an-edge}

An edge needs no `DETACH`, and its endpoints survive:

```cypher
MATCH (:person {name: 'Elizabeth Debicki'})-[r:acted_in]->(:movie {title: 'Tenet'})
DELETE r;
```

```
UPDATE 1
```

```cypher
MATCH (p:person {name: 'Elizabeth Debicki'})-[r]-() RETURN count(*) AS edges;
```

```
 edges
-------
 0
(1 row)
```

### Delete an unconnected vertex, and see what went {#delete-an-unconnected-vertex-and-see-what-went}

With no edges left, a plain `DELETE` succeeds. A `RETURN` after it reports the
element that was removed:

```cypher
MATCH (p:person {name: 'Elizabeth Debicki'})
DELETE p
RETURN properties(p) AS removed;
```

```
                   removed
---------------------------------------------
 {"born": 1990, "name": "Elizabeth Debicki"}
(1 row)
```

### Delete a vertex and its edges together {#delete-a-vertex-and-its-edges-together}

`Tenet` still has the `directed` edge. `DETACH DELETE` takes both:

```cypher
MATCH (m:movie {title: 'Tenet'}) DETACH DELETE m;
```

```
UPDATE 2
```

Two elements: the edge and the vertex. Christopher Nolan is untouched, and keeps
his other edges:

```cypher
MATCH (p:person {name: 'Christopher Nolan'})-[:directed]->(m:movie)
RETURN m.title AS film
ORDER BY film;
```

```
      film
----------------
 "Inception"
 "Interstellar"
(2 rows)
```

### Delete several elements in one clause {#delete-several-elements-in-one-clause}

List the edge before the vertices it joins and no `DETACH` is needed, because by
the time the vertices are deleted the edge is gone:

```cypher
CREATE (:person {name: 'Extra Two'});
MATCH (a:person {name: 'Extra Two'}) CREATE (a)-[:acted_in]->(:movie {title: 'Scratch'});
```

```
UPDATE 1
UPDATE 2
```

```cypher
MATCH (a:person {name: 'Extra Two'})-[r:acted_in]->(m:movie {title: 'Scratch'})
DELETE r, a, m;
```

```
UPDATE 3
```

The dataset is back to its original size:

```cypher
MATCH (n) RETURN label(n) AS label, count(*) AS n ORDER BY label;
```

```
  label   | n
----------+----
 "movie"  | 18
 "person" | 28
(2 rows)
```

## Notes {#notes}

`DELETE` takes elements, not properties. Naming a property is refused rather than
quietly ignored:

```cypher
MATCH (m:movie {title: 'The Matrix'}) DELETE m.title;
```

```
ERROR:  node, relationship, or path is expected
LINE 1: MATCH (m:movie {title: 'The Matrix'}) DELETE m.title;
                                                     ^
```

Use [`REMOVE`](/agensgraph/reference/clauses/remove/) for a property, or `SET m.title = NULL`.

> [!NOTE]
> `DETACH DELETE` on a busy vertex can delete a great many edges in one statement,
> and all of it is one transaction. Count first — `MATCH (v)-[r]-() RETURN count(r)`
> — when you are not sure how large the blast radius is.

## Compatibility {#compatibility}

### NODETACH (ISO/IEC 39075 §13.5) {#nodetach-isoiec-39075-135}

The standard's `<delete statement>` is `[ DETACH | NODETACH ] DELETE`, with
`NODETACH` the implicit default. AgensGraph implements the default but not the
keyword: `NODETACH DELETE m` is a syntax error. Write a plain `DELETE`, which
means the same thing.

## See also {#see-also}

- [`REMOVE`](/agensgraph/reference/clauses/remove/) — remove properties instead of elements
- [`MATCH`](/agensgraph/reference/clauses/match/) — binding the elements to delete
- [`CREATE`](/agensgraph/reference/clauses/create/), [`MERGE`](/agensgraph/reference/clauses/merge/) — the clauses that put them there
- [Data definition](/agensgraph/reference/ddl/) — dropping a whole label or graph
