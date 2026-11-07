---
title: Architecture overview
linkTitle: Architecture overview
description: Follow encrypted tables, index files, and WAL through the pg_tde storage architecture.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/architecture/overview.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 410
upstream_source: percona
---

`pg_tde` is a **customizable, complete, data at rest encryption extension**. Extension means that `pg_tde` is delivered as a PostgreSQL extension.

> [!NOTE]
> `pg_tde` relies on extensibility changes in the PostgreSQL core. It currently runs only with [Percona Server for PostgreSQL ](https://docs.percona.com/postgresql/17/index.html), which includes those changes.

The following sections break down the key architectural components of this design.

**a. Customizable** means that `pg_tde` supports many different use cases:

* Encrypting all tables in all databases, or only selected ones
* Storing encryption keys in different external key storage servers, for a list of these see [Key management overview](/percona/global-key-provider-configuration/overview/)
* Using a single key for a clusters, or different keys for different clusters
* Centralizing all keys in one provider, or splitting them across providers
* Controlling permissions: who manages keys and who can create encrypted or unencrypted tables

**b. Complete** means that `pg_tde` aims to encrypt data at rest.

**c. Data at rest** means everything written to the disk. This includes the following:

* Table data files
* Indexes
* Sequences
* Temporary tables
* Write Ahead Log (WAL)

## Main components {#main-components}

The main components of `pg_tde` are:

* **Core server changes** focus on making the server more extensible, allowing the main logic of `pg_tde` to remain separate, as an extension. Core changes also add encryption-awareness to some command line tools that have to work directly with encrypted tables or encrypted WAL files. 

    You can find the source code [here ](https://github.com/percona/postgres/tree/release-2.2.2).

* The **`pg_tde` extension** implements the encryption code by hooking into the extension points introduced in the core changes, and the already existing extension points in the PostgreSQL server.

    Everything is controllable with GUC variables and SQL statements, similar to other extensions.

* The **keyring API and libraries** implement the key storage logic with different key providers. The API is internal only, the keyring the libraries are currently part of the main codebase but could be separated into shared libraries in the future.
