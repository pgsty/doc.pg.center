---
title: etcd API
weight: 2625
description: "Aperçu de la conception de l’API etcd"
categories: [Concept]
upstream_link: "https://github.com/etcd-io/website/blob/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7/learning/api.md"
---

Ce document a pour objectif de présenter une vue d'ensemble des principes fondamentaux de l'API v3 d'etcd.
Il ne devrait pas être confondu avec l'API etcd v2, dépréciée à partir d'etcd v3.5.
Il ne prétend pas être exhaustif, mais vise à se concentrer sur les idées de base nécessaires à la compréhension d'etcd, sans les distractions des appels d'API moins courants.
Toutes les API etcd sont définies dans des services [gRPC][grpc-service], qui catégorisent les appels de procédure distante (RPC) compris par le serveur etcd.
Une liste complète de toutes les RPC etcd est documentée au format markdown dans le [listing des API gRPC][grpc-api].

## Services gRPC {#grpc-services}

Chaque requête d'API envoyée à un serveur etcd est un appel de procédure à distance gRPC. Les appels RPC dans etcd sont catégorisés selon leur fonctionnalité en services.

Les services importants pour la gestion de l'espace de clés d'etcd incluent :

* KV - Crée, met à jour, récupère et supprime des paires clé-valeur.
* Watch - Surveille les modifications apportées aux clés.
* Lease - Primitives pour consommer les messages de maintien de connexion client.

Les services qui gèrent le cluster lui-même incluent :

* Auth - Mécanisme d'authentification basé sur les rôles pour authentifier les utilisateurs.
* Cluster - Fournit des informations sur les membres et des fonctionnalités de configuration.
* Maintenance - Prend des instantanés de récupération, défragmente le magasin et retourne des informations d'état par membre.

### Requêtes et réponses {#requests-and-responses}

Toutes les requêtes RPC dans etcd suivent le même format. Chaque RPC dispose d'une fonction `Name` qui prend `NameRequest` en argument et renvoie `NameResponse` en réponse. Par exemple, voici la description de la requête RPC `Range` :

```protobuf
service KV {
  Range(RangeRequest) returns (RangeResponse)
  ...
}
```

### En-tête de réponse {#response-header}

Toutes les réponses de l'API etcd incluent un en-tête de réponse qui contient des métadonnées du cluster pour la réponse :

```proto
message ResponseHeader {
  uint64 cluster_id = 1;
  uint64 member_id = 2;
  int64 revision = 3;
  uint64 raft_term = 4;
}
```

* `cluster_id` - l'identifiant du cluster générant la réponse.
* `member_id` - l'identifiant du membre générant la réponse.
* `revision` - la révision du magasin clé-valeur lors de la génération de la réponse.
* `raft_term` - le mandat Raft du membre lors de la génération de la réponse.

Une application peut lire le champ `cluster_id` ou `member_id` pour s'assurer qu'elle communique avec le cluster (membre) prévu.

Les applications peuvent utiliser le champ `revision` pour connaître la dernière révision du magasin clé-valeur. Cela est particulièrement utile lorsque les applications spécifient une révision historique afin d'effectuer une `time travel query` et souhaitent connaître la dernière révision au moment de la requête.

Les applications peuvent utiliser `raft_term` pour détecter quand le cluster termine une nouvelle élection de leader.

## API clé-valeur {#key-value-api}

L'API Clé-Valeur manipule des paires clé-valeur stockées dans etcd. La majorité des requêtes adressées à etcd sont généralement des requêtes clé-valeur.

### Primitives système {#system-primitives}

### Paire clé-valeur {#key-value-pair}

Une paire clé-valeur est l'unité minimale manipulable par l'API clé-valeur. Chaque paire clé-valeur possède un certain nombre de champs, définis au format [protobuf][kv-proto] :

```protobuf
message KeyValue {
  bytes key = 1;
  int64 create_revision = 2;
  int64 mod_revision = 3;
  int64 version = 4;
  bytes value = 5;
  int64 lease = 6;
}
```

* `key` - clé sous forme d'octets. Une clé vide n'est pas autorisée.
* `value` - valeur sous forme d'octets.
* `version` - version de la clé. Une suppression réinitialise la version à zéro, et toute modification de la clé augmente sa version.
* `create_revision` - révision de la dernière création sur la clé.
* `mod_revision` - révision de la dernière modification sur la clé.
* `lease` - identifiant du bail attaché à la clé. Si le bail est égal à zéro, aucun bail n'est attaché à la clé.


