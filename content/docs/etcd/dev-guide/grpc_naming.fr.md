---
title: Découverte et nommage gRPC
weight: 3500
description: "go-grpc : pour résoudre les points d'extrémité gRPC avec un backend etcd"
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/dev-guide/grpc_naming.md"
aliases: [/etcd/dev-guide/grpc_naming/]
---

etcd fournit un résolveur gRPC afin de prendre en charge un système de noms alternatif qui récupère les points d'accès depuis etcd pour la découverte de services gRPC. Le mécanisme sous-jacent repose sur la surveillance des mises à jour des clés préfixées par le nom du service.

Notez que cette fonctionnalité est expérimentale car elle dépend du paquet [google.golang.org/grpc/resolver][], qui reste expérimental dans grpc-go.

## Utilisation de la découverte etcd avec go-grpc {#using-etcd-discovery-with-go-grpc}

Le client etcd fournit un résolveur gRPC permettant de résoudre les points d'accès gRPC à l'aide d'un backend etcd. Le résolveur est initialisé avec un client etcd :

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

## Gestion des points de terminaison de service {#managing-service-endpoints}

Le résolveur etcd traite toutes les clés situées sous le préfixe de la cible de résolution suivant un "/" (par exemple, "foo/bar/my-service/")
dont les valeurs sont encodées au format JSON (historiquement go-grpc `naming.Update`) comme des points de terminaison de service potentiels.
Les points de terminaison sont ajoutés au service en créant de nouvelles clés et supprimés du service en supprimant des clés.

### Ajout d’un point de terminaison {#adding-an-endpoint}

De nouveaux points de terminaison peuvent être ajoutés au service via `etcdctl` :

```sh
ETCDCTL_API=3 etcdctl put foo/bar/my-service/1.2.3.4 '{"Addr":"1.2.3.4"}'
```

La méthode `endpoints.Manager` du client etcd peut également enregistrer de nouveaux points d'accès avec une clé correspondant à `Addr` :

```go

em := endpoints.NewManager(client, "foo/bar/my-service")
err := em.AddEndpoint(context.TODO(),"foo/bar/my-service/e1", endpoints.Endpoint{Addr:"1.2.3.4"})
```
Pour activer l’équilibrage de charge en boucle (round-robin) lors de la connexion à un service disposant de plusieurs points d’accès, vous pouvez configurer votre connexion avec le chargeur de charge interne gRPC en boucle :

 ```go

conn, gerr := grpc.NewClient("etcd:///foo", grpc.WithResolvers(etcdResolver),
grpc.WithDefaultServiceConfig(`{"loadBalancingPolicy":"round_robin"}`))
 ```

### Suppression d'un point de terminaison {#deleting-an-endpoint}

Les hôtes peuvent être supprimés du service via `etcdctl` :

```sh
ETCDCTL_API=3 etcdctl del foo/bar/my-service/1.2.3.4
```

La méthode `endpoints.Manager` du client etcd prend également en charge la suppression des points de terminaison :

```go
em := endpoints.NewManager(client, "foo/bar/my-service")
err := em.DeleteEndpoint(context.TODO(), "foo/bar/my-service/e1")
```

### Inscrire un point de terminaison avec un bail {#registering-an-endpoint-with-a-lease}

Inscrire un point de terminaison avec un bail garantit que, si l'hôte ne peut pas maintenir un signal de cœur (par exemple, en cas de panne matérielle), il sera retiré du service :

```sh
lease=`ETCDCTL_API=3 etcdctl lease grant 5 | cut -f2 -d' '`
ETCDCTL_API=3 etcdctl put --lease=$lease my-service/1.2.3.4 '{"Addr":"1.2.3.4"}'
ETCDCTL_API=3 etcdctl lease keep-alive $lease
```
En Go :

```go
em := endpoints.NewManager(client, "foo/bar/my-service")
err := em.AddEndpoint(context.TODO(), "foo/bar/my-service/e1", endpoints.Endpoint{Addr:"1.2.3.4"})
```

### Mise à jour atomique des points de terminaison {#atomically-updating-endpoints}

Si l'on souhaite modifier plusieurs points de terminaison dans une seule transaction, `endpoints.Manager` peut être utilisé directement :

```
em := endpoints.NewManager(c, "foo")

err := em.Update(context.TODO(), []*endpoints.UpdateWithOpts{
    endpoints.NewDeleteUpdateOpts("foo/bar/my-service/e1", endpoints.Endpoint{Addr: "1.2.3.4"}),
	endpoints.NewAddUpdateOpts("foo/bar/my-service/e1", endpoints.Endpoint{Addr: "1.2.3.14"})})
```

[google.golang.org/grpc/resolver]: https://github.com/grpc/grpc-go/tree/4cedec40eb2ccfbe3f56bb15e894903111ada2d2/resolver
