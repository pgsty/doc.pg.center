---
title: "DROP OWNED"
description: "删除数据库角色拥有的数据库对象。"
weight: 1190
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-owned.md"
---

## 概要 {#synopsis}

```sql
DROP OWNED BY { <name> | CURRENT_USER | SESSION_USER } [, ...] [CASCADE | RESTRICT]
```

## 描述 {#description}

`DROP OWNED` 删除当前数据库中指定角色所拥有的所有对象。授予这些角色的、针对当前数据库中的对象或共享对象（数据库、表空间）的权限也会被撤销。

## 参数 {#parameters}

**`name`**

要删除其对象并撤销其权限的角色名称。

**`CASCADE`**

自动删除依赖受影响对象的对象，以及依赖这些对象的所有对象。

**`RESTRICT`**

如果有其他数据库对象依赖任一受影响对象，则拒绝删除该角色拥有的对象。这是默认行为。

## 注意事项 {#notes}

`DROP OWNED` 通常用于为删除一个或多个角色做准备。由于 `DROP OWNED` 只影响当前数据库中的对象，通常需要在每个包含待删除角色所拥有对象的数据库中运行此命令。

使用 `CASCADE` 选项可能使命令递归删除其他用户拥有的对象。

另一种选择是 [REASSIGN OWNED](/cloudberry/reference/sql-stmts/reassign-owned/) 命令，它重新分配一个或多个角色所拥有的全部数据库对象的所有权。不过，`REASSIGN OWNED` 不处理其他对象上的权限。

不会删除这些角色拥有的数据库和表空间。

## 示例 {#examples}

删除名为 `sally` 的角色拥有的数据库对象：

```sql
DROP OWNED BY sally;
```

## 兼容性 {#compatibility}

`DROP OWNED` 命令是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[REASSIGN OWNED](/cloudberry/reference/sql-stmts/reassign-owned/), [DROP ROLE](/cloudberry/reference/sql-stmts/drop-role/)
