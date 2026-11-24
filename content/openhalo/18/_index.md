---
type: docs
upstream_source: openhalo-pgsty
upstream_link: ""
search_keywords: ["OpenHalo 18", "aux_mysql 1.9", "PGSTY", "v18.6.1", "2627e6f", "6a93e8f", "v18.6", "MySQL 5.7"]
title: OpenHalo 18 and aux_mysql 1.9
linkTitle: OpenHalo 18
description: Architecture, lineage, version identities, five-level compatibility contract, and reading guide for PGSTY OpenHalo 18.
weight: 1
cascade:
  type: docs
  upstream_source: openhalo-pgsty
no_list: true
---

OpenHalo 18 combines a **PostgreSQL 18.6 kernel** (patched with protocol, executor, sequence, foreign-key, and collation hooks) with **`aux_mysql`**, an in-tree extension implementing the MySQL wire protocol, parser, rewrite rules, transaction semantics, and function library. MySQL clients connect on TCP port `3306` by default while PostgreSQL clients connect on `5432`. Both protocols read and write the same tables: a MySQL database corresponds to a schema inside the configured PostgreSQL database (`mysql.database`, default `postgres`).

This manual documents the [PGSTY maintained fork](https://github.com/pgsty/openhalo), targeting legacy MySQL 5.7 applications. Do not mix its configuration or support claims with the historical PG14 openHalo or commercial Halo Database 1.0.16 pages in this collection.

> [!IMPORTANT]
> **Source and package status (2026-11-10).** Source tag **`v18.6.1`** (`2627e6f3e94ffdaba9ca6a835c4a1ae2fba34183` on `main`) publishes **`aux_mysql 1.9`**, superseding tag `v18.6` (`60e7a225f2182b0a056501dba1aa79e358f9cbb1`, `aux_mysql 1.5`). The independent final acceptance audit and performance baselines on `2026-11-10` remain pinned to commit **`6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a`** (**conditional GO** within the disclosed boundaries); the four commits between `6a93e8f` and `v18.6.1` (`2627e6f`) add only copyright headers, `.gitignore` rules, and documentation updates with **zero executable C, SQL, or grammar rule changes**. Production multi-platform RPM/DEB binary packages for `v18.6.1` still require target-matrix package builds and package-level install/upgrade/restore acceptance; see [final acceptance and release conditions](/openhalo/18/acceptance/).

## Read this manual {#manual}

- [Functionality](/openhalo/18/features/) — support level, implemented behavior, runnable SQL examples, and migration impact across protocol, DML, transactions, types, indexes, generated columns, and metadata.
- [Changes since v18.6](/openhalo/18/changes/) — engineering progression from the initial seven blockers through WP1–WP10, final correctness fixes, and sorting speed recovery.
- [Compatibility boundaries](/openhalo/18/compatibility/) — exact behavior vs deliberate mappings, echoed-only settings, unsupported SQL, native PostgreSQL session impact, and diagnostic codes.
- [Build and configuration](/openhalo/18/configuration/) — lockstep compilation, instance initialization, `caching_sha2_password` authentication, `mysql.*` GUC contexts, and obsolete settings.
- [Migration and upgrade](/openhalo/18/migration/) — MySQL 5.7 migration, PG14 logical migration, real `1.5 → 1.9` upgrade, historical objects that do not self-repair, and backup/restore.
- [Final acceptance](/openhalo/18/acceptance/) — verified builds, SHA-256 digests, test and performance evidence, unverified scope, and remaining delivery gates.
{.cards}

## Product relationship and architecture {#lineage}

| Dimension | OpenHalo 18 (`pgsty/openhalo`) | Upstream openHalo 1.0 (`pg14`) | Commercial Halo Database (`1.0.16`) | Stock PostgreSQL 18.6 |
| --- | --- | --- | --- | --- |
| Kernel baseline | PostgreSQL 18.6 + targeted protocol, conflict, FK, sequence, and collation hooks | PostgreSQL 14.18 fork (~320 modified core files) | Proprietary multi-mode kernel | Unmodified PostgreSQL 18.6 |
| Where MySQL logic lives | `contrib/aux_mysql` (`shared_preload_libraries`, default `on`) + kernel hooks | Compiled into forked core analyzer/executor + SQL helpers in `aux_mysql` | Proprietary engine modules + `aux_mysql` / `plmyssql` | None |
| Extension & binary ABI | PG18 catalog layout preserved; protocol, parse, and plan structs differ—build kernel and extensions together | Diverges from stock PG14 (`DestReceiver`, `pg_proc`, ACL bits) | Proprietary binary distribution | Standard PG18 ABI |
| Authentication on 3306 | `caching_sha2_password` (TLS / RSA-OAEP + fast-auth cache) or `mysql_clear_password`, verified against PG SCRAM/MD5 | `mysql_native_password` via custom `password_encryption` | `mysql_native_password` via `hsql` / Halo settings | PG protocol only (`5432`) |
| Database / schema model | MySQL databases are schemas in `mysql.database` (`postgres`); first superuser MySQL login auto-installs `aux_mysql` when enabled | `database_compat_mode = 'mysql'` + manual `CREATE EXTENSION aux_mysql` | `cluster_net_services` + `mysql.default_tenant` | Native databases and schemas |
| Physical upgrade from PG14 | **Unsupported** (`pg_upgrade` explicitly rejects `1.0.14.x` binaries); use logical migration | N/A | Vendor-specific | Standard PG `pg_upgrade` from stock PG |
| Software license | Core & protocol hooks: PostgreSQL License; `aux_mysql` & combined build: GNU GPL v3 | GNU GPL v3 | Commercial / proprietary | PostgreSQL License |
{.wide .expand}

The MySQL grammar (`src/parser/mys_gram.y`) and base SQL catalog (`sql/aux_mysql.sql`) are deterministically generated from the repository's `pg14` branch (synced with `HaloTech-Co-Ltd/openHalo` through `90fc8d7`) by `tools/port_grammar.py` and `tools/port_aux_sql.py`, then extended with OpenHalo 18 C hooks and SQL upgrade scripts.

## Version identities {#versions}

| Identity | Exact meaning and current status (2026-11-10) |
| --- | --- |
| PostgreSQL `18.6` (`180006`) | Underlying kernel baseline (`PG_VERSION = 18.6`, `PG_VERSION_NUM = 180006`) in `pgsty/openhalo`, extended with protocol, ModifyTable conflict, RI foreign-key, atomic sequence, and locale hooks. |
| Tag `v18.6.1` (`2627e6f`) | Current source tag on `main` (`2627e6f3e94ffdaba9ca6a835c4a1ae2fba34183`, annotated tag `55aab1f7ef3ce5d4f2893dcf76e6a6c270c4cf89`); ships **`aux_mysql 1.9`**, adding four copyright-header/documentation commits on top of accepted `6a93e8f` with zero executable C/SQL/grammar changes (`e1f2424` clean-archive re-verified). |
| Accepted commit `6a93e8f` | `6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a`; **`aux_mysql 1.9`** snapshot pinned by the independent 2026-11-10 final source acceptance, binary SHA-256 digests, and benchmark measurements. Versions `1.6`–`1.8` are internal SQL upgrade steps, never released standalone. |
| Pre-acceptance tip `a000baa` | `a000baaf68602eda91ccf0b83aca02a7bf694cb1`; remote branch tip at the start of the 2026-11-10 acceptance audit, missing the final character-boolean `DEFAULT` unique-key fix. Superseded by `6a93e8f` and `v18.6.1`; do not package. |
| Tag `v18.6` (`60e7a22`) | Initial PG18 tag (`60e7a225f2182b0a056501dba1aa79e358f9cbb1`); installs **`aux_mysql 1.5`**. Earlier `openhalodb-18.6` source/RPM inputs point to this `1.5` baseline; multi-platform binary packages for `v18.6.1` still await package-level acceptance. |
| `5.7.32-log` | Default string in `mysql.halo_mysql_version`, `VERSION()`, and `@@version`. Controls handshake charset announcement and `/*!NNNNN ... */` gating; **does not** identify the `aux_mysql` version or guarantee full MySQL 5.7 equivalence. |
| Tag `v1.0-pg14` | `f9aedb893233f1f95afcd72206df8707ce8f8d64` on branch `pg14` (upstream `90fc8d7` plus two PGSTY socket/default commits); historical PG14 line. |
{.wide .expand}

Kernel and extension binaries must always come from the same build. Although `PG_VERSION` remains `18.6` (`PG_VERSION_NUM = 180006`), PG18 catalog compatibility does **not** make `aux_mysql.so` loadable into stock PostgreSQL 18, and `v18.6`'s earlier claim that unmodified stock PGDG C extension binaries load directly no longer holds in `v18.6.1` (`aux_mysql 1.9`) because `ClientSocket`, `OnConflictClause`, `ModifyTable`, and `pg_locale` structures/callbacks changed—rebuild and test third-party C extensions against OpenHalo 18 headers.

## Five-level compatibility contract {#contract}

Evaluating a MySQL workload against OpenHalo 18 requires distinguishing five different levels that are often conflated:

1. **Syntax accepted** — the parser accepts a clause without executing it. For example, `USE INDEX`, `IGNORE INDEX`, and `FORCE INDEX` parse across `SELECT`, `UPDATE`, and `DELETE`, then are discarded before planning.
2. **Setting echoed** — a variable or `sql_mode` flag can be assigned and read back without switching engine behavior. Examples include `wait_timeout`, non-default `auto_increment_increment` / `auto_increment_offset`, `ANSI_QUOTES`, `REAL_AS_FLOAT`, and direct `SET collation_connection = 'utf8mb4_unicode_ci'`.
3. **Behavior implemented** — the server enforces the rule at execution time, either with exact MySQL 5.7 semantics (such as `utf8mb4_general_ci` column comparisons, all-key `ON DUPLICATE KEY UPDATE` / `REPLACE`, `FOREIGN_KEY_CHECKS=0`, `GLOBAL read_only`, and boolean `1`/`0` writes) or through an explicit PostgreSQL mapping (such as read-write `REPEATABLE READ` running as PostgreSQL `READ COMMITTED`, or non-exact collations mapping with warning `1105`).
4. **Independently verified** — differential tests against live Oracle MySQL `5.7.32` checked stored values, `HEX` bytes, affected-row counts, warning codes, error codes, transaction rollback, and `1.5 → 1.9` upgrades on the named `aarch64` builds at commit `6a93e8f`.
5. **Full compatibility guarantee** — **not claimed**. Unprobed type combinations, workload-specific SQL forms, production multi-platform packages, and third-party extension combinations still require validation on your own schema and queries.

Across implemented features, the core safety rule is **no silent corruption**: non-strict `sql_mode` and `INSERT IGNORE` keep documented MySQL truncations and warnings where representable, but never strip `NUL` bytes from text, never weaken enforced constraints, and never clip unrepresentable `BIGINT UNSIGNED` values onto an existing unique key. Review the [complete boundary reference](/openhalo/18/compatibility/) before migrating an application.

## Documentation basis and licensing {#sources}

This manual is distilled directly from `README.md`, `CHANGELOG.md`, `contrib/aux_mysql/{README,MIGRATION,TESTING,ROUTE_A_RECHECK,UPSTREAM}.md`, and the C/SQL/generator implementation and regression suites in `v18.6.1` (`2627e6f3e94ffdaba9ca6a835c4a1ae2fba34183`), together with the independent final acceptance artifacts pinned to `6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a` (dated 2026-11-10). Where repository prose, C/SQL code, and live test outputs differed in emphasis, the actual C/SQL code and recorded `6a93e8f` execution evidence govern.

PostgreSQL 18.6 and the protocol hooks retain the PostgreSQL License (Portions Copyright (c) 1996–2025, PostgreSQL Global Development Group); `contrib/aux_mysql` derives from GPLv3 openHalo (Copyright (c) 2025, Halo Tech Co., Ltd.; Portions Copyright (c) 2026, PGSTY PTE. LTD.), so builds containing `aux_mysql` are distributed under GNU GPL v3. Provenance hashes for source files, acceptance artifacts, and paired English/Chinese pages are recorded in `data/imports/openhalo-pgsty.json`; see [attribution](/attribution/#openhalo).
