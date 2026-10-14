---
title: "Mode failsafe du DCS"
weight: 110
icon: fa-solid fa-shield-halved
description: "Comportement, exigences et précautions opérationnelles du mode failsafe du DCS."
module: [PATRONI]
categories: [Concept]
aliases: [/patroni/dcs_failsafe_mode/]
upstream_link: "https://patroni.readthedocs.io/en/latest/dcs_failsafe_mode.html"
---

<a id="dcs_failsafe_mode"></a>

--------

## Le problème {#the-problem}

Patroni s’appuie fortement sur le magasin de configuration distribué (DCS) pour gérer les élections de leader et détecter les partitions réseau. Un nœud ne peut exécuter PostgreSQL en tant que primaire que s’il parvient à mettre à jour le verrou de leader dans le DCS. En cas d’échec de mise à jour du verrou de leader, PostgreSQL est immédiatement rétrogradé et lancé en lecture seule. Selon le DCS utilisé, les chances de rencontrer ce problème varient. Par exemple, avec etcd, utilisé exclusivement par Patroni, les chances sont quasi nulles, tandis qu’avec l’API Kubernetes (appuyée sur etcd), ce problème peut être observé plus fréquemment.

--------

## Motifs de l'implémentation actuelle {#reasons-for-the-current-implementation}

L'échec de mise à jour du verrou de leader peut être dû à deux causes principales :

1.  Partitionnement réseau
2.  Le DCS est hors service

En général, il est impossible de distinguer ces deux cas à partir d’un seul nœud, et Patroni suppose donc le pire des cas – une partition du réseau. En cas de partition réseau, d’autres nœuds du cluster Patroni peuvent réussir à acquérir le verrou de leader et promouvoir PostgreSQL en primaire. Afin d’éviter une situation de split-brain, l’ancien primaire est rétrogradé avant l’expiration du verrou de leader.

--------

## Mode failsafe du DCS {#dcs-failsafe-mode}

Nous introduisons une option spéciale, `failsafe_mode`. Elle ne peut être activée que par la [configuration dynamique](/fr/docs/patroni/config/dynamic#dynamic) globale stockée dans la clé DCS `/config`. Si le mode failsafe est activé et que la mise à jour du verrou de leader dans le DCS échoue pour une raison autre qu'une discordance de version, de valeur ou d'index, PostgreSQL peut continuer à fonctionner comme primaire s'il peut joindre tous les membres connus du cluster via l'API REST de Patroni.

--------

## Détails d'implémentation au niveau bas {#low-level-implementation-details}

- Nous introduisons une nouvelle clé permanente dans le DCS, nommée `/failsafe`.
- La clé `/failsafe` contient tous les membres connus du cluster Patroni donné à un instant donné.
- Le leader actuel maintient la clé `/failsafe`.
- Un membre n'est autorisé à participer à la course au leader et à devenir le nouveau leader que s'il est présent dans la clé `/failsafe`.
- Si le cluster se compose d'un seul nœud, la clé `/failsafe` contiendra un seul membre.
- En cas de « panne » du DCS, le primaire existant se connecte à tous les membres présents dans la clé `/failsafe` via l'API REST `POST /failsafe` et peut continuer à fonctionner en tant que primaire si toutes les répliques l'ont reconnu.
- Si l'un des membres ne répond pas, le primaire est rétrogradé.
- Les répliques utilisent les requêtes entrantes de l'API REST `POST /failsafe` comme indicateur que le primaire est toujours actif. Cette information est mise en cache pendant `ttl` secondes.

--------

## F.A.Q. {#faq}

- Pourquoi le nœud primaire actuel doit-il voir TOUS les autres membres ? Ne pouvons-nous pas compter sur le quorum à cet effet ?

  C’est une excellente question ! Le problème réside dans le fait que la vue sur le quorum peut différer selon le point de vue du DCS et de Patroni. Alors que les nœuds DCS doivent être répartis de manière égale entre les zones de disponibilité, aucune règle similaire n’existe pour Patroni, et surtout, aucun mécanisme n’existe pour introduire et imposer une telle règle. Si la majorité des nœuds Patroni se retrouve dans la partie perdante du réseau partitionné (y compris le primaire), alors le primaire doit être rétrogradé. Seule la vérification de TOUS les autres membres permet de détecter une telle situation.

- Que se passe-t-il si un nœud/pod est arrêté pendant que le DCS est hors service ?

  Si le DCS n'est pas accessible, la vérification « tous les autres membres du cluster sont-ils accessibles ? » est exécutée à chaque cycle de la boucle de battement de cœur (toutes les `loop_wait` secondes). Si le pod/nœud est arrêté, la vérification échoue et PostgreSQL sera rétrogradé en mode lecture seule, sans pouvoir se rétablir tant que le DCS n'est pas rétabli.

- Que se passe-t-il si tous les membres du cluster Patroni sont perdus pendant que le DCS est hors service ?

  Patroni peut être configuré pour créer une nouvelle réplique à partir d'une sauvegarde même lorsque le cluster ne dispose pas de leader. Toutefois, si le nouveau membre n'est pas présent dans la clé `/failsafe`, il ne pourra pas acquérir le verrou de leader ni se promouvoir.

- Que se passe-t-il si le nœud primaire perd l'accès au DCS tandis que les répliques n'en sont pas affectées ?

  Le primaire exécutera le code failsafe et contactera toutes les répliques connues. Ces répliques utiliseront ces informations comme indicateur que le primaire est actif et ne démarreront pas la course au leader, même si le verrou de leader dans le DCS a expiré.

- Comment activer le mode failsafe ?

  Avant d'activer `failsafe_mode`, assurez-vous que tous les membres utilisent une version à jour de Patroni. Vous pouvez ensuite employer soit l'[API REST](/fr/docs/patroni/rest_api#rest_api) `PATCH /config`, soit [patronictl edit-config -s failsafe_mode=true](/fr/docs/patroni/patronictl#patronictl_edit_config_parameters).
