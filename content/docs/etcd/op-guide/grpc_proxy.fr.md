---
title: Proxy gRPC
weight: 4350
description: Un proxy inverse etcd sans état fonctionnant au niveau gRPC
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/grpc_proxy.md"
aliases: [/etcd/op-guide/grpc_proxy/]
---

Le proxy gRPC est un proxy inverse etcd sans état fonctionnant au niveau du protocole gRPC (L7). Le proxy est conçu pour réduire la charge de traitement totale imposée au cluster etcd principal. Pour assurer une évolutivité horizontale, il regroupe les requêtes d'API de surveillance et de bail. Pour protéger le cluster contre les clients abusifs, il met en cache les requêtes portant sur des plages de clés.

Le proxy gRPC prend en charge plusieurs points d'entrée de serveur etcd. Au démarrage du proxy, il choisit aléatoirement un point d'entrée de serveur etcd à utiliser. Ce point d'entrée traite toutes les requêtes jusqu'à ce que le proxy détecte une défaillance. Si le proxy gRPC détecte une défaillance d'un point d'entrée, il bascule vers un autre point d'entrée, si disponible, afin de masquer les défaillances à ses clients. D'autres politiques de réessai, telles que le round-robin pondéré, pourraient être prises en charge à l'avenir.

## API de surveillance évolutive {#scalable-watch-api}

Le proxy gRPC regroupe plusieurs observateurs clients (`c-watchers`) sur la même clé ou plage en un seul observateur (`s-watcher`) connecté à un serveur etcd. Le proxy diffuse tous les événements provenant du `s-watcher` à ses `c-watchers`.

En supposant que N clients effectuent une surveillance sur la même clé, un proxy gRPC peut réduire la charge de surveillance sur le serveur etcd de N à 1. Les utilisateurs peuvent déployer plusieurs proxies gRPC afin de répartir davantage la charge du serveur.

Dans l'exemple suivant, trois clients effectuent une surveillance sur la clé A. Le proxy gRPC regroupe les trois observateurs, créant un seul observateur attaché au serveur etcd.

```
            +-------------+
            | etcd server |
            +------+------+
                   ^ watch key A (s-watcher)
                   |
           +-------+-----+
           | gRPC proxy  | <-------+
           |             |         |
           ++-----+------+         |watch key A (c-watcher)
watch key A ^     ^ watch key A    |
(c-watcher) |     | (c-watcher)    |
    +-------+-+  ++--------+  +----+----+
    |  client |  |  client |  |  client |
    |         |  |         |  |         |
    +---------+  +---------+  +---------+
```

### Limitations {#limitations}

Pour effectuer une coalescence efficace de plusieurs observateurs clients en un seul observateur, le proxy gRPC effectue une coalescence des nouveaux `c-watchers` vers un `s-watcher` existant lorsque cela est possible. Ce `s-watcher` coalescé peut être hors synchronisation avec le serveur etcd en raison de retards réseau ou d’événements mis en mémoire tampon non livrés. Lorsque la révision de surveillance n’est pas précisée, le proxy gRPC ne garantit pas que le `c-watcher` commencera à surveiller à partir de la révision la plus récente du magasin. Par exemple, si un client surveille à partir d’un serveur etcd avec la révision 1000, cet observateur commencera à la révision 1000. Si un client surveille à partir du proxy gRPC, il peut commencer à surveiller à partir de la révision 990.

Des limitations similaires s'appliquent à l'annulation. Lorsqu'un observateur est annulé, la révision du serveur etcd peut être supérieure à la révision de la réponse d'annulation.

Ces deux limitations ne devraient pas poser de problème pour la plupart des cas d'utilisation. À l'avenir, des options supplémentaires pourraient être disponibles afin de forcer l'observateur à contourner le proxy gRPC pour des réponses de révision plus précises.

## API de bail évolutive {#scalable-lease-api}

Pour maintenir ses baux actifs, un client doit établir au moins un flux gRPC avec un serveur etcd afin d'envoyer des signaux d'activité périodiques. Si une charge de travail etcd implique une activité de bail importante répartie sur de nombreux clients, ces flux peuvent entraîner une utilisation excessive du processeur. Pour réduire le nombre total de flux sur le cluster principal, le proxy prend en charge la fusion des flux de bail.

En supposant que N clients mettent à jour des baux, un unique proxy gRPC réduit la charge des flux sur le serveur etcd de N à 1. Les déploiements peuvent inclure des proxies gRPC supplémentaires afin de répartir davantage les flux sur plusieurs proxies.

