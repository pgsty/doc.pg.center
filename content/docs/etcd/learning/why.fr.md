---
title: etcd par rapport aux autres magasins clé-valeur
weight: 2875
description: "Historique et usage d’etcd ainsi que comparaison avec d'autres outils"
categories: [Concept]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/learning/why.md"
aliases: [/etcd/learning/why/]
---

Le nom « etcd » provient de deux idées : le dossier unix « /etc » et les systèmes « d »istribués. Le dossier « /etc » est un emplacement destiné au stockage des données de configuration d’un système unique, tandis qu’etcd stocke les informations de configuration pour des systèmes distribués à grande échelle. Ainsi, un « d »istribué « /etc » devient « etcd ».

etcd est conçu comme une base commune pour les systèmes distribués à grande échelle. Il s'agit de systèmes qui ne tolèrent jamais une opération en split-brain et sont prêts à sacrifier la disponibilité pour atteindre cet objectif. etcd stocke les métadonnées de manière cohérente et résistante aux pannes. Un cluster etcd vise à offrir un stockage clé-valeur avec une stabilité, une fiabilité, une évolutivité et des performances de niveau supérieur.

Les systèmes distribués utilisent etcd comme magasin clé-valeur cohérent pour la gestion de configuration, la découverte de services et la coordination de travaux distribués. De nombreuses [organisations][production-users] utilisent etcd pour mettre en œuvre des systèmes de production tels que des planificateurs de conteneurs, des services de découverte de services et des stockages de données distribués. Les modèles distribués courants utilisant etcd incluent l’[élection de leader][etcd-etcdctl-elect], les [verrous distribués][etcd-etcdctl-lock] et la surveillance de la disponibilité des machines.

## Cas d'utilisation {#use-cases}

- Container Linux by CoreOS : Les applications exécutées sur [Container Linux][container-linux] bénéficient de mises à jour automatiques du noyau Linux, sans interruption de service. Container Linux utilise [locksmith] pour coordonner les mises à jour. Locksmith implémente un sémaphore distribué sur etcd afin de garantir qu’un sous-ensemble seulement d’un cluster est redémarré à tout moment donné.
- [Kubernetes][kubernetes] stocke les données de configuration dans etcd pour la découverte de services et la gestion du cluster ; la cohérence d’etcd est essentielle pour planifier correctement et faire fonctionner les services. Le serveur d’API Kubernetes persiste l’état du cluster dans etcd. Il utilise l’API de surveillance d’etcd pour surveiller le cluster et déployer des modifications critiques de configuration.

## Tableau comparatif {#comparison-chart}

Peut-être que etcd semble déjà être une solution adaptée, mais comme pour toute décision technologique, agissez avec prudence. Veuillez noter que cette documentation a été rédigée par l’équipe etcd. Bien que l’objectif idéal soit une comparaison impartiale des technologies et fonctionnalités, l’expertise et les biais des auteurs favorisent clairement etcd. Utilisez uniquement selon les indications.

Le tableau ci-dessous constitue une référence rapide pratique pour repérer facilement les différences entre etcd et ses alternatives les plus populaires. Des commentaires et détails supplémentaires pour chaque colonne figurent dans les sections suivant le tableau.

