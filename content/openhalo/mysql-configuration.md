---
type: docs
upstream_source: halodb
upstream_link: "" # Original summary; cite the reference below without claiming an upstream licence.
upstream_ref: "Halo Database 1.0.16; documentation snapshot 2026-11-07"
upstream_notice: /attribution/#halodb
title: Configure MySQL compatibility
linkTitle: Configuration and connection
description: Enable the Halo MySQL endpoint, install aux_mysql, create a user, and connect with mysql.
weight: 30
---

The current Halo Database instructions and the open-source OpenHalo README use different configuration names. Follow the section for the binary you are running.

## Halo 16: current mode setup {#halo-16}

Add the MySQL listener and its default database to `$PGDATA/postgresql.conf`:

```conf
cluster_net_services = ':3306:mysql'
mysql.default_tenant = 'mysql'
```

Both parameters are startup settings. Restart the server, create the database, and install the compatibility extension in that database:

```sh
pg_ctl restart
psql -c "CREATE DATABASE mysql;"
psql -d mysql -c "CREATE EXTENSION aux_mysql CASCADE;"
```

The official instructions state that `aux_mysql` also installs `plmyssql`. Install the extension in each database that will run MySQL compatibility syntax.

## Create a login role {#user}

Connect to the target database through the PostgreSQL-compatible administrative port and create a role with MySQL-native password encryption:

```sh
hsql -h /var/run/halo -p 1921 -U halo -d mysql
```

```sql
SET password_encryption = 'mysql_native_password';
CREATE USER mysqltest SUPERUSER PASSWORD 'replace-with-a-secret';
```

`SUPERUSER` follows the official smoke-test example and makes the demonstration work immediately. Use a separate least-privilege role with explicit database, schema, and table grants for an application. Do not copy the example password or grant superuser rights to an application account.

## Connect with the MySQL client {#connect}

Use the MySQL-compatible port and identify the target database explicitly:

```sh
mysql -h 127.0.0.1 -P 3306 -u mysqltest -D mysql -p
```

After connecting, verify the advertised compatibility version and run a small query:

```sql
SELECT VERSION();
SELECT 1;
```

`mysql.default_tenant` is the MySQL mode's default tenant database. The database passed to the setup must exist and have `aux_mysql` installed before it is used for compatibility syntax.

## MySQL mode parameters {#parameters}

The official [MySQL engine parameter reference](https://doc.halodbtech.com/multi-mode-compatibility/mysql-engine-parameters) says that `mysql.max_allowed_packet` is the only parameter in this group that can be changed online; the others require a restart.

| Parameter | Documented default | Use |
| --- | --- | --- |
| `mysql.default_tenant` | none; configure it | Default database for MySQL mode. |
| `mysql.max_allowed_packet` | `64MB` | Maximum protocol packet size; can be changed for the current session with `SET`. |
| `mysql.explicit_defaults_for_timestamp` | `off` | Controls automatic `TIMESTAMP` default behavior. |
| `mysql.on_error_rollback` | `on` | Automatically rolls back the current transaction after an error in MySQL mode. |
| `mysql.halo_mysql_version` | `5.7.32-log` | Version string reported to MySQL clients; it does not change the server binary. |
| `mysql.column_name_case_control` | `0` | Preserve column-name case; `1` lowercases and `2` uppercases. |
| `mysql.support_multiple_table_update` | `on` | Enables MySQL-style multi-table `UPDATE`. |
| `mysql.multi_table_delete_methond` | `1` | Selects the documented multi-table `DELETE` compatibility mode. The spelling is part of the upstream parameter name. |
| `mysql.create_trigger_for_auto_increment` | `on` | Creates the trigger used for `AUTO_INCREMENT` behavior. |
| `mysql.skip_utf8_verify` | `off` | Skips UTF-8 validation when enabled. |

Changing compatibility parameters can affect application-visible behavior. Record the values with the deployment configuration and retest migrations after changing them.

## OpenHalo source tree: legacy setup {#openhalo-legacy}

The pinned open-source [OpenHalo README](https://github.com/HaloTech-Co-Ltd/openHalo/blob/90fc8d777c3f111d4c8d236625bb15b5d4b19d7c/README.md) uses these parameter names:

```conf
database_compat_mode = 'mysql'
mysql.listener_on = true
mysql.port = 3306
```

These names belong to the source-tree version. Do not combine them with the Halo 16 `cluster_net_services` configuration. Check the `postgresql.conf.sample` shipped with the exact OpenHalo binary before starting it.

The original source-build and remote-login workflow remains in [Build and configure OpenHalo](/openhalo/quick-start/). Its `listen_addresses` and `pg_hba.conf` examples are PostgreSQL administration settings; they do not replace the MySQL listener configuration.

## Sources {#sources}

This page is an original summary of the [Halo Database MySQL compatibility reference](https://doc.halodbtech.com/multi-mode-compatibility/modes). No public documentation licence was identified; see the [source notice](/attribution/#halodb) for version, copyright, and citation details.
