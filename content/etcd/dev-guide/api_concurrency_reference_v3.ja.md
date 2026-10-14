---
title: APIリファレンス：並行処理
weight: 3900
description: "etcdの並行処理APIリファレンス"
categories: [リファレンス]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/api_concurrency_reference_v3.md"
---

このAPIリファレンスは、各見出しに記載した`.proto`ファイルから自動生成されています。

##### サービス `Lock` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#service-lock-serveretcdserverapiv3lockv3lockpbv3lockproto}

ロックサービスは、クライアント側のロック機能をgRPCインターフェースとして公開します。

| メソッド | リクエスト型 | レスポンス型 | 説明 |
| ------ | ------------ | ------------- | ----------- |
| Lock | LockRequest | LockResponse | Lockは、指定した名前付きロックの分散共有ロックを取得します。成功すると、呼び出し元がロックを保持している間だけ存在する、一意のキーを返します。このキーをトランザクションと組み合わせることで、ロックの所有権を保持している間だけetcdの更新が行われることを安全に保証できます。ロックは、そのキーに対してUnlockを呼び出すか、所有者に関連付けられたリースが期限切れになるまで保持されます。 |
| Unlock | UnlockRequest | UnlockResponse | Unlockは、Lockが返したキーを受け取り、ロックの保持を解除します。すると、ロックを待っている次のLock呼び出し元が起こされ、ロックの所有権が与えられます。 |

##### メッセージ `LockRequest` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-lockrequest-serveretcdserverapiv3lockv3lockpbv3lockproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| name | nameは、取得する分散共有ロックの識別子です。 | bytes |
| lease | leaseは、ロックの所有権に関連付けるリースのIDです。ロックを保持しているリースが期限切れになるか取り消されると、ロックは自動的に解放されます。同じリースによるLockの呼び出しは、1回の取得として扱います。同じリースで2回ロックしても、何も行いません。 | int64 |

##### メッセージ `LockResponse` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-lockresponse-serveretcdserverapiv3lockv3lockpbv3lockproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |
| key | keyは、Lockの呼び出し元がロックを所有している間、etcd上に存在するキーです。このキーは変更しないでください。変更すると、ロックの動作が未定義になる可能性があります。 | bytes |

##### メッセージ `UnlockRequest` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-unlockrequest-serveretcdserverapiv3lockv3lockpbv3lockproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| key | keyは、Lockによって付与されたロック所有権のキーです。 | bytes |

##### メッセージ `UnlockResponse` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-unlockresponse-serveretcdserverapiv3lockv3lockpbv3lockproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |

##### サービス `Election` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#service-election-serveretcdserverapiv3electionv3electionpbv3electionproto}

選挙サービスは、クライアント側の選挙機能をgRPCインターフェースとして公開します。

| メソッド | リクエスト型 | レスポンス型 | 説明 |
| ------ | ------------ | ------------- | ----------- |
| Campaign | CampaignRequest | CampaignResponse | Campaignは、選挙でリーダーシップを取得するまで待機し、成功するとリーダーシップを表すLeaderKeyを返します。LeaderKeyは、その選挙で新しい値を発行すること、リーダーシップの保持を条件にトランザクションでAPIリクエストを保護すること、および選挙から辞任することに使用できます。 |
| Proclaim | ProclaimRequest | ProclaimResponse | Proclaimは、リーダーが公開している値を新しい値で更新します。 |
| Leader | LeaderRequest | LeaderResponse | Leaderは、現在の選挙の宣言があれば、それを返します。 |
| Observe | LeaderRequest | LeaderResponse | Observeは、選挙で選出されたリーダーによる宣言を、発行された順にストリーミングします。 |
| Resign | ResignRequest | ResignResponse | Resignは、他の立候補者がその選挙のリーダーシップを取得できるよう、リーダーシップを解放します。 |

##### メッセージ `CampaignRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-campaignrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| name | nameは、立候補する選挙の識別子です。 | bytes |
| lease | leaseは、その選挙のリーダーシップに関連付けられたリースのIDです。リーダーを辞任する前にリースが期限切れになるか取り消されると、次の立候補者がいる場合は、その立候補者にリーダーシップが移ります。 | int64 |
| value | valueは、立候補者が選挙に勝ったときに設定する、最初の宣言値です。 | bytes |

##### メッセージ `CampaignResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-campaignresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |
| leader | leaderは、その選挙のリーダーシップを保持するために使用するリソースを表します。 | LeaderKey |

##### メッセージ `LeaderKey` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-leaderkey-serveretcdserverapiv3electionv3electionpbv3electionproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| name | nameは、リーダーシップキーに対応する選挙の識別子です。 | bytes |
| key | keyは、その選挙の所有権を表す不透明なキーです。キーを削除すると、リーダーシップは失われます。 | bytes |
| rev | revは、キーの作成リビジョンです。トランザクション中にキーの作成リビジョンがrevと一致するかを調べることで、選挙の所有権を検証できます。 | int64 |
| lease | leaseは、その選挙のリーダーのリースIDです。 | int64 |

##### メッセージ `LeaderRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-leaderrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| name | nameは、リーダーシップ情報を取得する選挙の識別子です。 | bytes |

##### メッセージ `LeaderResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-leaderresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |
| kv | kvは、リーダーの最新の更新を表すキー・バリューペアです。 | mvccpb.KeyValue |

##### メッセージ `ProclaimRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-proclaimrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| leader | leaderは、その選挙で保持しているリーダーシップです。 | LeaderKey |
| value | valueは、リーダーの現在の値を上書きするための更新値です。 | bytes |

##### メッセージ `ProclaimResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-proclaimresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |

##### メッセージ `ResignRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-resignrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| leader | leaderは、辞任によって手放すリーダーシップです。 | LeaderKey |

##### メッセージ `ResignResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-resignresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| フィールド | 説明 | 型 |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |

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
