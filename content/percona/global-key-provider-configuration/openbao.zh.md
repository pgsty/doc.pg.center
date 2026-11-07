---
title: 使用 OpenBao 作为密钥提供商
linkTitle: OpenBao
description: 将 OpenBao 注册为全局密钥提供商，并配置令牌、挂载点、CA 和命名空间。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/global-key-provider-configuration/openbao.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 340
upstream_source: percona
---

可以将 OpenBao 配置为 `pg_tde` 的全局密钥提供商，安全地管理加密密钥。

> [!NOTE]
> 本指南假定 OpenBao 服务器已配置完成且可以访问。OpenBao 的配置不在本文范围内，详见 [OpenBao 官方文档](https://openbao.org/docs/)。

## 使用示例 {#example-usage}

将 OpenBao 服务器注册为全局密钥提供商：

```sql
SELECT pg_tde_add_global_key_provider_vault_v2(
    'provider-name',
    'url',
    'mount',
    'secret_token_path',
    'ca_path',
    'namespace'
);
```

## 参数说明 {#parameter-descriptions}

* `provider-name`：用于标识此密钥提供商的名称。
* `secret_token_path`：包含访问令牌的文件路径，该令牌必须具有相应挂载点的读写权限。
* `url`：OpenBao 服务器的 URL。
* `mount`：keyring 存储密钥的挂载点。
* [可选] `ca_path`：用于 SSL 验证的 CA 文件路径。
* [可选] `namespace`：OpenBao 服务器中的命名空间。详见 [OpenBao 的命名空间支持](https://openbao.org/blog/namespaces-announcement/)。（可以在不提供 ca_path 时使用命名空间，此时请将 ca_path 设为 NULL。）

以下示例仅用于测试。生产环境应使用安全令牌，并正确验证 SSL：

```sql
SELECT pg_tde_add_global_key_provider_vault_v2(
    'my-openbao-provider',
    'https://openbao.example.com:8200',
    'secret/data',
    '/path/to/token_file',
    '/path/to/ca_cert.pem'
);
```

相关函数的更多信息见：

[Percona pg_tde 函数参考](/zh/percona/functions/)

## 下一步 {#next-steps}

[全局主密钥配置](/zh/percona/global-key-provider-configuration/set-principal-key/)
