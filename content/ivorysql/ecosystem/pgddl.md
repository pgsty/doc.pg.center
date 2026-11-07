---
title: pgddl (DDL Extractor)
linkTitle: pgddl(DDL Extractor)
description: 'IvorySQL v5.6 documentation: pgddl (DDL Extractor).'
type: docs
weight: 380
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/5.3.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

## 1. Overview {#overview}

pgddl is a SQL function extension specifically designed for PostgreSQL databases. It can generate clear, formatted SQL DDL (Data Definition Language) scripts directly from the database system catalog, such as CREATE TABLE or ALTER FUNCTION. It solves the problem that PostgreSQL natively lacks commands like SHOW CREATE TABLE, allowing users to easily obtain object creation statements in a pure SQL environment without relying on external tools (such as pg_dump).

This extension provides a complete solution through a set of simple SQL functions, with advantages including: requiring only SQL queries to operate, supporting flexible object filtering through WHERE clauses, and intelligently handling dependencies between objects to generate complete scripts including Drop and Create steps. This makes it particularly suitable for scenarios such as database change management, upgrade script writing, and structural auditing.

It should be noted that ddlx is still under development and may not yet cover all PostgreSQL object types and advanced options. Generated scripts should always be checked and tested in non-production environments first to ensure their correctness and safety.

## 2. Installation {#installation}

The IvorySQL installation package already integrates the pgddl plugin. If IvorySQL is installed using the installation package, pgddl can usually be used without manual installation. Other installation methods can refer to the source code installation steps below.

> [!TIP]
>
> The source installation environment is Ubuntu 24.04 (x86_64). IvorySQL 5 or higher version is already installed in the environment, with the installation path at /usr/local/ivorysql/ivorysql-5

### 2.1. Source Installation {#source-installation}

Download pgddl v0.31 code from <a href="https://github.com/lacanoid/pgddl" class="bare">https://github.com/lacanoid/pgddl</a>.

```
cd pgddl
# Set the PG_CONFIG environment variable to the pg_config path, e.g.: /usr/local/ivorysql/ivorysql-5/bin/pg_config
make PG_CONFIG=/path/to/pg_config
make PG_CONFIG=/path/to/pg_config install
```

## 3. Create Extension and Confirm ddlx Version {#create-extension-and-confirm-ddlx-version}

Connect to the database with psql and execute the following commands:

```
ivorysql=# CREATE extension ddlx;
CREATE EXTENSION

ivorysql=# SELECT * FROM pg_available_extensions WHERE name = 'ddlx';
 name | default_version | installed_version |         comment
------+-----------------+-------------------+-------------------------
 ddlx | 0.31            | 0.31              | DDL eXtractor functions
(1 row)
```

## 4. Usage {#usage}

For pgddl usage, please refer to the [ddlx Official Documentation](https://github.com/lacanoid/pgddl)
