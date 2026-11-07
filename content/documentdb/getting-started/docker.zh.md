---
title: Docker 快速入门
description: 使用 Docker 启动 DocumentDB Local，验证连接，并获取故障排除和下一步指导。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/documentdb.github.io/blob/90cfa088351557cd618034dfc00ab817c35a5f76/app/services/articleService.ts
upstream_ref: website 90cfa08; DocumentDB 1.0
weight: 20
translation_source_sha256: 7ece05422b3339971c5b1c91ded4f6ba3055cdeca0236dff8c892c7ade2faf4a
translation_review: AI-assisted bilingual review; 2026-11-07
---

使用 Docker 在本地运行 DocumentDB，验证环境可用后再编写使用驱动程序的应用代码。安装方式参见 [Docker 安装](https://documentdb.io/packages?method=docker)或 [Linux 软件包安装](https://documentdb.io/packages?method=packages)。

## 前提条件 {#prerequisites}

- [Docker](https://www.docker.com/)
- [mongosh](https://www.mongodb.com/docs/mongodb-shell/install/)，用于快速检查连接
- 一个可供 DocumentDB 使用的本地端口（示例使用 `10260`）

<span id="start-document-db"></span>

## 启动 DocumentDB {#start-documentdb}

先拉取镜像，这也会替换本地缓存的旧版 `latest` 镜像：

```bash
docker pull ghcr.io/documentdb/documentdb/documentdb-local:latest
```

然后启动容器：

```bash
docker run -dt --name documentdb \
  -p 127.0.0.1:10260:10260 \
  -e USERNAME='<YOUR_USERNAME>' \
  -e PASSWORD='<YOUR_PASSWORD>' \
  ghcr.io/documentdb/documentdb/documentdb-local:latest \
  --init-data true
```

> [!NOTE]
> DocumentDB Local 镜像默认发送使用情况遥测数据。若要关闭，请在镜像名称前添加 `-e DOCUMENTDB_USAGE_TELEMETRY=false`。参见[使用情况遥测](/documentdb/documentdb-local/#usage-telemetry)和[隐私声明](https://github.com/documentdb/documentdb/blob/v1.0-0/documentdb-local/PRIVACY.md)。

> 将 `<YOUR_USERNAME>` 和 `<YOUR_PASSWORD>` 替换为自己的凭据。
>
> `-p 127.0.0.1:10260:10260` 使端点只监听回环地址。仅写 `-p 10260:10260` 会将端口映射到**所有**网络接口，这通常不符合笔记本电脑上的使用需求。
>
> `--init-data true` 将内置示例数据加载到 `StoreData`，供下文的验证步骤查询。此选项**默认关闭**：不指定它时，容器启动后没有 `StoreData` 数据库，`use StoreData` 也不会返回任何内容。每个数据卷只加载一次示例数据。现有卷不会自动迁移；要重新加载，请重新创建卷。有关 `--init-data-path`、证书配置及其他运行时选项，参见 [DocumentDB Local](/documentdb/documentdb-local/)。

## 验证容器 {#verify-the-container}

```bash
docker ps --filter "name=documentdb"
```

应当能看到容器处于 `Up` 状态，且端口 `10260` 已映射到主机。

> [!IMPORTANT]
> `docker ps` 显示 `Up` 时，DocumentDB 往往还不能接受连接。请等到就绪提示出现后再连接，否则首次调用 `mongosh` 会因连接错误而失败：
>
> ```bash
> until docker logs documentdb 2>&1 | grep -q "=== DocumentDB is ready ==="; do sleep 2; done
> ```

## 验证连接 {#verify-the-connection}

使用 `mongosh` 确认身份验证、TLS 和网关端点正常工作：

下文跳过证书验证的做法**仅适用于本地开发**。通过共享网络或公网连接之前，请先配置受信任的证书。

```bash
mongosh localhost:10260 \
  -u '<YOUR_USERNAME>' \
  -p \
  --authenticationMechanism SCRAM-SHA-256 \
  --tls \
  --tlsAllowInvalidCertificates
```

接着做一次简单的健康检查。下文使用的示例数据要求在前面的 `docker run` 命令中指定 `--init-data true`，否则 `StoreData` 不会存在：

```javascript
db.runCommand({ ping: 1 })

use StoreData

db.stores.find({}, { _id: 0, name: 1, city: 1, "sales.revenue": 1 }).limit(3)
```

写入自己的文档，再将其读回。这一步不需要示例数据：

```javascript
use quickstart
db.orders.insertOne({ item: "widget", qty: 5 })
db.orders.find({ item: "widget" })
```

若要验证证书，而不使用 `--tlsAllowInvalidCertificates` 跳过验证，请按 [DocumentDB Local](/documentdb/documentdb-local/) 中的证书配置步骤操作。

## 持久化与初始化 {#persistence-and-initialization}

上述快速入门命令适用于用完即可丢弃的本地环境。需要进一步控制时：

- 将 `--data-path` 与挂载的主机目录配合使用，使数据在容器重启后得以保留
- 若需要空实例而非 `StoreData` 集合，省略 `--init-data true`
- 使用 `--init-data-path`，在启动时通过 `mongosh` 执行自己的 `.js` 初始化脚本

内置 `StoreData` 示例数据集的 `stores` 集合包含 41,505 个文档，`ratings` 集合包含 2 个文档。

## 停止、启动和移除 {#stop-start-and-remove}

```bash
docker stop documentdb       # stop, keep the data
docker start documentdb      # bring it back later
docker restart documentdb
docker logs documentdb       # gateway and startup output
```

如需更新镜像或重新开始：

```bash
# DESTROYS the container and its anonymous data volume
docker rm -fv documentdb
docker pull ghcr.io/documentdb/documentdb/documentdb-local:latest
# then run the Start DocumentDB command again
```

在删除容器之前，再次执行 `docker run --name documentdb` 会失败，报错为 `Conflict. The container name "/documentdb" is already in use`。存储需要保留的数据之前，请先挂载命名卷（`-v documentdb-data:/data`）。

在现有数据卷上使用新镜像，不会更新该卷中的 DocumentDB 模式（[documentdb#773](https://github.com/documentdb/documentdb/issues/773)）。要将旧版本或 1.0 发布候选版的数据迁移到 1.0，请在新卷上启动 1.0 镜像，再重新导入数据，例如使用 `mongodump` 和 `mongorestore`。

## 故障排除与调试 {#troubleshooting-and-debugging}

如果某项功能未按预期工作：

- 确认端口 `10260` 可用，且 `docker ps` 显示容器正在运行
- 使用 `docker logs documentdb` 检查启动、认证和 TLS 错误
- 如需更详细的网关日志，请使用 `-e DOCUMENTDB_LOG_LEVEL=debug` 重新创建容器。启动时会校验 `--log-level` 选项，但该选项目前不会改变容器的日志内容；环境变量则在执行 `docker run` 时确定。`docker restart` 无法改变这两者。
- 若客户端需要验证 TLS 证书，请按 [DocumentDB Local](/documentdb/documentdb-local/) 中的证书配置流程操作
- 更完整的 shell 操作示例见 [Mongo Shell 快速入门](/documentdb/getting-started/mongo-shell-quickstart/)

## 下一步 {#next-steps}

- [Mongo Shell 快速入门](/documentdb/getting-started/mongo-shell-quickstart/)
- [Node.js 快速入门](/documentdb/getting-started/nodejs-setup/)
- [Python 快速入门](/documentdb/getting-started/python-setup/)
- [DocumentDB Local](/documentdb/documentdb-local/)
- [示例画廊](https://documentdb.io/samples)
- [Linux 软件包快速入门](/documentdb/getting-started/packages/)
- [安装 DocumentDB](https://documentdb.io/packages?method=packages)
