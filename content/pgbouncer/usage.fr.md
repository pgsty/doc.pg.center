---
title: "Usage : pgbouncer commande"
linkTitle: "Utilisation"
weight: 30
description: "Utilisation en ligne de commande et console d'administration de PgBouncer"
icon: fa-solid fa-bell-concierge
module: [PGBOUNCER]
categories: [Tâche]
aliases: [/docs/pgbouncer/usage/]
upstream_link: "https://www.pgbouncer.org/usage.html"
---

--------

## Synopsis {#synopsis}

    pgbouncer [-d][-R][-v][-u user] <pgbouncer.ini>
    pgbouncer -V|-h

Sous Windows, les options sont :

    pgbouncer.exe [-v][-u user] <pgbouncer.ini>
    pgbouncer.exe -V|-h

Options supplémentaires pour la configuration d'un service Windows :

    pgbouncer.exe --regservice   <pgbouncer.ini>
    pgbouncer.exe --unregservice <pgbouncer.ini>

--------

## Description {#description}

**pgbouncer** est un pooler de connexions PostgreSQL. Toute application cliente peut se connecter à **pgbouncer** comme s’il était un serveur PostgreSQL, et **pgbouncer** établira une connexion vers le serveur réel, ou réutilisera l’une de ses connexions existantes.

L'objectif de **pgbouncer** est de réduire l'impact sur les performances lié à l'ouverture de nouvelles connexions vers PostgreSQL.

Afin de ne pas compromettre la sémantique transactionnelle pour le pooling de connexions, **pgbouncer** prend en charge plusieurs types de pooling lors de la rotation des connexions :

Pooling de sessions

:   Méthode la moins intrusive. Lorsqu’un client se connecte, une connexion serveur lui est attribuée pour toute la durée de sa connexion. Lorsque le client se déconnecte, la connexion serveur est remise dans le pool. Il s’agit de la méthode par défaut.

Pooling de transactions

:   Une connexion serveur est attribuée à un client uniquement pendant une transaction.
    Lorsque PgBouncer détecte la fin de la transaction, la connexion serveur sera remise dans le pool.

Pooling d'instructions

:   Méthode la plus agressive. La connexion au serveur sera immédiatement remise dans le pool après la fin d'une requête. Les transactions multi-instructions sont interdites en ce mode, car elles seraient rompues.

L’interface d’administration de **pgbouncer** propose de nouvelles commandes `SHOW`, disponibles lorsque l’on se connecte à une base de données « virtuelle » spéciale nommée **pgbouncer**.

--------

## Démarrage rapide {#quick-start}

Configuration et utilisation de base se déroulent comme suit.

1. Créez un fichier pgbouncer.ini. Détails dans **pgbouncer(5)**. Exemple simple :

        [databases]
        template1 = host=localhost port=5432 dbname=template1

        [pgbouncer]
        listen_port = 6432
        listen_addr = localhost
        auth_type = md5
        auth_file = userlist.txt
        logfile = pgbouncer.log
        pidfile = pgbouncer.pid
        admin_users = someuser

2. Créez un fichier `userlist.txt` contenant les utilisateurs autorisés :

        "someuser" "same_password_as_in_server"

3. Lancez **pgbouncer** :

        $ pgbouncer -d pgbouncer.ini

4. Faites que votre application (ou le client **psql**) se connecte à **pgbouncer** au lieu de se connecter directement au serveur PostgreSQL :

        $ psql -p 6432 -U someuser template1

5. Gérez **pgbouncer** en vous connectant à la base de données d'administration spéciale **pgbouncer** et en émettant `SHOW HELP;` pour commencer :

        $ psql -p 6432 -U someuser pgbouncer
        pgbouncer=# SHOW HELP;
        NOTICE:  Console usage
        DETAIL:
          SHOW [HELP|CONFIG|DATABASES|FDS|POOLS|CLIENTS|SERVERS|SOCKETS|LISTS|VERSION|...]
          SET key = arg
          RELOAD
          PAUSE
          SUSPEND
          RESUME
          SHUTDOWN
          [...]

6. Si vous avez modifié le fichier pgbouncer.ini, vous pouvez le recharger à l'aide de :

        pgbouncer=# RELOAD;

--------

## Options de ligne de commande {#command-line-switches}

