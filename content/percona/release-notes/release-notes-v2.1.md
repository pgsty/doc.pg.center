---
title: pg_tde 2.1.0 (2025-11-28)
linkTitle: 2.1.0
description: Changes, compatibility notes, and fixes for pg_tde 2.1.0 (2025-11-28).
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/release-notes/release-notes-v2.1.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 860
upstream_source: percona
---

> [!NOTE] Historical release
> This page describes this release at publication time. For current deployment requirements, read the [supported versions](/percona/index/supported-versions/) and [limitations](/percona/index/tde-limitations/).

The `pg_tde` by Percona extension brings [Transparent Data Encryption (TDE)](/percona/index/about-tde/) to PostgreSQL and enables you to keep sensitive data safe and secure.

[Get Started](/percona/install/)

## Release Highlights {#release-highlights}

### Added support for PostgreSQL 18.1 {#added-support-for-postgresql-18-1}

`pg_tde` is fully supported with the Postgres 18.1 version.

### Packaging changes for PostgreSQL 18 {#packaging-changes-for-postgresql-18}

Starting with PostgreSQL 18, `pg_tde` is distributed as a **standalone package** for RPM and DEB installations.

It is no longer bundled with the main PostgreSQL server package.

If your PostgreSQL 18 deployment uses `pg_tde`, make sure to install the matching `pg_tde` package separately.

Percona’s PostgreSQL **Docker images continue to include `pg_tde` by default**, so no additional action is required for container-based deployments.

For more information on the availability by PostgreSQL version, please see [Install pg_tde](/percona/install/).

### Added support for AIO {#added-support-for-aio}

Added support for **asynchronous I/O (AIO)** which is now the default I/O mechanism.

### Added namespace support for Vault Enterprise and OpenBao {#added-namespace-support-for-vault-enterprise-and-openbao}

Added support for HashiCorp Vault and OpenBao namespaces. The `namespace` parameter is now documented in [Add or modify Vault providers](/percona/functions/#add-or-modify-vault-providers) and fully supported.

### Repository split for multi-version PostgreSQL support {#repository-split-for-multi-version-postgresql-support}

Reorganized the project into a multi-repository structure to support several PostgreSQL versions more efficiently.

### Tooling changes {#tooling-changes}

The standard PostgreSQL command-line utilities can no longer operate on clusters encrypted with `pg_tde`. To manage encrypted data safely, use the `pg_tde_` equivalents provided by Percona:

* pg_basebackup to pg_tde_basebackup
* pg_checksums to pg_tde_checksums
* pg_resetwal to pg_tde_resetwal
* pg_rewind to pg_tde_rewind
* pg_waldump to pg_tde_waldump

> [!WARNING]
>
> The non-pg_tde_* versions will not work on encrypted clusters and may fail with errors if used. Always use the `pg_tde_` variants when working with TDE-enabled data.

### Added Akeyless support {#added-akeyless-support}

`pg_tde` is now compatible with the Akeyless CipherTrust Manager via the KMIP protocol. For more information, see the [Key management overview topic](/percona/global-key-provider-configuration/overview/).

### Added support for Vault and OpenBao namespaces {#added-support-for-vault-and-openbao-namespaces}

Implemented support for the "namespace" feature in Vault Enterprise and OpenBao, available both on the CLI and on the HTTP interface using the `X-Vault-Namespace` header.

### Documentation updates {#documentation-updates}

- Added the [Akeyless topic](/percona/global-key-provider-configuration/kmip-akeyless/)
- Added the [Impact of pg_tde on database operations](/percona/index/what-tde-impacts/) topic which summarizes how `pg_tde` interacts with core PostgreSQL operations
- Updated the [FAQ](/percona/faq/) with an answer to logical replication keeping data encrypted on subscribers
- Updated [Install pg_tde](/percona/install/) with a table for the `pg_tde` availability by PostgreSQL version
- Updated [Add or modify Vault providers](/percona/functions/#add-or-modify-vault-providers) to include the `namespace` parameter.

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
