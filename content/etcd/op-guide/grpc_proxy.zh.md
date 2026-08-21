---
title: gRPC 代理
weight: 4350
description: 一个无状态的 etcd 代理，运行在 gRPC 层
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/a9ee660fdbf9584deb4af639c4dc63b01413e44f/content/en/docs/v3.7/op-guide/grpc_proxy.md"
---

gRPC 代理是运行在 gRPC 层（L7）的无状态 etcd 反向代理。该代理旨在降低核心 etcd 集群的总体处理负载。为实现横向扩展，代理会合并监听和租约 API 请求。为防止恶意客户端对集群造成影响，代理会缓存键范围请求。

gRPC 代理支持多个 etcd 服务器端点。代理启动时，会随机选择一个 etcd 服务器端点使用。该端点将处理所有请求，直至代理检测到端点故障。若 gRPC 代理检测到端点故障，且存在其他可用端点，则会切换至其他端点，以向客户端隐藏故障。未来可能支持其他重试策略，例如加权轮询。

## 可扩展的监听 API {#scalable-watch-api}

gRPC 代理将同一键或范围上的多个客户端监听器（`c-watchers`）合并为一个连接到 etcd 服务器的监听器（`s-watcher`）。代理将 `s-watcher` 的所有事件广播给其 `c-watchers`。

假设有 N 个客户端监听同一个键，一个 gRPC 代理可将 etcd 服务器的监听负载从 N 降低至 1。用户可部署多个 gRPC 代理以进一步分摊服务器负载。

在以下示例中，三个客户端监听键 A。gRPC 代理将这三个监听器合并为一个监听器，该监听器连接到 etcd 服务器。

```
            +-------------+
            | etcd server |
            +------+------+
                   ^ watch key A (s-watcher)
                   |
           +-------+-----+
           | gRPC proxy  | <-------+
           |             |         |
           ++-----+------+         |watch key A (c-watcher)
watch key A ^     ^ watch key A    |
(c-watcher) |     | (c-watcher)    |
    +-------+-+  ++--------+  +----+----+
    |  client |  |  client |  |  client |
    |         |  |         |  |         |
    +---------+  +---------+  +---------+
```

### 限制 {#limitations}

为有效将多个客户端监听器合并为单一监听器，gRPC 代理在可能的情况下会将新的 `c-watchers` 合并至现有的 `s-watcher`。由于网络延迟或缓冲未送达的事件，该合并后的 `s-watcher` 可能与 etcd 服务器不同步。当监听修订版本未指定时，gRPC 代理不能保证 `c-watcher` 会从最新的存储修订版本开始监听。例如，若客户端从修订版本为 1000 的 etcd 服务器进行监听，该监听器将从修订版本 1000 开始。若客户端从 gRPC 代理进行监听，可能从修订版本 990 开始监听。

取消操作也存在类似的限制。当监听器被取消时，etcd 服务器的修订版本可能大于取消响应的修订版本。

上述两项限制通常不会对大多数使用场景造成影响。未来可能会增加额外选项，以强制监听器绕过 gRPC 代理，从而获得更精确的修订版本响应。

## 可扩展的租约 API {#scalable-lease-api}

为保持租约有效，客户端必须至少建立一个 gRPC 流至 etcd 服务器，以发送周期性心跳。若 etcd 工作负载涉及大量租约操作且分布于多个客户端，这些流可能导致 CPU 利用率过高。为减少核心集群上的总流数，代理支持租约流合并。

假设有 N 个客户端在更新租约，单个 gRPC 代理可将 etcd 服务器的流负载从 N 降低至 1。部署中可增加额外的 gRPC 代理，以进一步将流分布到多个代理上。

在以下示例中，三个客户端分别更新三个独立的租约（`L1`、`L2` 和 `L3`）。gRPC 代理将这三个客户端的租约流（`c-streams`）合并为一个附加到 etcd 服务器的租约保活流（`s-stream`）。代理将客户端侧租约心跳从 c-流转发至 s-流，随后将响应返回至对应的 c-流。

