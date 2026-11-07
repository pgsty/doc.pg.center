---
author: PGSTY
title: How pg_tde keeps data encrypted through PostgreSQL storage
description: A practical tour of tde_heap, the Storage Manager path, internal keys, principal keys, and WAL encryption.
date: 2026-11-07
tags:
- architecture
- encryption
- wal
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/architecture/encryption-architecture.md
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


Encryption only helps when it follows the real storage path. pg_tde marks the tables that need encryption with `tde_heap`, then uses PostgreSQL's Storage Manager to encrypt pages before they reach disk and decrypt them before they enter the buffer cache.

## The two-key hierarchy {#the-two-key-hierarchy}

Each encrypted data file has an internal key. The principal key protects the internal keys and lives in a key provider. This separation lets pg_tde rotate protection without rewriting every data page immediately.

## Where WAL fits {#where-wal-fits}

WAL encryption is cluster-wide. The WAL pages use internal keys, and those keys are protected by the server principal key. A WAL reader uses key metadata to decide which records need decryption.

## Operator consequence {#operator-consequence}

A table can be readable while its key provider is available and unreadable when the provider or credentials are missing. The [key management guide](/percona/global-key-provider-configuration/overview/) and [recovery limits](/percona/index/tde-limitations/) belong in the same runbook as the database configuration.
