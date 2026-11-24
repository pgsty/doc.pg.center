---
title: "spock.max_proto_version()"
description: "返回 Spock 扩展支持的最高协议版本。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_max_proto_version.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock_max_proto_version()

## 概要 {#synopsis}

spock_max_proto_version()

## 返回值 {#returns}

返回已安装的 Spock 扩展支持的最高协议版本号，类型为整数。协议版本决定不同 Spock 版本之间的兼容性。

## 说明 {#description}

返回 Spock 扩展支持的最高协议版本。

函数查询 Spock 扩展可用于复制通信的最高协议版本号。协议版本决定节点间进行复制时可用的功能。

运行不同 Spock 版本的节点建立复制连接时，会在双方各自支持的最高协议版本中选择较低者，以保证版本间兼容。

协议版本号以整数表示。数值越大，协议版本越新，可用的功能也越多。

此函数定义在 `public` 模式中，只执行查询，不修改数据。

## 参数 {#arguments}

此函数不接受参数。

## 示例 {#example}

以下命令显示当前安装的 Spock 使用协议版本 4。

    postgres=# SELECT spock_max_proto_version();
     spock_max_proto_version
    -------------------------
                           4
    (1 row)

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_max_proto_version.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
