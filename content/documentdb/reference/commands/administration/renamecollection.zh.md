---
title: renameCollection
description: 在同一个逻辑数据库内重命名 DocumentDB 集合。
type: docs
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/api-reference/commands/administration/renameCollection.md
weight: 60
translation_source_sha256: a2de2e7a216aca3b914c4139417a2a52538a082689776aa25d74dd0b853ad068
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
