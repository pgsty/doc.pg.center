---
title: APIリファレンス
weight: 3800
description: "etcd v3 APIの完全なリファレンス"
categories: [リファレンス]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/api_reference_v3.md"
---

このAPIリファレンスは、各見出しに記載した`.proto`ファイルから自動生成されています。

##### サービス `Auth` (api/etcdserverpb/rpc.proto) {#service-auth-apietcdserverpbrpcproto}

| メソッド | リクエスト型 | レスポンス型 | 説明 |
| ------ | ------------ | ------------- | ----------- |
| AuthEnable | AuthEnableRequest | AuthEnableResponse | AuthEnableは認証を有効にします。 |
| AuthDisable | AuthDisableRequest | AuthDisableResponse | AuthDisableは認証を無効にします。 |
| AuthStatus | AuthStatusRequest | AuthStatusResponse | AuthStatusは認証の状態を表示します。 |
| Authenticate | AuthenticateRequest | AuthenticateResponse | Authenticateは認証リクエストを処理します。 |
| UserAdd | AuthUserAddRequest | AuthUserAddResponse | UserAddは新しいユーザーを追加します。ユーザー名は空にできません。 |
| UserGet | AuthUserGetRequest | AuthUserGetResponse | UserGetはユーザーの詳細情報を取得します。 |
| UserList | AuthUserListRequest | AuthUserListResponse | UserListはすべてのユーザーの一覧を取得します。 |
| UserDelete | AuthUserDeleteRequest | AuthUserDeleteResponse | UserDeleteは指定したユーザーを削除します。 |
| UserChangePassword | AuthUserChangePasswordRequest | AuthUserChangePasswordResponse | UserChangePasswordは指定したユーザーのパスワードを変更します。 |
| UserGrantRole | AuthUserGrantRoleRequest | AuthUserGrantRoleResponse | UserGrantRoleは指定したユーザーにロールを付与します。 |
| UserRevokeRole | AuthUserRevokeRoleRequest | AuthUserRevokeRoleResponse | UserRevokeRoleは指定したユーザーからロールを取り消します。 |
| RoleAdd | AuthRoleAddRequest | AuthRoleAddResponse | RoleAddは新しいロールを追加します。ロール名は空にできません。 |
| RoleGet | AuthRoleGetRequest | AuthRoleGetResponse | RoleGetはロールの詳細情報を取得します。 |
| RoleList | AuthRoleListRequest | AuthRoleListResponse | RoleListはすべてのロールの一覧を取得します。 |
| RoleDelete | AuthRoleDeleteRequest | AuthRoleDeleteResponse | RoleDeleteは指定したロールを削除します。 |
| RoleGrantPermission | AuthRoleGrantPermissionRequest | AuthRoleGrantPermissionResponse | RoleGrantPermissionは、指定したキーまたは範囲に対する権限を、指定したロールに付与します。 |
| RoleRevokePermission | AuthRoleRevokePermissionRequest | AuthRoleRevokePermissionResponse | RoleRevokePermissionは、指定したロールからキーまたは範囲に対する権限を取り消します。 |

##### サービス `Cluster` (api/etcdserverpb/rpc.proto) {#service-cluster-apietcdserverpbrpcproto}

| メソッド | リクエスト型 | レスポンス型 | 説明 |
| ------ | ------------ | ------------- | ----------- |
| MemberAdd | MemberAddRequest | MemberAddResponse | MemberAddはクラスターにメンバーを追加します。 |
| MemberRemove | MemberRemoveRequest | MemberRemoveResponse | MemberRemoveはクラスターから既存のメンバーを削除します。 |
| MemberUpdate | MemberUpdateRequest | MemberUpdateResponse | MemberUpdateはメンバーの構成を更新します。 |
| MemberList | MemberListRequest | MemberListResponse | MemberListはクラスター内のすべてのメンバーを一覧表示します。 |
| MemberPromote | MemberPromoteRequest | MemberPromoteResponse | MemberPromoteは、Raftの学習者メンバー（投票権なし）を、Raftの投票メンバーに昇格させます。 |

##### サービス `KV` (api/etcdserverpb/rpc.proto) {#service-kv-apietcdserverpbrpcproto}

| メソッド | リクエスト型 | レスポンス型 | 説明 |
| ------ | ------------ | ------------- | ----------- |
| Range | RangeRequest | RangeResponse | Rangeはキー・バリューストアから範囲内のキーを取得します。 |
| Put | PutRequest | PutResponse | Putは指定したキーをキー・バリューストアに格納します。putリクエストはキー・バリューストアのリビジョンを増加させ、イベント履歴に1つのイベントを生成します。 |
| DeleteRange | DeleteRangeRequest | DeleteRangeResponse | DeleteRangeはキー・バリューストアから指定した範囲を削除します。deleteリクエストはキー・バリューストアのリビジョンを増加させ、削除したキーごとにイベント履歴に削除イベントを生成します。 |
| Txn | TxnRequest | TxnResponse | Txnは1つのトランザクション内で複数のリクエストを処理します。txnリクエストはキー・バリューストアのリビジョンを増加させ、完了したリクエストごとに、同じリビジョンを持つイベントを生成します。1つのtxn内で同じキーを複数回変更することはできません。 |
| Compact | CompactionRequest | CompactionResponse | Compactは、etcdキー・バリューストアのイベント履歴をコンパクションします。キー・バリューストアは定期的にコンパクションすることを推奨します。そうしないと、イベント履歴は無制限に増え続けます。 |

##### サービス `Lease` (api/etcdserverpb/rpc.proto) {#service-lease-apietcdserverpbrpcproto}

