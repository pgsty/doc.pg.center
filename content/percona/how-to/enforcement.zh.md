---
title: 强制使用加密
linkTitle: 强制使用加密
description: 通过集群、数据库、用户和会话级设置控制 pg_tde 的强制加密。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/how-to/enforcement.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 530
upstream_source: percona
---

在 `pg_tde` 中，强制加密确保特定操作、表或整个数据库只允许使用加密存储。在出于合规、安全或策略要求必须加密的环境中，它可以防止意外创建未加密的表或索引。

## 强制加密的作用 {#what-does-enforcement-do}

启用后，强制加密会：

* 阻止创建未加密的表或索引。
* 确保不同租户、数据库或用户一致地使用加密。
* 支持全局、按数据库或按角色限定作用范围。

## 强制使用加密 {#enforce-encryption-usage}

可以通过以下方式强制安全使用 `pg_tde`。

### 1. 在整个服务器上强制加密 {#1-enforce-encryption-across-the-server}

要在集群范围强制加密，在 `postgresql.conf` 中设置 [`pg_tde.enforce_encryption`](/zh/percona/variables/#pgtde-enforceencryption)：

```ini
pg_tde.enforce_encryption = on
```

> [!NOTE]
> **只有**超级用户可以设置或修改此参数。

这确保包括超级用户在内的所有用户都不能创建未加密表。不过，超级用户可以显式[覆盖当前会话的参数值](#override-enforcement-for-trusted-sessions)。

### 2. 对特定数据库强制加密 {#2-enforce-encryption-for-a-specific-database}

要只在特定数据库内强制加密，运行：

```sql
ALTER DATABASE example_db SET pg_tde.enforce_encryption = on;
```

这确保**只有**连接到该数据库时才强制加密。

### 3. 对特定用户强制加密 {#3-enforce-encryption-for-a-specific-user}

也可以按用户强制加密：

```sql
ALTER USER example_user SET pg_tde.enforce_encryption = on;
```

这确保 `example_user` 无论连接到哪个数据库，都不能创建未加密表。

### 为可信会话覆盖强制加密设置 {#override-enforcement-for-trusted-sessions}

超级用户可以在会话级别覆盖该参数：

```sql
SET pg_tde.enforce_encryption = off;
```

这样可以在某些特殊情况下临时创建未加密表，例如：

* 加载可信的公开参考数据集。
* 基准测试和测试环境。
* 重新加密前的迁移暂存阶段。

> [!NOTE]
> 超级用户虽然可以在自己的会话中关闭强制加密，但必须显式执行。默认的强制设置仍然生效，以防止意外配置错误。
