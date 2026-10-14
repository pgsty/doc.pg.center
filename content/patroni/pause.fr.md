---
title: "Mode Pause/Reprise pour le cluster"
linkTitle: "Mettre en pause/Reprendre le cluster"
weight: 100
icon: fa-solid fa-stopwatch
description: "Comportement du mode pause et reprise pour la gestion du cluster Patroni."
module: [PATRONI]
categories: [Tâche]
upstream_link: "https://patroni.readthedocs.io/en/latest/pause.html"
---

<a id="pause"></a>

--------

## Objectif {#the-goal}

Dans certains cas, Patroni doit pouvoir se retirer temporairement de la gestion du cluster tout en conservant l’état du cluster dans le DCS. Les cas d’utilisation possibles concernent des activités inhabituelles sur le cluster, telles que les mises à jour majeures de version ou la récupération après corruption. Pendant ces opérations, les nœuds sont souvent démarrés et arrêtés pour des raisons inconnues de Patroni, certains nœuds pouvant même être temporairement promus, ce qui contrevient à l’hypothèse d’un seul nœud primaire en cours d’exécution. Par conséquent, Patroni doit pouvoir se « détacher » du cluster en cours d’exécution, en implémentant une fonctionnalité équivalente au mode maintenance de Pacemaker.

--------

## Implémentation {#the-implementation}

Lorsque Patroni s'exécute en mode pause, il ne modifie pas l'état de PostgreSQL, à l'exception des cas suivants :

- Pour chaque nœud, la clé membre dans le DCS est mise à jour avec les informations actuelles concernant le cluster. Cela fait que Patroni exécute des requêtes en lecture seule sur un nœud membre si ce dernier est en cours d'exécution.
- Pour le nœud Postgres primaire possédant le verrou de leader, Patroni met à jour le verrou. Si le nœud détenteur du verrou de leader cesse d’être le primaire (c'est-à-dire s’il est rétrogradé manuellement), Patroni libère le verrou au lieu de promouvoir à nouveau le nœud.
- Les redémarrages manuels, les basculements manuels (`failover` ou `switchover`) sans programmation horaire et les réinitialisations sont autorisés. Aucune action programmée pour une exécution ultérieure n’est autorisée. Un `switchover` manuel n’est autorisé que si le nœud cible est spécifié.
- Si Patroni détecte des primaires en parallèle, il émet un avertissement, mais ne rétrograde pas le primaire sans verrou de leader.
- S’il n’y a pas de verrou de leader dans le cluster, le primaire en cours d’exécution acquiert le verrou. S’il existe plus d’un nœud primaire, le premier primaire à acquérir le verrou l’emporte. S’il n’y a aucun primaire du tout, Patroni ne tente pas de promouvoir une réplique. Une exception à cette règle existe : si le verrou de leader est absent parce que l’ancien primaire s’est lui-même rétrogradé suite à une promotion manuelle, alors seul le nœud candidat mentionné dans la requête de promotion peut acquérir le verrou de leader. Lorsque le nouveau verrou de leader est accordé (c’est-à-dire après avoir promu manuellement une réplique), Patroni s’assure que les répliques qui étaient en streaming depuis l’ancien leader basculent vers le nouveau.
- Lorsque Postgres est arrêté, Patroni ne tente pas de le démarrer. Lorsque Patroni est arrêté, il ne tente pas d’arrêter l’instance Postgres qu’il gère.
- Patroni n’essaiera pas de supprimer les slots de réplication qui ne représentent ni un autre membre du cluster ni un slot figurant dans la configuration des slots permanents.

--------

## Guide utilisateur {#user-guide}

[patronictl](/fr/patroni/patronictl#patronictl) prend en charge les commandes [pause](/fr/patroni/patronictl#patronictl_pause) et [resume](/fr/patroni/patronictl#patronictl_resume).

On peut également émettre une requête `PATCH /config` vers l’API REST de Patroni avec `{"pause": true/false/null}` pour mettre à jour la clé `{namespace}/{cluster}/config` dans le DCS.
