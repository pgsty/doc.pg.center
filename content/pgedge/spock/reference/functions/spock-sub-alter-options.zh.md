---
title: "spock.sub_alter_options()"
description: "在一次原子操作中修改已有订阅的一项或多项设置。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_alter_options.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock.sub_alter_options()

## 概要 {#synopsis}

spock.sub_alter_options (subscription_name name, options jsonb)

## 返回值 {#returns}

  - 如果 `options` 对象至少包含一个键，则返回 true，更新 Spock 系统目录，并通知应用进程重启。

  - 如果 `options` 是空对象（`{}`），则返回 false，不改动系统目录，也不重启应用进程。

  - 如果订阅不存在、`options` 不是 JSON 对象、包含未知的键，或任一选项值未通过验证，则报 ERROR。

## 说明 {#description}

在一次原子操作中修改已有订阅的一项或多项设置。

只修改 `options` 对象中明确指定的键，其余选项保留当前值。如果对象为空（`{}`），则返回 false，不改动系统目录，也不重启应用进程。

如果 `options` 至少有一个键，函数会将新值写入 Spock 系统目录，并通知应用进程重启以使设置生效。调用者可以使用 `spock.sub_show_status()` 或 `spock.sub_wait_for_sync()` 确认进程已经重启并进入 `replicating` 状态。

## 参数 {#arguments}

**`subscription_name`**

已有订阅的名称。

**`options`**

一个 JSON 对象，键是要修改的选项名。提供未知键会报错。支持以下键。


**`forward_origins`**


由来源名称构成的 JSON 数组，用于按事务来源确定订阅方要接收或应用的事务。唯一可用的数组元素是字符串 `"all"`。传入空数组（`[]`）可关闭来源转发。

与其他已启用的订阅组合使用时存在限制，详见[来源转发](/zh/pgedge/spock/reference/sub-mgmt/#origin-forwarding)。


**`apply_delay`**


PostgreSQL 时间间隔字符串，例如 `"2 seconds"`、`"500ms"` 或 `"0"`，指定应用进程在应用每个事务前等待的时长。必须传入字符串，直接传数值会报错。


**`skip_schema`**


指定应用变更时要排除哪些模式的 JSON 名称数组。传入空数组（`[]`）清空排除列表。

## 示例 {#example}

将应用延迟设为 2 秒。

    postgres=# SELECT spock.sub_alter_options('sub_n2_n1',
                  '{"apply_delay": "2 seconds"}');
     sub_alter_options
    -------------------
     t
    (1 row)

在一次调用中启用所有来源的转发，并排除 `audit` 模式。

    postgres=# SELECT spock.sub_alter_options('sub_n2_n1',
                  '{"forward_origins": ["all"], "skip_schema": ["audit"]}');
     sub_alter_options
    -------------------
     t
    (1 row)

传入空对象时不做任何更改，返回 false，也不重启应用进程。

    postgres=# SELECT spock.sub_alter_options('sub_n2_n1', '{}');
     sub_alter_options
    -------------------
     f
    (1 row)

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_alter_options.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
