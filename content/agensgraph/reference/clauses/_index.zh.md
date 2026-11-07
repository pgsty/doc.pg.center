---
title: 子句
linkTitle: 子句
description: 按流水线职责介绍 Cypher 与 GQL 的每个图查询子句。
type: docs
weight: 30
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/index.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
cascade:
  type: docs
no_list: true
---


Cypher 或 GQL 语句是由子句组成的流水线。这些页面按子句在这条流水线中的职责分组，而不是按字母顺序排列；每个页面都采用相同的结构。

标记为 **GQL** 的子句来自 ISO/IEC 39075。凡是接受 Cypher 语句的地方都可以接受这些子句——不存在单独的 GQL 模式。标准中哪些部分受支持，请参见 [GQL 一致性](/zh/agensgraph/appendix/gql-conformance/)。

## 读取 {#reading}

- [MATCH](/zh/agensgraph/reference/clauses/match/)
- [OPTIONAL MATCH](/zh/agensgraph/reference/clauses/optional-match/)
- [WHERE](/zh/agensgraph/reference/clauses/where/)
- [LOAD FROM](/zh/agensgraph/reference/clauses/load-from/)

## 投影 {#projecting}

- [RETURN](/zh/agensgraph/reference/clauses/return/)
- [WITH](/zh/agensgraph/reference/clauses/with/)
- [LET](/zh/agensgraph/reference/clauses/let/)
- [ORDER BY](/zh/agensgraph/reference/clauses/order-by/)
- [SKIP and LIMIT](/zh/agensgraph/reference/clauses/skip-and-limit/)

## 写入 {#writing}

- [CREATE](/zh/agensgraph/reference/clauses/create/)
- [INSERT](/zh/agensgraph/reference/clauses/insert/)
- [MERGE](/zh/agensgraph/reference/clauses/merge/)
- [SET](/zh/agensgraph/reference/clauses/set/)
- [REMOVE](/zh/agensgraph/reference/clauses/remove/)
- [DELETE](/zh/agensgraph/reference/clauses/delete/)

## 组合 {#composing}

- [UNWIND](/zh/agensgraph/reference/clauses/unwind/)
- [FOR](/zh/agensgraph/reference/clauses/for/)
- [FILTER](/zh/agensgraph/reference/clauses/filter/)
- [NEXT](/zh/agensgraph/reference/clauses/next/)
- [FINISH](/zh/agensgraph/reference/clauses/finish/)
- [UNION](/zh/agensgraph/reference/clauses/union/)

## 子查询 {#subqueries}

- [CALL](/zh/agensgraph/reference/clauses/call/)
- [CALL … YIELD](/zh/agensgraph/reference/clauses/call-yield/)
- [CALL { subquery }](/zh/agensgraph/reference/clauses/call-subquery/)
- [OPTIONAL CALL](/zh/agensgraph/reference/clauses/optional-call/)
- [Subquery value expressions](/zh/agensgraph/reference/clauses/subquery-expressions/)
