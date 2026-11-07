---
title: AI 与 LLM 集成
linkTitle: AI 与 LLM 集成
description: AgensGraph 常作为检索增强生成的后端，因为知识图谱及其 embedding 可以保存在同一个数据库中。
type: docs
weight: 50
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/drivers/ai-integrations.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: complete
---


## 概览 {#overview}

AgensGraph 常作为检索增强生成的后端，因为知识图谱及其 embedding 可以保存在同一个数据库中。图就是表，属性就是 `jsonb`，所以 `pgvector` 可以为顶点上的 embedding 建索引。

因此，一条查询可以找到语义上最接近的文档，再从它们出发沿图扩展。GraphRAG 需要的正是这一点。

这些集成位于独立手册：**[AgensGraph AI](https://tech.skaiworldwide.com/docs/en/agensgraph-ai/)**。每个集成在那里都有自己的安装和用法页面；本页说明它们各自的用途。

每一个集成都运行在 [AgensGraph Python 驱动](https://tech.skaiworldwide.com/docs/en/agensgraph-driver/python/)上。该驱动构建于 [psycopg 3](https://www.psycopg.org/psycopg3/)，并通过它运行 Cypher。因此，无论选择哪个框架，顶点、边或路径都会作为对象进入框架，而不是文本。0.3.1 集成要求 2.0 或更高版本的驱动。驱动本身参见[驱动与客户端库](/zh/agensgraph/drivers/)。

`pgvector` 负责 embedding，且不随 AgensGraph 捆绑，因此需要在数据库中安装一次。参见[向量搜索](/zh/agensgraph/guides/search/vector/)。

每个集成的源码都在 [agensgraph-ai 仓库](https://github.com/skaiworldwide-oss/agensgraph-ai)，该仓库还附带可运行的演示。

## LangChain {#langchain}

图存储、由 pgvector 支持的向量存储、聊天消息历史、LangGraph checkpointer，以及 LLM graph transformer。

[LangChain 集成](https://tech.skaiworldwide.com/docs/en/agensgraph-ai/langchain/)

## LlamaIndex {#llamaindex}

`PropertyGraphIndex` 和 `VectorStoreIndex` 存储，支持混合搜索、元数据过滤和针对 AgensGraph 调优的 Text2Cypher。

[LlamaIndex 集成](https://tech.skaiworldwide.com/docs/en/agensgraph-ai/llamaindex/)

## LightRAG {#lightrag}

同一个数据库承担全部四种 LightRAG 存储角色，并支持工作区多租户。

[LightRAG 集成](https://tech.skaiworldwide.com/docs/en/agensgraph-ai/lightrag/)

## cognee {#cognee}

cognee AI 记忆框架的图与向量适配器。

[cognee 集成](https://tech.skaiworldwide.com/docs/en/agensgraph-ai/cognee/)

## MCP 服务器 {#mcp-servers}

三个 Model Context Protocol 服务器——Cypher、memory 和数据建模——把 AgensGraph 暴露给 Claude Desktop 等客户端。

[MCP 服务器](https://tech.skaiworldwide.com/docs/en/agensgraph-ai/mcp/)

## 不使用框架 {#without-a-framework}

如果检索由你自己构建，而不是通过框架完成，三篇搜索指南是起点。[向量](/zh/agensgraph/guides/search/vector/)、[全文](/zh/agensgraph/guides/search/full-text/)和[混合](/zh/agensgraph/guides/search/hybrid/)搜索每篇末尾都有一个 GraphRAG 小节，用同一条语句把搜索与遍历组合起来。
