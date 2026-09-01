---
title: "FAQ"
weight: 180
icon: fa-solid fa-circle-question
description: "Questions fréquemment posées sur l'opération et le dépannage de Patroni."
module: [PATRONI]
categories: [Référence]
aliases: [/docs/patroni/faq/]
upstream_link: "https://patroni.readthedocs.io/en/latest/faq.html"
---

<a id="faq"></a>
Dans cette section, vous trouverez les réponses aux questions les plus fréquemment posées concernant Patroni. Chaque sous-section s'efforce de se concentrer sur des types de questions différents.

Nous espérons que cela vous aidera à clarifier la majeure partie de vos questions. Si vous avez encore des interrogations ou rencontrez un problème imprévu, veuillez vous référer à [chatting](/fr/patroni/contributing_guidelines#chatting) et [reporting_bugs](/fr/patroni/contributing_guidelines#reporting_bugs) pour obtenir des instructions sur la manière de demander de l’aide ou de signaler des anomalies.

--------

## Comparaison avec d'autres solutions de haute disponibilité {#comparison-with-other-ha-solutions}

Pourquoi Patroni nécessite-t-il un cluster séparé de nœuds DCS alors que d'autres solutions comme `repmgr` n'en ont pas besoin ?
Il existe différentes manières de mettre en œuvre des solutions de haute disponibilité, chacune présentant ses avantages et inconvénients.

Logiciels tels que `repmgr` effectuent la communication entre les nœuds afin de déterminer le moment où des actions doivent être entreprises.

Patroni, en revanche, dépend de l’état stocké dans le DCS. Le DCS agit comme source de vérité pour Patroni afin de déterminer ses actions.

Bien qu’un cluster DCS séparé puisse alourdir votre architecture, cette approche réduit également les risques de survenance de scénarios de split-brain dans votre cluster Postgres.

Quelle est la différence entre Patroni et d'autres solutions de haute disponibilité en ce qui concerne la gestion de Postgres ?
Patroni ne gère pas seulement la haute disponibilité du cluster Postgres, mais gère également Postgres lui-même.

Si les nœuds Postgres n'existent pas encore, Patroni s'occupe du démarrage du nœud primaire et du nœud de secours, ainsi que de la gestion de la configuration Postgres des nœuds. Si les nœuds Postgres existent déjà, Patroni reprendra la gestion du cluster.

En complément de ce qui précède, Patroni possède également des capacités d’autoréparation. Autrement dit, si un nœud primaire échoue, Patroni ne se contente pas de basculer vers une réplique, mais tente également de se reconnecter au nœud primaire précédent en tant que réplique du nouveau nœud primaire. De même, si une réplique échoue, Patroni tente de se reconnecter à cette réplique.

C’est pourquoi nous appelons Patroni un « modèle pour les solutions de haute disponibilité ». Il va au-delà de la simple gestion de la réplication physique : il gère PostgreSQL dans son ensemble.

--------

## DCS {#dcs}

Puis-je utiliser le même cluster `etcd` pour stocker les données de deux ou plusieurs clusters Patroni ?
Oui, vous le pouvez !

Les informations relatives à un cluster Patroni sont stockées dans le DCS sous un chemin préfixé par les paramètres Patroni `namespace` et `scope`.

Tant que vous n'avez pas de conflit d'espace de noms et de portée entre différents clusters Patroni, vous pouvez utiliser le même cluster DCS pour stocker les informations de plusieurs clusters Patroni.

Que se passe-t-il si j'essaie d'utiliser la même combinaison de `namespace` et `scope` pour différents clusters Patroni qui pointent vers le même cluster DCS ?
Le second cluster Patroni qui tente d'utiliser la même combinaison de `namespace` et `scope` ne pourra pas gérer PostgreSQL, car il trouvera des informations relatives à cette même combinaison dans le DCS, mais avec un identifiant système PostgreSQL incompatible. Ce désaccord sur l'identifiant système fait que Patroni interrompt la gestion du second cluster, car il suppose qu'il s'agit d'un autre cluster et que l'utilisateur a mal configuré Patroni.

Veillez à utiliser des valeurs différentes pour `namespace` / `scope` lorsque vous gérez plusieurs clusters Patroni partageant le même cluster DCS.

Que se passe-t-il si je perds mon cluster DCS ?
Le DCS est utilisé pour stocker essentiellement l’état et la configuration dynamique du cluster Patroni.

Le premier effet est que tous les clusters Patroni qui dépendent de ce DCS passeront en mode lecture seule — sauf si [dcs_failsafe_mode](/fr/patroni/dcs_failsafe_mode#dcs_failsafe_mode) est activé.

Que dois-je faire si je perds mon cluster DCS ?
Il existe trois résultats possibles en cas de perte de votre cluster DCS :

1.  Le cluster DCS est entièrement récupéré : aucune action n'est requise côté Patroni. Une fois le cluster DCS récupéré, Patroni devrait pouvoir se rétablir également ;
2.  Le cluster DCS est recréé sur place, et les points d'accès restent identiques. Aucun changement n'est nécessaire côté Patroni ;
3.  Un nouveau cluster DCS est créé avec des points d'accès différents. Vous devrez mettre à jour les points d'accès DCS dans la configuration Patroni de chaque nœud Patroni.

Si vous rencontrez le scénario `2.` ou `3.`, Patroni s'occupera de recréer les informations d'état en fonction de l'état actuel du cluster, puis de régénérer la configuration dynamique sur le DCS à partir d'un fichier de sauvegarde nommé `patroni.dynamic.json` stocké dans le répertoire de données PostgreSQL de chaque membre du cluster Patroni.

Que se passe-t-il si je perds la majorité dans mon cluster DCS ?
Le DCS deviendra inactif, ce qui entraînera la désactivation du nœud Postgres actuellement en lecture/écriture par Patroni.

Attention : Patroni s'appuie sur l'état du DCS pour effectuer des actions sur le cluster.

Vous pouvez utiliser le paramètre [dcs_failsafe_mode](/fr/patroni/dcs_failsafe_mode#dcs_failsafe_mode) pour atténuer cette situation.

--------

## patronictl {#patronictl}

Dois-je exécuter [patronictl](/fr/patroni/patronictl#patronictl) sur l’hôte Patroni ?
Non, il n’est pas nécessaire de le faire.

Exécuter [patronictl](/fr/patroni/patronictl#patronictl) sur l'hôte Patroni est pratique si vous avez accès à l'hôte Patroni, car vous pouvez utiliser le même fichier de configuration provenant de l'`patroni`agent pour l'application [patronictl](/fr/patroni/patronictl#patronictl).

Toutefois, [patronictl](/fr/patroni/patronictl#patronictl) est essentiellement un client et peut être exécuté depuis des machines distantes. Il suffit de lui fournir une configuration suffisante pour qu'il puisse accéder au DCS et à l'API REST des membres Patroni.

Pourquoi l'information provenant d'un de mes membres Patroni a-t-elle disparu de la sortie de la commande [patronictl_list](/fr/patroni/patronictl#patronictl_list) ?
Les informations affichées par la commande [patronictl_list](/fr/patroni/patronictl#patronictl_list) sont basées sur le contenu du DCS.

Si des informations relatives à un membre disparaissent du DCS, il est très probable que l'agent Patroni sur ce nœud ne s'exécute plus, ou qu'il ne parvient pas à communiquer avec le DCS.

Comme le membre n'est pas en mesure de mettre à jour les informations, celles-ci expirent finalement dans le DCS, et le membre n'est plus affiché dans la sortie de [patronictl_list](/fr/patroni/patronictl#patronictl_list).

Pourquoi l'information relative à l'un de mes membres Patroni n'est-elle pas à jour dans la sortie de la commande [patronictl_list](/fr/patroni/patronictl#patronictl_list) ?
Les informations affichées par la commande [patronictl_list](/fr/patroni/patronictl#patronictl_list) sont basées sur le contenu du DCS.

Par défaut, ces informations sont mises à jour par Patroni environ toutes `loop_wait` secondes. Autrement dit, même si tout fonctionne normalement, vous pouvez encore observer un « délai » allant jusqu’à `loop_wait` secondes dans les informations stockées dans le DCS.

Attention, cela n'est pas une règle. Certaines opérations effectuées par Patroni entraînent une mise à jour immédiate des informations dans le DCS.

--------

## Configuration {#configuration}

Quelle est la différence entre la configuration dynamique et la configuration locale ?
La configuration dynamique (ou configuration globale) est la configuration stockée dans le DCS, et qui est appliquée à tous les membres du cluster Patroni. C’est principalement là que vous devez stocker votre configuration.

Les paramètres spécifiques à un nœud, ou les paramètres que vous souhaitez remplacer par rapport à la configuration globale, doivent être définis uniquement sur le membre Patroni souhaité en tant que configuration locale. Cette configuration locale peut être spécifiée soit via le fichier de configuration, soit via des variables d'environnement.

Voir plus dans [config](/fr/patroni/config#config).

Quels sont les types de configuration dans Patroni, et quel est leur ordre de priorité ?
Les types sont :

- Configuration dynamique : appliquée à tous les membres ;
- Configuration locale : appliquée au membre local, remplace la configuration dynamique ;
- Configuration d'environnement : appliquée au membre local, remplace à la fois la configuration dynamique et la configuration locale.

**Remarque :** certains paramètres GUC de Postgres ne peuvent être définis que globalement, c’est-à-dire via une configuration dynamique. En outre, certains GUC sont imposés par Patroni avec une valeur codée en dur.

Voir plus dans [config](/fr/patroni/config#config).

Existe-t-il une fonctionnalité pour m’aider à créer mon fichier de configuration Patroni ?
Oui, il y en a une.

Vous pouvez utiliser les commandes `patroni --generate-sample-config` ou `patroni --generate-config` pour générer une configuration Patroni d'exemple ou une configuration Patroni basée sur une instance Postgres existante, respectivement.

Veuillez vous référer à [generate_sample_config](/fr/patroni/config#generate_sample_config) et [generate_config](/fr/patroni/config#generate_config) pour plus de détails.

J'ai modifié mes paramètres dans la configuration `bootstrap.dcs`, mais Patroni n'applique pas les changements aux membres du cluster. Quel est le problème ?
Les valeurs configurées sous `bootstrap.dcs` ne sont utilisées que lors de l'amorçage d'un cluster frais. Ces valeurs sont écrites dans le DCS pendant l'amorçage.

Une fois la phase d'amorçage terminée, vous ne pourrez modifier la configuration dynamique que via le DCS.

Reportez-vous à la question suivante pour plus de détails.

Comment puis-je modifier ma configuration dynamique ?
Vous devez modifier la configuration dans le DCS. Cela s'effectue soit en utilisant :

- [patronictl_edit_config](/fr/patroni/patronictl#patronictl_edit_config) ; ou
- Une requête `PATCH` vers [config_endpoint](/fr/patroni/rest_api#config_endpoint).

Comment puis-je modifier ma configuration locale ?  
Vous devez modifier le fichier de configuration du membre Patroni concerné, puis envoyer `SIHGUP` à l'agent Patroni. Vous pouvez utiliser l'une des deux méthodes suivantes :

- Envoyez une requête `POST` à l'API REST [reload_endpoint](/fr/patroni/rest_api#reload_endpoint) ; ou

- Exécutez [patronictl_reload](/fr/patroni/patronictl#patronictl_reload) ; ou

- Signalez localement le processus Patroni avec `SIGHUP` :

  > - Si vous avez lancé Patroni via systemd, vous pouvez utiliser la commande `systemctl reload PATRONI_UNIT.service`, `PATRONI_UNIT` étant le nom du service Patroni ; ou
  > - Si vous avez lancé Patroni par d'autres moyens, vous devrez identifier le processus `patroni` et exécuter `kill -s HUP PID`, `PID` étant l'identifiant du processus `patroni`.

**Remarque :** il existe des cas où un rechargement via la commande [patronictl_reload](/fr/patroni/patronictl#patronictl_reload) peut échouer :

- Certificats API REST expirés : vous pouvez y remédier en utilisant l'option `-k` de la commande [patronictl](/fr/patroni/patronictl#patronictl);
- Identifiants incorrects : par exemple, lorsqu'on modifie les identifiants `restapi` ou `ctl` dans le fichier de configuration, puis qu'on utilise ce même fichier de configuration pour Patroni et [patronictl](/fr/patroni/patronictl#patronictl).

Comment puis-je modifier ma configuration d’environnement ?
La configuration d’environnement n’est lue par Patroni qu’au démarrage.

En gardant cela à l’esprit, si vous modifiez la configuration de l’environnement, vous devrez redémarrer l’agent Patroni correspondant.

Prenez garde à ne pas provoquer de basculement dans le cluster ! Vous pourriez être intéressé par la vérification de [patronictl_pause](/fr/patroni/patronictl#patronictl_pause).

Comment puis-je réduire les lignes de journalisation répétitives relatives au battement cardiaque pendant un fonctionnement normal ?

Si vos journaux sont trop bruyants en raison de lignes répétées telles que `Lock owner: ...` et `no action. I am ...`, configurez `log.deduplicate_heartbeat_logs: true`.

Vous pouvez le définir soit dans le fichier YAML de Patroni ([log settings](/fr/patroni/config/yaml#log_settings)), soit avec `PATRONI_LOG_DEDUPLICATE_HEARTBEAT_LOGS=true`.

Gardez à l’esprit que cela réduit le volume de journalisation en supprimant les messages de battement de cœur répétés, mais vous perdez également la visibilité du battement de cœur par boucle, qui peut être utile lors du diagnostic du basculement.

Que se passe-t-il si je modifie une directive GUC de Postgres nécessitant un redémarrage ?
Lorsque vous modifiez la configuration dynamique ou locale, comme expliqué dans les questions précédentes, Patroni s'occupe automatiquement du rechargement de la configuration de Postgres pour vous.

Que se passe-t-il si je modifie une directive GUC de Postgres nécessitant un redémarrage ?
Patroni marquera les membres concernés avec un indicateur `pending restart`.

Il vous appartient de déterminer quand et comment redémarrer les membres. Cela peut être réalisé soit par :

- [patronictl_restart](/fr/patroni/patronictl#patronictl_restart) ; ou
- Une `POST` requête à [restart_endpoint](/fr/patroni/rest_api#restart_endpoint).

**Remarque :** certains paramètres GUC de Postgres nécessitent une gestion particulière en ce qui concerne l'ordre de redémarrage des nœuds Postgres. Reportez-vous à [shared_memory_gucs](/fr/patroni/config#shared_memory_gucs) pour plus de détails.

Quelle est la différence entre `etcd` et `etcd3` dans la configuration de Patroni ?
`etcd` utilise la version 2 de l'API de `etcd`, tandis que `etcd3` utilise la version 3 de l'API de `etcd`.

Attention : les informations stockées par la version 2 de l'API ne sont pas gérables par la version 3, et inversement.

Nous vous recommandons de configurer `etcd3` plutôt que `etcd` car :

- La version 2 de l'API est désactivée par défaut à partir de etcd v3.4 ;
- La version 2 de l'API sera entièrement supprimée à partir de etcd v3.6.

J'ai `use_slots` activé dans ma configuration Patroni, mais lorsque membre du cluster devient hors ligne pendant une certaine durée, le slot de réplication utilisé par ce membre est supprimé sur le nœud amont. Que puis-je faire pour éviter ce problème ?
Il existe deux options :

1.  Vous pouvez ajuster `member_slots_ttl` (valeur par défaut `30min`, disponible depuis Patroni `4.0.0` et PostgreSQL 11) ; les slots de réplication pour les membres absents ne seront pas supprimés lorsque la durée d'indisponibilité du membre est inférieure au seuil configuré.
2.  Vous pouvez configurer des slots de réplication physique permanents pour les membres.

Depuis Patroni `3.2.0`, il est désormais possible de disposer de slots membres en tant que slots permanents gérés par Patroni.

Patroni créera les emplacements physiques permanents sur tous les nœuds et veillera à ne pas supprimer ces emplacements, tout en faisant avancer les LSN de ces emplacements sur tous les nœuds selon le LSN consommé par le membre.

Plus tard, si vous décidez de supprimer le membre correspondant, il vous incombe de modifier la configuration des emplacements permanents ; sinon, Patroni conservera ces emplacements indéfiniment.

**Remarque :** pour les versions de Patroni antérieures à `3.2.0`, il était encore possible de configurer des slots membres en tant que slots physiques permanents, mais ceux-ci n'étaient gérés qu'en tant que leader actuel. En cas de basculement ou de basculement planifié, ces slots étaient recréés sur le nouveau leader, mais cela ne garantissait pas que celui-ci disposait de tous les segments WAL du nœud absent.

**Remarque :** même avec Patroni `3.2.0`, une petite condition de course peut survenir. Au tout début, lorsque le slot est créé sur la réplique, celui-ci peut être en avance par rapport au même slot sur le leader, et si personne ne consomme ce slot, il reste une possibilité que certains fichiers manquent après un basculement. En tenant compte de cela, il est recommandé de configurer l'archivage continu, ce qui permet de restaurer les WAL nécessaires ou d'effectuer une récupération à un point précis dans le temps.

Quelle est la différence entre `loop_wait`, `retry_timeout` et `ttl` ?
Patroni effectue périodiquement ce que l'on appelle un cycle HA. À chaque cycle HA, il effectue une série de vérifications sur le cluster afin d'évaluer son état de santé, et en fonction de cet état, il peut entreprendre des actions, comme basculer vers un serveur secondaire.

`loop_wait` détermine pendant combien de secondes Patroni doit s'endormir avant d'exécuter un nouveau cycle de vérifications de haute disponibilité.

`retry_timeout` définit le délai d'attente des opérations de réessai sur le DCS et sur Postgres. Par exemple : si le DCS est inactif depuis plus de `retry_timeout` secondes, Patroni peut démoter le nœud primaire en tant qu'action de sécurité.

`ttl` définit la durée de validité du verrou `leader` dans le DCS. Si le leader actuel du cluster n'est pas en mesure de renouveler la durée de validité pendant ses cycles de haute disponibilité pendant plus de `ttl`, alors la durée de validité expirera, ce qui déclenchera une `leader race` dans le cluster.

**Note :** lors de la modification de ces paramètres, veuillez garder à l’esprit que Patroni impose la règle et les valeurs minimales décrites dans la section [dynamic](/fr/patroni/config/dynamic#dynamic) du document.

--------

## Gestion de Postgres {#postgres-management}

Puis-je modifier directement les paramètres GUC de Postgres dans la configuration de Postgres ?
Vous le pouvez, mais vous devriez éviter de le faire.

La configuration de Postgres est gérée par Patroni, et toute tentative de modifier les fichiers de configuration peut être frustrée par Patroni, qui peut éventuellement les écraser.

Plusieurs options sont disponibles pour contourner la gestion effectuée par Patroni :

- Modifiez les paramètres GUC de Postgres via `$PGDATA/postgresql.base.conf` ; ou
- Définissez un `postgresql.custom_conf` qui sera utilisé à la place de `postgresql.base.conf` afin de le gérer de manière externe ; ou
- Modifiez les paramètres GUC à l’aide de `ALTER SYSTEM` / `ALTER DATABASE` / `ALTER USER`.

Vous trouverez davantage d'informations à ce sujet dans la section [important_configuration_rules](/fr/patroni/config#important_configuration_rules).

Dans tous les cas, nous vous recommandons de gérer toute la configuration de Postgres via Patroni. Cela centralise la gestion et facilite le débogage de Patroni lorsque cela est nécessaire.

Puis-je redémarrer directement les nœuds Postgres ?
Non, vous **ne devez pas** tenter de gérer Postgres directement !

Toute tentative de redémarrer le serveur Postgres sans Patroni peut entraîner des basculements dans votre cluster.

Si vous devez gérer le serveur Postgres, procédez par les moyens exposés par Patroni.

Patroni peut-il reprendre la gestion d’un cluster PostgreSQL déjà existant ?
Oui, il le peut !

Veuillez vous référer à [existing_data](/fr/patroni/existing_data#existing_data) pour obtenir des instructions détaillées.

Comment Patroni gère-t-il Postgres ?
Patroni s'occupe de démarrer et d'arrêter Postgres en exécutant les binaires Postgres, tels que `pg_ctl` et `postgres`.

En gardant cela à l'esprit, vous **devez** désactiver toute autre source pouvant gérer les clusters Postgres, comme les unités systemd, par exemple `postgresql.service`. Seul Patroni doit être en mesure de démarrer, d'arrêter et de promouvoir les instances Postgres dans le cluster. Ne pas le faire peut entraîner des scénarios de split-brain. Par exemple : si le nœud en cours d'exécution en tant que primaire échoue et que l'unité `postgresql.service` est activée, Postgres pourrait être redémarré et provoquer un split-brain.

--------

## Concepts et exigences {#concepts-and-requirements}

Quelles sont les applications qui font partie de Patroni ?
Patroni comprend essentiellement quelques applications :

- `patroni` : C’est l'agent Patroni, chargé de gérer un nœud Postgres ;
- [patronictl](/fr/patroni/patronictl#patronictl) : Il s'agit d'un utilitaire en ligne de commande utilisé pour interagir avec un cluster Patroni (effectuer des basculements planifiés, redémarrages, modifications de configuration, etc.). Pour plus d'informations, consultez [patronictl](/fr/patroni/patronictl#patronictl).

Qu'est-ce qu'un `standby cluster` dans Patroni ?
Il s'agit d'un cluster ne comportant aucun nœud Postgres primaire en cours d'exécution, c'est-à-dire qu'aucun membre en lecture-écriture n'est présent dans le cluster.

Ces types de clusters existent pour répliquer des données depuis un autre cluster et sont généralement utiles lorsque vous souhaitez répliquer des données entre des centres de données.

Il y aura un leader dans le cluster, qui sera un standby chargé de répliquer les modifications depuis un nœud Postgres distant. Ensuite, il y aura un ensemble de standbys configurés avec une réplication en cascade à partir de ce membre leader.

**Remarque :** le cluster de secours ne connaît rien sur le cluster source dont il effectue la réplication — il peut même utiliser `restore_command` au lieu du streaming WAL, et peut utiliser un cluster DCS absolument indépendant.

Pour plus de détails, consultez [standby_cluster](/fr/patroni/standby_cluster#standby_cluster).

Qu'est-ce qu'un `leader` dans Patroni ?
Un `leader` dans Patroni est comme un coordinateur du cluster.

Dans un cluster Patroni classique, `leader` sera le nœud en lecture/écriture.

Dans un cluster de secours Patroni, le `leader` (appelé aussi `standby leader`) sera chargé de la réplication depuis un nœud Postgres distant, et de la propagation de ces modifications aux autres membres du cluster de secours.

Le cluster Patroni nécessite-t-il un nombre minimum de nœuds Postgres ?
Non, vous pouvez exécuter Patroni avec un nombre quelconque de nœuds Postgres.

Attention : Patroni est déconnecté du DCS.

Que signifie [pause](/fr/patroni/pause#pause) dans Patroni ?
Pause est une opération exposée par Patroni permettant à l'utilisateur de demander à Patroni de suspendre la gestion de Postgres.

Cela est principalement utile lorsque vous souhaitez effectuer une maintenance sur le cluster et souhaitez éviter que Patroni ne prenne de décisions liées à la haute disponibilité, comme basculer vers un serveur secondaire lorsque vous arrêtez le serveur primaire.

Vous trouverez davantage d'informations à ce sujet dans [pause](/fr/patroni/pause#pause).

--------

## Basculement automatique {#automatic-failover}

Comment fonctionne le mécanisme de basculement automatique de Patroni ?
Le basculement automatique de Patroni repose sur ce que nous appelons `leader race`.

Patroni stocke l'état du cluster dans le DCS, notamment un verrou `leader` qui contient le nom du membre Patroni qui est actuellement le `leader` du cluster.

Ce verrou `leader` est associé à une durée de vie. Si le nœud leader ne parvient pas à mettre à jour le bail du verrou `leader` à temps, la clé expirera finalement dans le DCS.

Lorsque le verrou `leader` expire, il déclenche ce que Patroni appelle un `leader race` : tous les nœuds commencent à effectuer des vérifications pour déterminer s’ils sont les meilleurs candidats à la prise en charge du rôle `leader`. Certaines de ces vérifications incluent des appels à l'API REST de tous les autres membres Patroni.

Tous les membres Patroni qui se trouvent être le meilleur candidat pour acquérir le verrou `leader` tenteront de le faire. Le premier membre Patroni qui parvient à acquérir le verrou `leader` se promeut en nœud en lecture/écriture (ou `standby leader`), et les autres sont configurés pour le suivre.

Puis-je désactiver temporairement le basculement automatique dans le cluster Patroni ?
Oui, vous le pouvez !

Vous pouvez y parvenir en mettant temporairement le cluster en pause. Cela est généralement utile pour effectuer des opérations de maintenance.

Lorsque vous souhaitez reprendre le basculement automatique du cluster, il suffit de le désactiver.

Vous trouverez davantage d'informations à ce sujet dans [pause](/fr/patroni/pause#pause).

--------

## Initialisation et création des serveurs de secours {#bootstrapping-and-standbys-creation}

Comment Patroni crée-t-il un nœud Postgres primaire ? Et un nœud en veille ?
Par défaut, Patroni utilise `initdb` pour amorcer un cluster frais, et `pg_basebackup` pour créer des nœuds en veille à partir d'une copie du membre `leader`.

Vous pouvez personnaliser ce comportement en écrivant vos propres méthodes d'amorçage et vos propres méthodes de création de réplique.

Les méthodes personnalisées sont généralement utiles lorsque vous souhaitez restaurer des sauvegardes créées par des outils de sauvegarde tels que pgBackRest ou Barman, par exemple.

Pour obtenir des informations détaillées, veuillez vous référer à [custom_bootstrap](/fr/patroni/replica_bootstrap#custom_bootstrap) et [custom_replica_creation](/fr/patroni/replica_bootstrap#custom_replica_creation).

--------

## Surveillance {#monitoring}

Comment puis-je surveiller mon cluster Patroni ?
Patroni expose quelques points de terminaison pratiques dans son [rest_api](/fr/patroni/rest_api#rest_api) :

- `/metrics` : expose les métriques de surveillance au format pouvant être consommé par Prometheus ;
- `/patroni` : expose l'état du cluster au format JSON. Les informations affichées ici sont très similaires à celles affichées par l'endpoint `/metrics`.

Vous pouvez utiliser ces points d'accès pour implémenter des vérifications de surveillance.
