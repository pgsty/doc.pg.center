---
title: "配置参数"
description: "本文按字母顺序列出 Apache Cloudberry 数据库的配置参数（GUC）。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/config-params-guc-list.md"
---

## autovacuum_freeze_max_age {#autovacuum_freeze_max_age}

- 变量类型：整数
- 默认值：200000000
- 取值范围：[100000,2000000000]
- 设置类别：postmaster
- 描述：设置表中事务 ID 的“最大年龄”。自事务 ID 分配以来累积的事务数达到该值时，系统会自动对表执行 autovacuum，以防止事务 ID 回卷。即使禁用了 autovacuum，也会强制执行该操作，以确保数据安全。

## autovacuum_vacuum_cost_delay {#autovacuum_vacuum_cost_delay}

- 变量类型：实数
- 默认值：2
- 单位：ms
- 取值范围：[-1,100]
- 设置类别：sighup
- 描述：设置 autovacuum 操作的 vacuum 代价延迟时间，单位为毫秒。

## autovacuum_vacuum_scale_factor {#autovacuum_vacuum_scale_factor}

- 变量类型：实数
- 默认值：0.2
- 取值范围：[0,100]
- 设置类别：sighup
- 描述：控制执行 autovacuum 前，已更新或已删除元组数占总元组数的阈值比例。

## autovacuum_vacuum_threshold {#autovacuum_vacuum_threshold}

- 变量类型：整数
- 默认值：50
- 取值范围：[0,2147483647]
- 设置类别：sighup
- 描述：控制触发 autovacuum 所需的已更新或已删除元组的最小数量。

## checkpoint_timeout {#checkpoint_timeout}

- 取值范围：30 - 86400（整数，单位为秒）
- 默认值：300（5 分钟）
- 设置类别：local, system, reload
- 描述：指定自动 WAL 检查点之间的最大时间间隔。

  设置此参数时如果未指定单位，系统默认以秒为单位。允许的范围为 30 秒至 1 天。默认值为 5 分钟（300 秒或 5min）。增大此参数的值会增加崩溃恢复所需的时间。

## gp_appendonly_compaction_segfile_limit {#gp_appendonly_compaction_segfile_limit}

- 变量类型：整数
- 默认值：10
- 取值范围：[0,127]
- 设置类别：user
- 描述：设置必须为插入操作保留的仅追加存储段文件（segfile）的最小数量。

## gp_autostats_lock_wait {#gp_autostats_lock_wait}

- 变量类型：布尔值
- 默认值：off
- 设置类别：user
- 描述：控制 autostats 自动生成的 `ANALYZE` 是否等待获取锁。

## gp_command_count {#gp_command_count}

- 变量类型：整数
- 默认值：0
- 取值范围：[0,2147483647]
- 设置类别：internal
- 描述：显示客户端在当前会话中发送的命令数。

## gp_dynamic_partition_pruning {#gp_dynamic_partition_pruning}

- 参数类型：布尔值
- 默认值：on
- 设置类别：coordinator, session, reload
- 描述：启用能够动态排除分区扫描的执行计划。

## gp_enable_runtime_filter_pushdown {#gp_enable_runtime_filter_pushdown}

- 取值范围：布尔值
- 默认值：off
- 设置类别：user
- 描述：尝试将哈希连接的哈希表作为布隆过滤器下推到顺序扫描或访问方法（AM）。

## gp_enable_statement_trigger {#gp_enable_statement_trigger}

- 变量类型：布尔值
- 默认值：off
- 设置类别：user
- 描述：允许创建语句级触发器。

## gp_max_partition_level {#gp_max_partition_level}

- 变量类型：整数
- 默认值：0
- 取值范围：[0,2147483647]
- 设置类别：superuser
- 描述：设置使用经典语法创建分区表时允许的最大分区层级。

## gp_resource_manager {#gp_resource_manager}

- 取值范围：none, group, group-v2, queue
- 默认值：none
- 设置类别：local, system, restart
- 描述：指定 Apache Cloudberry 数据库集群当前启用的资源管理方案。
    - `none`：不使用资源管理器（默认）。
    - `group`：使用资源组，并启用基于 Linux cgroup v1 功能的资源组行为。
   - `group-v2`：使用资源组，并启用基于 Linux cgroup v2 功能的资源组行为。
    - `queue`：使用资源队列进行资源管理。

