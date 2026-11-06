---
title: "COMMIT"
description: "Commits the current transaction."
weight: 500
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/commit.md"
---

## Synopsis {#synopsis}

```sql
COMMIT [WORK | TRANSACTION] [AND [NO] CHAIN]
```

## Description {#description}

`COMMIT` commits the current transaction. All changes made by the transaction become visible to others and are guaranteed to be durable if a crash occurs.

## Parameters {#parameters}

**`WORK`**<br />
**`TRANSACTION`**

Optional key words. They have no effect.

**`AND CHAIN`**

If `AND CHAIN` is specified, a new transaction is immediately started with the same transaction characteristics (see [SET TRANSACTION](/cloudberry/reference/sql-stmts/set-transaction/)) as the just finished one. Otherwise, no new transaction is started.

## Notes {#notes}

Use [ROLLBACK](/cloudberry/reference/sql-stmts/rollback/) to prematurely end a transaction.

Issuing `COMMIT` when not inside a transaction does no harm, but it will provoke a warning message. `COMMIT AND CHAIN` when not inside a transaction is an error.

## Examples {#examples}

To commit the current transaction and make all changes permanent:

```sql
COMMIT;
```

## Compatibility {#compatibility}

The command `COMMIT` conforms to the SQL standard. The form `COMMIT TRANSACTION` is a Apache Cloudberry extension.

## See also {#see-also}

[BEGIN](/cloudberry/reference/sql-stmts/begin/), [END](/cloudberry/reference/sql-stmts/end/), [ROLLBACK](/cloudberry/reference/sql-stmts/rollback/), [START TRANSACTION](/cloudberry/reference/sql-stmts/start-transaction/)
