---
title: Vault 配置
linkTitle: HashiCorp Vault
description: 在 Docker 中配置 Vault KV v2、访问策略和令牌，并将其接入 pg_tde。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/global-key-provider-configuration/vault.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 330
upstream_source: percona
---

可以将 HashiCorp Vault 配置为 `pg_tde` 的全局密钥提供商，安全地管理加密密钥。开源版和企业版均受支持。

## 在 Docker 中配置 Vault 与 pg_tde {#configure-vault-with-pgtde-in-docker}

本示例介绍如何使用 Docker 并行运行 HashiCorp Vault 和带有 `pg_tde` 的 Percona PostgreSQL，配置 Vault 策略，并将其接入为 TDE 加密的全局密钥提供商。

> [!NOTE]
> 生产部署应遵循所在组织的安全规范。

### 1. 创建 docker-compose.yaml 文件 {#1-create-the-docker-compose-yaml-file}

以下 `docker-compose.yaml` 示例使用共享秘密卷来运行 Vault 和 PostgreSQL：

> [!DETAILS] docker-compose.yaml 示例文件
>
> ```bash
> version: '3.8'
>
> services:
> vault:
>     image: hashicorp/vault:latest
>     container_name: vault
>     ports:
>     - "8200:8200"
>     volumes:
>     - ./vault-config.hcl:/vault/config/vault-config.hcl
>     - ./vault-data:/vault/data
>     - shared-secrets:/vault/secrets
>     environment:
>     VAULT_ADDR: http://127.0.0.1:8200
>     command: vault server -config=/vault/config/vault-config.hcl
>
> pg:
>     image: percona/percona-distribution-postgresql:17.5-2
>     container_name: pg
>     ports:
>     - "5432:5432"
>     environment:
>     POSTGRES_PASSWORD: secret
>     ENABLE_PG_TDE: "1"
>     volumes:
>     - ./pgdata:/var/lib/postgresql/data
>     - shared-secrets:/etc/postgresql/secrets:ro
>     depends_on:
>     - vault
>
> volumes:
> shared-secrets:
> ```

### 2. 启用 KV v2 秘密引擎 {#2-enable-the-kv-v2-secrets-engine}

在 Vault 容器中，为 `pg_tde` 启用 KV v2 存储引擎：

```bash
vault secrets enable -path=tde -version=2 kv
```

这将创建用于存储加密密钥的 `tde/` 挂载点。

> [!NOTE] Vault 命名空间（企业版）和挂载点
> 使用 **Vault Enterprise 命名空间**时，配置 `pg_tde` 不需要单独提供命名空间参数。
>
> 可以直接在挂载路径中包含命名空间，例如：
>
> ```sql
> SELECT pg_tde_add_global_key_provider_vault_v2(
>     'vault-ns',
>     'https://127.0.0.1:8200',
>     'pgns/tde/data/global-key',
>     '/etc/postgresql/secrets/vault_token.txt',
>     NULL
> );
> ```
>
> 这等价于单独配置命名空间，适用于：
>
> * Vault OSS
> * Vault Enterprise（使用命名空间）

### 3. 为 pg_tde 创建 Vault 策略 {#3-create-a-vault-policy-for-pgtde}

定义 Vault 策略，授予 `pg_tde` 读取、写入和列出密钥的权限。

```bash
vault policy write tde-policy - <<EOF
path "tde/data/*" {
  capabilities = ["read", "create", "update", "list"]
}

path "tde/metadata/*" {
  capabilities = ["read", "list"]
}
EOF
```

该策略允许 `pg_tde`：

- 读取、创建和更新加密密钥。
- 列出和访问 `tde/` 路径的元数据。

> [!TIP]
>
> 如果遇到以下错误：
>
> ```sql
> ERROR: failed to get mount info for "http://vault:8200" at mountpoint ...
> ```
>
> 请确保 Vault 策略中包含以下路径：
>
> ```ini
> path "sys/mounts/*" {
>   capabilities = ["read"]
> }
> ```
>
> 这样 `pg_tde` 才能读取 Vault 的挂载元数据。

### 4. 创建认证方法和令牌 {#4-create-an-authentication-method-and-token}

