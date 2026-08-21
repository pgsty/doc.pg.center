---
title: API 参考
weight: 3800
description: "etcd v3 API 完整参考"
categories: [参考]
upstream_link: "https://github.com/etcd-io/website/blob/a9ee660fdbf9584deb4af639c4dc63b01413e44f/content/en/docs/v3.7/dev-guide/api_reference_v3.md"
---

本文 API 参考由命名的 `.proto` 文件自动生成。

##### 服务 `Auth` (api/etcdserverpb/rpc.proto) {#service-auth-apietcdserverpbrpcproto}

| 方法 | 请求类型 | 响应类型 | 描述 |
| ------ | ------------ | ------------- | ----------- |
| AuthEnable | AuthEnableRequest | AuthEnableResponse | AuthEnable 启用身份认证。 |
| AuthDisable | AuthDisableRequest | AuthDisableResponse | AuthDisable 禁用身份认证。 |
| AuthStatus | AuthStatusRequest | AuthStatusResponse | AuthStatus 显示身份认证状态。 |
| Authenticate | AuthenticateRequest | AuthenticateResponse | Authenticate 处理身份认证请求。 |
| UserAdd | AuthUserAddRequest | AuthUserAddResponse | UserAdd 添加新用户。用户名不能为空。 |
| UserGet | AuthUserGetRequest | AuthUserGetResponse | UserGet 获取用户详细信息。 |
| UserList | AuthUserListRequest | AuthUserListResponse | UserList 获取所有用户的列表。 |
| UserDelete | AuthUserDeleteRequest | AuthUserDeleteResponse | UserDelete 删除指定用户。 |
| UserChangePassword | AuthUserChangePasswordRequest | AuthUserChangePasswordResponse | UserChangePassword 更改指定用户的密码。 |
| UserGrantRole | AuthUserGrantRoleRequest | AuthUserGrantRoleResponse | UserGrant 为指定用户授予角色。 |
| UserRevokeRole | AuthUserRevokeRoleRequest | AuthUserRevokeRoleResponse | UserRevokeRole 撤销指定用户的指定角色。 |
| RoleAdd | AuthRoleAddRequest | AuthRoleAddResponse | RoleAdd 添加新角色。角色名不能为空。 |
| RoleGet | AuthRoleGetRequest | AuthRoleGetResponse | RoleGet 获取角色详细信息。 |
| RoleList | AuthRoleListRequest | AuthRoleListResponse | RoleList 获取所有角色的列表。 |
| RoleDelete | AuthRoleDeleteRequest | AuthRoleDeleteResponse | RoleDelete 删除指定角色。 |
| RoleGrantPermission | AuthRoleGrantPermissionRequest | AuthRoleGrantPermissionResponse | RoleGrantPermission 为指定角色授予指定键或范围的权限。 |
| RoleRevokePermission | AuthRoleRevokePermissionRequest | AuthRoleRevokePermissionResponse | RoleRevokePermission 撤销指定角色的指定键或范围的权限。 |

##### 服务 `Cluster` (api/etcdserverpb/rpc.proto) {#service-cluster-apietcdserverpbrpcproto}

| 方法 | 请求类型 | 响应类型 | 描述 |
| ------ | ------------ | ------------- | ----------- |
| MemberAdd | MemberAddRequest | MemberAddResponse | MemberAdd 将成员添加至集群。 |
| MemberRemove | MemberRemoveRequest | MemberRemoveResponse | MemberRemove 从集群中移除现有成员。 |
| MemberUpdate | MemberUpdateRequest | MemberUpdateResponse | MemberUpdate 更新成员配置。 |
| MemberList | MemberListRequest | MemberListResponse | MemberList 列出集群中的所有成员。 |
| MemberPromote | MemberPromoteRequest | MemberPromoteResponse | MemberPromote 将学习者成员（非投票成员）提升为 Raft 投票成员。 |

##### 服务 `KV` (api/etcdserverpb/rpc.proto) {#service-kv-apietcdserverpbrpcproto}

| 方法 | 请求类型 | 响应类型 | 描述 |
| ------ | ------------ | ------------- | ----------- |
| Range | RangeRequest | RangeResponse | Range 从键值存储中获取指定范围内的键。 |
| Put | PutRequest | PutResponse | Put 将指定键写入键值存储。Put 请求会递增键值存储的修订版本，并在事件历史中生成一个事件。 |
| DeleteRange | DeleteRangeRequest | DeleteRangeResponse | DeleteRange 从键值存储中删除指定范围内的键。删除请求会递增键值存储的修订版本，并为每个被删除的键在事件历史中生成一个删除事件。 |
| Txn | TxnRequest | TxnResponse | Txn 在单个事务中处理多个请求。事务请求会递增键值存储的修订版本，并为每个完成的请求生成具有相同修订版本的事件。不允许在同一个事务中多次修改同一键。 |
| Compact | CompactionRequest | CompactionResponse | Compact 对 etcd 键值存储中的事件历史进行压缩。键值存储应定期执行压缩，否则事件历史将无限增长。 |

##### 服务 `Lease` (api/etcdserverpb/rpc.proto) {#service-lease-apietcdserverpbrpcproto}

