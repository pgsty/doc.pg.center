---
title: "CREATE RESOURCE QUEUE"
description: "定义新的资源队列。"
weight: 750
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-resource-queue.md"
---

## 语法概要 {#synopsis}

```sql
CREATE RESOURCE QUEUE <name> WITH (<queue_attribute>=<value> [, ... ])
```

其中 queue_attribute 为：

```sql
    ACTIVE_STATEMENTS=<integer>
        [ MAX_COST=<float >[COST_OVERCOMMIT={TRUE|FALSE}] ]
        [ MIN_COST=<float >]
        [ PRIORITY={MIN|LOW|MEDIUM|HIGH|MAX} ]
        [ MEMORY_LIMIT='<memory_units>' ]

 | MAX_COST=float [ COST_OVERCOMMIT={TRUE|FALSE} ]
        [ ACTIVE_STATEMENTS=<integer >]
        [ MIN_COST=<float >]
        [ PRIORITY={MIN|LOW|MEDIUM|HIGH|MAX} ]
        [ MEMORY_LIMIT='<memory_units>' ]
```

## 说明 {#description}

为 Apache Cloudberry 资源管理创建新的资源队列。资源队列必须具有 `ACTIVE_STATEMENTS` 或 `MAX_COST` 值（也可以同时具有两者）。只有超级用户才能创建资源队列。

设置 `ACTIVE_STATEMENTS` 阈值的资源队列会限制分配到该队列的角色可以运行的查询数量上限，即同时允许运行的活动查询数。`ACTIVE_STATEMENTS` 的值应为大于 0 的整数。

设置 `MAX_COST` 阈值的资源队列会限制分配到该队列的角色可以运行的查询总成本上限。成本按查询计划器确定的查询*估算总成本*计量（查询的 `EXPLAIN` 输出会显示该值）。因此，管理员必须熟悉系统中通常运行的查询，才能为队列设置合适的成本阈值。成本以磁盘页读取次数为单位；1.0 等于顺序读取一个磁盘页。`MAX_COST` 的值指定为浮点数（例如 100.0），也可以指定为指数（例如 1e+2）。如果资源队列受成本阈值限制，管理员可以允许 `COST_OVERCOMMIT=TRUE`（默认值）。这意味着超过允许成本阈值的查询只有在系统空闲时才允许运行。如果指定 `COST_OVERCOMMIT=FALSE`，超过成本限制的查询将始终被拒绝，永远不会运行。指定 `MIN_COST` 值可以让管理员定义小查询的成本，使其免于进入资源队列。

> **注意** GPORCA 和 Postgres Planner 使用不同的查询成本模型，同一查询可能计算出不同成本。Apache Cloudberry 的资源队列资源管理方案既不区分也不对齐 GPORCA 与 Postgres Planner 的成本，而是使用优化器返回的实际成本值限制查询。

基于资源队列的资源管理处于活动状态时，应使用资源队列的 `MEMORY_LIMIT` 和 `ACTIVE_STATEMENTS` 限制，而不是配置基于成本的限制。即使使用 GPORCA，Apache Cloudberry 也可能对某些查询回退到 Postgres Planner，因此使用基于成本的限制可能产生意外结果。

如果未定义 `ACTIVE_STATEMENTS` 或 `MAX_COST` 的值，默认设为 `-1`（表示不限制）。定义资源队列后，必须使用 [ALTER ROLE](/cloudberry/reference/sql-stmts/alter-role/) 或 [CREATE ROLE](/cloudberry/reference/sql-stmts/create-role/) 命令将角色分配到该队列。

可以选择为资源队列分配 `PRIORITY`，控制与其他资源队列相比，该队列关联查询所使用的可用 CPU 资源相对份额。如果未定义 `PRIORITY` 的值，队列关联查询的默认优先级为 `MEDIUM`。

设置可选 `MEMORY_LIMIT` 阈值的资源队列会限制通过该队列提交的所有查询在 Segment 主机上可消耗的内存总量。它决定查询执行期间该查询所有工作进程在 Segment 主机上可消耗的内存总量。Apache Cloudberry 建议将 `MEMORY_LIMIT` 与 `ACTIVE_STATEMENTS` 配合使用，而不是与 `MAX_COST` 配合使用。基于语句的队列中，每个查询默认分配的内存为：`MEMORY_LIMIT / ACTIVE_STATEMENTS`。基于成本的队列中，每个查询默认分配的内存为：`MEMORY_LIMIT * (query_cost / MAX_COST)`。

只要不超过 `MEMORY_LIMIT` 或 `max_statement_mem`，就可以使用服务器配置参数 `statement_mem`，按查询覆盖默认内存分配。例如，为某个查询分配更多内存：

```sql
=> SET statement_mem='2GB';
=> SELECT * FROM my_big_table WHERE column='value' ORDER BY id;
=> RESET statement_mem;
```

所有资源队列的 `MEMORY_LIMIT` 值之和不应超过 Segment 主机的物理内存量。如果工作负载分布在多个队列上，内存分配可能超额订阅。不过，如果超过 `gp_vmem_protect_limit` 指定的 Segment 主机内存限制，查询可能会在执行期间被取消。

有关 `statement_mem`、`max_statement` 和 `gp_vmem_protect_limit` 的信息，请参见服务器配置参数。

## 参数 {#parameters}