| メソッド | リクエスト型 | レスポンス型 | 説明 |
| ------ | ------------ | ------------- | ----------- |
| LeaseGrant | LeaseGrantRequest | LeaseGrantResponse | LeaseGrantは、指定した生存時間内にサーバーがkeepAliveを受信しないと期限切れになるリースを作成します。リースが期限切れになると、それに関連付けられたすべてのキーも期限切れになり、削除されます。期限切れになった各キーは、イベント履歴に削除イベントを生成します。 |
| LeaseRevoke | LeaseRevokeRequest | LeaseRevokeResponse | LeaseRevokeはリースを取り消します。リースに関連付けられたすべてのキーは期限切れになり、削除されます。 |
| LeaseKeepAlive | LeaseKeepAliveRequest | LeaseKeepAliveResponse | LeaseKeepAliveは、クライアントからサーバーへキープアライブリクエストをストリーミングし、サーバーからクライアントへキープアライブレスポンスをストリーミングすることで、リースを維持します。 |
| LeaseTimeToLive | LeaseTimeToLiveRequest | LeaseTimeToLiveResponse | LeaseTimeToLiveはリース情報を取得します。 |
| LeaseLeases | LeaseLeasesRequest | LeaseLeasesResponse | LeaseLeasesは既存のすべてのリースを一覧表示します。 |

##### サービス `Maintenance` (api/etcdserverpb/rpc.proto) {#service-maintenance-apietcdserverpbrpcproto}

| メソッド | リクエスト型 | レスポンス型 | 説明 |
| ------ | ------------ | ------------- | ----------- |
| Alarm | AlarmRequest | AlarmResponse | Alarmは、クラスターの健全性に関するアラームの有効化、解除、照会を行います。 |
| Status | StatusRequest | StatusResponse | Statusはメンバーの状態を取得します。 |
| Defragment | DefragmentRequest | DefragmentResponse | Defragmentは、メンバーのバックエンドデータベースをデフラグメンテーションして、ストレージ領域を回収します。 |
| Hash | HashRequest | HashResponse | Hashは、ストレージ内のkey、lease、その他のバケットを含む、バックエンドのキー空間全体のハッシュを計算します。これはテスト専用です！Hash操作はMVCCロックを保持しないため、トランザクションが進行している本番環境では、この操作に依存しないでください。"key"バケットの整合性チェックには、代わりに"HashKV" APIを使用してください。 |
| HashKV | HashKVRequest | HashKVResponse | HashKVは、指定したリビジョンまでのすべてのMVCCキーのハッシュを計算します。バックエンドストレージの"key"バケットだけを走査します。 |
| Snapshot | SnapshotRequest | SnapshotResponse | Snapshotは、バックエンド全体のスナップショットを、メンバーからクライアントへストリームで送信します。 |
| MoveLeader | MoveLeaderRequest | MoveLeaderResponse | MoveLeaderは、現在のリーダーノードに対し、移譲先へリーダーシップを移すよう要求します。 |
| Downgrade | DowngradeRequest | DowngradeResponse | Downgradeは、クラスターのバージョンのダウングレードの要求、実行可能性の検証、またはダウングレードの取り消しを行います。etcd 3.5以降でサポートされています。 |

##### サービス `Watch` (api/etcdserverpb/rpc.proto) {#service-watch-apietcdserverpbrpcproto}

| メソッド | リクエスト型 | レスポンス型 | 説明 |
| ------ | ------------ | ------------- | ----------- |
| Watch | WatchRequest | WatchResponse | Watchは、現在または過去に発生したイベントを監視します。入力と出力はどちらもストリームです。入力ストリームはウォッチャーの作成とキャンセルに使用し、出力ストリームはイベントを送信します。1つのwatch RPCで複数のキー範囲を監視し、複数の監視のイベントを同時にストリーミングできます。最後のコンパクションリビジョン以降のイベント履歴全体を監視できます。 |

##### メッセージ `AlarmMember` (api/etcdserverpb/rpc.proto) {#message-alarmmember-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| memberID | memberIDは、発報されたアラームに関連付けられたメンバーのIDです。 | uint64 |
| alarm | alarmは、発報されたアラームの種類です。 | AlarmType |

##### メッセージ `AlarmRequest` (api/etcdserverpb/rpc.proto) {#message-alarmrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| action | actionは、発行するアラームリクエストの種類です。アクションには、アラーム状態のGET、アラームのACTIVATE、発報済みアラームのDEACTIVATEがあります。 | AlarmAction |
| memberID | memberIDは、アラームに関連付けられたメンバーのIDです。memberIDが0の場合、アラームリクエストはすべてのメンバーを対象とします。 | uint64 |
| alarm | alarmは、このリクエストで対象とするアラームの種類です。 | AlarmType |

##### メッセージ `AlarmResponse` (api/etcdserverpb/rpc.proto) {#message-alarmresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| alarms | alarmsは、アラームリクエストに関連付けられたアラームの一覧です。 | (slice of) AlarmMember |

##### メッセージ `AuthDisableRequest` (api/etcdserverpb/rpc.proto) {#message-authdisablerequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### メッセージ `AuthDisableResponse` (api/etcdserverpb/rpc.proto) {#message-authdisableresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### メッセージ `AuthEnableRequest` (api/etcdserverpb/rpc.proto) {#message-authenablerequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### メッセージ `AuthEnableResponse` (api/etcdserverpb/rpc.proto) {#message-authenableresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### メッセージ `AuthRoleAddRequest` (api/etcdserverpb/rpc.proto) {#message-authroleaddrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | nameは、認証システムに追加するロールの名前です。 | string |

##### メッセージ `AuthRoleAddResponse` (api/etcdserverpb/rpc.proto) {#message-authroleaddresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### メッセージ `AuthRoleDeleteRequest` (api/etcdserverpb/rpc.proto) {#message-authroledeleterequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| role |  | string |

##### メッセージ `AuthRoleDeleteResponse` (api/etcdserverpb/rpc.proto) {#message-authroledeleteresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### メッセージ `AuthRoleGetRequest` (api/etcdserverpb/rpc.proto) {#message-authrolegetrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| role |  | string |

