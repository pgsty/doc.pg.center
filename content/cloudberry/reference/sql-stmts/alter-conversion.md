---
title: "ALTER CONVERSION"
description: "Changes the definition of a conversion."
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-conversion.md"
---

## Synopsis {#synopsis}

```sql
ALTER CONVERSION <name> RENAME TO <new_name>

ALTER CONVERSION <name> OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }

ALTER CONVERSION <name> SET SCHEMA <new_schema>
```

## Description {#description}

`ALTER CONVERSION` changes the definition of a conversion.

You must own the conversion to use `ALTER CONVERSION`. To alter the owner, you must also be a direct or indirect member of the new owning role, and that role must have `CREATE` privilege on the conversion's schema. (These restrictions enforce that altering the owner does not do anything you could not do by dropping and recreating the conversion. However, a superuser can alter ownership of any conversion anyway.)

## Parameters {#parameters}

**`name`**

The name (optionally schema-qualified) of an existing conversion.

**`new_name`**

The new name of the conversion.

**`new_owner`**

The new owner of the conversion.

**`new_schema`**

The new schema for the conversion.

## Examples {#examples}

To rename the conversion `iso_8859_1_to_utf8` to `latin1_to_unicode`:

```sql
ALTER CONVERSION iso_8859_1_to_utf8 RENAME TO latin1_to_unicode;
```

To change the owner of the conversion `iso_8859_1_to_utf8` to `joe`:

```sql
ALTER CONVERSION iso_8859_1_to_utf8 OWNER TO joe;
```

## Compatibility {#compatibility}

There is no `ALTER CONVERSION` statement in the SQL standard.

## See also {#see-also}

[CREATE CONVERSION](/cloudberry/reference/sql-stmts/create-conversion/), [DROP CONVERSION](/cloudberry/reference/sql-stmts/drop-conversion/)
