---
title: "DROP CONVERSION"
description: "Removes a conversion."
weight: 1040
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-conversion.md"
---

## Synopsis {#synopsis}

```sql
DROP CONVERSION [IF EXISTS] <name> [CASCADE | RESTRICT]
```

## Description {#description}

`DROP CONVERSION` removes a previously defined conversion. To be able to drop a conversion, you must own the conversion.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the conversion does not exist. A notice is issued in this case.

**`name`**

The name of the conversion. The conversion name may be schema-qualified.

CASCADE
**`RESTRICT`**

These keywords have no effect since there are no dependencies on conversions.

## Examples {#examples}

Drop the conversion named `myname`:

```sql
DROP CONVERSION myname;
```

## Compatibility {#compatibility}

There is no `DROP CONVERSION` statement in the SQL standard. The standard has `CREATE TRANSLATION` and `DROP TRANSLATION` statements that are similar to the Apache Cloudberry `CREATE CONVERSION` and `DROP CONVERSION` statements.

## See also {#see-also}

[ALTER CONVERSION](/cloudberry/reference/sql-stmts/alter-conversion/), [CREATE CONVERSION](/cloudberry/reference/sql-stmts/create-conversion/)
