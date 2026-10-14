---
title: "9. Statistiques et surveillance"
linkTitle: "9. Statistiques et surveillance"
weight: 330
description: "Statistiques CSV et typées, commandes CLI d'exécution, CLI principale et fichiers de statistiques"
icon: fa-solid fa-chart-line
module: [HAPROXY]
categories: [Tâche]
aliases:
  - /haproxy/management/statistics-and-monitoring/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 9"
---

Il est possible de consulter l'état de HAProxy. Le mécanisme le plus couramment utilisé est la page de statistiques HTTP. Cette page expose également un format de sortie CSV alternatif destiné aux outils de surveillance. Le même format est disponible via le socket Unix.

Les statistiques sont regroupées par catégories désignées sous le nom de domaines, correspondant aux différents composants d'HAProxy. Deux domaines sont disponibles : proxy et resolvers. Si aucun domaine n'est précisé, le domaine proxy est sélectionné. Notez que seules les statistiques du proxy sont affichées sur la page HTTP.

## 9.1. Format CSV {#section-9-1}

Les statistiques peuvent être consultées soit via le socket Unix, soit via la page HTTP. Les deux méthodes fournissent un format CSV dont les champs sont décrits ci-dessous. La première ligne commence par un dièse ('#') et contient un mot par champ séparé par des virgules, représentant le titre de la colonne. Toutes les lignes suivantes, à partir de la deuxième, utilisent un format CSV classique avec une virgule comme délimiteur, et la guillemet double ('"') comme délimiteur textuel facultatif, uniquement si le texte enclos est ambigu (s'il contient une guillemet ou une virgule). Le caractère guillemet double ('"') présent dans le texte est doublé ('""'), ce qui correspond au format reconnu par la plupart des outils. Veuillez ne pas insérer de colonne avant celles-ci afin de ne pas rompre les outils utilisant des positions de colonne codées en dur.

Pour les statistiques du proxy, après chaque nom de champ, les types pouvant avoir une valeur pour ce champ sont indiqués entre parenthèses. Les types sont L (écouteurs), F (frontaux), B (backends) et S (serveurs). Un ensemble fixe de champs statiques est toujours disponible dans le même ordre. Une colonne contenant le caractère '-' délimite la fin des champs statiques, après laquelle la présence ou l'ordre des champs n'est pas garanti.

Voici la liste des champs statiques utilisant le domaine de statistiques du proxy :

```text
 0. pxname [LFBS]: nom du proxy
 1. svname [LFBS]: nom du service (FRONTEND pour un frontend, BACKEND pour un backend,
    un nom quelconque pour un serveur/écouteur)
 2. qcur [..BS]: requêtes actuellement en file. Pour le backend, nombre de requêtes en
    attente sans serveur attribué.
 3. qmax [..BS]: valeur maximale de qcur
 4. scur [LFBS]: sessions actuelles
 5. smax [LFBS]: nombre maximal de sessions
 6. slim [LFBS]: limite configurée de sessions
 7. stot [LFBS]: nombre cumulé de sessions
 8. bin [LFBS]: octets entrants
 9. bout [LFBS]: octets sortants
10. dreq [LFB.]: requêtes refusées pour des raisons de sécurité.
    - En tcp, une règle tcp-request content a correspondu.
    - En http, une règle http-request ou tarpit a correspondu.
11. dresp [LFBS]: réponses refusées pour des raisons de sécurité.
    - En http, une règle http-request ou "option checkcache" a correspondu.
12. ereq [LF..]: erreurs de requête. Causes possibles :
    - interruption prématurée par le client avant l'envoi de la requête.
    - erreur de lecture depuis le client
    - expiration du délai client
    - fermeture de connexion par le client
    - diverses requêtes incorrectes du client.
    - requête soumise à un tarpit.
13. econ [..BS]: nombre de requêtes ayant rencontré une erreur de connexion à un serveur
    backend. La statistique du backend additionne celles de tous ses serveurs
    et les erreurs de connexion sans serveur particulier (par exemple,
    aucun serveur actif dans le backend).
14. eresp [..BS]: erreurs de réponse, incluant srv_abrt. Autres erreurs possibles :
    - erreur d'écriture sur le socket client (non comptée pour le serveur)
    - échec d'application des filtres à la réponse.
15. wretr [..BS]: nombre de nouvelles tentatives de connexion à un serveur.
16. wredis [..BS]: nombre de réacheminements d'une requête vers un autre serveur.
    Pour un serveur, nombre de fois où il a été remplacé par un autre.
17. status [LFBS]: état (UP/DOWN/NOLB/MAINT/MAINT(via)/MAINT(resolution)...)
18. weight [..BS]: poids effectif total (backend), poids effectif (serveur)
19. act [..BS]: nombre de serveurs actifs (backend), serveur actif (serveur)
20. bck [..BS]: nombre de serveurs de secours (backend), serveur de secours (serveur)
21. chkfail [...S]: nombre de contrôles échoués (seulement lorsque le serveur est disponible).
22. chkdown [..BS]: nombre de transitions UP->DOWN. Le compteur du backend compte les
    transitions de tout le backend vers un état indisponible, et non la
    somme des compteurs de chaque serveur.
23. lastchg [..BS]: secondes écoulées depuis la dernière transition UP<->DOWN
24. downtime [..BS]: durée totale d'indisponibilité (en secondes). Pour le backend,
    indisponibilité de l'ensemble du backend, et non somme des durées
    d'indisponibilité des serveurs.
25. qlimit [...S]: maxqueue configuré pour le serveur, ou champ vide si la valeur
    est 0 (valeur par défaut, sans limite)
26. pid [LFBS]: identifiant du processus (0 pour la première instance, 1 pour la deuxième, ...)
27. iid [LFBS]: identifiant unique du proxy
28. sid [L..S]: identifiant du serveur (unique dans un proxy)
29. throttle [...S]: pourcentage actuel de limitation du serveur lorsque slowstart est
    actif, ou aucune valeur en dehors de slowstart.
30. lbtot [..BS]: nombre total de sélections d'un serveur pour une nouvelle session ou
    un réacheminement. Le compteur du serveur compte ses propres sélections.
31. tracked [...S]: identifiant proxy/serveur si le suivi est activé.
32. type [LFBS]: (0=frontend, 1=backend, 2=server, 3=socket/listener)
33. rate [.FBS]: sessions par seconde pendant la dernière seconde écoulée
34. rate_lim [.F..]: limite configurée de nouvelles sessions par seconde
35. rate_max [.FBS]: nombre maximal de nouvelles sessions par seconde
36. check_status [...S]: état du dernier contrôle d'état, parmi :
       UNK     -> inconnu
       INI     -> initialisation
       SOCKERR -> erreur de socket
       L4OK    -> contrôle réussi à la couche 4, sans test des couches supérieures
       L4TOUT  -> délai expiré aux couches 1-4
       L4CON   -> problème de connexion aux couches 1-4, par exemple
                  "Connection refused" (tcp rst) ou "No route to host" (icmp)
       L6OK    -> contrôle réussi à la couche 6
       L6TOUT  -> délai expiré à la couche 6 (SSL)
       L6RSP   -> réponse invalide à la couche 6 - erreur de protocole
       L7OK    -> contrôle réussi à la couche 7
       L7OKC   -> contrôle réussi sous condition à la couche 7, par exemple 404
                  avec disable-on-404
       L7TOUT  -> délai expiré à la couche 7 (HTTP/SMTP)
       L7RSP   -> réponse invalide à la couche 7 - erreur de protocole
       L7STS   -> erreur de réponse à la couche 7, par exemple HTTP 5xx
    Note : si un contrôle est en cours, le dernier état connu est indiqué
    avec le préfixe "* ", par exemple "* L7OK".
37. check_code [...S]: code des couches5-7, si disponible
38. check_duration [...S]: durée en ms du dernier contrôle d'état
39. hrsp_1xx [.FBS]: réponses http de code 1xx
40. hrsp_2xx [.FBS]: réponses http de code 2xx
41. hrsp_3xx [.FBS]: réponses http de code 3xx
42. hrsp_4xx [.FBS]: réponses http de code 4xx
43. hrsp_5xx [.FBS]: réponses http de code 5xx
44. hrsp_other [.FBS]: réponses http avec un autre code (erreur de protocole)
45. hanafail [...S]: détails des contrôles d'état échoués
46. req_rate [.F..]: requêtes HTTP par seconde pendant la dernière seconde écoulée
47. req_rate_max [.F..]: nombre maximal observé de requêtes HTTP par seconde
48. req_tot [.FB.]: nombre total de requêtes HTTP reçues
49. cli_abrt [..BS]: nombre de transferts de données interrompus par le client
50. srv_abrt [..BS]: nombre de transferts de données interrompus par le serveur
    (compris dans eresp)
51. comp_in [.FB.]: octets de réponse HTTP fournis au compresseur
52. comp_out [.FB.]: octets de réponse HTTP émis par le compresseur
53. comp_byp [.FB.]: octets ayant contourné le compresseur HTTP
    (limite CPU/BW)
54. comp_rsp [.FB.]: nombre de réponses HTTP compressées
55. lastsess [..BS]: secondes écoulées depuis la dernière session attribuée au
    serveur/backend
56. last_chk [...S]: contenu du dernier contrôle d'état ou erreur textuelle
57. last_agt [...S]: contenu du dernier contrôle d'agent ou erreur textuelle
58. qtime [..BS]: durée moyenne d'attente en file, en ms, sur les 1024 dernières requêtes
59. ctime [..BS]: durée moyenne de connexion, en ms, sur les 1024 dernières requêtes
60. rtime [..BS]: durée moyenne de réponse, en ms, sur les 1024 dernières requêtes
    (0 pour TCP)
61. ttime [..BS]: durée moyenne totale de session, en ms, sur les 1024 dernières
    requêtes
62. agent_status [...S]: état du dernier contrôle d'agent, parmi :
       UNK     -> inconnu
       INI     -> initialisation
       SOCKERR -> erreur de socket
       L4OK    -> contrôle réussi à la couche 4, sans test des couches supérieures
       L4TOUT  -> délai expiré aux couches 1-4
       L4CON   -> problème de connexion aux couches 1-4, par exemple
                  "Connection refused" (tcp rst) ou "No route to host" (icmp)
       L7OK    -> l'agent a indiqué "up"
       L7STS   -> l'agent a indiqué "fail", "stop" ou "down"
63. agent_code [...S]: code numérique indiqué par l'agent, le cas échéant (inutilisé actuellement)
64. agent_duration [...S]: durée en ms du dernier contrôle
65. check_desc [...S]: courte description lisible de check_status
66. agent_desc [...S]: courte description lisible de agent_status
67. check_rise [...S]: paramètre "rise" du serveur utilisé par les contrôles
68. check_fall [...S]: paramètre "fall" du serveur utilisé par les contrôles
69. check_health [...S]: valeur du contrôle d'état du serveur, entre 0 et rise+fall-1
70. agent_rise [...S]: paramètre "rise" de l'agent, normalement 1
71. agent_fall [...S]: paramètre "fall" de l'agent, normalement 1
72. agent_health [...S]: paramètre d'état de l'agent, entre 0 et rise+fall-1
73. addr [L..S]: address:port ou "unix". Une adresse IPv6 est encadrée de crochets.
74: cookie [..BS]: valeur du cookie du serveur ou nom du cookie du backend
75: mode [LFBS]: mode du proxy (tcp, http, health, unknown)
76: algo [..B.]: algorithme de répartition de charge
77: conn_rate [.F..]: nombre de connexions pendant la dernière seconde écoulée
78: conn_rate_max [.F..]: valeur maximale connue de conn_rate
79: conn_tot [.F..]: nombre cumulé de connexions
80: intercepted [.FB.]: nombre cumulé de requêtes interceptées (monitor, stats)
81: dcon [LF..]: requêtes refusées par les règles "tcp-request connection"
82: dses [LF..]: requêtes refusées par les règles "tcp-request session"
83: wrew [LFBS]: nombre cumulé d'avertissements de réécriture d'en-tête échouée
84: connect [..BS]: nombre cumulé de tentatives d'établissement de connexion
85: reuse [..BS]: nombre cumulé de réutilisations de connexion
86: cache_lookups [.FB.]: nombre cumulé de recherches dans le cache
87: cache_hits [.FB.]: nombre cumulé de succès dans le cache
88: srv_icur [...S]: nombre actuel de connexions inactives réutilisables
89: src_ilim [...S]: limite du nombre de connexions inactives disponibles
90. qtime_max [..BS]: durée maximale observée d'attente en file, en ms
91. ctime_max [..BS]: durée maximale observée de connexion, en ms
92. rtime_max [..BS]: durée maximale observée de réponse, en ms (0 pour TCP)
93. ttime_max [..BS]: durée maximale totale observée de session, en ms
94. eint [LFBS]: nombre cumulé d'erreurs internes
95. idle_conn_cur [...S]: nombre actuel de connexions inactives non sûres
96. safe_conn_cur [...S]: nombre actuel de connexions inactives sûres
97. used_conn_cur [...S]: nombre actuel de connexions utilisées
98. need_conn_est [...S]: estimation du nombre de connexions nécessaires
99. uweight [..BS]: poids utilisateur total (backend), poids utilisateur du serveur (serveur)
100. agg_server_status [..B.]: jauge agrégée du backend pour l'état des serveurs
101. agg_server_status_check [..B.]: (obsolète)
102. agg_check_status [..B.]: jauge agrégée du backend pour l'état des contrôles des serveurs
103. srid [...S]: révision de l'identifiant du serveur
104. sess_other [.F..]: nombre total de sessions autres que HTTP depuis le démarrage du processus
105. h1_sess [.F..]: nombre total de sessions HTTP/1 depuis le démarrage du processus
106. h2_sess [.F..]: nombre total de sessions HTTP/2 depuis le démarrage du processus
107. h3_sess [.F..]: nombre total de sessions HTTP/3 depuis le démarrage du processus
108. req_other [.F..]: nombre total de sessions autres que HTTP traitées par cet objet
     depuis le démarrage du processus worker
109. h1req [.F..]: nombre total de sessions HTTP/1 traitées par cet objet
     depuis le démarrage du processus worker
110. h2req [.F..]: nombre total de sessions HTTP/2 traitées par cet objet
     depuis le démarrage du processus worker
111. h3req [.F..]: nombre total de sessions HTTP/3 traitées par cet objet
     depuis le démarrage du processus worker
112. proto [L...]: protocole
113. priv_idle_cur [...S]: nombre actuel de connexions inactives privées
114. reqbin [LFBS]: octets de requête reçus depuis le démarrage du processus
     worker
115. reqbout [LFBS]: octets de requête envoyés depuis le démarrage du processus
     worker
116. resbin [LFBS]: octets de réponse reçus depuis le démarrage du processus
     worker
117. resbout [LFBS]: octets de réponse envoyés depuis le démarrage du processus
     worker
```

Pour tous les autres domaines de statistiques, la présence ou l'ordre des champs n'est pas garantie. Dans ce cas, la ligne d'en-tête doit toujours être utilisée pour analyser les données CSV.

## 9.2. Format de sortie typé {#section-9-2}

Les commandes « show info » et « show stat » prennent en charge un mode où chaque valeur de sortie est accompagnée de son type et d'informations suffisantes pour déterminer comment la valeur doit être agrégée entre les processus et comment elle évolue.

Dans tous les cas, la sortie se compose d'une seule valeur par ligne, avec toutes les informations séparées en champs délimités par des deux-points (':').

La première colonne indique l'objet ou la métrique dont la sortie est générée. Son format est spécifique à la commande produisant cette sortie et ne sera pas décrit dans cette section. En général, il se compose d'une série d'identifiants et de noms de champs.

La deuxième colonne contient 4 caractères indiquant respectivement l'origine, la nature, la portée et l'état de persistance de la valeur signalée. Le premier caractère (l'origine) indique l'emplacement d'où la valeur a été extraite. Les caractères possibles sont :

```text
M   La valeur est une métrique, valide à un instant donné et susceptible
    de changer selon sa nature.

S   La valeur est un état : une valeur discrète qui, par définition,
    ne peut pas être agrégée. Il peut s'agir de l'état d'un serveur
    ("UP" ou "DOWN"), du PID du processus, etc.

K   La valeur est une clé de tri : un identifiant unique dans sa classe
    permettant de grouper certaines valeurs. Tous les identifiants internes
    sont des clés. Un nom peut être une clé s'il est unique, comme celui
    d'un frontend. Les clés viennent généralement de la configuration,
    même si certaines sont attribuées automatiquement. Dans la plupart
    des cas, elles peuvent être assimilées à la configuration.

C   La valeur vient de la configuration. Certaines valeurs configurées
    sont utiles en sortie, comme une limite de connexions simultanées
    ou un nom de cookie. Elles sont, par définition, identiques dans
    tous les processus issus du même fichier de configuration.

P   La valeur vient du produit lui-même. Ces valeurs sont rares ; les plus
    courantes sont le nom du produit, sa version et sa date de publication.
    Elles sont aussi identiques dans tous les processus.
```

Le deuxième caractère (la nature) indique la nature de l'information transportée par le champ afin de permettre à un agrégateur de déterminer quelle opération utiliser pour agréger plusieurs valeurs. Les caractères possibles sont :

```text
A   La valeur représente l'ancienneté d'un événement. À la différence
    d'une durée, elle est calculée automatiquement selon la date actuelle.
    Exemple : temps écoulé depuis la dernière session sur un serveur.
    Les anciennetés sont généralement agrégées en retenant le minimum
    et n'ont pas besoin d'être stockées.

a   La valeur est déjà une moyenne, comme un temps de réponse moyen ou
    un poids de serveur. Les moyennes peuvent généralement être moyennées
    entre processus.

C   La valeur est un compteur cumulé. Elle augmente continuellement jusqu'à
    son rebouclage. Certains protocoles de surveillance distinguent
    compteurs et jauges pour indiquer un type différent. Les compteurs
    représentent des événements ou des volumes et peuvent généralement
    être additionnés : nombres de connexions ou d'octets, par exemple.

D   La valeur est une durée liée à un état, telle que la durée du dernier
    contrôle d'état ou d'indisponibilité d'un serveur. Ces durées ne sont
    généralement pas additionnées ; le maximum est souvent retenu pour
    calculer un SLA.

G   La valeur est une jauge : une mesure à un instant donné, comme la
    consommation mémoire ou le nombre actuel de connexions actives.
    Ces métriques sont généralement additionnées lors de l'agrégation.

L   La valeur est une limite, généralement configurée. Une limite est
    difficile à agréger car elle est propre au point où elle est relevée.
    Selon la situation, les limites peuvent être additionnées ou conservées
    séparément.

M   La valeur est un maximum, généralement le plus haut niveau connu d'une
    jauge, par exemple le nombre maximal de connexions simultanées au cours
    de la vie du produit. Pour agréger correctement des maxima, indiquez
    une plage allant du plus grand maximum à la somme de tous les maxima :
    on ne peut savoir s'ils ont été atteints simultanément.

m   La valeur est un minimum, généralement le plus bas niveau connu d'une
    jauge, par exemple le nombre minimal de pools mémoire libres au cours
    de la vie du produit. Pour agréger correctement des minima, indiquez
    une plage allant du plus petit minimum à la somme de tous les minima :
    on ne peut savoir s'ils ont été atteints simultanément.

N   La valeur est un nom, donc une chaîne : nom de proxy, de serveur ou
    de cookie. Les noms viennent de la configuration ou de clés et sont
    censés être identiques dans tous les processus.

O   La valeur est une sortie textuelle libre : sortie de commande,
    résultat de contrôle d'état ou description de nœud, par exemple.

R   La valeur est un taux d'événements mesuré à un instant donné. Elle
    ressemble à une jauge, mais le destinataire sait qu'elle évolue
    lentement et peut choisir de ne pas conserver toutes les valeurs.
    Exemple : connexions mesurées par seconde. Ces métriques sont
    généralement additionnées lors de l'agrégation.

T   La valeur est une date ou une heure, comme un champ donnant la date
    actuelle. Sa méthode d'agrégation dépend de l'implémentation.
    Aucun champ n'utilise actuellement ce type.
```

Le troisième caractère (la portée) indique l'étendue à laquelle la valeur est représentative. Certains éléments peuvent être propres à un processus, tandis que d'autres peuvent être propres à une configuration ou à un système. Cette distinction est importante pour déterminer si une seule valeur doit être conservée lors de l'agrégation, ou si les valeurs doivent être agrégées. Les caractères suivants sont actuellement pris en charge :

```text
C   La valeur est valide pour tout un cluster de nœuds communiquant via
    le protocole peers. Exemple : nombre d'entrées d'une table de
    persistance répliquée avec d'autres pairs. Aucune métrique
    n'utilise actuellement cette portée.

P   La valeur est valide seulement pour le processus qui la rapporte.
    La plupart des métriques utilisent cette portée.

S   La valeur est valide pour tout le service : les processus démarrés
    ensemble à partir du même fichier de configuration. Toutes les
    métriques issues de la configuration ont cette portée, ainsi que
    certaines métriques de ressources partagées, comme le cache SSL.

s   La valeur est valide pour tout le système : nom d'hôte, date actuelle
    ou consommation de ressources, par exemple. Aucune métrique
    n'utilise actuellement cette portée.
```

Le quatrième caractère (état de persistance) indique que la valeur (la métrique) est volatile ou persistante lors des rechargements. Les caractères suivants sont attendus :

```text
V   La métrique est volatile car elle est locale au processus actuel ;
    sa valeur est perdue lors d'un rechargement.

P   La métrique est persistante car elle peut être partagée avec d'autres
    processus associés, préservant sa valeur lors des rechargements.
```

Les consommateurs de ces informations auront généralement besoin de ces 4 caractères pour déterminer avec précision comment rapporter les informations agrégées issues de plusieurs processus.

Après cette colonne, la troisième colonne indique le type du champ, parmi « s32 » (entier signé 32 bits), « s64 » (entier signé 64 bits), « u32 » (entier non signé 32 bits), « u64 » (entier non signé 64 bits), « str » (chaîne de caractères). Il est important de connaître le type avant d’analyser la valeur afin de la lire correctement. Par exemple, une chaîne ne contenant que des chiffres reste une chaîne et non un entier (par exemple, un code d’erreur extrait par une vérification).

Ensuite, la quatrième colonne est la valeur elle-même, encodée selon son type. Les chaînes sont écrites telles quelles immédiatement après les deux-points, sans espace initial. Si une chaîne contient un deux-points, il s'affiche normalement. Cela signifie que la sortie ne doit pas être divisée exclusivement autour des deux-points, sinon certaines sorties de vérification ou des adresses de serveur pourraient être tronquées.

## 9.3. Commandes Unix Socket {#section-9-3}

Le socket de statistiques n'est pas activé par défaut. Pour l'activer, il est nécessaire d'ajouter une ligne dans la section globale de la configuration haproxy. Une deuxième ligne est recommandée afin de définir un délai d'expiration plus élevé, toujours apprécié lors de l'émission de commandes manuellement :

```text
global
    stats socket /var/run/haproxy.sock mode 600 level admin
    stats timeout 2m
```

Il est également possible d'ajouter plusieurs instances de socket de statistiques en répétant la ligne, et de les faire écouter sur un port TCP au lieu d'une socket UNIX. Cela n'est jamais fait par défaut car cela présente un risque, mais peut s'avérer utile dans certaines situations :

```text
global
    stats socket /var/run/haproxy.sock mode 600 level admin
    stats socket ipv4@192.168.0.1:9999 level admin
    stats timeout 2m
```

Pour accéder à la socket, un utilitaire externe tel que « socat » est nécessaire. Socat est un outil polyvalent permettant de connecter n'importe quoi à n'importe quoi. Nous l'utilisons pour connecter des terminaux à la socket, ou des canaux stdin/stdout à celle-ci pour les scripts. Les deux syntaxes principales que nous utiliserons sont les suivantes :

```shell
# socat /var/run/haproxy.sock stdio
# socat /var/run/haproxy.sock readline
```

Le premier est utilisé avec des scripts. Il est possible d'envoyer la sortie d'un script vers HAProxy, et de transmettre la sortie d'haproxy à un autre script. Cela est utile, par exemple, pour récupérer des compteurs ou des traces d'attaque.

Le second est utile uniquement pour émettre des commandes manuellement. Il présente l'avantage que le terminal est géré par la bibliothèque readline, qui prend en charge l'édition de ligne et l'historique, ce qui est très pratique lors de l'émission de commandes répétées (par exemple : surveiller un compteur).

La socket prend en charge trois modes de fonctionnement :

- non interactif, silencieux
- interactif, silencieux
- interactif avec invite

Le mode non interactif est le mode par défaut lorsque socat se connecte à la socket. Dans ce mode, une seule ligne peut être envoyée. Elle est traitée en entier, les réponses sont renvoyées, puis la connexion se ferme après la fin de la réponse. C’est le mode utilisé par les scripts et les outils de surveillance. Il est possible d’envoyer plusieurs commandes dans ce mode, à condition de les séparer par un point-virgule (';'). Par exemple :

```shell
# echo "show info;show stat;show table" | socat /var/run/haproxy stdio
```

Si une commande doit utiliser un point-virgule ou une barre oblique inverse (par exemple, dans une valeur), elle doit être précédée d'une barre oblique inverse ('&#92;').

Le mode interactif permet d'envoyer de nouvelles commandes après la fin des commandes des lignes précédentes.
Il existe deux variantes : l'une silencieuse, qui fonctionne comme le mode non interactif, sauf que le socket attend une nouvelle commande au lieu de se fermer, et une autre où une invite est affichée ('\>') au début de la ligne. Le mode interactif est préféré pour les outils avancés, tandis que le mode invite est préféré pour les humains.

Le mode peut être modifié à l’aide de la commande « prompt ». Par défaut, il bascule entre les modes interactif et prompt. Saisir « prompt » en mode interactif active le mode prompt. La commande accepte optionnellement un mode spécifique parmi les suivants :

- "n" : mode non interactif (exécution d'une seule commande, puis arrêt)
- "i" : mode interactif (exécution de plusieurs commandes, sans invite)
- "p" : mode invite (exécution de plusieurs commandes avec invite)

Étant donné que le mode par défaut est non interactif, la commande « prompt » doit être utilisée en premier afin de basculer le mode, faute de quoi la commande précédente entraînera la fermeture de la connexion. Le basculement vers le mode non interactif entraîne la fermeture de la connexion après la finalisation de toutes les commandes de la même ligne.

Pour cette raison, lors du débogage manuel, il est courant de commencer par la commande « prompt » :

```haproxy
# socat /var/run/haproxy readline
prompt
```

> afficher les informations...

Les outils interactifs peuvent préférer commencer par « prompt i » pour passer en mode interactif sans le prompt.

Optionnellement, le temps de fonctionnement du processus peut être affiché dans l’invite. Pour activer cette fonctionnalité, la commande « prompt timed » active l’invite et bascule l’affichage de l’heure. Le temps de fonctionnement est affiché au format « d:hh:mm:ss », où « d » représente le nombre de jours, et « hh », « mm », « ss » le nombre d’heures, de minutes et de secondes, chacun sur deux chiffres :

```haproxy
# socat /var/run/haproxy readline
prompt timed
```

[23:03:34:39]> show version 2.8-dev9-e5e622-18

[23:03:34:41]> quit

Lorsque l’invite temporelle est définie sur l’interface CLI principale, l’invite affiche le temps de fonctionnement du processus actuellement sélectionné, ce qui fonctionne pour le maître, le worker actuel ou un worker plus ancien :

```shell
master> prompt timed
[0:00:00:50] master> show proc
(...)
[0:00:00:58] master> @!11955     <-- master, passage au worker actuel
[0:00:01:03] 11955> @!11942      <-- worker actuel, passage au worker précédent
[0:00:02:17] 11942> @            <-- worker précédent, retour au master
[0:00:01:10] master>
```

Étant donné qu’il est possible d’envoyer plusieurs commandes en même temps, HAProxy utilise la ligne vide comme délimiteur pour marquer la fin de la sortie de chaque commande, et veille à ce qu’aucune commande ne produise de ligne vide en sortie. Un script peut donc parser facilement la sortie, même lorsque plusieurs commandes ont été enchaînées sur une seule ligne.

Certains commandes peuvent accepter un chargement optionnel. Pour ajouter un chargement à une commande, la première ligne doit se terminer par le motif "\<\<&#92;n". Les lignes suivantes seront traitées comme le chargement et peuvent contenir autant de lignes que nécessaire. Pour valider une commande avec un chargement, celle-ci doit se terminer par une ligne vide.

Le motif du payload peut être personnalisé afin de modifier la manière dont le payload se termine. Pour terminer un payload par autre chose qu'une ligne vide, un motif personnalisé peut être défini entre '\<\<' et '&#92;n'. Jusqu'à 64 caractères peuvent être utilisés en plus de '\<\<', sinon cela ne sera pas considéré comme un payload. Il devrait suffire d'utiliser des motifs de payload aléatoires. Par exemple, pour utiliser un fichier PEM contenant des lignes vides et des commentaires :

```haproxy
# echo -e "set ssl cert common.pem <<%EOF%\n$(cat common.pem)\n%EOF%\n" | \
socat /var/run/haproxy.stat -
```

Des limitations existent : le motif "\<\<" ne doit pas être collé au dernier mot de la ligne. La longueur d'une ligne de commande ne doit pas dépasser tune.bufsize, y compris le motif marquant le début du payload, mais en excluant le payload lui-même. La taille du payload est limitée par défaut à 128 Ko. Cette valeur peut être modifiée en configurant le paramètre global "tune.cli.max-payload-size", avec certaines précautions. Notez que le motif marquant la fin du payload fait partie de cette limite.

Lorsqu’un payload est saisi en mode interactif, l’invite change de « \> » à « + ».

Il est important de comprendre qu’en lançant plusieurs processus HAProxy sur les mêmes sockets, n’importe quel processus peut traiter la requête et produire ses propres statistiques.

La liste des commandes actuellement prises en charge sur le socket de statistiques est fournie ci-dessous. Si une commande inconnue est envoyée, HAProxy affiche le message d'utilisation, qui rappelle toutes les commandes prises en charge. Certaines commandes supportent une syntaxe plus complexe ; en cas d'erreur, le message indique généralement quelle partie de la commande est invalide.

Certaines commandes nécessitent un niveau de privilège supérieur pour fonctionner. Si vous ne disposez pas des privilèges suffisants, vous obtiendrez une erreur « Permission denied ». Veuillez consulter l’option « level » des lignes keyword « bind » dans le manuel de configuration pour plus d’informations.

<a id="entry-9-3-abort-ssl-ca-file"></a>

**`abort ssl ca-file <cafile>`**

```haproxy
abort ssl ca-file <cafile>
```

Abandonner et supprimer une transaction de mise à jour temporaire du fichier CA.

Voir également « set ssl ca-file » et « commit ssl ca-file ».

<a id="entry-9-3-abort-ssl-cert"></a>

**`abort ssl cert <filename>`**

```haproxy
abort ssl cert <filename>
```

Annuler et supprimer une transaction de mise à jour de certificat SSL temporaire.

Voir également « set ssl cert » et « commit ssl cert ».

<a id="entry-9-3-abort-ssl-crl-file"></a>

**`abort ssl crl-file <crlfile>`**

```haproxy
abort ssl crl-file <crlfile>
```

Abandonner et supprimer une transaction de mise à jour temporaire d’un fichier CRL.

Voir également « set ssl crl-file » et « commit ssl crl-file ».

<a id="entry-9-3-acme-renew"></a>

**`acme renew <certificate>`**

```haproxy
acme renew <certificate>
```

Démarre une tâche de génération de certificat ACME avec le nom de certificat fourni. Le certificat doit être lié à une section acme, voir la section [12.8](/fr/haproxy/other-sections/#section-12-8) « ACME » du manuel de configuration. Voir également « acme status ».

<a id="entry-9-3-acme-status"></a>

**`acme status`**

```haproxy
acme status
```

Affiche l'état de chaque certificat configuré avec ACME.

Cette commande affiche, séparés par une tabulation :

- Le nom du certificat configuré dans HAProxy
- La section acme utilisée dans la configuration
- L'état de la tâche acme, soit « Running », soit « Scheduled » ou soit « Stopped »
- La date d'expiration UTC du certificat au format ISO8601
- Le temps restant avant expiration (0d si expiré)
- La date planifiée UTC du certificat au format ISO8601
- Le temps restant avant planification (0d si Running)

Exemple :

```shell
$ echo "@1; acme status" | socat /tmp/master.sock - | column -t -s $'\t'
# certificate   section  state      expiration date (UTC)  expires in        scheduled date (UTC)  scheduled in
ecdsa.pem       LE       Running    2020-01-18T09:31:12Z   0d 0h00m00s       2020-01-15T21:31:12Z  0d 0h00m00s
foobar.pem.rsa  LE       Scheduled  2025-08-04T11:50:54Z   89d 23h01m13s     2025-07-27T23:50:55Z  82d 11h01m14s
```

<a id="entry-9-3-add-acl"></a>

**`add acl [@<ver>] <acl> <pattern>`**

```haproxy
add acl [@<ver>] <acl> <pattern>
```

Ajoutez une entrée dans la liste de contrôle d'accès `<acl>`. `<acl>` correspond au \#`<id>` ou au `<name>` retourné par la commande « show acl ».
Cette commande ne vérifie pas si l'entrée existe déjà. Les entrées sont ajoutées à la version courante de la liste de contrôle d'accès, sauf si une version spécifique est précisée avec "@`<ver>`". Ce numéro de version doit avoir été préalablement alloué par la commande « prepare acl », et se situer entre les versions indiquées dans "curr_ver" et "next_ver" dans la sortie de la commande « show acl ». Les entrées ajoutées avec un numéro de version spécifique ne seront pas prises en compte avant une opération « commit acl » sur celles-ci. Elles peuvent toutefois être consultées à l'aide de la commande « show acl @`<ver>` », et effacées à l'aide de la commande « clear acl @`<ver>` ».
Cette commande ne peut pas être utilisée si la référence `<acl>` est un nom également utilisé avec une carte. Dans ce cas, la commande « add map » doit être utilisée à la place.

<a id="entry-9-3-add-backend"></a>

**`add backend <name> from <defproxy> [mode <mode>] [guid <guid>]`**

```haproxy
add backend <name> from <defproxy> [mode <mode>] [guid <guid>]
```

Instanciez un nouveau proxy backend nommé `<name>`.

Seuls les proxies TCP ou HTTP peuvent être créés. Tous les paramètres sont hérités de l'instance de proxy par défaut `<defproxy>`. Par défaut, il est obligatoire de préciser le mode backend via l'argument du même nom, sauf si `<defproxy>` le définit explicitement. Il est également possible d'utiliser un argument GUID facultatif si nécessaire.

Les serveurs peuvent être ajoutés via la commande « add server ». Le backend est initialisé dans l'état non publié. Une fois prêt à recevoir le trafic, utilisez la commande « publish backend » pour exposer l'instance nouvellement créée.

Tous les proxies par défaut nommés peuvent être utilisés, à condition qu’ils respectent les mêmes règles d’héritage appliquées lors de l’analyse de la configuration. Toutefois, certaines exceptions s’appliquent, par exemple lorsque le mode n’est ni TCP ni HTTP.

Cette commande est restreinte et ne peut être émise que sur les sockets configurés au niveau « admin ».

<a id="entry-9-3-add-map"></a>

**`add map [@<ver>] <map> <key> <value>`**

```haproxy
add map [@<ver>] <map> <key> <value>
add map [@<ver>] <map> <payload>
```

Ajoutez une entrée dans la carte `<map>` pour associer la valeur `<value>` à la clé `<key>`. Cette commande ne vérifie pas si l'entrée existe déjà. Elle est principalement utilisée pour remplir une carte après une opération « clear » ou « prepare ». Les entrées sont ajoutées à la version courante de la liste ACL, sauf si une version spécifique est indiquée avec « @`<ver>` ». Ce numéro de version doit avoir été préalablement alloué par « prepare acl », et se situe entre les versions indiquées dans "curr_ver" et "next_ver" dans la sortie de « show acl ». Les entrées ajoutées avec un numéro de version spécifique ne seront pas prises en compte avant une opération « commit map » sur celles-ci. Elles peuvent toutefois être consultées à l’aide de la commande « show map @`<ver>` », et effacées à l’aide de la commande « clear acl @`<ver>` ». Si la carte désignée est également utilisée comme une ACL, celle-ci ne correspondra qu’à la partie `<key>` et ignorera la partie `<value>`. En utilisant la syntaxe du payload, il est possible d’ajouter plusieurs paires clé/valeur en les entrant sur des lignes séparées. Sur chaque nouvelle ligne, le premier mot est la clé et le reste de la ligne est considéré comme la valeur, qui peut même contenir des espaces.

Exemple :

```shell
# socat /tmp/sock1 -
prompt

> add map #-1 <<
+ key1 value1
+ key2 value2 with spaces
+ key3 value3 also with spaces
+ key4 value4

>
```

<a id="entry-9-3-add-server"></a>

**`add server <backend>/<server> [args]*`**

```haproxy
add server <backend>/<server> [args]*
```

Instanciez un nouveau serveur attaché au backend `<backend>`.

Le nom `<server>` ne doit pas déjà être utilisé dans le backend. Une restriction particulière s'applique au backend, qui doit utiliser un algorithme de répartition de charge dynamique. Un sous-ensemble de mots-clés issus de l'instruction de configuration du serveur peut être utilisé pour configurer le comportement du serveur (voir « add server help » pour obtenir la liste). Notez également qu'aucun paramètre ne sera réutilisé à partir d'une éventuelle instruction « default-server » dans le même backend.

Actuellement, un serveur dynamique est initialisé de manière statique avec la méthode d'initialisation « none ». Cela signifie qu'aucune résolution ne sera effectuée si un nom FQDN est spécifié comme adresse, même si la création du serveur sera validée.

Pour prendre en charge les opérations de rechargement, il est nécessaire que le serveur créé via l'interface en ligne de commande soit également inséré manuellement dans le fichier de configuration HAProxy pertinent. Un serveur dynamique absent de la configuration ne sera pas restauré après une opération de rechargement.

Un serveur dynamique peut utiliser le mot-clé « track » pour suivre l'état de vérification d'un autre serveur défini dans la configuration. Toutefois, il n'est pas possible de suivre un autre serveur dynamique. Cela garantit que la chaîne de suivi reste cohérente, même en cas de suppression de serveurs dynamiques.

Utilisez le mot-clé « check » pour activer la prise en charge des vérifications de santé. Notez que la vérification de santé est désactivée par défaut et doit être activée indépendamment du serveur à l’aide de la commande « enable health ». Pour les vérifications d’agent, utilisez le mot-clé « agent-check » et la commande « enable agent ». Notez que, dans ce cas, le serveur peut être activé par l’agent en fonction de l’état rapporté, sans commande explicite « enable server ». Cela signifie également qu’une attention particulière est requise lors de la suppression d’un serveur dynamique avec vérification d’agent. L’agent doit d’abord être désactivé à l’aide de la commande « disable agent » afin de pouvoir placer le serveur en mode maintenance requis avant sa suppression.

Il se peut que la limite de descripteurs de fichiers (fd) soit atteinte lors de l'utilisation d'un grand nombre de serveurs dynamiques. Veuillez vous référer à la documentation du mot-clé global « u-limit » dans ce cas.

<a id="entry-9-3-add-server-help"></a>

**`add server help`**

```haproxy
add server help
```

Liste des mots-clés pris en charge pour les serveurs dynamiques par la version actuelle de HAProxy. La syntaxe des mots-clés est similaire à celle de la ligne server du fichier de configuration ; reportez-vous à leur documentation respective pour plus de détails.

<a id="entry-9-3-add-ssl-ca-file"></a>

**`add ssl ca-file <cafile> <payload>`**

```haproxy
add ssl ca-file <cafile> <payload>
```

Ajoutez un nouveau certificat à un fichier ca. Cette commande est utile lorsque vous avez atteint la limite de taille de tampon sur l'interface en ligne de commande et que vous souhaitez ajouter plusieurs certificats. Au lieu d'utiliser une commande « set » avec tous les certificats, vous pouvez ajouter chaque certificat individuellement. Une commande « set ssl ca-file » réinitialise le fichier ca.

Exemple :

```text
echo -e "set ssl ca-file cafile.pem <<\n$(cat rootCA.crt)\n" | \
socat /var/run/haproxy.stat -
echo -e "add ssl ca-file cafile.pem <<\n$(cat intermediate1.crt)\n" | \
socat /var/run/haproxy.stat -
echo -e "add ssl ca-file cafile.pem <<\n$(cat intermediate2.crt)\n" | \
socat /var/run/haproxy.stat -
echo "commit ssl ca-file cafile.pem" | socat /var/run/haproxy.stat -
```

<a id="entry-9-3-add-ssl-crt-list"></a>

**`add ssl crt-list <crtlist> <certificate>`**

```haproxy
add ssl crt-list <crtlist> <certificate>
add ssl crt-list <crtlist> <payload>
```

Ajoutez un certificat à une liste de certificats (crt-list). Cette commande peut également être utilisée avec des répertoires, puisque les répertoires sont désormais chargés de la même manière que les listes de certificats. Cette commande permet d'utiliser un nom de certificat en paramètre ; pour utiliser des options SSL ou des filtres, une ligne de crt-list doit être envoyée en charge utile au lieu de paramètre. Une seule ligne de crt-list est prise en charge dans la charge utile. Cette commande charge le certificat pour toutes les lignes bind utilisant la crt-list. Pour ajouter un nouveau certificat à HAProxy, les commandes « new ssl cert » et « set ssl cert » doivent être utilisées.

Exemple :

```shell
$ echo "new ssl cert foobar.pem" | socat /tmp/sock1 -
$ echo -e "set ssl cert foobar.pem <<\n$(cat foobar.pem)\n" | socat
/tmp/sock1 -
$ echo "commit ssl cert foobar.pem" | socat /tmp/sock1 -
$ echo "add ssl crt-list certlist1 foobar.pem" | socat /tmp/sock1 -

$ echo -e 'add ssl crt-list certlist1 <<\nfoobar.pem [allow-0rtt] foo.bar.com
!test1.com\n' | socat /tmp/sock1 -
```

<a id="entry-9-3-add-ssl-ech"></a>

**`add ssl ech <bind> <payload>`**

```haproxy
add ssl ech <bind> <payload>
```

Ajoutez une clé ECH à une ligne `<bind>`. Le contenu doit être au format PEM pour ECH.
(<https://datatracker.ietf.org/doc/html/draft-farrell-tls-pemesni>)

Le format de la ligne bind est `<frontend>`/@`<filename>`:`<linenum>` (exemple : frontend1/@haproxy.conf:19)
ou `<frontend>`/`<name>` si la ligne bind a été nommée avec le mot-clé « name ».

Exige une version d'OpenSSL qui prend en charge ECH, et HAProxy doit être compilé avec USE_ECH=1.
Cette commande n'est prise en charge que sur une connexion CLI en mode expérimental (voir « experimental-mode on »).

Voir également « show ssl ech » et « ech » dans la [Section 5.1](/fr/haproxy/bind-and-server-options/#section-5-1) du manuel de configuration.

Exemple :

```shell
$ openssl ech -public_name foobar.com -out foobar3.com.ech
$ echo -e "experimental-mode on; add ssl ech frontend1/@haproxy.conf:19 <<%EOF%\n$(cat foobar3.com.ech)\n%EOF%\n" | \
  socat /tmp/haproxy.sock -
added a new ECH config to frontend1
```

<a id="entry-9-3-add-ssl-jwt"></a>

**`add ssl jwt <filename>`**

```haproxy
add ssl jwt <filename>
```

Ajoutez un certificat déjà chargé à la liste des certificats pouvant être utilisés pour la validation JWT
(voir le convertisseur "jwt_verify_cert"). Cette commande ne fonctionne pas sur les transactions en cours. Voir également les commandes « del ssl jwt » et « show ssl jwt ». Voir l’option de certificat « jwt » pour plus d’informations.

<a id="entry-9-3-clear-counters"></a>

**`clear counters`**

```haproxy
clear counters
```

Réinitialise les valeurs maximales des compteurs de statistiques dans chaque proxy (frontal et backend) et dans chaque serveur. Les compteurs accumulés ne sont pas affectés. Les compteurs d'activité internes rapportés par la commande « show activity » sont également réinitialisés. Cette commande peut être utilisée pour obtenir des compteurs propres après un incident, sans avoir à redémarrer ni à réinitialiser les compteurs de trafic. Cette commande est restreinte et ne peut être exécutée que sur les sockets configurés pour les niveaux « operator » ou « admin ».

<a id="entry-9-3-clear-counters-all"></a>

**`clear counters all`**

```haproxy
clear counters all
```

Réinitialise tous les compteurs de statistiques dans chaque proxy (frontal et backend) ainsi que dans chaque serveur. Cette opération a le même effet qu’un redémarrage. Cette commande est restreinte et ne peut être exécutée que sur les sockets configurés au niveau « admin ».

<a id="entry-9-3-clear-acl"></a>

**`clear acl [@<ver>] <acl>`**

```haproxy
clear acl [@<ver>] <acl>
```

Supprimez toutes les entrées de la liste de contrôle d'accès `<acl>`. `<acl>` correspond au \#`<id>` ou au `<name>` retourné par la commande « show acl ». Notez que si la référence `<acl>` est un nom partagé avec une carte, cette dernière sera également vidée. Par défaut, seule la version courante de la liste de contrôle d'accès est vidée (celle en cours de correspondance). Toutefois, il est possible de préciser une autre version en utilisant '@' suivi de cette version.

<a id="entry-9-3-clear-map"></a>

**`clear map [@<ver>] <map>`**

```haproxy
clear map [@<ver>] <map>
```

Supprimez toutes les entrées de la carte `<map>`. `<map>` est le \#`<id>` ou le `<name>` retourné par la commande « show map ». Notez que si la référence `<map>` est un nom partagé avec une liste de contrôle d'accès (acl), cette dernière sera également vidée. Par défaut, seule la version actuelle de la carte est vidée (celle en cours de correspondance). Toutefois, il est possible de spécifier une autre version en utilisant '@' suivi de cette version.

<a id="entry-9-3-clear-table"></a>

**`clear table <table> [ data.<type> <operator> <value> ] | [ key <key> ] |`**

```haproxy
clear table <table> [ data.<type> <operator> <value> ] | [ key <key> ] |
                    [ ptr <ptr> ]
```

Supprimez les entrées de la table de persistance `<table>`.

Cela est généralement utilisé pour débloquer certains utilisateurs qui se plaignent d’avoir été abusivement privés d’accès à un service, mais cela peut aussi servir à supprimer des entrées de persistance correspondant à un serveur qui va être remplacé (voir « show table » ci-dessous pour plus de détails). Notez qu’il arrive parfois que la suppression d’une entrée soit refusée car elle est actuellement suivie par une session. Il est courant de réessayer quelques secondes plus tard, après la fin de la session.

Dans le cas où aucun argument d'option n'est fourni, toutes les entrées seront supprimées.

Lorsque le formulaire "data." est utilisé, les entrées correspondant à un filtre appliqué à l’aide des données stockées (voir « stick-table » dans la section 4.2) sont supprimées. Un type de données stockées doit être spécifié dans `<type>`, et ce type de données doit être stocké dans la table, sinon une erreur est signalée. Les données sont comparées selon `<operator>` avec l’entier 64 bits `<value>`. Les opérateurs sont les mêmes qu’avec les ACLs :

    - eq : correspond aux entrées dont les données sont égales à cette valeur
    - ne : correspond aux entrées dont les données sont différentes de cette valeur
    - le : correspond aux entrées dont les données sont inférieures ou égales à cette valeur
    - ge : correspond aux entrées dont les données sont supérieures ou égales à cette valeur
    - lt : correspond aux entrées dont les données sont inférieures à cette valeur
    - gt : correspond aux entrées dont les données sont supérieures à cette valeur

Lorsque la forme clé est utilisée, l'entrée `<key>` est supprimée. La clé doit être du même type que la table, ce qui est actuellement limité à IPv4, IPv6, entier et chaîne.

Lorsque la forme ptr est utilisée, l'entrée `<ptr>` est supprimée. `<ptr>` est écrit sous la forme 0xffff et doit correspondre à l'adresse renvoyée par une commande précédente « show table ». Correspondre à une entrée à l'aide de son pointeur peut être pertinent si l'entrée ne peut pas être identifiée à l'aide de sa clé en raison d'une clé vide ou de caractères incompatibles sur le CLI.

Si data.`<type>` est de type tableau, on peut utiliser « [] » pour accéder à un index spécifique du tableau, comme ceci : data.gpt[1]

Exemple :

```shell
    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a4c: key=127.0.0.1 use=0 exp=3594729 gpc0=0 conn_rate(30000)=1 \
      bytes_out_rate(60000)=187
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191
>>> 0x80e6b40: key=127.0.0.3 use=0 exp=3594743 gpc0=2 conn_rate(30000)=10 \
      bytes_out_rate(60000)=200

    $ echo "clear table http_proxy key 127.0.0.1" | socat stdio /tmp/sock1

    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:1
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
>>> 0x80e6b40: key=127.0.0.3 use=0 exp=3594743 gpc0=2 conn_rate(30000)=10 \
      bytes_out_rate(60000)=200
      bytes_out_rate(60000)=191
    $ echo "clear table http_proxy data.gpc0 eq 1" | socat stdio /tmp/sock1
    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:1
>>> 0x80e6b40: key=127.0.0.3 use=0 exp=3594743 gpc0=2 conn_rate(30000)=10 \
      bytes_out_rate(60000)=200

    $ echo "clear table http_proxy ptr 0x80e6b40" | socat stdio /tmp/sock1
    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:0
```

<a id="entry-9-3-commit-acl"></a>

**`commit acl @<ver> <acl>`**

```haproxy
commit acl @<ver> <acl>
```

Validez tous les changements apportés à la version `<ver>` de la liste de contrôle d'accès `<acl>`, et supprimez toutes les versions antérieures. `<acl>` est le numéro \#`<id>` ou le `<name>` retourné par la commande « show acl ». Le numéro de version doit être compris entre "curr_ver"+1 et "next_ver" tel que rapporté par la commande « show acl ». Le contenu à valider dans la liste de contrôle d'accès peut être consulté à l'aide de la commande « show acl @`<ver>` `<acl>` » si nécessaire. Le numéro de version spécifié a normalement été créé à l'aide de la commande « prepare acl ». La substitution est atomique. Elle consiste à mettre à jour atomiquement la version courante vers la version spécifiée, ce qui rend instantanément invisibles toutes les entrées des autres versions et rend visibles toutes les entrées de la nouvelle version. Il est également possible d'utiliser cette commande pour supprimer atomiquement toutes les entrées visibles d'une liste de contrôle d'accès en appelant d'abord « prepare acl », puis en validant sans ajouter d'entrée. Cette commande ne peut pas être utilisée si la référence `<acl>` est un nom également utilisé comme carte. Dans ce cas, la commande « commit map » doit être utilisée à la place.

<a id="entry-9-3-commit-map"></a>

**`commit map @<ver> <map>`**

```haproxy
commit map @<ver> <map>
```

Validez toutes les modifications apportées à la version `<ver>` de la carte `<map>`, et supprimez toutes les versions antérieures. `<map>` est le \#`<id>` ou le `<name>` retourné par la commande « show map ». Le numéro de version doit être compris entre "curr_ver"+1 et "next_ver", tel que rapporté par la commande « show map ». Le contenu à valider dans la carte peut être consulté à l’aide de la commande « show map @`<ver>` `<map>` », si nécessaire. Le numéro de version spécifié a normalement été créé à l’aide de la commande « prepare map ». La substitution est atomique. Elle consiste à mettre à jour atomiquement la version courante vers la version spécifiée, ce qui entraîne instantanément la disparition de toutes les entrées des autres versions, et la visibilité immédiate de toutes les entrées de la nouvelle version. Il est également possible d’utiliser cette commande pour supprimer atomiquement toutes les entrées visibles d’une carte en exécutant d’abord « prepare map », puis en validant sans ajouter d’entrée.

<a id="entry-9-3-commit-ssl-ca-file"></a>

**`commit ssl ca-file <cafile>`**

```haproxy
commit ssl ca-file <cafile>
```

Valider une transaction de mise à jour temporaire du fichier CA SSL.

Dans le cas d'un fichier CA existant (dans un état « Used » dans « show ssl ca-file »), la nouvelle entrée d'arbre de fichier CA est insérée dans l'arbre de fichiers CA, et toutes les instances utilisant cette entrée de fichier CA sont reconstruites, ainsi que les contextes SSL qu'elles nécessitent. Tous les contextes précédemment utilisés par les instances reconstruites sont supprimés. En cas de succès, l'entrée de fichier CA précédente est supprimée de l'arbre. En cas d'échec, rien n'est retiré ni supprimé, et tous les contextes SSL d'origine sont conservés et utilisés. Une fois la transaction temporaire validée, elle est détruite.

Dans le cas d'un nouveau fichier CA (après une commande « new ssl ca-file » et dans un état « Unused » affiché par « show ssl ca-file »), le fichier CA sera inséré dans l'arbre des fichiers CA, mais ne sera utilisé nulle part dans HAProxy. Pour l'utiliser et générer des contextes SSL qui l'utilisent, vous devrez l'ajouter à une liste de certificats avec la commande « add ssl crt-list ».

Voir également « new ssl ca-file », « set ssl ca-file », « add ssl ca-file », « abort ssl ca-file » et « add ssl crt-list ».

<a id="entry-9-3-commit-ssl-cert"></a>

**`commit ssl cert <filename>`**

```haproxy
commit ssl cert <filename>
```

Validez une transaction de mise à jour temporaire du certificat SSL.

Dans le cas d'un certificat existant (dans un état « Used » dans « show ssl cert »), génère tous les contextes SSL et les SNIs dont il a besoin, insère-les, puis supprime les anciens. Remplace en mémoire les anciens certificats SSL partout où `<filename>` était utilisé dans la configuration. En cas d'échec, rien n'est supprimé ni inséré. Une fois la transaction temporaire validée, elle est détruite.

Dans le cas d'un nouveau certificat (après une commande « new ssl cert » et dans un état « Unused » affiché par « show ssl cert »), le certificat sera enregistré dans un stockage de certificats, mais ne sera utilisé nulle part dans haproxy. Pour l'utiliser et générer ses SNI, il faudra l'ajouter à une liste de certificats (crt-list) ou à un répertoire via la commande « add ssl crt-list ».

Voir également « new ssl cert », « set ssl cert », « abort ssl cert » et « add ssl crt-list ».

<a id="entry-9-3-commit-ssl-crl-file"></a>

**`commit ssl crl-file <crlfile>`**

```haproxy
commit ssl crl-file <crlfile>
```

Valider une transaction de mise à jour temporaire d'un fichier CRL SSL.

Dans le cas d'un fichier CRL existant (dans un état « Used » dans « show ssl crl-file »), la nouvelle entrée de fichier CRL est insérée dans l'arbre des fichiers CA (qui contient à la fois les fichiers CA et les fichiers CRL) et chaque instance utilisant l'entrée de fichier CRL est reconstruite, ainsi que les contextes SSL qu'elle nécessite. Tous les contextes précédemment utilisés par les instances reconstruites sont supprimés. En cas de succès, l'entrée de fichier CRL précédente est supprimée de l'arbre. En cas d'échec, rien n'est retiré ni supprimé, et tous les contextes SSL d'origine sont conservés et utilisés. Une fois la transaction temporaire validée, elle est détruite.

Dans le cas d'un nouveau fichier CRL (après une commande « new ssl crl-file » et en état « Unused » dans « show ssl crl-file »), le fichier CRL sera inséré dans l'arbre des fichiers CRL, mais ne sera utilisé nulle part dans HAProxy. Pour l'utiliser et générer des contextes SSL qui l'utilisent, vous devrez l'ajouter à une liste de certificats avec la commande « add ssl crt-list ».

Voir également « new ssl crl-file », « set ssl crl-file », « abort ssl crl-file » et « add ssl crt-list ».

<a id="entry-9-3-debug-counters"></a>

**`debug counters [reset|show|on|off|all|bug|chk|cnt|glt|?]*`**

```haproxy
debug counters [reset|show|on|off|all|bug|chk|cnt|glt|?]*
```

Liste les compteurs internes placés dans le code, qui peuvent varier selon certaines options de compilation. Certains dépendent de DEBUG_STRICT, d'autres de DEBUG_COUNTERS. La commande prend une combinaison d'arguments multiples, certains définissant des actions et d'autres des filtres : - bug active l'affichage des compteurs des requêtes BUG_ON() - cnt active l'affichage des compteurs des requêtes COUNT_IF() - chk active l'affichage des compteurs des requêtes CHECK_IF() - glt active l'affichage des compteurs des requêtes COUNT_GLITCH() - all active l'affichage des compteurs qui n'ont jamais été déclenchés (valeur 0) - off action : désactive la mise à jour des compteurs COUNT_IF() - on action : active la mise à jour des compteurs COUNT_IF() - reset action : réinitialise tous les compteurs spécifiés - show action : affiche tous les compteurs spécifiés

Par défaut, l’action est « show » afin d’afficher les compteurs, et les compteurs listés sont tous des types ayant une valeur non nulle. La commande « show » est implicite lorsqu’aucune autre action n’est spécifiée, et n’est présente que pour faciliter la génération de commandes à partir de scripts.

La sortie commence par un compteur entier, suivi du type du compteur en majuscules, puis de son emplacement dans le code (fichier:ligne), du nom de la fonction, et éventuellement de « : » suivi d'une description. Veuillez noter que le format de sortie peut évoluer entre les versions majeures, et que de nouveaux types et entrées peuvent être rétroportés vers les versions stables dans le but d'améliorer les capacités de débogage. Tout suivi effectué sur ces éléments doit être réalisé de manière très permissive et ne devrait, idéalement, pas être effectué.

En règle générale, les utilisateurs finaux n'utilisent pas cette commande, mais ils peuvent être invités à la faire par un développeur cherchant à diagnostiquer une anomalie ou à rechercher des entrées CNT ou GLT. À noter que des entrées « CHK » non nulles ne devraient pas se produire et doivent être signalées aux développeurs, car elles pourraient indiquer des hypothèses incorrectes dans le code.

<a id="entry-9-3-debug-dev"></a>

**`debug dev <command> [args]*`**

```haproxy
debug dev <command> [args]*
```

Appelle une commande spécifique au développeur. Prise en charge uniquement sur une connexion CLI en mode expert (voir « expert-mode on »). Ces commandes sont extrêmement dangereuses et sans tolérance ; toute utilisation incorrecte peut entraîner un plantage du processus. Elles sont destinées aux experts uniquement et doivent absolument ne pas être utilisées sauf instruction explicite. Certaines d'entre elles ne sont disponibles que lorsque haproxy est compilé avec DEBUG_DEV défini, car elles peuvent avoir des implications de sécurité. Toutes ces commandes exigent des privilèges d'administration et sont délibérément non documentées afin d'éviter d'encourager leur utilisation par des personnes non familières avec le code source.

<a id="entry-9-3-del-acl"></a>

**`del acl <acl> [<key>|#<ref>]`**

```haproxy
del acl <acl> [<key>|#<ref>]
```

Supprimez toutes les entrées ACL de l’ACL `<acl>` correspondant à la clé `<key>`. `<acl>` est le \#`<id>` ou le `<name>` retourné par la commande « show acl ». Si `<ref>` est utilisé, cette commande supprime uniquement la référence indiquée. La référence peut être trouvée en listant le contenu de l’ACL. Notez que si la référence `<acl>` est un nom partagé avec une map, l’entrée sera également supprimée dans la map.

<a id="entry-9-3-del-backend"></a>

**`del backend <name>`**

```haproxy
del backend <name>
```

Supprime le proxy backend nommé `<name>`.

Cette opération n’est possible que pour les proxies TCP ou HTTP. Pour réussir, l’instance backend doit avoir été précédemment dépubliée. En outre, tous ses serveurs doivent avoir été supprimés en premier lieu (via la commande CLI « del server »). Enfin, aucun flux ne doit encore être rattaché à l’instance backend.

Il existe des restrictions supplémentaires qui empêchent la suppression d’un backend. Premièrement, un backend ne peut pas être supprimé s’il est explicitement référencé par des éléments de configuration, par exemple via une règle use_backend ou dans des expressions sample. Certains paramètres de proxy sont également incompatibles avec la suppression en temps d’exécution. Actuellement, cela concerne l’utilisation des options dépréciées dispatch ou transparent. En outre, un backend ne peut pas être supprimé s’il contient une table de persistance (stick-table) déclarée. Enfin, il est actuellement impossible de supprimer un backend si des serveurs QUIC étaient présents dedans.

Il peut être utile d'utiliser « wait be-removable » avant cette commande pour vérifier les prérequis mentionnés ci-dessus. Cela fournit également une méthode pour attendre la fermeture définitive des flux associés au backend cible.

Cette commande est restreinte et ne peut être émise que sur les sockets configurés au niveau « admin ».

<a id="entry-9-3-del-map"></a>

**`del map <map> [<key>|#<ref>]`**

```haproxy
del map <map> [<key>|#<ref>]
```

Supprime toutes les entrées de la carte `<map>` correspondant à la clé `<key>`. `<map>` est le \#`<id>` ou le `<name>` retourné par la commande « show map ». Si l'option `<ref>` est utilisée, cette commande supprime uniquement la référence indiquée. La référence peut être identifiée en listant le contenu de la carte. Notez que si la référence `<map>` est un nom partagé avec une liste de contrôle d'accès (acl), l'entrée sera également supprimée de la carte.

<a id="entry-9-3-del-ssl-ca-file"></a>

**`del ssl ca-file <cafile>`**

```haproxy
del ssl ca-file <cafile>
```

Supprimez une entrée d’arbre de fichier CA depuis HAProxy. Le fichier CA doit être inutilisé et retiré de toute liste crt-list.
La commande « show ssl ca-file » affiche l’état des fichiers CA. La suppression ne fonctionne pas si un certificat est référencé directement via les directives « ca-file » ou « ca-verify-file » dans la configuration.

<a id="entry-9-3-del-ssl-cert"></a>

**`del ssl cert <certfile>`**

```haproxy
del ssl cert <certfile>
```

Supprimez un magasin de certificats depuis HAProxy. Le certificat doit être inutilisé (inclus pour la validation JWT) et retiré de toute liste crt-list ou répertoire. La commande « show ssl cert » affiche l'état du certificat. La suppression ne fonctionne pas avec un certificat référencé directement via la directive « crt » dans la configuration.

<a id="entry-9-3-del-ssl-crl-file"></a>

**`del ssl crl-file <crlfile>`**

```haproxy
del ssl crl-file <crlfile>
```

Supprime une entrée de l'arborescence des fichiers CRL de HAProxy. Le fichier CRL doit être inutilisé et retiré de toute crt-list. La commande « show ssl crl-file » affiche l'état des fichiers CRL. La suppression ne fonctionne pas avec un certificat référencé directement par la directive « crl-file » dans la configuration.

<a id="entry-9-3-del-ssl-crt-list"></a>

**`del ssl crt-list <filename> <certfile[:line]>`**

```haproxy
del ssl crt-list <filename> <certfile[:line]>
```

Supprime une entrée dans une liste de certificats. Cette opération supprime tous les SNIs utilisés pour cette entrée dans les frontaux. Si un certificat est utilisé plusieurs fois dans une liste de certificats, vous devez préciser quelle ligne vous souhaitez supprimer. Pour afficher les numéros de ligne, utilisez la commande « show ssl crt-list -n `<crtlist>` ».

<a id="entry-9-3-del-ssl-ech"></a>

**`del ssl ech <bind>`**

```haproxy
del ssl ech <bind>
```

Supprime les clés ECH d'une ligne bind.

Le format de la ligne bind est `<frontend>`/@`<filename>`:`<linenum>` (exemple : frontend1/@haproxy.conf:19)
ou `<frontend>`/`<name>` si la ligne bind a été nommée avec le mot-clé « name ».

Exige une version d'OpenSSL qui prend en charge ECH, et HAProxy doit être compilé avec USE_ECH=1.
Cette commande n'est prise en charge que sur une connexion CLI en mode expérimental (voir « experimental-mode on »).

Voir également « show ssl ech », « add ssl ech » et « ech » dans la [Section 5.1](/fr/haproxy/bind-and-server-options/#section-5-1) du manuel de configuration.

Exemple :

```shell
$ echo "experimental-mode on; del ssl ech frontend1/@haproxy.conf:19" | socat /tmp/haproxy.sock -
deleted all ECH configs from frontend1/@haproxy.conf:19
```

<a id="entry-9-3-del-ssl-jwt"></a>

**`del ssl jwt <filename>`**

```haproxy
del ssl jwt <filename>
```

Supprime un certificat déjà chargé de la liste des certificats pouvant être utilisés pour la validation JWT
(voir le convertisseur "jwt_verify_cert"). Cette commande ne fonctionne pas sur les transactions en cours. Voir également les commandes « add ssl jwt » et « show ssl jwt ». Voir l'option de certificat « jwt » pour plus d'informations.

<a id="entry-9-3-del-server"></a>

**`del server <backend>/<server>`**

```haproxy
del server <backend>/<server>
```

Supprimez un serveur supprimable attaché au backend `<backend>`. Un serveur supprimable est le serveur qui satisfait à toutes ces conditions :

-  non référencé par d'autres éléments de configuration
-  doit déjà être en maintenance (voir « disable server »)
-  ne doit pas avoir de connexions actives ou inactives

Si l'une de ces conditions n'est pas remplie, la commande échouera.

Les connexions actives sont celles ayant au moins une requête en cours. Il est possible d'accélérer leur fermeture en utilisant « shutdown sessions server ». Il est fortement recommandé d'utiliser « wait srv-removable » avant « del server » afin de garantir que toutes les connexions actives ou inactives sont fermées et que la commande aboutit.

<a id="entry-9-3-disable-agent"></a>

**`disable agent <backend>/<server>`**

```haproxy
disable agent <backend>/<server>
```

Marquez le contrôle de l'agent auxiliaire comme temporairement arrêté.

Dans le cas où une vérification d'agent est exécutée en tant que vérification auxiliaire, en raison du paramètre agent-check d'une directive server, de nouvelles vérifications ne sont initialisées que lorsque l'agent est activé. Ainsi, désactiver l'agent empêchera toute nouvelle vérification d'agent de démarrer jusqu'à ce que l'agent soit réactivé à l'aide de enable agent.

Lorsqu’un agent est désactivé, le traitement d’une vérification d’agent auxiliaire initiée pendant que l’agent était activé se déroule comme suit : toutes les valeurs qui modifieraient le poids, en particulier « drain » ou un poids retourné par l’agent, sont ignorées. Le traitement de la vérification d’agent reste inchangé dans les autres cas.

La motivation de cette fonctionnalité est de permettre de suspendre les effets de modification du poids provenant des vérifications d'agent, afin de configurer le poids d'un serveur à l'aide de set weight sans que celui-ci ne soit annulé par l'agent.

Cette commande est restreinte et ne peut être émise que sur les sockets configurés au niveau « admin ».

<a id="entry-9-3-disable-dynamic-cookie-backend"></a>

**`disable dynamic-cookie backend <backend>`**

```haproxy
disable dynamic-cookie backend <backend>
```

Désactiver la génération de cookies dynamiques pour le backend `<backend>`

<a id="entry-9-3-disable-frontend"></a>

**`disable frontend <frontend>`**

```haproxy
disable frontend <frontend>
```

Marquez le frontal comme arrêté temporairement. Cela correspond au mode utilisé lors d’un redémarrage doux : le frontal libère le port mais peut être réactivé si nécessaire. Utilisez cette option avec précaution, car certains systèmes d’exploitation non Linux ne parviennent pas à le réactiver. Cette fonction est destinée à être utilisée dans des environnements où l’arrêt d’un proxy n’est tout simplement pas envisageable, mais où un proxy mal configuré doit tout de même être corrigé. Ainsi, il devient possible de libérer le port et de le réaffecter à un autre processus afin de restaurer les opérations. Le frontal apparaîtra avec le statut « STOP » sur la page de statistiques.

Le frontal peut être spécifié soit par son nom, soit par son identifiant numérique, précédé d'un dièse ('#').

Cette commande est restreinte et ne peut être émise que sur les sockets configurés au niveau « admin ».

<a id="entry-9-3-disable-health"></a>

**`disable health <backend>/<server>`**

```haproxy
disable health <backend>/<server>
```

Marquez le contrôle d'état principal comme étant temporairement arrêté. Cela désactivera l'envoi des contrôles d'état, et le dernier résultat de contrôle d'état sera ignoré. Le serveur sera en état non contrôlé et considéré comme UP, sauf si un contrôle d'état auxiliaire le force à descendre.

Cette commande est restreinte et ne peut être émise que sur les sockets configurés au niveau « admin ».

<a id="entry-9-3-disable-server"></a>

**`disable server <backend>/<server>`**

```haproxy
disable server <backend>/<server>
```

Marquez le serveur comme INDISPONIBLE pour maintenance. Dans ce mode, aucune vérification supplémentaire n’est effectuée sur le serveur jusqu’à ce qu’il quitte la maintenance. Si le serveur est suivi par d’autres serveurs, ceux-ci seront également marqués comme INDISPONIBLE pendant la maintenance.

Dans la page des statistiques, un serveur en maintenance apparaîtra avec un statut « MAINT », ses serveurs de suivi affichant quant à eux le statut « MAINT(via) ».

Le backend et le serveur peuvent chacun être spécifiés soit par leur nom, soit par leur identifiant numérique, précédé d'un dièse ('#').

Cette commande est restreinte et ne peut être émise que sur les sockets configurés au niveau « admin ».

<a id="entry-9-3-dump-ssl-cert"></a>

**`dump ssl cert <certfile>`**

```haproxy
dump ssl cert <certfile>
```

Affiche un certificat chargé en mémoire HAProxy. Cela affichera le certificat au format PEM, suivi de la clé privée, puis du certificat feuille, enfin de la chaîne sera affichée. Vous pouvez également afficher une transaction en préfixant le nom de fichier par un astérisque. Cela est utile pour sauvegarder des certificats sur le système de fichiers lorsqu’ils ont été mis à jour via l’interface CLI et non sur le système de fichiers.

Cette commande est restreinte et ne peut être émise que sur les sockets configurés au niveau « admin ».

Exemples :

```shell
$ echo "dump ssl cert cert1.pem" | socat /tmp/sock1 -

$ echo "dump ssl cert cert1.pem" | socat /tmp/sock1 - | openssl storeutl -noout -text /dev/stdin
```

<a id="entry-9-3-dump-stats-file"></a>

**`dump stats-file`**

```haproxy
dump stats-file
```

Génère un fichier de statistiques pouvant être utilisé pour charger les valeurs des compteurs HAProxy au démarrage. Consultez la section « Stats-file » pour plus de détails.

<a id="entry-9-3-echo"></a>

**`echo <text>`**

```haproxy
echo <text>
```

Affiche du texte avec l'interface en ligne de commande. Peut être utile pour écrire des commentaires entre les commandes lors de l'exportation du résultat de plusieurs commandes.

Exemple :

```text
echo "expert-mode on; echo FDs from fdtab; show fd; echo wild FDs; debug dev fd" | socat /var/run/haproxy.sock -

```

<a id="entry-9-3-enable-agent"></a>

**`enable agent <backend>/<server>`**

```haproxy
enable agent <backend>/<server>
```

Reprend le contrôle d'agent auxiliaire qui avait été temporairement arrêté.

Voir « disable agent » pour connaître les détails de l'effet du démarrage et de l'arrêt temporaires d'un agent auxiliaire.

Cette commande est restreinte et ne peut être émise que sur les sockets configurés au niveau « admin ».

<a id="entry-9-3-enable-dynamic-cookie-backend"></a>

**`enable dynamic-cookie backend <backend>`**

```haproxy
enable dynamic-cookie backend <backend>
```

Activez la génération de cookies dynamiques pour le backend `<backend>`. Une clé secrète doit également être fournie.

<a id="entry-9-3-enable-frontend"></a>

**`enable frontend <frontend>`**

```haproxy
enable frontend <frontend>
```

Reprendre un frontal qui a été temporairement arrêté. Il se peut que certains ports d'écoute ne puissent plus être liés (par exemple, si un autre processus les a pris depuis l'opération « désactiver le frontal »). Dans ce cas, une erreur est affichée. Certains systèmes d'exploitation ne peuvent pas reprendre un frontal qui a été désactivé.

Le frontal peut être spécifié soit par son nom, soit par son identifiant numérique, précédé d'un dièse ('#').

Cette commande est restreinte et ne peut être émise que sur les sockets configurés au niveau « admin ».

<a id="entry-9-3-enable-health"></a>

**`enable health <backend>/<server>`**

```haproxy
enable health <backend>/<server>
```

Reprendre un contrôle d'état principal qui a été temporairement arrêté. Cela permettra à nouveau l'envoi de contrôles d'état. Voir « disable health » pour plus de détails.

Cette commande est restreinte et ne peut être émise que sur les sockets configurés au niveau « admin ».

<a id="entry-9-3-enable-server"></a>

**`enable server <backend>/<server>`**

```haproxy
enable server <backend>/<server>
```

Si le serveur était précédemment marqué comme DOWN pour maintenance, cela le marque comme UP et réactive les vérifications.

Le backend et le serveur peuvent chacun être spécifiés soit par leur nom, soit par leur identifiant numérique, précédé d'un dièse ('#').

Cette commande est restreinte et ne peut être émise que sur les sockets configurés au niveau « admin ».

<a id="entry-9-3-experimental-mode"></a>

**`experimental-mode [on|off]`**

```haproxy
experimental-mode [on|off]
```

Sans option, cela indique si le mode expérimental est activé ou désactivé sur la connexion actuelle. En spécifiant « on », il active le mode expérimental pour la connexion CLI actuelle uniquement. Avec « off », il le désactive.

Le mode expérimental est utilisé pour accéder à des fonctionnalités supplémentaires encore en développement. Ces fonctionnalités sont actuellement instables et doivent être utilisées avec précaution. Elles peuvent être sujettes à des changements cassants entre les versions.

Lorsqu’il est utilisé depuis l’interface CLI principale, cette commande ne doit pas être préfixée, car elle définira le mode pour tout worker lors de sa connexion à son interface CLI.

Exemple :

```text
echo "@1; experimental-mode on; <experimental_cmd>..." | socat /var/run/haproxy.master -
echo "experimental-mode on; @1 <experimental_cmd>..." | socat /var/run/haproxy.master -
```

<a id="entry-9-3-expert-mode"></a>

**`expert-mode [on|off]`**

```haproxy
expert-mode [on|off]
```

Cette commande est similaire à experimental-mode, mais elle sert à activer ou désactiver le mode expert.

Le mode expert permet d’afficher des commandes experts qui peuvent être extrêmement dangereuses pour le processus et qui peuvent parfois aider les développeurs à recueillir des informations importantes sur des bogues complexes. Toute utilisation incorrecte de ces fonctionnalités entraîne probablement une panne du processus. N’utilisez pas cette option sans y être invité. Notez que cette commande est volontairement omise dans le message d’aide. Cette commande n’est accessible qu’au niveau administrateur. Passer à un autre niveau réinitialise automatiquement le mode expert.

Lorsqu’il est utilisé depuis l’interface CLI principale, cette commande ne doit pas être préfixée, car elle définira le mode pour tout worker lors de sa connexion à son interface CLI.

Exemple :

```text
echo "@1; expert-mode on; debug dev exit 1" | socat /var/run/haproxy.master -
echo "expert-mode on; @1 debug dev exit 1" | socat /var/run/haproxy.master -
```

<a id="entry-9-3-get-map"></a>

**`get map <map> <value>`**

```haproxy
get map <map> <value>
get acl <acl> <value>
```

Recherchez la valeur `<value>` dans la carte `<map>` ou dans la liste ACL `<acl>`. `<map>` ou `<acl>` correspondent au(s) `<id>` ou au `<name>` retourné(s) par la commande « show map » ou « show acl ». Cette commande renvoie tous les modèles correspondants associés à cette carte. Elle est utile pour le débogage des cartes et des listes ACL. Le format de sortie est composé d'une ligne par type correspondant. Chaque ligne est composée d'une série de mots séparés par des espaces.

Les deux premiers mots sont :

```text
<match method>:   Méthode de correspondance appliquée : "found", "bool",
                  "int", "ip", "bin", "len", "str", "beg", "sub", "dir",
                  "dom", "end" ou "reg".

<match result>:   Résultat : "match" ou "no-match".
```

Les mots suivants ne sont retournés que si le motif correspond à une entrée.

     `<index type>` : « tree » ou « list ». Algorithme interne de recherche.

     `<case>` : « case-insensitive » ou « case-sensitive ». Interprétation de la casse.

     `<entry matched>` : match="`<entry>`". Retourne le motif correspondant. Utile avec les expressions régulières.

Les deux derniers mots servent à indiquer la valeur renvoyée et son type. Dans le cas « acl », le modèle n'existe pas.

     return=nothing : Aucun retour, car aucune « map » n'est définie.
     return="`<value>`" : La valeur retournée au format chaîne.
     return=cannot-display : La valeur ne peut pas être convertie en chaîne.

     type="`<type>`":         Le type de l'échantillon renvoyé.

<a id="entry-9-3-get-var"></a>

**`get var <name>`**

```haproxy
get var <name>
```

Affiche l'existence, le type et le contenu de la variable globale du processus « name ». Seules les variables globales du processus sont lisibles, donc le nom doit commencer par 'proc.', sinon aucune variable ne sera trouvée. Cette commande nécessite les niveaux « operator » ou « admin ».

<a id="entry-9-3-get-weight"></a>

**`get weight <backend>/<server>`**

```haproxy
get weight <backend>/<server>
```

Rapporte le poids actuel et le poids initial du serveur `<server>` dans le backend `<backend>` ou une erreur si l’un des deux n’existe pas. Le poids initial est celui qui apparaît dans le fichier de configuration. Les deux sont normalement égaux sauf si le poids actuel a été modifié. Le backend et le serveur peuvent chacun être spécifiés soit par leur nom, soit par leur identifiant numérique, précédé d’un dièse ('#').

<a id="entry-9-3-help"></a>

**`help [<command>]`**

```haproxy
help [<command>]
```

Affiche la liste des mots-clés connus ainsi que leur utilisation basique, ou les commandes correspondant à celle demandée. L'écran d'aide est également affiché pour les commandes inconnues.

<a id="entry-9-3-httpclient"></a>

**`httpclient [--htx] <method> <URI>`**

```haproxy
httpclient [--htx] <method> <URI>
```

Lancez une requête HTTP et affichez la réponse sur la CLI. Pris en charge uniquement sur une connexion CLI en mode expert (voir « expert-mode on »). Destiné uniquement au débogage. L'outil httpclient est capable de résoudre un nom de serveur dans l'URL à l'aide de la section de résolution « default », qui est remplie par défaut avec les serveurs DNS de votre /etc/resolv.conf. Toutefois, il ne pourra pas résoudre un hôte provenant de /etc/hosts si vous n'utilisez pas un démon DNS local capable de résoudre ces noms.

L'option --htx permet d'utiliser la représentation interne HAProxy htx via la fonction htx_dump(), principalement utilisée pour le débogage.

<a id="entry-9-3-new-ssl-ca-file"></a>

**`new ssl ca-file <cafile>`**

```haproxy
new ssl ca-file <cafile>
```

Créez une nouvelle entrée vide dans l’arborescence de fichier de certificats CA, à remplir avec un ensemble de certificats CA et à ajouter à une liste crt. Cette commande doit être utilisée en combinaison avec « set ssl ca-file », « add ssl ca-file » et « add ssl crt-list ».

<a id="entry-9-3-new-ssl-cert"></a>

**`new ssl cert <filename>`**

```haproxy
new ssl cert <filename>
```

Créez un nouveau magasin de certificats SSL vide à remplir avec un certificat et à ajouter à un répertoire ou à une liste de certificats. Cette commande doit être utilisée en combinaison avec « set ssl cert » et « add ssl crt-list ».

<a id="entry-9-3-new-ssl-crl-file"></a>

**`new ssl crl-file <crlfile>`**

```haproxy
new ssl crl-file <crlfile>
```

Créez une nouvelle entrée vide dans l’arborescence de fichier CRL, destinée à être remplie par un ensemble de CRLs et ajoutée à une liste de certificats. Cette commande doit être utilisée en combinaison avec « set ssl crl-file » et « add ssl crt-list ».

<a id="entry-9-3-prepare-acl"></a>

**`prepare acl <acl>`**

```haproxy
prepare acl <acl>
```

Allouez un nouveau numéro de version dans la liste de contrôle d'accès `<acl>` pour une substitution atomique. `<acl>` est le \#`<id>` ou le `<name>` retourné par la commande « show acl ». Le nouveau numéro de version est indiqué dans la réponse après « Nouvelle version créée : ». Ce numéro pourra ensuite être utilisé pour préparer l'ajout de nouvelles entrées dans la liste de contrôle d'accès, qui remplaceront atomiquement les entrées actuelles une fois validées. Il est indiqué comme "next_ver" dans la commande « show acl ». L'allocation de nouvelles versions n'a aucun impact, car les versions non utilisées sont automatiquement supprimées dès qu'une version plus récente est validée. Les numéros de version sont des valeurs non signées sur 32 bits, qui bouclent en fin de plage, il convient donc de porter une attention particulière lors de leur comparaison dans un programme externe. Cette commande ne peut pas être utilisée si la référence `<acl>` est un nom également utilisé comme carte. Dans ce cas, la commande « prepare map » doit être utilisée à la place.

<a id="entry-9-3-prepare-map"></a>

**`prepare map <map>`**

```haproxy
prepare map <map>
```

Allouez un nouveau numéro de version dans la carte `<map>` pour une substitution atomique. `<map>` est le \#`<id>` ou le `<name>` retourné par la commande « show map ». Le nouveau numéro de version est indiqué dans la réponse après « New version created: ». Ce numéro pourra ensuite être utilisé pour préparer l’ajout de nouvelles entrées dans la carte, qui remplaceront atomiquement les entrées actuelles une fois validées. Il est indiqué comme "next_ver" dans la commande « show map ». L’allocation de nouvelles versions n’a aucun impact, car les versions non utilisées sont automatiquement supprimées dès qu’une version plus récente est validée. Les numéros de version sont des valeurs non signées sur 32 bits, qui bouclent en fin de plage, il convient donc de porter une attention particulière lors de leur comparaison dans un programme externe.

<a id="entry-9-3-prompt"></a>

**`prompt [help | n | i | p | timed]*`**

```haproxy
prompt [help | n | i | p | timed]*
```

Modifie le comportement du mode interactif et l’invite affichée au début de la ligne en mode interactif :   - « help » : affiche l’utilisation de la commande   - « n » : passe en mode non interactif   - « i » : passe en mode interactif   - « p » : passe en mode interactif + invite   - « timed » : active ou désactive l’affichage de l’heure dans l’invite

Sans option, le mode d'interaction passe successivement en mode interactif, puis en mode non interactif. En mode non interactif, la connexion est fermée après la fin de la dernière commande de la ligne courante. En mode interactif, la connexion n'est pas fermée après la fin d'une commande, afin de permettre l'entrée d'une nouvelle commande. En mode invite, le mode interactif est toujours utilisé, et une invite apparaît au début de la ligne, indiquant à l'utilisateur que l'interpréteur attend une nouvelle commande. L'invite se compose d'un chevron droit suivi d'un espace (« \> »).

Le mode invite convient davantage aux utilisateurs humains, le mode interactif aux scripts avancés, et le mode non interactif (par défaut) aux scripts basiques. Notez que le mode non interactif n'est pas disponible pour la socket principale.

<a id="entry-9-3-publish-backend"></a>

**`publish backend <backend>`**

```haproxy
publish backend <backend>
```

Active le commutateur de contenu vers une instance backend. Il s'agit de l'opération inverse de la commande « unpublish backend ». Cette commande est restreinte et ne peut être exécutée que sur les sockets configurés pour les niveaux « operator » ou « admin ».

<a id="entry-9-3-quit"></a>

**`quit`**

```haproxy
quit
```

Fermer la connexion en mode interactif.

<a id="entry-9-3-set-anon"></a>

**`set anon [on|off] [<key>]`**

```haproxy
set anon [on|off] [<key>]
```

Cette commande permet d’activer ou de désactiver le « mode anonymisé » pour la session CLI en cours, qui remplace certains champs jugés sensibles ou confidentiels dans les sorties de commandes par des hachages conservant une cohérence suffisante entre les éléments afin d’aider les développeurs à repérer des relations entre éléments lors de la recherche de bogues, tout en disposant d’un nombre de bits faible (24) pour rendre les hachages non réversibles en raison du grand nombre de correspondances possibles. Lorsqu’il est activé, si aucune clé n’est spécifiée, la clé globale sera utilisée (soit définie dans le fichier de configuration via « anonkey », soit définie via la commande CLI « set anon global-key »). Si aucune telle clé n’a été définie, une clé aléatoire sera générée. Sinon, il est possible de spécifier la clé 32 bits à utiliser pour la session en cours, par exemple pour réutiliser la clé utilisée dans un dump précédent afin de faciliter la comparaison des sorties. Les développeurs n’auront jamais besoin de cette clé, et il est recommandé de ne jamais la partager, car elle pourrait permettre de confirmer ou infirmer certaines hypothèses sur ce que certains hachages pourraient cacher.

<a id="entry-9-3-set-dynamic-cookie-key-backend"></a>

**`set dynamic-cookie-key backend <backend> <value>`**

```haproxy
set dynamic-cookie-key backend <backend> <value>
```

Modifiez la clé secrète utilisée pour générer les cookies persistants dynamiques. Cela interrompra les sessions en cours.

<a id="entry-9-3-set-anon-global-key"></a>

**`set anon global-key <key>`**

```haproxy
set anon global-key <key>
```

Cela définit la clé d'anonymisation globale sur `<key>`, qui doit être un entier 32 bits compris entre 0 et 4294967295 (0 désactive la clé globale). Cette commande nécessite des privilèges d'administrateur.

<a id="entry-9-3-set-map"></a>

**`set map <map> [<key>|#<ref>] <value>`**

```haproxy
set map <map> [<key>|#<ref>] <value>
```

Modifiez la valeur correspondant à chaque clé `<key>` dans une carte `<map>`. `<map>` est le \#`<id>` ou `<name>` retourné par la commande « show map ». Si `<ref>` est utilisé à la place de `<key>`, seule l'entrée pointée par `<ref>` est modifiée. La nouvelle valeur est `<value>`.

<a id="entry-9-3-set-maxconn-frontend"></a>

**`set maxconn frontend <frontend> <value>`**

```haproxy
set maxconn frontend <frontend> <value>
```

Modifiez dynamiquement la valeur maxconn du frontend spécifié. Toute valeur positive est autorisée, y compris zéro, mais définir une valeur supérieure à maxconn global n’a guère de sens. Si la limite est augmentée et qu’il y a des connexions en attente, celles-ci seront immédiatement acceptées. Si elle est réduite à une valeur inférieure au nombre actuel de connexions, l’acceptation de nouvelles connexions sera reportée jusqu’à atteinte du seuil. Le frontend peut être spécifié soit par son nom, soit par son identifiant numérique précédé d’un dièse ('#').

<a id="entry-9-3-set-maxconn-server"></a>

**`set maxconn server <backend/server> <value>`**

```haproxy
set maxconn server <backend/server> <value>
```

Modifiez dynamiquement le paramètre maxconn du serveur spécifié. Toute valeur positive est autorisée, y compris zéro, mais définir une valeur supérieure au maxconn global n’a guère de sens.

<a id="entry-9-3-set-maxconn-global"></a>

**`set maxconn global <maxconn>`**

```haproxy
set maxconn global <maxconn>
```

Modifiez dynamiquement le paramètre global maxconn dans la plage définie par la valeur initiale de maxconn. Si cette valeur est augmentée et qu’il y a des connexions en attente, celles-ci seront immédiatement acceptées. Si elle est réduite à une valeur inférieure au nombre actuel de connexions, l’acceptation des nouvelles connexions sera retardée jusqu’à atteinte du seuil. Une valeur nulle restaure le paramètre initial.

<a id="entry-9-3-set-profiling-memory"></a>

**`set profiling memory { on | off }`**

```haproxy
set profiling memory { on | off }
set profiling tasks { auto | on | off | lock | no-lock | memory | no-memory }
```

Active ou désactive le profilage CPU ou mémoire pour le sous-système indiqué. Cela équivaut à définir ou supprimer les paramètres « profiling » dans la section « global » du fichier de configuration.
Voir également « show profiling ». Notez qu'une activation manuelle du profilage des tâches sur « on » réinitialise automatiquement les statistiques du planificateur, permettant ainsi de mesurer l'activité sur une période donnée.
Le profilage mémoire est limité à certains systèmes d'exploitation (fonctionne notamment sur la cible linux-glibc) et nécessite que USE_MEMORY_PROFILING soit défini au moment de la compilation.

Pour le profilage des tâches, il est possible d’activer ou de désactiver en temps réel la collecte des mesures de verrouillage et de mémoire par tâche, mais le changement n’est pris en compte qu’à la prochaine transition du profilage de « désactivé »/« auto » vers « activé » (soit automatiquement, soit manuellement). Ainsi, lorsqu’on utilise « no-lock » pour désactiver le profilage du verrouillage par tâche et économiser des cycles CPU, il est recommandé de désactiver puis réactiver le profilage des tâches afin de valider le changement.

<a id="entry-9-3-set-rate-limit-connections-global"></a>

**`set rate-limit connections global <value>`**

```haproxy
set rate-limit connections global <value>
```

Modifiez la limite de débit de connexions à l’échelle du processus, définie par le paramètre global « maxconnrate ». Une valeur nulle désactive la limitation. Cette limite s’applique à tous les frontaux et le changement prend effet immédiatement. La valeur est exprimée en nombre de connexions par seconde.

<a id="entry-9-3-set-rate-limit-http-compression-global"></a>

**`set rate-limit http-compression global <value>`**

```haproxy
set rate-limit http-compression global <value>
```

Modifiez le taux maximal de compression d'entrée, défini par le paramètre global « maxcomprate ». Une valeur nulle désactive la limitation. La valeur est exprimée en kilo-octets par seconde. Elle est disponible dans la commande « show info », sur la ligne « CompressBpsRateLim », en octets.

<a id="entry-9-3-set-rate-limit-sessions-global"></a>

**`set rate-limit sessions global <value>`**

```haproxy
set rate-limit sessions global <value>
```

Modifiez la limite de taux de sessions au niveau du processus, définie par le paramètre global « maxsessrate ». Une valeur nulle désactive la limitation. Cette limite s'applique à tous les frontaux et le changement prend effet immédiatement. La valeur est exprimée en nombre de sessions par seconde.

<a id="entry-9-3-set-rate-limit-ssl-sessions-global"></a>

**`set rate-limit ssl-sessions global <value>`**

```haproxy
set rate-limit ssl-sessions global <value>
```

Modifiez la limite de débit des sessions SSL à l’échelle du processus, définie par le paramètre global « maxsslrate ». Une valeur nulle désactive la limitation. Cette limite s’applique à tous les frontaux et prend effet immédiatement. La valeur est exprimée en nombre de sessions par seconde envoyées à la pile SSL. Elle s’applique avant l’établissement de la connexion afin de protéger la pile contre les abus liés à l’établissement de connexion.

<a id="entry-9-3-set-server"></a>

**`set server <backend>/<server> addr <ip4 or ip6 address> [port <port>]`**

```haproxy
set server <backend>/<server> addr <ip4 or ip6 address> [port <port>]
```

Remplacez l'adresse IP actuelle d'un serveur par celle fournie. Le port peut éventuellement être modifié à l'aide du paramètre « port ». Notez qu'un changement de port permet également de basculer entre le mappage de port (notation avec +X ou -Y), à condition qu'un port soit configuré pour le contrôle d'état.

<a id="entry-9-3-set-server-2"></a>

**`set server <backend>/<server> agent [ up | down ]`**

```haproxy
set server <backend>/<server> agent [ up | down ]
```

Forcer l'agent d'un serveur à un nouvel état. Cela peut être utile pour basculer immédiatement l'état d'un serveur, indépendamment de vérifications d'agent lentes, par exemple. Notez que le changement est propagé aux serveurs de suivi, le cas échéant.

<a id="entry-9-3-set-server-3"></a>

**`set server <backend>/<server> agent-addr <addr> [port <port>]`**

```haproxy
set server <backend>/<server> agent-addr <addr> [port <port>]
```

Modifie l'adresse des vérifications d'agent des serveurs. Permet de migrer les vérifications d'agent vers une autre adresse en temps réel.
Vous pouvez spécifier à la fois une adresse IP et un nom d'hôte, qui sera résolu. Facultativement, modifiez le port de l'agent.

<a id="entry-9-3-set-server-4"></a>

**`set server <backend>/<server> agent-port <port>`**

```haproxy
set server <backend>/<server> agent-port <port>
```

Modifiez le port utilisé pour les vérifications de l'agent.

<a id="entry-9-3-set-server-5"></a>

**`set server <backend>/<server> agent-send <value>`**

```haproxy
set server <backend>/<server> agent-send <value>
```

Modifie la chaîne d'agent envoyée à la cible de vérification de l'agent. Permet de mettre à jour la chaîne tout en modifiant l'adresse du serveur afin de maintenir les deux synchronisées.

<a id="entry-9-3-set-server-6"></a>

**`set server <backend>/<server> health [ up | stopping | down ]`**

```haproxy
set server <backend>/<server> health [ up | stopping | down ]
```

Forcer l'état de contrôle d'état d'un serveur à une nouvelle valeur. Cela peut être utile pour modifier immédiatement l'état d'un serveur, indépendamment de contrôles d'état lents, par exemple. Notez que le changement est propagé aux serveurs de suivi, le cas échéant.

<a id="entry-9-3-set-server-7"></a>

**`set server <backend>/<server> check-addr <ip4 | ip6> [port <port>]`**

```haproxy
set server <backend>/<server> check-addr <ip4 | ip6> [port <port>]
```

Modifiez l'adresse IP utilisée pour les contrôles d'état des serveurs. Facultativement, modifiez le port utilisé pour les contrôles d'état des serveurs.

<a id="entry-9-3-set-server-8"></a>

**`set server <backend>/<server> check-port <port>`**

```haproxy
set server <backend>/<server> check-port <port>
```

Modifiez le port utilisé pour le contrôle d'état en `<port>`

<a id="entry-9-3-set-server-9"></a>

**`set server <backend>/<server> state [ ready | drain | maint ]`**

```haproxy
set server <backend>/<server> state [ ready | drain | maint ]
```

Forcer l’état administratif d’un serveur vers un nouvel état. Cela peut être utile pour désactiver la répartition de charge et/ou tout trafic vers un serveur. Définir l’état sur « ready » place le serveur en mode normal, et la commande équivaut à la commande « enable server ». Définir l’état sur « maint » désactive tout trafic vers le serveur ainsi que tout contrôle d’état. Cela équivaut à la commande « disable server ». Définir le mode sur « drain » retire uniquement le serveur de la répartition de charge, mais permet toujours son contrôle d’état et l’acceptation de nouvelles connexions persistantes. Les modifications sont propagées aux serveurs de suivi s’il y en a.

<a id="entry-9-3-set-server-10"></a>

**`set server <backend>/<server> weight <weight>[%]`**

```haproxy
set server <backend>/<server> weight <weight>[%]
```

Modifie le poids d'un serveur par la valeur passée en argument. Cela correspond exactement à la commande « set weight » ci-dessous.

<a id="entry-9-3-set-server-11"></a>

**`set server <backend>/<server> fqdn <FQDN>`**

```haproxy
set server <backend>/<server> fqdn <FQDN>
```

Modifie le nom DNS complet (FQDN) d'un serveur par la valeur passée en argument. Cela nécessite que le résolveur DNS interne soit configuré et activé pour ce serveur.

<a id="entry-9-3-set-server-12"></a>

**`set server <backend>/<server> ssl [ on | off ]  (deprecated)`**

```haproxy
set server <backend>/<server> ssl [ on | off ]  (deprecated)
```

Cette option configure le chiffrement SSL des connexions sortantes vers le serveur. Lorsqu'elle est désactivée, tout le trafic devient en clair ; le chemin de contrôle d'état n'est pas modifié.

Cette commande est obsolète. Créez un serveur dynamiquement, avec ou sans SSL, à l’aide de la commande « add server » à la place.

<a id="entry-9-3-set-severity-output"></a>

**`set severity-output [ none | number | string ]`**

```haproxy
set severity-output [ none | number | string ]
```

Modifie le format de sortie de la sévérité du socket de statistiques connecté pour la durée de la session en cours.

<a id="entry-9-3-set-ssl-ca-file"></a>

**`set ssl ca-file <cafile> <payload>`**

```haproxy
set ssl ca-file <cafile> <payload>
```

Cette commande fait partie d’un système de transactions : les commandes « commit ssl ca-file » et « abort ssl ca-file » peuvent être requises. Si aucune transaction en cours n’existe, une entrée de fichier CA sera créée dans l’arborescence des fichiers CA, dans laquelle les certificats contenus dans le chargement seront stockés. L’entrée de fichier CA ne sera pas conservée dans l’arborescence des fichiers CA et ne sera stockée que dans une transaction temporaire. Si une transaction portant le même nom de fichier existe déjà, l’entrée de fichier CA précédente sera supprimée et remplacée par la nouvelle. Une fois les modifications effectuées, vous devez valider la transaction à l’aide d’un appel à « commit ssl ca-file ». Si vous souhaitez ajouter plusieurs certificats séparément, vous pouvez utiliser la commande « add ssl ca-file ».

Exemple :

```text
echo -e "set ssl ca-file cafile.pem <<\n$(cat rootCA.crt)\n" | \
socat /var/run/haproxy.stat -
echo "commit ssl ca-file cafile.pem" | socat /var/run/haproxy.stat -
```

<a id="entry-9-3-set-ssl-cert"></a>

**`set ssl cert <filename> <payload>`**

```haproxy
set ssl cert <filename> <payload>
```

Cette commande fait partie d’un système de transaction : les commandes « commit ssl cert » et « abort ssl cert » peuvent être nécessaires. Ce système de transaction fonctionne sur n’importe quel certificat affiché par la commande « show ssl cert », c’est-à-dire sur n’importe quel certificat frontal ou backend. Si aucune transaction en cours n’existe, elle dupliquerait le certificat `<filename>` en mémoire vers une transaction temporaire, puis mettrait à jour cette transaction avec le fichier PEM contenu dans le payload. Si une transaction existe déjà avec le même nom de fichier, elle mettra à jour cette transaction. Il est également possible de mettre à jour les fichiers liés à un certificat (.issuer, .sctl, .ocsp, etc.). Une fois les modifications effectuées, vous devez « commit ssl cert » la transaction.

L'injection de fichiers via la ligne de commande doit se faire avec précaution, car une ligne vide est utilisée pour signaler la fin du contenu. Il est recommandé d'injecter un fichier PEM ayant été nettoyé. Une méthode simple consiste à supprimer toutes les lignes vides et à ne conserver que les sections PEM. Cette opération peut être réalisée à l'aide d'une commande sed.

Exemple :

```haproxy
# With some simple sanitizing
 echo -e "set ssl cert localhost.pem <<\n$(sed -n '/^$/d;/-BEGIN/,/-END/p' 127.0.0.1.pem)\n" | \
 socat /var/run/haproxy.stat -

 # Complete example with commit
 echo -e "set ssl cert localhost.pem <<\n$(cat 127.0.0.1.pem)\n" | \
 socat /var/run/haproxy.stat -
 echo -e \
 "set ssl cert localhost.pem.issuer <<\n $(cat 127.0.0.1.pem.issuer)\n" | \
 socat /var/run/haproxy.stat -
 echo -e \
 "set ssl cert localhost.pem.ocsp <<\n$(base64 -w 1000 127.0.0.1.pem.ocsp)\n" | \
 socat /var/run/haproxy.stat -
 echo "commit ssl cert localhost.pem" | socat /var/run/haproxy.stat -
```

<a id="entry-9-3-set-ssl-crl-file"></a>

**`set ssl crl-file <crlfile> <payload>`**

```haproxy
set ssl crl-file <crlfile> <payload>
```

Cette commande fait partie d’un système de transactions : les commandes « commit ssl crl-file » et « abort ssl crl-file » peuvent être nécessaires. Si aucune transaction en cours n’existe, une entrée d’arborescence de fichier CRL sera créée, dans laquelle les listes de révocation contenues dans le payload seront stockées. L’entrée de fichier CRL ne sera pas conservée dans l’arborescence de fichiers CRL et ne sera stockée que dans une transaction temporaire. Si une transaction portant le même nom de fichier existe déjà, l’entrée de fichier CRL précédente sera supprimée et remplacée par la nouvelle. Une fois les modifications effectuées, vous devez valider la transaction à l’aide d’un appel à « commit ssl crl-file ».

Exemple :

```text
echo -e "set ssl crl-file crlfile.pem <<\n$(cat rootCRL.pem)\n" | \
socat /var/run/haproxy.stat -
echo "commit ssl crl-file crlfile.pem" | socat /var/run/haproxy.stat -
```

<a id="entry-9-3-set-ssl-ech"></a>

**`set ssl ech <bind> <payload>`**

```haproxy
set ssl ech <bind> <payload>
```

Remplacez les clés ECH d'une ligne bind par celle-ci. Le contenu doit être au format PEM pour ECH.
(<https://datatracker.ietf.org/doc/html/draft-farrell-tls-pemesni>)

Le format de la ligne bind est `<frontend>`/@`<filename>`:`<linenum>` (exemple : frontend1/@haproxy.conf:19)
ou `<frontend>`/`<name>` si la ligne bind a été nommée avec le mot-clé « name ».

Exige une version d'OpenSSL qui prend en charge ECH, et HAProxy doit être compilé avec USE_ECH=1.
Cette commande n'est prise en charge que sur une connexion CLI en mode expérimental (voir « experimental-mode on »).

Voir également « show ssl ech », « add ssl ech » et « ech » dans la [Section 5.1](/fr/haproxy/bind-and-server-options/#section-5-1) du manuel de configuration.

    $ openssl ech -public_name foobar.com -out foobar3.com.ech
    $ echo -e "experimental-mode on;
               set ssl ech frontend1/@haproxy.conf:19 <<%EOF%&#92;n$(cat foobar3.com.ech)&#92;n%EOF%&#92;n" | &#92;
      socat /tmp/haproxy.sock -
    set new ECH configs for frontend1/@haproxy.conf:19

<a id="entry-9-3-set-ssl-ocsp-response"></a>

**`set ssl ocsp-response <response | payload>`**

```haproxy
set ssl ocsp-response <response | payload>
```

Cette commande permet de mettre à jour une réponse OCSP pour un certificat (voir « crt » dans les lignes « bind »). Les mêmes contrôles sont effectués qu’à l’initialisation du chargement de la réponse. Le `<response>` doit être transmis sous forme d’une chaîne encodée en base64 de la réponse encodée en DER provenant du serveur OCSP. Cette commande n’est pas prise en charge avec BoringSSL.

Exemple :

```text
openssl ocsp -issuer issuer.pem -cert server.pem \
             -host ocsp.issuer.com:80 -respout resp.der
echo "set ssl ocsp-response $(base64 -w 10000 resp.der)" | \
             socat stdio /var/run/haproxy.stat

avec la syntaxe de charge utile :
echo -e "set ssl ocsp-response <<\n$(base64 resp.der)\n" | \
             socat stdio /var/run/haproxy.stat
```

<a id="entry-9-3-set-ssl-tls-key"></a>

**`set ssl tls-key <id> <tlskey>`**

```haproxy
set ssl tls-key <id> <tlskey>
```

Définissez la prochaine clé TLS pour l'écouteur `<id>` sur `<tlskey>`. Cette clé devient la clé finale, tandis que la clé précédente est utilisée pour le chiffrement (les autres ne servent qu'à déchiffrer). La clé TLS la plus ancienne présente est remplacée. `<id>` est soit un entier \#`<id>`, soit `<file>`, renvoyé par la commande « show tls-keys ». `<tlskey>` est une clé de billet TLS codée en base64 sur 48 ou 80 octets (par exemple : openssl rand 80 \| openssl base64 -A).

<a id="entry-9-3-set-table"></a>

**`set table <table> key <key> [data.<data_type> <value>]*`**

```haproxy
set table <table> key <key> [data.<data_type> <value>]*
set table <table> ptr <ptr> [data.<data_type> <value>]*
```

Crée ou met à jour une entrée dans la table de persistance. Si la clé n'est pas présente, une entrée est insérée.
Consultez stick-table dans la section 4.2 pour obtenir la liste de toutes les valeurs possibles pour `<data_type>`. L'utilisation la plus courante consiste à insérer dynamiquement des entrées pour les adresses IP sources, avec un indicateur dans gpc0 afin de bloquer dynamiquement une adresse IP ou d'en modifier la qualité de service. Il est possible de transmettre plusieurs data_types dans un appel unique.

Une recherche par pointeur peut être utilisée à la place de la recherche par clé pour une entrée existante : `<ptr>` doit être spécifié sous la forme 0xffff et correspond au pointeur retourné par une commande précédente « show table ». Une correspondance par pointeur peut être pertinente si l'entrée ne peut pas être identifiée par sa clé en raison d'une clé vide ou de caractères incompatibles sur le CLI.

Si data.`<data_type>` est de type tableau, les crochets « [] » peuvent être utilisés pour accéder à un index spécifique du tableau, comme ceci : data.gpt[1]

<a id="entry-9-3-set-timeout-cli"></a>

**`set timeout cli <delay>`**

```haproxy
set timeout cli <delay>
```

Modifie le délai d'expiration de l'interface CLI pour la connexion actuelle. Cela peut être utile lors de sessions de débogage longues, où l'utilisateur doit inspecter continuellement certains indicateurs sans être déconnecté. Le délai est spécifié en secondes.

<a id="entry-9-3-set-var"></a>

**`set var <name> <expression>`**

```haproxy
set var <name> <expression>
set var <name> expr <expression>
set var <name> fmt <format>
```

Permet de définir ou de remplacer la variable globale « name » par le résultat de l'expression
`<expression>` ou de la chaîne de format `<format>`. Seules les variables globales peuvent être utilisées, donc le nom
doit commencer par 'proc.', sinon aucune variable ne sera définie. Les `<expression>` et `<format>` ne peuvent
impliquer que des mots-clés d'extraction d'échantillon « internes » et des convertisseurs, même si les plus utiles seront probablement str('quelque chose'), int(), des chaînes simples ou des références à d'autres variables. Notez que le parseur de ligne de commande ne connaît pas les guillemets, donc tout espace dans l'expression doit être précédé d'une barre oblique inverse. Cette commande nécessite les niveaux « operator » ou « admin ». Cette commande n'est prise en charge que sur une connexion CLI en mode expérimental (voir « experimental-mode on »).

<a id="entry-9-3-set-weight"></a>

**`set weight <backend>/<server> <weight>[%]`**

```haproxy
set weight <backend>/<server> <weight>[%]
```

Modifie le poids d'un serveur à la valeur passée en argument. Si la valeur se termine par le signe '%', le nouveau poids sera relatif au poids initialement configuré. Les poids absolus sont autorisés entre 0 et 256. Les poids relatifs doivent être positifs, et le poids absolu résultant est plafonné à 256. Les serveurs faisant partie d'une ferme utilisant un algorithme de répartition de charge statique ont des limitations plus strictes, car le poids ne peut pas être modifié une fois fixé. Pour ces serveurs, les seules valeurs acceptées sont 0 et 100 % (ou 0 et le poids initial). Les modifications prennent effet immédiatement, bien que certains algorithmes de répartition de charge nécessitent un certain nombre de requêtes pour prendre en compte les changements. Une utilisation typique de cette commande consiste à désactiver un serveur pendant une mise à jour en lui attribuant un poids de zéro, puis à le réactiver après la mise à jour en le ramenant à 100 %. Cette commande est restreinte et ne peut être exécutée que sur les sockets configurés au niveau "admin". Le backend et le serveur peuvent chacun être spécifiés soit par leur nom, soit par leur identifiant numérique, précédé d'un dièse ('#').

<a id="entry-9-3-show-acl"></a>

**`show acl [[@<ver>] <acl>]`**

```haproxy
show acl [[@<ver>] <acl>]
```

Informations sur les convertisseurs d'ACL. Sans argument, la liste de toutes les ACL disponibles est renvoyée. Si un `<acl>` est spécifié, son contenu est affiché. `<acl>` est le \#`<id>` ou `<name>`. Par défaut, la version actuelle de l'ACL est affichée (la version actuellement en cours de correspondance et signalée comme 'curr_ver' dans la liste des ACL). Il est possible de plutôt afficher d'autres versions en préfixant '@`<ver>`' à l'identifiant de l'ACL. La version agit comme un filtre et les versions inexistantes ne renvoient simplement aucun résultat. Le format de sortie est identique à celui des cartes, y compris pour les valeurs d'exemple. Les données renvoyées ne constituent pas une liste des ACL disponibles, mais la liste de tous les modèles composant n'importe quelle ACL. Beaucoup de ces modèles peuvent être partagés avec les cartes. La valeur 'entry_cnt' représente le nombre total d'entrées ACL, pas seulement les entrées actives, ce qui signifie qu'elle inclut également les entrées actuellement en cours d'ajout.

<a id="entry-9-3-show-anon"></a>

**`show anon`**

```haproxy
show anon
```

Affiche l'état actuel du mode d'anonymisation (activé ou désactivé) ainsi que la clé de la session en cours.

<a id="entry-9-3-show-backend"></a>

**`show backend`**

```haproxy
show backend
```

Affiche la liste des backends disponibles dans le processus en cours d'exécution

<a id="entry-9-3-show-cli-level"></a>

**`show cli level`**

```haproxy
show cli level
```

Affiche le niveau CLI de la session CLI en cours. Le résultat peut être « admin », « operator » ou « user ».
Voir également les commandes « operator » et « user ».

Exemple :

```shell
$ socat /tmp/sock1 readline
prompt
> operator
> show cli level
operator
> user
> show cli level
user
> operator
Permission denied
```

<a id="entry-9-3-operator"></a>

**`operator`**

```haproxy
operator
```

Réduit le niveau CLI de la session CLI en cours à opérateur. Ce niveau ne peut pas être augmenté. Désactive également les modes expert et expérimental. Voir également « show cli level ».

<a id="entry-9-3-unpublish-backend"></a>

**`unpublish backend <backend>`**

```haproxy
unpublish backend <backend>
```

Marque le backend comme non qualifié pour la sélection du trafic futur. En pratique, les règles use_backend / default_backend qui le référencent sont ignorées et les règles de commutation de contenu suivantes sont évaluées. Contrairement aux backends désactivés, les contrôles d'état des serveurs restent actifs. Cette commande est restreinte et ne peut être émise que sur les sockets configurés pour les niveaux « operator » ou « admin ».

<a id="entry-9-3-user"></a>

**`user`**

```haproxy
user
```

Réduit le niveau CLI de la session CLI en cours à l'utilisateur. Ce niveau ne peut pas être augmenté. Désactive également les modes expert et expérimental. Voir également « show cli level ».

<a id="entry-9-3-show-activity"></a>

**`show activity [-1 | 0 | thread_num]`**

```haproxy
show activity [-1 | 0 | thread_num]
```

Rapporte certains compteurs relatifs aux événements internes qui aideront les développeurs et plus généralement toute personne suffisamment familière avec HAProxy à diagnostiquer les causes de comportements anormaux. Un exemple typique serait un processus correctement exécuté qui ne s'endort jamais et consomme 100 % du CPU. Les champs de sortie seront composés d'une ligne par métrique, avec les compteurs par thread sur la même ligne. Ces compteurs sont sur 32 bits et peuvent déborder au cours de la durée de vie du processus, ce qui n'est pas problématique car les appels à cette commande seront typiquement effectués deux fois. Les champs ne sont pas documentés intentionnellement afin que leur signification exacte soit vérifiée dans le code où les compteurs sont mis à jour. Ces valeurs sont également réinitialisées par la commande « clear counters ». Dans les déploiements multi-thread, la première colonne indiquera la valeur agrégée (ou la moyenne selon la nature de la métrique) pour tous les threads, et la liste des valeurs de chaque thread sera affichée entre crochets dans l'ordre des threads. Un numéro de thread optionnel peut être spécifié en argument. La valeur spéciale « 0 » rapportera uniquement la valeur agrégée (première colonne), et « -1 », qui est la valeur par défaut, affichera toutes les colonnes. Notez qu’à l’instar du mode mono-thread, il n’y aura pas de crochets lorsque seule une colonne est demandée.

<a id="entry-9-3-show-cli-sockets"></a>

**`show cli sockets`**

```haproxy
show cli sockets
```

Liste les sockets CLI. Le format de sortie est composé de 3 champs séparés par des espaces. Le premier champ est l'adresse de la socket, qui peut être une socket Unix, un couple adresse IPv4:port ou une adresse IPv6. Les sockets de types autres ne seront pas affichées. Le deuxième champ décrit le niveau de la socket : « admin », « user » ou « operator ». Le dernier champ liste les processus auxquels la socket est liée, séparés par des virgules, pouvant être des numéros ou « all ».

Exemple :

```shell
$ echo 'show cli sockets' | socat stdio /tmp/sock1
# socket lvl processes
/tmp/sock1 admin all
127.0.0.1:9999 user 2,3,4
127.0.0.2:9969 user 2
[::1]:9999 operator 2
```

<a id="entry-9-3-show-cache"></a>

**`show cache`**

```haproxy
show cache
```

Listez les caches configurés et les objets stockés dans chaque arbre de cache.

\$ echo 'show cache' \| socat stdio /tmp/sock1 0x7f6ac6c5b03a: foobar (shctx:0x7f6ac6c5b000,
available blocks:3918) 1 2 3 4

1.  pointeur vers la structure de cache
2.  nom du cache
3.  pointeur vers la zone mmap (shctx)
4.  nombre de blocs disponibles pour être réutilisés dans le shctx

0x7f6ac6c5b4cc hash:286881868 vary:0x0011223344556677 size:39114 (39 blocks), refcount:9, expire:237
1 2 3 4 5 6 7

1.  pointeur vers l'entrée du cache
2.  premiers 32 bits du hachage
3.  hachage secondaire de l'entrée en cas de variation
4.  taille de l'objet en octets
5.  nombre de blocs utilisés pour l'objet
6.  nombre de transactions utilisant l'entrée
7.  heure d'expiration, peut être négatif si déjà expiré

<a id="entry-9-3-show-dev"></a>

**`show dev`**

```haproxy
show dev
```

Cette commande a pour objectif de centraliser certaines informations que les développeurs HAProxy pourraient nécessiter pour mieux comprendre les causes d’un problème donné. Elle ne fournit généralement pas d’information utile à l’utilisateur, mais ces données permettent aux développeurs d’éliminer certaines hypothèses. Le format est approximativement une série de sections contenant des lignes indentées, une seule valeur par ligne, comme le type et la version du système d’exploitation, le type de processeur ou les limites de descripteurs d’ouverture au démarrage, par exemple. Certains champs seront omis afin d’éviter la répétition ou la pollution de la sortie lorsqu’ils ne contribuent pas à la valeur (par exemple, les valeurs illimitées). D’autres champs pourront apparaître à l’avenir, et certains pourront évoluer. Cette sortie n’est pas destinée à être analysée par des scripts, et ne doit pas être considérée avec un haut degré de fiabilité ; elle vise essentiellement à économiser du temps pour ceux qui peuvent la lire.

Techniquement parlant, ces informations sont prises telles quelles à partir d'une structure interne qui les stocke ensemble au démarrage, afin qu'elles puissent également être trouvées dans un fichier core après un plantage. Il peut donc arriver que les développeurs demandent une sortie précoce sur un processus bien comporté afin de la comparer avec ce qui est trouvé dans un dump core, ou de la comparer entre plusieurs rechargements (par exemple, certaines limites pourraient changer). Si l'anonymisation est activée, toute valeur potentiellement sensible sera également anonymisée (par exemple, le nom du nœud).

Exemple de sortie :

```shell
$ socat stdio /tmp/sock1 <<< "show dev"
Platform info
  machine vendor: To be filled by O.E.M
  machine family: Altra
  cpu model: Impl 0x41 Arch 8 Part 0xd0c r3p1
  virtual machine: no
  container: no
  OS name: Linux
  OS release: 6.2.0-36-generic
  OS version: #37~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  9 18:01:07 UTC 2
  OS architecture: aarch64
  node name: 489aaf
Process info
  pid: 1735846
  boot uid: 509
  boot gid: 1002
  fd limit (soft): 1024
  fd limit (hard): 1048576
```

<a id="entry-9-3-show-env"></a>

**`show env [<name>]`**

```haproxy
show env [<name>]
```

Affiche une ou toutes les variables d’environnement connues par le processus. Sans argument, toutes les variables sont affichées. Avec un argument, seule la variable spécifiée est affichée si elle existe. Sinon, le message « Variable non trouvée » est émis. Les variables sont affichées au format utilisé pour les stocker ou les renvoyer par l’outil « env », à savoir « `<name>`=`<value>` ». Cette commande peut être utile lors du débogage de certains fichiers de configuration utilisant abondamment des variables d’environnement afin de vérifier qu’elles contiennent les valeurs attendues. Cette commande est restreinte et ne peut être exécutée que sur les sockets configurés pour les niveaux « operator » ou « admin ».

<a id="entry-9-3-show-errors"></a>

**`show errors [<iid>|<proxy>] [request|response]`**

```haproxy
show errors [<iid>|<proxy>] [request|response]
```

Dump les dernières erreurs de requête et de réponse HTTP/1.x collectées par les frontaux et les backends. Si `<iid>` est spécifié, limiter le dump aux erreurs concernant soit le frontend, soit le backend dont l'ID est `<iid>`. L'ID de proxy "-1" provoquera le dump de toutes les instances. Si un nom de proxy est spécifié à la place, son ID sera utilisé comme filtre. Si "request" ou "response" est ajouté après le nom de proxy ou son ID, seules les erreurs de requête ou de réponse seront dumpées. Cette commande est restreinte et ne peut être exécutée que sur des sockets configurés pour les niveaux "operator" ou "admin".

Les erreurs qui peuvent être collectées sont les dernières erreurs de requête et de réponse provoquées par des violations de protocole, souvent dues à des caractères non valides dans les noms d’en-tête. Le rapport indique précisément quel caractère exact a violé le protocole. D'autres informations importantes, telles que la date exacte à laquelle l'erreur a été détectée, les noms du frontal et du backend, le nom du serveur (lorsqu'il est connu), l'identifiant de transaction interne et l'adresse source ayant initié la session, sont également rapportées.

Tous les caractères sont renvoyés, et les caractères non imprimables sont encodés. Les plus courants
(&#92;t = 9, &#92;n = 10, &#92;r = 13 et &#92;e = 27) sont encodés sous la forme d'une lettre suivie d'une barre oblique inverse. La barre oblique inverse elle-même est encodée par '&#92;&#92;' afin d'éviter toute confusion. Les autres caractères non imprimables sont encodés sous la forme '&#92;xNN', où NN représente la représentation hexadécimale sur deux chiffres du code ASCII du caractère.

Les lignes sont précédées de la position de leur premier caractère, à partir de 0 pour le début du tampon. Au plus une ligne d'entrée est affichée par ligne, et les lignes longues sont divisées en plusieurs lignes de sortie consécutives afin que la sortie n'excède jamais 79 caractères de large. Il est facile de détecter si une ligne a été coupée, car elle ne se termine pas par '&#92;n' et l'offset de la ligne suivante est suivi d'un signe '+', indiquant qu'elle est une continuation de la ligne précédente.

Exemple :

```shell
    $ echo "show errors -1 response" | socat stdio /tmp/sock1
>>> [04/Mar/2009:15:46:56.081] backend http-in (#2): invalid response
      src 127.0.0.1, session #54, frontend fe-eth0 (#1), server s2 (#1)
      response length 213 bytes, error at position 23:

      00000  HTTP/1.0 200 OK\r\n
      00017  header/bizarre:blah\r\n
      00038  Location: blah\r\n
      00054  Long-line: this is a very long line which should b
      00104+ e broken into multiple lines on the output buffer,
      00154+  otherwise it would be too large to print in a ter
      00204+ minal\r\n
      00211  \r\n

Dans l'exemple ci-dessus, le backend "http-in", d'ID interne 2, a bloqué
une réponse invalide de son serveur s2, d'ID interne 1. La requête
appartenait à la transaction 54 (appelée "session" ici), initiée par
la source 127.0.0.1 et reçue par le frontend fe-eth0, dont l'ID est 1.
La longueur totale de réponse était de 213 octets lors de la détection
de l'erreur, située à l'octet 23 : la barre oblique ('/') du nom
d'en-tête "header/bizarre", caractère HTTP invalide dans un nom d'en-tête.
```

<a id="entry-9-3-show-events"></a>

**`show events [<sink>] [-w] [-n] [-0] [-s]`**

```haproxy
show events [<sink>] [-w] [-n] [-0] [-s]
```

Sans option, cette commande liste tous les réceptacles d’événements connus ainsi que leurs types. Avec une option, elle affiche tous les événements disponibles dans le réceptacle désigné, si celui-ci est de type tampon. Si l’option "-w" est passée après le nom du réceptacle, une fois la fin du tampon atteinte, la commande attend de nouveaux événements et les affiche. Il est possible d’interrompre l’opération en saisissant une entrée (qui sera ignorée) ou en fermant la session. Enfin, l’option "-n" permet de se positionner directement à la fin du tampon, ce qui est souvent pratique lorsqu’elle est combinée à "-w" pour ne rapporter que les événements nouveaux. Pour plus de commodité, les options "-wn" ou "-nw" peuvent être utilisées pour activer les deux options simultanément. Par défaut, tous les événements sont délimités par un caractère de saut de ligne ('&#92;n' ou 10 ou 0x0A). Il est possible de modifier cette valeur par le caractère NUL ('&#92;0' ou 0) en passant l’argument "-0". L’option "-s" assainit la sortie afin que les données binaires capturées ou décodées ne modifient pas le rendu du terminal. Les caractères blancs (espace et tabulation) sont remplacés par un espace afin que chaque enregistrement reste sur une seule ligne. Les autres caractères de contrôle (0x00 à 0x1F et 0x7F), ainsi que les caractères non ASCII (0x80 et au-delà), sont remplacés par un « ? ». La longueur de la sortie est conservée. Ainsi, l’affichage d’un anneau ne peut injecter ni séquences d’échappement ANSI, ni codes modifiant le sens d’écriture dans le terminal de l’opérateur. Cela est utile pour une sortie vers un terminal ou vers un programme dont l’entrée ne doit pas être interprétée comme comportant des caractères spéciaux, par exemple des scripts de surveillance dont la sortie est copiée à l’identique dans des rapports.

<a id="entry-9-3-show-fd"></a>

**`show fd [-!plcfbsd]* [[<tgid>]/[<fd>] | <fd>]`**

```haproxy
show fd [-!plcfbsd]* [[<tgid>]/[<fd>] | <fd>]
```

Affiche la liste de tous les descripteurs de fichiers ou uniquement le nombre `<fd>` s'il est spécifié. La forme "`<tgid>`/`<fd>`" est également acceptée, où l'un des côtés peut être vide comme un joker ("/`<fd>`" pour le descripteur `<fd>` à travers les groupes de threads, "`<tgid>`/" pour tous les descripteurs de `<tgid>`). Le `<tgid>` est actuellement analysé mais ignoré, en attente d'une future prise en charge des tables de descripteurs par groupe de threads. Un ensemble d'indicateurs peut éventuellement être passé pour limiter le dump à certains types de FD ou en exclure d'autres. Lorsqu'on rencontre '-' ou '!', la sélection est inversée pour les caractères suivants dans le même argument. L'inversion est réinitialisée avant chaque mot d'argument délimité par des espaces. Les types de FD sélectionnables incluent 'p' pour les tubes, 'l' pour les écouteurs, 'c' pour les connexions (de tout type), 'f' pour les connexions frontales, 'b' pour les connexions backend (de tout type), 's' pour les connexions aux serveurs, 'd' pour les connexions à l'adresse "dispatch" ou à l'adresse transparente du backend. Avec cela, 'b' est un raccourci pour 'sd' et 'c' pour 'fb' ou 'fsd'. 'c!f' est équivalent à 'b' ("toutes les connexions sauf les connexions frontales" sont bien des connexions backend). Cette fonction est destinée uniquement aux développeurs qui doivent observer des états internes afin de déboguer des problèmes complexes tels qu'une utilisation anormale du CPU. Un descripteur est rapporté par ligne, et pour chacun, son état dans le poller est indiqué avec des lettres majuscules pour les indicateurs activés et minuscules pour les désactivés, en utilisant "P" pour "polled", "R" pour "ready", "A" pour "active", l'état des événements avec "H" pour "hangup", "E" pour "error", "O" pour "output", "P" pour "priority" et "I" pour "input", quelques autres indicateurs comme "N" pour "new" (ajouté récemment dans le cache des descripteurs), "U" pour "updated" (reçu une mise à jour dans le cache des descripteurs), "L" pour "linger_risk", "C" pour "cloned", puis la position de l'entrée mise en cache, le pointeur vers le propriétaire interne, le pointeur vers la fonction de rappel d'E/S et son nom lorsqu'il est connu. Lorsque le propriétaire est une connexion, les indicateurs de connexion et la cible sont rapportés (frontal, proxy ou serveur). Lorsque le propriétaire est un écouteur, l'état de l'écouteur et son frontal sont rapportés. Il n'y a aucun intérêt à utiliser cette commande sans une bonne connaissance des internes. Il convient de noter que le format de sortie peut évoluer au fil du temps, de sorte que cette sortie ne doit pas être analysée par des outils conçus pour être durables. Certains états internes peuvent sembler suspects à la fonction les listant ; dans ce cas, la ligne de sortie sera suffixée par un point d'exclamation ('!'). Cela peut aider à trouver un point de départ lors de la diagnostic d'un incident.

<a id="entry-9-3-show-info"></a>

**`show info [typed|json] [desc] [float]`**

```haproxy
show info [typed|json] [desc] [float]
```

Affiche les informations sur l'état de haproxy dans le processus actuel. Si l'argument facultatif « typed » est fourni, les numéros de champ, les noms et les types sont également émis afin que les outils de surveillance externes puissent facilement récupérer, éventuellement agréger, puis rapporter les informations contenues dans les champs qu'ils ne connaissent pas. Chaque champ est affiché sur une ligne distincte. Si l'argument facultatif « json » est fourni, les informations fournies par la sortie « typed » sont fournies au format JSON sous forme d'une liste d'objets JSON. Par défaut, le format ne contient que deux colonnes séparées par deux points (':'). La colonne de gauche est le nom du champ et la colonne de droite est la valeur. Il est très important de noter que, dans le format de sortie « typed », la sortie pour un objet unique est contiguë, de sorte qu'il n'est pas nécessaire pour le consommateur de stocker l'ensemble des données en même temps. Si l'argument facultatif « float » est fourni, certains champs habituellement émis sous forme d'entiers peuvent être émis sous forme de flottants pour une plus grande précision. Il n'est pas spécifié de manière explicite quels champs sont concernés, car cela pourrait évoluer au fil du temps. L'utilisation de cette option implique que le consommateur est capable de traiter les flottants. Le format de sortie utilisé est sprintf("%f").

Lorsque le format de sortie typé est utilisé, chaque ligne est composée de 4 colonnes séparées par des deux-points (':'). La première colonne est une série de 3 éléments séparés par des points. Le premier élément est la position numérique du champ dans la liste (commençant à zéro). Cette position ne doit pas évoluer au fil du temps, mais des trous sont à prévoir, selon les options de compilation ou si certains champs sont supprimés à l'avenir. Le deuxième élément est le nom du champ tel qu'il apparaît dans la sortie par défaut de « show info ». Le troisième élément est le numéro relatif du processus, commençant à 1.

Le reste de la ligne, à partir du premier deux-points, suit le format de sortie typé décrit dans la section précédente. En résumé, la deuxième colonne (après le premier « : ») indique l'origine, la nature et la portée de la variable. La troisième colonne précise le type du champ, parmi « s32 », « s64 », « u32 », « u64 » ou « str ». La quatrième colonne contient la valeur elle-même, que le consommateur sait interpréter grâce à la colonne 3 et traiter grâce à la colonne 2.

Ainsi, le format global de ligne en mode typé est :

```text
<field_pos>.<field_name>.<process_num>:<tags>:<type>:<value>
```

Lorsque « desc » est ajouté à la commande, un deux-points supplémentaire suivi d'une chaîne entre guillemets est ajouté, avec une description de la métrique. Au moment de la rédaction, cette fonctionnalité n'est prise en charge que pour les formats de sortie « typed » et par défaut.

Exemple :

```shell
> show info
Name: HAProxy
Version: 1.7-dev1-de52ea-146
Release_date: 2016/03/11
Nbproc: 1
Process_num: 1
Pid: 28105
Uptime: 0d 0h00m04s
Uptime_sec: 4
Memmax_MB: 0
PoolAlloc_MB: 0
PoolUsed_MB: 0
PoolFailed: 0
(...)

> show info typed
0.Name.1:POSV:str:HAProxy
1.Version.1:POSV:str:3.1-dev0-7c653d-2466
2.Release_date.1:POSV:str:2025/07/01
3.Nbthread.1:CGSV:u32:1
4.Nbproc.1:CGSV:u32:1
5.Process_num.1:KGPV:u32:1
6.Pid.1:SGPV:u32:638069
7.Uptime.1:MDPV:str:0d 0h00m07s
8.Uptime_sec.1:MDPV:u32:7
9.Memmax_MB.1:CLPV:u32:0
10.PoolAlloc_MB.1:MGPV:u32:0
11.PoolUsed_MB.1:MGPV:u32:0
12.PoolFailed.1:MCPV:u32:0
(...)
```

Dans le format typé, la présence de l'identifiant de processus à la fin de la première colonne permet de regrouper visuellement les sorties de plusieurs processus de manière très simple. Exemple :

```shell
$ ( echo show info typed | socat /var/run/haproxy.sock1;    \
    echo show info typed | socat /var/run/haproxy.sock2 ) |  \
  sort -t . -k 1,1n -k 2,2 -k 3,3n
0.Name.1:POS:str:HAProxy
0.Name.2:POS:str:HAProxy
1.Version.1:POS:str:1.7-dev1-868ab3-148
1.Version.2:POS:str:1.7-dev1-868ab3-148
2.Release_date.1:POS:str:2016/03/11
2.Release_date.2:POS:str:2016/03/11
3.Nbproc.1:CGS:u32:2
3.Nbproc.2:CGS:u32:2
4.Process_num.1:KGP:u32:1
4.Process_num.2:KGP:u32:2
5.Pid.1:SGP:u32:30120
5.Pid.2:SGP:u32:30121
6.Uptime.1:MDP:str:0d 0h01m28s
6.Uptime.2:MDP:str:0d 0h01m28s
(...)
```

Le format de la sortie JSON est décrit dans un schéma qui peut être affiché à l’aide de la commande « show schema json ».

La sortie JSON ne contient aucun espace blanc supplémentaire afin de réduire le volume de sortie. Pour une lecture humaine, il peut être utile de passer la sortie dans un formateur. Exemple :

\$ echo "show info json" \| socat /var/run/haproxy.sock stdio \| &#92; python
-m json.tool

La sortie JSON ne contient aucun espace blanc supplémentaire afin de réduire le volume de sortie. Pour une lecture humaine, il peut être utile de passer la sortie dans un formateur. Exemple :

\$ echo "show info json" \| socat /var/run/haproxy.sock stdio \| &#92; python
-m json.tool

<a id="entry-9-3-show-libs"></a>

**`show libs`**

```haproxy
show libs
```

Affiche la liste des bibliothèques dynamiques partagées et des fichiers objets chargés, sur les systèmes qui le supportent. Lorsqu'elles sont disponibles, pour chaque objet partagé, la plage d'adresses virtuelles, la taille et le chemin d'accès à l'objet seront indiqués. Cette commande peut par exemple servir à estimer quelle bibliothèque fournit une fonction apparaissant dans un dump. Notez que sur de nombreux systèmes, les adresses changent à chaque redémarrage (randomisation de l'espace d'adressage), de sorte que cette liste doit être récupérée au démarrage si elle est destinée à être utilisée pour analyser un fichier core. Cette commande ne peut être exécutée que sur les sockets configurés pour les niveaux « operator » ou « admin ». Notez que le format de sortie peut varier selon les systèmes d'exploitation, les architectures et même les versions de HAProxy, et ne doit pas être utilisé dans les scripts.

<a id="entry-9-3-show-map"></a>

**`show map [[@<ver>] <map>]`**

```haproxy
show map [[@<ver>] <map>]
```

Informations sur les convertisseurs de cartes. Sans argument, la liste de toutes les cartes disponibles est retournée. Si un `<map>` est spécifié, son contenu est affiché. `<map>` est le numéro de `<id>` ou `<name>`. Par défaut, la version actuelle de la carte est affichée (la version actuellement utilisée pour les correspondances et signalée comme 'curr_ver' dans la liste des cartes). Il est possible de plutôt afficher d'autres versions en préfixant '@`<ver>`' à l'identifiant de la carte. La version agit comme un filtre et les versions inexistantes ne renvoient simplement aucun résultat. La valeur 'entry_cnt' représente le nombre total d'entrées de la carte, y compris celles qui ne sont pas actives, ce qui signifie qu'elle inclut également les entrées actuellement en cours d'ajout.

Dans la sortie, la première colonne est un identifiant unique d'entrée, utilisable comme référence pour les opérations « del map » et « set map ». La deuxième colonne est le motif et la troisième colonne est l'exemple, le cas échéant. Les données renvoyées ne constituent pas directement une liste des cartes disponibles, mais la liste de tous les motifs composant une carte. De nombreux de ces motifs peuvent être partagés avec les ACL.

<a id="entry-9-3-show-peers"></a>

**`show peers [dict|-] [<peers section>]`**

```haproxy
show peers [dict|-] [<peers section>]
```

Informations sur les pairs configurés dans les sections « peers ». Sans argument, la liste des pairs appartenant à toutes les sections « peers » est affichée. Si `<peers section>` est spécifié, seules les informations relatives aux pairs appartenant à cette section « peers » sont affichées. Lorsque « dict » est précisé avant le nom de la section « peers », les caches entiers des dictionnaires Tx/Rx sont également affichés (très volumineux). L'utilisation de « - » peut être nécessaire pour afficher une section « peers » nommée « dict ».

Voici deux exemples de sorties où les pairs hostA, hostB et hostC appartiennent à la section « sharedlb ». Seulement hostA et hostB sont connectés. Seulement hostA a envoyé des données à hostB.

\$ echo "show peers" \| socat - /tmp/hostA 0x55deb0224320: [15/Apr/2019:11:28:01] id=sharedlb
state=0 flags=0x3 &#92; resync_timeout=`<PAST>` task_calls=45122
0x55deb022b540: id=hostC(remote) addr=127.0.0.12:10002 status=CONN &#92;
reconnect=4s confirm=0 flags=0x0 0x55deb022a440: id=hostA(local) addr=127.0.0.10:10000 status=NONE
&#92; reconnect=`<NEVER>` confirm=0 flags=0x0 0x55deb0227d70: id=hostB(remote)
addr=127.0.0.11:10001 status=ESTA reconnect=2s confirm=0 flags=0x20000200 appctx:0x55deb028fba0
st0=7 st1=0 task_calls=14456 &#92; state=EST xprt=RAW src=127.0.0.1:37257
addr=127.0.0.10:10000 remote_table:0x55deb0224a10 id=stkt local_id=1 remote_id=1
last_local_table:0x55deb0224a10 id=stkt local_id=1 remote_id=1 shared tables:

```text
0x55deb0224a10 local_id=1 remote_id=1 flags=0x0 remote_data=0x65
  last_acked=0 last_pushed=3 last_get=0 teaching_origin=0 update=3
  table:0x55deb022d6a0 id=stkt update=3 localupdate=3 \
    commitupdate=3 syncing=0
```

\$ echo "show peers" \| socat - /tmp/hostB 0x55871b5ab320: [15/Apr/2019:11:28:03] id=sharedlb
state=0 flags=0x3 &#92; resync_timeout=`<PAST>` task_calls=3 0x55871b5b2540:
id=hostC(remote) addr=127.0.0.12:10002 status=CONN &#92; reconnect=3s
confirm=0 flags=0x0 0x55871b5b1440: id=hostB(local) addr=127.0.0.11:10001 status=NONE
&#92; reconnect=`<NEVER>` confirm=0 flags=0x0 0x55871b5aed70: id=hostA(remote)
addr=127.0.0.10:10000 status=ESTA &#92; reconnect=2s confirm=0
flags=0x20000200 appctx:0x7fa46800ee00 st0=7 st1=0 task_calls=62356 &#92;
state=EST remote_table:0x55871b5ab960 id=stkt local_id=1 remote_id=1 last_local_table:0x55871b5ab960
id=stkt local_id=1 remote_id=1 shared tables:

```text
0x55871b5ab960 local_id=1 remote_id=1 flags=0x0 remote_data=0x65
  last_acked=3 last_pushed=0 last_get=3 teaching_origin=0 update=0
  table:0x55871b5b46a0 id=stkt update=1 localupdate=0 \
    commitupdate=0 syncing=0
```

<a id="entry-9-3-show-pools"></a>

**`show pools [byname|bysize|byusage] [detailed] [match <pfx>] [<nb>]`**

```haproxy
show pools [byname|bysize|byusage] [detailed] [match <pfx>] [<nb>]
```

Effectue un dump de l'état des pools mémoire internes. Cela est utile pour suivre l'utilisation mémoire lorsqu'une fuite de mémoire est suspectée, par exemple. Il effectue exactement la même opération que SIGQUIT exécuté au premier plan, sauf qu'il ne vide pas les pools. La sortie n'est pas triée par défaut. Si « byname » est spécifié, elle est triée par nom de pool ; si « bysize » est spécifié, elle est triée par taille d'élément dans l'ordre inverse ; si « byusage » est spécifié, elle est triée par utilisation totale dans l'ordre inverse, et seuls les éléments utilisés sont affichés. Il est également possible de limiter la sortie aux `<nb>` premiers éléments (par exemple, lors du tri par utilisation). Il est possible d'afficher également des détails internes supplémentaires, y compris la liste de tous les pools fusionnés, en spécifiant « detailed ». Enfin, si « match » est suivi d'un préfixe, seuls les pools dont le nom commence par ce préfixe seront affichés. Le total rapporté concerne uniquement les pools correspondant aux critères de filtrage. Exemple :

```shell
$ socat - /tmp/haproxy.sock <<< "show pools match quic byusage"
Dumping pools usage. Use SIGQUIT to flush them.
  - Pool quic_conn_r (65560 bytes): 1337 allocated (87653720 bytes), ...
  - Pool quic_crypto (1048 bytes): 6685 allocated (7005880 bytes), ...
  - Pool quic_conn (4056 bytes): 1337 allocated (5422872 bytes), ...
  - Pool quic_rxbuf (262168 bytes): 8 allocated (2097344 bytes), ...
  - Pool quic_conne (184 bytes): 9359 allocated (1722056 bytes), ...
  - Pool quic_frame (184 bytes): 7938 allocated (1460592 bytes), ...
  - Pool quic_tx_pac (152 bytes): 6454 allocated (981008 bytes), ...
  - Pool quic_tls_ke (56 bytes): 12033 allocated (673848 bytes), ...
  - Pool quic_rx_pac (408 bytes): 1596 allocated (651168 bytes), ...
  - Pool quic_tls_se (88 bytes): 6685 allocated (588280 bytes), ...
  - Pool quic_cstrea (88 bytes): 4011 allocated (352968 bytes), ...
  - Pool quic_tls_iv (24 bytes): 12033 allocated (288792 bytes), ...
  - Pool quic_dgram (344 bytes): 732 allocated (251808 bytes), ...
  - Pool quic_arng (56 bytes): 4011 allocated (224616 bytes), ...
  - Pool quic_conn_c (152 bytes): 1337 allocated (203224 bytes), ...
Total: 15 pools, 109578176 bytes allocated, 109578176 used ...
```

<a id="entry-9-3-show-profiling"></a>

**`show profiling [{all | status | tasks | memory}] [byaddr|bytime|byctx|aggr|<max_lines>]*`**

```haproxy
show profiling [{all | status | tasks | memory}] [byaddr|bytime|byctx|aggr|<max_lines>]*
```

Affiche les paramètres de profilage actuels, un par ligne, ainsi que la commande nécessaire pour les modifier.
Lorsque le profilage des tâches est activé, certaines statistiques par fonction collectées par le planificateur seront également émises, accompagnées d’un résumé indiquant le nombre d’appels, le temps CPU total/moyen et la latence totale/moyenne.
Lorsque le profilage mémoire est activé, certaines informations telles que le nombre d’allocations/libérations et leurs tailles seront rapportées. Il est possible de limiter la sortie à l’état de profilage uniquement, aux tâches ou au profilage mémoire en spécifiant les mots-clés correspondants ; par défaut, toutes les informations de profilage sont affichées. Il est également possible de limiter le nombre de lignes de sortie de chaque catégorie en spécifiant une limite numérique. Il est possible de demander que la sortie soit triée par adresse, par temps d’exécution total ou par contexte d’appel au lieu de l’utilisation, par exemple pour faciliter les comparaisons entre appels successifs ou vérifier ce qui doit être optimisé, et pour agréger l’activité des tâches par fonction appelée au lieu de voir les détails. Veuillez noter que le profilage est essentiellement destiné aux développeurs, car il fournit des indices sur l’endroit où les cycles CPU ou la mémoire sont gaspillés dans le code. Il n’y a rien d’utilisable à surveiller là-dedans.

<a id="entry-9-3-show-resolvers"></a>

**`show resolvers [<resolvers section id>]`**

```haproxy
show resolvers [<resolvers section id>]
```

Affiche les statistiques pour la section de résolveurs indiquée, ou pour toutes les sections de résolveurs si aucune section n'est fournie.

Pour chaque serveur de noms, les compteurs suivants sont rapportés :

```text
sent: nombre de requêtes DNS envoyées à ce serveur
valid: nombre de réponses DNS valides reçues de ce serveur
update: nombre de réponses DNS utilisées pour mettre à jour l'IP du serveur
cname: nombre de réponses CNAME
cname_error: erreurs CNAME rencontrées avec ce serveur
any_err: nombre de réponses vides (ex. serveur ne prenant pas en charge ANY)
nx: réponses de domaine inexistant reçues de ce serveur
timeout: nombre de fois où ce serveur n'a pas répondu à temps
refused: nombre de requêtes refusées par ce serveur
other: toutes les autres erreurs DNS
invalid: réponse DNS invalide du point de vue du protocole
too_big: réponse trop volumineuse
outdated: réponses arrivées trop tard (après un autre serveur de noms)
```

<a id="entry-9-3-show-quic"></a>

**`show quic [<format>] [<filter>]`**

```haproxy
show quic [<format>] [<filter>]
```

Affiche les informations sur toutes les connexions frontend QUIC actives. Cette commande est restreinte et ne peut être exécutée que sur les sockets configurés avec les niveaux « operator » ou « admin ».

Un argument facultatif peut être spécifié pour contrôler le niveau de détail. Sa valeur peut être interprétée de différentes manières. La première possibilité consiste à utiliser des valeurs prédéfinies : « oneline » pour le format par défaut, « stream » pour lister tous les flux actifs, ou « full » pour afficher toutes les informations. En alternative, une liste de champs séparés par des virgules peut être spécifiée afin de restreindre la sortie. Les valeurs actuellement prises en charge sont « tp », « sock », « pktns », « cc » et « mux ». Enfin, la valeur « help » dans le format affiche à la place un message d’aide plus détaillé.

L'argument final sert à restreindre ou étendre la liste des connexions. Par défaut, seules les connexions frontend actives sont affichées. Utilisez l'argument supplémentaire « clo » pour afficher les connexions frontend en cours de fermeture, « be » pour les connexions backend ou « all » pour toutes les catégories. Il est également possible de restreindre à une seule connexion en spécifiant son adresse hexadécimale.

<a id="entry-9-3-show-servers-conn"></a>

**`show servers conn [<backend>]`**

```haproxy
show servers conn [<backend>]
```

Affiche l'état des connexions actives et inactives des serveurs appartenant au backend spécifié (ou de tous les backends si aucun n'est précisé). Un nom ou un identifiant de backend peut être utilisé.

La sortie se compose d'une ligne d'en-tête affichant les titres des champs, suivie d'une ligne par serveur, contenant pour chaque serveur le nom et l'ID du backend, le nom et l'ID du serveur, l'adresse, le port et une série de valeurs. Le nombre de champs varie selon le nombre de threads. Le format exact de la sortie peut légèrement varier d'une version à l'autre et selon le nombre de threads. Il est nécessaire de prêter attention à la ligne d'en-tête pour aligner correctement les colonnes lors de l'extraction des valeurs, ainsi qu'au nombre de threads, car les dernières colonnes sont par thread :

```text
bkname/svname         Nom du backend '/' nom du serveur
bkid/svid             ID du backend '/' ID du serveur
addr                  Adresse IP du serveur
port                  Port du serveur (ou zéro s'il n'y en a pas)
-                     Champ inutilisé servant de séparateur visuel
purge_delay           Intervalle entre purges de connexions, en millisecondes
served                Nombre de connexions actuellement utilisées
used_cur              Nombre de connexions actuellement utilisées,
                      hors connexions rattachées à une session
used_max              Valeur maximale de used_cur depuis le démarrage du processus
need_est              Estimation glissante du total de connexions nécessaires
idle_sess             Nombre de connexions inactives marquées privées
unsafe_nb             Nombre de connexions inactives considérées "unsafe"
safe_nb               Nombre de connexions inactives considérées "safe"
idle_lim              Nombre maximal configuré de connexions inactives
idle_cur              Total des connexions actuellement inactives par thread
idle_per_thr[NB]      Connexions inactives par thread pour chacun des NB threads
```

HAProxy tue une partie de `<idle_cur>` toutes les `<purge_delay>` lorsque la somme de `<idle_cur>` + `<used_cur>` dépasse l'estimation `<need_est>`. Cette estimation varie en fonction de l'activité des connexions.

Étant donné la nature threadée des connexions inactives, il est important de comprendre que certaines valeurs peuvent évoluer après lecture, et qu’aucune cohérence au sein d’une ligne n’est garantie. Cette sortie est principalement destinée au débogage et ne doit pas être surveillée ni visualisée de manière régulière.

<a id="entry-9-3-show-servers-state"></a>

**`show servers state [<backend>]`**

```haproxy
show servers state [<backend>]
```

Affiche l'état des serveurs présents dans la configuration en cours d'exécution. Un nom ou un identifiant de backend peut être fourni pour limiter la sortie à ce backend uniquement.

Le dump a le format suivant :

- première ligne contient la version du format (1 dans cette spécification) ;
- deuxième ligne contient les en-têtes de colonne, précédés d'un dièse ('#') ;
- troisième ligne et les lignes suivantes contiennent les données ;
- chaque ligne commençant par un dièse ('#') est considérée comme un commentaire.

Étant donné que plusieurs versions de la sortie peuvent coexister, voici la liste des champs et leur ordre par version de format de fichier :

```text
1:
  be_id:                       Identifiant unique du backend.
  be_name:                     Libellé du backend.
  srv_id:                      Identifiant unique du serveur (dans le backend).
  srv_name:                    Libellé du serveur.
  srv_addr:                    Adresse IP du serveur.
  srv_op_state:                État opérationnel du serveur (UP/DOWN/...).
                                 0 = SRV_ST_STOPPED
                                   Le serveur est indisponible.
                                 1 = SRV_ST_STARTING
                                   Le serveur démarre progressivement
                                   (disponible mais limité).
                                 2 = SRV_ST_RUNNING
                                   Le serveur est entièrement disponible.
                                 3 = SRV_ST_STOPPING
                                   Le serveur est disponible mais en arrêt
                                   progressif (ex. 404).
  srv_admin_state:             État administratif du serveur (MAINT/DRAIN/...).
                               Cet état est un masque de valeurs :
                                 0x01 = SRV_ADMF_FMAINT
                                   Le serveur a été explicitement forcé
                                   en maintenance.
                                 0x02 = SRV_ADMF_IMAINT
                                   Le serveur a hérité l'état de maintenance
                                   d'un serveur suivi.
                                 0x04 = SRV_ADMF_CMAINT
                                   Le serveur est en maintenance en raison
                                   de la configuration.
                                 0x08 = SRV_ADMF_FDRAIN
                                   Le serveur a été explicitement forcé
                                   en état de drainage.
                                 0x10 = SRV_ADMF_IDRAIN
                                   Le serveur a hérité l'état de drainage
                                   d'un serveur suivi.
                                 0x20 = SRV_ADMF_RMAINT
                                   Le serveur est en maintenance en raison
                                   d'un échec de résolution d'adresse IP.
                                 0x40 = SRV_ADMF_HMAINT
                                   Le FQDN du serveur a été défini via le
                                   socket de statistiques.

  srv_uweight:                 Poids du serveur visible par l'utilisateur.
  srv_iweight:                 Poids initial du serveur.
  srv_time_since_last_change:  Temps depuis la dernière modification opérationnelle.
  srv_check_status:            État du dernier contrôle d'état.
  srv_check_result:            Résultat du dernier contrôle (FAILED/PASSED/...).
                                 0 = CHK_RES_UNKNOWN
                                   Valeur initiale par défaut.
                                 1 = CHK_RES_NEUTRAL
                                   Contrôle valide sans information d'état.
                                 2 = CHK_RES_FAILED
                                   Le contrôle a échoué.
                                 3 = CHK_RES_PASSED
                                   Le contrôle a réussi et le serveur est
                                   de nouveau entièrement disponible.
                                 4 = CHK_RES_CONDPASS
                                   Le contrôle indique que le serveur ne
                                   souhaite pas de nouvelles sessions.
  srv_check_health:            Compteur actuel rise / fall des contrôles.
  srv_check_state:             État du contrôle (ENABLED/PAUSED/...).
                               Cet état est un masque de valeurs :
                                 0x01 = CHK_ST_INPROGRESS
                                   Un contrôle est actuellement en cours.
                                 0x02 = CHK_ST_CONFIGURED
                                   Le contrôle est configuré et peut
                                   être activé.
                                 0x04 = CHK_ST_ENABLED
                                   Le contrôle est actuellement activé
                                   administrativement.
                                 0x08 = CHK_ST_PAUSED
                                   Contrôles suspendus pour maintenance
                                   (contrôles d'état uniquement).
  srv_agent_state:             État du contrôle d'agent (ENABLED/PAUSED/...).
                               Utilise le même masque de valeurs que
                               "srv_check_state", avec cette valeur supplémentaire :
                                 0x10 = CHK_ST_AGENT
                                   Contrôle d'agent (sinon, il s'agit d'un
                                   contrôle d'état).
  bk_f_forced_id:              Indicateur précisant si l'ID du backend est
                               imposé par la configuration.
  srv_f_forced_id:             Indicateur précisant si l'ID du serveur est
                               imposé par la configuration.
  srv_fqdn:                    FQDN du serveur.
  srv_port:                    Port du serveur.
  srvrecord:                   Enregistrement DNS SRV associé à ce SRV.
  srv_use_ssl:                 Utilisation de ssl pour les connexions serveur.
  srv_check_port:              Port du contrôle d'état du serveur.
  srv_check_addr:              Adresse du contrôle d'état du serveur.
  srv_agent_addr:              Adresse du contrôle d'agent du serveur.
  srv_agent_port:              Port du contrôle d'agent du serveur.
```

<a id="entry-9-3-show-sess"></a>

**`show sess [<options>*]`**

```haproxy
show sess [<options>*]
```

Affiche tous les flux actifs connus (anciennement appelés « sessions »). Évitez d'exécuter cette commande sur des connexions lentes, car cela peut générer une sortie très volumineuse. Cette commande est restreinte et ne peut être exécutée que sur les sockets configurés pour les niveaux « operator » ou « admin ». Notez que, sur des machines aux connexions rapidement recyclées, il se peut que la sortie affiche moins d’entrées que le nombre réellement existant, car seuls les flux existants au moment de l’entrée de la commande sont répertoriés ; ceux qui se ferment entre-temps ne seront pas inclus. Pour les options prises en charge, voir ci-dessous.

<a id="entry-9-3-show-sess-2"></a>

**`show sess [<id> | all | help] [<options>*]`**

```haproxy
show sess [<id> | all | help] [<options>*]
```

Affichez beaucoup d'informations internes sur les flux correspondants. La commande connaît deux formats de sortie : un format court, qui est le format par défaut lorsqu'aucun identifiant de flux spécifique n'est demandé, et un format étendu lors de la liste de flux désignés. Le format court, utilisé par défaut avec « show sess », n'affiche qu'un flux par ligne, avec quelques informations, et l'identifiant du flux au début de la ligne en format hexadécimal (il correspond à l'adresse mémoire du flux).

Dans sa forme étendue, utilisée par « show sess `<id>` » ou « show sess all », les flux sont affichés avec une quantité importante de détails de débogage sur plusieurs lignes (environ 20 par flux), tout en commençant toujours par leur identifiant. Le délimiteur entre les flux est l’identifiant situé au début de la ligne ; les lignes supplémentaires appartenant au même flux commencent par un ou plusieurs espaces (le flux est affiché avec un retrait). L’affichage de nombreux flux peut générer une sortie très volumineuse, prendre beaucoup de temps et être très coûteux en ressources CPU, il est donc toujours préférable de n’afficher que le minimum nécessaire. Ces informations sont inutiles pour la majorité des utilisateurs, mais peuvent être utilisées par les développeurs HAProxy pour diagnostiquer un bug complexe. Le format exact de la sortie n’est pas documenté intentionnellement afin qu’il puisse évoluer librement selon les besoins, y compris dans les branches stables. Cette sortie est destinée à être interprétée en consultant la fonction strm_dump_to_buffer() dans src/stream.c afin de comprendre la signification exacte de certains champs.

L'argument « help » affichera l'utilisation détaillée de la commande au lieu de déverser les flux.

Il est possible de définir certaines options afin de personnaliser l'affichage ou d'appliquer des filtres. Voici les options prises en charge :   - backend `<b>` : n'afficher que les flux attachés à ce backend   - frontend `<f>` : n'afficher que les flux attachés à ce frontal   - older `<age>` : n'afficher que les flux plus anciens que `<age>` secondes   - server `<b/s>` : n'afficher que les flux attachés à ce couple backend+serveur   - show-uri : afficher l'URI de la transaction, telle qu'elle a été capturée lors de l'analyse de la requête. Il n'est affiché que s'il a été capturé.   - susp : n'afficher que les flux considérés comme suspects par les développeurs, selon des critères qui peuvent évoluer dans le temps ou varier selon les versions.

<a id="entry-9-3-show-stat"></a>

**`show stat [domain <resolvers|proxy>] [{<iid>|<proxy>} <type> <sid>] \`**

```haproxy
show stat [domain <resolvers|proxy>] [{<iid>|<proxy>} <type> <sid>] \
          [typed|json] [desc] [up|no-maint]
```

Dump des statistiques. Le domaine est utilisé pour sélectionner les statistiques à afficher ; les résolveurs et les proxies sont actuellement disponibles. Par défaut, le format CSV est utilisé ; vous pouvez activer le format d'affichage étendu typé décrit dans la section précédente en passant « typed » après les autres arguments ; ou au format JSON en passant « json » après les autres arguments. En passant `<id>`, `<type>` et `<sid>`, il est possible de n'afficher que des éléments sélectionnés : - `<iid>` est un identifiant de proxy, -1 pour tout afficher. En alternative, un nom de proxy `<proxy>` peut être spécifié. Dans ce cas, l'identifiant de ce proxy sera utilisé comme sélecteur d'identifiant. - `<type>` sélectionne le type d'objets pouvant être dumpés : 1 pour les frontaux, 2 pour les backends, 4 pour les serveurs, -1 pour tout. Ces valeurs peuvent être combinées par opération OU, par exemple :

```text
1 + 2     = 3   -> frontend + backend.
1 + 2 + 4 = 7   -> frontend + backend + server.
```

    - `<sid>` est un identifiant de serveur, -1 pour exporter l'intégralité du proxy sélectionné.

Exemple :

```shell
    $ echo "show info;show stat" | socat stdio unix-connect:/tmp/sock1
>>> Name: HAProxy
    Version: 1.4-dev2-49
    Release_date: 2009/09/23
    Nbproc: 1
    Process_num: 1
    (...)

    # pxname,svname,qcur,qmax,scur,smax,slim,stot,bin,bout,dreq,  (...)
    stats,FRONTEND,,,0,0,1000,0,0,0,0,0,0,,,,,OPEN,,,,,,,,,1,1,0, (...)
    stats,BACKEND,0,0,0,0,1000,0,0,0,0,0,,0,0,0,0,UP,0,0,0,,0,250,(...)
    (...)
    www1,BACKEND,0,0,0,0,1000,0,0,0,0,0,,0,0,0,0,UP,1,1,0,,0,250, (...)

    $
```

Dans cet exemple, deux commandes ont été émises simultanément. Cela permet de déterminer facilement quel processus les statistiques concernent en mode multi-processus. Cette information n'est pas nécessaire dans le format de sortie typée, car le numéro de processus est indiqué sur chaque ligne. Notez la ligne vide suivant la sortie d'information, qui marque la fin du premier bloc. Une ligne vide similaire apparaît à la fin du second bloc (stats), afin que l'utilisateur sache que la sortie n'a pas été tronquée.

Lorsque « typed » est spécifié, le format de sortie est plus adapté aux outils de surveillance, car il fournit des positions numériques et indique le type de chaque champ de sortie. Chaque valeur apparaît sur une ligne distincte, accompagnée du numéro de processus, du numéro d'élément, de sa nature, de son origine et de son champ d'application. Ce même format est également disponible via les statistiques HTTP en ajoutant « ;typed » à l'URI. Il est très important de noter que, dans le format de sortie typé, les données d'un objet unique sont contiguës, de sorte qu'il n'est pas nécessaire pour le consommateur de stocker l'ensemble des données en même temps.

Le modificateur « up » entraîne l'affichage uniquement des serveurs signalés comme étant actifs ou non vérifiés. Les serveurs inactifs, non résolus ou en maintenance ne seront pas affichés. Cela correspond à l'option « ;up » dans les statistiques HTTP. De même, le modificateur « no-maint » agit comme le modificateur HTTP « ;no-maint » et empêche l'affichage des serveurs désactivés. La différence réside dans le fait que les serveurs activés mais inactifs ne seront pas exclus.

Lorsqu'on utilise le format de sortie typé, chaque ligne est composée de 4 colonnes séparées par des deux-points (':'). La première colonne est une série de 5 éléments séparés par des points. Le premier élément est une lettre indiquant le type de l'objet décrit. Actuellement, les types d'objets suivants sont connus : « F » pour un frontal, « B » pour un backend, « L » pour un écouteur, et « S » pour un serveur. Le deuxième élément est un entier positif représentant l'identifiant unique du proxy auquel appartient l'objet. Il correspond à la colonne « iid » de la sortie CSV et correspond à la valeur située devant la directive optionnelle « id » présente dans la section frontal ou backend. Le troisième élément est un entier positif contenant l'identifiant unique de l'objet à l'intérieur du proxy, et correspond à la colonne « sid » de la sortie CSV. La valeur 0 est utilisée lors du dump d'un frontal ou d'un backend. Pour un écouteur ou un serveur, cela correspond à son identifiant respectif à l'intérieur du proxy. Le quatrième élément est la position numérique du champ dans la liste (comptée à partir de zéro). Cette position ne doit pas évoluer au fil du temps, mais des trous sont à prévoir, selon les options de compilation ou si certains champs sont supprimés à l'avenir. Le cinquième élément est le nom du champ tel qu'il apparaît dans la sortie CSV. Le sixième élément est un entier positif et correspond au numéro relatif du processus, commençant à 1.

Le reste de la ligne, à partir du premier deux-points, suit le format de sortie typé décrit dans la section précédente. En résumé, la deuxième colonne (après le premier « : ») indique l'origine, la nature, la portée et l'état de persistance de la variable. La troisième colonne indique le type de champ, parmi « s32 », « s64 », « u32 », « u64 », « flt » et « str ». La quatrième colonne contient la valeur elle-même, que le consommateur sait interpréter grâce à la colonne 3 et traiter grâce à la colonne 2.

Lorsque « desc » est ajouté à la commande, un deux-points supplémentaire suivi d'une chaîne entre guillemets est ajouté, avec une description de la métrique. Au moment de la rédaction, cette fonctionnalité n'est prise en charge que pour le format de sortie « typed ».

Ainsi, le format global de ligne en mode typé est :

```text
<obj>.<px_id>.<id>.<fpos>.<fname>.<process_num>:<tags>:<type>:<value>
```

Voici un exemple de format de sortie typé :

```shell
$ echo "show stat typed" | socat stdio unix-connect:/tmp/sock1
F.2.0.0.pxname.1:KNSV:str:dummy
F.2.0.1.svname.1:KNSV:str:FRONTEND
F.2.0.4.scur.1:MGPV:u32:0
F.2.0.5.smax.1:MMPV:u32:0
F.2.0.6.slim.1:CLPV:u32:524269
F.2.0.7.stot.1:MCPP:u64:0
F.2.0.8.bin.1:MCPP:u64:0
F.2.0.9.bout.1:MCPP:u64:0
F.2.0.10.dreq.1:MCPP:u64:0
F.2.0.11.dresp.1:MCPP:u64:0
F.2.0.12.ereq.1:MCPP:u64:0
F.2.0.17.status.1:SGPV:str:OPEN
F.2.0.26.pid.1:KGPV:u32:1
F.2.0.27.iid.1:KGSV:u32:2
F.2.0.28.sid.1:KGSV:u32:0
F.2.0.32.type.1:CGSV:u32:0
F.2.0.33.rate.1:MRPP:u32:0
F.2.0.34.rate_lim.1:CLPV:u32:0
F.2.0.35.rate_max.1:MMPV:u32:0
F.2.0.46.req_rate.1:MRPP:u32:0
F.2.0.47.req_rate_max.1:MMPV:u32:0
F.2.0.48.req_tot.1:MCPP:u64:0
F.2.0.51.comp_in.1:MCPP:u64:0
F.2.0.52.comp_out.1:MCPP:u64:0
F.2.0.53.comp_byp.1:MCPP:u64:0
F.2.0.54.comp_rsp.1:MCPP:u64:0
(...)
```

Dans le format typé, la présence de l'identifiant de processus à la fin de la première colonne permet de regrouper visuellement les sorties de plusieurs processus, comme illustré dans l'exemple ci-dessous où chaque ligne s'affiche pour chaque processus :

```shell
$ ( echo show stat typed | socat /var/run/haproxy.sock1 -; \
    echo show stat typed | socat /var/run/haproxy.sock2 - ) | \
  sort -t . -k 1,1 -k 2,2n -k 3,3n -k 4,4n -k 5,5 -k 6,6n
B.3.0.0.pxname.1:KNSV:str:private-backend
B.3.0.0.pxname.2:KNSV:str:private-backend
B.3.0.1.svname.1:KNSV:str:BACKEND
B.3.0.1.svname.2:KNSV:str:BACKEND
B.3.0.2.qcur.1:MGPV:u32:0
B.3.0.2.qcur.2:MGPV:u32:0
B.3.0.3.qmax.1:MMPV:u32:0
B.3.0.3.qmax.2:MMPV:u32:0
B.3.0.4.scur.1:MGPV:u32:0
B.3.0.4.scur.2:MGPV:u32:0
B.3.0.5.smax.1:MMPV:u32:0
B.3.0.5.smax.2:MMPV:u32:0
B.3.0.6.slim.1:CLPV:u32:1000
B.3.0.6.slim.2:CLPV:u32:1000
(...)
```

Le format de la sortie JSON est décrit dans un schéma qui peut être affiché à l’aide de la commande « show schema json ».

La sortie JSON ne contient aucun espace blanc supplémentaire afin de réduire le volume de sortie. Pour une lecture humaine, il peut être utile de passer la sortie dans un formateur. Exemple :

\$ echo "show stat json" \| socat /var/run/haproxy.sock stdio \| &#92; python
-m json.tool

La sortie JSON ne contient aucun espace blanc supplémentaire afin de réduire le volume de sortie. Pour une lecture humaine, il peut être utile de passer la sortie dans un formateur. Exemple :

\$ echo "show stat json" \| socat /var/run/haproxy.sock stdio \| &#92; python
-m json.tool

<a id="entry-9-3-show-ssl-ca-file"></a>

**`show ssl ca-file [[*][\]<cafile>[:<index>]]`**

```haproxy
show ssl ca-file [[*][\]<cafile>[:<index>]]
```

Affiche la liste des fichiers de certificats autorités de certification (CA) chargés dans le processus ainsi que le nombre de certificats correspondants. Les certificats ne sont pas utilisés par aucun frontal ou backend tant que leur statut n'est pas « Used ». Une entrée "@system-ca" peut apparaître dans la liste ; elle est chargée par défaut par httpclient et contient la liste des autorités de certification fiables de votre système, renvoyée par OpenSSL. Si un nom de fichier est précédé d'un astérisque, il s'agit d'une transaction non encore validée. Si un `<cafile>` est spécifié sans `<index>`, il affichera l'état du fichier CA ("Used"/"Unused") suivi des détails de tous les certificats contenus dans ce fichier. Les détails affichés pour chaque certificat sont identiques à ceux affichés par la commande "show ssl cert". Si un `<cafile>` est spécifié suivi d'un `<index>`, seuls les détails du certificat ayant l'index spécifié seront affichés. Les index commencent à 1. Si l'index est invalide (par exemple trop élevé), rien ne sera affiché. Cette commande peut être utile pour vérifier qu'un fichier CA a été correctement mis à jour. Vous pouvez également afficher les détails d'une transaction en cours en précédant le nom de fichier par un '*'. Si le premier caractère du nom de fichier est un '*', il peut être échappé avec '&#92;\*'.

Exemple :

```shell
$ echo "show ssl ca-file" | socat /var/run/haproxy.master -
# transaction
*cafile.crt - 2 certificate(s)
# filename
cafile.crt - 1 certificate(s)

$ echo "show ssl ca-file cafile.crt" | socat /var/run/haproxy.master -
Filename: /home/tricot/work/haproxy/reg-tests/ssl/set_cafile_ca2.crt
Status: Used

Certificate #1:
Serial: 11A4D2200DC84376E7D233CAFF39DF44BF8D1211
notBefore: Apr  1 07:40:53 2021 GMT
notAfter: Aug 17 07:40:53 2048 GMT
Subject Alternative Name:
Algorithm: RSA4096
SHA1 FingerPrint: A111EF0FEFCDE11D47FE3F33ADCA8435EBEA4864
Subject: /C=FR/ST=Some-State/O=HAProxy Technologies/CN=HAProxy Technologies CA
Issuer: /C=FR/ST=Some-State/O=HAProxy Technologies/CN=HAProxy Technologies CA

$ echo "show ssl ca-file *cafile.crt:2" | socat /var/run/haproxy.master -
Filename: */home/tricot/work/haproxy/reg-tests/ssl/set_cafile_ca2.crt
Status: Unused

Certificate #2:
Serial: 587A1CE5ED855040A0C82BF255FF300ADB7C8136
[...]
```

<a id="entry-9-3-show-ssl-cert"></a>

**`show ssl cert [[*][\]<filename>]`**

```haproxy
show ssl cert [[*][\]<filename>]
```

Affiche la liste des certificats chargés dans le processus. Ils ne sont pas utilisés par aucun frontal ou backend tant que leur statut n'est pas « Used ». Si un nom de fichier est précédé d'un astérisque, il s'agit d'une transaction non encore validée. Si un nom de fichier est spécifié, les détails concernant le certificat seront affichés. Cette commande peut être utile pour vérifier qu'un certificat a bien été mis à jour. Vous pouvez également afficher les détails d'une transaction en précédant le nom de fichier par un '*'. Si le premier caractère du nom de fichier est un '*', il peut être échappé avec '&#92;\*'. Cette commande peut également être utilisée pour afficher les détails de la réponse OCSP d'un certificat en ajoutant à la fin du nom de fichier une extension ".ocsp". Elle fonctionne aussi bien pour les certificats validés que pour les transactions en cours. Pour un certificat validé, cette commande est équivalente à l'appel de « show ssl ocsp-response » avec l'identifiant correspondant de la réponse OCSP.

Exemple :

```shell
$ echo "@1 show ssl cert" | socat /var/run/haproxy.master -
# transaction
*test.local.pem
# filename
test.local.pem

$ echo "@1 show ssl cert test.local.pem" | socat /var/run/haproxy.master -
Filename: test.local.pem
Status: Used
Serial: 03ECC19BA54B25E85ABA46EE561B9A10D26F
notBefore: Sep 13 21:20:24 2019 GMT
notAfter: Dec 12 21:20:24 2019 GMT
Issuer: /C=US/O=Let's Encrypt/CN=Let's Encrypt Authority X3
Subject: /CN=test.local
Subject Alternative Name: DNS:test.local, DNS:imap.test.local
Algorithm: RSA2048
SHA1 FingerPrint: 417A11CAE25F607B24F638B4A8AEE51D1E211477

$ echo "@1 show ssl cert *test.local.pem" | socat /var/run/haproxy.master -
Filename: *test.local.pem
Status: Unused
[...]

$ echo "@1 show ssl cert \*.local.pem" | socat /var/run/haproxy.master -
Filename: *.local.pem
Status: Used
[...]
```

<a id="entry-9-3-show-ssl-crl-file"></a>

**`show ssl crl-file [[*][\]<crlfile>[:<index>]]`**

```haproxy
show ssl crl-file [[*][\]<crlfile>[:<index>]]
```

Affiche la liste des fichiers CRL chargés dans le processus. Ils ne sont pas utilisés par aucun frontal ou backend tant que leur statut n'est pas « Used ». Si un nom de fichier est précédé d'un astérisque, il s'agit d'une transaction non encore validée. Si un `<crlfile>` est spécifié sans `<index>`, il affiche l'état du fichier CRL ("Used"/"Unused") suivi des détails relatifs à toutes les listes de révocation contenues dans le fichier CRL. Les détails affichés pour chaque liste sont basés sur la sortie de la commande « openssl crl -text -noout -in `<file>` ». Si un `<crlfile>` est spécifié suivi d'un `<index>`, seul le détail de la liste ayant l'index spécifié est affiché. Les index commencent à 1. Si l'index est invalide (par exemple trop élevé), rien n'est affiché. Cette commande peut être utile pour vérifier qu'un fichier CRL a été correctement mis à jour. Vous pouvez également afficher les détails d'une transaction en cours en précédant le nom de fichier d'un '*'. Si le premier caractère du nom de fichier est un '*', il peut être échappé avec '&#92;\*'.

Exemple :

```shell
$ echo "show ssl crl-file" | socat /var/run/haproxy.master -
# transaction
*crlfile.pem
# filename
crlfile.pem

$ echo "show ssl crl-file crlfile.pem" | socat /var/run/haproxy.master -
Filename: /home/tricot/work/haproxy/reg-tests/ssl/crlfile.pem
Status: Used

Certificate Revocation List #1:
Version 1
Signature Algorithm: sha256WithRSAEncryption
Issuer: /C=FR/O=HAProxy Technologies/CN=Intermediate CA2
Last Update: Apr 23 14:45:39 2021 GMT
Next Update: Sep  8 14:45:39 2048 GMT
Revoked Certificates:
    Serial Number: 1008
        Revocation Date: Apr 23 14:45:36 2021 GMT

Certificate Revocation List #2:
Version 1
Signature Algorithm: sha256WithRSAEncryption
Issuer: /C=FR/O=HAProxy Technologies/CN=Root CA
Last Update: Apr 23 14:30:44 2021 GMT
Next Update: Sep  8 14:30:44 2048 GMT
No Revoked Certificates.
```

<a id="entry-9-3-show-ssl-crt-list"></a>

**`show ssl crt-list [-n] [<filename>]`**

```haproxy
show ssl crt-list [-n] [<filename>]
```

Affiche la liste des crt-list et des répertoires utilisés dans la configuration HAProxy. Si un nom de fichier est spécifié, affiche le contenu d’un crt-list ou d’un répertoire. Une fois affiché, la sortie peut être utilisée comme fichier crt-list. L’option '-n' permet d’afficher le numéro de ligne, ce qui est utile lors de l’utilisation combinée avec l’option 'del ssl crt-list' en cas de duplication d’entrée. La sortie avec l’option '-n' n’est pas compatible avec le format crt-list et ne peut pas être chargée par HAProxy.

Exemple :

```shell
echo "show ssl crt-list -n localhost.crt-list" | socat /tmp/sock1 -
# localhost.crt-list
common.pem:1 !not.test1.com *.test1.com !localhost
common.pem:2
ecdsa.pem:3 [verify none allow-0rtt ssl-min-ver TLSv1.0 ssl-max-ver TLSv1.3] localhost !www.test1.com
ecdsa.pem:4 [verify none allow-0rtt ssl-min-ver TLSv1.0 ssl-max-ver TLSv1.3]
```

<a id="entry-9-3-show-ssl-ech"></a>

**`show ssl ech [<name>]`**

```haproxy
show ssl ech [<name>]
```

Affichez la liste des clés ECH chargées dans le processus HAProxy.

Lorsque `<name>` est spécifié, affiche les clés correspondant à une ligne de liaison spécifique. Le format de la ligne de liaison est
`<frontend>`/@`<filename>`:`<linenum>` (par exemple : frontend1/@haproxy.conf:19) ou
`<frontend>`/`<name>` si la ligne de liaison a été nommée à l'aide du mot-clé « name ».

L’entrée « age » représente le temps, en secondes, écoulé depuis que la clé a été chargée dans la ligne bind. Cette valeur est réinitialisée lors du démarrage, du rechargement ou d'un redémarrage de HAProxy.

Exige une version d'OpenSSL qui prend en charge ECH, et HAProxy doit être compilé avec USE_ECH=1.
Cette commande n'est prise en charge que sur une connexion CLI en mode expérimental (voir « experimental-mode on »).

Voir également « ech » dans la [Section 5.1](/fr/haproxy/bind-and-server-options/#section-5-1) du manuel de configuration.

Exemple :

```shell
$ echo "experimental-mode on; show ssl ech" | socat /tmp/haproxy.sock -
 ***
 frontend: frontend1

 bind: frontend1/@haproxy.conf:19

 ECH entry: 0 public_name: example.com age: 557 (has private key)
      [fe0d,94,example.com,[0020,0001,0001],c39285b774bf61c071864181c5292a012b30adaf767e39369a566af05573ef2b,00,00]

 ECH entry: 1 public_name: example.com age: 557 (has private key)
      [fe0d,ee,example.com,[0020,0001,0001],6572191131b5cabba819f8cacf2d2e06fa0b87b30d9b793644daba7b8866d511,00,00]

 bind: frontend1/@haproxy.conf:20

 ECH entry: 0 public_name: example.com age: 557 (has private key)
      [fe0d,94,example.com,[0020,0001,0001],c39285b774bf61c071864181c5292a012b30adaf767e39369a566af05573ef2b,00,00]

 ECH entry: 1 public_name: example.com age: 557 (has private key)
      [fe0d,ee,example.com,[0020,0001,0001],6572191131b5cabba819f8cacf2d2e06fa0b87b30d9b793644daba7b8866d511,00,00]

$ echo "experimental-mode on; show ssl ech frontend1/@haproxy.conf:19" | socat /tmp/haproxy.sock -
***
ECH for frontend1/@haproxy.conf:19
ECH entry: 0 public_name: example.com age: 786 (has private key)
      [fe0d,94,example.com,[0020,0001,0001],c39285b774bf61c071864181c5292a012b30adaf767e39369a566af05573ef2b,00,00]

ECH entry: 1 public_name: example.com age: 786 (has private key)
      [fe0d,ee,example.com,[0020,0001,0001],6572191131b5cabba819f8cacf2d2e06fa0b87b30d9b793644daba7b8866d511,00,00]
```

<a id="entry-9-3-show-ssl-jwt"></a>

**`show ssl jwt`**

```haproxy
show ssl jwt
```

Affiche la liste des certificats pouvant être utilisés pour la validation JWT. Voir également les commandes « add ssl jwt » et « del ssl jwt ». Voir l'option de certificat « jwt » pour plus d'informations.

Exemple :

```shell
echo "show ssl jwt"  | socat /tmp/sock1 -
#filename
jwt.pem
```

<a id="entry-9-3-show-ssl-ocsp-response"></a>

**`show ssl ocsp-response [[text|base64] <id|path>]`**

```haproxy
show ssl ocsp-response [[text|base64] <id|path>]
```

Affichez les identifiants des entrées de l’arbre OCSP correspondant à toutes les réponses OCSP utilisées par HAProxy, ainsi que le chemin du certificat frontal correspondant, le nom de l’autorité émettrice et son hachage de clé, et le numéro de série du certificat pour lequel la réponse OCSP a été générée. Si un `<id>` valide ou le `<path>` d’un certificat frontal valide est fourni, affichez le contenu de la réponse OCSP correspondante. Lorsqu’un `<id>` est fourni, il est possible de définir le format dans lequel les données sont exportées. L’option « text » est la valeur par défaut et permet d’afficher des informations détaillées sur la réponse OCSP de la même manière qu’avec une commande « openssl ocsp -respin `<ocsp-response>` -text ». Le format « base64 » permet d’exporter le contenu d’une réponse OCSP au format base64.

Exemple :

```shell
$ echo "show ssl ocsp-response" | socat /var/run/haproxy.master -
# Certificate IDs
  Certificate ID key: 303b300906052b0e03021a050004148a83e0060faff709ca7e9b95522a2e81635fda0a0414f652b0e435d5ea923851508f0adbe92d85de007a0202100a
  Certificate path: /path_to_cert/foo.pem
    Certificate ID:
      Issuer Name Hash: 8A83E0060FAFF709CA7E9B95522A2E81635FDA0A
      Issuer Key Hash: F652B0E435D5EA923851508F0ADBE92D85DE007A
      Serial Number: 100A

$ echo "show ssl ocsp-response 303b300906052b0e03021a050004148a83e0060faff709ca7e9b95522a2e81635fda0a0414f652b0e435d5ea923851508f0adbe92d85de007a0202100a" | socat /var/run/haproxy.master -
OCSP Response Data:
  OCSP Response Status: successful (0x0)
  Response Type: Basic OCSP Response
  Version: 1 (0x0)
  Responder Id: C = FR, O = HAProxy Technologies, CN = ocsp.haproxy.com
  Produced At: May 27 15:43:38 2021 GMT
  Responses:
  Certificate ID:
    Hash Algorithm: sha1
    Issuer Name Hash: 8A83E0060FAFF709CA7E9B95522A2E81635FDA0A
    Issuer Key Hash: F652B0E435D5EA923851508F0ADBE92D85DE007A
    Serial Number: 100A
  Cert Status: good
  This Update: May 27 15:43:38 2021 GMT
  Next Update: Oct 12 15:43:38 2048 GMT
  [...]

$ echo "show ssl ocsp-response base64 /path_to_cert/foo.pem" | socat /var/run/haproxy.sock -
  MIIB8woBAKCCAewwggHoBgkrBgEFBQcwAQEEggHZMIIB1TCBvqE[...]
```

<a id="entry-9-3-show-ssl-ocsp-updates"></a>

**`show ssl ocsp-updates`**

```haproxy
show ssl ocsp-updates
```

Affiche des informations sur les entrées concernées par le mécanisme de mise à jour OCSP. La commande affiche une ligne par réponse OCSP et inclut l'heure prévue de mise à jour de la réponse, ainsi que l'heure de la dernière mise à jour réussie et les compteurs de mises à jour réussies et échouées. Elle indique également le statut de la dernière mise à jour (réussie ou non) sous forme numérique et textuelle. Consultez la liste complète des erreurs possibles ci-dessous. Les lignes sont triées par heure croissante de « Next Update ». Chaque ligne contient également le chemin vers le premier certificat frontal utilisant la réponse OCSP. Pour plus d'informations sur la mise à jour automatique OCSP, reportez-vous à la commande « show ssl ocsp-response » et à l'option « ocsp-update ».

Les codes d'erreur et les chaînes d'erreur de mise à jour peuvent être les suivants :

```text
  +----+-------------------------------------+
  | ID | message                             |
  +----+-------------------------------------+
  |  0 | "Unknown"                           |
  |  1 | "Update successful"                 |
  |  2 | "HTTP error"                        |
  |  3 | "Missing \"ocsp-response\" header"  |
  |  4 | "OCSP response check failure"       |
  |  5 | "Error during insertion"            |
  +----+-------------------------------------+
```

Exemple :

```shell
$ echo "show ssl ocsp-updates" | socat /tmp/haproxy.sock -
  OCSP Certid | Path | Next Update | Last Update | Successes | Failures | Last Update Status | Last Update Status (str)
      303b300906052b0e03021a050004148a83e0060faff709ca7e9b95522a2e81635fda0a0414f652b0e435d5ea923851508f0adbe92d85de007a02021015 | /path_to_cert/cert.pem | 30/Jan/2023:00:08:09 +0000 | - | 0 | 1 | 2 | HTTP error
      304b300906052b0e03021a0500041448dac9a0fb2bd32d4ff0de68d2f567b735f9b3c40414142eb317b75856cbae500940e61faf9d8b14c2c6021203e16a7aa01542f291237b454a627fdea9c1 | /path_to_cert/other_cert.pem | 30/Jan/2023:01:07:09 +0000 | 30/Jan/2023:00:07:09 +0000 | 1 | 0 | 1 | Update successful
```

<a id="entry-9-3-show-ssl-providers"></a>

**`show ssl providers`**

```haproxy
show ssl providers
```

Affiche les noms des fournisseurs chargés par OpenSSL lors de l'initialisation. Le chargement des fournisseurs peut effectivement être configuré via le fichier de configuration OpenSSL, et cette option permet de vérifier que les bons fournisseurs ont été chargés. Cette commande n'est disponible que sous OpenSSL v3.

Exemple :

```shell
$ echo "show ssl providers" | socat /var/run/haproxy.master -
Loaded providers:
    - fips
    - base
```

<a id="entry-9-3-show-ssl-sni"></a>

**`show ssl sni [-f <frontend>] [-A] [-t <offset>]`**

```haproxy
show ssl sni [-f <frontend>] [-A] [-t <offset>]
```

Affiche chaque SNI configuré pour le frontal désigné, ou tous les frontaux si aucun frontal n’a été spécifié. Cela permet de visualiser quels SNI sont proposés pour un frontal, et d’identifier si un SNI est défini plusieurs fois par plusieurs certificats pour le même frontal.

L'option -A permet de filtrer la liste et n'affiche que les certificats dont la date notAfter est dépassée, permettant ainsi d'afficher uniquement les certificats expirés.

L'option -t prend un décalage en secondes, ou avec une unité de temps (s, m, h, d), qui est ajouté à l'heure courante, permettant de vérifier quels certificats ont expiré après le décalage lorsqu'elle est combinée avec -A. Par exemple, si vous souhaitez vérifier quels certificats seraient expirés dans 30d, il suffit d'exécuter « show ssl sni -A -t 30d ».

Les colonnes sont séparées par un unique &#92;t, permettant une analyse simple.

La colonne « Frontend/Bind » indique le nom du frontal suivi de la position de la ligne de liaison dans la configuration (frontend/file:linenum).

La colonne « SNI » affiche le SNI, qui peut être un CN, un SAN ou un filtre provenant d'une liste de certificats (crt-list). Les certificats par défaut d'une ligne bind (qui sont soit déclarés explicitement via default-crt, soit implicites, à savoir le premier certificat d'une ligne bind lorsque strict-sni n'est pas utilisé) affichent le caractère « \* » dans la colonne SNI.

La colonne « Filtrage négatif » contient la liste des filtres négatifs associés à un joker. Elle affiche tous les filtres négatifs présents sur la même ligne de la liste crt. Un trait de soulignement est affiché s’il n’y en a aucun.

La colonne « Type » indique le type d'algorithme de chiffrement, qui peut être « rsa », « ecdsa » ou « dsa ».

La colonne « Filename » peut être soit un nom de fichier provenant de la configuration, soit un alias déclaré dans un crt-store.

Les colonnes « NotAfter » et « NotBefore » sont extraites directement du certificat X509 feuille.

Exemple :

```shell
$ echo "@1 show ssl sni -A -t 30d" | socat /var/run/haproxy-master.sock - | column -t -s $'\t'
# Frontend/Bind        SNI        Negative Filter  Type   Filename             NotAfter                  NotBefore
li1/haproxy.cfg:10021  *.ex.lan   !m1.ex.lan       rsa    example.lan.pem      Jun 13 13:37:21 2024 GMT  May 14 13:37:21 2024 GMT
li1/haproxy.cfg:10021  machine10  -                ecdsa  machine10.pem.ecdsa  Jun 13 13:37:21 2024 GMT  May 14 13:37:21 2024 GMT
li1/haproxy.cfg:10021  machine10  -                rsa    machine10.pem.rsa    Jun 13 13:37:21 2024 GMT  May 14 13:37:21 2024 GMT
li1/haproxy.cfg:10021  machine10  -                ecdsa  machine10.pem.ecdsa  Jun 13 13:37:21 2024 GMT  May 14 13:37:21 2024 GMT
li1/haproxy.cfg:10021  localhost  -                rsa    localhost.pem.rsa    Jun 13 13:37:11 2024 GMT  May 14 13:37:11 2024 GMT
li1/haproxy.cfg:10021  localhost  -                ecdsa  localhost.pem.ecdsa  Jun 13 13:37:10 2024 GMT  May 14 13:37:10 2024 GMT
li1/haproxy.cfg:10021  *          -                rsa    localhost.pem.rsa    Jun 13 13:37:11 2024 GMT  May 14 13:37:11 2024 GMT
```

<a id="entry-9-3-show-startup-logs"></a>

**`show startup-logs`**

```haproxy
show startup-logs
```

Affiche tous les messages émis pendant le démarrage du processus HAProxy actuel, chaque tampon startup-logs étant unique à son worker HAProxy.

Ce mot-clé existe également sur l’interface CLI principale, qui affiche la dernière tentative de démarrage ou de rechargement.

<a id="entry-9-3-show-table"></a>

**`show table`**

```haproxy
show table
```

Affiche des informations générales sur toutes les tables de persistance connues. Leur nom est retourné (le nom du proxy qui les contient), leur type (actuellement toujours zéro, toujours IP), leur taille maximale en nombre d'entrées possible, ainsi que le nombre d'entrées actuellement utilisées.

Exemple :

```shell
    $ echo "show table" | socat stdio /tmp/sock1
>>> # table: front_pub, type: ip, size:204800, used:171454
>>> # table: back_rdp, type: ip, size:204800, used:0
```

<a id="entry-9-3-show-table-2"></a>

**`show table <name> [ data.<type> <operator> <value> [data.<type> ...]] |`**

```haproxy
show table <name> [ data.<type> <operator> <value> [data.<type> ...]] |
                  [ key <key> ] | [ ptr <ptr> ]
```

Affiche le contenu de la table de persistance `<name>`. Dans ce mode, une première ligne d'information générique sur la table est affichée, comme avec la commande « show table », suivie de l'affichage de toutes les entrées. Étant donné que cela peut être très lourd, il est possible de spécifier un filtre afin de préciser les entrées à afficher.

Lorsque le formulaire "data." est utilisé, le filtre s'applique aux données stockées (voir « stick-table » dans la section 4.2). Un type de données stockées doit être spécifié dans `<type>`, et ce type de données doit être stocké dans la table, sinon une erreur est signalée. Les données sont comparées selon `<operator>` avec l'entier 64 bits `<value>`. Les opérateurs sont les mêmes qu'avec les ACLs :

    - eq : correspond aux entrées dont les données sont égales à cette valeur
    - ne : correspond aux entrées dont les données sont différentes de cette valeur
    - le : correspond aux entrées dont les données sont inférieures ou égales à cette valeur
    - ge : correspond aux entrées dont les données sont supérieures ou égales à cette valeur
    - lt : correspond aux entrées dont les données sont inférieures à cette valeur
    - gt : correspond aux entrées dont les données sont supérieures à cette valeur

Dans cette forme, vous pouvez utiliser plusieurs entrées de filtre de données, jusqu'à un maximum défini au moment de la compilation (4 par défaut).

Lorsque la forme clé est utilisée, l'entrée `<key>` est affichée. La clé doit être du même type que la table, ce qui est actuellement limité à IPv4, IPv6, entier et chaîne.

Lorsque la forme ptr est utilisée, l'entrée `<ptr>` est affichée. `<ptr>` est écrite sous la forme 0xffff et doit correspondre à l'adresse renvoyée par une commande précédente « show table ». Correspondre à une entrée à l'aide de son pointeur peut être pertinent si l'entrée ne peut pas être identifiée à l'aide de sa clé en raison d'une clé vide ou de caractères incompatibles sur le CLI.

Si data.`<type>` est de type tableau, on peut utiliser « [] » pour accéder à un index spécifique du tableau, comme ceci : data.gpt[1]

Exemple :

```shell
    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a4c: key=127.0.0.1 use=0 exp=3594729 gpc0=0 conn_rate(30000)=1  \
      bytes_out_rate(60000)=187
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191

    $ echo "show table http_proxy data.gpc0 gt 0" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191

    $ echo "show table http_proxy data.conn_rate gt 5" | \
        socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191

    $ echo "show table http_proxy key 127.0.0.2" | \
        socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191

    $ echo "show table http_proxy ptr 0x80e6a80" | \
        socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191
```

Lorsque le critère de données s'applique à une valeur dynamique dépendante du temps, comme un débit en octets, la valeur est calculée dynamiquement pendant l'évaluation de l'entrée afin de déterminer si elle doit être envoyée ou non. Cela signifie qu'un tel filtre peut correspondre pendant une certaine période, puis ne plus correspondre, car au fil du temps, le débit moyen des événements diminue.

Il est possible d'utiliser cette fonctionnalité pour extraire des listes d'adresses IP abuseuses du service, afin de les surveiller ou même de les bloquer dans un pare-feu. Exemple :

```shell
$ echo "show table http_proxy data.gpc0 gt 0" \
  | socat stdio /tmp/sock1 \
  | fgrep 'key=' | cut -d' ' -f2 | cut -d= -f2 > abusers-ip.txt
  ( ou | awk '/key/{ print a[split($2,a,"=")]; }' )
```

Lorsque la table de persistance est synchronisée avec une section peers prenant en charge le fractionnement, le numéro de fraction sera affiché pour chaque clé (sinon, « 0 » est indiqué). Cela permet de savoir quels peers recevront cette clé. Exemple :

```shell
$ echo "show table http_proxy" | socat stdio /tmp/sock1 | fgrep shard=
  0x7f23b0c822a8: key=10.0.0.2 use=0 exp=296398 shard=9 gpc0=0
  0x7f23a063f948: key=10.0.0.6 use=0 exp=296075 shard=12 gpc0=0
  0x7f23b03920b8: key=10.0.0.8 use=0 exp=296766 shard=1 gpc0=0
  0x7f23a43c09e8: key=10.0.0.12 use=0 exp=295368 shard=8 gpc0=0
```

<a id="entry-9-3-show-tasks"></a>

**`show tasks`**

```haproxy
show tasks
```

Affiche le nombre de tâches actuellement dans la file d'exécution, le nombre d'occurrences pour chaque fonction, ainsi que leur latence moyenne lorsqu'elle est connue (pour les tâches pures avec le profilage des tâches activé).
La capture est un instantané de l'instant où elle est effectuée, et peut présenter des variations selon les tâches restantes dans la file au moment de l'opération, notamment en mode mono-thread où il y a moins de chances que les opérations d'E/S reconstituent la file (sauf si celle-ci est pleine).
Cette commande accède exclusivement au processus et peut provoquer des latences mineures mais mesurables lorsqu'elle est exécutée sur un processus fortement sollicité, elle ne doit donc pas être utilisée de manière abusive par des bots de surveillance.

<a id="entry-9-3-show-threads"></a>

**`show threads`**

```haproxy
show threads
```

Affiche certains états internes et structures pour chaque thread, ce qui peut aider les développeurs à comprendre un problème. La sortie est conçue pour être lisible en affichant un bloc par thread. Lorsque HAProxy est compilé avec USE_THREAD_DUMP=1, un mécanisme avancé de dump utilisant des signaux de thread est employé afin que chaque thread puisse afficher son propre état tour à tour. Sans cette option, le thread traitant la commande affiche tous ses détails, tandis que les autres sont moins détaillés. Un astérisque ('\*') est affiché devant le thread gérant la commande. Un chevron droit ('\>') peut également être affiché devant les threads qui n'ont fait aucune progression depuis la dernière invocation de cette commande, indiquant un bogue dans le code qui doit absolument être signalé. Lorsque cela se produit entre deux threads, cela indique généralement un blocage. Si un seul thread est concerné, il s'agit d'un autre type de bogue, comme une liste corrompue. Dans tous les cas, le processus n'est plus entièrement fonctionnel et doit être redémarré.

Le format de sortie n’est pas documenté intentionnellement afin de permettre une évolution facile en fonction des besoins identifiés, sans devoir maintenir une compatibilité descendante, tout comme pour « show activity », les valeurs n’ont pas de sens sans le code à portée de main.

<a id="entry-9-3-show-tls-keys"></a>

**`show tls-keys [id|*]`**

```haproxy
show tls-keys [id|*]
```

Affiche toutes les références de clés TLS chargées. L'identifiant de référence de la clé de ticket TLS et le fichier à partir duquel les clés ont été chargées sont indiqués. Ces deux éléments peuvent être utilisés pour mettre à jour les clés TLS à l'aide de la commande « set ssl tls-key ». Si un identifiant est spécifié en paramètre, les tickets correspondants seront affichés ; en utilisant \*, tous les tickets de toutes les références seront affichés.

<a id="entry-9-3-show-schema-json"></a>

**`show schema json`**

```haproxy
show schema json
```

Affichez le schéma utilisé pour la sortie de « show info json » et « show stat json ».

Il ne contient aucun espace supplémentaire afin de réduire le volume de sortie. Pour une lecture humaine, passer la sortie dans un formateur élégant peut être utile. Exemple :

\$ echo "show schema json" \| socat /var/run/haproxy.sock stdio \| &#92;
python -m json.tool

Le schéma suit la spécification « JSON Schema » (json-schema.org), et les vérificateurs peuvent ainsi être utilisés pour valider la sortie des commandes « show info json » et « show stat json » par rapport au schéma.

<a id="entry-9-3-show-trace"></a>

**`show trace [<source>]`**

```haproxy
show trace [<source>]
```

Affiche l'état actuel du traçage. Pour chaque source, une ligne est affichée avec un caractère unique indiquant si le traçage est arrêté, en attente ou en cours. Le réceptacle de sortie utilisé par le traçage est indiqué (ou « none » s'il n'a pas été défini), suivi du nombre d'événements perdus dans ce réceptacle, puis d'une brève description de la source. Si un nom de source est spécifié, une liste détaillée de tous les événements pris en charge par la source est affichée, ainsi que leur état pour chaque action (report, start, pause, stop), indiqué par un "+" s'ils sont activés, ou un "-" sinon. Tous ces événements sont indépendants, et un événement peut déclencher un démarrage sans être rapporté, et inversement.

<a id="entry-9-3-show-version"></a>

**`show version`**

```haproxy
show version
```

Affiche la version du processus HAProxy en cours d'exécution. Cette fonctionnalité est disponible depuis l'interface CLI du processus principal et des processus workers.
Exemple :

```shell
$ echo "show version" | socat /var/run/haproxy.sock stdio
2.4.9

$ echo "show version" | socat /var/run/haproxy-master.sock stdio
2.5.0
```

<a id="entry-9-3-shutdown-frontend"></a>

**`shutdown frontend <frontend>`**

```haproxy
shutdown frontend <frontend>
```

Supprime complètement le frontal spécifié. Tous les ports auxquels il était lié seront libérés. Il ne sera plus possible d'activer ce frontal après cette opération. Cette fonction est destinée à être utilisée dans des environnements où l'arrêt d'un proxy n'est tout simplement pas envisageable, mais où un proxy mal configuré doit être corrigé. Ainsi, il devient possible de libérer le port et de le réaffecter à un autre processus afin de restaurer les opérations. Une fois terminé, le frontal n'apparaîtra plus du tout sur la page de statistiques.

Le frontal peut être spécifié soit par son nom, soit par son identifiant numérique, précédé d'un dièse ('#').

Cette commande est restreinte et ne peut être émise que sur les sockets configurés au niveau « admin ».

<a id="entry-9-3-shutdown-session"></a>

**`shutdown session <id>`**

```haproxy
shutdown session <id>
```

Interrompre immédiatement le flux correspondant à l'identifiant de flux spécifié. Cet identifiant est le premier champ au début des lignes des dumps de la commande « show sess » (il correspond au pointeur de flux). Cette commande peut être utilisée pour interrompre un flux en cours depuis longtemps sans attendre l'expiration du délai d'expiration, ou lorsqu'une transmission infinie est en cours. Les flux ainsi interrompus sont signalés dans les journaux avec un indicateur « K ».

<a id="entry-9-3-shutdown-sessions-server"></a>

**`shutdown sessions server <backend>/<server>`**

```haproxy
shutdown sessions server <backend>/<server>
```

Interrompre immédiatement tous les flux associés au serveur spécifié. Cette fonction peut être utilisée pour interrompre les flux longs après qu’un serveur a été placé en mode maintenance, par exemple. Les flux ainsi interrompus sont signalés dans les journaux avec un indicateur « K ».

Les connexions backend restent en état inactif, sauf si le serveur est déjà en mode maintenance, auquel cas elles seront immédiatement planifiées pour suppression.

<a id="entry-9-3-trace"></a>

**`trace`**

```haproxy
trace
```

La commande « trace » seule affiche les sources de traçage, leur état actuel et leurs courtes descriptions. Elle n'est destinée qu'à servir de menu pour accéder aux niveaux suivants ; consultez les autres commandes « trace » ci-dessous.

<a id="entry-9-3-trace-0"></a>

**`trace 0`**

```haproxy
trace 0
```

Arrête immédiatement toutes les traces. Cette commande est destinée à être utilisée comme solution rapide pour terminer une session de débogage ou comme action d'urgence en cas d'activation de traces complexes sur plusieurs sources ayant un impact sur le service.

<a id="entry-9-3-trace-2"></a>

**`trace <source> [<args...>]`**

```haproxy
trace <source> [<args...>]
```

Configure les traces pour la source `<source>`. Sans argument, cela affiche la liste de toutes les commandes secondaires prises en charge par la source donnée. Plusieurs commandes secondaires peuvent être enchaînées. Les commandes suivantes sont prises en charge :

event [ [+\|-\|!]`<name>` ] Sans argument, cette commande affiche la liste de tous les événements pris en charge par la source désignée. Ils sont précédés d’un "-" si ils ne sont pas activés, ou d’un "+" s’ils sont activés. Il est important de noter qu’une seule trace peut être étiquetée avec plusieurs événements, et tant qu’un des événements activés correspond à l’un des événements étiquetés sur la trace, cet événement sera transmis au sous-système de traçage. Par exemple, la réception d’un cadre HTTP/2 de type HEADERS peut déclencher un événement cadre et un événement flux, car le cadre crée un nouveau flux. Si l’événement cadre ou l’événement flux est activé pour cette source, le cadre sera transmis au cadre de traçage.

    Avec un argument, il est possible de basculer l'état de chaque événement et de les activer ou désactiver individuellement. Deux mots-clés spéciaux sont pris en charge : « none », qui ne correspond à aucun événement et est utilisé pour désactiver tous les événements en une seule fois, et « any », qui correspond à tous les événements et est utilisé pour activer tous les événements en une seule fois. Les autres événements sont spécifiques à la source d'événements. Il est possible d'activer un événement en spécifiant son nom, éventuellement précédé du signe « + » pour une meilleure lisibilité. Il est possible de désactiver un événement en spécifiant son nom précédé du signe « - » ou « ! ».

    Une façon de désactiver complètement une source de traçage consiste à passer « event none », et cette source sera instantanément entièrement ignorée.

follow `<other_source>` : cela permet à la source `<source>` d'émettre également des traces lorsque l'autre source `<other_source>` est verrouillée sur un critère et que le même critère correspond également à la source actuelle. Par exemple, si une source est verrouillée sur une session, suivre cette source depuis une autre en fera émettre des traces pour toutes les occurrences liées à cette session. Cela peut être utilisé, dans une certaine mesure, pour suivre les requêtes backend associées aux connexions frontend. La source « session » facilite cette opération en fournissant des événements « new » et « end » utilisables pour le traitement de verrouillage. Notez que la source `<source>` n'a pas besoin d'avoir ses traces activées dans ce cas, et son état de traçage ne sera pas non plus affecté. Il se peut toutefois que certains événements soient manquants s'ils ne contiennent pas d'informations permettant de les corrélater avec l'élément suivi. La méta-source « all » peut également être utilisée avec cette commande : dans ce cas, toutes les sources suivront `<other_source>`.

Exemple :

```text
trace h1 lock session start sess_new pause sess_end follow session
```

level [`<level>`] : sans argument, cette commande affiche tous les niveaux de traçage pour cette source, le niveau actuel étant indiqué par une étoile ('\*') placée en tête. Avec un argument, ce niveau de traçage est modifié en fonction du niveau spécifié. Les niveaux de détail constituent une forme de filtres appliqués avant la remontée des événements. Ces filtres permettent d'inclure ou d'exclure sélectivement les événements selon leur niveau d'importance. Par exemple, un développeur peut avoir besoin de connaître précisément l'emplacement dans le code où un en-tête HTTP a été jugé invalide, tandis qu'un utilisateur final peut ne pas s'intéresser du tout à la validité de cet en-tête. Actuellement, il existe 5 niveaux distincts de traçage :

```text
user       Informations destinées à l'utilisateur courant de haproxy
           souhaitant observer son trafic. Des requêtes et réponses HTTP
           sont généralement rapportées sans grands détails. La plupart
           des sources en font le niveau par défaut pour faciliter
           l'exploitation.

proto      En plus du niveau "user", rapporte les mises à jour du protocole,
           par exemple les types de trames ou les en-têtes HTTP décodés.

state      En plus du niveau "proto", rapporte les transitions d'état
           (ou leurs échecs) dans les analyseurs. Les tentatives d'opération
           sont donc visibles, tandis que "proto" ne montre que l'opération
           finale.

data       En plus du niveau "state", rapporte les transferts de données
           entre les différentes couches.

developer  Rapporte tout ce qui est disponible, y compris des informations
           avancées telles que "breaking out of this loop", utiles seulement
           au développeur cherchant à comprendre un bogue rare sur le terrain.
           Les noms de fonctions ne sont rapportés qu'à ce niveau.
```

    Il est fortement recommandé d'utiliser uniquement le niveau « user » et de ne passer à d'autres niveaux que si un développeur vous y invite. Il est également conseillé de configurer les événements en premier lieu avant de passer à des niveaux supérieurs, afin d'éviter d'obtenir de nombreuses lignes si aucun filtrage n'est appliqué. La méta-source « all » peut également être utilisée avec cette commande : dans ce cas, le niveau sera appliqué à toutes les sources existantes simultanément.

lock [critère] Sans argument, cette commande affiche la liste de tous les critères pris en charge par cette source pour le traitement en verrouillage, et indique le choix actuel par une étoile ('\*') en tête de celui-ci. Le verrouillage signifie que la source se concentre sur le premier événement correspondant et ne conserve que le critère qui a déclenché cet événement, tout en ignorant les autres jusqu’à l’arrêt de la trace. Cela permet par exemple de capturer une trace sur une connexion unique ou sur un flux unique. Les critères suivants sont pris en charge par certaines traces, pas nécessairement par toutes, car certains pourraient ne pas être disponibles pour la source :

```text
backend      verrouille sur le backend ayant démarré la trace
connection   verrouille sur la connexion ayant démarré la trace
frontend     verrouille sur le frontend ayant démarré la trace
listener     verrouille sur l'écouteur ayant démarré la trace
nothing      ne verrouille sur rien
server       verrouille sur le serveur ayant démarré la trace
session      verrouille sur la session ayant démarré la trace
thread       verrouille sur le thread ayant démarré la trace
```

    En complément de cela, chaque source peut fournir jusqu'à 4 critères spécifiques, tels que des états internes ou des identifiants de connexion. Par exemple, dans HTTP/2, il est possible de s'ancrer sur un flux H2 et d'ignorer les autres flux une fois qu'une trace a commencé.

    Lorsqu'un critère est passé en argument, celui-ci est utilisé à la place des autres, et tout suivi existant est immédiatement interrompu afin de pouvoir redémarrer avec le nouveau critère. Le mot-clé spécial « nothing » est pris en charge par toutes les sources pour désactiver définitivement le suivi.

{ pause \| start \| stop } [ [+\|-\|!]événement ] Sans argument, cette commande affiche la liste des événements activés pour mettre automatiquement en pause, démarrer ou arrêter une trace pour cette source. Ces événements sont spécifiques à chaque source de trace. Avec un argument, elle active l’événement pour l’action indiquée (si précédé optionnellement par un '+') ou le désactive (si précédé d’un '-' ou d’un '!'). Le mot-clé spécial « now » n’est pas un événement et demande d’exécuter l’action immédiatement. Les mots-clés « none » et « any » sont pris en charge de la même manière qu’avec « trace event ».

    Les trois actions prises en charge sont respectivement « pause », « start » et « stop ».
    L’action « pause » énumère les événements qui feront arrêter une trace en cours et attendront un nouvel événement de démarrage pour la reprendre.
    L’action « start » énumère les événements qui mettent la trace en mode d’attente jusqu’à l’apparition d’un de ces événements de démarrage.
    L’action « stop » énumère les événements qui arrêtent définitivement la trace jusqu’à ce qu’elle soit réactivée manuellement.

    En pratique, il est pertinent de démarrer manuellement une trace avec « start now » sans tenir compte des événements, et de l’arrêter avec « stop now ».
    Pour capturer des séquences d’événements plus subtiles, il est utile de définir « start » sur un événement normal (comme la réception d’une requête HTTP) et « stop » sur un événement très rare (comme l’émission d’une erreur spécifique), afin de garantir que les derniers événements capturés correspondent aux critères souhaités.
    L’événement « pause » est utile pour détecter la fin d’une séquence, désactiver le verrouillage et attendre une nouvelle opportunité de capturer.
    Dans ce cas, il peut être pertinent d’activer le verrouillage pour ne repérer qu’un critère spécifique (par exemple, un flux), de définir « start » sur n’importe quel événement qui déclenche ce critère (par exemple, tous les événements qui créent un flux), « stop » sur l’anomalie attendue, et « pause » sur n’importe quel événement qui met fin à ce critère (par exemple, n’importe quel événement de fin de flux).
    Dans ce cas, le journal de trace contiendra des séquences complètes de séries parfaitement propres affectant un seul objet, jusqu’à la dernière séquence contenant tout, depuis le début jusqu’à l’anomalie.

sink [`<sink>`] Sans argument, cette commande affiche la liste de tous les réceptacles d'événements disponibles pour cette source, et le réceptacle actuellement configuré est précédé d'une étoile ('\*'). Le réceptacle « none » est toujours disponible et signifie que tous les événements sont simplement ignorés, bien que leur traitement ne soit pas ignoré (par exemple, les verrous sont toujours appliqués). D'autres réceptacles sont disponibles selon la configuration et les options de compilation, mais en général « stdout » et « stderr » sont utilisables en mode débogage, et des tampons en mémoire en anneau devraient également être disponibles. Lorsqu'un nom est spécifié, le réceptacle est immédiatement changé pour la source indiquée. Les événements ne sont pas modifiés pendant un changement de réceptacle. Dans le pire des cas, certains peuvent être perdus si un réceptacle invalide (ou « none ») est utilisé, mais les opérations continuent vers une destination différente. La méta-source « all » peut également être utilisée avec cette commande : dans ce cas, le réceptacle est appliqué à toutes les sources existantes en même temps.

verbosity [`<level>`] Sans argument, cette commande affiche tous les niveaux de verbosité disponibles pour cette source, le niveau actuel étant indiqué par une étoile ('\*') placée devant. Avec un argument, cette commande change le niveau de verbosité vers celui spécifié.

    Les niveaux de verbosité indiquent jusqu'où le décodeur de trace doit aller pour fournir des informations détaillées. Cela dépend de la source de trace, car certaines sources ne fournissent même pas de décodeur spécifique. Le niveau « quiet » est toujours disponible et désactive tout décodage. Il peut être utile pour comprendre ce qui se passe avant d'analyser les détails, car il a un impact très faible sur les performances et la taille de la trace. Lorsqu'une source ne déclare aucun niveau de verbosité, le niveau « default » est disponible et entraîne l'appel d'un décodeur lorsqu'il est spécifié dans les traces. Il s'agit d'un décodage opportuniste. Lorsque la source déclare des niveaux de verbosité, ceux-ci sont listés avec une description de leur signification. Dans ce cas, le décodeur de trace fourni par la source sera aussi précis que possible, en fonction des informations disponibles au point de trace. Le premier niveau au-dessus de « quiet » est défini par défaut.

<a id="entry-9-3-update-ssl-ocsp-response"></a>

**`update ssl ocsp-response <certfile>`**

```haproxy
update ssl ocsp-response <certfile>
```

Créez une requête OCSP pour le `<certfile>` spécifié et envoyez-la au répondant OCSP dont l'URI doit être indiqué dans la section « Authority Information Access » du certificat. Seul le premier URI est pris en compte. La réponse OCSP reçue en retour est ensuite vérifiée et insérée dans l'arbre local des réponses OCSP. Cette commande ne fonctionne que pour les certificats qui ont déjà une réponse OCSP stockée, soit parce qu'elle a été fournie lors de l'initialisation, soit si elle a été définie précédemment à l'aide des commandes « set ssl cert » ou « set ssl ocsp-response ». Si la réponse OCSP reçue est valide et a été correctement insérée dans l'arbre local, son contenu est affiché sur la sortie standard. Le format est identique à celui décrit dans « show ssl ocsp-response ».

<a id="entry-9-3-wait"></a>

**`wait { -h | <delay> } [<condition> [<args>...]]`**

```haproxy
wait { -h | <delay> } [<condition> [<args>...]]
```

Dans sa forme la plus simple, sans condition, cette directive attend simplement le délai demandé avant de poursuivre. Elle peut être utilisée pour collecter des métriques sur un intervalle spécifique.

Avec une condition et des arguments facultatifs, la commande attend que la condition spécifiée soit remplie, qu'elle échoue de manière irréversible, ou qu'elle reste non remplie pendant toute la durée `<delay>`. Les conditions prises en charge sont :

- be-removable `<proxy>` : attend que le backend proxy spécifié soit supprimable par la commande « del backend ». Certaines conditions ne seront jamais acceptées (par exemple, un backend non encore dépublié ou comportant des serveurs) et entraîneront l'affichage d'un message d'erreur précis indiquant la condition non remplie. Si tout est correct avant l'expiration du délai, un succès est retourné et l'opération est terminée.

- srv-removable `<proxy>`/`<server>` : cette directive attend que le serveur spécifié soit éligible à la suppression par la commande « del server », c’est-à-dire qu’il soit en maintenance et ne possède plus aucune connexion (ni active ni inactive). Certaines conditions ne seront jamais acceptées (par exemple, le serveur non en maintenance) et entraîneront la remontée d’un message d’erreur spécifique indiquant la condition non remplie. Le serveur pourrait même avoir été supprimé en parallèle et ne plus exister. Si tout est correct avant l’expiration du délai, un succès est retourné et l’opération est terminée.

L'unité par défaut pour le délai est les millisecondes, bien que d'autres unités soient acceptées si elles sont suffixées par les unités de temporisation usuelles (us, ms, s, m, h, d). Lorsqu'il est utilisé avec l'utilitaire 'socat', n'oubliez pas d'élargir le délai d'expiration de socat afin de couvrir le temps d'attente. Passer "-h" en premier ou en second argument fournit la syntaxe de la commande. Exemple :

```shell
$ socat -t20 /path/to/socket - <<< "show activity; wait 10s; show activity"

$ socat -t5 /path/to/socket - <<< "
    disable server px/srv1
    shutdown sessions server px/srv1
    wait 2s srv-removable px/srv1
    del server px/srv1"
```

## 9.4. CLI principale {#section-9-4}

L'interface CLI principale est une socket liée au processus principal en mode principal-worker. Cette interface CLI permet d'accéder aux commandes de socket Unix depuis tous les processus en cours d'exécution ou en cours de terminaison, et permet une supervision basique de ces processus.

L'interface CLI principale ne peut être configurée qu'à partir des arguments du programme HAProxy, via l'option -S. Cette option accepte également des options bind, séparées par des virgules.

Exemple :

```haproxy
# haproxy -W -S 127.0.0.1:1234 -f test1.cfg
# haproxy -Ws -S /tmp/master-socket,uid,1000,gid,1000,mode,600 -f test1.cfg
# haproxy -W -S /tmp/master-socket,level,user -f test1.cfg
```

### 9.4.1. Commandes CLI principales {#section-9-4-1}

<a id="entry-9-4-1-entry"></a>

**`@<[!]pid>`**

```haproxy
@<[!]pid>
```

L'interface CLI principale utilise une notation de préfixe spéciale pour accéder aux processus multiples. Cette notation est facilement identifiable car elle commence par un @.

Un préfixe @ peut être suivi d'un numéro de processus relatif ou d'un point d'exclamation suivi d'un PID. (Par exemple : @1 ou @!1271). Un @ seul peut être utilisé pour spécifier le processus principal. Les processus restants ne sont accessibles qu'avec le PID comme numéro de processus relatif, et ne sont utilisables qu'avec les processus actuels.

Ce préfixe peut être utilisé comme enveloppe avant une commande, indiquant que cette commande uniquement sera envoyée au processus désigné. Dans ce cas, la commande complète se termine à la fin de la ligne ou à la point-virgule, comme toute commande régulière.

Bugs : le protocole sockpair@ utilisé pour implémenter la communication entre le processus principal et le worker est connu pour ne pas être fiable sous macOS en raison d'un problème dans l'implémentation de sendmsg(2) de macOS. Une commande pourrait ne pas obtenir de réponse à cause de cela.

Exemples :

```shell
$ socat /var/run/haproxy-master.sock readline
prompt
master> @1 show info; @2 show info
[...]
Process_num: 1
Pid: 1271
[...]
Process_num: 2
Pid: 1272
[...]
master>

$ echo '@!1271 show info; @!1272 show info' | socat /var/run/haproxy-master.sock -
[...]
```

Le préfixe peut également être utilisé comme commande autonome pour basculer le contexte d'exécution par défaut vers le processus désigné, indiquant que toutes les commandes ultérieures seront exécutées dans ce processus, jusqu'à ce qu'une nouvelle commande '@' change à nouveau le contexte d'exécution.

Exemples :

```shell
$ socat /var/run/haproxy-master.sock readline
prompt
master> @1
1271> show info
[...]
1271> show stat
[...]
1271> @
master>

$ echo '@1; show info; show stat; @2; show info; show stat' | socat /var/run/haproxy-master.sock -
[...]
```

Remarque sur les limitations : quelques rares commandes modifient l'état d'une session CLI (par exemple, « set anon », « set timeout ») et peuvent ne pas se comporter exactement de la même manière lorsqu'elles sont exécutées depuis la CLI principale, en raison de l'envoi individuel des commandes sur des sessions CLI distinctes. De même, quelques rares commandes (« show events », « wait ») surveillent activement l'entrée ou la fermeture de la CLI et sont immédiatement interrompues lorsque la CLI est fermée. Ces commandes ne fonctionneront pas comme prévu via la CLI principale, car l'entrée de la commande est fermée après chaque exécution. Dans de tels cas rares, la variante « @@ » ci-dessous pourrait être plus adaptée.

<a id="entry-9-4-1-entry-2"></a>

**`@@<[!]pid> [command...]`**

```haproxy
@@<[!]pid> [command...]
```

Ce préfixe ou commande est très similaire au préfixe "@" documenté ci-dessus, à ceci près qu’il entre dans le processus worker, transmet la ligne de commande entière telle quelle à ce dernier et reste connecté jusqu’à la fin de l’exécution de la commande. Les points-virgules sont également transmis, permettant d’exécuter une commande en pipeline complète dans un processus worker. La connexion avec le worker reste ouverte jusqu’à la fin de l’exécution de la liste des commandes. Toute donnée envoyée après les commandes sera acheminée vers l’interface CLI du worker et pourra être consommée par les commandes en cours d’exécution, mais sera perdue pour l’interface CLI du master, offrant ainsi une connexion véritablement bidirectionnelle avec le processus worker. En conséquence, les utilisateurs de ces commandes doivent être extrêmement prudents et attendre la fin de l’exécution d’une commande avant d’envoyer de nouvelles commandes à l’interface CLI du master.

Au lieu d'exécuter une seule commande, il est également possible d'ouvrir une session entièrement interactive sur le processus worker en ne spécifiant aucune commande (c’est-à-dire « @@1 » sur une ligne seule). Cette session peut être terminée soit en fermant la connexion, soit en quittant le processus worker (à l’aide de la commande « quit »). Dans ce cas, le mode d’invite du socket principal (interactif, invite, temporisé) est propagé au processus worker.

Bugs : le protocole sockpair@ utilisé pour implémenter la communication entre le processus principal et le worker est connu pour ne pas être fiable sous macOS en raison d'un problème dans l'implémentation de sendmsg(2) de macOS. Une commande pourrait ne pas obtenir de réponse à cause de cela.

Exemples :

```shell
# gracefully close connections and delete a server once idle (wait max 10s)
$ socat -t 11 /var/run/haproxy-master.sock - <<< \
   "@@1 disable server app2/srv36; \
   wait 10000 srv-removable app2/srv36; \
   del server app2/srv36"

# forcefully close connections and quickly delete a server
$ socat /var/run/haproxy-master.sock - <<< \
   "@@1 disable server app2/srv36; \
   shutdown sessions server app2/srv36; \
   wait 100 srv-removable app2/srv36; \
   del server app2/srv36"

# show messages arriving to this ring in real time ("tail -f" equivalent)
$ (echo "show events buf0 -w"; read) | socat /var/run/haproxy-master.sock -
```

<a id="entry-9-4-1-expert-mode"></a>

**`expert-mode [on|off]`**

```haproxy
expert-mode [on|off]
```

Cette commande active le mode « expert » pour chaque worker accédé depuis l'interface CLI principale. En combinaison avec « mcli-debug-mode », elle active également la commande sur le maître. Affiche le drapeau « e » dans l'invite de l'interface CLI principale.

Voir également « expert-mode » dans [Section 9.3](/fr/haproxy/statistics-and-monitoring/#section-9-3) et « mcli-debug-mode » dans 9.4.1.

<a id="entry-9-4-1-experimental-mode"></a>

**`experimental-mode [on|off]`**

```haproxy
experimental-mode [on|off]
```

Cette commande active le mode expérimental pour chaque worker accédé depuis l'interface CLI principale.
En combinaison avec « mcli-debug-mode », elle active également la commande sur le maître. Affiche le drapeau « x » dans l'invite de l'interface CLI principale.

Voir également « experimental-mode » dans [Section 9.3](/fr/haproxy/statistics-and-monitoring/#section-9-3) et « mcli-debug-mode » dans 9.4.1.

<a id="entry-9-4-1-hard-reload"></a>

**`hard-reload`**

```haproxy
hard-reload
```

Cette commande agit de la même manière que la commande « reload » sur l'interface CLI principale, à ceci près qu'elle effectue une interruption brutale (-st) au lieu d'une interruption douce (-sf) du processus précédent. Cela signifie que le processus précédent ne s'arrête pas en attendant la réalisation de quoi que ce soit, de sorte que toutes les connexions seront fermées.

Voir également la commande « reload ».

<a id="entry-9-4-1-mcli-debug-mode"></a>

**`mcli-debug-mode [on|off]`**

```haproxy
mcli-debug-mode [on|off]
```

Ce mot-clé permet d’activer un mode spécial dans l’interface CLI principale, qui permet d’utiliser sur l’interface CLI principale toutes les commandes destinées à l’interface CLI des workers, ce qui permet de déboguer le processus principal. Une fois activé, listez les nouvelles commandes disponibles à l’aide de « help ». En combinaison avec « experimental-mode » ou « expert-mode », il active encore plus de commandes. Affichez le drapeau « d » dans l’invite de l’interface CLI principale.

<a id="entry-9-4-1-prompt"></a>

**`prompt`**

```haproxy
prompt
```

Lorsque l’invite est activée (via la commande « prompt »), le contexte sur lequel le CLI opère est affiché dans l’invite. Le processus principal est identifié par la chaîne « master », tandis que les autres processus sont identifiés par leur PID. En cas d’échec du dernier rechargement, l’invite du processus principal est modifiée en « master[ReloadFailed]\> », afin de rendre visible le fait que le processus continue de fonctionner avec la configuration précédente et que la nouvelle configuration n’est pas opérationnelle.

L'invite de la CLI principale est capable d'afficher plusieurs indicateurs correspondant aux modes activés. « d » pour mcli-debug-mode, « e » pour expert-mode, « x » pour experimental-mode.

Exemple :

```shell
$ socat /var/run/haproxy-master.sock -
prompt
master> expert-mode on
master(e)> experimental-mode on
master(xe)> mcli-debug-mode on
master(xed)> @1
95191(xed)>
```

<a id="entry-9-4-1-reload"></a>

**`reload`**

```haproxy
reload
```

Vous pouvez également recharger le processus principal HAProxy à l’aide de la commande « reload », qui produit le même effet qu’un `kill -USR2` sur le processus principal, à condition que l’utilisateur dispose au moins des privilèges « operator » ou « admin ».

Cette commande permet d'effectuer un rechargement synchrone ; la commande renvoie un statut de rechargement une fois celui-ci effectué. Prenez garde au délai d'expiration si un outil est utilisé pour l'analyser, car il n'est renvoyé qu'après analyse de la configuration et création du nouveau processus worker. La commande « socat » utilise un délai d'expiration par défaut de 0,5 s, donc elle se termine avant d'afficher le message si le rechargement dure trop longtemps. « ncat » ne dispose pas de délai d'expiration par défaut. Lorsqu'il est compilé avec USE_SHM_OPEN=1, la commande de rechargement peut également exporter les journaux de démarrage du processus principal.

Exemple :

```shell
$ echo "reload" | socat -t300 /var/run/haproxy-master.sock stdin
Success=1
--
[NOTICE]   (482713): haproxy version is 2.7-dev7-4827fb-69
[NOTICE]   (482713): path to executable is ./haproxy
[WARNING]  (482713): config: 'http-request' rules ignored for proxy 'frt1' as they require HTTP mode.
[NOTICE]   (482713): New worker (482720) forked
[NOTICE]   (482713): Loading success.

$ echo "reload" | socat -t300 /var/run/haproxy-master.sock stdin
Success=0
--
[NOTICE]   (482886): haproxy version is 2.7-dev7-4827fb-69
[NOTICE]   (482886): path to executable is ./haproxy
[ALERT]    (482886): config: parsing [test3.cfg:1]: unknown keyword 'Aglobal' out of section.
[ALERT]    (482886): config: Fatal errors found in configuration.
[WARNING]  (482886): Loading failure!

$
```

La commande reload est la dernière exécutée sur l’interface CLI principale ; toutes les autres commandes suivantes sont ignorées.
Dès que la commande reload a renvoyé son statut, la connexion à l’interface CLI est fermée.

Notez qu’un rechargement fermera toutes les connexions vers l’interface CLI principale. Voir également la commande « hard-reload ».

<a id="entry-9-4-1-show-proc"></a>

**`show proc [debug]`**

```haproxy
show proc [debug]
```

L'interface CLI principale introduit une commande « show proc » pour surveiller les processus.

Exemple :

```shell
$ echo 'show proc' | socat /var/run/haproxy-master.sock -
#<PID>          <type>          <reloads>       <uptime>        <version>
1162            master          5 [failed: 0]   0d00h02m07s     2.5-dev13
# workers
1271            worker          1               0d00h00m00s     2.5-dev13
# old workers
1233            worker          3               0d00h00m43s     2.0-dev3-6019f6-289
```

Dans cet exemple, le maître a été rechargé 5 fois, mais un des anciens workers est toujours en cours d'exécution et a survécu à 3 rechargements. Vous pouvez accéder à l'interface CLI de ce worker pour comprendre ce qui se passe.

Le paramètre « debug » est utile pour afficher les détails de débogage ; il affiche actuellement les descripteurs de fichiers (FDs) utilisés pour la communication IPC. Notez que la sortie de débogage n'est pas garantie stable entre les versions de HAProxy.

<a id="entry-9-4-1-show-startup-logs"></a>

**`show startup-logs`**

```haproxy
show startup-logs
```

HAProxy doit être compilé avec USE_SHM_OPEN=1 pour être utilisé correctement sur l'interface CLI principale ou tous les messages ne seront pas visibles.

Comme son homologue sur la socket de statistiques, cette commande est capable d’afficher les messages de démarrage de HAProxy. Toutefois, elle ne fournit pas les messages de démarrage du worker actuel, mais ceux de la dernière initialisation ou rechargement, ce qui permet de récupérer les messages d’analyse d’un rechargement échoué.

Ces messages sont également affichés avec la commande « reload ».

## 9.5. Fichier de statistiques {#section-9-5}

Un fichier appelé stats-file peut être utilisé pour charger au démarrage du processus des compteurs internes de HAProxy avec des valeurs non nulles. Son usage principal consiste à préserver les statistiques des processus workers lors des rechargements. Seule une partie des statistiques exposées par HAProxy est présente dans un fichier stats-file, car il n’a de sens que de charger des valeurs de type métrique.

Pour l'instant, seuls les compteurs de proxy sont pris en charge dans stats-file. Cela permet de précharger des valeurs pour les frontaux, les backends, les serveurs et les écouteurs. Toutefois, seuls les objets dont l'identifiant GUID n'est pas vide sont stockés dans un fichier stats-file. Cela garantit que les valeurs seront préchargées pour les objets ayant un type et un GUID correspondants, même si d'autres paramètres diffèrent.

La commande CLI « dump stats-file » a pour but de générer un fichier de statistiques. Le format de ce fichier est défini en interne et peut faire l'objet de modifications ou d'extensions futures sans préavis. Il est conçu pour être compatible au moins entre les versions stables adjacentes de HAProxy, mais peut nécessiter une configuration optionnelle supplémentaire lors du chargement d'un fichier de statistiques dans un processus exécutant une version plus ancienne.
