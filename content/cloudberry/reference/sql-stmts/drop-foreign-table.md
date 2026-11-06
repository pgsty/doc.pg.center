---
title: "DROP FOREIGN TABLE"
description: "Removes a foreign table."
weight: 1100
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-foreign-table.md"
---

## Synopsis {#synopsis}

```sql
DROP FOREIGN TABLE [ IF EXISTS ] <name> [, ...] [ CASCADE | RESTRICT ]
```

## Description {#description}

`DROP FOREIGN TABLE` removes an existing foreign table. Only the owner of a foreign table can remove it.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the foreign table does not exist. Apache Cloudberry issues a notice in this case.

**`name`**

The name (optionally schema-qualified) of the foreign table to drop.

**`CASCADE`**

Automatically drop objects that depend on the foreign table (such as views), and in turn all objects that depend on those objects.

**`RESTRICT`**

Refuse to drop the foreign table if any objects depend on it. This is the default.

## Examples {#examples}

To destroy two foreign tables, `films` and `distributors`:

```sql
DROP FOREIGN TABLE films, distributors;
```

## Compatibility {#compatibility}

`DROP FOREIGN TABLE` conforms to ISO/IEC 9075-9 (SQL/MED), except that the standard only allows one foreign table to be dropped per command. The `IF EXISTS` clause is a Apache Cloudberry extension.

## See also {#see-also}

[ALTER FOREIGN TABLE](/cloudberry/reference/sql-stmts/alter-foreign-table/), [CREATE FOREIGN TABLE](/cloudberry/reference/sql-stmts/create-foreign-table/)
