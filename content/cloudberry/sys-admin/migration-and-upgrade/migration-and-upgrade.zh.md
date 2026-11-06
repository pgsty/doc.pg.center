---
title: "迁移与升级"
description: "使用 cbcopy 迁移 Greenplum 数据库，或将 Apache Cloudberry 数据库从 1.x 升级到 2.x。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/migration-and-upgrade/migration-and-upgrade.md"
---

本指南详细介绍两种场景：

1. 将 Greenplum Database 6.x/7.x 迁移到 Apache Cloudberry
2. 将 Apache Cloudberry 1.x（加入 Apache Incubator 前的非 Apache 发行版）升级到 Apache Cloudberry 2.x

这两种场景都使用 `cbcopy` 工具。cbcopy 是一个功能强大的数据迁移工具，用于高效地执行数据库迁移和升级操作。

## 前提条件 {#prerequisites}

开始迁移或升级前，请确保：

1. 已安装 Go 编程语言 1.19 或更高版本
2. 在源数据库和目标数据库上都具有超级用户权限
3. 源数据库集群与目标数据库集群之间具有网络连接
4. 源集群和目标集群都有足够的磁盘空间
5. 源数据库和目标数据库的所有节点上，`$GPHOME/bin` 目录中都安装了 `cbcopy` 和 `cbcopy_helper` 二进制文件

## 安装 cbcopy {#install-cbcopy}

1. 克隆代码仓库：
```bash
git clone https://github.com/cloudberry-contrib/cbcopy.git
```

2. 构建二进制文件：
```bash
cd cbcopy
make
```

3. 安装二进制文件：
```bash
make install
```

## 版本兼容性 {#version-compatibility}

### Cloudberry 升级（1.x 到 2.x） {#cloudberry-upgrade-1x-to-2x}
- 源：Cloudberry 1.6
- 目标：Cloudberry 2.0

### 从 Greenplum 迁移到 Cloudberry {#greenplum-to-cloudberry-migration}
- 源：Greenplum 6.x 或 7.x
- 目标：Cloudberry 1.x 或 2.x

## 迁移过程 {#migration-process}

迁移过程包含两个主要阶段：
1. 元数据迁移
2. 数据迁移

建议分别执行这两个阶段，以便更好地控制过程并提高可靠性：
1. 首先使用 `--metadata-only` 迁移元数据
2. 然后使用 `--data-only` 迁移数据

### 基本迁移命令 {#basic-migration-command}

```bash
cbcopy --source-host=<source_host> \
    --source-port=<source_port> \
    --source-user=<source_user> \
    --dest-host=<dest_host> \
    --dest-port=<dest_port> \
    --dest-user=<dest_user> \
    [additional_options]
```

### 迁移模式 {#migration-modes}

cbcopy 支持多种迁移模式：

1. **完整迁移**（`--full`）
   - 将源端的全部元数据和数据迁移到目标端

2. **数据库迁移**（`--dbname`）
   - 迁移指定的数据库
   ```bash
   cbcopy --dbname="database1,database2" [other_options]
   ```

3. **模式迁移**（`--schema`）
   - 迁移指定的模式
   ```bash
   cbcopy --schema="database.schema1,database.schema2" [other_options]
   ```

4. **表迁移**（`--include-table`）
   - 迁移指定的表
   ```bash
   cbcopy --include-table="database.schema.table1,database.schema.table2" [other_options]
   ```

### 数据加载选项 {#data-loading-options}

1. **追加模式**（`--append`）
   - 将迁移的记录插入现有表
   - 要保留现有数据时使用

2. **截断模式**（`--truncate`）
   - 插入迁移数据前清除现有记录
   - 要替换现有数据时使用
   ```bash
   cbcopy --truncate [other_options]
   ```

### 处理依赖关系 {#handle-dependencies}

#### 全局对象 {#global-objects}

对于依赖全局对象（例如表空间）的表：

1. 使用 `--with-global-metadata` 自动创建这些对象
2. 或在迁移前手动创建：
   ```sql
   CREATE TABLESPACE custom_tablespace LOCATION '/path/to/tablespace';
   ```

