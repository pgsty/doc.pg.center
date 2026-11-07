---
title: MERGE
linkTitle: MERGE
description: Matches a pattern if it already exists and creates it if it does not, then binds its variables either
  way.
type: docs
weight: 120
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/merge.html
upstream_source: agensgraph
upstream_modified: true
---


Matches a pattern if it already exists and creates it if it does not, then binds
its variables either way.

## Synopsis {#synopsis}

```text
MERGE pattern    [ ON { CREATE | MATCH } SET set_item [, set_item ] ... ] ...
```

**Notation:** uppercase keywords, lowercase placeholders, `[ ]` optional, `...` repeatable. See [Syntax conventions](/agensgraph/reference/syntax/).

## Description {#description}

`MERGE` is one clause doing the work of a [`MATCH`](/agensgraph/reference/clauses/match/) and a
[`CREATE`](/agensgraph/reference/clauses/create/). It looks for its pattern; if the pattern is there it
behaves like a `MATCH`, and if it is not there it behaves like a `CREATE`. Either
way the pattern's variables end up bound, so the rest of the query does not have
to know which happened.

One rule decides everything about `MERGE`. The clause considers **the whole
pattern**:

- If the entire pattern matches, nothing is written.
- If any part of it is missing, the **whole pattern is created**, including
  parts that already exist elsewhere in the graph. Merging
  `(a)-[:e]->(b)` when `a` and `b` exist but the edge does not creates a second
  `a` and a second `b` as well as the edge.
- So merge **one element at a time** when you are not sure what is already
  there. Use a `MERGE` per vertex, then a `MERGE` for the edge between the
  variables they bound. Written that way, `MERGE` is idempotent.

Other rules:

- `MERGE` takes **exactly one pattern**. Comma-separated patterns are a syntax
  error; use several `MERGE` clauses.
- `ON CREATE SET` runs only when the pattern was created; `ON MATCH SET` runs
  only when it was matched. Both may be given, in either order, and each takes a
  [`SET`](/agensgraph/reference/clauses/set/) item list.
- Properties in the pattern are part of what is matched. `MERGE (m:movie {title: 'Tenet'})`
  matches only a `movie` whose `title` is exactly `Tenet`; it does not match one
  that merely has a `title`.
- `MERGE` runs once per incoming row. It may lead a query, follow another clause,
  or end one.

## Parameters {#parameters}

pattern
: One path pattern in [`MATCH`](/agensgraph/reference/clauses/match/) syntax. Every property in it is both a
  match condition and, on create, a property to set.

ON CREATE SET
: Assignments applied only when the pattern was created.

ON MATCH SET
: Assignments applied only when the pattern was found.

set_item
: An assignment in [`SET`](/agensgraph/reference/clauses/set/) syntax: `variable.property = expression`,
  `variable = map` or `variable += map`.

## Examples {#examples}

Every example runs against [the example dataset](/agensgraph/get-started/example-dataset/).
The last example undoes them.

### Create the vertex, or find it {#create-the-vertex-or-find-it}

The first run creates:

```cypher
MERGE (m:movie {title: 'Tenet'}) RETURN m.title AS film, m.year AS year;
```

```
  film   | year
---------+------
 "Tenet" |
(1 row)
```

Only `title` was in the pattern, so `year` is unset. The second run finds the
same vertex and writes nothing:

```cypher
MERGE (m:movie {title: 'Tenet'}) RETURN m.title AS film, m.year AS year;
```

```
  film   | year
---------+------
 "Tenet" |
(1 row)
```

```cypher
MATCH (m:movie {title: 'Tenet'}) RETURN count(*) AS rows;
```

```
 rows
------
 1
(1 row)
```

### Set different properties on create and on match {#set-different-properties-on-create-and-on-match}

Start from nothing:

```cypher
MATCH (m:movie {title: 'Tenet'}) DETACH DELETE m;
```

```
UPDATE 1
```

```cypher
MERGE (m:movie {title: 'Tenet'})
ON CREATE SET m.year = 2020, m.source = 'created'
ON MATCH SET m.source = 'matched'
RETURN m.title AS film, m.year AS year, m.source AS source;
```

```
  film   | year |  source
---------+------+-----------
 "Tenet" | 2020 | "created"
(1 row)
```

The identical statement run a second time takes the other branch:

```cypher
MERGE (m:movie {title: 'Tenet'})
ON CREATE SET m.year = 2020, m.source = 'created'
ON MATCH SET m.source = 'matched'
RETURN m.title AS film, m.year AS year, m.source AS source;
```

```
  film   | year |  source
---------+------+-----------
 "Tenet" | 2020 | "matched"
(1 row)
```

`year` keeps the value the create branch gave it, because `ON MATCH SET` did not
touch it.