##### メッセージ `AuthRoleGetResponse` (api/etcdserverpb/rpc.proto) {#message-authrolegetresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| header |  | ResponseHeader |
| perm |  | (slice of) authpb.Permission |

##### メッセージ `AuthRoleGrantPermissionRequest` (api/etcdserverpb/rpc.proto) {#message-authrolegrantpermissionrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | nameは、権限を付与するロールの名前です。 | string |
| perm | permは、ロールに付与する権限です。 | authpb.Permission |

##### メッセージ `AuthRoleGrantPermissionResponse` (api/etcdserverpb/rpc.proto) {#message-authrolegrantpermissionresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### メッセージ `AuthRoleListRequest` (api/etcdserverpb/rpc.proto) {#message-authrolelistrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### メッセージ `AuthRoleListResponse` (api/etcdserverpb/rpc.proto) {#message-authrolelistresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| roles |  | (slice of) string |

##### メッセージ `AuthRoleRevokePermissionRequest` (api/etcdserverpb/rpc.proto) {#message-authrolerevokepermissionrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| role |  | string |
| key |  | bytes |
| range_end |  | bytes |

##### メッセージ `AuthRoleRevokePermissionResponse` (api/etcdserverpb/rpc.proto) {#message-authrolerevokepermissionresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### メッセージ `AuthStatusRequest` (api/etcdserverpb/rpc.proto) {#message-authstatusrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### メッセージ `AuthStatusResponse` (api/etcdserverpb/rpc.proto) {#message-authstatusresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| enabled |  | bool |
| authRevision | authRevisionは、認証ストアの現在のリビジョンです。 | uint64 |

##### メッセージ `AuthUserAddRequest` (api/etcdserverpb/rpc.proto) {#message-authuseraddrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |
| password |  | string |
| options |  | authpb.UserAddOptions |
| hashedPassword |  | string |

##### メッセージ `AuthUserAddResponse` (api/etcdserverpb/rpc.proto) {#message-authuseraddresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### メッセージ `AuthUserChangePasswordRequest` (api/etcdserverpb/rpc.proto) {#message-authuserchangepasswordrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | nameは、パスワードを変更するユーザーの名前です。 | string |
| password | passwordは、ユーザーの新しいパスワードです。このフィールドはAPIレイヤーで削除されることに注意してください。 | string |
| hashedPassword | hashedPasswordは、ユーザーの新しいパスワードのハッシュ値です。このフィールドはAPIレイヤーで初期化されることに注意してください。 | string |

##### メッセージ `AuthUserChangePasswordResponse` (api/etcdserverpb/rpc.proto) {#message-authuserchangepasswordresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### メッセージ `AuthUserDeleteRequest` (api/etcdserverpb/rpc.proto) {#message-authuserdeleterequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | nameは、削除するユーザーの名前です。 | string |

##### メッセージ `AuthUserDeleteResponse` (api/etcdserverpb/rpc.proto) {#message-authuserdeleteresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### メッセージ `AuthUserGetRequest` (api/etcdserverpb/rpc.proto) {#message-authusergetrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |

##### メッセージ `AuthUserGetResponse` (api/etcdserverpb/rpc.proto) {#message-authusergetresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| roles |  | (slice of) string |

##### メッセージ `AuthUserGrantRoleRequest` (api/etcdserverpb/rpc.proto) {#message-authusergrantrolerequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| user | userは、指定したロールを付与するユーザーの名前です。 | string |
| role | roleは、ユーザーに付与するロールの名前です。 | string |

##### メッセージ `AuthUserGrantRoleResponse` (api/etcdserverpb/rpc.proto) {#message-authusergrantroleresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### メッセージ `AuthUserListRequest` (api/etcdserverpb/rpc.proto) {#message-authuserlistrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### メッセージ `AuthUserListResponse` (api/etcdserverpb/rpc.proto) {#message-authuserlistresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| users |  | (slice of) string |

##### メッセージ `AuthUserRevokeRoleRequest` (api/etcdserverpb/rpc.proto) {#message-authuserrevokerolerequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |
| role |  | string |

##### メッセージ `AuthUserRevokeRoleResponse` (api/etcdserverpb/rpc.proto) {#message-authuserrevokeroleresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### メッセージ `AuthenticateRequest` (api/etcdserverpb/rpc.proto) {#message-authenticaterequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |
| password |  | string |

##### メッセージ `AuthenticateResponse` (api/etcdserverpb/rpc.proto) {#message-authenticateresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| token | tokenは、後続のRPCで使用できる認可済みトークンです。 | string |

##### メッセージ `CompactionRequest` (api/etcdserverpb/rpc.proto) {#message-compactionrequest-apietcdserverpbrpcproto}

CompactionRequestは、指定したリビジョンまでのキー・バリューストアをコンパクションします。コンパクションリビジョンより小さいリビジョンを持つ、更新によって古くなったキーはすべて削除されます。

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| revision | revisionは、コンパクション操作の対象となるキー・バリューストアのリビジョンです。 | int64 |
| physical | physicalを設定すると、RPCはコンパクションがローカルデータベースに物理的に適用され、対象のエントリーがバックエンドデータベースから完全に削除されるまで待機します。 | bool |

##### メッセージ `CompactionResponse` (api/etcdserverpb/rpc.proto) {#message-compactionresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### メッセージ `Compare` (api/etcdserverpb/rpc.proto) {#message-compare-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| result | resultは、この比較で使用する論理比較演算です。 | CompareResult |
| target | targetは、比較のために調べるキー・バリューのフィールドです。 | CompareTarget |
| key | keyは、比較操作の対象となるキーです。 | bytes |
| target_union |  | oneof |
| version | versionは、指定したキーのバージョンです。 | int64 |
| create_revision | create_revisionは、指定したキーの作成リビジョンです。 | int64 |
| mod_revision | mod_revisionは、指定したキーの最終変更リビジョンです。 | int64 |
| value | valueは、指定したキーの値をバイト列で表したものです。 | bytes |
| lease | leaseは、指定したキーのリースIDです。 | int64 |
| range_end | range_endは、指定したtargetを範囲[key, range_end)内のすべてのキーと比較します。キー範囲の詳細はRangeRequestを参照してください。 | bytes |

