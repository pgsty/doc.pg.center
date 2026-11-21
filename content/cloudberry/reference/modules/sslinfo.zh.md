---
title: sslinfo
description: sslinfo 提供当前客户端连接 Apache Cloudberry 时提交的 SSL 证书信息。
weight: 240
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/sslinfo.md
---

`sslinfo` 模块提供当前客户端连接 Apache Cloudberry 时提交的 SSL 证书信息。如果当前连接未使用 SSL，此模块的大多数函数返回 `NULL`。

Apache Cloudberry 的 `sslinfo` 模块与 PostgreSQL 的 `sslinfo` 模块等价。函数报告的是客户端到 Coordinator 的连接信息。

## 安装并注册模块 {#install-and-register-the-module}

`sslinfo` 不属于 Apache Cloudberry 的默认构建目标（`make` 和 `make install`），且只有在配置 Apache Cloudberry 时启用了 OpenSSL 支持，才能构建它（`--with-ssl=openssl`，或旧写法 `--with-openssl`）。如果 `CREATE EXTENSION` 报告该扩展不可用，请使用配置当前安装版本时所用的 Apache Cloudberry 源码树，构建并安装此模块：

```shell
make -C contrib/sslinfo install
```

集群的每台主机（Coordinator、Standby Coordinator 及所有 Segment 主机）上都必须有模块文件。`make install-world` 也会安装此模块。

然后在每个需要使用它的数据库中注册扩展：

```sql
CREATE EXTENSION sslinfo;
```

## 函数 {#functions}

| 函数 | 说明 |
|----------|-------------|
| `ssl_is_used() returns boolean` | 当前连接使用 SSL 时返回 `true`。 |
| `ssl_version() returns text` | 返回 SSL 连接使用的协议名称。 |
| `ssl_cipher() returns text` | 返回 SSL 连接使用的密码算法名称。 |
| `ssl_client_cert_present() returns boolean` | 客户端提交了有效的 SSL 证书时返回 `true`。 |
| `ssl_client_serial() returns numeric` | 返回客户端证书的序列号。 |
| `ssl_client_dn() returns text` | 返回客户端证书的完整主体。 |
| `ssl_issuer_dn() returns text` | 返回客户端证书的完整颁发者名称。 |
| `ssl_client_dn_field(fieldname text) returns text` | 返回客户端证书主体的一个字段。 |
| `ssl_issuer_field(fieldname text) returns text` | 返回客户端证书颁发者的一个字段。 |
| `ssl_extension_info() returns setof record` | 返回客户端证书中每个扩展的名称、值和关键性。 |

## 示例 {#example}

```sql
SELECT ssl_is_used(), ssl_version(), ssl_cipher();
SELECT ssl_client_dn_field('CN');
```

## 模块文档 {#module-documentation}

此模块各个函数的详细信息，参见 PostgreSQL 文档中的 [sslinfo](https://www.postgresql.org/docs/14/sslinfo.html)。
