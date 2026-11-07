---
title: Linux Packages Quick Start
description: Install DocumentDB on Linux with Ubuntu APT or EL9 RPM/dnf packages, set up a private PostgreSQL instance,
  and run your first query.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/documentdb.github.io/blob/90cfa088351557cd618034dfc00ab817c35a5f76/app/services/articleService.ts
upstream_ref: website 90cfa08; DocumentDB 1.0
weight: 30
---

Install DocumentDB from the published package repository and get a MongoDB-compatible endpoint on your own host.

The current official release publishes the full stack — extension, gateway, setup wizard and systemd units — for **Ubuntu 24.04 and EL9, on PostgreSQL 17 or 18, amd64 or arm64**. EL9 includes Rocky Linux, AlmaLinux, CentOS Stream, and registered Red Hat Enterprise Linux; [Linux packages installation](https://documentdb.io/packages?method=packages) supplies the prerequisite command for each family. Starting with v0.116, this is a deliberately smaller prebuilt matrix than earlier releases. The website repository mirrors only the current release assets and does not carry older packages forward to make other targets appear current.

**Recommended:** install the complete stack, then create a new private PostgreSQL 18 instance. The commands detect architecture on the Linux host where you run them. For containers or macOS/Windows evaluation, choose [Docker installation](https://documentdb.io/packages?method=docker).

> [!IMPORTANT]
> Already running v0.116 or v0.117 from packages? Follow [Upgrading](/documentdb/linux-packages/#upgrading) instead of installing again. Hosts that ran a 1.0 release candidate have no upgrade path; use a clean host. Removing packages preserves database files; reinstalling is not a data reset.

> [!NOTE]
> Need another distribution or PostgreSQL major? We welcome community builds. Check out the `v1.0-0` tag, pass `--version 1.0.0`, and use the version-parameterized [packaging scripts](https://github.com/documentdb/documentdb/blob/v1.0-0/packaging/README.md). `build_packages.sh` builds the extension, `gateway/build_gateway_packages.sh` builds the gateway, and `build_extra_packages.sh` builds the common, tools, stand-alone, and meta packages. PostgreSQL 15 is extension-only because the setup tools require PostgreSQL 16 or newer. These builds are on demand and are not official release assets hosted by documentdb.io.

You do not need PostgreSQL already installed — the setup wizard creates and manages its own instance. The install does add the PGDG repository and pull PostgreSQL, PostGIS and around 160 packages (about 140 MB), so pick a host you are willing to have PGDG on.

## Clean-host installer {#clean-host-installer}

On a fresh Ubuntu 24.04 or EL9 host, download and run the installer:

```sh
curl -fsSLo documentdb-install.sh https://documentdb.io/install.sh &&
sudo sh documentdb-install.sh
```

This installs the current release (v1.0-0) from the package repository on PostgreSQL 18; add `--pg-major 17` for 17.
On a host where DocumentDB is already set up, the installer only reports its status and doesn't upgrade it; to move an existing install to 1.0, follow [Upgrading](/documentdb/linux-packages/#upgrading).

## Install {#install}

<span id="ubuntu-24-04-postgre-sql-18-apt"></span>

### Ubuntu 24.04, PostgreSQL 18 (APT) {#ubuntu-2404-postgresql-18-apt}

```bash
sudo apt update && \
sudo apt install -y curl ca-certificates gnupg && \
curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor --yes -o /usr/share/keyrings/postgresql.gpg && \
echo "deb [signed-by=/usr/share/keyrings/postgresql.gpg] https://apt.postgresql.org/pub/repos/apt noble-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list >/dev/null && \
curl -fsSL https://documentdb.io/documentdb-archive-keyring.gpg | sudo gpg --dearmor --yes -o /usr/share/keyrings/documentdb-archive-keyring.gpg && \
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/documentdb-archive-keyring.gpg] https://documentdb.io/deb stable ubuntu24" | sudo tee /etc/apt/sources.list.d/documentdb.list >/dev/null && \
sudo apt update && \
sudo apt install -y documentdb-18
```

<span id="rocky-linux-alma-linux-or-cent-os-stream-9-postgre-sql-18-rpm"></span>

### Rocky Linux, AlmaLinux, or CentOS Stream 9, PostgreSQL 18 (RPM) {#rocky-linux-almalinux-or-centos-stream-9-postgresql-18-rpm}

```bash
if (. /etc/os-release && [ "$ID" = centos ]) && [ -f /etc/yum.repos.d/pgdg-redhat-all.repo ]; then sudo sed -i 's/rhel-\$releasever_major\.\$releasever_minor-/rhel-$releasever_major-/g' /etc/yum.repos.d/pgdg-redhat-all.repo; fi && \
sudo dnf install -y dnf-plugins-core && \
sudo dnf config-manager --set-enabled crb && \
sudo dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm && \
sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-9-$(uname -m)/pgdg-redhat-repo-latest.noarch.rpm && \
if (. /etc/os-release && [ "$ID" = centos ]) && [ -f /etc/yum.repos.d/pgdg-redhat-all.repo ]; then sudo sed -i 's/rhel-\$releasever_major\.\$releasever_minor-/rhel-$releasever_major-/g' /etc/yum.repos.d/pgdg-redhat-all.repo; fi && \
sudo dnf -qy module disable postgresql && \
sudo rpm --import https://documentdb.io/documentdb-archive-keyring.gpg && \
printf '%s\n' \
  '[documentdb]' \
  'name=DocumentDB Repository' \
  'baseurl=https://documentdb.io/rpm/rhel9' \
  'enabled=1' \
  'gpgcheck=1' \
  'gpgkey=https://documentdb.io/documentdb-archive-keyring.gpg' | sudo tee /etc/yum.repos.d/documentdb.repo >/dev/null && \
sudo dnf install -y documentdb-18
```

<span id="registered-red-hat-enterprise-linux-9-postgre-sql-18-rpm"></span>

### Registered Red Hat Enterprise Linux 9, PostgreSQL 18 (RPM) {#registered-red-hat-enterprise-linux-9-postgresql-18-rpm}

This command requires an active Red Hat subscription. RHEL exposes CodeReady Builder through
`subscription-manager`, not through the `crb` repository ID used by Rocky-family systems.

```bash
sudo subscription-manager repos --enable codeready-builder-for-rhel-9-$(uname -m)-rpms && \
sudo dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm && \
sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-9-$(uname -m)/pgdg-redhat-repo-latest.noarch.rpm && \
sudo dnf -qy module disable postgresql && \
sudo rpm --import https://documentdb.io/documentdb-archive-keyring.gpg && \
printf '%s\n' \
  '[documentdb]' \
  'name=DocumentDB Repository' \
  'baseurl=https://documentdb.io/rpm/rhel9' \
  'enabled=1' \
  'gpgcheck=1' \
  'gpgkey=https://documentdb.io/documentdb-archive-keyring.gpg' | sudo tee /etc/yum.repos.d/documentdb.repo >/dev/null && \
sudo dnf install -y documentdb-18
```

For PostgreSQL 17, select it in [Linux packages installation](https://documentdb.io/packages?method=packages) to generate matching install and setup commands for `documentdb-17`; there is no `documentdb-16`. Both EL9 flows enable CodeReady Builder, which supplies `libqhull_r.so.7` for PostGIS dependencies.

Then install `mongosh`, which you need to talk to the endpoint:

```bash
# Ubuntu 24.04
curl -fsSL https://pgp.mongodb.com/server-8.0.asc | sudo gpg --dearmor --yes -o /usr/share/keyrings/mongodb.gpg
echo "deb [signed-by=/usr/share/keyrings/mongodb.gpg] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb.list
sudo apt update && sudo apt install -y mongodb-mongosh

# EL9
printf '[mongodb-org-8.0]\nname=MongoDB\nbaseurl=https://repo.mongodb.org/yum/redhat/9/mongodb-org/8.0/$basearch/\ngpgcheck=1\nenabled=1\ngpgkey=https://pgp.mongodb.com/server-8.0.asc\n' | sudo tee /etc/yum.repos.d/mongodb.repo
sudo dnf install -y mongodb-mongosh
```

## Set up and connect {#set-up-and-connect}

> [!IMPORTANT]
> The wizard binds the gateway on **all interfaces** (`0.0.0.0:10260`) with a self-signed certificate. Firewall port `10260` before you run it on anything but a private machine, then read [Before exposing it to a network](/documentdb/linux-packages/#before-exposing-it-to-a-network).

Installing the packages puts files on disk; it does not create a database or start the endpoint. The setup wizard does that:

```bash
sudo documentdb-setup --pg-version 18 --use-new-postgres-instance --admin-user admin
```

It creates a new private PostgreSQL 18 instance, installs the extensions, starts the gateway, and enables it at boot. It **prompts for the admin password**. The explicit major and fresh-instance flags keep another installed PostgreSQL major or an existing system cluster from being selected accidentally.

Sample data is opt-in. Add `--load-sample-data` to the setup command to seed the `StoreData` database with 41,505 documents in `stores` and 2 documents in `ratings`. This requires `mongosh`; the command above leaves the new instance empty.

For automation, use the complete [unattended setup](/documentdb/linux-packages/#unattended-setup) command. To use PostgreSQL you already manage on this host, follow [Adopt an existing PostgreSQL instance](/documentdb/linux-packages/#adopt-an-existing-postgre-sql-instance); it changes configuration and may require an administrator-controlled restart. For SQL-only use without a gateway, see [Install the PostgreSQL extension only](/documentdb/linux-packages/#install-the-postgre-sql-extension-only).

Now open a shell against the endpoint. The password prompt uses the admin password you chose during setup. The self-signed certificate bypass is for **local development only**; use a trusted certificate for network access.

```bash
mongosh localhost:10260 -u admin -p --authenticationMechanism SCRAM-SHA-256 \
        --tls --tlsAllowInvalidCertificates
```

A database and collection are created on first write:

```javascript
> use quickstart
> db.orders.insertOne({ item: "widget", qty: 5 })
{ acknowledged: true, insertedId: ObjectId('...') }

> db.orders.find()
[ { _id: ObjectId('...'), item: 'widget', qty: 5 } ]
```

**That is a working DocumentDB.** Confirm the service state with `sudo documentdb-setup --status` and the version with `documentdb-gateway --version`.

## Where to go next {#where-to-go-next}

- Build an application: [Node.js Quick Start](/documentdb/getting-started/nodejs-setup/) or [Python Quick Start](/documentdb/getting-started/python-setup/)
- Secure it, manage services, run SQL, upgrade, uninstall, and hosts without systemd: [Operating a package install](/documentdb/linux-packages/)
- Install without internet access: [Offline / air-gapped install](/documentdb/linux-packages/offline/)
- Choose between the published distributions, architectures and PostgreSQL majors: [Linux packages installation](https://documentdb.io/packages?method=packages)

## Troubleshooting {#troubleshooting}

- `Unable to locate package documentdb-18` (apt) / `No match for argument: documentdb-18` (dnf) — the DocumentDB repository was not added, or the host is not in the current release matrix. Check [Linux packages installation](https://documentdb.io/packages?method=packages)
- `documentdb-18 : Depends: postgresql-18 but it is not installable` — PGDG was not added first
- `nothing provides libqhull_r.so.7` — CRB or CodeReady Builder was not enabled for the selected EL9 family
- `MongoServerError: Invalid key` — empty or wrong password; a bare `-p` prompts, so a non-interactive shell sends nothing
- Anything else — `sudo documentdb-setup --status` reports the listener, service states and resolved paths

More failure modes, including hosts without systemd: [Operating a package install](/documentdb/linux-packages/#troubleshooting).

## If you used an earlier repository target {#if-you-used-an-earlier-repository-target}

documentdb.io no longer publishes packages for Ubuntu 22.04, Debian 11/12/13, RHEL-compatible 8, or PostgreSQL 16. Existing installations keep running, but receive no package updates and cannot reinstall those packages from documentdb.io.

Empty signed metadata remains at the retired repository URLs so `apt update` and `dnf makecache` continue to work. Remove the source on a host that will not move to the current matrix:

```bash
# Debian / Ubuntu
sudo rm -f /etc/apt/sources.list.d/documentdb.list
sudo apt update

# RHEL-compatible
sudo rm -f /etc/yum.repos.d/documentdb.repo
sudo dnf clean all
```

To remain on an older target, use its GitHub release assets or build from the matching source tag. Neither path is part of the current hosted support matrix.
