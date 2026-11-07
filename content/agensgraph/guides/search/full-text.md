---
title: Full-text search
linkTitle: Full-text search
description: AgensGraph is built on PostgreSQL and inherits its full-text search engine, so you can run linguistic
  keyword search directly over text stored in graph properties.
type: docs
weight: 30
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/guides/search/full-text.html
upstream_source: agensgraph
upstream_modified: true
---


## Overview {#overview}

AgensGraph is built on PostgreSQL and inherits its full-text search engine, so you can run
linguistic keyword search directly over text stored in graph properties. Full-text search
normalizes documents and queries into lexemes (stemming, stop-word removal, case folding).
That makes it well suited to *lexical* retrieval: matching the words a user typed.

It is the natural complement to [vector search](/agensgraph/guides/search/vector/), which matches by *meaning*.
[Hybrid Search](/agensgraph/guides/search/hybrid/) covers combining the two. All three pages use the same movies, so
you can compare the results directly.

A graph property is stored as `jsonb`, so a text property is cast to `text` (with `::text`) before being converted to a `tsvector`.

## Example data {#example-data}

The examples use [the example dataset](/agensgraph/get-started/example-dataset/): 18 films, each
with a `plot` and a four-dimensional `embedding` of that plot. Load it before going further.

Real embeddings come from a model, such as `text-embedding-3-small` or a local
`sentence-transformers` model, and they have hundreds of dimensions. These are reduced to four
so the geometry stays readable on the page.

## Searching a text property {#searching-a-text-property}

Convert the property to a `tsvector` with `to_tsvector`, parse the user's input with one of
the `*_to_tsquery` functions, and match them with the `@@` operator. `websearch_to_tsquery`
accepts a forgiving, web-style syntax: quoted phrases, `OR`, and `-` to exclude a term. That
makes it a good default for user input.

```cypher
MATCH (m:movie)
WHERE to_tsvector('english', m.plot::text) @@ websearch_to_tsquery('english', 'machines')
RETURN m.title AS title;
```

```
           title
----------------------------
 "The Matrix"
 "The Matrix Reloaded"
 "The Matrix Revolutions"
 "The Matrix Resurrections"
(4 rows)
```

The query is matched against lexemes, not raw text. `machines` is reduced to the stem
`machin`, so the singular `machine` would match exactly the same rows.

Look also at what is *not* returned. *Total Recall* and *The Terminator* are thematically
about machine-dominated futures, but their plots never use the word, so keyword search cannot
find them. That recall gap is exactly where [vector search](/agensgraph/guides/search/vector/) helps.

Other query parsers are available depending on the input you expect:

| Function                 | Input style                                        |
| ------------------------ | -------------------------------------------------- |
| `websearch_to_tsquery`   | Web-style: `machines "virtual reality" -documentary` |
| `plainto_tsquery`        | Plain text, all terms `AND`-ed together            |
| `to_tsquery`             | Explicit operators: `machines & reality`           |

## Ranking results {#ranking-results}

`ts_rank` scores how well each document matches the query, so results can be ordered by
relevance. A plot that matches more of the query terms ranks higher:

```cypher
MATCH (m:movie)
WHERE to_tsvector('english', m.plot::text) @@ websearch_to_tsquery('english', 'machines OR reality')
RETURN m.title AS title,
       ts_rank(to_tsvector('english', m.plot::text),
               websearch_to_tsquery('english', 'machines OR reality')) AS rank
ORDER BY rank DESC;
```

```
           title            |    rank
----------------------------+-------------
 "The Matrix"               |  0.06079271
 "The Matrix Reloaded"      | 0.030396355
 "The Matrix Revolutions"   | 0.030396355
 "The Matrix Resurrections" | 0.030396355
(4 rows)
```

*The Matrix* ranks above its sequels because its plot contains **both** `machines` and
`reality`, while the sequels match only `machines`.

## Exact-term matching {#exact-term-matching}

Full-text search is the right tool when the query is a specific term that must match exactly:
a name, a code, a rare keyword. Asked for the film about *dinosaurs*, it returns precisely
one:

```cypher
MATCH (m:movie)
WHERE to_tsvector('english', m.plot::text) @@ websearch_to_tsquery('english', 'dinosaurs')
RETURN m.title AS title;
```

```
      title
-----------------
 "Jurassic Park"
(1 row)
```

[Vector search](/agensgraph/guides/search/vector/) has no notion of the literal word `dinosaurs`. Asked for the films
most similar to *Jurassic Park*, it returns *The Avengers* as the nearest neighbor. Both are
large-scale spectacle blockbusters, a reasonable guess by *meaning*, but not what someone
typing "dinosaurs" wants:

```cypher
MATCH (m:movie), (q:movie {title: 'Jurassic Park'})
RETURN m.title AS title
ORDER BY m.embedding::vector(4) <=> q.embedding::vector(4)
LIMIT 3;
```

```
      title
-----------------
 "Jurassic Park"
 "The Avengers"
 "Interstellar"
(3 rows)
```

So the two methods have opposite blind spots. Full-text search is precise but misses synonyms
and intent, while vector search captures meaning but drifts on exact terms. [Hybrid
Search](/agensgraph/guides/search/hybrid/) runs both and fuses the results to get the strengths of each.