|  | etcd | ZooKeeper | Consul | NewSQL (Cloud Spanner, CockroachDB, TiDB) |
| --- | --- | --- | --- | --- |
| Primitives de concurrence | [appels RPC verrou][etcd-v3lock], [appels RPC élection][etcd-v3election], [verrous en ligne de commande][etcd-etcdctl-lock], [élections en ligne de commande][etcd-etcdctl-elect], [recettes][etcd-recipe] en go | [recettes curator][curator] externes en Java | [API native de verrouillage][consul-lock] | [Rare][newsql-leader], le cas échéant |
| Lectures linéarisables | [Oui][etcd-linread] | Non | [Oui][consul-linread] | Parfois |
| Contrôle multiversion de concurrence | [Oui][etcd-mvcc] | Non | Non | Parfois |
| Transactions | [Comparaisons de champs, lecture, écriture][etcd-txn] | [Vérifications de version, écriture][zk-txn] | [Comparaison de champ, verrouillage, lecture, écriture][consul-txn] | Style SQL |
| Notification de modifications | [Intervalles historiques et actuels de clés][etcd-watch] | [Clés et répertoires actuels][zk-watch] | [Clés et préfixes actuels][consul-watch] | Déclencheurs (parfois) |
| Permissions utilisateur | [Basées sur les rôles][etcd-rbac] | [ACLs][zk-acl] | [ACLs][consul-acl] | Variables (par table [GRANT][cockroach-grant], par base [rôles][spanner-roles]) |
| API HTTP/JSON | [Oui][etcd-json] | Non | [Oui][consul-json] | Rarement |
| Réconfiguration du groupe d'hôtes | [Oui][etcd-reconfig] | [>3.5.0][zk-reconfig] | [Oui][consul-reconfig] | Oui |
| Taille maximale de base de données fiable | Plusieurs gigaoctets | Centaines de mégaoctets (parfois plusieurs gigaoctets) | Centaines de mégaoctets | Teraoctets+ |
| Latence minimale de linéarisation en lecture | RTT réseau | Pas de linéarisation en lecture | RTT + fsync | Barrières horaires (atomiques, NTP) |

### ZooKeeper {#zookeeper}

ZooKeeper résout le même problème qu’etcd : la coordination des systèmes distribués et le stockage des métadonnées. Toutefois, etcd bénéficie de l’expérience acquise grâce à l’analyse du design et de l’implémentation de ZooKeeper. Les enseignements tirés de ZooKeeper ont certainement influencé la conception d’etcd, lui permettant de prendre en charge des systèmes à grande échelle comme Kubernetes. Les améliorations apportées par etcd par rapport à ZooKeeper incluent :

* Reconfiguration dynamique de l’appartenance au cluster
* Lecture/écriture stable sous charge élevée
* Modèle de données à contrôle de concurrence multiversion
* Surveillance fiable des clés, sans jamais ignorer silencieusement les événements
* Primitives de bail déconnectant les connexions des sessions
* API pour verrous partagés distribués sûrs

En outre, etcd prend en charge une large gamme de langages et de frameworks directement. Alors que Zookeeper utilise son propre protocole RPC personnalisé, Jute, qui est unique à Zookeeper et limite les liaisons de langages [prises en charge][zk-bindings], le protocole client d’etcd est basé sur [gRPC][grpc], un cadre RPC populaire offrant des liaisons pour go, C++, Java et bien d’autres. De même, gRPC peut être sérialisé en JSON sur HTTP, si bien que des utilitaires de ligne de commande généraux comme `curl` peuvent interagir avec lui. Étant donné que les systèmes peuvent choisir parmi diverses options, ils sont construits autour d’etcd avec des outils natifs plutôt qu’autour d’etcd avec un ensemble fixe et unique de technologies.

Lorsqu’il s’agit d’évaluer les fonctionnalités, le support et la stabilité, les nouvelles applications souhaitant utiliser Zookeeper comme magasin de clés cohérent devraient privilégier etcd.

### Consul {#consul}

Consul est un cadre complet de découverte de services. Il propose des vérifications de santé intégrées, une détection de défaillances et des services DNS. En outre, Consul expose un magasin de clés-valeurs via des API HTTP RESTful. [Tel qu’il en est dans Consul 1.0][dbtester-comparison-results], le système de stockage ne se met pas à l’échelle aussi efficacement que d’autres systèmes comme etcd ou Zookeeper pour les opérations sur les clés-valeurs ; les systèmes nécessitant des millions de clés subiront des latences élevées et une pression mémoire importante. L’API de clés-valeurs manque notamment de fonctionnalités telles que les clés à plusieurs versions, les transactions conditionnelles et les surveillance fiables en continu.

etcd et Consul résolvent des problèmes différents. Si vous recherchez un magasin de clés-valeurs distribué et cohérent, etcd est une meilleure option que Consul. Si vous recherchez une découverte de services complète au sein d’un cluster, etcd ne possède pas suffisamment de fonctionnalités ; optez pour Kubernetes, Consul ou SmartStack.

### NewSQL (Cloud Spanner, CockroachDB, TiDB) {#newsql-cloud-spanner-cockroachdb-tidb}

