---
title: 混合搜索
linkTitle: 混合搜索
description: 把向量相似度和全文搜索通过 Reciprocal Rank Fusion 融合，再沿图关系扩展上下文。
type: docs
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/guides/search/hybrid.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
weight: 40
translation_status: complete
---


## 概览 {#overview}

[向量搜索](/zh/agensgraph/guides/search/vector/)按*含义*匹配，[全文搜索](/zh/agensgraph/guides/search/full-text/)按*词语*匹配。各自的优势正好补足对方的弱点。

向量搜索能找到改写表述和相关概念，却可能遗漏产品代码、名称或罕见关键词等精确词项。全文搜索擅长精确词项，却会遗漏同义词和意图。

**混合搜索**同时运行二者并合并结果，使检索兼顾语义理解与词法精确性。AgensGraph 在同一个数据库中提供 [pgvector](https://github.com/pgvector/pgvector) 和 PostgreSQL 全文搜索，因此混合查询可以用同一张图上的一条语句实现。

> 本页讨论的是*搜索结果融合*，与[组合 SQL 和 Cypher](/zh/agensgraph/querying/combining-sql-and-cypher/)一文不同；后者讨论在一条语句中混合 SQL 与 Cypher。

## 倒数排名融合 {#reciprocal-rank-fusion}

两种搜索的分数尺度不同（余弦距离与 `ts_rank`），不能直接相加。**倒数排名融合（Reciprocal Rank Fusion，RRF）**通过组合*排名*而不是分数，避开这一问题。

一个结果每出现在某种搜索中，就贡献 `1 / (k + rank)`，最终对这些贡献求和：

```
score(d) = 1/(k + rank_vector(d)) + 1/(k + rank_fulltext(d))
```

`k` 是平滑常量，用于限制最靠前的排名对结果的支配程度。60 是常见的默认值。文档在*任一种*搜索中排名较好，就能得到合理的得分；在*两种*搜索中都排名较好的文档得分最高。

## 示例数据 {#example-data}

本文使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)中的 18 部电影，每部都有 `plot` 属性，以及情节的四维 `embedding`。请先加载数据集。

实际嵌入向量由 `text-embedding-3-small` 或本地 `sentence-transformers` 等模型生成，通常有数百维。示例将维数降到四维，以便在页面上理解几何关系。

## 混合查询 {#the-hybrid-query}

倒数排名融合需要每种搜索的*排名*，SQL 窗口函数可以生成排名。因此，融合使用 SQL 查询，图数据则来自 Cypher `MATCH` 子查询。

一个子查询按向量距离排列电影，另一个按全文相关性排序。`row_number()` 将每组有序结果转换为排名，外层查询再对排名倒数求和。每个子查询只返回顶点 ID，并按未返回的排名表达式排序。因此，向量属性索引和全文属性索引可以直接服务于排序与过滤。

下面的查询寻找与《黑客帝国》（*The Matrix*）风格相近、同时字面上提到 `machines` 的电影。向量查询使用该片情节的嵌入向量：

```psql
WITH vec AS (
    SELECT id, row_number() OVER () AS rnk
    FROM (MATCH (m:movie)
          RETURN id(m) AS id
          ORDER BY m.embedding::vector(4) <=> '[-0.07594558, 0.04081754, 0.29592122, -0.11921061]'::vector(4)
          LIMIT 10) v
),
fts AS (
    SELECT id, row_number() OVER () AS rnk
    FROM (MATCH (m:movie)
          WHERE to_tsvector('english', m.plot::text) @@ websearch_to_tsquery('english', 'machines')
          RETURN id(m) AS id
          ORDER BY ts_rank(to_tsvector('english', m.plot::text),
                           websearch_to_tsquery('english', 'machines')) DESC) f
)
SELECT m.title AS title,
       round((COALESCE(1.0/(60 + vec.rnk), 0)
            + COALESCE(1.0/(60 + fts.rnk), 0))::numeric, 5) AS rrf_score,
       vec.rnk AS vec_rank,
       fts.rnk AS fts_rank
FROM (MATCH (m:movie) RETURN id(m) AS id, m.title AS title) m
LEFT JOIN vec ON vec.id = m.id
LEFT JOIN fts ON fts.id = m.id
WHERE vec.id IS NOT NULL OR fts.id IS NOT NULL
ORDER BY rrf_score DESC
LIMIT 6;
```

