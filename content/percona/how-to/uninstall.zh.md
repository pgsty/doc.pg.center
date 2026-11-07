---
title: 卸载 pg_tde
linkTitle: 卸载 pg_tde
description: 先解密表并关闭 WAL 加密，再分两次重启移除 pg_tde 共享库和配置。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/how-to/uninstall.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 590
upstream_source: percona
---

如果部署中不再需要透明数据加密（TDE），可以移除 `pg_tde` 扩展。

继续操作需要以下任一权限：

- 超级用户权限（全局移除扩展），或
- 数据库所有者权限（仅从特定数据库移除）。

按照以下步骤卸载 `pg_tde`。

## 第一步：从所有数据库移除 pg_tde {#step-1-remove-pgtde-from-all-databases}

卸载之前，必须从每个加载了扩展的数据库中移除它。如果在模板中安装了 `pg_tde`，新数据库会继承它。必须先从模板中删除，否则后续恢复或创建数据库会出问题。

a. 重写加密表。

将加密表重写回默认存储方法：

```sql
ALTER TABLE <table_name> SET ACCESS METHOD heap;
```

b. 全部加密表都已重写或删除后，再移除扩展：

```sql
DROP EXTENSION pg_tde;
```

> [!NOTE]
> 如果还有未解密或删除的加密对象，该命令会失败。需要先对这些对象执行上述步骤。
>
> 对集群中的每个数据库重复第一步。

## 第二步：关闭 WAL 加密 {#step-2-turn-off-wal-encryption}

如果使用了 WAL 加密，必须在卸载 `pg_tde` 库之前**关闭它**。

a. 运行：

```sql
ALTER SYSTEM SET pg_tde.wal_encrypt = off;
```

b. 重启 PostgreSQL 集群，使更改生效：

- Debian 和 Ubuntu：

```sh
sudo systemctl restart postgresql
```

- RHEL 及衍生发行版：

```sh
sudo systemctl restart postgresql-(pg-version)
```

## 第三步：卸载 pg_tde 共享库 {#step-3-uninstall-the-pgtde-shared-library}

> [!WARNING]
> 此过程会移除扩展，但**不会**自动解密数据。只有所有加密数据**已移除或解密**，且 WAL 加密**已关闭**后，才能卸载共享库。

> [!NOTE]
> 已加密的 WAL 页面**不会被解密**。任何需要读取它们的 PostgreSQL 集群，仍需加载 `pg_tde` 库，并确保 WAL 加密密钥可用且正在使用。

此时，共享库仍已加载，但不再活动。要完整卸载 `pg_tde`，继续以下步骤。

a. 执行 `SHOW shared_preload_libraries` 查看当前预加载库配置。

例如：

```sql
postgres=# SHOW shared_preload_libraries;
        shared_preload_libraries
-----------------------------------------
pg_stat_statements,pg_tde,auto_explain
(1 row)

postgres=#
```

b. 从列表中移除 `pg_tde`，通过 `ALTER SYSTEM SET shared_preload_libraries=<your list of libraries>` 应用新设置。

例如：

```sql
postgres=# ALTER SYSTEM SET shared_preload_libraries=pg_stat_statements,auto_explain;
ALTER SYSTEM
postgres=#
```

> [!NOTE]
> 实际库列表很可能与上述示例不同。不要移除其他必需扩展，只删除 `pg_tde`。
>
> 如果列表中只有 `pg_tde`，且它通过 `postgresql.conf` 设置，就不能使用 `ALTER SYSTEM SET ...` 关闭它。应当：
>
> 1. 从 `postgresql.conf` 删除 `shared_preload_libraries` 行。
> 2. 执行 `ALTER SYSTEM RESET shared_preload_libraries;`。

c. 重启 `postgresql` 集群，使更改生效：

- Debian 和 Ubuntu：

    ```sh
    sudo systemctl restart postgresql
    ```

- RHEL 及衍生发行版：

    ```sh
    sudo systemctl restart postgresql-(pg-version)
    ```

    > [!NOTE]
    > 服务名称可能随发行版和 PostgreSQL 版本而不同。

## 第四步：（可选但建议）清理配置 {#step-4-optional-but-recommended-clean-up-configuration}

现在可以安全地从 `postgresql.conf` 和 `postgresql.auto.conf` 中移除 `pg_tde` 相关配置。查找以 `pg_tde.` 开头的参数，按需删除或注释。

## 排查：重启时出现 PANIC，找不到检查点 {#troubleshooting-panic-checkpoint-not-found-on-restart}

如果从 `shared_preload_libraries` 移除 `pg_tde` 之前没有正确关闭 WAL 加密，或关闭 WAL 加密后未重启 PostgreSQL（见第三步 c），就可能出现此问题。

重启集群时可能看到：

```ini
2025-04-01 17:12:50.607 CEST [496385] PANIC:  could not locate a valid checkpoint record at 0/17B2580
```

此错误意味着 PostgreSQL 正在尝试读取加密 WAL，但没有加载 `pg_tde`。

解决步骤：

1. 将 `pg_tde` 重新加入 `shared_preload_libraries`。
2. 重启 PostgreSQL 集群。
3. 按照[关闭 WAL 加密的说明](#step-2-turn-off-wal-encryption)操作，再次卸载共享库。

> [!NOTE]
> 如果此前启用了 WAL 加密，正确卸载需要重启两次：
>
> - 第一次用于关闭 WAL 加密。
> - 第二次用于移除 `pg_tde` 库。