`-d`, `--daemon`
:   Exécuter en arrière-plan. Sans cette option, le processus s'exécute en premier plan.

    In daemon mode, setting `pidfile` as well as `logfile` or `syslog`
    is required.  No log messages will be written to stderr after
    going into the background.

    Note: Does not work on Windows; **pgbouncer** need to run as service there.

`-R`, `--reboot`
:   **OBSOLÈTE : au lieu de cette option, utilisez un redémarrage progressif avec plusieurs processus pgbouncer écoutant sur le même port en utilisant so_reuseport**
    Effectuez un redémarrage en ligne. Cela signifie vous connecter au processus en cours d'exécution, charger les sockets ouverts depuis celui-ci, puis les utiliser. Si aucun processus actif n'est présent, démarrez normalement.
    Note : Fonctionne uniquement si le système d'exploitation prend en charge les sockets Unix et si `unix_socket_dir` n'est pas désactivé dans la configuration. Ne fonctionne pas sous Windows.
    Ne fonctionne pas avec les connexions TLS, celles-ci sont perdues.

`-u` _USERNAME_, `--user=` _USERNAME_
:   Passer à l’utilisateur spécifié au démarrage.

`-v`, `--verbose`
:   Augmenter le niveau de détail. Peut être utilisé plusieurs fois.

`-q`, `--quiet`
:   Soyez silencieux : ne pas journaliser sur stderr. Cela n’affecte pas le niveau de verbosité du journal, uniquement le fait que stderr ne doit pas être utilisé. À utiliser dans les scripts init.d.

`-V`, `--version`
:   Affiche la version.

`-h`, `--help`
:   Affiche l’aide courte.

`--regservice`
:   Win32 : inscrire PgBouncer pour s'exécuter en tant que service Windows. La valeur du paramètre de configuration **service_name** est utilisée comme nom d'enregistrement.

`--unregservice`
:   Win32 : Désinscrire le service Windows.

--------

## Console d'administration {#admin-console}

La console est disponible en se connectant normalement à la base de données **pgbouncer** :

    $ psql -p 6432 pgbouncer

Seuls les utilisateurs listés dans les paramètres de configuration **admin_users** ou **stats_users** peuvent se connecter à la console. (À moins que `auth_type=any`, auquel cas tout utilisateur est autorisé à se connecter en tant que stats_user.)

En outre, le nom d’utilisateur **pgbouncer** est autorisé à se connecter sans mot de passe, si la connexion est établie via le socket Unix et que l’utilisateur Unix du client est identique à celui du processus en cours d’exécution.

La console d'administration ne prend actuellement en charge que le protocole de requête simple.
Certains pilotes utilisent le protocole de requête étendu pour toutes les commandes ; ces pilotes ne fonctionneront pas dans ce cas.

### Afficher les commandes {#show-commands}

Les commandes **SHOW** produisent des informations. Chaque commande est décrite ci-dessous.

#### MONTRER STATS {#show-stats}

Affiche les statistiques. Dans cette commande et les commandes apparentées, les valeurs totales correspondent à partir du démarrage du processus, les moyennes sont mises à jour toutes les `stats_period`.

base de données
:   Les statistiques sont présentées par base de données.

total_xact_count
:   Nombre total de transactions SQL regroupées par **pgbouncer**.

total_query_count
:   Nombre total de commandes SQL regroupées par **pgbouncer**.

total_server_assignment_count
:   Nombre total d'affectations d'un serveur à un client

total_received
:   Volume total en octets du trafic réseau reçu par **pgbouncer**.

total_sent
:   Volume total en octets de trafic réseau envoyé par **pgbouncer**.

total_xact_time
:   Nombre total de microsecondes passées par **pgbouncer** lorsqu'il est connecté à PostgreSQL dans une transaction, qu'elles soient en attente ou en cours d'exécution.

total_query_time
:   Nombre total de microsecondes passées par **pgbouncer** lorsqu'il est activement connecté à PostgreSQL, en exécutant des requêtes.

total_wait_time
:   Temps passé par les clients en attente d'un serveur, en microsecondes. Mis à jour lorsque la connexion d'un client est associée à une connexion serveur.

total_client_parse_count
:   Nombre total de requêtes préparées créées par les clients. N'est applicable que dans le mode de suivi des requêtes préparées nommées, voir `max_prepared_statements`.

total_server_parse_count
:   Nombre total d'instructions préparées créées par **pgbouncer** sur un serveur. N'est applicable que dans le mode de suivi des instructions préparées nommées, voir `max_prepared_statements`.

