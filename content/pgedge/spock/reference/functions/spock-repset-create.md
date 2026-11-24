---
title: spock.repset_create()
description: spock.repsetcreate ( setname name, replicateinsert boolean = true, replicateupdate boolean = true,
  replicatedelete boolean = true, replicatetruncate boolean = true )
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_create.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
---



`spock.repset_create()`

## SYNOPSIS {#synopsis}

spock.repset_create (
    set_name name,
    replicate_insert boolean = true,
    replicate_update boolean = true,
    replicate_delete boolean = true,
    replicate_truncate boolean = true
)

## RETURNS {#returns}

The OID of the newly created replication set.

## DESCRIPTION {#description}

Creates a new Spock replication set.

A replication set defines which types of table operations are replicated to
subscribers. Tables can later be added to this replication set with other
Spock functions.

By default, all data modification operations are replicated; INSERT, UPDATE,
DELETE, and TRUNCATE.

You can selectively disable specific operation types when creating the set.

This function writes metadata into the Spock catalogs but does not alter any
PostgreSQL server configuration.

This command must be executed by a superuser.

## ARGUMENTS {#arguments}

**`set_name`**

The unique name for the replication set.

**`replicate_insert`**

If true (the default), INSERT operations are replicated.

**`replicate_update`**

If true (the default), UPDATE operations are replicated.

**`replicate_delete`**

If true (the default), DELETE operations are replicated.

**`replicate_truncate`**

If true (the default), TRUNCATE operations are replicated.

## EXAMPLE {#example}

The following example creates a replication set named demo_repset; all
operations are replicated to the set:

    postgres=# SELECT spock.repset_create('demo_repset');
     repset_create 
    ---------------
        3356172311
   (1 row)

The following command creates a replication set named audit_only; only 
INSERT and UPDATE statements are replicated:

    postgres=# SELECT spock.repset_create('audit_only',
            replicate_delete := false,
            replicate_truncate := false);
        repset_create 
    ---------------
    3744767607
    (1 row)

---

[Upstream source](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_create.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