| 方法 | 请求类型 | 响应类型 | 描述 |
| ------ | ------------ | ------------- | ----------- |
| LeaseGrant | LeaseGrantRequest | LeaseGrantResponse | LeaseGrant 创建一个租约，若服务器在指定的生存时间（TTL）内未收到保活请求，则该租约将过期。若租约过期，所有关联该租约的键将被过期并删除。每个过期的键都会在事件历史中生成一个删除事件。 |
| LeaseRevoke | LeaseRevokeRequest | LeaseRevokeResponse | LeaseRevoke 撤销一个租约。所有关联该租约的键将过期并被删除。 |
| LeaseKeepAlive | LeaseKeepAliveRequest | LeaseKeepAliveResponse | LeaseKeepAlive 通过客户端向服务器流式发送保活请求，并从服务器流式接收保活响应，以维持租约的活跃状态。 |
| LeaseTimeToLive | LeaseTimeToLiveRequest | LeaseTimeToLiveResponse | LeaseTimeToLive 获取租约信息。 |
| LeaseLeases | LeaseLeasesRequest | LeaseLeasesResponse | LeaseLeases 列出所有现有的租约。 |

##### 服务 `Maintenance` (api/etcdserverpb/rpc.proto) {#service-maintenance-apietcdserverpbrpcproto}

| 方法 | 请求类型 | 响应类型 | 描述 |
| ------ | ------------ | ------------- | ----------- |
| Alarm | AlarmRequest | AlarmResponse | 告警用于激活、停用和查询与集群健康状态相关的告警。 |
| Status | StatusRequest | StatusResponse | 状态用于获取成员的状态。 |
| Defragment | DefragmentRequest | DefragmentResponse | 碎片整理用于对成员的后端数据库进行碎片整理，以恢复存储空间。 |
| Hash | HashRequest | HashResponse | 哈希用于计算整个后端键空间的哈希值，包括存储中的键、租约及其他桶。此功能仅用于测试！请勿在存在持续事务的生产环境中依赖此操作，因为哈希操作不持有 MVCC 锁。如需对“键”桶进行一致性检查，请改用“HashKV” API。 |
| HashKV | HashKVRequest | HashKVResponse | 哈希键用于计算指定修订版本之前所有 MVCC 键的哈希值。它仅遍历后端存储中的“键”桶。 |
| Snapshot | SnapshotRequest | SnapshotResponse | 快照通过流将成员的整个后端数据发送给客户端。 |
| MoveLeader | MoveLeaderRequest | MoveLeaderResponse | 转移领导者用于请求当前领导者将其领导权转移给指定接收节点。 |
| Downgrade | DowngradeRequest | DowngradeResponse | 降级用于请求降级、验证可行性或取消集群版本的降级操作。自 etcd 3.5 起支持。 |

##### 服务 `Watch` (api/etcdserverpb/rpc.proto) {#service-watch-apietcdserverpbrpcproto}

| 方法 | 请求类型 | 响应类型 | 描述 |
| ------ | ------------ | ------------- | ----------- |
| Watch | WatchRequest | WatchResponse | Watch 用于监听发生的事件或已发生的事件。输入和输出均为流；输入流用于创建和取消监听器，输出流用于发送事件。一个 Watch RPC 可以同时监听多个键范围，一次性流式传输多个监听的事件。可以从最后一次压缩的修订版本开始，监听完整的事件历史。 |

##### 消息 `AlarmMember` (api/etcdserverpb/rpc.proto) {#message-alarmmember-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| memberID | memberID 是与触发告警相关的成员的 ID。 | uint64 |
| alarm | alarm 是已触发的告警类型。 | AlarmType |

##### 消息 `AlarmRequest` (api/etcdserverpb/rpc.proto) {#message-alarmrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| action | action 表示要发出的告警请求类型。action 可以是获取告警状态、激活告警，或停用已触发的告警。 | AlarmAction |
| memberID | memberID 表示与告警关联的成员 ID。如果 memberID 为 0，则该告警请求涵盖所有成员。 | uint64 |
| alarm | alarm 表示本次请求所考虑的告警类型。 | AlarmType |

##### 消息 `AlarmResponse` (api/etcdserverpb/rpc.proto) {#message-alarmresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| alarms | alarms 是与告警请求相关联的告警列表。 | (slice of) AlarmMember |

##### 消息 `AuthDisableRequest` (api/etcdserverpb/rpc.proto) {#message-authdisablerequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### 消息 `AuthDisableResponse` (api/etcdserverpb/rpc.proto) {#message-authdisableresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### 消息 `AuthEnableRequest` (api/etcdserverpb/rpc.proto) {#message-authenablerequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### 消息 `AuthEnableResponse` (api/etcdserverpb/rpc.proto) {#message-authenableresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### 消息 `AuthRoleAddRequest` (api/etcdserverpb/rpc.proto) {#message-authroleaddrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name 是要添加到身份认证系统中的角色名称。 | string |

##### 消息 `AuthRoleAddResponse` (api/etcdserverpb/rpc.proto) {#message-authroleaddresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### 消息 `AuthRoleDeleteRequest` (api/etcdserverpb/rpc.proto) {#message-authroledeleterequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| role |  | string |

