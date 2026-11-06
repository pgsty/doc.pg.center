---
title: "DROP EXTENSION"
description: "从 Apache Cloudberry 中删除扩展。"
weight: 1070
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-extension.md"
---

## 概要 {#synopsis}

```sql
DROP EXTENSION [ IF EXISTS ] <name> [, ...] [ CASCADE | RESTRICT ]
```

## 描述 {#description}

`DROP EXTENSION` 从数据库中删除扩展。删除扩展时，其成员对象也会被删除。

> [!NOTE]
> 为创建扩展而安装的支持文件（例如库文件和 `.control` 文件）不会被删除。必须手动从 Apache Cloudberry 主机中删除这些文件。

必须拥有扩展才能使用 `DROP EXTENSION`。

## 参数 {#parameters}

**`IF EXISTS`**

如果扩展不存在，不报错；Apache Cloudberry 会发出一条提示。

**`name`**

已安装扩展的名称。

**`CASCADE`**

自动删除依赖此扩展的对象，以及依赖这些对象的所有对象。更多信息见 PostgreSQL 的[依赖跟踪](https://www.postgresql.org/docs/14/ddl-depend.html)文档。

> [!TIP]
> 发出带 `CASCADE` 关键字的 `DROP EXTENSION` 命令之前，应了解依赖此扩展的所有对象，以免产生意外后果。

**`RESTRICT`**

如果有对象依赖此扩展，则拒绝删除（扩展自身的成员对象以及同一条 `DROP` 命令中列出的其他扩展除外）。这是默认行为。

## 示例 {#examples}

从当前数据库中删除扩展 `hstore`：

```sql
DROP EXTENSION hstore;
```

如果数据库正在使用任何扩展对象，此命令就会失败。例如，某个表定义了 `hstore` 类型的列。添加 `CASCADE` 选项可强制删除这些依赖对象。

## 兼容性 {#compatibility}

`DROP EXTENSION` 是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[`CREATE EXTENSION`](/cloudberry/reference/sql-stmts/create-extension/), [`ALTER EXTENSION`](/cloudberry/reference/sql-stmts/alter-extension/)
