---
title: "UNLISTEN"
description: "Stops listening for a notification."
weight: 1770
upstream_link: "https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/sql-stmts/unlisten.md"
---

## Synopsis {#synopsis}

```sql
UNLISTEN { <channel> | * }
```

## Description {#description}

`UNLISTEN` is used to remove an existing registration for `NOTIFY` events. `UNLISTEN` cancels any existing registration of the current Apache Cloudberry session as a listener on the notification channel named channel. The special wildcard `*` cancels all listener registrations for the current session.

[NOTIFY](/cloudberry/reference/sql-stmts/notify/) contains a more extensive discussion of the use of `LISTEN` and `NOTIFY`.

## Parameters {#parameters}

**`channel`**

The name of a notification channel (any identifier).

**`*`**

All current listen registrations for this session are cleared.

## Notes {#notes}

You can unlisten something you were not listening for; no warning or error will appear.

At the end of each session, `UNLISTEN *` is automatically executed.

A transaction that has executed `UNLISTEN` cannot be prepared for two-phase commit.

## Examples {#examples}

To make a registration:

```sql
LISTEN virtual;
NOTIFY virtual;
Asynchronous notification "virtual" received from server process with PID 8448.
```

Once `UNLISTEN` has been executed, further `NOTIFY` messages will be ignored:

```sql
UNLISTEN virtual;
NOTIFY virtual;
-- no NOTIFY event is received
```

## Compatibility {#compatibility}

There is no `UNLISTEN` statement in the SQL standard.

## See also {#see-also}

[LISTEN](/cloudberry/reference/sql-stmts/listen/), [NOTIFY](/cloudberry/reference/sql-stmts/notify/)
