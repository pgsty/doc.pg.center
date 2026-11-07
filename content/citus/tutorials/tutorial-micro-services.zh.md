---
title: Citus 微服务教程
description: 使用 Citus 作为多个微服务的存储后端，部署并运维示例集群。
weight: 40
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/tutorial-micro-services?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
---

本教程使用 Citus 作为多个微服务的存储后端，演示一个示例集群的设置与基本操作。

> [!NOTE]
> 本教程假定 Citus 已安装并运行。如果尚未运行，可按[快速入门](/citus/installation/getting-started/)中的任一方案在本地部署。

## 分布式模式 {#distributed-schemas}

分布式模式可以在 Citus 集群内移动。系统可将它们作为整体在可用节点之间再平衡，从而无需手动分配即可高效共享资源。

微服务按设计拥有自己的存储层。我们不假定它们创建和保存哪种表或数据，而是为每项服务提供一个模式，并假定它们使用独立的 ROLE 连接数据库。用户连接时，其角色名会放在 `search_path` 开头；如果角色名与模式名相同，应用无需修改即可使用正确的 `search_path`。

示例使用三项服务：

- user 服务
- time 服务
- ping 服务

首先使用 psql 连接 Citus 协调节点。

**使用[快速入门](/citus/installation/getting-started/)中安装的原生 PostgreSQL 时**，协调节点运行在 9700 端口。

> [!NOTE] 示例端口
> 上游示例使用本地协调节点的 **9700** 端口，而软件包安装指南使用 PostgreSQL 默认的 **5432** 端口。请连接自己协调节点配置的端口；以下命令保留上游示例端口。

```bash
psql -p 9700
```

**使用 Docker 时**，可通过 `docker exec` 运行 psql 连接：

```bash
docker exec -it citus psql -U postgres
```

为各项服务创建数据库角色：

```sql
CREATE USER user_service;
CREATE USER time_service;
CREATE USER ping_service;
```

在 Citus 中可以通过两种方式分布模式：

手动调用 `citus_schema_distribute(schema_name)` 函数：

```sql
CREATE SCHEMA AUTHORIZATION user_service;
CREATE SCHEMA AUTHORIZATION time_service;
CREATE SCHEMA AUTHORIZATION ping_service;

SELECT citus_schema_distribute('user_service');
SELECT citus_schema_distribute('time_service');
SELECT citus_schema_distribute('ping_service');
```

该方法也可以将已有的普通模式转换为分布式模式。

> [!NOTE]
> 只能分布不包含分布式表和参考表的模式。

也可以启用配置参数 `citus.enable_schema_based_sharding`：

```sql
SET citus.enable_schema_based_sharding TO ON;

CREATE SCHEMA AUTHORIZATION user_service;
CREATE SCHEMA AUTHORIZATION time_service;
CREATE SCHEMA AUTHORIZATION ping_service;
```

可以在当前会话中修改该参数，也可以永久写入 postgresql.conf。将参数设为 ON 后，新创建的模式默认都会被分布。

列出当前已分布的模式：

```sql
select * from citus_schemas;
```

```text
schema_name  | colocation_id | schema_size | schema_owner
--------------+---------------+-------------+--------------
user_service |             5 | 0 bytes     | user_service
time_service |             6 | 0 bytes     | time_service
ping_service |             7 | 0 bytes     | ping_service
(3 rows)
```

## 创建表 {#creating-tables}

需要为每个微服务连接 Citus 协调节点。使用 `\c` 命令可在同一 psql 会话中切换用户。

```psql
\c citus user_service
```

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);
```

```psql
\c citus time_service
```

```sql
CREATE TABLE query_details (
    id SERIAL PRIMARY KEY,
    ip_address INET NOT NULL,
    query_time TIMESTAMP NOT NULL
);
```

```psql
\c citus ping_service
```

```sql
CREATE TABLE ping_results (
    id SERIAL PRIMARY KEY,
    host VARCHAR(255) NOT NULL,
    result TEXT NOT NULL
);
```

## 配置服务 {#configure-services}

本教程使用的服务可从以下公开仓库克隆：

`git clone https://github.com/citusdata/citus-example-microservices.git`。该仓库包含 ping、time 和 user 服务，每个服务都有一个要运行的 app.py。

```python

$ tree
    .
    ├── LICENSE
    ├── README.md
    ├── ping
    │   ├── app.py
    │   ├── ping.sql
    │   └── requirements.txt
    ├── time
    │   ├── app.py
    │   ├── requirements.txt
    │   └── time.sql
    └── user
        ├── app.py
        ├── requirements.txt
        └── user.sql
```

