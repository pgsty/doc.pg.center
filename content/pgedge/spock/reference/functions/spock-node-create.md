---
title: spock.node_create()
description: spock.nodecreate (nodename name, dsn text, location text, country text, info jsonb)
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_node_create.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



spock.node_create()

## SYNOPSIS {#synopsis}

spock.node_create (node_name name, dsn text, location text,
country text, info jsonb)

## RETURNS {#returns}

The OID of the newly created Spock node.

## DESCRIPTION {#description}

Creates a new Spock node definition.

A node represents a PostgreSQL instance that participates in Spock
replication. The node definition includes the connection information that
other nodes will use to communicate with this node.

Optional metadata fields such as location, country, and info can be provided
to describe the node for organizational or management purposes. These values
are stored in the Spock catalogs but are not required for replication to
function.

This function writes metadata into the Spock catalogs but does not modify
Postgres server configuration or networking settings.

This command must be executed by a superuser.

## ARGUMENTS {#arguments}

node_name

    A unique name for the Spock node.

dsn

    A PostgreSQL connection string that other nodes will use to
    connect to this node.

location

    Optional descriptive text indicating the physical or logical
    location of the node. The default is NULL.

country

    Optional country code or name associated with the node. The default is 
    NULL.

info

    Optional JSONB field for storing arbitrary metadata about
    the node.  The default is NULL.

    A `tiebreaker` key in this field overrides the node's default
    last-update-wins tiebreaker (otherwise the node's unique ID). Each
    node caches this value locally, populated once when it first learns
    about the node. A later change (via `spock.node_alter`, the
    recommended way, or a raw `UPDATE`) propagates automatically to every
    direct subscriber. `spock.node_refresh_info` updates a node that missed
    the change -- see the Tiebreaker section in conflict_types.md for
    details.

## EXAMPLE {#example}

In the following example, Spock creates a node named n3, with a connection
to a database named 'inventory':

    inventory=# SELECT spock.node_create('n3','host=10.0.0.12 port=5432 dbname=inventory');
     node_create
    -------------
            9057
    (1 row)

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_node_create.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
