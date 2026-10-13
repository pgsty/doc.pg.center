---
title: gRPCゲートウェイを使う理由
weight: 3375
description: "gRPCゲートウェイの使用を検討する理由"
categories: [概念]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/api_grpc_gateway.md"
aliases: [/etcd/dev-guide/api_grpc_gateway/]
---

etcd v3は、メッセージングプロトコルに[gRPC][grpc]を使用します。etcdプロジェクトは、gRPCでetcdクラスターと通信するための、gRPCベースの[Goクライアント][go-client]とコマンドラインユーティリティー[etcdctl][etcdctl]を提供しています。gRPCをサポートしない言語向けには、JSONの[gRPCゲートウェイ][grpc-gateway]を提供しています。このゲートウェイはRESTfulなプロキシとして動作し、HTTP/JSONリクエストをgRPCメッセージに変換します。

## gRPCゲートウェイの使用 {#using-grpc-gateway}

ゲートウェイは、etcdの[Protocol Buffers][api-ref]メッセージ定義の[JSONマッピング][json-mapping]を受け付けます。`key`と`value`フィールドはバイト配列として定義されているため、JSONではbase64でエンコードする必要があります。以下の例では`curl`を使いますが、どのHTTP/JSONクライアントでも同様に動作するはずです。

### 注意事項 {#notes}

gRPCゲートウェイのエンドポイントは、etcd v3.3以降で変更されています。

- etcd v3.2以前は、`[CLIENT-URL]/v3alpha/*`だけを使用します。
- etcd v3.3は、`[CLIENT-URL]/v3alpha/*`を維持しつつ、`[CLIENT-URL]/v3beta/*`を使用します。
- etcd v3.4は、`[CLIENT-URL]/v3beta/*`を維持しつつ、`[CLIENT-URL]/v3/*`を使用します。
  - **`[CLIENT-URL]/v3alpha/*`は非推奨です**。
- etcd v3.5以降は、`[CLIENT-URL]/v3/*`だけを使用します。
  - **`[CLIENT-URL]/v3beta/*`は非推奨です**。

gRPC-gatewayは、TLSのCommon Nameを使った認証をサポートしていません。

### キーの書き込みと取得 {#put-and-get-keys}

`/v3/kv/range`と`/v3/kv/put`サービスで、キーを読み書きします。

```bash
<<COMMENT
https://www.base64encode.org/
foo is 'Zm9v' in Base64
bar is 'YmFy'
COMMENT

curl -L http://localhost:2379/v3/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
# {"header":{"cluster_id":"12585971608760269493","member_id":"13847567121247652255","revision":"2","raft_term":"3"}}

curl -L http://localhost:2379/v3/kv/range \
  -X POST -d '{"key": "Zm9v"}'
# {"header":{"cluster_id":"12585971608760269493","member_id":"13847567121247652255","revision":"2","raft_term":"3"},"kvs":[{"key":"Zm9v","create_revision":"2","mod_revision":"2","version":"1","value":"YmFy"}],"count":"1"}

# get all keys prefixed with "foo"
curl -L http://localhost:2379/v3/kv/range \
  -X POST -d '{"key": "Zm9v", "range_end": "Zm9w"}'
# {"header":{"cluster_id":"12585971608760269493","member_id":"13847567121247652255","revision":"2","raft_term":"3"},"kvs":[{"key":"Zm9v","create_revision":"2","mod_revision":"2","version":"1","value":"YmFy"}],"count":"1"}
```

### キーの監視 {#watch-keys}

`/v3/watch`サービスで、キーを監視します。

```bash
curl -N http://localhost:2379/v3/watch \
  -X POST -d '{"create_request": {"key":"Zm9v"} }' &
# {"result":{"header":{"cluster_id":"12585971608760269493","member_id":"13847567121247652255","revision":"1","raft_term":"2"},"created":true}}

curl -L http://localhost:2379/v3/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}' >/dev/null 2>&1
# {"result":{"header":{"cluster_id":"12585971608760269493","member_id":"13847567121247652255","revision":"2","raft_term":"2"},"events":[{"kv":{"key":"Zm9v","create_revision":"2","mod_revision":"2","version":"1","value":"YmFy"}}]}}
```

### トランザクション {#transactions}

`/v3/kv/txn`で、トランザクションを発行します。

