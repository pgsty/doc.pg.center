---
title: pg_tde 2.1.1 (2026-01-22)
linkTitle: 2.1.1
description: Changes, compatibility notes, and fixes for pg_tde 2.1.1 (2026-01-22).
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/release-notes/release-notes-v2.1.1.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 850
upstream_source: percona
---

> [!NOTE] Historical release
> This page describes this release at publication time. For current deployment requirements, read the [supported versions](/percona/index/supported-versions/) and [limitations](/percona/index/tde-limitations/).

The `pg_tde` extension, provided by Percona, adds [Transparent Data Encryption (TDE)](/percona/index/about-tde/) to PostgreSQL and helps protect sensitive data at rest.

[Get Started](/percona/install/)

## Release Highlights {#release-highlights}

### Integrated Hashicorp Vault namespace {#integrated-hashicorp-vault-namespace}

The namespace of Hashicorp vault is integrated with ``pg_tde`` through the  ``pg_tde_add_global_key_provider_vault_v2`` parameter.

### Documentation updates {#documentation-updates}

Updated the [Global Principal Key configuration ](/percona/global-key-provider-configuration/set-principal-key/) and [Configure WAL encryption ](/percona/wal-encryption/) chapters with updated installation steps and removed outdated KMS configuration information.

## Known issues {#known-issues}

* Creating, changing, or rotating global key providers (or their keys) while `pg_tde_basebackup` is running may cause standbys or standalone clusters initialized from the backup to fail during WAL replay and may also lead to the corruption of encrypted data (tables, indexes, and other relations).

    Avoid making these actions during backup windows. Run a new full backup after completing a rotation or provider update.

* Using `pg_tde_basebackup` with `--wal-method=fetch` produces warnings.

    This behavior is expected and will be addressed in a future release.

* The default `mlock` limit on Rocky Linux 8 for ARM64-based architectures equals the memory page size and is 64 Kb. This results in the child process with `pg_tde` failing to allocate another memory page because the max memory limit is reached by the parent process.

    To prevent this, you can change the `mlock` limit to be at least twice bigger than the memory page size:

    * temporarily for the current session using the `ulimit -l <value>` command.
    * set a new hard limit in the `/etc/security/limits.conf` file. To do so, you require the superuser privileges.

    Adjust the limits with caution since it affects other processes running in your system.

## Changelog {#changelog}

### New Features {#new-features}

* [PG-1959 ](https://perconadev.atlassian.net/browse/PG-1959) - Namespace of Hashicorp vault is integrated with `pg_tde`
