---
title: Mongo Shell 快速入门
description: 使用 mongosh 通过 Docker 或 Linux 软件包连接 DocumentDB，并插入和读取你的第一个文档。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/documentdb.github.io/blob/90cfa088351557cd618034dfc00ab817c35a5f76/app/services/articleService.ts
upstream_ref: website 90cfa08; DocumentDB 1.0
weight: 70
translation_source_sha256: 43a7cf9572af072183812f2bfd62448a53da51814f97d8876d6bda6a015d81bc
translation_review: AI-assisted bilingual review; 2026-11-07
---

使用 `mongosh` 验证本地 DocumentDB 实例，检查示例数据，并运行你的第一个文档命令。

<span id="have-a-running-document-db-instance"></span>

## 是否已有正在运行的 DocumentDB 实例？ {#have-a-running-documentdb-instance}

如果已有实例，请继续使用它，并按下文准备客户端依赖。否则，请选择一种服务器安装方式：

- [Docker](https://documentdb.io/packages?method=docker)：在 Linux、macOS 或 Windows 上运行本地容器，推荐用于试用和开发。
- [Linux 软件包](https://documentdb.io/packages?method=packages)：安装全套组件，再通过配置向导创建私有 PostgreSQL 实例。

[Docker 快速入门](/documentdb/getting-started/docker/) 和 [Linux 软件包快速入门](/documentdb/getting-started/packages/) 包含完整的服务器操作说明。如果已有实例在运行，请勿启动第二个实例。

示例连接到 `localhost:10260`，所以客户端应当在 DocumentDB 所在主机上运行。Docker 使用自己设置的凭据；Linux 软件包使用用户名 `admin`，以及配置时设置的密码。如果修改过端点，请使用实际配置的主机和端口。

下文跳过自签名证书验证的做法**仅适用于本地开发**。通过网络访问时，请使用受信任的证书。Linux 软件包的配置向导默认将网关绑定到**所有网络接口**：配置前请用防火墙限制对端口 `10260` 的访问，并遵循[网络与证书指南](/documentdb/linux-packages/#before-exposing-it-to-a-network)。Docker 示例仅将端口映射到回环接口。


## 前提条件 {#prerequisites}

- [mongosh](https://www.mongodb.com/docs/mongodb-shell/install/)
- 你实例的端点和凭据（示例使用 `localhost:10260`）

## 可选：启动一个 Docker 实例 {#optional-start-a-docker-instance}

如果你已安装 Linux 软件包或已有正在运行的实例，请跳过此步骤。如果你选择了 Docker 且已安装 [Docker](https://www.docker.com/)：

```bash
docker run -dt --pull always --name documentdb \
  -p 127.0.0.1:10260:10260 \
  -e USERNAME='<YOUR_USERNAME>' \
  -e PASSWORD='<YOUR_PASSWORD>' \
  ghcr.io/documentdb/documentdb/documentdb-local:latest
```

> [!NOTE]
> DocumentDB Local 镜像默认发送使用情况遥测数据。若要关闭，请在镜像名称前添加 `-e DOCUMENTDB_USAGE_TELEMETRY=false`。参见[使用情况遥测](/documentdb/documentdb-local/#usage-telemetry)和[隐私声明](https://github.com/documentdb/documentdb/blob/v1.0-0/documentdb-local/PRIVACY.md)。

将占位符替换为自己的凭据。等到 `docker logs documentdb` 中出现就绪提示后再连接，参见 [Docker 快速入门](/documentdb/getting-started/docker/#verify-the-container)。

## 连接并验证连接 {#connect-and-verify-the-connection}

使用现有实例的凭据。不论通过 Docker 还是 Linux 软件包安装，跳过自签名证书验证的做法都**仅适用于本地开发**。

```bash
mongosh localhost:10260 \
  -u '<YOUR_USERNAME>' \
  -p \
  --authenticationMechanism SCRAM-SHA-256 \
  --tls \
  --tlsAllowInvalidCertificates
```

连接后，运行快速健康检查：

```javascript
db.runCommand({ ping: 1 })

db.adminCommand({ listDatabases: 1 })
```

成功的输出表明认证、TLS 和网关端点均正常工作。

## 探索内置示例数据 {#explore-the-built-in-sample-data}

示例数据需要**主动启用**，首次插入和读取文档并不需要它。通过 Linux 软件包安装时，可在配置命令中添加 `--load-sample-data`；这需要额外安装一个工具，参见[配置并连接](/documentdb/getting-started/packages/#set-up-and-connect)。Docker 可以通过 `--init-data true` 启动。未指定这些选项时，`StoreData` 不会存在。Docker 对每个数据卷只加载一次示例数据：如果卷中从未加载过示例数据，用 `--init-data true` 重新创建容器会加载这些数据，而不影响已有数据；再次加载则需要新卷。

如果你未加载示例数据，请直接跳至下方的 **创建你自己的集合**。

```javascript
use StoreData

db.stores.find(
  {},
  { _id: 0, name: 1, city: 1, "sales.revenue": 1 }
).limit(3)

db.ratings.find({}, { _id: 1, rating: 1 }).limit(2)
```

## 创建你自己的集合 {#create-your-own-collection}

```javascript
use quickstart

db.movies.deleteMany({})

db.movies.insertMany([
  { title: "The Matrix", year: 1999, genres: ["sci-fi", "action"] },
  { title: "Dune", year: 2021, genres: ["sci-fi", "adventure"] },
  { title: "Arrival", year: 2016, genres: ["sci-fi", "drama"] }
])

db.movies.createIndex({ title: 1 })

db.movies.find(
  { year: { $gte: 2000 } },
  { _id: 0, title: 1, year: 1 }
).sort({ year: -1 })
```

## 改用受信任的本地证书 {#use-a-trusted-local-certificate-instead}

若要验证证书，而不使用 `--tlsAllowInvalidCertificates` 跳过验证，请取得端点对应的受信任证书或 CA 文件。Linux 软件包用户请按[证书配置](/documentdb/linux-packages/#before-exposing-it-to-a-network)操作；Docker 用户可以用以下命令复制本地证书：

```bash
docker cp documentdb:/home/documentdb/.local/state/documentdb-gateway/tls/cert.pem ~/documentdb-cert.pem
```

然后将你的证书文件传递给 `mongosh`：

```bash
mongosh localhost:10260 \
  -u '<YOUR_USERNAME>' \
  -p \
  --authenticationMechanism SCRAM-SHA-256 \
  --tls \
  --tlsCAFile ~/documentdb-cert.pem
```

## 故障排除和调试 {#troubleshooting-and-debugging}

如果 `mongosh` 首次连接失败：

- 确认本地 DocumentDB 实例正在运行后再连接
- 如果使用 Docker，请检查 `docker ps --filter "name=documentdb"` 和 `docker logs documentdb`
- 如果使用 Linux 软件包，请检查 `sudo documentdb-setup --status`；对于手动构建的网关，请确认其进程正在监听端口 `10260`
- 如果认证失败，请确认启动 DocumentDB 时使用的用户名和密码
- 如果 TLS 验证失败，请保留 `--tlsAllowInvalidCertificates` 用于默认本地自签名设置，或切换至 `--tlsCAFile` 并使用受信任证书
- 如果 `mongosh` 未安装，请遵循 [mongosh 安装指南](https://www.mongodb.com/docs/mongodb-shell/install/)
- 使用 [Python 快速入门](/documentdb/getting-started/python-setup/) 或 [Node.js 快速入门](/documentdb/getting-started/nodejs-setup/) 从应用驱动程序验证同一端点

## 下一步 {#next-steps}

- [Visual Studio Code 快速入门](/documentdb/getting-started/vscode-quickstart/)
- [API 参考](/documentdb/reference/)
- [DocumentDB Local](/documentdb/documentdb-local/)
- [Python 快速入门](/documentdb/getting-started/python-setup/)
- [Node.js 快速入门](/documentdb/getting-started/nodejs-setup/)
- [示例画廊](https://documentdb.io/samples)
