---
title: "3. Démarrage de HAProxy"
linkTitle: "3. Démarrage de HAProxy"
weight: 270
description: "Syntaxe de ligne de commande, options, chargement de la configuration et comportement au démarrage"
icon: fa-solid fa-play
module: [HAPROXY]
categories: [Tâche]
aliases:
  - /haproxy/management/starting/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 3"
---

HAProxy est lancé en exécutant le programme « haproxy » avec un certain nombre d'arguments passés en ligne de commande. La syntaxe réelle est :

```shell
$ haproxy [<options>]*
```

où [`<options>`]\* est un nombre quelconque d'options. Une option commence toujours par '-' suivi d'une ou plusieurs lettres, et peut être suivie d'un ou plusieurs arguments supplémentaires. Sans option, HAProxy affiche la page d'aide avec un rappel des options prises en charge. Les options disponibles peuvent varier légèrement selon le système d'exploitation. Un nombre important de ces options se chevauchent avec une option équivalente dans la section « global ». Dans ce cas, la ligne de commande a toujours priorité sur le fichier de configuration, de sorte que la ligne de commande peut être utilisée pour imposer rapidement certains paramètres sans modifier les fichiers de configuration. La liste actuelle des options est :

<a id="entry-3-entry"></a>

**`-- <cfgfile>*`**

```haproxy
-- <cfgfile>*
```

Tous les arguments qui suivent "--" sont des chemins de fichiers ou de répertoires de configuration, chargés et traités dans l'ordre de déclaration. Cette forme est surtout utile lorsque le shell charge de nombreux fichiers ordonnés numériquement. Voir aussi "-f". Avec "-f", chaque nom de fichier doit être précédé de l'option, tandis qu'un seul "--" suffit avant l'ensemble des noms. Ces options peuvent être combinées et l'ordre de la ligne de commande continue de s'appliquer. Lorsque plusieurs fichiers sont indiqués, chacun doit commencer à une frontière de section ; son premier mot-clé doit donc être "global", "defaults", "peers", "listen", "frontend", "backend", etc. Un fichier ne peut pas contenir uniquement une liste de serveurs.

<a id="entry-3-f"></a>

**`-f <cfgfile|cfgdir>`**

```haproxy
-f <cfgfile|cfgdir>
```

ajoute `<cfgfile>` à la liste des fichiers de configuration à charger. Si `<cfgdir>` est un répertoire, tous les fichiers qu'il contient, et uniquement les fichiers, sont ajoutés à la liste dans l'ordre lexical (avec LC_COLLATE=C). Seuls les fichiers portant l'extension ".cfg" et les fichiers non cachés, sans préfixe ".", sont ajoutés. Les fichiers de configuration sont chargés et traités dans leur ordre de déclaration. Cette option peut être répétée pour charger plusieurs fichiers. Voir aussi "--". Avec "-f", chaque nom de fichier doit être précédé de l'option, tandis qu'un seul "--" suffit avant tous les noms. Ces options peuvent être combinées et l'ordre de la ligne de commande continue de s'appliquer. Lorsque plusieurs fichiers sont indiqués, chacun doit commencer à une frontière de section ; son premier mot-clé doit donc être "global", "defaults", "peers", "listen", "frontend", "backend", etc. Un fichier ne peut pas contenir uniquement une liste de serveurs.

<a id="entry-3-c"></a>

**`-C <dir>`**

```haproxy
-C <dir>
```

Change de répertoire pour `<dir>` avant de charger les fichiers de configuration. Cela est utile lorsque l'on utilise des chemins relatifs. Attention à l'utilisation de caractères génériques après "--", qui sont en réalité remplacés par le shell avant le démarrage de HAProxy.

<a id="entry-3-d"></a>

**`-D`**

```haproxy
-D
```

Démarrer en tant que démon. Le processus se détache du terminal actuel après avoir forké, et les erreurs ne sont plus signalées dans le terminal. Cette option équivaut au mot-clé « daemon » dans la section « global » de la configuration. Il est recommandé de toujours l'activer dans tout script d'initialisation afin qu'une configuration erronée ne bloque pas le démarrage du système.

<a id="entry-3-l"></a>

**`-L <name>`**

```haproxy
-L <name>
```

modifiez le nom du pair local en `<name>`, qui est par défaut le nom d'hôte local. Cela n'est utilisé que pour la réplication entre pairs. Vous pouvez utiliser la variable \$HAPROXY_LOCALPEER dans le fichier de configuration pour faire référence au nom du pair.

<a id="entry-3-n"></a>

**`-N <limit>`**

```haproxy
-N <limit>
```

définit la valeur par défaut de maxconn par proxy à `<limit>` au lieu de la valeur par défaut intégrée (généralement 2000).
Utile uniquement à des fins de débogage.

<a id="entry-3-v"></a>

**`-V`**

```haproxy
-V
```

active le mode verbeux (désactive le mode silencieux). Annule l'effet de "-q" ou de "quiet".

<a id="entry-3-w"></a>

