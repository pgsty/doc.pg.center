---
title: "Création de répliques et amorçage"
linkTitle: "Amorçage de réplique"
weight: 60
icon: fa-solid fa-boxes-stacked
description: "Création de répliques, amorçage et méthodes personnalisées de création de répliques."
module: [PATRONI]
categories: [Tâche]
aliases: [/patroni/replica_bootstrap/]
upstream_link: "https://patroni.readthedocs.io/en/latest/replica_bootstrap.html"
---

<a id="replica_imaging_and_bootstrap"></a>
Patroni permet de personnaliser la création d'une nouvelle réplique. Il prend également en charge la définition des actions à effectuer lors de l'amorçage d'un nouveau cluster vide. La distinction entre les deux est clairement établie : Patroni crée des répliques uniquement si la clé `initialize` est présente dans le DCS pour le cluster. Si la clé `initialize` est absente, Patroni lance l'amorçage exclusivement sur le premier nœud qui obtient le verrou de la clé `initialize`.

<a id="custom_bootstrap"></a>

--------

## Amorçage {#bootstrap}

PostgreSQL fournit la commande `initdb` pour initialiser un nouveau cluster, et Patroni l'appelle par défaut. Dans certains cas, notamment lors de la création d'un nouveau cluster à partir d'une copie d'un cluster existant, il est nécessaire de remplacer la méthode intégrée par des actions personnalisées. Patroni prend en charge l'exécution de scripts définis par l'utilisateur pour amorcer de nouveaux clusters, en leur fournissant certains arguments requis, tels que le nom du cluster et le chemin du répertoire de données. Cette configuration est définie dans la section `bootstrap` de la configuration de Patroni. Par exemple :

```yaml
bootstrap:
    method: <custom_bootstrap_method_name>
    <custom_bootstrap_method_name>:
        command: <path_to_custom_bootstrap_script> [param1 [, ...]]
        keep_existing_recovery_conf: False
        no_params: False
        recovery_conf:
            recovery_target_action: promote
            recovery_target_timeline: latest
            restore_command: <method_specific_restore_command>
```

Chaque méthode d’amorçage personnalisée doit être nommée par le paramètre `method` et définir une `command` dans la section portant ce nom. Une méthode spéciale `initdb` est disponible pour déclencher le comportement par défaut, auquel cas le paramètre `method` peut être omis entièrement. La `command` peut utiliser un chemin absolu, un chemin relatif au répertoire de travail de Patroni ou le nom d’une commande disponible dans `PATH`. En complément des paramètres fixes définis dans les fichiers de configuration, Patroni fournit deux paramètres spécifiques au cluster :

`--scope`  
Nom du cluster à amorcer

`--datadir`  
Chemin vers le répertoire de données de l'instance de cluster à amorcer

La transmission de ces deux drapeaux supplémentaires peut être désactivée en définissant un paramètre spécial `no_params` à `True`.

Si le script d'amorçage retourne `0`, Patroni tente de configurer et de démarrer l'instance PostgreSQL qu'il a produite. Si l'une des étapes intermédiaires échoue, ou si le script retourne une valeur différente de zéro, Patroni considère que l'amorçage a échoué, nettoie après lui-même et libère le verrou d'initialisation afin de permettre à un autre nœud de tenter l'amorçage.

Si un bloc `recovery_conf` est défini dans la même section que la méthode d'amorçage personnalisée, Patroni générera un `recovery.conf` avant de démarrer l'instance nouvellement amorcée (ou définira les paramètres de récupération dans la configuration de PostgreSQL si PostgreSQL est en version \>= 12). En général, cette configuration de récupération devrait contenir au moins l'un des paramètres `recovery_target_*`, accompagné du paramètre `recovery_target_action` défini sur `promote`.

