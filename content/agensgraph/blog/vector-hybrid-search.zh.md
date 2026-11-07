---
title: 向量与混合检索
linkTitle: 向量与混合检索
description: 比较语义相似度、精确词项和 RRF 混合排序，并说明图扩展应该放在检索之后。
type: docs
date: 2026-11-07
tags:
- 搜索
- 向量
- GraphRAG
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/guides/search/hybrid.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
summary: 从 AgensGraph 出发比较语义、词法与混合检索。
---

向量搜索和全文搜索的盲点相反。embedding 可以找到使用了不同词语、但主题相近的电影；全文查询可以找到稀有代码或专有名词，却可能错过同义表达。

混合检索同时运行两条路径，再用 Reciprocal Rank Fusion（RRF）融合名次：

```text
score(d) = 1 / (k + rank_vector(d)) + 1 / (k + rank_text(d))
```

关键在于工作顺序：每条路径先使用匹配的索引获得有限候选，再融合排名，最后只对排名靠前的种子沿图关系扩展。如果在排序前把整批候选全部展开，检索查询就会变成图扫描。

## 设计时问三个问题

1. 用户需要精确 token，还是只需要一个概念？
2. 哪条路径能够解释文档为什么被返回？
3. 种子排好名次后，需要多少图上下文？

[向量搜索指南](/zh/agensgraph/guides/search/vector/)介绍 pgvector 与相似度；[混合搜索指南](/zh/agensgraph/guides/search/hybrid/)把两条路径合并，再沿 `related_to` 边扩展 GraphRAG 上下文。
