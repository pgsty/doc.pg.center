---
title: Conception du client etcd
weight: 2250
description: "Décisions d'architecture du client et détails d'implémentation"
categories: [Concept]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/design-client.md"
---

Conception du client etcd {#etcd-client-design}
====================

*Gyuho Lee (github.com/gyuho, Amazon Web Services, Inc.), Joe Betz (github.com/jpbetz, Google Inc.)*


Introduction {#introduction}
====================

Le serveur etcd a démontré sa robustesse au fil de nombreuses années de tests d'injection d'erreurs. La logique d'application la plus complexe est déjà gérée par le serveur etcd et ses magasins de données (par exemple, la gestion de l'appartenance au cluster est transparente pour les clients, les propositions étant acheminées au leader au niveau du protocole Raft). Bien que les composants du serveur soient corrects, leur interaction avec les clients nécessite un ensemble différent de protocoles complexes afin de garantir leur correction et une haute disponibilité en cas de défaillance. Idéalement, le serveur etcd fournit une vue logique unique d'un cluster composé de plusieurs machines physiques, et le client implémente un basculement automatique entre les répliques. Ce document décrit les choix architecturaux du client ainsi que leurs détails d'implémentation.


Glossaire {#glossary}
====================

*clientv3* : client Go officiel pour l'API etcd v3.

*clientv3-grpc1.0* : Implémentation cliente officielle, avec [`grpc-go v1.0.x`](https://github.com/grpc/grpc-go/releases/tag/v1.0.0), utilisée dans la dernière version etcd v3.1.

*clientv3-grpc1.7* : Implémentation cliente officielle, avec [`grpc-go v1.7.x`](https://github.com/grpc/grpc-go/releases/tag/v1.7.0), utilisée dans les versions les plus récentes d'etcd v3.2 et v3.3.

*clientv3-grpc1.23* : Implémentation cliente officielle, avec [`grpc-go v1.23.x`](https://github.com/grpc/grpc-go/releases/tag/v1.23.0), utilisée dans la dernière version etcd v3.4.

*Balancer* : équilibreur de charge client etcd qui implémente un mécanisme de réessai et de basculement. Le client etcd devrait équilibrer automatiquement la charge entre plusieurs points d'accès.

*Endpoints* : une liste d’adresses d’extrémités du serveur etcd auxquelles les clients peuvent se connecter. En général, 3 ou 5 adresses client d’un cluster etcd.

*Endpoint fixe* : Lorsqu’il est configuré avec plusieurs endpoints, l’équilibreur de charge <= v3.3 sélectionne un seul endpoint pour établir une connexion TCP, afin de limiter le nombre total de connexions ouvertes vers le cluster etcd. En v3.4, l’équilibreur de charge effectue un balancement round-robin sur les endpoints fixés pour chaque requête, ce qui permet une répartition plus équilibrée de la charge.

*Connexion client* : connexion TCP établie avec un serveur etcd, via gRPC Dial.

*Connexion sous-jacente* : interface gRPC SubConn. Chaque connexion sous-jacente contient une liste d'adresses. L’équilibreur de charge crée une SubConn à partir d'une liste d'adresses résolues. Une connexion cliente gRPC peut être associée à plusieurs SubConn (par exemple, example.com se résout en `10.10.10.1` et `10.10.10.2` de deux connexions sous-jacentes). L’équilibreur de charge d'etcd v3.4 utilise un résolveur interne pour établir une connexion sous-jacente pour chaque point de terminaison.

*Déconnexion transitoire* : lorsque le serveur gRPC retourne une erreur de statut [`code Unavailable`](https://godoc.org/google.golang.org/grpc/codes#Code).


Exigences client {#client-requirements}
====================

*Exactitude*. Les requêtes peuvent échouer en cas de défaillance du serveur. Toutefois, les garanties de cohérence ne sont jamais violées : propriétés d’ordre global, écriture jamais corrompue, sémantique au plus une fois pour les opérations modifiables, la surveillance ne perçoit jamais d’événements partiels, et ainsi de suite.

*Vivacité*. Les serveurs peuvent tomber en panne ou se déconnecter brièvement. Les clients devraient pouvoir progresser dans les deux cas. Les clients devraient [ne jamais bloquer](https://github.com/etcd-io/etcd/issues/8980) en attendant qu’un serveur revienne en ligne, sauf si configuré pour ce faire. Idéalement, les clients détectent les serveurs indisponibles à l’aide de pings HTTP/2 et basculent vers d’autres nœuds avec des messages d’erreur clairs.

*Efficacité*. Les clients devraient fonctionner efficacement avec un usage minimal des ressources : les connexions TCP précédentes devraient être [fermées correctement](https://github.com/etcd-io/etcd/issues/9212) après un changement de point de terminaison. Le mécanisme de basculement devrait prévoir efficacement la prochaine réplique à connecter, sans tenter inutilement de se reconnecter aux nœuds défaillants.

*Portabilité*. Le client officiel devrait être clairement documenté et son implémentation devrait être applicable à d'autres liaisons de langage. La gestion des erreurs entre les différentes liaisons de langage devrait être cohérente. Étant donné qu’etcd s’engage pleinement en faveur de gRPC, l’implémentation devrait être étroitement alignée sur les objectifs de conception à long terme de gRPC (par exemple, une politique de réessai paramétrable devrait être compatible avec [gRPC retry](https://github.com/grpc/proposal/blob/master/A6-client-retries.md)). Les mises à jour entre deux versions du client devraient être non disruptives.


Aperçu du client {#client-overview}
====================

Le client etcd implémente les composants suivants :

* équilibreur de charge qui établit des connexions gRPC vers un cluster etcd,
* client API qui envoie des appels RPC à un serveur etcd, et
* gestionnaire d'erreurs qui détermine s'il faut réessayer une requête échouée ou basculer vers un autre point de terminaison.

Les langages peuvent différer quant à la manière d’établir une connexion initiale (par exemple, configurer TLS), à la manière d’encoder et d’envoyer des messages Protocol Buffer au serveur, à la gestion des appels RPC en flux, et ainsi de suite. Toutefois, les erreurs renvoyées par le serveur etcd seront identiques. La gestion des erreurs et la politique de nouvelle tentative devraient donc être identiques.

Par exemple, le serveur etcd peut retourner `"rpc error: code = Unavailable desc = etcdserver: request timed out"`, qui correspond à une erreur transitoire nécessitant une nouvelle tentative. Ou bien retourner `rpc error: code = InvalidArgument desc = etcdserver: key is not provided`, ce qui signifie que la requête était invalide et ne doit pas être réessayée. Le client Go peut analyser les erreurs à l’aide de `google.golang.org/grpc/status.FromError`, et le client Java à l’aide de `io.grpc.Status.fromThrowable`.


clientv3-grpc1.0 : Vue d'ensemble de l’équilibreur de charge {#clientv3-grpc10-balancer-overview}
--------------------

`clientv3-grpc1.0` maintient plusieurs connexions TCP lorsqu'il est configuré avec plusieurs points d'accès etcd. Il sélectionne alors une adresse et l'utilise pour envoyer toutes les requêtes clientes. L'adresse fixe est conservée jusqu'à la fermeture de l'objet client (voir *Figure 1*). Lorsque le client reçoit une erreur, il choisit aléatoirement une autre adresse et réessaie.

![client-balancer-figure-01.png](/etcd/learning/img/client-balancer-figure-01.png)


clientv3-grpc1.0 : Limitation de l’équilibreur de charge {#clientv3-grpc10-balancer-limitation}
--------------------

L'ouverture de plusieurs connexions TCP par `clientv3-grpc1.0` peut accélérer le basculement de l’équilibreur de charge, mais nécessite davantage de ressources. L’équilibreur de charge ne comprend pas l'état de santé des nœuds ni l'appartenance au cluster. Il est donc possible que l’équilibreur de charge reste bloqué sur un nœud défaillant ou isolé.


clientv3-grpc1.7 : Vue d'ensemble de l’équilibreur de charge {#clientv3-grpc17-balancer-overview}
--------------------

`clientv3-grpc1.7` ne maintient qu'une seule connexion TCP vers un serveur etcd sélectionné. Lorsqu'il est fourni avec plusieurs points d'accès du cluster, le client tente d'établir une connexion avec chacun d'eux. Dès qu'une connexion est active, l’équilibreur de charge fixe l'adresse, en fermant les autres (voir *Figure 2*). L'adresse fixée doit être conservée jusqu'à la fermeture de l'objet client. Une erreur, provenant d'une panne du serveur ou du réseau client, est transmise au gestionnaire d'erreurs du client (voir *Figure 3*).

![client-balancer-figure-02.png](/etcd/learning/img/client-balancer-figure-02.png)

![client-balancer-figure-03.png](/etcd/learning/img/client-balancer-figure-03.png)

Le gestionnaire d'erreurs client prend une erreur provenant du serveur gRPC, et décide de procéder à une nouvelle tentative sur le même point de terminaison ou de passer à d'autres adresses, en fonction du code d'erreur et du message (voir *Figure 4* et *Figure 5*).

![client-balancer-figure-04.png](/etcd/learning/img/client-balancer-figure-04.png)

![client-balancer-figure-05.png](/etcd/learning/img/client-balancer-figure-05.png)

Les appels RPC en flux, tels que Surveillance et KeepAlive, sont souvent demandés sans délai d'attente. À la place, le client peut envoyer des ping HTTP/2 périodiques pour vérifier l'état d'un point d'accès fixe ; si le serveur ne répond pas au ping, l'équilibreur de charge bascule vers d'autres points d'accès (voir *Figure 6*).

![client-balancer-figure-06.png](/etcd/learning/img/client-balancer-figure-06.png)


clientv3-grpc1.7 : Limitation de l’équilibreur de charge {#clientv3-grpc17-balancer-limitation}
--------------------

L’équilibreur de charge `clientv3-grpc1.7` envoie des keepalives HTTP/2 pour détecter les déconnexions provenant des requêtes en streaming. Il s'agit d'un mécanisme de ping simple basé sur un serveur gRPC, qui ne tient pas compte de l'appartenance au cluster, et ne peut donc pas détecter les partitions réseau. Comme un serveur gRPC partitionné peut continuer à répondre aux pings clients, l'équilibreur peut rester bloqué sur un nœud partitionné. Idéalement, le ping de keepalive doit détecter la partition et déclencher un basculement de point de terminaison avant l'expiration de la requête (voir [etcd#8673](https://github.com/etcd-io/etcd/issues/8673) et *Figure 7*).

![client-balancer-figure-07.png](/etcd/learning/img/client-balancer-figure-07.png)

L’équilibreur de charge `clientv3-grpc1.7` maintient une liste d'extrémités défaillantes. Les adresses déconnectées sont ajoutées à la liste « défaillantes » et considérées comme indisponibles jusqu'après la durée d'attente, qui est codée en dur comme le délai de connexion avec une valeur par défaut de 5 secondes. L’équilibreur de charge peut produire des faux positifs concernant les extrémités défaillantes. Par exemple, l'extrémité A peut revenir juste après avoir été bannie, mais rester indisponible pendant les 5 secondes suivantes (voir *Figure 8*).

`clientv3-grpc1.0` a connu les mêmes problèmes mentionnés ci-dessus.

![client-balancer-figure-08.png](/etcd/learning/img/client-balancer-figure-08.png)

Le projet gRPC Go en amont avait déjà migré vers la nouvelle interface d’équilibreur de charge. Par exemple, l'implémentation de l’équilibreur de charge sous-jacent utilisée par `clientv3-grpc1.7` utilise le nouvel équilibreur de charge gRPC et tente de rester cohérente avec les comportements de l’équilibreur de charge ancien. Bien que sa compatibilité ait été maintenue de manière raisonnable, le client etcd a toujours [souffert de modifications subtiles cassantes](https://github.com/grpc/grpc-go/issues/1649). En outre, les mainteneurs gRPC recommandent de [ne pas s'appuyer sur l'interface ancienne de l’équilibreur de charge](https://github.com/grpc/grpc-go/issues/1942#issuecomment-375368665). En général, pour bénéficier d'un meilleur support de la part des projets upstream, il est préférable de rester synchronisé avec les dernières versions de gRPC. De plus, de nouvelles fonctionnalités, telles que la politique de nouvelle tentative, ne seront peut-être pas reportées sur la branche gRPC 1.7. Par conséquent, le serveur etcd ainsi que le client doivent migrer vers les versions les plus récentes de gRPC.


clientv3-grpc1.23 : Aperçu de l’équilibreur de charge {#clientv3-grpc123-balancer-overview}
--------------------

`clientv3-grpc1.7` est si étroitement lié à l'ancienne interface gRPC qu'une mise à jour de n'importe quelle dépendance gRPC a perturbé le comportement des clients. La majeure partie des efforts de développement et de débogage a été consacrée à la correction de ces changements de comportement des clients. En conséquence, son implémentation est devenue excessivement complexe, fondée sur des hypothèses erronées concernant les connectivités serveur.

L'objectif principal de `clientv3-grpc1.23` est de simplifier la logique de basculement de l’équilibreur de charge ; plutôt que de maintenir une liste d'extrémités défaillantes, qui pourrait être périmée, il suffit de procéder à un roundrobin vers l'extrémité suivante chaque fois que le client se déconnecte de l'extrémité actuelle. Il ne suppose pas l'état des extrémités. Ainsi, il n'est plus nécessaire de suivre de manière complexe l'état (voir *Figure 8* et ci-dessus). La mise à jour vers `clientv3-grpc1.23` ne devrait poser aucun problème ; toutes les modifications ont été internes tout en préservant toutes les compatibilités descendantes.

En interne, lorsqu’il reçoit plusieurs points de terminaison, `clientv3-grpc1.23` crée plusieurs sous-connexions (une sous-connexion par point de terminaison), tandis que `clientv3-grpc1.7` n’établit qu’une seule connexion vers un point de terminaison fixe (voir *Figure 9*). Par exemple, dans un cluster de 5 nœuds, l’équilibreur de charge `clientv3-grpc1.23` nécessiterait 5 connexions TCP, tandis que `clientv3-grpc1.7` n’en nécessite qu’une seule. En conservant un pool de connexions TCP, `clientv3-grpc1.23` peut consommer davantage de ressources mais offre un équilibreur de charge plus flexible avec de meilleures performances de basculement. La politique de répartition par défaut est le round robin, mais elle peut être facilement étendue pour prendre en charge d’autres types d’équilibreurs de charge (par exemple, choix entre deux, sélection du leader, etc.). `clientv3-grpc1.23` utilise le groupe de résolution gRPC et implémente la politique de sélection de l’équilibreur de charge, afin de déléguer le travail de répartition complexe au gRPC amont. En revanche, `clientv3-grpc1.7` gère manuellement chaque connexion gRPC et le basculement de l’équilibreur de charge, ce qui complique l’implémentation. `clientv3-grpc1.23` implémente les nouvelles tentatives dans la chaîne d’intercepteurs gRPC, qui gère automatiquement les erreurs internes gRPC et permet des politiques de nouvelle tentative plus avancées, comme le backoff, tandis que `clientv3-grpc1.7` interprète manuellement les erreurs gRPC pour les nouvelles tentatives.

![client-balancer-figure-09.png](/etcd/learning/img/client-balancer-figure-09.png)


clientv3-grpc1.23 : Limitation de l’équilibreur de charge {#clientv3-grpc123-balancer-limitation}
--------------------

Les améliorations peuvent être apportées en mettant en cache l’état de chaque point de terminaison. Par exemple, l’équilibreur de charge peut interroger à l’avance chaque serveur afin de maintenir une liste de candidats sains, et utiliser ces informations lors d’un routage par rotation. Ou bien, en cas de déconnexion, l’équilibreur de charge peut privilégier les points de terminaison sains. Cela peut compliquer l’implémentation de l’équilibreur de charge, ce qui peut être traité dans des versions ultérieures.

Le ping de keepalive côté client ne prend toujours pas en compte les partitions réseau. Une requête en streaming peut bloquer sur un nœud partitionné. Une solution avancée de vérification de santé doit être mise en œuvre pour comprendre l’appartenance au cluster (voir [etcd#8673](https://github.com/etcd-io/etcd/issues/8673) pour plus de détails).

![client-balancer-figure-07.png](/etcd/learning/img/client-balancer-figure-07.png)

Actuellement, la logique de nouvelle tentative est gérée manuellement en tant qu'intercepteur. Cela pourrait être simplifié grâce [aux nouvelles tentatives officielles gRPC](https://github.com/grpc/proposal/blob/master/A6-client-retries.md).
