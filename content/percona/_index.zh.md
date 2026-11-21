---
upstream_link: https://github.com/percona/pg_tde/tree/5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a
title: Percona TDE 文档
linkTitle: Percona TDE
description: 从加密原理到安装、运维和参考的完整 pg_tde 文档。
no_list: true
type: docs
sidebar_root_for: self
sidebar_root_link_self: true
translation_notice: false
upstream_source: percona-20261121
weight: -50
outputs:
- HTML
- RSS
- print
- markdown
- LLMSFULL
cascade:
  type: docs
  upstream_source: percona-20261121
icon: fa-solid fa-shield-halved
---


pg_tde 文档按照生产 PostgreSQL 部署的实际路径组织：先理解加密模型，再安装扩展、配置密钥托管、验证加密表，最后处理 WAL、备份、恢复与升级。

当前版本为 [pg_tde 2.3.0](/zh/percona/release-notes/release-notes-v2.3.0/)，新增 PostgreSQL 19 支持，并可识别和查看 pg_tde 的 WAL 记录。

- [概览](/zh/percona/index/) — 了解 TDE、pg_tde、支持的部署方式与限制。
- [开始使用](/zh/percona/install/) — 安装软件包并创建扩展。
- [密钥管理](/zh/percona/global-key-provider-configuration/) — 配置 KMS 提供商与主密钥。
- [技术参考](/zh/percona/advanced-topics/) — 架构、函数、GUC 参数与流复制。
- [运维操作](/zh/percona/how-to/) — 备份、恢复、加密强制、多租户与升级。
- [发布说明](/zh/percona/release-notes/) — 跟踪兼容性与变更历史。

{.cards}
