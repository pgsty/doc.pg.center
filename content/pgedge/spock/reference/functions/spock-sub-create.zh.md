---
title: "spock.sub_create()"
description: "创建当前节点到提供方节点的订阅。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_create.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock.sub_create()

## 概要 {#synopsis}

spock.sub_create (subscription_name name, provider_dsn text,
replication_sets text[], synchronize_structure boolean,
synchronize_data boolean, forward_origins text[], apply_delay interval,
force_text_transfer boolean, enabled boolean, skip_schema text[])

## 返回值 {#returns}

新建订阅的 OID。

## 说明 {#description}

创建当前节点到提供方节点的订阅。

函数建立复制订阅，使当前节点（订阅方）接收指定提供方节点的变更。订阅定义要订阅哪些复制集，以及如何处理初始同步。

命令立即返回，不等待订阅初始化完成。可使用 spock.sub_wait_for_sync() 等待订阅完成同步并开始复制。

复制连接使用 subscription_name 作为 application_name，因此可以在 pg_stat_replication 中看到该名称。这便于监控，也便于在同步复制场景中配置 synchronous_standby_names。

函数向 Spock 系统目录写入元数据，并向提供方发起复制连接。

此命令必须由超级用户执行。

## 参数 {#arguments}

**`subscription_name`**

订阅名称，必须在整个集群中唯一。此名称显示在 pg_stat_replication 的 application_name 字段中。

**`provider_dsn`**

用于连接提供方节点的 PostgreSQL 连接字符串。

**`replication_sets`**

要订阅的复制集名称数组。可用值为 default、default_insert_only 和 ddl_sql。

**`synchronize_structure`**

设为 true 时，在开始复制前从提供方同步表和模式的结构。默认为 false。

**`synchronize_data`**

设为 true 时，对已订阅复制集内的所有表执行初始数据复制。默认为 false。

**`forward_origins`**

按来源选择要复制的变更。指定 `'{}'` 时，只复制由提供方节点本地产生的变更（来源 ID 为 0，即并非由其他节点复制而来）。在双向复制中，这可避免循环转发。指定 `{all}` 时复制所有来源的变更。默认值为 `{}`，只复制本地产生的变更。

与其他已启用的订阅组合使用时存在限制，详见[来源转发](/zh/pgedge/spock/reference/sub-mgmt/#origin-forwarding)。

**`apply_delay`**

表示应用延迟的时间间隔，指定收到提供方的变更后需等待多久才应用。适用于延迟备库，默认为 `'0'`。

**`force_text_transfer`**

设为 true 时，所有列都以文本形式复制。这种方式较慢，但允许在订阅方进行类型转换。默认为 false。

**`enabled`**

设为 true 时立即启用订阅。设为 false 时仅创建订阅，暂不启用。默认为 true。

**`skip_schema`**

结构和数据同步时要排除的模式名称数组。默认为 `'{}'`，即不跳过任何模式。

## 示例 {#example}

    SELECT spock.sub_create('sub_n2_n1',
        'host=127.0.0.1 port=5432 dbname=postgres');

    SELECT spock.sub_create('sub_n2_n1',
        'host=10.0.0.10 port=5432 dbname=postgres',
        replication_sets := '{default}',
        synchronize_structure := true,
        synchronize_data := true);

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_create.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
