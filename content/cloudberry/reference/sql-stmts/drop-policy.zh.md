---
title: "DROP POLICY"
description: "从表中删除行级安全策略。"
weight: 1200
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-policy.md"
---

## 概要 {#synopsis}

```sql
DROP POLICY [ IF EXISTS ] <name> ON <table_name> [ CASCADE | RESTRICT ]
```

## 描述 {#description}

`DROP POLICY` 从表中删除指定策略。注意，如果删除了表的最后一个策略，而该表仍通过 `ALTER TABLE` 启用了行级安全，则会采用默认拒绝策略。无论表是否存在策略，都可以使用 `ALTER TABLE ... DISABLE ROW LEVEL SECURITY` 禁用该表的行级安全。

## 参数 {#parameters}

**`IF EXISTS`**

如果策略不存在，不报错，而是发出一条提示。

**`name`**

要删除的策略名称。

**`table_name`**

策略所属表的名称（可带模式限定）。

CASCADE
**`RESTRICT`**

这些关键字没有效果，因为不存在对策略的依赖。

## 示例 {#examples}

删除表 `my_table` 上名为 `p1` 的策略：

```sql
DROP POLICY p1 ON my_table;
```

## 兼容性 {#compatibility}

`DROP POLICY` 是 Apache Cloudberry 对 SQL 标准的扩展。

## 另见 {#see-also}

[CREATE POLICY](/cloudberry/reference/sql-stmts/create-policy/), [ALTER POLICY](/cloudberry/reference/sql-stmts/alter-policy/)
