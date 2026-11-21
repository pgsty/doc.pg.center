---
title: "配置参数"
description: "本文按字母顺序列出 Apache Cloudberry 数据库的配置参数（GUC）。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/config-params-guc-list.md"
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

## gp_autostats_mode {#gp_autostats_mode}

- 变量类型：枚举
- 默认值：none
- 取值范围：none, on_change, onchange, on_no_stats
- 设置类别：user
- 描述：控制在函数外执行的语句修改表后，Coordinator 是否自动对该表运行 `ANALYZE`（函数内的语句使用 `gp_autostats_mode_in_functions`）。`on_change` 在 `CREATE TABLE AS`、`INSERT`、`UPDATE`、`DELETE` 或 `COPY FROM` 影响的行数超过 `gp_autostats_on_change_threshold` 时执行分析；`on_no_stats` 在 `CREATE TABLE AS` 后执行分析，也在向尚无统计信息的表执行 `INSERT` 或 `COPY FROM` 后执行分析；`none` 关闭自动分析，`onchange` 是可接受的 `on_change` 的另一种拼写。视图和分区父表从不通过此方式分析。

## gp_cached_segworkers_threshold {#gp_cached_segworkers_threshold}

- 变量类型：整数
- 默认值：5
- 取值范围：[1,2147483647]
- 设置类别：user
- 描述：设置会话为后续语句复用而缓存的空闲 Segment 工作进程（QE）数量上限，按每个 Segment 计算。释放读取工作进程时，如果该 Segment 的空闲列表已有此数量的工作进程，就销毁该进程而不再缓存。会话的写入工作进程不会因这一限制而被销毁，但会占用同一空闲列表中的一个位置，因此缓存写入工作进程时，读取工作进程的缓存数量上限比此值少一个。无论此参数如何设置，Coordinator 上的工作进程上限均为 1。

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

## gp_max_plan_size {#gp_max_plan_size}

- 变量类型：整数
- 默认值：0
- 单位：kB
- 取值范围：[0,2147483647]
- 设置类别：superuser
- 描述：设置 Coordinator 向 Segment 派发的未压缩序列化查询计划的大小上限。计划大小超过此值的查询会失败，报错为 "Query plan size limit exceeded"。值为 0 表示不限制。

## gp_max_slices {#gp_max_slices}

- 变量类型：整数
- 默认值：0
- 取值范围：[0,2147483647]
- 设置类别：user
- 描述：设置单个查询计划允许的最大切片数。切片数超过此值的查询会在执行器启动时报错失败。值为 0 表示不限制。

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

## gp_vmem_protect_limit {#gp_vmem_protect_limit}

- 变量类型：整数
- 默认值：8192
- 取值范围：[0,1073741823]
- 设置类别：postmaster
- 描述：设置一个 Segment 实例上的所有数据库会话通过 Cloudberry 内存跟踪器总共可预留的内存量，单位为 MB。该值是以 MB 为单位的纯数字，不附加单位，例如应写为 `8192`，而非 `8GB`。当 Segment 上的查询进程分配内存将使该 Segment 的内存总量超过此限制时，分配失败并报错 "Out of memory"，错误详情以 "Vmem limit reached" 开头。此限制适用于所有 `gp_resource_manager` 设置，`runaway_detector_activation_percent` 也以此值的百分比计算。

## krb_server_keyfile {#krb_server_keyfile}

- 变量类型：字符串
- 默认值：`<FILE:/workspace/dist/database/etc/postgresql/krb5.keytab>`
- 设置类别：sighup
- 描述：设置 Kerberos 服务器密钥文件的位置。

## lock_timeout {#lock_timeout}

- 变量类型：整数
- 默认值：0
- 单位：ms
- 取值范围：[0,2147483647]
- 设置类别：user
- 描述：设置任意语句等待获取表、索引、行或其他数据库对象上的锁的最长时间。如果等待超过此时长，语句会报错中止。值为 0 表示关闭此超时。

## log_autostats {#log_autostats}

