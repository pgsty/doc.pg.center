---
title: pg_tde 2.2.2 (2026-08-20)
linkTitle: 2.2.2
description: Changes, compatibility notes, and fixes for pg_tde 2.2.2 (2026-08-20).
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/release-notes/release-notes-v2.2.2.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 810
upstream_source: percona
---

The `pg_tde` extension, provided by Percona, adds [Transparent Data Encryption (TDE)](/percona/index/about-tde/) to PostgreSQL and helps protect sensitive data at rest.

[Get Started](/percona/install/)

## Release Highlights {#release-highlights}

`pg_tde` 2.2.2 focuses on fixing an issue with performance of WAL encryption and adding support for KMIP with HashiCorp Vault Enterprise. Vault Enterprise was already supported via the Vault V2 protocol, but now KMIP can be used too.

> [!WARNING]
> `pg_tde` 2.2.2 is not compatible with Percona Distribution for PostgreSQL older than 17.10.2 or 18.4.2.

## Known issues {#known-issues}

* The default `mlock` limit on Rocky Linux 8 for ARM64-based architectures equals the memory page size and is 64 Kb. This results in the child process with `pg_tde` failing to allocate another memory page because the max memory limit is reached by the parent process.

    To prevent this, you can change the `mlock` limit to be at least twice the memory page size:

    * temporarily for the current session using the `ulimit -l <value>` command.
    * set a new hard limit in the `/etc/security/limits.conf` file. To do so, you require the superuser privileges.

    Adjust the limits with caution since it affects other processes running in your system.

## Changelog {#changelog}

Changes introduced in `pg_tde` 2.2.2:

### New Features {#new-features}

- [PG-2125](https://perconadev.atlassian.net/browse/PG-2125) - Support using HashiCorp Vault Enterprise with KMIP
- [PG-2473](https://perconadev.atlassian.net/browse/PG-2473) - Basic support for building on Windows with Microsoft Visual C++

### Improvements {#improvements}

- [PG-2494](https://perconadev.atlassian.net/browse/PG-2494) - Improved performance of WAL encryption

### Bug Fixes {#bug-fixes}

- [PG-2492](https://perconadev.atlassian.net/browse/PG-2492) - Fixed crash when empty certificate parameters are passed to `pg_tde_add_global_key_provider_kmip()` or `pg_tde_add_database_key_provider_kmip()`
- [PG-2608](https://perconadev.atlassian.net/browse/PG-2608) - Fixed a race condition in the Vault key provider that could occur when multiple processes accessed the same cURL handle after a fork.
- [PG-2609](https://perconadev.atlassian.net/browse/PG-2609) - Fixed WAL archiving (`pg_tde_archive_decrypt` and `pg_tde_restore_encrypt`) when pg_wal dir is a symlink.
- Include bugfixes for frontend tools from PostgreSQL 16.15, 17.11 and 18.5
