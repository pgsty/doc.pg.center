---
title: Remove encryption from an encrypted table
linkTitle: Remove encryption from an encrypted table
description: Rewrite a tde_heap table with the standard heap access method.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/how-to/decrypt.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 580
upstream_source: percona
---

## Method 1. Change the access method {#method-1-change-the-access-method}

If you encrypted a table with the `tde_heap` access method and need to remove the encryption from it, run the following command against the desired table (`mytable` in the example below):

```sql
ALTER TABLE mytable SET ACCESS METHOD heap;
```

Note that the `SET ACCESS METHOD` command drops hint bits and this may affect performance. Running a plain `SELECT count(*)` or `VACUUM` command on the entire table will check every tuple for visibility and set its hint bits. Therefore, after executing the `ALTER TABLE` command, run a simple `count(*)` on your tables:

```sql
SELECT count(*) FROM mytable;
```

Check that the table is not encrypted:

```sql
SELECT pg_tde_is_encrypted('mytable');
```

The output returns `f` meaning that the table is no longer encrypted.

## Method 2. Create a new not encrypted table on the base of the encrypted one {#method-2-create-a-new-not-encrypted-table-on-the-base-of-the-encrypted-one}

Alternatively, you can create a new not encrypted table with the same structure and data as the initial table. For example, the original encrypted table is `EncryptedCustomers`. Use the following command to create a new table `Customers`:

```sql
CREATE TABLE Customers AS SELECT * FROM EncryptedCustomers;
```

The new table `Customers` inherits the structure and the data from `EncryptedCustomers`.

(Optional) If you no longer need the `EncryptedCustomers` table, you can delete it.

```sql
DROP TABLE EncryptedCustomers;
```
