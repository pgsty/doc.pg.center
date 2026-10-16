---
title: Resolución de nombres y descubrimiento con gRPC
weight: 3500
description: "go-grpc: para resolver endpoints gRPC con un backend etcd"
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/grpc_naming.md"
---

etcd proporciona un resolvedor gRPC para admitir un sistema de nombres alternativo que obtiene de etcd los endpoints para descubrir servicios gRPC. El mecanismo subyacente se basa en observar las actualizaciones de las claves con el prefijo del nombre del servicio.

Ten en cuenta que esta característica es experimental porque depende del paquete [google.golang.org/grpc/resolver][], que sigue siendo experimental en grpc-go.

## Uso del descubrimiento de etcd con go-grpc {#using-etcd-discovery-with-go-grpc}

El cliente de etcd proporciona un resolvedor gRPC para resolver endpoints gRPC con un backend etcd. El resolvedor se inicializa con un cliente de etcd:

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

## Gestión de endpoints de servicio {#managing-service-endpoints}

El resolvedor de etcd trata todas las claves bajo el prefijo del objetivo de resolución seguido de una "/" (p. ej., "foo/bar/my-service/")
con valores codificados en JSON (históricamente go-grpc `naming.Update`) como endpoints de servicio potenciales.
Los endpoints se añaden al servicio creando claves nuevas y se eliminan del servicio borrando claves.

### Añadir un endpoint {#adding-an-endpoint}

Se pueden añadir endpoints nuevos al servicio mediante `etcdctl`:

```sh
ETCDCTL_API=3 etcdctl put foo/bar/my-service/1.2.3.4 '{"Addr":"1.2.3.4"}'
```

El método `endpoints.Manager` del cliente de etcd también puede registrar endpoints nuevos con una clave que coincida con `Addr`:

```go

em := endpoints.NewManager(client, "foo/bar/my-service")
err := em.AddEndpoint(context.TODO(),"foo/bar/my-service/e1", endpoints.Endpoint{Addr:"1.2.3.4"})
```
Para activar el balanceo de carga round-robin al conectarte a un servicio con varios endpoints, puedes configurar tu conexión con el
 balanceador de carga round-robin interno de gRPC:

 ```go

conn, gerr := grpc.NewClient("etcd:///foo", grpc.WithResolvers(etcdResolver),
grpc.WithDefaultServiceConfig(`{"loadBalancingPolicy":"round_robin"}`))
 ```

### Eliminar un endpoint {#deleting-an-endpoint}

Los hosts pueden eliminarse del servicio mediante `etcdctl`:

```sh
ETCDCTL_API=3 etcdctl del foo/bar/my-service/1.2.3.4
```

El método `endpoints.Manager` del cliente de etcd también admite la eliminación de endpoints:

```go
em := endpoints.NewManager(client, "foo/bar/my-service")
err := em.DeleteEndpoint(context.TODO(), "foo/bar/my-service/e1")
```

### Registrar un endpoint con una concesión {#registering-an-endpoint-with-a-lease}

Registrar un endpoint con una concesión garantiza que, si el host no puede mantener un latido de mantenimiento (p. ej., si su máquina falla), se elimine del servicio:

```sh
lease=`ETCDCTL_API=3 etcdctl lease grant 5 | cut -f2 -d' '`
ETCDCTL_API=3 etcdctl put --lease=$lease my-service/1.2.3.4 '{"Addr":"1.2.3.4"}'
ETCDCTL_API=3 etcdctl lease keep-alive $lease
```
En Go:

```go
em := endpoints.NewManager(client, "foo/bar/my-service")
err := em.AddEndpoint(context.TODO(), "foo/bar/my-service/e1", endpoints.Endpoint{Addr:"1.2.3.4"})
```

### Actualización atómica de endpoints {#atomically-updating-endpoints}

Si se desea modificar varios endpoints en una sola transacción, se puede usar `endpoints.Manager` directamente:

```
em := endpoints.NewManager(c, "foo")

err := em.Update(context.TODO(), []*endpoints.UpdateWithOpts{
    endpoints.NewDeleteUpdateOpts("foo/bar/my-service/e1", endpoints.Endpoint{Addr: "1.2.3.4"}),
	endpoints.NewAddUpdateOpts("foo/bar/my-service/e1", endpoints.Endpoint{Addr: "1.2.3.14"})})
```

[google.golang.org/grpc/resolver]: https://github.com/grpc/grpc-go/tree/4cedec40eb2ccfbe3f56bb15e894903111ada2d2/resolver
