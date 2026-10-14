---
title: "12. Autres sections"
linkTitle: "12. Autres sections"
weight: 230
description: "Suivi, utilisateurs, courriels, erreurs, anneaux, certificats, ACME et contrôles d'état globaux"
icon: fa-solid fa-ellipsis
module: [HAPROXY]
categories: [Référence]
aliases:
  - /haproxy/configuration/other-sections/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 12"
---

Les sections décrites ci-dessous sont moins couramment utilisées et ne prennent généralement en charge qu'un petit nombre de paramètres. Il n'existe aucune relation implicite entre elles. Elles commencent toutes par un mot-clé unique. Aucune d'entre elles n'est autorisée avant une section « global ». Le support de certaines d'entre elles peut être conditionné par des options de compilation (par exemple, tout ce qui est lié au SSL).

## 12.1. Traces {#section-12-1}

À des fins de débogage, il est possible d’activer des traces sur un sous-système d’HAProxy. Cela permet d’afficher des messages de débogage relatifs à un sous-système spécifique. Il s’agit d’un outil très puissant pour diagnostiquer les problèmes. Les traces peuvent être configurées dynamiquement via l’interface CLI. Il est également possible de préconfigurer certaines options dans le fichier de configuration, dans des sections dédiées « traces ». Des informations complémentaires sur les traces sont disponibles dans le guide de gestion. Il s’agit d’un outil destiné aux développeurs, utilisé lors de sessions de débogage complexes. Il est très verbeux et coûteux en ressources, donc à utiliser avec précaution. En tant qu’outil destiné aux développeurs, aucune garantie de compatibilité descendante n’est assurée pour cette section.

<a id="entry-12-1-traces"></a>

**`traces`**

```haproxy
traces
```

Démarre une nouvelle section traces. Une ou plusieurs sections « traces » peuvent être utilisées. Toutes les directives sont évaluées dans l'ordre déclaré, les dernières remplaçant les précédentes.

<a id="entry-12-1-trace"></a>

**`trace <source> <args...>`**

```haproxy
trace <source> <args...>
```

Configure le sous-système « trace ». Chacun d’eux peut être trouvé dans le manuel de gestion et suit la même syntaxe exacte. Toute sortie que la commande « trace » produirait sera émise pendant l’étape d’analyse de la section. La plupart du temps, il s’agira d’erreurs et d’avertissements, mais certaines commandes incomplètes peuvent lister les choix autorisés. Cette commande n’est pas destinée à une utilisation régulière ; elle sera généralement proposée uniquement par les développeurs lors de sessions de débogage complexes. Il est important de garder à l’esprit que, selon le niveau de traçage et les détails activés, l’activation des traces peut fortement dégrader les performances globales. Veuillez vous référer au manuel de gestion pour la syntaxe des instructions.

Exemple :

```text
ring buf1
  size 10485760 # 10MB
  format timed
  backing-file /tmp/h1.traces

ring buf2
  size 10485760 # 10MB
  format timed
  backing-file /tmp/h2.traces

traces
  trace h1 sink buf1 level developer verbosity complete start now
  trace h2 sink buf1 level developer verbosity complete start now
```

## 12.2. Listes d'utilisateurs {#section-12-2}

Il est possible de contrôler l'accès aux sections frontend/backend/listen ou à l'interface http stats en n'autorisant que les utilisateurs authentifiés et autorisés. Pour cela, il est nécessaire de créer au moins une liste d'utilisateurs et de définir des utilisateurs.

<a id="entry-12-2-userlist"></a>

**`userlist <listname>`**

```haproxy
userlist <listname>
```

Crée une nouvelle liste d'utilisateurs nommée `<listname>`. Plusieurs listes d'utilisateurs indépendantes peuvent être utilisées pour stocker les données d'authentification et d'autorisation pour des clients indépendants.

<a id="entry-12-2-group"></a>

**`group <groupname> [users <user>,<user>,(...)]`**

```haproxy
group <groupname> [users <user>,<user>,(...)]
```

Ajoute le groupe `<groupname>` à la liste d'utilisateurs courante. Il est également possible d'attacher des utilisateurs à ce groupe en utilisant une liste séparée par des virgules de noms précédée du mot-clé « users ».

<a id="entry-12-2-user"></a>

**`user <username> [password|insecure-password <password>]`**

```haproxy
user <username> [password|insecure-password <password>]
                [groups <group>,<group>,(...)]
```

Ajoute l’utilisateur `<username>` à la liste d'utilisateurs courante. Les mots de passe sécurisés (chiffrés) et les mots de passe non sécurisés (non chiffrés) peuvent être utilisés. Les mots de passe chiffrés sont évalués à l’aide de la fonction crypt(3), ce qui implique que les algorithmes pris en charge dépendent des capacités du système. Par exemple, les systèmes Linux modernes basés sur Glibc prennent en charge MD5, SHA-256, SHA-512, ainsi que bien sûr la méthode classique basée sur DES pour le chiffrement des mots de passe.

Attention : l'utilisation de mots de passe chiffrés peut entraîner une augmentation significative de la charge CPU, selon le nombre de requêtes et l'algorithme utilisé. Pour chacune des variantes hachées, le mot de passe de chaque requête doit être traité par l'algorithme choisi avant de pouvoir être comparé à la valeur spécifiée dans le fichier de configuration. La plupart des algorithmes actuels sont délibérément conçus pour être coûteux à calculer afin de résister aux attaques par force brute. Ils ne se contentent pas de saler/hacher le mot de passe en clair une seule fois, mais le font des milliers de fois. Cela peut rapidement devenir un facteur majeur de la consommation CPU globale de HAProxy, et même entraîner des crashs d'applications !

Pour réduire l'utilisation élevée du processeur par les fonctions de hachage, une solution consiste à réduire le nombre d'itérations de la fonction de hachage (algorithmes de la famille SHA) ou à diminuer le « coût » de la fonction, si l'algorithme le permet.

En complément, les implémentations basées sur musl (par exemple, Alpine Linux) sont connues pour être plus lentes que leurs homologues glibc lors du calcul des hachages, vous devriez donc également prendre en compte cet aspect.

