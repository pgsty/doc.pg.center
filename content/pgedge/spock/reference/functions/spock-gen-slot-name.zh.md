---
title: "spock.gen_slot_name()"
description: "根据统一的命名规则为 Spock 订阅生成复制槽名称。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_gen_slot_name.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock.spock_gen_slot_name()

## 概要 {#synopsis}

spock.spock_gen_slot_name(dbname name, provider_node name,
subscription name)

## 返回值 {#returns}

生成的复制槽名称，类型为 `name`。

## 说明 {#description}

根据统一的命名规则为 Spock 订阅生成复制槽名称。

函数根据数据库名、提供方节点名和订阅名生成槽名。名称遵循 Spock 的内部规则，便于追溯且能保证唯一性。

函数只执行计算，无需访问数据库或修改数据。给定订阅配置后，可以用它预先确定 Spock 将生成的槽名。

## 参数 {#arguments}

**`dbname`**

数据库名称。

**`provider_node`**

提供方节点名称。

**`subscription`**

订阅名称。

## 示例 {#example}

在以下示例中，数据库名为 `postgres`，节点名为 `n1`，订阅名为 `sub_n2n1`。

    postgres=# SELECT spock.spock_gen_slot_name('postgres', 'n1', 'sub_n2n1');
       spock_gen_slot_name
    --------------------------
     spk_postgres_n1_sub_n2n1
    (1 row)

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_gen_slot_name.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
