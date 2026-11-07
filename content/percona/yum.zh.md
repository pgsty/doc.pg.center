---
title: 在 Red Hat Enterprise Linux 及其衍生发行版上安装 pg_tde
linkTitle: RHEL 及兼容发行版
description: 在 RHEL 及衍生发行版上启用 Percona 仓库并安装 pg_tde。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/yum.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 220
upstream_source: percona
---

本教程介绍如何随 [Percona Distribution for PostgreSQL](https://docs.percona.com/postgresql/latest/index.html) 安装 `pg_tde`。

> [!TIP]
> 继续之前，请检查[支持的平台列表](https://www.percona.com/services/policies/percona-software-support-lifecycle)。

## 安装 percona-release {#install-percona-release}

你需要使用 `percona-release` 仓库管理工具来启用所需的 Percona 仓库。

1. 安装 `percona-release`：

    ```bash
    sudo yum -y install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
    ```

2. 启用仓库：

    ```bash
    sudo percona-release enable-only ppg-18
    ```

## 安装 pg_tde {#install-pgtde}

安装 `pg_tde`：

```bash
sudo yum install -y percona-pg_tde(pg-version)
```

### PostgreSQL 18 示例 {#example-for-postgresql-18}

```bash
sudo yum install -y percona-pg_tde18
```

## 下一步 {#next-steps}

[配置 pg_tde](/zh/percona/setup/)
