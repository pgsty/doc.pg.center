---
title: etcd API
weight: 2625
description: "etcd APIの中心となる設計の概要"
categories: [概念]
upstream_link: "https://github.com/etcd-io/website/blob/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7/learning/api.md"
---

このドキュメントでは、etcd v3 APIの中心となる設計の概要を説明します。
etcd v3.5で非推奨となったetcd v2 APIとは異なることに注意してください。
すべてを網羅するものではなく、使用頻度の低いAPI呼び出しに話を広げずに、etcdを理解するために必要な基本的な考え方に焦点を当てます。
etcdのすべてのAPIは、etcdサーバーが処理するリモートプロシージャコール（RPC）を分類した[gRPCサービス][grpc-service]で定義されています。
etcdのすべてのRPCの完全な一覧は、[gRPC API一覧][grpc-api]にMarkdown形式で記載されています。

## gRPCサービス {#grpc-services}

etcdサーバーに送信するすべてのAPIリクエストは、gRPCのリモートプロシージャコールです。etcdのRPCは、機能に基づいてサービスに分類されます。

etcdのキー空間を扱う主要なサービスは、次のとおりです。

* KV - キー・バリューペアを作成、更新、取得、削除します。
* Watch - キーの変更を監視します。
* Lease - クライアントのキープアライブメッセージを処理するプリミティブを提供します。

クラスター自体を管理するサービスは、次のとおりです。

* Auth - ユーザーを認証するための、ロールに基づく認証機構です。
* Cluster - メンバーシップ情報と構成機能を提供します。
* Maintenance - リカバリー用スナップショットの作成、ストアのデフラグメンテーション、メンバーごとの状態情報の取得を行います。

### リクエストとレスポンス {#requests-and-responses}

etcdのすべてのRPCは同じ形式に従います。各RPCは、`NameRequest`を引数に取り、`NameResponse`をレスポンスとして返す関数`Name`を持ちます。たとえば、`Range` RPCの定義は次のとおりです。

```protobuf
service KV {
  Range(RangeRequest) returns (RangeResponse)
  ...
}
```

### レスポンスヘッダー {#response-header}

etcd APIのすべてのレスポンスには、そのレスポンスに関するクラスターのメタデータを含むヘッダーが付属します。

```proto
message ResponseHeader {
  uint64 cluster_id = 1;
  uint64 member_id = 2;
  int64 revision = 3;
  uint64 raft_term = 4;
}
```

* `cluster_id` - レスポンスを生成したクラスターのIDです。
* `member_id` - レスポンスを生成したメンバーのIDです。
* `revision` - レスポンス生成時のキー・バリューストアのリビジョンです。
* `raft_term` - レスポンス生成時のメンバーのRaftの任期です。

アプリケーションは、`cluster_id`または`member_id`フィールドを読み取り、意図したクラスター（メンバー）と通信していることを確認できます。

`revision`フィールドから、キー・バリューストアの最新のリビジョンを取得できます。これは、過去のリビジョンを指定して`time travel query`を実行し、リクエスト時点での最新のリビジョンを知りたい場合に特に役立ちます。

`raft_term`を使うと、クラスターが新しいリーダー選挙を完了したことを検出できます。

## Key-Value API {#key-value-api}

Key-Value APIは、etcd内に保存されたキー・バリューペアを操作します。通常、etcdに対するリクエストの大半はキー・バリューのリクエストです。

### システムのプリミティブ {#system-primitives}

### キー・バリューペア {#key-value-pair}

キー・バリューペアは、キー・バリューAPIで操作できる最小単位です。各キー・バリューペアは、[protobuf形式][kv-proto]で定義された複数のフィールドを持ちます。

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

* `key` - バイト列で表したキーです。空のキーは許可されません。
* `value` - バイト列で表した値です。
* `version` - キーのバージョンです。削除するとバージョンはゼロにリセットされ、キーを変更するたびにバージョンが増加します。
* `create_revision` - キーが最後に作成されたリビジョンです。
* `mod_revision` - キーが最後に変更されたリビジョンです。
* `lease` - キーに関連付けられたリースのIDです。leaseが0の場合、キーにリースは関連付けられていません。