total_bind_count
:   Nombre total de requêtes préparées lues par les clients et transférées à PostgreSQL par **pgbouncer**. N'est applicable que dans le mode de suivi des requêtes préparées nommées, voir `max_prepared_statements`.

avg_xact_count
:   Nombre moyen de transactions par seconde durant la dernière période de statistiques.

avg_query_count
:   Nombre moyen de requêtes par seconde durant la dernière période de statistiques.

avg_server_assignment_count
:   Nombre moyen de fois où un serveur est affecté à un client par seconde pendant la dernière période de statistiques.

avg_recv
:   Octets reçus en moyenne (par les clients) par seconde.

avg_sent
:   Nombre moyen d'octets envoyés (aux clients) par seconde.

avg_xact_time
:   Durée moyenne d'une transaction, en microsecondes.

avg_query_time
:   Durée moyenne d'exécution d'une requête, en microsecondes.

avg_wait_time
:   Temps passé par les clients en attente d'un serveur, en microsecondes (moyenne des temps d'attente des clients affectés à un backend pendant le `stats_period` actuel).

avg_client_parse_count
:   Nombre moyen de requêtes préparées créées par les clients. N'est applicable que dans le mode de suivi des requêtes préparées nommées, voir `max_prepared_statements`.

avg_server_parse_count
:   Nombre moyen de requêtes préparées créées par **pgbouncer** sur un serveur. N'est applicable que dans le mode de suivi des requêtes préparées nommées, voir `max_prepared_statements`.

avg_bind_count
:   Nombre moyen de requêtes préparées lues par les clients et transférées à PostgreSQL par **pgbouncer**. N'est applicable que dans le mode de suivi des requêtes préparées nommées, voir `max_prepared_statements`.

#### SHOW STATS_TOTALS {#show-stats_totals}

Sous-ensemble de **SHOW STATS** affichant les valeurs totales (**total_**).


#### SHOW STATS_AVERAGES {#show-stats_averages}

Sous-ensemble de **SHOW STATS** affichant les valeurs moyennes (**avg_**).

#### SHOW TOTALS {#show-totals}

Comme **SHOW STATS**, mais agrégé pour toutes les bases de données.

#### SHOW SERVEURS {#show-servers}

type
:   S, pour serveur.

user
:   Nom d'utilisateur que **pgbouncer** utilise pour se connecter au serveur.

base
:   Nom de la base de données.

réplication
:   Si la connexion au serveur utilise la réplication. Peut être **none**, **logical** ou **physical**.

state
:   État de la connexion du serveur PgBouncer, l'une des valeurs suivantes : **active**, **idle**, **used**, **tested**, **new**, **active_cancel**, **being_canceled**.

addr
:   Adresse IP du serveur PostgreSQL.

port
:   Port du serveur PostgreSQL.

local_addr
:   Adresse de départ de la connexion sur la machine locale.

local_port
:   Port de départ pour les connexions sur la machine locale.

connect_time
:   Date de la connexion.

request_time
:   Date de la dernière requête émise.

wait
:   Non utilisé pour les connexions serveur.

wait_us
:   Non utilisé pour les connexions serveur.

close_needed
:   1 si la connexion sera fermée dès que possible, car un rechargement du fichier de configuration ou une mise à jour DNS a modifié les informations de connexion ou que **RECONNECT** a été émis.

ptr
:   Adresse de l'objet interne pour cette connexion.

lien
:   Adresse de la connexion client avec laquelle le serveur est apparié.

remote_pid
:   PID du processus serveur backend. En cas de connexion via un socket Unix et si le système d'exploitation prend en charge la récupération des informations sur le PID, il s'agit du PID système. Sinon, il est extrait du paquet d'annulation envoyé par le serveur, qui doit correspondre au PID si le serveur est PostgreSQL, mais il s'agit d'un nombre aléatoire si le serveur est un autre PgBouncer.

tls
:   Chaîne contenant les informations de connexion TLS, ou chaîne vide si TLS n'est pas utilisé.

application_name
:   Chaîne de caractères contenant le `application_name` défini sur la connexion client liée,
    ou vide si ce paramètre n'est pas défini, ou s'il n'existe pas de connexion liée.

instructions préparées
:  Le nombre d'instructions préparées effectuées sur le serveur. Ce nombre est limité par le paramètre `max_prepared_statements`.

