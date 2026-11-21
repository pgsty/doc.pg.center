---
title: pgEdge 文档
description: pgEdge 核心扩展文档索引。
weight: -20
type: docs
sidebar_root_for: self
no_list: true
outputs:
- HTML
- RSS
- print
- markdown
- LLMSFULL
cascade:
  type: docs
  upstream_source: pgedge
upstream_source: pgedge
upstream_link: https://github.com/pgEdge/spock/tree/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c
linkTitle: pgEdge
sidebar_root_link_self: true
icon: fa-solid fa-share-nodes
---


四个扩展围绕分布式 PostgreSQL 的具体任务协作。先从 Spock 建立复制，再根据应用需要加入全局 ID、大对象复制与会话保护。

- [Spock](/zh/pgedge/spock/) — 多主逻辑复制与冲突处理
- [Snowflake](/zh/pgedge/snowflake/) — 分布式唯一 ID
- [LOLOR](/zh/pgedge/lolor/) — 大对象逻辑复制
- [SafeSession](/zh/pgedge/safesession/) — 按角色限制只读会话
{.cards}

本版英文来源为 Spock v6.0.0-beta.2、LOLOR 1.3.0 开发快照、SafeSession v1.1 和 Snowflake v2.6.1。中文已同步本轮增量，原有初稿仍保留初稿标记。参见[来源与版本](/pgedge/about/attribution/)。

## 开始阅读 {#start}

- [快速开始](/zh/pgedge/quick-start/)
- [来源与版本](/zh/pgedge/about/attribution/)
