---
title: 快速入门
weight: 900
description: 不到 5 分钟即可启动并运行 etcd！
icon: fa-solid fa-rocket
categories: [教程]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/quickstart.md"
---

按照以下步骤本地安装、运行并测试单成员 etcd 集群：

1. 从预构建的二进制文件或源码安装 etcd。详情请参见 [安装][]。

    > [!WARNING]
    > **重要**：务必完成安装说明的最后一步，确认可执行文件搜索路径中包含 `etcd`。

2. 启动 `etcd`：

    ```console
    $ etcd
    {"level":"info","ts":"2021-09-17T09:19:32.783-0400","caller":"etcdmain/etcd.go:72","msg":... }
    ⋮
    ```

    > [!NOTE]
    > **注意**：`etcd` 生成的输出包含 [日志](/zh/etcd/op-guide/configuration/#logging) &mdash; 信息级别日志可忽略。

3. 在**另一个终端**中，使用 `etcdctl` 设置键：

    ```console
    $ etcdctl put greeting "Hello, etcd"
    OK
    ```

4. 在同一终端中，检索键：

    ```console
    $ etcdctl get greeting
    greeting
    Hello, etcd
    ```

## 下一步？ {#whats-next}

从以下页面了解配置和使用 etcd 的更多方式：

- 如果你是开发者：
  - 探索 gRPC [API][]。
  - 查找 [语言绑定和工具][integrations]。

- 如果是运维人员或管理员：
  - 部署一个 [多机集群][clustering]。
  - 学习如何 [配置][] etcd。
  - 使用 TLS [保护 etcd 集群][security]。
  - [调优 etcd][tuning]。

[api]: /zh/etcd/learning/api
[clustering]: /zh/etcd/op-guide/clustering
[configure]: /zh/etcd/op-guide/configuration
[integrations]: /zh/etcd/integrations
[security]: /zh/etcd/op-guide/security
[tuning]: /zh/etcd/tuning
[Install]: /zh/etcd/install/
