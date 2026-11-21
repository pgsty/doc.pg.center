---
title: 1.0 发布候选版
description: DocumentDB 1.0 发布候选版已结束。DocumentDB 1.0 已发布；不支持将运行过发布候选版的主机和卷升级至 1.0。
type: docs
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/getting-started/release-candidate.md
weight: 1010
translation_source_sha256: 5a92ed413153c6f2b0ae9a9c82ea985ed2cf2e5e6dbaa4497b6072bc3b9b42b4
translation_review: AI-assisted bilingual review; 2026-11-07
---

1.0 发布候选版阶段已结束：[DocumentDB 1.0](/documentdb/getting-started/release-notes-1.0/) 于 2026-10-19 发布，采用与 v1.0-RC2 相同的提交。

不支持将运行过发布候选版的主机和数据卷升级至 1.0，安装程序会拒绝此类主机。请按照 [预编译软件包](/documentdb/getting-started/prebuilt-packages/) 或 [DocumentDB Local](/documentdb/documentdb-local/) 的说明，在全新主机或新卷上安装 1.0 版本，并使用 `mongodump` 和 `mongorestore` 迁移所需数据。
