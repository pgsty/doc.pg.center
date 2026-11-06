---
title: "ALTER TEXT SEARCH PARSER"
description: "使用 ALTER TEXT SEARCH PARSER 更改文本检索解析器的定义。"
weight: 360
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-text-search-parser.md"
---

## 描述 {#description}

更改文本检索解析器的定义。

## 概要 {#synopsis}

```sql
ALTER TEXT SEARCH PARSER <name> RENAME TO <new_name>
ALTER TEXT SEARCH PARSER <name> SET SCHEMA <new_schema>
```

## 描述 {#description-1}

`ALTER TEXT SEARCH PARSER` 用于更改文本检索解析器的定义。目前唯一支持的功能是更改解析器的名称。

必须是超级用户才能使用 `ALTER TEXT SEARCH PARSER`。

## 参数 {#parameters}

**`name`**

现有文本检索解析器的名称（可以带模式限定）。

**`new_name`**

文本检索解析器的新名称。

**`new_schema`**

文本检索解析器的新模式。

## 兼容性 {#compatibility}

SQL 标准中没有 `ALTER TEXT SEARCH PARSER` 语句。

## 另请参阅 {#see-also}

[CREATE TEXT SEARCH PARSER](/cloudberry/reference/sql-stmts/create-text-search-parser/)、[DROP TEXT SEARCH PARSER](/cloudberry/reference/sql-stmts/drop-text-search-parser/)
