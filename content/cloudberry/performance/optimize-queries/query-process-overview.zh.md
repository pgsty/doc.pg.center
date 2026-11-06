---
title: "查询处理概述"
description: "本节概述 Apache Cloudberry 处理查询的过程。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/optimize-queries/query-process-overview.md"
---

了解这一过程有助于编写和调优查询。

用户向 Apache Cloudberry 提交查询的方式与其他数据库管理系统相同：通过 `psql` 等客户端应用程序连接 Apache Cloudberry Coordinator 主机上的数据库实例，然后提交 SQL 语句。

## 查询规划与分发 {#query-planning-and-dispatch}

Coordinator 接收、解析并优化查询。生成的查询计划分为并行计划和定向计划。Coordinator 将并行查询计划分发给所有 Segment。

Coordinator 将定向查询计划分发给单个 Segment。每个 Segment 负责在自己持有的数据上执行本地数据库操作。大多数数据库操作，例如表扫描、连接、聚合和排序，都会在所有 Segment 上并行执行。各个 Segment 数据库独立执行这些操作，不依赖其他 Segment 数据库中存储的数据。

某些查询可能只访问单个 Segment 上的数据，例如单行 `INSERT`、`UPDATE`、`DELETE` 或 `SELECT` 操作，或者按表的分布键列过滤的查询。对于这些查询，查询计划不会分发给所有 Segment，而是定向发给包含受影响行或相关行的 Segment。

## Apache Cloudberry 查询计划 {#apache-cloudberry-query-plans}

查询计划是 Apache Cloudberry 为生成查询结果而执行的一组操作。计划中的每个*节点*或步骤代表一项数据库操作，例如表扫描、连接、聚合或排序。计划按从下到上的顺序解读和执行。

除了表扫描、连接等常见数据库操作，Apache Cloudberry 还有一种称为 *Motion* 的操作。Motion 操作在查询处理期间于 Segment 之间移动元组。并非所有查询都需要 Motion。例如，定向查询计划无需通过 Interconnect 移动数据。

为了在查询运行时尽可能提高并行度，Apache Cloudberry 将查询计划的工作划分为*切片（slice）*。切片是 Segment 可以独立处理的一部分计划。查询计划在每个 *Motion* 操作处切分，Motion 两侧各有一个切片。

例如，考虑以下涉及两张表连接的简单查询：

```sql
SELECT customer, amount
FROM sales JOIN customer USING (cust_id)
WHERE dateCol = '04-30-2016';
```

下图展示了查询计划。每个 Segment 都接收一份查询计划副本，并行执行。

本例的查询计划包含一个*重分布 Motion*，它在 Segment 之间移动元组以完成连接。之所以需要重分布 Motion，是因为 customer 表按 `cust_id` 分布到各 Segment，而 sales 表按 `sale_id` 分布。要执行连接，必须按 `cust_id` 对 `sales` 元组重分布。计划在重分布 Motion 两侧切分，形成*切片 1* 和*切片 2*。

该查询计划还包含另一种 Motion 操作，称为*汇集 Motion*。在汇集 Motion 中，各 Segment 将结果发回 Coordinator，由它呈现给客户端。由于查询计划始终在 Motion 处切分，此计划最顶端还存在一个隐含的切片（*切片 3*）。并非所有查询计划都涉及汇集 Motion。例如，`CREATE TABLE x AS SELECT...` 语句不包含汇集 Motion，因为元组会发送到新建的表，而不是 Coordinator。

## 并行查询执行 {#parallel-query-execution}

Apache Cloudberry 创建多个数据库进程来处理查询。在 Coordinator 上，查询工作进程称为*查询分发器*（QD）。QD 负责创建并分发查询计划，以及汇总和呈现最终结果。在 Segment 上，查询工作进程称为*查询执行器*（QE）。QE 负责完成分配给自己的工作，并将中间结果传递给其他工作进程。

查询计划的每个*切片*至少分配一个工作进程。工作进程独立执行分配给它的查询计划部分。查询运行期间，每个 Segment 都会有多个进程并行处理该查询。

位于不同 Segment、执行同一查询计划切片的相关进程称为*进程组（gang）*。一部分工作完成后，元组沿查询计划向上流动，从一个进程组传给下一个进程组。这种 Segment 之间的进程间通信由 Apache Cloudberry 的 *Interconnect* 组件承担。
