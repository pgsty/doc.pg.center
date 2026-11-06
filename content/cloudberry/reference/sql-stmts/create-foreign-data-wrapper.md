---
title: "CREATE FOREIGN DATA WRAPPER"
description: "Defines a new foreign-data wrapper."
weight: 610
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-foreign-data-wrapper.md"
---

## Synopsis {#synopsis}

```sql
CREATE FOREIGN DATA WRAPPER <name>
    [ HANDLER <handler_function> | NO HANDLER ]
    [ VALIDATOR <validator_function> | NO VALIDATOR ]
    [ OPTIONS ( [ mpp_execute { 'coordinator' | 'any' | 'all segments' } [, ] ] <option> '<value>' [, ... ] ) ]
```

## Description {#description}

`CREATE FOREIGN DATA WRAPPER` creates a new foreign-data wrapper in the current database. The user who defines the foreign-data wrapper becomes its owner.

The foreign-data wrapper name must be unique within the database.

Only superusers can create foreign-data wrappers.

## Parameters {#parameters}

**`name`**

The name of the foreign-data wrapper to create. The name must be unique within the database.

**`HANDLER handler_function`**

The name of a previously registered function that Apache Cloudberry calls to retrieve the execution functions for foreign tables. hander_function must take no arguments, and its return type must be `fdw_handler`.

It is possible to create a foreign-data wrapper with no handler function, but you can only declare, not access, foreign tables using such a wrapper.

**`VALIDATOR validator_function`**

The name of a previously registered function that Apache Cloudberry calls to check the generic options provided to the foreign-data wrapper. This function also checks the options for foreign servers, user mappings, and foreign tables that use the foreign-data wrapper. If no validator function or `NO VALIDATOR` is specified, Apache Cloudberry does not check options at creation time. (Depending upon the implementation, foreign-data wrappers may ignore or reject invalid options at runtime.)

validator_function must take two arguments: one of type `text[]`, which contains the array of options as stored in the system catalogs, and one of type `oid`, which identifies the OID of the system catalog containing the options.

The return type is ignored; validator_function should report invalid options using the `ereport(ERROR)` function.

**`OPTIONS ( option 'value' [, ... ] )`**

The options for the new foreign-data wrapper. Option names must be unique. The option names and values are foreign-data wrapper-specific and are validated using the foreign-data wrappers' validator_function.

**`mpp_execute { 'coordinator' | 'any' | 'all segments' }`**

A Apache Cloudberry-specific option that identifies the host from which the foreign-data wrapper reads or writes data:

- `coordinator` (the default)—Read or write data from the coordinator host.
- `any`—Read data from either the coordinator host or any one segment, depending on which path costs less.
- `all segments`—Read or write data from all segments. To support this option value, the foreign-data wrapper must have a policy that matches the segments to data.

> **Note** Apache Cloudberry supports parallel writes to foreign tables only when you set `mpp_execute 'all segments'`.

Support for the foreign-data wrapper `mpp_execute` option, and the specific modes, is foreign-data wrapper-specific.

The `mpp_execute` option can be specified in multiple commands: `CREATE FOREIGN TABLE`, `CREATE SERVER`, and `CREATE FOREIGN DATA WRAPPER`. The foreign table setting takes precedence over the foreign server setting, followed by the foreign-data wrapper setting.

## Notes {#notes}

The foreign-data wrapper functionality is still under development. Optimization of queries is primitive (and mostly left to the wrapper).

## Examples {#examples}

Create a useless foreign-data wrapper named `dummy`:

```sql
CREATE FOREIGN DATA WRAPPER dummy;
```

Create a foreign-data wrapper named `file` with a handler function named `file_fdw_handler`:

```sql
CREATE FOREIGN DATA WRAPPER file HANDLER file_fdw_handler;
```

Create a foreign-data wrapper named `mywrapper` that includes an option:

```sql
CREATE FOREIGN DATA WRAPPER mywrapper OPTIONS (debug 'true');
```

## Compatibility {#compatibility}

`CREATE FOREIGN DATA WRAPPER` conforms to ISO/IEC 9075-9 (SQL/MED), with the exception that the `HANDLER` and `VALIDATOR` clauses are extensions, and the standard clauses `LIBRARY` and `LANGUAGE` are not implemented in Apache Cloudberry.

Note, however, that the SQL/MED functionality as a whole is not yet conforming.

## See also {#see-also}

[ALTER FOREIGN DATA WRAPPER](/cloudberry/reference/sql-stmts/alter-foreign-data-wrapper/), [DROP FOREIGN DATA WRAPPER](/cloudberry/reference/sql-stmts/drop-foreign-data-wrapper/), [CREATE FOREIGN TABLE](/cloudberry/reference/sql-stmts/create-foreign-table/), [CREATE SERVER](/cloudberry/reference/sql-stmts/create-server/), [CREATE USER MAPPING](/cloudberry/reference/sql-stmts/create-user-mapping/)
