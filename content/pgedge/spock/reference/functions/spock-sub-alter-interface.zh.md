---
title: "spock.sub_alter_interface()"
description: "更改订阅连接到提供方节点时使用的网络接口。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_alter_interface.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



spock.sub_alter_interface()

## 概要 {#synopsis}

spock.sub_alter_interface (subscription_name name, interface_name name)

## 返回值 {#returns}

  - 成功更换接口时返回 true。

  - 如果订阅或接口不存在、参数无效或权限不足，则报 ERROR。

## 说明 {#description}

更改订阅连接到提供方节点时使用的网络接口。

函数修改已有订阅，使它通过另一个接口与提供方建立复制连接。指定的接口必须已在提供方节点上定义。

此函数适用于切换网络路径，例如从公有网络切换到私有网络，或者更换同一提供方节点的主机名或 IP 地址。

订阅将通过新接口重新建立连接。

此函数向 Spock 系统目录写入元数据。

此命令必须由超级用户执行。

## 参数 {#arguments}

**`subscription_name`**

已有订阅的名称。

**`interface_name`**

提供方节点上已有接口的名称。

## 示例 {#example}

以下示例修改连接复制集群时使用的接口，改用与 private_net 接口关联的连接字符串。

    postgres=# SELECT spock.sub_alter_interface('sub_n2_n1', 'private_net');
    sub_alter_interface 
    ---------------------
     t
    (1 row)

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/functions/spock_sub_alter_interface.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
