---
title: 配置 WAL 加密
linkTitle: WAL 加密
description: 为 WAL 配置默认或专用服务器主密钥，并满足加密 WAL 的归档与恢复要求。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/wal-encryption.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 510
upstream_source: percona
---

WAL 加密需要一个主密钥。可以通过以下任一方式满足这一要求：

> [!WARNING] WAL 归档和恢复要求
>
> 启用 WAL 加密的部署必须同时使用以下两个工具完成 WAL 归档和恢复，否则不受支持：
>
> * 在 `archive_command` 中使用 [`pg_tde_archive_decrypt`](/zh/percona/command-line-tools/pg-tde-archive-decrypt/)
> * 在 `restore_command` 中使用 [`pg_tde_restore_encrypt`](/zh/percona/command-line-tools/pg-tde-restore-encrypt/)
>
> 如果使用 pgBackRest，还必须关闭其异步归档、WAL 头部检查和页面校验和验证。在适用的 pgBackRest 配置节中加入：
>
> ```ini
> archive-async=n
> archive-header-check=n
> checksum-page=n
> ```

## 方式一：使用默认主密钥 {#option-1-use-the-default-principal-key}

如果服务器已配置默认主密钥，WAL 加密会自动使用它，无需再配置服务器密钥。

如果尚未配置默认主密钥，参阅[默认主密钥配置](/zh/percona/global-key-provider-configuration/set-principal-key/)。

## 方式二：为 WAL 配置专用服务器主密钥 {#option-2-configure-a-dedicated-server-principal-key-for-wal}

> [!NOTE]
> `pg_tde` WAL 加密所支持工具的完整列表见 [pg_tde 的限制](/zh/percona/index/tde-limitations/)。

1. 如果尚未创建 `pg_tde` 扩展，先创建它：

    ```sql
    CREATE EXTENSION IF NOT EXISTS pg_tde;
    ```

2. 配置全局密钥提供商。

    为 WAL 加密创建服务器主密钥之前，必须先配置全局密钥提供商。各类提供商的详细配置方法见[密钥管理概览](/zh/percona/global-key-provider-configuration/overview/)。

3. 使用全局密钥提供商创建服务器主密钥。

    服务器密钥（也称为主密钥）由 PostgreSQL 用于加密 WAL 数据。详细步骤见 [pg_tde_create_key_using_global_key_provider](/zh/percona/functions/#pgtdecreatekeyusingglobalkeyprovider)。

4. 设置服务器主密钥。

    此步骤将刚创建的服务器主密钥设为 PostgreSQL 当前用于 WAL 加密的密钥。详细步骤见 [pg_tde_set_server_key_using_global_key_provider](/zh/percona/functions/#pgtdesetserverkeyusingglobalkeyprovider)。

5. 使用 `ALTER SYSTEM` 启用 WAL 加密。运行此命令需要超级用户权限：

    ```sql
    ALTER SYSTEM SET pg_tde.wal_encrypt = on;
    ```

6. 重启服务器，使变更生效。

    * Debian 和 Ubuntu：

    ```sh
    sudo systemctl restart postgresql
    ```

    * RHEL 及衍生发行版：

    ```sh
    sudo systemctl restart postgresql-<version>
    ```

7.（可选）验证 WAL 加密已启用：

    ```sql
    SHOW pg_tde.wal_encrypt;
    ```

此后，无论表本身是否加密，其 WAL 文件都会开始加密。

关于架构、参数和函数的更多信息，参阅[技术参考](/zh/percona/advanced-topics/tech-reference/)。

需要根据基础设施调整配置时，可以[联系 Percona 支持](/zh/percona/get-help/)。
