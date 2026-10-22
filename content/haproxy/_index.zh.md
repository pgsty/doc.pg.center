---
title: "HAProxy 3.4.7-57 中文文档"
linkTitle: HAProxy
weight: 50
description: "HAProxy 3.4 入门、配置与管理三套完整手册的简体中文译本"
icon: fa-solid fa-network-wired
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
no_list: true
module: [HAPROXY]
categories: [参考]
upstream_source: haproxy
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
cascade:
  upstream_source: haproxy
  type: docs
  module: [HAPROXY]
---

**HAProxy** 是一款免费、快速、可靠的反向代理，适用于高可用、TCP 与 HTTP 负载均衡及应用流量管理。本组件收录三套 HAProxy 3.4 核心手册的完整中文译文，并将其重新编排为适合 OINK 阅读器的 Markdown 扁平阅读顺序。

本版对齐官方英文维护分支手册的 `3.4.7-57` 快照。最新稳定版为 `3.4.7`（`v3.4.7`）；
该快照包含稳定版发布之后的文档变更，源文件固定于提交
[`0faeaeda6cdb`](https://git.haproxy.org/?p=haproxy-3.4.git;a=commit;h=0faeaeda6cdbb65c0e0cedb9a20489581bd7d4c3)。

## 选择手册 {#choose-a-manual}

- [入门指南](/zh/haproxy/load-balancing/) — 用 9 个主题介绍负载均衡基础、HAProxy 架构、功能、容量规划、版本发布与周边生态。
- [配置手册](/zh/haproxy/http-fundamentals/) — 用 12 章完整覆盖代理、ACL、样本提取、日志、过滤器及各类选项。
- [管理指南](/zh/haproxy/prerequisites/) — 用 13 章讲解启动、重载、资源、日志、统计信息、运行时 CLI、故障排查与安全。
{.cards}

## 版本涵盖范围 {#edition-coverage}

| 手册 | 上游篇幅 | 本站编排 |
| --- | ---: | ---: |
| 入门指南 | 1,695 行 | 9 个扁平主题页 |
| 配置手册 | 33,246 行 | 12 个扁平章节页 |
| 管理指南 | 5,305 行 | 13 个扁平章节页 |

全部 34 个阅读页面均直接位于 HAProxy 组件根目录下。侧边栏使用三个不可点击的分组占位页分隔三套手册，不增加目录层级，也不占用前后翻页节点。

完整原始手册可从上方链接所指向的固定上游版本获取。[上游许可声明](/third_party/haproxy/LICENSE)与 [GPLv2 全文](/third_party/haproxy/GPL-2.0)随手册一并发布。每个页面均提供经审校的简体中文对照版本。