**`-W`**

```haproxy
-W
```

mode master-worker. Il est équivalent au mot-clé « master-worker » dans la section « global » de la configuration. Ce mode lance un « master » qui surveille les « workers ». En utilisant ce mode, vous pouvez recharger HAProxy directement en envoyant un signal SIGUSR2 au master. Le mode master-worker est compatible avec le mode en premier plan ou en daemon. Il est recommandé d'utiliser ce mode avec le mode multiprocess et systemd.

<a id="entry-3-ws"></a>

**`-Ws`**

```haproxy
-Ws
```

Mode master-worker avec prise en charge du type `notify` de service systemd.

<a id="entry-3-4"></a>

**`-4`**

```haproxy
-4
```

Forcer les résolveurs DNS à interroger et à accepter uniquement des adresses IPv4 (enregistrements « A »). Cela peut être utilisé lorsque des difficultés surviennent dans certains environnements privés de connectivité dual-stack bout en bout. Cette option remplace la directive globale « dns-accept-family » et la force à « ipv4 ».

<a id="entry-3-c-2"></a>

**`-c`**

```haproxy
-c
```

ne fait que vérifier les fichiers de configuration et quitte avant toute tentative de liaison. Le code de sortie est zéro si tout est correct, ou non nul en cas d'erreur. Les avertissements éventuels sont signalés. Par défaut, cette option ne signale pas de message de succès. Associée à "-V", elle affiche le message « Configuration file is valid » en cas de succès.

Les scripts doivent utiliser le code de sortie pour déterminer la réussite de la commande.

<a id="entry-3-cc"></a>

**`-cc`**

```haproxy
-cc
```

évalue une condition telle qu'elle est utilisée dans un bloc conditionnel de la configuration. Le statut de sortie est zéro si la condition est vraie, 1 si la condition est fausse ou 2 en cas d'erreur rencontrée.

<a id="entry-3-d-2"></a>

**`-d`**

```haproxy
-d
```

activez le mode débogage. Cela désactive le mode démon, force le processus à rester en premier plan et à afficher les événements entrants et sortants. Cette option ne doit jamais être utilisée dans un script d'initialisation.

<a id="entry-3-entry-2"></a>

**`-dA[file]`**

```haproxy
-dA[file]
```

effectue une archive de toutes les dépendances détectées au démarrage dans le fichier désigné au format tar, immédiatement après le chargement de la configuration. Cela équivaut à « set-dumpable libs », mais au lieu de conserver les bibliothèques en mémoire, il les écrit dans un fichier. Cette fonction peut être utilisée après une image mémoire (core dump), afin de fournir à des développeurs toutes les bibliothèques nécessaires pour analyser le core. Cette fonctionnalité n’est pas disponible sur tous les systèmes d’exploitation. Il est fortement recommandé de l’utiliser avec les fichiers de configuration réguliers, et éventuellement avec "-c" lorsqu’elle est utilisée manuellement, afin que HAProxy se termine immédiatement après l’archive, sans démarrer. Exemple :

```shell
$ haproxy -dA/tmp/libs.tar -c -f /etc/haproxy/haproxy.cfg
```

<a id="entry-3-entry-3"></a>

**`-dC[key]`**

```haproxy
-dC[key]
```

Exporter le fichier de configuration. Cette opération est effectuée après le découpage en jetons, de sorte que les commentaires sont supprimés et l’indentation est forcée. Si une clé non nulle est spécifiée, les lignes sont tronquées avant les champs sensibles ou confidentiels, et les identifiants et adresses sont émis hachés avec cette clé en utilisant le même algorithme que celui utilisé en mode anonyme sur la ligne de commande. Cela signifie que la sortie peut être partagée en toute sécurité avec un développeur qui en a besoin pour comprendre ce qui se passe dans un dump anonymisé à l’aide de la même clé. Veuillez également consulter la commande « set anon » de la ligne de commande.

<a id="entry-3-dd"></a>

**`-dD`**

```haproxy
-dD
```

Active le mode diagnostic. Ce mode affiche des avertissements supplémentaires sur les instructions de configuration suspectes. Certains messages peuvent empêcher le démarrage en mode "zero-warning".

Ces diagnostics servent principalement à attirer l’attention des opérateurs sur des problèmes potentiels encore inapparents, parfois liés à des configurations parfaitement intentionnelles. Ils peuvent changer même au sein d’une branche stable, ainsi qu’entre des machines exécutant exactement la même configuration. Ils *signaleront* donc régulièrement comme suspectes des instructions pourtant valides. Ils ne devraient être utilisés qu’avec "-c" pour effectuer un diagnostic plus approfondi. Leur résultat ne devrait jamais servir à empêcher le démarrage d’un service, ce qui se produit lorsqu’ils sont combinés avec "zero-warning" ou "-dW".

<a id="entry-3-df"></a>

**`-dF`**

```haproxy
-dF
```

