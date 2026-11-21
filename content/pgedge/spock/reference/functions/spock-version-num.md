---
title: spock.version_num()
description: The version number of the installed Spock extension as an integer.
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_version_num.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
---



spock.spock_version_num()

## SYNOPSIS {#synopsis}

spock.spock_version_num ()

## RETURNS {#returns}

The version number of the installed Spock extension as an integer.

## DESCRIPTION {#description}

Returns the version number of the Spock extension as an integer.

This function queries the Spock extension and returns its version encoded as
an integer value. The integer format allows for easy version comparison in
SQL queries without string parsing.

The integer typically represents the version in a format like XXYYZZ where XX
is the major version, YY is the minor version, and ZZ is the patch version.
For example, version 3.1.0 might be represented as 30100.

This is a read-only query function that does not modify any data.

## ARGUMENTS {#arguments}

This function takes no arguments.

## EXAMPLE {#example}

The following command returns the current Spock extension version as an
integer:

    postgres=# SELECT spock.spock_version_num();
    -[ RECORD 1 ]-----+------
    spock_version_num | 50005

---

[Upstream source](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_version_num.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