```
            title             | rrf_score | vec_rank | fts_rank
------------------------------+-----------+----------+----------
 "The Matrix"                 |   0.03279 |        1 |        1
 "The Matrix Reloaded"        |   0.03226 |        2 |        2
 "The Matrix Resurrections"   |   0.03150 |        3 |        4
 "The Matrix Revolutions"     |   0.03080 |        7 |        3
 "Total Recall"               |   0.01563 |        4 |
 "Avatar"                     |   0.01538 |        5 |
(6 rows)
```

融合在这里同时发挥了两种作用。《全面回忆》（*Total Recall*，向量排名第 4）没有出现 `machines`，因此全文搜索分支完全找不到它。但它仍然保留在结果中，因为向量搜索识别出它和《黑客帝国》一样，讲述的是*虚假现实*。

《黑客帝国：矩阵革命》（*The Matrix Revolutions*）则相反。它的向量距离排名只有第 7，会落在纯向量搜索的前五名之外；但全文搜索分支将它排在第 3，因为其情节确实使用了 *machines*。融合将它的排名提升回来。

**同时**满足两个分支的电影（*The Matrix*、*Reloaded*、*Resurrections*）排在最前。向量搜索贡献召回，全文搜索贡献精确性，RRF 将二者结合起来。

## 为两个分支建立索引 {#indexing-both-arms}

查询的每个分支都是普通的相似度搜索或全文搜索，因此可以使用[向量搜索](/zh/agensgraph/guides/search/vector/)和[全文搜索](/zh/agensgraph/guides/search/full-text/)中相同的**属性索引**加速：嵌入向量上的 HNSW 索引，以及纯文本情节上的 GIN 索引。

```sql
CREATE PROPERTY INDEX ON movie
    USING hnsw ((embedding::vector(4)) vector_cosine_ops);
CREATE PROPERTY INDEX ON movie
    USING gin ((to_tsvector('english', plot::text)));
```

每个 Cypher 子查询只返回 ID，并按原始排名表达式排序，因此规划器可以让每个分支使用相应的索引。HNSW 索引排列向量候选项，GIN 索引过滤全文匹配项，两种搜索都不必扫描整个标签。

融合查询的 `EXPLAIN` 相关部分如下：

```
 ...
 ->  Subquery Scan on vec
       ->  Limit
             ->  Index Scan using movie_embedding_idx on movie m
                   Order By: ((properties.'embedding'::text)::vector(4) <=> '[...]'::vector(4))
 ...
 ->  Subquery Scan on fts
       ->  Bitmap Heap Scan on movie m
             Recheck Cond: (to_tsvector('english', (properties.'plot'::text)::text) @@ '...'::tsquery)
             ->  Bitmap Index Scan on movie_plot_idx
```

> 对于很小的示例数据集，规划器仍可能选择顺序扫描，因为只扫描几行比使用索引更便宜。可以添加 `SET enable_seqscan = off` 来观察索引计划。对于真实规模的语料库，规划器会自动选择索引。

以上两个索引都是属性上的表达式索引。如果将[任一个属性提升](/zh/agensgraph/querying/typed-columns/)为类型列，需要重建相应分支的索引：表达式属性索引建立在 jsonb 属性包上，而提升后的键从列中读取。嵌入向量分支随后使用普通列索引，全文搜索分支则使用列上的 SQL 索引：

```cypher
ALTER VLABEL movie ADD COLUMN embedding vector(4) GENERATED;
CREATE PROPERTY INDEX ON movie USING hnsw (embedding vector_cosine_ops);
```

