---
type: docs
upstream_link: ""
search_keywords: ["SET NAMES", "caching_sha2_password", "mysql_native_password", "mysql_clear_password", "SCRAM", "pg_hba.conf", "mysql.port", "mysql.database", "mysql.max_allowed_packet", "mysql.require_secure_transport", "shared_preload_libraries", "flush_auth_cache", "database_compatibility_mode", "halo_mysql_password_encryption"]
title: Build and configuration
description: Compile matching OpenHalo 18 kernel and aux_mysql binaries, initialize an instance, configure authentication and TLS, and manage mysql.* GUC settings.
weight: 40
---

These instructions apply strictly to the **[PGSTY OpenHalo 18 fork](/openhalo/18/)**. Do not mix them with the historical PG14 openHalo or commercial Halo Database 1.0.16 guides. Verify the exact commit or extension version you are deploying: source tag `v18.6.1` (`2627e6f`, incorporating accepted commit `6a93e8f`) ships `aux_mysql 1.9`, whereas earlier tag `v18.6` (`60e7a22`) ships `aux_mysql 1.5` and multi-platform `18.6.1` binary packages remain pending package acceptance.

## Build matching kernel and extension binaries {#build}

OpenHalo 18 builds with **GNU make** (in-tree or VPATH) or PGXS against the matching OpenHalo 18 installation headers. **Meson is unsupported** and aborts early with an explicit error so an incomplete build cannot be installed by mistake. Top-level `make && make install` compiles and installs both the PostgreSQL 18.6 kernel and `contrib/aux_mysql`; a stock PostgreSQL 18 binary cannot load `aux_mysql`.

On Enterprise Linux 9 / 10, install the required build toolchain and libraries:

```sh
sudo dnf install -y gcc make bison flex perl readline-devel zlib-devel libicu-devel openssl-devel
```

- **ICU (`libicu-devel`)** is required.
- **OpenSSL (`openssl-devel`)** is strongly recommended: it provides TLS connections and RSA-OAEP public-key password exchange for `caching_sha2_password`. Without `--with-openssl`, password logins over the MySQL protocol can only use cleartext `mysql_clear_password`.
- On minimal EL10 containers, ensure `bison`, Perl `FindBin` (`perl-FindBin`), and the `openssl` CLI are present before building and initializing test fixtures.

From a clean, verified checkout (for example, source tag `v18.6.1` at `2627e6f3e94ffdaba9ca6a835c4a1ae2fba34183`, or pinned acceptance commit `6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a`):

```sh
./configure --prefix=/opt/openhalo18 --with-openssl --enable-depend
make -j"$(nproc)"
sudo make install
```

Debug verification builds add `--enable-debug --enable-cassert` and use a separate build directory and `--prefix`. Always pass `--enable-depend` (or perform a clean rebuild) when header files change: linking a newer `aux_mysql.so` against stale kernel object files—or loading prebuilt third-party extensions without rebuilding and testing them against OpenHalo 18's modified parse/plan/protocol headers—is unsupported.

## Initialize an instance and install aux_mysql {#initialize}

Run `initdb` and `pg_ctl` as a dedicated unprivileged OS service account (such as `postgres`), never as `root`:

```sh
sudo install -d -o postgres -g postgres /var/lib/openhalo18
sudo -iu postgres /opt/openhalo18/bin/initdb -D /var/lib/openhalo18/data
```

OpenHalo 18's `postgresql.conf.sample` preloads `aux_mysql` and turns on the MySQL listener out of the box. Review `/var/lib/openhalo18/data/postgresql.conf` before starting:

```ini
listen_addresses = 'localhost'
port = 5432
unix_socket_directories = '/tmp'
shared_preload_libraries = 'aux_mysql'
mysql.listener_on = on
mysql.port = 3306
mysql.database = 'postgres'
mysql.halo_mysql_version = '5.7.32-log'
```

Keep `aux_mysql` in `shared_preload_libraries` alongside any other required preloaded modules (loading `aux_mysql` dynamically without `shared_preload_libraries` fails with an error). Start the server and create the extension explicitly in `mysql.database`:

