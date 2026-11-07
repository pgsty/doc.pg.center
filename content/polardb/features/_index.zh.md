---
title: 功能参考
description: 按性能、可用性、安全、并行查询和扩展插件查阅 PolarDB 功能。
weight: 30
upstream_link: https://github.com/polardb/polardb-pg-docs/blob/b4733b0350888242afeba432a6837458c348a937/docs/zh/features/README.md
upstream_source: polardb
upstream_modified: true
icon: fa-solid fa-layer-group
no_list: true
type: docs
---


## 功能分类 {#功能分类}

- [高性能](/zh/polardb/features/performance/)
- [高可用](/zh/polardb/features/availability/)
- [安全](/zh/polardb/features/security/)
- [弹性跨机并行查询（ePQ）](/zh/polardb/features/epq/)
- [第三方插件](/zh/polardb/features/extensions/)

## 功能导览 {#功能导览}

### 高可用 {#高可用}

- [只读节点 Online Promote](/zh/polardb/features/availability/avail-online-promote/) {{< badge text="V11 / v1.1.1-" tone="info" >}}
- [WAL 日志并行回放](/zh/polardb/features/availability/avail-parallel-replay/) {{< badge text="V11 / v1.1.17-" tone="info" >}}
- [DataMax 日志节点](/zh/polardb/features/availability/datamax/) {{< badge text="V11 / v1.1.6-" tone="info" >}}
- [闪回表和闪回日志](/zh/polardb/features/availability/flashback-table/) {{< badge text="V11 / v1.1.22-" tone="info" >}}
- [Resource Manager](/zh/polardb/features/availability/resource-manager/) {{< badge text="V11 / v1.1.1-" tone="info" >}}

### 弹性跨机并行查询（ePQ） {#弹性跨机并行查询epq}

- [自适应扫描](/zh/polardb/features/epq/adaptive-scan/) {{< badge text="V11 / v1.1.17-" tone="info" >}}
- [集群拓扑视图](/zh/polardb/features/epq/cluster-info/) {{< badge text="V11 / v1.1.20-" tone="info" >}}
- [ePQ 支持创建 B-Tree 索引并行加速](/zh/polardb/features/epq/epq-create-btree-index/) {{< badge text="V11 / v1.1.15-" tone="info" >}}
- [ePQ 支持创建/刷新物化视图并行加速和批量写入](/zh/polardb/features/epq/epq-ctas-mtview-bulk-insert/) {{< badge text="V11 / v1.1.30-" tone="info" >}}
- [ePQ 执行计划查看与分析](/zh/polardb/features/epq/epq-explain-analyze/) {{< badge text="V11 / v1.1.20-" tone="info" >}}
- [ePQ 计算节点范围选择与并行度控制](/zh/polardb/features/epq/epq-node-and-dop/) {{< badge text="V11 / v1.1.20-" tone="info" >}}
- [ePQ 支持分区表查询](/zh/polardb/features/epq/epq-partitioned-table/) {{< badge text="V11 / v1.1.17-" tone="info" >}}
- [并行 INSERT](/zh/polardb/features/epq/parallel-dml/) {{< badge text="V11 / v1.1.17-" tone="info" >}}

### 第三方插件 {#第三方插件}

- [pgvector](/zh/polardb/features/extensions/pgvector/) {{< badge text="V11 / v1.1.35-" tone="info" >}}
- [smlar](/zh/polardb/features/extensions/smlar/) {{< badge text="V11 / v1.1.28-" tone="info" >}}

### 高性能 {#高性能}

- [预读 / 预扩展](/zh/polardb/features/performance/bulk-read-and-extend/) {{< badge text="V11 / v1.1.1-" tone="info" >}}
- [表大小缓存](/zh/polardb/features/performance/rel-size-cache/) {{< badge text="V11 / v1.1.10-" tone="info" >}}
- [Shared Server](/zh/polardb/features/performance/shared-server/) {{< badge text="V11 / v1.1.30-" tone="info" >}}

### 安全 {#安全}

- [polar_login_history 会话访问历史](/zh/polardb/features/security/polar_login_history/) {{< badge text="V15 / v15.12.4.0-" tone="info" >}}
- [TDE 透明数据加密](/zh/polardb/features/security/tde/) {{< badge text="V11 / v1.1.1-" tone="info" >}}
