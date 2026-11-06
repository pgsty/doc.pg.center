---
title: "DROP STATISTICS"
description: "Removes extended statistics."
weight: 1310
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-statistics.md"
---

## Synopsis {#synopsis}

```sql
DROP STATISTICS [ IF EXISTS ] <name> [, ...] [ CASCADE | RESTRICT ]
```

## Description {#description}

`DROP STATISTICS` removes statistics object(s) from the database. Only the statistics object's owner, the schema owner, or a superuser can drop a statistics object.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the statistics object does not exist. Apache Cloudberry issues a notice in this case.

**`name`**

The name (optionally schema-qualified) of the statistics object to drop.

CASCADE
**`RESTRICT`**

These key words have no effect, since there are no dependencies on statistics.

## Examples {#examples}

Destroy two statistics objects in different schemas, without failing if they do not exist:

```sql
DROP STATISTICS IF EXISTS
    accounting.users_uid_creation,
    public.grants_user_role;
```

## Compatibility {#compatibility}

There is no `DROP STATISTICS` command in the SQL standard.

## See also {#see-also}

[ALTER STATISTICS](/cloudberry/reference/sql-stmts/alter-statistics/), [CREATE STATISTICS](/cloudberry/reference/sql-stmts/create-statistics/)
