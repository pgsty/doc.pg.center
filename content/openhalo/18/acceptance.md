---
type: docs
upstream_link: ""
search_keywords: ["6a93e8f", "6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a", "2627e6f", "2627e6f3e94ffdaba9ca6a835c4a1ae2fba34183", "v18.6.1", "a000baa", "GCC 14", "231", "922", "FIND_IN_SET", "GO", "NO-GO", "final acceptance", "最终验收"]
title: Final acceptance and release conditions
description: Frozen 2026-11-10 acceptance verdict for commit 6a93e8f, post-acceptance source tag v18.6.1 (2627e6f) delta, verified binary SHA-256 digests, test and performance evidence, unverified scope, and remaining package gates.
weight: 60
---

**Acceptance date:** `2026-11-10` (`Asia/Shanghai`) · **Evaluated source commit:** `6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a` (`aux_mysql 1.9`).

- **Evaluated `6a93e8f` source verdict: Conditional GO** within the agreed `aux_mysql 1.9` compatibility scope. Every required build, core regression, differential suite, upgrade/restore test, and final-blocker check passed with zero open candidate-code blockers. Previously reproduced wrong-row writes on `> UINT64_MAX` unsigned keys, wrong-row writes on boolean literals/casts/defaults, `FIND_IN_SET` trailing-space mismatches, and multi-fold `general_ci` sort slowdowns are closed at `6a93e8f`. The condition is accurate public disclosure of the [compatibility boundaries](/openhalo/18/compatibility/)—never marketing OpenHalo 18 as full drop-in MySQL 5.7 equivalence.
- **Audit-time branch (`a000baa`) vs post-acceptance source tag `v18.6.1` (`2627e6f`) and binary packages**: At the time of the `6a93e8f` acceptance audit on `2026-11-10`, `origin/master` was still at `a000baaf68602eda91ccf0b83aca02a7bf694cb1` (**NO-GO**, missing the character-boolean `DEFAULT` unique-key fix) and earlier `openhalodb-18.6` RPM/source inputs still shipped `aux_mysql 1.5` (**NO-GO** for a `1.9` release). Later on `2026-11-10`, the repository merged `6a93e8f` into `main` and published **source tag `v18.6.1`** (`2627e6f3e94ffdaba9ca6a835c4a1ae2fba34183`, annotated tag `55aab1f7ef3ce5d4f2893dcf76e6a6c270c4cf89`): the four commits `6a93e8f..2627e6f` (`e1f2424`, `1d7e45e`, `2ae3a15`, `2627e6f`) add only copyright comment headers, `.gitignore` rules, and documentation updates with **zero executable C, SQL, or grammar rule changes**, and `e1f2424` underwent clean-archive debug/release re-verification (`ROUTE_A_RECHECK.md`). **Production multi-platform RPM/DEB binary packages remain pending** target-matrix package builds and package-level acceptance.

This page keeps the independent `2026-11-10` binary digests, differential counts, and benchmark measurements strictly pinned to `6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a` rather than silently attributing them to later commits or unvalidated binary packages.

## Accepted object and repository identities {#identity}

