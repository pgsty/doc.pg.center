---
title: drop and dropDatabase
description: Remove collections or logical databases using DocumentDB wire commands.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/administration/drop.md
weight: 30
---

`drop` removes a collection; `dropDatabase` removes the current logical database. Both invalidate associated gateway cursors.

```javascript
db.retired_timetables.drop()
db.getSiblingDB("bookings_scratch").dropDatabase()
```

| Parameter | Description |
| --- | --- |
| **`drop`** | (Required) A string specifying the collection name. |
| **`dropDatabase`** | (Required) A command marker, conventionally `1`; the target database comes from `$db`, supplied by the driver. |
{.fields}

The default wire adapters forward the database and collection names, not optional drop specifications. Do not rely on `encryptedFields`, `collectionUUID`, or `writeConcern` to change the drop operation. The response includes `ok` and `dropped`.

See [wire protocol and common fields](/documentdb/reference/commands/diagnostic/wire-protocol/). Source: gateway `processor/data_description.rs`, `process_drop_collection` and `process_drop_database`, and `postgres/documentdb_data_client.rs`.
