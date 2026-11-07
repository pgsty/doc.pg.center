---
title: PgAudit
linkTitle: pgaudit
description: 'IvorySQL v5.6 documentation: PgAudit.'
type: docs
weight: 430
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/5.8.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

## 1. Overview {#overview}

PgAudit is an auditing extension for IvorySQL that produces traceable log records for critical operations such as DDL, DML, and DCL. With the audit trail, database administrators can meet compliance requirements, quickly detect abnormal behavior, and identify accountability and impact scope when incidents occur.

## 2. Key Features {#key-features}

- **Comprehensive auditing**: Captures `SELECT`, `INSERT`, `UPDATE`, `DELETE`, DDL commands, privilege changes, and more to build a complete activity timeline.

- **Flexible scope control**: Supports global, role-based, and object-level auditing, allowing fine-grained configuration by user, role, schema, or operation type.

- **Seamless integration**: Reuses PostgreSQL’s standard logging subsystem and works with tools like `syslog` and `logrotate`, aligning with existing log ingestion and analysis pipelines.

- **Compliance ready**: Generates structured audit logs suitable for meeting regulatory requirements in finance, government, and other regulated industries.

- **Security enhancement**: Records and inspects database activity to surface unauthorized access, anomalous DML, or potential data leakage risks in time.

- **Operations insight**: Helps replay operational actions, locate performance bottlenecks, and support SQL tuning and incident troubleshooting.

## 3. Installation and Deployment {#installation-and-deployment}

### 3.1. Prerequisites {#prerequisites}

- A IvorySQL installation (recommended version aligned with the targeted PgAudit release).

- Build toolchain: `gcc`, `make`, `tar`, etc.

- Database superuser privileges to modify `ivorysql.conf` and restart the instance.

### 3.2. Compile and Install PgAudit {#compile-and-install-pgaudit}

Taking PgAudit 18.0 as an example:

```
wget https://github.com/pgaudit/pgaudit/archive/refs/tags/18.0.tar.gz
tar -xf 18.0.tar.gz
cd pgaudit-18.0
make install USE_PGXS=1 PG_CONFIG=$PGHOME/bin/pg_config
```

The commands above expect the environment variable `PGHOME` to point to the installed IvorySQL home directory. After installation, `pgaudit.so` will be placed in IvorySQL’s extension directory.

### 3.3. Baseline Configuration Before Registering the Extension {#baseline-configuration-before-registering-the-extension}

1.  Modify `ivorysql.conf` to load the plugin and configure common parameters: ---- shared_preload_libraries = 'pgaudit' \# Requires an instance restart pgaudit.log = 'read, write, ddl' \# Sample audit scope; adjust as needed ----

2.  Restart or reload the database instance so the shared library configuration takes effect.

### 3.4. Create the Extension and Verify {#create-the-extension-and-verify}

``` sql
CREATE EXTENSION IF NOT EXISTS pgaudit;
SELECT name,
       default_version,
       installed_version,
       comment
  FROM pg_available_extensions
 WHERE name = 'pgaudit';
```

If the returned `installed_version` matches the expected release, the extension has been installed successfully.

## 4. Usage {#usage}

Execute the following SQL sample:

```
[source,sql]
----
CREATE TABLE audit_demo(id serial PRIMARY KEY, info text);
INSERT INTO audit_demo(info) VALUES ('pgaudit test');
SELECT * FROM audit_demo;
UPDATE audit_demo SET info = 'pgaudit update' WHERE id = 1;
DELETE FROM audit_demo WHERE id = 1;
----
```

Check the audit logs on the database server:

```
tail -f $PGDATA/log/*.log | grep 'AUDIT:'
```

```
2025-10-31 15:56:32.113 CST [11451] LOG:  AUDIT: SESSION,1,1,DDL,CREATE SEQUENCE,SEQUENCE,public.audit_demo_id_seq,"CREATE TABLE audit_demo(id serial PRIMARY KEY, info text)",<not logged>
2025-10-31 15:56:32.113 CST [11451] LOG:  AUDIT: SESSION,1,1,DDL,CREATE TABLE,TABLE,public.audit_demo,"CREATE TABLE audit_demo(id serial PRIMARY KEY, info text)",<not logged>
2025-10-31 15:56:32.113 CST [11451] LOG:  AUDIT: SESSION,1,1,DDL,CREATE INDEX,INDEX,public.audit_demo_pkey,"CREATE TABLE audit_demo(id serial PRIMARY KEY, info text)",<not logged>
2025-10-31 15:56:32.113 CST [11451] LOG:  AUDIT: SESSION,1,1,DDL,ALTER SEQUENCE,SEQUENCE,public.audit_demo_id_seq,"CREATE TABLE audit_demo(id serial PRIMARY KEY, info text)",<not logged>
2025-10-31 15:56:32.117 CST [11451] LOG:  AUDIT: SESSION,2,1,WRITE,INSERT,,,INSERT INTO audit_demo(info) VALUES ('pgaudit test'),<not logged>
2025-10-31 15:56:32.121 CST [11451] LOG:  AUDIT: SESSION,3,1,READ,SELECT,,,SELECT * FROM audit_demo,<not logged>
2025-10-31 15:56:32.122 CST [11451] LOG:  AUDIT: SESSION,4,1,WRITE,UPDATE,,,UPDATE audit_demo SET info = 'pgaudit update' WHERE id = 1,<not logged>
2025-10-31 15:56:32.127 CST [11451] LOG:  AUDIT: SESSION,5,1,WRITE,DELETE,,,DELETE FROM audit_demo WHERE id = 1,<not logged>
```

To record parameter values as well, enable `pgaudit.log_parameter = 'on'`:

```
ivorysql=# SHOW pgaudit.log_parameter;
pgaudit.log_parameter
-----------------------
on
(1 row)
```
