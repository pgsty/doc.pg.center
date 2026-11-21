---
title: "END"
description: "Commits the current transaction."
weight: 1440
upstream_link: "https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/sql-stmts/end.md"
---

## Synopsis {#synopsis}

```sql
END [WORK | TRANSACTION] [AND [NO] CHAIN]
```

## Description {#description}

`END` commits the current transaction. All changes made by the transaction become visible to others and are guaranteed to be durable if a crash occurs. This command is a Apache Cloudberry extension that is equivalent to [`COMMIT`](/cloudberry/reference/sql-stmts/commit/).

## Parameters {#parameters}

**`WORK`**<br />
**`TRANSACTION`**

Optional keywords. They have no effect.

**`AND CHAIN`**

If `AND CHAIN` is specified, a new transaction is immediately started with the same transaction characteristics (see [SET TRANSACTION](/cloudberry/reference/sql-stmts/set-transaction/)) as the just finished one. Otherwise, no new transaction is started.

## Notes {#notes}

Use [`ROLLBACK`](/cloudberry/reference/sql-stmts/rollback/) to terminate a transaction.

Issuing `END` when not inside a transaction does no harm, but it will provoke a warning message.

## Examples {#examples}

To commit the current transaction and make all changes permanent:

```sql
END;
```

## Compatibility {#compatibility}

`END` is a Apache Cloudberry extension that provides functionality equivalent to [`COMMIT`](/cloudberry/reference/sql-stmts/commit/), which is specified in the SQL standard.

## See also {#see-also}

[`BEGIN`](/cloudberry/reference/sql-stmts/begin/), [`COMMIT`](/cloudberry/reference/sql-stmts/commit/), [`ROLLBACK`](/cloudberry/reference/sql-stmts/rollback/)
