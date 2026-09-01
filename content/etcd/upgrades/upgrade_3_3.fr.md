---
title: Mettre à jour etcd de 3.2 vers 3.3
weight: 6750
description: "Processus, listes de vérification et notes sur la mise à jour d’etcd de la version 3.2 à la 3.3"
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/upgrades/upgrade_3_3.md"
---

Dans le cas général, la mise à niveau de etcd 3.2 vers 3.3 peut être effectuée sans interruption de service, par mise à niveau progressive :
 - un par un, arrêtez les processus etcd v3.2 et remplacez-les par des processus etcd v3.3
 - après avoir lancé tous les processus v3.3, les nouvelles fonctionnalités de la version v3.3 sont disponibles pour le cluster

Avant de [lancer la mise à jour](#upgrade-procedure), lisez le reste du présent guide afin de vous préparer.

### Listes de vérification pour la mise à jour {#upgrade-checklists}

> [!WARNING]
> Lorsque [on migre depuis la version v2 sans données v3](https://github.com/etcd-io/etcd/issues/9480), le serveur etcd v3.2+ provoque une panne lorsqu'il restaure à partir d'un instantané existant mais qu'aucun fichier v3 `ETCD_DATA_DIR/member/snap/db` n'est présent. Cela se produit lorsque le serveur a été migré depuis la version v2 sans données v3 précédentes. Cela empêche également la perte accidentelle de données v3 (par exemple, le fichier `db` pourrait avoir été déplacé). etcd exige que la migration post-v3 ne puisse avoir lieu qu'avec des données v3 présentes. N'effectuez pas la mise à jour vers des versions v3 plus récentes tant que le serveur v3.0 ne contient pas de données v3.

> [!WARNING]
> si vous activez l'authentification et utilisez des bails (avec une durée de vie courte), il y a de fortes chances de rencontrer un [problème](https://github.com/etcd-io/etcd/issues/11689) entraînant une incohérence des données. Il est fortement recommandé de mettre à jour vers 3.2.31 ou ultérieur avant toute mise à jour vers 3.3, afin de corriger ce problème. En outre, si un utilisateur sans autorisation envoie une requête `LeaseRevoke` à un nœud 3.3 pendant la mise à jour, cela peut encore provoquer une corruption des données. Il est donc préférable de s'assurer que votre environnement ne contient pas d'appels anormaux avant la mise à jour ; consultez [#11691](https://github.com/etcd-io/etcd/pull/11691) pour plus de détails.


Changements importants marquants dans 3.3.

#### Changement du type de valeur du drapeau `etcd --auto-compaction-retention` en `string` {#changed-value-type-of-etcd---auto-compaction-retention-flag-to-string}

Modifié le drapeau `--auto-compaction-retention` en [acceptant des valeurs de type chaîne](https://github.com/etcd-io/etcd/pull/8563) avec [une granularité plus fine](https://github.com/etcd-io/etcd/issues/8503). À présent que `--auto-compaction-retention` accepte des valeurs de type chaîne, le champ du fichier YAML de configuration etcd `auto-compaction-retention` doit être modifié en `string` type. Auparavant, `--config-file etcd.config.yaml` pouvait inclure le champ `auto-compaction-retention: 24`, désormais il doit être `auto-compaction-retention: "24"` ou `auto-compaction-retention: "24h"`. Si configuré comme `--auto-compaction-mode periodic --auto-compaction-retention "24h"`, la valeur de durée pour le drapeau `--auto-compaction-retention` doit être valide pour la fonction [`time.ParseDuration`](https://golang.org/pkg/time/#ParseDuration) en Go.

```diff
# etcd.config.yaml
+auto-compaction-mode: periodic
-auto-compaction-retention: 24
+auto-compaction-retention: "24"
+# Or
+auto-compaction-retention: "24h"
```

#### Modifié `etcdserver.EtcdServer.ServerConfig` en `*etcdserver.EtcdServer.ServerConfig` {#changed-etcdserveretcdserverserverconfig-to-etcdserveretcdserverserverconfig}

`etcdserver.EtcdServer` a modifié le type de son champ membre `*etcdserver.ServerConfig` en `etcdserver.ServerConfig`. Et `etcdserver.NewServer` prend désormais `etcdserver.ServerConfig`, plutôt que `*etcdserver.ServerConfig`.

Avant et après (par exemple [k8s.io/kubernetes/test/e2e_node/services/etcd.go](https://github.com/kubernetes/kubernetes/blob/release-1.8/test/e2e_node/services/etcd.go#L50-L55))

```diff
import "github.com/coreos/etcd/etcdserver"

type EtcdServer struct {
	*etcdserver.EtcdServer
-	config *etcdserver.ServerConfig
+	config etcdserver.ServerConfig
}

func NewEtcd(dataDir string) *EtcdServer {
-	config := &etcdserver.ServerConfig{
+	config := etcdserver.ServerConfig{
		DataDir: dataDir,
        ...
	}
	return &EtcdServer{config: config}
}

func (e *EtcdServer) Start() error {
	var err error
	e.EtcdServer, err = etcdserver.NewServer(e.config)
    ...
```

#### Ajout de la structure `embed.Config.LogOutput` {#added-embedconfiglogoutput-struct}

> [!WARNING]
> Notez que ce champ a été renommé en `embed.Config.LogOutputs` dans le type `[]string` à partir de la version 3.4. Consultez le [guide de mise à jour vers la version 3.4](/fr/etcd/upgrades/upgrade_3_4/) pour plus de détails.

Champ `LogOutput` est ajouté à `embed.Config` :

```diff
package embed

type Config struct {
 	Debug bool `json:"debug"`
 	LogPkgLevels string `json:"log-package-levels"`
+	LogOutput string `json:"log-output"`
 	...
```

Avant que les avertissements du serveur gRPC ne soient journalisés dans etcdserver.

```
WARNING: 2017/11/02 11:35:51 grpc: addrConn.resetTransport failed to create client transport: connection error: desc = "transport: Error while dialing dial tcp: operation was canceled"; Reconnecting to {localhost:2379 <nil>}
WARNING: 2017/11/02 11:35:51 grpc: addrConn.resetTransport failed to create client transport: connection error: desc = "transport: Error while dialing dial tcp: operation was canceled"; Reconnecting to {localhost:2379 <nil>}
```

À compter de la version 3.3, les journaux du serveur gRPC sont désactivés par défaut.

> [!WARNING]
> Notez que la méthode `embed.Config.SetupLogging` a été dépréciée à partir de la version v3.4. Consultez le [guide de mise à jour vers la version v3.4](/fr/etcd/upgrades/upgrade_3_4/) pour plus de détails.

```go
import "github.com/coreos/etcd/embed"

cfg := &embed.Config{Debug: false}
cfg.SetupLogging()
```

Définissez le champ `embed.Config.Debug` sur `true` pour activer les journaux du serveur gRPC.

#### Modifié la réponse de l'endpoint `/health` {#changed-health-endpoint-response}

Précédemment, `[endpoint]:[client-port]/health` renvoyait une valeur JSON marshalisée manuellement. La version 3.3 définit désormais la structure [`etcdhttp.Health`](https://pkg.go.dev/github.com/etcd-io/etcd/etcdserver/api/etcdhttp#Health).

Notez qu’à partir des versions v3.3.0-rc.0, v3.3.0-rc.1 et v3.3.0-rc.2, les champs `etcdhttp.Health` ont un type booléen avec des champs `"health"` et `"errors"`. Afin de garantir la compatibilité descendante, nous avons reverti le champ `"health"` vers le type `string` et supprimé le champ `"errors"`. Les informations de santé supplémentaires seront fournies via des API séparées.

```bash
$ curl http://localhost:2379/health
{"health":"true"}
```

#### Modifié les points d'entrée HTTP de la passerelle gRPC (remplacé `/v3alpha` par `/v3beta`) {#changed-grpc-gateway-http-endpoints-replaced-v3alpha-with-v3beta}

Avant

```bash
curl -L http://localhost:2379/v3alpha/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

Après

```bash
curl -L http://localhost:2379/v3beta/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

Les requêtes vers les points de terminaison `/v3alpha` seront redirigées vers `/v3beta`, et `/v3alpha` sera supprimé dans la version 3.4.

#### Modifié les limites de taille maximale des requêtes {#changed-maximum-request-size-limits}

3.3 permet désormais des limites de taille de requête personnalisées pour le serveur et le **côté client**. Dans les versions précédentes (v3.2.10, v3.2.11), la taille de réponse du client était limitée à 4 MiB.

Les limites de requêtes côté serveur peuvent être configurées à l'aide du drapeau `--max-request-bytes` :

```bash
# limits request size to 1.5 KiB
etcd --max-request-bytes 1536

# client writes exceeding 1.5 KiB will be rejected
etcdctl put foo [LARGE VALUE...]
# etcdserver: request is too large
```

Ou configurez le champ `embed.Config.MaxRequestBytes` :

```go
import "github.com/coreos/etcd/embed"
import "github.com/coreos/etcd/etcdserver/api/v3rpc/rpctypes"

// limit requests to 5 MiB
cfg := embed.NewConfig()
cfg.MaxRequestBytes = 5 * 1024 * 1024

// client writes exceeding 5 MiB will be rejected
_, err := cli.Put(ctx, "foo", [LARGE VALUE...])
err == rpctypes.ErrRequestTooLarge
```

Si non spécifié, la limite côté serveur est par défaut de 1,5 MiB.

Les limites de requêtes côté client doivent être configurées en fonction des limites côté serveur.

```bash
# limits request size to 1 MiB
etcd --max-request-bytes 1048576
```

```go
import "github.com/coreos/etcd/clientv3"

cli, _ := clientv3.New(clientv3.Config{
    Endpoints: []string{"127.0.0.1:2379"},
    MaxCallSendMsgSize: 2 * 1024 * 1024,
    MaxCallRecvMsgSize: 3 * 1024 * 1024,
})


// client writes exceeding "--max-request-bytes" will be rejected from etcd server
_, err := cli.Put(ctx, "foo", strings.Repeat("a", 1*1024*1024+5))
err == rpctypes.ErrRequestTooLarge


// client writes exceeding "MaxCallSendMsgSize" will be rejected from client-side
_, err = cli.Put(ctx, "foo", strings.Repeat("a", 5*1024*1024))
err.Error() == "rpc error: code = ResourceExhausted desc = grpc: trying to send message larger than max (5242890 vs. 2097152)"


// some writes under limits
for i := range []int{0,1,2,3,4} {
    _, err = cli.Put(ctx, fmt.Sprintf("foo%d", i), strings.Repeat("a", 1*1024*1024-500))
    if err != nil {
        panic(err)
    }
}
// client reads exceeding "MaxCallRecvMsgSize" will be rejected from client-side
_, err = cli.Get(ctx, "foo", clientv3.WithPrefix())
err.Error() == "rpc error: code = ResourceExhausted desc = grpc: received message larger than max (5240509 vs. 3145728)"
```

Si non spécifié, la limite d’envoi côté client est par défaut fixée à 2 MiB (1,5 MiB + surcharge gRPC) et la limite de réception à `math.MaxInt32`. Voir [clientv3 godoc](https://pkg.go.dev/github.com/etcd-io/etcd/clientv3#Config) pour plus de détails.

#### Modifiées les signatures des fonctions d’enveloppe du client gRPC brut {#changed-raw-grpc-client-wrapper-function-signatures}

3.3 modifie les signatures de fonction du wrapper client gRPC `clientv3`. Ce changement était nécessaire pour prendre en charge les [options personnalisées `grpc.CallOption`sur les limites de taille de message](https://github.com/etcd-io/etcd/pull/9047).

Avant et après

```diff
-func NewKVFromKVClient(remote pb.KVClient) KV {
+func NewKVFromKVClient(remote pb.KVClient, c *Client) KV {

-func NewClusterFromClusterClient(remote pb.ClusterClient) Cluster {
+func NewClusterFromClusterClient(remote pb.ClusterClient, c *Client) Cluster {

-func NewLeaseFromLeaseClient(remote pb.LeaseClient, keepAliveTimeout time.Duration) Lease {
+func NewLeaseFromLeaseClient(remote pb.LeaseClient, c *Client, keepAliveTimeout time.Duration) Lease {

-func NewMaintenanceFromMaintenanceClient(remote pb.MaintenanceClient) Maintenance {
+func NewMaintenanceFromMaintenanceClient(remote pb.MaintenanceClient, c *Client) Maintenance {

-func NewWatchFromWatchClient(wc pb.WatchClient) Watcher {
+func NewWatchFromWatchClient(wc pb.WatchClient, c *Client) Watcher {
```

#### Changé le type d'erreur de l'API clientv3 `Snapshot` {#changed-clientv3-snapshot-api-error-type}

Précédemment, l'API clientv3 `Snapshot` renvoyait des erreurs de type [`grpc/*status.statusError`] brutes. La version 3.3 les traduit désormais en types d'erreurs publiques correspondants, afin de maintenir une cohérence avec les autres API.

Avant

```go
import "context"

// reading snapshot with canceled context should error out
ctx, cancel := context.WithCancel(context.Background())
rc, _ := cli.Snapshot(ctx)
cancel()
_, err := io.Copy(f, rc)
err.Error() == "rpc error: code = Canceled desc = context canceled"

// reading snapshot with deadline exceeded should error out
ctx, cancel = context.WithTimeout(context.Background(), time.Second)
defer cancel()
rc, _ = cli.Snapshot(ctx)
time.Sleep(2 * time.Second)
_, err = io.Copy(f, rc)
err.Error() == "rpc error: code = DeadlineExceeded desc = context deadline exceeded"
```

Après

```go
import "context"

// reading snapshot with canceled context should error out
ctx, cancel := context.WithCancel(context.Background())
rc, _ := cli.Snapshot(ctx)
cancel()
_, err := io.Copy(f, rc)
err == context.Canceled

// reading snapshot with deadline exceeded should error out
ctx, cancel = context.WithTimeout(context.Background(), time.Second)
defer cancel()
rc, _ = cli.Snapshot(ctx)
time.Sleep(2 * time.Second)
_, err = io.Copy(f, rc)
err == context.DeadlineExceeded
```

#### Changé la sortie de la commande `etcdctl lease timetolive` {#changed-etcdctl-lease-timetolive-command-output}

Précédemment, la commande `lease timetolive LEASE_ID` sur un bail expiré affichait `-1s` pour le nombre de secondes restantes. La version 3.3 affiche désormais des messages plus clairs.

Avant


```bash
lease 2d8257079fa1bc0c granted with TTL(0s), remaining(-1s)
```

Après

```bash
lease 2d8257079fa1bc0c already expired
```

#### Modifié les imports `golang.org/x/net/context` {#changed-golangorgxnetcontext-imports}

`clientv3` a déprécié `golang.org/x/net/context`. Si un projet intègre `golang.org/x/net/context` dans d'autres codes (par exemple, du code généré par etcd pour les protocoles buffer) et importe `github.com/coreos/etcd/clientv3`, une version de Go 1.9 ou ultérieure est requise pour la compilation.

Avant

```go
import "golang.org/x/net/context"
cli.Put(context.Background(), "f", "v")
```

Après

```go
import "context"
cli.Put(context.Background(), "f", "v")
```

#### Modifié la dépendance gRPC {#changed-grpc-dependency}

3.3 exige désormais [grpc/grpc-go](https://github.com/grpc/grpc-go/releases) `v1.7.5`.

##### Obsolète `grpclog.Logger` {#deprecated-grpcloglogger}

`grpclog.Logger` a été obsolète en faveur de [ `grpclog.LoggerV2` ](https://github.com/grpc/grpc-go/blob/master/grpclog/loggerv2.go). `clientv3.Logger` est désormais `grpclog.LoggerV2`.

Avant

```go
import "github.com/coreos/etcd/clientv3"
clientv3.SetLogger(log.New(os.Stderr, "grpc: ", 0))
```

Après

```go
import "github.com/coreos/etcd/clientv3"
import "google.golang.org/grpc/grpclog"
clientv3.SetLogger(grpclog.NewLoggerV2(os.Stderr, os.Stderr, os.Stderr))

// log.New above cannot be used (not implement grpclog.LoggerV2 interface)
```

##### Obsolète `grpc.ErrClientConnTimeout` {#deprecated-grpcerrclientconntimeout}

Précédemment, l'erreur `grpc.ErrClientConnTimeout` était renvoyée en cas de délai d'attente lors de la connexion client. La version 3.3 renvoie désormais `context.DeadlineExceeded` (voir [#8504](https://github.com/etcd-io/etcd/issues/8504)).

Avant

```go
// expect dial time-out on ipv4 blackhole
_, err := clientv3.New(clientv3.Config{
    Endpoints:   []string{"http://254.0.0.1:12345"},
    DialTimeout: 2 * time.Second
})
if err == grpc.ErrClientConnTimeout {
	// handle errors
}
```

Après

```go
_, err := clientv3.New(clientv3.Config{
    Endpoints:   []string{"http://254.0.0.1:12345"},
    DialTimeout: 2 * time.Second
})
if err == context.DeadlineExceeded {
	// handle errors
}
```

#### Changement du registre conteneur officiel {#changed-official-container-registry}

etcd utilise désormais [`gcr.io/etcd-development/etcd`](https://gcr.io/etcd-development/etcd) comme registre conteneur principal, et [`quay.io/coreos/etcd`](https://quay.io/coreos/etcd) comme secondaire.

Avant

```bash
docker pull quay.io/coreos/etcd:v3.2.5
```

Après

```bash
docker pull gcr.io/etcd-development/etcd:v3.3.0
```

### Mises à jour à partir de la version v3.3.14 {#upgrades-to--v3314}

[v3.3.14](https://github.com/etcd-io/etcd/releases/tag/v3.3.14) a dû intégrer certaines fonctionnalités de la version 3.4, tout en cherchant à minimiser les différences entre les implémentations du chargeur de client. Cette version corrige ["kube-apiserver 1.13.x refuse de fonctionner lorsque le premier serveur etcd n'est pas disponible" (kubernetes#72102)](https://github.com/kubernetes/kubernetes/issues/72102).

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

[Le nouveau chargeur de client](/fr/etcd/learning/design-client/) utilise un résolveur asynchrone pour transmettre les points de terminaison à la fonction de connexion gRPC. En conséquence, [v3.3.14](https://github.com/etcd-io/etcd/releases/tag/v3.3.14) ou une version ultérieure nécessite l'option `grpc.WithBlock` pour attendre que la connexion sous-jacente soit active.

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

Veuillez consulter [CHANGELOG](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.3.md) pour obtenir la liste complète des modifications.

### Liste de vérification pour la mise à jour du serveur {#server-upgrade-checklists}

#### Exigences de mise à jour {#upgrade-requirements}

Pour mettre à jour un déploiement etcd existant vers la version 3.3, le cluster en cours d'exécution doit être la version 3.2 ou ultérieure. Si la version est antérieure à 3.2, veuillez [mettre à jour vers la version 3.2](/fr/etcd/upgrades/upgrade_3_2/) avant de procéder à la mise à jour vers la version 3.3.

En outre, pour garantir une mise à niveau progressive sans incident, le cluster en cours d'exécution doit être sain. Vérifiez l'état de santé du cluster à l'aide de la commande `etcdctl endpoint health` avant de poursuivre.

#### Préparation {#preparation}

Avant de mettre à jour etcd, testez toujours les services dépendants d’etcd dans un environnement de préproduction avant de déployer la mise à jour dans l’environnement de production.

Avant de commencer, [sauvegardez les données etcd](/fr/etcd/op-guide/maintenance/#snapshot-backup). Si une erreur survient lors de la mise à jour, il sera possible d'utiliser cette sauvegarde pour [rétrograder](#downgrade) vers la version existante de etcd. Veuillez noter que la `snapshot`commande ne sauvegarde que les données v3. Pour les données v2, consultez [sauvegarde du magasin de données v2](https://etcd.io/docs/v2.3/admin_guide/#backing-up-the-datastore).

#### Versions mixtes {#mixed-versions}

Lors d'une mise à jour, un cluster etcd prend en charge des versions mixtes de membres et fonctionne selon le protocole de la version commune la plus basse. Le cluster est considéré comme mis à jour uniquement lorsque tous ses membres ont été mis à jour vers la version 3.3. Internement, les membres etcd négocient entre eux afin de déterminer la version globale du cluster, qui contrôle la version signalée et les fonctionnalités prises en charge.

#### Limitations {#limitations}

Note : Si le cluster ne contient que des données v3 et aucune donnée v2, il n'est pas soumis à cette limitation.

Si le cluster sert un jeu de données v2 dont la taille dépasse 50 Mo, chaque membre nouvellement mis à jour peut prendre jusqu’à deux minutes pour rattraper le cluster existant. Vérifiez la taille d’un instantané récent afin d’estimer la taille totale des données. Autrement dit, il est préférable d’attendre deux minutes entre chaque mise à jour de membre.

Pour une taille totale de données bien plus importante, de 100 Mo ou plus, ce processus unique peut prendre encore plus de temps. Les administrateurs de clusters etcd très volumineux de cette ampleur peuvent librement contacter l'équipe [etcd][etcd-contact] avant la mise à jour, et nous serons heureux de leur fournir des conseils sur la procédure.

#### Rétrogradation {#downgrade}

Si tous les membres ont été mis à jour vers la version v3.3, le cluster sera mis à jour vers la v3.3, et un retour en arrière depuis cet état finalisé est **impossible**. Si toutefois un seul membre reste en version v3.2, le cluster et ses opérations restent "v3.2", et il est possible, depuis cet état de cluster mixte, de revenir à l'utilisation d'une binaire etcd v3.2 sur tous les membres.

Veuillez [sauvegarder le répertoire de données](/fr/etcd/op-guide/maintenance/#snapshot-backup) de tous les membres etcd afin de permettre la désinstallation du cluster, même après son mise à jour complète.

### Procédure de mise à jour {#upgrade-procedure}

Cet exemple montre comment mettre à jour un cluster etcd v3.2 composé de 3 membres, en cours d'exécution sur une machine locale.

#### 1. Vérifier les prérequis de mise à jour {#1-check-upgrade-requirements}

Le cluster est-il sain et en cours d'exécution sous la version 3.2.x ?

```
$ ETCDCTL_API=3 etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 6.600684ms
localhost:22379 is healthy: successfully committed proposal: took = 8.540064ms
localhost:32379 is healthy: successfully committed proposal: took = 8.763432ms

$ curl http://localhost:2379/version
{"etcdserver":"3.2.7","etcdcluster":"3.2.0"}
```

#### 2. Arrêtez le processus etcd existant {#2-stop-the-existing-etcd-process}

Lorsque chaque processus etcd est arrêté, les autres membres du cluster enregistrent des erreurs attendues. Cela est normal, car la connexion avec un membre du cluster a été (temporairement) interrompue :

```
14:13:31.491746 I | raft: c89feb932daef420 [term 3] received MsgTimeoutNow from 6d4f535bae3ab960 and starts an election to get leadership.
14:13:31.491769 I | raft: c89feb932daef420 became candidate at term 4
14:13:31.491788 I | raft: c89feb932daef420 received MsgVoteResp from c89feb932daef420 at term 4
14:13:31.491797 I | raft: c89feb932daef420 [logterm: 3, index: 9] sent MsgVote request to 6d4f535bae3ab960 at term 4
14:13:31.491805 I | raft: c89feb932daef420 [logterm: 3, index: 9] sent MsgVote request to 9eda174c7df8a033 at term 4
14:13:31.491815 I | raft: raft.node: c89feb932daef420 lost leader 6d4f535bae3ab960 at term 4
14:13:31.524084 I | raft: c89feb932daef420 received MsgVoteResp from 6d4f535bae3ab960 at term 4
14:13:31.524108 I | raft: c89feb932daef420 [quorum:2] has received 2 MsgVoteResp votes and 0 vote rejections
14:13:31.524123 I | raft: c89feb932daef420 became leader at term 4
14:13:31.524136 I | raft: raft.node: c89feb932daef420 elected leader c89feb932daef420 at term 4
14:13:31.592650 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream MsgApp v2 reader)
14:13:31.592825 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream Message reader)
14:13:31.693275 E | rafthttp: failed to dial 6d4f535bae3ab960 on stream Message (dial tcp [::1]:2380: getsockopt: connection refused)
14:13:31.693289 I | rafthttp: peer 6d4f535bae3ab960 became inactive
14:13:31.936678 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream Message writer)
```

Il est recommandé de procéder à un [sauvegarde des données etcd](/fr/etcd/op-guide/maintenance/#snapshot-backup) à cette étape afin de disposer d’un chemin de retour en cas de problème :

```
$ etcdctl snapshot save backup.db
```

#### 3. Lancement d'un binaire etcd v3.3 en mode drop-in et démarrage du nouveau processus etcd {#3-drop-in-etcd-v33-binary-and-start-the-new-etcd-process}

Le nouvel etcd v3.3 publiera ses informations dans le cluster :

```
14:14:25.363225 I | etcdserver: published {Name:s1 ClientURLs:[http://localhost:2379]} to cluster a9ededbffcb1b1f1
```

Vérifiez que chaque membre, puis l’ensemble du cluster, devient sain avec la nouvelle binaire etcd v3.3 :

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:22379 is healthy: successfully committed proposal: took = 5.540129ms
localhost:32379 is healthy: successfully committed proposal: took = 7.321771ms
localhost:2379 is healthy: successfully committed proposal: took = 10.629901ms
```

Les membres mis à jour émettront des avertissements similaires au suivant jusqu'à ce que l'intégralité du cluster soit mis à jour. C'est normal et cessera une fois que tous les membres du cluster etcd auront été mis à jour vers la version 3.3 :

```
14:15:17.071804 W | etcdserver: member c89feb932daef420 has a higher version 3.3.0
14:15:21.073110 W | etcdserver: the local etcd version 3.2.7 is not up-to-date
14:15:21.073142 W | etcdserver: member 6d4f535bae3ab960 has a higher version 3.3.0
14:15:21.073157 W | etcdserver: the local etcd version 3.2.7 is not up-to-date
14:15:21.073164 W | etcdserver: member c89feb932daef420 has a higher version 3.3.0
```

#### 4. Répétez l'étape 2 à l'étape 3 pour tous les autres membres {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. Terminer {#5-finish}

Lorsque tous les membres sont mis à jour, le cluster signalera avec succès la mise à jour vers la version 3.3 :

```
14:15:54.536901 N | etcdserver/membership: updated the cluster version from 3.2 to 3.3
14:15:54.537035 I | etcdserver/api: enabled capabilities for version 3.3
```

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 2.312897ms
localhost:22379 is healthy: successfully committed proposal: took = 2.553476ms
localhost:32379 is healthy: successfully committed proposal: took = 2.517902ms
```

[etcd-contact]: https://groups.google.com/g/etcd-dev
