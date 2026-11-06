---
title: "REASSIGN OWNED"
description: "Changes the ownership of database objects owned by a database role."
weight: 1570
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/reassign-owned.md"
---

## Synopsis {#synopsis}

```sql
REASSIGN OWNED BY { <old_role> | CURRENT_USER | SESSION_USER } [, ...]
               TO { <new_role> | CURRENT_USER | SESSION_USER }
```

## Description {#description}

`REASSIGN OWNED` changes the ownership of database objects owned by any of the old_roles to new_role.

## Parameters {#parameters}

**`old_role`**

The name of a role. The ownership of all the objects in the current database, and of all shared objects (databases, tablespaces), owned by this role will be reassigned to new_role.

**`new_role`**

The name of the role that will be made the new owner of the affected objects.

## Notes {#notes}

`REASSIGN OWNED` is often used to prepare for the removal of one or more roles. Because `REASSIGN OWNED` does not affect objects in other databases, it is usually necessary to run this command in each database that contains objects owned by a role that is to be removed.

`REASSIGN OWNED` requires privileges on both the source role(s) and the target role.

The [DROP OWNED](/cloudberry/reference/sql-stmts/drop-owned/) command is an alternative that simply drops all of the database objects owned by one or more roles.

The `REASSIGN OWNED` command does not affect any privileges granted to the old_roles on objects that are not owned by them. Likewise, it does not affect default privileges created with `ALTER DEFAULT PRIVILEGES`. Use `DROP OWNED` to revoke such privileges.

## Examples {#examples}

Reassign any database objects owned by the role named `sally` and `bob` to `admin`:

```sql
REASSIGN OWNED BY sally, bob TO admin;
```

## Compatibility {#compatibility}

The `REASSIGN OWNED` command is a Apache Cloudberry extension.

## See also {#see-also}

[DROP OWNED](/cloudberry/reference/sql-stmts/drop-owned/), [DROP ROLE](/cloudberry/reference/sql-stmts/drop-role/), [ALTER DATABASE](/cloudberry/reference/sql-stmts/alter-database/)
