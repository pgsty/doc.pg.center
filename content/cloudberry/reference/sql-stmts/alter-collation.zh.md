---
title: "ALTER COLLATION"
description: "更改一个排序规则的定义。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-collation.md"
---

## 概要 {#synopsis}

```sql
ALTER COLLATION <name> REFRESH VERSION

ALTER COLLATION <name> RENAME TO <new_name>
ALTER COLLATION <name> OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }
ALTER COLLATION <name> SET SCHEMA <new_schema>
```

## 描述 {#description}

`ALTER COLLATION` 更改一个排序规则的定义。

要使用 `ALTER COLLATION`，你必须拥有该排序规则。要更改所有者，你还必须是新所有者角色的直接或间接成员，并且该角色必须在该排序规则所在的模式上具有 `CREATE` 权限。（这些限制确保更改所有者不会做到任何通过删除并重新创建该排序规则无法做到的事情。不过，超级用户无论如何都可以更改任何排序规则的所有权。）

## 参数 {#parameters}

**`name`**

一个现有排序规则的名称（可以是模式限定的）。

**`new_name`**

排序规则的新名称。

**`new_owner`**

排序规则的新所有者。

**`new_schema`**

排序规则的新模式。

**`REFRESH VERSION`**

更新排序规则的版本。参见下文的[注解](#notes)。

## 注解 {#notes}

使用由 ICU 库提供的排序规则时，创建排序规则对象时会把排序器（collator）特定于 ICU 的版本记录在系统目录中。使用该排序规则时，会将当前版本与所记录的版本进行核对，若二者不匹配则发出警告，例如：

```
WARNING: collation "xx-x-icu" has version mismatch
DETAIL: The collation in the database was created using version 1.2.3.4, but the operating system provides version 2.3.4.5.
HINT: Rebuild all objects affected by this collation and run ALTER COLLATION pg_catalog."xx-x-icu" REFRESH VERSION, or build PostgreSQL with the right library version.
```

排序规则定义的变化可能导致索引损坏及其他问题，因为数据库系统依赖于已存储的对象具有特定的排序顺序。通常应当避免这种情况，但在某些合理的场景中它仍可能发生，例如使用 `pg_upgrade` 升级到链接了更新版本 ICU 的服务器二进制文件时。发生这种情况时，所有依赖该排序规则的对象都应当重建，例如使用 `REINDEX`。完成之后，可以使用命令 `ALTER COLLATION ... REFRESH VERSION` 刷新排序规则版本。这会更新系统目录以记录当前的排序器版本，并使警告消失。请注意，这并不会真正检查所有受影响的对象是否已被正确重建。

下面的查询可用于找出当前数据库中所有需要刷新的排序规则，以及依赖于它们的对象：

```sql
SELECT pg_describe_object(refclassid, refobjid, refobjsubid) AS "Collation",
       pg_describe_object(classid, objid, objsubid) AS "Object"
  FROM pg_depend d JOIN pg_collation c
       ON refclassid = 'pg_collation'::regclass AND refobjid = c.oid
  WHERE c.collversion <> pg_collation_actual_version(c.oid)
  ORDER BY 1, 2;
```

## 示例 {#examples}

将排序规则 de_DE 重命名为 `german`：

```sql
ALTER COLLATION "de_DE" RENAME TO german;
```

将排序规则 `en_US` 的所有者更改为 `joe`：

```sql
ALTER COLLATION "en_US" OWNER TO joe;
```

## 兼容性 {#compatibility}

SQL 标准中没有 `ALTER COLLATION` 语句。

## 另见 {#see-also}

[CREATE COLLATION](/cloudberry/reference/sql-stmts/create-collation/)、[DROP COLLATION](/cloudberry/reference/sql-stmts/drop-collation/)
