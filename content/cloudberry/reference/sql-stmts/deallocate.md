---
title: "DEALLOCATE"
description: "Deallocates a prepared statement."
weight: 950
upstream_link: "https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/sql-stmts/deallocate.md"
---

## Synopsis {#synopsis}

```sql
DEALLOCATE [PREPARE] { <name> | ALL }
```

## Description {#description}

`DEALLOCATE` is used to deallocate a previously prepared SQL statement. If you do not explicitly deallocate a prepared statement, it is deallocated when the session ends.

For more information on prepared statements, see [PREPARE](/cloudberry/reference/sql-stmts/prepare/).

## Parameters {#parameters}

**`PREPARE`**

Optional key word which is ignored.

**`name`**

The name of the prepared statement to deallocate.

**`ALL`**

Deallocate all prepared statements

## Examples {#examples}

Deallocate the previously prepared statement named `insert_names`:

```sql
DEALLOCATE insert_names;
```

## Compatibility {#compatibility}

The SQL standard includes a `DEALLOCATE` statement, but it is only for use in embedded SQL.

## See also {#see-also}

[EXECUTE](/cloudberry/reference/sql-stmts/execute/), [PREPARE](/cloudberry/reference/sql-stmts/prepare/)
