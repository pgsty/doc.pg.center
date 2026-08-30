---
title: 版本管理
weight: 4900
description: etcd 的版本支持
categories: [概念]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/op-guide/versioning.md"
---

本文描述了 etcd 项目所支持的版本。

## 服务版本管理与支持版本 {#service-versioning-and-supported-versions}

etcd 版本号采用 **x.y.z** 格式，其中 **x** 表示主版本号，**y** 表示次版本号，**z** 表示补丁版本号，遵循 [语义化版本控制](https://semver.org/)规范。
新次版本号可能向 API 添加额外功能。

etcd 项目为当前版本及前一个版本维护发布分支。例如，当 v3.5 为当前版本时，v3.4 仍受支持。当 v3.6 发布后，v3.4 即停止支持。

根据严重性和可行性，适用于这两个发布分支的修复（包括安全修复）可能被回溯应用。
必要时，将从这些分支中发布补丁版本。

项目 [Maintainers](https://github.com/etcd-io/etcd/blob/main/OWNERS) 拥有此决策权。

可以使用 `etcdctl` 检查正在运行的 etcd 集群版本：

```sh
etcdctl --endpoints=127.0.0.1:2379 endpoint status
```

## API 版本管理 {#api-versioning}

`v3` API 的响应结果在 3.0.0 版本发布后不应发生变化，但后续将陆续增加新功能。
