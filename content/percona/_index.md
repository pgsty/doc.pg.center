---
upstream_link: https://github.com/percona/pg_tde/tree/5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a
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
  upstream_ref: 5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a
  upstream_modified: true
  upstream_source: percona-20261121
upstream_source: percona-20261121
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

The current release is [pg_tde 2.3.0](/percona/release-notes/release-notes-v2.3.0/), adding PostgreSQL 19 support and pg_tde-aware WAL record inspection. The Chinese edition is awaiting these incremental changes.

- [Overview](/percona/index/) — understand TDE, pg_tde, supported deployments, and limitations.
- [Get started](/percona/install/) — install the package and create the extension.
- [Key management](/percona/global-key-provider-configuration/) — configure KMS providers and principal keys.
- [Technical reference](/percona/advanced-topics/) — architecture, functions, GUC variables, and replication.
- [Operations](/percona/how-to/) — backup, restore, enforcement, multi-tenancy, and upgrades.
- [Release notes](/percona/release-notes/) — follow compatibility and change history.

{.cards}
