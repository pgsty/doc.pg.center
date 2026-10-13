---
title: 运行时重配置
weight: 4700
description: etcd 增量运行时重配置支持
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/runtime-configuration.md"
aliases: [/etcd/op-guide/runtime-configuration/]
---

etcd 支持增量式运行时重配置，允许用户在运行时更新集群成员。

重新配置请求仅在集群多数成员正常运行时才能处理。生产环境中**强烈建议**始终将集群规模设置为大于二。从两成员集群中移除成员是不安全的。两成员集群的多数为两个。若在移除过程中发生故障，集群可能无法继续推进，且可能需要 [从多数故障中重启][majority failure]。

为更好地理解运行时重配置的设计原理，请阅读 [运行时重配置文档][runtime-reconf]。

## 重新配置用例 {#reconfiguration-use-cases}

本节将介绍集群重新配置的一些常见原因。大多数情况仅涉及添加或移除成员的组合操作，具体说明如下，详见 [集群重新配置操作][cluster-reconf]。

### 轮换或升级多台机器 {#cycle-or-upgrade-multiple-machines}

如果多个集群成员需因计划内维护（如硬件升级、网络中断等）而迁移，建议逐个修改成员。

安全移除领导者是可行的，但选举过程期间会有一段短暂的停机时间。如果集群中存储的 v2 数据超过 50MB，建议对 [成员的数据目录][member migration]执行迁移。

### 修改集群规模 {#change-the-cluster-size}

增加集群规模可提升 [故障容忍度][fault tolerance table]，并提供更优的读取性能。由于客户端可从任意成员读取，增加成员数量可提升整体可串行化读取吞吐量。

减小集群规模可提升集群的写入性能，但会降低其容错能力。写入操作在被确认为已提交前，需复制到集群中多数成员。减小集群规模会降低所需的多数成员数，从而使每次写入更快地被提交。

### 替换故障节点 {#replace-a-failed-machine}

如果某台机器因硬件故障、数据目录损坏或其他严重情况而发生故障，应尽快予以替换。尚未移除的故障机器会负面影响法定人数，并降低系统对额外故障的容错能力。

要替换机器，请按照 [从集群中移除成员][remove member] 的操作说明执行，然后 [添加新成员][add member] 以替代原成员。如果集群数据量超过 50MB，建议在原成员数据目录仍可访问的情况下 [迁移该成员的数据目录][member migration]。

### 从多数成员故障重启集群 {#restart-cluster-from-majority-failure}

如果集群的多数节点丢失，或所有节点的 IP 地址均发生变更，则必须通过手动操作来安全恢复。恢复过程的基本步骤包括 [使用旧数据创建新集群][disaster recovery]、强制单个成员作为领导者，最后通过运行时配置逐个 [添加新成员][add member]至该新集群。

### 从少数成员故障中恢复集群 {#recover-cluster-from-minority-failure}