- 变量类型：布尔值
- 默认值：off
- 设置类别：superuser
- 描述：记录自动统计信息收集发起的 ANALYZE 操作详情（参见 `gp_autostats_mode`）。启用后，服务器日志记录哪个命令在哪张表上触发了自动 ANALYZE，也记录因用户不是表所有者而跳过自动 ANALYZE 的情况（仅当 `gp_autostats_allow_nonowner` 为默认值 off 时才执行此检查）。

## log_autovacuum_min_duration {#log_autovacuum_min_duration}

- 变量类型：整数
- 默认值：-1
- 单位：ms
- 取值范围：[-1,2147483647]
- 设置类别：sighup
- 描述：设置记录 autovacuum 操作所需的最短执行时间，超过此时长的操作会记入日志。值为 0 时记录所有 autovacuum 操作，-1 关闭 autovacuum 日志。也可以通过 `log_autovacuum_min_duration` 存储参数按表设置。

## log_btree_build_stats {#log_btree_build_stats}

- 变量类型：布尔值
- 默认值：off
- 设置类别：superuser
- 描述：将各类 B-树操作的系统资源使用统计信息（内存和 CPU）写入服务器日志。这是开发者选项，仅在构建服务器时定义了 `BTREE_BUILD_STATS` 宏的情况下存在，默认构建不包含此宏。

## log_checkpoints {#log_checkpoints}

- 取值范围：布尔值
- 默认值：on
- 设置类别：local, system, reload
- 描述：将检查点和重启点信息写入服务器日志。日志消息包含写入的缓冲区数量、写入耗时等统计信息。

## log_connections {#log_connections}

- 变量类型：布尔值
- 默认值：off
- 设置类别：superuser-backend
- 描述：每次连接尝试以及每次成功的客户端身份验证都会向服务器日志写入一行。某些客户端程序（如 psql）在确定是否需要密码时会尝试连接两次，因此重复的 "connection received" 消息并不总是表示存在问题。

## log_destination {#log_destination}

- 变量类型：字符串
- 默认值：stderr
- 设置类别：sighup
- 描述：设置服务器日志输出目标，以逗号分隔的列表指定 `stderr`、`csvlog`、`syslog` 和 `eventlog`。`syslog` 仅在支持它的平台上可用，`eventlog` 仅在 Windows 上可用。`csvlog` 要求启用 `logging_collector`。当列表包含 `stderr`、启用了 `logging_collector`，且 `gp_log_format` 为默认值 `csv` 时，所有消息都以 CSV 格式写入日志文件，不会发送至列表中的其他目标。要使用 `csvlog`、`syslog` 或 `eventlog`，请从列表中移除 `stderr`，或将 `gp_log_format` 设为 `text`。此参数不在 `SHOW ALL` 中显示。源码将其标为已废弃，但服务器仍在使用它。

## log_directory {#log_directory}

- 变量类型：字符串
- 默认值：log
- 设置类别：sighup
- 描述：设置启用日志收集器时写入服务器日志文件的目录。可以是绝对路径，也可以是相对于数据目录的路径。此参数不在 `SHOW ALL` 中显示，只有超级用户和 `pg_read_all_settings` 的成员可以查看。源码将其标为已废弃，但服务器仍在使用它。

## log_disconnections {#log_disconnections}

- 变量类型：布尔值
- 默认值：off
- 设置类别：superuser-backend
- 描述：客户端会话结束时，向服务器日志写入一行，其中包含会话持续时间。

## log_dispatch_stats {#log_dispatch_stats}

- 变量类型：布尔值
- 默认值：off
- 设置类别：superuser
- 描述：将每条语句的派发器性能统计信息写入服务器日志。当 `log_statement_stats`、`log_parser_stats`、`log_planner_stats` 或 `log_executor_stats` 中的任一项开启时，不能开启此参数。

## log_duration {#log_duration}

- 变量类型：布尔值
- 默认值：off
- 设置类别：superuser
- 描述：记录每条已完成 SQL 语句的执行时长。

## log_error_verbosity {#log_error_verbosity}

- 变量类型：枚举
- 默认值：default
- 取值范围：terse, default, verbose
- 设置类别：superuser
- 描述：控制每条日志消息写入服务器日志的详细程度。`terse` 省略 DETAIL、HINT、QUERY 和 CONTEXT 字段；`verbose` 添加 SQLSTATE 错误码，以及产生该消息的源文件名、函数名和行号。此参数不影响 Cloudberry 以自有 CSV 格式写入的消息；当 `log_destination` 包含 `stderr`、`logging_collector` 开启且 `gp_log_format` 为 `csv` 时，就会使用这种格式，而这些均为默认设置。对于 `csvlog` 输出，它只控制是否写入源文件名、函数名和行号。

