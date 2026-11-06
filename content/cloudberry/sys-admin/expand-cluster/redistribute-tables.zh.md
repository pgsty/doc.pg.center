---
title: "重分布表"
description: "重新分布表，使现有数据在扩容后的集群中保持平衡。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/expand-cluster/redistribute-tables.md"
---

创建扩容模式后，可以使用 [`gpexpand`](/cloudberry/reference/sys-utilities/gpexpand/) 在整个系统中重新分布表。计划在低使用时段执行此操作，此时工具的 CPU 使用和表锁对运行的影响最小。对要重新分布的表进行排序，优先处理最大或最关键的表。

> [!NOTE]
> 重新分布数据时，Apache Cloudberry 必须以生产模式运行。Apache Cloudberry 不能处于受限模式或 Coordinator 模式。启动 Apache Cloudberry 时不能指定 [`gpstart`](/cloudberry/reference/sys-utilities/gpstart/) 的 `-R` 或 `-m` 选项。

表重分布进行期间，新建的表或分区会按照正常运行时的方式在所有 Segment 上分布。即使相关数据尚未重新分布到新 Segment，查询也可以访问所有 Segment。正在重新分布的表或分区会被锁定，无法进行读写操作。重分布完成后，正常操作恢复。

- [为重分布排序表](#rank-tables-for-redistribution)
- [使用 gpexpand 重新分布表](#redistribute-tables-using-gpexpand)
- [监控表重分布](#monitor-table-redistribution)

## 为重分布排序表 {#rank-tables-for-redistribution}

对于大型系统，可以控制表的重分布顺序。调整扩容模式中的表 `rank` 值，为高频使用的表设置优先级并尽量减少性能影响。可用的空闲磁盘空间可能影响表排序；请参见[管理大规模 Cloudberry 系统中的重分布](/cloudberry/sys-admin/expand-cluster/plan-system-expansion/)。

要通过更新 [gpexpand.status_detail](/cloudberry/reference/sys-utilities/gpexpand/) 中的 `rank` 值为表的重分布排序，请使用 `psql` 或其他受支持的客户端连接 Apache Cloudberry。使用如下命令更新 *gpexpand.status_detail*：

```sql
=> UPDATE gpexpand.status_detail SET rank=10;

=> UPDATE gpexpand.status_detail SET rank=1 WHERE fq_name = 'public.lineitem';
=> UPDATE gpexpand.status_detail SET rank=2 WHERE fq_name = 'public.orders';
```

这些命令将所有表的优先级降低为 `10`，然后为 `lineitem` 设置 `1`，为 `orders` 设置 `2`。表重分布开始时，先重新分布 `lineitem`，然后是 `orders` 和 *gpexpand.status_detail* 中的所有其他表。要排除某个表的重分布，请将其从 *gpexpand.status_detail* 表中删除。

## 使用 gpexpand 重新分布表 {#redistribute-tables-using-gpexpand}

### 使用 gpexpand 重新分布表 {#to-redistribute-tables-with-gpexpand}

1. 以将运行 Apache Cloudberry 系统的用户（例如 `gpadmin`）登录 Coordinator 主机。
2. 运行 `gpexpand` 工具。可以使用 `-d` 或 `-e` 选项定义扩容会话的时间段。例如，要让工具连续运行最多 60 小时：

    ```shell
    $ gpexpand -d 60:00:00
    ```

    工具会持续重新分布表，直到模式中的最后一张表完成，或达到指定的持续时间或结束时间。会话开始和结束时，`gpexpand` 会更新 `gpexpand.status` 中的状态和时间。

> [!NOTE]
> 表重分布完成后，在目录表上运行 `VACUUM ANALYZE` 和 `REINDEX` 命令，以更新表统计信息并重建索引。请参见[常规 Vacuum 和 Analyze](/cloudberry/sys-admin/routine-maintain-tasks/)和 [`VACUUM`](/cloudberry/reference/sql-stmts/vacuum/)。

## 监控表重分布 {#monitor-table-redistribution}

表重分布过程中，可以查询扩容模式来查看：

- 当前进度摘要、表重分布的估计速率以及估计完成时间。使用 `gpexpand.expansion_progress`，如[查看扩容状态](#view-expansion-status)所述。
- 每张表的状态信息，使用 `gpexpand.status_detail`。请参见[查看表状态](#view-table-status)。

另请参见[监控集群扩容状态](/cloudberry/sys-admin/expand-cluster/plan-system-expansion/)，了解如何使用 `gpstate` 工具监控整体扩容进度。

### 查看扩容状态 {#view-expansion-status}

第一张表完成重分布后，*gpexpand.expansion_progress* 会计算估算值，并根据所有表的重分布速率刷新这些估算值。每次使用 `gpexpand` 启动表重分布会话时，计算都会重新开始。要监控进度，请使用 `psql` 或其他受支持的客户端连接 Apache Cloudberry，并使用如下命令查询 *gpexpand.expansion_progress*：

```sql
=# SELECT * FROM gpexpand.expansion_progress;
             name             |         value
------------------------------+-----------------------
 Bytes Left                   | 5534842880
 Bytes Done                   | 142475264
 Estimated Expansion Rate     | 680.75667095996092 MB/s
 Estimated Time to Completion | 00:01:01.008047
 Tables Expanded              | 4
 Tables Left                  | 4
(6 rows)
```

### 查看表状态 {#view-table-status}

*gpexpand.status_detail* 表存储模式中每张表的状态、上次更新时间以及更多信息。要查看某张表的状态，请使用 `psql` 或其他受支持的客户端连接 Apache Cloudberry，并查询 *gpexpand.status_detail*：

```sql
=> SELECT status, expansion_started, source_bytes FROM
gpexpand.status_detail WHERE fq_name = 'public.sales';
  status   |     expansion_started      | source_bytes
-----------+----------------------------+--------------
 COMPLETED | 2017-02-20 10:54:10.043869 |   4929748992
(1 row)
```
