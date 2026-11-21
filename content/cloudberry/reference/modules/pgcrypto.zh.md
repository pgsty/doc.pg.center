---
title: pgcrypto
description: pgcrypto 提供通用哈希、密码哈希、PGP 加密、原始加密和随机数据生成等密码学函数。
weight: 210
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/pgcrypto.md
---

`pgcrypto` 模块提供密码学函数，包括通用哈希、密码哈希、PGP 加密、原始加密和随机数据生成。利用这些函数，可以加密存储某些数据列。没有加密密钥的人无法读取加密存储的数据，也无法直接从磁盘读取其明文。

> [!NOTE]
> `pgcrypto` 函数在数据库服务器内部运行，这意味着 `pgcrypto` 与客户端应用之间传输的所有数据和密码都是明文。为提高安全性，还应在客户端与 Apache Cloudberry Coordinator 之间使用 SSL 连接。

## 安装并注册模块 {#install-and-register-the-module}

Apache Cloudberry 的默认构建会构建并安装 `pgcrypto`。在每个需要使用它的数据库中注册扩展：

```sql
CREATE EXTENSION pgcrypto;
```

## 函数 {#functions}

| 类别 | 函数 |
|-------|-----------|
| 通用哈希 | `digest()`, `hmac()` |
| 密码哈希 | `crypt()`, `gen_salt()` |
| PGP 加密 | `pgp_sym_encrypt()`, `pgp_sym_encrypt_bytea()`, `pgp_sym_decrypt()`, `pgp_sym_decrypt_bytea()`, `pgp_pub_encrypt()`, `pgp_pub_encrypt_bytea()`, `pgp_pub_decrypt()`, `pgp_pub_decrypt_bytea()`, `pgp_key_id()`, `armor()`, `dearmor()`, `pgp_armor_headers()` |
| 原始加密 | `encrypt()`, `decrypt()`, `encrypt_iv()`, `decrypt_iv()` |
| 随机数据 | `gen_random_bytes()`, `gen_random_uuid()` |

示例：

```sql
SELECT digest('santa claus', 'sha256');
SELECT pgp_sym_decrypt(pgp_sym_encrypt('santa clause', 'mypass', 'cipher-algo=aes256'), 'mypass');
```

除 PostgreSQL 模块的密码算法外，原始加密函数还接受 SM4 密码算法 `sm4-ecb` 和 `sm4-cbc`，`digest()` 和 `hmac()` 还接受 `sm3` 摘要。在使用 OpenSSL 的构建中，只有配置 Apache Cloudberry 时指定了 `--enable-openssl-redirect`，SM4 密码算法才可用；否则会报错 `Cannot use "sm4-ecb": No such cipher algorithm`。如果 OpenSSL 库提供 `sm3` 摘要，就可以使用它。

## FIPS 模式 {#fips-mode}

此模块定义配置参数 `pgcrypto.fips`，将 `pgcrypto` 限制在适用于 FIPS 140-2 模式的有限功能范围内。此参数为布尔值，默认值为 `off`，只有超级用户可以更改。

FIPS 模式要求集群所有主机上的 OpenSSL 库都提供 FIPS 模块。如果编译 Apache Cloudberry 时使用的 OpenSSL 版本不支持 FIPS，开启此参数会报错 `FIPS enabled OpenSSL is required for strict FIPS mode`。不含 OpenSSL 的构建不支持 FIPS 模式。

当 `pgcrypto.fips` 为 `on` 时：

- OpenSSL 库中的 FIPS 模式开启。
- 不允许使用 `crypt()` 和 `gen_salt()`。
- 不允许使用原始加密函数（`encrypt()`、`decrypt()`、`encrypt_iv()` 和 `decrypt_iv()`）。
- `digest()` 和 `hmac()` 拒绝 `md5` 等未经 FIPS 认可的摘要，错误以 `Cannot use "md5"` 开头。
- PGP 函数也不可用。它们只识别 `3des`、`aes128`（`aes`）、`aes192` 和 `aes256` 密码算法名称，以及 `sha1`、`sha256`、`sha384` 和 `sha512` 摘要名称；其他名称（如 `bf`）会被拒绝，报错 `Unsupported cipher algorithm`。使用已识别密码算法进行加解密时，随后仍会报错 `requested functionality not allowed in FIPS mode`，因为 `pgcrypto` 通过 FIPS 模式不允许的 OpenSSL 接口访问这些密码算法。

调用 `crypt()`、`gen_salt()` 或原始加密函数时，都会报错 `requested functionality not allowed in FIPS mode`。

### 启用 FIPS 模式 {#enable-fips-mode}

1. 将 `pgcrypto` 库加入 `shared_preload_libraries`，并重启集群。这使服务器在调用任何 `pgcrypto` 函数之前就能识别 `pgcrypto.fips` 参数。

    ```shell
    gpconfig -c shared_preload_libraries -v 'pgcrypto.so'
    gpstop -ar
    ```

    如果 `shared_preload_libraries` 已列出其他库，请在其值中保留它们。

2. 为每个必须使用 FIPS 模式的数据库设置参数。例如，为 `testdb` 数据库设置：

    ```sql
    ALTER DATABASE testdb SET pgcrypto.fips TO on;
    ```

3. 重新连接数据库，并检查设置：

    ```sql
    SHOW pgcrypto.fips;
    ```

要关闭 FIPS 模式，运行 `ALTER DATABASE testdb RESET pgcrypto.fips;`，然后重新连接。

## 模块文档 {#module-documentation}

此模块各个函数的详细信息，参见 PostgreSQL 文档中的 [pgcrypto](https://www.postgresql.org/docs/14/pgcrypto.html)。
