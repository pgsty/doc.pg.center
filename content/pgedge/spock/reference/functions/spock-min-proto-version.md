---
title: spock.min_proto_version()
description: The minimum Spock protocol version supported by the installed Spock extension as an integer.
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_min_proto_version.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
---



spock_min_proto_version()

## SYNOPSIS {#synopsis}

spock_min_proto_version()

## RETURNS {#returns}

The minimum Spock protocol version supported by the installed Spock extension
as an integer. The protocol version determines compatibility between Spock
versions.

## DESCRIPTION {#description}

Returns the minimum protocol version supported by the Spock extension.

This function queries the Spock extension and returns the lowest protocol
version number it can use for replication communication. The protocol
version determines the features and capabilities available for replication
between nodes.

When establishing replication connections between nodes running different
Spock versions, the nodes negotiate to use a protocol version that falls
within the supported range of both nodes. The minimum protocol version
defines the lower bound of compatibility - nodes supporting only protocol
versions below this minimum cannot replicate with this Spock installation.

The protocol version is returned as an integer value. This minimum version
ensures backward compatibility with older Spock releases while still
allowing the use of newer protocol features when both nodes support them.

This is a read-only query function that does not modify data. This function is 
defined in the public schema.

## ARGUMENTS {#arguments}

This function takes no arguments.

## EXAMPLE {#example}

The following command shows that the version of Spock in use is using protocol
version 3:

    postgres=# SELECT spock_min_proto_version();
     spock_min_proto_version
    -------------------------
                           3
    (1 row)

---

[Upstream source](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_min_proto_version.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