## gp_role {#gp_role}

- 取值范围：dispatch, execute, utility
- 默认值：未定义（取决于进程类型）
- 设置类别：只读（在后台自动设置）
- 描述：此参数用于标识当前服务器进程的角色。

    Coordinator 进程的角色为 `dispatch`，表示负责查询分发。Segment 进程的角色为 `execute`，表示负责执行查询计划。`utility` 用于特殊的维护或管理会话。此参数由系统在后台自动设置，主要用于区分不同类型的内部工作进程。

## gp_session_id {#gp_session_id}

- 变量类型：整数
- 默认值：-1
- 取值范围：[-2147483648,2147483647]
- 设置类别：backend
- 描述：用于唯一标识 Apache Cloudberry 集群中的一个会话。

## krb_server_keyfile {#krb_server_keyfile}

- 变量类型：字符串
- 默认值：`<FILE:/workspace/dist/database/etc/postgresql/krb5.keytab>`
- 设置类别：sighup
- 描述：设置 Kerberos 服务器密钥文件的位置。

## log_checkpoints {#log_checkpoints}

- 取值范围：布尔值
- 默认值：on
- 设置类别：local, system, reload
- 描述：将检查点和重启点信息写入服务器日志。日志消息包含写入的缓冲区数量、写入耗时等统计信息。

## max_connections {#max_connections}

- 取值范围：10 - 262143
- 默认值：Coordinator 上为 250，Segment 上为 750
- 设置类别：local, system, restart
- 描述：数据库服务器允许的最大并发连接数。

    在 Apache Cloudberry 系统中，客户端连接只能通过 Coordinator 实例接入。Segment 实例允许的连接数应为 Coordinator 的 3 至 10 倍。增大此参数的值时，必须相应增大 `max_prepared_transactions` 的值。

    此参数值越大，Apache Cloudberry 所需的共享内存就越多。

## max_replication_slots {#max_replication_slots}

- 变量类型：整数
- 默认值：10
- 取值范围：[0,262143]
- 设置类别：postmaster
- 描述：设置可以同时定义的最大复制槽数量。

## optimizer_array_constraints {#optimizer_array_constraints}

- 变量类型：布尔值
- 默认值：on
- 设置类别：user
- 描述：允许优化器的约束推导框架识别数组类型的约束。

## optimizer_array_expansion_threshold {#optimizer_array_expansion_threshold}

- 取值范围：大于 `0` 的整数
- 默认值：20
- 设置类别：coordinator, session, reload
- 描述：启用 GPORCA（默认）并执行包含常量数组谓词的查询时，`optimizer_array_expansion_threshold` 参数根据数组中的常量数量限制优化过程。

    如果查询谓词中的数组元素数量超过此参数指定的值，GPORCA 在查询优化时就不会将该谓词转换为析取范式，从而减少优化时间和内存消耗。例如，当 GPORCA 处理包含超过 20 个元素的 `IN` 子句的查询时，为保证优化性能，它不会将该子句转换为析取范式。可以通过执行计划中对 `IN` 条件的过滤方式观察到这一行为差异。

    修改此参数的值会影响优化时间、内存用量与约束推导所带来的优化收益（例如冲突检测和分区剪枝）之间的权衡。此参数可以在数据库系统级别、单个数据库级别，或会话和查询级别设置。

## optimizer_cost_model {#optimizer_cost_model}

- 变量类型：枚举
- 默认值：calibrated
- 设置类别：user
- 描述：设置优化器使用的代价模型。

## optimizer_cost_threshold {#optimizer_cost_threshold}

- 变量类型：实数
- 默认值：0
- 取值范围：[0,2.15E+09]
- 设置类别：user
- 描述：设置与最优执行计划代价相关的采样阈值，其中 0 表示无上限。

## optimizer_cte_inlining_bound {#optimizer_cte_inlining_bound}

- 变量类型：整数
- 默认值：0
- 取值范围：[0,2147483647]
- 设置类别：user
- 描述：设置优化器决定是否内联 CTE（公共表表达式）时使用的大小边界。

## optimizer_damping_factor_filter {#optimizer_damping_factor_filter}

- 变量类型：实数
- 默认值：0.75
- 取值范围：[0,1]
- 设置类别：user
- 描述：设置优化器用于选择谓词的阻尼因子，其中 `1.0` 表示无阻尼。

