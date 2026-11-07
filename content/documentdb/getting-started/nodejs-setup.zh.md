---
title: Node.js 快速入门
description: 使用 MongoDB Node.js 驱动程序通过 Docker 或 Linux 软件包连接到 DocumentDB，并运行你的首个查询。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/documentdb.github.io/blob/90cfa088351557cd618034dfc00ab817c35a5f76/app/services/articleService.ts
upstream_ref: website 90cfa08; DocumentDB 1.0
weight: 50
translation_source_sha256: 8db08a9337e44841f0f5ddbb3c32ba4c4e91dab2e51a8bac275885863cb15400
translation_review: AI-assisted bilingual review; 2026-11-07
---

使用官方 MongoDB 驱动程序从 Node.js 连接到 DocumentDB。

<span id="have-a-running-document-db-instance"></span>

## 是否已有正在运行的 DocumentDB 实例？ {#have-a-running-documentdb-instance}

如果已有实例，请继续使用它，并按下文准备客户端依赖。否则，请选择一种服务器安装方式：

- [Docker](https://documentdb.io/packages?method=docker)：在 Linux、macOS 或 Windows 上运行本地容器，推荐用于试用和开发。
- [Linux 软件包](https://documentdb.io/packages?method=packages)：安装全套组件，再通过配置向导创建私有 PostgreSQL 实例。

[Docker 快速入门](/documentdb/getting-started/docker/) 和 [Linux 软件包快速入门](/documentdb/getting-started/packages/) 包含完整的服务器操作说明。如果已有实例在运行，请勿启动第二个实例。

示例连接到 `localhost:10260`，所以客户端应当在 DocumentDB 所在主机上运行。Docker 使用自己设置的凭据；Linux 软件包使用用户名 `admin`，以及配置时设置的密码。如果修改过端点，请使用实际配置的主机和端口。

下文跳过自签名证书验证的做法**仅适用于本地开发**。通过网络访问时，请使用受信任的证书。Linux 软件包的配置向导默认将网关绑定到**所有网络接口**：配置前请用防火墙限制对端口 `10260` 的访问，并遵循[网络与证书指南](/documentdb/linux-packages/#before-exposing-it-to-a-network)。Docker 示例仅将端口映射到回环接口。


## 前提条件 {#prerequisites}

- Node.js 20.19 或更高版本（当前 `mongodb` 驱动程序的要求）
- npm
- 对 JavaScript 的基本了解

## 设置客户端凭据 {#set-your-client-credentials}

在运行应用程序的终端中设置这些凭据。将占位符替换为现有实例的凭据（Linux 软件包使用 `admin` 和配置时设置的密码）。驱动会直接传递原始值，不会将它们嵌入连接 URI。

```bash
export DOCUMENTDB_USERNAME='<YOUR_USERNAME>'
export DOCUMENTDB_PASSWORD='<YOUR_PASSWORD>'
```


## 可选：启动一个 Docker 实例 {#optional-start-a-docker-instance}

已经安装 Linux 软件包或已有运行中的实例时，请跳过此步骤。若选择 Docker，并且已经安装 [Docker](https://www.docker.com/)，请将下文的占位符替换为自己设置的凭据。下面这条完整命令还会设置应用程序读取的环境变量：

```bash
export DOCUMENTDB_USERNAME='<YOUR_USERNAME>'
export DOCUMENTDB_PASSWORD='<YOUR_PASSWORD>'

docker run -dt --pull always --name documentdb \
  -p 127.0.0.1:10260:10260 \
  -e USERNAME="${DOCUMENTDB_USERNAME:?Set DOCUMENTDB_USERNAME}" \
  -e PASSWORD="${DOCUMENTDB_PASSWORD:?Set DOCUMENTDB_PASSWORD}" \
  ghcr.io/documentdb/documentdb/documentdb-local:latest
```

> [!NOTE]
> DocumentDB Local 镜像默认发送使用情况遥测数据。若要关闭，请在镜像名称前添加 `-e DOCUMENTDB_USAGE_TELEMETRY=false`。参见[使用情况遥测](/documentdb/documentdb-local/#usage-telemetry)和[隐私声明](https://github.com/documentdb/documentdb/blob/v1.0-0/documentdb-local/PRIVACY.md)。

等到 `docker logs documentdb` 中出现就绪提示后再连接，参见 [Docker 快速入门](/documentdb/getting-started/docker/#verify-the-container)。

## 创建项目 {#create-a-project}

```bash
mkdir my-documentdb-app
cd my-documentdb-app
npm init -y
npm install mongodb
```

## 连接并运行你的首个查询 {#connect-and-run-your-first-queries}

创建 `index.js` 文件。示例使用 Linux 软件包配置或 Docker 提供的默认自签名证书，跳过证书验证的做法**仅适用于本地开发**。

```javascript
const { MongoClient } = require("mongodb");

const username = process.env.DOCUMENTDB_USERNAME;
const password = process.env.DOCUMENTDB_PASSWORD;

if (!username || !password) {
  throw new Error(
    "Set DOCUMENTDB_USERNAME and DOCUMENTDB_PASSWORD before running this script"
  );
}

const uri = "mongodb://localhost:10260/";
const options = {
  auth: { username, password },
  authSource: "admin",
  tls: true,
  tlsAllowInvalidCertificates: true,
  directConnection: true
};

async function main() {
  const client = new MongoClient(uri, options);

  try {
    await client.connect();

    const db = client.db("quickstart");
    await db.command({ ping: 1 });

    const movies = db.collection("movies");

    await movies.insertMany([
      { title: "The Matrix", year: 1999, genres: ["sci-fi", "action"] },
      { title: "Dune", year: 2021, genres: ["sci-fi", "adventure"] },
      { title: "Arrival", year: 2016, genres: ["sci-fi", "drama"] }
    ]);

    await movies.createIndex({ title: 1 });

    const recentMovies = await movies
      .find(
        { year: { $gte: 2000 } },
        { projection: { _id: 0, title: 1, year: 1 } }
      )
      .sort({ year: -1 })
      .toArray();

    console.log("Connected to DocumentDB");
    console.log(recentMovies);
  } finally {
    await client.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
```

运行脚本：

```bash
node index.js
```

## 改用受信任的本地证书连接 {#connect-with-a-trusted-local-certificate-instead}

若要验证证书，而不使用 `tlsAllowInvalidCertificates=true` 跳过验证，请取得端点对应的受信任证书或 CA 文件，并将原来的 `options` 对象替换为下文的版本。Linux 软件包用户请按[证书配置](/documentdb/linux-packages/#before-exposing-it-to-a-network)操作；Docker 用户可以用以下命令复制本地证书：

```bash
docker cp documentdb:/home/documentdb/.local/state/documentdb-gateway/tls/cert.pem ~/documentdb-cert.pem
```

```javascript
const options = {
  auth: { username, password },
  authSource: "admin",
  tls: true,
  tlsCAFile: "/absolute/path/documentdb-cert.pem",
  directConnection: true
};
```

## 后续步骤 {#next-steps}

- [Mongo Shell 快速入门](/documentdb/getting-started/mongo-shell-quickstart/)
- [Python 快速入门](/documentdb/getting-started/python-setup/)
- [DocumentDB Local](/documentdb/documentdb-local/)
- [示例画廊](https://documentdb.io/samples)
