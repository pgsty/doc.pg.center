---
title: "Configuration : pgbouncer.ini"
linkTitle: "Configuration"
weight: 20
description: "Fichier de configuration PgBouncer (pgbouncer.ini) – Référence"
icon: fa-solid fa-code
module: [PGBOUNCER]
categories: [Référence]
upstream_link: "https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/doc/config.md"
---

--------

## Description {#description}

Le fichier de configuration est au format « ini ». Les noms de section sont entre `[` et `]`. Les lignes commençant par `;` ou `#` sont traitées comme des commentaires et ignorées. Les caractères `;` et `#` ne sont pas reconnus comme spéciaux lorsqu'ils apparaissent ultérieurement dans la ligne.

--------

## Paramètres génériques {#generic-settings}

### logfile {#logfile}

Spécifie le fichier de journalisation. En mode démon (`-d`), il faut définir soit ce paramètre, soit `syslog`.

Le fichier journal reste ouvert, de sorte que, après rotation, il faut exécuter `kill -HUP` ou, depuis la console, `RELOAD;`. Sur Windows, le service doit être arrêté puis redémarré.

Notez que la configuration de `logfile` ne désactive pas en elle-même la journalisation vers stderr. Utilisez l'option en ligne de commande `-q` ou `-d` à cette fin.

Par défaut : non défini

### pidfile {#pidfile}

Spécifie le fichier PID. Sans `pidfile` défini, la démonisation (`-d`) n'est pas autorisée.

Par défaut : non défini

### listen_addr {#listen_addr}

Spécifie une liste (séparée par des virgules) d'adresses sur lesquelles écouter les connexions TCP. Vous pouvez également utiliser `*`, ce qui signifie « écouter sur toutes les adresses ». Si ce paramètre n'est pas défini, seules les connexions via socket Unix sont acceptées.

Les adresses peuvent être spécifiées sous forme numérique (IPv4/IPv6) ou par nom.

Par défaut : non défini

### listen_port {#listen_port}

Port sur lequel écouter. S'applique aux sockets TCP et Unix.

Par défaut : 6432

### unix_socket_dir {#unix_socket_dir}

Spécifie l'emplacement des sockets Unix. S'applique à la fois au socket d'écoute et aux connexions vers le serveur. Si la valeur est une chaîne vide, les sockets Unix sont désactivés. Une valeur commençant par `@` indique qu'un socket Unix dans l'espace de noms abstrait doit être créé (actuellement pris en charge sous Linux et Windows).

Par défaut : `/tmp` (vide sous Windows)

### unix_socket_mode {#unix_socket_mode}

Mode système de fichiers pour les sockets Unix. Ignoré pour les sockets dans l'espace de noms abstrait. Non pris en charge sous Windows.

Par défaut : 0777

### unix_socket_group {#unix_socket_group}

Nom du groupe à utiliser pour la socket Unix. Ignoré pour les sockets dans l'espace de noms abstrait. Non pris en charge sous Windows.

Par défaut : non défini

### user {#user}

Si défini, spécifie l’utilisateur Unix auquel passer après le démarrage. Fonctionne uniquement si PgBouncer est lancé en tant qu’utilisateur root ou s’il est déjà en cours d’exécution en tant qu’utilisateur donné. Non pris en charge sous Windows.

Par défaut : non défini

### pool_mode {#pool_mode}

Spécifie quand une connexion serveur peut être réutilisée par d'autres clients.

- **`session`** : Le serveur est rendu au pool après la déconnexion du client. Valeur par défaut.
- **`transaction`** : Le serveur est rendu au pool après la fin de la transaction.
- **`statement`** : Le serveur est rendu au pool après la fin de la requête. Les transactions s'étendant sur plusieurs instructions sont interdites dans ce mode.

### max_client_conn {#max_client_conn}

Nombre maximal de connexions clients autorisées.

Lorsque ce paramètre est augmenté, les limites de descripteurs de fichiers du système d'exploitation devront peut-être également être augmentées. Notez que le nombre de descripteurs de fichiers potentiellement utilisés dépasse `max_client_conn`. Si chaque utilisateur se connecte sous son propre nom d'utilisateur au serveur, le maximum théorique utilisé est :

```text
max_client_conn + (max pool_size * total databases * total users)
```

Si un utilisateur de base de données est spécifié dans la chaîne de connexion (tous les utilisateurs se connectent sous le même nom d'utilisateur), le maximum théorique est :

```text
max_client_conn + (max pool_size * total databases)
```

Le nombre maximum théorique ne devrait jamais être atteint, sauf si quelqu’un conçoit délibérément une charge spéciale à cet effet. Cela signifie toutefois que vous devriez fixer le nombre de descripteurs de fichiers à un nombre suffisamment élevé pour être en sécurité.

Recherchez `ulimit` dans la page de manuel de votre shell préféré. Note : `ulimit` n'est pas applicable dans un environnement Windows.

Par défaut : 100

### default_pool_size {#default_pool_size}

Le nombre maximal de connexions serveur autorisées par couple utilisateur/base de données. Peut être remplacé par `pool_size` dans la configuration par base de données et par utilisateur ; il s'agit de la valeur par défaut utilisée si aucun `pool_size` spécifique n'est défini pour une base de données ou un utilisateur donné.

Par défaut : 20

### min_pool_size {#min_pool_size}

Ajoute des connexions serveur supplémentaires au pool si leur nombre est inférieur à cette valeur. Améliore le comportement lorsque la charge normale revient soudainement après une période d'inactivité totale. La valeur est effectivement plafonnée à la taille du pool.

Appliqué uniquement aux pools où au moins l'une des conditions suivantes est vraie :

* l'entrée dans la section `[databases]` pour le pool a une valeur définie pour la clé `user` (appelée utilisateur forcé)
* il y a au moins un client connecté au pool

Par défaut : 0 (désactivé)

### reserve_pool_size {#reserve_pool_size}

Nombre de connexions supplémentaires autorisées vers un pool (voir `reserve_pool_timeout`). 0 désactive.

Par défaut : 0 (désactivé)

### reserve_pool_timeout {#reserve_pool_timeout}

Si un client n’a pas été servi pendant cette durée, utilisez des connexions supplémentaires provenant du pool de réserve. La valeur 0 désactive cette fonctionnalité. [secondes]

Par défaut : 5.0

### max_db_connections {#max_db_connections}

N'autorisez pas plus de ce nombre de connexions serveur par base de données (quel que soit l'utilisateur). Cette limite tient compte de la base de données PgBouncer à laquelle le client est connecté, et non de la base de données PostgreSQL de la connexion sortante.

Cela peut également être défini par base de données dans la section `[databases]`.

Notez que, lorsque la limite est atteinte, la fermeture d’une connexion client vers un pool ne permettra pas immédiatement d’établir une connexion serveur pour un autre pool, car la connexion serveur du premier pool reste ouverte. Une fois que la connexion serveur est fermée (en raison du délai d’inactivité), une nouvelle connexion serveur sera immédiatement établie pour le pool en attente.

Par défaut : 0 (illimité)

### max_db_client_connections {#max_db_client_connections}

N'autorisez pas plus de ce nombre de connexions clients à PgBouncer par base de données (quel que soit l'utilisateur). Cette limite tient compte de la base de données PgBouncer à laquelle le client est connecté, et non de la base de données PostgreSQL de la connexion sortante.

Il devrait être défini à une valeur supérieure ou égale à max_db_connections. La différence entre ces deux valeurs peut être interprétée comme le nombre maximal de connexions à une base de données donnée pouvant être en file d'attente en attendant que les connexions actives se terminent.

Cela peut également être défini par base de données dans la section `[databases]`.

Par défaut : 0 (illimité)

### max_user_connections {#max_user_connections}

N'autorisez pas plus de ce nombre de connexions serveur par utilisateur (quel que soit la base de données). Cette limite tient compte de l'utilisateur PgBouncer associé à un pool, qui est soit l'utilisateur spécifié pour la connexion serveur, soit, en l'absence de celui-ci, l'utilisateur avec lequel le client est connecté.

Cela peut également être défini par utilisateur dans la section `[users]`.

Notez que, lorsque la limite est atteinte, la fermeture d’une connexion client vers un pool ne permettra pas immédiatement d’établir une connexion serveur pour un autre pool, car la connexion serveur du premier pool reste ouverte. Une fois que la connexion serveur est fermée (en raison du délai d’inactivité), une nouvelle connexion serveur sera immédiatement établie pour le pool en attente.

Par défaut : 0 (illimité)

### max_user_client_connections {#max_user_client_connections}

N'autorisez pas plus de ce nombre de connexions clients par utilisateur (indépendamment de la base de données). Cette valeur devrait être définie à un nombre supérieur à max_user_connections. La différence entre max_user_connections et max_user_client_connections peut être conceptualisée comme la taille maximale de la file d'attente pour l'utilisateur.

Cela peut également être défini par utilisateur dans la section `[users]`.

Par défaut : 0 (illimité)

### server_round_robin {#server_round_robin}

Par défaut, PgBouncer réutilise les connexions serveur selon un mode LIFO (dernier entré, premier sorti), ce qui fait que peu de connexions supportent la charge la plus importante. Ce comportement offre les meilleures performances si vous disposez d’un seul serveur servant une base de données. Toutefois, si un système de répartition de charge (round-robin) est placé derrière une adresse de base de données (TCP, DNS ou liste d’hôtes), il est préférable que PgBouncer utilise également les connexions selon ce mode, afin d’obtenir une répartition uniforme de la charge.

Par défaut : 0

### track_extra_parameters {#track_extra_parameters}

Par défaut, PgBouncer suit tous les paramètres que Postgres signale au client et qui peuvent être modifiés par le client :

- `application_name`
- `client_encoding`
- `DateStyle`
- `default_transaction_read_only`
- `IntervalStyle`
- `scram_iterations` (depuis la version 16 de PostgreSQL)
- `search_path` (depuis la version 18 de PostgreSQL)
- `session_authorization`
- `standard_conforming_strings`
- `TimeZone`

Pour permettre le suivi d'autres paramètres, ceux-ci peuvent être spécifiés ici, afin que PgBouncer sache qu'ils doivent être conservés dans le cache des variables client et restaurés sur le serveur chaque fois que le client devient actif.

