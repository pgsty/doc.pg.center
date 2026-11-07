---
title: Writing a graph
linkTitle: Writing a graph
description: A write clause has no pattern matching of its own worth the name.
type: docs
weight: 20
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/querying/writing.html
upstream_source: agensgraph
upstream_modified: true
---


A write clause has no pattern matching of its own worth the name. It takes rows from
whatever came before it and does something to each one. So every write beyond the very
first `CREATE` follows the same shape: find first, then write.

That is the whole plan of this page. It walks the write clauses in the order you need them:
`CREATE`, `MERGE`, `SET`, `REMOVE`, `DELETE`. Then it finishes with what a transaction does
to a graph. The formal syntax for each is in the reference:
[`CREATE`](/agensgraph/reference/clauses/create/), [`MERGE`](/agensgraph/reference/clauses/merge/),
[`SET`](/agensgraph/reference/clauses/set/), [`REMOVE`](/agensgraph/reference/clauses/remove/),
[`DELETE`](/agensgraph/reference/clauses/delete/).

The examples run against [the example dataset](/agensgraph/get-started/example-dataset/) and put it
back as they found it, so you can work down the page and still match the counts other pages
print.

## Making something new {#making-something-new}

`CREATE` with a pattern that binds nothing existing makes a vertex:

```cypher
CREATE (p:person {name: 'Gloria Foster'}) RETURN p;
```

```
                   p                    
----------------------------------------
 person[4.153]{"name": "Gloria Foster"}
```

The `RETURN` is optional and the label is not: a vertex created with no label lands in
`ag_vertex`, and an edge must always have one. The id in that result is whatever the label's
sequence was up to, so your own will differ.

To connect two things that already exist, find them and then create the edge. There is no
way to write an edge to a vertex you have not matched:

```cypher
MATCH (p:person {name: 'Gloria Foster'}), (m:movie {title: 'The Matrix'})
CREATE (p)-[r:acted_in {role: 'The Oracle'}]->(m)
RETURN r;
```

```
                        r                        
-------------------------------------------------
 acted_in[5.71][4.153,3.1]{"role": "The Oracle"}
```

An edge prints as `label[id][start,end]{properties}`. `(p)` and `(m)` here carry no label
and no property map. They are references to variables already bound, and adding a label to
one would make it a *new* vertex instead.

A `CREATE` pattern longer than one element makes everything in it:

```cypher
CREATE (d:person {name: 'Marc Caro'})-[:directed]->(f:movie {title: 'The City of Lost Children', year: 1995})
RETURN d.name AS director, f.title AS film;
```

```
  director   |            film             
-------------+-----------------------------
 "Marc Caro" | "The City of Lost Children"
```

`INSERT` is the ISO/IEC 39075 spelling of the same clause and takes the same patterns:
`INSERT (:person {name: 'Ada Lovelace'})`. See [`INSERT`](/agensgraph/reference/clauses/insert/).

## Making something only if it is not there {#making-something-only-if-it-is-not-there}

`MERGE` matches its pattern, and creates it only when the match finds nothing:

```cypher
MERGE (p:person {name: 'Gloria Foster'}) RETURN p;
```

```
                   p                    
----------------------------------------
 person[4.153]{"name": "Gloria Foster"}
```

That found the vertex from the previous section rather than making a second one. Be careful
about *what* it matches on: the entire pattern, including every property in the map. Add one
property and the pattern no longer describes the vertex you have, so `MERGE` makes one that
it does describe:

```cypher
MERGE (p:person {name: 'Gloria Foster', born: 1933}) RETURN p;
```

```
                          p                           
------------------------------------------------------
 person[4.155]{"born": 1933, "name": "Gloria Foster"}
```

There are now two:

```cypher
MATCH (p:person {name: 'Gloria Foster'}) RETURN id(p) AS id, p.born AS born ORDER BY id;
```

```
  id   | born 
-------+------
 4.153 | 
 4.155 | 1933
```

So `MERGE` on a map of everything you know about a thing is a duplicate generator. `MERGE`
on the keys that *identify* it, with the rest of the values applied afterwards, is
idempotent. `ON CREATE SET` and `ON MATCH SET` are there for that:

