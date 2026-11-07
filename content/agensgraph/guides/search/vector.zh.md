---
title: 向量搜索
linkTitle: 向量搜索
description: 使用 pgvector 在 AgensGraph 图属性上做相似度搜索，并将结果扩展为 GraphRAG 上下文。
type: docs
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/guides/search/vector.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
weight: 20
translation_status: complete
---


## 概览 {#overview}

AgensGraph 基于 PostgreSQL 构建，因此 [pgvector](https://github.com/pgvector/pgvector) 扩展可以直接为图增加向量相似度搜索。嵌入向量与图数据保存在一起，同一个数据库就能组合语义（向量）搜索与 Cypher 图遍历。这是检索增强生成（RAG）和 *GraphRAG* 应用的基础。

向量搜索按*含义*匹配，而不只是匹配词语：两段文本即使没有共同词汇，也可能在向量空间中很接近。相对于关键词匹配，也就是[全文搜索](/zh/agensgraph/guides/search/full-text/)，这正是它的优势。

[混合搜索](/zh/agensgraph/guides/search/hybrid/)介绍如何组合二者。三篇指南使用同一组电影，可以直接比较行为。

嵌入向量作为顶点或边的数值数组**属性**存储。属性的类型是 `jsonb`，因此数组以 JSON 数组保存。需要执行向量运算时，用 `::vector(n)` 将其转换为 pgvector 的 `vector` 类型。

每次读取都会执行这一转换。对于几千行数据，这没有问题，但在大规模数据上会造成浪费。从 2.18 起，可以将属性[提升为真正的 `vector` 列](/zh/agensgraph/querying/typed-columns/)。

转换随后只在写入时执行一次，并且可以直接在列上建立 HNSW 索引。本页查询无需修改，仍然可以使用索引，因为提升后的列上多余的 `::vector(n)` 会被优化掉。

提升属性会改变两件事。

首先是值的*类型*。提升后的 `d.emb` 返回 `vector`，未提升的属性则返回 `jsonb`。因此，解析 JSON 表示的客户端需要更新。

其次是索引的形式。提升后的列使用普通列索引，而不是类型转换表达式索引，因此需要转储和恢复索引时，优先采用这种形式。

## 安装 pgvector {#installing-pgvector}

[pgvector](https://github.com/pgvector/pgvector) 是单独的扩展，必须针对当前 AgensGraph 安装进行编译和安装。安装后，在需要使用的数据库中启用它：

```sql
CREATE EXTENSION vector;
```

## 示例数据 {#example-data}

本文使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)中的 18 部电影，每部都有 `plot` 属性和对应情节的四维 `embedding`。请先加载数据集。

实际嵌入向量由 `text-embedding-3-small` 或本地 `sentence-transformers` 等模型生成，通常有数百维。示例将维数降到四维，便于在页面上理解几何关系。

## 相似度搜索 {#similarity-search}

pgvector 提供一组距离运算符及对应函数。将两个操作数都转换为 `vector(n)`，然后按距离排序。

| 运算符 | 函数 | 距离 | HNSW 运算符类 |
| --- | --- | --- | --- |
| `<=>` | `cosine_distance` | 余弦距离 | `vector_cosine_ops` |
| `<->` | `l2_distance` | 欧几里得距离（L2） | `vector_l2_ops` |
| `<#>` | `inner_product` | 负内积 | `vector_ip_ops` |
| `<+>` | `l1_distance` | 曼哈顿距离（L1） | `vector_l1_ops` |

查找情节与查询向量最接近的电影，使用余弦距离。此处的查询向量是《黑客帝国》（*The Matrix*）情节的嵌入，因此搜索返回含义最相近的电影：

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

前三个结果显然是续集，第四个结果更值得关注。《全面回忆》（*Total Recall*）的情节是“一个建筑工人发现自己的记忆是植入的”。它与《黑客帝国》的“一个黑客……由机器控制的模拟世界”**没有共同关键词**。

向量搜索仍然把它排在第四，因为两部电影都讲述了人物发现自身现实是虚构的故事。关键词搜索无法建立这种联系。

语义搜索捕捉到的正是这种关系，而词法搜索做不到。可以比较同一数据集上的[全文搜索](/zh/agensgraph/guides/search/full-text/)结果，并通过[混合搜索](/zh/agensgraph/guides/search/hybrid/)结合二者。

> `ORDER BY` 可以引用没有出现在 `RETURN` 列表中的距离表达式（AgensGraph 2.17 及以后）。只返回 `title` 能使输出简洁，更重要的是让 HNSW 索引用于排序。如果返回原始距离，距离会被转换为 `jsonb`，从而阻止索引的使用。

函数形式方便与另一个已存储的向量比较，例如查找“与《终结者》（*The Terminator*）最相似的电影”，无需手写查询向量：

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

## 使用 HNSW 建立索引 {#indexing-with-hnsw}

没有索引时，每次相似度查询都会扫描所有行，并逐行计算距离。对于较大的数据集，可以建立 HNSW 索引，使规划器能够采用索引扫描。因为被索引的值是类型转换表达式，需要使用**属性索引**：

```sql
CREATE PROPERTY INDEX ON movie
    USING hnsw ((embedding::vector(4)) vector_cosine_ops);
```

运算符类必须与查询的距离匹配：`<=>` 对应 `vector_cosine_ops`，`<->` 对应 `vector_l2_ops`，其他依此类推。前面的相似度查询随后可以使用索引：

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

> 示例只有 18 行，规划器仍可能选择顺序扫描，因为扫描这几行的成本更低。可以添加 `SET enable_seqscan = off` 来观察索引计划。对于真实规模的语料库，规划器会自动选择索引。

> 在 `::vector(n)` 类型转换上创建 HNSW 属性索引，需要 AgensGraph 2.17 或更高版本。

## 为提升后的列建立索引 {#indexing-a-promoted-column}

上面的索引建立在类型转换表达式上。提升属性会消除这一转换，使索引成为普通列索引。

属性提升会在 jsonb 属性包旁增加一个真正的类型列，并在写入时填充。声明的是列名；该列映射的属性默认与它同名：

```cypher
DROP PROPERTY INDEX movie_embedding_idx;
ALTER VLABEL movie ADD COLUMN embedding vector(4) GENERATED;
```

单独使用 `GENERATED` 会映射与列同名的属性，此处为 `embedding`。如果列需要使用不同名称，可写成 `GENERATED (sourceKey)`。例如，`ALTER VLABEL movie ADD COLUMN emb vector(4) GENERATED (embedding)` 会把同一属性存入名为 `emb` 的列。无论哪种方式，**查询始终使用属性名，而不是列名**：解析依据的是属性键，列名不会出现在 Cypher 中。完整说明参见[将属性提升为列](/zh/agensgraph/querying/typed-columns/)。

此时索引是普通列索引，不需要类型转换，也不需要额外括号：

```cypher
CREATE PROPERTY INDEX ON movie USING hnsw (embedding vector_cosine_ops);
```

本页所有查询仍然可以原样运行。提升后的列上多余的 `::vector(4)` 会被优化掉，因此 `m.embedding` 与 `m.embedding::vector(4)` 产生相同的计划：

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
> 提升某个属性键之前，应先删除读取它的表达式索引，如上例所示。表达式属性索引建立在 jsonb 属性包上，而提升后的键从列中读取，两者不再匹配。参见[表达式属性索引建立在属性包上](/zh/agensgraph/querying/typed-columns/#an-expression-property-index-is-built-over-the-bag)。

提升后值的类型会改变：`m.embedding` 现在返回 `vector`，而未提升时返回 `jsonb`。

## GraphRAG {#graphrag}

在图数据库中执行向量搜索有一个特别的优势：语义匹配可以成为图遍历的*起点*。

典型的 GraphRAG 检索在一次查询中完成两件事：先根据向量相似度找到与问题最相关的条目，再沿关系扩展，为语言模型收集相连的上下文。

[示例数据集](/zh/agensgraph/get-started/example-dataset/)已经通过 `related_to` 边连接系列续集和主题相关的电影，因此下面的遍历有关系可供跟随。

查询时，使用生成电影情节向量的同一个模型，为用户问题生成嵌入向量。然后执行一条 Cypher 查询，检索最接近的电影并扩展到其邻居。此处的问题嵌入是《黑客帝国》的向量：

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

`WITH … ORDER BY … LIMIT 2` 根据向量相似度选出最匹配问题的两部电影，它们就是*种子*。第二个 `MATCH` 从每个种子沿 `related_to` 边收集邻近电影。

组合后的集合包含种子及其图邻居，比仅使用向量搜索提供了更丰富的上下文，可以传给语言模型生成最终答案。

这一模式可以推广：从种子扩展多跳，按边类型或属性过滤，或连接人物、制片厂、来源等其他标签，以精确构造 RAG 流水线需要的上下文。

若希望由框架组装这些过程，[AI 与 LLM 集成](/zh/agensgraph/drivers/ai-integrations/)列出了可用的库。
