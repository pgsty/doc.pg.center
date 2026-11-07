---
title: 在 Debian 或 Ubuntu 上安装 pg_tde
linkTitle: Debian / Ubuntu
description: 在 Debian 或 Ubuntu 上配置 Percona APT 仓库并安装 pg_tde 软件包。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/apt.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 210
upstream_source: percona
---

本页介绍如何为 [Percona Distribution for PostgreSQL](https://docs.percona.com/postgresql/latest/index.html) 安装 `pg_tde`。

> [!TIP]
> 继续之前，请检查[支持的平台列表](https://www.percona.com/services/policies/percona-software-support-lifecycle)。

## 前置条件 {#preconditions}

1. 卸载 Debian 或其他基于 apt 的系统上可能已安装的上游 PostgreSQL 软件包（postgresql-*）。这些软件包与 Percona Server for PostgreSQL 以及独立的 `pg_tde` 软件包冲突。
2. 使用仓库管理工具 `percona-release` 启用 Percona APT 仓库，以便安装正确的 Percona Server for PostgreSQL 和 pg_tde 软件包。

## 安装 percona-release {#install-percona-release}

1. 安装 `percona-release` 需要以下依赖：

    - `wget`
    - `gnupg2`
    - `curl`
    - `lsb-release`

    安装依赖：

    ```bash
    sudo apt-get install -y wget gnupg2 curl lsb-release
    ```

2. 获取 `percona-release` 软件包：

    ```bash
    sudo wget https://repo.percona.com/apt/percona-release_latest.generic_all.deb
    ```

3. 安装 `percona-release`：

    ```bash
    sudo dpkg -i percona-release_latest.generic_all.deb
    ```

4. 启用 Percona Distribution for PostgreSQL 仓库：

    ```bash
    sudo percona-release enable-only ppg-18
    ```

5. 更新本地缓存：

    ```bash
    sudo apt-get update
    ```

## 安装 pg_tde {#install-pgtde}

满足全部[前置条件](#preconditions)后，安装 `pg_tde` 软件包：

```bash
sudo apt-get install -y percona-pg-tde(pg-version)
```

### PostgreSQL 18 示例 {#example-for-postgresql-18}

```bash
sudo apt-get install -y percona-pg-tde18
```

## 下一步 {#next-steps}

[配置 pg_tde](/zh/percona/setup/)
