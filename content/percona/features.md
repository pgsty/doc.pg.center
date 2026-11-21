---
title: Features
linkTitle: Features
description: An inventory of encryption capabilities, supported access methods, and PostgreSQL integration.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a/documentation/docs/features.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a
upstream_modified: true
weight: 120
upstream_source: percona-20261121
---

`pg_tde` is available for [Percona Server for PostgreSQL](https://docs.percona.com/postgresql/17/)
The Percona Server for PostgreSQL provides an extended Storage Manager API that allows integration with custom storage managers.

The following features are available for the extension:

* [Table encryption](/percona/test/#encrypt-data-in-a-new-table), including:
    * Data tables
    * Index data for encrypted tables
    * TOAST tables
    * Temporary tables

> [!NOTE]
> Metadata of those tables is not encrypted.

* Single-tenancy support via a [global keyring provider](/percona/global-key-provider-configuration/set-principal-key/)
* [Multi-tenancy support](/percona/how-to/multi-tenant-setup/)
* Table-level granularity for encryption and access control
* Multiple [Key management options](/percona/global-key-provider-configuration/overview/)

## Next steps {#next-steps}

Learn more about how `pg_tde` implements Transparent Data Encryption:

[About Transparent Data Encryption ](/percona/index/about-tde/)