启用 AppRole 认证方法：

```bash
vault auth enable approle
vault write auth/approle/role/tde-role policies="tde-policy"
```

生成关联 tde-policy 的令牌：

```bash
vault token create -policy="tde-policy"
```

输出示例：

```css
Key                  Value
token                hvs.{secret_code}
token_policies       ["default" "tde-policy"]
```

### 5. 与 PostgreSQL 共享令牌 {#5-share-the-token-with-postgresql}

将生成的令牌复制到共享秘密目录（共享秘密卷），供 PostgreSQL 使用：

```bash
echo "hvs.secret_code" > /vault/secrets/vault_token.txt
```

> [!TIP]
> 在 PostgreSQL 中，可以通过 `/etc/postgresql/secrets/vault_token.txt` 访问此文件。

### 6. 在 PostgreSQL 中将 Vault 注册为全局密钥提供商 {#6-register-vault-as-a-global-key-provider-in-postgresql}

在 PostgreSQL 容器中，执行以下命令将 `pg_tde` 连接到 Vault：

```sql
SELECT pg_tde_add_global_key_provider_vault_v2(
  'vault-provider',
  'http://vault:8200',
  'tde/data/global-key',
  '/etc/postgresql/secrets/vault_token.txt',
  NULL
);
```

### 7. 创建并设置全局主密钥 {#7-create-and-set-the-global-master-key}

创建全局主密钥：

```sql
SELECT pg_tde_create_key_using_global_key_provider(
  'global-master-key',
  'vault-provider'
);
```

然后设置它：

```sql
SELECT pg_tde_set_default_key_using_global_key_provider(
  'global-master-key',
  'vault-provider'
);
```

### 8. 使用示例表测试加密 {#8-test-encryption-with-a-sample-table}

创建示例表：

```sql
CREATE TABLE secure_data (
  id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name TEXT,
  amount NUMERIC(10,2),
  created_at DATE
) USING tde_heap;
```

向表中插入数据：

```sql
INSERT INTO secure_data (name, amount, created_at) VALUES
('Alice', 1234.56, '2025-08-01'),
('Bob', 7890.12, '2025-08-10'),
('Charlie', 345.67, '2025-08-19');
```

查询该表，确认加密正常工作：

```sql
select * from secure_data;
 id |  name   | amount  | created_at
----+---------+---------+------------
  1 | Alice   | 1234.56 | 2025-08-01
  2 | Bob     | 7890.12 | 2025-08-10
  3 | Charlie |  345.67 | 2025-08-19
(3 rows)
```

## 全局密钥提供商使用示例 {#example-global-key-provider-usage}

```sql
SELECT pg_tde_add_global_key_provider_vault_v2(
    'provider-name',
    'url',
    'mount',
    'secret_token_path',
    'ca_path'
);
```

## 参数说明 {#parameter-descriptions}

* `provider-name`：用于标识此密钥提供商的名称。
* `secret_token_path`：包含访问令牌的文件路径，该令牌必须具有相应挂载点的读写权限。
* `url`：Vault 服务器的 URL。
* `mount`：keyring 存储密钥的挂载点。
* [可选] `ca_path`：用于 SSL 验证的 CA 文件路径。

以下示例仅用于测试。生产环境应使用安全令牌，并正确验证 SSL：

```sql
SELECT pg_tde_add_global_key_provider_vault_v2(
    'my-vault',
    'https://vault.vault.svc.cluster.local:8200',
    'secret/data',
    '/path/to/token_file',
    '/path/to/ca_cert.pem'
);
```

相关函数详见[函数参考](/zh/percona/functions/)。

## 所需权限 {#required-permissions}

PostgreSQL 实例需要以下 Vault API 权限来管理和读取加密密钥：

* `sys/mounts/<mount>/*`：**read** 权限。
* `<mount>/data/*`：**create**、**read** 权限。
* `<mount>/metadata/*`：**list** 权限。

> [!NOTE]
> Vault 权限的更多信息见[相关文档](https://developer.hashicorp.com/vault/docs/concepts/policies)。

## 下一步 {#next-steps}

[全局主密钥配置](/zh/percona/global-key-provider-configuration/set-principal-key/)
