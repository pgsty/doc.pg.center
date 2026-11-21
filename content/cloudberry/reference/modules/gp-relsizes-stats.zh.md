---
title: gp_relsizes_stats
description: gp_relsizes_stats 收集并存储 Apache Cloudberry 关系文件的磁盘大小。
weight: 110
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/gp-relsizes-stats.md
---

`gp_relsizes_stats` 模块收集并存储 Apache Cloudberry 关系文件的磁盘大小。它扫描各个 Segment 上的数据库目录，记录每个关系文件的大小和修改时间，并提供按表和模式汇总这些数据的视图。

可以由后台工作进程定期收集统计信息，也可以调用函数按需收集。休眠时间参数允许将文件扫描分散到一段时间内，限制 I/O 负载。

## 构建与安装 {#build-and-install}

`gp_relsizes_stats` 默认随 Apache Cloudberry 构建和安装，不需要任何 `configure` 选项。

要从源码树中只构建并安装此模块：

```shell
make -C gpcontrib/gp_relsizes_stats
make -C gpcontrib/gp_relsizes_stats install
```

## 启用模块 {#enable-the-module}

1. 将库加入 `shared_preload_libraries` 并重启集群。只有预加载此库时，才会注册定期执行的后台工作进程：

    ```shell
    gpconfig -c shared_preload_libraries -v "'gp_relsizes_stats'" --skipvalidation
    gpstop -ra
    ```

    如果 `shared_preload_libraries` 已列出其他库，请在其值中保留它们。

2. 在每个需要收集统计信息的数据库中创建扩展：

    ```sql
    CREATE EXTENSION gp_relsizes_stats;
    ```

    此扩展标为可信，因此拥有数据库 `CREATE` 权限的非超级用户也可以创建。扩展会创建 `relsizes_stats_schema` 模式。创建扩展的角色获得该模式的 `USAGE` 权限，以及其中表和视图的 `SELECT` 权限，均带有转授权能力。

3. 可选：启用定期收集。此功能默认关闭：

    ```shell
    gpconfig -c gp_relsizes_stats.enabled -v on --skipvalidation
    gpstop -u
    ```

## 收集过程 {#how-collection-works}

- 主后台工作进程连接 `postgres` 数据库。`gp_relsizes_stats.enabled` 开启时，它执行一轮收集，然后休眠 `gp_relsizes_stats.restart_naptime` 指定的时长。
- 每轮收集遍历除 `template0`、`template1`、`diskquota` 和 `gpperfmon` 之外的所有数据库，为每个数据库启动一个动态后台工作进程。未创建此扩展的数据库会被跳过。
- 对每个数据库，工作进程重建 `segment_file_map`，重新扫描所有 Segment 上的数据库目录（默认表空间和用户表空间），用扫描结果替换 `segment_file_sizes` 的内容；如果 `gp_relsizes_stats.save_history` 开启，还会刷新 `table_sizes_history`。
- 每轮收集都需要空闲的后台工作进程槽。如果无法注册工作进程，错误消息会提示增大 `max_worker_processes`。如果定期执行的工作进程遇到此错误，它会退出，直到集群重启才再次启动。

## 配置参数 {#configuration-parameters}

所有参数只能在服务器配置中设置，并在重新加载配置后生效。休眠时间参数接受以毫秒为单位的纯整数，不接受 `'6h'` 之类带单位的值。

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `gp_relsizes_stats.enabled` | 布尔值 | `off` | 启用后台工作进程的定期收集。 |
| `gp_relsizes_stats.save_history` | 布尔值 | `on` | 收集时将表大小保存到 `relsizes_stats_schema.table_sizes_history`。 |
| `gp_relsizes_stats.restart_naptime` | 整数（ms） | `21600000` | 两轮收集之间的时间，默认值为 6 小时。范围：`0` 到 `2147483647`。 |
| `gp_relsizes_stats.database_naptime` | 整数（ms） | `0` | 一轮收集中分摊到各个数据库之间的总暂停时长。此值除以数据库数量后，作为处理完每个数据库后的休眠时长。范围：`0` 到 `2147483647`。 |
| `gp_relsizes_stats.file_naptime` | 整数（ms） | `1` | 扫描每个文件后的暂停时长。范围：`0` 到 `2147483647`。 |

## SQL 对象 {#sql-objects}

所有对象均创建在 `relsizes_stats_schema` 模式中。

### 函数 {#functions}

| 函数 | 返回值 | 说明 |
|---|---|---|
| `relsizes_collect_stats_once()` | `void` | 对所有数据库执行一轮收集，不执行休眠暂停，也不检查 `gp_relsizes_stats.enabled`。 |
| `get_stats_for_database(dboid oid, fast bool)` | `TABLE (segment integer, relfilenode oid, filepath text, size bigint, mtime bigint)` | 在所有 Segment 上运行，扫描数据库 `dboid` 的目录，为每个关系文件返回一行。`fast` 为 `true` 时，扫描文件之间不暂停。收集过程使用此函数。 |

### 表 {#tables}

`segment_file_map`：将关系映射到其在各个 Segment 上的关系文件节点。采用 AO 存储、随机分布。