id
:   ID unique du serveur.


#### MONTRER LES CLIENTS {#show-clients}

type
:   C, pour client.

user
:   Utilisateur du client connecté.

base
:   Nom de la base de données.

réplication
:   Si la connexion client utilise la réplication. Peut être **none**, **logical** ou **physical**.

state
:   État de la connexion client, l'une des valeurs suivantes : **active** (connexions clients liées à des connexions serveur), **idle** (connexions clients sans requête en attente de traitement), **waiting**, **active_cancel_req** ou **waiting_cancel_req**.

addr
:   Adresse IP du client.

port
:   Port source du client.

local_addr
:   Adresse de bout de connexion sur la machine locale.

local_port
:   Port de connexion sur la machine locale.

connect_time
:   Horodatage de l'instant de connexion.

request_time
:   Horodatage de la dernière requête du client.

wait
:   Temps d'attente actuel en secondes.

wait_us
:   Partie en microsecondes du temps d'attente actuel.

close_needed
:   non utilisé pour les clients

ptr
:   Adresse de l'objet interne pour cette connexion.

lien
:   Adresse de la connexion serveur avec laquelle le client est apparié.

remote_pid
:   Identifiant de processus, au cas où le client se connecterait via une socket Unix
    et que le système d'exploitation le permette.

tls
:   Chaîne contenant les informations de connexion TLS, ou chaîne vide si TLS n'est pas utilisé.

application_name
:   Chaîne de caractères contenant le `application_name` défini par le client pour cette connexion, ou vide si ce champ n’a pas été défini.

prepared_statements
:  Nombre de requêtes préparées par le client

id
:   ID unique du client.

#### SHOW POOLS {#show-pools}

Une nouvelle entrée de pool est créée pour chaque couple (base de données, utilisateur).

base
:   Nom de la base de données.

user
:   Nom d'utilisateur.

cl_active
:   Connexions clientes qui sont soit associées à des connexions serveur, soit inactives sans requête en attente de traitement.

cl_waiting
:   Connexions client qui ont envoyé des requêtes mais n’ont pas encore obtenu de connexion serveur.

cl_active_cancel_req
:   Connexions clientes ayant transmis des demandes d'annulation de requête au serveur et en attente de la réponse du serveur.

cl_waiting_cancel_req
:   Connexions clientes qui n'ont pas encore transmis les demandes d'annulation de requête au serveur.

sv_active
:   Connexions serveur liées à un client.

sv_active_cancel
:   Connexions serveur en cours d'envoi d'une demande d'annulation.

sv_being_canceled
:   Serveurs qui pourraient normalement devenir inactifs mais qui attendent de le devenir jusqu'à ce que toutes les demandes d'annulation en cours aient été traitées, celles-ci ayant été envoyées pour annuler une requête sur ce serveur.

sv_idle
:   Connexions serveur inutilisées et immédiatement disponibles pour les requêtes clients.

sv_used
:   Connexions serveur qui ont été inactives pendant plus de `server_check_delay`,
    donc elles nécessitent `server_check_query` pour pouvoir être utilisées à nouveau.

sv_tested
:   Connexions serveur en cours d'exécution soit `server_reset_query`, soit `server_check_query`.

sv_login
:   Connexions serveur actuellement en cours de connexion.

maxwait
:   Temps d'attente, en secondes, du premier (plus ancien) client dans la file d'attente.
    Si cette valeur commence à augmenter, c'est que le pool de serveurs actuel ne traite pas les requêtes assez rapidement.
    La cause peut être soit un serveur surchargé, soit une valeur de **pool_size** trop faible.

maxwait_us
:   Partie en microsecondes du temps d'attente maximal.

pool_mode
:   Le mode de mise en pool utilisé.

load_balance_hosts
:   Le paramètre load_balance_hosts utilisé si l'hôte du pool contient une liste séparée par des virgules.

#### SHOW PEER_POOLS {#show-peer_pools}

Une nouvelle entrée peer_pool est créée pour chaque pair configuré.

base de données
:   ID de l'entrée pair configurée.

cl_active_cancel_req
:   Connexions clientes ayant transmis des demandes d'annulation de requête au serveur et en attente de la réponse du serveur.

cl_waiting_cancel_req
:   Connexions clientes qui n'ont pas encore transmis les demandes d'annulation de requête au serveur.

