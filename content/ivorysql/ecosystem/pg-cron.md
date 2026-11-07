---
title: pgcron
linkTitle: pg_cron
description: 'IvorySQL v5.6 documentation: pgcron.'
type: docs
weight: 390
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/5.4.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

## 1. Overview {#overview}

Running periodic tasks in PostgreSQL, such as executing VACUUM or deleting old data, is a common requirement. A simple way to achieve this is to configure cron or other external daemons to periodically connect to the database and run commands. However, as databases increasingly run as managed services or standalone containers, configuring and running a separate daemon often becomes impractical. Additionally, it’s difficult to make your cron jobs aware of failover or schedule tasks across cluster nodes.

pg_cron is an open-source scheduled task extension for PostgreSQL that allows setting up cron-style task scheduling directly within the database for automating data maintenance tasks (cleanup, aggregation), database health checks, executing stored procedures and custom functions, and other operations. It stores cron jobs in tables, and periodic tasks automatically fail over with the PostgreSQL server. For more details, see [pg_cron documentation](https://github.com/citusdata/pg_cron).

## 2. Installation and Configuration {#installation-and-configuration}

> [!TIP]
>
> The source installation environment is Ubuntu 24.04 (x86_64). IvorySQL 5 or higher version is already installed in the environment, with the installation path at /usr/local/ivorysql/ivorysql-5

### 2.1. Source Installation {#source-installation}

```
# Clone pg_cron source code
git clone https://github.com/citusdata/pg_cron.git
cd pg_cron
# Set pg_config path to PATH environment variable, e.g.:
export PATH=/usr/local/ivorysql/ivorysql-5/bin/:$PATH
make
make install
```

### 2.2. Configuration File (ivorysql.conf) {#configuration-file-ivorysql-conf}

```
# Shared preload extensions
shared_preload_libraries = 'pg_cron'

# Specify task metadata storage database (default current database)
cron.database_name = 'ivorysql'

# Maximum number of concurrent tasks allowed
cron.max_running_jobs = 5
```

### 2.3. Restart Service {#restart-service}

```
pg_ctl restart -D ./data -l logfile
```

### 2.4. Create Extension and Confirm pg_cron Version {#create-extension-and-confirm-pg_cron-version}

Connect to the database with psql and execute the following commands:

```
ivorysql=# CREATE extension pg_cron;
CREATE EXTENSION

ivorysql=# SELECT * FROM pg_available_extensions WHERE name = 'pg_cron';
   name  | default_version | installed_version |         comment
---------+-----------------+-------------------+---------------------------
 pg_cron | 1.6             |                   |Job scheduler for PostgreSQL
(1 row)
```

## 3. Core Functionality Usage {#core-functionality-usage}

### 3.1. Creating Scheduled Tasks {#creating-scheduled-tasks}

```
SELECT cron.schedule(
    'nightly-data-cleanup',        -- Task name (unique identifier)
    '0 3 * * *',                   -- Cron expression (daily at UTC 3:00)
    $$DELETE FROM logs
      WHERE created_at < now() - interval '30 days'$$  -- SQL to execute
);
```

Cron expression quick reference:

|                     |                                           |
|---------------------|-------------------------------------------|
| Example             | Meaning                                   |
| '0 \* \* \* \*'     | Execute every hour on the hour            |
| '\*/15 \* \* \* \*' | Execute every 15 minutes                  |
| '0 9 \* \* 1-5'     | Execute at 9 AM on weekdays               |
| '0 1 1 \* \*'       | Execute at 1 AM on the 1st of every month |

pg_cron also allows using '\$' to represent the last day of the month.

### 3.2. Task Management {#task-management}

```
# View all tasks
SELECT * FROM cron.job;
```

![p31](/ivorysql/assets/images/upstream/f1e7ed6982ac72fd4ba945ad8be0245fe3cae0ad89bdb588d7f00631e7c0579e.png)

```
# View task execution history
SELECT * FROM cron.job_run_details ORDER BY start_time DESC LIMIT 10;
```

![p32](/ivorysql/assets/images/upstream/3859c53deb367ed120bf122be3c2fc7fbc8142db7738a77c56b03bcc0b5fe0a4.png)

```
# Delete task
SELECT cron.unschedule('nightly-data-cleanup');

# Pause task (update status)
UPDATE cron.job SET active = false WHERE jobname = 'delete-job-run-details';
```
