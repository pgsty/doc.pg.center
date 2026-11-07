---
title: Citus 中的 PostgreSQL 并行索引
description: 了解如何将 Citus 中的并行索引与 PostgreSQL 配合使用，以便更快地在大型数据集上创建索引。
weight: 110
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/parallel-indexing?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
linkTitle: 并行索引
---

**原始文章：** [Marco Slot · 2017 年 1 月 17 日](https://www.citusdata.com/blog/2017/01/17/parallel-indexing-with-citus/)。中文整理：[PGSTY](https://pgsty.com/)。

索引是优化数据库性能的重要工具，在大数据场景下也越来越重要。然而，随着数据量增长，索引维护往往成为写入瓶颈，尤其是[高级索引类型](https://www.postgresql.org/docs/current/static/textsearch-indexes.html)：每写入一行数据，都需要消耗 CPU 时间。创建索引的代价也可能高得难以承受，在 PostgreSQL 中为数 TB 数据建立新索引，可能需要数小时甚至数天。Citus 通过并行化加速索引的创建与维护。

Citus 可以将 PostgreSQL 表分布到多台机器上。它的一个优势是，你可以不断增加配有更多 CPU 的机器，持续提升写入能力；即便索引已经成为瓶颈，也能如此。Citus 允许以大规模并行方式执行 `CREATE INDEX`，从而快速为大表创建索引。此外，在分布式表上执行 [COPY 命令](https://www.postgresql.org/docs/current/static/sql-copy.html)时，可以并行写入多行数据，提升适合批量摄取的场景（如传感器数据、某些数据流）的性能。

下面通过为约 20 万行数据创建索引，展示并行索引的好处。这些数据来自 [GitHub Archive](https://www.githubarchive.org/)，包含较大的 JSON 对象。要运行示例，先建立一个 [Citus Cloud](https://www.citusdata.com/product/cloud/) 集群，包含 4 个工作节点，每个节点 4 个核心，运行 PostgreSQL 9.6。

运行以下命令下载示例数据：

```bash
wget http://examples.citusdata.com/github_archive/github_events-2015-01-01-{0..24}.csv.gz
gzip -d github_events-*.gz
```

接下来，先将 GitHub 事件表创建为普通 PostgreSQL 表，再将其分布到 4 个节点上：

```sql
CREATE TABLE github_events (
    event_id bigint,
    event_type text,
    event_public boolean,
    repo_id bigint,
    payload jsonb,
    repo jsonb,
    actor jsonb,
    org jsonb,
    created_at timestamp
);

-- (distributed table only) Shard the table by repo_id
SELECT create_distributed_table('github_events', 'repo_id');

-- Initial data load: 218934 events from 2015-01-01
\COPY github_events FROM PROGRAM 'cat github_events-*.csv' WITH (FORMAT CSV)
```

GitHub 数据集中的每个事件都包含一个内容详尽的 JSON 格式 payload 对象。为 payload 建立 GIN 索引后，就能快速对事件进行细粒度搜索，例如查找某位作者的提交。但创建这种索引的代价可能很高。好在并行索引可以同时利用所有核心，创建许多较小的索引，大幅加快这一过程：

```sql
CREATE INDEX github_events_payload_idx ON github_events USING GIN (payload);
```

| 操作 | 普通表 | 分布式表 | 加速比 |
| --- | --- | --- | --- |
| 对 219k 行执行 CREATE INDEX | 33.2s | 2.6s | 13x |

并行 `CREATE INDEX` 呈现出超线性加速：虽然只有 16 个核心，加速比却能超过 16 倍。向一个大索引插入数据，不如向每个分片各自的小索引插入数据高效（对于 N 行数据，复杂度为 O(log N)）。这为分片带来了另一项性能收益。

| 操作 | 普通表 | 分布式表 | 加速比 |
| --- | --- | --- | --- |
| 对 438k 行执行 CREATE INDEX | 55.9s | 3.2s | 17x |
| 对 876k 行执行 CREATE INDEX | 110.9s | 5.0s | 22x |
| 对 1.8M 行执行 CREATE INDEX | 218.2s | 8.9s | 25x |

索引创建后，`COPY` 命令也能利用并行索引维护。在内部，COPY 通过多个连接，异步向不同工作节点发送大量行，各工作节点再并行存储这些行并维护索引。这比单个 PostgreSQL 进程能达到的加载速度更快。具体加速多少取决于数据分布。如果所有数据都进入同一个分片，性能就与普通 PostgreSQL 相近。

```text
\COPY github_events FROM PROGRAM 'cat github_events-*.csv' WITH (FORMAT CSV)
```

| 操作 | 普通表 | 分布式表 | 加速比 |
| --- | --- | --- | --- |
| COPY 219k 行，无索引 | 18.9s | 12.4s | 1.5x |
| COPY 219k 行，有 GIN 索引 | 49.3s | 12.9s | 3.8x |

最后，测量索引对查询耗时的影响。尝试两种查询：一种覆盖所有仓库，另一种带有特定 `repo_id` 的筛选条件。这一区别对 Citus 很重要，因为 `github_events` 表按 `repo_id` 分片。带有特定 `repo_id` 条件的查询只访问单个分片，另一种查询则在所有分片上并行执行。

```sql
-- Get all commits by test@gmail.com from all repos
SELECT repo_id, jsonb_array_elements(payload->'commits')
  FROM github_events
 WHERE event_type = 'PushEvent' AND
       payload @> '{"commits":[{"author":{"email":"test@gmail.com"}}]}';

-- Get all commits by test@gmail.com from a single repo
SELECT repo_id, jsonb_array_elements(payload->'commits')
  FROM github_events
 WHERE event_type = 'PushEvent' AND
       payload @> '{"commits":[{"author":{"email":"test@gmail.com"}}]}' AND
       repo_id = 17330407;
```

对 219k 行数据执行查询，耗时如下。带 * 的耗时表示该查询由 Citus 并行执行。并行化会带来一定的固定开销，但也能承担更多计算工作，因此相比普通表上的查询，它可能更快，也可能略慢。

| 操作 | 普通表 | 分布式表 |
| --- | --- | --- |
| SELECT，无索引，所有仓库 | 900ms | 68ms* |
| SELECT，payload 上有 GIN 索引，所有仓库 | 2ms | 11ms* |
| SELECT，无索引，单个仓库 | 900ms | 28ms |
| SELECT，有索引，单个仓库 | 2ms | 2ms |

PostgreSQL 中的索引能显著缩短查询时间，但也会显著降低写入速度。Citus 让你可以横向扩展集群，在数据管道的读写两端都获得良好的性能。并行摄取配合单分片查询，是 Citus 特别擅长的组合：既能提供优于普通 PostgreSQL 的查询性能，又能获得更高、扩展性更好的写入吞吐量。

## 相关内容 {#related-content}

- [专题概览](/citus/articles/)
- [性能调优](/citus/operations/performance-tuning/)
