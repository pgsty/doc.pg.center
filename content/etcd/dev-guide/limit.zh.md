---
title: 系统限制
weight: 3625
description: "etcd 限制：请求与存储系统"
categories: [参考]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/limit.md"
---

## 请求大小限制 {#request-size-limit}

etcd 专为处理典型的元数据类小规模键值对而设计。虽然较大请求也能正常工作，但可能增加其他请求的延迟。默认情况下，单个请求的大小上限为 1.5 MiB。此限制可通过 etcd 服务器的 `--max-request-bytes` 标志进行配置。

## 存储容量限制 {#storage-size-limit}

默认存储大小限制为 2 GiB，可通过 `--quota-backend-bytes` 标志进行配置。在常规环境中，建议最大大小为 8 GiB，若配置值超过此限制，etcd 在启动时会发出警告。
