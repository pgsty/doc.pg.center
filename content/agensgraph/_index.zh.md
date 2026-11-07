---
title: AgensGraph 文档
linkTitle: AgensGraph
description: AgensGraph 2.18.6.1 手册：从创建图开始，到查询、搜索和运维。
type: docs
weight: -30
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/index.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
sidebar_root_for: self
sidebar_root_link_self: true
cascade:
  type: docs
  upstream_source: agensgraph
no_list: true
outputs:
- HTML
- RSS
- print
- markdown
- LLMSFULL
icon: fa-solid fa-diagram-project
---


AgensGraph 是构建在 PostgreSQL 上的开源多模型数据库，由 [SKAI Worldwide](https://skaiworldwide.com/)（前身 Bitnine）在 Apache License 2.0 下开发和维护。它同时把数据保存为**属性图**和关系表。你可以用 **Cypher**、**GQL**（ISO/IEC 39075）或 **SQL** 查询这些数据；当这是得到答案的最短路径时，还可以在一条语句中组合其中两种语言。

本手册覆盖 AgensGraph 2.18.6.1。2.18 版本构建在 PostgreSQL 18 上，并实现了 GQL 标准的相当大一部分。[AgensGraph 2.18](/zh/agensgraph/release-notes/2.18/) 列出了变化，包括应用程序需要了解的内容。

## 本手册如何组织 {#how-this-manual-is-organized}

[快速开始](/zh/agensgraph/get-started/)安装服务端，加载本手册所有示例使用的小型电影图，并带你得到第一个结果。请先读它。

[概念](/zh/agensgraph/concepts/)解释属性图模型，以及图如何布局在 PostgreSQL 中。图是模式，标签是表。正因如此，一条语句才能同时混合图操作和关系操作。

[查询](/zh/agensgraph/querying/)按你接触语言的顺序讲解：读取、写入、组合流水线、遍历路径、建立索引，以及在 SQL 与 Cypher 之间跨界。

[参考](/zh/agensgraph/reference/)是同一语言的形式化定义——词法规则、类型，以及每个子句、语句和函数的独立页面。当你知道自己要什么、需要精确语法时，查这里。

[指南](/zh/agensgraph/guides/)覆盖数据加载和搜索功能。[驱动与客户端库](/zh/agensgraph/drivers/)指向客户端库。[运维](/zh/agensgraph/operations/)面向服务端运行。[系统目录](/zh/agensgraph/system-catalogs/)记录描述图的目录，[附录](/zh/agensgraph/appendix/)收录 GQL 一致性表、兼容性说明、关键字和错误码清单，以及 2.17 页名到本版的映射。

## 目录 {#contents}

- [快速开始](/zh/agensgraph/get-started/)
- [概念](/zh/agensgraph/concepts/)
- [查询](/zh/agensgraph/querying/)
- [参考](/zh/agensgraph/reference/)
- [指南](/zh/agensgraph/guides/)
- [驱动与客户端库](/zh/agensgraph/drivers/)
- [运维](/zh/agensgraph/operations/)
- [系统目录](/zh/agensgraph/system-catalogs/)
- [版本说明](/zh/agensgraph/release-notes/)
- [附录](/zh/agensgraph/appendix/)

{.cards}
