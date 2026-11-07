---
title: Subquery value expressions
linkTitle: Subquery value expressions
description: 'Six expressions that answer a question with a subquery instead of a clause, usable anywhere a value
  is: RETURN, WHERE, FILTER, WITH and SQL.'
type: docs
weight: 260
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/subquery-expressions.html
upstream_source: agensgraph
upstream_modified: true
---


**GQL clause**  **Added in 2.18**

Six expressions that answer a question with a subquery instead of a clause, usable
anywhere a value is: `RETURN`, `WHERE`, `FILTER`, `WITH` and SQL.

## Synopsis {#synopsis}

```text
EXISTS { body }
COUNT { body }
COLLECT { body }
ARRAY { body }
VALUE { body }
expression [ NOT ] IN { body }
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

Each expression runs its body and reduces the result to one value. The body is
correlated: it sees the variables in scope where the expression is written, with no
import list to declare, unlike [`CALL { subquery }`](/agensgraph/reference/clauses/call-subquery/). Those
variables stay in scope through the whole body, so a clause inside it cannot bind
one of their names again: a `LET`, `UNWIND` or `FOR` on such a name, a `WITH` that
renames a value to it, or a `CALL { }` that returns it is refused. `MATCH (n)` on
the name refers to the outer node, and `WITH n` passes it on unchanged.

This table says what each one returns and what it does when the body is empty.
Five of the six answer an empty body with a value of their own type rather than
with null: a false, a zero, an empty list. `VALUE { }` has no such value to fall
back on, so it is the one that gives null.

| Expression | Returns | Body empty |
| --- | --- | --- |
| `EXISTS { }` | Boolean | `false` |
| `COUNT { }` | Row count, a `bigint` | `0` |
| `COLLECT { }` | List of the body's single column | `[]` |
| `ARRAY { }` | Same as `COLLECT` | `[]` |
| `VALUE { }` | The body's single value, in its own type | `null` |
| `x IN { }` | Boolean | `false` |

### What a body may be {#what-a-body-may-be}

Four kinds of body are accepted, and which ones are allowed depends on the
expression:

| Body | `EXISTS` / `COUNT` | `COLLECT` / `ARRAY` / `VALUE` / `IN` |
| --- | --- | --- |
| A bare pattern, with an optional `WHERE` | Yes | No |
| A `MATCH` statement, `OPTIONAL MATCH` included | Yes | No |
| A GQL read statement ending in `RETURN` | Yes | Yes |
| A SQL `SELECT` | Yes | Yes |

- **Write clauses are rejected.** `CREATE`, `INSERT`, `MERGE`, `SET`, `REMOVE`,
  `DELETE` and `DETACH DELETE` each raise a syntax error at the keyword.
- A read-statement body may use `DISTINCT`, `ORDER BY`, `SKIP`, `LIMIT`, the set
  operators and a nested `CALL { }`. It may not use [`NEXT`](/agensgraph/reference/clauses/next/).
- A bare-pattern body may not name the path (`EXISTS { p = (a)-[]->(b) }` is a
  syntax error), but `shortestpath()` and a variable-length edge are both fine.
- A **SQL `SELECT` body is uncorrelated**: it cannot see the enclosing query's
  variables. Referring to one raises `missing FROM-clause entry for table "<name>"`.

## Parameters {#parameters}

body
: The subquery, in one of the four shapes above. `COLLECT`, `ARRAY`, `VALUE` and
  `IN` need it to produce exactly one column.

expression
: For `x IN { }`, the value to look for. A node, relationship or graphid is
  matched by identity, as in `x IN [list]`, and an element on the left against a
  body of plain values is a type error. Any other value and a Cypher body's
  column meet as `jsonb`. A SQL body keeps its own column type, so unwrap the
  property first: `m.title #>> '{}'` yields `text`.

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).

### Test whether a pattern exists {#test-whether-a-pattern-exists}

`EXISTS { }` short-circuits: the planner turns it into a semi-join or an `EXISTS`
subplan rather than counting matches. A bare pattern is the shortest body, and it
takes a `WHERE`:

```cypher
MATCH (p:person)
WHERE EXISTS { (p)-[:directed]->(m:movie) WHERE m.year > 2015 }
RETURN p.name AS director ORDER BY director;
```

```
      director
--------------------
 "Denis Villeneuve"
 "Lana Wachowski"
(2 rows)
```

In `RETURN` it is a boolean column, `false` rather than null when nothing matches:

