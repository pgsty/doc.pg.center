---
title: Maintenance
weight: 4450
description: Guide de maintenance périodique du cluster etcd
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/maintenance.md"
---

## Aperçu {#overview}

Un cluster etcd nécessite une maintenance périodique pour rester fiable. Selon les besoins d'une application etcd, cette maintenance peut généralement être automatisée et effectuée sans interruption de service ni dégradation significative des performances.

Toute maintenance etcd gère les ressources de stockage consommées par l’espace de clés etcd. Une gestion insuffisante de la taille de l’espace de clés est protégée par des quotas d’espace de stockage ; si un membre etcd manque d’espace, un quota déclenchera des alarmes à l’échelle du cluster, mettant le système en mode maintenance à opérations limitées. Pour éviter de manquer d’espace pour les écritures dans l’espace de clés, l’historique de l’espace de clés etcd doit être compacté. L’espace de stockage lui-même peut être récupéré en défragmentant les membres etcd. Enfin, des sauvegardes périodiques d’instantanés de l’état des membres etcd permettent de récupérer toute perte logique de données ou corruption involontaire causée par une erreur opérationnelle.

## Rétention du journal Raft {#raft-log-retention}

`etcd --snapshot-count` définit le nombre d'entrées Raft appliquées à conserver en mémoire avant le compactage. Lorsque `--snapshot-count` est atteint, le serveur persiste d'abord les données d'instantané sur le disque, puis tronque les anciennes entrées. Lorsqu'un suiveur lent demande des journaux antérieurs à un index compacté, le leader envoie un instantané, forçant ainsi le suiveur à écraser son état.

Une valeur plus élevée de `--snapshot-count` conserve davantage d'entrées Raft en mémoire jusqu'à l'instantané, entraînant ainsi une [utilisation mémoire accrue et récurrente](https://github.com/kubernetes/kubernetes/issues/60589#issuecomment-371977156). Comme le leader conserve les dernières entrées Raft plus longtemps, un suiveur lent dispose de plus de temps pour se synchroniser avant que le leader ne prenne un instantané. `--snapshot-count` représente un compromis entre une utilisation mémoire plus élevée et une meilleure disponibilité des suiveurs lents.