## optimizer_damping_factor_groupby {#optimizer_damping_factor_groupby}

- 变量类型：实数
- 默认值：0.75
- 取值范围：[0,1]
- 设置类别：user
- 描述：设置优化器用于 `group by` 操作的阻尼因子，其中 `1.0` 表示无阻尼。

## optimizer_damping_factor_join {#optimizer_damping_factor_join}

- 变量类型：实数
- 默认值：0
- 取值范围：[0,1]
- 设置类别：user
- 描述：设置用于连接谓词的阻尼因子，其中 `1.0` 表示无阻尼，`0.0` 表示使用平方根阻尼。

## optimizer_discard_redistribute_hashjoin {#optimizer_discard_redistribute_hashjoin}

- 变量类型：布尔值
- 默认值：off
- 设置类别：user
- 描述：控制优化器是否丢弃包含重分布操作的哈希连接计划。

## optimizer_dpe_stats {#optimizer_dpe_stats}

- 变量类型：布尔值
- 默认值：on
- 设置类别：user
- 描述：在动态分区消除场景中，启用对分区表的统计信息推导。

## optimizer_enable_derive_stats_all_groups {#optimizer_enable_derive_stats_all_groups}

- 变量类型：布尔值
- 默认值：off
- 设置类别：user
- 描述：在完成搜索空间探索后，启用对所有组的统计信息推导。

## optimizer_enable_dynamicbitmapscan {#optimizer_enable_dynamicbitmapscan}

- 取值范围：布尔值
- 默认值：on
- 设置类别：user
- 描述：启用后，优化器使用动态位图扫描计划。

    如果此参数设为 `off`，GPORCA 就不会生成动态位图扫描计划，而是退回使用动态顺序扫描作为替代。

## optimizer_enable_dynamicindexonlyscan {#optimizer_enable_dynamicindexonlyscan}

- 参数类型：布尔值
- 默认值：on
- 设置类别：coordinator, session, reload
- 描述：启用 GPORCA（默认）时，`optimizer_enable_dynamicindexonlyscan` 参数控制是否生成动态仅索引扫描计划。

    默认值为 `on`。在规划针对分区表的查询时，如果查询不包含单行易变（SIRV）函数，GPORCA 可能会生成动态仅索引扫描作为备选方案。如果设为 `off`，GPORCA 就不会生成动态仅索引扫描计划。此参数可以在数据库系统级别、单个数据库级别，或会话和查询级别设置。

## optimizer_enable_dynamicindexscan {#optimizer_enable_dynamicindexscan}

- 取值范围：布尔值
- 默认值：on
- 设置类别：user
- 描述：此参数控制是否在查询计划中启用动态索引扫描。

    启用后，优化器使用动态索引扫描计划。如果此参数设为 `off`，GPORCA 就不会生成动态索引扫描计划，而是退回使用动态顺序扫描作为替代。

## optimizer_enable_foreign_table {#optimizer_enable_foreign_table}

- 参数类型：布尔值
- 默认值：true
- 设置类别：coordinator, session, reload
- 描述：启用 GPORCA（默认）且此参数设为 `true`（默认）时，GPORCA 会为涉及外表的查询生成执行计划。

    如果设为 `false`，包含外表的查询将退回由基于 PostgreSQL 的优化器规划。

## optimizer_enable_indexonlyscan {#optimizer_enable_indexonlyscan}

- 参数类型：布尔值
- 默认值：true
- 设置类别：coordinator, session, reload
- 描述：启用 GPORCA（默认）且此参数设为 `true`（默认）时，GPORCA 可以为 B-树索引以及包含查询中所有列的任意类型索引生成仅索引扫描计划。（GiST 索引仅在某些操作符类上支持仅索引扫描。）

    GPORCA 只访问索引中的值，而不访问表的实际数据块。这可以提高查询执行性能，尤其是在表已执行过 vacuum、包含宽列且所有可见列都已位于索引中，从而无需读取任何数据块的情况下。如果此参数设为 `false`，GPORCA 就不会生成仅索引扫描计划。此参数可以在数据库系统级别、单个数据库级别，或会话和查询级别设置。

## optimizer_enable_orderedagg {#optimizer_enable_orderedagg}

