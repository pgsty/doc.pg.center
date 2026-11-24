---
title: "spock.repset_create()"
description: "创建一个 Spock 复制集。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_create.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



`spock.repset_create()`

## 概要 {#synopsis}

spock.repset_create (
    set_name name,
    replicate_insert boolean = true,
    replicate_update boolean = true,
    replicate_delete boolean = true,
    replicate_truncate boolean = true
)

## 返回值 {#returns}

新建复制集的 OID。

## 说明 {#description}

创建一个 Spock 复制集。

复制集规定向订阅方复制哪些类型的表操作。之后可通过其他 Spock 函数把表加入该复制集。

默认复制所有数据修改操作，包括 INSERT、UPDATE、DELETE 和 TRUNCATE。

创建复制集时，可单独关闭特定操作类型。

函数向 Spock 系统目录写入元数据，不改动 PostgreSQL 服务器配置。

此命令必须由超级用户执行。

## 参数 {#arguments}

**`set_name`**

复制集的唯一名称。

**`replicate_insert`**

设为 true（默认值）时复制 INSERT 操作。

**`replicate_update`**

设为 true（默认值）时复制 UPDATE 操作。

**`replicate_delete`**

设为 true（默认值）时复制 DELETE 操作。

**`replicate_truncate`**

设为 true（默认值）时复制 TRUNCATE 操作。

## 示例 {#example}

以下示例创建名为 demo_repset 的复制集，复制所有操作类型。

    postgres=# SELECT spock.repset_create('demo_repset');
     repset_create 
    ---------------
        3356172311
   (1 row)

以下命令创建名为 audit_only 的复制集，仅复制 INSERT 和 UPDATE 语句。

    postgres=# SELECT spock.repset_create('audit_only',
            replicate_delete := false,
            replicate_truncate := false);
        repset_create 
    ---------------
    3744767607
    (1 row)

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_create.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
