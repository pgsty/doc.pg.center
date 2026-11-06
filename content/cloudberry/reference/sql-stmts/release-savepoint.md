---
title: "RELEASE SAVEPOINT"
description: "Destroys a previously defined savepoint."
weight: 1600
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/release-savepoint.md"
---

## Synopsis {#synopsis}

```sql
RELEASE [SAVEPOINT] <savepoint_name>
```

## Description {#description}

`RELEASE SAVEPOINT` destroys a savepoint previously defined in the current transaction.

Destroying a savepoint makes it unavailable as a rollback point, but it has no other user visible behavior. It does not undo the effects of commands run after the savepoint was established. (To do that, see [ROLLBACK TO SAVEPOINT](/cloudberry/reference/sql-stmts/rollback-to-savepoint/).) Destroying a savepoint when it is no longer needed may allow the system to reclaim some resources earlier than transaction end.

`RELEASE SAVEPOINT` also destroys all savepoints that were established *after* the named savepoint was established.

## Parameters {#parameters}

**`savepoint_name`**

The name of the savepoint to destroy.

## Notes {#notes}

Specifying a savepoint name that was not previously defined is an error.

It is not possible to release a savepoint when the transaction is in an aborted state.

If multiple savepoints have the same name, Apache Cloudberry releases only the most recently defined unreleased savepoint. Repeated commands release progressively older savepoints.

## Examples {#examples}

To establish and later destroy a savepoint:

```sql
BEGIN;
    INSERT INTO table1 VALUES (3);
    SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (4);
    RELEASE SAVEPOINT my_savepoint;
COMMIT;
```

The above transaction inserts both 3 and 4.

## Compatibility {#compatibility}

This command conforms to the SQL standard. The standard specifies that the key word `SAVEPOINT` is mandatory, but Apache Cloudberry allows it to be omitted.

## See also {#see-also}

[BEGIN](/cloudberry/reference/sql-stmts/begin/), [COMMIT](/cloudberry/reference/sql-stmts/commit/), [ROLLBACK](/cloudberry/reference/sql-stmts/rollback/), [ROLLBACK TO SAVEPOINT](/cloudberry/reference/sql-stmts/rollback-to-savepoint/), [SAVEPOINT](/cloudberry/reference/sql-stmts/savepoint/)
