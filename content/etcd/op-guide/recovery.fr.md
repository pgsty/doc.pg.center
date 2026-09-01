---
title: Récupération après sinistre
weight: 4275
description: "etcd Fonctionnalités d'instantané et de restauration v3"
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/op-guide/recovery.md"
---

etcd est conçu pour résister aux pannes de machines. Un cluster etcd se rétablit automatiquement après des pannes temporaires (par exemple, redémarrages de machine) et tolère jusqu'à *(N-1)/2* pannes permanentes pour un cluster composé de N membres. Lorsqu'un membre subit une panne permanente, qu'elle soit due à une défaillance matérielle ou à une corruption du disque, il perd accès au cluster. Si le cluster perd définitivement plus de *(N-1)/2* membres, il subit une panne catastrophique, perdant irrévocablement son quorum. Une fois le quorum perdu, le cluster ne peut plus atteindre de consensus et ne peut donc plus accepter de mises à jour.

Pour récupérer après une panne catastrophique, etcd v3 fournit des fonctionnalités d'instantané et de restauration afin de recréer le cluster sans perte de données clés v3. Pour récupérer les clés v2, reportez-vous au [guide d'administration v2][v2_recover].

[v2_recover]: https://etcd.io/docs/v2.3/admin_guide#disaster-recovery

## Instantané de l'espace de clés {#snapshotting-the-keyspace}

La récupération d’un cluster nécessite tout d’abord un instantané de l’espace de clés provenant d’un membre etcd. Un instantané peut être pris à partir d’un membre en cours d’exécution à l’aide de la commande `etcdctl snapshot save` ou en copiant le fichier `member/snap/db` depuis un répertoire de données etcd. Par exemple, la commande suivante crée un instantané de l’espace de clés servi par `$ENDPOINT` dans le fichier `snapshot.db` :

```sh
$ ETCDCTL_API=3 etcdctl --endpoints $ENDPOINT snapshot save snapshot.db
```

Notez qu’effectuer l’instantané à partir du fichier `member/snap/db` peut entraîner la perte de données non encore écrites, mais présentes dans le répertoire wal (write-ahead-log).

## État d’un instantané {#status-of-a-snapshot}

Pour comprendre quelle révision et quel hachage contient un instantané donné, vous pouvez utiliser la commande `etcdutl snapshot status` :

```sh
$ etcdutl snapshot status snapshot.db -w table
+---------+----------+------------+------------+
|  HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
+---------+----------+------------+------------+
| 7ef846e |   485261 |      11642 |      94 MB |
+---------+----------+------------+------------+
```

## Restauration d’un cluster {#restoring-a-cluster}

### Différence de révision {#revision-difference}

Lorsque vous restaurez un cluster, les clients existants peuvent percevoir une révision qui remonte de plusieurs centaines ou milliers d'unités. Cela est dû au fait qu’un instantané donné ne contient que l'historique des données jusqu’au moment où il a été pris, alors que l’état actuel du cluster peut déjà être plus avancé.

Cela pose particulièrement problème lors de l'exécution de Kubernetes avec etcd, où les contrôleurs et les opérateurs peuvent utiliser ce qu'on appelle `informers`, qui agissent comme des caches locaux et reçoivent des notifications de mise à jour via des surveillance. Le retour à une révision antérieure peut ne pas actualiser correctement ces caches, entraînant un comportement imprévisible et incohérent dans les contrôleurs.

Lors de la restauration à partir d’un instantané dans le cadre de : consommateurs connus de l’API de surveillance, copies locales mises en cache des données etcd ou de l’utilisation générale de Kubernetes, il est fortement recommandé de procéder à la restauration en utilisant les « augmentations de révision » ci-dessous.

### Restauration à partir d’un instantané {#restoring-from-snapshot}

Pour restaurer un cluster, il suffit d’un seul fichier d’instantané « db ». La restauration d’un cluster avec `etcdutl snapshot restore` crée de nouveaux répertoires de données etcd ; tous les membres doivent restaurer à l’aide du même instantané. La restauration écrase certaines métadonnées de l’instantané (en particulier l’ID de membre et l’ID de cluster) ; le membre perd alors son identité antérieure. Cette écrasement des métadonnées empêche le nouveau membre de rejoindre involontairement un cluster existant. Par conséquent, pour démarrer un cluster à partir d’un instantané, la restauration doit démarrer un nouveau cluster logique.

Une restauration simple peut être exécutée comme suit :

```sh
$ etcdutl snapshot restore snapshot.db --data-dir output-dir
```

### Vérifications d'intégrité {#integrity-checks}

L'intégrité de l'instantané peut être vérifiée de manière facultative au moment de la restauration. Si l'instantané est pris avec `etcdctl snapshot save`, il contient un hachage d'intégrité qui est vérifié par `etcdutl snapshot restore`. Si l'instantané est copié depuis le répertoire de données, aucun hachage d'intégrité n'est présent, et sa restauration ne sera possible qu'en utilisant `--skip-hash-check`.


