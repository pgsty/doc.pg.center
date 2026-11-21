---
title: Encrypted data scope
linkTitle: Encrypted data
description: Identify encrypted data files, WAL, and the information that remains unencrypted.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a/documentation/docs/index/tde-encrypts.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a
upstream_modified: true
weight: 160
upstream_source: percona-20261121
---

`pg_tde` encrypts the following components:

* **User data** in tables using the extension, including associated TOAST data. The table metadata (column names, data types, etc.) is not encrypted.
* **Temporary tables** created during the query execution, for data tables created using the extension.
* **Write-Ahead Log (WAL) data** for the entire database cluster. This includes WAL data in encrypted and non-encrypted tables.
* **Indexes** on encrypted tables.

[Check out the table access methods ](/percona/index/table-access-method/)