##### 消息 `AuthRoleDeleteResponse` (api/etcdserverpb/rpc.proto) {#message-authroledeleteresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### 消息 `AuthRoleGetRequest` (api/etcdserverpb/rpc.proto) {#message-authrolegetrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| role |  | string |

##### 消息 `AuthRoleGetResponse` (api/etcdserverpb/rpc.proto) {#message-authrolegetresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| header |  | ResponseHeader |
| perm |  | (切片) authpb.Permission |

##### 消息 `AuthRoleGrantPermissionRequest` (api/etcdserverpb/rpc.proto) {#message-authrolegrantpermissionrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name 是将被授予权限的角色名称。 | string |
| perm | perm 是要授予角色的权限。 | authpb.Permission |

##### 消息 `AuthRoleGrantPermissionResponse` (api/etcdserverpb/rpc.proto) {#message-authrolegrantpermissionresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### 消息 `AuthRoleListRequest` (api/etcdserverpb/rpc.proto) {#message-authrolelistrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### 消息 `AuthRoleListResponse` (api/etcdserverpb/rpc.proto) {#message-authrolelistresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| roles |  | (slice of) string |

##### 消息 `AuthRoleRevokePermissionRequest` (api/etcdserverpb/rpc.proto) {#message-authrolerevokepermissionrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| role |  | string |
| key |  | bytes |
| range_end |  | bytes |

##### 消息 `AuthRoleRevokePermissionResponse` (api/etcdserverpb/rpc.proto) {#message-authrolerevokepermissionresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### 消息 `AuthStatusRequest` (api/etcdserverpb/rpc.proto) {#message-authstatusrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### 消息 `AuthStatusResponse` (api/etcdserverpb/rpc.proto) {#message-authstatusresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| enabled |  | bool |
| authRevision | authRevision 是认证存储系统的当前修订版本 | uint64 |

##### 消息 `AuthUserAddRequest` (api/etcdserverpb/rpc.proto) {#message-authuseraddrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |
| password |  | string |
| options |  | authpb.UserAddOptions |
| hashedPassword |  | string |

##### 消息 `AuthUserAddResponse` (api/etcdserverpb/rpc.proto) {#message-authuseraddresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### 消息 `AuthUserChangePasswordRequest` (api/etcdserverpb/rpc.proto) {#message-authuserchangepasswordrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name 是要更改密码的用户的名称。 | string |
| password | password 是用户的新密码。请注意，该字段将在 API 层被移除。 | string |
| hashedPassword | hashedPassword 是用户的新的哈希密码。请注意，该字段将在 API 层被初始化。 | string |

##### 消息 `AuthUserChangePasswordResponse` (api/etcdserverpb/rpc.proto) {#message-authuserchangepasswordresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### 消息 `AuthUserDeleteRequest` (api/etcdserverpb/rpc.proto) {#message-authuserdeleterequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name 是要删除的用户名称。 | string |

##### 消息 `AuthUserDeleteResponse` (api/etcdserverpb/rpc.proto) {#message-authuserdeleteresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### 消息 `AuthUserGetRequest` (api/etcdserverpb/rpc.proto) {#message-authusergetrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |

##### 消息 `AuthUserGetResponse` (api/etcdserverpb/rpc.proto) {#message-authusergetresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| roles |  | (slice of) string |

##### 消息 `AuthUserGrantRoleRequest` (api/etcdserverpb/rpc.proto) {#message-authusergrantrolerequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| user | user 是应被授予指定角色的用户名。 | string |
| role | role 是应授予用户的角色名称。 | string |

##### 消息 `AuthUserGrantRoleResponse` (api/etcdserverpb/rpc.proto) {#message-authusergrantroleresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### 消息 `AuthUserListRequest` (api/etcdserverpb/rpc.proto) {#message-authuserlistrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### 消息 `AuthUserListResponse` (api/etcdserverpb/rpc.proto) {#message-authuserlistresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| users |  | (slice of) string |

##### 消息 `AuthUserRevokeRoleRequest` (api/etcdserverpb/rpc.proto) {#message-authuserrevokerolerequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |
| role |  | string |

##### 消息 `AuthUserRevokeRoleResponse` (api/etcdserverpb/rpc.proto) {#message-authuserrevokeroleresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### 消息 `AuthenticateRequest` (api/etcdserverpb/rpc.proto) {#message-authenticaterequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |
| password |  | string |

##### 消息 `AuthenticateResponse` (api/etcdserverpb/rpc.proto) {#message-authenticateresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| token | token 是可用于后续 RPC 的授权令牌 | string |

##### 消息 `CompactionRequest` (api/etcdserverpb/rpc.proto) {#message-compactionrequest-apietcdserverpbrpcproto}

CompactionRequest 对键值存储执行压缩，直至指定的修订版本。所有修订版本小于压缩修订版本的已覆盖键将被移除。

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| revision | revision 是执行压缩操作时键值存储的修订版本。 | int64 |
| physical | physical 设置为 true 时，RPC 将等待压缩操作在本地数据库中物理应用，确保已压缩的条目从后端数据库中完全移除。 | bool |

