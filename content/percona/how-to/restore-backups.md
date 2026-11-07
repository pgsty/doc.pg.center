---
title: Restore encrypted backups
linkTitle: Restore encrypted backups
description: Restore encrypted data while retaining access to keys and required metadata.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/how-to/restore-backups.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 560
upstream_source: percona
---

To restore an encrypted backup created with an earlier key, ensure the key is still available in your Key Management System (KMS). The backup remains **encrypted** on disk, `pg_tde` uses the correct key to transparently access the data.

## How pg_tde uses old keys to load backups {#how-pgtde-uses-old-keys-to-load-backups}

* **KMS**: stores the principal key(s) that were active when the backup was made.
* **Encrypted backup**: contains data encrypted with the key available at that time.
* **Current server**: `pg_tde` automatically loads the backup if the key is accessible through the KMS.

The table (internal) keys are stored within the backup. At runtime, `pg_tde` retrieves the principal key(s) from the configured KMS and uses them to decrypt the internal keys, enabling access to the encrypted table data.

> [!NOTE]
> If the required key(s) get deleted or are missing, the backup **cannot** be read.
>
> If the key(s) still exists but the KMS configuration has changed, you can use [`pg_tde_change_key_provider`](/percona/command-line-tools/pg-tde-change-key-provider/) to update the configuration.
>
> However, if the key(s) got deleted from all accessible KMS sources, the encrypted backup is **unrecoverable**.
