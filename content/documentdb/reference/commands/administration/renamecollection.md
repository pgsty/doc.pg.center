---
title: renameCollection
description: Rename a DocumentDB collection within the same logical database.
type: docs
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/api-reference/commands/administration/renameCollection.md
weight: 60
---

Renames a collection within the same logical database.

```javascript
db.createCollection("flights_staging")
db.flights_staging.renameCollection("flights_active", false)
```

| Parameter | Description |
| --- | --- |
| **`renameCollection`** | (Required) A string specifying the source namespace, `database.collection`. |
| **`to`** | (Required) A string specifying the destination namespace in the same database. |
| **`dropTarget`** | (Optional) A boolean that drops an existing destination collection if `true`; defaults to `false`. |
{.fields}

Cross-database renaming and renaming a collection to itself are rejected. Shared `writeConcern` and `comment` do not alter renaming behavior.

See [wire protocol and common fields](/documentdb/reference/commands/diagnostic/wire-protocol/). Source: `pg_documentdb/src/commands/rename_collection.c`, `ParseRenameCollectionSpec`.
