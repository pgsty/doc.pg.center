---
title: "DROP AGGREGATE"
description: "Removes an aggregate function."
weight: 1010
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-aggregate.md"
---

## Synopsis {#synopsis}

```sql
DROP AGGREGATE [IF EXISTS] <name> ( <aggregate_signature> ) [, ...] [CASCADE | RESTRICT]

-- where <aggregate_signature> is:

* |
[ <argmode> ] [ <argname> ] <argtype> [ , ... ] |
[ [ <argmode> ] [ <argname> ] <argtype> [ , ... ] ] ORDER BY [ <argmode> ] [ <argname> ] <argtype> [ , ... ]
```

## Description {#description}

`DROP AGGREGATE` removes an existing aggregate function. To run this command the current user must be the owner of the aggregate function.

## Parameters {#parameters}

**`IF EXISTS`**

Do not throw an error if the aggregate does not exist. A notice is issued in this case.

**`name`**

The name (optionally schema-qualified) of an existing aggregate function.

**`argmode`**

The mode of an argument: `IN` or `VARIADIC`. If omitted, the default is `IN`.

**`argname`**

The name of an argument. Note that `DROP AGGREGATE` does not actually pay any attention to argument names, since only the argument data types are needed to determine the aggregate function's identity.

**`argtype`**

An input data type on which the aggregate function operates. To reference a zero-argument aggregate function, write `*` in place of the list of argument specifications. To reference an ordered-set aggregate function, write `ORDER BY` between the direct and aggregated argument specifications.

**`CASCADE`**

Automatically drop objects that depend on the aggregate function (such as views using it) and in turn all objects that depend on those objects.

**`RESTRICT`**

Refuse to drop the aggregate function if any objects depend on it. This is the default.

## Notes {#notes}

Alternative syntaxes for referencing ordered-set aggregates are described under [ALTER AGGREGATE](/cloudberry/reference/sql-stmts/alter-aggregate/).

## Examples {#examples}

To remove the aggregate function `myavg` for type `integer`:

```sql
DROP AGGREGATE myavg(integer);
```

To remove the hypothetical-set aggregate function `myrank`, which takes an arbitrary list of ordering columns and a matching list of direct arguments:

```sql
DROP AGGREGATE myrank(VARIADIC "any" ORDER BY VARIADIC "any");
```

To remove multiple aggregate functions in one command:

```sql
DROP AGGREGATE myavg(integer), myavg(bigint);
```

## Compatibility {#compatibility}

There is no `DROP AGGREGATE` statement in the SQL standard.

## See also {#see-also}

[ALTER AGGREGATE](/cloudberry/reference/sql-stmts/alter-aggregate/), [CREATE AGGREGATE](/cloudberry/reference/sql-stmts/create-aggregate/)
