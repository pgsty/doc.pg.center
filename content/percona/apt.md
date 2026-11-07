---
title: Install pg_tde on Debian or Ubuntu
linkTitle: Debian / Ubuntu
description: Install the separate pg_tde package from Percona’s Debian and Ubuntu repositories.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/apt.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 210
upstream_source: percona
---

This page explains how to install `pg_tde` for [Percona Distribution for PostgreSQL ](https://docs.percona.com/postgresql/latest/index.html).

> [!TIP]
> Check the [list of supported platforms ](https://www.percona.com/services/policies/percona-software-support-lifecycle) before continuing.

## Preconditions {#preconditions}

1. Remove any upstream PostgreSQL packages (postgresql-*) that may already be installed on Debian or other apt-based systems. These packages conflict with Percona Server for PostgreSQL and with the standalone `pg_tde` package.
2. Ensure you enable the Percona APT repository using the repository management tool `percona-release`. This ensures the correct Percona Server for PostgreSQL and pg_tde packages are available for installation.

## Install percona-release {#install-percona-release}

1. You need the following dependencies to install `percona-release`:

    - `wget`
    - `gnupg2`
    - `curl`
    - `lsb-release`

    Install the dependencies:

    ```bash
    sudo apt-get install -y wget gnupg2 curl lsb-release
    ```

2. Fetch the `percona-release` package

    ```bash
    sudo wget https://repo.percona.com/apt/percona-release_latest.generic_all.deb
    ```

3. Install `percona-release`

    ```bash
    sudo dpkg -i percona-release_latest.generic_all.deb
    ```

4. Enable the Percona Distribution for PostgreSQL repository

    ```bash
    sudo percona-release enable-only ppg-18
    ```

5. Update the local cache

    ```bash
    sudo apt-get update
    ```

## Install pg_tde {#install-pgtde}

After all [preconditions](#preconditions) are met, install the `pg_tde` package:

```bash
sudo apt-get install -y percona-pg-tde(pg-version)
```

### Example for PostgreSQL 18 {#example-for-postgresql-18}

```bash
sudo apt-get install -y percona-pg-tde18
```

## Next steps {#next-steps}

[Configure pg_tde ](/percona/setup/)
