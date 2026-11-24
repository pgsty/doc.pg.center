---
title: "spock.table_wait_for_sync()"
description: "等待给定订阅中的指定表完成同步。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_table_wait_for_sync.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock.table_wait_for_sync()

## 概要 {#synopsis}

spock.table_wait_for_sync (subscription_name name, relation regclass)

## 返回值 {#returns}

void，成功完成时无返回值。

## 说明 {#description}

等待给定订阅中的指定表完成同步。

函数会阻塞当前会话，直到指定表完成同步。在执行依赖该表数据的操作前，可以用它确认表已完全同步。

spock.sub_wait_for_sync() 会等待订阅中所有表同步，本函数则只等待指定的一张表。这样可以更精细地监控同步进度，也适用于下游操作只依赖特定表的场景。

变更复制集并触发表重新同步后，建议先在提供方节点上执行 spock.wait_slot_confirm_lsn()。这样可确保检查订阅方的同步状态前，提供方已将所有必要变更刷盘。等提供方确认 LSN 后，再在订阅方调用 spock.table_wait_for_sync()。

函数会一直等待，直到该表完成同步。调用者应确认订阅正在处理数据，并排除阻碍同步完成的问题。

## 参数 {#arguments}

**`subscription_name`**

要监控的订阅名称。

**`relation`**

要等待其同步完成的表名，以 regclass 指定，可带模式名。

## 示例 {#example}

    SELECT spock.table_wait_for_sync('sub_n2_n1', 'public.mytable');

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_table_wait_for_sync.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
