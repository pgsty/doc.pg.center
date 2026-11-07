---
title: 入门指南
description: 选择 Docker 或 Linux 软件包，创建 DocumentDB 实例，并通过 shell、驱动程序或编辑器插入和读取你的第一个文档。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/documentdb.github.io/blob/90cfa088351557cd618034dfc00ab817c35a5f76/app/services/articleService.ts
upstream_ref: website 90cfa08; DocumentDB 1.0
weight: 10
translation_source_sha256: 07bd408774dc89ef027998ca6954f1886788fb33f9a99451245fc02361dbd2ab
translation_review: AI-assisted bilingual review; 2026-11-07
---

## 选择运行环境，执行第一次查询 {#choose-an-environment-then-run-your-first-query}

使用 Docker 或 Linux 软件包完成安装，创建可用实例，再通过 shell、驱动程序或编辑器插入并读取文档。

1. **选择安装方式。** 在 Linux、macOS 或 Windows 上，可以从 Docker 开始。需要直接安装到主机时，使用 Linux 软件包。

   **Docker：推荐用于试用和开发。** 安装 Docker 后，即可在 Linux、macOS 或 Windows 上运行本地实例。执行前请替换凭据占位符。端口仅绑定回环地址。

   ```bash
   docker run -dt --pull always --name documentdb \
     -p 127.0.0.1:10260:10260 \
     -e USERNAME='<YOUR_USERNAME>' \
     -e PASSWORD='<YOUR_PASSWORD>' \
     ghcr.io/documentdb/documentdb/documentdb-local:latest
   ```

   > [!NOTE]
   > DocumentDB Local 镜像默认发送使用情况遥测数据。若要关闭，请在镜像名称前添加 `-e DOCUMENTDB_USAGE_TELEMETRY=false`。参见[使用情况遥测](/documentdb/documentdb-local/#usage-telemetry)和[隐私声明](https://github.com/documentdb/documentdb/blob/v1.0-0/documentdb-local/PRIVACY.md)。

   等到 `docker logs documentdb` 中出现就绪提示后再连接。参见 [Docker 快速入门](/documentdb/getting-started/docker/)。

   **Linux 软件包。** 适用于没有 Docker，或需要自行控制 PostgreSQL、拓扑、服务及配置的环境。在 Ubuntu 24.04（Noble）或 EL9 上通过 apt 或 dnf 安装，然后运行配置向导。请打开 [Linux 软件包安装](https://documentdb.io/packages?method=packages)页面，或阅读完整的 [Linux 软件包快速入门](/documentdb/getting-started/packages/)。

2. **插入并读取第一个文档。** 选择自己习惯的客户端。每篇指南都会连接前面创建的实例，并验证插入和读取操作。示例数据是可选的。可以从 [Visual Studio Code 快速入门](/documentdb/getting-started/vscode-quickstart/)、[Node.js 快速入门](/documentdb/getting-started/nodejs-setup/)或 [Python 快速入门](/documentdb/getting-started/python-setup/)开始。
{.steps}

DocumentDB 是基于 PostgreSQL 构建的开源文档数据库平台，为开发者提供采用完全宽松许可证的开源文档存储平台。

<span id="what-is-document-db"></span>

## 什么是 DocumentDB？ {#what-is-documentdb}

DocumentDB 提供了一个基于 PostgreSQL 实现的 NoSQL 数据存储，使开发者能够完全了解引擎的架构与实现。它旨在提供以下功能：

- 通过 `pg_documentdb_gw` 网关实现与 MongoDB 线协议兼容，因此 MongoDB 驱动程序和工具可无需修改直接连接
- 通过 `pg_documentdb` 扩展提供公开的文档 CRUD 和管理 API
- 通过 `pg_documentdb_core` PostgreSQL 扩展原生支持 BSON 文档
- 高级索引功能，包括单字段索引、多键索引、复合索引、文本索引、地理空间索引和向量索引
- 由 `pgvector` PostgreSQL 扩展驱动的向量搜索功能
- 网关上支持 SCRAM-SHA-256 认证和 TLS
- 完全兼容 PostgreSQL，支持高级 SQL 操作

## 核心特性 {#key-features}

- **PostgreSQL 基础**：基于强大的 PostgreSQL 引擎构建，可同时利用文档与关系型数据能力
- **开源**：采用 MIT 许可证发布，对使用、修改和分发无任何限制
- **文档数据库标准**：首个致力于创建开放文档数据库标准的实现，类似于关系型数据库中的 ANSI SQL
- **随处运行**：提供 Linux 软件包、本地开发用容器镜像，以及用于复制部署的 Kubernetes Operator
- **开发者友好**：拥有丰富的工具与扩展生态，包括 VS Code 集成和 MongoDB 兼容性

## 架构组件 {#architecture-components}

DocumentDB 由四个主要组件构成：

1. **pg_documentdb_core**：PostgreSQL 核心扩展，提供原生 BSON 存储、字段访问和索引基础功能。
2. **pg_documentdb**：公共 API 层，实现文档命令、CRUD 操作、查询执行和索引管理。
3. **pg_documentdb_gw**：将 MongoDB 线协议请求转换为 PostgreSQL 操作的网关，并负责认证、会话和 TLS。
4. **pg_documentdb_extended_rum**：支撑 DocumentDB 文档索引的索引访问方法，1.0 版本中必需。

这些组件协同工作，让你既能通过兼容 MongoDB 的工具和驱动使用 DocumentDB，又能利用 PostgreSQL 的内部能力。



## 常见使用场景 {#common-use-cases}

- **现代 Web 应用**：以 MongoDB 兼容方式存储和查询 JSON 文档
- **人工智能/机器学习应用**：利用向量搜索实现相似性匹配与嵌入
- **混合数据模型**：在同一数据库中结合文档与关系型数据
- **迁移路径**：轻松从现有 MongoDB 工作负载迁移
- **本地开发**：用于开发和测试的全功能本地实例

## 从这里开始 {#start-here}

选定运行环境并创建可用实例后，使用适合当前需求的客户端连接：

1. **选择 Docker 或 Linux 软件包。** 在 Linux、macOS 或 Windows 上试用和开发时，推荐使用 [Docker 安装](https://documentdb.io/packages?method=docker)。没有 Docker，或需要自行控制 PostgreSQL、拓扑、服务与配置时，使用 [Linux 软件包安装](https://documentdb.io/packages?method=packages)。
2. **创建可用实例。** 按 [Docker 快速入门](/documentdb/getting-started/docker/)或 [Linux 软件包快速入门](/documentdb/getting-started/packages/)操作。Linux 软件包安装分为两个阶段：先安装软件包，再运行配置向导。仅复制命令或安装文件，都不能证明端点已经就绪。
3. **插入并读取第一个文档。** 按 [Visual Studio Code 快速入门](/documentdb/getting-started/vscode-quickstart/)、[Node.js 快速入门](/documentdb/getting-started/nodejs-setup/)或 [Python 快速入门](/documentdb/getting-started/python-setup/)操作。继续使用同一个运行中的实例，无需再安装一套服务器。

如需更高级的控制，[使用现有的本地 PostgreSQL 实例](/documentdb/linux-packages/#adopt-an-existing-postgre-sql-instance)，由管理员管理配置和重启；或[仅安装 PostgreSQL 扩展](/documentdb/linux-packages/#install-the-postgre-sql-extension-only)。仅扩展安装不会安装网关，因此应用程序和驱动程序无法连接；你需通过 SQL 使用它。


## 验证安装配置 {#verify-your-setup}

开始编写应用代码前，先确认可以连接 DocumentDB，并能插入和读取文档。使用 Docker 时，检查 `docker ps --filter "name=documentdb"`，并等待 `docker logs documentdb` 中的就绪提示；使用 Linux 软件包时，检查 `sudo documentdb-setup --status`。

在 DocumentDB 所在主机上运行下面的 shell 示例。Docker 使用自己设置的用户名，Linux 软件包使用 `admin`，然后在提示处输入密码。

跳过证书验证的做法**仅适用于本地开发**。Linux 软件包的配置向导默认将网关绑定到**所有网络接口**：运行配置前，请用防火墙限制对端口 `10260` 的访问，并遵循[网络与证书指南](/documentdb/linux-packages/#before-exposing-it-to-a-network)。

```bash
mongosh localhost:10260 \
  -u '<YOUR_USERNAME>' \
  -p \
  --authenticationMechanism SCRAM-SHA-256 \
  --tls \
  --tlsAllowInvalidCertificates
```

然后运行：

```javascript
db.runCommand({ ping: 1 })
use quickstart
db.orders.insertOne({ item: "widget", qty: 5 })
db.orders.find({ item: "widget" })
```

插入操作应返回 `acknowledged: true`，查询应返回你的文档。无需加载示例数据。

如需更完整的演示，可使用 [Mongo Shell 快速入门](/documentdb/getting-started/mongo-shell-quickstart/)。驱动程序示例可在 [Node.js 快速入门](/documentdb/getting-started/nodejs-setup/) 和 [Python 快速入门](/documentdb/getting-started/python-setup/) 中找到。


## 故障排除与调试 {#troubleshooting-and-debugging}

如果首次设置未成功：

- 使用 Linux 软件包时，检查 `sudo documentdb-setup --status`，并参见[软件包故障排查](/documentdb/getting-started/packages/#troubleshooting)。默认的 PostgreSQL 18 安装使用 `documentdb-local@18.target`，而不是元软件包的别名。
- 使用 Docker 时，通过 `docker ps` 确认容器正在运行，且端口 `10260` 已映射到主机。通过 `docker logs documentdb` 检查启动、认证和 TLS 错误。
- 若要验证证书，而不使用 `tlsAllowInvalidCertificates=true` 跳过验证，请按 Linux 软件包的[证书配置步骤](/documentdb/linux-packages/#before-exposing-it-to-a-network)操作；Docker 用户请参见 [DocumentDB Local](/documentdb/documentdb-local/)。
- 如需更详细的 Docker 诊断信息，请使用 `-e DOCUMENTDB_LOG_LEVEL=debug` 重新创建 DocumentDB Local（`--log-level` 选项目前不生效）。可用的运行时选项见 [DocumentDB Local](/documentdb/documentdb-local/)。
- 要更换安装方式，请打开 [Docker 安装](https://documentdb.io/packages?method=docker)或 [Linux 软件包安装](https://documentdb.io/packages?method=packages)页面。


## 探索核心功能 {#explore-key-features}

成功连接后，请继续以下指南：

- [API 参考](/documentdb/reference/) - MongoDB 命令和运算符覆盖范围
- [PostgreSQL 扩展 API](/documentdb/postgres-api/) - PostgreSQL 侧的函数、类型和运算符
- [DocumentDB Local](/documentdb/documentdb-local/) - 本地运行时选项、示例数据、证书和功能说明
- [内部架构](/documentdb/architecture/) - 核心、扩展和网关如何协同工作
- [示例画廊](https://documentdb.io/samples) - 可用于自身应用的端到端示例



## 社区与支持 {#community-and-support}

- **Discord 社区**：加入我们的 [Discord 服务器](https://discord.gg/vH7bYu524D)，参与或获取：
  - 社区交流会和定期答疑
  - 实时技术支持
  - 迁移协助
  - 最佳实践分享
- GitHub 仓库：[documentdb/documentdb](https://github.com/documentdb/documentdb)
- 文档：完整的指南和 API 参考
- 问题跟踪：在 GitHub 上报告缺陷、提出功能需求

## 下一步 {#next-steps}

完成初始设置后：

- 继续 [Mongo Shell 快速入门](/documentdb/getting-started/mongo-shell-quickstart/)、[Node.js 快速入门](/documentdb/getting-started/nodejs-setup/) 或 [Python 快速入门](/documentdb/getting-started/python-setup/)
- 探索 [API 参考](/documentdb/reference/) 以获取详细的命令和运算符文档
- 加入我们的社区以获取支持并参与贡献