##### メッセージ `DefragmentRequest` (api/etcdserverpb/rpc.proto) {#message-defragmentrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### メッセージ `DefragmentResponse` (api/etcdserverpb/rpc.proto) {#message-defragmentresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### メッセージ `DeleteRangeRequest` (api/etcdserverpb/rpc.proto) {#message-deleterangerequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | keyは、範囲内で削除する最初のキーです。 | bytes |
| range_end | range_endは、範囲[key, range_end)内で削除する最後のキーの次のキーです。range_endが指定されていない場合、範囲にはkey引数だけが含まれます。range_endが指定したキーに1を加えた値の場合、範囲にはそのキーを接頭辞に持つすべてのキーが含まれます。range_endが'\0'の場合、範囲にはkey引数以上のすべてのキーが含まれます。 | bytes |
| prev_kv | prev_kvが設定されている場合、etcdは削除前のキー・バリューペアを取得します。削除前のキー・バリューペアはdeleteレスポンスで返されます。 | bool |

##### メッセージ `DeleteRangeResponse` (api/etcdserverpb/rpc.proto) {#message-deleterangeresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| deleted | deletedは、範囲削除リクエストによって削除されたキーの数です。 | int64 |
| prev_kvs | リクエストにprev_kvが設定されている場合、削除前のキー・バリューペアが返されます。 | (slice of) mvccpb.KeyValue |

##### メッセージ `DowngradeInfo` (api/etcdserverpb/rpc.proto) {#message-downgradeinfo-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| enabled | enabledは、クラスターのダウングレードが有効になっているかどうかを示します。 | bool |
| targetVersion | targetVersionは、ダウングレード先のバージョンです。 | string |

##### メッセージ `DowngradeRequest` (api/etcdserverpb/rpc.proto) {#message-downgraderequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| action | actionは、発行するダウングレードリクエストの種類です。アクションには、対象バージョンのVALIDATE、クラスターバージョンのDOWNGRADE、現在のダウングレードジョブのCANCELがあります。 | DowngradeAction |
| version | versionは、ダウングレード先のバージョンです。 | string |

##### メッセージ `DowngradeResponse` (api/etcdserverpb/rpc.proto) {#message-downgraderesponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| version | versionは、クラスターの現在のバージョンです。 | string |

##### メッセージ `DowngradeVersionTestRequest` (api/etcdserverpb/rpc.proto) {#message-downgradeversiontestrequest-apietcdserverpbrpcproto}

DowngradeVersionTestRequestは、テスト専用です。このリクエストのversionは、WALレコードのバージョンとして読み取られます。ダウングレード先のバージョンがこのバージョンより小さい場合、オンラインのダウングレードやオフラインの移行は安全ではないため、許可すべきではありません。

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ver |  | string |

##### メッセージ `HashKVRequest` (api/etcdserverpb/rpc.proto) {#message-hashkvrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| revision | revisionは、ハッシュ操作の対象となるキー・バリューストアのリビジョンです。 | int64 |

##### メッセージ `HashKVResponse` (api/etcdserverpb/rpc.proto) {#message-hashkvresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| hash | hashは、応答するメンバーのMVCCキーから、指定したリビジョンまでを対象として計算したハッシュ値です。 | uint32 |
| compact_revision | compact_revisionは、ハッシュ計算の開始時点でコンパクションされていたキー・バリューストアのリビジョンです。 | int64 |
| hash_revision | hash_revisionは、ハッシュ計算の対象とする上限のリビジョンです。 | int64 |

##### メッセージ `HashRequest` (api/etcdserverpb/rpc.proto) {#message-hashrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### メッセージ `HashResponse` (api/etcdserverpb/rpc.proto) {#message-hashresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| hash | hashは、応答するメンバーのKVバックエンドから計算したハッシュ値です。 | uint32 |

##### メッセージ `LeaseCheckpoint` (api/etcdserverpb/rpc.proto) {#message-leasecheckpoint-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | IDは、チェックポイントを作成するリースのIDです。 | int64 |
| remaining_TTL | Remaining_TTLは、リースの有効期限までの残り時間です。 | int64 |

##### メッセージ `LeaseCheckpointRequest` (api/etcdserverpb/rpc.proto) {#message-leasecheckpointrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| checkpoints |  | (slice of) LeaseCheckpoint |

##### メッセージ `LeaseCheckpointResponse` (api/etcdserverpb/rpc.proto) {#message-leasecheckpointresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### メッセージ `LeaseGrantRequest` (api/etcdserverpb/rpc.proto) {#message-leasegrantrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| TTL | TTLは、秒単位の希望する生存時間です。期限切れのリースでは-1が返されます。 | int64 |
| ID | IDは、リースに要求するIDです。IDが0の場合、リースの貸し手がIDを選択します。 | int64 |

##### メッセージ `LeaseGrantResponse` (api/etcdserverpb/rpc.proto) {#message-leasegrantresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| ID | IDは、付与されたリースのIDです。 | int64 |
| TTL | TTLは、サーバーが選択した、秒単位のリースの生存時間です。 | int64 |
| error |  | string |

##### メッセージ `LeaseKeepAliveRequest` (api/etcdserverpb/rpc.proto) {#message-leasekeepaliverequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | IDは、維持するリースのIDです。 | int64 |

##### メッセージ `LeaseKeepAliveResponse` (api/etcdserverpb/rpc.proto) {#message-leasekeepaliveresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| ID | IDは、キープアライブリクエストのリースIDです。 | int64 |
| TTL | TTLは、リースの新しい生存時間です。 | int64 |

