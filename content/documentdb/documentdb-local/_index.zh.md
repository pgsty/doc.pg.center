---
title: DocumentDB Local
description: 学习如何使用 Docker 安装和运行 DocumentDB Local，用于本地开发和测试。包含设置说明、配置选项和证书管理。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/documentdb-local/index.md
weight: 20
translation_source_sha256: 090aa3b30dd78954d7f7fcbc541e14a89f92a9e47bd3d51382118ecdd3b8c586
translation_review: AI-assisted bilingual review; 2026-11-07
---

DocumentDB Local 提供了一个轻量级、容器化的环境，用于在本地开发和测试应用程序，包括原型设计和集成测试。

以下示例使用了版本 **1.0.0** 的 PostgreSQL 17 镜像。适用于 Linux amd64 和 arm64 的 PostgreSQL 15 到 18 的镜像分别标记为 `pg15-1.0.0` 到 `pg18-1.0.0`；`latest` 指向 `pg17-1.0.0`。当需要可复现的设置时，请使用带版本标签的镜像。[1.0 版本说明](/documentdb/getting-started/release-notes-1.0/) 列出了变更内容和已知问题。

> **使用情况遥测默认开启。** 1.0 版本镜像在启动和每小时向 Scarf 报告其版本、平台和 CPU 架构。可通过 `-e DOCUMENTDB_USAGE_TELEMETRY=false` 关闭该功能。详见 [使用情况遥测](#usage-telemetry)。

## 前提条件 {#prerequisites}

- [Docker](https://www.docker.com/)

## 安装 {#installation}

使用 `docker pull` 获取 Docker 容器镜像。

```bash
docker pull ghcr.io/documentdb/documentdb/documentdb-local:pg17-1.0.0
```

## 运行 {#running}

首先在同一个终端中选择管理员凭据（此操作在 bash 和 zsh 中均有效）：

```bash
printf 'DocumentDB username: '; IFS= read -r DOCUMENTDB_USERNAME
printf 'DocumentDB password: '; IFS= read -r -s DOCUMENTDB_PASSWORD; echo
export DOCUMENTDB_USERNAME DOCUMENTDB_PASSWORD
```

然后使用 `docker run` 启动容器，并使用 `docker ps` 检查其是否正在运行：

```bash
docker run -dt -p 127.0.0.1:10260:10260 --name docdb \
  -e USERNAME="${DOCUMENTDB_USERNAME:?Set DOCUMENTDB_USERNAME first}" \
  -e PASSWORD="${DOCUMENTDB_PASSWORD:?Set DOCUMENTDB_PASSWORD first}" \
  ghcr.io/documentdb/documentdb/documentdb-local:pg17-1.0.0

docker ps
```

```output
CONTAINER ID   IMAGE                                                         COMMAND                  CREATED         STATUS                            PORTS                        NAMES
5aff734a3591   ghcr.io/documentdb/documentdb/documentdb-local:pg17-1.0.0     "/bin/bash -c '/home…"   5 seconds ago   Up 4 seconds (health: starting)   127.0.0.1:10260->10260/tcp   docdb
```

> 导出的变量将在下面的客户端示例中重复使用；如果打开新的 shell，需重新设置。这些检查可防止凭据为空时回退到镜像中公开已知的默认凭据；容器仍接受这些默认凭据，但会发出醒目的警告。凭据通过环境变量传递，因为 `--username` 和 `--password` 参数在容器进程列表中始终可见。
>
> 回环绑定仅使网关在本机上可访问。若需允许远程客户端连接，请在使用 `-p 10260:10260` 之前，通过防火墙限制端口并配置远程客户端可验证的证书。
>
> 该容器将数据库写入 `/data`，镜像中声明为 Docker 卷。上述命令未在此处挂载任何内容，因此每次 `docker run` 都会获得一个全新的匿名卷：数据不会在重新创建容器后保留，旧卷将留在主机上，直到你执行清理操作。若要持久化数据，请挂载命名卷——`-v documentdb-data:/data`——详见下表中的 `--data-path`。

### 等待容器就绪 {#wait-for-the-container-to-be-ready}

`docker ps` 在 DocumentDB 可接受连接之前就报告容器为 `Up`，此时 PostgreSQL 仍需初始化，扩展需配置，管理员用户也需创建。过早连接将导致 `MongoServerSelectionError` 或 `ECONNREFUSED` 错误。

入口点在网关启动及任何请求的数据初始化完成后打印就绪提示。请等待该提示出现后再连接。

```bash
until docker logs docdb 2>&1 | grep -q "=== DocumentDB is ready ==="; do sleep 2; done
```

首次启动通常需要几十秒。如果命令在几分钟后仍未返回，容器很可能在启动过程中退出——请中断并检查 `docker ps -a` 和 `docker logs docdb` 以查找错误。

> 请使用 `docker logs docdb` 而非 `docker logs -f docdb` 检查就绪状态。容器在其整个生命周期中将 PostgreSQL、网关和入口点日志流式输出至 stdout，因此 `-f` 永远不会返回。

### 使用 mongosh 连接 {#connect-with-mongosh}

> DocumentDB 网关端点默认在端口 `10260` 上可用。若要通过 `mongosh` 访问，运行：

```bash
mongosh localhost:10260 \
  -u "${DOCUMENTDB_USERNAME:?Set DOCUMENTDB_USERNAME first}" \
  -p \
  --authenticationMechanism SCRAM-SHA-256 \
  --tls --tlsAllowInvalidCertificates
```

```output
Current Mongosh Log ID:	690cdcb84e2e610f0f48e609
Connecting to:		mongodb://<credentials>@localhost:10260/?tls=true&tlsAllowInvalidCertificates=true&directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.5.1
Using MongoDB:		7.0.0
Using Mongosh:		2.5.1
mongosh 2.5.9 is available for download: https://www.mongodb.com/try/download/shell

For mongosh info see: https://www.mongodb.com/docs/mongodb-shell/

[direct: mongos] test>
```

## Docker 命令 {#docker-commands}

下表总结了用于配置模拟器的可用 Docker 命令。该表详细说明了每个命令对应的参数、环境变量、允许值、默认设置及描述。

| 要求 | 参数 | 环境变量 | 允许值 | 默认值 | 描述 |
|---|---|---|---|---|---|
| 从容器将设置信息打印到 stdout | `--help`, `-h` | N/A | N/A | N/A | 显示可用配置信息 |
| 指定 DocumentDB 的用户名。 | `--username [value]` | 覆盖 `USERNAME` 环境变量 | 字符串 | `default_user` | DocumentDB 的用户名。不得为内部 DocumentDB 角色名称，且不得以 `documentdb`、`citus`、`pg` 或 `internal_role` 开头（不区分大小写）。容器会拒绝保留名称并在启动前退出。 |
| 指定 DocumentDB 的密码。 | `--password [value]` | 覆盖 `PASSWORD` 环境变量 | 字符串 | `Admin100` | DocumentDB 的密码。必须显式设置。内置默认密码广为人知，任何能访问映射到主机的端口的人都可使用它进行认证。当密码保持默认时，容器会在启动时打印警告；`DOCUMENTDB_ALLOW_DEFAULT_PASSWORD=true` 可禁用该警告。优先使用环境变量：`--password` 参数在容器进程列表中始终可见。在现有数据卷上更改密码将被忽略；卷将保留初始化时的管理员用户。 |
| DocumentDB 端点的端口。 | `--documentdb-port [value]` | 覆盖 `DOCUMENTDB_PORT` 环境变量 | 整数 | `10260` | 必须将该端口映射到主机。用于本地使用时，仅绑定回环地址——例如，`-p 127.0.0.1:10260:10260`。若要使用主机端口 `27017` 而不更改网关端口，使用 `-p 127.0.0.1:27017:10260` 进行映射；仅在同时更改容器端口时才添加 `--documentdb-port 27017`。 |
| 指定数据目录。 | `--data-path [value]` | 覆盖 `DATA_PATH` 环境变量。 | 字符串 | `/data` | 数据不会持久化，除非在此路径挂载卷——例如，`-v documentdb-data:/data`。若要使用不同目录，需同时设置挂载和标志，注意它们位于镜像名称的两侧：`-v` / `--mount` 是 `docker run` 选项，位于镜像名称前；`--data-path` 是容器参数，位于镜像名称后。详见下表下方的示例。 |
| 指定所有者。 | `--owner [value]` | 覆盖 `OWNER` 环境变量。 | 字符串 | `documentdb` | 用于创建管理员用户的 PostgreSQL 角色。该镜像初始化的集群只有一个超级用户角色 `documentdb`，因此请保持默认值：任何其他值在 PostgreSQL 初始化后都会导致 `role "<value>" does not exist` 错误，容器将退出。 |
| 指定是否启动 PostgreSQL 服务器。 | `--start-pg [value]` | 覆盖 `START_POSTGRESQL` 环境变量 | `true`, `false` | `true` | 仅当网关连接到自行运行的 PostgreSQL 服务器时，才将此选项设为 `false`；此时容器期望能通过 `--pg-port` 连接到该服务器。 |
| 指定是否创建用户。 | `--create-user [value]` | 覆盖 `CREATE_USER` 环境变量 | `true`, `false` | `true` | 使用 `false` 时，容器将以不创建管理员用户的方式启动网关。在你手动创建用户之前，无法通过 `--username` / `--password` 进行认证，且若启用数据初始化，则初始化会失败。 |
| 指定 PostgreSQL 服务器的端口。 | `--pg-port [value]` | 覆盖 `POSTGRESQL_PORT` 环境变量 | 整数 | `9712` | 指定 PostgreSQL 服务器的端口。 |
| 指定是否允许外部连接到 PostgreSQL。 | `--allow-external-connections [value]` | 覆盖 `ALLOW_EXTERNAL_CONNECTIONS` 环境变量 | `true`, `false` | `false` | 使容器内 PostgreSQL 服务器监听所有接口，并添加宽松的基于主机的认证规则（`host all all 0.0.0.0/0 scram-sha-256` 和 `host all all ::0/0 scram-sha-256`），允许任何角色从任意地址使用密码访问任意数据库。此设置仅更改容器内部的配置，因此还需将 PostgreSQL 端口映射到主机——例如 `-p 9712:9712`——才能从主机连接。当 `--start-pg false` 时被忽略。这不会影响网关，网关始终在 DocumentDB 端口上监听所有接口。 |
| 指定用于保护流量的证书路径。 | `--cert-path [value]` | 覆盖 `CERT_PATH` 环境变量。 | STRING | NA | PEM 格式证书。必须与 `--key-file` 一同设置——仅设置其中一个会在启动时失败。你需要将此文件挂载到容器中。例如，要设置 `/mycert.pem`，请将此选项添加到 `docker run` 命令中：`--mount type=bind,source=./mycert.pem,target=/mycert.pem`。 |
| 使用密钥文件中的密钥覆盖默认密钥。 | `--key-file [value]` | 覆盖 `KEY_FILE` 环境变量。 | STRING | NA | PEM 格式私钥。必须与 `--cert-path` 一同设置——仅设置其中一个会在启动时失败。你需要将此文件挂载到容器中。例如，要设置 `/mykey.key`，请将此选项添加到 `docker run` 命令中：`--mount type=bind,source=./mykey.key,target=/mykey.key` |
| 设置客户端连接的 TLS 模式。 | `--tlsMode [value]` | 覆盖 `TLS_MODE` 环境变量 | `disabled`, `allowTLS`, `requireTLS` | `allowTLS` | 使用 `allowTLS` 时，网关同时接受明文和 TLS 连接；`disabled` 行为相同。`requireTLS` 拒绝明文连接，因此每个客户端必须使用 `tls=true` 进行连接。 |
| 启用内置示例数据的初始化。 | `--init-data [value]` | 覆盖 `INIT_DATA` 环境变量 | `true`, `false` | `false` | 每个数据卷只加载一次 `StoreData` 数据集：卷内的标记文件记录是否执行过加载，因此即使卷内已有数据，只要从未加载过示例数据，也会执行加载。要再次加载示例数据，需使用新卷；参见[内置示例数据](#built-in-sample-data)。 |
| 指定用于数据库初始化的脚本目录。 | `--init-data-path [value]` | 覆盖 `INIT_DATA_PATH` 环境变量 | STRING | `/init_doc_db.d` | JavaScript 文件按字母顺序使用 `mongosh` 执行，每个数据卷执行一次（标记文件记录尝试情况，因此也会在从未运行过的现有卷上执行），在启用内置示例数据时，其执行顺序在后者之前。遇到语法或运行时错误时，容器会报错并停止。重启时不会重复执行，因此需修复脚本并从全新卷启动。 |
| 跳过内置示例数据的初始化。 | `--skip-init-data` | 覆盖 `SKIP_INIT_DATA` 环境变量 | `true`, `false`（仅 `SKIP_INIT_DATA` 有效——该标志本身不带值） | N/A | `--init-data false` 的旧版别名。注意 `SKIP_INIT_DATA=false` 的作用与该标志相反：当 `INIT_DATA` 未设置时，启用内置示例数据。不影响 `--init-data-path`。 |
| 禁用索引的扩展 RUM。 | `--disable-extended-rum` | 覆盖 `DISABLE_EXTENDED_RUM` 环境变量 | N/A（不带值） | N/A | **已弃用且被忽略**，仅在启动时发出警告；将在后续版本中移除。`documentdb_extended_rum` 在此镜像初始化的卷上始终启用。 |
| 启用遥测数据。 | `--enable-telemetry [value]` | 覆盖 `ENABLE_TELEMETRY` 环境变量 | `true`, `false` | `false` | 网关的运行指标，与 [使用情况遥测](#usage-telemetry) 无关。**已知问题**：值在启动时验证，但当前不产生遥测数据——网关的指标和追踪导出器在此镜像中被禁用，无效值只会导致启动中止。 |
| 指定日志详细程度。 | `--log-level [value]` | 覆盖 `LOG_LEVEL` 环境变量。 | `quiet`, `error`, `warn`, `info`, `debug`, `trace` | `info` | **已知问题**：值在启动时验证，但当前不会改变容器的日志输出。要更改网关自身的详细程度，请设置 `DOCUMENTDB_LOG_LEVEL` 环境变量；其值为追踪过滤器，例如 `info` 或 `debug`（`quiet` 不是其有效值）。 |
| 打开或关闭使用情况遥测。 | `--usage-telemetry [value]` | 覆盖 `DOCUMENTDB_USAGE_TELEMETRY` 环境变量 | `true`, `false`（也支持 `1`/`0`、`yes`/`no`、`on`/`off`，不区分大小写） | `true` | 在启动和每小时报告镜像版本、平台和 CPU 架构。无法识别的值将被视为 `false` 并发出警告，因此选择关闭遥测不会导致容器无法启动。参见 [使用情况遥测](#usage-telemetry)。 |
| 关闭使用情况遥测。 | `--disable-usage-telemetry` | N/A | N/A（不带值） | N/A | 与 `--usage-telemetry false` 相同。 |
| 设置 TOAST 压缩方式。 | `--toast-compression [value]` | 覆盖 `DOCUMENTDB_TOAST_COMPRESSION` 环境变量 | `lz4`, `pglz`, `default` | `lz4` | PostgreSQL 行外存储（TOAST）大值时采用的压缩方式。`lz4` 解压大文档的速度更快，`pglz` 是 PostgreSQL 内置方法，`default` 保留服务器自身的设置。仅影响新写入的值。指定 `--start-pg false` 时会忽略此选项并发出警告。 |
{.wide .expand}

> `--skip-init-data`、`--disable-usage-telemetry` 和 `--disable-extended-rum` 是仅有的三个不接收值的选项。如果仍给它们传值，例如 `--disable-usage-telemetry false`，就会被当作未知选项拒绝，容器随即退出。

一个完整的 `docker run` 显示了每种选项的位置——Docker 选项在镜像名称之前，容器参数在之后。这是上述 **运行** 部分中的命令，添加了持久化卷和示例数据，因此请先使用 `docker rm -f docdb` 删除该容器：

```bash
docker run -dt \
  -p 127.0.0.1:10260:10260 \
  -v documentdb-data:/data \
  --name docdb \
  -e USERNAME="${DOCUMENTDB_USERNAME:?Set DOCUMENTDB_USERNAME first}" \
  -e PASSWORD="${DOCUMENTDB_PASSWORD:?Set DOCUMENTDB_PASSWORD first}" \
  ghcr.io/documentdb/documentdb/documentdb-local:pg17-1.0.0 \
  --init-data true
```

## 使用情况遥测 {#usage-telemetry}

1.0 版本的镜像默认发送使用情况数据。原生包则不发送任何数据。

在启动时以及每小时一次，镜像会向 [Scarf](https://scarf.sh) 报告其版本、平台和 CPU 架构。它从不发送数据库名、集合名或用户名、查询、文档或凭据。Scarf 会看到每个请求的源 IP 地址，隐私声明指出，一旦收到该地址，就不应假设其为匿名。容器日志中的 `[TELEMETRY]` 通知会在使用情况遥测开启时提示这一状态。

要关闭此功能，请在镜像名称前添加以下任意一项：

```bash
-e DOCUMENTDB_USAGE_TELEMETRY=false
-e NO_ANALYTICS=1
-e DO_NOT_TRACK=1
```

或在镜像名称后添加 `--disable-usage-telemetry`（或 `--usage-telemetry false`）。`NO_ANALYTICS` 和 `DO_NOT_TRACK` 会覆盖任何开启此功能的设置。若要将报告发送至你自己的收集器，请设置 `DOCUMENTDB_USAGE_TELEMETRY_ENDPOINT`。

在 CI 环境中，请显式关闭此功能，使用 `-e DOCUMENTDB_USAGE_TELEMETRY=false`。镜像仅在容器自身环境中设置了非空值的 `CI`、`GITHUB_ACTIONS` 或 `TF_BUILD` 时跳过遥测，并且 `docker run` 不传递运行器的变量：在 CI 运行器上启动的容器仍会报告，除非你显式转发一个变量，例如 `-e GITHUB_ACTIONS`。`--enable-telemetry` 是网关自身指标的独立设置，不影响此功能。

详细信息请参见 [隐私声明](https://github.com/documentdb/documentdb/blob/v1.0-0/documentdb-local/PRIVACY.md)。镜像还将其包含在 `/home/documentdb/PRIVACY.md` 处。

## 内置示例数据 {#built-in-sample-data}

内置示例数据是 `StoreData` 数据集。加载该数据为可选操作：在容器参数中添加 `--init-data true`，如上例所示。如果你还提供了 `--init-data-path` 中的脚本，则两者都会运行：先执行你的脚本，再加载示例数据，每个操作都由卷中的独立标记追踪。

| 集合 | 文档数 |
|---|---:|
| `StoreData.stores` | 41,505 |
| `StoreData.ratings` | 2 |

捆绑的扩展 JSON 保留了 BSON 二进制、日期和时间戳值。在就绪提示之后，使用 `mongosh` 检查集合：

```javascript
db.getSiblingDB("StoreData").stores.countDocuments({})   // 41505
db.getSiblingDB("StoreData").ratings.countDocuments({})  // 2
```

每个数据卷只加载一次示例数据；要重新加载，请使用新的空卷。直接重新运行加载器时，它会容忍重复键，不会生成重复文档。手动运行加载器的说明见[对应版本的示例数据指南](https://github.com/documentdb/documentdb/tree/v1.0-0/documentdb-local/sample-data)。

## 容器生命周期 {#container-lifecycle}

- **健康检查。** 该镜像包含 Docker 健康检查。DocumentDB 能够接受连接后，`docker inspect -f '{{.State.Health.Status}}' docdb` 会报告 `healthy`。
- **失效的 `postmaster.pid`。** 在 `docker kill`、`docker rm -f`、因内存不足被终止或主机崩溃后，下次启动会移除失效文件，但前提是卷上的锁表明该文件由 1.0 容器写入。否则，容器会拒绝启动，因为旧容器可能仍在使用该卷。确认没有其他进程或容器使用该卷后，先带上 `-e DOCUMENTDB_FORCE_REMOVE_STALE_POSTMASTER_PID=true` 重新创建一次容器，随后再去掉该变量重新创建容器（`docker start` 无法添加该变量）。不要在不同主机间共享卷。在已被使用的卷上启动第二个容器会使其立即退出。
- **PostgreSQL 停止会使容器停止。** 如果容器内的 PostgreSQL 停止，网关会立即使请求失败，容器则会在 20 秒后（`DOCUMENTDB_POSTMASTER_EXIT_TIMEOUT`）退出，以便重启策略将其恢复。

## 升级镜像 {#upgrading-the-image}

在现有数据卷上使用新镜像不会更新其中的 DocumentDB 扩展（[#773](https://github.com/documentdb/documentdb/issues/773)），因此卷会保留旧的模式，而使用新的二进制文件。1.0 版本不支持就地升级卷。要将数据从 0.117 容器迁移到 1.0，使用 `mongodump` 导出数据，然后在新卷上启动 1.0 容器，并使用 `mongorestore` 加载数据。镜像的 PostgreSQL 主版本必须与初始化卷的版本匹配。

如果你在旧容器使用过的卷上启动 1.0 镜像，只要旧容器的 `postmaster.pid` 仍存在，1.0 镜像将拒绝启动；请参见 [容器生命周期](#container-lifecycle) 了解如何临时覆盖此检查，以及之后如何移除覆盖设置。对于 0.116 和 0.117 版本，请先使用 `docker stop` 停止旧容器，这会移除该文件；在 `docker kill`、`docker rm -f` 或崩溃后，该文件将保留。0.114 及更早版本的镜像通常不会干净地停止 PostgreSQL，因此其卷通常会保留该文件。

## 功能支持 {#feature-support}

请参阅 [documentdb](/documentdb/) 文档以了解当前支持的功能。


## 安装证书 {#installing-certificates}

如果你未使用 `--cert-path` 和 `--key-file` 提供自己的证书，DocumentDB Local 会在首次启动时生成一个自签名证书，并在相同容器的后续启动中重复使用该证书，因此 `docker stop` / `docker start` 可保持其稳定。删除并重新创建容器会生成新证书，除非你持久化存储该证书的目录。生成的证书有效期为 365 天，不会自动续期——重新创建容器，或从下述状态目录中删除 `cert.pem`，即可生成新证书。

若要验证证书，而不使用 `tlsAllowInvalidCertificates=true` 跳过验证，请先将证书从容器复制出来，再让 `mongosh` 使用该证书。

### 获取证书 {#get-certificate}

网关从第一个可写候选路径中选择其 TLS 状态目录。在本镜像中，该路径位于容器用户的主目录下，因此启动容器时无需额外选项。在 `bash` 窗口中，将证书从容器复制到本地主机：

```bash
docker cp docdb:/home/documentdb/.local/state/documentdb-gateway/tls/cert.pem ~/documentdb-cert.pem
```

网关启动时会在日志中记录实际选择的路径。如果复制操作报告 `No such container:path`，请先查看日志：

```bash
docker logs docdb | grep "TLS auto-gen"
```

为在重新创建容器时保持相同的证书，请使用 `DOCUMENTDB_TLS_STATE_DIR` 固定位置，并将其置于数据卷内。这将替换你之前启动的容器，因此请先运行 `docker rm -f docdb`：

```bash
docker run -dt \
  -p 127.0.0.1:10260:10260 \
  -v documentdb-data:/data \
  -e DOCUMENTDB_TLS_STATE_DIR=/data/tls \
  --name docdb \
  -e USERNAME="${DOCUMENTDB_USERNAME:?Set DOCUMENTDB_USERNAME first}" \
  -e PASSWORD="${DOCUMENTDB_PASSWORD:?Set DOCUMENTDB_PASSWORD first}" \
  ghcr.io/documentdb/documentdb/documentdb-local:pg17-1.0.0
```

请将路径指向数据目录内部，而非单独的卷：单独创建的卷由 root 拥有，而网关（以非特权用户运行）无法向该目录写入密钥。权衡之处在于，密钥会包含在数据卷的任何备份中。如果入口点必须修复数据目录的所有权（当所有者不匹配，或遇到 `DOCUMENTDB_FORCE_OWNERSHIP_REPAIR=true` 时会执行此操作），它将对目录运行 `chmod -R 750`，这会导致私钥变为组可读，而非仅所有者可读。

### 在 mongosh 中使用证书 {#use-the-certificate-with-mongosh}

```bash
mongosh localhost:10260 \
  -u "${DOCUMENTDB_USERNAME:?Set DOCUMENTDB_USERNAME first}" \
  -p \
  --authenticationMechanism SCRAM-SHA-256 \
  --tls --tlsCAFile ~/documentdb-cert.pem
```

```output
Current Mongosh Log ID:	690ce1171181053c6edbf354
Connecting to:		mongodb://<credentials>@localhost:10260/?directConnection=true&serverSelectionTimeoutMS=2000&authMechanism=SCRAM-SHA-256&tls=true&tlsCAFile=%2Fhome%2Fuser%2Fdocumentdb-cert.pem&appName=mongosh+2.5.1
Using MongoDB:		7.0.0
Using Mongosh:		2.5.1
mongosh 2.5.9 is available for download: https://www.mongodb.com/try/download/shell

For mongosh info see: https://www.mongodb.com/docs/mongodb-shell/

[direct: mongos] test>
```


## 超出本地开发范围 {#beyond-local-development}

DocumentDB Local 在单台机器上运行单个容器，不支持复制和故障切换，这使其适用于开发和测试。若需以其他方式运行 DocumentDB：

- [Kubernetes Operator](/documentdb/kubernetes-operator/) - 以启用复制的服务形式运行 DocumentDB，支持自动故障切换、备份与恢复以及滚动升级。
- [预编译软件包](/documentdb/getting-started/packages/) - 将 DocumentDB 扩展添加到你已运行的 PostgreSQL 服务器中。


## 报告问题 {#reporting-issues}

如果你在使用此版本的 DocumentDB 时遇到问题，请在 GitHub 仓库 (<https://github.com/documentdb/documentdb/issues>) 中打开一个问题，并添加标签 `documentdb-local`。
