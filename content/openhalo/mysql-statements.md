---
type: docs
upstream_source: halodb
upstream_link: "" # Original summary; cite the reference below without claiming an upstream licence.
upstream_ref: "Halo Database 1.0.16; documentation snapshot 2026-11-07"
upstream_notice: /attribution/#halodb
title: Compatible MySQL statements
linkTitle: MySQL statements
description: Documented MySQL statement forms for inserts, pagination, prepared statements, and user variables in Halo.
weight: 40
---

The official Halo 1.0.16 SQL syntax page documents the following MySQL-specific forms. The examples show the documented compatibility surface; validate application-specific statements against the exact server build.

## Replace and conflict handling {#replace-and-conflict-handling}

`REPLACE INTO` deletes a row with the same primary or unique key before inserting the new row. `INSERT IGNORE` skips rows that conflict with a primary or unique key. `ON DUPLICATE KEY UPDATE` updates an existing row when a key conflict occurs.

```sql
CREATE TABLE test (
  id INT PRIMARY KEY,
  name VARCHAR(50),
  UNIQUE (name)
);

INSERT INTO test VALUES (1, 'Alice'), (2, 'Bob');
REPLACE INTO test VALUES (1, 'Charlie');
INSERT IGNORE INTO test VALUES (1, 'Duplicate'), (3, 'David');
INSERT INTO test VALUES (1, 'Alice')
  ON DUPLICATE KEY UPDATE name = 'Alice updated';
```

`REPLACE` has delete-then-insert semantics. Check triggers, generated values, foreign keys, and audit behavior before using it as an upsert operation.

## `INSERT ... SET` {#insert-set}

The documented MySQL form uses a `SET` list instead of `VALUES`:

```sql
CREATE TABLE tab1 (
  id INT,
  name1 VARCHAR(128),
  name2 VARCHAR(128),
  UNIQUE (name1)
);

INSERT INTO tab1 SET name1 = 'n1', id = 1, name2 = 'n2';
```

## `LIMIT` pagination {#limit}

Halo documents `LIMIT N`, `LIMIT N,M`, and `LIMIT N OFFSET M`:

```sql
SELECT * FROM events ORDER BY created_at DESC LIMIT 10;
SELECT * FROM events ORDER BY created_at DESC LIMIT 20, 10;
SELECT * FROM events ORDER BY created_at DESC LIMIT 10 OFFSET 20;
```

Use an explicit `ORDER BY` when page stability matters.

## Prepared statements {#prepared-statements}

The SQL-level MySQL form is `PREPARE`, `EXECUTE`, and `DEALLOCATE PREPARE`:

```sql
PREPARE stmt1 FROM 'SELECT ? + ?';
SET @a = 1, @b = 2;
EXECUTE stmt1 USING @a, @b;
DEALLOCATE PREPARE stmt1;
```

Application drivers may use the MySQL binary protocol instead. Test parameter types, generated plans, and connection-pool behavior through the driver used by the application.

## User variables {#user-variables}

MySQL-style user variables use the `@name` form and remain available in the same session:

```sql
SET @myvar = 100;
SELECT @myvar;

SET @name = 'John';
SELECT * FROM users WHERE username = @name;
```

Do not use session variables as a substitute for bind parameters when handling untrusted input.

## Historical smoke-test results {#historical-tests}

An independent report tested OpenHalo `1.0.14.18` with a MySQL 5.7.32 client and recorded successful cases for basic CRUD, joins, views, transactions, ordinary indexes, common string functions, constraints, derived tables, correlated subqueries, and `EXISTS`. Those results are historical smoke tests, not a support guarantee for Halo Database 1.0.16 or every OpenHalo build. See [Known compatibility boundaries](/openhalo/mysql-compatibility-gaps/) for the source and caveats.

## Sources {#sources}

This page is an original summary of the [Halo Database MySQL compatibility reference](https://doc.halodbtech.com/multi-mode-compatibility/mysql/sql-syntax). No public documentation licence was identified; see the [source notice](/attribution/#halodb) for version, copyright, and citation details.