```sh
sudo -iu postgres /opt/openhalo18/bin/pg_ctl \
  -D /var/lib/openhalo18/data -l /var/lib/openhalo18/server.log start
sudo -iu postgres /opt/openhalo18/bin/psql -X -h /tmp -d postgres \
  -c 'CREATE EXTENSION aux_mysql;'
```

If `aux_mysql` is already installed on an existing data directory, check `extversion` and run the [in-place `ALTER EXTENSION` upgrade](/openhalo/18/migration/#upgrade)—never run `DROP EXTENSION aux_mysql CASCADE` on a populated database.

**Automatic vs explicit extension creation:**

- When `mysql.auto_create_extension = on` (default), the first **superuser** connection over the MySQL protocol synchronously runs `CREATE EXTENSION IF NOT EXISTS aux_mysql` in `mysql.database` before completing the handshake.
- Starting the server or connecting solely via PostgreSQL (`5432`) creates **no** extension objects automatically.
- Non-superuser MySQL logins fail with a privilege hint until a superuser installs `aux_mysql`.
- Automatic creation is automatically suppressed on recovery standbys and during binary upgrades. To keep a deliberate `DROP EXTENSION` from reinstalling on the next superuser MySQL login, set `mysql.auto_create_extension = off` and restart.
- Because `aux_mysql` adds database-wide `bool` assignment casts to `mysql.database` (`postgres` by default), place unrelated native PostgreSQL applications in **separate PostgreSQL databases** rather than sharing `mysql.database`.

## Authentication, TLS, and client connections {#authentication}

MySQL and PostgreSQL protocols share the same PostgreSQL roles (`pg_authid`), SCRAM-SHA-256 / MD5 password verifiers, and `pg_hba.conf` access rules: one password works on both `5432` and `3306`.

Create a least-privilege application role and schema via `psql`:

```sql
CREATE ROLE app LOGIN;
\password app
GRANT CONNECT ON DATABASE postgres TO app;
CREATE SCHEMA app AUTHORIZATION app;
```

Or create a user over a superuser MySQL connection (`CREATE USER app IDENTIFIED BY '...';`, then grant schema privileges as needed).

Add a matching `pg_hba.conf` entry using the **PostgreSQL host database name** (`postgres` when `mysql.database = 'postgres'`, **not** the MySQL schema name `app`):

```text
host    postgres    app    127.0.0.1/32    scram-sha-256
```

`pg_hba.conf` is evaluated first-match; reload PostgreSQL (`pg_ctl reload`) after editing it. Port `3306` supports only `scram-sha-256`, `md5`, `password`, `trust`, and `reject` `pg_hba.conf` authentication methods—other methods (`peer`, `ident`, `cert`, `gss`, `ldap`, `pam`, etc.) fail with `1045` (`28000`), and a `scram-sha-256` HBA rule rejects roles whose stored secret is still `md5`. Enforce TLS-only MySQL connections with `ssl = on` in `postgresql.conf` and `hostssl` rules in `pg_hba.conf` (there is no `mysql.require_secure_transport` GUC). Opening remote access requires updating `listen_addresses` (or `mysql.listen_addresses`), restarting the postmaster, and restricting client CIDRs and firewall rules. Connect with a standard MySQL client:

```sh
mysql --host=127.0.0.1 --port=3306 --user=app --password --database=app
```

**How `caching_sha2_password` and `mysql_clear_password` work:**

- **`caching_sha2_password` (default)**: Because PostgreSQL stores SCRAM/MD5 verifiers from which neither MySQL's `SHA256(SHA256(password))` stage2 digest nor `mysql_native_password`'s `SHA1(SHA1(password))` digest can be derived offline (`mysql_native_password` challenge-response is therefore unsupported), each user's **first login** after startup (or cache eviction) performs MySQL full authentication—sending the password protected by TLS (`ssl = on` / `hostssl`) or encrypted with the server's auto-generated RSA key pair (`mysql_rsa_private_key.pem` in `$PGDATA`), verifying it against `pg_authid`, and caching `(stage2, sha256(rolpassword))` in shared memory. Subsequent logins hit the fast challenge-response path.
- **Automatic and manual cache invalidation**: Changing a role's password (`ALTER ROLE ... PASSWORD` or `\password`) changes `rolpassword`, immediately invalidating the cached entry without hooks or restarts. Superusers can also flush the entire shared-memory cache manually via `SELECT mysql.flush_auth_cache();`.
- **Legacy drivers and `mysql_clear_password`**: Connector/J `8.4`, `go-sql-driver/mysql` `1.9`, PyMySQL, and MySQL 8+ CLIs support `caching_sha2_password` natively. When `mysql.default_authentication_plugin = 'mysql_clear_password'`, the initial greeting announces `mysql_native_password` and the server immediately sends an `AuthSwitchRequest` (`0xfe`) to `mysql_clear_password` so legacy 5.7 clients/drivers (such as Connector/J `5.1.49`, verified over TLS with cleartext plugin opt-in and `connectionCollation=utf8mb4_general_ci`) complete authentication cleanly; always pair `mysql_clear_password` with `hostssl`.

## Parameter reference {#parameters}

| Parameter | Default | PG context | Range / values & operational effect |
| --- | --- | --- | --- |
| `mysql.listener_on` | `on` | `postmaster` (restart) | Enables or disables the MySQL TCP listener on startup. |
| `mysql.port` | `3306` | `postmaster` (restart) | TCP port (`0..65535`); `0` disables the MySQL listener. No MySQL Unix socket is created. |
| `mysql.listen_addresses` | Inherits `listen_addresses` | `postmaster` (restart) | Comma-separated bind addresses for the MySQL listener; `NULL`/unset follows PostgreSQL `listen_addresses`. |
| `mysql.database` | `'postgres'` | `sighup` (reload) | PostgreSQL database to which new MySQL connections bind; MySQL `DATABASE`s are schemas inside it. Pre-create the database and install `aux_mysql` before admitting ordinary users. |
| `mysql.auto_create_extension` | `on` | `postmaster` (restart) | Synchronously runs `CREATE EXTENSION IF NOT EXISTS aux_mysql` on the first superuser MySQL login (disabled on standbys and during `pg_upgrade`). |
| `mysql.halo_mysql_version` | `'5.7.32-log'` | `sighup` (reload) | Advertised in handshake, `VERSION()`, and `@@version`; selects handshake charset (`45` below `8.0`, `255` for `8.0+`) and gates `/*!NNNNN ... */` executable comments. Does **not** indicate `aux_mysql` SQL version. |
| `mysql.default_authentication_plugin` | `'caching_sha2_password'` | `sighup` (reload) | Handshake auth plugin announced to new MySQL connections: `caching_sha2_password` or `mysql_clear_password`. |
| `mysql.auth_cache_size` | `1024` | `postmaster` (restart) | Shared-memory entry count (`0..1000000`) for `caching_sha2_password` fast authentication; `0` disables caching so every login uses full TLS/RSA auth. |
| `mysql.rsa_private_key_file` | `'mysql_rsa_private_key.pem'` | `postmaster` (restart) | RSA private key path (relative to `$PGDATA`) for non-TLS `caching_sha2_password` key exchange; auto-generated on startup if missing. |
| `mysql.max_allowed_packet` | `67108864` (`64 MiB`) | `sighup` (reload) | Byte limit (`1024..1073741823`) on incoming MySQL command packets and accumulated `COM_STMT_SEND_LONG_DATA` payloads. Exposed via `@@max_allowed_packet`; `SET` over MySQL is explicitly rejected. |
| `mysql.statement_rollback` | `on` | `user` (session) | Wraps statements inside explicit transactions in hidden savepoints so a single statement error rolls back only that statement. `off` uses PostgreSQL whole-transaction abort semantics (useful for `> 64`-write bulk transactions). |
| `mysql.default_collation` | `'case_insensitive'` | `user` (session) | Collation in schema `mysql` applied to new string columns without explicit column/table `COLLATE` (`case_insensitive` maps to `utf8mb4_general_ci` on `1.9`). Empty string `''` uses the PG database default collation. |
| `mysql.parser` | `'mysql'` | `user` (session) | SQL dialect on MySQL wire connections: `'mysql'` or `'postgres'` (`'postgresql'` accepted as alias). Native PostgreSQL connections on `5432` always use PostgreSQL SQL. |
{.wide .expand}

Query `pg_settings` and `pg_extension` over a PostgreSQL connection (`5432`) to confirm active values, pending restarts, and the installed `aux_mysql` SQL version:

```sql
SELECT name, setting, context, pending_restart
FROM pg_settings
WHERE name LIKE 'mysql.%'
ORDER BY name;

SELECT extname, extversion
FROM pg_extension
WHERE extname = 'aux_mysql';
```

## Session initialization and diagnostics {#session}

Over a MySQL connection (`3306`), inspect effective session charset, collation, `sql_mode`, isolation, and warnings:

```sql
SET NAMES 'utf8mb4' COLLATE 'utf8mb4_general_ci';
SELECT @@character_set_client, @@character_set_connection,
       @@character_set_results, @@collation_connection;
SHOW WARNINGS;
SELECT @@sql_mode, @@autocommit, @@transaction_isolation, @@transaction_read_only;
```

Always check `SHOW WARNINGS` after `SET NAMES`: requesting an approximated collation such as `SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci'` succeeds with warning `1105` and sets `@@collation_connection` to `'utf8mb4_general_ci'`, whereas direct `SET collation_connection = 'utf8mb4_unicode_ci'` echoes the string without warning or effect. Likewise, verify which `sql_mode` flags and system variables are enforced vs echoed-only in [accepted settings vs implemented behavior](/openhalo/18/compatibility/#accepted-vs-implemented).

## Obsolete and foreign settings not to copy {#old-settings}

| Source product | Obsolete / foreign setting | OpenHalo 18 replacement / action |
| --- | --- | --- |
| OpenHalo PG14 (`1.0`) | `database_compat_mode`, `standard_parserengine_auxiliary` | **Remove.** Wire port selects the protocol; `mysql.parser` controls MySQL connections. |
| OpenHalo PG14 (`1.0`) | `mysql.ci_collation`, `halo_mysql_ci_collation` | **Remove.** Collation is controlled per column/table and via `mysql.default_collation`. |
| Early PG18 research | `halo_mysql.*` GUC prefix | **Rename** to the documented `mysql.*` parameters (`check_pg14_config.py` flags these). |
| Pre-`v18.6.1` root README drafts | `mysql.require_secure_transport`, `mysql.explicit_defaults_for_timestamp`, `mysql.table_access_method_Startup`, `mysql.table_access_method_Convert` | **Remove (non-existent GUCs).** Enforce TLS via `ssl = on` + `hostssl` in `pg_hba.conf`; select table access methods via `default_table_access_method` or DDL `ENGINE=<am>` / `ENCRYPTION='Y'`. |
| OpenHalo PG14 (`1.0`) | `--with-uuid=ossp` requirement, `password_encryption = 'mysql_native_password'` | **Remove.** `mysql.uuid()` uses core `gen_random_uuid()`; roles use standard PostgreSQL `scram-sha-256` passwords with `caching_sha2_password` on `3306`. |
| Commercial Halo 1.0.16 | `cluster_net_services`, `mysql.default_tenant`, `plmyssql`, `hsql -p 1921`, `mysql.on_error_rollback`, `mysql.multi_table_delete_methond`, `mysql.skip_utf8_verify` | **Do not use.** Belong to commercial Halo Database 1.0.16, not `pgsty/openhalo`. |
{.wide .expand}

Always start from a fresh OpenHalo 18 `initdb` configuration and run the [PG14 configuration preflight script](/openhalo/18/migration/#pg14) before migrating settings from an older cluster.
