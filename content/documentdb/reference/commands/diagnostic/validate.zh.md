---
title: validate
description: 使用支持的验证模式验证 DocumentDB 集合元数据和索引。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/diagnostic/validate.md
weight: 90
translation_source_sha256: 0905a6cece8b49dd7e3126ec3b35866880ec537fa043f00e1b2fb1bc766af8af
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
