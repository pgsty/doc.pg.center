---
title: Full-text search as a graph seed
linkTitle: Full-text search as a graph seed
description: Exact terms, GIN indexes, ranking, and graph expansion for lexical GraphRAG in AgensGraph.
type: docs
date: 2026-11-07
tags:
- Search
- GraphRAG
- PostgreSQL
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/guides/search/full-text.html
upstream_source: agensgraph
upstream_modified: true
summary: A practical reading of the AgensGraph full-text search guide.
---

Full-text search answers a narrow question well: did this term appear in the document, and how strongly did it match? That precision is useful before a graph traversal expands the answer.

In AgensGraph, a text property can be converted to a `tsvector` and queried with `websearch_to_tsquery`:

```cypher
MATCH (m:movie)
WHERE to_tsvector('english', m.plot::text) @@ websearch_to_tsquery('english', 'machines')
RETURN m.title AS title;
```

The query matches lexemes. Stemming makes `machines` and `machine` meet at the same stem, while a thematically related film without the literal word stays out of the result. That is a feature when the question contains a code, a name, or an exact phrase.

## Index the same expression

The index must match the expression and text configuration used by the query:

```sql
CREATE PROPERTY INDEX ON movie
    USING gin ((to_tsvector('english', plot::text)));
```

After promoting `plot` to a generated `text` column in 2.18, rebuild the index over the column. The property name in Cypher stays the same, but the physical read path changes.

## Let the graph add context

The lexical result can seed a traversal. Rank the best matches, keep a small number of seeds, and then collect their neighbours. The model receives context that includes both the exact matches and the relationships attached to them.

Full-text search does not understand synonyms or intent; vector search does not guarantee literal terms. The [full-text guide](/agensgraph/guides/search/full-text/) and [hybrid search guide](/agensgraph/guides/search/hybrid/) show the boundary in executable queries.
