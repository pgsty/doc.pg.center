---
title: "DROP ROUTINE"
description: "Removes a routine."
weight: 1260
upstream_link: "https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/sql-stmts/drop-routine.md"
---

## Synopsis {#synopsis}

```sql
DROP ROUTINE [IF EXISTS] name ( [ [argmode] [argname] argtype [, ...] ] )
    [CASCADE | RESTRICT]
```

## Description {#description}

`DROP ROUTINE` removes the definition of an existing routine, which can be an aggregate function, a normal function, or a procedure. Refer to [DROP AGGREGATE](/cloudberry/reference/sql-stmts/drop-aggregate/), [DROP FUNCTION](/cloudberry/reference/sql-stmts/drop-function/), and [DROP PROCEDURE](/cloudberry/reference/sql-stmts/drop-procedure/) for the description of the parameters, more examples, and further details.

## Examples {#examples}

To drop the routine `foo` for type `integer`:

```sql
DROP ROUTINE foo(integer);
```

This command will work independent of whether `foo` is an aggregate, function, or procedure.

## Compatibility {#compatibility}

This command conforms to the SQL standard, with these Apache Cloudberry extensions:

- The standard only allows one routine to be dropped per command.

- The `IF EXISTS` option.

- The ability to specify argument modes and names.

- Aggregate functions are an extension.

## See also {#see-also}

[DROP AGGREGATE](/cloudberry/reference/sql-stmts/drop-aggregate/), [DROP FUNCTION](/cloudberry/reference/sql-stmts/drop-function/), [DROP PROCEDURE](/cloudberry/reference/sql-stmts/drop-procedure/), [ALTER ROUTINE](/cloudberry/reference/sql-stmts/alter-routine/)
