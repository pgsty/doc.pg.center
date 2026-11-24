---
type: docs
upstream_link: ""
search_keywords: ["ALTER EXTENSION", "1.5", "1.9", "PG14", "mysqldump", "pg_dump", "review_fix_migration", "generated_manifest", "FOREIGN_KEY_CHECKS", "pending foreign key", "pending_foreign_keys", "bind_pending_foreign_keys", "check_pg14_config", "upgrade"]
title: Migration and upgrade
description: Procedures for MySQL 5.7 migration, OpenHalo PG14 logical migration, in-place v18.6 (aux_mysql 1.5) to 1.9 upgrade, non-self-healing object audits, and backup/restore.
weight: 50
---

OpenHalo 18 involves three distinct transition paths that must not be confused:

1. **MySQL 5.7 → OpenHalo 18** — logical schema adaptation and data import against the [compatibility boundaries](/openhalo/18/compatibility/).
2. **OpenHalo PG14 (`1.0.14.x`) → OpenHalo 18** — **logical migration only** (`pg_upgrade` and shared data directories are unsupported and explicitly blocked).
3. **OpenHalo `v18.6` (`aux_mysql 1.5`) → `v18.6.1` / `aux_mysql 1.9` (`2627e6f` / `6a93e8f`)** — **in-place PostgreSQL 18 binary + `ALTER EXTENSION` upgrade**, followed by explicit audit and repair of historical `1.5` objects and data that **never self-heal automatically**.

## Preflight before any migration or upgrade {#preflight}

Inventory the running binary, `aux_mysql` version (`SELECT extversion FROM pg_extension WHERE extname = 'aux_mysql'`), `postgresql.conf`, authoritative MySQL DDL, and application SQL/driver versions. Keep a verified backup and the old installation binaries until post-cutover acceptance.

Always rehearse on a disposable staging copy first: compare row counts, primary/unique keys, text and `HEX()` bytes, column defaults, generated-column values, foreign-key enforcement/cascades, `SHOW WARNINGS`, and transaction/affected-row behavior under the real application driver. For `1.9`, confirm the build comes from source tag `v18.6.1` (`2627e6f3e94ffdaba9ca6a835c4a1ae2fba34183`) or accepted commit `6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a` (never pre-acceptance `a000baa`), and never infer the extension version from `SELECT VERSION()` (`5.7.32-log`).

## Migrate from MySQL 5.7 {#mysql}

Standard Oracle `mysqldump` 5.7 logical dumps can be imported into OpenHalo 18 when schemas and SQL stay within the [documented boundaries](/openhalo/18/compatibility/):

1. **Audit incompatible types and DDL before exporting**:
   - Check `BIGINT UNSIGNED` columns for values above `9223372036854775807` (`INT64_MAX`)—they fail with `1264` in every mode.
   - Check `CHAR`/`VARCHAR`/`TEXT` columns for embedded `0x00` bytes (`1366`)—move raw byte payloads to `BINARY`/`VARBINARY`/`BLOB`, never stripping `0x00` during import.
   - Check non-exact collations (`utf8mb4_unicode_ci`, locale-specific `_ci`/`_cs`) for new `UNIQUE` key duplicates under `utf8mb4_general_ci` or `utf8mb4_bin`.
   - Ensure foreign keys reference `PRIMARY KEY` or `UNIQUE` parent columns (non-unique parent indexes are rejected even under `FOREIGN_KEY_CHECKS=0`). Out-of-order child/parent tables in a dump are handled via pending FKs while `FOREIGN_KEY_CHECKS=0`.
   - Convert unsupported `ENUM`, `SET`, and negative or `>= 24:00:00` `TIME` duration columns explicitly, and remove MySQL stored procedures, MySQL trigger bodies, `EVENT`s, and `DELETE target FROM ... JOIN ...` queries.
2. **Explicit PostgreSQL representation example for `ENUM`, `SET`, and duration `TIME`**:
   The pattern below (executed over the PostgreSQL connection in `mysql.database`) enforces allowed member values and preserves signed durations, **without** automatically replicating MySQL `ENUM` ordinal sorting, `SET` bitmask arithmetic, or MySQL driver wire types—review application queries accordingly:

