---
title: Mettre en place un cluster local
weight: 3125
description: Configuration de clusters locaux pour les tests et le développement
categories: [Tutoriel]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/dev-guide/local_cluster.md"
aliases: [/etcd/dev-guide/local_cluster/]
---

Pour les déploiements de test et de développement, la méthode la plus rapide et la plus simple consiste à configurer un cluster local. Pour un déploiement en production, reportez-vous à la section [clustering][clustering].

## Cluster autonome local {#local-standalone-cluster}

### Démarrage d’un cluster {#starting-a-cluster}

Exécutez la commande suivante pour déployer un cluster etcd en tant que cluster autonome :

```
$ ./etcd
...
```

Si le binaire `etcd` n'est pas présent dans le répertoire de travail courant, il se peut qu'il se trouve soit à `$GOPATH/bin/etcd`, soit à `/usr/local/bin/etcd`. Exécutez la commande en conséquence.

Le membre etcd en cours d'exécution écoute sur `localhost:2379` pour les requêtes clientes.

### Interaction avec le cluster {#interacting-with-the-cluster}

Utilisez `etcdctl` pour interagir avec le cluster en cours d'exécution :

1. Stockez une paire clé-valeur exemple dans le cluster :

    ```
      $ ./etcdctl put foo bar
      OK
    ```

    Si OK est affiché, la sauvegarde de la paire clé-valeur a réussi.

2. Récupérer la valeur de `foo` :

    ```
    $ ./etcdctl get foo
    bar
    ```

    Si `bar` est retourné, l'interaction avec le cluster etcd fonctionne comme prévu.

## Cluster local à plusieurs membres {#local-multi-member-cluster}

### Démarrage d’un cluster {#starting-a-cluster-1}

Un `Procfile` situé à la racine du dépôt git d'etcd est fourni pour configurer facilement un cluster local à plusieurs membres. Pour démarrer un cluster à plusieurs membres, accédez à la racine de l'arborescence source d'etcd et exécutez les étapes suivantes :

1. Installer `goreman` pour contrôler les applications basées sur Procfile :

    ```
    $ go install github.com/mattn/goreman@latest
    ```

2. Démarrez un cluster avec `goreman` en utilisant le Procfile par défaut d'etcd :

    ```
    $ goreman -f Procfile start
    ```

    Les membres démarrent. Ils écoutent respectivement sur `localhost:2379`, `localhost:22379` et `localhost:32379` les requêtes clientes.

### Interaction avec le cluster {#interacting-with-the-cluster-1}

Utilisez `etcdctl` pour interagir avec le cluster en cours d'exécution :

1. Affichez la liste des membres :

    ```
    $ etcdctl --write-out=table --endpoints=localhost:2379 member list
    ```
    La liste des membres etcd s'affiche comme suit :

    ```
    +------------------+---------+--------+------------------------+------------------------+
    |        ID        | STATUS  |  NAME  |       PEER ADDRS       |      CLIENT ADDRS      |
    +------------------+---------+--------+------------------------+------------------------+
    | 8211f1d0f64f3269 | started | infra1 | http://127.0.0.1:2380  | http://127.0.0.1:2379  |
    | 91bc3c398fb3c146 | started | infra2 | http://127.0.0.1:22380 | http://127.0.0.1:22379 |
    | fd422379fda50e48 | started | infra3 | http://127.0.0.1:32380 | http://127.0.0.1:32379 |
    +------------------+---------+--------+------------------------+------------------------+
    ```

2. Stockez une paire clé-valeur exemple dans le cluster :

    ```
    $ etcdctl put foo bar
    OK
    ```

    Si OK est affiché, la sauvegarde de la paire clé-valeur a réussi.

### Test de tolérance aux pannes {#testing-fault-tolerance}

Pour tester la tolérance aux pannes d'etcd, arrêtez un membre et tentez de récupérer la clé.

1. Identifiez le nom du processus du membre à arrêter.

    Le `Procfile` liste les propriétés du cluster à plusieurs membres. Par exemple, considérez le membre dont le nom de processus est `etcd2`.

2. Arrêtez le membre :

    ```
    # kill etcd2
    $ goreman run stop etcd2
    ```

3. Stockez une clé :

    ```
    $ etcdctl put key hello
    OK
    ```

4.  Récupérez la clé stockée à l'étape précédente :

    ```
    $ etcdctl get key
    hello
    ```

5. Récupérer une clé depuis un membre arrêté :

    ```
    $ etcdctl --endpoints=localhost:22379 get key
    ```

    La commande doit afficher une erreur due à un échec de connexion :

    ```
    2017/06/18 23:07:35 grpc: Conn.resetTransport failed to create client transport: connection error: desc = "transport: dial tcp 127.0.0.1:22379: getsockopt: connection refused"; Reconnecting to "localhost:22379"
    Error:  grpc: timed out trying to connect
    ```
6. Redémarrez le membre arrêté :

    ```
    $ goreman run restart etcd2
    ```

7. Obtenez la clé depuis le membre redémarré :

    ```
    $ etcdctl --endpoints=localhost:22379 get key
    hello
    ```

    Redémarrer le membre rétablit la connexion. `etcdctl` pourra désormais récupérer la clé avec succès. Pour en savoir plus sur l'interaction avec etcd, consultez la section [interaction avec etcd][interacting].

[clustering]: /fr/docs/etcd/op-guide/clustering/
[interacting]: /fr/docs/etcd/dev-guide/interacting_v3/
