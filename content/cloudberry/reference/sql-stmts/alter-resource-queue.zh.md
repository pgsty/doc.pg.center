---
title: "ALTER RESOURCE QUEUE"
description: "修改资源队列的限制。"
weight: 240
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-resource-queue.md"
---

## 概要 {#synopsis}

```sql
ALTER RESOURCE QUEUE <name> WITH ( <queue_attribute>=<value> [, ... ] ) 
```

其中 queue_attribute 为：

```sql
ACTIVE_STATEMENTS=<integer>
MEMORY_LIMIT='<memory_units>'
MAX_COST=<float>
COST_OVERCOMMIT={TRUE|FALSE}
MIN_COST=<float>
PRIORITY={MIN|LOW|MEDIUM|HIGH|MAX}
```

```sql
ALTER RESOURCE QUEUE <name> WITHOUT ( <queue_attribute> [, ... ] )
```

其中 queue_attribute 为：

```sql
ACTIVE_STATEMENTS
MEMORY_LIMIT
MAX_COST
COST_OVERCOMMIT
MIN_COST
```

> **注意** 资源队列必须具有 `ACTIVE_STATEMENTS` 或 `MAX_COST` 值。不要同时从资源队列中移除这两个 `queue_attributes`。

## 说明 {#description}

`ALTER RESOURCE QUEUE` 用于修改资源队列的限制。只有超级用户才能修改资源队列。资源队列必须具有 `ACTIVE_STATEMENTS` 或 `MAX_COST` 值（也可以两者都有）。你还可以设置或重置资源队列的优先级，以控制与该队列关联的查询所使用的可用 CPU 资源的相对份额；或者设置或重置资源队列的内存限制，以控制通过该队列提交的所有查询在一台 Segment 主机上可以消耗的内存量。

`ALTER RESOURCE QUEUE WITHOUT` 用于移除先前为某项资源设置的指定限制。资源队列必须具有 `ACTIVE_STATEMENTS` 或 `MAX_COST` 值。不要同时从资源队列中移除这两个 `queue_attributes`。

## 参数 {#parameters}

**`name`**

要修改其限制的资源队列的名称。

**`ACTIVE_STATEMENTS integer`**

系统在任一时刻允许的、由此资源队列中的用户提交的活动语句的数量。`ACTIVE_STATEMENTS` 的值应为大于 0 的整数。要将 `ACTIVE_STATEMENTS` 重置为无限制，请输入 `-1`。

**`MEMORY_LIMIT 'memory_units'`**

为此资源队列中的用户提交的所有语句设置总内存配额。内存单位可以用 kB、MB 或 GB 指定。资源队列的最小内存配额为 10MB。没有最大值；但是，查询执行时的上限受 Segment 主机物理内存的限制。默认值为无限制（`-1`）。

**`MAX_COST float`**

系统在任一时刻允许的、由此资源队列中的用户提交的语句的查询优化器代价总和。`MAX_COST` 的值指定为浮点数（例如 100.0），也可以指定为指数形式（例如 1e+2）。要将 `MAX_COST` 重置为无限制，请输入 `-1.0`。

**`COST_OVERCOMMIT boolean`**

如果资源队列基于查询代价进行限制，管理员可以允许代价超额提交（`COST_OVERCOMMIT=TRUE`，默认值）。这意味着，超过允许代价阈值的查询将被允许运行，但仅限于系统空闲时。如果指定 `COST_OVERCOMMIT=FALSE`，超过代价限制的查询将始终被拒绝，永远不允许运行。

**`MIN_COST float`**

代价低于此限制的查询不会排队，而是立即运行。代价以磁盘页面读取次数为单位度量；1.0 相当于一次顺序磁盘页面读取。`MIN_COST` 的值指定为浮点数（例如 100.0），也可以指定为指数形式（例如 1e+2）。要将 `MIN_COST` 重置为无限制，请输入 `-1.0`。

**`PRIORITY={MIN|LOW|MEDIUM|HIGH|MAX}`**

设置与资源队列关联的查询的优先级。在发生争用时，优先级较高的队列中的查询或语句将获得更大份额的可用 CPU 资源。低优先级队列中的查询可能会在优先级较高的查询运行期间被延迟。

## 注解 {#notes}

GPORCA 和 Postgres 规划器使用不同的查询代价模型，对同一查询可能计算出不同的代价。Apache Cloudberry 资源队列资源管理方案既不区分也不对齐 GPORCA 与 Postgres 规划器之间的代价；它使用优化器返回的字面代价值来限制查询。

启用基于资源队列的资源管理时，请对资源队列使用 `MEMORY_LIMIT` 和 `ACTIVE_STATEMENTS` 限制，而不要配置基于代价的限制。即使使用 GPORCA，Apache Cloudberry 也可能对某些查询回退到 Postgres 规划器，因此使用基于代价的限制可能导致意外结果。

## 示例 {#examples}

修改资源队列的活动查询限制：

```sql
ALTER RESOURCE QUEUE myqueue WITH (ACTIVE_STATEMENTS=20);
```

修改资源队列的内存限制：

```sql
ALTER RESOURCE QUEUE myqueue WITH (MEMORY_LIMIT='2GB');
```

将资源队列的最大和最小查询代价限制重置为无限制：

```sql
ALTER RESOURCE QUEUE myqueue WITH (MAX_COST=-1.0, 
  MIN_COST= -1.0);
```

将资源队列的查询代价限制重置为 310（即 30000000000.0），并且不允许超额提交：

```sql
ALTER RESOURCE QUEUE myqueue WITH (MAX_COST=3e+10, 
  COST_OVERCOMMIT=FALSE);
```

将与资源队列关联的查询的优先级重置为最低级别：

```sql
ALTER RESOURCE QUEUE myqueue WITH (PRIORITY=MIN);
```

从资源队列中移除 `MAX_COST` 和 `MEMORY_LIMIT` 限制：

```sql
ALTER RESOURCE QUEUE myqueue WITHOUT (MAX_COST, MEMORY_LIMIT);
```

## 兼容性 {#compatibility}

`ALTER RESOURCE QUEUE` 语句是 Apache Cloudberry 的扩展。标准 PostgreSQL 中不存在该命令。

## 另请参阅 {#see-also}

[CREATE RESOURCE QUEUE](/cloudberry/reference/sql-stmts/create-resource-queue/)、[DROP RESOURCE QUEUE](/cloudberry/reference/sql-stmts/drop-resource-queue/)、[CREATE ROLE](/cloudberry/reference/sql-stmts/create-role/)、[ALTER ROLE](/cloudberry/reference/sql-stmts/alter-role/)