##### 消息 `CompactionResponse` (api/etcdserverpb/rpc.proto) {#message-compactionresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### 消息 `Compare` (api/etcdserverpb/rpc.proto) {#message-compare-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| result | result 是本次比较操作的逻辑比较结果。 | CompareResult |
| target | target 是用于比较的键值字段。 | CompareTarget |
| key | key 是比较操作的主体键。 | bytes |
| target_union |  | oneof |
| version | version 是指定键的版本。 | int64 |
| create_revision | create_revision 是指定键的创建修订版本。 | int64 |
| mod_revision | mod_revision 是指定键的最后一次修改修订版本。 | int64 |
| value | value 是指定键的值，以字节形式表示。 | bytes |
| lease | lease 是指定键的租约 ID。 | int64 |
| range_end | range_end 将指定目标与键范围 [key, range_end) 内的所有键进行比较。有关键范围的更多详情，请参见 RangeRequest。 | bytes |

##### 消息 `DefragmentRequest` (api/etcdserverpb/rpc.proto) {#message-defragmentrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### 消息 `DefragmentResponse` (api/etcdserverpb/rpc.proto) {#message-defragmentresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### 消息 `DeleteRangeRequest` (api/etcdserverpb/rpc.proto) {#message-deleterangerequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | 键是范围中要删除的第一个键。 | bytes |
| range_end | range_end 是范围 [key, range_end) 中最后一个要删除的键的下一个键。若未指定 range_end，则范围仅包含 key 参数。若 range_end 比给定键大一位，则范围包含所有以该键为前缀的键。若 range_end 为 '\0'，则范围包含所有大于或等于 key 参数的键。 | bytes |
| prev_kv | 若设置 prev_kv，etcd 会在删除前获取对应的键值对。删除响应中将返回先前的键值对。 | bool |

##### 消息 `DeleteRangeResponse` (api/etcdserverpb/rpc.proto) {#message-deleterangeresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| deleted | deleted 表示删除范围请求所删除的键的数量。 | int64 |
| prev_kvs | 若请求中设置了 prev_kv，则返回之前的键值对。 | (slice of) mvccpb.KeyValue |

##### 消息 `DowngradeInfo` (api/etcdserverpb/rpc.proto) {#message-downgradeinfo-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| enabled | enabled 表示集群是否启用降级。 | bool |
| targetVersion | targetVersion 是目标降级版本。 | string |

##### 消息 `DowngradeRequest` (api/etcdserverpb/rpc.proto) {#message-downgraderequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| action | action 是要发出的降级请求类型。action 可以是 VALIDATE 目标版本、DOWNGRADE 集群版本，或 CANCEL 当前的降级任务。 | DowngradeAction |
| version | version 是要降级的目标版本。 | string |

##### 消息 `DowngradeResponse` (api/etcdserverpb/rpc.proto) {#message-downgraderesponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| version | version 是当前集群的版本。 | string |

##### 消息 `DowngradeVersionTestRequest` (api/etcdserverpb/rpc.proto) {#message-downgradeversiontestrequest-apietcdserverpbrpcproto}

DowngradeVersionTestRequest 仅用于测试。请求中的版本将被读取为 WAL 记录版本。如果降级目标版本小于该版本，则降级（在线）或迁移（离线）不安全，因此不应允许。

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ver |  | string |

##### 消息 `HashKVRequest` (api/etcdserverpb/rpc.proto) {#message-hashkvrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| revision | 修订版本是哈希操作对应的键值存储修订版本。 | int64 |

##### 消息 `HashKVResponse` (api/etcdserverpb/rpc.proto) {#message-hashkvresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| hash | hash 是响应成员在指定修订版本前的 MVCC 键计算得出的哈希值。 | uint32 |
| compact_revision | compact_revision 是 hash 开始时键值存储的压缩修订版本。 | int64 |
| hash_revision | hash_revision 是哈希计算所覆盖的修订版本。 | int64 |

##### 消息 `HashRequest` (api/etcdserverpb/rpc.proto) {#message-hashrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### 消息 `HashResponse` (api/etcdserverpb/rpc.proto) {#message-hashresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| hash | hash 是响应成员的 KV 后端数据库计算得出的哈希值。 | uint32 |

##### 消息 `LeaseCheckpoint` (api/etcdserverpb/rpc.proto) {#message-leasecheckpoint-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID 是要检查点的租约 ID。 | int64 |
| remaining_TTL | remaining_TTL 是租约到期前剩余的时间。 | int64 |

##### 消息 `LeaseCheckpointRequest` (api/etcdserverpb/rpc.proto) {#message-leasecheckpointrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| checkpoints |  | (slice of) LeaseCheckpoint |

##### 消息 `LeaseCheckpointResponse` (api/etcdserverpb/rpc.proto) {#message-leasecheckpointresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### 消息 `LeaseGrantRequest` (api/etcdserverpb/rpc.proto) {#message-leasegrantrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| TTL | TTL 是建议的存活时间（秒）。过期的租约将返回 -1. | int64 |
| ID | ID 是租约请求的 ID。若 ID 设置为 0，则由租约发放方选择 ID。 | int64 |

##### 消息 `LeaseGrantResponse` (api/etcdserverpb/rpc.proto) {#message-leasegrantresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| ID | ID 是授予租约的租约 ID。 | int64 |
| TTL | TTL 是服务器选定的租约存活时间（秒）。 | int64 |
| error |  | string |

