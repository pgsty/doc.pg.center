---
title: 函数
linkTitle: SQL 函数
description: pg_tde SQL 函数参考：密钥提供商、主密钥、加密状态和密钥验证。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/functions.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 640
upstream_source: percona
---

> [!NOTE] 本站勘误
> 参数名及密钥作用域已按固定提交的源码修正。 详见[勘误记录](/zh/percona/site/errata/)。


`pg_tde` 扩展提供一组函数，用于管理其运行的各个方面。

> [!NOTE]
> 执行以下命令时，如果未报错，说明操作成功。

## 密钥提供商管理 {#key-provider-management}

密钥提供商是负责管理加密密钥的系统或服务。`pg_tde` 支持的提供商详见[密钥管理概览](/zh/percona/global-key-provider-configuration/overview/)。

密钥提供商管理包括：

* [添加新密钥提供商](#add-a-key-provider)
* [修改现有密钥提供商](#change-an-existing-provider)
* [删除密钥提供商](#delete-a-provider)
* [列出密钥提供商](#list-key-providers)

### 添加密钥提供商 {#add-a-key-provider}

每种提供商类型都有对应的函数，用于添加新提供商。

添加提供商有两类函数：一类添加到当前数据库，另一类添加到全局作用域。

* `pg_tde_add_database_key_provider_<type>('provider-name', <provider specific parameters>)`
* `pg_tde_add_global_key_provider_<type>('provider-name', <provider specific parameters>)`

新提供商的名称必须在其作用域内唯一。但数据库本地提供商可以与全局提供商同名。

### 修改现有提供商 {#change-an-existing-provider}

每种提供商类型都有对应的函数，用于修改现有提供商。

修改提供商有两类函数：一类修改当前数据库中的提供商，另一类修改全局作用域中的提供商。

* `pg_tde_change_database_key_provider_<type>('provider-name', <provider specific parameters>)`
* `pg_tde_change_global_key_provider_<type>('provider-name', <provider specific parameters>)`

修改时，引用的名称必须已经存在于数据库本地或全局作用域。

`change` 函数与 `add` 函数需要相同的参数。除名称不可更改外，其他参数的设置都会被覆盖。

不同实现所需的专用参数不同，详见相应小节。

> [!NOTE]
> 更新后的提供商必须能够获取与原配置相同的主密钥。
> 如果新配置无法访问已有密钥，加密数据和备份将无法读取。

#### 添加或修改 Vault 提供商 {#add-or-modify-vault-providers}

Vault 提供商连接 HashiCorp Vault 或 OpenBao 服务器，将密钥保存在版本 2 的键值存储中。

使用以下函数添加 Vault 提供商：

```sql
SELECT pg_tde_add_database_key_provider_vault_v2(
  'provider-name',
  'url',
  'mount',
  'secret_token_path',
  'ca_path'
);

SELECT pg_tde_add_global_key_provider_vault_v2(
  'provider-name',
  'url',
  'mount',
  'secret_token_path',
  'ca_path'
);

SELECT pg_tde_add_database_key_provider_vault_v2(
  'provider-name',
  'url',
  'mount',
  'secret_token_path',
  'ca_path',
  'namespace'
);

SELECT pg_tde_add_global_key_provider_vault_v2(
  'provider-name',
  'url',
  'mount',
  'secret_token_path',
  'ca_path',
  'namespace'
);
```

使用以下函数修改 Vault 提供商：

```sql
SELECT pg_tde_change_database_key_provider_vault_v2(
  'provider-name',
  'url',
  'mount',
  'secret_token_path',
  'ca_path'
);

SELECT pg_tde_change_global_key_provider_vault_v2(
  'provider-name',
  'url',
  'mount',
  'secret_token_path',
  'ca_path'
);
SELECT pg_tde_change_database_key_provider_vault_v2(
  'provider-name',
  'url',
  'mount',
  'secret_token_path',
  'ca_path',
  'namespace'
);

SELECT pg_tde_change_global_key_provider_vault_v2(
  'provider-name',
  'url',
  'mount',
  'secret_token_path',
  'ca_path',
  'namespace'
);
```

其中：

* `provider-name`：密钥提供商的名称。
* `url`：Vault 服务器的 URL。
* `mount`：Vault 服务器上用于保存密钥的挂载点。
* `secret_token_path`：包含访问令牌的文件路径，该令牌必须具有上述挂载点的读写权限。
* **[可选]** `ca_path`：用于 SSL 验证的 CA 文件路径。
* **[命名空间]** `namespace`：使用 [Vault 命名空间](https://developer.hashicorp.com/vault/docs/enterprise/namespaces)时的命名空间路径。

#### 添加或修改 KMIP 提供商 {#add-or-modify-kmip-providers}

KMIP 提供商使用远程 KMIP 服务器。

使用以下函数添加 KMIP 提供商：

```sql
SELECT pg_tde_add_database_key_provider_kmip(
  'provider-name',
  'kmip-addr',
  port,
  '/path_to/client_cert.pem',
  '/path_to/client_key.pem',
  '/path_to/server_certificate.pem'
);

SELECT pg_tde_add_global_key_provider_kmip(
  'provider-name',
  'kmip-addr',
  port,
  '/path_to/client_certificate.pem',
  '/path_to/client_key.pem',
  '/path_to/server_certificate.pem'
);
```

使用以下函数修改 KMIP 提供商：

```sql
SELECT pg_tde_change_database_key_provider_kmip(
  'provider-name',
  'kmip-addr',
  port,
  '/path_to/client_cert.pem',
  '/path_to/client_key.pem',
  '/path_to/server_certificate.pem'
);

SELECT pg_tde_change_global_key_provider_kmip(
  'provider-name',
  'kmip-addr',
  port,
  '/path_to/client_certificate.pem',
  '/path_to/client_key.pem',
  '/path_to/server_certificate.pem'
);
```

其中：

* `provider-name`：提供商名称。
* `kmip-addr`：KMIP 服务器的 IP 地址或域名。
* `port`：与 KMIP 服务器通信的端口。大多数 KMIP 服务器使用 5696。
* `server-certificate`：KMIP 服务器证书文件的路径。
* `client-certificate`：客户端证书的路径。
* `client-key`：客户端密钥的路径。

> [!NOTE]
> 指定的访问参数必须具有在服务器上读写密钥的权限。

### 添加或修改本地密钥文件提供商 {#add-or-modify-local-key-file-providers}

此提供商使用本地密钥文件管理数据库密钥。

该功能面向开发或快速测试，将密钥以未加密形式保存在指定的数据文件中。

> [!IMPORTANT]
> **不建议**在生产环境使用本地密钥文件提供商，因为它们不具备外部密钥管理系统的安全性和可管理性。

添加本地密钥文件提供商：

```sql
SELECT pg_tde_add_database_key_provider_file(
  'provider-name',
  '/path/to/the/key/provider/data.file'
);

SELECT pg_tde_add_global_key_provider_file(
  'provider-name',
  '/path/to/the/key/provider/data.file'
);
```

修改本地密钥文件提供商：

```sql
SELECT pg_tde_change_database_key_provider_file(
  'provider-name',
  '/path/to/the/key/provider/data.file'
);

SELECT pg_tde_change_global_key_provider_file(
  'provider-name',
  '/path/to/the/key/provider/data.file'
);
```

其中：

* `provider-name`：提供商名称，可以任意指定，用于标识该提供商。
* `/path/to/the/key/provider/data.file`：密钥提供商文件的路径。

### 删除提供商 {#delete-a-provider}

以下函数删除当前数据库或全局作用域中的现有提供商：

* `pg_tde_delete_database_key_provider('provider-name')`
* `pg_tde_delete_global_key_provider('provider-name')`

只能删除当前未使用的密钥提供商。如果当前主密钥正在使用待删除的提供商，函数会返回错误。

通过 GUC 参数 `pg_tde.inherit_global_providers` 启用了全局提供商时，只有全局提供商未在任何地方（包括任何数据库）使用，才能将其删除。如果有数据库正在使用它，则返回错误。

### 列出密钥提供商 {#list-key-providers}

以下函数列出当前数据库或全局作用域中所有提供商的详情，包括全部配置值：

* `pg_tde_list_all_database_key_providers()`
* `pg_tde_list_all_global_key_providers()`

## 主密钥管理 {#principal-key-management}

这些函数可以在指定提供商中创建主密钥，并将密钥用于当前数据库、全局或默认等特定作用域；也可以让特定作用域改用另一个已有密钥。

主密钥以函数中指定的名称保存在提供商中。例如，使用 Vault 提供商创建名为 "foo" 的密钥后，就能在 Vault 服务器的指定挂载点看到名为 "foo" 的密钥。

### pg_tde_create_key_using_database_key_provider {#pgtdecreatekeyusingdatabasekeyprovider}

通过指定名称的数据库本地密钥提供商创建主密钥。之后使用 [`pg_tde_set_key_using_database_key_provider()`](#pgtdesetkeyusingdatabasekeyprovider) 启用该密钥。

```sql
SELECT pg_tde_create_key_using_database_key_provider(
  'key-name',
  'provider-name'
);
```

### pg_tde_create_key_using_global_key_provider {#pgtdecreatekeyusingglobalkeyprovider}

在指定名称的全局密钥提供商中创建主密钥。之后通过 `pg_tde_set_*` 系列函数启用该密钥。

```sql
SELECT pg_tde_create_key_using_global_key_provider(
  'key-name',
  'provider-name'
);
```

### pg_tde_set_key_using_database_key_provider {#pgtdesetkeyusingdatabasekeyprovider}

使用指定的本地密钥提供商，为**当前**数据库设置主密钥，同时轮换内部加密密钥，使其使用指定的主密钥。

此函数通常用于通过本地密钥提供商实现按数据库加密的场景。

```sql
SELECT pg_tde_set_key_using_database_key_provider(
  'key-name',
  'provider-name'
);
```

### pg_tde_set_key_using_global_key_provider {#pgtdesetkeyusingglobalkeyprovider}

使用指定的全局密钥提供商和密钥名称，为**当前数据库**设置或轮换主密钥。WAL 加密使用 `pg_tde_set_server_key_using_global_key_provider`。

```sql
SELECT pg_tde_set_key_using_global_key_provider(
  'key-name',
  'provider-name'
);
```

### pg_tde_set_server_key_using_global_key_provider {#pgtdesetserverkeyusingglobalkeyprovider}

使用指定的全局密钥提供商设置或轮换服务器主密钥。使用此函数为 WAL 加密设置主密钥。

```sql
SELECT pg_tde_set_server_key_using_global_key_provider(
  'key-name',
  'provider-name'
);
```

### pg_tde_set_default_key_using_global_key_provider {#pgtdesetdefaultkeyusingglobalkeyprovider}

使用指定的全局密钥提供商设置或轮换服务器默认主密钥。

未单独配置密钥提供商和密钥的数据库，会自动将默认密钥作为主密钥。

```sql
SELECT pg_tde_set_default_key_using_global_key_provider(
  'key-name',
  'provider-name'
);
```

### pg_tde_delete_key {#pgtdedeletekey}

取消当前数据库的主密钥设置。如果当前数据库存在加密表且未配置默认主密钥，则报错。如果存在加密表但也有默认主密钥，则使用默认密钥加密内部密钥。

```sql
SELECT pg_tde_delete_key();
```

### pg_tde_delete_default_key {#pgtdedeletedefaultkey}

取消默认主密钥设置。只有没有数据库使用默认主密钥时，才允许执行。

```sql
SELECT pg_tde_delete_default_key();
```

## 检查加密状态 {#encryption-status-check}

### pg_tde_is_encrypted {#pgtdeisencrypted}

判断关系是否使用 `pg_tde` 扩展加密。对于没有存储的关系，例如视图、外部表、分区表和分区索引，返回 `NULL`。

要验证表已加密，运行：

```sql
SELECT pg_tde_is_encrypted(
  'table_name'
);
```

也可以检查自定义模式中的表是否加密，按以下方式传入模式名：

```sql
SELECT pg_tde_is_encrypted(
  'schema.table_name'
);
```

此函数还可用于验证索引和序列是否加密。

### pg_tde_key_info {#pgtdekeyinfo}

如果当前数据库存在主密钥，显示其信息。

```sql
SELECT pg_tde_key_info();
```

### pg_tde_server_key_info {#pgtdeserverkeyinfo}

如果服务器作用域存在主密钥，显示其信息。

```sql
SELECT pg_tde_server_key_info();
```

### pg_tde_default_key_info {#pgtdedefaultkeyinfo}

如果存在默认主密钥，显示其信息。

```sql
SELECT pg_tde_default_key_info();
```

### pg_tde_verify_key {#pgtdeverifykey}

检查当前数据库的加密配置是否正常，包括：

* 已配置密钥提供商。
* 可以通过指定配置访问提供商。
* 数据库存在主密钥。
* 可以从远程提供商获取主密钥。
* 提供商返回的主密钥与服务器内存中缓存的密钥相同。

任一检查失败都会报错。

```sql
SELECT pg_tde_verify_key();
```

### pg_tde_verify_server_key {#pgtdeverifyserverkey}

检查服务器作用域的加密配置是否正常，包括：

* 已配置密钥提供商。
* 可以通过指定配置访问提供商。
* 全局作用域存在主密钥。
* 可以从远程提供商获取主密钥。
* 提供商返回的主密钥与服务器内存中缓存的密钥相同。

任一检查失败都会报错。

```sql
SELECT pg_tde_verify_server_key();
```

### pg_tde_verify_default_key {#pgtdeverifydefaultkey}

检查默认密钥是否配置正确，包括：

* 已配置密钥提供商。
* 可以通过指定配置访问提供商。
* 存在可供任意作用域使用的主密钥。
* 可以从远程提供商获取主密钥。
* 提供商返回的主密钥与服务器内存中缓存的密钥相同。

任一检查失败都会报错。

```sql
SELECT pg_tde_verify_default_key();
```
