---
title: "spock.repset_alter()"
description: "修改已有 Spock 复制集的复制行为。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_alter.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



`spock.repset_alter()`

## 概要 {#synopsis}

spock.repset_alter (
    set_name name,
    replicate_insert boolean,
    replicate_update boolean,
    replicate_delete boolean,
    replicate_truncate boolean
)

## 返回值 {#returns}

修改后复制集的 OID。

## 说明 {#description}

修改已有 Spock 复制集的复制行为。

复制集定义哪些类型的表操作会复制到订阅方。创建复制集后，可用此函数更改这些设置。

传入 NULL 的参数会保留当前设置，只有显式指定的操作类型会改变。

函数更新 Spock 系统目录中的元数据，不更改 PostgreSQL 服务器配置。

此命令必须由超级用户执行。

## 参数 {#arguments}

**`set_name`**

已有复制集的名称。

**`replicate_insert`**

设为 true 时复制 INSERT 操作，默认为 NULL。

**`replicate_update`**

设为 true 时复制 UPDATE 操作，默认为 NULL。

**`replicate_delete`**

设为 true 时复制 DELETE 操作，默认为 NULL。

**`replicate_truncate`**

设为 true 时复制 TRUNCATE 操作，默认为 NULL。

## 示例 {#example}

以下命令在 demo_repset 复制集中启用所有操作类型。

    postgres=# SELECT spock.repset_alter('demo_repset',
            replicate_insert := true,
            replicate_update := true,
            replicate_delete := true,
            replicate_truncate := true);
     repset_alter 
    --------------
       3356172311
    (1 row)

以下命令在 audit_only 复制集中关闭 DELETE 和 TRUNCATE 的复制。

    postgres=# SELECT spock.repset_alter('audit_only',
        replicate_delete := false,
        replicate_truncate := false);
    repset_alter 
    --------------
       3744767607
    (1 row)


---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_alter.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