##### メッセージ `LeaseLeasesRequest` (api/etcdserverpb/rpc.proto) {#message-leaseleasesrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### メッセージ `LeaseLeasesResponse` (api/etcdserverpb/rpc.proto) {#message-leaseleasesresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| leases |  | (slice of) LeaseStatus |

##### メッセージ `LeaseRevokeRequest` (api/etcdserverpb/rpc.proto) {#message-leaserevokerequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | IDは、取り消すリースのIDです。そのIDが取り消されると、関連付けられたすべてのキーが削除されます。 | int64 |

##### メッセージ `LeaseRevokeResponse` (api/etcdserverpb/rpc.proto) {#message-leaserevokeresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### メッセージ `LeaseStatus` (api/etcdserverpb/rpc.proto) {#message-leasestatus-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID |  | int64 |

##### メッセージ `LeaseTimeToLiveRequest` (api/etcdserverpb/rpc.proto) {#message-leasetimetoliverequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | IDは、そのリースのIDです。 | int64 |
| keys | keysをtrueにすると、このリースに関連付けられたすべてのキーを照会します。 | bool |

##### メッセージ `LeaseTimeToLiveResponse` (api/etcdserverpb/rpc.proto) {#message-leasetimetoliveresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| ID | IDは、キープアライブリクエストのリースIDです。 | int64 |
| TTL | TTLは、秒単位のリースの残りTTLです。リースはTTL+1秒未満で期限切れになります。 | int64 |
| grantedTTL | GrantedTTLは、リースの作成時または更新時に最初に付与された、秒単位の時間です。 | int64 |
| keys | Keysは、このリースに関連付けられたキーの一覧です。 | (slice of) bytes |

##### メッセージ `Member` (api/etcdserverpb/rpc.proto) {#message-member-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | IDは、このメンバーのメンバーIDです。 | uint64 |
| name | nameは、人が読めるメンバー名です。メンバーが起動していない場合、名前は空文字列になります。 | string |
| peerURLs | peerURLsは、クラスターとの通信用にメンバーが公開するURLの一覧です。 | (slice of) string |
| clientURLs | clientURLsは、クライアントとの通信用にメンバーが公開するURLの一覧です。メンバーが起動していない場合、clientURLsは空になります。 | (slice of) string |
| isLearner | isLearnerは、そのメンバーがRaftの学習者メンバーかどうかを示します。 | bool |

##### メッセージ `MemberAddRequest` (api/etcdserverpb/rpc.proto) {#message-memberaddrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| peerURLs | peerURLsは、追加するメンバーがクラスターとの通信に使用するURLの一覧です。 | (slice of) string |
| isLearner | isLearnerは、追加するメンバーがRaftの学習者メンバーかどうかを示します。 | bool |

##### メッセージ `MemberAddResponse` (api/etcdserverpb/rpc.proto) {#message-memberaddresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| member | memberは、追加したメンバーの情報です。 | Member |
| members | membersは、新しいメンバーを追加した後の、すべてのメンバーの一覧です。 | (slice of) Member |

##### メッセージ `MemberListRequest` (api/etcdserverpb/rpc.proto) {#message-memberlistrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| linearizable |  | bool |

##### メッセージ `MemberListResponse` (api/etcdserverpb/rpc.proto) {#message-memberlistresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | membersは、クラスターに関連付けられたすべてのメンバーの一覧です。 | (slice of) Member |

##### メッセージ `MemberPromoteRequest` (api/etcdserverpb/rpc.proto) {#message-memberpromoterequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | IDは、昇格させるメンバーのメンバーIDです。 | uint64 |

##### メッセージ `MemberPromoteResponse` (api/etcdserverpb/rpc.proto) {#message-memberpromoteresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | membersは、メンバーを昇格させた後の、すべてのメンバーの一覧です。 | (slice of) Member |

##### メッセージ `MemberRemoveRequest` (api/etcdserverpb/rpc.proto) {#message-memberremoverequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | IDは、削除するメンバーのメンバーIDです。 | uint64 |

##### メッセージ `MemberRemoveResponse` (api/etcdserverpb/rpc.proto) {#message-memberremoveresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | membersは、メンバーを削除した後の、すべてのメンバーの一覧です。 | (slice of) Member |

##### メッセージ `MemberUpdateRequest` (api/etcdserverpb/rpc.proto) {#message-memberupdaterequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | IDは、更新するメンバーのメンバーIDです。 | uint64 |
| peerURLs | peerURLsは、メンバーがクラスターとの通信に使用する、新しいURLの一覧です。 | (slice of) string |

##### メッセージ `MemberUpdateResponse` (api/etcdserverpb/rpc.proto) {#message-memberupdateresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | membersは、メンバーを更新した後の、すべてのメンバーの一覧です。 | (slice of) Member |

##### メッセージ `MoveLeaderRequest` (api/etcdserverpb/rpc.proto) {#message-moveleaderrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| targetID | targetIDは、新しいリーダーのノードIDです。 | uint64 |

##### メッセージ `MoveLeaderResponse` (api/etcdserverpb/rpc.proto) {#message-moveleaderresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### メッセージ `PutRequest` (api/etcdserverpb/rpc.proto) {#message-putrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | keyは、キー・バリューストアに格納するキーをバイト列で表したものです。 | bytes |
| value | valueは、キー・バリューストア内のキーに関連付ける値をバイト列で表したものです。 | bytes |
| lease | leaseは、キー・バリューストア内のキーに関連付けるリースIDです。leaseが0の場合、リースがないことを示します。 | int64 |
| prev_kv | prev_kvが設定されている場合、etcdは変更前のキー・バリューペアを取得します。変更前のキー・バリューペアはputレスポンスで返されます。 | bool |
| ignore_value | ignore_valueが設定されている場合、etcdは現在の値を使ってキーを更新します。キーが存在しない場合はエラーを返します。 | bool |
| ignore_lease | ignore_leaseが設定されている場合、etcdは現在のリースを使ってキーを更新します。キーが存在しない場合はエラーを返します。 | bool |

