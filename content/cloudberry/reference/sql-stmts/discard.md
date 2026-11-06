---
title: "DISCARD"
description: "Discards the session state."
weight: 980
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/discard.md"
---

## Synopsis {#synopsis}

```sql
DISCARD { ALL | PLANS | SEQUENCES | TEMPORARY | TEMP }
```

## Description {#description}

`DISCARD` releases internal resources associated with a database session. This command is useful for partially or fully resetting the session's state. There are several subcommands to release different types of resources; the `DISCARD ALL` variant subsumes all the others, and also resets additional state.

Apache Cloudberry does not support invoking `DISCARD ALL` in a transaction.

## Parameters {#parameters}

**`PLANS`**

Releases all cached query plans, forcing re-planning to occur the next time the associated prepared statement is used.

**`SEQUENCES`**

Discards all cached sequence-related state, including any preallocated sequence values that have not yet been returned by `nextval()`. (See [CREATE SEQUENCE](/cloudberry/reference/sql-stmts/create-sequence/) for a description of preallocated sequence values.)

**`TEMPORARY/TEMP`**

Drops all temporary tables created in the current session.

**`ALL`**

Releases all temporary resources associated with the current session and resets the session to its initial state. Currently, this has the same effect as executing the following sequence of statements:

```sql
    CLOSE ALL;
    SET SESSION AUTHORIZATION DEFAULT;
    RESET ALL;
    DEALLOCATE ALL;
    UNLISTEN *;
    SELECT pg_advisory_unlock_all();
    DISCARD PLANS;
    DISCARD SEQUENCES;
    DISCARD TEMP;
```

## Notes {#notes}

`DISCARD ALL` cannot be run inside a transaction block.

## Compatibility {#compatibility}

`DISCARD` is a Apache Cloudberry extension.
