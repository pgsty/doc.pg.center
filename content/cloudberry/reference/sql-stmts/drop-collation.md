---
title: "DROP COLLATION"
description: "Removes a previously defined collation."
weight: 1030
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-collation.md"
---

## Synopsis {#synopsis}

```sql
DROP COLLATION [ IF EXISTS ] <name> [ CASCADE | RESTRICT ]
```

## Description {#description}

`DROP COLLATION` removes a previously defined collation. To be able to drop a collation, you must own the collation.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the collation does not exist. A notice is issued in this case.

**`name`**

The name of the collation. The collation name can be schema-qualified.

**`CASCADE`**

Automatically drop objects that depend on the collation, and in turn all objects that depend on those objects.

**`RESTRICT`**

Refuse to drop the collation if any objects depend on it. This is the default.

## Examples {#examples}

To drop the collation named `german`:

```sql
DROP COLLATION german;
```

## Compatibility {#compatibility}

The `DROP COLLATION` command conforms to the SQL standard, apart from the `IF EXISTS` option, which is a Apache Cloudberry extension.

## See also {#see-also}

[ALTER COLLATION](/cloudberry/reference/sql-stmts/alter-collation/), [CREATE COLLATION](/cloudberry/reference/sql-stmts/create-collation/)
