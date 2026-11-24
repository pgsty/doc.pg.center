---
title: "spock.version_num()"
description: "以整数形式返回 Spock 扩展的版本号。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_version_num.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock.spock_version_num()

## 概要 {#synopsis}

spock.spock_version_num ()

## 返回值 {#returns}

已安装的 Spock 扩展的整数版本号。

## 说明 {#description}

以整数形式返回 Spock 扩展的版本号。

函数查询 Spock 扩展，并返回编码成整数的版本号。这样可直接在 SQL 查询中比较版本，无需解析字符串。

整数通常采用 XXYYZZ 格式，XX 表示主版本号，YY 表示次版本号，ZZ 表示补丁版本号。例如，3.1.0 可能表示为 30100。

此函数只执行查询，不修改任何数据。

## 参数 {#arguments}

此函数不接受参数。

## 示例 {#example}

以下命令以整数形式返回当前 Spock 扩展版本号。

    postgres=# SELECT spock.spock_version_num();
    -[ RECORD 1 ]-----+------
    spock_version_num | 50005

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_version_num.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
