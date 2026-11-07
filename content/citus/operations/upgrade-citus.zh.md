---
title: Citus 升级
description: 了解如何升级 PostgreSQL 集群上的 Citus 版本，包括次要更新的修补程序升级和主要版本升级。
weight: 60
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/upgrade-citus?view=citus-14
upstream_ref: citus-14; be6cf64ecd13
translation_status: translated
---

保持 Citus 扩展为最新版本，可获得最新功能、性能改进和缺陷修复。本指南介绍在 PostgreSQL 集群上升级 Citus 的过程，包括小幅更新所需的补丁版本升级，以及可能引入新功能的主版本升级。了解升级过程有助于维护安全、高效的分布式数据库环境，同时尽量减少停机时间并确保应用程序兼容性。

## 升级 Citus 版本 {#upgrade-citus-versions}

要升级 Citus，先获取新版扩展，再将其安装到每个数据库实例上。Citus 为每个次版本提供独立的软件包，因此默认的软件包升级只提供缺陷修复，不会引入破坏性变更。下面先介绍最简单的补丁版本升级。

### 补丁版本升级 {#patch-version-upgrade}

要将当前 Citus 版本升级到最新补丁版本，运行包管理器的标准升级命令即可。

假设版本 **14.0** 当前安装在 PostgreSQL **17** 上：

**Ubuntu 或 Debian**

```bash
sudo apt-get update
sudo apt-get install --only-upgrade postgresql-17-citus-14.0
sudo service postgresql restart
```

**Red Hat Enterprise Linux 或 CentOS**

```bash
sudo yum update citus140_17
sudo service postgresql-17 restart
```

### 主版本和次版本升级 {#major-and-minor-version-upgrades}

