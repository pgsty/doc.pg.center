---
title: 归属与许可证
description: 记录本迁移站点的源码、版权、许可证与修改信息。
type: docs
weight: 10
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/README.md
cascade:
  type: docs
  upstream_source: babelfish-site
translation_notice: en
upstream_notice: /zh/babelfish/site/attribution/
upstream_license: LicenseRef-Babelfish-Website-ZH
---



本站是 [Babelfish 上游网站](https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/README.md)的中英文社区镜像，由 PGSTY 整理为 Hugo / OINK 站点。本站不是 Babelfish、AWS 或 Microsoft 的官方网站。项目名称和标志用于标识上游项目，不表示其认可本站。

> Copyright Babelfish for PostgreSQL Contributors.

## 许可证记录 {#license-records}

上游存在两份不一致的声明，本站原样保留，并不将它们解释为双重许可：

- 仓库的 [`LICENSE`](/babelfish/assets/legal/upstream-LICENSE.txt) 是完整的 Apache License 2.0 文本。
- 同一修订的 [README · Credits](https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/README.md#credits) 声称网站采用 BSD-3-Clause；并注明网站从 BSD 许可的 [djangoproject.com](https://github.com/django/djangoproject.com) 分叉，合并了 [Just the Docs](https://github.com/pmarsceill/just-the-docs) 主题。[原始 README 副本](/babelfish/assets/legal/upstream-README.md)完整保留了该记录。
- Babelfish **软件组件**采用 Apache 2.0 或 PostgreSQL 许可证，具体以各源码仓库的许可证为准。这与网站材料的声明分开记录。
- 本次新增的站点配置、转换脚本和中文翻译按 Apache 2.0 提供，不改变原始材料的权利归属。
- 本站主题为 [OINK v1.5.1](https://github.com/pgsty/oink/releases/tag/v1.5.1)，按其自身 Apache 2.0 许可证使用。

## 上游第三方声明 {#third-party}

[原始 THIRD-PARTY 文件](/babelfish/assets/legal/upstream-THIRD-PARTY.txt)保留以下记录：

| 组件 | 许可证 | 原版权声明 |
| --- | --- | --- |
| Just the Docs 0.3.3 | MIT | Copyright (c) 2016 Patrick Marsceill |
| Jekyll Pure Liquid Table of Contents 1.1.0 | MIT | Copyright (c) 2017 Vladimir Jimenez |
| Bootstrap Icons 1.4.1 | MIT | Copyright (c) 2019-2020 The Bootstrap Authors |

这些是上游网站的历史依赖声明；本站使用 OINK 的本地资源和 Hugo 构建流程。

## 来源与修改 {#source-snapshot}

| 项目 | 记录 |
| --- | --- |
| 上游仓库 | [babelfish_project_website](https://github.com/babelfish-for-postgresql/babelfish_project_website) |
| 源码修订 | `f468c5ed3d38849502ee924cb3e236357404d14d` |
| 抓取日期 | 2026-11-06 |
| 中文翻译与站点维护 | PGSTY 文档项目 |
| 构建主题 | Hugo Extended / OINK 1.5.1 |

迁移将 Jekyll 页面转换为 Hugo Markdown，调整导航和站内链接，补充中文全文与双语锚点。原始代码块、技术标识符、博客作者和发布日期予以保留；贡献者照片缩小并转换为 WebP，项目标志仅适配明暗背景。原首页的发展原则与创始资料分别收录于[项目发展原则](/zh/babelfish/site/principles/)和[关于页面](/zh/babelfish/site/)。

每篇文档提供固定修订的源码链接，仓库中的 `data/upstream-manifest.json` 记录来源校验值、去向和结构数量。上游在 2023 年[宣布迁移文档](/zh/babelfish/blog/release/babelfish-website-announcement/)，当前文档应查阅 [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki)。历史设计文件单独标记，不作为当前支持列表。
