---
title: "CREATE SERVER"
description: "定义新的外部服务器。"
weight: 800
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-server.md"
---

## 概要 {#synopsis}

```sql
CREATE SERVER [ IF NOT EXISTS ] <server_name> [ TYPE '<server_type>' ] [ VERSION '<server_version>' ]
    FOREIGN DATA WRAPPER <fdw_name>
    [ OPTIONS ( [ mpp_execute { 'coordinator' | 'any' | 'all segments' } [, ] ]
                [ num_segments '<num>' [, ] ]
                [ <option> '<value>' [, ... ]] ) ]
```

## 描述 {#description}

`CREATE SERVER` 定义新的外部服务器。定义该服务器的用户成为其所有者。

外部服务器通常封装外部数据包装器访问外部数据源所需的连接信息。额外的用户特定连接信息可以通过用户映射指定。

创建服务器需要对指定的外部数据包装器拥有 `USAGE` 权限。

## 参数 {#parameters}

**`IF NOT EXISTS`**

如果同名服务器已经存在，不报错；Apache Cloudberry 会发出一条提示。注意，无法保证现有服务器与原本要创建的服务器有任何相似之处。

**`server_name`**

要创建的外部服务器名称，在数据库中必须唯一。

**`server_type`**

可选的服务器类型，可能对外部数据包装器有用。

**`server_version`**

可选的服务器版本，可能对外部数据包装器有用。

**`fdw_name`**

管理该服务器的外部数据包装器名称。

**`OPTIONS ( option 'value' [, ... ] )`**

新外部服务器的选项。这些选项通常定义服务器的连接细节，但实际名称和值取决于该服务器的外部数据包装器。

**`mpp_execute { 'coordinator' | 'any' | 'all segments' }`**

Apache Cloudberry 特有的选项，指定外部数据包装器在哪台主机上读写数据：

- `coordinator`（默认值）——在 Coordinator 主机上读写数据。
- `any`——在 Coordinator 主机或任意一个 Segment 上读取数据，取决于哪条路径的代价更低。
- `all segments`——在所有 Segment 上读写数据。要支持此选项值，外部数据包装器应具有将 Segment 与数据匹配的策略。

> **注意** 只有设置 `mpp_execute 'all segments'` 时，Apache Cloudberry 才支持并行写入外表。

是否支持外部服务器的 `mpp_execute` 选项及其具体模式，取决于外部数据包装器。

可以在多种命令中指定 `mpp_execute` 选项：`CREATE FOREIGN TABLE`、`CREATE SERVER` 和 `CREATE FOREIGN DATA WRAPPER`。外表设置优先于外部服务器设置，后者又优先于外部数据包装器设置。

**`num_segments 'num'`**

当 `mpp_execute` 设为 `'all segments'` 时，Apache Cloudberry 特有的 `num_segments` 选项指定在源 Apache Cloudberry 集群上启动的查询执行器数量。如果未提供值，num 默认为源集群中的 Segment 数量。

是否支持外部服务器的 `num_segments` 选项，取决于外部数据包装器。

## 注意事项 {#notes}

使用 dblink 模块时（见 dblink），可以将外部服务器名称作为 `dblink_connect()` 函数的参数，以提供连接参数。要以这种方式使用外部服务器，必须拥有其 `USAGE` 权限。

## 示例 {#examples}

创建名为 `myserver` 的外部服务器，使用名为 `gpfdw1` 的外部数据包装器，并包含连接选项：

```sql
CREATE SERVER myserver FOREIGN DATA WRAPPER gpfdw1 
    OPTIONS (host 'foo', dbname 'foodb', port '5432');
```

## 兼容性 {#compatibility}

`CREATE SERVER` 符合 ISO/IEC 9075-9（SQL/MED）。

## 另见 {#see-also}

[ALTER SERVER](/cloudberry/reference/sql-stmts/alter-server/), [DROP SERVER](/cloudberry/reference/sql-stmts/drop-server/), [CREATE FOREIGN DATA WRAPPER](/cloudberry/reference/sql-stmts/create-foreign-data-wrapper/), [CREATE FOREIGN TABLE](/cloudberry/reference/sql-stmts/create-foreign-table/), [CREATE USER MAPPING](/cloudberry/reference/sql-stmts/create-user-mapping/)
