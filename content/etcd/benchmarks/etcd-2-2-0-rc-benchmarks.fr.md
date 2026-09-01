---
title: Benchmarking etcd v2.2.0-rc
weight: 5625
description: Mesures de performance pour etcd v2.2.0-rc
categories: [Référence]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/benchmarks/etcd-2-2-0-rc-benchmarks.md"
---

## Machine physique {#physical-machine}

Type de machine GCE n1-highcpu-2

- 1 disque SSD local dédié monté sous /var/lib/etcd
- 1 disque lent dédié pour le système d'exploitation
- 1,8 Go de mémoire
- 2 processeurs

## etcd cluster {#etcd-cluster}

3 membres etcd 2.2.0-rc, chacun exécuté sur une seule machine.

Versions détaillées :

```
etcd Version: 2.2.0-alpha.1+git
Git SHA: 59a5a7e
Go Version: go1.4.2
Go OS/Arch: linux/amd64
```

En outre, nous utilisons 3 membres etcd 2.1.0 en phase alpha pour constituer le cluster et obtenir des performances de base. La tête du commit d'etcd est située à [c7146bd5][c7146bd5], identique à celle utilisée dans [benchmark etcd 2.1][etcd-2.1-benchmark].

## Test {#testing}

Initialisez une autre machine et utilisez l'outil de benchmark HTTP [hey][hey] pour envoyer des requêtes à chaque membre etcd. Consultez le [guide de manipulation du benchmark][hack-benchmark] pour des instructions détaillées.

## Performances {#performance}

### lecture d'une seule clé {#reading-one-single-key}

| taille de la clé en octets | nombre de clients | serveur etcd cible | débit de lecture (QPS) | latence au 90e percentile (ms) |
|-----------------------------|-------------------|--------------------|------------------------|-------------------------------|
| 64                          | 1                 | seul leader        | 2804 (-5%)   | 0,4 (+0 %)                    |
| 64                          | 64                | seul leader        | 17816 (+0 %)           | 5,7 (-6%)           |
| 64                          | 256               | seul leader        | 18667 (-6%)  | 20,4 (+2 %)                   |
| 256                         | 1                 | seul leader        | 2181 (-15%)   | 0,5 (+25 %)                   |
| 256                         | 64                | seul leader        | 17435 (-7%)  | 6,0 (+9 %)                    |
| 256                         | 256               | seul leader        | 18180 (-8%)  | 21,3 (+3 %)                   |
| 64                          | 64                | tous les serveurs  | 46965 (-4%)  | 2,1 (+0 %)                    |
| 64                          | 256               | tous les serveurs  | 55286 (-6%)  | 7,4 (+6 %)                    |
| 256                         | 64                | tous les serveurs  | 46603 (-6%)  | 2,1 (+5 %)                    |
| 256                         | 256               | tous les serveurs  | 55291 (-6%)  | 7,3 (+4 %)                    |

### écriture d'une seule clé {#writing-one-single-key}

| taille de la clé en octets | nombre de clients | serveur etcd cible | débit d'écriture QPS | latence au 90e percentile (ms) |
|-----------------------------|-------------------|--------------------|------------------------|-------------------------------|
| 64                          | 1                 | seul leader        | 76 (+22%)              | 19,4 (-15%)          |
| 64                          | 64                | seul leader        | 2461 (+45%)            | 31,8 (-32%)          |
| 64                          | 256               | seul leader        | 4275 (+1%)             | 69,6 (-10%)          |
| 256                         | 1                 | seul leader        | 64 (+20%)              | 16,7 (-30%)          |
| 256                         | 64                | seul leader        | 2385 (+30%)            | 31,5 (-19%)          |
| 256                         | 256               | seul leader        | 4353 (-3%)   | 74,0 (+9%)                    |
| 64                          | 64                | tous les serveurs  | 2005 (+81%)            | 49,8 (-55%)          |
| 64                          | 256               | tous les serveurs  | 4868 (+35%)            | 81,5 (-40%)          |
| 256                         | 64                | tous les serveurs  | 1925 (+72%)            | 47,7 (-59%)          |
| 256                         | 256               | tous les serveurs  | 4975 (+36%)            | 70,3 (-36%)          |

### explication des modifications de performance {#performance-changes-explanation}

- Le QPS de lecture est généralement réduit de 5 à 8 % dans la plupart des scénarios. La raison en est que etcd enregistre des métriques pour chaque opération de stockage. Ces métriques sont importantes pour la surveillance et le débogage, ce qui rend cette réduction acceptable.

- Le QPS d'écriture vers le leader augmente de 20 à 30 %. Cela est dû à la déconnexion de la boucle principale Raft et de la boucle d'application des entrées, ce qui empêche leurs blocages mutuels.

- Le débit d'écriture QPS sur tous les serveurs augmente de 30 à 80 % car le suiveur peut recevoir plus tôt l'index de validation le plus récent et valider les propositions plus rapidement.

[c7146bd5]: https://github.com/etcd-io/etcd/commits/c7146bd5f2c73716091262edc638401bb8229144
[etcd-2.1-benchmark]: /fr/etcd/benchmarks/etcd-2-1-0-alpha-benchmarks/
[hack-benchmark]: https://github.com/etcd-io/etcd/tree/v2.3.8/hack/benchmark
[hey]: https://github.com/rakyll/hey
