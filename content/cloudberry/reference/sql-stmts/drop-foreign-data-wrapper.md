---
title: "DROP FOREIGN DATA WRAPPER"
description: "Removes a foreign-data wrapper."
weight: 1090
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-foreign-data-wrapper.md"
---

## Synopsis {#synopsis}

```sql
DROP FOREIGN DATA WRAPPER [ IF EXISTS ] <name> [ CASCADE | RESTRICT ]
```

## Description {#description}

`DROP FOREIGN DATA WRAPPER` removes an existing foreign-data wrapper from the current database. A foreign-data wrapper may be removed only by its owner.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the foreign-data wrapper does not exist. Apache Cloudberry issues a notice in this case.

**`name`**

The name of an existing foreign-data wrapper.

**`CASCADE`**

Automatically drop objects that depend on the foreign-data wrapper (such as foreign tables and servers), and in turn all objects that depend on those objects.

**`RESTRICT`**

Refuse to drop the foreign-data wrapper if any object depends on it. This is the default.

## Examples {#examples}

Drop the foreign-data wrapper named `dbi`:

```sql
DROP FOREIGN DATA WRAPPER dbi;
```

## Compatibility {#compatibility}

`DROP FOREIGN DATA WRAPPER` conforms to ISO/IEC 9075-9 (SQL/MED). The `IF EXISTS` clause is a Apache Cloudberry extension.

## See also {#see-also}

[CREATE FOREIGN DATA WRAPPER](/cloudberry/reference/sql-stmts/create-foreign-data-wrapper/), [ALTER FOREIGN DATA WRAPPER](/cloudberry/reference/sql-stmts/alter-foreign-data-wrapper/)
