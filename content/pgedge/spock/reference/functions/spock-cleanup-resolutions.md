---
title: spock.cleanup_resolutions
description: The spock.cleanupresolutions() function manually deletes old rows from the spock.resolutions table.
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_cleanup_resolutions.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



The `spock.cleanup_resolutions()` function manually deletes old rows from the
`spock.resolutions` table.

## Synopsis {#synopsis}

```sql
spock.cleanup_resolutions(days integer DEFAULT NULL) RETURNS bigint
```

## Description {#description}

Deletes rows from `spock.resolutions` whose `log_time` is older than the
retention window. Returns the number of rows deleted.

This function is a superuser-only manual trigger for the same cleanup that
the apply worker runs automatically once per day. It is useful for
immediate cleanup via `pg_cron` or when the apply worker has not been
running.

When `days` is provided it takes precedence over
`spock.resolutions_retention_days`, including when the GUC is set to `0`
(automatic cleanup disabled). If `days` is omitted, the GUC value is used;
if the GUC is also `0`, the function returns `0` without deleting anything.

## Arguments {#arguments}

The function accepts the following argument:

- `days` - Retention window in days. Overrides `spock.resolutions_retention_days`
  for this call. Pass an explicit value to perform a one-off cleanup when
  automatic cleanup is disabled (`resolutions_retention_days = 0`). Default
  is `NULL` (use the GUC value).

## Example {#example}

Delete rows older than the configured retention window:

```sql
SELECT spock.cleanup_resolutions();
```

Delete rows older than 60 days, regardless of the GUC setting:

```sql
SELECT spock.cleanup_resolutions(60);
```

## See Also {#see-also}

`spock.resolutions_retention_days`

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_cleanup_resolutions.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
