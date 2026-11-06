---
title: "ALTER MATERIALIZED VIEW"
description: "更改物化视图的定义。"
weight: 160
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-materialized-view.md"
---

## 概要 {#synopsis}

```sql
ALTER MATERIALIZED VIEW [ IF EXISTS ] <name> <action> [, ... ]
ALTER MATERIALIZED VIEW <name>
    DEPENDS ON EXTENSION <extension_name>
ALTER MATERIALIZED VIEW [ IF EXISTS ] <name>
    RENAME [ COLUMN ] <column_name> TO <new_column_name>
ALTER MATERIALIZED VIEW [ IF EXISTS ] <name>
    RENAME TO <new_name>
ALTER MATERIALIZED VIEW [ IF EXISTS ] <name>
    SET SCHEMA <new_schema>
ALTER MATERIALIZED VIEW ALL IN TABLESPACE <name> [ OWNED BY <role_name> [, ... ] ]
    SET TABLESPACE <new_tablespace> [ NOWAIT ]

-- where <action> is one of:

    ALTER [ COLUMN ] <column_name> SET STATISTICS <integer>
    ALTER [ COLUMN ] <column_name> SET ( <attribute_option> = <value> [, ... ] )
    ALTER [ COLUMN ] <column_name> RESET ( <attribute_option> [, ... ] )
    ALTER [ COLUMN ] <column_name> SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN }
    CLUSTER ON <index_name>
    SET WITHOUT CLUSTER
    SET TABLESPACE <new_tablespace>
    SET ( <storage_paramete>r = <value> [, ... ] )
    RESET ( <storage_parameter> [, ... ] )
    OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }
```

## 描述 {#description}

`ALTER MATERIALIZED VIEW` 更改现有物化视图的各种辅助属性。

要使用 `ALTER MATERIALIZED VIEW`，你必须拥有该物化视图。要更改物化视图所在的模式，你还必须在新模式上具有 `CREATE` 权限。要更改所有者，你还必须是新所有者角色的直接或间接成员，并且该角色必须在该物化视图所在的模式上具有 `CREATE` 权限。（这些限制确保更改所有者不会做到任何通过删除并重新创建该物化视图无法做到的事情。不过，超级用户无论如何都可以更改任何视图的所有权。）

`DEPENDS ON EXTENSION` 形式将物化视图标记为依赖于某个扩展，这样，如果该扩展被删除，该物化视图也会被自动删除。

`ALTER MATERIALIZED VIEW` 可用的语句子形式和操作是 `ALTER TABLE` 所提供的那些的子集，并且用于物化视图时含义相同。详情请参见 [ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/) 的说明。

## 参数 {#parameters}

**`name`**

一个现有物化视图的名称（可以是模式限定的）。

**`column_name`**

新列或现有列的名称。

**`extension_name`**

该物化视图要依赖的扩展的名称。

**`new_column_name`**

现有列的新名称。

**`new_owner`**

物化视图的新所有者的用户名。

**`new_name`**

物化视图的新名称。

**`new_schema`**

物化视图的新模式。

## 示例 {#examples}

将物化视图 `foo` 重命名为 `bar`：

```sql
ALTER MATERIALIZED VIEW foo RENAME TO bar;
```

## 兼容性 {#compatibility}

`ALTER MATERIALIZED VIEW` 是 Apache Cloudberry 对 SQL 标准的扩展。

## 另见 {#see-also}

[CREATE MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/create-materialized-view/)、[DROP MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/drop-materialized-view/)、[REFRESH MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/refresh-materialized-view/)