```cypher
MATCH (p:person {name: 'Keanu Reeves'}) RETURN EXISTS { (p)-[:directed]->(:movie) } AS directs;
```

```
 directs
---------
 f
(1 row)
```

### Count matches {#count-matches}

`COUNT { }` over a pattern counts the pattern's matches:

```cypher
MATCH (m:movie {title: 'The Matrix'}) RETURN COUNT { (:person)-[:acted_in]->(m) } AS cast_size;
```

```
 cast_size
-----------
 3
(1 row)
```

A read-statement body keeps its own `DISTINCT`, `LIMIT` and grouping, so it can
count something a pattern cannot:

```cypher
MATCH (m:movie {title: 'The Matrix'})
RETURN COUNT { MATCH (p:person)-[:acted_in]->(m) RETURN DISTINCT p } AS distinct_cast;
```

```
 distinct_cast
---------------
 3
(1 row)
```

### Gather a column into a list {#gather-a-column-into-a-list}

`COLLECT { }` returns a list, preserving the body's order and its nulls. `ARRAY { }`
is the same expression under the standard's name:

{{< tabs >}}
{{< tab label="GQL — ARRAY" >}}
```cypher
MATCH (m:movie {title: 'The Matrix'})
RETURN ARRAY { MATCH (p:person)-[:acted_in]->(m) RETURN p.name ORDER BY p.name } AS cast;
```
{{< /tab >}}
{{< tab label="Cypher — COLLECT" >}}
```cypher
MATCH (m:movie {title: 'The Matrix'})
RETURN COLLECT { MATCH (p:person)-[:acted_in]->(m) RETURN p.name ORDER BY p.name } AS cast;
```
{{< /tab >}}
{{< /tabs >}}
```
                            cast
------------------------------------------------------------
 ["Carrie-Anne Moss", "Keanu Reeves", "Laurence Fishburne"]
(1 row)
```

An empty body gives an empty list, not null:

```cypher
MATCH (m:movie {title: 'The Matrix'})
RETURN COLLECT { MATCH (p:person)-[:acted_in]->(m) WHERE p.born > 2000 RETURN p.name } AS nobody;
```

```
 nobody
--------
 []
(1 row)
```

### Take a single value {#take-a-single-value}

`VALUE { }` is the scalar subquery. Unlike everything else on this page it keeps
the column's own type, so a graph element survives instead of being boxed:

```cypher
MATCH (m:movie {title: 'Inception'})
RETURN VALUE { MATCH (p:person)-[:directed]->(m) RETURN p.name } AS director;
```

```
      director
---------------------
 "Christopher Nolan"
(1 row)
```

```cypher
MATCH (m:movie {title: 'Inception'})
RETURN label(VALUE { MATCH (p:person)-[:directed]->(m) RETURN p }) AS yielded_type;
```

```
 yielded_type
--------------
 "person"
(1 row)
```

The body must produce at most one row. More than one is a run-time error, so add an
`ORDER BY … LIMIT 1` or an aggregate when the body is not already single-valued:

```cypher
MATCH (m:movie {title: 'The Matrix'})
RETURN VALUE { MATCH (p:person)-[:acted_in]->(m) RETURN p.name } AS one_of_three;
```

```
ERROR:  more than one row returned by a subquery used as an expression
```

### Test membership against a subquery {#test-membership-against-a-subquery}

`x IN { }` is a semi-join, not a materialized list, so it stays cheap on a large
body. A value and a Cypher body's column meet as `jsonb`:

```cypher
MATCH (m:movie)
WHERE m.year IN { MATCH (x:movie) WHERE x.genre = 'Adventure' RETURN x.year }
RETURN m.title AS film ORDER BY film;
```

```
      film
-----------------
 "Jurassic Park"
(1 row)
```

A node is matched by identity, so two nodes with the same properties are still
two nodes. The semi-join then runs on the id:

```cypher
MATCH (p:person)
WHERE p IN { MATCH (d:person)-[:directed]->(:movie {title: 'Inception'}) RETURN d }
RETURN p.name AS director;
```

```
      director
--------------------
 "Christopher Nolan"
(1 row)
```

A SQL body keeps its own column type. `rating.title` is `text`, so unwrap the
property with `#>> '{}'` rather than comparing it as `jsonb`:

```cypher
MATCH (m:movie)
WHERE m.title #>> '{}' IN { SELECT title FROM rating WHERE source = 'audience' }
RETURN m.title AS film ORDER BY film;
```

```
      film
----------------
 "Inception"
 "Interstellar"
 "The Matrix"
(3 rows)
```

