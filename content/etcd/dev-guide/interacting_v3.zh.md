---
title: 与 etcd 交互
weight: 3250
description: "etcdctl：与 etcd 服务器交互的命令行工具"
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/dev-guide/interacting_v3.md"
---

用户通常通过设置或获取键的值来与 etcd 交互。本节介绍如何使用 etcdctl（用于与 etcd 服务器交互的命令行工具）实现这一操作。此处描述的概念同样适用于 gRPC API 或客户端库 API。

etcdctl 与 etcd 通信时所使用的 API 版本可通过 `ETCDCTL_API` 环境变量设置为 `2` 或 `3`。默认情况下，主分支（3.4）上的 etcdctl 使用 v3 API，而较早版本（3.3 及更早）默认使用 v2 API。

请注意，使用 v2 API 创建的任何键均无法通过 v3 API 查询。对 v2 键执行 v3 API ```etcdctl get``` 操作时，将返回 0 且不包含键数据，这是预期行为。


```bash
export ETCDCTL_API=3
```

## 查找版本 {#find-versions}

etcdctl 版本与服务器 API 版本可用于确定执行 etcd 各项操作时应使用的正确命令。

以下是查找版本号的命令：

```bash
$ etcdctl version
etcdctl version: 3.1.0-alpha.0+git
API version: 3.1
```

## 写入键 {#write-a-key}

应用程序通过向键写入数据将键存储到 etcd 集群中。每个存储的键都会通过 Raft 协议复制到集群中的所有成员，以实现一致性和可靠性。

以下是将键 `foo` 的值设置为 `bar` 的命令：

```bash
$ etcdctl put foo bar
OK
```

此外，可通过为键附加租约，将其设置为指定时间间隔。

以下是将键 `foo1` 的值设置为 `bar1` 并保留 10 秒的命令。

```bash
$ etcdctl put foo1 bar1 --lease=1234abcd
OK
```

> [!NOTE]
> 上述命令中的租约 ID `1234abcd` 指创建 10 秒租约时返回的 ID。该 ID 后续可附加至键。

## 读取键 {#read-keys}

应用程序可从 etcd 集群读取键的值。查询可读取单个键，或键的范围。

假设 etcd 集群已存储以下键：

```bash
foo = bar
foo1 = bar1
foo2 = bar2
foo3 = bar3
```

以下是读取键 `foo` 值的命令：

```bash
$ etcdctl get foo
foo
bar
```

以下是读取键 `foo` 值的十六进制格式的命令：

```bash
$ etcdctl get foo --hex
\x66\x6f\x6f          # Key
\x62\x61\x72          # Value
```

以下是仅读取键 `foo` 值的命令：

```bash
$ etcdctl get foo --print-value-only
bar
```

以下是遍历从 `foo` 到 `foo3` 范围内键的命令：

```bash
$ etcdctl get foo foo3
foo
bar
foo1
bar1
foo2
bar2
```

> [!NOTE]
> `foo3` 被排除，因为范围位于半开区间 `[foo, foo3)` 内，不包含 `foo3`。

以下是遍历所有以 `foo` 为前缀的键的命令：

```bash
$ etcdctl get --prefix foo
foo
bar
foo1
bar1
foo2
bar2
foo3
bar3
```

以下是遍历所有以 `foo` 为前缀的键、并将结果数量限制为 2 的命令：

```bash
$ etcdctl get --prefix --limit=2 foo
foo
bar
foo1
bar1
```

