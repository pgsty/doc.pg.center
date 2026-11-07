---
title: Connecting to Babelfish
linkTitle: Client tools
description: Connect through the TDS or PostgreSQL port with familiar client tools.
weight: 20
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_usage/command-line.md
upstream_ref: main @ f468c5ed3d38
upstream_notice: /babelfish/site/attribution/
---


> [!NOTE] Website documentation snapshot
> Upstream moved new documentation to [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki) in 2023. Check the [release notes](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/releases) for the version you use; this page preserves the website documentation.

## Using client tools to connect to Babelfish {#using-client-tools-to-connect-to-babelfish}

You can use a SQL Server client to connect with Babelfish on the TDS port.
When connecting from a Windows system, SQL Server Management Studio (SSMS) or
`sqlcmd` are good choices of clients.  If you are connecting to the TDS port
from a Linux system, `sqlcmd` is a good choice.

Other clients that speak the TDS protocol can also be used, but are not
officially supported by Babelfish.  On Linux, these include the FreeTDS command
line tool `tsql`.

You can use any PostgreSQL client to connect to Babelfish on the PostgreSQL
port.  `psql` and pgAdmin are examples of open-source clients that run on
Windows and Linux platforms and speak the PostgreSQL protocol.
