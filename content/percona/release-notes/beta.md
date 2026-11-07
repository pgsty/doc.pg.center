---
title: pg_tde Beta (2024-06-30)
linkTitle: Beta
description: Changes, compatibility notes, and fixes for pg_tde Beta (2024-06-30).
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/release-notes/beta.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 920
upstream_source: percona
---

> [!NOTE] Historical release
> This page describes this release at publication time. For current deployment requirements, read the [supported versions](/percona/index/supported-versions/) and [limitations](/percona/index/tde-limitations/).

`pg_tde` extension brings in [Transparent Data Encryption (TDE)](/percona/index/about-tde/) to PostgreSQL and enables you to keep sensitive data safe and secure.

[Get started](/percona/install/)

> [!IMPORTANT]
>
> This version of Percona Transparent Data Encryption extension **is 
> not recommended for production environments yet**. We encourage you to test it and [give your feedback](https://forums.percona.com/c/postgresql/pg-tde-transparent-data-encryption-tde/82).
>
> This will help us improve the product and make it production-ready faster.

## Release Highlights {#release-highlights}

Starting with `pg_tde` Beta, the access method for `pg_tde` extension is renamed `tde_heap_basic`. Use this access method name to create tables. Find guidelines in [Test TDE](/percona/test/) tutorial.

## Changelog {#changelog}

* Fixed the issue with `pg_tde` running out of memory used for decrypted tuples. The fix introduces the new component `TDEBufferHeapTupleTableSlot` that keeps track of the allocated memory for decrypted tuples and frees this memory when the tuple slot is no longer needed.

* Fixed the issue with adjusting a current position in a file by using raw file descriptor for the `lseek` function. (Thanks to user _rainhard_ for providing the fix)

* Enhanced the init script to consider a custom superuser for the POSTGRES_USER parameter when `pg_tde` is running via Docker (Thanks to _Alejandro Paredero_ for reporting the issue)
