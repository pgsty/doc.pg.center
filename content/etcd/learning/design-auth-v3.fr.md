---
title: "etcd conception de l'authentification v3"
weight: 2500
description: etcd authentification v3
categories: [Concept]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/learning/design-auth-v3.md"
---

## Pourquoi ne pas réutiliser le système d'authentification v2 ? {#why-not-reuse-the-v2-auth-system}

Le protocole v3 utilise gRPC comme transport, à la place d'une interface RESTful comme dans la v2. Ce nouveau protocole offre l'opportunité d'améliorer et d'évoluer la conception de la v2. Par exemple, l'authentification v3 repose sur une authentification basée sur la connexion, contrairement à l'authentification par requête plus lente de la v2. En outre, les sémantiques de l'authentification v2 s'avèrent souvent peu pratiques en pratique lorsqu'il s'agit d'assurer la cohérence, ce qui sera expliqué dans les sections suivantes. Pour la v3, une description et une implémentation clairement définies du mécanisme d'authentification corrigent les déficiences du système d'authentification v2.

### Exigences fonctionnelles {#functionality-requirements}

* Authentification par connexion, pas par requête
   * Authentification basée sur l'identifiant utilisateur et le mot de passe implémentée pour l'API gRPC
   * L'authentification doit être actualisée après tout changement de stratégie d'authentification
* Sa fonctionnalité doit être aussi simple et utile que celle de la version v2
   * La version v3 propose un espace de clés plat, contrairement à la structure hiérarchique de la version v2. La vérification des autorisations sera assurée par correspondance d'intervalle.
* Elle doit offrir des garanties de cohérence plus fortes que celles de la version v2 pour l'authentification

### Modifications principales requises {#main-required-changes}

* Un client doit établir une connexion dédiée uniquement à l'authentification avant d'envoyer des requêtes authentifiées
* Ajouter les informations de permission (identifiant utilisateur et révision autorisée) aux commandes Raft (`etcdserverpb.InternalRaftRequest`)
* Chaque requête est vérifiée pour les autorisations au niveau de la couche machine d'état, plutôt qu'au niveau de l'API

### Consistance des métadonnées de permission {#permission-metadata-consistency}

Les métadonnées relatives à l’authentification doivent également être stockées et gérées dans le stockage contrôlé par le protocole Raft d’etcd, comme les autres données stockées dans etcd. Cela est nécessaire pour ne pas compromettre la disponibilité et la cohérence de l’ensemble du cluster. Si la lecture ou l’écriture des métadonnées (par exemple, les informations de permission) nécessitait l’accord de chaque nœud (plus qu’un quorum), la défaillance d’un seul nœud pourrait bloquer l’ensemble du cluster. Exiger l’accord de tous les nœuds simultanément signifie que la vérification des requêtes ordinaires read/write ne peut pas être accomplie si un membre du cluster est hors ligne, même si le cluster dispose d’un quorum disponible. Ce schéma unanime dégrade finalement la disponibilité du cluster ; un consensus basé sur le quorum issu de Raft suffit, car l’accord découle d’un ordre cohérent.

Le mécanisme d'authentification dans le protocole etcd v2 comporte une difficulté car la cohérence des métadonnées devrait fonctionner comme indiqué ci-dessus, mais ne fonctionne pas : chaque vérification de permission est traitée par le membre etcd qui reçoit la requête cliente (server/etcdserver/api/v2http/client.go), y compris les membres suiveurs. Il est donc possible que la vérification soit basée sur des métadonnées obsolètes.


