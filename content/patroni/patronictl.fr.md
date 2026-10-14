---
title: "patronictl"
weight: 50
icon: fa-solid fa-terminal
description: "Référence de la commande pour la configuration, la syntaxe et les sous-commandes de patronictl."
module: [PATRONI]
categories: [Référence]
upstream_link: "https://patroni.readthedocs.io/en/latest/patronictl.html"
---

<a id="patronictl"></a>
Patroni dispose d'une interface en ligne de commande nommée [patronictl](/fr/patroni/patronictl#patronictl), utilisée principalement pour interagir avec l'API REST de Patroni et avec le DCS. Elle vise à simplifier l'exécution d'opérations au sein du cluster et peut être facilement utilisée par des humains ou des scripts.

<a id="patronictl_configuration"></a>

--------

## Configuration {#configuration}

[patronictl](/fr/patroni/patronictl#patronictl) utilise 3 sections de la configuration :

- **ctl** : comment s'authentifier auprès de l'API REST de Patroni, et comment valider l'identité du serveur. Consulter [paramètres ctl](/fr/patroni/config/yaml#patronictl_settings) pour plus de détails ;
- **restapi** : comment s'authentifier auprès de l'API REST de Patroni, et comment valider l'identité du serveur. N'est utilisé que si la configuration `ctl` est insuffisante. [patronictl](/fr/patroni/patronictl#patronictl) s'intéresse principalement à la section `restapi.authentication` (en cas de non-présence de `ctl.authentication`) et au paramètre `restapi.cafile` (en cas de non-présence de `ctl.cacert`). Consulter [paramètres de l'API REST](/fr/patroni/config/yaml#restapi_settings) pour plus de détails ;
- DCS (par exemple **etcd**) : comment contacter et s'authentifier auprès du DCS utilisé par Patroni.

Ces options de configuration peuvent provenir soit de variables d’environnement, soit d’un fichier de configuration. Consultez les sections ci-dessus dans [Paramètres de configuration par environnement](/fr/patroni/config/env#env) ou [Paramètres de configuration YAML](/fr/patroni/config/yaml#yaml) pour comprendre comment définir ces options via des variables d’environnement ou un fichier de configuration.

Si vous choisissez d'utiliser des variables d'environnement, il s'agit d'une approche directe. Patronictl lira les variables d'environnement et utilisera leurs valeurs.

Si vous choisissez d'utiliser un fichier de configuration, vous disposez de différentes méthodes pour indiquer à [patronictl](/fr/patroni/patronictl#patronictl) le fichier à utiliser. Par défaut, [patronictl](/fr/patroni/patronictl#patronictl) tentera de charger un fichier de configuration nommé `patronictl.yaml`, qui doit se trouver dans l'un des chemins suivants, selon votre système :

- macOS : `~/Library/Application Support/patroni`
- macOS (POSIX) : `~/.patroni`
- Unix : `~/.config/patroni`
- Unix (POSIX) : `~/.patroni`
- Windows (itinérant) : `C:\Users\<user>\AppData\Roaming\patroni`
- Windows (non itinérant) : `C:\Users\<user>\AppData\Local\patroni`

Vous pouvez remplacer ce comportement de l'une des manières suivantes :

- En définissant la variable d'environnement `PATRONICTL_CONFIG_FILE` avec le chemin vers un fichier de configuration personnalisé ;
- En utilisant l'argument en ligne de commande `-c` / `--config-file` de [patronictl](/fr/patroni/patronictl#patronictl) avec le chemin vers un fichier de configuration personnalisé.

> [!NOTE]
> Si vous exécutez [patronictl](/fr/patroni/patronictl#patronictl) sur le même hôte que le démon `patroni`, vous pouvez utiliser le même fichier de configuration, à condition qu'il contienne toutes les sections de configuration requises par [patronictl](/fr/patroni/patronictl#patronictl).

<a id="patronictl_usage"></a>

--------

## Utilisation {#usage}

[patronictl](/fr/patroni/patronictl#patronictl) met à disposition plusieurs opérations pratiques. Cette section a pour but de décrire chacune d'entre elles.

Avant d'aborder chacune des sous-commandes de [patronictl](/fr/patroni/patronictl#patronictl), sachez que [patronictl](/fr/patroni/patronictl#patronictl) dispose elle-même des arguments suivants en ligne de commande :

`-c` / `--config-file`
Comme expliqué précédemment, utilisé pour spécifier le chemin vers un fichier de configuration pour [patronictl](/fr/patroni/patronictl#patronictl).

`-d` / `--dcs-url` / `--dcs`
Fournir une chaîne de connexion vers le DCS utilisé par Patroni.

Cet argument peut être utilisé soit pour remplacer les paramètres DCS et `namespace` provenant de la configuration [patronictl](/fr/patroni/patronictl#patronictl), soit pour les définir s’ils sont absents de la configuration.

La valeur doit être au format `DCS://HOST:PORT/NAMESPACE`, par exemple `etcd3://localhost:2379/service` pour se connecter à etcd v3 en cours d'exécution sur `localhost` avec le cluster Patroni stocké dans l'espace de noms `service`. Toute partie manquante dans la valeur de l'argument sera remplacée par la valeur présente dans la configuration ou par sa valeur par défaut.

`-k` / `--insecure`
Indicateur permettant de contourner la validation du certificat SSL du serveur API REST.

Voici le synopsis de l'exécution d'une commande depuis le [patronictl](/fr/patroni/patronictl#patronictl) :

```text
patronictl [ { -c | --config-file } CONFIG_FILE ]
  [ { -d | --dcs-url | --dcs } DCS_URL ] 
  [ { -k | --insecure } ]
  SUBCOMMAND
```

> [!NOTE]
> Voici la syntaxe pour le synopsis :
>
> - Les options entre crochets sont facultatives ;
> - Les options entre accolades représentent une opération « choisir un parmi un ensemble » ;
> - Les options avec `[, ... ]` peuvent être spécifiées plusieurs fois ;
> - Les éléments écrits en majuscules représentent une valeur littérale qui doit être fournie.
>
> Nous utiliserons cette même syntaxe pour décrire les sous-commandes de [patronictl](/fr/patroni/patronictl#patronictl) dans les sous-sections suivantes. De plus, lors de la description des sous-commandes dans les sous-sections suivantes, la syntaxe des commandes doit être considérée comme une substitution du `SUBCOMMAND` dans le synopsis ci-dessus.

Dans les sous-sections suivantes, vous trouverez la description de chaque commande implémentée par [patronictl](/fr/patroni/patronictl#patronictl). Pour illustrer, nous utiliserons les fichiers de configuration présents dans le dépôt GitHub de Patroni (fichiers `postgres0.yml`, `postgres1.yml` et `postgres2.yml`).

<a id="patronictl_demote_cluster"></a>

### patronictl demote-cluster {#patronictl-demote-cluster}

<a id="patronictl_demote_cluster_synopsis"></a>

#### Synopsis {#synopsis}

```text
demote-cluster
  [ CLUSTER_NAME ]
  [ --host HOST ]
  [ --port PORT ]
  [ --restore-command RESTORE_COMMAND ]
  [ --primary-slot-name PRIMARY_SLOT_NAME ]
  [ --force ]
```

<a id="patronictl_demote_cluster_description"></a>

#### Description {#description}

`patronictl demote-cluster` convertit un cluster Patroni régulier en [cluster de secours](/fr/patroni/standby_cluster#standby_cluster).

La commande applique une mise à jour de la configuration dynamique avec une section `standby_cluster` construite à partir des options de connexion fournies pour le primaire distant, puis attend que le leader soit en cours d'exécution en tant que leader de secours. Elle affiche la topologie actuelle du cluster avant de modifier la configuration et demande une confirmation, sauf si `--force` est utilisé.

Au moins un des éléments `--host`, `--port` ou `--restore-command` doit être spécifié.

<a id="patronictl_demote_cluster_parameters"></a>

#### Paramètres {#parameters}

`CLUSTER_NAME` : Nom du cluster Patroni.

Si ce paramètre n'est pas fourni, [patronictl](/fr/patroni/patronictl#patronictl) tentera de récupérer sa valeur à partir de la configuration `scope`, si elle existe.

`--host` : Adresse du nœud distant.

`--port` : Port du nœud distant.

`--restore-command` : Commande permettant de restaurer les enregistrements WAL depuis le serveur primaire distant.

`--primary-slot-name` : Nom du slot de réplication sur le nœud distant à utiliser pour la réplication.

`--force` : Indicateur permettant de passer outre les invites de confirmation lors de la rétrogradation du cluster.

Utile pour les scripts.

<a id="patronictl_demote_cluster_examples"></a>

#### Exemples {#examples}

Rétrogradez le cluster en cluster de secours qui suit un point de terminaison primaire distant :

```bash
$ patronictl -c postgres0.yml demote-cluster batman --host 192.0.2.10 --port 5432 --primary-slot-name batman --force
```

<a id="patronictl_dsn"></a>

### patronictl dsn {#patronictl-dsn}

<a id="patronictl_dsn_synopsis"></a>

#### Synopsis {#synopsis-1}

```text
dsn
  [ CLUSTER_NAME ]
  [ { { -r | --role } { leader | primary | standby-leader | replica | standby | any } | { -m | --member } MEMBER_NAME } ]
  [ --group CITUS_GROUP ]
```

<a id="patronictl_dsn_description"></a>

#### Description {#description-1}

`patronictl dsn` obtient la chaîne de connexion d'un membre du cluster Patroni.

Si plusieurs membres correspondent aux paramètres de cette commande, l’un d’entre eux sera sélectionné, en priorisant le nœud primaire.

<a id="patronictl_dsn_parameters"></a>

#### Paramètres {#parameters-1}

`CLUSTER_NAME` : Nom du cluster Patroni.

Si ce paramètre n'est pas fourni, [patronictl](/fr/patroni/patronictl#patronictl) tentera de récupérer sa valeur à partir de la configuration `scope`, si elle existe.

`-r` / `--role`
Choisissez un membre ayant le rôle indiqué.

Le rôle peut être l’un des suivants :

- `leader` : le leader d'un cluster Patroni régulier ou d'un cluster Patroni en veille ; ou
- `primary` : le leader d'un cluster Patroni régulier ; ou
- `standby-leader` : le leader d'un cluster Patroni en veille ; ou
- `replica` : une réplique d'un cluster Patroni ; ou
- `standby` : identique à `replica` ; ou
- `any` : tout rôle. Identique à omettre ce paramètre ; ou

`-m` / `--member`
Sélectionnez un membre du cluster portant le nom indiqué.

`MEMBER_NAME` est le nom du membre.

`--group`
Sélectionnez un membre faisant partie du groupe Citus indiqué.

`CITUS_GROUP` est l'identifiant du groupe Citus.

<a id="patronictl_dsn_examples"></a>

#### Exemples {#examples-1}

Obtenir le DSN du nœud primaire :

``` bash
$ patronictl -c postgres0.yml dsn batman -r primary
host=127.0.0.1 port=5432
```

Obtenir la chaîne de connexion (DSN) du nœud nommé `postgresql1` :

``` bash
$ patronictl -c postgres0.yml dsn batman --member postgresql1
host=127.0.0.1 port=5433
```

<a id="patronictl_edit_config"></a>

### patronictl edit-config {#patronictl-edit-config}

<a id="patronictl_edit_config_synopsis"></a>

#### Synopsis {#synopsis-2}

```text
edit-config
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { -q | --quiet } ]
  [ { -s | --set } CONFIG="VALUE" [, ... ] ]
  [ { -p | --pg } PG_CONFIG="PG_VALUE" [, ... ] ]
  [ { --apply | --replace } CONFIG_FILE ]
  [ --force ]
```

<a id="patronictl_edit_config_description"></a>

#### Description {#description-2}

`patronictl edit-config` modifie la configuration dynamique du cluster et met à jour le DCS avec ces modifications.

> [!NOTE]
> Lorsqu'il est appelé via un TTY, la commande tente d'afficher une différence de la configuration dynamique à l'aide d'un outil de pagination. Par défaut, elle tente d'utiliser soit `less` soit `more`. Si vous souhaitez utiliser un autre outil de pagination, définissez la variable d'environnement `PAGER` avec celui souhaité.

<a id="patronictl_edit_config_parameters"></a>

#### Paramètres {#parameters-2}

`CLUSTER_NAME` : Nom du cluster Patroni.

Si ce paramètre n'est pas fourni, [patronictl](/fr/patroni/patronictl#patronictl) tentera de récupérer sa valeur à partir de la configuration `scope`, si elle existe.

`--group`
Modifie la configuration dynamique du groupe Citus indiqué.

Si ce paramètre n'est pas fourni, [patronictl](/fr/patroni/patronictl#patronictl) tentera de récupérer sa valeur à partir de la configuration `citus.group`, si elle existe.

`CITUS_GROUP` est l'identifiant du groupe Citus.

`-q` / `--quiet`
Indicateur permettant de passer outre l'affichage de la différence de configuration.

`-s` / `--set`
Définir une option de configuration dynamique donnée avec une valeur donnée.

`CONFIG` est le nom du chemin de configuration dynamique dans l'arborescence YAML, dont les niveaux sont séparés par `.`.

`VALUE` est la valeur de `CONFIG`. Si elle est égale à `null`, alors `CONFIG` sera supprimé de la configuration dynamique.

`-p` / `--pg`
Définir une option de configuration dynamique Postgres donnée avec la valeur indiquée.

Il s'agit essentiellement d'un raccourci pour `-s` / `--set` avec `CONFIG` préfixé par `postgresql.parameters.`.

`PG_CONFIG` est le nom de la configuration Postgres à définir.

`PG_VALUE` est la valeur de `PG_CONFIG`. Si elle est égale à `null`, alors `PG_CONFIG` sera supprimé de la configuration dynamique.

`--apply`
Appliquer la configuration dynamique à partir du fichier spécifié.

Il est similaire à la spécification de plusieurs options `-s` / `--set`, une pour chaque configuration de `CONFIG_FILE`.

`CONFIG_FILE` est le chemin vers un fichier contenant la configuration dynamique à appliquer, au format YAML. Utilisez `-` si vous souhaitez lire à partir de `stdin`.

`--replace`
Remplacez la configuration dynamique dans le DCS par la configuration dynamique spécifiée dans le fichier fourni.

`CONFIG_FILE` est le chemin vers un fichier contenant la nouvelle configuration dynamique à appliquer, au format YAML. Utilisez `-` si vous souhaitez lire depuis `stdin`.

`--force`
Indicateur permettant de passer outre les invites de confirmation lors du changement de la configuration dynamique.

Utile pour les scripts.

<a id="patronictl_edit_config_examples"></a>

#### Exemples {#examples-2}

Modifiez le paramètre GUC Postgres `max_connections` :

``` diff
patronictl -c postgres0.yml edit-config batman --pg max_connections="150" --force
---
+++
@@ -1,6 +1,8 @@
loop_wait: 10
maximum_lag_on_failover: 1048576
postgresql:
+  parameters:
+    max_connections: 150
  pg_hba:
  - host replication replicator 127.0.0.1/32 md5
  - host all all 0.0.0.0/0 md5

Configuration changed
```

Modifiez les paramètres `loop_wait` et `ttl` :

``` diff
patronictl -c postgres0.yml edit-config batman --set loop_wait="15" --set ttl="45" --force
---
+++
@@ -1,4 +1,4 @@
-loop_wait: 10
+loop_wait: 15
maximum_lag_on_failover: 1048576
postgresql:
  pg_hba:
@@ -6,4 +6,4 @@
  - host all all 0.0.0.0/0 md5
  use_pg_rewind: true
retry_timeout: 10
-ttl: 30
+ttl: 45

Configuration changed
```

Supprimez le paramètre `maximum_lag_on_failover` de la configuration dynamique :

``` diff
patronictl -c postgres0.yml edit-config batman --set maximum_lag_on_failover="null" --force
---
+++
@@ -1,5 +1,4 @@
loop_wait: 10
-maximum_lag_on_failover: 1048576
postgresql:
  pg_hba:
  - host replication replicator 127.0.0.1/32 md5

Configuration changed
```

<a id="patronictl_failover"></a>

### patronictl failover {#patronictl-failover}

<a id="patronictl_failover_synopsis"></a>

#### Synopsis {#synopsis-3}

```text
failover
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  --candidate CANDIDATE_NAME
  [ --force ]
```

<a id="patronictl_failover_description"></a>

#### Description {#description-3}

`patronictl failover` effectue un basculement manuel dans le cluster.

Il est conçu pour être utilisé lorsque le cluster n'est pas sain, par exemple :

- Il n’y a pas de leader ; ou
- Aucun standby synchrone n’est disponible dans un cluster synchrone.

Il permet également de basculer vers un nœud asynchrone si le mode synchrone est activé.

> [!NOTE]
> Rien n'empêche d'exécuter `patronictl failover` dans un cluster sain. Toutefois, nous recommandons d'utiliser `patronictl switchover` dans ces cas.

> [!WARNING]
> Le déclenchement d’un basculement peut entraîner une perte de données, selon l’état de mise à jour de la réplique promue par rapport au primaire.

<a id="patronictl_failover_parameters"></a>

#### Paramètres {#parameters-3}

`CLUSTER_NAME` : Nom du cluster Patroni.

Si ce paramètre n'est pas fourni, [patronictl](/fr/patroni/patronictl#patronictl) tentera de récupérer sa valeur à partir de la configuration `scope`, si elle existe.

`--group`
Effectuez un basculement dans le groupe Citus indiqué.

`CITUS_GROUP` est l'identifiant du groupe Citus.

`--candidate`
Nœud à promouvoir lors d'un basculement.

`CANDIDATE_NAME` est le nom du nœud à promouvoir.

`--force`
Indicateur permettant de passer outre les invites de confirmation lors d’un basculement.

Utile pour les scripts.

<a id="patronictl_failover_examples"></a>

#### Exemples {#examples-3}

Basculer vers le nœud `postgresql2` :

``` bash
$ patronictl -c postgres0.yml failover batman --candidate postgresql2 --force
Current cluster topology
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  3 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  3 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  3 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
2023-09-12 11:52:27.50978 Successfully failed over to "postgresql2"
+ Cluster: batman (7277694203142172922) -+---------+----+-------------+---------+------------+---------+
| Member      | Host           | Role    | State   | TL | Receive LSN |     Lag | Replay LSN |     Lag |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
| postgresql0 | 127.0.0.1:5432 | Replica | stopped |    |     unknown | unknown |    unknown | unknown |
| postgresql1 | 127.0.0.1:5433 | Replica | running |  3 |   0/4000188 |       0 |  0/4000188 |       0 |
| postgresql2 | 127.0.0.1:5434 | Leader  | running |  3 |             |         |            |         |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
```

<a id="patronictl_flush"></a>

### patronictl flush {#patronictl-flush}

<a id="patronictl_flush_synopsis"></a>

#### Synopsis {#synopsis-4}

```text
flush
  CLUSTER_NAME
  [ MEMBER_NAME [, ... ] ]
  { restart | switchover }
  [ --group CITUS_GROUP ]
  [ { -r | --role } { leader | primary | standby-leader | replica | standby | any } ]
  [ --force ]
```

<a id="patronictl_flush_description"></a>

#### Description {#description-4}

`patronictl flush` supprime les événements planifiés, le cas échéant.

<a id="patronictl_flush_parameters"></a>

#### Paramètres {#parameters-4}

`CLUSTER_NAME`
Nom du cluster Patroni.

`MEMBER_NAME`
Supprimer les événements planifiés pour le ou les membres Patroni indiqués.

Plusieurs membres peuvent être spécifiés. Si aucun membre n'est spécifié, tous les membres sont pris en compte.

> [!NOTE]
> Utilisé uniquement lors de la suppression d'événements de redémarrage planifiés.

`restart`
Supprimer les événements de redémarrage planifiés.

`switchover`
Supprimer l'événement de basculement planifié.

`--group`
Supprimer les événements planifiés du groupe Citus indiqué.

`CITUS_GROUP` est l'identifiant du groupe Citus.

`-r` / `--role`
Supprimer les événements planifiés pour les membres ayant le rôle spécifié.

Le rôle peut être l’un des suivants :

- `leader` : le leader d'un cluster Patroni régulier ou d'un cluster Patroni en veille ; ou
- `primary` : le leader d'un cluster Patroni régulier ; ou
- `standby-leader` : le leader d'un cluster Patroni en veille ; ou
- `replica` : une réplique d'un cluster Patroni ; ou
- `standby` : identique à `replica` ; ou
- `any` : tout rôle. Identique à omettre ce paramètre.

> [!NOTE]
> Utilisé uniquement lors de la suppression d'événements de redémarrage planifiés.

`--force`
Indicateur permettant de passer outre les invites de confirmation lors de l'exécution de l'opération d'effacement.

Utile pour les scripts.

<a id="patronictl_flush_examples"></a>

#### Exemples {#examples-4}

Supprimer un événement de basculement planifié :

``` bash
$ patronictl -c postgres0.yml flush batman switchover --force
Success: scheduled switchover deleted
```

Supprimer le redémarrage planifié de tous les nœuds de secours :

``` bash
$ patronictl -c postgres0.yml flush batman restart -r replica --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+---------------------------+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag | Scheduled restart         |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     | 2025-03-23T18:00:00-03:00 |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
Success: flush scheduled restart for member postgresql1
Success: flush scheduled restart for member postgresql2
```

Supprimer le redémarrage planifié des nœuds `postgresql0` et `postgresql1` :

``` bash
$ patronictl -c postgres0.yml flush batman postgresql0 postgresql1 restart --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+---------------------------+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag | Scheduled restart         |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     | 2025-03-23T18:00:00-03:00 |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
Success: flush scheduled restart for member postgresql0
Success: flush scheduled restart for member postgresql1
```

<a id="patronictl_history"></a>

### patronictl history {#patronictl-history}

<a id="patronictl_history_synopsis"></a>

#### Synopsis {#synopsis-5}

```text
history
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { -f | --format } { pretty | tsv | json | yaml } ]
```

<a id="patronictl_history_description"></a>

#### Description {#description-5}

`patronictl history` affiche l'historique des événements de basculement et de basculement planifié du cluster, le cas échéant.

Les informations suivantes sont incluses dans la sortie :

`TL`
Timeline Postgres au moment de l'événement.

`LSN`
LSN de Postgres au moment de l'événement.

`Reason`
Raison extraite du fichier Postgres `.history`.

`Timestamp`
Heure à laquelle l'événement s'est produit.

`New Leader`
Membre Patroni ayant été promu pendant l'événement.

<a id="patronictl_history_parameters"></a>

#### Paramètres {#parameters-5}

`CLUSTER_NAME`
Nom du cluster Patroni.

Si ce paramètre n'est pas fourni, [patronictl](/fr/patroni/patronictl#patronictl) tentera de récupérer sa valeur à partir de la configuration `scope`, si elle existe.

`--group`
Affiche l'historique des événements du groupe Citus spécifié.

`CITUS_GROUP` est l'identifiant du groupe Citus.

Si ce paramètre n'est pas fourni, [patronictl](/fr/patroni/patronictl#patronictl) tentera de récupérer sa valeur à partir de la configuration `citus.group`, si elle existe.

`-f` / `--format`
Comment formater la liste des événements dans la sortie.

Le format peut être l'un des suivants :

- `pretty` : affiche l'historique sous forme de tableau élégant ; ou
- `tsv` : affiche l'historique sous forme d'information tabulaire, les colonnes étant séparées par `\t` ; ou
- `json` : affiche l'historique au format JSON ; ou
- `yaml` : affiche l'historique au format YAML.

La valeur par défaut est `pretty`.

<a id="patronictl_history_examples"></a>

#### Exemples {#examples-5}

Affichez l'historique des événements :

``` bash
$ patronictl -c postgres0.yml history batman
+----+----------+------------------------------+----------------------------------+-------------+
| TL |      LSN | Reason                       | Timestamp                        | New Leader  |
+----+----------+------------------------------+----------------------------------+-------------+
|  1 | 24392648 | no recovery target specified | 2023-09-11T22:11:27.125527+00:00 | postgresql0 |
|  2 | 50331864 | no recovery target specified | 2023-09-12T11:34:03.148097+00:00 | postgresql0 |
|  3 | 83886704 | no recovery target specified | 2023-09-12T11:52:26.948134+00:00 | postgresql2 |
|  4 | 83887280 | no recovery target specified | 2023-09-12T11:53:09.620136+00:00 | postgresql0 |
+----+----------+------------------------------+----------------------------------+-------------+
```

Affichez l'historique des événements au format YAML :

``` bash
$ patronictl -c postgres0.yml history batman -f yaml
- LSN: 24392648
  New Leader: postgresql0
  Reason: no recovery target specified
  TL: 1
  Timestamp: '2023-09-11T22:11:27.125527+00:00'
- LSN: 50331864
  New Leader: postgresql0
  Reason: no recovery target specified
  TL: 2
  Timestamp: '2023-09-12T11:34:03.148097+00:00'
- LSN: 83886704
  New Leader: postgresql2
  Reason: no recovery target specified
  TL: 3
  Timestamp: '2023-09-12T11:52:26.948134+00:00'
- LSN: 83887280
  New Leader: postgresql0
  Reason: no recovery target specified
  TL: 4
  Timestamp: '2023-09-12T11:53:09.620136+00:00'
```

<a id="patronictl_list"></a>

### patronictl list {#patronictl-list}

<a id="patronictl_list_synopsis"></a>

#### Synopsis {#synopsis-6}

```text
list
  [ CLUSTER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ { -e | --extended } ]
  [ { -t | --timestamp } ]
  [ { -f | --format } { pretty | tsv | json | yaml } ]
  [ { -W | { -w | --watch } TIME } ]
```

<a id="patronictl_list_description"></a>

#### Description {#description-6}

`patronictl list` affiche des informations sur le cluster Patroni et ses membres.

Les informations suivantes sont incluses dans la sortie :

`Cluster`
Nom du cluster Patroni.

`Member`
Nom du membre Patroni.

`Host`
Hôte sur lequel le membre est situé.

`Role`
Rôle actuel du membre.

Peut être l'un des suivants :

- `Leader` : le leader actuel d'un cluster Patroni régulier ; ou
- `Standby Leader` : le leader actuel d'un cluster de secours Patroni ; ou
- `Sync Standby` : une réplique de secours synchrone d'un cluster Patroni avec le mode synchrone activé ; ou
- `Replica` : une réplique de secours régulière d'un cluster Patroni.

`State`
État actuel de PostgreSQL dans le membre Patroni.

Quelques exemples parmi les états possibles :

- `running` : si PostgreSQL est actuellement en cours d'exécution ;
- `streaming` : si une réplique et PostgreSQL reçoit actuellement des journaux WAL depuis le nœud primaire ;
- `in archive recovery` : si une réplique et PostgreSQL récupère actuellement les journaux WAL depuis l'archive ;
- `stopped` : si PostgreSQL a été arrêté ;
- `crashed` : si PostgreSQL a planté.

`TL`
Timeline actuelle de PostgreSQL dans le membre Patroni.

`Receive LSN`
Dernière position du journal WAL reçue et synchronisée sur le disque par la réplication en streaming du membre (`pg_catalog.pg_last_(xlog|wal)_receive_(location|lsn)()`).

`Receive Lag`
Retard de réplication entre la position `Receive LSN` du membre et son amont, en mégaoctets.

`Replay LSN`
Dernière position du journal WAL rejouée durant la récupération du membre (`pg_catalog.pg_last_(xlog|wal)_replay_(location|lsn)()`).

`Replay Lag`
Retard de réplication entre la position `Replay LSN` du membre et son amont, en mégaoctets.

En outre, les informations suivantes peuvent être incluses dans la sortie :

`System identifier`
Identifiant système Postgres.

> [!NOTE]
> Affiché dans l'en-tête du tableau.
>
> Affiché uniquement si le format de sortie est `pretty`.

`Group`
ID du groupe Citus.

> [!NOTE]
> Affiché dans l'en-tête du tableau.
>
> Affiché uniquement si un cluster Citus est utilisé.

`Pending restart`
`*` indique que le nœud nécessite un redémarrage pour que certaines configurations Postgres prennent effet. Une valeur vide indique que le nœud n'a pas besoin de redémarrage.

> [!NOTE]
> Affiché en tant qu'attribut membre.
>
> Affiché si :
>
> - Impression au format `pretty` ou `tsv` avec la sortie étendue activée ; ou
> - Si le nœud nécessite un redémarrage.

`Scheduled restart`
Horodatage auquel un redémarrage a été planifié pour l'instance Postgres gérée par le membre Patroni. Une valeur vide indique qu'aucun redémarrage n'est planifié pour le membre.

> [!NOTE]
> Affiché en tant qu'attribut membre.
>
> Affiché si :
>
> - Impression au format `pretty` ou `tsv` avec la sortie étendue activée ; ou
> - Si le nœud a un redémarrage planifié.

`Tags`
Contient les balises définies pour le membre Patroni. Une valeur vide indique qu'aucune balise n'a été configurée, ou qu'elles ont été configurées avec des valeurs par défaut.

> [!NOTE]
> Affiché en tant qu'attribut membre.
>
> Affiché si :
>
> - Impression au format `pretty` ou `tsv` avec la sortie étendue activée ; ou
> - Si le nœud possède des balises personnalisées, ou des balises par défaut avec des valeurs non par défaut.

`Scheduled switchover`
Horodatage auquel un basculement planifié a été prévu pour le cluster Patroni, le cas échéant.

> [!NOTE]
> Affiché dans le pied de tableau.
>
> Affiché uniquement s'il existe un basculement planifié, et que le format de sortie est `pretty`.

`Maintenance mode`

> Si la surveillance du cluster est actuellement mise en pause.
>
> > [!NOTE]
> > Affiché dans le pied de tableau.
>
> > Affiché uniquement si le cluster est en pause, et que le format de sortie est `pretty`.

<a id="patronictl_list_parameters"></a>

#### Paramètres {#parameters-6}

`CLUSTER_NAME`
Nom du cluster Patroni.

Si ce paramètre n'est pas fourni, [patronictl](/fr/patroni/patronictl#patronictl) tentera de récupérer sa valeur à partir de la configuration `scope`, si elle existe.

`--group`
Affiche les informations relatives aux membres du groupe Citus spécifié.

`CITUS_GROUP` est l'identifiant du groupe Citus.

`-e` / `--extended`
Affiche des informations étendues.

Forcer l'affichage des attributs `Pending restart`, `Scheduled restart` et `Tags`, même si leur valeur est vide.

> [!NOTE]
> S'applique uniquement aux formats de sortie `pretty` et `tsv`.

`-t` / `--timestamp`
Affiche un horodatage avant d'afficher les informations sur le cluster et ses membres.

`-f` / `--format`
Comment formater la liste des membres du cluster dans la sortie.

Le format peut être l'un des suivants :

- `pretty` : affiche les membres du cluster sous forme de tableau élégant ; ou
- `tsv` : affiche les membres du cluster sous forme d'information tabulaire, les colonnes étant séparées par `\t` ; ou
- `json` : affiche les membres du cluster au format JSON ; ou
- `yaml` : affiche les membres du cluster au format YAML.

La valeur par défaut est `pretty`.

`-W`
Actualisez automatiquement les informations toutes les 2 secondes.

`-w` / `--watch`
Actualiser automatiquement les informations à l'intervalle spécifié.

`TIME` est l'intervalle entre les actualisations, en secondes.

<a id="patronictl_list_examples"></a>

#### Exemples {#examples-6}

Affichez les informations sur le cluster au format `pretty` :

``` bash
$ patronictl -c postgres0.yml list batman
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
```

Affichez les informations sur le cluster au format `pretty` avec des colonnes étendues :

``` bash
$ patronictl -c postgres0.yml list batman -e
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+-----------------+------------------------+-------------------+------+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag | Pending restart | Pending restart reason | Scheduled restart | Tags |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+-----------------+------------------------+-------------------+------+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |                 |                        |                   |      |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |                 |                        |                   |      |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |                 |                        |                   |      |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+-----------------+------------------------+-------------------+------+
```

Affichez les informations sur le cluster au format YAML, avec l'horodatage de l'exécution :

``` bash
$ patronictl -c postgres0.yml list batman -f yaml -t
2023-09-12 13:30:48
- Cluster: batman
  Host: 127.0.0.1:5432
  Member: postgresql0
  Role: Leader
  State: running
  TL: 5
- Cluster: batman
  Host: 127.0.0.1:5433
  Receive LSN: 0/40004E8
  Receive Lag: 0
  Replay LSN: 0/40004E8
  Replay Lag: 0
  Member: postgresql1
  Role: Replica
  State: streaming
  TL: 5
- Cluster: batman
  Host: 127.0.0.1:5434
  Receive LSN: 0/40004E8
  Receive Lag: 0
  Replay LSN: 0/40004E8
  Replay Lag: 0
  Member: postgresql2
  Role: Replica
  State: streaming
  TL: 5
```

<a id="patronictl_pause"></a>

### patronictl pause {#patronictl-pause}

<a id="patronictl_pause_synopsis"></a>

#### Synopsis {#synopsis-7}

```text
pause
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ --wait ]
```

<a id="patronictl_pause_description"></a>

#### Description {#description-7}

`patronictl pause` met temporairement le cluster Patroni en mode maintenance et désactive le basculement automatique.

<a id="patronictl_pause_parameters"></a>

#### Paramètres {#parameters-7}

`CLUSTER_NAME`
Nom du cluster Patroni.

Si ce paramètre n'est pas fourni, [patronictl](/fr/patroni/patronictl#patronictl) tentera de récupérer sa valeur à partir de la configuration `scope`, si elle existe.

`--group`
Met en pause le groupe Citus indiqué.

`CITUS_GROUP` est l'identifiant du groupe Citus.

Si ce paramètre n'est pas fourni, [patronictl](/fr/patroni/patronictl#patronictl) tentera de récupérer sa valeur à partir de la configuration `citus.group`, si elle existe.

`--wait`
Attendez que tous les membres Patroni soient mis en pause avant de restituer le contrôle à l'appelant.

<a id="patronictl_pause_examples"></a>

#### Exemples {#examples-7}

Mettez le cluster en mode maintenance, puis attendez que tous les nœuds aient été mis en pause :

``` bash
$ patronictl -c postgres0.yml pause batman --wait
'pause' request sent, waiting until it is recognized by all nodes
Success: cluster management is paused
```

<a id="patronictl_promote_cluster"></a>

### patronictl promote-cluster {#patronictl-promote-cluster}

<a id="patronictl_promote_cluster_synopsis"></a>

#### Synopsis {#synopsis-8}

```text
promote-cluster
  [ CLUSTER_NAME ]
  [ --force ]
```

<a id="patronictl_promote_cluster_description"></a>

#### Description {#description-8}

`patronictl promote-cluster` convertit un cluster de secours en cluster Patroni régulier.

La commande supprime la section `standby_cluster` de la configuration dynamique et attend que le leader fonctionne en tant que primaire. Elle affiche la topologie actuelle du cluster avant de modifier la configuration et demande une confirmation, sauf si `--force` est utilisé.

<a id="patronictl_promote_cluster_parameters"></a>

#### Paramètres {#parameters-8}

`CLUSTER_NAME` : Nom du cluster Patroni.

Si ce paramètre n'est pas fourni, [patronictl](/fr/patroni/patronictl#patronictl) tentera de récupérer sa valeur à partir de la configuration `scope`, si elle existe.

`--force` : Indicateur permettant de passer outre les invites de confirmation lors de la promotion du cluster.

Utile pour les scripts.

<a id="patronictl_promote_cluster_examples"></a>

#### Exemples {#examples-8}

Promouvoir le cluster de secours pour qu’il fonctionne en tant que cluster Patroni régulier :

```bash
$ patronictl -c postgres0.yml promote-cluster batman --force
```

<a id="patronictl_query"></a>

### patronictl query {#patronictl-query}

<a id="patronictl_query_synopsis"></a>

#### Synopsis {#synopsis-9}

```text
query
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { { -r | --role } { leader | primary | standby-leader | replica | standby | any } | { -m | --member } MEMBER_NAME } ]
  [ { -d | --dbname } DBNAME ]
  [ { -U | --username } USERNAME ]
  [ --password ]
  [ --format { pretty | tsv | json | yaml } ]
  [ { { -f | --file } FILE_NAME | { -c | --command } SQL_COMMAND } ]
  [ --delimiter ]
  [ { -W | { -w | --watch } TIME } ]
```

<a id="patronictl_query_description"></a>

#### Description {#description-9}

`patronictl query` exécute une commande ou un script SQL sur un membre du cluster Patroni.

<a id="patronictl_query_parameters"></a>

#### Paramètres {#parameters-9}

`CLUSTER_NAME`
Nom du cluster Patroni.

Si ce paramètre n'est pas fourni, [patronictl](/fr/patroni/patronictl#patronictl) tentera de récupérer sa valeur à partir de la configuration `scope`, si elle existe.

`--group`
Interrogez le groupe Citus indiqué.

`CITUS_GROUP` est l'identifiant du groupe Citus.

`-r` / `--role`
Choisissez un membre ayant le rôle indiqué.

Le rôle peut être l’un des suivants :

- `leader` : le leader d'un cluster Patroni régulier ou d'un cluster Patroni en veille ; ou
- `primary` : le leader d'un cluster Patroni régulier ; ou
- `standby-leader` : le leader d'un cluster Patroni en veille ; ou
- `replica` : une réplique d'un cluster Patroni ; ou
- `standby` : identique à `replica` ; ou
- `any` : tout rôle. Identique à omettre ce paramètre.

`-m` / `--member`
Choisissez un membre ayant le nom indiqué.

`MEMBER_NAME` est le nom du membre à sélectionner.

`-d` / `--dbname`
Base de données à laquelle se connecter pour exécuter la requête.

`DBNAME` est le nom de la base de données. S'il n'est pas fourni, la valeur par défaut est `USERNAME`.

`-U` / `--username`
Utilisateur pour se connecter à la base de données.

`USERNAME` nom de l'utilisateur. S'il n'est pas fourni, la valeur par défaut est l'utilisateur du système d'exploitation exécutant `patronictl query`.

`--password`
Demande le mot de passe de l'utilisateur qui établit la connexion.

Comme Patroni utilise `libpq`, vous pouvez également créer un fichier `~/.pgpass` ou définir la variable d'environnement `PGPASSWORD`.

`--format`
Comment formater la sortie de la requête.

Le format peut être l'un des suivants :

- `pretty` : affiche les résultats de la requête sous forme de tableau mis en forme ; ou
- `tsv` : affiche les résultats de la requête sous forme d'information tabulaire, les colonnes étant séparées par `\t` ; ou
- `json` : affiche les résultats de la requête au format JSON ; ou
- `yaml` : affiche les résultats de la requête au format YAML.

La valeur par défaut est `tsv`.

`-f` / `--file`
Utilisez un fichier comme source de commandes pour exécuter des requêtes.

`FILE_NAME` est le chemin d'accès au fichier source.

`-c` / `--command`
Exécutez la commande SQL fournie dans la requête.

`SQL_COMMAND` est la commande SQL à exécuter.

`--delimiter`
Le délimiteur utilisé lors de l'affichage des informations au format `tsv`, ou `\t` si omis.

`-W`
Exécuter automatiquement la requête toutes les 2 secondes.

`-w` / `--watch`
Réexécuter automatiquement la requête à l'intervalle spécifié.

`TIME` indique, en secondes, l'intervalle séparant les réexécutions.

<a id="patronictl_query_examples"></a>

#### Exemples {#examples-9}

Exécutez une commande SQL en tant qu'utilisateur `postgres`, puis indiquez son mot de passe :

``` bash
$ patronictl -c postgres0.yml query batman -U postgres --password -c "SELECT now()"
Password:
now
2023-09-12 18:10:53.228084+00:00
```

Exécutez une commande SQL en tant qu'utilisateur `postgres`, en prenant le mot de passe depuis la variable d'environnement `libpq` :

``` bash
$ PGPASSWORD=patroni patronictl -c postgres0.yml query batman -U postgres -c "SELECT now()"
now
2023-09-12 18:11:37.639500+00:00
```

Exécutez une commande SQL et affichez au format `pretty` toutes les 2 secondes :

``` bash
$ patronictl -c postgres0.yml query batman -c "SELECT now()" --format pretty -W
+----------------------------------+
| now                              |
+----------------------------------+
| 2023-09-12 18:12:16.716235+00:00 |
+----------------------------------+
+----------------------------------+
| now                              |
+----------------------------------+
| 2023-09-12 18:12:18.732645+00:00 |
+----------------------------------+
+----------------------------------+
| now                              |
+----------------------------------+
| 2023-09-12 18:12:20.750573+00:00 |
+----------------------------------+
```

Exécutez une commande SQL sur la base de données `test` et affichez la sortie au format YAML :

``` bash
$ patronictl -c postgres0.yml query batman -d test -c "SELECT now() AS column_1, 'test' AS column_2" --format yaml
- column_1: 2023-09-12 18:14:22.052060+00:00
  column_2: test
```

Exécutez une commande SQL sur le membre `postgresql2` :

``` bash
$ patronictl -c postgres0.yml query batman -m postgresql2 -c "SHOW port"
port
5434
```

Exécutez une commande SQL sur l'un des serveurs de secours :

``` bash
$ patronictl -c postgres0.yml query batman -r replica -c "SHOW port"
port
5433
```

<a id="patronictl_reinit"></a>

### patronictl reinit {#patronictl-reinit}

<a id="patronictl_reinit_synopsis"></a>

#### Synopsis {#synopsis-10}

```text
reinit
  CLUSTER_NAME
  [ MEMBER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ --wait ]
  [ --force ]
  [ --from-leader ]
```

<a id="patronictl_reinit_description"></a>

#### Description {#description-10}

`patronictl reinit` reconstruit une instance Postgres en mode standby gérée par une réplique membre du cluster Patroni.

<a id="patronictl_reinit_parameters"></a>

#### Paramètres {#parameters-10}

`CLUSTER_NAME`
Nom du cluster Patroni.

`MEMBER_NAME`
Nom du membre réplique pour lequel l'instance Postgres sera reconstruite.

Plusieurs répliques peuvent être spécifiées. Si aucune réplique n'est spécifiée, la commande ne fait rien.

`--group`  
Reconstruit un membre réplique du groupe Citus indiqué.

`CITUS_GROUP` est l'identifiant du groupe Citus.

`--wait`
Attendez que la réinitialisation du ou des nœuds de secours Postgres soit terminée.

`--force`
Indicateur permettant de passer outre les invites de confirmation lors de la reconstruction des instances secondaires Postgres.

Utile pour les scripts.

`--from-leader`
Indicateur permettant d'obtenir un basebackup directement depuis le leader.

<a id="patronictl_reinit_examples"></a>

#### Exemples {#examples-10}

Demandez une reconstruction de toutes les répliques du cluster Patroni et renvoyez immédiatement le contrôle à l'appelant :

``` bash
$ patronictl -c postgres0.yml reinit batman postgresql1 postgresql2 --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: reinitialize for member postgresql1
Success: reinitialize for member postgresql2
```

Demandez une reconstruction de `postgresql2` et attendez sa finalisation :

``` bash
$ patronictl -c postgres0.yml reinit batman postgresql2 --wait --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: reinitialize for member postgresql2
Waiting for reinitialize to complete on: postgresql2
Reinitialize is completed on: postgresql2
```

Demandez une reconstruction de `postgresql2` et obtenez le basebackup directement depuis le leader :

``` bash
$ patronictl -c postgres0.yml reinit batman postgresql2 --from-leader
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: reinitialize for member postgresql2
```

<a id="patronictl_reload"></a>

### patronictl reload {#patronictl-reload}

<a id="patronictl_reload_synopsis"></a>

#### Synopsis {#synopsis-11}

```text
reload
  CLUSTER_NAME
  [ MEMBER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ { -r | --role } { leader | primary | standby-leader | replica | standby | any } ]
  [ --force ]
```

<a id="patronictl_reload_description"></a>

#### Description {#description-11}

`patronictl reload` demande un rechargement de la configuration locale pour un ou plusieurs membres Patroni.

Il déclenche également `pg_ctl reload` sur l'instance Postgres gérée, même si rien n'a changé.

<a id="patronictl_reload_parameters"></a>

#### Paramètres {#parameters-11}

`CLUSTER_NAME`
Nom du cluster Patroni.

`MEMBER_NAME`
Demander un rechargement de la configuration locale pour le ou les membres Patroni indiqués.

Plusieurs membres peuvent être spécifiés. Si aucun membre n'est spécifié, tous les membres sont pris en compte.

`--group`
Demandez un rechargement des membres du groupe Citus donné.

`CITUS_GROUP` est l'identifiant du groupe Citus.

`-r` / `--role`
Sélectionne les membres ayant le rôle indiqué.

Le rôle peut être l’un des suivants :

- `leader` : le leader d'un cluster Patroni régulier ou d'un cluster Patroni en veille ; ou
- `primary` : le leader d'un cluster Patroni régulier ; ou
- `standby-leader` : le leader d'un cluster Patroni en veille ; ou
- `replica` : une réplique d'un cluster Patroni ; ou
- `standby` : identique à `replica` ; ou
- `any` : tout rôle. Identique à omettre ce paramètre.

`--force`
Indicateur permettant de passer outre les invites de confirmation lors de la demande de rechargement de la configuration locale.

Utile pour les scripts.

<a id="patronictl_reload_examples"></a>

#### Exemples {#examples-11}

Demandez un rechargement de la configuration locale de tous les membres du cluster Patroni :

``` bash
$ patronictl -c postgres0.yml reload batman --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Reload request received for member postgresql0 and will be processed within 10 seconds
Reload request received for member postgresql1 and will be processed within 10 seconds
Reload request received for member postgresql2 and will be processed within 10 seconds
```

<a id="patronictl_remove"></a>

### patronictl remove {#patronictl-remove}

<a id="patronictl_remove_synopsis"></a>

#### Synopsis {#synopsis-12}

```text
remove
  CLUSTER_NAME
  [ --group CITUS_GROUP ]
  [ { -f | --format } { pretty | tsv | json | yaml } ]
```

<a id="patronictl_remove_description"></a>

#### Description {#description-12}

`patronictl remove` supprime les informations du cluster du DCS.

Il s'agit d'une action interactive.

> [!WARNING]
> Cette opération détruira les informations du cluster Patroni dans le DCS.

<a id="patronictl_remove_parameters"></a>

#### Paramètres {#parameters-12}

`CLUSTER_NAME`
Nom du cluster Patroni.

`--group`
Supprimez les informations relatives au cluster Patroni associées au groupe Citus donné.

`CITUS_GROUP` est l'identifiant du groupe Citus.

`-f` / `--format`
Comment formater la liste des membres dans la sortie lors de la demande de confirmation.

Le format peut être l'un des suivants :

- `pretty` : affiche les membres sous forme de tableau mis en forme ; ou
- `tsv` : affiche les membres sous forme d'information tabulaire, les colonnes étant séparées par `\t` ; ou
- `json` : affiche les membres au format JSON ; ou
- `yaml` : affiche les membres au format YAML.

La valeur par défaut est `pretty`.

<a id="patronictl_remove_examples"></a>

#### Exemples {#examples-12}

Supprimer les informations relatives au cluster Patroni `batman` du DCS :

``` bash
$ patronictl -c postgres0.yml remove batman
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Please confirm the cluster name to remove: batman
You are about to remove all information in DCS for batman, please type: "Yes I am aware": Yes I am aware
This cluster currently is healthy. Please specify the leader name to continue: postgresql0
```

<a id="patronictl_restart"></a>

### patronictl restart {#patronictl-restart}

<a id="patronictl_restart_synopsis"></a>

#### Synopsis {#synopsis-13}

```text
restart
  CLUSTER_NAME
  [ MEMBER_NAME [, ...] ]
  [ --group CITUS_GROUP ]
  [ { -r | --role } { leader | primary | standby-leader | replica | standby | any } ]
  [ --any ]
  [ --pg-version PG_VERSION ]
  [ --pending ]
  [ --timeout TIMEOUT ]
  [ --scheduled TIMESTAMP ]
  [ --force ]
```

<a id="patronictl_restart_description"></a>

#### Description {#description-13}

`patronictl restart` demande un redémarrage de l'instance Postgres gérée par un membre du cluster Patroni.

Le redémarrage peut être effectué immédiatement ou planifié pour une date ultérieure.

<a id="patronictl_restart_parameters"></a>

#### Paramètres {#parameters-13}

`CLUSTER_NAME`
Nom du cluster Patroni.

`--group`
Redémarrez le cluster Patroni associé au groupe Citus donné.

`CITUS_GROUP` est l'identifiant du groupe Citus.

`-r` / `--role`
Sélectionnez les membres ayant le rôle indiqué.

Le rôle peut être l’un des suivants :

- `leader` : le leader d'un cluster Patroni régulier ou d'un cluster Patroni en veille ; ou
- `primary` : le leader d'un cluster Patroni régulier ; ou
- `standby-leader` : le leader d'un cluster Patroni en veille ; ou
- `replica` : une réplique d'un cluster Patroni ; ou
- `standby` : identique à `replica` ; ou
- `any` : tout rôle. Identique à omettre ce paramètre.

`--any`
Redémarre un nœud aléatoire parmi ceux qui correspondent aux filtres donnés.

`--pg-version`
Sélectionnez uniquement les membres dont la version de l'instance Postgres gérée est antérieure à la version indiquée.

`PG_VERSION` est la version de Postgres à comparer.

`--pending`
Sélectionnez uniquement les membres marqués comme `Pending restart`.

`--timeout` : Interrompre le redémarrage s'il dure plus que le délai spécifié, et basculer vers une réplique si le problème se situe sur le primaire.

`TIMEOUT` est le nombre de secondes à attendre avant d'abandonner le redémarrage.

`--scheduled`
Planifiez un redémarrage à effectuer à l'horodatage indiqué.

`TIMESTAMP` est l'horodatage auquel le redémarrage doit avoir lieu. Spécifiez-le au format non ambigu, idéalement avec le fuseau horaire. Vous pouvez également utiliser la valeur littérale `now` pour exécuter le redémarrage immédiatement.

`--force`
Indicateur permettant de passer outre les invites de confirmation lors de la demande de redémarrage.

Utile pour les scripts.

<a id="patronictl_restart_examples"></a>

#### Exemples {#examples-13}

Redémarrez immédiatement tous les membres du cluster :

``` bash
$ patronictl -c postgres0.yml restart batman --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: restart on member postgresql0
Success: restart on member postgresql1
Success: restart on member postgresql2
```

Redémarrez immédiatement un membre aléatoire du cluster :

``` bash
$ patronictl -c postgres0.yml restart batman --any --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: restart on member postgresql1
```

Planifiez un redémarrage pour qu'il se produise à `2023-09-13T18:00-03:00` :

``` bash
$ patronictl -c postgres0.yml restart batman --scheduled 2023-09-13T18:00-03:00 --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: restart scheduled on member postgresql0
Success: restart scheduled on member postgresql1
Success: restart scheduled on member postgresql2
```

<a id="patronictl_resume"></a>

### patronictl resume {#patronictl-resume}

<a id="patronictl_resume_synopsis"></a>

#### Synopsis {#synopsis-14}

```text
resume
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ --wait ]
```

<a id="patronictl_resume_description"></a>

#### Description {#description-14}

`patronictl resume` sort le cluster Patroni du mode maintenance et réactive le basculement automatique.

<a id="patronictl_resume_parameters"></a>

#### Paramètres {#parameters-14}

`CLUSTER_NAME`
Nom du cluster Patroni.

Si ce paramètre n'est pas fourni, [patronictl](/fr/patroni/patronictl#patronictl) tentera de récupérer sa valeur à partir de la configuration `scope`, si elle existe.

`--group`
Reprendre le groupe Citus indiqué.

`CITUS_GROUP` est l'identifiant du groupe Citus.

Si ce paramètre n'est pas fourni, [patronictl](/fr/patroni/patronictl#patronictl) tentera de récupérer sa valeur à partir de la configuration `citus.group`, si elle existe.

`--wait`
Attendez que tous les membres Patroni soient repassés en mode actif avant de restituer le contrôle à l'appelant.

<a id="patronictl_resume_examples"></a>

#### Exemples {#examples-14}

Mettez le cluster hors du mode maintenance :

``` bash
$ patronictl -c postgres0.yml resume batman --wait
'resume' request sent, waiting until it is recognized by all nodes
Success: cluster management is resumed
```

<a id="patronictl_show_config"></a>

### patronictl show-config {#patronictl-show-config}

<a id="patronictl_show_config_synopsis"></a>

#### Synopsis {#synopsis-15}

```text
show-config
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
```

<a id="patronictl_show_config_description"></a>

#### Description {#description-15}

`patronictl show-config` affiche la configuration dynamique du cluster stockée dans le DCS.

<a id="patronictl_show_config_parameters"></a>

#### Paramètres {#parameters-15}

`CLUSTER_NAME`
Nom du cluster Patroni.

Si ce paramètre n'est pas fourni, [patronictl](/fr/patroni/patronictl#patronictl) tentera de récupérer sa valeur à partir de la configuration `scope`, si elle existe.

`--group`
Affiche la configuration dynamique du groupe Citus donné.

`CITUS_GROUP` est l'identifiant du groupe Citus.

Si ce paramètre n'est pas fourni, [patronictl](/fr/patroni/patronictl#patronictl) tentera de récupérer sa valeur à partir de la configuration `citus.group`, si elle existe.

<a id="patronictl_show_config_examples"></a>

#### Exemples {#examples-15}

Affiche la configuration dynamique du cluster `batman` :

``` bash
$ patronictl -c postgres0.yml show-config batman
loop_wait: 10
postgresql:
  parameters:
    max_connections: 250
  pg_hba:
  - host replication replicator 127.0.0.1/32 md5
  - host all all 0.0.0.0/0 md5
  use_pg_rewind: true
retry_timeout: 10
ttl: 30
```

<a id="patronictl_switchover"></a>

### patronictl switchover {#patronictl-switchover}

<a id="patronictl_switchover_synopsis"></a>

#### Synopsis {#synopsis-16}

```text
switchover
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { --leader | --primary } LEADER_NAME ]
  --candidate CANDIDATE_NAME
  [ --force ]
```

<a id="patronictl_switchover_description"></a>

#### Description {#description-16}

`patronictl switchover` effectue un basculement planifié dans le cluster.

Il est conçu pour être utilisé lorsque le cluster est sain, par exemple :

- Il y a un leader ;
- Il existe des répliques synchrones disponibles dans un cluster synchrone.

> [!NOTE]
> Si votre cluster est défaillant, vous pourriez être intéressé par `patronictl failover` à la place.

<a id="patronictl_switchover_parameters"></a>

#### Paramètres {#parameters-16}

`CLUSTER_NAME`
Nom du cluster Patroni.

Si ce paramètre n'est pas fourni, [patronictl](/fr/patroni/patronictl#patronictl) tentera de récupérer sa valeur à partir de la configuration `scope`, si elle existe.

`--group`
Effectuez un basculement planifié dans le groupe Citus indiqué.

`CITUS_GROUP` est l'identifiant du groupe Citus.

`--leader` / `--primary`
Indiquez le leader à rétrograder au moment du basculement planifié.

`LEADER_NAME` devrait correspondre au nom du leader actuel dans le cluster.

`--candidate`
Nœud à promouvoir lors d'un basculement planifié, et qui prendra le rôle primaire.

`CANDIDATE_NAME` est le nom du nœud à promouvoir.

`--scheduled`
Planifiez un basculement planifié à effectuer à l'horodatage indiqué.

`TIMESTAMP` est l'horodatage auquel le basculement planifié doit avoir lieu. Indiquez-le au format non ambigu, idéalement avec le fuseau horaire. Vous pouvez également utiliser le littéral `now` pour exécuter le basculement planifié immédiatement.

`--force`
Indicateur permettant de passer outre les invites de confirmation lors d’un basculement planifié.

Utile pour les scripts.

<a id="patronictl_switchover_examples"></a>

#### Exemples {#examples-16}

Basculer sur le nœud `postgresql2` :

``` bash
$ patronictl -c postgres0.yml switchover batman --leader postgresql0 --candidate postgresql2 --force
Current cluster topology
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
2023-09-13 14:15:23.07497 Successfully switched over to "postgresql2"
+ Cluster: batman (7277694203142172922) -+---------+----+-------------+---------+------------+---------+
| Member      | Host           | Role    | State   | TL | Receive LSN |     Lag | Replay LSN |     Lag |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
| postgresql0 | 127.0.0.1:5432 | Replica | stopped |    |     unknown | unknown |    unknown | unknown |
| postgresql1 | 127.0.0.1:5433 | Replica | running |  6 |   0/4000188 |       0 |  0/4000188 |       0 |
| postgresql2 | 127.0.0.1:5434 | Leader  | running |  6 |             |         |            |         |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
```

Planifiez un basculement planifié entre `postgresql0` et `postgresql2` afin qu’il ait lieu à `2023-09-13T18:00:00-03:00` :

``` bash
$ patronictl -c postgres0.yml switchover batman --leader postgresql0 --candidate postgresql2 --scheduled 2023-09-13T18:00-03:00 --force
Current cluster topology
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  8 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
2023-09-13 14:18:11.20661 Switchover scheduled
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  8 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Switchover scheduled at: 2023-09-13T18:00:00-03:00
                    from: postgresql0
                    to: postgresql2
```

<a id="patronictl_topology"></a>

### patronictl topology {#patronictl-topology}

<a id="patronictl_topology_synopsis"></a>

#### Synopsis {#synopsis-17}

```text
topology
  [ CLUSTER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ { -W | { -w | --watch } TIME } ]
```

<a id="patronictl_topology_description"></a>

#### Description {#description-17}

`patronictl topology` affiche les informations concernant le cluster Patroni et ses membres selon une approche en arbre.

Les informations suivantes sont incluses dans la sortie :

`Cluster`
Nom du cluster Patroni.

> [!NOTE]
> Affiché dans l'en-tête du tableau.

`System identifier`
Identifiant système Postgres.

> [!NOTE]
> Affiché dans l'en-tête du tableau.

`Member`
Nom du membre Patroni.

> [!NOTE]
> Les informations de cette colonne s’affichent sous forme d’arborescence des membres en fonction des connexions de réplication.

`Host`
Hôte sur lequel le membre est situé.

`Role`
Rôle actuel du membre.

Peut être l'un des suivants :

- `Leader` : le leader actuel d'un cluster Patroni régulier ; ou
- `Standby Leader` : le leader actuel d'un cluster de secours Patroni ; ou
- `Sync Standby` : une réplique de secours synchrone d'un cluster Patroni avec le mode synchrone activé ; ou
- `Replica` : une réplique de secours régulière d'un cluster Patroni.

`State`
État actuel de PostgreSQL dans le membre Patroni.

Quelques exemples parmi les états possibles :

- `running` : si PostgreSQL est actuellement en cours d'exécution ;
- `streaming` : si une réplique et PostgreSQL reçoit actuellement des journaux WAL depuis le nœud primaire ;
- `in archive recovery` : si une réplique et PostgreSQL récupère actuellement les journaux WAL depuis l'archive ;
- `stopped` : si PostgreSQL a été arrêté ;
- `crashed` : si PostgreSQL a planté.

`TL`
Timeline actuelle de PostgreSQL dans le membre Patroni.

`Receive LSN`
Dernière position du journal WAL reçue et synchronisée sur le disque par la réplication en streaming du membre (`pg_catalog.pg_last_(xlog|wal)_receive_(location|lsn)()`).

`Receive Lag`
Retard de réplication entre la position `Receive LSN` du membre et son amont, en mégaoctets.

`Replay LSN`
Dernière position du journal WAL rejouée durant la récupération du membre (`pg_catalog.pg_last_(xlog|wal)_replay_(location|lsn)()`).

`Replay Lag`
Retard de réplication entre la position `Replay LSN` du membre et son amont, en mégaoctets.

En outre, les informations suivantes peuvent être incluses dans la sortie :

`Group`
ID du groupe Citus.

> [!NOTE]
> Affiché dans l'en-tête du tableau.
>
> Affiché uniquement si un cluster Citus est utilisé.

`Pending restart`
`*` indique que le nœud nécessite un redémarrage pour que certaines configurations Postgres prennent effet. Une valeur vide indique que le nœud n'a pas besoin de redémarrage.

> [!NOTE]
> Affiché en tant qu'attribut membre.
>
> Affiché si le nœud nécessite un redémarrage.

`Scheduled restart`
Horodatage auquel un redémarrage a été planifié pour l'instance Postgres gérée par le membre Patroni. Une valeur vide indique qu'aucun redémarrage n'est planifié pour le membre.

> [!NOTE]
> Affiché en tant qu'attribut membre.
>
> Affiché si le nœud a un redémarrage planifié.

`Tags`
Contient les balises définies pour le membre Patroni. Une valeur vide indique qu'aucune balise n'a été configurée, ou qu'elles ont été configurées avec des valeurs par défaut.

> [!NOTE]
> Affiché en tant qu'attribut membre.
>
> Affiché si le nœud possède des balises personnalisées, ou des balises par défaut avec des valeurs non par défaut.

`Scheduled switchover`
Horodatage auquel un basculement planifié a été prévu pour le cluster Patroni, le cas échéant.

> [!NOTE]
> Affiché dans le pied de tableau.
>
> Affiché uniquement si un basculement planifié est prévu.

`Maintenance mode`

> Si la surveillance du cluster est actuellement mise en pause.
>
> > [!NOTE]
> > Affiché dans le pied de tableau.
>
> > Affiché uniquement si le cluster est mis en pause.

<a id="patronictl_topology_parameters"></a>

#### Paramètres {#parameters-17}

`CLUSTER_NAME`
Nom du cluster Patroni.

Si ce paramètre n'est pas fourni, [patronictl](/fr/patroni/patronictl#patronictl) tentera de récupérer sa valeur à partir de la configuration `scope`, si elle existe.

`--group`
Affiche les informations relatives aux membres du groupe Citus spécifié.

`CITUS_GROUP` est l'identifiant du groupe Citus.

`-W`
Actualisez automatiquement les informations toutes les 2 secondes.

`-w` / `--watch`
Actualiser automatiquement les informations à l'intervalle spécifié.

`TIME` est l'intervalle entre les actualisations, en secondes.

<a id="patronictl_topology_examples"></a>

#### Exemples {#examples-17}

Affiche la topologie du cluster `batman` -- `postgresql1` et `postgresql2` sont en réplication depuis `postgresql0` :

``` bash
$ patronictl -c postgres0.yml topology batman
+ Cluster: batman (7277694203142172922) ---+-----------+----+-------------+-----+------------+-----+
| Member        | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+---------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0   | 127.0.0.1:5432 | Leader  | running   |  8 |             |     |            |     |
| + postgresql1 | 127.0.0.1:5433 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| + postgresql2 | 127.0.0.1:5434 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+---------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
```

<a id="patronictl_version"></a>

### patronictl version {#patronictl-version}

<a id="patronictl_version_synopsis"></a>

#### Synopsis {#synopsis-18}

```text
version
  [ CLUSTER_NAME [, ... ] ]
  [ MEMBER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
```

<a id="patronictl_version_description"></a>

#### Description {#description-18}

`patronictl version` obtient la version de l'application [patronictl](/fr/patroni/patronictl#patronictl). En outre, elle peut également inclure des informations sur la version des clusters Patroni et de leurs membres.

<a id="patronictl_version_parameters"></a>

#### Paramètres {#parameters-18}

`CLUSTER_NAME`
Nom du cluster Patroni.

`MEMBER_NAME`
Nom du membre du cluster Patroni.

`--group`
Considérez un cluster Patroni avec le groupe Citus donné.

`CITUS_GROUP` est l'identifiant du groupe Citus.

<a id="patronictl_version_examples"></a>

#### Exemples {#examples-18}

Obtenir la version de [patronictl](/fr/patroni/patronictl#patronictl) uniquement :

``` bash
$ patronictl -c postgres0.yml version
patronictl version 4.0.0
```

Obtenir la version de [patronictl](/fr/patroni/patronictl#patronictl) et de tous les membres du cluster `batman` :

``` bash
$ patronictl -c postgres0.yml version batman
patronictl version 4.0.0

postgresql0: Patroni 4.0.0 PostgreSQL 16.4
postgresql1: Patroni 4.0.0 PostgreSQL 16.4
postgresql2: Patroni 4.0.0 PostgreSQL 16.4
```

Obtenir la version de [patronictl](/fr/patroni/patronictl#patronictl) et des membres `postgresql1` et `postgresql2` du cluster `batman` :

``` bash
$ patronictl -c postgres0.yml version batman postgresql1 postgresql2
patronictl version 4.0.0

postgresql1: Patroni 4.0.0 PostgreSQL 16.4
postgresql2: Patroni 4.0.0 PostgreSQL 16.4
```