désactive le transfert accéléré des données. Il s'agit d'un mécanisme d'optimisation du transfert de données qui consiste à acheminer les données directement d'un côté à l'autre sans réveiller le flux. Grâce à cette directive, il est possible de désactiver cette optimisation. Notez qu'elle désactive également tout splice TCP du noyau. Cette commande n'est pas destinée à une utilisation régulière ; elle sera généralement proposée uniquement par les développeurs lors de sessions de débogage complexes.

<a id="entry-3-dg"></a>

**`-dG`**

```haproxy
-dG
```

désactive l'utilisation de getaddrinfo() pour résoudre les noms d'hôtes en adresses. Cette option peut être utilisée lorsque l'on suspecte que getaddrinfo() ne fonctionne pas comme prévu. Cette option a été mise à disposition en raison de la présence de nombreuses implémentations incorrectes de getaddrinfo() sur divers systèmes, qui provoquent des anomalies difficiles à diagnostiquer.

<a id="entry-3-di"></a>

**`-dI`**

```haproxy
-dI
```

activez le fork non sécurisé. Ceci équivaut à l’option « insecure-fork-wanted » dans la section globale. Cela peut être utile lors de l’exécution de tous les tests de régularité avec ASAN, qui nécessitent de faire un fork d’addr2line pour résoudre les adresses.

<a id="entry-3-entry-4"></a>

**`-dK<class[,class]*>`**

```haproxy
-dK<class[,class]*>
```

affiche la liste des mots-clés enregistrés dans chaque classe. La liste des classes est disponible avec
"-dKhelp". Toutes les classes peuvent être affichées en utilisant "-dKall", sinon une sélection parmi celles indiquées dans l’aide peut être spécifiée sous forme d’une liste séparée par des virgules. Le format de sortie varie selon la classe de mots-clés affichée (par exemple, "cfg" affiche les mots-clés de configuration connus dans un format ressemblant au format de fichier de configuration, tandis que "smp" affiche les fonctions d'extraction d'échantillon précédées d'une matrice de compatibilité par ensemble de règles). Ces sorties peuvent rarement être utilisées directement par des humains, mais elles peuvent être très utiles pour des outils externes cherchant à détecter l’apparition de nouveaux mots-clés à certains endroits afin de mettre automatiquement à jour certaines documentations, fichiers de mise en évidence syntaxique, analyseurs de configuration, API, etc. Le format de sortie peut évoluer légèrement au fil du temps, aussi est-il fortement recommandé d’utiliser cette sortie principalement pour détecter les différences par rapport à des archives antérieures. Notez qu’il n’est pas possible de lister tous les mots-clés, car de nombreux mots-clés existaient bien avant la création des différents systèmes d’enregistrement des mots-clés, et ils n’apparaissent donc pas ici. Toutefois, puisque les nouveaux mots-clés ne sont ajoutés que par les mécanismes modernes, il est raisonnablement sûr de supposer que cette sortie peut être utilisée pour détecter les ajouts de langage avec une bonne précision. Les mots-clés ne sont affichés qu’après analyse complète de la configuration, afin que même les mots-clés créés dynamiquement puissent être inclus. Une bonne manière de produire une sortie et de quitter est d’exécuter une vérification silencieuse de configuration sur une configuration existante :

```text
./haproxy -dKall -q -c -f foo.cfg
```

Si aucun fichier de configuration n'est disponible, l'utilisation de "-f /dev/null" permet également d'extraire tous les mots-clés par défaut, mais le code de retour ne sera pas zéro, car aucun écouteur ne sera présent, et devra être ignoré.

<a id="entry-3-dl"></a>

**`-dL`**

```haproxy
-dL
```

affiche la liste des bibliothèques partagées dynamiques chargées à la fin du traitement de la configuration. Celle-ci inclut généralement aussi des dépendances profondes, telles que tout ce qui est chargé depuis du code Lua, ainsi que l'exécutable lui-même. La liste est affichée au format permettant de la nettoyer facilement afin de produire directement une archive tar de toutes les dépendances. Comme cette commande ne bloque pas le démarrage du programme, il est recommandé de ne l'utiliser qu'en combinaison avec "-c" et "-q", où seule la liste des objets chargés sera affichée (ou rien en cas d'erreur). En outre, gardez à l'esprit que, lors de la fourniture d'un tel package pour aider à l'analyse d'un fichier core, la plupart des bibliothèques sont en réalité des liens symboliques qui doivent être déréférencés lors de la création de l'archive :

```text
./haproxy -W -q -c -dL -f foo.cfg | tar -T - -hzcf archive.tgz
```

Lorsqu'il est lancé en mode verbeux (-V), les plages d'adresses des bibliothèques partagées sont également énumérées, à moins que le mode silencieux ne soit activé (-q).

<a id="entry-3-entry-5"></a>

**`-dM[<byte>[,]][help|options,...]`**

```haproxy
-dM[<byte>[,]][help|options,...]
```

