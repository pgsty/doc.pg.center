---
title: "Convertir un nœud autonome en cluster Patroni"
linkTitle: "Convertir un cluster existant"
weight: 140
icon: fa-solid fa-truck-moving
description: "Procédure de conversion des données PostgreSQL existantes en cluster Patroni."
module: [PATRONI]
categories: [Tâche]
aliases: [/patroni/existing_data/]
upstream_link: "https://patroni.readthedocs.io/en/latest/existing_data.html"
---

<a id="existing_data"></a>
Cette section décrit le processus de conversion d'une instance PostgreSQL autonome en cluster Patroni.

Pour déployer un cluster Patroni sans utiliser d'instance PostgreSQL préexistante, consultez plutôt [Exécution et configuration](/fr/docs/patroni/readme#running_configuring).

--------

## Procédure {#procedure}

Vous trouverez ci-dessous un aperçu des étapes permettant de convertir un cluster Postgres existant en cluster géré par Patroni. Dans ces étapes, nous supposons que tous les nœuds faisant partie du cluster existant sont actuellement en fonctionnement, et que vous *ne prévoyez pas* de modifier la configuration de Postgres pendant la migration. Les étapes :

1.  Créez les utilisateurs Postgres comme indiqué dans la section [authentification](/fr/docs/patroni/config/yaml#postgresql_settings) de la configuration Patroni. Vous trouverez des exemples de commandes SQL pour créer les utilisateurs dans le bloc de code ci-dessous, dans lequel vous devez remplacer les noms d'utilisateur et les mots de passe selon votre environnement. Si vous avez déjà les utilisateurs correspondants, vous pouvez ignorer cette étape.

    ``` sql
    -- Patroni superuser
    -- Replace PATRONI_SUPERUSER_USERNAME and PATRONI_SUPERUSER_PASSWORD accordingly
    CREATE USER PATRONI_SUPERUSER_USERNAME WITH SUPERUSER ENCRYPTED PASSWORD 'PATRONI_SUPERUSER_PASSWORD';

    -- Patroni replication user
    -- Replace PATRONI_REPLICATION_USERNAME and PATRONI_REPLICATION_PASSWORD accordingly
    CREATE USER PATRONI_REPLICATION_USERNAME WITH REPLICATION ENCRYPTED PASSWORD 'PATRONI_REPLICATION_PASSWORD';

    -- Patroni rewind user, if you intend to enable use_pg_rewind in your Patroni configuration
    -- Replace PATRONI_REWIND_USERNAME and PATRONI_REWIND_PASSWORD accordingly
    CREATE USER PATRONI_REWIND_USERNAME WITH ENCRYPTED PASSWORD 'PATRONI_REWIND_PASSWORD';
    GRANT EXECUTE ON function pg_catalog.pg_ls_dir(text, boolean, boolean) TO PATRONI_REWIND_USERNAME;
    GRANT EXECUTE ON function pg_catalog.pg_stat_file(text, boolean) TO PATRONI_REWIND_USERNAME;
    GRANT EXECUTE ON function pg_catalog.pg_read_binary_file(text) TO PATRONI_REWIND_USERNAME;
    GRANT EXECUTE ON function pg_catalog.pg_read_binary_file(text, bigint, bigint, boolean) TO PATRONI_REWIND_USERNAME;
    ```

2.  Effectuez les étapes suivantes sur tous les nœuds Postgres. Effectuez toutes les étapes sur un nœud avant de passer au nœud suivant. Commencez par le nœud primaire, puis passez à chaque nœud de secours :

    1.  Si vous exécutez Postgres via systemd, désactivez l'unité systemd de Postgres. Patroni gère le démarrage et l'arrêt du démon Postgres, il est donc nécessaire de désactiver cette unité.
    2.  Créez un fichier de configuration YAML pour Patroni. Vous pouvez utiliser l'[outil de génération et de validation de la configuration Patroni](/fr/docs/patroni/config#validate_generate_config) à cette fin.
        - **Note (spécifique au nœud primaire) :** Si vous utilisez des slots de réplication pour la réplication entre les membres du cluster, il est recommandé d'activer `use_slots` et de configurer les slots de réplication existants comme permanents via l'élément de configuration `slots`. Prenez garde au fait que Patroni crée automatiquement des slots de réplication pour la réplication entre les membres, et supprime les slots qu'il ne reconnaît pas, lorsque `use_slots` est activé. L'idée d'utiliser des slots permanents consiste à permettre à vos slots existants de persister pendant la migration vers Patroni. Consultez [Paramètres de configuration dynamique](/fr/docs/patroni/config/dynamic#dynamic) pour plus de détails.
    3.  Démarrez Patroni à l'aide de l'unité de service systemd `patroni`. Patroni détecte automatiquement que Postgres est déjà en cours d'exécution et commence à surveiller l'instance.

3.  Transférez la procédure de démarrage de Postgres à Patroni. Pour cela, vous devez redémarrer les membres du cluster à l'aide de la commande [patronictl restart cluster-name member-name](/fr/docs/patroni/patronictl#patronictl_restart_parameters). Pour une indisponibilité minimale, vous pouvez souhaiter diviser cette étape en :

    1.  Redémarrage immédiat des nœuds de secours.
    2.  Redémarrage planifié du nœud primaire au sein d'une fenêtre de maintenance.

4.  Si vous avez configuré des slots permanents à l'étape `2.2.`, vous devriez les supprimer de la configuration `slots` à l'aide de la commande [patronictl edit-config cluster-name](/fr/docs/patroni/patronictl#patronictl_edit_config_parameters) une fois que le `restart_lsn` des slots créés par Patroni a rattrapé le `restart_lsn` des slots originaux pour les membres correspondants. En supprimant les slots de la configuration `slots`, vous permettez à Patroni de supprimer les slots originaux de votre cluster une fois qu'ils ne sont plus nécessaires. Vous trouverez ci-dessous une requête d'exemple pour vérifier le `restart_lsn` de quelques slots, afin de les comparer :

    ``` sql
    -- Assume original_slot_for_member_x is the name of the slot in your original
    -- cluster for replicating changes to member X, and slot_for_member_x is the
    -- slot created by Patroni for that purpose. You need restart_lsn of
    -- slot_for_member_x to be >= restart_lsn of original_slot_for_member_x
    SELECT slot_name,
           restart_lsn
    FROM pg_replication_slots
    WHERE slot_name IN (
        'original_slot_for_member_x',
        'slot_for_member_x'
    )
    ```

<a id="major_upgrade"></a>

## Mise à niveau majeure de la version PostgreSQL {#major-upgrade-of-postgresql-version}

La procédure de mise à niveau majeure avec `pg_upgrade` est la suivante :

1.  Arrêtez Patroni
2.  Mettez à jour les binaires PostgreSQL et exécutez [pg_upgrade](https://www.postgresql.org/docs/current/pgupgrade.html) sur le nœud primaire
3.  Mettez à jour patroni.yml
4.  Supprimez la clé `initialize` du DCS ou effacez l'état complet du cluster du DCS. La deuxième option peut être réalisée en exécutant [patronictl remove cluster-name](/fr/docs/patroni/patronictl#patronictl_remove_parameters). Cela est nécessaire car le nouveau cluster PostgreSQL est initialisé avec initdb, ce qui lui attribue un nouvel identifiant système PostgreSQL.
5.  Si vous avez effacé l'état du cluster à l'étape précédente, vous pouvez souhaiter copier patroni.dynamic.json depuis le répertoire de données ancien vers le nouveau. Cela vous aidera à conserver certains paramètres PostgreSQL que vous aviez définis auparavant.
6.  Démarrez Patroni sur le nœud primaire.
7.  Mettez à jour les binaires PostgreSQL, mettez à jour patroni.yml et effacez le data_dir sur les nœuds de secours.
8.  Démarrez Patroni sur les nœuds de secours et attendez la fin de la réplication.

L'exécution de pg_upgrade sur des nœuds de secours n'est pas prise en charge par PostgreSQL. Si vous savez ce que vous faites, vous pouvez essayer la procédure rsync décrite dans <https://www.postgresql.org/docs/current/pgupgrade.html> au lieu d'effacer le data_dir sur les nœuds de secours. La méthode la plus sûre reste toutefois de laisser Patroni effectuer la réplication des données pour vous.

--------

## FAQ {#faq}

- Lors du démarrage de Patroni, Patroni signale qu'il ne peut pas se lier au port PostgreSQL.

  Vous devez vérifier `listen_addresses` et `port` dans `postgresql.conf` et `postgresql.listen` dans `patroni.yml`. N'oubliez pas que `pg_hba.conf` devrait autoriser un tel accès.

- Après avoir demandé à Patroni de redémarrer le nœud, PostgreSQL affiche le message d'erreur `could not open configuration file "/etc/postgresql/10/main/pg_hba.conf": No such file or directory`

  Cela peut signifier différentes choses selon la manière dont vous gérez la configuration de PostgreSQL. Si vous avez spécifié `postgresql.config_dir`, Patroni génère le `pg_hba.conf` à partir des paramètres de la section [amorçage](/fr/docs/patroni/config/yaml#bootstrap_settings) uniquement lorsqu’il amorce un nouveau cluster. Dans ce scénario, le `PGDATA` n’était pas vide, par conséquent, aucun amorçage n’a eu lieu. Ce fichier doit exister au préalable.