À la fois etcd et les bases de données NewSQL (par exemple, [Cockroach][cockroach], [TiDB][tidb], [Google Spanner][spanner]) offrent des garanties fortes de cohérence des données avec une haute disponibilité. Toutefois, les paramètres de conception de système sensiblement différents entraînent des API client et des caractéristiques de performance sensiblement différentes.

Les bases de données NewSQL sont conçues pour s'étendre horizontalement à travers des centres de données. Ces systèmes partitionnent généralement les données entre plusieurs groupes de réplication cohérents (shards), potentiellement distants, et stockent des jeux de données de l'ordre du téraoctet et plus. Ce type d'évolutivité les rend peu adaptés à la coordination distribuée, en raison de latences élevées dues à l'attente des horloges et de la prévision d'updates avec des graphes de dépendances majoritairement localisés. Les données sont organisées en tables, incluant des fonctionnalités de requête de style SQL avec des sémantiques plus riches que celles d'etcd, mais au prix d'une complexité accrue pour le traitement, la planification et l'optimisation des requêtes.

En résumé, choisissez etcd pour stocker des métadonnées ou coordonner des applications distribuées. Si vous devez stocker plusieurs gigaoctets de données ou si des requêtes SQL complètes sont nécessaires, privilégiez une base de données NewSQL.

## Utilisation d'etcd pour les métadonnées {#using-etcd-for-metadata}

etcd réplique toutes les données au sein d'un seul groupe de réplication cohérent. Pour stocker jusqu'à quelques Go de données avec un ordre cohérent, il s'agit de la méthode la plus efficace. Chaque modification de l'état du cluster, qui peut affecter plusieurs clés, est attribuée un identifiant unique global, appelé révision dans etcd, issu d'un compteur strictement croissant permettant de raisonner sur l'ordre. Étant donné qu'il n'existe qu'un seul groupe de réplication, la requête de modification n'a besoin de passer que par le protocole Raft pour être validée. En limitant le consensus à un seul groupe de réplication, etcd obtient une cohérence distribuée avec un protocole simple tout en atteignant une latence faible et un débit élevé.

La réplication sous-jacente à etcd ne peut pas être mise à l’échelle horizontalement en raison de l’absence de fractionnement des données. À l’inverse, les bases de données NewSQL fractionnent généralement les données sur plusieurs groupes de réplication cohérents, stockant des jeux de données de l’ordre du téraoctet et plus. Toutefois, pour attribuer à chaque modification un identifiant global unique et croissant, chaque requête doit passer par un protocole de coordination supplémentaire entre les groupes de réplication. Cette étape de coordination supplémentaire peut potentiellement entraîner des conflits sur l’identifiant global, obligeant les requêtes ordonnées à se réessayer. Le résultat est une approche plus complexe, généralement moins performante qu’etcd pour un ordre strict.

Si une application traite principalement des métadonnées ou de l’ordre des métadonnées, par exemple pour coordonner des processus, choisissez etcd. Si l’application nécessite un grand magasin de données étendu sur plusieurs centres de données et ne dépend pas fortement des propriétés d’ordre global fort, choisissez une base de données NewSQL.

## Utilisation d'etcd pour la coordination distribuée {#using-etcd-for-distributed-coordination}

etcd propose des primitives de coordination distribuée telles que les surveillance d'événements, les bails, les élections et les verrous partagés distribués, directement intégrées (notez que, dans le cas du verrou partagé distribué, les utilisateurs doivent être conscients de ses propriétés non évidentes. Les détails sont décrits ci-dessous). Ces primitives sont à la fois maintenues et soutenues par les développeurs etcd ; laisser ces primitives aux bibliothèques externes revient à éviter la responsabilité du développement de logiciels distribués fondamentaux, ce qui laisse le système incomplet. Les bases de données NewSQL s'attendent généralement à ce que ces primitives de coordination soient développées par des tiers. De même, ZooKeeper dispose d'une bibliothèque de recettes de coordination séparée et indépendante [library][curator]. Consul, qui propose une API native de verrouillage, va jusqu'à s'excuser en disant que c’est « [not a bulletproof method][consul-bulletproof] ».