force l'empoisonnement de la mémoire, et/ou modifie d'autres options de débogage de la mémoire. L'empoisonnement de la mémoire signifie que chaque région mémoire allouée avec malloc() ou pool_alloc() sera remplie avec `<byte>` avant d'être renvoyée au demandeur. Lorsque `<byte>` n'est pas spécifié, sa valeur par défaut est 0x50 ('P'). Bien que cela ralentisse légèrement les opérations, cela permet de déclencher de manière fiable les problèmes dus à une initialisation manquante dans le code, provoquant des crashs aléatoires. Notez que -dM0 a pour effet de transformer tout appel à malloc() en un appel à calloc(). Dans tous les cas, si un bug apparaît ou disparaît lors de l'utilisation de cette option, cela signifie qu'il y a un bug dans haproxy, veuillez le signaler. Plusieurs autres options sont disponibles, soit seules, soit après une virgule suivant le byte. L'option spéciale « help » affiche la liste des options prises en charge actuellement ainsi que leurs valeurs actuelles. Chaque option de débogage peut être activée ou désactivée. Les options les plus optimales sont généralement choisies au moment de la compilation en fonction du système d'exploitation et n'ont pas besoin d'être ajustées, sauf si suggérées par un développeur. Les options de débogage prises en charge incluent (activer/désactiver) :

- fail / no-fail :

```text
Active des échecs aléatoires d'allocation mémoire, conjointement avec
le paramètre global "tune.fail-alloc". Cela permet de détecter les
vérifications d'erreur manquantes dans le code. Cette option prédéfinit
un taux d'échec de 1%.
```

- no-merge / merge :

```text
Par défaut, les pools de tailles très proches sont fusionnés pour
améliorer l'efficacité, ce qui complique l'analyse de certains dumps
mémoire. Cette option désactive ce mécanisme et peut légèrement
augmenter la consommation mémoire.
```

- cold-first / hot-first :

```text
Pour optimiser le taux de succès du cache CPU, les objets libérés le
plus récemment ("hot") sont réutilisés par défaut pour les nouvelles
allocations. Cela complique toutefois l'analyse des dumps mémoire et
peut masquer les utilisations après libération. Cette option sélectionne
plutôt les objets les plus froids en premier, ce qui peut légèrement
augmenter l'utilisation du CPU.
```

- integrity / no-integrity :

```text
Active les vérifications d'intégrité mémoire de la zone allouée pour
s'assurer qu'elle n'a pas été modifiée depuis sa dernière libération.
Cette option fonctionne au mieux avec "no-merge", "cold-first" et "tag".
Son activation augmente légèrement l'utilisation du CPU.
```

- backup / no-backup :

```text
Copie chaque objet lors de sa libération pour permettre aux développeurs
de l'inspecter. Compare aussi son contenu au moment de l'allocation
pour détecter une modification intermédiaire, signe d'une utilisation
après libération. Cela double la consommation mémoire et augmente
légèrement l'utilisation du CPU (comme "integrity"). Avec "integrity",
le contenu est toujours dupliqué mais la comparaison n'est pas réalisée
ici : elle est effectuée par "integrity". Comme "integrity", cette
option fonctionne au mieux avec "no-merge", "cold-first" et "tag".
```

- no-global / global :

```text
Selon le système d'exploitation, un cache mémoire global au processus
peut être activé si l'allocateur standard est jugé trop lent ou peu
efficace avec les threads. Cette option impose son activation ou sa
désactivation. Le désactiver peut augmenter l'utilisation du CPU avec
un allocateur inefficace ; l'activer peut augmenter la consommation
mémoire avec un allocateur efficace.
```

- no-cache / cache :

```text
Chaque thread dispose d'un cache local d'objets très rapide pour les
allocations, toujours activé par défaut. Cette option le désactive.
Comme le cache global passe aussi par les caches locaux, cela désactive
effectivement tous les caches et alloue directement via l'allocateur
par défaut. L'utilisation du CPU peut augmenter fortement, mais un
petit système peut aussi économiser un peu de mémoire.
```

- caller / no-caller :

```text
Réserve un espace supplémentaire dans chaque objet alloué pour y
stocker l'adresse du dernier appelant l'ayant alloué ou libéré.
Cela aide les développeurs à reconstituer l'historique lors de
l'analyse des dumps mémoire et à comprendre un événement inattendu.
```

- tag / no-tag :

```text
Réserve un espace supplémentaire dans chaque objet alloué pour une
marque permettant de détecter une double libération, la libération
d'un objet invalide ou un débordement de tampon. Les garanties de
fiabilité sont nettement renforcées au prix de 4 ou 8 octets
supplémentaires par allocation. C'est généralement la première étape
pour détecter une corruption mémoire.
```

- poison / no-poison :

```text
Remplit les objets alloués d'un motif fixe pour empêcher la présence
de valeurs accidentelles telles que 0 lorsqu'un nouveau champ a été
oublié dans une routine d'initialisation. Ces bogues se reproduisent
rarement, surtout lorsque les pools ne sont pas fusionnés. Cette
fonction est normalement activée en passant directement la valeur
de l'octet à -dM ; cette option permet de désactiver ou réactiver
l'emploi d'une valeur déjà définie.
```

