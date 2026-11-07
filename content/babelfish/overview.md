---
title: Get started
linkTitle: Overview
description: Babelfish components, use cases, and ways to contribute.
weight: 10
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_docs/index.md
upstream_ref: main @ f468c5ed3d38
upstream_notice: /babelfish/site/attribution/
---


> [!NOTE] Website documentation snapshot
> Upstream moved new documentation to [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki) in 2023. Check the [release notes](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/releases) for the version you use; this page preserves the website documentation.

## Babelfish for PostgreSQL documentation {#babelfish-for-postgresql-documentation}

This site contains the technical documentation for [Babelfish for PostgreSQL](/babelfish/), an [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) and [PostgreSQL](https://www.postgresql.org/about/licence/) open-source project that adds a Microsoft SQL Server-compatible end-point to PostgreSQL. With the addition of Babelfish, PostgreSQL understands T-SQL, SQL Server's proprietary SQL dialect, and supports the TDS communication protocol, so applications originally written for SQL Server may work with PostgreSQL with fewer code changes and without changing database drivers.


[Get started](/babelfish/installation/compiling-babelfish-from-source/)


---

## Why use Babelfish for PostgreSQL? {#why-use-babelfish-for-postgresql}

Babelfish for PostgreSQL may help in the following use cases:

* When transitioning your SQL Server compatible source code to an open-source based database.
* When moving away from proprietary or legacy applications that don't make source code available.

Babelfish for PostgreSQL functionality is distributed in five components:

Component | Purpose
:--- | :---
[Babelfish Server Patch](https://github.com/babelfish-for-postgresql/postgresql_modified_for_babelfish) | Enables Babelfish hooks for PostgreSQL.
[Babelfish TDS Extension](https://github.com/babelfish-for-postgresql/babelfish_extensions/tree/BABEL_1_0_0/contrib/babelfishpg_tds) | TDS - provides a secondary endpoint that speaks the TDS (SQL Server) network protocol.
[Babelfish Language Extension](https://github.com/babelfish-for-postgresql/babelfish_extensions/tree/BABEL_1_0_0/contrib/babelfishpg_tsql) | Provides a procedural language compatible with T-SQL (Uses ANTLR parser).
[Babelfish Money Type](https://github.com/babelfish-for-postgresql/babelfish_extensions/tree/BABEL_1_0_0/contrib/babelfishpg_money) | Supports the money type in SQL Server. This is a variation of the open-source fixed-decimal extension.
[Babelfish Common](https://github.com/babelfish-for-postgresql/babelfish_extensions/tree/BABEL_1_0_0/contrib/babelfishpg_common) | Supports the various datatypes in SQL Server.


For information about the project components, see the [Software architecture page](/babelfish/internals/software-architecture/).


## Get involved {#get-involved}

The project welcomes your contributions and feedback on issues, bug fixes, features, plugins, and documentation. To get involved, visit [the Babelfish for PostgreSQL website](/babelfish/contributing/).

All components are available under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.html) and the [PostgreSQL License](https://www.postgresql.org/about/licence/) on [GitHub](https://github.com/babelfish-for-postgresql). Our thanks go out to the PostgreSQL team and the [Babelfish project contributors](/babelfish/site/contributors/).



<!---
This should be 
commented out
-->