### See a whole-pattern MERGE duplicate a vertex {#see-a-whole-pattern-merge-duplicate-a-vertex}

There is one Christopher Nolan, and he has not directed `Tenet`:

```cypher
MATCH (m:movie {title: 'Tenet'}) DETACH DELETE m;
MATCH (p:person {name: 'Christopher Nolan'}) RETURN count(*) AS nolans;
```

```
UPDATE 1
 nolans
--------
 1
(1 row)
```

Merging the whole path finds no match, because the edge is missing. So it
creates the whole path:

```cypher
MERGE (d:person {name: 'Christopher Nolan'})-[:directed]->(m:movie {title: 'Tenet'})
RETURN d.name AS director, m.title AS film;
```

```
      director       |  film
---------------------+---------
 "Christopher Nolan" | "Tenet"
(1 row)
```

```cypher
MATCH (p:person {name: 'Christopher Nolan'}) RETURN count(*) AS nolans;
```

```
 nolans
--------
 2
(1 row)
```

A second Christopher Nolan, with no `born` property and none of the original's
edges. This is the mistake `MERGE` invites.

### Merge one element at a time instead {#merge-one-element-at-a-time-instead}

Undo that, then merge each element separately:

```cypher
MATCH (p:person {name: 'Christopher Nolan'})
WHERE NOT EXISTS { MATCH (p)-[:directed]->(:movie {title: 'Inception'}) }
DETACH DELETE p;
MATCH (m:movie {title: 'Tenet'}) DETACH DELETE m;
```

```
UPDATE 2
UPDATE 1
```

```cypher
MERGE (d:person {name: 'Christopher Nolan'})
MERGE (m:movie {title: 'Tenet'})
MERGE (d)-[:directed]->(m)
RETURN d.name AS director, m.title AS film;
```

```
      director       |  film
---------------------+---------
 "Christopher Nolan" | "Tenet"
(1 row)
```

```cypher
MATCH (p:person {name: 'Christopher Nolan'}) RETURN count(*) AS nolans;
```

```
 nolans
--------
 1
(1 row)
```

The first `MERGE` matched the existing person, the second created the film, the
third created just the edge. Running the same three clauses again changes
nothing:

```cypher
MATCH (p:person {name: 'Christopher Nolan'})-[:directed]->(m:movie)
RETURN count(*) AS edges;
```

```
 edges
-------
 3
(1 row)
```

Two from the original dataset plus the one merged, however many times the
statement runs.

### Reject more than one pattern {#reject-more-than-one-pattern}

```cypher
MERGE (a:movie {title: 'A'}), (b:movie {title: 'B'});
```

```
ERROR:  syntax error at or near ","
LINE 1: MERGE (a:movie {title: 'A'}), (b:movie {title: 'B'});
                                    ^
```

Write two `MERGE` clauses.

### Undo the examples {#undo-the-examples}

```cypher
MATCH (m:movie {title: 'Tenet'}) DETACH DELETE m;
```

```
UPDATE 2
```

## Notes {#notes}

A unique constraint turns the duplication risk into a clean failure rather than
silent data corruption. With `name` unique on `person`, the whole-pattern merge
above cannot create its second Nolan:

```cypher
CREATE CONSTRAINT unique_person_name ON person ASSERT name IS UNIQUE;
MERGE (d:person {name: 'Christopher Nolan'})-[:directed]->(m:movie {title: 'Tenet'})
RETURN d.name AS director, m.title AS film;
```

```
CREATE CONSTRAINT
ERROR:  conflicting key value violates exclusion constraint "unique_person_name"
DETAIL:  Key ((properties.'name'))=("Christopher Nolan") conflicts with existing key ((properties.'name'))=("Christopher Nolan").
```

Nothing is created, and the transaction reports the reason. Declare a constraint
on whatever key your merges use.

## Compatibility {#compatibility}

### MERGE is not a GQL clause {#merge-is-not-a-gql-clause}

ISO/IEC 39075 has no `MERGE`: its data-modifying statements are
`<insert statement>` (§13.2), `<set statement>` (§13.3), `<remove statement>`
(§13.4) and `<delete statement>` (§13.5). `MERGE` comes from Cypher, and
AgensGraph keeps it. A standard-only equivalent is a
[`CALL { subquery }`](/agensgraph/reference/clauses/call-subquery/) or an `EXISTS` test followed by
[`INSERT`](/agensgraph/reference/clauses/insert/).

## See also {#see-also}

- [`CREATE`](/agensgraph/reference/clauses/create/) — write unconditionally
- [`MATCH`](/agensgraph/reference/clauses/match/) — the pattern syntax
- [`SET`](/agensgraph/reference/clauses/set/) — the assignment syntax `ON CREATE SET` and `ON MATCH SET` take
- [`DELETE`](/agensgraph/reference/clauses/delete/) — remove what a merge created
