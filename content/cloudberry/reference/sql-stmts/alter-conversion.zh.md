---
title: "ALTER CONVERSION"
description: "更改一个编码转换的定义。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-conversion.md"
---

## 概要 {#synopsis}

```sql
ALTER CONVERSION <name> RENAME TO <new_name>

ALTER CONVERSION <name> OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }

ALTER CONVERSION <name> SET SCHEMA <new_schema>
```

## 描述 {#description}

`ALTER CONVERSION` 更改一个编码转换的定义。

要使用 `ALTER CONVERSION`，你必须拥有该编码转换。要更改所有者，你还必须是新所有者角色的直接或间接成员，并且该角色必须在该编码转换所在的模式上具有 `CREATE` 权限。（这些限制确保更改所有者不会做到任何通过删除并重新创建该编码转换无法做到的事情。不过，超级用户无论如何都可以更改任何编码转换的所有权。）

## 参数 {#parameters}

**`name`**

一个现有编码转换的名称（可以是模式限定的）。

**`new_name`**

编码转换的新名称。

**`new_owner`**

编码转换的新所有者。

**`new_schema`**

编码转换的新模式。

## 示例 {#examples}

将编码转换 `iso_8859_1_to_utf8` 重命名为 `latin1_to_unicode`：

```sql
ALTER CONVERSION iso_8859_1_to_utf8 RENAME TO latin1_to_unicode;
```

将编码转换 `iso_8859_1_to_utf8` 的所有者更改为 `joe`：

```sql
ALTER CONVERSION iso_8859_1_to_utf8 OWNER TO joe;
```

## 兼容性 {#compatibility}

SQL 标准中没有 `ALTER CONVERSION` 语句。

## 另见 {#see-also}

[CREATE CONVERSION](/cloudberry/reference/sql-stmts/create-conversion/)、[DROP CONVERSION](/cloudberry/reference/sql-stmts/drop-conversion/)