<a id="entry-3-dr"></a>

**`-dR`**

```haproxy
-dR
```

désactive l'option de socket SO_REUSEPORT sur les ports d'écoute. Cela équivaut à la directive "noreuseport" de la section "global". Cette option peut être appliquée dans les scénarios à multi-threading lorsque des problèmes de répartition de charge sont observés entre les threads HAProxy (pouvant être surveillés avec top).

<a id="entry-3-ds"></a>

**`-dS`**

```haproxy
-dS
```

désactive l'utilisation de l'appel système splice(). Cela équivaut à la directive "nosplice" dans la section "global". Cette option peut être utilisée lorsque splice() est suspecté de se comporter de manière incorrecte ou de provoquer des problèmes de performance, ou lorsqu'on utilise strace pour visualiser les données transférées (lesquelles ne sont pas visibles lorsqu'on utilise splice()).

<a id="entry-3-dt"></a>

**`-dT`**

```haproxy
-dT
```

désactive l'utilisation de ktls. Cela équivaut à la directive « noktls » de la section « global ». Cela est principalement utile lorsqu'un bug lié à ktls est suspecté.

<a id="entry-3-dv"></a>

**`-dV`**

```haproxy
-dV
```

Désactive la vérification SSL du côté serveur. Cela équivaut à la directive « ssl-server-verify none » dans la section « global ». Cela est utile pour reproduire des problèmes de production en dehors de l’environnement de production. Ne jamais utiliser cela dans un script d’initialisation, car cela réduit la sécurité SSL des serveurs.

<a id="entry-3-dw"></a>

**`-dW`**

```haproxy
-dW
```

Si défini, HAProxy refusera de démarrer si un avertissement a été émis lors du traitement de la configuration.
Cela permet de détecter des erreurs subtiles et de maintenir la configuration propre et portable entre les versions.
Il est recommandé de définir cette option dans les scripts de service lorsque les configurations sont gérées par des humains, mais il est recommandé de ne pas l'utiliser avec des configurations générées, qui ont tendance à émettre plus d'avertissements.
Elle peut être combinée avec "-c" pour faire échouer les configurations vérifiées en cas d'avertissement. Cela équivaut à l'option globale "zero-warning".

<a id="entry-3-dz"></a>

**`-dZ`**

```haproxy
-dZ
```

désactive le transfert des données en mode « zero-copy ». Cela équivaut à la directive "tune.disable-zero-copy-forwarding" de la section « global ». Cela peut être utile en cas de problèmes de perte de données ou d'intégrité des données, ou lors de l'utilisation de strace pour observer les données transférées, car cela désactive également le splice TCP du noyau.

<a id="entry-3-db"></a>

**`-db`**

```haproxy
-db
```

Désactivez le mode en arrière-plan et le mode multi-processus. Le processus reste en premier plan. Ce paramètre est principalement utilisé pendant le développement ou lors de petits tests, car l’envoi de Ctrl-C suffit à arrêter le processus. Ne l’utilisez jamais dans un script d’initialisation.

<a id="entry-3-dc"></a>

**`-dc`**

```haproxy
-dc
```

Activer le débogage de l'affinité CPU. La liste des CPUs sélectionnés et évacués ainsi que leur topologie seront rapportées avant le démarrage.

<a id="entry-3-de"></a>

**`-de`**

```haproxy
-de
```

désactive l'utilisation du poller « epoll ». Cela équivaut à la directive « noepoll » de la section « global ».
Il est principalement utile lorsque l'on suspecte un bug lié à ce poller. Sur les systèmes prenant en charge epoll, le mécanisme de secours sera généralement le poller « poll ».

<a id="entry-3-dk"></a>

**`-dk`**

```haproxy
-dk
```

désactive l'utilisation du poller « kqueue ». Cela équivaut à la directive « nokqueue » de la section « global ». Cela est principalement utile lorsqu'un bug lié à ce poller est suspecté. Sur les systèmes prenant en charge kqueue, le mécanisme de secours sera généralement le poller « poll ».

<a id="entry-3-dp"></a>

**`-dp`**

```haproxy
-dp
```

désactive l'utilisation du poller « poll ». Cela équivaut à la directive « nopoll » de la section « global ».
Il est principalement utile lorsque l'on suspecte un bogue lié à ce poller. Sur les systèmes prenant en charge poll, le mécanisme de secours sera généralement le poller « select », qui ne peut pas être désactivé et est limité à 1024 descripteurs de fichiers.

<a id="entry-3-dr-2"></a>

**`-dr`**

```haproxy
-dr
```

