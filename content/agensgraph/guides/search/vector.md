---
title: Vector search
linkTitle: Vector search
description: AgensGraph is built on PostgreSQL, so the pgvector extension adds vector similarity search to a graph
  directly.
type: docs
weight: 20
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/guides/search/vector.html
upstream_source: agensgraph
upstream_modified: true
---


## Overview {#overview}

AgensGraph is built on PostgreSQL, so the [pgvector](https://github.com/pgvector/pgvector)
extension adds vector similarity search to a graph directly. Embeddings then live next to
your graph data, and one database can combine semantic (vector) search with Cypher graph
traversal. That is the foundation for retrieval-augmented generation (RAG) and *GraphRAG*
applications.

Vector search matches by *meaning* rather than by words: two texts can be close in vector
space even when they share no vocabulary. That is its strength over keyword matching, which
is [full-text search](/agensgraph/guides/search/full-text/).

[Hybrid Search](/agensgraph/guides/search/hybrid/) covers combining the two. The examples in all three pages use the
same set of movies, so you can compare the behaviour directly.

An embedding is stored as a numeric array **property** on a vertex or edge. Properties are
`jsonb`, so the array is kept as a JSON array. A `::vector(n)` cast turns it into pgvector's
`vector` type wherever a vector operation needs one.

That cast happens on every read. That is fine for a few thousand rows and wasteful at scale.
From 2.18 you can [promote the property to a real `vector`
column](/agensgraph/querying/typed-columns/) instead.

The cast then happens once at write time, and an HNSW index can be built on the column
itself. The queries on this page keep working unchanged and keep using the index, because a
leftover `::vector(n)` on a promoted column is folded away.

Two things change when you promote.

The value's *type*. A promoted `d.emb` comes back as `vector`, where an unpromoted one comes
back as `jsonb`, so a client that parses the JSON form needs updating.

The shape of the index. Over a promoted column it is an ordinary column index rather than an
index over a cast expression, which makes it the form to prefer for an index you dump and
restore.

## Installing pgvector {#installing-pgvector}

[pgvector](https://github.com/pgvector/pgvector) is a separate extension that must be built and installed against your AgensGraph installation. Once it is available, enable it per database:

```sql
CREATE EXTENSION vector;
```

## Example data {#example-data}

The examples use [the example dataset](/agensgraph/get-started/example-dataset/): 18 films, each
with a `plot` and a four-dimensional `embedding` of that plot. Load it before going further.

Real embeddings come from a model, such as `text-embedding-3-small` or a local
`sentence-transformers` model, and they have hundreds of dimensions. These are reduced to four
so the geometry stays readable on the page.

## Similarity search {#similarity-search}

pgvector provides a set of distance operators and matching functions. Cast both operands to `vector(n)` and order by the distance.

| Operator | Function          | Distance              | HNSW operator class |
| -------- | ----------------- | --------------------- | ------------------- |
| `<=>`    | `cosine_distance` | cosine distance       | `vector_cosine_ops` |
| `<->`    | `l2_distance`     | Euclidean (L2)        | `vector_l2_ops`     |
| `<#>`    | `inner_product`   | (negative) inner product | `vector_ip_ops`  |
| `<+>`    | `l1_distance`     | taxicab (L1)          | `vector_l1_ops`     |

Find the movies whose plots are closest to a query vector (cosine distance). Here the query is the embedding of *The Matrix*'s plot, so the search returns the films most similar in meaning:

```cypher
MATCH (m:movie)
RETURN m.title AS title
ORDER BY m.embedding::vector(4) <=> '[-0.07594558, 0.04081754, 0.29592122, -0.11921061]'::vector(4)
LIMIT 4;
```

```
           title
----------------------------
 "The Matrix"
 "The Matrix Reloaded"
 "The Matrix Resurrections"
 "Total Recall"
(4 rows)
```

The first three results are the obvious sequels, but the fourth is the interesting one.
*Total Recall*'s plot is *"a construction worker discovers that his memories have been
implanted"*. It shares **no keywords** with *The Matrix*'s *"a hacker … a simulated world
controlled by machines"*.

Vector search still ranks it fourth, because both films are about a character discovering that
their reality is fabricated. A keyword search could never connect the two.

Semantic search captures precisely that, and lexical search cannot. Compare the [Full Text
Search](/agensgraph/guides/search/full-text/) results on the same data, and see [Hybrid Search](/agensgraph/guides/search/hybrid/) for
combining both.

> `ORDER BY` may reference the distance expression even though it is not in the `RETURN` list (AgensGraph 2.17 and later). Returning only `title` keeps the output clean and, more importantly, lets the HNSW index serve the ordering. Returning the raw distance would convert it to `jsonb` and prevent the index from being used.

The function form is convenient for comparing against another stored vector, such as "movies
most similar to *The Terminator*". It saves writing the query vector by hand:

```cypher
MATCH (m:movie), (q:movie {title: 'The Terminator'})
RETURN m.title AS title
ORDER BY m.embedding::vector(4) <=> q.embedding::vector(4)
LIMIT 4;
```

```
            title
----------------------------
 "The Terminator"
 "Terminator 2: Judgment Day"
 "Minority Report"
 "Blade Runner"
(4 rows)
```

## Indexing with HNSW {#indexing-with-hnsw}

Without an index, every similarity query scans all rows and computes the distance for each. For larger data sets, create an HNSW index so the planner can use an index scan. Because the indexed value is a cast expression, use a **property index**:

```sql
CREATE PROPERTY INDEX ON movie
    USING hnsw ((embedding::vector(4)) vector_cosine_ops);
```

Match the operator class to the distance you query with (`vector_cosine_ops` for `<=>`, `vector_l2_ops` for `<->`, and so on). The earlier similarity query then uses the index:

```psql
EXPLAIN
MATCH (m:movie)
RETURN m.title AS title
ORDER BY m.embedding::vector(4) <=> '[-0.07594558, 0.04081754, 0.29592122, -0.11921061]'::vector(4)
LIMIT 4;
```

```
 Limit
   ->  Index Scan using movie_embedding_idx on movie m
         Order By: ((properties.'embedding'::text)::vector(4) <=> '[...]'::vector(4))
```

> On this 18-row demo the planner may still prefer a sequential scan because it is cheaper for so few rows; add `SET enable_seqscan = off` to observe the index plan. On a real corpus the planner chooses the index automatically.

> HNSW property indexes over a `::vector(n)` cast require AgensGraph 2.17 or later.

## Indexing a promoted column {#indexing-a-promoted-column}

The index above is built over a cast expression. Promoting the property removes the cast, so
the index becomes an ordinary one over a column.

Promotion gives the property a real typed column beside the jsonb bag, filled at write time.
The column name is what you are declaring; the property it mirrors is named by the same word:

```cypher
DROP PROPERTY INDEX movie_embedding_idx;
ALTER VLABEL movie ADD COLUMN embedding vector(4) GENERATED;
```

`GENERATED` on its own mirrors the property that shares the column's name, here `embedding`.
Write `GENERATED (sourceKey)` when the column should be called something else &mdash;
`ALTER VLABEL movie ADD COLUMN emb vector(4) GENERATED (embedding)` stores the same property
in a column named `emb`. Either way **the query keeps naming the property, never the column**:
resolution is by property key, and the column name never appears in Cypher. [Promoting a
property to a column](/agensgraph/querying/typed-columns/) is the full treatment.

The index is then an ordinary one over a column, with no cast and no parentheses:

```cypher
CREATE PROPERTY INDEX ON movie USING hnsw (embedding vector_cosine_ops);
```

Every query on this page still works, unchanged. A leftover `::vector(4)` on a promoted
column is folded away, so `m.embedding` and `m.embedding::vector(4)` produce the same plan:

```psql
EXPLAIN (COSTS OFF)
MATCH (m:movie)
RETURN m.title AS title
ORDER BY m.embedding <=> '[-0.07594558, 0.04081754, 0.29592122, -0.11921061]'::vector(4)
LIMIT 4;
```

```
 Limit
   ->  Index Scan using movie_embedding_idx on movie m
         Order By: (embedding <=> '[-0.07594558,0.04081754,0.2959212,-0.11921061]'::vector(4))
```

> [!IMPORTANT]
> Drop an expression index before promoting the key it reads, as above. A property index over
> an expression is built against the jsonb bag, and a query over a promoted key reads the
> column, so the two no longer meet. See [An expression property index is built over the
> bag](/agensgraph/querying/typed-columns/#an-expression-property-index-is-built-over-the-bag).

The value's type changes with promotion: `m.embedding` now comes back as `vector`, where the
unpromoted property came back as `jsonb`.

## GraphRAG {#graphrag}

Vector search inside a graph database has a particular strength: a semantic match can be the
*starting point* of a graph traversal.

A typical GraphRAG retrieval does two things in one query. It finds the items most relevant to
a question by vector similarity, then expands along relationships to gather connected context
for the language model.

The [example dataset](/agensgraph/get-started/example-dataset/) already carries `related_to` edges
between films: franchise sequels and thematically linked titles. So the traversal below has
something to follow.

At query time, embed the user's question with the same model used for the plots. Then run a
single Cypher query that retrieves the closest movies and expands to their neighbors. Here
the question embedding is *The Matrix*'s vector:

```cypher
MATCH (seed:movie)
WITH seed
ORDER BY seed.embedding::vector(4) <=> '[-0.07594558, 0.04081754, 0.29592122, -0.11921061]'::vector(4)
LIMIT 2
MATCH (seed)-[:related_to]-(ctx:movie)
RETURN seed.title AS seed, collect(DISTINCT ctx.title) AS related_context;
```

```
         seed          |                      related_context
-----------------------+-----------------------------------------------------------
 "The Matrix"          | ["The Matrix Reloaded", "The Terminator", "Total Recall"]
 "The Matrix Reloaded" | ["The Matrix", "The Matrix Revolutions"]
(2 rows)
```

The `WITH … ORDER BY … LIMIT 2` selects the two movies that best match the question by vector
similarity. Those are the *seeds*. The second `MATCH` follows `related_to` edges from each
seed to collect neighboring films.

The combined set is the seeds plus their graph neighbors. It forms a richer context than
vector search alone, and it can be passed to a language model to generate the final answer.

This pattern generalizes. Seeds can be expanded over multiple hops, filtered by edge type or
properties, or joined to other labels (people, studios, sources) to assemble exactly the
context a RAG pipeline needs.

If you would rather a framework assembled it, [AI and LLM
integrations](/agensgraph/drivers/ai-integrations/) lists the libraries that do.
