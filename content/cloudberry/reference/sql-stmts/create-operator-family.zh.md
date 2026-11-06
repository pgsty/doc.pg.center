---
title: "CREATE OPERATOR FAMILY"
description: "定义新的操作符族。"
weight: 690
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-operator-family.md"
---

## 概要 {#synopsis}

```sql
CREATE OPERATOR FAMILY <name>  USING <index_method>  
```

## 描述 {#description}

`CREATE OPERATOR FAMILY` 创建新的操作符族。操作符族定义一组相关操作符类，也可以包含一些与这些操作符类兼容、但并非任一单独索引正常工作所必需的额外操作符和支持函数。（索引所必需的操作符和函数应归入相关操作符类，而不应作为操作符族中的“松散”成员。通常，单一数据类型的操作符绑定到操作符类，而跨数据类型的操作符可以作为松散成员，存在于包含这两种数据类型操作符类的操作符族中。）

新操作符族最初为空。随后应通过 `CREATE OPERATOR CLASS` 命令向其中添加操作符类，也可以通过 `ALTER OPERATOR FAMILY` 命令添加“松散”的操作符及其对应支持函数。

如果给出模式名，则在指定模式中创建操作符族；否则在当前模式中创建。同一模式中的两个操作符族只有在对应不同索引方法时才能同名。

定义操作符族的用户成为其所有者。目前，创建用户必须是超级用户。（此限制是因为错误的操作符族定义可能导致服务器行为异常，甚至崩溃。）

更多信息见 PostgreSQL 文档中的[索引扩展接口](https://www.postgresql.org/docs/12/xindex.html)。

## 参数 {#parameters}

**`name`**

要创建的操作符族名称（可带模式限定）。

**`index_method`**

此操作符族对应的索引方法名称。

## 兼容性 {#compatibility}

`CREATE OPERATOR FAMILY` 是 Apache Cloudberry 的扩展。SQL 标准中没有 `CREATE OPERATOR FAMILY` 语句。

## 另见 {#see-also}

[ALTER OPERATOR FAMILY](/cloudberry/reference/sql-stmts/alter-operator-family/), [DROP OPERATOR FAMILY](/cloudberry/reference/sql-stmts/drop-operator-family/), [ALTER OPERATOR CLASS](/cloudberry/reference/sql-stmts/alter-operator-class/), [CREATE OPERATOR CLASS](/cloudberry/reference/sql-stmts/create-operator-class/), [DROP OPERATOR CLASS](/cloudberry/reference/sql-stmts/drop-operator-class/)
