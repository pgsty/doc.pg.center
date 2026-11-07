---
title: pg_tde Alpha 1 (2024-03-28)
linkTitle: Alpha 1
description: Changes, compatibility notes, and fixes for pg_tde Alpha 1 (2024-03-28).
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/release-notes/alpha1.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 930
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

The Alpha1 version of the extension introduces the following key features:

* You can now rotate principal keys used for data encryption. This reduces the risk of long-term exposure to potential attacks and helps you comply with security standards such as GDPR, HIPAA, and PCI DSS.

* You can now configure encryption differently for each database. For example, encrypt specific tables in some databases with different encryption keys while keeping others non-encrypted.

* Keyring configuration has undergone several improvements, namely:

    * You can define separate keyring configuration for each database
    * You can change keyring configuration dynamically, without having to restart the server
    * The keyring configuration is now stored in a catalog separately for each database, instead of a configuration file
    * Avoid storing secrets in the unencrypted catalog by configuring keyring parameters to be read from external sources (file, http(s) request)

## Improvements {#improvements}

* Renamed the repository and Docker image from `postgres-tde-ext` to `pg_tde`. The extension name remains unchanged
* Changed the Initialization Vector (IV) calculation of both the data and internal keys

## Bugs fixed {#bugs-fixed}

* Fixed toast related crashes
* Fixed a crash with the DELETE statement
* Fixed performance-related issues
* Fixed a bug where `pg_tde` sent many 404 requests to the Vault server
* Fixed сompatibility issues with old OpenSSL versions
* Fixed сompatibility with old Curl versions
