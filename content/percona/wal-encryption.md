---
title: Configure WAL encryption
linkTitle: WAL encryption
description: Create and assign the server principal key, then enable encrypted WAL writes.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/wal-encryption.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 510
upstream_source: percona
---

WAL encryption requires a principal key. You can satisfy this requirement in one of the following ways:

> [!WARNING] WAL archiving and recovery requirements
>
> A deployment with WAL encryption is not supported unless you use both of the following tools for WAL archiving and recovery:
>
> * [`pg_tde_archive_decrypt`](/percona/command-line-tools/pg-tde-archive-decrypt/) in `archive_command`
> * [`pg_tde_restore_encrypt`](/percona/command-line-tools/pg-tde-restore-encrypt/) in `restore_command`
>
> If you use pgBackRest, you must also disable its asynchronous archiving, WAL header checks, and page checksum validation. Add these settings to the applicable pgBackRest configuration section:
>
> ```ini
> archive-async=n
> archive-header-check=n
> checksum-page=n
> ```

## Option 1: Use the default principal key {#option-1-use-the-default-principal-key}

If a default principal key is already configured for the server, WAL encryption uses it automatically. No additional server key configuration is required.

If you have not yet configured a default principal key, see [Default Principal Key configuration](/percona/global-key-provider-configuration/set-principal-key/).

## Option 2: Configure a dedicated server principal key for WAL {#option-2-configure-a-dedicated-server-principal-key-for-wal}

> [!NOTE]
> For a comprehensive list of supported `pg_tde` WAL encryption tools see [Limitations of pg_tde](/percona/index/tde-limitations/).

1. Create the `pg_tde` extension if it does not exist:

    ```sql
    CREATE EXTENSION IF NOT EXISTS pg_tde;
    ```

2. Configure a global key provider

    Before creating the server (principal) key for WAL encryption, you must first configure a global key provider. See [Key management overview](/percona/global-key-provider-configuration/overview/) for detailed instructions on configuring supported key providers.

3. Create the server (principal) key using the global key provider

    The server key (also referred to as the principal key) is the key used by PostgreSQL to encrypt WAL data. See [pg_tde_create_key_using_global_key_provider](/percona/functions/#pgtdecreatekeyusingglobalkeyprovider) for  more detailed instructions.

4. Set the server (principal) key

    This step sets the previously created server (principal) key as the active key used by PostgreSQL for WAL encryption. See [pg_tde_set_server_key_using_global_key_provider](/percona/functions/#pgtdesetserverkeyusingglobalkeyprovider) for  more detailed instructions.

5. Enable WAL encryption using the `ALTER SYSTEM` command. You need the privileges of the superuser to run this command:

    ```sql
    ALTER SYSTEM SET pg_tde.wal_encrypt = on;
    ```

6. Restart the server to apply the changes.

    * On Debian and Ubuntu:

    ```sh
    sudo systemctl restart postgresql
    ```

    * On RHEL and derivatives

    ```sh
    sudo systemctl restart postgresql-<version>
    ```

7. (Optional) Verify that WAL encryption is enabled:

    ```sql
    SHOW pg_tde.wal_encrypt;
    ```

Now WAL files start to be encrypted for both encrypted and unencrypted tables.

For more technical references related to architecture, variables or functions, see:
[Technical Reference](/percona/advanced-topics/tech-reference/)

💬 Need help customizing this for your infrastructure? [Contact Percona support ](/percona/get-help/)