##### メッセージ `PutResponse` (api/etcdserverpb/rpc.proto) {#message-putresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| prev_kv | リクエストにprev_kvが設定されている場合、変更前のキー・バリューペアが返されます。 | mvccpb.KeyValue |

##### メッセージ `RangeRequest` (api/etcdserverpb/rpc.proto) {#message-rangerequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | keyは、範囲の最初のキーです。range_endが指定されていない場合、リクエストはkeyだけを検索します。 | bytes |
| range_end | range_endは、要求した範囲[key, range_end)の上限です。range_endが'\0'の場合、範囲にはkey以上（>=）のすべてのキーが含まれます。range_endがkeyに1を加えたもの（例："aa"+1 == "ab"、"a\xff"+1 == "b"）の場合、範囲リクエストはkeyを接頭辞に持つすべてのキーを取得します。keyとrange_endの両方が'\0'の場合、範囲リクエストはすべてのキーを返します。 | bytes |
| limit | limitは、リクエストで返すキーの数の上限です。limitが0の場合、上限なしとして扱います。 | int64 |
| revision | revisionは、範囲の取得に使用するキー・バリューストアの時点です。revisionが0以下の場合、最新のキー・バリューストアを対象とします。そのリビジョンがすでにコンパクションされている場合、レスポンスとしてErrCompactedを返します。 | int64 |
| sort_order | sort_orderは、ソートして返す結果の順序です。 | SortOrder |
| sort_target | sort_targetは、ソートに使用するキー・バリューのフィールドです。 | SortTarget |
| serializable | serializableは、範囲リクエストでメンバーローカルの直列化可能読み取りを使用するよう設定します。範囲リクエストはデフォルトで線形化可能です。線形化可能なリクエストは、直列化可能なリクエストよりレイテンシーが高く、スループットが低くなりますが、クラスターの現在のコンセンサスを反映します。性能を高めるため、直列化可能な範囲リクエストは、古いデータを読み取る可能性と引き換えに、クラスター内の他のノードとのコンセンサスを必要とせず、ローカルに処理されます。 | bool |
| keys_only | keys_onlyが設定されている場合、値は返さず、キーだけを返します。 | bool |
| count_only | count_onlyが設定されている場合、範囲内のキーの数だけを返します。 | bool |
| min_mod_revision | min_mod_revisionは、返すキーの変更リビジョンの下限です。変更リビジョンがこれより小さいキーはすべて除外されます。 | int64 |
| max_mod_revision | max_mod_revisionは、返すキーの変更リビジョンの上限です。変更リビジョンがこれより大きいキーはすべて除外されます。 | int64 |
| min_create_revision | min_create_revisionは、返すキーの作成リビジョンの下限です。作成リビジョンがこれより小さいキーはすべて除外されます。 | int64 |
| max_create_revision | max_create_revisionは、返すキーの作成リビジョンの上限です。作成リビジョンがこれより大きいキーはすべて除外されます。 | int64 |

##### メッセージ `RangeResponse` (api/etcdserverpb/rpc.proto) {#message-rangeresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| kvs | kvsは、範囲リクエストに一致するキー・バリューペアの一覧です。件数を要求した場合、kvsは空になります。 | (slice of) mvccpb.KeyValue |
| more | moreは、要求した範囲内に、返すべきキーがまだあるかどうかを示します。 | bool |
| count | countは、要求された場合に、範囲内の実際のキー数に設定されます。Kvsとは異なり、上限やフィルター（Min/Max、Create/Modify、Revisionsなど）の影響を受けず、指定した範囲内の総数を反映します。 | int64 |

##### メッセージ `RequestOp` (api/etcdserverpb/rpc.proto) {#message-requestop-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| request | requestは、トランザクションが受け付けるリクエスト型の共用体です。 | oneof |
| request_range |  | RangeRequest |
| request_put |  | PutRequest |
| request_delete_range |  | DeleteRangeRequest |
| request_txn |  | TxnRequest |

##### メッセージ `ResponseHeader` (api/etcdserverpb/rpc.proto) {#message-responseheader-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| cluster_id | cluster_idは、レスポンスを送信したクラスターのIDです。 | uint64 |
| member_id | member_idは、レスポンスを送信したメンバーのIDです。 | uint64 |
| revision | revisionは、リクエストが適用された時点のキー・バリューストアのリビジョンです。キー・バリューストアを操作しない呼び出しでは設定されません（したがって0です）。監視の進捗レスポンスでは、header.revisionが進捗を示します。このストリームで今後受信するすべてのイベントは、header.revisionより大きいリビジョン番号を持つことが保証されます。 | int64 |
| raft_term | raft_termは、リクエストが適用された時点のRaftの任期です。 | uint64 |

##### メッセージ `ResponseOp` (api/etcdserverpb/rpc.proto) {#message-responseop-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| response | responseは、トランザクションが返すレスポンス型の共用体です。 | oneof |
| response_range |  | RangeResponse |
| response_put |  | PutResponse |
| response_delete_range |  | DeleteRangeResponse |
| response_txn |  | TxnResponse |

##### メッセージ `SnapshotRequest` (api/etcdserverpb/rpc.proto) {#message-snapshotrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### メッセージ `SnapshotResponse` (api/etcdserverpb/rpc.proto) {#message-snapshotresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header | headerは、キー・バリューストアの現在の情報を保持します。スナップショットストリームの最初のheaderは、スナップショットの時点を示します。 | ResponseHeader |
| remaining_bytes | remaining_bytesは、このメッセージの後に送信するblobのバイト数です。 | uint64 |
| blob | blobは、スナップショットストリームの次のスナップショットチャンクを保持します。 | bytes |
| version | スナップショットに記録されたストレージスキーマのバージョンです。メンバーのローカルバックエンドから取得され、バイナリーのバージョンとは異なる場合があります。スナップショットのリストア時に対応している必要があるetcdのストレージバージョンを示します。 | string |

