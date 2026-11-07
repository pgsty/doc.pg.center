---
title: PostgreSQL 扩展与网关
description: 了解 DocumentDB 的三个 PostgreSQL 扩展与协议网关，包括 BSON、文档操作、索引和 MongoDB 兼容连接。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/postgres-api/index.md
weight: 40
linkTitle: PostgreSQL API
translation_source_sha256: 742b748b633e65609c459ff3e907c7d25acb4cf845c1212dbf07695fcdc98dc2
translation_review: AI-assisted bilingual review; 2026-11-07
---

DocumentDB 由三个 PostgreSQL 扩展和一个网关组成。它们协同工作，在 PostgreSQL 上提供兼容 MongoDB 的文档数据库功能。

<span id="pg-documentdb-core"></span>

## pg_documentdb_core {#pg_documentdb_core}

`pg_documentdb_core` 为原生 PostgreSQL 引入 BSON 数据类型及其操作。它提供处理 BSON 数据所需的基础数据结构和函数，是实现文档读写以及面向文档的 NoSQL 功能的基础。

### 主要功能 {#key-features}

- **BSON 数据类型支持：** 为 PostgreSQL 添加 BSON（二进制 JSON）数据类型，高效存储和处理类似 JSON 的文档。
- **原生操作：** 实现针对 BSON 数据的 PostgreSQL 原生操作，以兼顾集成与性能。
- **可扩展性：** 为 DocumentDB 生态中的其他功能和扩展提供基础。

<span id="pg-documentdb"></span>

## pg_documentdb {#pg_documentdb}

`pg_documentdb` 是 DocumentDB 的公共 API 层，提供数据库中文档的增删改查功能。它利用 `pg_documentdb_core` 的能力，提供一套在 PostgreSQL 中管理文档数据的 API。

### 主要功能 {#key-features-1}

- **文档读写：** 提供创建、读取、更新和删除文档的 API。
- **高级查询：** 支持全文搜索、地理空间查询、向量搜索和聚合流水线等复杂查询。
- **索引管理：** 支持单字段、多键、复合、部分、唯一、TTL、文本、地理空间与向量索引。
- **用户与角色管理：** 内置用于管理用户、角色和 SCRAM 认证的命令。
- **组件集成：** 与 `pg_documentdb_core` 协作，提供文档管理能力。

### 使用方法 {#usage}

使用 `pg_documentdb` 前，需要在 PostgreSQL 环境中安装并配置 `pg_documentdb_core`。随后可通过任何 PostgreSQL 客户端，使用 `pg_documentdb` 提供的 API 执行文档操作。可调用的函数列表见[函数参考](/documentdb/postgres-api/functions/)。

<span id="pg-documentdb-extended-rum"></span>

## pg_documentdb_extended_rum {#pg_documentdb_extended_rum}

`pg_documentdb_extended_rum`（SQL 扩展名为 `documentdb_extended_rum`）是 DocumentDB 对 PostgreSQL RUM 索引访问方法的分支，为文档索引提供支持。它保留 RUM 的磁盘格式，并针对文档负载扩展查询路径。

DocumentDB 1.0 必须使用该扩展：`documentdb.rum_library_load_option` 默认为 `require_documentdb_extended_rum`，因此 `pg_documentdb` 从扩展 RUM 库加载索引处理器。该库只能通过 `shared_preload_libraries` 加载，而 `CREATE EXTENSION documentdb CASCADE` 不会创建这个扩展。因此，手动配置的服务器必须在建立索引前完成这两步：

```sql
-- postgresql.conf: add pg_documentdb_extended_rum to shared_preload_libraries and set
-- documentdb.alternate_index_handler_name = 'extended_rum', then restart
CREATE EXTENSION documentdb_extended_rum;
```

软件包配置向导和 `documentdb-local` 镜像会自动完成这些操作。加载选项见[配置参考](/documentdb/postgres-api/configuration/)。

<span id="pg-documentdb-gw"></span>

## pg_documentdb_gw {#pg_documentdb_gw}

`pg_documentdb_gw` 是协议转换网关，将用户发送的 MongoDB 线协议命令转换为调用 `pg_documentdb` API 的 PostgreSQL 查询。MongoDB 兼容驱动和工具（如 `mongosh`、PyMongo、官方 MongoDB Node.js 驱动与 VS Code 扩展）因此可以直接连接 DocumentDB，无需修改。

### 主要功能 {#key-features-2}

- **MongoDB 线协议：** 解析 `OP_MSG`、`OP_QUERY`、`OP_INSERT` 等协议消息，并调用相应的 `pg_documentdb` SQL 函数。
- **认证：** 使用 SCRAM-SHA-256。它是 `hello`/`isMaster` 握手中唯一公布的认证机制，也是标准构建中唯一可用的机制。网关在 SASL 启动时还接受基于令牌的 `MONGODB-OIDC` 认证，但该路径依赖扩展未定义的 `documentdb_api_internal.authenticate_token` 函数，需要部署方提供令牌认证实现。`PLAIN` 会被拒绝。
- **TLS 终止：** 在网关端口（默认 `10260`）终止 TLS，驱动可使用标准 MongoDB 风格的 `mongodb://` 连接串，并设置 `tls=true`。
- **游标与会话管理：** 将 `getMore`、`killCursors`、`killSessions` 和 `killOp` 命令转换为对应的后端操作。
- **部署方式：** 可作为独立进程运行，这是 `documentdb-local` 容器的默认方式；也可从源码构建，通过 `pg_documentdb_gw_host` 扩展作为 PostgreSQL 后台工作进程运行。软件包和容器镜像不包含这个扩展。
