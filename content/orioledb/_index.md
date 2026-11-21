---
title: OrioleDB documentation
linkTitle: OrioleDB
description: Install and configure OrioleDB, explore its storage engine, build from source, and reproduce benchmarks.
weight: -5
type: docs
search_keywords: ["OrioleDB", "orioledb"]
icon: fa-solid fa-dove
sidebar_root_for: self
sidebar_root_link_self: true
no_list: true
outputs: [HTML, RSS, print, markdown, LLMSFULL]
upstream_source: orioledb
upstream_link: https://www.orioledb.com/docs
upstream_notice: /orioledb/attribution/
upstream_modified: true
cascade:
  type: docs
  upstream_source: orioledb
---

OrioleDB is a PostgreSQL storage engine built around index-organized tables, undo-based MVCC, copy-on-write checkpoints, and row-level WAL. This manual covers installation, configuration, storage internals, development, and benchmark reproduction.

> [!NOTE] Version context
> This edition follows the upstream website snapshot of **2026-11-06**. The guides describe a Beta release and require patched PostgreSQL binaries; the benchmark recipes use beta18. Check the [installation requirements and limitations](/orioledb/usage/getting-started/#current-limitations) before using the examples.

- [Overview](/orioledb/introduction/) — Storage design and PostgreSQL patches.
- [Usage](/orioledb/usage/) — Installation, configuration, rewind, and upgrades.
- [Architecture](/orioledb/architecture/) — B-trees, undo logs, checkpoints, and recovery.
- [Development](/orioledb/contributing/) — Source builds and binary compatibility.
- [Benchmarks](/orioledb/benchmarks/) — pgbench and vehicle-tracking workloads.
- [Sources and licensing](/orioledb/attribution/) — Snapshot coverage and original rights.
{.cards}

## Release update {#release-update}

[OrioleDB v1.10.3](https://github.com/orioledb/orioledb/releases/tag/v1.10.3), published on November 9, 2026, fixes `INSERT ... ON CONFLICT DO UPDATE` silently skipping a row with a committed foreign-key lock whose undo has already been passed by a checkpoint or by time. The SQL extension version remains `1.10`; the release changes neither the storage format nor the WAL format.

The guides remain the website snapshot described above, and historical benchmark recipes retain their original versions. This release notice does not change the project's Beta status or the requirement for patched PostgreSQL.

## Start reading {#start}

Start with [Getting started](/orioledb/usage/getting-started/) to create your first OrioleDB table, then consult the [configuration reference](/orioledb/usage/configuration/). For implementation details, begin with the [architecture overview](/orioledb/architecture/overview/).

Every page has an English and Chinese edition. Use Duo View to read them side by side, or the page menu to print and copy Markdown. The [complete Markdown manual](/orioledb/llms-full.txt) is also available as one file.
