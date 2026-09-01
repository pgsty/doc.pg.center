---
title: "Benchmarking d'etcd v2.2.0"
weight: 5750
description: Mesures de performance pour etcd v2.2.0
categories: [Référence]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/benchmarks/etcd-2-2-0-benchmarks.md"
---

## Machines physiques {#physical-machines}

Type de machine GCE n1-highcpu-2

- 1 disque SSD local dédié monté en répertoire de données etcd
- 1 disque lent dédié pour le système d'exploitation
- 1,8 Go de mémoire
- 2 processeurs

## etcd cluster {#etcd-cluster}

3 membres etcd 2.2.0, chacun exécuté sur une machine unique.

Versions détaillées :

```
etcd Version: 2.2.0
Git SHA: e4561dd
Go Version: go1.5
Go OS/Arch: linux/amd64
```

## Test {#testing}

Initialisez une autre machine, en dehors du cluster etcd, puis exécutez l’outil de benchmark HTTP [`hey` avec un correctif de réutilisation de connexion](https://github.com/rakyll/hey) pour envoyer des requêtes à chaque membre du cluster etcd. Consultez les [instructions de benchmark](https://github.com/etcd-io/etcd/tree/v2.3.8/hack/benchmark) pour obtenir le correctif et les étapes permettant de reproduire nos procédures.

Les performances sont calculées à partir des résultats de 100 itérations de benchmark.

## Performances {#performance}

### Performance de lecture d'une clé unique {#single-key-read-performance}

| taille de la clé en octets | nombre de clients | serveur etcd cible | débit moyen de lecture (QPS) | écart-type du débit de lecture (QPS) | latence moyenne au 90e percentile (ms) | écart-type de la latence |
|-----------------------------|-------------------|--------------------|-------------------------------|------------------------------------|----------------------------------------|--------------------------|
| 64                          | 1                 | seul leader        | 2303                          | 200                                | 0,49                                   | 0,06                     |
| 64                          | 64                | seul leader        | 15048                         | 685                                | 7,60                                   | 0,46                     |
| 64                          | 256               | seul leader        | 14508                         | 434                                | 29,76                                  | 1,05                     |
| 256                         | 1                 | seul leader        | 2162                          | 214                                | 0,52                                   | 0,06                     |
| 256                         | 64                | seul leader        | 14789                         | 792                                | 7,69                                   | 0,48                     |
| 256                         | 256               | seul leader        | 14424                         | 512                                | 29,92                                  | 1,42                     |
| 64                          | 64                | tous les serveurs  | 45752                         | 2048                               | 2,47                                   | 0,14                     |
| 64                          | 256               | tous les serveurs  | 46592                         | 1273                               | 10,14                                  | 0,59                     |
| 256                         | 64                | tous les serveurs  | 45332                         | 1847                               | 2,48                                   | 0,12                     |
| 256                         | 256               | tous les serveurs  | 46485                         | 1340                               | 10,18                                  | 0,74                     |

### Performance d'écriture pour une clé unique {#single-key-write-performance}

| taille de la clé en octets | nombre de clients | serveur etcd cible | débit moyen d'écriture QPS | écart-type du débit d'écriture QPS | latence moyenne au 90e percentile (ms) | écart-type de la latence |
|-----------------------------|-------------------|--------------------|-----------------------------|-------------------------------|----------------------------------------|--------------------------|
| 64 | 1 | leader uniquement | 55 | 4 | 24,51 | 13,26 |
| 64 | 64 | leader uniquement | 2139 | 125 | 35,23 | 3,40 |
| 64 | 256 | leader uniquement | 4581 | 581 | 70,53 | 10,22 |
| 256 | 1 | leader uniquement | 56 | 4 | 22,37 | 4,33 |
| 256 | 64 | leader uniquement | 2052 | 151 | 36,83 | 4,20 |
| 256 | 256 | leader uniquement | 4442 | 560 | 71,59 | 10,03 |
| 64 | 64 | tous les serveurs | 1625 | 85 | 58,51 | 5,14 |
| 64 | 256 | tous les serveurs | 4461 | 298 | 89,47 | 36,48 |
| 256 | 64 | tous les serveurs | 1599 | 94 | 60,11 | 6,43 |
| 256 | 256 | tous les serveurs | 4315 | 193 | 88,98 | 7,01 |

## Améliorations des performances {#performance-changes}

- Comme etcd enregistre désormais des métriques pour chaque appel d'API, la performance en QPS de lecture semble légèrement diminuer dans la plupart des scénarios. Ce léger impact sur les performances a été jugé acceptable en échange de la richesse des informations de surveillance et de débogage fournies.

- Le taux de requêtes d'écriture QPS vers les leaders du cluster semble avoir légèrement augmenté. Cela est dû au fait que la boucle principale et les boucles d'entrée ont été déconnectées dans la logique Raft d'etcd, éliminant plusieurs blocages entre elles.

- Le QPS d'écriture vers tous les membres semble avoir augmenté de manière significative, car les suiveurs reçoivent désormais l'index de validation le plus récent plus rapidement, et traitent les propositions de validation plus rapidement.