sv_active_cancel
:   Connexions serveur en cours d'envoi d'une demande d'annulation.

sv_login
:   Connexions serveur actuellement en cours de connexion.

#### MONTRER LES LISTES {#show-lists}

Affiche les informations internes suivantes, en colonnes (et non en lignes) :

bases de données
:   Nombre de bases de données.

utilisateurs
:   Nombre d'utilisateurs.

pools
:   Nombre de pools.

free_clients
:   Nombre de clients libres. Ce sont des clients déconnectés, mais PgBouncer conserve en mémoire la mémoire allouée pour eux afin de la réutiliser ultérieurement pour de nouveaux clients, afin d'éviter des allocations.

used_clients
:   Nombre de clients utilisés.

login_clients
:   Nombre de clients en état **login**.

free_servers
:   Nombre de serveurs libres. Ce sont des serveurs déconnectés, mais PgBouncer conserve en mémoire la mémoire allouée pour eux afin de la réutiliser ultérieurement pour des serveurs futurs, afin d'éviter de nouvelles allocations.

used_servers
:   Nombre de serveurs utilisés.

dns_names
:   Nombre de noms DNS dans le cache.

dns_zones
:   Nombre de zones DNS en cache.

dns_queries
:   Nombre de requêtes DNS en cours.

dns_pending
:   non utilisé

#### MONTRER UTILISATEURS {#show-users}

name
:   Le nom d'utilisateur

pool_size
:   La taille de pool substituée par l'utilisateur. Peut être NULL si non définie.

reserve_pool_size
:   La taille de réserve personnalisée pour l'utilisateur, ou NULL si non définie.

pool_mode
:   Le mode de pool défini par l'utilisateur, ou NULL si non défini.

max_user_connections
:   Paramètre max_user_connections de l'utilisateur. Si ce paramètre n'est pas défini pour cet utilisateur spécifique, la valeur par défaut sera affichée.

current_connections
:   Nombre actuel de connexions au serveur que cet utilisateur a ouvert vers tous les serveurs.

max_user_client_connections
:   Paramètre max_user_client_connections de l'utilisateur. Si ce paramètre n'est pas défini pour cet utilisateur spécifique, la valeur par défaut sera affichée.

current_client_connections
:   Nombre actuel de connexions clients ouvertes par cet utilisateur vers PgBouncer.

#### SHOW DATABASES {#show-databases}

name
:   Nom de l'entrée de base de données configurée.

host
:   Hôte auquel PgBouncer se connecte.

port
:   Port auquel PgBouncer se connecte.

base de données
:   Nom réel de la base de données vers laquelle PgBouncer se connecte.

force_user
:   Lorsque l'utilisateur est spécifié dans la chaîne de connexion, la connexion entre PgBouncer et PostgreSQL est forcée à l'utilisateur indiqué, quel que soit l'utilisateur client.

pool_size
:   Nombre maximal de connexions vers le serveur.

min_pool_size
:   Nombre minimum de connexions vers le serveur.

reserve_pool_size
:   Nombre maximal de connexions supplémentaires pour cette base de données.

server_lifetime
:   Durée maximale de vie d'une connexion serveur pour cette base de données

pool_mode
:   Le mode de poolage substitut de la base de données, ou NULL si le mode par défaut doit être utilisé à la place.

load_balance_hosts
:   L'option load_balance_hosts de la base de données si l'hôte contient une liste séparée par des virgules.

max_connections
:   Nombre maximal de connexions serveur autorisées pour cette base de données, tel que défini par **max_db_connections**, soit globalement, soit par base de données.

current_connections
:   Nombre actuel de connexions serveur pour cette base de données.

max_client_connections
:   Nombre maximal de connexions clients autorisées pour cette instance de PgBouncer, tel que défini par max_db_client_connections par base de données.

current_client_connections
:   Nombre actuel de connexions clients pour cette base de données.

en pause
:   1 si cette base de données est actuellement en pause, sinon 0.

désactivé
:   1 si cette base de données est actuellement désactivée, sinon 0.

#### MONTRER LES PEERS {#show-peers}

peer_id
:   Identifiant de l'entrée pair configurée.

host
:   Hôte auquel PgBouncer se connecte.

port
:   Port auquel PgBouncer se connecte.

pool_size
:   Nombre maximal de connexions serveur pouvant être établies vers ce pair

