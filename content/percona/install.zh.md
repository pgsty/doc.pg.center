---
title: 安装 pg_tde
linkTitle: 入门安装
description: 通过包管理器、Docker、Kubernetes 或 tar 归档安装 pg_tde，并确认不同 PostgreSQL 版本的打包方式。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/install.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 200
upstream_source: percona
---

你可以通过多种方式安装 `pg_tde`。为了方便、快捷地完成安装，**强烈建议使用包管理器**。

不同 PostgreSQL 版本中 `pg_tde` 的提供方式如下：

| **PostgreSQL 版本** | **是否自动安装 pg_tde？** | **需要执行的操作** |
| -------- | -------- | -------- |
| 17.x 至 17.6（小版本更新） | 是 | 无 |
| 17.7 及后续版本 | 否 | 手动安装软件包 |
| 18.x 及后续版本 | 否 | 手动安装软件包 |

> [!IMPORTANT]
> 从 PPG 17.7 开始，`pg_tde` 不再包含于 Percona Server for PostgreSQL 软件包中，而是单独发布：Debian 或 Ubuntu 上的包名为 `percona-pg-tde(pg-version)`，Red Hat Enterprise Linux 及衍生发行版上的包名为 `percona-pg_tde(pg-version)`。

> [!NOTE]
> 支持的平台、产品和版本详见 [Percona 软件与平台生命周期](https://www.percona.com/services/policies/percona-software-support-lifecycle)。

{{< tabs group="package-manager-docker-kubernetes-tar-download-not-recommended" >}}
{{< tab label="包管理器" value="package-manager" >}}

Percona 为 64 位 Linux 发行版提供 DEB 和 RPM 格式的安装包。

在 Debian 或 Ubuntu 上，使用 `apt` 安装。

在 Red Hat Enterprise Linux 及兼容的衍生发行版上，使用 `yum` 安装。

[在 Debian 或 Ubuntu 上安装](/zh/percona/apt/)
[在 RHEL 或衍生发行版上安装](/zh/percona/yum/)

{{< /tab >}}
{{< tab label="Docker" value="docker" >}}

`pg_tde` 包含在 Percona Distribution for PostgreSQL Docker 镜像中。使用该镜像可以获得完整的加密功能。详细步骤见下方指南。

[在 Docker 中运行](https://docs.percona.com/postgresql/17/docker.html#enable-encryption)

{{< /tab >}}
{{< tab label="Kubernetes" value="kubernetes" >}}

使用 Percona Operator 在 Kubernetes 中部署 Percona Server for PostgreSQL 时，可以启用 `pg_tde`。

{{< /tab >}}
{{< tab label="Tar 归档（不推荐）" value="tar-download-not-recommended" >}}

Percona Distribution for PostgreSQL 的 tar 归档包含 `pg_tde`。详细步骤见下方指南。

[从 tar 归档安装](https://docs.percona.com/postgresql/18/tarball.html)

{{< /tab >}}
{{< /tabs >}}

## 下一步 {#next-steps}

安装完成后，可以继续：

[配置 pg_tde](/zh/percona/setup/)
[了解密钥管理](/zh/percona/global-key-provider-configuration/overview/)
[验证加密配置](/zh/percona/test/)
[启用 WAL 加密](/zh/percona/wal-encryption/)
