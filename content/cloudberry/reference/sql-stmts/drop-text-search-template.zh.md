---
title: "DROP TEXT SEARCH TEMPLATE"
description: "使用 DROP TEXT SEARCH TEMPLATE 删除文本检索模板并控制依赖对象的处理方式。"
weight: 1370
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-text-search-template.md"
---

## 描述 {#description}

删除文本检索模板。

## 概要 {#synopsis}

```sql
DROP TEXT SEARCH TEMPLATE [ IF EXISTS ] <name> [ CASCADE | RESTRICT ]
```

## 描述 {#description-1}

`DROP TEXT SEARCH TEMPLATE` 删除现有文本检索模板。必须是超级用户才能使用此命令。

必须是超级用户才能使用 `ALTER TEXT SEARCH TEMPLATE`。

## 参数 {#parameters}

**`IF EXISTS`**

如果文本检索模板不存在，不报错；Apache Cloudberry 会发出一条提示。

**`name`**

现有文本检索模板的名称（可带模式限定）。

**`CASCADE`**

自动删除依赖此文本检索模板的对象，以及依赖这些对象的所有对象。

**`RESTRICT`**

如果有对象依赖此文本检索模板，则拒绝删除。这是默认行为。

## 示例 {#examples}

删除文本检索模板 `thesaurus`：

```sql
DROP TEXT SEARCH TEMPLATE thesaurus;
```

如果有现有文本检索字典使用此模板，此命令就不会成功。添加 `CASCADE` 可将这些字典与模板一起删除。

## 兼容性 {#compatibility}

SQL 标准中没有 `DROP TEXT SEARCH TEMPLATE` 语句。

## 另见 {#see-also}

[ALTER TEXT SEARCH TEMPLATE](/cloudberry/reference/sql-stmts/alter-text-search-template/), [CREATE TEXT SEARCH TEMPLATE](/cloudberry/reference/sql-stmts/create-text-search-template/)
