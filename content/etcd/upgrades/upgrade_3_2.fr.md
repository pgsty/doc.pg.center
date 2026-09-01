---
title: Mettre à jour etcd de 3.1 vers 3.2
weight: 6800
description: "Processus, listes de vérification et notes sur la mise à jour d’etcd de la version 3.1 à la 3.2"
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/upgrades/upgrade_3_2.md"
---

Dans le cas général, la mise à niveau de etcd 3.1 vers 3.2 peut être effectuée sans interruption de service, par mise à niveau progressive :
 - un par un, arrêtez les processus etcd v3.1 et remplacez-les par des processus etcd v3.2
 - après avoir lancé tous les processus v3.2, les nouvelles fonctionnalités de la version v3.2 sont disponibles pour le cluster

Avant de [lancer la mise à jour](#upgrade-procedure), lisez le reste du présent guide afin de vous préparer.

### Listes de vérification pour la mise à jour {#upgrade-checklists}

> [!WARNING]
> Lorsque [on migre depuis la version v2 sans données v3](https://github.com/etcd-io/etcd/issues/9480), le serveur etcd v3.2+ provoque une panne lorsqu'il restaure à partir d'un instantané existant mais qu'aucun fichier v3 `ETCD_DATA_DIR/member/snap/db` n'est présent. Cela se produit lorsque le serveur a été migré depuis la version v2 sans données v3 précédentes. Cela empêche également la perte accidentelle de données v3 (par exemple, le fichier `db` pourrait avoir été déplacé). etcd exige que la migration post-v3 ne puisse avoir lieu qu'avec des données v3 présentes. N'effectuez pas la mise à jour vers des versions v3 plus récentes tant que le serveur v3.0 ne contient pas de données v3.

Changements importants marquants dans 3.2.

#### Changé la valeur par défaut de `snapshot-count` {#changed-default-snapshot-count-value}

Une valeur plus élevée de `--snapshot-count` conserve davantage d'entrées Raft en mémoire jusqu'à l'instantané, entraînant ainsi une utilisation mémoire plus élevée et récurrente de [ ](https://github.com/kubernetes/kubernetes/issues/60589#issuecomment-371977156). Comme le leader conserve les dernières entrées Raft plus longtemps, un suiveur lent dispose de plus de temps pour se synchroniser avant que le leader ne prenne un instantané. `--snapshot-count` représente un compromis entre une utilisation mémoire plus élevée et une meilleure disponibilité des suiveurs lents.

Depuis la version 3.2, la valeur par défaut de `--snapshot-count` a [passé de 10 000 à 100 000](https://github.com/etcd-io/etcd/pull/7160).

#### Changement de dépendance gRPC (>=3.2.10) {#changed-grpc-dependency-3210}

3.2.10 ou ultérieure exige désormais [grpc/grpc-go](https://github.com/grpc/grpc-go/releases) `v1.7.5` (les versions antérieures à 3.2.9 exigent `v1.2.1`).

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

Précédemment, l'erreur `grpc.ErrClientConnTimeout` était renvoyée en cas de délai d'attente lors de la connexion client. La version 3.2 renvoie désormais `context.DeadlineExceeded` (voir [#8504](https://github.com/etcd-io/etcd/issues/8504)).

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

#### Modifié les limites de taille de requête maximale (>=3.2.10) {#changed-maximum-request-size-limits-3210}

3.2.10 et 3.2.11 permettent de définir des limites personnalisées de taille de requête côté serveur. À partir de la version 3.2.12, il est possible de définir des limites personnalisées de taille de requête côté serveur et côté **client**. Dans les versions antérieures (v3.2.10, v3.2.11), la taille des réponses côté client était limitée à 4 MiB.

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

#### Modifié les enveloppes client gRPC brutes {#changed-raw-grpc-client-wrappers}

3.2.12 ou versions ultérieures modifient les signatures de fonction du wrapper client gRPC `clientv3`. Ce changement était nécessaire pour prendre en charge les [options `grpc.CallOption`sur les limites de taille des messages](https://github.com/etcd-io/etcd/pull/9047).

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

#### Modifié l'API `clientv3.Lease.TimeToLive` {#changed-clientv3leasetimetolive-api}

Précédemment, l'API `clientv3.Lease.TimeToLive` renvoyait `lease.ErrLeaseNotFound` en cas d'ID de bail inexistant. La version 3.2 renvoie désormais TTL=-1 dans sa réponse, sans erreur (voir [#7305](https://github.com/etcd-io/etcd/pull/7305)).

Avant

```go
// when leaseID does not exist
resp, err := TimeToLive(ctx, leaseID)
resp == nil
err == lease.ErrLeaseNotFound
```

Après

```go
// when leaseID does not exist
resp, err := TimeToLive(ctx, leaseID)
resp.TTL == -1
err == nil
```

#### Déplacé `clientv3.NewFromConfigFile` vers `clientv3.yaml.NewConfig` {#moved-clientv3newfromconfigfile-to-clientv3yamlnewconfig}

`clientv3.NewFromConfigFile` est déplacé vers `yaml.NewConfig`.

Avant

```go
import "github.com/coreos/etcd/clientv3"
clientv3.NewFromConfigFile
```

Après

```go
import clientv3yaml "github.com/coreos/etcd/clientv3/yaml"
clientv3yaml.NewConfig
```

#### Changement apporté à `--listen-peer-urls` et `--listen-client-urls` {#change-in---listen-peer-urls-and---listen-client-urls}

3.2 refuse désormais les noms de domaine pour `--listen-peer-urls` et `--listen-client-urls` (3.1 n’affichait que des avertissements), car un nom de domaine n’est pas valide pour le lien d’interface réseau. Assurez-vous que ces URL sont correctement formatées en tant que `scheme://IP:port`.

Consultez [issue #6336](https://github.com/etcd-io/etcd/issues/6336) pour plus de contextes.

### Liste de vérification pour la mise à jour du serveur {#server-upgrade-checklists}

#### Exigences de mise à jour {#upgrade-requirements}

Pour mettre à jour un déploiement etcd existant vers la version 3.2, le cluster en cours d'exécution doit être la version 3.1 ou ultérieure. Si la version est antérieure à 3.1, veuillez [mettre à jour vers la version 3.1](/fr/etcd/upgrades/upgrade_3_1) avant de procéder à la mise à jour vers la version 3.2.

En outre, pour garantir une mise à niveau progressive sans incident, le cluster en cours d'exécution doit être sain. Vérifiez l'état de santé du cluster à l'aide de la commande `etcdctl endpoint health` avant de poursuivre.

#### Préparation {#preparation}

Avant de mettre à jour etcd, testez toujours les services dépendants d’etcd dans un environnement de préproduction avant de déployer la mise à jour dans l’environnement de production.

Avant de commencer, [sauvegardez les données etcd](/fr/etcd/op-guide/maintenance#snapshot-backup). Si une erreur survient durant la mise à jour, il sera possible d'utiliser cette sauvegarde pour [rétrograder](#downgrade) vers la version existante de etcd. Veuillez noter que la `snapshot`commande ne sauvegarde que les données v3. Pour les données v2, consultez [sauvegarde du magasin de données v2](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore).

#### Versions mixtes {#mixed-versions}

Lors d'une mise à jour, un cluster etcd prend en charge des versions mixtes de membres et fonctionne selon le protocole de la version commune la plus basse. Le cluster n'est considéré comme mis à jour qu'une fois que tous ses membres ont été mis à jour vers la version 3.2. Internement, les membres etcd négocient entre eux afin de déterminer la version globale du cluster, qui détermine la version signalée et les fonctionnalités prises en charge.

#### Limitations {#limitations}

Note : Si le cluster ne contient que des données v3 et aucune donnée v2, il n'est pas soumis à cette limitation.

Si le cluster sert un jeu de données v2 dont la taille dépasse 50 Mo, chaque membre nouvellement mis à jour peut prendre jusqu’à deux minutes pour rattraper le cluster existant. Vérifiez la taille d’un instantané récent afin d’estimer la taille totale des données. Autrement dit, il est préférable d’attendre deux minutes entre chaque mise à jour de membre.

Pour une taille totale de données bien plus importante, de 100 Mo ou plus, ce processus unique peut prendre encore plus de temps. Les administrateurs de clusters etcd très volumineux de cette ampleur peuvent librement contacter l'équipe [etcd][etcd-contact] avant la mise à jour, et nous serons heureux de leur fournir des conseils sur la procédure.

#### Rétrogradation {#downgrade}

Si tous les membres ont été mis à jour vers la version v3.2, le cluster sera mis à jour vers la version v3.2, et le retour en arrière depuis cet état finalisé est **impossible**. Si toutefois un seul membre reste en version v3.1, le cluster et ses opérations restent "v3.1", et il est possible, depuis cet état de cluster mixte, de revenir à l'utilisation d'une binaire etcd v3.1 sur tous les membres.

Veuillez [sauvegarder le répertoire de données](/fr/etcd/op-guide/maintenance#snapshot-backup) de tous les membres etcd afin de permettre la désinstallation du cluster, même après son mise à jour complète.

### Procédure de mise à jour {#upgrade-procedure}

Cet exemple montre comment mettre à jour un cluster etcd v3.1 composé de 3 membres, en cours d'exécution sur une machine locale.

#### 1. Vérifier les prérequis de mise à jour {#1-check-upgrade-requirements}

Le cluster est-il sain et en cours d'exécution sous la version 3.1.x ?

```
$ ETCDCTL_API=3 etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 6.600684ms
localhost:22379 is healthy: successfully committed proposal: took = 8.540064ms
localhost:32379 is healthy: successfully committed proposal: took = 8.763432ms

$ curl http://localhost:2379/version
{"etcdserver":"3.1.7","etcdcluster":"3.1.0"}
```

#### 2. Arrêtez le processus etcd existant {#2-stop-the-existing-etcd-process}

Lorsque chaque processus etcd est arrêté, les autres membres du cluster enregistrent des erreurs attendues. Cela est normal, car la connexion avec un membre du cluster a été (temporairement) interrompue :

```
2017-04-27 14:13:31.491746 I | raft: c89feb932daef420 [term 3] received MsgTimeoutNow from 6d4f535bae3ab960 and starts an election to get leadership.
2017-04-27 14:13:31.491769 I | raft: c89feb932daef420 became candidate at term 4
2017-04-27 14:13:31.491788 I | raft: c89feb932daef420 received MsgVoteResp from c89feb932daef420 at term 4
2017-04-27 14:13:31.491797 I | raft: c89feb932daef420 [logterm: 3, index: 9] sent MsgVote request to 6d4f535bae3ab960 at term 4
2017-04-27 14:13:31.491805 I | raft: c89feb932daef420 [logterm: 3, index: 9] sent MsgVote request to 9eda174c7df8a033 at term 4
2017-04-27 14:13:31.491815 I | raft: raft.node: c89feb932daef420 lost leader 6d4f535bae3ab960 at term 4
2017-04-27 14:13:31.524084 I | raft: c89feb932daef420 received MsgVoteResp from 6d4f535bae3ab960 at term 4
2017-04-27 14:13:31.524108 I | raft: c89feb932daef420 [quorum:2] has received 2 MsgVoteResp votes and 0 vote rejections
2017-04-27 14:13:31.524123 I | raft: c89feb932daef420 became leader at term 4
2017-04-27 14:13:31.524136 I | raft: raft.node: c89feb932daef420 elected leader c89feb932daef420 at term 4
2017-04-27 14:13:31.592650 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream MsgApp v2 reader)
2017-04-27 14:13:31.592825 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream Message reader)
2017-04-27 14:13:31.693275 E | rafthttp: failed to dial 6d4f535bae3ab960 on stream Message (dial tcp [::1]:2380: getsockopt: connection refused)
2017-04-27 14:13:31.693289 I | rafthttp: peer 6d4f535bae3ab960 became inactive
2017-04-27 14:13:31.936678 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream Message writer)
```

Il est recommandé de procéder à un [sauvegarde des données etcd](/fr/etcd/op-guide/maintenance#snapshot-backup) à cette étape afin de disposer d’un chemin de retour en cas de problème :

```
$ etcdctl snapshot save backup.db
```

#### 3. Lancer le binaire etcd v3.2 en mode drop-in et démarrer le nouveau processus etcd {#3-drop-in-etcd-v32-binary-and-start-the-new-etcd-process}

Le nouvel etcd v3.2 publiera ses informations dans le cluster :

```
2017-04-27 14:14:25.363225 I | etcdserver: published {Name:s1 ClientURLs:[http://localhost:2379]} to cluster a9ededbffcb1b1f1
```

Vérifiez que chaque membre, puis l’ensemble du cluster, devient sain avec la nouvelle binaire etcd v3.2 :

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:22379 is healthy: successfully committed proposal: took = 5.540129ms
localhost:32379 is healthy: successfully committed proposal: took = 7.321771ms
localhost:2379 is healthy: successfully committed proposal: took = 10.629901ms
```

Les membres mis à jour émettront des avertissements similaires au suivant jusqu'à ce que l'intégralité du cluster soit mis à jour. C'est normal et cessera une fois que tous les membres du cluster etcd auront été mis à jour vers la version 3.2 :

```
2017-04-27 14:15:17.071804 W | etcdserver: member c89feb932daef420 has a higher version 3.2.0
2017-04-27 14:15:21.073110 W | etcdserver: the local etcd version 3.1.7 is not up-to-date
2017-04-27 14:15:21.073142 W | etcdserver: member 6d4f535bae3ab960 has a higher version 3.2.0
2017-04-27 14:15:21.073157 W | etcdserver: the local etcd version 3.1.7 is not up-to-date
2017-04-27 14:15:21.073164 W | etcdserver: member c89feb932daef420 has a higher version 3.2.0
```

#### 4. Répétez l'étape 2 à l'étape 3 pour tous les autres membres {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. Terminer {#5-finish}

Lorsque tous les membres sont mis à jour, le cluster signalera avec succès la mise à jour vers la version 3.2 :

```
2017-04-27 14:15:54.536901 N | etcdserver/membership: updated the cluster version from 3.1 to 3.2
2017-04-27 14:15:54.537035 I | etcdserver/api: enabled capabilities for version 3.2
```

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 2.312897ms
localhost:22379 is healthy: successfully committed proposal: took = 2.553476ms
localhost:32379 is healthy: successfully committed proposal: took = 2.517902ms
```

[etcd-contact]: https://groups.google.com/g/etcd-dev
