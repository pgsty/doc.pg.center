---
title: spock.gen_slot_name()
description: spock.spockgenslotname(dbname name, providernode name, subscription name)
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_gen_slot_name.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



spock.spock_gen_slot_name()

## SYNOPSIS {#synopsis}

spock.spock_gen_slot_name(dbname name, provider_node name,
subscription name)

## RETURNS {#returns}

The generated replication slot name as a name type.

## DESCRIPTION {#description}

Generates a standardized replication slot name for a Spock subscription.

This function creates a consistent naming convention for replication slots
based on the database name, provider node name, and subscription name. The
generated name follows Spock's internal naming scheme to ensure uniqueness
and traceability.

This function that performs a calculation without accessing the
database or modifying any data. It can be used to predict what slot name
Spock will generate for a given subscription configuration.

## ARGUMENTS {#arguments}

dbname

    The name of the database.

provider_node

    The name of the provider node.

subscription

    The name of the subscription.

## EXAMPLE {#example}

The following example executes the function; the database name is postgres,
the node name is n1, and the subscription name is sub_n2n1:

    postgres=# SELECT spock.spock_gen_slot_name('postgres', 'n1', 'sub_n2n1');
       spock_gen_slot_name
    --------------------------
     spk_postgres_n1_sub_n2n1
    (1 row)

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_gen_slot_name.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
