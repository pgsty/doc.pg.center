---
title: 来源与许可
description: Citus 14 的上游来源、快照范围、版权许可与翻译原则。
weight: 90
type: docs
icon: fa-solid fa-scale-balanced
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/?view=citus-14
no_list: true
---

本版由 PGSTY 根据 [Microsoft Learn 上的 Citus 14 文档](https://learn.microsoft.com/en-us/postgresql/citus/?view=citus-14)独立整理，作为 **PG.CENTER** 的文档集发布，使用 OINK **1.5.1** 与 Hugo Extended **0.168.0**。本版不由 Microsoft 或 Citus 项目维护。

## 来源与收录范围 {#sources}

上游快照采集于 **2026 年 11 月 7 日**，覆盖首页和目录中的全部 **59 篇文档**，其中包含手册收录的十篇技术文章。全部 60 个源页面均下载了中英文 HTML 与 Markdown 快照；所需的 27 张配图保存在本地页面包中。

整理后的版本每种语言各有 **67 页**：59 个导入页面、六个新增主题目录页、文档集首页以及本来源说明页。内容分为概览、安装部署、教程、数据建模、集群运维、迁移指南、参考手册、专题文章八组；上游的参考与指南索引分别用作其中两个目录页。

Microsoft Learn 标注的源仓库为 [`MicrosoftDocs/azure-databases-docs`](https://github.com/MicrosoftDocs/azure-databases-docs)，但采集时该公开仓库已不可用。本版另保留了一个[仓库存档快照](https://github.com/Kiranchandratrey/azure-databases-docs/tree/ff9de504fdbe2b7aa9d06411e0f0472d39dc1f14/citus)，固定在提交 `ff9de504fdbe2b7aa9d06411e0f0472d39dc1f14`，用于核对文档源码与许可文件。Learn 已发布页面可能具有更新的独立修订，不能将该存档提交视为所有采集页面的共同版本。

逐文件[导入清单](https://github.com/pgsty/doc.pg.center/blob/main/data/imports/citus.json)记录了已发布页面的源提交、源路径、快照校验和、标题锚点、代码校验和、图片和翻译状态。[上游登记表](https://github.com/pgsty/doc.pg.center/blob/main/data/upstreams.yaml)记录版本与许可文件校验和。

## 版权与许可 {#licenses}

Copyright (c) Microsoft Corporation and contributors。原始 Citus 文章保留作者权利及其原始发表链接。

源仓库中的文档与其他内容采用 **[知识共享署名 4.0 国际许可协议（CC BY 4.0）](https://creativecommons.org/licenses/by/4.0/)**；仓库中的代码采用 **MIT 许可证**。以下完整文本未经修改，随本版保留：

- [文档许可 — LICENSE](/third_party/citus/LICENSE)
- [代码许可 — LICENSE-CODE](/third_party/citus/LICENSE-CODE)
- [法律与商标声明 — ThirdPartyNotices.md](/third_party/citus/ThirdPartyNotices.md)

这些许可不授予使用 Microsoft 名称、标识或商标的权利。PostgreSQL、Citus、Azure 及其他产品名称仍属于各自权利人。本版自行撰写的导读、中文改编与导航采用 CC BY 4.0，并继续遵守上述原始条款。

## 专题文章与历史语境 {#articles}

[专题与博客](/citus/articles/)收录 Citus 手册中的十篇技术文章，不包含 Citus 公司博客的全部历史文章。上游手册提供的原始发表链接均予保留。示例、日期、基准测试结果和 Citus Cloud 停止接受新用户的说明保留原有语境；历史文章中提到的“最新版本”不代表当前 Citus 发行版。

## 整理与翻译原则 {#editorial}

以英文原文为准。Microsoft Learn 发布的中文为机器译文，在本版中仅作参考。PGSTY 已对照英文校订全部 59 个导入页面，复核术语、适用条件以及双语标题、示例和链接；导入清单记录每篇译文所依据的英文版本。后续新增但未完成校订的页面必须明确标注机器译稿。

本版重组导航、改写站内链接、保留上游标题锚点、将配图保存到本地，并将 Learn 提示块转为 OINK 提示块。导入时仅保留适用于 `citus-14` 的内容，排除 Learn HTML 中隐藏的旧版本段落。中英文代码、命令、程序输出、SQL 标识符和链接目标保持一致；Markdown 和整套手册导出均保留来源与版权许可说明。

已记录的勘误包括：根据 Citus 原始文章恢复指数公式、修复旧交叉引用、补充教程省略内容与端口差异说明，以及更正托管服务名称。七处程序输出段落以代码块保留原始换行。这些调整均记入导入清单；未经修改的中英文快照另存于本地来源归档。
