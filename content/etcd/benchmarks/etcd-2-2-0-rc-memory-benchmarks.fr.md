---
title: Benchmarking etcd v2.2.0-rc-memory
weight: 5500
description: Mesures de performance pour etcd v2.2.0-rc-memory
categories: [Référence]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/benchmarks/etcd-2-2-0-rc-memory-benchmarks.md"
---

## Machine physique {#physical-machine}

Type de machine GCE n1-standard-2

- 1 disque SSD local dédié monté sous /var/lib/etcd
- 1 disque lent dédié pour le système d'exploitation
- 7,5 Go de mémoire
- 2 processeurs

## etcd {#etcd}

```
etcd Version: 2.2.0-rc.0+git
Git SHA: 103cb5c
Go Version: go1.5
Go OS/Arch: linux/amd64
```

## Test {#testing}

Démarrez un cluster etcd composé de 3 membres, chacun utilisant 2 cœurs.

La longueur du nom de clé est toujours de 64 octets, ce qui constitue une longueur raisonnable pour une clé moyenne.

## Utilisation maximale mémoire {#memory-maximal-usage}

-  etcd peut utiliser une mémoire maximale si un suiveur est défaillant et que le leader continue d'envoyer des instantanés.
- `max RSS` est la consommation mémoire maximale enregistrée sur 3 exécutions.

| taille de la valeur (octets) | nombre de clés | taille des données (Mo) | RSS maximal (Mo) | taux maximal RSS/données sur le leader |
|-------------------------|-----------------|-------------------|------------------|----------------------------------------|
| 128                     | 50000           | 6                 | 433              | 72x                                    |
| 128                     | 100000          | 12                | 659              | 54x                                    |
| 128                     | 200000          | 24                | 1466             | 61x                                    |
| 1024                    | 50000           | 48                | 1253             | 26x                                    |
| 1024                    | 100000          | 96                | 2344             | 24x                                    |
| 1024                    | 200000          | 192               | 4361             | 22x                                    |

## Seuil de taille des données {#data-size-threshold}

- Lorsque etcd atteint le seuil de taille des données, il peut déclencher facilement une élection de leader et rejeter une partie des propositions.
- Dans la plupart des cas, le cluster etcd devrait fonctionner correctement s'il ne dépasse pas ce seuil. Si le fonctionnement est dégradé en raison de ressources insuffisantes, réduisez la taille des données.

| taille de la valeur (octets) | limitation sur le nombre de clés | seuil de taille de données suggéré (Mo) | mémoire RSS consommée (Mo) |
|-------------------|----------------------|-----------------------------------|------------------|
| 128               | 400K                 | 48                                | 2400             |
| 1024              | 300K                 | 292                               | 6500             |
