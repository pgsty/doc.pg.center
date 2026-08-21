---
title: etcd API
weight: 2625
description: etcd API 核心设计概述
categories: [概念]
upstream_link: "https://github.com/etcd-io/website/blob/a9ee660fdbf9584deb4af639c4dc63b01413e44f/content/en/docs/v3.7/learning/api.md"
---

本文旨在概述 v3 版 etcd API 的核心设计。
切勿将本指南与已弃用的 etcd v2 API 混淆，后者已于 etcd v3.5 中弃用。
本文并非全面涵盖所有内容，而是聚焦于理解 etcd 所需的基本概念，避免被较少使用的 API 调用分散注意力。
所有 etcd API 均定义在 [gRPC services][grpc-service] 中，这些服务对 etcd 服务器所理解的远程过程调用（RPC）进行了分类。
所有 etcd RPC 的完整列表已在 [gRPC API listing][grpc-api] 的 Markdown 文档中记录。

## gRPC 服务 {#grpc-services}

发送至 etcd 服务器的每个 API 请求均为 gRPC 远程过程调用。etcd 中的 RPC 按功能划分为不同的服务。

与 etcd 键空间相关的关键服务包括：
* KV - 创建、更新、获取和删除键值对。
* Watch - 监听键的变化。
* Lease - 客户端心跳消息的消费原语。
管理集群自身的服务包括：
* Auth - 基于角色的身份认证机制，用于用户身份认证。
* Cluster - 提供成员信息和配置管理功能。
* Maintenance - 执行恢复快照、整理碎片以及返回各成员状态信息。
### 请求与响应 {#requests-and-responses}

etcd 中的所有 RPC 均遵循相同的格式。每个 RPC 都有一个函数 `Name`，它接收 `NameRequest` 作为参数，并返回 `NameResponse` 作为响应。例如，以下是 `Range` RPC 的描述：

```protobuf
service KV {
  Range(RangeRequest) returns (RangeResponse)
  ...
}
```

### 响应头 {#response-header}

etcd API 的所有响应均附带响应头，其中包含该响应对应的集群元数据：

```proto
message ResponseHeader {
  uint64 cluster_id = 1;
  uint64 member_id = 2;
  int64 revision = 3;
  uint64 raft_term = 4;
}
```

* Cluster_ID - 生成响应的集群的 ID。
* Member_ID - 生成响应的成员的 ID。
* Revision - 生成响应时键值存储的修订版本。
* Raft_Term - 生成响应时成员的 Raft 任期。
应用程序可读取 `Cluster_ID` 或 `Member_ID` 字段，以确保其与预期的集群（成员）进行通信。

应用程序可使用 `Revision` 字段了解键值存储的最新修订版本。当应用程序指定历史修订版本以执行 `time travel query` 操作，并希望获知请求时刻的最新修订版本时，此功能尤为有用。

应用程序可以使用 `Raft_Term` 检测集群完成新的领导者选举。

## 键值 API {#key-value-api}

键值对 API 用于操作存储在 etcd 中的键值对。发送至 etcd 的大多数请求通常为键值对请求。

### 系统原语 {#system-primitives}

### 键值对 {#key-value-pair}

键值对是键值 API 可操作的最小单元。每个键值对包含若干字段，定义于 [protobuf 格式][kv-proto]：

```protobuf
message KeyValue {
  bytes key = 1;
  int64 create_revision = 2;
  int64 mod_revision = 3;
  int64 version = 4;
  bytes value = 5;
  int64 lease = 6;
}
```

* Key - 以字节表示的键。不允许使用空键。
* Value - 以字节表示的值。
* Version - 键的版本号。删除操作会将版本重置为零，对键的任何修改都会增加其版本号。
* Create_Revision - 键最后一次创建时的修订版本。
* Mod_Revision - 键最后一次修改时的修订版本。
* Lease - 附加到键的租约 ID。若租约为 0，则表示该键未附加任何租约。

除了键和值之外，etcd 还在键消息中附加了额外的修订版本元数据。该修订版本信息按创建和修改时间对键进行排序，有助于管理分布式同步中的并发。etcd 客户端的[分布式共享锁][locks] 使用创建修订版本来等待锁所有权。类似地，修改修订版本用于检测[软件事务内存][STM]读集冲突，并等待[选举][elections]更新。

