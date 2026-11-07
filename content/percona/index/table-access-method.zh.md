---
title: 表访问方法与 pg_tde
linkTitle: 表访问方法
description: 理解 heap 与 tde_heap 的关系，以及在集群或会话中更改默认表访问方法。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/index/table-access-method.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 170
upstream_source: percona
---

表访问方法决定 PostgreSQL 如何在表中存储数据。默认的表访问方法是 `heap`。PostgreSQL 将数据组织成堆结构，表中的行没有特定顺序；每行独立存储，并由唯一的行标识符（TID）标识。

## heap 访问方法的工作方式 {#how-the-heap-access-method-works}

**插入：** 插入新行时，PostgreSQL 在表空间中寻找空闲位置并存储该行。

**删除：** 删除行时，PostgreSQL 将该行占据的空间标记为空闲，但数据会保留到被新插入的数据覆盖。

**更新：** PostgreSQL 通过删除旧行并插入包含更新值的新行来处理更新。

## 自定义访问方法 {#custom-access-method}

自定义访问方法允许你定义并实现自己的 PostgreSQL 数据组织方式。当默认表访问方法无法满足需求时，这很有用。

自定义访问方法通常通过 PostgreSQL 扩展提供。安装扩展并在 PostgreSQL 中启用后，就会创建相应的自定义访问方法。

`tde_heap` 就是一个例子。**只有**在[启用了 `pg_tde` 扩展](/zh/percona/setup/)并配置了密钥提供商的数据库中，它才会自动创建，使你能够加密数据。

要使用自定义访问方法，在 `CREATE TABLE` 命令中指定 `USING` 子句：

```sql
CREATE TABLE table_name (
    column1 data_type,
    column2 data_type,
    ...
) USING tde_heap;
```

### tde_heap 如何配合 pg_tde 工作 {#how-tdeheap-works-with-pgtde}

`tde_heap` 基于默认的 `heap` 访问方法，用来标记哪些表需要加密。它使用自定义存储管理器 TDE SMGR，后者只有在安装 `pg_tde` 扩展后才会启用。

每次数据修改都会先发送到缓冲区管理器，由它更新缓冲区缓存，再交给存储管理器写入磁盘。如果表需要加密，数据会交给 TDE 存储管理器，在落盘之前完成加密。

同样，客户端查询数据库时，PostgreSQL 内核把请求交给缓冲区管理器，检查所需数据是否已在缓冲区缓存中。如果不在，缓冲区管理器向存储管理器请求数据。TDE 存储管理器从磁盘读取加密数据，解密后加载到缓冲区缓存。缓冲区管理器再将请求的数据传给 PostgreSQL 内核，最后返回客户端。

因此，加密发生在存储管理器层。

## 更改默认表访问方法 {#changing-the-default-table-access-method}

可以修改默认表访问方法，让整个数据库集群中的每个表都使用自定义访问方法创建。例如，将 `tde_heap` 设为默认表访问方法即可默认启用数据加密。

更改之前，请考虑以下事项：

* 这是全局设置，作用于整个数据库集群，而不只是单个数据库。建议谨慎设置，因为 `CREATE` 语句未显式指定访问方法的所有表和物化视图都会使用该默认访问方法。
* 修改配置之前，必须在所有数据库中创建 `pg_tde` 扩展并配置密钥提供商。否则 PostgreSQL 找不到指定的访问方法，将报错。

设置新的默认表访问方法的步骤如下：

1. 在 `default_table_access_method` 参数中设置访问方法：

    {{< tabs group="via-the-alter-system-command-via-the-configuration-file-via-the-set-command" >}}
    {{< tab label="使用 ALTER SYSTEM" value="via-the-alter-system-command" >}}

    使用 `ALTER SYSTEM`，需要超级用户或 `ALTER SYSTEM` 权限。

    ```sql
    ALTER SYSTEM SET default_table_access_method = tde_heap;
    ```

    {{< /tab >}}
    {{< tab label="修改配置文件" value="via-the-configuration-file" >}}

    编辑 `postgresql.conf` 配置文件，为 `default_table_access_method` 设置参数值。

    ```ini
    default_table_access_method = 'tde_heap'
    ```  

    {{< /tab >}}
    {{< tab label="使用 SET" value="via-the-set-command" >}}

    可以使用 `SET` 命令临时修改当前会话的默认表访问方法。

    与修改 `postgresql.conf` 文件或使用 `ALTER SYSTEM` 不同，`SET` 所做的更改在会话结束后不会保留。

    运行 `SET` 不需要超级用户权限。

    可以在会话期间的任何时候执行 `SET`。

    ```sql
    SET default_table_access_method = tde_heap;
    ```

    {{< /tab >}}
    {{< /tabs >}}

2. 重新加载配置，使更改生效：

    ```sql
    SELECT pg_reload_conf();
    ```

[了解 pg_tde 的限制](/zh/percona/index/tde-limitations/)
