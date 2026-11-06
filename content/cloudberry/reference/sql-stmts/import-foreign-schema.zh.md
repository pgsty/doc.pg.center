---
title: "IMPORT FOREIGN SCHEMA"
description: "从外部服务器导入表定义。"
weight: 1490
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/import-foreign-schema.md"
---

## 概要 {#synopsis}

```sql
IMPORT FOREIGN SCHEMA <remote_schema>
    [ { LIMIT TO | EXCEPT } ( <table_name> [, ...] ) ]
    FROM SERVER <server_name>
    INTO <local_schema>
    [ OPTIONS ( <option> '<value>' [, ... ] ) ]
```

## 描述 {#description}

`IMPORT FOREIGN SCHEMA` 创建表示外部服务器上现有表的外表。新外表归发出命令的用户所有，并使用与远程表匹配的正确列定义和选项创建。

默认导入外部服务器上指定模式中的所有表和视图。也可以将表列表限制为指定子集，或排除特定表。所有新外表都创建在目标模式中，该模式必须已经存在。

要使用 `IMPORT FOREIGN SCHEMA`，用户必须拥有外部服务器上的 `USAGE` 权限，以及目标模式上的 `CREATE` 权限。

是否支持导入外部模式，取决于外部数据包装器。

## 参数 {#parameters}

**`remote_schema`**

要从中导入的远程模式。远程模式的具体含义取决于所用的外部数据包装器。

**`LIMIT TO ( table_name [, ...] )`**

只导入名称与给定表名之一匹配的外表，忽略外部模式中的其他表。

**`EXCEPT ( table_name [, ...] )`**

从导入中排除指定外表。外部模式中的所有表都会导入，只有此处列出的表除外。

**`server_name`**

要从中导入表定义的外部服务器名称。

**`local_schema`**

Apache Cloudberry 将在其中创建所导入外表的模式。

**`OPTIONS ( option 'value' [, ... ] )`**

导入期间使用的选项。允许的选项名称和值取决于各个外部数据包装器。

## 示例 {#examples}

从服务器 `film_server` 上的远程模式 `foreign_films` 导入表定义，在本地模式 `films` 中创建外表：

```sql
IMPORT FOREIGN SCHEMA foreign_films
    FROM SERVER film_server INTO films;
```

与上例相同，但只导入 `actors` 和 `directors` 两个表（如果存在）：

```sql
IMPORT FOREIGN SCHEMA foreign_films LIMIT TO (actors, directors)
    FROM SERVER film_server INTO films;
```

## 兼容性 {#compatibility}

`IMPORT FOREIGN SCHEMA` 命令符合 SQL 标准，但 `OPTIONS` 子句是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[CREATE FOREIGN TABLE](/cloudberry/reference/sql-stmts/create-foreign-table/), [CREATE SERVER](/cloudberry/reference/sql-stmts/create-server/)
