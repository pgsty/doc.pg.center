---
title: "CREATE FOREIGN DATA WRAPPER"
description: "定义新的外部数据包装器。"
weight: 610
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-foreign-data-wrapper.md"
---

## 概要 {#synopsis}

```sql
CREATE FOREIGN DATA WRAPPER <name>
    [ HANDLER <handler_function> | NO HANDLER ]
    [ VALIDATOR <validator_function> | NO VALIDATOR ]
    [ OPTIONS ( [ mpp_execute { 'coordinator' | 'any' | 'all segments' } [, ] ] <option> '<value>' [, ... ] ) ]
```

## 描述 {#description}

`CREATE FOREIGN DATA WRAPPER` 在当前数据库中创建新的外部数据包装器。定义该包装器的用户成为其所有者。

外部数据包装器的名称在数据库中必须唯一。

只有超级用户才能创建外部数据包装器。

## 参数 {#parameters}

**`name`**

要创建的外部数据包装器名称，在数据库中必须唯一。

**`HANDLER handler_function`**

先前注册的函数名称，Apache Cloudberry 调用它来获取外表的执行函数。hander_function 必须不接受参数，返回类型必须为 `fdw_handler`。

可以创建不带处理函数的外部数据包装器，但使用这种包装器只能声明外表，不能访问外表。

**`VALIDATOR validator_function`**

先前注册的函数名称，Apache Cloudberry 调用它来检查提供给外部数据包装器的通用选项。此函数还检查使用该包装器的外部服务器、用户映射和外表的选项。如果未指定验证函数，或指定了 `NO VALIDATOR`，Apache Cloudberry 就不会在创建时检查选项。（根据具体实现，外部数据包装器可能在运行时忽略或拒绝无效选项。）

validator_function 必须接受两个参数：一个为 `text[]` 类型，包含按系统目录中所存形式表示的选项数组；另一个为 `oid` 类型，标识包含这些选项的系统目录的 OID。

返回类型会被忽略；validator_function 应使用 `ereport(ERROR)` 函数报告无效选项。

**`OPTIONS ( option 'value' [, ... ] )`**

新外部数据包装器的选项。选项名称必须唯一。选项名称和值取决于具体的外部数据包装器，并由其 validator_function 验证。

**`mpp_execute { 'coordinator' | 'any' | 'all segments' }`**

Apache Cloudberry 特有的选项，指定外部数据包装器在哪台主机上读写数据：

- `coordinator`（默认值）——在 Coordinator 主机上读写数据。
- `any`——在 Coordinator 主机或任意一个 Segment 上读取数据，取决于哪条路径的成本更低。
- `all segments`——在所有 Segment 上读写数据。要支持此选项值，外部数据包装器必须具有将 Segment 与数据匹配的策略。

> **注意** 只有设置 `mpp_execute 'all segments'` 时，Apache Cloudberry 才支持并行写入外表。

是否支持外部数据包装器的 `mpp_execute` 选项及其具体模式，取决于包装器的实现。

可以在多种命令中指定 `mpp_execute` 选项：`CREATE FOREIGN TABLE`、`CREATE SERVER` 和 `CREATE FOREIGN DATA WRAPPER`。外表设置优先于外部服务器设置，后者又优先于外部数据包装器设置。

## 注意事项 {#notes}

外部数据包装器功能仍在开发中。查询优化较为基础（大部分交给包装器处理）。

## 示例 {#examples}

创建名为 `dummy`、没有实际用途的外部数据包装器：

```sql
CREATE FOREIGN DATA WRAPPER dummy;
```

创建名为 `file` 的外部数据包装器，其处理函数名为 `file_fdw_handler`：

```sql
CREATE FOREIGN DATA WRAPPER file HANDLER file_fdw_handler;
```

创建名为 `mywrapper`、包含一个选项的外部数据包装器：

```sql
CREATE FOREIGN DATA WRAPPER mywrapper OPTIONS (debug 'true');
```

## 兼容性 {#compatibility}

`CREATE FOREIGN DATA WRAPPER` 符合 ISO/IEC 9075-9（SQL/MED），但 `HANDLER` 和 `VALIDATOR` 子句属于扩展，且 Apache Cloudberry 没有实现标准中的 `LIBRARY` 和 `LANGUAGE` 子句。

不过，SQL/MED 功能作为一个整体尚未符合标准。

## 另见 {#see-also}

[ALTER FOREIGN DATA WRAPPER](/cloudberry/reference/sql-stmts/alter-foreign-data-wrapper/), [DROP FOREIGN DATA WRAPPER](/cloudberry/reference/sql-stmts/drop-foreign-data-wrapper/), [CREATE FOREIGN TABLE](/cloudberry/reference/sql-stmts/create-foreign-table/), [CREATE SERVER](/cloudberry/reference/sql-stmts/create-server/), [CREATE USER MAPPING](/cloudberry/reference/sql-stmts/create-user-mapping/)
