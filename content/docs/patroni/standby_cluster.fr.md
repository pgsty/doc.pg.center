---
title: "cluster de secours"
weight: 80
icon: fa-solid fa-clone
description: "Configuration du cluster de secours, comportement et réplication depuis un primaire distant."
module: [PATRONI]
categories: [Tâche]
aliases: [/patroni/standby_cluster/]
upstream_link: "https://patroni.readthedocs.io/en/latest/standby_cluster.html"
---

<a id="standby_cluster"></a>
Patroni prend également en charge l'exécution d'une réplication en cascade vers un centre de données distant (région) à l'aide d'une fonctionnalité appelée « stand-by cluster ». Ce type de cluster présente les caractéristiques suivantes :

- « leader en veille », qui se comporte presque comme un leader de cluster régulier, à ceci près qu'il effectue la réplication à partir d'un nœud distant.
- répliques en cascade, qui effectuent la réplication à partir d'un leader en veille.

Le leader de secours détient et met à jour un verrou de leader dans le DCS. Si le verrou de leader expire, les répliques en cascade effectueront une élection afin de choisir un autre leader parmi les serveurs de secours.

Il n’existe aucune relation supplémentaire entre le cluster de secours et le cluster primaire dont il effectue la réplication, en particulier, ils ne doivent pas partager la même portée DCS s’ils utilisent le même DCS. Ils ne se connaissent mutuellement que par les informations de réplication. En outre, le cluster de secours n’est pas affiché dans la sortie de [patronictl_list](/fr/docs/patroni/patronictl#patronictl_list) ou de [patronictl_topology](/fr/docs/patroni/patronictl#patronictl_topology) sur le cluster primaire.

Pour des raisons de flexibilité, vous pouvez spécifier les méthodes de création d'une réplique et de récupération des enregistrements WAL lorsque le cluster est en mode « standby » en indiquant la clé [create_replica_methods](/fr/docs/patroni/replica_bootstrap#custom_replica_creation) dans la section [standby_cluster](/fr/docs/patroni/standby_cluster#standby_cluster). Cette configuration diffère de la création de répliques lorsque le cluster est détaché et fonctionne comme un cluster normal, qui est contrôlée par `create_replica_methods` dans la section `postgresql`. Les deux clés « standby » et « normal » font référence à la section `create_replica_methods` dans `postgresql`.

Pour configurer un tel cluster, vous devez spécifier la section [standby_cluster](/fr/docs/patroni/standby_cluster#standby_cluster) dans la configuration Patroni :

```yaml
bootstrap:
    dcs:
        standby_cluster:
            host: 1.2.3.4
            port: 5432
            primary_slot_name: patroni
            create_replica_methods:
            - basebackup
```

Notez que ces options ne seront appliquées qu'une seule fois lors de l'amorçage du cluster, et que la seule manière de les modifier par la suite passe par le DCS.

Patroni s'attend à trouver `postgresql.conf` ou `postgresql.conf.backup` dans PGDATA du serveur primaire distant et ne démarrera pas si ces fichiers ne sont pas présents après une basebackup. Si le serveur primaire distant conserve `postgresql.conf` ailleurs, il vous incombe de le copier dans PGDATA.

Si vous utilisez des slots de réplication sur le cluster de secours, vous devez également créer le slot de réplication correspondant sur le cluster primaire. Ce dernier ne sera pas créé automatiquement par l’implémentation du cluster de secours. Vous pouvez utiliser la fonctionnalité des slots de réplication permanents de Patroni sur le cluster primaire afin de maintenir un slot de réplication portant le même nom que `primary_slot_name`, ou sa valeur par défaut si `primary_slot_name` n’est pas fourni.

En cas où le site distant ne fournit pas un seul point d'accès connecté au primaire, il est possible de lister tous les hôtes du cluster source dans la section `standby_cluster.host`. Lorsque `standby_cluster.host` contient plusieurs hôtes séparés par des virgules, Patroni effectuera :

-  ajoutez `target_session_attrs=read-write` au `primary_conninfo` sur le nœud leader de secours.
-  utilisez `target_session_attrs=read-write` pour déterminer si vous devez exécuter `pg_rewind` ou lors de l'exécution de `pg_rewind` sur tous les nœuds du cluster de secours.
-  Il est important de noter que pour que `pg_rewind` fonctionne correctement, soit le cluster doit être initialisé avec `data page checksums` (`--data-checksums` option pour `initdb`) et/ou `wal_log_hints` doit être défini sur `on`. Sinon, `pg_rewind` ne fonctionnera pas correctement.

Il est également possible de répliquer un cluster de secours à partir d’un autre cluster de secours ou d’un membre de secours du cluster primaire : pour cela, vous devez définir un seul hôte dans la section `standby_cluster.host`. Toutefois, vous devez prendre garde au fait que `pg_rewind` échouera à s’exécuter sur le cluster de secours dans ce cas.

> [!AVERTISSEMENT]
> Les noms de membre (le champ `name` dans la configuration Patroni de chaque nœud) doivent être uniques dans l'ensemble du cluster primaire et de tous les clusters de secours connectés à celui-ci.
>
> Patroni définit `synchronous_standby_names` sur le cluster primaire à l'aide des noms de membre, qui deviennent également les `application_name` de chaque connexion de réplication dans `pg_stat_replication`. Si un nœud d'un cluster de secours partage le même nom qu'un membre du cluster primaire, PostgreSQL détecte deux connexions ayant des valeurs `application_name` identiques. Cette ambiguïté peut amener PostgreSQL à satisfaire la condition de réplication synchrone en utilisant la connexion du cluster de secours au lieu du membre du cluster primaire prévu, ce qui fait que PostgreSQL reconnaît prématurément les transactions comme étant validées de manière synchrone, alors qu'elles ne sont pas durables sur le bon nœud de secours.
>
> Il s'agit d'une défaillance silencieuse : la réplication continue sans aucune erreur signalée, mais le cluster fonctionne effectivement sans nœud de secours synchrone valide, ce qui constitue un risque potentiel de perte de données en cas de défaillance du cluster primaire.
