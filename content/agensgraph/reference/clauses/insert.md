---
title: INSERT
linkTitle: INSERT
description: Creates the vertices and edges a pattern describes.
type: docs
weight: 110
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/insert.html
upstream_source: agensgraph
upstream_modified: true
---


**GQL clause**  **Added in 2.18**

Creates the vertices and edges a pattern describes. It is the GQL name for the
clause Cypher calls `CREATE`.

## Synopsis {#synopsis}

```text
INSERT [ path_variable = ] pattern [, [ path_variable = ] pattern ] ...
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`INSERT` and [`CREATE`](/agensgraph/reference/clauses/create/) are the same clause under two names. The parser builds an
identical tree for both, so they accept the same patterns, raise the same errors
and produce the same plan.

- Every element in the pattern is created, except one already bound to a variable
  in scope. That element is reused as an endpoint and not duplicated.
- An `INSERT` runs once per input row. With no preceding clause it runs once.
- Variables the pattern binds are visible to the clauses that follow, and to later
  patterns in the same `INSERT`.
- Every edge needs exactly one label and a direction. Labels must already exist
  unless `enable_graph_ddl` is on to create them implicitly.

## Parameters {#parameters}

path_variable
: Optional name bound to the whole path the pattern created. Returning it yields a
  `graphpath` value listing the new vertices and edges in order.

pattern
: A vertex or path pattern, as described in [Syntax](/agensgraph/reference/syntax/). Property maps
  may be written inline (`{title: 'Tenet'}`) or supplied whole with `=` from an
  expression, including a SQL subquery.

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).

Add one film. `INSERT` and `CREATE` are interchangeable. Switch tabs to compare:

{{< tabs >}}
{{< tab label="GQL — INSERT" >}}
```cypher
INSERT (:movie {title: 'Tenet', year: 2020, genre: 'Action'});
```
{{< /tab >}}
{{< tab label="Cypher — CREATE" >}}
```cypher
CREATE (:movie {title: 'Tenet', year: 2020, genre: 'Action'});
```
{{< /tab >}}
{{< /tabs >}}
```
UPDATE 1
```

Both plan identically:

```cypher
EXPLAIN (COSTS OFF) INSERT (:movie {title: 'Tenet'});
```

```
  QUERY PLAN
--------------
 Graph Create
   ->  Result
(2 rows)
```

### Return what you created {#return-what-you-created}

`INSERT` binds its variables like any other clause, so a following `RETURN` can
report them:

```cypher
INSERT (p:person {name: 'John David Washington', born: 1984}) RETURN p.name AS person;
```

```
         person
-------------------------
 "John David Washington"
(1 row)
```

### Attach a new element to one already in the graph {#attach-a-new-element-to-one-already-in-the-graph}

A variable bound by a preceding `MATCH` is an endpoint, not a new vertex, so only
the edge is created:

```cypher
MATCH (p:person {name: 'Christopher Nolan'}), (m:movie {title: 'Tenet'})
INSERT (p)-[:directed]->(m)
RETURN count(*) AS edges;
```

```
 edges
-------
 1
(1 row)
```

### Build several patterns in one clause {#build-several-patterns-in-one-clause}

Patterns are separated by commas and may refer to variables earlier patterns
bound:

```cypher
MATCH (m:movie {title: 'Tenet'})
INSERT (a:person {name: 'Robert Pattinson', born: 1986}),
       (b:person {name: 'Elizabeth Debicki', born: 1990}),
       (a)-[:acted_in {role: 'Neil'}]->(m),
       (b)-[:acted_in {role: 'Kat'}]->(m);
```

```
UPDATE 4
```

The tag counts the four elements the one clause created:

```cypher
MATCH (p:person)-[r:acted_in]->(:movie {title: 'Tenet'})
RETURN p.name AS actor, r.role AS role ORDER BY actor;
```

```
        actor        |  role
---------------------+--------
 "Elizabeth Debicki" | "Kat"
 "Robert Pattinson"  | "Neil"
(2 rows)
```

### Take a property map from a SQL query {#take-a-property-map-from-a-sql-query}

The `= expression` form supplies the whole map at once. Use it to load
properties out of a table:

```cypher
INSERT (:movie = (SELECT jsonb_build_object('title', 'Dunkirk', 'year', 2017)));
```

```
UPDATE 1
```

```cypher
MATCH (m:movie {title: 'Dunkirk'}) RETURN m.year AS year;
```

```
 year
------
 2017
(1 row)
```

## Notes {#notes}

The clause reports its ordinary graph-write command tag, `UPDATE n`, rather than a
`CREATE` tag. Pair it with [`FINISH`](/agensgraph/reference/clauses/finish/) when you want a write and no
projection.

Refusals name `CREATE` even when you wrote `INSERT`, because both spellings build
the same clause. The ones worth knowing:

| Pattern | Error |
| --- | --- |
| `INSERT ()-[]->()` | `only one relationship type is allowed for CREATE` |
| `INSERT ()-[:acted_in\|directed]->()` | `only one relationship type is allowed for CREATE` |
| `INSERT ()-[:directed]-()` | `only directed relationships are allowed in CREATE` |
| `INSERT (:ag_vertex)` | `specifying default label is not allowed` |
| `INSERT ()-[:ag_edge]->()` | `cannot create edge on default label` |
| `INSERT (:directed)` | `label "directed" is edge label` |
| `INSERT ()-[:movie]->()` | `label "movie" is vertex label` |
| `INSERT (m)` where `m` is already bound | `there must be at least one relationship` |

> [!NOTE]
> `insert` became a reserved keyword in 2.18. It is still accepted unquoted wherever
> that leaves the grammar unambiguous — as a variable name, `MATCH (insert:person)`,
> and as a label name in a pattern, `MATCH (n:insert)`. It is not accepted as a
> `CREATE VLABEL` name, as an `ORDER BY` key naming a `RETURN` alias, or as a SQL
> table or column name; write `"insert"` there, or rename.

## Compatibility {#compatibility}

> [!NOTE] GQL conformance
> :class: gql-conformance
>
> Implements the GQL *INSERT statement* (ISO/IEC 39075:2024 §13.2) over the
> *insert graph pattern* of §16.5.
>
> - **Supported** — inserting nodes and edges, several patterns per statement,
>   reusing a bound element as an endpoint, inline property maps, and a path
>   variable over the inserted pattern.
> - **Not supported** — the standard's typed-graph checks (§18), which require a
>   graph type; AgensGraph graphs are untyped, so an insert is validated against the
>   labels that exist rather than against a declared node or edge type.
>
> Track status in the [GQL conformance matrix](/agensgraph/appendix/gql-conformance/).

### openCypher {#opencypher}

openCypher spells this clause `CREATE`, which AgensGraph accepts as a synonym. The
`INSERT` name comes from GQL and from SQL, where it does the same job on a table.

## See also {#see-also}

- [`CREATE`](/agensgraph/reference/clauses/create/) — the Cypher synonym, same clause
- [`MERGE`](/agensgraph/reference/clauses/merge/) — create only what is not already there
- [`FOR`](/agensgraph/reference/clauses/for/) **GQL** — drive an `INSERT` once per list element
- [`FINISH`](/agensgraph/reference/clauses/finish/) **GQL** — write without projecting
- [Syntax](/agensgraph/reference/syntax/) — the pattern grammar `INSERT` takes
- [GQL conformance matrix](/agensgraph/appendix/gql-conformance/)
