---
title: "ABORT"
description: "Terminates the current transaction."
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/abort.md"
---

## Synopsis {#synopsis}

```sql
ABORT [WORK | TRANSACTION] [AND [NO] CHAIN]
```

## Description {#description}

`ABORT` rolls back the current transaction and causes all the updates made by the transaction to be discarded. This command is identical in behavior to the standard SQL command [`ROLLBACK`](/cloudberry/reference/sql-stmts/rollback/), and is present only for historical reasons.

## Parameters {#parameters}

**`WORK`**<br />
**`TRANSACTION`**

Optional key words. They have no effect.

**`AND CHAIN`**

If `AND CHAIN` is specified, a new transaction is immediately started with the same transaction characteristics (see [SET TRANSACTION](/cloudberry/reference/sql-stmts/set-transaction/)) as the just finished one. Otherwise, no new transaction is started.

## Notes {#notes}

Use [`COMMIT`](/cloudberry/reference/sql-stmts/commit/) to successfully terminate a transaction.

Issuing `ABORT` outside of a transaction block emits a warning and otherwise has no effect.

## Examples {#examples}

To terminate all changes:

```sql
ABORT;
```

## Compatibility {#compatibility}

This command is a Apache Cloudberry extension present for historical reasons. `ROLLBACK` is the equivalent standard SQL command.

## See also {#see-also}

[`BEGIN`](/cloudberry/reference/sql-stmts/begin/), [`COMMIT`](/cloudberry/reference/sql-stmts/commit/), [`ROLLBACK`](/cloudberry/reference/sql-stmts/rollback/)