ignorer les échecs de résolution d'adresse du serveur. Il est fréquent, lors de la validation d'une configuration en dehors d'un environnement de production, de ne pas avoir accès aux mêmes résolveurs, ce qui entraîne l'échec de la résolution d'adresse du serveur, rendant ainsi difficile le test d'une configuration. Cette option ajoute simplement la méthode « none » à la liste des méthodes de résolution d'adresse pour tous les serveurs, garantissant que, même si la bibliothèque libc échoue à résoudre une adresse, la séquence de démarrage n'est pas interrompue.

<a id="entry-3-dt-2"></a>

**`-dt [<trace_desc>,...]`**

```haproxy
-dt [<trace_desc>,...]
```

active les traces sur stderr. Sans argument, cela active toutes les sources de trace au niveau d'erreur. Cela peut notamment être utile pour détecter des violations de protocole provenant de clients ou de serveurs. Un argument facultatif peut être utilisé pour spécifier une liste de configurations de trace différentes, séparées par une virgule. Chaque élément active une ou toutes les sources de trace. En outre, le niveau et la verbosité peuvent être spécifiés de manière facultative pour chaque élément en utilisant deux-points comme séparateur interne avec le nom de la trace. En cas d'entrée d'une verbosité ou d'un nom de niveau invalide, la liste des mots-clés disponibles est affichée. Par exemple, il peut être pratique de passer « help » pour chaque champ afin de consulter la liste en premier.

<a id="entry-3-dv-2"></a>

**`-dv`**

```haproxy
-dv
```

désactive l'utilisation du poller « evports ». Cela équivaut à la directive « noevports » de la section « global ». Cela est principalement utile lorsque l'on soupçonne un bogue lié à ce poller. Sur les systèmes prenant en charge les event ports (SunOS dérivé de Solaris 10 et ultérieur), le mécanisme de secours sera généralement le poller « poll ».

<a id="entry-3-m"></a>

**`-m <limit>`**

```haproxy
-m <limit>
```

limite la mémoire allouable, utilisée pour stocker les données du processus, à `<limit>` mégaoctets. Cela peut entraîner des refus de connexion ou des ralentissements, selon la quantité de mémoire nécessaire pour les opérations normales. Cette option est principalement utilisée pour forcer le processus HAProxy à fonctionner dans un scénario de consommation de ressources contrainte. Il est important de noter que la mémoire n'est pas partagée entre les processus haproxy, et un processus fils créé via l'appel système fork() hérite des limites de ressources de son processus parent. Ainsi, en mode master-worker, cette limite de mémoire est appliquée séparément au master et à son processus worker forké.

<a id="entry-3-n-2"></a>

**`-n <limit>`**

```haproxy
-n <limit>
```

limite la limite de connexions par processus à `<limit>`. Cela équivaut à la directive « maxconn » de la section globale. Elle a une priorité supérieure à cette directive. Cela peut être utilisé pour imposer rapidement des limites inférieures afin d'éviter une interruption de service sur des systèmes où les limites de ressources sont trop faibles.

<a id="entry-3-p"></a>

**`-p <file>`**

```haproxy
-p <file>
```

Écrivez les PID de tous les processus dans `<file>` au démarrage. Cela équivaut à la directive "pidfile" de la section "global". Le fichier est ouvert avant d'entrer dans la jail chroot, et après avoir exécuté le chdir() implicite par "-C". Chaque PID apparaît sur une ligne distincte.

<a id="entry-3-q"></a>

**`-q`**

```haproxy
-q
```

activer le mode « quiet ». Cela désactive les messages de sortie. Peut être utilisé en combinaison avec "-c" pour vérifier uniquement si un fichier de configuration est valide ou non.

<a id="entry-3-s"></a>

**`-S <bind>[,bind_options...]`**

```haproxy
-S <bind>[,bind_options...]
```

En mode master-worker, liez une interface CLI maître, qui permet l'accès à tous les processus, qu'ils soient en cours d'exécution ou en cours de terminaison. Pour des raisons de sécurité, il est recommandé de lier l'interface CLI maître à une socket UNIX locale. Les options de liaison sont les mêmes que le mot-clé « bind » dans le fichier de configuration, avec les mots séparés par des virgules au lieu d'espaces.

Notez que ce socket ne peut pas être utilisé pour récupérer les sockets d'écoute d'un ancien processus lors d'un rechargement sans interruption.

<a id="entry-3-sf"></a>

**`-sf <pid>*`**

```haproxy
-sf <pid>*
```

envoyer le signal « finish » (SIGUSR1) aux processus anciens après la fin du démarrage, afin de leur demander de terminer leur traitement et de quitter. `<pid>` est une liste d'identifiants de processus à signaler (un par argument). La liste se termine à la première option commençant par un « - ». Il n'est pas problématique que la liste des identifiants de processus soit vide, de sorte qu'elle puisse être construite dynamiquement à partir du résultat d'une commande comme « pidof » ou « pgrep ».

<a id="entry-3-st"></a>

**`-st <pid>*`**

```haproxy
-st <pid>*
```

