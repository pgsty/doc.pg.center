---
type: docs
upstream_link: ""
search_keywords: ["FIND_IN_SET", "boolean defaults", "布尔默认值", "UINT64_MAX", "ODKU", "REPLACE", "v18.6.1", "2627e6f", "6a93e8f", "a000baa", "sorting performance", "排序性能"]
title: Changes since v18.6
description: Complete engineering record from released v18.6 (aux_mysql 1.5) to accepted 6a93e8f and source tag v18.6.1 (aux_mysql 1.9), linking initial blockers, WP1–WP10, final correctness fixes, and sorting recovery.
weight: 20
---

This page traces every substantive change between the initial **`v18.6` tag (`60e7a225f2182b0a056501dba1aa79e358f9cbb1`, `aux_mysql 1.5`)** and **`aux_mysql 1.9`**—accepted at **`6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a`** on `2026-11-10` and published as **source tag `v18.6.1` (`2627e6f3e94ffdaba9ca6a835c4a1ae2fba34183`)** on `main`. It records completed source engineering and verification; multi-platform `18.6.1` binary packages still await package-level acceptance. Extension versions `1.6`, `1.7`, and `1.8` are internal SQL upgrade steps (`1.5 → 1.6 → 1.7 → 1.8 → 1.9`) that were never released standalone.

The engineering progression followed five stages (followed by source tag publication):

1. **Initial independent NO-GO review (`9dc937f`, 2026-11-07)** — identified seven P1 blockers (`B01`–`B07`) and thirteen additional behavioral differences (`B08`–`B20`).
2. **Kernel & extension foundation (`cffcee6`..`517cd0b`, `1.6`–`1.9` base)** — added PostgreSQL 18 conflict, FK, sequence, and collation hooks plus core DML, transaction, binary, index, lock, and generated-column implementations.
3. **Ten Route A work packages (`8cf384d`..`2a7f1e7`, WP1–WP10 + `f0dc476`)** — resolved type, conversion, collation-search, unsigned-key, prefix-NUL, real `1.5` upgrade, index-hint, and pending-FK ACL gaps.
4. **Final correctness & sorting speed fixes (`aa25342`, `6f9c4f3`, `a000baa`, `6a93e8f`)** — closed remaining wrong-row corruption paths on `> UINT64_MAX` inputs and boolean/default writes, fixed `FIND_IN_SET` trailing spaces and legacy driver metadata, and eliminated a multi-fold `general_ci` sort regression.
5. **Independent final acceptance & `v18.6.1` source tag (2026-11-10)** — verified `6a93e8f` across EL9 debug/release (`GCC 11.5.0`) and EL10 (`GCC 14.3.1`) against live MySQL `5.7.32`, then added four copyright-header/documentation commits (`e1f2424`..`2627e6f`, zero executable C/SQL/grammar changes; `e1f2424` clean-archive re-verified) and tagged `v18.6.1`.

## Kernel and extension foundation {#foundation}

Compared with `v18.6` (`aux_mysql 1.5`), the `1.6`–`1.9` foundation introduced matched kernel hooks (`9dc937f`, `c247eca`) and extension subsystems (`cffcee6`..`517cd0b`):