| Item | Verified state |
| --- | --- |
| Pinned acceptance commit | `6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a` (branch `codex/aux19-boolean-defaults` at audit time, clean working tree) |
| Candidate version | PostgreSQL `18.6` (`PG_VERSION_NUM = 180006`) kernel with OpenHalo hooks + `aux_mysql 1.9` |
| Audit-time `origin/master` | `a000baaf68602eda91ccf0b83aca02a7bf694cb1` — lacked the `6a93e8f` boolean-default key-arbitration fix (**NO-GO** as-is) |
| Post-acceptance `main` & `v18.6.1` | `2627e6f3e94ffdaba9ca6a835c4a1ae2fba34183` (annotated tag `v18.6.1` `55aab1f7ef3ce5d4f2893dcf76e6a6c270c4cf89`, `2026-11-10 18:16:14 +0800`); `6a93e8f` + 4 copyright-header/`.gitignore`/doc commits (`0` executable C/SQL/grammar changes; `e1f2424` clean-archive re-verified: `231/231` core, `26/26` smoke, `23/23` integration/upgrade, `922` `release_fixes.py`) |
| Historical Git tags | `v18.6` (`60e7a225f2182b0a056501dba1aa79e358f9cbb1`, annotated tag `5086d18f03af2794b69c87c784768a7aeb5d43e9`, `aux_mysql 1.5`) and `v1.0-pg14` (`f9aedb893233f1f95afcd72206df8707ce8f8d64`) |
| Source byte identity | `git archive` of `6a93e8f` (`7,464` tracked files) matched the checkout, EL9 build tree, and EL10 build tree byte for byte (`v18.6` baseline: `7,391` files; `a000baa`: `7,464` files) |
| Reference oracle | Live Oracle MySQL Community Server `5.7.32` (`VERSION() = '5.7.32'`) |
| Candidate builds | Three clean from-archive builds (`--with-openssl --enable-depend`, `-O2`, implicit-function-declaration and int-conversion treated as errors): **EL9 Debug** (`--enable-debug --enable-cassert`, Rocky Linux 9.8 `aarch64`, GCC `11.5.0`), **EL9 Release** (same host/compiler), and **EL10 GCC 14** (Rocky Linux 10.2 `aarch64`, GCC `14.3.1` in an isolated container) |
| Process verification | Live `/proc/<pid>/exe` and mapped `aux_mysql.so` SHA-256 digests were verified for every tested server process rather than trusting port numbers or directory names |
{.wide .expand}

The acceptance audit modified zero product files, test scripts, or `expected/` outputs. Shared-memory exhaustion from the container host's 64 MiB `/dev/shm` was avoided via test-instance `dynamic_shared_memory_type = mmap` without altering product defaults.

## Verification matrix {#tests}

| Verification suite | EL9 Debug (`GCC 11.5.0`) | EL9 Release (`GCC 11.5.0`) | EL10 (`GCC 14.3.1`) |
| --- | --- | --- | --- |
| Clean archive build & install | PASS | PASS | PASS |
| PostgreSQL core `installcheck` | `231 / 231` | `231 / 231` | `231 / 231` |
| `tests/run.sh` wire & driver smoke | `26 / 26` (`0` skips) | `26 / 26` (`0` skips) | Full smoke not repeated |
| `tests/release_fixes.py` | `922` assertions | `922` assertions | `922` assertions |
| `TESTING.md` integration, Route A, history & recovery | `23 / 23` invocations | `23 / 23` invocations | Matrix not repeated |
| Real `v18.6` (`1.5`) → `1.9` binary + SQL upgrade | PASS | PASS | Not repeated |
| Legacy Connector/J `5.1.49` (TLS, text & prepared) | PASS | PASS | Not repeated |
| Independent boolean & default oracle matrix | `547` groups (`0` diffs) | `547` groups (`0` diffs) | Covered via `release_fixes.py` |
| Adversarial random-string collation oracle | `4,000` strings (`seed 191106`, `0` diffs) | Same | Not repeated |
{.wide .expand}

Assertion and group counts overlap across harnesses and **must not be summed into a single "total test cases" marketing number or compatibility percentage**:

