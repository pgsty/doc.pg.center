---
title: Mettre à jour etcd de 3.3 à 3.4
weight: 6700
description: "Processus, listes de vérification et notes sur la mise à niveau d'etcd de la version 3.3 à la 3.4"
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_4.md"
aliases: [/etcd/upgrades/upgrade_3_4/]
---

Dans le cas général, la mise à niveau d’etcd 3.3 vers 3.4 peut s'effectuer sans interruption de service, par mise à niveau progressive :
 - un par un, arrêtez les processus etcd v3.3 et remplacez-les par des processus etcd v3.4
 - après avoir lancé tous les processus v3.4, les nouvelles fonctionnalités de la version v3.4 sont disponibles pour le cluster

Avant de [lancer la mise à jour](#upgrade-procedure), lisez le reste du présent guide afin de vous préparer.



### Listes de vérification pour la mise à jour {#upgrade-checklists}

> [!WARNING]
> Lorsque [on migre depuis la version v2 sans données v3](https://github.com/etcd-io/etcd/issues/9480), le serveur etcd v3.2+ provoque une panne lorsqu'il restaure à partir d'un instantané existant mais qu'aucun fichier v3 `ETCD_DATA_DIR/member/snap/db` n'est présent. Cela se produit lorsque le serveur a été migré depuis la version v2 sans données v3 précédentes. Cela empêche également la perte accidentelle de données v3 (par exemple, le fichier `db` pourrait avoir été déplacé). etcd exige que les opérations après migration vers v3 ne soient effectuées que si des données v3 sont présentes. N'effectuez pas la mise à jour vers des versions v3 plus récentes tant que le serveur v3.0 ne contient pas de données v3.

Changements de rupture mis en évidence dans la version 3.4.

#### Rendre `ETCDCTL_API=3 etcdctl` par défaut {#make-etcdctl_api3-etcdctl-default}

`ETCDCTL_API=3` est désormais la valeur par défaut.

```diff
etcdctl set foo bar
Error: unknown command "set" for "etcdctl"

-etcdctl set foo bar
+ETCDCTL_API=2 etcdctl set foo bar
bar

ETCDCTL_API=3 etcdctl put foo bar
OK

-ETCDCTL_API=3 etcdctl put foo bar
+etcdctl put foo bar
```

#### Rendre `etcd --enable-v2=false` par défaut {#make-etcd---enable-v2false-default}

[`etcd --enable-v2=false`](https://github.com/etcd-io/etcd/pull/10935) est désormais la valeur par défaut.

Cela signifie qu'à moins que `etcd --enable-v2=true` ne soit spécifié, le serveur etcd v3.4 n'acceptera pas les requêtes de l'API v2.

Si l'API v2 était utilisée, assurez-vous d'activer l'API v2 dans la version 3.4 :

```diff
-etcd
+etcd --enable-v2=true
```

D'autres API HTTP fonctionneront toujours (par exemple `[CLIENT-URL]/metrics`, `[CLIENT-URL]/health`, passerelle gRPC v3).

#### Dépréciation des drapeaux `etcd --ca-file` et `etcd --peer-ca-file` {#deprecated-etcd---ca-file-and-etcd---peer-ca-file-flags}

Les drapeaux `--ca-file` et `--peer-ca-file` sont obsolètes ; ils ont été dépréciés depuis la version v2.1.

Note : la configuration de ce paramètre active automatiquement l'authentification par certificat client, quelle que soit la valeur définie pour `--client-cert-auth`.

```diff
-etcd --ca-file ca-client.crt
+etcd --trusted-ca-file ca-client.crt
```

```diff
-etcd --peer-ca-file ca-peer.crt
+etcd --peer-trusted-ca-file ca-peer.crt
```

#### Erreur `grpc.ErrClientConnClosing` obsolète {#deprecated-grpcerrclientconnclosing-error}

`grpc.ErrClientConnClosing` a été [déprécié dans gRPC >= 1.10](https://github.com/grpc/grpc-go/pull/1854).

```diff
import (
+	"go.etcd.io/etcd/clientv3"

	"google.golang.org/grpc"
+	"google.golang.org/grpc/codes"
+	"google.golang.org/grpc/status"
)

_, err := kvc.Get(ctx, "a")
-if err == grpc.ErrClientConnClosing {
+if clientv3.IsConnCanceled(err) {

// or
+s, ok := status.FromError(err)
+if ok {
+  if s.Code() == codes.Canceled
```

#### Exiger `grpc.WithBlock` pour la connexion client {#require-grpcwithblock-for-client-dial}

[Le nouveau répartiteur de charge client](/fr/docs/etcd/learning/design-client/) utilise un résolveur asynchrone pour transmettre les points de terminaison à la fonction gRPC dial. En conséquence, le client v3.4 exige l'option `grpc.WithBlock` pour attendre que la connexion sous-jacente soit active.

```diff
import (
	"time"
	"go.etcd.io/etcd/clientv3"
+	"google.golang.org/grpc"
)

+// "grpc.WithBlock()" to block until the underlying connection is up
ccfg := clientv3.Config{
  Endpoints:            []string{"localhost:2379"},
  DialTimeout:          time.Second,
+ DialOptions:          []grpc.DialOption{grpc.WithBlock()},
  DialKeepAliveTime:    time.Second,
  DialKeepAliveTimeout: 500 * time.Millisecond,
}
```

#### Dépréciation des métriques Prometheus `etcd_debugging_mvcc_db_total_size_in_bytes` {#deprecating-etcd_debugging_mvcc_db_total_size_in_bytes-prometheus-metrics}

v3.4 promeut les métriques Prometheus `etcd_debugging_mvcc_db_total_size_in_bytes` vers `etcd_mvcc_db_total_size_in_bytes`, afin d'encourager la surveillance du stockage etcd.

`etcd_debugging_mvcc_db_total_size_in_bytes` est toujours fourni dans la version 3.4 pour des raisons de compatibilité descendante. Il sera complètement obsolète dans la version 3.5.

```diff
-etcd_debugging_mvcc_db_total_size_in_bytes
+etcd_mvcc_db_total_size_in_bytes
```

Notez que les métriques de l'espace de noms `etcd_debugging_*` sont marquées comme expérimentales. Au fur et à mesure que nous améliorons le guide de surveillance, certaines métriques pourraient être promues.

#### Dépréciation des métriques Prometheus `etcd_debugging_mvcc_put_total` {#deprecating-etcd_debugging_mvcc_put_total-prometheus-metrics}

v3.4 promeut les métriques Prometheus `etcd_debugging_mvcc_put_total` vers `etcd_mvcc_put_total`, afin d'encourager la surveillance du stockage etcd.

`etcd_debugging_mvcc_put_total` est toujours fourni dans la version 3.4 pour des raisons de compatibilité descendante. Il sera complètement obsolète dans la version 3.5.

```diff
-etcd_debugging_mvcc_put_total
+etcd_mvcc_put_total
```

Notez que les métriques de l'espace de noms `etcd_debugging_*` sont marquées comme expérimentales. Au fur et à mesure que nous améliorons le guide de surveillance, certaines métriques pourraient être promues.

#### Dépréciation des métriques Prometheus `etcd_debugging_mvcc_delete_total` {#deprecating-etcd_debugging_mvcc_delete_total-prometheus-metrics}

v3.4 promeut les métriques Prometheus `etcd_debugging_mvcc_delete_total` vers `etcd_mvcc_delete_total`, afin d'encourager la surveillance du stockage etcd.

`etcd_debugging_mvcc_delete_total` est toujours fourni dans la version 3.4 pour des raisons de compatibilité descendante. Il sera complètement obsolète dans la version 3.5.

```diff
-etcd_debugging_mvcc_delete_total
+etcd_mvcc_delete_total
```

Notez que les métriques de l'espace de noms `etcd_debugging_*` sont marquées comme expérimentales. Au fur et à mesure que nous améliorons le guide de surveillance, certaines métriques pourraient être promues.

#### Dépréciation des métriques Prometheus `etcd_debugging_mvcc_txn_total` {#deprecating-etcd_debugging_mvcc_txn_total-prometheus-metrics}

v3.4 promeut les métriques Prometheus `etcd_debugging_mvcc_txn_total` vers `etcd_mvcc_txn_total`, afin d'encourager la surveillance du stockage etcd.

`etcd_debugging_mvcc_txn_total` est toujours fourni dans la version 3.4 pour des raisons de compatibilité descendante. Il sera complètement obsolète dans la version 3.5.

```diff
-etcd_debugging_mvcc_txn_total
+etcd_mvcc_txn_total
```

Notez que les métriques de l'espace de noms `etcd_debugging_*` sont marquées comme expérimentales. Au fur et à mesure que nous améliorons le guide de surveillance, certaines métriques pourraient être promues.

#### Dépréciation des métriques Prometheus `etcd_debugging_mvcc_range_total` {#deprecating-etcd_debugging_mvcc_range_total-prometheus-metrics}

v3.4 promeut les métriques Prometheus `etcd_debugging_mvcc_range_total` vers `etcd_mvcc_range_total`, afin d'encourager la surveillance du stockage etcd.

`etcd_debugging_mvcc_range_total` est toujours fourni dans la version 3.4 pour des raisons de compatibilité descendante. Il sera complètement obsolète dans la version 3.5.

```diff
-etcd_debugging_mvcc_range_total
+etcd_mvcc_range_total
```

Notez que les métriques de l'espace de noms `etcd_debugging_*` sont marquées comme expérimentales. Au fur et à mesure que nous améliorons le guide de surveillance, certaines métriques pourraient être promues.

#### Dépréciation du drapeau `etcd --log-output` (maintenant `--log-outputs`) {#deprecating-etcd---log-output-flag-now---log-outputs}

Renommez [`etcd --log-output` en `--log-outputs`](https://github.com/etcd-io/etcd/pull/9624) pour prendre en charge plusieurs sorties de journalisation. **`etcd --logger=capnslog` ne prend pas en charge plusieurs sorties de journalisation.**

**`etcd --log-output`** sera obsolète à partir de la version 3.5. **`etcd --logger=capnslog` sera obsolète à partir de la version 3.5**.

```diff
-etcd --log-output=stderr
+etcd --log-outputs=stderr

+# to write logs to stderr and a.log file at the same time
+# only "--logger=zap" supports multiple writers
+etcd --logger=zap --log-outputs=stderr,a.log
```

v3.4 ajoute la prise en charge de `etcd --logger=zap --log-outputs=stderr` pour la journalisation structurée et plusieurs sorties de journal. La motivation principale est de favoriser la surveillance automatisée d'etcd, plutôt que d'analyser les journaux serveur après une panne. Les développements futurs viseront à réduire au minimum la quantité de logs générés par etcd, et à faciliter sa surveillance grâce aux métriques et aux alertes. **`etcd --logger=capnslog` sera déprécié à partir de v3.5**.

#### Changer le type de champ `log-outputs` dans `etcd --config-file` en `[]string` {#changed-log-outputs-field-type-in-etcd---config-file-to-string}

À présent que `log-outputs` (ancien nom de champ `log-output`) accepte plusieurs sorties de journalisation, le champ du fichier YAML de configuration etcd `log-outputs` doit être modifié en type `[]string` comme indiqué ci-dessous :

```diff
 # Specify 'stdout' or 'stderr' to skip journald logging even when running under systemd.
-log-output: default
+log-outputs: [default]
```

#### Renommer `embed.Config.LogOutput` en `embed.Config.LogOutputs` {#renamed-embedconfiglogoutput-to-embedconfiglogoutputs}

[**`embed.Config.LogOutput`** a été renommé en **`embed.Config.LogOutputs`**](https://github.com/etcd-io/etcd/pull/9624) afin de prendre en charge plusieurs sorties de journalisation. Le type de [`embed.Config.LogOutput` est également passé de `string` à `[]string`](https://github.com/etcd-io/etcd/pull/9579) afin de prendre en charge plusieurs sorties de journalisation.

```diff
import "github.com/coreos/etcd/embed"

cfg := &embed.Config{Debug: false}
-cfg.LogOutput = "stderr"
+cfg.LogOutputs = []string{"stderr"}
```

#### v3.5 déprécie `capnslog` {#v35-deprecates-capnslog}

**v3.5 dépréciera le drapeau `etcd --log-package-levels` pour `capnslog`** ; `etcd --logger=zap --log-outputs=stderr` sera la valeur par défaut. **v3.5 dépréciera l'endpoint `[CLIENT-URL]/config/local/log`.**

```diff
-etcd
+etcd --logger zap
```

#### Dépréciation du drapeau `etcd --debug` (maintenant `--log-level=debug`) {#deprecating-etcd---debug-flag-now---log-leveldebug}

La version 3.4 déprécie l'utilisation du drapeau [`etcd --debug`](https://github.com/etcd-io/etcd/pull/10947). À la place, utilisez le drapeau `etcd --log-level=debug`.

```diff
-etcd --debug
+etcd --logger zap --log-level debug
```

#### Champ `pkg/transport.TLSInfo.CAFile` obsolète {#deprecated-pkgtransporttlsinfocafile-field}

Champ `pkg/transport.TLSInfo.CAFile` obsolète.

```diff
import "github.com/coreos/etcd/pkg/transport"

tlsInfo := transport.TLSInfo{
    CertFile: "/tmp/test-certs/test.pem",
    KeyFile: "/tmp/test-certs/test-key.pem",
-   CAFile: "/tmp/test-certs/trusted-ca.pem",
+   TrustedCAFile: "/tmp/test-certs/trusted-ca.pem",
}
tlsConfig, err := tlsInfo.ClientConfig()
if err != nil {
    panic(err)
}
```

#### Modifier `embed.Config.SnapCount` en `embed.Config.SnapshotCount` {#changed-embedconfigsnapcount-to-embedconfigsnapshotcount}

Pour rester cohérent avec le nom du drapeau `etcd --snapshot-count`, le champ `embed.Config.SnapCount` a été renommé en `embed.Config.SnapshotCount` :

```diff
import "github.com/coreos/etcd/embed"

cfg := embed.NewConfig()
-cfg.SnapCount = 100000
+cfg.SnapshotCount = 100000
```

#### Modifier `etcdserver.ServerConfig.SnapCount` en `etcdserver.ServerConfig.SnapshotCount` {#changed-etcdserverserverconfigsnapcount-to-etcdserverserverconfigsnapshotcount}

Pour rester cohérent avec le nom du drapeau `etcd --snapshot-count`, le champ `etcdserver.ServerConfig.SnapCount` a été renommé en `etcdserver.ServerConfig.SnapshotCount` :

```diff
import "github.com/coreos/etcd/etcdserver"

srvcfg := etcdserver.ServerConfig{
-  SnapCount: 100000,
+  SnapshotCount: 100000,
```

#### Signature de fonction modifiée dans le package `wal` {#changed-function-signature-in-package-wal}

Les signatures de fonction de `wal` ont été modifiées pour prendre en charge le journalisateur structuré.

```diff
import "github.com/coreos/etcd/wal"
+import "go.uber.org/zap"

+lg, _ = zap.NewProduction()

-wal.Open(dirpath, snap)
+wal.Open(lg, dirpath, snap)

-wal.OpenForRead(dirpath, snap)
+wal.OpenForRead(lg, dirpath, snap)

-wal.Repair(dirpath)
+wal.Repair(lg, dirpath)

-wal.Create(dirpath, metadata)
+wal.Create(lg, dirpath, metadata)
```

#### Modifier le type `IntervalTree` dans le package `pkg/adt` {#changed-intervaltree-type-in-package-pkgadt}

`pkg/adt.IntervalTree` est désormais défini comme une `interface`.

```diff
import (
    "fmt"

    "go.etcd.io/etcd/pkg/adt"
)

func main() {
-    ivt := &adt.IntervalTree{}
+    ivt := adt.NewIntervalTree()
```

#### Dépréciation de `embed.Config.SetupLogging` {#deprecated-embedconfigsetuplogging}

`embed.Config.SetupLogging` a été supprimé afin d'éviter une configuration incorrecte de la journalisation, et est désormais configuré automatiquement.

```diff
import "github.com/coreos/etcd/embed"

cfg := &embed.Config{Debug: false}
-cfg.SetupLogging()
```

#### Modifier les points d'entrée HTTP de la passerelle gRPC (remplacé `/v3beta` par `/v3`) {#changed-grpc-gateway-http-endpoints-replaced-v3beta-with-v3}

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

Les requêtes vers les points de terminaison `/v3beta` seront redirigées vers `/v3`, et `/v3beta` sera supprimé dans la version 3.5.

#### Balises d'image conteneur obsolètes {#deprecated-container-image-tags}

`latest` et les balises de version mineure sont obsolètes :

```diff
-docker pull gcr.io/etcd-development/etcd:latest
+docker pull gcr.io/etcd-development/etcd:v3.4.0

-docker pull gcr.io/etcd-development/etcd:v3.4
+docker pull gcr.io/etcd-development/etcd:v3.4.0

-docker pull gcr.io/etcd-development/etcd:v3.4
+docker pull gcr.io/etcd-development/etcd:v3.4.1

-docker pull gcr.io/etcd-development/etcd:v3.4
+docker pull gcr.io/etcd-development/etcd:v3.4.2
```

### Liste de vérification pour la mise à jour du serveur {#server-upgrade-checklists}

#### Exigences de mise à jour {#upgrade-requirements}

Pour mettre à jour un déploiement etcd existant vers la version 3.4, le cluster en cours d'exécution doit être la version 3.3 ou ultérieure. Si la version est antérieure à 3.3, veuillez [mettre à jour vers la version 3.3](/fr/docs/etcd/upgrades/upgrade_3_3/) avant de procéder à la mise à jour vers la version 3.4.

En outre, pour garantir une mise à niveau progressive sans incident, le cluster en cours d'exécution doit être sain. Vérifiez l'état de santé du cluster à l'aide de la commande `etcdctl endpoint health` avant de poursuivre.

#### Préparation {#preparation}

Avant de mettre à jour etcd, testez toujours les services dépendants d’etcd dans un environnement de préproduction avant de déployer la mise à jour dans l’environnement de production.

Avant de commencer, [téléchargez la sauvegarde d'instantané](/fr/docs/etcd/op-guide/maintenance/#snapshot-backup). Si une erreur survient lors de la mise à jour, il sera possible d'utiliser cette sauvegarde pour [rétrograder](#downgrade) vers la version existante d’etcd. Veuillez noter que la commande `snapshot` ne sauvegarde que les données v3. Pour les données v2, consultez [sauvegarde du magasin de données v2](https://etcd.io/docs/v2.3/admin_guide/#backing-up-the-datastore).

#### Versions mixtes {#mixed-versions}

Lors d'une mise à jour, un cluster etcd prend en charge des versions mixtes de membres et fonctionne selon le protocole de la version commune la plus basse. Le cluster n'est considéré comme mis à jour qu'une fois que tous ses membres ont été mis à jour vers la version 3.4. En interne, les membres etcd négocient entre eux afin de déterminer la version globale du cluster, qui contrôle la version signalée et les fonctionnalités prises en charge.

#### Limitations {#limitations}

Note : Si le cluster ne contient que des données v3 et aucune donnée v2, il n'est pas soumis à cette limitation.

Si le cluster sert un jeu de données v2 dont la taille dépasse 50 Mo, chaque membre nouvellement mis à jour peut prendre jusqu’à deux minutes pour rattraper le cluster existant. Vérifiez la taille d’un instantané récent afin d’estimer la taille totale des données. Autrement dit, le plus sûr est d’attendre deux minutes entre chaque mise à jour de membre.

Pour une taille totale de données bien plus importante, de 100 Mo ou plus, ce processus unique peut prendre encore plus de temps. Les administrateurs de clusters etcd très volumineux de cette ampleur peuvent librement contacter l'équipe [etcd][etcd-contact] avant la mise à jour, et nous serons heureux de leur fournir des conseils sur la procédure.

#### Rétrogradation {#downgrade}

Si tous les membres ont été mis à jour vers la version v3.4, le cluster sera mis à jour vers la version v3.4, et un retour en arrière depuis cet état finalisé est **impossible**. Toutefois, si un seul membre reste en version v3.3, le cluster et ses opérations restent "v3.3", et il est possible, depuis cet état de cluster mixte, de revenir à l'utilisation d’un binaire etcd v3.3 sur tous les membres.

Veuillez [télécharger la sauvegarde d'instantané](/fr/docs/etcd/op-guide/maintenance/#snapshot-backup) afin de permettre la rétrogradation du cluster, même après sa mise à jour complète.

### Procédure de mise à jour {#upgrade-procedure}

Cet exemple montre comment mettre à jour un cluster etcd v3.3 composé de 3 membres, en cours d'exécution sur une machine locale.

#### Étape 1 : vérifier les exigences de mise à jour {#step-1-check-upgrade-requirements}

Le cluster est-il sain et en cours d'exécution sous la version 3.3.x ?

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 2.118638ms
localhost:22379 is healthy: successfully committed proposal: took = 3.631388ms
localhost:32379 is healthy: successfully committed proposal: took = 2.157051ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.3.5","etcdcluster":"3.3.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.3.5","etcdcluster":"3.3.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.3.5","etcdcluster":"3.3.0"}
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
10.237579 I | etcdserver: updating the cluster version from 3.0 to 3.3
10.238315 N | etcdserver/membership: updated the cluster version from 3.0 to 3.3
10.238451 I | etcdserver/api: enabled capabilities for version 3.3


^C21.192174 N | pkg/osutil: received interrupt signal, shutting down...
21.192459 I | etcdserver: 7339c4e5e833c029 starts leadership transfer from 7339c4e5e833c029 to 729934363faa4a24
21.192569 I | raft: 7339c4e5e833c029 [term 8] starts to transfer leadership to 729934363faa4a24
21.192619 I | raft: 7339c4e5e833c029 sends MsgTimeoutNow to 729934363faa4a24 immediately as 729934363faa4a24 already has up-to-date log
WARNING: 2018/05/17 12:45:21 grpc: addrConn.resetTransport failed to create client transport: connection error: desc = "transport: Error while dialing dial tcp: operation was canceled"; Reconnecting to {localhost:2379 0  <nil>}
WARNING: 2018/05/17 12:45:21 grpc: addrConn.transportMonitor exits due to: grpc: the connection is closing
21.193589 I | raft: 7339c4e5e833c029 [term: 8] received a MsgVote message with higher term from 729934363faa4a24 [term: 9]
21.193626 I | raft: 7339c4e5e833c029 became follower at term 9
21.193651 I | raft: 7339c4e5e833c029 [logterm: 8, index: 9, vote: 0] cast MsgVote for 729934363faa4a24 [logterm: 8, index: 9] at term 9
21.193675 I | raft: raft.node: 7339c4e5e833c029 lost leader 7339c4e5e833c029 at term 9
21.194424 I | raft: raft.node: 7339c4e5e833c029 elected leader 729934363faa4a24 at term 9
21.292898 I | etcdserver: 7339c4e5e833c029 finished leadership transfer from 7339c4e5e833c029 to 729934363faa4a24 (took 100.436391ms)
21.292975 I | rafthttp: stopping peer 729934363faa4a24...
21.293206 I | rafthttp: closed the TCP streaming connection with peer 729934363faa4a24 (stream MsgApp v2 writer)
21.293225 I | rafthttp: stopped streaming with peer 729934363faa4a24 (writer)
21.293437 I | rafthttp: closed the TCP streaming connection with peer 729934363faa4a24 (stream Message writer)
21.293459 I | rafthttp: stopped streaming with peer 729934363faa4a24 (writer)
21.293514 I | rafthttp: stopped HTTP pipelining with peer 729934363faa4a24
21.293590 W | rafthttp: lost the TCP streaming connection with peer 729934363faa4a24 (stream MsgApp v2 reader)
21.293610 I | rafthttp: stopped streaming with peer 729934363faa4a24 (stream MsgApp v2 reader)
21.293680 W | rafthttp: lost the TCP streaming connection with peer 729934363faa4a24 (stream Message reader)
21.293700 I | rafthttp: stopped streaming with peer 729934363faa4a24 (stream Message reader)
21.293711 I | rafthttp: stopped peer 729934363faa4a24
21.293720 I | rafthttp: stopping peer b548c2511513015...
21.293987 I | rafthttp: closed the TCP streaming connection with peer b548c2511513015 (stream MsgApp v2 writer)
21.294063 I | rafthttp: stopped streaming with peer b548c2511513015 (writer)
21.294467 I | rafthttp: closed the TCP streaming connection with peer b548c2511513015 (stream Message writer)
21.294561 I | rafthttp: stopped streaming with peer b548c2511513015 (writer)
21.294742 I | rafthttp: stopped HTTP pipelining with peer b548c2511513015
21.294867 W | rafthttp: lost the TCP streaming connection with peer b548c2511513015 (stream MsgApp v2 reader)
21.294892 I | rafthttp: stopped streaming with peer b548c2511513015 (stream MsgApp v2 reader)
21.294990 W | rafthttp: lost the TCP streaming connection with peer b548c2511513015 (stream Message reader)
21.295004 E | rafthttp: failed to read b548c2511513015 on stream Message (context canceled)
21.295013 I | rafthttp: peer b548c2511513015 became inactive
21.295024 I | rafthttp: stopped streaming with peer b548c2511513015 (stream Message reader)
21.295035 I | rafthttp: stopped peer b548c2511513015
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
+ --initial-cluster-state new \
+ --logger zap \
+ --log-outputs stderr
```

Le nouvel etcd v3.4 publiera ses informations dans le cluster. À ce stade, le cluster continue de fonctionner selon le protocole v3.3, qui constitue la version la plus basse commune.

> `{"level":"info","ts":1526586617.1647713,"caller":"membership/cluster.go:485","msg":"set initial cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1648536,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1649303,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","from":"3.0","from":"3.3"}`

> `{"level":"info","ts":1526586617.1649797,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.3"}`

> `{"level":"info","ts":1526586617.2107732,"caller":"etcdserver/server.go:1770","msg":"published local member to cluster through raft","local-member-id":"7339c4e5e833c029","local-member-attributes":"{Name:s1 ClientURLs:[http://localhost:2379]}","request-path":"/0/members/7339c4e5e833c029/attributes","cluster-id":"7dee9ba76d59ed53","publish-timeout":7}`

Vérifiez que chaque membre, puis l’ensemble du cluster, devient sain avec le binaire etcd v3.4 nouvellement installé :

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:32379 is healthy: successfully committed proposal: took = 2.337471ms
localhost:22379 is healthy: successfully committed proposal: took = 1.130717ms
localhost:2379 is healthy: successfully committed proposal: took = 2.124843ms
COMMENT
```

Les membres non mis à jour afficheront des avertissements tels que les suivants jusqu'à ce que tout le cluster soit mis à jour.

Cela est attendu et cessera une fois que tous les membres du cluster etcd auront été mis à jour vers la version 3.4 :

```
:41.942121 W | etcdserver: member 7339c4e5e833c029 has a higher version 3.4.0
:45.945154 W | etcdserver: the local etcd version 3.3.5 is not up-to-date
```

#### Étape 5 : répéter l'*étape 3* et l'*étape 4* pour les membres restants {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

Lorsque tous les membres sont mis à jour, le cluster signalera avec succès la mise à jour vers la version 3.4 :

Membre 1 :

> `{"level":"info","ts":1526586949.0920913,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`
> `{"level":"info","ts":1526586949.0921566,"caller":"etcdserver/server.go:2272","msg":"cluster version is updated","cluster-version":"3.4"}`

Membre 2 :

> `{"level":"info","ts":1526586949.092117,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"729934363faa4a24","from":"3.3","from":"3.4"}`
> `{"level":"info","ts":1526586949.0923078,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`

Membre 3 :

> `{"level":"info","ts":1526586949.0921423,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"b548c2511513015","from":"3.3","from":"3.4"}`
> `{"level":"info","ts":1526586949.0922918,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`


```bash
endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 492.834µs
localhost:22379 is healthy: successfully committed proposal: took = 1.015025ms
localhost:32379 is healthy: successfully committed proposal: took = 1.853077ms
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

[etcd-contact]: https://groups.google.com/g/etcd-dev
