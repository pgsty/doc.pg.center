---
title: "Garanties de l'API etcd"
weight: 2750
description: Garanties API offertes par etcd
categories: [Concept]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/api_guarantees.md"
---

etcd est un magasin clé-valeur cohérent et durable.
Le magasin clé-valeur est exposé via des [services gRPC][grpc Services].
etcd offre les garanties de cohérence et de durabilité les plus fortes pour un système distribué.
Cette spécification énumère les garanties d'API offertes par etcd.

### API à prendre en compte {#apis-to-consider}

* APIs KV
  * [Range](/fr/etcd/learning/api/#range)
  * [RangeStream](/fr/etcd/learning/api/#rangestream)
  * [Put](/fr/etcd/learning/api/#put)
  * [Delete](/fr/etcd/learning/api/#delete-range)
  * [Transaction](/fr/etcd/learning/api/#transaction)
* APIs de surveillance
  * [Surveillance](/fr/etcd/learning/api/#watch-api)
* APIs de bail
  * [Octroyer](/fr/etcd/learning/api/#obtaining-leases)
  * [Révoquer]
  * [Keep alive](/fr/etcd/learning/api/#keep-alives)

L'API KV permet de lire et de manipuler directement le magasin de paires clé-valeur.
L'API surveillance permet de s'abonner aux modifications apportées au magasin de paires clé-valeur.
L'API bail permet d'attribuer une durée de vie à une clé.

Les API KV et surveillance permettent d'accéder non seulement aux versions les plus récentes des clés, mais aussi aux versions antérieures, dans une fenêtre continue d'historique limitée par une opération de compactage.

L’appel à l’API KV a un effet immédiat, tandis que les réponses de l’API de surveillance peuvent arriver avec un délai non borné.
Dans un cluster etcd correctement fonctionnel, vous devriez vous attendre à ce que les événements de surveillance apparaissent avec un délai de 10 ms après leur occurrence.
Toutefois, aucun délai maximal n'est garanti, et les événements dans des clusters défaillants pourraient ne jamais arriver.

## API clé-valeur {#kv-apis}

etcd garantit la durabilité et la sérialisabilité stricte pour tous les appels d'API de type clé-valeur.
Il s'agit de la garantie d'isolation la plus forte des systèmes de bases de données transactionnelles distribuées.

### Durabilité {#durability}

Toutes les opérations terminées sont durables. Toutes les données accessibles sont également des données durables.
Une lecture ne renverra jamais de données qui n’ont pas été rendues durables.

### Sérialisabilité stricte {#strict-serializability}

Les opérations du service KV sont atomiques et s'effectuent dans un ordre total, conforme à l'ordre temporel réel de ces opérations. L'ordre total est implicite grâce à la [révision][revision]. En savoir plus sur la [sérialisabilité stricte][strict serializability].

Pour les transactions sans transactions imbriquées, l'ordre d'exécution des opérations est garanti identique à celui de sa liste d'opérations, ce qui signifie des réponses GET stables au sein de la transaction.
Pour les transactions avec des transactions imbriquées, l'ordre d'exécution n'est pas spécifié.

La sérialisabilité stricte implique d'autres garanties plus faibles qui pourraient être plus faciles à comprendre :

#### Atomicité {#atomicity}

Toutes les requêtes d'API sont atomiques ; une opération s'effectue entièrement ou pas du tout. Pour les requêtes de surveillance, tous les événements générés par une seule opération figurent dans une seule réponse de surveillance. La surveillance ne peut jamais observer des événements partiels pour une seule opération.

#### Linéarisabilité {#linearizability}

Du point de vue du client, la linéarisabilité offre des propriétés utiles qui facilitent le raisonnement. Il s'agit d'une description claire extraite de l'[article original][linearizability]: `La linéarisabilité donne l’illusion que chaque opération effectuée par des processus concurrents prend effet instantanément à un instant situé entre son invocation et sa réponse.`

Par exemple, considérons un client effectuant une écriture au point de temps 1 (*t1*). Un client effectuant une lecture à *t2* (avec *t2* > *t1*) devrait recevoir une valeur au moins aussi récente que l'écriture précédente, terminée à *t1*. Toutefois, la lecture pourrait ne se terminer qu'à *t3*. La lecture renvoie la valeur courante à un instant précis entre *t2* et *t3*. Elle peut inclure ou exclure une écriture concurrente à cette lecture ; une valeur courante à *t2* peut donc encore être renvoyée même si une autre écriture se termine avant *t3*.

etcd garantit la linéarisabilité pour toutes les autres opérations par défaut.
La linéarisabilité comporte toutefois un coût, car les requêtes linéarisées doivent passer par le processus de consensus Raft. Pour obtenir des latences plus faibles et un débit plus élevé pour les requêtes en lecture, les clients peuvent configurer le mode de cohérence d'une requête sur `serializable`, qui peut accéder à des données obsolètes par rapport au quorum, mais élimine la pénalité de performance liée à la dépendance des accès linéarisés au consensus actif.

## API de surveillance {#watch-apis}

Les surveillances offrent les garanties suivantes concernant les événements :
* Ordre – les événements sont ordonnés par révision.
  Un événement ne peut jamais apparaître sur une surveillance s’il précède dans le temps un événement déjà publié. Pour les transactions sans transactions imbriquées, l’ordre des événements générés est garanti identique à celui de la liste des opérations. Pour les transactions avec transactions imbriquées, l’ordre des événements générés n’est pas spécifié.
* Unicité – un événement ne peut jamais apparaître deux fois sur une surveillance.
* Fiabilité – une séquence d’événements ne peut jamais omettre de sous-séquence d’événements dans la fenêtre d’historique disponible. Si des événements sont ordonnés dans le temps comme a < b < c, alors si la surveillance reçoit les événements a et c, elle est garantie de recevoir b tant que b reste dans la fenêtre d’historique disponible.
* Atomicité – une liste d’événements est garantie d’englober des révisions complètes.
  Les mises à jour effectuées dans la même révision sur plusieurs clés ne seront jamais divisées entre plusieurs listes d’événements.
* Reprise possible – une surveillance interrompue peut être reprise en établissant une nouvelle surveillance démarrant après la dernière révision reçue dans un événement de surveillance avant la rupture, à condition que cette révision soit dans la fenêtre d’historique.
* Marquable – les événements de notification de progression garantissent que tous les événements jusqu’à une révision ont déjà été livrés.

etcd ne garantit pas la linéarisabilité pour les opérations de surveillance. Les utilisateurs doivent vérifier la révision des événements de surveillance afin de garantir un ordre correct par rapport aux autres opérations.

## API bail {#lease-apis}

etcd fournit [un mécanisme de bail][lease]. Le cas d'utilisation principal d'un bail est la mise en œuvre de mécanismes de coordination distribuée, tels que des verrous distribués. Le mécanisme de bail est simple : un bail peut être créé à l'aide de l'API grant, attaché à une clé à l'aide de l'API put, révoqué à l'aide de l'API revoke, et expirera selon le temps de vie (TTL) défini par l'horloge murale. Toutefois, les utilisateurs doivent être conscients [des propriétés importantes des API et de leur utilisation][why] afin d'implémenter correctement des mécanismes de coordination distribuée.

## Définitions spécifiques à etcd {#etcd-specific-definitions}

### Opération terminée {#operation-completed}

Une opération etcd est considérée comme terminée lorsqu'elle est validée par consensus, et donc « exécutée » — stockée de manière permanente — par le moteur de stockage etcd. Le client sait qu'une opération est terminée lorsqu'il reçoit une réponse du serveur etcd. Notez que le client peut ignorer l'état d'une opération si la requête expire, ou s'il y a une interruption réseau entre le client et le membre etcd. etcd peut également annuler des opérations lors d'une élection de leader. etcd ne renvoie pas de réponses `abort` aux requêtes en cours des clients dans cet événement.

### révision {#revision}

Une opération etcd qui modifie le magasin clé-valeur se voit attribuer une révision unique strictement croissante. Une opération transactionnelle peut modifier le magasin clé-valeur plusieurs fois, mais une seule révision lui est attribuée. L'attribut révision d'une paire clé-valeur modifiée par l'opération a la même valeur que la révision de l'opération. La révision peut être utilisée comme horloge logique pour le magasin clé-valeur. Une paire clé-valeur ayant une révision plus élevée est modifiée après une paire clé-valeur ayant une révision plus faible. Deux paires clé-valeur ayant la même révision sont modifiées par une opération « simultanément ».

[grpc Services]: /fr/etcd/learning/api/#grpc-services
[lease]: https://web.stanford.edu/class/cs240/readings/leases.pdf
[linearizability]: https://cs.brown.edu/~mph/HerlihyW90/p463-herlihy.pdf
[serializable_isolation]: https://en.wikipedia.org/wiki/Isolation_(database_systems)#Serializable
[strict serializability]: http://jepsen.io/consistency/models/strict-serializable
[txn]: /fr/etcd/learning/api/#transaction
[why]: /fr/etcd/learning/why/#notes-on-the-usage-of-lock-and-lease
[revision]: #revision
