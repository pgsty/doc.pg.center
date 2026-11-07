---
title: Overview of pg_tde CLI tools
linkTitle: Tool overview
description: Choose the pg_tde-aware utilities required for encrypted data and WAL.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/command-line-tools/cli-tools.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 710
upstream_source: percona
---

The `pg_tde` extension provides a set of command-line utilities designed specifically for operating on  encrypted data and clusters. These utilities exist in parallel with the standard PostgreSQL utilities but you **must** use them when working with data encrypted by `pg_tde`.

> [!NOTE]
> The standard PostgreSQL tools cannot operate on `pg_tde`-encrypted WAL or tables.

## New `pg_tde` specific tools {#new-pgtde-specific-tools}

These tools are introduced exclusively by `pg_tde` to support key rotation and WAL encryption workflows:

* [pg_tde_change_key_provider](/percona/command-line-tools/pg-tde-change-key-provider/): change the encryption key provider for a database
* [pg_tde_archive_decrypt](/percona/command-line-tools/pg-tde-archive-decrypt/): decrypts WAL before archiving
* [pg_tde_restore_encrypt](/percona/command-line-tools/pg-tde-restore-encrypt/): a custom restore command for making sure the restored WAL is encrypted

## Tools for working with `pg_tde`-encrypted data {#tools-for-working-with-pgtde-encrypted-data}

These tools are modified versions of standard PostgreSQL utilities that include `pg_tde` support. You must use the `pg_tde_*` variants when working with encrypted WAL or tables:

* [pg_tde_checksums](/percona/command-line-tools/pg-tde-checksums/): verify data checksums
* [pg_tde_waldump](/percona/command-line-tools/pg-tde-waldump/): inspect and decrypt WAL files
* [pg_tde_basebackup](/percona/how-to/backup-wal-enabled/): create base backups that include encrypted data
* pg_tde_resetwal: reset the WAL for clusters using `pg_tde`
* pg_tde_rewind: rewind clusters that use encrypted WAL
* [pg_tde_upgrade](/percona/command-line-tools/pg-tde-upgrade/): perform major version upgrades of clusters with `pg_tde`
