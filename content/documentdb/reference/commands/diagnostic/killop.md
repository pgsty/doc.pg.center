---
title: killOp
description: Cancel a DocumentDB operation using the string identifier reported by currentOp.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/diagnostic/killOp.md
weight: 80
---

Requests cancellation of a running operation. Run against `admin`.

```javascript
const flightOps = db.currentOp({
  active: true,
  ns: "bookings.flights"
}).inprog
if (flightOps.length > 0) {
  db.killOp(flightOps[0].opid)
}
```

| Parameter | Description |
| --- | --- |
| **`killOp`** | (Required) A command marker, conventionally `1`. |
| **`op`** | (Required) A string specifying the operation identifier reported by [`currentOp`](/documentdb/reference/commands/diagnostic/currentop/). Numeric identifiers are rejected by the gateway. |
{.fields}

Cancellation is subject to server authorization. See [wire protocol and common fields](/documentdb/reference/commands/diagnostic/wire-protocol/).

Source: gateway `processor/data_management.rs`, `process_kill_op`, and `pg_documentdb/src/commands/kill_op.c`.
