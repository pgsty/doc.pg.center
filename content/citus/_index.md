---
title: Citus 14 documentation
linkTitle: Citus
description: Scale PostgreSQL with Citus. Install a cluster, design distributed tables, migrate applications, and explore SQL, APIs, and technical articles.
weight: -4
type: docs
icon: fa-solid fa-table-cells-large
search_keywords: [Citus, distributed PostgreSQL, sharding, multitenant]
sidebar_root_for: self
sidebar_root_link_self: true
no_list: true
outputs: [HTML, RSS, print, markdown, LLMSFULL]
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/?view=citus-14
upstream_modified: true
cascade:
  type: docs
  upstream_source: citus
  upstream_modified: true
---

Citus is an open source PostgreSQL extension for distributed tables and parallel queries. Start with a single node, then add workers as your data and workload grow. Use PostgreSQL's SQL, drivers, and tools to build multitenant applications, real-time analytics, time series, and microservices.

> [!NOTE] Citus 14 edition
> This community edition follows the **Citus 14** documentation on Microsoft Learn, captured on **November 7, 2026**. The [sources and licensing page](/citus/attribution/) records the upstream revisions, retained blog articles, and translation policy.

- [Overview](/citus/overview/) — Architecture, sharding models, workloads, and common questions.
- [Installation](/citus/installation/) — Docker, Linux packages, single-node installations, and clusters.
- [Tutorials](/citus/tutorials/) — Build multitenant, analytics, time series, and microservice applications.
- [Data modeling](/citus/modeling/) — Distribution keys, colocation, application integration, and triggers.
- [Administration](/citus/operations/) — Manage tables, diagnose queries, tune performance, and upgrade.
- [Migration](/citus/migration/) — Adapt schemas and queries, move data, and migrate application frameworks.
- [SQL and API reference](/citus/reference/) — Functions, configuration, metadata, SQL support, and execution.
- [Articles and blog archive](/citus/articles/) — Ten technical articles on SaaS, aggregation, HyperLogLog, and more.
{.cards}

## Choose a starting point {#start}

**Try Citus locally:** follow the [Docker quickstart](/citus/installation/single-node-docker/), then run the [multitenant tutorial](/citus/tutorials/tutorial-multi-tenant/).

**Plan a distributed application:** compare [workloads and limitations](/citus/overview/postgresql-citus-scale/) and learn how to [choose a distribution column](/citus/modeling/data-modeling/).

**Operate a cluster:** start with [cluster management](/citus/operations/cluster-management/), [diagnostic queries](/citus/operations/diagnostic-queries/), and the [configuration reference](/citus/reference/api-guc/).

## Read and reuse {#reading}

Use the language menu or Duo View to read the English and Chinese editions. Search covers page titles, summaries, and section headings, including the API reference. The page menu provides printing and Markdown; the [complete Markdown manual](/citus/llms-full.txt) includes the collection in reading order, with source and license notices.

Original documentation: [Microsoft Learn](https://learn.microsoft.com/en-us/postgresql/citus/?view=citus-14). Project: [citusdata/citus](https://github.com/citusdata/citus). [Sources, copyright, and editorial notes](/citus/attribution/).