Si vous devez spécifier plusieurs valeurs, utilisez une liste séparée par des virgules (par exemple, `some_extension.setting, other_extension.setting`)

Note : La plupart des paramètres ne peuvent pas être entièrement suivis de cette manière. PgBouncer n'a connaissance des modifications effectuées avec `SET` que pour les paramètres que Postgres signale au client. Postgres dispose d’[une liste officielle des paramètres qu’il signale au client](https://www.postgresql.org/docs/current/protocol-flow.html#PROTOCOL-ASYNC). Les extensions Postgres peuvent toutefois modifier cette liste : elles peuvent ajouter elles-mêmes des paramètres qu'elles signalent également, et commencer à signaler des paramètres existants que Postgres ne signale pas. En particulier, Citus 12.0+ fait que Postgres signale aussi `search_path`. Certains des paramètres suivis par défaut ne sont également signalés que par les versions plus récentes de Postgres : `default_transaction_read_only` depuis Postgres 14, `scram_iterations` depuis Postgres 16 et `search_path` depuis Postgres 18.

Pour un paramètre suivi que Postgres ne signale pas (par exemple `search_path` sur les versions de Postgres antérieures à 18), PgBouncer ne connaît que la valeur qu'un client a spécifiée dans son paquet de démarrage (ou dans le paramètre de démarrage `options`). Cette valeur est appliquée à la connexion serveur chaque fois que le client devient actif, et le paramètre est réinitialisé à sa valeur par défaut pour les clients qui ne l'ont pas spécifié. Les modifications effectuées avec `SET` après la connexion ne sont pas suivies pour ces paramètres, et fuient donc vers les autres clients partageant la connexion serveur, sauf si `server_reset_query_always` est utilisé.

Le protocole Postgres permet de spécifier des paramètres, soit directement comme paramètre dans le paquet de démarrage, soit à l'intérieur du paquet de démarrage [`options`][options-startup]. Les paramètres spécifiés par l'une ou l'autre de ces méthodes sont pris en charge par `track_extra_parameters`. Toutefois, il n'est pas possible d'inclure `options` lui-même dans `track_extra_parameters`, uniquement les paramètres contenus dans `options`.

Par défaut : vide

### ignore_startup_parameters {#ignore_startup_parameters}

Par défaut, PgBouncer autorise uniquement les paramètres qu'il peut suivre dans les paquets de démarrage (voir `track_extra_parameters` pour la liste). Tous les autres paramètres provoquent une erreur. Pour autoriser d'autres paramètres, ils peuvent être spécifiés ici, afin que PgBouncer sache qu'ils sont gérés par l'administrateur et qu'il puisse les ignorer.

Si vous devez spécifier plusieurs valeurs, utilisez une liste séparée par des virgules (par exemple, `options,extra_float_digits`)

Le protocole Postgres permet de spécifier des paramètres, soit directement comme paramètre dans le paquet de démarrage, soit à l'intérieur du paquet de démarrage [`options`][options-startup]. Les paramètres spécifiés par l'une ou l'autre de ces méthodes sont pris en charge par `ignore_startup_parameters`. Il est même possible d'inclure `options` lui-même dans `ignore_startup_parameters`, auquel cas tout paramètre inconnu contenu dans `options` est ignoré.

[options-startup]: https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-OPTIONS

Par défaut : vide

### peer_id {#peer_id}

L'identifiant pair utilisé pour identifier ce processus PgBouncer au sein d'un groupe de processus PgBouncer interconnectés. La valeur `peer_id` doit être unique au sein d'un groupe de processus PgBouncer interconnectés. Si elle est définie à 0, l'interconnexion des processus PgBouncer est désactivée. Pour plus d'informations, consultez la documentation de la section `[peers]`. La valeur maximale pouvant être utilisée pour `peer_id` est 16383.

Par défaut : 0

### disable_pqexec {#disable_pqexec}

Désactive le protocole Simple Query (PQexec). Contrairement au protocole Extended Query, le protocole Simple Query permet d’envoyer plusieurs requêtes dans un même paquet, ce qui expose à certains types d’attaques par injection SQL. Le désactiver peut améliorer la sécurité. Évidemment, cela signifie que seuls les clients utilisant exclusivement le protocole Extended Query resteront fonctionnels.

Par défaut : 0

### application_name_add_host {#application_name_add_host}

Ajoute l'adresse et le port de l'hôte client au nom d'application défini au début de la connexion. Cela permet d'identifier la source de requêtes incorrectes, etc. Cette logique s'applique uniquement au début d'une connexion. Si `application_name` est modifié ultérieurement avec `SET`, PgBouncer ne le modifie pas à nouveau.

Par défaut : 0

### conffile {#conffile}

Affiche l'emplacement du fichier de configuration actuel. Le modifier amène PgBouncer à utiliser un autre fichier de configuration pour le prochain `RELOAD` / `SIGHUP`.

Par défaut : fichier fourni en ligne de commande

### service_name {#service_name}

Utilisé lors de l'enregistrement du service win32.

Par défaut : `pgbouncer`

### job_name {#job_name}

Alias pour `service_name`.

### stats_period {#stats_period}

Détermine à quelle fréquence les moyennes affichées par diverses commandes `SHOW` sont mises à jour et à quelle fréquence les statistiques agrégées sont écrites dans le journal (mais voir `log_stats`). [secondes]

Par défaut : 60

### max_prepared_statements {#max_prepared_statements}

Lorsque cette valeur est différente de zéro, PgBouncer suit les commandes liées aux requêtes préparées nommées au niveau du protocole envoyées par le client en mode pooling de transactions et pooling d'instructions. PgBouncer garantit que toute requête préparée par un client est disponible sur la connexion serveur qui lui est attribuée, même si elle a été initialement préparée sur une autre connexion serveur.

PgBouncer examine en interne toutes les requêtes envoyées par les clients sous forme de requête préparée, et attribue à chaque chaîne de requête unique un nom interne au format `PGBOUNCER_{unique_id}`. Si la même chaîne de requête est préparée plusieurs fois (éventuellement par des clients différents), ces requêtes partagent le même nom interne. PgBouncer ne prépare la requête sur le serveur PostgreSQL réel qu’en utilisant le nom interne (et non le nom fourni par le client). PgBouncer suit le nom que le client a attribué à chaque requête préparée. Il réécrit ensuite chaque commande utilisant une requête préparée en remplaçant le nom côté client par le nom interne (par exemple, en remplaçant `my_prepared_statement` par `PGBOUNCER_123`) avant de transmettre cette commande au serveur. Plus important encore, si la requête préparée que le client souhaite exécuter n’est pas encore préparée sur le serveur (par exemple, parce qu’un serveur différent est désormais affecté au client que lors de la préparation de la requête), alors PgBouncer prépare la requête de manière transparente avant de l’exécuter.

Note : Le suivi et la réécriture des commandes de requêtes préparées ne fonctionnent pas pour les commandes de requêtes préparées au niveau SQL, aussi `PREPARE`, `EXECUTE` et `DEALLOCATE` sont-ils acheminés directement vers Postgres. L'exception à cette règle concerne les commandes `DEALLOCATE ALL` et `DISCARD ALL`, qui fonctionnent comme prévu et effacent les requêtes préparées que PgBouncer a suivies pour le client qui envoie cette commande.

La valeur réelle de ce paramètre contrôle le nombre de requêtes préparées conservées actives dans un cache LRU sur une connexion serveur unique. Lorsque ce paramètre est défini à 0, le support des requêtes préparées est désactivé pour le pooling de transactions et le pooling d'instructions. Pour obtenir les meilleures performances, vous devez veiller à ce que cette valeur soit supérieure au nombre de requêtes préparées couramment utilisées par votre application. Prenez en compte que plus cette valeur est élevée, plus la consommation mémoire de chaque connexion PgBouncer sur votre serveur PostgreSQL sera importante, car davantage de requêtes seront conservées préparées sur ces connexions. Cela augmente également la consommation mémoire de PgBouncer lui-même, car il doit maintenant suivre les chaînes de requêtes.

L'impact sur la mémoire utilisée par PgBouncer n'est toutefois pas important :
- Chaque requête unique est stockée une seule fois dans un cache de requêtes global.
- Chaque connexion client conserve une mémoire tampon utilisée pour réécrire les paquets. Cette mémoire tampon ne dépasse pas 4 fois la taille de `pkt_buf`. Cette limite n'est toutefois souvent pas atteinte ; cela ne se produit que lorsque les requêtes contenues dans vos requêtes préparées ont une taille comprise entre 2 et 4 fois celle de `pkt_buf`.

Considérez le scénario suivant comme exemple :
- Il y a 1000 clients actifs
- Les clients préparent 200 requêtes uniques
- La taille moyenne d'une requête est de 5kB
- La valeur du paramètre `pkt_buf` est définie par défaut à 4096 (4kB)

Ensuite, PgBouncer a besoin au plus de la quantité suivante de mémoire pour gérer ces requêtes préparées :

```text
200 x 5kB + 1000 x 4 x 4kB = ~17MB of memory.
```

