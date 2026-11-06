---
title: "视图存储概述"
description: "视图与表相似，二者都是关系，也就是“带有列的某种对象”。"
weight: 60
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/operate-with-db-objects/view-storage.md"
---

所有这类对象都存储在目录表 `pg_class` 中。它们之间的主要区别如下：

- 视图没有数据文件（因为它不保存数据）。
- 视图的 `pg_class.relkind` 值是 `v`，而不是 `r`。
- 视图有一个名为 `_RETURN` 的 `ON SELECT` 查询重写规则。

    该重写规则包含视图的定义，并存储在 `pg_rewrite` 目录表的 `ev_action` 列中。

有关视图的更多技术信息，请参见 PostgreSQL 文档中的[视图和规则系统](https://www.postgresql.org/docs/14/rules-views.html)。

此外，视图定义*不是*以字符串形式存储，而是以查询语法解析树的形式存储。视图在创建时解析，这会带来以下几个结果：

- 对象名称会在 `CREATE VIEW` 期间解析，因此当前的 `search_path` 设置会影响视图定义。
- 引用的对象不是通过名称引用，而是通过其内部不可变对象 ID 引用。因此，无需删除视图即可重命名视图定义中引用的对象或列。
- Apache Cloudberry 可以准确确定视图定义中使用了哪些对象，因此可以为这些对象添加依赖关系。

请注意，Apache Cloudberry 处理视图的方式与处理函数的方式大不相同：函数体以字符串形式存储，在创建时不会解析。因此，Apache Cloudberry 不知道给定函数依赖哪些对象。

## 视图依赖信息存储在哪里 {#where-view-dependency-information-is-stored}

以下系统目录表包含用于确定视图依赖哪些表的信息。

- `pg_class` - 对象信息，包括表和视图。`relkind` 列描述对象类型。
- `pg_depend` - 数据库特定（非共享）对象的对象依赖信息。
- `pg_rewrite` - 表和视图的重写规则。
- `pg_attribute` - 表列信息。
- `pg_namespace` - 模式（命名空间）信息。

需要注意，视图并不直接依赖其使用的对象：实际承担依赖关系的对象是视图的重写规则。这会为视图依赖信息增加一层间接关系。
