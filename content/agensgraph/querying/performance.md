---
title: Tuning a query
linkTitle: Tuning a query
description: A Cypher query is planned by PostgreSQL's planner.
type: docs
weight: 80
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/querying/performance.html
upstream_source: agensgraph
upstream_modified: true
---


A Cypher query is planned by PostgreSQL's planner. There is no separate graph engine with its
own rules, so `EXPLAIN` works, statistics matter, and the tuning you already know applies.

The AgensGraph-specific parts are a handful of plan nodes for traversal, one statistics
problem that bites every new graph, and five settings that change plan shape.

This page is about plan shape only. Resource-shaped tuning covers `shared_buffers`,
`work_mem`, `effective_cache_size`, parallelism and autovacuum. None of it is graph-specific,
and it lives in [Configuration](/agensgraph/operations/configuration/).

## A graph to measure on {#a-graph-to-measure-on}

[The example dataset](/agensgraph/get-started/example-dataset/) is 46 elements, which is not enough
for the planner to make an interesting decision. Build something with a degree distribution
and drop it at the end:

```sql
CREATE TABLE seed_account AS SELECT g AS n, 'user' || g AS handle FROM generate_series(1, 20000) g;
CREATE TABLE seed_follows AS SELECT (1 + (g % 20000)) AS src, (1 + ((g * 7919) % 20000)) AS dst FROM generate_series(1, 120000) g;
```

```cypher
CREATE GRAPH perflab;
SET graph_path = perflab;
CREATE VLABEL account;
CREATE ELABEL follows;
LOAD FROM seed_account AS r CREATE (:account {handle: r.handle, n: r.n});
CREATE PROPERTY INDEX ON account (handle);
```

```cypher
LOAD FROM seed_follows AS r MATCH (a:account {n: r.src}), (b:account {n: r.dst}) CREATE (a)-[:follows]->(b);
```

```sql
ANALYZE perflab.account;
```

