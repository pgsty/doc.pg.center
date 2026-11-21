---
title: DocumentDB documentation
type: docs
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/readme.md
description: 'DocumentDB 1.2.0: installation, operations, PostgreSQL APIs, commands, and operators.'
linkTitle: DocumentDB
weight: -10
sidebar_root_for: self
sidebar_root_link_self: true
no_list: true
icon: fa-solid fa-file-code
outputs:
- HTML
- RSS
- print
- markdown
- LLMSFULL
cascade:
  type: docs
  upstream_source: documentdb-20261121
---

DocumentDB provides a PostgreSQL-based document database with BSON storage,
document operations, indexes, and a MongoDB wire protocol gateway. This edition
covers the published DocumentDB 1.2.0 documentation. The existing Simplified Chinese edition remains based on 1.0 while the incremental translation is pending.

- [Release notes for 1.2](/documentdb/getting-started/release-notes-1.2/) — Compatibility, container startup, upgrades, and renamed metrics.
- [Getting started](/documentdb/getting-started/) — Docker, Linux packages, and your first query with a shell, driver, or editor.
- [DocumentDB Local](/documentdb/documentdb-local/) — Container options, persistent data, certificates, and telemetry.
- [Linux package operations](/documentdb/linux-packages/) — Secure, operate, upgrade, and install without internet access.
- [PostgreSQL API](/documentdb/postgres-api/) — Extensions, gateway, functions, and configuration parameters.
- [Command and operator reference](/documentdb/reference/) — MongoDB Query Language commands, expressions, and aggregation stages.
- [Kubernetes Operator](/documentdb/kubernetes-operator/) — Deployment prerequisites and the independently versioned operator manual.
{.cards}

> [!NOTE] Source edition
> The documentation repository is pinned at `8fb7fda`; website-generated guides
> and corrections are pinned at `4a83a07` (21 November 2026). The upstream
> [architecture chapter](/documentdb/architecture/) is still forthcoming.
> See [source and translation notices](/attribution/#documentdb).
