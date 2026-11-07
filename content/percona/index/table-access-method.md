---
title: Table access methods and pg_tde
linkTitle: Table access methods
description: Use tde_heap explicitly or as the default access method for new tables.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/index/table-access-method.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 170
upstream_source: percona
---

A table access method is the way how PostgreSQL stores the data in a table. The default table access method is `heap`. PostgreSQL organizes data in a heap structure, meaning there is no particular order to the rows in the table. Each row is stored independently and identified by its unique row identifier (TID).

## How the heap access method works {#how-the-heap-access-method-works}

**Insertion**: When a new row is inserted, PostgreSQL finds a free space in the tablespace and stores the row there.

**Deletion**: When a row is deleted, PostgreSQL marks the space occupied by the row as free, but the data remains until it is overwritten by a new insertion.

**Updates**: PostgreSQL handles updates by deleting the old row and inserting a new row with the updated values.

## Custom access method {#custom-access-method}

Custom access methods allow you to implement and define your own way of organizing data in PostgreSQL. This is useful if the default table access method doesn't meet your needs.

Custom access methods are typically available with PostgreSQL extensions. When you install an extension and enable it in PostgreSQL, a custom access method is created.

An example of such an approach is the `tde_heap` access method. It is automatically created **only** for the databases where you [enabled the `pg_tde` extension](/percona/setup/) and configured the key provider, enabling you to encrypt the data.

To use a custom access method, specify the `USING` clause for the `CREATE TABLE` command:

```sql
CREATE TABLE table_name (
    column1 data_type,
    column2 data_type,
    ...
) USING tde_heap;
```

### How tde_heap works with pg_tde {#how-tdeheap-works-with-pgtde}

The `tde_heap` access method works on top of the default `heap` access method and is a marker to point which tables require encryption. It uses the custom storage manager TDE SMGR, which becomes active only after you installed the `pg_tde` extension.

Every data modification operation is first sent to the Buffer Manager, which updates the buffer cache. Then, it is passed to the storage manager, which then writes it to disk. When a table requires encryption, the data is sent to the TDE storage manager, where it is encrypted before written to disk.

Similarly, when a client queries the database, the PostgreSQL core sends the request to the Buffer Manager which checks if the requested data is already in the buffer cache. If it’s not there, the Buffer Manager requests the data from the storage manager. The TDE storage manager  reads the encrypted data from disk, decrypts it and loads it to the buffer cache. The Buffer Manager sends the requested data to the PostgreSQL core and then to the client.

Thus, the encryption is done at the storage manager level.

## Changing the default table access method {#changing-the-default-table-access-method}

You can change the default table access method so that every table in the entire database cluster is created using the custom access method. For example, you can enable data encryption by default by defining the `tde_heap` as the default table access method.

However, consider the following before making this change:

* This is a global setting and applies across the entire database cluster and not just a single database.
We recommend setting it with caution because all tables and materialized views created without an explicit access method in their `CREATE` statement will default to the specified table access method.
* You must create the `pg_tde` extension and configure the key provider for all databases before you modify the configuration. Otherwise PostgreSQL won't find the specified access method and will throw an error.

Here is how you can set the new default table access method:

1. Add the access method to the `default_table_access_method` parameter:

    {{< tabs group="via-the-alter-system-command-via-the-configuration-file-via-the-set-command" >}}
    {{< tab label="via the `ALTER SYSTEM` command" value="via-the-alter-system-command" >}}

    Use `ALTER SYSTEM`, it requires superuser or `ALTER SYSTEM` privileges.

    ```sql
    ALTER SYSTEM SET default_table_access_method = tde_heap;
    ```

    {{< /tab >}}
    {{< tab label="via the configuration file" value="via-the-configuration-file" >}}

    Edit the `postgresql.conf` configuration file and add the value for the `default_table_access_method` parameter.

    ```ini
    default_table_access_method = 'tde_heap'
    ```  

    {{< /tab >}}
    {{< tab label="via the `SET` command" value="via-the-set-command" >}}

    You can use the SET command to change the default table access method temporarily, for the current session. 

    Unlike modifying the `postgresql.conf` file or using the `ALTER SYSTEM` command, the changes you make via the `SET` command don't persist after the session ends.

    You also don't need to have the superuser privileges to run the `SET` command.

    You can run the SET command anytime during the session. 

    ```sql
    SET default_table_access_method = tde_heap;
    ```

    {{< /tab >}}
    {{< /tabs >}}

2. Reload the configuration to apply the changes:

    ```sql
    SELECT pg_reload_conf();
    ```

[Understand pg_tde's limitations ](/percona/index/tde-limitations/)
