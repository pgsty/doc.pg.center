---
title: Keyring file configuration
linkTitle: Local keyring
description: Configure a plaintext file keyring for local development and testing.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/global-key-provider-configuration/keyring.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 320
upstream_source: percona
---

> [!NOTE] Editorial correction
> The inspection example now uses the table it creates and the current database key-info function. See [site errata](/percona/site/errata/).

This setup is intended for development and stores the keys, unencrypted, in a data file you specify.

> [!NOTE]
>  While keyring files may be acceptable for **local** or **testing environments**, proper [KMS providers](/percona/global-key-provider-configuration/overview/) are the recommended approach for production deployments.

You can configure key providers either at the database level (for development and testing) or at the global level (for production).

The steps below provide an example on how to add a [database-scoped key provider](/percona/functions/#add-or-modify-local-key-file-providers):

1. Create a database-scoped file key provider (`file-keyring` in this example) in the `/tmp/pg_tde_test_local_keyring.per` file:

    ```sql
    SELECT pg_tde_add_database_key_provider_file(
        'file-keyring',
        '/tmp/pg_tde_test_local_keyring.per'
    );
    ```

2. Create a key (`my_default_key` in this example) inside the newly created `file-keyring` provider:

    ```sql
    SELECT pg_tde_create_key_using_database_key_provider(
        'my_default_key',
        'file-keyring'
    );
    ```

3. Set the key (`my_default_key`) from the key provider (`file-keyring`):

    ```sql
    SELECT pg_tde_set_key_using_database_key_provider(
        'my_default_key',
        'file-keyring'
    );
    ```

    > [!TIP]
    > You can check the current database key information (such as the date and time of creation). Run:
    >
    > ```sql
    > SELECT pg_tde_key_info();
    > ```

4. Now, create a table using [tde_heap](/percona/index/table-access-method/#how-tdeheap-works-with-pgtde):

    ```sql
    CREATE TABLE customer_table (a INT) USING tde_heap;
    ```

    The newly created table is encrypted with the database key you have set (`my_default_key`).

    > [!TIP]
    > To check if your created table is encrypted with tde_heap, run:
    >
    > ```sql
    > \d+ customer_table
    > ```
    >
    > If `Access method: tde_heap`, then your table is encrypted.
    >
    > > [!DETAILS] Example output
    > >     postgres=# \d+ customer_table
    > >                                         Table "public.customer_table"
    > >     Column |  Type   | Collation | Nullable | Default | Storage | Compression | Stats target | Description
    > >     --------+---------+-----------+----------+---------+---------+-------------+--------------+-------------
    > >     a      | integer |           |          |         | plain   |             |              |
    > >     Access method: tde_heap

## Further reading {#further-reading}

Next, for production deployments, [configure a global principal key](/percona/global-key-provider-configuration/set-principal-key/) using a proper [KMS provider](/percona/global-key-provider-configuration/overview/).

Alternatively, you can skip directly to [validating encryption with pg_tde](/percona/test/) or [configuring WAL encryption](/percona/wal-encryption/).

You can also review the available `pg_tde` functions in [Functions](/percona/functions/).
