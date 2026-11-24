---
title: 在 Spock 中使用 Snowflake 序列
description: 说明 Snowflake 序列如何降低分布式复制集群中的主键冲突风险。
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/managing/snowflake.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
translation_status: translated
translation_notice: en
translator: PGSTY 社区
type: docs
---



[Snowflake 扩展](https://github.com/pgEdge/snowflake-sequences)提供基于序列的唯一 ID 方案，用于在分布式复制集群中替代 PostgreSQL 内建的 `bigserial` 数据类型。Snowflake 序列将不同节点同一时间分配相同键值的风险降到最低，从而避免潜在的数据冲突。


> [!NOTE]
>
> Spock 强烈建议使用 Snowflake 序列，而不是传统 PostgreSQL 序列。Snowflake 序列可以减轻网络延迟扰乱分布式事务序列的担忧。
>

使用 [`Snowflake` 序列](https://docs.pgedge.com/snowflake/v2-4/creating/)可以充分利用分布式多主复制解决方案提供的优势。Snowflake 提供基于 `int8` 和序列的唯一 ID 方案，可选择替代 PostgreSQL 内建的 `bigserial` 数据类型。

## 比较序列类型 {#comparing-sequence-types}

以下示例比较传统 PostgreSQL 序列（`id` 值 `1` 和 `2`）存储的详细程度，与 Snowflake 序列（`id` 值 `135824181823537153` 和 `135824609030176769`）可提供的详细程度：

```sql
acctg=# SELECT id, snowflake.format(id), customer, invoice FROM orders;
         id         |                          format                           |        customer        |  invoice
--------------------+-----------------------------------------------------------+------------------------+------------
                  1 | {"id": 1, "ts": "2022-12-31 19:00:00-05", "count": 0}     | Chesterfield Schools   | art_9338
                  2 | {"id": 2, "ts": "2022-12-31 19:00:00-05", "count": 0}     | Chesterfield Schools   | math_9663
 135824181823537153 | {"id": 1, "ts": "2024-01-10 14:16:48.438-05", "count": 0} | Prince William Schools | math_8330
 135824609030176769 | {"id": 1, "ts": "2024-01-10 14:18:30.292-05", "count": 0} | Fluvanna Schools       | art_9447
(4 rows)
```

> [!NOTE] 示例的版本差异
> 表格保留了上游的输出。按 v2.6.1 的位布局，表中两个较大的 ID 均来自节点 `0`，计数器均为 `1`。[Snowflake 函数](/zh/pgedge/snowflake/snowflake-functions/)

## Snowflake 序列结构 {#snowflake-sequence-structure}

与传统 PostgreSQL 序列不同，Snowflake 序列由时间戳、计数器和唯一节点标识符组成；该结构确保可提供超过 18 万亿个唯一序列号。Snowflake 序列提供以下能力：

- 位于不同区域的节点可以独立分配 ID，用于新增或修改数据。
- 各节点使用唯一节点号即可保持 ID 唯一，无需手工分配编号区间。
- ID 内含生成时的时间戳，可用来比较生成时间。跨节点时钟偏差和事务提交时机都会影响顺序，不能从 ID 推断全局提交顺序。

在内部，Snowflake 序列是 64 位整数，对外表示为 `bigint` 值。这 64 位划分为以下位段：

- Bit 63 未使用，表示 `int8` 的符号。
- Bits 22–62 以毫秒精度存储时间戳。
- Bits 12–21 存储唯一的 pgEdge Distributed Postgres 节点号。
- Bits 0–11 存储一毫秒内的计数器。

时间戳是 41 位无符号值，表示自 2023-01-01 起经过的毫秒数。计数器是 12 位无符号值，每次分配 ID 时递增；每个节点每毫秒可分配 4096 个唯一 ID，约合每秒 400 万个。节点号是全局集群内 PostgreSQL 实例的 10 位唯一标识符；该值通过 `snowflake.node` GUC 在 `postgresql.conf` 文件中设置。

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/managing/snowflake.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文译校：PGSTY 社区。
