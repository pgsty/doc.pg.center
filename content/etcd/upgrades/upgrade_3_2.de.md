---
title: Upgrade von etcd 3.1 auf 3.2
weight: 6800
description: Verfahren, Checklisten und Hinweise zum Upgrade von etcd 3.1 auf 3.2
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_2.md"
---

Im Allgemeinen kann das Upgrade von etcd 3.1 auf 3.2 als Rolling Upgrade ohne Ausfallzeit erfolgen:
 - Die etcd-v3.1-Prozesse nacheinander stoppen und durch etcd-v3.2-Prozesse ersetzen.
 - Sobald alle v3.2-Prozesse laufen, stehen dem Cluster die neuen Funktionen von v3.2 zur Verfügung.

Lesen Sie zur Vorbereitung den Rest dieses Leitfadens, bevor Sie [mit dem Upgrade beginnen](#upgrade-procedure).

### Checklisten für das Upgrade {#upgrade-checklists}

> [!WARNING]
> Bei der [Migration von v2 ohne v3-Daten](https://github.com/etcd-io/etcd/issues/9480) löst der etcd-Server v3.2+ eine Panic aus, wenn etcd aus vorhandenen Snapshots wiederhergestellt wird, aber keine v3-Datei `ETCD_DATA_DIR/member/snap/db` vorhanden ist. Dies tritt auf, wenn der Server von v2 migriert wurde, ohne zuvor v3-Daten zu enthalten. Dadurch wird auch ein versehentlicher Verlust von v3-Daten verhindert (z. B. könnte die Datei `db` verschoben worden sein). etcd verlangt, dass weitere Migrationen nach der Migration auf v3 nur mit v3-Daten erfolgen können. Führen Sie kein Upgrade auf neuere v3-Versionen durch, bevor der v3.0-Server v3-Daten enthält.

Wichtige inkompatible Änderungen in 3.2.

#### Geänderter Standardwert für `snapshot-count` {#changed-default-snapshot-count-value}

Ein höherer Wert für `--snapshot-count` hält bis zum Snapshot mehr Raft-Einträge im Speicher und führt dadurch zu [wiederholt höherer Speichernutzung](https://github.com/kubernetes/kubernetes/issues/60589#issuecomment-371977156). Da der Leader die neuesten Raft-Einträge länger vorhält, hat ein langsamer Follower mehr Zeit, vor dem Snapshot des Leaders aufzuholen. `--snapshot-count` stellt einen Kompromiss zwischen höherer Speichernutzung und besserer Verfügbarkeit langsamer Follower dar.

Seit v3.2 wurde der Standardwert von `--snapshot-count` [von 10,000 auf 100,000 geändert](https://github.com/etcd-io/etcd/pull/7160).

#### Geänderte gRPC-Abhängigkeit (>=3.2.10) {#changed-grpc-dependency-3210}

3.2.10 oder höher benötigt jetzt [grpc/grpc-go](https://github.com/grpc/grpc-go/releases) `v1.7.5` (<=3.2.9 benötigt `v1.2.1`).

##### `grpclog.Logger` ist veraltet {#deprecated-grpcloglogger}

`grpclog.Logger` ist zugunsten von [`grpclog.LoggerV2`](https://github.com/grpc/grpc-go/blob/master/grpclog/loggerv2.go) veraltet. `clientv3.Logger` ist jetzt `grpclog.LoggerV2`.

Vorher

```go
import "github.com/coreos/etcd/clientv3"
clientv3.SetLogger(log.New(os.Stderr, "grpc: ", 0))
```

Nachher

```go
import "github.com/coreos/etcd/clientv3"
import "google.golang.org/grpc/grpclog"
clientv3.SetLogger(grpclog.NewLoggerV2(os.Stderr, os.Stderr, os.Stderr))

// log.New above cannot be used (not implement grpclog.LoggerV2 interface)
```

##### `grpc.ErrClientConnTimeout` ist veraltet {#deprecated-grpcerrclientconntimeout}

Bisher wurde bei Zeitüberschreitungen beim Verbindungsaufbau des Clients der Fehler `grpc.ErrClientConnTimeout` zurückgegeben. 3.2 gibt stattdessen `context.DeadlineExceeded` zurück (siehe [#8504](https://github.com/etcd-io/etcd/issues/8504)).

Vorher

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

Nachher

```go
_, err := clientv3.New(clientv3.Config{
    Endpoints:   []string{"http://254.0.0.1:12345"},
    DialTimeout: 2 * time.Second
})
if err == context.DeadlineExceeded {
	// handle errors
}
```

#### Geänderte Obergrenzen für die Anfragegröße (>=3.2.10) {#changed-maximum-request-size-limits-3210}

3.2.10 und 3.2.11 erlauben benutzerdefinierte Größenlimits für Anfragen auf der Serverseite. >=3.2.12 erlaubt benutzerdefinierte Größenlimits für Anfragen sowohl auf der Server- als auch auf der **Clientseite**. In früheren Versionen (v3.2.10, v3.2.11) war die Größe der Antworten an Clients auf nur 4 MiB begrenzt.

Serverseitige Anfragelimits lassen sich mit dem Flag `--max-request-bytes` konfigurieren:

```bash
# limits request size to 1.5 KiB
etcd --max-request-bytes 1536

# client writes exceeding 1.5 KiB will be rejected
etcdctl put foo [LARGE VALUE...]
# etcdserver: request is too large
```

Oder konfigurieren Sie das Feld `embed.Config.MaxRequestBytes`:

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

**Ohne Angabe beträgt das serverseitige Limit standardmäßig 1.5 MiB**.

Clientseitige Anfragelimits müssen anhand der serverseitigen Limits konfiguriert werden.

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

**Ohne Angabe beträgt das clientseitige Sendelimit standardmäßig 2 MiB (1.5 MiB + zusätzliche gRPC-Bytes) und das Empfangslimit `math.MaxInt32`**. Weitere Einzelheiten finden Sie in der [clientv3-godoc-Dokumentation](https://pkg.go.dev/github.com/etcd-io/etcd/clientv3#Config).

#### Geänderte Wrapper für direkte gRPC-Clients {#changed-raw-grpc-client-wrappers}

3.2.12 oder höher ändert die Funktionssignaturen des gRPC-Client-Wrappers von `clientv3`. Diese Änderung war erforderlich, um [benutzerdefinierte `grpc.CallOption` für Nachrichtengrößenlimits](https://github.com/etcd-io/etcd/pull/9047) zu unterstützen.

Vorher und nachher

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

#### Geänderte API `clientv3.Lease.TimeToLive` {#changed-clientv3leasetimetolive-api}

Bisher gab die API `clientv3.Lease.TimeToLive` bei einer nicht vorhandenen Lease-ID `lease.ErrLeaseNotFound` zurück. 3.2 gibt stattdessen TTL=-1 in der Antwort und keinen Fehler zurück (siehe [#7305](https://github.com/etcd-io/etcd/pull/7305)).

Vorher

```go
// when leaseID does not exist
resp, err := TimeToLive(ctx, leaseID)
resp == nil
err == lease.ErrLeaseNotFound
```

Nachher

```go
// when leaseID does not exist
resp, err := TimeToLive(ctx, leaseID)
resp.TTL == -1
err == nil
```

#### `clientv3.NewFromConfigFile` nach `clientv3.yaml.NewConfig` verschoben {#moved-clientv3newfromconfigfile-to-clientv3yamlnewconfig}

`clientv3.NewFromConfigFile` wurde nach `yaml.NewConfig` verschoben.

Vorher

```go
import "github.com/coreos/etcd/clientv3"
clientv3.NewFromConfigFile
```

Nachher

```go
import clientv3yaml "github.com/coreos/etcd/clientv3/yaml"
clientv3yaml.NewConfig
```

#### Änderung an `--listen-peer-urls` und `--listen-client-urls` {#change-in---listen-peer-urls-and---listen-client-urls}

3.2 weist jetzt Domainnamen für `--listen-peer-urls` und `--listen-client-urls` zurück (3.1 gibt nur Warnungen aus), da ein Domainname für die Bindung an eine Netzwerkschnittstelle ungültig ist. Stellen Sie sicher, dass diese URLs korrekt als `scheme://IP:port` formatiert sind.

Weitere Hintergründe finden Sie in [Issue #6336](https://github.com/etcd-io/etcd/issues/6336).

### Checklisten für das Server-Upgrade {#server-upgrade-checklists}

#### Upgrade-Voraussetzungen {#upgrade-requirements}

Um eine bestehende etcd-Installation auf 3.2 zu aktualisieren, muss der laufende Cluster Version 3.1 oder höher verwenden. Falls er eine ältere Version als 3.1 verwendet, führen Sie vor dem Upgrade auf 3.2 zunächst ein [Upgrade auf 3.1](/de/etcd/upgrades/upgrade_3_1) durch.

Außerdem muss der laufende Cluster fehlerfrei sein, damit das Rolling Upgrade reibungslos verläuft. Prüfen Sie den Zustand des Clusters mit dem Befehl `etcdctl endpoint health`, bevor Sie fortfahren.

#### Vorbereitung {#preparation}

Testen Sie vor einem etcd-Upgrade immer die von etcd abhängigen Dienste in einer Staging-Umgebung, bevor Sie das Upgrade in der Produktionsumgebung durchführen.

[Erstellen Sie vor Beginn ein Backup der etcd-Daten](/de/etcd/op-guide/maintenance#snapshot-backup). Falls beim Upgrade etwas schiefgeht, können Sie mit diesem Backup ein [Downgrade](#downgrade) auf die bestehende etcd-Version durchführen. Beachten Sie, dass der Befehl `snapshot` nur die v3-Daten sichert. Informationen zu v2-Daten finden Sie unter [Backup des v2-Datenspeichers](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore).

#### Gemischte Versionen {#mixed-versions}

Während des Upgrades unterstützt ein etcd-Cluster Mitglieder mit gemischten etcd-Versionen und verwendet das Protokoll der niedrigsten gemeinsamen Version. Der Cluster gilt erst als aktualisiert, wenn alle Mitglieder auf Version 3.2 aktualisiert wurden. Intern handeln die etcd-Mitglieder untereinander die Gesamtversion des Clusters aus, die die gemeldete Version und die unterstützten Funktionen bestimmt.

#### Einschränkungen {#limitations}

Hinweis: Wenn der Cluster nur v3-Daten und keine v2-Daten enthält, gilt diese Einschränkung nicht.

Wenn der Cluster einen v2-Datenbestand von mehr als 50MB bereitstellt, kann es bis zu zwei Minuten dauern, bis jedes neu aktualisierte Mitglied zum bestehenden Cluster aufgeschlossen hat. Prüfen Sie die Größe eines aktuellen Snapshots, um die Gesamtdatenmenge abzuschätzen. Anders ausgedrückt ist es am sichersten, zwischen den Upgrades der einzelnen Mitglieder jeweils 2 Minuten zu warten.

Bei einer deutlich größeren Gesamtdatenmenge von 100MB oder mehr kann dieser einmalige Vorgang noch länger dauern. Administratoren sehr großer etcd-Cluster dieser Größenordnung können vor dem Upgrade das [etcd-Team][etcd-contact] kontaktieren; wir beraten Sie gern zum Vorgehen.

#### Downgrade {#downgrade}

Wenn alle Mitglieder auf v3.2 aktualisiert wurden, wird der Cluster auf v3.2 aktualisiert; ein Downgrade aus diesem abgeschlossenen Zustand ist **nicht möglich**. Solange jedoch noch ein einziges Mitglied v3.1 verwendet, bleiben der Cluster und sein Betrieb auf „v3.1“. Aus diesem Zustand mit gemischten Versionen ist es möglich, auf allen Mitgliedern wieder eine etcd-v3.1-Binärdatei zu verwenden.

[Erstellen Sie ein Backup des Datenverzeichnisses](/de/etcd/op-guide/maintenance#snapshot-backup) aller etcd-Mitglieder, um ein Downgrade des Clusters auch nach einem vollständig abgeschlossenen Upgrade zu ermöglichen.

### Upgrade-Verfahren {#upgrade-procedure}

Dieses Beispiel zeigt das Upgrade eines etcd-v3.1-Clusters mit 3 Mitgliedern, der auf einem lokalen Rechner läuft.

#### 1. Upgrade-Voraussetzungen prüfen {#1-check-upgrade-requirements}

Ist der Cluster fehlerfrei und läuft er mit v3.1.x?

```
$ ETCDCTL_API=3 etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 6.600684ms
localhost:22379 is healthy: successfully committed proposal: took = 8.540064ms
localhost:32379 is healthy: successfully committed proposal: took = 8.763432ms

$ curl http://localhost:2379/version
{"etcdserver":"3.1.7","etcdcluster":"3.1.0"}
```

#### 2. Den bestehenden etcd-Prozess stoppen {#2-stop-the-existing-etcd-process}

Wenn ein etcd-Prozess gestoppt wird, protokollieren die anderen Cluster-Mitglieder erwartete Fehler. Dies ist normal, da die Verbindung zu einem Cluster-Mitglied (vorübergehend) unterbrochen wurde:

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

An dieser Stelle empfiehlt es sich, [ein Backup der etcd-Daten zu erstellen](/de/etcd/op-guide/maintenance#snapshot-backup), um bei Problemen ein Downgrade durchführen zu können:

```
$ etcdctl snapshot save backup.db
```

#### 3. Die etcd-v3.2-Binärdatei einsetzen und den neuen etcd-Prozess starten {#3-drop-in-etcd-v32-binary-and-start-the-new-etcd-process}

Das neue etcd v3.2 veröffentlicht seine Informationen im Cluster:

```
2017-04-27 14:14:25.363225 I | etcdserver: published {Name:s1 ClientURLs:[http://localhost:2379]} to cluster a9ededbffcb1b1f1
```

Prüfen Sie, ob jedes Mitglied und anschließend der gesamte Cluster mit der neuen etcd-v3.2-Binärdatei wieder fehlerfrei ist:

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:22379 is healthy: successfully committed proposal: took = 5.540129ms
localhost:32379 is healthy: successfully committed proposal: took = 7.321771ms
localhost:2379 is healthy: successfully committed proposal: took = 10.629901ms
```

Aktualisierte Mitglieder protokollieren Warnungen wie die folgenden, bis der gesamte Cluster aktualisiert ist. Dies ist zu erwarten und endet, sobald alle etcd-Cluster-Mitglieder auf v3.2 aktualisiert wurden:

```
2017-04-27 14:15:17.071804 W | etcdserver: member c89feb932daef420 has a higher version 3.2.0
2017-04-27 14:15:21.073110 W | etcdserver: the local etcd version 3.1.7 is not up-to-date
2017-04-27 14:15:21.073142 W | etcdserver: member 6d4f535bae3ab960 has a higher version 3.2.0
2017-04-27 14:15:21.073157 W | etcdserver: the local etcd version 3.1.7 is not up-to-date
2017-04-27 14:15:21.073164 W | etcdserver: member c89feb932daef420 has a higher version 3.2.0
```

#### 4. Schritt 2 bis Schritt 3 für alle anderen Mitglieder wiederholen {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. Abschluss {#5-finish}

Sobald alle Mitglieder aktualisiert wurden, meldet der Cluster den erfolgreichen Abschluss des Upgrades auf 3.2:

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