etcdは、キーと値に加え、キーのメッセージの一部としてリビジョンのメタデータも付与します。このリビジョン情報は、作成時刻と変更時刻によってキーに順序を付け、分散同期のための並行処理制御に役立ちます。etcdクライアントの[分散共有ロック][locks]は、作成リビジョンを使ってロックの所有権を待ちます。同様に、変更リビジョンは、[ソフトウェアトランザクショナルメモリー][STM]の読み取り集合の競合の検出や、[リーダー選挙][elections]の更新の待機に使用します。

#### リビジョン {#revisions}

etcdは、キー空間が変更されるたびに増加する、クラスター全体の64ビットカウンターであるストアリビジョンを保持します。リビジョンはグローバルな論理時計として機能し、ストアへのすべての更新を順序付けます。新しいリビジョンが表す変更は差分です。リビジョンに関連付けられるデータは、ストアを変更したデータです。内部的には、新しいリビジョンとは、増加したリビジョンをキーとして、バックエンドのB+treeに変更を書き込むことを意味します。

etcdの[多版型同時実行制御][mvcc]バックエンドを考えると、リビジョンの有用性がさらに分かります。MVCCモデルでは、過去のキーのリビジョンを保持するため、キー・バリューストアを過去のリビジョンの状態で参照できます。クラスター管理者は、この履歴の保持ポリシーを設定して、ストレージを細かく管理できます。通常、etcdはタイマーによってキーの古いリビジョンを破棄します。一般的なetcdクラスターは、更新によって古くなったキーのデータを数時間保持します。これにより、一時的なネットワーク障害だけでなく、クライアントの長時間の切断にも確実に対処できます。ウォッチャーは、最後に観測した過去のリビジョンから再開するだけです。同様に、特定の時点のストアを読み取るには、読み取りリクエストにリビジョンを指定すると、そのリビジョンがコミットされた時点のキー空間の状態からキーを返せます。

#### キー範囲 {#key-ranges}

etcdのデータモデルは、平坦なバイナリーキー空間上のすべてのキーにインデックスを付けます。これは、キーをディレクトリにまとめる階層構造を使う他のキー・バリューストアとは異なります。キーはディレクトリ単位ではなく、キーの区間`[a, b)`で列挙します。

etcdでは、この区間を「範囲」と呼ぶことがよくあります。範囲に対する操作は、ディレクトリに対する操作より表現力があります。階層型ストアと同様に、`[a, a+1)`による単一キーの検索（例：`['a', 'a\x00')`は`'a'`を検索）や、ディレクトリの深さに従ってキーをエンコードすることによるディレクトリ検索をサポートします。さらに、区間では接頭辞も表せます。たとえば、区間`['a', 'b')`は、文字列'a'を接頭辞に持つすべてのキーを検索します。

慣例として、リクエストの範囲は`key`と`range_end`フィールドで表します。`key`フィールドは範囲の最初のキーで、空にしないでください。`range_end`は、範囲の最後のキーの次のキーです。`range_end`が指定されていないか空の場合、範囲にはkey引数だけが含まれます。`range_end`が`key`に1を加えたもの（例：`"aa"+1 == "ab"`、`"a\xff"+1 == "b"`）の場合、その範囲はkeyを接頭辞に持つすべてのキーを表します。`key`と`range_end`の両方が`'\0'`の場合、その範囲はすべてのキーを表します。`range_end`が`'\0'`の場合、その範囲はkey引数以上のすべてのキーを表します。

### Range {#range}

`RangeRequest`を受け取る`Range` API呼び出しで、キー・バリューストアからキーを取得します。

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

* `key`, `range_end` - 取得するキー範囲です。
* `limit` - リクエストで返すキーの最大数です。limitを0に設定すると、上限なしとして扱います。
* `revision` - 範囲の取得に使用するキー・バリューストアの時点です。revisionがゼロ以下の場合、最新のキー・バリューストアを対象とします。リビジョンがすでにコンパクションされている場合、レスポンスとして`ErrCompacted`を返します。
* `sort_order` - ソートするリクエストの順序です。
* `sort_target` - ソート対象のキー・バリューのフィールドです。
* `serializable` - 範囲リクエストで、メンバーローカルの直列化可能読み取りを使用するように設定します。Rangeはデフォルトで線形化可能であり、クラスターの現在のコンセンサスを反映します。性能と可用性を高めるため、直列化可能な範囲リクエストは、古いデータを読み取る可能性と引き換えに、クラスター内の他のノードとのコンセンサスを必要とせず、ローカルに処理されます。
* `keys_only` - 値を返さず、キーだけを返します。
* `count_only` - 範囲内のキーの数だけを返します。
* `min_mod_revision` - 返されるキーの変更リビジョンの下限です。変更リビジョンがそれより小さいキーはすべて除外されます。
* `max_mod_revision` - キーの変更リビジョンの上限です。変更リビジョンがそれより大きいキーはすべて除外されます。
* `min_create_revision` - 返されるキーの作成リビジョンの下限です。作成リビジョンがそれより小さいキーはすべて除外されます。
* `max_create_revision` - キーの作成リビジョンの上限です。作成リビジョンがそれより大きいキーはすべて除外されます。

