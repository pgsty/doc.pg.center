---
title: The property graph model
linkTitle: The property graph model
description: 'AgensGraph stores data in two shapes at once: as relational tables, and as a property graph.'
type: docs
weight: 10
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/concepts/property-graph-model.html
upstream_source: agensgraph
upstream_modified: true
---


AgensGraph stores data in two shapes at once: as relational tables, and as a *property
graph*. This page defines the graph half — the five things a graph is made of, and the rules
each one obeys in AgensGraph specifically.

![A labelled property graph](/agensgraph/assets/images/upstream/property_model.png)

## Vertices {#vertices}

A vertex is an entity: a person, a film, an account, a sensor. It has an identity, a label,
and any number of properties.

A vertex belongs to **exactly one label**. That is the rule most likely to differ from a
graph database you have used before — there is no set of labels per vertex. Where you would
reach for several labels on one vertex, use [label
inheritance](/agensgraph/concepts/label-inheritance/) instead, which lets one pattern match a family of labels.

## Edges {#edges}

An edge connects two vertices. It has an identity, a label, any number of properties, and a
direction: it always has a start vertex and an end vertex.

Three rules hold in AgensGraph:

* **An edge always has a label.** There is no unlabelled edge.
* **An edge always has both endpoints.** A dangling edge cannot exist, so deleting a vertex
  that still has edges is refused:

      ERROR:  Vertex with connected edges cannot be removed
      HINT:  Use DETACH DELETE or remove connected edges before deleting the vertex.
* **Direction is recorded, and matching it is optional.** You store an edge one way round and
  decide per query whether direction matters: `-[:acted_in]->` follows it, `-[:acted_in]-`
  ignores it. There is no reason to store the mirror image of an edge.

## Properties {#properties}

Properties are the data on a vertex or an edge. A property has a string name and a value.

Properties are stored as a single `jsonb` document per element, so the value can be any JSON
type: a string, a number, a boolean, an array, or a nested object. Two consequences:

* **A label imposes no column list.** Two vertices with the same label may carry entirely
  different property names. Nothing has to be declared in advance.
* **`null` is not a property value.** Assigning `null` removes the property:

      MATCH (n:person {name: 'Tmp'}) SET n.born = NULL RETURN n;
      person[4.40]{"name": "Tmp"}

  So a property set to null and a property that was never there are the same thing. Turning
  on `allow_null_properties` changes that, and the null is stored:

      person[4.40]{"born": null, "name": "Tmp"}

Because a read has to go into a JSON document, a property that every query filters on can be
worth [promoting to a typed column](/agensgraph/querying/typed-columns/). That is a performance
choice, not a modelling one — the property stays a property.

> [!NOTE]
> `n.id` is not a vertex's identity. It reads a property named `id`, which usually does not
> exist. The identity is `id(n)`.

## Labels {#labels}

A label groups elements of the same kind. `movie`, `person`, `acted_in` are labels.

A label is what you attach an index to, what you grant permissions on, and what a pattern
names to narrow a search. Vertex labels and edge labels are distinct kinds, created with
`CREATE VLABEL` and `CREATE ELABEL`, and a name may be used once per graph.

Every graph is created with two labels you do not declare: `ag_vertex` and `ag_edge`. Every
label you create inherits from one of them. That inheritance is what makes an unlabelled
pattern like `MATCH (n)` mean "any vertex". A vertex created with no label at all lands in
`ag_vertex`:

```cypher
CREATE ({tmp: 1});
MATCH (n:ag_vertex ONLY) RETURN label(n) AS label, id(n) AS id, n.tmp;
```

```
    label    | id  | tmp
-------------+-----+------
 "ag_vertex" | 1.3 | 1
```

You cannot name the default label yourself:

```cypher
CREATE (:ag_vertex {tmp: 1});
```

```
ERROR:  specifying default label is not allowed
```

Label names are folded to lower case unless you double-quote them, the same way PostgreSQL
folds unquoted identifiers. A backtick is not a quoting character here — see
[Syntax](/agensgraph/reference/syntax/).

## Paths {#paths}

A path is a sequence of vertices joined by edges. It is a value in its own right: you can
bind it to a variable, return it, and ask for its length or its members.

```cypher
MATCH p = (a:person {name: 'Keanu Reeves'})-[:acted_in]->(m:movie)
RETURN length(p) AS hops, a.name AS actor, m.title AS film
ORDER BY film LIMIT 2;
```

```
 hops |     actor      |         film
------+----------------+-----------------------
 1    | "Keanu Reeves" | "The Matrix"
 1    | "Keanu Reeves" | "The Matrix Reloaded"
```

A path's length is its number of edges, so a single vertex is a path of length 0 and an edge
to itself is a path of length 1. Paths are how you express "any number of hops": see
[Paths](/agensgraph/querying/paths/) for variable-length patterns, shortest paths and weighted
search.

## Graphs {#graphs}

A graph is the container for labels, and a database may hold several. A graph is also a
PostgreSQL schema, so a graph name and a schema name cannot collide — see [How a graph is stored](/agensgraph/concepts/graph-on-postgresql/).

A session works in **one** graph at a time, named by `graph_path`:

```cypher
SET graph_path = moviekb;
```

Without it, nothing resolves:

```
ERROR:  graph_path is NULL
HINT:  Use SET graph_path
```

`graph_path` takes exactly one graph name, and a pattern cannot qualify a label with a graph
name — `MATCH (n:other.work)` is a syntax error. To read two graphs in one statement, use
SQL, which sees them as two schemas:

```cypher
CREATE GRAPH other;
SET graph_path = other;
CREATE VLABEL work;
CREATE (:work {title: 'A'}), (:work {title: 'B'});
SET graph_path = moviekb;
```

```sql
SELECT (SELECT count(*) FROM moviekb.movie) AS movies,
       (SELECT count(*) FROM other.work)    AS works;
```

```
 movies | works
--------+-------
     18 |     2
```

```cypher
DROP GRAPH other CASCADE;
```

Because `graph_path` is a per-session setting, set it for the database if every session wants
the same graph:

```sql
ALTER DATABASE mydb SET graph_path = moviekb;
```
