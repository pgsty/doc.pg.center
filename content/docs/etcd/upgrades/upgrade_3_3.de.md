---
title: Upgrade von etcd 3.2 auf 3.3
weight: 6750
description: Verfahren, Checklisten und Hinweise zum Upgrade von etcd 3.2 auf 3.3
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_3.md"
aliases: [/etcd/upgrades/upgrade_3_3/]
---

Im Allgemeinen kann das Upgrade von etcd 3.2 auf 3.3 als Rolling Upgrade ohne Ausfallzeit erfolgen:
 - Die etcd-v3.2-Prozesse nacheinander stoppen und durch etcd-v3.3-Prozesse ersetzen.
 - Sobald alle v3.3-Prozesse laufen, stehen dem Cluster die neuen Funktionen von v3.3 zur Verfügung.

Lesen Sie zur Vorbereitung den Rest dieses Leitfadens, bevor Sie [mit dem Upgrade beginnen](#upgrade-procedure).

### Checklisten für das Upgrade {#upgrade-checklists}

> [!WARNING]
> Bei der [Migration von v2 ohne v3-Daten](https://github.com/etcd-io/etcd/issues/9480) löst der etcd-Server v3.2+ eine Panic aus, wenn etcd aus vorhandenen Snapshots wiederhergestellt wird, aber keine v3-Datei `ETCD_DATA_DIR/member/snap/db` vorhanden ist. Dies tritt auf, wenn der Server von v2 migriert wurde, ohne zuvor v3-Daten zu enthalten. Dadurch wird auch ein versehentlicher Verlust von v3-Daten verhindert (z. B. könnte die Datei `db` verschoben worden sein). etcd verlangt, dass weitere Migrationen nach der Migration auf v3 nur mit v3-Daten erfolgen können. Führen Sie kein Upgrade auf neuere v3-Versionen durch, bevor der v3.0-Server v3-Daten enthält.

> [!WARNING]
> Wenn Sie Authentifizierung aktivieren und Leases mit kurzer TTL verwenden, tritt mit hoher Wahrscheinlichkeit ein [Problem](https://github.com/etcd-io/etcd/issues/11689) auf, das zu Dateninkonsistenzen führt. Es wird dringend empfohlen, zunächst auf 3.2.31+ zu aktualisieren, um dieses Problem zu beheben, und erst anschließend auf 3.3. Wenn ein Benutzer ohne Berechtigung während des Upgrades eine `LeaseRevoke`-Anfrage an den 3.3-Knoten sendet, kann dies außerdem weiterhin Datenbeschädigungen verursachen. Stellen Sie daher vor dem Upgrade am besten sicher, dass solche unzulässigen Aufrufe in Ihrer Umgebung nicht vorkommen. Einzelheiten finden Sie in [#11691](https://github.com/etcd-io/etcd/pull/11691).


Wichtige inkompatible Änderungen in 3.3.

#### Werttyp des Flags `etcd --auto-compaction-retention` in `string` geändert {#changed-value-type-of-etcd---auto-compaction-retention-flag-to-string}

Das Flag `--auto-compaction-retention` wurde so geändert, dass es [Zeichenfolgenwerte akzeptiert](https://github.com/etcd-io/etcd/pull/8563), und zwar mit [feinerer Granularität](https://github.com/etcd-io/etcd/issues/8503). Da `--auto-compaction-retention` jetzt Zeichenfolgenwerte akzeptiert, muss das Feld `auto-compaction-retention` in der YAML-Konfigurationsdatei von etcd auf den Typ `string` geändert werden. Bisher konnte `--config-file etcd.config.yaml` das Feld `auto-compaction-retention: 24` enthalten; jetzt muss es `auto-compaction-retention: "24"` oder `auto-compaction-retention: "24h"` lauten. Bei der Konfiguration `--auto-compaction-mode periodic --auto-compaction-retention "24h"` muss der Zeitdauerwert des Flags `--auto-compaction-retention` für die Go-Funktion [`time.ParseDuration`](https://golang.org/pkg/time/#ParseDuration) gültig sein.

```diff
# etcd.config.yaml
+auto-compaction-mode: periodic
-auto-compaction-retention: 24
+auto-compaction-retention: "24"
+# Or
+auto-compaction-retention: "24h"
```

#### `*etcdserver.ServerConfig` in `etcdserver.ServerConfig` geändert {#changed-etcdserveretcdserverserverconfig-to-etcdserveretcdserverserverconfig}

`etcdserver.EtcdServer` hat den Typ seines Mitgliedsfelds von `*etcdserver.ServerConfig` in `etcdserver.ServerConfig` geändert. Außerdem akzeptiert `etcdserver.NewServer` jetzt `etcdserver.ServerConfig` anstelle von `*etcdserver.ServerConfig`.

Vorher und nachher (z. B. [k8s.io/kubernetes/test/e2e_node/services/etcd.go](https://github.com/kubernetes/kubernetes/blob/release-1.8/test/e2e_node/services/etcd.go#L50-L55))

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

#### Feld `embed.Config.LogOutput` hinzugefügt {#added-embedconfiglogoutput-struct}

> [!WARNING]
> Beachten Sie, dass dieses Feld in v3.4 in `embed.Config.LogOutputs` mit dem Typ `[]string` umbenannt wurde. Weitere Einzelheiten finden Sie im [Upgrade-Leitfaden für v3.4](/de/docs/etcd/upgrades/upgrade_3_4/).

Das Feld `LogOutput` wurde zu `embed.Config` hinzugefügt:

```diff
package embed

type Config struct {
 	Debug bool `json:"debug"`
 	LogPkgLevels string `json:"log-package-levels"`
+	LogOutput string `json:"log-output"`
 	...
```

Bisher wurden gRPC-Serverwarnungen in etcdserver protokolliert.

```
WARNING: 2017/11/02 11:35:51 grpc: addrConn.resetTransport failed to create client transport: connection error: desc = "transport: Error while dialing dial tcp: operation was canceled"; Reconnecting to {localhost:2379 <nil>}
WARNING: 2017/11/02 11:35:51 grpc: addrConn.resetTransport failed to create client transport: connection error: desc = "transport: Error while dialing dial tcp: operation was canceled"; Reconnecting to {localhost:2379 <nil>}
```

Ab v3.3 sind gRPC-Serverprotokolle standardmäßig deaktiviert.

> [!WARNING]
> Beachten Sie, dass die Methode `embed.Config.SetupLogging` seit v3.4 veraltet ist. Weitere Einzelheiten finden Sie im [Upgrade-Leitfaden für v3.4](/de/docs/etcd/upgrades/upgrade_3_4/).

```go
import "github.com/coreos/etcd/embed"

cfg := &embed.Config{Debug: false}
cfg.SetupLogging()
```

Setzen Sie das Feld `embed.Config.Debug` auf `true`, um gRPC-Serverprotokolle zu aktivieren.

#### Geänderte Antwort des Endpunkts `/health` {#changed-health-endpoint-response}

Bisher gab `[endpoint]:[client-port]/health` einen manuell serialisierten JSON-Wert zurück. 3.3 definiert jetzt die Struktur [`etcdhttp.Health`](https://pkg.go.dev/github.com/etcd-io/etcd/etcdserver/api/etcdhttp#Health).

Beachten Sie, dass `etcdhttp.Health` in v3.3.0-rc.0, v3.3.0-rc.1 und v3.3.0-rc.2 die booleschen Felder `"health"` und `"errors"` besitzt. Aus Gründen der Abwärtskompatibilität haben wir das Feld `"health"` auf den Typ `string` zurückgesetzt und das Feld `"errors"` entfernt. Weitere Zustandsinformationen werden über separate APIs bereitgestellt.

```bash
$ curl http://localhost:2379/health
{"health":"true"}
```

#### Geänderte HTTP-Endpunkte des gRPC-Gateways (`/v3alpha` durch `/v3beta` ersetzt) {#changed-grpc-gateway-http-endpoints-replaced-v3alpha-with-v3beta}

Vorher

```bash
curl -L http://localhost:2379/v3alpha/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

Nachher

```bash
curl -L http://localhost:2379/v3beta/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

Anfragen an `/v3alpha`-Endpunkte werden an `/v3beta` umgeleitet; `/v3alpha` wird im Release 3.4 entfernt.

#### Geänderte Obergrenzen für die Anfragegröße {#changed-maximum-request-size-limits}

3.3 erlaubt jetzt benutzerdefinierte Größenlimits für Anfragen sowohl auf der Server- als auch auf der **Clientseite**. In früheren Versionen (v3.2.10, v3.2.11) war die Größe der Antworten an Clients auf nur 4 MiB begrenzt.

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

#### Geänderte Funktionssignaturen der Wrapper für direkte gRPC-Clients {#changed-raw-grpc-client-wrapper-function-signatures}

3.3 ändert die Funktionssignaturen des gRPC-Client-Wrappers von `clientv3`. Diese Änderung war erforderlich, um [benutzerdefinierte `grpc.CallOption` für Nachrichtengrößenlimits](https://github.com/etcd-io/etcd/pull/9047) zu unterstützen.

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

#### Geänderter Fehlertyp der clientv3-API `Snapshot` {#changed-clientv3-snapshot-api-error-type}

Bisher gab die clientv3-API `Snapshot` unverarbeitete Fehler vom Typ [`grpc/*status.statusError`] zurück. v3.3 wandelt diese Fehler jetzt in die entsprechenden öffentlichen Fehlertypen um, um mit anderen APIs konsistent zu sein.

Vorher

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

Nachher

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

#### Geänderte Ausgabe des Befehls `etcdctl lease timetolive` {#changed-etcdctl-lease-timetolive-command-output}

Bisher gab der Befehl `lease timetolive LEASE_ID` bei einer abgelaufenen Lease `-1s` als verbleibende Sekunden aus. 3.3 gibt jetzt klarere Meldungen aus.

Vorher


```bash
lease 2d8257079fa1bc0c granted with TTL(0s), remaining(-1s)
```

Nachher

```bash
lease 2d8257079fa1bc0c already expired
```

#### Geänderte Importe von `golang.org/x/net/context` {#changed-golangorgxnetcontext-imports}

`clientv3` hat `golang.org/x/net/context` als veraltet eingestuft. Wenn ein Projekt `golang.org/x/net/context` in anderem Code als eingebundene Abhängigkeit mitführt (z. B. in von etcd generiertem Protocol-Buffer-Code) und `github.com/coreos/etcd/clientv3` importiert, wird zum Kompilieren Go 1.9+ benötigt.

Vorher

```go
import "golang.org/x/net/context"
cli.Put(context.Background(), "f", "v")
```

Nachher

```go
import "context"
cli.Put(context.Background(), "f", "v")
```

#### Geänderte gRPC-Abhängigkeit {#changed-grpc-dependency}

3.3 benötigt jetzt [grpc/grpc-go](https://github.com/grpc/grpc-go/releases) `v1.7.5`.

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

Bisher wurde bei Zeitüberschreitungen beim Verbindungsaufbau des Clients der Fehler `grpc.ErrClientConnTimeout` zurückgegeben. 3.3 gibt stattdessen `context.DeadlineExceeded` zurück (siehe [#8504](https://github.com/etcd-io/etcd/issues/8504)).

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

#### Geänderte offizielle Container-Registry {#changed-official-container-registry}

etcd verwendet jetzt [`gcr.io/etcd-development/etcd`](https://gcr.io/etcd-development/etcd) als primäre und [`quay.io/coreos/etcd`](https://quay.io/coreos/etcd) als sekundäre Container-Registry.

Vorher

```bash
docker pull quay.io/coreos/etcd:v3.2.5
```

Nachher

```bash
docker pull gcr.io/etcd-development/etcd:v3.3.0
```

### Upgrades auf >= v3.3.14 {#upgrades-to--v3314}

[v3.3.14](https://github.com/etcd-io/etcd/releases/tag/v3.3.14) musste einige Funktionen aus 3.4 aufnehmen, wobei versucht wurde, die Unterschiede zwischen den Implementierungen des Client-Balancers möglichst gering zu halten. Dieses Release behebt [„kube-apiserver 1.13.x verweigert die Arbeit, wenn der erste etcd-Server nicht verfügbar ist“ (kubernetes#72102)](https://github.com/kubernetes/kubernetes/issues/72102).

`grpc.ErrClientConnClosing` ist [seit gRPC >= 1.10 veraltet](https://github.com/grpc/grpc-go/pull/1854).

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

[Der neue Client-Balancer](/de/docs/etcd/learning/design-client/) verwendet einen asynchronen Resolver, um Endpunkte an die gRPC-Funktion zum Verbindungsaufbau zu übergeben. Daher benötigt [v3.3.14](https://github.com/etcd-io/etcd/releases/tag/v3.3.14) oder höher die Option `grpc.WithBlock` beim Verbindungsaufbau, um zu warten, bis die zugrunde liegende Verbindung hergestellt ist.

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

Eine vollständige Liste der Änderungen finden Sie im [Änderungsprotokoll (CHANGELOG)](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.3.md).

### Checklisten für das Server-Upgrade {#server-upgrade-checklists}

#### Upgrade-Voraussetzungen {#upgrade-requirements}

Um eine bestehende etcd-Installation auf 3.3 zu aktualisieren, muss der laufende Cluster Version 3.2 oder höher verwenden. Falls er eine ältere Version als 3.2 verwendet, führen Sie vor dem Upgrade auf 3.3 zunächst ein [Upgrade auf 3.2](/de/docs/etcd/upgrades/upgrade_3_2/) durch.

Außerdem muss der laufende Cluster fehlerfrei sein, damit das Rolling Upgrade reibungslos verläuft. Prüfen Sie den Zustand des Clusters mit dem Befehl `etcdctl endpoint health`, bevor Sie fortfahren.

#### Vorbereitung {#preparation}

Testen Sie vor einem etcd-Upgrade immer die von etcd abhängigen Dienste in einer Staging-Umgebung, bevor Sie das Upgrade in der Produktionsumgebung durchführen.

[Erstellen Sie vor Beginn ein Backup der etcd-Daten](/de/docs/etcd/op-guide/maintenance/#snapshot-backup). Falls beim Upgrade etwas schiefgeht, können Sie mit diesem Backup ein [Downgrade](#downgrade) auf die bestehende etcd-Version durchführen. Beachten Sie, dass der Befehl `snapshot` nur die v3-Daten sichert. Informationen zu v2-Daten finden Sie unter [Backup des v2-Datenspeichers](https://etcd.io/docs/v2.3/admin_guide/#backing-up-the-datastore).

#### Gemischte Versionen {#mixed-versions}

Während des Upgrades unterstützt ein etcd-Cluster Mitglieder mit gemischten etcd-Versionen und verwendet das Protokoll der niedrigsten gemeinsamen Version. Der Cluster gilt erst als aktualisiert, wenn alle Mitglieder auf Version 3.3 aktualisiert wurden. Intern handeln die etcd-Mitglieder untereinander die Gesamtversion des Clusters aus, die die gemeldete Version und die unterstützten Funktionen bestimmt.

#### Einschränkungen {#limitations}

Hinweis: Wenn der Cluster nur v3-Daten und keine v2-Daten enthält, gilt diese Einschränkung nicht.

Wenn der Cluster einen v2-Datenbestand von mehr als 50MB bereitstellt, kann es bis zu zwei Minuten dauern, bis jedes neu aktualisierte Mitglied zum bestehenden Cluster aufgeschlossen hat. Prüfen Sie die Größe eines aktuellen Snapshots, um die Gesamtdatenmenge abzuschätzen. Anders ausgedrückt ist es am sichersten, zwischen den Upgrades der einzelnen Mitglieder jeweils 2 Minuten zu warten.

Bei einer deutlich größeren Gesamtdatenmenge von 100MB oder mehr kann dieser einmalige Vorgang noch länger dauern. Administratoren sehr großer etcd-Cluster dieser Größenordnung können vor dem Upgrade das [etcd-Team][etcd-contact] kontaktieren; wir beraten Sie gern zum Vorgehen.

#### Downgrade {#downgrade}

Wenn alle Mitglieder auf v3.3 aktualisiert wurden, wird der Cluster auf v3.3 aktualisiert; ein Downgrade aus diesem abgeschlossenen Zustand ist **nicht möglich**. Solange jedoch noch ein einziges Mitglied v3.2 verwendet, bleiben der Cluster und sein Betrieb auf „v3.2“. Aus diesem Zustand mit gemischten Versionen ist es möglich, auf allen Mitgliedern wieder eine etcd-v3.2-Binärdatei zu verwenden.

[Erstellen Sie ein Backup des Datenverzeichnisses](/de/docs/etcd/op-guide/maintenance/#snapshot-backup) aller etcd-Mitglieder, um ein Downgrade des Clusters auch nach einem vollständig abgeschlossenen Upgrade zu ermöglichen.

### Upgrade-Verfahren {#upgrade-procedure}

Dieses Beispiel zeigt das Upgrade eines etcd-v3.2-Clusters mit 3 Mitgliedern, der auf einem lokalen Rechner läuft.

#### 1. Upgrade-Voraussetzungen prüfen {#1-check-upgrade-requirements}

Ist der Cluster fehlerfrei und läuft er mit v3.2.x?

```
$ ETCDCTL_API=3 etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 6.600684ms
localhost:22379 is healthy: successfully committed proposal: took = 8.540064ms
localhost:32379 is healthy: successfully committed proposal: took = 8.763432ms

$ curl http://localhost:2379/version
{"etcdserver":"3.2.7","etcdcluster":"3.2.0"}
```

#### 2. Den bestehenden etcd-Prozess stoppen {#2-stop-the-existing-etcd-process}

Wenn ein etcd-Prozess gestoppt wird, protokollieren die anderen Cluster-Mitglieder erwartete Fehler. Dies ist normal, da die Verbindung zu einem Cluster-Mitglied (vorübergehend) unterbrochen wurde:

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

An dieser Stelle empfiehlt es sich, [ein Backup der etcd-Daten zu erstellen](/de/docs/etcd/op-guide/maintenance/#snapshot-backup), um bei Problemen ein Downgrade durchführen zu können:

```
$ etcdctl snapshot save backup.db
```

#### 3. Die etcd-v3.3-Binärdatei einsetzen und den neuen etcd-Prozess starten {#3-drop-in-etcd-v33-binary-and-start-the-new-etcd-process}

Das neue etcd v3.3 veröffentlicht seine Informationen im Cluster:

```
14:14:25.363225 I | etcdserver: published {Name:s1 ClientURLs:[http://localhost:2379]} to cluster a9ededbffcb1b1f1
```

Prüfen Sie, ob jedes Mitglied und anschließend der gesamte Cluster mit der neuen etcd-v3.3-Binärdatei wieder fehlerfrei ist:

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:22379 is healthy: successfully committed proposal: took = 5.540129ms
localhost:32379 is healthy: successfully committed proposal: took = 7.321771ms
localhost:2379 is healthy: successfully committed proposal: took = 10.629901ms
```

Aktualisierte Mitglieder protokollieren Warnungen wie die folgenden, bis der gesamte Cluster aktualisiert ist. Dies ist zu erwarten und endet, sobald alle etcd-Cluster-Mitglieder auf v3.3 aktualisiert wurden:

```
14:15:17.071804 W | etcdserver: member c89feb932daef420 has a higher version 3.3.0
14:15:21.073110 W | etcdserver: the local etcd version 3.2.7 is not up-to-date
14:15:21.073142 W | etcdserver: member 6d4f535bae3ab960 has a higher version 3.3.0
14:15:21.073157 W | etcdserver: the local etcd version 3.2.7 is not up-to-date
14:15:21.073164 W | etcdserver: member c89feb932daef420 has a higher version 3.3.0
```

#### 4. Schritt 2 bis Schritt 3 für alle anderen Mitglieder wiederholen {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. Abschluss {#5-finish}

Sobald alle Mitglieder aktualisiert wurden, meldet der Cluster den erfolgreichen Abschluss des Upgrades auf 3.3:

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
