---
title: Offline / Air-gapped Install
description: Stage a full dependency closure on a connected machine and install DocumentDB on a host with no internet
  access.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/documentdb.github.io/blob/90cfa088351557cd618034dfc00ab817c35a5f76/app/services/articleService.ts
upstream_ref: website 90cfa08; DocumentDB 1.0
weight: 20
---

An air-gapped host has no route to PGDG either, and DocumentDB pulls PostgreSQL, `pg_cron`, `pgvector` and PostGIS from there — the release assets alone are not enough. Stage the full dependency closure on a connected machine with the **same distribution, release and architecture** as the target.

For a connected host, use the [Linux Packages Quick Start](/documentdb/getting-started/packages/) instead.

## Stage the bundle (connected machine) {#stage-the-bundle-connected-machine}

Configure the repositories exactly as for an online install: run the whole [Install](/documentdb/getting-started/packages/#install) block for your distribution **except the final `sudo apt install -y documentdb-18` / `sudo dnf install -y documentdb-18` line** — delete that line and the `&& \` that precedes it. On RHEL the DocumentDB repository is written by the `tee /etc/yum.repos.d/documentdb.repo` line near the end, so stopping earlier leaves `dnf download` with nothing to find. Then:

```bash {tab="Debian / Ubuntu" group="documentdb-offline-os" value="deb"}
# Debian / Ubuntu
sudo apt-get install -y dpkg-dev
mapfile -t PKGS < <(apt-cache depends --recurse --no-recommends --no-suggests \
    --no-conflicts --no-breaks --no-replaces --no-enhances documentdb-18 \
  | grep '^[a-zA-Z0-9]' | sort -u)
mkdir -p bundle && cd bundle
apt-get download "${PKGS[@]}"
dpkg-scanpackages . /dev/null > Packages && gzip -k Packages
```

```bash {tab="EL / RHEL" value="rpm"}
# RHEL-compatible
sudo dnf install -y dnf-plugins-core createrepo_c
mkdir -p bundle
sudo dnf download --resolve --alldeps --destdir bundle documentdb-18
createrepo_c bundle
```

> [!NOTE]
> **Use the full-closure flags, not `--download-only`.** `apt-get install --download-only` and a bare `dnf download --resolve` skip whatever is already installed on the staging machine; the bundle looks complete and the target dies with `Depends: adduser but it is not installable`.

Expect ~200 packages / 200 MB (DEB) or ~270 / 170 MB (RPM), mostly PostGIS and GDAL. That is more than an online install downloads, because the closure includes packages already present on the staging machine. The `unsandboxed as root` and `dpkg-scanpackages ... override file` warnings are harmless.

## Install from the bundle (air-gapped target) {#install-from-the-bundle-air-gapped-target}

Copy `bundle/` across — including the `Packages`/`Packages.gz` or `repodata/` index inside it, which is what makes the next step resolve — and point the package manager at it:

```bash {tab="Debian / Ubuntu" group="documentdb-offline-os" value="deb"}
# Debian / Ubuntu
echo "deb [trusted=yes] file:///path/to/bundle ./" \
  | sudo tee /etc/apt/sources.list.d/documentdb-offline.list
sudo apt-get update
sudo apt install -y documentdb-18
```

```bash {tab="EL / RHEL" value="rpm"}
# RHEL-compatible
printf '%s\n' '[documentdb-offline]' 'name=DocumentDB offline bundle' \
  'baseurl=file:///path/to/bundle' 'enabled=1' 'gpgcheck=0' \
  | sudo tee /etc/yum.repos.d/documentdb-offline.repo
sudo dnf install -y --disablerepo='*' --enablerepo=documentdb-offline documentdb-18
```

> [!IMPORTANT]
> The `--disablerepo`/`--enablerepo` pair is not optional. DNF **aborts the whole transaction** if any enabled repository is unreachable, and every RHEL-compatible image ships `baseos`, `appstream` and `extras` enabled — so without it the install fails with `Error: Failed to download metadata for repo 'baseos'` even though your bundle is perfectly good. APT differs here: it only warns about unreachable sources and continues.

`[trusted=yes]` / `gpgcheck=0` accept the unsigned local directory. Upstream signatures were verified at staging time; `sha256sum` the transfer if it crosses an untrusted boundary.

Then continue with [Set up and connect](/documentdb/getting-started/packages/#set-up-and-connect) — `documentdb-setup` needs no network.

`mongosh` is **not** part of the bundle and the target cannot reach the MongoDB repository, so stage it in the same pass if you want to verify from the air-gapped host — add `mongodb-mongosh` to the package list after configuring the MongoDB repository shown in the quick start. Otherwise verify with `sudo documentdb-setup --status` and connect from a machine that does have `mongosh`.

## Smaller offline cases {#smaller-offline-cases}

If the target already has PostgreSQL, the PGDG extension dependencies (`postgresql-N-cron`, `-pgvector`, `-postgis-3`) and `jq`, you do not need a bundle:

- **Extension only, one file** — `sudo apt install ./ubuntu24.04-postgresql-18-documentdb_1.0-0_amd64.deb`. No gateway and no `documentdb-setup`.
- **Full stack from the release assets** — pass the five packages for the selected PostgreSQL major to a *single* `apt install` / `dnf install`: `documentdb-N`, the matching `postgresql-N-documentdb` / `postgresqlN-documentdb` extension, `documentdb-common`, `documentdb-gateway`, and `documentdb-postgresql-tools`. For PostgreSQL 18 only, the optional `documentdb` meta package may be included; it selects `documentdb-18`. Local files resolve dependencies only against enabled repositories, so a package whose dependencies are not included still fails.