- 参数类型：布尔值
- 默认值：on
- 设置类别：coordinator, session, reload
- 描述：启用 GPORCA（默认）时，此参数控制是否为有序聚合生成查询计划。

    当设为 `on`（默认）时，GPORCA 会为包含有序聚合的查询生成执行计划。当设为 `off` 时，此类查询将退回由基于 PostgreSQL 的优化器规划。

    此参数可以在数据库系统级别、单个数据库级别，或会话和查询级别设置。

## optimizer_enable_push_join_below_union_all {#optimizer_enable_push_join_below_union_all}

- 参数类型：布尔值
- 默认值：off
- 设置类别：coordinator, session, reload
- 描述：启用 GPORCA（默认）时，`optimizer_enable_push_join_below_union_all` 参数控制 GPORCA 在遇到包含 `JOIN UNION ALL` 的查询时的行为。

    默认值为 `off`。当查询包含 `JOIN UNION ALL` 时，GPORCA 不执行任何转换。

    如果设为 `on` 且计划代价符合要求，GPORCA 会将 `JOIN UNION ALL` 转换为多个先执行 `JOIN`、再执行 `UNION ALL` 的子查询。如果 `UNION ALL` 的子查询能够从连接操作中获益（但在原计划中不满足条件），这种转换可能提高连接性能。

    例如，在索引嵌套循环连接非常高效的场景中，如内表很大且有索引、外表很小，或者多个带索引的大表与一个小表进行 `UNION ALL` 时，这种转换可以将连接条件下推为索引条件，性能可能优于哈希连接。

    启用此转换可能增加查询规划时间，因此建议分别在启用和禁用此参数时使用 `EXPLAIN` 分析查询执行计划。此参数可以在数据库系统级别、单个数据库级别，或会话和查询级别设置。

## optimizer_enable_query_parameter {#optimizer_enable_query_parameter}

- 变量类型：布尔值
- 默认值：on
- 设置类别：user
- 描述：允许 GPORCA 优化器处理查询参数。

## optimizer_enable_right_outer_join {#optimizer_enable_right_outer_join}

- 参数类型：布尔值
- 默认值：on
- 设置类别：coordinator, session, reload
- 描述：启用 GPORCA（默认）时，此参数控制 GPORCA 是否生成右外连接。

    如果设为默认值 `on`，GPORCA 既可以直接生成右外连接，也可以在优化器认为合适时将左外连接转换为右外连接。如果设为 `off`，GPORCA 会将输入的右外连接转换为等价的左外连接，并完全避免生成任何右外连接。

    如果使用右外连接的查询出现性能问题，可以将此参数设为 `off` 来禁用右外连接。

    此参数可以在数据库系统级别、单个数据库级别，或会话和查询级别设置。不过，更建议在查询级别控制它，因为在某些场景下，右外连接可能是更合适的查询计划选择。

## optimizer_force_three_stage_scalar_dqa {#optimizer_force_three_stage_scalar_dqa}

- 变量类型：布尔值
- 默认值：on
- 设置类别：user
- 描述：强制优化器始终为标量去重聚合选择三阶段聚合计划。

## optimizer_nestloop_factor {#optimizer_nestloop_factor}

- 变量类型：实数
- 默认值：1024
- 取值范围：[1,1.79769e+308]
- 设置类别：user
- 描述：设置优化器中嵌套循环连接的代价因子。

## optimizer_penalize_broadcast_threshold {#optimizer_penalize_broadcast_threshold}

- 参数类型：整数
- 取值范围：`[0,2147483647]`
- 默认值：100000
- 设置类别：user
- 描述：指定无需施加惩罚即可广播的最大关系行数。

    如果广播行数超过此阈值，优化器会增大该计划的执行代价，以降低选择该计划的可能性。

    将此参数设为 `0` 会禁用惩罚机制，即不对任何广播施加惩罚。

## optimizer_push_group_by_below_setop_threshold {#optimizer_push_group_by_below_setop_threshold}

- 变量类型：整数
- 默认值：10
- 取值范围：[0,2147483647]
- 设置类别：user
- 描述：设置尝试将 `GROUP BY` 操作下推到 SetOp 节点之下时允许的最大子节点数量。

## optimizer_replicated_table_insert {#optimizer_replicated_table_insert}

