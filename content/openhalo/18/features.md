---
type: docs
upstream_link: ""
search_keywords: ["AUTO_INCREMENT", "COM_STMT_PREPARE", "COM_STMT_FETCH", "WITH CONSISTENT SNAPSHOT", "FOREIGN_KEY_CHECKS", "GET_LOCK", "ODKU", "ON DUPLICATE KEY UPDATE", "REPLACE", "HEX", "UNHEX", "GROUP_CONCAT", "SHOW CREATE TABLE", "mysql.sum", "prefix index", "VIRTUAL", "STORED", "utf8mb4_general_ci"]
title: Functionality
description: Supported protocol, SQL, DML, transaction, data type, index, generated-column, and operational capabilities in aux_mysql 1.9, with examples and migration impact.
weight: 10
---

This reference describes what OpenHalo 18 implements in **`aux_mysql 1.9`** (source tag [`v18.6.1` / accepted commit `6a93e8f`](/openhalo/18/#versions)). Every section states the **support level**, **implemented behavior**, **verified SQL examples**, and **boundary / migration impact**; see [compatibility boundaries](/openhalo/18/compatibility/) for the complete edge-case and diagnostic reference.

## Protocol, authentication, and prepared statements {#protocol}

| Capability | Support level | Implemented behavior |
| --- | --- | --- |
| Dual-protocol listener | Implemented | One PostgreSQL 18.6 postmaster serves PostgreSQL on `5432` and MySQL TCP connections on `mysql.port` (`3306`). MySQL databases map to schemas inside `mysql.database` (`postgres`); `USE db` and `COM_INIT_DB` switch `search_path`. |
| Authentication & TLS | Implemented | `caching_sha2_password` (MySQL 8 default: shared-memory stage2 fast-auth cache, TLS or auto-generated RSA-OAEP full auth) and optional `mysql_clear_password` (delivered via an `AuthSwitchRequest` `0xfe` after the initial greeting), verified against PostgreSQL SCRAM/MD5 role passwords and `pg_hba.conf` (`scram-sha-256`, `md5`, `password`, `trust`, and `reject` supported on port `3306`; `mysql_native_password` challenge-response is unavailable because PG verifiers do not store `SHA1(SHA1(password))`). `ALTER ROLE ... PASSWORD` automatically invalidates stale cache entries; `SELECT mysql.flush_auth_cache()` clears the cache explicitly. TLS uses PostgreSQL `ssl_*`, `hostssl`, and `pg_stat_ssl`. |
| Connection initialization | Implemented (mapped) | Quoted or unquoted `SET NAMES charset [COLLATE collation]`, `SET NAMES DEFAULT`, `SET CHARACTER SET`, and `SET CHARSET` (including `DEFAULT`). Updates `character_set_client`, `character_set_results`, `character_set_connection`, and `collation_connection` (`CHARACTER SET` derives connection defaults from database variables). Non-UTF8 charsets and non-exact collations map to UTF-8 and `utf8mb4_general_ci` / `utf8mb4_bin` (or `utf8_*`) with warning `1105`. |
| Wire packet & result metadata | Implemented | Enforces reloadable `mysql.max_allowed_packet` (`64 MiB` default) on incoming packets and accumulated `COM_STMT_SEND_LONG_DATA` payloads. Character result columns advertise MySQL 5.7 charset `45` (`utf8mb4_general_ci`); binary results advertise `63` (`binary`), in both text and binary prepared protocols. Handshake announces `45` when `mysql.halo_mysql_version` is below `8.0`. |
| Binary prepared protocol | Implemented | `COM_STMT_PREPARE`, `COM_STMT_EXECUTE`, `COM_STMT_CLOSE`, `COM_STMT_RESET`, and `COM_STMT_SEND_LONG_DATA`, returning binary result packets while routing bound values through the MySQL rewrite/type rules. `COM_STMT_FETCH` fails with error `1421` (`ER_STMT_HAS_NO_OPEN_CURSOR`) because server-side prepared cursors are not opened. |
| SQL prepared statements | Implemented | `PREPARE name FROM 'sql'` (or `@var`), `EXECUTE name [USING @a, ...]`, and `DEALLOCATE` / `DROP PREPARE name`. Statement names are case-insensitive; re-preparing replaces an existing name; `USING` also accepts general expressions (an OpenHalo extension beyond MySQL's `@var`-only rule). Binary and SQL prepared statements share a per-session `max_prepared_stmt_count` limit of `16,382` (error `1461` when exceeded). |
| Session reset & utility commands | Partial / stubbed | `COM_RESET_CONNECTION` aborts open transactions, releases `GET_LOCK` locks, drops prepared statements, user variables, and temp tables, resets session variables, and preserves the active `USE` schema. `COM_PING` returns OK; `COM_FIELD_LIST`, `COM_SET_OPTION`, and `COM_STATISTICS` return minimal compatibility responses. |
| Tested client drivers | Verified in scope | Oracle `mysql` / `mysqldump` 5.7.32, MariaDB CLI, PyMySQL, `go-sql-driver/mysql` 1.9, Connector/J 8.4.0 and legacy 5.1.49, `mysqlslap`, `sysbench`, and raw `COM_STMT_*` wire probes. |
{.wide .expand}

```sql
SET NAMES 'utf8mb4' COLLATE 'utf8mb4_general_ci';
SET @stmt_sql = 'SELECT id, HEX(payload) FROM items WHERE code = ?';
PREPARE lookup_item FROM @stmt_sql;
SET @target = 'alice';
EXECUTE lookup_item USING @target;
DEALLOCATE PREPARE lookup_item;
```

**Boundaries and migration impact:** MySQL Unix domain sockets, `COM_CHANGE_USER`, and `KILL [QUERY]` are unsupported (`1047` on unsupported wire commands; cancel backends from PostgreSQL instead). Wire and storage encoding is always UTF-8—declaring `SET NAMES latin1` warns (`1105`) rather than enabling raw single-byte passthrough, and `@@collation_connection` does not yet propagate to bare string literals (`'A' = 'a'` is `0`). See [collation boundaries](/openhalo/18/compatibility/#collations).

## SQL dialect and DML {#sql}

| Capability | Support level | Implemented behavior |
| --- | --- | --- |
| Lexical & dialect syntax | Implemented | Backtick identifiers, double-quoted string literals, `LIMIT offset, count`, `INSERT ... VALUES ()` empty-column defaults, `INSERT ... SET col=val`, inline `KEY` / `UNIQUE KEY` definitions, column/table `COMMENT`, `CREATE USER ... IDENTIFIED BY`, `@user_var` (`:=` and `SELECT ... INTO @var`), and `DO expr, ...` (PostgreSQL `DO` blocks require `LANGUAGE`). |
| Comments & `LIKE` escapes | Implemented | `#` to newline; `--` only before whitespace, control characters, or end-of-input (`1--1` evaluates as `1 - -1`); executable comments `/*! ... */` and `/*!NNNNN ... */` when `NNNNN <= mysql.halo_mysql_version`; extra OK packet for trailing comments after a multi-statement `;`. String literals retain the backslash of `\%` and `\_` so `LIKE 'a\_b'` matches only literal `a_b`. `NO_BACKSLASH_ESCAPES` is honored. |
| Strict vs lenient writes & `IGNORE` | Implemented (bounded) | With `STRICT_TRANS_TABLES` / `STRICT_ALL_TABLES` off (or under `INSERT IGNORE` / `UPDATE IGNORE`), out-of-range signed integers, `DECIMAL`, and overlong `VARCHAR`/`CHAR`/`BINARY`/`VARBINARY` clip or truncate with warnings (`1264` / `1265`), and `INSERT IGNORE` skips per-row unique or foreign-key conflicts with warnings. `BIGINT UNSIGNED > INT64_MAX` (`1264`) and character `NUL` (`1366`) always fail. |
| `ON DUPLICATE KEY UPDATE` | Implemented | Arbitrates across **all** non-partial `PRIMARY KEY` and `UNIQUE` indexes (including prefix and composite keys), resolves `VALUES(col)` against proposed values and bare `col` against the existing row, processes repeated keys in statement order, and supports `INSERT IGNORE ... ON DUPLICATE KEY UPDATE`. Reports `1` per insert, `2` per changed update, and `0` per no-op update (`1` when `CLIENT_FOUND_ROWS` is set). |
| `REPLACE INTO` | Implemented | Deletes **every** conflicting row across all unique keys (firing `ON DELETE` foreign-key actions and triggers), fills omitted columns from table defaults rather than old row values, and inserts the new row. Reports `1` when no row conflicted—or when conflicting on a table with a single unique index, no row-level `DELETE` triggers (including incoming FK `ON DELETE` triggers), and identical column values—and reports `1 + deleted_rows` whenever conflicting row(s) are physically deleted and re-inserted. Without any unique key on the table, both `ODKU` and `REPLACE` insert plainly. |
| Joined `UPDATE` and `DELETE` | Partial | Supports single-target `UPDATE t1 JOIN t2 ... SET ...` (and comma joins) and single-target `DELETE FROM target USING table_references WHERE ...` (including self-references and index hints), plus `ORDER BY ... LIMIT n` on single-table `UPDATE`/`DELETE`. |
| `AUTO_INCREMENT` | Implemented (bounded) | Backed by `GENERATED BY DEFAULT AS IDENTITY` (`INCREMENT 1 CACHE 1 NO CYCLE`) plus a before-insert trigger. `NULL` and `0` generate the next value unless `NO_AUTO_VALUE_ON_ZERO` is set; explicit positive values atomically advance the sequence; `ALTER TABLE ... AUTO_INCREMENT = n` advances (or resets when the table is empty); `MODIFY` / `CHANGE` can keep, add (continuing past `MAX(col)`), or drop `AUTO_INCREMENT`; `CREATE TABLE ... LIKE` creates an independent counter. |
| `ENGINE=` and `ENCRYPTION=` | Mapped | `ENGINE=<name>` selects an installed PostgreSQL table access method of the same lowercase name (such as `orioledb`); `ENGINE=InnoDB` / `MyISAM` keeps PostgreSQL `heap`. `ENCRYPTION='Y'` selects `tde_heap` and fails explicitly if `pg_tde` is not installed, preventing silent unencrypted creation. |
| Index hints | Syntax accepted & ignored | Parses `USE`, `IGNORE`, and `FORCE` `INDEX` / `KEY` with optional `FOR JOIN`, `FOR ORDER BY`, or `FOR GROUP BY`, table aliases, empty `USE INDEX ()`, `PRIMARY`, and chained hints in `SELECT`, `UPDATE`, and `DELETE`, then discards them. |
{.wide .expand}

```sql
CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(64) UNIQUE,
    code VARCHAR(32) UNIQUE,
    visits INT NOT NULL DEFAULT 0
);

INSERT INTO accounts (email, code, visits)
VALUES ('a@example.com', 'c1', 1), ('b@example.com', 'c2', 1);

-- Updates existing id=1 -> affected rows: 2 (0 if visits were already unchanged)
INSERT INTO accounts (email, code, visits) VALUES ('a@example.com', 'c9', 2)
ON DUPLICATE KEY UPDATE visits = visits + VALUES(visits);

-- Conflicts on BOTH email (id=1) and code (id=2): deletes both, inserts 1 new row -> affected rows: 3
REPLACE INTO accounts (email, code) VALUES ('a@example.com', 'c2');
```

**Boundaries and migration impact:** Plain `UPDATE` still reports **matched** rows rather than changed rows; `DELETE target FROM ... JOIN ...` (including comma joins and `LEFT JOIN` orphan deletes) and multi-target `UPDATE`/`DELETE` fail with `1064`—rewrite joined deletes to `DELETE FROM target USING ... WHERE ...`. Non-default `auto_increment_increment` / `auto_increment_offset` values are echoed without changing ID allocation, and partitioned-table `AUTO_INCREMENT` counter changes are rejected. See [expression and DML boundaries](/openhalo/18/compatibility/#expressions).

## Transactions, isolation, and foreign keys {#transactions}

| Capability | Support level | Implemented behavior |
| --- | --- | --- |
| Transaction control & implicit commits | Implemented | Supports `autocommit=0`, `BEGIN` / `START TRANSACTION`, `COMMIT`, `ROLLBACK`, `SAVEPOINT`, and MySQL implicit commits before `BEGIN`, DDL (except `CREATE TEMPORARY TABLE`), and `SET autocommit=1`. Under `autocommit=1`, each statement in a multi-statement `COM_QUERY` commits independently. Issuing `COMMIT` on an aborted transaction block returns error `1180` (`SQLSTATE 40000`) instead of silently reporting `COMMIT` for a rollback. |
| Statement-level rollback | Implemented | With `mysql.statement_rollback = on` (default), each statement inside an open transaction runs under a hidden savepoint (`__aux_mysql_stmt`), including syntax errors, so a failed statement rolls back only its own changes and keeps earlier statements intact. |
| Isolation & access-mode settings | Implemented (mapped) | Accepts `SET GLOBAL` / `SESSION TRANSACTION ...` (and scope-less `SET TRANSACTION ...`) plus `transaction_isolation` / `tx_isolation` and `transaction_read_only` / `tx_read_only` (aliases kept synchronized). Scope-less `SET TRANSACTION` applies to the next transaction only and is consumed when an application table is opened, or by `COMMIT`/`ROLLBACK`/DDL. **Read-write `REPEATABLE READ`, `READ COMMITTED`, and `READ UNCOMMITTED` run as PostgreSQL `READ COMMITTED`**; **read-only `REPEATABLE READ`** and **`START TRANSACTION WITH CONSISTENT SNAPSHOT`** (when effective MySQL isolation is `REPEATABLE READ`; under other isolation levels it emits warning `138` and ignores the clause, matching InnoDB) acquire a true `REPEATABLE READ` snapshot; `SERIALIZABLE` uses PostgreSQL serialization and maps `40001` failures to MySQL deadlock code `1213` (falling back to `REPEATABLE READ` on a hot standby). |
| Read-only enforcement | Implemented | Read-only transactions reject writes with `1792`. `SET GLOBAL read_only = 1` (ordinary roles) and `super_read_only = 1` (all roles, including superusers) enforce read-only checks per statement (`1290`), covering DML, DDL, `SELECT ... FOR UPDATE`, and persistent sequence writes while keeping `TEMPORARY` tables writable. Setting `super_read_only=1` enables `read_only`; clearing `read_only=0` clears `super_read_only`. |
| Enforced foreign keys | Implemented | Enforces `REFERENCES` constraints and `ON DELETE` / `ON UPDATE` (`RESTRICT`, `NO ACTION`, `CASCADE`, `SET NULL`, `SET DEFAULT`) via PostgreSQL RI triggers. Invalid child writes fail with `1452`; blocked parent updates/deletes fail with `1451`; `INSERT IGNORE` skips invalid child rows with a warning. |
| `FOREIGN_KEY_CHECKS` & pending FKs | Implemented | Session `FOREIGN_KEY_CHECKS=0` (settable by any MySQL user) disables only FK checks and cascading actions while keeping user triggers, `AUTO_INCREMENT`, and `ON UPDATE CURRENT_TIMESTAMP` active. Creating a child table before its parent (or dropping a parent under `FOREIGN_KEY_CHECKS=0`) stores durable pending FK metadata on an extension-managed trigger (`aux_mysql_pending_fk_*`), visible in `SHOW CREATE TABLE` and `information_schema`, and automatically binds a `NOT VALID` FK once the parent is created (if the child owner holds `USAGE` + `REFERENCES`; otherwise warns `1142` and stays pending). |
{.wide .expand}

```sql
-- Stable repeatable snapshot for reporting queries:
START TRANSACTION WITH CONSISTENT SNAPSHOT;
SELECT COUNT(*), SUM(total) FROM orders;
COMMIT;

-- Load child tables before parents during logical dump import:
SET FOREIGN_KEY_CHECKS = 0;
CREATE TABLE order_items (
    id INT PRIMARY KEY,
    order_id INT NOT NULL,
    CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);
CREATE TABLE orders (id INT PRIMARY KEY);
SET FOREIGN_KEY_CHECKS = 1;
-- New orphan writes now fail with 1452; historical rows loaded while checks were off stay unvalidated.
```

**Boundaries and migration impact:** Applications that execute plain `SELECT`s inside a read-write `REPEATABLE READ` transaction and expect not to see concurrent commits must switch read-only reporting transactions to `START TRANSACTION READ ONLY` or `START TRANSACTION WITH CONSISTENT SNAPSHOT`. Transactions executing more than 64 writing statements under `mysql.statement_rollback = on` overflow PostgreSQL's per-backend `subxid` cache—batch writes or review `mysql.statement_rollback = off`. Foreign keys always require a `PRIMARY KEY` or `UNIQUE` index on the parent (`TRUNCATE` does not cascade), and re-enabling `FOREIGN_KEY_CHECKS=1` does not validate existing orphan rows. See [transaction boundaries](/openhalo/18/compatibility/#transactions).

## Data types and expressions {#types}

| Area | Support level | Implemented behavior |
| --- | --- | --- |
| `CHAR` / `VARCHAR` / `TEXT` | Implemented (bounded) | Stored as native PostgreSQL `bpchar`, `varchar`, and `text` (`TINYTEXT`, `TEXT`, `MEDIUMTEXT`, and `LONGTEXT` all use `text`). `CHAR(n)` extracts logical unpadded values by default and honors `PAD_CHAR_TO_FULL_LENGTH` across `CONCAT`, `CONCAT_WS`, `CAST`, `CONVERT`, `HEX`, `ELT`, `GROUP_CONCAT`, user variables, lock names, and `EXECUTE`. **All character columns reject `NUL` (`0x00`) with error `1366` in every mode.** |
| `BINARY` / `VARBINARY` / `BLOB` | Implemented | New `BINARY(n)` (`mysql.binary_n`) zero-pads (`0x00`) to `n` bytes; `VARBINARY(n)` (`mysql.varbinary_n`) enforces byte length `n`; `TINYBLOB`/`BLOB`/`MEDIUMBLOB`/`LONGBLOB` preserve arbitrary byte sequences including `0x00` and non-UTF8 bytes. Strict overflow errors (`1406`); lenient/`IGNORE` truncates with warning (`1265`). Native PG text I/O uses `bytea` hex escaping so `pg_dump` round-trips raw bytes cleanly. |
| Binary ↔ character casts | Implemented | Assigning or `CAST`ing binary data to `CHAR`/`VARCHAR`/`TEXT` validates full UTF-8 payloads and rejects `0x00` (including `BINARY(n)` trailing `0x00` padding!) or invalid UTF-8 with `1366` even under `IGNORE`. `CAST(bin AS SIGNED)` / `UNSIGNED` / `DECIMAL` parses leading ASCII decimal digits and stops at `NUL` or non-digits (malformed `DECIMAL` emits warning `1292`). |
| Signed & unsigned integers | Implemented (bounded) | `TINYINT`, `SMALLINT`, `MEDIUMINT`, `INT`, `BIGINT` plus `UNSIGNED` domains. **`BIGINT UNSIGNED` is a `0..9223372036854775807` (`INT64_MAX`) domain over `int8`**: positive values above `INT64_MAX` always raise `1264` (including `IGNORE` and binary prepared parameters); non-strict negative inputs clip to `0` with warning `1264`. |
| `DECIMAL` & floating point | Implemented | Bare `DECIMAL` defaults to `DECIMAL(10,0)` and preserves `(p,s)` across `SHOW` and `information_schema` (untyped PG `numeric` displays as `decimal(65,30)` with warning `1105`). Unqualified `FLOAT` / `FLOAT(0..24)` uses `float4`; `DOUBLE`, `REAL`, and `FLOAT(25..53)` use `float8`. |
| Date & time types | Partial | `DATE`, `TIME[(0..6)]` (clock time), `DATETIME[(0..6)]`, `TIMESTAMP[(0..6)]`, `YEAR`, and `ON UPDATE CURRENT_TIMESTAMP[(0..6)]`. Both `DATETIME` and bare `TIMESTAMP` map to `timestamp without time zone` (default precision `0`, preserving `0..6` in text and binary results). |
| Booleans & defaults | Implemented (bounded) | `TRUE`/`FALSE`, comparisons, and `IF`/`CASE` boolean results store numeric `1`/`0` (`INT`, `BIGINT`, `TINYINT(1)`, `DECIMAL`, `FLOAT`, `DOUBLE`), string `'1'`/`'0'` (`CHAR`, `VARCHAR`, `TEXT`), and byte `'1'`/`'0'` (`BINARY` zero-padded, `VARBINARY`, `BLOB`) across strict/lenient modes, `DEFAULT`, `CAST`/`CONVERT`, `ODKU`/`REPLACE` conflict checks, generated columns, and prepared statements. Quoted `'true'` stays `'true'`. `SUM(bool)` and boolean `CONCAT`/`GROUP_CONCAT` work. |
| Hex & bit literals (`mysql.hexlit`) | Implemented (bounded) | `X'41'`, `0x41`, `b'101'`, and `0b101` return `VARBINARY` bytes by default (`SELECT 0x41` -> `A`), act as numbers in arithmetic/numeric/BIT contexts (`0x41 + 0` -> `65`), store numbers into numeric columns, bytes into string/binary columns, and bits into `BIT(n)` (`1406` on overflow), and support indexed `binary_col = X'...'` lookups. `HEX()` and `UNHEX()` handle strings, binary, 64-bit two's-complement numbers (`HEX(-1)` -> 16 `F`s), and `BIT` (`UNHEX` of invalid hex returns `NULL` with warning `1411`). |
| String, conditional & math functions | Partial | `/` yields `DECIMAL` (`DIV` integer division; divide-by-zero returns `NULL` + warning `1365`, or error `1365` on strict writes with `ERROR_FOR_DIVISION_BY_ZERO`). Collation-aware `LOCATE`, `INSTR`, `POSITION`, `LIKE`, `STRCMP`, `FIELD`, and `FIND_IN_SET` (matching both collation and trailing-space count); case-sensitive `REPLACE()` and byte-exact `SUBSTRING_INDEX()`; `CHAR`/`VARCHAR`/`TEXT` `IF()` / `IFNULL()`; byte-preserving binary `GROUP_CONCAT()`. `SHOW WARNINGS` / `SHOW ERRORS` retains up to 64 diagnostics. |
{.wide .expand}

```sql
CREATE TABLE payloads (
    id INT PRIMARY KEY,
    flag VARCHAR(8) NOT NULL DEFAULT TRUE,
    fixed_bin BINARY(4) NOT NULL,
    raw_blob BLOB,
    created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
);

INSERT INTO payloads (id, fixed_bin, raw_blob)
VALUES (1, 'A', 0x4100ff);

SELECT flag, HEX(flag), HEX(fixed_bin), HEX(raw_blob), CAST(0x3432 AS UNSIGNED)
FROM payloads;
-- flag='1', HEX(flag)='31', HEX(fixed_bin)='41000000', HEX(raw_blob)='4100FF', CAST=42
```

**Boundaries and migration impact:** Native `ENUM` and `SET` (`1091`), negative or `>= 24:00:00` `TIME` durations, zero dates (`0000-00-00`), MySQL `TIMESTAMP` cross-timezone storage conversion, `CAST(-1 AS UNSIGNED)` uint64 wraparound, boolean `AVG`/`MIN`/`MAX`/`STD`/`BIT_*` or `(1>0)+0`, multi-argument `GROUP_CONCAT(a, b)`, and mixed-type `COALESCE(1, 'a')` / `IF(c, 1, 'a')` are unsupported or differ. Installing `aux_mysql` also adds database-wide `bool -> numeric/float/binary` assignment casts visible to native PostgreSQL sessions in that same database. See [data representation](/openhalo/18/compatibility/#representation) and [PostgreSQL coexistence](/openhalo/18/compatibility/#coexistence).

## Collations and indexes {#indexes}

| Capability | Support level | Implemented behavior |
| --- | --- | --- |
| Four exact MySQL collations | Implemented | `utf8_general_ci`, `utf8mb4_general_ci`, `utf8_bin`, and `utf8mb4_bin` in schema `mysql`. `general_ci` implements MySQL 5.7 BMP case/accent weight tables (`> U+FFFF` weight `0xFFFD`) with `PAD SPACE`, streaming comparator, and abbreviated sort keys; `bin` implements UTF-8 codepoint order with `PAD SPACE`. |
| Other MySQL collation names | Approximated (`1105`) | Accepted in column/table DDL, expression `COLLATE`, views, `CREATE TABLE AS`, and `SET NAMES ... COLLATE`: names ending in `_ci` map to `utf8mb4_general_ci` (or `utf8_general_ci`), and all other names map to `utf8mb4_bin` (or `utf8_bin`), emitting warning `1105`. `SHOW CREATE TABLE` reports the effective collation. |
| Table default collation | Implemented | Unannotated string columns inherit table `COLLATE=` (persisted via `SECURITY LABEL FOR aux_mysql`) or `mysql.default_collation` (`case_insensitive` -> `utf8mb4_general_ci`). |
| Prefix & oversized indexes (`mysql_prefix`) | Implemented (heap recheck) | `KEY (col(n))`, `UNIQUE KEY (col(n))`, and `PRIMARY KEY (col(n))` count `n` characters on character columns and `n` bytes on binary columns across single and composite keys. Keys with explicit prefixes or unbounded/wide columns use the `mysql_prefix` index access method: bounded btree candidate keys narrow lookups while dirty-snapshot heap rechecks compare original prefix values for uniqueness, `ODKU`, and `REPLACE`. Hash collisions never decide equality, and no auxiliary hash index is created on `1.9`. |
| Short full-column indexes | Implemented (native `btree`) | Unprefixed keys whose maximum tuple width fits safely within btree bounds stay native PostgreSQL `btree`, preserving `ORDER BY ... LIMIT` index scans and index-only scans. |
| Per-table key names | Implemented (bounded) | Key names are scoped per table (allowing identical `KEY idx_created` names across tables in a dump); omitted names default to `col`, `col_2`, etc. Physical PostgreSQL index names append `$<8-hex-digits>` while `SHOW INDEX`, `SHOW CREATE TABLE`, `information_schema.STATISTICS`, `DROP INDEX k ON t`, `ALTER TABLE ... DROP/RENAME INDEX`, `CREATE TABLE ... LIKE`, and `1062` duplicate-key messages use the logical MySQL key name. |
{.wide .expand}

```sql
CREATE TABLE articles (
    id INT PRIMARY KEY,
    slug VARCHAR(500) COLLATE utf8mb4_general_ci NOT NULL,
    body LONGTEXT NOT NULL,
    UNIQUE KEY uk_slug_prefix (slug(12)),
    KEY idx_created (id),
    KEY idx_body (body(32))
);

-- Enforces uniqueness on the first 12 characters under utf8mb4_general_ci:
INSERT INTO articles VALUES (1, 'hello-world-alpha', 'first');
-- Fails with 1062 on key 'uk_slug_prefix' because first 12 chars match case-insensitively:
-- INSERT INTO articles VALUES (2, 'HELLO-WORLD-beta', 'second');
```

**Boundaries and migration impact:** Unicode UCA / language-specific weights (`utf8mb4_unicode_ci`, `utf8mb4_0900_ai_ci`, `latin2_czech_cs`) are not reproduced, so sorting and `UNIQUE` collisions can differ from MySQL on accented, ligature, or supplementary-plane strings. `mysql_prefix` indexes always recheck the heap and cannot satisfy `Index Only Scan` or `ORDER BY` sort plans. Logical key names truncate at `54` bytes (`63` minus the 9-byte `$<8-hex>` suffix) and fold case in ASCII only. Upgrading from `1.5` never rebuilds legacy ICU collations or discarded prefix indexes in place; see [migration audits](/openhalo/18/migration/#audit).

## Generated columns {#generated}

| Aspect | Support level | Implemented behavior |
| --- | --- | --- |
| `VIRTUAL` and `STORED` declarations | Implemented (materialized) | Accepts `col type [GENERATED ALWAYS] AS (expr)` with `VIRTUAL` (default) or `STORED`. Because PostgreSQL native virtual columns cannot be indexed or call `aux_mysql` functions, **both `VIRTUAL` and `STORED` columns are physically stored on disk**, while preserving their declared `VIRTUAL GENERATED` / `STORED GENERATED` metadata in `SHOW COLUMNS`, `SHOW CREATE TABLE`, `information_schema.COLUMNS`, and `CREATE TABLE ... LIKE` so Oracle `mysqldump` omits generated values from `INSERT` statements. |
| Dependency chaining & `ALTER` | Implemented | A generated column may reference earlier generated columns in the same table; `ALTER TABLE ... MODIFY / CHANGE` recomputes dependent generated columns, including across base-column type changes. Explicit non-`DEFAULT` writes via `INSERT`, `UPDATE`, `ODKU`, or `REPLACE` fail with `3105`. |
| Deterministic expression policy | Implemented (allowlisted) | `CREATE TABLE`, `ALTER TABLE`, and `CREATE TABLE ... LIKE` validate resolved expressions before planning (`src/mys_generated_policy.h`). Non-deterministic constructs (`RAND()`, `NOW()`, `CURRENT_TIMESTAMP`, `@vars`, `@@vars`, subqueries, sequences, relative date strings like `'now'`/`'today'`, user domains, and arbitrary SQL/PLpgSQL UDFs) fail with `3102`. Audited `aux_mysql` implementations (`CONCAT`, `CONCAT_WS`, `IF`, `IFNULL`, `/`, `DIV`, `HEX`, `UNHEX`, `SUBSTR`, `LOCATE`, `REPLACE`, `DATE_FORMAT` on typed temporal columns, etc.) are wrapped in extension-managed `aux_mysql_gen_<hash>` functions and cleaned up on `DROP` / `ALTER`. |
| Writer `sql_mode` coercion | Implemented | Bounded `VARCHAR(n)` / `CHAR(n)` and `DECIMAL(p,s)` generated columns apply the **writing session's** `sql_mode` and `IGNORE` rules at write time (including constant generators and repeated prepared executions), emitting truncation/range warnings in non-strict mode or errors in strict mode. |
{.wide .expand}

```sql
CREATE TABLE line_items (
    id INT PRIMARY KEY,
    qty INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    gross DECIMAL(12,2) GENERATED ALWAYS AS (qty * unit_price) VIRTUAL,
    label VARCHAR(32) GENERATED ALWAYS AS (CONCAT('item-', id)) STORED,
    KEY idx_gross (gross)
);

INSERT INTO line_items (id, qty, unit_price) VALUES (1, 3, 19.50);
SELECT id, gross, label FROM line_items;
-- 1 | 58.50 | item-1
```

**Boundaries and migration impact:** Because `VIRTUAL` columns are materialized on write, storage space and write cost match `STORED` columns, and changing a later reader's `sql_mode` never changes already stored generated values. Generated `DATE_FORMAT(col, fmt)` requires a typed `DATE`/`DATETIME`/`TIMESTAMP` column (implicit text-to-date casts such as `CAST(CONCAT(...) AS DATE)` fail with `3102`). `VIRTUAL` primary keys and generated expressions referencing `AUTO_INCREMENT` are allowed by OpenHalo 18 as PostgreSQL-backed extensions, but MySQL 5.7 rejects them on dump replay. Pre-1.8 discarded expressions and historical unsafe `IMMUTABLE` wrappers are not auto-repaired by upgrade; see [generated-column audit](/openhalo/18/migration/#audit).

## User locks, metadata, and operations {#operations}

| Capability | Support level | Implemented behavior |
| --- | --- | --- |
| MySQL 5.7 user-level locks | Implemented | `GET_LOCK(str, timeout)`, `RELEASE_LOCK(str)`, `IS_FREE_LOCK(str)`, `IS_USED_LOCK(str)`, and `RELEASE_ALL_LOCKS()`. Supports multiple simultaneous locks and recursive re-acquisition per session; case-insensitive names up to 64 characters (`3057` when longer); integer/float timeouts in seconds (negative waits indefinitely; `0x..` hex literals handled as in MySQL); deadlock wait-cycle detection (`3058`). Transaction `COMMIT`/`ROLLBACK` keeps locks held; `COM_RESET_CONNECTION` and disconnect release them. Backed by PostgreSQL session advisory locks (`objsubid = 19801` in `mysql.database`). |
| `SHOW` & `information_schema` | Partial | `SHOW DATABASES`, `SHOW [FULL] TABLES`, `SHOW [FULL] COLUMNS`, `SHOW INDEX`, `SHOW CREATE TABLE`, `SHOW CREATE VIEW`, `SHOW CHARACTER SET [WHERE ...]`, `SHOW COLLATION`, `SHOW GLOBAL` / `SESSION VARIABLES` (live values via `mysql.show_system_variable`), `SHOW ENGINE INNODB STATUS` (syntax stub), and `SHOW WARNINGS` / `SHOW ERRORS [LIMIT ...]`. `information_schema` (`mys_informa_schema`) exposes `COLUMNS`, `STATISTICS`, `TABLES`, `VIEWS`, `ROUTINES`, `TABLE_CONSTRAINTS`, `KEY_COLUMN_USAGE`, and `REFERENTIAL_CONSTRAINTS` (including pending missing-parent FKs). |
| Backup, restore & replication | PostgreSQL-native + SQL dump | Physical HA, streaming replication, PITR, and archiving use standard PostgreSQL WAL tools (Patroni, pgBackRest). Logical backups work via matched PG18 `pg_dump` / `pg_restore` (retaining triggers and security labels) and Oracle MySQL `mysqldump` within the supported SQL subset. |
{.wide .expand}

```sql
SELECT GET_LOCK('nightly_settlement', 5) AS acquired,
       IS_USED_LOCK('NIGHTLY_SETTLEMENT') = CONNECTION_ID() AS owned_by_me;
-- Perform multi-transaction work; COMMIT does not release GET_LOCK
SELECT RELEASE_LOCK('nightly_settlement');
```

**Boundaries and migration impact:** `GET_LOCK` entries share PostgreSQL's lock table (`max_locks_per_transaction`). `SHOW STATUS`, `performance_schema` live telemetry, and unported `information_schema` tables remain incomplete or empty stubs. MySQL binlog / GTID replication is unavailable (`@@gtid_mode = 'OFF'`, `@@gtid_executed = ''`). See [operational limits](/openhalo/18/compatibility/#operations) and [backup and restore](/openhalo/18/migration/#restore).
