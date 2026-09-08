---
title: 配置本地集群
weight: 3125
description: 配置本地集群进行测试和开发
categories: [教程]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/dev-guide/local_cluster.md"
aliases: [/etcd/dev-guide/local_cluster/]
---

对于测试和开发部署，最快捷简便的方式是配置本地集群。对于生产部署，请参考 [clustering][clustering] 章节。

## 本地独立集群 {#local-standalone-cluster}

### 启动集群 {#starting-a-cluster}

运行以下命令以将 etcd 集群部署为独立集群：

```
$ ./etcd
...
```

如果 `etcd` 二进制文件不在当前工作目录中，它可能位于 `$GOPATH/bin/etcd` 或 `/usr/local/bin/etcd`。请相应地运行命令。

运行中的 etcd 成员在 `localhost:2379` 上监听客户端请求。

### 与集群交互 {#interacting-with-the-cluster}

使用 `etcdctl` 与运行中的集群交互：

1. 在集群中存储一个示例键值对：

    ```
      $ ./etcdctl put foo bar
      OK
    ```

    如果输出 OK，表示键值对已成功存储。

2. 获取 `foo` 的值：

    ```
    $ ./etcdctl get foo
    bar
    ```

    如果返回 `bar`，表示可正常与 etcd 集群交互。

## 本地多成员集群 {#local-multi-member-cluster}

### 启动集群 {#starting-a-cluster-1}

在 etcd 代码仓库根目录下提供了一个 `Procfile`，用于便捷地配置本地多成员集群。要启动多成员集群，请进入 etcd 源码根目录并执行以下操作：

1. 安装 `goreman` 以控制基于 Procfile 的应用程序：

    ```
    $ go install github.com/mattn/goreman@latest
    ```

2. 使用 `goreman` 和 etcd 的默认 Procfile 启动集群：

    ```
    $ goreman -f Procfile start
    ```

    各成员启动后，分别在 `localhost:2379`、`localhost:22379` 和 `localhost:32379` 上监听客户端请求。

### 与集群交互 {#interacting-with-the-cluster-1}

使用 `etcdctl` 与运行中的集群交互：

1. 打印成员列表：

    ```
    $ etcdctl --write-out=table --endpoints=localhost:2379 member list
    ```
    etcd 成员列表如下：

    ```
    +------------------+---------+--------+------------------------+------------------------+
    |        ID        | STATUS  |  NAME  |       PEER ADDRS       |      CLIENT ADDRS      |
    +------------------+---------+--------+------------------------+------------------------+
    | 8211f1d0f64f3269 | started | infra1 | http://127.0.0.1:2380  | http://127.0.0.1:2379  |
    | 91bc3c398fb3c146 | started | infra2 | http://127.0.0.1:22380 | http://127.0.0.1:22379 |
    | fd422379fda50e48 | started | infra3 | http://127.0.0.1:32380 | http://127.0.0.1:32379 |
    +------------------+---------+--------+------------------------+------------------------+
    ```

2. 在集群中存储一个示例键值对：

    ```
    $ etcdctl put foo bar
    OK
    ```

    如果输出 OK，表示键值对已成功存储。

### 测试容错能力 {#testing-fault-tolerance}

为验证 etcd 的容错能力，请终止一个成员，并尝试获取键。

1. 确定待停止成员的进程名称。

    `Procfile` 列出了多成员集群的属性。以进程名为 `etcd2` 的成员为例。

2. 停止成员：

    ```
    # kill etcd2
    $ goreman run stop etcd2
    ```

3. 存储键：

    ```
    $ etcdctl put key hello
    OK
    ```

4. 检索上一步存储的键：

    ```
    $ etcdctl get key
    hello
    ```

5. 从已停止的成员中检索键：

    ```
    $ etcdctl --endpoints=localhost:22379 get key
    ```

    该命令应显示由连接失败引起的错误：

    ```
    2017/06/18 23:07:35 grpc: Conn.resetTransport failed to create client transport: connection error: desc = "transport: dial tcp 127.0.0.1:22379: getsockopt: connection refused"; Reconnecting to "localhost:22379"
    Error:  grpc: timed out trying to connect
    ```
6. 重启已停止的成员：

    ```
    $ goreman run restart etcd2
    ```

7. 从重启后的成员获取键：

    ```
    $ etcdctl --endpoints=localhost:22379 get key
    hello
    ```

    重启成员后会重新建立连接，`etcdctl` 现在应能成功获取该键。如需详细了解如何与 etcd 交互，请参阅[与 etcd 交互][interacting]。

[clustering]: /zh/docs/etcd/op-guide/clustering/
[interacting]: /zh/docs/etcd/dev-guide/interacting_v3/
