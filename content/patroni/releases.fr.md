---
title: "Notes de version"
weight: 190
icon: fa-solid fa-scroll
description: "Notes de version et historique des modifications de Patroni, par ordre chronologique."
module: [PATRONI]
categories: [Référence]
upstream_link: "https://patroni.readthedocs.io/en/latest/releases.html"
---

<a id="releases"></a>

--------

## Version 4.1.5 {#version-415}

Publié le 2026-08-12

**Améliorations de compatibilité**

- Compatibilité avec PostgreSQL 14.24, 15.19, 16.15, 17.11, 18.6 (Alexander Kukushkin)

  Ajoutez le nouveau paramètre GUC `output_plugin_libraries`, qui restreint les plugins de décodage logique.

**Améliorations**

- Journaliser les réinitialisations de connexion de l'API REST à `DEBUG` au lieu de `WARNING` (Kyle McLaren)

  Assurez-vous que les variantes courantes de « client est parti au milieu de l'écriture » sont désactivées sans affecter le traitement des erreurs réelles (non liées à la connexion).

**Correctifs de bogues**

- Correction de l'alignement de la validation (`thread_stack_size`) (Sundong Kim)

  Corrigez la valeur `aligned` de `65535` à `65536` dans l'entrée du schéma `thread_stack_size`. Précédemment, `patroni --validate-config` rejetait presque toutes les valeurs réalistes, y compris la valeur par défaut `524288` appliquée par le démon lui-même.

- Autoriser la validation de `synchronous_mode` pour accepter `'quorum'` et des chaînes booléennes (Eray Araz)

  `patroni --validate-config` a précédemment rejeté les valeurs `synchronous_mode` telles que `quorum` et les chaînes booléennes au format PostgreSQL acceptées en temps d'exécution.

## Version 4.1.4 {#version-414}

Sorti le 2026-07-07

**Correctifs de bogues**

- Vérifiez la variable d'environnement `NOTIFY_SOCKET` avant d'utiliser le paquet `systemd` (Polina Bungina)

  Tentez d'importer et d'utiliser le package uniquement lorsque la variable d'environnement `NOTIFY_SOCKET` est définie, afin d'éviter l'exception `FileNotFoundError: [Errno 2] No such file or directory`.

- Unifier la requête `pg_replication_slots` (Polina Bungina)

  Une gestion incorrecte des valeurs `failover` et `synced` entraînait des exceptions `KeyError` lors de la suppression des slots de réplication logique incorrects.

- Prendre en compte les paramètres d'authentification spécifiques à la version lors de la génération de la configuration (Polina Bungina)

  Dans la commande `patroni --generate-config`, supprimez tous les paramètres d'authentification inapplicables qui ont été accidentellement récupérés à partir de l'environnement, en fonction de la version obtenue via une connexion PostgreSQL.

- Gérer `pg_rewind` pendant le démarrage d'une instance PostgreSQL en réplica (Alexander Kukushkin)

  Revenez aux informations de `pg_controldata` lorsqu'une instance PostgreSQL est en cours d'exécution mais n'accepte pas encore les connexions.

- Corriger le type de métrique Prometheus pour `patroni_postgres_timeline` (Huseyin Demir)

  Déclarez la métrique `patroni_postgres_timeline` comme `gauge` au lieu de `counter`, car elle n'est pas toujours strictement croissante (par exemple, elle peut être réinitialisée à 0 si une instance PostgreSQL n'est pas en cours d'exécution).

- Ne pas arrêter le watchdog tant que les clients backend ne sont pas entièrement arrêtés (Alexander Kukushkin)

  Précédemment, si `primary_stop_timeout` était plus court que le délai minimum du watchdog, et que le délai d'arrêt expirait effectivement, Patroni désactivait le watchdog avant que tous les backends clients n'aient terminé.

- Gérer l'erreur de délai d'attente de requête pour la requête de surveillance (Alexander Kukushkin)

  En cas d'erreur de délai d'attente de requête, utilisez le rôle mis en cache comme solution de repli afin d'éviter de rétrograder le primaire. En outre, définissez explicitement `pg_stat_statements.track` sur `none` pour la requête de surveillance, afin d'éviter des appels coûteux à la collecte des déchets `pg_stat_statements`.

- Supprimer les slots de réplication gérés par Patroni avec `wal_status=lost` (Alexander Kukushkin)

  Les slots de réplication avec `wal_status=lost` ne sont plus utilisables. Patroni supprimera désormais ces slots et les recréera si nécessaire.

- Corriger la représentation du rôle dans l'erreur de validation du membre patronictl (Polina Bungina)

  S'assure que la bonne représentation sous forme de chaîne est utilisée dans le message d'exception, empêchant les erreurs d'être formatées comme `Error: No CtlPostgresqlRole.REPLICA among provided members`.

## Version 4.1.3 {#version-413}

Sorti le 2026-05-05

**Améliorations de stabilité**

- Gérer correctement l'erreur etcd mal étiquetée (Ants Aasma)

  Les versions actuelles d’etcd génèrent une erreur `Unknown` lorsque le leader etcd est perdu pendant la mise à jour de la durée de location. Patroni va désormais remplacer le code d’erreur signalé par `Unavailable`.

**Correctifs de bogues**

- Utilisez la version binaire lorsque le fichier `PG_VERSION` n'existe pas (Polina Bungina)

  Dans certains cas, par exemple lors de l'utilisation d'un amorçage personnalisé, le fichier `PG_VERSION` peut ne pas être présent dans le répertoire de données. Dans ce cas, Patroni traitait la version comme 0.0, ce qui provoquait des problèmes avec certaines logiques spécifiques à la version. Avec cette correction, Patroni tentera d'obtenir la version à partir de la binaire dans de tels cas.

- Réorganisation de l'initialisation du logger pour éviter la perte des premiers messages de journal (Alexander Kukushkin)

  Créez `PatroniLogger` avant de charger `Config` afin de capturer les messages de journalisation précoces.

- Inclure `MONOTONIC_USEC` dans la notification systemd `RELOADING=1` (Alexander Kukushkin)

  systemd 257+ exige `MONOTONIC_USEC` en conjonction avec `RELOADING=1` pour les services `Type=notify-reload`. Sans cela, `systemctl reload` bloque indéfiniment.

**Améliorations**

