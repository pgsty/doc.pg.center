---
title: Software architecture
linkTitle: Software architecture
description: The server patch, extensions, and mapping of SQL Server databases to PostgreSQL schemas.
weight: 40
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_internals/software-architecture.md
upstream_ref: main @ f468c5ed3d38
upstream_notice: /babelfish/site/attribution/
---


> [!NOTE] Website documentation snapshot
> Upstream moved new documentation to [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki) in 2023. Check the [release notes](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/releases) for the version you use; this page preserves the website documentation.

Babelfish uses [hooks](/babelfish/internals/postgresql-hooks/) to implement Microsoft SQL Server behavior
from a PostgreSQL server. This allows the PostgreSQL server to speak more than one language, making
the setup flexible and easy to manage.

A PostgreSQL database that is running Babelfish listens for connections on two (configurable) TCP 
ports, in two dialects:

- SQL Server dialect (TDS).
- PostgreSQL dialect.
 
Once the TDS handler has accepted and processed a request coming in on the TDS port,
the request is passed on to a PostgreSQL backend. The backend parses the request using a 
custom parser, modified to understand SQL Server dialect.

![Babelfish system architecture](/babelfish/assets/images/babelfish-architecture.png)
{width="800" caption="Babelfish system architecture"}

There are no significant changes to the PostgreSQL optimizer or the PostgreSQL executor.

The PostgreSQL core that is distributed with Babelfish has been modified to prepare for trigger processing, 
transaction handling, and other behaviors that are different in SQL Server. This means that the database 
server is not 100% identical to a community distribution of PostgreSQL.  

### Databases vs. schemas {#databases-vs-schemas}

PostgreSQL supports the following logical structure of objects:

- Instance: a running PostgreSQL server (the PostgreSQL community documentation calls this a cluster)
- Database: what a user connects to
- Schema: a logical grouping of tables and other objects inside a database
- Table: where the data is stored

SQL Server supports the same objects.  

In contrast to PostgreSQL, SQL Server allows you to query tables that reside in another database, 
or join tables in different databases. To enable cross-database joins, you should use the `multi-db` 
deployment mode in Babelfish.

In `multi-db` mode, when you call the `USE` command to switch from one database to the other, you remain 
connected to the same PostgreSQL database, but switch to a different schema. Understanding this relationship 
may help you if you plan to query the same table using both protocols.

To learn more about single and multi-database deployments, [see the documentation](/babelfish/installation/single-multiple/),
which deals with this topic in more detail.


### Babelfish extensions {#babelfish-extensions}

Babelfish uses extensions to make PostgreSQL compatible with SQL Server:

- `babelfishpg_common`: SQL Server data types
- `babelfishpg_money`: Fixed precision numeric type
- `babelfishpg_tds`: TDS protocol extension
- `babelfishpg_tsql`: T-SQL extension

Here is a more detailed description of these extensions:

#### `babelfishpg_common`: SQL Server data types {#babelfishpgcommon-sql-server-data-types}

Data types are often really similar but not necessarily 100% identical.
Therefore, the Babelfish development team provides specific data types which
mimic SQL Server behavior.

#### `babelfishpg_money`: Money data type {#babelfishpgmoney-money-data-type}

The `babelfishpg_money` extension implements the money data type.

#### `babelfishpg_tds`: TDS protocol extension {#babelfishpgtds-tds-protocol-extension}

This extension implements the TDS client-server protocol.  You need to modify the `shared_preload_libraries` 
parameter (in the postgresql.conf file) to ensure that the extension is loaded
at server startup time. 

#### `babelfishpg_tsql`: T-SQL extension {#babelfishpgtsql-t-sql-extension}

This extension provides the code needed for to handle T-SQL syntax.  It contains functions,
[system views](/babelfish/internals/system-views/) and other infrastructure required to implement SQL Server functionality.