Ce délai signifie qu'une modification de configuration d'authentification ne peut pas être immédiatement reflétée après l'exécution de la commande etcdctl. Il n'existe donc aucun moyen de savoir pendant combien de temps les métadonnées obsolètes restent actives. En pratique, le changement de configuration est immédiatement pris en compte après l'exécution de la commande. Toutefois, dans certains cas de forte charge, l'état incohérent peut être prolongé, ce qui peut entraîner des situations contre-intuitives pour les utilisateurs et les développeurs. Une solution de contournement est nécessaire, comme [this](https://github.com/etcd-io/etcd/pull/4317#issuecomment-179037582).

### Des permissions incohérentes sont dangereuses pour les requêtes linéarisées {#inconsistent-permissions-are-unsafe-for-linearized-requests}

Un état d'authentification incohérent est particulièrement critique pour les écritures. Même si un opérateur désactive les écritures pour un utilisateur, si l'écriture n'est ordonnée qu'au regard du magasin clé-valeur et non du système d'authentification, il est possible que l'écriture aboutisse avec succès. Sans ordonnancement simultané sur le magasin d'authentification et le magasin clé-valeur, le système sera vulnérable aux attaques par permission obsolète.

Par conséquent, la logique de vérification des autorisations doit être ajoutée à la machine d’état d’etcd. Chaque machine d’état doit vérifier les requêtes en fonction de ses informations d’autorisation lors de l’étape apply (de sorte que les informations d’authentification ne soient pas périmées).

## Conception et mise en œuvre {#design-and-implementation}

### Authentification {#authentication}

Au départ, un client doit établir une connexion gRPC uniquement pour authentifier son identifiant utilisateur et son mot de passe. Un serveur etcd répondra par une réponse d’authentification. Cette réponse sera un jeton d’authentification en cas de succès, ou une erreur en cas d’échec. Le client peut utiliser son jeton d’authentification pour présenter ses identifiants à etcd lors de requêtes API.

La connexion cliente utilisée pour demander le jeton d'authentification est généralement abandonnée ; elle ne peut pas transporter les informations d'authentification du nouveau jeton. Cela est dû au fait que gRPC ne permet pas d'ajouter des informations d'authentification par appel RPC après la création de la connexion (appel à `grpc.Dial()`). Par conséquent, un client ne peut pas attribuer un jeton à sa connexion s'il l'obtient via cette connexion. Le client doit établir une nouvelle connexion pour utiliser le jeton.

#### Notes sur l'implémentation de l'appel RPC `Authenticate()` {#notes-on-the-implementation-of-authenticate-rpc}

`Authenticate()` génère un jeton d'authentification à partir d'un nom d'utilisateur et d'un mot de passe fournis. etcd enregistre et vérifie un mot de passe configuré et un mot de passe fourni à l'aide du package `bcrypt` de Go. Par conception, le mécanisme de vérification des mots de passe de `bcrypt` est coûteux en termes de calcul, nécessitant près de 100 ms sur un serveur x64 ordinaire. Par conséquent, effectuer cette vérification dans la phase apply de la machine d'état entraînerait des problèmes de performance : le cluster etcd ne pourrait servir qu'approximativement 10 `Authenticate()` requêtes par seconde.

Pour des performances optimales, le mécanisme d’authentification v3 vérifie les mots de passe au niveau de l’API etcd, où cette vérification peut être parallélisée en dehors de raft. Toutefois, cela peut entraîner des failles potentielles de permission time-of-check/time-of-use (TOCTOU) :
1. le client A envoie une requête `Authenticate()`
1. le niveau de l’API traite la partie de vérification du mot de passe de `Authenticate()`
1. un autre client B envoie une requête de `ChangePassword()` et le serveur la traite
1. le niveau de la machine d’état traite la partie obtenir un numéro de révision pour le `Authenticate()` provenant de A
1. le serveur retourne un succès au client A
1. le client A est désormais authentifié avec un mot de passe obsolète

Pour éviter une telle situation, la couche API effectue une *vérification du numéro de version* basée sur le numéro de révision du magasin d’authentification. Lors de la vérification du mot de passe, la couche API enregistre le numéro de révision du magasin d’authentification. Après une vérification réussie du mot de passe, la couche API compare le numéro de révision enregistré avec le numéro de révision le plus récent. Si les numéros diffèrent, cela signifie qu’un autre utilisateur a mis à jour les métadonnées d’authentification. Dans ce cas, elle réessaie la vérification. Grâce à ce mécanisme, la vérification réussie du mot de passe basée sur un mot de passe obsolète peut être évitée.

### Résolution d'un jeton au niveau de l'API {#resolving-a-token-in-the-api-layer}

Après s'être authentifié avec `Authenticate()`, un client peut établir une connexion gRPC comme il le ferait sans authentification. En plus du processus d'initialisation existant, le client doit associer le jeton à la connexion nouvellement créée. `grpc.WithPerRPCCredentials()` fournit la fonctionnalité nécessaire à cette opération.

Chaque requête authentifiée provenant du client dispose d'un jeton. Ce jeton peut être obtenu avec `grpc.metadata.FromIncomingContext()` côté serveur. Le serveur peut déterminer qui émet la requête et à quel moment l'utilisateur a été autorisé. Ces informations seront renseignées par la couche API dans l'en-tête (`etcdserverpb.RequestHeader.Username` et `etcdserverpb.RequestHeader.AuthRevision`) d'une entrée de journal Raft (`etcdserverpb.InternalRaftRequest`).

### Vérification de la permission dans la machine à états {#checking-permission-in-the-state-machine}

Les informations d'authentification dans `etcdserverpb.RequestHeader` sont vérifiées lors de l'étape d'application de la machine à états. Cette étape vérifie que l'utilisateur dispose des autorisations nécessaires pour accéder aux clés demandées, selon la dernière révision du magasin d'authentification.

### Deux types de jetons : simples et JWT {#two-types-of-tokens-simple-and-jwt}

Il existe deux types de jetons : simples et JWT. Le jeton simple n'est pas conçu pour les cas d'utilisation en production. Ses jetons ne sont pas signés cryptographiquement, et les serveurs doivent suivre de manière étatique la correspondance entre jetons et utilisateurs ; il est destiné à des tests en développement. Les jetons JWT doivent être utilisés pour les déploiements en production, car ils sont signés et vérifiés cryptographiquement. Du point de vue de l'implémentation, le JWT est sans état. Son jeton peut inclure des métadonnées, notamment le nom d'utilisateur et la révision, de sorte que les serveurs n'aient pas à mémoriser la correspondance entre les jetons et les métadonnées.

> [!WARNING]
> Un problème connu[#18437](https://github.com/etcd-io/etcd/issues/18437) concerne les jetons simples. Dans les serveurs etcd, les jetons sont résolus au niveau de l'API et les jetons simples sont étatiques. Ce processus n'est pas protégé par une vérification linéarisable, ce qui signifie qu'un membre etcd peut ne pas avoir terminé le traitement d'une requête d'authentification précédente avant de recevoir la suivante. Dans de tels cas, le membre peut renvoyer une erreur « jeton d'authentification invalide » au client. Ce problème est généralement rare sur un nœud disposant de conditions réseau favorables, mais peut survenir en cas de latence importante. En tant que contournement, les applications peuvent implémenter un mécanisme de nouvelle tentative pour gérer cette erreur.

### Définition directe des jetons JWT {#directly-setting-jwt-tokens}

En plus du flux RPC standard `Authenticate()`, etcd prend en charge la définition de jetons JWT directement au niveau du client. Cela permet aux applications de gérer l'intégralité du cycle de vie des jetons JWT en dehors d'etcd, y compris la génération, la validation et le renouvellement.

#### Cas d'utilisation et flux de travail {#use-case-and-workflow}

Cette approche est utile lorsque :

* Un système de gestion des jetons indépendant (en dehors d'etcd) gère la génération et le cycle de vie des jetons JWT
* Les applications reçoivent des jetons JWT pré-signés via un mécanisme externe (par exemple, des variables d'environnement, un service de configuration)
* Le cycle de vie des jetons doit être géré entièrement par l'application cliente et non par la génération automatique de jetons d'etcd

Le flux de travail typique est :

1.  Une autorité externe (non etcd) génère un jeton JWT signé qui inclut le nom d'utilisateur et d'autres revendications
2.  L'application reçoit le jeton pré-signé et configure le client etcd avec celui-ci
3.  Le client soumet le jeton JWT directement avec les requêtes (sans appeler `Authenticate()`)
4.  Le serveur etcd valide la signature du jeton à l'aide de sa clé publique configurée et accorde l'accès en fonction du nom d'utilisateur contenu dans le jeton
5.  Avant l'expiration du jeton, l'application obtient un nouveau jeton auprès de l'autorité externe
6.  L'application crée un nouveau client avec le jeton mis à jour (la mise à jour du jeton nécessite la recréation du client)

#### Comment il diffère de l'authentification standard {#how-it-differs-from-standard-authentication}

Lors de l'utilisation du flux standard `Authenticate()` :

* Le client appelle `Authenticate()` avec le nom d'utilisateur et le mot de passe
* etcd génère et renvoie un jeton
* Le client utilise automatiquement ce jeton pour les requêtes ultérieures
* La mise à jour du jeton nécessite d'appeler à nouveau `Authenticate()`

Lorsque les jetons JWT sont définis directement :

* Le client est initialisé avec un jeton JWT pré-signé
* Le client **ne** fait pas appel à `Authenticate()`
* Le jeton est utilisé directement dans toutes les requêtes
* L'application cliente est responsable d'obtenir de nouveaux jetons avant l'expiration et de gérer le cycle de vie du client

#### AuthStatus sans jeton valide {#authstatus-without-valid-token}

Pour prendre en charge les applications qui gèrent elles-mêmes leurs jetons JWT, l’API RPC `AuthStatus` a été conçue afin de permettre aux clients de déterminer si l’authentification est activée et de récupérer la révision actuelle de `authRevision`. Cela est essentiel dans les scénarios de récupération où un jeton a expiré et où le client a besoin de la dernière révision afin d’obtenir un nouveau jeton valide auprès de son fournisseur externe de jetons.

Sans cette fonctionnalité, un jeton expiré pourrait empêcher un client d'accéder au `authRevision` actuel, entraînant un blocage dans lequel aucun nouveau jeton ne peut être généré.

## Remarques sur la différence entre les modèles KVS et les modèles de système de fichiers {#notes-on-the-difference-between-kvs-models-and-file-system-models}

etcd v3 est un système de stockage clé-valeur (KVS), et non un système de fichiers. Les autorisations peuvent donc être attribuées aux utilisateurs sous la forme d’un nom de clé exact ou d’une plage de clés, comme `["start key", "end key")`. Cela signifie qu’il est possible d’accorder des autorisations pour une clé inexistante. Les utilisateurs doivent veiller à ne pas accorder involontairement des autorisations. Dans un système similaire à un système de fichiers (par exemple Chubby ou ZooKeeper), une structure de données analogue à un inode peut contenir les informations d’autorisation. Il n’est alors pas possible d’accorder une autorisation à une clé inexistante (à l’exception du cas des bits sticky).

Le modèle etcd v3 nécessite plusieurs recherches de métadonnées, contrairement aux systèmes de fichiers. Le coût maximal de recherche correspond à la somme des clés et intervalles accordés par l'utilisateur. Ce coût ne peut être évité, car l'espace de clés plat du v3 diffère entièrement du modèle de système de fichiers Unix (où chaque inode inclut des métadonnées de permissions). En pratique, ce coût ne pose pas de problème sérieux, car les métadonnées sont suffisamment petites pour bénéficier du cache.
