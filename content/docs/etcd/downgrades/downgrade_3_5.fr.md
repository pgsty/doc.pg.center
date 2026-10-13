---
title: "Rétrogradation d'etcd de la version 3.5 à la 3.4"
weight: 6700
description: "Processus, listes de vérification et notes sur la rétrogradation d'etcd de la version 3.5 à la 3.4"
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/downgrades/downgrade_3_5.md"
aliases: [/etcd/downgrades/downgrade_3_5/]
---

Dans le cas général, la rétrogradation d'etcd 3.5 vers 3.4 peut s'effectuer sans interruption de service, en mode rolling :

-  un par un, arrêtez les processus etcd 3.5 et remplacez-les par des processus etcd 3.4
-  dès le démarrage d’un processus 3.4, les nouvelles fonctionnalités de 3.5 ne sont plus disponibles pour le cluster

Avant de [commencer la rétrogradation](#downgrade-procedure), lisez le reste du présent guide afin de vous préparer.

### Listes de vérification pour la rétrogradation {#downgrade-checklists}

> [!WARNING]
> Si votre cluster a activé l'authentification, la rétrogradation progressive depuis la version 3.5 n'est pas prise en charge, car la version 3.5 [modifie le format des entrées WAL liées à l'authentification](https://github.com/etcd-io/etcd/pull/11943). Vous pouvez suivre les [instructions d'authentification](/fr/docs/etcd/op-guide/authentication/rbac/) pour désactiver l'authentification, puis supprimer tous les utilisateurs.

Principaux changements avec rupture de compatibilité entre 3.5 et 3.4 :

#### Différence entre les drapeaux {#difference-in-flags}

Si vous utilisez l'un des drapeaux suivants dans vos configurations 3.5, veillez à les supprimer, les renommer ou modifier leur valeur par défaut lors de la rétrogradation vers la version 3.4.

> [!NOTE]
> La différence est basée sur les versions 3.5.14 et 3.4.33. La différence réelle dépend de votre version de correctif ; vérifiez d'abord avec `diff <(etcd-3.5/bin/etcd -h | grep \\-\\-) <(etcd-3.4/bin/etcd -h | grep \\-\\-)`.

```diff
# flags not available in 3.4
-etcd --socket-reuse-port
-etcd --socket-reuse-address
-etcd --raft-read-timeout
-etcd --raft-write-timeout
-etcd --v2-deprecation
-etcd --client-cert-file
-etcd --client-key-file
-etcd --peer-client-cert-file
-etcd --peer-client-key-file
-etcd --self-signed-cert-validity
-etcd --enable-log-rotation --log-rotation-config-json=some.json
-etcd --experimental-enable-distributed-tracing --experimental-distributed-tracing-address='localhost:4317' --experimental-distributed-tracing-service-name='etcd' --experimental-distributed-tracing-instance-id='' --experimental-distributed-tracing-sampling-rate='0'
-etcd --experimental-compact-hash-check-enabled --experimental-compact-hash-check-time='1m'
-etcd --experimental-downgrade-check-time
-etcd --experimental-memory-mlock
-etcd --experimental-txn-mode-write-with-shared-buffer
-etcd --experimental-bootstrap-defrag-threshold-megabytes
-etcd --experimental-stop-grpc-service-on-defrag

# same flag with different names
-etcd --backend-bbolt-freelist-type=map
+etcd --experimental-backend-bbolt-freelist-type=array

# same flag different defaults
-etcd --pre-vote=true
+etcd --pre-vote=false

-etcd --logger=zap
+etcd --logger=capnslog
```

#### `etcd --logger zap` {#etcd---logger-zap}

3.4 utilise par défaut `--logger=capnslog` tandis que 3.5 utilise par défaut `--logger=zap`.

Si vous souhaitez continuer à utiliser `zap`, il doit être spécifié explicitement.

```diff
+etcd --logger=zap --log-outputs=stderr

+# to write logs to stderr and a.log file at the same time
+etcd --logger=zap --log-outputs=stderr,a.log
```

#### Différence entre les métriques Prometheus {#difference-in-prometheus-metrics}

```diff
# metrics not available in 3.4
-etcd_debugging_mvcc_db_compaction_last
```

### Liste de vérification pour la rétrogradation du serveur {#server-downgrade-checklists}

#### Exigences de rétrogradation {#downgrade-requirements}

Pour garantir une rétrogradation progressive sans incident, le cluster en cours d'exécution doit être sain. Vérifiez l'état du cluster à l'aide de la commande `etcdctl endpoint health` avant de poursuivre.

La version 3.4 vers laquelle effectuer la rétrogradation doit être supérieure ou égale à 3.4.32.

#### Préparation {#preparation}

Avant de rétrograder etcd, testez toujours les services dépendants d’etcd dans un environnement de préproduction avant de déployer la mise à jour vers l’environnement de production.

Avant de commencer, [téléchargez la sauvegarde d'instantané](/fr/docs/etcd/op-guide/maintenance/#snapshot-backup). Si une erreur survient lors de la rétrogradation, il sera possible d'utiliser cette sauvegarde pour [annuler](#rollback) la mise à jour et revenir à la version etcd existante. Veuillez noter que la commande `snapshot` ne sauvegarde que les données v3. Pour les données v2, consultez [sauvegarde du magasin de données v2](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore).

Avant de commencer, téléchargez la dernière version d’etcd 3.4, et vérifiez que sa version est supérieure ou égale à 3.4.32.

#### Versions mixtes {#mixed-versions}

Lors d'une opération de rétrogradation, un cluster etcd prend en charge des versions mixtes de membres et fonctionne selon le protocole de la version commune la plus basse. Le cluster est considéré comme rétrogradé dès qu’un de ses membres est rétrogradé à la version 3.4. En interne, les membres etcd négocient entre eux afin de déterminer la version globale du cluster, qui détermine la version signalée et les fonctionnalités prises en charge.

#### Limitations {#limitations}

Note : Si le cluster ne contient que des données v3 et aucune donnée v2, il n'est pas soumis à cette limitation.

Si le cluster sert un jeu de données v2 d'une taille supérieure à 50 Mo, chaque membre nouvellement rétrogradé peut prendre jusqu'à deux minutes pour se synchroniser avec le cluster existant. Vérifiez la taille d'un instantané récent afin d'estimer la taille totale des données. Autrement dit, le plus sûr est d'attendre deux minutes entre chaque rétrogradation de membre.

Pour une taille totale de données bien plus importante, de 100 Mo ou plus, ce processus unique peut prendre encore plus de temps. Les administrateurs de clusters etcd très volumineux de cette ampleur peuvent librement contacter l'équipe [etcd][etcd-contact] avant la rétrogradation, et nous serons heureux de leur fournir des conseils sur la procédure.

#### Retour en arrière {#rollback}

Si un membre a été rétrogradé à la version 3.4, la version du cluster sera rétrogradée à 3.4, et les opérations seront compatibles avec "3.4". Vous devrez suivre les instructions [Mettre à jour etcd de 3.4 vers 3.5](/fr/docs/etcd/upgrades/upgrade_3_5/) pour effectuer un retour en arrière.

Veuillez [télécharger la sauvegarde d'instantané](/fr/docs/etcd/op-guide/maintenance/#snapshot-backup) afin de permettre la remontée du cluster, même après qu'il ait été entièrement rétrogradé.

### Procédure de rétrogradation {#downgrade-procedure}

Cet exemple montre comment effectuer une rétrogradation d’un cluster etcd 3.5 composé de 3 membres, en cours d’exécution sur une machine locale.

#### Étape 1 : vérifier les conditions de rétrogradation {#step-1-check-downgrade-requirements}

Le cluster est-il sain et en cours d'exécution avec la version 3.5.x ?

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 2.118638ms
localhost:22379 is healthy: successfully committed proposal: took = 3.631388ms
localhost:32379 is healthy: successfully committed proposal: took = 2.157051ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.5.0","etcdcluster":"3.5.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.5.0","etcdcluster":"3.5.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.5.0","etcdcluster":"3.5.0"}
COMMENT
```

#### Étape 2 : télécharger la sauvegarde d'instantané depuis le leader {#step-2-download-snapshot-backup-from-leader}

[Téléchargez l'instantané de sauvegarde](/fr/docs/etcd/op-guide/maintenance/#snapshot-backup) afin de pouvoir annuler cette rétrogradation et restaurer l’état antérieur en cas de problème.

#### Étape 3 : arrêter un serveur etcd existant {#step-3-stop-one-existing-etcd-server}

Avant d'arrêter le serveur, vérifiez s'il est leader

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
|    ENDPOINT     |        ID        | VERSION | DB SIZE | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS |
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
|  localhost:2379 | 8211f1d0f64f3269 |  3.5.13 |   20 kB |      true |      false |         2 |          9 |                  9 |        |
| localhost:22379 | 91bc3c398fb3c146 |  3.5.13 |   20 kB |     false |      false |         2 |          9 |                  9 |        |
| localhost:32379 | fd422379fda50e48 |  3.5.13 |   20 kB |     false |      false |         2 |          9 |                  9 |        |
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
COMMENT
```

Si le serveur à arrêter est le leader, vous pouvez réduire la durée d'indisponibilité en transférant le rôle de leader vers un autre serveur avec `move-leader` avant d'arrêter ce serveur.

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 move-leader 91bc3c398fb3c146

etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
|    ENDPOINT     |        ID        | VERSION | DB SIZE | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS |
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
|  localhost:2379 | 8211f1d0f64f3269 |  3.5.13 |   20 kB |     false |      false |         3 |         11 |                 11 |        |
| localhost:22379 | 91bc3c398fb3c146 |  3.5.13 |   20 kB |      true |      false |         3 |         11 |                 11 |        |
| localhost:32379 | fd422379fda50e48 |  3.5.13 |   20 kB |     false |      false |         3 |         11 |                 11 |        |
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
COMMENT
```

Lorsque chaque processus etcd est arrêté, les autres membres du cluster enregistrent des erreurs attendues. Cela est normal, car la connexion avec un membre du cluster a été (temporairement) interrompue :

```bash
{"level":"info","ts":"2024-05-14T20:25:47.051124Z","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"91bc3c398fb3c146 became leader at term 3"}
{"level":"info","ts":"2024-05-14T20:25:47.051139Z","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"raft.node: 91bc3c398fb3c146 elected leader 91bc3c398fb3c146 at term 3"}

^C{"level":"warn","ts":"2024-05-14T20:27:09.094119Z","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"91bc3c398fb3c146","remote-peer-id":"8211f1d0f64f3269","error":"EOF"}
{"level":"warn","ts":"2024-05-14T20:27:09.09427Z","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"91bc3c398fb3c146","remote-peer-id":"8211f1d0f64f3269","error":"EOF"}
{"level":"warn","ts":"2024-05-14T20:27:09.095535Z","caller":"rafthttp/peer_status.go:66","msg":"peer became inactive (message send to peer failed)","peer-id":"8211f1d0f64f3269","error":"failed to dial 8211f1d0f64f3269 on stream MsgApp v2 (peer 8211f1d0f64f3269 failed to find local node 91bc3c398fb3c146)"}
{"level":"warn","ts":"2024-05-14T20:27:09.43915Z","caller":"rafthttp/stream.go:223","msg":"lost TCP streaming connection with remote peer","stream-writer-type":"stream Message","local-member-id":"91bc3c398fb3c146","remote-peer-id":"8211f1d0f64f3269"}
{"level":"warn","ts":"2024-05-14T20:27:11.085646Z","caller":"etcdserver/cluster_util.go:294","msg":"failed to reach the peer URL","address":"http://127.0.0.1:12380/version","remote-member-id":"8211f1d0f64f3269","error":"Get \"http://127.0.0.1:12380/version\": dial tcp 127.0.0.1:12380: connect: connection refused"}
{"level":"warn","ts":"2024-05-14T20:27:11.085718Z","caller":"etcdserver/cluster_util.go:158","msg":"failed to get version","remote-member-id":"8211f1d0f64f3269","error":"Get \"http://127.0.0.1:12380/version\": dial tcp 127.0.0.1:12380: connect: connection refused"}
{"level":"warn","ts":"2024-05-14T20:27:13.557385Z","caller":"rafthttp/probing_status.go:68","msg":"prober detected unhealthy status","round-tripper-name":"ROUND_TRIPPER_SNAPSHOT","remote-peer-id":"8211f1d0f64f3269","rtt":"416.079µs","error":"dial tcp 127.0.0.1:12380: connect: connection refused"}
```

#### Étape 4 : redémarrer le serveur etcd avec la même configuration + `--next-cluster-version-compatible` {#step-4-restart-the-etcd-server-with-same-configuration----next-cluster-version-compatible}

Redémarrez le serveur etcd avec la même configuration, mais avec le nouveau binaire etcd et `--next-cluster-version-compatible`.

```diff
-etcd-3.5/bin --name s1 \
+etcd-3.4/bin --name s1 \
  --data-dir /tmp/etcd/s1 \
  --listen-client-urls http://localhost:2379 \
  --advertise-client-urls http://localhost:2379 \
  --listen-peer-urls http://localhost:2380 \
  --initial-advertise-peer-urls http://localhost:2380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:22380,s3=http://localhost:32380 \
  --initial-cluster-token tkn \
  --initial-cluster-state existing
  --next-cluster-version-compatible
```

Le nouvel etcd 3.4 publiera ses informations dans le cluster. À ce stade, le cluster commencera à fonctionner selon le protocole 3.4, qui constitue la version commune la plus basse.

```bash
> `{"level":"info","ts":"2024-05-13T21:05:43.981445Z","caller":"membership/cluster.go:561","msg":"set initial cluster version","cluster-id":"ef37ad9dc622a7c4","local-member-id":"8211f1d0f64f3269","cluster-version":"3.0"}`

> `{"level":"info","ts":"2024-05-13T21:05:43.982188Z","caller":"api/capability.go:77","msg":"enabled capabilities for version","cluster-version":"3.0"}`

> `{"level":"info","ts":"2024-05-13T21:05:43.982312Z","caller":"membership/cluster.go:549","msg":"updated cluster version","cluster-id":"ef37ad9dc622a7c4","local-member-id":"8211f1d0f64f3269","from":"3.0","from":"3.5"}`

> `{"level":"info","ts":"2024-05-13T21:05:43.982376Z","caller":"api/capability.go:77","msg":"enabled capabilities for version","cluster-version":"3.5"}`

> `{"level":"info","ts":"2024-05-13T21:05:44.000672Z","caller":"etcdserver/server.go:2152","msg":"published local member to cluster through raft","local-member-id":"8211f1d0f64f3269","local-member-attributes":"{Name:infra1 ClientURLs:[http://127.0.0.1:2379]}","request-path":"/0/members/8211f1d0f64f3269/attributes","cluster-id":"ef37ad9dc622a7c4","publish-timeout":"7s"}`

> `{"level":"info","ts":"2024-05-13T21:05:46.452631Z","caller":"membership/cluster.go:549","msg":"updated cluster version","cluster-id":"ef37ad9dc622a7c4","local-member-id":"8211f1d0f64f3269","from":"3.5","from":"3.4"}`
```

Vérifiez que chaque membre, puis l’intégralité du cluster, deviennent sains avec le nouveau binaire etcd 3.4 :

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:32379 is healthy: successfully committed proposal: took = 2.337471ms
localhost:22379 is healthy: successfully committed proposal: took = 1.130717ms
localhost:2379 is healthy: successfully committed proposal: took = 2.124843ms
COMMENT
```

Les membres non rétrogradés enregistreront des informations semblables aux suivantes

```bash
{"level":"info","ts":"2024-05-13T21:05:46.450764Z","caller":"etcdserver/server.go:2633","msg":"updating cluster version using v2 API","from":"3.5","to":"3.4"}
{"level":"info","ts":"2024-05-13T21:05:46.452419Z","caller":"membership/cluster.go:576","msg":"updated cluster version","cluster-id":"ef37ad9dc622a7c4","local-member-id":"91bc3c398fb3c146","from":"3.5","to":"3.4"}
{"level":"info","ts":"2024-05-13T21:05:46.452547Z","caller":"etcdserver/server.go:2652","msg":"cluster version is updated","cluster-version":"3.4"}
```

#### Étape 5 : répéter l'*étape 3* et l'*étape 4* pour les membres restants {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

Lorsque tous les membres sont rétrogradés, vérifiez l’état de santé et la version du cluster :

```bash
endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 492.834µs
localhost:22379 is healthy: successfully committed proposal: took = 1.015025ms
localhost:32379 is healthy: successfully committed proposal: took = 1.853077ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.4.32","etcdcluster":"3.4.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.4.32","etcdcluster":"3.4.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.4.32","etcdcluster":"3.4.0"}
COMMENT
```

[etcd-contact]: https://groups.google.com/g/etcd-dev
