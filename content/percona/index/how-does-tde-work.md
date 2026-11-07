---
title: How pg_tde works
linkTitle: How it works
description: How pg_tde applies encryption within the PostgreSQL storage path.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/index/how-does-tde-work.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 140
upstream_source: percona
---

To encrypt the data, two types of keys are used:

* **Internal encryption keys** to encrypt user data. They are stored internally, near the data that they encrypt.
* The **principal key** to encrypt database keys. It is kept separately from the database keys and is managed externally in the key management store.

> [!NOTE]
> For more information on managing and storing principal keys externally, including supported key management systems and the local keyring option, see [Key management overview](/percona/global-key-provider-configuration/overview/).

The encryption process works as follows:

![image](/percona/assets/images/tde-flow.png)

When a user creates an encrypted table using `pg_tde`, a new random key is generated internally for that table and is encrypted using the AES-CBC cipher algorithm. This key is used to encrypt all data the user inserts in that table. Eventually the encrypted data gets stored in the underlying storage.

The internal key itself is encrypted using the principal key. The principal key is stored externally in the key management store.

Similarly when the user queries the encrypted table, the principal key is retrieved from the key store to decrypt the internal key. Then the same unique internal key for that table is used to decrypt the data, and unencrypted data gets returned to the user. So, effectively, every TDE table has a unique key, and each table key is encrypted using the principal key.

[Understand the encrypted data scope ](/percona/index/tde-encrypts/)
