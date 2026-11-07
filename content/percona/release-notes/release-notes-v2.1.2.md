---
title: pg_tde 2.1.2 (2026-03-02)
linkTitle: 2.1.2
description: Changes, compatibility notes, and fixes for pg_tde 2.1.2 (2026-03-02).
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/release-notes/release-notes-v2.1.2.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 840
upstream_source: percona
---

> [!NOTE] Historical release
> This page describes this release at publication time. For current deployment requirements, read the [supported versions](/percona/index/supported-versions/) and [limitations](/percona/index/tde-limitations/).

The `pg_tde` extension, provided by Percona, adds [Transparent Data Encryption (TDE)](/percona/index/about-tde/) to PostgreSQL and helps protect sensitive data at rest.

[Get Started](/percona/install/)

## Release Highlights {#release-highlights}

### Documentation updates {#documentation-updates}

* The [Architecture](/percona/architecture/overview/) documentation is redesigned for improved clarity and readability. The chapter is now split into smaller, more focused sections.
* The [Technical reference overview](/percona/advanced-topics/tech-reference/) is updated with quick-skim cards for quick topic access.
* A dedicated [Usage reference](/percona/advanced-topics/usage-guide/) topic is introduced which describes the main `pg_tde` operations available.

## Known issues {#known-issues}

* `pg_rewind` and `pg_tde_rewind`

    Using `pg_rewind` or `pg_tde_rewind` between diverged nodes in clusters that use `pg_tde` may lead to corrupted tables or indexes due to internal encryption key differences between clusters.

    Queries may fail with:

    ```bash
    ERROR: invalid page in block 0 of relation "base/..."
    ```

    This behavior is a known issue.

    For more information, see [pg_tde limitations](/percona/index/tde-limitations/).

* `pg_upgrade` is currently unsupported when `pg_tde` is enabled

    PostgreSQL clusters that use `pg_tde` cannot currently be upgraded using `pg_upgrade`.

* Do not create, change, or rotate global key providers (or their keys) while `pg_tde_basebackup` is running. Doing so may cause standbys or clusters initialized from the backup to fail during WAL replay and may result in corruption of encrypted data (tables, indexes, and other relations).

* Using `pg_tde_basebackup` with `--wal-method=fetch` produces warnings.

    This behavior is expected and will be addressed in a future release.

* The default `mlock` limit on Rocky Linux 8 for ARM64-based architectures equals the memory page size and is 64 Kb. This results in the child process with `pg_tde` failing to allocate another memory page because the max memory limit is reached by the parent process.

    To prevent this, you can change the `mlock` limit to be at least twice bigger than the memory page size:

    * temporarily for the current session using the `ulimit -l <value>` command.
    * set a new hard limit in the `/etc/security/limits.conf` file. To do so, you require the superuser privileges.

    Adjust the limits with caution since it affects other processes running in your system.

## Changelog {#changelog}

### Improvements {#improvements}

* [PG-2088 ](https://perconadev.atlassian.net/browse/PG-2088), [PG-2179 ](https://perconadev.atlassian.net/browse/PG-2179) - Improved handling of Vault/OpenBao KV v2 mount point validation in `pg_tde`. The extension no longer fails when configured with tokens that lack access to mount metadata endpoints and now works correctly with tokens that have only the required KV v2 read/write permissions.

### Bugs Fixed {#bugs-fixed}

* Updated `pg_tde` CLI tools to include upstream bug fixes and stability improvements from PostgreSQL 18.2 and 17.8.
