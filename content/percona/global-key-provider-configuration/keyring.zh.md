---
title: keyring 文件配置
linkTitle: 本地 keyring
description: 使用本地明文 keyring 文件配置数据库密钥，适用于开发和测试。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/global-key-provider-configuration/keyring.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 320
upstream_source: percona
---

> [!NOTE] 本站勘误
> 检查命令已改为示例实际创建的表，并使用当前数据库的密钥信息函数。 详见[勘误记录](/zh/percona/site/errata/)。


此配置面向开发环境，将密钥以未加密形式保存在指定的数据文件中。

> [!NOTE]
> **本地**或**测试环境**可以使用 keyring 文件，但生产部署建议使用合适的 [KMS 提供商](/zh/percona/global-key-provider-configuration/overview/)。

密钥提供商可以配置在数据库级别（用于开发和测试），也可以配置在全局级别（用于生产）。

以下示例演示如何添加[数据库作用域的密钥提供商](/zh/percona/functions/#add-or-modify-local-key-file-providers)：

1. 创建数据库作用域的文件密钥提供商（本例为 `file-keyring`），将密钥保存在 `/tmp/pg_tde_test_local_keyring.per` 中：

    ```sql
    SELECT pg_tde_add_database_key_provider_file(
        'file-keyring',
        '/tmp/pg_tde_test_local_keyring.per'
    );
    ```

2. 在新建的 `file-keyring` 提供商中创建密钥（本例为 `my_default_key`）：

    ```sql
    SELECT pg_tde_create_key_using_database_key_provider(
        'my_default_key',
        'file-keyring'
    );
    ```

3. 将密钥提供商（`file-keyring`）中的密钥（`my_default_key`）设为当前密钥：

    ```sql
    SELECT pg_tde_set_key_using_database_key_provider(
        'my_default_key',
        'file-keyring'
    );
    ```

    > [!TIP]
    > 可以查询当前数据库主密钥的信息，例如创建日期和时间。运行：
    >
    > ```sql
    > SELECT pg_tde_key_info();
    > ```

4. 使用 [tde_heap](/zh/percona/index/table-access-method/#how-tdeheap-works-with-pgtde) 创建表：

    ```sql
    CREATE TABLE customer_table (a INT) USING tde_heap;
    ```

    新建的表会使用你设置的数据库主密钥（`my_default_key`）加密。

    > [!TIP]
    > 要检查创建的表是否使用 tde_heap 加密，请运行：
    >
    > ```sql
    > \d+ customer_table
    > ```
    >
    > 如果显示 `Access method: tde_heap`，说明表已加密。
    >
    > > [!DETAILS] 输出示例
    > >         postgres=# \d+ customer_table
    > >                                             Table "public.customer_table"
    > >         Column |  Type   | Collation | Nullable | Default | Storage | Compression | Stats target | Description
    > >         --------+---------+-----------+----------+---------+---------+-------------+--------------+-------------
    > >         a      | integer |           |          |         | plain   |             |              |
    > >         Access method: tde_heap

## 延伸阅读 {#further-reading}

对于生产部署，接下来应使用合适的 [KMS 提供商](/zh/percona/global-key-provider-configuration/overview/)[配置全局主密钥](/zh/percona/global-key-provider-configuration/set-principal-key/)。

也可以直接[验证 pg_tde 加密](/zh/percona/test/)或[配置 WAL 加密](/zh/percona/wal-encryption/)。

可用的 `pg_tde` 函数见[函数参考](/zh/percona/functions/)。
