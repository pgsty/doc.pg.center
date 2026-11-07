---
title: AI and LLM integrations
linkTitle: AI and LLM integrations
description: AgensGraph is a common backing store for retrieval-augmented generation, because a knowledge graph
  and its embeddings can live in one database.
type: docs
weight: 50
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/drivers/ai-integrations.html
upstream_source: agensgraph
upstream_modified: true
---


## Overview {#overview}

AgensGraph is a common backing store for retrieval-augmented generation, because a knowledge
graph and its embeddings can live in one database. The graph is tables, and a property is
`jsonb`, so `pgvector` indexes an embedding stored on a vertex.

One query can therefore find the semantically closest documents and then walk the graph out
from them. GraphRAG needs exactly that.

The integrations live in their own manual: **[AgensGraph
AI](https://tech.skaiworldwide.com/docs/en/agensgraph-ai/)**. Each has its own installation
and usage pages there; this page says what each one is for.

Every one of them runs on the [AgensGraph Python
driver](https://tech.skaiworldwide.com/docs/en/agensgraph-driver/python/), which is built on
[psycopg 3](https://www.psycopg.org/psycopg3/) and runs Cypher through it. So a vertex, an edge or
a path reaches the framework as an object rather than as text, whichever framework you pick. The
0.3.1 integrations require version 2.0 or later of the driver. See
[Drivers and client libraries](/agensgraph/drivers/ai-integrations/index) for the driver on its own.

`pgvector` handles the embeddings and is not bundled, so you install it into the database
once. See [Vector search](/agensgraph/guides/search/vector/).

Source for every integration: the [agensgraph-ai
repository](https://github.com/skaiworldwide-oss/agensgraph-ai), which also ships runnable
demos.

## LangChain {#langchain}

A graph store, a pgvector-backed vector store, chat-message history, a LangGraph checkpointer,
and an LLM graph transformer.

[LangChain integration](https://tech.skaiworldwide.com/docs/en/agensgraph-ai/langchain/)

## LlamaIndex {#llamaindex}

`PropertyGraphIndex` and `VectorStoreIndex` stores, with hybrid search, metadata filtering and
AgensGraph-tuned Text2Cypher.

[LlamaIndex integration](https://tech.skaiworldwide.com/docs/en/agensgraph-ai/llamaindex/)

## LightRAG {#lightrag}

All four LightRAG storage roles on one database, with workspace multi-tenancy.

[LightRAG integration](https://tech.skaiworldwide.com/docs/en/agensgraph-ai/lightrag/)

## cognee {#cognee}

Graph and vector adapters for the cognee AI-memory framework.

[cognee integration](https://tech.skaiworldwide.com/docs/en/agensgraph-ai/cognee/)

## MCP servers {#mcp-servers}

Three Model Context Protocol servers — Cypher, memory and data modeling — that expose
AgensGraph to clients such as Claude Desktop.

[MCP servers](https://tech.skaiworldwide.com/docs/en/agensgraph-ai/mcp/)

## Without a framework {#without-a-framework}

If you are building the retrieval yourself rather than through a framework, the three search
guides are the place to start. [Vector](/agensgraph/guides/search/vector/), [full-text](/agensgraph/guides/search/full-text/)
and [hybrid](/agensgraph/guides/search/hybrid/) search each end with a GraphRAG section that combines the
search with a traversal in one statement.
