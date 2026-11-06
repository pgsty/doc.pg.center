---
title: "REASSIGN OWNED"
description: "更改数据库角色所拥有的数据库对象的所有权。"
weight: 1570
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/reassign-owned.md"
---

## 概要 {#synopsis}

```sql
REASSIGN OWNED BY { <old_role> | CURRENT_USER | SESSION_USER } [, ...]
               TO { <new_role> | CURRENT_USER | SESSION_USER }
```

## 描述 {#description}

`REASSIGN OWNED` 将任一 old_roles 角色拥有的数据库对象的所有权更改为 new_role。

## 参数 {#parameters}

**`old_role`**

角色名称。该角色拥有的当前数据库中的全部对象以及所有共享对象（数据库、表空间）的所有权都会重新分配给 new_role。

**`new_role`**

将成为受影响对象的新所有者的角色名称。

## 注意事项 {#notes}

`REASSIGN OWNED` 通常用于为删除一个或多个角色做准备。由于 `REASSIGN OWNED` 不影响其他数据库中的对象，通常需要在每个包含待删除角色所拥有对象的数据库中运行此命令。

`REASSIGN OWNED` 要求同时拥有源角色和目标角色的权限。

另一种选择是 [DROP OWNED](/cloudberry/reference/sql-stmts/drop-owned/) 命令，它直接删除一个或多个角色拥有的全部数据库对象。

`REASSIGN OWNED` 命令不影响授予 old_roles 的、针对非其所有对象的权限。同样，它也不影响通过 `ALTER DEFAULT PRIVILEGES` 创建的默认权限。使用 `DROP OWNED` 可撤销这些权限。

## 示例 {#examples}

将名为 `sally` 和 `bob` 的角色拥有的数据库对象重新分配给 `admin`：

```sql
REASSIGN OWNED BY sally, bob TO admin;
```

## 兼容性 {#compatibility}

`REASSIGN OWNED` 命令是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[DROP OWNED](/cloudberry/reference/sql-stmts/drop-owned/), [DROP ROLE](/cloudberry/reference/sql-stmts/drop-role/), [ALTER DATABASE](/cloudberry/reference/sql-stmts/alter-database/)
