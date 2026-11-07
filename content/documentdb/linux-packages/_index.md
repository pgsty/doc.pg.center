---
title: Operating a Package Install
description: Secure, manage, upgrade and remove a DocumentDB installed from Linux packages, including known package-install
  issues.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/documentdb.github.io/blob/90cfa088351557cd618034dfc00ab817c35a5f76/app/services/articleService.ts
upstream_ref: website 90cfa08; DocumentDB 1.0
weight: 30
---

Day-2 operations for a DocumentDB installed from Linux packages: securing the endpoint, managing services, running SQL, upgrading, and removal. Install first with the [Linux Packages Quick Start](/documentdb/getting-started/packages/).

## Before exposing it to a network {#before-exposing-it-to-a-network}

The gateway binds **all interfaces** (`0.0.0.0:10260` and `[::]:10260`) by default. The PostgreSQL instance behind it stays on loopback.

Before using this anywhere but a private machine:

- Restrict the listener with `DOCUMENTDB_LISTEN_ADDR=127.0.0.1:10260` in `/etc/documentdb/local/<major>/gateway.env` and restart the service, or firewall port `10260`. **Re-running `documentdb-setup` silently resets this to a wildcard bind**, so re-check with `grep DOCUMENTDB_LISTEN_ADDR /etc/documentdb/local/<major>/gateway.env` afterwards. A firewall rule is the more durable control.
- Use a strong admin password and create per-application users rather than sharing `admin`.

### Replace the self-signed certificate {#replace-the-self-signed-certificate}

`tlsAllowInvalidCertificates=true` disables server authentication. To use a real certificate,
set all three values in `/etc/documentdb/local/<major>/gateway.env`:

```ini
DOCUMENTDB_TLS_AUTO_GENERATE=false
DOCUMENTDB_TLS_CERT_FILE=/etc/documentdb/tls/server.crt
DOCUMENTDB_TLS_KEY_FILE=/etc/documentdb/tls/server.key
```

The gateway runs as `documentdb-gateway`. Every parent directory must be traversable by that
account; keep the private key restricted but readable, for example
`root:documentdb-gateway` with mode `0640`. Restart
`documentdb-gateway-local@<major>.service`, verify it is active, and then remove
`tlsAllowInvalidCertificates=true` from clients.

## Services and paths {#services-and-paths}

```bash
sudo documentdb-setup --status      # gateway listener, service states, resolved paths
documentdb-gateway --version        # DocumentDB version
dpkg -l | grep documentdb           # or: rpm -qa | grep documentdb
```

| Thing | Where |
| --- | --- |
| Gateway port | `10260` |
| PostgreSQL port | `9700 + <major>` (9718 for PG 18), loopback only |
| Gateway log | systemd: `journalctl -u documentdb-gateway-local@18.service` · otherwise `/var/lib/documentdb-gateway/gateway.log` |
| PostgreSQL log | systemd: `journalctl -u documentdb-postgresql@18.service` · otherwise `/var/lib/documentdb-local/<major>/data/pglog.log` |
| Setup state / gateway env | `/etc/documentdb/local/<major>/setup.conf`, `.../gateway.env` |

On a systemd host both services log to the journal; the log **files** above exist only when `documentdb-setup` falls back to its non-systemd `nohup` mode. `documentdb-setup --status` prints whichever applies to your host.

Units are templated per PostgreSQL major:

```bash
sudo systemctl status  documentdb-local@18.target
sudo systemctl restart documentdb-local@18.target
sudo systemctl stop    documentdb-local@18.target
```

<span id="adopt-an-existing-postgre-sql-instance"></span>

## Adopt an existing PostgreSQL instance {#adopt-an-existing-postgresql-instance}

Use this mode only when PostgreSQL already exists **locally on the gateway host** and its service and data remain
operator-owned; remote PostgreSQL adoption is not supported. You need administrator access to change PostgreSQL configuration and restart its service. Back up the instance first. The wizard does not create, delete, start, or stop
that PostgreSQL instance, but it does add managed configuration blocks, create the gateway role,
install the DocumentDB extensions, and register the gateway.

