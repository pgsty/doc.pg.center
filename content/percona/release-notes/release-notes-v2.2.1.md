---
title: pg_tde 2.2.1 (2026-07-06)
linkTitle: 2.2.1
description: Changes, compatibility notes, and fixes for pg_tde 2.2.1 (2026-07-06).
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/release-notes/release-notes-v2.2.1.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 820
upstream_source: percona
---

> [!NOTE] Historical release
> This page describes this release at publication time. For current deployment requirements, read the [supported versions](/percona/index/supported-versions/) and [limitations](/percona/index/tde-limitations/).

The `pg_tde` extension, provided by Percona, adds [Transparent Data Encryption (TDE)](/percona/index/about-tde/) to PostgreSQL and helps protect sensitive data at rest.

[Get Started](/percona/install/)

## Release Highlights {#release-highlights}

`pg_tde` 2.2.1 focuses on stability and compatibility improvements. This release improves `pg_rewind` reliability. For more details, see the [Changelog](#changelog).

> [!WARNING]
> `pg_tde` 2.2.1 is not compatible with Percona Distribution for PostgreSQL older than 17.10.2 or 18.4.2.

## Known issues {#known-issues}

* The default `mlock` limit on Rocky Linux 8 for ARM64-based architectures equals the memory page size and is 64 Kb. This results in the child process with `pg_tde` failing to allocate another memory page because the max memory limit is reached by the parent process.

    To prevent this, you can change the `mlock` limit to be at least twice the memory page size:

    * temporarily for the current session using the `ulimit -l <value>` command.
    * set a new hard limit in the `/etc/security/limits.conf` file. To do so, you require the superuser privileges.

    Adjust the limits with caution since it affects other processes running in your system.

## Changelog {#changelog}

Changes introduced in `pg_tde` 2.2.1:

### New Features {#new-features}

- [PG-2398](https://perconadev.atlassian.net/browse/PG-2398) - PostgreSQL 16 support

### Bug Fixes {#bug-fixes}

- [PG-2407](https://perconadev.atlassian.net/browse/PG-2407) - Fixed multiple issues affecting `pg_rewind` for `pg_tde` clusters, improving reliability during rewind and recovery operations.
- [PG-2258](https://perconadev.atlassian.net/browse/PG-2258) - Fixed "could not find server principal key" error from `pg_tde_basebackup`

### Changes {#changes}

- Remove support for building `pg_tde` with `make`, now it can only be built with Meson
