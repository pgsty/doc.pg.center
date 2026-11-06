---
title: "ALTER LANGUAGE"
description: "更改过程语言的定义。"
weight: 150
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-language.md"
---

## 概要 {#synopsis}

```sql
ALTER [ PROCEDURAL ] LANGUAGE <name> RENAME TO <new_name>
ALTER [ PROCEDURAL ] LANGUAGE <name> OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }
```

## 描述 {#description}

`ALTER LANGUAGE` 更改特定数据库中某个过程语言的定义。所支持的定义更改包括重命名该语言或指派新的所有者。要使用 `ALTER LANGUAGE`，你必须是超级用户或该语言的所有者。

## 参数 {#parameters}

**`name`**

语言的名称。

**`new_name`**

该语言的新名称。

**`new_owner`**

该语言的新所有者。

## 兼容性 {#compatibility}

SQL 标准中没有 `ALTER LANGUAGE` 语句。

## 另见 {#see-also}

[CREATE LANGUAGE](/cloudberry/reference/sql-stmts/create-language/)、[DROP LANGUAGE](/cloudberry/reference/sql-stmts/drop-language/)
