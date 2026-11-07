---
title: Glossary
linkTitle: Glossary
description: The vocabulary this manual uses, with a link to the page that treats each term properly.
type: docs
weight: 60
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/appendix/glossary.html
upstream_source: agensgraph
upstream_modified: true
---


The vocabulary this manual uses, with a link to the page that treats each term properly.
Terms are grouped by what they describe rather than alphabetically, because several of them
only make sense next to each other.

## The model {#the-model}

property graph
: A data model in which the data is a set of vertices connected by edges, and both carry
  named values. AgensGraph stores one property graph and one set of relational tables in the
  same database, and one statement may read both. See [The property graph
  model](/agensgraph/concepts/property-graph-model/).

graph
: A named property graph. It is the container for a set of labels, and the unit `graph_path`
  selects. A graph is a PostgreSQL schema, created with `CREATE GRAPH`. See [How a graph is stored](/agensgraph/concepts/graph-on-postgresql/).

vertex
: One entity in a graph: a person, a film, an account. A vertex has an identity, exactly one
  label, and a set of properties. It prints as `label[graphid]{properties}`, for example
  `movie[3.7]{"title": "Avatar"}`. See [The property graph
  model](/agensgraph/concepts/property-graph-model/).

edge
: One directed connection between two vertices, with its own label and properties. An edge
  cannot exist without both endpoints. Every edge is directed, and a pattern may traverse it
  in either direction. See [The property graph model](/agensgraph/concepts/property-graph-model/).

property
: One named value on a vertex or an edge, such as `title`, `year` or `weight`. Properties are
  schemaless: two vertices of the same label need not carry the same keys. They live together
  in one `jsonb` document per element. A property key is not an identifier, so it is
  unaffected by keyword reservation and by case folding. See [How a graph is stored](/agensgraph/concepts/graph-on-postgresql/).

label
: The name that classifies a vertex or an edge, and the unit of storage: a label is a
  PostgreSQL table. A vertex has exactly one label, and it cannot be changed after the vertex
  is created. There is no label set. See [How a graph is stored](/agensgraph/concepts/graph-on-postgresql/).

vlabel
: A vertex label, the kind created by `CREATE VLABEL`. Its table is
  `(id graphid, properties jsonb)` and inherits from the graph's `ag_vertex`. See [Data
  definition](/agensgraph/reference/ddl/).

elabel
: An edge label, the kind created by `CREATE ELABEL`. Its table adds `start` and `end` to a
  vlabel's columns and inherits from the graph's `ag_edge`. See [Data
  definition](/agensgraph/reference/ddl/).

label inheritance
: A label may inherit from another, so a match on the parent also returns rows of every
  child. This is how one entity plays several roles, in place of a label set.
  `MATCH (n:parent ONLY)` opts out of it. See [Label
  inheritance](/agensgraph/concepts/label-inheritance/).

## Identity and addressing {#identity-and-addressing}

graphid
: The identity of a vertex or an edge, and a first-class type. It is a 64-bit value printed
  as two numbers, *label id*`.`*local id*. So `3.7` is row 7 of label 3. `id(n)` returns it.
  `n.id` does not, because `id` is only an ordinary property name. See
  [Limits](/agensgraph/appendix/limits/).

graph_path
: The setting that names the graph a statement runs against. There is no default: with
  `graph_path` unset, every graph statement is refused with `ERROR: graph_path is NULL`. Set
  it per session with `SET graph_path = name`, or per role or cluster. See
  [Configuration](/agensgraph/operations/configuration/).

## Querying {#querying}

path
: A sequence of alternating vertices and edges, produced by a pattern rather than by a
  constructor. `MATCH p = (a)-[e]->(b)` binds one as a value of type `graphpath`, which
  `nodes()`, `relationships()` and `length()` then read. See [Reading a
  graph](/agensgraph/querying/reading/).

traversal
: Following edges from one vertex to reach others. A graph query does this instead of
  joining on a key. A traversal of unknown depth is written with a quantified edge,
  `-[r*1..3]->`. See [Reading a graph](/agensgraph/querying/reading/).

property index
: An index on a property expression, created with `CREATE PROPERTY INDEX ON label (key)`. It
  is a PostgreSQL index whose key is an expression over the `properties` document, and a
  plain `CREATE INDEX` cannot express that key. See [How a graph is stored](/agensgraph/concepts/graph-on-postgresql/).

promoted column
: A property given a real column of a declared type, generated and stored from the
  `properties` document. A property read resolves to the column, so an ordinary index on it
  serves the query and the value keeps its own type. `movie.year` in the example dataset is
  one. See [`CREATE VLABEL`](/agensgraph/reference/ddl/create-vlabel/) and [`ALTER
  VLABEL`](/agensgraph/reference/ddl/alter-label/).

## The languages {#the-languages}

Cypher
: The graph query language AgensGraph has always accepted. It is declarative, and it matches
  by drawing a pattern in ASCII. AgensGraph's dialect is close to other implementations but
  not identical. See [Cypher, GQL and SQL](/agensgraph/concepts/languages/) and [Cypher
  compatibility](/agensgraph/appendix/cypher-compatibility/).

GQL
: ISO/IEC 39075:2024, the international standard for graph query languages. Release 2.18
  implements a substantial part of it, including the statements `LET`, `NEXT`, `FILTER`,
  `FINISH`, `INSERT` and `FOR`. GQL is not a separate mode: its statements and Cypher's mix
  freely in one pipeline. See [GQL conformance](/agensgraph/appendix/gql-conformance/).

## See also {#see-also}

- [The property graph model](/agensgraph/concepts/property-graph-model/) — the model, with worked
  examples
- [How a graph is stored](/agensgraph/concepts/graph-on-postgresql/) — how each term above is stored
- [The example dataset](/agensgraph/get-started/example-dataset/) — the graph every example uses
