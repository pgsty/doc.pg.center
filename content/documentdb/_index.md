---
title: DocumentDB documentation
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/readme.md
description: 'DocumentDB 1.0: installation, operations, PostgreSQL APIs, commands, and operators.'
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
  upstream_source: documentdb
---

DocumentDB provides a PostgreSQL-based document database with BSON storage,
document operations, indexes, and a MongoDB wire protocol gateway. This edition
includes the published DocumentDB 1.0 documentation and its Simplified Chinese translation.

- [Getting started](/documentdb/getting-started/) — Docker, Linux packages, and your first query with a shell, driver, or editor.
- [DocumentDB Local](/documentdb/documentdb-local/) — Container options, persistent data, certificates, and telemetry.
- [Linux package operations](/documentdb/linux-packages/) — Secure, operate, upgrade, and install without internet access.
- [PostgreSQL API](/documentdb/postgres-api/) — Extensions, gateway, functions, and configuration parameters.
- [Command and operator reference](/documentdb/reference/) — MongoDB Query Language commands, expressions, and aggregation stages.
- [Kubernetes Operator](/documentdb/kubernetes-operator/) — Deployment prerequisites and the independently versioned operator manual.
{.cards}

> [!NOTE] Source edition
> The documentation repository is pinned at `cf69384`; website-generated guides
> and corrections are pinned at `90cfa08` (7 November 2026). The upstream
> [architecture chapter](/documentdb/architecture/) is still forthcoming.
> See [source and translation notices](/attribution/#documentdb).
