---
type: docs
upstream_source: openhalo
upstream_link: ""
title: OpenHalo documentation
linkTitle: OpenHalo
description: Maintained OpenHalo 18 manual, versioned changes, compatibility boundaries and acceptance, with historical PG14 and Halo Database references.
weight: -70
sidebar_root_for: self
sidebar_root_link_self: true
outputs:
- HTML
- RSS
- print
- markdown
- LLMSFULL
cascade:
  type: docs
  upstream_source: openhalo
no_list: true
icon: fa-solid fa-circle-nodes
---

OpenHalo adds MySQL wire-protocol and SQL compatibility to PostgreSQL. This collection separates **four distinct lineages and versions** that share related naming:

1. **PGSTY OpenHalo 18 (`pgsty/openhalo`)** — a PostgreSQL 18.6 kernel with protocol, execution, sequence, foreign-key, and collation hooks, paired with the `aux_mysql` extension (source tag `v18.6.1` at `2627e6f` on `main` ships `aux_mysql 1.9`, incorporating the 2026-11-10 accepted commit `6a93e8f`; earlier tag `v18.6` ships `1.5`, and multi-platform binary packages for `18.6.1` remain pending package acceptance).
2. **Upstream openHalo 1.0 (`HaloTech-Co-Ltd/openHalo`, PG14)** — the open-source PostgreSQL 14.18 fork where MySQL protocol and analyzer changes were compiled directly into ~320 kernel files.
3. **Commercial Halo Database (`1.0.16`)** — Halo Tech's proprietary multi-mode product, which uses its own listener, tenant, authentication, and procedural settings (`cluster_net_services`, `mysql.default_tenant`, `plmyssql`).
4. **Stock PostgreSQL 18** — unmodified upstream PostgreSQL, which shares catalog storage layout with OpenHalo 18 but does not have OpenHalo's protocol, parse, or plan node ABI hooks.

Verify which binary and extension version you are running before copying any configuration or assuming compatibility.

## Choose the right manual {#benefits}

| Edition | Product and baseline | Status and intended use |
| --- | --- | --- |
| [OpenHalo 18 / aux_mysql 1.9](/openhalo/18/) | `pgsty/openhalo` on PostgreSQL 18.6 (source tag `v18.6.1` / `2627e6f`; accepted source `6a93e8f`; legacy tag `v18.6` / `1.5`) | **Maintained manual.** Current functionality, change log, boundaries, configuration, migration, and 2026-11-10 final source acceptance (`6a93e8f`). Multi-platform binary packages still require package-level acceptance. |
| [PG14 build guide (historical)](/openhalo/quick-start/) | `HaloTech-Co-Ltd/openHalo` at `90fc8d7` (PostgreSQL 14.18) | **Historical reference.** Preserves upstream PG14 build commands and `database_compat_mode` settings; incompatible with OpenHalo 18. |
| [Halo Database 1.0.16 reference (historical)](/openhalo/mysql-compatibility/) | Commercial Halo Database 1.0.16 manual snapshot (2026-11-07) | **External product summary.** Documents another product's `cluster_net_services`, `ENUM`/`SET`, and parameters; not the OpenHalo 18 support matrix. |
| [PG14 compatibility test report (historical)](/openhalo/mysql-compatibility-gaps/) | OpenHalo `1.0.14.18 (251127)` independent student report (`80a8d07`) | **Historical test evidence.** 57-case test snapshot on PG14; retained for background only. |
| [Initial OpenHalo 18 review (historical)](/openhalo/mysql57-compatibility-review/) | `pgsty/openhalo` at `9dc937f` (`aux_mysql 1.5`, 2026-11-07) | **Historical NO-GO baseline.** Records the seven initial blockers and differential findings prior to the `1.9` fixes; read alongside [changes](/openhalo/18/changes/) and [final acceptance](/openhalo/18/acceptance/). |
{.wide .expand}

## OpenHalo 18 manual {#migration}

