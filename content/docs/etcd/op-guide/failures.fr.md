---
title: Modes de défaillance
weight: 4250
description: "Types d'échecs et la tolérance d'etcd à leur égard"
categories: [Concept]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/op-guide/failures.md"
aliases: [/etcd/op-guide/failures/]
---

Les défaillances sont fréquentes dans un déploiement à grande échelle de machines. Une machine défaillante est une machine dont le matériel ou le logiciel présente une anomalie. Plusieurs machines peuvent défaillir simultanément en cas de panne de courant ou de problèmes réseau. Plusieurs types de défaillances peuvent également survenir en même temps ; il est presque impossible d’énumérer toutes les situations de défaillance possibles.

Dans cette section, nous recensons les types d'pannes et discutons de la manière dont etcd est conçu pour y résister. La plupart des utilisateurs, sinon tous, peuvent associer une panne particulière à un type de panne spécifique. Pour se préparer aux rares pannes [irréversibles][unrecoverable], il est toujours [recommandé de sauvegarder][backup] le cluster etcd.

## Échec mineur des suiveurs {#minor-followers-failure}

Lorsque moins de la moitié des suiveurs échouent, le cluster etcd peut continuer à accepter des requêtes et à progresser sans interruption majeure. Par exemple, deux échecs de suiveurs n’affectent pas le fonctionnement d’un cluster etcd à cinq membres. Toutefois, les clients perdent la connectivité avec les membres défaillants. Les bibliothèques clientes doivent masquer ces interruptions aux utilisateurs pour les requêtes en lecture en se reconnectant automatiquement à d’autres membres. Les opérateurs doivent s’attendre à une augmentation de la charge système sur les autres membres en raison des reconnexions.

## Défaillance du leader {#leader-failure}

Lorsqu’un leader échoue, le cluster etcd élit automatiquement un nouveau leader. L’élection n’a pas lieu instantanément après l’échec du leader. Elle prend environ un délai d’élection, car le modèle de détection des échecs repose sur un délai d’attente.

Pendant l'élection du leader, le cluster ne peut pas traiter d'écritures. Les requêtes d'écriture envoyées pendant l'élection sont mises en attente jusqu'à l'élection d'un nouveau leader.

Les écritures déjà envoyées au vieux leader mais non encore validées peuvent être perdues. Le nouveau leader peut réécrire n'importe quelle entrée non validée provenant du leader précédent. Du point de vue de l'utilisateur, certaines requêtes d'écriture peuvent expirer après une nouvelle élection de leader. Toutefois, aucune écriture validée n'est jamais perdue.

Le nouveau leader étend automatiquement les délais de tous les bails. Ce mécanisme garantit qu’un bail ne sera pas expiré avant le TTL accordé, même s’il a été accordé par le leader ancien.

## Défaillance majoritaire {#majority-failure}

Lorsque la majorité des membres du cluster échoue, le cluster etcd échoue et ne peut plus accepter d'écritures.

Le cluster etcd ne peut être mis en récupération qu’après la disponibilité de la majorité des membres. Si la majorité des membres ne peut revenir en ligne, l’opérateur doit alors lancer [la récupération après sinistre][unrecoverable] pour restaurer le cluster.

Dès qu'une majorité des membres fonctionne, le cluster etcd élit automatiquement un nouveau leader et redevient sain. Le nouveau leader étend automatiquement les délais de tous les bails. Ce mécanisme garantit qu’aucun bail n’expire en raison d’une indisponibilité du serveur.

## Partition réseau {#network-partition}

Une partition réseau est similaire à une défaillance mineure d’un suiveur ou à une défaillance du leader. Une partition réseau divise le cluster etcd en deux parties ; l’une dispose d’une majorité de membres, l’autre d’une minorité. Le côté majoritaire devient le cluster disponible, tandis que le côté minoritaire devient indisponible. Il n’y a pas de « split-brain » dans etcd car les membres du cluster sont explicitement added/removed et chaque modification est approuvée par la majorité actuelle des membres.

Si le leader se trouve du côté majoritaire, alors, du point de vue de la majorité, la défaillance correspond à une défaillance d’un suiveur minoritaire. Si le leader se trouve du côté minoritaire, il s’agit d’une défaillance du leader. Le leader du côté minoritaire cède son rôle, et le côté majoritaire élit un nouveau leader.

Une fois que la partition réseau est résolue, le côté minoritaire reconnaît automatiquement le leader provenant du côté majoritaire et restaure son état.

## Échec du démarrage {#failure-during-bootstrapping}

Le démarrage initial d’un cluster réussit uniquement si tous les membres requis démarrent correctement. Si une erreur survient pendant le démarrage initial, supprimez les répertoires de données sur tous les membres, puis redémarrez le cluster avec un nouveau cluster-token ou un nouveau jeton de découverte.

Bien sûr, il est possible de récupérer un cluster initialisé qui a échoué, tout comme on récupère un cluster en cours d'exécution. Toutefois, la récupération de ce cluster prend presque toujours plus de temps et de ressources que le démarrage d'un nouveau cluster, car aucune donnée n'a besoin d'être récupérée.

[backup]: /fr/docs/etcd/op-guide/maintenance/#snapshot-backup
[unrecoverable]: /fr/docs/etcd/op-guide/recovery/
