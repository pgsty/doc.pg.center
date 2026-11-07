---
title: Purpose of Babelfish
linkTitle: What is Babelfish?
description: How SQL Server clients connect to PostgreSQL through Babelfish.
weight: 20
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_docs/purpose.md
upstream_ref: main @ f468c5ed3d38
upstream_notice: /babelfish/site/attribution/
---


> [!NOTE] Website documentation snapshot
> Upstream moved new documentation to [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki) in 2023. Check the [release notes](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/releases) for the version you use; this page preserves the website documentation.

Babelfish for PostgreSQL extends your PostgreSQL database with the ability to
accept database connections from Microsoft SQL Server clients.  Doing this
allows applications originally built for SQL Server to work directly with
PostgreSQL with few code changes compared to a traditional migration and without
changing database drivers.  For more information about migrating, see
[migrating to Babelfish](/babelfish/usage/migration/).

Babelfish provides an additional endpoint for a PostgreSQL database cluster
that allows it to understand the SQL Server wire-level protocol and commonly
used SQL Server statements.  This approach allows client applications that use
the Tabular Data Stream (TDS) wire protocol to connect natively to the TDS
listener port on PostgreSQL. Babelfish supports TDS versions 7.1 and higher.
For more information on the SQL Server wire-level protocol, see
[\[MS-TDS\]: /babelfish/purpose/Tabular Data Stream Protocol](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-tds/b46a581a-39de-4745-b076-ec4dbb7d13ec)
on the Microsoft website.

You can access your data simultaneously using a Babelfish TDS connection from
one application and a native PostgreSQL connection from another application.
You can customize the ports used for client connections when you initialize
Babelfish, or later by setting PostgreSQL parameters.  For more information
about the parameters that control Babelfish, see
[configuring Babelfish](/babelfish/internals/configuration/).

By default, to use the following dialects use the following ports:

- SQL Server dialect, clients connect to port 1433.

- PostgreSQL dialect, clients connect to port 5432.

Babelfish runs the Transact-SQL (T-SQL) language.


### Join the Babelfish community {#join-the-babelfish-community}

Be part of the community and help to make improvements.
You're welcome to [contribute to Babelfish](/babelfish/contributing/).
