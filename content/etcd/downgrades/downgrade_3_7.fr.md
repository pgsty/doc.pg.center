---
title: "Rétrogradation d'etcd de la version v3.7 à la v3.6"
weight: 6600
description: "Processus, listes de vérification et notes sur la rétrogradation d'etcd de la version 3.7 à la version 3.6"
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/downgrades/downgrade_3_7.md"
---

Dans le cas général, la rétrogradation d'etcd v3.7 vers v3.6 peut se faire sans interruption de service, par mise à jour progressive :

-  un à un, arrêtez les processus etcd v3.7 et remplacez-les par des processus etcd v3.6
-  après avoir activé la rétrogradation, les nouvelles fonctionnalités de la v3.7 ne sont plus disponibles pour le cluster

Avant de [commencer la rétrogradation](#downgrade-procedure), lisez le reste du présent guide afin de vous préparer.

### Listes de vérification pour la rétrogradation {#downgrade-checklists}

Différences notables entre v3.7 et v3.6 :

#### Différence entre les drapeaux {#difference-in-flags}

La version 3.7 n'introduit aucune nouvelle option, aussi un processus v3.6 accepte toutes les options d'une configuration v3.7, et aucune modification de configuration n'est requise lors d'une rétrogradation.

> [!NOTE]
> La différence est basée sur les versions v3.7.0-rc.0 et v3.6.13. La différence réelle dépendra de votre version de correctif ; vérifiez d'abord avec `diff <(etcd-3.7/bin/etcd -h | grep \\-\\-) <(etcd-3.6/bin/etcd -h | grep \\-\\-)`.

Les indicateurs `--experimental-*` obsolètes, supprimés à partir de la version v3.7, existent encore dans la version v3.6, mais ne les réajoutez pas après une rétrogradation ; utilisez leurs équivalents non expérimentaux ou les entrées `--feature-gates`, qui fonctionnent sur les deux versions.

#### Différence entre les métriques Prometheus {#difference-in-prometheus-metrics}

```diff
# metrics not available in v3.6
-etcd_server_request_duration_seconds
-etcd_debugging_server_watch_send_loop_control_stream_duration_seconds
-etcd_debugging_server_watch_send_loop_progress_duration_seconds
-etcd_debugging_server_watch_send_loop_watch_stream_duration_seconds
-etcd_debugging_server_watch_send_loop_watch_stream_duration_per_event_seconds
```

### Liste de vérification pour la rétrogradation du serveur {#server-downgrade-checklists}

#### Exigences de rétrogradation {#downgrade-requirements}

Pour garantir une rétrogradation progressive sans incident, le cluster en cours d'exécution doit être sain. Vérifiez l'état du cluster à l'aide de la commande `etcdctl endpoint health` avant de poursuivre.

#### Préparation {#preparation}

Avant de rétrograder etcd, testez toujours les services dépendants d’etcd dans un environnement de préproduction avant de déployer la mise à jour vers l’environnement de production.

Avant de commencer, [téléchargez l'instantané de sauvegarde](/fr/etcd/op-guide/maintenance/#snapshot-backup). Si une erreur survient lors de la rétrogradation, il sera possible d'utiliser cette sauvegarde pour [annuler](#rollback) la mise à jour et revenir à la version existante d'etcd.

Avant de commencer, téléchargez la dernière version d'etcd v3.6.

#### Versions mixtes {#mixed-versions}

Lors d'une rétrogradation, un cluster etcd prend en charge des versions mixtes de membres et fonctionne selon le protocole de la version commune la plus basse. Le cluster est considéré comme rétrogradé une fois que la rétrogradation est activée par `etcdctl downgrade enable 3.6`. En interne, la version globale du cluster est définie sur la version cible de la rétrogradation, ce qui contrôle la version signalée et les fonctionnalités prises en charge.

#### Retour en arrière {#rollback}

Avant de procéder à la rétrogradation de votre cluster etcd, créez et [téléchargez une sauvegarde sous forme d'instantané](/fr/etcd/op-guide/maintenance/#snapshot-backup) de votre cluster etcd. Cet instantané peut être utilisé pour restaurer le cluster dans son état antérieur à la rétrogradation, le cas échéant. Si des utilisateurs rencontrent des problèmes pendant la rétrogradation, ils doivent d'abord identifier et résoudre la cause racine.

Si la rétrogradation a commencé après l'exécution de `etcdctl downgrade enable`, et que le cluster est toujours dans un état de version mixte, où au moins un membre reste sur la version v3.7, les utilisateurs peuvent annuler le processus de rétrogradation en cours en exécutant `etcdctl downgrade cancel`, puis en redémarrant tous les membres rétrogradés avec les binaires d'origine v3.7.

Une fois que tous les membres ont été rétrogradés vers la version v3.6, le cluster est considéré comme entièrement rétrogradé. Si les utilisateurs souhaitent revenir à la version d'origine après avoir achevé une rétrogradation complète, ils doivent suivre le guide officiel de [mise à jour](/fr/etcd/upgrades/upgrade_3_7/) afin d'assurer la cohérence et d'éviter toute corruption des données.

### Procédure de rétrogradation {#downgrade-procedure}

Cet exemple montre comment effectuer une rétrogradation d’un cluster etcd à 3 membres en version v3.7, exécuté sur une machine locale. La sortie ci-dessous provient d’une exécution réelle contre etcd v3.7.0-rc.0 et etcd v3.6.13 sur un seul hôte, utilisant trois ports de bouclage, sur un cluster qui a été mis à jour depuis v3.6.13 peu de temps auparavant.

#### Étape 1 : vérifier les conditions de rétrogradation {#step-1-check-downgrade-requirements}

Le cluster est-il sain et en cours d'exécution sous la version 3.7.x ?

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 1.052416ms
localhost:32379 is healthy: successfully committed proposal: took = 1.11625ms
localhost:22379 is healthy: successfully committed proposal: took = 1.114291ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.7.0-rc.0","etcdcluster":"3.7.0","storage":"3.7.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.7.0-rc.0","etcdcluster":"3.7.0","storage":"3.7.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.7.0-rc.0","etcdcluster":"3.7.0","storage":"3.7.0"}
COMMENT

etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |  VERSION   | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 | 3.7.0-rc.0 |           3.7.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         5 |         20 |                 20 |        |                          |             false |
| localhost:22379 | 729934363faa4a24 | 3.7.0-rc.0 |           3.7.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         20 |                 20 |        |                          |             false |
| localhost:32379 |  b548c2511513015 | 3.7.0-rc.0 |           3.7.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         20 |                 20 |        |                          |             false |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

#### Étape 2 : télécharger la sauvegarde d'instantané depuis le leader {#step-2-download-snapshot-backup-from-leader}

[Téléchargez l'instantané de sauvegarde](/fr/etcd/op-guide/maintenance/#snapshot-backup) afin de pouvoir annuler cette rétrogradation et restaurer l’état antérieur en cas de problème :

```bash
etcdctl --endpoints=localhost:2379 snapshot save backup.db
<<COMMENT
{"level":"info","ts":"2026-07-02T06:48:11.091982+0300","caller":"snapshot/v3_snapshot.go:83","msg":"created temporary db file","path":"backup.db.part"}
{"level":"info","ts":"2026-07-02T06:48:11.092253+0300","logger":"client","caller":"v3/maintenance.go:236","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":"2026-07-02T06:48:11.099884+0300","caller":"snapshot/v3_snapshot.go:96","msg":"fetching snapshot","endpoint":"localhost:2379"}
{"level":"info","ts":"2026-07-02T06:48:11.100394+0300","logger":"client","caller":"v3/maintenance.go:302","msg":"completed snapshot read; closing"}
{"level":"info","ts":"2026-07-02T06:48:11.103116+0300","caller":"snapshot/v3_snapshot.go:111","msg":"fetched snapshot","endpoint":"localhost:2379","size":"98 kB","took":"10.9815ms","etcd-version":"3.7.0"}
{"level":"info","ts":"2026-07-02T06:48:11.103296+0300","caller":"snapshot/v3_snapshot.go:121","msg":"saved","path":"backup.db"}
Snapshot saved at backup.db
Server version 3.7.0
COMMENT
```

#### Étape 3 : valider la version cible de la rétrogradation {#step-3-validate-downgrade-target-version}

Validez la version cible de la rétrogradation avant d’activer la rétrogradation :

- Nous ne prenons en charge la rétrogradation que d'une version mineure à la fois. Par exemple, la rétrogradation de la version v3.7 vers la v3.5 n'est pas autorisée.
- Veuillez ne pas passer à l'étape suivante tant que la validation n'est pas réussie.

```bash
etcdctl downgrade validate 3.6
<<COMMENT
Downgrade validate success, cluster version 3.7
COMMENT
```

#### Étape 4 : activer la rétrogradation {#step-4-enable-downgrade}

```bash
etcdctl downgrade enable 3.6
<<COMMENT
Downgrade enable success, cluster version 3.7
COMMENT
```

Après avoir activé la rétrogradation, le cluster commencera à fonctionner avec le protocole v3.6, qui est la version cible de la rétrogradation. En outre, etcd migrera automatiquement le schéma vers la version cible de la rétrogradation, ce qui se produit généralement très rapidement. Vérifiez que la version de stockage de tous les serveurs a bien été migrée vers la v3.6 en consultant l’état des points de terminaison avant de passer à l’étape suivante.

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |  VERSION   | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         5 |         22 |                 22 |        |                    3.6.0 |              true |
| localhost:22379 | 729934363faa4a24 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         22 |                 22 |        |                    3.6.0 |              true |
| localhost:32379 |  b548c2511513015 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         22 |                 22 |        |                    3.6.0 |              true |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

> [!NOTE]
> Une fois la rétrogradation activée, le cluster continuera à fonctionner avec le protocole v3.6, même si tous les serveurs exécutent encore le binaire v3.7, à moins que la rétrogradation ne soit annulée à l’aide de `etcdctl downgrade cancel`

#### Étape 5 : arrêter un serveur etcd existant {#step-5-stop-one-existing-etcd-server}

Avant d'arrêter le serveur, vérifiez s'il est le leader. Nous recommandons de rétrograder le leader en dernier. Si le serveur à arrêter est le leader, vous pouvez réduire une partie de la durée d'indisponibilité en transférant le rôle de leader vers un autre serveur avec `move-leader` avant d'arrêter ce serveur.

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 move-leader 729934363faa4a24
<<COMMENT
Leadership transferred from 7339c4e5e833c029 to 729934363faa4a24
COMMENT
```

Lorsque chaque processus etcd est arrêté, les autres membres du cluster enregistrent des erreurs attendues. Cela est normal, car la connexion avec un membre du cluster a été (temporairement) interrompue :

```bash
{"level":"warn","ts":"2026-07-02T06:48:14.518460+0300","caller":"rafthttp/stream.go:227","msg":"lost TCP streaming connection with remote peer","stream-writer-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":"2026-07-02T06:48:15.913169+0300","caller":"etcdserver/cluster_util.go:261","msg":"failed to reach the peer URL","address":"http://localhost:22380/version","remote-member-id":"729934363faa4a24","error":"Get \"http://localhost:22380/version\": dial tcp [::1]:22380: connect: connection refused"}
{"level":"warn","ts":"2026-07-02T06:48:15.913364+0300","caller":"etcdserver/cluster_util.go:162","msg":"failed to get version","remote-member-id":"729934363faa4a24","error":"Get \"http://localhost:22380/version\": dial tcp [::1]:22380: connect: connection refused"}
{"level":"warn","ts":"2026-07-02T06:48:16.856521+0300","caller":"version/monitor.go:212","msg":"remotes server has mismatching etcd version","remote-member-id":"b548c2511513015","current-server-version":"3.7.0","target-version":"3.6.0"}
```

#### Étape 6 : redémarrer le serveur etcd avec la même configuration {#step-6-restart-the-etcd-server-with-same-configuration}

Redémarrez le serveur etcd avec la même configuration, mais en utilisant le binaire etcd v3.6.

```diff
-etcd-3.7/bin/etcd --name s2 \
+etcd-3.6/bin/etcd --name s2 \
  --data-dir /tmp/etcd/s2 \
  --listen-client-urls http://localhost:22379 \
  --advertise-client-urls http://localhost:22379 \
  --listen-peer-urls http://localhost:22380 \
  --initial-advertise-peer-urls http://localhost:22380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:22380,s3=http://localhost:32380 \
  --initial-cluster-token tkn \
  --initial-cluster-state existing
```

Vérifiez que chaque membre, puis l’ensemble du cluster, devient sain avec le binaire etcd v3.6 :

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |  VERSION   | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         5 |         23 |                 23 |        |                    3.6.0 |              true |
| localhost:22379 | 729934363faa4a24 |     3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         23 |                 23 |        |                    3.6.0 |              true |
| localhost:32379 |  b548c2511513015 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         23 |                 23 |        |                    3.6.0 |              true |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT

etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 939.625µs
localhost:32379 is healthy: successfully committed proposal: took = 981.459µs
localhost:22379 is healthy: successfully committed proposal: took = 1.11075ms
COMMENT
```

> [!NOTE]
> Contrairement à la version 3.5, le point d'extrémité d'état de la version 3.6 indique bien les informations de rétrogradation, de sorte que les membres rétrogradés continuent à afficher `DOWNGRADE ENABLED` comme true et leur version de stockage jusqu'à la fin de la rétrogradation.

#### Étape 7 : répéter *étape 5* et *étape 6* pour les membres restants {#step-7-repeat-step-5-and-step-6-for-rest-of-the-members}

Lorsque tous les membres sont rétrogradés, la rétrogradation se termine automatiquement et `DOWNGRADE ENABLED` est réinitialisé à false. Vérifiez l'état de santé et le statut du cluster, puis confirmez que la version mineure de tous les membres et la version de stockage sont v3.6 :

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        | VERSION | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 |  3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         6 |         30 |                 30 |        |                          |             false |
| localhost:22379 | 729934363faa4a24 |  3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         6 |         30 |                 30 |        |                          |             false |
| localhost:32379 |  b548c2511513015 |  3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         6 |         30 |                 30 |        |                          |             false |
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT

etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:22379 is healthy: successfully committed proposal: took = 5.176958ms
localhost:32379 is healthy: successfully committed proposal: took = 5.177875ms
localhost:2379 is healthy: successfully committed proposal: took = 5.191625ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.6.13","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.6.13","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.6.13","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT
```

Dans le journal du leader, vous devriez être en mesure de voir un message similaire au suivant :

```bash
{"level":"info","ts":"2026-07-02T06:48:32.312205+0300","caller":"version/monitor.go:143","msg":"the cluster has been downgraded","cluster-version":"3.6.0"}
```
