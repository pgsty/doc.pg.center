---
title: spock.sub_drop()
description: spock.subdrop (subscriptionname name, ifexists boolean)
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_sub_drop.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



spock.sub_drop()

## SYNOPSIS {#synopsis}

spock.sub_drop (subscription_name name, ifexists boolean)

## RETURNS {#returns}

The OID of the dropped subscription.

## DESCRIPTION {#description}

Disconnects and removes a subscription from the cluster.

This function terminates the replication connection for the specified
subscription and removes all associated metadata from the Spock catalogs. It
does not affect data that has already been replicated to the subscriber.

If ifexists is set to false (default), an error is raised when the specified
subscription does not exist. If ifexists is true, the function returns
successfully without error.

Returns NULL if any argument is NULL.

This command must be executed by a superuser.

## ARGUMENTS {#arguments}

subscription_name

    The name of the existing subscription to remove.

ifexists

    If true, do not raise an error when the subscription does not exist.
    Default is false.

## EXAMPLE {#example}

    SELECT spock.sub_drop('sub_n2_n1');

    SELECT spock.sub_drop('sub_n2_n1', true);

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_sub_drop.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
