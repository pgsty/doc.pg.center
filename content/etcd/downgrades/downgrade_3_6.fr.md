---
title: "Rétrogradation d'etcd de la version v3.6 à la v3.5"
weight: 6650
description: "Processus, listes de vérification et notes sur la mise à jour inverse d'etcd de la version 3.6 à la version 3.5"
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/downgrades/downgrade_3_6.md"
---

Dans le cas général, la rétrogradation de etcd v3.6 vers v3.5 peut s'effectuer sans interruption de service, en mode rolling :

-  un à un, arrêtez les processus etcd v3.6 et remplacez-les par des processus etcd v3.5
-  après avoir activé la rétrogradation, les nouvelles fonctionnalités de la version v3.6 ne sont plus disponibles pour le cluster

Avant de [effectuer une mise vers une version antérieure](#downgrade-procedure), lisez le reste du présent guide afin de vous préparer.

### Listes de vérification pour la mise à jour vers une version antérieure {#downgrade-checklists}

Changements importants marquants de la version v3.6 à la v3.5 :

#### Différence entre les drapeaux {#difference-in-flags}

Si vous utilisez l'un des drapeaux suivants dans vos configurations v3.6, veillez à les supprimer, les renommer ou modifier leur valeur par défaut lors de la mise à jour vers la version v3.5.

> [!NOTE]
> La différence est basée sur les versions v3.6.0 et v3.5.18. La différence réelle dépend de votre version de correctif ; vérifiez d'abord avec `diff <(etcd-3.6/bin/etcd -h | grep \\-\\-) <(etcd-3.5/bin/etcd -h | grep \\-\\-)`.

```diff
# flags not available in v3.5
-etcd --discovery-token ''
-etcd --discovery-endpoints ''
-etcd --discovery-dial-timeout '2s'
-etcd --discovery-request-timeout '5s'
-etcd --discovery-keepalive-time '2s'
-etcd --discovery-keepalive-timeout '6s'
-etcd --discovery-insecure-transport 'true'
-etcd --discovery-insecure-skip-tls-verify 'false'
-etcd --discovery-cert ''
-etcd --discovery-key ''
-etcd --discovery-cacert ''
-etcd --discovery-user ''
-etcd --discovery-password ''
-etcd --feature-gates
-etcd --log-format

# same flag with different names
-etcd --bootstrap-defrag-threshold-megabytes
+etcd --experimental-bootstrap-defrag-threshold-megabytes
-etcd --compaction-batch-limit
+etcd --experimental-compaction-batch-limit
-etcd --compact-hash-check-time
+etcd --experimental-compact-hash-check-time
-etcd --compaction-sleep-interval
+etcd --experimental-compaction-sleep-interval
-etcd --corrupt-check-time
+etcd --experimental-corrupt-check-time
-etcd --enable-distributed-tracing
+etcd --experimental-enable-distributed-tracing
-etcd --distributed-tracing-address
+etcd --experimental-distributed-tracing-address
-etcd --distributed-tracing-instance-id
+etcd --experimental-distributed-tracing-instance-id
-etcd --distributed-tracing-sampling-rate
+etcd --experimental-distributed-tracing-sampling-rate
-etcd --distributed-tracing-service-name
+etcd --experimental-distributed-tracing-service-name
-etcd --downgrade-check-time
+etcd --experimental-downgrade-check-time
-etcd --max-learners
+etcd --experimental-max-learners
-etcd --memory-mlock
+etcd --experimental-memory-mlock
-etcd --peer-skip-client-san-verification
+etcd --experimental-peer-skip-client-san-verification
-etcd --snapshot-catchup-entries
+etcd --experimental-snapshot-catchup-entries
-etcd --warning-apply-duration
+etcd --experimental-warning-apply-duration
-etcd --warning-unary-request-duration
+etcd --experimental-warning-unary-request-duration
-etcd --watch-progress-notify-interval
+etcd --experimental-watch-progress-notify-interval

# equivalent flags of v3.6 feature gates
-etcd --feature-gates=CompactHashCheck=true
+etcd --experimental-compact-hash-check-enabled=true
-etcd --feature-gates=InitialCorruptCheck=true
+etcd --experimental-enable-initial-corrupt-check=true
-etcd --feature-gates=LeaseCheckpoint=true
+etcd --experimental-enable-lease-checkpoint=true
-etcd --feature-gates=LeaseCheckpointPersist=true
+etcd --experimental-enable-lease-checkpoint-persist=true
-etcd --feature-gates=StopGRPCServiceOnDefrag=true
+etcd --experimental-stop-grpc-service-on-defrag=true
-etcd --feature-gates=TxnModeWriteWithSharedBuffer=false
+etcd --experimental-txn-mode-write-with-shared-buffer=false

# same flag different defaults
-etcd --snapshot-count=10000
+etcd --snapshot-count=100000
-etcd --v2-deprecation='write-only'
+etcd --v2-deprecation='not-yet'
-etcd --discovery-fallback='exit'
+etcd --discovery-fallback='proxy'

```

#### Différence entre les métriques Prometheus {#difference-in-prometheus-metrics}

```diff
# metrics not available in v3.5
-etcd_network_known_peers
-etcd_server_feature_enabled
```

### Liste de vérification pour la mise à jour vers une version antérieure du serveur {#server-downgrade-checklists}

#### Exigences de mise à jour vers une version antérieure {#downgrade-requirements}

Pour garantir une mise à jour descendante progressive sans incident, le cluster en cours d'exécution doit être sain. Vérifiez l'état du cluster à l'aide de la commande `etcdctl endpoint health` avant de poursuivre.

#### Préparation {#preparation}

Avant de procéder à une mise vers une version antérieure d’etcd, testez toujours les services dépendants d’etcd dans un environnement de préproduction avant de déployer la mise à jour vers l’environnement de production.

Avant de commencer, [téléchargez l'instantané de sauvegarde](/fr/etcd/op-guide/maintenance/#snapshot-backup). Si une erreur survient lors de la rétrogradation, il sera possible d'utiliser cette sauvegarde pour [annuler](#rollback) la mise à jour et revenir à la version existante de etcd.

Avant de commencer, téléchargez la dernière version de etcd v3.5.

#### Versions mixtes {#mixed-versions}

Lors d'une mise à jour vers une version inférieure, un cluster etcd prend en charge des versions mixtes de membres et fonctionne selon le protocole de la version commune la plus basse. Le cluster est considéré comme mis à jour vers une version inférieure une fois que la mise à jour vers une version inférieure est activée par `etcdctl downgrade enable 3.5`. Internement, la version globale du cluster est définie sur la version cible de la mise à jour vers une version inférieure, ce qui contrôle la version signalée et les fonctionnalités prises en charge.

#### Annuler {#rollback}

Avant de procéder à la mise à jour inférieure de votre cluster etcd, créez et [téléchargez une sauvegarde sous forme d'instantané](/fr/etcd/op-guide/maintenance/#snapshot-backup) de votre cluster etcd. Cet instantané peut être utilisé pour restaurer le cluster dans son état antérieur à la mise à jour si nécessaire. Si des utilisateurs rencontrent des problèmes lors de la mise à jour inférieure, ils doivent d'abord identifier et résoudre la cause racine.

Si la désinstallation a commencé après l'exécution de `etcdctl downgrade enabled`, et que le cluster est toujours dans un état mixte — où au moins un membre reste sur la version v3.6 —, les utilisateurs peuvent annuler le processus de mise à jour en cours en exécutant `etcdctl downgrade cancel`, puis en redémarrant tous les membres mis à jour avec les binaires d'origine v3.6.

Une fois que tous les membres ont été rétrogradés vers la version v3.5, le cluster est considéré comme entièrement rétrogradé. Si les utilisateurs souhaitent revenir à la version d'origine après avoir achevé un rétrogradation complète, ils doivent suivre le guide officiel d'[mise à jour](/fr/etcd/upgrades/upgrade_3_6/) afin d'assurer la cohérence et d'éviter toute corruption des données.

### Procédure de rétrogradation {#downgrade-procedure}

Cet exemple montre comment effectuer une mise à jour inverse d’un cluster etcd v3.6 à trois membres fonctionnant sur une machine locale.

#### Étape 1 : vérifier les conditions de rétrogradation {#step-1-check-downgrade-requirements}

Le cluster est-il sain et en cours d'exécution sous la version 3.6.x ?

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 2.118638ms
localhost:22379 is healthy: successfully committed proposal: took = 3.631388ms
localhost:32379 is healthy: successfully committed proposal: took = 2.157051ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT

etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |    VERSION    | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 8211f1d0f64f3269 | 3.6.0-alpha.0 |           3.6.0 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         2 |         10 |                 10 |        |                          |             false |
| localhost:22379 | 91bc3c398fb3c146 | 3.6.0-alpha.0 |           3.6.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         2 |         10 |                 10 |        |                          |             false |
| localhost:32379 | fd422379fda50e48 | 3.6.0-alpha.0 |           3.6.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         2 |         10 |                 10 |        |                          |             false |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

#### Étape 2 : télécharger la sauvegarde instantané depuis le leader {#step-2-download-snapshot-backup-from-leader}

[Téléchargez l'instantané de sauvegarde](/fr/etcd/op-guide/maintenance/#snapshot-backup) afin de disposer d'une voie de retour en cas de problème.

#### Étape 3 : valider la version cible de la mise à jour vers une version antérieure {#step-3-validate-downgrade-target-version}

Validez la version cible de la rétrogradation avant d’activer la rétrogradation :

- Nous ne supportons que le retour arrière d'une version mineure à la fois. Par exemple, le retour arrière de la version v3.6 vers la v3.4 n'est pas autorisé.
- Veuillez ne pas passer à l'étape suivante tant que la validation n'est pas réussie.

```bash
etcdctl downgrade validate 3.5
<<COMMENT
Downgrade validate success, cluster version 3.6
COMMENT
```

#### Étape 4 : activer la remontée de version {#step-4-enable-downgrade}

```bash
etcdctl downgrade enable 3.5
<<COMMENT
Downgrade enable success, cluster version 3.6
COMMENT
```

Après avoir activé la désactivation de la version, le cluster commencera à fonctionner avec le protocole v3.5, qui est la version cible de la désactivation. En outre, etcd migrera automatiquement le schéma vers la version cible de la désactivation, ce qui se produit généralement très rapidement. Vérifiez que la version de stockage de tous les serveurs a été migrée vers v3.5 en consultant l’état des points de terminaison avant de passer à l’étape suivante.

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |    VERSION    | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 8211f1d0f64f3269 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         2 |         12 |                 12 |        |                    3.5.0 |              true |
| localhost:22379 | 91bc3c398fb3c146 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         2 |         12 |                 12 |        |                    3.5.0 |              true |
| localhost:32379 | fd422379fda50e48 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         2 |         12 |                 12 |        |                    3.5.0 |              true |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

> [!NOTE]
> Une fois la désinstallation autorisée, le cluster continuera à fonctionner avec le protocole v3.5, même si tous les serveurs exécutent encore le binaire v3.6, à moins que la désinstallation ne soit annulée à l’aide de `etcdctl downgrade cancel`

#### Étape 5 : arrêter un serveur etcd existant {#step-5-stop-one-existing-etcd-server}

Avant d'arrêter le serveur, vérifiez s'il est le leader. Nous recommandons de mettre à jour le leader en dernier.

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |    VERSION    | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 8211f1d0f64f3269 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         2 |         12 |                 12 |        |                    3.5.0 |              true |
| localhost:22379 | 91bc3c398fb3c146 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         2 |         12 |                 12 |        |                    3.5.0 |              true |
| localhost:32379 | fd422379fda50e48 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         2 |         12 |                 12 |        |                    3.5.0 |              true |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

Si le serveur à arrêter est le leader, vous pouvez réduire la durée d'indisponibilité en `move-leader` vers un autre serveur avant d'arrêter ce serveur.

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 move-leader 91bc3c398fb3c146

etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |    VERSION    | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 8211f1d0f64f3269 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         3 |         13 |                 13 |        |                    3.5.0 |              true |
| localhost:22379 | 91bc3c398fb3c146 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         3 |         13 |                 13 |        |                    3.5.0 |              true |
| localhost:32379 | fd422379fda50e48 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         3 |         13 |                 13 |        |                    3.5.0 |              true |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

Lorsque chaque processus etcd est arrêté, les autres membres du cluster enregistrent des erreurs attendues. Cela est normal, car la connexion avec un membre du cluster a été (temporairement) interrompue :

```bash
{"level":"warn","ts":"2025-02-28T17:35:43.795069Z","caller":"etcdserver/cluster_util.go:259","msg":"failed to reach the peer URL","address":"http://127.0.0.1:12380/version","remote-member-id":"8211f1d0f64f3269","error":"Get \"http://127.0.0.1:12380/version\": dial tcp 127.0.0.1:12380: connect: connection refused"}
{"level":"warn","ts":"2025-02-28T17:35:43.795149Z","caller":"etcdserver/cluster_util.go:160","msg":"failed to get version","remote-member-id":"8211f1d0f64f3269","error":"Get \"http://127.0.0.1:12380/version\": dial tcp 127.0.0.1:12380: connect: connection refused"}
{"level":"warn","ts":"2025-02-28T17:35:44.368651Z","caller":"rafthttp/probing_status.go:68","msg":"prober detected unhealthy status","round-tripper-name":"ROUND_TRIPPER_SNAPSHOT","remote-peer-id":"8211f1d0f64f3269","rtt":"483.01µs","error":"dial tcp 127.0.0.1:12380: connect: connection refused"}
{"level":"warn","ts":"2025-02-28T17:35:44.368726Z","caller":"rafthttp/probing_status.go:68","msg":"prober detected unhealthy status","round-tripper-name":"ROUND_TRIPPER_RAFT_MESSAGE","remote-peer-id":"8211f1d0f64f3269","rtt":"735.659µs","error":"dial tcp 127.0.0.1:12380: connect: connection refused"}
```

#### Étape 6 : redémarrer le serveur etcd avec la même configuration (sans les indicateurs supprimés ou remplacés dans la version 3.5) {#step-6-restart-the-etcd-server-with-same-configuration-minus-the-flags-that-are-removed-or-replaced-in-v35}

Redémarrez le serveur etcd avec la même configuration, mais avec le binaire etcd mis à jour.

```diff
-etcd-3.6/bin --name s1 \
+etcd-3.5/bin --name s1 \
  --data-dir /tmp/etcd/s1 \
  --listen-client-urls http://localhost:2379 \
  --advertise-client-urls http://localhost:2379 \
  --listen-peer-urls http://localhost:2380 \
  --initial-advertise-peer-urls http://localhost:2380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:22380,s3=http://localhost:32380 \
  --initial-cluster-token tkn \
  --initial-cluster-state existing
```

Vérifiez que chaque membre, puis l’intégralité du cluster, deviennent sains avec la nouvelle binaire etcd v3.5 :

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |    VERSION    | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 8211f1d0f64f3269 |        3.5.18 |                 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         3 |         14 |                 14 |        |                          |             false |
| localhost:22379 | 91bc3c398fb3c146 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         3 |         14 |                 14 |        |                    3.5.0 |              true |
| localhost:32379 | fd422379fda50e48 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         3 |         14 |                 14 |        |                    3.5.0 |              true |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT

etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:22379 is healthy: successfully committed proposal: took = 4.650967ms
localhost:2379 is healthy: successfully committed proposal: took = 4.634377ms
localhost:32379 is healthy: successfully committed proposal: took = 5.047777ms
COMMENT
```

> [!NOTE]
> Vous verrez que `DOWNGRADE ENABLED` est false pour le serveur v3.5, car les informations de rétrogradation ne sont pas implémentées dans le point de terminaison d'état de la v3.5 ; la rétrogradation reste toutefois activée pour le cluster à ce stade.

#### Étape 7 : répéter *étape 5* et *étape 6* pour les membres restants {#step-7-repeat-step-5-and-step-6-for-rest-of-the-members}

Lorsque tous les membres sont rétrogradés, vérifiez l’état et la santé du cluster, puis confirmez que la version mineure de tous les membres est v3.5 et que la version de stockage est vide :

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        | VERSION | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 8211f1d0f64f3269 |  3.5.18 |                 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         3 |         26 |                 26 |        |                          |             false |
| localhost:22379 | 91bc3c398fb3c146 |  3.5.18 |                 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         3 |         26 |                 26 |        |                          |             false |
| localhost:32379 | fd422379fda50e48 |  3.5.18 |                 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         3 |         26 |                 26 |        |                          |             false |
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT

etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:22379 is healthy: successfully committed proposal: took = 4.650967ms
localhost:2379 is healthy: successfully committed proposal: took = 4.634377ms
localhost:32379 is healthy: successfully committed proposal: took = 5.047777ms
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

Dans le journal du leader, vous devriez être en mesure de voir un message similaire au suivant :

```bash
{"level":"info","ts":"2025-02-28T17:59:50.019862Z","caller":"etcdserver/server.go:2749","msg":"the cluster has been downgraded","cluster-version":"3.5.0"}
```
