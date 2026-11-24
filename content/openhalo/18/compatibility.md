---
type: docs
upstream_link: ""
search_keywords: ["BIGINT UNSIGNED", "INT64_MAX", "NUL", "ENUM", "SET", "REPEATABLE READ", "FIND_IN_SET", "unicode_ci", "collation_connection", "COALESCE", "PAD_CHAR_TO_FULL_LENGTH", "ANSI_QUOTES", "wait_timeout", "TIMESTAMP", "3819", "sql_mode"]
title: Compatibility boundaries
description: Authoritative reference for exact MySQL 5.7 behavior, deliberate mappings, accepted-only settings, unsupported features, native PostgreSQL effects, and diagnostic codes in aux_mysql 1.9.
weight: 30
---

This page is part of the **`aux_mysql 1.9` compatibility contract** (accepted at `6a93e8f` and published in source tag `v18.6.1`). The [conditional GO source verdict](/openhalo/18/acceptance/) depends on publishing these boundaries accurately. Passing regression suites does not establish drop-in MySQL 5.7 equivalence or exempt an application from schema, SQL, transaction, and driver validation.

## Data representation and storage limits {#representation}

| Type / area | Actual OpenHalo 18 boundary | Migration and application impact |
| --- | --- | --- |
| `BIGINT UNSIGNED` | Domain `mysql."bigint unsigned"` over signed `int8`: stores **`0..9223372036854775807` (`INT64_MAX`)**. Every positive write above `INT64_MAX`—both `INT64_MAX + 1 .. UINT64_MAX` and `> UINT64_MAX`, across literals, strings, expressions, `INSERT SELECT`, `ODKU`, `REPLACE`, and binary `COM_STMT_EXECUTE` unsigned parameters—**fails with error `1264` in every `sql_mode` and under `IGNORE`**, rolling back statement side effects before unique-key arbitration. Non-strict (and `IGNORE`) negative writes clip to `0` with warning `1264`; strict negative writes without `IGNORE` fail with domain check error **`3819`** instead of MySQL's `1264`. | Audit 64-bit unsigned IDs, hash keys, and `UUID_SHORT()` consumers. Values in the upper half of `uint64` cannot be stored, and never saturate to `UINT64_MAX` or silently collapse onto an existing `INT64_MAX` unique key. `CAST(expr AS UNSIGNED)` lowers to signed `int8` (`CAST(-1 AS UNSIGNED)` returns `-1`, not `18446744073709551615`), and hex arithmetic above `INT64_MAX` errors. |
| `CHAR` / `VARCHAR` / `TEXT` `NUL` | Backed by PostgreSQL character types (`bpchar`, `varchar`, `text`). Any `NUL` byte (`0x00`) **fails with error `1366` in every `sql_mode`, including `INSERT IGNORE`**. `TINYTEXT`, `TEXT`, `MEDIUMTEXT`, and `LONGTEXT` all display as `text` in `SHOW CREATE TABLE` and `information_schema.COLUMNS`. | Bytes are never stripped or replaced to make a write succeed. Migrate columns that legitimately hold `0x00` or arbitrary bytes to `BINARY`, `VARBINARY`, or `BLOB`, reviewing length limits, comparisons, and indexes. |
| Binary → character conversions | Assigning or `CAST`ing `BINARY`, `VARBINARY`, or `BLOB` to character types validates UTF-8 across the entire payload. Any `0x00`—**including `BINARY(n)` trailing zero-byte padding**—or invalid UTF-8 raises `1366` even under `IGNORE`. | Do not use `CAST(binary_col AS CHAR)` on zero-padded `BINARY(n)` values or non-UTF8 payloads; trim `0x00` bytes explicitly on the binary side or keep binary types. |
| Legacy `1.5` `BINARY` / `VARBINARY` | Pre-`1.8` `mysql.binary` and `mysql.varbinary` are `bytea` domains that discarded declared lengths; `1.5 → 1.9` upgrade preserves existing column types and stored bytes. | Recover original `(n)` lengths from MySQL DDL and run reviewed `ALTER TABLE ... MODIFY` to adopt `mysql.binary_n` / `mysql.varbinary_n` padding and length enforcement. |
| `DECIMAL` metadata | Bare `DECIMAL` is `DECIMAL(10,0)`. Expressions, views, or PostgreSQL-created `numeric` columns without a MySQL `(p,s)` typmod report `decimal(65,30)` with warning `1105`. | Replaying `decimal(65,30)` preserves at most `35` integer and `30` fractional digits; audit wider unbounded PostgreSQL `numeric` values before logical dump/replay. |
| `FLOAT` / `DOUBLE` / `REAL` | New unqualified `FLOAT` / `FLOAT(0..24)` uses `float4` (wire type `FLOAT`); `DOUBLE`, `REAL`, and `FLOAT(25..53)` use `float8` (`REAL_AS_FLOAT` does not switch `REAL` to `float4`). Deprecated `FLOAT(M,D)` / `DOUBLE(M,D)` syntax does not enforce `(M,D)` rounding. Scientific literals like `1.5e0` parse as `numeric`, not `DOUBLE`. | Existing `float8` columns are not narrowed on upgrade; declare `DOUBLE` explicitly where 64-bit IEEE precision is required. |
| `DATETIME` & `TIMESTAMP` | Both `DATETIME[(0..6)]` and bare MySQL `TIMESTAMP[(0..6)]` map to PostgreSQL `timestamp without time zone` (default precision `0`; `SHOW CREATE TABLE` may spell `timestamp(n)`). Zero dates (`0000-00-00`) are rejected. | Bare `TIMESTAMP` columns **do not convert stored values between UTC and session `time_zone`** on read/write (unlike MySQL `TIMESTAMP`), and the first `TIMESTAMP NOT NULL` column does not receive implicit `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` unless declared explicitly. |
| `ENUM` & `SET` | Unsupported (`error 1091`: `type "enum"` / `"set" does not exist`). | Convert explicitly to PostgreSQL `CHECK`-constrained `text`, native PG `ENUM`, or integer bitmasks, and adapt application ordinal/bitmask queries; see [migration examples](/openhalo/18/migration/#mysql). |
| `TIME` durations | Mapped to clock-of-day `time without time zone`: negative values (such as `'-01:00:00'`) and durations `>= 24:00:00` fail. | Use PostgreSQL `interval` or integer seconds/microseconds for elapsed-time columns and adapt client decoding. |
| `BIT`, variables & temporal writes | `BIT(n)` result fields return text `'1'` rather than raw byte `0x01` in probed cases; `@user_var` numeric typing differs; boolean or integer expressions written to `DATE`/`TIME`/`DATETIME`/`TIMESTAMP`, `YEAR`, or `JSON` fail; integer expressions assigned directly to `BINARY`/`VARBINARY`/`BLOB` fail. | Test wire-level driver decoding for `BIT` columns, and format temporal/JSON/binary inputs explicitly rather than relying on implicit integer or boolean coercions. |
{.wide .expand}

```sql
CREATE TABLE u64_demo (id INT PRIMARY KEY, u BIGINT UNSIGNED UNIQUE);
INSERT INTO u64_demo VALUES (1, 9223372036854775807);

-- Fails with error 1264 even under IGNORE; row (1, 9223372036854775807) is untouched:
-- INSERT IGNORE INTO u64_demo VALUES (2, 18446744073709551615);
-- REPLACE INTO u64_demo VALUES (2, 18446744073709551616);

SET sql_mode = '';
INSERT INTO u64_demo VALUES (2, -1);   -- Clips to 0 with warning 1264
SET sql_mode = 'STRICT_TRANS_TABLES';
-- INSERT INTO u64_demo VALUES (3, -1); -- Fails with domain check error 3819
```

## Collations, character sets, and literal propagation {#collations}

| Requested setting or construct | Actual behavior in OpenHalo 18 |
| --- | --- |
| `utf8_general_ci`, `utf8mb4_general_ci`, `utf8_bin`, `utf8mb4_bin` | **Exact dedicated implementations** in schema `mysql`: MySQL 5.7 BMP case/accent weights (`> U+FFFF` mapped to weight `0xFFFD`, matching MySQL 5.7 `utf8mb4_general_ci`) or UTF-8 codepoint order, both with `PAD SPACE`. |
| Other `*_ci` collation names (e.g. `utf8mb4_unicode_ci`, `utf8mb4_0900_ai_ci`, `latin1_swedish_ci`) | Mapped to `utf8mb4_general_ci` (or `utf8_general_ci` under `SET NAMES utf8`) with **warning `1105`** in DDL, expression `COLLATE`, views, `CREATE TABLE AS`, and `SET NAMES ... COLLATE`. |
| Other non-`_ci` collation names (e.g. `latin2_czech_cs`, `ascii_bin`) | Mapped to `utf8mb4_bin` (or `utf8_bin`) with **warning `1105`**. |
| `SHOW CREATE TABLE` on mapped collations | Displays the effective rule (`utf8mb4_general_ci` / `utf8mb4_bin`) or OpenHalo alias (`case_insensitive` / `case_sensitive`), never pretending the unimplemented locale is active. |
| Non-UTF8 charsets (`latin1`, `gbk`, `ucs2`, `utf16`, `utf32`) | Database and wire representation remain UTF-8; `SET NAMES` / `CONVERT(... USING ...)` maps to `utf8mb4` with warning `1105` rather than performing single-byte or UTF-16/32 transcoding. Explicit `CHARACTER SET ascii` in DDL hits a parser keyword gap (`1064`). |
| `SET NAMES ... COLLATE ...` vs `SET collation_connection = ...` | `SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci'` warns `1105` and sets `@@collation_connection = 'utf8mb4_general_ci'`. Direct `SET collation_connection = 'utf8mb4_unicode_ci'` emits **no warning** and echoes `'utf8mb4_unicode_ci'` in `SELECT @@collation_connection`, without implementing `unicode_ci`. |
| Bare string literals & `@vars` | **Collation propagation is incomplete.** Two bare literals use the PostgreSQL database collation (`C` / UTF-8 byte order) even after `SET NAMES utf8mb4 COLLATE utf8mb4_general_ci`. Column references and explicit `COLLATE` clauses use the MySQL collation. |
| Legacy ICU collations (`case_insensitive`, `case_sensitive`, `ignore_accents`) | Retained from earlier versions so existing tables and indexes keep working across upgrades; never rewritten in place by `ALTER EXTENSION`. |
{.wide .expand}

```sql
SET NAMES utf8mb4 COLLATE utf8mb4_general_ci;

-- Bare literals compare case-sensitively (returns 0, -1, 0; MySQL 5.7 returns 1, 0, 1):
SELECT 'A' = 'a', STRCMP('A', 'a'), FIND_IN_SET('A', 'a,b');

-- Column expressions and explicit COLLATE clauses use utf8mb4_general_ci (returns 1, 1):
SELECT ('A' COLLATE utf8mb4_general_ci) = 'a',
       FIND_IN_SET('A' COLLATE utf8mb4_general_ci, 'a,b');
```

In the exhaustive `collation_all` verification (`221` non-binary MySQL 5.7 collation names × `3` character column types = `9,945` assertions), every query matched the declared `general_ci`/`bin` mapping contract without errors, while recording **246 expected differences from the requested MySQL locale**: `3` column-type cases on `latin2_czech_cs` (`LOCATE('L', s)` because `_cs` maps to `bin` rather than Czech case weights), `165` cases across `ucs2_*`/`utf16_*`/`utf16le_*`, and `78` cases across `utf32_*` (`LOCATE('', s, 2)` returning UTF-8 offset `2` instead of MySQL's 2-byte/4-byte code-unit offsets `3`/`5`). Before migrating tables that rely on `unicode_ci` or locale-specific weights, check for new `UNIQUE` key collisions under `utf8mb4_general_ci` / `utf8mb4_bin`.

## Transactions, isolation mapping, and affected rows {#transactions}

| MySQL transaction / DML construct | Effective OpenHalo 18 behavior | Consequence for applications |
| --- | --- | --- |
| `READ UNCOMMITTED` / `READ COMMITTED` | PostgreSQL `READ COMMITTED`. | Standard read-committed statement snapshots; dirty reads never occur. |
| **Read-write `REPEATABLE READ`** (default) | **PostgreSQL `READ COMMITTED`** (deliberate product choice). | Avoids PostgreSQL `40001` serialization aborts on concurrent InnoDB-style `UPDATE`/`DELETE` workloads, **but plain `SELECT`s in the same read-write transaction see newly committed rows from other sessions**. |
| **Read-only `REPEATABLE READ`** (`START TRANSACTION READ ONLY` / `SET TRANSACTION READ ONLY`) | **PostgreSQL `REPEATABLE READ`** (stable snapshot) + read-only guard (`1792` on writes). | Use this mode—or `START TRANSACTION WITH CONSISTENT SNAPSHOT`—whenever multi-query reports require a repeatable snapshot. |
| `START TRANSACTION WITH CONSISTENT SNAPSHOT` | **PostgreSQL `REPEATABLE READ`** snapshot acquired immediately **when the effective MySQL isolation level is `REPEATABLE READ` (default)**; under `READ COMMITTED`, `READ UNCOMMITTED`, or `SERIALIZABLE`, emits **warning `138`** and ignores `WITH CONSISTENT SNAPSHOT` (matching InnoDB). | Keep session/next isolation at `REPEATABLE READ` when using `WITH CONSISTENT SNAPSHOT` for consistent point-in-time reporting. |
| `SERIALIZABLE` | PostgreSQL SSI `SERIALIZABLE` (falls back to `REPEATABLE READ` on a hot standby); conflicts report MySQL deadlock code **`1213` (`SQLSTATE 40001`)**. | Application retry loops handling `1213` / `40001` work as expected; lock timing differs from InnoDB shared locking reads. |
| Delete + reinsert contention | PostgreSQL MVCC tuple visibility + btree uniqueness rather than InnoDB gap/next-key locks. | Under concurrent `DELETE` + `INSERT` of the same key, a waiting `DELETE` can match `0` rows after the other session commits its replacement, causing the follower's `INSERT` to hit `1062`. |
| Statement-level rollback (`mysql.statement_rollback = on`) | Wraps each statement inside an explicit transaction in a hidden savepoint (`subxid`). | Transactions with **more than 64 writing statements** overflow the per-backend `PGPROC` `subxid` cache and increase snapshot overhead. Commit in smaller batches or evaluate `mysql.statement_rollback = off` (which aborts the whole transaction on error, PostgreSQL-style). |
| `INSERT ... ON DUPLICATE KEY UPDATE` row count | `1` per inserted row; `2` per conflicting row whose stored values changed; `0` per unchanged conflict (`1` with `CLIENT_FOUND_ROWS`). | Matches MySQL 5.7 affected-row semantics. |
| `REPLACE INTO` row count | `1` per non-conflicting insert—or when conflicting on a table with a single unique index, no row-level `DELETE` triggers (including incoming FK `ON DELETE` triggers), and identical column values; `1 + deleted_rows` whenever conflicting row(s) are physically deleted and re-inserted across unique keys. | Matches MySQL 5.7 InnoDB affected-row counting. |
| **Plain `UPDATE` row count** | Always returns **matched rows**, even when `CLIENT_FOUND_ROWS` is off and column values are unchanged. | Optimistic-locking or ORM checks that expect `UPDATE t SET v = 1` on a row already holding `1` to return `0` affected rows will observe `1` instead. |
{.wide .expand}

```sql
CREATE TABLE counters (id INT PRIMARY KEY, v INT NOT NULL);
INSERT INTO counters VALUES (1, 10);

-- Plain UPDATE returns 1 (matched) even though v is already 10 (MySQL without CLIENT_FOUND_ROWS returns 0):
UPDATE counters SET v = 10 WHERE id = 1;

-- ODKU distinguishes unchanged (0 without CLIENT_FOUND_ROWS) vs changed (2):
INSERT INTO counters VALUES (1, 10) ON DUPLICATE KEY UPDATE v = VALUES(v); -- 0 affected
INSERT INTO counters VALUES (1, 11) ON DUPLICATE KEY UPDATE v = VALUES(v); -- 2 affected
```

## Accepted settings and syntax vs implemented behavior {#accepted-vs-implemented}

Do not infer behavioral support merely because a `SET` statement succeeds, `SELECT @@var` echoes a value, or a DDL/DML clause parses without error:

| Setting or syntax | Accepted / echoed? | Actual runtime behavior |
| --- | --- | --- |
| `USE` / `IGNORE` / `FORCE` `INDEX` or `KEY` | Parsed in `SELECT`, `UPDATE`, `DELETE` | **Ignored.** Planner chooses access paths using PostgreSQL statistics. |
| `auto_increment_increment`, `auto_increment_offset` | Accepted & echoed in `@@variables` / `SHOW VARIABLES` | **Not implemented** when set to non-default values; sequences always allocate with `INCREMENT 1` (`1, 2, 3, ...`). |
| `wait_timeout`, `interactive_timeout`, `innodb_lock_wait_timeout` | Accepted & echoed | **Not wired** to PostgreSQL `idle_session_timeout` or `lock_timeout`; idle MySQL connections are not disconnected by `wait_timeout`. Configure PostgreSQL timeouts in `postgresql.conf` / `ALTER ROLE` instead. |
| `sql_mode`: `STRICT_TRANS_TABLES`, `STRICT_ALL_TABLES`, `ERROR_FOR_DIVISION_BY_ZERO`, `NO_AUTO_VALUE_ON_ZERO`, `NO_BACKSLASH_ESCAPES`, `PAD_CHAR_TO_FULL_LENGTH`, `NO_ZERO_DATE`, `NO_ZERO_IN_DATE`, `ALLOW_INVALID_DATES` | Accepted & echoed | **Implemented** on the covered conversion, scanner, `AUTO_INCREMENT`, `CHAR`, and date-operator paths (with documented narrow exceptions below). |
| `sql_mode`: `ANSI_QUOTES`, `PIPES_AS_CONCAT`, `REAL_AS_FLOAT`, `IGNORE_SPACE`, `NO_UNSIGNED_SUBTRACTION`, `HIGH_NOT_PRECEDENCE` | Accepted & echoed | **Not implemented** in lexer/grammar/types: `"..."` remains a string literal under `ANSI_QUOTES`, and `REAL` remains `float8` under `REAL_AS_FLOAT`. |
| `sql_mode`: `ONLY_FULL_GROUP_BY` | Echoed when set (absent from initial `@@sql_mode` string) | **PostgreSQL grouping rules always apply**: clearing `ONLY_FULL_GROUP_BY` (`SET sql_mode=''`) does **not** allow ungrouped non-PK `SELECT` columns. |
| `SET collation_connection = '...'` | Accepted & echoed verbatim | **Does not validate, map, or propagate** to literal comparisons; use `SET NAMES ... COLLATE ...` to see the effective mapped rule and `1105` warning. |
| `ENGINE=InnoDB` / `MyISAM` vs `ENGINE=<pg_am>` | Accepted | `InnoDB`/`MyISAM` fall back to PostgreSQL default `heap`; installed PG table AMs (e.g. `orioledb`) are selected by name; `ENCRYPTION='Y'` requires `pg_tde` (`tde_heap`) or errors. |
| `CHECK (...)` constraints in `CREATE TABLE` | Accepted & **enforced** | PostgreSQL enforces `CHECK` constraints (whereas MySQL 5.7 parsed and ignored `CHECK`). |
{.wide .expand}

## Expressions, functions, and unsupported SQL forms {#expressions}

| Area | Current boundary |
| --- | --- |
| Boolean expressions & aggregates | Boolean writes (`1`/`0`, `'1'`/`'0'`), `CONCAT`/`GROUP_CONCAT`, `IF(cond, TRUE, FALSE)`, and **`SUM(bool)`** (returning `bigint`) work. **Boolean arithmetic** (`(1>0)+0`, `(status='paid')*amount`), **other boolean aggregates** (`AVG`, `MIN`, `MAX`, `STD`, `BIT_OR`, `BIT_AND`, `BIT_XOR` -> `1305`), numeric functions on booleans (`ROUND`, `ABS`), and mixed-type `COALESCE` / `GREATEST` fail. Wrap predicates in `IF(cond, 1, 0)` or `CASE WHEN cond THEN 1 ELSE 0 END` for arithmetic and `AVG`/`MIN`/`MAX`. |
| Mixed-type conditionals | `CHAR` / `VARCHAR` / `TEXT` combinations in `IF()` and `IFNULL()` work. Cross-family combinations such as `COALESCE(int_col, varchar_col)` (`1105`), `IF(cond, int_col, varchar_col)` (`1305`), `COALESCE(1, 'a')` (`1366`), and `IFNULL(varbinary_col, char_col)` (`1305`) fail without explicit `CAST(... AS CHAR)`. |
| `GROUP_CONCAT` | Single-argument `GROUP_CONCAT([DISTINCT] expr [ORDER BY ...] [SEPARATOR ...])` works on text, booleans, and raw binary columns. Multi-argument `GROUP_CONCAT(a, b)` is incomplete—rewrite as `GROUP_CONCAT(CONCAT(a, b))`. |
| `FIND_IN_SET` | `text` and `bigint` overloads enforce collation and trailing-space equality, but `DECIMAL` arguments (`FIND_IN_SET(2.0, '1,2,3')`) fail with `1305`. Executed as an SQL function (~9× slower than MySQL 5.7 on 300k-row scans). |
| Missing MySQL functions & `LOAD` / `SHOW` | MySQL `JSON_*` (`JSON_EXTRACT`, `JSON_SET`, etc.), spatial functions (`POINT`, `ST_Distance`), full-text `MATCH ... AGAINST`, `SHA1`, `CRC32`, `TO_BASE64`, `QUOTE`, `SOUNDEX`, `ORD`, `CHAR()`, `LOAD DATA INFILE`, `SELECT ... INTO OUTFILE`, and `SHOW DATABASES LIKE ...` are unimplemented. |
| Multi-table `DELETE` & multi-target DML | Single-target `DELETE FROM target USING ...` and `UPDATE ... JOIN ...` work. **`DELETE target FROM target JOIN ...`**, comma-join `DELETE target FROM a, b ...`, `LEFT JOIN` orphan-delete spellings, and **multi-target `UPDATE` / `DELETE`** fail with syntax error `1064`. |
| Multi-statement raw syntax errors | Inside an already-open explicit transaction block with `mysql.statement_rollback = on`, syntax errors are deferred to a savepoint-guarded marker so earlier statements in the transaction survive. Outside an open transaction block (for example, an `autocommit=1` packet `INSERT ...; BAD SQL;`), raw parsing validates the entire `COM_QUERY` packet upfront and rejects it before statement 1 runs. |
| Stored programs, triggers & events | Native MySQL `CREATE PROCEDURE` / `FUNCTION` (`BEGIN ... END`), MySQL trigger bodies, and `CREATE EVENT` are unsupported. PostgreSQL `BEGIN ATOMIC` / `DO ... LANGUAGE` fixtures used in upgrade tests are PostgreSQL syntax, not MySQL routine compatibility. |
| Protocol & session control | No MySQL Unix domain socket, `COM_CHANGE_USER`, MySQL `KILL [QUERY]`, `COM_STMT_FETCH` cursors (`1421`), or `mysql_native_password` challenge-response; port `3306` accepts only `scram-sha-256`, `md5`, `password`, `trust`, and `reject` `pg_hba.conf` methods (`1045` on others), and caps session prepared statements at `16,382` (`1461`). |
{.wide .expand}

Three narrowly scoped behavioral differences are explicitly accepted in `1.9`:

- **`PAD_CHAR_TO_FULL_LENGTH` on unoverloaded string functions**: stored bytes and WP3-covered functions (`CONCAT`, `CAST`, `HEX`, `GROUP_CONCAT`, etc.) preserve full `CHAR(n)` width, but functions without dedicated `bpchar` overloads (such as `LENGTH(char_col)`) still receive PostgreSQL's space-trimmed `text` value.
- **Extreme binary numeric `CAST` inputs**: `CAST(binary_val AS SIGNED)` / `DECIMAL` can reject extreme exponents such as `1e1000000` / `1e-1000000` and negative `SIGNED` overflow rather than matching MySQL's exact clipping edge cases; malformed binary `DECIMAL` consistently emits warning `1292` (whereas MySQL 5.7 varies between no warning, `1292`, and `1366`).
- **Empty-needle `LOCATE` on multibyte UTF-8**: `LOCATE('', multibyte_string, pos)` returns a character position rather than MySQL's byte/code-unit offset at boundary positions.

## Indexes, generated columns, and foreign keys {#objects}

- **`mysql_prefix` index scan limits**: keys with explicit `(col(n))` prefixes or wide/unbounded columns (`TEXT`, `BLOB`, wide `VARCHAR`) use `mysql_prefix`, which always rechecks heap tuples and disables `Index Only Scan` and `ORDER BY` sort scans. High-skew workloads where many rows share the same prefix incur extra heap recheck work during lookups and unique checks. Short unprefixed keys keep native PostgreSQL `btree` scans.
- **Key-name length and case**: physical PostgreSQL index names reserve `9` bytes (`$<8-hex>`) out of `63` bytes (`NAMEDATALEN - 1`), truncating logical MySQL key names above **`54` bytes** (~18 three-byte UTF-8 CJK characters) and folding key-name case in ASCII only.
- **Materialized `VIRTUAL` generated columns**: `VIRTUAL` columns are stored physically on disk and evaluated under the **writing session's** `sql_mode` / `IGNORE` settings; changing a later reader's `sql_mode` never recomputes stored rows. Nondeterministic functions, session variables, arbitrary UDFs, and implicit text-to-temporal conversions in generated `DATE_FORMAT` (or `CAST(CONCAT(...) AS DATE)`) fail validation with `3102`. `VIRTUAL` primary keys and generated columns referencing `AUTO_INCREMENT` are OpenHalo extensions rejected by MySQL 5.7 on dump replay.
- **Foreign-key parent uniqueness and PostgreSQL ACLs**: foreign keys always require a `PRIMARY KEY` or `UNIQUE` constraint on the referenced parent columns with compatible types; referencing a non-unique parent index is rejected even when `FOREIGN_KEY_CHECKS=0`. Parent `TRUNCATE` does not cascade. Binding a pending missing-parent FK checks the child table owner's current `USAGE` on the parent schema and `REFERENCES` on the parent table/columns (even during superuser `pg_restore`), emitting warning `1142` and leaving the FK pending when privileges are absent—a deliberate PostgreSQL security boundary where MySQL 5.7 does not check `REFERENCES`.

## Native PostgreSQL coexistence, ABI, and historical data {#coexistence}

- **Database-wide boolean assignment casts in `mysql.database`**: `aux_mysql 1.9` installs six database-level `ASSIGNMENT` casts from `pg_catalog.bool` (`numeric`, `float4`, `float8`, `bytea`, `mysql.binary_n`, `mysql.varbinary_n`). In the database where `aux_mysql` is installed (`postgres` by default), **native PostgreSQL sessions (`psql` on `5432`) also observe `SELECT true::numeric` -> `1` and `SELECT true::bytea` -> `\x31`**, whereas `SELECT true::text` stays `'true'` and native PG character column defaults (`DEFAULT true`) keep `'true'`. Run unrelated PostgreSQL applications in their own separate PostgreSQL databases where `aux_mysql` is not installed.
- **Kernel and third-party extension ABI**: Although `PG_VERSION` remains `18.6` (`PG_VERSION_NUM = 180006`), OpenHalo 18 modifies protocol, parse, and plan node structures (`ClientSocket`, `OnConflictClause`, `ModifyTable`, `pg_locale` callbacks), so `v18.6`'s earlier claim that unmodified stock PGDG C extension binaries load directly no longer holds in `v18.6.1` (`aux_mysql 1.9`). Always compile the kernel and `aux_mysql` together, and rebuild and test any third-party PostgreSQL C extension (`pg_tde`, `orioledb`, `PostGIS`, `pgvector`, etc.) against the exact OpenHalo 18 headers; cross-protocol extension usage is untested.
- **No physical PG14 upgrade and no automatic repair of historical data**: `pg_upgrade` from OpenHalo PG14 (`1.0.14.x`) is blocked by design. Upgrading `v18.6` (`aux_mysql 1.5`) to `1.9` updates extension catalogs cleanly, **but never guesses or repairs** discarded `1.5` `BINARY`/`VARBINARY` lengths, discarded prefix lengths, legacy ICU indexes, lost generated expressions, unsafe `IMMUTABLE` generator wrappers, `NOT ENFORCED` FKs, orphan rows, or historical `'true'`/`'false'`/`0` values. Follow [Migration and upgrade](/openhalo/18/migration/#audit).

## Operational and diagnostic boundaries {#operations}

- `SHOW STATUS` and `performance_schema` tables are largely unpopulated stubs; monitor production instances through PostgreSQL catalog views (`pg_stat_activity`, `pg_stat_statements`, `pg_locks`, `pg_stat_ssl`).
- `SHOW WARNINGS` and `SHOW ERRORS` retain at most **64** diagnostics for the current statement in session memory, and MySQL 5.7 `sql_mode` deprecation warnings (`3090` / `3135`) and exact English error prose are not reproduced word for word.
- Session locks (`GET_LOCK`) allocate entries in PostgreSQL's shared lock table (`max_locks_per_transaction`).
- MySQL binlog / GTID replication is unavailable (`@@gtid_mode = 'OFF'`, `@@gtid_executed = ''`, `@@gtid_purged = ''`). PostgreSQL WAL LSNs are not MySQL GTIDs. Native `pg_dump` backups must preserve extension-managed triggers and `--no-security-labels` must **not** be passed when table default collations matter.

## Diagnostic and error code reference {#diagnostics}

| Code | Meaning in OpenHalo 18 (`aux_mysql 1.9`) |
| --- | --- |
| `138` | `WITH CONSISTENT SNAPSHOT` warning when ignored outside `REPEATABLE READ` isolation. |
| `1045` (`28000`) | MySQL authentication failure, `reject` HBA rule, `md5` role secret under a `scram-sha-256` HBA rule, or unsupported `pg_hba.conf` method on port `3306` (`peer`, `ident`, `cert`, `gss`, `ldap`, `pam`, etc.). |
| `1047` (`08S01`) | Unsupported MySQL wire command (such as `COM_CHANGE_USER`). |
| `1061` / `1062` | Duplicate key name in table / duplicate entry on `PRIMARY` or `UNIQUE` key. |
| `1064` | SQL syntax error (including unsupported `DELETE target FROM ... JOIN ...` or `CHARACTER SET ascii`). |
| `1091` | Unsupported type lookup (such as `ENUM` or `SET`). |
| `1105` | Documented charset/collation or `decimal(65,30)` approximation warning—or general PostgreSQL error without a dedicated MySQL code (such as `COALESCE` type mismatch); always inspect the message text. |
| `1142` | Insufficient `USAGE` / `REFERENCES` privilege when binding a pending foreign key (emitted as warning during parent DDL/restore). |
| `1180` (`40000`) | `COMMIT` issued on a transaction that PostgreSQL already aborted due to an earlier error. |
| `1213` (`40001`) | `SERIALIZABLE` serialization failure or deadlock exposed for driver retry. |
| `1264` | Numeric value out of range; warning when clipped in non-strict mode, **always an error for `BIGINT UNSIGNED > INT64_MAX`** (including `IGNORE`). |
| `1265` / `1292` | Data truncated / malformed numeric prefix warning (including binary `DECIMAL` casts and `TEXT + 0`). |
| `1290` / `1792` | Write rejected by `GLOBAL read_only` or `super_read_only` / write rejected by read-only transaction. |
| `1305` | Function or operator overload does not exist (such as `AVG(bool)`, `(1>0)+0`, or `FIND_IN_SET(decimal, text)`). |
| `1365` | Division by zero (warning returning `NULL`, or error on strict write with `ERROR_FOR_DIVISION_BY_ZERO`). |
| `1366` | Invalid character value or conversion—**always raised on `NUL` (`0x00`) in character types and bad UTF-8 / `BINARY(n)` zero-padding casts to text**, even under `IGNORE`. |
| `1406` / `1411` | Data or `BIT(n)` value too long for column / invalid hex digit in `UNHEX()` (warning returning `NULL`). |
| `1421` / `1461` | `COM_STMT_FETCH` rejected because server-side prepared cursors are not opened / session prepared statement limit (`16,382`) exceeded. |
| `1451` / `1452` | Foreign-key parent delete/update blocked / child insert/update missing parent key. |
| `3057` / `3058` | `GET_LOCK` name longer than 64 characters / user-level lock wait-cycle deadlock. |
| `3102` / `3105` | Disallowed generated-column expression / explicit non-`DEFAULT` write to a generated column. |
| `3819` | PostgreSQL domain `CHECK` violation (such as strict-mode negative write into an `UNSIGNED` column without `IGNORE`). |
{.wide .expand}

Treat `SHOW WARNINGS` output as part of every compatibility check: acceptance tests compared stored bytes, error codes, and warning codes together rather than treating an `OK` packet as proof of exact behavior.
