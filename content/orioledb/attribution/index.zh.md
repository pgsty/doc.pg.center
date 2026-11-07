---
title: 来源与许可
description: OrioleDB 快照范围、原始版权、译文来源，以及保留的上游差异说明。
weight: 60
type: docs
search_keywords: ["OrioleDB", "attribution"]
icon: fa-solid fa-scale-balanced
upstream_source: orioledb
upstream_link: https://www.orioledb.com/docs
upstream_notice: /zh/orioledb/attribution/
upstream_modified: true
---

本手册是由 [PGSTY](https://pgsty.com/) 维护的独立社区文档版本。开发、发布和支持仍由 [OrioleDB 上游项目](https://www.orioledb.com/)负责。

## 来源与范围 {#sources-and-coverage}

英文正文与中文译文来自 PGSTY 已整理的 OrioleDB 社区版本，其依据是 **2026-11-06** 抓取的上游在线网站。本集合收录全部 **18 篇文档**和**两份基准测试指南**，加上章节索引与本版说明，中英文**各 26 页**。

文档包括项目介绍、五篇使用指南、八篇架构文章和四篇开发指南；基准测试涵盖 pgbench 与车辆跟踪。产品首页、博客文章、作者资料与标签归档不在本集合范围内。

`data/imports/orioledb.json` 保留来源路径、Markdown 校验值、原始 HTML 校验值、代码指纹与迁入资源的校验值。图片随页面资源包存放，由中英文页面共享。[车辆跟踪驱动脚本](/orioledb/assets/tracking-bench.py)以源码文本形式保留，供复现测试时使用。

## 版权与许可证 {#copyright-and-licenses}

[OrioleDB 代码仓库](https://github.com/orioledb/orioledb)提供 Apache License 2.0 或 PostgreSQL License 二选一授权。来源社区版本对项目文档选择 **PostgreSQL 许可证**。完整声明 **Copyright (c) 2025-2026, Supabase Inc.** 及免责声明保留在 [LICENSE-POSTGRESQL.txt](/third_party/orioledb/LICENSE-POSTGRESQL.txt) 中。

上游网站标注 **Copyright © 2026 Supabase Inc**。基准测试材料、网站插图与商标保留原权利。来源版本未核实覆盖这些材料的独立通用转载许可，因此将其记为 **Upstream terms（上游条款）**，不套用本站或软件项目的许可证。软件的其他条款见上游 [Apache 许可证](https://github.com/orioledb/orioledb/blob/main/LICENSE-APACHE.txt)与 [PATENTS](https://github.com/orioledb/orioledb/blob/main/PATENTS.txt)。

中文翻译与社区整理署名为 **PGSTY**，以英文为权威版本。本次整合保留来源版本的译文状态，不代表重新完成了逐句技术审校。[PG.CENTER 版权说明](/zh/attribution/#orioledb)将本集合与其他手册一并登记。

## 本版整理内容 {#changes-in-this-edition}

来源版本已将 Docusaurus HTML 转为 Hugo Markdown。本次整合保留正文、代码、表格、图示、脚注与标题 ID，将介绍独立为概览页，并增设阅读入口。内部文档链接统一使用 `/orioledb/` 和 `/zh/orioledb/`。HTML 页面使用 OINK 原生署名；本站通过一处导出适配将相同署名加入 Markdown 和 LLMS，章节导读中的来源声明则随打印版保留。

各章节共用一棵 OrioleDB 侧栏。中英文标题 ID 对齐，用于双语对照和同步滚动。导航、搜索、图片缩放、表格展开、代码复制、打印及 Markdown/LLMS 导出均使用 OINK **1.5.1** 的原生功能。

## 版本语境与原文差异 {#version-context-and-source-discrepancies}

本版记录的是网站快照，不对应单一的软件发布版本。安装示例、实验功能与基准测试可能使用不同构建。来源版本记录了以下尚未解决的差异：

- 配置参考给出的回退默认值是 `500` 秒、`86400` 个事务，回退教程则写作 `3600` 和 `100000`。两页分别保留原值，使用时应检查实际运行版本的设置。
- 块设备指南介绍直接访问块设备，却又称主要数据保留在文件系统中。此处保留上游表述。
- 恢复示例在同一句先后顺序比较中两次写工作进程 #2。此处保留原文歧义。
- 中文空闲空间说明根据变长区段的上下文，将“can just read”译为不能仅依赖顺序读取，并澄清重复的检查点图注。页面合并说明纠正重复的兄弟页与图号引用；检查点说明将“release the log”按语境理解为释放锁。这些均沿用来源译文的编辑判断。

基准测试指南保留上游环境与方法。车辆跟踪的两组测试均使用带补丁的 PostgreSQL；pgbench 则另行构建原版 PostgreSQL 作为对照。PG.CENTER 没有独立重跑这些基准测试。
