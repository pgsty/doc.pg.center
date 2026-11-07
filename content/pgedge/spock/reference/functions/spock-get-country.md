---
title: spock.get_country()
description: The country code configured for the node as text, or ?? if not set.
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_get_country.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



spock.get_country()

## SYNOPSIS {#synopsis}

spock.get_country ()

## RETURNS {#returns}

The country code configured for the node as text, or `??` if not set.

## DESCRIPTION {#description}

Returns the spock.country property that was set during node creation. You can
modify the property after configuration; modification requires a server
restart to apply the change.

This function retrieves the value of the spock.country configuration
parameter for the current session. The country code is typically used in
multi-region or geo-distributed replication topologies to identify the
geographic location of nodes and apply region-specific routing or filtering
rules.

This function does not modify any data.

## ARGUMENTS {#arguments}

This function takes no arguments.

## EXAMPLE {#example}

If the spock.country parameter has not been set, the function returns:

    postgres=# SELECT spock.get_country();
     get_country
    -------------
     ??
    (1 row)

If spock.country is set to `US`, the function returns:

    postgres=# SELECT spock.get_country();
     get_country
    -------------
     US
    (1 row)

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_get_country.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