Si `keep_existing_recovery_conf` est défini et positionné à `True`, Patroni ne supprimera pas le fichier `recovery.conf` existant s'il existe (PostgreSQL \<= 11). De même, dans ce cas, Patroni ne supprimera pas le fichier `recovery.signal` ou `standby.signal` existant s'il existe, ni ne remplacera les paramètres de récupération configurés (PostgreSQL \>= 12). Cela est utile lors du démarrage à partir d'une sauvegarde avec des outils comme pgBackRest, qui génèrent automatiquement la configuration de récupération appropriée.

En outre, toutes les paires clé/valeur supplémentaires indiquées dans la configuration de la méthode d'amorçage personnalisée seront passées en tant qu'arguments à `command` au format `--name=value`. Par exemple :

```yaml
bootstrap:
    method: <custom_bootstrap_method_name>
    <custom_bootstrap_method_name>:
        command: <path_to_custom_bootstrap_script>
        arg1: value1
        arg2: value2
```

Le `command` configuré sera alors appelé avec, en plus, les arguments en ligne de commande `--arg1=value1 --arg2=value2`.

> [!NOTE]
> Les méthodes d'amorçage ne sont ni chaînées, ni remplacées par celle par défaut en cas d'échec de la méthode principale

Par exemple, vous pouvez amorcer un cluster Patroni vierge à partir d'une sauvegarde Barman avec une configuration de ce type :

```yaml
bootstrap:
    method: barman
    barman:
        keep_existing_recovery_conf: true
        command: patroni_barman --api-url https://barman-host:7480 recover
        barman-server: my_server
        ssh-command: ssh postgres@patroni-host
```

> [!NOTE]
> `patroni_barman recover` nécessite que Barman et `pg-backup-api` soient configurés sur l'hôte Barman, afin de pouvoir exécuter un `barman recover` distant via l'API de sauvegarde. L'exemple ci-dessus utilise un sous-ensemble des paramètres disponibles. Vous pouvez obtenir davantage d'informations en exécutant `patroni_barman recover --help`.

<a id="custom_replica_creation"></a>

--------

## Construction de répliques {#building-replicas}

Patroni utilise `pg_basebackup`, éprouvé et fiable, afin de créer de nouvelles répliques. Il nécessite une instance PostgreSQL source en cours d’exécution et ne fournit pas de nettoyage intégré des fichiers de sauvegarde obsolètes. Certains utilisateurs préfèrent d'autres solutions de sauvegarde, telles que `WAL-E`, `pgBackRest`, `Barman` et d'autres, ou simplement concevoir leurs propres scripts. Afin de prendre en charge tous ces cas d'utilisation, Patroni prend en charge l'exécution de scripts personnalisés pour cloner une nouvelle réplique. Ceux-ci sont configurés dans le bloc de configuration `postgresql` :

```yaml
postgresql:
    create_replica_methods:
        - <method name>
    <method name>:
        command: <command name>
        keep_data: True
        no_params: True
        no_leader: 1
```

exemple : wal_e

```yaml
postgresql:
    create_replica_methods:
        - wal_e
        - basebackup
    wal_e:
        command: patroni_wale_restore
        no_leader: 1
        envdir: '{{WALE_ENV_DIR}}'
        use_iam: 1
    basebackup:
        max-rate: '100M'
```

exemple : pgBackRest

```yaml
postgresql:
    create_replica_methods:
        - pgbackrest
        - basebackup
    pgbackrest:
        command: /usr/bin/pgbackrest --stanza=<scope> --delta restore
        keep_data: True
        no_params: True
    basebackup:
        max-rate: '100M'
```

exemple : Barman

```yaml
postgresql:
    create_replica_methods:
        - barman
        - basebackup
    barman:
        command: patroni_barman --api-url https://barman-host:7480 recover
        barman-server: my_server
        ssh-command: ssh postgres@patroni-host
    basebackup:
        max-rate: '100M'
```

> [!NOTE]
> `patroni_barman recover` nécessite que Barman et `pg-backup-api` soient configurés sur l'hôte Barman, afin de pouvoir exécuter un `barman recover` distant via l'API de sauvegarde. L'exemple ci-dessus utilise un sous-ensemble des paramètres disponibles. Vous pouvez obtenir davantage d'informations en exécutant `patroni_barman recover --help`.