```
          +-------------+
          | etcd server |
          +------+------+
                 ^
                 | heartbeat L1, L2, L3
                 | (s-stream)
                 v
         +-------+-----+
         | gRPC proxy  +<-----------+
         +---+------+--+            | heartbeat L3
             ^      ^               | (c-stream)
heartbeat L1 |      | heartbeat L2  |
(c-stream)   v      v (c-stream)    v
      +------+-+  +-+------+  +-----+--+
      | client |  | client |  | client |
      +--------+  +--------+  +--------+
```

## 客户端滥用防护 {#abusive-clients-protection}

gRPC 代理在不违反一致性要求的前提下，会缓存请求的响应。这可以防止在紧密循环中运行的恶意客户端对 etcd 服务器造成过载。

## 启动 etcd gRPC 代理 {#start-etcd-grpc-proxy}

考虑一个具有以下静态端点的 etcd 集群：

| 名称 | 地址 | 主机名 |
|------|---------|------------------|
| infra0 | 10.0.1.10 | infra0.example.com |
| infra1 | 10.0.1.11 | infra1.example.com |
| infra2 | 10.0.1.12 | infra2.example.com |

使用以下命令启动 etcd gRPC 代理，以通过这些静态端点进行访问：

```bash
$ etcd grpc-proxy start --endpoints=infra0.example.com,infra1.example.com,infra2.example.com --listen-addr=127.0.0.1:2379
```

etcd gRPC 代理启动并在端口 2379 上监听。它将客户端请求转发至上述三个端点中的一个。

通过代理发送请求：

```bash
$ ETCDCTL_API=3 etcdctl --endpoints=127.0.0.1:2379 put foo bar
OK
$ ETCDCTL_API=3 etcdctl --endpoints=127.0.0.1:2379 get foo
foo
bar
```

## 客户端端点同步与名称解析 {#client-endpoint-synchronization-and-name-resolution}

代理支持将端点注册至用户定义的发现端点，以供发现。此举具有两个目的。首先，它允许客户端将其端点与一组代理端点同步，以实现高可用性。其次，它是 etcd [gRPC 命名](/zh/etcd/dev-guide/grpc_naming/)的端点提供者。

通过提供用户自定义前缀来注册代理：

```bash
$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23790 \
  --advertise-client-url=127.0.0.1:23790 \
  --resolver-prefix="___grpc_proxy_endpoint" \
  --resolver-ttl=60

$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23791 \
  --advertise-client-url=127.0.0.1:23791 \
  --resolver-prefix="___grpc_proxy_endpoint" \
  --resolver-ttl=60
```

代理将列出其所有成员的成员列表：

```bash
ETCDCTL_API=3 etcdctl --endpoints=http://localhost:23790 member list --write-out table

+----+---------+--------------------------------+------------+-----------------+
| ID | STATUS  |              NAME              | PEER ADDRS |  CLIENT ADDRS   |
+----+---------+--------------------------------+------------+-----------------+
|  0 | started | Gyu-Hos-MBP.sfo.coreos.systems |            | 127.0.0.1:23791 |
|  0 | started | Gyu-Hos-MBP.sfo.coreos.systems |            | 127.0.0.1:23790 |
+----+---------+--------------------------------+------------+-----------------+
```

这使得客户端可通过 Sync 自动发现代理端点：

```go
cli, err := clientv3.New(clientv3.Config{
    Endpoints: []string{"http://localhost:23790"},
})
if err != nil {
    log.Fatal(err)
}
defer cli.Close()

// fetch registered grpc-proxy endpoints
if err := cli.Sync(context.Background()); err != nil {
    log.Fatal(err)
}
```

请注意，如果配置代理时未指定解析器前缀，

```bash
$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23792 \
  --advertise-client-url=127.0.0.1:23792
```

成员列表 API 通过 gRPC 代理返回其自身的 `advertise-client-url`：

