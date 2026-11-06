---
title: "SET SESSION AUTHORIZATION"
description: "Sets the session role identifier and the current role identifier of the current session."
weight: 1710
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/set-session-authorization.md"
---

## Synopsis {#synopsis}

```sql
SET [SESSION | LOCAL] SESSION AUTHORIZATION <rolename>

SET [SESSION | LOCAL] SESSION AUTHORIZATION DEFAULT

RESET SESSION AUTHORIZATION
```

## Description {#description}

This command sets the session role identifier and the current role identifier of the current SQL-session context to be rolename. The role name may be written as either an identifier or a string literal. Using this command, it is possible, for example, to temporarily become an unprivileged user and later switch back to being a superuser.

The session role identifier is initially set to be the (possibly authenticated) role name provided by the client. The current role identifier is normally equal to the session user identifier, but may change temporarily in the context of `setuid` functions and similar mechanisms; it can also be changed by [SET ROLE](/cloudberry/reference/sql-stmts/set-role/). The current user identifier is relevant for permission checking.

The session user identifier may be changed only if the initial session user (the authenticated user) had the superuser privilege. Otherwise, the command is accepted only if it specifies the authenticated user name.

The `DEFAULT` and `RESET` forms reset the session and current user identifiers to be the originally authenticated user name. These forms may be run by any user.

## Parameters {#parameters}

**`SESSION`**

Specifies that the command takes effect for the current session. This is the default.

**`LOCAL`**

Specifies that the command takes effect for only the current transaction. After `COMMIT` or `ROLLBACK`, the session-level setting takes effect again. Note that `SET LOCAL` will appear to have no effect if it is run outside of a transaction.

**`rolename`**

The name of the role to assume.

**`NONE`**<br />
**`RESET`**

Reset the session and current role identifiers to be that of the role used to log in.

## Examples {#examples}

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

## Compatibility {#compatibility}

The SQL standard allows some other expressions to appear in place of the literal rolename, but these options are not important in practice. Apache Cloudberry allows identifier syntax (rolename), which SQL does not. SQL does not allow this command during a transaction; Apache Cloudberry does not make this restriction. The `SESSION` and `LOCAL` modifiers are a Apache Cloudberry extension, as is the `RESET` syntax.

## See also {#see-also}

[SET ROLE](/cloudberry/reference/sql-stmts/set-role/)
