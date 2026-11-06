---
title: "ALTER TABLESPACE"
description: "Changes the definition of a tablespace."
weight: 330
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-tablespace.md"
---

## Synopsis {#synopsis}

```sql
ALTER TABLESPACE <name> RENAME TO <new_name>

ALTER TABLESPACE <name> OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }

ALTER TABLESPACE <name> SET ( <tablespace_option> = <value> [, ... ] )

ALTER TABLESPACE <name> RESET ( <tablespace_option> [, ... ] )
```

## Description {#description}

`ALTER TABLESPACE` changes the definition of a tablespace.

You must own the tablespace to use `ALTER TABLESPACE`. To alter the owner, you must also be a direct or indirect member of the new owning role. (Note that superusers have these privileges automatically.)

## Parameters {#parameters}

**`name`**

The name of an existing tablespace.

**`new_name`**

The new name of the tablespace. The new name cannot begin with `pg_` or `gp_ `(reserved for system tablespaces).

**`new_owner`**

The new owner of the tablespace.

**`tablespace_parameter`**

A tablespace parameter to set or reset. Currently, the only available parameters are `seq_page_cost` and `random_page_cost`. Setting either value for a particular tablespace will override the planner's usual estimate of the cost of reading pages from tables in that tablespace, as established by the configuration parameters of the same name (see `seq_page_cost`, `random_page_cost`). This may be useful if one tablespace is located on a disk which is faster or slower than the remainder of the I/O subsystem.

## Examples {#examples}

Rename tablespace `index_space` to `fast_raid`:

```sql
ALTER TABLESPACE index_space RENAME TO fast_raid;
```

Change the owner of tablespace `index_space`:

```sql
ALTER TABLESPACE index_space OWNER TO mary;
```

## Compatibility {#compatibility}

There is no `ALTER TABLESPACE` statement in the SQL standard.

## See also {#see-also}

[`CREATE TABLESPACE`](/cloudberry/reference/sql-stmts/create-tablespace/), [`DROP TABLESPACE`](/cloudberry/reference/sql-stmts/drop-tablespace/)
