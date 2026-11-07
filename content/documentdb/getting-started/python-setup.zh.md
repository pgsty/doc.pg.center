---
title: Python 快速入门
description: 使用 Docker 或 Linux 软件包通过 PyMongo 连接到 DocumentDB，并从 Python 运行你的首个查询。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/documentdb.github.io/blob/90cfa088351557cd618034dfc00ab817c35a5f76/app/services/articleService.ts
upstream_ref: website 90cfa08; DocumentDB 1.0
weight: 60
translation_source_sha256: 589ee0f5e1fb0e08c1cf1f006210e43ad0d1cf2af059f51b22effa8f826a2979
translation_review: AI-assisted bilingual review; 2026-11-07
---

使用 PyMongo 连接 DocumentDB，验证认证和 TLS，并在 Python 中执行第一次文档查询。

<span id="have-a-running-document-db-instance"></span>

## 是否已有正在运行的 DocumentDB 实例？ {#have-a-running-documentdb-instance}

如果已有实例，请继续使用它，并按下文准备客户端依赖。否则，请选择一种服务器安装方式：

- [Docker](https://documentdb.io/packages?method=docker)：在 Linux、macOS 或 Windows 上运行本地容器，推荐用于试用和开发。
- [Linux 软件包](https://documentdb.io/packages?method=packages)：安装全套组件，再通过配置向导创建私有 PostgreSQL 实例。

[Docker 快速入门](/documentdb/getting-started/docker/) 和 [Linux 软件包快速入门](/documentdb/getting-started/packages/) 包含完整的服务器操作说明。如果已有实例在运行，请勿启动第二个实例。

示例连接到 `localhost:10260`，所以客户端应当在 DocumentDB 所在主机上运行。Docker 使用自己设置的凭据；Linux 软件包使用用户名 `admin`，以及配置时设置的密码。如果修改过端点，请使用实际配置的主机和端口。

下文跳过自签名证书验证的做法**仅适用于本地开发**。通过网络访问时，请使用受信任的证书。Linux 软件包的配置向导默认将网关绑定到**所有网络接口**：配置前请用防火墙限制对端口 `10260` 的访问，并遵循[网络与证书指南](/documentdb/linux-packages/#before-exposing-it-to-a-network)。Docker 示例仅将端口映射到回环接口。


## 前提条件 {#prerequisites}

- Python 3.9 或更高版本
- pip
- 可选：[mongosh](https://www.mongodb.com/docs/mongodb-shell/install/) 用于独立连接检查

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

## 创建虚拟环境（可选） {#create-a-virtual-environment-optional}

```bash
python3 -m venv .venv
source .venv/bin/activate
```

如果你不使用虚拟环境，请使用计划用于应用程序的 Python 解释器运行接下来的命令。

<span id="install-py-mongo"></span>

## 安装 PyMongo {#install-pymongo}

```bash
python -m pip install pymongo
```

> PyMongo 已包含其所需的 `bson` 包。请勿从 PyPI 单独安装 `bson` 包。

## 连接并运行你的首个查询 {#connect-and-run-your-first-queries}

创建 `quickstart.py` 文件。示例使用 Linux 软件包配置或 Docker 提供的默认自签名证书，跳过证书验证的做法**仅适用于本地开发**。

```python
import os

from pymongo import MongoClient

username = os.environ.get("DOCUMENTDB_USERNAME")
password = os.environ.get("DOCUMENTDB_PASSWORD")

if not username or not password:
    raise RuntimeError(
        "Set DOCUMENTDB_USERNAME and DOCUMENTDB_PASSWORD before running this script"
    )

client = MongoClient(
    "mongodb://localhost:10260/",
    username=username,
    password=password,
    authSource="admin",
    tls=True,
    tlsAllowInvalidCertificates=True,
)

try:
    client.admin.command("ping")

    db = client["quickstart"]
    movies = db["movies"]

    movies.delete_many({})
    movies.insert_many(
        [
            {"title": "The Matrix", "year": 1999, "genres": ["sci-fi", "action"]},
            {"title": "Dune", "year": 2021, "genres": ["sci-fi", "adventure"]},
            {"title": "Arrival", "year": 2016, "genres": ["sci-fi", "drama"]},
        ]
    )

    movies.create_index("title")

    for movie in movies.find(
        {"year": {"$gte": 2000}},
        {"_id": 0, "title": 1, "year": 1},
    ).sort("year", -1):
        print(movie)
finally:
    client.close()
```

运行脚本：

```bash
python quickstart.py
```

成功执行 `ping` 后，你应能看到最近的电影文档被打印输出。

## 探索内置示例数据 {#explore-the-built-in-sample-data}

示例数据需要**主动启用**，首次插入和读取文档并不需要它。通过 Linux 软件包安装时，可在配置命令中添加 `--load-sample-data`；这需要额外安装一个工具，参见[配置并连接](/documentdb/getting-started/packages/#set-up-and-connect)。Docker 可以通过 `--init-data true` 启动。未指定这些选项时，`StoreData` 不会存在。Docker 对每个数据卷只加载一次示例数据：如果卷中从未加载过示例数据，用 `--init-data true` 重新创建容器会加载这些数据，而不影响已有数据；再次加载则需要新卷。

如果你已加载示例数据，请在 `client.admin.command("ping")` 之后添加以下代码片段：

```python
for store in client["StoreData"]["stores"].find(
    {},
    {"_id": 0, "name": 1, "city": 1, "sales.revenue": 1},
).limit(3):
    print(store)
```

## 改用受信任的本地证书 {#use-a-trusted-local-certificate-instead}

若要验证证书，而不使用 `tlsAllowInvalidCertificates=true` 跳过验证，请取得端点对应的受信任证书或 CA 文件，并将原来的 `MongoClient` 调用替换为下文的版本。Linux 软件包用户请按[证书配置](/documentdb/linux-packages/#before-exposing-it-to-a-network)操作；Docker 用户可以用以下命令复制本地证书：

```bash
docker cp documentdb:/home/documentdb/.local/state/documentdb-gateway/tls/cert.pem ~/documentdb-cert.pem
```

```python
client = MongoClient(
    "mongodb://localhost:10260/",
    username=username,
    password=password,
    authSource="admin",
    tls=True,
    tlsCAFile="/absolute/path/documentdb-cert.pem",
)
```

## 故障排除和调试 {#troubleshooting-and-debugging}

如果 Python 快速入门首次尝试未成功：

- 在启动 Python 前，确认你的本地 DocumentDB 实例正在运行
- 如果你使用了 Docker，请检查 `docker ps --filter "name=documentdb"` 和 `docker logs documentdb`
- 如果你使用了 Linux 软件包，请检查 `sudo documentdb-setup --status`；对于手动构建的网关，请确认其进程正在监听端口 `10260`
- 如果 Python 无法导入 `pymongo`，请使用 `python -c "import sys; print(sys.executable)"` 验证当前激活的解释器，并通过 `python -m pip install pymongo` 重新安装
- 如果出现 TLS 或证书错误，请使用默认本地自签名流程（通过 `tlsAllowInvalidCertificates=true`）或切换为受信任的本地证书（通过 `tlsCAFile`）
- 使用 [Mongo Shell 快速入门](/documentdb/getting-started/mongo-shell-quickstart/) 独立验证端点，与你的应用程序代码无关

## 下一步 {#next-steps}

- [Mongo Shell 快速入门](/documentdb/getting-started/mongo-shell-quickstart/)
- [Node.js 快速入门](/documentdb/getting-started/nodejs-setup/)
- [Visual Studio Code 快速入门](/documentdb/getting-started/vscode-quickstart/)
- [DocumentDB Local](/documentdb/documentdb-local/)
- [API 参考](/documentdb/reference/)
- [示例画廊](https://documentdb.io/samples)