```bash
ETCDCTL_API=3 etcdctl --endpoints=http://localhost:23792 member list --write-out table

+----+---------+--------------------------------+------------+-----------------+
| ID | STATUS  |              NAME              | PEER ADDRS |  CLIENT ADDRS   |
+----+---------+--------------------------------+------------+-----------------+
|  0 | started | Gyu-Hos-MBP.sfo.coreos.systems |            | 127.0.0.1:23792 |
+----+---------+--------------------------------+------------+-----------------+
```

## 命名空间 {#namespacing}

假设某个应用需要完全控制整个键空间，但 etcd 集群与其他应用共享。为使所有应用能够互不干扰地运行，代理可对 etcd 键空间进行分区，使客户端看似拥有对完整键空间的访问权限。当代理收到标志 `--namespace` 时，所有进入代理的客户端请求都会被转换，使键带上用户自定义的前缀。对 etcd 集群的访问将基于该前缀，而代理返回的响应会移除前缀；对客户端而言，似乎根本不存在前缀。

要为代理命名空间，请使用 `--namespace` 启动它：

```bash
$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23790 \
  --namespace=my-prefix/
```

对代理的访问现在已透明地在 etcd 集群上添加前缀：

```bash
$ ETCDCTL_API=3 etcdctl --endpoints=localhost:23790 put my-key abc
# OK
$ ETCDCTL_API=3 etcdctl --endpoints=localhost:23790 get my-key
# my-key
# abc
$ ETCDCTL_API=3 etcdctl --endpoints=localhost:2379 get my-prefix/my-key
# my-prefix/my-key
# abc
```

## TLS 终止 {#tls-termination}

通过 gRPC 代理终止安全 etcd 集群的 TLS，通过提供一个未加密的本地端点。

尝试操作，请使用客户端 HTTPS 启动单成员 etcd 集群：

```sh
$ etcd --listen-client-urls https://localhost:2379 --advertise-client-urls https://localhost:2379 --cert-file=peer.crt --key-file=peer.key --trusted-ca-file=ca.crt --client-cert-auth
```

确认客户端端口正在提供 HTTPS 服务：

```sh
# fails
$ ETCDCTL_API=3 etcdctl --endpoints=http://localhost:2379 endpoint status
# works
$ ETCDCTL_API=3 etcdctl --endpoints=https://localhost:2379 --cert=client.crt --key=client.key --cacert=ca.crt endpoint status
```

接下来，在 `localhost:12379` 上启动一个 gRPC 代理，通过客户端证书连接到 etcd 端点 `https://localhost:2379`：

```sh
$ etcd grpc-proxy start --endpoints=https://localhost:2379 --listen-addr localhost:12379 --cert client.crt --key client.key --cacert=ca.crt --insecure-skip-tls-verify &
```

最后，通过使用 HTTP 向代理写入键来测试 TLS 终止：

```sh
$ ETCDCTL_API=3 etcdctl --endpoints=http://localhost:12379 put abc def
# OK
```

## 指标与健康状况 {#metrics-and-health}

gRPC 代理为 `--endpoints` 定义的 etcd 成员暴露 `/health` 和 Prometheus `/metrics` 端点。可另定义一个额外的 URL，该 URL 将对 `/metrics` 和 `/health` 端点响应，并设置 `--metrics-addr` 标志。

```bash
$ etcd grpc-proxy start \
  --endpoints https://localhost:2379 \
  --metrics-addr https://0.0.0.0:4443 \
  --listen-addr 127.0.0.1:23790 \
  --key client.key \
  --key-file proxy-server.key \
  --cert client.crt \
  --cert-file proxy-server.crt \
  --cacert ca.pem \
  --trusted-ca-file proxy-ca.pem
 ```

### 已知问题 {#known-issue}

代理的主要接口同时支持 HTTP/2 和 HTTP/1.1。若如上例所示配置了 TLS，当使用 cURL 等客户端访问监听接口时，必须在请求中显式设置协议为 HTTP/1.1，才能返回 `/metrics` 或 `/health`。通过使用 `--metrics-addr` 标志，次要接口将不再具有此要求。

```bash
 $ curl --cacert proxy-ca.pem --key proxy-client.key --cert proxy-client.crt https://127.0.0.1:23790/metrics --http1.1
```
