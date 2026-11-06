---
title: "ALTER RESOURCE GROUP"
description: "修改资源组的限制。"
weight: 230
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-resource-group.md"
---

## 概要 {#synopsis}

```sql
ALTER RESOURCE GROUP <name> SET <group_attribute> <value>
```

其中 group_attribute 为以下之一：

```sql
CPU_MAX_PERCENT=<integer> | CPUSET=<coordinator_cores>;<segment_cores>
[ MEMORY_LIMIT=<integer> ]
[ CPU_WEIGHT=<integer> ]
[ CONCURRENCY=<integer> ]
[ MIN_COST=<integer> ]
```

## 说明 {#description}

`ALTER RESOURCE GROUP` 用于修改资源组的限制。只有超级用户才能修改资源组。

对于为角色创建的资源组，你可以设置或重置其并发限制，以控制该组中同时处于活动状态的语句的最大数量。你还可以重置资源组的内存或 CPU 资源，以控制通过该组提交的所有查询在每台 Segment 主机上可以消耗的内存或 CPU 资源量。

修改资源组的 CPU 资源管理模式或限制时，新的模式或限制会立即生效。

修改为角色创建的资源组的内存限制时，如果当前资源使用量小于或等于新值，并且该资源组中没有正在运行的事务，则新的资源限制会立即生效。如果当前资源使用量超过新的内存限制值，或者其他资源组中有正在运行的事务占用了部分资源，则 Apache Cloudberry 会推迟分配新的限制，直到资源使用量回落到新值的范围之内。

增加为外部组件创建的资源组的内存限制时，新的资源限制会随着系统内存资源变为可用而逐步生效。减少为外部组件创建的资源组的内存限制时，其行为取决于具体组件。例如，如果减少为 PL/Container 运行时创建的资源组的内存限制，正在运行的容器中的查询可能会因内存不足而失败。

单次 `ALTER RESOURCE GROUP` 调用只能修改一种限制类型。

## 参数 {#parameters}

**`name`**

要修改的资源组的名称。

**`CONCURRENCY integer`**

该资源组允许的最大并发事务数，包括活动事务和空闲事务。`CONCURRENCY` 的值必须是 [0 .. `max_connections`] 范围内的整数。为角色定义的资源组的默认 `CONCURRENCY` 值为 20。

对于为外部组件创建的资源组，必须将 `CONCURRENCY` 设置为 `0`。

> **注意** 不能将 `admin_group` 的 `CONCURRENCY` 值设置为 `0`。

**`CPU_MAX_PERCENT integer`**

该资源组可以使用的最大可用 CPU 资源的百分比。取值范围为 `1-100`。

**`CPU_WEIGHT integer`**

当前组的调度优先级。取值范围为 `1-500`，默认值为 100。

**`CPUSET <coordinator_cores>;<segment_cores>`**

`CPUSET` 指定在 Coordinator 主机和 Segment 主机上为该资源组保留的 CPU 核。你指定的 CPU 核必须在系统中可用，并且不能与为其他资源组指定的 CPU 核重叠。

> **注意** 创建资源组时，必须指定 `CPU_MAX_PERCENT` 或 `CPUSET` 之一，但不能同时指定两者。

将核指定为以逗号分隔的列表，列表项可以是单个核编号或核编号区间。先定义 Coordinator 主机的核，再定义 Segment 主机的核，两者之间用分号分隔。必须用单引号将完整的核配置括起来。例如，'1;1,3-4' 表示为 Coordinator 主机配置核 1，为 Segment 主机配置核 1、3 和 4。

> **注意** 只有在为 Apache Cloudberry 集群启用了基于资源组的资源管理之后，才能为资源组配置 `CPUSET`。

**`MEMORY_LIMIT integer`**

为该资源组保留的最大可用内存，单位为 MB。该值决定了查询执行期间，资源组内所有工作进程在一台 Segment 主机上可以消耗的内存总量。

可以为资源组指定的最小内存量为 `0`。默认值为 `-1`。

指定 `MEMORY_LIMIT` 为 `-1` 时，`MEMORY LIMIT` 取服务器配置参数 `statement_mem` 的值。

> **注意** 如果设置了服务器配置参数 `gp_resgroup_memory_query_fixed_mem`，则在会话级别上，其值会覆盖 `MEMORY_LIMIT` 的值。

**`MIN_COST integer`**

对该资源组中查询所生成的查询计划的代价限制。当查询的查询计划代价小于该值时，该查询将脱离其所属的资源组。

这意味着低代价查询会执行得更快，因为它们不受资源约束。

取值范围为 `0-500`。默认值为 `0`，表示不使用代价来绕过查询。

## 注解 {#notes}

使用 [CREATE ROLE](/cloudberry/reference/sql-stmts/create-role/) 或 [ALTER ROLE](/cloudberry/reference/sql-stmts/alter-role/) 为角色（用户）分配特定的资源组。

不能在显式事务或子事务中提交 `ALTER RESOURCE GROUP` 命令。

## 示例 {#examples}

修改资源组的活动事务限制：

```sql
ALTER RESOURCE GROUP rgroup1 SET CONCURRENCY 13;
```

更新资源组的 CPU 限制：

```sql
ALTER RESOURCE GROUP rgroup2 SET CPU_MAX_PERCENT 45;
```

更新资源组的内存限制：

```sql
ALTER RESOURCE GROUP rgroup3 SET MEMORY_LIMIT 30;
```

在 Coordinator 主机和所有 Segment 主机上为资源组保留 CPU 核 1：

```sql
ALTER RESOURCE GROUP rgroup5 SET CPUSET '1;1';
```

## 兼容性 {#compatibility}

`ALTER RESOURCE GROUP` 语句是 Apache Cloudberry 的扩展。标准 PostgreSQL 中不存在该命令。

## 另请参阅 {#see-also}

[CREATE RESOURCE GROUP](/cloudberry/reference/sql-stmts/create-resource-group/)、[DROP RESOURCE GROUP](/cloudberry/reference/sql-stmts/drop-resource-group/)、[CREATE ROLE](/cloudberry/reference/sql-stmts/create-role/)、[ALTER ROLE](/cloudberry/reference/sql-stmts/alter-role/)