envoyer le signal « terminate » (SIGTERM) aux processus anciens après la fin du démarrage pour les interrompre immédiatement sans terminer ce qu’ils étaient en train de faire. `<pid>` est une liste d’identifiants de processus à signaler (un par argument). La liste se termine à tout argument commençant par un « - ». Il n’est pas problématique que la liste des identifiants de processus soit vide, de sorte qu’elle puisse être construite dynamiquement à partir du résultat d’une commande comme « pidof » ou « pgrep ».

<a id="entry-3-v-2"></a>

**`-v`**

```haproxy
-v
```

Indiquez la version et la date de compilation.

<a id="entry-3-vv"></a>

**`-vv`**

```haproxy
-vv
```

affiche la version, les options de compilation, les versions des bibliothèques et les pollers disponibles. Cette sortie est systématiquement demandée lors de la soumission d'un rapport de bug.

<a id="entry-3-x"></a>

**`-x <unix_socket>`**

```haproxy
-x <unix_socket>
```

se connecter au socket spécifié et essayer de récupérer les sockets d'écoute de l'ancien processus, puis les utiliser à la place de tenter de lier de nouveaux sockets. Cela est utile pour éviter de manquer toute nouvelle connexion lors du rechargement de la configuration sous Linux.

Sans mode master-worker, la fonctionnalité doit être activée sur le socket de statistiques en utilisant « expose-fd listeners » dans votre configuration.

En mode master-worker, il n'est pas nécessaire d'utiliser « expose-fd listeners », le master utilisera automatiquement cette option lors d'un rechargement avec la syntaxe « sockpair@ », ce qui permet au master de se connecter directement à un worker sans avoir recours à une socket de statistiques déclarée dans la configuration. Si vous souhaitez désactiver cette fonctionnalité, vous pouvez passer -x /dev/null.

Une manière sûre de lancer HAProxy à partir d’un fichier d’initialisation consiste à forcer le mode démon, à stocker les PID existants dans un fichier de PID, puis à utiliser ce fichier pour avertir les processus anciens de se terminer avant de quitter :

```text
haproxy -f /etc/haproxy.cfg \
        -D -p /var/run/haproxy.pid -sf $(cat /var/run/haproxy.pid)
```

Lorsque la configuration est répartie entre plusieurs fichiers spécifiques (par exemple : tcp versus http), il est recommandé d'utiliser l'option "-f" :

```text
haproxy -f /etc/haproxy/global.cfg -f /etc/haproxy/stats.cfg \
        -f /etc/haproxy/default-tcp.cfg -f /etc/haproxy/tcp.cfg \
        -f /etc/haproxy/default-http.cfg -f /etc/haproxy/http.cfg \
        -D -p /var/run/haproxy.pid -sf $(cat /var/run/haproxy.pid)
```

Lorsqu’un nombre inconnu de fichiers est attendu, par exemple des fichiers spécifiques à un client, il est recommandé de leur attribuer un nom commençant par un numéro de séquence de taille fixe, puis de les charger à l’aide de "--", éventuellement après avoir chargé certains paramètres par défaut :

```text
haproxy -f /etc/haproxy/global.cfg -f /etc/haproxy/stats.cfg \
        -f /etc/haproxy/default-tcp.cfg -f /etc/haproxy/tcp.cfg \
        -f /etc/haproxy/default-http.cfg -f /etc/haproxy/http.cfg \
        -D -p /var/run/haproxy.pid -sf $(cat /var/run/haproxy.pid) \
        -f /etc/haproxy/default-customers.cfg -- /etc/haproxy/customers/*
```

Parfois, une erreur de démarrage peut survenir pour une raison quelconque. Il est alors important de vérifier que la version d'HAProxy que vous lancez est bien celle attendue et qu'elle prend en charge les fonctionnalités que vous attendez (par exemple : SSL, PCRE, compression, Lua, etc.). Cette vérification peut être effectuée à l’aide de la commande « haproxy -vv ». Certains éléments importants, tels que certaines options de compilation, le système cible et les versions des bibliothèques utilisées, y sont indiqués. C’est également ce que vous serez systématiquement invité à fournir lors de la soumission d’un rapport de bug :

```shell
$ haproxy -vv
```

HAProxy version 1.6-dev7-a088d3-4 2015/10/08 Copyright 2000-2015 Willy Tarreau <willy@haproxy.org>

Build options:

```text
TARGET  = linux2628
CPU     = generic
CC      = gcc
CFLAGS  = -pg -O0 -g -fno-strict-aliasing -Wdeclaration-after-statement \
          -DBUFSIZE=8030 -DMAXREWRITE=1030 -DSO_MARK=36 -DTCP_REPAIR=19
OPTIONS = USE_ZLIB=1 USE_DLMALLOC=1 USE_OPENSSL=1 USE_LUA=1 USE_PCRE=1
```

Default settings:

```text
maxconn = 2000, bufsize = 8030, maxrewrite = 1030, maxpollevents = 200
```

