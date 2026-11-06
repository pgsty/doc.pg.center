---
title: "DROP ROLE"
description: "删除数据库角色。"
weight: 1250
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-role.md"
---

## 概要 {#synopsis}

```sql
DROP ROLE [IF EXISTS] <name> [, ...]
```

## 描述 {#description}

`DROP ROLE` 删除指定角色。要删除超级用户角色，你自己必须是超级用户。要删除非超级用户角色，必须拥有 `CREATE ROLE` 权限。

如果任一数据库中仍有对象引用该角色，则不能删除，否则会报错。删除角色前，必须删除其拥有的所有对象（或重新分配这些对象的所有权），并撤销授予该角色的其他对象上的权限。[`REASSIGN OWNED`](/cloudberry/reference/sql-stmts/reassign-owned/) 和 [`DROP OWNED`](/cloudberry/reference/sql-stmts/drop-owned/) 命令可用于此目的。

不过，无需事先删除涉及该角色的成员关系；`DROP ROLE` 会自动撤销目标角色在其他角色中的成员资格，以及其他角色在目标角色中的成员资格。其他角色不会被删除，也不会受到其他影响。

## 参数 {#parameters}

**`IF EXISTS`**

如果角色不存在，不报错，而是发出一条提示。

**`name`**

要删除的角色名称。

## 示例 {#examples}

删除名为 `sally` 和 `bob` 的角色：

```sql
DROP ROLE sally, bob;
```

## 兼容性 {#compatibility}

SQL 标准定义了 `DROP ROLE`，但只允许一次删除一个角色，且规定的权限要求与 Apache Cloudberry 不同。

## 另见 {#see-also}

[`REASSIGN OWNED`](/cloudberry/reference/sql-stmts/reassign-owned/), [`DROP OWNED`](/cloudberry/reference/sql-stmts/drop-owned/), [`CREATE ROLE`](/cloudberry/reference/sql-stmts/create-role/), [ALTER ROLE](/cloudberry/reference/sql-stmts/alter-role/), [`SET ROLE`](/cloudberry/reference/sql-stmts/set-role/)
