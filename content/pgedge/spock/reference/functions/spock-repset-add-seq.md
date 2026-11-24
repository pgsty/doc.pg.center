---
title: spock.repset_add_seq()
description: spock.repsetaddseq ( setname name, relation regclass, synchronizedata boolean)
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_add_seq.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
---



`spock.repset_add_seq()`

## SYNOPSIS {#synopsis}

spock.repset_add_seq (
    set_name name,
    relation regclass,
    synchronize_data boolean)

## RETURNS {#returns}

- true if the sequence was successfully added to the replication set.
- Raises an ERROR if the sequence is already a member of the
  replication set, or if the call has invalid parameters or
  insufficient privileges.

## DESCRIPTION {#description}

Adds a sequence to an existing Spock replication set.

Once added, changes to the sequence value are replicated to subscribers
that are subscribed to the replication set. This ensures that nextval
operations remain consistent across nodes in a multi-master environment.

If synchronize_data is true, the current sequence value is immediately
synchronized to all subscribers.

This function updates metadata stored in the Spock catalogs and does not
modify PostgreSQL configuration.

This command must be executed by a superuser.

## ARGUMENTS {#arguments}

**`set_name`**

The name of an existing replication set.

**`relation`**

The sequence to add, specified as a regclass
(for example, 'public.my_sequence').

**`synchronize_data`**

If true, the current sequence value is synchronized to
all subscribers. The default is false.

## EXAMPLE {#example}

Add a sequence (named public.sales_order_no_seq) to the 'default' replication
set:

    postgres=# SELECT spock.repset_add_seq('default', 'public.sales_order_no_seq');
     repset_add_seq
    ----------------
     t
    (1 row)

Add a sequence (named public.sales_invoice_no_seq) and synchronize its current value:

    postgres=# SELECT spock.repset_add_seq(
        'default',
        'public.sales_invoice_no_seq',
        synchronize_data := true
    );
     repset_add_seq
    ----------------
     t
    (1 row)

---

[Upstream source](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_add_seq.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
