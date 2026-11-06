---
title: "CHECKPOINT"
description: "Forces a write-ahead log checkpoint."
weight: 460
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/checkpoint.md"
---

## Synopsis {#synopsis}

```sql
CHECKPOINT
```

## Description {#description}

A checkpoint is a point in the write-ahead log sequence at which all data files have been updated to reflect the information in the log. All data files will be flushed to disk.

The `CHECKPOINT` command forces an immediate checkpoint when the command is issued, without waiting for a regular checkpoint scheduled by the system. `CHECKPOINT` is not intended for use during normal operation.

If run during recovery, the `CHECKPOINT` command will force a restartpoint rather than writing a new checkpoint.

Only superusers may call `CHECKPOINT`.

## Compatibility {#compatibility}

The `CHECKPOINT` command is a Apache Cloudberry extension.
