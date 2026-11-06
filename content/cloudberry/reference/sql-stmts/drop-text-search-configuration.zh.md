---
title: "DROP TEXT SEARCH CONFIGURATION"
description: "删除文本检索配置。"
weight: 1340
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-text-search-configuration.md"
---

## 概要 {#synopsis}

```sql
DROP TEXT SEARCH CONFIGURATION [ IF EXISTS ] <name> [ CASCADE | RESTRICT ]
```

## 描述 {#description}

`DROP TEXT SEARCH CONFIGURATION` 删除现有文本检索配置。必须是该配置的所有者才能运行此命令。

## 参数 {#parameters}

**`IF EXISTS`**

如果文本检索配置不存在，不报错；Apache Cloudberry 会发出一条提示。

**`name`**

现有文本检索配置的名称（可带模式限定）。

**`CASCADE`**

自动删除依赖此文本检索配置的对象，以及依赖这些对象的所有对象。

**`RESTRICT`**

如果有对象依赖此文本检索配置，则拒绝删除。这是默认行为。

## 示例 {#examples}

删除文本检索配置 `my_english`：

```sql
DROP TEXT SEARCH CONFIGURATION my_english;
```

如果有现有索引在 `to_tsvector` 调用中引用此配置，此命令就不会成功。添加 `CASCADE` 可将这些索引与文本检索配置一起删除。

## 兼容性 {#compatibility}

SQL 标准中没有 `DROP TEXT SEARCH CONFIGURATION` 语句。

## 另见 {#see-also}

[ALTER TEXT SEARCH CONFIGURATION](/cloudberry/reference/sql-stmts/alter-text-search-configuration/), [CREATE TEXT SEARCH CONFIGURATION](/cloudberry/reference/sql-stmts/create-text-search-configuration/)