### Restauration avec augmentation de la révision {#restoring-with-revision-bump}

Afin de garantir que les révisions ne diminuent jamais après une restauration, vous pouvez utiliser l'option `--bump-revision`. Cette option prend un entier sur 64 bits, qui indique le nombre de révisions à ajouter à la révision actuelle de l'instantané. Étant donné qu'une écriture dans etcd augmente la révision de un, vous pouvez couvrir un instantané datant d'une semaine en augmentant la révision de 1'000'000'000, à condition que etcd fonctionne avec moins de 1500 écritures par seconde.

Dans le contexte des contrôleurs Kubernetes, il est également important de marquer toutes les révisions, y compris la mise à jour, comme compactées à l’aide de `--mark-compacted`. Cela garantit que toutes les surveillance sont terminées et qu’etcd ne répond pas aux requêtes concernant les révisions survenues après la prise de l’instantané — ce qui invalide effectivement les caches d’informateurs.

Un appel complet peut avoir l'aspect suivant :

```sh
$ etcdutl snapshot restore snapshot.db --bump-revision 1000000000 --mark-compacted --data-dir output-dir
```

### Restauration avec membre mis à jour {#restoring-with-updated-membership}

Les membres d’un cluster etcd sont stockés dans etcd lui-même et maintenus grâce à l'algorithme de consensus Raft. Lorsque le quorum est entièrement perdu, vous devrez peut-être reconsidérer l'emplacement et la manière dont le nouveau cluster est constitué, par exemple sur un ensemble entièrement nouveau de membres.

Lors de la restauration à partir d’un instantané, vous pouvez fournir directement la nouvelle configuration d’appartenance dans la base de données comme suit :

```sh
$ etcdutl snapshot restore snapshot.db \
  --name m1 \
  --data-dir m1.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host1:2380
```

Cela garantit que le cluster nouvellement construit ne se connecte qu'aux autres membres restaurés ayant le jeton donné, et non aux membres plus anciens qui pourraient encore être actifs et tenter de se connecter.

En revanche, lors du démarrage d’etcd, vous pouvez fournir `--force-new-cluster` afin de remplacer l’appartenance au cluster tout en conservant les données d’application existantes. Notez que cette opération est fortement déconseillée, car elle provoquera un arrêt brutal si d’autres membres du cluster précédent sont encore actifs. Veillez à sauvegarder régulièrement des instantanés.


### Exemple bout en bout {#end-2-end-example}

Prenez un instantané à partir d’un cluster en cours d’exécution à l’aide de :

```sh
$ etcdctl snapshot save snapshot.db
```

En continuant de l'exemple précédent, la commande suivante crée de nouveaux répertoires de données etcd (`m1.etcd`, `m2.etcd`, `m3.etcd`) pour un cluster à trois membres :

```sh
$ etcdutl snapshot restore snapshot.db \
  --name m1 \
  --data-dir m1_data_dir.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host1:2380
$ etcdutl snapshot restore snapshot.db \
  --name m2 \
  --data-dir m2_data_dir.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host2:2380
$ etcdutl snapshot restore snapshot.db \
  --name m3 \
  --data-dir m3_data_dir.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host3:2380
```

Ensuite, démarrez `etcd` avec les nouveaux répertoires de données :

```sh
$ etcd \
  --name m1 \
  --data-dir m1_data_dir.etcd \
  --listen-client-urls http://host1:2379 \
  --advertise-client-urls http://host1:2379 \
  --listen-peer-urls http://host1:2380 &
$ etcd \
  --name m2 \
  --data-dir m2_data_dir.etcd \
  --listen-client-urls http://host2:2379 \
  --advertise-client-urls http://host2:2379 \
  --listen-peer-urls http://host2:2380 &
$ etcd \
  --name m3 \
  --data-dir m3_data_dir.etcd \
  --listen-client-urls http://host3:2379 \
  --advertise-client-urls http://host3:2379 \
  --listen-peer-urls http://host3:2380 &
```

Le cluster etcd restauré doit maintenant être disponible et servir l’espace de clés depuis l’instantané.

À partir de etcd v3.6, les utilisateurs ne peuvent utiliser que `etcdctl` pour créer un instantané des données, mais doivent utiliser `etcdutl` pour restaurer les données à partir d’un instantané. Si `--data-dir` n’est pas spécifié, la valeur par défaut de `--data-dir` est `<name>.etcd` (où `<name>` correspond à la valeur de `--name`). Par exemple, si `--data-dir` n’a pas été fourni et que les membres sont nommés `m1`, `m2` et `m3`, les répertoires `--data-dir` seront `m1.etcd`, `m2.etcd` et `m3.etcd`.
