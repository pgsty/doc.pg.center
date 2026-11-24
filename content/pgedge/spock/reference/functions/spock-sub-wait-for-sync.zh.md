---
title: "spock.sub_wait_for_sync"
description: "spock.sub_wait_for_sync() 等待指定订阅的初始模式同步和数据同步完成，并等待所有尚未完成的表重新同步任务结束。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_wait_for_sync.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



`spock.sub_wait_for_sync()` 等待指定订阅完成初始模式同步和数据同步。

## 概要 {#synopsis}

```sql
spock.sub_wait_for_sync(subscription_name name)
```

## 说明 {#description}

`spock.sub_wait_for_sync()` 等待指定订阅的初始模式同步和数据同步完成，并等待所有尚未完成的表重新同步任务结束。

此函数会阻塞当前会话，直到订阅完全同步。它既监控新建订阅的初始同步阶段，也监控因复制集变更或手动操作而单独进行重新同步的表。

变更复制集并触发表重新同步后，建议先在提供方节点上调用 `spock.wait_slot_confirm_lsn()`。这样可确保检查订阅方的同步状态前，提供方已将所有必要变更刷盘。等提供方确认 LSN 后，再在订阅方调用 `spock.sub_wait_for_sync()`。

函数会一直等待，直到同步完成。调用者应确认订阅正在处理数据，并排除阻碍同步完成的问题。

## 参数 {#arguments}

此函数接受以下参数。

- `subscription_name`：要等待其同步完成的订阅名称。

## 示例 {#example}

以下示例使用 `spock.sub_wait_for_sync()` 等待订阅 `sub_n2_n1` 完成同步。

```sql
SELECT spock.sub_wait_for_sync('sub_n2_n1');
-[ RECORD 1 ]-----+-
sub_wait_for_sync |
```

关于零停机添加节点时如何使用订阅同步，详见 [ZODAN 教程](/zh/pgedge/spock/modify/zodan/zodan-tutorial/)。

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_wait_for_sync.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
