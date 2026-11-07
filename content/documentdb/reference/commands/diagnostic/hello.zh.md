---
title: hello
description: hello 命令返回有关 DocumentDB 服务器的信息，包括拓扑角色、线协议限制和 DocumentDB 引擎版本。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/diagnostic/hello.md
weight: 70
translation_source_sha256: e73bfb7ed0a15ed541c084085c1d977e0945417a7e12959771b8c0ac94d3da89
translation_review: AI-assisted bilingual review; 2026-11-07
---

`hello` 命令返回一个文档，描述 DocumentDB 服务器的角色，以及连接限制、支持的身份验证机制，和你所连接的 DocumentDB 引擎版本。这是从 MongoDB 客户端发现 DocumentDB 版本的推荐方式，因为 `internal.documentdb_versions` 字段报告的是底层引擎版本，而非仅模拟的 MongoDB 线协议版本。

`internal.documentdb_versions` 中的版本来自后端 DocumentDB PostgreSQL 扩展，而非网关。该数组报告两个值：已安装的 SQL 扩展版本（来自 `pg_extension` 系统目录，例如 `1.0-0`）以及已加载的二进制版本（来自 `documentdb_api.binary_version()`，以点分形式表示，例如 `1.0.0`）。在 PostgreSQL 中，已安装的扩展版本 *即* 是模式版本——它跟踪已应用的 SQL 升级脚本——因此第一个值反映了数据库中当前安装的模式。这两个值通常描述同一发行版，仅格式不同，但在升级过程中可能产生偏差——例如，在 1.0 包安装于 0.117 之上，但 `ALTER EXTENSION documentdb UPDATE` 尚未运行时。`["0.117-0", "1.0.0"]` 类似的不匹配表明 SQL 模式落后于已加载的二进制版本。

返回网关握手信息。该命令不读取集合数据，也不需要加载 airline 示例数据集。

## 示例 {#example}

```javascript
db.hello()
```

要分别检查后端版本值：

```javascript
db.hello().internal.documentdb_versions
```

这些是与部署相关的值，而非固定的示例输出。

## 请求参数 {#request-parameters}

| 参数 | 描述 |
| --- | --- |
| **`hello`** | （必需）命令标记，通常为 `1`。 |
| **`client`** | （可选）指定存储在连接上的驱动程序/应用程序元数据的文档。第二个 `client` 文档将导致 `ClientMetadataCannotBeMutated` 错误。 |
{.fields}

`isMaster` 和 `ismaster` 会到达相同的处理器，但响应中使用 `ismaster` 而非 `isWritablePrimary`。

处理器不通过 `topologyVersion` 和 `maxAwaitTimeMS` 实现可等待的 hello，也不通过 `speculativeAuthenticate` 实现推测性身份验证。请求中的 `saslSupportedMechs` 值不会选择机制：处理器报告启用的网关身份验证方案。

## 响应字段 {#response-fields}

| 字段 | 实现行为 |
| --- | --- |
| `isWritablePrimary` | 由 hello 处理器设置为 `true`。旧版处理器使用 `ismaster`。 |
| `msg` | 设置为 `isdbgrid`。 |
| `maxBsonObjectSize`, `maxMessageSizeBytes` | 网关协议限制，单位为字节。 |
| `maxWriteBatchSize` | 配置的网关写入批处理限制。 |
| `localTime` | 当前网关时间。 |
| `logicalSessionTimeoutMinutes` | 设置为 `30`。 |
| `minWireVersion`, `maxWireVersion` | 最小值为 `0`；最大值遵循配置的兼容版本。 |
| `readOnly` | 配置的连接只读状态。 |
| `connectionId` | 连接标识符。 |
| `saslSupportedMechs` | 启用的网关身份验证方案。 |
| `internal` | 配置的拓扑元数据，包括默认部署中的 `documentdb_versions`。 |
| `operationTime` | 在启用变更流时包含。 |
| `ok` | 成功标记。 |

在默认后端中，`internal.documentdb_versions` 包含已安装的 SQL 扩展版本，后跟已加载的二进制版本。第一个值跟踪已应用的 SQL 升级；第二个值标识已加载的实现。它们在升级过程中可能产生偏差。[`buildInfo`](/documentdb/reference/commands/diagnostic/compatibility/) 报告的是配置的线兼容版本，而非这些引擎版本。

## Shell 语法 {#shell-syntax}

```javascript
db.runCommand({ hello: 1 })
```

```javascript
db.hello()
```

## 详细示例 {#detailed-examples}

### 示例 1：检查服务器角色和版本 {#example-1-inspect-the-server-role-and-version}

运行 `hello` 命令以查看完整响应：

```javascript
db.runCommand({ hello: 1 })
```

服务器返回一个类似于以下内容的文档：

```json
{
  "isWritablePrimary": true,
  "msg": "isdbgrid",
  "maxBsonObjectSize": 16777216,
  "maxMessageSizeBytes": 48000000,
  "maxWriteBatchSize": 25000,
  "localTime": 1783006410548,
  "logicalSessionTimeoutMinutes": 30,
  "minWireVersion": 0,
  "maxWireVersion": 21,
  "readOnly": false,
  "connectionId": 382703778,
  "saslSupportedMechs": [
    "SCRAM-SHA-256"
  ],
  "internal": {
    "documentdb_versions": [
      "1.0-0",
      "1.0.0"
    ],
    "kind": ""
  },
  "ok": 1
}
```

<span id="example-2-determine-the-document-db-engine-version"></span>

### 示例 2：确定 DocumentDB 引擎版本 {#example-2-determine-the-documentdb-engine-version}

要仅读取 DocumentDB 引擎版本，请投影 `internal.documentdb_versions` 字段：

```javascript
db.runCommand({ hello: 1 }).internal.documentdb_versions
```

该命令返回一个数组，包含已安装的 SQL 扩展版本，后跟已加载的二进制版本：

```json
[ "1.0-0", "1.0.0" ]
```

第一个值是已安装的 SQL 扩展版本——即模式版本，来自 `pg_extension` 系统目录——第二个值是编译后的二进制版本。它们通常描述同一发行版，仅格式不同。

> [!NOTE]
> `buildInfo` 命令报告的是模拟的 MongoDB 线协议版本（例如 `7.0.0`），而非 DocumentDB 引擎版本。请使用 `hello` 并读取 `internal.documentdb_versions` 以确定 DocumentDB 版本。

## 相关内容 {#related-content}

- [DocumentDB Local](/documentdb/documentdb-local/)

## 实现 {#implementation}

源码：网关 `processor/ismaster.rs`、默认拓扑配置以及 PostgreSQL 版本信息查询。有关源码范围，请参阅 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。