Identify the instance as `<major>/<name>`. On Ubuntu, run `pg_lsclusters`; a typical instance
is `18/main`. The standard PGDG layout on EL9 has one instance per major and also uses
`18/main`; add `--pg-port` when it listens on a non-default port.

```bash
sudo documentdb-setup --target-postgres-instance 18/main --admin-user admin
```

If `shared_preload_libraries` changed, the first run prints a restart handoff instead of
finishing setup. Restart the operator-managed PostgreSQL service, then re-run the exact setup
command it prints. Typical service names are `postgresql@18-main.service` on Ubuntu and
`postgresql-18.service` on EL9. The wizard intentionally does not restart an adopted
PostgreSQL instance for you.

The wizard's default `default_toast_compression` setting applies to newly written values in
every database on an adopted instance. If other workloads must retain PostgreSQL's own default,
prefix both setup runs with `sudo DOCUMENTDB_TOAST_COMPRESSION=default`.

<span id="install-the-postgre-sql-extension-only"></span>

## Install the PostgreSQL extension only {#install-the-postgresql-extension-only}

Choose this advanced path for SQL-facing DocumentDB capabilities in PostgreSQL you manage.
It does **not** install the gateway, create a network endpoint for drivers, or run
`documentdb-setup`. Shell, driver, and VS Code quick starts require the complete stack instead.

