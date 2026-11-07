---
title: 文档勘误
description: 固定版本 pg_tde 文档的本站更正与核验依据。
type: docs
translation_notice: false
upstream_source: percona
upstream_link: https://github.com/percona/pg_tde/tree/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
---


以下更正适用于 [1660e66a6a30 文档快照](https://github.com/percona/pg_tde/tree/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39)，属于本站编辑性修订，不表示上游已合并这些更正。[来源清单](/percona/assets/source-manifest.json)仍记录原始文件与校验值。

| 页面 | 更正 | 依据 |
| --- | --- | --- |
| [函数](/zh/percona/functions/)与[使用参考](/zh/percona/advanced-topics/usage-guide/) | 使用 `pg_tde.inherit_global_providers`，替换过时参数名。 | [GUC 声明](https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/src/pg_tde_guc.c) |
| [函数](/zh/percona/functions/) | `pg_tde_set_key_using_global_key_provider` 设置当前数据库主密钥；独立的 server 函数用于 WAL。 | [主密钥实现](https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/src/catalog/tde_principal_key.c) |
| [使用参考](/zh/percona/advanced-topics/usage-guide/) | 服务器与默认主密钥设置函数只使用全局提供商，不能写成 `(global/database)` 变体。 | [SQL 定义](https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/pg_tde--1.0.sql) |
| [恢复工具](/zh/percona/command-line-tools/pg-tde-restore-encrypt/) | `%f` 是 WAL 文件名，`%p` 是写入未加密 WAL 段的目标路径。 | [工具内置帮助](https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/src/bin/pg_tde_restore_encrypt.c) |
| [复制](/zh/percona/replication/) | 先创建主密钥，再将其设为服务器主密钥。 | [SQL 定义](https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/pg_tde--1.0.sql) |
| [常见问题](/zh/percona/faq/) | `work_mem` 溢出临时文件不加密；普通 `VACUUM` 不轮换文件内部密钥，`VACUUM FULL` 等表重写操作才会生成新密钥。 | [限制](/zh/percona/index/tde-limitations/)及[加密架构](/zh/percona/architecture/encryption-architecture/) |
| [keyring 示例](/zh/percona/global-key-provider-configuration/keyring/) | 检查实际创建的 `customer_table`，使用 `pg_tde_key_info()` 查看当前数据库主密钥。 | [函数参考](/zh/percona/functions/) |
| [KMIP 概览](/zh/percona/global-key-provider-configuration/overview/) | 保留较早的验证状态描述，同时提示 2.2.2 已宣布支持 Vault Enterprise KMIP。 | [2.2.2 发布说明](/zh/percona/release-notes/release-notes-v2.2.2/) |

此外还补齐缺失的 SQL 引号，删除 RC 变更日志末尾的重复残片，修复链接与锚点，并将 MkDocs 页签和提示框转换为 Oink 组件。历史发布页明确标记对应时期。本站未嵌入上游聊天服务和反馈组件。

英文转换可通过 `scripts/import_upstream.py` 与 `scripts/upstream_edits.json` 重现，中文同步维护。翻译审校记录为本次自校记录，不表示经过独立审校，也不代表已运行 pg_tde 的数据库测试。
