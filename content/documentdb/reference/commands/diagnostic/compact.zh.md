---
title: compact
description: 运行集合维护、更新统计信息，或估算 DocumentDB 中可回收的存储空间。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/diagnostic/compact.md
weight: 20
translation_source_sha256: 652d8c2aeeb9d4d8352378816862d4b8b77c6ef2699562459b7b043fad511fc2
translation_review: AI-assisted bilingual review; 2026-11-07
---

运行集合维护或估算可回收空间。

```javascript
db.runCommand({ compact: "flights", dryRun: true })
db.runCommand({ compact: "flights", mode: "updateStats" })
```

| 参数 | 描述 |
| --- | --- |
| **`compact`** | (必需) 指定集合名称的字符串。 |
| **`dryRun`** | (可选) 布尔值，返回 `estimatedBytesFreed` 而不执行压实；默认值为 `false`。不可与 `mode: "updateStats"` 同时使用。 |
| **`freeSpaceTargetMB`** | (可选) 当估算可回收空间低于此正数阈值（单位：MB）时跳过压实。 |
| **`mode`** | (可选) 作为 DocumentDB 扩展提供的字符串：`standard`（默认）执行普通清理，`full` 请求阻塞式表重写，`updateStats` 刷新规划器统计信息。 |
{.fields}

完全压实要求服务器启用完整清理功能。关闭时，`mode: "full"` 会返回成功及 `bytesFreed: 0`，但不会重写集合。试运行和标准维护不要求启用该功能。操作必须通过集合维护权限检查。

参见 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。源码：`pg_documentdb/src/commands/compact.c`、`ParseCompactCommandSpec` 和 `command_compact`。
