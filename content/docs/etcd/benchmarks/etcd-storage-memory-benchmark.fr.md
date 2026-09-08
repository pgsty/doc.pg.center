---
title: "Benchmark de l'utilisation de la mémoire de stockage"
weight: 5125
description: Mesures de performance pour le stockage etcd (index en mémoire et cache de pages)
categories: [Référence]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/benchmarks/etcd-storage-memory-benchmark.md"
aliases: [/etcd/benchmarks/etcd-storage-memory-benchmark/]
---

<!---todo: link storage to storage design doc-->
Deux composants du stockage etcd consomment de la mémoire physique. Le processus etcd alloue un *index en mémoire* afin d'accélérer la recherche des clés. La *mémoire tampon de pages*, gérée par le système d'exploitation, stocke les données récemment accessibles sur disque pour une réutilisation rapide.

L'index en mémoire stocke toutes les clés dans une structure de données [arbre B][btree], accompagnées de pointeurs vers les données sur disque (les valeurs). Chaque clé dans l'arbre B peut contenir plusieurs pointeurs, chacun faisant référence à une version différente de sa valeur. La consommation mémoire théorique de l'index en mémoire peut donc être approximée par la formule :

`N * (c1 + avg_key_size) + N * (avg_versions_of_key) * (c2 + size_of_pointer)`

où `c1` représente la surcharge liée aux métadonnées de clé et `c2` la surcharge liée aux métadonnées de version.

Le graphique montre la structure détaillée de l'arbre B en mémoire.

```


                                In mem index

                               +------------+
                               | key || ... |
  +--------------+             |     ||     |
  |              |             +------------+
  |              |             | v1  || ... |
  |   disk    <----------------|     ||     | Tree Node
  |              |             +------------+
  |              |             | v2  || ... |
  |           <----------------+     ||     |
  |              |             +------------+
  +--------------+       +-----+    |   |   |
                         |     |    |   |   |
                         |     +------------+
                         |
                         |
                         ^
                      ------+
                      | ... |
                      |     |
                      +-----+
                      | ... | Tree Node
                      |     |
                      +-----+
                      | ... |
                      |     |
                      ------+
```

La mémoire du cache [Page cache][pagecache] est gérée par le système d'exploitation et n'est pas traitée en détail dans ce document.

## Environnement de test {#testing-environment}

Version etcd
- git head https://github.com/etcd-io/etcd/commit/776e9fb7be7eee5e6b58ab977c8887b4fe4d48db

Type de machine GCE n1-standard-2

- 7,5 Go de mémoire
- 2x processeurs

## Utilisation mémoire de l'index en mémoire {#in-memory-index-memory-usage}

Dans ce test, nous ne mesurons que la consommation mémoire de l'index en mémoire. L'objectif est de déterminer `c1` et `c2` mentionnés ci-dessus, afin de comprendre la limite maximale de consommation mémoire du stockage.

Nous calculons la consommation de mémoire à l’aide de Go runtime.ReadMemStats. Nous déterminons la différence entre le nombre total d’octets alloués avant la création de l’index et après sa création. Cette méthode ne reflète pas parfaitement la consommation de mémoire de l’index en mémoire mais permet toutefois d’observer le profil de consommation approximatif.

| N    | versions | taille de clé | utilisation mémoire |
|------|----------|---------------|---------------------|
| 100K | 1        | 64 octets     | 22 Mo               |
| 100K | 5        | 64 octets     | 39 Mo               |
| 1M   | 1        | 64 octets     | 218 Mo              |
| 1M   | 5        | 64 octets     | 432 Mo              |
| 100K | 1        | 256 octets    | 41 Mo               |
| 100K | 5        | 256 octets    | 65 Mo               |
| 1M   | 1        | 256 octets    | 409 Mo              |
| 1M   | 5        | 256 octets    | 506 Mo              |


En fonction du résultat, nous pouvons calculer `c1=120bytes`, `c2=30bytes`. Nous n'avons besoin que de deux jeux de données pour calculer `c1` et `c2`, car ce sont les seules variables inconnues dans la formule. Les valeurs `c1=120bytes` et `c2=30bytes` correspondent à la moyenne des 4 jeux de `c1` et `c2` que nous avons calculés. La surcharge liée aux métadonnées clés reste encore relativement importante (50 %) pour des paires clé-valeur de petite taille. Toutefois, il s'agit d'une amélioration significative par rapport au vieux magasin, qui présentait au moins une surcharge de 1000 %.

## Utilisation mémoire globale {#overall-memory-usage}

La consommation mémoire globale indique la quantité de mémoire RSS utilisée par etcd, y compris le stockage. La taille des valeurs devrait avoir très peu d'impact sur la consommation mémoire globale d'etcd, car les valeurs sont conservées sur disque et seules les valeurs fréquemment utilisées sont conservées en mémoire, gérées par le cache de pages du système d'exploitation.

| N    | versions | taille clé | taille valeur | utilisation mémoire |
|------|----------|------------|---------------|---------------------|
| 100K | 1        | 64 octets  | 256 octets    | 40 Mo               |
| 100K | 5        | 64 octets  | 256 octets    | 89 Mo               |
| 1M   | 1        | 64 octets  | 256 octets    | 470 Mo              |
| 1M   | 5        | 64 octets  | 256 octets    | 880 Mo              |
| 100K | 1        | 64 octets  | 1 Ko          | 102 Mo              |
| 100K | 5        | 64 octets  | 1 Ko          | 164 Mo              |
| 1M   | 1        | 64 octets  | 1 Ko          | 587 Mo              |
| 1M   | 5        | 64 octets  | 1 Ko          | 836 Mo              |

En fonction des résultats, nous savons que la taille des valeurs n'a pas d'impact significatif sur la consommation mémoire. Une légère augmentation est observée en raison de données supplémentaires conservées dans le cache de page du système d'exploitation.

[btree]: https://en.wikipedia.org/wiki/B-tree
[pagecache]: https://en.wikipedia.org/wiki/Page_cache
