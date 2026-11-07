---
title: 配置
linkTitle: 配置
description: AgensGraph 的配置就是 PostgreSQL 配置，再加上它自己的十一个设置。
type: docs
weight: 20
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/operations/configuration.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: complete
---


AgensGraph 的配置就是 PostgreSQL 配置，再加上它自己的十一个设置。本页说明如何设置，以及哪些设置对图负载重要。AgensGraph 新增的设置参见[服务器设置](/zh/agensgraph/reference/guc/)。本页未列出的数百个 PostgreSQL 设置，参见 [PostgreSQL 服务器配置章节](https://www.postgresql.org/docs/18/runtime-config.html)——它原样适用。

## 设置可以写在哪里 {#where-a-setting-can-be-set}

作用域从最宽到最窄排列；适用的最窄作用域获胜。

| 方式 | 作用域 | 说明 |
| --- | --- | --- |
| `postgresql.conf` | 整个集群 | 编辑文件后执行 `ag_ctl reload`；如果设置的 context 是 `postmaster`，则重启。 |
| `ALTER SYSTEM SET` | 整个集群 | 写入 `postgresql.auto.conf`；仍需要 reload 或重启。 |
| `ALTER DATABASE db SET` | 单个数据库 | 下一次连接生效。 |
| `ALTER ROLE r SET` | 单个角色 | 下一次连接生效。 |
| `SET` | 当前会话 | 断开连接后恢复。`SET LOCAL` 在事务结束时恢复。 |

`graph_path` 是你会最先遇到的设置，本质上是会话级的。如果每个会话都要使用同一个图，可以为数据库设置：

```sql
ALTER DATABASE mydb SET graph_path = moviekb;
```

查看设置当前是什么、值来自哪里：

```sql
SELECT name, setting, source, sourcefile, sourceline
FROM pg_settings WHERE name = 'work_mem';
```

`SHOW ALL` 列出全部。`pg_settings` 把同样信息呈现为可过滤的表，因此更有用——`boot_val` 列是内置默认值，`reset_val` 是 `RESET` 会得到的值，`context` 说明修改是否需要重启。

> [!NOTE]
> 请从 `pg_settings.boot_val` 读取内置默认值，不要读安装目录中带注释的 `postgresql.conf.sample`。`boot_val` 才是服务端实际启动时使用的值。

## 内存 {#memory}

这四项决定了服务端大部分行为；PostgreSQL 的默认值刻意设得很小，以便任何机器都能启动。

**`shared_buffers`**——服务端自己的页缓存。默认 128 MB。专用机器上，25% RAM 是合理起点。远高于 40% 通常适得其反，因为操作系统缓存也持有这些页。需要重启。

**`work_mem`**——单个排序或哈希在写入磁盘前可用的内存。默认 4 MB。它按操作计算，不按连接计算：一条图查询可能同时持有多个哈希，多连接查询可能使用这个值的若干倍。因此应逐步调高，并关注服务端是否内存不足。

**`maintenance_work_mem`**——用于 `VACUUM`、`ANALYZE`、`CREATE INDEX` 和 `REINDEX`。批量加载后建索引时，值得临时大幅调高，因为它一次只被一个命令使用。

**`effective_cache_size`**——不是分配，而是提示。它告诉规划器机器大约有多少内存可用于缓存。正是这个估计让索引扫描看起来可负担。可设为 RAM 的 50-75%。在大机器上保留 4 GB 默认值，是图遍历在索引扫描会胜出时选择顺序扫描的最常见原因。

## 对遍历重要的规划器设置 {#planner-settings-that-matter-for-traversal}

**`random_page_cost`**——规划器对随机页读取相对于顺序读取的估计，默认 4。这个比例描述的是机械盘。在 SSD 或 NVMe 上，真实比例远接近 1，而图遍历几乎全是随机访问：它按索引沿边进入分散的堆页。在闪存上把它降到约 1.1，是最可能改善遍历计划的单项修改。

不要盲信这一点，也不要推到极端。请测量：用 `EXPLAIN (ANALYZE, BUFFERS)` 分别在 4 和 1.1 下运行最慢的遍历并比较，然后保留在你的数据上胜出的值。接近零的值会告诉规划器随机 I/O 免费，即使在内存中也不是这样；它会乐意选择抖动严重的计划。

**`max_parallel_workers_per_gather`**——默认 2。图写入不并行执行，遍历也大部分是串行的，因此收益主要来自 `MATCH` 降级得到的顺序扫描和位图扫描。调高它有助于面向整个标签的分析查询。

**`jit`**——默认开启。长时间运行的分析查询能收回成本，短查询则付出编译时间。如果负载是大量小遍历，请测量关闭后的效果。

## PostgreSQL 18 的异步 I/O {#asynchronous-io-on-postgresql-18}

PostgreSQL 18 引入了异步 I/O，图查询可以免费获得其中一部分。这一点值得理解，因为收益来自配置修改，而不是查询修改。

定长 `MATCH` 会降级为标签表上的普通顺序、位图和索引扫描；PostgreSQL 18 的预读被**顺序扫描和位图堆扫描**使用，因此它们自动受益。有两类访问不会：PostgreSQL 18 中普通索引扫描的堆读取没有预读，而可变长度、最短路径和 Dijkstra 引擎按设计一次走一个顶点。

两个设置控制它：

**`effective_io_concurrency`**——PostgreSQL 18 默认 16，之前是 1。它控制整个机制；如果你从旧版本沿用了 `postgresql.conf` 并把它固定为 1，就已经关闭异步 I/O。

**`io_method`**——默认 `worker`，在后台 worker 中执行读取。在 Linux 上，`io_uring` 对冷扫描更快，有时明显更快，但只有服务端构建时带 liburing 才可用。设置前先检查：

```sql
SELECT enumvals FROM pg_settings WHERE name = 'io_method';
```

```
 enumvals
---------------
 {sync,worker}
```

这个构建没有 `io_uring`；带它构建的版本会列出三个值。修改 `io_method` 需要重启。

数据放不进缓存时收益最大；已经缓存时接近零。因此想观察它要用冷缓存测试。不要期待它帮助最短路径查询——那类查询的瓶颈是串行探测，而不是 I/O。

## 日志 {#logging}

**`log_statement`**——默认 `none`。注意 2.18 的变化：`mod` 现在会记录 Cypher 写入。2.18 之前，Cypher 语句只有在 `all` 时才计入记录；因此要求记录数据修改语句的服务端会记录 SQL `INSERT`，却静默跳过旁边的 `CREATE`。

**`log_min_duration_statement`**——当图负载慢但不知道是哪条查询时，首选这个设置。它记录超过阈值的每条语句，包括 Cypher。

**`auto_explain`**——contrib 模块，也是图负载上最有用的诊断工具，因为慢遍历通常意味着计划变了，而不是数据变多了：

```
shared_preload_libraries = 'auto_explain'
auto_explain.log_min_duration = '3s'
auto_explain.log_analyze = on
```

## AgensGraph 新增设置 {#settings-agensgraph-adds}

共十一个，见[服务器设置](/zh/agensgraph/reference/guc/)：`allow_null_properties`、`auto_gather_graphmeta`、`cypher_allow_unsafe_ddl`、`eager_mem`、`enable_eager`、`enable_graph_ddl`、`enable_graph_dml`、`enable_graph_endpoint_elision`、`enable_multiple_update`、`enable_property_promotion`、`graph_path`。

与运维相关的有：

* **`graph_path`**——会话工作的图。没有它，任何对象都无法解析。
* **`auto_gather_graphmeta`**——保持 `ag_graphmeta` 最新，让规划器可以裁剪扫描。每次写入都有代价，因此默认关闭；权衡和 `regather_graphmeta()` 见[图元数据](/zh/agensgraph/system-catalogs/graph-metadata/)。
* **`enable_graph_dml`** 和 **`enable_graph_ddl`**——默认关闭，分别控制用 SQL 写入和重塑标签。维护工作之外请保持关闭。
* **`eager_mem`**——eager 图写计划可用的内存，与 `work_mem` 并列。

## 接下来 {#where-to-go-next}

* [部署](/zh/agensgraph/operations/deployment/)——容量、数据目录和 systemd 运行。
* [安全](/zh/agensgraph/operations/security/)——认证、角色和图上的权限。
* [查询性能](/zh/agensgraph/querying/performance/)——面向计划形态的调优，与本页是不同问题。
