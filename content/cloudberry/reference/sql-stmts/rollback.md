---
title: "ROLLBACK"
description: "Stops the current transaction."
weight: 1650
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/rollback.md"
---

## Synopsis {#synopsis}

```sql
ROLLBACK [WORK | TRANSACTION] [AND [NO] CHAIN]
```

## Description {#description}

`ROLLBACK` rolls back the current transaction and causes all the updates made by the transaction to be discarded.

## Parameters {#parameters}

**`WORK`**<br />
**`TRANSACTION`**

Optional key words. They have no effect.

**`AND CHAIN`**

If `AND CHAIN` is specified, a new transaction is immediately started with the same transaction characteristics (see [`SET TRANSACTION`](/cloudberry/reference/sql-stmts/set-transaction/)) as the just finished one. Otherwise, no new transaction is started.

## Notes {#notes}

Use [`COMMIT`](/cloudberry/reference/sql-stmts/commit/) to successfully end the current transaction.

Issuing `ROLLBACK` when not inside a transaction block emits a warning and otherwise has no effect. `ROLLBACK AND CHAIN` outside of a transaction block is an error.

## Examples {#examples}

To discard all changes made in the current transaction:

```sql
ROLLBACK;
```

## Compatibility {#compatibility}

The command `ROLLBACK` conforms to the SQL standard. The form `ROLLBACK TRANSACTION` is a Apache Cloudberry extension.

## See also {#see-also}

[`BEGIN`](/cloudberry/reference/sql-stmts/begin/), [`COMMIT`](/cloudberry/reference/sql-stmts/commit/), [`ROLLBACK TO SAVEPOINT`](/cloudberry/reference/sql-stmts/rollback-to-savepoint/), [`SAVEPOINT`](/cloudberry/reference/sql-stmts/savepoint/)
