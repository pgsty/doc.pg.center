---
title: 事务命令
description: 使用 DocumentDB 会话和事务元数据提交或中止事务。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/sessions/transaction-commands.md
weight: 20
translation_source_sha256: 30e6b6ab3888e1bbedb17a4ba823a0e66486802a3394882e89b574f94a816ea0
translation_review: AI-assisted bilingual review; 2026-11-07
---

驱动程序通过在其首个操作中添加事务元数据来启动事务，而非发送单独的 begin 命令。

## 事务上下文 {#transaction-context}

使用驱动程序的事务 API 来维护匹配的 [会话和事务元数据](/documentdb/reference/commands/diagnostic/wire-protocol/#common-request-fields)。读取隔离遵循 [共享读关注级别规则](/documentdb/reference/commands/diagnostic/wire-protocol/#read-concern)。

<span id="commit-transaction-and-abort-transaction"></span>

## commitTransaction 和 abortTransaction {#committransaction-and-aborttransaction}

使用 [航空公司的示例数据集](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset)，通过一次读取启动事务并提交。会话辅助函数维护匹配的 `lsid` 和 `txnNumber` 值：

```javascript
const bookingsSession = db.getMongo().startSession({ causalConsistency: false })
const bookingsDb = bookingsSession.getDatabase("bookings")
bookingsSession.startTransaction()
bookingsDb.flights.findOne({ route_no: "PG0101" })
bookingsSession.commitTransaction()
bookingsSession.endSession()
```

使用 `bookingsSession.abortTransaction()` 而非 `commitTransaction()` 来中止事务。辅助函数不返回原始命令文档；线协议处理器在成功时返回 `ok: 1`。缺失或不存在的活动事务会产生 `NoSuchTransaction`；对已提交事务的提交操作被视为幂等重试。

处理器不实现每命令的 `writeConcern` 策略、`maxCommitTimeMS` 或恢复令牌协调。

源码：网关 `processor/transaction.rs` 和 `requests/common_fields.rs`。
