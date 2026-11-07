---
title: 加密架构
linkTitle: 加密架构
description: pg_tde 的双层密钥结构、AES 算法、SMGR 加密流程与 WAL 加密机制。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/architecture/encryption-architecture.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 420
upstream_source: percona
---

本节介绍 `pg_tde` 如何在 PostgreSQL 内部实现加密，涵盖密钥层次、支持的加密算法、加密流程，以及支持表、WAL 和其他数据库文件加密的内核改动。

这些组件共同构成 `pg_tde` 静态数据加密的基础。

## 双层密钥结构 {#two-key-hierarchy}

`pg_tde` 使用两类密钥：

1. 内部密钥用于加密数据，保存在 PostgreSQL 数据目录的 `$PGDATA/pg_tde` 下。
2. 主密钥用于加密内部密钥，通过密钥提供商 API 保存在外部密钥管理系统（KMS）中。

`pg_tde` 为每个数据库使用一个主密钥。该数据库的所有内部密钥都使用这个主密钥加密。

内部密钥对应具体的数据库文件：[对象标识符（OID）](https://www.postgresql.org/docs/current/datatype-oid.html) 不同的文件使用不同的内部密钥。

**示例：**

一个带有 4 个索引的表至少有 5 个内部密钥：表使用一个，每个索引各使用一个。序列或 TOAST 表等其他关联关系也有各自的密钥。

## 加密算法 {#encryption-algorithm}

`pg_tde` 当前使用以下加密算法：

* `AES-128-CBC`、`AES-256-CBC`：使用内部密钥加密数据库文件。
* `AES-128-CTR`、`AES-256-CTR`：使用内部密钥加密 WAL。
* `AES-128-GCM`、`AES-256-GCM`：使用主密钥加密内部密钥。

## 加密流程 {#encryption-workflow}

可以使用 `pg_tde` 加密整个数据库，也可以只加密选定的表。

为在不修改元数据结构的前提下实现这一点，加密表以 `tde_heap` 访问方法标记。

`tde_heap` 与 `heap` 访问方法在功能上相同。`pg_tde` 据此区分加密表（`tde_heap`）和未加密表（`heap`）。

是否加密的初始判断通过 `postgres` 事件触发器机制完成：

* `CREATE TABLE` 或 `ALTER TABLE` 语句使用 `tde_heap` 子句时，新创建的数据文件被标记为加密。
* 之后的文件操作会对数据进行加密或解密。

后续判断通过略作修改的存储管理器（SMGR）API 完成：

* `TRUNCATE` 或 `VACUUM FULL` 使数据库文件以不同 ID 重新创建时，新文件继承原文件的加密信息。
* 根据继承的信息，文件会被加密或保持未加密状态。

## WAL 加密功能 {#wal-encryption-functionality}

可以通过 GUC 参数 [`pg_tde.wal_encrypt`](/zh/percona/variables/#pgtde-walencrypt) 全局控制 WAL 加密。修改该参数需要重启服务器。

WAL 密钥还记录密钥创建后第一次 WAL 写入的 [LSN](https://www.postgresql.org/docs/17/wal-internals.html)。`pg_tde` 据此知道哪些 WAL 范围已经加密，以及使用了哪个密钥。

> [!NOTE]
> 详见[配置 WAL 加密](/zh/percona/wal-encryption/)。

这一设置只控制写入：启用 WAL 加密后，只有新写入的 WAL 才会加密。因此，同一个 WAL 文件可能同时包含加密和未加密的数据，取决于写入时该参数的状态。

`pg_tde` 使用内部密钥跟踪 WAL 记录的加密状态。服务器重启时，若启用了 WAL 加密，就写入一个新的内部密钥；若当前已关闭但此前启用过，则写入一个虚拟密钥，标记 WAL 加密已结束。

WAL 读取代码据此决定某条 WAL 记录是否需要解密，以及应使用哪个密钥。

## 加密其他访问方法 {#encrypting-other-access-methods}

目前 `pg_tde` 只加密 `heap` 表，以及与其关联的索引、TOAST 表、序列等文件。

索引包括所有通过 SMGR API 操作的索引，而不仅限于 PostgreSQL 内置索引。

使用 SMGR API 的其他表访问方法也可以支持加密。这需要添加一个标记访问方法并扩展事件触发器，做法与 `heap` 表相同。

## 存储管理器（SMGR）API {#storage-manager-smgr-api}

`pg_tde` 依赖略作修改的 SMGR API。改动包括：

* 让 API 具备通用扩展能力，允许扩展向存储管理器注入自定义代码。
* 增加文件跟踪信息。为已有关系创建新文件时，原文件的引用也会传入 SMGR 函数。

借助这些改动，`pg_tde` 在普通的 Magnetic Disk SMGR API 之上增加了一层：如果关联的表已加密，`pg_tde` 就在写入磁盘前加密文件，并在读取后按需解密。

## WAL 加密 {#wal-encryption}

WAL 加密通过独立的、覆盖整个服务器的机制实现，该机制扩展了 PostgreSQL 的 WAL 相关 API。与 SMGR 集成类似，它依赖对 PostgreSQL 内核 API 的额外扩展，以支持 WAL 记录加密。

配置方法见[配置 WAL 加密](/zh/percona/wal-encryption/)。
