---
title: Corruption des données
weight: 5000
description: etcd corruption des données et récupération
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/op-guide/data_corruption.md"
---

etcd dispose d'une détection automatique des corruption de données intégrée afin d'éviter que l'état du membre ne diverge.

## Activation détection corruption données {#enabling-data-corruption-detection}

Détection de corruption de données possible à l'aide de :
* Vérification initiale, activée avec le drapeau `--experimental-initial-corrupt-check`.
* Vérification périodique de :
  * Hachage de la révision compactée, activée avec le drapeau `--experimental-compact-hash-check-enabled`.
  * Hachage de la dernière révision, activée avec le drapeau `--experimental-corrupt-check-time`.

La vérification initiale sera exécutée lors du démarrage du membre etcd.
Le membre comparera son état persistant avec celui des autres membres et quittera l'exécution s'il détecte une incohérence.

Les deux vérifications périodiques seront exécutées par le leader du cluster dans un cluster déjà en cours d'exécution.
Le leader comparera son état persistant aux autres membres et déclenchera une alarme CORRUPT en cas de désaccord.
Les deux vérifications ont le même objectif, mais il est recommandé de les activer toutes les deux afin d'équilibrer performance et temps de détection.
* Vérification de hachage de la révision compactée – nécessite une compactage régulière, coût minimal sur la performance, gère les suiveurs lents.
* Vérification de hachage de la dernière révision – coût élevé sur la performance, ne gère pas les suiveurs lents ni les compactages fréquents.

### Vérification du hachage de révision compactée {#compacted-revision-hash-check}

Lorsqu’il est activé à l’aide du drapeau `--experimental-compact-hash-check-enabled`, la vérification est exécutée toutes les minutes.
Cette fréquence peut être ajustée à l’aide du drapeau `--experimental-compact-hash-check-time` selon le format suivant : `1m` - toutes les minutes, `1h` - toutes les heures.
Cette vérification étend le compactage afin d’effectuer également le calcul d’un checksum pouvant être comparé entre les membres du cluster.
Elle ne provoque pas de balayage supplémentaire de la base de données, ce qui la rend très peu coûteuse, mais nécessite un compactage régulier dans le cluster.

### Vérification du hachage de la dernière révision {#latest-revision-hash-check}

Activé à l'aide du drapeau `--experimental-corrupt-check-time`, nécessite de préciser une période d'exécution au format : `1m` - toutes les minutes, `1h` - toutes les heures.
La période recommandée est de quelques heures en raison du coût élevé en performance.
L'exécution d'un contrôle nécessite le calcul d'un somme de contrôle en analysant l'intégralité du contenu etcd à la révision indiquée.

## Restauration d’un membre corrompu {#restoring-a-corrupted-member}

Il existe trois façons de restaurer un membre corrompu :
* Purger l’état persistant du membre
* Remplacer le membre
* Restaurer tout le cluster

Une fois que le membre corrompu est restauré, l'alarme CORRUPT peut être supprimée.

### Purger l'état persistant d'un membre {#purge-member-persistent-state}

L'état des membres peut être supprimé en procédant comme suit :
1. Arrêt de l'instance etcd.
2. Sauvegarde du répertoire de données etcd.
3. Déplacement du sous-répertoire `snap` depuis le répertoire de données etcd.
6. Démarrage de `etcd` avec `--initial-cluster-state=existing` et la liste des membres du cluster indiquée dans `--initial-cluster`.

Le membre etcd est censé télécharger un instantané à jour depuis le leader.

### Remplacer le membre {#replace-member}

Un membre peut être remplacé par :
1. Arrêt de l'instance etcd.
2. Sauvegarde du répertoire de données etcd.
3. Suppression du répertoire de données.
4. Suppression du membre du cluster en exécutant `etcdctl member remove`.
5. Ajout du membre à nouveau en exécutant `etcdctl member add`.
6. Démarrage de `etcd` avec `--initial-cluster-state=existing` et la liste des membres du cluster indiquée dans `--initial-cluster`.

### Restaurer l'intégralité du cluster {#restore-whole-cluster}

Un cluster peut être restauré en sauvegardant un instantané depuis le leader actuel et en le restorant sur tous les membres.
Exécutez `etcdctl snapshot save` contre le leader et suivez [procédure de restauration d'un cluster](/fr/etcd/op-guide/recovery/).
