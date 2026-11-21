---
title: diskquota
description: diskquota 允许管理员限制数据库中模式、角色或表空间使用的磁盘空间。
weight: 50
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/diskquota.md
---

`diskquota` 模块让 Apache Cloudberry 管理员可以限制数据库中模式、角色或表空间使用的磁盘空间。

Apache Cloudberry 在源码的 `gpcontrib/diskquota` 目录中包含 `diskquota` 2.3。

## 安装 {#installation}

### 构建模块 {#build-the-module}

`diskquota` 默认不构建。要随 Apache Cloudberry 构建并安装此模块，在运行 `configure` 时指定 `--with-diskquota` 选项：

```shell
./configure --with-diskquota [other options...]
make
make install
```

此模块使用 CMake 构建，因此构建主机上必须安装 `cmake`。

### 启用模块 {#enable-the-module}

使用此模块之前，执行以下步骤：

1. 创建 `diskquota` 数据库。模块使用此数据库存储已启用模块的数据库列表。

    ```shell
    createdb diskquota
    ```

2. 将 `diskquota-2.3` 共享库加入服务器配置参数 `shared_preload_libraries`，并重启 Apache Cloudberry。务必保留该配置参数原有的设置。例如：

    ```shell
    gpconfig -s shared_preload_libraries
    gpconfig -c shared_preload_libraries -v 'diskquota-2.3'
    gpstop -ar
    ```

    如果 `shared_preload_libraries` 已包含其他库，请指定逗号分隔的列表，例如 `'auto_explain,diskquota-2.3'`。

3. 在每个需要执行磁盘使用配额限制的数据库中创建 `diskquota` 扩展。`diskquota.max_monitored_databases` 参数限制可创建此扩展的数据库数量（默认为 `50`）。

    ```sql
    CREATE EXTENSION diskquota;
    ```

4. 如果创建扩展时数据库非空，`diskquota` 会发出以下警告。运行 `diskquota.init_table_size_table()` 函数计算已有表的大小。数据库中文件较多时，此操作可能需要一些时间。

    ```
    WARNING:  [diskquota] diskquota is not ready because current database is not empty
    HINT:  please run 'SELECT diskquota.init_table_size_table();' to initialize diskquota
    ```

    ```sql
    SELECT diskquota.init_table_size_table();
    ```

> [!NOTE]
> 必须通过 `shared_preload_libraries` 加载此库。否则，模块函数会报错，指出 `diskquota-2.3` 不在 `shared_preload_libraries` 中。

`gpconfig` 和 `gpstop` 工具的更多信息，参见 [gpconfig](/cloudberry/reference/sys-utilities/gpconfig/) 和 [gpstop](/cloudberry/reference/sys-utilities/gpstop/)。

## 关于 diskquota 模块 {#about-the-diskquota-module}

表的磁盘使用量包括表数据、索引、TOAST 表和空闲空间映射。对于 AO 表，计算还包括可见性映射和块目录表等辅助表。

可以使用 `diskquota` 模块设置以下配额：

- 模式磁盘配额限制数据库中特定模式下所有表可使用的磁盘空间。模式的磁盘使用量是该模式中所有表在所有 Segment 上的磁盘使用量之和。
- 角色磁盘配额限制数据库中特定角色所拥有的所有表可使用的磁盘空间。角色的磁盘使用量是该角色拥有的所有表在所有 Segment 上的磁盘使用量之和。虽然角色是集群级对象，但角色的配额上限和磁盘使用量分别按数据库计算。
- 模式表空间磁盘配额限制数据库中特定模式、特定表空间中的所有表可使用的磁盘空间。
- 角色表空间磁盘配额限制数据库中特定角色在特定表空间中拥有的所有表可使用的磁盘空间。
- 逐 Segment 表空间磁盘配额在已为模式或角色设置表空间配额时，限制单个 Segment 可使用的磁盘空间。

> [!NOTE]
> 不能为系统所有者（即初始化集群的引导超级用户）设置角色磁盘配额。

每个数据库在 `diskquota.quota_config` 表中存储和管理自身的配额配置。

