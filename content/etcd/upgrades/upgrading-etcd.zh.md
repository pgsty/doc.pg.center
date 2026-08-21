---
title: 升级 etcd 集群与应用程序
weight: 6500
description: 升级 etcd 集群和应用程序的文档列表
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/a9ee660fdbf9584deb4af639c4dc63b01413e44f/content/en/docs/v3.7/upgrades/upgrading-etcd.md"
---

本节包含与升级 etcd 集群及应用程序相关的特定文档。

## 升级策略 {#upgrade-policy}

升级前请注意，etcd 仅支持以下两种升级场景：

* **补丁升级**：在同一小版本内升级补丁版本（例如 3.7.0 至 3.7.1）。
* **小版本升级**：每次仅升级一个次版本（例如 3.6 至 3.7）。不支持跳过次版本的升级，此类操作很可能失败。请在升级至下一个次版本前，先更新至最新补丁版本。

## 升级 etcd v3.x 集群 {#upgrading-an-etcd-v3x-cluster}

* [将 etcd 从 3.0 升级至 3.1](/zh/etcd/upgrades/upgrade_3_1/)
* [将 etcd 从 3.1 升级至 3.2](/zh/etcd/upgrades/upgrade_3_2/)
* [将 etcd 从 3.2 升级至 3.3](/zh/etcd/upgrades/upgrade_3_3/)
* [将 etcd 从 3.3 升级至 3.4](/zh/etcd/upgrades/upgrade_3_4/)
* [将 etcd 从 3.4 升级至 3.5](/zh/etcd/upgrades/upgrade_3_5/)
* [将 etcd 从 3.5 升级至 3.6](/zh/etcd/upgrades/upgrade_3_6/)
* [将 etcd 从 3.6 升级至 3.7](/zh/etcd/upgrades/upgrade_3_7/)

## 升级至 etcd v2.3 {#upgrading-from-etcd-v23}

* [将 v2.3 集群升级至 v3.0](/zh/etcd/upgrades/upgrade_3_0/)
