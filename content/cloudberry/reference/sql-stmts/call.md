---
title: "CALL"
description: "Invokes a procedure."
weight: 450
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/call.md"
---

## Synopsis {#synopsis}

```sql
CALL <name> ( [ <argument> ] [, ...] )
```

## Description {#description}

`CALL` executes a procedure.

If the procedure has any output parameters, then a result row will be returned, containing the values of those parameters.

## Parameters {#parameters}

**`name`**

The name (optionally schema-qualified) of the procedure.

**`argument`**

An input argument for the procedure call.

## Notes {#notes}

The user must have `EXECUTE` privilege on the procedure in order to be allowed to invoke it.

To call a function (not a procedure), use [SELECT](/cloudberry/reference/sql-stmts/select/) instead.

If `CALL` is invoked in a transaction block, then the called procedure cannot run transaction control statements. Transaction control statements are only allowed if `CALL` is invoked in its own transaction.

PL/pgSQL handles output parameters in `CALL` commands differently; refer to [Calling a Procedure](https://www.postgresql.org/docs/12/plpgsql-control-structures.html#PLPGSQL-STATEMENTS-CALLING-PROCEDURE) in the PostgreSQL documentation for more information.

## Examples {#examples}

```sql
CALL do_db_maintenance();
```

## Compatibility {#compatibility}

`CALL` conforms to the SQL standard.

## See also {#see-also}

[CREATE PROCEDURE](/cloudberry/reference/sql-stmts/create-procedure/)
