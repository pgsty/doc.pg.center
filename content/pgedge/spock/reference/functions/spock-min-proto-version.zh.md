---
title: "spock.min_proto_version()"
description: "返回 Spock 扩展支持的最低协议版本。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_min_proto_version.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock_min_proto_version()

## 概要 {#synopsis}

spock_min_proto_version()

## 返回值 {#returns}

返回已安装的 Spock 扩展支持的最低协议版本号，类型为整数。协议版本决定不同 Spock 版本之间的兼容性。

## 说明 {#description}

返回 Spock 扩展支持的最低协议版本。

函数查询 Spock 扩展可用于复制通信的最低协议版本号。协议版本决定节点间进行复制时可用的功能。

运行不同 Spock 版本的节点建立复制连接时，会协商选择双方都支持的协议版本。最低版本划定了兼容范围的下界：只支持更低版本协议的节点无法与当前安装的 Spock 进行复制。

协议版本号以整数表示。最低版本保证与较早版本 Spock 的向后兼容，同时允许两个节点在均支持的情况下使用较新的协议功能。

此函数定义在 `public` 模式中，只执行查询，不修改数据。

## 参数 {#arguments}

此函数不接受参数。

## 示例 {#example}

以下命令显示当前使用的 Spock 使用协议版本 3。

    postgres=# SELECT spock_min_proto_version();
     spock_min_proto_version
    -------------------------
                           3
    (1 row)

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_min_proto_version.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
