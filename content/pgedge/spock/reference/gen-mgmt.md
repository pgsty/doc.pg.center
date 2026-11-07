---
title: Management Functions
description: You can use the following settings to manage your replication clusters.
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/gen_mgmt.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



You can use the following settings to manage your replication clusters.

| Command  | Description
|----------|-------------
| [spock.get_country](/pgedge/spock/reference/functions/spock-get-country/) | Returns the country code configured for the node. |
| [spock_max_proto_version](/pgedge/spock/reference/functions/spock-max-proto-version/) | Returns the maximum protocol version supported by Spock. Defined in the public schema so invoked without the `spock.` prefix. |
| [spock_min_proto_version](/pgedge/spock/reference/functions/spock-min-proto-version/) | Returns the minimum protocol version supported by Spock. Defined in the public schema, so invoked without the `spock.` prefix. |
| [spock.node_info](/pgedge/spock/reference/functions/spock-node-info/) | Returns information about the local Spock node. |
| [spock_version](/pgedge/spock/reference/functions/spock-version/) | Returns the version string of the Spock extension. Defined in the public schema so invoked without the `spock.` prefix. |
| [spock_version_num](/pgedge/spock/reference/functions/spock-version-num/) | Returns the version number of Spock as an integer. Defined in the public schema so invoked without the `spock.` prefix. |

## spock.get_country {#spockget_country}

Use `spock.get_country` to retrieve the country code configured for the node.

`spock.get_country()`

Returns the `spock.country` property that was set during node creation. You
can modify the property after configuration; modification requires a server
restart to apply the change.

This function retrieves the value of the spock.country configuration
parameter for the current session. The country code is typically used in
multi-region or geo-distributed replication topologies to identify the
geographic location of nodes and apply region-specific routing or filtering
rules.

This function takes no arguments.

## spock_max_proto_version {#spock_max_proto_version}

Use `spock_max_proto_version` to retrieve the maximum protocol version
supported by Spock. 

`spock_max_proto_version()`

Returns the maximum protocol version supported by the Spock extension.

This function takes no arguments, and is defined in the public
schema so must be invoked without the `spock.` prefix.

This function queries the Spock extension and returns the highest protocol
version number it can use for replication communication. The protocol
version determines the features and capabilities available for replication
between nodes.

When establishing replication connections between nodes running different
Spock versions, the nodes negotiate to use the lower of the two maximum
protocol versions. This ensures compatibility between nodes running
different Spock releases.


## spock_min_proto_version {#spock_min_proto_version}

Use `spock_min_proto_version` to retrieve the minimum protocol version
supported by Spock.

`spock_min_proto_version()`

Returns the minimum protocol version supported by the Spock extension.

This function takes no arguments, and is defined in the public
schema so must be invoked without the `spock.` prefix.

This function queries the Spock extension and returns the lowest protocol
version number it can use for replication communication. The protocol
version determines the features and capabilities available for replication
between nodes.

When establishing replication connections between nodes running different
Spock versions, the nodes negotiate to use a protocol version that falls
within the supported range of both nodes. The minimum protocol version
defines the lower bound of compatibility.

## spock.node_info {#spocknode_info}

Use `spock.node_info` to retrieve information about the local Spock node.

`spock.node_info()`

This function queries the Spock catalogs and returns metadata about the
current node, including its identifier, name, database information, and any
optional descriptive fields that were set during node creation.

This function takes no arguments.

## spock_version {#spock_version}

Use `spock_version` to retrieve the version string of the Spock extension.

`spock_version()`

Returns the version number of the Spock extension.

This function takes no arguments, and is defined in the public
schema so must be invoked without the `spock.` prefix.

This function queries the Spock extension and returns its version as a text
string. The version string typically follows semantic versioning format
(for example, "4.0.1" or "5.0.4").

## spock_version_num {#spock_version_num}

Use `spock_version_num` to retrieve the version number of Spock as an
integer. 

`spock_version_num()`

Returns the version number of the Spock extension as an integer.

This function takes no arguments, and is defined in the public
schema so must be invoked without the `spock.` prefix.

This function queries the Spock extension and returns its version encoded
as an integer value. The integer format allows for easy version comparison
in SQL queries without string parsing.

The integer typically represents the version in a format like XXYYZZ where
XX is the major version, YY is the minor version, and ZZ is the patch
version. For example, version 3.1.0 might be represented as 30100.

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/gen_mgmt.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