##### 消息 `LeaseKeepAliveRequest` (api/etcdserverpb/rpc.proto) {#message-leasekeepaliverequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID 是要保持保活的租约的租约 ID。 | int64 |

##### 消息 `LeaseKeepAliveResponse` (api/etcdserverpb/rpc.proto) {#message-leasekeepaliveresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| ID | ID 是保活请求中提供的租约 ID。 | int64 |
| TTL | TTL 是租约的新存活时间。 | int64 |

##### 消息 `LeaseLeasesRequest` (api/etcdserverpb/rpc.proto) {#message-leaseleasesrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### 消息 `LeaseLeasesResponse` (api/etcdserverpb/rpc.proto) {#message-leaseleasesresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| leases |  | (slice of) LeaseStatus |

##### 消息 `LeaseRevokeRequest` (api/etcdserverpb/rpc.proto) {#message-leaserevokerequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID 是要撤销的租约 ID。撤销 ID 后，所有关联的键将被删除。 | int64 |

##### 消息 `LeaseRevokeResponse` (api/etcdserverpb/rpc.proto) {#message-leaserevokeresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### 消息 `LeaseStatus` (api/etcdserverpb/rpc.proto) {#message-leasestatus-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID |  | int64 |

##### 消息 `LeaseTimeToLiveRequest` (api/etcdserverpb/rpc.proto) {#message-leasetimetoliverequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID 是该租约的租约 ID。 | int64 |
| keys | keys 为 true 时表示查询与该租约关联的所有键。 | bool |

##### 消息 `LeaseTimeToLiveResponse` (api/etcdserverpb/rpc.proto) {#message-leasetimetoliveresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| ID | ID 是保活请求中提供的租约 ID。 | int64 |
| TTL | TTL 是租约剩余的有效时间（秒）；租约将在不超过 TTL+1 秒内过期。 | int64 |
| grantedTTL | GrantedTTL 是租约创建或续期时授予的初始有效时间（秒）。 | int64 |
| keys | Keys 是附加到该租约的键列表。 | (slice of) bytes |

##### 消息 `Member` (api/etcdserverpb/rpc.proto) {#message-member-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID 是此成员的成员 ID。 | uint64 |
| name | name 是成员的可读名称。如果成员未启动，name 将为空字符串。 | string |
| peerURLs | peerURLs 是成员向集群暴露的用于通信的 URL 列表。 | (slice of) string |
| clientURLs | clientURLs 是成员向客户端暴露的用于通信的 URL 列表。如果成员未启动，clientURLs 将为空。 | (slice of) string |
| isLearner | isLearner 表示该成员是否为 Raft 学习者成员。 | bool |

##### 消息 `MemberAddRequest` (api/etcdserverpb/rpc.proto) {#message-memberaddrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| peerURLs | peerURLs 是新增成员用于与集群通信的 URL 列表。 | (slice of) string |
| isLearner | isLearner 表示新增成员是否为 Raft 学习者成员。 | bool |

##### 消息 `MemberAddResponse` (api/etcdserverpb/rpc.proto) {#message-memberaddresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| member | member 是新增成员的成员信息。 | Member |
| members | members 是添加新成员后所有成员的列表。 | (slice of) Member |

##### 消息 `MemberListRequest` (api/etcdserverpb/rpc.proto) {#message-memberlistrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| linearizable |  | bool |

##### 消息 `MemberListResponse` (api/etcdserverpb/rpc.proto) {#message-memberlistresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | members 是与集群关联的所有成员的列表。 | (slice of) Member |

##### 消息 `MemberPromoteRequest` (api/etcdserverpb/rpc.proto) {#message-memberpromoterequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID 是要提升的成员的成员 ID。 | uint64 |

##### 消息 `MemberPromoteResponse` (api/etcdserverpb/rpc.proto) {#message-memberpromoteresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | members 是提升成员后所有成员的列表。 | (slice of) Member |

##### 消息 `MemberRemoveRequest` (api/etcdserverpb/rpc.proto) {#message-memberremoverequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID 是要移除成员的成员 ID。 | uint64 |

##### 消息 `MemberRemoveResponse` (api/etcdserverpb/rpc.proto) {#message-memberremoveresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | members 是移除成员后所有成员的列表。 | (slice of) Member |

##### 消息 `MemberUpdateRequest` (api/etcdserverpb/rpc.proto) {#message-memberupdaterequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID 是待更新成员的成员 ID。 | uint64 |
| peerURLs | peerURLs 是成员与集群通信所使用的新的 URL 列表。 | (slice of) string |

##### 消息 `MemberUpdateResponse` (api/etcdserverpb/rpc.proto) {#message-memberupdateresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | members 是更新成员后所有成员的列表。 | (slice of) Member |

##### 消息 `MoveLeaderRequest` (api/etcdserverpb/rpc.proto) {#message-moveleaderrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| targetID | targetID 是新领导者的节点 ID。 | uint64 |

