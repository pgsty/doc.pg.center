---
title: TDS 线协议
linkTitle: TDS 协议
description: 了解 TDS 数据包头、登录握手与加密协商。
weight: 60
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_internals/tds-protocol.md
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

## TDS 线协议 {#the-tds-wire-protocol}

Babelfish 在 PostgreSQL 服务器上通过 TDS 线协议实现 SQL Server 行为。Babelfish 支持通过以下网络类型及相关协议连接：

- [TCP](https://en.wikipedia.org/wiki/Transmission_Control_Protocol)。
- VIA（Virtual Interface Architecture，虚拟接口架构）。
- 传输层安全协议 [TLS](https://en.wikipedia.org/wiki/Transport_Layer_Security) 与安全套接层 [SSL](https://datatracker.ietf.org/doc/html/rfc6101)。

### 基本消息流程 {#basic-message-flow}

消息流程始于客户端向服务器发送连接请求。服务器响应后，客户端发送认证请求。认证成功后，后续客户端请求与服务器响应在双方之间往返传输。TDS 依靠客户端与服务器之间的网络传输顺序维持握手过程。

### TDS 客户端通信 {#tds-client-communications}

每个客户端请求或服务器响应由一个或多个数据包组成。每个包都包含 TDS 首部，字段如下：

- Type：消息类型。
- Status：消息状态。
- Length：从数据包起始处到令牌数据末尾的长度，使用无符号短整数表示，最大为 65535。
- SPID：当前连接的会话 ID。
- PacketID：每发送一个数据包就递增。对于跨多个包的消息尤其重要。该值按“模 255”发送，因此只需 1 字节。
- Window：当前未使用，发送值为 `0x0`。

建立连接前，TDS 协议要求通过 PRELOGIN 通信协商一些重要的连接属性。双方交换关键信息；如果客户端和服务器无法相互理解，系统可以终止连接尝试。

PRELOGIN 通信成功后，客户端可以发起 SSL/TLS 握手。客户端根据 Babelfish 服务器的 [SSL 配置](#ssltls-support-for-tds-connections)协商认证和加密方式。

通过 PRELOGIN 后，客户端可使用 LOGIN7 定义客户端与服务器之间使用的认证规则。

### TDS 连接的 SSL/TLS 支持 {#ssltls-support-for-tds-connections}

Babelfish 使用 PostgreSQL 原生 SSL 支持来加密客户端与服务器之间的通信。服务器端 SSL 的配置详见 [PostgreSQL 文档](https://www.postgresql.org/docs/13/ssl-tcp.html#SSL-SETUP)。

要使用 SSL 加密，编译 PostgreSQL 服务器时需启用 SSL 支持，并在 `postgresql.conf` 中将 `ssl` 设为 `on`。服务器在同一个 TCP 端口监听 SSL 和非 SSL 连接，并与接入的客户端协商是否使用 SSL。默认情况下，客户端可以选择是否要求 SSL 连接。服务器会在同一个 TCP 端口接受明文和加密连接，与客户端协商连接类型。如果将 `babelfishpg_tds.tds_ssl_encrypt` 设为 `true`，则所有连接都必须使用端到端加密；客户端请求不加密连接时会被拒绝。

下表说明客户端连接时 Babelfish 如何解释 SSL 设置：

| 客户端 SSL 设置 | Babelfish SSL 设置 | 是否允许连接 | 返回客户端的值 |
| --- | --- | --- | --- |
| ENCRYPT_OFF | tds_ssl_encrypt=false | 允许，仅登录包加密 | ENCRYPT_OFF |
| ENCRYPT_OFF | tds_ssl_encrypt=true | 允许，整个连接加密 | ENCRYPT_REQ |
| ENCRYPT_ON | tds_ssl_encrypt=false | 允许，整个连接加密 | ENCRYPT_ON |
| ENCRYPT_ON | tds_ssl_encrypt=true | 允许，整个连接加密 | ENCRYPT_ON |
| ENCRYPT_NOT_SUP | tds_ssl_encrypt=false | 允许 | ENCRYPT_NOT_SUP |
| ENCRYPT_NOT_SUP | tds_ssl_encrypt=true | 不允许，关闭连接 | ENCRYPT_REQ |
| ENCRYPT_REQ | tds_ssl_encrypt=false | 允许，整个连接加密 | ENCRYPT_ON |
| ENCRYPT_REQ | tds_ssl_encrypt=true | 允许，整个连接加密 | ENCRYPT_ON |
| ENCRYPT_CLIENT_CERT | tds_ssl_encrypt=false | 不允许，关闭连接 | Unsupported |
| ENCRYPT_CLIENT_CERT | tds_ssl_encrypt=true | 不允许，关闭连接 | Unsupported |