```sql
CREATE SCHEMA migrated;
CREATE TABLE migrated.example (
    id integer PRIMARY KEY,
    state text CHECK (state IN ('new', 'done')),
    flags text CHECK (string_to_array(flags, ',') <@ ARRAY['red', 'blue']),
    elapsed interval CHECK (extract(year FROM elapsed) = 0
                            AND extract(month FROM elapsed) = 0)
);
INSERT INTO migrated.example VALUES (1, 'done', 'red,blue', interval '-01:02:03');
SELECT state, flags, extract(epoch FROM elapsed) FROM migrated.example;
```

3. **Import without `--force` hiding errors**: Oracle `mysqldump` wraps `SET NAMES`, `FOREIGN_KEY_CHECKS=0`, `TIME_ZONE`, `SQL_MODE`, and view definitions in `/*!50700 ... */` executable comments that OpenHalo 18 executes when `NNNNN <= mysql.halo_mysql_version`. Do **not** treat a `--force` client exit code of `0` as a clean import; verify every table, row count, index, and constraint afterward.

## Migrate from OpenHalo PG14 (`1.0.14.x`) {#pg14}

OpenHalo 18 uses PostgreSQL 18 system catalogs and extension-based MySQL hooks; it is **not** binary-compatible with the OpenHalo 14 fork. Never start OpenHalo 18 binaries on a PG14 data directory or run `pg_upgrade` (`pg_upgrade` explicitly rejects `1.0.14.x` branded binaries, and spoofing the version string would still leave incompatible catalog layouts).

1. Run the read-only configuration and schema preflight scripts from the OpenHalo 18 tree against every PG14 database:

```sh
python3 contrib/aux_mysql/tools/check_pg14_config.py /path/to/old/postgresql.conf
psql -X -d old_database -f contrib/aux_mysql/tools/check_pg14_schema.sql
```

`check_pg14_config.py` exits with code `2` when removed or renamed parameters (`database_compat_mode`, `standard_parserengine_auxiliary`, `mysql.ci_collation`, `halo_mysql.*`, missing `aux_mysql` in `shared_preload_libraries`) require edits. `check_pg14_schema.sql` flags `ENUM`/`SET` columns, `TIME` columns requiring duration range checks, and `FLOAT` columns (`float8` on PG14 vs `float4` for new unqualified `FLOAT` on 18; declare `DOUBLE` to retain 64-bit precision).

