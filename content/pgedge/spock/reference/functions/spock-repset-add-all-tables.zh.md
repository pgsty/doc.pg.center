---
title: "spock.repset_add_all_tables()"
description: "将指定模式中所有已有的表添加到复制集。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_add_all_tables.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock.repset_add_all_tables()

## 概要 {#synopsis}

spock.repset_add_all_tables (set_name name, schema_names text[],
synchronize_data boolean)

## 返回值 {#returns}

  - 所有可复制的表均已添加到复制集时返回 true。

  - 如果参数无效、权限不足或操作失败，则返回 false。

## 说明 {#description}

将指定模式中所有已有的表添加到复制集。

函数将指定模式中找到的表对象登记到指定复制集。它只处理执行时已经存在的表，之后创建的表必须另行调用 spock.repset_add_table() 添加。

无法复制的表会被跳过，并产生一条指明模式名和表名的 WARNING。其余表仍会添加。如果复制集复制 UPDATE 或 DELETE，而表没有基于索引的复制标识，或者该表属于 spock.reserved_object 中列出的扩展，就会跳过此表。对于 spock.reserved_object 中列出的模式，只报告一次，并跳过整个模式。

复制 UPDATE 或 DELETE 的复制集需要在订阅方定位受影响的行，因此只接受具有基于索引的复制标识的表。可以使用 PRIMARY KEY，也可以使用建在 NOT NULL 列上、通过 ALTER TABLE ... REPLICA IDENTITY USING INDEX 指定的唯一索引。即使表有 PRIMARY KEY，REPLICA IDENTITY FULL 和 REPLICA IDENTITY NOTHING 也不满足要求。没有基于索引的复制标识的表可以加入只复制 INSERT 和 TRUNCATE 的复制集。

spock.repset_add_table() 遇到无法复制的表会报错，而本函数会继续处理其他关系，不会因为一个关系就拒绝整个调用。指定的模式不存在时仍会报错。

函数不考虑视图、物化视图、序列，以及 UNLOGGED 和 TEMPORARY 表。

分区表和各分区会作为独立的表收集，并逐一检查。在所有受支持的 PostgreSQL 版本中，ALTER TABLE ... REPLICA IDENTITY 都不会级联到分区。因此分区表和各分区的复制标识可能不同，可能父表被添加而某个分区被跳过，也可能恰好相反。Spock 按关系判断复制集成员身份。即使父表已加入复制集，被跳过的分区中各行的变更也不会复制。

synchronize_data 参数控制是否立即将表中已有数据同步到订阅方。设为 true 时，所有订阅该复制集的订阅方都会对每张表启动一次全表复制。

函数向 Spock 系统目录写入元数据，记录哪些表属于该复制集。

此命令必须由超级用户执行。

## 参数 {#arguments}

**`set_name`**

已有复制集的名称。

**`schema_names`**

模式名称数组。这些模式中的所有表都将加入复制集。

**`synchronize_data`**

设为 true 时，立即将表中已有数据同步到所有订阅方。默认为 false。

## 示例 {#example}

在数组中指定一个或多个模式名，即可将其中所有表添加到指定的复制集。以下命令将 public 模式中的所有表添加到 default 复制集。

    postgres=# SELECT spock.repset_add_all_tables('default', ARRAY['public']);
    -[ RECORD 1 ]---------+--
    repset_add_all_tables | t

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_add_all_tables.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
