---
title: 使用 tde_heap 的流复制
linkTitle: 流复制
description: 配置使用 tde_heap 的 PostgreSQL 主备流复制，并保持密钥提供商配置与路径一致。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/replication.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 520
upstream_source: percona
---

> [!NOTE] 本站勘误
> 创建密钥和设置服务器主密钥是两个独立操作。 详见[勘误记录](/zh/percona/site/errata/)。


本节介绍当主库启用了 `pg_tde` 扩展，尤其是 [`tde_heap`](/zh/percona/index/table-access-method/) 访问方法时，如何配置 PostgreSQL 流复制。

开始之前，请先完成 [`pg_tde` 配置步骤](/zh/percona/setup/)。

> [!NOTE]
> **不需要**在备库执行 `CREATE EXTENSION`，扩展会自动复制过去。

## 1. 配置主库 {#1-configure-the-primary}

### 创建主密钥 {#create-a-principal-key}

先使用 `pg_tde_create_key_using_global_key_provider` 在已配置的全局提供商上创建密钥，再通过 [`pg_tde_set_server_key_using_global_key_provider`](/zh/percona/functions/#pgtdesetserverkeyusingglobalkeyprovider) 将其设为服务器主密钥。

### 创建复制角色 {#create-the-replication-role}

在主库创建复制角色：

```sql
CREATE ROLE example_replicator WITH REPLICATION LOGIN PASSWORD 'example_password';
```

### 配置 pg_hba.conf {#configure-pghba-conf}

要允许副本连接主库，在 `pg_hba.conf` 中加入以下行：

```conf
host  replication  example_replicator  standby_ip/32  scram-sha-256
```

确保该行位于其他复制连接的 host 规则之前，然后**重新加载**配置：

```sql
SELECT pg_reload_conf();
```

## 2. 配置备库 {#2-configure-the-standby}

### 执行数据库备份 {#perform-a-database-backup}

从备库机器执行基础备份，拉取加密的基础备份：

```bash
export PGPASSWORD='example_password'
pg_tde_basebackup \
  -h primary_ip \
  -D /var/lib/pgsql/data \
  -U example_replicator \
  --wal-method=stream \
  --slot=tde_slot \
  -C \
  -c fast \
  -v -P
```

### 配置 postgresql.conf {#configure-postgresql-conf}

基础备份完成后，在备库的 `postgresql.conf` 中加入：

```ini
shared_preload_libraries = 'pg_tde'
```

## 3. 启动并验证复制 {#3-start-and-validate-replication}

假设主库和备库分别运行在不同主机上，启动 PostgreSQL 服务：

```bash
sudo systemctl start postgresql
```

> [!WARNING] 复制必须保持密钥管理一致
>
> 使用 Vault、KMIP 等 KMS 提供商时，确保主库和备库都能访问**相同的**密钥管理配置，并且配置文件在两个系统上的路径相同。
>
> 例如：
>
> - 如果为 Vault 配置的秘密文件路径为 `/path/to/secret.file`，主库和备库的相同路径下都**必须**存在该文件。
> - `keyring_file` 提供商将密钥材料保存在本地文件中，**并非为多服务器共享或并发使用而设计**，因此**不建议**用于复制环境。

* 在主库上：

```sql
SELECT client_addr, state FROM pg_stat_replication;
```

* 在备库上：

```sql
SELECT
    pg_is_in_recovery()          AS in_recovery,
    pg_last_wal_receive_lsn()    AS receive_lsn,
    pg_last_wal_replay_lsn()     AS replay_lsn;
```

> [!TIP]
> 要验证配置正常工作，在主库创建加密表后，可以在备库运行以下命令，确认加密已启用且密钥可以解析：
>
> ```sql
> SELECT pg_tde_is_encrypted('your_encrypted_table');
> ```
