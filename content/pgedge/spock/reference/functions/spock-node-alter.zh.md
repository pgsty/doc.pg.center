---
title: "spock.node_alter()"
description: "修改本地节点自身的 location、country 或 info，可同时修改多项。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_node_alter.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock.node_alter()

## 概要 {#synopsis}

spock.node_alter (p_location text DEFAULT NULL, p_country text DEFAULT NULL,
p_info_patch jsonb DEFAULT NULL)

## 返回值 {#returns}

成功时返回 `true`。如果 `p_info_patch` 不是 JSON 对象，或者其中的 `tiebreaker` 不是 JSON 数值、不是整数或超出 32 位整数范围，则抛出错误。

## 说明 {#description}

修改本地节点自身的 `location`、`country` 或 `info`，可同时修改多项。`p_info_patch` 会合并到现有 `info` 中。此函数仅能修改本地节点自身的记录，目标唯一，因此不像 `spock.node_refresh_info` 那样接受 `node_name` 参数。

省略参数（保留为 `NULL`）时，对应字段维持原值。`p_location` 和 `p_country` 各自仅在非 `NULL` 时覆盖原值。`p_info_patch` 也仅在非 `NULL` 时通过 `||` 按键合并到原有 `info` 中，补丁未提及的原有键会保留。

函数会验证 `p_info_patch` 中的 `tiebreaker` 键。其值必须是 JSON 数值，不能是字符串或 JSON `null`，并且必须是 32 位整数范围内的整数。否则调用报错，所有值维持原状。应通过此函数安全地修改节点的冲突裁决值。它的作用及必须验证的原因见[冲突处理中的 Tiebreaker 一节](/zh/pgedge/spock/conflicts/)。

最终执行的同样是 `UPDATE spock.node`，因此手写 `UPDATE` 与调用本函数的传播效果一致：变更会自动到达本节点的所有直接订阅方，无需手动操作，详见[自动传播节点元数据](/zh/pgedge/spock/reference/node-mgmt/#automatic-node-metadata-propagation)。直接对本节点自身的行执行 `UPDATE spock.node SET ...` 仍受支持，效果相同。`spock.node_alter` 负责验证输入并安全合并 `info`，底层表依然可以直接访问。

## 参数 {#arguments}

**`p_location`**

可选。替换本节点的 `location`。省略或传入 `NULL` 时保留原值。

**`p_country`**

可选。替换本节点的 `country`。省略或传入 `NULL` 时保留原值。

**`p_info_patch`**

可选。要合并到本节点现有 `info` 中的 JSON 对象。未提及的已有键会保留。省略或传入 `NULL` 时全部保留原值。如果包含 `tiebreaker`，其值必须是能用 32 位整数表示的 JSON 数值。

## 示例 {#example}

在 `n1` 上设置自定义冲突裁决值，同时保留 `info` 中已设置的其他键。

    n1=# SELECT spock.node_alter(p_info_patch => '{"tiebreaker": 42}'::jsonb);
     node_alter
    ------------
     t
    (1 row)

`n1` 的每个直接订阅方都会自动收到改动，无需调用 `spock.node_refresh_info`。

    n2=# SELECT info->>'tiebreaker' FROM spock.node WHERE node_name = 'n1';
     ?column?
    ----------
     42
    (1 row)

在一次调用中同时更新位置和国家。

    n1=# SELECT spock.node_alter(p_location => 'us-east', p_country => 'US');
     node_alter
    ------------
     t
    (1 row)

无效的冲突裁决值会被拒绝，原有设置均保留。

    n1=# SELECT spock.node_alter(p_info_patch => '{"tiebreaker": "42"}'::jsonb);
    ERROR:  invalid "tiebreaker" value "42": must be a JSON number, not a string or null

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_node_alter.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
