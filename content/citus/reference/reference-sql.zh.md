---
title: 在 Citus 分布式表上运行 SQL 查询
description: 本文介绍如何使用标准 PostgreSQL 查询在 Citus 中查询分布式表。
weight: 100
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/reference-sql?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
---

如前文所述，Citus 扩展了最新版本的 PostgreSQL，使其支持分布式执行。使用 Citus 时，可以在协调节点上运行标准 PostgreSQL [SELECT](http://www.postgresql.org/docs/current/static/sql-select.html) 查询。对于包含复杂筛选、分组、排序和 `JOIN` 的 SELECT 查询，Citus 会将其并行化以提升性能。总体而言，Citus 将 SELECT 查询拆分成较小的片段，分配给工作节点并监督执行，随后合并结果（必要时进行排序），将最终结果返回用户。

以下各节介绍 Citus 可以运行的不同类型的查询。

## 聚合函数 {#aggregate-functions}

Citus 支持并能并行执行 PostgreSQL 支持的大多数聚合函数，包括用户自定义聚合。聚合采用以下三种执行方式，按优先级排序：

1. 如果按表的分布列分组，Citus 可以将整个查询下推到各工作节点执行。这种情况下支持所有聚合，并在工作节点上并行执行。（计划使用的自定义聚合必须安装在工作节点上。）
2. 如果*不是*按表的分布列分组，Citus 仍可针对具体情况优化。对于 `sum()`、`avg()`、`count(distinct)` 等特定聚合，Citus 内置了规则，将查询重写为工作节点上的*部分聚合*。例如，计算平均值时，Citus 从各工作节点获取总和与计数，再由协调节点计算最终平均值。

   具有特殊处理规则的聚合完整列表如下：

   ```sql
   avg, min, max, sum, count, array_agg, jsonb_agg, jsonb_object_agg, json_agg, json_object_agg, bit_and, bit_or, bool_and, bool_or, every, hll_add_agg, hll_union_agg, topn_add_agg, topn_union_agg, any_value, tdigest(double precision, int), tdigest_percentile(double precision, int, double precision), tdigest_percentile(double precision, int, double precision\[\]), tdigest_percentile(tdigest, double precision), tdigest_percentile(tdigest, double precision\[\]), tdigest_percentile_of(double precision, int, double precision), tdigest_percentile_of(double precision, int, double precision\[\]), tdigest_percentile_of(tdigest, double precision), tdigest_percentile_of(tdigest, double precision\[\])
   ```
3. 最后的手段是从工作节点拉取所有行，在协调节点上聚合。如果聚合既不按分布列分组，也不属于预定义的特殊情况，Citus 就会退回这种方式。这会增加网络开销；数据集过大时，还可能耗尽协调节点的资源。（如下例所示，可以禁用这种回退行为。）

   查询的小改动可能改变执行方式，导致意外的性能下降。例如，按非分布列分组的 `sum(x)` 可以分布式执行，但 `sum(distinct x)` 必须将全部输入记录拉到协调节点。

   一个列的计算方式就可能影响整个查询的执行。下面的例子中，如果 `sum(distinct value2)` 必须在协调节点上分组，`sum(value1)` 也必须如此，即使它单独执行时没有问题。

   ```sql
   SELECT sum(value1), sum(distinct value2) FROM distributed_table;
   ```

   为避免意外地将数据拉到协调节点，可以设置以下全局用户配置（GUC）：

   ```sql
   SET citus.coordinator_aggregation_strategy TO 'disabled';
   ```

   禁用协调节点聚合策略后，*第三类*聚合查询将完全无法运行。

### Count(distinct) 聚合 {#countdistinct-aggregates}

Citus 以多种方式支持 `count(distinct)` 聚合。如果 `count(distinct)` 聚合针对分布列，Citus 可以直接将查询下推到工作节点。否则，Citus 在各工作节点执行 select distinct 语句，将列表返回协调节点，再计算最终数量。

工作节点上的不同值越多，传输这些数据就越慢，尤其是查询包含多个 `count(distinct)` 聚合时，例如：

```sql
-- multiple distinct counts in one query tend to be slow
SELECT count(distinct a), count(distinct b), count(distinct c)
FROM table_abc;
```

对于这类查询，工作节点上生成的 select distinct 语句实际上会产生行的笛卡尔积，并将其传输到协调节点。

为了提高性能，可以按照以下步骤改用近似计数：

1. 在所有 PostgreSQL 实例（协调节点及所有工作节点）上下载并安装 hll 扩展。

   hll 扩展定义了 HyperLogLog（HLL）数据结构，获取方式参见 [postgresql-hll GitHub 仓库](https://github.com/citusdata/postgresql-hll)。
2. 在协调节点运行以下命令，在所有 PostgreSQL 实例中创建 hll 扩展：

   ```sql
   CREATE EXTENSION hll;
   ```
3. 设置 `citus.count_distinct_error_rate`，启用 `count_distinct` 近似计算。该配置值越小，预期结果越精确，但计算耗时越长。这里将其设置为 *0.005*。

   ```sql
   SET citus.count_distinct_error_rate to 0.005;
   ```

完成后，`count(distinct)` 聚合会自动改用 HLL，无需修改查询。此时可以对表的任意列执行近似去重计数查询。

#### HyperLogLog 列 {#hyperloglog-column}

有些用户已经将数据存储为 HLL 列。这时可以调用 `hll_union_agg(hll_column)` 动态汇总数据。

### 估算前 n 项 {#estimating-the-top-n-items}

通过计数、排序和行数限制，可以计算集合中的前 *n* 项。不过，数据量增加后，这种方法会变慢且消耗大量资源。使用近似算法效率更高。

PostgreSQL 的开源 [TopN 扩展](https://github.com/citusdata/postgresql-topn)可以快速返回 *top-n* 查询的近似结果。该扩展将排名靠前的值物化为 JSON 数据，可增量更新这些值，也可按需合并不同时间区间的结果。

#### 基本操作 {#basic-operations}

在了解 TopN 的实际应用前，先看几个基本操作。首先，`topn_add` 会更新 JSON 对象，记录某个键出现的次数：

```sql
-- starting from nothing, record that we saw an "a"
select topn_add('{}', 'a');
-- => {"a": 1}

-- record the sighting of another "a"
select topn_add(topn_add('{}', 'a'), 'a');
-- => {"a": 2}
```

该扩展还提供了扫描多个值的聚合函数：

```sql
-- for normal_rand
create extension tablefunc;

-- count values from a normal distribution
SELECT topn_add_agg(floor(abs(i))::text)
  FROM normal_rand(1000, 5, 0.7) i;
-- => {"2": 1, "3": 74, "4": 420, "5": 425, "6": 77, "7": 3}
```

当不同值的数量超过阈值时，聚合会丢弃出现频率最低的值的信息，以控制空间占用。可通过全局用户配置 `topn.number_of_counters` 控制该阈值，默认值为 *1000*。

#### 实际示例 {#realistic-example}

下面用一个更贴近实际的例子说明 TopN 的用法。我们将导入 2000 年的亚马逊商品评论，并使用 TopN 快速查询。首先下载数据集：

```bash
curl -L https://examples.citusdata.com/customer_reviews_2000.csv.gz | \
  gunzip > reviews.csv
```

接着，将其导入分布式表：

```psql
CREATE TABLE customer_reviews
(
    customer_id TEXT,
    review_date DATE,
    review_rating INTEGER,
    review_votes INTEGER,
    review_helpful_votes INTEGER,
    product_id CHAR(10),
    product_title TEXT,
    product_sales_rank BIGINT,
    product_group TEXT,
    product_category TEXT,
    product_subcategory TEXT,
    similar_product_ids CHAR(10)[]
);

SELECT create_distributed_table('customer_reviews', 'product_id');

\COPY customer_reviews FROM 'reviews.csv' WITH CSV
```

然后添加扩展，创建目标表以保存 TopN 生成的 json 数据，并应用前面介绍的 `topn_add_agg` 函数。

```sql
-- run below command from coordinator, it will be propagated to the worker nodes as well
CREATE EXTENSION topn;

-- a table to materialize the daily aggregate
CREATE TABLE reviews_by_day
(
  review_date date unique,
  agg_data jsonb
);

SELECT create_reference_table('reviews_by_day');

-- materialize how many reviews each product got per day per customer
INSERT INTO reviews_by_day
  SELECT review_date, topn_add_agg(product_id)
  FROM customer_reviews
  GROUP BY review_date;
```

现在可以直接对 `reviews_by_day` 使用 TopN，而无需在 `customer_reviews` 上编写复杂的窗口函数。例如，下面的查询找出前五天中每天评论次数最多的商品：

```sql
SELECT review_date, (topn(agg_data, 1)).*
FROM reviews_by_day
ORDER BY review_date
LIMIT 5;
```

```text
┌─────────────┬────────────┬───────────┐
│ review_date │    item    │ frequency │
├─────────────┼────────────┼───────────┤
│ 2000-01-01  │ 0939173344 │        12 │
│ 2000-01-02  │ B000050XY8 │        11 │
│ 2000-01-03  │ 0375404368 │        12 │
│ 2000-01-04  │ 0375408738 │        14 │
│ 2000-01-05  │ B00000J7J4 │        17 │
└─────────────┴────────────┴───────────┘
```

TopN 创建的 JSON 字段可以使用 `topn_union` 和 `topn_union_agg` 合并。使用后者可以合并第一个月的全部数据，列出该月评论次数最多的五件商品。

```sql
SELECT (topn(topn_union_agg(agg_data), 5)).*
FROM reviews_by_day
WHERE review_date >= '2000-01-01' AND review_date < '2000-02-01'
ORDER BY 2 DESC;
```

```text
┌────────────┬───────────┐
│    item    │ frequency │
├────────────┼───────────┤
│ 0375404368 │       217 │
│ 0345417623 │       217 │
│ 0375404376 │       217 │
│ 0375408738 │       217 │
│ 043936213X │       204 │
└────────────┴───────────┘
```

更多信息和示例参见 [TopN readme](https://github.com/citusdata/postgresql-topn/blob/master/README.md)。

### 百分位数计算 {#percentile-calculations}

在大量行上计算精确百分位数可能代价过高，因为协调节点必须接收所有行才能完成最终排序和处理。另一种方式是在工作节点上使用*概要算法（sketch algorithm）*并行求近似值。协调节点只需合并压缩后的摘要即可得到最终结果，无需读取全部行。

一种常见的百分位数概要算法使用名为 `tdigest` 的压缩数据结构，PostgreSQL 的 [t-digest 扩展](https://github.com/tvondra/tdigest)提供了该算法。Citus 已集成对此扩展的支持。

在 Citus 中使用 `tdigest` 的步骤如下：

1. 在所有 PostgreSQL 节点（协调节点和全部工作节点）上下载并安装 `tdigest` 扩展。安装说明参见 [t-digest 扩展 GitHub 仓库](https://github.com/tvondra/tdigest)。
2. 在数据库中创建 `tdigest` 扩展。在协调节点运行以下命令：

   ```sql
   CREATE EXTENSION tdigest;
   ```

   协调节点也会将命令传播到工作节点。

查询中使用该扩展定义的聚合函数时，Citus 会在适用的情况下重写查询，将部分 `tdigest` 计算下推到工作节点。

传入聚合函数的 `compression` 参数可以控制 `tdigest` 的精度，需要在精度与工作节点、协调节点之间交换的数据量之间权衡。有关 `tdigest` 扩展中聚合函数的完整用法，请参阅官方 [t-digest 扩展 GitHub 仓库](https://github.com/tvondra/tdigest)中的文档。

## LIMIT 下推 {#limit-pushdown}

Citus 还会尽可能将行数限制子句下推到工作节点的分片上，以减少网络传输的数据量。

不过，有时包含 `LIMIT` 的 `SELECT` 查询需要从各分片获取所有行，才能生成精确结果。例如，查询要求按聚合列排序时，需要取得所有分片上该列的结果，才能确定最终聚合值。大量网络传输会削弱 `LIMIT` 子句的性能收益。对于这类场景，如果近似结果具有实际意义，Citus 提供了网络开销更低的近似 `LIMIT` 选项。

`LIMIT` 近似计算默认禁用，可通过配置参数 `citus.limit_clause_row_fetch_count` 启用。Citus 据此限制各任务返回给协调节点进行聚合的行数，因此最终结果可能是近似值。提高此上限可提升最终结果的精度，同时仍限制从工作节点拉取的最大行数。

```sql
SET citus.limit_clause_row_fetch_count to 10000;
```

## 分布式表上的视图 {#views-on-distributed-tables}

Citus 支持分布式表上的所有视图。有关视图语法和功能，参见 PostgreSQL 的 [CREATE VIEW](https://www.postgresql.org/docs/current/static/sql-createview.html) 文档。

不同视图可能生成效率不同的查询计划。有关识别和改善视图性能问题的更多信息，参见 `subquery_perf`。（视图在内部被视为子查询。）

Citus 也支持物化视图，并将其作为本地表存储在协调节点上。

## 连接 {#joins}

Citus 支持任意数量表之间的等值连接，不受表大小和分布方式限制。查询规划器根据表的分布情况，选择最优的连接方法和顺序。它会评估多种可能的连接顺序，生成网络数据传输量最小的连接计划。

### 共置连接 {#colocated-joins}

两个表共置时，可以基于共有的分布列高效连接。共置连接是连接两个大型分布式表最有效的方式。

在内部，Citus 协调节点通过分布列元数据，判断共置表的哪些分片可能与另一表的分片匹配。利用这些元数据，Citus 可以剪除不可能产生匹配连接键的分片对。剩余分片对的连接在工作节点上并行执行，随后将结果返回协调节点。

> [!NOTE]
> 请确保两个表的分片数相同，且分布列的类型完全一致。在 int 和 bigint 这样略有不同的类型之间进行连接，也可能引发问题。

### 参考表连接 {#reference-table-joins}

将 [参考表](/citus/reference/reference-ddl/#reference-tables) 用作*维度表*，可以高效地连接大型*事实表*。Citus 将参考表完整复制到所有工作节点，因此参考表连接可拆分为各工作节点上的本地连接并行执行。它类似于更灵活的共置连接：参考表不按特定列分布，因此可以按任意列连接。

参考表也可以与协调节点上的本地表连接。

### 外连接下推（Citus 13.2） {#outer-join-pushdown-citus-132}

在 Citus 13.2 中，当外侧是重复出现在各节点上的关系（例如参考表或中间结果）时，符合条件的 LEFT 和 RIGHT 外连接可以下推到工作节点。规划器会在重复关系一侧注入分片区间约束，以保证正确性。这样就能在工作节点上执行连接，避免在协调节点连接以及产生大量中间结果。

- 默认启用，可通过 `citus.enable_recurring_outer_join_pushdown` 禁用。
- 适用于能够推导分片区间的重复关系外连接（通常涉及哈希分布表），包括外侧为参考表、中间结果或集合返回函数的情况。
- 规划器根据分片哈希范围推导约束，并将其注入重复关系一侧的扫描（参考表、中间结果或 SRF）。
- 规划器会检查适用条件，详见 Citus 源码中的 `CanPushdownRecurringOuterJoin`。

示例：

```sql
EXPLAIN (COSTS OFF)
SELECT *
FROM product_categories pc
LEFT JOIN products_table pt
  ON pc.category_id = pt.product_id;
```

**13.2 之前**（参考表连接不下推）：

```text
Custom Scan (Citus Adaptive)
  -> Distributed Subplan ...
  -> Task
       -> Hash Right Join
            Hash Cond: (intermediate_result.product_id = pc.category_id)
```

**Citus 13.2**（添加约束后下推）：

```text
Custom Scan (Citus Adaptive)
  Task Count: 32
  -> Task
       Node: host=localhost port=9701 dbname=postgres
       -> Hash Right Join
            Hash Cond: (pt.product_id = pc.category_id)
            -> Seq Scan on products_table_102072 pt
            -> Hash
                 -> Seq Scan on product_categories_102106 pc
                    Filter: ((category_id IS NULL) OR (btint4cmp('-2147483648', hashint8(category_id::bigint)) < 0
                             AND btint4cmp(hashint8(category_id::bigint), '-2013265921') <= 0))
```

### 重分区连接 {#repartition-joins}

有时需要基于分布列以外的列连接两个表。为此，Citus 可以在查询时动态重新分区，支持按非分布键列进行连接。

这种情况下，查询优化器根据表的分布列、连接键和大小决定哪些表需要重新分区。重新分区后，只需连接相关的分片对，从而大幅减少网络数据传输量。

一般而言，共置连接比重分区连接更高效，因为后者需要重新分发数据。因此，应尽可能按常用连接键分布表。

## 相关内容 {#related-content}

- [数据定义语言（DDL）操作参考](/citus/reference/reference-ddl/)
- [数据修改语言（DML）操作参考](/citus/reference/reference-dml/)
- [Citus SQL 参考概述](/citus/reference/)