##### 消息 `MoveLeaderResponse` (api/etcdserverpb/rpc.proto) {#message-moveleaderresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### 消息 `PutRequest` (api/etcdserverpb/rpc.proto) {#message-putrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | key 是要存入键值对存储的键，以字节形式表示。 | bytes |
| value | value 是要与键关联的值，以字节形式表示。 | bytes |
| lease | lease 是要与键关联的租约 ID。租约值为 0 表示无租约。 | int64 |
| prev_kv | 若设置 prev_kv，etcd 在修改前获取该键的先前键值对。先前的键值对将在 put 响应中返回。 | bool |
| ignore_value | 若设置 ignore_value，etcd 使用键的当前值更新键。若键不存在，则返回错误。 | bool |
| ignore_lease | 若设置 ignore_lease，etcd 使用键的当前租约更新键。若键不存在，则返回错误。 | bool |

##### 消息 `PutResponse` (api/etcdserverpb/rpc.proto) {#message-putresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| prev_kv | 若请求中设置了 prev_kv，则返回之前的键值对。 | mvccpb.KeyValue |

##### 消息 `RangeRequest` (api/etcdserverpb/rpc.proto) {#message-rangerequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | key 是范围的第一个键。若未指定 range_end，则请求仅查找该键。 | bytes |
| range_end | range_end 是请求范围 [key, range_end) 的上界。若 range_end 为 '\0'，则范围为所有大于等于 key 的键。若 range_end 为 key 加一（例如 "aa"+1 == "ab"，"a\xff"+1 == "b"），则范围请求获取所有以 key 为前缀的键。若 key 和 range_end 均为 '\0'，则范围请求返回所有键。 | bytes |
| limit | limit 是请求返回键数量的限制。当 limit 设置为 0 时，视为无限制。 | int64 |
| revision | revision 是用于范围请求的键值存储的时间点。若 revision 小于或等于零，则范围针对最新的键值存储。若该修订版本已被压缩，则返回 ErrCompacted 作为响应。 | int64 |
| sort_order | sort_order 是返回结果排序的顺序。 | SortOrder |
| sort_target | sort_target 是用于排序的键值字段。 | SortTarget |
| serializable | serializable 将范围请求设置为使用可序列化成员本地读取。范围请求默认为线性一致；线性一致请求的延迟较高、吞吐量较低，但反映集群当前的共识状态。为获得更好性能，可接受可能的陈旧读取，可序列化范围请求在本地服务，无需与其他节点达成共识。 | bool |
| keys_only | keys_only 为真时，仅返回键而不返回值。 | bool |
| count_only | count_only 为真时，仅返回范围内键的数量。 | bool |
| min_mod_revision | min_mod_revision 是返回键修改修订版本的下界；所有修改修订版本较小的键将被过滤掉。 | int64 |
| max_mod_revision | max_mod_revision 是返回键修改修订版本的上界；所有修改修订版本较大的键将被过滤掉。 | int64 |
| min_create_revision | min_create_revision 是返回键创建修订版本的下界；所有创建修订版本较小的键将被过滤掉。 | int64 |
| max_create_revision | max_create_revision 是返回键创建修订版本的上界；所有创建修订版本较大的键将被过滤掉。 | int64 |

##### 消息 `RangeResponse` (api/etcdserverpb/rpc.proto) {#message-rangeresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| kvs | kvs 是范围请求匹配的键值对列表。当请求计数时，kvs 为空。 | (slice of) mvccpb.KeyValue |
| more | more 表示在请求的范围内是否还有更多键待返回。 | bool |
| count | 当请求计数时，count 设置为指定范围内实际的键数量。与 kvs 不同，它不受限制和过滤器（例如 Min/Max、Create/Modify、Revisions）影响，反映指定范围内完整的键数量。 | int64 |

##### 消息 `RequestOp` (api/etcdserverpb/rpc.proto) {#message-requestop-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| request | request 是事务接受的请求类型的联合。 | oneof |
| request_range |  | RangeRequest |
| request_put |  | PutRequest |
| request_delete_range |  | DeleteRangeRequest |
| request_txn |  | TxnRequest |

##### 消息 `ResponseHeader` (api/etcdserverpb/rpc.proto) {#message-responseheader-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| cluster_id | cluster_id 是发送响应的集群的 ID。 | uint64 |
| member_id | member_id 是发送响应的成员的 ID。 | uint64 |
| revision | revision 是请求被应用时键值存储的修订版本，对于不与键值存储交互的调用，该字段未设置（即为 0）。对于监听进度响应，header.revision 表示进度。在此流中接收到的所有未来事件的修订版本号均保证高于 header.revision 号。 | int64 |
| raft_term | raft_term 是请求被应用时的 Raft 任期。 | uint64 |

##### 消息 `ResponseOp` (api/etcdserverpb/rpc.proto) {#message-responseop-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| response | response 是事务返回的响应类型集合。 | oneof |
| response_range |  | RangeResponse |
| response_put |  | PutResponse |
| response_delete_range |  | DeleteRangeResponse |
| response_txn |  | TxnResponse |