| 列 | 类型 | 说明 |
|---|---|---|
| `segment` | `integer` | Segment 内容 ID。 |
| `reloid` | `oid` | 关系的 OID。 |
| `relfilenode` | `oid` | 该 Segment 上的关系文件节点。 |

`segment_file_sizes`：最近一次文件扫描的结果。采用 AO 存储、随机分布。

| 列 | 类型 | 说明 |
|---|---|---|
| `segment` | `integer` | Segment 内容 ID。 |
| `relfilenode` | `oid` | 从文件名解析出的关系文件节点。 |
| `filepath` | `text` | 文件路径。 |
| `size` | `bigint` | 文件大小，单位为字节。 |
| `mtime` | `bigint` | 文件的最后修改时间，表示为 Unix 时间戳。 |

`table_sizes_history`：带有收集日期的表大小。采用随机分布。

| 列 | 类型 | 说明 |
|---|---|---|
| `insert_date` | `date` | 收集此行的日期。 |
| `nspname` | `text` | 模式名称。 |
| `relname` | `text` | 表名称。 |
| `size` | `bigint` | 表大小，单位为字节。 |
| `mtime` | `timestamp` | 表的各个文件中的最新修改时间。 |

### 视图 {#views}

`table_files`：为每张表（关系类型为 `r` 和 `p`，不含 `pg_global` 表空间）的每个文件返回一行，包括 TOAST 表、TOAST 索引和 AO 表辅助关系的文件。不包括表上的索引和 AO 表的块目录，因此 `table_sizes` 中的大小不是关系的总大小。

| 列 | 类型 | 说明 |
|---|---|---|
| `nspname` | `name` | 模式名称。 |
| `relname` | `name` | 表名称。对于 `own_file = false` 的行，此列为根分区表的名称。 |
| `segment` | `integer` | Segment 内容 ID。 |
| `relfilenode` | `oid` | 关系文件节点。 |
| `filepath` | `text` | 文件路径。关系在磁盘上没有文件时为 `NULL`。 |
| `kind` | `text` | `main`、`toast`、`toast_idx`、`ao`、`ao_vm`、`ao_vm_idx` 之一。 |
| `size` | `bigint` | 文件大小，单位为字节。关系没有文件时为 `0`。 |
| `mtime` | `bigint` | 修改时间，表示为 Unix 时间戳。关系没有文件时为 `0`。 |
| `own_file` | `boolean` | 文件属于 `relname` 指定的关系时为 `true`；文件属于后代分区、归计到根分区表时为 `false`。 |

`table_sizes`：每张表的总大小。根分区表的大小包含其所有后代分区。每个分区也各自显示为一行。

| 列 | 类型 | 说明 |
|---|---|---|
| `nspname` | `name` | 模式名称。 |
| `relname` | `name` | 表名称。 |
| `size` | `numeric` | 文件大小之和，单位为字节。 |
| `mtime` | `timestamp with time zone` | 表的各个文件中的最新修改时间。 |

`namespace_sizes`：每个模式的总大小。仅对 `own_file = true` 的行求和，避免重复计算分区。

| 列 | 类型 | 说明 |
|---|---|---|
| `nspname` | `name` | 模式名称。 |
| `size` | `numeric` | 文件大小之和，单位为字节。 |

## 示例 {#example}

按需收集统计信息并检查表大小：

```sql
CREATE EXTENSION gp_relsizes_stats;

CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    department_id INT,
    date_of_birth DATE
);

INSERT INTO employees (first_name, last_name, department_id, date_of_birth) VALUES
('John', 'Doe', 1, '1988-06-15'),
('Jane', 'Smith', 2, '1990-07-20'),
('Emily', 'Jones', 1, '1985-08-30');

SELECT relsizes_stats_schema.relsizes_collect_stats_once();

SELECT size FROM relsizes_stats_schema.table_sizes_history WHERE relname = 'employees';
```

```text
 size
-------
 65536
(1 row)
```

检查模式大小：

```sql
SELECT size FROM relsizes_stats_schema.namespace_sizes WHERE nspname = 'public';
```

允许另一个角色读取统计信息：

```sql
GRANT USAGE ON SCHEMA relsizes_stats_schema TO user2;
GRANT SELECT ON ALL TABLES IN SCHEMA relsizes_stats_schema TO user2;
```

## 使用说明 {#usage-notes}

- 只有通过 `shared_preload_libraries` 加载库时，定期执行的后台工作进程才会运行。`relsizes_collect_stats_once()` 在未预加载库时也能工作。
- 只在 Segment 上收集文件大小，不扫描 Coordinator 上的文件。
- `segment_file_sizes` 和视图中的大小反映最近一次收集结果，而非文件的当前状态。
- 每次收集都会删除数据库中 `table_sizes_history` 的所有行，然后按当前日期插入当前表大小。因此，该表保存的是最近一次在 `gp_relsizes_stats.save_history` 开启状态下执行的收集结果。
- 分区表（根和中间层级）在磁盘上没有文件，在 `table_files` 中显示的大小为 `0`。
- 此模块仅在 Linux 上测试过。
