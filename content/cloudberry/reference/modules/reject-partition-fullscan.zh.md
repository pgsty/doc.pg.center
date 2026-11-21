---
title: reject_partition_fullscan
description: reject_partition_fullscan 拒绝未有效进行分区剪枝而扫描分区表所有分区的查询。
weight: 230
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/reject-partition-fullscan.md
---

`reject_partition_fullscan` 模块拒绝未有效进行分区剪枝而扫描分区表所有分区的查询。它安装一个规划器钩子，检查生成的计划，不论计划来自基于 Postgres 的规划器还是 GPORCA；如果将扫描分区表的全部分区，则报错。

此模块用于防止遗漏分区键过滤条件的高开销查询。

## 构建与安装 {#build-and-install}

`reject_partition_fullscan` 是 `gpcontrib` 下的调试扩展之一。默认启用的 `--enable-debug-extensions` 生效时，会构建这些扩展。如果配置 Apache Cloudberry 时使用 `--disable-debug-extensions`，则不会构建此模块。

## 启用模块 {#enable-the-module}

此模块通过加载共享库工作，不包含 SQL 对象。

- 要为整个集群启用，将库加入 `shared_preload_libraries`，然后重启集群：

    ```shell
    gpconfig -c shared_preload_libraries -v 'reject_partition_fullscan'
    gpstop -ra
    ```

    如果 `shared_preload_libraries` 已列出其他库，请在其值中保留它们。

- 要只为当前会话启用，使用 `LOAD` 加载库。这需要超级用户权限：

    ```sql
    LOAD 'reject_partition_fullscan';
    ```

可以执行 `CREATE EXTENSION reject_partition_fullscan`，但它不会创建对象。规划器钩子和配置参数在库加载时注册。

> [!NOTE]
> 库加载后默认开启检查，因为 `reject_partition_fullscan` 的默认值为 `on`。

## 配置参数 {#configuration-parameters}

任何角色都可以在自己的会话中更改这两个参数。

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `reject_partition_fullscan` | 布尔值 | `on` | 拒绝未进行分区剪枝而扫描所有分区的分区表查询。 |
| `partition_fullscan_threshold` | 整数 | `0` | 查询在分区剪枝后允许扫描的最大分区数。为 `0` 时，如果剩余分区超过一个，就拒绝基于 Postgres 的规划器生成的计划。参见[行为](#behavior)。范围：`0` 到 `2147483647`。 |

## 行为 {#behavior}

语句规划完成后，模块遍历计划树，检查每个分区表扫描：

- 当 `partition_fullscan_threshold = 0` 时，如果计划时剪枝后剩余分区超过一个，就拒绝基于 Postgres 的规划器生成的计划。因此，即使包含分区键过滤条件，只要保留了两个或更多分区，也会被拒绝。要允许这类查询，请设置正的阈值。
- 当 `partition_fullscan_threshold` 大于 `0` 时，如果剪枝后剩余分区数大于阈值，就拒绝该语句。

> [!CAUTION]
> 此模块对基于 Postgres 的规划器生成的计划能可靠工作。默认优化器 GPORCA 会将运行时剪枝信息附加到动态扫描，模块因而将这类扫描视为可在运行时剪枝。因此，GPORCA 规划的 `SELECT` 语句即使扫描所有分区，也不会被拒绝。分区表上的 `UPDATE` 和 `DELETE` 语句由基于 Postgres 的规划器规划，会接受检查。要对 `SELECT` 语句执行此检查，请在会话中通过 `SET optimizer = off` 关闭 GPORCA。

被拒绝的语句会报错，形式如下：

```text
ERROR:  partitioned table "<schema>.<table>" full partition scan is not allowed, <n> partitions would be scanned
HINT:  Add a WHERE clause on the partition key to enable partition pruning.
```

检查适用于每条经过规划的语句，包括 `SELECT`、`UPDATE` 和 `DELETE` 语句、子查询引用的分区表，以及 `EXPLAIN`、`INSERT ... SELECT` 和 `CREATE TABLE AS` 等读取分区表的语句。

以下情况不会被拒绝：

- `reject_partition_fullscan` 为 `off`。
- `enable_partition_pruning` 为 `off`。
- 扫描最多覆盖一个分区，例如只有单个分区的分区表。
- 可在运行时剪枝：计划中的剪枝步骤在执行器启动或执行过程中求值（例如在分区键上使用参数的预备语句），或 GPORCA 动态扫描使用基于连接的分区剪枝。

## 示例 {#example}

```sql
LOAD 'reject_partition_fullscan';
SET optimizer = off;

CREATE TABLE pfr_test (id int, dt date, val text)
    PARTITION BY RANGE (dt);
CREATE TABLE pfr_test_p1 PARTITION OF pfr_test
    FOR VALUES FROM ('2025-01-01') TO ('2025-04-01');
CREATE TABLE pfr_test_p2 PARTITION OF pfr_test
    FOR VALUES FROM ('2025-04-01') TO ('2025-07-01');
CREATE TABLE pfr_test_p3 PARTITION OF pfr_test
    FOR VALUES FROM ('2025-07-01') TO ('2025-10-01');

SET reject_partition_fullscan = on;
SET partition_fullscan_threshold = 0;

-- Rejected: no filter on the partition key
SELECT * FROM pfr_test;
SELECT * FROM pfr_test WHERE val = 'x';
UPDATE pfr_test SET val = 'y';

-- Allowed: the filter prunes the scan to one partition
SELECT * FROM pfr_test WHERE dt = '2025-02-01';
DELETE FROM pfr_test WHERE dt = '2025-02-01';

-- Rejected: two partitions remain after pruning
SELECT * FROM pfr_test
    WHERE dt >= '2025-01-01' AND dt < '2025-07-01';

-- Threshold mode: allow up to 2 partitions
SET partition_fullscan_threshold = 2;

-- Allowed: pruned to 2 partitions
SELECT * FROM pfr_test
    WHERE dt >= '2025-01-01' AND dt < '2025-07-01';

-- Rejected: 3 partitions exceed the threshold
SELECT * FROM pfr_test;
```

要允许某个会话执行全分区扫描，关闭检查：

```sql
SET reject_partition_fullscan = off;
```

## 使用说明 {#usage-notes}

- 任何角色都可以更改这两个参数，因此此模块用于防止意外的全分区扫描，不是强制约束机制。
- 检查在规划时针对优化器产生的计划执行，不考虑分区中包含多少数据。
- 通过 `LOAD` 加载库时，检查只作用于当前会话。