- **Generator & clean-tree checks**: all `5` generated grammar/SQL outputs (`mys_gram.y`, `aux_mysql.sql`, `aux_mysql_fix_show.sql`, `aux_mysql--1.6--1.7.sql`, `aux_mysql_update18.sql`) regenerated byte-for-byte from `pg14`; zero residual `text_string` references remained.
- **Smoke & driver coverage (`26/26`, `0` skips)**: SQL regression scripts (`p3`–`p9`, `m1`–`m4`), `46` AB differential cases, PyMySQL, raw `COM_STMT_*` binary packets, TLS/RSA and bad-password rejection, `mysql` CLI, `mysqlslap`, freshly built `go-sql-driver/mysql` `1.9`, and Connector/J `8.4.0`. Missing dependencies exit `2` (incomplete) and were never counted as `PASS`.
- **Route A per-package counts (each EL9 build)**: `text` (`375`), `binary` (`122`), `char` (`42`), `collation` (`468`), `collation_all` (`9,945` across `221` MySQL 5.7 character collations × `3` types, explicitly logging the **246 expected locale/encoding differences** under the `1105` approximation contract), `numeric_cast` (`372`), `uint64` (`167`, seeding an `INT64_MAX` row before testing `> UINT64_MAX` writes and rollback), `prefix_nul` (`19`), `hints` (`315`), and `route_a_fk_privileges` (`46`).
- **Independent 547-group boolean/default probe**: `480` boolean writes (`10` types × `6` boolean expressions × `4` write forms × `2` `sql_mode`s) + `16` seeded unique-key collision writes (`INSERT`, `ODKU`, `REPLACE`, `UPDATE IGNORE`) + `32` `DEFAULT` / default-conflict cases + `19` `ALTER` / transaction / reconnect cases against live MySQL `5.7.32`, comparing values, `HEX`, warning levels/codes, error codes, and (for the `480 + 16` write/conflict groups, captured **before** `SHOW WARNINGS`) affected-row counts—with **zero differences**.
- **Stock PostgreSQL 18 standalone harnesses**: `indexes_standalone.py` and `binary_fix/run.sh` passed on unmodified PG18, covering libpq text/binary wire I/O, NUL-prefix defense, concurrency, cache invalidation, and `pg_dump`/`pg_restore`.

## Upgrade and backup/restore evidence {#upgrade}

