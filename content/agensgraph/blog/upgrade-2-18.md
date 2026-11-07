---
title: What changed in AgensGraph 2.18
linkTitle: What changed in AgensGraph 2.18
description: PostgreSQL 18, GQL additions, typed columns, and the checks to run before upgrading.
type: docs
date: 2026-11-07
tags:
- Release
- Upgrade
- PostgreSQL
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/release_notes/2.18.html
upstream_source: agensgraph
upstream_modified: true
summary: A source-linked upgrade checklist for AgensGraph 2.18.
---

AgensGraph 2.18 moves the base from PostgreSQL 17.10 to PostgreSQL 18. The release adds a substantial part of GQL, introduces typed-column property promotion, improves graph planning, and fixes several crash and wrong-result classes.

The changes that deserve an application test are more specific than the headline:

- `xor`, `current_graph`, and `current_property_graph` become reserved words;
- conditions in `WHERE`, `FILTER`, `AND`, `OR`, `NOT`, `XOR`, and `CASE WHEN` must be boolean;
- `collect()` over graph elements returns graph arrays;
- pagination after `WITH … WHERE` follows filter, order, then limit;
- row-level security on graph writes is enforced correctly;
- a 2.17 data directory cannot be started by 2.18 binaries.

The safest upgrade sequence is to inventory identifiers and query results, take a tested backup, upgrade a copy of the cluster, rerun RLS and pagination tests, and only then move the production data directory. The [release notes](/agensgraph/release-notes/2.18/) carry the complete change list and the [upgrade procedure](/agensgraph/release-notes/upgrade-to-2.18/) carries the operational sequence.