## diskquota 如何监控磁盘使用量 {#how-diskquota-monitors-disk-usage}

`diskquota` 基于后台工作进程框架。Coordinator 上运行一个 `diskquota` 启动器进程，它为已创建扩展的数据库在 Coordinator 上启动 `diskquota` 工作进程。Segment 上不运行启动器或工作进程。

工作进程监控其数据库中模式、角色和表空间的磁盘使用量。各 Segment 上存储管理器的钩子记录文件被创建、扩展或截断的表，称为活跃表。工作进程定期向 Segment 查询活跃表的大小，更新相应模式和角色的磁盘使用量，并与配额上限比较。超出配额时，工作进程将该模式、角色或表空间放入共享内存中的拒绝映射（reject map）。

`diskquota` 可以执行磁盘使用量的软限制和硬限制：

- `diskquota` 始终执行软限制。查询运行前检查拒绝映射。如果新增数据的查询所针对的模式、角色或表空间在拒绝映射中，查询会在开始前被取消，并报错说明配额已超出。如果查询开始时未超出配额，则允许运行，即使最终导致超出配额也是如此。
- 启用硬限制后，`diskquota` 还会在查询执行期间检查磁盘使用量。如果查询运行期间超出磁盘配额，`diskquota` 会终止查询。硬限制默认关闭。参见 [diskquota.hard_limit](#diskquotahard_limit)。

达到配额后，将模式或角色加入拒绝映射会有一定延迟，因为工作进程定期重新计算表大小（默认每两秒一次）。在此期间，其他查询仍可增加数据。当 `DROP`、`TRUNCATE` 或 `VACUUM FULL` 等移除数据的操作使磁盘使用量降到配额以下时，也存在同样的延迟。参见 [diskquota.naptime](#diskquotanaptime)。

删除行或对表运行 `VACUUM` 不会释放磁盘空间，因此仅执行这些操作不能将模式或角色移出拒绝映射。要减小表占用的磁盘空间，请运行 `VACUUM FULL` 或 `TRUNCATE TABLE`。

如果已创建扩展的数据库数量大于 `diskquota.max_workers`，启动器会动态启动和停止工作进程，让数据库共享可用的工作进程。

## 函数与视图 {#functions-and-views}

模块的函数和视图位于 `diskquota` 模式中。

只有超级用户可以运行设置配额的函数，以及 `pause()` 和 `resume()` 函数。

| 函数 | 说明 |
|---|---|
| `void init_table_size_table()` | 计算当前数据库中已有表的大小。 |
| `void set_schema_quota(schema_name text, quota text)` | 设置当前数据库中某个模式的磁盘配额。 |
| `void set_role_quota(role_name text, quota text)` | 设置当前数据库中某个角色的磁盘配额。 |
| `void set_schema_tablespace_quota(schema_name text, tablespace_name text, quota text)` | 设置当前数据库中某个模式与表空间组合的磁盘配额。 |
| `void set_role_tablespace_quota(role_name text, tablespace_name text, quota text)` | 设置当前数据库中某个角色与表空间组合的磁盘配额。 |
| `void set_per_segment_quota(tablespace_name text, ratio float4)` | 设置当前数据库中某个表空间的逐 Segment 磁盘配额比例。 |
| `void pause()` | 继续统计当前数据库的磁盘使用量，但停止在超出上限时报错。 |
| `void resume()` | 恢复在当前数据库磁盘使用量超出上限时报错。 |
| `status()` | 返回含 `name` 和 `status` 列的表，显示当前数据库的软限制和硬限制状态，以及 `diskquota` 的二进制和模式版本。 |
| `bigint relation_size(relation regclass)` | 返回 `diskquota` 计算得到的关系在所有 Segment 上的大小。 |
| `boolean wait_for_worker_new_epoch()` | 等待当前数据库的工作进程完成新一轮磁盘使用量刷新。 |

| 视图 | 说明 |
|---|---|
| `show_fast_database_size_view` | 显示当前数据库的磁盘空间使用量。 |
| `show_fast_schema_quota_view` | 列出当前数据库中模式的配额与磁盘使用量。 |
| `show_fast_role_quota_view` | 列出当前数据库中角色的配额与磁盘使用量。 |
| `show_fast_schema_tablespace_quota_view` | 按表空间列出当前数据库中模式的配额与磁盘使用量。 |
| `show_fast_role_tablespace_quota_view` | 按表空间列出当前数据库中角色的配额与磁盘使用量。 |
| `show_segment_ratio_quota_view` | 显示当前数据库中已设置比例的表空间的逐 Segment 配额比例。 |
| `rejectmap` | 列出拒绝映射中的条目。 |

## 配置参数 {#configuration-parameters}

模块定义以下服务器配置参数，使用 `gpconfig` 工具设置。标为“重启”的参数在重启集群（`gpstop -ar`）后生效；标为“重新加载”的参数在重新加载配置（`gpstop -u`）后生效。

| 参数 | 默认值 | 生效方式 | 说明 |
|---|---|---|---|
| `diskquota.naptime` | `2` | 重新加载 | `diskquota` 重新计算表大小的间隔，单位为秒。 |
| `diskquota.hard_limit` | `off` | 重新加载 | 启用或禁用磁盘使用量硬限制。 |
| `diskquota.worker_timeout` | `60` | 重新加载 | `diskquota.wait_for_worker_new_epoch()` 等待工作进程超过此时长后，会发出超时通知，单位为秒。 |
| `diskquota.max_workers` | `10` | 重启 | 可同时运行的 `diskquota` 工作进程数上限，最大值为 `20`。 |
| `diskquota.max_active_tables` | `307200` (`300 * 1024`) | 重启 | `diskquota` 可同时跟踪的活跃关系（表、索引等）数量上限。 |
| `diskquota.max_table_segments` | `10485760` (`10 * 1024 * 1024`) | 重启 | 集群中表段的数量上限。 |
| `diskquota.max_monitored_databases` | `50` | 重启 | `diskquota` 可监控的数据库数量上限，最大值为 `1024`。 |
| `diskquota.max_quota_probes` | `1048576` (`1024 * 1024`) | 重启 | 集群中配额探针的数量上限。 |

### diskquota.naptime {#diskquotanaptime}

`diskquota.naptime` 值越小，检测到磁盘使用量变化的延迟越短。以下示例将其设为十秒：

```shell
gpconfig -c diskquota.naptime -v 10
gpstop -u
```

### diskquota.hard_limit {#diskquotahard_limit}

启用硬限制后，`diskquota` 在查询执行期间检查配额。如果运行中的查询超出配额上限，`diskquota` 会终止查询。

要为所有数据库启用硬限制，将此参数设为 `on` 并重新加载配置：

```shell
gpconfig -c diskquota.hard_limit -v 'on'
gpstop -u
```

运行以下查询查看硬限制设置：

```sql
SELECT * FROM diskquota.status();
```

### diskquota.max_workers {#diskquotamax_workers}

此参数指定可同时运行的最大工作进程数，不包含启动器进程。`diskquota` 工作进程取自服务器配置参数 `max_worker_processes` 确定的工作进程池，因此 `diskquota.max_workers` 应小于 `max_worker_processes`。

### diskquota.max_active_tables {#diskquotamax_active_tables}

活跃表是自 `diskquota` 上次重新计算表大小以来，大小可能发生变化的表。活跃表列表存放在服务器启动时分配的共享内存中。如果活跃表共享内存已满，`diskquota` 可能无法及时检测相应的磁盘使用量变化。

### diskquota.max_table_segments {#diskquotamax_table_segments}

一张表（包括分区表的每张子表）分布在所有 Segment 上。`diskquota` 将表在每个 Segment 上的部分计为一个表段（table segment）。因此，此参数限制 `diskquota` 可监控的表数量。

扩容集群时，每张表消耗更多表段，会降低 `diskquota` 能支持的表数量。如果出现以下警告，请增大 `diskquota.max_table_segments`，然后重启 Apache Cloudberry：

```
WARNING:  [diskquota] the number of tables exceeds the limit, please increase the GUC value for diskquota.max_table_segments. Current diskquota.max_table_segments value: 10485760
```

## 使用 diskquota 模块 {#use-the-diskquota-module}

### 查看 diskquota 状态 {#view-the-diskquota-status}

调用 `status()` 函数，查看当前数据库的软限制和硬限制状态，以及 `diskquota` 的版本号：

```sql
SELECT * FROM diskquota.status();
```

```
          name          | status
------------------------+--------
 soft limits            | on
 hard limits            | off
 current binary version | 2.3.0
 current schema version | 2.3
(4 rows)
```

数据库中的 `diskquota` 暂停时，`soft limits` 状态为 `paused`；如果启用了硬限制，`hard limits` 状态也为 `paused`。

### 暂停和恢复配额限制 {#pause-and-resume-quota-enforcement}

要在一段时间内停止对当前数据库报告超出配额的错误，先暂停、再恢复 `diskquota`：

```sql
SELECT diskquota.pause();
-- Perform the operations for which quotas should not be enforced.
SELECT diskquota.resume();
```

暂停期间，`diskquota` 仍继续统计磁盘使用量。

### 设置模式或角色磁盘配额 {#set-a-schema-or-role-disk-quota}

使用 `diskquota.set_schema_quota()` 和 `diskquota.set_role_quota()` 函数设置、更新或删除当前数据库中模式和角色的磁盘配额上限。两个参数分别为模式或角色名称，以及要设置的配额。配额使用 MB、GB、TB 或 PB 单位，例如 `'2TB'`。不带单位的数字按 MB 解释，不允许配额为 `0`。

函数会将模式或角色名称转换为小写，除非在字符串内部用双引号括起名称，例如 `'"MyRole"'`。

以下示例为 `acct` 模式设置 250GB 配额：

```sql
SELECT diskquota.set_schema_quota('acct', '250GB');
```

以下示例为 `nickd` 角色设置 500MB 配额：

```sql
SELECT diskquota.set_role_quota('nickd', '500MB');
```

要更改配额，使用新的配额值再次调用函数。

要移除模式或角色配额，将配额值设为 `'-1'`。

### 为模式或角色设置表空间磁盘配额 {#set-a-tablespace-disk-quota-for-a-schema-or-role}

使用 `diskquota.set_schema_tablespace_quota()` 和 `diskquota.set_role_tablespace_quota()` 函数设置、更新或删除当前数据库中模式和角色的逐表空间磁盘配额上限。三个参数分别为模式或角色名称、表空间名称，以及要设置的配额。

以下示例为 `tspaced1` 表空间中的 `acct` 模式设置 250GB 磁盘配额：

```sql
SELECT diskquota.set_schema_tablespace_quota('acct', 'tspaced1', '250GB');
```

以下示例为 `tspaced2` 表空间中的 `nickd` 角色设置 500MB 磁盘配额：

```sql
SELECT diskquota.set_role_tablespace_quota('nickd', 'tspaced2', '500MB');
```

要更改配额，使用新的配额值再次调用函数。

要移除模式或角色的表空间配额，将配额值设为 `'-1'`。

### 设置逐 Segment 表空间磁盘配额 {#set-a-per-segment-tablespace-disk-quota}

为模式或角色设置表空间配额时，还可以为该表空间定义逐 Segment 配额。逐 Segment 配额限制表空间在单个 Segment 上可消耗的磁盘空间，有助于防止数据倾斜导致某个 Segment 的磁盘写满。

使用 `diskquota.set_per_segment_quota()` 函数设置、更新或删除逐 Segment 表空间配额。两个参数分别为表空间名称和一个比例。该比例表示单个 Segment 可使用的磁盘配额相对于平均 Segment 配额的倍数。不允许比例为 `0`。

平均 Segment 配额的计算方式如下：

```
avg_seg_quota = tablespace_quota / number_of_segments
```

例如，集群有 8 个 Segment，设置以下模式表空间配额后，`tspaced1` 表空间的平均 Segment 配额为 `800GB / 8 = 100GB`：

```sql
SELECT diskquota.set_schema_tablespace_quota('accts', 'tspaced1', '800GB');
```

随后设置以下逐 Segment 比例，则每个 Segment 允许的最大磁盘使用量为 `100GB * 2.0 = 200GB`：

```sql
SELECT diskquota.set_per_segment_quota('tspaced1', '2.0');
```

要更改比例，使用新值再次调用函数。要移除逐 Segment 表空间配额，将比例设为 `'-1'`。

查询 `show_segment_ratio_quota_view` 视图，查看表空间已设置的逐 Segment 配额比例：

```sql
SELECT tablespace_name, per_seg_quota_ratio
  FROM diskquota.show_segment_ratio_quota_view WHERE tablespace_name IN ('tspaced1');
```

```
 tablespace_name | per_seg_quota_ratio
-----------------+---------------------
 tspaced1        |                   2
(1 row)
```

### 显示磁盘配额与磁盘使用量 {#display-disk-quotas-and-disk-usage}

`diskquota.show_fast_schema_quota_view` 视图列出当前数据库的模式配额。`nspsize_in_bytes` 列包含计算得到的该模式下所有表的大小。

```sql
SELECT * FROM diskquota.show_fast_schema_quota_view;
```

```
 schema_name | schema_oid | quota_in_mb | nspsize_in_bytes
-------------+------------+-------------+------------------
 acct        |      16561 |      256000 |           131072
 public      |       2200 |         250 |          3014656
(2 rows)
```

`diskquota.show_fast_role_quota_view` 视图列出当前数据库的角色配额。`rolsize_in_bytes` 列包含计算得到的该角色拥有的所有表的大小。

```sql
SELECT * FROM diskquota.show_fast_role_quota_view;
```

```
 role_name | role_oid | quota_in_mb | rolsize_in_bytes
-----------+----------+-------------+------------------
 mdach     |    16558 |         500 |           131072
 nickd     |    16577 |         500 |        144670720
(2 rows)
```

要查看模式和角色的逐表空间磁盘配额，查询 `diskquota.show_fast_schema_tablespace_quota_view` 和 `diskquota.show_fast_role_tablespace_quota_view` 视图。例如：

```sql
SELECT schema_name, tablespace_name, quota_in_mb, nspsize_tablespace_in_bytes
   FROM diskquota.show_fast_schema_tablespace_quota_view
   WHERE schema_name = 'acct' AND tablespace_name = 'tspaced1';
```

### 列出 diskquota 监控的数据库 {#identify-the-diskquota-monitored-databases}

运行以下命令，获取集群中 `diskquota` 监控的数据库列表：

```sql
\c diskquota
SELECT d.datname FROM diskquota_namespace.database_list q, pg_database d
    WHERE q.dbid = d.oid ORDER BY d.datname;
```

## 说明与限制 {#notes-and-limitations}

- 删除数据库之前，先删除其中的 `diskquota` 扩展。每个已创建扩展的数据库都有 `diskquota` 工作进程与之连接。
- `diskquota` 也统计临时表的磁盘使用量。临时表大小计入表所有者角色的使用量，不计入当前模式，因为临时表位于临时模式中。
- 拒绝映射的共享内存已满时，即使某些模式或角色已达到配额上限，仍可能继续加载数据。

## 示例 {#examples}

### 设置模式配额 {#set-a-schema-quota}

此示例配置模式配额，展示向模式添加数据时的软限制行为。假定已预加载 `diskquota` 库，且 `diskquota` 数据库已存在。

1. 创建名为 `testdb` 的数据库，并连接它。

    ```shell
    createdb testdb
    psql -d testdb
    ```

2. 在数据库中创建 `diskquota` 扩展。

    ```sql
    CREATE EXTENSION diskquota;
    ```

3. 创建名为 `s1` 的模式。

    ```sql
    CREATE SCHEMA s1;
    ```

4. 为 `s1` 模式设置 1MB 磁盘配额。

    ```sql
    SELECT diskquota.set_schema_quota('s1', '1 MB');
    ```

5. 在 `s1` 模式中创建表并插入少量数据。该模式尚无数据，因此不在拒绝映射中。

    ```sql
    SET search_path TO s1;
    CREATE TABLE a(i int) DISTRIBUTED BY (i);
    INSERT INTO a SELECT generate_series(1,100);
    ```

6. 插入足以超过模式 1MB 配额的大量数据。执行 `INSERT` 命令前，`s1` 模式不在拒绝映射中，因此只有软限制生效时，即使命令会超出模式上限，也允许运行。

    ```sql
    INSERT INTO a SELECT generate_series(1,10000000);
    ```

7. 尝试插入少量数据。由于上一条命令超出了模式的磁盘配额，模式已在拒绝映射中，任何加载数据的命令都会被取消。

    ```sql
    INSERT INTO a SELECT generate_series(1,100);
    ```

    ```
    ERROR:  schema's disk space quota exceeded with name: s1
    ```

8. 将配额设为 `-1`，移除 `s1` 模式的配额，再次插入少量数据。`INSERT` 命令前休眠 5 秒，确保命令运行前拒绝映射已更新。

    ```sql
    SELECT diskquota.set_schema_quota('s1', '-1');
    SELECT pg_sleep(5);
    INSERT INTO a SELECT generate_series(1,100);
    ```

### 启用硬限制 {#enable-hard-limit-enforcement}

此示例启用磁盘使用量硬限制，并重新运行上一个示例的命令。开始前，清空上一示例中的表，使模式再次处于配额以内：

```sql
TRUNCATE s1.a;
SELECT diskquota.wait_for_worker_new_epoch();
```

1. 启用硬限制。

    ```shell
    gpconfig -c diskquota.hard_limit -v 'on'
    gpstop -u
    ```

2. 查看硬限制设置。

    ```sql
    SELECT * FROM diskquota.status();
    ```

3. 再次为 `s1` 模式设置 1MB 磁盘配额。

    ```sql
    SELECT diskquota.set_schema_quota('s1', '1 MB');
    ```

4. 插入足以超过模式 1MB 配额的大量数据。执行 `INSERT` 命令前，`s1` 模式不在拒绝映射中，因此命令可以开始执行。操作超出模式配额时，`diskquota` 会终止查询，报错类似于 `schema's disk space quota exceeded with name: 17952`。启用硬限制时，错误报告的是模式 OID，而非名称。

    ```sql
    INSERT INTO a SELECT generate_series(1,10000000);
    ```

5. 移除 `s1` 模式的配额，并等待拒绝映射更新：

    ```sql
    SELECT diskquota.set_schema_quota('s1', '-1');
    SELECT diskquota.wait_for_worker_new_epoch();
    ```

### 设置逐 Segment 表空间配额 {#set-a-per-segment-tablespace-quota}

此示例配置表空间配额和逐 Segment 表空间配额。使用前面示例中的 `testdb` 数据库和 `s1` 模式，并假定集群中存在名为 `tbsp1` 的表空间。

1. 为 `tbsp1` 表空间中的 `s1` 模式设置 10MB 磁盘配额。

    ```sql
    SELECT diskquota.set_schema_tablespace_quota('s1', 'tbsp1', '10 MB');
    ```

2. 在 `tbsp1` 表空间中创建名为 `b` 的表，并插入一些数据。数据未超出 10MB 配额。

    ```sql
    SET search_path TO s1;
    CREATE TABLE b(i int) TABLESPACE tbsp1 DISTRIBUTED BY (i);
    INSERT INTO b SELECT generate_series(1,100000);
    ```

3. 将 `tbsp1` 表空间的逐 Segment 比例设为 `0.1`。此时，单个 Segment 最多可使用平均 Segment 配额乘以 `0.1` 的空间，小于表在某个 Segment 上已使用的空间。

    ```sql
    SELECT diskquota.set_per_segment_quota('tbsp1', 0.1);
    ```

4. 等待 `diskquota` 刷新磁盘使用量，然后尝试插入更多数据。由于超出了逐 Segment 表空间配额，命令被取消。

    ```sql
    SELECT diskquota.wait_for_worker_new_epoch();
    INSERT INTO b SELECT generate_series(1,100);
    ```

    ```
    ERROR:  tablespace: tbsp1, schema: s1 diskquota exceeded per segment quota
    ```
