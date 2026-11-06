---
title: "CREATE RESOURCE GROUP"
description: "定义新的资源组。"
weight: 740
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-resource-group.md"
---

## 语法概要 {#synopsis}

```sql
CREATE RESOURCE GROUP <name> WITH (<group_attribute>=<value> [, ... ])
```

其中 group_attribute 为以下选项之一：

```sql
CPU_MAX_PERCENT=<integer> | CPUSET=<coordinator_cores>;<segment_cores>
[ MEMORY_LIMIT=<integer> ]
[ CPU_WEIGHT=<integer> ]
[ CONCURRENCY=<integer> ]
[ MIN_COST=<integer> ]
```

## 说明 {#description}

为 Apache Cloudberry 资源管理创建新的资源组。可以创建资源组来管理角色的资源，也可以管理 PL/Container 等 Apache Cloudberry 外部组件的资源。

启用资源组后，为用户角色创建的资源组会规定该角色的并发事务数、内存和 CPU 限制。可以将此类资源组分配给一个或多个角色。

启用资源组后，为 Apache Cloudberry 外部组件（例如 PL/Container）创建的资源组会规定该组件的内存和 CPU 限制。这些资源组使用 cgroups 同时管理 CPU 和内存。外部组件的资源组分配由组件决定。例如，配置 PL/Container 运行时时分配 PL/Container 资源组。不能将为外部组件创建的资源组分配给角色，也不能将为角色创建的资源组分配给外部组件。

必须拥有 `SUPERUSER` 权限才能创建资源组。Apache Cloudberry 集群最多允许 100 个资源组。

Apache Cloudberry 预定义了两个默认资源组：`admin_group` 和 `default_group`。这些组名以及组名 `none` 均为保留名称。

要为资源组设置合适的限制，Apache Cloudberry 管理员必须熟悉系统中通常运行的查询、运行这些查询的用户/角色，以及可能使用的外部组件（例如 PL/Container）。

为角色创建资源组后，使用 [ALTER ROLE](/cloudberry/reference/sql-stmts/alter-role/) 或 [CREATE ROLE](/cloudberry/reference/sql-stmts/create-role/) 命令将该组分配给一个或多个角色。

创建用于管理外部组件 CPU 和内存资源的资源组后，配置外部组件使用该资源组。例如，配置 PL/Container 运行时的 `resource_group_id`。

## 参数 {#parameters}

**`name`**

资源组名称。

**`CONCURRENCY integer`**

可选。该资源组允许的最大并发事务数，包括活动事务和空闲事务。`CONCURRENCY` 值必须是 [0 .. `max_connections`] 范围内的整数。为角色定义的资源组中，`CONCURRENCY` 的默认值为 20。

为外部组件创建资源组时，必须将 `CONCURRENCY` 设为 `0`。

> **注意** 不能将 `admin_group` 的 `CONCURRENCY` 设为 `0`。

**`CPU_MAX_PERCENT integer`**

可选。资源组可以使用的最大可用 CPU 资源百分比。取值范围为 `1-100`。

**`CPU_WEIGHT integer`**

可选。当前组的调度优先级。取值范围为 `1-500`，默认值为 100。

**`CPUSET <coordinator_cores>;<segment_cores>`**

`CPUSET` 用于指定在 Coordinator 主机和 Segment 主机上为该资源组预留的 CPU 核。指定的 CPU 核必须在系统中可用，且不能与为其他资源组指定的 CPU 核重叠。

> **注意** 创建资源组时必须指定 `CPU_MAX_PERCENT` 或 `CPUSET` 之一，但不能同时指定两者。

使用逗号分隔的单个核编号或核编号区间列表指定核心。先定义 Coordinator 主机核心，再定义 Segment 主机核心，并用分号分隔两者。完整核心配置必须用单引号括起。例如，'1;1,3-4' 为 Coordinator 主机配置核心 1，为 Segment 主机配置核心 1、3 和 4。

> **注意** 只有在为 Apache Cloudberry 集群启用基于资源组的资源管理后，才能为资源组配置 `CPUSET`。

**`MEMORY_LIMIT integer`**

可选。为该资源组预留的最大可用内存，单位为 MB。此值决定查询执行期间 Segment 主机上该资源组内所有工作进程可消耗的内存总量。

可以为资源组指定的最小内存量为 `0`。默认值为 `-1`。

指定 `MEMORY_LIMIT` 为 `-1` 时，`MEMORY LIMIT` 取服务器配置参数 `statement_mem` 的值。

> **注意** 如果设置了服务器配置参数 `gp_resgroup_memory_query_fixed_mem`，它会在会话级覆盖 `MEMORY_LIMIT` 的值。

**`MIN_COST integer`**

可选。该资源组中查询生成的查询计划的代价限制。当查询计划代价小于此值时，会将查询从其所属资源组中取消分配。

这意味着低代价查询会更快执行，因为它们不受资源限制。

取值范围为 `0-500`。默认值为 `0`，表示不使用代价来绕过查询。

## 注意事项 {#notes}

不能在显式事务或子事务中提交 `CREATE RESOURCE GROUP` 命令。

使用 `gp_toolkit.gp_resgroup_config` 系统视图显示所有资源组的限制设置：

```sql
SELECT * FROM gp_toolkit.gp_resgroup_config;
```

## 示例 {#examples}

创建 CPU 和内存限制百分比均为 35 的资源组：

```sql
CREATE RESOURCE GROUP rgroup1 WITH (CPU_MAX_PERCENT=35, MEMORY_LIMIT=35);
```

创建并发事务上限为 20、内存上限为 15、CPU 上限为 25 的资源组：

```sql
CREATE RESOURCE GROUP rgroup2 WITH (CONCURRENCY=20, 
  MEMORY_LIMIT=15, CPU_MAX_PERCENT=25);
```

创建用于管理 PL/Container 资源的资源组，指定内存上限为 10、CPU 上限为 10：

```sql
CREATE RESOURCE GROUP plc_run1 WITH (MEMORY_LIMIT=10, CPU_MAX_PERCENT=10,
  CONCURRENCY=0);
```

创建内存限制百分比为 11 的资源组，并为其分配 Coordinator 主机的 CPU 核 1 以及 Segment 主机的 CPU 核 1 到 3：

```sql
CREATE RESOURCE GROUP rgroup3 WITH (CPUSET='1;1-3', MEMORY_LIMIT=11);
```

## 兼容性 {#compatibility}

`CREATE RESOURCE GROUP` 是 Apache Cloudberry 的扩展。SQL 标准没有关于资源组或资源管理的规定。

## 另请参阅 {#see-also}

[ALTER ROLE](/cloudberry/reference/sql-stmts/alter-role/), [CREATE ROLE](/cloudberry/reference/sql-stmts/create-role/), [ALTER RESOURCE GROUP](/cloudberry/reference/sql-stmts/alter-resource-group/), [DROP RESOURCE GROUP](/cloudberry/reference/sql-stmts/drop-resource-group/)