Dans la version 3.2, la valeur par défaut de `--snapshot-count` est [passée de 10 000 à 100 000](https://github.com/etcd-io/etcd/pull/7160). Dans la version 3.7.0, la valeur par défaut est de 10 000.

Sur le plan des performances, un nombre supérieur à 100 000 pour `--snapshot-count` peut affecter le débit d'écriture. Un plus grand nombre d'objets en mémoire peut ralentir la phase de marquage du ramasse-miettes de [`runtime.scanobject`](https://golang.org/src/runtime/mgc.go), et une récupération mémoire peu fréquente rend l'allocation plus lente. Les performances varient selon les charges de travail et les environnements système. Toutefois, en général, un compactage trop fréquent affecte la disponibilité du cluster et le débit d'écriture. Un compactage trop rare est également préjudiciable, car il exerce une pression excessive sur le ramasse-miettes Go. Voir [Comprendre les aspects de performance d'etcd et de Raft](https://www.slideshare.net/mitakeh/understanding-performance-aspects-of-etcd-and-raft) pour plus de résultats de recherche.

## Compactage de l'historique : base de données clé-valeur API v3 {#history-compaction-v3-api-key-value-database}

Depuis que etcd conserve un historique exact de son espace de clés, cet historique doit être régulièrement compacté afin d'éviter une dégradation des performances et un épuisement éventuel de l'espace de stockage. La compactation de l'historique de l'espace de clés supprime toutes les informations relatives aux clés remplacées avant une révision donnée de l'espace de clés. L'espace utilisé par ces clés devient alors disponible pour de nouvelles écritures dans l'espace de clés.

L'espace de clés peut être compacté automatiquement selon la politique de rétention des historiques à fenêtre temporelle de `etcd`, ou manuellement via `etcdctl`. La méthode `etcdctl` offre un contrôle fin du processus de compactage, tandis que le compactage automatique convient aux applications qui nécessitent l'historique des clés pendant une durée déterminée.

Un compactage initié par `etcdctl` fonctionne comme suit :

```sh
# compact up to revision 3
$ etcdctl compact 3
```

Les révisions antérieures à la révision de compactage deviennent inaccessibles :

```sh
$ etcdctl get --rev=2 somekey
Error:  rpc error: code = 11 desc = etcdserver: mvcc: required revision has been compacted
```

### Compactage automatique {#auto-compaction}

`etcd` peut être défini pour effectuer automatiquement le compactage de l'espace de clés à l'aide des options `--auto-compaction-mode` et `--auto-compaction-retention`. Deux modes de compactage sont disponibles : `periodic` (par défaut) et `revision`.

#### Compactage périodique {#periodic-compaction}

Le compactage périodique conserve une fenêtre temporelle de l'historique de l'espace de clés :

```sh
# keep one hour of history
$ etcd --auto-compaction-retention=1h
```

La valeur de rétention précise la quantité d'historique à conserver. Un enregistrement ne sera pas compacté avant environ cette durée écoulée depuis sa création. Cela garantit que les observateurs lents peuvent encore rattraper leur retard dans la fenêtre de rétention.

Lorsque la période de rétention est supérieure à 1 heure, etcd effectue une compaction toutes les heures tout en maintenant la fenêtre complète de rétention. Lorsque la période de rétention est égale ou inférieure à 1 heure, etcd effectue une compaction à intervalle égal à la période de rétention.

Par exemple, avec `--auto-compaction-retention=10h`, etcd attend 10 heures pour le premier compactage, puis compacte toutes les heures par la suite :

```text
0hr  (rev = 1)
1hr  (rev = 10)
...
8hr  (rev = 80)
9hr  (rev = 90)
10hr (rev = 100, Compact(1))
11hr (rev = 110, Compact(10))
...
```

Les valeurs recommandées dépendent du cas d'utilisation :

- Mises à jour fréquentes des mêmes clés : une période courte, telle que `1h` ou `30m`
- Mises à jour peu fréquentes : une période plus longue, telle que `24h`, `48h`, ou `72h`
- Valeur par défaut générale : `10h`

#### Compactage de révision {#revision-compaction}

Le compactage par révision conserve un nombre fixe de révisions :

```sh
# keep 1000 revisions
$ etcd --auto-compaction-mode=revision --auto-compaction-retention=1000
```

etcd vérifie toutes les 5 minutes et effectue une compaction sur `"latest revision" - 1000`. Par exemple, lorsque la dernière révision est 30000, elle effectue une compaction à la révision 29000.

## Défragmentation {#defragmentation}

Après avoir compacté l’espace de clés, la base de données backend peut présenter une fragmentation interne. Toute fragmentation interne correspond à de l’espace libre pour la base de données backend mais qui continue de consommer de l’espace de stockage. La compactation des anciennes révisions fragmente `etcd` en interne en laissant des espaces vides dans la base de données backend. L’espace fragmenté est disponible pour `etcd` mais non disponible pour le système de fichiers hôte. Autrement dit, la suppression des données d’application ne libère pas l’espace sur le disque.

Le processus de défragmentation libère cet espace de stockage au système de fichiers. La défragmentation est effectuée au niveau du membre, afin d'éviter des pics de latence affectant l'ensemble du cluster.

Pour défragmenter un membre etcd, utilisez la commande `etcdctl defrag` :

```sh
$ etcdctl defrag
Finished defragmenting etcd member[127.0.0.1:2379]
```

> [!WARNING]
> Notez que la défragmentation d'un membre en cours d'exécution bloque le système en lecture et écriture pendant la reconstruction de ses états

> [!WARNING]
> Notez que la demande de défragmentation n'est pas répliquée au sein du cluster. Autrement dit, la demande n'est appliquée qu'au nœud local. Spécifiez tous les membres dans l'option `--endpoints` ou l'option `--cluster` pour trouver automatiquement tous les membres du cluster.

Exécutez les opérations de défragmentation pour tous les points d'accès du cluster associé au point d'accès par défaut :

```bash
$ etcdctl defrag --cluster
Finished defragmenting etcd member[http://127.0.0.1:2379]
Finished defragmenting etcd member[http://127.0.0.1:22379]
Finished defragmenting etcd member[http://127.0.0.1:32379]
```

Pour défragmenter directement un répertoire de données etcd lorsque etcd n'est pas en cours d'exécution, utilisez la commande :

```sh
etcdutl defrag --data-dir <path-to-etcd-data-dir>
```

## Quota d'espace {#space-quota}

Le quota d’espace dans `etcd` garantit un fonctionnement fiable du cluster. Sans quota d’espace, `etcd` peut connaître des performances médiocres si l’espace de clés devient trop volumineux, ou simplement manquer d’espace de stockage, entraînant un comportement imprévisible du cluster. Si la base de données backend de l’espace de clés de tout membre dépasse le quota d’espace, `etcd` déclenche une alarme à l’échelle du cluster, qui met le cluster en mode maintenance, acceptant uniquement les lectures et suppressions de clés. Le cluster ne peut reprendre un fonctionnement normal qu’après avoir libéré suffisamment d’espace dans l’espace de clés, défragmenté la base de données backend et effacé l’alarme de quota d’espace.

Par défaut, `etcd` définit un quota d'espace conservateur adapté à la plupart des applications, mais il peut être configuré en ligne de commande, en octets :

```sh
# set a very small 16 MiB quota
$ etcd --quota-backend-bytes=$((16*1024*1024))
```

Le quota d’espace peut être déclenché par une boucle :

```sh
# fill keyspace
$ while [ 1 ]; do dd if=/dev/urandom bs=1024 count=1024  | ETCDCTL_API=3 etcdctl put key  || break; done
...
Error:  rpc error: code = 8 desc = etcdserver: mvcc: database space exceeded
# confirm quota space is exceeded
$ ETCDCTL_API=3 etcdctl --write-out=table endpoint status
+----------------+------------------+-----------+---------+-----------+-----------+------------+
|    ENDPOINT    |        ID        |  VERSION  | DB SIZE | IS LEADER | RAFT TERM | RAFT INDEX |
+----------------+------------------+-----------+---------+-----------+-----------+------------+
| 127.0.0.1:2379 | bf9071f4639c75cc | 2.3.0+git | 18 MB   | true      |         2 |       3332 |
+----------------+------------------+-----------+---------+-----------+-----------+------------+
# confirm alarm is raised
$ ETCDCTL_API=3 etcdctl alarm list
memberID:13803658152347727308 alarm:NOSPACE
```

Supprimer les données d’espace de clés excessives et défragmenter la base de données du backend ramènera le cluster dans les limites du quota :

```sh
# get current revision
$ rev=$(ETCDCTL_API=3 etcdctl --endpoints=:2379 endpoint status --write-out="json" | egrep -o '"revision":[0-9]*' | egrep -o '[0-9].*')
# compact away all old revisions
$ ETCDCTL_API=3 etcdctl compact $rev
compacted revision 1516
# defragment away excessive space
$ ETCDCTL_API=3 etcdctl defrag
Finished defragmenting etcd member[127.0.0.1:2379]
# disarm alarm
$ ETCDCTL_API=3 etcdctl alarm disarm
memberID:13803658152347727308 alarm:NOSPACE
# test puts are allowed again
$ ETCDCTL_API=3 etcdctl put newkey 123
OK
```

La métrique `etcd_mvcc_db_total_size_in_use_in_bytes` indique l'utilisation réelle de la base de données après un compactage de l'historique, tandis que `etcd_debugging_mvcc_db_total_size_in_bytes` affiche la taille de la base de données incluant l'espace libre en attente de défragmentation. Cette dernière n'augmente que lorsque la première est proche d'elle, ce qui signifie qu'une fois que ces deux métriques sont proches du quota, un compactage de l'historique est nécessaire pour éviter de déclencher la limite d'espace.

`etcd_debugging_mvcc_db_total_size_in_bytes` est renommé en `etcd_mvcc_db_total_size_in_bytes` à compter de la version 3.4.

> [!WARNING]
> Il est possible de recevoir une erreur `ErrGRPCNoSpace` pour une requête Put/Txn/LeaseGrant, tout en voyant la requête d'écriture réussir en arrière-plan, car etcd vérifie la limite d'espace à la couche API et à la couche Apply, et la couche Apply ne lèvera que l'alarme `NOSPACE` sans bloquer la transaction.

## Sauvegarde d'instantané {#snapshot-backup}

Effectuer des instantanés du cluster `etcd` de manière régulière constitue une sauvegarde durable pour un espace de clés etcd. En prenant des instantanés périodiques de la base de données backend d'un membre etcd, un cluster `etcd` peut être restauré à un instant donné dans un état connu comme étant valide.

Un instantané est pris avec `etcdctl` :

```sh
$ etcdctl snapshot save backup.db
$ etcdutl --write-out=table snapshot status backup.db
+----------+----------+------------+------------+
|   HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
+----------+----------+------------+------------+
| fe01cf57 |       10 |          7 | 2.1 MB     |
+----------+----------+------------+------------+
```
