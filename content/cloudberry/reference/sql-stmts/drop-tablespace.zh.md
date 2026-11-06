---
title: "DROP TABLESPACE"
description: "删除表空间。"
weight: 1330
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-tablespace.md"
---

## 概要 {#synopsis}

```sql
DROP TABLESPACE [IF EXISTS] <name>
```

## 描述 {#description}

`DROP TABLESPACE` 从系统中删除表空间。

只有表空间所有者或超级用户才能删除表空间。表空间必须不包含任何数据库对象才能删除。即使当前数据库中没有对象使用该表空间，其他数据库的对象仍可能驻留其中。另外，如果任一活动会话的 temp_tablespaces 设置中列出了该表空间，`DROP TABLESPACE` 可能因其中驻留的临时文件而失败。

## 参数 {#parameters}

**`IF EXISTS`**

如果表空间不存在，不报错；Apache Cloudberry 会发出一条提示。

**`name`**

要删除的表空间名称。

## 注意事项 {#notes}

不能在事务块中运行 `DROP TABLESPACE`。

应在系统活动较少时运行 `DROP TABLESPACE`，避免并发创建表和临时对象引发问题。删除表空间期间存在一个很短的时间窗口，此时仍可能在正在删除的表空间中创建表。如果发生这种情况，Apache Cloudberry 会返回警告。下面是 `DROP TABLESPACE` 警告的示例。

```sql
testdb=# DROP TABLESPACE mytest; 
WARNINGtablespace with oid "16415" is not empty  (seg1 192.168.8.145:25433 pid=29023)
WARNINGtablespace with oid "16415" is not empty  (seg0 192.168.8.145:25432 pid=29022)
WARNINGtablespace with oid "16415" is not empty
DROP TABLESPACE
```

表空间目录中的表数据不会被删除。可以使用 [ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/) 命令更改表所定义的表空间，并将数据移至现有表空间。

## 示例 {#examples}

删除表空间 `mystuff`：

```sql
DROP TABLESPACE mystuff;
```

## 兼容性 {#compatibility}

`DROP TABLESPACE` 是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[`CREATE TABLESPACE`](/cloudberry/reference/sql-stmts/create-tablespace/), [`ALTER TABLESPACE`](/cloudberry/reference/sql-stmts/alter-tablespace/)
