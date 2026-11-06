---
title: "SET ROLE"
description: "设置当前会话的当前角色标识符。"
weight: 1700
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/set-role.md"
---

## 语法概要 {#synopsis}

```sql
SET [SESSION | LOCAL] ROLE <rolename>

SET [SESSION | LOCAL] ROLE NONE

RESET ROLE
```

## 说明 {#description}

此命令将当前 SQL 会话上下文中的当前角色标识符设为 rolename。角色名可以写成标识符，也可以写成字符串字面量。执行 `SET ROLE` 后，SQL 命令的权限检查就如同指定角色是最初登录的角色一样。

指定的 rolename 必须是当前会话用户所属的角色。如果会话用户是超级用户，则可以选择任意角色。

`NONE` 和 `RESET` 形式将当前角色标识符重置为当前会话角色标识符。任何用户都可以执行这两种形式。

## 参数 {#parameters}

**`SESSION`**

指定命令对当前会话生效。这是默认行为。

**`LOCAL`**

指定命令仅对当前事务生效。在 `COMMIT` 或 `ROLLBACK` 后，会话级设置重新生效。请注意，在事务之外执行 `SET LOCAL` 看起来不会产生任何效果。

**`rolename`**

在此会话中用于权限检查的角色名称。

**`RESET`**

将当前角色标识符重置为当前会话角色标识符（即用于登录的角色的标识符）。

## 注意事项 {#notes}

使用此命令既可以增加权限，也可以限制权限。如果会话用户角色具有 `INHERITS` 属性，则它会自动具有所有可通过 `SET ROLE` 切换到的角色的全部权限；此时，`SET ROLE` 实际上会舍弃直接授予会话用户及其所属其他角色的所有权限，只保留指定角色可用的权限。另一方面，如果会话用户角色具有 `NOINHERITS` 属性，`SET ROLE` 会舍弃直接授予会话用户的权限，转而获得指定角色可用的权限。

特别是，当超级用户选择用 `SET ROLE` 切换到非超级用户角色时，就会失去其超级用户权限。

`SET ROLE` 的效果与 `SET SESSION AUTHORIZATION` 类似，但涉及的权限检查有很大不同。另外，`SET SESSION AUTHORIZATION` 决定后续 `SET ROLE` 命令允许使用哪些角色，而使用 `SET ROLE` 更改角色不会改变后续 `SET ROLE` 所允许的角色集合。

`SET ROLE` 不会处理角色的 `ALTER ROLE` 设置中指定的会话变量；这些会话变量只在登录时处理。

## 示例 {#examples}

```sql
SELECT SESSION_USER, CURRENT_USER;
 session_user | current_user 
--------------+--------------
 peter        | peter

SET ROLE 'paul';

SELECT SESSION_USER, CURRENT_USER;
 session_user | current_user 
--------------+--------------
 peter        | paul
```

## 兼容性 {#compatibility}

Apache Cloudberry 允许标识符语法（rolename），而 SQL 标准要求角色名写成字符串字面量。SQL 不允许在事务期间执行此命令；Apache Cloudberry 没有这一限制。`SESSION` 和 `LOCAL` 修饰符以及 `RESET` 语法都是 Apache Cloudberry 的扩展。

## 另请参阅 {#see-also}

[`SET SESSION AUTHORIZATION`](/cloudberry/reference/sql-stmts/set-session-authorization/)