- [Overview, lineage, and version identities](/openhalo/18/) — how OpenHalo 18 relates to PG14, Halo Database, and stock PostgreSQL, plus the five-level compatibility contract.
- [Functionality](/openhalo/18/features/) — supported protocol, SQL, DML, transactions, types, collations, indexes, generated columns, and metadata with examples.
- [Changes since v18.6](/openhalo/18/changes/) — from the initial seven blockers through WP1–WP10, final correctness fixes, and sorting speed recovery.
- [Compatibility boundaries](/openhalo/18/compatibility/) — exact rules, deliberate mappings, echoed-only settings, unsupported features, and native PG impact.
- [Build and configuration](/openhalo/18/configuration/) — lockstep kernel/extension build, `initdb`, `caching_sha2_password`, `mysql.*` GUC contexts, and removed settings.
- [Migration and upgrade](/openhalo/18/migration/) — MySQL 5.7 import, PG14 logical migration, real `1.5 → 1.9` upgrade, non-self-healing historical data, and backup/restore.
- [Final acceptance and release conditions](/openhalo/18/acceptance/) — frozen `6a93e8f` source verdict, SHA-256 fingerprints, benchmarks, unverified scope, and remaining package gates.
{.cards}

## Architecture {#how-it-works}

OpenHalo 18 runs a single PostgreSQL 18.6 postmaster that listens for PostgreSQL clients on port `5432` and MySQL clients on port `3306`. Each MySQL connection runs in a regular PostgreSQL backend subject to `max_connections`, `pg_hba.conf`, `pg_stat_activity`, and PostgreSQL password verifiers. MySQL databases map to schemas inside the configured PostgreSQL database (`mysql.database`, default `postgres`), so both protocols can query the same tables.

Protocol framing, `caching_sha2_password` authentication, `COM_STMT_*` binary statements, the MySQL parser, parse-tree rewriting, transaction wrapping, and MySQL functions live in `contrib/aux_mysql`, backed by kernel hooks for conflict arbitration, foreign keys, atomic sequence advancement, and collations. Build and validate the kernel and `aux_mysql` together from the same commit.

The upstream diagram below illustrates the general dual-protocol model from the PG14 project; it is not an ABI or deployment specification for OpenHalo 18.

![Historical OpenHalo protocol architecture](/openhalo/assets/how-it-works.png)

## Performance evidence {#performance}

Wire-protocol compatibility does not guarantee faster execution than MySQL across workloads. In the 2026-11-10 acceptance benchmark on 300,000 rows (`aarch64`, Rocky Linux 9.8), candidate `6a93e8f` eliminated an earlier multi-fold sorting regression (`63.82 ms` median `ORDER BY` vs `102.24 ms` on released `v18.6`) and cut `FIND_IN_SET` scan time from `3.049 s` to `0.677 s`—while remaining roughly nine times slower than MySQL 5.7.32 (`0.073 s`) on `FIND_IN_SET` because that function is still implemented in SQL. Read the [measured numbers, method, and hardware limits](/openhalo/18/acceptance/#performance) before extrapolating to production queries.

## Migration decisions {#pace}

Applications can keep standard MySQL drivers and CLI tools while migrating incrementally, provided their schemas, SQL patterns, and transaction assumptions fit the documented contract. Review [compatibility boundaries](/openhalo/18/compatibility/) and [migration audits](/openhalo/18/migration/) before cutover—especially `BIGINT UNSIGNED` (`0..INT64_MAX`), `CHAR`/`VARCHAR`/`TEXT` `NUL` rejection (`1366`), the four exact collation names vs `1105` approximations, read-write `REPEATABLE READ` mapping to PostgreSQL `READ COMMITTED`, `UPDATE` matched-row counts, and historical `1.5` objects that require explicit repair. Moving from OpenHalo PG14 to OpenHalo 18 always requires logical migration.

## Historical references {#mysql-compatibility}

> [!WARNING]
> **Do not copy historical settings into OpenHalo 18.** Parameters on the pages below—such as `database_compat_mode`, `--with-uuid=ossp`, `cluster_net_services`, `mysql.default_tenant`, `plmyssql`, and `password_encryption = 'mysql_native_password'`—belong to PG14 openHalo or commercial Halo Database 1.0.16 and are unsupported or rejected on OpenHalo 18.

These pages retain their original product context, evidence, and stable URLs:

- [PG14 build and configuration](/openhalo/quick-start/)
- [Halo Database 1.0.16 MySQL compatibility](/openhalo/mysql-compatibility/)
- [Halo Database 1.0.16 configuration and connection](/openhalo/mysql-configuration/)
- [Halo Database 1.0.16 MySQL statements](/openhalo/mysql-statements/)
- [Halo Database 1.0.16 data types](/openhalo/mysql-data-types/)
- [Historical PG14 OpenHalo compatibility report](/openhalo/mysql-compatibility-gaps/)
- [Initial OpenHalo 18 review, 2026-11-07 (`9dc937f`)](/openhalo/mysql57-compatibility-review/)
{.cards}
