---
title: Install pg_tde
linkTitle: Get started
description: Choose packages, containers, Kubernetes, or a source archive for your PostgreSQL deployment.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/install.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 200
upstream_source: percona
---

You can select from multiple easy-to-follow installation options to install `pg_tde`, however **we strongly recommend using a Package Manager** for a convenient and quick installation.

`pg_tde` availability by PostgreSQL version:

| **PostgreSQL version** | **Is pg_tde installed automatically?** | **Action Required** |
| -------- | -------- | -------- |
| 17.x - 17.6 (minor updates) | Yes | None |
| 17.7 (and later) | No | Install the package manually |
| 18.x (and later) | No | Install the package manually |

> [!IMPORTANT]
> Starting with PPG 17.7, `pg_tde` is no longer bundled with the Percona server for PostgreSQL package. It is now delivered as a separate package named `percona-pg-tde(pg-version)` for Debian or Ubuntu and `percona-pg_tde(pg-version)` for Red Hat Enterprise Linux and Derivatives.

> [!NOTE]
> Specific information on the supported platforms, products, and versions is described in the [Percona Software and Platform Lifecycle ](https://www.percona.com/services/policies/percona-software-support-lifecycle) page.

{{< tabs group="package-manager-docker-kubernetes-tar-download-not-recommended" >}}
{{< tab label="Package manager" value="package-manager" >}}

Percona provides installation packages in DEB and RPM formats for 64-bit Linux distributions.

If you are on Debian or Ubuntu, use `apt` for installation.

If you are on Red Hat Enterprise Linux or compatible derivatives, use `yum` for installation.

[Install on Debian or Ubuntu ](/percona/apt/)
[Install on RHEL or derivatives ](/percona/yum/)

{{< /tab >}}
{{< tab label="Docker" value="docker" >}}

`pg_tde` is a part of the Percona Distribution for PostgreSQL Docker image. Use this image to enjoy full encryption capabilities. Check below to get access to a detailed step-by-step guide. 

[Run in Docker ](https://docs.percona.com/postgresql/17/docker.html#enable-encryption)

{{< /tab >}}
{{< tab label="Kubernetes" value="kubernetes" >}}

You can enable `pg_tde` when deploying Percona Server for PostgreSQL in Kubernetes using the Percona Operator.

{{< /tab >}}
{{< tab label="Tar download (not recommended)" value="tar-download-not-recommended" >}}

`pg_tde` is included in the Percona Distribution for PostgreSQL tarball. Select the below link to access the step-by-step guide. 

[Install from tarballs ](https://docs.percona.com/postgresql/18/tarball.html)

{{< /tab >}}
{{< /tabs >}}

## Next steps {#next-steps}

After finishing the installation, you can proceed with:

[Set up pg_tde](/percona/setup/)
[Learn about key management](/percona/global-key-provider-configuration/overview/)
[Validate your encryption setup](/percona/test/)
[Enable WAL encryption](/percona/wal-encryption/)
