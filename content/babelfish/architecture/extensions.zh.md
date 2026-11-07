---
title: Babelfish 扩展
linkTitle: 早期扩展规划
description: 保留 TDS、语言与数据类型扩展的早期设计规划。
weight: 20
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_architecture/extensions.md
upstream_ref: main @ f468c5ed3d38
translation_notice: en
upstream_modified: true
translation_status: complete
translation_credit: PGSTY 文档项目
upstream_notice: /zh/babelfish/site/attribution/
upstream_license: LicenseRef-Babelfish-Website-ZH
---



> [!WARNING] 历史设计资料
> 此文件来自上游源码中未发布为文档栏目的一组早期设计资料，保留用于研究项目历史，不代表当前功能支持。当前说明见 [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki)。中文翻译：PGSTY 文档项目。

以下是上游早期的扩展总体规划，记录了团队当时正在创建的扩展。

| 扩展 | 拟用名称 | 说明 |
| --- | --- | --- |
| TDS 扩展 | babelfishpg_tds | 提供使用 TDS（SQL Server）网络协议的第二个端点，SQL Server 应用应连接此端点。包含扩展本身及运行所需的协议钩子两部分。协议钩子当时已提交社区，参见[讨论](https://www.postgresql.org/message-id/flat/CAGBW59d5SjLyJLt-jwNv%2BoP6esbD8SCB%3D%3D%3D11WVe5%3DdOHLQ5wQ%40mail.gmail.com)。 |
| 语言扩展 | babelfishpg_tsql | 使用 ANTLR 解析器，提供兼容 T-SQL 的过程语言。 |
| 数据类型扩展 2 | babelfishpg_common | 包含 Babelfish 工程团队开发的其他数据类型，以及依赖的函数、索引、运算符等。计划将其他扩展中的所有数据类型提取到此扩展。 |
| 数据类型扩展 1 | Fixeddecimal | 从 2ndQuadrant 开发的 fixeddecimal 类型分叉。团队计划保留与原仓库的关联，注明原作者，并保留全部开发历史。命名方面，希望沿用原名称；还计划将为 Babelfish 增加的改进贡献回 2ndQuadrant。[原始源码](https://github.com/2ndQuadrant/fixeddecimal/blob/master/fixeddecimal.c)。 |
