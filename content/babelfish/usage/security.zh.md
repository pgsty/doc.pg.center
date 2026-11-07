---
title: Babelfish 安全管理
linkTitle: 安全性
description: 查阅 SSL/TLS 协商、预定义角色及权限操作的版本支持。
weight: 70
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_usage/security.md
upstream_ref: main @ f468c5ed3d38
translation_notice: en
upstream_modified: true
translation_status: complete
translation_credit: PGSTY 文档项目
upstream_notice: /zh/babelfish/site/attribution/
upstream_license: LicenseRef-Babelfish-Website-ZH
---



> [!NOTE] 文档快照
> 本文译自上游网站，中文翻译由 PGSTY 文档项目整理。上游自 2023 年起将新文档迁至 [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki)；请结合所用版本的[发行说明](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/releases)核对功能支持。

## Babelfish 安全性 {#babelfish-security}

Babelfish 通过以下方式提供安全环境：

- 支持可配置的客户端 SSL 连接，对通信进行加密。
- 使用预定义角色保护 Babelfish 对象。

以下各节分别介绍这两个方面。

### 客户端连接的 SSL/TLS 支持 {#ssltls-support-for-client-connections}

Babelfish 使用 PostgreSQL 原生的 SSL 支持，加密客户端与服务器之间的通信。服务器端 SSL 配置方法见 [PostgreSQL 文档](https://www.postgresql.org/docs/13/ssl-tcp.html#SSL-SETUP)。

要使用 SSL 加密，必须在编译 PostgreSQL 服务器时启用 SSL 支持，并在 `postgresql.conf` 中将 `ssl` 设置为 `on`。服务器在同一个 TCP 端口上监听 SSL 和非 SSL 连接，并与客户端协商是否使用 SSL。默认情况下，客户端可以自行决定是否要求 SSL 连接；服务器会在同一端口接受加密和未加密的连接请求并协商连接类型。

如果 `babelfishpg_tds.tds_ssl_encrypt` 为 `true`，则所有连接都必须使用端到端加密。在这种情况下，请求未加密连接的客户端会被拒绝。

下表列出客户端连接时，Babelfish 如何解释 SSL 设置：

| 客户端 SSL 设置   | Babelfish SSL 设置 | 是否允许连接                         | 返回客户端的值 |
|:---------------------|:----------------------|:--------------------------------------------|:-------------------------|
| ENCRYPT_OFF          | tds_ssl_encrypt=false | 允许，仅登录数据包加密      | ENCRYPT_OFF              |
| ENCRYPT_OFF          | tds_ssl_encrypt=true  | 允许，整个连接加密 | ENCRYPT_REQ              |
| ENCRYPT_ON           | tds_ssl_encrypt=false | 允许，整个连接加密 | ENCRYPT_ON               |
| ENCRYPT_ON           | tds_ssl_encrypt=true  | 允许，整个连接加密 | ENCRYPT_ON               |
| ENCRYPT_NOT_SUP      | tds_ssl_encrypt=false | 是                                         | ENCRYPT_NOT_SUP          |
| ENCRYPT_NOT_SUP      | tds_ssl_encrypt=true  | 不允许，关闭连接                       | ENCRYPT_REQ              |
| ENCRYPT_REQ          | tds_ssl_encrypt=false | 允许，整个连接加密 | ENCRYPT_ON               |
| ENCRYPT_REQ          | tds_ssl_encrypt=true  | 允许，整个连接加密 | ENCRYPT_ON               |
| ENCRYPT_CLIENT_CERT  | tds_ssl_encrypt=false | 不允许，关闭连接                       | 不支持              |
| ENCRYPT_CLIENT_CERT  | tds_ssl_encrypt=true  | 不允许，关闭连接                       | 不支持              |

### 用户管理与角色 {#user-management-and-roles}

Babelfish 会创建以下 T-SQL 角色：

- `sysadmin`
- `master_db_owner`
- `master_dbo`
- `master_guest`
- `tempdb_db_owner`
- `tempdb_dbo`
- `tempdb_guest`

对于在 Babelfish 中创建的每个数据库，还会创建 `dbname_db_owner` 和 `dbname_dbo` 角色，其中 `dbname` 为数据库名。此外，还支持以下角色和权限功能：

| 功能                                                                                   | 支持版本   |
|:------------------------------------------------------------------------------------------|:---------------------|
| 固定服务器角色： dbcreator, securityadmin                                              | 版本 4.5+, 5.1+  |
| 固定数据库角色： db_owner, db_datareader, db_datawriter, db_accessadmin, db_securityadmin | 版本 4.5+, 5.1+  |
| ALTER AUTHORIZATION ON DATABASE （更改数据库所有者）                                         | 版本 3.4+         |
| 模式级 GRANT/REVOKE (GRANT ... ON SCHEMA::)                                        | 版本 3.6+, 4.2+  |
| 对象级 GRANT/REVOKE (GRANT ... ON OBJECT::)                                        | 所有版本         |
| ALTER SERVER ROLE ... ADD MEMBER                                                          | 所有版本         |

这些角色实现了 SQL Server 的对象所有权结构，由数据库维护，不应直接用于客户端连接。
