---
title: "spock.replicate_ddl()"
description: "在本地执行 DDL 命令，并将其加入复制队列以便在订阅方执行。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_replicate_ddl.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock.replicate_ddl()

## 概要 {#synopsis}

spock.replicate_ddl (command text[], replication_sets text[], search_path text,
role text)

## 返回值 {#returns}

  - 在本地成功执行 DDL 并将其加入复制队列时返回 true。

  - 命令执行失败或加入复制队列失败时返回 false。

传入文本数组时返回一组布尔值，每条命令对应一个值。

## 说明 {#description}

在本地执行 DDL 命令，并将其加入复制队列以便在订阅方执行。

函数先在本地节点执行指定的 DDL，再将其加入复制队列。所有订阅了任一指定复制集的订阅节点都会执行该命令。

函数既可接受一条文本形式的 DDL 命令，也可接受 DDL 命令数组。传入数组时，命令会依次执行并加入复制队列。

search_path 和 role 参数控制 DDL 命令在提供方及订阅方节点上的执行上下文。

函数会写入复制队列，并在传播变更之前先修改本地数据库模式。

执行此命令的用户必须有权执行相应的 DDL 命令。

## 参数 {#arguments}

**`command`**

要执行并复制的 DDL 命令，可以是单条文本或命令数组。

**`replication_sets`**

复制集名称数组。只有订阅了其中至少一个复制集的订阅方才会收到并执行 DDL。默认值为 `'{ddl_sql}'`。

**`search_path`**

执行 DDL 命令时使用的模式搜索路径。默认为当前会话的 search_path 设置。

**`role`**

执行 DDL 命令的角色（用户），默认为当前用户。

## 示例 {#examples}

以下命令创建一张表，并指示 Spock 将 DDL 复制到其他节点。

    postgres=# SELECT spock.replicate_ddl('CREATE TABLE users (id SERIAL PRIMARY KEY,
        name TEXT)');
    -[ RECORD 1 ]-+--
    replicate_ddl | t

以下命令修改表，添加一列，并指示 Spock 将 DDL 复制到其他节点。

    postgres=# SELECT spock.replicate_ddl('ALTER TABLE users ADD COLUMN email TEXT',
        '{default,ddl_sql}');
    -[ RECORD 1 ]-+--
    replicate_ddl | t

以下命令创建表并为该表创建索引，再指示 Spock 将 DDL 复制到其他节点。

    postgres=# SELECT spock.replicate_ddl(ARRAY['CREATE TABLE orders (id SERIAL)',
        'CREATE INDEX ON orders(id)']);
    -[ RECORD 1 ]-+--
    replicate_ddl | t
    -[ RECORD 2 ]-+--
    replicate_ddl | t

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_replicate_ddl.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
