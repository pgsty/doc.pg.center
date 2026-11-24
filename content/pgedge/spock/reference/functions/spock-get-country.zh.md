---
title: "spock.get_country()"
description: "返回创建节点时设置的 spock.country 属性。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_get_country.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock.get_country()

## 概要 {#synopsis}

spock.get_country ()

## 返回值 {#returns}

返回为该节点配置的国家代码，类型为 `text`。未设置时返回 `??`。

## 说明 {#description}

返回创建节点时设置的 `spock.country` 属性。之后可修改该属性，重启服务器后改动生效。

函数读取当前会话中配置参数 `spock.country` 的值。在跨区域或地理分布式复制拓扑中，通常用国家代码标识节点所在的地理位置，并据此应用区域路由或过滤规则。

此函数不会修改任何数据。

## 参数 {#arguments}

此函数不接受参数。

## 示例 {#example}

如果没有设置 `spock.country`，返回结果如下。

    postgres=# SELECT spock.get_country();
     get_country
    -------------
     ??
    (1 row)

如果将 `spock.country` 设置为 `US`，返回结果如下。

    postgres=# SELECT spock.get_country();
     get_country
    -------------
     US
    (1 row)

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_get_country.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