- 变量类型：布尔值
- 默认值：on
- 设置类别：user
- 描述：向复制表插入数据时省略广播操作。

## optimizer_skew_factor {#optimizer_skew_factor}

- 变量类型：整数
- 默认值：0
- 取值范围：[0,100]
- 设置类别：user
- 描述：设置数据倾斜因子的来源和权重。`0` 表示禁用基于样本统计信息的数据倾斜推导，`1`–`100` 表示启用并基于样本计算倾斜比率；代价估算实际使用的数据倾斜量，是此参数与倾斜比率的乘积。

## optimizer_sort_factor {#optimizer_sort_factor}

- 变量类型：实数
- 默认值：1
- 取值范围：[0,1.79769e+308]
- 设置类别：user
- 描述：设置优化器中排序操作的代价因子；`1.0` 表示与默认代价相同，大于 1 表示排序代价更高，小于 1 表示代价更低。

## optimizer_trace_fallback {#optimizer_trace_fallback}

- 变量类型：布尔值
- 默认值：off
- 设置类别：user
- 描述：GPORCA 退回使用传统优化器时，以 `INFO` 日志级别打印信息。

## optimizer_use_gpdb_allocators {#optimizer_use_gpdb_allocators}

- 变量类型：布尔值
- 默认值：on
- 设置类别：postmaster
- 描述：允许 GPORCA 优化器使用数据库的内存上下文管理机制（Memory Contexts）。

## optimizer_xform_bind_threshold {#optimizer_xform_bind_threshold}

- 变量类型：整数
- 默认值：0
- 取值范围：[0,2147483647]
- 设置类别：user
- 描述：限制每个组表达式上的每条转换规则（xform）最多可以生成的绑定数量。设为 `0` 表示不启用此限制。

## superuser_reserved_connections {#superuser_reserved_connections}

- 取值范围：小于 `max_connections` 的整数
- 默认值：10
- 设置类别：local, system, restart
- 描述：指定为 Apache Cloudberry 数据库超级用户保留的连接槽数量。

## track_io_timing {#track_io_timing}

- 参数类型：布尔值
- 默认值：off
- 设置类别：superuser
- 描述：用于收集数据库 I/O 活动的耗时统计信息。启用后，系统记录语句执行期间的 I/O 操作耗时，有助于性能分析和瓶颈定位。此参数默认关闭，且只能由超级用户设置。

## wal_compression {#wal_compression}

- 变量类型：布尔值
- 默认值：on
- 设置类别：superuser
- 描述：启用对 WAL 文件中整页写入的压缩。

## wal_keep_size {#wal_keep_size}

- 参数类型：整数
- 取值范围：0 - 2147483647（单位为 MB）
- 默认值：320
- 设置类别：sighup
- 描述：指定为备用服务器保留的 WAL 文件的最大大小。

## work_mem {#work_mem}

- 取值范围：整数，单位为千字节
- 默认值：32MB
- 设置类别：coordinator, session, reload
- 描述：指定每个查询操作（如排序或哈希表）在写入磁盘临时文件之前可以使用的最大内存量。如果未指定单位，则默认为千字节。默认值为 32MB。

    在复杂查询中，可能并行执行多个排序或哈希操作，每个操作在写入临时文件之前，都可以使用 `work_mem` 指定的内存量。此外，多个会话可能同时执行这些操作，因此总内存消耗可能远高于 `work_mem` 本身的值。选择此参数的值时，应特别考虑这一点。

    `work_mem` 影响以下操作：用于 `ORDER BY`、`DISTINCT` 和合并连接的排序操作；用于哈希连接、哈希聚合和处理 `IN` 子查询的哈希表；位图索引扫描；以及基于元组存储的操作，例如函数扫描、CTE、PL/pgSQL 和管理 UDF。

    除了为特定执行算子分配内存，`work_mem` 还会影响 PostgreSQL 优化器对某些查询计划的偏好。注意，`work_mem` 独立于资源队列和资源组的内存管理机制。它在查询级别生效，不受资源队列或资源组内存限制的影响。

## writable_external_table_bufsize {#writable_external_table_bufsize}

- 变量类型：整数
- 默认值：1024
- 单位：kB
- 取值范围：[32,131072]
- 设置类别：user
- 描述：设置向可写外部表写入数据之前，向 gpfdist 写入时使用的缓冲区大小（单位为 kB）。
