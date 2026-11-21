---
title: "pg_tde 2.3.0 (2026-11-17)"
weight: 1
upstream_source: percona-20261121
upstream_link: https://github.com/percona/pg_tde/blob/5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a/documentation/docs/release-notes/release-notes-v2.3.0.md
---

> [!NOTE] Release date
> The 2.3.0 tag was published on November 17, 2026. The upstream documentation date variable was still `TBD` at this pinned revision.

The `pg_tde` extension, provided by Percona, adds [Transparent Data Encryption (TDE)](/percona/index/about-tde/) to PostgreSQL and helps protect sensitive data at rest.

[Get Started](/percona/install/)

## Release Highlights {#release-highlights}

`pg_tde` 2.3.0 adds support for PostgreSQL 19 and makes `pg_tde_waldump` aware of the `pg_tde` custom resource manager. For more details, see the [Changelog](#changelog).

## Known issues {#known-issues}

* The default `mlock` limit on Rocky Linux 8 for ARM64-based architectures equals the memory page size and is 64 Kb. This results in the child process with `pg_tde` failing to allocate another memory page because the max memory limit is reached by the parent process.

    To prevent this, you can change the `mlock` limit to be at least twice the memory page size:

    * temporarily for the current session using the `ulimit -l <value>` command.
    * set a new hard limit in the `/etc/security/limits.conf` file. To do so, you require the superuser privileges.

    Adjust the limits with caution since it affects other processes running in your system.

## Changelog {#changelog}

Changes introduced in `pg_tde` 2.3.0:

### New Features {#new-features}

- [PG-2536](https://perconadev.atlassian.net/browse/PG-2536), [PG-2813](https://perconadev.atlassian.net/browse/PG-2813) - Support for PostgreSQL 19

### Improvements {#improvements}

- [PG-2754](https://perconadev.atlassian.net/browse/PG-2754) - `pg_tde_waldump` now recognises the `pg_tde` custom resource manager, prints proper data for its records and accepts it in the `--rmgr` filter
