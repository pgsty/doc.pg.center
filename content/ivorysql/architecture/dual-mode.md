---
title: Dual-mode design
linkTitle: Dual-mode design
description: 'IvorySQL v5.6 documentation: Dual-mode design.'
type: docs
weight: 760
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/7.4.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

## 1. Objective {#objective}

- In order to support both the PG mode and Oracle-compatible mode, IvorySQL allows specifying the -m parameter during initdb to obtain either a PG mode database or an Oracle-compatible mode database.



- If the -m parameter is not specified, it defaults to Oracle-compatible mode.

- If the -m parameter is specified as pg, the database will no longer be compatible with Oracle syntax.

## 2. Function {#function}

- initdb -m initialization requires judgment of different modes, among which oracle mode requires the execution of SQL statements postgres_oracle.bki. The default is Oracle compatibility mode, and the process is as follows:

- Startup: When starting, it determines whether it is an Oracle compatibility mode based on the initialization mode;

```
Description:
database_mode: Used to indicate initialization mode;
database_mode=DB_PG，PG mode, and cannot be switched;
database_mode=DB_ORACLE， oracle compatibility mode;
```

## 3. Test cases {#test-cases}

```
Initialize the PG mode:
./initdb -D ../data -m pg

Initialize the Oracle compatibility mode:
./initdb -D ../data -m oracle

or
./initdb -D ../data
```
