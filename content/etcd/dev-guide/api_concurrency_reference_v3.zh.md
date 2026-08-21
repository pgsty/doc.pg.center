---
title: "API 参考：并发"
weight: 3900
description: "etcd 并发 API 参考"
categories: [参考]
upstream_link: "https://github.com/etcd-io/website/blob/a9ee660fdbf9584deb4af639c4dc63b01413e44f/content/en/docs/v3.7/dev-guide/api_concurrency_reference_v3.md"
---

本文 API 参考由命名的 `.proto` 文件自动生成。

##### 服务 `Lock` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#service-lock-serveretcdserverapiv3lockv3lockpbv3lockproto}

锁服务将客户端锁功能以 gRPC 接口的形式暴露。

| 方法 | 请求类型 | 响应类型 | 描述 |
| ------ | ------------ | ------------- | ----------- |
| Lock | LockRequest | LockResponse | Lock 在指定名称的锁上获取分布式共享锁。成功时，将返回一个唯一键，该键在调用方持有锁期间持续存在。该键可与事务配合使用，以确保对 etcd 的更新仅在持有锁所有权时发生。锁将持续持有，直至对键调用 Unlock，或与所有者关联的租约到期。 |
| Unlock | UnlockRequest | UnlockResponse | Unlock 接收 Lock 返回的键，并释放对锁的持有。等待获取锁的下一个 Lock 调用者将被唤醒，并获得锁的所有权。 |

##### 消息 `LockRequest` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-lockrequest-serveretcdserverapiv3lockv3lockpbv3lockproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| name | name 是要获取的分布式共享锁的标识符。 | bytes |
| lease | lease 是将附加到锁所有权的租约 ID。如果该租约到期或被撤销且当前持有锁，则锁会自动释放。使用相同租约调用 Lock 将被视为一次获取；使用相同租约两次锁定为无操作。 | int64 |

##### 消息 `LockResponse` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-lockresponse-serveretcdserverapiv3lockv3lockpbv3lockproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |
| key | 键是在锁持有者持有锁期间存在于 etcd 中的键。用户不应修改此键，否则锁可能表现出未定义行为。 | bytes |

##### 消息 `UnlockRequest` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-unlockrequest-serveretcdserverapiv3lockv3lockpbv3lockproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| key | key 是由 Lock 分配的锁所有权键。 | bytes |

##### 消息 `UnlockResponse` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-unlockresponse-serveretcdserverapiv3lockv3lockpbv3lockproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |

##### 服务 `Election` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#service-election-serveretcdserverapiv3electionv3electionpbv3electionproto}

选举服务通过 gRPC 接口向客户端暴露选举功能。

| 方法 | 请求类型 | 响应类型 | 描述 |
| ------ | ------------ | ------------- | ----------- |
| Campaign | CampaignRequest | CampaignResponse | Campaign 等待在选举中获取领导权，若成功则返回代表领导权的 LeaderKey。该 LeaderKey 可用于在选举中发布新值、以事务方式保护依赖于当前领导权的 API 请求，以及退出选举。 |
| Proclaim | ProclaimRequest | ProclaimResponse | Proclaim 使用新值更新领导者的公布值。 |
| Leader | LeaderRequest | LeaderResponse | Leader 返回当前选举的公布值（如有）。 |
| Observe | LeaderRequest | LeaderResponse | Observe 以有序方式流式传输选举中当选领导者发布的公告。 |
| Resign | ResignRequest | ResignResponse | Resign 释放选举中的领导权，使其他竞选者可获取领导权。 |

##### 消息 `CampaignRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-campaignrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| name | name 是竞选的标识符。 | bytes |
| lease | lease 是与选举领导权关联的租约 ID。如果在放弃领导权之前租约到期或被撤销，则领导权将转移给下一个竞选者（如果存在）。 | int64 |
| value | value 是竞选者赢得选举时设置的初始声明值。 | bytes |

##### 消息 `CampaignResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-campaignresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |
| leader | leader 描述用于维持选举领导权的资源。 | LeaderKey |

##### 消息 `LeaderKey` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-leaderkey-serveretcdserverapiv3electionv3electionpbv3electionproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| name | name 是与领导权键对应的选举标识符。 | bytes |
| key | key 是表示选举所有权的不透明键。若该键被删除，则失去领导权。 | bytes |
| rev | rev 是该键的创建修订版本。在事务中可通过检查键的创建修订版本是否与 rev 匹配，来验证对选举的所有权。 | int64 |
| lease | lease 是选举领导者的租约 ID。 | int64 |

##### 消息 `LeaderRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-leaderrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| name | name 是领导权信息的选举标识符。 | bytes |

##### 消息 `LeaderResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-leaderresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |
| kv | kv 表示最新的领导者更新的键值对。 | mvccpb.KeyValue |

##### 消息 `ProclaimRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-proclaimrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| leader | leader 表示对选举的领导权持有。 | LeaderKey |
| value | value 是用于覆盖领导者当前值的更新。 | bytes |

##### 消息 `ProclaimResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-proclaimresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |

##### 消息 `ResignRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-resignrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| leader | leader 是通过辞职放弃领导权的领导者。 | LeaderKey |

##### 消息 `ResignResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-resignresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |

##### 消息 `Event` (api/mvccpb/kv.proto) {#message-event-apimvccpbkvproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| type | type 表示事件类型。若 type 为 PUT，表示已将新数据存储至键。若 type 为 DELETE，表示该键已被删除。 | EventType |
| kv | kv 保存事件对应的 KeyValue。PUT 事件包含当前的键值对。PUT 事件中 kv.Version=1 表示键的创建。DELETE/EXPIRE 事件包含被删除的键，其修改修订版本设置为删除时的修订版本。 | KeyValue |
| prev_kv | prev_kv 保存事件发生前的键值对。 | KeyValue |

##### 消息 `KeyValue` (api/mvccpb/kv.proto) {#message-keyvalue-apimvccpbkvproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| key | key 是以字节形式表示的键。不允许使用空键。 | 字节 |
| create_revision | create_revision 是该键上次创建时的修订版本。 | int64 |
| mod_revision | mod_revision 是该键上次修改时的修订版本。 | int64 |
| version | version 是键的版本号。删除操作会将版本号重置为零，任何对键的修改都会增加其版本号。 | int64 |
| value | value 是键所持有的值，以字节形式表示。 | 字节 |
| lease | lease 是附加到该键的租约 ID。当附加的租约到期时，该键将被删除。若 lease 为 0，则表示该键未附加任何租约。 | int64 |
