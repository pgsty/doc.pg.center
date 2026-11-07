---
title: GUC 参数
linkTitle: GUC 参数
description: pg_tde 的 WAL 加密、强制加密、全局提供商继承和 AES 密码算法参数。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/variables.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 630
upstream_source: percona
---

`pg_tde` 扩展提供以下 GUC 参数来配置其行为。

## pg_tde.wal_encrypt {#pgtde-walencrypt}

**类型** — boolean <br>
**默认值** — off

控制是否加密 WAL 写入的布尔参数。

修改此参数需要重启服务器，且只能在服务器级别设置。

WAL 加密由全局控制。启用后，整个 PostgreSQL 集群的所有 WAL 写入都会加密。

该参数只控制新的 WAL 写入，不影响已有 WAL 记录。

只要用于加密的密钥仍然可用，`pg_tde` 就始终能够读取已有的加密 WAL 记录。

启用 WAL 加密需要配置全局主密钥。详见 [WAL 加密配置](/zh/percona/wal-encryption/)。

## pg_tde.enforce_encryption {#pgtde-enforceencryption}

**类型** — boolean <br>
**默认值** — off

控制是否允许创建新的未加密表的布尔参数。

启用后，`CREATE TABLE` 必须使用 `tde_heap` 访问方法，否则会失败。

同样，`ALTER TABLE <x> SET ACCESS METHOD` 也只有将访问方法设为 `tde_heap` 时才允许执行。

其他 DDL 操作仍然允许。例如，只要不更改访问方法，就可以对未加密表执行其他 `ALTER` 命令。

可以在以下级别设置此参数：

* 全局：整个 PostgreSQL 集群。
* 数据库：指定数据库。
* 用户：指定用户。
* 会话：当前会话。

设置或修改参数值需要超级用户权限。示例见[强制加密](/zh/percona/how-to/enforcement/)。

## pg_tde.inherit_global_providers {#pgtde-inheritglobalproviders}

**类型** — boolean <br>
**默认值** — on

控制数据库能否使用全局密钥提供商存储主密钥的布尔参数。

关闭后，更改密钥提供商的函数只能使用数据库本地提供商。

此时，已配置的默认主密钥也会被禁用。

可以在以下级别设置此参数：

* 全局：整个 PostgreSQL 集群。
* 数据库：指定数据库。
* 用户：指定用户。
* 会话：当前会话。

> [!NOTE]
> 此设置不影响已有的全局密钥使用，只阻止通过全局提供商创建新的主密钥。

## pg_tde.cipher {#pgtde-cipher}

**类型** — string <br>
**默认值** — aes_128

用于选择密码算法（加密算法）的字符串参数。目前支持 `aes_128` 和 `aes_256`，分别对应 128 位和 256 位 AES 密钥。

该设置仅适用于设置之后创建的对象，包括主密钥、内部密钥以及由这些密钥加密的数据。已有对象不会重新加密。
