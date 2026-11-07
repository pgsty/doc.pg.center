---
title: spock.node_alter()
description: spock.nodealter (plocation text DEFAULT NULL, pcountry text DEFAULT NULL, pinfopatch jsonb DEFAULT
  NULL)
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_node_alter.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



spock.node_alter()

## SYNOPSIS {#synopsis}

spock.node_alter (p_location text DEFAULT NULL, p_country text DEFAULT NULL,
p_info_patch jsonb DEFAULT NULL)

## RETURNS {#returns}

`true` on success. Raises an error if `p_info_patch` is not a JSON object,
or if it contains a `tiebreaker` key that is not a JSON number, is not a
whole number, or does not fit a 32-bit integer.

## DESCRIPTION {#description}

Changes the local node's own `location`, `country`, and/or `info`, merging
`p_info_patch` into the existing `info` rather than replacing it. Only
this node's own row can be altered -- there is no `node_name` argument,
since (unlike `spock.node_refresh_info`) there is only ever one valid
target: the local node.

Any omitted argument (left `NULL`) is left unchanged: `p_location` and
`p_country` each independently overwrite only if non-`NULL`, and
`p_info_patch` is merged key-by-key into the existing `info` (via `||`)
only if non-`NULL` -- an existing key not mentioned in the patch is left
as-is, not removed.

A `tiebreaker` key inside `p_info_patch` is validated: it must be a JSON
number (not a string, and not JSON `null`), a whole number, and fit a
32-bit integer, or the call raises an error and changes nothing. This is
the safe way to change a node's tiebreaker; see the Tiebreaker section in
[conflict_types.md](/pgedge/spock/conflicts/) for what the tiebreaker
does and why validation matters here.

This ends in the same `UPDATE spock.node` that a hand-written `UPDATE`
would use, so it propagates identically: automatically to every direct
subscriber of this node (see
[Automatic node metadata propagation](/pgedge/spock/reference/node-mgmt/#automatic-node-metadata-propagation)),
with no manual step required. A raw `UPDATE spock.node SET ...` on this
node's own row remains fully supported and behaves the same way --
`spock.node_alter` exists to validate the input and merge `info` safely,
not to gate access to the underlying table.

## ARGUMENTS {#arguments}

p_location

    Optional. Replaces this node's `location`. Left unchanged if omitted
    (or NULL).

p_country

    Optional. Replaces this node's `country`. Left unchanged if omitted
    (or NULL).

p_info_patch

    Optional. A JSON object merged into this node's existing `info`
    (existing keys not mentioned are preserved). Left unchanged if
    omitted (or NULL). A `tiebreaker` key, if present, must be a JSON
    number representable as a 32-bit integer.

## EXAMPLE {#example}

Assign a custom tiebreaker on `n1`, without disturbing any other `info`
keys already set:

    n1=# SELECT spock.node_alter(p_info_patch => '{"tiebreaker": 42}'::jsonb);
     node_alter
    ------------
     t
    (1 row)

Every direct subscriber of `n1` picks this up automatically -- no
`spock.node_refresh_info` call needed:

    n2=# SELECT info->>'tiebreaker' FROM spock.node WHERE node_name = 'n1';
     ?column?
    ----------
     42
    (1 row)

Update location and country together in one call:

    n1=# SELECT spock.node_alter(p_location => 'us-east', p_country => 'US');
     node_alter
    ------------
     t
    (1 row)

An invalid tiebreaker is rejected and changes nothing:

    n1=# SELECT spock.node_alter(p_info_patch => '{"tiebreaker": "42"}'::jsonb);
    ERROR:  invalid "tiebreaker" value "42": must be a JSON number, not a string or null

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_node_alter.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
