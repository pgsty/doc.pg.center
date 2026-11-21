---
title: postgres_fdw
description: postgres_fdw 是访问远程 PostgreSQL 或 Apache Cloudberry 数据库的外部数据包装器。
weight: 220
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/postgres-fdw.md
---

`postgres_fdw` 模块是一个外部数据包装器（FDW），可用于访问远程 PostgreSQL 或 Apache Cloudberry 数据库中的数据。

Apache Cloudberry 的 `postgres_fdw` 模块是 PostgreSQL `postgres_fdw` 模块的修改版。它支持 Apache Cloudberry 外表的 MPP 执行选项，也有 PostgreSQL 模块没有的限制。下文分别介绍。

## 安装并注册模块 {#install-and-register-the-module}

`postgres_fdw` 不属于 Apache Cloudberry 的默认构建目标（`make` 和 `make install`）。如果 `CREATE EXTENSION` 报告该扩展不可用，请使用配置当前安装版本时所用的 Apache Cloudberry 源码树，构建并安装此模块：

```shell
make -C contrib/postgres_fdw install
```

集群的每台主机（Coordinator、Standby Coordinator 及所有 Segment 主机）上都必须有模块文件。`make install-world` 也会安装此模块。

然后在每个需要使用它的数据库中注册扩展：

```sql
CREATE EXTENSION postgres_fdw;
```

## 基本用法 {#basic-usage}

```sql
CREATE SERVER pgserver FOREIGN DATA WRAPPER postgres_fdw
  OPTIONS (host 'pghost', port '5432', dbname 'sales');

CREATE USER MAPPING FOR CURRENT_USER SERVER pgserver
  OPTIONS (user 'remote_user', password 'secret');

CREATE FOREIGN TABLE orders_ft (id int, amount numeric)
  SERVER pgserver
  OPTIONS (schema_name 'public', table_name 'orders');

SELECT count(*) FROM orders_ft;
```

## 选项 {#options}

此模块接受 `libpq` 的连接选项，以及 PostgreSQL 14 `postgres_fdw` 模块的选项：`schema_name`、`table_name`、`column_name`、`use_remote_estimate`、`fdw_startup_cost`、`fdw_tuple_cost`、`extensions`、`updatable`、`truncatable`、`fetch_size`、`batch_size`、`async_capable`、`keep_connections`、`password_required`、`sslcert` 和 `sslkey`。

以下选项为 Apache Cloudberry 特有：

| 选项 | 设置位置 | 说明 |
|--------|-------|-------------|
| `mpp_execute` | 外表、服务器或外部数据包装器 | Apache Cloudberry 选项，决定在哪里访问外表：`'coordinator'`（等同于 `'master'`）、`'any'` 或 `'all segments'`。 |
| `num_segments` | 服务器 | 当外表的 `mpp_execute` 选项为 `'all segments'` 时，访问该外表的 Segment 数量。不设置此选项时，使用集群的所有 Segment。 |

使用 `mpp_execute 'all segments'` 时，`INSERT INTO <foreign table> SELECT ...` 语句从各个 Segment 并行写入远程服务器。

## 通过一个外表访问多个远程服务器 {#access-multiple-remote-servers-from-one-foreign-table}

`mpp_execute` 选项为 `'all segments'` 的外表可以读取多个远程服务器上结构相同的表。将每个服务器作为外部 Segment 加入外表：

```sql
CREATE SERVER mpps1 FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'pghost1', dbname 'fdw1');
CREATE SERVER mpps2 FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'pghost2', dbname 'fdw2');
CREATE USER MAPPING FOR CURRENT_USER SERVER mpps1;
CREATE USER MAPPING FOR CURRENT_USER SERVER mpps2;

CREATE FOREIGN TABLE fs1 (a int, b text)
  SERVER mpps1
  OPTIONS (schema_name 'public', table_name 't1', mpp_execute 'all segments');

ADD FOREIGN SEGMENT FROM SERVER mpps1 INTO fs1;
ADD FOREIGN SEGMENT FROM SERVER mpps2 INTO fs1;
```

随后，对 `fs1` 的查询会让每个查询执行器进程扫描一个远程服务器，并在 Coordinator 上汇集结果：

```sql
SET optimizer = off;
EXPLAIN (COSTS OFF) SELECT * FROM fs1;
```

```text
                QUERY PLAN
------------------------------------------
 Gather Motion 2:1  (slice1; segments: 2)
   ->  Foreign Scan on fs1
 Optimizer: Postgres query optimizer
(3 rows)
```

对于这样的外表：

- 聚合可以作为部分聚合下推到远程服务器，并在 Coordinator 上完成最终聚合。
- `LIMIT` 子句先在每个 Segment 上施加初步限制，再将行汇集到 Coordinator。
- 隐藏列 `gp_foreign_server` 包含行来源外部服务器的 OID。可以在连接条件中使用它，例如 `fs1.gp_foreign_server = fs2.gp_foreign_server`，以仅连接来自同一服务器的行。

> [!CAUTION]
> 对具有外部 Segment 的外表进行查询时，只有使用基于 Postgres 的规划器才能返回正确结果。GPORCA 忽略外部 Segment：它在集群的所有 Segment 上扫描表，导致某些远程服务器被多次读取、行重复，且每行的 `gp_foreign_server` 均为 `0`。查询这样的表之前，请关闭 GPORCA：
>
```sql
SET optimizer = off;
```

## 限制 {#limitations}

- 不支持 `use_remote_estimate` 选项。如果服务器或外表设置了此选项，无论值为何，模块都会忽略它并报告警告 `fdw option 'use_remote_estimate' is not supported.`。
- 远程服务器为 Apache Cloudberry 数据库时，只支持对外表执行 `INSERT`，不支持 `UPDATE` 和 `DELETE`。

## 函数 {#functions}

| 函数 | 说明 |
|----------|-------------|
| `postgres_fdw_get_connections(OUT server_name text, OUT valid boolean) returns setof record` | 返回 `postgres_fdw` 从本地会话建立的所有已打开连接的外部服务器名称，以及每个连接是否有效。 |
| `postgres_fdw_disconnect(server_name text) returns boolean` | 断开本地会话到指定外部服务器的已打开连接。 |
| `postgres_fdw_disconnect_all() returns boolean` | 断开本地会话到外部服务器的所有已打开连接。 |

## 模块文档 {#module-documentation}

此模块选项和行为的详细信息，参见 PostgreSQL 文档中的 [postgres_fdw](https://www.postgresql.org/docs/14/postgres-fdw.html)。