#### 修订版本 {#revisions}

etcd 维护一个 64 位的集群范围计数器，即存储修订版本，每当键空间发生修改时，该计数器就会递增。修订版本充当全局逻辑时钟，对存储系统中的所有更新进行顺序排序。新修订版本所代表的变更具有增量特性；与某一修订版本关联的数据即为导致存储系统发生变化的数据。在内部，新修订版本意味着将变更写入后端数据库的 B+ 树，键为递增后的修订版本。

当结合 etcd 的 [多版本并发控制][mvcc] 后端时，修订版本的价值更加凸显。MVCC 模型意味着，由于历史键版本被保留，键值存储可从过去的修订版本中进行查看。此历史记录的保留策略可由集群管理员配置，以实现细粒度的存储管理；通常情况下，etcd 会通过定时机制丢弃旧的键修订版本。典型的 etcd 集群会保留被覆盖的键数据数小时。这同样能够可靠地处理长时间的客户端断开连接，而不仅仅是瞬时网络中断：监听器只需从最后一次观察到的历史修订版本处恢复即可。类似地，若需在特定时间点读取存储内容，读取请求可标记一个修订版本，以返回该修订版本提交时键空间的视图。

#### 键范围 {#key-ranges}

etcd 的数据模型将所有键索引于一个扁平的二进制键空间中。这与其它键值存储系统不同，后者采用层级结构将键组织为目录。etcd 不通过目录列出键，而是通过键区间列出键 `[a, b)`。

这些区间在 etcd 中通常被称为“范围”。对范围的操作比对目录的操作更强大。与分层存储类似，范围支持通过 `[a, a+1)` 进行单个键查找（例如，['a', 'a\x00') 查找键 'a'），并可通过编码键的目录深度实现目录查找。除上述操作外，范围还可编码前缀；例如，范围 `['a', 'b')` 用于查找所有以字符串 'a' 为前缀的键。

按照惯例，请求的范围由字段 `key` 和 `range_end` 表示。`key` 字段为范围的起始键，必须非空。`range_end` 字段为范围最后一个键之后的键。若 `range_end` 未指定或为空，则范围仅包含键参数本身。若 `range_end` 为 `key` 加一（例如，“aa”+1 == “ab”，"a\xff"+1 == “b”），则范围表示所有以该键为前缀的键。若 `key` 和 `range_end` 均为 '\0'，则范围表示所有键。若 `range_end` 为 '\0'，则范围表示所有大于或等于键参数的键。

### 范围 {#range}

通过 `Range` API 调用从键值存储中获取键，该调用接受一个 `RangeRequest`：

```protobuf
message RangeRequest {
  enum SortOrder {
	NONE = 0; // default, no sorting
	ASCEND = 1; // lowest target value first
	DESCEND = 2; // highest target value first
  }
  enum SortTarget {
	KEY = 0;
	VERSION = 1;
	CREATE = 2;
	MOD = 3;
	VALUE = 4;
  }

  bytes key = 1;
  bytes range_end = 2;
  int64 limit = 3;
  int64 revision = 4;
  SortOrder sort_order = 5;
  SortTarget sort_target = 6;
  bool serializable = 7;
  bool keys_only = 8;
  bool count_only = 9;
  int64 min_mod_revision = 10;
  int64 max_mod_revision = 11;
  int64 min_create_revision = 12;
  int64 max_create_revision = 13;
}
```