##### メッセージ `StatusRequest` (api/etcdserverpb/rpc.proto) {#message-statusrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### メッセージ `StatusResponse` (api/etcdserverpb/rpc.proto) {#message-statusresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| version | versionは、応答するetcdメンバーのバイナリーのバージョンです。ストレージスキーマのバージョンは、storageVersionで別に報告されます。 | string |
| dbSize | dbSizeは、応答するメンバーのバックエンドデータベースに物理的に割り当てられた領域のサイズ（バイト単位）です。 | int64 |
| leader | leaderは、応答するメンバーが現在のリーダーと認識しているメンバーのIDです。 | uint64 |
| raftIndex | raftIndexは、応答するメンバーの現在のRaftコミット済みインデックスです。 | uint64 |
| raftTerm | raftTermは、応答するメンバーの現在のRaftの任期です。 | uint64 |
| raftAppliedIndex | raftAppliedIndexは、応答するメンバーの現在のRaft適用済みインデックスです。 | uint64 |
| errors | errorsは、アラームや健全性に関する情報と状態を保持します。 | (slice of) string |
| dbSizeInUse | dbSizeInUseは、応答するメンバーのバックエンドデータベースで論理的に使用されている領域のサイズ（バイト単位）です。 | int64 |
| isLearner | isLearnerは、そのメンバーがRaftの学習者メンバーかどうかを示します。 | bool |
| storageVersion | storageVersionは、dbファイルのバージョンです。目標のクラスターバージョンに対して、更新が遅れる場合があります。 | string |
| dbSizeQuota | dbSizeQuotaは、設定されたetcdのストレージクォータ（バイト単位）です（--quota-backend-bytesフラグでetcdインスタンスに渡した値）。 | int64 |
| downgradeInfo | downgradeInfoは、ダウングレード処理が存在するかどうかを示します。 | DowngradeInfo |

##### メッセージ `TxnRequest` (api/etcdserverpb/rpc.proto) {#message-txnrequest-apietcdserverpbrpcproto}

Googleのpaxosdb論文より：この実装の中心となるのは、MultiOpと呼ぶ強力なプリミティブです。反復処理を除くすべてのデータベース操作は、MultiOpを1回呼び出すことで実装されています。MultiOpはアトミックに適用され、3つの要素で構成されます。1. guardと呼ぶテストのリスト。guard内の各テストは、データベース内の1つのエントリーを検査します。値の有無を確認したり、指定した値と比較したりできます。guard内の異なる2つのテストは、データベース内の同じエントリーにも、異なるエントリーにも適用できます。guard内のすべてのテストが適用され、MultiOpはその結果を返します。すべてのテストがtrueの場合、MultiOpはt op（下記の項目2）を実行し、それ以外の場合はf op（下記の項目3）を実行します。2. t opと呼ぶデータベース操作のリスト。リスト内の各操作は、挿入、削除、検索のいずれかで、データベースの1つのエントリーに適用されます。リスト内の異なる2つの操作は、データベース内の同じエントリーにも、異なるエントリーにも適用できます。これらの操作は、guardの評価結果がtrueの場合に実行されます。3. f opと呼ぶデータベース操作のリスト。t opと同様ですが、guardの評価結果がfalseの場合に実行されます。

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| compare | compareは、条件の論理積を表す述語のリストです。比較が成功するとsuccessのリクエストを順番に処理し、レスポンスにはそれぞれの応答が同じ順序で含まれます。比較が失敗するとfailureのリクエストを順番に処理し、レスポンスにはそれぞれの応答が同じ順序で含まれます。 | (slice of) Compare |
| success | successは、compareの評価結果がtrueの場合に適用するリクエストのリストです。 | (slice of) RequestOp |
| failure | failureは、compareの評価結果がfalseの場合に適用するリクエストのリストです。 | (slice of) RequestOp |

##### メッセージ `TxnResponse` (api/etcdserverpb/rpc.proto) {#message-txnresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| succeeded | succeededは、compareの評価結果がtrueの場合にtrueに、それ以外の場合にfalseに設定されます。 | bool |
| responses | responsesは、succeededがtrueの場合にはsuccessを、falseの場合にはfailureを適用した結果に対応するレスポンスのリストです。 | (slice of) ResponseOp |

##### メッセージ `WatchCancelRequest` (api/etcdserverpb/rpc.proto) {#message-watchcancelrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| watch_id | watch_idは、これ以上イベントを送信しないようキャンセルするウォッチャーのIDです。 | int64 |

##### メッセージ `WatchCreateRequest` (api/etcdserverpb/rpc.proto) {#message-watchcreaterequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | keyは、監視対象として登録するキーです。 | bytes |
| range_end | range_endは、監視する範囲[key, range_end)の終端です。range_endが指定されていない場合、key引数だけを監視します。range_endが'\0'の場合、key引数以上のすべてのキーを監視します。range_endが指定したキーに1を加えた値の場合、そのキーを接頭辞に持つすべてのキーを監視します。 | bytes |
| start_revision | start_revisionは、監視を開始するリビジョン（そのリビジョンを含む）で、省略可能です。start_revisionを指定しない場合は「現在」から開始します。 | int64 |
| progress_notify | progress_notifyを設定すると、最近のイベントがない場合に、etcdサーバーが新しいウォッチャーへイベントを含まないWatchResponseを定期的に送信します。これは、クライアントが切断されたウォッチャーを、最近の既知のリビジョンから復旧したい場合に役立ちます。etcdサーバーは、現在の負荷に基づいて通知の送信頻度を決めることがあります。 | bool |
| filters | filtersは、ウォッチャーに送り返す前にサーバー側でイベントをフィルタリングします。 | (slice of) FilterType |
| prev_kv | prev_kvが設定されている場合、作成したウォッチャーはイベント発生前のKVを取得します。以前のKVがすでにコンパクションされている場合、何も返されません。 | bool |
| watch_id | watch_idが指定され、0でない場合、そのIDがこのウォッチャーに割り当てられます。etcdでのウォッチャー作成は同期操作ではないため、これを使うことで、同じストリーム上に複数のウォッチャーを作成する際に正しい順序を保てます。ストリーム上ですでに使用中のIDを持つウォッチャーを作成すると、エラーが返されます。 | int64 |
| fragment | fragmentは、大きなリビジョンを複数の監視レスポンスに分割できるようにします。 | bool |