En théorie, il est possible de construire ces primitives sur n'importe quel système de stockage offrant une cohérence forte. Toutefois, les algorithmes sont souvent subtils ; il est facile de concevoir un algorithme de verrouillage qui semble fonctionner, pour qu’il cesse soudainement de fonctionner à cause d’un effet de myriade et d’un décalage de temporisation. En outre, d’autres primitives prises en charge par etcd, telles que la mémoire transactionnelle, dépendent du modèle de données MVCC d’etcd ; une cohérence forte simple ne suffit pas.

Pour la coordination distribuée, le choix d’etcd peut aider à éviter les problèmes opérationnels et économiser des efforts ingénierie.

### Remarques sur l'utilisation du verrouillage et du bail {#notes-on-the-usage-of-lock-and-lease}
etcd fournit des API de verrouillage [basées sur le mécanisme de bail][etcd-v3lock], qui repose sur [le mécanisme de bail][lease] et [son implémentation dans etcd][etcdlease]. L'idée fondamentale du mécanisme de bail est la suivante : un serveur accorde à un client demandeur un jeton, appelé bail. Lorsqu'un bail est accordé, le serveur lui associe un délai d'expiration (TTL). Lorsque le serveur détecte que le temps écoulé dépasse le TTL, il retire le bail. Tant qu'un client détient un bail non retiré, il peut affirmer qu'il détient l'accès à une ressource associée à ce bail. Dans le cas d'etcd, la ressource est une clé dans l'espace de clés etcd. etcd fournit des API de verrouillage selon ce schéma. Toutefois, les API de verrouillage ne peuvent pas être utilisées seules comme mécanisme d'exclusion mutuelle. Elles sont appelées API de verrouillage [pour des raisons historiques][chubby]. Elles peuvent toutefois être utilisées comme mécanisme d'optimisation de l'exclusion mutuelle, comme décrit ci-dessous.

L'aspect le plus important du mécanisme de bail est que le délai d'expiration (TTL) est défini comme un intervalle de temps physique. Le serveur et le client mesurent le passage du temps à l'aide de leurs propres horloges. Cela permet une situation où le serveur révoque le bail, mais le client continue de prétendre en être le propriétaire.

Comment le mécanisme de bail garantit-il l'exclusion mutuelle du mécanisme de verrouillage ? En réalité, le mécanisme de bail lui-même ne garantit pas l'exclusion mutuelle. Le fait de détenir un bail ne garantit pas que son détenteur détient un verrou sur la ressource.

