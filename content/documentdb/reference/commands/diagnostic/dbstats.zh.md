---
title: dbStats
description: 返回当前逻辑 DocumentDB 数据库的统计信息。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/diagnostic/dbStats.md
weight: 50
translation_source_sha256: a42cdd4ac15f4256164266269fd9ccb70f026e56275561cc757c01e19eea29ee
translation_review: AI-assisted bilingual review; 2026-11-07
---

返回当前逻辑数据库的统计信息。

```javascript
db.stats({ scale: 1024 })
```

| 参数 | 描述 |
| --- | --- |
| **`dbStats`** | (必需) 命令标记，通常为 `1`；目标数据库由连接的 `$db` 提供。 |
| **`scale`** | (可选) 指定适用于字节大小字段的除数；默认值为 `1`。后端会将数值截断为整数。 |
{.fields}

`null` 或 undefined `scale` 使用 `1`。默认线协议适配器仅转发数据库和缩放因子，不包含 `freeStorage` 选项。

参见 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。源码：网关 `processor/data_management.rs`、`process_db_stats` 和后端 `pg_documentdb/src/commands/db_stats.c`。