En plus de la clé et de sa valeur, etcd attache des métadonnées de révision supplémentaires au message de clé. Ces informations de révision ordonnent les clés selon leur date de création et de modification, ce qui est utile pour gérer la concurrence dans la synchronisation distribuée. Les [verrous partagés distribués][locks] du client etcd utilisent la révision de création pour attendre la possession du verrou. De même, la révision de modification est utilisée pour détecter les conflits sur l'ensemble de lecture de la [mémoire transactionnelle logicielle][STM] et attendre les mises à jour de l'[élection du leader][elections].

#### Révisions {#revisions}

etcd maintient un compteur 64 bits valable pour l’ensemble du cluster, appelé révision du magasin, qui est incrémenté à chaque modification de l’espace de clés. La révision sert d’horloge logique globale, ordonnant séquentiellement toutes les mises à jour du magasin. Le changement représenté par une nouvelle révision est incrémental ; les données associées à une révision sont celles qui ont modifié le magasin. En interne, une nouvelle révision signifie écrire les modifications dans l’arbre B+ du backend, indexées par la révision incrémentée.

Les révisions prennent davantage de valeur lorsqu’on considère le backend [contrôle de concurrence à plusieurs versions][mvcc] d’etcd. Le modèle MVCC signifie que le magasin clé-valeur peut être consulté à partir de révisions passées, car les anciennes révisions des clés sont conservées. La politique de conservation de cet historique peut être configurée par les administrateurs du cluster afin de gérer finement le stockage ; en général, etcd supprime les anciennes révisions des clés selon un horaire. Un cluster etcd typique conserve les données obsolètes des clés pendant plusieurs heures. Cela permet également une gestion fiable des déconnexions longues des clients, et non seulement des perturbations réseau transitoires : les observateurs reprennent simplement à partir de la dernière révision historique observée. De même, pour lire dans le magasin à un instant précis, les requêtes de lecture peuvent être étiquetées avec une révision afin de retourner les clés selon une vue de l’espace des clés au moment où cette révision a été validée.

#### Plages de clés {#key-ranges}

Le modèle de données etcd indexe toutes les clés dans un espace binaire plat. Cela diffère des autres systèmes de magasin clé-valeur qui organisent les clés selon une structure hiérarchique en répertoires. Au lieu de lister les clés par répertoire, les clés sont listées par intervalles de clés `[a, b)`.

Ces intervalles sont souvent appelés « plages » dans etcd. Les opérations sur les plages sont plus puissantes que les opérations sur les répertoires. Comme un magasin hiérarchique, les plages permettent les recherches par clé unique via `[a, a+1)` (par exemple, `['a', 'a\x00')` recherche `'a'`) et les recherches par répertoire en codant les clés selon leur profondeur dans l’arborescence. En plus de ces opérations, les plages peuvent également encoder des préfixes ; par exemple, la plage `['a', 'b')` recherche toutes les clés dont le préfixe est la chaîne 'a'.

Par convention, les plages pour une requête sont indiquées par les champs `key` et `range_end`. Le champ `key` est la première clé de la plage et doit être non vide. Le champ `range_end` est la clé suivant la dernière clé de la plage. Si `range_end` n’est pas fourni ou est vide, la plage est définie comme ne contenant que la clé fournie. Si `range_end` est égal à `key` plus un (par exemple, `"aa"+1 == "ab"`, `"a\xff"+1 == "b"`), alors la plage représente toutes les clés ayant pour préfixe la clé. Si les deux champs `key` et `range_end` sont égaux à `'\0'`, la plage représente toutes les clés. Si `range_end` est égal à `'\0'`, la plage correspond à toutes les clés supérieures ou égales à la clé fournie.

### Range {#range}

Les clés sont récupérées depuis le magasin clé-valeur à l’aide de l’appel d’API `Range`, qui prend un `RangeRequest` :

