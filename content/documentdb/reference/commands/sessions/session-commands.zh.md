---
title: 会话命令
description: 终止 DocumentDB 逻辑会话。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/sessions/session-commands.md
weight: 10
translation_source_sha256: 8cfe4fd8e47003eef2db4d076b75248964032f60ea8c413eee16db82880242c2
translation_review: AI-assisted bilingual review; 2026-11-07
---

驱动程序创建逻辑会话 ID，并将其作为 `lsid` 附加。默认网关不实现显式的 `startSession` 线协议命令；这并不妨碍驱动程序管理的会话，包括 shell 的 `startSession()` 辅助函数。

<span id="end-sessions-and-kill-sessions"></span>

## endSessions 和 killSessions {#endsessions-and-killsessions}

示例将会话附加到对 [航空示例数据集](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset) 的读取操作中：

```javascript
const bookingsSession = db.getMongo().startSession()
bookingsSession.getDatabase("bookings").flights.find().limit(1).toArray()
bookingsSession.endSession()

const dispatcherSession = db.getMongo().startSession()
dispatcherSession.getDatabase("bookings").flights.find().limit(1).toArray()
db.adminCommand({ killSessions: [dispatcherSession.id] })
dispatcherSession.endSession()
```

`endSession()` 结束客户端会话；驱动程序管理服务器端会话的清理，并可池化底层服务器会话。它不保证 `endSessions` 的立即发送。没有等效的 shell 辅助函数用于显式发送 `killSessions`，因此该示例使用了管理请求。

| 参数 | 描述 |
| --- | --- |
| **`endSessions`** | (必需) 指定会话 ID 列表的文档数组。每个文档为 `{ id: <BSON UUID> }`。 |
| **`killSessions`** | (必需) 指定会话 ID 列表的文档数组。每个文档为 `{ id: <BSON UUID> }`。 |
{.fields}

两个处理器均会失效所选会话的游标并移除其事务，前提是满足所有权授权条件。启用会话参数验证后，ID 文档内的额外字段将被拒绝，必须使用 UUID 二进制子类型，且 `null` 数组元素将被忽略。空数组表示不选择任何会话。

参见 [事务命令](/documentdb/reference/commands/sessions/transaction-commands/) 和 [线协议与通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。

源码：网关 `processor/session.rs`、`processor/process.rs` 和 `requests/request_type.rs`。