#### SHOW FDS {#show-fds}

Commande interne – affiche la liste des descripteurs de fichiers en cours d'utilisation avec leur état interne associé.

Lorsque l’utilisateur connecté porte le nom « pgbouncer », se connecte via une socket Unix et possède le même UID que le processus en cours d’exécution, les descripteurs de fichiers réels sont transmis à travers la connexion. Ce mécanisme est utilisé pour effectuer un redémarrage en ligne.
Note : Cette fonctionnalité ne fonctionne pas sous Windows.

Cette commande bloque également la boucle d'événements interne, elle ne doit donc pas être utilisée pendant que PgBouncer est en cours d'utilisation.

fd
:   Valeur numérique du descripteur de fichier.

tâche
:   L'un des éléments suivants : **pooler**, **client** ou **server**.

utilisateur : Utilisateur de la connexion utilisant le descripteur de fichier (FD).

base de données
:   Base de données de la connexion utilisant le descripteur de fichier (FD).

addr
:   Adresse IP de la connexion utilisant le descripteur de fichier (FD), **unix** si un socket Unix est utilisé.

port
:   Port utilisé par la connexion utilisant le descripteur de fichier (FD).

annuler
:   Clé d'annulation pour cette connexion.

lien
:   descripteur de fichier correspondant au serveur/client. NULL si inactif.

#### SHOW SOCKETS, SHOW ACTIVE_SOCKETS {#show-sockets-show-active_sockets}

Affiche des informations de bas niveau sur les sockets ou uniquement les sockets actifs.
Cela inclut les informations affichées sous **SHOW CLIENTS** et **SHOW SERVERS**, ainsi que d'autres informations de niveau plus bas.

#### SHOW CONFIG {#show-config}

Affiche les paramètres de configuration actuels, un par ligne, avec les colonnes suivantes :

clé
:   Nom de la variable de configuration

valeur
:   Valeur de configuration

default
:   Valeur par défaut de la configuration

modifiable
:   Soit **yes** soit **no**, indique si la variable peut être modifiée pendant l'exécution.
    Si **no**, la variable ne peut être modifiée qu'au démarrage. Utilisez **SET** pour modifier une variable en cours d'exécution.

#### SHOW MEM {#show-mem}

Affiche des informations de bas niveau sur les tailles actuelles des différentes allocations mémoire internes. Les informations présentées sont sujettes à modification.

#### SHOW DNS_HOSTS {#show-dns_hosts}

Afficher les noms d'hôte dans le cache DNS.

hostname
:   Nom d'hôte.

ttl
:   Nombre de secondes avant la prochaine recherche.

addrs
:   Liste de adresses séparées par des virgules.

#### SHOW DNS_ZONES {#show-dns_zones}

Affiche les zones DNS en mémoire cache.

zonename
:   Nom de la zone.

serial
:   Numéro de série actuel.

count
:   Noms d'hôtes appartenant à cette zone.


#### SHOW VERSION {#show-version}

Affiche la chaîne de version de PgBouncer.

#### MONTRER ÉTAT {#show-state}

Affiche les paramètres d'état de PgBouncer. Les états actuels sont : *active*, *paused* et *suspended*.

### Commandes de contrôle du processus {#process-controlling-commands}

#### PAUSE [db] {#pause-db}

