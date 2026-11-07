---
title: validate
description: Validate DocumentDB collection metadata and indexes with supported validation modes.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/diagnostic/validate.md
weight: 90
---

Validates a collection and returns validation information. Views are not supported.

```javascript
db.flights.validate()
```

| Parameter | Description |
| --- | --- |
| **`validate`** | (Required) A string specifying the collection name. |
| **`repair`** | (Optional) A boolean-like value that repairs baseline collection access privileges; not a general-purpose BSON or index repair facility. |
{.fields}

`repair` defaults to `false`. Collection-owner authorization is required.

See [wire protocol and common fields](/documentdb/reference/commands/diagnostic/wire-protocol/). Source: `pg_documentdb/src/commands/validate.c`, `command_validate`.
