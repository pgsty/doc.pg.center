---
title: 快速入门
weight: 900
description: 不到 5 分钟即可启动并运行 etcd！
icon: fa-solid fa-rocket
categories: [教程]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/quickstart.md"
aliases: [/etcd/quickstart/]
---

按照以下步骤本地安装、运行并测试单成员 etcd 集群：

1. 从预构建的二进制文件或源码安装 etcd。详情请参见 [安装][Install]。

    > [!WARNING]
    > **重要**：务必完成安装说明的最后一步，确认可执行文件搜索路径中包含 `etcd`。

2. 启动 `etcd`：

    ```console
    $ etcd
    {"level":"info","ts":"2021-09-17T09:19:32.783-0400","caller":"etcdmain/etcd.go:72","msg":... }
    ⋮
    ```

    > [!NOTE]
    > **注意**：`etcd` 生成的输出为 [日志](/zh/docs/etcd/op-guide/configuration/#logging) &mdash; 信息级别日志可忽略。

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
  - 学习如何 [配置][configure] etcd。
  - 使用 TLS [保护 etcd 集群][security]。
  - [调优 etcd][tuning]。

[api]: /zh/docs/etcd/learning/api
[clustering]: /zh/docs/etcd/op-guide/clustering
[configure]: /zh/docs/etcd/op-guide/configuration
[integrations]: /zh/docs/etcd/integrations
[security]: /zh/docs/etcd/op-guide/security
[tuning]: /zh/docs/etcd/tuning
[Install]: /zh/docs/etcd/install/
