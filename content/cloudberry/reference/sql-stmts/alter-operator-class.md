---
title: "ALTER OPERATOR CLASS"
description: "Changes the definition of an operator class."
weight: 170
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-operator-class.md"
---

## Synopsis {#synopsis}

```sql
ALTER OPERATOR CLASS <name> USING <index_method> RENAME TO <new_name>

ALTER OPERATOR CLASS <name> USING <index_method> OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }

ALTER OPERATOR CLASS <name> USING <index_method> SET SCHEMA <new_schema>
```

## Description {#description}

`ALTER OPERATOR CLASS` changes the definition of an operator class.

You must own the operator class to use `ALTER OPERATOR CLASS`. To alter the owner, you must also be a direct or indirect member of the new owning role, and that role must have `CREATE` privilege on the operator class's schema. (These restrictions enforce that altering the owner does not do anything you could not do by dropping and recreating the operator class. However, a superuser can alter ownership of any operator class anyway.)

## Parameters {#parameters}

**`name`**

The name (optionally schema-qualified) of an existing operator class.

**`index_method`**

The name of the index method this operator class is for.

**`new_name`**

The new name of the operator class.

**`new_owner`**

The new owner of the operator class

**`new_schema`**

The new schema for the operator class.

## Compatibility {#compatibility}

There is no `ALTER OPERATOR CLASS` statement in the SQL standard.

## See also {#see-also}

[CREATE OPERATOR CLASS](/cloudberry/reference/sql-stmts/create-operator-class/), [DROP OPERATOR CLASS](/cloudberry/reference/sql-stmts/drop-operator-class/), [ALTER OPERATOR FAMILY](/cloudberry/reference/sql-stmts/alter-operator-family/)
