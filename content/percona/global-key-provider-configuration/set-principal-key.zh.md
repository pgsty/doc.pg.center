---
title: 配置默认主密钥
linkTitle: 默认主密钥
description: 添加全局密钥提供商，创建并设置供未单独配置密钥的数据库使用的默认主密钥。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/global-key-provider-configuration/set-principal-key.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 390
upstream_source: percona
---

可以通过全局密钥提供商为服务器配置默认主密钥。所有未单独配置加密密钥的数据库都会使用它。

配置默认主密钥需要多个步骤，涉及以下函数：

- [pg_tde_add_global_key_provider_&lt;TYPE&gt;()](/zh/percona/advanced-topics/usage-guide/#add-providers)：添加全局密钥提供商。
- [pg_tde_create_key_using_global_key_provider()](/zh/percona/functions/#pgtdecreatekeyusingglobalkeyprovider)：在全局密钥提供商中创建主密钥。
- [pg_tde_set_default_key_using_global_key_provider()](/zh/percona/functions/#pgtdesetdefaultkeyusingglobalkeyprovider)：设置默认主密钥；如果已经配置了内部加密密钥，还会轮换内部加密密钥。

## 添加全局密钥提供商 {#add-a-global-key-provider}

添加方法见[密钥提供商管理](/zh/percona/functions/#key-provider-management)。

## 创建默认主密钥 {#create-a-default-principal-key}

> [!NOTE]
> 下方示例输出仅用于演示。请务必将密钥名称和提供商替换为实际值。

创建全局主密钥：

```sql
SELECT pg_tde_create_key_using_global_key_provider(
    'key-name',
    'global_vault_provider'
);
```

> [!DETAILS] 输出示例
> ```sql
>     postgres=# SELECT pg_tde_create_key_using_global_key_provider(
>         'keytest1',
>         'file-keyring'
>     );
>     pg_tde_create_key_using_global_key_provider
>     ---------------------------------------------
>
>     (1 row)
> ```

## 设置默认主密钥 {#set-a-default-principal-key}

设置默认主密钥：

```sql
SELECT pg_tde_set_default_key_using_global_key_provider(
    'key-name',
    'global_vault_provider'
);
```

> [!DETAILS] 输出示例
> ```sql
>     postgres=# SELECT pg_tde_set_default_key_using_global_key_provider(
>         'keytest1',
>         'file-keyring'
>     );
>     pg_tde_set_default_key_using_global_key_provider 
>     --------------------------------------------------
>
>     (1 row)
> ```

## 参数说明 {#parameter-description}

* `key-name`：主密钥在提供商中存储时使用的名称。
* `global_vault_provider`：之前配置的全局密钥提供商名称。

> [!NOTE]
>
> 如果未报错，说明操作成功。

## 密钥生成原理 {#how-key-generation-works}

密钥材料（实际的密码学密钥）由 `pg_tde` 自动生成，并由配置的提供商安全存储。

> [!NOTE]
>
> 此过程设置的是**整个服务器的默认主密钥**。未显式配置密钥的数据库都会回退到使用该密钥。

## 下一步 {#next-steps}

按照验证步骤确认加密按预期工作：

[验证 pg_tde 加密](/zh/percona/test/)
