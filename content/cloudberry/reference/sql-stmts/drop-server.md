---
title: "DROP SERVER"
description: "Removes a foreign server descriptor."
weight: 1300
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-server.md"
---

## Synopsis {#synopsis}

```sql
DROP SERVER [ IF EXISTS ] <name> [, ...] [ CASCADE | RESTRICT ]
```

## Description {#description}

`DROP SERVER` removes an existing foreign server descriptor. The user running this command must be the owner of the server.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the server does not exist. Apache Cloudberry issues a notice in this case.

**`name`**

The name of an existing server.

**`CASCADE`**

Automatically drop objects that depend on the server (such as user mappings), and in turn all objects that depend on those objects.

**`RESTRICT`**

Refuse to drop the server if any object depends on it. This is the default.

## Examples {#examples}

Drop the server named `foo` if it exists:

```sql
DROP SERVER IF EXISTS foo;
```

## Compatibility {#compatibility}

`DROP SERVER` conforms to ISO/IEC 9075-9 (SQL/MED). The `IF EXISTS` clause is a Apache Cloudberry extension.

## See also {#see-also}

[CREATE SERVER](/cloudberry/reference/sql-stmts/create-server/), [ALTER SERVER](/cloudberry/reference/sql-stmts/alter-server/)
