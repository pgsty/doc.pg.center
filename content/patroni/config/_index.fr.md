---
title: "Configuration Patroni"
weight: 30
icon: fa-solid fa-code
description: "Modèle de configuration Patroni, règles de priorité et outils de validation."
sidebar_expanded: true
module: [PATRONI]
categories: [Référence]
aliases: [/docs/patroni/config/]
upstream_link: "https://patroni.readthedocs.io/en/latest/patroni_configuration.html"
---

<a id="config"></a>
Il existe 3 types de configuration Patroni :

- Configuration dynamique globale [pending_restart](/fr/patroni/config/dynamic#dynamic).
  Ces options sont stockées dans le magasin de configuration distribué (DCS) et appliquées sur tous les nœuds du cluster. La configuration dynamique peut être définie à tout moment à l’aide de l’outil [patronictl_edit_config](/fr/patroni/patronictl#patronictl_edit_config) ou de l’API REST de Patroni [REST API](/fr/patroni/rest_api#rest_api). Si les options modifiées ne font pas partie de la configuration au démarrage, elles sont appliquées de manière asynchrone (lors du prochain cycle de réveil) sur chaque nœud, qui est ensuite rechargé. Si le nœud nécessite un redémarrage pour appliquer la configuration (pour les paramètres [PostgreSQL](https://www.postgresql.org/docs/current/view-pg-settings.html) avec contexte postmaster, lorsque leurs valeurs ont changé), un indicateur spécial `pending_restart` indiquant cela est défini dans le fichier JSON members.data. En outre, l’état du nœud indique cela en affichant `"restart_pending": true`.

- Fichier de configuration local [patroni.yml](/fr/patroni/config/yaml#yaml) (patroni.yml).
  Ces options sont définies dans le fichier de configuration et ont priorité sur la configuration dynamique. `patroni.yml` peut être modifié et rechargé en cours d'exécution (sans redémarrage de Patroni) en envoyant le signal SIGHUP au processus Patroni, en effectuant une requête `POST /reload`REST-API ou en exécutant [patronictl_reload](/fr/patroni/patronictl#patronictl_reload). La configuration locale peut être un fichier YAML unique ou un répertoire. Lorsqu'il s'agit d'un répertoire, tous les fichiers YAML qu'il contient sont chargés un par un dans l'ordre trié. En cas de définition d'une clé dans plusieurs fichiers, l'occurrence dans le dernier fichier a priorité.

- [Configuration de l'environnement](/fr/patroni/config/env#env).
    Il est possible de définir/écraser certains paramètres de configuration « Local » à l'aide de variables d'environnement. La configuration par environnement est particulièrement utile lorsque vous exécutez l'application dans un environnement dynamique et que vous ne connaissez pas certains paramètres à l'avance (par exemple, il n'est pas possible de connaître votre adresse IP externe lorsque vous êtes exécuté à l'intérieur de `docker`).

<a id="important_configuration_rules"></a>

--------

## Règles importantes {#important-rules}

### Paramètres PostgreSQL contrôlés par Patroni {#postgresql-parameters-controlled-by-patroni}

Certains paramètres PostgreSQL **doivent avoir les mêmes valeurs sur le primaire et les répliques**. Pour ces paramètres, **les valeurs définies dans les fichiers de configuration localisés de Patroni ou via les variables d’environnement n’ont aucun effet**. Pour modifier ou définir leurs valeurs, il faut modifier la configuration partagée dans le DCS. Voici la liste réelle de ces paramètres, accompagnée de leurs valeurs par défaut et minimales :

- **max_connections** : valeur par défaut 100, valeur minimale 25
- **max_locks_per_transaction** : valeur par défaut 64, valeur minimale 32
- **max_worker_processes** : valeur par défaut 8, valeur minimale 2
- **max_prepared_transactions** : valeur par défaut 0, valeur minimale 0
- **wal_level** : valeur par défaut hot_standby, valeurs acceptées : hot_standby, replica, logical
- **track_commit_timestamp** : valeur par défaut off

Pour les paramètres ci-dessous, PostgreSQL n'exige pas que les valeurs soient identiques entre le primaire et toutes les répliques. Toutefois, étant donné la possibilité qu'une réplique devienne le primaire à tout moment, il n'a guère de sens de les configurer différemment ; par conséquent, **Patroni limite leur définition à la** [configuration dynamique](/fr/patroni/config/dynamic#dynamic).

- **max_wal_senders** : valeur par défaut 10, valeur minimale 3
- **max_replication_slots** : valeur par défaut 10, valeur minimale 4
- **wal_keep_segments** : valeur par défaut 8, valeur minimale 1
- **wal_keep_size** : valeur par défaut 128 Mo, valeur minimale 16 Mo
- **wal_log_hints** : activé

Ces paramètres sont vérifiés afin de s'assurer qu'ils sont valides ou qu'ils atteignent une valeur minimale.

Certains autres paramètres Postgres sont contrôlés par Patroni :

- **listen_addresses** - est défini soit à partir de la variable d'environnement `postgresql.listen`, soit à partir de la variable d'environnement `PATRONI_POSTGRESQL_LISTEN`
- **port** - est défini soit à partir de la variable d'environnement `postgresql.listen`, soit à partir de la variable d'environnement `PATRONI_POSTGRESQL_LISTEN`
- **cluster_name** - est défini soit à partir de la variable d'environnement `scope`, soit à partir de la variable d'environnement `PATRONI_SCOPE`
- **hot_standby: on**

Pour plus de sécurité, les paramètres provenant des listes ci-dessus sont écrits dans `postgresql.conf`, puis passés sous forme de liste d'arguments à `postgres`, qui leur accorde la plus haute priorité (sauf `wal_keep_segments` et `wal_keep_size`), même au-dessus de [ALTER SYSTEM](https://www.postgresql.org/docs/current/static/sql-altersystem.html)

Il existe également des paramètres tels que **PostgreSQL.listen**, **PostgreSQL.data_dir** qui **peuvent être définis uniquement localement**, c’est-à-dire dans le fichier de configuration Patroni [config](/fr/patroni/config/yaml#yaml) ou via la variable d’environnement [configuration](/fr/patroni/config/env#env). Dans la plupart des cas, la configuration locale remplace la configuration dynamique.

Lors de l'application des options de configuration locales ou dynamiques, les actions suivantes sont effectuées :

- Le nœud vérifie d'abord s'il existe un fichier `postgresql.base.conf` ou si le paramètre `custom_conf` est défini.
- Si le paramètre `custom_conf` est défini, le fichier qu'il spécifie est utilisé comme configuration de base, en ignorant `postgresql.base.conf` et `postgresql.conf`.
- Si le paramètre `custom_conf` n'est pas défini et que `postgresql.base.conf` existe, il contient la configuration « originale » renommée et est utilisé comme configuration de base.
- Si aucun fichier `custom_conf` ni `postgresql.base.conf` n'existe, le fichier `postgresql.conf` d'origine est renommé en `postgresql.base.conf` et utilisé comme configuration de base.
- Les options dynamiques (à l'exception de celles mentionnées ci-dessus) sont exportées dans `postgresql.conf`, et une directive d'inclusion est ajoutée dans `postgresql.conf` vers la configuration de base (soit `postgresql.base.conf`, soit le fichier situé à `custom_conf`). Ainsi, il est possible d'appliquer de nouvelles options sans devoir relire le fichier de configuration pour vérifier la présence de l'inclusion.
- Certains paramètres essentiels à la gestion du cluster par Patroni sont remplacés par la ligne de commande.
- Si une option nécessitant un redémarrage est modifiée (il faut examiner le contexte dans pg_settings et les valeurs réelles de ces options), un indicateur pending_restart est défini sur ce nœud. Cet indicateur est réinitialisé à chaque redémarrage.

Les paramètres seront appliqués dans l'ordre suivant (les paramètres en temps d'exécution ont la priorité la plus élevée) :

1.  charger les paramètres à partir du fichier `postgresql.base.conf` (ou à partir d’un fichier `custom_conf`, le cas échéant)
2.  charger les paramètres à partir du fichier `postgresql.conf`
3.  charger les paramètres à partir du fichier `postgresql.auto.conf`
4.  paramètre en temps d’exécution utilisant `-o --name=value`

Cela permet la configuration de tous les nœuds (2), la configuration d’un nœud spécifique à l’aide de `ALTER SYSTEM` (3) et garantit que les paramètres essentiels au fonctionnement de Patroni sont appliqués (4), tout en laissant de la place aux outils de configuration qui gèrent `postgresql.conf` directement sans impliquer Patroni (1).

<a id="shared_memory_gucs"></a>

### Paramètres PostgreSQL affectant la mémoire partagée {#postgresql-parameters-that-touch-shared-memory}

PostgreSQL dispose de certains paramètres qui déterminent la taille de la mémoire partagée qu’ils utilisent :

- **max_connections**
- **max_prepared_transactions**
- **max_locks_per_transaction**
- **max_wal_senders**
- **max_worker_processes**

La modification de ces paramètres nécessite un redémarrage de PostgreSQL pour prendre effet, et leurs structures de mémoire partagée ne peuvent pas être plus petites sur les nœuds secondaires que sur le nœud primaire.

Comme expliqué précédemment, Patroni limite la modification de leurs valeurs à la [configuration dynamique](/fr/patroni/config/dynamic#dynamic), qui comprend généralement :

1.  Application des modifications via [patronictl_edit_config](/fr/patroni/patronictl#patronictl_edit_config) (ou via l'API REST `/config` point d'accès)
2.  Redémarrage des nœuds via [patronictl_restart](/fr/patroni/patronictl#patronictl_restart) (ou via l'API REST `/restart` point d'accès)

**Note :** veillez à redémarrer les nœuds PostgreSQL à l’aide de la commande [patronictl_restart](/fr/patroni/patronictl#patronictl_restart), ou via l’endpoint REST `/restart`. Une tentative de redémarrage de PostgreSQL en redémarrant le démon Patroni, par exemple en exécutant `systemctl restart patroni`, peut provoquer un basculement dans le cluster, si vous redémarrez le nœud primaire.

Toutefois, comme ces paramètres gèrent la mémoire partagée, une attention particulière doit être portée lors du redémarrage des nœuds :

- Si vous souhaitez **augmenter** la valeur de l'un de ces paramètres :

  > 1.  Redémarrez tous les serveurs secondaires en premier
  > 2.  Redémarrez le serveur primaire ensuite

- Si vous souhaitez **réduire** la valeur de l'un de ces paramètres :

  > 1.  Redémarrez le serveur primaire en premier
  > 2.  Redémarrez ensuite tous les serveurs secondaires

**Remarque :** si vous tentez de redémarrer tous les nœuds en même temps après **avoir diminué** la valeur de l'un de ces paramètres, Patroni ignorera le changement et redémarrera le secondaire avec la valeur d'origine, ce qui nécessitera de redémarrer à nouveau les secondaires ultérieurement. Patroni agit ainsi pour empêcher le secondaire de tomber dans une boucle de redémarrages infinie, car PostgreSQL quitte avec un message `FATAL` si vous tentez de définir l'un de ces paramètres à une valeur inférieure à celle visible dans `pg_controldata` sur le nœud secondaire. Autrement dit, nous ne pouvons diminuer le paramètre sur le secondaire qu'une fois que son `pg_controldata` est à jour avec le primaire concernant ces modifications apportées au primaire.

Plus d'informations à ce sujet sont disponibles dans [Aperçu administrateur PostgreSQL](https://www.postgresql.org/docs/current/hot-standby.html#HOT-STANDBY-ADMIN).

### Paramètres de configuration Patroni {#patroni-configuration-parameters}

En outre, les options de configuration suivantes de Patroni **peuvent être modifiées uniquement de manière dynamique** :

- **ttl** : 30
- **loop_wait** : 10
- **retry_timeout** : 10
- **maximum_lag_on_failover** : 1048576
- **max_timelines_history** : 0
- **check_timeline** : false
- **PostgreSQL.use_slots** : true

Lorsque ces options sont modifiées, Patroni lit la section correspondante de la configuration stockée dans le DCS et met à jour ses valeurs en cours d'exécution.

Les nœuds Patroni enregistrent l'état des options du DCS sur le disque à chaque modification de configuration, dans le fichier `patroni.dynamic.json` situé dans le répertoire de données de Postgres. Seul le leader est autorisé à restaurer ces options à partir de la sauvegarde sur disque si elles sont totalement absentes du DCS ou si elles sont invalides.

<a id="validate_generate_config"></a>

--------

## Génération et validation de la configuration {#configuration-generation-and-validation}

Patroni fournit des interfaces en ligne de commande pour générer et valider une [configuration locale](/fr/patroni/config/yaml#yaml). Avec l'exécutable `patroni`, vous pouvez :

- Créez une configuration Patroni d'exemple locale ;
- Créez un fichier de configuration Patroni pour l'instance PostgreSQL en cours d'exécution localement (par exemple, comme étape de préparation pour l'intégration [Patroni](/fr/patroni/existing_data#existing_data)) ;
- Validez un fichier de configuration Patroni donné.

<a id="generate_sample_config"></a>

### Configuration exemple de Patroni {#sample-patroni-configuration}

```text
patroni --generate-sample-config [configfile]
```

#### Description {#description}

Générez un fichier de configuration Patroni d'exemple au format `yaml`. Les valeurs des paramètres sont définies à l'aide de la configuration [Environnement](/fr/patroni/config/env#env), sinon, si non définies, les valeurs par défaut utilisées par Patroni ou la chaîne `#FIXME` sont utilisées pour les valeurs qui devront être définies ultérieurement par l'utilisateur.

Certains valeurs par défaut sont définies en fonction de la configuration locale :

> - **PostgreSQL.listen** : l'adresse IP renvoyée par l'appel à `gethostname` pour le nom d'hôte de la machine actuelle et le port standard `5432`.
> - **PostgreSQL.connect_address** : l'adresse IP renvoyée par l'appel à `gethostname` pour le nom d'hôte de la machine actuelle et le port standard `5432`.
> - **PostgreSQL.authentication.rewind** : n'est défini que si la version de PostgreSQL peut être déterminée à partir du binaire et que la version est 11 ou ultérieure.
> - **restapi.listen** : adresse IP renvoyée par l'appel à `gethostname` pour le nom d'hôte de la machine actuelle et le port standard `8008`.
> - **restapi.connect_address** : adresse IP renvoyée par l'appel à `gethostname` pour le nom d'hôte de la machine actuelle et le port standard `8008`.

#### Paramètres {#parameters}

`configfile` - chemin complet du fichier de configuration utilisé pour stocker le résultat. Si non fourni, le résultat est envoyé à `stdout`.

<a id="generate_config"></a>

### Configuration Patroni pour une instance en cours d'exécution {#patroni-configuration-for-a-running-instance}

```text
patroni --generate-config [--dsn DSN] [configfile]
```

#### Description {#description-1}

Générez une configuration Patroni au format `yaml` pour l'instance PostgreSQL exécutée localement. Le DSN fourni, qui est prioritaire, ou les [variables d'environnement](https://www.postgresql.org/docs/current/libpq-envars.html) de PostgreSQL serviront à la connexion. Si aucun mot de passe n'est fourni, vous devrez le saisir à l'invite.

Toutes les options GUC non internes définies dans l'instance Postgres source, qu'elles aient été configurées via un fichier de configuration, via la ligne de commande du postmaster ou via des variables d'environnement, serviront de source pour les paramètres de configuration Patroni suivants :

> - **scope** : valeur GUC `cluster_name` ;
> - **PostgreSQL.listen** : valeurs GUC `listen_addresses` et `port` ;
> - **PostgreSQL.datadir** : valeur GUC `data_directory` ;
> - **PostgreSQL.parameters** : valeurs GUC `archive_command`, `restore_command`, `archive_cleanup_command`, `recovery_end_command`, `ssl_passphrase_command`, `hba_file`, `ident_file`, `config_file` ;
> - **bootstrap.dcs** : toutes les autres valeurs GUC PostgreSQL collectées.

Si `scope`, `postgresql.listen` ou `postgresql.datadir` n’est pas défini à partir des paramètres GUC de Postgres, la valeur respective de la configuration [Environment](/fr/patroni/config/env#env) est utilisée.

Autres règles applicables à la définition des valeurs :

> - **name** : valeur de la variable d'environnement `PATRONI_NAME` si définie, sinon le nom d'hôte de la machine actuelle.
> - **PostgreSQL.bin_dir** : chemin vers les binaires Postgres extraits de l'instance en cours d'exécution.
> - **PostgreSQL.connect_address** : adresse IP renvoyée par l'appel à `gethostname` pour le nom d'hôte de la machine actuelle et le port utilisé pour la connexion à l'instance, ou la valeur du paramètre GUC `port`.
> - **PostgreSQL.authentication.superuser** : configuration utilisée pour la connexion à l'instance ;
> - **PostgreSQL.pg_hba** : lignes extraites depuis le fichier `hba_file` de l'instance source.
> - **PostgreSQL.pg_ident** : lignes extraites depuis le fichier `ident_file` de l'instance source.
> - **restapi.listen** : adresse IP renvoyée par l'appel à `gethostname` pour le nom d'hôte de la machine actuelle et le port standard `8008`.
> - **restapi.connect_address** : adresse IP renvoyée par l'appel à `gethostname` pour le nom d'hôte de la machine actuelle et le port standard `8008`.

Les autres paramètres définis à l’aide de la configuration [Environnement](/fr/patroni/config/env#env) sont également inclus dans la configuration.

#### Paramètres {#parameters-1}

`configfile`
Chemin complet du fichier de configuration utilisé pour stocker le résultat. Si ce chemin n'est pas fourni, le résultat est envoyé à `stdout`.

`dsn`
Chaîne DSN facultative pour l'instance PostgreSQL locale afin d'obtenir les valeurs GUC.

### Valider la configuration Patroni {#validate-patroni-configuration}

```text
patroni --validate-config [configfile] [--ignore-listen-port | -i]
```

#### Description {#description-2}

Validez la configuration Patroni fournie et affichez les informations relatives aux vérifications échouées.

#### Paramètres {#parameters-2}

`configfile`
Chemin complet du fichier de configuration à vérifier. Si non fourni ou si le fichier n'existe pas, tentera de lire à partir de la variable d'environnement `PATRONI_CONFIG_VARIABLE`, ou, si elle n'est pas définie, à partir des variables d'environnement Patroni [Patroni](/fr/patroni/config/env#env).

`--ignore-listen-port | -i`
Indicateur facultatif pour ignorer les échecs de liaison des ports `listen` déjà en cours d'utilisation lors de la validation de `configfile`.

`--print | -p`
Indicateur facultatif pour afficher la configuration locale (y compris les substitutions de configuration d'environnement) après sa validation réussie.
