---
title: spock.node_info()
description: 'A record containing information about the local Spock node:'
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_node_info.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
---



spock.node_info()

## SYNOPSIS {#synopsis}

spock.node_info()

## RETURNS {#returns}

A record containing information about the local Spock node:

  - node_id is the OID of the node.
  - node_name is the name of the node.
  - sysid is the system identifier.
  - dbname is the database name.
  - replication_sets is the available replication sets.
  - location is the node location (if set).
  - country is the node country (if set).
  - info is additional metadata stored in JSONB format (if set).

## DESCRIPTION {#description}

Returns information about the local Spock node.

This function queries the Spock catalogs and returns metadata about the
current node, including its identifier, name, database information, and any
optional descriptive fields that were set during node creation.

This is a read-only query function that does not modify data.

## ARGUMENTS {#arguments}

This function takes no arguments.

## EXAMPLE {#example}

    postgres=# SELECT * FROM spock.node_info();

    -[ RECORD 1 ]----+--------------------------------------
    node_id          | 49708
    node_name        | n1
    sysid            | 7600444661598442547
    dbname           | postgres
    replication_sets | "default",default_insert_only,ddl_sql
    location         |
    country          |
    info             | 

---

[Upstream source](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_node_info.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
