---
title: "Paramètres de configuration YAML"
linkTitle: "Configuration YAML"
weight: 20
icon: fa-solid fa-code
description: "Référence complète des options et sections de configuration YAML pour Patroni"
module: [PATRONI]
categories: [Référence]
upstream_link: "https://patroni.readthedocs.io/en/latest/yaml_configuration.html"
---

<a id="yaml"></a>

--------

## Global/Universel {#globaluniversal}

- **thread_pool_size** : taille du pool de threads utilisé par Patroni pour exécuter les tâches asynchrones et communiquer via l'API REST avec les autres membres lors d'une course au leader ou de vérifications failsafe. Valeur minimale : `5`, valeur par défaut : `5`.
- **thread_stack_size** : spécifie la taille de la pile à utiliser pour les threads lancés par Patroni. La valeur doit être alignée sur `64kB`. Valeur minimale : `64kB`, valeur par défaut (définie par Patroni) : `512kB`.
- **name** : le nom de l'hôte. Doit être unique dans le cluster.
- **namespace** : chemin dans le magasin de configuration où Patroni stockera les informations sur le cluster. Valeur par défaut : "/service"
- **scope** : nom du cluster

<a id="log_settings"></a>

--------

## Journalisation {#log}

- **type** : définit le format des journaux. Peut être soit **plain** soit **json**. Pour utiliser le format **json**, vous devez avoir installé [jsonlogger](/fr/patroni/installation#extras). La valeur par défaut est **plain**.
- **level** : définit le niveau général de journalisation. La valeur par défaut est **INFO** (voir [la documentation sur le module logging de Python](https://docs.python.org/3.6/library/logging.html#levels))
- **traceback_level** : définit le niveau à partir duquel les traces d'erreur sont visibles. La valeur par défaut est **ERROR**. Définissez-la sur **DEBUG** si vous souhaitez voir les traces d'erreur uniquement lorsque **log.level=DEBUG** est activé.
- **format** : définit la chaîne de formatage des journaux. Si le type de journal est **plain**, le format de journal devrait être une chaîne. Reportez-vous aux [attributs LogRecord](https://docs.python.org/3.6/library/logging.html#logrecord-attributes) pour obtenir la liste des attributs disponibles. Si le type de journal est **json**, le format de journal peut être une liste en plus d'une chaîne. Chaque élément de la liste devrait correspondre à un attribut LogRecord. Attention : seul le nom du champ est requis, et **%(** et **)** doivent être omis. Si vous souhaitez afficher un champ de journal avec un nom de clé différent, utilisez un dictionnaire où la clé du dictionnaire est le champ de journal, et la valeur est le nom du champ que vous souhaitez afficher dans le journal. Valeur par défaut : **%(asctime)s %(levelname)s: %(message)s**
- **dateformat** : définit la chaîne de formatage de la date et de l'heure. (voir la documentation de [formatTime()](https://docs.python.org/3.6/library/logging.html#logging.Formatter.formatTime))
- **static_fields** : ajoute des champs supplémentaires au journal. Cette option n'est disponible que lorsque le type de journal est défini sur **json**.
- **max_queue_size** : Patroni utilise une journalisation en deux étapes. Les enregistrements de journal sont écrits dans une file mémoire et un thread distinct les extrait de la file pour les écrire sur stderr ou dans un fichier. La taille maximale de la file interne est limitée par défaut à **1000** enregistrements, ce qui suffit à conserver les journaux des dernières 1h20.
- **dir** : Répertoire dans lequel écrire les journaux d'application. Le répertoire doit exister et être accessible en écriture par l'utilisateur exécutant Patroni. Si cette valeur est définie, l'application conserve par défaut 4 fichiers de journaux de 25 Mo chacun. Vous pouvez ajuster ces valeurs de rétention à l'aide de `file_num` et `file_size` (voir ci-dessous).
- **mode** : Permissions des fichiers de journal (par exemple, `0644`). Si non spécifié, les permissions sont déterminées selon la valeur courante de umask.
- **file_num** : Nombre de fichiers de journaux d'application à conserver.
- **file_size** : Taille du fichier patroni.log (en octets) qui déclenche un roulement des journaux.
- **loggers** : Cette section permet de redéfinir le niveau de journalisation par module Python.
  - **patroni.postmaster: WARNING**
  - **urllib3: DEBUG**
- **deduplicate_heartbeat_logs** : Si défini à `true`, les journaux de battement de cœur identiques successifs ne seront pas affichés. La valeur par défaut est `false`.

> [!WARNING]
> Le moment auquel la boucle HA s'exécute peut constituer une information très utile pour diagnostiquer les basculements dus à un épuisement des ressources et à des problèmes similaires. Lorsque `deduplicate_heartbeat_logs` est défini sur `true`, aucun journal n'est généré pour l'exécution de la boucle HA (sauf en cas de changement de leader), ce qui fait que cette information potentiellement utile ne sera pas disponible dans les journaux.

Voici un exemple de configuration de Patroni pour activer la journalisation au format JSON.

```yaml
log:
   type: json
   format:
      - message
      - module
      - asctime: '@timestamp'
      - levelname: level
   static_fields:
      app: patroni
```

<a id="bootstrap_settings"></a>

--------

## Configuration d'amorçage {#bootstrap-configuration}

> [!NOTE]
> Une fois que Patroni a initialisé le cluster pour la première fois et que les paramètres ont été stockés dans le DCS, toutes les modifications ultérieures apportées à la section `bootstrap.dcs` du fichier de configuration YAML n'auront aucun effet ! Pour les modifier, utilisez soit la commande [patronictl_edit_config](/fr/patroni/patronictl#patronictl_edit_config), soit l'[API REST](/fr/patroni/rest_api#rest_api) de Patroni.

- **bootstrap** :
  - **dcs** : Cette section sera écrite dans `/<namespace>/<scope>/config` du magasin de configuration donné après l'amorçage du nouveau cluster. La configuration dynamique globale du cluster. Vous pouvez y placer n'importe quel paramètre décrit dans les [Paramètres de configuration dynamique](/fr/patroni/config/dynamic#dynamic) sous `bootstrap.dcs` ; une fois que Patroni aura initialisé (amorcé) le nouveau cluster, il écrira cette section dans `/<namespace>/<scope>/config` du magasin de configuration.

  - **method** : script personnalisé à utiliser pour amorcer ce cluster.

    Consultez la [documentation des méthodes d'amorçage personnalisées](/fr/patroni/replica_bootstrap#custom_bootstrap) pour plus de détails. Lorsque `initdb` est spécifié, la commande par défaut `initdb` est utilisée. `initdb` est également déclenché lorsque le paramètre `method` est absent du fichier de configuration.

  - **initdb** : (facultatif) liste des options à passer à initdb.

    - **- data-checksums** : doit être activé lorsque pg_rewind est nécessaire sur la version 9.3.
    - **- encoding: UTF8** : encodage par défaut pour les nouvelles bases de données.
    - **- locale: UTF8** : paramètre régional par défaut pour les nouvelles bases de données.

  - **post_bootstrap** ou **post_init** : un script supplémentaire exécuté après l’initialisation du cluster. Le script reçoit une chaîne de connexion au format URL (avec le superutilisateur du cluster comme nom d’utilisateur). La variable PGPASSFILE est définie sur le chemin d’accès au fichier pgpass.

<a id="citus_settings"></a>

--------

## Citus {#citus}

Active l'intégration de Patroni avec [Citus](https://docs.citusdata.com). Si configuré, Patroni s'occupe de l'enregistrement des nœuds workers Citus sur le coordinateur. Vous trouverez plus d'informations sur le support Citus [ici](/fr/patroni/citus#citus).

- **group** : l'identifiant du groupe Citus, entier. Utilisez `0` pour le coordinateur et `1`, `2`, etc. pour les workers
- **database** : la base de données où l'extension [citus](/fr/patroni/citus#citus) doit être créée. Doit être identique sur le coordinateur et tous les workers. Actuellement, une seule base de données est prise en charge.

<a id="consul_settings"></a>

--------

## Consul {#consul}

La plupart des paramètres sont facultatifs, mais vous devez renseigner **host** ou **url**.

- **host** : l'hôte:port de l'agent local Consul.
- **url** : URL de l'agent local Consul, au format : http(s)://host:port.
- **port** : (facultatif) port de Consul.
- **scheme** : (facultatif) **http** ou **https**, par défaut **http**.
- **token** : (facultatif) jeton ACL.
- **verify** : (facultatif) indique si le certificat SSL doit être vérifié pour les requêtes HTTPS.
- **cacert** : (facultatif) certificat CA. Si présent, active la validation.
- **cert** : (facultatif) fichier contenant le certificat client.
- **key** : (facultatif) fichier contenant la clé client. Peut être vide si la clé est incluse dans **cert**.
- **dc** : (facultatif) Centre de données avec lequel établir la communication. Par défaut, le centre de données de l'hôte est utilisé.
- **consistency** : (facultatif) Sélectionne le mode de cohérence de consul. Les valeurs possibles sont `default`, `consistent` ou `stale` (plus de détails dans [référence API consul](https://www.consul.io/api/features/consistency.html/))
- **checks** : (facultatif) liste des vérifications de santé Consul utilisées pour la session. Par défaut, une liste vide est utilisée.
- **register_service** : (facultatif) indique s'il faut enregistrer un service avec le nom défini par le paramètre scope et l'étiquette master, primary, replica ou standby-leader selon le rôle du nœud. La valeur par défaut est **false**.
- **service_tags** : (facultatif) étiquettes statiques supplémentaires à ajouter au service Consul, en plus du rôle (`primary`/`replica`/`standby-leader`). Par défaut, une liste vide est utilisée.
- **service_check_interval** : (facultatif) fréquence à laquelle effectuer la vérification de santé contre l'URL enregistrée. Valeur par défaut : '5s'.
- **service_check_tls_server_name** : (facultatif) remplacer le nom d'hôte SNI lors de la connexion via TLS, voir également [référence de l'API de vérification de l'agent Consul](https://www.consul.io/api-docs/agent/check#tlsservername).

Le `token` doit disposer des autorisations ACL suivantes :

    service_prefix "${scope}" {
        policy = "write"
    }
    key_prefix "${namespace}/${scope}" {
        policy = "write"
    }
    session_prefix "" {
        policy = "write"
    }

--------

## etcd {#etcd}

La plupart des paramètres sont facultatifs, mais vous devez spécifier l’un des éléments suivants : **host**, **hosts**, **url**, **proxy** ou **srv**

- **host** : l'hôte:port de l'endpoint etcd.
- **hosts** : liste des endpoints etcd au format host1:port1,host2:port2,etc... Peut être une chaîne séparée par des virgules ou une liste YAML réelle.
- **use_proxies** : si ce paramètre est défini à true, Patroni considère **hosts** comme une liste de proxys et ne procède pas à la découverte de la topologie du cluster etcd.
- **url** : URL de l'endpoint etcd.
- **proxy** : URL du proxy pour etcd. Si vous vous connectez à etcd via un proxy, utilisez ce paramètre au lieu de **url**.
- **srv** : Domaine dans lequel rechercher les enregistrements SRV pour la découverte automatique du cluster. Patroni tentera de consulter ces noms de service SRV pour le domaine spécifié (dans cet ordre, jusqu'à la première réussite) : `_etcd-client-ssl`, `_etcd-client`, `_etcd-ssl`, `_etcd`, `_etcd-server-ssl`, `_etcd-server`. Si des enregistrements SRV pour `_etcd-server-ssl` ou `_etcd-server` sont récupérés, le protocole pair ETCD sera utilisé pour interroger ETCD afin d'obtenir la liste des membres disponibles. Sinon, les hôtes provenant des enregistrements SRV seront utilisés.
- **srv_suffix** : Configure un suffixe pour le nom SRV interrogé lors de la découverte. Utilisez cette option pour distinguer plusieurs clusters etcd sous le même domaine. Fonctionne uniquement en conjonction avec **srv**. Par exemple, si `srv_suffix: foo` et `srv: example.org` sont définis, la requête DNS SRV suivante est effectuée : `_etcd-client-ssl-foo._tcp.example.org` (et ainsi de suite pour chaque nom de service SRV etcd possible).
- **protocol** : (facultatif) http ou https, si non spécifié, http est utilisé. Si **url** ou **proxy** est spécifié, le protocole est déduit de ces valeurs.
- **username** : (facultatif) nom d'utilisateur pour l'authentification etcd.
- **password** : (facultatif) mot de passe pour l'authentification etcd.
- **cacert** : (facultatif) certificat CA. Si présent, active la validation.
- **cert** : (facultatif) fichier contenant le certificat client.
- **key** : (facultatif) fichier contenant la clé client. Peut être vide si la clé est incluse dans **cert**.

--------

## Etcdv3 {#etcdv3}

Si vous souhaitez que Patroni fonctionne avec un cluster etcd via la version 3 du protocole, vous devez utiliser la section `etcd3` dans le fichier de configuration de Patroni. Tous les paramètres de configuration sont identiques à ceux de `etcd`.

> [!WARNING]
> Les clés créées avec la version 2 du protocole ne sont pas visibles avec la version 3 du protocole, et inversement ; il n'est donc pas possible de passer de `etcd` à `etcd3` en mettant simplement à jour le fichier de configuration Patroni. En outre, Patroni utilise la passerelle gRPC d'etcd (proxy) pour communiquer avec l'API V3, ce qui rend l'authentification par nom commun TLS impossible.

--------

## ZooKeeper {#zookeeper}

- **hosts** : Liste des membres du cluster ZooKeeper au format : \['host1:port1', 'host2:port2', 'etc...'\].
- **use_ssl** : (facultatif) Indique si le protocole SSL est utilisé. Valeur par défaut : `false`. Si défini à `false`, tous les paramètres spécifiques à SSL sont ignorés.
- **cacert** : (facultatif) Certificat de l'autorité de certification. S'il est présent, il active la validation.
- **cert** : (facultatif) Fichier contenant le certificat client.
- **key** : (facultatif) Fichier contenant la clé client.
- **key_password** : (facultatif) Mot de passe de la clé client.
- **verify** : (facultatif) Indique si la vérification du certificat doit être effectuée ou non. La valeur par défaut est `true`.
- **set_acls** : (facultatif) Si défini, configure Kazoo pour appliquer une ACL par défaut à chaque ZNode qu'il crée. Les ACL peuvent utiliser le schéma `x509` (par défaut) ou d'autres schémas ZooKeeper pris en charge, tels que `digest`. Elles doivent être spécifiées sous forme de dictionnaire, où la clé est le principal complet (éventuellement préfixé par le schéma) et la valeur une liste de permissions. Les permissions peuvent être une ou plusieurs des valeurs suivantes : `CREATE`, `READ`, `WRITE`, `DELETE`, `ADMIN`, ou `ALL`. Par exemple, `set_acls: {CN=principal1: [CREATE, READ], digest:principal2:+pjROuBuuwNNSujKyH8dGcEnFPQ=: [ALL]}`.
- **auth_data** : (facultatif) Informations d'authentification à utiliser pour la connexion. Doit être un dictionnaire au format où `scheme` est la clé et `credential` la valeur. Valeur par défaut : dictionnaire vide.

> [!NOTE]
> Il est obligatoire d'installer `kazoo>=2.6.0` pour prendre en charge le SSL.

--------

## Exhibitor {#exhibitor}

- **hosts** : liste initiale des nœuds Exhibitor (ZooKeeper) au format : « host1,host2,etc... ». Cette liste est mise à jour automatiquement chaque fois que la topologie du cluster Exhibitor (ZooKeeper) change.
- **poll_interval** : fréquence à laquelle la liste des nœuds ZooKeeper et Exhibitor doit être actualisée depuis Exhibitor.
- **port** : port Exhibitor.

<a id="kubernetes_settings"></a>

--------

## Kubernetes {#kubernetes}

- **bypass_api_service** : (facultatif) Lors de la communication avec l'API Kubernetes, Patroni utilise généralement le service [kubernetes](/fr/patroni/kubernetes#kubernetes), dont l'adresse est exposée dans les pods via la variable d'environnement `KUBERNETES_SERVICE_HOST`. Si `bypass_api_service` est défini sur `true`, Patroni résout la liste des nœuds API derrière le service et établit une connexion directe avec eux.
- **namespace** : (facultatif) espace de noms Kubernetes dans lequel s'exécute le pod Patroni. Valeur par défaut : `default`.
- **labels** : Étiquettes au format `{label1: value1, label2: value2}`. Ces étiquettes seront utilisées pour localiser les objets existants (Pods et soit des Endpoints, soit des ConfigMaps) associés au cluster actuel. Patroni les définira également sur chaque objet (Endpoint ou ConfigMap) qu'il crée.
- **scope_label** : (facultatif) nom de l'étiquette contenant le nom du cluster. Valeur par défaut : `cluster-name`.
- **bootstrap_labels** : (facultatif) Étiquettes au format `{label1: value1, label2: value2}`. Ces étiquettes seront attribuées au pod Patroni lorsque son état est `initializing new cluster`, `running custom bootstrap script`, `starting after custom bootstrap` ou `creating replica`.
- **role_label** : (facultatif) nom de l'étiquette contenant le rôle (`primary`, `replica` ou autre valeur personnalisée). Patroni définira cette étiquette sur le pod dans lequel il s'exécute. Valeur par défaut : `role`.
- **leader_label_value** : (facultatif) valeur de l'étiquette du pod lorsque le rôle de Postgres est `primary`. Valeur par défaut : `primary`.
- **follower_label_value** : (facultatif) valeur de l'étiquette du pod lorsque le rôle de Postgres est `replica`. Valeur par défaut : `replica`.
- **standby_leader_label_value** : (facultatif) valeur de l'étiquette du pod lorsque le rôle de Postgres est `standby_leader`. Valeur par défaut : `primary`.
- **tmp_role_label** : (facultatif) nom de l'étiquette temporaire contenant le rôle (`primary` ou `replica`). La valeur de cette étiquette utilisera toujours la valeur par défaut correspondante au rôle. À définir uniquement si nécessaire.
- **use_endpoints** : (facultatif) si défini à true, Patroni utilisera des Endpoints au lieu de ConfigMaps pour effectuer les élections du leader et maintenir l'état du cluster.
- **pod_ip** : (facultatif) adresse IP du pod dans lequel s'exécute Patroni. Cette valeur est requise lorsque `use_endpoints` est activé et est utilisée pour remplir les sous-ensembles du point de terminaison leader lorsque le PostgreSQL du pod est promu.
- **ports** : (facultatif) si l'objet Service possède un nom de port, ce même nom doit apparaître dans l'objet Endpoint, sinon le service ne fonctionnera pas. Par exemple, si votre service est défini comme `{Kind: Service, spec: {ports: [{name: postgresql, port: 5432, targetPort: 5432}]}}`, vous devez définir `kubernetes.ports: [{"name": "postgresql", "port": 5432}]` et Patroni l'utilisera pour mettre à jour les sous-ensembles de l'Endpoint leader. Ce paramètre n'est utilisé que si `kubernetes.use_endpoints` est défini.
- **cacert** : (facultatif) indique le fichier CA_BUNDLE contenant les certificats des autorités de certification approuvées pour vérifier les certificats SSL de l'API Kubernetes. En l'absence de valeur, Patroni utilise celle du secret ServiceAccount.
- **retriable_http_codes** : (facultatif) liste des codes d'état HTTP de l'API K8s pour lesquels une nouvelle tentative doit être effectuée. Par défaut, Patroni réessaie pour `500`, `503` et `504`, ou lorsque la réponse de l'API K8s contient l'en-tête HTTP `retry-after`.

<a id="raft_settings"></a>

--------

## Raft (obsolète) {#raft-deprecated}

- **self_addr** : adresse `ip:port` d'écoute des connexions Raft. `self_addr` doit être accessible depuis les autres nœuds du cluster. Sans cette valeur, le nœud ne participe pas au consensus.

- **bind_addr** : (facultatif) `ip:port` sur lequel écouter pour les connexions Raft. Si non spécifié, `self_addr` sera utilisé.

- **partner_addrs** : liste des autres nœuds Patroni du cluster au format : \['ip1:port', 'ip2:port', 'etc...'\]

- **data_dir** : répertoire dans lequel stocker le journal Raft et les instantanés. Si non spécifié, le répertoire de travail actuel est utilisé.

- **password** : (facultatif) Chiffrer le trafic Raft avec un mot de passe spécifié, nécessite le module `cryptography`.
- **min_timeout** : (facultatif) délai minimum d'élection en secondes pour l'implémentation Raft sous-jacente pysyncobj. Doit être supérieur à 3 × `append_entries_period`. Valeur par défaut : `0.4`.
- **max_timeout** : (facultatif) délai maximum d'élection en secondes pour l'implémentation Raft sous-jacente pysyncobj. Doit être supérieur à `min_timeout`. Valeur par défaut : `1.4`.
- **connection_timeout** : (facultatif) durée en secondes après laquelle une connexion sans réception de données est considérée comme inactive. Doit être supérieur ou égal à `max_timeout`. Valeur par défaut : `3.5`.
- **append_entries_period** : (facultatif) intervalle en secondes pour l'envoi des commandes de battement de cœur (append_entries). Doit être inférieur à un tiers de `min_timeout`. Valeur par défaut : `0.1`.
- **connection_retry_time** : (facultatif) intervalle en secondes entre les tentatives de reconnexion aux nœuds hors ligne. Valeur par défaut : `5.0`.
- **leader_fallback_timeout** : (facultatif) durée en secondes après laquelle un leader ne recevant aucune réponse de la majorité redevient un suiveur. Doit être supérieur à `append_entries_period`. Valeur par défaut : `30.0`.

> [!NOTE]
> Ces paramètres de temporisation sont utiles dans les réseaux à forte latence où les temporisations par défaut de pysyncobj sont trop strictes. Les contraintes suivantes doivent être respectées : `min_timeout` > 3 * `append_entries_period`, `max_timeout` > `min_timeout`, `connection_timeout` >= `max_timeout` et `leader_fallback_timeout` > `append_entries_period`. Patroni vérifie ces conditions au démarrage et refuse de démarrer si elles sont violées. Ces valeurs ne peuvent pas être modifiées en cours d'exécution et nécessitent un redémarrage.
>
> [!WARNING]
> Ces paramètres ne font que relâcher les temporisations d'élection et de connexion de pysyncobj ; ils n'étendent pas le délai maximal par commande que Patroni applique aux opérations Raft. Chaque commande Raft (rafraîchissement du verrou du leader, écriture de l'état du cluster) doit toujours s'achever dans un délai de `retry_timeout` (valeur par défaut `10`). Sur des liens à très forte latence — environ au-dessus de quelques secondes de temps de trajet aller-retour — une seule commande peut dépasser `retry_timeout` même si `connection_timeout` est porté bien au-dessus du RTT, ce qui fait que le DCS semble inaccessible et le primaire peut être rétrogradé. Sur de tels liens, il faut également augmenter `retry_timeout` et `ttl` en conséquence, tout en maintenant `loop_wait + 2 * retry_timeout <= ttl`.

FAQ rapide sur l’implémentation Raft

  - Q : Comment lister tous les nœuds fournissant le consensus ?

    A : `syncobj_admin -conn host:port -status` où l’adresse hôte:port correspond à l’adresse d’un nœud du cluster

  - Q : Nœud qui faisait partie du consensus et qui a disparu ; je ne peux pas réutiliser la même IP pour un autre nœud. Comment supprimer ce nœud du consensus ?

    A : `syncobj_admin -conn host:port -remove host2:port2` où `host2:port2` correspond à l'adresse du nœud que vous souhaitez supprimer du consensus.

  - Q : Où obtenir l'utilitaire `syncobj_admin` ?

    A : Il est installé conjointement avec le module `pysyncobj` (implémentation Python du protocole RAFT), qui est une dépendance de Patroni.

  - Q : Est-il possible d'exécuter un nœud Patroni sans l'ajouter au consensus ?

    A : Oui, il suffit de commenter ou de supprimer `raft.self_addr` dans la configuration de Patroni.

  - Q : Est-il possible d'exécuter Patroni et PostgreSQL uniquement sur deux nœuds ?

    A : Oui, sur le troisième nœud, vous pouvez exécuter `patroni_raft_controller` (sans Patroni ni PostgreSQL). Dans un tel déploiement, il est possible de perdre temporairement un nœud sans affecter le primaire.

<a id="postgresql_settings"></a>

--------

## PostgreSQL {#postgresql}

- **postgresql** :
  - **authentication** :

    - **superuser** :
      - **username** : nom de l'utilisateur superutilisateur, défini lors de l'initialisation (initdb) et utilisé ultérieurement par Patroni pour se connecter à PostgreSQL.
      - **password** : mot de passe de l'utilisateur superutilisateur, défini lors de l'initialisation (initdb).
      - **sslmode** : (facultatif) correspond au paramètre de connexion [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE), qui permet à un client de spécifier le mode de négociation TLS avec le serveur. Pour plus d'informations sur le fonctionnement de chaque mode, veuillez consulter la documentation [PostgreSQL](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). Le mode par défaut est `prefer`.
      - **sslkey** : (facultatif) correspond au paramètre de connexion [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY), qui précise l'emplacement de la clé secrète utilisée avec le certificat client.
      - **sslpassword** : (facultatif) correspond au paramètre de connexion [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD), qui précise le mot de passe de la clé secrète spécifiée dans `sslkey`.
      - **sslcert** : (facultatif) correspond au paramètre de connexion [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT), qui précise l'emplacement du certificat client.
      - **sslrootcert** : (facultatif) correspond au paramètre de connexion [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT) , qui précise l'emplacement d'un fichier contenant un ou plusieurs certificats d'autorités de certification (CA) utilisés par le client pour vérifier le certificat d'un serveur.
      - **sslcrl** : (facultatif) correspond au paramètre de connexion [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL) , qui précise l'emplacement d'un fichier contenant une liste de révocation de certificats. Un client refusera la connexion à tout serveur dont le certificat figure dans cette liste.
      - **sslcrldir** : (facultatif) correspond au paramètre de connexion [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR), qui précise l'emplacement d'un répertoire contenant des fichiers listant les certificats révoqués. Un client refusera de se connecter à tout serveur dont le certificat figure dans cette liste.
      - **sslnegotiation** : (facultatif) correspond au paramètre de connexion [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION), qui contrôle la négociation du chiffrement SSL avec le serveur, le cas échéant.
      - **gssencmode** : (facultatif) correspond au paramètre de connexion [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE), qui détermine si une connexion TCP/IP sécurisée GSS sera négociée avec le serveur, et avec quelle priorité
      - **channel_binding** : (facultatif) correspond au paramètre de connexion [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING), qui contrôle l'utilisation du binding de canal par le client.
    - **replication** :
      - **username** : nom d'utilisateur de réplication ; l'utilisateur sera créé lors de l'initialisation. Les répliques utiliseront cet utilisateur pour accéder à la source de réplication via la réplication en flux
      - **password** : mot de passe de réplication ; l'utilisateur sera créé lors de l'initialisation.
      - **sslmode** : (facultatif) correspond au paramètre de connexion [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE), qui permet à un client de spécifier le mode de négociation TLS avec le serveur. Pour plus d'informations sur le fonctionnement de chaque mode, veuillez consulter la documentation [PostgreSQL](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). Le mode par défaut est `prefer`.
      - **sslkey** : (facultatif) correspond au paramètre de connexion [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY), qui précise l'emplacement de la clé secrète utilisée avec le certificat client.
      - **sslpassword** : (facultatif) correspond au paramètre de connexion [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD), qui précise le mot de passe de la clé secrète spécifiée dans `sslkey`.
      - **sslcert** : (facultatif) correspond au paramètre de connexion [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT), qui précise l'emplacement du certificat client.
      - **sslrootcert** : (facultatif) correspond au paramètre de connexion [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT) , qui précise l'emplacement d'un fichier contenant un ou plusieurs certificats d'autorités de certification (CA) utilisés par le client pour vérifier le certificat d'un serveur.
      - **sslcrl** : (facultatif) correspond au paramètre de connexion [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL) , qui précise l'emplacement d'un fichier contenant une liste de révocation de certificats. Un client refusera la connexion à tout serveur dont le certificat figure dans cette liste.
      - **sslcrldir** : (facultatif) correspond au paramètre de connexion [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR), qui précise l'emplacement d'un répertoire contenant des fichiers listant les certificats révoqués. Un client refusera de se connecter à tout serveur dont le certificat figure dans cette liste.
      - **sslnegotiation** : (facultatif) correspond au paramètre de connexion [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION), qui contrôle la négociation du chiffrement SSL avec le serveur, le cas échéant.
      - **gssencmode** : (facultatif) correspond au paramètre de connexion [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE), qui détermine si une connexion TCP/IP sécurisée GSS sera négociée avec le serveur, et avec quelle priorité
      - **channel_binding** : (facultatif) correspond au paramètre de connexion [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING), qui contrôle l'utilisation du binding de canal par le client.
    - **rewind** :
      - **username** : (facultatif) nom de l'utilisateur pour `pg_rewind` ; l'utilisateur sera créé lors de l'initialisation de PostgreSQL 11+ et toutes les [permissions](https://www.postgresql.org/docs/11/app-pgrewind.html#id-1.9.5.8.8) nécessaires lui seront accordées.
      - **password** : (facultatif) mot de passe de l'utilisateur pour `pg_rewind` ; l'utilisateur sera créé lors de l'initialisation.
      - **sslmode** : (facultatif) correspond au paramètre de connexion [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE), qui permet à un client de spécifier le mode de négociation TLS avec le serveur. Pour plus d'informations sur le fonctionnement de chaque mode, veuillez consulter la documentation [PostgreSQL](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). Le mode par défaut est `prefer`.
      - **sslkey** : (facultatif) correspond au paramètre de connexion [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY), qui précise l'emplacement de la clé secrète utilisée avec le certificat client.
      - **sslpassword** : (facultatif) correspond au paramètre de connexion [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD), qui précise le mot de passe de la clé secrète spécifiée dans `sslkey`.
      - **sslcert** : (facultatif) correspond au paramètre de connexion [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT), qui précise l'emplacement du certificat client.
      - **sslrootcert** : (facultatif) correspond au paramètre de connexion [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT) , qui précise l'emplacement d'un fichier contenant un ou plusieurs certificats d'autorités de certification (CA) utilisés par le client pour vérifier le certificat d'un serveur.
      - **sslcrl** : (facultatif) correspond au paramètre de connexion [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL) , qui précise l'emplacement d'un fichier contenant une liste de révocation de certificats. Un client refusera la connexion à tout serveur dont le certificat figure dans cette liste.
      - **sslcrldir** : (facultatif) correspond au paramètre de connexion [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR), qui précise l'emplacement d'un répertoire contenant des fichiers listant les certificats révoqués. Un client refusera de se connecter à tout serveur dont le certificat figure dans cette liste.
      - **sslnegotiation** : (facultatif) correspond au paramètre de connexion [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION), qui contrôle la négociation du chiffrement SSL avec le serveur, le cas échéant.
      - **gssencmode** : (facultatif) correspond au paramètre de connexion [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE), qui détermine si une connexion TCP/IP sécurisée GSS sera négociée avec le serveur, et avec quelle priorité
      - **channel_binding** : (facultatif) correspond au paramètre de connexion [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING), qui contrôle l'utilisation du binding de canal par le client.

  - **callbacks** : scripts de rappel à exécuter lors de certaines actions. Patroni transmettra l'action, le rôle et le nom du cluster. (Voir le fichier scripts/aws.py pour un exemple de mise en œuvre.)

    - **on_reload** : exécuter ce script lorsqu'un rechargement de la configuration est déclenché.
    - **on_restart** : exécuter ce script lorsqu'un redémarrage de PostgreSQL est effectué (sans changement de rôle).
    - **on_role_change** : exécuter ce script lorsqu'un changement de rôle de PostgreSQL est en cours (promotion ou rétrogradation).
    - **on_start** : exécuter ce script lors du démarrage de PostgreSQL.
    - **on_stop** : exécuter ce script lors de l'arrêt de PostgreSQL.

  - **connect_address** : adresse IP + port par lequel PostgreSQL est accessible depuis d'autres nœuds et applications.

  - **proxy_address** : adresse IP + port par lequel un pool de connexions (par exemple pgbouncer) en cours d'exécution à côté de Postgres est accessible. La valeur est écrite dans la clé member du DCS sous la forme `proxy_url` et peut être utilisée et se révéler utile pour la découverte de services.

  - **create_replica_methods** : une liste ordonnée des méthodes de création pour transformer un nœud Patroni en nouvelle réplique. La méthode par défaut est « basebackup » ; les autres méthodes sont supposées faire référence à des scripts, chacun configuré comme un élément de configuration distinct. Voir la documentation [méthodes personnalisées de création de réplique](/fr/patroni/replica_bootstrap#custom_replica_creation) pour plus d'explications.

  - **data_dir** : Emplacement du répertoire de données PostgreSQL, soit [existant](/fr/patroni/existing_data#existing_data) soit à initialiser par Patroni.

  - **config_dir** : Emplacement du répertoire de configuration de Postgres, par défaut le répertoire de données. Doit être accessible en écriture par Patroni.

  - **bin_dir** : (facultatif) Chemin vers les binaires PostgreSQL (pg_ctl, initdb, pg_controldata, pg_basebackup, postgres, pg_isready, pg_rewind). Si ce paramètre n'est pas fourni ou est une chaîne vide, la variable d'environnement PATH sera utilisée pour localiser les exécutables.

  - **bin_name** : (facultatif) Permet de remplacer les noms des binaires Postgres, si vous utilisez une distribution Postgres personnalisée :

    - **pg_ctl** : (facultatif) Nom personnalisé pour le binaire `pg_ctl`.
    - **initdb** : (facultatif) Nom personnalisé pour le binaire `initdb`.
    - **pg_controldata** : (facultatif) Nom personnalisé pour le binaire `pg_controldata`.
    - **pg_basebackup** : (facultatif) Nom personnalisé pour le binaire `pg_basebackup`.
    - **postgres** : (facultatif) Nom personnalisé pour le binaire `postgres`.
    - **pg_isready** : (facultatif) Nom personnalisé pour le binaire `pg_isready`.
    - **pg_rewind** : (facultatif) Nom personnalisé pour le binaire `pg_rewind`.

  - **listen** : adresse IP + port auxquels Postgres écoute ; doit être accessible depuis les autres nœuds du cluster, si vous utilisez la réplication en flux. Plusieurs adresses séparées par des virgules sont autorisées, à condition que le composant port soit ajouté après la dernière adresse, séparé par deux-points, par exemple `listen: 127.0.0.1,127.0.0.2:5432`. Patroni utilisera la première adresse de cette liste pour établir des connexions locales vers le nœud PostgreSQL.

  - **use_unix_socket** : indique que Patroni doit privilégier l'utilisation de sockets Unix pour se connecter au cluster. La valeur par défaut est `false`. Si `unix_socket_directories` est définie, Patroni utilisera la première valeur adaptée parmi celles-ci pour se connecter au cluster, puis passera à TCP si aucune valeur ne convient. Si `unix_socket_directories` n'est pas spécifié dans `postgresql.parameters`, Patroni supposera que la valeur par défaut doit être utilisée et omettra `host` des paramètres de connexion.

  - **use_unix_socket_repl** : spécifie que Patroni doit privilégier l'utilisation de sockets Unix pour la connexion utilisateur de réplication au cluster. La valeur par défaut est `false`. Si `unix_socket_directories` est définie, Patroni utilisera la première valeur adaptée parmi celles-ci pour se connecter au cluster, puis passera à TCP en cas d'absence de valeur adaptée. Si `unix_socket_directories` n'est pas spécifié dans `postgresql.parameters`, Patroni supposera que la valeur par défaut doit être utilisée et omettra `host` des paramètres de connexion.

  - **pgpass** : chemin vers le fichier de mots de passe [.pgpass](https://www.postgresql.org/docs/current/static/libpq-pgpass.html). Patroni crée ce fichier avant d'exécuter pg_basebackup, le script post_init et dans certaines autres circonstances. Le chemin doit être accessible en écriture par Patroni.

  - **recovery_conf** : paramètres de configuration supplémentaires écrits dans recovery.conf lors de la configuration du suiveur.

  - **custom_conf** : chemin vers un fichier `postgresql.conf` personnalisé facultatif, qui sera utilisé à la place de `postgresql.base.conf`. Le fichier doit exister sur tous les nœuds du cluster, être lisible par PostgreSQL et sera inclus à partir de son emplacement réel sur `postgresql.conf`. Notez que Patroni ne surveillera pas ce fichier pour les modifications, ni ne le sauvegardera. Toutefois, ses paramètres peuvent toujours être remplacés par les mécanismes de configuration dynamique de Patroni — voir [configuration dynamique](/fr/patroni/config#config) pour plus de détails.

  - **parameters** : paramètres de configuration (GUC) pour Postgres au format `{ssl: "on", ssl_cert_file: "cert_file"}`.
  - **parameters_primary** : (facultatif) substitutions de paramètres spécifiques au rôle pour le primaire. Ces valeurs sont fusionnées avec et remplacent celles de la section **parameters** de base.
  - **parameters_replica** : (facultatif) substitutions de paramètres spécifiques au rôle pour la réplique. Ces valeurs sont fusionnées avec et remplacent celles de la section **parameters** de base.
  - **parameters_standby_leader** : (facultatif) substitutions de paramètres spécifiques au rôle pour standby_leader. Ces valeurs sont fusionnées avec et remplacent celles du paramètre **parameters**.

  - **pg_hba** : liste des lignes que Patroni utilisera pour générer `pg_hba.conf`. Patroni ignore ce paramètre si le paramètre PostgreSQL `hba_file` possède une valeur différente de celle par défaut. Associé à la [configuration dynamique](/fr/patroni/config/dynamic#dynamic), ce paramètre simplifie la gestion de `pg_hba.conf`.

    - **- host all all 0.0.0.0/0 md5**
    - **- host replication replicator 127.0.0.1/32 md5** : Une ligne de ce type est obligatoire pour la réplication.
  - **pg_hba_primary** : (facultatif) entrées pg_hba spécifiques au rôle pour le serveur primaire. Elles remplacent entièrement **pg_hba** (pas de fusion). Si non définies, **pg_hba** est utilisée.
  - **pg_hba_replica** : (facultatif) entrées pg_hba spécifiques au rôle pour la réplique. Elles remplacent entièrement **pg_hba** (pas de fusion). Si non définies, **pg_hba** est utilisée.
  - **pg_hba_standby_leader** : (facultatif) entrées pg_hba spécifiques au rôle pour standby_leader. Elles remplacent entièrement **pg_hba** (pas de fusion). Si non définies, **pg_hba** est utilisée.

  - **pg_ident** : liste de lignes que Patroni utilisera pour générer `pg_ident.conf`. Patroni ignore ce paramètre si le paramètre `ident_file` PostgreSQL est défini avec une valeur différente de celle par défaut. Associé à la [configuration dynamique](/fr/patroni/config/dynamic#dynamic), ce paramètre simplifie la gestion de `pg_ident.conf`.

    - **- mapname1 systemname1 pguser1**
    - **- mapname1 systemname2 pguser2**
  - **pg_ident_primary** : (facultatif) entrées pg_ident spécifiques aux rôles pour le serveur primaire. Elles remplacent entièrement **pg_ident** (pas de fusion). Si non définies, **pg_ident** est utilisée.
  - **pg_ident_replica** : (facultatif) entrées pg_ident spécifiques aux rôles pour la réplique. Elles remplacent entièrement **pg_ident** (pas de fusion). Si non définies, **pg_ident** est utilisée.
  - **pg_ident_standby_leader** : (facultatif) entrées pg_ident spécifiques au rôle pour standby_leader. Elles remplacent entièrement **pg_ident** (aucune fusion n'est effectuée). Si non définies, **pg_ident** est utilisée.

  - **pg_ctl_timeout** : Durée d'attente de pg_ctl lors des opérations `start`, `stop` ou `restart`. Valeur par défaut : 60 secondes.

  - **use_pg_rewind** : tenter d'utiliser pg_rewind sur l'ancien leader lorsqu'il rejoint le cluster en tant que réplique. Le cluster doit être initialisé avec `data page checksums` (`--data-checksums` pour `initdb`) et/ou `wal_log_hints` doit être défini sur `on`, sinon `pg_rewind` ne fonctionnera pas.

  - **rewind** : (facultatif) options personnalisées à passer à la commande `pg_rewind`. Peut être spécifié sous forme de liste de chaînes de caractères et/ou de dictionnaires clé-valeur simples. Les options non autorisées incluent : `target-pgdata`, `source-pgdata`, `source-server`, `write-recovery-conf`, `dry-run`, `restore-target-wal`, `config-file`, `no-ensure-shutdown`, `version`, et `help`. Exemple d'utilisation :

    ```yaml
    postgresql:
      rewind:
        - debug
        - progress
        - sync-method: fsync
    ```

  - **remove_data_directory_on_rewind_failure** : Si cette option est activée, Patroni supprime le répertoire de données PostgreSQL et recrée la réplique. Sinon, il tente de suivre le nouveau leader. La valeur par défaut est **false**.

  - **remove_data_directory_on_diverged_timelines** : Patroni supprimera le répertoire de données PostgreSQL et recréera la réplique si elle détecte une divergence des timelines et que l'ancien nœud primaire ne peut pas démarrer le streaming depuis le nouveau nœud primaire. Cette option est utile lorsque `pg_rewind` ne peut pas être utilisé. Lors de la vérification de la divergence des timelines sur PostgreSQL v10 et les versions antérieures, Patroni tentera de se connecter avec les identifiants de réplication à la base de données « postgres ». Par conséquent, un tel accès doit être autorisé dans pg_hba.conf. La valeur par défaut est **false**.

  - **replica_method** : pour chaque méthode de création de réplique autre que basebackup, vous devez ajouter une section de configuration du même nom. Cette section doit au minimum inclure "command" avec le chemin complet vers le script réel à exécuter. D'autres paramètres de configuration seront transmis au script sous la forme « parameter=value ».

  - **pre_promote** : un script de fencing qui s'exécute lors d'un basculement, après l'acquisition du verrou leader mais avant la promotion de la réplique. Si le script se termine avec un code différent de zéro, Patroni ne promeut pas la réplique et supprime la clé leader du DCS.

  - **before_stop** : un script qui s'exécute immédiatement avant l'arrêt de postgres. Contrairement à un callback, ce script s'exécute de manière synchrone, bloquant l'arrêt jusqu'à son achèvement. Le code de retour de ce script n'a pas d'incidence sur la poursuite de l'arrêt.

<a id="restapi_settings"></a>

--------

## REST API {#rest-api}

- **restapi** :
  - **thread_pool_size** : taille du pool de threads utilisé par Patroni pour traiter les requêtes de l'API REST. La valeur minimale est `5`, la valeur par défaut est `5`.
  - **connect_address** : adresse IP (ou nom d'hôte) et port permettant d'accéder à l'[API REST de Patroni](/fr/patroni/rest_api#rest_api). Tous les membres du cluster doivent pouvoir joindre cette adresse. Sauf pour une démonstration locale, utilisez une adresse réseau plutôt que « localhost » ou une adresse de boucle locale telle que "127.0.0.1". Elle peut servir d'endpoint pour les vérifications de santé HTTP (voir ci-dessous la configuration du paramètre REST « listen »), ainsi que pour les requêtes utilisateur (directement ou via l'API REST), et pour les vérifications de santé effectuées par les membres du cluster lors des élections du leader (par exemple, pour déterminer si le leader est toujours en cours d'exécution, ou si un nœud possède une position WAL supérieure à celle de l'entité effectuant la requête, etc.). L'adresse connect_address est inscrite dans la clé du membre dans le DCS, ce qui permet de traduire le nom du membre en adresse pour se connecter à son API REST.
  - **listen** : adresse IP (ou nom d'hôte) et port auxquels Patroni écoute pour l'API REST – afin de fournir également les contrôles de santé et la messagerie entre les nœuds participants, comme décrit ci-dessus. Permet de fournir des informations de contrôle de santé à HAProxy (ou tout autre équilibreur de charge capable d'effectuer des vérifications HTTP « OPTIONS » ou « GET »).
  - **authentication** : (facultatif)
    - **username** : nom d'utilisateur pour l'authentification basique protégeant les points d'accès de l'API REST sensibles.
    - **password** : mot de passe d'authentification basique pour protéger les points d'entrée de l'API REST sensibles.
  - **certfile** : (facultatif) : spécifie le fichier contenant le certificat au format PEM. Si le fichier de certificat n'est pas spécifié ou est vide, le serveur API fonctionnera sans SSL.
  - **keyfile** : (facultatif) : spécifie le fichier contenant la clé secrète au format PEM.
  - **keyfile_password** : (facultatif) : spécifie le mot de passe permettant de déchiffrer le fichier de clé.
  - **cafile** : (facultatif) : Spécifie le fichier contenant le CA_BUNDLE avec les certificats des autorités de certification (CA) de confiance à utiliser lors de la vérification des certificats clients.
  - **ciphers** : (facultatif) : Spécifie les suites de chiffrement autorisées (par exemple « ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-SHA256:!SSLv1:!SSLv2:!SSLv3:!TLSv1:!TLSv1.1 »)
  - **verify_client**: (facultatif) : `none` (par défaut), `optional` ou `required`. Lorsque `none` est utilisé, l'API REST ne vérifiera pas les certificats clients. Lorsque `required` est utilisé, les certificats clients sont requis pour tous les appels à l'API REST. Lorsque `optional` est utilisé, les certificats clients sont requis pour tous les points de terminaison REST sensibles. Lorsque `required` est utilisé, l'authentification du client réussit si la vérification de la signature du certificat réussit. Pour `optional`, le certificat client n'est vérifié que pour les requêtes `PUT`, `POST`, `PATCH` et `DELETE`.
  - **allowlist** : (facultatif) : spécifie l'ensemble des hôtes autorisés à appeler les points de terminaison d'API REST sensibles. Chaque élément peut être un nom d'hôte, une adresse IP ou une adresse réseau au format CIDR. Par défaut, `allow all` est utilisé. Si `allowlist` ou `allowlist_include_members` sont définis, tout ce qui n'est pas inclus est rejeté.
  - **allowlist_include_members** : (facultatif) : si défini à `true`, autorise l'accès à des points de terminaison d'API REST sensibles depuis d'autres membres du cluster inscrits dans le DCS (l'adresse IP ou le nom d'hôte est extrait des membres `api_url`). Prenez garde, il se peut que le système d'exploitation utilise une adresse IP différente pour les connexions sortantes.
  - **http_extra_headers** : (facultatif) : les en-têtes HTTP permettent au serveur d'API REST de transmettre des informations supplémentaires dans une réponse HTTP.
  - **https_extra_headers** : (facultatif) : Les en-têtes HTTPS permettent au serveur de l'API REST de transmettre des informations supplémentaires dans une réponse HTTP lorsque TLS est activé. Cela transmet également les informations supplémentaires définies dans `http_extra_headers`.
  - **request_queue_size** : (facultatif) : Définit la taille de la file d'attente des requêtes pour la socket TCP utilisée par l'API REST de Patroni. Une fois la file pleine, les requêtes supplémentaires reçoivent une erreur « Connection denied ». La valeur par défaut est 5.
  - **server_tokens**: (facultatif) : Configure la valeur de l'en-tête `Server` HTTP.
    - `Minimal` : L'en-tête ne contiendra que la version de Patroni, par exemple `Patroni/4.0.0`.
    - `ProductOnly` : L'en-tête ne contiendra que le nom du produit, par exemple `Patroni`.
    - `Original` (par défaut) : L'en-tête affichera le comportement d'origine et indiquera les versions de BaseHTTP et de Python, par exemple `BaseHTTP/0.6 Python/3.12.3`.

Voici un exemple des paramètres **http_extra_headers** et **https_extra_headers** :

```yaml
restapi:
  listen: <listen>
  connect_address: <connect_address>
  authentication:
    username: <username>
    password: <password>
  http_extra_headers:
    'X-Frame-Options': 'SAMEORIGIN'
    'X-XSS-Protection': '1; mode=block'
    'X-Content-Type-Options': 'nosniff'
  cafile: <ca file>
  certfile: <cert>
  keyfile: <key>
  https_extra_headers:
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
```

<div class="warning">

<div class="title">

Avertissement

</div>

-  Le `restapi.connect_address` doit être accessible depuis tous les nœuds d'un cluster Patroni donné. Internement, Patroni l'utilise pendant la course au leader pour identifier les nœuds présentant un retard de réplication minimal.
-  Si vous avez activé la validation des certificats clients (`restapi.verify_client` est défini sur `required`), vous devez également fournir des **certificats clients valides** dans les `ctl.certfile`, `ctl.keyfile`, `ctl.keyfile_password`. En l'absence de ces certificats, Patroni ne fonctionnera pas correctement.

</div>

<a id="patronictl_settings"></a>

--------

## CTL {#ctl}

- **ctl** : (facultatif)
  - **authentication** :
    - **username** : Nom d'utilisateur pour l'authentification basique afin d'accéder aux points de terminaison API REST protégés. Si non fourni, [patronictl](/fr/patroni/patronictl#patronictl) utilisera la valeur fournie pour le paramètre "username" de l'API REST.
    - **password** : Mot de passe pour l'authentification basique afin d'accéder aux points de terminaison API REST protégés. Si non fourni, [patronictl](/fr/patroni/patronictl#patronictl) utilisera la valeur fournie pour le paramètre "password" de l'API REST.
  - **insecure** : autorise les connexions à l'API REST sans vérification des certificats SSL.
  - **cacert** : spécifie le fichier contenant le CA_BUNDLE ou le répertoire contenant les certificats des autorités de certification de confiance à utiliser lors de la vérification des certificats SSL de l'API REST. Si ce paramètre n'est pas fourni, [patronictl](/fr/patroni/patronictl#patronictl) utilisera la valeur fournie pour le paramètre "cafile" de l'API REST.
  - **certfile** : spécifie le fichier contenant le certificat client au format PEM.
  - **keyfile** : Spécifie le fichier contenant la clé secrète client au format PEM.
  - **keyfile_password** : Spécifie un mot de passe pour déchiffrer le fichier de clé client.

--------

## Watchdog {#watchdog}

- **mode** : `off`, `automatic` ou `required`. Avec `off`, le watchdog est désactivé. Avec `automatic`, il est utilisé s'il est disponible et ignoré sinon. Avec `required`, le nœud ne devient leader que si le watchdog peut être activé avec succès.
- **device** : chemin du périphérique watchdog. Valeur par défaut : `/dev/watchdog`.
- **safety_margin** : marge de sécurité, en secondes, entre le déclenchement du watchdog et l'expiration de la clé de leader.

<a id="tags_settings"></a>

--------

## Balises {#tags}

- **clonefrom** : `true` ou `false`. Si cette option est définie à `true`, d'autres nœuds pourraient privilégier ce nœud pour l'amorçage (prendre `pg_basebackup` à partir de). Si plusieurs nœuds ont l'étiquette `clonefrom` définie à `true`, le nœud à partir duquel amorcer sera choisi aléatoirement. La valeur par défaut est `false`.
- **noloadbalance** : `true` ou `false`. Si cette option est définie à `true`, le nœud renvoie le code d’état HTTP 503 pour la vérification de santé de l’API REST `GET /replica` et est donc exclu de la répartition de charge. Valeur par défaut : `false`.
- **replicatefrom** : Le nom d’une autre réplique à partir de laquelle effectuer la réplication. Utilisé pour prendre en charge la réplication en cascade.
- **nosync** : `true` ou `false`. Si cette option est définie à `true`, le nœud ne sera jamais sélectionné comme réplique synchrone.
- **sync_priority** : entier, détermine la priorité que ce nœud doit avoir lors de la sélection de la réplique synchrone lorsque [synchronous_mode](/fr/patroni/replication_modes#synchronous_mode) est défini sur `on`. Les nœuds ayant une priorité plus élevée sont privilégiés par rapport à ceux ayant une priorité plus faible. Si la valeur de `sync_priority` est 0 ou négative, ce nœud ne peut pas être écrit dans `synchronous_standby_names` PostgreSQL (similaire à `nosync: true`). Notez que ce paramètre a une signification opposée à la valeur `sync_priority` rapportée par la vue `pg_stat_replication`.
- **nofailover** : `true` ou `false`, contrôle si ce nœud est autorisé à participer à la course au rôle de leader et à devenir leader. La valeur par défaut est `false`, ce qui signifie que ce nœud <span id="can">peut</span>\_ participer aux courses au rôle de leader.
- **failover_priority** : entier, contrôle la priorité que ce nœud doit avoir lors d’un basculement. Les nœuds ayant une priorité plus élevée sont préférés aux nœuds à priorité plus faible si ceux-ci ont reçu/rejoué la même quantité de WAL. Toutefois, les nœuds ayant une valeur de LSN de réception/rejeu plus élevée sont préférés, quelle que soit leur priorité. Si `failover_priority` est égal à 0 ou négatif, ce nœud n’est pas autorisé à participer à la course au rôle de leader ni à devenir leader (similaire à `nofailover: true`). Limitation connue : `failover_priority` ne fonctionne actuellement pas avec [réplication synchrone basée sur le quorum](/fr/patroni/replication_modes#quorum_mode).
- **nostream** : `true` ou `false`. Si cette option est définie à `true`, le nœud n'utilisera pas le protocole de réplication pour diffuser les WAL. Il s'appuiera alors sur la récupération depuis les archives (si `restore_command` est configuré) ainsi que sur les sondages `pg_wal`/`pg_xlog`. Cette configuration désactive également la copie et la synchronisation des slots de réplication logique permanents sur le nœud lui-même et sur toutes ses répliques en cascade. Définir cette option sur un nœud primaire n'a aucun effet.

> [!WARNING]
> Renseignez uniquement `nofailover` ou `failover_priority`. `nofailover: true` équivaut à `failover_priority: 0`, tandis que `nofailover: false` attribue au nœud la priorité 1.

En plus de ces balises prédéfinies, vous pouvez également ajouter les vôtres :

- **key1** : `true`
- **key2** : `false`
- **key3** : `1.4`
- **key4** : `"RandomString"`

Les balises sont visibles dans l'API [REST](/fr/patroni/rest_api#rest_api) et dans la commande [patronictl_list](/fr/patroni/patronictl#patronictl_list). Vous pouvez également vérifier l'état d'intégrité d'une instance à l'aide de ces balises. Si la balise n'est pas définie pour une instance, ou si sa valeur respective ne correspond pas à la valeur demandée, le code de statut HTTP renvoyé sera 503.