融合查询本身无需修改。[向量搜索](/zh/agensgraph/guides/search/vector/#indexing-a-promoted-column)和[全文搜索](/zh/agensgraph/guides/search/full-text/#indexing-a-promoted-column)分别展示了各自的处理方式。

## 调优 {#tuning}

- **`k` 常量**：较大的值会减小靠前排名的优势，较小的值则让前几个结果占主导。60 是合理的起点。
- **加权**：要偏向某种方法，可以为其贡献乘上系数，例如 `1.5 * COALESCE(1.0/(60 + vec.rnk), 0)` 会提高语义搜索的权重。
- **候选深度**：每个 CTE 内部的 `LIMIT` 控制融合前各搜索分支的检索深度。增大它可以提高召回，但会付出一定的延迟代价。

## GraphRAG {#graphrag}

混合检索为图遍历提供了更强的起点。先同时按语义相似度与关键词相关性排序（使用 RRF），再从排名靠前的结果沿关系扩展，为语言模型组装上下文。

倒数排名融合需要 SQL 窗口函数，但所有接触图的部分，包括检索与扩展，都写成 `FROM` 子句中的 Cypher `MATCH` 子查询。这正是[组合 SQL 和 Cypher](/zh/agensgraph/querying/combining-sql-and-cypher/)的机制。查询仍然直接操作图，并复用前面建立的属性索引。

[示例数据集](/zh/agensgraph/get-started/example-dataset/)已经通过 `related_to` 边连接系列续集和主题相关的电影，因此下面的遍历有关系可供跟随。

此处向量分支检索类似《黑客帝国》的电影，全文搜索分支匹配关键词 `memories`。SQL 的 `row_number()` 将每组有序结果转换为排名；`seeds` CTE 用 RRF 融合二者并保留前两名；最后一次 Cypher 遍历收集各个种子的邻居：

```psql
WITH vec AS (
    SELECT id, row_number() OVER () AS rnk
    FROM (MATCH (m:movie)
          RETURN id(m) AS id
          ORDER BY m.embedding::vector(4) <=> '[-0.07594558, 0.04081754, 0.29592122, -0.11921061]'::vector(4)
          LIMIT 10) v
),
fts AS (
    SELECT id, row_number() OVER () AS rnk
    FROM (MATCH (m:movie)
          WHERE to_tsvector('english', m.plot::text) @@ websearch_to_tsquery('english', 'memories')
          RETURN id(m) AS id
          ORDER BY ts_rank(to_tsvector('english', m.plot::text),
                           websearch_to_tsquery('english', 'memories')) DESC) f
),
seeds AS (
    SELECT m.id, m.title,
           COALESCE(1.0/(60 + vec.rnk), 0) + COALESCE(1.0/(60 + fts.rnk), 0) AS score
    FROM (MATCH (m:movie) RETURN id(m) AS id, m.title AS title) m
    LEFT JOIN vec ON vec.id = m.id
    LEFT JOIN fts ON fts.id = m.id
    WHERE vec.id IS NOT NULL OR fts.id IS NOT NULL
    ORDER BY score DESC
    LIMIT 2
)
SELECT s.title AS seed,
       jsonb_agg(DISTINCT ctx.title) AS expanded_context
FROM seeds s
LEFT JOIN (MATCH (a:movie)-[:related_to]-(b:movie)
           RETURN id(a) AS aid, b.title AS title) ctx ON ctx.aid = s.id
GROUP BY s.title
ORDER BY s.title;
```

```
      seed      |                   expanded_context
----------------+-----------------------------------------------------------
 "The Matrix"   | ["The Matrix Reloaded", "The Terminator", "Total Recall"]
 "Total Recall" | ["Inception", "The Matrix"]
(2 rows)
```

融合改变了遍历的种子。《全面回忆》的向量与《黑客帝国》的距离只排在第 4，所以纯向量种子选择本来会扩展《黑客帝国》和《黑客帝国：重装上阵》。但关键词 `memories` 精确匹配《全面回忆》，RRF 将它提升到前两名。

有了《全面回忆》这个种子，遍历会沿其 `related_to` 边到达《盗梦空间》（*Inception*），找到任一分支单独使用时都不会呈现的上下文。

最终结果包含混合排名的种子及其图邻居，同时利用语义相似性、精确关键词和显式关系，是这三种方法中上下文最丰富的一种。

[AI 与 LLM 集成](/zh/agensgraph/drivers/ai-integrations/)中的框架可以构造相同的查询结构，其中几个框架将它封装为单个检索器。