**`name`**

资源队列名称。

**`ACTIVE_STATEMENTS integer`**

设置 `ACTIVE_STATEMENTS` 阈值的资源队列会限制分配到该队列的角色可以运行的查询数量。它控制同时允许运行的活动查询数。`ACTIVE_STATEMENTS` 的值应为大于 0 的整数。

**`MEMORY_LIMIT 'memory_units'`**

设置该资源队列中用户提交的所有语句的内存总配额。内存单位可以是 kB、MB 或 GB。资源队列的最小内存配额为 10MB，没有最大值，但查询执行时的上限受 Segment 主机物理内存限制。默认值为无限制（`-1`）。

**`MAX_COST float`**

设置 `MAX_COST` 阈值的资源队列会限制分配到该队列的角色可以运行的查询总成本上限。成本按 Apache Cloudberry 查询优化器确定的查询*估算总成本*计量（查询的 `EXPLAIN` 输出会显示该值）。因此，管理员必须熟悉系统中通常运行的查询，才能为队列设置合适的成本阈值。成本以磁盘页读取次数为单位；1.0 等于顺序读取一个磁盘页。`MAX_COST` 的值指定为浮点数（例如 100.0），也可以指定为指数（例如 1e+2）。

**`COST_OVERCOMMIT boolean`**

如果资源队列受 `MAX_COST` 限制，管理员可以允许 `COST_OVERCOMMIT`（默认值）。这意味着超过允许成本阈值的查询只有系统空闲时才允许运行。如果指定 `COST_OVERCOMMIT=FALSE`，超过成本限制的查询将始终被拒绝，永远不会运行。

**`MIN_COST float`**

被视为小查询的最低查询成本限制。成本低于此限制的查询不会排队，会立即运行。成本按查询计划器确定的查询*估算总成本*计量（查询的 `EXPLAIN` 输出会显示该值）。因此，管理员必须熟悉系统中通常运行的查询，才能为小查询设置合适成本。成本以磁盘页读取次数为单位；1.0 等于顺序读取一个磁盘页。`MIN_COST` 的值指定为浮点数（例如 100.0），也可以指定为指数（例如 1e+2）。

**`PRIORITY={MIN|LOW|MEDIUM|HIGH|MAX}`**

设置与资源队列关联查询的优先级。发生争用时，优先级较高队列中的查询或语句会获得更大份额的可用 CPU 资源。低优先级队列中的查询可能会在高优先级查询运行时延迟。如果未指定优先级，队列关联查询的优先级为 `MEDIUM`。

## 注意事项 {#notes}

使用 `gp_toolkit.gp_resqueue_status` 系统视图查看资源队列的限制设置和当前状态：

```sql
SELECT * from gp_toolkit.gp_resqueue_status WHERE 
  rsqname='queue_name';
```

另一个名为 `pg_stat_resqueue` 的系统视图显示资源队列随时间变化的统计指标。不过，要使用此视图，必须启用服务器配置参数 `stats_queue_level`。有关使用资源队列的更多信息，请参见《Apache Cloudberry 管理员指南》中的“管理工作负载和资源”。

`CREATE RESOURCE QUEUE` 不能在事务中运行。

此外，在 `EXPLAIN ANALYZE` 命令执行期间运行的 SQL 语句不受资源队列限制。

## 示例 {#examples}

创建活动查询上限为 20 的资源队列：

```sql
CREATE RESOURCE QUEUE myqueue WITH (ACTIVE_STATEMENTS=20);
```

创建活动查询上限为 20、总内存上限为 2000MB 的资源队列（执行时每个查询将分配 100MB Segment 主机内存）：

```sql
CREATE RESOURCE QUEUE myqueue WITH (ACTIVE_STATEMENTS=20, 
  MEMORY_LIMIT='2000MB');
```

创建查询成本上限为 3000.0 的资源队列：

```sql
CREATE RESOURCE QUEUE myqueue WITH (MAX_COST=3000.0);
```

创建查询成本上限为 310（或 30000000000.0）且不允许超额提交的资源队列，并允许成本低于 500 的小查询立即运行：

```sql
CREATE RESOURCE QUEUE myqueue WITH (MAX_COST=3e+10, 
  COST_OVERCOMMIT=FALSE, MIN_COST=500.0);
```

同时设置活动查询上限和查询成本上限的资源队列：

```sql
CREATE RESOURCE QUEUE myqueue WITH (ACTIVE_STATEMENTS=30, 
  MAX_COST=5000.00);
```

创建活动查询上限为 5 且优先级为最大值的资源队列：

```sql
CREATE RESOURCE QUEUE myqueue WITH (ACTIVE_STATEMENTS=5, 
  PRIORITY=MAX);
```

## 兼容性 {#compatibility}

`CREATE RESOURCE QUEUE` 是 Apache Cloudberry 的扩展。SQL 标准没有关于资源队列或资源管理的规定。

## 另请参阅 {#see-also}

[ALTER ROLE](/cloudberry/reference/sql-stmts/alter-role/), [CREATE ROLE](/cloudberry/reference/sql-stmts/create-role/), [ALTER RESOURCE QUEUE](/cloudberry/reference/sql-stmts/alter-resource-queue/), [DROP RESOURCE QUEUE](/cloudberry/reference/sql-stmts/drop-resource-queue/)
