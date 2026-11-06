---
title: "DROP TEXT SEARCH DICTIONARY"
description: "删除文本检索字典。"
weight: 1350
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-text-search-dictionary.md"
---

## 概要 {#synopsis}

```sql
DROP TEXT SEARCH DICTIONARY [ IF EXISTS ] <name> [ CASCADE | RESTRICT ]
```

## 描述 {#description}

`DROP TEXT SEARCH DICTIONARY` 删除现有文本检索字典。必须是该字典的所有者才能运行此命令。

## 参数 {#parameters}

**`IF EXISTS`**

如果文本检索字典不存在，不报错；Apache Cloudberry 会发出一条提示。

**`name`**

现有文本检索字典的名称（可带模式限定）。

**`CASCADE`**

自动删除依赖此文本检索字典的对象，以及依赖这些对象的所有对象。

**`RESTRICT`**

如果有对象依赖此文本检索字典，则拒绝删除。这是默认行为。

## 示例 {#examples}

删除文本检索字典 `english`：

```sql
DROP TEXT SEARCH DICTIONARY english;
```

如果有现有文本检索配置使用此字典，此命令就不会成功。添加 `CASCADE` 可将这些配置与字典一起删除。

## 兼容性 {#compatibility}

SQL 标准中没有 `CREATE TEXT SEARCH DICTIONARY` 语句。

## 另见 {#see-also}

[ALTER TEXT SEARCH DICTIONARY](/cloudberry/reference/sql-stmts/alter-text-search-dictionary/), [CREATE TEXT SEARCH DICTIONARY](/cloudberry/reference/sql-stmts/create-text-search-dictionary/)