クライアントは、`Range`呼び出しから`RangeResponse`メッセージを受信します。

```protobuf
message RangeResponse {
  ResponseHeader header = 1;
  repeated mvccpb.KeyValue kvs = 2;
  bool more = 3;
  int64 count = 4;
}
```

* `kvs` - 範囲リクエストに一致するキー・バリューペアの一覧です。`count_only`を設定すると、`kvs`は空になります。
* `more` - 要求した範囲内に返すべきキーがまだあるかどうかを示します。
* `count` - リクエスト時に範囲内に存在するキーの実際の数です。`kvs`とは異なり、制限やフィルター（例：Min/Max、Create/Modify、Revisions）の影響を受けず、指定した範囲内の完全な数を反映します。

キー範囲が大きく、レスポンス全体をバッファーに保持したくない場合は、[RangeStream](#rangestream)を参照してください。

### RangeStream {#rangestream}

`RangeStream`は`Range`と同じ結果セットを返しますが、サーバーがレスポンスを一連のチャンクに分割し、クライアントへストリーミングします。これにより、サーバーとクライアントのどちらも、大きな範囲全体をメモリーに保持する必要がなくなります。`RangeStream`は、`Range`と同じ`RangeRequest`を受け付けます。

クライアントは、`RangeStream`呼び出しから`RangeStreamResponse`メッセージのストリームを受信します。

```protobuf
message RangeStreamResponse {
  RangeResponse range_response = 1;
}
```

各チャンクのフィールドは、次のように設定されます。

* `kvs` - 各チャンクは、結果の重複しない一部分を保持します。すべてのチャンクの`kvs`を到着順に連結すると、1回の`Range`呼び出しと同じキー集合が得られます。
* `header`、`more`、`count` - ストリームがエラーなく完了した場合に限り、最後のチャンクにだけ設定されます。それより前のチャンクでは、これらのフィールドはゼロ値のままです。各チャンクの`range_response`に`proto.Merge`を適用すると、`Range`が返すものと同等の`RangeResponse`が得られます。

ストリームがエラーで終了した場合、有効な`header`、`more`、`count`を持つチャンクはありません。

ストリーム内のすべてのチャンクは、同じリビジョンを対象に処理されます。リクエストに`Revision`が設定されていない場合、サーバーはストリームの開始時に最新のコミット済みリビジョンを取得し、残りのストリームでも同じリビジョンを使います。

`RangeStream`は、独自のソート順序やリビジョンフィルター（`min_mod_revision`、`max_mod_revision`、`min_create_revision`、`max_create_revision`）をサポートしません。どちらかを使用したリクエストは、`Unimplemented`を返します。etcdのgRPCプロキシも`RangeStream`をサポートしません。

`RangeStream`を処理する一般的な方法は、次の2つです。

1. **各チャンクを個別に処理する。** 結果全体を集める前に、キーが届くたびにデコードして処理したい、高い性能が求められる場面に適しています。クライアントはチャンクを順に読み、各チャンクの`kvs`を処理します。ストリームが正常に終了した後、最後のチャンクから`header`、`more`、`count`を読み取ります。
2. **単一のレスポンスにまとめる。** 単項の`Range`と同等の結果が必要な場合に適しています。クライアントは、各チャンクの`range_response`を、たとえば`proto.Merge`で1つの`RangeResponse`にマージします。マージ後の結果には、すべての`kvs`と、最後のチャンクの`header`、`more`、`count`が含まれます。Goクライアントは、この処理を補助する`clientv3.GetStreamToGetResponse`を提供します。

### Put {#put}

`PutRequest`を受け取る`Put`呼び出しで、キー・バリューストアにキーを保存します。

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

* `key` - キー・バリューストアに格納するキーの名前です。
* `value` - キー・バリューストア内のキーに関連付ける、バイト列の値です。
* `lease` - キー・バリューストア内のキーに関連付けるリースIDです。leaseが0の場合、リースがないことを示します。
* `prev_kv` - 設定されている場合、etcdは変更前のキー・バリューペアを取得します。変更前のキー・バリューペアはputレスポンスで返されます。
* `ignore_value` - 設定されている場合、現在の値を使ってキーを更新します。キーが存在しない場合はエラーを返します。
* `ignore_lease` - 設定されている場合、etcdは現在のリースを使ってキーを更新します。キーが存在しない場合はエラーを返します。

クライアントは、`Put`呼び出しから`PutResponse`メッセージを受信します。

```protobuf
message PutResponse {
  ResponseHeader header = 1;
  mvccpb.KeyValue prev_kv = 2;
}
```

* `prev_kv` - リクエストで`prev_kv`が設定されている場合、変更前のキー・バリューペアが返されます。

### 範囲の削除 {#delete-range}

`DeleteRangeRequest`を受け取る`DeleteRange`呼び出しで、キーの範囲を削除します。

```protobuf
message DeleteRangeRequest {
  bytes key = 1;
  bytes range_end = 2;
  bool prev_kv = 3;
}
```

* `key` - 範囲内で削除する最初のキーです。
* `range_end` - 範囲`[key, range_end)`内で削除する最後のキーの次のキーです。

クライアントは、`DeleteRange`呼び出しから`DeleteRangeResponse`メッセージを受信します。

```protobuf
message DeleteRangeResponse {
  ResponseHeader header = 1;
  int64 deleted = 2;
  repeated mvccpb.KeyValue prev_kvs = 3;
}
```

* `deleted` - 範囲削除リクエストで削除されたキーの数です。
* `prev_kvs` - 変更前のキー・バリューペアです。リクエストで`prev_kv`が設定されている場合に返されます。

### トランザクション {#transaction}

トランザクションは、キー・バリューストア上のアトミックなIf/Then/Else構造です。リクエストをアトミックなブロック（then/else）にまとめ、キー・バリューストアの内容に基づいて実行条件（if）を設定するプリミティブを提供します。トランザクションは、意図しない並行更新からキーを保護すること、比較交換操作を構築すること、より高度な並行処理制御を開発することに使用できます。

トランザクションは、1つのリクエスト内で複数のリクエストをアトミックに処理できます。キー・バリューストアの変更では、そのトランザクションによってストアのリビジョンが増加するのは1回だけで、生成されるすべてのイベントが同じリビジョンを持つことを意味します。ただし、1つのトランザクション内で同じキーを複数回変更することは禁止されています。

すべてのトランザクションには、`If`文のように、複数の比較の論理積による実行条件があります。各比較は、ストア内の1つのキーを検査します。値の有無、指定した値との比較、キーのリビジョンやバージョンを確認できます。異なる2つの比較は、同じキーにも異なるキーにも適用できます。すべての比較はアトミックに適用されます。すべてがtrueの場合、トランザクションは成功とされ、etcdはthen / `success`リクエストブロックを適用します。それ以外は失敗とされ、else / `failure`リクエストブロックを適用します。

各比較は、`Compare`メッセージとしてエンコードされます。

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

* `result` - 論理比較演算の種類です（等しい、より小さい、など）。
* `target` - 比較するキー・バリューのフィールドです。キーのバージョン、作成リビジョン、変更リビジョン、値のいずれかです。
* `key` - 比較対象のキーです。
* `target_union` - 比較のためにユーザーが指定するデータです。

比較ブロックを処理した後、トランザクションはリクエストのブロックを適用します。ブロックは、`RequestOp`メッセージのリストです。

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

* `request_range` - `RangeRequest`です。
* `request_put` - `PutRequest`です。キーは一意でなければなりません。他のPutsやDeletesとキーが重複してはいけません。
* `request_delete_range` - `DeleteRangeRequest`です。PutsやDeletesのリクエストとキーが重複してはいけません。

以上をまとめ、`TxnRequest`を受け取る`Txn` API呼び出しでトランザクションを発行します。

```protobuf
message TxnRequest {
  repeated Compare compare = 1;
  repeated RequestOp success = 2;
  repeated RequestOp failure = 3;
}
```

* `compare` - 条件の論理積を表す述語のリストです。比較が成功すると、successのリクエストが順に処理され、レスポンスにそれぞれのレスポンスが順番に含まれます。
* `success` - すべての比較の評価結果がtrueの場合に処理するリクエストのリストです。
* `failure` - 比較がfalseと評価された場合に適用されるリクエストのリストです。

クライアントは、`Txn`呼び出しから`TxnResponse`メッセージを受信します。

```protobuf
message TxnResponse {
  ResponseHeader header = 1;
  bool succeeded = 2;
  repeated ResponseOp responses = 3;
}
```

* `succeeded` - 比較がtrueと評価された場合はtrue、そうでなければfalseです。
* `responses` - succeededがtrueの場合はsuccess、falseの場合はfailureを適用した結果に対応するレスポンスのリストです。

```protobuf
message ResponseOp {
  oneof response {
    RangeResponse response_range = 1;
    PutResponse response_put = 2;
    DeleteRangeResponse response_delete_range = 3;
  }
}
```

内部の各レスポンスに含まれる`ResponseHeader`は、どのような用途でも解釈しないでください。
最新のリビジョンを取得する必要がある場合、クライアントは常に`TxnResponse`の最上位の`ResponseHeader`を確認してください。


## Watch API {#watch-api}

`Watch` APIは、キーの変更を非同期に監視する、イベントに基づくインターフェースを提供します。etcdの監視は、現在または過去の指定したリビジョンから継続的に監視してキーの変更を待ち、キーの更新をクライアントへストリーミングします。

### イベント {#events}

すべてのキーの各変更は、`Event`メッセージで表されます。`Event`メッセージは、更新データと更新の種類を提供します。

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

* `type` - イベントの種類です。PUTは、キーに新しいデータが保存されたことを示します。DELETEは、キーが削除されたことを示します。
* `kv` - イベントに関連付けられたKeyValueです。PUTイベントは現在のkvペアを含みます。kv.Version=1のPUTイベントは、キーが作成されたことを示します。DELETEイベントは、変更リビジョンが削除時のリビジョンに設定された、削除済みのキーを含みます。
* `prev_kv` - イベント直前のリビジョンにおける、そのキーのキー・バリューペアです。帯域幅を節約するため、監視で明示的に有効にした場合にだけ設定されます。

### 監視ストリーム {#watch-streams}

監視は長時間継続するリクエストであり、gRPCストリームでイベントデータをストリーミングします。監視ストリームは双方向です。クライアントはストリームに書き込んで監視を設定し、ストリームから読み取って監視イベントを受信します。イベントに監視ごとの識別子を付けることで、1つの監視ストリームに多数の異なる監視を多重化できます。この多重化によって、中核のetcdクラスターのメモリー使用量と接続の負担を減らせます。

監視イベントに関する保証については、[etcd APIの保証][watch-api-guarantees]を参照してください。

クライアントは、`Watch`が返したストリームで`WatchCreateRequest`を送信して、監視を作成します。

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

* `key`, `range_end` - 監視するキー範囲です。
* `start_revision` - 監視を開始するリビジョン（そのリビジョンを含む）で、省略可能です。指定しない場合、監視作成レスポンスのヘッダーにあるリビジョンの次からイベントをストリーミングします。最後のコンパクションリビジョンから、利用可能なイベント履歴全体を監視できます。
* `progress_notify` - 設定されている場合、最近のイベントがなければ、監視はイベントを含まないWatchResponseを定期的に受信します。これは、切断されたウォッチャーを、最近の既知のリビジョンから復旧したい場合に役立ちます。通知の送信頻度は、etcdサーバーが現在の負荷に基づいて決定します。
* `filters` - サーバー側で除外するイベントの種類のリストです。
* `prev_kv` - 設定されている場合、監視はイベント発生前のキー・バリューデータを受信します。上書きされたデータの確認に役立ちます。

クライアントは、`WatchCreateRequest`への応答として、または既存の監視で新しいイベントが発生した場合に、`WatchResponse`を受信します。

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

* `watch_id` - レスポンスに対応する監視のIDです。
* `created` - 監視作成リクエストへのレスポンスである場合にtrueに設定されます。クライアントはIDを保存し、そのストリームで監視イベントを受信するようにしてください。作成したウォッチャーへ送信されるすべてのイベントは、同じwatch_idを持ちます。
* `canceled` - 監視キャンセルリクエストへのレスポンスである場合にtrueに設定されます。キャンセルされたウォッチャーには、それ以降のイベントは送信されません。
* `compact_revision` - ウォッチャーがコンパクション済みリビジョンで監視しようとすると、etcdで利用可能な最小の過去のリビジョンに設定されます。これは、コンパクション済みリビジョンでウォッチャーを作成した場合や、ウォッチャーがキー・バリューストアの進行に追いつけない場合に発生します。ウォッチャーはキャンセルされます。同じstart_revisionで新しい監視を作成しても失敗します。
* `events` - 指定した監視IDに対応する、新しいイベントを順に並べたリストです。

クライアントが監視イベントの受信を停止するには、`WatchCancelRequest`を発行します。

```protobuf
message WatchCancelRequest {
   int64 watch_id = 1;
}
```

* `watch_id` - これ以上イベントを送信しないようキャンセルする監視のIDです。

## Lease API {#lease-api}

リースは、クライアントの生存を検出する仕組みです。クラスターは、生存時間付きのリースを付与します。指定したTTL期間内にetcdクラスターがkeepAliveを受信しなければ、リースは期限切れになります。

リースとキー・バリューストアを結び付けるため、各キーには最大1つのリースを関連付けられます。リースが期限切れになるか取り消されると、そのリースに関連付けられたすべてのキーが削除されます。期限切れになった各キーは、イベント履歴に削除イベントを生成します。

### リースの取得 {#obtaining-leases}

`LeaseGrantRequest`を受け取る`LeaseGrant` API呼び出しで、リースを取得します。

```protobuf
message LeaseGrantRequest {
  int64 TTL = 1;
  int64 ID = 2;
}
```

* `TTL` - 秒単位の希望する生存時間です。
* `ID` - リースに要求するIDです。IDを0に設定すると、etcdがIDを選択します。

クライアントは、`LeaseGrant`呼び出しから`LeaseGrantResponse`を受信します。

```protobuf
message LeaseGrantResponse {
  ResponseHeader header = 1;
  int64 ID = 2;
  int64 TTL = 3;
}
```

* `ID` - 付与されたリースのIDです。
* `TTL` - サーバーが選択した、秒単位のリースの生存時間です。

```protobuf
message LeaseRevokeRequest {
  int64 ID = 1;
}
```

* `ID` - 取り消すリースのIDです。リースを取り消すと、関連付けられたすべてのキーが削除されます。

### キープアライブ {#keep-alives}

リースは、`LeaseKeepAlive` API呼び出しで作成した双方向ストリームで更新します。クライアントがリースを更新するときは、ストリームで`LeaseKeepAliveRequest`を送信します。

```protobuf
message LeaseKeepAliveRequest {
  int64 ID = 1;
}
```

* `ID` - 維持するリースのIDです。

キープアライブストリームは、`LeaseKeepAliveResponse`で応答します。

```protobuf
message LeaseKeepAliveResponse {
  ResponseHeader header = 1;
  int64 ID = 2;
  int64 TTL = 3;
}
```

* `ID` - 新しいTTLで更新されたリースです。
* `TTL` - リースに残された、秒単位の新しい生存時間です。

[watch-api-guarantees]: /ja/etcd/learning/api_guarantees/#watch-apis
[elections]: https://github.com/etcd-io/etcd/blob/main/client/v3/concurrency/election.go
[grpc-api]: /ja/etcd/dev-guide/api_reference_v3/
[grpc-service]: https://github.com/etcd-io/etcd/blob/main/api/etcdserverpb/rpc.proto
[kv-proto]: https://github.com/etcd-io/etcd/blob/main/api/mvccpb/kv.proto
[locks]: https://github.com/etcd-io/etcd/blob/main/client/v3/concurrency/mutex.go
[mvcc]: https://en.wikipedia.org/wiki/Multiversion_concurrency_control
[stm]: https://github.com/etcd-io/etcd/blob/main/client/v3/concurrency/stm.go
