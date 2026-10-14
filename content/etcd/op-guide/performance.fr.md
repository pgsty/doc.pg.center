---
title: Performances
weight: 4550
description: "Comprendre les performances : latence et débit"
categories: [Concept]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/performance.md"
---

## Comprendre les performances {#understanding-performance}

etcd offre des performances stables et élevées de manière soutenue. Deux facteurs définissent les performances : la latence et le débit. La latence correspond au temps nécessaire pour accomplir une opération. Le débit correspond au nombre total d'opérations effectuées durant une période donnée. En général, la latence moyenne augmente lorsque le débit global augmente, lorsque etcd accepte des requêtes clientes concurrentes. Dans des environnements cloud courants, comme une instance standard `n-4` sur Google Compute Engine (GCE) ou un type de machine équivalent sur AWS, un cluster etcd composé de trois membres exécute une requête en moins d'une milliseconde en charge légère, et peut traiter plus de 30 000 requêtes par seconde en charge lourde.

etcd utilise l'algorithme de consensus Raft pour répliquer les requêtes entre les membres et parvenir à un accord. Les performances du consensus, en particulier la latence de validation, sont limitées par deux contraintes physiques : la latence d'E/S réseau et la latence d'E/S disque. Le temps minimal pour finaliser une requête etcd correspond au temps de trajet aller-retour (RTT) réseau entre les membres, plus le temps que `fdatasync` met à valider les données dans un stockage permanent. Le RTT au sein d'un centre de données peut atteindre plusieurs centaines de microsecondes. Un RTT typique aux États-Unis est d'environ 50 ms, et peut s'élever à 400 ms entre les continents. La latence typique de fdatasync pour un disque rotatif est d'environ 10 ms. Pour les SSD, la latence est souvent inférieure à 1 ms. Pour améliorer le débit, etcd regroupe plusieurs requêtes ensemble et les soumet à Raft. Cette politique de regroupement permet à etcd d'atteindre un haut débit même sous une charge importante.

D'autres sous-systèmes influencent les performances globales d'etcd. Chaque requête etcd sérialisée doit passer par le moteur de stockage MVCC basé sur boltdb, ce qui prend généralement quelques dizaines de microsecondes. De manière périodique, etcd effectue un instantané incrémental de ses requêtes récemment appliquées, qu'il fusionne avec l'instantané précédent sur disque. Ce processus peut entraîner une pointe de latence. Bien que cela ne pose généralement pas de problème sur les SSD, cela peut doubler la latence observée sur les disques durs. De même, les compactages en cours peuvent affecter les performances d'etcd. Heureusement, l'impact est souvent négligeable, car le compactage est progressif, évitant ainsi toute concurrence pour les ressources avec les requêtes régulières. Le système RPC, gRPC, fournit à etcd une API bien définie et extensible, mais introduit également une latence supplémentaire, notamment pour les lectures locales.

## Benchmarks {#benchmarks}

Le benchmark de la performance d’etcd peut être effectué à l’aide de l’outil en ligne de commande [benchmark](https://github.com/etcd-io/etcd/tree/main/tools/benchmark) fourni avec etcd.

Pour des mesures de performance de base, nous considérons un cluster etcd composé de trois membres avec la configuration matérielle suivante :

- Google Cloud Compute Engine
- 3 machines de 8 vCPU + 16 Go de mémoire + 50 Go de SSD
- 1 machine (client) de 16 vCPU + 30 Go de mémoire + 50 Go de SSD
- Ubuntu 17.04
- etcd 3.2.0, go 1.8.3

Avec cette configuration, etcd peut écrire approximativement :

| Nombre de clés | Taille de la clé en octets | Taille de la valeur en octets | Nombre de connexions | Nombre de clients | Serveur etcd cible | Débit d'écriture moyen (QPS) | Latence moyenne par requête | RSS moyen du serveur |
|---------------:|------------------:|--------------------:|----------------------:|------------------:|--------------------|------------------:|----------------------------:|-------------------:|
| 10 000 | 8 | 256 | 1 | 1 | leader uniquement | 583 | 1,6 ms | 48 Mo |
| 100 000 | 8 | 256 | 100 | 1 000 | leader uniquement | 44 341 | 22 ms | 124 Mo |
| 100 000 | 8 | 256 | 100 | 1 000 | tous les membres | 50 104 | 20 ms | 126 Mo |

Commandes d'exemple :

```sh
# write to leader
benchmark --endpoints=${HOST_1} --target-leader --conns=1 --clients=1 \
    put --key-size=8 --sequential-keys --total=10000 --val-size=256
benchmark --endpoints=${HOST_1} --target-leader  --conns=100 --clients=1000 \
    put --key-size=8 --sequential-keys --total=100000 --val-size=256

# write to all members
benchmark --endpoints=${HOST_1},${HOST_2},${HOST_3} --conns=100 --clients=1000 \
    put --key-size=8 --sequential-keys --total=100000 --val-size=256
```

Les requêtes de lecture linéarisable passent par un quorum de membres du cluster pour atteindre un consensus afin d’obtenir les données les plus récentes. Les requêtes de lecture sérialisable sont moins coûteuses que les lectures linéarisables, car elles sont servies par n’importe quel membre etcd unique, plutôt que par un quorum de membres, au prix d’une possible lecture de données obsolètes. etcd peut effectuer des lectures :

| Nombre de requêtes | Taille de la clé en octets | Taille de la valeur en octets | Nombre de connexions | Nombre de clients | Cohérence | Débit moyen en lectures (QPS) | Latence moyenne par requête |
|-------------------:|------------------:|--------------------:|----------------------:|------------------:|-------------|-----------------:|----------------------------:|
| 10 000 | 8 | 256 | 1 | 1 | Linéarisable | 1 353 | 0,7 ms |
| 10 000 | 8 | 256 | 1 | 1 | Sérialisable | 2 909 | 0,3 ms |
| 100 000 | 8 | 256 | 100 | 1 000 | Linéarisable | 141 578 | 5,5 ms |
| 100 000 | 8 | 256 | 100 | 1 000 | Sérialisable | 185 758 | 2,2 ms |

Commandes d'exemple :

```sh
# Single connection read requests
benchmark --endpoints=${HOST_1},${HOST_2},${HOST_3} --conns=1 --clients=1 \
    range YOUR_KEY --consistency=l --total=10000
benchmark --endpoints=${HOST_1},${HOST_2},${HOST_3} --conns=1 --clients=1 \
    range YOUR_KEY --consistency=s --total=10000

# Many concurrent read requests
benchmark --endpoints=${HOST_1},${HOST_2},${HOST_3} --conns=100 --clients=1000 \
    range YOUR_KEY --consistency=l --total=100000
benchmark --endpoints=${HOST_1},${HOST_2},${HOST_3} --conns=100 --clients=1000 \
    range YOUR_KEY --consistency=s --total=100000
```

Nous recommandons d'exécuter le test de benchmark lors de la mise en place d'un cluster etcd pour la première fois dans un nouvel environnement afin de vérifier que le cluster atteint des performances adéquates ; la latence du cluster et le débit peuvent être sensibles aux légères différences d'environnement.
