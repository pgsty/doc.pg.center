---
title: spock.repset_drop()
description: spock.repsetdrop (setname name, ifexists boolean)
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_repset_drop.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



spock.repset_drop()

## SYNOPSIS {#synopsis}

spock.repset_drop (set_name name, ifexists boolean)

## RETURNS {#returns}

  - true if the replication set was successfully dropped.

  - false if the replication set does not exist and ifexists is true.

  - ERROR if the replication set does not exist and ifexists is false.

## DESCRIPTION {#description}

Drops an existing replication set.

This function removes a replication set from the Spock configuration. When
a replication set is dropped, all table, sequence, and DDL memberships
associated with it are removed. However, the actual tables and sequences
themselves remain in the database - only their association with the
replication set is deleted.

Dropping a replication set does not affect existing subscriptions that
reference it, but those subscriptions will stop receiving changes for
objects that were in the dropped replication set. Subscriptions can be
modified to remove the dropped replication set using
spock.sub_remove_repset().

The ifexists parameter controls error-handling behavior for the function;
when set to true, the function returns false if the replication set does not
exist instead of raising an error. This is useful in situations where the
replication set may or may not be present.

This function modifies the Spock catalogs but does not modify any user data
or the Postgres server configuration.

## ARGUMENTS {#arguments}

set_name

    The name of the replication set to drop.

ifexists

    If true, the function returns false instead of raising an error
    when the replication set does not exist. Defaults to false.

## EXAMPLE {#example}

The following command drops a replication set named demo_repset; it does not
raise an error if the set does not exist:

    postgres=# SELECT spock.repset_drop('demo_repset', true);
     repset_drop 
    -------------
     t
    (1 row)

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_repset_drop.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