##### メッセージ `WatchProgressRequest` (api/etcdserverpb/rpc.proto) {#message-watchprogressrequest-apietcdserverpbrpcproto}

監視ストリームの進捗状態を、監視レスポンスストリームでできるだけ早く送信するよう要求します。

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### メッセージ `WatchRequest` (api/etcdserverpb/rpc.proto) {#message-watchrequest-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| request_union | request_unionは、新しいウォッチャーを作成するか、既存のウォッチャーをキャンセルするためのリクエストです。 | oneof |
| create_request |  | WatchCreateRequest |
| cancel_request |  | WatchCancelRequest |
| progress_request |  | WatchProgressRequest |

##### メッセージ `WatchResponse` (api/etcdserverpb/rpc.proto) {#message-watchresponse-apietcdserverpbrpcproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| watch_id | watch_idは、レスポンスに対応するウォッチャーのIDです。 | int64 |
| created | createdは、監視作成リクエストへのレスポンスである場合にtrueに設定されます。クライアントはwatch_idを記録し、作成したウォッチャーのイベントを同じストリームから受信するようにしてください。作成したウォッチャーに送信されるすべてのイベントには、同じwatch_idが付与されます。 | bool |
| canceled | canceledは、監視キャンセルリクエストへのレスポンスである場合、またはstart_revisionがすでにコンパクションされている場合にtrueに設定されます。キャンセルされたウォッチャーには、それ以降のイベントは送信されません。 | bool |
| compact_revision | compact_revisionは、ウォッチャーがコンパクション済みのインデックスで監視しようとした場合に、最小のインデックスに設定されます。これは、コンパクション済みのリビジョンでウォッチャーを作成した場合、またはウォッチャーがキー・バリューストアの進行に追いつけない場合に発生します。クライアントはそのウォッチャーをキャンセル済みとして扱い、同じstart_revisionでウォッチャーを作り直さないようにしてください。 | int64 |
| cancel_reason | cancel_reasonは、ウォッチャーをキャンセルする理由を示します。 | string |
| fragment | fragmentは、大きな監視レスポンスが複数のレスポンスに分割された場合にtrueです。 | bool |
| events |  | (slice of) mvccpb.Event |

##### メッセージ `Event` (api/mvccpb/kv.proto) {#message-event-apimvccpbkvproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| type | typeはイベントの種類です。typeがPUTの場合、キーに新しいデータが保存されたことを示します。typeがDELETEの場合、キーが削除されたことを示します。 | EventType |
| kv | kvは、イベントのKeyValueを保持します。PUTイベントは現在のkvペアを含みます。kv.Version=1のPUTイベントは、キーが作成されたことを示します。DELETE/EXPIREイベントは、変更リビジョンが削除時のリビジョンに設定された、削除済みのキーを含みます。 | KeyValue |
| prev_kv | prev_kvは、イベント発生前のキー・バリューペアを保持します。 | KeyValue |

##### メッセージ `KeyValue` (api/mvccpb/kv.proto) {#message-keyvalue-apimvccpbkvproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| key | keyは、バイト列で表したキーです。空のキーは許可されません。 | bytes |
| create_revision | create_revisionは、このキーが最後に作成されたリビジョンです。 | int64 |
| mod_revision | mod_revisionは、このキーが最後に変更されたリビジョンです。 | int64 |
| version | versionは、キーのバージョンです。削除するとバージョンは0にリセットされ、キーを変更するたびにバージョンが増加します。 | int64 |
| value | valueは、キーが保持する値をバイト列で表したものです。 | bytes |
| lease | leaseは、キーに関連付けられたリースのIDです。関連付けられたリースが期限切れになると、キーは削除されます。leaseが0の場合、キーにリースは関連付けられていません。 | int64 |

##### メッセージ `Lease` (server/lease/leasepb/lease.proto) {#message-lease-serverleaseleasepbleaseproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| ID |  | int64 |
| TTL |  | int64 |
| RemainingTTL |  | int64 |

##### メッセージ `LeaseInternalRequest` (server/lease/leasepb/lease.proto) {#message-leaseinternalrequest-serverleaseleasepbleaseproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| LeaseTimeToLiveRequest |  | etcdserverpb.LeaseTimeToLiveRequest |

##### メッセージ `LeaseInternalResponse` (server/lease/leasepb/lease.proto) {#message-leaseinternalresponse-serverleaseleasepbleaseproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| LeaseTimeToLiveResponse |  | etcdserverpb.LeaseTimeToLiveResponse |

##### メッセージ `Permission` (api/authpb/auth.proto) {#message-permission-apiauthpbauthproto}

Permissionは、単一のエンティティーです。

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| permType |  | Type |
| key |  | bytes |
| range_end |  | bytes |

##### メッセージ `Role` (api/authpb/auth.proto) {#message-role-apiauthpbauthproto}

Roleは、authRolesバケット内の単一のエントリーです。

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| name |  | bytes |
| keyPermission |  | (slice of) Permission |

##### メッセージ `User` (api/authpb/auth.proto) {#message-user-apiauthpbauthproto}

Userは、authUsersバケット内の単一のエントリーです。

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| name |  | bytes |
| password |  | bytes |
| roles |  | (slice of) string |
| options |  | UserAddOptions |

##### メッセージ `UserAddOptions` (api/authpb/auth.proto) {#message-useraddoptions-apiauthpbauthproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| no_password |  | bool |
