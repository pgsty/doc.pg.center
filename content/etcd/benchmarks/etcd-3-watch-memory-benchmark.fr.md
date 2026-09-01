---
title: "Benchmark de l'utilisation mémoire de la surveillance"
weight: 5250
description: Mesures de performance pour les observateurs etcd
categories: [Référence]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/benchmarks/etcd-3-watch-memory-benchmark.md"
---

> [!NOTE]
> Les fonctionnalités de surveillance sont en développement actif, et leur utilisation mémoire peut évoluer au cours de ce développement. Nous ne prévoyons pas d'augmentation significative au-delà des valeurs indiquées ci-dessous.

Un objectif principal d’etcd est de prendre en charge un très grand nombre d’observateurs effectuant une surveillance massivement étendue. etcd vise à supporter O(10k) clients, O(100K) flux de surveillance (O(10) flux par client) et O(10M) surveillance totale (O(100) surveillance par flux). La mémoire consommée par chaque surveillance individuelle représente la plus grande partie de l’utilisation globale d’etcd, et constitue donc le point focal des optimisations actuelles et futures.


Trois composants liés de la surveillance etcd consomment de la mémoire physique : chaque `grpc.Conn`, chaque flux de surveillance et chaque instance d'activité de surveillance. `grpc.Conn` maintient la connexion TCP réelle et l'état de connexion gRPC associé. Chaque `grpc.Conn` consomme environ 10 ko de mémoire, et peut avoir plusieurs flux de surveillance attachés.

Chaque flux de surveillance est une connexion HTTP2 indépendante qui consomme une autre quantité de mémoire O(10 ko).
Plusieurs surveillance peuvent partager un même flux de surveillance.

La surveillance est la structure réelle qui suit les modifications apportées au magasin clé-valeur. Chaque surveillance ne doit consommer que < 1 Ko.

```
                                          +-------+
                                          | watch |
                              +---------> | foo   |
                              |           +-------+
                       +------+-----+
                       |   stream   |
      +--------------> |            |
      |                +------+-----+     +-------+
      |                       |           | watch |
      |                       +---------> | bar   |
+-----+------+                            +-------+
|            |         +------------+
|   conn     +-------> |   stream   |
|            |         |            |
+-----+------+         +------------+
      |
      |
      |
      |                +------------+
      +--------------> |   stream   |
                       |            |
                       +------------+
```

La consommation mémoire théorique de la surveillance peut être approximée par la formule suivante :
`memory = c1 * number_of_conn + c2 * avg_number_of_stream_per_conn + c3 * avg_number_of_watch_stream`

## Environnement de test {#testing-environment}

Version etcd
- git head https://github.com/etcd-io/etcd/commit/185097ffaa627b909007e772c175e8fefac17af3

Type de machine GCE n1-standard-2
- 7,5 Go de mémoire
- 2x processeurs

## Utilisation mémoire globale {#overall-memory-usage}

La consommation mémoire globale indique la quantité de [RSS][rss] consommée par etcd, incluant les observateurs clients. Bien que le résultat puisse varier jusqu’à 10 %, il reste significatif, car l’objectif est de comprendre l’usage mémoire approximatif et le schéma d’allocation.

À partir des résultats du benchmark, nous pouvons estimer approximativement que `c1 = 17kb`, `c2 = 18kb` et `c3 = 350bytes`. Ainsi, chaque connexion cliente supplémentaire consomme 17 ko de mémoire, chaque flux supplémentaire consomme 18 ko de mémoire, et chaque surveillance supplémentaire n'entraîne qu'une augmentation de 350 octets. Un serveur etcd unique peut maintenir des millions de surveillance avec quelques gigaoctets de mémoire dans un cas normal.


| clients | flux par client | surveillance par flux | surveillance totale | utilisation mémoire |
|---------|------------------|------------------------|------------------------|----------------------|
| 1k |  1 |   1 |   1k |   50Mo |
| 2k |  1 |   1 |   2k |   90Mo |
| 5k |  1 |   1 |   5k |  200Mo |
| 1k | 10 |   1 |  10k |  217Mo |
| 2k | 10 |   1 |  20k |  417Mo |
| 5k | 10 |   1 |  50k |  980Mo |
| 1k | 50 |   1 |  50k | 1001Mo |
| 2k | 50 |   1 | 100k | 1960Mo |
| 5k | 50 |   1 | 250k | 4700Mo |
| 1k | 50 |  10 | 500k | 1171Mo |
| 2k | 50 |  10 |   1M | 2371Mo |
| 5k | 50 |  10 | 2.5M | 5710Mo |
| 1k | 50 | 100 |   5M | 2380Mo |
| 2k | 50 | 100 |  10M | 4672Mo |
| 5k | 50 | 100 |  25M |  *OOM* |

[rss]: https://en.wikipedia.org/wiki/Resident_set_size
