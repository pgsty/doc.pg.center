---
title: 兼容性命令
description: 描述 DocumentDB 兼容线协议命令的简单响应。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/diagnostic/compatibility.md
weight: 30
translation_source_sha256: efed95c9f7c112ab0be4b261f5f2a6adddccba29c55240999583bb3a94978cc2
translation_review: AI-assisted bilingual review; 2026-11-07
---

这些命令具有网关处理程序，但并未实现其 MongoDB 名称所暗示的所有行为。除非另有说明，否则命令特定选项不会改变其响应。

## 状态和信息命令 {#status-and-information-commands}

| 命令 | 调用方式 | 实现的行为 |
| --- | --- | --- |
| `ping` | `{ ping: 1 }` | 返回 `{ ok: 1 }`；检查网关的响应性，而非数据库健康状态。 |
| `buildInfo` | `{ buildInfo: 1 }` | 返回配置的 MongoDB 兼容 `version`、`versionArray`、`bits: 64` 和 `maxBsonObjectSize`。`buildinfo` 是别名。使用 [`hello`](/documentdb/reference/commands/diagnostic/hello/) 获取引擎版本。 |
| `getCmdLineOpts` | `{ getCmdLineOpts: 1 }` | 返回空的 `argv` 数组，而非网关的实际启动参数。 |
| `getLog` | `{ getLog: "global" }` | 返回空的 `log` 和 `totalLinesWritten: 0`；不暴露服务器日志，也不实现日志名称选择。 |
| `hostInfo` | `{ hostInfo: 1 }` | 返回当前时间，包含占位符内存、操作系统和 CPU 字段。 |
| `isdbgrid` | `{ isdbgrid: 1 }` | 返回 `isdbgrid: 1` 和配置的主机名。并非完整的分片健康检查。 |
| `whatsmyuri` | `{ whatsmyuri: 1 }` | 仅返回 `{ ok: 1 }`；不返回客户端 URI。 |

例如：

```javascript
db.runCommand({ ping: 1 })
db.serverBuildInfo()
```

<span id="get-default-rw-concern"></span>

## getDefaultRWConcern {#getdefaultrwconcern}

在 `admin` 上运行：

```javascript
db.adminCommand({ getDefaultRWConcern: 1 })
```

响应始终报告隐式的 `majority` 读关注级别和写关注级别，以及 `wtimeout: 0`。这是固定的兼容性响应，并不能证明实现了任意命令级别的关注选项。

## 其他无操作命令 {#other-no-ops}

`enableSharding` 返回成功，但不会启用数据库级别的分片状态。`refreshSessions` 和 `killAllSessionsByPattern` 返回成功，但不会刷新或终止会话。其命令参数不会用于执行这些操作。有关实际终止会话的命令，请参阅 [会话命令](/documentdb/reference/commands/sessions/session-commands/)。

参见 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。源码：网关 `processor/constant.rs` 和 `processor/process.rs`。