主版本和次版本升级的步骤相同，但需要注意：这些升级可能对 Citus API 引入不向后兼容的变更。升级前请查看 Citus [变更日志](https://github.com/citusdata/citus/blob/master/CHANGELOG.md)，检查是否存在可能影响应用程序的变更。

> [!IMPORTANT]
> 从 Citus 13.2 开始，重要功能可以回移到近期仍受支持的主版本。因此，应始终升级到目标主版本的最新次版本，以免丢失功能。例如，假设 Citus 20.1 引入的功能被回移到 Citus 18.3 和 19.5，而你要从 Citus 18.3 升级到 Citus 19。如果升级到 19.4 或更早版本，就会丢失该功能；应升级到 19.5 或更高版本。如果要升级到 Citus 20，则应升级到 20.1 或更高版本，而不是 20.0。
> 
> 总之，应始终升级到目标主版本的最新次版本，而不是较早的次版本。

Citus 的每个主版本和次版本都以独立名称的软件包发布。安装新版软件包时会自动删除旧版。

#### 步骤 1. 更新 Citus 包 {#step-1-update-citus-package}

如果 Citus 和 PostgreSQL 都需要升级，应先升级 Citus 扩展，再升级 PostgreSQL（参见 [PostgreSQL 17 → 18](#upgrade-postgresql-version-from-17-to-18)）。

以下是在 PostgreSQL **17** 上将 Citus 从 **13.2 升级到 14.0** 的步骤：

**Ubuntu 或 Debian**

```bash
sudo apt-get update
sudo apt-get install postgresql-17-citus-14.0
sudo service postgresql restart
```

**Red Hat**

```bash
# Red Hat Enterprise Linux or CentOS
sudo yum swap citus130_17 citus140_17
sudo service postgresql-17 restart
```

#### 步骤 2. 在数据库中应用更新 {#step-2-apply-update-in-database}

安装新包并重启数据库后，运行扩展升级脚本。

```sql
-- you must restart PostgreSQL before running this
ALTER EXTENSION citus UPDATE;

-- you should see the upgraded Citus version
SELECT * FROM citus_version();

-- Run this procedure during one of these upgrade paths:
--   * upgrading to Citus 11 or later while still on a pre-11 version, OR
--   * upgrading to Citus 14 or later while still on a pre-14 version.
-- Run it on the coordinator node.
CALL citus_finish_citus_upgrade();
```

> [!NOTE]
> - 如果从早期主版本升级到 Citus 14.x，`citus_finish_citus_upgrade()` 还会修复任何注册排序规则列与组中表的分布列不匹配的共置组。 这是一项仅涉及元数据的操作（不涉及数据移动），可在需要时更新所有节点上的`pg_dist_colocation` 和 `pg_dist_partition`。

在主版本升级期间，从 yum 安装新版软件包开始，直到服务器重启并执行 `ALTER EXTENSION` 为止，Citus 不会执行分布式查询。这项限制用于保护数据，因为 Citus 对象和函数定义与版本相关。通过 yum 安装后，应先重启，再运行 `ALTER EXTENSION`。极少数情况下，如果升级出错，可以通过 [`citus.enable_version_checks`](/citus/reference/api-guc/#citusenable_version_checks-boolean) 配置参数禁用此检查。也可以[联系我们](https://www.citusdata.com/about/contact_us)并提供错误信息，以便协助排查。

## 将 PostgreSQL 版本从 17 升级到 18 {#upgrade-postgresql-version-from-17-to-18}

在开始之前，请记录以下路径。 实际路径可能与此处列出的路径不同：

现有数据目录（例如 `/opt/pgsql/17/data`）：`export OLD_PG_DATA=/opt/pgsql/17/data`

现有的 PostgreSQL 安装路径（例如 `/usr/pgsql-17`） `export OLD_PG_PATH=/usr/pgsql-17`

升级后的新数据目录 `export NEW_PG_DATA=/opt/pgsql/18/data`

新的 PostgreSQL 安装路径 `export NEW_PG_PATH=/usr/pgsql-18`

然后按其他 PostgreSQL 升级相同的步骤操作：准备元数据；配置新实例，将 Citus 加入 shared_preload_libraries；停止旧服务器；运行 pg_upgrade；如果 `postgresql.auto.conf`、`server.crt` 和 `server.key` 由 Citus 生成，则复制这些文件；启动新服务器；运行 `citus_finish_pg_upgrade()`。

> [!NOTE]
> 不要尝试 *同时升级* Citus 和 PostgreSQL 版本。 如果要升级这两者，请先升级 Citus。

### 对于每个节点 {#for-every-node}

按照以下步骤，在每个节点（协调节点和工作节点）上升级运行 Citus 的 PostgreSQL：

1. 备份 Citus 元数据。

   ```sql
   -- run this on the coordinator and worker nodes
   
   SELECT citus_prepare_pg_upgrade();
   ```
2. 将新数据库实例配置为使用 Citus。

   - 在 `postgresql.conf` 中将 Citus 加入共享预加载库。

     ```ini
     shared_preload_libraries = 'citus'
     ```
   - **请勿创建** Citus 扩展。
   - **请勿** 启动新服务器。
3. 停止旧服务器。
4. 检查升级兼容性。

   ```bash
   $NEW_PG_PATH/bin/pg_upgrade -b $OLD_PG_PATH/bin/ -B $NEW_PG_PATH/bin/ \
                               -d $OLD_PG_DATA -D $NEW_PG_DATA --check
   ```

   应看到 “Clusters are compatible” 消息。如果没有，请先修复错误再继续。确保：

   - `NEW_PG_DATA` 包含由新的 PostgreSQL 版本初始化的空数据库
   - Citus 扩展**未**创建
5. 执行升级（与之前类似，但不含 `--check` 选项）。

   ```bash
   $NEW_PG_PATH/bin/pg_upgrade -b $OLD_PG_PATH/bin/ -B $NEW_PG_PATH/bin/ \
   -d $OLD_PG_DATA -D $NEW_PG_DATA
   ```
6. 如果没有自行设置传输层安全（TLS）配置，Citus 会代为配置。此时需要复制 Citus 生成的 `postgresql.auto.conf` 文件以及证书文件（`server.crt` 和 `server.key`）。

   ```bash
   cp $OLD_PG_DATA/postgresql.auto.conf $NEW_PG_DATA/
   cp $OLD_PG_DATA/server.crt $NEW_PG_DATA/
   cp $OLD_PG_DATA/server.key $NEW_PG_DATA/
   ```
7. 启动新服务器。
8. 在运行下一步给出的查询之前，**不要**运行任何查询。
9. 在新的协调节点上恢复元数据。

   ```sql
   -- run this on the coordinator and worker nodes
   
   SELECT citus_finish_pg_upgrade();
   ```

## 相关内容 {#related-content}

- [Citus 中的集群管理](/citus/operations/cluster-management/)
- [Citus 表管理](/citus/operations/table-management/)
- [Citus 的诊断查询](/citus/operations/diagnostic-queries/)
- [什么是 Citus？](/citus/overview/what-is-citus/)
