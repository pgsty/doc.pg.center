---
title: drop 和 dropDatabase
description: 使用 DocumentDB 线协议命令删除集合或逻辑数据库。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/administration/drop.md
weight: 30
translation_source_sha256: 070002622a29b4efc3a868b2c93561dfb59468c3b1c9f558bf620971389231ca
translation_review: AI-assisted bilingual review; 2026-11-07
---

`drop` 删除一个集合；`dropDatabase` 删除当前逻辑数据库。两者均会使相关的网关游标失效。

```javascript
db.retired_timetables.drop()
db.getSiblingDB("bookings_scratch").dropDatabase()
```

| 参数 | 描述 |
| --- | --- |
| **`drop`** | (必需) 指定集合名称的字符串。 |
| **`dropDatabase`** | (必需) 命令标记，通常为 `1`；目标数据库来自 `$db`，由驱动程序提供。 |
{.fields}

默认线协议适配器转发数据库和集合名称，而非可选的删除指定项。不要依赖 `encryptedFields`、`collectionUUID` 或 `writeConcern` 来更改删除操作。响应中包含 `ok` 和 `dropped`。

参见 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。源码：网关 `processor/data_description.rs`、`process_drop_collection` 和 `process_drop_database`，以及 `postgres/documentdb_data_client.rs`。