#### 角色管理 {#role-management}

要在迁移期间更改表所有者：

1. 在目标数据库中创建目标角色
2. 使用 `--owner-mapping-file` 指定角色映射：
   ```
   source_role1,target_role1
   source_role2,target_role2
   ```

### 表空间管理 {#tablespace-management}

处理表空间有三种选项：

1. **默认模式**
   - 使用与源端相同的表空间名称创建对象
   - 使用 `--with-global-metadata` 或手动创建表空间

2. **单个目标表空间**（`--dest-tablespace`）
   ```bash
   cbcopy --dest-tablespace=new_space [other_options]
   ```

3. **表空间映射**（`--tablespace-mapping-file`）
   ```
   source_tablespace1,target_tablespace1
   source_tablespace2,target_tablespace2
   ```

### 性能优化 {#performance-optimization}

1. **并行作业**
   - 使用 `--copy-jobs` 控制并发复制的表数量
   ```bash
   cbcopy --copy-jobs=8 [other_options]
   ```

2. **复制策略**

   cbcopy 会根据表大小自动选择最佳策略：

   - 在 Coordinator 上复制：适用于小表
   - 在 Segment 上复制：适用于集群配置匹配的大表
   - 在外部表上复制：适用于其他情况

### 迁移验证 {#migration-validation}

cbcopy 会通过比较源端和目标端的行数自动执行验证。失败的迁移会记录在：

- `$USER/gpAdminLogs/cbcopy_succeed_$timestamp`
- `$USER/gpAdminLogs/cbcopy_failed_$timestamp`

如需重试，请使用：
```bash
cbcopy --exclude-table-file=cbcopy_succeed_$timestamp [other_options]
```

## 示例场景 {#example-scenarios}

### 场景 1：Cloudberry 1.6 升级到 2.0 {#scenario-1-cloudberry-16-to-20-upgrade}

```bash
# Step 1: Migrate metadata
cbcopy --source-host=127.0.0.1 \
    --source-port=15432 \
    --source-user=gpadmin \
    --dest-host=127.0.0.1 \
    --dest-port=25432 \
    --dest-user=gpadmin \
    --full \
    --metadata-only

# Step 2: Migrate data
cbcopy --source-host=127.0.0.1 \
    --source-port=15432 \
    --source-user=gpadmin \
    --dest-host=127.0.0.1 \
    --dest-port=25432 \
    --dest-user=gpadmin \
    --full \
    --data-only \
    --truncate
```

### 场景 2：Greenplum 6.x/7.x 迁移到 Cloudberry 2.0 {#scenario-2-greenplum-6x7x-to-cloudberry-20-migration}

```bash
# Step 1: Migrate metadata with global objects
cbcopy --source-host=127.0.0.1 \
    --source-port=15432 \
    --source-user=gpadmin \
    --dest-host=127.0.0.1 \
    --dest-port=25432 \
    --dest-user=gpadmin \
    --full \
    --metadata-only \
    --with-global-metadata

# Step 2: Migrate data
cbcopy --source-host=127.0.0.1 \
    --source-port=15432 \
    --source-user=gpadmin \
    --dest-host=127.0.0.1 \
    --dest-port=25432 \
    --dest-user=gpadmin \
    --full \
    --data-only \
    --truncate \
    --copy-jobs=8
```

## 故障排除 {#troubleshooting}

1. **迁移失败**
   - 检查 `$USER/gpAdminLogs/cbcopy_$timestamp.log` 以获取详细错误信息
   - 使用成功/失败文件重试失败的迁移

2. **常见问题**
   - 确保目标数据库中存在所有必需的表空间
   - 验证两个数据库之间的网络连接
   - 检查两个数据库上的用户权限
   - 确保两个集群都有足够的磁盘空间

## 其他资源 {#additional-resources}

- [cbcopy GitHub 仓库](https://github.com/cloudberry-contrib/cbcopy)

> [!NOTE]
> cbcopy 由社区成员贡献；但是请注意，它目前还不是由 Cloudberry 官方项目维护的工具。
