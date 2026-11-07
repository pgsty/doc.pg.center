---
title: 查询性能优化
description: 了解如何优化 Citus 查询性能，以便优化分布式 PostgreSQL 工作负载并加快查询速度。
weight: 40
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/performance-tuning?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
---

本文介绍如何调优 Citus 集群以获得最高性能，以及与性能相关的若干配置参数。选择合适的分布列会影响性能。可以先将数据库调优到单台 PostgreSQL 服务器上的高性能状态，再将工作负载扩展到集群中的所有 CPU。

## 表分布和分片 {#table-distribution-and-shards}

创建分布式表的第一步是选择合适的分布列。这有助于 Citus 将多个操作直接下推到工作节点上的分片，并排除无关分片，从而显著加快查询。

通常应选择最常用的 `join key`，或大多数查询用于过滤的列，作为分布列。对于过滤，Citus 使用分布列的范围排除无关分片，确保查询只访问与 WHERE 子句范围重叠的分片。对于连接，如果 `join key` 就是分布列，Citus 只在分布列范围匹配或重叠的分片之间执行连接。所有这些分片上的连接都可以在工作节点上并行执行，因此效率更高。

此外，如果操作基于分布列，Citus 可以将其直接下推到工作节点上的分片。这样可以大幅减少每个节点上的计算量，以及跨节点传输数据所需的网络带宽。

选择合适的分布列后，下一步是调优工作节点的性能。

## PostgreSQL 优化 {#postgresql-tuning}

Citus 协调节点将传入查询拆分为片段查询，并发送到工作节点并行处理。工作节点是经过扩展的 PostgreSQL 服务器，会对这些查询应用 PostgreSQL 的标准规划和执行逻辑。调优 Citus 的第一步，是调优工作节点上的 PostgreSQL 配置参数以获得高性能。

参数调优需要反复试验，通常要尝试多次才能达到可接受的性能。调优时最好只加载一小部分数据，让每次迭代更快完成。

开始调优前，创建 Citus 集群并向其中加载数据。在协调节点上对有代表性的查询运行 EXPLAIN，检查其性能。Citus 扩展了 EXPLAIN 命令，可提供分布式查询执行的信息。EXPLAIN 输出会显示每个工作节点如何处理查询，以及协调节点如何合并结果。

下面的示例显示一个查询的计划。使用 VERBOSE 标志可以查看发送到工作节点的实际查询。

```sql
EXPLAIN VERBOSE
 SELECT date_trunc('minute', created_at) AS minute,
        sum((payload->>'distinct_size')::int) AS num_commits
   FROM github_events
  WHERE event_type = 'PushEvent'
  GROUP BY minute
  ORDER BY minute;
```

```text
    Sort (cost=0.00..0.00 rows=0 width=0)
      Sort Key: remote_scan.minute
      -> HashAggregate (cost=0.00..0.00 rows=0 width=0)
        Group Key: remote_scan.minute
        -> Custom Scan (Citus Adaptive) (cost=0.00..0.00 rows=0 width=0)
          Task Count: 32
          Tasks Shown: One of 32
          -> Task
            Query: SELECT date_trunc('minute'::text, created_at) AS minute, sum(((payload OPERATOR(pg_catalog.->>) 'distinct_size'::text))::integer) AS num_commits FROM github_events_102042 github_events WHERE (event_type OPERATOR(pg_catalog.=) 'PushEvent'::text) GROUP BY (date_trunc('minute'::text, created_at))
            Node: host=localhost port=5433 dbname=postgres
            -> HashAggregate (cost=93.42..98.36 rows=395 width=16)
              Group Key: date_trunc('minute'::text, created_at)
              -> Seq Scan on github_events_102042 github_events (cost=0.00..88.20 rows=418 width=503)
                Filter: (event_type = 'PushEvent'::text)
    (13 rows)
```

共有 32 个分片，规划器选择 Citus 自适应执行器执行此查询：

```text
  -> Custom Scan (Citus Adaptive) (cost=0.00..0.00 rows=0 width=0)
      Task Count: 32
```

接下来，规划器选择其中一个工作节点，并展示查询在那里如何执行。输出中包含发送到工作节点的主机、端口、数据库和查询；如有需要，可以直接连接该工作节点测试查询：

