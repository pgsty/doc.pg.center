---
title: Install pg_tde on Red Hat Enterprise Linux and Derivatives
linkTitle: RHEL / Rocky / Alma
description: Install the pg_tde RPM package on Red Hat Enterprise Linux and compatible distributions.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/yum.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 220
upstream_source: percona
---

This tutorial shows how to install `pg_tde` with [Percona Distribution for PostgreSQL](https://docs.percona.com/postgresql/latest/index.html).

> [!TIP]
> Check the [list of supported platforms ](https://www.percona.com/services/policies/percona-software-support-lifecycle) before continuing.

## Install percona-release {#install-percona-release}

You need the `percona-release` repository management tool that enables the desired Percona repository for you.

1. Install `percona-release`:

    ```bash
    sudo yum -y install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
    ```

2. Enable the repository:

    ```bash
    sudo percona-release enable-only ppg-18
    ```

## Install pg_tde {#install-pgtde}

Install `pg_tde`:

```bash
sudo yum install -y percona-pg_tde(pg-version)
```

### Example for PostgreSQL 18 {#example-for-postgresql-18}

```bash
sudo yum install -y percona-pg_tde18
```

## Next steps {#next-steps}

[Configure pg_tde ](/percona/setup/)