## Indexing with GIN {#indexing-with-gin}

Recomputing `to_tsvector` for every row on each search does not scale. Create a GIN index on
the same `to_tsvector` expression so matches are found through the index. The indexed value is
an expression over a property, so use a **property index** and wrap the expression in
parentheses:

```sql
CREATE PROPERTY INDEX ON movie
    USING gin ((to_tsvector('english', plot::text)));
```

The search then uses the index instead of scanning every row:

```psql
EXPLAIN
MATCH (m:movie)
WHERE to_tsvector('english', m.plot::text) @@ websearch_to_tsquery('english', 'machines')
RETURN m.title;
```

```
 Bitmap Heap Scan on movie m
   Recheck Cond: (to_tsvector('english'::regconfig, (properties.'plot'::text)::text) @@ '''machin'''::tsquery)
   ->  Bitmap Index Scan on movie_plot_idx
         Index Cond: (to_tsvector('english'::regconfig, (properties.'plot'::text)::text) @@ '''machin'''::tsquery)
```

The text search configuration used at query time (`'english'` above) must match the one in
the index expression for the index to be used.

> On this small demo the planner may still prefer a sequential scan because it is cheaper for so few rows; add `SET enable_seqscan = off` to observe the index plan. On a real corpus the planner chooses the index automatically.

> GIN property indexes over a `to_tsvector(...)` expression require AgensGraph 2.17 or later.

## Indexing a promoted column {#indexing-a-promoted-column}

From 2.18 a property can be [promoted to a real typed
column](/agensgraph/querying/typed-columns/), which removes the per-row `jsonb` read and the
`::text` cast. `ALTER VLABEL movie ADD COLUMN plot text GENERATED` mirrors the property named
by the column, here `plot`; `GENERATED (sourceKey)` mirrors a differently named key. Queries
keep naming the property, never the column &mdash; resolution is by property key.

The index on this page needs rebuilding when you promote, because it is an *expression* over
the property. A property index over an expression is built against the jsonb bag, and a query
over a promoted key reads the column, so the two would no longer meet.

Write this one as SQL over the column. `\dGi` still lists it, and the query uses it:

```cypher
DROP PROPERTY INDEX movie_plot_idx;
ALTER VLABEL movie ADD COLUMN plot text GENERATED;
```

```sql
CREATE INDEX movie_plot_idx ON moviekb.movie USING gin (to_tsvector('english', plot));
```

```psql
EXPLAIN (COSTS OFF)
MATCH (m:movie)
WHERE to_tsvector('english', m.plot) @@ websearch_to_tsquery('english', 'machines')
RETURN m.title;
```

```
 Bitmap Heap Scan on movie m
   Recheck Cond: (to_tsvector('english'::regconfig, plot) @@ '''machin'''::tsquery)
   ->  Bitmap Index Scan on movie_plot_idx
         Index Cond: (to_tsvector('english'::regconfig, plot) @@ '''machin'''::tsquery)
```

`m.plot` needs no `::text` now: the promoted column is already `text`. See [An expression
property index is built over the
bag](/agensgraph/querying/typed-columns/#an-expression-property-index-is-built-over-the-bag).

## GraphRAG {#graphrag}

Full-text search can also seed a graph traversal. Find the movies whose text best matches the
question, then expand along relationships to gather connected context for a language model.

This is the lexical counterpart to the GraphRAG example in [Vector Search](/agensgraph/guides/search/vector/). It
shines when the question contains specific terms (names, codes, exact phrases) that keyword
search handles better than embeddings.

The [example dataset](/agensgraph/get-started/example-dataset/) already carries `related_to` edges
between films: franchise sequels and thematically linked titles. So the traversal below has
something to follow.

A single Cypher query ranks the movies by full-text relevance to the question (here the term
`resistance`), keeps the best matches, and expands them to their neighbors:

```cypher
MATCH (seed:movie)
WHERE to_tsvector('english', seed.plot::text) @@ websearch_to_tsquery('english', 'resistance')
WITH seed, ts_rank(to_tsvector('english', seed.plot::text),
                   websearch_to_tsquery('english', 'resistance')) AS rank
ORDER BY rank DESC, seed.title
LIMIT 2
MATCH (seed)-[:related_to]-(ctx:movie)
RETURN seed.title AS seed, collect(DISTINCT ctx.title) AS related_context;
```

```
             seed             |               related_context
------------------------------+----------------------------------------------
 "Terminator 2: Judgment Day" | ["The Terminator"]
 "The Terminator"             | ["Terminator 2: Judgment Day", "The Matrix"]
(2 rows)
```

The `WHERE` filter and `WITH … ORDER BY rank LIMIT` select the movies whose text best matches
the query. Those are the *seeds*, here the two *Terminator* films. The second `MATCH` follows
`related_to` edges to gather related titles.

The seeds plus their neighbors form the context passed to the model. Notice that the traversal
reaches *The Matrix*. The keyword `resistance` never matched that film, but it is linked to
the *Terminator* films by their shared war-against-machines theme. To combine this lexical
retrieval with semantic (vector) retrieval before expanding, see [Hybrid Search](/agensgraph/guides/search/hybrid/).

For the same retrieval through a framework rather than by hand, see [AI and LLM
integrations](/agensgraph/drivers/ai-integrations/).
