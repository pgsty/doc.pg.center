---
title: Label inheritance
linkTitle: Label inheritance
description: A label can inherit from another label.
type: docs
weight: 30
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/concepts/label-inheritance.html
upstream_source: agensgraph
upstream_modified: true
---


A label can inherit from another label. The child is a separate label with its own id
sequence and its own rows, but a pattern that names the parent also matches the child's
rows. That gives you a type hierarchy without giving up the ability to query the whole
family in one pattern.

Inheritance is PostgreSQL table inheritance — [a label is a table](/agensgraph/concepts/graph-on-postgresql/),
and `INHERITS` on a label becomes `INHERITS` on that table.

## Declaring a hierarchy {#declaring-a-hierarchy}

The examples on this page build their own small graph rather than using
[the example dataset](/agensgraph/get-started/example-dataset/), because inheritance is easier to
see on a hierarchy than on films and people. Run `DROP GRAPH inh CASCADE;` when you are done
with it.

```cypher
CREATE GRAPH inh;
SET graph_path = inh;

CREATE VLABEL work;
CREATE VLABEL film INHERITS (work);
CREATE VLABEL series INHERITS (work);

CREATE (:film {title: 'A'}), (:series {title: 'B'}), (:work {title: 'C'});
```

Naming the parent matches every row in the family:

```cypher
MATCH (n:work) RETURN label(n) AS label, n.title AS t ORDER BY t;
```

```
  label   |  t
----------+-----
 "film"   | "A"
 "series" | "B"
 "work"   | "C"
```

Naming a child matches only that child:

```cypher
MATCH (n:film) RETURN label(n) AS label, n.title AS t;
```

```
 label  |  t
--------+-----
 "film" | "A"
```

Note what `label(n)` returns: the label the vertex was created with, never the parent. A
vertex belongs to exactly one label. "Matching the parent" is about which tables the pattern
scans, not about a vertex having two labels.

## ONLY: excluding the children {#only-excluding-the-children}

`ONLY` restricts a pattern to the named label itself:

```cypher
MATCH (n:work ONLY) RETURN label(n) AS label, n.title AS t;
```

```
 label  |  t
--------+-----
 "work" | "C"
```

It works on edges too, and is written inside the brackets:

```cypher
MATCH ()-[e:rel ONLY]->() RETURN count(e) AS n;
```

```
 n
---
 0
```

That zero is the useful case: `rel` has a child, `sequel`, and all the edges were created as
`sequel`, so `rel ONLY` matches none of them while plain `rel` matches all of them.

## Edges inherit the same way {#edges-inherit-the-same-way}

```cypher
CREATE ELABEL rel;
CREATE ELABEL sequel INHERITS (rel);

MATCH (a:film {title: 'A'}), (b:series {title: 'B'}) CREATE (a)-[:sequel]->(b);
MATCH ()-[e:rel]->() RETURN label(e) AS label;
```

```
  label
----------
 "sequel"
```

## More than one parent {#more-than-one-parent}

A label may inherit from several labels at once:

```cypher
CREATE VLABEL hybrid INHERITS (work, film);
```

The rows of `hybrid` are then matched by `MATCH (n:work)` and by `MATCH (n:film)`.

## What every graph already inherits {#what-every-graph-already-inherits}

Every label you create inherits from `ag_vertex` or `ag_edge`, even when you write no
`INHERITS` clause. That is why an unlabelled `MATCH (n)` matches everything. See
[How a graph is stored](/agensgraph/concepts/graph-on-postgresql/#every-graph-has-two-labels-you-did-not-create).

## What it costs {#what-it-costs}

A pattern on a parent scans the parent's table and every table below it, so the plan grows
an `Append` over the family:

```cypher
EXPLAIN (COSTS OFF) MATCH (n:work) RETURN n;
```

```
             QUERY PLAN
------------------------------------
 Result
   ->  Append
         ->  Seq Scan on work n_1
         ->  Seq Scan on film n_2
         ->  Seq Scan on series n_3
         ->  Seq Scan on hybrid n_4
```

`ONLY` takes the `Append` away:

```cypher
EXPLAIN (COSTS OFF) MATCH (n:work ONLY) RETURN n;
```

```
     QUERY PLAN
--------------------
 Seq Scan on work n
```

Two things follow. A deep hierarchy makes the cheapest possible query, "give me the rows of
one label", plan over more relations than it needs. So name the child, or add `ONLY`, when
you want one label's rows and no others. And an index has to exist on each table that will be scanned: an
index on `work` does not index `film`'s rows. [Indexes and
constraints](/agensgraph/querying/indexes-and-constraints/) covers building an index across a
hierarchy.

> [!NOTE]
> Reach for inheritance when a query genuinely wants the whole family — a `work` that is
> sometimes a `film` and sometimes a `series`. If every query names the child anyway, separate
> labels are simpler and plan better.
