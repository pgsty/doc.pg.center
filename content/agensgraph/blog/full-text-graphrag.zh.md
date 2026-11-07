---
title: 把全文搜索作为图种子
linkTitle: 把全文搜索作为图种子
description: 介绍 AgensGraph 中的精确词项、GIN 索引、相关性排序和 GraphRAG 图扩展。
type: docs
date: 2026-11-07
tags:
- 搜索
- GraphRAG
- PostgreSQL
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/guides/search/full-text.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
summary: 从 AgensGraph 全文搜索指南中提炼一条可执行的阅读路径。
---

全文搜索擅长回答一个很窄的问题：文档中是否出现了这个词，它匹配得有多强？在图遍历之前保留这种精确性，可以让后续上下文扩展有可靠的种子。

在 AgensGraph 中，可以把文本属性转换为 `tsvector`，再用 `websearch_to_tsquery` 查询：

```cypher
MATCH (m:movie)
WHERE to_tsvector('english', m.plot::text) @@ websearch_to_tsquery('english', 'machines')
RETURN m.title AS title;
```

查询匹配的是词元。词干化会让 `machines` 与 `machine` 归到同一个词干；如果一部电影只是主题相关、却没有出现这个字面词，它就不会被返回。当问题包含代码、名称或精确短语时，这正是想要的行为。

## 索引必须匹配表达式

查询使用的表达式和全文配置必须与索引一致：

```sql
CREATE PROPERTY INDEX ON movie
    USING gin ((to_tsvector('english', plot::text)));
```

2.18 把 `plot` 提升为生成的 `text` 列后，要按列重建索引。Cypher 中仍然写属性名，但物理读取路径已经改变。

## 让图补齐上下文

全文搜索的结果可以成为遍历种子：先按相关性排序，保留少量最佳种子，再收集它们的邻居。最终交给模型的上下文同时包含精确命中的对象和与它们相连的关系。

全文搜索不理解同义词和意图，向量搜索也不能保证字面词出现。[全文搜索指南](/zh/agensgraph/guides/search/full-text/)与[混合搜索指南](/zh/agensgraph/guides/search/hybrid/)提供了可执行的完整查询。
