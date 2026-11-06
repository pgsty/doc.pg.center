---
title: "DROP CAST"
description: "删除类型转换。"
weight: 1020
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-cast.md"
---

## 概要 {#synopsis}

```sql
DROP CAST [IF EXISTS] (<sourcetype> AS <targettype>) [CASCADE | RESTRICT]
```

## 描述 {#description}

`DROP CAST` 删除先前定义的类型转换。必须拥有源数据类型或目标数据类型才能删除该转换；这与创建类型转换所需的权限相同。

## 参数 {#parameters}

**`IF EXISTS`**

如果类型转换不存在，不报错，而是发出一条提示。

**`sourcetype`**

类型转换的源数据类型名称。

**`targettype`**

类型转换的目标数据类型名称。

CASCADE
**`RESTRICT`**

这些关键字没有效果，因为不存在对类型转换的依赖。

## 示例 {#examples}

删除从 `text` 类型到 `int` 类型的转换：

```sql
DROP CAST (text AS int);
```

## 兼容性 {#compatibility}

`DROP CAST` 命令符合 SQL 标准。

## 另见 {#see-also}

[CREATE CAST](/cloudberry/reference/sql-stmts/create-cast/)
