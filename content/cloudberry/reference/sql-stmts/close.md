---
title: "CLOSE"
description: "Closes a cursor."
weight: 470
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/close.md"
---

## Synopsis {#synopsis}

```sql
CLOSE { <cursor_name> | ALL }
```

## Description {#description}

`CLOSE` frees the resources associated with an open cursor. After the cursor is closed, no subsequent operations are allowed on it. A cursor should be closed when it is no longer needed.

Every non-holdable open cursor is implicitly closed when a transaction is terminated by `COMMIT` or `ROLLBACK`. A holdable cursor is implicitly closed if the transaction that created it is prematurely ended via `ROLLBACK`. If the creating transaction successfully commits, the holdable cursor remains open until an explicit `CLOSE` is run, or the client disconnects.

## Parameters {#parameters}

**`cursor_name`**

The name of an open cursor to close.

**`ALL`**

Close all open cursors.

## Notes {#notes}

Apache Cloudberry does not have an explicit `OPEN` cursor statement. A cursor is considered open when it is declared. Use the [DECLARE](/cloudberry/reference/sql-stmts/declare/) statement to declare (and open) a cursor.

You can see all available cursors by querying the `pg_cursors` system view.

If a cursor is closed after a savepoint which is later rolled back, the `CLOSE` is not rolled back; that is, the cursor remains closed.

## Examples {#examples}

Close the cursor `portala`:

```sql
CLOSE portala;
```

## Compatibility {#compatibility}

`CLOSE` is fully conforming with the SQL standard. `CLOSE ALL` is a Apache Cloudberry extension.

## See also {#see-also}

[DECLARE](/cloudberry/reference/sql-stmts/declare/), [FETCH](/cloudberry/reference/sql-stmts/fetch/), [MOVE](/cloudberry/reference/sql-stmts/move/), [RETRIEVE](/cloudberry/reference/sql-stmts/retrieve/)
