---
title: 密钥与密钥提供商管理
linkTitle: 密钥与提供商
description: 主密钥轮换、内部密钥重建、密钥存储布局和密钥提供商迁移。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/architecture/key-provider-management.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 430
upstream_source: percona
---

`pg_tde` 使用由主密钥和内部密钥构成的层次结构加密数据库文件。本章介绍密钥轮换、重新生成、存储和密钥提供商配置，帮助你确保加密数据安全且可访问。

## 主密钥轮换 {#principal-key-rotation}

可以轮换主密钥以满足常见安全策略，或处理主密钥可能泄露的情况。

轮换时，`pg_tde` 生成主密钥的新版本，并用新密钥重新加密关联的内部密钥。旧主密钥保留在原位置，因为解密备份或其他数据库时可能仍然需要它。

## 重新生成内部密钥 {#internal-key-regeneration}

表、索引和其他数据文件的内部密钥在文件创建时生成。没有直接重新加密文件的方法。

可以间接实现这一点：`VACUUM FULL` 或需要重写文件的 `ALTER TABLE` 等操作会将表数据移入新文件，同时为新文件创建新密钥，实际效果相当于轮换内部密钥。不过，这需要在整个操作期间持有表的排他锁，对大表可能并不合适。

WAL 内部密钥创建后不会改变。每次服务器启动或重启都会生成新的 WAL 密钥。如果启用了 WAL 加密（`pg_tde.wal_encrypt`），新密钥创建后的所有 WAL 写入都会使用它加密，直到下次重启生成**另一个**密钥。这样可以确保每个 WAL 段使用一致的加密密钥，无需手动管理密钥轮换。

## 内部密钥存储 {#internal-key-storage}

内部密钥以及其他 `pg_tde` 元数据统一保存在 `$PGDATA/pg_tde` 目录中。该目录为每个数据库保存独立的文件，例如：

* 加密后的内部密钥，以及内部密钥到表的映射。
* 密钥提供商信息。

`$PGDATA/pg_tde` 中还包含一个以 OID `1664` 标记的特殊全局区域，用于保存全局密钥提供商和全局内部密钥。

全局区域用于 WAL 加密。数据库也可以使用全局区域，例如为不同数据库配置独立主密钥、但使用同一个全局密钥提供商的场景。为此，必须启用全局提供商继承。

全局默认主密钥使用特殊 OID `1663`。

## 密钥提供商（主密钥存储） {#key-providers-principal-key-storage}

在 `pg_tde` 中，密钥管理系统（KMS）被视为外部密钥提供商。提供商负责保存并提供 `pg_tde` 加解密所需的主密钥。

配置密钥提供商后，`pg_tde` 会：

* 在创建新主密钥时将其上传。
* 在需要解密时（例如启动或重启时）从提供商获取主密钥。
* 缓存已获取的密钥，减少重复查询。

> [!NOTE]
> 每个密钥提供商都需要详细配置，包括服务地址和认证信息。

支持的提供商完整列表及配置步骤见[密钥管理概览](/zh/percona/global-key-provider-configuration/overview/)。

## 密钥提供商管理 {#key-provider-management}

密钥提供商的配置或位置可能变化，例如服务迁移到新地址，或主密钥需要迁移到另一类型的提供商。`pg_tde` 支持这两种场景，可以通过简单的 [SQL 函数](/zh/percona/functions/#key-provider-management)管理主密钥。

某些情况下无法使用 SQL 函数管理提供商。例如，服务器停机期间提供商发生变更，服务器因而不知道这些变化。如果启动过程需要访问加密密钥，就可能启动失败。

为处理这种情况，`pg_tde` 也提供[命令行工具](/zh/percona/command-line-tools/cli-tools/)来恢复数据库。

## 密钥提供商的敏感信息 {#sensitive-key-provider-information}

> [!IMPORTANT]
> 密钥提供商的认证信息属于敏感信息，必须妥善保护。
> 不要将这些凭据与数据库一起存放在 `$PGDATA` 中。应将其保存在安全位置，并通过严格的文件系统权限防止未经授权的访问。