Le suivi des requêtes préparées entraîne non seulement un coût mémoire, mais aussi une utilisation accrue du CPU, car PgBouncer doit inspecter et réécrire les requêtes. Plusieurs instances de PgBouncer peuvent écouter sur le même port afin d'utiliser plusieurs cœurs pour le traitement ; consultez [la documentation de l'option `so_reuseport`](#so_reuseport) pour plus de détails.

Bien entendu, les requêtes préparées offrent également des bénéfices en termes de performance. Tout comme lors d'une connexion directe à PostgreSQL, en préparant une requête exécutée plusieurs fois, on réduit la quantité totale d'analyse syntaxique et de planification nécessaire. La manière dont PgBouncer suit les requêtes préparées est particulièrement avantageuse pour les performances lorsque plusieurs clients préparent la même requête. Car les connexions clients réutilisent automatiquement une requête préparée sur une connexion serveur, même si elle a été préparée par un autre client. Par exemple, si vous avez un `pool_size` de 20 et que 100 clients préparent exactement la même requête, alors la requête n'est préparée (et donc analysée) que 20 fois sur le serveur PostgreSQL.

La réutilisation des requêtes préparées présente un inconvénient. Si les types de retour ou d'argument d'une requête préparée changent entre deux exécutions, PostgreSQL lève actuellement une erreur telle que :

```text
ERROR:  cached plan must not change result type
```

Vous pouvez éviter ces erreurs en ne faisant pas coexister plusieurs clients utilisant exactement la même chaîne de requête dans une requête préparée, tout en attendant des types d'arguments ou de résultats différents. L'une des causes les plus fréquentes de ce problème survient lors d'une migration DDL, par exemple lorsqu'une nouvelle colonne est ajoutée ou qu'un type de colonne est modifié sur une table existante. Dans ces cas, vous pouvez exécuter `RECONNECT` sur la console d'administration de PgBouncer après la migration afin de forcer la re-préparation de la requête et faire disparaître l'erreur.

Par défaut : 200

### scram_iterations {#scram_iterations}

Nombre d'itérations de calcul à effectuer lors du hachage d'un mot de passe à l'aide de SCRAM-SHA-256. Un nombre plus élevé d'itérations offre une protection renforcée contre les attaques par force brute sur les mots de passe stockés, mais ralentit l'authentification.

Par défaut : 4096

--------

## Paramètres d'authentification {#authentication-settings}

PgBouncer gère son propre mécanisme d'authentification des clients et dispose de sa propre base d'utilisateurs. Ces paramètres contrôlent ce comportement.

### auth_type {#auth_type}

Comment authentifier les utilisateurs.

- **`cert`**: Le client doit se connecter via une connexion TLS munie d'un certificat client valide. Le nom d'utilisateur est ensuite extrait du champ CommonName du certificat.
- **`md5`**: Utiliser la vérification de mot de passe basée sur MD5. Il s'agit de la méthode d'authentification par défaut. `auth_file` peut contenir à la fois des mots de passe hachés en MD5 et des mots de passe en clair. Si `md5` est configuré et qu'un utilisateur dispose d'un secret SCRAM, l'authentification SCRAM est utilisée automatiquement à la place.
- **`scram-sha-256`**: Utiliser la vérification de mot de passe avec SCRAM-SHA-256. `auth_file` doit contenir des secrets SCRAM ou des mots de passe en clair.
- **`plain`**: Le mot de passe en clair est transmis sur le réseau. Obsolète.
- **`trust`**: Aucune authentification n'est effectuée. Le nom d'utilisateur doit toutefois exister dans `auth_file`.
- **`any`**: Comme la méthode `trust`, mais le nom d'utilisateur fourni est ignoré. Nécessite que toutes les bases de données soient configurées pour se connecter en tant qu'utilisateur spécifique. En outre, la base de données console permet à n'importe quel utilisateur de se connecter en tant qu'utilisateur de statistiques ; les utilisateurs listés dans `admin_users` reçoivent les privilèges d'administrateur.
- **`hba`**: Le type d'authentification réel est chargé à partir de `auth_hba_file`. Cela permet d'utiliser différentes méthodes d'authentification pour différents chemins d'accès, par exemple : les connexions via socket Unix utilisent la méthode d'authentification `peer`, les connexions via TCP doivent utiliser TLS.
- **`ldap`**: Les utilisateurs sont authentifiés contre un serveur LDAP, comme dans PostgreSQL (voir <https://www.postgresql.org/docs/current/auth-ldap.html> pour les détails). Les options de connexion LDAP sont configurées à l'aide du paramètre `auth_ldap_options`, ou de manière alternative dans le `auth_hba_file`.
- **`pam`**: PAM est utilisé pour authentifier les utilisateurs, `auth_file` est ignoré. Cette méthode n'est pas compatible avec les bases de données utilisant l'option `auth_user`. Le nom de service transmis à PAM est « pgbouncer ». `pam` n'est pas pris en charge dans le fichier de configuration HBA.

### auth_hba_file {#auth_hba_file}

Fichier de configuration HBA à utiliser lorsque `auth_type` est `hba`. Voir la section [Format du fichier HBA](#hba-file-format) ci-dessous pour les détails.

Par défaut : non défini

### auth_ident_file {#auth_ident_file}

Fichier de mappage d'identité à utiliser lorsque `auth_type` est `hba` et qu'un mappage d'utilisateur sera défini. Voir la section [Format du fichier de mappage d'identité](#ident-map-file-format) ci-dessous pour les détails.

Par défaut : non défini

### auth_file {#auth_file}

Nom du fichier à charger pour les noms d’utilisateurs et les mots de passe. Voir la section [Format du fichier d'authentification](#authentication-file-format) ci-dessous pour les détails.

La plupart des types d'authentification (voir ci-dessus) exigent que `auth_file` ou `auth_user` soit défini ; sinon, aucun utilisateur ne serait défini.

Par défaut : non défini

### auth_user {#auth_user}

Si `auth_user` est défini, tout utilisateur non spécifié dans `auth_file` sera interrogé via la requête `auth_query` depuis `pg_authid` dans la base de données, en utilisant `auth_user`. Le mot de passe de `auth_user` sera extrait de `auth_file`. (Si `auth_user` n'exige pas de mot de passe, alors il n'est pas nécessaire de le définir dans `auth_file`.)

L'accès direct à `pg_authid` nécessite des droits d'administrateur. Il est préférable d'utiliser un utilisateur non superutilisateur qui appelle une fonction définie en tant que SECURITY DEFINER.

Par défaut : non défini

### auth_query {#auth_query}

Requête permettant de charger le mot de passe de l'utilisateur depuis la base de données.

L'accès direct à `pg_authid` nécessite des droits d'administrateur. Il est préférable d'utiliser un utilisateur non superutilisateur qui appelle une fonction définie en tant que SECURITY DEFINER.

Notez que la requête s'exécute dans la base de données cible. Ainsi, si une fonction est utilisée, elle doit être installée dans chaque base de données.

La requête doit retourner deux colonnes, le nom d'utilisateur et le mot de passe (chiffré/haché de manière appropriée). Pour signaler que l'utilisateur n'existe pas, retournez soit aucune ligne, soit une ligne dont la valeur du nom d'utilisateur est NULL. (La requête par défaut ci-dessous ne retourne aucune ligne pour un utilisateur inexistant. La variante avec la valeur NULL est utile lorsque la requête appelle une fonction retournant un enregistrement, comme dans l'exemple présenté dans la section [Exemples](#examples) ci-dessous.) Une valeur NULL dans la colonne du mot de passe signifie que l'utilisateur existe mais qu'aucun mot de passe n'est disponible pour lui, de sorte qu'aucun mot de passe proposé par le client ne sera accepté.

Par défaut : `SELECT rolname, CASE WHEN rolvaliduntil < now() THEN NULL ELSE rolpassword END FROM pg_authid WHERE rolname=$1 AND rolcanlogin`

### auth_dbname {#auth_dbname}

Nom de la base de données dans la section `[databases]` à utiliser à des fins d'authentification. Cette option peut être globale ou remplacée dans la chaîne de connexion si ce paramètre est spécifié.

### auth_ldap_options {#auth_ldap_options}

Options de connexion LDAP à utiliser si `auth_type` est `ldap`. (Non utilisées si l'authentification est configurée via `auth_hba_file`.) Exemple :

```ini
auth_ldap_options = ldapurl="ldap://127.0.0.1:12345/dc=example,dc=net?uid?sub"
```

--------

## Paramètres de journalisation {#log-settings}

### syslog {#syslog}

Active ou désactive la journalisation syslog. Sous Windows, le journal des événements est utilisé à la place.

Par défaut : 0

### syslog_ident {#syslog_ident}

Sous quel nom envoyer les journaux à syslog.

Par défaut : `pgbouncer` (nom du programme)

### syslog_facility {#syslog_facility}

Sous quelle facility envoyer les journaux à syslog. Possibilités : `auth`, `authpriv`, `daemon`, `user`, `local0-7`.

Par défaut : `daemon`

### log_connections {#log_connections}

Enregistrer les connexions réussies.

Par défaut : 1

### log_disconnections {#log_disconnections}

Journaliser les déconnexions avec leurs raisons.

Par défaut : 1

### log_pooler_errors {#log_pooler_errors}

Enregistre les messages d'erreur que le pooler envoie aux clients.

Par défaut : 1

### log_stats {#log_stats}

Écrire les statistiques agrégées dans le journal toutes les `stats_period`. Cette fonction peut être désactivée si des outils de surveillance externes sont utilisés pour récupérer les mêmes données à partir des commandes `SHOW`.

Par défaut : 1

### verbose {#verbose}

Augmenter le niveau de verbosité. Correspond à l’option `-v` en ligne de commande. Par exemple, utiliser `-v -v` en ligne de commande équivaut à `verbose=2`. 3 est le niveau de verbosité le plus élevé actuellement pris en charge.

Par défaut : 0

--------

## Contrôle d'accès à la console {#console-access-control}

### admin_users {#admin_users}

Liste séparée par des virgules d'utilisateurs de base de données autorisés à se connecter et à exécuter toutes les commandes sur la console d'administration. Avec `auth_type=any`, cette liste détermine toujours qui reçoit les privilèges d'administrateur ; les autres utilisateurs peuvent se connecter en tant qu'utilisateurs de statistiques. Voir les [contrôles d'accès à la console de la version 1.26.0](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/src/admin.c#L1572-L1609).

Par défaut : vide

### stats_users {#stats_users}

Liste séparée par des virgules d'utilisateurs de base de données autorisés à se connecter et à exécuter des requêtes en lecture seule sur la console. Cela signifie toutes les commandes `SHOW`.

Par défaut : vide

--------

## Vérifications de santé des connexions, délais d'attente {#connection-sanity-checks-timeouts}

### server_reset_query {#server_reset_query}

Requête envoyée au serveur lors de la libération de la connexion, avant de la rendre disponible aux autres clients. À ce moment, aucune transaction n'est en cours, donc la valeur ne doit pas inclure `ABORT` ni `ROLLBACK`.

La requête doit nettoyer tout changement apporté à la session de base de données afin que le client suivant obtienne une connexion dans un état défini. La valeur par défaut est `DISCARD ALL`, qui supprime tout, mais cela laisse le client suivant sans état pré-caché. Elle peut être rendue plus légère, par exemple `DEALLOCATE ALL`, qui ne supprime que les requêtes préparées, si l'application ne casse pas lorsqu'un certain état est conservé.

Lorsqu’un pooling de transactions est utilisé, `server_reset_query` n’est pas utilisé, car, dans ce mode, les clients ne doivent pas utiliser de fonctionnalités liées à la session, puisque chaque transaction aboutit sur une connexion différente et donc dans un état de session différent.

Par défaut : `DISCARD ALL`

### server_reset_query_always {#server_reset_query_always}

Indique si `server_reset_query` doit être exécuté dans tous les modes de pooling. Lorsque ce paramètre est désactivé (valeur par défaut), `server_reset_query` ne sera exécuté que dans les pools en mode pooling de sessions. Les connexions en mode pooling de transactions n’ont pas besoin d’une requête de réinitialisation.

Ce paramètre sert à contourner les configurations défectueuses qui exécutent des applications utilisant des fonctionnalités de session sur un PgBouncer configuré en pooling de transactions. Il transforme une panne aléatoire en une panne déterministe : les clients perdent toujours leur état après chaque transaction.

Par défaut : 0

### server_check_delay {#server_check_delay}

Durée pendant laquelle les connexions libérées sont conservées disponibles pour une réutilisation immédiate, sans exécuter `server_check_query` sur celle-ci. Si la valeur est 0, le contrôle est toujours exécuté.

Par défaut : 30.0

### server_check_query {#server_check_query}

Requête simple sans action pour vérifier si la connexion au serveur est active.

Si la valeur est une chaîne vide, la vérification de cohérence est désactivée.

Si `<empty>`, envoyer une requête vide en tant que vérification de cohérence.

Par défaut : `<empty>`

### server_fast_close {#server_fast_close}

Déconnecte un serveur en mode pooling de sessions immédiatement ou après la fin de la transaction en cours s’il est en mode "close_needed" (défini par `RECONNECT`, `RELOAD` modifiant les paramètres de connexion ou un changement DNS), plutôt que d’attendre la fin de la session. En mode pooling de transactions ou pooling d'instructions, cela n’a aucun effet, car c’est le comportement par défaut dans ces modes.

Si, en raison de ce paramètre, une connexion serveur est fermée avant la fin de la session client, la connexion client est également fermée. Cela garantit que le client détecte que la session a été interrompue.

Ce paramètre permet que les modifications de configuration de connexion prennent effet plus rapidement lorsque le pooling de sessions et des sessions de longue durée sont utilisés. Le désavantage est que les sessions clients risquent d’être interrompues par un changement de configuration, ce qui impose aux applications clientes de prévoir une logique de reconnexion et de rétablissement de l’état de session. Toutefois, notez qu’aucune transaction ne sera perdue, car les transactions en cours ne sont pas interrompues, uniquement les sessions inactives.

Par défaut : 0

### server_lifetime {#server_lifetime}

Le pooler fermera une connexion serveur inutilisée (non actuellement liée à une connexion client) qui a été établie depuis plus longtemps que cette durée. Une valeur de 0 signifie que la connexion ne doit être utilisée qu'une seule fois, puis fermée. [secondes]

Cela peut également être défini par base de données dans la section `[databases]`.

Par défaut : 3600.0

### server_idle_timeout {#server_idle_timeout}

Si une connexion vers un serveur est restée inactive plus de ce nombre de secondes, elle sera fermée. Si cette valeur est 0, ce délai d'expiration est désactivé. [secondes]

Par défaut : 600.0

### server_connect_timeout {#server_connect_timeout}

Si la connexion et l'authentification ne se terminent pas dans ce délai, la connexion sera fermée. [secondes]

Par défaut : 15.0

### server_login_retry {#server_login_retry}

Si la connexion au serveur échoue, en raison d'un échec de connexion ou d'une authentification, le pooler attend cette durée avant de tenter à nouveau de se connecter. Pendant l'intervalle d'attente, les nouveaux clients tentant de se connecter au serveur défaillant obtiennent immédiatement une erreur, sans autre tentative de connexion. [secondes]

Le but de ce comportement est que les clients ne s'accumulent pas inutilement en attente d'une connexion serveur lorsque ce dernier n'est pas opérationnel. Toutefois, cela signifie également qu'en cas de défaillance temporaire du serveur, par exemple lors d'un redémarrage ou en cas de configuration erronée, le pooler ne tentera de se reconnecter à celui-ci qu'au moins après cette durée. Les événements planifiés, tels que les redémarrages, doivent normalement être gérés à l'aide de la commande `PAUSE` afin d'éviter ce délai.

Par défaut : 15.0

### client_login_timeout {#client_login_timeout}

Si un client se connecte mais ne parvient pas à terminer sa connexion dans ce délai, il sera déconnecté. [secondes]

Par défaut : 60.0

### autodb_idle_timeout {#autodb_idle_timeout}

Si les pools de bases de données créés automatiquement (via `*`) n'ont pas été utilisés pendant ce nombre de secondes, ils sont libérés. L'inconvénient de cette approche est qu'ils perdent également leurs statistiques. [secondes]

Par défaut : 3600.0

### pool_idle_timeout {#pool_idle_timeout}

Si un pool (un couple base de données/utilisateur spécifique) est resté sans connexion client ni connexion serveur pendant ce nombre de secondes, il est libéré. Ce paramètre est similaire à `autodb_idle_timeout`, mais il libère des pools individuels plutôt que des bases de données créées automatiquement dans leur ensemble. Notez que, contrairement à `server_idle_timeout` (qui ferme les connexions serveur inactives mais conserve le pool), ce paramètre libère le pool tout entier, et seulement lorsqu'il est complètement vide.

Comme pour `autodb_idle_timeout`, l'inconvénient est que les statistiques d'un pool libéré sont perdues. Étant donné que les totaux par base de données dans `SHOW STATS` correspondent à la somme des pools existant actuellement, libérer un pool fait diminuer ces totaux, ce que les systèmes de surveillance peuvent interpréter à tort comme une réinitialisation de compteur. Pour cette raison, ce paramètre est désactivé par défaut. 0 désactive. [secondes]

Par défaut : 0 (désactivé)

### dns_max_ttl {#dns_max_ttl}

Durée pendant laquelle les résolutions DNS peuvent être mises en cache. Le TTL DNS réel est ignoré. [secondes]

Par défaut : 15.0

### dns_nxdomain_ttl {#dns_nxdomain_ttl}

Durée de mise en cache des erreurs DNS et des requêtes DNS NXDOMAIN. [secondes]

Par défaut : 15.0

### dns_zone_check_period {#dns_zone_check_period}

Période d'inspection pour détecter un changement du numéro de série d'une zone.

PgBouncer peut collecter des zones DNS à partir des noms d’hôte (tout ce qui suit le premier point) et vérifier périodiquement si le numéro de série de la zone a changé. Si une modification est détectée, tous les noms d’hôte de cette zone sont à nouveau résolus. Si l’adresse IP d’un hôte change, ses connexions sont invalidées.

Fonctionne uniquement avec le backend c-ares (option `configure` `--with-cares`).

Par défaut : 0.0 (désactivé)

### resolv_conf {#resolv_conf}

Emplacement d'un fichier `resolv.conf` personnalisé. Cela permet de spécifier des serveurs DNS personnalisés et éventuellement d'autres options de résolution de noms, indépendamment de la configuration globale du système d'exploitation.

Exige un backend evdns (>= 2.0.3) ou c-ares (>= 1.15.0).

L'analyse du fichier est effectuée par la bibliothèque backend DNS, et non par PgBouncer ; reportez-vous à la documentation de la bibliothèque pour obtenir les détails sur la syntaxe et les directives autorisées.

Par défaut : vide (utiliser les paramètres par défaut du système d'exploitation)

### query_wait_notify {#query_wait_notify}

Délai pendant lequel un client sera mis en file d'attente avant que PgBouncer n'envoie un message de notification indiquant qu'il est en file d'attente. [secondes]

Une valeur de 0 désactive ce message de notification.

Par défaut : 5

### login_notify_message {#login_notify_message}

Message de notification de bienvenue envoyé au client après une connexion réussie. Peut être utilisé pour s'assurer que les clients comprennent qu'ils se connectent à pgbouncer plutôt qu'à postgres directement.

Par défaut : vide (aucun message de bienvenue envoyé)

--------

## Paramètres TLS {#tls-settings}

Si le contenu de l'un des fichiers cert ou key est modifié sans changer le nom de fichier réel dans la configuration, les nouveaux contenus de fichier seront utilisés pour les nouvelles connexions après un RELOAD. Les connexions existantes ne seront toutefois pas fermées. Si, pour des raisons de sécurité, il est nécessaire que toutes les connexions utilisent les nouveaux fichiers dès que possible (ASAP), il est conseillé d'exécuter RECONNECT après le RELOAD.

La modification d'un paramètre TLS quelconque déclenche automatiquement un RECONNECT pour des raisons de sécurité.

### client_tls_sslmode {#client_tls_sslmode}

Mode TLS à utiliser pour les connexions provenant des clients. Les connexions TLS sont désactivées par défaut. Lorsqu'elles sont activées, `client_tls_key_file` et `client_tls_cert_file` doivent également être configurés afin de définir la clé et le certificat utilisés par PgBouncer pour accepter les connexions clients. Le format de fichier de certificat le plus courant utilisable par PgBouncer est PEM.

- **`disable`**: TCP brut. Si le client demande TLS, cela est ignoré. Valeur par défaut.
- **`allow`**: Si le client demande TLS, il est utilisé. Sinon, TCP brut est utilisé. Si le client présente un certificat client, il n'est pas validé.
- **`prefer`**: Identique à `allow`.
- **`require`**: Le client doit utiliser TLS. Sinon, la connexion est rejetée. Si le client présente un certificat client, il n'est pas validé.
- **`verify-ca`**: Le client doit utiliser TLS avec un certificat client valide.
- **`verify-full`**: Identique à `verify-ca`.

### client_tls_key_file {#client_tls_key_file}

Clé privée de PgBouncer pour accepter les connexions clients.

Par défaut : non défini

### client_tls_cert_file {#client_tls_cert_file}

Certificat associé à la clé privée. Les clients peuvent le valider.

Par défaut : non défini

### client_tls_ca_file {#client_tls_ca_file}

Fichier de certificat racine utilisé pour valider les certificats clients.

Par défaut : non défini

### client_tls_protocols {#client_tls_protocols}

Quelles versions du protocole TLS sont autorisées. Valeurs autorisées : `tlsv1.0`, `tlsv1.1`, `tlsv1.2`, `tlsv1.3`. Raccourcis : `all` (tlsv1.0,tlsv1.1,tlsv1.2,tlsv1.3), `secure` (tlsv1.2,tlsv1.3).

Par défaut : `secure`

### client_tls_ciphers {#client_tls_ciphers}

Chiffrements TLS autorisés, au format OpenSSL. Raccourcis :

- `default`/`secure`/`fast`/`normal` (tous utilisent les paramètres par défaut OpenSSL du système)
- `all` (active tous les chiffrements, non recommandé)

Seules les connexions utilisant la version TLS 1.2 et inférieure sont concernées. Pour la version 1.3, voir `client_tls13_ciphers` ci-dessous.

Par défaut : `default`

### client_tls13_ciphers {#client_tls13_ciphers}

Chiffrements TLS v1.3 autorisés. Si vide, il utilisera la valeur de `client_tls_ciphers`. Valeurs autorisées :

- `TLS_AES_256_GCM_SHA384`
- `TLS_CHACHA20_POLY1305_SHA256`
- `TLS_AES_128_GCM_SHA256`
- `TLS_AES_128_CCM_8_SHA256`
- `TLS_AES_128_CCM_SHA256`

Seules les connexions utilisant TLS version 1.3 et supérieure sont concernées. Pour les versions 1.2 et inférieures, voir `client_tls_ciphers`.

Par défaut : `<empty>`

### client_tls_ecdhcurve {#client_tls_ecdhcurve}

Nom de la courbe elliptique à utiliser pour les échanges de clés ECDH.

Valeurs autorisées : `none` (DH désactivé), `auto` (ECDH 256 bits), nom de courbe

Par défaut : `auto`

### client_tls_dheparams {#client_tls_dheparams}

Type d'échange de clés DHE.

Valeurs autorisées : `none` (DH désactivé), `auto` (DH 2048 bits), `legacy` (DH 1024 bits)

Par défaut : `auto`

### server_tls_sslmode {#server_tls_sslmode}

Mode TLS à utiliser pour les connexions aux serveurs PostgreSQL. Le mode par défaut est `prefer`.

- **`disable`** : TCP brut. Le serveur n'est même pas interrogé pour une connexion TLS.
- **`allow`** : Se comporte comme `prefer` : demande d'abord TLS, puis se rabat sur une connexion TCP non chiffrée si le serveur refuse TLS. Le certificat du serveur n'est pas validé.
- **`prefer`** : Une connexion TLS est toujours demandée en premier au serveur PostgreSQL. Si elle est refusée, la connexion est établie en TCP brut. Le certificat du serveur n'est pas validé. Valeur par défaut.
- **`require`** : La connexion doit obligatoirement s'établir en TLS. Si le serveur la refuse, la connexion en TCP brut n'est pas tentée. Le certificat du serveur n'est pas validé.
- **`verify-ca`** : La connexion doit obligatoirement s'établir en TLS et le certificat du serveur doit être valide selon `server_tls_ca_file`. Le nom d'hôte du serveur n'est pas vérifié par rapport au certificat.
- **`verify-full`** : La connexion doit obligatoirement s'établir en TLS et le certificat du serveur doit être valide selon `server_tls_ca_file`. Le nom d'hôte du serveur doit correspondre aux informations du certificat.

### server_tls_ca_file {#server_tls_ca_file}

Fichier de certificat racine utilisé pour valider les certificats des serveurs PostgreSQL.

Par défaut : non défini

### server_tls_key_file {#server_tls_key_file}

Clé privée de PgBouncer pour s'authentifier auprès du serveur PostgreSQL.

Par défaut : non défini

### server_tls_cert_file {#server_tls_cert_file}

Certificat associé à la clé privée. Le serveur PostgreSQL peut le valider.

Par défaut : non défini

### server_tls_protocols {#server_tls_protocols}

Quelles versions du protocole TLS sont autorisées. Valeurs autorisées : `tlsv1.0`, `tlsv1.1`, `tlsv1.2`, `tlsv1.3`. Raccourcis : `all` (tlsv1.0,tlsv1.1,tlsv1.2,tlsv1.3), `secure` (tlsv1.2,tlsv1.3), `legacy` (all).

Par défaut : `secure`

### server_tls_ciphers {#server_tls_ciphers}

Chiffrements TLS autorisés, au format OpenSSL. Raccourcis :

- `default`/`secure`/`fast`/`normal` (tous utilisent les paramètres par défaut OpenSSL du système)
- `all` (active tous les chiffrements, non recommandé)

Seules les connexions utilisant la version TLS 1.2 et inférieure sont concernées. Pour la version 1.3, voir `server_tls13_ciphers` ci-dessous.

Par défaut : `default`

### server_tls13_ciphers {#server_tls13_ciphers}

Chiffrements TLS v1.3 autorisés. Si vide, il utilisera la valeur de `server_tls_ciphers`. Valeurs autorisées :

- `TLS_AES_256_GCM_SHA384`
- `TLS_CHACHA20_POLY1305_SHA256`
- `TLS_AES_128_GCM_SHA256`
- `TLS_AES_128_CCM_8_SHA256`
- `TLS_AES_128_CCM_SHA256`

Seules les connexions utilisant TLS version 1.3 et supérieure sont concernées. Pour les versions 1.2 et inférieures, voir `server_tls_ciphers`.

Par défaut : `<empty>`

--------

## Délais d'attente dangereux {#dangerous-timeouts}

Définir les délais suivants peut entraîner des erreurs imprévues.

### query_timeout {#query_timeout}

Requêtes exécutées plus longtemps que ce délai sont annulées. Cette option ne devrait être utilisée qu'avec un `statement_timeout` côté serveur légèrement plus petit, afin de ne s'appliquer qu'en cas de problèmes réseau. [secondes]

Par défaut : 0.0 (désactivé)

### query_wait_timeout {#query_wait_timeout}

Temps maximal autorisé aux requêtes pour attendre leur exécution. Si la requête n'est pas affectée à un serveur pendant cette durée, le client est déconnecté. La valeur 0 désactive cette fonctionnalité. Si cette option est désactivée, les clients seront mis en file d'attente indéfiniment. [secondes]

Ce paramètre est utilisé pour empêcher des serveurs ne répondant plus de s'accaparer des connexions. Il est également utile lorsque le serveur est hors service ou refuse les connexions pour quelque raison que ce soit.

Ce paramètre peut également être configuré par base de données et par utilisateur. La précédence est : utilisateur, puis base de données, puis global. Une valeur 0 explicite au niveau sélectionné désactive ce délai d'expiration. Voir le [code de sélection du délai de la version 1.26.0](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/src/janitor.c#L328-L336).

Par défaut : 120.0

### cancel_wait_timeout {#cancel_wait_timeout}

Temps maximal autorisé aux demandes d'annulation pour attendre leur exécution. Si la demande d'annulation n'est pas affectée à un serveur pendant cette durée, le client est déconnecté. La valeur 0 désactive cette fonctionnalité. Si cette option est désactivée, les demandes d'annulation seront mises en file d'attente indéfiniment. [secondes]

Ce paramètre est utilisé pour empêcher qu’un client ne se bloque lorsqu’une annulation ne peut être acheminée en raison de la panne du serveur.

Par défaut : 10.0

### client_idle_timeout {#client_idle_timeout}

Les connexions clients inactives depuis plus de ce nombre de secondes sont fermées. Cette valeur devrait être supérieure aux paramètres de durée de vie des connexions côté client, et n’est utilisée qu’en cas de problèmes réseau. [secondes]

Par défaut : 0.0 (désactivé)

### idle_transaction_timeout {#idle_transaction_timeout}

Si un client reste plus longtemps que cette durée dans l’état « idle in transaction », il sera déconnecté. [secondes]

Par défaut : 0.0 (désactivé)

### transaction_timeout {#transaction_timeout}

Si un client reste plus longtemps que cette durée dans l'état « en transaction », il sera déconnecté. [secondes]

Par défaut : 0.0 (désactivé)

--------

## Paramètres réseau de bas niveau {#low-level-network-settings}

### pkt_buf {#pkt_buf}

Taille du tampon interne pour les paquets. Influence la taille des paquets TCP envoyés et l'utilisation mémoire globale. Les paquets réels libpq peuvent être plus grands que cette valeur, il n'est donc pas nécessaire de la définir élevée.

Par défaut : 4096

### max_packet_size {#max_packet_size}

Taille maximale des paquets PostgreSQL autorisés par PgBouncer. Un paquet correspond soit à une requête, soit à une ligne d'un jeu de résultats. Le jeu de résultats complet peut être plus grand.

Par défaut : 2147483647

### listen_backlog {#listen_backlog}

Argument Backlog pour `listen(2)`. Détermine le nombre de nouvelles tentatives de connexion non traitées conservées dans la file d'attente. Lorsque la file est pleine, les nouvelles connexions supplémentaires sont rejetées.

Par défaut : 128

### sbuf_loopcnt {#sbuf_loopcnt}

Nombre de fois où les données doivent être traitées sur une connexion avant de passer à l'étape suivante. Sans cette limite, une connexion avec un grand jeu de résultats peut bloquer PgBouncer pendant une longue période. Une boucle traite une quantité de données égale à `pkt_buf`. La valeur 0 signifie qu'aucune limite n'est appliquée.

Par défaut : 5

### so_reuseport {#so_reuseport}

Spécifie si l'option de socket `SO_REUSEPORT` doit être définie sur les sockets TCP d'écoute. Sur certains systèmes d'exploitation, cela permet d'exécuter plusieurs instances de PgBouncer sur le même hôte, écoutant sur le même port, avec une répartition automatique des connexions par le noyau. Cette option permet à PgBouncer d'utiliser davantage de cœurs processeurs. (PgBouncer est monothread et utilise un cœur processeur par instance.)

Le comportement en détail dépend du noyau du système d'exploitation. À la date de rédaction de ce document, ce paramètre produit l'effet souhaité sur Linux (versions suffisamment récentes), DragonFlyBSD et FreeBSD. (Sur FreeBSD, il applique l'option de socket `SO_REUSEPORT_LB` à la place.) Certains autres systèmes d'exploitation prennent en charge l'option de socket, mais celle-ci n'aura pas l'effet souhaité : elle permettra à plusieurs processus de se lier au même port, mais seul l'un d'entre eux recevra les connexions. Consultez la documentation de votre système d'exploitation concernant `setsockopt()` pour plus de détails.

Sur les systèmes qui ne prennent pas du tout en charge l'option de socket, activer ce paramètre entraînera une erreur.

Chaque instance de PgBouncer sur le même hôte doit disposer de paramètres différents au moins pour `unix_socket_dir` et `pidfile`, ainsi que pour `logfile` si celui-ci est utilisé. Notez également que, si vous utilisez cette option, il devient impossible de se connecter à une instance spécifique de PgBouncer via TCP/IP, ce qui peut avoir des implications pour la surveillance et la collecte de métriques.

Pour garantir que les annulations de requêtes fonctionnent correctement, vous devriez configurer le peering PgBouncer entre les différents processus PgBouncer. Pour plus de détails, reportez-vous à la documentation relative à l'option de configuration `peer_id` et à la section de configuration `peers`. Un exemple utilisant le peering et `so_reuseport` est également disponible dans la section d'exemples de cette documentation.

Par défaut : 0

### tcp_defer_accept {#tcp_defer_accept}

Définit l'option de socket `TCP_DEFER_ACCEPT` ; consultez `man 7 tcp` pour les détails. (Il s'agit d'une option booléenne : 1 signifie activée. La valeur réelle définie lorsqu'elle est activée est actuellement codée en dur à 45 secondes.)

Cela n’est actuellement pris en charge que sous Linux.

Par défaut : 1 sous Linux, sinon 0

### tcp_socket_buffer {#tcp_socket_buffer}

Par défaut : non défini

### tcp_keepalive {#tcp_keepalive}

Active la fonctionnalité de keepalive basique avec les paramètres par défaut du système d'exploitation.

Sur Linux, les valeurs par défaut du système sont `tcp_keepidle=7200`, `tcp_keepintvl=75`, `tcp_keepcnt=9`. Elles sont probablement similaires sur d'autres systèmes d'exploitation.

Par défaut : 1

### tcp_keepcnt {#tcp_keepcnt}

Par défaut : non défini

### tcp_keepidle {#tcp_keepidle}

Par défaut : non défini

### tcp_keepintvl {#tcp_keepintvl}

Par défaut : non défini

### tcp_user_timeout {#tcp_user_timeout}

Définit l'option de socket `TCP_USER_TIMEOUT`. Cela précise la durée maximale, en millisecondes, pendant laquelle les données transmises peuvent rester non reconnues avant que la connexion TCP ne soit fermée de force. Si cette valeur est définie à 0, la valeur par défaut du système d'exploitation est utilisée.

Cela n’est actuellement pris en charge que sous Linux.

Par défaut : 0

--------

## Section [databases] {#section-databases}

La section `[databases]` définit les noms des bases de données auxquelles les clients de PgBouncer peuvent se connecter et précise où ces connexions seront acheminées. La section contient des lignes key=value telles que

```ini
dbname = connection string
```

où la clé sera prise comme nom de base de données et la valeur comme chaîne de connexion, composée de paires clé=valeur de paramètres de connexion, décrites ci-dessous (similaire à libpq, mais la bibliothèque libpq réelle n'est pas utilisée et l'ensemble des fonctionnalités disponibles est différent). Exemple :

```ini
foodb = host=host1.example.com port=5432
bardb = host=localhost dbname=bazdb
```

Le nom de base de données peut contenir les caractères `_0-9A-Za-z` sans guillemets. Les noms contenant d'autres caractères doivent être cités avec les guillemets standard SQL pour les identifiants : guillemets doubles, avec `""` pour une occurrence unique de guillemet double.

Le nom de base de données `pgbouncer` est réservé à la console d'administration et ne peut pas être utilisé comme clé ici.

`*` agit comme base de données de secours : si le nom exact n'existe pas, sa valeur est utilisée comme chaîne de connexion pour la base de données demandée. Par exemple, si une entrée existe (et aucune autre entrée ne la surcharge)

```ini
* = host=foo
```

alors une connexion à PgBouncer spécifiant une base de données `bar` se comportera effectivement comme si une entrée

```ini
bar = host=foo dbname=bar
```

existait (en tirant parti du fait que la valeur par défaut de `dbname` est le nom de la base de données côté client ; voir ci-dessous).

Les entrées de base de données créées automatiquement sont supprimées si elles restent inactives plus longtemps que le délai spécifié par le paramètre `autodb_idle_timeout`.

### dbname {#dbname}

Nom de la base de données de destination.

Par défaut : identique au nom de la base du côté client

### host {#host}

Nom d'hôte ou adresse IP vers laquelle se connecter. Les noms d'hôte sont résolus au moment de la connexion, le résultat est mis en cache pendant la durée spécifiée par le paramètre `dns_max_ttl`. Lorsqu'une résolution de nom d'hôte change, les connexions serveur existantes sont automatiquement fermées lorsqu'elles sont libérées (selon le mode de pooling), et les nouvelles connexions serveur utilisent immédiatement la nouvelle résolution. Si DNS retourne plusieurs résultats, ils sont utilisés de manière round-robin.

Si la valeur commence par `/`, un socket Unix dans l'espace de noms du système de fichiers est utilisé. Si la valeur commence par `@`, un socket Unix dans l'espace de noms abstrait est utilisé.

Une liste séparée par des virgules d’hôtes ou d’adresses peut être spécifiée. Dans ce cas, les connexions sont établies de manière round-robin. (Si une liste d’hôtes contient des noms d’hôtes qui se résolvent eux-mêmes via DNS en plusieurs adresses, les systèmes de rotation opèrent de manière indépendante. Il s’agit d’une dépendance d’implémentation susceptible de changer.) Notez qu’une liste exige que tous les hôtes soient disponibles en permanence : aucun mécanisme n’existe pour ignorer les hôtes inaccessibles ou sélectionner uniquement les hôtes disponibles dans la liste ou similaire. (Cela diffère de ce qu’une liste d’hôtes signifie dans libpq.) Notez également que cela n’a d’effet que sur le choix des destinations des nouvelles connexions. Voir également le paramètre `server_round_robin` pour savoir comment les clients sont affectés aux connexions serveur déjà établies.

Exemples :

```text
host=localhost
host=127.0.0.1
host=2001:0db8:85a3:0000:0000:8a2e:0370:7334
host=/var/run/postgresql
host=192.168.0.1,192.168.0.2,192.168.0.3
```

Par défaut : non défini, ce qui signifie utiliser une socket Unix

### port {#port}

Par défaut : 5432

### user {#user-1}

Si `user=` est défini, toutes les connexions à la base de données cible seront établies avec l'utilisateur spécifié, ce qui signifie qu'il n'y aura qu'un seul pool pour cette base de données.

Sinon, PgBouncer se connecte à la base de données de destination avec le nom d'utilisateur du client, ce qui signifie qu'il y aura un pool par utilisateur.

### password {#password}

Si aucun mot de passe n'est spécifié ici, le mot de passe provenant de `auth_file` sera utilisé pour l'utilisateur indiqué ci-dessus. Les formes dynamiques de découverte de mot de passe telles que `auth_query` ne sont pas actuellement prises en charge.

### auth_user {#auth_user-1}

Remplacement du paramètre global `auth_user`, le cas échéant.

### auth_query {#auth_query-1}

Remplacement du paramètre global `auth_query`, le cas échéant. L'intégralité de l'instruction SQL doit être entourée de guillemets simples.

### auth_dbname {#auth_dbname-1}

Remplacement du paramètre global `auth_dbname`, le cas échéant.

### pool_size {#pool_size}

Définir la taille maximale des pools pour cette base de données. Si ce paramètre n'est pas défini, la valeur de `default_pool_size` est utilisée.

### min_pool_size {#min_pool_size-1}

Définir la taille minimale du pool pour cette base de données. Si ce paramètre n'est pas défini, la valeur globale `min_pool_size` est utilisée.

Imposé uniquement si au moins l'une des conditions suivantes est vraie :

* cette entrée dans la section `[databases]` a une valeur définie pour la clé `user` (appelée utilisateur forcé)
* il y a au moins un client connecté au pool

### reserve_pool_size {#reserve_pool_size-1}

Définir un nombre supplémentaire de connexions pour cette base de données. Si ce paramètre n'est pas défini, la valeur globale `reserve_pool_size` est utilisée. Pour des raisons de compatibilité descendante, `reserve_pool` est un alias de cette option.

### connect_query {#connect_query}

Requête à exécuter après établissement d'une connexion, mais avant de permettre à tout client de l'utiliser. Si la requête génère des erreurs, celles-ci sont journalisées, mais ignorées dans les autres cas.

### pool_mode {#pool_mode-1}

Définissez le mode de pool spécifique à cette base de données. Si ce paramètre n'est pas défini, le mode par défaut `pool_mode` est utilisé.

### query_wait_timeout {#query_wait_timeout-1}

Temps maximal autorisé aux requêtes pour attendre leur exécution. La valeur 0 désactive cette fonctionnalité. Omettez ce paramètre pour hériter de la valeur par défaut applicable. [secondes]

Voir la description du paramètre global `query_wait_timeout` pour plus de détails.

Un `query_wait_timeout` défini au niveau utilisateur prime sur ce paramètre de base de données. Si aucun des deux n'est défini, le `query_wait_timeout` global est utilisé.

### load_balance_hosts {#load_balance_hosts}

Lorsqu'une liste séparée par des virgules est spécifiée dans `host`, `load_balance_hosts` détermine quel élément est sélectionné pour une nouvelle connexion.

Note : Ce paramètre contrôle actuellement uniquement le comportement de répartition de charge lorsqu’une chaîne de connexion contient plusieurs hôtes, mais pas lorsqu’un enregistrement DNS d’un hôte unique fait référence à plusieurs adresses IP. Il s’agit d’une fonctionnalité manquante, donc dans une version future, ce paramètre pourrait commencer à contrôler les deux méthodes de répartition de charge.

- **`round-robin`** : Une nouvelle tentative de connexion choisit l'entrée hôte suivante dans la liste.
- **`disable`** : Une nouvelle connexion continue d'utiliser la même entrée hôte jusqu'à ce qu'une connexion échoue, après quoi l'entrée hôte suivante est choisie.

Il est recommandé de définir `server_login_retry` à une valeur inférieure à celle par défaut afin d'assurer des tentatives rapides lorsqu'un ou plusieurs hôtes sont disponibles.

Par défaut : `round-robin`

### max_db_connections {#max_db_connections-1}

Définir un maximum de connexions serveur au niveau de la base de données (c'est-à-dire que toutes les pools au sein de la base de données ne comporteront pas plus de ce nombre de connexions serveur).

### max_db_client_connections {#max_db_client_connections-1}

Configure le nombre maximum de connexions clients au niveau de la base de données. Devrait être utilisé en conjonction avec `max_client_conn` afin de limiter le nombre de connexions que PgBouncer est autorisé à accepter.

### server_lifetime {#server_lifetime-1}

Configurez `server_lifetime` par base de données. Si ce paramètre n'est pas défini, la base de données utilisera la valeur configurée au niveau de l'instance pour `server_lifetime`.

### client_encoding {#client_encoding}

Demande un `client_encoding` spécifique au serveur.

### datestyle {#datestyle}

Demande le `datestyle` spécifique au serveur.

### timezone {#timezone}

Demande le `timezone` spécifique au serveur.

--------

## Section [users] {#section-users}

Cette section contient des lignes key=value telles que

```ini
user1 = settings
```

où la clé sera prise comme nom d'utilisateur et la valeur comme liste de paires clé=valeur de paramètres de configuration spécifiques à cet utilisateur. Exemple :

```ini
user1 = pool_mode=session
```

Seuls quelques paramètres sont disponibles ici.

Notez que lorsque `auth_file` est configuré, si un utilisateur est défini dans cette section mais non listé dans `auth_file`, PgBouncer tentera d'utiliser `auth_query` pour trouver le mot de passe de cet utilisateur si `auth_user` est défini. Si `auth_user` n'est pas défini, PgBouncer fera comme si l'utilisateur existait et ne renverra pas de message « no such user » au client, mais il n'acceptera aucun mot de passe fourni.

### pool_size {#pool_size-1}

Définir la taille maximale des pools pour toutes les connexions de cet utilisateur. Si ce paramètre n'est pas défini, la base de données ou `default_pool_size` est utilisée.

### reserve_pool_size {#reserve_pool_size-2}

Définir le nombre de connexions supplémentaires autorisées pour un pool de cet utilisateur. Si ce paramètre n'est pas défini, la configuration de la base de données ou la valeur globale `reserve_pool_size` est utilisée.

### pool_mode {#pool_mode-2}

Définir le mode de pool à utiliser pour toutes les connexions de cet utilisateur. Si ce paramètre n'est pas défini, le mode défini dans la base de données ou la valeur par défaut `pool_mode` est utilisé.

### max_user_connections {#max_user_connections-1}

Définir un maximum pour le nombre de connexions serveur par utilisateur (c’est-à-dire que tous les pools associés à l’utilisateur ne comporteront pas plus de ce nombre de connexions serveur).

### query_timeout {#query_timeout-1}

Définissez le nombre maximal de secondes pendant lesquelles une requête utilisateur peut s'exécuter. Si ce délai est défini, il remplace le paramètre `query_timeout` au niveau du serveur décrit ci-dessus.

### query_wait_timeout {#query_wait_timeout-2}

Temps maximal autorisé aux requêtes pour attendre leur exécution. La valeur 0 désactive cette fonctionnalité. Omettez ce paramètre pour hériter de la valeur par défaut applicable. [secondes]

Voir la description du paramètre global `query_wait_timeout` pour plus de détails.

Ce paramètre prime à la fois sur le `query_wait_timeout` défini au niveau de la base de données et sur le global. S'il n'est pas défini, le paramètre de la base de données est utilisé, à défaut la valeur globale.

### idle_transaction_timeout {#idle_transaction_timeout-1}

Définissez le nombre maximum de secondes pendant lesquelles une transaction inactive peut rester ouverte pour un utilisateur. Si ce délai est défini, il remplace le paramètre `idle_transaction_timeout` au niveau du serveur décrit ci-dessus.

### transaction_timeout {#transaction_timeout-1}

Définissez le nombre maximum de secondes pendant lesquelles une transaction peut rester ouverte pour un utilisateur. Si ce paramètre est défini, il remplace le délai d'attente au niveau du serveur `transaction_timeout` décrit ci-dessus.

### client_idle_timeout {#client_idle_timeout-1}

Définissez le délai maximal en secondes pendant lequel un client est autorisé à rester connecté sans activité à l'instance PgBouncer. Si ce délai est défini, il remplace le paramètre `client_idle_timeout` au niveau du serveur décrit ci-dessus.

Veuillez noter qu’il s’agit d’un délai d'attente potentiellement dangereux.

### max_user_client_connections {#max_user_client_connections-1}

Définir un maximum pour le nombre de connexions clients par utilisateur. Il s'agit de l'équivalent utilisateur de la configuration `max_client_conn`.

--------

## Section [peers] {#section-peers}

La section `[peers]` définit les pairs auxquels PgBouncer peut acheminer les requêtes d'annulation et l'emplacement vers lequel ces requêtes d'annulation seront acheminées.

Les processus PgBouncer peuvent être associés en groupe en définissant une valeur `peer_id` et une section `[peers]` dans les configurations de tous les processus PgBouncer. Ces processus PgBouncer peuvent alors transférer les requêtes d'annulation vers le processus qui a reçu la requête à annuler. Cela est nécessaire pour assurer le bon fonctionnement des annulations lorsque plusieurs processus PgBouncer (éventuellement sur des serveurs différents) sont situés derrière le même équilibreur de charge TCP. Les requêtes d'annulation sont envoyées via des connexions TCP différentes de celles de la requête qu'elles annulent, si bien qu'un équilibreur de charge TCP pourrait acheminer la connexion de requête d'annulation vers un processus différent de celui visé. En les associant, ces requêtes d'annulation parviennent finalement au bon processus. Une explication plus détaillée est fournie dans cet [enregistrement d'une conférence][cancel-problem-video].

[cancel-problem-video]: https://www.youtube.com/watch?v=X-nCHcZ6vQU

La section contient des lignes key=value telles que

```ini
peer_id = connection string
```

Où la clé sera utilisée comme `peer_id` et la valeur comme chaîne de connexion, composée de paires clé=valeur de paramètres de connexion, décrites ci-dessous (similaire à libpq, mais la bibliothèque libpq n’est pas utilisée et l’ensemble des fonctionnalités disponibles est différent). Exemple :

```ini
1 = host=host1.example.com
2 = host=/tmp/pgbouncer-2  port=5555
```

Note 1 : Pour que le peering fonctionne, le `peer_id` de chaque processus PgBouncer doit être unique au sein du groupe. La section `[peers]` devrait contenir une entrée pour chacun de ces identifiants. Un exemple est disponible dans la section Exemples de cette documentation. Il **est** autorisé, mais non obligatoire, d'inclure dans la section `[peers]` le `peer_id` du processus PgBouncer auquel la configuration est destinée. Cette entrée sera ignorée, mais sa présence simplifie la gestion des configurations : elle permet d'utiliser exactement la même section `[peers]` dans plusieurs configurations.

Note 2 : Le peering entre versions différentes est pris en charge à condition que tous les pairs soient du même côté de la limite de version v1.21.0. La version v1.21.0 a introduit des modifications importantes dans la manière dont les jetons d'annulation sont encodés, les rendant incompatibles avec ceux générés par les versions antérieures.

### host {#host-1}

Nom d'hôte ou adresse IP vers laquelle se connecter. Les noms d'hôte sont résolus au moment de la connexion, le résultat est mis en cache pendant la durée spécifiée par le paramètre `dns_max_ttl`. Si DNS retourne plusieurs résultats, ils sont utilisés de manière round-robin. Toutefois, il n'est généralement pas recommandé d'utiliser un nom d'hôte qui résout vers plusieurs adresses IP, car la requête d'annulation pourrait encore être acheminée vers le mauvais nœud, ce qui nécessiterait un nouvel acheminement (autorisé au maximum trois fois).

Si la valeur commence par `/`, un socket Unix dans l'espace de noms du système de fichiers est utilisé. Si la valeur commence par `@`, un socket Unix dans l'espace de noms abstrait est utilisé.

Exemples :

```text
host=localhost
host=127.0.0.1
host=2001:0db8:85a3:0000:0000:8a2e:0370:7334
host=/var/run/pgbouncer-1
```

### port {#port-1}

Par défaut : 6432

### pool_size {#pool_size-2}

Définissez le nombre maximal de demandes d'annulation pouvant être en cours vers le pair en même temps. Il est tout à fait normal que des demandes d'annulation arrivent par vagues, par exemple lorsque le serveur Postgres sous-jacent est lent ou hors service. Il est donc important que `pool_size` ne soit pas trop bas afin de pouvoir gérer ces vagues.

Si ce n'est pas défini, `default_pool_size` est utilisé.

--------

## Directive include {#include-directive}

Le fichier de configuration de PgBouncer peut contenir des directives include, qui spécifient un autre fichier de configuration à lire et à traiter. Cela permet de diviser le fichier de configuration en parties physiquement séparées. Les directives include ont la forme suivante :

```ini
%include filename
```

Si le nom de fichier n'est pas un chemin absolu, il est considéré comme relatif au répertoire de travail courant.

--------

## Format de fichier d'authentification {#authentication-file-format}

Cette section décrit le format du fichier spécifié par le paramètre `auth_file`. Il s'agit d'un fichier texte au format suivant :

```text
"username1" "password" ...
"username2" "md5abcdef012342345" ...
"username2" "SCRAM-SHA-256$<iterations>:<salt>$<storedkey>:<serverkey>"
```

Il doit y avoir au moins 2 champs, entourés de guillemets doubles. Le premier champ est le nom d'utilisateur et le second est soit un mot de passe en clair, soit un mot de passe haché en MD5, soit un secret SCRAM. PgBouncer ignore le reste de la ligne. Les guillemets doubles dans une valeur de champ peuvent être échappés en écrivant deux guillemets doubles.

Format de mot de passe MD5 PostgreSQL :

```text
"md5" + md5(password + username)
```

L'utilisateur `admin` avec le mot de passe `1234` disposera d'un mot de passe haché MD5 égal à `md545f2603610af569b6155c45067268c6b`.

Format secret SCRAM PostgreSQL :

```text
SCRAM-SHA-256$<iterations>:<salt>$<storedkey>:<serverkey>
```

Consultez la documentation PostgreSQL et le RFC 5803 pour plus de détails à ce sujet.

Les mots de passe ou secrets stockés dans le fichier d'authentification servent à deux fins. Premièrement, ils sont utilisés pour vérifier les mots de passe des connexions clients entrantes, si une méthode d'authentification basée sur le mot de passe est configurée. Deuxièmement, ils sont utilisés comme mots de passe pour les connexions sortantes vers le serveur backend, si le serveur backend exige une authentification basée sur le mot de passe (à moins que le mot de passe ne soit spécifié directement dans la chaîne de connexion de la base de données).

### Limitations {#limitations}

Si le mot de passe est stocké en clair, il peut être utilisé pour toute authentification basée sur le mot de passe utilisée par le serveur backend ; clair, MD5 ou SCRAM (voir <https://www.postgresql.org/docs/current/auth-password.html> pour les détails).

Les mots de passe hachés MD5 peuvent être utilisés si le serveur backend utilise l'authentification MD5 (ou si certains utilisateurs ont des mots de passe hachés MD5).

Les secrets SCRAM ne peuvent être utilisés pour se connecter à un serveur que si l’authentification du client utilise également SCRAM, si la définition de la base de données dans PgBouncer ne précise pas de nom d’utilisateur, et si les secrets SCRAM sont identiques dans PgBouncer et le serveur PostgreSQL (même sel et nombre d’itérations, et non seulement le même mot de passe). Ceci est dû à une propriété de sécurité intrinsèque du SCRAM : le secret SCRAM stocké ne peut, en lui-même, être utilisé pour dériver les identifiants de connexion.

Le fichier d'authentification peut être rédigé à la main, mais il est également utile de le générer à partir d'une autre liste d'utilisateurs et de mots de passe. Consultez `./etc/mkauth.py` pour un exemple de script permettant de générer le fichier d'authentification à partir de la table système `pg_authid`. En alternative, utilisez `auth_query` à la place de `auth_file` afin d'éviter d'avoir à maintenir un fichier d'authentification séparé.

### Remarque sur les serveurs gérés {#note-on-managed-servers}

Si le serveur backend est configuré pour utiliser l’authentification par mot de passe SCRAM, PgBouncer ne peut pas s’authentifier correctement s’il ne connaît ni a) le mot de passe utilisateur en clair, ni b) le secret SCRAM correspondant.

Certains fournisseurs de cloud (par exemple, AWS RDS) interdisent l'accès aux tables système sensibles de PostgreSQL pour récupérer les mots de passe. Même pour l'utilisateur le plus privilégié (par exemple, membre de `rds_superuser`), `select * from pg_authid` retourne `ERROR: permission denied for table pg_authid`. Ce comportement est connu ([blog](https://aws.amazon.com/blogs/database/best-practices-for-migrating-postgresql-databases-to-amazon-rds-and-amazon-aurora/)).

Par conséquent, il est impossible de récupérer un secret SCRAM existant une fois qu’il a été stocké sur un serveur géré, ce qui rend difficile la configuration de PgBouncer pour utiliser le même secret SCRAM. Toutefois, il est encore possible de configurer et d’utiliser le secret SCRAM des deux côtés en utilisant la méthode suivante :

Générez le secret SCRAM pour un mot de passe arbitraire à l’aide d’un outil capable d’afficher le secret. Par exemple, `psql --echo-hidden` et la commande `\password` affichent le secret SCRAM sur la console avant de l’envoyer au serveur.

```bash
$ psql --echo-hidden <connection_string>
postgres=# \password <role_name>
Enter new password for user "<role_name>":
Enter it again:
********* QUERY **********
ALTER USER <role_name> PASSWORD 'SCRAM-SHA-256$<iterations>:<salt>$<storedkey>:<serverkey>'
**************************
```

Notez le secret SCRAM affiché dans la section QUERY et définissez-le dans `userlist.txt` de PgBouncer.

Si vous avez utilisé un outil autre que `psql --echo-hidden`, vous devez également définir le secret SCRAM sur le serveur (vous pouvez utiliser `ALTER ROLE <role_name> PASSWORD '<scram_secret>'` à cette fin).

--------

## Format du fichier HBA {#hba-file-format}

L'emplacement du fichier HBA est spécifié par le paramètre `auth_hba_file`. Il n'est utilisé que si `auth_type` est défini à `hba`.

Le fichier suit le format du fichier PostgreSQL `pg_hba.conf` (voir <https://www.postgresql.org/docs/current/auth-pg-hba-conf.html>).

* Types d'enregistrement pris en charge : `local`, `host`, `hostssl`, `hostnossl`.
* Champ base de données : prend en charge `all`, `replication`, `sameuser`, `@file`, plusieurs noms. Non pris en charge : `samerole`, `samegroup`.
* Champ nom d'utilisateur : prend en charge `all`, `@file`, plusieurs noms. Non pris en charge : `+groupname`.
* Champ adresse : prend en charge `all`, IPv4, IPv6. Non pris en charge : `samehost`, `samenet`, noms DNS, préfixes de domaine.
* Champ méthode d'authentification : seules les méthodes prises en charge par le `auth_type` de PgBouncer sont prises en charge, ainsi que `peer` et `reject`, mais à l'exception de `any` et `pam`, qui ne fonctionnent qu'à l'échelle globale.
* Le paramètre de mappage de nom d'utilisateur (`map=`) est pris en charge lorsque `auth_type` est défini à `cert` ou `peer`.

--------

## Format du fichier de mappage d'identité {#ident-map-file-format}

L'emplacement du fichier de correspondance ident est spécifié par le paramètre `auth_ident_file`. Il n'est chargé que si `auth_type` est défini sur `hba`.

Le format de fichier est une variante simplifiée du fichier de correspondance ident PostgreSQL (voir <https://www.postgresql.org/docs/current/auth-username-maps.html>).

* Les lignes prises en charge sont uniquement au format `map-name system-username database-username`.
* Aucune prise en charge de l'inclusion de fichiers ou de répertoires.
* Champ nom d'utilisateur système : non pris en charge : expressions régulières.
* Champ nom d'utilisateur base de données : prend en charge `all` ou un seul nom d'utilisateur Postgres. Non pris en charge : `+groupname`, expressions régulières.

--------

## Exemples {#examples}

Exemple de configuration minimaliste :

```ini
[databases]
template1 = host=localhost dbname=template1 auth_user=someuser

[pgbouncer]
pool_mode = session
listen_port = 6432
listen_addr = localhost
auth_type = md5
auth_file = users.txt
logfile = pgbouncer.log
pidfile = pgbouncer.pid
admin_users = someuser
stats_users = stat_collector
```

Exemples de bases de données :

```ini
[databases]

; foodb over Unix socket
foodb =

; redirect bardb to bazdb on localhost
bardb = host=localhost dbname=bazdb

; access to destination database will go with single user
forcedb = host=localhost port=300 user=baz password=foo client_encoding=UNICODE datestyle=ISO
```

Exemple d'une fonction sécurisée pour `auth_query` :

```sql
CREATE OR REPLACE FUNCTION pgbouncer.user_lookup(in i_username text, out uname text, out phash text)
RETURNS record AS $$
BEGIN
    SELECT rolname, CASE WHEN rolvaliduntil < now() THEN NULL ELSE rolpassword END
    FROM pg_authid
    WHERE rolname=i_username AND rolcanlogin
    INTO uname, phash;
    RETURN;
END;
$$ LANGUAGE plpgsql
   SECURITY DEFINER
   -- Set a secure search_path: trusted schema(s), then 'pg_temp'.
   SET search_path = pg_catalog, pg_temp;
REVOKE ALL ON FUNCTION pgbouncer.user_lookup(text) FROM public, pgbouncer;
GRANT EXECUTE ON FUNCTION pgbouncer.user_lookup(text) TO pgbouncer;
```

Exemples de configurations pour 2 processus PgBouncer en peering afin de créer une configuration PgBouncer à plusieurs cœurs utilisant `so_reuseport`. La configuration du premier processus :

```ini
[databases]
postgres = host=localhost dbname=postgres

[peers]
1 = host=/tmp/pgbouncer1
2 = host=/tmp/pgbouncer2

[pgbouncer]
listen_addr=127.0.0.1
auth_file=auth_file.conf
so_reuseport=1
unix_socket_dir=/tmp/pgbouncer1
peer_id=1
```

La configuration du second processus :

```ini
[databases]
postgres = host=localhost dbname=postgres

[peers]
1 = host=/tmp/pgbouncer1
2 = host=/tmp/pgbouncer2

[pgbouncer]
listen_addr=127.0.0.1
auth_file=auth_file.conf
so_reuseport=1
; only unix_socket_dir and peer_id are different
unix_socket_dir=/tmp/pgbouncer2
peer_id=2
```

--------

## Voir aussi {#see-also}

pgbouncer(1) - page de manuel pour une utilisation générale, commandes de la console

<https://www.pgbouncer.org/>
