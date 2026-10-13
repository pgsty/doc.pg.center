---
title: Именование и обнаружение gRPC
weight: 3500
description: "go-grpc: разрешение конечных точек gRPC с бэкендом etcd"
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/grpc_naming.md"
aliases: [/etcd/dev-guide/grpc_naming/]
---

etcd предоставляет резолвер gRPC для поддержки альтернативной системы имён, которая получает конечные точки из etcd при обнаружении служб gRPC. Механизм основан на наблюдении за обновлениями ключей с префиксом имени службы.

Эта возможность является экспериментальной, поскольку зависит от пакета [google.golang.org/grpc/resolver][], который всё ещё считается экспериментальным в grpc-go.

## Использование обнаружения etcd с go-grpc {#using-etcd-discovery-with-go-grpc}

Клиент etcd предоставляет резолвер gRPC для разрешения конечных точек gRPC с бэкендом etcd. Резолвер инициализируется клиентом etcd:

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

## Управление конечными точками службы {#managing-service-endpoints}

Резолвер etcd рассматривает как потенциальные конечные точки службы все ключи под префиксом целевого имени с завершающим "/" (например, "foo/bar/my-service/"), значения которых закодированы в JSON (исторически — go-grpc `naming.Update`).
Конечные точки добавляются созданием новых ключей и удаляются удалением ключей.

### Добавление конечной точки {#adding-an-endpoint}

Новые конечные точки можно добавить в службу с помощью `etcdctl`:

```sh
ETCDCTL_API=3 etcdctl put foo/bar/my-service/1.2.3.4 '{"Addr":"1.2.3.4"}'
```

Метод `endpoints.Manager` клиента etcd также может зарегистрировать новую конечную точку с ключом, соответствующим `Addr`:

```go

em := endpoints.NewManager(client, "foo/bar/my-service")
err := em.AddEndpoint(context.TODO(),"foo/bar/my-service/e1", endpoints.Endpoint{Addr:"1.2.3.4"})
```
Чтобы включить циклическую балансировку нагрузки при подключении к службе с несколькими конечными точками, настройте соединение с внутренним циклическим балансировщиком gRPC:

 ```go

conn, gerr := grpc.NewClient("etcd:///foo", grpc.WithResolvers(etcdResolver),
grpc.WithDefaultServiceConfig(`{"loadBalancingPolicy":"round_robin"}`))
 ```

### Удаление конечной точки {#deleting-an-endpoint}

Узлы можно удалить из службы с помощью `etcdctl`:

```sh
ETCDCTL_API=3 etcdctl del foo/bar/my-service/1.2.3.4
```

Метод `endpoints.Manager` клиента etcd также поддерживает удаление конечных точек:

```go
em := endpoints.NewManager(client, "foo/bar/my-service")
err := em.DeleteEndpoint(context.TODO(), "foo/bar/my-service/e1")
```

### Регистрация конечной точки с арендой {#registering-an-endpoint-with-a-lease}

Регистрация конечной точки с арендой гарантирует её удаление из службы, если узел не сможет поддерживать heartbeat keepalive, например из-за отказа машины:

```sh
lease=`ETCDCTL_API=3 etcdctl lease grant 5 | cut -f2 -d' '`
ETCDCTL_API=3 etcdctl put --lease=$lease my-service/1.2.3.4 '{"Addr":"1.2.3.4"}'
ETCDCTL_API=3 etcdctl lease keep-alive $lease
```
В Golang:

```go
em := endpoints.NewManager(client, "foo/bar/my-service")
err := em.AddEndpoint(context.TODO(), "foo/bar/my-service/e1", endpoints.Endpoint{Addr:"1.2.3.4"})
```

### Атомарное обновление конечных точек {#atomically-updating-endpoints}

Чтобы изменить несколько конечных точек в одной транзакции, можно напрямую использовать `endpoints.Manager`:

```
em := endpoints.NewManager(c, "foo")

err := em.Update(context.TODO(), []*endpoints.UpdateWithOpts{
    endpoints.NewDeleteUpdateOpts("foo/bar/my-service/e1", endpoints.Endpoint{Addr: "1.2.3.4"}),
	endpoints.NewAddUpdateOpts("foo/bar/my-service/e1", endpoints.Endpoint{Addr: "1.2.3.14"})})
```

[google.golang.org/grpc/resolver]: https://github.com/grpc/grpc-go/tree/4cedec40eb2ccfbe3f56bb15e894903111ada2d2/resolver
