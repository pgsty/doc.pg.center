---
title: "Benchmarking d'etcd v3"
weight: 5375
description: Mesures de performance pour etcd v3
categories: [Référence]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/benchmarks/etcd-3-demo-benchmarks.md"
---

## Machines physiques {#physical-machines}

Type de machine GCE n1-highcpu-2

- 1 disque SSD local dédié monté sous /var/lib/etcd
- 1 disque lent dédié pour le système d'exploitation
- 1,8 Go de mémoire
- 2 processeurs
- version etcd 2.2.0

## etcd cluster {#etcd-cluster}

1 membre etcd en mode démonstration v3

## Test {#testing}

Utilisez l'outil de benchmark [etcd v3][etcd-v3-benchmark].

## Performances {#performance}

### lecture d'une seule clé {#reading-one-single-key}

| taille de la clé en octets | nombre de clients | QPS de lecture | latence au 90e percentile (ms) |
|-----------------------------|-------------------|----------------|-------------------------------|
| 256                         | 1                 | 2716           | 0,4                           |
| 256                         | 64                | 16623          | 6,1                           |
| 256                         | 256               | 16622          | 21,7                          |

Les performances sont presque identiques à celles obtenues avec un gestionnaire de serveur vide.

### lecture d'une seule clé après un put {#reading-one-single-key-after-putting}

| taille de la clé en octets | nombre de clients | QPS de lecture | latence au 90e percentile (ms) |
|-----------------------------|-------------------|----------------|-------------------------------|
| 256                         | 1                 | 2269           | 0,5                           |
| 256                         | 64                | 13582          | 8,6                           |
| 256                         | 256               | 13262          | 47,5                          |

La performance avec un gestionnaire de serveur vide n'est pas affectée par une opération put. La dégradation des performances devrait donc être causée par le package de stockage.

[etcd-v3-benchmark]: https://github.com/etcd-io/etcd/tree/main/tools/benchmark