Without the unwrap the comparison has no operator: `operator does not exist: jsonb
= text`.

### Use one in a projection or from SQL {#use-one-in-a-projection-or-from-sql}

A subquery expression is a value, so it can be projected by `WITH` and then tested:

```cypher
MATCH (m:movie)
WITH m.title AS film, COUNT { (:person)-[:acted_in]->(m) } AS cast_size
FILTER cast_size > 2
RETURN film, cast_size;
```

```
     film     | cast_size
--------------+-----------
 "The Matrix" | 3
(1 row)
```

It also works from SQL, wrapped in the Cypher query that supplies its variables:

```cypher
SELECT (MATCH (m:movie {title: 'The Matrix'}) RETURN COUNT { (:person)-[:acted_in]->(m) }) AS cast_size;
```

```
 cast_size
-----------
 3
(1 row)
```

## Notes {#notes}

A write clause anywhere in a body is refused at the keyword, whichever expression
wraps it:

```cypher
MATCH (m:movie) RETURN COUNT { CREATE (:tmp) RETURN 1 AS one } AS n;
```

```
ERROR:  syntax error at or near "CREATE"
LINE 1: MATCH (m:movie) RETURN COUNT { CREATE (:tmp) RETURN 1 AS one...
                                       ^
```

So is a binding that would hide a variable of the enclosing query, with the same
error the clause raises at the top level:

```cypher
MATCH (m:movie) RETURN COUNT { LET m = 1 RETURN m } AS n;
```

```
ERROR:  variable "m" already exists
LINE 1: MATCH (m:movie) RETURN COUNT { LET m = 1 RETURN m } AS n;
                                           ^
HINT:  LET cannot redefine an existing variable; use a different name.
```

> [!NOTE]
> `ARRAY` is a reserved keyword, as it is in PostgreSQL, and so is `IN`. `COLLECT`,
> `COUNT`, `EXISTS` and `VALUE` are not reserved, so they remain usable as
> identifiers — a `RETURN … AS value` still works.

## Compatibility {#compatibility}

> [!NOTE] GQL conformance
> :class: gql-conformance
>
> Two of the six are in the standard:
>
> - `EXISTS { }` implements the GQL *exists predicate* (ISO/IEC 39075:2024 §19.4),
>   including the bare `<graph pattern>` and `<match statement block>` bodies of that
>   subclause and the nested query specification. **Supported** in full.
> - `VALUE { }` implements the GQL *value query expression* (§20.6), Feature GQ18,
>   "Scalar subqueries", with the empty-body-is-null rule of General Rule 2.
>   **Supported**, except that §20.6 Syntax Rule 10 requires the body to carry
>   `LIMIT 1` or an aggregate; AgensGraph accepts any body and raises a run-time
>   error if it returns more than one row.
>
> `COUNT { }`, `COLLECT { }`, `ARRAY { }` and `x IN { }` are **extensions**. ISO/IEC
> 39075:2024 has no subquery form of `COUNT` — §20.9 defines only `COUNT(*)` and
> `COUNT(<value expression>)` — and its list aggregate is `COLLECT_LIST(…)`, also an
> aggregate over rows rather than a subquery. `COUNT { }` and `COLLECT { }` come from
> openCypher; `ARRAY { }` follows SQL's `ARRAY(<subquery>)`; `x IN { }` follows SQL's
> `IN (<subquery>)`.
>
> Track status in the [GQL conformance matrix](/agensgraph/appendix/gql-conformance/).

### openCypher {#opencypher}

openCypher has `EXISTS { }`, `COUNT { }` and `COLLECT { }` with the same meanings.
It has no `ARRAY { }`, no `VALUE { }` and no `x IN { }` over a subquery. For a
scalar it uses `head(COLLECT { … })`, and for membership `x IN COLLECT { … }`. Both
of those work here too, but they materialize the whole list, so prefer
`VALUE { }` and `x IN { }`.

## See also {#see-also}

- [`CALL { subquery }`](/agensgraph/reference/clauses/call-subquery/) **GQL** — a subquery as a clause, with an explicit import list
- [`FILTER`](/agensgraph/reference/clauses/filter/) **GQL** — a clause these predicates suit
- [`WHERE`](/agensgraph/reference/clauses/where/) — the other place a predicate goes
- [Combining SQL and Cypher](/agensgraph/querying/combining-sql-and-cypher/) — how a SQL body fits in
- [GQL conformance matrix](/agensgraph/appendix/gql-conformance/)
