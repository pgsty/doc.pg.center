---
title: "ALTER RULE"
description: "修改规则的定义。"
weight: 270
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-rule.md"
---

## 概要 {#synopsis}

```sql
ALTER RULE name ON <table_name> RENAME TO <new_name>
```

## 说明 {#description}

`ALTER RULE` 用于修改现有规则的属性。目前唯一可用的操作是修改规则的名称。

要使用 `ALTER RULE`，你必须是该规则所应用的表或视图的所有者。

## 参数 {#parameters}

**`name`**

要修改的现有规则的名称。

**`table_name`**

该规则所应用的表或视图的名称（可以带模式限定）。

**`new_name`**

规则的新名称。

## 示例 {#examples}

重命名现有规则：

```sql
ALTER RULE notify_all ON emp RENAME TO notify_me; 
```

## 兼容性 {#compatibility}

`ALTER RULE` 是 Apache Cloudberry 的扩展，整个查询重写系统也是如此。

## 另请参阅 {#see-also}

[`CREATE RULE`](/cloudberry/reference/sql-stmts/create-rule/)、[`DROP RULE`](/cloudberry/reference/sql-stmts/drop-rule/)
