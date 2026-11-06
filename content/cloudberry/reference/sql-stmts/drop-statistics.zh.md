---
title: "DROP STATISTICS"
description: "删除扩展统计信息。"
weight: 1310
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-statistics.md"
---

## 概要 {#synopsis}

```sql
DROP STATISTICS [ IF EXISTS ] <name> [, ...] [ CASCADE | RESTRICT ]
```

## 描述 {#description}

`DROP STATISTICS` 从数据库中删除统计信息对象。只有统计信息对象所有者、模式所有者或超级用户才能删除统计信息对象。

## 参数 {#parameters}

**`IF EXISTS`**

如果统计信息对象不存在，不报错；Apache Cloudberry 会发出一条提示。

**`name`**

要删除的统计信息对象名称（可带模式限定）。

CASCADE
**`RESTRICT`**

这些关键字没有效果，因为不存在对统计信息的依赖。

## 示例 {#examples}

删除不同模式中的两个统计信息对象，在对象不存在时不报错：

```sql
DROP STATISTICS IF EXISTS
    accounting.users_uid_creation,
    public.grants_user_role;
```

## 兼容性 {#compatibility}

SQL 标准中没有 `DROP STATISTICS` 命令。

## 另见 {#see-also}

[ALTER STATISTICS](/cloudberry/reference/sql-stmts/alter-statistics/), [CREATE STATISTICS](/cloudberry/reference/sql-stmts/create-statistics/)
