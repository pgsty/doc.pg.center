---
title: Vector and hybrid retrieval
linkTitle: Vector and hybrid retrieval
description: Where semantic similarity helps, where exact words still matter, and how RRF combines both before graph
  expansion.
type: docs
date: 2026-11-07
tags:
- Search
- Vector
- GraphRAG
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/guides/search/hybrid.html
upstream_source: agensgraph
upstream_modified: true
summary: A practical comparison of semantic, lexical, and hybrid retrieval in AgensGraph.
---

Vector search and full-text search fail in opposite directions. An embedding can find a film with a similar theme even when it uses different words. A full-text query can find a rare code or proper name but miss a synonym.

Hybrid retrieval runs both arms and fuses ranks with Reciprocal Rank Fusion (RRF):

```text
score(d) = 1 / (k + rank_vector(d)) + 1 / (k + rank_text(d))
```

The important detail is the order of work. Run each retrieval arm against a matching index, fuse a bounded candidate set, then expand only the top seeds through graph relationships. Expanding the whole candidate set before ranking turns a focused retrieval query into a graph scan.

## A useful test

Ask three questions of a retrieval design:

1. Does a user need an exact token, or a concept?
2. Which arm can explain why a document was returned?
3. How much graph context is useful after the seeds are ranked?

The [vector guide](/agensgraph/guides/search/vector/) covers pgvector and similarity. The [hybrid guide](/agensgraph/guides/search/hybrid/) combines both arms and follows `related_to` edges into a GraphRAG context.
