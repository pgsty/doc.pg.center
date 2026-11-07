---
title: spock.repset_alter()
description: spock.repsetalter ( setname name, replicateinsert boolean, replicateupdate boolean, replicatedelete
  boolean, replicatetruncate boolean )
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_repset_alter.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



`spock.repset_alter()`

## SYNOPSIS {#synopsis}

spock.repset_alter (
    set_name name,
    replicate_insert boolean,
    replicate_update boolean,
    replicate_delete boolean,
    replicate_truncate boolean
)

## RETURNS {#returns}

The OID of the altered replication set.

## DESCRIPTION {#description}

Modifies the replication behavior of an existing Spock replication set.

Each replication set defines which types of table operations are replicated to
subscribers. This function allows you to change those behaviors after the set
has been created.

Any argument left as NULL will retain its current setting. Only the
specified operation types are modified.

This function updates metadata in the Spock catalogs and does not change
PostgreSQL server configuration.

This command must be executed by a superuser.

## ARGUMENTS {#arguments}

set_name

    The name of an existing replication set.

replicate_insert

    If true, INSERT operations are replicated; the default is NULL.

replicate_update

    If true, UPDATE operations are replicated; the default is NULL.

replicate_delete

    If true, DELETE operations are replicated; the default is NULL.

replicate_truncate

    If true, TRUNCATE operations are replicated; the default is NULL.

## EXAMPLE {#example}

The following command enables all operations in the demo_repset replication
set:

    postgres=# SELECT spock.repset_alter('demo_repset',
            replicate_insert := true,
            replicate_update := true,
            replicate_delete := true,
            replicate_truncate := true);
     repset_alter 
    --------------
       3356172311
    (1 row)

The following command disables DELETE and TRUNCATE replication in the
audit_only replication_set:

    postgres=# SELECT spock.repset_alter('audit_only',
        replicate_delete := false,
        replicate_truncate := false);
    repset_alter 
    --------------
       3744767607
    (1 row)


---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_repset_alter.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
