---
title: spock.sub_alter_options()
description: spock.subalteroptions (subscriptionname name, options jsonb)
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_sub_alter_options.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



spock.sub_alter_options()

## SYNOPSIS {#synopsis}

spock.sub_alter_options (subscription_name name, options jsonb)

## RETURNS {#returns}

  - true if the `options` object contained at least one key; the Spock
    catalog is updated and the apply worker is signalled to restart.

  - false if the `options` object was empty (`{}`); the catalog is not
    touched and the apply worker is not restarted.

  - Raises an ERROR if the subscription does not exist, if `options` is
    not a JSON object, if an unrecognised key is supplied, or if any
    option value fails validation.

## DESCRIPTION {#description}

Changes one or more options on an existing subscription in a single
atomic operation.

Only the keys present in the `options` object are modified; omitted
options retain their current values. If the object is empty (`{}`), the
function returns false without touching the catalog or restarting the
apply worker.

When at least one key is present in `options`, the function writes the
new values to the Spock catalog and signals the apply worker to restart
so that they take effect. The caller can use `spock.sub_show_status()`
or `spock.sub_wait_for_sync()` to confirm the worker has restarted and
reached `replicating` status.

## ARGUMENTS {#arguments}

subscription_name

    The name of an existing subscription.

options

    A JSON object whose keys are the option names to change. Unrecognised
    keys raise an error. Supported keys:

    forward_origins

        A JSON array of origin names whose transactions the subscriber
        should apply or receive based on their origin. The only accepted
        element is the string "all". Pass an empty array ([]) to disable
        origin forwarding.

        See [Origin Forwarding](/pgedge/spock/reference/sub-mgmt/#origin-forwarding) for the
        restriction on combining this with other enabled subscriptions.

    apply_delay

        A PostgreSQL interval string (e.g. "2 seconds", "500ms", "0")
        that sets how long the apply worker waits before applying each
        transaction. The value must be a string; passing a bare number
        raises an error.

    skip_schema

        A JSON array of schema names to exclude from apply. Pass an
        empty array ([]) to clear the exclusion list.

## EXAMPLE {#example}

Set a 2-second apply delay:

    postgres=# SELECT spock.sub_alter_options('sub_n2_n1',
                  '{"apply_delay": "2 seconds"}');
     sub_alter_options
    -------------------
     t
    (1 row)

Enable forwarding of all origins and exclude the `audit` schema in a
single call:

    postgres=# SELECT spock.sub_alter_options('sub_n2_n1',
                  '{"forward_origins": ["all"], "skip_schema": ["audit"]}');
     sub_alter_options
    -------------------
     t
    (1 row)

No-op call (empty object); returns false without restarting the worker:

    postgres=# SELECT spock.sub_alter_options('sub_n2_n1', '{}');
     sub_alter_options
    -------------------
     f
    (1 row)

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_sub_alter_options.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