* Key, Range_End - 要获取的键范围。
* Limit - 请求返回的最大键数量。当 Limit 设置为 0 时，表示无限制。
* Revision - 用于范围查询的键值存储的时间点。若 Revision 小于或等于 0，则范围覆盖最新的键值存储。若指定的 Revision 已被压缩，返回 ErrCompacted 作为响应。
* Sort_Order - 已排序请求的排序顺序。
* Sort_Target - 用于排序的键值字段。
* Serializable - 将范围请求设置为使用可序列化成员本地读取。默认情况下，Range 为线性一致；其反映集群当前的共识状态。为获得更好的性能和可用性，可接受可能的陈旧读取，可序列化范围请求将本地服务，无需与其他节点达成共识。
* Keys_Only - 仅返回键，不返回值。
* Count_Only - 仅返回范围内键的数量。
* Min_Mod_Revision - 键修改修订版本的下限；过滤掉小于该值的修改修订版本。
* Max_Mod_Revision - 键修改修订版本的上限；过滤掉大于该值的修改修订版本。
* Min_Create_Revision - 键创建修订版本的下限；过滤掉小于该值的创建修订版本。
* Max_Create_Revision - 键创建修订版本的上限；过滤掉大于该值的创建修订版本。
客户端从 `Range` 调用接收到 `RangeResponse` 消息：

```protobuf
message RangeResponse {
  ResponseHeader header = 1;
  repeated mvccpb.KeyValue kvs = 2;
  bool more = 3;
  int64 count = 4;
}
```

