---
title: 配置 Citus：GUC 参数参考
description: 查阅影响 Citus 行为的专用配置参数和标准 PostgreSQL 参数。
weight: 40
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/api-guc?view=citus-14
upstream_ref: citus-14; a0636007e123
translation_status: translated
---

多种配置参数会影响 Citus 的行为，包括标准 PostgreSQL 参数和 Citus 专用参数。有关 PostgreSQL 配置参数，参见 PostgreSQL 文档的[运行时配置](http://www.postgresql.org/docs/current/static/runtime-config.html)部分。

本参考的其余部分介绍 Citus 专用配置参数。与 PostgreSQL 参数一样，可以修改 `postgresql.conf`，也可以[使用 SET 命令](http://www.postgresql.org/docs/current/static/config-setting.html)设置这些参数。

例如，可以使用以下命令更新设置：

```sql
ALTER DATABASE citus SET citus.multi_task_query_log_level = 'log';
```

## 通用配置 {#general-configuration}

### citus.max_background_task_executors_per_node （整数） {#citusmax_background_task_executors_per_node-integer}

控制同一时刻可以并行运行的后台任务数量，例如迁入或迁出节点的分片移动任务。提高此值时，也应考虑提高 `citus.max_background_task_executors` 和 [max_worker_processes](https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-MAX-WORKER-PROCESSES)。

- 默认值：1
- 最小值：1
- 最大值：128

### citus.max_worker_nodes_tracked （整数） {#citusmax_worker_nodes_tracked-integer}

Citus 在协调节点的共享哈希表中跟踪工作节点的位置和成员关系。此配置限制哈希表大小，从而限制可跟踪的工作节点数。默认值为 2,048。只能在服务器启动时设置，对协调节点生效。

### citus.use_secondary_nodes （枚举） {#citususe_secondary_nodes-enum}

设置为 `SELECT` 查询选择节点时采用的策略。如果设为 `always`，规划器只查询 `pg_dist_node` 中标记为备用节点的节点。

支持以下枚举值：

- **never**：（默认）所有读取都在主节点上执行。
- **always**：改为在备用节点上读取，并禁止插入和更新语句。

### citus.cluster_name （文本） {#cituscluster_name-text}

告知协调节点的规划器，它负责协调哪个集群。设置 `cluster_name` 后，规划器只查询该集群内的工作节点。

### citus.enable_version_checks （布尔值） {#citusenable_version_checks-boolean}

升级 Citus 需要重启服务器以加载新的共享库，并运行 `ALTER EXTENSION UPDATE` 命令。未完成这两个步骤可能导致错误或崩溃。因此，Citus 会检查代码版本与扩展版本是否匹配，不匹配时就报错。

默认值为 *true*，对协调节点生效。极少数情况下，复杂的升级流程可能需要将其设为 *false*，禁用此检查。

### citus.log_distributed_deadlock_detection （布尔值） {#cituslog_distributed_deadlock_detection-boolean}

是否在服务器日志中记录分布式死锁检测相关的处理过程。默认值为 false。

### citus.distributed_deadlock_detection_factor （浮点数） {#citusdistributed_deadlock_detection_factor-floating-point}

设置检查分布式死锁前的等待时间，该值乘以 PostgreSQL 的 [deadlock_timeout](https://www.postgresql.org/docs/current/static/runtime-config-locks.html) 才是实际等待时间。默认值为 *2*，设为 *-1* 可禁用分布式死锁检测。

### citus.node_connection_timeout （整数） {#citusnode_connection_timeout-integer}

全局用户配置（GUC）`citus.node_connection_timeout` 设置等待连接建立的最长时间，单位为毫秒。如果超时前连一个工作节点连接都未能建立，Citus 就会报错。它影响协调节点到工作节点，以及工作节点之间的连接。

- 默认值：30 秒
- 最小值：10 毫秒
- 最大值：1 小时

```sql
-- set to 60 seconds
ALTER DATABASE foo
SET citus.node_connection_timeout = 60000;
```

### citus.node_conninfo （文本） {#citusnode_conninfo-text}

`citus.node_conninfo` 为所有节点间连接设置非敏感的 [libpq 连接参数](https://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-PARAMKEYWORDS)。

```sql
-- key=value pairs separated by spaces.
-- For example, ssl options:

ALTER DATABASE foo
SET citus.node_conninfo =
  'sslrootcert=/path/to/citus.crt sslmode=verify-full';
```

Citus 仅采用允许选项中的以下子集：

- connect_timeout
- gsslib†
- host
- keepalives
- keepalives_count
- keepalives_idle
- keepalives_interval
- krbsrvname†
- sslcompression
- sslcrl
- sslmode（从 Citus 8.1 开始默认为 "require"）
- sslnegotiation
- sslrootcert
- tcp_user_timeout

*（† 表示取决于运行时是否具备可选的 PostgreSQL 功能。）*

`node_conninfo` 设置仅影响新建立的连接。要强制所有连接使用新设置，请务必重新加载 PostgreSQL 配置：

```sql
SELECT pg_reload_conf();
```

> [!WARNING]
> Citus 9.2.4 之前的版本需要完整重启数据库，才能强制所有连接使用新设置。

### citus.local_hostname （文本） {#cituslocal_hostname-text}

Citus 节点有时需要连接自身来执行系统操作。例如在 MX 模式下，节点作为客户端查询入口，需要在本地执行分片查询片段。默认使用 `localhost` 连接自身，但这个地址可能造成问题。例如，主机要求入站连接使用 `sslmode=verify-full` 时，将 `localhost` 添加为 SSL 证书的备用主机名并不总是合适或可行。

`citus.local_hostname` 指定节点连接自身所用的主机名。默认值为 *localhost*。

```sql
ALTER SYSTEM SET citus.local_hostname TO 'mynode.example.com';
```

### citus.show_shards_for_app_name_prefixes （文本） {#citusshow_shards_for_app_name_prefixes-text}

默认情况下，Citus 会在 PostgreSQL 提供给 SQL 客户端的表列表中隐藏分片，因为每个分布式表有多个分片，全部显示可能干扰客户端使用。

`citus.show_shards_for_app_name_prefixes` 允许为需要查看分片的指定客户端显示分片。默认值为 `''`。

```psql
-- show shards to psql only (hide in other clients, like pgAdmin)

SET citus.show_shards_for_app_name_prefixes TO 'psql';

-- also accepts a comma separated list

SET citus.show_shards_for_app_name_prefixes TO 'psql,pg_dump';
```

### citus.rebalancer_by_disk_size_base_cost （整数） {#citusrebalancer_by_disk_size_base_cost-integer}

使用 by_disk_size 再平衡策略时，会在每个分片组的实际磁盘大小上加上此项指定的代价，单位为字节。这可避免某些分片数据很少时产生不合理的平衡结果。其假设是：即使空分片也有一定代价，因为要考虑并行性，而且空分片组未来很可能增长。

默认值为 `100MB`。

### citus.shard_transfer_mode （枚举） {#citusshard_transfer_mode-enum}

控制移动分片和分布式模式的默认方法，供分片再平衡、`citus_move_shard_placement`、`rebalance_table_shards` 和 `citus_schema_move` 使用。可用时使用逻辑复制以避免阻塞写入，否则回退到阻塞复制。

可选值：

- **auto**（默认）：存在副本标识时使用逻辑复制，否则回退到旧行为，即阻塞写入并使用 COPY。
- **force_logical**：即使表没有副本标识，也强制使用逻辑复制。复制期间，这些表上的并发 UPDATE/DELETE 会失败。
- **block_writes**：始终使用 COPY；对于缺少主键或副本标识的表，阻塞其写入。

此 GUC 对协调节点生效，用于设置集群数据移动操作的默认方式。

```sql
-- force logical replication for shard moves
SET citus.shard_transfer_mode = 'force_logical';
SELECT rebalance_table_shards('orders');
```

## 查询统计 {#query-statistics}

### citus.stat_statements_purge_interval （整数） {#citusstat_statements_purge_interval-integer}

> [!NOTE]
> 从 11.0 版本开始，此 GUC 属于 Citus 社区版。

设置维护守护进程清理 `citus_stat_statements` 的频率：删除其中在 `pg_stat_statements` 中没有匹配记录的条目。清理间隔以秒为单位，默认值为 *10*，设为 *0* 可禁用清理。

```psql
SET citus.stat_statements_purge_interval TO 5;
```

此参数对协调节点生效，可以在运行时修改。

### citus.stat_statements_max （整数） {#citusstat_statements_max-integer}

> [!NOTE]
> 从 11.0 版本开始，此 GUC 属于 Citus 社区版。

设置 `citus_stat_statements` 中存储的最大行数，默认值为 *50000*，可设置为 *1000* 至 *10000000* 之间的任意值。每行需要 140 字节，因此将 `stat_statements_max` 设为最大值 1000 万时会占用 1.4 GB 内存。

修改后需要重启 PostgreSQL 才能生效。

### citus.stat_statements_track （枚举） {#citusstat_statements_track-enum}

> [!NOTE]
> 从 11.0 版本开始，此 GUC 属于 Citus 社区版。

记录 `citus_stat_statements` 统计信息需要额外 CPU 资源。数据库负载较高时，管理员可能希望关闭语句跟踪。`citus.stat_statements_track` 控制跟踪的开启与关闭。

- **all**：跟踪所有语句。
- **none**：（默认）禁用跟踪。

### citus.stat_tenants_untracked_sample_rate （浮点数） {#citusstat_tenants_untracked_sample_rate-floating-point}

设置 `citus_stat_tenants` 对新租户的采样率，取值范围为 *0.0* 到 *1.0*，默认值为 *1.0*，即对未跟踪租户的查询进行 100% 采样。设置较低值后，尚未跟踪的租户按指定比例采样，已经跟踪的租户仍然对全部查询采样。

### citus.enable_stat_counters （布尔值） {#citusenable_stat_counters-boolean}

启用后，Citus 收集连接和查询执行计数器。可以通过 `citus_stat_counters` 视图和 `citus_stat_counters()` 函数查询，并使用 `citus_stat_counters_reset()` 重置。

> [!IMPORTANT]
> - 默认值：**false**（禁用）。
> - 只有超级用户可以修改。
> - 计数器不持久化，服务器重启后会重置。
> - 禁用后停止采集，但已有计数器仍可查询。

```sql
-- enable stat counters collection
ALTER SYSTEM SET citus.enable_stat_counters = true;
SELECT pg_reload_conf();
```

## 数据加载 {#data-loading}

### citus.multi_shard_commit_protocol （枚举） {#citusmulti_shard_commit_protocol-enum}

设置对哈希分布表执行 COPY 时采用的提交协议。每个分片放置上的 COPY 都在事务块中执行，确保 COPY 出错时不会导入数据。不过，存在一种特殊故障：所有放置上的 COPY 均成功，但在所有事务提交前发生了硬件故障。可以通过此参数选择以下提交协议，以防止这种情况下的数据丢失：

- **2pc**：（默认）各分片放置上复制数据的事务先执行 PostgreSQL [两阶段提交](http://www.postgresql.org/docs/current/static/sql-prepare-transaction.html)的准备阶段，再提交。提交失败时，可以分别使用 COMMIT PREPARED 或 ROLLBACK PREPARED 手动恢复或中止。使用 `2pc` 时，应提高所有工作节点上的 [max_prepared_transactions](http://www.postgresql.org/docs/current/static/runtime-config-resource.html)，通常设为与 max_connections 相同。
- **1pc**：各分片放置上复制数据的事务在一轮内提交。如果所有放置的 COPY 成功后提交失败，可能丢失数据，这种情况很少发生。

### citus.shard_count （整数） {#citusshard_count-integer}

设置哈希分区表的分片数，默认值为 *32*。用户定义函数 [create_distributed_table](/citus/reference/api-udf/#create_distributed_table) 在创建哈希分区表时采用此值。可在运行时设置，对协调节点生效。

### citus.replicate_reference_tables_on_activate （布尔值） {#citusreplicate_reference_tables_on_activate-boolean}

所有包含分布式表的节点都必须存放参考表分片。默认情况下，系统在激活节点时（即调用 `citus_add_node` 或 `citus_activate_node` 等函数时）将参考表分片复制过去。但如果参考表很大，复制耗时可能很长，节点激活时未必适合执行复制。

将 `citus.replicate_reference_tables_on_activate` 设为 `off` 可以推迟参考表复制。此时，系统在该节点创建新分片时才复制参考表，例如调用 `create_distributed_table`、`create_reference_table`，或分片再平衡器将分片移动到新节点时。

此 GUC 的默认值为 *on*。

### citus.metadata_sync_mode （枚举） {#citusmetadata_sync_mode-enum}

> [!NOTE]
> 只有超级用户可以修改。

此 GUC 决定 Citus 如何跨节点同步元数据。为使 MX 模式下任意节点都能规划和路由查询，Citus 必须保持各节点的元数据最新。默认在一个事务中更新全部元数据以确保一致性。不过，PostgreSQL 对缓存失效处理有硬性内存限制，大集群的 Citus 元数据同步可能因内存耗尽而失败。

为此，Citus 提供可选的非事务同步模式，通过一系列小事务完成同步。这种方式可以在有限内存下工作，但事务可能失败，导致元数据不一致。为缓解这一问题，非事务元数据同步被设计为幂等操作，必要时可以反复重试。

此 GUC 有两个取值：

- **transactional**：（默认）在一个事务中同步所有元数据。
- **nontransactional**：使用多个小事务同步元数据。

示例：

```sql
-- to add a new node and sync nontransactionally

SET citus.metadata_sync_mode TO 'nontransactional';
SELECT citus_add_node(<ip>, <port>);

-- to manually (re)sync

SET citus.metadata_sync_mode TO 'nontransactional';
SELECT start_metadata_sync_to_all_nodes();
```

建议先尝试事务模式，仅在发生内存不足错误时再切换到非事务模式。

## 规划器配置 {#planner-configuration}

### citus.enable_local_fast_path_query_optimization （布尔值） {#citusenable_local_fast_path_query_optimization-boolean}

为本地单分片路由查询启用延迟快速路径规划优化。启用后，Citus 在识别分片后才构建快速路径占位计划。如果接收节点已经持有目标分片（MX 模式），Citus 就使用分片 OID 重新规划并复用缓存计划，省去反解析、解析和规划的开销。完整行为参见[延迟快速路径规划](/citus/reference/reference-processing/#delayed-fast-path-planning-citus-132)。

- 默认值：true

### citus.enable_recurring_outer_join_pushdown （布尔值） {#citusenable_recurring_outer_join_pushdown-boolean}

控制 Citus 是否在参考表或中间结果上注入分片区间约束，将符合条件的 LEFT/RIGHT 外连接（重复关系外连接）下推到工作节点。Citus 13.2 默认启用。若希望强制这类连接在协调节点执行，可以禁用。

- 默认值：true

### citus.local_table_join_policy （枚举） {#cituslocal_table_join_policy-enum}

此 GUC 决定连接本地表与分布式表时如何移动数据。调整连接策略有助于减少工作节点之间的数据传输量。

为执行连接，Citus 会按需将本地表或分布式表的数据发送到相应节点。这种表数据复制称为*转换*。转换本地表时，规划器将其发送给需要这些数据执行连接的工作节点；转换分布式表时，则由协调节点收集数据并用于连接。转换期间只传输必要的行。

有四种模式来表达转换偏好：

- **auto**：（默认）Citus 选择转换所有本地表或所有分布式表，以支持两者之间的连接。它使用启发式规则：如果连接中的分布式表具有基于唯一索引（如主键）的常量过滤条件，就转换分布式表，以减少工作节点之间的数据移动。
- **never**：禁止本地表与分布式表之间的连接。
- **prefer-local**：优先转换本地表。
- **prefer-distributed**：优先转换分布式表。如果分布式表很大，可能导致工作节点之间移动大量数据。

例如，假设 `citus_table` 是按 `x` 列分布的分布式表，`postgres_table` 是本地表：

```sql
CREATE TABLE citus_table(x int primary key, y int);
SELECT create_distributed_table('citus_table', 'x');

CREATE TABLE postgres_table(x int, y int);

-- even though the join is on primary key, there isn't a constant filter
-- hence postgres_table will be sent to worker nodes to support the join
SELECT * FROM citus_table JOIN postgres_table USING (x);

-- there is a constant filter on a primary key, hence the filtered row
-- from the distributed table will be pulled to coordinator to support the join
SELECT * FROM citus_table JOIN postgres_table USING (x) WHERE citus_table.x = 10;

SET citus.local_table_join_policy to 'prefer-distributed';
-- since we prefer distributed tables, citus_table will be pulled to coordinator
-- to support the join. Note that citus_table can be huge.
SELECT * FROM citus_table JOIN postgres_table USING (x);

SET citus.local_table_join_policy to 'prefer-local';
-- even though there is a constant filter on primary key for citus_table
-- postgres_table will be sent to necessary workers because we are using 'prefer-local'.
SELECT * FROM citus_table JOIN postgres_table USING (x) WHERE citus_table.x = 10;
```

### citus.limit_clause_row_fetch_count （整数） {#cituslimit_clause_row_fetch_count-integer}

设置 LIMIT 子句优化时每个任务提取的行数。有些带 LIMIT 的 SELECT 查询需要从各任务提取全部行才能生成结果。如果近似结果具有实际意义，可以用此配置指定从每个分片提取的行数。LIMIT 近似计算默认禁用，此参数默认设为 *-1*。可在运行时设置，对协调节点生效。

### citus.count_distinct_error_rate （浮点数） {#cituscount_distinct_error_rate-floating-point}

Citus 可以通过 postgresql-hll 扩展近似计算 count(distinct)。此配置指定期望的误差率。默认值 *0.0* 禁用近似计算；*1.0* 不提供任何结果精度保证。建议设为 *0.005* 以获得最佳效果。可在运行时设置，对协调节点生效。

### citus.task_assignment_policy （枚举） {#citustask_assignment_policy-enum}

> [!NOTE]
> 此 GUC 适用于针对[参考表](/citus/reference/reference-ddl/#reference-tables)的查询。

设置向工作节点分配任务的策略。协调节点根据分片位置分配任务，此参数决定分配方式。目前支持三种策略。

- **greedy**：默认的贪心策略，目标是将任务均匀分配到各工作节点。
- **round-robin**：轮询策略，在不同副本间轮流分配任务。当表的分片数相对工作节点数较少时，可以提高集群利用率。
- **first-replica**：按照分片放置（副本）的插入顺序分配任务，即将某分片的查询片段交给持有其第一个副本的工作节点。这可以明确保证哪些节点使用哪些分片，从而更有力地保证数据驻留内存。

可在运行时设置，对协调节点生效。

### enable_non_colocated_router_query_pushdown （布尔值） {#enable_non_colocated_router_query_pushdown-boolean}

为引用非共置分布式表的查询启用路由规划器。

通常只有引用共置分布式表的查询才启用路由规划器，因为非共置表的目标分片不保证始终位于同一节点，例如分片再平衡后就可能分离。因此，启用此选项虽然能优化部分非共置表查询，却不能保证在分片再平衡或修改其中某个表的分片数后，同样的查询仍能工作。

默认值为 `off`。

## 中间数据传输 {#intermediate-data-transfer}

### citus.binary_worker_copy_format （布尔值） {#citusbinary_worker_copy_format-boolean}

使用二进制 COPY 格式在工作节点之间传输中间数据。连接大型表时，Citus 可能需要动态重新分区，并在工作节点之间重新分发数据。PostgreSQL 13 及更早版本默认值为 `false`，即使用文本编码传输；PostgreSQL 14 及更高版本默认值为 `true`。设为 `true` 后，数据库采用 PostgreSQL 二进制序列化格式。该参数对工作节点生效，需在 postgresql.conf 中修改。编辑配置后发送 SIGHUP 信号或重启服务器即可生效。

### citus.max_intermediate_result_size （整数） {#citusmax_intermediate_result_size-integer}

设置无法下推到工作节点执行的公共表表达式（CTE）及复杂子查询的中间结果大小上限，单位为 KB。默认值为 1 GB，*-1* 表示不限大小。超出上限的查询会被取消并报错。

## 数据定义语言（DDL） {#data-definition-language-ddl}

### citus.enable_ddl_propagation （布尔值） {#citusenable_ddl_propagation-boolean}

控制是否自动将 DDL 修改从协调节点传播到所有工作节点，默认值为 *true*。某些模式修改需要获取表上的访问排他锁，而自动传播会依次作用于所有工作节点，因此可能暂时降低集群的响应能力。可以选择禁用此设置，改为手动传播修改。

> [!NOTE]
> 支持传播的 DDL 列表参见 [DDL 参考](/citus/reference/reference-ddl/)。

### citus.enable_local_reference_table_foreign_keys （布尔值） {#citusenable_local_reference_table_foreign_keys-boolean}

此设置默认启用，允许在参考表和本地表之间创建外键。要使用该功能，必须通过 `citus_add_node` 将协调节点注册到自身。

参考表和本地表之间的外键有少量开销。创建外键时，Citus 必须将普通表加入元数据，并在 `partition_table` 中跟踪。加入元数据的本地表具有与参考表相同的限制（参见 `ddl` 和 `citus_sql_reference`）。

删除外键后，Citus 会自动从元数据中移除这类本地表，解除这些限制。

### citus.enable_change_data_capture （布尔值） {#citusenable_change_data_capture-boolean}

此设置默认禁用。启用后，Citus 会调整 `wal2json` 和 `pgoutput` 逻辑解码器，使其适用于分布式表：将解码器输出中的分片名（例如 `foo_102027`）改写为分布式表的基础名称（例如 `foo`），并避免在租户隔离及分片拆分、移动、再平衡期间发布重复事件。

使用示例参见 `cdc`。

### citus.enable_schema_based_sharding （布尔值） {#citusenable_schema_based_sharding-boolean}

设为 `ON` 后，所有新建模式默认都是分布式模式。每个分布式模式会自动关联一个独立的共置组，因此其中新建的表无需分片键，就会自动成为共置分布式表。可以为单个会话修改此设置。

使用示例参见 `microservices_tutorial`。

## 执行器配置 {#executor-configuration}

### 通用配置 {#general}

#### citus.all_modifications_commutative {#citusall_modifications_commutative}

Citus 遵循操作可交换性规则，为修改操作获取适当的锁以保证正确性。例如，它假定两个 INSERT 语句可交换执行顺序，但 INSERT 与 UPDATE 或 DELETE 不可交换；两个 UPDATE 或 DELETE 也被视为不可交换。因此，UPDATE 和 DELETE 要求 Citus 获取更强的锁。

如果 UPDATE 与 INSERT 或其他 UPDATE 可以交换执行顺序，可以将此参数设为 true，放宽这些假设。此时所有命令都视为可交换，仅获取共享锁，可能提高整体吞吐量。可在运行时设置，对协调节点生效。

#### citus.multi_task_query_log_level （枚举） {#citusmulti_task_query_log_level-enum}

为生成多个任务（即涉及多个分片）的查询设置日志级别。在迁移多租户应用时很有用：可以对这类查询报错或警告，以找出它们并添加 tenant_id 过滤条件。可在运行时设置，对协调节点生效。默认值为 *off*。

支持以下枚举值：

- **off**：不记录生成多个任务（跨多个分片）的查询。
- **debug**：以 DEBUG 级别记录语句。
- **log**：以 LOG 级别记录语句，日志中包含执行的 SQL 查询。
- **notice**：以 NOTICE 级别记录语句。
- **warning**：以 WARNING 级别记录语句。
- **error**：以 ERROR 级别记录语句。

开发测试时可以使用 `error`，生产部署时使用较低级别，例如 `log`。选择 `log` 后，多任务查询会出现在数据库日志中，查询文本显示在“STATEMENT”之后。

```text
LOG:  multi-task query about to be executed
HINT:  Queries are split to multiple tasks if they have to be split into several queries on the workers.
STATEMENT:  select * from foo;
```

#### citus.propagate_set_commands （枚举） {#cituspropagate_set_commands-enum}

决定协调节点向工作节点传播哪些 SET 命令。默认值为 *none*。

支持以下值：

- **none**：不传播任何 SET 命令。
- **local**：只传播 SET LOCAL 命令。

#### citus.enable_repartition_joins （布尔值） {#citusenable_repartition_joins-boolean}

通常，尝试使用自适应执行器执行[重分区连接](/citus/reference/reference-sql/#repartition-joins)会报错。但将 `citus.enable_repartition_joins` 设为 *true* 后，Citus 就允许执行这种连接。默认值为 *false*。

#### citus.enable_repartitioned_insert_select （布尔值） {#citusenable_repartitioned_insert_select-boolean}

默认情况下，无法下推的 `INSERT INTO ... SELECT` 会尝试对 SELECT 结果行重新分区，并在工作节点之间传输，以完成插入。但目标表分片过多时，这种方式可能性能不佳，因为确定结果分区方式时处理分片区间的开销太大。可以将 `citus.enable_repartitioned_insert_select` 设为 *false*，手动禁用重新分区。

#### citus.enable_binary_protocol （布尔值） {#citusenable_binary_protocol-boolean}

设为 true 后，协调节点在适用时使用 PostgreSQL 二进制序列化格式与工作节点交换数据。部分列类型不支持二进制序列化。

工作节点需要返回大量数据时，此参数尤其有用，例如返回行数很多、每行列数很多，或使用 postgresql-hll 扩展的 `hll` 等大型类型。

默认值为 *true*。设为 *false* 时，所有结果都以文本格式编码和传输。

#### citus.max_shared_pool_size （整数） {#citusmax_shared_pool_size-integer}

设置协调节点所有并发会话对每个**远程**节点可建立的连接总数上限。PostgreSQL 需要为每个连接分配固定资源，此 GUC 有助于缓解远程节点的连接压力。

若不限流，每个多分片查询在各远程节点建立的连接数与访问的分片数成正比，最多可达分片数/工作节点数。同时运行数十个多分片查询，很容易触及远程节点的 `max_connections` 上限而导致查询失败。

默认自动设为协调节点自身的 `max_connections`，但不保证与远程节点的设置相同，参见下面的说明。设为 *-1* 可禁用限流。

> [!NOTE]
> 部分操作不遵守 `citus.max_shared_pool_size`，其中最重要的是重分区连接。因此，可将远程节点的 `max_connections` 设得略高于协调节点的 `max_connections`，为工作节点执行重分区查询所需的连接预留空间。

#### citus.local_shared_pool_size （整数） {#cituslocal_shared_pool_size-integer}

设置协调节点所有并发会话对**本地**节点可建立的连接总数上限。本地节点持有分片时，此设置才相关，例如[单节点 Citus](/citus/installation/single-node/)。

默认自动设为该节点自身 `max_connections` 的一半，为客户端后端（如 `psql` 或应用连接）预留空间，避免内部 Citus 连接占满全部槽位。设为 *-1* 可禁用限流。

此 GUC 与 `citus.max_shared_pool_size` 提供类似的限流功能，但只针对本地节点。

#### citus.max_adaptive_executor_pool_size （整数） {#citusmax_adaptive_executor_pool_size-integer}

`max_shared_pool_size` 限制所有会话到工作节点的连接数，而 `max_adaptive_executor_pool_size` 仅限制*当前*会话的连接数。此 GUC 可用于：

- 防止单个后端占用全部工作节点资源。
- 实现优先级管理：为低优先级会话设置较小的 `max_adaptive_executor_pool_size`，高优先级会话则使用较大值。

默认值为 *16*。

#### citus.executor_slow_start_interval （整数） {#citusexecutor_slow_start_interval-integer}

设置向同一工作节点建立连接之间的等待时间，单位为毫秒。

如果多分片查询的各个任务耗时很短，通常一个连接就能完成，且该连接往往已经缓存。为避免多余的连接，执行器会在尝试建立连接之间等待指定毫秒数。间隔结束后，再增加允许打开的连接数量。

对于超过 500 ms 的长查询，慢启动可能增加延迟；对于短查询，则更快。默认值为 *10 ms*。

#### citus.max_cached_conns_per_worker （整数） {#citusmax_cached_conns_per_worker-integer}

每个后端都会连接工作节点以查询分片。事务结束后，会保留配置数量的连接，以加快后续命令。提高此值可以降低多分片查询延迟，但也会增加工作节点的开销。

默认值为 *1*。并发会话较少的集群可以考虑较大值，例如 *2*，但不宜过高，例如 *16* 就过大了。

#### citus.force_max_query_parallelization （布尔值） {#citusforce_max_query_parallelization-boolean}

模拟已弃用且现已移除的实时执行器。此设置尽可能打开更多连接，以最大化查询并行度。

启用后，Citus 强制自适应执行器在并行分布式查询中使用尽可能多的连接。否则，执行器可能选择较少连接，以优化整体查询吞吐量。在内部，将其设为 *true* 会为每个任务使用一个连接。

如果事务的首个查询很轻量、只需少量连接，而后续查询需要更多连接，此设置就很有用。Citus 根据首条语句决定事务使用的连接数，如果不用此 GUC 提示，就可能限制后续查询。

```sql
BEGIN;
-- add this hint
SET citus.force_max_query_parallelization TO ON;

-- a lightweight query that doesn't require many connections
SELECT count(*) FROM table WHERE filter = x;

-- a query that benefits from more connections, and can obtain
-- them since we forced max parallelization above
SELECT ... very .. complex .. SQL;
COMMIT;
```

默认值为 *false*。

### EXPLAIN 输出 {#explain-output}

#### citus.explain_all_tasks （布尔值） {#citusexplain_all_tasks-boolean}

对分布式查询运行 [EXPLAIN](http://www.postgresql.org/docs/current/static/sql-explain.html) 时，Citus 默认只显示任意一个任务的输出。大多数情况下，各任务的 EXPLAIN 输出相似，但有时某些任务的计划不同，或执行时间明显更长。这时可以启用此参数，让 EXPLAIN 输出包含所有任务，不过 EXPLAIN 的执行时间可能因此延长。

#### citus.explain_analyze_sort_method （枚举） {#citusexplain_analyze_sort_method-enum}

决定 EXPLAIN ANALYZE 输出中任务的排序方式。`citus.explain_analyze_sort_method` 默认值为 `execution-time`。

支持以下值：

- **execution-time**：按执行时间排序。
- **taskId**：按任务 ID 排序。

## 相关内容 {#related-content}

- [用户定义函数](/citus/reference/api-udf/)
- [元数据表和视图](/citus/reference/api-metadata/)
- [什么是 Azure Cosmos DB for PostgreSQL？](/citus/overview/what-is-citus/)
