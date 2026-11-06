---
title: "DROP TRIGGER"
description: "Removes a trigger."
weight: 1390
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-trigger.md"
---

## Synopsis {#synopsis}

```sql
DROP TRIGGER [IF EXISTS] <name> ON <table> [CASCADE | RESTRICT]
```

## Description {#description}

`DROP TRIGGER` will remove an existing trigger definition. To run this command, the current user must be the owner of the table for which the trigger is defined.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the trigger does not exist. A notice is issued in this case.

**`name`**

The name of the trigger to remove.

**`table`**

The name (optionally schema-qualified) of the table for which the trigger is defined.

**`CASCADE`**

Automatically drop objects that depend on the trigger.

**`RESTRICT`**

Refuse to drop the trigger if any objects depend on it. This is the default.

## Examples {#examples}

Remove the trigger `sendmail` on table `expenses`;

```sql
DROP TRIGGER sendmail ON expenses;
```

## Compatibility {#compatibility}

The `DROP TRIGGER` statement in Apache Cloudberry is not compatible with the SQL standard. In the SQL standard, trigger names are not local to tables, so the command is simply `DROP TRIGGER name`.

## See also {#see-also}

[ALTER TRIGGER](/cloudberry/reference/sql-stmts/alter-trigger/), [CREATE TRIGGER](/cloudberry/reference/sql-stmts/create-trigger/)
