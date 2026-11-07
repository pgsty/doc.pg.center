---
title: Documentation errata
description: Corrections made to the fixed pg_tde documentation snapshot.
type: docs
translation_notice: false
upstream_source: percona
upstream_link: https://github.com/percona/pg_tde/tree/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
---


These corrections apply to the [1660e66a6a30 snapshot](https://github.com/percona/pg_tde/tree/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39). They are downstream editorial changes, not an assertion that the upstream repository has merged them. Original files remain identifiable by the [source manifest](/percona/assets/source-manifest.json).

| Page | Correction | Evidence |
| --- | --- | --- |
| [Functions](/percona/functions/) and [usage reference](/percona/advanced-topics/usage-guide/) | Use `pg_tde.inherit_global_providers`; remove obsolete parameter names. | [GUC declarations](https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/src/pg_tde_guc.c) |
| [Functions](/percona/functions/) | `pg_tde_set_key_using_global_key_provider` sets the current database key. The separate server function sets the WAL key. | [Key implementation](https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/src/catalog/tde_principal_key.c) |
| [Usage reference](/percona/advanced-topics/usage-guide/) | Server/default key setters use global providers; the `(global/database)` notation is invalid for those two functions. | [SQL definitions](https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/pg_tde--1.0.sql) |
| [Restore tool](/percona/command-line-tools/pg-tde-restore-encrypt/) | `%f` is the WAL file name; `%p` is the destination for the unencrypted WAL segment. | [Built-in help](https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/src/bin/pg_tde_restore_encrypt.c) |
| [Replication](/percona/replication/) | Create the principal key before assigning it as the server key. | [SQL definitions](https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/pg_tde--1.0.sql) |
| [FAQ](/percona/faq/) | `work_mem` spill files are not encrypted; ordinary `VACUUM` does not rotate a file’s internal key. Use a table rewrite such as `VACUUM FULL`. | [Limitations](/percona/index/tde-limitations/) and [architecture](/percona/architecture/encryption-architecture/) |
| [Keyring example](/percona/global-key-provider-configuration/keyring/) | Inspect `customer_table`, the table actually created; use `pg_tde_key_info()` for the current database key. | [Function reference](/percona/functions/) |
| [KMIP overview](/percona/global-key-provider-configuration/overview/) | Preserve the older verification wording but flag its difference from the 2.2.2 announcement of Vault Enterprise KMIP support. | [2.2.2 release notes](/percona/release-notes/release-notes-v2.2.2/) |

We also close a missing SQL quote, remove a duplicated RC changelog fragment, repair Markdown links and anchors, and replace MkDocs tabs/callouts with Oink components. Historical releases are labelled by their period. The upstream chatbot and feedback embed are not included.

The reproducible English transformations are recorded in `scripts/import_upstream.py` and `scripts/upstream_edits.json`; Chinese counterparts are maintained alongside them. Translation review is a self-review, not an independent certification or a runtime test of pg_tde.
