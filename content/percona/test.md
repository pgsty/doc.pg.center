---
title: Validate Encryption with pg_tde
linkTitle: Verify encryption
description: Create or convert a table with tde_heap and verify its encryption status.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/test.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 240
upstream_source: percona
---

After enabling the `pg_tde` extension for a database, you can begin encrypting data using the `tde_heap` table access method.

## Encrypt data in a new table {#encrypt-data-in-a-new-table}

1. Create a table in the database for which you have [enabled `pg_tde`](/percona/setup/) using the `tde_heap` access method as follows:

    ```sql
    CREATE TABLE <table_name> (<field> <datatype>) USING tde_heap;
    ```

    **Warning:** Example for testing purposes only:

    ```sql
    CREATE TABLE albums (
        album_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        artist_id INTEGER,
        title TEXT NOT NULL,
        released DATE NOT NULL
    ) USING tde_heap;
    ```

    Learn more about table access methods and how you can enable data encryption by default in the [Table Access Methods and TDE](/percona/index/table-access-method/) section.

2. To check if the data is encrypted, run the following function:

    ```sql
    SELECT pg_tde_is_encrypted('table_name');
    ```

    The function returns `true` or `false`.

3. (Optional) Rotate the principal key.

To re-encrypt the data using a new key, see [Principal key management](/percona/functions/#principal-key-management).

## Encrypt existing table {#encrypt-existing-table}

You can encrypt an existing table. It requires rewriting the table, so for large tables, it might take a considerable amount of time.

Run the following command:

```sql
ALTER TABLE table_name SET ACCESS METHOD tde_heap;
```

> [!IMPORTANT]
> Using `SET ACCESS METHOD` drops hint bits which can impact query performance. To restore performance, run:
>
> ```sql
> SELECT count(*) FROM table_name;
> ```
>
> This forces PostgreSQL to check every tuple for visibility and reset the hint bits.

> [!TIP]
> Want to remove encryption later? See how to [decrypt your data](/percona/how-to/decrypt/).

## Next steps {#next-steps}

[Configure WAL encryption ](/percona/wal-encryption/)