* Kvs - 范围请求匹配的键值对列表。当 `Count_Only` 设置时，`Kvs` 为空。
* More - 当 `limit` 设置时，表示请求范围内还有更多键待返回。
* Count - 满足范围请求的键的总数。
对于键范围较大且不希望缓冲完整响应的情况，请参见 [RangeStream](#rangestream)。

### 范围流 {#rangestream}

`RangeStream` 返回的结果集与 `Range` 相同，但服务器会将响应拆分为一系列数据块，并流式传输至客户端。这可避免在任一端完全将大范围数据缓冲在内存中。`RangeStream` 接受与 `RangeRequest` 相同的 `Range`。

客户端从 `RangeStream` 调用接收 `RangeStreamResponse` 消息流：

```protobuf
message RangeStreamResponse {
  RangeResponse range_response = 1;
}
```

跨块的字段填充：

* Kvs - 每个数据块携带结果的不相交片段。按接收顺序拼接每个数据块的 `kvs`，可得到与单次 `Range` 调用相同的结果键集合。
* Header, More, Count - 仅在最后一个数据块中填充，且仅在流无错误完成时。早期数据块中的这些字段保持零值。对每个数据块的 `range_response` 应用 `proto.Merge`，可得到与 `Range` 返回结果等价的 `RangeResponse`。
如果流以错误结束，则没有任何数据块携带有效的 `header`、`more` 或 `count`。

流中的每个数据块均基于相同的修订版本提供。若请求未设置 `Revision`，服务器将在流开始时捕获最新的已提交修订版本，并在流的剩余过程中重复使用该版本。

`RangeStream` 不支持自定义排序顺序或修订版本过滤（`min_mod_revision`、`max_mod_revision`、`min_create_revision`、`max_create_revision`）。使用任一功能的请求将返回 `Unimplemented`。`RangeStream` 也不被 etcd gRPC 代理支持。

有两种常用方法可用来使用 `RangeStream`：

1. **独立处理每个数据块。** 适用于高性能场景，客户端希望在键到达时立即解码并处理，而非先收集全部结果。客户端遍历各个数据块并处理其中的 `kvs`；流正常结束后，再从最后一个数据块读取 `header`、`more` 或 `count`。
2. **合并为单一响应。** 适用于客户端希望获得与单次 `Range` 调用等效结果的场景。客户端将每个数据块中的 `range_response` 合并为一个 `RangeResponse`（例如使用 `proto.Merge`）。合并后的结果包含完整的 `kvs`，以及来自最后一个数据块的 `header`、`more` 和 `count`。Go 客户端提供 `clientv3.GetStreamToGetResponse` 辅助函数来实现此模式。

### 设置 {#put}

键通过发出 `Put` 调用保存到键值存储中，该调用接收一个 `PutRequest`：

```protobuf
message PutRequest {
  bytes key = 1;
  bytes value = 2;
  int64 lease = 3;
  bool prev_kv = 4;
  bool ignore_value = 5;
  bool ignore_lease = 6;
}
```

* Key - 要写入键值存储的键名称。
* Value - 以字节为单位的值，与键值存储中的键关联。
* Lease - 与键值存储中键关联的租约 ID。租约值为 0 表示无租约。
* Prev_Kv - 设置后，响应中包含本次 `Put` 请求更新前的键值对数据。
* Ignore_Value - 设置后，更新键而不更改其当前值。若键不存在，返回错误。
* Ignore_Lease - 设置后，更新键而不更改其当前租约。若键不存在，返回错误。
客户端从 `Put` 调用接收到 `PutResponse` 消息：

```protobuf
message PutResponse {
  ResponseHeader header = 1;
  mvccpb.KeyValue prev_kv = 2;
}
```

* Prev_Kv - 若在 `PutRequest` 中设置了 `Prev_Kv`，则为 `Put` 覆盖的键值对。
### 删除范围 {#delete-range}

使用 `DeleteRange` 调用删除键的范围，该调用接受 `DeleteRangeRequest`：

```protobuf
message DeleteRangeRequest {
  bytes key = 1;
  bytes range_end = 2;
  bool prev_kv = 3;
}
```

* Key, Range_End - 要删除的键范围。
* Prev_Kv - 设置后，返回被删除的键值对内容。
客户端从 `DeleteRange` 调用接收到 `DeleteRangeResponse` 消息：

```protobuf
message DeleteRangeResponse {
  ResponseHeader header = 1;
  int64 deleted = 2;
  repeated mvccpb.KeyValue prev_kvs = 3;
}
```

* Deleted - 已删除的键的数量。
* Prev_Kv - `DeleteRange` 操作所删除的所有键值对的列表。
### 事务 {#transaction}

事务是对键值存储的原子性 If/Then/Else 构造。它提供了一种将请求分组为原子块（即 Then/Else）的原语，其执行受键值存储内容的保护（即 If）。事务可用于防止键被意外的并发更新，构建比较并交换操作，并开发更高级别的并发控制。

事务可在单个请求中原子性地处理多个请求。对于键值存储的修改，这意味着事务的存储修订版本仅递增一次，且事务生成的所有事件将具有相同的修订版本。然而，在单个事务中多次修改同一键是被禁止的。

所有事务均通过一系列比较条件的合取进行保护，类似于一个 `If` 语句。每个比较条件检查存储系统中的单个键。它可以检查值是否存在或不存在，与指定值进行比较，或检查键的修订版本或版本号。两个不同的比较条件可作用于同一键或不同键。所有比较条件均以原子方式应用；若所有比较条件均为真，则认为事务成功，etcd 将执行事务的 then / `success` 请求块；否则认为事务失败，并执行 else / `failure` 请求块。

每个比较操作均以 `Compare` 消息编码：

```protobuf
message Compare {
  enum CompareResult {
    EQUAL = 0;
    GREATER = 1;
    LESS = 2;
    NOT_EQUAL = 3;
  }
  enum CompareTarget {
    VERSION = 0;
    CREATE = 1;
    MOD = 2;
    VALUE= 3;
  }
  CompareResult result = 1;
  // target is the key-value field to inspect for the comparison.
  CompareTarget target = 2;
  // key is the subject key for the comparison operation.
  bytes key = 3;
  oneof target_union {
    int64 version = 4;
    int64 create_revision = 5;
    int64 mod_revision = 6;
    bytes value = 7;
  }
}
```

* Result - 逻辑比较操作的类型（例如，相等、小于等）。
* Target - 要比较的键值字段。可以是键的版本、创建修订版本、修改修订版本或值。
* Key - 用于比较的键。
* Target_Union - 用户指定的用于比较的数据。
处理完比较块后，事务会应用一个请求块。块是一组 `RequestOp` 消息：

```protobuf
message RequestOp {
  // request is a union of request types accepted by a transaction.
  oneof request {
    RangeRequest request_range = 1;
    PutRequest request_put = 2;
    DeleteRangeRequest request_delete_range = 3;
  }
}
```

* Request_Range - 一个 `RangeRequest`。
* Request_Put - 一个 `PutRequest`。键必须唯一。不得与任何其他 Put 或 Delete 操作共享键。
* Request_Delete_Range - 一个 `DeleteRangeRequest`。不得与任何 Put 或 Delete 请求共享键。
所有操作合并为一个事务，通过 `Txn` API 调用发起，该调用接收一个 `TxnRequest`：

```protobuf
message TxnRequest {
  repeated Compare compare = 1;
  repeated RequestOp success = 2;
  repeated RequestOp failure = 3;
}
```

* Compare - 用于保护事务的一组谓词，表示各项条件的合取。
* Success - 所有 Compare 测试结果均为真时要执行的一组请求。
* Failure - 任意一个 Compare 测试结果为假时要执行的一组请求。
客户端从 `Txn` 调用接收到 `TxnResponse` 消息：

```protobuf
message TxnResponse {
  ResponseHeader header = 1;
  bool succeeded = 2;
  repeated ResponseOp responses = 3;
}
```

* Succeeded - `Compare` 评估结果为 true 或 false。
* Responses - 若 succeeded 为 true，则为应用 `Success` 块所得结果的响应列表；若 succeeded 为 false，则为 `Failure` 的响应列表。
`Responses` 列表对应于应用 `RequestOp` 列表后的结果，每个响应均以 `ResponseOp` 编码：

```protobuf
message ResponseOp {
  oneof response {
    RangeResponse response_range = 1;
    PutResponse response_put = 2;
    DeleteRangeResponse response_delete_range = 3;
  }
}
```

每个内部响应中包含的 `ResponseHeader` 不应以任何方式解释。
若客户端需要获取最新的修订版本，则应始终检查 `TxnResponse` 中顶层的 `ResponseHeader`。


## 监听 API {#watch-api}

本节中的 `Watch` API 提供基于事件的接口，用于异步监听键的变更。etcd 监听机制通过从指定的修订版本（当前或历史）持续监听键的变化，并将键的更新流式传输回客户端。

### 事件 {#events}

每个键的每一次变更均以 `Event` 消息表示。`Event` 消息同时提供更新的数据和更新类型：

```protobuf
message Event {
  enum EventType {
    PUT = 0;
    DELETE = 1;
  }
  EventType type = 1;
  KeyValue kv = 2;
  KeyValue prev_kv = 3;
}
```

* Type - 事件类型。PUT 类型表示键已存储新数据。DELETE 类型表示键已被删除。
* KV - 与事件关联的 KeyValue。PUT 事件包含当前的键值对。PUT 事件中 kv.Version=1 表示键的创建。DELETE 事件包含被删除的键，其修改修订版本设置为删除操作的修订版本。
* Prev_KV - 事件发生前紧邻修订版本的键对应的键值对。为节省带宽，仅在监听操作显式启用时才填充。
### 监听流 {#watch-streams}

监听是长期运行的请求，使用 gRPC 流来传输事件数据。监听流为双向通信；客户端通过向流写入来建立监听，通过读取来接收监听事件。通过为每个监听事件添加唯一的标识符，单个监听流可复用多个不同的监听。这种复用有助于降低核心 etcd 集群的内存占用和连接开销。

有关监听事件的保证说明，请参阅 [etcd api guarantees][watch-api-guarantees]。

客户端通过向 `Watch` 返回的流发送 `WatchCreateRequest` 来创建监听：

```protobuf
message WatchCreateRequest {
  bytes key = 1;
  bytes range_end = 2;
  int64 start_revision = 3;
  bool progress_notify = 4;

  enum FilterType {
    NOPUT = 0;
    NODELETE = 1;
  }
  repeated FilterType filters = 5;
  bool prev_kv = 6;
}
```

* Key, Range_End - 要监听的键范围。
* Start_Revision - 可选的修订版本，用于指定监听的起始位置（包含该修订版本）。若未指定，则从监听创建响应头中的修订版本之后的事件开始流式传输。可以从最后一次压缩修订版本开始，监听全部可用的事件历史。
* Progress_Notify - 若启用，当无新事件时，监听器将周期性地收到一个无事件的 WatchResponse。这在客户端希望从最近已知的修订版本恢复断开的监听器时非常有用。etcd 服务器根据当前负载决定通知的发送频率。
* Filters - 服务器端用于过滤的事件类型列表。
* Prev_Kv - 若启用，监听器将接收事件发生前的键值数据。这有助于了解哪些数据已被覆盖。
当收到 `WatchCreateRequest` 或某个已建立的监听存在新事件时，客户端将收到 `WatchResponse`：

```protobuf
message WatchResponse {
  ResponseHeader header = 1;
  int64 watch_id = 2;
  bool created = 3;
  bool canceled = 4;
  int64 compact_revision = 5;

  repeated mvccpb.Event events = 11;
}
```

* Watch_ID - 与响应对应的监听器 ID。
* Created - 若响应对应创建监听器请求，则设为 true。客户端应存储该 ID，并预期在流中接收该监听器的事件。发送至已创建监听器的所有事件均具有相同的 watch_id。
* Canceled - 若响应对应取消监听器请求，则设为 true。不再向已取消的监听器发送任何事件。
* Compact_Revision - 若监听器尝试在已压缩的修订版本上监听，则设为 etcd 可用的最小历史修订版本。此情况发生在以已压缩的修订版本创建监听器，或监听器无法跟上键值存储的进度时。监听器将被取消；使用相同 start_revision 创建新监听器将失败。
* Events - 与指定监听器 ID 对应的新事件序列列表。
如果客户端希望停止接收某个监听的事件，它会发出 `WatchCancelRequest`：

```protobuf
message WatchCancelRequest {
   int64 watch_id = 1;
}
```

* Watch_ID - 用于取消监听的 ID，以停止后续事件的传输。
## 租约 API {#lease-api}

租约是一种用于检测客户端活跃状态的机制。集群会授予带有生存时间（TTL）的租约。如果在指定的 TTL 期间内，etcd 集群未收到客户端的保活请求，该租约将到期。

为将租约与键值存储关联，每个键最多可绑定一个租约。当租约到期或被撤销时，所有绑定到该租约的键将被删除。每个过期的键都会在事件历史中生成一个删除事件。

### 获取租约 {#obtaining-leases}

租约通过 `LeaseGrant` API 调用获取，该调用接收一个 `LeaseGrantRequest`：

```protobuf
message LeaseGrantRequest {
  int64 TTL = 1;
  int64 ID = 2;
}
```

* TTL - 建议的生存时间，单位为秒。
* ID - 租约请求的 ID。若 ID 设置为 0，etcd 将自动选择一个 ID。
客户端从 `LeaseGrant` 调用接收到 `LeaseGrantResponse`：

```protobuf
message LeaseGrantResponse {
  ResponseHeader header = 1;
  int64 ID = 2;
  int64 TTL = 3;
}
```

* ID - 已授予租约的租约 ID。
* TTL - 为服务器选定的生存时间（以秒为单位）的租约。
```protobuf
message LeaseRevokeRequest {
  int64 ID = 1;
}
```

* ID - 要撤销的租约 ID。撤销租约后，所有关联的键将被删除。
### 保活 {#keep-alives}

租约通过使用 `LeaseKeepAlive` API 调用创建的双向流进行刷新。当客户端希望刷新租约时，它会通过该流发送 `LeaseKeepAliveRequest`：

```protobuf
message LeaseKeepAliveRequest {
  int64 ID = 1;
}
```

* ID - 要保活的租约的租约 ID。
保活流将响应 `LeaseKeepAliveResponse`：

```protobuf
message LeaseKeepAliveResponse {
  ResponseHeader header = 1;
  int64 ID = 2;
  int64 TTL = 3;
}
```

* ID - 已通过新 TTL 刷新的租约。
* TTL - 租约剩余的有效时间，单位为秒。
[watch-api-guarantees]: /zh/etcd/learning/api_guarantees/#watch-apis
[elections]: https://github.com/etcd-io/etcd/blob/main/client/v3/concurrency/election.go
[grpc-api]: /zh/etcd/dev-guide/api_reference_v3/
[grpc-service]: https://github.com/etcd-io/etcd/blob/main/api/etcdserverpb/rpc.proto
[kv-proto]: https://github.com/etcd-io/etcd/blob/main/api/mvccpb/kv.proto
[locks]: https://github.com/etcd-io/etcd/blob/main/client/v3/concurrency/mutex.go
[mvcc]: https://en.wikipedia.org/wiki/Multiversion_concurrency_control
[stm]: https://github.com/etcd-io/etcd/blob/main/client/v3/concurrency/stm.go
