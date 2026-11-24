---
title: "管理函数"
description: "使用以下函数管理复制集群。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/gen_mgmt.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



使用以下函数管理复制集群。

| 命令 | 说明 |
| --- | --- |
| [spock.get_country](/zh/pgedge/spock/reference/functions/spock-get-country/) | 返回节点配置的国家或地区代码。 |
| [spock_max_proto_version](/zh/pgedge/spock/reference/functions/spock-max-proto-version/) | 返回 Spock 支持的最高协议版本。函数位于 public 模式，调用时省略 `spock.` 前缀。 |
| [spock_min_proto_version](/zh/pgedge/spock/reference/functions/spock-min-proto-version/) | 返回 Spock 支持的最低协议版本。函数位于 public 模式，调用时省略 `spock.` 前缀。 |
| [spock.node_info](/zh/pgedge/spock/reference/functions/spock-node-info/) | 返回本地 Spock 节点的信息。 |
| [spock_version](/zh/pgedge/spock/reference/functions/spock-version/) | 返回 Spock 扩展的版本字符串。函数位于 public 模式，调用时省略 `spock.` 前缀。 |
| [spock_version_num](/zh/pgedge/spock/reference/functions/spock-version-num/) | 以整数返回 Spock 版本号。函数位于 public 模式，调用时省略 `spock.` 前缀。 |

## spock.get_country {#spockget_country}

使用 `spock.get_country` 获取节点配置的国家或地区代码。

`spock.get_country()`

返回创建节点时设置的 `spock.country` 属性。配置后仍可修改，需重启服务器才生效。

函数读取当前会话的 spock.country 配置参数。在跨区域复制拓扑中，通常用国家或地区代码标识节点位置，再应用特定地区的路由或过滤规则。

此函数不接受参数。

## spock_max_proto_version {#spock_max_proto_version}

使用 `spock_max_proto_version` 获取 Spock 支持的最高协议版本。

`spock_max_proto_version()`

返回 Spock 扩展支持的最高协议版本。

函数不接受参数，定义在 public 模式中，调用时须省略 `spock.` 前缀。

该函数查询 Spock 扩展并返回可用于复制通信的最高协议版本。协议版本决定节点间复制可用的功能。

不同 Spock 版本的节点建立复制连接时，会在双方支持的范围内，选取两个最高版本中较低的一个，以保证兼容。


## spock_min_proto_version {#spock_min_proto_version}

使用 `spock_min_proto_version` 获取 Spock 支持的最低协议版本。

`spock_min_proto_version()`

返回 Spock 扩展支持的最低协议版本。

函数不接受参数，定义在 public 模式中，调用时须省略 `spock.` 前缀。

该函数查询 Spock 扩展并返回复制通信可用的最低协议版本。协议版本决定节点间复制可用的功能。

运行不同版本的 Spock 节点建立复制连接时，必须从双方支持的范围中协商协议版本。最低协议版本界定了兼容下限。

## spock.node_info {#spocknode_info}

使用 `spock.node_info` 查询本地 Spock 节点信息。

`spock.node_info()`

该函数查询 Spock 系统目录，返回当前节点的标识符、名称、数据库信息及创建节点时设置的可选描述字段。

此函数不接受参数。

## spock_version {#spock_version}

使用 `spock_version` 获取 Spock 扩展的版本字符串。

`spock_version()`

返回 Spock 扩展的版本号。

函数不接受参数，定义在 public 模式中，调用时须省略 `spock.` 前缀。

以文本形式返回 Spock 扩展的版本，通常采用语义化版本格式，例如 "4.0.1" 或 "5.0.4"。

## spock_version_num {#spock_version_num}

使用 `spock_version_num` 获取整数形式的 Spock 版本号。

`spock_version_num()`

以整数形式返回 Spock 扩展版本。

函数不接受参数，定义在 public 模式中，调用时须省略 `spock.` 前缀。

返回以整数编码的扩展版本，SQL 查询可以直接比较版本，无须解析字符串。

整数通常形如 XXYYZZ，XX 为主版本，YY 为次版本，ZZ 为补丁版本。例如 3.1.0 可表示为 30100。

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/gen_mgmt.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
