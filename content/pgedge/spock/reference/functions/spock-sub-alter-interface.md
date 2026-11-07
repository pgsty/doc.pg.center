---
title: spock.sub_alter_interface()
description: spock.subalterinterface (subscriptionname name, interfacename name)
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_sub_alter_interface.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



spock.sub_alter_interface()

## SYNOPSIS {#synopsis}

spock.sub_alter_interface (subscription_name name, interface_name name)

## RETURNS {#returns}

  - true if the interface was successfully changed.

  - Raises an ERROR if the subscription or interface does not exist, or
    if the call has invalid parameters or insufficient privileges.

## DESCRIPTION {#description}

Changes the network interface used by a subscription to connect to its
provider node.

This function modifies an existing subscription to use a different interface
when establishing the replication connection to the provider. The specified
interface must already exist on the provider node.

This is useful for switching between different network paths, such as moving
from a public network to a private network connection, or switching to a
different hostname or IP address for the same provider node.

The subscription connection will be restarted using the new interface.

This function writes metadata into the Spock catalogs.

This command must be executed by a superuser.

## ARGUMENTS {#arguments}

subscription_name

    The name of an existing subscription.

interface_name

    The name of an existing interface on the provider node.

## EXAMPLE {#example}

The following example modifies the interface used when connecting to the
replication cluster to use the connection string associated with an
interface named private_net:

    postgres=# SELECT spock.sub_alter_interface('sub_n2_n1', 'private_net');
    sub_alter_interface 
    ---------------------
     t
    (1 row)

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_sub_alter_interface.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
