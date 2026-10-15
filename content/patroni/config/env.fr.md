---
title: "Paramètres de configuration de l'environnement"
linkTitle: "Configuration de l'environnement"
weight: 30
icon: fa-solid fa-sliders
description: "Variables d'environnement pour remplacer les paramètres de configuration de Patroni."
module: [PATRONI]
categories: [Référence]
upstream_link: "https://patroni.readthedocs.io/en/latest/ENVIRONMENT.html"
---

<a id="env"></a>
Il est possible de remplacer certains paramètres de configuration définis dans le fichier de configuration Patroni à l’aide des variables d’environnement système. Ce document liste toutes les variables d’environnement prises en charge par Patroni. Les valeurs définies via ces variables ont toujours priorité sur celles définies dans le fichier de configuration Patroni.

--------

## Global/Universel {#globaluniversal}

- **PATRONI_CONFIGURATION** : il est possible de définir toute la configuration de Patroni via la variable d'environnement [PATRONI_CONFIGURATION](/fr/patroni/config#config). Dans ce cas, aucune autre variable d'environnement ne sera prise en compte !
- **PATRONI_THREAD_POOL_SIZE** : taille du pool de threads utilisé par Patroni pour exécuter les tâches asynchrones et communiquer via l'API REST avec les autres membres lors d'une course au leader ou lors des vérifications du mode failsafe. La valeur minimale est `5`, la valeur par défaut est `5`.
- **PATRONI_THREAD_STACK_SIZE** : spécifie la taille de pile à utiliser pour les threads lancés par Patroni. La valeur doit être alignée sur `64kB`. La valeur minimale est `64kB`, la valeur par défaut (définie par Patroni) est `512kB`.
- **PATRONI_NAME** : nom du nœud sur lequel l'instance actuelle de Patroni est en cours d'exécution. Doit être unique dans le cluster.
- **PATRONI_NAMESPACE** : chemin dans le magasin de configuration où Patroni conservera les informations sur le cluster. Valeur par défaut : "/service"
- **PATRONI_SCOPE** : nom du cluster
- **PG_MALLOC_ARENA_MAX** : valeur personnalisée pour la variable d'environnement `MALLOC_ARENA_MAX` du processus `postmaster`. Si non définie, `postmaster` héritera de la valeur de `MALLOC_ARENA_MAX`.

--------

## Journalisation {#log}

