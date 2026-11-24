---
title: "spock.repset_drop()"
description: "删除已有的复制集。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_drop.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock.repset_drop()

## 概要 {#synopsis}

spock.repset_drop (set_name name, ifexists boolean)

## 返回值 {#returns}

  - 成功删除复制集时返回 true。

  - 复制集不存在且 ifexists 为 true 时返回 false。

  - 复制集不存在且 ifexists 为 false 时抛出 ERROR。

## 说明 {#description}

删除已有的复制集。

函数从 Spock 配置中删除复制集，同时移除与其关联的所有表、序列和 DDL 的成员关系。数据库中实际的表和序列会保留，删除的只是它们和该复制集的关联。

引用该复制集的现有订阅会保留，但将停止接收原属该复制集的对象变更。可以使用 spock.sub_remove_repset() 从订阅中移除已删除的复制集。

ifexists 参数控制错误处理方式。如果设为 true，复制集不存在时函数返回 false，不报错。适合事先无法确定复制集是否存在的场景。

函数修改 Spock 系统目录，不修改用户数据或 Postgres 服务器配置。

## 参数 {#arguments}

**`set_name`**

要删除的复制集名称。

**`ifexists`**

设为 true 时，如果复制集不存在则返回 false，不抛出错误。默认为 false。

## 示例 {#example}

以下命令删除名为 demo_repset 的复制集。如果该复制集不存在，也不会报错。

    postgres=# SELECT spock.repset_drop('demo_repset', true);
     repset_drop 
    -------------
     t
    (1 row)

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_drop.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
