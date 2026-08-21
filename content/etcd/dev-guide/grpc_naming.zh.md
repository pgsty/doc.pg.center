---
title: gRPC 命名与发现
weight: 3500
description: "go-grpc：使用 etcd 后端解析 gRPC 端点"
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/a9ee660fdbf9584deb4af639c4dc63b01413e44f/content/en/docs/v3.7/dev-guide/grpc_naming.md"
---

etcd 提供了一个 gRPC 解析器，用于支持一种替代名称系统，该系统从 etcd 获取端点以发现 gRPC 服务。其底层机制基于监听以服务名称为前缀的键的更新。

请注意，此功能为实验性功能，因为它依赖于 [google.golang.org/grpc/resolver][] 包，而该包在 grpc-go 中仍处于实验阶段。

## 使用 go-grpc 实现 etcd 发现 {#using-etcd-discovery-with-go-grpc}

etcd 客户端为使用 etcd 后端解析 gRPC 端点提供了 gRPC 解析器。该解析器通过一个 etcd 客户端进行初始化：

```go
import (
	clientv3 "go.etcd.io/etcd/client/v3"
	etcdnaming "go.etcd.io/etcd/client/v3/naming/resolver"

	"google.golang.org/grpc"
)

...

cli, err := clientv3.NewFromURL("http://localhost:2379")
if err != nil {
    // ...
}
r, err := etcdnaming.NewBuilder(cli)
if err != nil {
    // ...
}
conn, gerr := grpc.NewClient("my-service", grpc.WithResolvers(r), ...)
```

## 管理服务端点 {#managing-service-endpoints}

etcd 解析器将解析目标前缀下所有以 "/" 分隔的键（例如 "foo/bar/my-service/"）视为潜在服务端点，这些键对应的值需为 JSON 编码格式（历史版本为 go-grpc `naming.Update`）。通过创建新键将端点添加至服务，通过删除键将端点从服务中移除。

### 添加端点 {#adding-an-endpoint}

可通过 `etcdctl` 向服务添加新的端点：

```sh
ETCDCTL_API=3 etcdctl put foo/bar/my-service/1.2.3.4 '{"Addr":"1.2.3.4"}'
```

etcd 客户端的 `endpoints.Manager` 方法还可注册新的端点，其键与 `Addr` 匹配：

```go

em := endpoints.NewManager(client, "foo/bar/my-service")
err := em.AddEndpoint(context.TODO(),"foo/bar/my-service/e1", endpoints.Endpoint{Addr:"1.2.3.4"})
```
当通过多个端点连接服务时，若要启用轮询负载均衡，可使用 gRPC 内置的轮询负载均衡器配置连接：

 ```go

conn, gerr := grpc.NewClient("etcd:///foo", grpc.WithResolvers(etcdResolver),
grpc.WithDefaultServiceConfig(`{"loadBalancingPolicy":"round_robin"}`))
 ```

### 删除端点 {#deleting-an-endpoint}

可通过 `etcdctl` 从服务中删除主机：

```sh
ETCDCTL_API=3 etcdctl del foo/bar/my-service/1.2.3.4
```

etcd 客户端的 `endpoints.Manager` 方法还支持删除端点：

```go
em := endpoints.NewManager(client, "foo/bar/my-service")
err := em.DeleteEndpoint(context.TODO(), "foo/bar/my-service/e1")
```

### 使用租约注册端点 {#registering-an-endpoint-with-a-lease}

使用租约注册端点可确保，若主机无法维持保活心跳（例如其所在机器发生故障），该端点将从服务中移除：

```sh
lease=`ETCDCTL_API=3 etcdctl lease grant 5 | cut -f2 -d' '`
ETCDCTL_API=3 etcdctl put --lease=$lease my-service/1.2.3.4 '{"Addr":"1.2.3.4"}'
ETCDCTL_API=3 etcdctl lease keep-alive $lease
```
在 Go 语言中：

```go
em := endpoints.NewManager(client, "foo/bar/my-service")
err := em.AddEndpoint(context.TODO(), "foo/bar/my-service/e1", endpoints.Endpoint{Addr:"1.2.3.4"})
```

### 原子性更新端点 {#atomically-updating-endpoints}

若需在单个事务中修改多个端点，可直接使用 `endpoints.Manager`：

```
em := endpoints.NewManager(c, "foo")

err := em.Update(context.TODO(), []*endpoints.UpdateWithOpts{
    endpoints.NewDeleteUpdateOpts("foo/bar/my-service/e1", endpoints.Endpoint{Addr: "1.2.3.4"}),
	endpoints.NewAddUpdateOpts("foo/bar/my-service/e1", endpoints.Endpoint{Addr: "1.2.3.14"})})
```

[google.golang.org/grpc/resolver]: https://github.com/grpc/grpc-go/tree/4cedec40eb2ccfbe3f56bb15e894903111ada2d2/resolver
