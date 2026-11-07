---
title: 配置多租户
linkTitle: 配置多租户
description: 为不同数据库配置独立密钥与提供商，实现 pg_tde 多租户加密隔离。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/how-to/multi-tenant-setup.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 540
upstream_source: percona
---

以下步骤介绍如何使用 `pg_tde` 配置多租户。多租户允许不同数据库使用不同密钥加密，提供精细的数据控制，并允许为每个数据库设置不同的安全策略和访问控制，确保只有相应数据库的授权用户能够访问数据。

如果不需要多租户，使用全局密钥提供商即可。配置步骤见[配置 pg_tde](/zh/percona/setup/)。

启用 WAL 加密的方法见[配置 WAL 加密](/zh/percona/wal-encryption/)。

## 注意事项 {#considerations}

可以使用外部密钥提供商管理加密密钥。推荐使用密钥管理存储（KMS），详见[配置密钥管理（KMS）](/zh/percona/global-key-provider-configuration/overview/)。

> [!NOTE]
> 执行以下命令时，如果未报错，说明操作成功。

## 启用扩展 {#enable-extension}

在启动时加载 `pg_tde`。该扩展需要额外共享内存，因此应将 `pg_tde` 加入 `shared_preload_libraries`，然后重启 `postgresql` 集群。

1. 在 `psql` 中使用 [ALTER SYSTEM](https://www.postgresql.org/docs/current/sql-altersystem.html) 修改 `shared_preload_libraries`。此操作需要超级用户权限。

    ```sql
    ALTER SYSTEM SET shared_preload_libraries = 'pg_tde';
    ```

2. 启动或重启 `postgresql` 集群，使更改生效。

    * Debian 和 Ubuntu：

       ```sh
       sudo systemctl restart postgresql-17
       ```

    * RHEL 及衍生发行版：

       ```sh
       sudo systemctl restart postgresql-17
       ```

3. 使用 [CREATE EXTENSION](https://www.postgresql.org/docs/current/sql-createextension.html) 创建扩展，需要超级用户或数据库所有者权限。以数据库超级用户身份连接 `psql` 并执行：

    ```sql
    CREATE EXTENSION pg_tde;
    ```

    `pg_tde` 扩展在当前数据库中创建。要在其他数据库中启用数据加密，必须分别对它们执行 `CREATE EXTENSION`。

    > [!TIP]
    >
    > 可以让每个新数据库自动启用 `pg_tde`。按以下方式修改模板数据库 `template1`：
    >
    > ```sh
    > psql -d template1 -c 'CREATE EXTENSION pg_tde;'
    > ```

## 配置密钥提供商 {#key-provider-configuration}

必须对每个创建了扩展的数据库执行这些步骤。更多配置说明见[配置密钥管理（KMS）](/zh/percona/global-key-provider-configuration/overview/)。

1. 配置密钥提供商。

    {{< tabs group="with-kmip-server-with-hashicorp-vault-with-a-keyring-file-not-recommended" >}}
    {{< tab label="KMIP 服务器" value="with-kmip-server" >}}

    KMIP 服务器的配置不在本文范围内。

    确保已取得 KMIP 服务器的根证书和客户端密钥对。客户端密钥必须有权在服务器上创建和读取密钥。可参阅 [HashiCorp Vault Enterprise KMIP Secrets Engine 配置指南](https://developer.hashicorp.com/vault/tutorials/enterprise/kmip-engine)。

    测试时可以使用 Eviden KMS 服务器配置所需证书。使用实际 KMIP 服务器时，应取得由密钥管理设备签发的有效证书。

    ```sql
    SELECT pg_tde_add_database_key_provider_kmip(
      'provider-name',
      'kmip-addr', 
      `port`, 
      '/path_to/client_cert.pem', 
      '/path_to/client_key.pem', 
      '/path_to/server_certificate.pem'
    );
    ```

    其中：

    * `provider-name`：提供商名称，可以任意指定，用于标识该提供商。
    * `kmip-addr`：KMIP 服务器的 IP 地址或域名。
    * `port`：通信端口，通常为 5696。
    * `server-certificate`：KMIP 服务器证书文件的路径。
    * `client-cert`：客户端证书路径。
    * `client-key`：客户端密钥路径。

    **警告：以下示例仅用于测试。**

    ```sql
    SELECT pg_tde_add_database_key_provider_kmip(
        'kmip', 
        '127.0.0.1', 
        5696, 
        '/tmp/client_cert_jane_doe.pem', 
        '/tmp/client_key_jane_doe.pem', 
        '/tmp/server_certificate.pem'
    );
    ```

    {{< /tab >}}
    {{< tab label="HashiCorp Vault" value="with-hashicorp-vault" >}}

    Vault 服务器的配置不在本文范围内。

    ```sql
    SELECT pg_tde_add_database_key_provider_vault_v2(
        'provider-name', 
        'url', 
        'mount', 
        'secret_token_path', 
        'ca_path'
    );
    ```

    其中：

    * `url`：Vault 服务器的 URL。
    * `mount`：keyring 存储密钥的挂载点。
    * `secret_token_path`：包含访问令牌的文件路径，该令牌必须具有上述挂载点的读写权限。
    * [可选] `ca_path`：用于 SSL 验证的 CA 文件路径。

    **警告：以下示例仅用于测试。**

    ```sql
    SELECT pg_tde_add_database_key_provider_file_vault_v2(
        'my-vault',
        'http://vault.vault.svc.cluster.local:8200',
        'secret/data',
        'hvs.zPuyktykA...example...ewUEnIRVaKoBzs2', 
        NULL
    );
    ```

    {{< /tab >}}
    {{< tab label="Keyring 文件（不推荐）" value="with-a-keyring-file-not-recommended" >}}

    此配置用于开发环境，将密钥以未加密形式保存在指定的数据文件中。

    ```sql
    SELECT pg_tde_add_database_key_provider_file(
        'provider-name', 
        '/path/to/the/keyring/data.file'
    );
    ```

    {{< /tab >}}
    {{< /tabs >}}

    **警告：以下示例仅用于测试。**

        ```sql
        SELECT pg_tde_add_database_key_provider_file(
            'file-keyring', 
            '/tmp/pg_tde_test_local_keyring.per'
        );
        ```

2. 创建密钥。

    ```sql
    SELECT pg_tde_create_key_using_database_key_provider(
        'name-of-the-key', 
        'provider-name'
    );
    ```

    其中：

    * `name-of-the-key`：主密钥名称，用于标识该密钥。
    * `provider-name`：先前添加的密钥提供商名称。主密钥与此提供商关联，并在其中存储和读取。

    **警告：以下示例仅用于测试。**

    ```sql
    SELECT pg_tde_create_key_using_database_key_provider(
        'test-db-master-key', 
        'file-vault'
    );
    ```

    > [!NOTE]
    > 密钥自动生成。

3. 将该密钥用作主密钥。

    ```sql
    SELECT pg_tde_set_key_using_database_key_provider(
        'name-of-the-key', 
        'provider-name'
    );
    ```

    其中：

    * `name-of-the-key`：主密钥名称，用于标识该密钥。
    * `provider-name`：先前添加的密钥提供商名称，主密钥将与它关联。

    **警告：以下示例仅用于测试。**

    ```sql
    SELECT pg_tde_set_key_using_database_key_provider(
        'test-db-master-key',
        'file-vault'
    );
    ```