```protobuf
message RangeRequest {
  enum SortOrder {
	NONE = 0; // default, no sorting
	ASCEND = 1; // lowest target value first
	DESCEND = 2; // highest target value first
  }
  enum SortTarget {
	KEY = 0;
	VERSION = 1;
	CREATE = 2;
	MOD = 3;
	VALUE = 4;
  }

  bytes key = 1;
  bytes range_end = 2;
  int64 limit = 3;
  int64 revision = 4;
  SortOrder sort_order = 5;
  SortTarget sort_target = 6;
  bool serializable = 7;
  bool keys_only = 8;
  bool count_only = 9;
  int64 min_mod_revision = 10;
  int64 max_mod_revision = 11;
  int64 min_create_revision = 12;
  int64 max_create_revision = 13;
}
```

* `key`, `range_end` - Plage de clés à récupérer.
* `limit` - nombre maximal de clés retournées pour la requête. Si la limite est définie à 0, elle est traitée comme sans limite.
* `revision` - instantané du magasin clé-valeur à utiliser pour la plage. Si la révision est inférieure ou égale à zéro, la plage concerne l’état le plus récent du magasin clé-valeur. Si la révision est compactée, la réponse renvoie `ErrCompacted`.
* `sort_order` - ordre de tri pour les requêtes triées.
* `sort_target` - champ du magasin clé-valeur à trier.
* `serializable` - active les lectures sérialisables locales au membre pour la requête de plage. Par défaut, Range est linéarisable ; elle reflète le consensus actuel du cluster. Pour de meilleures performances et disponibilité, au prix de lectures potentiellement obsolètes, une requête de plage sérialisable est servie localement sans nécessiter de consensus avec les autres nœuds du cluster.
* `keys_only` - ne retourne que les clés, et non les valeurs.
* `count_only` - ne retourne que le nombre de clés dans la plage.
* `min_mod_revision` - borne inférieure des révisions de modification des clés renvoyées ; toutes les clés dont la révision de modification est inférieure sont filtrées.
* `max_mod_revision` - borne supérieure des révisions de modification des clés ; toutes les clés dont la révision de modification est supérieure sont filtrées.
* `min_create_revision` - borne inférieure des révisions de création des clés renvoyées ; toutes les clés dont la révision de création est inférieure sont filtrées.
* `max_create_revision` - borne supérieure des révisions de création des clés ; toutes les clés dont la révision de création est supérieure sont filtrées.

Le client reçoit un message `RangeResponse` de l'appel `Range` :

```protobuf
message RangeResponse {
  ResponseHeader header = 1;
  repeated mvccpb.KeyValue kvs = 2;
  bool more = 3;
  int64 count = 4;
}
```

* `kvs` - la liste des paires clé-valeur correspondant à la requête de plage. `kvs` est vide lorsque `count_only` est défini.
* `more` - indique s'il reste des clés à renvoyer dans la plage demandée.
* `count` - le nombre réel de clés dans la plage lorsque la requête le demande. Contrairement à `kvs`, il n'est affecté ni par les limites ni par les filtres (par ex. Min/Max, Create/Modify, Revisions) et reflète le nombre complet dans la plage spécifiée.

