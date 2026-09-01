---
title: "Test de performance d'etcd v2.1.0"
weight: 5875
description: Mesures de performance pour etcd v2.1.0
categories: [Référence]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/benchmarks/etcd-2-1-0-alpha-benchmarks.md"
---

## Machines physiques {#physical-machines}

Type de machine GCE n1-highcpu-2

- 1 disque SSD local dédié monté sous /var/lib/etcd
- 1 disque lent dédié pour le système d'exploitation
- 1,8 Go de mémoire
- 2 processeurs
- version etcd 2.1.0 alpha

## etcd cluster {#etcd-cluster}

3 membres etcd, chacun exécuté sur une machine unique

## Test {#testing}

Initialisez une autre machine et utilisez l'outil de benchmark HTTP [hey][hey] pour envoyer des requêtes à chaque membre etcd. Consultez le [guide de manipulation du benchmark][hack-benchmark] pour des instructions détaillées.

## Performances {#performance}

### lecture d'une seule clé {#reading-one-single-key}

| taille de la clé en octets | nombre de clients | serveur etcd cible | QPS de lecture | Latence au 90e percentile (ms) |
|-----------------------------|-------------------|--------------------|----------------|-------------------------------|
| 64                          | 1                 | seul leader        | 1534           | 0,7                           |
| 64                          | 64                | seul leader        | 10125          | 9,1                           |
| 64                          | 256               | seul leader        | 13892          | 27,1                          |
| 256                         | 1                 | seul leader        | 1530           | 0,8                           |
| 256                         | 64                | seul leader        | 10106          | 10,1                          |
| 256                         | 256               | seul leader        | 14667          | 27,0                          |
| 64                          | 64                | tous les serveurs  | 24200          | 3,9                           |
| 64                          | 256               | tous les serveurs  | 33300          | 11,8                          |
| 256                         | 64                | tous les serveurs  | 24800          | 3,9                           |
| 256                         | 256               | tous les serveurs  | 33000          | 11,5                          |

### écriture d'une seule clé {#writing-one-single-key}

| taille de la clé en octets | nombre de clients | serveur etcd cible | débit d'écriture (QPS) | latence au 90e percentile (ms) |
|-----------------------------|-------------------|--------------------|------------------------|-------------------------------|
| 64                          | 1                 | seul leader        | 60                     | 21,4                          |
| 64                          | 64                | seul leader        | 1 742                  | 46,8                          |
| 64                          | 256               | seul leader        | 3 982                  | 90,5                          |
| 256                         | 1                 | seul leader        | 58                     | 20,3                          |
| 256                         | 64                | seul leader        | 1 770                  | 47,8                          |
| 256                         | 256               | seul leader        | 4 157                  | 105,3                         |
| 64                          | 64                | tous les serveurs  | 1 028                  | 123,4                         |
| 64                          | 256               | tous les serveurs  | 3 260                  | 123,8                         |
| 256                         | 64                | tous les serveurs  | 1 033                  | 121,5                         |
| 256                         | 256               | tous les serveurs  | 3 061                  | 119,3                         |

[hack-benchmark]: https://github.com/etcd-io/etcd/tree/main/hack/benchmark
[hey]: https://github.com/rakyll/hey
