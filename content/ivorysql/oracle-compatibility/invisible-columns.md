---
title: Invisible Columns
linkTitle: Invisible Columns
description: 'IvorySQL v5.6 documentation: Invisible Columns.'
type: docs
weight: 220
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/7.13.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

## 1. Objective {#objective}

The introduction of this feature is to accommodate Oracle’s invisible column functionality, making database design simpler and enhancing the flexibility of data management. Users will have better control over the visibility of columns.

Invisible columns are also useful during application migration. Making new columns invisible means that they will not be visible to any existing application, but they can still be referenced by any new applications, thus simplifying the online migration of applications.

## 2. Function descriptions {#function-descriptions}

Invisible columns allow users to conceal specific columns during operations like SELECT \*. You can use invisible column to make changes to a table without disrupting applications that use the table. Any generic access of a table does not show the invisible columns in the table. Invisible columns must be explicitly referenced by column names in order to be accessed in queries and other operations.

Support for invisible columns in psql extended describe (\d+) is added, in oracle mode only.

## 3. Test cases {#test-cases}

### 3.1. Create a table with invisible columns {#create-a-table-with-invisible-columns}

```
ivorysql=# CREATE TABLE mytable (a INT, b INT INVISIBLE, c INT);
CREATE TABLE
```

### 3.2. Insert values into invisible columns {#insert-values-into-invisible-columns}

You can insert a value into an invisible column only if you explicitly specify the invisible column in the column list for the INSERT statement. Omitting the column list in the INSERT statement is not allowed. Errors will be reported.

```
ivorysql=# INSERT INTO mytable (a, b, c) VALUES (1,2,3);
INSERT 0 1

ivorysql=# INSERT INTO mytable VALUES (4,5,6);
ERROR:  INSERT has more expressions than target columns
LINE 1: INSERT INTO mytable  VALUES (4,5,6);
```

### 3.3. Display output for invisible columns {#display-output-for-invisible-columns}

You can use a SELECT statement to display output for an invisible column only if you explicitly specify the invisible column in the column list.

```
ivorysql=# select * from mytable;
 a | c
---+---
 1 | 3
(1 row)

ivorysql=# select a,b,c from mytable;
 a | b | c
---+---+---
 1 | 2 | 3
(1 row)
```

### 3.4. Support for invisible columns in psql extended describe (\d+) in Oracle mode {#support-for-invisible-columns-in-psql-extended-describe-d-in-oracle-mode}

```
ivorysql=# \d+ mytable
                                                   Table "public.mytable"
 Column |      Type       | Collation | Nullable | Default | Invisible | Storage | Compression | Stats target | Description
--------+-----------------+-----------+----------+---------+-----------+---------+-------------+--------------+-------------
 a      | pg_catalog.int4 |           |          |         |           | plain   |             |              |
 b      | pg_catalog.int4 |           |          |         | invisible | plain   |             |              |
 c      | pg_catalog.int4 |           |          |         |           | plain   |             |              |
Access method: heap
```

## 4. Limitations {#limitations}

- Modify column is not supported currently. Will be enhanced in later version;

- In Oracle, there are special considerations for invisible columns and column ordering. When a table contains one or more invisible columns, the invisible columns are not included in the column order for the table. We have not yet addressed this part.
