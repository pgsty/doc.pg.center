---
title: 快速开始
description: Spock 双节点集群的阅读路径。
weight: 5
icon: fa-solid fa-rocket
upstream_source: pgedge
upstream_link: https://github.com/pgEdge/spock/tree/4ac1aec2f0807dc7ee806ab99a6e99a4556186df
type: docs
---


先阅读安装前提，再按完整教程配置两个节点。Spock 需要 PostgreSQL 内核补丁；两端必须准备一致的表结构，并允许节点间认证连接。

![两个 PostgreSQL 节点都接受读写，Spock 在节点之间异步双向复制。](/pgedge/assets/images/replication-light.svg)
{width="600" height="388" caption="双节点复制示意。提交在本地完成；另一节点可见的时间取决于复制延迟。"}

- [安装前提](/zh/pgedge/spock/installation/)
- [从安装到复制验证](/zh/pgedge/spock/getting-started/)
- [双节点操作](/zh/pgedge/spock/two-node/)
- [资源估算](/zh/pgedge/spock/sizing/)
- [冲突类型](/zh/pgedge/spock/conflicts/)
- [使用限制](/zh/pgedge/spock/limitations/)
{.cards}
