---
title: Key management overview
linkTitle: Choose a provider
description: Choose a supported KMS and understand principal keys, provider scope, and deployment requirements.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/global-key-provider-configuration/overview.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 310
upstream_source: percona
---

> [!NOTE] Editorial correction
> This overview retains an older qualification of Vault KMIP. The 2.2.2 release notes explicitly announce Vault Enterprise KMIP support; consult those notes for the version-specific status. See [site errata](/percona/site/errata/).

In production environments, storing encryption keys locally on the PostgreSQL server can introduce security risks. To enhance security, `pg_tde` supports integration with external Key Management Systems (KMS) through a Global Key Provider interface.

This section describes how you can configure `pg_tde` to use the local and external key providers.

To use an external KMS with `pg_tde`:

1. Configure a Key Provider
2. Set the [Global Principal Key](/percona/global-key-provider-configuration/set-principal-key/)

> [!NOTE]
> While key files may be acceptable for **local** or **testing environments**, KMS integration is the recommended approach for production deployments.

> [!IMPORTANT]
> When using HashiCorp Vault, **KV v2 is the recommended and supported integration method**.
>
> The KMIP engine in Vault is not a validated configuration for `pg_tde` and is not recommended for production deployments.

> [!WARNING]
> Do not rotate encryption keys while a backup is running. This may result in an inconsistent backup and restore failure. This applies to all backup tools.
>
> Schedule key rotations outside backup windows. After rotating keys, take a new full backup.
>
> For more details, see [Limitations of pg_tde](/percona/index/tde-limitations/#limitations-when-using-pgtde).

`pg_tde` has been tested with the following key providers:

| KMS Provider       | Description                                           | Documentation |
|--------------------|-------------------------------------------------------|---------------|
| **KMIP**           | Standard Key Management Interoperability Protocol.    | [Configure KMIP →](/percona/global-key-provider-configuration/kmip-server/) |
| **Vault**          | HashiCorp Vault integration (KV v2 API). | [Configure Vault →](/percona/global-key-provider-configuration/vault/) |
| **Fortanix**       | Fortanix DSM key management.                          | [Configure Fortanix →](/percona/global-key-provider-configuration/kmip-fortanix/) |
| **Thales**         | Thales CipherTrust Manager and DSM.                   | [Configure Thales →](/percona/global-key-provider-configuration/kmip-thales/) |
| **OpenBao**        | Community fork of Vault, supporting KV v2.            | [Configure OpenBao →](/percona/global-key-provider-configuration/openbao/) |
| **Akeyless**        | A cloud-based secrets management platform for securely storing and accessing credentials and encryption keys.            | [Configure Akeyless →](/percona/global-key-provider-configuration/kmip-akeyless/) |
| **Keyring file** *(not recommended)* | Local key file for dev/test only.                  | [Configure keyring file →](/percona/global-key-provider-configuration/keyring/) |
