---
title: 使用参考
linkTitle: 使用参考
description: 配置密钥提供商、管理与轮换密钥、授予权限，以及创建和修改加密表。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/advanced-topics/usage-guide.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 620
upstream_source: percona
---

> [!NOTE] 本站勘误
> 过时的 GUC 名称、服务器及默认主密钥函数的无效变体已按源码修正。 详见[勘误记录](/zh/percona/site/errata/)。


本章介绍 `pg_tde` 的主要操作，包括配置密钥提供商、管理主密钥、设置权限和加密表。

执行具体的 `pg_tde` 任务时，可将本章作为参考。

## 前置条件 {#prerequisites}

使用 `pg_tde` 之前，先按照[安装 pg_tde](/zh/percona/install/) 完成配置。

## 添加提供商 {#add-providers}

可以在全局作用域或数据库作用域添加密钥提供商。

如果 `pg_tde.inherit_global_providers` 为 `on`，所有数据库都能看到并使用全局提供商。为 `off` 时，全局提供商仅用于 WAL 加密。

添加全局提供商：

```sql
pg_tde_add_global_key_provider_<TYPE>('provider_name', ... details ...)
```

添加数据库专用提供商：

```sql
pg_tde_add_database_key_provider_<TYPE>('provider_name', ... details ...)
```

## 修改提供商 {#change-providers}

修改全局提供商的参数值：

```sql
pg_tde_change_global_key_provider_<TYPE>('provider_name', ... details ...)
```

修改数据库专用提供商的参数值：

```sql
pg_tde_change_database_key_provider_<TYPE>('provider_name', ... details ...)
```

这些函数也允许更改提供商类型，但**不会**迁移任何数据。它们适用于服务器地址变化等基础设施迁移场景。

## 从命令行修改提供商 {#change-providers-from-the-command-line}

`pg_tde` 提供 `pg_tde_change_key_provider` 工具，可以从命令行修改提供商。

该工具与上述函数类似，语法如下：

```sh
pg_tde_change_key_provider <dbOid> <providerType> ... details ...
```

> [!NOTE]
> 该工具用于 PostgreSQL 服务器停止运行时，因此会绕过全部权限检查。由于无法访问系统目录，它需要数据库 OID（`dbOid`），而不是数据库名称。
>
> 此工具不会验证任何参数。

## 删除提供商 {#delete-providers}

使用以下函数删除提供商：

```sql
pg_tde_delete_database_key_provider(provider_name)
pg_tde_delete_global_key_provider(provider_name)
```

对于数据库专用提供商，函数先检查它是否正在使用，只有未被使用时才会删除。

对于全局提供商，函数会检查 WAL 或任何数据库是否在使用它；如果正在使用，则返回错误。

## 列出或查询提供商 {#list-query-providers}

`pg_tde` 提供两个函数来查看提供商：

* `pg_tde_list_all_database_key_providers()`
* `pg_tde_list_all_global_key_providers()`

它们返回提供商名称、类型和配置的列表。

## 提供商权限 {#provider-permissions}

`pg_tde` 根据管理函数的执行权限实现访问控制。

对于密钥和提供商管理，提供以下两个函数：

```sql
pg_tde_GRANT_database_key_management_TO_role(role_name)
pg_tde_REVOKE_database_key_management_FROM_role(role_name)
```

这些函数接受字符串形式的角色名称，例如 `'user1'`。

## 创建和轮换密钥 {#create-and-rotate-keys}

使用以下函数创建主密钥：

```sql
pg_tde_create_key_using_(global/database)_key_provider('key-name', 'provider-name')
```

使用以下函数启用或轮换主密钥：

```sql
pg_tde_set_key_using_(global/database)_key_provider('key-name', 'provider-name')
pg_tde_set_server_key_using_global_key_provider('key-name', 'provider-name')
pg_tde_set_default_key_using_global_key_provider('key-name', 'provider-name')
```

## 默认主密钥 {#default-principal-key}

通过 `pg_tde.inherit_global_providers`，还可以配置默认的全局主密钥。已启用 `pg_tde`、但未通过 `pg_tde_set_key_using_(global/database)_key_provider` 配置数据库专用主密钥的数据库都会使用它。

借助此功能，可以让整个服务器的所有数据库使用相同主密钥，从而完全关闭多租户隔离。

### 管理默认密钥 {#manage-a-default-key}

使用以下函数管理默认密钥：

* `pg_tde_create_key_using_global_key_provider('key-name','provider-name')`
* `pg_tde_set_default_key_using_global_key_provider('key-name','provider-name')`
* `pg_tde_delete_default_key()`

> [!NOTE]
> 只有当前没有数据库使用默认主密钥时，才能执行 `pg_tde_delete_default_key()`。
> 更改默认主密钥，会为使用当前默认主密钥的所有数据库轮换内部密钥的加密。

### 删除密钥 {#delete-a-key}

`pg_tde_delete_key()` 取消当前数据库的主密钥设置。如果当前数据库存在加密表且未配置默认主密钥，函数会报错。如果存在加密表但也有默认主密钥，则使用默认密钥加密内部密钥。

> [!NOTE]
> **不能**取消 WAL 密钥设置，因为服务器密钥单独管理。

## 当前密钥详情 {#current-key-details}

`pg_tde_key_info()` 返回当前主密钥名称及其使用的提供商。

`pg_tde_server_key_info()` 返回服务器密钥的相应信息。

`pg_tde_default_key_info()` 返回默认密钥的相应信息。

`pg_tde_verify_key()` 检查密钥提供商是否可访问、能否从中下载当前主密钥，以及它是否与内存中的当前密钥相同。任一检查失败都会报告相应错误。

## 密钥权限 {#key-permissions}

对特定数据库拥有管理权限的用户（`pg_tde_(grant/revoke)_(global/database)_key_management_(to/from)_role`）可以更改该数据库的密钥，并使用当前密钥相关函数。如果启用了 `pg_tde.inherit_global_providers`，也可以通过全局提供商创建密钥。

`pg_tde_(grant/revoke)_database_key_management_to_role` 函数仅处理上述函数的特定权限：允许用户更改数据库密钥，但不允许修改提供商配置。

## 创建加密表 {#create-an-encrypted-table}

使用以下命令创建加密表：

```sql
CREATE TABLE t1(a INT) USING tde_heap;
```

## 修改加密表 {#alter-an-encrypted-table}

使用以下命令更改或修改加密表：

```sql
ALTER TABLE t1;
```

## 更改 pg_tde.inherit_global_providers 设置 {#change-the-pgtde-inheritglobalkeys-setting}

可以在 `pg_tde.inherit_global_providers = on` 时使用 `pg_tde`，让数据库引用全局密钥或 keyring，然后将该设置改为 `off`。

此时，已有的全局提供商或全局默认主密钥引用会继续工作，但不能再建立新的全局作用域引用。