2. Initialize a fresh OpenHalo 18 cluster, transfer only reviewed settings (see [obsolete settings](/openhalo/18/configuration/#old-settings)), create `aux_mysql`, apply reviewed user DDL, and load user data logically. **Never replay internal SQL/catalog objects from an OpenHalo 14 dump** into OpenHalo 18.

## Upgrade released v18.6 (`aux_mysql 1.5`) to `1.9` {#upgrade}

Published tag `v18.6` installs `aux_mysql 1.5`. Upgrading an existing OpenHalo 18 cluster to `v18.6.1` / `aux_mysql 1.9` (`2627e6f` / `6a93e8f`) reuses the same PG18 data directory:

1. Stop the running `v18.6` server cleanly.
2. Install the matching new OpenHalo 18 kernel and `aux_mysql 1.9` binaries built from the same commit (never replace `aux_mysql.so` alone). If `mysql.auto_create_extension` was triggering 1.5's old background startup race on fresh test clusters, keep `aux_mysql` managed explicitly.
3. Start the data directory under the new binaries, connect to `mysql.database` via PostgreSQL (`psql`), and run:

```sql
ALTER EXTENSION aux_mysql UPDATE TO '1.9';
SELECT extname, extversion FROM pg_extension WHERE extname = 'aux_mysql';
```

PostgreSQL automatically chains `1.5 → 1.6 → 1.7 → 1.8 → 1.9` without rewriting user tables and preserves `information_schema.columns.EXTRA` descriptors so dependent user views remain intact. **Never run `DROP EXTENSION aux_mysql CASCADE`** on a database containing user tables.

During the brief window between starting new `1.9` binaries and executing `ALTER EXTENSION`, existing `1.5`/`1.8` SQL objects remain operational; once `ALTER EXTENSION` commits, catalog invalidation makes new `1.9` types, casts, and prefix access methods available to both existing and newly opened MySQL sessions without requiring a server restart.

*(Note: in final acceptance, upgrading a real `v18.6` / `1.5` cluster produced **zero raw catalog differences** against a fresh `1.9` install across all 3,476 extension members. Only the separate, unreleased `1.6 → 1.7 → 1.8 → 1.9` development chain retains a benign `pg_catalog.default` vs `pg_catalog.C` collation difference on the ASCII metadata view column `mys_informa_schema.columns.extra`.)*

## Historical objects and wrong data that do NOT self-repair {#audit}

Catalog parity with a fresh `1.9` installation **does not mean historical user tables or previously corrupted values were repaired**. Upgrading `1.5 → 1.9` intentionally avoids guessing lost schema metadata or silently mutating existing rows. Run the read-only migration audit against each application schema in `mysql.database`:

```sh
psql -X -v review_schema=app -v check_fk=1 \
  -f contrib/aux_mysql/tools/review_fix_migration.sql
```

(`check_fk=1` executes read-only orphan-count queries, which scan referenced/child tables.) Every item below requires explicit administrator review and repair:

| Historical state surviving `1.5 → 1.9` | Why upgrade cannot auto-fix it | Supported audit and repair action |
| --- | --- | --- |
| **`BINARY(n)` / `VARBINARY(n)` length lost** (`mysql.binary` / `mysql.varbinary`) | `1.5` discarded `(n)` (`atttypmod = -1`); a declared `BINARY(4)` storing `'A'` physically holds single byte `0x41`. | Compare `octet_length` / `HEX()` against authoritative MySQL DDL; verify all rows fit `(n)`, then run a reviewed MySQL `ALTER TABLE ... MODIFY col BINARY(n)` to migrate to `mysql.binary_n` / `mysql.varbinary_n`. |
| **Prefix index length lost / old whole-column or MD5 index** | `1.5` could create whole-column or expression indexes that no longer record `col(n)`. | Compare `pg_get_indexdef()` with original MySQL DDL; query duplicate prefixes under the target collation (`GROUP BY LEFT(col, n) COLLATE utf8mb4_general_ci HAVING COUNT(*) > 1`), resolve duplicates, and recreate the key via MySQL DDL before dropping the old index. |
| **Legacy ICU collations & indexes** (`case_insensitive`, etc.) | Existing columns/indexes keep their old collation OIDs; weights and `PAD SPACE` differ from `1.9` `utf8mb4_general_ci` / `utf8mb4_bin`. | Check for duplicate keys under the `1.9` collation, then rebuild tables/indexes from reviewed MySQL DDL. For tables lacking default-collation labels, set reviewed metadata explicitly (`SECURITY LABEL FOR aux_mysql ON TABLE app.t IS 'case_sensitive'`). |
| **Discarded generated expression (`NULL` or plain `DEFAULT`)** | Pre-`1.8` parsers turned some `GENERATED ALWAYS AS (expr)` columns into ordinary `NULL`-valued or `DEFAULT` columns; stored `NULL`s cannot reveal `v + 1`. | Supply original MySQL definitions via a trusted `generated_manifest` (below), review the emitted `ALTER TABLE ... MODIFY` statements, and execute them over MySQL in dependency order under the intended `sql_mode`. Also re-`MODIFY` pre-`1.9` generated columns if they need `1.9` writer `sql_mode` coercions. |
| **Unsafe `IMMUTABLE` generator wrappers (`aux_mysql_gen_*`)** | Pre-`1.9` versions could wrap `RAND()`, `NOW()`, `@vars`, or external reads inside an `IMMUTABLE` SQL function. `1.9` blocks `ALTER` / `CREATE TABLE LIKE` (`3102`) on tables retaining unsafe generators, and does not rewrite already folded values. | Inspect generator function bodies printed by `review_fix_migration.sql`, `DROP` or `MODIFY` the unsafe column to an audited deterministic expression, and verify recomputed values. |
| **`NOT ENFORCED` foreign keys & historical orphan rows** | `1.5` created FKs as `NOT ENFORCED`, and `FOREIGN_KEY_CHECKS=0` permits orphan child rows; deleting or rejecting them during `ALTER EXTENSION` would destroy data or block upgrade. | Inspect `conenforced` and `convalidated` plus `check_fk=1` orphan counts, clean up or reconcile orphan rows per business rules, then run `enforce_fk=1` and `validate_fk=1` (below). |
| **Previously mis-stored `'true'`, `'false'`, `'fals'`, or `0` from boolean writes** | Pre-`6a93e8f` builds could store `'true'`/`'false'` in strings or `0` in lenient numbers when writing booleans, which is indistinguishable on disk from an intentional literal `'true'` or `0`. | Reconcile affected tables against authoritative source data or application logs before cutover. |
| **Existing `FLOAT` (`float8`) & unconstrained `DATETIME` domains** | Upgrade never narrows existing `float8` columns to `float4` or truncates existing fractional timestamps. | Inspect stored precision/ranges before running `MODIFY`; use `DOUBLE` explicitly if `float8` precision must be kept. |
{.wide .expand}

After repairing any orphan child rows according to application data rules, enforce and validate historical `NOT ENFORCED` / `NOT VALID` foreign keys transactionally in place (preserving constraint OIDs, comments, and dependencies; rolls back cleanly if any orphan remains):

```sh
psql -X -v review_schema=app -v enforce_fk=1 -v validate_fk=1 \
  -f contrib/aux_mysql/tools/review_fix_migration.sql
```

To generate reviewed `ALTER TABLE ... MODIFY` statements for generated columns whose expressions were discarded in `1.5`, pass `-v generated_manifest=/path/to/manifest.sql` containing rows sourced from your authoritative MySQL schema history:

```sql
INSERT INTO pg_temp.review_fix_generated_source
 (table_schema, table_name, column_name, type_sql, expression_sql, kind, attributes_sql, provenance)
VALUES ('app', 't', 'g', 'varchar(2)', 'v', 'STORED', '', 'original MySQL schema dump');
```

## Pending foreign keys and PostgreSQL privilege checks {#pending-fk}

When a child table declares a foreign key to a missing parent (under `FOREIGN_KEY_CHECKS=0` or during out-of-order dump restore), OpenHalo 18 stores the declaration on a `POST_DATA` trigger (`aux_mysql_pending_fk_*`) and guards new non-`NULL` child writes until the parent appears.

Whenever the parent table is created, altered, or restored—**even when `pg_restore` runs as a PostgreSQL superuser**—OpenHalo 18 checks the **child table owner's current privileges**:

- `USAGE` on the parent schema, **and**
- `REFERENCES` on the parent table (or on every referenced parent column, including implicit primary keys).

If permission is missing, OpenHalo 18 emits **warning `1142`**, allows the parent DDL or restore to finish, leaves existing rows untouched, and keeps the FK in its guarded pending state. Note that dropping and recreating a parent table drops its former grants. Grant the intended `USAGE` and `REFERENCES` privileges to the child owner, then run an `ALTER TABLE` on either the child or parent to complete binding (binding creates a `NOT VALID` constraint so historical orphan rows do not abort DDL; run `VALIDATE CONSTRAINT` after auditing rows).

## Backup, restore, cutover, and rollback {#restore}

Maintain **both** PostgreSQL-native backups and MySQL logical dumps, and rehearse full restore before production cutover:

- **Native `pg_dump` / `pg_restore`**: Use binaries matching your OpenHalo 18 PG18 version. **Retain triggers and security labels**—never pass `--no-security-labels` (which strips table default-collation labels) or strip `aux_mysql_pending_fk_*` triggers (which carry pending missing-parent FK definitions). Legacy pre-`1.8` index names without the `$<8-hex>` suffix remain recognized automatically and need no rename-only rebuild.
- **MySQL logical dumps (`mysqldump`)**: Use **Oracle MySQL `5.7+` `mysqldump` and `mysql` clients** when generated columns are present. MariaDB `10.5` `mysqldump` emits generated column values into `INSERT` statements even against a real MySQL 5.7 server, producing dumps that both MySQL 5.7 and OpenHalo 18 (`3105`) reject. Views or generated expressions using PostgreSQL-only syntax, `VIRTUAL` primary keys, and generated columns referencing `AUTO_INCREMENT` require conversion before replaying a dump onto native MySQL 5.7.
- **Replication & HA**: Use PostgreSQL physical streaming replication / WAL archiving (Patroni, pgBackRest). MySQL binlog / GTID replication is not supported.
- **Rollback**: Downgrading `aux_mysql 1.9 → 1.5` in place is **not supported**—swapping binaries back does not undo SQL catalog upgrades (`mysql.binary_n`, `mysql_prefix`, casts, views). If a cutover must be rolled back, restore the verified pre-upgrade backup onto the matching old kernel and extension binaries.