若某个特定成员丢失，则相当于替换一台故障机器。具体步骤请参见 [替换故障机器](/zh/docs/etcd/op-guide/runtime-configuration/#replace-a-failed-machine)。

## 集群重新配置操作 {#cluster-reconfiguration-operations}

考虑到这些使用场景，每种相关操作均可予以描述。

在进行任何更改之前，必须有 etcd 成员的简单多数（法定人数）可用。这与向 etcd 执行任何写操作的基本要求相同。

对集群的所有更改必须按顺序执行：

* 若要更新单个成员的 peerURLs，请执行更新操作
* 若要替换健康的单个成员，请先移除旧成员，再添加新成员
* 若要从 3 个成员增加到 5 个成员，请执行两次添加操作
* 若要从 5 个成员减少到 3 个成员，请执行两次移除操作

所有示例均使用 etcd 自带的 `etcdctl` 命令行工具。如需在不使用 `etcdctl` 的情况下更改成员关系，请使用 [v3 gRPC members API][member-api-grpc]。

### 更新成员 {#update-a-member}

#### 更新通告客户端 URL {#update-advertise-client-urls}

要更新成员的通告客户端 URL，只需使用更新后的客户端 URL 标志（`--advertise-client-urls`）或环境变量（`ETCD_ADVERTISE_CLIENT_URLS`）重启该成员。重启后的成员将自动发布更新后的 URL。错误更新的客户端 URL 不会影响 etcd 集群的健康状态。

#### 更新通告对等成员 URL {#update-advertise-peer-urls}

要更新成员的通告对等成员 URL，需先通过 member 命令显式更新，然后重启该成员。由于更新对等成员 URL 会更改集群范围的配置，可能影响 etcd 集群的健康状态，因此需要额外执行此操作。

要更新通告的对等成员 URL，首先需找到目标成员的 ID。使用 `etcdctl` 列出所有成员：

```sh
$ etcdctl member list
6e3bd23ae5f1eae0: name=node2 peerURLs=http://localhost:23802 clientURLs=http://127.0.0.1:23792
924e2e83e93f2560: name=node3 peerURLs=http://localhost:23803 clientURLs=http://127.0.0.1:23793
a8266ecf031671f3: name=node1 peerURLs=http://localhost:23801 clientURLs=http://127.0.0.1:23791
```

本示例使用 `update` 更新 ID 为 a8266ecf031671f3 的成员，将其 peerURLs 值更改为 `http://10.0.1.10:2380`：

```sh
$ etcdctl member update a8266ecf031671f3 --peer-urls=http://10.0.1.10:2380
Updated member with ID a8266ecf031671f3 in cluster
```

### 移除成员 {#remove-a-member}

假设要移除的成员 ID 为 a8266ecf031671f3。使用 `remove` 命令执行移除操作：

```sh
$ etcdctl member remove a8266ecf031671f3
Removed member a8266ecf031671f3 from cluster
```

目标成员将在此时自行停止，并在日志中输出移除信息：

```
etcd: this member has been permanently removed from the cluster. Exiting.
```

安全移除领导者是可行的，但在此期间集群将处于不可用状态，直到新的领导者被选举出来。该持续时间通常为选举超时时间加上投票过程所需时间。

### 添加新成员 {#add-a-new-member}

添加成员是一个两步过程：

* 通过 [gRPC 成员 API][member-api-grpc] 或 `etcdctl member add` 命令将新成员添加至集群。
* 使用包含更新后成员列表（现有成员 + 新成员）的新集群配置启动新成员。

`etcdctl` 通过指定成员的 [名称][conf-name] 和 [已通告的对等成员 URL][conf-adv-peer]，将新成员添加到集群中：

```sh
$ etcdctl member add infra3 --peer-urls=http://10.0.1.13:2380
added member 9bf1b35fc7761a23 to cluster

ETCD_NAME="infra3"
ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra3=http://10.0.1.13:2380"
ETCD_INITIAL_CLUSTER_STATE=existing
```

`etcdctl` 已向集群通报了新成员，并打印出成功启动该成员所需的环境变量。现在请使用新成员的相关标志启动新的 etcd 进程：

```sh
$ export ETCD_NAME="infra3"
$ export ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra3=http://10.0.1.13:2380"
$ export ETCD_INITIAL_CLUSTER_STATE=existing
$ etcd --listen-client-urls http://10.0.1.13:2379 --advertise-client-urls http://10.0.1.13:2379 --listen-peer-urls http://10.0.1.13:2380 --initial-advertise-peer-urls http://10.0.1.13:2380 --data-dir %data_dir%
```

新成员将作为集群的一部分运行，并立即开始追赶集群中其他成员的进度。

若添加多个成员，最佳实践是逐个配置成员，并在添加更多新成员前验证每个成员是否已正确启动。若向单成员集群添加新成员，在新成员启动前，集群无法推进，因为达成共识需要多数成员（即至少两个成员）达成一致。此行为仅发生在 `etcdctl member add` 通知集群新成员存在，且新成员成功与现有成员建立连接之间的时段。

#### 添加一个学习者成员 {#add-a-new-member-as-learner}

从 v3.4 版本开始，etcd 支持以学习者成员 / 非投票成员身份添加新成员。
其设计动机与架构详情请参见 [设计文档][design-learner]。
为使添加新成员的过程更加安全，并在添加新成员时降低集群停机时间，建议将新成员以学习者成员身份加入集群，直至其完成数据同步。该过程可描述为三个步骤：

* 通过 [gRPC members API][member-api-grpc] 或 `etcdctl member add --learner` 命令，将新成员添加为学习者成员。

* 使用新的集群配置启动新成员，配置中包含更新后的成员列表（现有成员 + 新成员）。
此步骤与之前完全相同。

* 通过 [gRPC members API][member-api-grpc] 或 `etcdctl member promote` 命令，将新添加的学习者成员提升为投票成员。etcd 服务器会验证提升请求，以确保操作安全。
只有当学习者成员的 Raft 日志已追赶上领导者时，才能将其提升为投票成员。
若学习者成员尚未追赶上领导者的 Raft 日志，成员提升请求将失败（详见[提升成员时的错误情况][error cases when promoting a member]一节获取更多细节）。
在此情况下，应等待片刻后重试。

在 v3.4 版本中，etcd 服务器将集群可拥有的学习者成员数量限制为一个。主要考虑是减少因将数据从领导者传播到学习者成员而给领导者带来的额外负载。

使用 `etcdctl member add` 并配合标志 `--learner`，可将新成员作为学习者成员添加至集群。

```sh
$ etcdctl member add infra3 --peer-urls=http://10.0.1.13:2380 --learner
Member 9bf1b35fc7761a23 added to cluster a7ef944b95711739

ETCD_NAME="infra3"
ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra3=http://10.0.1.13:2380"
ETCD_INITIAL_CLUSTER_STATE=existing
```

新添加的学习者成员启动新的 etcd 进程后，使用 `etcdctl member promote` 将该学习者成员提升为投票成员。
```
$ etcdctl member promote 9bf1b35fc7761a23
Member 9e29bbaa45d74461 promoted in cluster a7ef944b95711739
```

#### 添加成员时的错误情况 {#error-cases-when-adding-members}

在以下情况下，新主机未包含在已枚举节点的列表中。如果这是一个新集群，必须将该节点添加到初始集群成员列表中。

```sh
$ etcd --name infra3 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state existing
etcdserver: assign ids error: the member count is unequal
exit 1
```

在此错误示例中，启动时指定的地址（10.0.1.14:2380）与加入集群时注册的地址（10.0.1.13:2380）不同：

```sh
$ etcd --name infra4 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra4=http://10.0.1.14:2380 \
  --initial-cluster-state existing
etcdserver: assign ids error: unmatched member while checking PeerURLs
exit 1
```

如果 etcd 启动时使用了已移除成员的数据目录，且连接到集群中的任何活跃成员，则 etcd 会自动退出：

```sh
$ etcd
etcd: this member has been permanently removed from the cluster. Exiting.
exit 1
```

#### 添加学习者成员时的错误情况 {#error-cases-when-adding-a-learner-member}

如果集群中已存在 1 个学习者成员，则无法再添加学习者成员（v3.4）。
```
$ etcdctl member add infra4 --peer-urls=http://10.0.1.14:2380 --learner
Error: etcdserver: too many learner members in cluster
```

#### 提升学习者成员时的错误情况 {#error-cases-when-promoting-a-learner-member}

学习者成员只有在与领导者同步后，才能被提升为投票成员。
```
$ etcdctl member promote 9bf1b35fc7761a23
Error: etcdserver: can only promote a learner member which is in sync with leader
```

提升非学习者成员将失败。
```
$ etcdctl member promote 9bf1b35fc7761a23
Error: etcdserver: can only promote a learner member
```

提升集群中不存在的成员将失败。
```
$ etcdctl member promote 12345abcde
Error: etcdserver: member not found
```


### 严格重新配置检查模式 (`-strict-reconfig-check`) {#strict-reconfiguration-check-mode--strict-reconfig-check}

如上所述，添加新成员的最佳实践是每次仅配置一个成员，并在添加更多新成员前验证其是否正确启动。逐步进行此操作至关重要，因为如果新添加的成员配置不正确（例如对等成员 URL 错误），集群可能失去法定人数。法定人数丢失的原因在于，即使新添加的成员无法与其他现有成员通信，该成员仍会被计入法定人数。此外，若存在连接问题或操作问题，也可能导致法定人数丢失。

为避免此问题，etcd 提供了选项 `-strict-reconfig-check`。若将此选项传递给 etcd，则当重新配置后已启动的成员数量将少于重新配置后集群的法定人数时，etcd 会拒绝该重新配置请求。

默认启用。

[add member]: #add-a-new-member
[cluster-reconf]: #cluster-reconfiguration-operations
[conf-adv-peer]: /zh/docs/etcd/op-guide/configuration#clustering
[conf-name]: /zh/docs/etcd/op-guide/configuration#member
[design-learner]: /zh/docs/etcd/learning/design-learner
[disaster recovery]: /zh/docs/etcd/op-guide/recovery
[error cases when promoting a member]: #error-cases-when-promoting-a-learner-member
[fault tolerance table]: https://etcd.io/docs/v2.3/admin_guide/#fault-tolerance-table
[majority failure]: #restart-cluster-from-majority-failure
[member migration]: https://etcd.io/docs/v2.3/admin_guide/#member-migration
[member-api]: https://etcd.io/docs/v2.3/members_api/
[member-api-grpc]: /zh/docs/etcd/dev-guide/api_reference_v3/
[remove member]: #remove-a-member
[runtime-reconf]: /zh/docs/etcd/op-guide/runtime-reconf-design/