```bash
# target CREATE
curl -L http://localhost:2379/v3/kv/txn \
  -X POST \
  -d '{"compare":[{"target":"CREATE","key":"Zm9v","createRevision":"2"}],"success":[{"requestPut":{"key":"Zm9v","value":"YmFy"}}]}'
# {"header":{"cluster_id":"12585971608760269493","member_id":"13847567121247652255","revision":"3","raft_term":"2"},"succeeded":true,"responses":[{"response_put":{"header":{"revision":"3"}}}]}
```

```bash
# target VERSION
curl -L http://localhost:2379/v3/kv/txn \
  -X POST \
  -d '{"compare":[{"version":"4","result":"EQUAL","target":"VERSION","key":"Zm9v"}],"success":[{"requestRange":{"key":"Zm9v"}}]}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"6","raft_term":"3"},"succeeded":true,"responses":[{"response_range":{"header":{"revision":"6"},"kvs":[{"key":"Zm9v","create_revision":"2","mod_revision":"6","version":"4","value":"YmF6"}],"count":"1"}}]}
```

### 認証 {#authentication}

`/v3/auth`サービスで、認証を設定します。

```bash
# create root user
curl -L http://localhost:2379/v3/auth/user/add \
  -X POST -d '{"name": "root", "password": "pass"}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"1","raft_term":"2"}}

# create root role
curl -L http://localhost:2379/v3/auth/role/add \
  -X POST -d '{"name": "root"}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"1","raft_term":"2"}}

# grant root role
curl -L http://localhost:2379/v3/auth/user/grant \
  -X POST -d '{"user": "root", "role": "root"}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"1","raft_term":"2"}}

# enable auth
curl -L http://localhost:2379/v3/auth/enable -X POST -d '{}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"1","raft_term":"2"}}
```

`/v3/auth/authenticate`でetcdの認証を行い、認証トークンを取得します。

```bash
# get the auth token for the root user
curl -L http://localhost:2379/v3/auth/authenticate \
  -X POST -d '{"name": "root", "password": "pass"}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"1","raft_term":"2"},"token":"sssvIpwfnLAcWAQH.9"}
```

認証情報を使ってキーを取得するには、`Authorization`ヘッダーに認証トークンを設定します。

```bash
curl -L http://localhost:2379/v3/kv/put \
  -H 'Authorization: sssvIpwfnLAcWAQH.9' \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"2","raft_term":"2"}}
```

### エラーレスポンス {#error-responses}

gRPCゲートウェイは、gRPCのステータスをHTTPステータスコードとJSONのエラー本文に変換します。
etcd v3.6以降は、grpc-gateway v2へのアップグレードによってエラー処理が変わりました
（v2移行ガイドの[エラー処理に関する注意事項][grpc-gateway-v2-errors]を参照）。
現在のゲートウェイの動作は、[GoogleのAPIエラーモデル][google-api-errors]で説明されている
`google.rpc.Status`（code、message、details）に沿っています。
以前のgrpc-gatewayにはトップレベルの`error`フィールドも含まれていましたが、
etcd v3.6以降では、このフィールドはサポートされていません。

クライアントは、HTTPステータスコードを成功・失敗の主な判断材料として扱ってください。
リクエストが失敗した場合は、`message`フィールドをエラー情報の主な情報源とし、
追加の詳細情報から、さらに詳しい状況を読み取ることを推奨します。

## Swagger {#swagger}

生成された[Swagger][swagger] API定義は、[rpc.swagger.json][swagger-doc]にあります。

[api-ref]: /ja/docs/etcd/dev-guide/api_reference_v3/
[etcdctl]: https://github.com/etcd-io/etcd/tree/main/etcdctl
[go-client]: https://github.com/etcd-io/etcd/tree/main/client/v3
[grpc]: https://www.grpc.io/
[grpc-gateway]: https://github.com/grpc-ecosystem/grpc-gateway
[grpc-gateway-v2-errors]: https://github.com/grpc-ecosystem/grpc-gateway/blob/main/docs/docs/development/grpc-gateway_v2_migration_guide.md#error-handling-configuration-has-been-overhauled
[json-mapping]: https://developers.google.com/protocol-buffers/docs/proto3#json
[google-api-errors]: https://cloud.google.com/apis/design/errors
[swagger]: http://swagger.io/
[swagger-doc]: /docs/etcd/dev-guide/apispec/swagger/rpc.swagger.json
