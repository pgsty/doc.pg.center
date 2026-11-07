---
title: 验证 pg_tde 加密
linkTitle: 验证加密
description: 创建加密表、检查加密状态，并将现有表转换为 tde_heap。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/test.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 240
upstream_source: percona
---

为数据库启用 `pg_tde` 扩展后，就可以使用 `tde_heap` 表访问方法加密数据。

## 加密新表中的数据 {#encrypt-data-in-a-new-table}

1. 在[已启用 `pg_tde`](/zh/percona/setup/) 的数据库中，使用 `tde_heap` 访问方法创建表：

    ```sql
    CREATE TABLE <table_name> (<field> <datatype>) USING tde_heap;
    ```

    **警告：以下示例仅用于测试。**

    ```sql
    CREATE TABLE albums (
        album_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        artist_id INTEGER,
        title TEXT NOT NULL,
        released DATE NOT NULL
    ) USING tde_heap;
    ```

    关于表访问方法以及如何默认启用数据加密，详见[表访问方法与 pg_tde](/zh/percona/index/table-access-method/)。

2. 要检查数据是否已加密，运行以下函数：

    ```sql
    SELECT pg_tde_is_encrypted('table_name');
    ```

    该函数返回 `true` 或 `false`。

3.（可选）轮换主密钥。

要使用新密钥重新加密数据，详见[主密钥管理](/zh/percona/functions/#principal-key-management)。

## 加密现有表 {#encrypt-existing-table}

可以加密现有表。该操作需要重写表，因此处理大表可能需要相当长的时间。

运行以下命令：

```sql
ALTER TABLE table_name SET ACCESS METHOD tde_heap;
```

> [!IMPORTANT]
> `SET ACCESS METHOD` 会丢弃提示位，可能影响查询性能。要恢复性能，请运行：
>
> ```sql
> SELECT count(*) FROM table_name;
> ```
>
> 这会强制 PostgreSQL 检查每个元组的可见性并重新设置提示位。

> [!TIP]
> 以后需要移除加密时，参阅[解密数据](/zh/percona/how-to/decrypt/)。

## 下一步 {#next-steps}

[配置 WAL 加密](/zh/percona/wal-encryption/)
