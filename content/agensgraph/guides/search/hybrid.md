---
title: Hybrid search
linkTitle: Hybrid search
description: Vector search matches by meaning.
type: docs
weight: 40
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/guides/search/hybrid.html
upstream_source: agensgraph
upstream_modified: true
---


## Overview {#overview}

[Vector search](/agensgraph/guides/search/vector/) matches by *meaning*. [Full-text search](/agensgraph/guides/search/full-text/) matches by
*words*. Each is strong where the other is weak.

Vector search finds paraphrases and related concepts, but it can miss an exact term such as a
product code, a name or a rare keyword. Full-text search nails exact terms, but it misses
synonyms and intent.

**Hybrid search** runs both and merges their results, so retrieval is semantically aware and
lexically precise. AgensGraph provides both [pgvector](https://github.com/pgvector/pgvector)
and PostgreSQL full-text search in one database, so a hybrid query is a single statement over
the same graph.

> This page is about *search-result fusion*. It is unrelated to the [Combining SQL and Cypher](/agensgraph/querying/combining-sql-and-cypher/) page, which is about mixing SQL and Cypher in one statement.

## Reciprocal Rank Fusion {#reciprocal-rank-fusion}

The two searches produce scores on different scales (cosine distance vs. `ts_rank`), so they
cannot be added. **Reciprocal Rank Fusion (RRF)** avoids the problem by combining *ranks*
rather than scores.

Each result contributes `1 / (k + rank)` from each search it appears in, and the contributions
are summed:

```
score(d) = 1/(k + rank_vector(d)) + 1/(k + rank_fulltext(d))
```

`k` is a smoothing constant that limits how much the very top ranks dominate. 60 is the
commonly used default. A document that ranks well in *either* search scores reasonably; a
document that ranks well in *both* scores highest.

## Example data {#example-data}

The examples use [the example dataset](/agensgraph/get-started/example-dataset/): 18 films, each
with a `plot` and a four-dimensional `embedding` of that plot. Load it before going further.

Real embeddings come from a model, such as `text-embedding-3-small` or a local
`sentence-transformers` model, and they have hundreds of dimensions. These are reduced to four
so the geometry stays readable on the page.

## The hybrid query {#the-hybrid-query}

Reciprocal Rank Fusion needs a *rank* from each search, and SQL window functions produce one.
So the fusion is a SQL query whose graph data comes from Cypher `MATCH` subqueries.

One subquery ranks the movies by vector distance and another by full-text relevance.
`row_number()` turns each ordered result into a rank, and the outer query sums the reciprocal
ranks. Each subquery returns only the vertex id and orders by its ranking expression, which it
does not return. So the vector and full-text property indexes can serve the ordering and the
filtering directly.

The query below looks for films in the vein of *The Matrix* that also literally mention
`machines`. The vector query is that film's plot embedding:

```psql
WITH vec AS (
    SELECT id, row_number() OVER () AS rnk
    FROM (MATCH (m:movie)
          RETURN id(m) AS id
          ORDER BY m.embedding::vector(4) <=> '[-0.07594558, 0.04081754, 0.29592122, -0.11921061]'::vector(4)
          LIMIT 10) v
),
fts AS (
    SELECT id, row_number() OVER () AS rnk
    FROM (MATCH (m:movie)
          WHERE to_tsvector('english', m.plot::text) @@ websearch_to_tsquery('english', 'machines')
          RETURN id(m) AS id
          ORDER BY ts_rank(to_tsvector('english', m.plot::text),
                           websearch_to_tsquery('english', 'machines')) DESC) f
)
SELECT m.title AS title,
       round((COALESCE(1.0/(60 + vec.rnk), 0)
            + COALESCE(1.0/(60 + fts.rnk), 0))::numeric, 5) AS rrf_score,
       vec.rnk AS vec_rank,
       fts.rnk AS fts_rank
FROM (MATCH (m:movie) RETURN id(m) AS id, m.title AS title) m
LEFT JOIN vec ON vec.id = m.id
LEFT JOIN fts ON fts.id = m.id
WHERE vec.id IS NOT NULL OR fts.id IS NOT NULL
ORDER BY rrf_score DESC
LIMIT 6;
```

```
            title             | rrf_score | vec_rank | fts_rank
------------------------------+-----------+----------+----------
 "The Matrix"                 |   0.03279 |        1 |        1
 "The Matrix Reloaded"        |   0.03226 |        2 |        2
 "The Matrix Resurrections"   |   0.03150 |        3 |        4
 "The Matrix Revolutions"     |   0.03080 |        7 |        3
 "Total Recall"               |   0.01563 |        4 |
 "Avatar"                     |   0.01538 |        5 |
(6 rows)
```

Fusion does two things at once here. *Total Recall* (vector rank 4) never uses the word
`machines`, so the full-text arm misses it entirely. It survives in the result anyway, because
vector search recognized it as a *false-reality* story like *The Matrix*.

*The Matrix Revolutions* goes the other way. It is only the 7th-nearest vector, low enough to
fall outside a vector-only top five, but the full-text arm ranks it 3rd because its plot
literally says *machines*. Fusion pulls it back up.

The films that satisfy **both** arms (*The Matrix*, *Reloaded*, *Resurrections*) take the top
spots. Vector search contributes recall, full-text search contributes precision, and RRF
blends the two.

## Indexing both arms {#indexing-both-arms}

Each arm of the query is an ordinary similarity or full-text search, so the same **property
indexes** described in [Vector Search](/agensgraph/guides/search/vector/) and [Full Text Search](/agensgraph/guides/search/full-text/)
accelerate it. Those are an HNSW index over the embedding and a GIN index over the plain-text
plot:

```sql
CREATE PROPERTY INDEX ON movie
    USING hnsw ((embedding::vector(4)) vector_cosine_ops);
CREATE PROPERTY INDEX ON movie
    USING gin ((to_tsvector('english', plot::text)));
```

Each Cypher subquery returns only the id and orders by its raw ranking expression, so the
planner can serve each arm from its index. The HNSW index orders the vector candidates and the
GIN index filters the full-text matches, so neither search scans the whole label.

The relevant parts of `EXPLAIN` for the fusion query are:

```
 ...
 ->  Subquery Scan on vec
       ->  Limit
             ->  Index Scan using movie_embedding_idx on movie m
                   Order By: ((properties.'embedding'::text)::vector(4) <=> '[...]'::vector(4))
 ...
 ->  Subquery Scan on fts
       ->  Bitmap Heap Scan on movie m
             Recheck Cond: (to_tsvector('english', (properties.'plot'::text)::text) @@ '...'::tsquery)
             ->  Bitmap Index Scan on movie_plot_idx
```

> On a tiny demo data set the planner may still choose a sequential scan because it is cheaper than an index for a handful of rows; add `SET enable_seqscan = off` to observe the index plan. On a real corpus the planner selects the indexes automatically.

Both indexes above are expressions over a property. If you [promote either
property](/agensgraph/querying/typed-columns/) to a typed column, rebuild that arm's index: an
expression property index is built over the jsonb bag, while a query over a promoted key reads
the column. The embedding arm then becomes a plain index over the column, and the full-text
arm a SQL index over it:

```cypher
ALTER VLABEL movie ADD COLUMN embedding vector(4) GENERATED;
CREATE PROPERTY INDEX ON movie USING hnsw (embedding vector_cosine_ops);
```

The fusion query itself does not change. [Vector search](/agensgraph/guides/search/vector/#indexing-a-promoted-column)
and [full-text search](/agensgraph/guides/search/full-text/#indexing-a-promoted-column) each show their side.

## Tuning {#tuning}

* **`k` constant** — larger values flatten the contribution of the top ranks; smaller values let the first few results dominate. 60 is a reasonable starting point.
* **Weighting** — to favor one method, multiply its term, e.g. `1.5 * COALESCE(1.0/(60 + vec.rnk), 0)` to lean semantic.
* **Candidate depth** — the `LIMIT` inside each CTE controls how deep each search reaches before fusion; increase it for higher recall at some cost in latency.

## GraphRAG {#graphrag}

Hybrid retrieval is the strongest starting point for a graph traversal. Rank the films by both
semantic similarity and keyword relevance (RRF), then expand the top results along
relationships to assemble context for a language model.

Reciprocal Rank Fusion needs SQL window functions, but every piece that touches the graph is
written as a Cypher `MATCH` subquery in the `FROM` clause: each retrieval *and* the expansion.
That is the [Combining SQL and Cypher](/agensgraph/querying/combining-sql-and-cypher/) mechanism.
The query stays graph-native and reuses the property indexes built above.

The [example dataset](/agensgraph/get-started/example-dataset/) already carries `related_to` edges
between films: franchise sequels and thematically linked titles. So the traversal below has
something to follow.

Here the vector arm retrieves films like *The Matrix* while the full-text arm matches the
keyword `memories`. The SQL `row_number()` turns each ordered result into a rank. The `seeds`
CTE fuses the two with RRF and keeps the top two, and a final Cypher traversal collects each
seed's neighbors:

```psql
WITH vec AS (
    SELECT id, row_number() OVER () AS rnk
    FROM (MATCH (m:movie)
          RETURN id(m) AS id
          ORDER BY m.embedding::vector(4) <=> '[-0.07594558, 0.04081754, 0.29592122, -0.11921061]'::vector(4)
          LIMIT 10) v
),
fts AS (
    SELECT id, row_number() OVER () AS rnk
    FROM (MATCH (m:movie)
          WHERE to_tsvector('english', m.plot::text) @@ websearch_to_tsquery('english', 'memories')
          RETURN id(m) AS id
          ORDER BY ts_rank(to_tsvector('english', m.plot::text),
                           websearch_to_tsquery('english', 'memories')) DESC) f
),
seeds AS (
    SELECT m.id, m.title,
           COALESCE(1.0/(60 + vec.rnk), 0) + COALESCE(1.0/(60 + fts.rnk), 0) AS score
    FROM (MATCH (m:movie) RETURN id(m) AS id, m.title AS title) m
    LEFT JOIN vec ON vec.id = m.id
    LEFT JOIN fts ON fts.id = m.id
    WHERE vec.id IS NOT NULL OR fts.id IS NOT NULL
    ORDER BY score DESC
    LIMIT 2
)
SELECT s.title AS seed,
       jsonb_agg(DISTINCT ctx.title) AS expanded_context
FROM seeds s
LEFT JOIN (MATCH (a:movie)-[:related_to]-(b:movie)
           RETURN id(a) AS aid, b.title AS title) ctx ON ctx.aid = s.id
GROUP BY s.title
ORDER BY s.title;
```

```
      seed      |                   expanded_context
----------------+-----------------------------------------------------------
 "The Matrix"   | ["The Matrix Reloaded", "The Terminator", "Total Recall"]
 "Total Recall" | ["Inception", "The Matrix"]
(2 rows)
```

Fusion changes which films seed the traversal. *Total Recall* is only the 4th-nearest vector
to *The Matrix*, so vector-only seeding would have expanded *The Matrix* and *The Matrix
Reloaded*. But the keyword `memories` matches *Total Recall* exactly, and RRF lifts it into the
top two.

With *Total Recall* among the seeds, the traversal follows its `related_to` edge and reaches
*Inception*: context that neither arm alone would have surfaced.

The result is hybrid-ranked seeds plus their graph neighborhood. It is the richest context of
the three approaches, drawing on semantic similarity, exact keywords, and explicit
relationships at once.

The frameworks in [AI and LLM integrations](/agensgraph/drivers/ai-integrations/) build this
same shape for you, and several expose it as one retriever.
