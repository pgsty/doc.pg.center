---
title: Mettre à jour etcd de la version v3.6 à la version v3.7
weight: 6700
description: "Processus, listes de vérification et notes sur la mise à niveau d'etcd de v3.6 à v3.7"
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/upgrades/upgrade_3_7.md"
aliases: [/etcd/upgrades/upgrade_3_7/]
---

Dans le cas général, la mise à niveau de etcd v3.6 vers v3.7 peut être une mise à niveau progressive sans interruption de service :

-  un à un, arrêtez les processus etcd v3.6 et remplacez-les par des processus etcd v3.7
-  après avoir lancé tous les processus v3.7, les nouvelles fonctionnalités de la version v3.7 sont disponibles pour le cluster

Avant de [lancer la mise à jour](#upgrade-procedure), lisez le reste du présent guide afin de vous préparer.

### Listes de vérification pour la mise à jour {#upgrade-checklists}

#### Mise à jour 3.6 {#update-36}

> [!IMPORTANT]
> Avant de procéder à la mise à niveau vers 3.7, assurez-vous que tous vos membres 3.6 ont été mis à jour vers 3.6.11 ou une version ultérieure. Les correctifs 3.6 antérieurs peuvent ne pas être compatibles avec une mise à niveau progressive vers 3.7.

#### Magasin V2 {#v2-store}

Le magasin v2 a été entièrement supprimé dans la version 3.7. L'API HTTP v2 (`--enable-v2`), l'émission v2 sur v3 (`--experimental-enable-v2v3`), le service de découverte v2, le paquet `client/v2` et le chargement des fichiers d'instantané v2 ont tous disparu. Consultez les références aux modifications rétroactives dans [CHANGELOG-3.7](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.7.md).

Si vous effectuez une mise à jour à partir d’un cluster 3.6, ces indicateurs sont déjà absents et aucune action n’est requise. Si vous migrez depuis une version antérieure avec des données v2 personnalisées, suivez le [guide de migration v2](https://etcd.io/docs/v3.4/op-guide/v2-migration/) avant la mise à jour.

#### Refactorisation Go {#go-refactoring}

La version 3.7 contient des refontes internes importantes qui n’affectent pas les mises à jour normales, mais qui méritent d’être prises en compte lors de la mise à jour d’intégrations personnalisées :

- Migration de `gogo/protobuf` vers `google.golang.org/protobuf` standard (suivi dans [#14533](https://github.com/etcd-io/etcd/issues/14533)).
- Migration des bibliothèques de journalisation et d'étiquetage dépréciées `go-grpc-middleware` v1 vers les intercepteurs v2 ([#20420](https://github.com/etcd-io/etcd/pull/20420)).
- Les intercepteurs gRPC OpenTelemetry ont été mis à jour vers `otelgrpc` v0.61.0, remplaçant les composants dépréciés `UnaryServerInterceptor` et `StreamServerInterceptor` par `NewServerHandler` ([#20017](https://github.com/etcd-io/etcd/pull/20017)).

Si vous intégrez etcd en tant que bibliothèque, effectuez la compilation contre l'API `clientv3`, ou dépendez de packages internes, examinez le [CHANGELOG](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.7.md) avant de procéder à la mise à jour.

### Drapeaux supprimés {#flags-removed}

Toutes les options `--experimental-*` obsolètes ont été supprimées dans la version 3.7 ([#19959](https://github.com/etcd-io/etcd/pull/19959)). Dans la version 3.6, chacune de ces options a été remplacée soit par une option non expérimentale du même nom, soit par une entrée `--feature-gates`. Si vous avez encore l'une de ces options définie, remplacez-la par l'équivalent de la version 3.6 **avant** de passer à la version 3.7, sinon le processus de la version 3.7 ne pourra pas démarrer.

```diff
-etcd --experimental-bootstrap-defrag-threshold-megabytes
-etcd --experimental-compact-hash-check-enabled
-etcd --experimental-compact-hash-check-time
-etcd --experimental-compaction-batch-limit
-etcd --experimental-compaction-sleep-interval
-etcd --experimental-corrupt-check-time
-etcd --experimental-distributed-tracing-address
-etcd --experimental-distributed-tracing-instance-id
-etcd --experimental-distributed-tracing-sampling-rate
-etcd --experimental-distributed-tracing-service-name
-etcd --experimental-downgrade-check-time
-etcd --experimental-enable-distributed-tracing
-etcd --experimental-enable-lease-checkpoint
-etcd --experimental-enable-lease-checkpoint-persist
-etcd --experimental-initial-corrupt-check
-etcd --experimental-memory-mlock
-etcd --experimental-peer-skip-client-san-verification
-etcd --experimental-snapshot-catchup-entries
-etcd --experimental-stop-grpc-service-on-defrag
-etcd --experimental-txn-mode-write-with-shared-buffer
-etcd --experimental-warning-apply-duration
-etcd --experimental-warning-unary-request-duration
-etcd --experimental-watch-progress-notify-interval
```

Reportez-vous au guide de mise à jour [v3.5 vers v3.6](/fr/docs/etcd/upgrades/upgrade_3_6/) pour la correspondance de chaque indicateur supprimé vers son équivalent non expérimental ou à `--feature-gates` entrée.

### Drapeaux ajoutés {#flags-added}

Aucun.

### Drapeaux avec de nouvelles valeurs par défaut {#flags-with-new-defaults}

Aucun.

### Liste de vérification pour la mise à jour du serveur {#server-upgrade-checklists}

#### Exigences de mise à jour {#upgrade-requirements}

Pour mettre à jour un déploiement etcd existant vers la version 3.7, le cluster en cours d'exécution doit être la version 3.6.11 ou ultérieure. Si le cluster utilise une version mineure antérieure, veuillez d'abord [mettre à jour vers la version 3.6](/fr/docs/etcd/upgrades/upgrade_3_6/) ; etcd ne prend en charge la mise à jour que d'une version mineure à la fois.

En outre, pour garantir une mise à niveau progressive sans incident, le cluster en cours d'exécution doit être sain. Vérifiez l'état de santé du cluster à l'aide de la commande `etcdctl endpoint health` avant de poursuivre.

#### Préparation {#preparation}

Avant de mettre à jour etcd, testez toujours les services dépendants d’etcd dans un environnement de préproduction avant de déployer la mise à jour dans l’environnement de production.

Avant de commencer, téléchargez la sauvegarde d'instance, [instantané de sauvegarde](/fr/docs/etcd/op-guide/maintenance/#snapshot-backup). Si une erreur survient lors de la mise à jour, il sera possible d'utiliser cette sauvegarde pour [annuler](#rollback) la mise à jour et revenir à la version précédente de etcd.

#### Versions mixtes {#mixed-versions}

Lors d'une mise à jour, un cluster etcd prend en charge des versions mixtes de membres et fonctionne selon le protocole de la version commune la plus basse. Le cluster est considéré comme mis à jour uniquement lorsque tous ses membres ont été mis à jour vers la version v3.7. Internement, les membres etcd négocient entre eux afin de déterminer la version globale du cluster, qui contrôle la version signalée et les fonctionnalités prises en charge.

#### Annuler {#rollback}

Avant de mettre à jour votre cluster etcd, créez et [téléchargez une sauvegarde sous forme d'instantané](/fr/docs/etcd/op-guide/maintenance/#snapshot-backup) de votre cluster etcd. Cet instantané peut être utilisé pour restaurer le cluster dans son état antérieur à la mise à jour si nécessaire. Si des utilisateurs rencontrent des problèmes pendant la mise à jour, ils doivent d'abord identifier et résoudre la cause racine. Si le cluster est toujours dans un état mixte, où au moins un membre reste sur la version v3.6, il est possible de remplacer le binaire ou l'image par la version v3.6 antérieure, ou de restaurer directement le cluster à l'aide de l'instantané. Dans cet état mixte, le cluster continue de fonctionner en tant que cluster v3.6, permettant ainsi un retour arrière sans suivre un processus formel de rétrogradation.

Toutefois, une fois que tous les membres ont été mis à jour vers la version 3.7, le cluster est considéré comme entièrement mis à jour et la restauration à une version antérieure à l’aide des binaires n’est plus possible. Dans ce cas, les seules options de récupération sont de restaurer à partir de l’instantané pris avant la mise à jour ou de suivre le guide officiel de [désinstallation](/fr/docs/etcd/downgrades/downgrading-etcd/) en cas de problème lors de la mise à jour.

### Procédure de mise à jour {#upgrade-procedure}

Cet exemple montre comment mettre à jour un cluster etcd v3.6 composé de trois membres, exécuté sur une machine locale. La sortie ci-dessous provient d'une exécution réelle contre etcd v3.6.12 et etcd v3.7.0-rc.0 sur un hôte unique utilisant trois ports de boucle locale.

#### Étape 1 : vérifier les exigences de mise à jour {#step-1-check-upgrade-requirements}

Le cluster est-il sain et en cours d'exécution avec la version 3.6.11 ou ultérieure ?

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 7.681459ms
localhost:22379 is healthy: successfully committed proposal: took = 7.691750ms
localhost:32379 is healthy: successfully committed proposal: took = 7.698000ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.6.12","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT
```

#### Étape 2 : télécharger la sauvegarde instantané depuis le leader {#step-2-download-snapshot-backup-from-leader}

[Téléchargez l'instantané de sauvegarde](/fr/docs/etcd/op-guide/maintenance/#snapshot-backup) afin de disposer d'une voie de retour en cas de problème.

Le leader etcd est garanti pour avoir les données d'application les plus récentes ; récupérez donc l'instantané depuis le leader :

```bash
for p in 2379 22379 32379; do
  echo -n "localhost:$p leader="
  curl -sL http://localhost:$p/metrics | grep "^etcd_server_is_leader " | awk '{print $2}'
done
<<COMMENT
localhost:2379 leader=1
localhost:22379 leader=0
localhost:32379 leader=0
COMMENT

etcdctl --endpoints=localhost:2379 snapshot save backup.db
<<COMMENT
{"level":"info","ts":"2026-06-02T07:01:41.863225+0300","caller":"snapshot/v3_snapshot.go:83","msg":"created temporary db file","path":"backup.db.part"}
{"level":"info","ts":"2026-06-02T07:01:41.866451+0300","logger":"client","caller":"v3@v3.6.12/maintenance.go:236","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":"2026-06-02T07:01:41.874080+0300","caller":"snapshot/v3_snapshot.go:96","msg":"fetching snapshot","endpoint":"localhost:2379"}
{"level":"info","ts":"2026-06-02T07:01:41.877203+0300","caller":"snapshot/v3_snapshot.go:111","msg":"fetched snapshot","endpoint":"localhost:2379","size":"98 kB","took":"13.822583ms","etcd-version":"3.6.0"}
{"level":"info","ts":"2026-06-02T07:01:41.877303+0300","caller":"snapshot/v3_snapshot.go:121","msg":"saved","path":"backup.db"}
Snapshot saved at backup.db
Server version 3.6.0
COMMENT
```

#### Étape 3 : arrêter un serveur etcd existant {#step-3-stop-one-existing-etcd-server}

Lorsque chaque processus etcd est arrêté, les autres membres du cluster enregistrent des erreurs attendues. Cela est normal, car la connexion avec un membre du cluster a été (temporairement) interrompue. Le leader transfère son rôle avant de s'arrêter :

```bash
{"level":"info","ts":"2026-06-02T07:01:54.949299+0300","caller":"etcdserver/server.go:1274","msg":"leadership transfer finished","local-member-id":"7339c4e5e833c029","old-leader-member-id":"7339c4e5e833c029","new-leader-member-id":"b548c2511513015","took":"101.052625ms"}
{"level":"info","ts":"2026-06-02T07:01:54.949369+0300","caller":"etcdserver/server.go:2349","msg":"server has stopped; stopping cluster version's monitor"}
{"level":"info","ts":"2026-06-02T07:01:55.503219+0300","caller":"embed/etcd.go:626","msg":"stopped serving peer traffic","address":"127.0.0.1:2380"}
```

#### Étape 4 : redémarrer le serveur etcd avec la même configuration {#step-4-restart-the-etcd-server-with-same-configuration}

Redémarrez le serveur etcd avec la même configuration, mais avec le binaire etcd mis à jour.

```diff
-etcd-old --name ${name} \
+etcd-new --name ${name} \
  --data-dir /path/to/${name}.etcd \
  --listen-client-urls http://localhost:2379 \
  --advertise-client-urls http://localhost:2379 \
  --listen-peer-urls http://localhost:2380 \
  --initial-advertise-peer-urls http://localhost:2380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:22380,s3=http://localhost:32380 \
  --initial-cluster-token tkn \
  --initial-cluster-state new
```

Le nouvel etcd v3.7 publiera ses informations dans le cluster. À ce stade, le cluster continue de fonctionner selon le protocole v3.6, qui constitue la version la plus basse commune.

> `{"level":"info","ts":"2026-06-02T07:01:58.920780+0300","caller":"membership/cluster.go:296","msg":"set cluster version from store","cluster-version":"3.6"}`
>
> `{"level":"info","ts":"2026-06-02T07:01:58.979186+0300","caller":"etcdserver/server.go:1828","msg":"published local member to cluster through raft","local-member-id":"7339c4e5e833c029","local-member-attributes":"{Name:s1 ClientURLs:[http://localhost:2379]}","cluster-id":"7dee9ba76d59ed53","publish-timeout":"7s"}`

Vérifiez que chaque membre, puis l’ensemble du cluster, devient sain avec la nouvelle binaire etcd v3.7 :

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w table
<<COMMENT
+-----------------+------------------+------------+-----------------+---------+--------+-----------+
|    ENDPOINT     |        ID        |  VERSION   | STORAGE VERSION | DB SIZE | LEADER | RAFT TERM |
+-----------------+------------------+------------+-----------------+---------+--------+-----------+
|  localhost:2379 | 7339c4e5e833c029 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  false |         3 |
| localhost:22379 | 729934363faa4a24 |     3.6.12 |           3.6.0 |   98 kB |  false |         3 |
| localhost:32379 |  b548c2511513015 |     3.6.12 |           3.6.0 |   98 kB |   true |         3 |
+-----------------+------------------+------------+-----------------+---------+--------+-----------+
COMMENT
```

Les membres non mis à jour et le membre mis à jour vont générer des messages concernant l'état à version mixte jusqu'à ce que l'intégralité du cluster soit mis à jour. Cela est attendu et cessera une fois que tous les membres du cluster etcd auront été mis à jour vers la version 3.7.

#### Étape 5 : répéter l'*étape 3* et l'*étape 4* pour les membres restants {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

Lorsque tous les membres sont mis à jour, le cluster signalera avec succès la mise à jour vers la version v3.7 :

> `{"level":"info","ts":"2026-06-02T07:02:36.054783+0300","caller":"etcdserver/server.go:2311","msg":"updating cluster version using v3 API","from":"3.6","to":"3.7"}`
>
> `{"level":"info","ts":"2026-06-02T07:02:36.059345+0300","caller":"membership/cluster.go:593","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","from":"3.6","to":"3.7"}`
>
> `{"level":"info","ts":"2026-06-02T07:02:36.059409+0300","caller":"etcdserver/server.go:2326","msg":"cluster version is updated","cluster-version":"3.7"}`

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 550.833µs
localhost:32379 is healthy: successfully committed proposal: took = 733.458µs
localhost:22379 is healthy: successfully committed proposal: took = 714.416µs
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
```
