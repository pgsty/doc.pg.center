---
title: "DROP TEXT SEARCH PARSER"
description: "使用 DROP TEXT SEARCH PARSER 删除文本检索解析器并控制依赖对象的处理方式。"
weight: 1360
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-text-search-parser.md"
---

## 描述 {#description}

删除文本检索解析器。

## 概要 {#synopsis}

```sql
DROP TEXT SEARCH PARSER [ IF EXISTS ] <name> [ CASCADE | RESTRICT ]
```

## 描述 {#description-1}

`DROP TEXT SEARCH PARSER` 删除现有文本检索解析器。必须是超级用户才能使用此命令。

## 参数 {#parameters}

**`IF EXISTS`**

如果文本检索解析器不存在，不报错；Apache Cloudberry 会发出一条提示。

**`name`**

现有文本检索解析器的名称（可带模式限定）。

**`CASCADE`**

自动删除依赖此文本检索解析器的对象，以及依赖这些对象的所有对象。

**`RESTRICT`**

如果有对象依赖此文本检索解析器，则拒绝删除。这是默认行为。

## 示例 {#examples}

删除文本检索解析器 `my_parser`：

```sql
DROP TEXT SEARCH PARSER my_parser;
```

如果有现有文本检索配置使用此解析器，此命令就不会成功。添加 `CASCADE` 可将这些配置与解析器一起删除。

## 兼容性 {#compatibility}

SQL 标准中没有 `DROP TEXT SEARCH PARSER` 语句。

## 另见 {#see-also}

[ALTER TEXT SEARCH PARSER](/cloudberry/reference/sql-stmts/alter-text-search-parser/), [CREATE TEXT SEARCH PARSER](/cloudberry/reference/sql-stmts/create-text-search-parser/)
