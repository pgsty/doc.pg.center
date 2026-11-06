---
title: "ALTER GROUP"
description: "更改角色名称或成员关系。"
weight: 130
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-group.md"
---

## 概要 {#synopsis}

```sql
ALTER GROUP <role_specification> ADD USER <user_name> [, ... ]

ALTER GROUP <role_specification> DROP USER <user_name> [, ... ]

-- where <role_specification> can be:

    <role_name>
  | CURRENT_USER
  | SESSION_USER

ALTER GROUP <group_name> RENAME TO <new_name>
```

## 描述 {#description}

`ALTER GROUP` 更改用户组的属性。这是一个已过时的命令，不过为了向后兼容仍然被接受，因为用户和组已被更通用的角色概念所取代。

前两种形式向组中添加用户或从组中移除用户。（对于此用途，任何角色都可以充当“用户”或“组”。这些形式实际上等价于授予或撤销被指定为“组”的角色的成员关系；因此，首选的做法是使用 [GRANT](/cloudberry/reference/sql-stmts/grant/) 或 [REVOKE](/cloudberry/reference/sql-stmts/revoke/)。

第三种形式更改组的名称。这与使用 [ALTER ROLE](/cloudberry/reference/sql-stmts/alter-role/) 重命名角色完全等价。

## 参数 {#parameters}

**`group_name`**

要修改的组（角色）的名称。

**`user_name`**

要添加到组或从组中移除的用户（角色）。这些用户（角色）必须已经存在；`ALTER GROUP` 不会创建或删除用户。

**`new_name`**

组的新名称。

## 示例 {#examples}

向组中添加用户：

```sql
ALTER GROUP staff ADD USER karl, john;
```

从组中移除用户：

```sql
ALTER GROUP workers DROP USER beth;
```

## 兼容性 {#compatibility}

SQL 标准中没有 `ALTER GROUP` 语句。

## 另见 {#see-also}

[ALTER ROLE](/cloudberry/reference/sql-stmts/alter-role/)、[GRANT](/cloudberry/reference/sql-stmts/grant/)、[REVOKE](/cloudberry/reference/sql-stmts/revoke/)
