---
title: KMIP 配置
linkTitle: KMIP 配置
description: 配置 KMIP 全局密钥提供商所需的证书、连接参数和使用示例。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/global-key-provider-configuration/kmip-server.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 350
upstream_source: percona
---

> [!NOTE] 本站勘误
> 本页保留了早期对 Vault KMIP 的验证状态说明；2.2.2 发布说明已明确宣布支持 Vault Enterprise KMIP，具体版本状态请以对应发布说明为准。 详见[勘误记录](/zh/percona/site/errata/)。


要让 `pg_tde` 使用密钥管理互操作协议（KMIP）服务器，必须将其配置为全局密钥提供商。配置完成后，`pg_tde` 可以从集中式密钥管理设备安全地获取和管理加密密钥。

> [!IMPORTANT]
> 将 HashiCorp Vault 用作 KMIP 服务器尚不是经过验证的 `pg_tde` 部署方式，不建议用于生产环境。
>
> 使用 Vault 管理密钥时，请采用 [KV v2 集成方式](/zh/percona/global-key-provider-configuration/vault/)。

> [!NOTE]
> 你需要 KMIP 服务器的根证书，以及有权在服务器上创建和读取密钥的客户端密钥与证书对。

测试时可以使用 Eviden KMS 服务器，以便生成证书并验证基本 KMIP 行为。使用生产级 KMIP 服务器时，请从密钥管理设备获取有效、受信任的证书。

## 使用示例 {#example-usage}

```sql
SELECT pg_tde_add_global_key_provider_kmip(
    'provider-name',
    'kmip-IP', 
    `port`,
    '/path_to/server_certificate.pem', 
    '/path_to/client_cert.pem',
    '/path_to/client_key.pem'
);
```

## 参数说明 {#parameter-descriptions}

* `provider-name`：提供商名称，可以任意指定，用于标识该提供商。
* `kmip-IP`：KMIP 服务器的 IP 地址或域名。
* `port`：与 KMIP 服务器通信的端口，通常为 5696。
* `server-certificate`：KMIP 服务器证书文件的路径。
* `client_cert`：客户端证书的路径。
* `client_key`：客户端密钥的路径。

以下示例仅用于测试。

```sql
SELECT pg_tde_add_global_key_provider_kmip(
    'kmip','127.0.0.1', 
    5696, 
    '/tmp/server_certificate.pem', 
    '/tmp/client_cert_jane_doe.pem',
    '/tmp/client_key_jane_doe.pem'
);
```

相关函数的更多信息见：

[Percona pg_tde 函数参考](/zh/percona/functions/)

## 下一步 {#next-steps}

[全局主密钥配置](/zh/percona/global-key-provider-configuration/set-principal-key/)
