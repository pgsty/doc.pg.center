---
title: 功能门控
weight: 1175
icon: fa-solid fa-toggle-on
categories: [参考]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/feature-gates/index.md"
aliases: [/etcd/feature-gates/]
---

<!-- overview -->
本文概述了管理员可在 etcd 中指定的各种功能门控。

请参阅 [特性阶段](#feature-stages) 了解功能各阶段的说明。

<!-- body -->
## 概述 {#overview}

功能门控是一组描述 etcd 特性的 key=value 键值对。
可使用 etcd 的 `--feature-gates` 命令行标志来开启或关闭这些特性。

etcd 允许启用或禁用一组功能门控。
使用 `-h` 标志查看全部功能门控列表。
要设置功能门控，请使用 `--feature-gates` 标志，并在命令行中指定功能对的列表：

```shell
--feature-gates=...,StopGRPCServiceOnDefrag=true
```

或在 YAML 配置文件中指定 `feature-gates`：

```shell
feature-gates: ...,StopGRPCServiceOnDefrag=true
```

### 变更 `embed.Config` 结构体 {#change-in-embedetcdserver-struct}

在 3.6 版本中，字段 `ServerFeatureGate` 被添加至 `embed.Config`，应取代以下实验性字段：

```diff
package embed

type Config struct {
  // Deprecated: Use CompactHashCheck Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalCompactHashCheckEnabled bool `json:"experimental-compact-hash-check-enabled"`

  // Deprecated: Use InitialCorruptCheck Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalInitialCorruptCheck bool `json:"experimental-initial-corrupt-check"`

  // Deprecated: Use TxnModeWriteWithSharedBuffer Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalTxnModeWriteWithSharedBuffer bool `json:"experimental-txn-mode-write-with-shared-buffer"`

  // Deprecated: Use StopGRPCServiceOnDefrag Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalStopGRPCServiceOnDefrag bool `json:"experimental-stop-grpc-service-on-defrag"`

  // Deprecated: Use LeaseCheckpoint Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalEnableLeaseCheckpoint bool `json:"experimental-enable-lease-checkpoint"`
  
  // Deprecated: Use LeaseCheckpointPersist Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalEnableLeaseCheckpointPersist bool `json:"experimental-enable-lease-checkpoint-persist"`

+ // ServerFeatureGate is a server level feature gate
+ ServerFeatureGate featuregate.FeatureGate
  ...
```

### Alpha 或 Beta 功能的功能门控 {#feature-gates-for-alpha-or-beta-features}

下表总结了可在 etcd 上设置的功能门控。

| 特性                             | 默认值   | 阶段   | 说明                                                                                   |
|----------------------------------|----------|--------|----------------------------------------------------------------------------------------|
| CompactHashCheck                 | false    | Alpha  | 启用领导者定期检查跟随者的压缩哈希值。                                                                 |
| InitialCorruptCheck              | false    | Alpha  | 在向任何客户端或对等成员提供服务前启用数据损坏检查。                                                                 |
| LeaseCheckpoint                  | false    | Alpha  | 启用领导者向其他成员发送定期检查点，以防止领导者变更时剩余 TTL 被重置。                                               |
| LeaseCheckpointPersist           | false    | Alpha  | 启用持久化剩余 TTL，以防止长期租约的无限自动续期。                                                                 |
| SetMemberLocalAddr               | false    | Alpha  | 启用在与对等成员通信时，使用 initial-advertise-peer-urls 中指定的第一个非环回本地地址作为本地地址。                                     |
| StopGRPCServiceOnDefrag          | false    | Alpha  | 启用在执行碎片整理时停止 etcd gRPC 服务对客户端请求的响应。                                                             |
| TxnModeWriteWithSharedBuffer     | true     | Beta   | 启用写入事务在其只读检查操作中使用共享缓冲区。                                                                 |

## 使用某个功能 {#using-a-feature}

### 特性阶段 {#feature-stages}

特性可处于 *Alpha*、*Beta*、*GA* 或 *Deprecated* 阶段。
*Alpha* 特性表示：

* 默认禁用。
* 可能存在缺陷。启用该功能可能会暴露缺陷。
* 该功能的支持可能随时被取消，且不另行通知。
* 该 API 可能在后续软件版本中以不兼容的方式发生变更，且不另行通知。
* 由于存在更高的缺陷风险且缺乏长期支持，仅建议在短期测试集群中使用。

*Beta* 特性表示：

* 默认启用。
* 该功能经过充分测试，启用该功能被认为是安全的。
* 整体功能的支持不会被移除，尽管细节可能会变更。
* 仅建议用于非业务关键场景，因为更广泛采用可能导致发现新的难以察觉的缺陷。

> [!NOTE]
> 请务必尝试使用 *Beta* 特性，并提供反馈！
> 进入正式发布阶段后，我们可能不再适合对这些特性进行进一步修改。

一个“正式发布”（General Availability，GA）特性也被称为“稳定”特性。其含义为：

* 该功能始终处于启用状态；无法将其禁用。
* 相应的功能门控已不再需要。
* 稳定版本的功能将在后续多个发布版本的软件中出现。

一个已弃用（Deprecated）的功能表示：

* 功能门控已不再使用。
* 该功能已进入正式发布阶段或已被移除。
