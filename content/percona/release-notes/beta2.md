---
title: pg_tde Beta 2 (2024-12-16)
linkTitle: Beta 2
description: Changes, compatibility notes, and fixes for pg_tde Beta 2 (2024-12-16).
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/release-notes/beta2.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 910
upstream_source: percona
---

> [!NOTE] Historical release
> This page describes this release at publication time. For current deployment requirements, read the [supported versions](/percona/index/supported-versions/) and [limitations](/percona/index/tde-limitations/).

`pg_tde` extension brings in [Transparent Data Encryption (TDE)](/percona/index/about-tde/) to PostgreSQL and enables you to keep sensitive data safe and secure.

[Get started](/percona/install/)

> [!IMPORTANT]
>
> This version of Percona Transparent Data Encryption extension **is 
> not recommended for production environments yet**. We encourage you to test it and [give your feedback](https://forums.percona.com/c/postgresql/pg-tde-transparent-data-encryption-tde/82).
>
> This will help us improve the product and make it production-ready faster.

## Release Highlights {#release-highlights}

With this release, `pg_tde` extension offers two database specific versions:

*  PostgreSQL Community version provides only the `tde_heap_basic` access method using which you can introduce table encryption and WAL encryption for data in the encrypted tables. Index data remains unencrypted.
* Version for Percona Server for PostgreSQL provides the `tde_heap`access method. using this method you can encrypt index data in encrypted tables thus increasing the safety of your sensitive data. For backward compatibility, the `tde_heap_basic` method is available in this version too. 

## Changelog {#changelog}

The Beta 2 version introduces the following features and improvements:

### New Features {#new-features}

* Added the `tde_heap` access method with which you can now enable index encryption for encrypted tables and global WAL data encryption. To use this access method, you must install Percona Server for PostgreSQL. Check the [installation guide](/percona/install/)
* Added event triggers to identify index creation operations on encrypted tables and store those in a custom storage.
* Added support for secure transfer of keys using the [OASIS Key Management Interoperability Protocol (KMIP)](https://docs.oasis-open.org/kmip/kmip-spec/v2.0/os/kmip-spec-v2.0-os.html). The KMIP implementation was tested with the PyKMIP server and the HashiCorp Vault Enterprise KMIP Secrets Engine.

### Improvements {#improvements}

* WAL encryption improvements:

   * Added a global key to encrypt WAL data in global space
   * Added WAL key management

* Keyring improvements:

    * Renamed functions to point their usage for principal key management
    * Improved keyring provider management across databases and the global space.
    * Keyring configuration now uses common JSON API. This simplifies code handling and enables frontend tools like `pg_waldump` to read the code thus improving debugging.

* The `pg_tde_is_encrypted` function now supports custom schemas in the format of `pg_tde_is_encrypted('schema.table');`
* Changed the location of internal TDE files: instead of the database directory, now all files are stored in ` $PGDATA/pg_tde`
* Improved error reporting when `pg_tde` is not added to the `shared_preload_libraries`
* Improved memory usage of `tde_heap_basic `during sequential reads
* Improved `tde_heap_basic` for select statements
* Added encryption support for (some) command line utilities

### Bugs fixed {#bugs-fixed}

* Fixed multiple bugs with `tde_heap_basic` and TOAST records
* Fixed various memory leaks