```cypher
MERGE (p:person {name: 'Joe Pantoliano'})
  ON CREATE SET p.born = 1951, p.seen = 1
  ON MATCH SET p.seen = p.seen + 1
RETURN p;
```

```
                                p                                 
------------------------------------------------------------------
 person[4.156]{"born": 1951, "name": "Joe Pantoliano", "seen": 1}
```

Run it again and only the `ON MATCH` branch fires:

```
                                p                                 
------------------------------------------------------------------
 person[4.156]{"born": 1951, "name": "Joe Pantoliano", "seen": 2}
```

`MERGE` works on edges the same way, and matching an edge pattern means matching its label,
its direction, its property map *and* both endpoints. Bind the endpoints with `MATCH` first
so `MERGE` decides about the edge alone. This one is already there, so nothing is created:

```cypher
MATCH (p:person {name: 'Christopher Nolan'}), (m:movie {title: 'Inception'})
MERGE (p)-[r:directed]->(m) RETURN r;
```

```
            r             
--------------------------
 directed[6.8][4.8,3.5]{}
```

Back to one Gloria Foster before going on:

```cypher
MATCH (p:person {name: 'Gloria Foster', born: 1933}) DELETE p;
```

A uniqueness constraint on the identifying property is the durable version of this
discipline, because it refuses the duplicate instead of relying on you to write the right
`MERGE`. See [Indexes and constraints](/agensgraph/querying/indexes-and-constraints/#constraints).

## Changing properties {#changing-properties}

`SET` on one property adds it or replaces it:

```cypher
MATCH (p:person {name: 'Gloria Foster'}) SET p.born = 1933 RETURN p;
```

```
                          p                           
------------------------------------------------------
 person[4.153]{"born": 1933, "name": "Gloria Foster"}
```

`SET p += { ... }` merges a map in, adding keys and overwriting the ones that collide:

```cypher
MATCH (p:person {name: 'Gloria Foster'}) SET p += {died: 2001, city: 'Chicago'} RETURN p;
```

```
                                           p                                           
---------------------------------------------------------------------------------------
 person[4.153]{"born": 1933, "city": "Chicago", "died": 2001, "name": "Gloria Foster"}
```

`SET p = { ... }` replaces the whole property map. Everything not in the new map is gone:

```cypher
MATCH (p:person {name: 'Gloria Foster'}) SET p = {name: 'Gloria Foster', born: 1933} RETURN p;
```

```
                          p                           
------------------------------------------------------
 person[4.153]{"born": 1933, "name": "Gloria Foster"}
```

The difference between `+=` and `=` is the difference between `UPDATE ... SET one_column`
and replacing the row, and it is easy to type the wrong one.

Assigning null does not store a null. It removes the property:

```cypher
MATCH (p:person {name: 'Gloria Foster'}) SET p.born = NULL RETURN p;
```

```
                   p                    
----------------------------------------
 person[4.153]{"name": "Gloria Foster"}
```

So a property set to null and a property that never existed are the same state, and there is
no way to tell them apart afterwards. `allow_null_properties` changes that and stores the
null; it is off by default. `REMOVE` is the explicit spelling of the same thing:

```cypher
MATCH (p:person {name: 'Joe Pantoliano'}) REMOVE p.seen RETURN p;
```

```
                           p                           
-------------------------------------------------------
 person[4.156]{"born": 1951, "name": "Joe Pantoliano"}
```

An edge's properties are written exactly like a vertex's:

```cypher
MATCH (:person {name: 'Gloria Foster'})-[r:acted_in]->(:movie {title: 'The Matrix'})
SET r.credited = true RETURN r;
```

```
                                 r                                 
-------------------------------------------------------------------
 acted_in[5.71][4.153,3.1]{"role": "The Oracle", "credited": true}
```

> [!NOTE]
> A promoted property is the one exception to "a property can hold anything". Once a key has
> a typed column behind it, a write whose JSON type does not fit that column aborts. See
> [Promoting a property to a column](/agensgraph/querying/typed-columns/#what-promotion-costs-you).

## Removing things {#removing-things}

`DELETE` removes what you matched and hands it back, so you can see what went:

```cypher
MATCH (p:person {name: 'Joe Pantoliano'}) DELETE p RETURN p;
```

```
                           p                           
-------------------------------------------------------
 person[4.156]{"born": 1951, "name": "Joe Pantoliano"}
```

A vertex that still has edges cannot be deleted, because an edge with a missing endpoint
cannot exist:

```cypher
MATCH (p:person {name: 'Gloria Foster'}) DELETE p;
```

```
ERROR:  Vertex with connected edges cannot be removed
HINT:  Use DETACH DELETE or remove connected edges before deleting the vertex.
```

Either remove the edges yourself:

```cypher
MATCH (:person {name: 'Gloria Foster'})-[r:acted_in]->() DELETE r RETURN r;
```

```
                                 r                                 
-------------------------------------------------------------------
 acted_in[5.71][4.153,3.1]{"role": "The Oracle", "credited": true}
```

or say `DETACH DELETE`, which removes the vertex together with every edge touching it:

```cypher
MATCH (d:person {name: 'Marc Caro'}) DETACH DELETE d;
MATCH (f:movie {title: 'The City of Lost Children'}) DETACH DELETE f;
MATCH (p:person {name: 'Gloria Foster'}) DELETE p;
```

The dataset is now back to what it was:

```cypher
MATCH (n) RETURN count(n) AS elements;
```

```
 elements 
----------
 46
```

The refusal is a guard, not an inconvenience. `DETACH DELETE` on a hub vertex can remove far
more than you meant, so match the edges you intend to lose and count them before you delete
anything.

## Reading what you just wrote {#reading-what-you-just-wrote}

A write clause is not the end of a statement. Its output rows carry on down the pipeline,
and a read after it sees the graph as the write left it:

```cypher
CREATE (:person {name: 'Gloria Foster'})
WITH 1 AS done
MATCH (p:person {name: 'Gloria Foster'})
RETURN count(p) AS found;
```

```
 found 
-------
 1
```

The planner arranges that by materialising the write's effects before the next read runs.
That is an "eager" plan, and `EXPLAIN` labels it as such. [Tuning a
query](/agensgraph/querying/performance/#the-settings-that-change-plan-shape) covers what that costs and the
setting that forbids it.

## Transactions {#transactions}

A graph is tables in a database, so a write to a graph is an ordinary transactional write.
There is nothing to enable and no second commit to think about: a Cypher write and a SQL
write in one transaction commit together or roll back together.

```sql
CREATE TABLE import_log (what text, at timestamptz DEFAULT now());
```

```cypher
BEGIN;
CREATE (:person {name: 'Gloria Foster'});
INSERT INTO import_log (what) VALUES ('added Gloria Foster');
MATCH (p:person {name: 'Gloria Foster'}) RETURN count(p) AS found;
```

```
 found 
-------
 1
```

Inside the transaction both writes are there. Roll back and neither is:

```cypher
ROLLBACK;
MATCH (p:person {name: 'Gloria Foster'}) RETURN count(p) AS found;
```

```
 found 
-------
 0
```

```sql
SELECT count(*) AS logged FROM import_log;
```

```
 logged 
--------
      0
```

```sql
DROP TABLE import_log;
```

Everything else that follows from being PostgreSQL follows here too: isolation levels,
savepoints, `SELECT ... FOR UPDATE` on a label table, deadlock detection between two
sessions writing the same vertex. A bulk load is one transaction if you want it to be, and
`CREATE GRAPH` inside a transaction rolls back like any other DDL.

Two gates exist in the other direction. Writing rows into a label with SQL `INSERT`,
`UPDATE`, `DELETE` or `MERGE` is refused unless `enable_graph_dml` is on. Reshaping a
label with `ALTER TABLE` is refused unless `enable_graph_ddl` is on. Either can leave the
graph catalog describing something that is no longer true. See [How a graph is stored](/agensgraph/concepts/graph-on-postgresql/#what-is-deliberately-closed-off).

## Where to go next {#where-to-go-next}

* [Loading data](/agensgraph/guides/loading-data/) — bulk loading, including `LOAD FROM` over an
  existing table.
* [Composing a query](/agensgraph/querying/composing/) — `WITH`, `UNWIND` and aggregation, all of which are
  useful in front of a write clause.
* [Security](/agensgraph/operations/security/) — grants and row-level security on a label.
