---
title: validate
description: 使用支持的验证模式验证 DocumentDB 集合元数据和索引。
type: docs
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/api-reference/commands/diagnostic/validate.md
weight: 90
translation_source_sha256: 6a221d9da6f9b6bbcd5c3dfca855880d7442d82cd76784c66c782af55b102573
translation_review: AI-assisted bilingual review; 2026-11-07
---

验证集合并返回验证信息。不支持视图。

```javascript
db.flights.validate()
```

| 参数 | 描述 |
| --- | --- |
| **`validate`** | (必需) 指定集合名称的字符串。 |
| **`repair`** | (可选) 类布尔值，用于修复基础集合访问权限；并非通用的 BSON 或索引修复工具。 |
{.fields}

`repair` 默认值为 `false`。需要集合所有者授权。

参见 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。源码：`pg_documentdb/src/commands/validate.c`, `command_validate`。
