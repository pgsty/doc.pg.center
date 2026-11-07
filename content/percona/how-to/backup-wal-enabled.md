---
title: Backup with WAL encryption enabled
linkTitle: Backup with WAL encryption enabled
description: Back up an encrypted cluster and handle WAL with pgBackRest and pg_tde tools.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/how-to/backup-wal-enabled.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 550
upstream_source: percona
---

> [!DANGER]
> Do not rotate encryption keys while a backup is running. This may result in an inconsistent backup and restore failure. This applies to all backup tools.
>
> For more details, see [Limitations of pg_tde](/percona/index/tde-limitations/#limitations-when-using-pgtde).

To create a backup with WAL encryption enabled:

1. Copy the `pg_tde` directory from the source server’s data directory, for example `/var/lib/postgresql/data/pg_tde/`, including the `wal_keys` and `1664_providers` files, to the backup destination directory where `pg_tde_basebackup` will write the backup.

    Also copy any external files referenced by your providers configuration (such as certificate or key files) into the same relative paths under the backup destination, so that they are located and validated by `pg_tde_basebackup -E`.

2. Run:

    ```bash
    pg_tde_basebackup -D /path/to/backup -E [aes_128|aes_256]
    ```

    Where:

    - `-D /path/to/backup` specifies the backup location where you have to copy `pg_tde`.
    - `-E` (or `--encrypt-wal`) enables WAL encryption and validates that the copied `pg_tde` and provider files are present and that the server key is accessible (required). The `-E` option accepts a cipher argument. The currently supported values are `aes_128` and `aes_256`. If `-E` is not specified, `pg_tde_basebackup` attempts to determine the cipher from the server's key. If no cipher can be determined, `pg_tde_basebackup` defaults to `aes_128`.

> [!NOTE]
> - The `-E` flag only works with the `-X stream` option (default). It is not compatible with `-X none` or `-X fetch`. For more information, see [the backup method compatibility with WAL encryption](#backup-method-compatibility-with-wal-encryption).
> - The `-E` flag is only supported with the plain output format (`-F p`). It cannot be used with the tar output format (`-F t`).

## Key rotation during backups {#key-rotation-during-backups}

> [!DANGER]
> Do not rotate encryption keys while a backup is in progress. This applies to all backup tools.
>
> Backups created during key rotation may fail to start during WAL replay and may lead to corruption of encrypted data (tables, indexes, and other relations).
>
> For example, you may see errors such as:
>
> ```sql
> FATAL: failed to retrieve principal key "database_keyXXXX" from key provider "providerYYYY"
> CONTEXT: WAL redo at ... ROTATE_PRINCIPAL_KEY ...
> ```
>
> To ensure standby recoverability, plan key rotations outside backup windows or take a new full backup after rotation completes.

## Restore a backup created with WAL encryption {#restore-a-backup-created-with-wal-encryption}

When you want to restore a backup created with `pg_tde_basebackup -E`:

1. Ensure all external files referenced by your providers configuration (such as certificates or key files) are also present and accessible at the same relative paths.
2. Start PostgreSQL with the restored data directory.

## Backup method compatibility with WAL encryption {#backup-method-compatibility-with-wal-encryption}

Tar format (`-F t`):

* Works with `-X fetch`.
* Does not support `-X stream` when WAL encryption is enabled. Using `pg_tde_basebackup -F t -X stream` will create a broken replica.

Streaming mode (`-X stream`):

* **Must** specify `-E` (`--encrypt-wal`).
* Without `-E`, backups may contain decrypted WAL while `wal_encryption=on` remains in `postgresql.conf` and `pg_tde/wal_keys` are copied. This leads to **startup failures and compromised data in the backup**.

Fetch mode (`-X fetch`):

* Compatible with encrypted WAL without requiring any additional flags.

None (`-X none`):

* Excludes WAL from the backup and is unaffected by WAL encryption.

> [!NOTE]
> If the source server has `pg_tde/wal_keys`, running `pg_tde_basebackup` with `-X none` or `-X fetch` produces warnings such as:
>
> ```sql
> pg_tde_basebackup: warning: the source has WAL keys, but no WAL encryption configured for the target backups
> pg_tde_basebackup: detail: This may lead to exposed data and broken backup
> pg_tde_basebackup: hint: Run pg_tde_basebackup with -E to encrypt streamed WAL
> ```
>
> You can safely ignore the warnings with `-X none` or `-X fetch`, since no WAL streaming occurs.
