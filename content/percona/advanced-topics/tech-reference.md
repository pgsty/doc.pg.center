---
title: Technical reference overview
linkTitle: Reference overview
description: Find the architecture, configuration, SQL, and replication reference pages.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a/documentation/docs/advanced-topics/tech-reference.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a
upstream_modified: true
weight: 610
upstream_source: percona-20261121
---

This section covers the internal components and tools that power `pg_tde`.

Use it to understand how encryption is implemented, fine-tune a configuration, leverage advanced CLI tools and functions for diagnostics and customization.

### Usage reference {#usage-reference}

A description of the main `pg_tde` operations available, including configuring key providers, managing principal keys, setting permissions, and encrypting tables.

[Follow the usage guide ](/percona/advanced-topics/usage-guide/)

### Functions {#functions}

Use built-in functions to manage key providers, create and rotate principal keys, and verify encryption status. Includes commands for Vault, KMIP, and local providers, plus utilities to inspect or validate keys.

[Browse available functions →](/percona/functions/)

### GUC Variables {#guc-variables}

Configure how `pg_tde` behaves with PostgreSQL. Control WAL encryption, enforce encryption for new tables, and manage global provider inheritance. Includes scope levels, defaults, and permission requirements.

[Configure GUC variables ](/percona/variables/)

### Streaming replication {#streaming-replication}

Learn how to configure PostgreSQL streaming replication with `pg_tde` using the `tde_heap` access method. Covers primary and standby setup, key management requirements, and validation steps.

[Set up replication with `tde_heap` ](/percona/replication/)
