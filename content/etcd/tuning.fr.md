---
title: Optimisation
weight: 1450
description: "Quand mettre à jour les paramètres d'intervalle de battement et de délai d'élection"
icon: fa-solid fa-sliders
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tuning.md"
---

Les paramètres par défaut d’etcd devraient fonctionner correctement pour les installations sur un réseau local où la latence réseau moyenne est faible. Toutefois, lors de l’utilisation d’etcd sur plusieurs centres de données ou sur des réseaux à forte latence, il se peut que les paramètres d’intervalle de battement et de délai d’élection nécessitent une adaptation.

Le réseau n’est pas la seule source de latence. Chaque requête et réponse peut être affectée par des disques lents sur le leader et le suiveur. Chacun de ces délais d’attente représente le temps total écoulé entre la requête et la réponse réussie de l’autre machine.

## Paramètres de temps {#time-parameters}

Le protocole de consensus distribué sous-jacent repose sur deux paramètres temporels distincts pour garantir qu’un nœud peut transférer la direction si un autre stagne ou devient hors ligne. Le premier paramètre s’appelle l’*Intervalle de battement*. Il correspond à la fréquence à laquelle le leader informe les suiveurs qu’il est toujours en fonction.
Pour les bonnes pratiques, ce paramètre devrait être réglé autour du temps de trajet aller-retour entre les membres. Par défaut, etcd utilise un intervalle de battement de `100ms`.

Le deuxième paramètre est le *Délai d'élection*. Ce délai indique combien de temps un suiveur attend sans recevoir de battement de cœur avant de tenter de devenir leader lui-même. Par défaut, etcd utilise un délai d'élection `1000ms`.

Ajuster ces valeurs constitue un compromis. La valeur de l'intervalle de battement devrait être d'environ le maximum du temps de trajet moyen (RTT) entre les membres, généralement comprise entre 0,5 et 1,5 fois le temps de trajet. Si l'intervalle de battement est trop faible, etcd enverra des messages inutiles, ce qui augmente la consommation de ressources CPU et réseau. À l'inverse, un intervalle de battement trop élevé entraîne un délai d'élection élevé. Un délai d'élection plus élevé prolonge le temps nécessaire à la détection d'une panne du leader. La méthode la plus simple pour mesurer le temps de trajet (RTT) consiste à utiliser l'utilitaire [PING][ping].

Le délai d'élection devrait être réglé en fonction de l'intervalle de battement et du temps de trajet moyen entre les membres. Les délais d'élection doivent être au moins dix fois supérieurs au temps de trajet pour tenir compte des variations du réseau. Par exemple, si le temps de trajet entre les membres est de 10 ms, le délai d'élection doit être d'au moins 100 ms.

La limite supérieure du délai d'élection est de 50000 ms (50 s), qui ne doit être utilisée qu'en cas de déploiement d'un cluster etcd distribué à l'échelle mondiale. Un délai de trajet aller-retour raisonnable pour les États-Unis continentaux est de 130 ms, et le délai entre les États-Unis et le Japon est d'environ 350 à 400 ms. Si le réseau présente des performances inégales ou des retards/pertes réguliers de paquets, il se peut qu'une ou deux tentatives soient nécessaires pour envoyer correctement un paquet. Ainsi, 5 s constitue une limite supérieure raisonnable pour le délai de trajet global. Étant donné que le délai d'élection doit être d'un ordre de grandeur supérieur au délai de diffusion, dans le cas d'un cluster réparti à l'échelle mondiale avec un délai d'environ 5 s, une durée maximale de 50 secondes devient raisonnable.

L'intervalle de battement et la durée d'élection devraient être identiques pour tous les membres d'un cluster. Définir des valeurs différentes pour les membres etcd peut perturber la stabilité du cluster.

Les valeurs par défaut peuvent être remplacées en ligne de commande :

```sh
# Command line arguments:
$ etcd --heartbeat-interval=100 --election-timeout=500

# Environment variables:
$ ETCD_HEARTBEAT_INTERVAL=100 ETCD_ELECTION_TIMEOUT=500 etcd
```

Les valeurs sont indiquées en millisecondes.

## Instantanés {#snapshots}

etcd ajoute toutes les modifications de clés à un fichier journal. Ce journal s'étend indéfiniment et constitue un historique linéaire complet de chaque modification apportée aux clés. Un historique complet fonctionne bien pour les clusters peu utilisés, mais les clusters fortement utilisés se retrouvent avec un journal volumineux.

Pour éviter d'avoir un journal très volumineux, etcd effectue des instantanés périodiques. Ces instantanés permettent à etcd de compacter le journal en enregistrant l'état actuel du système et en supprimant les anciens journaux.

### Optimisation des instantanés {#snapshot-tuning}

Les instantanés Raft sont créés après un nombre configuré d’entrées appliquées ; etcd 3.7 n’utilise plus le backend V2. Par défaut, un instantané est effectué toutes les 10 000 modifications. Si l’utilisation mémoire et disque d’etcd est trop élevée, essayez de réduire le seuil d’instantané en définissant la commande suivante en ligne de commande :

```sh
# Command line arguments:
$ etcd --snapshot-count=5000

# Environment variables:
$ ETCD_SNAPSHOT_COUNT=5000 etcd
```

## Disque {#disk}

Un cluster etcd est très sensible aux latences disque. Étant donné qu'etcd doit persister les propositions dans son journal, l'activité disque provoquée par d'autres processus peut entraîner de longues latences `fsync`. En conséquence, etcd peut manquer des battements, provoquant des délais d'attente des requêtes et une perte temporaire du leader. Un serveur etcd peut parfois fonctionner de manière stable aux côtés de ces processus lorsqu'il bénéficie d'une priorité disque élevée.

Sur Linux, la priorité du disque d'etcd peut être configurée avec `ionice` :

```sh
# best effort, highest priority
$ sudo ionice -c2 -n0 -p `pgrep etcd`
```

## Réseau {#network}

Si le leader etcd traite un grand nombre de requêtes clientes concurrentes, il peut retarder le traitement des requêtes de pair suiveur en raison de la congestion du réseau. Cela se manifeste par des messages d'erreur de tampon d'envoi sur les nœuds suiveurs :

```
dropped MsgProp to 247ae21ff9436b2d since streamMsg's sending buffer is full
dropped MsgAppResp to 247ae21ff9436b2d since streamMsg's sending buffer is full
```

Ces erreurs peuvent être résolues en priorisant le trafic pair d'etcd par rapport au trafic client. Sur Linux, le trafic pair peut être priorisé en utilisant le mécanisme de contrôle du trafic :

```
tc qdisc add dev eth0 root handle 1: prio bands 3
tc filter add dev eth0 parent 1: protocol ip prio 1 u32 match ip sport 2380 0xffff flowid 1:1
tc filter add dev eth0 parent 1: protocol ip prio 1 u32 match ip dport 2380 0xffff flowid 1:1
tc filter add dev eth0 parent 1: protocol ip prio 2 u32 match ip sport 2379 0xffff flowid 1:1
tc filter add dev eth0 parent 1: protocol ip prio 2 u32 match ip dport 2379 0xffff flowid 1:1
```

[ping]: https://en.wikipedia.org/wiki/Ping_(networking_utility)


Pour annuler `tc`, exécutez :

```
tc qdisc del dev eth0 root
```

## CPU {#cpu}

Comme etcd est très sensible à la latence, les performances peuvent être optimisées davantage sur les systèmes Linux en définissant le gouverneur CPU sur le mode `performance` ou `conservative`.

Sous Linux, le gouverneur du processeur peut être configuré en mode performance :
```
echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```