20,000 accounts and 120,000 `follows` edges. Only the vertex label was analysed. That
omission is [the point of a later section](#statistics-on-edge-labels).

## Reading a Cypher EXPLAIN {#reading-a-cypher-explain}

```cypher
EXPLAIN (COSTS OFF) MATCH (a:account {handle: 'user42'})-[r1:follows]->(b:account)-[r2:follows]->(c:account) RETURN c.handle;
```

```
                                                                                                 QUERY PLAN                                                                                                 
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Hash Join
   Hash Cond: (r2."end" = c.id)
   ->  Nested Loop
         ->  Nested Loop
               ->  Index Scan using account_handle_idx on account a
                     Index Cond: (properties.'handle' = '"user42"'::jsonb)
               ->  Bitmap Heap Scan on follows r1
                     Recheck Cond: ((a.id = start) AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
                     ->  Bitmap Index Scan on follows_start_idx
                           Index Cond: ((start = a.id) AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
         ->  Index Scan using follows_start_idx on follows r2
               Index Cond: ((start = r1."end") AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
               Filter: (r1.id <> id)
   ->  Hash
         ->  Seq Scan on account c
```

Four things in there are AgensGraph-specific and everything else is a plan you have read
before.

**A property read prints as `properties.'key'`.** That is the Cypher parser's spelling of a
property access, and it is not SQL you can type. In an `Index Cond` it is being matched
against an expression index. In a `Filter` it is being evaluated per row. Which of those you
get is [the subject of the indexes page](/agensgraph/querying/indexes-and-constraints/).

**A `graphid` range test is a label test.** `start >= '3.0' AND start <= '3.281474976710655'`
is "the vertex at this end of the edge is an `account`". A label id lives in the high bits of
a `graphid`, so one label's ids form a contiguous range and the test is answerable from the
edge's own columns. See [Identity: the
graphid](/agensgraph/concepts/graph-on-postgresql/#identity-the-graphid).

**`Filter: (r1.id <> id)`** on the second edge is the uniqueness rule: no path may use one
edge twice.

**A pattern element you did not name gets a synthetic alias**, printed as `"<0000000002>"`.
The counter behind it advances on every statement, so a plan containing one differs from run
to run. Name every element of a pattern whose plan you want to compare against a baseline.

`EXPLAIN (ANALYZE)` works and is the only way to see the estimates against reality:

```cypher
EXPLAIN (ANALYZE, COSTS OFF, TIMING OFF, SUMMARY OFF, BUFFERS OFF)
MATCH (a:account {handle: 'user42'})-[r1:follows]->(b:account) RETURN count(b);
```

```
                                                                                                 QUERY PLAN                                                                                                 
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Aggregate (actual rows=1.00 loops=1)
   ->  Nested Loop (actual rows=6.00 loops=1)
         ->  Nested Loop (actual rows=6.00 loops=1)
               ->  Index Scan using account_handle_idx on account a (actual rows=1.00 loops=1)
                     Index Cond: (properties.'handle' = '"user42"'::jsonb)
                     Index Searches: 1
               ->  Bitmap Heap Scan on follows r1 (actual rows=6.00 loops=1)
                     Recheck Cond: ((a.id = start) AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
                     Heap Blocks: exact=1
                     ->  Bitmap Index Scan on follows_start_idx (actual rows=6.00 loops=1)
                           Index Cond: ((start = a.id) AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
                           Index Searches: 6
         ->  Index Only Scan using account_pkey on account b (actual rows=1.00 loops=6)
               Index Cond: (id = r1."end")
               Heap Fetches: 6
               Index Searches: 6
```

> [!NOTE]
> Read a variable-length or shortest-path plan in the default text format. `Dijkstra` is the
> one of the three whose plan also reads correctly through `EXPLAIN (FORMAT JSON)`.

## Plan nodes for a traversal {#plan-nodes-for-a-traversal}

A fixed-length pattern needs no special node: it is scans and joins, as above. The nodes below
appear for the things SQL has no operator for.

`Graph VLE` is a variable-length edge, and it names the edge label and the range:

```cypher
SET graph_path = moviekb;
EXPLAIN (COSTS OFF) MATCH (a:movie {title: 'The Matrix'})-[r:related_to*1..3]->(b:movie) RETURN b.title;
```

```
                          QUERY PLAN                          
--------------------------------------------------------------
 Nested Loop
   ->  Seq Scan on movie a
         Filter: (properties.'title' = '"The Matrix"'::jsonb)
   ->  Hash Join
         Hash Cond: (r."end" = b.id)
         ->  Subquery Scan on r
               ->  Graph VLE on related_to [1..3]
                     ->  Result
         ->  Hash
               ->  Seq Scan on movie b
```

`on related_to` is the line to read. An untyped variable-length edge becomes
`Graph VLE on ag_edge`, which walks every edge label in the graph at every hop. That is the
single biggest avoidable cost in a path query. [Paths](/agensgraph/querying/paths/#what-a-path-costs) has the
comparison.

`Shortestpath VLE [min..max]` is a `shortestpath` or `allshortestpaths`, sitting above two
`Hash2Side` nodes: the two frontiers of a bidirectional search, one growing from each end.

`Dijkstra` is a weighted search. Its child is the scan it expands through, so an index on the
edge label's `start` column is what it walks.

`Graph Create`, `Graph Set` and `Graph Delete` are the write nodes:

```cypher
SET graph_path = perflab;
EXPLAIN (COSTS OFF) MATCH (a:account {handle: 'user42'}) SET a.seen = 1;
```

```
                          QUERY PLAN                           
---------------------------------------------------------------
 Graph Set
   ->  Index Scan using account_handle_idx on account a
         Index Cond: (properties.'handle' = '"user42"'::jsonb)
```

A write node marked **`eager`** has to finish before anything above it runs, because something
above it reads what the write changed:

```cypher
EXPLAIN (COSTS OFF)
MATCH (a:account {handle: 'user42'}) SET a.seen = 1
WITH a MATCH (a)-[r:follows]->(b:account) RETURN count(b);
```

```
                                                                  QUERY PLAN                                                                   
-----------------------------------------------------------------------------------------------------------------------------------------------
 Aggregate
   ->  Nested Loop
         ->  Nested Loop
               ->  Subquery Scan on _agens_default_s
                     ->  Graph Set eager
                           ->  Index Scan using account_handle_idx on account a
                                 Index Cond: (properties.'handle' = '"user42"'::jsonb)
               ->  Index Only Scan using follows_start_idx on follows r
                     Index Cond: ((start = (_agens_default_s.a).id) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
         ->  Index Only Scan using account_pkey on account b
               Index Cond: (id = r."end")
```

Eagerness is what makes [a write visible to a later read in the same
statement](/agensgraph/querying/writing/#reading-what-you-just-wrote). It costs a materialisation of the write's
output, bounded by `eager_mem`. `MERGE` is always eager, and so is any `SET`, `REMOVE` or
`DELETE` that is not the last clause in its statement.

The names beginning `_agens_default_s` are the generated aliases for a pipeline's stages,
roughly one per `WITH`. They are stable within a plan and are not something to tune.

## Statistics on edge labels {#statistics-on-edge-labels}

This is the first thing to check on any new graph, and it is worth more than any index.

The cost of a traversal is a product of degrees: how many edges leave the vertices you
started from, how many leave those you reached, and so on. Statistics on an edge label's
`start` and `end` columns describe those degrees. AgensGraph sets both columns' statistics
target to the maximum, 1,000, when the label is created:

```sql
SELECT attname, attstattarget FROM pg_attribute
WHERE attrelid = 'perflab.follows'::regclass AND attnum > 0 ORDER BY attnum;
```

```
  attname   | attstattarget 
------------+---------------
 id         |              
 start      |          1000
 end        |          1000
 properties |              
```

A target is not a sample. Until something analyses the label there is nothing there:

```sql
SELECT count(*) AS stats_rows FROM pg_stats WHERE schemaname = 'perflab' AND tablename = 'follows';
```

```
 stats_rows 
------------
          0
```

And the estimates are guesses. Here is a two-hop count on a freshly loaded graph:

```cypher
EXPLAIN MATCH (a:account {handle: 'user42'})-[r1:follows]->(b:account)-[r2:follows]->(c:account) RETURN count(c);
```

```
                                                                                                    QUERY PLAN                                                                                                    
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Aggregate  (cost=10088.00..10088.01 rows=1 width=32)
   ->  Hash Join  (cost=677.81..9622.10 rows=186358 width=8)
         Hash Cond: (r2."end" = c.id)
         ->  Nested Loop  (cost=20.81..8475.81 rows=186358 width=24)
               ->  Nested Loop  (cost=20.39..779.08 rows=433 width=16)
                     ->  Index Scan using account_handle_idx on account a  (cost=0.29..8.30 rows=1 width=8)
                           Index Cond: (properties.'handle' = '"user42"'::jsonb)
                     ->  Bitmap Heap Scan on follows r1  (cost=20.10..766.44 rows=433 width=24)
                           Recheck Cond: ((a.id = start) AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
                           ->  Bitmap Index Scan on follows_start_idx  (cost=0.00..20.00 rows=433 width=0)
                                 Index Cond: ((start = a.id) AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
               ->  Index Scan using follows_start_idx on follows r2  (cost=0.42..13.48 rows=430 width=24)
                     Index Cond: ((start = r1."end") AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
                     Filter: (r1.id <> id)
         ->  Hash  (cost=407.00..407.00 rows=20000 width=8)
               ->  Seq Scan on account c  (cost=0.00..407.00 rows=20000 width=8)
```

433 edges out of one account, 186,358 two-hop pairs, and a hash over all 20,000 accounts to
resolve the far endpoint. Now analyse the edge label:

```sql
ANALYZE perflab.follows;
```

```cypher
EXPLAIN MATCH (a:account {handle: 'user42'})-[r1:follows]->(b:account)-[r2:follows]->(c:account) RETURN count(c);
```

```
                                                                                                    QUERY PLAN                                                                                                    
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Aggregate  (cost=51.17..51.18 rows=1 width=32)
   ->  Nested Loop  (cost=5.52..51.08 rows=36 width=8)
         ->  Nested Loop  (cost=5.23..39.78 rows=36 width=24)
               ->  Nested Loop  (cost=4.81..35.54 rows=6 width=16)
                     ->  Index Scan using account_handle_idx on account a  (cost=0.29..8.30 rows=1 width=8)
                           Index Cond: (properties.'handle' = '"user42"'::jsonb)
                     ->  Bitmap Heap Scan on follows r1  (cost=4.52..27.18 rows=6 width=24)
                           Recheck Cond: ((a.id = start) AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
                           ->  Bitmap Index Scan on follows_start_idx  (cost=0.00..4.52 rows=6 width=0)
                                 Index Cond: ((start = a.id) AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
               ->  Index Scan using follows_start_idx on follows r2  (cost=0.42..0.65 rows=6 width=24)
                     Index Cond: ((start = r1."end") AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
                     Filter: (r1.id <> id)
         ->  Index Only Scan using account_pkey on account c  (cost=0.29..0.31 rows=1 width=8)
               Index Cond: (id = r2."end")
```

6 edges, 36 pairs, an index-only scan for the far endpoint, and an estimated cost of 51
against 10,088. And 36 is exactly right:

```cypher
MATCH (a:account {handle: 'user42'})-[r1:follows]->(b:account)-[r2:follows]->(c:account) RETURN count(c) AS pairs;
```

```
 pairs 
-------
    36
```

The rule that follows: **after any bulk load, `ANALYZE` the edge labels, not just the vertex
labels.** Autovacuum gets there eventually, but "eventually" is after the first users have run
the query. A graph whose degrees change shape, when a hub vertex arrives, is worth
re-analysing explicitly rather than waiting for the row-count threshold.

## The settings that change plan shape {#the-settings-that-change-plan-shape}

Five settings affect how a graph query is planned. These are their real values, read from
`pg_settings`:

| Setting | Default | Scope | What it does |
| --- | --- | --- | --- |
| `enable_eager` | `on` | session | When off, a statement that needs an eager plan is refused instead of planned. |
| `eager_mem` | 4 MB | session | Memory an eager node may use before spilling. |
| `enable_graph_endpoint_elision` | `on` | session | Removes the scan for a pattern endpoint whose value the query never reads. |
| `enable_property_promotion` | `on` | session | Resolves a Cypher property read to a promoted typed column when one exists. |
| `auto_gather_graphmeta` | `off` | superuser | Maintains `ag_graphmeta` edge connectivity, which lets the planner prune unreachable labels from a scan. |

> [!NOTE]
> `postgresql.conf.sample` states the wrong default for `enable_eager` and
> `enable_multiple_update`. Both are on. Read `pg_settings`, not the sample file.

None of these is a knob to turn in production. Four are on already, and the fifth is a
decision about maintaining a catalog. Know them for diagnosis: turning one off tells you
whether it is responsible for a plan you did not expect.

### Endpoint elision {#endpoint-elision}

An endpoint whose value the query never reads is not scanned at all. `b` here is bound and
labelled, and never projected:

```cypher
EXPLAIN (COSTS OFF) MATCH (a:account)-[r:follows]->(b:account) RETURN a.handle;
```

```
                                                                            QUERY PLAN                                                                             
-------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Hash Join
   Hash Cond: (r.start = a.id)
   ->  Seq Scan on follows r
         Filter: (("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid) AND (start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid))
   ->  Hash
         ->  Seq Scan on account a
```

One join, and `(b:account)` survives only as a range test on the edge's `"end"` column. Switch
the elision off and the second scan and join come back:

```cypher
SET enable_graph_endpoint_elision = off;
EXPLAIN (COSTS OFF) MATCH (a:account)-[r:follows]->(b:account) RETURN a.handle;
RESET enable_graph_endpoint_elision;
```

```
                                                                               QUERY PLAN                                                                                
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Hash Join
   Hash Cond: (r."end" = b.id)
   ->  Hash Join
         Hash Cond: (r.start = a.id)
         ->  Seq Scan on follows r
               Filter: ((start >= '3.0'::graphid) AND (start <= '3.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
         ->  Hash
               ->  Seq Scan on account a
   ->  Hash
         ->  Seq Scan on account b
```

The lesson is not about the setting. Projecting an endpoint you do not need costs a scan and a
join, every time. So keep a `RETURN` to what the caller reads.

### Scan pruning from ag_graphmeta {#scan-pruning-from-ag_graphmeta}

`ag_graphmeta` holds one row per start-label, edge-label, end-label triple that actually
occurs in the graph, with how many edges make it up. With that, an unlabelled pattern endpoint
can be narrowed to the labels the edge is known to reach. It is
maintained only when `auto_gather_graphmeta` is on, so by default an unlabelled endpoint scans
the whole `ag_vertex` family:

```cypher
EXPLAIN (COSTS OFF) MATCH (n)-[r:follows]->(m) RETURN n, m;
```

```
                    QUERY PLAN                     
---------------------------------------------------
 Hash Join
   Hash Cond: (m.id = r."end")
   ->  Append
         ->  Seq Scan on ag_vertex m_1
         ->  Seq Scan on account m_2
   ->  Hash
         ->  Hash Join
               Hash Cond: (n.id = r.start)
               ->  Append
                     ->  Seq Scan on ag_vertex n_1
                     ->  Seq Scan on account n_2
               ->  Hash
                     ->  Seq Scan on follows r
```

Turn gathering on and both `Append`s collapse. Gathering builds a baseline for every graph in
the database, so do it deliberately:

```cypher
SET auto_gather_graphmeta = on;
EXPLAIN (COSTS OFF) MATCH (n)-[r:follows]->(m) RETURN n, m;
RESET auto_gather_graphmeta;
```

```
               QUERY PLAN                
-----------------------------------------
 Hash Join
   Hash Cond: (r."end" = m.id)
   ->  Hash Join
         Hash Cond: (r.start = n.id)
         ->  Seq Scan on follows r
         ->  Hash
               ->  Seq Scan on account n
   ->  Hash
         ->  Seq Scan on account m
```

`follows` only ever runs `account` → `account`, so the two unlabelled endpoints can only be
accounts. On a graph with many labels this is the difference between one scan per endpoint and
one per label. It costs maintenance on every edge write, plus a rescan whenever the baseline
is invalidated.

Two labels are all this example has, so the saving here is small. The shape of it is the
point. `pg_catalog.ag_graphmeta` holds the counts and `ag_graph.graphmeta_valid` gates their
use. See [Graph metadata](/agensgraph/system-catalogs/graph-metadata/).

The plainest alternative is to name the label in the pattern. `MATCH (n:account)-[r:follows]->(m:account)`
needs no catalog at all.

### Forbidding an eager plan {#forbidding-an-eager-plan}

`enable_eager = off` does not produce a different plan. It refuses to produce one:

```cypher
SET enable_eager = off;
EXPLAIN (COSTS OFF)
MATCH (a:account {handle: 'user42'}) SET a.seen = 1
WITH a MATCH (a)-[r:follows]->(b:account) RETURN count(b);
RESET enable_eager;
```

```
ERROR:  eagerness plan is not allowed.
```

Use it to find out which statement in a workload depends on eagerness. Do not run with it
off. Eagerness is a correctness requirement for such a statement rather than a cost choice,
so there is no cheaper plan to fall back to and the server raises an error instead.

### Resolution to a promoted column {#resolution-to-a-promoted-column}

`enable_property_promotion = off` sends a property read back to the `jsonb` bag even where a
typed column exists. The plan changes and the answers do not, because the value is in both
places. It is the way to establish whether a promotion is behind a plan you did not expect,
without dropping the column. [Turning resolution
off](/agensgraph/querying/typed-columns/#turning-resolution-off) has the before and after.

## What to do, in order {#what-to-do-in-order}

1. **`ANALYZE` every label the query touches, edge labels included.** Nothing else on this
   list matters until this is done.
2. **Check the anchor.** A traversal wants one selective, indexed starting point. `EXPLAIN`
   should show an `Index Cond`, not a `Filter`, on the property that picks it —
   [Indexes and constraints](/agensgraph/querying/indexes-and-constraints/) says which predicates can.
3. **Name the edge label in every variable-length pattern.** `Graph VLE on ag_edge` in a plan
   points at the query rather than at the planner.
4. **Bound the length** of a variable-length pattern.
5. **Project only what the caller reads**, so unused endpoints elide.
6. **Consider promoting a property** you filter, join or order on constantly —
   [Promoting a property to a column](/agensgraph/querying/typed-columns/#when-to-promote).
7. **Then look at resources.** [Configuration](/agensgraph/operations/configuration/).

## Clean up {#clean-up}

```cypher
DROP GRAPH perflab CASCADE;
```

```sql
DROP TABLE seed_account;
DROP TABLE seed_follows;
```

## Where to go next {#where-to-go-next}

* [Indexes and constraints](/agensgraph/querying/indexes-and-constraints/) — which predicates an index can serve.
* [Paths](/agensgraph/querying/paths/#what-a-path-costs) — the traversal-specific version of this page.
* [Promoting a property to a column](/agensgraph/querying/typed-columns/) — when the read itself is the cost.
* [Configuration](/agensgraph/operations/configuration/) — memory, I/O and autovacuum.
