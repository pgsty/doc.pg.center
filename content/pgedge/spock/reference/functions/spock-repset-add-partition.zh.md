---
title: "spock.repset_add_partition()"
description: "将分区添加到其父表所属的一个或多个复制集中。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_add_partition.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



`spock.repset-add-partition ()`

## 概要 {#synopsis}

spock.repset_add_partition (
    parent regclass,
    partition regclass,
    row_filter text)

## 返回值 {#returns}

  - 如果父表不是分区表，或所有分区都已加入相应复制集，则返回 0。

  - 其他情况下返回正整数，表示成功添加到复制集的分区数。

## 说明 {#description}

将分区添加到其父表所属的一个或多个复制集中。

处理分区表时，可以用此函数确保新建或已有的分区纳入复制。如果省略 partition 参数，Spock 会自动找出并添加指定父表的所有分区。

可选的 row_filter 用于限定分区中哪些行参与复制。

此函数向 Spock 系统目录写入元数据，不修改 PostgreSQL 配置。

此命令必须由超级用户执行。

## 参数 {#arguments}

**`parent`**

父分区表，以 regclass 指定。

**`partition`**

要添加的某个分区。省略时添加父表的所有分区。默认值为 NULL。

**`row_filter`**

可选的 SQL 表达式，用于过滤分区中参与复制的行。默认值为 NULL。

## 示例 {#example}

将名为 `'public.sales_parent'` 的父表的全部四个分区加入父表所属的复制集。

    SELECT spock.repset_add_partition('public.sales_parent');
    -[ RECORD 1 ]--------+--
    repset_add_partition | 4

将指定分区 public.sales_2026_q1 加入父表所属的复制集。

    postgres=# SELECT spock.repset_add_partition(
        'public.sales_parent',
        'public.sales_2026_q1',
        'region = ''US'''
    );
    -[ RECORD 1 ]--------+--
    repset_add_partition | 1


---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_add_partition.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