- **Real `v18.6` (`1.5`) → `1.9` restart upgrade**: initialized with actual `v18.6` binaries and `aux_mysql 1.5` (with `1.5`'s racy background auto-installer disabled), populated numeric, character/binary, prefix-key, checked/unchecked FK, orphan-row, discarded-generator, boolean-default, view, `BEGIN ATOMIC` procedure, and `DO`-backed trigger objects over the MySQL protocol, stopped `v18.6`, started the same data directory under `6a93e8f`, and executed `ALTER EXTENSION aux_mysql UPDATE`. Both open and newly connected MySQL sessions, repeated prepared statements, inherited boolean defaults, and dependent views worked cleanly. *(Note: the `BEGIN ATOMIC` procedure and `DO` trigger body verify survival of existing catalog objects across upgrade, not support for MySQL 5.7 stored-routine syntax.)*
- **Raw catalog parity (`1.5 → 1.9` vs fresh `1.9`)**: **zero raw differences** across `3,476` extension members, `1,859` functions/procedures, `20` views, `272` view columns, `88` casts, `665` operators, and `27` operator classes—plus an independent catalog audit of `596` types, `13` domain constraints, `5` collations, `1,866` function attribute rows (including `7` aggregates), `7` aggregate definitions, and `201` relation attributes. Only the separate **unreleased `1.6 → 1.7 → 1.8 → 1.9` chain** retains the documented `pg_catalog.default` vs `pg_catalog.C` collation difference on `mys_informa_schema.columns.extra`.
- **Logical dump & restore round trips**: verified native `pg_dump`/`pg_restore` and Oracle MySQL `5.7.32` `mysqldump`/`mysql` round trips—including replaying OpenHalo's unmodified `mysqldump` output directly into live MySQL `5.7.32`—preserving `NUL` and arbitrary binary bytes, hex defaults, generated columns, prefix primary keys, pending missing-parent FK triggers, and historical orphan rows while enforcing new writes and cascades after restore.

## Performance evidence and scope {#performance}

Benchmarks ran on the EL9 `aarch64` host (`GCC 11.5.0 -O2` release builds) over **300,000 rows** after all compilation and regression jobs finished, using 1 warm-up plus 10 interleaved rounds:

- **`ORDER BY` workload**: sorting 32-character `MD5(id)` strings under `utf8mb4_general_ci`, measured inside PostgreSQL via `EXPLAIN (ANALYZE, TIMING OFF)` with `work_mem = '64MB'`, `jit = off`, and `max_parallel_workers_per_gather = 0`.
- **`FIND_IN_SET` workload**: full client-timed round-trip aggregate over an 8-item comma-separated list across all 300,000 rows (deterministic sum `1350000`).

| Build / baseline | `ORDER BY` median (10-round range) | `FIND_IN_SET` client median |
| --- | ---: | ---: |
| Candidate `6a93e8f` (`aux_mysql 1.9`) | **`63.82 ms`** (`57.98–76.12 ms`) | **`0.677 s`** |
| Preceding `a000baa` (`aux_mysql 1.9`) | `59.97 ms` (`56.05–124.12 ms`) | `0.688 s` |
| Published `v18.6` (`aux_mysql 1.5`, ICU) | `102.24 ms` | `3.049 s` |
| Reference MySQL `5.7.32` (3-sample reference) | *(different timing layer; not tabulated)* | **`~0.073 s`** |
{.wide .expand}

**Interpretation boundaries:**

- Relative to published `v18.6`, candidate `6a93e8f` reduced `ORDER BY` time by **~38%** and `FIND_IN_SET` time by **~78%**, confirming that the earlier multi-fold `1.9` sorting regression did not recur.
- Candidate `6a93e8f` and `a000baa` run identical collation/sorting code; their 10-round ranges overlap (`63.82 ms` vs `59.97 ms` in the quiet 10-round run, while an earlier 3-sample run recorded `58.14 ms` vs `62.80 ms`), reflecting shared-host background variance rather than a code difference.
- **`FIND_IN_SET` remains ~9× slower than MySQL `5.7.32` (`0.677 s` vs `0.073 s`)** because it is still an SQL function (`unnest(string_to_array(...))`), not a C implementation. Cross-engine `ORDER BY` numbers are intentionally omitted from direct comparison because server-internal `EXPLAIN (ANALYZE, TIMING OFF)` and client-side protocol timing do not measure the same path. These figures do not substitute for dedicated bare-metal benchmarks on customer queries.

## Audit artifact SHA-256 fingerprints {#evidence}

The acceptance archive retains `FINAL_REPORT.md`, `verification.json`, `SHA256SUMS`, process maps, build logs, per-suite exit codes, raw SQL/HEX/warning transcripts, catalog diffs, and all benchmark samples. These digests verify an audit copy; they **do not** imply a public package download URL exists:

| Verified audit artifact | SHA-256 |
| --- | --- |
| Candidate `git archive` snapshot (`source.tar.gz`) | `e0a7fc4a2e278985847e575121e60a2f92e7cea5b3b5a1f551721c6fa4b2c6f5` |
| Complete acceptance evidence bundle (`evidence.tar.gz`, `33,580,392` bytes) | `df0c062078ab9cfdf612fea4c905aa7eb203ccfef614d3b6d55558799d78803c` |
| EL9 Debug `postgres` (`Rocky 9.8 aarch64`, `GCC 11.5.0`) | `631926e75e09c7fe630c33aedb1434fe3ef3497749d907d3838ce8eff88ae1ea` |
| EL9 Debug `aux_mysql.so` | `f895c7421412ef46135b971878e51c598edf95f0bb5df7589eba34d68e9ea3d9` |
| EL9 Release `postgres` (`Rocky 9.8 aarch64`, `GCC 11.5.0`) | `2d054ec9405cd4cfdffb8190f4efe358e4752e9857b337562cc4888dfd9ee326` |
| EL9 Release `aux_mysql.so` | `6eac22a68a39d47296a688464ea0a950c5156be0f1e495a7cbb1ce1534b96557` |
| EL10 Release `postgres` (`Rocky 10.2 aarch64`, `GCC 14.3.1`) | `cb443a169f60cc21074fa3a7fdf1746c6e3ccb249f9ef244fe2f2e4f51cadcb5` |
| EL10 Release `aux_mysql.so` | `80bcdc4fe4afc93f67ac64b6597d4becd0083799d6eef0def47c283b19069b37` |
{.wide .expand}

To reproduce from source, export `6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a` into a clean directory and run the isolated disposable-instance procedures in `contrib/aux_mysql/TESTING.md`. Never point the regression suites at a shared or production database (several tests recreate schemas and toggle `GLOBAL read_only` / `super_read_only`), and always build actual `v18.6` binaries for `release_real_upgrade.py` rather than simulating `1.5` on new binaries.

## Release-delivery gates status {#release-gates}

1. **D1 — Merge `6a93e8f` into the main branch and tag source (`Completed at source level as v18.6.1`)**: `6a93e8f` was merged onto `main` and tagged **`v18.6.1`** (`2627e6f3e94ffdaba9ca6a835c4a1ae2fba34183`), superseding pre-acceptance `a000baa` with only copyright-header, `.gitignore`, and documentation commits (`e1f2424`..`2627e6f`).
2. **D2 — Cut a new immutable package source archive and update RPM/DEB specs (`Pending`)**: existing `openhalodb-18.6` packaging inputs (`source tarball sha256: 6fdd17769c1f25bc4bf9e3677afeb940b73eb9a401dcea13616391fa38d064b4`) still package `default_version = '1.5'`. Cut an immutable `18.6.1` source archive from `v18.6.1` (`2627e6f`) and update RPM/DEB specs without overwriting the historical `18.6` archive.
3. **D3 — Build and validate final platform packages (`Pending`)**: on every supported OS/architecture target, verify main and debuginfo package payloads, runtime library dependencies, fresh dual-protocol installation, real `1.5 → 1.9` package upgrade, and `pg_dump` / `mysqldump` restore before signing and publishing repositories.
4. **D4 — Ship compatibility and migration documentation alongside packages (`Completed in source & manual; attach to package release notes`)**: repository docs (`v18.6.1`) and this manual publish the [compatibility boundaries](/openhalo/18/compatibility/) and [non-self-healing upgrade audit rules](/openhalo/18/migration/#audit); link them directly from binary package release notes.

Because `v18.6.1` (`2627e6f`) introduces zero executable C, SQL, or grammar changes relative to `6a93e8f` (and `e1f2424`'s header-comment regeneration was re-verified from a clean archive), source-level differential suites do not need to be re-run blindly—**multi-platform package builds and package-level acceptance (`D2` and `D3`) are what remain mandatory before announcing binary packages**. Any subsequent change to source code, compiler flags, or installation layout requires re-running the affected suites.

## Unverified areas and insufficient evidence {#limits}

The following items were **not** verified in this acceptance run and carry **no `PASS` claim** (insufficient evidence until tested explicitly):

- **Production multi-platform packages & other architectures/compilers**: six-platform production RPM/DEB builds, `x86_64` binaries, Debian/Ubuntu toolchains, and Clang builds were not executed at `6a93e8f` (only EL9 `aarch64` GCC `11.5.0` and EL10 `aarch64` GCC `14.3.1` source builds were verified).
- **Third-party PostgreSQL extension binary/runtime coexistence**: extensions such as `pg_tde`, `orioledb`, `PostGIS`, `pgvector`, `Citus`, and `TimescaleDB` were not rebuilt or integration-tested against `6a93e8f`'s modified node/callback headers (early smoke tests at `c380da3` predated commit `c247eca`'s struct changes).
- **Untested legacy client versions**: an exploratory Connector/J `5.1.40` probe failed JDK TLS handshake negotiation before query execution—providing evidence neither of `5.1.40` compatibility nor of a wire-metadata regression (`5.1.49` and `8.4.0` passed). Clients requiring `mysql_native_password` exclusively without `caching_sha2_password` or `mysql_clear_password` remain outside scope.
- **Exhaustive non-boolean temporal/JSON expression matrices & workload soak tests**: `DATE`/`TIME`/`DATETIME`/`TIMESTAMP`/`YEAR`/`JSON` non-boolean expression combinations were not exhaustively re-enumerated across every SQL context in this round, and customer production workloads, extreme-skew `mysql_prefix` benchmarks, multi-day soak/capacity tests, and formal security penetration audits were not performed.
- **Non-zero compiler warnings**: while implicit function declarations and integer/pointer conversions passed as `-Werror` checks, `3` unused-function / variable-shadow warnings remain under GCC `11.5.0` and `9` warnings (adding `-Wmissing-variable-declarations` on inherited globals) remain under GCC `14.3.1`.

For historical context on the pre-fix baseline, see the preserved [2026-11-07 initial OpenHalo 18 review at `9dc937f`](/openhalo/mysql57-compatibility-review/).