Le `create_replica_methods` définit les méthodes disponibles pour créer une réplique ainsi que l'ordre d'exécution. Patroni s'arrête à la première méthode qui retourne 0. Chaque méthode devrait définir une section distincte dans le fichier de configuration, en précisant la commande à exécuter et les paramètres personnalisés à passer à cette commande. Tous les paramètres seront transmis au format `--name=value`. Outre les paramètres définis par l'utilisateur, Patroni fournit plusieurs paramètres spécifiques au cluster :

`--scope`  
Cluster auquel cette réplique appartient

`--datadir`  
Chemin vers le répertoire de données de la réplique

`--role`  
Toujours « replica »

`--connstring`  
Chaîne de connexion pour se connecter au membre du cluster à cloner (primaire ou autre réplique). L'utilisateur figurant dans la chaîne de connexion peut exécuter des commandes SQL et des commandes du protocole de réplication.

Un paramètre spécial `no_leader`, lorsqu’il est activé, permet à Patroni d'appeler la méthode de création de réplique même en l'absence de leader en cours d'exécution ou de répliques. Dans ce cas, une chaîne de connexion vide sera passée. Cela est utile pour restaurer un cluster précédemment en cours d'exécution à partir d'une sauvegarde binaire.

Un paramètre spécial `keep_data`, lorsqu’il est activé, indique à Patroni de ne pas nettoyer le dossier PGDATA avant d'appeler la restauration.

Un paramètre spécial `no_params`, lorsqu’il est activé, désactive l’ajout automatique des paramètres spécifiques au cluster à la commande personnalisée. Les paramètres définis par l’utilisateur sont toujours transmis.

Une méthode `basebackup` est un cas particulier : elle sera utilisée si `create_replica_methods` est vide, même si elle peut être explicitement listée parmi les méthodes `create_replica_methods`. Cette méthode initialise une nouvelle réplique avec `pg_basebackup` ; la sauvegarde de base est extraite depuis le leader, sauf s’il existe des répliques étiquetées `clonefrom`, auquel cas l’une de ces répliques sera utilisée comme origine pour pg_basebackup. Elle fonctionne sans configuration ; toutefois, il est possible de spécifier une section de configuration `basebackup`. Les mêmes règles que pour la configuration des autres méthodes s’appliquent, à savoir que seules les options longues (avec --) devraient être indiquées. Patroni n’accepte ni le remplacement des paramètres de connexion ni les options produisant des sauvegardes au format tar ou compressées côté client. À partir de PostgreSQL 15, la compression côté serveur est prise en charge avec `compress: server-gzip` ou `compress: server-zstd`. Patroni filtre les options qu’il contrôle et les réglages de compression autres que la compression côté serveur, mais n’effectue pas de validation complète de tous les noms et valeurs des options. Notez également que, dans le cas où des liens symboliques sont utilisés pour le dossier WAL, il incombe à l’utilisateur de spécifier le chemin correct `--waldir` en tant qu’option, afin que le lien symbolique soit conservé après la construction ou la réinitialisation de la réplique. Cette option n’est prise en charge qu’à partir de la version v10.

Vous pouvez spécifier les paramètres de basebackup soit sous forme de map (paires clé-valeur), soit sous forme de liste d'éléments, chacun pouvant être une paire clé-valeur ou une clé unique (pour les options qui ne prennent aucune valeur, par exemple, `--verbose`). Considérez ces deux exemples :

```yaml
postgresql:
    basebackup:
        max-rate: '100M'
        checkpoint: 'fast'
```

et

```yaml
postgresql:
    basebackup:
        - verbose
        - max-rate: '100M'
        - waldir: /pg-wal-mount/external-waldir
```

Si toutes les méthodes de création de réplique échouent, Patroni tentera à nouveau toutes les méthodes dans l'ordre lors du cycle suivant de la boucle d'événements.
