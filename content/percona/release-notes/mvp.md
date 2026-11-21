---
title: pg_tde MVP (2023-12-12)
linkTitle: MVP
description: Changes, compatibility notes, and fixes for pg_tde MVP (2023-12-12).
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a/documentation/docs/release-notes/mvp.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a
upstream_modified: true
weight: 940
upstream_source: percona-20261121
---

> [!NOTE] Historical release
> This page describes this release at publication time. For current deployment requirements, read the [supported versions](/percona/index/supported-versions/) and [limitations](/percona/index/tde-limitations/).

The Minimum Viable Product (MVP) version of `pg_tde` introduces the following functionality:

* Encryption of heap tables, including TOAST
* Encryption keys are stored either in Hashicorp Vault server or in local keyring file (for development)
* The key storage is configurable via separate JSON configuration files
* Replication support
