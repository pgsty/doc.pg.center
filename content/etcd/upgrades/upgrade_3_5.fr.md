---
title: Mettre à jour etcd de 3.4 à 3.5
weight: 6650
description: "Processus, listes de vérification et notes sur la mise à niveau d'etcd de la version 3.4 à la 3.5"
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_5.md"
---

Dans le cas général, la mise à niveau d’etcd 3.4 vers 3.5 peut être effectuée sans interruption de service, en mode mise à niveau progressive :
 - un par un, arrêtez les processus etcd v3.4 et remplacez-les par des processus etcd v3.5
 - après avoir lancé tous les processus v3.5, les nouvelles fonctionnalités de la version v3.5 sont disponibles pour le cluster

Avant de [lancer la mise à jour](#upgrade-procedure), lisez le reste du présent guide afin de vous préparer.



### Listes de vérification pour la mise à jour {#upgrade-checklists}

> [!WARNING]
> Lorsque [on migre depuis la version v2 sans données v3](https://github.com/etcd-io/etcd/issues/9480), le serveur etcd v3.2+ provoque une panne lorsqu'il restaure à partir d'un instantané existant mais qu'aucun fichier v3 `ETCD_DATA_DIR/member/snap/db` n'est présent. Cela se produit lorsque le serveur a été migré depuis la version v2 sans données v3 précédentes. Cela empêche également la perte accidentelle de données v3 (par exemple, le fichier `db` pourrait avoir été déplacé). etcd exige que les opérations après migration vers v3 ne soient effectuées que si des données v3 sont présentes. N'effectuez pas la mise à jour vers des versions v3 plus récentes tant que le serveur v3.0 ne contient pas de données v3.

> [!WARNING]
> Si votre cluster a l'authentification activée, la mise à niveau progressive à partir d'une version 3.4 ou antérieure n'est pas prise en charge, car la version 3.5 [modifie le format des entrées WAL liées à l'authentification](https://github.com/etcd-io/etcd/pull/11943).

Changements de rupture mis en évidence dans la version 3.5.

#### Métriques Prometheus `etcd_debugging_mvcc_db_total_size_in_bytes` obsolètes {#deprecated-etcd_debugging_mvcc_db_total_size_in_bytes-prometheus-metrics}

v3.5 a promu les métriques Prometheus `etcd_debugging_mvcc_db_total_size_in_bytes` à `etcd_mvcc_db_total_size_in_bytes`, afin de favoriser la surveillance du stockage etcd. La version v3.5 déprécie complètement `etcd_debugging_mvcc_db_total_size_in_bytes`.

```diff
-etcd_debugging_mvcc_db_total_size_in_bytes
+etcd_mvcc_db_total_size_in_bytes
```

Notez que les métriques de l'espace de noms `etcd_debugging_*` sont marquées comme expérimentales. Au fur et à mesure que nous améliorons le guide de surveillance, certaines métriques pourraient être promues.

#### Métriques Prometheus `etcd_debugging_mvcc_put_total` obsolètes {#deprecated-etcd_debugging_mvcc_put_total-prometheus-metrics}

v3.5 a promu les métriques Prometheus `etcd_debugging_mvcc_put_total` à `etcd_mvcc_put_total`, afin de favoriser la surveillance du stockage etcd. La version v3.5 déprécie complètement `etcd_debugging_mvcc_put_total`.

```diff
-etcd_debugging_mvcc_put_total
+etcd_mvcc_put_total
```

Notez que les métriques de l'espace de noms `etcd_debugging_*` sont marquées comme expérimentales. Au fur et à mesure que nous améliorons le guide de surveillance, certaines métriques pourraient être promues.

#### Métriques Prometheus `etcd_debugging_mvcc_delete_total` obsolètes {#deprecated-etcd_debugging_mvcc_delete_total-prometheus-metrics}

v3.5 a promu les métriques Prometheus `etcd_debugging_mvcc_delete_total` à `etcd_mvcc_delete_total`, afin de favoriser la surveillance du stockage etcd. La version v3.5 déprécie complètement `etcd_debugging_mvcc_delete_total`.

```diff
-etcd_debugging_mvcc_delete_total
+etcd_mvcc_delete_total
```

Notez que les métriques de l'espace de noms `etcd_debugging_*` sont marquées comme expérimentales. Au fur et à mesure que nous améliorons le guide de surveillance, certaines métriques pourraient être promues.

#### Métriques Prometheus `etcd_debugging_mvcc_txn_total` obsolètes {#deprecated-etcd_debugging_mvcc_txn_total-prometheus-metrics}

v3.5 a promu les métriques Prometheus `etcd_debugging_mvcc_txn_total` à `etcd_mvcc_txn_total`, afin de favoriser la surveillance du stockage etcd. La version v3.5 déprécie complètement `etcd_debugging_mvcc_txn_total`.

```diff
-etcd_debugging_mvcc_txn_total
+etcd_mvcc_txn_total
```

Notez que les métriques de l'espace de noms `etcd_debugging_*` sont marquées comme expérimentales. Au fur et à mesure que nous améliorons le guide de surveillance, certaines métriques pourraient être promues.

#### Métriques Prometheus `etcd_debugging_mvcc_range_total` obsolètes {#deprecated-etcd_debugging_mvcc_range_total-prometheus-metrics}

v3.5 a promu les métriques Prometheus `etcd_debugging_mvcc_range_total` à `etcd_mvcc_range_total`, afin de favoriser la surveillance du stockage etcd. La version v3.5 déprécie complètement `etcd_debugging_mvcc_range_total`.

```diff
-etcd_debugging_mvcc_range_total
+etcd_mvcc_range_total
```

Notez que les métriques de l'espace de noms `etcd_debugging_*` sont marquées comme expérimentales. Au fur et à mesure que nous améliorons le guide de surveillance, certaines métriques pourraient être promues.

#### Dépréciation de `etcd --logger capnslog` {#deprecated-etcd---logger-capnslog}

La version 3.5 utilise par défaut `--logger=zap` afin de prendre en charge plusieurs sorties de journalisation et la journalisation structurée.

**`etcd --logger=capnslog` a été déprécié à partir de la version 3.5**, et `--logger=zap` est désormais la valeur par défaut.

```diff
-etcd --logger=capnslog
+etcd --logger=zap --log-outputs=stderr

+# to write logs to stderr and a.log file at the same time
+etcd --logger=zap --log-outputs=stderr,a.log
```

v3.4 ajoute la prise en charge de `etcd --logger=zap` pour la journalisation structurée et plusieurs sorties de journal. La motivation principale est de favoriser la surveillance automatisée d’etcd, plutôt que d’analyser les journaux serveur lorsqu’il commence à présenter des anomalies. Les développements futurs viseront à réduire au minimum la quantité de logs générés par etcd, et à faciliter sa surveillance grâce aux métriques et aux alertes. **`etcd --logger=capnslog` sera déprécié à partir de v3.5.**

#### Dépréciation de `etcd --log-output` {#deprecated-etcd---log-output}

v3.4 a renommé [`etcd --log-output` en `--log-outputs`](https://github.com/etcd-io/etcd/pull/9624) afin de prendre en charge plusieurs sorties de journalisation.

**`etcd --log-output` a été déprécié à partir de la version 3.5.**

```diff
-etcd --log-output=stderr
+etcd --log-outputs=stderr
```

#### Dépréciation de le drapeau `etcd --debug` (maintenant `--log-level=debug`) {#deprecated-etcd---debug-flag-now---log-leveldebug}

**Le drapeau `etcd --debug` a été déprécié.**

```diff
-etcd --debug
+etcd --log-level debug
```

#### Dépréciation de `etcd --log-package-levels` {#deprecated-etcd---log-package-levels}

**Le drapeau `etcd --log-package-levels` pour `capnslog` a été déprécié.**

Maintenant, **`etcd --logger=zap`** est la valeur par défaut.

```diff
-etcd --log-package-levels 'etcdmain=CRITICAL,etcdserver=DEBUG'
+etcd --logger=zap --log-outputs=stderr
```

#### Dépréciation de `[CLIENT-URL]/config/local/log` {#deprecated-client-urlconfiglocallog}

**L'endpoint `/config/local/log` est déprécié à partir de la version 3.5, tout comme le drapeau `etcd --log-package-levels`.**

```diff
-$ curl http://127.0.0.1:2379/config/local/log -XPUT -d '{"Level":"DEBUG"}'
-# debug logging enabled
```

#### Modifier les points d'accès HTTP de la passerelle gRPC (obsolète `/v3beta`) {#changed-grpc-gateway-http-endpoints-deprecated-v3beta}

Avant

```bash
curl -L http://localhost:2379/v3beta/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

Après

```bash
curl -L http://localhost:2379/v3/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

`/v3beta` a été supprimé dans la version 3.5.



### Liste de vérification pour la mise à jour du serveur {#server-upgrade-checklists}

#### Exigences de mise à jour {#upgrade-requirements}

Pour mettre à jour un déploiement etcd existant vers la version 3.5, le cluster en cours d'exécution doit être la version 3.4 ou ultérieure. Si la version est antérieure à 3.4, veuillez [mettre à jour vers la version 3.4](/fr/etcd/upgrades/upgrade_3_4/) avant de procéder à la mise à jour vers la version 3.5.

En outre, pour garantir une mise à niveau progressive sans incident, le cluster en cours d'exécution doit être sain. Vérifiez l'état de santé du cluster à l'aide de la commande `etcdctl endpoint health` avant de poursuivre.

#### Préparation {#preparation}

Avant de mettre à jour etcd, testez toujours les services dépendants d’etcd dans un environnement de préproduction avant de déployer la mise à jour dans l’environnement de production.

Avant de commencer, [téléchargez l'instantané de sauvegarde](/fr/etcd/op-guide/maintenance/#snapshot-backup). Si une erreur survient lors de la mise à jour, il sera possible d'utiliser cette sauvegarde pour [rétrograder](#downgrade) vers la version existante d’etcd. Veuillez noter que la commande `snapshot` ne sauvegarde que les données v3. Pour les données v2, consultez [sauvegarde du magasin de données v2](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore).

#### Versions mixtes {#mixed-versions}

Lors d'une mise à jour, un cluster etcd prend en charge des versions mixtes de membres et fonctionne selon le protocole de la version commune la plus basse. Le cluster n'est considéré comme mis à jour qu'une fois que tous ses membres ont été mis à jour vers la version 3.5. En interne, les membres etcd négocient entre eux afin de déterminer la version globale du cluster, qui contrôle la version signalée et les fonctionnalités prises en charge.

#### Limitations {#limitations}

Note : Si le cluster ne contient que des données v3 et aucune donnée v2, il n'est pas soumis à cette limitation.

Si le cluster sert un jeu de données v2 dont la taille dépasse 50 Mo, chaque membre nouvellement mis à jour peut prendre jusqu’à deux minutes pour rattraper le cluster existant. Vérifiez la taille d’un instantané récent afin d’estimer la taille totale des données. Autrement dit, le plus sûr est d’attendre deux minutes entre chaque mise à jour de membre.

Pour une taille totale de données bien plus importante, de 100 Mo ou plus, ce processus unique peut prendre encore plus de temps. Les administrateurs de clusters etcd très volumineux de cette ampleur peuvent librement contacter l'équipe [etcd][etcd-contact] avant la mise à jour, et nous serons heureux de leur fournir des conseils sur la procédure.

#### Rétrogradation {#downgrade}

Si tous les membres ont été mis à jour vers la version v3.5, le cluster sera mis à jour vers la v3.5, et un retour en arrière depuis cet état finalisé est **impossible**. Toutefois, si un seul membre reste en version v3.4, le cluster et ses opérations restent "v3.4", et il est possible, depuis cet état de cluster mixte, de revenir à l'utilisation d’un binaire etcd v3.4 sur tous les membres.

Veuillez [télécharger la sauvegarde d'instantané](/fr/etcd/op-guide/maintenance/#snapshot-backup) afin de permettre la rétrogradation du cluster, même après sa mise à jour complète.

### Procédure de mise à jour {#upgrade-procedure}

Cet exemple montre comment mettre à jour un cluster etcd v3.4 à trois membres en cours d'exécution sur une machine locale.

#### Étape 1 : vérifier les exigences de mise à jour {#step-1-check-upgrade-requirements}

Le cluster est-il sain et en cours d'exécution sous la version 3.4.x ?

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 2.118638ms
localhost:22379 is healthy: successfully committed proposal: took = 3.631388ms
localhost:32379 is healthy: successfully committed proposal: took = 2.157051ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.4.0","etcdcluster":"3.4.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.4.0","etcdcluster":"3.4.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.4.0","etcdcluster":"3.4.0"}
COMMENT
```

#### Étape 2 : télécharger la sauvegarde d'instantané depuis le leader {#step-2-download-snapshot-backup-from-leader}

[Téléchargez l'instantané de sauvegarde](/fr/etcd/op-guide/maintenance/#snapshot-backup) afin de disposer d'une voie de retour en cas de problème.

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
{"level":"info","ts":1526585787.148433,"caller":"snapshot/v3_snapshot.go:109","msg":"created temporary db file","path":"backup.db.part"}
{"level":"info","ts":1526585787.1485257,"caller":"snapshot/v3_snapshot.go:120","msg":"fetching snapshot","endpoint":"localhost:2379"}
{"level":"info","ts":1526585787.1519694,"caller":"snapshot/v3_snapshot.go:133","msg":"fetched snapshot","endpoint":"localhost:2379","took":0.003502721}
{"level":"info","ts":1526585787.1520295,"caller":"snapshot/v3_snapshot.go:142","msg":"saved","path":"backup.db"}
Snapshot saved at backup.db
COMMENT
```

#### Étape 3 : arrêter un serveur etcd existant {#step-3-stop-one-existing-etcd-server}

Lorsque chaque processus etcd est arrêté, les autres membres du cluster enregistrent des erreurs attendues. Cela est normal, car la connexion avec un membre du cluster a été (temporairement) interrompue :

```bash
{"level":"info","ts":1526587281.2001143,"caller":"etcdserver/server.go:2249","msg":"updating cluster version","from":"3.0","to":"3.4"}
{"level":"info","ts":1526587281.2010646,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","from":"3.0","from":"3.4"}
{"level":"info","ts":1526587281.2012327,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}
{"level":"info","ts":1526587281.2013083,"caller":"etcdserver/server.go:2272","msg":"cluster version is updated","cluster-version":"3.4"}



^C{"level":"info","ts":1526587299.0717514,"caller":"osutil/interrupt_unix.go:63","msg":"received signal; shutting down","signal":"interrupt"}
{"level":"info","ts":1526587299.0718873,"caller":"embed/etcd.go:285","msg":"closing etcd server","name":"s1","data-dir":"/tmp/etcd/s1","advertise-peer-urls":["http://localhost:2380"],"advertise-client-urls":["http://localhost:2379"]}
{"level":"info","ts":1526587299.0722554,"caller":"etcdserver/server.go:1341","msg":"leadership transfer starting","local-member-id":"7339c4e5e833c029","current-leader-member-id":"7339c4e5e833c029","transferee-member-id":"729934363faa4a24"}
{"level":"info","ts":1526587299.0723994,"caller":"raft/raft.go:1107","msg":"7339c4e5e833c029 [term 3] starts to transfer leadership to 729934363faa4a24"}
{"level":"info","ts":1526587299.0724802,"caller":"raft/raft.go:1113","msg":"7339c4e5e833c029 sends MsgTimeoutNow to 729934363faa4a24 immediately as 729934363faa4a24 already has up-to-date log"}
{"level":"info","ts":1526587299.0737045,"caller":"raft/raft.go:797","msg":"7339c4e5e833c029 [term: 3] received a MsgVote message with higher term from 729934363faa4a24 [term: 4]"}
{"level":"info","ts":1526587299.0737681,"caller":"raft/raft.go:656","msg":"7339c4e5e833c029 became follower at term 4"}
{"level":"info","ts":1526587299.073831,"caller":"raft/raft.go:882","msg":"7339c4e5e833c029 [logterm: 3, index: 9, vote: 0] cast MsgVote for 729934363faa4a24 [logterm: 3, index: 9] at term 4"}
{"level":"info","ts":1526587299.0738947,"caller":"raft/node.go:312","msg":"raft.node: 7339c4e5e833c029 lost leader 7339c4e5e833c029 at term 4"}
{"level":"info","ts":1526587299.0748374,"caller":"raft/node.go:306","msg":"raft.node: 7339c4e5e833c029 elected leader 729934363faa4a24 at term 4"}
{"level":"info","ts":1526587299.1726425,"caller":"etcdserver/server.go:1362","msg":"leadership transfer finished","local-member-id":"7339c4e5e833c029","old-leader-member-id":"7339c4e5e833c029","new-leader-member-id":"729934363faa4a24","took":0.100389359}
{"level":"info","ts":1526587299.1728148,"caller":"rafthttp/peer.go:333","msg":"stopping remote peer","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1751974,"caller":"rafthttp/stream.go:291","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1752589,"caller":"rafthttp/stream.go:301","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.177348,"caller":"rafthttp/stream.go:291","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1774004,"caller":"rafthttp/stream.go:301","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"b548c2511513015"}
{"level":"info","ts":1526587299.177515,"caller":"rafthttp/pipeline.go:86","msg":"stopped HTTP pipelining with remote peer","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1777067,"caller":"rafthttp/stream.go:436","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015","error":"read tcp 127.0.0.1:34636->127.0.0.1:32380: use of closed network connection"}
{"level":"info","ts":1526587299.1778402,"caller":"rafthttp/stream.go:459","msg":"stopped stream reader with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1780295,"caller":"rafthttp/stream.go:436","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015","error":"read tcp 127.0.0.1:34634->127.0.0.1:32380: use of closed network connection"}
{"level":"info","ts":1526587299.1780987,"caller":"rafthttp/stream.go:459","msg":"stopped stream reader with remote peer","stream-reader-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015"}
{"level":"info","ts":1526587299.1781602,"caller":"rafthttp/peer.go:340","msg":"stopped remote peer","remote-peer-id":"b548c2511513015"}
{"level":"info","ts":1526587299.1781986,"caller":"rafthttp/peer.go:333","msg":"stopping remote peer","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1802843,"caller":"rafthttp/stream.go:291","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1803446,"caller":"rafthttp/stream.go:301","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1824749,"caller":"rafthttp/stream.go:291","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.18255,"caller":"rafthttp/stream.go:301","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"729934363faa4a24"}
{"level":"info","ts":1526587299.18261,"caller":"rafthttp/pipeline.go:86","msg":"stopped HTTP pipelining with remote peer","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1827736,"caller":"rafthttp/stream.go:436","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24","error":"read tcp 127.0.0.1:51482->127.0.0.1:22380: use of closed network connection"}
{"level":"info","ts":1526587299.182845,"caller":"rafthttp/stream.go:459","msg":"stopped stream reader with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1830168,"caller":"rafthttp/stream.go:436","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24","error":"context canceled"}
{"level":"warn","ts":1526587299.1831107,"caller":"rafthttp/peer_status.go:65","msg":"peer became inactive","peer-id":"729934363faa4a24","error":"failed to read 729934363faa4a24 on stream Message (context canceled)"}
{"level":"info","ts":1526587299.1831737,"caller":"rafthttp/stream.go:459","msg":"stopped stream reader with remote peer","stream-reader-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24"}
{"level":"info","ts":1526587299.1832306,"caller":"rafthttp/peer.go:340","msg":"stopped remote peer","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1837125,"caller":"rafthttp/http.go:424","msg":"failed to find remote peer in cluster","local-member-id":"7339c4e5e833c029","remote-peer-id-stream-handler":"7339c4e5e833c029","remote-peer-id-from":"b548c2511513015","cluster-id":"7dee9ba76d59ed53"}
{"level":"warn","ts":1526587299.1840093,"caller":"rafthttp/http.go:424","msg":"failed to find remote peer in cluster","local-member-id":"7339c4e5e833c029","remote-peer-id-stream-handler":"7339c4e5e833c029","remote-peer-id-from":"b548c2511513015","cluster-id":"7dee9ba76d59ed53"}
{"level":"warn","ts":1526587299.1842315,"caller":"rafthttp/http.go:424","msg":"failed to find remote peer in cluster","local-member-id":"7339c4e5e833c029","remote-peer-id-stream-handler":"7339c4e5e833c029","remote-peer-id-from":"729934363faa4a24","cluster-id":"7dee9ba76d59ed53"}
{"level":"warn","ts":1526587299.1844475,"caller":"rafthttp/http.go:424","msg":"failed to find remote peer in cluster","local-member-id":"7339c4e5e833c029","remote-peer-id-stream-handler":"7339c4e5e833c029","remote-peer-id-from":"729934363faa4a24","cluster-id":"7dee9ba76d59ed53"}
{"level":"info","ts":1526587299.2056687,"caller":"embed/etcd.go:473","msg":"stopping serving peer traffic","address":"127.0.0.1:2380"}
{"level":"info","ts":1526587299.205819,"caller":"embed/etcd.go:480","msg":"stopped serving peer traffic","address":"127.0.0.1:2380"}
{"level":"info","ts":1526587299.2058413,"caller":"embed/etcd.go:289","msg":"closed etcd server","name":"s1","data-dir":"/tmp/etcd/s1","advertise-peer-urls":["http://localhost:2380"],"advertise-client-urls":["http://localhost:2379"]}
```

#### Étape 4 : redémarrer le serveur etcd avec la même configuration {#step-4-restart-the-etcd-server-with-same-configuration}

Redémarrez le serveur etcd avec la même configuration, mais avec le binaire etcd mis à jour.

```diff
-etcd-old --name s1 \
+etcd-new --name s1 \
  --data-dir /tmp/etcd/s1 \
  --listen-client-urls http://localhost:2379 \
  --advertise-client-urls http://localhost:2379 \
  --listen-peer-urls http://localhost:2380 \
  --initial-advertise-peer-urls http://localhost:2380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:22380,s3=http://localhost:32380 \
  --initial-cluster-token tkn \
  --initial-cluster-state new
```

Le nouvel etcd v3.5 publiera ses informations dans le cluster. À ce stade, le cluster continue de fonctionner selon le protocole v3.4, qui constitue la version la plus basse commune.

> `{"level":"info","ts":1526586617.1647713,"caller":"membership/cluster.go:485","msg":"set initial cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1648536,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1649303,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","from":"3.0","from":"3.4"}`

> `{"level":"info","ts":1526586617.1649797,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`

> `{"level":"info","ts":1526586617.2107732,"caller":"etcdserver/server.go:1770","msg":"published local member to cluster through raft","local-member-id":"7339c4e5e833c029","local-member-attributes":"{Name:s1 ClientURLs:[http://localhost:2379]}","request-path":"/0/members/7339c4e5e833c029/attributes","cluster-id":"7dee9ba76d59ed53","publish-timeout":7}`

Vérifiez que chaque membre, puis l’intégralité du cluster, deviennent sains avec le nouveau binaire etcd v3.5 :

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:32379 is healthy: successfully committed proposal: took = 2.337471ms
localhost:22379 is healthy: successfully committed proposal: took = 1.130717ms
localhost:2379 is healthy: successfully committed proposal: took = 2.124843ms
COMMENT
```

Les membres non mis à jour afficheront des avertissements tels que les suivants jusqu'à ce que tout le cluster soit mis à jour.

Cela est attendu et cessera une fois que tous les membres du cluster etcd auront été mis à jour vers la version 3.5 :

```
:41.942121 W | etcdserver: member 7339c4e5e833c029 has a higher version 3.5.0
:45.945154 W | etcdserver: the local etcd version 3.4.0 is not up-to-date
```

#### Étape 5 : répéter l'*étape 3* et l'*étape 4* pour les membres restants {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

Lorsque tous les membres sont mis à jour, le cluster signalera avec succès la mise à jour vers la version 3.5 :

Membre 1 :

> `{"level":"info","ts":1526586949.0920913,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`
> `{"level":"info","ts":1526586949.0921566,"caller":"etcdserver/server.go:2272","msg":"cluster version is updated","cluster-version":"3.5"}`

Membre 2 :

> `{"level":"info","ts":1526586949.092117,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"729934363faa4a24","from":"3.4","from":"3.5"}`
> `{"level":"info","ts":1526586949.0923078,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`

Membre 3 :

> `{"level":"info","ts":1526586949.0921423,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"b548c2511513015","from":"3.4","from":"3.5"}`
> `{"level":"info","ts":1526586949.0922918,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`


```bash
endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 492.834µs
localhost:22379 is healthy: successfully committed proposal: took = 1.015025ms
localhost:32379 is healthy: successfully committed proposal: took = 1.853077ms
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

[etcd-contact]: https://groups.google.com/g/etcd-dev