Tous les mots de passe sont considérés comme des arguments normaux et sont donc soumis à la section 2.2 [Citation et échappement](/fr/haproxy/configuration-basics/#section-2-2). Il est donc recommandé de citer les mots de passe entre guillemets simples.

Exemple :

```text
userlist L1
  group G1 users tiger,scott
  group G2 users xdb,scott

  user tiger password $6$k6y3o.eP$JlKBx9za9667qe4(...)xHSwRv6J.C0/D7cV91
  user scott insecure-password 'elgato'
  user xdb insecure-password 'hello'

userlist L2
  group G1
  group G2

  user tiger password $6$k6y3o.eP$JlKBx(...)xHSwRv6J.C0/D7cV91 groups G1
  user scott insecure-password 'elgato' groups G1,G2
  user xdb insecure-password 'hello' groups G2
```

Veuillez noter que les deux listes sont fonctionnellement identiques.

## 12.3. Mailers {#section-12-3}

Il est possible d'envoyer des alertes par courrier électronique lorsque l'état des serveurs change. Si les alertes par courrier électronique sont configurées, celles-ci sont envoyées à chaque serveur de messagerie défini dans une section *mailers*. Les courriers sont envoyés aux serveurs de messagerie via Lua (voir *examples/lua/mailers.lua*).

<a id="entry-12-3-mailers"></a>

**`mailers <mailersect>`**

```haproxy
mailers <mailersect>
```

Crée une nouvelle liste de messagerie nommée `<mailersect>`. Il s'agit d'une section indépendante référencée par un ou plusieurs proxies.

<a id="entry-12-3-mailer"></a>

**`mailer <mailername> <ip>:<port>`**

```haproxy
mailer <mailername> <ip>:<port>
```

Définit un serveur de messagerie dans une section mailers.

Exemple :

```text
global
    # mailers.lua file as provided in the git repository
    # adjust path as needed
    lua-load examples/lua/mailers.lua

mailers mymailers
    mailer smtp1 192.168.0.1:587
    mailer smtp2 192.168.0.2:587

backend mybackend
    mode tcp
    balance roundrobin

    email-alert mailers mymailers
    email-alert from test1@horms.org
    email-alert to test2@horms.org

    server srv1 192.168.0.30:80
    server srv2 192.168.0.31:80
```

<a id="entry-12-3-timeout-mail"></a>

**`timeout mail <time>`**

```haproxy
timeout mail <time>
```

Définit le délai disponible pour établir une connexion mail et envoyer les données au serveur de messagerie. Si ce paramètre n'est pas défini, la valeur par défaut est de 10 secondes. Pour permettre l'envoi d'au moins deux paquets SYN-ACK pendant la négociation TCP initiale, il est recommandé de maintenir cette valeur au-dessus de 4 secondes.

Exemple :

```text
mailers mymailers
    timeout mail 20s
    mailer smtp1 192.168.0.1:587
```

## 12.4. Erreurs HTTP {#section-12-4}

Il est possible de déclarer globalement plusieurs groupes d'erreurs HTTP, pouvant être importés ultérieurement dans n'importe quelle section proxy. Un même groupe peut être référencé à plusieurs endroits et être importé entièrement ou partiellement.

<a id="entry-12-4-http-errors"></a>

**`http-errors <name>`**

```haproxy
http-errors <name>
```

Crée un nouveau groupe d'erreurs HTTP nommé `<name>`. Il s'agit d'une section indépendante pouvant être référencée par un ou plusieurs proxies à l'aide de son nom.

<a id="entry-12-4-errorfile"></a>

**`errorfile <code> <file>`**

```haproxy
errorfile <code> <file>
```

Associer le contenu d’un fichier à un code d’erreur HTTP

Arguments :

```text
<code>    est le code d'état HTTP. HAProxy peut actuellement produire
          les codes 200, 400, 401, 403, 404, 405, 407, 408, 410,
          425, 429, 500, 501, 502, 503 et 504.

<file>    désigne un fichier contenant la réponse HTTP complète.
          Il est recommandé d'ajouter l'extension ".http" au nom du
          fichier pour éviter de confondre la réponse avec une page
          d'erreur HTML, et d'utiliser un chemin absolu : les fichiers
          sont lus avant l'exécution de tout chroot.
```

Veuillez vous référer à la directive « errorfile » dans la section [4](/fr/haproxy/proxies/) pour plus de détails.

Exemple :

```text
http-errors website-1
    errorfile 400 /etc/haproxy/errorfiles/site1/400.http
    errorfile 404 /etc/haproxy/errorfiles/site1/404.http
    errorfile 408 /dev/null  # work around Chrome pre-connect bug

http-errors website-2
    errorfile 400 /etc/haproxy/errorfiles/site2/400.http
    errorfile 404 /etc/haproxy/errorfiles/site2/404.http
    errorfile 408 /dev/null  # work around Chrome pre-connect bug
```

## 12.5. Anneaux {#section-12-5}

Il est possible de déclarer globalement des tampons anneau, destinés à être utilisés comme cible pour les serveurs de journaux ou les traces.

<a id="entry-12-5-ring"></a>

**`ring <ringname>`**

```haproxy
ring <ringname>
```

Crée un nouveau tampon anneau nommé `<ringname>`.

<a id="entry-12-5-backing-file"></a>

**`backing-file <path>`**

```haproxy
backing-file <path>
```

Cela remplace l'allocation mémoire régulière par un fichier mappé en mémoire RAM pour stocker l'anneau. Cela peut être utile pour collecter des traces ou des journaux destinés à une analyse post-mortem, sans avoir à connecter un client lent à l'interface CLI. Les nouveaux contenus remplacent automatiquement les anciens, de sorte que les derniers contenus sont toujours disponibles. Les contenus écrits dans l'anneau deviennent visibles dans ce fichier une fois le processus arrêté (ils peuvent même apparaître très rapidement, mais aucune garantie n'est donnée, car les écritures ne sont pas synchrones).

Lorsque cette option est utilisée, la taille totale de l’espace de stockage est réduite de la taille du « struct ring » qui commence au début de la zone et qui est nécessaire pour récupérer le contenu de celle-ci. Le fichier sera créé avec les droits du propriétaire initial, avec les permissions 0600, et de la taille configurée par la directive « size ». Lors de l’analyse de la directive (donc même pendant les vérifications de configuration), tout fichier existant non vide sera renommé en ajoutant le suffixe ".bak", et tout fichier existant précédemment avec le suffixe ".bak" sera supprimé. Cela garantit qu’un rechargement instantané ou un redémarrage du processus ne supprimera pas d’informations de débogage précieuses, et laissera à l’administrateur le temps de repérer ce nouveau fichier ".bak" et de l’archiver si nécessaire. Ainsi, après une panne, le fichier désigné par `<path>` contiendra les informations les plus récentes, et si le service est redémarré, le fichier "`<path>`.bak" les contiendra à la place. Cela signifie que la capacité de stockage totale requise sera le double de la taille de l’anneau. Les échecs de rotation du fichier sont ignorés silencieusement, de sorte que placer le fichier dans un répertoire sans permissions d’écriture suffira à empêcher la création du fichier de sauvegarde si cela n’est pas souhaité.

AVERTISSEMENT : l'utilisation de cette fonctionnalité comporte des implications en matière de stabilité et de sécurité. Premièrement, la sauvegarde de l'anneau sur un périphérique lent (par exemple, un disque dur physique) peut entraîner des ralentissements perceptibles lors des accès, voire même des panics si trop de threads entrent en concurrence pour les accès. Deuxièmement, une modification de la zone par un processus externe peut provoquer la panne du processus HAProxy ou l'écrasement de certaines parties de sa propre mémoire par des traces. Troisièmement, si le système de fichiers est plein avant l'anneau, les écritures dans l'anneau peuvent provoquer la panne du processus.

Les informations présentes dans cet anneau sont structurées et ne sont PAS directement lisibles à l’aide d’un éditeur de texte (même si la majeure partie d’entre elles semble à peine lisible). La sortie de ce fichier est destinée uniquement aux développeurs.

<a id="entry-12-5-description"></a>

**`description <text>`**

```haproxy
description <text>
```

La description est une chaîne de caractères facultative décrivant l'anneau. Elle s'affiche en ligne de commande. Par défaut, `<name>` est réutilisé pour remplir ce champ.

<a id="entry-12-5-format"></a>

**`format <format>`**

```haproxy
format <format>
```

Format utilisé pour stocker les événements dans le tampon anneau.

Arguments :

```text
<format> est le format utilisé pour produire les messages syslog.
         Il peut prendre l'une des valeurs suivantes :

  iso     Message contenant uniquement la date ISO suivie du texte.
          Le PID, le nom du processus et le nom du système sont omis.
          Ce format est destiné à un serveur de journaux local.

  local   Comme le format syslog rfc3164, sans le champ du nom d'hôte.
          C'est la valeur par défaut.
          Note : "log-send-hostname" remplace cette valeur par défaut
          par rfc3164.

  raw     Message contenant uniquement le texte. Le niveau, le PID,
          la date, l'heure, le nom du processus et celui du système
          sont omis. Ce format est destiné aux conteneurs ou au
          développement, où la sévérité dépend uniquement du
          descripteur utilisé (stdout/stderr). C'est la valeur par défaut.

  rfc3164 Format de message syslog RFC3164.
          (https://tools.ietf.org/html/rfc3164)

  rfc5424 Format de message syslog RFC5424.
          (https://tools.ietf.org/html/rfc5424)

  short   Message contenant uniquement un niveau entre chevrons tel
          que '<3>', suivi du texte. Le PID, la date, l'heure, le nom
          du processus et celui du système sont omis. Ce format est
          destiné à un serveur de journaux local et est compatible
          avec le journaliseur systemd.

 priority Message contenant uniquement un niveau et une catégorie syslog
          entre chevrons tels que '<63>', suivis du texte. Le PID, la date,
          l'heure, le nom du processus et celui du système sont omis.
          Ce format est destiné à un serveur de journaux local.

  timed   Message contenant uniquement un niveau entre chevrons tel
          que '<3>', suivi de la date ISO et du texte. Le PID, le nom
          du processus et celui du système sont omis. Ce format est
          destiné à un serveur de journaux local.
```

<a id="entry-12-5-maxlen"></a>

**`maxlen <length>`**

```haproxy
maxlen <length>
```

La longueur maximale d'un message d'événement stocké dans l'anneau, y compris l'en-tête formaté. Si un message d'événement est plus long que `<length>`, il sera tronqué à cette longueur.

<a id="entry-12-5-server"></a>

**`server <name> <address> [param*]`**

```haproxy
server <name> <address> [param*]
```

Utilisé pour configurer un serveur syslog TCP afin d'envoyer les messages provenant du tampon circulaire. Cela prend en charge tous les paramètres « server » décrits au paragraphe 5.2. Certains de ces paramètres sont sans effet dans les sections « ring ». Point important : il n'y a peu de raisons d'ajouter plus d'un serveur à un tampon, car tous les serveurs reçoivent une copie identique du contenu du tampon, et le tampon progresse donc à la vitesse du serveur le plus lent. Si un serveur ne répond pas, il empêche la suppression des anciens messages et peut bloquer l'insertion de nouveaux messages dans le tampon. La manière correcte d'envoyer des messages à plusieurs serveurs consiste à utiliser un tampon distinct par serveur de journalisation, et non à attacher plusieurs serveurs au même tampon. Notez que la directive spécifique « log-proto » est utilisée pour définir le protocole utilisé pour envoyer les messages.

<a id="entry-12-5-size"></a>

**`size <size>`**

```haproxy
size <size>
```

Ce paramètre indique la taille facultative, en octets, du tampon anneau. La valeur par défaut est définie à BUFSIZE.

<a id="entry-12-5-timeout-connect"></a>

**`timeout connect <timeout>`**

```haproxy
timeout connect <timeout>
```

Définir le temps maximal d'attente pour qu'une tentative de connexion à un serveur aboutisse.

Arguments :

```text
<timeout> est le délai d'expiration, en millisecondes par défaut. Une autre
          unité peut être utilisée si son suffixe suit le nombre, comme
          expliqué au début de ce document.
```

<a id="entry-12-5-timeout-server"></a>

**`timeout server <timeout>`**

```haproxy
timeout server <timeout>
```

Définir le temps maximal pendant lequel les données en attente restent dans le tampon de sortie.

Arguments :

```text
<timeout> est le délai d'expiration, en millisecondes par défaut. Une autre
          unité peut être utilisée si son suffixe suit le nombre, comme
          expliqué au début de ce document.
```

Exemple :

```text
global
    log ring@myring local7

ring myring
    description "My local buffer"
    format rfc5424
    maxlen 1200
    size 32764
    timeout connect 5s
    timeout server 10s
    server mysyslogsrv 127.0.0.1:6514 log-proto octet-count
```

## 12.6. Transmission des journaux {#section-12-6}

Il est possible de déclarer une ou plusieurs sections de transfert de journaux ; HAProxy transmettra tous les messages de journal reçus à une liste de serveurs de journaux.

<a id="entry-12-6-log-forward"></a>

**`log-forward <name>`**

```haproxy
log-forward <name>
```

Crée un nouveau proxy de transfert de journaux identifié par `<name>`.

<a id="entry-12-6-backlog"></a>

**`backlog <conns>`**

```haproxy
backlog <conns>
```

Indiquez des indices au système concernant la taille approximative du tampon d'écoute souhaitée pour les connexions acceptées.

<a id="entry-12-6-bind"></a>

**`bind <addr> [param*]`**

```haproxy
bind <addr> [param*]
```

Utilisé pour configurer un écouteur de journalisation en flux afin de recevoir les messages à acheminer. Cela prend en charge les paramètres « bind » décrits au paragraphe 5.1, y compris ceux concernant le ssl, mais certaines directives telles que « alpn » peuvent être sans pertinence pour le protocole syslog sur TCP. Ces écouteurs prennent en charge les deux modes « Comptage d'octets » et « Encadrement non transparent » tels que définis dans le rfc-6587.

<a id="entry-12-6-dgram-bind"></a>

**`dgram-bind <addr> [param*]`**

```haproxy
dgram-bind <addr> [param*]
```

Utilisé pour configurer un écouteur de journalisation de datagrammes afin de recevoir les messages à acheminer. Les adresses doivent être au format IPv4 ou IPv6, suivies d'un port. Cette option prend en charge certains paramètres « bind » présents dans le paragraphe 5.1, notamment « interface », « namespace » ou « transparent », les autres étant ignorés silencieusement car sans pertinence dans le cas UDP/syslog.

<a id="entry-12-6-log-global"></a>

**`log global`**

```haproxy
log global
log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]
    <facility> [<level> [<minlevel>]]
```

Utilisé pour configurer les serveurs de journalisation cibles. Voir les détails supplémentaires dans la documentation des proxies. Si aucun format n'est spécifié, HAProxy tente de conserver le format de journalisation entrant. La facility configurée est ignorée, sauf si le message entrant ne présente pas de facility alors qu'une facility est obligatoire dans le format sortant. Si aucun horodatage n'est disponible dans le format d'entrée, mais que le champ existe dans le format de sortie, HAProxy utilisera la date locale.

Exemple :

```text
global
   log stderr format iso local7

ring myring
    description "My local buffer"
    format rfc5424
    maxlen 1200
    size 32764
    timeout connect 5s
    timeout server 10s
    # syslog tcp server
    server mysyslogsrv 127.0.0.1:514 log-proto octet-count

log-forward sylog-loadb
    dgram-bind 127.0.0.1:1514
    bind 127.0.0.1:1514
    # all messages on stderr
    log global
    # all messages on local tcp syslog server
    log ring@myring local0
    # load balance messages on 4 udp syslog servers
    log 127.0.0.1:10001 sample 1:4 local0
    log 127.0.0.1:10002 sample 2:4 local0
    log 127.0.0.1:10003 sample 3:4 local0
    log 127.0.0.1:10004 sample 4:4 local0
```

<a id="entry-12-6-maxconn"></a>

**`maxconn <conns>`**

```haproxy
maxconn <conns>
```

Fixer le nombre maximum de connexions simultanées sur un forwarder de journaux. 10 est la valeur par défaut.

<a id="entry-12-6-timeout-client"></a>

**`timeout client <timeout>`**

```haproxy
timeout client <timeout>
```

Définir le délai maximal d'inactivité du côté client.

<a id="entry-12-6-option-assume-rfc6587-ntf"></a>

**`option assume-rfc6587-ntf`**

```haproxy
option assume-rfc6587-ntf
```

Force HAProxy à traiter les flux de journaux TCP entrants comme utilisant toujours un encadrement non transparent. Cette option simplifie la logique d'encadrement et garantit un traitement cohérent des messages, ce qui est particulièrement utile lors de la gestion de caractères de départ mal formés.

<a id="entry-12-6-option-dont-parse-log"></a>

**`option dont-parse-log`**

```haproxy
option dont-parse-log
```

Active la capacité de HAProxy à acheminer des messages syslog sans tenter de les analyser ni de les reformater, ce qui est utile pour acheminer des messages pouvant ne pas respecter les formats traditionnels. Cette option devrait être utilisée avec le paramètre format raw sur les cibles de journalisation de destination afin de garantir la préservation du contenu original du message.

<a id="entry-12-6-option-host"></a>

**`option host { replace | fill | keep | append }`**

```haproxy
option host { replace | fill | keep | append }
```

Définir la stratégie d'hôte à utiliser dans la section log-forward concernant le champ nom d'hôte syslog
pour les messages sortants au format rfc3164 ou rfc5424.

      replace Si le message d'entrée contient déjà une valeur pour le champ hostname,
      elle est remplacée par l'adresse IP source de l'expéditeur.
      Si le message d'entrée ne contient pas de valeur pour le champ hostname
      (par exemple : '-' dans un message rfc5424, ou un message non conforme rfc3164 ou rfc5424),
      l'adresse IP source de l'expéditeur est utilisée comme valeur du champ hostname.

      fill    Si le message d'entrée contient déjà une valeur pour le champ hostname,
              nous la conservons.
              Si le message d'entrée ne contient pas de valeur pour le champ hostname
              (par exemple : '-' dans un message rfc5424 ou un message non conforme rfc3164 ou rfc5424),
              nous utilisons l'adresse IP source de l'expéditeur comme valeur du champ hostname.
              (Ceci est la valeur par défaut)

      keep    Si le message d'entrée contient déjà une valeur pour le champ hostname,
              nous la conservons.
              Si le message d'entrée ne contient pas de valeur pour le champ hostname,
              nous la définissons sur « localhost » (rfc3164) ou « - » (rfc5424).

      append  Si le message d'entrée contient déjà une valeur pour le champ hostname,
              nous ajoutons une virgule suivie de l'adresse IP de l'expéditeur.
              Si le message d'entrée ne contient pas de valeur pour le champ hostname,
              nous utilisons l'adresse IP source de l'expéditeur.

Pour toutes les options ci-dessus, si l'adresse IP source de l'expéditeur n'est pas disponible (par exemple : socket UNIX/ABNS), la stratégie résultante est « keep ».

Notez que cette option n'est pertinente que pour les formats de journalisation de destination rfc3164 ou rfc5424. Dans les autres cas, son réglage n'aura aucun effet visible.

## 12.7. Stockage des certificats {#section-12-7}

HAProxy utilise un mécanisme de stockage interne pour charger et stocker les certificats utilisés dans la configuration.
Ce stockage peut être configuré à l’aide d’une section « crt-store ». Elle permet de définir des certificats et les fichiers à charger dans ce stockage. Une définition de certificat doit être écrite avant d’être utilisée ailleurs dans la configuration.

crt-store [`<name>`]

Le paramètre « crt-store » accepte un nom facultatif en argument. Si un nom est spécifié, chaque certificat de ce magasin doit être référencé à l’aide de « @`<name>`/`<crt>` » ou de « @`<name>`/`<alias>` ».

Les fichiers du magasin de certificats peuvent également être mis à jour dynamiquement via l'interface CLI. Voir « set ssl cert » dans la section [9.3](/fr/haproxy/statistics-and-monitoring/#section-9-3) du guide d'administration.

Les mots-clés suivants sont pris en charge dans la section « crt-store » :

- crt-base
- key-base
- load

<a id="entry-12-7-crt-base"></a>

**`crt-base <dir>`**

```haproxy
crt-base <dir>
```

Attribue un répertoire par défaut pour récupérer les certificats SSL lorsqu’un chemin relatif est utilisé avec les directives « crt ». Les emplacements absolus spécifiés prennent priorité et ignorent « crt-base ». Lorsqu’il est utilisé dans un bloc « crt-store », le paramètre « crt-base » de la section globale est ignoré.

<a id="entry-12-7-key-base"></a>

**`key-base <dir>`**

```haproxy
key-base <dir>
```

Attribue un répertoire par défaut pour récupérer les clés privées SSL lorsque des chemins relatifs sont utilisés avec les directives « key ». Les emplacements absolus spécifiés ont priorité et ignorent « key-base ». Lorsqu'il est utilisé dans un crt-store, la valeur « key-base » de la section globale est ignorée.

<a id="entry-12-7-load"></a>

**`load [crt <filename>] [param*]`**

```haproxy
load [crt <filename>] [param*]
```

Charger les fichiers SSL dans le magasin de certificats. Pour la liste des paramètres, voir la section « 12.7.1. Options de chargement ».

Exemple :

```text
crt-store
    load crt "site1.crt" key "site1.key" ocsp "site1.ocsp" alias "site1"
    load crt "site2.crt" key "site2.key"

frontend in2
    bind *:443 ssl crt "@/site1" crt "site2.crt"

crt-store web
    crt-base /etc/ssl/certs/
    key-base /etc/ssl/private/
    load crt "site3.crt" alias "site3"
    load crt "site4.crt" key "site4.key"

frontend in2
    bind *:443 ssl crt "@/site1" crt "site2.crt"  crt "@web/site3" crt "@web/site4.crt"
```

### 12.7.1. Options de chargement {#section-12-7-1}

Charger les fichiers SSL dans le magasin de certificats. Le mot-clé load peut accepter plusieurs paramètres, listés ci-dessous. Ces mots-clés sont également utilisables dans un crt-list.

<a id="entry-12-7-1-crt"></a>

**`crt <filename>`**

```haproxy
crt <filename>
```

Cet argument est obligatoire ; il charge un fichier PEM qui doit contenir le certificat public, mais peut également inclure les certificats intermédiaires et la clé privée. Si aucune clé privée n’est fournie dans ce fichier, une clé peut être spécifiée à l’aide du mot-clé « key ».

<a id="entry-12-7-1-acme"></a>

**`acme <string>`**

```haproxy
acme <string>
```

Cette option permet de configurer le protocole ACME pour un certificat donné. Il s'agit d'une fonctionnalité expérimentale qui nécessite la présence du mot-clé « expose-experimental-directives » dans la section globale.

Lorsqu’on utilise le mot-clé « acme » dans un crt-store, il est possible de démarrer sans certificat existant sur le disque. Une paire de clés temporaire sera alors utilisée jusqu’à la génération du certificat ACME. Ce comportement est propre aux crt-store ; ni une ligne crt-list ni une ligne ssl-f-use ne peuvent produire le même résultat sans avoir déclaré au préalable un crt-store.

Voir également [Section 12.8](/fr/haproxy/other-sections/#section-12-8) ("ACME") et « domains » dans cette section.

<a id="entry-12-7-1-alias"></a>

**`alias <string>`**

```haproxy
alias <string>
```

Argument facultatif. Permet de nommer le certificat avec un alias, afin de pouvoir le référencer par ce dernier dans la configuration. Un alias doit être précédé de '@/' lorsqu'il est appelé ailleurs dans la configuration.

<a id="entry-12-7-1-domains"></a>

**`domains <string>`**

```haproxy
domains <string>
```

Configurez la liste des domaines utilisés pour les certificats ACME. Le premier domaine de la liste est utilisé comme CN. Les domaines sont séparés par des virgules dans la liste.

Voir également [Section 12.8](/fr/haproxy/other-sections/#section-12-8) ("ACME") et « acme » dans cette section.

Exemple :

```text
load crt "example.com.pem" acme LE domains "bar.example.com,foo.example.com"
```

<a id="entry-12-7-1-ips"></a>

**`ips <string>`**

```haproxy
ips <string>
```

Configurez la liste des adresses IP à inclure en tant que SAN IP dans le certificat ACME. Les adresses IP sont séparées par des virgules dans la liste.

La génération d’un certificat avec des adresses IP peut nécessiter l’utilisation du profil « shortlived ».

Voir également [Section 12.8](/fr/haproxy/other-sections/#section-12-8) ("ACME"), les champs « acme » et « domains » dans cette section.

Exemple :

```text
load crt "server.pem" acme LE ips "192.0.2.1,2001:db8::1"
```

<a id="entry-12-7-1-key"></a>

**`key <filename>`**

```haproxy
key <filename>
```

Cet argument est facultatif. Chargez une clé privée au format PEM. Si une clé privée était déjà définie dans « crt », elle sera remplacée.

<a id="entry-12-7-1-ocsp"></a>

**`ocsp <filename>`**

```haproxy
ocsp <filename>
```

Cet argument est facultatif ; il charge une réponse OCSP au format DER. Il peut être mis à jour via l'interface en ligne de commande.

<a id="entry-12-7-1-issuer"></a>

**`issuer <filename>`**

```haproxy
issuer <filename>
```

Cet argument est facultatif. Chargez l'émetteur OCSP au format PEM. Pour identifier quel certificat une réponse OCSP concerne, le certificat de l'émetteur est nécessaire. Si le certificat de l'émetteur n'est pas trouvé dans le fichier « crt », il peut être chargé à partir d'un fichier avec cet argument.

<a id="entry-12-7-1-sctl"></a>

**`sctl <filename>`**

```haproxy
sctl <filename>
```

Cet argument est facultatif. Le support de l’extension TLS Certificate Transparency (RFC6962) est activé.
Le fichier doit contenir une liste valide de timestamps de certificat signés, comme décrit dans la RFC. Le fichier est analysé pour vérifier la syntaxe de base, mais aucune signature n’est vérifiée.

<a id="entry-12-7-1-ocsp-update"></a>

**`ocsp-update [ off | on ]`**

```haproxy
ocsp-update [ off | on ]
```

Active la mise à jour automatique de la réponse OCSP lorsqu'elle est définie sur « on », désactive-la sinon. Sa valeur par défaut est « off ». Pour activer la mise à jour automatique OCSP sur une ligne bind, vous pouvez utiliser cette option dans un crt-store ou utiliser l'option globale "tune.ocsp-update.mode". Si un certificat donné est utilisé dans plusieurs crt-lists avec des valeurs différentes pour l'option « ocsp-update », une erreur sera générée. De même, si un certificat hérite de l'option globale sur une ligne bind et qu'une option explicite « ocsp-update » incompatible est définie dans un crt-list, la même erreur sera générée.

Exemples :

Voici une configuration exemple permettant de l’activer avec un crt-list :

haproxy.cfg:

```text
frontend fe
    bind :443 ssl crt-list haproxy.list
```

haproxy.list:

```text
server_cert.pem [ocsp-update on] foo.bar
```

Voici une configuration exemple permettant de l’activer avec un crt-store :

haproxy.cfg:

```text
crt-store
  load crt foobar.pem ocsp-update on

frontend fe
    bind :443 ssl crt foobar.pem
```

Lorsque cette option est définie sur « on », une réponse OCSP est tentée à chaque fois qu’une URI OCSP est trouvée dans le certificat du frontal. La seule limitation de ce mode est que l’émetteur du certificat doit être connu afin de construire le certid OCSP. Chaque réponse OCSP sera mise à jour au moins une fois par heure, et plus fréquemment encore si la date d’expiration d’une réponse OCSP est antérieure à cette limite d’une heure. Un intervalle minimum de mise à jour de 5 minutes est toujours respecté afin d’éviter de mettre à jour trop fréquemment des réponses dont la durée de validité est très courte, voire sans champ « Next Update ». En raison de cette limite stricte, veuillez noter qu’en cas de mise à jour automatique activée sur « on », toute réponse OCSP chargée lors de l’initialisation ne sera pas mise à jour avant au moins 5 minutes, même si sa date d’expiration est antérieure à now+5m. Cela ne devrait pas poser de problème majeur, car une réponse OCSP doit être valide au moment du chargement lors de l’initialisation (sa date d’expiration doit être dans le futur), si bien qu’il est peu probable qu’elle expire si rapidement après l’initialisation. En revanche, si un certificat contient une URI OCSP mais aucune réponse OCSP, définir cette option sur « on » pour ce certificat garantira que la réponse OCSP sera automatiquement récupérée juste après l’initialisation. Les délais minimum et maximum par défaut (5 minutes et 1 heure respectivement) peuvent être configurés à l’aide des options globales "ocsp-update.maxdelay" et "ocsp-update.mindelay".

Lorsqu'une réponse OCSP est mise à jour par la tâche de mise à jour automatique ou après un appel à la commande CLI « update ssl ocsp-response », une ligne de journalisation dédiée est émise. Elle suit un format dédié contenant l'en-tête "`<OCSP-UPDATE>`" et est suivie d'informations spécifiques liées à OCSP :   - le chemin du certificat frontal correspondant   - un statut de mise à jour numérique   - un statut de mise à jour textuel   - le nombre d'échecs de mise à jour pour la réponse donnée   - le nombre de succès de mise à jour pour la réponse donnée

Voir la commande CLI « show ssl ocsp-updates » pour la liste complète des codes d'erreur et des messages d'erreur. Cette ligne est émise indépendamment du succès ou de l'échec de la mise à jour de la réponse OCSP concernée. La requête/réponse OCSP est envoyée et reçue via une instance http_client ayant l'option dontlog-normal activée et utilisant le format de journalisation HTTP régulier en cas d'erreur (par exemple, répondeur OCSP inatteignable). Si une telle erreur se produit, une autre ligne de journalisation contenant des informations HTTP sera émise en parallèle de la ligne « normale » OCSP (qui comportera probablement « HTTP error » comme statut textuel). Toutefois, si une erreur purement HTTP survient (par exemple, répondeur OCSP inatteignable), une ligne de journalisation supplémentaire suivant le format HTTP régulier sera émise. Voici deux exemples de telles lignes de journalisation, avec d'abord une ligne de journalisation de mise à jour OCSP réussie, puis un exemple d'erreur HTTP avec les deux lignes différentes (les lignes ont été divisées et l'URL raccourcie pour plus de lisibilité) :

```text
<133>Mar  6 11:16:53 haproxy[14872]: <OCSP-UPDATE> /path_to_cert/foo.pem 1 \
        "Update successful" 0 1

<133>Mar  6 11:18:55 haproxy[14872]: <OCSP-UPDATE> /path_to_cert/bar.pem 2 \
        "HTTP error" 1 0
<133>Mar  6 11:18:55 haproxy[14872]: -:- [06/Mar/2023:11:18:52.200] \
        <OCSP-UPDATE> -/- 2/0/-1/-1/3009 503 217 - - SC-- 0/0/0/0/3 0/0 {} \
        "GET http://127.0.0.1:12345/MEMwQT HTTP/1.1"
```

Dépannage : Une erreur courante pouvant survenir avec les certificats Let's Encrypt est due à une résolution DNS qui fournit une adresse IPv6, alors que votre système ne dispose pas de route sortante IPv6 valide. Dans ce cas, vous pouvez soit créer la route appropriée, soit définir l'option « httpclient.resolvers.prefer ipv4 » dans la section globale. En cas d'erreur « échec de vérification de la réponse OCSP », vérifiez que le certificat émetteur que vous avez fourni est valide. Un message d'erreur plus précis peut également être affiché entre parenthèses après le message d'erreur générique. Cela peut se produire pour les erreurs « échec de vérification de la réponse OCSP » ou « erreur lors de l'insertion ».

<a id="entry-12-7-1-jwt"></a>

**`jwt [ off | on ]`**

```haproxy
jwt [ off | on ]
```

Permettre l'utilisation de ce certificat pour la validation ou le déchiffrement JWT via les convertisseurs "jwt_verify_cert", "jwt_decrypt_cert" ou "jwt_decrypt" lorsque cette option est définie sur « on ». Sa valeur par défaut est « off ».

Lorsqu’il est défini sur « on » pour un certificat donné, la commande CLI « del ssl cert » ne fonctionnera pas. Pour être supprimé, un certificat doit ne pas être utilisé, ni pour les échanges SSL, ni pour la validation JWT.

Cette option peut être modifiée en temps réel à l’aide des commandes CLI « add ssl jwt » et « del ssl jwt ». Voir également la commande CLI « show ssl jwt ».

<a id="entry-12-7-1-generate-dummy"></a>

**`generate-dummy [ off | on ]`**

```haproxy
generate-dummy [ off | on ]
```

Permet la génération d'une clé privée et de son certificat auto-signé au moment de l'analyse lorsque cette option est définie sur « on ». Cela peut être utile si aucun certificat n'est disponible pendant la phase de test, par exemple. Dans ce cas, les options « keytype », « bits » et « curves » peuvent être utilisées pour personnaliser la clé privée. Lorsqu'elle n'est pas utilisée, la valeur par défaut est « off ». (voir également « keytype », « bits » et « curves »).

<a id="entry-12-7-1-keytype"></a>

**`keytype [ RSA | ECDSA ]`**

```haproxy
keytype [ RSA | ECDSA ]
```

Permet la sélection du type de clé privée utilisé pour générer, au moment de l'analyse, un certificat auto-signé. Cela s'applique lorsque « generate-dummy » est défini sur « on » pour ce certificat. En l'absence d'utilisation, la valeur par défaut est « RSA ». (voir également « generate-dummy »).

<a id="entry-12-7-1-bits"></a>

**`bits <number>`**

```haproxy
bits <number>
```

Configurez le nombre de bits à générer pour un certificat auto-signé RSA lorsque « generate-dummy » est défini sur « on » pour ce certificat auto-signé et que « keytype » est défini sur « RSA ». En l'absence d'utilisation, la valeur par défaut est 2048. (voir également « generate-dummy »).

<a id="entry-12-7-1-curves"></a>

**`curves <string>`**

```haproxy
curves <string>
```

Configurez les courbes lorsque « generate-dummy » est défini sur « on » et que « keytype » est défini sur « ECDSA » pour ce certificat auto-signé. La valeur par défaut est « P-384 ».

## 12.8. ACME {#section-12-8}

acme `<name>`

Le protocole ACME peut être configuré à l'aide de la section « acme ». Cette section prend un argument "`<name>`", utilisé pour lier un certificat à la section.

La section ACME permet de configurer HAProxy en tant que client ACMEv2. Cette fonctionnalité est expérimentale, ce qui signifie que « expose-experimental-directives » doit être présent dans la section global pour pouvoir l'utiliser.

Un guide est disponible sur le wiki HAProxy
<https://github.com/haproxy/wiki/wiki/ACME:--native-haproxy>

Limitations actuelles : <a id="entry-12-8-the-feature-is"></a>

**`- Cette fonctionnalité est limitée aux challenges http-01, dns-01 ou dns-persist-01`**

```haproxy
- Cette fonctionnalité est limitée aux challenges http-01, dns-01 ou dns-persist-01
```

Pour l'instant, l'authentification http-01 est entièrement gérée par HAProxy, mais les méthodes dns-01 et dns-persist-01 nécessitent soit le dataplaneAPI, soit un autre outil tiers pour communiquer avec une API de fournisseur DNS. dns-persist-01 n'exige qu'une seule configuration de l'entrée TXT, qui peut donc être définie manuellement sans outil.
<a id="entry-12-8-it-is-possible"></a>

**`- Il est possible de démarrer sans certificat existant sur le disque. Pour cela`**

```haproxy
- Il est possible de démarrer sans certificat existant sur le disque. Pour cela
```

Ainsi, le certificat doit être configuré dans un magasin de certificats (crt-store). Lorsqu’on utilise le mot-clé « acme » dans un crt-store, une paire de clés temporaire sera utilisée jusqu’à la génération du certificat ACME.
<a id="entry-12-8-the-current-haproxy"></a>

**`- L'architecture actuelle de HAProxy est non bloquante ; l'accès au disque`**

```haproxy
- L'architecture actuelle de HAProxy est non bloquante ; l'accès au disque
```

n'est pas censé être effectué après le chargement de la configuration, car cela pourrait bloquer la boucle d'événements,
bloquant ainsi le trafic sur le même thread. Cela signifie que les certificats et clés générés par
HAProxy devront être extraits depuis l'extérieur de HAProxy en utilisant la commande « dump ssl cert » sur le socket de statistiques. Il est possible d'automatiser l'extraction des certificats en utilisant le dataplaneAPI ou le script haproxy-dump-certs fourni dans le répertoire admin/cli/.

Le planificateur ACME démarre au démarrage de HAProxy. Il parcourt les certificats et lance une tâche de renouvellement ACME lorsque la date notAfter est passée de curtime + (notAfter - notBefore) / 12, ou 7 jours si notBefore n’est pas défini. Le planificateur s’endort ensuite et se réveille après 12 heures. Il est possible de lancer manuellement une tâche de renouvellement avec la commande « acme renew ». Voir également « acme status » dans le guide d’administration.

Les mots-clés suivants sont utilisables dans la section ACME :

<a id="entry-12-8-account-key"></a>

**`account-key <filename>`**

```haproxy
account-key <filename>
```

Configurez le chemin vers la clé du compte. La clé doit être générée avant le lancement de HAProxy. Si le mot-clé account n'est pas utilisé, la section acme tentera de charger un fichier en utilisant le nom de la section "`<name>`.account.key". Si le fichier n'existe pas, HAProxy en générera un, en utilisant les paramètres de la section acme.

Vous pouvez également générer manuellement une clé privée RSA avec OpenSSL :

```text
openssl genrsa -out account.key 2048
```

Ou une clé ecdsa :

```text
openssl ecparam -name secp384r1 -genkey -noout -out account.key
```

<a id="entry-12-8-acme-vars"></a>

**`acme-vars <string>`**

```haproxy
acme-vars <string>
```

Passer des variables arbitraires à l'outil externe de provisionnement DNS (par exemple, le dataplaneAPI) via le réceptacle « dpapi ». Les sémantiques sont spécifiques à l'outil ; reportez-vous à la documentation de votre outil de provisionnement DNS.

Ce mot-clé n’a d’importance que lorsque le type de défi est « dns-01 » ou « dns-persist-01 ».

Voir aussi : « challenge », « provider-name »

<a id="entry-12-8-bits"></a>

**`bits <number>`**

```haproxy
bits <number>
```

Configurez le nombre de bits à générer pour un certificat RSA. Valeur par défaut : 2048. Une valeur trop élevée peut déclencher un avertissement si votre machine n'est pas suffisamment puissante. (Cela peut être configuré avec « warn-blocked-traffic-after », mais bloquer le trafic trop longtemps pourrait déclencher le watchdog.)

<a id="entry-12-8-challenge"></a>

**`challenge <string>`**

```haproxy
challenge <string>
```

Prend en paramètre un type de défi, qui doit être http-01, dns-01 ou dns-persist-01. Si non utilisé, la valeur par défaut est http-01.

dns-persist-01 implémente draft-ietf-acme-dns-persist. Contrairement à dns-01, il utilise un enregistrement TXT statique situé en "\_validation-persist.`<domain>`" qui est défini une fois et ne change jamais entre les renouvellements. Cet enregistrement doit contenir l'URI du compte et une politique facultative. Ce type de défi ne nécessite pas d'accès en écriture à l'API du fournisseur DNS à chaque renouvellement.

<a id="entry-12-8-challenge-ready"></a>

**`challenge-ready <value>[,<value>]*`**

```haproxy
challenge-ready <value>[,<value>]*
```

Configurez les conditions qui doivent être remplies avant d'envoyer une notification au serveur ACME indiquant qu'un défi dns-01 est prêt à être validé. Les valeurs acceptées sont :

```text
cli  - attend qu'un opérateur signale que le challenge est prêt via la
       commande CLI "acme challenge_ready <crt> domain <domain>" sur la
       CLI master ou le socket de statistiques. Un outil externe de
       provisionnement DNS peut ainsi confirmer que l'enregistrement TXT
       est défini avant que HAProxy poursuive.

dns  - effectue une prévérification DNS en résolvant l'enregistrement TXT
       de "_acme-challenge.<domain>" via la section de résolveurs "default"
       configurée, et non les serveurs de noms faisant autorité.
       Le challenge n'est pas soumis tant que l'enregistrement TXT ne
       correspond pas au jeton attendu. Les résultats peuvent donc
       dépendre du cache DNS des résolveurs. Le délai entre les tentatives
       de résolution est contrôlé par "dns-delay". Cette option est
       indépendante de la commande CLI et ne nécessite aucune
       intervention humaine.

       Pour dns-01, l'enregistrement TXT de "_acme-challenge.<domain>"
       est résolu et doit correspondre au jeton attendu. Pour dns-persist-01,
       l'enregistrement TXT de "_validation-persist.<domain>" est résolu
       et seule sa présence est vérifiée.

delay - impose une attente initiale de "dns-delay" avant de poursuivre.
        Sans "dns", le challenge est soumis après expiration de ce délai.
        Avec "dns", l'attente initiale précède les prévérifications DNS.

none - aucune condition de disponibilité ; le challenge est soumis
       immédiatement au serveur ACME sans confirmation externe.
       Cette option ne peut être combinée aux autres.
```

Plusieurs valeurs peuvent être combinées avec une virgule. Lorsque plusieurs conditions sont spécifiées, HAProxy les traite dans l'ordre suivant : il attend d'abord la confirmation CLI ("cli"), puis applique le délai initial ("delay"), puis effectue les vérifications DNS préalables ("dns").

Cette option n’est compatible qu’avec les types de défis dns-01 et dns-persist-01.

Lorsque « challenge » est défini sur « dns-01 » et que cette option n’est pas configurée, la valeur par défaut est « cli ».

Lorsque « challenge » est défini sur « dns-persist-01 » et que cette option n’est pas configurée, la valeur par défaut est « dns,delay ».

Lorsque « challenge » est défini sur « dns-persist-01 », une vérification DNS opportuniste initiale est toujours effectuée avant l’évaluation des conditions « challenge-ready ». Étant donné que l’enregistrement TXT "\_validation-persist.`<domain>`" est défini une fois et ne change pas entre les renouvellements, HAProxy vérifie à l’heure du renouvellement si l’enregistrement est déjà présent. Si la vérification réussit pour tous les domaines, le défi est soumis immédiatement, sans passer par les étapes « challenge-ready » (cli, délai, dns). Si la vérification échoue, HAProxy reprend le flux normal de « challenge-ready ».

Exemple :

```shell
# Wait for CLI confirmation, then verify DNS propagation
challenge-ready cli,dns
```

<a id="entry-12-8-contact"></a>

**`contact <string>`**

```haproxy
contact <string>
```

L’adresse électronique du contact associée à la clé de compte dans l’Autorité de certification.

<a id="entry-12-8-curves"></a>

**`curves <string>`**

```haproxy
curves <string>
```

Lorsque vous utilisez le type de clé ECDSA, configurez les courbes. La valeur par défaut est P-384.

<a id="entry-12-8-directory"></a>

**`directory <string>`**

```haproxy
directory <string>
```

Ce mot-clé configure l'URL du répertoire de l'autorité de certification utilisée par cette section acme. Ce mot-clé est obligatoire, car aucune URL par défaut n'est définie.

Exemple :

```text
directory https://acme-staging-v02.api.letsencrypt.org/directory
```

<a id="entry-12-8-dns-delay"></a>

**`dns-delay <time>`**

```haproxy
dns-delay <time>
```

Configurez le délai utilisé par les conditions « challenge-ready » « delay » et « dns ». La valeur est une durée exprimée au format temps HAProxy (par exemple « 5m », « 300s »). La valeur par défaut est de 30 secondes.

Son rôle dépend des conditions « challenge-ready » en vigueur :

```text
delay     - le challenge est soumis après expiration de ce délai,
            sans prévérification DNS.

dns       - délai entre deux tentatives successives de résolution DNS.
            La première sonde est envoyée immédiatement, sans attente initiale.

dns+delay - attente initiale avant la première tentative de résolution DNS,
            et délai entre les nouvelles tentatives suivantes.
```

Notez que la résolution passe par la section « default » des résolveurs configurés, et non par les serveurs de noms autoritatifs. Les résultats peuvent donc encore être affectés par le cache DNS au niveau du résolveur.

<a id="entry-12-8-dns-timeout"></a>

**`dns-timeout <time>`**

```haproxy
dns-timeout <time>
```

Lorsque « challenge-ready » inclut « dns », configurez le délai maximal autorisé pour résoudre avec succès l'enregistrement TXT avant d'abandonner le défi. La valeur est une durée exprimée au format temps HAProxy (par exemple « 10m », « 600s »). La valeur par défaut est de 600 secondes.

Le délai commence au moment où la première tentative de résolution DNS est déclenchée (après le délai initial « dns-delay »). Si la tentative de résolution suivante devait être déclenchée après l'expiration du délai, le défi est interrompu avec une erreur. Cela empêche une boucle de réessais infinie en cas d'échec de propagation DNS.

Voir également : « dns-delay »

<a id="entry-12-8-keytype"></a>

**`keytype <string>`**

```haproxy
keytype <string>
```

Configurez le type de clé qui sera générée. La valeur peut être soit « RSA » soit « ECDSA ». Vous pouvez également configurer les « curves » pour ECDSA et le nombre de « bits » pour RSA. Par défaut, les clés EC384 sont générées.

<a id="entry-12-8-map"></a>

**`map <map>`**

```haproxy
map <map>
```

Configurez la carte utilisée pour stocker le jeton (clé) et l'empreinte (valeur), ce qui est utile pour répondre à un défi lorsque plusieurs comptes sont utilisés. La tâche ACME ajoutera des entrées avant la validation du défi et supprimera ces entrées à la fin de la tâche.

<a id="entry-12-8-profile"></a>

**`profile <string>`**

```haproxy
profile <string>
```

Demandez un profil de certificat spécifique à l'autorité de certification en incluant un champ « profile » dans la requête newOrder. Cela implémente le brouillon draft-ietf-acme-profiles.

Les noms de profil sont des identificateurs courts spécifiques à l'AC (par exemple, « classic », « shortlived »). Lorsqu'ils sont définis, le nom de profil est envoyé tel quel dans le payload JSON de newOrder. L'AC est libre d'ignorer la requête ou de renvoyer une erreur si le profil n'est pas pris en charge. Lorsqu'il n'est pas défini, aucun champ de profil n'est inclus, et l'AC utilise sa politique d'émission par défaut.

Voir <https://letsencrypt.org/docs/profiles/> pour les profils Let's Encrypt.

Exemple :

```shell
# Request short-lived certificates
profile shortlived
```

<a id="entry-12-8-provider-name"></a>

**`provider-name <string>`**

```haproxy
provider-name <string>
```

Spécifiez le nom du fournisseur DNS transmis à l'outil externe de provisionnement DNS (par exemple, le dataplaneAPI) via le réceptacle « dpapi ». Les valeurs acceptées sont spécifiques à l'outil ; reportez-vous à la documentation de votre outil de provisionnement DNS.

Ce mot-clé n’a d’importance que lorsque le type de défi est « dns-01 » ou « dns-persist-01 ».

Voir aussi : « challenge », « acme-vars »

<a id="entry-12-8-reuse-key"></a>

**`reuse-key { on | off }`**

```haproxy
reuse-key { on | off }
```

Si cette option est définie sur « on », HAProxy ne générera pas de nouvelle clé privée et conservera la précédente. La rotation des clés privées est recommandée ; lorsque cette option est activée, il est recommandé de régénérer manuellement les clés régulièrement.

Cette option peut être utile lors de l'utilisation de clés RSA supérieures à 2048 bits, qui peuvent nécessiter du temps pour être générées et risquent de ralentir un thread chargé de cette opération.

Utiliser la même clé peut être utile lorsque vous utilisez le cache de votre serveur ACME, car cela permet de récupérer un certificat valide correspondant à la clé actuelle.

La valeur par défaut est « off ».

Exemple :

```text
global
    expose-experimental-directives
    httpclient.resolvers.prefer ipv4

frontend in
    bind *:80
    bind *:443 ssl
    http-request return status 200 content-type text/plain lf-string "%[path,field(-1,/)].%[path,field(-1,/),map(virt@acme)]\n" if { path_beg '/.well-known/acme-challenge/' }
    ssl-f-use crt "foo.example.com.pem.rsa"   acme LE1 domains "foo.example.com.pem,bar.example.com"
    ssl-f-use crt "foo.example.com.pem.ecdsa" acme LE2 domains "foo.example.com.pem,bar.example.com"

acme LE1
    directory https://acme-staging-v02.api.letsencrypt.org/directory
    account-key /etc/haproxy/letsencrypt.account.key
    contact john.doe@example.com
    challenge http-01
    keytype RSA
    bits 2048
    map virt@acme

acme LE2
    directory https://acme-staging-v02.api.letsencrypt.org/directory
    account-key /etc/haproxy/letsencrypt.account.key
    contact john.doe@example.com
    challenge http-01
    keytype ECDSA
    curves P-384
    map virt@acme
```

<a id="entry-12-8-eab-key-id"></a>

**`eab-key-id <filename>`**

```haproxy
eab-key-id <filename>
```

Configurez le chemin vers le fichier d'identifiant de clé EAB. Les identifiants sont fournis par l'autorité de certification et doivent être placés au chemin spécifié avant le démarrage de HAProxy. Ils sont utilisés uniquement lors de la création du compte.

Le fichier doit contenir une chaîne ASCII brute.

Les identifiants EAB ne sont requis que lors de la création initiale du compte ACME et peuvent être supprimés par la suite, soit depuis la configuration, soit en vidant les fichiers. Un fichier vide est ignoré sans message d'erreur. Les espaces blancs ne sont pas ignorés, à l’exception du saut de ligne final.

Voir aussi : « eab-mac-key », « eab-mac-alg »

<a id="entry-12-8-eab-mac-key"></a>

**`eab-mac-key <filename>`**

```haproxy
eab-mac-key <filename>
```

Configurez le chemin vers le fichier de clé MAC EAB. Le credential est fourni par l'autorité de certification (CA) et doit être placé au chemin spécifié avant le démarrage de HAProxy. Il est utilisé uniquement lors de la création de compte.

Le fichier doit contenir une clé MAC encodée en base64url.

Les identifiants EAB ne sont requis que lors de la création initiale du compte ACME et peuvent être supprimés par la suite, soit depuis la configuration, soit en vidant les fichiers. Un fichier vide est ignoré sans message d'erreur. Les espaces blancs ne sont pas ignorés, à l’exception du saut de ligne final.

Voir aussi : « eab-key-id », « eab-mac-alg »

<a id="entry-12-8-eab-mac-alg"></a>

**`eab-mac-alg { HS256 | HS384 | HS512 }`**

```haproxy
eab-mac-alg { HS256 | HS384 | HS512 }
```

Configure l'algorithme MAC utilisé pour la signature EAB. La valeur par défaut est HS256. La clé MAC EAB doit être suffisamment grande pour supporter l'algorithme MAC spécifié. Toutes les autorités de certification ne prennent pas en charge des algorithmes autres que HS256.

Voir aussi : « eab-key-id », « eab-mac-key »

## 12.9. Contrôles d'état {#section-12-9}

Il est possible de déclarer globalement plusieurs contrôles d'état pouvant être utilisés par les serveurs dans toute la configuration, en ignorant la configuration locale du proxy.

<a id="entry-12-9-healthcheck"></a>

**`healthcheck <name>`**

```haproxy
healthcheck <name>
```

Crée un nouveau contrôle d'état nommé `<name>`. Ce nom doit être unique. Il doit être utilisé dans la ligne server pour référencer une section de contrôle d'état spécifique.

<a id="entry-12-9-type"></a>

**`type <type>`**

```haproxy
type <type>
```

Définit le type de contrôle d'état. Ce paramètre est obligatoire. Les types de contrôle d'état suivants sont pris en charge :

    * tcp-check
    * httpchk
    * ssl-hello-chk
    * smtpchk
    * pgsql-check
    * redis-check
    * mysql-check
    * ldap-check
    * spop-check

Chaque type utilise les mêmes paramètres, le cas échéant, que l'option correspondante du proxy. Par exemple, la méthode, l'URI… peuvent être spécifiées pour le type « httpchk » :

Exemples :

```text
   healthcheck my-http-check
type httpchk GET /health HTTP/1.1 %[srv_name]
```

Voir aussi : « option tcp-check », « option httpchk », « option ssl-hello-chk », « option smtpchk », « option mysql-check », « option pgsql-check », « option redis-check », « option ldap-check » et « option spop-check »

<a id="entry-12-9-http-check-comment"></a>

**`http-check comment <string>`**

```haproxy
http-check comment <string>
http-check connect [default] [port <expr>] [addr <ip>] [send-proxy]
                   [via-socks4] [ssl] [sni <sni>] [alpn <alpn>] [linger]
                   [proto <name>] [comment <msg>]
http-check disable-on-404
http-check expect [min-recv <int>] [comment <msg>]
                  [ok-status <st>] [error-status <st>] [tout-status <st>]
                  [on-success <fmt>] [on-error <fmt>] [status-code <expr>]
                  [!] <match> <pattern>
http-check send [meth <method>] [{ uri <uri> | uri-lf <fmt> }>] [ver <version>]
                [hdr <name> <fmt>]* [{ body <string> | body-lf <fmt> }]
                [comment <msg>]
http-check send-state
http-check set-var(<var-name>[,<cond>...]) <expr>
http-check set-var-fmt(<var-name>[,<cond>...]) <fmt>
http-check unset-var(<var-name>)
```

Ajoutez une règle spécifique http-check pour un contrôle d'état « httpchk ». La syntaxe utilisée est identique à celle des directives du proxy correspondant. Consultez la documentation du proxy correspondant pour plus de détails.

<a id="entry-12-9-tcp-check-comment"></a>

**`tcp-check comment <string>`**

```haproxy
tcp-check comment <string>
tcp-check connect [default] [port <expr>] [addr <ip>] [send-proxy] [via-socks4]
                  [ssl] [sni <sni>] [alpn <alpn>] [linger]
                  [proto <name>] [comment <msg>]
tcp-check expect [min-recv <int>] [comment <msg>]
                 [ok-status <st>] [error-status <st>] [tout-status <st>]
                 [on-success <fmt>] [on-error <fmt>] [status-code <expr>]
                 [!] <match> <pattern>
tcp-check send <data> [comment <msg>]
tcp-check send-lf <fmt> [comment <msg>]
tcp-check send-binary <hexstring> [comment <msg>]
tcp-check send-binary-lf <hexfmt> [comment <msg>]
tcp-check set-var(<var-name>[,<cond>...]) <expr>
tcp-check set-var-fmt(<var-name>[,<cond>...]) <fmt>
tcp-check unset-var(<var-name>)
```

Ajoutez une règle tcp-check spécifique pour un contrôle d'état « tcp-check ». La syntaxe utilisée est identique à celle des directives correspondantes du proxy. Consultez la documentation du proxy correspondant pour plus de détails.
