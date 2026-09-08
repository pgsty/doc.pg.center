---
title: Métriques
weight: 1350
description: Métriques pour la surveillance en temps réel et le débogage
icon: fa-solid fa-chart-line
categories: [Référence]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/metrics/_index.md"
aliases: [/etcd/metrics/]
---

etcd utilise [Prometheus][prometheus] pour le reporting des métriques. Ces métriques peuvent être utilisées pour la surveillance en temps réel et le débogage. etcd ne persiste pas ses métriques ; si un membre est redémarré, les métriques seront réinitialisées.

La manière la plus simple de consulter les métriques disponibles consiste à utiliser cURL sur le point de terminaison des métriques `/metrics`. Le format est décrit [dans la documentation Prometheus](http://prometheus.io/docs/instrumenting/exposition_formats/).

Suivez le [document de démarrage rapide de Prometheus][prometheus-getting-started] pour mettre en place un serveur Prometheus afin de collecter les métriques etcd.

Le nommage des métriques suit les bonnes pratiques [Prometheus][prometheus-naming] recommandées. Un nom de métrique porte un préfixe `etcd` ou `etcd_debugging` en tant qu'espace de noms, ainsi qu'un préfixe de sous-système (par exemple `wal` et `etcdserver`).

## etcd espace de noms métriques {#etcd-namespace-metrics}

Les métriques sous le préfixe `etcd` sont destinées à la surveillance et à l'alerte. Il s'agit de métriques stables de haut niveau. Tout changement apporté à ces métriques sera mentionné dans les notes de version.

Les métriques liées à etcd2 sont documentées dans le [guide des métriques v2][v2-http-metrics].

### Serveur {#server}

Ces métriques décrivent l’état du serveur etcd. Pour détecter les interruptions ou les problèmes en vue du dépannage, les métriques du serveur de chaque cluster etcd en production doivent être surveillées de près.

Toutes ces métriques sont préfixées par `etcd_server_`

| Nom                       | Description                                              | Type    |
|---------------------------|----------------------------------------------------------|---------|
| has_leader                | Indique si un leader existe. 1 signifie qu'il existe, 0 qu'il n'existe pas. | Gauge   |
| leader_changes_seen_total | Nombre de changements de leader observés.               | Counter |
| proposals_committed_total | Nombre total de propositions de consensus validées.       | Gauge   |
| proposals_applied_total   | Nombre total de propositions de consensus appliquées.     | Gauge   |
| proposals_pending         | Nombre actuel de propositions en attente.                 | Gauge   |
| proposals_failed_total    | Nombre total de propositions défaillantes observées.       | Counter |

`has_leader` indique si le membre dispose d'un leader. Si un membre ne dispose pas de leader, il est entièrement indisponible. Si aucun membre du cluster ne dispose de leader, l'ensemble du cluster est entièrement indisponible.

`leader_changes_seen_total` compte le nombre de changements de leader observés par le membre depuis son démarrage. Un nombre élevé de changements de leader affecte fortement les performances d'etcd. Cela indique également qu'un leader est instable, probablement à cause de problèmes de connectivité réseau ou d'une charge excessive sur le cluster etcd.

`proposals_committed_total` enregistre le nombre total de propositions de consensus validées. Ce compteur doit augmenter au fil du temps si le cluster est sain. Plusieurs membres sains d'un cluster etcd peuvent avoir un nombre différent de propositions validées à un instant donné. Cette différence peut être due à une récupération après le démarrage, à un retard par rapport au leader, ou au fait d'être le leader et donc d'avoir le plus grand nombre de validations. Il est important de surveiller cette métrique sur tous les membres du cluster ; un retard important et persistant entre un membre et son leader indique que ce membre est lent ou défaillant.

`proposals_applied_total` enregistre le nombre total de propositions de consensus appliquées. Le serveur etcd applique chaque proposition validée de manière asynchrone. La différence entre `proposals_committed_total` et `proposals_applied_total` devrait généralement être faible (de quelques milliers, même sous charge élevée). Si cette différence continue de croître, cela indique que le serveur etcd est surchargé. Cela peut se produire lors de l'application de requêtes coûteuses, comme des requêtes de plage importantes ou des opérations de transaction volumineuses.

`proposals_pending` indique le nombre de propositions en attente de validation. Une augmentation du nombre de propositions en attente suggère une charge élevée des clients ou un membre incapable de valider les propositions.

`proposals_failed_total` sont généralement liés à deux problèmes : des défaillances temporaires liées à une élection du leader ou une interruption prolongée causée par la perte du quorum dans le cluster.

### Disque {#disk}

Ces métriques décrivent l'état des opérations sur le disque.

Toutes ces métriques sont préfixées par `etcd_disk_`.

| Nom                                | Description                                           | Type      |
|------------------------------------|-------------------------------------------------------|-----------|
| wal_fsync_duration_seconds         | Les distributions de latence de fsync appelées par le WAL | Histogramme |
| backend_commit_duration_seconds    | Les distributions de latence de commit appelées par le backend | Histogramme |

Un `wal_fsync` est appelé lorsque etcd persiste ses entrées de journal sur le disque avant de les appliquer.

Un `backend_commit` est appelé lorsque etcd effectue le commit d'un instantané incrémentiel de ses modifications les plus récentes sur le disque.

Des latences élevées des opérations sur le disque (`wal_fsync_duration_seconds` ou `backend_commit_duration_seconds`) indiquent souvent des problèmes de disque. Cela peut entraîner une latence élevée des requêtes ou rendre le cluster instable.

### Réseau {#network}

Ces métriques décrivent l'état du réseau.

Toutes ces métriques sont préfixées par `etcd_network_`

| Nom                             | Description                                                        | Type          |
|----------------------------------|--------------------------------------------------------------------|---------------|
| peer_sent_bytes_total            | Nombre total d'octets envoyés au pair dont l'ID est `To`.           | Compteur(À)   |
| peer_received_bytes_total        | Nombre total d'octets reçus du pair dont l'ID est `From`.   | Compteur(De)  |
| peer_sent_failures_total         | Nombre total d'échecs d'envoi provenant du pair dont l'ID est `To`.      | Compteur(À)   |
| peer_received_failures_total     | Nombre total d'échecs de réception provenant du pair dont l'ID est `From`. | Compteur(De)  |
| peer_round_trip_time_seconds     | Histogramme du temps de trajet aller-retour entre pairs.                           | Histogramme(À) |
| client_grpc_sent_bytes_total     | Nombre total d'octets envoyés aux clients gRPC.                    | Compteur       |
| client_grpc_received_bytes_total | Nombre total d'octets reçus par les clients gRPC.                | Compteur       |

`peer_sent_bytes_total` compte le nombre total d'octets envoyés à un pair spécifique. En général, le membre leader envoie plus de données que les autres membres, car il est chargé de transmettre les données répliquées.

`peer_received_bytes_total` compte le nombre total d'octets reçus d'un pair spécifique. En général, les membres suiveurs reçoivent des données uniquement du membre leader.

### Requêtes gRPC {#grpc-requests}

Ces métriques sont exposées via [go-grpc-prometheus][go-grpc-prometheus].

## métriques de débogage de l'espace de noms etcd {#etcd_debugging-namespace-metrics}

Les métriques sous le préfixe `etcd_debugging` sont destinées au débogage. Elles sont très dépendantes de l'implémentation et instables. Elles pourraient être modifiées ou supprimées sans avertissement dans de nouvelles versions d'etcd. Certaines de ces métriques pourraient être déplacées vers le préfixe `etcd` lorsqu'elles deviendront plus stables.

### instantané {#snapshot}

| Nom                                        | Description                                                | Type      |
|--------------------------------------------|------------------------------------------------------------|-----------|
| snapshot_save_total_duration_seconds       | Les distributions de latence totale de l'appel save effectué par snapshot | Histogramme |

Une durée d'instantané anormalement élevée (`snapshot_save_total_duration_seconds`) indique des problèmes de disque et pourrait entraîner une instabilité du cluster.

## Métriques fournies par Prometheus {#prometheus-supplied-metrics}

La bibliothèque cliente Prometheus fournit un certain nombre de métriques dans les espaces de noms `go` et `process`. Quelques-unes sont particulièrement intéressantes.

| Nom                               | Description                                | Type         |
|-----------------------------------|--------------------------------------------|--------------|
| process_open_fds                  | Nombre de descripteurs de fichiers ouverts. | Gauge        |
| process_max_fds                   | Nombre maximal de descripteurs de fichiers ouverts. | Gauge        |

> [!NOTE]
> Les métriques relatives au processus, telles que `process_open_fds` et `process_max_fds`, ne sont pas prises en charge sur les systèmes Darwin (macOS) pour l'instant.

Une utilisation importante des descripteurs de fichiers (`process_open_fds`) (c’est-à-dire proche de la limite de descripteurs de fichiers du processus, `process_max_fds`) indique un problème potentiel d’épuisement des descripteurs de fichiers. Si les descripteurs de fichiers sont épuisés, etcd peut planter car il ne pourra pas créer de nouveaux fichiers WAL.

## Liste générée des métriques {#generated-list-of-metrics}

[go-grpc-prometheus]: https://github.com/grpc-ecosystem/go-grpc-prometheus
[prometheus]: https://prometheus.io/
[prometheus-getting-started]: https://prometheus.io/docs/introduction/getting_started/
[prometheus-naming]: https://prometheus.io/docs/practices/naming/
[v2-http-metrics]: https://etcd.io/docs/v2.3/metrics/#http-requests
