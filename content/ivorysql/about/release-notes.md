---
title: Release notes
linkTitle: Release
description: 'IvorySQL v5.6 documentation: Release notes.'
type: docs
weight: 30
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/1.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---


## 1. Version Overview {#version-overview}

&#91;**Release Date: September 18, 2026**&#93;

IvorySQL 5.6 updates the PostgreSQL core to version 18.6 and delivers fixes for Oracle compatibility, memory safety, client interfaces, and extension builds. For a comprehensive list of updates, please visit our [documentation site](https://docs.ivorysql.org/).

## 2. Upstream Updates {#upstream-updates}

PostgreSQL 18.5 was not released because a regression was discovered during release preparation.

- PostgreSQL 18.6

  1.  Restrict logical decoding output plugins to the set specified by a new server parameter `output_plugin_libraries`.

  2.  Fix contrib/pgcrypto’s PGP encryption to detect unsupported ciphers.

  3.  Fix psql to skip in-line data following a scripted `COPY …​ FROM STDIN` command, even if the `COPY` fails before sending `PGRES_COPY_IN`.

  4.  Check for `USAGE` privilege on data types in places that formerly failed to check that.

  5.  Invalidate role-dependent cached plans after role changes.

  6.  Ensure that parallel GIN index builds update the table’s `pg_class.reltuples` value correctly.

For further details, visit [PostgreSQL 18.6 release notes](https://www.postgresql.org/docs/release/18.6/).

## 3. Enhancements {#enhancements}

- Upgrade to PG 18.6 kernel: Feature [\#1719](https://github.com/IvorySQL/IvorySQL/pull/1719)\
  PostgreSQL kernel upgraded to version 18.6.

- PGNexus Now Supports IvorySQL 5.6\
  PGNexus is now fully compatible with IvorySQL 5.6, bringing a zero-barrier, cloud-based AI-assisted experimentation experience. As a one-stop knowledge and experimentation platform for a wide range of scenarios, PGNexus lets users build environments with one click through an online sandbox, with no local installation required. It supports patch application, testing, and validation across multiple topologies, including standalone, streaming replication, logical replication, and high-availability clusters. Ready to use out of the box, PGNexus helps universities, enterprises, and developers collaborate efficiently and rapidly explore new version features.\
  [Learn more about PGNexus](https://pgnexus.ai)\
  [Try the IvorySQL 5.6 sandbox](https://pgnexus.ai/sandboxes)

- AI-assisted contribution guidelines: Feature [\#1473](https://github.com/IvorySQL/IvorySQL/pull/1473)\
  Establish guidelines covering licensing compliance, human review and sign-off responsibilities, AI tool attribution, disclosure of AI-generated code percentages, and responsible participation in code reviews.

- IvorySQL 5.6 [Online Experience](http://trial.ivorysql.org/): Feature [\#12](https://github.com/IvorySQL/ivorysql-wasm/pull/12)\
  An interactive, browser-based environment is now available, allowing users to explore and evaluate IvorySQL 5.6 in real time — no installation required.

- Packaging for All Platforms\
  Provides multi-platform media packages for X86, ARM, MIPS, and LoongArch architectures.

- Containerized Deployment Support\
  Supports quick deployment of standalone or highly available IvorySQL 5.6 clusters via Docker Compose, Podman, Swarm, Helm, and the IvorySQL 5.6 Operator.

- IvorySQL Cloud 5.6 released (Visual Database Lifecycle Management Platform)\
  Offers a fully managed, graphical control plane that handles IvorySQL 5.6 database subscriptions, orchestrates end-to-end lifecycle operations, and integrates surrounding ecosystem services.

- Extensions\
  Support for 34 Extensions and Tools: AGE, ddlx, pg_ai_query, pg_bigm, pg_bulkload, pg_cron, pg_curl, pg_hint_plan, pg_jieba, pg_partman, pg_profile, pg_readonly, pg_repack, pg_show_plans, pg_stat_monitor, pg_textsearch, pgagent, pgaudit, pgBackRest, pgBouncer, PgDog, pgnodemx, PGroonga, pgRouting, pgsql-http, pgtt, pgvector, plpgsql_check, PostGIS, redis_fdw, set_user, system_stats, wal2json, zhparser.

## 4. Fixed Issues {#fixed-issues}

- Fix potential overflow and NaN mishandling in Oracle-compatible interval multiplication and division: PR [\#1211](https://github.com/IvorySQL/IvorySQL/pull/1211)

- Disallow persisting ivorysql.compatible_mode through ALTER USER/ROLE/DATABASE SET, and close the SET …​ TO DEFAULT and parameter-specific RESET bypasses: PR [\#1372](https://github.com/IvorySQL/IvorySQL/pull/1372)

- Fix package-qualified variable references resolving to unrelated local variables during expression evaluation: PR [\#1381](https://github.com/IvorySQL/IvorySQL/pull/1381)

- Fix build failures with GCC 14 and later: PR [\#1385](https://github.com/IvorySQL/IvorySQL/pull/1385)

- Fix validation of conflicting or repeated SHARD options on sequences: PR [\#1401](https://github.com/IvorySQL/IvorySQL/pull/1401)

- Fix build failures of third-party PostgreSQL extensions against IvorySQL: PR [\#1448](https://github.com/IvorySQL/IvorySQL/pull/1448)

- Make ivorysql.enable_case_switch visible in SHOW ALL and configurable in configuration files: PR [\#1450](https://github.com/IvorySQL/IvorySQL/pull/1450)

- Fix missing package names and wrong schema qualification in DBMS_UTILITY backtrace and call-stack output: PR [\#1471](https://github.com/IvorySQL/IvorySQL/pull/1471)

- Fix incorrect newline handling and m/n option behavior in REGEXP_COUNT, REGEXP_SUBSTR, REGEXP_INSTR, and REGEXP_REPLACE: PR [\#1489](https://github.com/IvorySQL/IvorySQL/pull/1489)

- Fix Ivyresult memory leaks on early-return paths: PR [\#1556](https://github.com/IvorySQL/IvorySQL/pull/1556)

- Fix heap buffer overruns in psql named-bind query escaping and \bind handling: PR [\#1569](https://github.com/IvorySQL/IvorySQL/pull/1569)

- Fix heap buffer overflows when long namespace prefixes or URLs are used in XML functions: PR [\#1827](https://github.com/IvorySQL/IvorySQL/pull/1827)

## 5. Source Code {#source-code}

IvorySQL’s development is maintained across four main repositories:

- IvorySQL database source code: <a href="https://github.com/IvorySQL/IvorySQL" class="bare">https://github.com/IvorySQL/IvorySQL</a>

- IvorySQL official website: <a href="https://github.com/IvorySQL/Ivory-www" class="bare">https://github.com/IvorySQL/Ivory-www</a>

- IvorySQL documentation: <a href="https://github.com/IvorySQL/IvorySQL_docs" class="bare">https://github.com/IvorySQL/IvorySQL_docs</a>

- IvorySQL Docker: <a href="https://github.com/IvorySQL/docker_library" class="bare">https://github.com/IvorySQL/docker_library</a>

## 6. Contributors {#contributors}

The following individuals (in alphabetical order) have contributed to this release as patch authors, committers, reviewers, testers, or reporters of issues.

- 123123213weqw

- Aias00

- ai-yang

- btlqql

- Cédric Villemain

- db-nikhil

- digoal

- enkilee

- Fawei Zhao

- Ge Sui

- goeason-world

- Grant Zhou

- hanjianqiao

- lispking

- messere1

- NotHimmel

- Shuntian Jiao

- Steven Niu

- tian1220A

- Xiangyu Liang

- Xiaohui Liu

- Xinjie LYU

- Xueyu Gao

- xuhuicai

- yaozichen2025

- Yasir Hussain Shah

- yyqdbngt

- Z95-cmyk

- Zhe Zhang

- Zheng Tao

- Zhenhao Pan

- Zhuoyan Shi

[Complete Changelog](https://github.com/IvorySQL/IvorySQL/compare/IvorySQL_5.4...IvorySQL_5.6)