PgBouncer tente de se déconnecter de tous les serveurs. La déconnexion de chaque connexion serveur attend que cette connexion serveur soit libérée selon le mode de pooling du pool serveur (en mode pooling de transactions, la transaction doit être terminée ; en mode statement, l'instruction doit être terminée ; en mode pooling de sessions, le client doit se déconnecter). La commande ne retourne pas avant que toutes les connexions serveur n’aient été déconnectées. À utiliser lors d’un redémarrage de la base de données.

Si le nom de la base de données est spécifié, seule cette base de données sera mise en pause.

Les nouvelles connexions clients vers une base de données en pause resteront en attente jusqu'à l'appel de **RESUME**.

#### DÉSACTIVER db {#disable-db}

Refuser toutes les nouvelles connexions clients sur la base de données donnée.

#### ACTIVER db {#enable-db}

Autoriser de nouvelles connexions clients après une commande précédente **DISABLE**.

#### RECONNECT [db] {#reconnect-db}

Ferme chaque connexion serveur ouverte pour la base de données donnée, ou pour toutes les bases de données, après sa libération (selon le mode de mise en pool), même si sa durée de vie n’est pas encore écoulée. De nouvelles connexions serveur peuvent être établies immédiatement et se connecteront selon les paramètres de taille du pool.

Cette commande est utile lorsque la configuration de connexion au serveur a changé, par exemple pour effectuer un basculement progressif vers un nouveau serveur. Elle *n’est pas* nécessaire lorsqu’une chaîne de connexion dans le fichier pgbouncer.ini a été modifiée et rechargée (voir **RELOAD**) ou lorsque la résolution DNS a changé, car dans ces cas, la commande équivalente sera exécutée automatiquement. Cette commande n’est nécessaire que si quelque chose en aval de PgBouncer route les connexions.

Après l'exécution de cette commande, une période prolongée peut s'écouler durant laquelle certaines connexions serveur sont dirigées vers une ancienne destination et d'autres vers une nouvelle destination. Cette situation n'est probablement pertinente que lors du basculement du trafic en lecture seule entre des réplicas en lecture seule, ou lors du basculement entre les nœuds d'une configuration de réplication multimaster. Si toutes les connexions doivent être redirigées simultanément, **PAUSE** est recommandé à la place. Pour fermer les connexions serveur sans attendre (par exemple, lors d'un basculement d'urgence plutôt que d'un basculement progressif), envisagez également **KILL**.

#### KILL [db] {#kill-db}

Déconnecter immédiatement toutes les connexions clients et serveurs pour la base de données indiquée ou pour toutes les bases de données, en excluant la base de données d'administration.

Les nouvelles connexions clients vers une base de données arrêtée resteront en attente jusqu'à l'appel de **RESUME**.

#### KILL_CLIENT id {#kill_client-id}

Tuer immédiatement la connexion client spécifiée, ainsi que toutes les connexions serveur associées à ce client. Le client à tuer est identifié par la valeur `id`, qui peut être obtenue à l’aide de la commande `SHOW CLIENTS`.

Une commande d'exemple aura une forme semblable à `KILL_CLIENT 1234`.

#### SUSPENDRE {#suspend}

Tous les tampons de socket sont vidés et PgBouncer cesse d'écouter les données sur ceux-ci.
La commande ne retourne pas avant que tous les tampons soient vides. À utiliser lors d'un redémarrage en ligne de PgBouncer.

Les nouvelles connexions clients vers une base de données suspendue attendront jusqu'à l'appel de **RESUME**.

#### SYNTHÈSE [db] {#resume-db}

Reprendre le travail après une commande précédente **KILL**, **PAUSE** ou **SUSPEND**.

#### ARRÊT {#shutdown}

Le processus PgBouncer s'arrête.

#### SHUTDOWN WAIT_FOR_SERVERS {#shutdown-wait_for_servers}

Arrêtez d'accepter de nouvelles connexions et effectuez l'arrêt après la libération de tous les serveurs.
Cela revient essentiellement à émettre **PAUSE** et **SHUTDOWN**, sauf que cette commande arrête également l'acceptation de nouvelles connexions pendant l'attente du **PAUSE**, tout en déconnectant immédiatement les clients en attente d'une connexion serveur. Veuillez noter que les sockets UNIX resteront ouverts pendant l'arrêt, mais n'accepteront que les connexions à la console d'administration de PgBouncer.

#### SHUTDOWN WAIT_FOR_CLIENTS {#shutdown-wait_for_clients}

Arrêtez d'accepter de nouvelles connexions et arrêtez le processus une fois que tous les clients existants se sont déconnectés. Veuillez noter que les sockets UNIX resteront ouverts pendant l'arrêt, mais n'accepteront que les connexions à la console d'administration de pgbouncer. Cette commande peut être utilisée pour effectuer un redémarrage progressif sans interruption de deux processus PgBouncer en suivant la procédure suivante :

