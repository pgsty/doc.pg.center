---
title: spock.sub_alter_skiplsn()
description: spock.subalterskiplsn (subscriptionname name, lsn pglsn) RETURNS boolean
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_alter_skiplsn.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
---



`spock.sub_alter_skiplsn()`

## SYNOPSIS {#synopsis}

`spock.sub_alter_skiplsn (subscription_name name, lsn pg_lsn) RETURNS boolean`

## RETURNS {#returns}

`true` if the skip LSN was successfully set, `false` otherwise.

## DESCRIPTION {#description}

Advances the replication position of an existing subscription to the specified Log Sequence Number (LSN). This is typically used as a recovery operation when a subscription is unable to proceed due to a problematic change in the replication stream. Any changes between the old LSN and the specified LSN will be permanently skipped.

This command must be executed by a superuser.

## ARGUMENTS {#arguments}

**`subscription_name`**

The name of an existing subscription.

**`lsn`**

The Log Sequence Number to which the subscription should advance.

## EXAMPLE {#example}

`SELECT spock.sub_alter_skiplsn('sub_n1_to_n2', '0/16B6A50');`

---

[Upstream source](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_alter_skiplsn.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
