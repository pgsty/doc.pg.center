---
title: "SET SESSION AUTHORIZATION"
description: "设置当前会话的会话角色标识符和当前角色标识符。"
weight: 1710
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/set-session-authorization.md"
---

## 语法概要 {#synopsis}

```sql
SET [SESSION | LOCAL] SESSION AUTHORIZATION <rolename>

SET [SESSION | LOCAL] SESSION AUTHORIZATION DEFAULT

RESET SESSION AUTHORIZATION
```

## 说明 {#description}

此命令将当前 SQL 会话上下文中的会话角色标识符和当前角色标识符设为 rolename。角色名可以写成标识符，也可以写成字符串字面量。例如，使用此命令可以暂时成为无特权用户，之后再切换回超级用户。

会话角色标识符最初被设为客户端提供的（可能经过身份验证的）角色名。当前角色标识符通常等于会话用户标识符，但在 `setuid` 函数及类似机制的上下文中可能临时改变；也可以通过 [SET ROLE](/cloudberry/reference/sql-stmts/set-role/) 更改。当前用户标识符用于权限检查。

只有初始会话用户（经过身份验证的用户）具有超级用户权限时，才能更改会话用户标识符。否则，只有指定经过身份验证的用户名时，才会接受此命令。

`DEFAULT` 和 `RESET` 形式将会话用户标识符和当前用户标识符重置为最初经过身份验证的用户名。任何用户都可以执行这两种形式。

## 参数 {#parameters}

**`SESSION`**

指定命令对当前会话生效。这是默认行为。

**`LOCAL`**

指定命令仅对当前事务生效。在 `COMMIT` 或 `ROLLBACK` 后，会话级设置重新生效。请注意，在事务之外执行 `SET LOCAL` 看起来不会产生任何效果。

**`rolename`**

要切换为的角色名称。

**`NONE`**<br />
**`RESET`**

将会话角色标识符和当前角色标识符重置为用于登录的角色的标识符。

## 示例 {#examples}

```sql
SELECT SESSION_USER, CURRENT_USER;
 session_user | current_user 
--------------+--------------
 peter        | peter

SET SESSION AUTHORIZATION 'paul';

SELECT SESSION_USER, CURRENT_USER;
 session_user | current_user 
--------------+--------------
 paul         | paul
```

## 兼容性 {#compatibility}

SQL 标准允许在字面量 rolename 的位置使用其他一些表达式，但这些选项在实践中并不重要。Apache Cloudberry 允许标识符语法（rolename），而 SQL 不允许。SQL 不允许在事务期间执行此命令；Apache Cloudberry 没有这一限制。`SESSION` 和 `LOCAL` 修饰符以及 `RESET` 语法都是 Apache Cloudberry 的扩展。

## 另请参阅 {#see-also}

[SET ROLE](/cloudberry/reference/sql-stmts/set-role/)
