---
title: gRPC-Namensauflösung und Discovery
weight: 3500
description: "go-grpc: gRPC-Endpunkte mit einem etcd-Backend auflösen"
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/grpc_naming.md"
aliases: [/etcd/dev-guide/grpc_naming/]
---

etcd stellt einen gRPC-Resolver für ein alternatives Namenssystem bereit, das Endpunkte aus etcd abruft, um gRPC-Dienste zu finden. Der zugrunde liegende Mechanismus beobachtet Änderungen an Schlüsseln, deren Präfix der Dienstname ist.

Diese Funktion ist experimentell, da sie vom Paket [google.golang.org/grpc/resolver][] abhängt, das in grpc-go noch experimentell ist.

## etcd-Discovery mit go-grpc verwenden {#using-etcd-discovery-with-go-grpc}

Der etcd-Client stellt einen gRPC-Resolver bereit, der gRPC-Endpunkte mit einem etcd-Backend auflöst. Der Resolver wird mit einem etcd-Client initialisiert:

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

## Dienstendpunkte verwalten {#managing-service-endpoints}

Der etcd-Resolver betrachtet alle Schlüssel unter dem Präfix des Auflösungsziels, gefolgt von einem "/" (z. B. "foo/bar/my-service/"),
mit JSON-kodierten Werten (früher go-grpc `naming.Update`) als mögliche Dienstendpunkte.
Durch Anlegen neuer Schlüssel werden Endpunkte zum Dienst hinzugefügt; durch Löschen der Schlüssel werden sie entfernt.

### Einen Endpunkt hinzufügen {#adding-an-endpoint}

Neue Endpunkte lassen sich mit `etcdctl` zum Dienst hinzufügen:

```sh
ETCDCTL_API=3 etcdctl put foo/bar/my-service/1.2.3.4 '{"Addr":"1.2.3.4"}'
```

Die Methode `endpoints.Manager` des etcd-Clients kann ebenfalls neue Endpunkte mit einem zu `Addr` passenden Schlüssel registrieren:

```go

em := endpoints.NewManager(client, "foo/bar/my-service")
err := em.AddEndpoint(context.TODO(),"foo/bar/my-service/e1", endpoints.Endpoint{Addr:"1.2.3.4"})
```
Um beim Verbindungsaufbau zu einem Dienst mit mehreren Endpunkten Round-Robin-Lastverteilung zu aktivieren, kann die Verbindung mit dem
 internen Round-Robin-Load-Balancer von grpc eingerichtet werden:

 ```go

conn, gerr := grpc.NewClient("etcd:///foo", grpc.WithResolvers(etcdResolver),
grpc.WithDefaultServiceConfig(`{"loadBalancingPolicy":"round_robin"}`))
 ```

### Einen Endpunkt löschen {#deleting-an-endpoint}

Hosts lassen sich mit `etcdctl` aus dem Dienst entfernen:

```sh
ETCDCTL_API=3 etcdctl del foo/bar/my-service/1.2.3.4
```

Die Methode `endpoints.Manager` des etcd-Clients unterstützt auch das Löschen von Endpunkten:

```go
em := endpoints.NewManager(client, "foo/bar/my-service")
err := em.DeleteEndpoint(context.TODO(), "foo/bar/my-service/e1")
```

### Einen Endpunkt mit einer Lease registrieren {#registering-an-endpoint-with-a-lease}

Die Registrierung eines Endpunkts mit einer Lease stellt sicher, dass er aus dem Dienst entfernt wird, wenn der Host keinen Keepalive-Heartbeat mehr aufrechterhalten kann, etwa bei einem Ausfall des Rechners:

```sh
lease=`ETCDCTL_API=3 etcdctl lease grant 5 | cut -f2 -d' '`
ETCDCTL_API=3 etcdctl put --lease=$lease my-service/1.2.3.4 '{"Addr":"1.2.3.4"}'
ETCDCTL_API=3 etcdctl lease keep-alive $lease
```
In Go:

```go
em := endpoints.NewManager(client, "foo/bar/my-service")
err := em.AddEndpoint(context.TODO(), "foo/bar/my-service/e1", endpoints.Endpoint{Addr:"1.2.3.4"})
```

### Endpunkte atomar aktualisieren {#atomically-updating-endpoints}

Um mehrere Endpunkte in einer einzigen Transaktion zu ändern, kann `endpoints.Manager` direkt verwendet werden:

```
em := endpoints.NewManager(c, "foo")

err := em.Update(context.TODO(), []*endpoints.UpdateWithOpts{
    endpoints.NewDeleteUpdateOpts("foo/bar/my-service/e1", endpoints.Endpoint{Addr: "1.2.3.4"}),
	endpoints.NewAddUpdateOpts("foo/bar/my-service/e1", endpoints.Endpoint{Addr: "1.2.3.14"})})
```

[google.golang.org/grpc/resolver]: https://github.com/grpc/grpc-go/tree/4cedec40eb2ccfbe3f56bb15e894903111ada2d2/resolver
