---
title: 配置 pg_tde
linkTitle: 加载扩展
description: 配置共享预加载库、重启 PostgreSQL，并在目标数据库中创建 pg_tde 扩展。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/setup.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 230
upstream_source: percona
---

使用 `pg_tde` 加密数据之前，必须启用扩展，并配置 PostgreSQL 在启动时加载它。这确保加密操作所需的钩子和共享内存可用。

> [!NOTE]
> 多租户配置方法见[配置多租户](/zh/percona/how-to/multi-tenant-setup/)。

`pg_tde` 扩展需要额外的共享内存。必须配置 PostgreSQL 在启动时预加载它。

## 1. 配置 shared_preload_libraries {#1-configure-sharedpreloadlibraries}

可以通过两种方式配置 `shared_preload_libraries` 参数：

* 在 `postgresql.conf` 文件中加入以下行：

    ```bash
    shared_preload_libraries = 'pg_tde'
    ```

* 使用 [ALTER SYSTEM](https://www.postgresql.org/docs/current/sql-altersystem.html) 命令。以**超级用户**身份在 `psql` 中运行：

    ```sql
    ALTER SYSTEM SET shared_preload_libraries = 'pg_tde';
    ```

## 2. 重启 PostgreSQL 集群 {#2-restart-the-postgresql-cluster}

重启 `postgresql` 集群，使配置生效。

* Debian 和 Ubuntu：

       ```sh
       sudo systemctl restart postgresql.service
       ```

* RHEL 及衍生发行版：

       ```sh
       sudo systemctl restart postgresql-17
       ```

## 3. 创建扩展 {#3-create-the-extension}

重启 PostgreSQL 后，以**超级用户**或**数据库所有者**身份连接 `psql`，运行：

```sql
CREATE EXTENSION pg_tde;
```

详见 [CREATE EXTENSION](https://www.postgresql.org/docs/current/sql-createextension.html)。

> [!NOTE]
> `pg_tde` 扩展只在当前数据库中创建。要在其他数据库中启用，必须分别在每个数据库中执行该命令。

## 4.（可选）默认启用 pg_tde {#4-optional-enable-pgtde-by-default}

要让所有新建数据库自动启用 `pg_tde`，请修改 `template1` 数据库：

```sql
psql -d template1 -c 'CREATE EXTENSION pg_tde;'
```

> [!NOTE]
> 建议使用外部密钥提供商（KMS）管理加密密钥。配置说明见[下一步](#next-steps)。

## 下一步 {#next-steps}

[配置密钥管理（KMS）](/zh/percona/global-key-provider-configuration/overview/)
