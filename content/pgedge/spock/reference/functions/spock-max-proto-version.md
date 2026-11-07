---
title: spock.max_proto_version()
description: The maximum spock protocol version supported by the installed Spock extension as an integer.
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_max_proto_version.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



spock_max_proto_version()

## SYNOPSIS {#synopsis}

spock_max_proto_version()

## RETURNS {#returns}

The maximum spock protocol version supported by the installed Spock extension
as an integer.  The protocol version determines compatibility between Spock
versions.

## DESCRIPTION {#description}

Returns the maximum protocol version supported by the Spock extension.

This function queries the Spock extension and returns the highest protocol
version number it can use for replication communication. The protocol
version determines the features and capabilities available for replication
between nodes.

When establishing replication connections between nodes running different
Spock versions, the nodes negotiate to use the lower of the two maximum
protocol versions. This ensures compatibility between nodes running
different Spock releases.

The protocol version is returned as an integer value. Higher numbers
indicate newer protocol versions with additional features.

This is a read-only query function that does not modify data. This function is
defined in the public schema.

## ARGUMENTS {#arguments}

This function takes no arguments.

## EXAMPLE {#example}

The following command shows that the current version of Spock uses protocol
version 4:

    postgres=# SELECT spock_max_proto_version();
     spock_max_proto_version
    -------------------------
                           4
    (1 row)

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_max_proto_version.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
