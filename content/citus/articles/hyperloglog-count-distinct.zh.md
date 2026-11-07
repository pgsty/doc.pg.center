---
title: PostgreSQL 上使用 HyperLogLog 实现分布式去重计数
description: 使用 HyperLogLog 在分布式 PostgreSQL 中高效估算去重计数，了解算法原理和查询示例。
weight: 60
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/hyperloglog-count-distinct?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
linkTitle: HLL 去重计数
---

**原始文章：** [Burak Yucesoy · 2017 年 4 月 4 日](https://www.citusdata.com/blog/2017/04/04/distributed-count-distinct-with-postgresql/)。中文整理：[PGSTY](https://pgsty.com/)。

在数据库上运行 `SELECT COUNT(DISTINCT)` 是再常见不过的操作。一些应用的分析仪表板会突出显示去重用户数、产品数、访问次数等指标。传统的 `SELECT COUNT(DISTINCT)` 查询在单机环境中表现良好，但在分布式系统中却是个难题。这类查询不能简单地下推到工作节点后再将结果相加，因为不同工作节点上可能存在重复记录。你可以改用以下方法：

- 将所有去重后的数据拉取到一台机器上计数。（无法扩展）
- 执行 map/reduce。（可以扩展，但速度慢）

近似算法或概要算法（sketch）可以帮助解决这类问题。概要算法是一类概率算法，能在数学上可证明的误差范围内高效生成近似结果。这类算法有很多，本文只关注其中一种：HyperLogLog（[HLL](https://github.com/aggregateknowledge/postgresql-hll)）。HLL 擅长估算列表中的不同元素数量。理解其内部原理，有助于说明为什么 HLL 能以可扩展的方式解决去重计数问题。本文将介绍 HLL 如何用于分布式场景，并给出使用示例。

## HLL 的内部原理是什么？ {#what-does-hll-do-behind-the-curtains}

### 对所有元素计算哈希值 {#hash-all-elements}

HLL 和几乎所有其他概率计数算法都依赖数据的均匀分布。现实中的数据并不均匀，因此 HLL 首先对每个元素计算哈希值，让分布更加均匀。均匀分布意味着元素的每一位取 0 或 1 的概率均为 0.5。除了改善分布，哈希还能让 HLL 以同样的方式处理所有数据类型。只要某种数据类型有相应的哈希函数，就可以用 HLL 估算其基数。

### 在数据中寻找罕见模式 {#observe-the-data-for-rare-patterns}

计算所有元素的哈希值后，HLL 会检查每个哈希值的二进制表示，主要寻找那些不太可能出现的位模式。出现这样的罕见模式，意味着正在处理的数据集很大。

为此，HLL 会检查每个元素哈希值的前导零位数，并找出其中的最大值。基本思路是：要观察到 k 个前导零，需要进行 \(2^{k+1}\) 次试验（即检查这么多个哈希后的数值）。因此，如果数据集中前导零位数的最大值为 k，HLL 就估计其中约有 \(2^{k+1}\) 个不同元素。

- HLL 的内存占用很低。对于最大数值 n，只需存储 *log log n* 位。例如，如果将元素哈希为 64 位整数，只需存储 6 位就能进行估算。与必须记住所有值的方法相比，这尤其节省内存。
- 只需遍历一次数据，就能找出前导零位数的最大值。
- 可以处理流式数据。算出前导零位数的最大值后，如果有新数据到达，无需重新遍历整个数据集，就能将其纳入计算。只需找出每个新元素的前导零位数，与整个数据集已有的最大值比较，并在必要时更新最大值。
- 可以高效合并两个独立数据集的估算结果。只需选取两者中较大的前导零位数，作为合并后数据集的最大值即可。因此，可以将数据划分为多个分片，分别估算基数，再合并结果。这种性质称为可加性，使 HLL 能够用于分布式系统。

### 随机平均 {#stochastic-averaging}

这些预测可能并不精确，而且总是形如 \(2^k\)。如果数据分布不够均匀，估算结果还可能出现偏差。

一种可能的解决办法是用不同的哈希函数重复上述过程，再取平均值。这可能有效，但对所有数据反复计算哈希值的开销很高。HLL 使用一种称为随机平均的方法来解决这个问题：将数据分到多个桶中，对每个桶分别使用前述算法，再对结果取平均值。具体做法是用哈希值的前几位决定元素所属的桶，用剩余位计算前导零位数的最大值。

还可以通过选择桶的数量来控制精度。每个桶需要存储 *log log n* 位。由于每份估算只占 *log log n* 位，即使创建大量桶，内存占用仍然很小。处理大规模数据时，这一点尤其重要。要合并两份估算，需要先逐桶合并，再取平均值。因此，如果计划执行合并，就应保留每个桶的前导零位数最大值。

### 还有什么？ {#more}

HLL 还会执行其他操作以提高估算精度，不过，观察位模式和随机平均是其核心。经过这些优化，HLL 只需 1.5 kB 内存，就能以约 2% 的典型误差率估算数据集基数。使用更多内存还可以提高精度。

## 分布式系统中的 HLL {#hll-in-distributed-systems}

如前所述，HLL 具有可加性。可以将数据集分为多个部分，用 HLL 分别估算每部分的不同元素数量，再高效合并 HLL 中间结果，得到全部数据的不同元素数量，无需重新访问原始数据。

如果处理的数据规模很大，并且分散存储在不同的物理机器上，就可以使用 HLL 对全部数据进行去重计数，而不必将所有数据拉取到同一个位置。事实上，Citus 可以代你完成这项工作。PostgreSQL 有一个与 Citus 完全兼容的 [HLL 扩展](https://github.com/aggregateknowledge/postgresql-hll)。安装该扩展并完成配置后，在分布式表上运行 COUNT(DISTINCT) 查询时，Citus 会自动使用 HLL，无需额外操作。

## 动手使用 HLL {#hands-on-with-hll}

> [!NOTE]
> 本文提到了 Citus Cloud 服务。Amazon Web Service（AWS）上的 Citus Cloud 已不再接受新用户注册。如果你刚开始使用 Citus，仍然可以使用它：Citus 是开源软件，也作为 Azure Database for PostgreSQL 中完全集成的部署选项在 Microsoft Azure 云上提供。
>
> 更多信息请参阅[托管服务](/citus/installation/citus-cloud/)。

### 设置 {#setup}

这里使用 Citus Cloud 和 GitHub 事件数据来演示 HLL。关于 Citus Cloud 和该数据集的更多信息，请参阅[在 Citus 上开始使用 GitHub 事件数据](https://www.citusdata.com/blog/2017/01/27/getting-started-with-github-events-data/)。创建 Citus Cloud 实例并通过 psql 连接后，可以在协调节点上运行以下命令，创建 HLL 扩展：

```sql
CREATE EXTENSION hll;
```

然后，设置 `citus.count_distinct_error_rate` 配置值，启用近似去重计数。该值越小，预期结果越准确，但计算时间和内存开销也越大。这里将其设为 0.005。

```sql
SET citus.count_distinct_error_rate TO 0.005;
```

可以使用 `github_events` 表：

```psql
CREATE TABLE github_events
(
    event_id bigint,
    event_type text,
    event_public boolean,
    repo_id bigint,
    payload jsonb,
    repo jsonb,
    user_id bigint,
    org jsonb,
    created_at timestamp
);

SELECT create_distributed_table('github_events', 'user_id');

\COPY github_events FROM large_events.csv CSV
```

### 示例 {#examples}

将表分布后，可以运行普通的 COUNT(DISTINCT) 查询，统计有多少不同用户创建了事件：

```sql
SELECT
    COUNT(DISTINCT user_id)
FROM
    github_events;
```

返回结果应类似于：

```text
    .
     count
    --------
     264227

    (1 row)
```

这个查询看起来与 HLL 毫无关系。但只要将 `citus.count_distinct_error_rate` 设为大于 0 的值，并执行 `COUNT(DISTINCT)` 查询，Citus 就会自动使用 HLL。对于这样的简单用例，甚至不需要修改查询。创建过事件的精确去重用户数为 264198，因此误差率略大于 0.0001。

还可以通过条件筛选结果。例如，查询有多少不同用户创建了 PushEvent：

```sql
SELECT
    COUNT(DISTINCT user_id)
FROM
    github_events
WHERE
    event_type = 'PushEvent'::text;
```

返回结果为：

```text
    .
     count
    --------
     157471

    (1 row)
```

同样，这个查询的精确去重计数为 157154，误差率大于 0.002。

### 结论 {#conclusion}

如果在扩展 PostgreSQL 的 `count (distinct)` 查询时遇到困难，而且可以接受足够接近精确值的计数，不妨试试 HLL。

## 相关内容 {#related-content}

- [专题概览](/citus/articles/)
- [实时事件聚合](/citus/articles/aggregation/)
