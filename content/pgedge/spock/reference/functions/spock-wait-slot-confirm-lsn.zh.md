---
title: "spock.wait_slot_confirm_lsn()"
description: "等待指定的复制槽确认已接收变更，直到指定的日志序列号（LSN）。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_wait_slot_confirm_lsn.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock.wait_slot_confirm_lsn()

## 概要 {#synopsis}

spock.wait_slot_confirm_lsn (slotname name, target pg_lsn)

## 返回值 {#returns}

void，成功完成时无返回值。

## 说明 {#description}

等待指定的复制槽确认已接收变更，直到指定的日志序列号（LSN）。

函数会阻塞当前会话，直到复制槽确认的刷盘 LSN 达到或超过目标 LSN。可据此确保订阅方已接收并确认复制变更，再继续执行后续操作。

已确认的刷盘 LSN 表示订阅方成功接收、应用并持久化复制变更的位置。此函数通过等待该位置，协调提供方和订阅方节点的操作。

如果复制槽不存在，函数会报错。函数会一直等待，直到达到目标 LSN，因此调用者应确认该位置可达，且订阅正在处理变更。

此函数不修改数据，但可能长时间阻塞，具体取决于复制延迟和网络状况。

## 参数 {#arguments}

**`slotname`**

要监控的复制槽名称。

**`target`**

要等待的目标日志序列号。复制槽确认的刷盘 LSN 达到或超过该值时，函数返回。

## 示例 {#example}

以下命令等待名为 spock_local_sync_346_79a 的槽确认已接收到目标 LSN（0/3000000）处的变更。

    SELECT spock.wait_slot_confirm_lsn('spock_local_sync_346_79a',
    '0/3000000');

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_wait_slot_confirm_lsn.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
