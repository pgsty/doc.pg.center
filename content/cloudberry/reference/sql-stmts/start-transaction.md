---
title: "START TRANSACTION"
description: "Starts a transaction block."
weight: 1750
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/start-transaction.md"
---

## Synopsis {#synopsis}

```sql
START TRANSACTION [<transaction_mode>] [, ...]

-- where <transaction_mode> is one of:

   ISOLATION LEVEL {SERIALIZABLE | REPEATABLE READ | READ COMMITTED | READ UNCOMMITTED}
   READ WRITE | READ ONLY
   [NOT] DEFERRABLE
```

## Description {#description}

`START TRANSACTION` begins a new transaction block. If the isolation level, read/write mode, or deferrable mode is specified, the new transaction has those characteristics, as if [SET TRANSACTION](/cloudberry/reference/sql-stmts/set-transaction/) was run. This is the same as the [`BEGIN`](/cloudberry/reference/sql-stmts/begin/) command.

## Parameters {#parameters}

Refer to [SET TRANSACTION](/cloudberry/reference/sql-stmts/set-transaction/) for information on the meaning of the parameters to this statement.

## Compatibility {#compatibility}

In the standard, it is not necessary to issue `START TRANSACTION` to start a transaction block: any SQL command implicitly begins a block. Apache Cloudberry's behavior can be seen as implicitly issuing a `COMMIT` after each command that does not follow `START TRANSACTION` (or `BEGIN`), and it is therefore often called 'autocommit'. Other relational database systems may offer an autocommit feature as a convenience.

The `DEFERRABLE` transaction_mode is a Apache Cloudberry language extension.

The SQL standard requires commas between successive transaction_modes, but for historical reasons Apache Cloudberry allows the commas to be omitted.

See also the compatibility section of [SET TRANSACTION](/cloudberry/reference/sql-stmts/set-transaction/).

## See also {#see-also}

[`BEGIN`](/cloudberry/reference/sql-stmts/begin/), [`COMMIT`](/cloudberry/reference/sql-stmts/commit/), [`ROLLBACK`](/cloudberry/reference/sql-stmts/rollback/), [`SAVEPOINT`](/cloudberry/reference/sql-stmts/savepoint/), [`SET TRANSACTION`](/cloudberry/reference/sql-stmts/set-transaction/)