## log_executor_stats {#log_executor_stats}

- 变量类型：布尔值
- 默认值：off
- 设置类别：superuser
- 描述：将每条语句的执行器性能统计信息写入服务器日志。当 `log_statement_stats` 开启时，不能开启此参数。

## log_file_mode {#log_file_mode}

- 变量类型：整数
- 默认值：0600
- 取值范围：[0000,0777]
- 设置类别：sighup
- 描述：设置 `logging_collector` 开启时创建的日志文件的权限。其值为 `chmod` 和 `umask` 系统调用接受的数字模式。使用常见的八进制格式时，数字必须以 0（零）开头。

## log_filename {#log_filename}

- 变量类型：字符串
- 默认值：gpdb-%Y-%m-%d_%H%M%S.csv
- 设置类别：sighup
- 描述：设置服务器日志文件的名称模式，按 `strftime` 模式解释。文件后缀由 `gp_log_format` 决定：使用默认 CSV 格式时，如果名称不以 `.csv` 结尾，就将其最后四个字符替换为 `.csv`；使用 TEXT 格式时，则将末尾的 `.csv` 替换为 `.log`。只有超级用户和 `pg_read_all_settings` 的成员可以查看此参数，`SHOW ALL` 不显示它。

## log_hostname {#log_hostname}

- 变量类型：布尔值
- 默认值：off
- 设置类别：sighup
- 描述：默认情况下，连接日志消息只显示连接主机的 IP 地址。开启此参数后，还会记录主机名；这需要为每次连接执行反向 DNS 查询，根据主机名解析配置的不同，可能带来不可忽略的性能开销。

## log_line_prefix {#log_line_prefix}

- 变量类型：字符串
- 默认值：`'%m [%p] '`
- 设置类别：sighup
- 描述：设置写入每行日志开头的 printf 风格字符串。`%m`（带毫秒的时间戳）和 `%p`（进程 ID）等 `%` 转义会替换为状态信息。空值表示无前缀。Cloudberry 以自有 CSV 格式写入的消息不使用此前缀；当 `log_destination` 包含 `stderr`、`logging_collector` 开启且 `gp_log_format` 为 `csv` 时，就会使用这种格式，而这些均为默认设置。此参数不在 `SHOW ALL` 中显示。源码将其标为已废弃，但服务器仍在使用它。

## log_lock_waits {#log_lock_waits}

- 变量类型：布尔值
- 默认值：off
- 设置类别：superuser
- 描述：会话等待获取锁的时间超过 `deadlock_timeout` 时，写入一条日志消息。

## log_min_duration_sample {#log_min_duration_sample}

- 变量类型：整数
- 默认值：-1
- 单位：ms
- 取值范围：[-1,2147483647]
- 设置类别：superuser
- 描述：对执行时长至少达到指定时间的已完成语句进行抽样，记录语句及其执行时长。`log_statement_sample_rate` 指定记录比例。`0` 将所有语句纳入抽样，`-1` 禁用此功能。超过 `log_min_duration_statement` 的语句始终记录。

## log_min_duration_statement {#log_min_duration_statement}

- 变量类型：整数
- 默认值：-1
- 单位：ms
- 取值范围：[-1,2147483647]
- 设置类别：superuser
- 描述：记录执行时长至少达到指定时间的每条已完成语句及其执行时长。`0` 记录所有语句及其执行时长，`-1` 禁用此功能。

## log_min_error_statement {#log_min_error_statement}

- 变量类型：枚举
- 默认值：error
- 取值范围：debug5, debug4, debug3, debug2, debug1, info, notice, warning, error, log, fatal, panic
- 设置类别：superuser
- 描述：当消息严重级别达到或超过此级别时，将导致错误的 SQL 语句写入服务器日志。每个级别都包含其后的所有级别；级别越靠后，记录的语句越少。

## log_min_messages {#log_min_messages}

