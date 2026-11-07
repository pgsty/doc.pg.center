---
title: pg_tde 的工作方式
linkTitle: 工作原理
description: 了解内部加密密钥与主密钥如何配合，在写入和读取时透明地加解密数据。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/index/how-does-tde-work.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 140
upstream_source: percona
---

加密数据时使用两类密钥：

* **内部加密密钥**用于加密用户数据，存储在内部，靠近其加密的数据。
* **主密钥**用于加密数据库密钥，与数据库密钥分开保存，由外部密钥管理存储管理。

> [!NOTE]
> 关于如何在外部管理和存储主密钥，包括支持的密钥管理系统和本地 keyring 选项，详见[密钥管理概览](/zh/percona/global-key-provider-configuration/overview/)。

加密过程如下：

![pg_tde 加密流程](/percona/assets/images/tde-flow.png)

用户通过 `pg_tde` 创建加密表时，系统会在内部为该表生成一个新的随机密钥，并使用 AES-CBC 密码算法对其加密。这个密钥用于加密用户向表中插入的全部数据。加密后的数据最终写入底层存储。

内部密钥本身使用主密钥加密。主密钥保存在外部密钥管理存储中。

同样，当用户查询加密表时，系统从密钥存储中获取主密钥，用它解密内部密钥，再用该表唯一的内部密钥解密数据，并将明文返回给用户。因此，每个 TDE 表都有唯一的密钥，每个表密钥又由主密钥加密。

[了解加密数据的范围](/zh/percona/index/tde-encrypts/)
