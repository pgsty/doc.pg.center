---
title: Encryption enforcement
linkTitle: Encryption enforcement
description: Require new tables to use encryption at the server, database, role, or session level.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/how-to/enforcement.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 530
upstream_source: percona
---

For `pg_tde`, encryption enforcement ensures that only encrypted storage is allowed for specific operations, tables, or the entire database. It prevents the accidental creation of unencrypted tables or indexes in environments where encryption is required for compliance, security, or policy enforcement.

## What does enforcement do? {#what-does-enforcement-do}

When enabled, encryption enforcement:

* Prevents creation of unencrypted tables or indexes
* Enforces consistent encryption usage across tenants, databases, or users
* Can be scoped globally, per database, or per role

## Enforce encryption usage {#enforce-encryption-usage}

Use the following techniques to enforce the secure use of `pg_tde`.

### 1. Enforce encryption across the server {#1-enforce-encryption-across-the-server}

To enforce encryption cluster-wide, set the [`pg_tde.enforce_encryption`](/percona/variables/#pgtde-enforceencryption) variable in `postgresql.conf`:

```ini
pg_tde.enforce_encryption = on
```

> [!NOTE]
> **Only** superusers can set or change this variable.

This ensures that no user, including superusers, can create unencrypted tables. Superusers can however explicitly [override the variable in their session](#override-enforcement-for-trusted-sessions).

### 2. Enforce encryption for a specific database {#2-enforce-encryption-for-a-specific-database}

To apply encryption enforcement only within a specific database, run:

```sql
ALTER DATABASE example_db SET pg_tde.enforce_encryption = on;
```

This ensures encryption is enforced **only** when connected to that database.

### 3. Enforce encryption for a specific user {#3-enforce-encryption-for-a-specific-user}

You can also enforce encryption on a per-user basis, run:

```sql
ALTER USER example_user SET pg_tde.enforce_encryption = on;
```

This ensures that the user `example_user` cannot create unencrypted tables, regardless of which database they connect to.

### Override enforcement for trusted sessions {#override-enforcement-for-trusted-sessions}

Superusers can override the variable at the session level:

```sql
SET pg_tde.enforce_encryption = off;
```

This allows temporary creation of unencrypted tables in special cases, such as:

* Loading trusted, public reference datasets
* Benchmarking and test environments
* Migration staging before re-encryption

> [!NOTE]
> While superusers can disable enforcement in their session, they must do so explicitly. Enforcement defaults remain active to protect from accidental misconfiguration.
