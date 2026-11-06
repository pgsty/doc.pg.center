---
title: "MOVE"
description: "Positions a cursor."
weight: 1540
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/move.md"
---

## Synopsis {#synopsis}

```sql
MOVE [ <forward_direction> [ FROM | IN ] ] <cursor_name>
```

where `<forward_direction>` can be empty or one of:

```sql
    NEXT
    FIRST
    LAST
    ABSOLUTE <count>
    RELATIVE <count>
    <count>
    ALL
    FORWARD
    FORWARD <count>
    FORWARD ALL
```

## Description {#description}

`MOVE` repositions a cursor without retrieving any data. `MOVE` works exactly like the [`FETCH`](/cloudberry/reference/sql-stmts/fetch/) command, except it only positions the cursor and does not return rows.

> **Note** You cannot `MOVE` a `PARALLEL RETRIEVE CURSOR`.

> **Note** Because Apache Cloudberry does not support scrollable cursors, it is not possible to move a cursor position backwards. You can only move a cursor forward in position using `MOVE`.

The parameters for the `MOVE` command are identical to those of the `FETCH` command; refer to [`FETCH`](/cloudberry/reference/sql-stmts/fetch/) for details on syntax and usage.

## Outputs {#outputs}

On successful completion, a `MOVE` command returns a command tag of the form

```sql
MOVE <count>
```

The count is the number of rows that a `FETCH` command with the same parameters would have returned (possibly zero).

## Examples {#examples}

Start the transaction:

```sql
BEGIN;
```

Create a cursor:

```sql
DECLARE mycursor CURSOR FOR SELECT * FROM films;
```

Skip the first 5 rows in the cursor `mycursor`:

```sql
MOVE FORWARD 5 IN mycursor;
MOVE 5
```

Fetch the next row after that (row 6):

```sql
FETCH 1 FROM mycursor;
 code  | title  | did | date_prod  |  kind  |  len
-------+--------+-----+------------+--------+-------
 P_303 | 48 Hrs | 103 | 1982-10-22 | Action | 01:37
(1 row)
```

Close the cursor and end the transaction:

```sql
CLOSE mycursor;
COMMIT;
```

## Compatibility {#compatibility}

There is no `MOVE` statement in the SQL standard.

## See also {#see-also}

[DECLARE](/cloudberry/reference/sql-stmts/declare/), [FETCH](/cloudberry/reference/sql-stmts/fetch/), [CLOSE](/cloudberry/reference/sql-stmts/close/)
