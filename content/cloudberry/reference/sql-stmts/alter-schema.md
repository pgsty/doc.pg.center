---
title: "ALTER SCHEMA"
description: "Changes the definition of a schema."
weight: 280
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-schema.md"
---

## Synopsis {#synopsis}

```sql
ALTER SCHEMA <name> RENAME TO <new_name>

ALTER SCHEMA <name> OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }
```

## Description {#description}

`ALTER SCHEMA` changes the definition of a schema.

You must own the schema to use `ALTER SCHEMA`. To rename a schema you must also have the `CREATE` privilege for the database. To alter the owner, you must also be a direct or indirect member of the new owning role, and you must have the `CREATE` privilege for the database. Note that superusers have all these privileges automatically.

## Parameters {#parameters}

**`name`**

The name of an existing schema.

**`new_name`**

The new name of the schema. The new name cannot begin with `pg_`, as such names are reserved for system schemas.

**`new_owner`**

The new owner of the schema.

## Compatibility {#compatibility}

There is no `ALTER SCHEMA` statement in the SQL standard.

## See also {#see-also}

[CREATE SCHEMA](/cloudberry/reference/sql-stmts/create-schema/), [DROP SCHEMA](/cloudberry/reference/sql-stmts/drop-schema/)
