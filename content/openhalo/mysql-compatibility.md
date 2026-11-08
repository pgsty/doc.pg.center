---
type: docs
upstream_source: halodb
upstream_link: "" # Original summary; cite the reference below without claiming an upstream licence.
upstream_ref: "Halo Database 1.0.16; documentation snapshot 2026-11-07"
upstream_notice: /attribution/#halodb
title: MySQL compatibility
linkTitle: MySQL compatibility
description: MySQL protocol, SQL syntax, data types, functions, and compatibility scope in Halo.
weight: 20
---

Halo Database 1.0.16 documents common MySQL 5.6 through 8.0 features: the MySQL protocol, data types, SQL syntax, operators, and system functions. This collection turns that reference into a shorter guide for running and assessing MySQL applications through Halo.

The open-source [openHalo project](https://github.com/HaloTech-Co-Ltd/openHalo) is related source code, but its pinned README uses an older configuration interface. The current Halo Database pages and the openHalo source tree are versioned separately below.

## Reference pages {#reference-pages}

- [Configure and connect to the MySQL endpoint](/openhalo/mysql-configuration/): Halo 16 setup, the legacy openHalo parameters, users, and the `mysql` client.
- [Compatible MySQL statements](/openhalo/mysql-statements/): `REPLACE`, `INSERT IGNORE`, `ON DUPLICATE KEY UPDATE`, `LIMIT`, prepared statements, and user variables.
- [Compatible MySQL data types](/openhalo/mysql-data-types/): numeric, character, date/time, `ENUM`, `SET`, and `YEAR`.
- [Known compatibility boundaries](/openhalo/mysql-compatibility-gaps/): versioned results from an independent OpenHalo test report and a migration test plan.
- [OpenHalo 18 and MySQL 5.7 review](/openhalo/mysql57-compatibility-review/): independent builds, real MySQL 5.7.32 comparisons, migration results, and blocking issues at fixed commit `9dc937f`.

{.cards}

## What the compatibility layer covers {#coverage}

The official reference groups the MySQL surface into these areas:

- data types, including integer and floating-point families, character types, `ENUM`, `SET`, `DATE`, `DATETIME`, `TIMESTAMP`, and `YEAR`;
- MySQL-specific statement forms such as `REPLACE INTO`, `INSERT IGNORE`, `ON DUPLICATE KEY UPDATE`, `INSERT ... SET`, `LIMIT`, SQL-level prepared statements, and `@` user variables;
- date, string, numeric, encryption, control-flow, and aggregate functions;
- comparison, logical, and bitwise operators;
- `CREATE SCHEMA` and `DROP SCHEMA` in MySQL mode, plus standard MySQL clients and drivers.

The full official pages are [SQL syntax](https://doc.halodbtech.com/multi-mode-compatibility/mysql/sql-syntax), [data types](https://doc.halodbtech.com/multi-mode-compatibility/mysql/data-types), [functions](https://doc.halodbtech.com/multi-mode-compatibility/mysql/functions), [operators](https://doc.halodbtech.com/multi-mode-compatibility/mysql/operators), and [other compatibility features](https://doc.halodbtech.com/multi-mode-compatibility/mysql/misc-features).

## How a MySQL application connects {#connection-model}

The MySQL endpoint speaks the standard MySQL protocol. In the documented Halo 16 setup, `cluster_net_services` assigns a MySQL listener port, `mysql.default_tenant` selects the default database, and `aux_mysql` is installed in the database that will run MySQL compatibility syntax. See [Configure and connect](/openhalo/mysql-configuration/) for the exact sequence.

`CREATE SCHEMA` and `DROP SCHEMA` are documented as MySQL database operations in MySQL mode. The underlying server remains PostgreSQL-based, so database names, schemas, roles, permissions, transaction behavior, and type edge cases should be checked against the exact Halo build.

## Version boundary {#version-boundary}

The OpenHalo source material in this collection is pinned to commit [`90fc8d7`](https://github.com/HaloTech-Co-Ltd/openHalo/tree/90fc8d777c3f111d4c8d236625bb15b5d4b19d7c). The official compatibility reference is for Halo Database 1.0.16. Do not treat a Halo Database configuration example as proof that the same parameter exists in the open-source build, or treat an old OpenHalo test result as a current Halo Database support matrix.

Compatibility targets common application behavior. It does not promise that every MySQL administrative command, storage-engine feature, optimizer hint, export facility, stored program, or client-specific extension is available. Run the application's schema, migrations, queries, transactions, drivers, and operational jobs against the exact server version before switching production traffic.

For the independent test evidence and its limitations, see [Known compatibility boundaries](/openhalo/mysql-compatibility-gaps/).

## Sources {#sources}

This page is an original summary of the [Halo Database MySQL compatibility reference](https://doc.halodbtech.com/multi-mode-compatibility/mysql). No public documentation licence was identified; see the [source notice](/attribution/#halodb) for version, copyright, and citation details.