##### 消息 `SnapshotRequest` (api/etcdserverpb/rpc.proto) {#message-snapshotrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### 消息 `SnapshotResponse` (api/etcdserverpb/rpc.proto) {#message-snapshotresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header | header 包含当前键值存储的信息。快照流中的第一个 header 指示快照的时间点。 | ResponseHeader |
| remaining_bytes | remaining_bytes 表示在本消息之后还需发送的 blob 字节数。 | uint64 |
| blob | blob 包含快照流中的下一个快照数据块。 | bytes |
| version | 创建快照的本地服务器版本。在运行不同版本二进制文件的集群中，各集群可能返回不同结果。用于告知恢复快照时应使用的 etcd 服务器版本。 | string |

##### 消息 `StatusRequest` (api/etcdserverpb/rpc.proto) {#message-statusrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### 消息 `StatusResponse` (api/etcdserverpb/rpc.proto) {#message-statusresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| version | version 是响应成员所使用的集群协议版本。 | string |
| dbSize | dbSize 是响应成员后端数据库实际分配的大小，单位为字节。 | int64 |
| leader | leader 是响应成员认为当前的领导者成员 ID。 | uint64 |
| raftIndex | raftIndex 是响应成员当前 Raft 已提交索引。 | uint64 |
| raftTerm | raftTerm 是响应成员当前的 Raft 任期。 | uint64 |
| raftAppliedIndex | raftAppliedIndex 是响应成员当前 Raft 已应用索引。 | uint64 |
| errors | errors 包含告警/健康信息和状态。 | (slice of) string |
| dbSizeInUse | dbSizeInUse 是响应成员后端数据库逻辑上正在使用的大小，单位为字节。 | int64 |
| isLearner | isLearner 表示该成员是否为 Raft 学习者成员。 | bool |
| storageVersion | storageVersion 是数据库文件的版本。该版本可能与目标集群版本存在延迟更新。 | string |
| dbSizeQuota | dbSizeQuota 是配置的 etcd 存储配额，单位为字节（由标志 --quota-backend-bytes 传递给 etcd 实例）。 | int64 |
| downgradeInfo | downgradeInfo 表示是否存在降级过程。 | DowngradeInfo |

##### 消息 `TxnRequest` (api/etcdserverpb/rpc.proto) {#message-txnrequest-apietcdserverpbrpcproto}

MultiOp 原语

源自 Google PaxosDB 论文：我们的实现基于一种强大的原语，称为 MultiOp。除迭代外，所有数据库操作均通过一次 MultiOp 调用实现。MultiOp 以原子方式应用，包含三个组成部分：1. 一组称为 guard 的测试。guard 中的每个测试检查数据库中的单个条目。测试可检查值是否存在或不存在，或与给定值进行比较。guard 中的两个不同测试可作用于数据库中的同一或不同条目。所有测试均被应用，MultiOp 返回测试结果。若所有测试均为真，则执行 t op（参见下文第 2 项），否则执行 f op（参见下文第 3 项）。2. 一组称为 t op 的数据库操作。列表中的每个操作为插入、删除或查找操作，且作用于单个数据库条目。列表中的两个不同操作可作用于数据库中的同一或不同条目。当 guard 求值为真时执行这些操作。3. 一组称为 f op 的数据库操作。与 t op 类似，但在 guard 求值为假时执行。

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| compare | compare 是一组表示逻辑与关系的谓词。如果比较成功，则按顺序处理 success 请求，并在响应中按顺序返回各自的响应。如果比较失败，则按顺序处理 failure 请求，并在响应中按顺序返回各自的响应。 | (slice of) Compare |
| success | success 是一组在 compare 求值为 true 时执行的请求。 | (slice of) RequestOp |
| failure | failure 是一组在 compare 求值为 false 时执行的请求。 | (slice of) RequestOp |

##### 消息 `TxnResponse` (api/etcdserverpb/rpc.proto) {#message-txnresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| succeeded | 如果 compare 的评估结果为 true，则 succeeded 设置为 true；否则为 false。 | bool |
| responses | responses 是一个响应列表，对应于当 succeeded 为 true 时执行成功的结果，或当 succeeded 为 false 时执行失败的结果。 | (slice of) ResponseOp |

##### 消息 `WatchCancelRequest` (api/etcdserverpb/rpc.proto) {#message-watchcancelrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| watch_id | watch_id 是要取消的监听器 ID，取消后将不再传输事件。 | int64 |

##### 消息 `WatchCreateRequest` (api/etcdserverpb/rpc.proto) {#message-watchcreaterequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | key 是要监听的键。 | bytes |
| range_end | range_end 是要监听的范围 [key, range_end) 的结束位置。若未提供 range_end，则仅监听 key 参数指定的键。若 range_end 等于 '\0'，则监听所有大于或等于 key 参数的键。若 range_end 比给定键大一位，则监听所有具有该前缀（即给定键）的键。 | bytes |
| start_revision | start_revision 是可选的监听起始修订版本（包含）。未指定 start_revision 表示“现在”。 | int64 |
| progress_notify | progress_notify 设置后，若无新事件，etcd 服务器将定期向新监听器发送不包含事件的 WatchResponse。此功能在客户端希望从最近已知修订版本恢复断开的监听器时非常有用。etcd 服务器可根据当前负载决定通知发送的频率。 | bool |
| filters | filters 用于在服务器端过滤事件，再发送给监听器。 | (slice of) FilterType |
| prev_kv | 若设置 prev_kv，监听器将在事件发生前获取对应的前一个 KV。若前一个 KV 已被压缩，则不会返回任何内容。 | bool |
| watch_id | 若提供非零的 watch_id，该 ID 将被分配给此监听器。由于在 etcd 中创建监听器并非同步操作，因此可通过该 ID 确保在同一流上创建多个监听器时顺序正确。若在流上已存在相同 ID 的监听器，则创建操作将返回错误。 | int64 |
| fragment | fragment 启用将大修订版本拆分为多个监听响应。 | bool |

