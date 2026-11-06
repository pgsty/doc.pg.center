---
title: "搭建 Cloudberry 演示集群"
description: "本步骤介绍如何搭建 Cloudberry 演示集群并测试基本功能。"
weight: 80
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/build/set-demo-cluster.md"
---

演示集群由一个 Coordinator、一个 Standby Coordinator，以及多个主 Segment 和镜像 Segment 组成，所有组件均运行在同一台开发主机上。

## 设置初始容器（并非所有环境都需要） {#set-up-initial-container-not-required-for-all-environments}

容器环境通常不会默认启动 SSH 守护进程。由于 Cloudberry 高度依赖 SSH 进行进程间通信，因此需要初始化并启动 SSH 服务器：

```bash
if ! pgrep sshd > /dev/null; then
    echo "SSH daemon not running. Starting it now..."
    sudo ssh-keygen -A
    echo "PasswordAuthentication yes" | sudo tee -a /etc/ssh/sshd_config
    sudo /usr/sbin/sshd
else
    echo "SSH daemon is already running"
fi
```

## 为 Cloudberry 配置 SSH {#configure-ssh-for-cloudberry}

Cloudberry 使用 SSH 进行 Coordinator 与 Segment 之间的通信。以下命令会将主机加入 known_hosts 并验证 SSH 连接，以确保 gpadmin 用户的 SSH 配置正确：

```bash
ssh-keyscan $(hostname) >> ~/.ssh/known_hosts
ssh $(hostname) date
```

## 设置 Cloudberry 环境变量 {#set-up-cloudberry-environment-variables}

> [!WARNING] 警告
> 请注意，自 Cloudberry 2.1.0 起，`greenplum_path.sh` 已更名为 `cloudberry-env.sh`。有关此变更的更多信息，请参阅这篇[博客文章](https://cloudberry.apache.org/blog/from-greenplum-path.sh-to-cloudberry-env.sh)。

加载 Cloudberry 环境变量，为二进制文件、库和其他必要组件设置路径：

```bash
# For Apache Cloudberry 2.1.0+
source /usr/local/cloudberry-db/cloudberry-env.sh

# For Apache Cloudberry 2.0.0
source /usr/local/cloudberry-db/greenplum_path.sh
```

## 创建开发集群 {#create-development-cluster}

创建一个在单台机器上模拟完整 Cloudberry 部署的演示集群，其中包含 1 个 Coordinator、1 个 Standby Coordinator、3 个主 Segment 和 3 个镜像 Segment：

```bash
make create-demo-cluster --directory=~/cloudberry
```

演示集群中，Coordinator、Standby Coordinator 和 Segment 的端口如下：

```
    COORDINATOR PORT (PGPORT). : 7000
    STANDBY PORT ............. : 7001
    SEGMENT PORTS ............ : 7002 7003 7004 7005 7006 7007
```

## 配置集群环境 {#configure-cluster-environment}

创建集群后，验证并加载指向 Coordinator 端口和数据目录的集群专用变量：

```bash
source ~/cloudberry/gpAux/gpdemo/gpdemo-env.sh
```

## 验证集群部署 {#validate-cluster-deployment}

使用以下基本命令验证集群是否正常运行：

```bash
# Displays detailed cluster state including segment status
gpstate

# Tests cluster shutdown and startup
gpstop -a
gpstart -a

# Confirms Cloudberry version and build
psql template1 -c 'SELECT version()'

# Views segment configuration showing primary/mirror relationships
psql template1 -c 'SELECT * from gp_segment_configuration'

# Checks available PostgreSQL extensions
psql template1 -c 'SELECT * FROM pg_available_extensions'
```

## 连接默认的 `postgres` 数据库 {#connect-to-the-default-postgres-database}

使用以下命令连接默认的 `postgres` 数据库：

```bash
psql -p 7000 postgres
```

或者：

```bash
psql postgres
```

输出类似如下：

```bash
[gpadmin@cdw cloudberry]$ psql -p 7000 postgres
psql (14.4, server 14.4)
Type "help" for help.

postgres=# select version();
                                                                                                             version
------------------------------------------------------------------------------------------------------------------------
 PostgreSQL 14.4 (Apache Cloudberry 2.0.0-devel+dev.1959.g94a81765e6 build dev) on x86_64-pc-linux-gnu, compiled by gcc (GCC
) 11.5.0 20240719 (Red Hat 11.5.0-5), 64-bit compiled on May 28 2025 19:57:16 (with assert checking)
(1 row)

postgres=# \q
```

## 扩展测试示例：pg_stat_statements {#extension-testing-example-pg_stat_statements}

本示例演示如何启用并测试 `pg_stat_statements` 扩展。该扩展提供 SQL 查询执行统计信息：

```bash
# Creates a database for testing
createdb gpadmin

# Enables the extension by adding it to shared libraries
echo "shared_preload_libraries='pg_stat_statements'" >> $COORDINATOR_DATA_DIRECTORY/postgresql.conf

# Restarts cluster to load the new library (-r flag means "restart")
gpstop -ar

# Creates the extension in the database
psql gpadmin -e -c 'CREATE EXTENSION pg_stat_statements'

# Runs test queries to generate statistics
psql gpadmin --echo-queries <<EOF
-- Create a sample table
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary NUMERIC
);

-- Insert sample data
INSERT INTO employees (name, department, salary)
VALUES
('Alice', 'HR', 60000),
('Bob', 'Engineering', 80000),
('Charlie', 'Marketing', 70000);

-- Query the data to generate some statistics
SELECT * FROM employees WHERE department = 'Engineering';
SELECT AVG(salary) FROM employees;

-- View most frequently called queries
SELECT query, calls, total_exec_time AS total_time, rows
FROM pg_stat_statements
ORDER BY calls DESC
LIMIT 5;

-- View most time-consuming queries
SELECT query, calls, total_exec_time AS total_time, rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 5;
EOF
```

## 删除开发集群 {#destroy-development-cluster}

如需清理环境并重新开始，可以删除演示集群：

```bash
make destroy-demo-cluster --directory=~/cloudberry
```

此命令会删除所有集群数据和配置，以便在需要时创建全新的集群。

## 排查 SSH 连接问题 {#troubleshoot-ssh-connection-issues}

运行 `create-demo-cluster` 时，如果尚未完成 SSH 主机验证，进程可能会挂起。通常表现为进程停滞，等待用户确认主机身份。

因此，需要在创建集群前运行：

```bash
ssh-keyscan $(hostname) >> ~/.ssh/known_hosts
```
此命令会自动将主机的 SSH 密钥加入 known_hosts 文件，避免在创建集群时出现交互式提示。

如果仍然遇到 SSH 问题：

1. 确认 SSH 守护进程正在运行。
2. 检查 known_hosts 文件是否存在且权限正确。
3. 在继续创建集群前，使用 `ssh $(hostname) date` 测试 SSH 连接。
