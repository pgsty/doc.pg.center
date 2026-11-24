---
title: "spock.repset_add_all_seqs()"
description: "将指定模式中所有已有的序列添加到复制集。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_add_all_seqs.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock.repset_add_all_seqs()

## 概要 {#synopsis}

spock.repset_add_all_seqs (set_name name, schema_names text[],
synchronize_data boolean)

## 返回值 {#returns}

  - 所有序列均成功添加到复制集时返回 true。

  - 如果参数无效、权限不足或操作失败，则报 ERROR。

## 说明 {#description}

将指定模式中所有已有的序列添加到复制集。

函数将指定模式中找到的所有序列对象登记到指定复制集。它只处理执行时已存在的序列，之后创建的序列必须另行调用 spock.repset_add_seq() 添加。

synchronize_data 参数控制是否立即在节点间同步序列值。设为 true 时，每个序列的当前值都会传播到订阅方。

函数向 Spock 系统目录写入元数据，记录哪些序列属于该复制集。

此命令必须由超级用户执行。

**警告**：在多主复制场景中，建议不要将序列添加到复制集。可以使用 [Snowflake 序列](https://github.com/pgEdge/snowflake)管理分布式环境中的序列，以避免冲突。

## 参数 {#arguments}

**`set_name`**

已有复制集的名称。

**`schema_names`**

模式名称数组。这些模式中的所有序列都将加入复制集。

**`synchronize_data`**

设为 true 时，立即同步每个序列的当前值。默认为 false。

## 示例 {#example}

调用 repset_add_all_seqs 时可以指定一个或多个模式。第一条命令将 `'public'` 模式中的序列添加到 `'default'` 复制集。

    postgres=# SELECT spock.repset_add_all_seqs('default', ARRAY['public']);
    -[ RECORD 1 ]-------+--
    repset_add_all_seqs | t

以下命令将 `'public'` 和 `'alice'` 两个模式中的所有序列添加到 `'default'` 复制集。

    postgres=# SELECT spock.repset_add_all_seqs('default', ARRAY['public', 'alice'],true);
    -[ RECORD 1 ]-------+--
    repset_add_all_seqs | t

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_repset_add_all_seqs.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