- **Kernel hooks (`src/backend/` & `src/include/`)**: all-unique-index conflict arbitration and delete-then-insert `REPLACE` in `nodeModifyTable.c`; `FOREIGN_KEY_CHECKS=0` trigger gating and pending-FK hooks in `ri_triggers.c` and `trigger.c`; custom collation comparator / abbreviated-key methods in `pg_locale.c`; atomic monotonic sequence advancement (`SetSequenceValueAtLeast`) and read-only sequence guards in `sequence.c`; early Meson build rejection and `pg_upgrade` rejection of `1.0.14.x` binaries.
- **Protocol, comments, and prepared execution**: SQL `PREPARE` / `EXECUTE` / `DEALLOCATE`, `DO expr`, executable comments `/*! ... */` and `/*!NNNNN ... */`, MySQL `#` and whitespace-guarded `--` comments, trailing-comment OK packets, and literal `\%` / `\_` preservation for `LIKE`.
- **Transactions and access modes**: `START TRANSACTION WITH CONSISTENT SNAPSHOT`, effective `READ ONLY` (`1792`) and `GLOBAL read_only` / `super_read_only` (`1290`, including sequence writes), synchronized `tx_*` / `transaction_*` variables, and `1180` error reporting when `COMMIT` ends an aborted transaction.
- **DML, locks, keys, and types**: crash-free single-target `UPDATE ... JOIN` / comma-join matching; all-key `ODKU` / `REPLACE` with `VALUES(col)`, default filling on unlisted `REPLACE` columns, plain insert when no unique key exists, and MySQL affected-row accounting; length-aware `mysql.binary_n` / `mysql.varbinary_n`, `mysql.hexlit` (`0x..`, `X'..'`, `b'..'`, `0b..`), and `HEX()` / `UNHEX()`; `mysql_prefix` index access method with heap rechecks; per-table key names (`$<8-hex>` physical suffix); MySQL 5.7 user-level locks (`GET_LOCK` family); stored computation, allowlist validation, writer `sql_mode` coercion, and MySQL metadata export for `VIRTUAL` / `STORED` generated columns; preserved `DECIMAL(p,s)` and `DATETIME(0..6)` metadata.

The [functionality reference](/openhalo/18/features/) defines the resulting user-visible behavior.

### Disposition of the initial review findings {#initial-review}

