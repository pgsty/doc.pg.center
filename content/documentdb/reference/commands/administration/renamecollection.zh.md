---
title: renameCollection
description: 在同一个逻辑数据库内重命名 DocumentDB 集合。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/administration/renameCollection.md
weight: 60
translation_source_sha256: 7eef992760f08945c233bd4f6c3687eac7dbe36f7fc7abf40f8b172ef8d1ef76
translation_review: AI-assisted bilingual review; 2026-11-07
---

在同一个逻辑数据库内重命名一个集合。

```javascript
db.createCollection("flights_staging")
db.flights_staging.renameCollection("flights_active", false)
```

| 参数 | 描述 |
| --- | --- |
| **`renameCollection`** | (必需) 指定源命名空间的字符串，`database.collection`。 |
| **`to`** | (必需) 指定同一数据库中目标命名空间的字符串。 |
| **`dropTarget`** | (可选) 布尔值，如果 `true`，则删除已存在的目标集合；默认值为 `false`。 |
{.fields}

不支持跨数据库重命名，也不支持将集合重命名为自身。共享 `writeConcern` 和 `comment` 不会改变重命名行为。

参见 [线协议和通用字段](/documentdb/reference/commands/diagnostic/wire-protocol/)。源码：`pg_documentdb/src/commands/rename_collection.c`, `ParseRenameCollectionSpec`。
