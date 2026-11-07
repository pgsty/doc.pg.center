---
title: hello
description: The hello command returns information about the DocumentDB server, including topology role, wire protocol
  limits, and the DocumentDB engine version.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/diagnostic/hello.md
weight: 70
---

The `hello` command returns a document describing the role of the DocumentDB server, along with connection limits, supported authentication mechanisms, and the version of the DocumentDB engine you are connected to. It's the recommended way to discover the DocumentDB version from a MongoDB client, since the `internal.documentdb_versions` field reports the underlying engine version rather than only the emulated MongoDB wire-protocol version.

The versions in `internal.documentdb_versions` come from the backend DocumentDB PostgreSQL extension, not from the gateway. The array reports two values: the installed SQL extension version (from the `pg_extension` catalog, such as `1.0-0`) followed by the loaded binary version (from `documentdb_api.binary_version()`, in dotted form such as `1.0.0`). In PostgreSQL, the installed extension version *is* the schema version — it tracks which SQL upgrade scripts have been applied — so the first value reflects the schema currently installed in the database. These two values normally describe the same release and differ only in formatting, but they can diverge during an upgrade — for example, after the 1.0 packages are installed over 0.117 but before `ALTER EXTENSION documentdb UPDATE` has been run. A mismatch such as `["0.117-0", "1.0.0"]` indicates the SQL schema is behind the loaded binary.

Returns gateway handshake information. This command does not read collection data and does not require loading the airline example dataset.

## Example {#example}

```javascript
db.hello()
```

To inspect the backend version values separately:

```javascript
db.hello().internal.documentdb_versions
```

These are deployment-dependent values, not fixed example output.

## Request parameters {#request-parameters}

| Parameter | Description |
| --- | --- |
| **`hello`** | (Required) A command marker, conventionally `1`. |
| **`client`** | (Optional) A document specifying the driver/application metadata stored on the connection. A second `client` document fails with `ClientMetadataCannotBeMutated`. |
{.fields}

`isMaster` and `ismaster` reach the same handler, but use `ismaster` in the response instead of `isWritablePrimary`.

The handler does not implement awaitable hello through `topologyVersion` and `maxAwaitTimeMS`, or speculative authentication through `speculativeAuthenticate`. The request's `saslSupportedMechs` value does not select mechanisms: the handler reports enabled gateway authentication schemes.

## Response fields {#response-fields}

| Field | Implementation behavior |
| --- | --- |
| `isWritablePrimary` | Set to `true` by the hello handler. The legacy handler uses `ismaster` instead. |
| `msg` | Set to `isdbgrid`. |
| `maxBsonObjectSize`, `maxMessageSizeBytes` | Gateway protocol limits in bytes. |
| `maxWriteBatchSize` | Configured gateway write-batch limit. |
| `localTime` | Current gateway time. |
| `logicalSessionTimeoutMinutes` | Set to `30`. |
| `minWireVersion`, `maxWireVersion` | Minimum is `0`; maximum follows the configured compatibility version. |
| `readOnly` | Configured connection read-only state. |
| `connectionId` | Connection identifier. |
| `saslSupportedMechs` | Enabled gateway authentication schemes. |
| `internal` | Configured topology metadata, including `documentdb_versions` in the default deployment. |
| `operationTime` | Included when change streams are enabled. |
| `ok` | Success marker. |

In the default backend, `internal.documentdb_versions` contains the installed SQL extension version followed by the loaded binary version. The first tracks applied SQL upgrades; the second identifies the loaded implementation. They can diverge during an upgrade. [`buildInfo`](/documentdb/reference/commands/diagnostic/compatibility/) reports the configured wire-compatibility version, not these engine versions.

## Shell syntax {#shell-syntax}

```javascript
db.runCommand({ hello: 1 })
```

```javascript
db.hello()
```

## Detailed Examples {#detailed-examples}

### Example 1: Inspect the server role and version {#example-1-inspect-the-server-role-and-version}

Run the `hello` command to view the full response:

```javascript
db.runCommand({ hello: 1 })
```

The server returns a document similar to the following:

```json
{
  "isWritablePrimary": true,
  "msg": "isdbgrid",
  "maxBsonObjectSize": 16777216,
  "maxMessageSizeBytes": 48000000,
  "maxWriteBatchSize": 25000,
  "localTime": 1783006410548,
  "logicalSessionTimeoutMinutes": 30,
  "minWireVersion": 0,
  "maxWireVersion": 21,
  "readOnly": false,
  "connectionId": 382703778,
  "saslSupportedMechs": [
    "SCRAM-SHA-256"
  ],
  "internal": {
    "documentdb_versions": [
      "1.0-0",
      "1.0.0"
    ],
    "kind": ""
  },
  "ok": 1
}
```

<span id="example-2-determine-the-document-db-engine-version"></span>

### Example 2: Determine the DocumentDB engine version {#example-2-determine-the-documentdb-engine-version}

To read only the DocumentDB engine version, project the `internal.documentdb_versions` field:

```javascript
db.runCommand({ hello: 1 }).internal.documentdb_versions
```

The command returns an array with the installed SQL extension version followed by the loaded binary version:

```json
[ "1.0-0", "1.0.0" ]
```

The first value is the installed SQL extension version — the schema version, from the `pg_extension` catalog — and the second is the compiled binary version. They normally describe the same release and differ only in formatting.

> [!NOTE]
> The `buildInfo` command reports the emulated MongoDB wire-protocol version (for example, `7.0.0`), not the DocumentDB engine version. Use `hello` and read `internal.documentdb_versions` to determine the DocumentDB version.

## Related content {#related-content}

- [DocumentDB Local](/documentdb/documentdb-local/)

## Implementation {#implementation}

Source: gateway `processor/ismaster.rs`, the default topology configuration, and the PostgreSQL version-information query. See [wire protocol and common fields](/documentdb/reference/commands/diagnostic/wire-protocol/) for source scope.