The [2026-11-07 initial review at `9dc937f`](/openhalo/mysql57-compatibility-review/#blocking-issues) remains preserved verbatim as historical evidence. Its seven P1 blockers (`B01`–`B07`) and key secondary findings (`B08`–`B20`) reached the following dispositions in `6a93e8f`:

| Initial finding (`9dc937f`) | Disposition in `6a93e8f` (`aux_mysql 1.9`) |
| --- | --- |
| `B01` · `UPDATE ... JOIN` backend crash | **Fixed (`cffcee6`).** Rewritten safely without assertion failure or `SIGSEGV`; covered in debug and release DML suites. |
| `B02` · Unenforced foreign keys (`NOT ENFORCED`) | **Fixed for new DDL (`da426c5`, `c247eca`, `2a7f1e7`).** Enforces RI checks/actions, honors session `FOREIGN_KEY_CHECKS=0`, persists missing-parent pending FKs, and checks child-owner ACLs on bind. Pre-existing `NOT ENFORCED` FKs and orphan rows still require [migration audit](/openhalo/18/migration/#audit). |
| `B03` · `REPEATABLE READ` visibility | **Retained as explicit product mapping (`510d65f`).** Read-write `REPEATABLE READ` intentionally runs on PostgreSQL `READ COMMITTED`; read-only `REPEATABLE READ` and `START TRANSACTION WITH CONSISTENT SNAPSHOT` now provide a true repeatable snapshot. |
| `B04` · Ineffective read-only settings | **Fixed (`510d65f`, `c247eca`).** Transaction read-only (`1792`) and `GLOBAL read_only` / `super_read_only` (`1290`, including sequence advancement) are enforced per statement; `TEMPORARY` tables remain writable. |
| `B05` · `DECIMAL` export loses `(p,s)` | **Fixed (`381c6b7`).** `DECIMAL(p,s)` round-trips through `SHOW` and `information_schema`; bare `DECIMAL` defaults to `(10,0)`; untyped PG `numeric` warns `1105` as `decimal(65,30)`. |
| `B06` · Collation uniqueness (`PAD SPACE`) | **Fixed for four exact names (`0bf5d13`, `c247eca`, `4419811`, `6f9c4f3`).** `utf8_general_ci`, `utf8mb4_general_ci`, `utf8_bin`, and `utf8mb4_bin` enforce MySQL 5.7 weights and `PAD SPACE` uniqueness; other names warn `1105` as approximations; legacy ICU indexes are not rewritten in place. |
| `B07` · Prefix key uniqueness (`UNIQUE(col(n))`) | **Fixed for new keys (`92a181a`, `9ef2a83`).** Character/byte prefixes enforce uniqueness and `ODKU`/`REPLACE` via `mysql_prefix` heap rechecks and expose `Sub_part`; historical `1.5` indexes with discarded lengths require original DDL. |
| Secondary `B09`, `B11`, `B13`, `B19` | **Fixed in scope.** `AUTO_INCREMENT` generates IDs on `NULL` and `0` (honoring `NO_AUTO_VALUE_ON_ZERO`); `REPLACE` deletes and reinserts with new IDs, defaults, and row counts; new `BINARY(n)` pads with `0x00`; `INSERT IGNORE` truncates representable overflows with warnings and skips row-level key/FK conflicts. |
| Secondary `B08`, `B10`, `B12`, `B14`–`B18`, `B20` | **Documented boundaries or partial fixes.** Bare `TIMESTAMP` stays `timestamp without time zone` without cross-zone shift (`B08`); `auto_increment_increment`/`offset` (`B10`), `ANSI_QUOTES` (`B14`), and `wait_timeout` (`B15`) remain echoed-only; plain `UPDATE` still counts matched rows while `ODKU` is fixed (`B12`); multi-statement raw syntax errors still reject the packet before execution outside an active savepoint (`B16`); charset metadata (`45`/`63`), `SHOW VARIABLES`, and `SHOW WARNINGS` are improved while `SHOW STATUS` stays partial (`B17`); `PAD_CHAR_TO_FULL_LENGTH` works on covered conversions while functions like `LENGTH()` still trim (`B18`); `BIGINT UNSIGNED > INT64_MAX` fails cleanly with `1264` rather than supporting full `uint64` (`B20`). |
{.wide .expand}

## Ten Route A work packages {#work-packages}

After merging the `1.9` feature set (`6821954`), ten targeted work packages (`WP1`–`WP10`) and a conversion pass (`f0dc476`) addressed compatibility regressions and upgrade safety:

| Package & commit | Scope and verified outcome |
| --- | --- |
| `WP1` · Native `TEXT` (`8cf384d`) | Removed an unpublished custom `text_string` type; restored native PostgreSQL `text` across `TINYTEXT`/`TEXT`/`MEDIUMTEXT`/`LONGTEXT`, kept explicit `CHAR(n)` lengths in `CAST`, added `CONVERT(... USING ...)`, and enforced the `1366` `NUL` boundary across 375 assertions. |
| `WP2` · Binary-to-character (`894b949`) | Added UTF-8-validating assignment casts from `mysql.binary_n` / `mysql.varbinary_n` to `text`/`varchar`/`bpchar` (`1366` on `NUL` or bad UTF-8, including `BINARY(n)` padding) and byte-preserving binary `GROUP_CONCAT` (122 assertions). |
| `WP3` · `CHAR` logical values (`29a3d6d`) | Centralized `CHAR(n)` extraction so default mode trims trailing spaces and `PAD_CHAR_TO_FULL_LENGTH` retains full width across `CONCAT`, `CONCAT_WS`, `CAST`, `CONVERT`, `HEX`, `ELT`, `GROUP_CONCAT`, user variables, locks, and `EXECUTE` (42 assertions). |
| `WP4` · Collation searches (`4419811`) | Routed MySQL `LOCATE`, `INSTR`, and `POSITION` through collation-aware search (`general_ci` weight table, `bin` codepoints, and legacy ICU aliases) and added case-sensitive character `REPLACE()` (468 + 9,945 assertions). |
| `WP5` · Binary numeric `CAST` (`3f26bed`) | Dispatched `CAST`/`CONVERT` of `BLOB`/`VARBINARY`/`BINARY`/`UNHEX` to `SIGNED`/`UNSIGNED`/`DECIMAL` through a length-aware ASCII decimal parser (`NUL`/invalid UTF-8 terminate numeric prefix rather than raising `1366`), leaving native PG `bytea::int8` unchanged (372 assertions). |
| `WP6` · `uint64` high-half safety (`bc1d29c`) | Rejected `INT64_MAX + 1 .. UINT64_MAX` writes with `1264` (including `IGNORE` and binary `MYSQL_TYPE_LONGLONG` unsigned parameters) so distinct keys never collapse onto `INT64_MAX`, and allowed `INSERT IGNORE ... ON DUPLICATE KEY UPDATE`. *(Inputs `> UINT64_MAX` were tightened further in `F1` below.)* |
| `WP7` · Prefix `NUL` defense (`9ef2a83`) | Made `bin` and legacy collation prefix clipping count explicit lengths so embedded `NUL` cannot truncate an index key early, verified via a private stock-PG18 bridge while keeping production character `NUL` rejection (`1366`, 19 assertions + standalone suite). |
| `WP8` · Real `1.5 → 1.9` upgrade (`0dc12fe`) | Repaired missing upgrade metadata/diagnostic helpers, preserved `information_schema.columns.EXTRA` view descriptors, and verified an actual `v18.6` (`1.5`) data directory upgraded in place to `1.9` with zero raw catalog differences. |
| `WP9` · Ignored index hints (`311ef83`) | Parsed `USE`/`IGNORE`/`FORCE` `INDEX`/`KEY` across `SELECT`, `UPDATE`, and `DELETE`, and correlated `DELETE FROM target USING ...` self-joins by `(tableoid, ctid)` so hinted multi-table `USING` deletes succeed (315 assertions). |
| `WP10` · Pending FK owner ACLs (`2a7f1e7`) | Verified child-owner `USAGE` on parent schema and table/column `REFERENCES` before binding pending FKs (including during superuser `pg_restore`); insufficient privileges emit warning `1142` and keep the FK pending without aborting parent DDL (46 assertions). |
{.wide .expand}

## Final correctness fixes {#final-fixes}

Independent reviews of `f0dc476`, `aa25342`, `6f9c4f3`, and `a000baa` uncovered remaining wrong-row corruption paths, driver metadata issues, and a sorting regression. Four commits closed them without adding a new extension version beyond `1.9`:

| Fix & commit | Defect before fix | Behavior in `6a93e8f` / `v18.6.1` |
| --- | --- | --- |
| `F1` · Positive overflow above `UINT64_MAX` (`aa25342`) | Under `sql_mode=''` or `IGNORE`, values `> 18446744073709551615` clipped to `INT64_MAX` in `mys_lenient_int`, causing `ODKU` to update—or `REPLACE` to delete—an existing `INT64_MAX` row. | Every positive `BIGINT UNSIGNED` write `> 9223372036854775807` fails with `1264` in all modes and under `IGNORE` (`mys_lenient_int` in `src/mys_semantics.c`), rolling back statement and trigger side effects. |
| `F2` · `FIND_IN_SET` trailing spaces (`aa25342`) | `PAD SPACE` equality matched `'a'` against `'a '` inside `FIND_IN_SET`. | `mysql.find_in_set` in `sql/aux_mysql_fix_compat.sql` checks both collation equality and trailing-space byte count on `text` and `bigint` overloads without altering `FIELD`, `STRCMP`, `LIKE`, or `IN`. |
| `F3` / `F6` · Boolean `CONCAT` & `CHAR`/`VARCHAR` conditionals (`aa25342`) | Boolean `CONCAT` / `GROUP_CONCAT` emitted `'t'`/`'f'`; mixed `CHAR`/`VARCHAR` `IF()` and `IFNULL()` failed as ambiguous. | Boolean concatenation emits `'1'`/`'0'`; `bpchar`/`varchar`/`text` and `bool` `IF`/`IFNULL` overloads resolve unambiguously and are admitted by the generated-column policy. |
| `F9` · Result charset metadata (`aa25342`) | Character result fields advertised MySQL 8 charset `255` (`utf8mb4_0900_ai_ci`), breaking legacy MySQL 5.7 drivers. | Character fields advertise `45` (`utf8mb4_general_ci`) and binary fields `63` in text and prepared packets; verified with Connector/J `5.1.49`. |
| `F10` · Connection charset spellings (`aa25342`) | Quoted charsets, `SET NAMES ... COLLATE ...`, `SET NAMES DEFAULT`, `SET CHARACTER SET`, and `SET CHARSET` failed to parse. | All forms parse, update session variables consistently, and emit warning `1105` on charset/collation approximations (`set_connection_charset` in `src/mysm/systemVar.c`). |
| Compiler hygiene (`aa25342`) | Implicit declarations and int/pointer conversions broke strict modern C compilers. | Cleanly builds and passes `pg_regress` + `release_fixes.py` on Rocky Linux 10.2 with `GCC 14.3.1` treating implicit declarations and int-conversions as errors. |
| Boolean numeric/string writes (`6f9c4f3`) | In `sql_mode=''`, literal `TRUE` converted via `'true'` to `0` (`1265`), and implicit `text(bool)` stored `'true'`/`'false'` (or `'fals'`/`1406`) in character columns—corrupting `ODKU`/`REPLACE` target rows. | `bool_literal_value` converts `TRUE`/`FALSE` literals to `1`/`0`, and implicit MySQL boolean-to-character assignments convert via `int4(bool)` to `'1'`/`'0'` while preserving native PG `true::text = 'true'`. |
| Boolean casts to `DECIMAL`, floats & binary (`a000baa`) | Assigning predicates, `IF()`, or `TRUE`/`FALSE` to `DECIMAL`, `FLOAT`/`DOUBLE`, or `BINARY`/`VARBINARY`/`BLOB` failed with `1105` across 1,640 probed cases. | Adds six `ASSIGNMENT` casts from `pg_catalog.bool` (`numeric`, `float4`, `float8`, `bytea`, `mysql.binary_n`, `mysql.varbinary_n`) backed by immutable C helpers (`sql/aux_mysql_fix_compat.sql`). |
| Boolean character `DEFAULT`s & `LIKE` (`6a93e8f`) | `VARCHAR`/`CHAR DEFAULT TRUE/FALSE` saved `'true'`/`'false'` (or expanded after parse analysis), so omitted-column `ODKU`/`REPLACE` collided with an unrelated `'true'` unique key on `a000baa`. `CREATE TABLE ... LIKE` also dropped column defaults. | Normalizes boolean defaults in `CREATE`/`ALTER`, moves `mys_assign_bool_as_int` to `mys_planner` (`src/mys_utility.c`) **after** `DEFAULT` expansion (covering inherited `1.5` defaults without catalog migration), and enables `CREATE_TABLE_LIKE_DEFAULTS` with independent identity sequences. |
{.wide .expand}

### Why default expansion before key arbitration matters {#default-example}

On pre-acceptance branch tip `a000baa` (before `6a93e8f` and `v18.6.1`), omitting a `VARCHAR UNIQUE DEFAULT TRUE` column expanded the default to `'true'` instead of `'1'`, causing `ON DUPLICATE KEY UPDATE` to overwrite—or `REPLACE` to delete—an unrelated row whose key was the literal string `'true'`:

```sql
SET sql_mode='';
CREATE TABLE d (
    id INT PRIMARY KEY,
    k VARCHAR(20) UNIQUE DEFAULT TRUE,
    note VARCHAR(20)
);
INSERT INTO d VALUES (10, 'true', 'old');
INSERT INTO d(id, note) VALUES (20, 'new')
    ON DUPLICATE KEY UPDATE note='changed';
SELECT id, k, HEX(k), note FROM d ORDER BY id;
DROP TABLE d;
```

Candidate `6a93e8f` and MySQL 5.7.32 both keep `(10, 'true', '74727565', 'old')`, insert `(20, '1', '31', 'new')`, and report `1` affected row (`REPLACE INTO d(id, note) VALUES (20, 'new')` likewise keeps both rows). On `a000baa`, `ODKU` left only `(10, 'true', 'changed')` and `REPLACE` deleted `id = 10` leaving only `(20, 'true', 'new')`, reporting `2` affected rows without any warning. Genuine quoted string defaults (`DEFAULT 'true'`) and native PostgreSQL sessions retain `'true'`. Already stored `'true'` values from older runs are not rewritten automatically.

## Sorting and FIND_IN_SET performance correction {#performance}

Early `1.9` commits (`aa25342`) built and freed full two-byte weight arrays on every `general_strncoll` call and disabled abbreviated sort keys on `utf8mb4_general_ci` and `utf8mb4_bin`, causing a multi-fold `ORDER BY` / `GROUP BY` / `CREATE INDEX` slowdown relative to `v18.6` (`3,845 ms` vs `92 ms` on a 300k-row sort in development probes).

Commit `6f9c4f3` (`general_strncoll` and `general_strnxfrm_prefix` in `src/mys_prefix.c`) replaced temporary key allocation with streaming weight comparison (using a 128-entry ASCII lookup table from the same MySQL 5.7 weight table, stopping at the first differing weight) and added `strnxfrm_prefix` abbreviated sort keys padded with the space weight (`0x20`) so `memcmp` order matches `PAD SPACE` comparison, while keeping `strnxfrm` separate as the trimmed equality hash key.

Because `FIND_IN_SET` evaluates `item = $1` under the caller's collation, faster collation comparison also reduced its scan time. **`FIND_IN_SET` remains a SQL function** (`mysql.find_in_set` in `sql/aux_mysql_fix_compat.sql`), not a C implementation. In the final 2026-11-10 interleaved acceptance run (Rocky Linux 9.8 `aarch64`, GCC 11.5.0 `-O2` release build, 300,000 rows, `work_mem = 64MB`, JIT and parallel workers off, 1 warm-up + 10 interleaved samples):

- **`ORDER BY` (`utf8mb4_general_ci` 32-char MD5 strings, `EXPLAIN (ANALYZE, TIMING OFF)`)**: candidate `6a93e8f` median **`63.82 ms`** vs **`102.24 ms`** on released `v18.6` (~38% faster; `a000baa` median `59.97 ms`, overlapping sample ranges on the shared host).
- **`FIND_IN_SET` (8-item list aggregate, full client query time)**: candidate `6a93e8f` median **`0.677 s`** vs **`3.049 s`** on released `v18.6` (~78% faster), **still ~9× slower than MySQL 5.7.32 (`0.073 s` 3-sample median)** due to per-row SQL function and array-unnest overhead.

These measurements verify that the `1.9` sorting regression is closed on the acceptance fixture; they are not general hardware or customer-workload benchmarks. See [acceptance performance details](/openhalo/18/acceptance/#performance).

## Deliberate deferrals and narrow 1.9 limits {#deferred}

By explicit release scope decision, `aux_mysql 1.9` defers native `ENUM`/`SET`, negative or `>= 24h` `TIME` durations, MySQL `TIMESTAMP` cross-timezone conversion, full unsigned 64-bit (`> INT64_MAX`) storage and expressions, boolean arithmetic and `AVG`/`MIN`/`MAX`/`STD`/`BIT_*` aggregates, broader mixed-type `IF`/`IFNULL`/`COALESCE`/`GREATEST`, multi-argument `GROUP_CONCAT`, `DELETE target FROM ... JOIN ...` and multi-target DML, bare-literal/variable collation propagation, MySQL stored procedures/triggers/events, `JSON_*` / spatial functions, and MySQL binlog/GTID replication.

Three narrow behavioral differences are also explicitly retained in `1.9`: partial `PAD_CHAR_TO_FULL_LENGTH` trimming in functions such as `LENGTH()`, rejection of extreme exponents (`1e1000000` / `1e-1000000`) and negative `SIGNED` overflow in binary numeric `CAST`, and character-position return values for empty-needle `LOCATE('', multibyte_str, pos)`. Every item and its migration workaround is detailed in [compatibility boundaries](/openhalo/18/compatibility/).
