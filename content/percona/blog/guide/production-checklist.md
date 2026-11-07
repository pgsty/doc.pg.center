---
author: PGSTY
title: A production checklist for pg_tde
description: The small set of installation, key custody, WAL, backup, and recovery checks to complete before enabling
  TDE in production.
date: 2026-11-07
tags:
- operations
- security
- backup
translation_notice: false
upstream_link: https://github.com/percona/pg_tde
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
upstream_source: percona
type: docs
---


An editorial reading note by PGSTY, based on the upstream documentation.


Before enabling encryption, make the key provider and recovery path as concrete as the database configuration.

## Checklist {#checklist}

- Confirm the Percona PostgreSQL and pg_tde versions are compatible.
- Load `pg_tde` through `shared_preload_libraries` and create the extension in every database that needs it.
- Use an external KMS or KMIP-compatible provider for production; keep keyring files for development and testing.
- Create and verify a principal key before creating encrypted tables.
- Test `tde_heap` on a new table and on a disposable copy of an existing table.
- If WAL encryption is enabled, use the pg_tde-aware archive and restore tools.
- Back up the provider configuration and document how the server obtains historical keys.
- Test restore, replica creation, major upgrade, and provider outage procedures.
- Record which objects are outside the encryption scope, including temporary files and statistics.

## Related documentation {#related-documentation}

- [Install pg_tde](/percona/install/)
- [Configure key management](/percona/global-key-provider-configuration/overview/)
- [Validate encryption](/percona/test/)
- [Configure WAL encryption](/percona/wal-encryption/)
- [Understand limitations](/percona/index/tde-limitations/)
