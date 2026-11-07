---
title: 在 PostgreSQL 中使用 HyperLogLog 实现高效汇总表
description: 了解如何将 HyperLogLog 与 PostgreSQL 中的汇总表配合使用，以便高效聚合和查询大型数据集。
weight: 50
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/efficient-rollup?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
linkTitle: HLL 汇总表
---

**原始文章：** [Burak Yucesoy · 2017 年 6 月 30 日](https://www.citusdata.com/blog/2017/06/30/efficient-rollup-with-hyperloglog-on-postgres/)。中文整理：[PGSTY](https://pgsty.com/)。

在 PostgreSQL 中，如果不再需要对旧数据进行详细分析，但仍需执行基本的聚合查询，通常会使用汇总表。

借助汇总表，可以针对仍需执行的查询预先聚合旧数据。这样就不必保留全部旧数据，而可以将其删除或转移到较慢的存储中，节省空间和计算资源。

本文先展示一个不使用 HyperLogLog（HLL）的 PostgreSQL 汇总表示例。

## 不使用 HLL 的汇总表：以 GitHub 事件数据为例 {#rollup-tables-without-hllusing-github-events-data-as-an-example}

这个 GitHub 数据集中的每条记录都代表一个在 GitHub 中创建的事件，并包含事件类型、创建日期、创建事件的用户等关键信息。更多信息请参阅[在 Citus 上开始使用 GitHub 事件数据](https://www.citusdata.com/blog/2017/01/27/getting-started-with-github-events-data/)。

如果想用图表展示每分钟创建的 GitHub 事件数，可以使用汇总表。有了汇总表，就不必为绘制图表而存储所有用户事件，只需按分钟聚合事件创建数量，并保存聚合后的数据。如果需要节省空间，之后就可以丢弃其余事件数据。

下面用 `github_events` 表演示这一过程：

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

\COPY github_events FROM events.csv CSV
```

在本例中，如果不经常对旧数据进行详细分析，就没有必要继续为其占用资源。可以改用汇总表，只在内存中保留必要信息。为此，创建如下汇总表：

```sql
CREATE TABLE github_events_rollup_minute
(
    created_at timestamp,
    event_count bigint
);
```

再用 INSERT/SELECT 填充它：

```sql
INSERT INTO github_events_rollup_minute(
    created_at,
    event_count
)
SELECT
    date_trunc('minute', created_at) AS created_at,
    COUNT(*) AS event_count
FROM github_events
GROUP BY 1;
```

现在可以将较旧、体积更大的数据存储在磁盘等较便宜的资源上，供将来访问，同时把 `github_events_rollup_minute` 表保留在内存中，用来构建分析仪表板。

上例按分钟聚合数据后，可以回答每小时、每天共创建多少事件之类的问题，但无法再得知每秒创建的事件数这一更细粒度的信息。

另外，由于没有分别保存各用户创建的事件数，也无法用这张汇总表对每个用户单独进行分析。

## 不使用 HLL 时，汇总表存在一些限制 {#without-hll-rollup-tables-have-a-few-limitations}

对于去重计数查询，普通汇总表的用处就有限了。例如，按分钟预聚合之后，无法回答按小时去重计数的问题。不能简单地累加每分钟的结果来得到一小时内创建事件的去重用户数，因为不同分钟之间很可能存在重复记录。

如果要按不同列组合的条件计算去重数量，就需要多张汇总表。

有时，你想按日期筛选，统计创建事件的去重用户数；有时想按事件类型筛选，进行去重计数；有时则同时使用这两种条件。借助 HLL，一张汇总表就能回答这些查询；不使用 HLL，则需要为每种不同类型的查询准备单独的汇总表。

## 使用 HLL {#hll-in-use}

如果汇总的是 HLL 数据类型，而不是最终的去重用户数量，就能轻松解决重复记录的问题。HLL 以特定方式编码数据，使各部分的去重计数能够合并，而不会重复计算重叠的记录。

如果要按不同列组合的条件进行去重计数，HLL 同样很有用。例如，按日期、按事件类型，或同时按两者统计创建事件的去重数量时，HLL 可以用一张汇总表处理所有组合。

而不使用 HLL 时，要按不同列组合的条件进行去重计数，就需要创建：

- 7 张不同的汇总表，覆盖 3 列的所有组合
- 15 张汇总表，覆盖 4 列的所有组合
- \(2^n - 1\) 张汇总表，覆盖 n 列的所有非空组合

## 结合 HLL 与汇总表 {#hll-and-rollup-tables-in-action-together}

HLL 可以回答 GitHub 事件数据中的一些典型去重计数查询。首先创建 `github_events` 表，并加载数据：

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

\COPY github_events FROM events.csv CSV
```

然后创建汇总表。这里希望同时按 `user` 和 `event_type` 维度进行去重计数，因此要使用一张稍有不同的汇总表：

```sql
DROP TABLE IF EXISTS github_events_rollup_minute;

CREATE TABLE github_events_rollup_minute(
    created_at timestamp,
    event_type text,
    distinct_user_id_count hll
);
```

最后，使用 INSERT/SELECT 填充汇总表，并用 `hll_hash_bigint` 函数对每个 `user_id` 计算哈希值。

```sql
INSERT INTO github_events_rollup_minute(
    created_at,
    event_type,
    distinct_user_id_count
)
SELECT
    date_trunc('minute', created_at) AS created_at,
    event_type,
    hll_add_agg(hll_hash_bigint(user_id))
FROM github_events
GROUP BY 1, 2;

INSERT 0 2484
```

## HLL 能回答哪些查询？ {#what-kinds-of-queries-can-hll-answer}

要将 HLL 值转为具体的去重计数，可以考虑这个问题：

**在 2016-12-01 05:35:00 这一分钟，各种事件类型分别有多少不同用户创建了事件？**

需要使用 `hll_cardinality` 函数，将 HLL 数据结构转为具体的去重计数。

```sql
SELECT
    created_at,
    event_type,
    hll_cardinality(distinct_user_id_count) AS distinct_count
FROM
    github_events_rollup_minute
WHERE
    created_at = '2016-12-01 05:35:00'::timestamp
ORDER BY 2;

     created_at      |          event_type           |  distinct_count
---------------------+-------------------------------+------------------
 2016-12-01 05:35:00 | CommitCommentEvent            |                1
 2016-12-01 05:35:00 | CreateEvent                   |               59
 2016-12-01 05:35:00 | DeleteEvent                   |                6
 2016-12-01 05:35:00 | ForkEvent                     |               20
 2016-12-01 05:35:00 | GollumEvent                   |                2
 2016-12-01 05:35:00 | IssueCommentEvent             |               42
 2016-12-01 05:35:00 | IssuesEvent                   |               13
 2016-12-01 05:35:00 | MemberEvent                   |                4
 2016-12-01 05:35:00 | PullRequestEvent              |               24
 2016-12-01 05:35:00 | PullRequestReviewCommentEvent |                4
 2016-12-01 05:35:00 | PushEvent                     | 254.135297564883
 2016-12-01 05:35:00 | ReleaseEvent                  |                4
 2016-12-01 05:35:00 | WatchEvent                    |               57
(13 rows)
```

HLL 还能帮助回答以下查询：

**在这一个小时内，有多少不同用户创建了事件？**

使用 HLL 即可得到答案。

```sql
SELECT
    hll_cardinality(SUM(distinct_user_id_count)) AS distinct_count
FROM
    github_events_rollup_minute
WHERE
    created_at BETWEEN '2016-12-01 05:00:00'::timestamp AND '2016-12-01 06:00:00'::timestamp;

 distinct_count
------------------
 10978.2523520687
(1 row)
```

另一个可以利用 HLL 可加性的问题是：

**在 2016-12-01 的每个小时内，分别有多少不同用户创建了事件？**

```sql
SELECT
    EXTRACT(HOUR FROM created_at) AS hour,
    hll_cardinality(SUM(distinct_user_id_count)) AS distinct_count
FROM
    github_events_rollup_minute
WHERE
    created_at BETWEEN '2016-12-01 00:00:00'::timestamp AND '2016-12-01 23:59:59'::timestamp
GROUP BY 1
ORDER BY 1;

  hour |  distinct_count
-------+------------------
     5 |  10598.637184899
     6 | 17343.2846931687
     7 | 18182.5699816622
     8 | 12663.9497604266
(4 rows)
```

由于数据有限，查询只返回了四行。最后再看一个问题：

**每个小时内有多少不同用户创建了 PushEvent？**

```sql
SELECT
    EXTRACT(HOUR FROM created_at) AS hour,
    hll_cardinality(SUM(distinct_user_id_count)) AS distinct_push_count
FROM
    github_events_rollup_minute
WHERE
    created_at BETWEEN '2016-12-01 00:00:00'::timestamp AND '2016-12-01 23:59:59'::timestamp
    AND event_type = 'PushEvent'::text
GROUP BY 1
ORDER BY 1;

 hour | distinct_push_count
------+---------------------
    5 |    6206.61586498546
    6 |    9517.80542100396
    7 |    10370.4087640166
    8 |    7067.26073810357
(4 rows)
```

## 一张 HLL 汇总表，胜过千张普通汇总表 {#a-rollup-table-with-hll-is-worth-a-thousand-rollup-tables-without-hll}

如果不使用 HLL，可能需要为每条查询准备不同的汇总表；而一张 HLL 汇总表就能回答这些查询。上面的四个示例查询都只用到一张 HLL 汇总表。不使用 HLL，则需要三张独立的汇总表才能回答全部查询。

为了支持分析查询，不使用 HLL 时往往还需要更多汇总表。对于 n 个约束条件的所有非空组合，需要 \(2^n - 1\) 张汇总表。使用 HLL，一张汇总表即可完成这项工作。

一张 HLL 汇总表比多张普通汇总表更容易维护，占用的内存也更少。有些情况下，不使用 HLL 的汇总表开销过高，甚至超过收益，人们便会决定完全不用汇总表。

## 想进一步了解 PostgreSQL 中的 HLL？ {#want-to-learn-more-about-hll-in-postgresql}

HLL 在分布式系统中同样有用。与汇总表类似，在 Citus 这样的分布式系统中，不同部分的数据通常放在不同节点上，因此不同节点上很可能存在重复记录。HLL 通过编码数据来合并各部分的去重计数、解决记录重叠问题，这套技术同样能用于分布式系统。

更多信息请参阅[在 PostgreSQL 上使用 HyperLogLog 进行分布式去重计数](/citus/articles/hyperloglog-count-distinct/)。该文介绍了 HLL 的内部原理，以及它如何合并各部分的去重计数而不重复计算重叠记录。

## 相关内容 {#related-content}

- [专题概览](/citus/articles/)
- [教程：时序数据](/citus/tutorials/tutorial-time-series/)
