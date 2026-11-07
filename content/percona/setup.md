---
title: Configure pg_tde
linkTitle: Load the extension
description: Preload the library, restart PostgreSQL, and enable the extension in a database.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/setup.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 230
upstream_source: percona
---

Before you can use `pg_tde` for data encryption, you must enable the extension and configure PostgreSQL to load it at startup. This setup ensures that the necessary hooks and shared memory are available for encryption operations.

> [!NOTE]
> To learn how to configure multi-tenancy, refer to the [Configure multi-tenancy](/percona/how-to/multi-tenant-setup/) guidelines.

The `pg_tde` extension requires additional shared memory. You need to configure PostgreSQL to preload it at startup.

## 1. Configure shared_preload_libraries {#1-configure-sharedpreloadlibraries}

You can configure the `shared_preload_libraries` parameter in two ways:

* Add the following line to the `postgresql.conf` file:

    ```bash
    shared_preload_libraries = 'pg_tde'
    ```

* Use the [ALTER SYSTEM ](https://www.postgresql.org/docs/current/sql-altersystem.html) command. Run the following command in `psql` as a **superuser**:

    ```sql
    ALTER SYSTEM SET shared_preload_libraries = 'pg_tde';
    ```

## 2. Restart the PostgreSQL cluster {#2-restart-the-postgresql-cluster}

Restart the `postgresql` cluster to apply the configuration.

* On Debian and Ubuntu:

       ```sh
       sudo systemctl restart postgresql.service
       ```

* On RHEL and derivatives:

       ```sh
       sudo systemctl restart postgresql-17
       ```

## 3. Create the extension {#3-create-the-extension}

After restarting PostgreSQL, connect to `psql` as a **superuser** or **database owner** and run:

```sql
CREATE EXTENSION pg_tde;
```

See [CREATE EXTENSION ](https://www.postgresql.org/docs/current/sql-createextension.html) for more details.

> [!NOTE]
> The `pg_tde` extension is created only for the current database. To enable it for other databases, you must run the command in each individual database.

## 4. (Optional) Enable pg_tde by default {#4-optional-enable-pgtde-by-default}

To automatically have `pg_tde` enabled for all new databases, modify the `template1` database:

```sql
psql -d template1 -c 'CREATE EXTENSION pg_tde;'
```

> [!NOTE]
> It’s recommended to use an external key provider (KMS) to manage encryption keys. For configuration instructions, see [Next steps](#next-steps).

## Next steps {#next-steps}

[Configure Key Management (KMS) ](/percona/global-key-provider-configuration/overview/)
