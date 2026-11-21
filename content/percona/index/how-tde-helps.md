---
title: Benefits of pg_tde
linkTitle: Why TDE?
description: Where database-level encryption complements other protections for stored data.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a/documentation/docs/index/how-tde-helps.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a
upstream_modified: true
weight: 150
upstream_source: percona-20261121
---

The benefits of using `pg_tde` are outlined below for different users and organizations.

## Benefits for organizations {#benefits-for-organizations}

* **Data safety:** Prevents unauthorized access to stored data, even if backup files or storage devices are stolen or leaked.
* **Enterprise-ready Architecture:** Supports both single and multi-tenancy, giving flexibility for SaaS providers or internal multi-user systems.

## Benefits for DBAs and engineers {#benefits-for-dbas-and-engineers}

* **Granular control:** Encrypt specific tables or databases instead of the entire system, reducing performance overhead.
* **Operational simplicity:** Works transparently without requiring major application changes.
* **Defense in depth:** Adds another layer of protection to existing controls like TLS (encryption in transit), access control, and role-based permissions.

When combined with the external Key Management Systems (KMS), `pg_tde` enables centralized control, auditing, and rotation of encryption keys—critical for secure production environments.

> [!NOTE] See also
>
> You can find more information on Transparent Data Encryption (TDE) in [this article](https://www.percona.com/blog/transparent-data-encryption-tde/).

[Learn how pg_tde works ](/percona/index/how-does-tde-work/)
