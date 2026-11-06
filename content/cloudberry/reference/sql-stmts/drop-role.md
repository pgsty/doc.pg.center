---
title: "DROP ROLE"
description: "Removes a database role."
weight: 1250
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-role.md"
---

## Synopsis {#synopsis}

```sql
DROP ROLE [IF EXISTS] <name> [, ...]
```

## Description {#description}

`DROP ROLE` removes the specified role(s). To drop a superuser role, you must be a superuser yourself. To drop non-superuser roles, you must have `CREATE ROLE` privilege.

A role cannot be removed if it is still referenced in any database; an error will be raised if so. Before dropping the role, you must drop all the objects it owns (or reassign their ownership) and revoke any privileges the role has been granted on other objects. The [`REASSIGN OWNED`](/cloudberry/reference/sql-stmts/reassign-owned/) and [`DROP OWNED`](/cloudberry/reference/sql-stmts/drop-owned/) commands can be useful for this purpose.

However, it is not necessary to remove role memberships involving the role; `DROP ROLE` automatically revokes any memberships of the target role in other roles, and of other roles in the target role. The other roles are not dropped nor otherwise affected.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the role does not exist. A notice is issued in this case.

**`name`**

The name of the role to remove.

## Examples {#examples}

Remove the roles named `sally` and `bob`:

```sql
DROP ROLE sally, bob;
```

## Compatibility {#compatibility}

The SQL standard defines `DROP ROLE`, but it allows only one role to be dropped at a time, and it specifies different privilege requirements than Apache Cloudberry uses.

## See also {#see-also}

[`REASSIGN OWNED`](/cloudberry/reference/sql-stmts/reassign-owned/), [`DROP OWNED`](/cloudberry/reference/sql-stmts/drop-owned/), [`CREATE ROLE`](/cloudberry/reference/sql-stmts/create-role/), [ALTER ROLE](/cloudberry/reference/sql-stmts/alter-role/), [`SET ROLE`](/cloudberry/reference/sql-stmts/set-role/)
