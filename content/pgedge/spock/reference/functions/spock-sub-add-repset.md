---
title: spock.sub_add_repset()
description: spock.subaddrepset (subscriptionname name, replicationset name)
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_sub_add_repset.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



spock.sub_add_repset()

## SYNOPSIS {#synopsis}

spock.sub_add_repset (subscription_name name, replication_set name)

## RETURNS {#returns}

  - true if the replication set was successfully added.

  - Raises an ERROR if the subscription does not exist, the replication
    set is already attached, or the call has invalid parameters or
    insufficient privileges.

## DESCRIPTION {#description}

Adds a replication set to an existing subscription.

This function modifies a subscription to begin receiving changes from an
additional replication set on the provider node. The subscription will start
consuming events from the newly added replication set immediately.

This operation does not perform data synchronization. It only activates the
consumption of future events from the replication set. If you need to
synchronize existing data from the replication set, you must handle that
separately.

This function writes metadata into the Spock catalogs.

Returns NULL if any argument is NULL.

This command must be executed by a superuser.

## ARGUMENTS {#arguments}

subscription_name

    The name of an existing subscription.

replication_set

    The name of the replication set to add to the subscription.

## EXAMPLE {#example}

The following example adds a replication set named audit_only to a 
subscription named sub_n2_n1:

    postgres=# SELECT spock.sub_add_repset('sub_n2_n1', 'audit_only');
    -[ RECORD 1 ]--+--
    sub_add_repset | t

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_sub_add_repset.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
