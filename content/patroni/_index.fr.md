---
title: "Documentation Patroni 4.1.5"
linkTitle: Patroni
weight: 10
icon: fa-solid fa-heart-pulse
description: "Aperçu de la documentation haute disponibilité de Patroni pour PostgreSQL."
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
module: [PATRONI]
categories: [Concept]
upstream_source: patroni
upstream_link: "https://patroni.readthedocs.io/en/latest/index.html"
cascade:
  upstream_source: patroni
  type: docs
  module: [PATRONI]
---

> [!WARNING]
> Exécution de Patroni sur des **systèmes à mémoire limitée avec Python 3.11+**

Si vous exécutez Patroni sur un système avec des limites de mémoire strictes, par exemple avec `vm.overcommit_memory=2` (recommandé pour PostgreSQL), et utilisez Python 3.11 ou une version ultérieure, vous pouvez observer un comportement inattendu :

- Patroni semble sain
- PostgreSQL continue de s'exécuter
- L'**API REST de Patroni devient inopérante**
- Le système d'exploitation indique que Patroni écoute sur le port de l'API REST
- Les journaux de Patroni semblent normaux ; cependant, les messages suivants peuvent apparaître une fois : `Exception ignored in thread started by: <object repr() failed>`, `MemoryError`
- Les journaux du noyau peuvent contenir des messages tels que `not enough memory for the allocation`

Ce comportement est dû à un [bug dans Python 3.11+](https://github.com/python/cpython/issues/140746). Sous des conditions de mémoire strictes, le démarrage d'un nouveau thread peut bloquer indéfiniment en l'absence de mémoire libre.

## Solution recommandée {#recommended-solution}

Les versions récentes de Patroni (4.1.1+, 4.0.8+) réduisent l'impact de ce problème en lançant tous les threads requis dès le démarrage, avant que le système ne soit soumis à une pression mémoire.

## Recommandations supplémentaires (Linux, glibc) {#additional-recommendations-linux-glibc}

Lors de l'exécution avec `vm.overcommit_memory=2` (recommandé pour PostgreSQL), nous recommandons également de lancer Patroni avec les variables d'environnement suivantes configurées :

- `MALLOC_ARENA_MAX=1` - réduit la quantité de mémoire virtuelle allouée par glibc aux applications multithreadées
- `PG_MALLOC_ARENA_MAX=` - réinitialise la valeur de `MALLOC_ARENA_MAX` pour les processus PostgreSQL lancés par Patroni.

En outre, vous pouvez ajuster les paramètres de configuration suivants de Patroni :

- `thread_stack_size` - taille de la pile utilisée par les threads lancés par Patroni. Réduire cette valeur diminue l'utilisation mémoire du processus Patroni. La valeur par défaut définie par Patroni est `512kB`. Augmentez `thread_stack_size` si Patroni subit des plantages liés à la pile ; sinon, la valeur par défaut est suffisante.
- `thread_pool_size` - taille du pool de threads utilisé par Patroni pour les tâches asynchrones et la communication API REST avec les autres membres lors de la course au leader ou des vérifications failsafe. La valeur par défaut est `5`, ce qui est suffisant pour les clusters à trois nœuds.
- `restapi.thread_pool_size` - taille du pool de threads utilisé pour traiter les requêtes API REST. La valeur par défaut est `5`, permettant jusqu'à cinq requêtes API REST en parallèle. Notez que les requêtes impliquant des requêtes SQL sont effectivement sérialisées, car une seule connexion à la base de données est utilisée, aussi l'augmentation de cette valeur ne procure généralement aucun avantage.

--------

Patroni est un modèle de solutions PostgreSQL à haute disponibilité (HA) basé sur Python. Pour une accessibilité maximale, Patroni prend en charge une variété de magasins de configuration distribués, tels que [ZooKeeper](https://zookeeper.apache.org/), [etcd](https://github.com/coreos/etcd), [Consul](https://github.com/hashicorp/consul) ou [Kubernetes](https://kubernetes.io). Les ingénieurs base de données, les DBA, les ingénieurs DevOps et les SRE qui souhaitent déployer rapidement une solution PostgreSQL à haute disponibilité dans des datacenters — ou ailleurs — devraient y trouver un intérêt.

Nous appelons Patroni un « modèle » car il est loin d’être un système de réplication universel ou immédiatement utilisable. Il présente ses propres contraintes. À utiliser avec prudence. Il existe de nombreuses façons de mettre en œuvre une haute disponibilité avec PostgreSQL ; pour en consulter la liste, reportez-vous à la [Documentation PostgreSQL](https://wiki.postgresql.org/wiki/Replication,_Clustering,_and_Connection_Pooling).

Versions de PostgreSQL actuellement prises en charge : 9.3 à 18.

**Remarque aux utilisateurs de Citus** : À compter de la version 3.0, Patroni intègre harmonieusement l'extension de base de données [Citus](https://github.com/citusdata/citus) pour PostgreSQL. Veuillez consulter la page [Prise en charge de Citus](/fr/patroni/citus#citus) dans la documentation de Patroni pour plus d'informations sur l'utilisation de la haute disponibilité Patroni avec un cluster distribué Citus.

**Remarque aux utilisateurs Kubernetes** : Patroni peut s'exécuter nativement sur Kubernetes. Consultez le chapitre [Kubernetes](/fr/patroni/kubernetes#kubernetes) de la documentation Patroni.

<img src="/img/patroni/patroni-logo.png" width="128" height="128" alt="image" />
