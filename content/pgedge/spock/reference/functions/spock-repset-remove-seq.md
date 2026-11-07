---
title: spock.repset_remove_seq()
description: spock.repsetremoveseq ( setname name, relation regclass)
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_repset_remove_seq.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



`spock.repset_remove_seq ()`

## SYNOPSIS {#synopsis}

spock.repset_remove_seq (
    set_name name,
    relation regclass)

## RETURNS {#returns}

    - true if the sequence was successfully removed from the replication set.
    - Raises an ERROR if the sequence is not a member of the replication
      set, or if the call has invalid parameters or insufficient
      privileges.

## DESCRIPTION {#description}

Removes a sequence from an existing Spock replication set.

After removal, changes to the sequence value are no longer replicated to
subscribers of the replication set.

This function updates metadata stored in the Spock catalogs and does not
modify PostgreSQL configuration.

This command must be executed by a superuser.

## ARGUMENTS {#arguments}

set_name

    The name of an existing replication set.

relation

    The sequence to remove, specified as a regclass
    (for example, 'public.my_sequence').

## EXAMPLE {#example}

Remove a sequence (public.orders_id_seq) from a replication set (demo_repset):

    postgres=# SELECT spock.repset_remove_seq('demo_repset', 'public.orders_id_seq');
     repset_remove_seq 
    -------------------
     t
    (1 row)

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_repset_remove_seq.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
