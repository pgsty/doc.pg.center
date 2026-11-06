---
title: "SAVEPOINT"
description: "Defines a new savepoint within the current transaction."
weight: 1660
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/savepoint.md"
---

## Synopsis {#synopsis}

```sql
SAVEPOINT <savepoint_name>
```

## Description {#description}

`SAVEPOINT` establishes a new savepoint within the current transaction.

A savepoint is a special mark inside a transaction that allows all commands that are run after it was established to be rolled back, restoring the transaction state to what it was at the time of the savepoint.

## Parameters {#parameters}

**`savepoint_name`**

The name of the new savepoint. If savepoints with the same name already exist, they are inaccessible until newer identically-named savepoints are released.

## Notes {#notes}

Use [`ROLLBACK TO SAVEPOINT`](/cloudberry/reference/sql-stmts/rollback-to-savepoint/) to rollback to a savepoint. Use [`RELEASE SAVEPOINT`](/cloudberry/reference/sql-stmts/release-savepoint/) to destroy a savepoint, keeping the effects of commands run after it was established.

Savepoints can be established only inside a transaction block. You can define multiple savepoints within a transaction.

## Examples {#examples}

To establish a savepoint and later undo the effects of all commands run after it was established:

```sql
BEGIN;
    INSERT INTO table1 VALUES (1);
    SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (2);
    ROLLBACK TO SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (3);
COMMIT;
```

The above transaction inserts the values 1 and 3, but not 2.

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

To use a single savepoint name:

``` sql
BEGIN;
    INSERT INTO table1 VALUES (1);
    SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (2);
    SAVEPOINT my_savepoint;
    INSERT INTO table1 VALUES (3);

    -- rollback to the second savepoint
    ROLLBACK TO SAVEPOINT my_savepoint;
    SELECT * FROM table1;               -- shows rows 1 and 2

    -- release the second savepoint
    RELEASE SAVEPOINT my_savepoint;

    -- rollback to the first savepoint
    ROLLBACK TO SAVEPOINT my_savepoint;
    SELECT * FROM table1;               -- shows only row 1
COMMIT;
```

The above transaction shows row 3 being rolled back first, then row 2.

## Compatibility {#compatibility}

SQL requires a savepoint to be destroyed automatically when another savepoint with the same name is established. In Apache Cloudberry, the old savepoint is kept, though only the more recent one is used when rolling back or releasing. (Releasing the newer savepoint will cause the older one to again become accessible to [ROLLBACK TO SAVEPOINT](/cloudberry/reference/sql-stmts/rollback-to-savepoint/) and [RELEASE SAVEPOINT](/cloudberry/reference/sql-stmts/release-savepoint/).) Otherwise, `SAVEPOINT` is fully SQL conforming.

## See also {#see-also}

[`BEGIN`](/cloudberry/reference/sql-stmts/begin/), [`COMMIT`](/cloudberry/reference/sql-stmts/commit/), [`RELEASE SAVEPOINT`](/cloudberry/reference/sql-stmts/release-savepoint/), [`ROLLBACK`](/cloudberry/reference/sql-stmts/rollback/), [`ROLLBACK TO SAVEPOINT`](/cloudberry/reference/sql-stmts/rollback-to-savepoint/)
