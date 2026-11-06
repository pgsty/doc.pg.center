---
title: "日志审计"
description: "本文介绍 Apache Cloudberry 中会被记录、且应当监控以检测安全威胁的事件。"
weight: 70
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/security/log-auditing.md"
---

Apache Cloudberry 能够审计多种事件，包括系统启动和关闭、Segment 数据库故障、导致错误的 SQL 语句，以及所有连接尝试和断开连接事件。Apache Cloudberry 还会记录 SQL 语句及其相关信息，并可通过多种配置方式调整审计信息的详细程度。`log_error_verbosity` 配置参数控制写入服务器日志的每条消息的详细程度。类似地，`log_min_error_statement` 参数允许管理员专门配置 SQL 语句记录的详细程度，而 `log_statement` 参数决定审计哪些类型的 SQL 语句。如果可审计事件由 Apache Cloudberry 外部的主体发起，Apache Cloudberry 会记录其用户名。

Apache Cloudberry 仅允许具有适当角色的管理员对日志文件执行操作，以防止未经授权修改和删除审计记录。日志采用基于逗号分隔值（CSV）的专用格式存储。各 Segment 和 Coordinator 分别存储自己的日志文件，管理员也可以远程访问这些文件。Apache Cloudberry 还允许通过 `log_truncate_on_rotation` 参数覆盖旧日志文件。这是一个本地参数，必须在各 Segment 和 Coordinator 的配置文件中分别设置。

