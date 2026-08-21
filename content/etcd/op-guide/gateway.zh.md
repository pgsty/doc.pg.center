---
title: etcd 网关
weight: 4300
description: etcd 网关的使用场景及配置方法
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/a9ee660fdbf9584deb4af639c4dc63b01413e44f/content/en/docs/v3.7/op-guide/gateway.md"
---

## etcd 网关是什么 {#what-is-etcd-gateway}

etcd 网关是一个简单的 TCP 代理，负责将网络数据转发至 etcd 集群。网关为无状态且透明的；它既不检查客户端请求，也不干扰集群响应。网关不会终止 TLS 连接，不会代表客户端执行 TLS 握手，也不会验证连接是否已加密。

网关支持多个 etcd 服务器端点，并采用简单的轮询策略。它仅将请求路由至可用端点，并向客户端隐藏故障。未来可能支持其他重试策略，例如加权轮询。

## 何时使用 etcd 网关 {#when-to-use-etcd-gateway}

每个访问 etcd 的应用程序都必须首先知晓 etcd 集群客户端端点的地址。如果同一服务器上的多个应用程序访问同一个 etcd 集群，每个应用程序仍需知晓 etcd 集群的通告客户端端点。如果 etcd 集群重新配置为使用不同的端点，每个应用程序也可能需要更新其端点列表。这种大规模的重新配置既繁琐又容易出错。

etcd 网关通过作为稳定的本地端点来解决此问题。典型的 etcd 网关配置中，每台机器上运行一个监听本地地址的网关，每个 etcd 应用程序连接到其本地网关。结果是，只需更新网关的端点，而无需逐一更新每个应用程序。

综上所述，为自动传播集群端点变更，etcd 网关需在每台运行多个访问同一 etcd 集群的应用程序的机器上运行。

## 何时不应使用 etcd 网关 {#when-not-to-use-etcd-gateway}

- 提升性能

网关并非用于提升 etcd 集群性能。它不提供缓存、监听合并或批处理功能。etcd 团队正在开发一种用于提升集群可扩展性的缓存代理。

- 在集群管理系统上运行

高级集群管理系统（如 Kubernetes）原生支持服务发现。应用程序可通过系统管理的 DNS 名称或虚拟 IP 地址访问 etcd 集群。例如，kube-proxy 相当于 etcd 网关。

## 启动 etcd 网关 {#start-etcd-gateway}

考虑一个具有以下静态端点的 etcd 集群：

| 名称 | 地址 | 主机名 | 端口 |
|------|---------|------------------|----|
| infra0 | 10.0.1.10 | infra0.example.com | 2379 |
| infra1 | 10.0.1.11 | infra1.example.com | 2379 |
| infra2 | 10.0.1.12 | infra2.example.com | 2379 |

使用以下命令启动 etcd 网关，以通过静态端点进行访问：

```bash
$ etcd gateway start --endpoints=infra0.example.com:2379,infra1.example.com:2379,infra2.example.com:2379
2016-08-16 11:21:18.867350 I | tcpproxy: ready to proxy client requests to [...]
```

或者，若使用 DNS 进行服务发现，请考虑使用 DNS SRV 记录：

```bash
$ dig +noall +answer SRV _etcd-client._tcp.example.com
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra0.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra1.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra2.example.com.
```

```bash
$ dig +noall +answer infra0.example.com infra1.example.com infra2.example.com
infra0.example.com.  300  IN  A  10.0.1.10
infra1.example.com.  300  IN  A  10.0.1.11
infra2.example.com.  300  IN  A  10.0.1.12
```

使用以下命令启动 etcd 网关，从 DNS SRV 条目中获取端点：

```bash
$ etcd gateway start --discovery-srv=example.com
2016-08-16 11:21:18.867350 I | tcpproxy: ready to proxy client requests to [...]
```

## 配置标志 {#configuration-flags}

### etcd 集群 {#etcd-cluster}

#### --endpoints {#endpoints}

* 用逗号分隔的 etcd 服务器端点列表，用于转发客户端连接。
* 默认值：`127.0.0.1:2379`
* 必须包含端口。
* 无效示例：`https://127.0.0.1:2379`（网关不终止 TLS）。请注意，网关不会验证 HTTP 协议模式或检查请求内容，仅将请求转发至指定端点。

#### --discovery-srv {#discovery-srv}

* 用于通过 SRV 记录引导集群端点的 DNS 域名。
* 默认值：未设置

### 网络 {#network}

#### --listen-addr {#listen-addr}

* 用于接收客户端请求的接口和端口。
* 默认值：`127.0.0.1:23790`

#### --retry-delay {#retry-delay}

* 重试连接已失败端点前的延迟时长。
* 默认值：1m0s
* 无效示例："123"（期望以时间单位格式提供）

### 安全 {#security}

#### --insecure-discovery {#insecure-discovery}

* 接受不安全或易受中间人攻击的 SRV 记录。
* 默认值：`false`

#### --trusted-ca-file {#trusted-ca-file}

* 客户端 TLS CA 文件路径，用于 etcd 集群验证 SRV 发现返回的端点。请注意，该设置仅用于认证发现的端点，而非用于数据传输的连接建立。网关不会终止 TLS 连接，也不会代表客户端创建 TLS 连接。
* 默认值：未设置