以下是使用 [`RangeStream`](/zh/etcd/learning/api/#rangestream) RPC 遍历所有以 `foo` 为前缀的键的命令。结果与单次 `Range` 调用完全相同：

```bash
$ etcdctl get --stream --prefix foo
foo
bar
foo1
bar1
foo2
bar2
foo3
bar3
```

`--stream` 不支持 `--order`、`--sort-by` 或修订版本过滤。

## 读取键的过往版本 {#read-past-version-of-keys}

应用程序可能需要读取已被覆盖的键的旧版本。例如，应用程序可通过访问键的早期版本来回滚至旧配置。或者，应用程序可通过访问键的历史记录，在多次请求中获取多个键的一致视图。

由于对 etcd 集群键值存储的每次修改都会递增 etcd 集群的全局修订版本，因此应用程序可通过提供较早的 etcd 修订版本来读取已被覆盖的键。

假设一个 etcd 集群中已存在以下键：

```bash
foo = bar         # revision = 2
foo1 = bar1       # revision = 3
foo = bar_new     # revision = 4
foo1 = bar1_new   # revision = 5
```

以下是访问键的历史版本的示例：

```bash
$ etcdctl get --prefix foo # access the most recent versions of keys
foo
bar_new
foo1
bar1_new

$ etcdctl get --prefix --rev=4 foo # access the versions of keys at revision 4
foo
bar_new
foo1
bar1

$ etcdctl get --prefix --rev=3 foo # access the versions of keys at revision 3
foo
bar
foo1
bar1

$ etcdctl get --prefix --rev=2 foo # access the versions of keys at revision 2
foo
bar

$ etcdctl get --prefix --rev=1 foo # access the versions of keys at revision 1
```

## 读取大于等于指定键字节值的键 {#read-keys-which-are-greater-than-or-equal-to-the-byte-value-of-the-specified-key}

应用程序可能需要读取字节值大于或等于指定键的键。

假设一个 etcd 集群中已存在以下键：

```bash
a = 123
b = 456
z = 789
```

以下是读取键值大于或等于键 `b` 字节值的命令：

```bash
$ etcdctl get --from-key b
b
456
z
789
```

## 删除键 {#delete-keys}

应用程序可以从 etcd 集群中删除一个键或一组键。

假设一个 etcd 集群中已存在以下键：

```bash
foo = bar
foo1 = bar1
foo3 = bar3
zoo = val
zoo1 = val1
zoo2 = val2
a = 123
b = 456
z = 789
```

以下是删除键 `foo` 的命令：

```bash
$ etcdctl del foo
1 # one key is deleted
```

以下是删除键范围从 `foo` 到 `foo9` 的命令：

```bash
$ etcdctl del foo foo9
2 # two keys are deleted
```

以下是删除键 `zoo` 的命令，删除后将返回被删除的键值对：

```bash
$ etcdctl del --prev-kv zoo
1   # one key is deleted
zoo # deleted key
val # the value of the deleted key
```

以下是用于删除前缀为 `zoo` 的键的命令：

```bash
$ etcdctl del --prefix zoo
2 # two keys are deleted
```

以下是删除键值大于或等于键 `b` 字节值的命令：

```bash
$ etcdctl del --from-key b
2 # two keys are deleted
```

## 监听键变化 {#watch-key-changes}

应用程序可对键或键范围进行监听，以监控任何更新。

以下是监听键 `foo` 的命令：

```bash
$ etcdctl watch foo
# in another terminal: etcdctl put foo bar
PUT
foo
bar
```

以下是监听键 `foo` 的十六进制格式的命令：

```bash
$ etcdctl watch foo --hex
# in another terminal: etcdctl put foo bar
PUT
\x66\x6f\x6f          # Key
\x62\x61\x72          # Value
```

以下是监听从 `foo` 到 `foo9` 范围键的命令：

```bash
$ etcdctl watch foo foo9
# in another terminal: etcdctl put foo bar
PUT
foo
bar
# in another terminal: etcdctl put foo1 bar1
PUT
foo1
bar1
```

以下是监听键前缀为 `foo` 的键的命令：

```bash
$ etcdctl watch --prefix foo
# in another terminal: etcdctl put foo bar
PUT
foo
bar
# in another terminal: etcdctl put fooz1 barz1
PUT
fooz1
barz1
```

以下是监听多个键 `foo` 和 `zoo` 的命令：

```bash
$ etcdctl watch -i
$ watch foo
$ watch zoo
# in another terminal: etcdctl put foo bar
PUT
foo
bar
# in another terminal: etcdctl put zoo val
PUT
zoo
val
```

## 监听键的历史变更 {#watch-historical-changes-of-keys}

应用程序可能需要监听 etcd 中键的历史变更。例如，应用程序可能希望接收某个键的所有修改；如果应用程序保持与 etcd 的连接，则 `watch` 已足够。然而，如果应用程序或 etcd 发生故障，故障期间可能发生变更，应用程序将无法实时接收更新。为确保更新能够送达，应用程序必须能够监听键的历史变更。为此，应用程序可以在监听时指定一个历史修订版本，如同读取键的过去版本一样。

假设已完成以下操作序列：

```bash
$ etcdctl put foo bar         # revision = 2
OK
$ etcdctl put foo1 bar1       # revision = 3
OK
$ etcdctl put foo bar_new     # revision = 4
OK
$ etcdctl put foo1 bar1_new   # revision = 5
OK
```

以下是监听历史变更的示例：

```bash
# watch for changes on key `foo` since revision 2
$ etcdctl watch --rev=2 foo
PUT
foo
bar
PUT
foo
bar_new
```

```bash
# watch for changes on key `foo` since revision 3
$ etcdctl watch --rev=3 foo
PUT
foo
bar_new
```

以下是一个仅从最后一次历史变更开始监听的示例：

```bash
# watch for changes on key `foo` and return last revision value along with modified value
$ etcdctl watch --prev-kv foo
# in another terminal: etcdctl put foo bar_latest
PUT
foo         # key
bar_new     # last value of foo key before modification
foo         # key
bar_latest  # value of foo key after modification
```

## 监听进度 {#watch-progress}

应用程序可能需要检查监听的进度，以判断监听流的更新状态。例如，若监听用于更新缓存，则了解缓存相对于法定人数读取的修订版本是否过时会很有帮助。

可以使用交互式监听会话中的“progress”命令，向 etcd 服务器请求在监听流中发送进度通知更新：

```bash
$ etcdctl watch -i
$ watch a
$ progress
progress notify: 1
# in another terminal: etcdctl put x 0
# in another terminal: etcdctl put y 1
$ progress
progress notify: 3
```

> [!NOTE]
> 进度通知响应中的修订版本号是监听流所连接的本地 etcd 服务器节点的修订版本。如果该节点处于网络分区状态且不属于法定人数，此进度通知的修订版本可能低于对非分区 etcd 服务器节点执行法定人数读取时返回的修订版本。

## 压缩的修订版本 {#compacted-revisions}

如前所述，etcd 会保留修订版本，以便应用程序能够读取键的过往版本。然而，为了避免积累无限量的历史数据，必须对过去的修订版本执行压缩。执行压缩后，etcd 会移除历史修订版本，释放资源以供后续使用。所有修订版本早于已压缩修订版本的过时数据将不可用。

以下是执行压缩修订版本的命令：

```bash
$ etcdctl compact 5
compacted revision 5

# any revisions before the compacted one are not accessible
$ etcdctl get --rev=4 foo
Error:  rpc error: code = 11 desc = etcdserver: mvcc: required revision has been compacted
```

> [!NOTE]
> 可通过在任意键（存在或不存在）上使用 get 命令以 JSON 格式获取当前 etcd 服务器的修订版本。以下示例展示了对 etcd 服务器中不存在的 mykey 执行操作的情况：

```bash
$ etcdctl get mykey -w=json
{"header":{"cluster_id":14841639068965178418,"member_id":10276657743932975437,"revision":15,"raft_term":4}}
```

## 授予租约 {#grant-leases}

应用程序可从 etcd 集群授予键的租约。当键绑定到租约时，其生命周期与租约的生命周期绑定，而租约的生命周期由生存时间（TTL）决定。每个租约在授予时由应用程序指定最小生存时间（TTL）值。租约的实际 TTL 值至少为最小 TTL，且由 etcd 集群选定。一旦租约的 TTL 到期，租约即失效，所有绑定的键将被删除。

以下是授予租约的命令：

```bash
# grant a lease with 60 second TTL
$ etcdctl lease grant 60
lease 32695410dcc0ca06 granted with TTL(60s)

# attach key foo to lease 32695410dcc0ca06
$ etcdctl put --lease=32695410dcc0ca06 foo bar
OK
```

## 撤销租约 {#revoke-leases}

应用程序通过租约 ID 撤销租约。撤销租约将删除其所有关联的键。

假设已完成以下操作序列：

```bash
$ etcdctl lease grant 60
lease 32695410dcc0ca06 granted with TTL(60s)
$ etcdctl put --lease=32695410dcc0ca06 foo bar
OK
```

以下是撤销相同租约的命令：

```bash
$ etcdctl lease revoke 32695410dcc0ca06
lease 32695410dcc0ca06 revoked

$ etcdctl get foo
# empty response since foo is deleted due to lease revocation
```

## 保持租约有效 {#keep-leases-alive}

应用程序可通过刷新租约的 TTL 来维持租约有效，防止其过期。

假设已完成以下操作序列：

```bash
$ etcdctl lease grant 60
lease 32695410dcc0ca06 granted with TTL(60s)
```

以下是保持相同租约持续有效的命令：

```bash
$ etcdctl lease keep-alive 32695410dcc0ca06
lease 32695410dcc0ca06 keepalived with TTL(60)
lease 32695410dcc0ca06 keepalived with TTL(60)
lease 32695410dcc0ca06 keepalived with TTL(60)
...
```

## 获取租约信息 {#get-lease-information}

应用程序可能需要了解租约信息，以便能够续期，或检查租约是否仍然有效或已过期。应用程序也可能需要知道某个特定租约所关联的键。

假设已完成以下操作序列：

```bash
# grant a lease with 500 second TTL
$ etcdctl lease grant 500
lease 694d5765fc71500b granted with TTL(500s)

# attach key zoo1 to lease 694d5765fc71500b
$ etcdctl put zoo1 val1 --lease=694d5765fc71500b
OK

# attach key zoo2 to lease 694d5765fc71500b
$ etcdctl put zoo2 val2 --lease=694d5765fc71500b
OK
```

获取租约信息的命令如下：

```bash
$ etcdctl lease timetolive 694d5765fc71500b
lease 694d5765fc71500b granted with TTL(500s), remaining(258s)
```

以下是获取租约信息及其关联键的命令：

```bash
$ etcdctl lease timetolive --keys 694d5765fc71500b
lease 694d5765fc71500b granted with TTL(500s), remaining(132s), attached keys([zoo2 zoo1])

# if the lease has expired or does not exist it will give the below response:
Error:  etcdserver: requested lease not found
```