- 变量类型：枚举
- 默认值：warning
- 取值范围：debug5, debug4, debug3, debug2, debug1, info, notice, warning, error, log, fatal, panic
- 设置类别：superuser
- 描述：控制写入服务器日志的消息级别。每个级别都包含其后的所有级别；级别越靠后，写入日志的消息越少。

## log_parameter_max_length {#log_parameter_max_length}

- 变量类型：整数
- 默认值：-1
- 单位：B
- 取值范围：[-1,1073741823]
- 设置类别：superuser
- 描述：设置随语句一起写入服务器日志的每个绑定参数值的最大字节数。`-1` 完整记录参数值，`0` 关闭这些消息中的绑定参数值记录。

## log_parameter_max_length_on_error {#log_parameter_max_length_on_error}

- 变量类型：整数
- 默认值：0
- 单位：B
- 取值范围：[-1,1073741823]
- 设置类别：user
- 描述：设置写入错误消息的每个绑定参数值的最大字节数。`-1` 完整记录参数值，`0`（默认值）关闭错误消息中的绑定参数值记录。

## log_parser_stats {#log_parser_stats}

- 变量类型：布尔值
- 默认值：off
- 设置类别：superuser
- 描述：将每条语句的解析器性能统计信息写入服务器日志。当 `log_statement_stats` 开启时，不能开启此参数。

## log_planner_stats {#log_planner_stats}

- 变量类型：布尔值
- 默认值：off
- 设置类别：superuser
- 描述：将每条语句的规划器性能统计信息写入服务器日志。当 `log_statement_stats` 开启时，不能开启此参数。

## log_recovery_conflict_waits {#log_recovery_conflict_waits}

- 变量类型：布尔值
- 默认值：off
- 设置类别：sighup
- 描述：备库上的启动进程因恢复冲突而等待的时间超过 `deadlock_timeout` 时，写入一条日志消息。

## log_replication_commands {#log_replication_commands}

- 变量类型：布尔值
- 默认值：off
- 设置类别：superuser
- 描述：将每条复制命令写入服务器日志。

## log_rotation_age {#log_rotation_age}

- 变量类型：整数
- 默认值：1440
- 单位：min
- 取值范围：[0,35791394]
- 设置类别：sighup
- 描述：设置日志文件的最长使用时间，达到该时长后，日志收集器关闭当前文件并创建新文件。默认值为 1440 分钟（1d），即每 24 小时创建一个新日志文件。设为 0 可关闭按时间轮转日志。

## log_rotation_size {#log_rotation_size}

- 变量类型：整数
- 默认值：1048576
- 单位：kB
- 取值范围：[0,2097151]
- 设置类别：sighup
- 描述：设置日志文件的大小上限，达到该大小后，日志收集器关闭当前文件并创建新文件。默认值 1048576 kB 即 1 GB。设为 0 可关闭按大小轮转日志。

## log_statement {#log_statement}

- 变量类型：枚举
- 默认值：none
- 取值范围：none, ddl, mod, all
- 设置类别：superuser
- 描述：控制将哪些 SQL 语句写入服务器日志。`ddl` 记录 CREATE、ALTER 和 DROP 等数据定义语句；`mod` 记录这些语句以及 INSERT、UPDATE、DELETE、TRUNCATE 和 COPY FROM 等数据修改语句；`all` 记录每条语句。内置默认值为 `none`，但 `gpinitsystem` 会将 `log_statement=all` 写入 Coordinator 的 `postgresql.conf`。

## log_statement_sample_rate {#log_statement_sample_rate}

- 变量类型：实数
- 默认值：1
- 取值范围：[0,1]
- 设置类别：superuser
- 描述：设置超过 `log_min_duration_sample` 的语句的记录比例。`0` 表示均不记录，`1` 表示全部记录。

## log_statement_stats {#log_statement_stats}

- 变量类型：布尔值
- 默认值：off
- 设置类别：superuser
- 描述：将每条语句的累计性能统计信息（解析器、规划器和执行器的合计）写入服务器日志。当 `log_parser_stats`、`log_planner_stats`、`log_dispatch_stats` 或 `log_executor_stats` 中的任一项开启时，不能开启此参数。

## log_temp_files {#log_temp_files}

