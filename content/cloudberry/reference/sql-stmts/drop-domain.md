---
title: "DROP DOMAIN"
description: "Removes a domain."
weight: 1060
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-domain.md"
---

## Synopsis {#synopsis}

```sql
DROP DOMAIN [IF EXISTS] <name> [, ...]  [CASCADE | RESTRICT]
```

## Description {#description}

`DROP DOMAIN` removes a previously defined domain. Only the owner of a domain can remove it.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the domain does not exist. A notice is issued in this case.

**`name`**

The name (optionally schema-qualified) of an existing domain.

**`CASCADE`**

Automatically drop objects that depend on the domain (such as table columns), and in turn all objects that depend on those objects.

**`RESTRICT`**

Refuse to drop the domain if any objects depend on it. This is the default.

## Examples {#examples}

Remove the domain named `us_postal_code`:

```sql
DROP DOMAIN us_postal_code;
```

## Compatibility {#compatibility}

This command conforms to the SQL standard, except for the `IF EXISTS` option, which is a Apache Cloudberry extension.

## See also {#see-also}

[ALTER DOMAIN](/cloudberry/reference/sql-stmts/alter-domain/), [CREATE DOMAIN](/cloudberry/reference/sql-stmts/create-domain/)
