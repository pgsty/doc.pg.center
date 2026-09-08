---
title: 集群指南
weight: 4150
description: "配置 etcd 集群：静态配置、etcd 发现和 DNS 发现"
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/op-guide/clustering.md"
aliases: [/etcd/op-guide/clustering/]
---

## 概述 {#overview}

静态启动 etcd 集群要求每个成员均知晓集群中的其他成员。在某些情况下，集群成员的 IP 地址可能无法提前确定。在这些情况下，可以借助发现服务来引导启动 etcd 集群。

一旦 etcd 集群启动并运行，添加或移除成员需通过 [运行时重配置][runtime-conf]完成。为更好地理解运行时重配置的设计原理，建议阅读 [运行时配置设计文档][runtime-reconf-design]。

本文将介绍用于引导 etcd 集群的以下机制：

* [静态](#static)
* [etcd 发现](#etcd-discovery)
* [DNS 发现](#dns-discovery)

每个引导机制将用于创建一个由三台机器组成的 etcd 集群，具体细节如下：

| 名称 | 地址 | 主机名 |
|------|---------|------------------|
| infra0 | 10.0.1.10 | infra0.example.com |
| infra1 | 10.0.1.11 | infra1.example.com |
| infra2 | 10.0.1.12 | infra2.example.com |

## 静态 {#static}

如已知晓集群成员、其地址及集群规模，可在启动前通过设置 `initial-cluster` 标志使用离线引导配置。每台机器将获取以下任一环境变量或命令行参数：

```
ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380"
ETCD_INITIAL_CLUSTER_STATE=new
```

```
--initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
--initial-cluster-state new
```

请注意，`initial-cluster` 中指定的 URL 是 _已通告的对等成员 URL_，即它们应与相应节点上 `initial-advertise-peer-urls` 的值匹配。

若为测试目的而启动多个集群（或创建并销毁单个集群），强烈建议为每个集群分配一个唯一的 `initial-cluster-token`。通过此操作，即使各集群配置完全相同，etcd 仍可为各集群生成唯一的集群 ID 和成员 ID。此举可防止集群间相互干扰，避免造成集群数据损坏。

etcd 在 [`listen-client-urls`][conf-listen-client] 监听以接收客户端流量。etcd 成员会向其他成员、代理和客户端通告 [`advertise-client-urls`][conf-adv-client] 中指定的 URL。请注意，`advertise-client-urls` 必须对目标客户端可达。常见错误是将 `advertise-client-urls` 设置为 localhost，或在远程客户端需访问 etcd 时未更改默认值。

在每台机器上，使用以下标志启动 etcd：

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state new
```
```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls http://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state new
```
```
$ etcd --name infra2 --initial-advertise-peer-urls http://10.0.1.12:2380 \
  --listen-peer-urls http://10.0.1.12:2380 \
  --listen-client-urls http://10.0.1.12:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.12:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state new
```

以 `--initial-cluster` 开头的命令行参数在 etcd 的后续运行中将被忽略。引导过程完成后，可自由移除环境变量或命令行标志。如需后续修改配置（例如向集群中添加或移除成员），请参阅 [runtime configuration][runtime-conf] 指南。

### TLS {#tls}

etcd 通过 TLS 协议支持加密通信。TLS 通道可用于对等成员之间的集群内部加密通信，也可用于客户端流量的加密。本节提供配置启用对等成员和客户端 TLS 的集群示例。有关 etcd TLS 支持的更多详细信息，请参阅 [security guide][security-guide]。

#### 自签名证书 {#self-signed-certificates}

使用自签名证书的集群可同时实现流量加密和连接身份认证。要启动使用自签名证书的集群，每个集群成员应拥有唯一的密钥对（`member.crt`、`member.key`），并由共享的集群 CA 证书（`ca.crt`）分别对对等成员连接和客户端连接的证书进行签名。证书可通过参考 etcd [TLS 设置][tls-setup] 示例生成。

在每台机器上，etcd 将使用以下标志启动：

```
$ etcd --name infra0 --initial-advertise-peer-urls https://10.0.1.10:2380 \
  --listen-peer-urls https://10.0.1.10:2380 \
  --listen-client-urls https://10.0.1.10:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.10:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --client-cert-auth --trusted-ca-file=/path/to/ca-client.crt \
  --cert-file=/path/to/infra0-client.crt --key-file=/path/to/infra0-client.key \
  --peer-client-cert-auth --peer-trusted-ca-file=ca-peer.crt \
  --peer-cert-file=/path/to/infra0-peer.crt --peer-key-file=/path/to/infra0-peer.key
```
```
$ etcd --name infra1 --initial-advertise-peer-urls https://10.0.1.11:2380 \
  --listen-peer-urls https://10.0.1.11:2380 \
  --listen-client-urls https://10.0.1.11:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.11:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --client-cert-auth --trusted-ca-file=/path/to/ca-client.crt \
  --cert-file=/path/to/infra1-client.crt --key-file=/path/to/infra1-client.key \
  --peer-client-cert-auth --peer-trusted-ca-file=ca-peer.crt \
  --peer-cert-file=/path/to/infra1-peer.crt --peer-key-file=/path/to/infra1-peer.key
```
```
$ etcd --name infra2 --initial-advertise-peer-urls https://10.0.1.12:2380 \
  --listen-peer-urls https://10.0.1.12:2380 \
  --listen-client-urls https://10.0.1.12:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.12:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --client-cert-auth --trusted-ca-file=/path/to/ca-client.crt \
  --cert-file=/path/to/infra2-client.crt --key-file=/path/to/infra2-client.key \
  --peer-client-cert-auth --peer-trusted-ca-file=ca-peer.crt \
  --peer-cert-file=/path/to/infra2-peer.crt --peer-key-file=/path/to/infra2-peer.key
```

#### 自动证书管理 {#automatic-certificates}

如果集群需要加密通信但不需要身份认证连接，etcd 可配置为自动为其生成密钥。在初始化时，每个成员会根据其通告的 IP 地址和主机名自动生成一组密钥。

在每台机器上，etcd 将使用以下标志启动：

```
$ etcd --name infra0 --initial-advertise-peer-urls https://10.0.1.10:2380 \
  --listen-peer-urls https://10.0.1.10:2380 \
  --listen-client-urls https://10.0.1.10:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.10:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --auto-tls \
  --peer-auto-tls
```
```
$ etcd --name infra1 --initial-advertise-peer-urls https://10.0.1.11:2380 \
  --listen-peer-urls https://10.0.1.11:2380 \
  --listen-client-urls https://10.0.1.11:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.11:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --auto-tls \
  --peer-auto-tls
```
```
$ etcd --name infra2 --initial-advertise-peer-urls https://10.0.1.12:2380 \
  --listen-peer-urls https://10.0.1.12:2380 \
  --listen-client-urls https://10.0.1.12:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.12:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --auto-tls \
  --peer-auto-tls
```

### 错误案例 {#error-cases}

在以下示例中，我们未将新主机包含在已枚举节点的列表中。如果这是一个新集群，该节点必须添加到初始集群成员列表中。

```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls https://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --initial-cluster infra0=http://10.0.1.10:2380 \
  --initial-cluster-state new
etcd: infra1 not listed in the initial cluster config
exit 1
```

在此示例中，我们尝试将一个节点（infra0）映射到与其在集群列表中枚举的地址（10.0.1.10:2380）不同的地址（127.0.0.1:2380）。如果该节点需监听多个地址，则所有地址 _必须_ 在 "initial-cluster" 配置指令中反映出来。

```
$ etcd --name infra0 --initial-advertise-peer-urls http://127.0.0.1:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state=new
etcd: error setting up initial cluster: infra0 has different advertised URLs in the cluster and advertised peer URLs list
exit 1
```

如果对等成员使用了不同的配置参数集并尝试加入此集群，etcd 将报告集群 ID 不匹配并退出。

```
$ etcd --name infra3 --initial-advertise-peer-urls http://10.0.1.13:2380 \
  --listen-peer-urls http://10.0.1.13:2380 \
  --listen-client-urls http://10.0.1.13:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.13:2379 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra3=http://10.0.1.13:2380 \
  --initial-cluster-state=new
etcd: conflicting cluster ID to the target cluster (c6ab534d07e8fcc4 != bc25ea2a74fb18b0). Exiting.
exit 1
```

## 发现 {#discovery}

在多种情况下，集群对等成员的 IP 地址可能无法提前知晓。这在使用云服务提供商或网络采用 DHCP 时较为常见。在这种情况下，应避免指定静态配置，而是利用现有的 etcd 集群来引导新集群。此过程称为“发现”。

有两种可用于发现的方法：

* etcd 发现服务
* DNS SRV 记录

### etcd 发现 {#etcd-discovery}

为更好地理解发现服务协议的设计，建议阅读发现服务协议 [documentation][discovery-proto]。

#### 发现 URL 的生命周期 {#lifetime-of-a-discovery-url}

发现 URL 用于标识一个唯一的 etcd 集群。每个 etcd 实例应共享一个新的发现 URL，以引导新集群，而非复用现有的发现 URL。

此外，发现 URL 仅可用于集群的初始引导。若需在集群运行后更改集群成员关系，请参阅 [运行时重配置][runtime-conf] 指南。

#### 自定义 etcd 发现服务 {#custom-etcd-discovery-service}

发现机制通过现有的集群来引导自身。若使用私有 etcd 集群，请按如下方式创建 URL：

```
$ curl -X PUT https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83/_config/size -d value=3
```

通过将 size 键设置为 URL，可创建一个预期集群大小为 3 的发现 URL。

此情况下使用的 URL 为 `https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83`，etcd 成员在启动时将使用 `https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83` 目录进行注册。

**每个成员必须指定不同的名称标志。`Hostname` 或 `machine-id` 是不错的选择。否则，由于名称重复，发现将失败。**

现在我们为每个成员启动 etcd，并设置相关标志：

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
```
```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls http://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --discovery https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
```
```
$ etcd --name infra2 --initial-advertise-peer-urls http://10.0.1.12:2380 \
  --listen-peer-urls http://10.0.1.12:2380 \
  --listen-client-urls http://10.0.1.12:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.12:2379 \
  --discovery https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
```

这将导致每个成员向自定义的 etcd 发现服务注册自身，并在所有机器完成注册后启动集群。

#### 公共 etcd 发现服务 {#public-etcd-discovery-service}

如果无可用的现有集群，可使用托管在 `discovery.etcd.io` 的公共发现服务。若要使用“new”端点创建私有发现 URL，请使用以下命令：

```
$ curl https://discovery.etcd.io/new?size=3
https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

这将创建一个初始大小为 3 个成员的集群。若未指定大小，则默认使用 3。

```
ETCD_DISCOVERY=https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

```
--discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

**每个成员必须指定不同的名称标志，否则由于名称重复，发现将失败。`Hostname` 或 `machine-id` 是不错的选择。**

现在我们为每个成员启动 etcd，并设置相关标志：

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```
```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls http://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```
```
$ etcd --name infra2 --initial-advertise-peer-urls http://10.0.1.12:2380 \
  --listen-peer-urls http://10.0.1.12:2380 \
  --listen-client-urls http://10.0.1.12:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.12:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

这将导致每个成员向发现服务注册自身，并在所有成员注册完成后启动集群。

使用环境变量 `ETCD_DISCOVERY_PROXY` 可使 etcd 通过 HTTP 代理连接发现服务。

#### 错误和警告情况 {#error-and-warning-cases}

##### 发现服务器错误 {#discovery-server-errors}


```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
etcd: error: the cluster doesn’t have a size configuration value in https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de/_config
exit 1
```

##### 警告 {#warnings}

这是一个无害的警告，表示此机器将忽略发现 URL。

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
etcdserver: discovery token ignored since a cluster has already been initialized. Valid log found at /var/lib/etcd
```

### DNS 发现 {#dns-discovery}

DNS [SRV 记录][rfc-srv] 可用作发现机制。`--discovery-srv` 标志可用于设置发现 SRV 记录所在的 DNS 域名。
设置 `--discovery-srv example.com` 会导致按列出的顺序查找 DNS SRV 记录：

* _etcd-server-ssl._tcp.example.com
* _etcd-server._tcp.example.com

如果发现 `_etcd-server-ssl._tcp.example.com`，etcd 将尝试通过 TLS 执行引导过程。

为帮助客户端发现 etcd 集群，将按以下顺序查找下列 DNS SRV 记录：

* _etcd-client._tcp.example.com
* _etcd-client-ssl._tcp.example.com

如果发现 `_etcd-client-ssl._tcp.example.com`，客户端将尝试通过 SSL/TLS 与 etcd 集群通信。

如果 etcd 使用 TLS，发现 SRV 记录（例如 `example.com`）必须包含在 SSL 证书的 DNS SAN 中，且需与主机名一同列出，否则集群化将失败，并出现如下日志消息：

```
[...] rejected connection from "10.0.1.11:53162" (error "remote error: tls: bad certificate", ServerName "example.com")
```

如果 etcd 使用 TLS 但未使用自定义证书颁发机构，则发现域名（例如 example.com）必须与 SRV 记录域名（例如 infra1.example.com）匹配。此举旨在防范伪造 SRV 记录指向其他域名的攻击；若域名匹配，即使该域名在 PKI 下拥有有效证书，也不会被未知第三方控制。

`-discovery-srv-name` 标志还可配置在发现过程中查询的 SRV 名称后缀。
使用此标志可在同一域名下区分多个 etcd 集群。
例如，若 `discovery-srv=example.com` 和 `-discovery-srv-name=foo` 均已设置，则会执行以下 DNS SRV 查询：

* _etcd-server-ssl-foo._tcp.example.com
* _etcd-server-foo._tcp.example.com

#### 创建 DNS SRV 记录 {#create-dns-srv-records}

```
$ dig +noall +answer SRV _etcd-server._tcp.example.com
_etcd-server._tcp.example.com. 300 IN  SRV  0 0 2380 infra0.example.com.
_etcd-server._tcp.example.com. 300 IN  SRV  0 0 2380 infra1.example.com.
_etcd-server._tcp.example.com. 300 IN  SRV  0 0 2380 infra2.example.com.
```

```
$ dig +noall +answer SRV _etcd-client._tcp.example.com
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra0.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra1.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra2.example.com.
```

```
$ dig +noall +answer infra0.example.com infra1.example.com infra2.example.com
infra0.example.com.  300  IN  A  10.0.1.10
infra1.example.com.  300  IN  A  10.0.1.11
infra2.example.com.  300  IN  A  10.0.1.12
```

#### 使用 DNS 引导 etcd 集群 {#bootstrap-the-etcd-cluster-using-dns}

etcd 集群成员可通告域名或 IP 地址，引导过程将解析 DNS A 记录。
自 3.2 版本起（3.1 版本会打印警告）`--listen-peer-urls` 和 `--listen-client-urls` 将拒绝为网络接口绑定使用域名。

`--initial-advertise-peer-urls` 中解析出的地址必须与 SRV 目标中的任一解析地址匹配。etcd 成员会读取解析地址，以判断其是否属于 SRV 记录中定义的集群。

```
$ etcd --name infra0 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://infra0.example.com:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://infra0.example.com:2379 \
--listen-client-urls http://0.0.0.0:2379 \
--listen-peer-urls http://0.0.0.0:2380
```

```
$ etcd --name infra1 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://infra1.example.com:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://infra1.example.com:2379 \
--listen-client-urls http://0.0.0.0:2379 \
--listen-peer-urls http://0.0.0.0:2380
```

```
$ etcd --name infra2 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://infra2.example.com:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://infra2.example.com:2379 \
--listen-client-urls http://0.0.0.0:2379 \
--listen-peer-urls http://0.0.0.0:2380
```

集群也可使用 IP 地址而非域名进行引导：

```
$ etcd --name infra0 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://10.0.1.10:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://10.0.1.10:2379 \
--listen-client-urls http://10.0.1.10:2379 \
--listen-peer-urls http://10.0.1.10:2380
```

```
$ etcd --name infra1 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://10.0.1.11:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://10.0.1.11:2379 \
--listen-client-urls http://10.0.1.11:2379 \
--listen-peer-urls http://10.0.1.11:2380
```

```
$ etcd --name infra2 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://10.0.1.12:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://10.0.1.12:2379 \
--listen-client-urls http://10.0.1.12:2379 \
--listen-peer-urls http://10.0.1.12:2380
```

自 v3.1.0 版本起（v3.2.9 除外），当 `etcd --discovery-srv=example.com` 配置了 TLS 时，服务器仅在提供的证书中包含根域名 `example.com` 作为主题备用名称（SAN）字段的条目时，才会对对等成员/客户端进行身份认证。参见 [DNS SRV 说明][security-guide-dns-srv]。

### 网关 {#gateway}

etcd 网关是一个简单的 TCP 代理，用于将网络数据转发至 etcd 集群。请参阅 [网关指南][gateway] 以获取更多信息。

### 代理 {#proxy}

当设置 `--proxy` 标志时，etcd 以 [代理模式][proxy] 运行。该代理模式仅支持 etcd v2 API；目前无计划支持 v3 API。对于 v3 API 支持，将在 etcd 3.0 发布后推出具备增强功能的新代理。

要使用 v2 API 代理搭建 etcd 集群，请阅读 etcd 2.3 版本发布中的 [集群化文档][clustering_etcd2]。

[clustering_etcd2]: https://github.com/etcd-io/etcd/blob/release-2.3/Documentation/clustering.md
[conf-adv-client]: /zh/docs/etcd/op-guide/configuration/#clustering
[conf-listen-client]: /zh/docs/etcd/op-guide/configuration/#member
[discovery-proto]: /zh/docs/etcd/dev-internal/discovery_protocol/
[gateway]: /zh/docs/etcd/op-guide/gateway/
[proxy]: https://github.com/etcd-io/etcd/blob/release-2.3/Documentation/proxy.md
[rfc-srv]: http://www.ietf.org/rfc/rfc2052.txt
[runtime-conf]: /zh/docs/etcd/op-guide/runtime-configuration/
[runtime-reconf-design]: /zh/docs/etcd/op-guide/runtime-reconf-design/
[security-guide-dns-srv]: /zh/docs/etcd/op-guide/security/#notes-for-dns-srv
[security-guide]: /zh/docs/etcd/op-guide/security/
[tls-setup]: https://github.com/etcd-io/etcd/tree/main/hack/tls-setup