##### 消息 `WatchProgressRequest` (api/etcdserverpb/rpc.proto) {#message-watchprogressrequest-apietcdserverpbrpcproto}

请求在监听响应流中尽快发送监听流进度状态。

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### 消息 `WatchRequest` (api/etcdserverpb/rpc.proto) {#message-watchrequest-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| request_union | request_union 是创建新监听器或取消现有监听器的请求。 | oneof |
| create_request |  | WatchCreateRequest |
| cancel_request |  | WatchCancelRequest |
| progress_request |  | WatchProgressRequest |

##### 消息 `WatchResponse` (api/etcdserverpb/rpc.proto) {#message-watchresponse-apietcdserverpbrpcproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| watch_id | watch_id 是与响应对应监听器的 ID。 | int64 |
| created | 如果响应对应创建监听请求，则 created 被设置为 true。客户端应记录 watch_id，并期望从同一流中接收该监听器的事件。发送给该监听器的所有事件都将附加相同的 watch_id。 | bool |
| canceled | 如果响应对应取消监听请求，或 start_revision 已被压缩，则 canceled 被设置为 true。不再向已取消的监听器发送任何事件。 | bool |
| compact_revision | 如果监听器尝试在已被压缩的索引处监听，则 compact_revision 被设置为最小索引。这种情况发生在以已被压缩的修订版本创建监听器，或监听器无法跟上键值存储进度时。客户端应将监听器视为已取消，并不应再尝试以相同 start_revision 创建监听器。 | int64 |
| cancel_reason | cancel_reason 表示取消监听器的原因。 | string |
| fragment | 如果大型监听响应被拆分到多个响应中，则 fragment 为 true。 | bool |
| events |  | (slice of) mvccpb.Event |

##### 消息 `Event` (api/mvccpb/kv.proto) {#message-event-apimvccpbkvproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| type | type 表示事件类型。若 type 为 PUT，表示已将新数据存储至键。若 type 为 DELETE，表示该键已被删除。 | EventType |
| kv | kv 保存事件对应的 KeyValue。PUT 事件包含当前的键值对。PUT 事件中 kv.Version=1 表示键的创建。DELETE/EXPIRE 事件包含被删除的键，其修改修订版本设置为删除时的修订版本。 | KeyValue |
| prev_kv | prev_kv 保存事件发生前的键值对。 | KeyValue |

##### 消息 `KeyValue` (api/mvccpb/kv.proto) {#message-keyvalue-apimvccpbkvproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| key | key 是以字节表示的键。不允许使用空键。 | bytes |
| create_revision | create_revision 是该键上次创建时的修订版本。 | int64 |
| mod_revision | mod_revision 是该键上次修改时的修订版本。 | int64 |
| version | version 是键的版本号。删除操作会将版本号重置为零，任何对键的修改都会增加其版本号。 | int64 |
| value | value 是键所持有的值，以字节表示。 | bytes |
| lease | lease 是附加到该键的租约 ID。当附加的租约到期时，该键将被删除。若 lease 为 0，则表示该键未附加任何租约。 | int64 |

##### 消息 `Lease` (server/lease/leasepb/lease.proto) {#message-lease-serverleaseleasepbleaseproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| ID |  | int64 |
| TTL |  | int64 |
| RemainingTTL |  | int64 |

##### 消息 `LeaseInternalRequest` (server/lease/leasepb/lease.proto) {#message-leaseinternalrequest-serverleaseleasepbleaseproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| LeaseTimeToLiveRequest |  | etcdserverpb.LeaseTimeToLiveRequest |

##### 消息 `LeaseInternalResponse` (server/lease/leasepb/lease.proto) {#message-leaseinternalresponse-serverleaseleasepbleaseproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| LeaseTimeToLiveResponse |  | etcdserverpb.LeaseTimeToLiveResponse |

##### 消息 `Permission` (api/authpb/auth.proto) {#message-permission-apiauthpbauthproto}

权限是一个单一实体

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| permType |  | 类型 |
| key |  | bytes |
| range_end |  | bytes |

##### message `Role` (api/authpb/auth.proto) {#message-role-apiauthpbauthproto}

角色是 authRoles 存储桶中的单个条目。

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| name |  | bytes |
| keyPermission |  | (切片) Permission |

##### message `User` (api/authpb/auth.proto) {#message-user-apiauthpbauthproto}

用户是存储桶 authUsers 中的单个条目

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| name |  | bytes |
| password |  | bytes |
| roles |  | (slice of) string |
| options |  | UserAddOptions |

##### message `UserAddOptions` (api/authpb/auth.proto) {#message-useraddoptions-apiauthpbauthproto}

| 字段 | 描述 | 类型 |
| ----- | ----------- | ---- |
| no_password |  | bool |
