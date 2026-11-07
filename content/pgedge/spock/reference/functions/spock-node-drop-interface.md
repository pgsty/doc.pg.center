---
title: spock.node_drop_interface()
description: spock.nodedropinterface (nodename name, interfacename name)
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_node_drop_interface.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



spock.node_drop_interface()

## SYNOPSIS {#synopsis}

spock.node_drop_interface (node_name name, interface_name name)

## RETURNS {#returns}

  - true if the interface was dropped successfully.

  - Raises an ERROR if the interface does not exist, the call has
    invalid parameters or insufficient privileges, or the interface
    cannot be removed.

## DESCRIPTION {#description}

Removes an existing network interface definition from a Spock node.

This function deletes the interface definition from the Spock catalogs. It
does not modify PostgreSQL server configuration or networking settings; it
only removes Spock's logical representation of the interface.

Other nodes that were using this interface to connect will no longer be able
to use it. To avoid a client error, ensure that no active subscriptions rely
on this interface before attempting to remove it.

This function writes metadata into the Spock catalogs but does not modify
PostgreSQL server configuration or networking settings.

This command must be executed by a superuser.

## ARGUMENTS {#arguments}

node_name

    The name of an existing Spock node.

interface_name

    The name of the interface to remove from the node.

## EXAMPLE {#example}

The following example drops an interface named 'private_net':

    inventory=# SELECT spock.node_drop_interface('n3', 'private_net');
     node_drop_interface
    ---------------------
     t
    (1 row)

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_node_drop_interface.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