- 变量类型：整数
- 默认值：-1
- 单位：kB
- 取值范围：[-1,2147483647]
- 设置类别：superuser
- 描述：临时文件删除时，如果其大小大于或等于此值，则记录该文件的名称和大小。设为 0 可记录所有临时文件，设为 -1（默认值）可关闭此日志记录。

## log_timezone {#log_timezone}

- 变量类型：字符串
- 默认值：GMT
- 设置类别：sighup
- 描述：设置写入服务器日志的时间戳所用的时区。`initdb` 会在 `postgresql.conf` 中将其设为所在环境的时区。

## log_transaction_sample_rate {#log_transaction_sample_rate}

- 变量类型：实数
- 默认值：0
- 取值范围：[0,1]
- 设置类别：superuser
- 描述：设置需要记录其全部语句的事务比例，不考虑语句执行时长。`0` 表示不记录，`1` 表示记录所有事务的语句。

## log_truncate_on_rotation {#log_truncate_on_rotation}

- 变量类型：布尔值
- 默认值：off
- 设置类别：sighup
- 描述：开启时，日志收集器截断（覆盖）已有的同名日志文件，而不是向其追加内容。只有按时间轮转且新文件名不同于当前文件名时才会截断；按大小轮转和服务器启动始终采用追加方式。

## max_connections {#max_connections}

- 取值范围：10 - 262143
- 默认值：Coordinator 上为 250，Segment 上为 750
- 设置类别：local, system, restart
- 描述：数据库服务器允许的最大并发连接数。

    在 Apache Cloudberry 系统中，客户端连接只能通过 Coordinator 实例接入。Segment 实例允许的连接数应为 Coordinator 的 3 至 10 倍。增大此参数的值时，必须相应增大 `max_prepared_transactions` 的值。

    此参数值越大，Apache Cloudberry 所需的共享内存就越多。

## max_locks_per_transaction {#max_locks_per_transaction}

- 变量类型：整数
- 默认值：128
- 取值范围：[10,2147483647]
- 设置类别：postmaster
- 描述：控制共享锁表的大小。其容量按每个服务器进程或预备事务在任一时刻最多需要锁定 `max_locks_per_transaction` 个对象的假设确定。锁表可容纳 `max_locks_per_transaction` *（`max_connections` + `max_prepared_transactions` + 其他后台进程数）个锁条目，因此只要锁表还有空闲空间，单个事务就可以锁定超过此数量的对象。如果查询涉及大量表或分区，并因共享内存不足而失败，请增大此值。

## max_replication_slots {#max_replication_slots}

- 变量类型：整数
- 默认值：10
- 取值范围：[0,262143]
- 设置类别：postmaster
- 描述：设置可以同时定义的最大复制槽数量。

## max_slot_wal_keep_size {#max_slot_wal_keep_size}

- 变量类型：整数
- 默认值：-1
- 单位：MB
- 取值范围：[-1,2147483647]
- 设置类别：sighup
- 描述：设置复制槽可在磁盘上保留的 WAL 最大数量。如果某个槽保留的 WAL 超过此值，该槽会被标为无效，所保留的 WAL 段会释放以供删除或回收。值为 -1 表示复制槽可保留不限量的 WAL。

## max_statement_mem {#max_statement_mem}

- 变量类型：整数
- 默认值：2048000
- 单位：kB
- 取值范围：[32768,2147483647]
- 设置类别：superuser
- 描述：设置 `statement_mem` 的上限：尝试将 `statement_mem` 设为大于或等于 `max_statement_mem` 的值时会被拒绝。它也以相同方式限制 `gp_resgroup_memory_query_fixed_mem`。默认值 `2048000` kB 即 2000MB。

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

## statement_mem {#statement_mem}

- 变量类型：整数
- 默认值：128000
- 单位：kB
- 取值范围：[1000,2147483647]
- 设置类别：user
- 描述：设置为查询预留的内存量。默认值 `128000` kB 即 125MB。查询实际获得的内存还取决于资源管理器：资源队列的 `MEMORY_LIMIT`，或资源组的 `MEMORY_QUOTA` 和 `gp_resgroup_memory_query_fixed_mem`。此值必须小于 `max_statement_mem`。

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
