---
title: CentOS 或 Red Hat 上的多节点 Citus 集群
description: 使用 RPM 软件包部署多节点 Citus，构建分布式 PostgreSQL 集群。
weight: 80
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/multi-node-fedora-centos-rhel?view=citus-14
upstream_ref: citus-14; 8445a2831f01
translation_status: translated
---

本节介绍如何使用 RPM 软件包，在自己的 Linux 主机上部署多节点 Citus 集群。

## 配置所有节点 {#configure-all-nodes}

### 1. 添加软件仓库 {#1-add-repository}

```bash
# Add Citus repository for package manager
curl https://install.citusdata.com/community/rpm.sh | sudo bash
```

### 2. 安装 PostgreSQL 与 Citus，初始化数据库 {#2-install-postgresql--citus-and-initialize-a-database}

```bash
# install PostgreSQL with Citus extension
sudo yum install -y citus140_18
# initialize system database
sudo /usr/pgsql-18/bin/postgresql-18-setup initdb
# preload citus extension
echo "shared_preload_libraries = 'citus'" | sudo tee -a /var/lib/pgsql/18/data/postgresql.conf
```

PostgreSQL 将特定版本的可执行文件放在 `/usr/pgsql-18/bin` 中，通常直接使用 `psql` 即可。最新版本会加入命令搜索路径；服务器本身可通过 *service* 命令管理。

### 3. 配置连接与认证 {#3-configure-connection-and-authentication}

启动数据库前，先调整访问权限。默认情况下，数据库服务器仅接受来自 localhost 的客户端连接。这里将其配置为监听所有 IP 接口，再修改客户端认证文件，允许本地网络中的连接。

```bash
sudo vi /var/lib/pgsql/18/data/postgresql.conf
```

```bash
# Uncomment listen_addresses for the changes to take effect
listen_addresses = '*'
```

```bash
sudo vi /var/lib/pgsql/18/data/pg_hba.conf
```

```bash
# Allow unrestricted access to nodes in the local network. The following ranges
# correspond to 24, 20, and 16-bit blocks in Private IPv4 address spaces.
host    all             all             10.0.0.0/8              trust

# Also allow the host unrestricted access to connect to itself
host    all             all             127.0.0.1/32            trust
host    all             all             ::1/128                 trust
```

> [!NOTE]
> 你的 DNS 配置可能有所不同。此外，这些访问设置对某些环境来说过于宽松。详情见[加强工作节点安全](/citus/operations/cluster-management/#increasing-worker-security)；PostgreSQL 手册也[介绍了如何](http://www.postgresql.org/docs/current/static/auth-pg-hba-conf.html)收紧访问控制。

### 4. 启动数据库服务器并创建 Citus 扩展 {#4-start-database-servers-create-citus-extension}

```bash
# start the db server
sudo service postgresql-18 restart
# and make it start automatically when computer does
sudo chkconfig postgresql-18 on
```

需要在集群中使用的**每个数据库**中创建 Citus 扩展。以下示例将扩展添加到名为 `postgres` 的默认数据库。

```bash
sudo -i -u postgres psql -c "CREATE EXTENSION citus;"
```

## 配置协调节点 {#configure-the-coordinator-node}

完成上述操作后，以下步骤**仅在协调节点上**执行。

### 1. 添加工作节点信息 {#1-add-worker-node-information}

让协调节点了解它的工作节点。调用用户定义函数（UDF），将节点信息加入 `pg_dist_node` 系统目录表；协调节点通过该表获取工作节点列表。假设有两个工作节点，分别名为 `worker-101` 和 `worker-102`，将其 DNS 名称（或 IP 地址）及服务端口加入表中。

```bash
# Register the hostname that future workers will use to connect
# to the coordinator node.
#
# You'll need to change the example, 'coord.example.com',
# to match the actual hostname

sudo -i -u postgres psql -c \
  "SELECT citus_set_coordinator_host('coord.example.com', 5432);"

# Add the worker nodes.
#
# Similarly, you'll need to change 'worker-101' and 'worker-102' to the
# actual hostnames

sudo -i -u postgres psql -c "SELECT * from citus_add_node('worker-101', 5432);"
sudo -i -u postgres psql -c "SELECT * from citus_add_node('worker-102', 5432);"
```

### 2. 验证安装 {#2-verify-that-installation-succeeded}

确认协调节点已读取预期的工作节点配置，即可验证安装是否成功。在 shell 中执行以下命令，应当列出刚加入 `pg_dist_node` 表的工作节点。

```bash
sudo -i -u postgres psql -c "SELECT * FROM citus_get_active_worker_nodes();"
```

## 开始使用 Citus {#ready-to-use-citus}

安装完成后即可使用 Citus 集群。以 `postgres` 用户通过 `psql` 访问新建的 Citus 数据库：

```bash
sudo -i -u postgres psql
```

## 相关内容 {#related-content}

- [多节点概览](/citus/installation/multi-node/)
