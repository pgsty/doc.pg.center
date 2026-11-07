---
title: Beta（2024-06-30）
linkTitle: Beta
description: pg_tde Beta 历史版本：访问方法重命名、内存与文件定位修复。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/release-notes/beta.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 920
upstream_source: percona
---

> [!NOTE] 历史版本
> 本页记录发布当时的能力。当前部署要求请查阅[支持的版本](/zh/percona/index/supported-versions/)和[已知限制](/zh/percona/index/tde-limitations/)。


Percona 提供的 `pg_tde` 扩展为 PostgreSQL 增加[透明数据加密（TDE）](/zh/percona/index/about-tde/)，帮助保护敏感的静态数据。

[开始使用](/zh/percona/install/)

> [!IMPORTANT]
>
> 此版本的 Percona 透明数据加密扩展**尚不建议用于生产环境**。欢迎测试并[提供反馈](https://forums.percona.com/c/postgresql/pg-tde-transparent-data-encryption-tde/82)，帮助改进产品，使其更快达到生产可用状态。

## 版本亮点 {#release-highlights}

从 `pg_tde` Beta 开始，扩展的访问方法重命名为 `tde_heap_basic`。创建表时使用该名称，相关步骤见[测试 TDE](/zh/percona/test/)。

## 变更日志 {#changelog}

* 修复 `pg_tde` 用于解密元组的内存耗尽问题。新组件 `TDEBufferHeapTupleTableSlot` 跟踪为解密元组分配的内存，并在不再需要元组槽时释放它。
* 通过向 `lseek` 传入原始文件描述符，修复调整文件当前位置的问题。感谢用户 _rainhard_ 提供修复。
* 改进初始化脚本，在 Docker 中运行 `pg_tde` 时支持 `POSTGRES_USER` 指定的自定义超级用户。感谢 _Alejandro Paredero_ 报告问题。