- Passer outre la récupération après panne en mode utilisateur unique lorsque `backup_label` existe (Vadim Ponomarev)

  Passer outre la récupération après panne en mode utilisateur unique et laisser PostgreSQL gérer la récupération pendant le démarrage normal lors du lancement d'une réplique restaurée à partir d'une sauvegarde externe (non via une méthode d'amorçage personnalisée).

- Avertir lors de l'exécution sous `systemd` sans le paquet `python-systemd` (Alexander Kukushkin)

  Au lieu d’enregistrer « systemd integration is not supported » au démarrage, vérifiez la présence de `NOTIFY_SOCKET` et n’émettez un avertissement que lorsque vous êtes effectivement en cours d’exécution sous `systemd` sans que le paquet `python-systemd` soit installé.

## Version 4.1.2 {#version-412}

Publié le 2026-04-21

**Améliorations du support systemd**

- Ajouter la prise en charge du type d'unité systemd `notify-reload` (Ronan Dunklau)

  Permet à `systemctl reload` d'attendre que Patroni ait effectivement traité le rechargement de la configuration en envoyant les notifications `RELOADING=1` et `READY=1` à systemd.

- Envoyer une notification `STOPPING=1` à systemd lors de l'arrêt (Alexander Kukushkin)

  Patroni notifie désormais correctement systemd qu'il s'arrête, conformément au protocole de notification systemd.

- Ne pas permettre à PostgreSQL d'envoyer des notifications à systemd (Alexander Kukushkin)

  Supprime `NotifyAccess=all` du fichier unit systemd d'exemple. Filtre `NOTIFY_SOCKET` dans l'environnement au démarrage de PostgreSQL afin qu'il n'envoie pas `READY=1` ni `STOPPING=1` à systemd. Lorsque vous prenez en charge un PostgreSQL déjà démarré avant Patroni et qui possède déjà `NOTIFY_SOCKET`, réappliquez `READY=1` lors de l'arrêt de PostgreSQL pour contrer son `STOPPING=1`.

## Version 4.1.1 {#version-411}

Sorti le 2026-04-08

**Améliorations de stabilité**

- Compatibilité avec les modifications liées au thread dans Python 3.11+ (Alexander Kukushkin)

  Évitez de démarrer ou d'arrêter des threads en cours d'exécution. Introduisez des pools de threads pour l'API REST et pour l'exécution des tâches asynchrones. Permettez la configuration globale de `thread_pool_size` et de `restapi.thread_pool_size`.

- Compatibilité avec Python 3.14 (Alexander Kukushkin)

  Exécuter les tests contre Python 3.14 et corriger les problèmes de compatibilité.

- Compatibilité avec les correctifs de sécurité etcd dans les versions 3.6.9, 3.5.28 et 3.4.42 (Alexander Kukushkin)

  Ces versions d’etcd ont corrigé des CVEs et modifié le comportement : les lectures de topologie du cluster et les keepalives de bail ne sont désormais plus autorisés sans authentification. Patroni gère désormais cette contrainte en s’authentifiant dans les chemins d’identification des membres et de maintien du bail, en se réauthentifiant en cas d’échec d’authentification, et en renvoyant les requêtes en conséquence.

- Améliorations de la gestion des erreurs Etcd3 (Alexander Kukushkin)

  Gérer les réponses JSON corrompues, être souple dans l'analyse des erreurs JSON, et améliorer le rapport des erreurs internes d'etcd.

**Correctifs de bogues**

- Réessayer la mise à jour du leader en cas d'erreur temporaire Kubernetes `403` (Sophia Ruan, Alexander Kukushkin)

  Lorsque l'API Kubernetes retourne temporairement `403 Permission Denied` (par exemple lors de problèmes RBAC transitoires), Patroni vérifie désormais si le nœud actuel conserve toujours le statut de leader et retente la mise à jour du leader dans un délai de `retry_timeout` au lieu de rétrograder immédiatement le primaire.

- Corriger le problème de renommage du nœud leader en mode synchronisation et en pause (Alexander Kukushkin)

  La clé `/sync` n’a pas été mise à jour après le renommage du nœud leader avec un redémarrage de Patroni en pause (sans redémarrage de Postgres). Cela a empêché Patroni de promouvoir après le prochain redémarrage sans pause.

- Déclencher une vérification `pg_rewind` lorsque la timeline du même primaire augmente (Alexander Kukushkin)

  Une augmentation de timeline peut survenir suite à une récupération après panne en mode utilisateur unique, suivie d'une promotion après avoir obtenu la clé leader, tandis que les autres nœuds répliques sont isolés du DCS. Dans ce cas, les nœuds répliques n’ont pas déclenché la machine à états `pg_rewind` car le leader, et par conséquent `primary_conninfo`, n’a pas changé.

- N’écrire le mot de passe superutilisateur pendant l’amorçage `initdb` que s’il n’est pas vide (Michael Banck)

  Écrire un mot de passe vide pendant l'amorçage `initdb` causait des problèmes.

- Corriger le bogue lié à `failover_priority` avec `synchronous_mode=on` (Alexander Kukushkin)

  Les valeurs de `tag.failover_priority` ont été ignorées lorsque `synchronous_node_count > 1` était actif.

- Corriger le bug de comparaison du mot de passe `primary_conninfo` (Alexander Kukushkin)

  À compter de PostgreSQL 10, Patroni utilise le fichier passfile situé dans `primary_conninfo` et échouait à mettre à jour le passfile après la mise à jour du mot de passe de réplication dans la configuration YAML lors d’un rechargement.

- Ne redémarrez pas la réplique avec l'étiquette `nofailover` en mode pause (Alexander Kukushkin)

  Auparavant, Patroni démarrait une réplique PostgreSQL arrêtée manuellement en mode pause lorsque le tag `nofailover` était défini sur `true`.

- Corriger `check_recovery_conf()` lorsque PostgreSQL est dans l'état de démarrage (Alexander Kukushkin)

  Pour PostgreSQL v12 et les versions ultérieures, `pg_settings` ne peut pas être interrogé tant que le serveur n’est pas entièrement démarré et n’accepte pas encore de connexions. Les paramètres de récupération manquants sont désormais ajoutés à l’état interne lors de l’écriture de `postgresql.conf`. En outre, restaurez le contrôle `Postgresql.is_starting()` dans `Ha.is_healthiest_node()`.

- Valider les options utilisateur au format dictionnaire pour `initdb`/`basebackup` (m4rrypro)

  Lorsque les options `initdb` ou `basebackup` ont été fournies sous forme de dictionnaire (au lieu d'une liste), la validation `option_is_allowed()` était ignorée, autorisant l'utilisation d'options bloquées.

- Autoriser la compression côté serveur pour l'option `basebackup` (m4rrypro)

  L'option `compress` était entièrement bloquée pour `basebackup`, mais depuis PostgreSQL 15, la compression côté serveur est utile et fonctionne de manière transparente avec le format brut. La compression côté client est toujours rejetée.

- Ne pas recharger la configuration PostgreSQL pendant l'exécution d'un amorçage personnalisé (Alexander Kukushkin)

  Un amorçage personnalisé peut être complexe et impliquer plusieurs démarrages et arrêts de PostgreSQL. Les rechargements de la configuration de PostgreSQL pendant ce processus pourraient entraîner un comportement imprévu.

- Vérifier que `postgresql.parameters` est un dictionnaire (Alexander Kukushkin)

  Rejeter la nouvelle configuration si `postgresql.parameters` n'est pas un dictionnaire.

## Version 4.1.0 {#version-410}

Sortie le 2025-09-23

**Nouvelles fonctionnalités**

- Ajouter la prise en charge du type d'unité systemd « notify » (Ronan Dunklau)

  Sans type d'unité de notification, il est possible de lancer Patroni puis de lui envoyer immédiatement un signal SIGHUP via systemd, ce qui l'arrête effectivement avant qu'il n'ait eu le temps de configurer ses gestionnaires de signaux.

- Fournir les informations sur le LSN/le décalage de réception et de relecture via l'API et ctl (Polina Bungina)

  Le point de terminaison de l’API REST Patroni `/cluster` et la commande `patronictl list` fournissent désormais des informations sur le LSN de réception, le LSN de relecture, le délai de réception et le délai de relecture pour chaque membre répliqué.

- Assurer une démotion propre vers le cluster de secours (Polina Bungina)

  Veillez à ce que l'introduction de la section [standby_cluster](/fr/patroni/standby_cluster#standby_cluster) dans la configuration dynamique entraîne une démotion propre du cluster.

- Implémenter les commandes `patronictl demote-cluster` et `promote-cluster` (Polina Bungina)

  Les nouvelles commandes de démotion et de promotion du cluster gèrent à la fois l’édition dynamique de la configuration et la vérification de l’état du résultat.

- Implémenter le tag `sync_priority` (Polina Bungina)

  Ce paramètre contrôle la priorité qu'un membre doit avoir lors de la sélection d'une réplique synchrone lorsque [synchronous_mode](/fr/patroni/replication_modes#synchronous_mode) est défini sur `on`.

- Implémenter l'option `--print` pour `--validate-config` (Polina Bungina)

  Affiche la configuration locale (y compris les substitutions de configuration d'environnement) après sa validation réussie.

- Implémenter `kubernetes.bootstrap_labels` (Polina Bungina)

  Cette fonctionnalité permet de définir des étiquettes qui seront attribuées à un pod membre lorsqu'il se trouve dans l'état `initializing new cluster`, `running custom bootstrap script`, `starting after custom bootstrap` ou `creating replica`.

- Ajouter une option de configuration pour supprimer les journaux de battement de cœur en doublon (Michael Morris)

  Si elle est définie sur `true`, les journaux de battement de cœur identiques successifs ne doivent pas être affichés.

- Ajouter un attribut facultatif `cluster_type` aux slots de réplication permanents (Michael Banck)

  Cela vous permet de définir si une slot de réplication permanente particulière doit toujours être créée, ou uniquement sur un cluster primaire ou un cluster de secours.

- Rendre le header du serveur HTTP configurable (David Grierson)

  Introduisez le paramètre de configuration `restapi.server_tokens` qui permet de restreindre les informations divulguées dans l’en-tête HTTP du serveur.

- Implémenter des vérifications de disponibilité API pour la réplication sur les membres répliques (Ants Aasma)

  L’implémentation précédente considérait les répliques comme prêtes dès que PostgreSQL était démarré. Avec ce changement, un pod réplique n’est considéré comme prêt que lorsque PostgreSQL est en cours de réplication et n’a pas un retard trop important sur le leader.

**Améliorations**

- Réduire le niveau de journalisation des échecs de configuration du watchdog (Ants Aasma)

  Affichez la ligne de journal `Could not activate Linux watchdog device` au niveau de journalisation débogage, sauf si le watchdog est configuré en mode `required`. Elle était précédemment affichée au niveau info.

- Profitez de `written_lsn` et `latest_end_lsn` provenant de `pg_stat_wal_receiver` (Alexander Kukushkin)

  `written_lsn`, le LSN d'écriture réel, est désormais préféré à celui retourné par `pg_last_wal_receive_lsn()`, qui correspond en réalité au LSN de vidage. `latest_end_lsn` pointe vers le vidage du WAL sur l'hôte source. En cas de rôle primaire, cela permet un calcul plus précis du décalage de relecture, car les valeurs stockées dans le DCS ne sont mises à jour que toutes les `loop_wait` secondes.

- Éviter les interactions avec les slots créés avec l'option `failover=true` (Alexander Kukushkin)

  Ce changement est nécessaire pour rendre la fonctionnalité des slots de basculement logique entièrement fonctionnelle.

- Ajouter l'état PostgreSQL au point de terminaison de l'API REST `/metrics` (Ivan Filianin)

  Les informations sur l'état de l'instance PostgreSQL sont désormais disponibles dans la sortie au format Prometheus du point de terminaison de l'API REST `/metrics`.

--------

## Version 4.0.7 {#version-407}

Sortie le 2025-09-22

**Nouvelles fonctionnalités**

- Ajouter le support de PostgreSQL 18 RC1 (Alexander Kukushkin)

  Les règles de validation des paramètres GUC ont été étendues. Patroni gère désormais correctement le nouveau worker d'E/S en arrière-plan.

**Correctifs de bogues**

- Corriger un éventuel problème lié à la résolution de localhost en IPv6 sous Windows (András Váczi)

  Lors de la configuration de `listen_addresses` dans PostgreSQL, l'utilisation de `0.0.0.0` ou `127.0.0.1` limite l'écoute à IPv4 uniquement, excluant IPv6. Sur les systèmes Windows typiques, `localhost` résout souvent par défaut vers l'adresse IPv6 `::1`. Pour assurer la compatibilité, Patroni configure désormais PostgreSQL pour écouter sur `127.0.0.1`, plutôt que sur `localhost`, sur les systèmes Windows.

- Retourner la configuration globale uniquement lorsque la clé `/config` existe dans le DCS (Alexander Kukushkin)

  L'API REST de Patroni renvoyait une configuration vide au lieu de lever une erreur lorsque la clé `/config` était absente dans le DCS.

- Corriger le problème de mode de secours non déclenché en cas d'indisponibilité d'etcd (Alexander Kukushkin)

  Patroni ne gérait pas toujours correctement les exceptions `etcd3`, ce qui empêchait le déclenchement du mode de secours.

- Correction d'un blocage en réentrance du gestionnaire de signal (Waynerv)

  Patroni s'exécutant dans un conteneur Docker avec `PID=1` présentait des blocages dans certains cas particuliers après avoir reçu `SIGCHLD`.

- Recréer (permanent) la slot physique lorsqu'elle ne réserve pas de WAL (Israel Barth Rubio)

  Les slots de réplication physique permanents créés en dehors de l’orbite de Patroni sans réservation de WAL provoquaient une erreur `replication slot cannot be advanced`. Pour y remédier, Patroni recrée désormais ces slots.

- Gérer correctement les messages d'annulation de surveillance dans `etcd3` (Alexander Kukushkin)

  Lorsque `etcd3` envoie un message d'annulation au canal d'observation, il ne ferme pas la connexion. Cela entraîne l'utilisation par Patroni de données obsolètes. Patroni résout désormais ce problème en interrompant la boucle de lecture des réponses fractionnées et en fermant la connexion côté Patroni.

- Gérer le cas où le `HTTPConnection` socket est encapsulé par `pyopenssl` (Alexander Kukushkin)

  Patroni n'utilisait pas correctement les interfaces `pyopenssl`, imposées dans `python-etcd`.

**Améliorations de la documentation**

- Améliorer les instructions pour les clusters à deux nœuds (Nikolay Samokhvalov)

  Préciser le comportement pendant un basculement et les exigences relatives au DCS.

--------

## Version 4.0.6 {#version-406}

Sortie le 2025-06-06

**Correctifs de bogues**

- Corriger un bug lors du basculement depuis un leader ayant une priorité plus élevée (Alexander Kukushkin)

  Assurez-vous que Patroni ignore l'ancien leader ayant une priorité plus élevée lorsqu'il signale le même `LSN` que le nœud actuel.

- Corrigez les permissions du fichier `postgresql.conf` créé en dehors de `PGDATA` (Michael Banck)

  Respectez la valeur umask système lors de la création du fichier `postgresql.conf` en dehors du répertoire `PGDATA`.

- Corriger le bug lié au basculement planifié dans `synchronous_mode=quorum` (Alexander Kukushkin)

  Ne pas vérifier les exigences de quorum lorsqu'un candidat est spécifié.

- Ignorer les nœuds etcd obsolètes en comparant le terme du cluster (Alexander Kukushkin)

  Mémorisez le dernier "raft_term" connu du cluster etcd, et lors de l'exécution des requêtes clientes, comparez-le avec le "raft_term" rapporté par un nœud etcd.

- Mettre à jour les fichiers de configuration PostgreSQL sur `SIGHUP` (Alexander Kukushkin)

  Précédemment, Patroni ne remplaçait les fichiers de configuration PostgreSQL que si un changement dans la configuration globale ou locale était détecté.

- Gérer correctement l'exception `Unavailable` levée par `etcd3` (Alexander Kukushkin)

  Patroni tentait auparavant de renouveler ces requêtes sur le même nœud `etcd3`, mais passer à un autre nœud constitue une stratégie préférable.

- Améliorer la gestion des baux (`etcd3`) (Alexander Kukushkin)

  Assurez-vous que Patroni renouvelle le bail `etcd3` au moins une fois par boucle HA.

- Revérifier les annotations en cas de code d’état 409 lors de l’acquisition du verrou leader (Alexander Kukushkin)

  Implémenter le même comportement que celui appliqué à l’objet leader lors de la version 4.0.3 de Patroni.

- Prenez en compte `replay_lsn` lors de l'avancement des slots (Polina Bungina)

  N'essayez pas de faire avancer les slots sur les répliques au-delà de `replay_lsn`. En outre, faites avancer le slot à la position `replay_lsn` si `replay_lsn` dépasse déjà le `confirmed_flush_lsn` de ce slot sur la réplique, mais que la réplique n'a pas encore rejoué l'`LSN` effective à laquelle ce slot se trouve sur le primaire.

- Assurez-vous que `CHECKPOINT` est exécuté après la promotion (Alexander Kukushkin)

  Il était possible que la tâche de point de contrôle n’ait pas été réinitialisée lors de la rétrogradation, car `CHECKPOINT` n’était pas encore terminé. Cela a entraîné l’utilisation d’un `result` périmé lors de la prochaine promotion.

- Éviter d'exécuter une démotion « hors ligne » en parallèle (Alexander Kukushkin)

  En cas d'arrêt lent, il se peut que la prochaine boucle de battement de cœur déclenche à nouveau la méthode de gestion des erreurs du DCS, entraînant un avertissement `AsyncExecutor is busy, demoting from the main thread` et le redémarrage de la démotion hors ligne.

- Normaliser la valeur `data_dir` avant de renommer le répertoire de données en cas d'échec de l'initialisation (Waynerv)

  Empêchez une barre oblique finale dans la valeur du paramètre `data_dir` de perturber le processus de renommage après une erreur d'initialisation.

- Vérifiez que `synchronous_standby_names` contient la valeur attendue (Alexander Kukushkin)

  Précédemment, le mécanisme implémentant la machine à états pour la réplication synchrone sans quorum ne vérifiait pas la valeur réelle de `synchronous_standby_names`, ce qui entraînait l'utilisation d'une valeur obsolète de `synchronous_standby_names` lorsque `pg_stat_replication` est un sous-ensemble de `synchronous_standby_names`.

--------

## Version 4.0.5 {#version-405}

Sorti le 2025-02-20

**Améliorations de stabilité**

- Compatibilité avec `python-json-logger>=3.1` (Alexander Kukushkin)

  Supprimez les avertissements générés par l'utilisation de l'API ancienne.

- Compatibilité avec Python 3.13 (Alexander Kukushkin)

  Exécuter les tests contre Python 3.13.

- Compatibilité avec `pyinstaller>=4.4` (Joe Jensen)

  Passez au `iter_modules` par défaut si l'attribut `pyinstaller` `toc` n'est pas présent.

- Corriger les problèmes liés à la prise en charge de PostgreSQL 9.5 (Alexander Kukushkin)

  - Gérer correctement le format de sortie `pg_rewind`.
  - Tenir compte du fait que le format `synchronous_standby_names` ne prend pas en charge la spécification « num ».

- Compatibilité avec les derniers changements apportés à `urlparse` (Alexander Kukushkin)

  `urlparse` n'accepte plus plusieurs hôtes contenant le caractère `[]` dans l'URL. Pour pallier ce problème, passez aux wrappers natifs de `PQconninfoParse()` à partir de `libpq`, lorsque cela est possible, et utilisez uniquement notre implémentation pour les versions anciennes de `psycopg2` liées à une version obsolète de `libpq`.

**Correctifs de bogues**

- Afficher uniquement les membres à redémarrer lors de la confirmation du redémarrage (András Váczi)

  Précédemment, lors de l'exécution de `patronictl restart <clustername> --pending`, la confirmation listait tous les membres, qu'ils aient ou non un redémarrage en attente.

- Annuler les tâches longues en cours lors de l'arrêt de Patroni et supprimer le répertoire de données en cas d'échec de l'amorçage d'une réplique (Alexander Kukushkin)

  Précédemment, Patroni pouvait s'arrêter pendant l'amorçage d'une réplique, tandis que `pg_basebackup` / `wal-g` / `pgBackRest` / `barman` ou des outils similaires continuaient de fonctionner.

- Gérer correctement les noms de cluster contenant une barre oblique dans `patronictl edit-config` (Antoni Mur)

  Remplacez une barre oblique dans `cluster_name` par un trait de soulignement.

- Éviter de supprimer les slots physiques trop tôt (Alexander Kukushkin)

  Reporter la suppression des slots de réplication physique contenant `xmin` après un basculement : sur le nouveau primaire — jusqu’à ce que ce membre soit promu, sur les répliques — jusqu’à ce qu’un leader soit présent dans le cluster.

- Gérer toutes les exceptions levées par le sous-processus dans `controldata()` (Alexander Kukushkin)

  Patroni ne gérait pas correctement toutes les exceptions pouvant être levées lors de l'appel de l'utilitaire `pg_controldata`.

- Corriger le bug lié à un slot d’un ancien leader non conservé lors d’un basculement (Alexander Kukushkin)

  Évitez de vous fier à tort à la présence des membres dans le DCS pendant un basculement, car la clé `/member` du leader précédent expire précisément au même moment.

- Corriger quelques bogues dans la machine à états du quorum (Alexander Kukushkin)

  - Lorsqu’il s’agit d’évaluer la présence de nœuds sains pour une course au rôle de leader, il est nécessaire de prendre en compte les exigences de quorum avant de procéder à la rétrogradation. En l’absence de cette prise en compte, l’ancien leader pourrait se retrouver en récupération entouré de nœuds asynchrones.
  - `QuorumStateResolver` ne gérant pas correctement le cas où un nœud réplique se connecte puis se déconnecte rapidement.

**Améliorations**

- Améliorer le message d'erreur en cas de fichier de configuration vide ou non au format dictionnaire (Julian)

  Lancer une exception plus explicite lors de la validation de la présence d'un objet `Mapping` valide dans le fichier de configuration Patroni.

--------

## Version 4.0.4 {#version-404}

Sorti le 2024-11-22

**Améliorations de stabilité**

- Ajouter la compatibilité avec le module `py-consul` (Alexander Kukushkin)

  Le module `python-consul` n'est plus maintenu depuis longtemps, tandis que `py-consul` en est le remplacement officiel. La compatibilité descendante avec python-consul est conservée.

- Ajouter la compatibilité avec le module `prettytable>=3.12.0` (Alexander Kukushkin)

  Traiter les avertissements de dépréciation.

- Compatibilité avec le module `ydiff==1.4.2` (Alexander Kukushkin)

  Corrigez les problèmes de compatibilité pour la dernière version, restreignez la version dans `requirements.txt`, et introduisez un test de compatibilité pour la dernière version.

**Correctifs de bogues**

- Exécuter le rappel `on_role_change` après un échec de récupération du primaire (Polina Bungina, Alexander Kukushkin)

  Exécutez également le rappel `on_role_change` pour une instance primaire qui n’a pas pu démarrer après un incident, afin d’augmenter les chances que le rappel soit exécuté, même si le démarrage ultérieur en tant que réplique échoue.

- Corriger une fuite de thread dans `patronictl list -W` (Alexander Kukushkin)

  Mettre en cache l'objet d'instance DCS pour éviter les fuites de threads.

- Veillez à n'écrire que les paramètres pris en charge dans la chaîne de connexion (Alexander Kukushkin)

  Patroni transmettait des paramètres introduits dans les versions plus récentes dans la chaîne de connexion, ce qui entraînait des erreurs de connexion.

--------

## Version 4.0.3 {#version-403}

Sorti le 2024-10-18

**Correctifs de bogues**

- Désactiver `pgaudit` lors de la création d'utilisateurs afin de ne pas exposer le mot de passe (kviset)

  Patroni enregistrait les mots de passe `superuser`, `replication` et `rewind` lors de leur création lorsque l'extension `pgaudit` était activée.

- Corriger le problème lié aux configurations mixtes : primaire sur une version de Patroni antérieure à la v4 et répliques en v4+ (Alexander Kukushkin)

  Utilisez `xlog_location` extrait de la clé `/members` au lieu de tenter d'obtenir la position du slot d'un membre à partir de la clé `/status` si la version de Patroni en cours d'exécution sur le leader est antérieure à 4.0.0. Ne pas procéder ainsi entraîne une accumulation des WAL sur les répliques.

- Ne pas ignorer les paramètres GUC PostgreSQL valides qui n'ont pas de validateur Patroni (Polina Bungina)

  Vérifier toujours contre `postgres --describe-config` si une directive GUC ne dispose pas de validateur Patroni mais est en réalité une directive GUC valide.

**Améliorations**

- Vérifier les annotations en cas de code d'état 409 lors de la lecture de l'objet leader dans K8s (Alexander Kukushkin)

  Évitez une mise à jour supplémentaire si la requête `PATCH` a été annulée par Patroni, même si la requête a réussi à mettre à jour la cible.

- Ajouter la prise en charge de l'option de connexion côté client `sslnegotiation` (Alexander Kukushkin)

  `sslnegotiation` a été ajouté à la version finale de PostgreSQL 17.

--------

## Version 4.0.2 {#version-402}

Sorti le 2024-09-17

**Correctifs de bogues**

- Gérer les exceptions lors de la découverte des fichiers de validation de configuration (Alexander Kukushkin)

  Ignorer les répertoires pour lesquels Patroni ne dispose pas des autorisations suffisantes pour effectuer des opérations de liste.

- Assurez-vous que les slots de réplication physique inactifs ne retiennent pas `xmin` (Alexander Kukushkin, Polina Bungina)

  Depuis la version 3.2.0, Patroni crée des slots de réplication physique pour tous les membres sur les répliques et les met à jour périodiquement à l’aide de la fonction `pg_replication_slot_advance()`. Toutefois, si `hot_standby_feedback` est activé pour une raison quelconque et que le primaire est rétrogradé en réplique, les slots désormais inactifs transmettent la valeur `NOT NULL` `xmin` au nouveau primaire. Cela empêche le seuil `xmin` d’être avancé et empêche le vacuum de nettoyer les tuples morts. Avec cette correction, Patroni recrée les slots de réplication physique qui devraient être inactifs mais dont la valeur `NOT NULL` `xmin` est présente.

- Corriger un traitement d'erreur non géré `DCSError` pendant la phase de démarrage (Waynerv)

  Assurez-vous de la connectivité DCS avant de vérifier l'unicité du nom du nœud.

- Inclure explicitement les paramètres GUC `CMDLINE_OPTIONS` lors de la requête sur `pg_settings` (Alexander Kukushkin)

  Veillez à ce que toutes les options GUC transmises au postmaster sous forme de paramètres de ligne de commande soient restaurées lorsque Patroni rejoint un standby en cours d'exécution. Il s'agit d'une correction complémentaire liée au correctif appliqué dans Patroni 3.2.2.

- Corriger la logique d'encadrement des chaînes dans `synchronous_standby_names` (Alexander Kukushkin)

  Selon la documentation PostgreSQL, les mots-clés `ANY` et `FIRST` doivent être entre guillemets doubles, ce que Patroni n'avait pas fait auparavant.

- Corriger le problème de connexion keepalive hors plage (hadizamani021)

  Assurez-vous que la valeur calculée de l'option `keepalive`, basée sur la valeur configurée de `ttl`, ne dépasse pas la valeur maximale autorisée pour la plateforme actuelle.

--------

## Version 4.0.1 {#version-401}

Sortie le 2024-08-30

**Correction de bogue**

- Patroni créait des slots de réplication inutiles pour lui-même (Alexander Kukushkin)

  Cela se produisait si `name` contenait des majuscules ou des caractères spéciaux.

--------

## Version 4.0.0 {#version-400}

Sortie le 2024-08-29

> [!WARNING]
> - Cette version achève le travail de suppression du terme « master », en faveur de « primary ». Cela implique quelques modifications non rétrocompatibles, veuillez lire attentivement les notes de version. La mise à jour vers Patroni 4+ fonctionnera de manière fiable uniquement si vous exécutez Patroni 3.1.0 ou une version ultérieure. La mise à jour depuis une version antérieure directement vers 4+ est possible, mais peut entraîner un comportement imprévu si le nœud primaire tombe pendant que les autres nœuds fonctionnent avec d'autres versions de Patroni.

**Modifications non rétrocompatibles**

- Les modifications non rétrocompatibles suivantes ont été introduites lors de la suppression du terme non inclusif « master » dans le code de Patroni :
  - Sur Kubernetes, Patroni définit par défaut l'étiquette `role` sur `primary`. Si vous souhaitez conserver le comportement ancien et éviter toute interruption ou migrations complexes et longues, vous pouvez configurer les paramètres `kubernetes.leader_label_value` et `kubernetes.standby_leader_label_value` à `master`. En savoir plus [ici](/fr/patroni/kubernetes#kubernetes_role_values).
  - Le rôle Patroni est écrit dans le DCS sous le nom `primary` au lieu de `master`.
  - Le rôle Patroni retourné par l'API REST de Patroni a été modifié de `master` à `primary`.
  - L'API REST de Patroni n'accepte plus `role=master` dans les requêtes aux points de terminaison `/switchover`, `/failover`, `/restart`.
  - Le point de terminaison de l'API REST `/metrics` ne rapportera plus la métrique `patroni_master`.
  - [patronictl](/fr/patroni/patronictl#patronictl) n'accepte plus l'option `--master` pour aucune commande. Les options `--leader` ou `--primary` doivent être utilisées à la place.
  - `no_master` dans la configuration déclarative des méthodes de création de réplique personnalisées n'est plus traité comme une option spéciale ; utilisez `no_leader` à la place.
  - `patroni_wale_restore` ne prend plus en charge l'option `--no_master`.
  - `patroni_barman` ne prend plus en charge l'option `--role=master`.
  - Tous les scripts de rappel sont exécutés avec l'option `role=primary` passée au lieu de `role=master`.
- `patronictl failover` ne prend plus en charge l'option `--leader` qui était obsolète depuis Patroni 3.2.0.
- La fonctionnalité de création d'utilisateurs (`bootstrap.users` section de configuration) obsolète depuis Patroni 3.2.0 a été supprimée.

**Nouvelles fonctionnalités**

- Basculement basé sur le quorum (Ants Aasma, Alexander Kukushkin)

  La fonctionnalité implémente une réplication synchrone basée sur le quorum (disponible à partir de PostgreSQL v10), qui permet de réduire les latences dans le pire des cas, même en opération normale, car une latence plus élevée de réplication vers un serveur secondaire peut être compensée par les autres serveurs secondaires. Patroni met en place des mesures supplémentaires pour empêcher toute perte de données visible par l’utilisateur en choisissant comme candidat au basculement le serveur ayant reçu la transaction la plus récente.

- Inscrire les secondaires Citus dans `pg_dist_node` (Alexander Kukushkin)

  Patroni maintient désormais la liste des nœuds avec `role==replica`, `state==running` et sans `noloadbalance` [tag](/fr/patroni/config/yaml#tags_settings) dans `pg_dist_node`.

- Durée de rétention configurable des slots de réplication des membres (Alexander Kukushkin)

  Implémente le support du paramètre de configuration global `member_slots_ttl`, qui détermine pendant combien de temps les slots de réplication des membres doivent être conservés lorsque la clé du membre est absente.

- Rendre les permissions des fichiers de journalisation créés par Patroni configurables (Alexander Kukushkin)

  Permet de définir des permissions spécifiques pour les fichiers de journal créés par Patroni. Si non spécifié, les permissions sont définies en fonction de la valeur actuelle de `umask`.

- Compatibilité avec PostgreSQL 17 beta3 (Alexander Kukushkin)

  Les règles de validation des paramètres GUC ont été étendues. Patroni gère tous les nouveaux backends auxiliaires lors de l'arrêt et définit `dbname` dans `primary_conninfo`, comme requis pour la synchronisation des slots de réplication logique.

- Implémenter l'option `--ignore-listen-port` pour la validation de la configuration Patroni (Sahil Naphade)

  Permettre d'ignorer les ports déjà bindés lors de l'exécution de `patroni --validate-config`.

**Améliorations**

- Rendre `wal_log_hints` configurables (Paul_Kim)

  Permet d'éviter la surcharge liée à l'activation de `wal_log_hints` lorsque `use_pg_rewind` est défini sur `off`.

- Journaliser la commande `pg_basebackup` au niveau `DEBUG` (Waynerv)

  Facilite le débogage des initialisations échouées.

**Correctifs de bogues**

- Avancer les slots permanents pour les nœuds en cascade pendant le mode de secours (Alexander Kukushkin)

  Assurez-vous que les slots des répliques en cascade sont correctement avancés sur le serveur primaire lorsque le mode de secours est activé. Cela est réalisé en étendant la réponse des répliques à la requête de l'API REST `POST /failsafe` avec leur `xlog_location`.

- Ne pas permettre au nœud actuel d'être sélectionné comme synchrone (Alexander Kukushkin)

  Il se peut qu’un « quelque chose » soit en cours de diffusion depuis le nœud primaire actuel avec `application_name`, correspondant au nom du nœud primaire actuel. Patroni ne gérait pas correctement cette situation, ce qui pouvait entraîner la déclaration du nœud primaire comme nœud synchrone, bloquant ainsi les basculements planifiés.

- Ignorer `restapi.allowlist_include_members` pour les requêtes POST /failsafe (Alexander Kukushkin)

- Améliorer la validation des paramètres GUC (Polina Bungina)

  En raison de la validation supplémentaire effectuée via l'exécution de la commande `postgres --describe-config`, il était auparavant impossible de définir des GUCs non listés dans ce cadre par le biais de la configuration Patroni. Cette limitation est désormais levée.

- Ajouter une ligne avec `localhost` au fichier `.pgpass` lorsque des sockets Unix sont détectés (Alexander Kukushkin)

  Patroni ajoutera une ligne supplémentaire au fichier `.pgpass` si le paramètre `host` spécifié commence par le caractère `/`. Cela permet de traiter un cas particulier où `host` correspond au chemin par défaut du répertoire de socket.

- Corriger les problèmes de journalisation (Waynerv)

  URL de requête correctement définie dans les journaux de gestion des erreurs en mode de secours et ordre des horodatages corrigé dans les journaux de vérification du postmaster.

--------

## Version 3.3.2 {#version-332}

Publié le 2024-07-11

**Correctifs de bogues**

- Corriger le mode de réplication synchrone PostgreSQL en mode simple (Israel Barth Rubio)

  Depuis l'introduction de [synchronous_mode](/fr/patroni/replication_modes#synchronous_mode) dans Patroni, la réplication synchrone brute de Postgres ne fonctionnait plus. Avec cette correction, Patroni définit la valeur de `synchronous_standby_names` selon la configuration de l'utilisateur, le cas échéant, lorsque [synchronous_mode](/fr/patroni/replication_modes#synchronous_mode) est désactivé.

- Gérer l'invalidation des slots logiques sur une instance de secours (Polina Bungina)

  Depuis PG16, les slots de réplication logique sur une instance de secours peuvent être invalidés en raison de l’horizon : à partir de maintenant, Patroni impose la copie (c’est-à-dire la recréation) des slots invalidés.

- Corriger la condition de course entre l'avancement du slot logique et la copie (Alexander Kukushkin)

  En raison de ce bogue, il était possible qu'une slot de réplication logique invalidée soit copiée lors d'un redémarrage de PostgreSQL à plusieurs reprises.

--------

## Version 3.3.1 {#version-331}

Sorti le 2024-06-17

**Améliorations de stabilité**

- Compatibilité avec Python 3.12 (Alexander Kukushkin)

  Gérer un nouvel attribut ajouté à `logging.LogRecord`.

**Correctifs de bogues**

- Corriger la récursion infinie dans la gestion des balises `replicatefrom` (Alexander Kukushkin)

  Dans le cadre de cette correction, améliorer également le contrôle `is_physical_slot()` et mettre à jour la documentation.

- Corriger le rapport de rôle incorrect dans les clusters de secours (Alexander Kukushkin)

  `synchronous_standby_names` et la réplication synchrone ne fonctionnent qu'avec un nœud primaire réel, et dans le cas de la réplication en cascade, ils sont simplement ignorés par Postgres. Avant cette correction, `patronictl list` et `GET /cluster` signalait à tort certains nœuds comme synchrones.

- Assurer la disponibilité du paramètre GUC `allow_in_place_tablespaces` (Polina Bungina)

  `allow_in_place_tablespaces` a été ajouté non seulement à PostgreSQL 15, mais également intégré en retour (backpatched) dans les versions 10 à 14.

--------

## Version 3.3.0 {#version-330}

Sorti le 2024-04-04

> [!WARNING]
> Toutes les versions anciennes de Patroni sont incompatibles avec `ydiff>=1.3`.
>
> Les options suivantes sont disponibles pour "résoudre" le problème :
>
> 1.  mettre à jour Patroni vers la dernière version
> 2.  installer `ydiff<1.3` après l'installation de Patroni
> 3.  installer le module `cdiff`

**Nouvelles fonctionnalités**

- Ajouter la possibilité de passer `auth_data` au client Zookeeper (Aras Mumcuyan)

  Il permet de spécifier les identifiants d'authentification à utiliser pour la connexion.

- Ajouter un script contrib pour l'intégration avec `Barman` (Israel Barth Rubio)

  Fournissez une application `patroni_barman` permettant d'effectuer des opérations `Barman` à distance et pouvant être utilisée comme méthode d'amorçage personnalisée ou de réplique personnalisée, ou comme rappel `on_role_change`. Veuillez consulter [ici](/fr/patroni/tools_integration#tools_integration) pour plus d'informations.

- Prise en charge du format de journal `JSON` (alisalemmi)

  Outre `plain` (par défaut), Patroni prend désormais en charge le format de journalisation `json`. Nécessite que la bibliothèque `python-json-logger>=2.0.2` soit installée.

- Afficher les informations `pending_restart_reason` (Polina Bungina)

  Fournit des informations détaillées sur les paramètres PostgreSQL ayant déclenché l'indicateur `pending_restart`. Aussi bien `patronictl list` que le point de terminaison REST `/patroni` affichent désormais les noms des paramètres et leur « diff » dans `pending_restart_reason`.

- Implémenter le tag `nostream` (Grigory Smolkin)

  Si l'étiquette `nostream` est définie sur `true`, le nœud n'utilisera pas le protocole de réplication pour diffuser les WAL, mais s'appuiera à la place sur la récupération depuis les archives (si `restore_command` est configuré). Cela désactive également la copie et la synchronisation des slots de réplication logique permanents sur le nœud lui-même et sur toutes ses répliques en cascade.

**Améliorations**

- Effectuer la validation de la section `log` (Alexander Kukushkin)

  Jusqu'à présent, le validateur ne vérifiait pas la correction de la configuration de journalisation fournie.

- Améliorer la journalisation des modifications des paramètres PostgreSQL (Polina Bungina)

  Convertir les anciennes valeurs au format lisible par un humain et journaliser les informations concernant le désaccord entre la configuration `pg_controldata` et la configuration globale de Patroni.

**Correctifs de bogues**

- Filtrer correctement les options non autorisées `pg_basebackup` (Israel Barth Rubio)

  En raison d'un bogue, Patroni ne filtrait pas correctement les options non autorisées configurées pour la méthode d'amorçage de la réplique `basebackup`, lorsqu'elles étaient fournies au format `- setting: value`.

- Correction de la gestion des erreurs d'authentification `etcd3` (Alexander Kukushkin)

  Toujours réessayer une fois en cas d'erreur d'authentification `etcd3` si l'authentification n'a pas été effectuée juste avant l'exécution de la requête. En outre, ne pas redémarrer les observateurs lors de la réauthentification.

- Améliorer la logique de découverte des fichiers validateurs (Waynerv)

  Utilisez la bibliothèque `importlib` pour découvrir les fichiers contenant des paramètres de configuration disponibles, lorsque cela est possible (pour Python 3.9+). Cette implémentation est plus stable et ne perturbe pas les distributions Patroni basées sur les archives `zip`.

- Utilisez `target_session_attrs` uniquement lorsque plusieurs hôtes sont spécifiés dans la section [standby_cluster](/fr/patroni/standby_cluster#standby_cluster) (Alexander Kukushkin)

  `target_session_attrs=read-write` est désormais ajouté à `primary_conninfo` sur le nœud de secours en tant que leader, uniquement lorsque la section `standby_cluster.host` contient plusieurs hôtes séparés par des virgules.

- Ajouter du code de compatibilité pour la bibliothèque `ydiff` version 1.3+ (Alexander Kukushkin)

  Patroni s'appuie sur certaines API de `ydiff` qui ne sont pas publiques, car elles sont censées ne servir qu'à un outil terminal et non à un module Python. Malheureusement, les modifications apportées à l'API dans la version 1.3 ont rompu la compatibilité avec les anciennes versions de Patroni.

--------

## Version 3.2.2 {#version-322}

Sorti le 2024-01-17

**Correctifs de bogues**

- Ne pas permettre à la réplique de restaurer la clé d’initialisation lorsque le DCS a été effacé (Alexander Kukushkin)

  Cela se produisait dans la méthode où Patroni devait reprendre un cluster PG autonome.

- Utiliser une lecture cohérente lors de la récupération de la clé de synchronisation mise à jour depuis Consul (Alexander Kukushkin)

  Consul ne propose aucune interface permettant d'obtenir immédiatement `ModifyIndex` pour la clé que nous venons de mettre à jour, il faut donc effectuer une opération de lecture explicite. Étant donné que les lectures obsolètes sont autorisées par défaut, nous pouvions parfois obtenir une version obsolète de la clé.

- Recharger la configuration de Postgres si un paramètre nécessitant un redémarrage a été rétabli à sa valeur d'origine (Polina Bungina)

  Précédemment, Patroni ne mettait pas à jour la configuration, mais réinitialisait uniquement le `pending_restart`.

- Corriger la logique inversée du message de confirmation lors d’un basculement vers un candidat asynchrone en mode synchrone (Polina Bungina)

  Le problème n'existe que dans [patronictl](/fr/patroni/patronictl#patronictl).

- Exclure le leader des candidats au basculement dans [patronictl](/fr/patroni/patronictl#patronictl) (Polina Bungina)

  Si le cluster est sain, basculer vers un leader existant est une opération sans effet.

- Créer la base de données Citus et l'extension de manière idempotente (Alexander Kukushkin, Zhao Junwang)

  Il permettra de les créer dans le script `post_bootstrap` au cas où il serait nécessaire d'ajouter d'autres dépendances à la base de données Citus.

- Ne pas filtrer la balise `nofailover` contradictoire (Polina Bungina)

  La configuration `{nofailover: false, failover_priority: 0}` définie sur un nœud ne lui a pas permis de participer à la course, ce qui devrait être le cas, car le tag `nofailover` doit avoir la priorité.

- Corrigé le problème lié au gel avec PyInstaller (Sophia Ruan)

  Le `freeze_support()` a été appelé après `argparse`, ce qui a empêché Patroni de démarrer PostgreSQL.

- Correctif d'un bogue dans le générateur de configuration pour la configuration [patronictl](/fr/patroni/patronictl#patronictl) et [Citus](/fr/patroni/citus#citus) (Israel Barth Rubio)

  Il empêchait les paramètres de configuration [patronictl](/fr/patroni/patronictl#patronictl) et [Citus](/fr/patroni/citus#citus) définis via des variables d'environnement d'être écrits dans la configuration générée.

- Restaurer les paramètres GUC de récupération et certains paramètres gérés par Patroni lors de la connexion à un standby en cours d'exécution (Alexander Kukushkin)

  Patroni échouait à redémarrer Postgres à partir de la version 12 avec une erreur signalant l'absence de `port` dans l'une des structures internes.

- Correctifs liés au drapeau `pending_restart` (Polina Bungina)

  N'exposez pas `pending_restart` lorsqu'un amorçage personnalisé est utilisé avec `recovery_target_action = promote` ou lorsque `hot_standby` ou `wal_log_hints` ont été modifiés, par exemple à l'aide de `ALTER SYSTEM`.

--------

## Version 3.2.1 {#version-321}

Sorti le 2023-11-30

**Correctifs de bogues**

- Limite les valeurs acceptées pour l'argument `--format` dans [patronictl](/fr/patroni/patronictl#patronictl) (Alexander Kukushkin)

  Il acceptait auparavant n'importe quelle chaîne arbitraire et ne produisait aucune sortie si la valeur n'était pas reconnue.

- Vérifiez que les nœuds répliques ont reçu le LSN de point de contrôle lors de l'arrêt avant de libérer la clé leader (Alexander Kukushkin)

  Précédemment, dans certains cas, nous utilisions le LSN de l’enregistrement SWITCH qui est suivi d’un CHECKPOINT (si le mode d’archivage est activé). En conséquence, le primaire précédent devait parfois effectuer `pg_rewind`, mais cela n’entraînait aucune perte de données.

- Effectuer une requête HTTP réelle lors de la vérification de l'unicité du nom de nœud (Alexander Kukushkin)

  Lors de l'exécution de Patroni dans des conteneurs, il se peut que le trafic soit acheminé via `docker-proxy`, qui écoute sur le port et accepte les connexions entrantes. Cela provoquait des faux positifs.

- Corrigé le support de Citus avec etcd v2 (Alexander Kukushkin)

  Patroni échouait à déployer un nouveau cluster Citus avec etcd v2.

- Corrigé le comportement de `pg_rewind` avec PostgreSQL v16+ (Alexander Kukushkin)

  Le format du message d'erreur de `pg_waldump` a été modifié en version 16, ce qui a entraîné l'appel de `pg_rewind` par Patroni même lorsque cela n'était pas nécessaire.

- Correctif d'un bug lié à l'amorçage personnalisé (Alexander Kukushkin)

  Patroni appliquait incorrectement l'argument `--command`, qui est en lui-même une commande d'amorçage.

- Corrigé le problème lié aux points de terminaison de vérification de santé de l'API REST (Sophia Ruan)

  Il existait des risques que, après le redémarrage de Postgres, l’état `unknown` soit retourné pour Postgres en raison de connexions non correctement fermées.

- Mettre en cache les résultats de sortie de `postgres --describe-config` (Waynerv)

  Ils sont utilisés pour déterminer quels paramètres GUC sont disponibles afin de valider la configuration de PostgreSQL, et nous ne prévoyons pas que cette liste change pendant l'exécution de Patroni.

--------

## Version 3.2.0 {#version-320}

Sorti le 2023-10-25

**Avis de dépréciation**

- Le support `bootstrap.users` sera supprimé à partir de la version 4.0.0. Si vous devez créer des utilisateurs après le déploiement d'un nouveau cluster, utilisez le hook `bootstrap.post_bootstrap` à cette fin.

**Modifications non rétrocompatibles**

- Appliquer la règle `loop_wait + 2*retry_timeout <= ttl` et fixer en dur les valeurs minimales possibles (Alexander Kukushkin)

  Valeurs minimales : `loop_wait=2`, `retry_timeout=3`, `ttl=20`. Si les valeurs sont inférieures ou violent cette règle, elles sont ajustées et un avertissement est inscrit dans les journaux de Patroni.

**Nouvelles fonctionnalités**

- Priorité de basculement (Mark Pekala)

  Avec l'aide de `tags.failover_priority`, il est désormais possible de rendre un nœud plus favorisé lors de la course au leader. Plus de détails dans la documentation (référence aux balises).

- Implémenté `patroni --generate-config [--dsn DSN]` et `patroni --generate-sample-config` (Polina Bungina)

  Il permet de générer un fichier de configuration pour le cluster PostgreSQL en cours d'exécution ou un fichier de configuration exemple pour un nouveau cluster Patroni.

- Utilisez une connexion dédiée à Postgres pour l'API REST de Patroni (Alexander Kukushkin)

  Cela permet d'éviter de bloquer la boucle principale de battement si le système est sous forte charge.

- Enrichir certains points de terminaison avec le `name` du nœud (sskserk)

  Pour le point de terminaison de surveillance, `name` est ajouté à côté de `scope`, et pour le point de terminaison des métriques, `name` est ajouté aux étiquettes.

- Veiller à la distinction stricte entre basculement et basculement planifié (Polina Bungina)

  Améliorer la précision des messages de journalisation et autoriser le basculement vers un nœud asynchrone dans un cluster synchrone sain.

- Rendre les slots de réplication physique permanents compatibles avec le comportement des slots logiques permanents (Alexander Kukushkin)

  Créez des slots de réplication physique permanents sur tous les nœuds pouvant devenir le leader et utilisez la fonction `pg_replication_slot_advance()` pour avancer `restart_lsn` sur les slots des nœuds de secours.

- Ajouter la capacité de spécifier un espace de noms via l'argument `--dcs` dans [patronictl](/fr/patroni/patronictl#patronictl) (Israel Barth Rubio)

  Cette possibilité peut être utile lorsque [patronictl](/fr/patroni/patronictl#patronictl) est utilisé sans fichier de configuration.

- Ajouter la prise en charge de paramètres supplémentaires dans la configuration d'amorçage personnalisée (Israel Barth Rubio)

  Précédemment, il n’était possible d’ajouter que des arguments personnalisés à `command`, mais on peut désormais les spécifier sous forme de mappage.

**Améliorations**

- Définissez la variable GUC `citus.local_hostname` sur la même valeur utilisée par Patroni pour se connecter à Postgres (Alexander Kukushkin)

  Il existe des cas où Citus doit établir une connexion avec le serveur Postgres local. Par défaut, il utilise `localhost`, qui n'est pas toujours disponible.

**Correctifs de bogues**

- Ignorez le paramètre [synchronous_mode](/fr/patroni/replication_modes#synchronous_mode) dans un cluster de secours (Polina Bungina)

  Postgres ne prend pas en charge la réplication synchrone en cascade, et le fait de ne pas ignorer [synchronous_mode](/fr/patroni/replication_modes#synchronous_mode) rompait le basculement planifié dans un cluster de secours.

- Gérer SIGCHLD pour le rappel `on_reload` (Alexander Kukushkin)

  Ne pas le faire entraîne un processus zombie, qui n’est ramassé qu’au moment de l’exécution suivante de `on_reload`.

- Gérer l'erreur `AuthOldRevision` lors de l'utilisation d'etcd v3 (Alexander Kukushkin, Kenny Do)

  L'erreur est levée si etcd est configuré pour utiliser JWT et que la base de données utilisateur dans etcd est mise à jour.

--------

## Version 3.1.2 {#version-312}

Publié le 2023-09-26

**Correctifs de bogues**

- Correctif d'un bogue lié aux vérifications `wal_keep_size` (Alexander Kukushkin)

  Le `wal_keep_size` est une variable GUC qui possède normalement une unité, et Patroni échouait à convertir sa valeur en `int`. En conséquence, la valeur de `bootstrap.dcs` n’a pas été écrite dans la clé `/config` par la suite.

- Détecter et résoudre les incohérences entre la clé `/sync` et `synchronous_standby_names` (Alexander Kukushkin)

  Par défaut, Patroni met à jour `/sync` et `synchronous_standby_names` dans un ordre très précis, mais en cas de bug ou lorsque quelqu’un réinitialise manuellement `synchronous_standby_names`, Patroni pouvait entrer dans un état incohérent. En conséquence, il était possible que le basculement se produise sur un nœud asynchrone.

- Lire les valeurs des paramètres GUC lors de la connexion à une instance Postgres en cours d'exécution (Alexander Kukushkin)

  Lorsqu’il est redémarré en [pause](/fr/patroni/pause#pause), Patroni supprimait le paramètre GUC `synchronous_standby_names` provenant de `postgresql.conf`. Pour résoudre ce problème et éviter des situations similaires, Patroni lira la valeur du GUC s’il rejoint un serveur Postgres déjà en cours d’exécution.

- Supprimé les avertissements ennuyeux lors de la vérification de l'unicité du nœud (Alexander Kukushkin)

  Les messages `WARNING` sont générés par `urllib3` si Patroni est redémarré rapidement.

--------

## Version 3.1.1 {#version-311}

Sorti le 2023-09-20

**Correctifs de bogues**

- Réinitialiser l'état du mode de secours lors de la promotion (ChenChangAo)

  Si un basculement planifié ou un basculement s'est produit peu de temps après l'activation du mode de secours, le nouveau primaire promu se rétrogradait lui-même une fois le mode de secours redevenu inactif.

- Supprimez les avertissements inutiles dans [patronictl](/fr/patroni/patronictl#patronictl) (Alexander Kukushkin)

  Si [patronictl](/fr/patroni/patronictl#patronictl) utilise le même fichier patroni.yaml que Patroni et peut accéder au répertoire `PGDATA`, il se peut qu’il affiche des avertissements gênants concernant des valeurs incorrectes dans la configuration globale.

- Activer explicitement le mode synchrone dans un cas particulier (Alexander Kukushkin)

  Le mode synchrone n’a effectivement jamais été activé s’il n’y a aucune réplique en cours de diffusion depuis le primaire.

- Correctif d'un bogue lié à la validation des valeurs entières `0` (Israel Barth Rubio)

  Dans la plupart des cas, cela n’a causé aucun problème, seulement des avertissements.

- Ne pas renvoyer les slots logiques pour le cluster de secours (Alexander Kukushkin)

  Patroni ne peut pas créer de slots de réplication logique dans le cluster de secours, ces derniers doivent donc être ignorés s’ils sont définis dans la configuration globale.

- Éviter d'afficher la docstring dans la sortie de `patronictl --help` (Israel Barth Rubio)

  Le module `click` doit recevoir un indice spécial à cet effet.

- Correctif d'un bogue lié à `kubernetes.standby_leader_label_value` (Alexander Kukushkin)

  Cette fonctionnalité n’a tout simplement jamais fonctionné.

- Identifiant système du cluster retourné en sortie `patronictl list` (Polina Bungina)

  Le problème a été introduit lors de la mise en œuvre du support de Citus, où il fallait masquer l'identifiant car il diffère entre le coordinateur et tous les workers.

- Remplacer la méthode `write_leader_optime` dans l'implémentation Kubernetes (Alexander Kukushkin)

  La méthode doit écrire le LSN d'arrêt sur l'Endpoint/ConfigMap du leader lorsque aucune réplique saine n'est disponible pour devenir le nouveau primaire.

- Ne pas démarrer PostgreSQL arrêté en mode pause (Alexander Kukushkin)

  En raison d'une condition de course, Patroni supposait à tort que le standby devait être redémarré car certains paramètres de récupération (`primary_conninfo` ou similaires) avaient été modifiés.

- Correctif d'un bogue dans la commande `patronictl query` (Israel Barth Rubio)

  Ça n’a pas fonctionné lorsque seul l’argument `-m` a été fourni ou lorsque ni `-r` ni `-m` n’ont été fournis.

- Traiter correctement les paramètres entiers utilisés dans la ligne de commande pour démarrer postgres (Polina Bungina)

  Si les valeurs sont fournies sous forme de chaînes de caractères et non converties en entier, cela entraînait un calcul incorrect de `max_prepared_transactions` basé sur `max_connections` pour les clusters Citus.

- Ne comptez pas sur `pg_stat_wal_receiver` pour déterminer `pg_rewind` (Alexander Kukushkin)

  Il se peut que le timeline rapporté par `received_tli` depuis `pg_stat_wal_receiver` soit en avance par rapport au timeline réellement rejoué, tandis que le timeline rapporté par `IDENTIFY_SYSTEM` via la connexion de réplication est toujours correct.

--------

## Version 3.1.0 {#version-310}

Sorti le 2023-08-03

**Modifications non rétrocompatibles**

- Modifié le sens sémantique de `restapi.keyfile` et `restapi.certfile` (Alexander Kukushkin)

  Précédemment, Patroni utilisait `restapi.keyfile` et `restapi.certfile` comme certificats clients en tant que mécanisme de secours si aucun paramètre de configuration respective n'était présent dans la section `ctl`.

> [!WARNING]
> Si vous avez activé la validation des certificats clients (`restapi.verify_client` est défini sur `required`), vous devez également fournir des **certificats clients valides** dans `ctl.certfile`, `ctl.keyfile`, `ctl.keyfile_password`. En l'absence de ces certificats, Patroni ne fonctionnera pas correctement.

**Nouvelles fonctionnalités**

- Rendre le libellé du rôle du Pod configurables (Waynerv)

  Les valeurs peuvent être personnalisées à l’aide des paramètres `kubernetes.leader_label_value`, `kubernetes.follower_label_value` et `kubernetes.standby_leader_label_value`. Cette fonctionnalité sera particulièrement utile lorsque nous modifierons le rôle `master` en `primary`. Vous trouverez davantage d’informations sur cette fonctionnalité et les étapes de migration [ici](/fr/patroni/kubernetes#kubernetes_role_values).

**Améliorations**

- Diverses améliorations apportées à `patroni --validate-config` (Alexander Kukushkin)

  Validation améliorée des paramètres pour différents DCS et pour les sections `bootstrap.dcs`, `ctl`, `restapi` et [watchdog](/fr/patroni/watchdog#watchdog).

- Démarrer PostgreSQL hors mode récupération s’il a subi une panne pendant la récupération alors que Patroni est en cours d'exécution (Alexander Kukushkin)

  Il peut réduire le temps de récupération et aidera à éviter des incréments inutiles de la timeline.

- Éviter les mises à jour inutiles de la clé `/status` (Alexander Kukushkin)

  Lorsqu’aucune slot logique permanente n’est présente, Patroni mettait à jour `/status` à chaque boucle de battement de cœur, même lorsque le LSN sur le primaire ne progressait pas.

- Interdire à un primaire obsolète de remporter la course au leader (Alexander Kukushkin)

  Si Patroni était en suspens pendant une durée importante en raison d'un manque de ressources, il vérifiera en outre qu'aucun autre nœud n'a promu PostgreSQL avant d'acquérir le verrou de leader.

- Affichage de la visibilité de la validation de certains paramètres PostgreSQL (Alexander Kukushkin, Feike Steenbergen)

  Si la validation de `max_connections`, `max_wal_senders`, `max_prepared_transactions`, `max_locks_per_transaction`, `max_replication_slots` ou `max_worker_processes` a échoué, Patroni utilisait auparavant une valeur par défaut raisonnable. À présent, en plus de cela, un avertissement sera également affiché.

- Définir les autorisations pour les fichiers et répertoires créés dans `PGDATA` (Alexander Kukushkin)

  Tous les fichiers créés par Patroni avaient uniquement des permissions de lecture/écriture pour le propriétaire. Ce comportement empêchait les outils de sauvegarde s'exécutant sous un utilisateur différent et s'appuyant sur les permissions de lecture par groupe. Patroni respecte désormais les permissions sur `PGDATA` et définit correctement les permissions sur tous les répertoires et fichiers qu'il crée à l'intérieur de `PGDATA`.

**Correctifs de bogues**

- Exécuter `archive_command` via le shell (Waynerv)

  Patroni peut archiver certains segments WAL avant d'effectuer une récupération d'incident en mode utilisateur unique ou avant `pg_rewind`. Si la commande d'archivage contient des opérateurs de shell, comme `&&`, elle ne fonctionnait pas avec Patroni.

- Corrigé les vérifications d'arrêt « en cas de basculement planifié » (Polina Bungina)

  Il se peut que le candidat spécifié soit toujours en cours de diffusion et n’ait pas reçu le point de contrôle d’arrêt, mais que la clé du leader ait été supprimée car d’autres nœuds étaient sains.

- Corrigé la vérification « est primaire » (Alexander Kukushkin)

  Pendant la course au leader, les répliques n’ont pas pu détecter que PostgreSQL sur l’ancien leader était toujours en cours d’exécution en tant que primaire.

- Corrigé `patronictl list` (Alexander Kukushkin)

  Le champ Nom du cluster était absent dans les formats de sortie `tsv`, `json` et `yaml`.

- Comportement corrigé de `pg_rewind` après pause (Alexander Kukushkin)

  Dans certains cas, Patroni n’a pas pu réintégrer le faux primaire au cluster avec `pg_rewind` après la sortie du mode maintenance.

- Corrigé un bogue dans l'implémentation etcd v3 (Alexander Kukushkin)

  Invalider le cache KV interne si une mise à jour de clé utilisant les champs `create_revision`/`mod_revision` échoue en raison d’un désaccord de révision.

- Comportement corrigé des répliques dans un cluster de secours en pause (Alexander Kukushkin)

  Lorsque la clé du leader expire, les répliques du cluster de secours ne suivront plus le nœud distant, mais conserveront `primary_conninfo` tel quel.

--------

## Version 3.0.4 {#version-304}

Publié le 2023-07-13

**Nouvelles fonctionnalités**

- Rendre le statut de réplication des nœuds secondaires visible (Alexander Kukushkin)

  Pour PostgreSQL 9.6+, Patroni signalera l'état de réplication comme `streaming` lorsque le nœud secondaire diffuse depuis l'autre nœud, ou comme `in archive recovery` lorsqu'aucune connexion de réplication n'est établie et que `restore_command` est défini. Cet état est visible dans les clés `member` du DCS, dans l'API REST et dans la sortie de `patronictl list`.

**Améliorations**

- Messages d'erreur améliorés avec etcd v3 (Alexander Kukushkin)

  Lorsque le cluster etcd v3 n'est pas accessible, Patroni signale qu'il ne parvient pas à accéder aux points d'entrée `/v2`.

- Utilisez la lecture en quorum dans [patronictl](/fr/patroni/patronictl#patronictl) si cela est possible (Alexander Kukushkin)

  Les clusters etcd ou Consul pourraient être dégradés en lecture seule, mais du point de vue de [patronictl](/fr/patroni/patronictl#patronictl) tout semblait fonctionner correctement. Ce comportement va maintenant entraîner une erreur.

- Empêcher les scénarios de split-brain dus à des noms en double dans la configuration (Mark Pekala)

  Lors du démarrage, Patroni vérifie si un nœud portant le même nom est enregistré dans le DCS, puis tente de consulter son API REST. Si l'API REST est accessible, Patroni s'arrête avec une erreur. Cela permet de prévenir les erreurs humaines.

- Démarrer PostgreSQL hors mode récupération s'il s'est arrêté brutalement pendant que Patroni était en cours d'exécution (Alexander Kukushkin)

  Il peut réduire le temps de récupération et éviter des incréments inutiles de la timeline.

**Correctifs de bogues**

- Le certificat SSL de l'API REST n'a pas été rechargé lors de la réception d'un SIGHUP (Israel Barth Rubio)

  La régression a été introduite dans la version 3.0.3.

- Correction de la validation des GUC entiers pour des paramètres tels que `max_connections` (Feike Steenbergen)

  Patroni n'acceptait pas les valeurs numériques entre guillemets. Une régression a été introduite à partir de la version 3.0.3.

- Corriger le problème lié à [synchronous_mode](/fr/patroni/replication_modes#synchronous_mode) (Alexander Kukushkin)

  Exécutez `txid_current()` avec `synchronous_commit=off` afin qu’il ne patiente pas accidentellement pour des répliques synchrones absentes lorsque `synchronous_mode_strict` est activé.

--------

## Version 3.0.3 {#version-303}

Publié le 2023-06-22

**Nouvelles fonctionnalités**

- Compatibilité avec PostgreSQL 16 beta1 (Alexander Kukushkin)

  Règles étendues de validation des paramètres GUC.

- Rendre le validateur des paramètres GUC de PostgreSQL extensible (Israel Barth Rubio)

  Les règles de validation sont chargées à partir de fichiers YAML situés dans le répertoire `patroni/postgresql/available_parameters/`. Les fichiers sont ordonnés par ordre alphabétique et appliqués les uns après les autres. Cela permet d'associer des validateurs personnalisés aux distributions non standards de Postgres.

- Ajout de l'option `restapi.request_queue_size` (Andrey Zhidenkov, Aleksei Sukhov)

  Définit la taille de la file d'attente des requêtes pour la socket TCP utilisée par l'API REST de Patroni. Dès que la file est pleine, les requêtes supplémentaires reçoivent une erreur « Connection denied ». La valeur par défaut est 5.

- Appeler `initdb` directement lors de l'initialisation d'un nouveau cluster (Matt Baker)

  Précédemment, il était appelé via `pg_ctl`, ce qui nécessitait une mise entre guillemets particulière des paramètres passés à `initdb`.

- Ajout d'un hook avant l'arrêt (Le Duane)

  Le hook peut être configuré via `postgresql.before_stop` et s'exécute juste avant `pg_ctl stop`. Le code de sortie n'a pas d'impact sur le processus d'arrêt.

- Ajout de la prise en charge des noms personnalisés pour les binaires Postgres (Israel Barth Rubio, Polina Bungina)

  Lorsqu’un déploiement Postgres personnalisé est utilisé, il se peut que les binaires Postgres soient compilés avec des noms différents de ceux utilisés par la distribution communautaire. Les noms binaires personnalisés peuvent être configurés à l’aide des paramètres de configuration `postgresql.bin_name.*` et des variables d’environnement `PATRONI_POSTGRESQL_BIN_*`.

**Améliorations**

- Plusieurs améliorations apportées à `patroni --validate-config` (Polina Bungina)

  - Rendre `bootstrap.initdb` facultatif. Il n'est requis que pour les nouveaux clusters, mais `patroni --validate-config` signalait une erreur si ce paramètre manquait dans la configuration.
  - Ne pas générer d'erreur lorsque `postgresql.bin_dir` est vide ou non défini. Essayer d'abord de localiser les binaires Postgres dans le PATH par défaut.
  - Rendre la section `postgresql.authentication.rewind` facultative. Si elle est absente, Patroni utilise le superutilisateur.

- Rapport d'erreurs amélioré dans [patronictl](/fr/patroni/patronictl#patronictl) (Israel Barth Rubio)

  Le symbole `\n` a été affiché tel quel, au lieu du symbole de saut de ligne réel.

**Correctifs de bogues**

- Correctif apporté à la prise en charge de Citus (Alexander Kukushkin)

  Si l'appel à l'API REST effectué par le worker promu vers le coordinateur échouait pendant un basculement planifié, le groupe Citus donné restait bloqué pendant une durée indéfinie.

- Autoriser l'URL `etcd3` dans l'option `--dcs-url` de [patronictl](/fr/patroni/patronictl#patronictl) (Israel Barth Rubio)

  Si les utilisateurs tentaient de passer une URL `etcd3` via l'option `--dcs-url` de [patronictl](/fr/patroni/patronictl#patronictl), ils rencontreraient une exception.

--------

## Version 3.0.2 {#version-302}

Publié le 2023-03-24

> [!WARNING]
> La version 3.0.2 a cessé de prendre en charge les versions de Python antérieures à 3.6.

**Nouvelles fonctionnalités**

- Ajout de l'état de réplique synchrone au point de terminaison `/metrics` (Thomas von Dein, Alexander Kukushkin)

  Avant, seul le rapport `primary`/`standby_leader`/`replica` était effectué.

- Gestion conviviale de `PAGER` dans [patronictl](/fr/patroni/patronictl#patronictl) (Israel Barth Rubio)

  Il rend le pageur configurable via la variable d'environnement `PAGER`, qui remplace `less` et `more` par défaut.

- Rendre le code d'état HTTP réessayable configurable dans K8s (Alexander Kukushkin)

  Sur certaines plates-formes gérées, il est possible d'obtenir le code d'état `401 Unauthorized`, qui est parfois résolu après quelques tentatives supplémentaires.

**Améliorations**

- Pendant l’amorçage personnalisé, ne définir `hot_standby` sur `off` que si `recovery_target_action` est défini sur `promote` (Alexander Kukushkin)

  Il était nécessaire de faire fonctionner `recovery_target_action=pause` correctement.

- Interdire au rappel `on_reload` de tuer d'autres rappels (Alexander Kukushkin)

  `on_start`/`on_stop`/`on_role_change` sont généralement utilisés pour ajouter/supprimer une adresse IP virtuelle, et `on_reload` ne doit pas y interférer.

- Passé à `IMDSFetcher` dans l'exemple de script de rappel AWS (Polina Bungina)

  Le `IMDSv2` nécessite un jeton pour fonctionner, et le `IMDSFetcher` le gère de manière transparente.

**Correctifs de bogues**

- Correctif apporté à `patronictl switchover` sur un cluster Citus exécutant sur Kubernetes (Lukáš Lalinský)

  Ça n’a pas fonctionné pour les espaces de noms différents de `default`.

- N'écrivez pas dans `PGDATA` si la version majeure n'est pas connue (Alexander Kukushkin)

  Si immédiatement après le démarrage, `PGDATA` était vide (peut-être pas encore monté), Patroni effectuait une supposition erronée sur la version de PostgreSQL et créait de façon erronée le fichier `recovery.conf`, même si la version majeure réelle est v10+.

- Correction d'un bug lié aux métadonnées Citus après un basculement du coordinateur (Alexander Kukushkin)

  L'appel `citus_set_coordinator_host()` ne provoque pas de synchronisation des métadonnées et le changement est resté invisible sur les nœuds worker. Ce problème est résolu en passant à `citus_update_node()`.

- Utilisez les hôtes etcd répertoriés dans le fichier de configuration comme solution de repli lorsque tous les nœuds etcd sont "défaillants" (Alexander Kukushkin)

  Le cluster etcd peut modifier sa topologie au fil du temps, et Patroni tente de la suivre. Si, à un moment donné, tous les nœuds deviennent inaccessibles, Patroni utilisera une combinaison de nœuds provenant de la configuration, ainsi que de la dernière topologie connue, lorsqu'il tentera de se reconnecter.

--------

## Version 3.0.1 {#version-301}

Publié le 2023-02-16

**Correctifs de bogues**

- Passez le nom de rôle approprié à un script de rappel `on_role_change`. (Alexander Kukushkin, Polina Bungina)

  Patroni avait précédemment transmis incorrectement le rôle `promoted` à un script de rappel `on_role_change` lors d'une promotion. Le nom du rôle transmis a été rétabli à `master`. Cette régression a été introduite dans la version 3.0.0.

--------

## Version 3.0.0 {#version-300}

Sorti le 2023-01-30

Cette version ajoute une intégration avec [Citus](https://www.citusdata.com) et permet de résister aux interruptions temporaires du DCS sans dégrader le rôle de primaire.

> [!WARNING]
> - La version 3.0.0 est la dernière version à supporter Python 2.7. La prochaine version supprimera le support des versions de Python antérieures à 3.7.
>
> - Le support RAFT est obsolète. Nous ferons notre possible pour le maintenir, mais nous ne garantissons ni ne prenons de responsabilité quant aux éventuels problèmes.
> - Cette version marque la première étape vers l'élimination du terme « master » au profit de « primary ». La mise à niveau vers la prochaine version majeure fonctionnera de manière fiable uniquement si vous exécutez au moins la version 3.0.0.

**Nouvelles fonctionnalités**

- Mode de secours DCS (Alexander Kukushkin, Polina Bungina)

  Si la fonctionnalité est activée, elle permet au cluster Patroni de résister aux interruptions temporaires du DCS. Vous trouverez plus de détails dans la [documentation](/fr/patroni/dcs_failsafe_mode#dcs_failsafe_mode).

- Prise en charge Citus (Alexander Kukushkin, Polina Bungina, Jelte Fennema)

  Patroni permet un déploiement et une gestion simplifiés des clusters [Citus](https://www.citusdata.com) hautement disponibles. Veuillez consulter [ici](/fr/patroni/citus#citus) pour plus d'informations.

**Améliorations**

- Supprimer les erreurs récurrentes lors de la suppression de slots de réplication inconnus mais actifs (Michael Banck)

  Patroni continuera d’écrire ces journaux, mais uniquement en mode DEBUG.

- Exécuter une seule requête de surveillance par boucle HA (Alexander Kukushkin)

  Ce n’était pas le cas si la réplication synchrone est activée.

- Conserver uniquement le répertoire de données échoué le plus récent (William Albertus Dembo)

  Si l'amorçage a échoué, Patroni renommait précédemment le dossier \$PGDATA en y ajoutant un suffixe horodaté. Désormais, ce suffixe sera `.failed` et, si un tel dossier existe, il sera supprimé avant le renommage.

- Amélioration de la vérification des connexions de réplication synchrone (Alexander Kukushkin)

  Lorsque le nouvel hôte est ajouté à `synchronous_standby_names`, il sera configuré en mode synchrone dans le DCS uniquement lorsqu'il aura rattrapé le primaire, en plus de `pg_stat_replication.sync_state = 'sync'`.

**Fonctionnalité supprimée**

- Supprimer `patronictl scaffold` (Alexander Kukushkin)

  La seule raison de sa présence était une méthode expéditive pour exécuter des clusters de secours.

--------

## Version 2.1.7 {#version-217}

Sorti le 2023-01-04

**Correctifs de bogues**

- Corrigé de petites incompatibilités avec les modules Python hérités (Alexander Kukushkin)

  Ils empêchaient la compilation ou l'exécution de Patroni sur Debian buster/Ubuntu bionic.

--------

## Version 2.1.6 {#version-216}

Sorti le 2022-12-30

**Améliorations**

- Corriger les exceptions gênantes lors de la fermeture du socket SSL (Alexander Kukushkin)

  HAProxy ferme les connexions dès qu’il reçoit le code d’état HTTP, ne laissant aucune chance à Patroni de fermer correctement la connexion SSL.

- Ajuster l'exemple de Dockerfile pour arm64 (Polina Bungina)

  Supprimer les références explicites à `amd64` et `x86_64`, ne supprimez pas `libnss_files.so.*`.

**Améliorations de sécurité**

- Forcer `search_path=pg_catalog` pour les connexions hors protocole de réplication (Alexander Kukushkin)

  Étant donné que Patroni dépend fortement des connexions en tant qu'utilisateur superutilisateur, nous souhaitons le protéger contre les attaques potentielles menées à l’aide de fonctions définies par l’utilisateur et/ou d’opérateurs dans le schéma `public` ayant le même nom et la même signature que les objets correspondants dans `pg_catalog`. Pour cela, `search_path=pg_catalog` est imposé pour toutes les connexions établies par Patroni (sauf les connexions de réplication).

- Empêcher la sauvegarde des mots de passe dans `pg_stat_statements` (Feike Steenbergen)

  Cela est réalisé en définissant `pg_stat_statements.track_utility=off` lors de la création des utilisateurs.

**Correctifs de bogues**

- Déclarer `proxy_address` comme facultatif (Denis Laxalde)

  Comme il s'agit en réalité d'une option non obligatoire.

- Améliorer le comportement de l’option insecure (Alexander Kukushkin)

  L'option `insecure` de Ctl ne fonctionnait pas correctement lorsque des certificats clients étaient utilisés pour les requêtes de l'API REST.

- Prendre la configuration du watchdog depuis `bootstrap.dcs` lors de l'amorçage du nouveau cluster (Matt Baker)

  Patroni configurait initialement le watchdog avec les valeurs par défaut lors de l'amorçage d'un nouveau cluster, plutôt que d'utiliser la configuration utilisée pour amorcer le DCS.

- Corriger le traitement des extensions de fichier lors de la recherche d'exécutables dans WIN32 (Martín Marqués)

  Ajoutez `.exe` au nom de fichier uniquement s’il ne possède pas d’extension.

- Correction de la configuration du TTL de Consul (Alexander Kukushkin)

  Nous avons utilisé `ttl/2.0` lors de la définition de la valeur sur HTTPClient, mais oublié de multiplier la valeur actuelle par 2 dans la propriété de la classe. Cela entraînait un décalage du TTL Consul de deux fois.

**Fonctionnalité supprimée**

- Supprimer `patronictl configure` (Polina Bungina)

  Il n’est plus nécessaire de créer séparément une configuration [patronictl](/fr/patroni/patronictl#patronictl).

--------

## Version 2.1.5 {#version-215}

Publié le 2022-11-28

Cette version améliore la compatibilité avec PostgreSQL 15 et déclare la prise en charge d'etcd v3 comme prête pour la production. Patroni sur Raft reste en version Bêta.

**Nouvelles fonctionnalités**

- Améliorer `patroni --validate-config` (Denis Laxalde)

  Quitter avec le code 1 si la configuration est invalide et afficher les erreurs sur stderr.

- Ne supprimez pas les slots de réplication en mode pause (Alexander Kukushkin)

  Patroni crée automatiquement ou supprime des slots de réplication physique lorsque les membres rejoignent ou quittent le cluster. En mode pause, les slots ne seront plus supprimés.

- Prise en charge de la méthode de requête `HEAD` pour les points de terminaison de surveillance (Robert Cutajar)

  Si utilisé à la place de `GET`, Patroni ne renverra que le code d’état HTTP.

- Prise en charge des tests behave sur Windows (Alexander Kukushkin)

  Émuler l’arrêt gracieux de Patroni (`SIGTERM`) sous Windows en introduisant le nouvel endpoint d’API REST `POST /sigterm`.

- Présentation de `postgresql.proxy_address` (Alexander Kukushkin)

  Il sera écrit dans la clé du membre du DCS sous la forme de `proxy_url` et pourra être utilisé utilement pour la découverte de service.

**Améliorations de stabilité**

- Appeler `pg_replication_slot_advance()` depuis un thread (Alexander Kukushkin)

  Sur les clusters chargés disposant de nombreux slots de réplication logique, l'appel `pg_replication_slot_advance()` affectait la boucle principale de haute disponibilité et pouvait entraîner l’expiration de la clé du membre.

- Archiver les WAL susceptibles de manquer avant d’appeler `pg_rewind` sur l’ancien primaire (Polina Bungina)

  Si le primaire a cessé de fonctionner et est resté hors ligne pendant une durée importante, certains fichiers WAL pourraient manquer à l’archive ainsi qu’au nouveau primaire. Il existe un risque que `pg_rewind` supprime ces fichiers WAL depuis l’ancien primaire, rendant impossible son démarrage en tant que réplica. En archivant les fichiers WAL `ready`, nous atténuons non seulement ce problème, mais améliorons également l’expérience d’archivage continu en général.

- Ignorer les erreurs `403` lors de la création du service Kubernetes (Nick Hudson, Polina Bungina)

  Patroni envoyait en continu des messages de journalisation à cause d'essais infructueux de création du service, qui pouvait déjà exister.

- Améliorer la sonde de vivacité (Alexander Kukushkin)

  La sonde de vivacité commencera à échouer si la boucle de battement de cœur s'exécute plus longtemps que `ttl` sur le serveur primaire ou `2*ttl` sur la réplique. Cela nous permettra de l'utiliser comme alternative au [watchdog](/fr/patroni/watchdog#watchdog) sur Kubernetes.

- Assurez-vous qu’uniquement le nœud synchrone tente d’acquérir le verrou lors d’un basculement planifié (Alexander Kukushkin, Polina Bungina)

  Précédemment, il existait une faible probabilité qu'un membre asynchrone à jour devienne leader si un basculement planifié était effectué sans spécifier de cible.

- Éviter le clonage pendant l'exécution de l'amorçage (Ants Aasma)

  N'autorisez pas de méthode de création de réplique qui ne nécessite pas de leader lors de l'amorçage du cluster.

- Compatibilité avec kazoo-2.9.0 (Alexander Kukushkin)

  Selon la version de Python, la méthode `SequentialThreadingHandler.select()` peut lever les exceptions `TypeError` et `IOError` si `select()` est appelée sur une socket fermée.

- Arrêter explicitement la connexion SSL avant la fermeture du socket (Alexander Kukushkin)

  Ne pas le faire a entraîné des erreurs `unexpected eof while reading` avec OpenSSL 3.0.

- Compatibilité avec `prettytable>=2.2.0` (Alexander Kukushkin)

  En raison de modifications de l'API interne, l'en-tête du nom du cluster était affiché sur la mauvaise ligne.

**Correctifs de bogues**

- Gérer le jeton expiré pour etcd lease_grant (monsterxx03)

  En cas d'erreur, obtenez un nouveau jeton et réessayez la requête.

- Corriger un bogue dans le point de terminaison `GET /read-only-sync` (Alexander Kukushkin)

  Il a été introduit dans la version précédente et n’a jamais fonctionné correctement.

- Gérer le cas où le stockage du répertoire de données a disparu (Alexander Kukushkin)

  Patroni vérifie périodiquement la présence et la non-vacuité du répertoire PGDATA, mais en cas de problème de stockage, `os.listdir()` lève l'exception `OSError`, interrompant ainsi la boucle de battement de cœur.

- Appliquer `master_stop_timeout` en attendant que les backends utilisateurs se terminent (Alexander Kukushkin)

  Quelque chose qui ressemble à un backend utilisateur pourrait en réalité être un worker en arrière-plan (par exemple, Citus Maintenance Daemon) qui échoue à s'arrêter.

- Accepter `*:<port>` pour `postgresql.listen` (Denis Laxalde)

  Le `patroni --validate-config` se plaignait de son invalidité.

- Correction des délais d'attente dans Raft (Alexander Kukushkin)

  Lorsque Patroni ou patronictl démarrent, ils tentent d'obtenir la topologie du cluster Raft à partir des membres connus. Ces appels étaient effectués sans délais d'attente appropriés.

- Mettre à jour de force le service Consul si le jeton a été modifié (John A. Lotoski)

  Ne pas le faire entraîne des erreurs « rpc error making call: rpc error making call: ACL not found ».

--------

## Version 2.1.4 {#version-214}

Sorti le 2022-06-01

**Nouvelles fonctionnalités**

- Améliorer le comportement de `pg_rewind` sur les systèmes Debian/Ubuntu classiques (Gunnar "Nick" Bluth)

  Dans les installations PostgreSQL qui situent `postgresql.conf` en dehors du répertoire de données (par exemple, les paquets Ubuntu/Debian), `pg_rewind --restore-target-wal` échoue à déterminer la valeur du champ `restore_command`.

- Autoriser la définition de `TLSServerName` dans les vérifications de service Consul (Michael Gmelin)

  Utile lorsque les vérifications sont effectuées par adresse IP et que le `node_name` Consul n'est pas un FQDN.

- Ajout de la prise en charge de `ppc64le` dans le watchdog (Jean-Michel Scheiwiler)

  Et correction de la prise en charge du watchdog sur certaines plates-formes non-x86.

- Passé le rappel aws.py de `boto` à `boto3` (Alexander Kukushkin)

> `boto` 2.x est abandonné depuis 2018 et échoue avec Python 3.9.

- Actualiser périodiquement le jeton du compte de service sur K8s (Haitao Li)

  Depuis la version Kubernetes v1.21, les jetons de compte de service expirent au bout de 1 heure.

- Ajout du point de terminaison de surveillance `/read-only-sync` (Dennis4b)

  Il est similaire à `/read-only` mais inclut uniquement les répliques synchrones.

**Améliorations de stabilité**

- Ne copiez pas le slot de réplication logique vers une réplique si une incompatibilité de configuration est détectée dans la configuration de décodage logique avec le serveur primaire (Alexander Kukushkin)

  Une réplique ne copiera plus un slot de réplication logique depuis le serveur primaire si ce slot ne correspond pas aux options de configuration `plugin` ou `database`. Auparavant, la vérification de correspondance avec ces options de configuration n'était pas effectuée avant que la réplique n'ait copié le slot et n'ait démarré avec, ce qui entraînait des redémarrages inutiles et répétés.

- Traitement particulier des paramètres de configuration de récupération pour PostgreSQL v12+ (Alexander Kukushkin)

  Lors du démarrage en tant que réplique, Patroni doit pouvoir mettre à jour `postgresql.conf` et redémarrer/recharger si l'adresse du leader a changé, en conservant les valeurs actuelles des paramètres au lieu de les interroger auprès de `pg_settings`.

- Meilleure gestion des adresses IPv6 dans les paramètres `postgresql.listen` (Alexander Kukushkin)

  Étant donné que le paramètre `listen` comporte un port, les utilisateurs tentent de placer des adresses IPv6 entre crochets, ce qui n'est pas correctement supprimé lorsque la liste contient plus d'une adresse.

- Utilisez les identifiants `replication` uniquement lors de la vérification de divergence sur PostgreSQL v10 et les versions antérieures (Alexander Kukushkin)

  Si `rewind` est activé, Patroni utilisera à nouveau les identifiants `superuser` ou `rewind` sur les versions récentes de Postgres.

**Correctifs de bogues**

- Corrigé l'importation manquante de `dateutil.parser` (Wesley Mendes)

  Les tests n’échouaient que grâce à l’importation de `dateutil.parser` depuis d’autres modules.

- Vérifiez que l'annotation `optime` est une chaîne de caractères (Sebastian Hasler)

  Dans certains cas, Patroni tentait de le passer comme une valeur numérique.

- Meilleure gestion de l'échec de tentative `pg_rewind` (Alexander Kukushkin)

  Si le primaire devient indisponible pendant `pg_rewind`, `$PGDATA` sera laissé dans un état corrompu. À ce stade, Patroni supprimera le répertoire de données, même si cette action n'est pas autorisée par la configuration.

- Ne supprimez pas les annotations `slots` du leader `ConfigMap`/`Endpoint` lorsque PostgreSQL n'est pas prêt (Alexander Kukushkin)

  Si la valeur `slots` n'est pas fournie, l'annotation conserve la valeur actuelle.

- Gérer le problème de concurrence avec les observateurs API Kubernetes (Alexander Kukushkin)

  Dans certains cas (inconnus), les observateurs pourraient devenir obsolètes ; en conséquence, la méthode `attempt_to_acquire_leader()` pourrait échouer en raison du code d’état HTTP 409. Dans ce cas, nous réinitialisons les connexions des observateurs et recommençons depuis le début.

--------

## Version 2.1.3 {#version-213}

Sorti le 2022-02-18

**Nouvelles fonctionnalités**

- Ajout du support des clés TLS chiffrées pour [patronictl](/fr/patroni/patronictl#patronictl) (Alexander Kukushkin)

  Il peut être configuré via le paramètre de configuration `ctl.keyfile_password` ou la variable d'environnement `PATRONI_CTL_KEYFILE_PASSWORD`.

- Ajout de métriques supplémentaires au point de terminaison /metrics (Alexandre Pereira)

  Spécifiquement, `patroni_pending_restart` et `patroni_is_paused`.

- Permettre de spécifier plusieurs hôtes dans la configuration du cluster de secours (Michael Banck)

  Si le cluster de secours est en réplication depuis le cluster Patroni, il peut être utile de s'appuyer sur le basculement côté client, disponible dans `libpq` depuis PostgreSQL v10. Cela consiste à utiliser `primary_conninfo` sur le leader du cluster de secours et le paramètre `pg_rewind` dans la chaîne de connexion avec `target_session_attrs=read-write`. Le fichier `pgpass` sera généré avec plusieurs lignes (une ligne par hôte), et au lieu d'appeler `CHECKPOINT` sur les nœuds du cluster primaire, le cluster de secours attendra que `pg_control` soit mis à jour.

**Améliorations de stabilité**

- Compatibilité avec les versions anciennes de `psycopg2` (Alexander Kukushkin)

  Par exemple, le `psycopg2` installé à partir des paquets Ubuntu 18.04 ne possède pas encore l'exception `UndefinedFile`.

- Redémarrez l'observateur `etcd3` si aucun nœud etcd ne répond (Alexander Kukushkin)

  Si le watcher est actif, la méthode `get_cluster()` continue de renvoyer des informations périmées, même si tous les nœuds etcd échouent.

- Ne supprimez pas le verrou du leader dans le cluster de secours pendant la mise en pause (Alexander Kukushkin)

  Précédemment, le verrou était maintenu uniquement par le nœud en cours d'exécution en tant que leader primaire et non en tant que leader de secours.

**Correctifs de bogues**

- Correctif d'un bogue dans l'amorçage du leader de secours (Alexander Kukushkin)

  Patroni considérait l'amorçage comme échoué si PostgreSQL n'acceptait pas les connexions après 60 secondes. Ce bug a été introduit dans la version 2.1.2.

- Correctif d'un bug lié au basculement vers un serveur secondaire en cascade (Alexander Kukushkin)

  Lors de la détermination des slots à créer sur un standby en cascade, nous avons oublié de tenir compte du fait que le leader pourrait être absent.

- Corrigé de petits problèmes dans le validateur de configuration de Postgres (Alexander Kukushkin)

  Les paramètres entiers introduits dans PostgreSQL v14 échouaient à être validés car les valeurs min et max étaient entre guillemets dans le validator.py

- Utiliser les identifiants de réplication lors de la vérification de l'état de leader (Alexander Kukushkin)

  Il se peut que `remove_data_directory_on_diverged_timelines` soit défini, mais que `rewind_credentials` ne soit pas défini et que l'accès en superutilisateur entre les nœuds ne soit pas autorisé.

- Corrigé l'erreur « port en cours d'utilisation » lors du remplacement du certificat de l'API REST (Ants Aasma)

  Lors du changement de certificats, une condition de course existait avec une requête API concurrente. Si une requête est active pendant la période de remplacement, la substitution échoue avec une erreur « port en cours d'utilisation » et Patroni se retrouve bloqué dans un état sans serveur API actif.

- Corrigé un bug lors de l'amorçage du cluster si les mots de passe contiennent des caractères `%` (Bastien Wirtz)

  La méthode d'amorçage exécute le bloc `DO`, avec tous les paramètres correctement encadrés de guillemets, mais la méthode `cursor.execute()` n'apprécie pas une liste vide lorsque des paramètres sont passés.

- Corrigé l'exception « AttributeError: no attribute 'leader' » (Hrvoje Milković)

  Cela peut survenir si le mode synchrone est activé et que le contenu DCS a été effacé.

- Corriger le bogue dans la vérification du timeline de divergence (Alexander Kukushkin)

  Patroni supposait à tort que les timelines avaient divergé. Cela n'avait pas d'impact pour pg_rewind, mais si pg_rewind n'est pas autorisé et que `remove_data_directory_on_diverged_timelines` est défini, cela a entraîné une réinitialisation du précédent leader.

--------

## Version 2.1.2 {#version-212}

Sorti le 2021-12-03

**Nouvelles fonctionnalités**

- Compatibilité avec `psycopg>=3.0` (Alexander Kukushkin)

  Par défaut, `psycopg2` est privilégié. `psycopg>=3.0` est utilisé uniquement si `psycopg2` n'est pas disponible ou si sa version est trop ancienne.

- Ajouter le champ `dcs_last_seen` à l'API REST (Michael Banck)

  Ce champ indique la dernière heure (en époque Unix) à laquelle un membre du cluster a communiqué avec succès avec le DCS. Cela permet d'identifier et/ou d'analyser les partitions réseau.

- Libérer le verrou de leader lorsque `pg_controldata` signale « shut down » (Alexander Kukushkin)

  Pour résoudre le problème de basculement planifié ou d'arrêt lent lorsque `archive_command` est lent ou défaillant, Patroni supprimera immédiatement la clé leader après que `pg_controldata` aura signalé que PGDATA est `shut down` de manière propre et qu’il aura vérifié qu’au moins une réplique a reçu toutes les modifications. Si aucune réplique ne remplit cette condition, la clé leader n’est pas supprimée et le comportement précédent est conservé, c’est-à-dire que Patroni continuera à mettre à jour le verrou.

- Ajouter la prise en charge du paramètre de connexion `sslcrldir` (Kostiantyn Nemchenko)

  Le paramètre de connexion nouvellement introduit est disponible à partir de PostgreSQL v14.

- Autoriser la définition de listes de contrôle d'accès (ACL) pour les ZNodes dans Zookeeper (Alwyn Davis)

  Introduisez une nouvelle option de configuration `zookeeper.set_acls` afin que Kazoo applique une liste de contrôle d'accès par défaut à chaque ZNode qu'il crée.

**Améliorations de stabilité**

- Reporte l'essai suivant de récupération jusqu'à la prochaine boucle HA (Alexander Kukushkin)

  Si PostgreSQL s'est arrêté de manière inattendue en raison d'un espace disque insuffisant (par exemple), et qu'il ne parvient pas à démarrer, Patroni tente de le récupérer de manière trop impétueuse, ce qui provoque une surcharge des journaux.

- Ajouter un journal avant la démotion, qui peut prendre un certain temps (Michael Banck)

  La démotion peut prendre un certain temps, et il n’est pas toujours évident, en consultant les journaux, ce qui se passe réellement.

- Améliorer les messages d'état « I am » (Michael Banck)

  `no action. I am a secondary ({0})` vs `no action. I am ({0}), a secondary`

- Conversion en entier `wal_keep_segments` lors de la conversion en `wal_keep_size` (Jorge Solórzano)

  Il est possible de définir `wal_keep_segments` sous forme de chaîne dans la [configuration dynamique](/fr/patroni/config/dynamic#dynamic) globale. Python étant un langage à typage dynamique, la chaîne était simplement multipliée. Par exemple, `wal_keep_segments: "100"` était converti en `100100100100100100100100100100100100100100100100MB`.

- Autoriser le basculement planifié uniquement vers des nœuds synchrones lorsque la réplication synchrone est activée (Alexander Kukushkin)

  En outre, un nœud ne participe à l’élection du leader que face à des nœuds synchrones connus.

- Utiliser le rôle mis en cache comme solution de secours lorsque Postgres est lent (Alexander Kukushkin)

  Dans certains cas extrêmes, PostgreSQL pourrait être tellement lent que la requête normale de surveillance ne s’achève pas en quelques secondes. Une gestion incorrecte de l’exception `statement_timeout` pourrait entraîner une situation où PostgreSQL n’était pas rétrogradé à temps lorsque la clé leader expire ou en cas d’échec de mise à jour. En cas d’une telle exception, Patroni utilisera le cache `role` pour déterminer si PostgreSQL est en cours d’exécution en tant que primaire.

- Éviter les mises à jour inutiles du ZNode membre (Alexander Kukushkin)

  Si aucune valeur n’a changé dans les données des membres, la mise à jour ne doit pas avoir lieu.

- Optimiser le point de contrôle après promotion (Alexander Kukushkin)

  Évitez d'exécuter `CHECKPOINT` si la dernière timeline est déjà stockée dans `pg_control`. Cela permet d'éviter des `CHECKPOINT` inutiles juste après l'initialisation du nouveau cluster avec `initdb`.

- Privilégier les membres sans `nofailover` lors du choix des nœuds de synchronisation (Alexander Kukushkin)

  Précédemment, les nœuds synchrones étaient sélectionnés uniquement en fonction du retard de réplication, ce qui signifiait que le nœud portant l'étiquette `nofailover` avait les mêmes chances de devenir synchrone qu'un autre nœud. Ce comportement était à la fois ambigu et dangereux, car en cas de défaillance du primaire, le basculement ne pouvait pas avoir lieu automatiquement.

- Supprimer les hôtes en double du cache machine etcd (Michael Banck)

  Les URL clientes annoncées dans le cluster etcd pourraient être mal configurées. Supprimer les doublons dans Patroni dans ce cas constitue une amélioration facile à mettre en œuvre.

**Correctifs de bogues**

- Ignorer les slots de réplication temporaires lors de la gestion des slots (Alexander Kukushkin)

  À compter de la version 10, `pg_basebackup` crée une slot de réplication temporaire pour le streaming WAL, et Patroni tentait de la supprimer car le nom de la slot semblait inconnu. Pour résoudre ce problème, nous ignorons toutes les slots temporaires lors de la requête de la vue `pg_replication_slots`.

- Assurez-vous que `pg_replication_slot_advance()` ne dépasse pas son délai d’exécution (Alexander Kukushkin)

  Patroni utilisait le `statement_timeout` par défaut dans ce cas, et une fois l'appel échoué, les chances de récupération sont très faibles, ce qui entraîne une augmentation de la taille de `pg_wal` et du bloat de `pg_catalog`.

- Le `/status` n'a pas été mis à jour lors de la rétrogradation (Alexander Kukushkin)

  Après la rétrogradation de PostgreSQL, l'ancien leader met à jour le dernier LSN dans le DCS. À compter de `2.1.0`, la nouvelle clé `/status` a été introduite, mais l'optime a continué à être écrit dans `/optime/leader`.

- Gérer les exceptions DCS lors de la rétrogradation (Alexander Kukushkin)

  Lors de la rétrogradation du maître en raison de l'échec de mise à jour du verrou leader, il se peut que le DCS tombe complètement et que l'appel à `get_cluster()` lève une exception. En l'absence d'un traitement approprié, cela entraîne l'arrêt prolongé de Postgres jusqu'à la récupération du DCS.

- Le `use_unix_socket_repl` ne fonctionnait pas dans certains cas (Alexander Kukushkin)

  Spécifiquement, si `postgresql.unix_socket_directories` n’est pas défini. Dans ce cas, Patroni doit utiliser la valeur par défaut de `libpq`.

- Corriger quelques problèmes liés à l'API REST de Patroni (Alexander Kukushkin)

  Le champ `clusters_unlocked` peut parfois ne pas être défini, ce qui entraîne des exceptions dans le point de terminaison `GET /metrics`. En outre, la méthode de gestion des erreurs supposait que le tuple `connect_address` possédait toujours deux éléments, alors qu'il peut en contenir davantage en cas d'adresse IPv6.

- Attendez que le nœud nouvellement promu ait terminé la récupération avant de décider d'effectuer un rewind (Alexander Kukushkin)

  La promotion effective peut prendre un certain temps, ainsi que la création de la nouvelle timeline. En l'absence d'attente, les répliques pourraient en venir à la conclusion qu'un retour en arrière n'est pas nécessaire.

- Gérer les timelines manquantes dans un fichier d'historique lors de la décision d'effectuer un rewind (Alexander Kukushkin)

  Si la ligne temporelle de la réplique actuelle est absente du fichier d'historique sur le serveur primaire, la réplique supposait à tort qu'un rewind n'était pas nécessaire.

--------

## Version 2.1.1 {#version-211}

Sorti le 2021-08-19

**Nouvelles fonctionnalités**

- Prise en charge du suffixe de nom SRV etcd (David Pavlicek)

  etcd permet de distinguer plusieurs clusters etcd situés sous le même domaine, et Patroni le prend désormais en charge.

- Enrichir l'historique avec le nouveau leader (huiyalin525)

  Il ajoute la nouvelle colonne à la sortie `patronictl history`.

- Rendre le bundle CA configurable pour la configuration Kubernetes intra-cluster (Aron Parsons)

  Par défaut, Patroni utilise `/var/run/secrets/kubernetes.io/serviceaccount/ca.crt` et cette nouvelle fonctionnalité permet de spécifier un `kubernetes.cacert` personnalisé.

- Prise en charge de l'inscription/désinscription dynamique en tant que service Consul et du changement d'étiquettes (Tommy Li)

  Un redémarrage de Patroni était auparavant nécessaire.

**Correctifs de bogues**

- Éviter un rechargement inutile de l'API REST (Alexander Kukushkin)

  La version précédente a ajouté la fonctionnalité de recharger les certificats de l'API REST en cas de modification sur le disque. Malheureusement, le rechargement s'effectuait de manière inconditionnelle juste après le démarrage.

- Ne pas résoudre les membres du cluster lorsque `etcd.use_proxies` est défini (Alexander Kukushkin)

  Lors du démarrage, Patroni vérifie l’état du cluster etcd en interrogeant la liste des membres. En outre, il tente également de résoudre les noms d’hôte, ce qui n’est pas nécessaire lors de l’utilisation d’etcd via un proxy et provoquait des avertissements inutiles.

- Ignorer les lignes comportant des valeurs NULL dans `pg_stat_replication` (Alexander Kukushkin)

  Il semble que la vue `pg_stat_replication` puisse contenir des valeurs NULL dans les champs `replay_lsn`, `flush_lsn` ou `write_lsn` même lorsque `state = 'streaming'` est défini.

--------

## Version 2.1.0 {#version-210}

Publié le 2021-07-06

Cette version ajoute la compatibilité avec PostgreSQL v14, permet aux slots de réplication logique de persister lors d’un basculement ou d’un basculement planifié, implémente le support de la liste autorisée pour l’API REST, et réduit le nombre de journaux à une seule ligne par battement de cœur.

**Nouvelles fonctionnalités**

- Compatibilité avec PostgreSQL v14 (Alexander Kukushkin)

  Reprendre la relecture du WAL si Patroni n'est pas en mode « pause » lui-même. La relecture pourrait être en « pause » en raison d'un changement de certains paramètres, par exemple `max_connections` sur le primaire.

- Basculement des slots logiques (Alexander Kukushkin)

  Activer la persistance des slots de réplication logique lors d’un basculement ou d’un basculement planifié sur PostgreSQL v11+. Le slot de réplication est copié depuis le serveur primaire vers la réplique avec un redémarrage, puis la fonction [pg_replication_slot_advance()](https://www.postgresql.org/docs/11/functions-admin.html#id-1.5.8.31.8.5.2.2.8.1.1) est utilisée pour le faire avancer. En conséquence, le slot existe déjà avant le basculement, et aucun événement ne devrait être perdu, mais il existe une possibilité que certains événements soient livrés plus d’une fois.

- Liste blanche implémentée pour l'API REST de Patroni (Alexander Kukushkin)

  Si configuré, seules les adresses IP correspondant aux règles seront autorisées à appeler les points de terminaison non sécurisés. En outre, il est possible d'inclure automatiquement les adresses IP des membres du cluster dans la liste.

- Ajout du support des connexions de réplication via socket Unix (Mohamad El-Rifai)

  Précédemment, Patroni utilisait toujours TCP pour la connexion de réplication, ce qui pouvait entraîner certains problèmes avec la vérification SSL. L'utilisation de sockets Unix permet d'exempter l'utilisateur de réplication de la vérification SSL.

- Vérification de santé sur les balises définies par l'utilisateur (Arman Jafari Tehrani)

  En plus des [balises prédéfinies :](/fr/patroni/config/yaml#tags_settings), il est possible de spécifier un nombre quelconque de balises personnalisées, visibles dans la sortie `patronictl list` et dans l'API REST. À partir de maintenant, il est possible d'utiliser des balises personnalisées dans les vérifications de santé.

- Ajouté le point de terminaison Prometheus `/metrics` (Mark Mercado, Michael Banck)

  Le point de terminaison exposant les mêmes métriques que `/patroni`.

- Réduction de la quantité de messages dans les journaux de Patroni (Alexander Kukushkin)

  Lorsque tout fonctionne normalement, une seule ligne est écrite à chaque exécution de la boucle HA.

**Modifications non rétrocompatibles**

- La fonctionnalité `permanent logical replication slots` ancienne ne fonctionnera plus avec PostgreSQL v10 et les versions antérieures (Alexander Kukushkin)

  La stratégie de création des slots logiques après une promotion ne garantit pas qu’aucun événement logique ne soit perdu et est donc désactivée.

- Le point de terminaison `/leader` renvoie toujours 200 si le nœud détient le verrou (Alexander Kukushkin)

  Promouvoir le cluster de secours nécessite de mettre à jour les contrôles de santé des équilibreurs de charge, ce qui n’est pas très pratique et facile à oublier. Pour y remédier, nous modifions le comportement du point de terminaison de contrôle de santé `/leader`. Il renverra désormais 200, qu’il s’agisse d’un cluster classique ou d’un [standby_cluster](/fr/patroni/standby_cluster#standby_cluster).

**Améliorations apportées au support Raft**

- Prise en charge fiable du chiffrement du trafic Raft (Alexander Kukushkin)

  En raison des différents problèmes liés à `PySyncObj`, le support du chiffrement était très instable

- Gérer les problèmes de DNS dans l'implémentation Raft (Alexander Kukushkin)

  Si `self_addr` et/ou `partner_addrs` sont configurés à l’aide du nom DNS au lieu des adresses IP, `PySyncObj` effectuait uniquement une résolution au moment de la création de l’objet. Cela provoquait des problèmes lorsque le même nœud revenait en ligne avec une adresse IP différente.

**Améliorations de stabilité**

- Compatibilité avec `psycopg2-2.9+` (Alexander Kukushkin)

  Dans `psycopg2`, le `autocommit = True` est ignoré dans le bloc `with connection`, ce qui interrompt les connexions du protocole de réplication.

- Corriger les boucles HA excessives avec Zookeeper (Alexander Kukushkin)

  La mise à jour des ZNodes des membres provoquait une réaction en chaîne, entraînant l'exécution multiple consécutive des boucles HA.

- Recharger si le certificat de l'API REST est modifié sur le disque (Michael Todorovic)

  Si le fichier de certificat de l'API REST a été mis à jour in situ, Patroni n’a pas effectué de rechargement.

- Ne pas créer le répertoire pgpass si l'authentification Kerberos est utilisée (Kostiantyn Nemchenko)

  L'authentification Kerberos et l'authentification par mot de passe sont mutuellement exclusives.

- Corrigé de petits problèmes liés à l'amorçage personnalisé (Alexander Kukushkin)

  Démarrez PostgreSQL avec `hot_standby=off` uniquement lors d'une restauration point-in-time (PITR), puis redémarrez-le après la fin de la restauration.

**Correctifs de bogues**

- Compatibilité avec `kazoo-2.7+` (Alexander Kukushkin)

  Étant donné que Patroni gère lui-même les nouvelles tentatives, il dépend du comportement ancien de `kazoo` selon lequel les requêtes adressées à un cluster Zookeeper sont immédiatement rejetées lorsque aucune connexion n'est disponible.

- Demander explicitement la version du cluster etcd v3 lorsque l'on sait qu'on se connecte via un proxy (Alexander Kukushkin)

  Patroni fonctionne avec un cluster etcd v3 via une passerelle gRPC, et la version du cluster détermine le point de terminaison à utiliser (`/v3`, `/v3beta` ou `/v3alpha`). La version a été déterminée uniquement en conjonction avec la topologie du cluster, mais cette dernière n’a jamais été établie lors de la connexion via un proxy.

--------

## Version 2.0.2 {#version-202}

Publié le 2021-02-22

**Nouvelles fonctionnalités**

- Capacité à ignorer les slots de réplication gérés de manière externe (James Coleman)

  Patroni tente de supprimer toute slot de réplication inconnue de son point de vue, mais il existe certainement des cas où les slots de réplication doivent être gérés de manière externe. À partir de maintenant, il est possible de configurer des slots qui ne doivent pas être supprimés.

- Ajout du support de la limitation des suites de chiffrement pour l'API REST (Gunnar "Nick" Bluth)

  Il peut être configuré via `restapi.ciphers` ou la variable d'environnement `PATRONI_RESTAPI_CIPHERS`.

- Ajout du support des clés TLS chiffrées pour l'API REST (Jonathan S. Katz)

  Il peut être configuré via `restapi.keyfile_password` ou la variable d’environnement `PATRONI_RESTAPI_KEYFILE_PASSWORD`.

- Comparaison en temps constant des identifiants d'authentification de l'API REST (Alex Brasetvik)

  Utilisez `hmac.compare_digest()` à la place de `==`, qui est vulnérable aux attaques par timing.

- Sélectionnez les nœuds synchrones en fonction du délai de réplication (Krishna Sarabu)

  Si le délai de réplication sur le nœud synchrone commence à dépasser le seuil configuré, il peut être rétrogradé en mode asynchrone et/ou remplacé par l'autre nœud. Le comportement est contrôlé par `maximum_lag_on_syncnode`.

**Améliorations de stabilité**

- Démarrer postgres avec `hot_standby = off` lors d'un amorçage personnalisé (Igor Yanchenko)

  Pendant l'amorçage personnalisé, Patroni restaure le basebackup, démarre PostgreSQL et attend la fin de la récupération. Certains paramètres PostgreSQL sur le serveur de secours ne peuvent pas être inférieurs à ceux du serveur primaire, et si la nouvelle valeur (restaurée à partir du WAL) est supérieure à la valeur configurée, PostgreSQL panique et s'arrête. Pour éviter ce comportement, nous effectuerons l'amorçage personnalisé sans le mode `hot_standby`.

- Avertir l'utilisateur si le watchdog requis n'est pas en état sain (Nicolas Thauvin)

  Lorsque l'appareil watchdog n'est pas accessible en écriture ou est absent en mode requis, le membre ne peut pas être promu. Un avertissement a été ajouté pour indiquer à l'utilisateur l'emplacement de cette mauvaise configuration.

- Meilleure verbosité en mode récupération pour un seul utilisateur (Alexander Kukushkin)

  Si Patroni détecte que PostgreSQL n'a pas été arrêté correctement, dans certains cas, la récupération après panne est exécutée en lançant PostgreSQL en mode utilisateur unique. Il se peut que la récupération échoue (par exemple en raison d'un manque d'espace disque), mais que les erreurs soient ignorées.

- Ajout de la compatibilité avec le module `python-consul2` (Alexander Kukushkin, Wilfried Roset)

  Le bon vieux `python-consul` n'est plus maintenu depuis plusieurs années, aussi quelqu'un a-t-il créé une version dérivée avec de nouvelles fonctionnalités et des correctifs de bogues.

- N'utilisez pas `bypass_api_service` lors de l'exécution de [patronictl](/fr/patroni/patronictl#patronictl) (Alexander Kukushkin)

  Lorsqu'un pod K8s s'exécute dans un namespace différent de `default`, il ne dispose pas nécessairement de suffisamment de permissions pour interroger le point de terminaison [kubernetes](/fr/patroni/kubernetes#kubernetes). Dans ce cas, Patroni affiche un avertissement et ignore le paramètre `bypass_api_service`. En cas d'utilisation de [patronictl](/fr/patroni/patronictl#patronictl), cet avertissement était un peu ennuyeux.

- Créez `raft.data_dir` s'il n'existe pas ou assurez-vous qu'il est accessible en écriture (Mark Mercado)

  Améliore l'ergonomie et la facilité d'utilisation.

**Correctifs de bogues**

- Ne pas interrompre le redémarrage ou la promotion si le verrouillage du leader est perdu en pause (Alexander Kukushkin)

  En mode pause, il est autorisé à exécuter PostgreSQL en tant que primaire sans verrou.

- Correctif apporté à `shutdown_request()` dans l'API REST (Nicolas Limage)

  Afin d'améliorer la gestion des connexions SSL et de différer la négociation jusqu'à la mise en route du thread, Patroni substitue plusieurs méthodes dans le `HTTPServer`. La méthode `shutdown_request()` a été oubliée.

- Corrigé le problème de temps de sommeil lors de l'utilisation de Zookeeper (Alexander Kukushkin)

  Patroni pouvait dormir jusqu'à deux fois plus longtemps entre les exécutions du code HA.

- Corrigé les appels invalides à `os.symlink()` lors du déplacement du répertoire de données après un amorçage échoué (Andrew L'Ecuyer)

  Si l'amorçage a échoué, Patroni renomme le répertoire de données, pg_wal et tous les espaces de tables. Ensuite, il met à jour les liens symboliques afin de maintenir la cohérence du système de fichiers. La création des liens symboliques échouait en raison de l'inversion des arguments `src` et `dst`.

- Corrigé un bogue dans la méthode post_bootstrap() (Alexander Kukushkin)

  Si le mot de passe de superutilisateur n’a pas été configuré, Patroni échouait à appeler le script `post_init`, ce qui faisait échouer tout l’amorçage.

- Corrigé un problème avec pg_rewind dans le cluster de secours (Alexander Kukushkin)

  Si le nom de l'utilisateur superutilisateur est différent de `postgres`, `pg_rewind` échouait dans le cluster de secours car la chaîne de connexion ne contenait pas le nom de la base de données.

- Quitter uniquement si l'authentification avec etcd v3 a échoué explicitement (Alexander Kukushkin)

  Lors du démarrage, Patroni effectue la découverte de la topologie du cluster etcd et s'authentifie si nécessaire. Il se peut qu'un des serveurs etcd soit injoignable : Patroni tente alors de s'authentifier sur ce serveur, puis échoue au lieu de réessayer avec le nœud suivant.

- Gérer le cas où cmdline() de psutil retourne une liste vide (Alexander Kukushkin)

  Les processus zombies sont encore des enfants du postmaster, mais ils n'ont pas de cmdline()

- Traiter la variable d'environnement `PATRONI_KUBERNETES_USE_ENDPOINTS` comme une valeur booléenne (Alexander Kukushkin)

  Ne pas le faire rendait impossible la désactivation de `kubernetes.use_endpoints` via l'environnement.

- Améliorer la gestion des erreurs de mise à jour concurrente des points de terminaison (Alexander Kukushkin)

  Patroni interroge explicitement l'objet endpoint actuel, vérifie que le pod actuel détient toujours le verrou leader, puis répète la mise à jour.

--------

## Version 2.0.1 {#version-201}

Sorti le 2020-10-01

**Nouvelles fonctionnalités**

- Utilisez `more` comme visualiseur de pagination dans `patronictl edit-config` si `less` n'est pas disponible (Pavel Golub)

  Sous Windows, il s'agit de `more.com`. En outre, `cdiff` a été remplacé par `ydiff` dans `requirements.txt`, mais [patronictl](/fr/patroni/patronictl#patronictl) continue de prendre en charge chacun d'eux à des fins de compatibilité.

- Ajout du support de `raft` `bind_addr` et `password` (Alexander Kukushkin)

  `raft.bind_addr` peut être utile lors de l'exécution derrière un NAT. `raft.password` active le chiffrement du trafic (nécessite le module `cryptography`).

- Prise en charge du paramètre de connexion `sslpassword` ajoutée (Kostiantyn Nemchenko)

  Le paramètre de connexion a été introduit dans PostgreSQL 13.

**Améliorations de stabilité**

- Modifié le comportement en pause (Alexander Kukushkin)

  1.   Patroni n'appellera pas la méthode `bootstrap` si le répertoire `PGDATA` est manquant ou vide.
  2.   Patroni ne quittera pas en cas de différence d'identifiant de système (sysid) en mode pause, il ne fera que générer un avertissement.
  3.   Le nœud n'essaiera pas de s'attribuer la clé leader en mode pause si PostgreSQL est en cours d'exécution hors récupération (acceptant les écritures) mais que l'identifiant de système (sysid) ne correspond pas à celui de la clé d'initialisation.

- Appliquer `master_start_timeout` lors de l'exécution de la récupération après incident (Alexander Kukushkin)

  Si PostgreSQL a planté sur le nœud leader, Patroni effectue une récupération après panne en lançant PostgreSQL en mode utilisateur unique. Pendant la récupération après panne, le verrou leader est mis à jour. Si la récupération après panne n'est pas terminée dans `master_start_timeout` secondes, Patroni l'interrompt de force et libère le verrou leader.

- Supprimé l'extra `secure` des exigences `urllib3` (Alexander Kukushkin)

  La seule raison d'y ajouter cela était la dépendance `ipaddress` pour Python 2.7.

**Correctifs de bogues**

- Corrigé un bogue dans `Kubernetes.update_leader()` (Alexander Kukushkin)

  Une exception non gérée empêchait la rétrogradation du primaire lorsque la mise à jour de l’objet leader avait échoué.

- Corrigé le blocage de [patronictl](/fr/patroni/patronictl#patronictl) lors de l'utilisation du protocole RAFT (Alexander Kukushkin)

  Lors de l'utilisation de [patronictl](/fr/patroni/patronictl#patronictl) avec la configuration Patroni, `self_addr` devrait être ajouté au `partner_addrs`.

- Correctif d'un bogue dans `get_guc_value()` (Alexander Kukushkin)

  Patroni échouait à obtenir la valeur de `restore_command` sur PostgreSQL 12, ce qui empêchait la récupération des WAL manquants pour `pg_rewind`.

--------

## Version 2.0.0 {#version-200}

Sorti le 2020-09-02

Cette version améliore la compatibilité avec PostgreSQL 13, ajoute le support de plusieurs répliques synchrones, apporte des améliorations importantes dans la gestion de `pg_rewind`, ajoute le support d'Etcd v3 et de Patroni en mode RAFT pur (sans Etcd, Consul ni Zookeeper), et permet d'appeler de manière optionnelle le script `pre_promote` (fencing).

**Prise en charge de PostgreSQL 13**

- Ne pas déclencher `on_reload` lors de la promotion vers `standby_leader` sur PostgreSQL 13+ (Alexander Kukushkin)

  Lors de la promotion vers `standby_leader`, nous modifions `primary_conninfo`, mettons à jour le rôle et rechargeons Postgres. Étant donné que `on_role_change` et `on_reload` se dupliquent effectivement, Patroni n’appellera qu’`on_role_change`.

- Ajout du support des paramètres de connexion `gssencmode` et `channel_binding` (Alexander Kukushkin)

  PostgreSQL 12 a introduit les paramètres de connexion `gssencmode` et 13 `channel_binding`, qui peuvent désormais être utilisés si définis dans la section `postgresql.authentication`.

- Gérer le renommage de `wal_keep_segments` en `wal_keep_size` (Alexander Kukushkin)

  En cas de mauvaise configuration (`wal_keep_segments` sur 13 et `wal_keep_size` sur les versions antérieures), Patroni ajustera automatiquement la configuration.

- Utilisez `pg_rewind` avec `--restore-target-wal` sur 13 si possible (Alexander Kukushkin)

  Sur PostgreSQL 13, Patroni vérifie si `restore_command` est configuré et indique à `pg_rewind` de l'utiliser.

**Nouvelles fonctionnalités**

- \[BETA\] Prise en charge implémentée de Patroni sur RAFT pur (Alexander Kukushkin)

  Cela permet de faire fonctionner Patroni sans dépendances tierces, comme etcd, Consul ou Zookeeper. Pour assurer une haute disponibilité, vous devez exécuter soit trois nœuds Patroni, soit deux nœuds Patroni et un nœud avec `patroni_raft_controller`. Pour plus d'informations, consultez la [documentation](/fr/patroni/config/yaml#raft_settings).

- \[BETA\] Prise en charge implémentée du protocole etcd v3 via gRPC-gateway (Alexander Kukushkin)

  etcd 3.0 a été publié il y a plus de quatre ans, et etcd 3.4 désactive par défaut la version v2. Il existe également des chances que la version v2 soit entièrement supprimée d’etcd ; c’est pourquoi nous avons mis en œuvre la prise en charge d’etcd v3 dans Patroni. Pour commencer à l’utiliser, vous devez créer explicitement la section `etcd3` dans le fichier de configuration de Patroni.

- Prise en charge de plusieurs répliques synchrones (Krishna Sarabu)

  Il permet d'exécuter un cluster avec plus d'une réplique synchrone. Le nombre maximal de répliques synchrones est contrôlé par le nouveau paramètre `synchronous_node_count`. Il est défini par défaut à 1 et n'a aucun effet lorsque le paramètre [synchronous_mode](/fr/patroni/replication_modes#synchronous_mode) est défini sur `off`.

- Ajout de la possibilité d'appeler le script `pre_promote` (Sergey Dudoladov)

  Contrairement aux callbacks, le script `pre_promote` est appelé de manière synchrone après l'acquisition du verrou de leader, mais avant la promotion de PostgreSQL. Si le script échoue ou renvoie un code de sortie non nul, le nœud actuel libère le verrou de leader.

- Ajout de la prise en charge des répertoires de configuration (Floris van Nee)

  Les fichiers YAML du répertoire sont chargés et appliqués dans l'ordre alphabétique.

- Validation avancée des paramètres PostgreSQL (Alexander Kukushkin)

  Si le paramètre spécifique n'est pas pris en charge par la version actuelle de PostgreSQL ou si sa valeur est incorrecte, Patroni supprimera entièrement le paramètre ou tentera de corriger sa valeur.

- Réveiller le thread principal lorsque le point de contrôle forcé après promotion est terminé (Alexander Kukushkin)

  Les répliques attendent une indication de point de contrôle via la clé membre du leader dans le DCS. Cette clé est normalement mise à jour une seule fois par boucle HA. Sans réveiller le thread principal, les répliques devront attendre jusqu'à `loop_wait` secondes de plus que nécessaire.

- Utilisation de la vue `pg_stat_wal_receiver` à partir de la version 9.6 (Alexander Kukushkin)

  La vue contient les valeurs à jour de `primary_conninfo` et `primary_slot_name`, tandis que le contenu de `recovery.conf` pourrait être périmé.

- Amélioration de la gestion des adresses IPv6 dans le fichier de configuration Patroni (Mateusz Kowalski)

  L'adresse IPv6 est censée être placée entre crochets, alors que Patroni s'attendait à la recevoir sans crochets. Les deux formats sont désormais pris en charge.

- Paramètre de configuration Consul `service_tags` ajouté (Robert Edström)

  Ils sont utiles pour la découverte de services dynamiques, par exemple par des équilibreurs de charge.

- Prise en charge SSL implémentée pour Zookeeper (Kostiantyn Nemchenko)

  Il nécessite `kazoo>=2.6.0`.

- Option `no_params` implémentée pour la méthode d'amorçage personnalisée (Kostiantyn Nemchenko)

  Il permet d'appeler `wal-g`, `pgBackRest` et d'autres outils de sauvegarde sans les encapsuler dans des scripts shell.

- Déplacer les fichiers WAL et les espaces de table après un échec de l'initialisation (Feike Steenbergen)

  Lors de l’exécution de `reinit`, Patroni supprimait déjà non seulement `PGDATA` mais aussi le répertoire WAL lié par lien symbolique et les espaces de tables. La méthode `move_data_directory()` effectuera désormais une opération similaire, à savoir renommer le répertoire WAL et les espaces de tables, puis mettre à jour les liens symboliques dans PGDATA.

**Améliorations apportées au support de pg_rewind**

- Vérification améliorée de la divergence de la chronologie (Alexander Kukushkin)

  Nous n'avons pas besoin de rembobiner lorsque la position de relecture sur la réplique n'est pas en avance par rapport au point de basculement, ou lorsque la fin de l'enregistrement de point de contrôle sur l'ancien nœud primaire est identique au point de basculement. Pour obtenir la fin de l'enregistrement de point de contrôle, nous utilisons `pg_waldump` et analysons sa sortie.

- Essayer de récupérer le WAL manquant si `pg_rewind` en signale la perte (Alexander Kukushkin)

  Il se peut que le segment WAL requis pour `pg_rewind` n'existe plus dans le répertoire `pg_wal`, ce qui empêche `pg_rewind` de localiser le point de contrôle antérieur au point de divergence. À partir de PostgreSQL 13, `pg_rewind` peut utiliser `restore_command` pour récupérer les WAL manquants. Pour les versions antérieures de PostgreSQL, Patroni analyse les erreurs d'une tentative de rewind échouée et tente de récupérer les WAL manquants en appelant `restore_command` de manière autonome.

- Détecter une nouvelle timeline dans le cluster de secours et déclencher le rewind ou la réinitialisation si nécessaire (Alexander Kukushkin)

  Le cluster [standby_cluster](/fr/patroni/standby_cluster#standby_cluster) est découplé du cluster primaire et ne connaît donc pas immédiatement les élections de leader ni les changements de timeline. Afin de détecter ce fait, le `standby_leader` vérifie périodiquement l'existence de nouveaux fichiers d'historique dans `pg_wal`.

- Raccourcir et améliorer la présentation de la sortie du journal d'historique (Alexander Kukushkin)

  Lorsque Patroni tente de déterminer la nécessité de `pg_rewind`, il peut écrire le contenu du fichier d'historique provenant du serveur primaire dans les journaux. Le fichier d'historique grandit à chaque basculement ou basculement planifié, et finit par occuper trop de lignes, dont la plupart ne sont pas utiles. Au lieu d'afficher les données brutes, Patroni n'affichera que 3 lignes précédant la timeline actuelle de la réplique et 2 lignes après.

**Améliorations apportées à K8s**

- Supprimer le module python [kubernetes](/fr/patroni/kubernetes#kubernetes) (Alexander Kukushkin)

  Le client Python officiel pour Kubernetes contient une grande quantité de code généré automatiquement et est donc très lourd. Patroni n'utilise qu'une petite partie des points d'entrée de l'API Kubernetes, et la mise en œuvre de leur prise en charge n'a pas été difficile.

- Permettre de contourner le service [kubernetes](/fr/patroni/kubernetes#kubernetes) (Alexander Kukushkin)

  Lorsqu’il est exécuté sur K8s, Patroni communique généralement avec l’API K8s via le service [kubernetes](/fr/patroni/kubernetes#kubernetes), dont l’adresse est exposée dans la variable d’environnement `KUBERNETES_SERVICE_HOST`. Comme tout autre service, le service [kubernetes](/fr/patroni/kubernetes#kubernetes) est géré par `kube-proxy`, qui, selon la configuration, dépend soit d’un programme en espace utilisateur, soit de `iptables` pour le routage du trafic. En ignorant le composant intermédiaire et en se connectant directement aux nœuds maîtres K8s, il devient possible d’implémenter une stratégie de réessai améliorée et de réduire les risques de rétrogradation de PostgreSQL lors de la mise à jour des nœuds maîtres K8s.

- Synchronisation des boucles HA de tous les pods d'un cluster Patroni (Alexander Kukushkin)

  Ne pas le faire augmentait le délai de détection des défaillances de `ttl` à `ttl + loop_wait`.

- Remplir `references` et `nodename` dans les adresses des sous-ensembles sur K8s (Alexander Kukushkin)

  Certains équilibreurs de charge dépendent de ces informations.

- Corriger d'éventuelles conditions de course dans `update_leader()` (Alexander Kukushkin)

  La mise à jour concurrente du ConfigMap ou de l'objet Endpoint du leader effectuée en dehors de Patroni peut entraîner l'échec de l'appel `update_leader()`. Dans ce cas, Patroni vérifie à nouveau que le nœud actuel détient toujours le verrou leader, puis répète la mise à jour.

- Interdire explicitement le patching de configurations inexistantes (Alexander Kukushkin)

  Pour les clusters DCS autres que [kubernetes](/fr/patroni/kubernetes#kubernetes), l'appel PATCH échoue avec une exception en raison de `cluster.config` étant `None`, mais sur Kubernetes, il créait sans problème l'annotation de configuration et empêchait l'écriture de la configuration d'amorçage après l'achèvement de l'amorçage.

- Corriger un bug dans [pause](/fr/patroni/pause#pause) (Alexander Kukushkin)

  Les répliques supprimaient `primary_conninfo` et redémarraient PostgreSQL lorsque la clé du leader était absente, mais elles ne devraient rien faire.

**Améliorations de l'API REST**

- Reporter l'établissement de la connexion TLS jusqu'à ce que le thread worker ait démarré (Alexander Kukushkin, Ben Harris)

  Si la négociation TLS a été effectuée dans le thread d'API et que le client n'a envoyé aucune donnée, le thread d'API était bloqué (risque de déni de service).

- Vérifier `basic-auth` indépendamment du certificat client dans l'API REST (Alexander Kukushkin)

  Précédemment, seul le certificat client était validé. Effectuer deux vérifications de manière indépendante est un cas d'utilisation absolument valable.

- Écrire un double `CRLF` après les en-têtes HTTP de la requête `OPTIONS` (Sergey Burladyan)

  HAProxy était satisfait avec un seul `CRLF`, tandis que la vérification de santé de Consul signalait une connexion interrompue et une fin inattendue du flux (EOF).

- `GET /cluster` affichait des informations obsolètes sur les membres Zookeeper (Alexander Kukushkin)

  Le point de terminaison utilisait la vue interne du cluster de Patroni. Pour Patroni lui-même, cela n'avait pas d'impact, mais lorsqu'il est exposé à l'extérieur, il est nécessaire de fournir des informations à jour, en particulier le retard de réplication.

- Contrôle de santé corrigé pour le cluster de secours (Alexander Kukushkin)

  Le `GET /standby-leader` d'un maître et le `GET /master` d'un `standby_leader` répondaient incorrectement avec 200.

- Implémenté `DELETE /switchover` (Alexander Kukushkin)

  L'appel d'API REST supprime le basculement planifié programmé.

- Créé les points de terminaison `/readiness` et `/liveness` (Alexander Kukushkin)

  Ils peuvent être utiles pour supprimer les pods « non sains » des adresses de sous-ensembles lorsque le service Kubernetes est utilisé avec des sélecteurs d'étiquettes.

- Contrôles de santé améliorés de l'API REST `GET /replica` et `GET /async` (Krishna Sarabu, Alexander Kukushkin)

  Les vérifications prennent désormais en charge un mot-clé facultatif `?lag=<max-lag>` et ne renvoient un code 200 que si le décalage est inférieur à la valeur fournie. En cas d'utilisation de cette fonctionnalité, veuillez noter que les informations sur la position du WAL sur le leader sont mises à jour uniquement toutes les `loop_wait` secondes !

- Ajout du support des en-têtes HTTP définis par l'utilisateur dans la réponse de l'API REST (Yogesh Sharma)

  Cette fonctionnalité peut être utile si des requêtes sont effectuées depuis un navigateur.

**Améliorations apportées à patronictl**

- Ne tentez pas d'appeler un leader inexistant dans `patronictl pause` (Alexander Kukushkin)

  Lors de la mise en pause d’un cluster sans leader sur K8s, [patronictl](/fr/patroni/patronictl#patronictl) affichait des avertissements indiquant que le membre « None » n’était pas accessible.

- Gérer le cas où le `conn_url` d’un membre est manquant (Alexander Kukushkin)

  Sur K8s, il se peut que le pod ne dispose pas des annotations nécessaires car Patroni n'est pas encore en cours d'exécution. Cela faisait échouer [patronictl](/fr/patroni/patronictl#patronictl).

- Ajout de la possibilité d'afficher la topologie du cluster en ASCII (Maxim Fedotov, Alexander Kukushkin)

  Il est très utile d’obtenir un aperçu du cluster avec une réplication en cascade.

- Implémenter `patronictl flush switchover` (Alexander Kukushkin)

  Avant cela, `patronictl flush` ne supportait que l'annulation des redémarrages planifiés.

**Correctifs de bogues**

- Erreur d'attribut lors de l'amorçage du cluster avec un PGDATA existant (Krishna Sarabu)

  Lors de la tentative de création/mise à jour de la clé `/history`, Patroni tentait d'accéder à l'objet `ClusterConfig` qui n'avait pas encore été créé dans le DCS.

- Gestion améliorée des exceptions dans Consul (Alexander Kukushkin)

  Une exception non gérée dans la méthode `touch_member()` a provoqué l'arrêt complet du processus Patroni.

- Forcer `synchronous_commit=local` pour le script `post_init` (Alexander Kukushkin)

  Patroni effectuait déjà cette opération lors de la création des utilisateurs (`replication`, `rewind`), mais l'oubli dans le cas de `post_init` était une erreur. En conséquence, si le script ne l'effectuait pas en interne de manière autonome, l'amorçage dans [synchronous_mode](/fr/patroni/replication_modes#synchronous_mode) n'était pas capable de s'achever.

- Augmentation de `maxsize` dans le gestionnaire de pool Consul (ponvenkates)

  Avec le `size=1` par défaut, certains avertissements ont été générés.

- Patroni signalait incorrectement que PostgreSQL était en cours d'exécution (Alexander Kukushkin)

  L'état n'a pas été mis à jour lorsque, par exemple, Postgres a planté en raison d'une erreur de disque plein.

- Insérer `*` dans `pgpass` à la place des valeurs absentes ou vides (Alexander Kukushkin)

  Si, par exemple, `standby_cluster.port` n’est pas spécifié, le fichier `pgpass` a été incorrectement généré.

- Ignorer la création de slot de réplication physique sur le nœud leader en présence de caractères spéciaux (Krishna Sarabu)

  Patroni semblait créer un slot inactif (lorsque `slots` est défini) pour le nœud leader lorsque le nom contenait des caractères spéciaux tels que '-' (par exemple, "abc-us-1").

- Éviter de supprimer un `pg_hba.conf` introuvable dans l'amorçage personnalisé (Krishna Sarabu)

  Patroni échouait si `pg_hba.conf` se trouvait en dehors du répertoire `pgdata` après un amorçage personnalisé.

--------

## Version 1.6.5 {#version-165}

Publié le 2020-08-23

**Nouvelles fonctionnalités**

- Délai d'arrêt du maître (Krishna Sarabu)

  Le nombre de secondes autorisées à Patroni pour attendre lors de l'arrêt de Postgres. N'est effectif que lorsque [synchronous_mode](/fr/patroni/replication_modes#synchronous_mode) est activé. Si la valeur est supérieure à 0 et que [synchronous_mode](/fr/patroni/replication_modes#synchronous_mode) est activé, Patroni envoie `SIGKILL` au postmaster si l'opération d'arrêt dure plus longtemps que la valeur définie par `master_stop_timeout`. Définissez cette valeur en fonction de votre compromis entre durabilité et disponibilité. Si le paramètre n'est pas défini ou est défini sur une valeur non positive, `master_stop_timeout` n'a pas d'effet.

- Ne créez pas de slot physique permanent portant le nom du primaire (Alexander Kukushkin)

  Il s'agit d'un problème courant où le nœud primaire recycle les segments WAL tandis que la réplique est hors ligne. Nous disposons désormais d'une solution efficace pour les clusters statiques, comprenant un nombre fixe de nœuds dont les noms ne changent jamais. Il suffit de lister les noms de tous les nœuds dans `slots` afin que le nœud primaire ne supprime pas le slot lorsque le nœud est hors ligne (non inscrit dans le DCS).

- Premier brouillon du validateur de configuration (Igor Yanchenko)

  Utilisez `patroni --validate-config patroni.yaml` afin de valider la configuration de Patroni.

- Possibilité de configurer la longueur maximale de l'historique des timelines (Krishna Sarabu)

  Patroni écrit l'historique des basculements et des basculements planifiés dans la clé `/history` du DCS. Au fil du temps, la taille de cette clé augmente, mais dans la plupart des cas, seules les dernières lignes sont pertinentes. Le paramètre `max_timelines_history` permet de spécifier le nombre maximal d'éléments d'historique de timeline à conserver dans le DCS.

- Compatibilité avec Kazoo 2.7.0 (Danyal Prout)

  Certaines méthodes non publiques de Kazoo ont vu leurs signatures modifiées, mais Patroni en dépendait.

**Améliorations apportées à patronictl**

- Afficher les balises des membres (Kostiantyn Nemchenko, Alexander Kukushkin)

  Les balises sont configurées individuellement pour chaque nœud, et il n’existait aucune méthode simple pour obtenir un aperçu global de celles-ci.

- Améliorer la sortie des membres (Alexander Kukushkin)

  Le nom du cluster redondant ne sera plus affiché sur chaque ligne, mais uniquement dans l’en-tête du tableau.

``` bash
$ patronictl list
+ Cluster: batman (6813309862653668387) +---------+----+-----------+---------------------+
|    Member   |      Host      |  Role  |  State  | TL | Lag in MB | Tags                |
+-------------+----------------+--------+---------+----+-----------+---------------------+
| postgresql0 | 127.0.0.1:5432 | Leader | running |  3 |           | clonefrom: true     |
|             |                |        |         |    |           | noloadbalance: true |
|             |                |        |         |    |           | nosync: true        |
+-------------+----------------+--------+---------+----+-----------+---------------------+
| postgresql1 | 127.0.0.1:5433 |        | running |  3 |       0.0 |                     |
+-------------+----------------+--------+---------+----+-----------+---------------------+
```

- Échouer si un fichier de configuration est spécifié explicitement mais non trouvé (Kaarel Moppel)

  Précédemment, [patronictl](/fr/patroni/patronictl#patronictl) ne signalait qu'un message `DEBUG`.

- Résolu le problème de pod K8s non initialisé entraînant une panne de patronictl (Alexander Kukushkin)

  Patroni dépend de certaines annotations de pods sur K8s. Lorsqu'un pod Patroni s'arrête ou démarre, aucune annotation valide n'est encore présente, et [patronictl](/fr/patroni/patronictl#patronictl) échouait avec une exception.

**Améliorations de stabilité**

- Appliquer un délai de 1 seconde en cas d'échec de l'appel LIST au serveur d'API K8s (Alexander Kukushkin)

  C'est surtout nécessaire pour éviter la surcharge des journaux, mais cela contribue également à prévenir la famine du thread principal.

- Réessayer si l'en-tête HTTP `retry-after` est retourné par l'API K8s (Alexander Kukushkin)

  Si le serveur d'API Kubernetes est saturé de demandes, il peut demander une nouvelle tentative.

- Nettoyer l’environnement `KUBERNETES_` depuis le postmaster (Feike Steenbergen)

  Les variables d'environnement `KUBERNETES_` ne sont pas obligatoires pour PostgreSQL, mais les exposer au postmaster les rend également accessibles aux processus backend et aux utilisateurs réguliers de la base de données (par exemple, via pl/perl).

- Nettoyer les espaces de table sur une réinitialisation (Krishna Sarabu)

  Lors d’un `reinit`, Patroni supprimait uniquement `PGDATA` tout en laissant les répertoires de tablespaces définis par l’utilisateur. Cela entraînait une boucle dans le processus de réinitialisation. La solution de contournement précédente consistait à implémenter le script d’amorçage personnalisé [custom bootstrap](/fr/patroni/replica_bootstrap#custom_bootstrap).

- Exécuter explicitement `CHECKPOINT` après la promotion (Alexander Kukushkin)

  Cela permet de réduire le temps avant que le nouveau serveur primaire ne soit utilisable pour `pg_rewind`.

- Actualisation intelligente des membres etcd (Alexander Kukushkin)

  En cas d'échec de Patroni à exécuter une requête sur tous les membres du cluster Etcd, Patroni vérifiera à nouveau les enregistrements `A` ou `SRV` pour détecter des modifications d'adresses IP/hôtes avant de réessayer la prochaine fois.

- Ignorer les valeurs manquantes de `pg_controldata` (Feike Steenbergen)

  Les valeurs manquent lors de l’utilisation de binaires dont la version ne correspond pas à celle de PGDATA. Patroni tentera tout de même de démarrer PostgreSQL, qui signalera que la version majeure ne correspond pas et s’arrêtera avec une erreur.

**Correctifs de bogues**

- Désactiver la vérification SSL pour Consul lorsque cela est nécessaire (Julien Riou)

  À partir d'une certaine version de `urllib3`, le paramètre `cert_reqs` doit être explicitement défini sur `ssl.CERT_NONE` afin de désactiver efficacement la vérification SSL.

- Éviter d'ouvrir une connexion de réplication à chaque cycle de la boucle HA (Alexander Kukushkin)

  La régression a été introduite dans la version 1.6.4.

- Appeler le rappel `on_role_change` en cas d'échec du primaire (Alexander Kukushkin)

  Dans certains cas, cela peut entraîner la conservation de l'adresse IP virtuelle sur l'ancien nœud primaire. Ce comportement régressif a été introduit à partir de la version 1.4.5.

- Réinitialiser l'état de rembobinage si PostgreSQL a été démarré après un pg_rewind réussi (Alexander Kukushkin)

  En raison de ce bogue, Patroni démarrait PostgreSQL, arrêté manuellement, en mode pause.

- Convertir `recovery_min_apply_delay` en `ms` lors de la vérification de `recovery.conf`

  Patroni redémarrait indéfiniment la réplique si `recovery_min_apply_delay` était configuré sur PostgreSQL antérieur à la version 12.

- Compatibilité avec PyInstaller (Alexander Kukushkin)

  PyInstaller permet de figer (packager) des applications Python en exécutables autonomes. La compatibilité a été rompue lors du passage à la méthode `spawn` au lieu de `fork` pour `multiprocessing`.

--------

## Version 1.6.4 {#version-164}

Sorti le 2020-01-27

**Nouvelles fonctionnalités**

- Implémenté l'option `--wait` pour `patronictl reinit` (Igor Yanchenko)

  patronictl attendra que `reinit` se termine si l'option `--wait` est utilisée.

- Améliorations supplémentaires du support Windows (Igor Yanchenko, Alexander Kukushkin)

  1.  Tous les scripts shell utilisés pour les tests d'intégration sont réécrits en python
  2.  Le `pg_ctl kill` sera utilisé pour arrêter postgres sur les systèmes non POSIX
  3.  N'essayez pas d'utiliser les sockets Unix

**Améliorations de stabilité**

- Vérifiez que `unix_socket_directories` et `stats_temp_directory` existent (Igor Yanchenko)

  Lors du démarrage de Patroni et de Postgres, assurez-vous que `unix_socket_directories` et `stats_temp_directory` existent ou tentez de les créer. Patroni s'arrêtera si la création échoue.

- Assurez-vous que `postgresql.pgpass` se trouve à l'emplacement où Patroni dispose d'un accès en écriture (Igor Yanchenko)

  En cas de manque d'accès en écriture, Patroni se terminera avec une exception.

- Désactiver par défaut la vérification Consul `serfHealth` (Kostiantyn Nemchenko)

  Même en cas de problèmes réseau mineurs, la défaillance de `serfHealth` entraîne l’invalidation de toutes les sessions associées au nœud. La clé leader est ainsi perdue bien avant `ttl`, ce qui provoque des redémarrages inattendus des répliques et éventuellement la rétrogradation du primaire.

- Configurez les keepalives TCP pour les connexions vers l'API K8s (Alexander Kukushkin)

  En cas de non-réception de données sur la socket après un délai de TTL secondes, celle-ci peut être considérée comme interrompue.

- Éviter la journalisation des mots de passe lors de la création d'utilisateurs (Alexander Kukushkin)

  Si le mot de passe est rejeté ou si la journalisation est configurée en mode verbeux ou non configurée du tout, il se peut que le mot de passe soit écrit dans les journaux de PostgreSQL. Pour éviter cela, Patroni modifiera `log_statement`, `log_min_duration_statement` et `log_min_error_statement` en des valeurs sûres avant d'effectuer l'opération de création ou de mise à jour de l'utilisateur.

**Correctifs de bogues**

- Utilisez `restore_command` provenant de la configuration [standby_cluster](/fr/patroni/standby_cluster#standby_cluster) sur les répliques en cascade (Alexander Kukushkin)

  Le `standby_leader` le faisait déjà depuis le début, dès l'existence de cette fonctionnalité. Ne pas effectuer la même opération sur les répliques pourrait empêcher celles-ci de rattraper le standby leader.

- Mettre à jour la timeline signalée par le cluster de secours (Alexander Kukushkin)

  En cas de basculement de timeline, le cluster de secours était correctement en réplication depuis le primaire, mais [patronictl](/fr/patroni/patronictl#patronictl) signalait l'ancienne timeline.

- Autoriser la définition de certains paramètres de récupération dans custom_conf (Alexander Kukushkin)

  Lors de la validation des paramètres de récupération sur une réplique, Patroni ignorera `archive_cleanup_command`, `promote_trigger_file`, `recovery_end_command`, `recovery_min_apply_delay` et `restore_command` s'ils ne sont pas définis dans la configuration Patroni mais sont présents dans des fichiers autres que `postgresql.auto.conf` ou `postgresql.conf`.

- Améliorer la gestion des paramètres PostgreSQL comportant un point dans leur nom (Alexander Kukushkin)

  Ces paramètres peuvent être définis par des extensions où l’unité n’est pas nécessairement une chaîne de caractères. Modifier cette valeur peut nécessiter un redémarrage (par exemple `pg_stat_statements.max`).

- Améliorer la gestion des exceptions pendant l'arrêt (Alexander Kukushkin)

  Pendant l'arrêt, Patroni tente de mettre à jour son état dans le DCS. Si le DCS est inaccessible, une exception peut être levée. Le manque de gestion des exceptions empêchait le thread de journalisation de s'arrêter.

--------

## Version 1.6.3 {#version-163}

Sorti le 2019-12-05

**Correctifs de bogues**

- Ne pas exposer le mot de passe lors de l'exécution de `pg_rewind` (Alexander Kukushkin)

  Un bogue a été introduit dans le [#1301](https://github.com/patroni/patroni/pull/1301)

- Appliquer les paramètres de connexion spécifiés dans `postgresql.authentication` à `pg_basebackup` et les méthodes personnalisées de création de réplique (Alexander Kukushkin)

  Ils comptaient sur une chaîne de connexion de type URL et les paramètres n'ont donc jamais été pris en compte.

--------

## Version 1.6.2 {#version-162}

Sorti le 2019-12-05

**Nouvelles fonctionnalités**

- Implémenté `patroni --version` (Igor Yanchenko)

  Il affiche la version actuelle de Patroni et quitte.

- Définir l’en-tête `user-agent` pour toutes les requêtes HTTP (Alexander Kukushkin)

  Patroni communique avec Consul, etcd et l'API Kubernetes via le protocole http. Disposer d'un `user-agent` spécialement conçu (par exemple : `Patroni/1.6.2 Python/3.6.8 Linux`) peut s'avérer utile pour le débogage et la surveillance.

- Permettre de configurer le niveau de journalisation pour les traces d'exceptions (Igor Yanchenko)

  Si vous définissez `log.traceback_level=DEBUG`, les traces d'exceptions ne seront visibles que lorsque `log.level=DEBUG`. Le comportement par défaut reste inchangé.

**Améliorations de stabilité**

- Éviter d'importer tous les modules DCS lors de la recherche du module requis par le fichier de configuration (Alexander Kukushkin)

  Il n’est pas nécessaire d’importer les modules etcd, Consul et Kubernetes si l’on n’a besoin que d’un système tel que Zookeeper. Cela permet de réduire la consommation de mémoire et de résoudre le problème des messages INFO `Failed to import smth`.

- Supprimé le module python `requests` des exigences explicites (Alexander Kukushkin)

  Il n'était utilisé pour rien de critique, mais causait de nombreux problèmes lors du lancement de la nouvelle version de `urllib3`.

- Améliorer la gestion de `etcd.hosts` fourni sous forme de chaîne séparée par des virgules au lieu d’un tableau YAML (Igor Yanchenko)

  Précédemment, cela échouait lorsqu'il était écrit au format `host1:port1, host2:port2` (le caractère espace après la virgule).

**Améliorations de l'ergonomie**

- N'obligez pas les utilisateurs à choisir des membres dans une liste vide dans [patronictl](/fr/patroni/patronictl#patronictl) (Igor Yanchenko)

  Si l'utilisateur fournit un nom de cluster incorrect, une exception sera levée plutôt que de demander de choisir un membre dans une liste vide.

- Rendre le message d'erreur plus utile si l'API REST ne peut pas se lier (Igor Yanchenko)

  Pour un utilisateur inexpérimenté, il peut être difficile de déterminer ce qui ne va pas à partir de la trace de pile Python.

**Correctifs de bogues**

- Corriger le calcul de `wal_buffers` (Alexander Kukushkin)

  L'unité de base a été passée des blocs de 8 ko aux octets à partir de PostgreSQL 11.

- Utilisez `passfile` dans `primary_conninfo` uniquement sur PostgreSQL 10+ (Alexander Kukushkin)

  Sur les anciennes versions, aucune garantie n’est assurée quant au bon fonctionnement de `passfile`, sauf si la dernière version de `libpq` est installée.

--------

## Version 1.6.1 {#version-161}

Sorti le 2019-11-15

**Nouvelles fonctionnalités**

- Ajout de la variable d'environnement `PATRONICTL_CONFIG_FILE` (msvechla)

  Il permet de configurer l'argument `--config-file` pour [patronictl](/fr/patroni/patronictl#patronictl) à partir de l'environnement.

- Implémenter `patronictl history` (Alexander Kukushkin)

  Il affiche l'historique des basculements et des basculements planifiés.

- Passer `-c statement_timeout=0` en `PGOPTIONS` lors de `pg_rewind` (Alexander Kukushkin)

  Il protège contre le cas où `statement_timeout` sur le serveur est défini sur une valeur faible et une des instructions exécutées par pg_rewind est annulée.

- Autoriser des valeurs plus faibles pour la configuration de PostgreSQL (Soulou)

  Patroni n'autorisait pas certains paramètres de configuration PostgreSQL à être définis à une valeur inférieure à des valeurs codées en dur. Les valeurs minimales autorisées sont désormais plus faibles, sans toutefois modifier les valeurs par défaut.

- Autoriser l'authentification basée sur les certificats (Jonathan S. Katz)

  Cette fonctionnalité permet l’authentification basée sur les certificats pour les comptes superutilisateur, réplication et rewind, et permet à l’utilisateur de spécifier le `sslmode` avec lequel il souhaite se connecter.

- Utilisez `passfile` dans `primary_conninfo` au lieu du mot de passe (Alexander Kukushkin)

  Il permet d'éviter de définir les permissions `600` sur postgresql.conf

- Effectuer `pg_ctl reload` indépendamment des modifications de configuration (Alexander Kukushkin)

  Il se peut que certains fichiers de configuration ne soient pas gérés par Patroni. Lorsqu'une recharge est effectuée via l'API REST ou en envoyant SIGHUP au processus Patroni, on s'attend généralement à ce que PostgreSQL soit également rechargé. Ce n'était pas le cas auparavant lorsque aucune modification n'avait été apportée à la section `postgresql` de la configuration Patroni.

- Comparez tous les paramètres de récupération, et non seulement `primary_conninfo` (Alexander Kukushkin)

  Précédemment, la méthode `check_recovery_conf()` ne vérifiait que si `primary_conninfo` avait changé, sans tenir compte de tous les autres paramètres de récupération.

- Permettre d'appliquer certains paramètres de récupération sans redémarrage (Alexander Kukushkin)

  À partir de PostgreSQL 12, les paramètres de récupération suivants peuvent être modifiés sans redémarrage : `archive_cleanup_command`, `promote_trigger_file`, `recovery_end_command` et `recovery_min_apply_delay`. Dans les futures versions de PostgreSQL, cette liste sera étendue, et Patroni la prendra en charge automatiquement.

- Permettre de modifier `use_slots` en ligne (Alexander Kukushkin)

  Précédemment, il fallait redémarrer Patroni et supprimer les slots manuellement.

- Supprimez uniquement les variables d'environnement préfixées par `PATRONI_` au démarrage de Postgres (Cody Coons)

  Il résouda plusieurs problèmes liés à l'exécution de différents wrappers de données étrangères.

**Améliorations de stabilité**

- Utilisez LIST + WATCH lors de l'utilisation de l'API Kubernetes (Alexander Kukushkin)

  Il permet de recevoir efficacement les modifications d'objets (pods, endpoints, configmaps) et réduit la charge sur les nœuds maîtres Kubernetes.

- Améliorer le flux de travail lorsque PGDATA n'est pas vide pendant l'amorçage (Alexander Kukushkin)

  Selon le code source de `initdb`, un répertoire PGDATA peut être considéré comme vide lorsque seuls `lost+found` et `.dotfiles` s'y trouvent. Patroni adopte désormais la même logique. Si `PGDATA` n'est pas vide, tout en étant invalide du point de vue de `pg_controldata`, Patroni émet une alerte et s'arrête.

- Éviter l’appel coûteux à `os.listdir()` à chaque boucle HA (Alexander Kukushkin)

  Lorsque le système est sous charge d'E/S, l'exécution de `os.listdir()` peut prendre quelques secondes (voire plusieurs minutes), ce qui affecte négativement le cycle de haute disponibilité de Patroni. Cela peut même entraîner la disparition de la clé leader du DCS en raison de l'absence de mise à jour. Il existe une méthode plus efficace et moins coûteuse pour vérifier que le répertoire PGDATA n'est pas vide. Nous vérifions désormais la présence du fichier `global/pg_control` dans PGDATA.

- Quelques améliorations apportées à l'infrastructure de journalisation (Alexander Kukushkin)

  Précédemment, il était possible de perdre les dernières lignes de journalisation lors de l'arrêt, car le thread de journalisation était un thread `daemon`.

- Utiliser la méthode de démarrage multiprocessing `spawn` avec Python 3.4+ (Maciej Kowalczyk)

  Il s'agit d'un [problème connu](https://bugs.python.org/issue6721) en Python, lié à une incompatibilité entre les threads et le multiprocessing. Passer de la méthode par défaut `fork` à `spawn` est une solution recommandée. Ne pas le faire peut entraîner un blocage du processus de démarrage du Postmaster, avec Patroni signalant indéfiniment `INFO: restarting after failure in progress`, alors que PostgreSQL est en réalité en cours d'exécution.

**Améliorations de l'API REST**

- Permettre de vérifier les certificats clients dans l'API REST (Alexander Kukushkin)

  Si `verify_client` est défini sur `required`, Patroni vérifie les certificats clients pour toutes les appels d'API REST. Lorsqu'il est défini sur `optional`, les certificats clients sont vérifiés uniquement pour les points de terminaison d'API REST non sécurisés.

- Renvoyer le code de réponse 503 pour la requête de vérification de santé `GET /replica` si PostgreSQL n'est pas en cours d'exécution (Alexander Anikin)

  Postgres peut passer un temps important en phase de récupération avant de commencer à accepter les connexions clientes.

- Implémenter les points de terminaison `/history` et `/cluster` (Alexander Kukushkin)

  Le point de terminaison `/history` affiche le contenu de la clé `history` dans le DCS. Le point de terminaison `/cluster` affiche tous les membres du cluster ainsi que certaines informations de service, telles que les redémarrages en attente ou programmés et les basculements planifiés.

**Améliorations apportées au support d’etcd**

- Réessayer en cas d'erreur interne RAFT sur etcd (Alexander Kukushkin)

  Lors de l'arrêt d'un nœud etcd, celui-ci envoie `response code=300, data='etcdserver: server stopped'`, ce qui provoquait la rétrogradation du primaire par Patroni.

- Ne pas abandonner trop tôt la tentative de répétition des requêtes etcd (Alexander Kukushkin)

  Lorsqu'il y avait des problèmes réseau, Patroni épuisait rapidement la liste des nœuds etcd et abandonnait sans utiliser l'intégralité de `retry_timeout`, pouvant entraîner la rétrogradation du primaire.

**Correctifs de bogues**

- Désactiver `synchronous_commit` lors de la délivrance de permissions d'exécution à l'utilisateur `pg_rewind` (kremius)

  Si l'amorçage est effectué avec `synchronous_mode_strict: true`, l'instruction `GRANT EXECUTE` attendait indéfiniment parce qu’aucun nœud de secours synchrone n’était disponible.

- Corriger une fuite mémoire sous Python 3.7 (Alexander Kukushkin)

  Patroni utilise `ThreadingMixIn` pour traiter les requêtes de l'API REST, et Python 3.7 crée par défaut des threads non démon pour chaque requête.

- Corriger les conditions de course dans les actions asynchrones (Alexander Kukushkin)

  Il existait un risque que `patronictl reinit --force` soit écrasé par la tentative de récupération d’un serveur Postgres arrêté. Cela a abouti à une situation où Patroni tentait de démarrer Postgres pendant que basebackup était en cours d’exécution.

- Corriger la condition de course dans la méthode `postmaster_start_time()` (Alexander Kukushkin)

  Si la méthode est exécutée depuis le thread de l'API REST, elle nécessite la création d'un objet curseur distinct.

- Corriger le problème de non-promotion du standby synchrone dont le nom contenait des lettres majuscules (Alexander Kukushkin)

  Nous avons converti le nom en minuscules car PostgreSQL effectuait la même opération lors de la comparaison de `application_name` avec la valeur de `synchronous_standby_names`.

- Tuer tous les processus enfants ainsi que le processus de rappel avant de démarrer le nouveau (Alexander Kukushkin)

  Ne pas le faire rend difficile l’implémentation de rappels (callbacks) dans bash et peut éventuellement entraîner une situation où deux rappels s’exécutent simultanément.

- Corriger le problème « start failed » (Alexander Kukushkin)

  Dans certains cas, l’état de Postgres peut être défini comme « start failed » même si Postgres est effectivement en cours d’exécution.

--------

## Version 1.6.0 {#version-160}

Sorti le 2019-08-05

Cette version ajoute la compatibilité avec PostgreSQL 12, permet d'exécuter pg_rewind sans privilèges de superutilisateur sur PostgreSQL 11 et versions ultérieures, et active la prise en charge d'IPv6.

**Nouvelles fonctionnalités**

- Psycopg2 a été supprimé des dépendances et doit être installé indépendamment (Alexander Kukushkin)

  À compter de la version 2.8.0, `psycopg2` a été divisé en deux paquets distincts, `psycopg2` et `psycopg2-binary`, pouvant être installés simultanément au même emplacement dans le système de fichiers. Afin de réduire le problème de conflits de dépendances, nous laissons l’utilisateur choisir la méthode d’installation. Plusieurs options sont disponibles ; veuillez consulter la [documentation](/fr/patroni/installation#psycopg2_install_options).

- Compatibilité avec PostgreSQL 12 (Alexander Kukushkin)

  À compter de PostgreSQL 12, il n’existe plus de `recovery.conf` et tous les paramètres de récupération précédents sont convertis en paramètres [GUC](https://www.enterprisedb.com/blog/what-guc-variable). Afin de se protéger contre `ALTER SYSTEM SET primary_conninfo` ou des configurations similaires, Patroni analysera `postgresql.auto.conf` et supprimera tous les paramètres de serveur de secours et de récupération présents dans ce fichier. La configuration de Patroni reste compatible avec les versions antérieures. Par exemple, même si `restore_command` est un GUC, il est possible de le spécifier dans la section `postgresql.recovery_conf.restore_command` et Patroni l’écrira dans `postgresql.conf` pour PostgreSQL 12.

- Permettre d'utiliser `pg_rewind` sans privilèges de superutilisateur sur PostgreSQL 11 et versions ultérieures (Alexander Kukushkin)

  Si vous souhaitez utiliser cette fonctionnalité, définissez `username` et `password` dans la section `postgresql.authentication.rewind` du fichier de configuration Patroni. Pour un cluster existant, vous devrez créer l'utilisateur manuellement et accorder la permission `GRANT EXECUTE` sur quelques fonctions. Vous trouverez des détails supplémentaires dans la documentation PostgreSQL [documentation](https://www.postgresql.org/docs/11/app-pgrewind.html#id-1.9.5.8.8).

- Comparer intelligemment les valeurs réelles et souhaitées de `primary_conninfo` sur les réplicas (Alexander Kukushkin)

  Cela peut aider à éviter le redémarrage de la réplique lors de la conversion d’un cluster primaire-secours existant en un cluster géré par Patroni

- Prise en charge d'IPv6 (Alexander Kukushkin)

  Deux problèmes majeurs étaient présents. Le service API REST de Patroni écoutait uniquement sur `0.0.0.0` et les adresses IPv6 utilisées dans `api_url` et `conn_url` n’étaient pas correctement encadrées de crochets.

- Prise en charge de Kerberos (Ajith Vilas, Alexander Kukushkin)

  Il permet d'utiliser l'authentification Kerberos entre les nœuds Postgres au lieu de définir des mots de passe dans le fichier de configuration Patroni

- Gérer `pg_ident.conf` (Alexander Kukushkin)

  Cette fonctionnalité fonctionne de manière similaire à `pg_hba.conf` : si `postgresql.pg_ident` est défini dans le fichier de configuration ou dans le DCS, Patroni écrira sa valeur dans `pg_ident.conf`, toutefois, si `postgresql.parameters.ident_file` est défini, Patroni supposera que `pg_ident` est géré depuis l'extérieur et ne mettra pas à jour le fichier.

**Améliorations de l'API REST**

- Ajout du point de terminaison `/health` (Wilfried Roset)

  Il renverra le code d’état HTTP 200 uniquement si PostgreSQL est en cours d’exécution

- Ajout des points de terminaison `/read-only` et `/read-write` (Julien Riou)

  Le point de terminaison `/read-only` permet des lectures équilibrées entre les répliques et le primaire. Le point de terminaison `/read-write` est un alias de `/primary`, `/leader` et `/master`.

- Utilisez `SSLContext` pour encapsuler la socket de l'API REST (Julien Riou)

  L'utilisation de `ssl.wrap_socket()` est obsolète et permettait encore des protocoles bientôt obsolètes, tels que TLS 1.1.

**Améliorations de la journalisation**

- Journalisation en deux étapes (Alexander Kukushkin)

  Tous les messages d’enregistrement sont d’abord écrits dans une file en mémoire et ensuite vidés de manière asynchrone vers stderr ou un fichier depuis un thread distinct. La taille maximale de la file est limitée (configurable). Si cette limite est atteinte, Patroni commencera à perdre des messages d’enregistrement, ce qui reste préférable à bloquer la boucle HA.

- Activer la journalisation de débogage pour les appels d'API GET/OPTIONS ainsi que la latence (Jan Tomsa)

  Il facilitera le débogage des vérifications de santé effectuées par HAProxy, Consul ou d'autres outils qui déterminent quel nœud est le primaire ou la réplique.

- Journaliser les exceptions capturées dans Retry (Daniel Kucera)

  Enregistrez l'exception finale lorsque le nombre d'essais ou le délai d'attente a été atteint. Cela devrait aider à déboguer certains problèmes survenant lors de la communication avec le DCS.

**Améliorations apportées à patronictl**

- Améliorer les dialogues pour le basculement planifié programmé et le redémarrage programmé (Rafia Sabih)

  Les dialogues précédents ne tenaient pas compte des actions planifiées et étaient donc trompeurs.

- Vérifier l'existence du fichier de configuration (Wilfried Roset)

  Être explicite au sujet du fichier de configuration lorsque le nom de fichier fourni n'existe pas, plutôt que de l'ignorer silencieusement (ce qui peut entraîner une mauvaise compréhension).

- Ajouter une valeur de secours pour `EDITOR` (Wilfried Roset)

  Lorsque la variable d'environnement `EDITOR` n'était pas définie, `patronictl edit-config` échouait avec `PatroniCtlException`. La nouvelle stratégie consiste à essayer d'abord `editor`, puis `vi`, qui devraient être disponibles sur la plupart des systèmes.

**Améliorations apportées au support de Consul**

- Permet de spécifier le mode de cohérence Consul (Jan Tomsa)

  Vous pouvez en savoir plus sur le mode de cohérence [ici](https://www.consul.io/api/features/consistency.html).

- Recharger la configuration de Consul lors d'un signal SIGHUP (Cameron Daniel Kucera, Alexander Kukushkin)

  Il est particulièrement utile lorsque quelqu’un modifie la valeur de `token`.

**Correctifs de bogues**

- Corriger un cas particulier lors du basculement planifié ou du basculement (Sharoon Thomas)

  La variable `scheduled_at` peut être non définie si l'API REST n'est pas accessible et que le DCS est utilisé comme solution de repli.

- Activer la confiance pour localhost dans `pg_hba.conf` pendant l'amorçage personnalisé (Alexander Kukushkin)

  Précédemment, il était ouvert uniquement via unix_socket, ce qui provoquait de nombreuses erreurs : `FATAL:  no pg_hba.conf entry for replication connection from host "127.0.0.1", user "replicator"`

- Considérer le nœud synchrone comme sain même lorsque l'ancien leader est en avance (Alexander Kukushkin)

  Si le primaire perd l'accès au DCS, il redémarre PostgreSQL en lecture seule, mais il se peut que d'autres nœuds puissent encore accéder à l'ancien primaire via l'API REST. Ce cas de figure entraînait une non-promotion du standby synchrone, car l'ancien primaire signalait une position WAL supérieure à celle du standby synchrone.

- Correctifs de bogues pour le cluster de secours (Alexander Kukushkin)

  Permettre l'amorçage d'une réplique dans un cluster de secours lorsque le standby_leader n'est pas accessible, ainsi que quelques autres corrections mineures.

--------

## Version 1.5.6 {#version-156}

Sorti le 2019-08-03

**Nouvelles fonctionnalités**

- Prise en charge du cluster etcd via un ensemble de proxys (Alexander Kukushkin)

  Il se peut que le cluster etcd ne soit pas accessible directement, mais via un ensemble de proxys. Dans ce cas, Patroni n'effectuera pas la découverte de la topologie etcd, mais effectuera un round-robin sur les hôtes proxy. Ce comportement est contrôlé par `etcd.use_proxies`.

- Modification du comportement des rappels lors du changement de rôle sur le nœud (Alexander Kukushkin)

  Si le rôle a été modifié depuis `master` ou `standby_leader` vers `replica` ou depuis `replica` vers `standby_leader`, le rappel `on_restart` ne sera plus appelé, en faveur du rappel `on_role_change`.

- Modifier la manière dont PostgreSQL est lancé (Alexander Kukushkin)

  Utilisez `multiprocessing.Process` au lieu d'exécuter le processus lui-même et `multiprocessing.Pipe` pour transmettre l'identifiant du processus postmaster au processus Patroni. Avant cela, nous utilisions des tubes, ce qui laissait le processus postmaster avec stdin fermé.

**Correctifs de bogues**

- Corriger le rôle retourné par l'API REST pour le standby leader (Alexander Kukushkin)

  Il renvoyait incorrectement `replica` au lieu de `standby_leader`

- Attendre la fin du rappel si celui-ci ne peut pas être interrompu (Julien Tachoires)

  Patroni ne dispose pas de suffisamment de privilèges pour terminer le script de rappel en cours d'exécution sous `sudo`. Cet échec entraînait l'annulation du nouveau rappel. Si le script en cours ne peut pas être arrêté, Patroni attendra qu'il se termine, puis exécutera le script de rappel suivant.

- Réduire la durée de maintien du verrou par la méthode dcs.get_cluster (Alexander Kukushkin)

  En raison du verrou maintenu, la lenteur du DCS affectait les contrôles de santé de l'API REST, provoquant des faux positifs.

- Améliorer le nettoyage du répertoire PGDATA lorsque `pg_wal`/`pg_xlog` est un lien symbolique (Julien Tachoires)

  Dans ce cas, Patroni supprimera explicitement les fichiers du répertoire cible.

- Supprimer l'utilisation inutile de os.path.relpath (Ants Aasma)

  Cela dépend de la possibilité de résoudre le répertoire de travail ; cela échouera si Patroni est lancé dans un répertoire qui est ultérieurement supprimé du système de fichiers.

- Ne pas imposer la version SSL lors de la communication avec etcd (Alexander Kukushkin)

  Pour une raison inconnue, les paquets python3-etcd sur Debian et Ubuntu ne sont pas basés sur la dernière version du paquet et imposent donc TLSv1, qui n’est pas pris en charge par etcd v3. Nous avons résolu ce problème du côté de Patroni.

--------

## Version 1.5.5 {#version-155}

Sorti le 2019-02-15

Cette version introduit la possibilité de réinitialisation automatique de l’ancien maître, améliore la sortie de la commande patronictl list et corrige un certain nombre de bogues.

**Nouvelles fonctionnalités**

- Ajouter le support des variables d'environnement `PATRONI_ETCD_PROTOCOL`, `PATRONI_ETCD_USERNAME` et `PATRONI_ETCD_PASSWORD` (Étienne M)

  Avant, il était possible de les configurer uniquement dans le fichier de configuration ou en tant que partie de `PATRONI_ETCD_URL`, ce qui n’est pas toujours pratique.

- Permettre la réinitialisation automatique de l'ancien maître (Alexander Kukushkin)

  Si pg_rewind est désactivé ou ne peut pas être utilisé, l'ancien nœud maître pourrait ne pas parvenir à démarrer en tant que nouvelle réplique en raison de timelines divergentes. Dans ce cas, la seule solution consiste à effacer le répertoire de données et à réinitialiser. Ce comportement peut être modifié en définissant `postgresql.remove_data_directory_on_diverged_timelines`. Lorsqu'il est défini, Patroni effacera automatiquement le répertoire de données et réinitialisera l'ancien nœud maître.

- Afficher les informations sur les timelines dans patronictl list (Alexander Kukushkin)

  Il aide à détecter les répliques obsolètes. En outre, `Host` inclura « :{port} » si la valeur du port n'est pas celle par défaut ou s'il y a plus d'un membre en cours d'exécution sur le même hôte.

- Créez un service sans tête associé au point d'extrémité \$SCOPE-config (Alexander Kukushkin)

  Le point de terminaison « config » conserve les informations relatives à la configuration Patroni et PostgreSQL au niveau du cluster, au fichier d'historique, et surtout, il contient la clé `initialize`. Lorsqu'un nœud maître Kubernetes est redémarré ou mis à jour, les points de terminaison sans service sont supprimés. Le service sans adresse IP (headless) empêche cette suppression.

**Correctifs de bogues**

- Ajuster le délai d'attente en lecture pour la requête bloquante de surveillance du leader (Alexander Kukushkin)

  Selon la documentation Consul, le délai d'attente réel de la réponse est augmenté d'un petit délai aléatoire ajouté au délai maximal fourni, afin de répartir les temps de réveil des requêtes concurrentes. Ce délai supplémentaire peut atteindre au maximum `wait / 16` en plus de la durée maximale. Dans notre cas, nous ajoutons `wait / 15` ou 1 seconde, selon la valeur la plus élevée.

- Utilisez toujours replication=1 lors de la connexion via le protocole de réplication à postgres (Alexander Kukushkin)

  À compter de PostgreSQL 10, la ligne dans pg_hba.conf avec database=replication n'accepte plus les connexions comportant le paramètre replication=database.

- Ne pas écrire primary_conninfo dans recovery.conf pour un cluster de secours wal-only (Alexander Kukushkin)

  Bien que ni `host` ni `port` ne soient définis dans la configuration du [standby_cluster](/fr/patroni/standby_cluster#standby_cluster), Patroni plaçait le `primary_conninfo` dans le `recovery.conf`, ce qui est inutile et génère de nombreuses erreurs.

--------

## Version 1.5.4 {#version-154}

Sorti le 2019-01-15

Cette version implémente une journalisation flexible et corrige plusieurs bogues.

**Nouvelles fonctionnalités**

- Améliorations de l'infrastructure de journalisation (Alexander Kukushkin, Lucas Capistrant, Alexander Anikin)

  La configuration de journalisation peut être définie non seulement à partir de variables d’environnement, mais également à partir du fichier de configuration Patroni. Cela permet de modifier la configuration de journalisation en temps réel en mettant à jour la configuration et en effectuant un rechargement ou en envoyant un signal SIGHUP au processus Patroni. Par défaut, Patroni écrit les journaux sur stderr, mais il est désormais possible d’écrire les journaux directement dans un fichier et de le faire tourner lorsque sa taille atteint un seuil défini. En outre, la prise en charge d’un format de date personnalisé a été ajoutée, ainsi que la possibilité de paramétrer finement le niveau de journalisation pour chaque module Python.

- Permettre de prendre en compte la timeline actuelle lors des élections de leader (Alexander Kukushkin)

  Il se peut que le nœud se considère comme le plus sain, même s’il n’est pas sur la dernière timeline connue. Dans certains cas, il est souhaitable d’éviter de promouvoir un tel nœud, ce qui peut être réalisé en définissant le paramètre `check_timeline` à `true` (le comportement par défaut reste inchangé).

- Conditions assouplies concernant les identifiants de superutilisateur

  Libpq permet d'ouvrir des connexions sans spécifier explicitement le nom d'utilisateur ni le mot de passe. Selon la situation, il s'appuie soit sur le fichier pgpass, soit sur la méthode d'authentification trust dans pg_hba.conf. Comme pg_rewind utilise également libpq, il fonctionne de la même manière.

- Implémenté la possibilité de configurer l'enregistrement du service Consul et l'intervalle de vérification via des variables d'environnement (Alexander Kukushkin)

  L'enregistrement du service dans Consul a été ajouté à partir de la version 1.5.0, mais jusqu'à présent, il n'était possible de l'activer que via patroni.yaml.

**Améliorations de la stabilité**

- Passez archive_mode à off pendant l'amorçage personnalisé (Alexander Kukushkin)

  Nous souhaitons éviter l'archivage des fichiers WAL et des fichiers d'historique jusqu'à ce que le cluster soit pleinement fonctionnel. Cela aide vraiment lorsque l'amorçage personnalisé implique pg_upgrade.

- Appliquer un délai de cinq secondes lors du chargement de la configuration globale au démarrage (Alexander Kukushkin)

  Cela permet d'éviter de surcharger le DCS lors du démarrage initial de Patroni.

- Réduire le nombre de messages d'erreur générés lors de l'arrêt (Alexander Kukushkin)

  Ils étaient inoffensifs mais plutôt ennuyeux et parfois effrayants.

- Sécuriser explicitement les permissions en lecture-écriture pour recovery.conf au moment de la création (Lucas Capistrant)

  Nous ne souhaitons pas que quiconque d'autre que l'utilisateur patroni/postgres puisse lire ce fichier, car il contient le nom d'utilisateur et le mot de passe de réplication.

- Rediriger les exceptions HTTPServer vers le journal (Julien Riou)

  Par défaut, ces exceptions étaient journalisées sur la sortie standard, ce qui perturbait les journaux réguliers.

**Correctifs de bogues**

- Suppression du tuyau stderr vers stdout pour le processus pg_ctl (Cody Coons)

  Hériter de stderr du processus principal Patroni permet de visualiser tous les journaux Postgres ainsi que tous les journaux Patroni. Cette fonctionnalité est particulièrement utile dans un environnement conteneurisé, où les journaux Patroni et Postgres peuvent être consommés à l’aide d’outils standards (docker logs, kubectl, etc.). En outre, ce changement corrige un bogue empêchant Patroni de capturer le PID du postmaster lorsque Postgres écrit des avertissements sur stderr.

- Définit le délai d'expiration de la désinscription de la vérification de service Consul au format Go time (Pavel Kirillov)

  L'enregistrement échouait sans unité de temps explicitement mentionnée.

- Relâcher les contrôles de configuration du cluster standby_cluster (Dmitry Dolgov, Alexander Kukushkin)

  Il acceptait uniquement des chaînes de caractères comme valeurs valides, ce qui rendait impossible de spécifier le port sous forme d'entier ou create_replica_methods sous forme de liste.

--------

## Version 1.5.3 {#version-153}

Sorti le 2018-12-03

Version de compatibilité et de correction de bogues.

- Améliorer la stabilité lors de l'exécution avec python3 contre zookeeper (Alexander Kukushkin)

  Le changement de `loop_wait` provoquait la déconnexion de Patroni de ZooKeeper, sans réconnection ultérieure.

- Corriger les incompatibilités avec PostgreSQL 9.3 (Alexander Kukushkin)

  Lors de l'ouverture d'une connexion de réplication, il faut spécifier replication=1, car la version 9.3 ne comprend pas replication='database'

- Assurez-vous de rafraîchir la session Consul au moins une fois par boucle HA et améliorez le traitement des exceptions liées aux sessions Consul (Alexander Kukushkin)

  Redémarrer l'agent Consul local invalide toutes les sessions associées au nœud. Ne pas appeler la mise à jour de session à temps et ne pas gérer correctement les erreurs de session entraînait la rétrogradation du primaire.

--------

## Version 1.5.2 {#version-152}

Sorti le 2018-11-26

Version de compatibilité et de correction de bogues.

- Compatibilité avec kazoo-2.6.0 (Alexander Kukushkin)

  Afin de garantir que les requêtes soient exécutées avec un délai approprié, Patroni redéfinit la méthode create_connection du module python-kazoo. La dernière version de kazoo a légèrement modifié la manière dont la méthode create_connection est appelée.

- Corriger le plantage de Patroni lorsque le cluster Consul perd son leader (Alexander Kukushkin)

  L'incident était dû à une implémentation incorrecte de la méthode touch_member, qui doit renvoyer une valeur booléenne et ne doit pas lever d'exceptions.

--------

## Version 1.5.1 {#version-151}

Sorti le 2018-11-01

Cette version introduit la prise en charge des slots de réplication permanents, ajoute la prise en charge de pgBackRest et corrige un certain nombre de bogues.

**Nouvelles fonctionnalités**

- Slots de réplication permanents (Alexander Kukushkin)

  Les slots de réplication permanents sont conservés lors d’un basculement ou d’un basculement planifié : Patroni sur le nouveau nœud primaire créera les slots de réplication configurés dès la promotion. Ces slots peuvent être configurés à l’aide de `patronictl edit-config`. La configuration initiale peut également être définie dans [bootstrap.dcs](/fr/patroni/config/yaml#yaml).

- Ajouter la prise en charge de pgBackRest (Yogesh Sharma)

  pgBackRest peut restaurer dans un dossier \$PGDATA existant, ce qui permet une restauration rapide car les fichiers non modifiés depuis la dernière sauvegarde sont ignorés. Pour prendre en charge cette fonctionnalité, un nouveau paramètre `keep_data` a été introduit. Voir la section [méthode de création de réplique](/fr/patroni/replica_bootstrap#custom_replica_creation) pour des exemples supplémentaires.

**Correctifs de bogues**

- Quelques correctifs de bogues dans le flux « cluster de secours » (Alexander Kukushkin)

  Veuillez consulter <https://github.com/patroni/patroni/pull/823> pour plus de détails.

- Corriger la vérification de santé de l'API REST lorsque la gestion du cluster est mise en pause et que le DCS n'est pas accessible (Alexander Kukushkin)

  La régression a été introduite dans <https://github.com/patroni/patroni/commit/90cf930036a9d5249265af15d2b787ec7517cf57>

--------

## Version 1.5.0 {#version-150}

Sorti le 2018-09-20

Cette version permet au cluster HA Patroni de fonctionner en mode standby (cluster de secours), introduit un support expérimental de l'exécution sous Windows et propose un nouveau paramètre de configuration pour inscrire le service PostgreSQL dans Consul.

**Nouvelles fonctionnalités**

- Cluster de secours (Dmitry Dolgov)

  Un ou plusieurs nœuds Patroni peuvent former un cluster de secours qui s'exécute en parallèle du cluster primaire (c’est-à-dire dans un autre centre de données) et se compose de nœuds de secours qui se répliquent à partir du maître du cluster primaire. Tous les nœuds PostgreSQL du cluster de secours sont des répliques ; l’une de ces répliques se désigne elle-même pour se répliquer directement à partir du maître distant, tandis que les autres se répliquent à partir d’elle selon une chaîne en cascade. Une description plus détaillée de cette fonctionnalité et quelques exemples de configuration sont disponibles [ici](/fr/patroni/standby_cluster#standby_cluster).

- Inscrire les services dans Consul (Pavel Kirillov, Alexander Kukushkin)

  Si le paramètre `register_service` de la [configuration Consul](/fr/patroni/config/yaml#consul_settings) est activé, le nœud enregistre un service nommé `scope` avec le tag `master`, `replica` ou `standby-leader`.

- Prise en charge expérimentale de Windows (Pavel Golub)

  À partir de maintenant, il est possible d'exécuter Patroni sous Windows, bien que le support Windows soit récent et n'ait pas bénéficié du même niveau de test dans des environnements réels que son équivalent Linux. Nous accueillons vos retours !

**Améliorations apportées à patronictl**

- Ajouter le drapeau patronictl -k/--insecure et la prise en charge du certificat restapi (Wilfried Roset)

  Autrefois, si l'API REST était protégée par des certificats auto-signés, [patronictl](/fr/patroni/patronictl#patronictl) échouait à les vérifier. Il n'existait aucun moyen de désactiver cette vérification. Il est désormais possible de configurer [patronictl](/fr/patroni/patronictl#patronictl) pour ignorer complètement la vérification du certificat ou de fournir les certificats de l'autorité de certification et du client dans la section [ctl:](/fr/patroni/config/yaml#patronictl_settings) de la configuration.

- Exclure les membres portant l'étiquette nofailover de la sortie de patronictl switchover/failover (Alexander Anikin)

  Précédemment, ces membres étaient incorrectement proposés comme candidats lors d’un basculement planifié ou d’un basculement, tous deux interactifs, via patronictl.

**Améliorations de stabilité**

- Éviter l'analyse des lignes de sortie non au format clé-valeur de pg_controldata (Alexander Anikin)

  Dans certains cas, pg_controldata peut produire des lignes sans caractère deux-points. Cela provoquait une erreur dans le code Patroni chargé d'analyser la sortie de pg_controldata, masquant ainsi le problème réel ; ces lignes apparaissent souvent dans un avertissement affiché par pg_controldata avant la sortie régulière, par exemple lorsque la version majeure du binaire ne correspond pas à celle du répertoire de données PostgreSQL.

- Ajouter le nom du membre au message d'erreur lors de l'élection du leader (Jan Mussler)

  Pendant l'élection du leader, Patroni se connecte à tous les membres connus du cluster et demande leur état. Cet état est écrit dans le journal de Patroni et inclut le nom du membre. Auparavant, si le membre n'était pas accessible, le message d'erreur ne précisait pas son nom, ne contenant que l'URL.

- Réserver immédiatement la position WAL lors de la création du slot de réplication (Alexander Kukushkin)

  À partir de la version 9.6, la fonction `pg_create_physical_replication_slot` propose un paramètre booléen supplémentaire `immediately_reserve`. Lorsqu’il est défini à `false`, qui est également la valeur par défaut, le slot ne réserve pas la position WAL jusqu’à la réception de la première connexion client, pouvant entraîner la perte de certains segments requis par le client pendant la fenêtre temporelle comprise entre la création du slot et la connexion initiale.

- Corriger un bug dans la réplication synchrone stricte (Alexander Kukushkin)

  Lors de l'exécution avec `synchronous_mode_strict: true`, dans certains cas, Patroni place `*` dans le `synchronous_standby_names`, ce qui modifie l'état de synchronisation pour la plupart des connexions de réplication en `potential`. Auparavant, Patroni ne pouvait pas sélectionner de candidat synchrone dans de telles circonstances, car il ne prenait en compte que ceux dont l'état était `async`.

--------

## Version 1.4.6 {#version-146}

Sorti le 2018-08-14

**Correctifs de bogues et améliorations de stabilité**

Cette version corrige un problème critique concernant le point de terminaison de l'API Patroni /master, qui renvoyait un statut 200 pour un nœud non maître. Il s'agit d'un problème de rapport, sans véritable split-brain, mais dans certaines circonstances, les clients pourraient être dirigés vers le nœud en lecture seule.

- Réinitialisation de l'état is_leader lors d'une rétrogradation (Alexander Kukushkin, Oleksii Kliukin)

  Assurez-vous que le membre du cluster rétrogradé cesse de répondre avec le code 200 à l'appel d'API /master.

- Ajouter un nouveau champ "cluster_unlocked" à la sortie de l'API (Dmitry Dolgov)

  Ce champ indique si le cluster dispose d'un maître en cours d'exécution. Il peut être utilisé lorsque la requête d'un autre nœud n'est pas possible, mais qu'une réplique est accessible.

--------

## Version 1.4.5 {#version-145}

Sorti le 2018-08-03

**Nouvelles fonctionnalités**

- Améliorer la journalisation lors de l'application de la nouvelle configuration PostgreSQL (Don Seiler)

  Patroni journalise les noms et les valeurs des paramètres modifiés.

- Compatibilité Python 3.7 (Christoph Berg)

  async est un mot-clé réservé dans python3.7

- Passez l'état à « stopped » dans le DCS lors de l'arrêt d'un membre (Tony Sorrentino)

  Cela affiche l'état du membre comme « stopped » dans la commande « patronictl list ».

- Améliorer le message journalisé lorsque postmaster.pid périmé correspond à un processus en cours (Ants Aasma)

  Le message précédent était d'une confusion totale.

- Implémenter la fonctionnalité patronictl reload (Don Seiler)

  Avant cela, il n’était possible de recharger la configuration que par l’appel d’une API REST ou en envoyant le signal SIGHUP au processus Patroni.

- Prendre et appliquer certains paramètres depuis controldata lors du démarrage en tant que réplique (Alexander Kukushkin)

  La valeur de `max_connections` et de certains autres paramètres définis dans la configuration globale peut être inférieure à celle réellement utilisée par le serveur primaire ; dans ce cas, la réplique ne peut pas démarrer et doit être corrigée manuellement. Patroni s'occupe désormais de cette situation en lisant et en appliquant la valeur provenant de `pg_controldata`, en lançant PostgreSQL et en définissant le drapeau `pending_restart`.

- Si défini, utilisez LD_LIBRARY_PATH lors du démarrage de postgres (Chris Fraser)

  Lors du démarrage de Postgres, Patroni transmettait précédemment les variables d’environnement PATH, LC_ALL et LANG si elles étaient définies. Il effectue désormais la même opération avec LD_LIBRARY_PATH. Cela devrait faciliter l’utilisation lorsque PostgreSQL est installé dans un emplacement non standard.

- Renommer create_replica_method en create_replica_methods (Dmitry Dolgov)

  Pour préciser qu'il s'agit effectivement d'un tableau. Le nom ancien est toujours pris en charge pour assurer la compatibilité descendante.

**Correctifs de bogues et améliorations de stabilité**

- Correction de la condition de démarrage de la réplique en raison de pg_rewind en état de pause (Oleksii Kliukin)

  Évitez de démarrer la réplique qui a déjà exécuté pg_rewind.

- Répondre avec un statut 200 à la vérification de santé du maître uniquement si update_lock a réussi (Alexander Kukushkin)

  Empêcher Patroni de s'auto-déclarer maître sur l'ancien maître (dégradé) si le DCS est partitionné.

- Corriger la compatibilité avec le nouveau module consul (Alexander Kukushkin)

  À compter de la version 1.1.0, python-consul a modifié son API interne et utilise désormais `list` à la place de `dict` pour passer les paramètres de requête.

- Gérer les exceptions provenant du thread de l'API REST de Patroni lors de l'arrêt (Alexander Kukushkin)

  Ces exceptions non interceptées maintenaient PostgreSQL en cours d'exécution lors de l'arrêt.

- Effectuer la récupération après incident uniquement lorsque PostgreSQL s'exécute en tant que maître (Alexander Kukushkin)

  Exiger que `pg_controldata` signale « in production », « shutting down » ou « in crash recovery ». Dans tous les autres cas, aucune récupération après panne n'est nécessaire.

- Améliorer la gestion des erreurs de configuration (Henning Jacobs, Alexander Kukushkin)

  Il est possible de modifier de nombreux paramètres en temps réel (y compris `restapi.listen`) en mettant à jour le fichier de configuration Patroni et en envoyant un signal SIGHUP au processus Patroni. Cette correction élimine les exceptions obscures du thread 'restapi' lorsque certains paramètres reçoivent des valeurs non valides.

--------

## Version 1.4.4 {#version-144}

Sorti le 2018-05-22

**Améliorations de stabilité**

- Corriger la condition de course dans poll_failover_result (Alexander Kukushkin)

  Il n’a pas affecté directement le basculement ni le basculement planifié, mais dans certains cas rares, il signalait un succès trop tôt, lorsque l’ancien leader libérait le verrou, entraînant un message 'Failed over to "None"' au lieu de 'Failed over to "desired-node"'.

- Traiter les noms de paramètres Postgres comme insensibles à la casse (Alexander Kukushkin)

  La plupart des paramètres Postgres utilisent des noms au format snake_case, mais trois exceptions à cette règle existent : DateStyle, IntervalStyle et TimeZone. Postgres accepte ces paramètres même lorsqu’ils sont écrits avec une casse différente (par exemple, timezone = 'some/tzn') ; toutefois, Patroni n’a pas pu trouver de correspondance insensible à la casse pour ces noms dans pg_settings et a ignoré ces paramètres en conséquence.

- Interrompre le démarrage si la connexion à une instance PostgreSQL en cours d'exécution est tentée et que le cluster n'est pas initialisé (Alexander Kukushkin)

  Patroni peut s'attacher à une instance Postgres déjà en cours d'exécution. Il est impératif de démarrer Patroni sur le nœud maître avant de passer aux répliques.

- Corriger le comportement de patronictl scaffold (Alexander Kukushkin)

  Passez un objet dict à `touch_member` au lieu d'une chaîne JSON encodée ; l'implémentation DCS s'occupera du codage.

- Ne pas rétrograder le maître si la mise à jour de la clé leader a échoué en pause (Alexander Kukushkin)

  Pendant une maintenance, un DCS peut commencer à refuser les requêtes d'écriture tout en continuant à répondre aux requêtes de lecture. Dans ce cas, Patroni mettait auparavant le nœud maître PostgreSQL en mode lecture seule après avoir échoué à mettre à jour le verrou leader dans le DCS.

- Synchroniser les slots de réplication lorsque Patroni détecte un nouveau processus postmaster (Alexander Kukushkin)

  Si PostgreSQL a été redémarré, Patroni doit s'assurer que la liste des slots de réplication correspond à ses attentes.

- Vérifier le sysid et synchroniser les slots de réplication après la sortie du mode pause (Alexander Kukushkin)

  En mode `maintenance`, il se peut que le répertoire de données ait été entièrement réécrit ; il est donc nécessaire de s'assurer que `Database system identifier` appartient toujours à notre cluster et que les slots de réplication sont synchronisés avec les attentes de Patroni.

- Corriger une éventuelle impossibilité de démarrage due à la présence d'un fichier de verrouillage postmaster dans un répertoire de données PostgreSQL (Alexander Kukushkin)

  Détecter une réutilisation du PID à partir du fichier de verrou du postmaster. Ce problème est plus susceptible de se produire si vous exécutez Patroni et Postgres dans un conteneur Docker.

- Renforcer la protection contre la suppression accidentelle du DCS (Alexander Kukushkin)

  Patroni dispose de nombreux mécanismes pour empêcher un basculement dans ce cas et peut aussi restaurer toutes les clés. Toutefois, avant cette modification, la suppression accidentelle de la clé /config désactivait le mode pause pendant un cycle de la boucle HA.

- Ne pas quitter lors de la découverte d'un ID système non valide (Oleksii Kliukin)

  Ne quittez pas lorsque l'ID système du cluster est vide ou ne passe pas le contrôle de validation. Dans ce cas, le cluster nécessite probablement une réinitialisation ; mentionnez-le dans le message de résultat. Évitez d'arrêter Patroni, faute de quoi la réinitialisation ne pourra pas avoir lieu.

**Compatibilité avec Kubernetes 1.10+**

- Ajout d'une vérification des sous-ensembles vides (Cody Coons)

  Kubernetes 1.10.0+ commence à retourner `Endpoints.subsets` défini sur `None` au lieu de `[]`.

**Améliorations de l'amorçage**

- Rendre la suppression de recovery.conf facultative (Brad Nicholson)

  Si `bootstrap.<custom_bootstrap_method_name>.keep_existing_recovery_conf` est définie et configurée sur `True`, Patroni ne supprimera pas le fichier `recovery.conf` existant. Cela est utile lors de l'amorçage à partir d'une sauvegarde avec des outils comme pgBackRest, qui génèrent automatiquement le `recovery.conf` approprié.

- Autoriser des options pour la méthode intégrée basebackup (Oleksii Kliukin)

  Il est désormais possible de fournir des options à la méthode intégrée basebackup en définissant la section `basebackup` dans la configuration, de manière similaire à la manière dont elles sont définies pour les méthodes de création de réplique personnalisées. La différence réside dans le format accepté par la section `basebackup` : puisque pg_basebackup accepte à la fois des options `--key=value` et `--key`, le contenu de la section peut être soit un dictionnaire de paires clé-valeur, soit une liste contenant des dictionnaires à un élément ou simplement des clés (pour les options qui ne prennent pas de valeur). Voir la section [méthode de création de réplique](/fr/patroni/replica_bootstrap#custom_replica_creation) pour des exemples supplémentaires.

--------

## Version 1.4.3 {#version-143}

Sorti le 2018-03-05

**Améliorations de la journalisation**

- Rendre le niveau de journalisation configurable via des variables d'environnement (Andy Newton, Keyvan Hedayati)

  `PATRONI_LOGLEVEL` - définit le niveau de journalisation général
  `PATRONI_REQUESTS_LOGLEVEL` - définit le niveau de journalisation pour toutes les requêtes HTTP, par exemple les appels à l'API Kubernetes
  Voir [documentation sur la journalisation Python](https://docs.python.org/3.6/library/logging.html#levels) pour obtenir la liste des niveaux de journalisation possibles

**Améliorations de stabilité et corrections de bogues**

- Ne pas redécouvrir la topologie du cluster etcd lorsque la surveillance expire (Alexander Kukushkin)

  Si nous n'avons qu'un seul hôte dans la configuration etcd et que cet hôte précis n'est pas accessible, Patroni tentait de découvrir la topologie du cluster sans jamais y parvenir. Il devrait plutôt passer à l'hôte suivant disponible.

- Écrivez le contenu de bootstrap.pg_hba dans un pg_hba.conf après l'amorçage personnalisé (Alexander Kukushkin)

  À présent, il se comporte de manière similaire à l'amorçage habituel avec `initdb`

- Le mode utilisateur unique attendait une entrée utilisateur et n’a jamais terminé (Alexander Kukushkin)

  La régression a été introduite dans <https://github.com/patroni/patroni/pull/576>

--------

## Version 1.4.2 {#version-142}

Sorti le 2018-01-30

**Améliorations apportées à patronictl**

- Renommer le basculement programmé en basculement planifié programmé (Alexander Kukushkin)

  Les fonctions de basculement et de basculement planifié ont été séparées à partir de la version 1.4, mais `patronictl list` signalait encore `Scheduled failover` au lieu de `Scheduled switchover`.

- Afficher les informations sur les redémarrages en attente (Alexander Kukushkin)

  Pour appliquer certains changements de configuration, il peut être nécessaire de redémarrer PostgreSQL. Patroni indiquait déjà ce besoin via l'API REST et lors de l'écriture de l'état du nœud dans le DCS, mais il n'existait aucun moyen simple de le faire apparaître.

- Faire en sorte que show-config fonctionne avec cluster_name provenant du fichier de configuration (Alexander Kukushkin)

  Il fonctionne de manière similaire à `patronictl edit-config`

**Améliorations de stabilité**

- Ne pas appeler pg_controldata pendant l'amorçage (Alexander Kukushkin)

  Pendant l’initialisation avec initdb ou un amorçage personnalisé, il existe une fenêtre temporelle durant laquelle pgdata n’est pas vide, mais pg_control n’a pas encore été écrit. Dans ce cas, l’appel à pg_controldata échouait avec des messages d’erreur.

- Gérer les exceptions levées par psutil (Alexander Kukushkin)

  La ligne de commande est lue et analysée à chaque appel de la méthode `cmdline()`. Il se peut que le processus examiné ait déjà disparu, auquel cas l'exception `NoSuchProcess` est levée.

**Améliorations du support Kubernetes**

- Ne pas masquer les erreurs provenant de l'API Kubernetes (Alexander Kukushkin)

  Un appel à l'API Kubernetes peut échouer pour diverses raisons. Dans certains cas, cet appel doit être réessayé ; dans d'autres, il faut enregistrer le message d'erreur et la trace de la pile d'exceptions. Ce changement facilitera le débogage des problèmes d'autorisations Kubernetes.

- Mettre à jour l'exemple Dockerfile Kubernetes pour installer Patroni à partir de la branche master (Maciej Szulik)

  Avant cela, il utilisait `feature/k8s`, qui est devenu obsolète.

- Ajouter une gestion RBAC appropriée pour exécuter Patroni sur k8s (Maciej Szulik)

  Ajoutez le compte de service affecté aux pods du cluster, le rôle qui ne possède que les autorisations nécessaires, et le rolebinding qui associe le compte de service au rôle.

--------

## Version 1.4.1 {#version-141}

Sorti le 2018-01-17

**Correctifs apportés à patronictl**

- Ne pas afficher le leader actuel dans la liste suggérée des membres vers lesquels effectuer un basculement. (Alexander Kukushkin)

  patronictl failover peut encore fonctionner lorsque le cluster dispose d’un leader, qui doit être exclu de la liste des membres vers lesquels un basculement est possible.

- Rendre l'outil patronictl switchover compatible avec l'API ancienne de Patroni (Alexander Kukushkin)

  En cas d'échec de l'appel API REST POST /switchover avec le code d'état 501, l'opération sera tentée à nouveau, mais cette fois vers le point de terminaison /failover.

--------

## Version 1.4 {#version-14}

Sorti le 2018-01-10

Cette version ajoute le support de Kubernetes en tant que DCS, permettant d'exécuter Patroni en tant qu'agent natif cloud dans Kubernetes sans déploiement supplémentaire d'etcd, Zookeeper ou Consul.

**Avis de mise à jour**

L’installation de Patroni via pip ne fournira plus automatiquement les dépendances relatives aux systèmes tels que etcd, Zookeeper, Consul ou Kubernetes, ni la prise en charge d’AWS. Pour activer ces fonctionnalités, il est nécessaire de les spécifier explicitement dans la commande pip install, par exemple `pip install 'patroni[etcd,kubernetes]'`.

**Prise en charge Kubernetes**

Implémentez un DCS basé sur Kubernetes. Les métadonnées des endpoints sont utilisées pour stocker la configuration et la clé du leader. Le champ métadonnées dans la définition des pods est utilisé pour stocker les données relatives aux membres. En plus de l'utilisation des endpoints, Patroni prend en charge les ConfigMaps. Vous trouverez davantage d'informations sur cette fonctionnalité dans le [chapitre Kubernetes de la documentation](/fr/patroni/kubernetes#kubernetes)

**Améliorations de stabilité**

- Extraire le processus postmaster dans un objet distinct (Ants Aasma)

  Cet objet identifie un processus postmaster en cours d'exécution par son identifiant de processus (pid) et son heure de démarrage, et simplifie la détection (et la résolution) des situations où le postmaster a été redémarré à l’insu de Patroni ou où le répertoire postgres a disparu du système de fichiers.

- Réduire le nombre de requêtes SELECT effectuées par Patroni à chaque itération du cycle HA (Alexander Kukushkin)

  À chaque itération de la boucle HA, Patroni doit connaître l’état de récupération et la position absolue du WAL. À partir de maintenant, Patroni exécutera une seule requête SELECT pour obtenir ces informations, au lieu de deux sur la réplique et trois sur le maître.

- Supprimer la clé leader à l'arrêt uniquement lorsque nous détenons le verrou (Ants Aasma)

  Suppression sans condition générant des exceptions inutiles et trompeuses.

**Améliorations apportées à patronictl**

- Ajouter la commande version à patronictl (Ants Aasma)

  Il affichera la version de Patroni installée ainsi que les versions des instances Patroni en cours d'exécution (si le nom du cluster est spécifié).

- Rendre facultative la spécification de l'argument cluster_name pour certaines commandes patronictl (Alexander Kukushkin, Ants Aasma)

  Il fonctionnera si patronictl utilise un fichier de configuration Patroni habituel avec `scope` défini.

- Afficher les informations concernant le basculement planifié programmé et le mode maintenance (Alexander Kukushkin)

  Avant cela, il était possible d'obtenir ces informations uniquement à partir des journaux de Patroni ou directement depuis le DCS.

- Améliorer `patronictl reinit` (Alexander Kukushkin)

  Parfois, `patronictl reinit` refusait de poursuivre lorsque Patroni était occupé par d'autres actions, notamment la tentative de démarrage de postgres. [patronictl](/fr/patroni/patronictl#patronictl) ne proposait aucune commande pour annuler ces actions longues, et la seule solution (dangereuse) consistait à supprimer manuellement le répertoire de données. La nouvelle implémentation de `reinit` annule de force les autres actions longues avant de procéder à la réinitialisation.

- Implémenter le drapeau `--wait` dans `patronictl pause` et `patronictl resume` (Alexander Kukushkin)

  Il fera attendre [patronictl](/fr/patroni/patronictl#patronictl) jusqu’à ce que l’action demandée soit reconnue par tous les nœuds du cluster. Ce comportement est obtenu en exposant le drapeau [pause](/fr/patroni/pause#pause) pour chaque nœud dans le DCS et via l’API REST.

- Renommer `patronictl failover` en `patronictl switchover` (Alexander Kukushkin)

  L'ancien `failover` n'était en réalité capable que d'un basculement planifié ; il refusait de s'exécuter dans un cluster ne comportant pas de leader.

- Modifier le comportement de `patronictl failover` (Alexander Kukushkin)

  Il fonctionnera même s’il n’y a pas de leader, mais dans ce cas, vous devrez spécifier explicitement un nœud qui doit devenir le nouveau leader.

**Exposer des informations sur la timeline et l'historique**

- Exposer la timeline actuelle dans le DCS et via l'API (Alexander Kukushkin)

  Stocke les informations concernant la timeline actuelle de chaque membre du cluster. Ces informations sont accessibles via l'API et sont stockées dans le DCS

- Stocker l'historique des promotions dans la clé /history dans le DCS (Alexander Kukushkin)

  En outre, stockez l'historique des timelines enrichi de l'horodatage de la promotion correspondante dans la clé /history du DCS et mettez-le à jour à chaque promotion.

**Ajouter des points de terminaison pour obtenir des répliques synchrones et asynchrones**

- Ajouter de nouveaux points de terminaison /sync et /async (Alexander Kukushkin, Oleksii Kliukin)

> Ces points de terminaison (également accessibles via /synchronous et /asynchronous) renvoient 200 uniquement pour les répliques synchrones et asynchrones respectivement (en excluant celles marquées comme `noloadbalance`).

**Autoriser plusieurs hôtes pour etcd**

- Ajouter un nouveau paramètre `hosts` à la configuration etcd (Alexander Kukushkin)

  Ce paramètre doit contenir la liste initiale des hôtes utilisés pour découvrir et peupler la liste des membres en cours d'exécution du cluster etcd. Si, pour une raison quelconque, cette liste d'hôtes découverts est épuisée (aucun hôte disponible à partir de cette liste), Patroni reviendra à la liste initiale fournie par le paramètre `hosts`.

--------

## Version 1.3.6 {#version-136}

Sorti le 2017-11-10

**Améliorations de stabilité**

- Vérifier l'heure de démarrage du processus lors de la vérification du statut de PostgreSQL. (Ants Aasma)

  Après un plantage qui ne nettoie pas postmaster.pid, un nouveau processus peut avoir le même PID, entraînant un résultat faux positif pour is_running(), ce qui provoque diverses anomalies de comportement.

- Arrêtez PostgreSQL avant l'amorçage lorsque le répertoire de données est perdu (ainlolcat)

  Lorsque le répertoire de données du maître est supprimé de force, le processus postgres peut rester en vie pendant un certain temps et empêcher la réplique créée à la place de ce maître précédent de démarrer ou de se répliquer. La correction fait en sorte que Patroni mette en cache le PID du postmaster et son heure de démarrage, puis termine l'ancien postmaster s'il est toujours en cours d'exécution après la suppression du répertoire de données correspondant.

- Effectuer une récupération après incident en mode utilisateur unique si le serveur principal PostgreSQL tombe en panne (Alexander Kukushkin)

  Il est dangereux de démarrer immédiatement en mode standby et impossible de faire fonctionner `pg_rewind` si PostgreSQL n’a pas été arrêté correctement. La récupération après incident en mode utilisateur unique ne s’active que si `pg_rewind` est activé ou s’il n’y a actuellement pas de maître.

**Améliorations de Consul**

- Permettre de fournir une configuration de datacenter pour Consul (Vilius Okockis, Alexander Kukushkin)

  Avant cela, Patroni communiquait toujours avec le datacenter de l'hôte sur lequel il s'exécutait.

- Envoyer toujours un jeton dans l’en-tête HTTP X-Consul-Token (Alexander Kukushkin)

  Si `consul.token` est défini dans la configuration de Patroni, nous l'envoyons toujours dans l'en-tête HTTP 'X-Consul-Token'. Le module python-consul cherche à rester « cohérent » avec l'API REST de Consul, qui n'accepte pas le jeton en tant que paramètre de requête pour l'API [session](https://www.consul.io/api/session.html), mais fonctionne toutefois avec l'en-tête 'X-Consul-Token'.

- Ajuster la durée de vie de la session si la valeur fournie est inférieure au minimum autorisé (Stas Fomin, Alexander Kukushkin)

  Il se peut que le TTL fourni dans la configuration Patroni soit inférieur au minimum supporté par Consul. Dans ce cas, l'agent Consul échoue à créer une nouvelle session. Sans session, Patroni ne peut pas créer de clés de membre ni de clé de leader dans le magasin de clés de Consul, ce qui entraîne un cluster défaillant.

**Autres améliorations**

- Définir un format de journal personnalisé via la variable d'environnement `PATRONI_LOGFORMAT` (Stas Fomin)

  Permet de désactiver les horodatages et d'autres champs similaires dans les journaux de Patroni si ces informations sont déjà ajoutées par le système de journalisation (généralement lorsque Patroni s'exécute en tant que service).

--------

## Version 1.3.5 {#version-135}

Sorti le 2017-10-12

**Correction de bogue**

- Définir le rôle sur « uninitialized » si le répertoire de données a été supprimé (Alexander Kukushkin)

  Si le nœud était en cours d'exécution en tant que maître, il empêchait le basculement.

**Amélioration de la stabilité**

- Essayez de lancer postmaster en mode utilisateur unique si nous avons tenté et échoué à démarrer postgres (Alexander Kukushkin)

  Ce problème survient généralement lorsque le nœud exécutant en tant que maître a été interrompu et que les lignes temporelles sont devenues divergentes. Si `recovery.conf` définit `restore_command`, il y a de très fortes chances que PostgreSQL interrompe le démarrage et laisse le controldata inchangé. Cela rend impossible l'utilisation de `pg_rewind`, qui nécessite une fermeture propre.

**Améliorations de Consul**

- Permettre de spécifier des contrôles de santé lors de la création d'une session (Alexander Kukushkin)

  Si non spécifié, Consul utilise « serfHealth ». D'une part, cela permet une détection rapide d'un maître isolé ; d'autre part, cela empêche Patroni de tolérer des perturbations réseau courtes.

**Correction de bogue**

- Corriger le watchdog sous Python 3 (Ants Aasma)

  Une mauvaise compréhension de l'interface de l'appel ioctl(). Si mutable=False, alors fcntl.ioctl() renvoie effectivement le tampon arg. Cela fonctionnait accidentellement sous Python2 car la comparaison entre int et str ne renvoyait pas d'erreur. La signalisation des erreurs se fait en effet par la levée d'une IOError sous Python2 et d'une OSError sous Python3.

--------

## Version 1.3.4 {#version-134}

Publié le 2017-09-08

**Améliorations apportées à Consul**

- Passez le jeton Consul en tant qu'en-tête (Andrew Colin Kissa)

  Les en-têtes sont désormais la méthode privilégiée pour transmettre le jeton à l'[API Consul](https://www.consul.io/api/index.html#authentication).

- Configuration avancée pour Consul (Alexander Kukushkin)

  possibilité de spécifier `scheme`, `token`, les certificats client et CA [détails](/fr/patroni/config/yaml#consul_settings).

- Compatibilité avec python-consul-0.7.1 et versions ultérieures (Alexander Kukushkin)

  Le module python-consul nouvellement introduit a modifié la signature de certaines méthodes

- Le message « Could not take out TTL lock » n’a jamais été journalisé (Alexander Kukushkin)

  Pas une erreur critique, mais le manque de journalisation appropriée complique l'investigation en cas de problème.

**Utiliser quote_ident pour échapper synchronous_standby_names**

- Lors de l'écriture de `synchronous_standby_names` dans `postgresql.conf`, sa valeur doit être entre guillemets (Alexander Kukushkin)

  Si elle n’est pas correctement entre guillemets, PostgreSQL désactive effectivement la réplication synchrone et continue de fonctionner.

**Plusieurs correctifs de bogues liés à l’état de pause, principalement liés au watchdog** (Alexander Kukushkin)

- Ne pas envoyer de messages de maintien de connexion si le watchdog n'est pas actif
- Éviter d'activer le watchdog en mode pause
- Définir l'état correct de PostgreSQL en mode pause
- Ne pas tenter d'exécuter des requêtes depuis l'API si PostgreSQL est arrêté

--------

## Version 1.3.3 {#version-133}

Sorti le 2017-08-04

**Correctifs de bogues**

- la réplication synchrone a été désactivée peu après la promotion, même lorsque synchronous_mode_strict était activé (Alexander Kukushkin)
- créer un fichier `pg_ident.conf` vide s'il est manquant après une restauration depuis une sauvegarde (Alexander Kukushkin)
- ouvrir l'accès dans `pg_hba.conf` à toutes les bases de données, et non seulement à postgres (Franco Bellagamba)

--------

## Version 1.3.2 {#version-132}

Sorti le 2017-07-31

**Correction de bogue**

- patronictl edit-config ne fonctionnait pas avec ZooKeeper (Alexander Kukushkin)

--------

## Version 1.3.1 {#version-131}

Sorti le 2017-07-28

**Correction de bogue**

- le basculement via l'API était défaillant en raison d'un changement apporté à `_MemberStatus` (Alexander Kukushkin)

--------

## Version 1.3 {#version-13}

Sorti le 2017-07-27

Version 1.3 ajoute la possibilité d'amorçage personnalisé, améliore considérablement le support de pg_rewind, renforce le support du mode synchrone, ajoute l'édition de configuration à patronictl et implémente le support du watchdog sous Linux. En outre, il s'agit de la première version fonctionnant correctement avec PostgreSQL 10.

**Avis de mise à jour**

Aucun problème de compatibilité n’est connu avec la nouvelle version de Patroni. La configuration issue de la version 1.2 devrait fonctionner sans modification. Il est possible de procéder à la mise à jour en installant les nouveaux paquets, puis en redémarrant Patroni (ce qui entraîne un redémarrage de PostgreSQL), ou en mettant d’abord Patroni en mode [pause](/fr/patroni/pause#pause), puis en redémarrant Patroni sur tous les nœuds du cluster (Patroni en mode pause ne tentera pas d’arrêter ou de démarrer PostgreSQL), avant de reprendre le mode normal à la fin.

**Amorçage personnalisé**

- Rendre le processus de bootstrap du cluster configurable (Alexander Kukushkin)

  Autoriser l'utilisation de scripts d'amorçage personnalisés au lieu de `initdb` lors de l'initialisation du premier nœud du cluster. La commande d'amorçage reçoit le nom du cluster et le chemin du répertoire de données. Le cluster résultant peut être configuré pour effectuer une récupération, permettant ainsi de procéder à un amorçage à partir d'une sauvegarde et de réaliser une récupération à un instant donné. Pour une description détaillée de cette fonctionnalité, consulter la [documentation](/fr/patroni/replica_bootstrap#custom_bootstrap).

**Prise en charge améliorée de pg_rewind**

- Décidez de l'exécution de pg_rewind en fonction des différences de timeline par rapport au maître actuel (Alexander Kukushkin)

  Précédemment, Patroni disposait d’un ensemble fixe de conditions déclenchant pg_rewind, à savoir lors du démarrage d’un ancien nœud maître, lors d’un basculement planifié vers le nœud désigné pour chaque autre nœud du cluster, ou lorsqu’une réplique portait l’étiquette nofailover. Tous ces cas ont en commun un risque que certaines répliques soient en avance par rapport au nouveau maître. Dans certains cas, pg_rewind ne faisait rien ; dans d’autres, il ne s’exécutait pas lorsque cela était nécessaire. Au lieu de s’appuyer sur cette liste limitée de règles, Patroni compare désormais les positions WAL du maître et de la réplique (en utilisant le protocole de réplication en streaming) afin de déterminer de manière fiable si un rewind est nécessaire pour la réplique.

**Mode de réplication synchrone strict**

- Améliorer le support de la réplication synchrone en ajoutant le mode strict (James Sewell, Alexander Kukushkin)

  Par défaut, lorsque le mode synchrone [synchronous_mode](/fr/patroni/replication_modes#synchronous_mode) est activé et qu’aucune réplique n’est attachée au maître, Patroni désactive la réplication synchrone afin de maintenir le maître disponible en écriture. L’option `synchronous_mode_strict` modifie ce comportement : lorsqu’elle est définie, Patroni ne désactive pas la réplication synchrone en l’absence de répliques, ce qui bloque effectivement tous les clients tentant d’écrire des données sur le maître. En plus de la garantie du mode synchrone, qui empêche toute perte de données due à un basculement automatique, le mode strict assure que chaque écriture est soit durablement stockée sur deux nœuds, soit non effectuée du tout si le cluster ne contient qu’un seul nœud.

**Édition de la configuration avec patronictl**

- Ajouter la modification de configuration à patronictl (Ants Aasma, Alexander Kukushkin)

  Ajouter la possibilité à patronictl de modifier la configuration dynamique d’un cluster stockée dans le DCS. La prise en charge permet de spécifier les paramètres/valeurs depuis la ligne de commande, d’invoquer l’éditeur défini par la variable d’environnement \$EDITOR, ou d’appliquer une configuration à partir d’un fichier YAML.

**Prise en charge du watchdog sous Linux**

- Implémenter la prise en charge du watchdog pour Linux (Ants Aasma)

  Prise en charge du watchdog logiciel Linux afin de redémarrer le nœud sur lequel Patroni ne s'exécute pas ou ne répond pas (par exemple en cas de charge élevée). Le watchdog logiciel Linux redémarre le nœud non réactif. Il est possible de configurer le périphérique watchdog à utiliser (`/dev/watchdog` par défaut) et le mode (on, automatic, off) depuis la section watchdog de la configuration de Patroni. Vous pouvez obtenir davantage d'informations dans la documentation du [watchdog](/fr/patroni/watchdog#watchdog).

**Ajouter la prise en charge de PostgreSQL 10**

- Patroni est compatible avec toutes les versions bêta de PostgreSQL 10 publiées à ce jour, et nous prévoyons qu'il le sera également avec PostgreSQL 10 lors de sa sortie.

**Améliorations mineures liées à PostgreSQL**

- Définir pg_hba.conf via le fichier de configuration Patroni ou la configuration dynamique dans le DCS (Alexander Kukushkin)

  Permet de définir le contenu de `pg_hba.conf` dans la sous-section `pg_hba` de la section `postgresql` de la configuration. Cela simplifie la gestion de `pg_hba.conf` sur plusieurs nœuds, car il suffit de le définir une seule fois dans le DCS au lieu de se connecter à chaque nœud, de le modifier manuellement et de recharger la configuration.

  Lorsqu'il est défini, le contenu de cette section remplace entièrement le `pg_hba.conf` actuel. Patroni l'ignore si le paramètre PostgreSQL `hba_file` est défini.

- Prise en charge de la connexion via un socket UNIX au cluster PostgreSQL local (Alexander Kukushkin)

  Ajoutez l'option `use_unix_socket` à la section `postgresql` de la configuration Patroni. Lorsqu'elle est définie à true et que l'option PostgreSQL `unix_socket_directories` n'est pas vide, permet à Patroni d'utiliser la première valeur de celle-ci pour se connecter au cluster PostgreSQL local. Si `unix_socket_directories` n'est pas définie, Patroni supposera sa valeur par défaut et omettra complètement le paramètre `host` dans la chaîne de connexion PostgreSQL.

- Prise en charge du changement des identifiants de superutilisateur et de réplication lors du rechargement (Alexander Kukushkin)

- Prise en charge du stockage des fichiers de configuration en dehors du répertoire de données PostgreSQL (@jouir)

  Ajoutez la directive de configuration `postgresql` `config_dir`. Elle est par défaut définie sur le répertoire de données et doit être accessible en écriture par Patroni.

**Correctifs de bogues et améliorations de stabilité**

- Gérer les exceptions EtcdEventIndexCleared et EtcdWatcherCleared (Alexander Kukushkin)

  Rétablissement plus rapide lorsque l'opération watch est terminée par etcd, en évitant les tentatives de réessai inutiles.

- Supprimer la boucle d'erreurs en cas d'échec d'etcd et réduire le bruit dans les journaux (Ants Aasma)

  Éviter de réessayer immédiatement et de générer des traces de pile dans les journaux lors des deuxième échecs de connexion etcd et suivants.

- Exporter les variables de locale lors du fork des processus PostgreSQL (Oleksii Kliukin)

  Éviter l'erreur fatale `postmaster became multithreaded during startup` dans les locales non anglaises pour PostgreSQL compilé avec NLS.

- Vérifications supplémentaires lors de la suppression du slot de réplication (Alexander Kukushkin)

  Dans certains cas, Patroni est empêché de supprimer le slot de réplication par l'envoyeur WAL.

- Tronquer le nom du slot de réplication à 63 caractères (NAMEDATALEN - 1) pour respecter les règles de nommage de PostgreSQL (Nick Scott)

- Corriger une condition de course entraînant l'ouverture de connexions supplémentaires vers le cluster PostgreSQL depuis Patroni (Alexander Kukushkin)

- Libérer la clé leader lorsque le nœud redémarre avec un répertoire de données vide (Alex Kerney)

- Mettre l'exécuteur asynchrone en état d'occupation lors de l'amorçage sans leader (Alexander Kukushkin)

  Une telle omission pourrait entraîner des erreurs indiquant que le nœud appartient à un cluster différent, car Patroni poursuivait son fonctionnement normal tout en étant amorcé par une méthode d'amorçage ne nécessitant pas la présence d'un leader dans le cluster.

- Améliorer la méthode de création de réplique WAL-E (Joar Wandborg, Alexander Kukushkin).

  - Utilisez csv.DictReader pour analyser les sauvegardes complètes WAL-E, en acceptant les dates ISO avec une séparation entre date et heure par un espace.
  - Prise en charge de la récupération de la position actuelle du WAL depuis la réplique afin d'estimer la quantité de WAL à restaurer. Auparavant, le code appelait des fonctions d'information système disponibles uniquement sur le nœud principal.

--------

## Version 1.2 {#version-12}

Sorti le 2016-12-13

Cette version apporte des améliorations importantes dans la gestion de la réplication synchrone, rend le processus de démarrage et le basculement plus fiables, ajoute le support de PostgreSQL 9.6 et corrige de nombreux bogues. En outre, la documentation, y compris ces notes de version, a été déplacée vers [https://patroni.readthedocs.io](https://patroni.readthedocs.io).

**Réplication synchrone**

- Ajouter le support de la réplication synchrone. (Ants Aasma)

  Ajoute une nouvelle variable de configuration [synchronous_mode](/fr/patroni/replication_modes#synchronous_mode). Lorsqu'elle est activée, Patroni gère `synchronous_standby_names` afin d'activer la réplication synchrone chaque fois qu'un serveur secondaire sain est disponible. Lorsque le mode synchrone est activé, Patroni ne bascule automatiquement vers un serveur secondaire que s'il était en réplication synchrone au moment de la panne du maître. Cela signifie effectivement qu'aucune transaction visible par l'utilisateur n'est perdue dans ce cas. Consultez la [documentation de la fonctionnalité](/fr/patroni/replication_modes#synchronous_mode) pour obtenir une description détaillée et les informations sur l'implémentation.

**Améliorations de la fiabilité**

- Ne tentez pas de mettre à jour la position du leader stockée dans la clé `leader optime` lorsque PostgreSQL n'est pas 100 % sain. Rétrogradez immédiatement en cas d'échec de la mise à jour de la clé leader. (Alexander Kukushkin)

- Exclure les nœuds défaillants de la liste des sources depuis lesquelles cloner la nouvelle réplique. (Alexander Kukushkin)

- Implémenter une stratégie de réessai et de délai d'attente pour Consul, similaire à celle utilisée pour etcd. (Alexander Kukushkin)

- Faites en sorte que `--dcs` et `--config-file` s'appliquent à toutes les options de [patronictl](/fr/patroni/patronictl#patronictl). (Alexander Kukushkin)

- Écrivez tous les paramètres PostgreSQL dans postgresql.conf. (Alexander Kukushkin)

  Il permet de démarrer PostgreSQL configuré par Patroni avec simplement `pg_ctl`.

- Éviter les exceptions lorsqu'aucun utilisateur n'est défini dans la configuration. (Kirill Pushkin)

- Autoriser la mise en pause d'un cluster défaillant. Avant cette correction, [patronictl](/fr/patroni/patronictl#patronictl) abandonnait si le nœud sur lequel il tentait d'exécuter la mise en pause était défaillant. (Alexander Kukushkin)

- Améliorer la fonctionnalité de surveillance du leader. (Alexander Kukushkin)

  Précédemment, les répliques surveillaient toujours la clé du leader (en attendant le délai d'attente ou un changement de la clé du leader). Avec cette modification, elles ne surveillent que lorsque PostgreSQL de la réplique est en état `running` et non lorsqu'il est arrêté, en cours de démarrage ou de redémarrage.

- Éviter les conditions de course lors de la gestion du signal SIGCHLD en tant que PID 1. (Alexander Kukushkin)

  Un état de course pouvait autrefois se produire lors de l'exécution à l'intérieur de conteneurs Docker, car le même processus dans Patroni assurait à la fois la création de nouveaux processus et la gestion du signal SIGCHLD provenant de ceux-ci. Ce changement utilise des fork/exec pour Patroni et laisse le processus PID 1 original chargé de gérer les signaux émis par les enfants.

- Corriger la restauration WAL-E. (Oleksii Kliukin)

  Précédemment, la restauration WAL-E utilisait le drapeau `no_master` pour éviter toute consultation du maître, ce qui faisait que Patroni choisissait toujours la restauration à partir des WAL plutôt que de `pg_basebackup`. Ce changement rétablit la signification d'origine de `no_master`, à savoir que la restauration WAL-E par Patroni peut être sélectionnée comme méthode de réplication si le maître n'est pas en cours d'exécution. Ce dernier état est vérifié en examinant la chaîne de connexion transmise à la méthode. En outre, cela rend le mécanisme de réessai plus robuste et gère d'autres détails subtils.

- Implémenter un cache de résolution DNS asynchrone. (Alexander Kukushkin)

  Éviter les échecs lorsque le DNS est temporairement indisponible (par exemple, en raison d’un trafic excessif reçu par le nœud).

- Implémenter l'état de démarrage et le délai d'attente pour le démarrage du maître. (Ants Aasma, Alexander Kukushkin)

  Précédemment, `pg_ctl` attendait une expiration du délai avant de considérer sans réserve que PostgreSQL était en cours d'exécution. Cela faisait apparaître PostgreSQL comme en cours d'exécution dans les listes alors qu'il ne l'était pas réellement, entraînant une condition de course qui pouvait provoquer un basculement, une récupération après panne, ou une récupération après panne interrompue par un basculement, avec un rewind manqué. Cette modification ajoute un paramètre `master_start_timeout` et introduit un nouvel état dans la boucle principale de haute disponibilité : `starting`. Lorsque `master_start_timeout` vaut 0, le basculement est immédiat en cas de panne du maître, dès qu'un candidat au basculement est disponible. Sinon, Patroni attend après avoir tenté de démarrer PostgreSQL sur le maître pendant la durée du délai ; une fois celui-ci expiré, il procède au basculement si possible. Les demandes de basculement manuel seront respectées même pendant la panne du maître, avant l'expiration du délai.

  Introduisez le paramètre `timeout` dans le point de terminaison d’API `restart` et dans la commande [patronictl](/fr/patroni/patronictl#patronictl). Lorsqu’il est défini et que le redémarrage prend plus de temps que le délai d’attente, PostgreSQL est considéré comme défaillant et les autres nœuds deviennent éligibles pour obtenir le verrou de leader.

- Corriger le comportement de `pg_rewind` en mode pause. (Ants Aasma)

  Éviter un redémarrage inutile en mode pause lorsque Patroni pense devoir effectuer un rewind mais que celui-ci n'est pas possible (par exemple, si `pg_rewind` est absent). Revenir aux valeurs par défaut de `libpq` pour `superuser` (utilisateur système par défaut) si l'authentification `superuser` est absente dans la section de configuration Patroni associée à `pg_rewind`.

- Exécution sérialisée des rappels. Interrompre le rappel précédent du même type lorsqu’un nouveau rappel est sur le point de s’exécuter. Corrige le problème de création de processus zombies lors de l’exécution des rappels. (Alexander Kukushkin)

- Évitez de promouvoir un ancien maître lorsque la clé leader est définie dans le DCS, mais que la mise à jour de cette clé leader échoue. (Alexander Kukushkin)

  Cela évite le problème d’un maître actuel qui continuerait à assumer son rôle lorsqu’il est isolé ensemble avec la minorité de nœuds dans etcd et d’autres systèmes de coordination (DCS) autorisant des lectures « incohérentes ».

**Divers**

- Ajouter l'option de configuration `post_init` lors de l'amorçage. (Alejandro Martínez)

  Patroni appellera le script spécifié par cet argument juste après avoir exécuté `initdb` et lancé PostgreSQL pour un nouveau cluster. Le script reçoit une URL de connexion avec `superuser`. Si un mot de passe est fourni, Patroni définit `PGPASSFILE` pour qu’il pointe vers le fichier `.pgpass` contenant le mot de passe. Si le script échoue, l’initialisation de Patroni échoue également. Cette fonctionnalité est utile pour ajouter de nouveaux utilisateurs ou créer des extensions dans le nouveau cluster.

- Ajouter la prise en charge de PostgreSQL 9.6. (Alexander Kukushkin)

  Utilisez `wal_level = replica` comme synonyme de `hot_standby`, en évitant le drapeau pending_restart lorsqu'il passe de l'un à l'autre. (Alexander Kukushkin)

**Améliorations de la documentation**

- Ajouter un [diagramme de la boucle principale](https://raw.githubusercontent.com/patroni/patroni/master/docs/ha_loop_diagram.png) de Patroni. (Alejandro Martínez, Alexander Kukushkin)

- Améliorer le fichier README en ajoutant le chart Helm et les liens vers les notes de version. (Lauri Apple)

- Déplacer la documentation Patroni vers `Read the Docs`. La documentation à jour est disponible sur [https://patroni.readthedocs.io](https://patroni.readthedocs.io). (Oleksii Kliukin)

  Rend la documentation facilement consultable depuis différents appareils (y compris les smartphones) et consultable par recherche.

- Déplacer le paquet vers le versionnement sémantique. (Oleksii Kliukin)

  Patroni suivra le schéma de version majeur.mineur.patch afin d'éviter de publier une nouvelle version mineure pour des correctifs mineurs mais critiques. Seules les notes de version de la version mineure seront publiées, incluant tous les correctifs.

--------

## Version 1.1 {#version-11}

Sorti le 2016-09-07

Cette version améliore la gestion du cluster Patroni grâce à la mise en place du mode pause, améliore la maintenance grâce à des redémarrages planifiés et conditionnels, renforce la résilience de l’interaction de Patroni avec etcd ou Zookeeper, et améliore considérablement patronictl.

**Avis de mise à jour**

Lors de la mise à jour à partir de versions inférieures à 1.0, consultez les notes de version de la version 1.0 pour en savoir plus sur le changement des identifiants et du format de configuration.

**Mode pause**

- Introduire le mode pause pour détacher temporairement Patroni de la gestion d'une instance PostgreSQL (Murat Kabilov, Alexander Kukushkin, Oleksii Kliukin).

  Précédemment, il fallait envoyer le signal SIGKILL à Patroni pour l’arrêter sans interrompre PostgreSQL. Le nouveau mode pause détache Patroni du cluster PostgreSQL sans arrêter Patroni lui-même. Ce comportement est similaire au mode maintenance dans Pacemaker. Patroni reste responsable de la mise à jour des clés des membres et du leader dans le DCS, mais il ne lancera, n’arrêtera ni ne redémarrera le serveur PostgreSQL dans le processus. Quelques exceptions existent, par exemple les basculements manuels, les réinitialisations et les redémarrages restent autorisés. Vous pouvez consulter [une description détaillée de cette fonctionnalité](/fr/patroni/pause#pause).

En outre, patronictl prend en charge de nouvelles commandes [pause](/fr/patroni/pause#pause) et `resume` pour activer ou désactiver le mode pause.

**Redémarrages planifiés et conditionnels**

- Ajouter des conditions à la commande d'API de redémarrage (Oleksii Kliukin)

  Ce changement améliore les redémarrages de Patroni en ajoutant plusieurs conditions pouvant être vérifiées afin d’effectuer le redémarrage. Ces conditions incluent le redémarrage lorsque le rôle PostgreSQL est soit un maître, soit une réplique, la vérification du numéro de version de PostgreSQL, ou encore le redémarrage uniquement lorsque celui-ci est nécessaire pour appliquer des modifications de configuration.

- Ajouter des redémarrages planifiés (Oleksii Kliukin)

  Il est désormais possible de planifier un redémarrage à une date ultérieure. Un seul redémarrage planifié par nœud est pris en charge. Il est possible d’annuler un redémarrage planifié s’il n’est plus nécessaire. La combinaison de redémarrages planifiés et conditionnels est prise en charge, permettant par exemple de planifier des mises à jour mineures de PostgreSQL la nuit, en redémarrant uniquement les instances exécutant une version mineure obsolète, sans ajouter de logique spécifique à PostgreSQL dans les scripts d’administration.

- Ajouter la prise en charge des redémarrages conditionnels et planifiés dans patronictl (Murat Kabilov).

  patronictl restart prend en charge plusieurs nouvelles options. Il existe également la commande patronictl flush pour supprimer les actions planifiées.

**Interaction robuste avec le DCS**

- Définir les délais d'attente de Kazoo en fonction de loop_wait (Alexander Kukushkin)

  Initialement, les valeurs de ping_timeout et connect_timeout étaient calculées à partir du délai de session négocié. Le paramètre loop_wait de Patroni n'était pas pris en compte. En conséquence, une seule tentative de nouvelle connexion pouvait prendre plus de temps que le délai de session, ce qui forçait Patroni à libérer le verrou et à se rétrograder.

  Ce paramétrage réduit les délais de ping et de connexion à la moitié de la valeur de loop_wait, accélérant la détection des problèmes de connexion tout en laissant suffisamment de temps pour tenter de renouveler la tentative de connexion avant de perdre le verrou.

- Mettre à jour la topologie etcd uniquement après la réussite de la requête d'origine (Alexander Kukushkin)

  Reportez la mise à jour de la topologie etcd connue par le client jusqu’après la requête initiale. Lors de la récupération de la topologie du cluster, implémentez les délais de nouvelle tentative en fonction du nombre de nœuds connu dans le cluster etcd. Cela fait préférer à notre client l’obtention des résultats de la requête à la mise à jour de la liste des nœuds.

  Ces modifications rendent les connexions de Patroni au DCS plus robustes face aux problèmes réseau.

**Patronictl, surveillance et configuration**

- Renvoyer des informations sur les répliques en streaming via l'API (Feike Steenbergen)

  Précédemment, il n’existait aucun moyen fiable de requêter Patroni concernant les instances PostgreSQL qui ne parvenaient pas à diffuser les modifications (par exemple, en raison de problèmes de connexion). Ce changement expose le contenu de pg_stat_replication via le point de terminaison /patroni.

- Ajouter la commande scaffold patronictl (Oleksii Kliukin)

  Ajoutez une commande permettant de créer une structure de cluster dans etcd. Le cluster est créé avec un sysid et un leader spécifiés par l'utilisateur, et les clés leader ainsi que les clés de membre sont rendues persistantes. Cette commande est utile pour créer des configurations dites « sans maître », dans lesquelles un cluster Patroni composé uniquement de répliques se synchronise à partir d'un nœud maître externe ignorant l'existence de Patroni. Par la suite, il est possible de supprimer la clé leader, ce qui permet de promouvoir l'un des nœuds Patroni et de remplacer le maître initial par un cluster HA basé sur Patroni.

- Ajouter l'option de configuration `bin_dir` pour localiser les binaires PostgreSQL (Ants Aasma)

  Il est utile de pouvoir spécifier explicitement l'emplacement des binaires PostgreSQL lorsque l'on utilise des distributions Linux prenant en charge l'installation de plusieurs versions de PostgreSQL en même temps.

- Permet de remplacer le chemin du fichier de configuration à l'aide de `custom_conf` (Alejandro Martínez)

  Permet de spécifier des chemins de fichiers de configuration personnalisés, qui ne seront pas gérés par Patroni, [détails](/fr/patroni/config/yaml#postgresql_settings).

**Correctifs de bogues et améliorations du code**

- Rendre Patroni compatible avec le schéma de nouvelle version de PostgreSQL 10 et versions ultérieures (Feike Steenbergen)

  Assurez-vous que Patroni comprend les numéros de version à deux chiffres lors de redémarrages conditionnels basés sur la version de PostgreSQL.

- Utilisez pkgutil pour trouver les modules DCS (Alexander Kukushkin)

  Utilisez le module Python dédié au lieu de parcourir manuellement les répertoires pour localiser les modules DCS.

- Appeler toujours le rappel on_start au démarrage de Patroni (Alexander Kukushkin)

  Précédemment, Patroni ne lançait aucune fonction de rappel lors de la connexion à un nœud déjà en cours d'exécution avec le rôle correct. Étant donné que les fonctions de rappel sont souvent utilisées pour acheminer les connexions clientes, cela pouvait entraîner l'échec de l'enregistrement du nœud en cours d'exécution dans le schéma de routage des connexions. Avec cette correction, Patroni appelle la fonction de rappel on_start même lorsqu'il se connecte à un nœud déjà en cours d'exécution.

- Ne supprimez pas les slots de réplication actifs (Murat Kabilov, Oleksii Kliukin)

  Évitez de supprimer des slots de réplication physique actifs sur le maître. PostgreSQL ne peut pas les supprimer de toute façon. Ce changement permet d'exécuter des répliques ou consommateurs non gérés par Patroni sur le maître.

- Fermer les connexions Patroni au démarrage de l'instance PostgreSQL (Alexander Kukushkin)

  Forcer Patroni à fermer toutes les connexions anciennes lors du démarrage d'un nœud PostgreSQL. Évite le piège de réutiliser des connexions anciennes si le postmaster a été tué avec SIGKILL.

- Remplacer les caractères non valides lors de la construction des noms de slot à partir des noms de membre (Ants Aasma)

  Assurez-vous que les noms de standby ne respectant pas les règles de nommage des slots n'entraînent pas l'échec de la création du slot ou du démarrage du standby. Remplacez les traits d'union dans les noms de slots par des traits de soulignement, et remplacez tous les autres caractères non autorisés dans les noms de slots par leurs codepoints Unicode.

--------

## Version 1.0 {#version-10}

Sorti le 2016-07-05

Cette version introduit la configuration dynamique globale, qui permet de modifier dynamiquement les paramètres de configuration de PostgreSQL et de Patroni pour l’ensemble du cluster HA. Elle inclut également de nombreux correctifs.

**Avis de mise à jour**

Lors de la mise à jour à partir de la version v0.90 ou inférieure, mettez à jour toutes les répliques avant le maître. Comme nous ne stockons plus les identifiants de réplication dans le DCS, une ancienne réplique ne pourra pas se connecter au nouveau maître.

**Configuration dynamique**

- Implémenter la configuration globale dynamique (Alexander Kukushkin)

  Introduire un nouveau point de terminaison de l'API REST /config afin de fournir les paramètres de configuration de PostgreSQL et de Patroni qui doivent être définis globalement pour l'ensemble du cluster HA (maître et toutes les répliques). Ces paramètres sont définis dans le DCS et, dans de nombreuses situations, peuvent être appliqués sans interrompre PostgreSQL ou Patroni. Patroni définit un indicateur spécial appelé « pending restart », visible via l'API, lorsqu'une ou plusieurs valeurs nécessitent un redémarrage de PostgreSQL. Dans ce cas, le redémarrage doit être effectué manuellement via l'API.

  Un signal SIGHUP envoyé à Patroni ou une requête POST vers /reload entraîne la relecture du fichier de configuration.

  Consultez la configuration [Patroni](/fr/patroni/config#config) pour les détails sur les paramètres pouvant être modifiés et l'ordre de traitement des sources de configuration.

  Le format du fichier de configuration *a changé* depuis la version 0.90. Patroni reste compatible avec les anciens fichiers de configuration, mais afin de bénéficier des paramètres d'amorçage, celui-ci doit être mis à jour. Les utilisateurs sont invités à procéder à cette mise à jour en se référant à la page de documentation [de la configuration dynamique](/fr/patroni/config/dynamic#dynamic).

**Configuration plus flexible**\*

- Rendre configurables la configuration PostgreSQL et le nom de la base de données à laquelle Patroni se connecte (Misja Hoebe)

  Introduire les paramètres de configuration `database` et `config_base_name`. Parmi d'autres fonctionnalités, cela permet d'exécuter Patroni avec PipelineDB et d'autres dérivés de PostgreSQL.

- Ajouter la possibilité de configurer certains paramètres de Patroni via des variables d'environnement (Alexander Kukushkin)

  Celles-ci incluent la portée, le nom du nœud et l'espace de noms, ainsi que les secrets, ce qui facilite l'exécution de Patroni dans un environnement dynamique, par exemple Kubernetes. Veuillez vous référer à la documentation des [variables d'environnement prises en charge](/fr/patroni/config/env#env) pour plus de détails.

- Mettez à jour le conteneur Docker intégré de Patroni pour tirer parti de la configuration basée sur les variables d'environnement (Feike Steenbergen).

- Ajouter le support Zookeeper à l'image Docker Patroni (Alexander Kukushkin)

- Séparer les options de configuration de Zookeeper et d'Exhibitor (Alexander Kukushkin)

- Faire que patronictl réutilise le code de Patroni pour lire la configuration (Alexander Kukushkin)

  Cela permet à patronictl de tirer parti de la configuration basée sur l'environnement.

- Définir le nom de l'application sur le nom du nœud dans primary_conninfo (Alexander Kukushkin)

  Cela simplifie l'identification et la configuration de la réplication synchrone pour un nœud donné.

**Améliorations apportées à la stabilité, à la sécurité et à l'ergonomie**

- Réinitialiser le sysid et ne pas appeler pg_controldata pendant la restauration d'une sauvegarde en cours (Alexander Kukushkin)

  Ce changement réduit le bruit généré par les vérifications de santé de l'API Patroni pendant l'initialisation longue de ce nœud à partir de la sauvegarde.

- Corriger plusieurs cas limites de pg_rewind (Alexander Kukushkin)

  Évitez d'exécuter pg_rewind si le cluster source n'est pas le maître.

  En outre, évitez de supprimer le répertoire de données lors d’un rewind infructueux, sauf si le nouveau paramètre *remove_data_directory_on_rewind_failure* est défini sur true. Par défaut, il est false.

- Supprimer les mots de passe de la chaîne de connexion de réplication dans le DCS (Alexander Kukushkin)

  Précédemment, Patroni utilisait toujours les identifiants de réplication extraits de l'URL PostgreSQL dans le DCS. Ce comportement a maintenant été modifié afin de prendre les identifiants depuis la configuration de Patroni. Les secrets (nom d'utilisateur et mot de passe de réplication) ne sont plus exposés dans le DCS.

- Corriger le mécanisme asynchrone autour de l'appel de démotion (Alexander Kukushkin)

  La commande demote s'exécute désormais entièrement de manière asynchrone, sans bloquer les interactions avec le DCS.

- Forcer patronictl à toujours envoyer l'en-tête d'autorisation si celui-ci est configuré (Alexander Kukushkin)

  Cela permet à patronictl d'émettre des requêtes « protégées », c’est-à-dire de redémarrage ou de réinitialisation, lorsque Patroni est configuré pour exiger une autorisation pour ces opérations.

- Gérer correctement l'exception SystemExit (Alexander Kukushkin)

  Évite les problèmes liés à l'arrêt incorrect de Patroni lors de la réception du signal SIGTERM

- Exemples de modèles HAProxy pour confd (Alexander Kukushkin)

  Génère et modifie dynamiquement la configuration HAProxy à partir de l’état Patroni dans le DCS à l’aide de confd

- Améliorer et restructurer la documentation afin de la rendre plus accessible aux nouveaux utilisateurs (Lauri Apple)

- L'API doit indiquer role=master lors de l'exécution de pg_ctl stop (Alexander Kukushkin)

  Rend les appels de rappel plus fiables, en particulier dans le cas d'arrêt d'un cluster. En outre, introduit l'option `pg_ctl_timeout` pour définir le délai d'attente des appels de démarrage, d'arrêt et de redémarrage via `pg_ctl`.

- Corriger la logique de réessai dans etcd (Alexander Kukushkin)

  Rendre les nouvelles tentatives plus prévisibles et plus robustes.

- Rendre le code Zookeeper plus résilient aux perturbations réseau courtes (Alexander Kukushkin)

  Réduisez les délais d’attente de connexion pour rendre les tentatives de connexion à Zookeeper plus fréquentes.

--------

## Version 0.90 {#version-090}

Sorti le 2016-04-27

Cette version ajoute la prise en charge de Consul, introduit une nouvelle balise *noloadbalance*, modifie le comportement de la balise *clonefrom*, améliore la gestion de *pg_rewind* et améliore le programme de contrôle *patronictl*.

**Prise en charge de Consul**

- Implémenter le support Consul (Alexander Kukushkin)

  Patroni fonctionne avec Consul, en plus d'etcd et de Zookeeper. Les paramètres de connexion peuvent être configurés dans le fichier YAML.

**Nouvelles et améliorées : balises**

- Implémenter l'étiquette *noloadbalance* (Alexander Kukushkin)

  Ce tag fait que Patroni indique toujours à l'équilibreur de charge que la réplique n'est pas disponible.

- Modifier l'implémentation de l'étiquette *clonefrom* (Alexander Kukushkin)

  Précédemment, un nom de nœud devait être fourni à l’option *clonefrom*, ce qui forçait une réplique étiquetée à se baser sur un nœud spécifique. La nouvelle implémentation rend *clonefrom* une balise booléenne : si elle est définie à true, la réplique devient candidate pour être utilisée comme source de clonage par d'autres répliques. Lorsque plusieurs candidates sont présentes, la réplique choisit aléatoirement l'une d'entre elles.

**Améliorations de stabilité et de sécurité**

- Plusieurs améliorations de fiabilité (Alexander Kukushkin)

  Supprime certains messages d'erreur parasites, améliore la stabilité du basculement, corrige certains cas limites liés à la lecture des données depuis le DCS, ainsi que les opérations d'arrêt, de démotion et de réattache de l'ancien leader.

- Améliorer le script système pour éviter de tuer les processus enfants de Patroni lors de l'arrêt (Jan Keirse, Alexander Kukushkin)

  Auparavant, lors de l'arrêt de Patroni, *systemd* envoyait également un signal à PostgreSQL. Comme Patroni tentait lui aussi d'arrêter PostgreSQL, des demandes d'arrêt différentes étaient envoyées : l'arrêt intelligent, puis l'arrêt rapide. Les réplicas se déconnectaient alors trop tôt et l'ancien primaire ne pouvait plus rejoindre le cluster après sa rétrogradation. Correctif de Jan, fondé sur les recherches préalables d'Alexander.

- Éliminer certains cas où l'ancien maître n'arrivait pas à exécuter pg_rewind avant de se rejoindre en tant que réplique (Oleksii Kliukin)

  Précédemment, nous ne lançions *pg_rewind* que si l'ancien maître avait planté. Modifiez ce comportement pour toujours exécuter *pg_rewind* sur l'ancien maître, à condition que *pg_rewind* soit présent dans le système. Cela corrige le cas où le maître est arrêté avant que les répliques n'aient pu récupérer les dernières modifications (par exemple, pendant un arrêt « smart »).

- De nombreuses améliorations apportées aux tests unitaires et d'acceptation, en particulier, permettent désormais le support de Zookeeper et de Consul (Alexander Kukushkin).

- Rendre Travis CI plus rapide et implémenter le support de l'exécution des tests contre Zookeeper (Exhibitor) et Consul (Alexander Kukushkin)

  Les tests unitaires et les tests d'acceptation s'exécutent automatiquement contre etcd, Zookeeper et Consul à chaque validation ou demande de fusion.

- Effacez les variables d'environnement avant d'appeler les commandes PostgreSQL depuis Patroni (Feike Steenbergen)

  Cela empêche la possibilité de lire les variables d'environnement système en se connectant au cluster PostgreSQL géré par Patroni.

**Modifications de configuration et de contrôle**

- Unifier patronictl et la configuration Patroni (Feike Steenbergen)

  patronictl peut utiliser le même fichier de configuration que Patroni lui-même.

- Activer la lecture de la configuration par Patroni depuis les variables d'environnement (Oleksii Kliukin)

  Cela simplifie la génération automatique de la configuration pour Patroni, ou la fusion d'une configuration unique provenant de différentes sources.

- Inclure l'identifiant du système de base de données dans les informations renvoyées par l'API (Feike Steenbergen)

- Implémenter *delete_cluster* pour tous les DCS disponibles (Alexander Kukushkin)

  Active la prise en charge de systèmes DCS autres qu'etcd dans patronictl.

--------

## Version 0.80 {#version-080}

Sorti le 2016-03-14

Cette version introduit la prise en charge de la *réplication en cascade* et simplifie la gestion de Patroni grâce aux *basculements programmés* (scheduled failovers). Il est possible d'utiliser des versions antérieures de Patroni (en particulier la 0.78) combinées à celle-ci afin de migrer vers la nouvelle version. Notez que les fonctionnalités liées au basculement programmé et à la réplication en cascade ne fonctionneront qu'avec Patroni 0.80 et versions ultérieures.

**Réplication en cascade**

> - Ajouter la prise en charge des balises *replicatefrom* et *clonefrom* pour le nœud Patroni (Oleksii Kliukin).
>
> La balise *replicatefrom* permet à une réplique d'utiliser un nœud arbitraire comme source, pas nécessairement le maître. La balise *clonefrom* fait de même pour la sauvegarde initiale. Ensemble, elles permettent à Patroni de prendre entièrement en charge la réplication en cascade.

- Ajouter le support pour exécuter les méthodes de réplication afin d'initialiser la réplique même en l'absence de connexion de réplication active (Oleksii Kliukin).

> Cela est utile pour créer des répliques à partir des instantanés stockés sur S3 ou FTP. Une méthode de réplication ne nécessitant pas de connexion de réplication active doit indiquer *no_master: true* dans la configuration YAML. Ces scripts seront toutefois exécutés dans l'ordre si une connexion de réplication est présente.

**Patronictl, améliorations de l'API et du DCS**

- Implémenter des basculements programmés (Feike Steenbergen).

  Les basculements peuvent être programmés pour avoir lieu à une heure future donnée, à l’aide de patronictl ou d’appels à l’API.

- Ajouter la prise en charge des paramètres *dbuser* et *password* dans patronictl (Feike Steenbergen).

- Ajouter la version de PostgreSQL à la sortie de vérification de santé (Feike Steenbergen).

- Améliorer le support de Zookeeper dans patronictl (Oleksandr Shulgin)

- Migrer vers python-etcd 0.4.3 (Alexander Kukushkin)

**Configuration**

- Ajouter un script de configuration système d'exemple pour Patroni (Jan Keirse).
- Corriger le problème de Patroni ignorant le nom d'utilisateur superutilisateur spécifié dans le fichier de configuration pour les connexions à la base de données (Alexander Kukushkin).
- Corriger la gestion du signal CTRL-C en créant un identifiant de session et un groupe de processus séparés pour le postmaster lancé par Patroni (Alexander Kukushkin).

**Tests**

- Ajouter des tests d'acceptation avec *behave* afin de vérifier des scénarios réels de fonctionnement de Patroni (Alexander Kukushkin, Oleksii Kliukin).

  Les tests peuvent être lancés manuellement à l’aide de la commande *behave*. Ils sont également lancés automatiquement pour les demandes de fusion et après chaque validation.

  Les notes de version pour certaines versions antérieures sont disponibles sur la [page GitHub du projet](https://github.com/patroni/patroni/releases).