- **PATRONI_LOG_TYPE** : définit le format des journaux. Peut être soit **plain** soit **json**. Pour utiliser le format **json**, vous devez avoir installé [jsonlogger](/fr/patroni/installation#extras). La valeur par défaut est **plain**.
- **PATRONI_LOG_LEVEL** : définit le niveau général de journalisation. La valeur par défaut est **INFO** (voir [la documentation sur le module logging de Python](https://docs.python.org/3.6/library/logging.html#levels))
- **PATRONI_LOG_TRACEBACK_LEVEL** : définit le niveau auquel les traces d'erreur seront visibles. La valeur par défaut est **ERROR**. Définissez-la sur **DEBUG** si vous souhaitez voir les traces d'erreur uniquement lorsque **PATRONI_LOG_LEVEL=DEBUG** est activé.
- **PATRONI_LOG_FORMAT** : définit la chaîne de formatage des journaux. Si le type de journal est **plain**, le format devrait être une chaîne. Reportez-vous aux [attributs LogRecord](https://docs.python.org/3.6/library/logging.html#logrecord-attributes) pour obtenir la liste des attributs disponibles. Si le type de journal est **json**, le format peut être une liste en plus d'une chaîne. Chaque élément de la liste devrait correspondre à un attribut LogRecord. Prenez garde à ce que seul le nom du champ est requis, et que les **%(** et **)** doivent être omis. Si vous souhaitez afficher un champ de journal avec un nom de clé différent, utilisez un dictionnaire où la clé du dictionnaire est le champ de journal, et la valeur est le nom du champ que vous souhaitez afficher dans le journal. Valeur par défaut : **%(asctime)s %(levelname)s: %(message)s**
- **PATRONI_LOG_DATEFORMAT** : définit la chaîne de formatage de la date et de l'heure. (voir la documentation de [formatTime()](https://docs.python.org/3.6/library/logging.html#logging.Formatter.formatTime))
- **PATRONI_LOG_STATIC_FIELDS** : ajoute des champs supplémentaires au journal. Cette option n'est disponible que lorsque le type de journal est défini sur **json**. Exemple `PATRONI_LOG_STATIC_FIELDS="{app: patroni}"`
- **PATRONI_LOG_MAX_QUEUE_SIZE** : Patroni utilise une journalisation en deux étapes. Les enregistrements de journal sont écrits dans une file mémoire et un thread distinct extrait ces enregistrements de la file pour les écrire sur stderr ou dans un fichier. La taille maximale de la file interne est limitée par défaut à **1000** enregistrements, ce qui suffit à conserver les journaux des dernières 1h20.
- **PATRONI_LOG_DIR** : Répertoire dans lequel écrire les journaux d'application. Le répertoire doit exister et être accessible en écriture par l'utilisateur exécutant Patroni. Si vous définissez cette variable d'environnement, l'application conservera par défaut 4 fichiers de journaux de 25 Mo chacun. Vous pouvez ajuster ces valeurs de rétention à l'aide de `PATRONI_LOG_FILE_NUM` et `PATRONI_LOG_FILE_SIZE` (voir ci-dessous).
- **PATRONI_LOG_MODE** : Permissions des fichiers de journal (par exemple, `0644`). Si non spécifié, les permissions seront déterminées en fonction de la valeur actuelle de umask.
- **PATRONI_LOG_FILE_NUM** : Nombre de journaux d'application à conserver.
- **PATRONI_LOG_FILE_SIZE** : Taille du fichier patroni.log (en octets) qui déclenche un roulement du journal.
- **PATRONI_LOG_LOGGERS** : Redéfinir le niveau de journalisation par module Python. Exemple `PATRONI_LOG_LOGGERS="{patroni.postmaster: WARNING, urllib3: DEBUG}"`.
- **PATRONI_LOG_DEDUPLICATE_HEARTBEAT_LOGS** : Si défini à `true`, les journaux de battement de cœur identiques successifs ne seront pas affichés. La valeur par défaut est `false`.

> [!WARNING]
> Le moment auquel la boucle HA s'exécute peut constituer une information très utile pour diagnostiquer les basculements dus à l'épuisement des ressources et à des problèmes similaires. Lorsque `PATRONI_LOG_DEDUPLICATE_HEARTBEAT_LOGS` est défini sur `true`, aucun journal n'est généré pour l'exécution de la boucle HA (sauf en cas de changement de leader), ce qui fait que cette information potentiellement utile ne sera pas disponible dans les journaux.

--------

## Citus {#citus}

Active l'intégration de Patroni avec [Citus](https://docs.citusdata.com). Si elle est configurée, Patroni s'occupe de l'enregistrement des nœuds workers Citus sur le coordinateur. Vous trouverez plus d'informations sur le support Citus [ici](/fr/patroni/citus#citus).

- **PATRONI_CITUS_GROUP** : l'identifiant du groupe Citus, entier. Utilisez `0` pour le coordinateur et `1`, `2`, etc. pour les workers
- **PATRONI_CITUS_DATABASE** : la base de données où l'extension [citus](/fr/patroni/citus#citus) doit être créée. Doit être identique sur le coordinateur et tous les workers. Actuellement, une seule base de données est prise en charge.

--------

## Consul {#consul}

- **PATRONI_CONSUL_HOST** : l'hôte:port de l'agent local Consul.
- **PATRONI_CONSUL_URL** : URL de l'agent local Consul, au format : http(s)://host:port
- **PATRONI_CONSUL_PORT** : (facultatif) port Consul
- **PATRONI_CONSUL_SCHEME** : (facultatif) **http** ou **https**, par défaut **http**
- **PATRONI_CONSUL_TOKEN** : (facultatif) jeton ACL
- **PATRONI_CONSUL_VERIFY** : (facultatif) indique si la vérification du certificat SSL est activée pour les requêtes HTTPS
- **PATRONI_CONSUL_CACERT** : (facultatif) Certificat CA. S'il est présent, la validation est activée.
- **PATRONI_CONSUL_CERT** : (facultatif) Fichier contenant le certificat client
- **PATRONI_CONSUL_KEY** : (facultatif) Fichier contenant la clé client. Peut être vide si la clé est incluse dans le certificat.
- **PATRONI_CONSUL_DC** : (facultatif) Centre de données avec lequel établir la communication. Par défaut, le centre de données de l'hôte est utilisé.
- **PATRONI_CONSUL_CONSISTENCY** : (facultatif) Sélectionne le mode de cohérence Consul. Les valeurs possibles sont `default`, `consistent`, ou `stale` (plus de détails dans la [référence de l'API Consul](https://www.consul.io/api/features/consistency.html/))
- **PATRONI_CONSUL_CHECKS** : (facultatif) liste des vérifications de santé Consul utilisées pour la session. Par défaut, une liste vide est utilisée.
- **PATRONI_CONSUL_REGISTER_SERVICE** : (facultatif) indique si un service doit être enregistré avec le nom défini par le paramètre scope et l'étiquette master, primary, replica ou standby-leader selon le rôle du nœud. Valeur par défaut : **false**
- **PATRONI_CONSUL_SERVICE_TAGS** : (facultatif) étiquettes statiques supplémentaires à ajouter au service Consul, en plus du rôle (`primary`/`replica`/`standby-leader`). Par défaut, une liste vide est utilisée.
- **PATRONI_CONSUL_SERVICE_CHECK_INTERVAL** : (facultatif) fréquence à laquelle effectuer la vérification de santé sur l'URL enregistrée
- **PATRONI_CONSUL_SERVICE_CHECK_TLS_SERVER_NAME** : (facultatif) remplacer l'hôte SNI lors de la connexion via TLS, voir également [référence de l'API de vérification de l'agent consul](https://www.consul.io/api-docs/agent/check#tlsservername).

--------

## etcd {#etcd}

- **PATRONI_ETCD_PROXY** : URL du proxy pour etcd. Si vous vous connectez à etcd via un proxy, utilisez ce paramètre à la place de **PATRONI_ETCD_URL**
- **PATRONI_ETCD_URL** : URL d'accès à etcd, au format : http(s)://(username:password@)host:port
- **PATRONI_ETCD_HOSTS** : liste des points de terminaison etcd au format 'host1:port1','host2:port2', etc...
- **PATRONI_ETCD_USE_PROXIES** : Si ce paramètre est défini sur true, Patroni considérera **hosts** comme une liste de proxys et n'effectuera pas de découverte de topologie du cluster etcd, mais s'en tiendra à la liste fixe de **hosts**.
- **PATRONI_ETCD_PROTOCOL** : http ou https, si non spécifié, http est utilisé. Si **url** ou **proxy** est spécifié, le protocole sera déduit de ces valeurs.
- **PATRONI_ETCD_HOST** : l'hôte:port du point de terminaison etcd.
- **PATRONI_ETCD_SRV** : Domaine dans lequel rechercher les enregistrements SRV pour la découverte automatique du cluster. Patroni tentera de consulter ces noms de service SRV pour le domaine spécifié (dans cet ordre, jusqu'à la première réussite) : `_etcd-client-ssl`, `_etcd-client`, `_etcd-ssl`, `_etcd`, `_etcd-server-ssl`, `_etcd-server`. Si des enregistrements SRV pour `_etcd-server-ssl` ou `_etcd-server` sont récupérés, le protocole pair ETCD sera utilisé pour interroger ETCD afin d'obtenir la liste des membres disponibles. Sinon, les hôtes provenant des enregistrements SRV seront utilisés.
- **PATRONI_ETCD_SRV_SUFFIX** : Configure un suffixe au nom SRV interrogé lors de la découverte. Utilisez cette option pour distinguer plusieurs clusters etcd sous le même domaine. Fonctionne uniquement en conjonction avec **PATRONI_ETCD_SRV**. Par exemple, si `PATRONI_ETCD_SRV_SUFFIX=foo` et `PATRONI_ETCD_SRV=example.org` sont définis, la requête DNS SRV suivante est effectuée : `_etcd-client-ssl-foo._tcp.example.org` (et ainsi de suite pour chaque nom de service SRV etcd possible).
- **PATRONI_ETCD_USERNAME** : nom d'utilisateur pour l'authentification etcd.
- **PATRONI_ETCD_PASSWORD** : mot de passe pour l'authentification etcd.
- **PATRONI_ETCD_CACERT** : certificat CA. S'il est présent, il active la validation.
- **PATRONI_ETCD_CERT** : fichier contenant le certificat client.
- **PATRONI_ETCD_KEY** : fichier contenant la clé client. Peut être vide si la clé est incluse dans le certificat.

--------

## Etcdv3 {#etcdv3}

Les noms d'environnement pour Etcdv3 sont similaires à ceux d'etcd ; il suffit de remplacer `ETCD` par `ETCD3` dans le nom de la variable. Exemple : `PATRONI_ETCD3_HOST`, `PATRONI_ETCD3_CACERT`, et ainsi de suite.

> [!WARNING]
> Les clés créées avec la version 2 du protocole ne sont pas visibles avec la version 3 du protocole, et inversement ; il n'est donc pas possible de passer d'etcd à Etcdv3 en ne mettant à jour que la configuration de Patroni. En outre, Patroni utilise la passerelle gRPC (proxy) d'Etcd pour communiquer avec l'API V3, ce qui empêche l'authentification par nom commun TLS.

--------

## ZooKeeper {#zookeeper}

- **PATRONI_ZOOKEEPER_HOSTS** : Liste séparée par des virgules des membres du cluster ZooKeeper : "'host1:port1','host2:port2','etc...'". Il est important de mettre chaque élément entre guillemets !
- **PATRONI_ZOOKEEPER_USE_SSL** : (facultatif) Indique si le protocole SSL est utilisé. Valeur par défaut : `false`. Si défini à `false`, tous les paramètres spécifiques au SSL sont ignorés.
- **PATRONI_ZOOKEEPER_CACERT** : (facultatif) Certificat CA. Si présent, active la validation.
- **PATRONI_ZOOKEEPER_CERT** : (facultatif) Fichier contenant le certificat client.
- **PATRONI_ZOOKEEPER_KEY** : (facultatif) Fichier contenant la clé client.
- **PATRONI_ZOOKEEPER_KEY_PASSWORD** : (facultatif) Mot de passe de la clé client.
- **PATRONI_ZOOKEEPER_VERIFY** : (facultatif) Indique si la vérification du certificat doit être effectuée ou non. Valeur par défaut : `true`.
- **PATRONI_ZOOKEEPER_SET_ACLS** : (facultatif) Si défini, configure Kazoo pour appliquer une ACL par défaut à chaque ZNode qu'il crée. Les ACL peuvent utiliser le schéma `x509` (par défaut) ou d'autres schémas pris en charge par ZooKeeper, tels que `digest`. Elles doivent être spécifiées sous forme de dictionnaire, où la clé est le principal complet (éventuellement préfixé par le schéma) et la valeur une liste de permissions. Les permissions peuvent être une ou plusieurs des valeurs suivantes : `CREATE`, `READ`, `WRITE`, `DELETE`, `ADMIN`, ou `ALL`. Par exemple, `set_acls: {CN=principal1: [CREATE, READ], digest:principal2:+pjROuBuuwNNSujKyH8dGcEnFPQ=: [ALL]}`.
- **PATRONI_ZOOKEEPER_AUTH_DATA** : (facultatif) Informations d'authentification à utiliser pour la connexion. Doit être un dictionnaire dont `scheme` est la clé et `credential` la valeur. Valeur par défaut : dictionnaire vide.

> [!NOTE]
> Il est obligatoire d'installer `kazoo>=2.6.0` pour prendre en charge le SSL.

--------

## Exhibitor {#exhibitor}

- **PATRONI_EXHIBITOR_HOSTS** : liste initiale des nœuds Exhibitor (ZooKeeper) au format : 'host1,host2,etc...'. Cette liste est mise à jour automatiquement chaque fois que la topologie du cluster Exhibitor (ZooKeeper) change.
- **PATRONI_EXHIBITOR_PORT** : port Exhibitor.

<a id="kubernetes_environment"></a>

--------

## Kubernetes {#kubernetes}

- **PATRONI_KUBERNETES_BYPASS_API_SERVICE** : (facultatif) Lors de la communication avec l'API Kubernetes, Patroni utilise généralement le service [kubernetes](/fr/patroni/kubernetes#kubernetes), dont l'adresse est exposée dans les pods via la variable d'environnement `KUBERNETES_SERVICE_HOST`. Si `PATRONI_KUBERNETES_BYPASS_API_SERVICE` est défini sur `true`, Patroni résoudra la liste des nœuds API derrière le service et s'y connectera directement.
- **PATRONI_KUBERNETES_NAMESPACE** : (facultatif) Espace de noms Kubernetes dans lequel s'exécute le pod Patroni. Valeur par défaut : `default`.
- **PATRONI_KUBERNETES_LABELS** : Étiquettes au format `{label1: value1, label2: value2}`. Ces étiquettes seront utilisées pour localiser les objets existants (Pods et soit des Endpoints, soit des ConfigMaps) associés au cluster actuel. Patroni les définira également sur chaque objet (Endpoint ou ConfigMap) qu'il crée.
- **PATRONI_KUBERNETES_SCOPE_LABEL** : (facultatif) nom de l'étiquette contenant le nom du cluster. La valeur par défaut est `cluster-name`.
- **PATRONI_KUBERNETES_BOOTSTRAP_LABELS** : (facultatif) Étiquettes au format `{label1: value1, label2: value2}`. Ces étiquettes seront attribuées au pod Patroni lorsque son état est l'un des suivants : `initializing new cluster`, `running custom bootstrap script`, `starting after custom bootstrap` ou `creating replica`.
- **PATRONI_KUBERNETES_ROLE_LABEL** : (facultatif) nom de l'étiquette contenant le rôle (`primary`, `replica` ou autre valeur personnalisée). Patroni définira cette étiquette sur le pod dans lequel il s'exécute. Valeur par défaut : `role`.
- **PATRONI_KUBERNETES_LEADER_LABEL_VALUE** : (facultatif) valeur de l'étiquette du pod lorsque le rôle PostgreSQL est `primary`. Valeur par défaut : `primary`.
- **PATRONI_KUBERNETES_FOLLOWER_LABEL_VALUE** : (facultatif) valeur de l'étiquette du pod lorsque le rôle PostgreSQL est `replica`. Valeur par défaut : `replica`.
- **PATRONI_KUBERNETES_STANDBY_LEADER_LABEL_VALUE** : (facultatif) valeur de l'étiquette du pod lorsque le rôle Postgres est `standby_leader`. Valeur par défaut : `primary`.
- **PATRONI_KUBERNETES_TMP_ROLE_LABEL** : (facultatif) nom de l'étiquette temporaire contenant le rôle (`primary` ou `replica`). La valeur de cette étiquette utilisera toujours la valeur par défaut correspondante au rôle. À définir uniquement si nécessaire.
- **PATRONI_KUBERNETES_USE_ENDPOINTS** : (facultatif) si défini à true, Patroni utilisera des Endpoints au lieu de ConfigMaps pour effectuer les élections du leader et maintenir l’état du cluster.
- **PATRONI_KUBERNETES_POD_IP** : (facultatif) adresse IP du pod dans lequel Patroni s’exécute. Cette valeur est requise lorsque `PATRONI_KUBERNETES_USE_ENDPOINTS` est activé et est utilisée pour remplir les sous-ensembles de l’endpoint leader lorsque le pod PostgreSQL est promu.
- **PATRONI_KUBERNETES_PORTS** : (facultatif) si l'objet Service possède un nom pour le port, ce même nom doit apparaître dans l'objet Endpoint, sinon le service ne fonctionnera pas. Par exemple, si votre service est défini comme `{Kind: Service, spec: {ports: [{name: postgresql, port: 5432, targetPort: 5432}]}}`, vous devez définir `PATRONI_KUBERNETES_PORTS='[{"name": "postgresql", "port": 5432}]'` et Patroni l'utilisera pour mettre à jour les sous-ensembles de l'Endpoint leader. Ce paramètre n'est utilisé que si `PATRONI_KUBERNETES_USE_ENDPOINTS` est défini.
- **PATRONI_KUBERNETES_CACERT** : (facultatif) indique le fichier CA_BUNDLE contenant les certificats des autorités de certification approuvées pour vérifier les certificats SSL de l'API Kubernetes. En l'absence de valeur, Patroni utilise celle du secret ServiceAccount.
- **PATRONI_RETRIABLE_HTTP_CODES** : (facultatif) liste des codes d'état HTTP de l'API K8s pour lesquels une nouvelle tentative doit être effectuée. Par défaut, Patroni réessaie pour `500`, `503` et `504`, ou lorsque la réponse de l'API K8s contient l'en-tête HTTP `retry-after`.

--------

## Raft (obsolète) {#raft-deprecated}

- **PATRONI_RAFT_SELF_ADDR** : `ip:port` sur lequel écouter pour les connexions Raft. L'`self_addr` doit être accessible depuis les autres nœuds du cluster. Si non définie, le nœud ne participera pas au consensus.
- **PATRONI_RAFT_BIND_ADDR** : (facultatif) `ip:port` sur lequel écouter pour les connexions Raft. Si non spécifié, l'`self_addr` sera utilisé.
- **PATRONI_RAFT_PARTNER_ADDRS** : liste des autres nœuds Patroni du cluster au format `"'ip1:port1','ip2:port2'"`. Il est important de mettre chaque élément entre guillemets !
- **PATRONI_RAFT_DATA_DIR** : répertoire dans lequel stocker les journaux Raft et les instantanés. Si non spécifié, le répertoire de travail actuel est utilisé.
- **PATRONI_RAFT_PASSWORD** : (facultatif) Chiffrer le trafic Raft avec un mot de passe spécifié, nécessite le module `cryptography` Python.
- **PATRONI_RAFT_MIN_TIMEOUT** : (facultatif) délai minimum d'élection en secondes pour l'implémentation Raft pysyncobj sous-jacente. Doit être supérieur à 3 × `PATRONI_RAFT_APPEND_ENTRIES_PERIOD`. Valeur par défaut : `0.4`.
- **PATRONI_RAFT_MAX_TIMEOUT** : (facultatif) délai maximal d'élection en secondes pour l'implémentation Raft pysyncobj sous-jacente. Doit être supérieur à `PATRONI_RAFT_MIN_TIMEOUT`. Valeur par défaut : `1.4`.
- **PATRONI_RAFT_CONNECTION_TIMEOUT** : (facultatif) délai en secondes après lequel une connexion sans données reçues est considérée comme morte. Doit être supérieur ou égal à `PATRONI_RAFT_MAX_TIMEOUT`. Valeur par défaut : `3.5`.
- **PATRONI_RAFT_APPEND_ENTRIES_PERIOD** : (facultatif) intervalle en secondes pour l'envoi des commandes de battement de cœur. Doit être inférieur à un tiers de `PATRONI_RAFT_MIN_TIMEOUT`. Valeur par défaut : `0.1`.
- **PATRONI_RAFT_CONNECTION_RETRY_TIME** : (facultatif) intervalle en secondes entre les tentatives de reconnexion aux nœuds hors ligne. Valeur par défaut : `5.0`.
- **PATRONI_RAFT_LEADER_FALLBACK_TIMEOUT** : (facultatif) durée en secondes après laquelle un leader ne recevant aucune réponse de la majorité redevient un suiveur. Doit être supérieur à `PATRONI_RAFT_APPEND_ENTRIES_PERIOD`. Valeur par défaut : `30.0`.

> [!NOTE]
> Patroni vérifie ces contraintes au démarrage et refusera de démarrer si elles sont violées. Ces valeurs ne peuvent pas être modifiées en cours d'exécution et nécessitent un redémarrage. Pour plus de détails, y compris la limitation liée aux latences élevées, consultez [Paramètres Raft](/fr/patroni/config/yaml#raft_settings).

--------

## PostgreSQL {#postgresql}

- **PATRONI_POSTGRESQL_LISTEN** : adresse IP + port auxquels Postgres écoute. Plusieurs adresses séparées par des virgules sont autorisées, à condition que le composant port soit ajouté après la dernière adresse, séparé par deux-points, c’est-à-dire `listen: 127.0.0.1,127.0.0.2:5432`. Patroni utilisera la première adresse de cette liste pour établir des connexions locales vers le nœud PostgreSQL.
- **PATRONI_POSTGRESQL_CONNECT_ADDRESS** : adresse IP + port par lequel Postgres est accessible depuis d'autres nœuds et applications.
- **PATRONI_POSTGRESQL_PROXY_ADDRESS** : adresse IP + port par lequel un pool de connexions (par exemple pgbouncer) en cours d'exécution à côté de Postgres est accessible. La valeur est écrite dans la clé member du DCS sous la forme `proxy_url` et peut être utilisée/utile pour la découverte de services.
- **PATRONI_POSTGRESQL_DATA_DIR** : emplacement du répertoire de données Postgres, existant ou à initialiser par Patroni.
- **PATRONI_POSTGRESQL_CONFIG_DIR** : Emplacement du répertoire de configuration de Postgres, par défaut le répertoire de données. Doit être accessible en écriture par Patroni.
- **PATRONI_POSTGRESQL_BIN_DIR** : Chemin vers les binaires de PostgreSQL (pg_ctl, initdb, pg_controldata, pg_basebackup, postgres, pg_isready, pg_rewind). La valeur par défaut est une chaîne vide, ce qui signifie que les exécutables seront recherchés dans la variable d'environnement PATH.
- **PATRONI_POSTGRESQL_BIN_PG_CTL** : (facultatif) Nom personnalisé pour le binaire `pg_ctl`.
- **PATRONI_POSTGRESQL_BIN_INITDB** : (facultatif) Nom personnalisé pour le binaire `initdb`.
- **PATRONI_POSTGRESQL_BIN_PG_CONTROLDATA** : (facultatif) Nom personnalisé pour le binaire `pg_controldata`.
- **PATRONI_POSTGRESQL_BIN_PG_BASEBACKUP** : (facultatif) Nom personnalisé pour le binaire `pg_basebackup`.
- **PATRONI_POSTGRESQL_BIN_POSTGRES** : (facultatif) Nom personnalisé pour le binaire `postgres`.
- **PATRONI_POSTGRESQL_BIN_IS_READY** : (facultatif) Nom personnalisé pour le binaire `pg_isready`.
- **PATRONI_POSTGRESQL_BIN_PG_REWIND** : (facultatif) Nom personnalisé pour le binaire `pg_rewind`.
- **PATRONI_POSTGRESQL_PGPASS** : chemin vers le fichier de mot de passe [.pgpass](https://www.postgresql.org/docs/current/static/libpq-pgpass.html). Patroni crée ce fichier avant d'exécuter pg_basebackup et dans certaines autres circonstances. L'emplacement doit être accessible en écriture par Patroni.
- **PATRONI_REPLICATION_USERNAME** : nom d'utilisateur de réplication ; l'utilisateur sera créé lors de l'initialisation. Les répliques utiliseront cet utilisateur pour accéder à la source de réplication via la réplication en flux
- **PATRONI_REPLICATION_PASSWORD** : mot de passe de réplication ; l'utilisateur sera créé lors de l'initialisation.
- **PATRONI_REPLICATION_SSLMODE** : (facultatif) correspond au paramètre de connexion [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE), qui permet à un client de spécifier le mode de négociation TLS avec le serveur. Pour plus d'informations sur le fonctionnement de chaque mode, veuillez consulter la documentation [PostgreSQL](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). Le mode par défaut est `prefer`.
- **PATRONI_REPLICATION_SSLKEY** : (facultatif) correspond au paramètre de connexion [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY), qui précise l'emplacement de la clé secrète utilisée avec le certificat client.
- **PATRONI_REPLICATION_SSLPASSWORD** : (facultatif) correspond au paramètre de connexion [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD), qui précise le mot de passe de la clé secrète spécifiée dans `PATRONI_REPLICATION_SSLKEY`.
- **PATRONI_REPLICATION_SSLCERT** : (facultatif) correspond au paramètre de connexion [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT), qui précise l'emplacement du certificat client.
- **PATRONI_REPLICATION_SSLROOTCERT** : (facultatif) correspond au paramètre de connexion [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT), qui précise l'emplacement d'un fichier contenant un ou plusieurs certificats d'autorités de certification (CA) utilisés par le client pour vérifier le certificat d'un serveur.
- **PATRONI_REPLICATION_SSLCRL** : (facultatif) correspond au paramètre de connexion [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL), qui précise l'emplacement d'un fichier contenant une liste de révocation de certificats. Un client refusera la connexion à tout serveur dont le certificat figure dans cette liste.
- **PATRONI_REPLICATION_SSLCRLDIR** : (facultatif) correspond au paramètre de connexion [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR), qui précise l'emplacement d'un répertoire contenant des fichiers listant les certificats révoqués. Un client refusera de se connecter à tout serveur dont le certificat figure dans cette liste.
- **PATRONI_REPLICATION_SSLNEGOTIATION** : (facultatif) correspond au paramètre de connexion [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION), qui contrôle la négociation du chiffrement SSL avec le serveur, le cas échéant.
- **PATRONI_REPLICATION_GSSENCMODE** : (facultatif) correspond au paramètre de connexion [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE), qui détermine si une connexion TCP/IP sécurisée GSS sera négociée avec le serveur, et avec quelle priorité
- **PATRONI_REPLICATION_CHANNEL_BINDING** : (facultatif) correspond au paramètre de connexion [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING), qui contrôle l'utilisation de la liaison de canal par le client.
- **PATRONI_SUPERUSER_USERNAME** : nom de l'utilisateur superutilisateur, défini lors de l'initialisation (initdb) et utilisé ultérieurement par Patroni pour se connecter à PostgreSQL. Cet utilisateur est également utilisé par pg_rewind.
- **PATRONI_SUPERUSER_PASSWORD** : mot de passe pour l'utilisateur superutilisateur, défini lors de l'initialisation (initdb).
- **PATRONI_SUPERUSER_SSLMODE** : (facultatif) correspond au paramètre de connexion [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE), qui permet à un client de spécifier le mode de négociation TLS avec le serveur. Pour plus d'informations sur le fonctionnement de chaque mode, veuillez consulter la documentation [PostgreSQL](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). Le mode par défaut est `prefer`.
- **PATRONI_SUPERUSER_SSLKEY** : (facultatif) correspond au paramètre de connexion [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY), qui précise l'emplacement de la clé secrète utilisée avec le certificat client.
- **PATRONI_SUPERUSER_SSLPASSWORD** : (facultatif) correspond au paramètre de connexion [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD), qui précise le mot de passe de la clé secrète spécifiée dans `PATRONI_SUPERUSER_SSLKEY`.
- **PATRONI_SUPERUSER_SSLCERT** : (facultatif) correspond au paramètre de connexion [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT), qui précise l'emplacement du certificat client.
- **PATRONI_SUPERUSER_SSLROOTCERT** : (facultatif) correspond au paramètre de connexion [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT), qui précise l'emplacement d'un fichier contenant un ou plusieurs certificats d'autorités de certification (CA) utilisés par le client pour vérifier le certificat d'un serveur.
- **PATRONI_SUPERUSER_SSLCRL** : (facultatif) correspond au paramètre de connexion [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL), qui précise l'emplacement d'un fichier contenant une liste de révocation de certificats. Un client refusera la connexion à tout serveur dont le certificat figure dans cette liste.
- **PATRONI_SUPERUSER_SSLCRLDIR** : (facultatif) correspond au paramètre de connexion [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR), qui précise l'emplacement d'un répertoire contenant des fichiers listant les certificats révoqués. Un client refusera de se connecter à tout serveur dont le certificat figure dans cette liste.
- **PATRONI_SUPERUSER_SSLNEGOTIATION** : (facultatif) correspond au paramètre de connexion [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION), qui contrôle la négociation du chiffrement SSL avec le serveur, le cas échéant.
- **PATRONI_SUPERUSER_GSSENCMODE** : (facultatif) correspond au paramètre de connexion [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE), qui détermine si une connexion TCP/IP sécurisée GSS sera négociée avec le serveur, et avec quelle priorité
- **PATRONI_SUPERUSER_CHANNEL_BINDING** : (facultatif) correspond au paramètre de connexion [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING), qui contrôle l'utilisation de la liaison de canal par le client.
- **PATRONI_REWIND_USERNAME** : (facultatif) nom de l'utilisateur pour `pg_rewind` ; l'utilisateur sera créé lors de l'initialisation de PostgreSQL 11+ et toutes les autorisations [nécessaires](https://www.postgresql.org/docs/11/app-pgrewind.html#id-1.9.5.8.8) lui seront accordées.
- **PATRONI_REWIND_PASSWORD** : (facultatif) mot de passe de l'utilisateur pour `pg_rewind` ; l'utilisateur sera créé lors de l'initialisation.
- **PATRONI_REWIND_SSLMODE** : (facultatif) correspond au paramètre de connexion [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE), qui permet à un client de spécifier le mode de négociation TLS avec le serveur. Pour plus d'informations sur le fonctionnement de chaque mode, veuillez consulter la documentation [PostgreSQL](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). Le mode par défaut est `prefer`.
- **PATRONI_REWIND_SSLKEY** : (facultatif) correspond au paramètre de connexion [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY), qui précise l'emplacement de la clé secrète utilisée avec le certificat client.
- **PATRONI_REWIND_SSLPASSWORD** : (facultatif) correspond au paramètre de connexion [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD), qui précise le mot de passe de la clé secrète spécifiée dans `PATRONI_REWIND_SSLKEY`.
- **PATRONI_REWIND_SSLCERT** : (facultatif) correspond au paramètre de connexion [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT), qui précise l'emplacement du certificat client.
- **PATRONI_REWIND_SSLROOTCERT** : (facultatif) correspond au paramètre de connexion [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT), qui précise l'emplacement d'un fichier contenant un ou plusieurs certificats d'autorités de certification (CA) utilisés par le client pour vérifier le certificat d'un serveur.
- **PATRONI_REWIND_SSLCRL** : (facultatif) correspond au paramètre de connexion [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL), qui précise l'emplacement d'un fichier contenant une liste de révocation de certificats. Un client refusera de se connecter à tout serveur dont le certificat figure dans cette liste.
- **PATRONI_REWIND_SSLCRLDIR** : (facultatif) correspond au paramètre de connexion [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR), qui précise l'emplacement d'un répertoire contenant des fichiers listant les certificats révoqués. Un client refusera de se connecter à tout serveur dont le certificat figure dans cette liste.
- **PATRONI_REWIND_SSLNEGOTIATION** : (facultatif) correspond au paramètre de connexion [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION), qui contrôle la négociation du chiffrement SSL avec le serveur, le cas échéant.
- **PATRONI_REWIND_GSSENCMODE** : (facultatif) correspond au paramètre de connexion [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE), qui détermine si une connexion TCP/IP sécurisée GSS sera négociée avec le serveur, et avec quelle priorité
- **PATRONI_REWIND_CHANNEL_BINDING** : (facultatif) correspond au paramètre de connexion [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING), qui contrôle l'utilisation de la liaison de canal par le client.

--------

## REST API {#rest-api}

- **PATRONI_RESTAPI_THREAD_POOL_SIZE** : taille du pool de threads utilisé par Patroni pour traiter les requêtes de l'API REST. La valeur minimale est `5`, la valeur par défaut est `5`.
- **PATRONI_RESTAPI_CONNECT_ADDRESS** : adresse IP et port d'accès à l'API REST.
- **PATRONI_RESTAPI_LISTEN** : adresse IP et port auxquels Patroni écoute, afin de fournir des informations de vérification de santé pour HAProxy.
- **PATRONI_RESTAPI_USERNAME** : nom d'utilisateur pour l'authentification basique protégeant les points de terminaison de l'API REST sensibles.
- **PATRONI_RESTAPI_PASSWORD** : Mot de passe d'authentification basique pour protéger les points de terminaison API REST sensibles.
- **PATRONI_RESTAPI_CERTFILE** : Spécifie le fichier contenant le certificat au format PEM. Si le fichier de certificat n'est pas précisé ou est vide, le serveur API fonctionnera sans SSL.
- **PATRONI_RESTAPI_KEYFILE** : Spécifie le fichier contenant la clé secrète au format PEM.
- **PATRONI_RESTAPI_KEYFILE_PASSWORD** : Spécifie le mot de passe pour déchiffrer le fichier de clé.
- **PATRONI_RESTAPI_CAFILE** : indique le fichier CA_BUNDLE contenant les certificats des autorités de certification approuvées pour vérifier les certificats clients.
- **PATRONI_RESTAPI_CIPHERS** : (facultatif) indique les suites de chiffrement autorisées, par exemple "ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-SHA256:!SSLv1:!SSLv2:!SSLv3:!TLSv1:!TLSv1.1".
- **PATRONI_RESTAPI_VERIFY_CLIENT** : `none` (par défaut), `optional` ou `required`. Lorsque `none` est utilisé, l'API REST ne vérifiera pas les certificats clients. Lorsque `required` est utilisé, les certificats clients sont requis pour tous les appels à l'API REST. Lorsque `optional` est utilisé, les certificats clients sont requis pour tous les points de terminaison REST sensibles. Lorsque `required` est utilisé, l'authentification du client réussit si la vérification de la signature du certificat réussit. Pour `optional`, le certificat client n'est vérifié que pour les requêtes `PUT`, `POST`, `PATCH` et `DELETE`.
- **PATRONI_RESTAPI_ALLOWLIST** : (facultatif) : Spécifie l'ensemble des hôtes autorisés à appeler les points de terminaison d'API REST sensibles. Chaque élément peut être un nom d'hôte, une adresse IP ou une adresse réseau au format CIDR. Par défaut, `allow all` est utilisé. Si `allowlist` ou `allowlist_include_members` sont définis, tout ce qui n'est pas inclus est rejeté.
- **PATRONI_RESTAPI_ALLOWLIST_INCLUDE_MEMBERS** : (facultatif) Si défini à `true`, permet d'accéder à des points de terminaison d'API REST sensibles depuis d'autres membres du cluster inscrits dans le DCS (l'adresse IP ou le nom d'hôte est extrait des membres `api_url`). Prenez garde, il se peut que le système d'exploitation utilise une adresse IP différente pour les connexions sortantes.
- **PATRONI_RESTAPI_HTTP_EXTRA_HEADERS** : (facultatif) Les en-têtes HTTP permettent au serveur d'API REST de transmettre des informations supplémentaires dans une réponse HTTP.
- **PATRONI_RESTAPI_HTTPS_EXTRA_HEADERS** : (facultatif) Les en-têtes HTTPS permettent au serveur d'API REST de transmettre des informations supplémentaires dans une réponse HTTP lorsque TLS est activé. Cela transmet également les informations supplémentaires définies dans `http_extra_headers`.
- **PATRONI_RESTAPI_REQUEST_QUEUE_SIZE** : (facultatif) Définit la taille de la file d'attente des requêtes pour la socket TCP utilisée par l'API REST de Patroni. Dès que la file est pleine, les requêtes supplémentaires reçoivent une erreur « Connection denied ». La valeur par défaut est 5.
- **PATRONI_RESTAPI_SERVER_TOKENS** : (facultatif) Configure la valeur de l’en-tête HTTP `Server`. `Original` (par défaut) conserve le comportement original et affiche les versions de BaseHTTP et de Python, par exemple `BaseHTTP/0.6 Python/3.12.3`. `Minimal` : l’en-tête ne contiendra que la version de Patroni, par exemple `Patroni/4.0.0`. `ProductOnly` : l’en-tête ne contiendra que le nom du produit, par exemple `Patroni`.

<div class="warning">

<div class="title">

Avertissement

</div>

-  Le `PATRONI_RESTAPI_CONNECT_ADDRESS` doit être accessible depuis tous les nœuds d'un cluster Patroni donné. Internement, Patroni l'utilise lors de la course au leader pour identifier les nœuds présentant un retard de réplication minimal.
-  Si vous avez activé la validation des certificats client (`PATRONI_RESTAPI_VERIFY_CLIENT` est défini sur `required`), vous devez également fournir des **certificats clients valides** dans les `PATRONI_CTL_CERTFILE`, `PATRONI_CTL_KEYFILE`, `PATRONI_CTL_KEYFILE_PASSWORD`. En l'absence de ces certificats, Patroni ne fonctionnera pas correctement.

</div>

--------

## CTL {#ctl}

- **PATRONICTL_CONFIG_FILE** : (facultatif) emplacement du fichier de configuration.
- **PATRONI_CTL_USERNAME** : (facultatif) nom d'utilisateur pour l'authentification basique afin d'accéder aux points de terminaison protégés de l'API REST. Si non fourni, [patronictl](/fr/patroni/patronictl#patronictl) utilisera la valeur fournie pour le paramètre « username » de l'API REST.
- **PATRONI_CTL_PASSWORD** : (facultatif) Mot de passe d'authentification basique pour accéder aux points de terminaison protégés de l'API REST. Si non fourni, [patronictl](/fr/patroni/patronictl#patronictl) utilisera la valeur fournie pour le paramètre « password » de l'API REST.
- **PATRONI_CTL_INSECURE** : (facultatif) Autoriser les connexions à l'API REST sans vérification des certificats SSL.
- **PATRONI_CTL_CACERT** : (facultatif) indique le fichier CA_BUNDLE ou le répertoire contenant les certificats des autorités de certification approuvées pour vérifier les certificats SSL de l'API REST. En l'absence de valeur, [patronictl](/fr/patroni/patronictl#patronictl) utilisera la valeur fournie pour le paramètre "cafile" de l'API REST.
- **PATRONI_CTL_CERTFILE** : (facultatif) indique le fichier du certificat client au format PEM.
- **PATRONI_CTL_KEYFILE** : (facultatif) indique le fichier de la clé secrète du client au format PEM.
- **PATRONI_CTL_KEYFILE_PASSWORD** : (facultatif) Spécifie un mot de passe pour déchiffrer le fichier de clé client.
