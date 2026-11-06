---
title: "使用 pgvector 进行向量相似性检索"
description: "pgvector 是一个用于向量相似性检索的开源插件。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/advanced-analytics/pgvector-search.md"
---

它支持精确和近似最近邻检索，以及 L2 距离、内积和余弦距离。更多详情请参见 [pgvector/pgvector：Postgres 的开源向量相似性检索](https://github.com/pgvector/pgvector)。

Apache Cloudberry 允许通过 SQL 语句使用 pgvector 进行数据存储、查询、索引、混合检索等操作。本文介绍如何在 Apache Cloudberry 中使用 pgvector。

> [!NOTE]
> pgvector 扩展由专门的 pgvector 社区维护，但 Cloudberry 致力于确保它在本平台中的兼容性和易用性。这里有一个[分叉的 pgvector 版本](https://github.com/cloudberry-contrib/pgvector)，由社区成员贡献并针对 Cloudberry 定制；但请注意，它不是作为官方 Cloudberry 项目维护的。

## 快速开始 {#quick-start}

启用扩展（在每个要使用它的数据库中执行一次）：

``` sql
CREATE EXTENSION vector;
```

创建一个 3 维向量列：

``` sql
CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));
```

插入向量数据：

``` sql
INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]');
```

按 L2 距离获取最近邻：

``` sql
SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;
```

注意：内积使用 `<#>`，余弦距离使用 `<=>`。

## 存储数据 {#store-data}

创建带向量列的表：

``` sql
CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));
```

或者向已有表添加向量列：

``` sql
ALTER TABLE items ADD COLUMN embedding vector(3);
```

插入向量：

``` sql
INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]');
```

插入并更新向量：

``` sql
INSERT INTO items (id, embedding) VALUES (1, '[1,2,3]'), (2, '[4,5,6]')
    ON CONFLICT (id) DO UPDATE SET embedding = EXCLUDED.embedding;
```

更新向量：

``` sql
UPDATE items SET embedding = '[1,2,3]' WHERE id = 1;
```

删除向量：

``` sql
DELETE FROM items WHERE id = 1;
```

## 查询数据 {#query-data}

获取某个向量的最近邻：

``` sql
SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;
```

支持的距离函数如下：

- `<->`：L2 距离
- `<#>`：负内积
- `<=>`：余弦距离

获取某一行的最近邻：

``` sql
SELECT * FROM items WHERE id != 1 ORDER BY embedding <-> (SELECT embedding FROM items WHERE id = 1) LIMIT 5;
```

获取指定距离范围内的行：

``` sql
SELECT * FROM items WHERE embedding <-> '[3,1,2]' < 5;
```

注意：同时使用 `ORDER BY` 和 `LIMIT` 可以利用索引。

获取距离：

``` sql
SELECT embedding <-> '[3,1,2]' AS distance FROM items;
```

对于内积，需要乘以 `-1`（因为 `<#>` 返回负内积）。

``` sql
SELECT (embedding <#> '[3,1,2]') * -1 AS inner_product FROM items;
```

对于余弦相似性，使用 `1` 减去余弦距离。

``` sql
SELECT 1 - (embedding <=> '[3,1,2]') AS cosine_similarity FROM items;
```

计算向量的平均值：

``` sql
SELECT AVG(embedding) FROM items;
```

计算一组向量的平均值：

``` sql
SELECT category_id, AVG(embedding) FROM items GROUP BY category_id;
```

## 为数据建立索引 {#index-data}

默认情况下，pgvector 执行精确最近邻检索，可以提供较高的召回率。

如果需要更高的检索速度，可以添加索引来使用近似最近邻检索，但这可能会降低性能。与添加普通索引不同，添加近似索引后，**查询将返回不同的结果**。

pgvector 支持以下索引类型：

- HNSW
- IVFFlat

### HNSW 索引 {#hnsw-index}

**关于 HNSW**

HNSW（Hierarchical Navigable Small World，分层可导航小世界）是一种高效的近似最近邻检索算法，设计用于处理大规模、高维数据集。

HNSW 的基本原理如下：

> - 多级图结构：HNSW 通过构建多级图组织数据。在该图中，每个节点表示一个数据点（或向量），节点之间的边反映它们在空间中的相对邻近程度。
> - 检索优化：这种多级结构使检索过程能够快速跳过许多不相关的数据点，缩小查询向量的邻近区域，从而大幅提高查询效率。

HNSW 特别适用于以下场景：

> - 高维数据：HNSW 索引非常适合高维数据集，因为它擅长处理高维空间中的复杂邻近关系。
> - 大型数据集：HNSW 索引适合大型数据集，因为与许多其他类型的索引相比，它能更好地平衡查询速度和召回率。

创建 HNSW 索引需要更长时间并使用更多内存，但可以提供更好的查询性能（速度与召回率之间的权衡）。与 IVFFlat 不同，HNSW 不需要训练步骤，因此即使表中没有数据，也可以创建索引。

为计划使用的每个距离函数添加索引。

#### 创建 HNSW 索引 {#create-an-hnsw-index}

每种距离度量都有其适用场景。选择哪种方法创建索引，取决于希望优化的检索类型。例如，如果应用重点是获取方向相似但长度可能不同的向量，那么使用余弦距离创建的索引可能更合适。另一方面，如果关注向量之间的直线距离，则应选择基于 L2 距离的索引。

L2 距离：

``` sql
CREATE INDEX ON items USING hnsw (embedding vector_l2_ops);
```

内积：

``` sql
CREATE INDEX ON items USING hnsw (embedding vector_ip_ops);
```

余弦距离：

``` sql
CREATE INDEX ON items USING hnsw (embedding vector_cosine_ops);
```

可建立索引的向量最大维度为 2000。

#### HNSW 索引选项 {#hnsw-index-options}

- `m`：每层的最大连接数（默认值为 `16`）。
- `ef_construction`：用于构建图的动态候选列表大小（默认值为 `64`）。

``` sql
CREATE INDEX ON items USING hnsw (embedding vector_l2_ops) WITH (m = 16, ef_construction = 64);
```

较大的 `ef_construction` 值可以提供更高的召回率，但会增加索引构建时间并降低插入速度。

#### HNSW 索引查询选项 {#hnsw-index-query-options}

指定检索时动态候选列表的大小（默认值为 `40`）。值越大，召回率越高，但速度越慢。

``` sql
SET hnsw.ef_search = 100;
```

在事务中使用 `SET LOCAL`，可以将其应用于单个查询：

``` sql
BEGIN;
SET LOCAL hnsw.ef_search = 100;
SELECT ...
COMMIT;
```

#### HNSW 索引构建时间 {#hnsw-index-build-time}

当 HNSW 索引的内部图结构能够装入 `maintenance_work_mem` 时，索引构建速度会大幅提升。

``` sql
SET maintenance_work_mem = '8GB';
```

如果图不再适合装入内存，系统会发出通知：

``` sql
NOTICE:  hnsw graph no longer fits into maintenance_work_mem after 100000 tuples
DETAIL:  Building will take significantly more time.
HINT:  Increase maintenance_work_mem to speed up builds.
```

注意：不要将 `maintenance_work_mem` 设置得过高，因为这会耗尽服务器内存。

与其他索引类型一样，加载初始数据后再创建索引会更快。

``` sql
SET max_parallel_maintenance_workers = 7; -- Including the leader thread
```

如果需要更多工作进程，可能还需要增加 `max_parallel_workers`（默认值为 `8`）。

#### 查看 HNSW 索引进度 {#view-hnsw-index-progress}

创建 HNSW 索引时，可以检查构建进度：

``` sql
SELECT phase, round(100.0 * blocks_done / nullif(blocks_total, 0), 1) AS "%" FROM pg_stat_progress_create_index;
```

HNSW 索引构建过程包含以下阶段：

1. `initializing`：索引创建的初始阶段。在此阶段，系统准备开始构建索引所需的全部资源和配置。
2. `loading tuples`：将数据点（或向量）添加到多级图，并建立相应的连接。

### IVFFlat 索引 {#ivfflat-index}

**关于 IVFFlat**

IVFFlat 索引是一种适用于大型数据集的高效向量检索方法，尤其适合近似最近邻（ANN）检索。

IVFFlat 索引的基本原理如下：

> - 分区检索空间：IVFFlat 将数据划分为多个“列表”。这些列表通过对数据集进行聚类创建（例如使用 K-means 算法），每个列表表示数据空间中的一个集群。
> - 降低检索复杂度：系统不再搜索整个数据集，而是先确定检索向量可能属于哪些列表（或集群），然后只在这些列表中检索，从而减少计算时间。

IVFFlat 特别适用于以下场景：

> - 大型数据集：对于包含大量向量的数据集，完整检索（检查每个向量）可能非常耗时。IVFFlat 通过聚类和分区优化检索过程。
> - 近似检索：IVFFlat 是一种近似最近邻检索方法，适用于需要快速响应且可以接受检索结果存在一定误差的场景。

要使用 IVFFlat 获得良好的召回率，请遵循以下最佳实践：

> - 在表中插入一些数据后再创建索引。
> - 选择适当的列表数量。对于最多 100 万行的表，建议使用行数除以 1000 作为列表数量。对于超过 100 万行的表，使用行数的平方根作为列表数量。
> - 在查询期间指定适当的探针数（探针数越多，召回率越高，但查询越慢）。建议先尝试列表数量的平方根。为计划使用的每个距离函数添加索引。

#### 创建 IVFFlat 索引 {#create-an-ivfflat-index}

每种距离度量都有其适用场景。选择哪种方法创建索引，取决于希望优化的检索类型。例如，如果应用重点是寻找方向相似但长度可能不同的向量，那么使用余弦距离创建的索引可能更合适。另一方面，如果关注向量之间的直线距离，则应选择基于 L2 距离的索引。

`lists` 参数指定分区（列表）的数量。

L2 距离：

``` sql
CREATE INDEX ON items USING ivfflat (embedding vector_l2_ops) WITH (lists = 100);
```

内积：

``` sql
CREATE INDEX ON items USING ivfflat (embedding vector_ip_ops) WITH (lists = 100);
```

余弦距离：

``` sql
CREATE INDEX ON items USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

注意：Apache Cloudberry 当前支持为最多 2000 维的向量建立索引。

#### 指定探针数 {#specify-the-number-of-probes}

探针数表示近似最近邻检索期间系统检查的“列表”数量。这些列表是通过 K-means 等聚类算法创建的数据集子集。增加探针数意味着系统检查更多列表来获取最近邻，从而提高准确性。探针数越大，检索准确性越高，但计算开销也越大，检索速度越慢。因此，应根据具体使用场景在探针数这一参数上进行权衡。

指定探针数（默认值为 `1`）：

``` sql
SET ivfflat.probes = 10;
```

如果选择较大的探针数，可能会损失一些影响速度的性能，但可以获得更高的召回率。也可以将其设置为列表数量，以执行精确最近邻检索（此时优化器确实会使用索引）。

在事务中使用 `SET LOCAL`，为单个查询设置探针数：

``` sql
BEGIN;
SET LOCAL ivfflat.probes = 10;
SELECT ...
COMMIT;
```

#### 查看 IVFFlat 索引进度 {#view-ivfflat-index-progress}

可以在创建索引期间检查索引进度：

``` sql
SELECT phase, tuples_done, tuples_total FROM pg_stat_progress_create_index;
```

进度阶段包括：

1. `initializing`：索引创建的初始阶段。系统在此阶段准备所需的全部资源和配置。
2. `performing k-means`：使用 k-means 算法将向量数据集划分为多个列表（或集群）。
3. `sorting tuples`：对数据（元组）排序。排序依据是向量值或其所属列表，用于优化索引结构并提高检索效率。
4. `loading tuples`：将数据实际加载到索引结构中，即将元组数据写入索引，以确保其满足索引要求。

注意：`tuples_done` 和 `tuples_total` 只有在 loading tuples 阶段才会填充。

### 在索引中使用过滤器 {#use-filters-in-indexes}

创建索引时，可以使用 `WHERE` 子句限制索引范围。这种方法可以让向量检索只考虑满足特定条件的行，从而提高检索效率和准确性。

``` sql
SELECT * FROM items WHERE category_id = 123 ORDER BY embedding <-> '[3,1,2]' LIMIT 5;
```

为精确检索在一个或多个 `WHERE` 列上创建索引：

``` sql
CREATE INDEX ON items (category_id);
```

为近似检索在向量列上创建部分索引：

``` sql
CREATE INDEX ON items USING ivfflat (embedding vector_l2_ops) WITH (lists = 100) WHERE (category_id = 123);
```

对于多个 `WHERE` 列取不同值的近似检索，请使用分区：

``` sql
CREATE TABLE items (embedding vector(3), category_id int) PARTITION BY LIST(category_id);
```

## 混合检索 {#hybrid-search}

使用 Apache Cloudberry 全文检索执行混合检索：

``` sql
SELECT id, content FROM items, plainto_tsquery('hello search') query
    WHERE textsearch @@ query ORDER BY ts_rank_cd(textsearch, query) DESC LIMIT 5;
```

## pgvector 性能 {#pgvector-performance}

使用 `EXPLAIN ANALYZE` 调试性能：

``` sql
EXPLAIN ANALYZE SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;
```

### 精确检索 {#exact-search}

要在没有索引的情况下加快查询速度，可以增加 `max_parallel_workers_per_gather` 参数的值。

``` sql
SET max_parallel_workers_per_gather = 4;
```

如果向量已经规范化为长度 `1`（例如[OpenAI 嵌入](https://platform.openai.com/docs/guides/embeddings/which-distance-function-should-i-use)），使用内积可以获得最佳性能。

``` sql
SELECT * FROM items ORDER BY embedding <#> '[3,1,2]' LIMIT 5;
```

### 近似检索 {#approximate-search}

要加快带索引的查询，可以增加倒排列表的数量（代价是召回率会有所降低）。

``` sql
CREATE INDEX ON items USING ivfflat (embedding vector_l2_ops) WITH (lists = 1000);
```

以上是 pgvector 最近邻检索和性能优化的一些指导。可以根据需求和数据结构，按照这些建议进行调整和优化。