运行服务前，编辑 user/app.py、ping/app.py 和 time/app.py，为 Citus 集群填写[连接配置](https://www.psycopg.org/docs/module.html#psycopg2.connect)：

```python

# Database configuration

db_config = {
    'host': 'localhost',
    'database': 'citus',
    'user': 'ping_service',
    'port': 9700
}
```

保存所有修改后的文件，再进入下一步运行服务。

## 运行服务 {#running-the-services}

进入每个应用目录，在各自的 Python 环境中运行应用。

```bash

cd user
pipenv install
pipenv shell
python app.py
```

对 time 和 ping 服务重复上述步骤。完成后即可使用 API。

创建一些用户：

```bash

curl -X POST -H "Content-Type: application/json" -d '[
  {"name": "John Doe", "email": "john@example.com"},
  {"name": "Jane Smith", "email": "jane@example.com"},
  {"name": "Mike Johnson", "email": "mike@example.com"},
  {"name": "Emily Davis", "email": "emily@example.com"},
  {"name": "David Wilson", "email": "david@example.com"},
  {"name": "Sarah Thompson", "email": "sarah@example.com"},
  {"name": "Alex Miller", "email": "alex@example.com"},
  {"name": "Olivia Anderson", "email": "olivia@example.com"},
  {"name": "Daniel Martin", "email": "daniel@example.com"},
  {"name": "Sophia White", "email": "sophia@example.com"}
]' http://localhost:5000/users
```

列出已创建的用户：

```bash

curl http://localhost:5000/users
```

获取当前时间：

```bash

curl http://localhost:5001/current_time
```

对 example.com 执行 ping：

```bash

curl -X POST -H "Content-Type: application/json" -d '{"host": "example.com"}' http://localhost:5002/ping
```

## 探索数据库 {#exploring-the-database}

调用一些 API 函数后，系统会保存数据。可以检查 `citus_schemas` 表，确认结果是否符合预期：

```sql

select * from citus_schemas;
```

```text

schema_name | colocation_id | schema_size | schema_owner
--------------+---------------+-------------+--------------
user_service |             1 | 112 kB      | user_service
time_service |             2 | 32 kB       | time_service
ping_service |             3 | 32 kB       | ping_service
(3 rows)
```

创建模式时不需要指定使用哪些机器，Citus 会自动选择。以下查询可以查看每个模式所在的位置：

```sql

select nodename,nodeport, table_name, pg_size_pretty(sum(shard_size))
  from citus_shards
group by nodename,nodeport, table_name;
```

```text

nodename | nodeport |         table_name         | pg_size_pretty
-----------+----------+----------------------------+----------------
localhost |     9701 | time_service.query_details | 32 kB
localhost |     9702 | user_service.users         | 112 kB
localhost |     9702 | ping_service.ping_results | 32 kB
```

在示例中，time 服务位于 localhost:9701，user 与 ping 服务共享第二个工作节点 localhost:9702。这只是一个演示；数据量很小。假设节点间存储利用率不均衡，可将较小的 time 和 ping 服务放到同一台机器，把较大的 user 服务单独放置。

可以要求 Citus 按磁盘大小重新平衡集群：

```sql

select citus_rebalance_start();
```

```text

NOTICE: Scheduled 1 moves as job 1
DETAIL: Rebalance scheduled as background job
HINT: To monitor progress, run: SELECT * FROM citus_rebalance_status();
citus_rebalance_start
-----------------------
                     1
(1 row)
```

操作完成后，查看新的布局：

```sql

select nodename,nodeport, table_name, pg_size_pretty(sum(shard_size))
  from citus_shards
group by nodename,nodeport, table_name;
```

```text

nodename | nodeport |         table_name         | pg_size_pretty
-----------+----------+----------------------------+----------------
localhost |     9701 | time_service.query_details | 32 kB
localhost |     9701 | ping_service.ping_results | 32 kB
localhost |     9702 | user_service.users         | 112 kB
(3 rows)
```

模式已按预期移动，集群更加均衡。该操作对应用透明，无须重启应用，服务可以继续处理查询。

完成本教程后，你已经掌握了使用 Citus 为微服务提供存储的基本流程。

## 相关内容 {#related-content}

- [多租户应用教程](/citus/tutorials/tutorial-multi-tenant/)
- [什么是 Citus？](/citus/overview/what-is-citus/)
