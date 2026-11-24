---
title: "spock.repset_show_table()"
description: "返回特定表在指定复制集中的详细复制配置。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_show_table.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock.repset_show_table()

## 概要 {#synopsis}

spock.repset_show_table (relation regclass, repsets text[])

## 返回值 {#returns}

包含表复制配置详情的一条记录，各字段如下。

  - relid 是表关系的 OID。
  - nspname 是表所在的模式名。
  - relname 是表名。
  - att_list 是参与复制的列名数组。
  - 对表应用了行过滤条件时，has_row_filter 为 true。
  - relkind 表示关系类型，`'r'` 为普通表，`'p'` 为分区表。
  - 如果表是分区表的一个分区，relispartition 为 true。

## 说明 {#description}

返回特定表在指定复制集中的详细复制配置。

函数查询一张表在一个或多个复制集中的配置，列出参与复制的列、是否应用行过滤条件，以及表的类型和分区状态。

att_list 字段列出参与复制的具体列。如果复制所有列，其中会列出全部列名。如果将表加入复制集时配置了列过滤，则只列出当时指定的列。

has_row_filter 指明是否对表应用了行过滤表达式。有表达式时，只有符合自定义条件的行才会复制。

repsets 参数可以指定多个复制集。函数根据该表在这些集合中的配置返回相应信息。

此函数只执行查询，不修改任何数据。

## 参数 {#arguments}

**`relation`**

要查询复制信息的表。

**`repsets`**

复制集名称数组，用于指定在哪些复制集中检查表的配置。

## 示例 {#example}

以下命令显示 public.invoices 表的详细信息。

    postgres=# SELECT * FROM spock.repset_show_table('public.invoices',
        ARRAY['default', 'ddl_sql']);
    -[ RECORD 1 ]--+-----------------------------------------
    relid          | 17241
    nspname        | public
    relname        | invoices
    att_list       | {order_id,customer_id,order_date,amount}
    has_row_filter | f
    relkind        | r
    relispartition | f

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_show_table.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