Dans le cas de la gestion des accès mutuels aux clés d'etcd lui-même via un verrou etcd, l'exclusion mutuelle est mise en œuvre selon le mécanisme de validation du numéro de version (appelé parfois compare and swap dans d'autres systèmes comme Consul). Dans les RPCs d'etcd tels que `Put` ou `Txn`, il est possible de spécifier des conditions requises concernant le numéro de révision et l'ID de bail pour les opérations. Si ces conditions ne sont pas satisfaites, l'opération peut échouer. Grâce à ce mécanisme, etcd fournit un verrouillage distribué aux clients. Cela signifie qu'un client sait qu'il acquiert un verrou sur une clé lorsque sa requête est exécutée avec succès par le cluster etcd.

Dans la littérature sur le verrouillage distribué, des conceptions similaires sont décrites :
* Dans le papier [Chubby][chubby], le concept de *séquenceur* est introduit. Nous interprétons que ce séquenceur est presque identique à la combinaison du numéro de révision et de l'ID de bail d'etcd.
* Dans [Comment réaliser un verrouillage distribué][fencing], Martin Kleppmann a introduit l'idée de *jeton de clôture*. Les auteurs interprètent que ce jeton de clôture correspond au numéro de révision dans le cas d'etcd.
* Dans [Utilisations pratiques des horloges synchronisées dans les systèmes distribués][physicalclock], on trouve une description selon laquelle Thor implémente un mécanisme de verrouillage distribué basé sur la validation du numéro de version et du bail.

Pourquoi etcd et d'autres systèmes proposent-ils des bails, alors qu'ils offrent une exclusion mutuelle basée sur la validation du numéro de version ? Les bails fournissent une mécanique d'optimisation visant à réduire le nombre de requêtes abandonnées.

Notez qu’en ce qui concerne les clés etcd, elles peuvent être verrouillées de manière efficace grâce aux mécanismes de bail et de validation du numéro de version. Si les utilisateurs doivent protéger des ressources n’ayant pas de lien avec etcd, ces ressources doivent fournir un mécanisme de validation du numéro de version ainsi qu’une cohérence entre les réplicas, comme le font les clés etcd. La fonction de verrouillage propre à etcd ne peut pas être utilisée pour protéger des ressources externes.

[chubby]: https://research.google/pubs/pub27897/
[cockroach]: https://github.com/cockroachdb/cockroach
[cockroach-grant]: https://www.cockroachlabs.com/docs/stable/grant.html
[consul-acl]: https://www.consul.io/docs/security/acl
[consul-bulletproof]: https://www.consul.io/docs/dynamic-app-config/sessions
[consul-json]: https://www.consul.io/api-docs#formatted-json-output
[consul-linread]: https://www.consul.io/api-docs#consistency
[consul-lock]: https://www.consul.io/commands/lock
[consul-reconfig]: https://developer.hashicorp.com/consul/tutorials/datacenter-operations/add-remove-servers
[consul-txn]: https://www.consul.io/api/kv#txn
[consul-watch]: https://www.consul.io/docs/dynamic-app-config/watches
[container-linux]: https://coreos.com/why
[curator]: http://curator.apache.org/
[dbtester-comparison-results]: https://github.com/coreos/dbtester/tree/master/test-results/2018Q1-02-etcd-zookeeper-consul
[etcd-commonname]: /fr/docs/etcd/op-guide/authentication/#using-tls-common-name
[etcd-etcdctl-elect]: https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#elect-options-election-name-proposal
[etcd-etcdctl-lock]: https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#lock-options-lockname-command-arg1-arg2-
[etcd-json]: /fr/docs/etcd/dev-guide/api_grpc_gateway/
[etcd-linread]: /fr/docs/etcd/learning/api_guarantees/#linearizability
[etcd-mvcc]: /fr/docs/etcd/learning/data_model/
[etcd-rbac]: /fr/docs/etcd/op-guide/authentication/rbac
[etcd-recipe]: https://godoc.org/github.com/etcd-io/etcd/client/v3/experimental/recipes
[etcd-reconfig]: /fr/docs/etcd/op-guide/runtime-configuration
[etcd-txn]: /fr/docs/etcd/learning/api/#transaction
[etcd-v3election]: https://pkg.go.dev/go.etcd.io/etcd/server/v3/etcdserver/api/v3election/v3electionpb
[etcd-v3lock]: https://pkg.go.dev/go.etcd.io/etcd/server/v3/etcdserver/api/v3lock/v3lockpb
[etcd-watch]: /fr/docs/etcd/learning/api/#watch-streams
[etcdlease]: https://godoc.org/github.com/etcd-io/etcd/client/v3/leasing
[fencing]: https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html
[grpc]: https://www.grpc.io
[kubernetes]: https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/
[lease]: https://web.stanford.edu/class/cs240/readings/leases.pdf
[locksmith]: https://github.com/coreos/locksmith
[newsql-leader]: http://dl.acm.org/citation.cfm?id=2960999
[physicalclock]: https://web.archive.org/web/20190725151657/http://www.dainf.cefetpr.br/~tacla/SDII/PracticalUseOfClocks.pdf
[production-users]: https://github.com/etcd-io/etcd/blob/main/ADOPTERS.md
[spanner]: https://cloud.google.com/spanner/
[spanner-roles]: https://cloud.google.com/spanner/docs/iam#roles
[tidb]: https://github.com/pingcap/tidb
[zk-acl]: https://zookeeper.apache.org/doc/r3.1.2/zookeeperProgrammers.html#sc_ZooKeeperAccessControl
[zk-bindings]: https://zookeeper.apache.org/doc/r3.1.2/zookeeperProgrammers.html#ch_bindings
[zk-reconfig]: https://zookeeper.apache.org/doc/current/zookeeperReconfig.html
[zk-txn]: https://zookeeper.apache.org/doc/r3.4.3/api/org/apache/zookeeper/ZooKeeper.html#multi(java.lang.Iterable)
[zk-watch]: https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkWatches
