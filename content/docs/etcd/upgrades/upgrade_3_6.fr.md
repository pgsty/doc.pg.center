---
title: Mettre à jour etcd de la version v3.5 à la version v3.6
weight: 6600
description: "Processus, listes de vérification et notes sur la mise à niveau d'etcd de la version 3.5 à la version 3.6"
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_6.md"
aliases: [/etcd/upgrades/upgrade_3_6/]
---

Dans le cas général, la mise à niveau d’etcd v3.5 vers v3.6 peut être une mise à niveau progressive sans interruption de service :

-  un à un, arrêtez les processus etcd v3.5 et remplacez-les par des processus etcd v3.6
-  après avoir lancé tous les processus v3.6, les nouvelles fonctionnalités de la version v3.6 sont disponibles pour le cluster

Avant de [lancer la mise à jour](#upgrade-procedure), lisez le reste du présent guide afin de vous préparer.

### Listes de vérification pour la mise à jour {#upgrade-checklists}

#### Mise à jour 3.5 {#update-35}

> [!IMPORTANT]
> Avant de mettre à jour vers la version 3.6, assurez-vous que [tous vos membres 3.5 sont mis à jour vers la version 3.5.32 ou ultérieure](https://etcd.io/blog/2026/july-patch-release/). Les correctifs 3.5.24 à 3.5.26 corrigent plusieurs blocages potentiels liés à la mise à jour ; [3.5.32](https://etcd.io/blog/2026/july-patch-release/) ajoute `--v2-deprecation=write-only-skip-check` et étend `etcdutl check v2store` afin d'inspecter les enregistrements WAL ainsi que l'instantané v2.

#### Magasin V2 {#v2-store}

> [!NOTE]
> Si le drapeau `--enable-v2` n'est pas configuré ou est défini à false, aucune action supplémentaire n'est requise.

Si `--enable-v2` est configuré, exécutez la commande `etcdutl check v2store` pour vérifier si le v2store contient des données non liées aux membres (données personnalisées). Si aucune donnée personnalisée n'est présente, le drapeau peut être supprimé en toute sécurité. Sinon, consultez le guide de migration [v2](https://etcd.io/docs/v3.4/op-guide/v2-migration/) pour plus de détails.

### Drapeaux ajoutés {#flags-added}

```diff
+etcd --discovery-token ''
+etcd --discovery-endpoints ''
+etcd --discovery-dial-timeout '2s'
+etcd --discovery-request-timeout '5s'
+etcd --discovery-keepalive-time '2s'
+etcd --discovery-keepalive-timeout '6s'
+etcd --discovery-insecure-transport 'true'
+etcd --discovery-insecure-skip-tls-verify 'false'
+etcd --discovery-cert ''
+etcd --discovery-key ''
+etcd --discovery-cacert ''
+etcd --discovery-user ''
+etcd --discovery-password ''
+etcd --feature-gates
+etcd --log-format
```

### Drapeaux supprimés {#flags-removed}

```diff
-etcd --enable-v2
-etcd --experimental-enable-v2v3
-etcd --proxy
-etcd --proxy-failure-wait
-etcd --proxy-refresh-interval
-etcd --proxy-dial-timeout
-etcd --proxy-write-timeout
-etcd --proxy-read-timeout
```

### Drapeaux obsolètes {#flags-deprecated}

**Le drapeau `etcd --experimental-bootstrap-defrag-threshold-megabytes` a été déprécié.**

```diff

-etcd --experimental-bootstrap-defrag-threshold-megabytes

+etcd --bootstrap-defrag-threshold-megabytes

```

**Le drapeau `etcd --experimental-compaction-batch-limit` a été déprécié.**

```diff

-etcd --experimental-compaction-batch-limit

+etcd --compaction-batch-limit

```

**Le drapeau `etcd --experimental-compact-hash-check-time` a été déprécié.**

```diff

-etcd --experimental-compact-hash-check-time

+etcd --compact-hash-check-time

```

**Le drapeau `etcd --experimental-compaction-sleep-interval` a été déprécié.**

```diff

-etcd --experimental-compaction-sleep-interval

+etcd --compaction-sleep-interval

```

**Le drapeau `etcd --experimental-corrupt-check-time` a été déprécié.**

```diff

-etcd --experimental-corrupt-check-time

+etcd --corrupt-check-time

```

**Le drapeau `etcd --experimental-enable-distributed-tracing` a été déprécié.**

```diff

-etcd --experimental-enable-distributed-tracing

+etcd --enable-distributed-tracing

```

**Le drapeau `etcd --experimental-distributed-tracing-address` a été déprécié.**

```diff

-etcd --experimental-distributed-tracing-address

+etcd --distributed-tracing-address

```

**Le drapeau `etcd --experimental-distributed-tracing-instance-id` a été déprécié.**

```diff

-etcd --experimental-distributed-tracing-instance-id

+etcd --distributed-tracing-instance-id

```

**Le drapeau `etcd --experimental-distributed-tracing-sampling-rate` a été déprécié.**

```diff

-etcd --experimental-distributed-tracing-sampling-rate

+etcd --distributed-tracing-sampling-rate

```

**Le drapeau `etcd --experimental-distributed-tracing-service-name` a été déprécié.**

```diff

-etcd --experimental-distributed-tracing-service-name

+etcd --distributed-tracing-service-name

```

**Le drapeau `etcd --experimental-downgrade-check-time` a été déprécié.**

```diff

-etcd --experimental-downgrade-check-time

+etcd --downgrade-check-time

```

**Le drapeau `etcd --experimental-max-learners` a été déprécié.**

```diff

-etcd --experimental-max-learners

+etcd --max-learners

```

**Le drapeau `etcd --experimental-memory-mlock` a été déprécié.**

```diff

-etcd --experimental-memory-mlock

+etcd --memory-mlock

```

**Le drapeau `etcd --experimental-peer-skip-client-san-verification` a été déprécié.**

```diff

-etcd --experimental-peer-skip-client-san-verification

+etcd --peer-skip-client-san-verification

```

**Le drapeau `etcd --experimental-snapshot-catchup-entries` a été déprécié.**

```diff

-etcd --experimental-snapshot-catchup-entries

+etcd --snapshot-catchup-entries

```

**Le drapeau `etcd --experimental-warning-apply-duration` a été déprécié.**

```diff

-etcd --experimental-warning-apply-duration

+etcd --warning-apply-duration

```

**Le drapeau `etcd --experimental-warning-unary-request-duration` a été déprécié.**

```diff

-etcd --experimental-warning-unary-request-duration

+etcd --warning-unary-request-duration

```

**Le drapeau `etcd --experimental-watch-progress-notify-interval` a été déprécié.**

```diff

-etcd --experimental-watch-progress-notify-interval

+etcd --watch-progress-notify-interval

```

### Migration des options expérimentales de v3.5 vers les portes fonctionnelles {#equivalent-flags-of-v35-feature-gates}

**Porte fonctionnelle correspondant à `etcd --experimental-compact-hash-check-enabled=true`**

```diff

-etcd --experimental-compact-hash-check-enabled=true

+etcd --feature-gates=CompactHashCheck=true

```

**Porte fonctionnelle correspondant à `etcd --experimental-initial-corrupt-check=true`**

```diff

-etcd --experimental-initial-corrupt-check=true

+etcd --feature-gates=InitialCorruptCheck=true

```

**Porte fonctionnelle correspondant à `etcd --experimental-enable-lease-checkpoint=true`**

```diff

-etcd --experimental-enable-lease-checkpoint=true

+etcd --feature-gates=LeaseCheckpoint=true

```

**Porte fonctionnelle correspondant à `etcd --experimental-enable-lease-checkpoint-persist=true`**

```diff

-etcd --experimental-enable-lease-checkpoint-persist=true

+etcd --feature-gates=LeaseCheckpointPersist=true

```

**Porte fonctionnelle correspondant à `etcd --experimental-stop-grpc-service-on-defrag=true`**

```diff

-etcd --experimental-stop-grpc-service-on-defrag=true

+etcd --feature-gates=StopGRPCServiceOnDefrag=true

```

**Porte fonctionnelle correspondant à `etcd --experimental-txn-mode-write-with-shared-buffer=false`**

```diff

-etcd --experimental-txn-mode-write-with-shared-buffer=false

+etcd --feature-gates=TxnModeWriteWithSharedBuffer=false

```

### Drapeaux avec de nouvelles valeurs par défaut {#flags-with-new-defaults}

**Valeur par défaut d'origine du drapeau `etcd --snapshot-count=100000`**

```diff

-etcd --snapshot-count=100000

+etcd --snapshot-count=10000

```

**Valeur par défaut d'origine du drapeau `etcd --v2-deprecation='not-yet'`**

```diff

-etcd --v2-deprecation='not-yet'

+etcd --v2-deprecation='write-only'

```

**Valeur par défaut d'origine du drapeau `etcd --discovery-fallback='proxy'`**

```diff

-etcd --discovery-fallback='proxy'

+etcd --discovery-fallback='exit'

```

### Différence entre les métriques Prometheus {#difference-in-prometheus-metrics}

```diff
# metrics added in v3.6
+etcd_network_known_peers
+etcd_server_feature_enabled
```

### Liste de vérification pour la mise à jour du serveur {#server-upgrade-checklists}

#### Exigences de mise à jour {#upgrade-requirements}

Pour mettre à jour un déploiement etcd existant vers la version 3.6, le cluster en cours d'exécution doit être la version 3.5 ou ultérieure. Si la version est antérieure à 3.5, veuillez [mettre à jour vers la version 3.5](/fr/docs/etcd/upgrades/upgrade_3_5/) avant de procéder à la mise à jour vers la version 3.6.

En outre, pour garantir une mise à niveau progressive sans incident, le cluster en cours d'exécution doit être sain. Vérifiez l'état de santé du cluster à l'aide de la commande `etcdctl endpoint health` avant de poursuivre.

#### Préparation {#preparation}

Avant de mettre à jour etcd, testez toujours les services dépendants d’etcd dans un environnement de préproduction avant de déployer la mise à jour dans l’environnement de production.

Avant de commencer, [téléchargez la sauvegarde d'instantané](/fr/docs/etcd/op-guide/maintenance/#snapshot-backup). Si une erreur survient lors de la mise à jour, il sera possible d'utiliser cette sauvegarde pour [annuler](#rollback) la mise à jour et revenir à la version existante d’etcd. Veuillez noter que la commande `snapshot` ne sauvegarde que les données v3.

#### Versions mixtes {#mixed-versions}

Lors d'une mise à jour, un cluster etcd prend en charge des versions mixtes de membres et fonctionne selon le protocole de la version commune la plus basse. Le cluster n'est considéré comme mis à jour qu'une fois que tous ses membres ont été mis à jour vers la version v3.6. En interne, les membres etcd négocient entre eux afin de déterminer la version globale du cluster, qui contrôle la version signalée et les fonctionnalités prises en charge.

#### Retour arrière {#rollback}

Avant de mettre à jour votre cluster etcd, créez et [téléchargez une sauvegarde sous forme d'instantané](/fr/docs/etcd/op-guide/maintenance/#snapshot-backup) de votre cluster etcd. Cet instantané peut être utilisé pour restaurer le cluster dans son état antérieur à la mise à jour si nécessaire. Si les utilisateurs rencontrent des problèmes pendant la mise à jour, ils doivent d'abord identifier et résoudre la cause racine. Si le cluster est toujours dans un état mixte — où au moins un membre reste sur la version v3.5 —, il est possible de remplacer le binaire ou l'image par la version v3.5 antérieure, ou de restaurer directement le cluster à l'aide de l'instantané. Dans cet état mixte, le cluster continue de fonctionner en tant que cluster v3.5, permettant ainsi un retour arrière sans suivre un processus formel de rétrogradation.

Toutefois, une fois que tous les membres ont été mis à jour vers la version v3.6, le cluster est considéré comme entièrement mis à jour et le simple remplacement des binaires n’est plus un retour arrière valide. Les options de récupération consistent à restaurer depuis l’instantané pris avant la mise à jour ou à suivre le guide officiel de rétrogradation pour revenir à la version d’origine en assurant la cohérence et en évitant toute corruption des données.

### Procédure de mise à jour {#upgrade-procedure}

Cet exemple montre comment mettre à jour un cluster etcd v3.5 composé de 3 membres, en cours d'exécution sur une machine locale.

#### Étape 1 : vérifier les exigences de mise à jour {#step-1-check-upgrade-requirements}

Le cluster est-il sain et en cours d'exécution sous la version 3.5.x ?

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 2.555774ms
localhost:32379 is healthy: successfully committed proposal: took = 2.631133ms
localhost:22379 is healthy: successfully committed proposal: took = 3.020958ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.5.18","etcdcluster":"3.5.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.5.18","etcdcluster":"3.5.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.5.18","etcdcluster":"3.5.0"}
COMMENT
```

#### Étape 2 : télécharger la sauvegarde d'instantané depuis le leader {#step-2-download-snapshot-backup-from-leader}

[Téléchargez l'instantané de sauvegarde](/fr/docs/etcd/op-guide/maintenance/#snapshot-backup) afin de disposer d'une voie de retour en cas de problème.

Le leader etcd possède toujours les données d'application les plus récentes ; récupérez donc l'instantané depuis le leader :

```bash
curl -sL http://localhost:2379/metrics | grep etcd_server_is_leader
<<COMMENT
# HELP etcd_server_is_leader Whether or not this member is a leader. 1 if is, 0 otherwise.
# TYPE etcd_server_is_leader gauge
etcd_server_is_leader 1
COMMENT

curl -sL http://localhost:22379/metrics | grep etcd_server_is_leader
<<COMMENT
etcd_server_is_leader 0
COMMENT

curl -sL http://localhost:32379/metrics | grep etcd_server_is_leader
<<COMMENT
etcd_server_is_leader 0
COMMENT

etcdctl --endpoints=localhost:2379 snapshot save backup.db
<<COMMENT
{"level":"info","ts":"2025-03-01T04:34:10.336768+0530","caller":"snapshot/v3_snapshot.go:65","msg":"created temporary db file","path":"backup.db.part"}
{"level":"info","ts":"2025-03-01T04:34:10.342373+0530","logger":"client","caller":"v3@v3.5.18/maintenance.go:212","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":"2025-03-01T04:34:10.342433+0530","caller":"snapshot/v3_snapshot.go:73","msg":"fetching snapshot","endpoint":"localhost:2379"}
{"level":"info","ts":"2025-03-01T04:34:10.346482+0530","logger":"client","caller":"v3@v3.5.18/maintenance.go:220","msg":"completed snapshot read; closing"}
{"level":"info","ts":"2025-03-01T04:34:10.348801+0530","caller":"snapshot/v3_snapshot.go:88","msg":"fetched snapshot","endpoint":"localhost:2379","size":"20 kB","took":"now"}
{"level":"info","ts":"2025-03-01T04:34:10.348933+0530","caller":"snapshot/v3_snapshot.go:97","msg":"saved","path":"backup.db"}
Snapshot saved at backup.db
COMMENT
```

#### Étape 3 : arrêter un serveur etcd existant {#step-3-stop-one-existing-etcd-server}

Lorsque chaque processus etcd est arrêté, les autres membres du cluster enregistrent des erreurs attendues. Cela est normal, car la connexion avec un membre du cluster a été (temporairement) interrompue :

```bash
{"level":"info","ts":"2025-03-01T04:31:50.654520+0530","caller":"etcdserver/server.go:2676","msg":"cluster version is updated","cluster-version":"3.5"}
{"level":"info","ts":"2025-03-01T04:34:10.345927+0530","caller":"v3rpc/maintenance.go:130","msg":"sending database snapshot to client","total-bytes":20480,"size":"20 kB"}
{"level":"info","ts":"2025-03-01T04:34:10.346094+0530","caller":"v3rpc/maintenance.go:170","msg":"sending database sha256 checksum to client","total-bytes":20480,"checksum-size":32}
{"level":"info","ts":"2025-03-01T04:34:10.346108+0530","caller":"v3rpc/maintenance.go:179","msg":"successfully sent database snapshot to client","total-bytes":20480,"size":"20 kB","took":"now"}
^C
{"level":"info","ts":"2025-03-01T04:35:01.443045+0530","caller":"osutil/interrupt_unix.go:64","msg":"received signal; shutting down","signal":"interrupt"}
{"level":"info","ts":"2025-03-01T04:35:01.443088+0530","caller":"embed/etcd.go:408","msg":"closing etcd server","name":"node1","data-dir":"/tmp/etcd-node1","advertise-peer-urls":["http://127.0.0.1:2380"],"advertise-client-urls":["http://127.0.0.1:2379"]}
{"level":"info","ts":"2025-03-01T04:35:01.443417+0530","caller":"etcdserver/server.go:1503","msg":"leadership transfer starting","local-member-id":"bf9071f4639c75cc","current-leader-member-id":"bf9071f4639c75cc","transferee-member-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.443441+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc [term 2] starts to transfer leadership to 91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.443455+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc sends MsgTimeoutNow to 91bc3c398fb3c146 immediately as 91bc3c398fb3c146 already has up-to-date log"}
{"level":"warn","ts":"2025-03-01T04:35:01.443517+0530","caller":"embed/serve.go:179","msg":"stopping insecure grpc server due to error","error":"accept tcp 127.0.0.1:2379: use of closed network connection"}
{"level":"warn","ts":"2025-03-01T04:35:01.443548+0530","caller":"embed/serve.go:181","msg":"stopped insecure grpc server due to error","error":"accept tcp 127.0.0.1:2379: use of closed network connection"}
{"level":"info","ts":"2025-03-01T04:35:01.445536+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc [term: 2] received a MsgVote message with higher term from 91bc3c398fb3c146 [term: 3]"}
{"level":"info","ts":"2025-03-01T04:35:01.445556+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc became follower at term 3"}
{"level":"info","ts":"2025-03-01T04:35:01.445565+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc [logterm: 2, index: 12, vote: 0] cast MsgVote for 91bc3c398fb3c146 [logterm: 2, index: 12] at term 3"}
{"level":"info","ts":"2025-03-01T04:35:01.445572+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"raft.node: bf9071f4639c75cc lost leader bf9071f4639c75cc at term 3"}
{"level":"info","ts":"2025-03-01T04:35:01.446773+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"raft.node: bf9071f4639c75cc elected leader 91bc3c398fb3c146 at term 3"}
{"level":"info","ts":"2025-03-01T04:35:01.544062+0530","caller":"etcdserver/server.go:1520","msg":"leadership transfer finished","local-member-id":"bf9071f4639c75cc","old-leader-member-id":"bf9071f4639c75cc","new-leader-member-id":"91bc3c398fb3c146","took":"100.640374ms"}
{"level":"info","ts":"2025-03-01T04:35:01.544160+0530","caller":"rafthttp/peer.go:330","msg":"stopping remote peer","remote-peer-id":"91bc3c398fb3c146"}
{"level":"warn","ts":"2025-03-01T04:35:01.544956+0530","caller":"rafthttp/stream.go:286","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.544984+0530","caller":"rafthttp/stream.go:294","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"91bc3c398fb3c146"}
{"level":"warn","ts":"2025-03-01T04:35:01.545050+0530","caller":"rafthttp/stream.go:286","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.545065+0530","caller":"rafthttp/stream.go:294","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.545099+0530","caller":"rafthttp/pipeline.go:85","msg":"stopped HTTP pipelining with remote peer","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146"}
{"level":"warn","ts":"2025-03-01T04:35:01.545156+0530","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146","error":"context canceled"}
{"level":"warn","ts":"2025-03-01T04:35:01.545178+0530","caller":"rafthttp/peer_status.go:66","msg":"peer became inactive (message send to peer failed)","peer-id":"91bc3c398fb3c146","error":"failed to read 91bc3c398fb3c146 on stream MsgApp v2 (context canceled)"}
{"level":"info","ts":"2025-03-01T04:35:01.545199+0530","caller":"rafthttp/stream.go:442","msg":"stopped stream reader with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146"}
{"level":"warn","ts":"2025-03-01T04:35:01.545246+0530","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146","error":"context canceled"}
{"level":"info","ts":"2025-03-01T04:35:01.545263+0530","caller":"rafthttp/stream.go:442","msg":"stopped stream reader with remote peer","stream-reader-type":"stream Message","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.545272+0530","caller":"rafthttp/peer.go:335","msg":"stopped remote peer","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.545282+0530","caller":"rafthttp/peer.go:330","msg":"stopping remote peer","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545307+0530","caller":"rafthttp/stream.go:286","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"fd422379fda50e48"}
{"level":"info","ts":"2025-03-01T04:35:01.545328+0530","caller":"rafthttp/stream.go:294","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545359+0530","caller":"rafthttp/stream.go:286","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"fd422379fda50e48"}
{"level":"info","ts":"2025-03-01T04:35:01.545379+0530","caller":"rafthttp/stream.go:294","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"fd422379fda50e48"}
{"level":"info","ts":"2025-03-01T04:35:01.545410+0530","caller":"rafthttp/pipeline.go:85","msg":"stopped HTTP pipelining with remote peer","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545467+0530","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48","error":"context canceled"}
{"level":"warn","ts":"2025-03-01T04:35:01.545485+0530","caller":"rafthttp/peer_status.go:66","msg":"peer became inactive (message send to peer failed)","peer-id":"fd422379fda50e48","error":"failed to read fd422379fda50e48 on stream MsgApp v2 (context canceled)"}
{"level":"info","ts":"2025-03-01T04:35:01.545504+0530","caller":"rafthttp/stream.go:442","msg":"stopped stream reader with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545560+0530","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48","error":"context canceled"}
{"level":"info","ts":"2025-03-01T04:35:01.545577+0530","caller":"rafthttp/stream.go:442","msg":"stopped stream reader with remote peer","stream-reader-type":"stream Message","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48"}
{"level":"info","ts":"2025-03-01T04:35:01.545592+0530","caller":"rafthttp/peer.go:335","msg":"stopped remote peer","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545669+0530","caller":"rafthttp/http.go:413","msg":"failed to find remote peer in cluster","local-member-id":"bf9071f4639c75cc","remote-peer-id-stream-handler":"bf9071f4639c75cc","remote-peer-id-from":"91bc3c398fb3c146","cluster-id":"59a05384c9b79ee"}
{"level":"warn","ts":"2025-03-01T04:35:01.545698+0530","caller":"rafthttp/http.go:413","msg":"failed to find remote peer in cluster","local-member-id":"bf9071f4639c75cc","remote-peer-id-stream-handler":"bf9071f4639c75cc","remote-peer-id-from":"fd422379fda50e48","cluster-id":"59a05384c9b79ee"}
{"level":"warn","ts":"2025-03-01T04:35:01.545732+0530","caller":"rafthttp/http.go:413","msg":"failed to find remote peer in cluster","local-member-id":"bf9071f4639c75cc","remote-peer-id-stream-handler":"bf9071f4639c75cc","remote-peer-id-from":"91bc3c398fb3c146","cluster-id":"59a05384c9b79ee"}
{"level":"warn","ts":"2025-03-01T04:35:01.545765+0530","caller":"rafthttp/http.go:413","msg":"failed to find remote peer in cluster","local-member-id":"bf9071f4639c75cc","remote-peer-id-stream-handler":"bf9071f4639c75cc","remote-peer-id-from":"fd422379fda50e48","cluster-id":"59a05384c9b79ee"}
{"level":"info","ts":"2025-03-01T04:35:01.549658+0530","caller":"embed/etcd.go:613","msg":"stopping serving peer traffic","address":"127.0.0.1:2380"}
{"level":"info","ts":"2025-03-01T04:35:02.550532+0530","caller":"embed/etcd.go:618","msg":"stopped serving peer traffic","address":"127.0.0.1:2380"}
{"level":"info","ts":"2025-03-01T04:35:02.550561+0530","caller":"embed/etcd.go:410","msg":"closed etcd server","name":"node1","data-dir":"/tmp/etcd-node1","advertise-peer-urls":["http://127.0.0.1:2380"],"advertise-client-urls":["http://127.0.0.1:2379"]}
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

Le nouvel etcd v3.6 publiera ses informations dans le cluster. À ce stade, le cluster continue de fonctionner selon le protocole v3.5, qui constitue la version la plus basse commune.

> `{"level":"info","ts":"2025-03-01T04:40:36.828+0530","caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`
>
> `{"level":"info","ts":"2025-03-01T04:40:36.889+0530","caller":"membership/cluster.go:539","msg":"updated cluster version","cluster-id":"59a05384c9b79ee","local-member-id":"bf9071f4639c75cc","from":"3.0","to":"3.5"}`
>
> `{"level":"info","ts":"2025-03-01T04:40:36.828+0530","caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`
>
> `{"level":"info","ts":"2025-03-01T04:40:36.894+0530","caller":"etcdserver/server.go:1686","msg":"published local member to cluster through raft","local-member-id":"bf9071f4639c75cc","local-member-attributes":"{Name:node1 ClientURLs:[http://127.0.0.1:2379]}","cluster-id":"59a05384c9b79ee","publish-timeout":"7s"}`

Vérifiez que chaque membre, puis l’ensemble du cluster, devient sain avec le nouveau binaire etcd v3.6 :

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 1.704998ms
localhost:22379 is healthy: successfully committed proposal: took = 2.331754ms
localhost:32379 is healthy: successfully committed proposal: took = 2.490705ms
COMMENT
```

Les membres non mis à jour afficheront des avertissements tels que les suivants jusqu'à ce que tout le cluster soit mis à jour.

Cela est attendu et cessera une fois que tous les membres du cluster etcd auront été mis à jour vers la version 3.6 :

```bash
{"level":"warn","ts":"2025-03-01T04:40:37.545960+0530","caller":"etcdserver/cluster_util.go:189","msg":"leader found higher-versioned member","local-member-version":"3.5.18","remote-member-id":"bf9071f4639c75cc","remote-member-version":"3.6.0-alpha.0"}
```

#### Étape 5 : répéter l'*étape 3* et l'*étape 4* pour les membres restants {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

Lorsque tous les membres sont mis à jour, le cluster signalera avec succès la mise à jour vers la version v3.6 :

Membre 1 :

> `{"level":"info","ts":"2025-03-01T04:58:32.375+0530","caller":"etcdserver/server.go:2149","msg":"updating cluster version using v3 API","from":"3.5","to":"3.6"}`
> `{"level":"info","ts":"2025-03-01T04:58:32.377+0530","caller":"etcdserver/server.go:2164","msg":"cluster version is updated","cluster-version":"3.6"}`

Membre 2 :

> `{"level":"info","ts":"2025-03-01T04:58:32.377+0530","caller":"membership/cluster.go:539","msg":"updated cluster version","cluster-id":"59a05384c9b79ee","local-member-id":"91bc3c398fb3c146","from":"3.5","to":"3.6"}`

Membre 3 :

> `{"level":"info","ts":"2025-03-01T04:58:32.377+0530","caller":"membership/cluster.go:539","msg":"updated cluster version","cluster-id":"59a05384c9b79ee","local-member-id":"fd422379fda50e48","from":"3.5","to":"3.6"}`

```bash
endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 492.834µs
localhost:22379 is healthy: successfully committed proposal: took = 1.015025ms
localhost:32379 is healthy: successfully committed proposal: took = 1.853077ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0"}
COMMENT
```
