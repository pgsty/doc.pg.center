---
title: "spock.repset_remove_partition()"
description: "从包含父表的复制集中移除指定分区，或移除该分区表的所有分区。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_remove_partition.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock.repset_remove_partition()

## 概要 {#synopsis}

spock.repset_remove_partition (parent regclass, partition regclass)

## 返回值 {#returns}

实际从复制集中移除的分区数量，类型为整数。

## 说明 {#description}

从包含父表的复制集中移除指定分区，或移除该分区表的所有分区。

函数可将分区表的分区移出复制范围，同时保留父表的复制集成员身份。指定具体分区时只移除该分区；partition 参数为 NULL 时，父表的所有分区都将移出复制范围。

当父表和其他分区仍需复制时，可用此函数排除特定分区。例如，只复制近期分区，不复制旧分区中的历史数据。

从复制集中移除分区只会取消其成员资格。分区表仍保留在数据库中，可继续在本地访问。

函数返回实际从复制集中移除的分区数。如果没有移除任何分区（例如这些分区均不属于任何复制集），返回 0。

函数修改 Spock 系统目录，不修改用户数据或 PostgreSQL 服务器配置。

## 参数 {#arguments}

**`parent`**

父分区表，函数将从复制集中移除它的一个或多个分区。

**`partition`**

要从复制集中移除的具体分区。设为 NULL 时移除父表的所有分区。默认为 NULL。

## 示例 {#example}

    SELECT spock.repset_remove_partition('public.mytable',
    'public.mytable_202012');

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_remove_partition.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
