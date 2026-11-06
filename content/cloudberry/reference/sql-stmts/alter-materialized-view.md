---
title: "ALTER MATERIALIZED VIEW"
description: "Changes the definition of a materialized view."
weight: 160
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-materialized-view.md"
---

## Synopsis {#synopsis}

```sql
ALTER MATERIALIZED VIEW [ IF EXISTS ] <name> <action> [, ... ]
ALTER MATERIALIZED VIEW <name>
    DEPENDS ON EXTENSION <extension_name>
ALTER MATERIALIZED VIEW [ IF EXISTS ] <name>
    RENAME [ COLUMN ] <column_name> TO <new_column_name>
ALTER MATERIALIZED VIEW [ IF EXISTS ] <name>
    RENAME TO <new_name>
ALTER MATERIALIZED VIEW [ IF EXISTS ] <name>
    SET SCHEMA <new_schema>
ALTER MATERIALIZED VIEW ALL IN TABLESPACE <name> [ OWNED BY <role_name> [, ... ] ]
    SET TABLESPACE <new_tablespace> [ NOWAIT ]

-- where <action> is one of:

    ALTER [ COLUMN ] <column_name> SET STATISTICS <integer>
    ALTER [ COLUMN ] <column_name> SET ( <attribute_option> = <value> [, ... ] )
    ALTER [ COLUMN ] <column_name> RESET ( <attribute_option> [, ... ] )
    ALTER [ COLUMN ] <column_name> SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN }
    CLUSTER ON <index_name>
    SET WITHOUT CLUSTER
    SET TABLESPACE <new_tablespace>
    SET ( <storage_paramete>r = <value> [, ... ] )
    RESET ( <storage_parameter> [, ... ] )
    OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }
```

## Description {#description}

`ALTER MATERIALIZED VIEW` changes various auxiliary properties of an existing materialized view.

You must own the materialized view to use `ALTER MATERIALIZED VIEW`. To change a materialized view's schema, you must also have `CREATE` privilege on the new schema. To alter the owner, you must also be a direct or indirect member of the new owning role, and that role must have `CREATE` privilege on the materialized view's schema. (These restrictions enforce that altering the owner doesn't do anything you couldn't do by dropping and recreating the materialized view. However, a superuser can alter ownership of any view anyway.)

The `DEPENDS ON EXTENSION` form marks the materialized view as dependent on an extension, such that the materialized view will automatically be dropped if the extension is dropped.

The statement subforms and actions available for `ALTER MATERIALIZED VIEW` are a subset of those available for `ALTER TABLE`, and have the same meaning when used for materialized views. See the descriptions for [ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/) for details.

## Parameters {#parameters}

**`name`**

The name (optionally schema-qualified) of an existing materialized view.

**`column_name`**

Name of a new or existing column.

**`extension_name`**

The name of the extension that the materialized view is to depend on.

**`new_column_name`**

New name for an existing column.

**`new_owner`**

The user name of the new owner of the materialized view.

**`new_name`**

The new name for the materialized view.

**`new_schema`**

The new schema for the materialized view.

## Examples {#examples}

To rename the materialized view `foo` to `bar`:

```sql
ALTER MATERIALIZED VIEW foo RENAME TO bar;
```

## Compatibility {#compatibility}

`ALTER MATERIALIZED VIEW` is a Apache Cloudberry extension of the SQL standard.

## See also {#see-also}

[CREATE MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/create-materialized-view/), [DROP MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/drop-materialized-view/), [REFRESH MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/refresh-materialized-view/)
