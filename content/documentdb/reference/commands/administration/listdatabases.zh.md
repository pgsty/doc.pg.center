---
title: listDatabases
description: 列出逻辑 DocumentDB 数据库并过滤返回的元数据。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/administration/listDatabases.md
weight: 50
translation_source_sha256: 358243037cfca640ede968f3a5bfb0bd3f2d87aa2131fc480bfd6d54ad8f1809
translation_review: AI-assisted bilingual review; 2026-11-07
---

列出逻辑数据库。在 `admin` 上运行。

```javascript
db.getMongo().getDBs({ nameOnly: true, filter: { name: "bookings" } })
```

| 参数 | 描述 |
| --- | --- |
| **`listDatabases`** | (必需) 命令标记，通常为 `1`。 |
| **`nameOnly`** | (可选) 类布尔值，返回数据库名称时不含大小字段；默认为 `false`。 |
| **`filter`** | (可选) 用于过滤返回的数据库文档的文档。 |
{.fields}

默认实现报告每个数据库的占位符 `sizeOnDisk: 0` 和 `empty: false`；`totalSize` 测量底层 PostgreSQL 数据库，而非分别测量的逻辑数据库大小之和。`authorizedDatabases` 不被识别。此命令返回一个 `databases` 数组，而非游标。

参见 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。源码：`pg_documentdb/src/commands/db_stats.c`, `command_list_databases`。
