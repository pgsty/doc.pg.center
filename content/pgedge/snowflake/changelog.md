---
title: Changelog
description: All notable changes to the Snowflake extension are documented here.
weight: 200
upstream_source: pgedge-snowflake
upstream_link: https://github.com/pgEdge/snowflake/blob/429a16803c8c6336fcfede7cce0ccd3de05216d8/docs/changelog.md
upstream_modified: true
upstream_ref: 429a16803c8c
source_kind: pinned-main-snapshot
type: docs
---



All notable changes to the Snowflake extension are documented here.

## 2.6.0  {#260}

### Added {#added}

- Added support for Postgres 19


## 2.5.0  {#250}

### Added {#added-1}

- PG18 support: added a PG18 test configuration and adjusted the Docker
  build to skip LLVM bitcode compilation on PG18.

### Changed {#changed}

- Adopted three-digit (`MAJOR.MINOR.PATCH`) versioning. The extension
  version is now `2.5.0`.

### Fixed {#fixed}

- Fixed dump/restore of snowflake-converted sequences.
  `convert_sequence_to_snowflake()` previously left `MAXVALUE` at
  `(old last_value + 1)`, but `snowflake.nextval()` bypasses `MAXVALUE`
  and writes snowflake-sized values, so `pg_dump` could emit a `setval()`
  that failed to restore. Sequences are now converted with
  `AS bigint MAXVALUE 9223372036854775807`, and sequences converted by
  earlier versions are auto-repaired on upgrade. (SUP-140)
- Fixed the SQL command used to convert sequences to Snowflake.

### Security / CI {#security--ci}

- Pinned GitHub Actions to full commit SHAs to harden against supply
  chain attacks.
- Removed `shell=True` and shell-injection risks from test runner and
  helper subprocess calls; use `shlex.split()` for correct argument
  tokenization.
- Fixed a SQL injection warning and a missing parameter in
  `execute_sqlite_query`, and suppressed Bandit B603 warnings on internal
  test helper subprocess calls.
- Fixed the Dockerfile `ARG` handling for newer BuildKit versions.
- Updated the copyright year to 2026.

---

[Upstream source](https://github.com/pgEdge/snowflake/blob/429a16803c8c6336fcfede7cce0ccd3de05216d8/docs/changelog.md) · `429a16803c8c` · Copyright (c) 2023–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