Dans l'exemple suivant, trois clients mettent à jour trois baux indépendants (`L1`, `L2` et `L3`). Le proxy gRPC fusionne les trois flux de bail client (`c-streams`) en un seul flux de renouvellement de bail (`s-stream`) associé à un serveur etcd. Le proxy transfère les battements de cœur de bail côté client provenant des flux c vers le flux s, puis renvoie les réponses aux flux c correspondants.

```
          +-------------+
          | etcd server |
          +------+------+
                 ^
                 | heartbeat L1, L2, L3
                 | (s-stream)
                 v
         +-------+-----+
         | gRPC proxy  +<-----------+
         +---+------+--+            | heartbeat L3
             ^      ^               | (c-stream)
heartbeat L1 |      | heartbeat L2  |
(c-stream)   v      v (c-stream)    v
      +------+-+  +-+------+  +-----+--+
      | client |  | client |  | client |
      +--------+  +--------+  +--------+
```

## Protection contre les clients abusifs {#abusive-clients-protection}

Le proxy gRPC met en cache les réponses aux requêtes lorsqu'il ne compromet pas les exigences de cohérence. Cela peut protéger le serveur etcd contre les clients abusifs exécutant des boucles serrées.

## Démarrer le proxy gRPC etcd {#start-etcd-grpc-proxy}

Considérez un cluster etcd avec les points de terminaison statiques suivants :

|Nom|Adresse|Nom d'hôte|
|------|---------|------------------|
|infra0|10.0.1.10|infra0.example.com|
|infra1|10.0.1.11|infra1.example.com|
|infra2|10.0.1.12|infra2.example.com|

Démarrez le proxy gRPC etcd pour utiliser ces points de terminaison statiques avec la commande :

```bash
$ etcd grpc-proxy start --endpoints=infra0.example.com,infra1.example.com,infra2.example.com --listen-addr=127.0.0.1:2379
```

Le proxy gRPC etcd démarre et écoute sur le port 2379. Il achemine les requêtes clientes vers l'un des trois points de terminaison fournis ci-dessus.

Envoi de requêtes via le proxy :

```bash
$ ETCDCTL_API=3 etcdctl --endpoints=127.0.0.1:2379 put foo bar
OK
$ ETCDCTL_API=3 etcdctl --endpoints=127.0.0.1:2379 get foo
foo
bar
```

## Synchronisation des points de terminaison client et résolution de noms {#client-endpoint-synchronization-and-name-resolution}

Le proxy prend en charge l'enregistrement de ses points d'accès pour la découverte, en écrivant sur un point d'accès défini par l'utilisateur. Cela sert deux objectifs. Premièrement, cela permet aux clients de synchroniser leurs points d'accès avec un ensemble de points d'accès du proxy afin d'assurer une haute disponibilité. Deuxièmement, il agit comme un fournisseur de points d'accès pour etcd [résolution de noms gRPC](/fr/docs/etcd/dev-guide/grpc_naming/).

Enregistrez le ou les proxies en précisant un préfixe défini par l'utilisateur :

```bash
$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23790 \
  --advertise-client-url=127.0.0.1:23790 \
  --resolver-prefix="___grpc_proxy_endpoint" \
  --resolver-ttl=60

$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23791 \
  --advertise-client-url=127.0.0.1:23791 \
  --resolver-prefix="___grpc_proxy_endpoint" \
  --resolver-ttl=60
```

Le proxy répertoriera tous ses membres dans la liste des membres :

```bash
ETCDCTL_API=3 etcdctl --endpoints=http://localhost:23790 member list --write-out table

+----+---------+--------------------------------+------------+-----------------+
| ID | STATUS  |              NAME              | PEER ADDRS |  CLIENT ADDRS   |
+----+---------+--------------------------------+------------+-----------------+
|  0 | started | Gyu-Hos-MBP.sfo.coreos.systems |            | 127.0.0.1:23791 |
|  0 | started | Gyu-Hos-MBP.sfo.coreos.systems |            | 127.0.0.1:23790 |
+----+---------+--------------------------------+------------+-----------------+
```

Cela permet aux clients de découvrir automatiquement les points d'accès du proxy via Sync :

```go
cli, err := clientv3.New(clientv3.Config{
    Endpoints: []string{"http://localhost:23790"},
})
if err != nil {
    log.Fatal(err)
}
defer cli.Close()

// fetch registered grpc-proxy endpoints
if err := cli.Sync(context.Background()); err != nil {
    log.Fatal(err)
}
```

Notez qu’en cas de configuration d’un proxy sans préfixe de résolveur,

```bash
$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23792 \
  --advertise-client-url=127.0.0.1:23792
```

L'API de liste des membres du grpc-proxy retourne son propre `advertise-client-url` :