Pour les plages de clés importantes où le tamponnage de la réponse complète est indésirable, consultez [RangeStream](#rangestream).

### RangeStream {#rangestream}

`RangeStream` retourne le même jeu de résultats que `Range`, mais le serveur fractionne la réponse en une séquence de morceaux et la diffuse au client. Cela évite de stocker entièrement de grandes plages en mémoire côté serveur ou côté client. `RangeStream` accepte les mêmes `RangeRequest` que `Range`.

Le client reçoit un flux de messages `RangeStreamResponse` à partir de l'appel `RangeStream` :

```protobuf
message RangeStreamResponse {
  RangeResponse range_response = 1;
}
```

Remplissage des champs par morceaux :

* `kvs` - chaque morceau contient une tranche disjointe du résultat. En concaténant les `kvs` de chaque morceau dans l'ordre de leur arrivée, on obtient le même ensemble de clés qu'une unique requête `Range`.
* `header`, `more`, `count` - renseignés uniquement dans le dernier morceau, et uniquement lorsque le flux se termine sans erreur. Les morceaux précédents laissent ces champs à zéro. Appliquer `proto.Merge` sur le `range_response` de chaque morceau donne un `RangeResponse` équivalent à ce que `Range` aurait retourné.

Si le flux se termine avec une erreur, aucun morceau ne contient de `header`, `more` ou `count` valide.

Chaque morceau du flux est servi en référence à la même révision. Si la requête ne définit pas `Revision`, le serveur capture la dernière révision validée au moment du démarrage du flux et la réutilise pour le reste du flux.

`RangeStream` ne prend pas en charge les ordres de tri personnalisés ni les filtres de révision (`min_mod_revision`, `max_mod_revision`, `min_create_revision`, `max_create_revision`). Les requêtes utilisant l’un ou l’autre retournent `Unimplemented`. `RangeStream` n’est pas non plus pris en charge par le proxy gRPC etcd.

Il existe deux méthodes courantes pour consommer un `RangeStream` :

1. **Traitez chaque tranche indépendamment.** Adapté aux scénarios à haute performance où le client souhaite décoder et agir sur les clés au fur et à mesure de leur arrivée, plutôt que de collecter l’ensemble du résultat d’abord. Le client itère les tranches et traite `kvs` de chacune, puis lit `header`, `more` ou `count` de la dernière tranche après la fin propre du flux.
2. **Assemblez une seule réponse.** Adapté lorsque le client souhaite obtenir un résultat équivalent à une requête unaire `Range`. Le client fusionne chaque `range_response` de tranche en un seul `RangeResponse` (par exemple, à l’aide de `proto.Merge`). Le résultat fusionné contient l’intégralité de `kvs`, ainsi que `header`, `more` et `count` provenant de la dernière tranche. Le client Go fournit `clientv3.GetStreamToGetResponse` comme aide pour ce schéma.

### Put {#put}

Les clés sont stockées dans le magasin clé-valeur en émettant un appel à `Put`, qui prend un `PutRequest` :

```protobuf
message PutRequest {
  bytes key = 1;
  bytes value = 2;
  int64 lease = 3;
  bool prev_kv = 4;
  bool ignore_value = 5;
  bool ignore_lease = 6;
}
```

* `key` - le nom de la clé à insérer dans le magasin clé-valeur.
* `value` - la valeur, en octets, à associer à la clé dans le magasin clé-valeur.
* `lease` - l'identifiant de bail à associer à la clé dans le magasin clé-valeur. Une valeur de bail égale à 0 indique l'absence de bail.
* `prev_kv` - lorsque défini, etcd récupère la paire clé-valeur précédente avant de la modifier. La paire clé-valeur précédente est renvoyée dans la réponse du put.
* `ignore_value` - lorsque défini, met à jour la clé en utilisant sa valeur actuelle. Retourne une erreur si la clé n'existe pas.
* `ignore_lease` - lorsque défini, etcd met à jour la clé en utilisant son bail actuel. Retourne une erreur si la clé n'existe pas.

Le client reçoit un message `PutResponse` de l'appel `Put` :

```protobuf
message PutResponse {
  ResponseHeader header = 1;
  mvccpb.KeyValue prev_kv = 2;
}
```

* `prev_kv` - si `prev_kv` est défini dans la requête, la paire clé-valeur précédente est renvoyée.

### Supprimer une plage {#delete-range}

Les plages de clés sont supprimées à l'aide de l'appel `DeleteRange`, qui prend un `DeleteRangeRequest` :

```protobuf
message DeleteRangeRequest {
  bytes key = 1;
  bytes range_end = 2;
  bool prev_kv = 3;
}
```

* `key` - la première clé à supprimer dans la plage.
* `range_end` - la clé suivant la dernière clé à supprimer pour la plage `[key, range_end)`.

Le client reçoit un message `DeleteRangeResponse` de l'appel `DeleteRange` :

```protobuf
message DeleteRangeResponse {
  ResponseHeader header = 1;
  int64 deleted = 2;
  repeated mvccpb.KeyValue prev_kvs = 3;
}
```

* `deleted` - nombre de clés supprimées par la requête de suppression de plage.
* `prev_kvs` - les paires clé-valeur précédentes, renvoyées lorsque `prev_kv` est défini dans la requête.

### Transaction {#transaction}

Une transaction est une construction atomique If/Then/Else sur le magasin clé-valeur. Elle fournit une primitive pour regrouper des requêtes dans des blocs atomiques (c’est-à-dire then/else), dont l’exécution est protégée (c’est-à-dire if) en fonction du contenu du magasin clé-valeur. Les transactions peuvent être utilisées pour protéger les clés contre des mises à jour concurrentes non désirées, pour mettre en œuvre des opérations compare-and-swap, et pour développer des contrôles de concurrence de niveau supérieur.

Une transaction peut traiter atomiquement plusieurs requêtes en une seule requête. Pour les modifications du magasin clé-valeur, cela signifie que la révision du magasin n'est incrémentée qu'une seule fois pour la transaction, et que tous les événements générés par la transaction auront la même révision. Toutefois, les modifications apportées à la même clé plusieurs fois au sein d'une même transaction sont interdites.

Toutes les transactions sont protégées par une conjonction de comparaisons, similaire à une instruction `If`. Chaque comparaison vérifie une seule clé dans le magasin. Elle peut vérifier l'absence ou la présence d'une valeur, la comparer à une valeur donnée, ou vérifier la révision ou la version d'une clé. Deux comparaisons différentes peuvent s'appliquer à la même clé ou à des clés différentes. Toutes les comparaisons sont appliquées de manière atomique ; si toutes les comparaisons sont vraies, la transaction est considérée comme réussie et etcd applique le bloc de requête then / `success`, sinon elle est considérée comme échouée et applique le bloc de requête else / `failure`.

Chaque comparaison est encodée sous la forme d'un message `Compare` :

```protobuf
message Compare {
  enum CompareResult {
    EQUAL = 0;
    GREATER = 1;
    LESS = 2;
    NOT_EQUAL = 3;
  }
  enum CompareTarget {
    VERSION = 0;
    CREATE = 1;
    MOD = 2;
    VALUE= 3;
  }
  CompareResult result = 1;
  // target is the key-value field to inspect for the comparison.
  CompareTarget target = 2;
  // key is the subject key for the comparison operation.
  bytes key = 3;
  oneof target_union {
    int64 version = 4;
    int64 create_revision = 5;
    int64 mod_revision = 6;
    bytes value = 7;
  }
}
```

* `result` - le type d'opération de comparaison logique (par exemple, égal, inférieur à, etc.).
* `target` - le champ clé-valeur à comparer. Soit la version de la clé, la révision de création, la révision de modification ou la valeur.
* `key` - la clé pour la comparaison.
* `target_union` - les données spécifiées par l'utilisateur pour la comparaison.

Après le traitement du bloc de comparaison, la transaction applique un bloc de requêtes. Un bloc est une liste de messages `RequestOp` :

```protobuf
message RequestOp {
  // request is a union of request types accepted by a transaction.
  oneof request {
    RangeRequest request_range = 1;
    PutRequest request_put = 2;
    DeleteRangeRequest request_delete_range = 3;
  }
}
```

* `request_range` - une `RangeRequest`.
* `request_put` - une `PutRequest`. Les clés doivent être uniques. Elle ne peut pas partager de clés avec d'autres opérations Put ou Delete.
* `request_delete_range` - une `DeleteRangeRequest`. Elle ne peut pas partager de clés avec des requêtes Put ou Delete.

Ces éléments sont réunis dans une transaction émise par un appel API `Txn`, qui prend un `TxnRequest` :

```protobuf
message TxnRequest {
  repeated Compare compare = 1;
  repeated RequestOp success = 2;
  repeated RequestOp failure = 3;
}
```

* `compare` - une liste de prédicats représentant une conjonction de termes. Si la comparaison réussit, les requêtes de succès sont traitées dans l'ordre et la réponse contient leurs réponses respectives dans l'ordre.
* `success` - Une liste de requêtes à traiter si toutes les évaluations des tests Compare retournent true.
* `failure` - une liste de requêtes appliquées lorsque la comparaison est évaluée à false.

Le client reçoit un message `TxnResponse` de l'appel `Txn` :

```protobuf
message TxnResponse {
  ResponseHeader header = 1;
  bool succeeded = 2;
  repeated ResponseOp responses = 3;
}
```

* `succeeded` - true si la comparaison a été évaluée à true, false sinon.
* `responses` - une liste de réponses correspondant aux résultats de l'application de success si succeeded est true, ou de failure si succeeded est false.

```protobuf
message ResponseOp {
  oneof response {
    RangeResponse response_range = 1;
    PutResponse response_put = 2;
    DeleteRangeResponse response_delete_range = 3;
  }
}
```

Le `ResponseHeader` inclus dans chaque réponse interne ne devrait en aucun cas être interprété.
Si les clients ont besoin d'obtenir la dernière révision, ils devraient toujours vérifier le `ResponseHeader` au niveau supérieur dans `TxnResponse`.


## API de surveillance {#watch-api}

L'API `Watch` fournit une interface basée sur des événements pour surveiller de manière asynchrone les modifications apportées aux clés. Une surveillance etcd attend les modifications apportées aux clés en surveillant continuellement à partir d'une révision donnée, actuelle ou historique, et diffuse les mises à jour des clés vers le client.

### Événements {#events}

Chaque modification de chaque clé est représentée par des messages `Event`. Un message `Event` fournit à la fois les données de la mise à jour et le type de mise à jour :

```protobuf
message Event {
  enum EventType {
    PUT = 0;
    DELETE = 1;
  }
  EventType type = 1;
  KeyValue kv = 2;
  KeyValue prev_kv = 3;
}
```

* `type` - Le type d'événement. Un type PUT indique que de nouvelles données ont été stockées pour la clé. Un type DELETE indique que la clé a été supprimée.
* `kv` - La paire clé-valeur associée à l'événement. Un événement PUT contient la paire clé-valeur actuelle. Un événement PUT avec kv.Version=1 indique la création d'une clé. Un événement DELETE contient la clé supprimée, dont la révision de modification est définie sur la révision de la suppression.
* `prev_kv` - La paire clé-valeur de la clé à la révision immédiatement antérieure à l'événement. Pour économiser la bande passante, cette information n'est renseignée que si la surveillance a explicitement activé cette fonctionnalité.

### Surveillance des flux {#watch-streams}

Les surveillances sont des requêtes à exécution longue et utilisent des flux gRPC pour transmettre les données d’événements. Un flux de surveillance est bidirectionnel : le client écrit dans le flux pour établir des surveillances et lit pour recevoir les événements de surveillance. Un seul flux de surveillance peut multiplexer plusieurs surveillances distinctes en étiquetant les événements avec des identifiants propres à chaque surveillance. Cette multiplexion permet de réduire la charge mémoire et le surcroît de connexion sur le cluster central etcd.

Pour en savoir plus sur les garanties relatives aux événements de surveillance, veuillez consulter [garanties de l'API etcd][watch-api-guarantees].

Un client crée une surveillance en envoyant un `WatchCreateRequest` sur un flux renvoyé par `Watch` :

```protobuf
message WatchCreateRequest {
  bytes key = 1;
  bytes range_end = 2;
  int64 start_revision = 3;
  bool progress_notify = 4;

  enum FilterType {
    NOPUT = 0;
    NODELETE = 1;
  }
  repeated FilterType filters = 5;
  bool prev_kv = 6;
}
```

* `key`, `range_end` - La plage de clés à surveiller.
* `start_revision` - Une révision facultative à partir de laquelle commencer la surveillance de manière inclusive. Si elle n'est pas fournie, la diffusion en continu des événements suit la révision indiquée dans l'en-tête de réponse de création de surveillance. L'historique complet des événements peut être surveillé à partir de la dernière révision de compactage.
* `progress_notify` - Lorsqu'elle est définie, la surveillance reçoit périodiquement une réponse de surveillance sans événements, si aucun événement récent n'est disponible. Cela est utile lorsque les clients souhaitent récupérer un observateur déconnecté à partir d'une révision connue récente. Le serveur etcd détermine la fréquence d'envoi des notifications en fonction de la charge actuelle du serveur.
* `filters` - Liste des types d’événements à exclure côté serveur.
* `prev_kv` - Lorsqu'il est défini, la surveillance reçoit les données clé-valeur antérieures à l'événement. Cela est utile pour connaître les données qui ont été écrasées.

En réponse à un `WatchCreateRequest` ou si un nouvel événement est détecté pour une surveillance déjà établie, le client reçoit un `WatchResponse` :

```protobuf
message WatchResponse {
  ResponseHeader header = 1;
  int64 watch_id = 2;
  bool created = 3;
  bool canceled = 4;
  int64 compact_revision = 5;

  repeated mvccpb.Event events = 11;
}
```

* `watch_id` - l'identifiant de la surveillance correspondant à la réponse.
* `created` - défini à true si la réponse correspond à une requête de création de surveillance. Le client doit stocker l'identifiant et s'attendre à recevoir des événements pour cette surveillance sur le flux. Tous les événements envoyés à l'observateur créé auront le même watch_id.
* `canceled` - défini à true si la réponse correspond à une requête d'annulation de surveillance. Aucun événement supplémentaire ne sera envoyé à l'observateur annulé.
* `compact_revision` - défini à la révision historique minimale disponible dans etcd si un observateur tente de surveiller à une révision compactée. Cela se produit lorsqu'un observateur est créé à une révision compactée ou lorsque l'observateur ne parvient pas à suivre l'évolution du magasin clé-valeur. L'observateur sera annulé ; la création de nouvelles surveillances avec la même start_revision échouera.
* `events` - une liste d'événements nouveaux, dans l'ordre, correspondant à l'identifiant de surveillance donné.

Si le client souhaite cesser de recevoir des événements pour une surveillance, il émet un `WatchCancelRequest` :

```protobuf
message WatchCancelRequest {
   int64 watch_id = 1;
}
```

* `watch_id` - l'ID de la surveillance à annuler afin qu'aucun événement supplémentaire ne soit transmis.

## API bail {#lease-api}

Les baux sont un mécanisme de détection de la disponibilité des clients. Le cluster accorde des baux avec une durée de vie. Un bail expire si le cluster etcd ne reçoit pas de keepAlive dans le délai TTL imparti.

Pour lier les baux au magasin clé-valeur, chaque clé peut être associée à au plus un bail. Lorsqu’un bail expire ou est révoqué, toutes les clés associées à ce bail sont supprimées. Chaque clé expirée génère un événement de suppression dans l'historique des événements.

### Obtention des baux {#obtaining-leases}

Les baux sont obtenus via l'appel d'API `LeaseGrant`, qui prend un `LeaseGrantRequest` :

```protobuf
message LeaseGrantRequest {
  int64 TTL = 1;
  int64 ID = 2;
}
```

* `TTL` - le délai d'expiration indicatif, en secondes.
* `ID` - l'identifiant demandé pour le bail. Si l'ID est défini à 0, etcd choisira un identifiant.

Le client reçoit un `LeaseGrantResponse` de l'appel `LeaseGrant` :

```protobuf
message LeaseGrantResponse {
  ResponseHeader header = 1;
  int64 ID = 2;
  int64 TTL = 3;
}
```

* `ID` - l'identifiant du bail pour le bail accordé.
* `TTL` - est le délai d'expiration, en secondes, sélectionné par le serveur pour le bail.

```protobuf
message LeaseRevokeRequest {
  int64 ID = 1;
}
```

* `ID` - l'identifiant du bail à révoquer. Lorsque le bail est révoqué, toutes les clés associées sont supprimées.

### Renouvellement des baux {#keep-alives}

Les baux sont actualisés à l’aide d’un flux bidirectionnel créé à l’aide de l’appel d’API `LeaseKeepAlive`. Lorsque le client souhaite actualiser un bail, il envoie un `LeaseKeepAliveRequest` sur le flux :

```protobuf
message LeaseKeepAliveRequest {
  int64 ID = 1;
}
```

* `ID` - l'identifiant du bail dont il faut maintenir la validité.

Le flux de maintien de connexion répond avec un `LeaseKeepAliveResponse` :

```protobuf
message LeaseKeepAliveResponse {
  ResponseHeader header = 1;
  int64 ID = 2;
  int64 TTL = 3;
}
```

* `ID` - le bail qui a été actualisé avec un nouveau délai de validité.
* `TTL` - le nouveau délai de validité, en secondes, restant pour le bail.

[watch-api-guarantees]: /fr/etcd/learning/api_guarantees/#watch-apis
[elections]: https://github.com/etcd-io/etcd/blob/main/client/v3/concurrency/election.go
[grpc-api]: /fr/etcd/dev-guide/api_reference_v3/
[grpc-service]: https://github.com/etcd-io/etcd/blob/main/api/etcdserverpb/rpc.proto
[kv-proto]: https://github.com/etcd-io/etcd/blob/main/api/mvccpb/kv.proto
[locks]: https://github.com/etcd-io/etcd/blob/main/client/v3/concurrency/mutex.go
[mvcc]: https://en.wikipedia.org/wiki/Multiversion_concurrency_control
[stm]: https://github.com/etcd-io/etcd/blob/main/client/v3/concurrency/stm.go
