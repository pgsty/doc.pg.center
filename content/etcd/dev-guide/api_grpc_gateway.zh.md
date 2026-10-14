---
title: 为什么使用 gRPC 网关
weight: 3375
description: 为何应考虑使用 gRPC 网关
categories: [概念]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/api_grpc_gateway.md"
---

etcd v3 使用 [gRPC][grpc] 作为其消息协议。etcd 项目包含一个基于 gRPC 的 [Go 客户端][go-client]，以及一个命令行工具 [etcdctl][etcdctl]，用于通过 gRPC 与 etcd 集群通信。对于不支持 gRPC 的语言，etcd 提供一个 JSON [gRPC 网关][grpc-gateway]。该网关提供一个 RESTful 代理，可将 HTTP/JSON 请求转换为 gRPC 消息。

## 使用 gRPC 网关 {#using-grpc-gateway}

网关接受 etcd 的 [协议缓冲][api-ref] 消息定义的 [JSON 映射][json-mapping]。请注意，`key` 和 `value` 字段定义为字节数组，因此在 JSON 中必须进行 base64 编码。以下示例使用 `curl`，但任何 HTTP/JSON 客户端均可正常工作。

### 备注 {#notes}

自 etcd v3.3 起，gRPC 网关端点已更改：

- etcd v3.2 或更早版本仅使用 `[CLIENT-URL]/v3alpha/*`。
- etcd v3.3 使用 `[CLIENT-URL]/v3beta/*`，同时保留 `[CLIENT-URL]/v3alpha/*`。
- etcd v3.4 使用 `[CLIENT-URL]/v3/*`，同时保留 `[CLIENT-URL]/v3beta/*`。
  - **`[CLIENT-URL]/v3alpha/*` 已弃用**。
- etcd v3.5 或更高版本仅使用 `[CLIENT-URL]/v3/*`。
  - **`[CLIENT-URL]/v3beta/*` 已弃用**。

gRPC 网关不支持使用 TLS 通用名称进行身份认证。

### 设置和获取键 {#put-and-get-keys}

使用 `/v3/kv/range` 和 `/v3/kv/put` 服务读写键：

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

### 监听键 {#watch-keys}

使用 `/v3/watch` 服务监听键：

```bash
curl -N http://localhost:2379/v3/watch \
  -X POST -d '{"create_request": {"key":"Zm9v"} }' &
# {"result":{"header":{"cluster_id":"12585971608760269493","member_id":"13847567121247652255","revision":"1","raft_term":"2"},"created":true}}

curl -L http://localhost:2379/v3/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}' >/dev/null 2>&1
# {"result":{"header":{"cluster_id":"12585971608760269493","member_id":"13847567121247652255","revision":"2","raft_term":"2"},"events":[{"kv":{"key":"Zm9v","create_revision":"2","mod_revision":"2","version":"1","value":"YmFy"}}]}}
```

### 事务 {#transactions}

使用 `/v3/kv/txn` 发起一个事务：

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

### 身份认证 {#authentication}

使用 `/v3/auth` 服务设置身份认证：

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

使用 `/v3/auth/authenticate` 对 etcd 进行身份认证以获取身份认证令牌：

```bash
# get the auth token for the root user
curl -L http://localhost:2379/v3/auth/authenticate \
  -X POST -d '{"name": "root", "password": "pass"}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"1","raft_term":"2"},"token":"sssvIpwfnLAcWAQH.9"}
```

将 `Authorization` 请求头设置为身份认证令牌，以使用身份认证凭据获取键：

```bash
curl -L http://localhost:2379/v3/kv/put \
  -H 'Authorization: sssvIpwfnLAcWAQH.9' \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"2","raft_term":"2"}}
```

### 错误响应 {#error-responses}

gRPC 网关将 gRPC 状态转换为 HTTP 状态码和 JSON 错误正文。从 etcd v3.6 开始，升级至 grpc-gateway v2 改变了错误处理方式（参见 v2 迁移指南中的 [错误处理说明][grpc-gateway-v2-errors]），网关行为现在与 `google.rpc.Status`（代码、消息、详情）一致，如 [Google API 错误模型][google-api-errors] 所述。历史上，较早版本的 grpc-gateway 也包含一个顶层 `error` 字段，但该字段在 etcd v3.6 及更高版本中不再受支持。

客户端应将 HTTP 状态码作为判断成功或失败的主要依据。若请求失败，客户端应以 `message` 字段作为错误信息的主要来源，并可使用其他附加信息获取进一步上下文。

## Swagger 接口文档 {#swagger}

生成的 [Swagger][swagger] API 定义可在 [rpc.swagger.json][swagger-doc] 中找到。

[api-ref]: /zh/etcd/dev-guide/api_reference_v3/
[etcdctl]: https://github.com/etcd-io/etcd/tree/main/etcdctl
[go-client]: https://github.com/etcd-io/etcd/tree/main/client/v3
[grpc]: https://www.grpc.io/
[grpc-gateway]: https://github.com/grpc-ecosystem/grpc-gateway
[grpc-gateway-v2-errors]: https://github.com/grpc-ecosystem/grpc-gateway/blob/main/docs/docs/development/grpc-gateway_v2_migration_guide.md#error-handling-configuration-has-been-overhauled
[json-mapping]: https://developers.google.com/protocol-buffers/docs/proto3#json
[google-api-errors]: https://cloud.google.com/apis/design/errors
[swagger]: http://swagger.io/
[swagger-doc]: /etcd/dev-guide/apispec/swagger/rpc.swagger.json
