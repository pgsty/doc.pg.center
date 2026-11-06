---
title: "ALTER TRIGGER"
description: "Changes the definition of a trigger."
weight: 380
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-trigger.md"
---

## Synopsis {#synopsis}

```sql
ALTER TRIGGER <name> ON <table> RENAME TO <newname>
```

## Description {#description}

`ALTER TRIGGER` changes properties of an existing trigger. The `RENAME` clause changes the name of the given trigger without otherwise changing the trigger definition. You must own the table on which the trigger acts to be allowed to change its properties.

## Parameters {#parameters}

**`name`**

The name of an existing trigger to alter.

**`table`**

The name of the table on which this trigger acts.

**`newname`**

The new name for the trigger.

## Notes {#notes}

The ability to temporarily activate or deactivate a trigger is provided by [ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/), not by `ALTER TRIGGER`, because `ALTER TRIGGER` has no convenient way to express the option of activating or deactivating all of a table's triggers at once.

Note that Apache Cloudberry has limited support of triggers in this release. See [CREATE TRIGGER](/cloudberry/reference/sql-stmts/create-trigger/) for more information.

## Examples {#examples}

To rename an existing trigger:

```sql
ALTER TRIGGER emp_stamp ON emp RENAME TO emp_track_chgs;
```

## Compatibility {#compatibility}

`ALTER TRIGGER` is a Apache Cloudberry extension of the SQL standard.

## See also {#see-also}

[ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/), [CREATE TRIGGER](/cloudberry/reference/sql-stmts/create-trigger/), [DROP TRIGGER](/cloudberry/reference/sql-stmts/drop-trigger/)
