---
title: pgEdge documentation
description: Documentation for core pgEdge extensions.
weight: -20
type: docs
sidebar_root_for: self
no_list: true
outputs:
- HTML
- RSS
- print
- markdown
- LLMSFULL
cascade:
  type: docs
  upstream_source: pgedge
upstream_source: pgedge
upstream_link: https://github.com/pgEdge/spock/tree/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c
linkTitle: pgEdge
sidebar_root_link_self: true
icon: fa-solid fa-share-nodes
---


Four extensions address concrete tasks in distributed PostgreSQL. Start with Spock replication, then add identifiers, large-object replication, and session protection as your application needs them.

- [Spock](/pgedge/spock/) — Multi-master replication and conflicts
- [Snowflake](/pgedge/snowflake/) — Distributed unique IDs
- [LOLOR](/pgedge/lolor/) — Large object logical replication
- [SafeSession](/pgedge/safesession/) — Read-only sessions by role
{.cards}

The English source set is Spock v6.0.0-beta.2, LOLOR 1.3.0 development, SafeSession v1.1, and Snowflake v2.6.1. The Chinese edition includes the reviewed incremental updates; unchanged portions of existing drafts retain their draft status. See [sources and versions](/pgedge/about/attribution/).

## Start reading {#start}

- [Quick start](/pgedge/quick-start/)
- [Sources and versions](/pgedge/about/attribution/)
