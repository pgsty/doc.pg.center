---
upstream_link: https://github.com/percona/pg_tde/tree/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
title: Percona TDE documentation
linkTitle: Percona TDE
description: The complete pg_tde documentation, organized from first principles through installation, operations,
  and reference.
no_list: true
type: docs
sidebar_root_for: self
sidebar_root_link_self: true
cascade:
  type: docs
  upstream_name: percona/pg_tde documentation
  upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
  upstream_license: LicenseRef-pg-tde
  upstream_notice: /percona/site/attribution/
  upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
  upstream_modified: true
  upstream_source: percona
upstream_source: percona
weight: -50
outputs:
- HTML
- RSS
- print
- markdown
- LLMSFULL
icon: fa-solid fa-shield-halved
---


The pg_tde documentation follows the path a production PostgreSQL deployment takes: understand the encryption model, install the extension, configure key custody, validate encrypted tables, then operate WAL, backups, recovery, and upgrades.

- [Overview](/percona/index/) — understand TDE, pg_tde, supported deployments, and limitations.
- [Get started](/percona/install/) — install the package and create the extension.
- [Key management](/percona/global-key-provider-configuration/) — configure KMS providers and principal keys.
- [Technical reference](/percona/advanced-topics/) — architecture, functions, GUC variables, and replication.
- [Operations](/percona/how-to/) — backup, restore, enforcement, multi-tenancy, and upgrades.
- [Release notes](/percona/release-notes/) — follow compatibility and change history.

{.cards}
