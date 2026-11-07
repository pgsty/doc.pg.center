---
title: pg_tde_change_key_provider
linkTitle: 更换密钥提供商
description: 服务器离线且因密钥提供商不可访问而无法启动时，直接修复提供商配置。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/command-line-tools/pg-tde-change-key-provider.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 740
upstream_source: percona
---

此工具用于修改密钥提供商配置，也可以更改其类型。

它直接编辑配置文件，不检查权限，也不检查是否存在正在运行的 `postgres` 进程。

该工具仅用于修复因无法访问密钥提供商而无法启动的服务器。

例如，从旧备份恢复时，提供商地址已经变化。可以使用此工具修正配置，让服务器能够启动。

**警告：只能在服务器离线时使用此工具。** 服务器运行期间需要修改提供商配置时，应使用 [`pg_tde_change_(global/database)_key_provider_<type>`](/zh/percona/functions/#change-an-existing-provider) SQL 函数。

## 使用示例 {#example-usage}

修改提供商配置时，应按提供商类型指定所有参数，与调用 [`pg_tde_change_(global/database)_key_provider_<type>`](/zh/percona/functions/#change-an-existing-provider) SQL 函数时相同。

通用语法如下：

```sh
pg_tde_change_key_provider [-D <datadir>] <dbOid> <provider_name> <new_provider_type> <provider_parameters...>
```

## 参数说明 {#parameter-description}

* [可选] `<datadir>`：数据目录。未指定时，`pg_tde` 使用 `$PGDATA` 环境变量。
* `<provider_name>`：为密钥提供商指定的名称。
* `<new_provider_type>`：可以为 `file`、`vault` 或 `kmip`。
* `<dbOid>`

根据提供商类型，还需要以下参数：

```sh
pg_tde_change_key_provider [-D <datadir>] <dbOid> <provider_name> file <filename>
pg_tde_change_key_provider [-D <datadir>] <dbOid> <provider_name> vault-v2 <url> <mount_path> <token_path> [<ca_path>]
pg_tde_change_key_provider [-D <datadir>] <dbOid> <provider_name> kmip <host> <port> <cert_path> <key_path> [<ca_path>] 
```