Cloudberry 提供了名为 `gp_toolkit` 的管理模式，可用于查询日志文件、系统目录和运行环境，以获取系统状态信息。有关详细信息及用法，请参阅 [`gp_toolkit` — 查看服务器日志文件](/cloudberry/reference/sys-catalogs/gp_toolkit/#view-server-log-files)。

Apache Cloudberry 包含 PostgreSQL 审计扩展 pgaudit，通过 PostgreSQL 提供的标准日志功能，记录详细的会话和对象审计日志。PostgreSQL Audit 的目标是提供生成审计日志所需的工具，以满足某些政府、金融或 ISO 认证审计的要求。

## 查看数据库服务器日志文件 {#view-the-database-server-log-files}

Apache Cloudberry 中的每个数据库实例（Coordinator 和 Segment）都是一个正在运行的 PostgreSQL 数据库服务器，各自拥有服务器日志文件。每日的日志文件在 Coordinator 和各 Segment 数据目录下的 `log` 目录中创建。

服务器日志文件以逗号分隔值（CSV）格式写入。并非每条日志记录的所有字段都有值。例如，只有与查询工作进程相关的日志记录才会填充 `slice_id`。可以通过会话标识符（`gp_session_id`）和命令标识符（`gp_command_count`）识别属于某个查询的相关日志记录。

|\# |字段名 |数据类型 |说明 |
|:--|:----------|:---------|:-----------|
|1 |event_time |timestamp with time zone |日志记录写入日志的时间 |
|2 |user_name |varchar(100) |数据库用户名 |
|3 |database_name |varchar(100) |数据库名 |
|4 |process_id |varchar(10) |系统进程 ID（以 "p" 为前缀） |
|5 |thread_id |varchar(50) |线程计数（以 "th" 为前缀） |
|6 |remote_host |varchar(100) |在 Coordinator 上，为客户端机器的主机名或地址；在 Segment 上，为 Coordinator 的主机名或地址。 |
|7 |remote_port |varchar(10) |Segment 或 Coordinator 的端口号 |
|8 |session_start_time |timestamp with time zone |会话连接建立的时间 |
|9 |transaction_id |int |Coordinator 上的顶层事务 ID。此 ID 是所有子事务的父事务 ID。 |
|10 |gp_session_id |text |会话标识号（以 "con" 为前缀） |
|11 |gp_command_count |text |会话中的命令编号（以 "cmd" 为前缀） |
|12 |gp_segment |text |Segment 的内容标识符（主 Segment 以 "seg" 为前缀，镜像 Segment 以 "mir" 为前缀）。Coordinator 的内容 ID 始终为 -1。 |
|13 |slice_id |text |切片 ID（正在运行的查询计划片段） |
|14 |distr_tranx_id text |分布式事务 ID |
|15 |local_tranx_id |text |本地事务 ID |
|16 |sub_tranx_id |text |子事务 ID |
|17 |event_severity  |varchar(10) |取值包括：LOG、ERROR、FATAL、PANIC、DEBUG1、DEBUG2 |
|18 |sql_state_code |varchar(10) |与日志消息关联的 SQL 状态码 |
|19 |event_message |text |日志或错误消息文本 |
|20 |event_detail |text |与错误或警告消息关联的详细信息文本 |
|21 |event_hint |text |与错误或警告消息关联的提示信息文本 |
|22 |internal_query |text |内部生成的查询文本 |
|23 |internal_query_pos |int |游标在内部生成的查询文本中的位置索引 |
|24 |event_context |text |生成此消息时的上下文 |
|25 |debug_query_string |text |用户提供的查询字符串，包含用于调试的完整详细信息。此字符串可能会被修改以供内部使用。 |
|26 |error_cursor_pos |int |游标在查询字符串中的位置索引 |
|27 |func_name |text |生成此消息的函数 |
|28 |file_name |text |此消息来源的内部代码文件 |
|29 |file_line |int |此消息来源在代码文件中的行号 |
|30 |stack_trace |text |与此消息关联的堆栈跟踪文本 |

Cloudberry 提供了名为 `gplogfilter` 的工具，可在 Apache Cloudberry 日志文件中搜索符合指定条件的记录。默认情况下，该工具会搜索默认日志位置中的 Cloudberry Coordinator 日志文件。例如，显示 Coordinator 日志文件的最后三行：

```shell
$ gplogfilter -n 3
```

也可以通过 `gpssh` 工具运行 `gplogfilter`，一次搜索所有 Segment 日志文件。例如，显示各 Segment 日志文件的最后三行：

```shell
$ gpssh -f seg_host_file
  => source /usr/local/cloudberry-db/greenplum_path.sh
  => gplogfilter -n 3 /data*/*/gp*/pg_log/gpdb*.csv
```

以下是 Cloudberry 中与安全相关的审计（或日志）服务器配置参数，均在 postgresql.conf 配置文件中设置：

|字段名 |取值范围 |默认值 |说明 |
|:-----------|:------------|:--------|:------------|
|log_connections |布尔值 |off |向服务器日志输出一行，详细记录每次成功的连接。一些客户端程序（如 psql）在确定是否需要密码时会尝试连接两次，因此重复的“connection received”消息并不总是表示存在问题。 |
|log_disconnections |布尔值 |off |在客户端会话结束时向服务器日志输出一行，其中包含会话持续时间。 |
|log_statement |NONE<br/>DDL<br/>MOD<br/>ALL |ALL |控制记录哪些 SQL 语句。DDL 记录所有数据定义命令，例如 CREATE、ALTER 和 DROP 命令。MOD 记录所有 DDL 语句，以及 INSERT、UPDATE、DELETE、TRUNCATE 和 COPY FROM。如果 PREPARE 和 EXPLAIN ANALYZE 语句所包含的命令属于应记录的类型，也会记录这些语句。 |
|log_hostname |布尔值 |off |默认情况下，连接日志消息仅显示连接主机的 IP 地址。启用此选项后，还会记录主机名。请注意，根据主机名解析配置的不同，这可能会造成不可忽略的性能开销。 |
|log_duration |布尔值 |off |记录每条已完成且符合 log_statement 设置的语句的执行时长。 |
|log_error_verbosity |TERSE<br/>DEFAULT<br/>VERBOSE |DEFAULT |控制写入服务器日志的每条消息的详细程度。 |
|log_min_duration_statement |毫秒数、0、-1 |-1 |如果语句的执行时长大于或等于指定的毫秒数，则在同一条日志记录中记录该语句及其执行时长。设为 0 时会输出所有语句及其执行时长。-1 表示停用此功能。例如，设为 250 时，所有运行 250ms 或更长时间的 SQL 语句都会被记录。启用此选项有助于找出应用程序中尚未优化的查询。 |
|log_min_messages |DEBUG5<br/>DEBUG4<br/>DEBUG3<br/>DEBUG2<br/>DEBUG1<br/>INFO<br/>NOTICE<br/>WARNING<br/>ERROR<br/>LOG<br/>FATAL<br/>PANIC |NOTICE |控制将哪些级别的消息写入服务器日志。每个级别都包含其后列出的所有级别。级别越靠后，写入日志的消息越少。 |
|log_rotation_size |0 - INT_MAX/1024 千字节|1048576|大于 0 时，每当向日志写入的数据达到指定的千字节数，就创建一个新日志文件。设为零可停用按大小创建新日志文件的功能。 |
|log_rotation_age |任何有效的时间表达式（数值和单位） |1d |决定单个日志文件的存续时间。自当前日志文件创建起经过指定时间后，就会创建一个新日志文件。设为零可停用按时间创建新日志文件的功能。 |
|log_statement_stats |布尔值 |off |对于每个查询，将查询解析器、规划器和执行器的总体性能统计信息写入服务器日志。这是一种粗略的性能分析工具。 |
|log_truncate_on_rotation |布尔值 |off |截断（覆盖）已有的同名日志文件，而不是追加内容。只有因按时间轮转而打开新文件时，才会发生截断。例如，将此设置与 `gpseg#-%H.log` 这样的 `log_filename` 配合使用，会生成 24 个按小时划分的日志文件，然后循环覆盖这些文件。关闭此选项时，始终向已有文件追加内容。 |