Encrypted password support via crypt(3): yes Built with zlib version: 1.2.6 Compression algorithms
supported: identity("identity"), deflate("deflate"), &#92;
raw-deflate("deflate"), gzip("gzip") Built with OpenSSL version: OpenSSL 1.0.1o 12 Jun 2015 Running
on OpenSSL version: OpenSSL 1.0.1o 12 Jun 2015 OpenSSL library supports TLS extensions: yes OpenSSL
library supports SNI: yes OpenSSL library supports prefer-server-ciphers: yes Built with PCRE
version: 8.12 2011-01-15 PCRE library supports JIT: no (USE_PCRE_JIT not set) Built with Lua
version: Lua 5.3.1 Built with transparent proxy support using: IP_TRANSPARENT IP_FREEBIND

Available polling systems:

```text
 epoll: pref=300,  test result OK
  poll: pref=200,  test result OK
select: pref=150,  test result OK
```

Total: 3 (3 usable), will use epoll.

Les informations pertinentes que de nombreux utilisateurs non développeurs peuvent vérifier ici sont :
<a id="entry-3-the-version"></a>

**`- la version`**

```haproxy
- la version
```

1.6-dev7-a088d3-4 signifie que le code est actuellement au commit ID « a088d3 », qui est le 4e après la version officielle "1.6-dev7". La version 1.6-dev7 s'afficherait sous la forme "1.6-dev7-8c1ad7". Ce qui compte ici, c'est en réalité "1.6-dev7". Il s'agit de la 7e version de développement de ce qui deviendra ultérieurement la version 1.6. Une version de développement non adaptée à une utilisation en production (sauf si vous savez exactement ce que vous faites). Une version stable s'affiche sous la forme d'une version à trois nombres, comme "1.5.14-16f863", indiquant le 14e correctif appliqué sur la version 1.5. Il s'agit d'une version prête à être utilisée en production.

<a id="entry-3-the-release-date"></a>

**`- la date de publication`**

```haproxy
- la date de publication
```

2015/10/08. Il est représenté au format universel année/mois/jour. Ici, cela signifie le 8 octobre 2015. Étant donné que les versions stables sont publiées tous les quelques mois (1 à 2 mois au début, parfois 6 mois une fois le produit très stable), si vous voyez une date ancienne ici, cela signifie probablement que vous êtes touché par un certain nombre de bogues ou de problèmes de sécurité qui ont depuis été corrigés, et qu’il pourrait être utile de vérifier le site officiel.

<a id="entry-3-build-options"></a>

**`- les options de compilation`**

```haproxy
- les options de compilation
```

Ils concernent les personnes qui construisent elles-mêmes leurs paquets ; ils peuvent expliquer pourquoi certaines fonctionnalités ne se comportent pas comme prévu. Par exemple, la version de développement ci-dessus a été compilée pour Linux 2.6.28 ou ultérieur, ciblant un processeur générique (sans optimisations spécifiques au processeur), et ne contient aucune optimisation de code (-O0), ce qui entraîne une performance médiocre.

<a id="entry-3-libraries-versions"></a>

**`- les versions des bibliothèques`**

```haproxy
- les versions des bibliothèques
```

La version de zlib est indiquée comme étant présente dans la bibliothèque elle-même. En général, zlib est considéré comme un produit très stable et les mises à jour ne sont presque jamais nécessaires. OpenSSL indique deux versions : celle utilisée au moment de la compilation et celle actuellement utilisée, telle qu'elle est présente sur le système. Ces versions peuvent différer uniquement par la dernière lettre, mais jamais par les chiffres. La date de compilation est également indiquée, car la plupart des bugs d'OpenSSL sont liés à la sécurité et doivent être pris au sérieux ; cette bibliothèque doit donc absolument être tenue à jour. Voir une version âgée de quatre mois est hautement suspect, et en effet, une mise à jour a été manquée. PCRE fournit des expressions régulières très rapides et est fortement recommandé. Certaines de ses extensions, comme le JIT, ne sont pas présentes dans toutes les versions et restent encore jeunes, si bien que certaines personnes préfèrent ne pas les activer lors de la compilation, ce qui explique pourquoi l'état de compilation est également indiqué. En ce qui concerne le langage de script Lua, HAProxy attend la version 5.3, qui est très récente, étant sortie peu avant HAProxy 1.6. Il est important de vérifier sur le site web de Lua si des correctifs sont proposés pour cette branche.

<a id="entry-3-available-polling-systems"></a>

**`- Les mécanismes de scrutation disponibles influent sur la capacité de montée en charge du processus lorsque`**

```haproxy
- Les mécanismes de scrutation disponibles influent sur la capacité de montée en charge du processus lorsque
```

gestion de plus d'environ mille connexions simultanées. Ces mécanismes ne sont disponibles que lorsque le système approprié a été indiqué dans la variable TARGET lors de la compilation. Le mécanisme « epoll » est fortement recommandé sous Linux, et le mécanisme « kqueue » est fortement recommandé sous BSD. En leur absence, la fonction poll() ou même select() sera utilisée, entraînant une utilisation élevée du CPU lors de la gestion d'un grand nombre de connexions.