```text
  Tasks Shown: One of 32
    -> Task
      Query: SELECT date_trunc('minute'::text, created_at) AS minute, sum(((payload OPERATOR(pg_catalog.->>) 'distinct_size'::text))::integer) AS num_commits FROM github_events_102042 github_events WHERE (event_type OPERATOR(pg_catalog.=) 'PushEvent'::text) GROUP BY (date_trunc('minute'::text, created_at))
      Node: host=localhost port=5433 dbname=postgres
```

接下来，分布式 EXPLAIN 显示在该工作节点上对片段查询运行普通 PostgreSQL EXPLAIN 的结果：

```text
  -> HashAggregate (cost=93.42..98.36 rows=395 width=16)
      Group Key: date_trunc('minute'::text, created_at)
      -> Seq Scan on github_events_102042 github_events (cost=0.00..88.20 rows=418 width=503)
        Filter: (event_type = 'PushEvent'::text)
```

现在可以使用标准 PostgreSQL 技术连接到 `localhost` 的 5433 端口，调优分片 github_events_102042 上的查询性能。每次修改后，都可以从协调节点或直接在工作节点上再次运行 EXPLAIN。

这类优化首先涉及配置设置。PostgreSQL 默认使用较为保守的资源设置，其中 `shared_buffers` 和 `work_mem` 可能是优化读取性能时最重要的两个参数。本文稍后会讨论这些参数。除此之外，还有多个配置设置会影响查询性能；详见 [PostgreSQL 手册](http://www.postgresql.org/docs/current/static/runtime-config.html)及 [PostgreSQL 9.0 High Performance](http://www.amazon.com/PostgreSQL-High-Performance-Gregory-Smith/dp/184951030X)。

`shared_buffers` 定义数据库用于缓存数据的内存量，默认值为 128 MB。如果工作节点有 1 GB 或更多内存，一个合理的 `shared_buffers` 起始值是系统内存的四分之一。某些工作负载适合更大的 `shared_buffers` 设置。由于 PostgreSQL 还依赖操作系统缓存，通常很难证明使用超过内存 25% 的值比更小的值更好。

如果经常执行复杂排序，提高 `work_mem` 可以让 PostgreSQL 在内存中执行更大的排序，比基于磁盘的排序更快。如果工作节点内存充足却仍有大量磁盘活动，提高 `work_mem` 可能会有所帮助。这有助于 PostgreSQL 选择更高效的查询计划，并让更多操作在内存中完成。

除配置设置外，PostgreSQL 查询规划器还依赖表内容的统计信息来生成良好计划。默认情况下会启用 ANALYZE，并在运行时收集统计信息。有关 PostgreSQL 规划器和 ANALYZE 命令的更多信息，请参阅 [PostgreSQL 文档](http://www.postgresql.org/docs/current/static/sql-analyze.html)。

最后，可以在表上创建索引以提高数据库性能。索引让数据库比没有索引时更快地查找和获取特定行。要选择最有效的索引，请使用 [EXPLAIN](http://www.postgresql.org/docs/current/static/sql-explain.html) 运行查询。通过 `EXPLAIN` 查看查询计划，并优化较慢的部分。创建索引后，系统必须使其与表保持同步，这会增加数据操作的开销。因此，应删除查询中很少使用或从不使用的索引。

要提高写入性能，可以通过常规 PostgreSQL 配置调优来提高 INSERT 速率。建议提高 `checkpoint_timeout` 和 `max_wal_size`。此外，可根据应用程序的可靠性要求选择修改 `fsync` 或 `synchronous_commit`。

将一个工作节点调优到满意状态后，也要手动将这些变更应用到其他工作节点。要验证它们的行为是否一致，可在协调节点上设置以下配置变量：

```sql
SET citus.explain_all_tasks = 1;
```

现在，EXPLAIN 会显示所有任务的查询计划，而不只是一个任务。

```sql
EXPLAIN
 SELECT date_trunc('minute', created_at) AS minute,
        sum((payload->>'distinct_size')::int) AS num_commits
   FROM github_events
  WHERE event_type = 'PushEvent'
  GROUP BY minute
  ORDER BY minute;
```

```text
    Sort (cost=0.00..0.00 rows=0 width=0)
      Sort Key: remote_scan.minute
      -> HashAggregate (cost=0.00..0.00 rows=0 width=0)
        Group Key: remote_scan.minute
        -> Custom Scan (Citus Adaptive) (cost=0.00..0.00 rows=0 width=0)
          Task Count: 32
          Tasks Shown: All
          -> Task
            Node: host=localhost port=5433 dbname=postgres
            -> HashAggregate (cost=93.42..98.36 rows=395 width=16)
              Group Key: date_trunc('minute'::text, created_at)
              -> Seq Scan on github_events_102042 github_events (cost=0.00..88.20 rows=418 width=503)
                Filter: (event_type = 'PushEvent'::text)
          -> Task
            Node: host=localhost port=5434 dbname=postgres
            -> HashAggregate (cost=103.21..108.57 rows=429 width=16)
              Group Key: date_trunc('minute'::text, created_at)
              -> Seq Scan on github_events_102043 github_events (cost=0.00..97.47 rows=459 width=492)
                Filter: (event_type = 'PushEvent'::text)
          --
          -- ... repeats for all 32 tasks
          --     alternating between workers one and two
          --     (running in this case locally on ports 5433, 5434)
          --

    (199 rows)
```

工作节点执行结果的差异可能来自配置调优差异、分片间数据分布不均，或机器硬件差异。要进一步了解查询在每个分片上的运行时间，请使用 EXPLAIN ANALYZE。

> [!NOTE]
> 启用 `citus.explain_all_tasks` 后，EXPLAIN 计划会按顺序获取；对于 EXPLAIN ANALYZE，这可能需要很长时间。

默认情况下，Citus 按执行时间降序排列任务。如果禁用 `citus.explain_all_tasks`，Citus 会显示运行时间最长的单个任务。此功能只能与 EXPLAIN ANALYZE 一起使用，因为普通 EXPLAIN 不执行查询，也就不知道执行时间。可以使用 `explain_analyze_sort_method` 更改排序方式。

## 横向扩展性能 {#scale-out-performance}

达到单个分片的目标性能后，可以在所有工作节点上设置相似的配置参数。Citus 会在工作节点之间并行运行片段查询，因此查询性能可以扩展到集群中所有 CPU 核心计算能力的总和。唯一的限制是数据能否装入内存。

为了让 Citus 获得最佳性能，应尽量将更多工作集放入内存。如果无法将整个工作集放入内存，最佳实践是使用固态硬盘（SSD），而不是硬盘驱动器（HDD）。HDD 在连续数据块的顺序读取上表现尚可，但随机读写性能较低。并发查询大量执行随机读写时，SSD 的查询性能可能比 HDD 高出数倍。如果查询的计算量很大，还应考虑选择 CPU 更强的机器。

要测量数据库对象的磁盘空间使用量，可以登录工作节点，使用 [PostgreSQL 管理函数](http://www.postgresql.org/docs/current/static/functions-admin.html#FUNCTIONS-ADMIN-DBSIZE)测量各个分片。`pg_total_relation_size()` 可用于获取表占用的总磁盘空间；也可以使用 PostgreSQL 文档中的其他函数获取更具体的大小信息。根据分片大小和分片数量，可以计算集群的硬件需求。

每个工作节点上的分片数量也会影响性能。Citus 将传入查询拆分为片段查询，这些查询在工作节点上的各个分片中运行。因此，查询命中的分片数决定了每个查询的并行度。要获得最大并行度，应在每个节点上创建足够多的分片，使每个 CPU 核心至少对应一个分片。如果查询按分布列过滤，Citus 会对无关分片进行剪枝。分片数多于核心数也可能有益，因为即使剪枝后仍能获得更高并行度。

## 分布式查询性能优化 {#distributed-query-performance-tuning}

在集群中分布数据并将每个工作节点调优到最佳性能后，查询通常会获得显著提升。最后一步是调优几个分布式性能参数。

在调整具体配置参数前，应测量分布式集群上的查询时间，并与单个分片的性能比较。在协调节点上启用相关设置、计时并运行查询，再在工作节点上运行其中一个片段查询。这些操作有助于确定时间花在工作节点上的部分，以及将数据取回协调节点所花的时间，然后据此找出瓶颈并优化数据库。

有一些参数可用于优化分布式查询规划器和执行器，分为常规参数和高级参数。常规性能调优部分足以覆盖大多数用例和常见配置；高级性能调优部分介绍一些可能在特定用例中带来性能提升的参数。

### 常规 {#general}

要提高 INSERT 性能，并发度对插入速率的影响最大。可以尝试并行运行多个并发 INSERT 语句。如果协调节点足够强大，能够同时使用其全部 CPU 核心，就可以获得较高的插入速率。

#### 子查询/CTE 网络开销 {#subquerycte-network-overhead}

在最佳情况下，Citus 可以在一个步骤中运行包含子查询和 CTE 的查询。这通常是因为主查询和子查询都以相同方式按表的分布列过滤，并且可以一起下推到工作节点。然而，有时 Citus 必须先执行子查询，再执行主查询，并将子查询的中间结果复制到其他工作节点供主查询使用。这种技术称为“推拉执行”。

如果子查询需要单独执行一个步骤，应避免在工作节点之间发送过多数据，因为网络开销会降低性能。EXPLAIN 命令可以帮助了解查询的执行方式，包括是否需要多个步骤。更多信息请参阅[子查询/CTE 推拉执行](/citus/reference/reference-processing/#subquery-and-cte-push-pull-execution)。

还可以主动设置保护措施，防止产生大型中间结果。在与协调节点的新连接中调整 `max_intermediate_result_size` 限制。默认的最大中间结果大小为 1 GB，足以容纳一些低效查询。可以将该值调低后运行查询：

```sql
-- set a restrictive limit for intermediate results
SET citus.max_intermediate_result_size = '512kB';

-- attempt to run queries
-- SELECT ...
```

如果查询具有超出此限制的子查询或 CTE，则会取消查询，并看到错误消息：

```text
ERROR: the intermediate result size exceeds citus.max_intermediate_result_size (currently 512 kB)
DETAIL: Citus restricts the size of intermediate results of complex subqueries and CTEs to avoid accidentally pulling large result sets into once place.
HINT: To run the current query, set citus.max_intermediate_result_size to a higher value or -1 to disable.
```

可以在 EXPLAIN ANALYZE 输出中获取中间结果的大小及其目标位置。

```sql
EXPLAIN ANALYZE
WITH deleted_rows AS (
  DELETE FROM page_views WHERE tenant_id IN (3, 4) RETURNING *
), viewed_last_week AS (
  SELECT * FROM deleted_rows WHERE view_time > current_timestamp - interval '7 days'
)
SELECT count(*) FROM viewed_last_week;
```

```text
    Custom Scan (Citus Adaptive) (cost=0.00..0.00 rows=0 width=0) (actual time=570.076..570.077 rows=1 loops=1)
      -> Distributed Subplan 31_1
            Subplan Duration: 6978.07 ms
            Intermediate Data Size: 26 MB
            Result destination: Write locally
            -> Custom Scan (Citus Adaptive) (cost=0.00..0.00 rows=0 width=0) (actual time=364.121..364.122 rows=0 loops=1)
                  Task Count: 2
                  Tuple data received from nodes: 0 bytes
                  Tasks Shown: One of 2
                  -> Task
                        Tuple data received from node: 0 bytes
                        Node: host=localhost port=5433 dbname=postgres
                        -> Delete on page_views_102016 page_views (cost=5793.38..49272.28 rows=324712 width=6) (actual time=362.985..362.985 rows=0 loops=1)
                              -> Bitmap Heap Scan on page_views_102016 page_views (cost=5793.38..49272.28 rows=324712 width=6) (actual time=362.984..362.984 rows=0 loops=1)
                                    Recheck Cond: (tenant_id = ANY ('{3,4}'::integer[]))
                                    -> Bitmap Index Scan on view_tenant_idx_102016 (cost=0.00..5712.20 rows=324712 width=0) (actual time=19.193..19.193 rows=325733 loops=1)
                                          Index Cond: (tenant_id = ANY ('{3,4}'::integer[]))
                            Planning Time: 0.050 ms
                            Execution Time: 363.426 ms
            Planning Time: 0.000 ms
            Execution Time: 364.241 ms
     Task Count: 1
     Tuple data received from nodes: 6 bytes
     Tasks Shown: All
     -> Task
           Tuple data received from node: 6 bytes
           Node: host=localhost port=5432 dbname=postgres
           -> Aggregate (cost=33741.78..33741.79 rows=1 width=8) (actual time=565.008..565.008 rows=1 loops=1)
                 -> Function Scan on read_intermediate_result intermediate_result (cost=0.00..29941.56 rows=1520087 width=0) (actual time=326.645..539.158 rows=651466 loops=1)
                       Filter: (view_time > (CURRENT_TIMESTAMP - '7 days'::interval))
               Planning Time: 0.047 ms
               Execution Time: 569.026 ms
    Planning Time: 1.522 ms
    Execution Time: 7549.308 ms
```

在 EXPLAIN ANALYZE 输出中，你将看到有关中间结果的以下信息：

Intermediate Data Size: 26 MB Result destination: Write locally

输出显示中间结果的大小和写入位置。此处的 “Write locally” 表示写入负责协调查询执行的节点。其他查询也可能显示为以下形式：

Intermediate Data Size: 26 MB Result destination: Send to 2 nodes

这意味着中间结果被推送到两个工作节点，产生了更多网络流量。

使用 CTE，或连接 CTE 与分布式表时，可以遵循以下规则避免推拉执行：

- 表应共置。
- CTE 查询不应需要合并步骤（例如在非分布列上执行 LIMIT 或 GROUP BY）。
- 表和 CTE 应按分布列连接。

此外，PostgreSQL 12 及更高版本允许 Citus 利用 *CTE 内联*，在更多情况下将 CTE 下推到工作节点。可以使用 `MATERIALIZED` 关键字控制内联行为。更多信息请参阅 [PostgreSQL 文档](https://www.postgresql.org/docs/current/queries-with.html)。

### 高级 {#advanced}

本节讨论高级性能调优参数。这些参数适用于特定用例，并非所有部署都需要。

#### 连接管理 {#connection-management}

运行多分片查询时，Citus 必须在并行化收益和数据库连接开销之间取得平衡。[查询执行](https://docs.citusdata.com/en/stable/get_started/concepts.html#query-execution)介绍了如何将查询转换为工作节点任务，以及如何建立到工作节点的数据库连接。

- 对于查询较短的事务性工作负载（例如延迟低于 20 ms），将 `max_adaptive_executor_pool_size` 设置为 1 或 2 等较小值。对于并行度至关重要的分析工作负载，保留默认值 16。
- 对于由短查询组成、受网络延迟而非并行度限制的事务性工作负载，将 `executor_slow_start_interval` 设置为 100 ms 等较大值。对于分析工作负载，保留默认值 10 ms。
- `max_cached_conns_per_worker` 的默认值 1 通常合理。使用少量并发会话的集群可以尝试 2 等较大值，但不宜再大（例如 16 就过高）。设置过高会使会话保留空闲连接，不必要地占用工作节点资源。
- 将 `max_shared_pool_size` 设置为与你的*工作节点* [max_connections](https://www.postgresql.org/docs/current/runtime-config-connection.html#RUNTIME-CONFIG-CONNECTION-SETTINGS) 设置相同。此设置主要用于故障保护。

#### 任务分配策略 {#task-assignment-policy}

Citus 查询规划器根据分片位置将任务分配给工作节点。可以通过设置 `citus.task_assignment_policy` 配置参数选择分配算法，从而选用最适合用例的策略。

**greedy** 策略旨在将任务均匀分布到各工作节点，是默认策略，在大多数情况下都能正常工作。**round-robin** 策略以轮询方式在不同副本之间交替，将任务分配到工作节点。当表的分片数相对于工作节点较少时，轮询策略可以提高集群利用率。第三种策略是 **first-replica**，根据分片放置（副本）的插入顺序分配任务。使用此策略，可以确定每台机器访问哪些分片；它有助于提供更强的内存驻留保证，使工作集保持在内存中供查询使用。

#### 中间数据传输格式 {#intermediate-data-transfer-format}

在 PostgreSQL 13 及更低版本上，Citus 默认以文本格式在工作节点之间传输中间查询数据。对于 hll 或 hstore 数组等数据类型，序列化和反序列化的成本可能很高；此时使用二进制格式传输中间数据可以提高查询性能。可以启用 `binary_worker_copy_format` 配置选项使用二进制格式。

#### 二进制协议 {#binary-protocol}

在某些情况下，查询时间的大部分用于将查询结果从工作节点发送到协调节点。当查询请求大量行（例如 `select * from table`），或结果列使用大型类型（例如来自 postgresql-hll 和 tdigest 扩展的 `hll` 或 `tdigest`）时，就可能出现这种情况。

此时可以将 `citus.enable_binary_protocol` 设置为 `true`，把结果编码从文本改为二进制。对于具有紧凑二进制表示的类型（例如 `hll`、`tdigest`、`timestamp` 和 `double precision`），二进制编码可以显著减少带宽占用。

对于 PostgreSQL 14 及更高版本，此设置默认已经是 `true`。在这些 PostgreSQL 版本上显式启用它没有效果。

## 横向扩展数据引入 {#scale-out-data-ingestion}

Citus 支持将数据引入扩展到很高的速率，但需要权衡应用程序集成、吞吐量和延迟。本节讨论不同的数据引入方式，并给出吞吐量和延迟的预期范围。

### 实时插入和更新 {#real-time-inserts-and-updates}

在 Citus 协调节点上，可以直接对分布式表执行 INSERT、INSERT .. ON CONFLICT、UPDATE 和 DELETE。执行这些命令后，变更会立即对用户可见。

执行 INSERT（或其他数据引入命令）时，Citus 首先根据分布列的值找到正确的分片放置，然后连接存放这些分片放置的工作节点，并在相应节点上执行 INSERT。从用户角度看，由于连接工作节点存在网络延迟，INSERT 需要几毫秒才能完成；但 Citus 协调节点可以处理并发 INSERT，从而达到较高吞吐量。

#### 插入吞吐量 {#insert-throughput}

要使用 Citus 测量数据引入速率，可以使用名为 pgbench 的标准工具；本文提供可重复的基准测试步骤。

也可以使用 pgbench 等标准 PostgreSQL 基准测试工具测量 Citus 的数据引入速率。详细说明请参阅可重复的基准测试步骤。

基准测试结果取决于集群配置：

- 协调节点资源（CPU 核心、内存）
- 工作节点的数量和大小
- 节点之间的网络延迟
- pgbench 并发设置（线程和客户端计数）
- 数据库配置优化

例如，一个拥有双核协调节点和两个单核工作节点的基础 Citus 集群每秒可以处理数千次 INSERT。扩展到拥有 4–8 个核心和更多工作节点的强大硬件后，吞吐量可以显著提高，甚至达到每秒数万次事务。

基准测试的关键观察结果：

- 入门级集群每天可以处理数百万条事务性 INSERT 语句。
- CPU 容量为 4 倍的更强大集群每天可以处理数十亿条 INSERT 语句。
- 网络延迟和 PostgreSQL 连接处理通常会成为瓶颈。
- 在拥有多张表和多个索引的生产环境中，瓶颈可能转移到其他资源。

#### 更新吞吐量 {#update-throughput}

要使用 Citus 测量 UPDATE 吞吐量，可以采用 INSERT 测试使用的相同步骤。

UPDATE 性能与 INSERT 性能遵循类似模式。吞吐量取决于集群配置、并发设置，以及更新是分布在多个分片上还是集中在特定分区上。

| 协调节点 | 工作节点 | 延迟（ms） | 每秒事务数 |
| --- | --- | --- | --- |
| 2 核 - 7.5GB RAM | 2 * （1 核 - 15GB RAM） | 25.0 | 10,200 |
| 4 核 - 15GB RAM | 2 * （1 核 - 15GB RAM） | 19.6 | 13,000 |
| 8 核 - 30GB RAM | 2 * （1 核 - 15GB RAM） | 20.3 | 12,600 |
| 8 核 - 30GB RAM | 4 * （1 核 - 15GB RAM） | 10.7 | 23,900 |

这些基准数据表明，Citus 的 UPDATE 吞吐量略低于 INSERT。这是因为 pgbench 会为 UPDATE 语句创建主键索引，而 UPDATE 在工作节点上需要执行更多工作。

UPDATE 语句会导致数据库膨胀，需要定期运行 VACUUM 进行清理。在 Citus 中，VACUUM 会跨工作节点并行运行，因此不太可能影响工作负载。

#### 插入和更新：吞吐量清单 {#insert-and-update-throughput-checklist}

在中等规模的 Citus 集群上运行前述 pgbench 基准测试时，通常可以达到每秒 10K–50K 次 INSERT，相当于每天约 10 亿至 40 亿次 INSERT。如果没有达到这一吞吐量，请检查以下事项：

- 检查应用程序与数据库之间的网络延迟。 高延迟会影响写入吞吐量。
- 使用并发线程引入数据。如果 INSERT 的往返延迟为 4 ms，单个线程每秒可以处理 250 次 INSERT；运行 100 个并发线程时，写入吞吐量会随线程数增加。
- 检查集群节点是否存在 CPU 或磁盘瓶颈。引入的数据会经过协调节点，因此要检查协调节点是否受 CPU 限制。
- 避免在 INSERT 语句之间关闭连接，这样也避免了连接设置的开销。
- 请记住，列大小会影响插入速度。 具有大型 JSON blob 的行处理时间比包含小列（如整数）的行耗时更长。

#### 插入和更新：延迟 {#insert-and-update-latency}

与批量 COPY 命令相比，执行 INSERT 或 UPDATE 的优势是其他查询可以立即看到变更。执行 INSERT 或 UPDATE 时，Citus 协调节点会将命令直接路由到相关工作节点；协调节点还会在同一会话中保持与工作节点的连接，因此后续命令的响应时间更短。

```psql
-- Set up a distributed table that keeps account history information
CREATE TABLE pgbench_history (tid int, bid int, aid int, delta int, mtime timestamp);
SELECT create_distributed_table('pgbench_history', 'aid');

-- Enable timing to see reponse times
\timing on

-- First INSERT requires connection set-up, second will be faster
INSERT INTO pgbench_history VALUES (10, 1, 10000, -5000, CURRENT_TIMESTAMP); -- Time: 10.314 ms
INSERT INTO pgbench_history VALUES (10, 1, 22000, 5000, CURRENT_TIMESTAMP); -- Time: 3.132 ms
```

### 临时暂存数据 {#stage-data-temporarily}

加载临时暂存数据时，可以考虑使用[未记录日志表](https://www.postgresql.org/docs/current/static/sql-createtable.html#SQL-CREATETABLE-UNLOGGED)。PostgreSQL 预写式日志不会记录未记录日志表，因此插入行的速度更快，但它不适合长期存储数据。可以先将传入数据加载到未记录日志表，处理后再移入永久表。

```sql
-- example unlogged table
CREATE UNLOGGED TABLE unlogged_table (
  key text,
  value text
);

-- its shards will be unlogged as well when
-- the table is distributed
SELECT create_distributed_table('unlogged_table', 'key');

-- ready to load data
```

### 批量 COPY（250K–2M/秒） {#bulk-copy-250k---2ms}

分布式表支持从 Citus 协调节点执行[COPY](http://www.postgresql.org/docs/current/static/sql-copy.html)进行批量引入，其引入速率可以高于 INSERT。

COPY 可以通过 `COPY .. FROM STDIN` 直接从应用程序加载数据，也可以从服务器上的文件或服务器上执行的程序加载。

```sql
COPY pgbench_history FROM STDIN WITH (FORMAT CSV);
```

在 psql 中，可以使用 `\COPY` 从本地计算机加载数据。`\COPY` 实际上会先向服务器发送 `COPY .. FROM STDIN`，然后再发送本地数据；直接加载数据的应用程序也会采用这种方式。

```bash
psql -c "\COPY pgbench_history FROM 'pgbench_history-2016-03-04.csv' (FORMAT CSV)"
```

分布式表使用 COPY 的一个强大功能是：它通过多个并行连接异步将数据复制到工作节点，每个分片放置对应一个连接。这样可以利用多个工作节点和多个 CPU 核心并行引入数据。尤其在存在 GIN 等昂贵索引时，与直接导入普通 PostgreSQL 表相比，这一功能可以带来显著的性能提升。

从吞吐量看，使用 COPY 时预计每秒可引入 250K–2M 行。更多信息请参阅 [向分布式 PostgreSQL 表执行 COPY，最高每秒 700 万行](https://www.citusdata.com/blog/2016/06/15/copy-postgresql-distributed-tables)。

> [!NOTE]
> 请确保基准测试环境配置正确，以便观察到最佳 COPY 性能。请遵循以下建议：
> 
> - 建议使用较大的批次（约 50000–100000 行）。可以使用多个文件（1、10、1000、10000 等）进行基准测试，每个文件包含相应大小的批次。
> - 使用并行数据引入。将线程数或引入器数增加到 2、4、8、16，然后运行基准测试。
> - 使用计算优化的协调节点。对于工作节点，选择拥有足够 vCPU 的内存优化型实例。
> - 使用相对较少的分片，32 个应已足够，也可以将 64 个作为对照进行基准测试。
> - 在适当的时间范围内引入数据（例如 2、4、8 或 24 小时）。更长的测试更能代表生产环境。

## 相关内容 {#related-content}

- [诊断查询](/citus/operations/diagnostic-queries/)
- [指南](/citus/articles/)
- [什么是 Citus？](/citus/overview/what-is-citus/)
