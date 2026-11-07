---
title: 全文搜索
linkTitle: 全文搜索
description: 使用 PostgreSQL 全文搜索在图属性上做词法检索、相关性排序、GIN 索引和 GraphRAG。
type: docs
weight: 30
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/guides/search/full-text.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: complete
---


## 概览 {#overview}

AgensGraph 基于 PostgreSQL 构建，继承了它的全文搜索引擎，因此可以直接对图属性中存储的文本执行基于语言处理的关键词搜索。全文搜索会将文档和查询规范化为词元，包括词干提取、停用词过滤和大小写归一。这使它很适合*词法*检索，即匹配用户输入的词语。

它与按*含义*匹配的[向量搜索](/zh/agensgraph/guides/search/vector/)天然互补。[混合搜索](/zh/agensgraph/guides/search/hybrid/)介绍如何结合二者。这三篇指南使用同一组电影，便于直接比较结果。

图属性以 `jsonb` 存储，因此需要先将文本属性转换为 `text`（使用 `::text`），再转换为 `tsvector`。

## 示例数据 {#example-data}

本文使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)中的 18 部电影。每部电影都有 `plot` 属性，以及情节的四维 `embedding`。请先加载数据集，再继续阅读。

实际嵌入向量由模型生成，例如 `text-embedding-3-small` 或本地 `sentence-transformers` 模型，通常有数百维。示例将维数降到四维，让页面上的几何关系更容易理解。

## 搜索文本属性 {#searching-a-text-property}

用 `to_tsvector` 将属性转换为 `tsvector`，用 `*_to_tsquery` 系列函数解析用户输入，再用 `@@` 运算符进行匹配。`websearch_to_tsquery` 接受宽松的网页搜索语法：引号内的短语、`OR`，以及用 `-` 排除词项。这使它成为处理用户输入时合适的默认选择。

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

查询匹配的是词元，而非原始文本。`machines` 会被约化为词干 `machin`，因此单数 `machine` 也会匹配完全相同的行。

也要注意*没有*返回的电影。《全面回忆》（*Total Recall*）和《终结者》（*The Terminator*）的主题都与机器统治的未来有关，但情节文本中没有使用这个词，所以关键词搜索找不到它们。[向量搜索](/zh/agensgraph/guides/search/vector/)恰好可以弥补这一召回缺口。

根据预期输入形式，还可以选择其他查询解析器：

| 函数 | 输入形式 |
| --- | --- |
| `websearch_to_tsquery` | 网页搜索风格：`machines "virtual reality" -documentary` |
| `plainto_tsquery` | 普通文本，所有词项通过 `AND` 连接 |
| `to_tsquery` | 显式运算符：`machines & reality` |

## 对结果排序 {#ranking-results}

`ts_rank` 为每篇文档与查询的匹配程度打分，因此可以按相关性排列结果。情节文本中匹配的查询词越多，排名越高：

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

《黑客帝国》（*The Matrix*）排在续集之前，因为其情节**同时**包含 `machines` 和 `reality`，而续集只匹配 `machines`。

## 精确词项匹配 {#exact-term-matching}

当查询包含必须精确匹配的特定词项，如名称、代码或罕见关键词时，全文搜索很合适。搜索关于*恐龙*（`dinosaurs`）的电影时，它恰好只返回一部：

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

[向量搜索](/zh/agensgraph/guides/search/vector/)没有字面词 `dinosaurs` 的概念。搜索与《侏罗纪公园》（*Jurassic Park*）最相似的电影时，最近的邻居是《复仇者联盟》（*The Avengers*）。两者都是宏大场面的商业大片，按*含义*推测有其合理性，但这并不是输入“dinosaurs”的人想要的结果：

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

因此，两种方法的盲点正好相反。全文搜索精确，却会遗漏同义词和意图；向量搜索能捕捉含义，但遇到精确词项时可能偏离。[混合搜索](/zh/agensgraph/guides/search/hybrid/)同时运行两种检索并融合结果，以发挥各自的优势。

## 使用 GIN 建立索引 {#indexing-with-gin}

每次搜索都为每一行重新计算 `to_tsvector`，无法适应大规模数据。可以在相同的 `to_tsvector` 表达式上建立 GIN 索引，通过索引找到匹配项。索引值是属性上的表达式，因此需要使用**属性索引**，并用括号括起表达式：

```sql
CREATE PROPERTY INDEX ON movie
    USING gin ((to_tsvector('english', plot::text)));
```

随后，搜索会使用索引，而不是扫描所有行：

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

查询使用的文本搜索配置（上面的 `'english'`）必须与索引表达式中的配置相同，才能使用该索引。

> 示例数据很小，规划器仍可能选择顺序扫描，因为扫描这几行的成本更低。可以添加 `SET enable_seqscan = off` 来观察索引计划。对于真实规模的语料库，规划器会自动选择索引。

> 在 `to_tsvector(...)` 表达式上创建 GIN 属性索引，需要 AgensGraph 2.17 或更高版本。

## 为提升后的列建立索引 {#indexing-a-promoted-column}

从 2.18 起，可以将属性[提升为真正的类型列](/zh/agensgraph/querying/typed-columns/)，从而消除逐行读取 `jsonb` 和执行 `::text` 转换的开销。`ALTER VLABEL movie ADD COLUMN plot text GENERATED` 会映射与列同名的属性，此处为 `plot`；`GENERATED (sourceKey)` 则映射另一个名称的键。查询始终使用属性名，而不是列名，因为解析依据的是属性键。

提升属性时，需要重建本页的索引，因为它是属性上的*表达式*索引。表达式属性索引建立在 jsonb 属性包之上，而提升后的键会从列中读取，两者不再匹配。

此时应使用 SQL 直接为列建立索引。`\dGi` 仍然会列出它，查询也能使用它：

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

现在 `m.plot` 不再需要 `::text`，因为提升后的列已经是 `text` 类型。参见[表达式属性索引建立在属性包上](/zh/agensgraph/querying/typed-columns/#an-expression-property-index-is-built-over-the-bag)。

## GraphRAG {#graphrag}

全文搜索也可以为图遍历提供种子。先找到文本与问题最匹配的电影，再沿关系扩展，为语言模型收集相连的上下文。

这是[向量搜索](/zh/agensgraph/guides/search/vector/)中 GraphRAG 示例的词法版本。当问题中包含名称、代码、精确短语等特定词项时，关键词搜索通常比嵌入向量处理得更好，这正是该方法的适用场景。

[示例数据集](/zh/agensgraph/get-started/example-dataset/)已经通过 `related_to` 边连接了系列续集和主题相关的电影，因此下面的遍历有可沿用的关系。

单条 Cypher 查询按电影与问题（此处为词项 `resistance`）的全文相关性排序，保留最佳匹配，再扩展到其邻居：

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

`WHERE` 过滤与 `WITH … ORDER BY rank LIMIT` 选出文本最匹配查询的电影。它们就是*种子*，这里是两部《终结者》电影。第二个 `MATCH` 沿 `related_to` 边收集相关电影。

种子及其邻居组成传给模型的上下文。注意，遍历到达了《黑客帝国》。关键词 `resistance` 本身没有匹配这部电影，但“与机器作战”的共同主题将它与《终结者》系列连接起来。若要在扩展前结合词法检索与语义（向量）检索，参见[混合搜索](/zh/agensgraph/guides/search/hybrid/)。

若要通过框架完成同样的检索，而不是手写查询，参见 [AI 与 LLM 集成](/zh/agensgraph/drivers/ai-integrations/)。
