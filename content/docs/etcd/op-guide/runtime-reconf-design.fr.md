---
title: "Conception de la reconfiguration à l'exécution"
weight: 4650
description: "Conception des commandes de reconfiguration en temps d'exécution d'etcd"
categories: [Concept]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/op-guide/runtime-reconf-design.md"
aliases: [/etcd/op-guide/runtime-reconf-design/]
---

La reconfiguration à l’exécution est l’une des fonctionnalités les plus complexes et sujettes aux erreurs dans un système distribué, en particulier dans un système fondé sur le consensus comme etcd.

Lisez la suite pour en savoir plus sur la conception des commandes de reconfiguration en cours d'exécution d'etcd et sur la manière dont nous avons résolu ces problèmes.

## Les modifications de configuration en deux phases maintiennent le cluster en sécurité {#two-phase-config-changes-keep-the-cluster-safe}

Dans etcd, toute reconfiguration en cours d'exécution doit suivre [deux phases][add-member] pour des raisons de sécurité. Par exemple, pour ajouter un membre, il faut d'abord informer le cluster de la nouvelle configuration, puis démarrer le nouveau membre.

Phase 1 - Informer le cluster de la nouvelle configuration

Pour ajouter un membre à un cluster etcd, effectuez un appel d'API afin de demander l'ajout d'un nouveau membre au cluster. C'est la seule méthode permettant d'ajouter un nouveau membre à un cluster existant. L'appel d'API se termine lorsque le cluster a accepté le changement de configuration.

Phase 2 - Démarrer un nouveau membre

Pour rejoindre le nouveau membre etcd au cluster existant, précisez le bon `initial-cluster` et définissez `initial-cluster-state` sur `existing`. Lorsque le membre démarre, il contacte d'abord le cluster existant et vérifie que la configuration actuelle du cluster correspond à celle attendue spécifiée dans `initial-cluster`. Lorsque le nouveau membre démarre correctement, le cluster atteint la configuration attendue.

En divisant le processus en deux phases distinctes, les utilisateurs sont obligés de préciser explicitement les modifications apportées au membre du cluster. Cela accorde en réalité plus de flexibilité aux utilisateurs et simplifie la compréhension du comportement. Par exemple, si une tentative est faite d’ajouter un nouveau membre ayant le même ID qu’un membre existant dans un cluster etcd, l’action échoue immédiatement lors de la première phase, sans affecter le cluster en cours d’exécution. Une protection similaire est mise en place pour empêcher l’ajout accidentel de nouveaux membres. Si un nouveau membre etcd tente de rejoindre le cluster avant que le cluster n’ait accepté le changement de configuration, il ne sera pas accepté par le cluster.

Sans le workflow explicite concernant l’appartenance au cluster, etcd serait vulnérable aux modifications imprévues de l’appartenance au cluster. Par exemple, si etcd est exécuté sous un système d’initialisation tel que systemd, il serait redémarré après avoir été supprimé via l’API d’appartenance, puis tenterait de se réjoindre au cluster au démarrage. Ce cycle se reproduirait chaque fois qu’un membre est supprimé via l’API et que systemd est configuré pour redémarrer etcd après un échec, ce qui est inattendu.

Nous considérons que la reconfiguration à l'exécution doit être une opération rare. Nous avons choisi de la rendre explicite et pilotée par l'utilisateur afin d'assurer la sécurité de la configuration et de maintenir le cluster toujours en fonctionnement sans heurt, sous un contrôle explicite.

## Perte permanente du quorum nécessite un nouveau cluster {#permanent-loss-of-quorum-requires-new-cluster}

Si un cluster perd définitivement la majorité de ses membres, un nouveau cluster devra être lancé à partir d'un répertoire de données ancien afin de restaurer l'état précédent.

Il est tout à fait possible de forcer la suppression des membres défaillants du cluster existant afin de procéder à une récupération. Toutefois, nous avons choisi de ne pas prendre en charge cette méthode, car elle contourne la phase normale de validation du consensus, ce qui est dangereux. Si le membre à supprimer n’est pas réellement défaillant ou n’a pas été supprimé de manière forcée par d’autres membres du même cluster, etcd se retrouvera avec un cluster divergent présentant le même clusterID. Cela constitue un risque très important et difficile à debug/fix par la suite.

Avec un déploiement correct, la probabilité de perte définitive de la majorité est très faible. Mais il s'agit d'un problème suffisamment grave pour mériter une attention particulière. Nous recommandons vivement de lire la documentation de [récupération après sinistre][disaster-recovery] et de préparer une stratégie de récupération face à une perte définitive de la majorité avant de mettre etcd en production.

## N'utilisez pas de service de découverte publique pour la reconfiguration en cours d'exécution {#do-not-use-public-discovery-service-for-runtime-reconfiguration}

Le service de découverte publique ne doit être utilisé que pour amorcer un cluster. Pour ajouter un membre à un cluster existant, utilisez l’API de reconfiguration en temps d’exécution.

Le service de découverte est conçu pour amorcer un cluster etcd dans un environnement cloud, lorsque les adresses IP de tous les membres ne sont pas connues à l’avance. Une fois le cluster amorcé avec succès, les adresses IP de tous les membres sont connues. Techniquement, le service de découverte ne devrait plus être nécessaire.

Il semble que l'utilisation du service de découverte public soit un moyen pratique de procéder à une reconfiguration en cours d'exécution, puisque le service de découverte possède déjà toutes les informations de configuration du cluster. Toutefois, compter sur le service de découverte public entraîne des difficultés :

1.  introduit des dépendances externes pour l'ensemble du cycle de vie du cluster, et non seulement au moment du démarrage. En cas de problème de réseau entre le cluster et le service de découverte publique, le cluster en sera affecté.

2. Le service de découverte public doit refléter la configuration d'exécution correcte du cluster tout au long de son cycle de vie. Il doit proposer des mécanismes de sécurité pour éviter les actions non autorisées, ce qui est difficile.

3. Le service de découverte public doit gérer des dizaines de milliers de configurations de cluster. Le backend de notre service de découverte public n’est pas prêt à supporter cette charge.

Pour disposer d'un service de découverte qui prend en charge la reconfiguration en temps réel, le meilleur choix est de mettre en place le vôtre en interne.

[add-member]: /fr/docs/etcd/op-guide/runtime-configuration/#add-a-new-member
[disaster-recovery]: /fr/docs/etcd/op-guide/recovery/
