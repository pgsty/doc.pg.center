---
title: "DROP FUNCTION"
description: "Removes a function."
weight: 1110
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-function.md"
---

## Synopsis {#synopsis}

```sql
DROP FUNCTION [IF EXISTS] name ( [ [argmode] [argname] argtype [, ...] ] )
    [CASCADE | RESTRICT]
```

## Description {#description}

`DROP FUNCTION` removes the definition of an existing function. To run this command the user must be the owner of the function. The argument types to the function must be specified, since several different functions may exist with the same name and different argument lists.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the function does not exist. A notice is issued in this case.

**`name`**

The name (optionally schema-qualified) of an existing function.

**`argmode`**

The mode of an argument: either `IN`, `OUT`, `INOUT`, or `VARIADIC`. If omitted, the default is `IN`. Note that `DROP FUNCTION` does not actually pay any attention to `OUT` arguments, since only the input arguments are needed to determine the function's identity. So it is sufficient to list the `IN`, `INOUT`, and `VARIADIC` arguments.

**`argname`**

The name of an argument. Note that `DROP FUNCTION` does not actually pay any attention to argument names, since only the argument data types are needed to determine the function's identity.

**`argtype`**

The data type(s) of the function's arguments (optionally schema-qualified), if any.

**`CASCADE`**

Automatically drop objects that depend on the function (such as operators).

**`RESTRICT`**

Refuse to drop the function if any objects depend on it. This is the default.

## Examples {#examples}

This command removes the square root function:

```sql
DROP FUNCTION sqrt(integer);
```

## Compatibility {#compatibility}

A `DROP FUNCTION` statement is defined in the SQL standard, but it is not compatible with this command.

## See also {#see-also}

[CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/), [ALTER FUNCTION](/cloudberry/reference/sql-stmts/alter-function/)