Use the extension package for your PostgreSQL major: `postgresql-N-documentdb` on Ubuntu
or `postgresqlN-documentdb` on EL9. You own PostgreSQL configuration, extension activation,
and service restarts. Create `documentdb_extended_rum` as well as `documentdb`:
`CREATE EXTENSION documentdb CASCADE` does not pull it in, and without it every index
creation fails. Follow the matching release's [manual package instructions](https://github.com/documentdb/documentdb/blob/v1.0-0/packaging/README.md),
or the [extension-only offline instructions](/documentdb/linux-packages/offline/#smaller-offline-cases)
when PostgreSQL and all extension dependencies are already installed.

## Running SQL against a package-managed private instance {#running-sql-against-a-package-managed-private-instance}

A greenfield PostgreSQL instance runs as the `documentdb-local` user on a socket, so a bare
`psql` will not find it:

```bash
sudo -u documentdb-local psql -h /run/documentdb-local/18/postgresql -p 9718 -d postgres
```

```sql
SELECT extname, extversion FROM pg_extension WHERE extname LIKE 'documentdb%';
```

For an adopted instance, use the operator's existing PostgreSQL connection instead.

## Upgrading {#upgrading}

Package installs from v0.116 or v0.117 upgrade in place to 1.0. Move the entire stack
together; upgrading only `postgresql-N-documentdb` does not update the gateway, tools,
common payload, or `documentdb-N`. These steps use systemd; upgrading a host without it isn't covered here.
On a package-managed private PostgreSQL 18 instance:

> [!WARNING]
> A host that ran a 1.0 release candidate (RC1 or RC2) has no upgrade path. Move it to a
> clean host or a new, empty PostgreSQL instance and follow the
> [fresh installation](/documentdb/getting-started/packages/). Removing packages alone does not create a
> fresh database: package removal preserves PostgreSQL data and in-database content, and a
> later setup run reuses an initialized data directory.

```bash
# Debian / Ubuntu
sudo systemctl stop documentdb-gateway-local@18.service &&
sudo apt update &&
sudo apt install --only-upgrade documentdb-18 postgresql-18-documentdb \
  documentdb-common documentdb-gateway documentdb-postgresql-tools

# EL9: use this instead of the apt commands above
sudo systemctl stop documentdb-gateway-local@18.service &&
sudo dnf upgrade documentdb-18 postgresql18-documentdb \
  documentdb-common documentdb-gateway documentdb-postgresql-tools
```

Upgrading the packages does not update the database catalog. The simplest way is to restart
PostgreSQL so it loads the new libraries, then re-run setup with the options you installed with.
Setup updates the extensions and then starts the gateway:

```bash
sudo systemctl restart documentdb-postgresql@18.service &&
sudo documentdb-setup --pg-version 18 --use-new-postgres-instance --admin-user admin
```

Setup adds any missing `shared_preload_libraries` entries and updates the extensions, but only in
the `postgres` database. If your gateway uses another database, take the manual route below. It also asks for the admin password and sets it on the existing admin
user: enter the current password to keep it.

To update by hand, or for every other database that has DocumentDB installed, first check that
the extended RUM library is preloaded:

```bash
sudo -u documentdb-local psql -h /run/documentdb-local/18/postgresql -p 9718 -d postgres -X -Atc "SHOW shared_preload_libraries;"
```

If `pg_documentdb_extended_rum` is missing (possible on a 0.116 install), add it before updating;
the update below would succeed without it, and index builds would fail later. If the gateway uses
`postgres`, re-run setup as above. If it uses another database, add the library to
`shared_preload_libraries` in the instance's `postgresql.conf` yourself: setup would point the
gateway back at `postgres`. Then restart
PostgreSQL, update the extensions in one transaction, and start the gateway only if that worked:

```bash
sudo systemctl restart documentdb-postgresql@18.service &&
sudo -u documentdb-local psql -h /run/documentdb-local/18/postgresql -p 9718 -d postgres \
  -X -1 -v ON_ERROR_STOP=1 \
  -c 'ALTER EXTENSION documentdb_core UPDATE;' \
  -c 'ALTER EXTENSION documentdb UPDATE;' \
  -c 'CREATE EXTENSION IF NOT EXISTS documentdb_extended_rum CASCADE;' \
  -c 'ALTER EXTENSION documentdb_extended_rum UPDATE;' &&
sudo systemctl start documentdb-gateway-local@18.service
```

`-1` runs the statements as one transaction: if any fails, every extension stays at its old version
and the gateway stays stopped. `-X` skips `~/.psqlrc`, which could otherwise turn `ON_ERROR_STOP` off. If DocumentDB is installed in other databases too, run the `psql` part for each of them, with
that `-d`, before the last line, so the gateway starts only after every database is updated.
PostgreSQL applies intermediate upgrade scripts automatically. Take a backup first.

On a host with both PostgreSQL 17 and 18, `documentdb-common`, `documentdb-gateway` and
`documentdb-postgresql-tools` serve both majors, so upgrading them affects both: stop both gateways
(`documentdb-gateway-local@17.service` and `@18.service`) before upgrading, then update each major.

For an adopted PostgreSQL instance, setup never restarts PostgreSQL. Stop the gateway
(`documentdb-gateway-local@18.service`) before upgrading, restart the operator-managed PostgreSQL
service yourself, then re-run
`documentdb-setup --pg-version 18 --target-postgres-instance 18/main --admin-user admin` (with your cluster name); it
updates the extensions and then starts the gateway. If
setup has to change `shared_preload_libraries`, it exits without updating the extensions: restart
PostgreSQL and run it once more. By hand, use that instance's own `psql` connection.

## Remove or reset {#remove-or-reset}

### Greenfield: destroy the package-managed instance {#greenfield-destroy-the-package-managed-instance}

```bash
# Reset reads setup.conf before removing it, stops the services, and destroys
# the package-managed data directory. Do not run --restore first.
sudo documentdb-local-reset --pg-version 18 --confirm-destroy    # DESTROYS the data directory

# Name the package you installed AND the extension: autoremove does not reap
# postgresql-18-documentdb, and 'remove' would leave config behind.
sudo apt purge --autoremove documentdb-18 postgresql-18-documentdb
sudo dnf remove documentdb-18 postgresql18-documentdb && sudo dnf autoremove
```

<span id="brownfield-detach-from-an-existing-postgre-sql-instance"></span>

### Brownfield: detach from an existing PostgreSQL instance {#brownfield-detach-from-an-existing-postgresql-instance}

Before restoring, run `sudo documentdb-setup --status` and note the gateway port for the major
you are removing.

On a systemd host, a scoped restore stops and disables that major's gateway:

```bash
sudo documentdb-setup --restore --pg-version 18
```

On a host without systemd, the current setup tooling cannot safely attribute a nohup gateway process to one
PostgreSQL major. If only one DocumentDB major is configured, use an unscoped restore so the
orphan gateway sweep runs:

```bash
sudo documentdb-setup --restore --yes
```

If more than one DocumentDB major is configured without systemd, schedule a maintenance window
and use the same unscoped restore. It detaches every configured major and stops the nohup
gateways; re-run setup for the majors you are keeping afterward. A scoped restore alone is not
sufficient on a no-systemd host.

Restart the adopted PostgreSQL service after restore to apply removal of the managed settings.
On an unscoped multi-major restore, restart each operator-managed PostgreSQL service involved.

Verify that the target gateway port is no longer listening before removing packages. Substitute
the port you noted above; the command should produce no output:

```bash
ss -lnt | grep ':10260'
```

Then remove the selected major:

```bash
sudo apt purge --autoremove documentdb-18 postgresql-18-documentdb
sudo dnf remove documentdb-18 postgresql18-documentdb && sudo dnf autoremove
```

Do not run `documentdb-local-reset` for brownfield installations: the PostgreSQL instance and
its data belong to the operator. Do not run restore before a greenfield reset either; restore
deletes the state that identifies custom data directories and protects adopted clusters.

On a systemd multi-major host, remove one major at a time and re-check the survivor:
`documentdb-common` owns the shared tooling and only `documentdb-N` holds it.

## Known package-install issues {#known-package-install-issues}

These are defects in this release, not expected behaviour. Most need a host without systemd to hit; the status issue also affects systemd hosts.

| Area | Issue | Affects |
| --- | --- | --- |
| Status | `documentdb-setup --status` can report "active" for any process holding port 10260 | **any host** |
| Restart | Re-running `documentdb-setup` to restart can hang; redirecting output to a file avoids it | no systemd |
| Stop | A scoped `documentdb-setup --restore --pg-version N` cannot stop a nohup gateway; follow the no-systemd brownfield removal steps above | no systemd |
| Minimal RHEL | Install `procps-ng` first, or `--restore` reports success while the gateway keeps serving and a later run fails with `Port 10260 is already in use` | no systemd |

**Prefer a systemd host for anything you care about**, where the service lifecycle is managed by systemd rather than by the setup script.

<span id="multiple-postgre-sql-majors"></span>

## Multiple PostgreSQL majors {#multiple-postgresql-majors}

Install the matching `documentdb-N` for every major you configure. `documentdb-setup` refuses a major whose extension package is missing:

```text
ERROR: The DocumentDB extension package is not installed for PostgreSQL 17
(/usr/share/postgresql/17/extension/documentdb.control is missing).
```

Each major also needs its own gateway port — the second one fails on `Gateway port 10260 is already in use` unless you pass `--gateway-port`:

```bash
sudo documentdb-setup --pg-version 17 --use-new-postgres-instance \
  --gateway-port 10261 --admin-user admin
```

## Troubleshooting {#troubleshooting}

Failure modes beyond the four in the [quick start](/documentdb/getting-started/packages/#troubleshooting):

- `Bad GPG signature` on `pgdg-common` — wrong architecture in the PGDG repository URL
- `apt install` hangs in a container — `export DEBIAN_FRONTEND=noninteractive` first, and drop the leading `sudo` when running as `root` (minimal images often have no `sudo`). Keep `sudo -u <user>`, which switches user; `su documentdb-local -c` fails because that account has `/usr/sbin/nologin`, so use `su -s /bin/bash documentdb-local -c '...'`
- `ss: command not found` on a minimal EL9 host — install `iproute`; the DocumentDB packages do not pull it in
- `db.version()` and `buildInfo` in `mongosh` report the emulated MongoDB wire version, not DocumentDB's — use `documentdb-gateway --version`

## Unattended setup {#unattended-setup}

`documentdb-setup` prompts for the admin password. For servers and CI, provide exactly one
password source and pass `--yes`. For a new private instance:

```bash
printf '%s' "$ADMIN_PW" | sudo documentdb-setup --pg-version 18 \
  --use-new-postgres-instance --admin-user admin --admin-password-stdin --yes
```

For brownfield adoption, replace `--pg-version 18 --use-new-postgres-instance` with
`--target-postgres-instance 18/main`. You can use
`--admin-password-file /path/to/protected/file` instead of stdin.
