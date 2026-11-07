---
title: spock.wait_slot_confirm_lsn()
description: spock.waitslotconfirmlsn (slotname name, target pglsn)
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_wait_slot_confirm_lsn.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



spock.wait_slot_confirm_lsn()

## SYNOPSIS {#synopsis}

spock.wait_slot_confirm_lsn (slotname name, target pg_lsn)

## RETURNS {#returns}

void (returns nothing upon successful completion).

## DESCRIPTION {#description}

Waits until the specified replication slot has confirmed receipt of changes
up to the target Log Sequence Number (LSN).

This function blocks the current session until the replication slot's
confirmed flush LSN reaches or exceeds the specified target LSN. This is
useful for ensuring that a subscriber has received and acknowledged
replication changes before proceeding with subsequent operations.

The confirmed flush LSN represents the position up to which the subscriber
has successfully received, applied, and durably stored the replicated
changes. This function provides a synchronization mechanism to coordinate
activities between the provider and subscriber nodes.

If the replication slot does not exist, the function will raise an error.
The function will continue waiting indefinitely until the target LSN is
reached, so callers should ensure the target LSN is reachable and that the
subscription is actively processing changes.

This function does not modify any data but may block for an extended period
depending on replication lag and network conditions.

## ARGUMENTS {#arguments}

slotname

    The name of the replication slot to monitor.

target

    The target Log Sequence Number to wait for. The function returns
    when the slot's confirmed flush LSN reaches or exceeds this
    value.

## EXAMPLE {#example}

The following command waits for a slot named spock_local_sync_346_79a to
confirm that it has received changes to the target LSN (0/3000000):

    SELECT spock.wait_slot_confirm_lsn('spock_local_sync_346_79a',
    '0/3000000');

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_wait_slot_confirm_lsn.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
