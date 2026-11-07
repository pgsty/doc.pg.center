---
title: Transaction commands
description: Commit or abort transactions using DocumentDB session and transaction metadata.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/sessions/transaction-commands.md
weight: 20
---

Drivers start a transaction by adding transaction metadata to its first operation, not by sending a separate begin command.

## Transaction context {#transaction-context}

Use the driver's transaction API to maintain matching [session and transaction metadata](/documentdb/reference/commands/diagnostic/wire-protocol/#common-request-fields). Read isolation follows the [shared read-concern rules](/documentdb/reference/commands/diagnostic/wire-protocol/#read-concern).

<span id="commit-transaction-and-abort-transaction"></span>

## commitTransaction and abortTransaction {#committransaction-and-aborttransaction}

Using the [airline example dataset](/documentdb/reference/commands/diagnostic/wire-protocol/#airline-example-dataset), start a transaction with a read and commit it. The session helper maintains matching `lsid` and `txnNumber` values:

```javascript
const bookingsSession = db.getMongo().startSession({ causalConsistency: false })
const bookingsDb = bookingsSession.getDatabase("bookings")
bookingsSession.startTransaction()
bookingsDb.flights.findOne({ route_no: "PG0101" })
bookingsSession.commitTransaction()
bookingsSession.endSession()
```

Use `bookingsSession.abortTransaction()` instead of `commitTransaction()` to abort. The helpers do not return a raw command document; the wire handlers return `ok: 1` on success. A missing or nonexistent active transaction produces `NoSuchTransaction`; committing an already committed transaction is handled as an idempotent retry.

The handlers do not implement per-command `writeConcern` policies, `maxCommitTimeMS`, or recovery-token coordination.

Source: gateway `processor/transaction.rs` and `requests/common_fields.rs`.
