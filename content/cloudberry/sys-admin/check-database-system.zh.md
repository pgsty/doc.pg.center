---
title: "检查 Apache Cloudberry 系统"
linkTitle: "检查数据库系统"
description: "可以使用系统自带或以插件形式提供的各种工具检查 Apache Cloudberry 系统。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/check-database-system.md"
---

观察 Apache Cloudberry 系统的日常运行性能，有助于管理员了解系统行为、规划工作流并排查问题。本页介绍诊断数据库性能和活动的场景。

<!-- Also, be sure to review [Recommended Monitoring and Maintenance Tasks](/cloudberry/sys-admin/recommended-maintenance-monitoring-tasks/) for monitoring activities you can script to quickly detect problems in the system. -->
作为 Apache Cloudberry 管理员，需要检查系统是否出现问题，例如 Segment 停止运行或 Segment 主机磁盘空间耗尽。以下主题介绍如何检查 Apache Cloudberry 系统的健康状况，以及如何查看系统的特定状态信息。

- [检查系统状态](#check-system-state)
- [检查磁盘空间使用情况](#check-disk-space-usage)
- [检查数据分布倾斜](#check-for-data-distribution-skew)
<!-- - [Check for and terminate overflowed backends](#check-for-and-terminate-overflowed-backends) -->
- [查看数据库对象的元数据信息](#view-metadata-information-about-database-objects)
- [查看会话内存使用信息](#view-session-memory-usage-information)
- [查看并记录每个进程的内存使用信息](#view-and-log-per-process-memory-usage-information)
- [查看查询工作文件使用信息](#view-query-workfile-usage-information)

## 检查系统状态 {#check-system-state}

Apache Cloudberry 系统由分布在多台机器上的多个 PostgreSQL 实例（Coordinator 和 Segment）组成。要检查 Apache Cloudberry 系统，需要了解整个系统的信息以及各个实例的状态信息。`gpstate` 工具提供 Apache Cloudberry 系统的状态信息。

### 查看 Coordinator 和 Segment 的状态与配置 {#view-coordinator-and-segment-status-and-configuration}

`gpstate` 的默认操作是检查 Segment 实例，并显示正常 Segment 和故障 Segment 的简要状态。例如，要快速查看 Apache Cloudberry 系统的状态：

```shell
gpstate
```

要查看更详细的 Apache Cloudberry 阵列配置，请将 `gpstate` 与 `-s` 选项一起使用：

```shell
gpstate -s
```

### 查看镜像配置和状态 {#view-your-mirroring-configuration-and-status}

如果使用镜像来实现数据冗余，可能需要查看系统中的镜像 Segment 实例列表、它们当前的同步状态，以及镜像到主实例的映射。例如，要查看系统中的镜像 Segment 及其状态：

```shell
gpstate -m
```

要查看主 Segment 到镜像 Segment 的映射：

```shell
gpstate -c
```

要查看 Standby Coordinator 镜像的状态：

```shell
gpstate -f
```

## 检查磁盘空间使用情况 {#check-disk-space-usage}

对于数据库管理员，检查磁盘空间使用情况至关重要。关键是将 Coordinator 和 Segment 数据目录的使用率保持在 70% 以下。磁盘已满虽然不会损坏数据，但可能停止正常的数据库活动，最终迫使服务器关闭。

可以使用 `gp_toolkit` 管理模式中的 `gp_disk_free` 外部表，检查 Segment 主机文件系统中剩余的可用空间（以千字节为单位）。例如：

```sql
SELECT * FROM gp_toolkit.gp_disk_free ORDER BY dfsegment;
```

### 检查分布式数据库和表的大小 {#check-the-sizing-of-distributed-databases-and-tables}

`gp_toolkit` 管理模式包含多个视图，可以用来确定分布式 Apache Cloudberry 数据库、模式、表或索引的磁盘空间使用情况。

#### 查看数据库的磁盘空间使用情况 {#view-disk-space-usage-for-a-database}

要查看数据库的总大小（以字节为单位），请使用 `gp_toolkit` 管理模式中的 `gp_size_of_database` 视图。例如：

```sql
SELECT * FROM gp_toolkit.gp_size_of_database ORDER BY sodddatname;
```

#### 查看表的磁盘空间使用情况 {#view-disk-space-usage-for-a-table}

`gp_toolkit` 管理模式包含多个用于检查表大小的视图。表大小视图按对象 ID（而不是名称）列出表。例如：

```sql
SELECT relname AS name, sotdsize AS size, sotdtoastsize 
AS toast, sotdadditionalsize AS other 
FROM gp_toolkit.gp_size_of_table_disk as sotd, pg_class 
WHERE sotd.sotdoid=pg_class.oid ORDER BY relname;
```

要按名称检查表的大小，需要在 `pg_class` 表中查找关系名称（`relname`）。例如，要查看 `test_table` 表的大小：

```sql
SELECT relname AS name, sotdsize AS size, sotdtoastsize 
AS toast, sotdadditionalsize AS other 
FROM gp_toolkit.gp_size_of_table_disk as sotd, pg_class 
WHERE sotd.sotdoid=pg_class.oid AND pg_class.relname = 'test_table'
ORDER BY relname;
```

#### 查看索引的磁盘空间使用情况 {#view-disk-space-usage-for-indexes}

`gp_toolkit` 管理模式包含多个用于检查索引大小的视图。要查看表上所有索引的总大小，请使用 `gp_size_of_all_table_indexes` 视图。要查看特定索引的大小，请使用 `gp_size_of_index` 视图。索引大小视图按对象 ID（而不是名称）列出表和索引。例如，要查看表上所有索引的大小：

```sql
SELECT soisize, relname as indexname
FROM pg_class, gp_toolkit.gp_size_of_index
WHERE pg_class.oid=gp_size_of_index.soioid 
AND pg_class.relkind='i';
```

要按名称检查索引的大小，需要在 `pg_class` 表中查找关系名称（`relname`）。例如，要检查 `test_index` 索引的大小：

```sql
SELECT pg_class.relname AS indexname, gp_toolkit.gp_size_of_index.soioid, gp_toolkit.gp_size_of_index.soisize
FROM pg_class, gp_toolkit.gp_size_of_index
WHERE pg_class.oid = gp_toolkit.gp_size_of_index.soioid
AND pg_class.relkind = 'i'
AND pg_class.relname = 'test_index';
```

## 检查数据分布倾斜 {#check-for-data-distribution-skew}

Apache Cloudberry 中的所有表都是分布式的，也就是说，数据会分布到系统的所有 Segment 上。不均匀的数据分布可能降低查询处理性能。表创建时设置的分布策略决定表行的分布方式。有关如何选择表分布策略，请参见以下主题：

- [查看表的分布键](#view-a-tables-distribution-key)
- [查看数据分布](#view-data-distribution)
- [检查查询处理倾斜](#check-for-query-processing-skew)

`gp_toolkit` 管理模式还包含多个用于检查表数据分布倾斜的视图。

### 查看表的分布键 {#view-a-tables-distribution-key}

要查看用作表数据分布键的列，可以在 `psql` 中使用 `\d+` 元命令查看表定义。例如：

```sql
=# \d+ sales

                Table "retail.sales"
 Column      |     Type     | Modifiers | Description
-------------+--------------+-----------+-------------
 sale_id     | integer      |           |
 amt         | float        |           |
 date        | date         |           |
Has OIDs: no
Distributed by: (sale_id)
```

创建复制表时，Apache Cloudberry 会在每个 Segment 上存储表中的所有行。复制表没有分布键。对于普通分布表，`\d+` 元命令会报告分布键；对于复制表，它会显示 `Distributed Replicated`。

### 查看数据分布 {#view-data-distribution}

要查看表行的数据分布（每个 Segment 上的行数），可以运行如下查询：

```sql
SELECT gp_segment_id, count(*) 
FROM <table_name> GROUP BY gp_segment_id;
```

如果所有 Segment 的行数大致相同，则认为表的分布是平衡的。

> [!TIP]
> 如果在复制表上运行此查询，会失败，因为 Apache Cloudberry 不允许用户查询引用复制表中的系统列 `gp_segment_id`（或系统列 `ctid`、`cmin`、`cmax`、`xmin` 和 `xmax`）。由于每个 Segment 都包含表的所有行，复制表按定义均匀分布。

### 检查查询处理倾斜 {#check-for-query-processing-skew}

查询处理时，所有 Segment 都应具有相同的工作负载，以确保最佳性能。如果发现查询性能不佳，可能需要使用 `EXPLAIN` 命令进一步调查。<!-- For information about using the `EXPLAIN` command and query profiling, see [Query Profiling](/cloudberry/performance/optimize-queries/analyze-query-performance/).-->

如果表的数据分布策略与查询谓词不匹配，查询处理工作负载可能发生倾斜。要检查处理倾斜，可以运行如下查询：

```sql
=# SELECT gp_segment_id, count(*) FROM <table_name>
   WHERE <column>='<value>' GROUP BY gp_segment_id;
```

这会显示给定 `WHERE` 谓词在每个 Segment 上返回的行数。

如[查看数据分布](#view-data-distribution)中所述，如果在复制表上运行此查询，会失败，因为查询中不能引用复制表的 `gp_segment_id` 系统列。

#### 避免极端倾斜警告 {#avoid-an-extreme-skew-warning}

执行哈希连接操作的查询时，可能会收到以下警告消息：

`Extreme skew in the innerside of Hashjoin`

当哈希连接运算符的输入发生倾斜时，就会出现此情况。它不会阻止查询成功完成。可以执行以下步骤，避免计划中出现倾斜：

1. 确保所有事实表都已分析。
2. 验证查询使用的任何已填充临时表都已分析。
3. 查看查询的 `EXPLAIN ANALYZE` 计划，并查找以下情况：

    - 如果带有多列过滤条件的扫描产生的行数多于估计值，请将服务器配置参数 `gp_selectivity_damping_factor` 设置为 `2` 或更高，然后重新测试查询。
    - 如果在连接一个相对较小（少于 5000 行）的单个事实表时发生倾斜，请将服务器配置参数 `gp_segments_for_planner` 设置为 `1`，然后重新测试查询。

4. 检查查询中应用的过滤条件是否与基表的分布键匹配。如果过滤条件和分布键相同，可以考虑使用不同的分布键重新分布部分基表。
5. 检查连接键的基数。如果基数较低，可以尝试使用不同的连接列或在表上增加过滤条件重写查询，以减少行数。这些更改可能改变查询语义。

<!-- ## Check for and terminate overflowed backends

Sub-transaction overflow occurs when a Apache Cloudberry backend creates more than 64 sub-transactions, resulting in a high lookup cost for visibility checks. This slows query performance, but even more so when it occurs in combination with long-running transactions, which result in still more lookups. Terminating sub-overflowed backends and/or backends with long-running transactions can help prevent and alleviate performance problems.

Apache Cloudberry includes a view (`gp_suboverflowed_backend`) that is run over a user-defined function to help users query for sub-overflowed backends. Users can use segment id and process id information reported in the view to terminate the offending backends, thereby preventing degradation of performance.

### Steps for identifying and terminating overflowed backends {#steps-for-identifying-and-terminating-overflowed-backends}

Follow these steps below to identify and terminate overflowed backends.

1. Select all from the view:

    ```sql
    select * from gp_suboverflowed_backend;
    ```

    This returns output similar to the following:

    ```sql
   segid |   pids    
    -------+-----------
    -1 | 
     0 | {1731513}
     1 | {1731514}
     2 | {1731515}
   (4 rows)
    ```

2. Connect to the database in utility mode and query `pg_stat_activity` to return the session id for the process id in the output for a segment. For example:

    ```sql
    select sess_id from pg_stat_activity where pid=1731513;
    ```

    ```sql
    sess_id 
    ---------
      10
    (1 row)
    ```

3. Terminate the session, which will terminate all associated backends on all segments:

    ```sql
    select pg_terminate_backend(pid) from pg_stat_activity where sess_id=10;
    ```

4. Verify that there are no more sub-overflowed backends:

    ```sql
    select * from gp_suboverflowed_backend;
    ```

    ```sql
   segid |   pids    
    -------+-----------
    -1 | 
     0 |
     1 | 
     2 | 
    (4 rows)
    ``` -->

## 查看数据库对象的元数据信息 {#view-metadata-information-about-database-objects}

Apache Cloudberry 在系统目录中跟踪数据库对象的各种元数据信息，例如表、视图、索引等，以及角色和表空间等全局对象。

### 查看上次执行的操作 {#view-the-last-operation-performed}

可以使用系统视图 `pg_stat_operations` 和 `pg_stat_partition_operations` 查看对对象（例如表）执行的操作。例如，要查看对某张表执行的操作，包括表的创建时间以及上次 vacuum 和 analyze 的时间：

```sql
=> SELECT schemaname as schema, objname as table, 
   usename as role, actionname as action, 
   subtype as type, statime as time 
   FROM pg_stat_operations 
   WHERE objname='test_table';

 schema |   table    |  role   | action  | type  |             time              
--------+------------+---------+---------+-------+-------------------------------
 public | test_table | gpadmin | CREATE  | TABLE | 2024-01-16 15:26:36.998256+08
 public | test_table | gpadmin | VACUUM  |       | 2024-01-16 15:26:42.073407+08
 public | test_table | gpadmin | ANALYZE |       | 2024-01-16 15:26:45.97546+08
(3 rows)
```

### 查看对象定义 {#view-the-definition-of-an-object}

要查看表或视图等对象的定义，可以在 `psql` 中使用 `\d+` 元命令。例如，要查看表定义：

```sql
\d+ <mytable>
```

## 查看会话内存使用信息 {#view-session-memory-usage-information}

可以创建并使用 `session_level_memory_consumption` 视图，查看正在 Apache Cloudberry 上运行查询的会话当前内存使用情况。该视图包含会话信息，以及会话连接的数据库、当前运行的查询和会话进程消耗的内存等信息。

- [创建 `session_level_memory_consumption` 视图](#create-the-session_level_memory_consumption-view)
- [关于 `session_level_memory_consumption` 视图](#about-the-session_level_memory_consumption-view)

### 创建 `session_level_memory_consumption` 视图 {#create-the-session_level_memory_consumption-view}

要在 Apache Cloudberry 中创建 `session_state.session_level_memory_consumption` 视图，请对每个数据库执行一次 `CREATE EXTENSION gp_internal_tools;` 命令。例如，要在 `testdb` 数据库中安装该视图，请使用以下命令：

```shell
psql -d testdb -c "CREATE EXTENSION gp_internal_tools;"
```

### 关于 `session_level_memory_consumption` 视图 {#about-the-session_level_memory_consumption-view}

`session_state.session_level_memory_consumption` 视图提供正在运行 SQL 查询的会话的内存消耗和空闲时间信息。

启用基于资源队列的资源管理时，`is_runaway` 列根据会话查询的 ` vmem` 内存消耗，表示 Apache Cloudberry 是否将该会话视为失控会话。在基于资源队列的资源管理方案下，当查询消耗过多内存时，Apache Cloudberry 会将会话视为失控会话。Apache Cloudberry 服务器配置参数 `runaway_detector_activation_percent` 控制 Apache Cloudberry 将会话视为失控会话的条件。

基于资源组的资源管理处于活动状态时，`is_runaway`、`runaway_vmem_mb` 和 `runaway_command_cnt` 列不适用。

|列|类型|引用|描述|
|------|----|----------|-----------|
|`datname`|name| |会话连接的数据库名称。|
|`sess_id`|integer| |会话 ID。|
|`usename`|name| |会话用户名称。|
|`query`|text| |会话当前正在运行的 SQL 查询。|
|`segid`|integer| |Segment ID。|
|`vmem_mb`|integer| |会话的 vmem 内存总使用量，单位为 MB。|
|`is_runaway`|boolean| |该会话在 Segment 上被标记为失控会话。|
|`qe_count`|integer| |会话的查询进程数。|
|`active_qe_count`|integer| |会话的活动查询进程数。|
|`dirty_qe_count`|integer| |尚未释放其内存的会话查询进程数。对于未运行的会话，值为 `-1`。|
|`runaway_vmem_mb`|integer| |会话被标记为失控会话时所消耗的 vmem 内存量。|
|`runaway_command_cnt`|integer| |会话被标记为失控会话时的命令计数。|
|`idle_start`|timestamptz| |该会话中的查询进程上次变为空闲的时间。|

## 查看并记录每个进程的内存使用信息 {#view-and-log-per-process-memory-usage-information}

Apache Cloudberry 在内存上下文中分配所有内存。内存上下文便于管理需要存活不同时间长度的内存。销毁上下文会释放其中分配的全部内存。

跟踪服务器进程或长时间运行查询使用的内存量，有助于发现潜在内存不足状况的来源。Apache Cloudberry 提供了可用于此目的的系统视图和管理函数。

### 关于 `pg_backend_memory_contexts` 视图 {#about-the-pg_backend_memory_contexts-view}

要显示附加到当前会话的服务器进程中所有活动内存上下文的内存使用情况，请使用 `pg_backend_memory_contexts` 系统视图。此视图限制超级用户访问，但可以向其他角色授予访问权限。

``` sql
SELECT * FROM pg_backend_memory_contexts;
```

### 关于内存上下文管理函数 {#about-the-memory-context-admin-functions}

可以使用系统管理函数 `pg_log_backend_memory_contexts()`，指示 Apache Cloudberry 将 Coordinator 主机上其他会话的内存使用情况转储到服务器日志中。此函数的执行仅限超级用户，不能授予其他角色。

`pg_log_backend_memory_contexts()` 函数的签名如下：

```
pg_log_backend_memory_contexts( pid integer )
```

其中，`pid` 标识要转储其内存上下文的进程。

`pg_log_backend_memory_contexts()` 在本地主机上成功为进程激活内存上下文记录时返回 `t`。激活记录后，Apache Cloudberry 会以 `LOG` 消息级别为每个内存上下文写入一条日志。日志消息根据设置的日志配置出现在服务器日志中；有关更多信息，请参见 PostgreSQL 文档中的[错误报告与日志记录](https://www.postgresql.org/docs/14/runtime-config-logging.html)。*内存上下文日志消息不会发送给客户端*。

<!-- Memory context logging functions that dump memory usage across all Cloudberry segments, or dump usage for a specific segment are named `gp_log_backend_memory_contexts()`.

`gp_log_backend_memory_contexts()` has two signatures:

```
gp_log_backend_memory_contexts( sess_id integer )
gp_log_backend_memory_contexts( sess_id integer, contentId integer )
```

where `sess_id` is the Apache Cloudberry identifier assigned to the session (typically obtained from the `pg_stat_activity` view), and `contentID` in the second signature identifies the segment instance of interest.

When you invoke `gp_log_backend_memory_contexts()` on the Apache Cloudberry coordinator host, it invokes `pg_log_backend_memory_contexts()` on the individual segments, which in turn triggers a memory usage dump to each segment log. The functions return an integer identifying the number of segments on which memory context logging was successfully activated. -->

### 示例日志消息 {#sample-log-messages}

命令：

``` sql
SELECT pg_log_backend_memory_contexts( pg_backend_pid() );
```

会将以下（部分）内存上下文消息转储到本地服务器日志文件：

```
2024-01-16 16:45:57.228512 UTC,"gpadmin","testdb",p16389,th-557447104,"[local]",,2024-01-16 15:57:32 UTC,0,,cmd10,seg-1,,,,sx1,"LOG","00000","logging memory contexts of PID 16389",,,,,,"SELECT pg_log_backend_memory_contexts(pg_backend_pid());",0,,"mcxt.c",1278,
2024-01-16 16:45:57.229275 UTC,"gpadmin","testdb",p16389,th-557447104,"[local]",,2024-01-16 15:57:32 UTC,0,,cmd10,seg-1,,,,sx1,"LOG","00000","level: 0; TopMemoryContext: 108384 total in 6 blocks; 23248 free (21 chunks); 85136 used",,,,,,,0,,"mcxt.c",884,
2024-01-16 16:45:57.229822 UTC,"gpadmin","testdb",p16389,th-557447104,"[local]",,2024-01-16 15:57:32 UTC,0,,cmd10,seg-1,,,,sx1,"LOG","00000","level: 1; pgstat TabStatusArray lookup hash table: 8192 total in 1 blocks; 1416 free (0 chunks); 6776 used",,,,,,,0,,"mcxt.c",884,
2024-01-16 16:45:57.230387 UTC,"gpadmin","testdb",p16389,th-557447104,"[local]",,2024-01-16 15:57:32 UTC,0,,cmd10,seg-1,,,,sx1,"LOG","00000","level: 1; TopTransactionContext: 8192 total in 1 blocks; 7576 free (1 chunks); 616 used",,,,,,,0,,"mcxt.c",884,
2024-01-16 16:45:57.230961 UTC,"gpadmin","testdb",p16389,th-557447104,"[local]",,2024-01-16 15:57:32 UTC,0,,cmd10,seg-1,,,,sx1,"LOG","00000","level: 1; TableSpace cache: 8192 total in 1 blocks; 2056 free (0 chunks); 6136 used",,,,,,,0,,"mcxt.c",884,
```

## 查看查询工作文件使用信息 {#view-query-workfile-usage-information}

Apache Cloudberry 管理模式 `gp_toolkit` 包含显示 Apache Cloudberry 工作文件信息的视图。如果内存不足以在内存中运行查询，Apache Cloudberry 会在磁盘上创建工作文件。这些信息可用于排查和调优查询。还可以使用这些视图中的信息指定 Apache Cloudberry 配置参数 `gp_workfile_limit_per_query` 和 `gp_workfile_limit_per_segment` 的值。

模式 `gp_toolkit` 中的视图如下：

- `gp_workfile_entries` 视图：当前在某个 Segment 上使用磁盘空间存储工作文件的每个运算符一行。
- `gp_workfile_usage_per_query` 视图：当前在某个 Segment 上使用磁盘空间存储工作文件的每个查询一行。
- `gp_workfile_usage_per_segment` 视图：每个 Segment 一行，每行显示当前该 Segment 上工作文件使用的磁盘空间总量。

有关使用 `gp_toolkit` 的信息，请参见[使用 `gp_toolkit`](#use-gp_toolkit)。

## 查看数据库服务器日志文件 {#view-the-database-server-log-files}

Apache Cloudberry 中的每个数据库实例（Coordinator 和 Segment）都运行一个拥有自己服务器日志文件的 PostgreSQL 数据库服务器。日志文件在 Coordinator 数据目录和每个 Segment 数据目录的 `log` 目录中创建。

### 日志文件格式 {#log-file-format}

服务器日志文件以逗号分隔值（CSV）格式写入。某些日志条目不会为所有日志字段提供值。例如，只有与查询工作进程相关的日志条目才会填充 `slice_id`。可以通过查询的会话标识符（`gp_session_id`）和命令标识符（`gp_command_count`）识别特定查询的相关日志条目。

日志中写入以下字段：

|编号|字段名称|数据类型|描述|
|------|----------|---------|-----------|
|1|event\_time|timestamp with time zone|写入日志条目的时间|
|2|user\_name|varchar(100)|数据库用户名|
|3|database\_name|varchar(100)|数据库名称|
|4|process\_id|varchar(10)|系统进程 ID（前缀为 "p"）|
|5|thread\_id|varchar(50)|线程计数（前缀为 "th"）|
|6|remote\_host|varchar(100)|在 Coordinator 上为客户端机器的主机名/地址；在 Segment 上为 Coordinator 的主机名/地址。|
|7|remote\_port|varchar(10)|Segment 或 Coordinator 的端口号|
|8|session\_start\_time|timestamp with time zone|会话连接打开的时间|
|9|transaction\_id|int|Coordinator 上的顶层事务 ID。此 ID 是所有子事务的父事务。|
|10|gp\_session\_id|text|会话标识符编号（前缀为 "con"）|
|11|gp\_command\_count|text|会话中的命令编号（前缀为 "cmd"）|
|12|gp\_segment|text|Segment content 标识符（主 Segment 的前缀为 "seg"，镜像的前缀为 "mir"）。Coordinator 的 content ID 始终为 -1。|
|13|slice\_id|text|Slice ID（正在执行的查询计划部分）|
|14|distr\_tranx\_id|text|分布式事务 ID|
|15|local\_tranx\_id|text|本地事务 ID|
|16|sub\_tranx\_id|text|子事务 ID|
|17|event\_severity|varchar(10)|包括：LOG、ERROR、FATAL、PANIC、DEBUG1、DEBUG2|
|18|sql\_state\_code|varchar(10)|与日志消息关联的 SQL 状态码|
|19|event\_message|text|日志或错误消息文本|
|20|event\_detail|text|与错误或警告消息关联的详细信息文本|
|21|event\_hint|text|与错误或警告消息关联的提示信息文本|
|22|internal\_query|text|内部生成的查询文本|
|23|internal\_query\_pos|int|内部生成的查询文本中的游标索引|
|24|event\_context|text|生成此消息的上下文|
|25|debug\_query\_string|text|用户提供的、包含完整调试详细信息的查询字符串。此字符串可以为内部使用而修改。|
|26|error\_cursor\_pos|int|查询字符串中的游标索引|
|27|func\_name|text|生成此消息的函数|
|28|file\_name|text|消息起源的内部代码文件|
|29|file\_line|int|消息起源的代码文件行号|
|30|stack\_trace|text|与此消息关联的堆栈跟踪文本|

### 搜索 Apache Cloudberry 服务器日志文件 {#search-the-apache-cloudberry-server-log-files}

Apache Cloudberry 提供名为 `gplogfilter` 的工具，可以在 Apache Cloudberry 日志文件中搜索与指定条件匹配的条目。默认情况下，该工具会在默认日志位置搜索 Apache Cloudberry Coordinator 日志文件。例如，要显示 Coordinator 目录下每个日志文件的最后三行：

```shell
gplogfilter -n 3
```

<!-- To search through all segment log files at the same time, run `gplogfilter` through the `gpssh` utility. For example, to display the last 3 lines of each segment log file:

```shell
gpssh -f <seg_host_file>
```

```shell
=> source /usr/local/cloudberry/cloudberry-env.sh
=> gplogfilter -n 3 <seg_host_file>
``` -->

## 使用 `gp_toolkit` {#use-gp_toolkit}

使用 Apache Cloudberry 管理模式 `gp_toolkit` 查询系统目录、日志文件和运行环境，获取系统状态信息。`gp_toolkit` 模式包含多个可通过 SQL 命令访问的视图。所有数据库用户都可以访问 `gp_toolkit` 模式。某些对象需要超级用户权限。可以使用类似以下的命令，将 `gp_toolkit` 模式加入模式搜索路径：

```sql
=> ALTER ROLE myrole SET search_path TO myschema,gp_toolkit;
```

## SQL 标准错误码 {#sql-standard-error-codes}

以下表格列出所有已定义的错误码。其中一些错误码未使用，但由 SQL 标准定义。表中还显示错误类别。每个错误类别都有一个末三位为 `000` 的标准错误码。该错误码仅用于属于该类别、但没有分配更具体错误码的错误条件。

每个错误码对应的 PL/pgSQL 条件名称与表中显示的短语相同，只是将空格替换为下划线。例如，错误码 22012（DIVISION BY ZERO）的条件名称为 `DIVISION_BY_ZERO`。条件名称可以使用大写或小写。

> [!TIP]
> **如何查看错误码**
>
> 在 Apache Cloudberry 中执行 SQL 查询或其他数据库操作时，如果发生错误，系统会返回错误消息。但是，标准错误消息可能不会直接显示 SQLSTATE 错误码。以下是查看这些错误码的一些方法：
>
> - 使用 PL/pgSQL 异常处理。例如：
>
>     ```sql
>     DO $$
>     BEGIN
>     -- Replaces the following SQL with your query
>     EXECUTE 'Your SQL Query';
>     EXCEPTION WHEN OTHERS THEN
>     RAISE NOTICE 'Error code: %', SQLSTATE;
>     END
>     $$;
>     ```
>
> - 检查数据库日志。Apache Cloudberry 会在日志文件中记录包括错误码在内的详细错误信息。根据系统设置，可以在数据库服务器上检查日志文件以获取这些信息。
>
> - 使用高级数据库客户端工具。某些高级数据库客户端或管理工具可能提供更详细的错误报告功能，可以直接显示 SQLSTATE 错误码。
>
> 注意：
>
> 并非所有错误都有特定的 SQLSTATE 错误码。有些错误可能只有一般错误类别码，例如内部错误的 'XX000'。
>
> 使用 PL/pgSQL 异常处理时，请确保 SQL 查询语句正确格式化为字符串，尤其是在动态执行 SQL 语句时。
>
> PL/pgSQL 不识别警告条件名称（与错误条件名称相对）；警告条件属于 00、01 和 02 类。

|错误码|含义|常量|
|----------|-------|--------|
**类别 00**— 成功完成
|00000|SUCCESSFUL COMPLETION|successful_completion|
类别 01 — 警告
|01000|WARNING|warning|
|0100C|DYNAMIC RESULT SETS RETURNED|dynamic\_result\_sets\_returned|
|01008|IMPLICIT ZERO BIT PADDING|implicit\_zero\_bit\_padding|
|01003|NULL VALUE ELIMINATED IN SET FUNCTION|null\_value\_eliminated\_in\_set\_function|
|01007|PRIVILEGE NOT GRANTED|privilege\_not\_granted|
|01006|PRIVILEGE NOT REVOKED|privilege\_not\_revoked|
|01004|STRING DATA RIGHT TRUNCATION|string\_data\_right\_truncation|
|01P01|DEPRECATED FEATURE|deprecated\_feature|
**类别 02** — 无数据（根据 SQL 标准，这也属于警告类别）
|02000|NO DATA|no\_data|
|02001|NO ADDITIONAL DYNAMIC RESULT SETS RETURNED|no\_additional\_dynamic\_result\_sets\_returned|
**类别 03** — SQL 语句尚未完成
|03000|SQL STATEMENT NOT YET COMPLETE|sql\_statement\_not\_yet\_complete|
**类别 08** — 连接异常
|08000|CONNECTION EXCEPTION|connection\_exception|
|08003|CONNECTION DOES NOT EXIST|connection\_does\_not\_exist|
|08006|CONNECTION FAILURE|connection\_failure|
|08001|SQLCLIENT UNABLE TO ESTABLISH SQLCONNECTION|sqlclient\_unable\_to\_establish\_sqlconnection|
|08004|SQLSERVER REJECTED ESTABLISHMENT OF SQLCONNECTION|sqlserver\_rejected\_establishment\_of\_sqlconnection|
|08007|TRANSACTION RESOLUTION UNKNOWN|transaction\_resolution\_unknown|
|08P01|PROTOCOL VIOLATION|protocol\_violation|
**类别 09** — 触发的操作异常
|09000|TRIGGERED ACTION EXCEPTION|triggered\_action\_exception|
**类别 0A** — 不支持的功能
|0A000|FEATURE NOT SUPPORTED|feature\_not\_supported|
**类别 0B** — 无效的事务启动
|0B000|INVALID TRANSACTION INITIATION|invalid\_transaction\_initiation|
**类别 0F** — 定位器异常
|0F000|LOCATOR EXCEPTION|locator\_exception|
|0F001|INVALID LOCATOR SPECIFICATION|invalid\_locator\_specification|
**类别 0L** — 无效授权者
|0L000|INVALID GRANTOR|invalid\_grantor|
|0LP01|INVALID GRANT OPERATION|invalid\_grant\_operation|
**类别 0P** — 无效角色说明
|0P000|INVALID ROLE SPECIFICATION|invalid\_role\_specification|
**类别 21** — 基数违反
|21000|CARDINALITY VIOLATION|cardinality\_violation|
**类别 22** — 数据异常
|22000|DATA EXCEPTION|data\_exception|
|2202E|ARRAY SUBSCRIPT ERROR|array\_subscript\_error|
|22021|CHARACTER NOT IN REPERTOIRE|character\_not\_in\_repertoire|
|22008|DATETIME FIELD OVERFLOW|datetime\_field\_overflow|
|22012|DIVISION BY ZERO|division\_by\_zero|
|22005|ERROR IN ASSIGNMENT|error\_in\_assignment|
|2200B|ESCAPE CHARACTER CONFLICT|escape\_character\_conflict|
|22022|INDICATOR OVERFLOW|indicator\_overflow|
|22015|INTERVAL FIELD OVERFLOW|interval\_field\_overflow|
|2201E|INVALID ARGUMENT FOR LOGARITHM|invalid\_argument\_for\_logarithm|
|2201F|INVALID ARGUMENT FOR POWER FUNCTION|invalid\_argument\_for\_power\_function|
|2201G|INVALID ARGUMENT FOR WIDTH BUCKET FUNCTION|invalid\_argument\_for\_width\_bucket\_function|
|22018|INVALID CHARACTER VALUE FOR CAST|invalid\_character\_value\_for\_cast|
|22007|INVALID DATETIME FORMAT|invalid\_datetime\_format|
|22019|INVALID ESCAPE CHARACTER|invalid\_escape\_character|
|2200D|INVALID ESCAPE OCTET|invalid\_escape\_octet|
|22025|INVALID ESCAPE SEQUENCE|invalid\_escape\_sequence|
|22P06|NONSTANDARD USE OF ESCAPE CHARACTER|nonstandard\_use\_of\_escape\_character|
|22010|INVALID INDICATOR PARAMETER VALUE|invalid\_indicator\_parameter\_value|
|22020|INVALID LIMIT VALUE|invalid\_limit\_value|
|22023|INVALID PARAMETER VALUE|invalid\_parameter\_value|
|2201B|INVALID REGULAR EXPRESSION|invalid\_regular\_expression|
|22009|INVALID TIME ZONE DISPLACEMENT VALUE|invalid\_time\_zone\_displacement\_value|
|2200C|INVALID USE OF ESCAPE CHARACTER|invalid\_use\_of\_escape\_character|
|2200G|MOST SPECIFIC TYPE MISMATCH|most\_specific\_type\_mismatch|
|22004|NULL VALUE NOT ALLOWED|null\_value\_not\_allowed|
|22002|NULL VALUE NO INDICATOR PARAMETER|null\_value\_no\_indicator\_parameter|
|22003|NUMERIC VALUE OUT OF RANGE|numeric\_value\_out\_of\_range|
|22026|STRING DATA LENGTH MISMATCH|string\_data\_length\_mismatch|
|22001|STRING DATA RIGHT TRUNCATION|string\_data\_right\_truncation|
|22011|SUBSTRING ERROR|substring\_error|
|22027|TRIM ERROR|trim\_error|
|22024|UNTERMINATED C STRING|unterminated\_c\_string|
|2200F|ZERO LENGTH CHARACTER STRING|zero\_length\_character\_string|
|22P01|FLOATING POINT EXCEPTION|floating\_point\_exception|
|22P02|INVALID TEXT REPRESENTATION|invalid\_text\_representation|
|22P03|INVALID BINARY REPRESENTATION|invalid\_binary\_representation|
|22P04|BAD COPY FILE FORMAT|bad\_copy\_file\_format|
|22P05|UNTRANSLATABLE CHARACTER|untranslatable\_character|
**类别 23** — 完整性约束违反
|23000|INTEGRITY CONSTRAINT VIOLATION|integrity\_constraint\_violation|
|23001|RESTRICT VIOLATION|restrict\_violation|
|23502|NOT NULL VIOLATION|not\_null\_violation|
|23503|FOREIGN KEY VIOLATION|foreign\_key\_violation|
|23505|UNIQUE VIOLATION|unique\_violation|
|23514|CHECK VIOLATION|check\_violation|
**类别 24** — 无效游标状态
|24000|INVALID CURSOR STATE|invalid\_cursor\_state|
**类别 25** — 无效事务状态
|25000|INVALID TRANSACTION STATE|invalid\_transaction\_state|
|25001|ACTIVE SQL TRANSACTION|active\_sql\_transaction|
|25002|BRANCH TRANSACTION ALREADY ACTIVE|branch\_transaction\_already\_active|
|25008|HELD CURSOR REQUIRES SAME ISOLATION LEVEL|held\_cursor\_requires\_same\_isolation\_level|
|25003|INAPPROPRIATE ACCESS MODE FOR BRANCH TRANSACTION|inappropriate\_access\_mode\_for\_branch\_transaction|
|25004|INAPPROPRIATE ISOLATION LEVEL FOR BRANCH TRANSACTION|inappropriate\_isolation\_level\_for\_branch\_transaction|
|25005|NO ACTIVE SQL TRANSACTION FOR BRANCH TRANSACTION|no\_active\_sql\_transaction\_for\_branch\_transaction|
|25006|READ ONLY SQL TRANSACTION|read\_only\_sql\_transaction|
|25007|SCHEMA AND DATA STATEMENT MIXING NOT SUPPORTED|schema\_and\_data\_statement\_mixing\_not\_supported|
|25P01|NO ACTIVE SQL TRANSACTION|no\_active\_sql\_transaction|
|25P02|IN FAILED SQL TRANSACTION|in\_failed\_sql\_transaction|
**类别 26** — 无效 SQL 语句名称
|26000|INVALID SQL STATEMENT NAME|invalid\_sql\_statement\_name|
**类别 27** — 触发的数据变更违反
|27000|TRIGGERED DATA CHANGE VIOLATION|triggered\_data\_change\_violation|
**类别 28** — 无效授权说明
|28000|INVALID AUTHORIZATION SPECIFICATION|invalid\_authorization\_specification|
**类别 2B** — 依赖的权限描述符仍存在
|2B000|DEPENDENT PRIVILEGE DESCRIPTORS STILL EXIST|dependent\_privilege\_descriptors\_still\_exist|
|2BP01|DEPENDENT OBJECTS STILL EXIST|dependent\_objects\_still\_exist|
**类别 2D** — 无效事务终止
|2D000|INVALID TRANSACTION TERMINATION|invalid\_transaction\_termination|
**类别 2F** — SQL 例程异常
|2F000|SQL ROUTINE EXCEPTION|sql\_routine\_exception|
|2F005|FUNCTION EXECUTED NO RETURN STATEMENT|function\_executed\_no\_return\_statement|
|2F002|MODIFYING SQL DATA NOT PERMITTED|modifying\_sql\_data\_not\_permitted|
|2F003|PROHIBITED SQL STATEMENT ATTEMPTED|prohibited\_sql\_statement\_attempted|
|2F004|READING SQL DATA NOT PERMITTED|reading\_sql\_data\_not\_permitted|
**类别 34** — 无效游标名称
|34000|INVALID CURSOR NAME|invalid\_cursor\_name|
**类别 38** — 外部例程异常
|38000|EXTERNAL ROUTINE EXCEPTION|external\_routine\_exception|
|38001|CONTAINING SQL NOT PERMITTED|containing\_sql\_not\_permitted|
|38002|MODIFYING SQL DATA NOT PERMITTED|modifying\_sql\_data\_not\_permitted|
|38003|PROHIBITED SQL STATEMENT ATTEMPTED|prohibited\_sql\_statement\_attempted|
|38004|READING SQL DATA NOT PERMITTED|reading\_sql\_data\_not\_permitted|
**类别 39** — 外部例程调用异常
|39000|EXTERNAL ROUTINE INVOCATION EXCEPTION|external\_routine\_invocation\_exception|
|39001|INVALID SQLSTATE RETURNED|invalid\_sqlstate\_returned|
|39004|NULL VALUE NOT ALLOWED|null\_value\_not\_allowed|
|39P01|TRIGGER PROTOCOL VIOLATED|trigger\_protocol\_violated|
|39P02|SRF PROTOCOL VIOLATED|srf\_protocol\_violated|
**类别 3B** — 保存点异常
|3B000|SAVEPOINT EXCEPTION|savepoint\_exception|
|3B001|INVALID SAVEPOINT SPECIFICATION|invalid\_savepoint\_specification|
**类别 3D** — 无效目录名称
|3D000|INVALID CATALOG NAME|invalid\_catalog\_name|
**类别 3F** — 无效模式名称
|3F000|INVALID SCHEMA NAME|invalid\_schema\_name|
**类别 40** — 事务回滚
|40000|TRANSACTION ROLLBACK|transaction\_rollback|
|40002|TRANSACTION INTEGRITY CONSTRAINT VIOLATION|transaction\_integrity\_constraint\_violation|
|40001|SERIALIZATION FAILURE|serialization\_failure|
|40003|STATEMENT COMPLETION UNKNOWN|statement\_completion\_unknown|
|40P01|DEADLOCK DETECTED|deadlock\_detected|
**类别 42** — 语法错误或访问规则违反
|42000|SYNTAX ERROR OR ACCESS RULE VIOLATION|syntax\_error\_or\_access\_rule\_violation|
|42601|SYNTAX ERROR|syntax\_error|
|42501|INSUFFICIENT PRIVILEGE|insufficient\_privilege|
|42846|CANNOT COERCE|cannot\_coerce|
|42803|GROUPING ERROR|grouping\_error|
|42830|INVALID FOREIGN KEY|invalid\_foreign\_key|
|42602|INVALID NAME|invalid\_name|
|42622|NAME TOO LONG|name\_too\_long|
|42939|RESERVED NAME|reserved\_name|
|42804|DATATYPE MISMATCH|datatype\_mismatch|
|42P18|INDETERMINATE DATATYPE|indeterminate\_datatype|
|42809|WRONG OBJECT TYPE|wrong\_object\_type|
|42703|UNDEFINED COLUMN|undefined\_column|
|42883|UNDEFINED FUNCTION|undefined\_function|
|42P01|UNDEFINED TABLE|undefined\_table|
|42P02|UNDEFINED PARAMETER|undefined\_parameter|
|42704|UNDEFINED OBJECT|undefined\_object|
|42701|DUPLICATE COLUMN|duplicate\_column|
|42P03|DUPLICATE CURSOR|duplicate\_cursor|
|42P04|DUPLICATE DATABASE|duplicate\_database|
|42723|DUPLICATE FUNCTION|duplicate\_function|
|42P05|DUPLICATE PREPARED STATEMENT|duplicate\_prepared\_statement|
|42P06|DUPLICATE SCHEMA|duplicate\_schema|
|42P07|DUPLICATE TABLE|duplicate\_table|
|42712|DUPLICATE ALIAS|duplicate\_alias|
|42710|DUPLICATE OBJECT|duplicate\_object|
|42702|AMBIGUOUS COLUMN|ambiguous\_column|
|42725|AMBIGUOUS FUNCTION|ambiguous\_function|
|42P08|AMBIGUOUS PARAMETER|ambiguous\_parameter|
|42P09|AMBIGUOUS ALIAS|ambiguous\_alias|
|42P10|INVALID COLUMN REFERENCE|invalid\_column\_reference|
|42611|INVALID COLUMN DEFINITION|invalid\_column\_definition|
|42P11|INVALID CURSOR DEFINITION|invalid\_cursor\_definition|
|42P12|INVALID DATABASE DEFINITION|invalid\_database\_definition|
|42P13|INVALID FUNCTION DEFINITION|invalid\_function\_definition|
|42P14|INVALID PREPARED STATEMENT DEFINITION|invalid\_prepared\_statement\_definition|
|42P15|INVALID SCHEMA DEFINITION|invalid\_schema\_definition|
|42P16|INVALID TABLE DEFINITION|invalid\_table\_definition|
|42P17|INVALID OBJECT DEFINITION|invalid\_object\_definition|
**类别 44** — WITH CHECK OPTION 违反
|44000|WITH CHECK OPTION VIOLATION|with\_check\_option\_violation|
**类别 53** — 资源不足
|53000|INSUFFICIENT RESOURCES|insufficient\_resources|
|53100|DISK FULL|disk\_full|
|53200|OUT OF MEMORY|out\_of\_memory|
|53300|TOO MANY CONNECTIONS|too\_many\_connections|
**类别 54** — 超出程序限制
|54000|PROGRAM LIMIT EXCEEDED|program\_limit\_exceeded|
|54001|STATEMENT TOO COMPLEX|statement\_too\_complex|
|54011|TOO MANY COLUMNS|too\_many\_columns|
|54023|TOO MANY ARGUMENTS|too\_many\_arguments|
**类别 55** — 对象不在先决状态
|55000|OBJECT NOT IN PREREQUISITE STATE|object\_not\_in\_prerequisite\_state|
|55006|OBJECT IN USE|object\_in\_use|
|55P02|CANT CHANGE RUNTIME PARAM|cant\_change\_runtime\_param|
|55P03|LOCK NOT AVAILABLE|lock\_not\_available|
**类别 57** — 运算符干预
|57000|OPERATOR INTERVENTION|operator\_intervention|
|57014|QUERY CANCELED|query\_canceled|
|57P01|ADMIN SHUTDOWN|admin\_shutdown|
|57P02|CRASH SHUTDOWN|crash\_shutdown|
|57P03|CANNOT CONNECT NOW|cannot\_connect\_now|
**类别 58** — 系统错误（Apache Cloudberry 外部的错误）
|58030|IO ERROR|io\_error|
|58P01|UNDEFINED FILE|undefined\_file|
|58P02|DUPLICATE FILE|duplicate\_file|
类别 F0 — 配置文件错误
|F0000|CONFIG FILE ERROR|config\_file\_error|
|F0001|LOCK FILE EXISTS|lock\_file\_exists|
**类别 P0** — PL/pgSQL 错误
|P0000|PLPGSQL ERROR|plpgsql\_error|
|P0001|RAISE EXCEPTION|raise\_exception|
|P0002|NO DATA FOUND|no\_data\_found|
|P0003|TOO MANY ROWS|too\_many\_rows|
**类别 XX** — 内部错误
|XX000|INTERNAL ERROR|internal\_error|
|XX001|DATA CORRUPTED|data\_corrupted|
|XX002|INDEX CORRUPTED|index\_corrupted|
