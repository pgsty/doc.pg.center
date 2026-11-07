---
title: pgcron
linkTitle: pg_cron
description: IvorySQL v5.6 文档：pgcron。
type: docs
weight: 390
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/5.4.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---

## 1. 概述 {#overview}

在 PostgreSQL 中运行周期性任务，例如执行 VACUUM或删除旧数据，是一种常见需求。实现这一点的简单方法是配置 cron或其他外部守护进程，使其定期连接到数据库并运行命令。然而，随着数据库越来越多地作为托管服务或独立容器运行，配置和运行一个单独的守护进程通常变得不切实际。此外，很难让您的 cron任务感知故障转移，或者跨集群节点调度任务。

pg_cron 是 PostgreSQL 的开源定时任务扩展，允许直接在数据库内部设置 cron 风格的任务调度，用于自动化数据维护任务(清理，聚合), 数据库健康检查，执行存储过程和自定义函数等操作。它将cron任务存储在表中，周期性任务会随着 PostgreSQL 服务器自动进行故障转移。详情可以参见 [pg_cron文档](https://github.com/citusdata/pg_cron)。

## 2. 安装配置 {#installation-and-configuration}

> [!TIP]
>
> 源码安装环境为 Ubuntu 24.04(x86_64)，环境中已经安装了IvorySQL5及以上版本，安装路径为/usr/local/ivorysql/ivorysql-5

### 2.1. 源码安装 {#source-installation}

```
# 拉取pg_cron源码
git clone https://github.com/citusdata/pg_cron.git
cd pg_cron
# 将pg_config的路径设置到PATH环境变量里，eg：
export PATH=/usr/local/ivorysql/ivorysql-5/bin/:$PATH
make
make install
```

### 2.2. 配置文件 (ivorysql.conf) {#configuration-file-ivorysql-conf}

```
# 共享预加载扩展
shared_preload_libraries = 'pg_cron'

# 指定任务元数据存储库（默认当前库）
cron.database_name = 'ivorysql'

# 允许的最大并发任务数
cron.max_running_jobs = 5
```

### 2.3. 重启服务 {#restart-service}

```
pg_ctl restart -D ./data -l logfile
```

### 2.4. 创建Extension并确认pg_cron版本 {#create-extension-and-confirm-pg_cron-version}

psql 连接到数据库，执行如下命令：

```
ivorysql=# CREATE extension pg_cron;
CREATE EXTENSION

ivorysql=# SELECT * FROM pg_available_extensions WHERE name = 'pg_cron';
   name  | default_version | installed_version |         comment
---------+-----------------+-------------------+---------------------------
 pg_cron | 1.6             |                   |Job scheduler for PostgreSQL
(1 row)
```

## 3. 核心功能使用 {#core-functionality-usage}

### 3.1. 创建定时任务 {#creating-scheduled-tasks}

```
SELECT cron.schedule(
    'nightly-data-cleanup',        -- 任务名称（唯一标识）
    '0 3 * * *',                   -- cron表达式（每天UTC 3:00）
    $$DELETE FROM logs
      WHERE created_at < now() - interval '30 days'$$  -- 执行SQL
);
```

cron表达式速查表：

|                     |                    |
|---------------------|--------------------|
| 示例                | 含义               |
| '0 \* \* \* \*'     | 每小时整点执行     |
| '\*/15 \* \* \* \*' | 每15分钟执行       |
| '0 9 \* \* 1-5'     | 工作日早9点执行    |
| '0 1 1 \* \*'       | 每月1日凌晨1点执行 |

pg_cron还允许使用 '\$'表示月份的最后一天。

### 3.2. 任务管理 {#task-management}

```
# 查看所有任务
SELECT * FROM cron.job;
```

![p31](/ivorysql/assets/images/upstream/f1e7ed6982ac72fd4ba945ad8be0245fe3cae0ad89bdb588d7f00631e7c0579e.png)

```
# 查看任务执行历史
SELECT * FROM cron.job_run_details ORDER BY start_time DESC LIMIT 10;
```

![p32](/ivorysql/assets/images/upstream/3859c53deb367ed120bf122be3c2fc7fbc8142db7738a77c56b03bcc0b5fe0a4.png)

```
# 删除任务
SELECT cron.unschedule('nightly-data-cleanup');

# 暂停任务（更新状态）
UPDATE cron.job SET active = false WHERE jobname = 'delete-job-run-details';
```
