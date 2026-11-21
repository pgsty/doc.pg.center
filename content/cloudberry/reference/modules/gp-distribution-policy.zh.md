---
title: gp_distribution_policy
description: gp_distribution_policy 检查表中的行是否存储在分布策略指定的 Segment 上。
weight: 70
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/gp-distribution-policy.md
---

`gp_distribution_policy` 模块检查表中的行是否存储在该表分布策略指定的 Segment 上。它在每个 Segment 上扫描表，计算每行分布键列的哈希值，并验证该行是否属于此 Segment。

此模块用于检测落在错误 Segment 上的行。

## 构建与安装 {#build-and-install}

`gp_distribution_policy` 默认随 Apache Cloudberry 构建和安装，不需要任何 `configure` 选项。

## 启用模块 {#enable-the-module}

在每个需要使用它的数据库中创建扩展。创建扩展需要超级用户权限，不需要 `shared_preload_libraries`。

```sql
CREATE EXTENSION gp_distribution_policy;
```

扩展将其函数安装到 `public` 模式中。

## 函数 {#functions}

| 函数 | 返回值 | 说明 |
|---|---|---|
| `gp_table_distribution_check(regclass)` | `TABLE (gp_segment_id int, is_distribution_correct boolean)` | 在所有 Segment 上运行检查，每个 Segment 返回一行。如果该 Segment 上存储的所有行都属于它，`is_distribution_correct` 为 `true`；如果至少有一行位于错误的 Segment，则为 `false`。 |
| `gp_distribution_policy_table_check(relid regclass)` | `boolean` | 检查函数执行所在实例上的表行。它是 `gp_table_distribution_check()` 内部使用的逐 Segment 检查函数。应调用 `gp_table_distribution_check()`，不要直接调用此函数。 |

## 示例 {#example}

```sql
CREATE EXTENSION gp_distribution_policy;

CREATE TABLE some_other_table(id int, some_other_data int) DISTRIBUTED BY (id);
INSERT INTO some_other_table SELECT i, i FROM generate_series(1,12) i;

SELECT gp_table_distribution_check('some_other_table');
```

在包含三个 Segment 且所有行都放置正确的集群上，输出为：

```text
 gp_table_distribution_check
-----------------------------
 (0,t)
 (1,t)
 (2,t)
(3 rows)
```

如果某个 Segment 存储的行按哈希应属于另一个 Segment，则报告为 `f`。例如，将同一行直接插入每个 Segment 后，只有一个 Segment 的分布正确：

```text
 gp_table_distribution_check
-----------------------------
 (0,t)
 (1,f)
 (2,f)
(3 rows)
```

要将结果按独立列返回：

```sql
SELECT * FROM gp_table_distribution_check('some_other_table');
```

## 使用说明 {#usage-notes}

- 输入关系必须是表、物化视图或目录表。对于视图、外表和分区表，函数会报错 `input relation is not a table`。要检查分区表，请对每个叶子分区运行检查。
- 支持堆表和 AO 表。
- 此检查只对哈希分布表有意义。对于随机分布表和复制表，即使数据放置正确，函数也会对某些 Segment 报告 `false`，因此不要对这类表使用此函数。
- 检查在每个 Segment 上扫描表；在某个 Segment 上遇到第一行放置错误的数据后，该 Segment 的检查就停止。如果大表的分布正确，检查会读取整张表。
- 结果指出哪些 Segment 包含放置错误的行，但不会标识具体的行。
