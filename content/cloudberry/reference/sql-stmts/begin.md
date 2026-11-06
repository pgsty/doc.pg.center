---
title: "BEGIN"
description: "Starts a transaction block."
weight: 440
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/begin.md"
---

## Synopsis {#synopsis}

```sql
BEGIN [WORK | TRANSACTION] [<transaction_mode>]

-- where <transaction_mode> is:

   ISOLATION LEVEL {READ UNCOMMITTED | READ COMMITTED | REPEATABLE READ | SERIALIZABLE}
   READ WRITE | READ ONLY
   [NOT] DEFERRABLE
```

## Description {#description}

`BEGIN` initiates a transaction block, that is, all statements after a `BEGIN` command will be run in a single transaction until an explicit [COMMIT](/cloudberry/reference/sql-stmts/commit/) or [ROLLBACK](/cloudberry/reference/sql-stmts/rollback/) is given. By default (without `BEGIN`), Apache Cloudberry runs transactions in "autocommit" mode, that is, each statement is run in its own transaction and a commit is implicitly performed at the end of the statement (if execution was successful, otherwise a rollback is done).

Statements are run more quickly in a transaction block, because transaction start/commit requires significant CPU and disk activity. Execution of multiple statements inside a transaction is also useful to ensure consistency when making several related changes: other sessions will be unable to see the intermediate states wherein not all the related updates have been done.

If the isolation level, read/write mode, or deferrable mode is specified, the new transaction has those characteristics, as if [SET TRANSACTION](/cloudberry/reference/sql-stmts/set-transaction/) was run.

## Parameters {#parameters}

WORK
**`TRANSACTION`**

Optional key words. They have no effect.

Refer to [SET TRANSACTION](/cloudberry/reference/sql-stmts/set-transaction/) for information on the meaning of the other parameters to this statement.

## Notes {#notes}

[START TRANSACTION](/cloudberry/reference/sql-stmts/start-transaction/) has the same functionality as `BEGIN`.

Use [COMMIT](/cloudberry/reference/sql-stmts/commit/) or [ROLLBACK](/cloudberry/reference/sql-stmts/rollback/) to terminate a transaction block.

Issuing `BEGIN` when already inside a transaction block will provoke a warning message. The state of the transaction is not affected. To nest transactions within a transaction block, use savepoints (see [SAVEPOINT](/cloudberry/reference/sql-stmts/savepoint/)).

For reasons of backwards compatibility, the commas between successive transaction_modes can be omitted.

## Examples {#examples}

To begin a transaction block:

```sql
BEGIN;
```

## Compatibility {#compatibility}

`BEGIN` is a Apache Cloudberry language extension. It is equivalent to the SQL-standard command [START TRANSACTION](/cloudberry/reference/sql-stmts/start-transaction/), whose reference page contains additional compatibility information.

The `DEFERRABLE` transaction_mode is a Apache Cloudberry language extension.

Incidentally, the `BEGIN` key word is used for a different purpose in embedded SQL. You are advised to be careful about the transaction semantics when porting database applications.

## See also {#see-also}

[COMMIT](/cloudberry/reference/sql-stmts/commit/), [ROLLBACK](/cloudberry/reference/sql-stmts/rollback/), [SAVEPOINT](/cloudberry/reference/sql-stmts/savepoint/), [START TRANSACTION](/cloudberry/reference/sql-stmts/start-transaction/)
