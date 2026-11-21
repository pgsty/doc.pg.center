---
title: Babelfish 文档
linkTitle: Babelfish
description: 覆盖安装、使用、内部机制、客户端与故障排查的技术文档。
weight: -60
type: docs
icon: fa-solid fa-fish
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website
translation_notice: en
sidebar_root_for: self
sidebar_root_link_self: true
cascade:
  type: docs
  upstream_source: babelfish
upstream_notice: /zh/babelfish/site/attribution/
upstream_license: LicenseRef-Babelfish-Website-ZH
outputs:
- HTML
- RSS
- print
- markdown
- LLMSFULL
---



从安装开始，选择迁移模式，评估兼容性，再连接应用。这里保留 Babelfish 网站的技术文档与中文全文翻译。

> [!NOTE] 版本适用范围
> 上游在 2023 年宣布将最新文档迁往 [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki)。本站依据固定源码快照整理，历史限制请对照所用版本的发行说明。

## 发布渠道 {#release-channels}

截至 2026 年 11 月 21 日，[Babelfish 开源扩展](https://github.com/babelfish-for-postgresql/babelfish_extensions/releases)在 GitHub 上的最新公开发布版本为 **6.1.0**。[适用于 Amazon Aurora PostgreSQL 的 Babelfish 6.2.0](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraPostgreSQLReleaseNotes/AuroraBabelfish.Updates.html)于 9 月 29 日公布，属于另一个发行版和发布渠道。本站保留的网站手册并非与上述任一渠道版本对应的参考文档；请查阅实际部署的二进制软件对应的发行说明。

首次使用建议先阅读[项目概览](/zh/babelfish/overview/)、[源码安装](/zh/babelfish/installation/compiling-babelfish-from-source/)和[迁移指南](/zh/babelfish/usage/migration/)。