1. Faites fonctionner deux ou plusieurs processus PgBouncer sur le même port en utilisant `so_reuseport` ([configurer le peering](/fr/pgbouncer/config/#section-peers) est recommandé, mais non obligatoire). Pour obtenir une interruption nulle lors du redémarrage, redémarrez ces processus un par un, laissant ainsi les autres en cours d'exécution afin d'accepter les connexions pendant qu'un processus est redémarré.
2. Choisissez un processus à redémarrer en premier, appelons-le A.
3. Exécutez `SHUTDOWN WAIT_FOR_CLIENTS` (ou envoyez `SIGTERM`) au processus A.
4. Forcez tous les clients à se reconnecter. Cela peut être réalisé en attendant un certain temps jusqu'à ce que le pooler côté client provoque les reconnexions en raison de son `server_idle_timeout` (ou d'une configuration similaire). Sinon, si aucun pooler côté client n'est utilisé, cela peut être fait en redémarrant les clients. Une fois que tous les clients se sont reconnectés, le processus A s'arrêtera automatiquement, car aucun client ne sera plus connecté à celui-ci.
5. Redémarrez le processus A.
6. Répétez les étapes 3, 4 et 5 pour chacun des processus restants, un par un, jusqu'à ce que tous les processus aient été redémarrés.


#### RECHARGER {#reload}

Le processus PgBouncer recharge ses fichiers de configuration et met à jour les paramètres modifiables. Cela inclut le fichier de configuration principal ainsi que les fichiers spécifiés par les paramètres `auth_file` et `auth_hba_file`.

PgBouncer détecte lors d'un rechargement du fichier de configuration que les paramètres de connexion d'une définition de base de données ont changé. Une connexion serveur existante vers la destination ancienne sera fermée lors de sa prochaine libération (selon le mode de regroupement), et les nouvelles connexions serveur utiliseront immédiatement les paramètres de connexion mis à jour.

#### WAIT_CLOSE [db] {#wait_close-db}

Attendez que toutes les connexions serveur, pour la base de données spécifiée ou pour toutes les bases de données, aient quitté l’état "close_needed" (voir **SHOW SERVERS**). Cette commande peut être appelée après un **RECONNECT** ou un **RELOAD** pour attendre que le changement de configuration correspondant ait été pleinement activé, par exemple dans des scripts de basculement.

### Autres commandes {#other-commands}

#### SET key = arg {#set-key--arg}

Modifie un paramètre de configuration (voir également **SHOW CONFIG**). Par exemple :

    SET log_connections = 1;
    SET server_check_query = 'select 2';

(Remarque : cette commande est exécutée sur la console d'administration de PgBouncer et définit les paramètres de PgBouncer. Une commande **SET** exécutée sur une autre base de données sera transmise au serveur PostgreSQL comme toute autre commande SQL.)

### Signaux {#signals}

SIGHUP
:   Recharger la configuration. Équivalent à exécuter la commande **RELOAD** sur la console d'administration.

SIGTERM
:   Arrêt sécurisé maximal. Attend que tous les clients actifs se déconnectent, mais n'accepte plus de nouvelles connexions. Cela équivaut à émettre la commande **SHUTDOWN WAIT_FOR_CLIENTS** depuis la console d'administration. Si ce signal est reçu alors qu'un arrêt est déjà en cours, un « arrêt immédiat » est déclenché à la place d’un « arrêt sécurisé maximal ». Dans les versions de PgBouncer antérieures à 1.23.0, ce signal provoquait un « arrêt immédiat ».

SIGINT
:   Arrêt sécurisé. Équivalent à l’envoi de **SHUTDOWN WAIT_FOR_SERVERS** depuis la console.
    Si ce signal est reçu pendant qu’un arrêt est déjà en cours, un « arrêt immédiat » est déclenché au lieu d’un « arrêt sécurisé ».

SIGQUIT
:   Arrêt immédiat. Équivalent à l’envoi de **SHUTDOWN** depuis la console d'administration.

SIGUSR1
:   Identique à l'envoi de **PAUSE** depuis la console d'administration.

SIGUSR2
:   Identique à l'envoi de **RESUME** depuis la console d'administration.

### Paramètres Libevent {#libevent-settings}

Du document officiel de Libevent :

> Il est possible de désactiver la prise en charge d'epoll, kqueue, devpoll ou poll
> en définissant la variable d'environnement EVENT_NOEPOLL,
> EVENT_NOKQUEUE, EVENT_NODEVPOLL, EVENT_NOPOLL ou EVENT_NOSELECT,
> respectivement.
>
> En définissant la variable d'environnement EVENT_SHOW_METHOD, libevent
> affiche la méthode de notification du noyau qu'il utilise.

--------

## Voir aussi {#see-also}

pgBouncer(5) - page de manuel des descriptions des paramètres de configuration

<https://www.pgbouncer.org/>
