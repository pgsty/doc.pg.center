---
title: killOp
description: 使用由 currentOp 报告的字符串标识符取消 DocumentDB 操作。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/diagnostic/killOp.md
weight: 80
translation_source_sha256: dbeb5de5134bcdb10ebe4b170514ef084f096ba0cfa56f9331f708f822eb6a21
translation_review: AI-assisted bilingual review; 2026-11-07
---

请求取消正在运行的操作。请在 `admin` 上执行。

```javascript
const flightOps = db.currentOp({
  active: true,
  ns: "bookings.flights"
}).inprog
if (flightOps.length > 0) {
  db.killOp(flightOps[0].opid)
}
```

| 参数 | 描述 |
| --- | --- |
| **`killOp`** | (必需) 命令标记，通常为 `1`。 |
| **`op`** | (必需) 指定由 [`currentOp`](/documentdb/reference/commands/diagnostic/currentop/) 报告的操作标识符的字符串。数值标识符会被网关拒绝。 |
{.fields}

取消操作受服务器授权限制。参见 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。

源码：网关 `processor/data_management.rs`、`process_kill_op` 和 `pg_documentdb/src/commands/kill_op.c`。
