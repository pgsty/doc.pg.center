---
title: "ALTER OPERATOR CLASS"
description: "更改一个操作符类的定义。"
weight: 170
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-operator-class.md"
---

## 概要 {#synopsis}

```sql
ALTER OPERATOR CLASS <name> USING <index_method> RENAME TO <new_name>

ALTER OPERATOR CLASS <name> USING <index_method> OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }

ALTER OPERATOR CLASS <name> USING <index_method> SET SCHEMA <new_schema>
```

## 描述 {#description}

`ALTER OPERATOR CLASS` 更改一个操作符类的定义。

要使用 `ALTER OPERATOR CLASS`，你必须拥有该操作符类。要更改所有者，你还必须是新所有者角色的直接或间接成员，并且该角色必须在该操作符类所在的模式上具有 `CREATE` 权限。（这些限制确保更改所有者不会做到任何通过删除并重新创建该操作符类无法做到的事情。不过，超级用户无论如何都可以更改任何操作符类的所有权。）

## 参数 {#parameters}

**`name`**

一个现有操作符类的名称（可以是模式限定的）。

**`index_method`**

该操作符类所对应的索引方法的名称。

**`new_name`**

该操作符类的新名称。

**`new_owner`**

该操作符类的新所有者。

**`new_schema`**

该操作符类的新模式。

## 兼容性 {#compatibility}

SQL 标准中没有 `ALTER OPERATOR CLASS` 语句。

## 另见 {#see-also}

[CREATE OPERATOR CLASS](/cloudberry/reference/sql-stmts/create-operator-class/)、[DROP OPERATOR CLASS](/cloudberry/reference/sql-stmts/drop-operator-class/)、[ALTER OPERATOR FAMILY](/cloudberry/reference/sql-stmts/alter-operator-family/)