```bash
ETCDCTL_API=3 etcdctl --endpoints=http://localhost:23792 member list --write-out table

+----+---------+--------------------------------+------------+-----------------+
| ID | STATUS  |              NAME              | PEER ADDRS |  CLIENT ADDRS   |
+----+---------+--------------------------------+------------+-----------------+
|  0 | started | Gyu-Hos-MBP.sfo.coreos.systems |            | 127.0.0.1:23792 |
+----+---------+--------------------------------+------------+-----------------+
```

## Espace de noms {#namespacing}

Supposons qu'une application exige un contrôle total sur l'ensemble de l'espace de clés, mais que le cluster etcd soit partagé avec d'autres applications. Pour permettre à toutes les applications de fonctionner sans se perturber mutuellement, le proxy peut partitionner l'espace de clés etcd de manière à ce que les clients perçoivent un accès à l'espace de clés complet. Lorsque le proxy reçoit le drapeau `--namespace`, toutes les requêtes clientes entrant dans le proxy sont traduites afin d'ajouter un préfixe défini par l'utilisateur aux clés. Les accès au cluster etcd se font sous ce préfixe, et les réponses du proxy suppriment ce préfixe ; pour le client, il semble qu'aucun préfixe n'existe.

Pour attribuer un espace de noms à un proxy, lancez-le avec `--namespace` :

```bash
$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23790 \
  --namespace=my-prefix/
```

Les accès au proxy sont désormais transparentement préfixés sur le cluster etcd :

```bash
$ ETCDCTL_API=3 etcdctl --endpoints=localhost:23790 put my-key abc
# OK
$ ETCDCTL_API=3 etcdctl --endpoints=localhost:23790 get my-key
# my-key
# abc
$ ETCDCTL_API=3 etcdctl --endpoints=localhost:2379 get my-prefix/my-key
# my-prefix/my-key
# abc
```

## Terminaison TLS {#tls-termination}

Utilisez le proxy gRPC pour terminer les connexions TLS à un cluster etcd sécurisé et exposer un point d’accès local non chiffré.

Pour le tester, démarrez un cluster etcd à membre unique avec un client HTTPS :

```sh
$ etcd --listen-client-urls https://localhost:2379 --advertise-client-urls https://localhost:2379 --cert-file=peer.crt --key-file=peer.key --trusted-ca-file=ca.crt --client-cert-auth
```

Vérifiez que le port client est configuré pour servir HTTPS :

```sh
# fails
$ ETCDCTL_API=3 etcdctl --endpoints=http://localhost:2379 endpoint status
# works
$ ETCDCTL_API=3 etcdctl --endpoints=https://localhost:2379 --cert=client.crt --key=client.key --cacert=ca.crt endpoint status
```

Ensuite, démarrez un proxy gRPC sur `localhost:12379` en vous connectant au point de terminaison etcd `https://localhost:2379` à l'aide des certificats clients :

```sh
$ etcd grpc-proxy start --endpoints=https://localhost:2379 --listen-addr localhost:12379 --cert client.crt --key client.key --cacert=ca.crt --insecure-skip-tls-verify &
```

Enfin, testez la terminaison TLS en insérant une clé dans le proxy via http :

```sh
$ ETCDCTL_API=3 etcdctl --endpoints=http://localhost:12379 put abc def
# OK
```

## Métriques et état de santé {#metrics-and-health}

Le proxy gRPC expose les points de terminaison `/health` et Prometheus `/metrics` pour les membres etcd définis par `--endpoints`. Une alternative consiste à définir une URL supplémentaire qui répondra à la fois aux points de terminaison `/metrics` et `/health` avec le drapeau `--metrics-addr`.

```bash
$ etcd grpc-proxy start \
  --endpoints https://localhost:2379 \
  --metrics-addr https://0.0.0.0:4443 \
  --listen-addr 127.0.0.1:23790 \
  --key client.key \
  --key-file proxy-server.key \
  --cert client.crt \
  --cert-file proxy-server.crt \
  --cacert ca.pem \
  --trusted-ca-file proxy-ca.pem
 ```

### Problème connu {#known-issue}

L'interface principale du proxy sert à la fois HTTP2 et HTTP/1.1. Si le proxy est configuré avec TLS comme indiqué dans l'exemple ci-dessus, l'utilisation d'un client tel que cURL contre l'interface d'écoute nécessite de définir explicitement le protocole à HTTP/1.1 dans la requête afin de retourner `/metrics` ou `/health`. En utilisant le drapeau `--metrics-addr`, l'interface secondaire n'aura pas cette exigence.

```bash
 $ curl --cacert proxy-ca.pem --key proxy-client.key --cert proxy-client.crt https://127.0.0.1:23790/metrics --http1.1
```
