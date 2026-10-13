---
title: Upgrade von etcd 3.3 auf 3.4
weight: 6700
description: Verfahren, Checklisten und Hinweise zum Upgrade von etcd 3.3 auf 3.4
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_4.md"
aliases: [/etcd/upgrades/upgrade_3_4/]
---

Im Allgemeinen kann das Upgrade von etcd 3.3 auf 3.4 als Rolling Upgrade ohne Ausfallzeit erfolgen:
 - Die etcd-v3.3-Prozesse nacheinander stoppen und durch etcd-v3.4-Prozesse ersetzen.
 - Sobald alle v3.4-Prozesse laufen, stehen dem Cluster die neuen Funktionen von v3.4 zur Verfügung.

Lesen Sie zur Vorbereitung den Rest dieses Leitfadens, bevor Sie [mit dem Upgrade beginnen](#upgrade-procedure).



### Checklisten für das Upgrade {#upgrade-checklists}

> [!WARNING]
> Bei der [Migration von v2 ohne v3-Daten](https://github.com/etcd-io/etcd/issues/9480) löst der etcd-Server v3.2+ eine Panic aus, wenn etcd aus vorhandenen Snapshots wiederhergestellt wird, aber keine v3-Datei `ETCD_DATA_DIR/member/snap/db` vorhanden ist. Dies tritt auf, wenn der Server von v2 migriert wurde, ohne zuvor v3-Daten zu enthalten. Dadurch wird auch ein versehentlicher Verlust von v3-Daten verhindert (z. B. könnte die Datei `db` verschoben worden sein). etcd verlangt, dass weitere Migrationen nach der Migration auf v3 nur mit v3-Daten erfolgen können. Führen Sie kein Upgrade auf neuere v3-Versionen durch, bevor der v3.0-Server v3-Daten enthält.

Wichtige inkompatible Änderungen in 3.4.

#### `ETCDCTL_API=3 etcdctl` wird zum Standard {#make-etcdctl_api3-etcdctl-default}

`ETCDCTL_API=3` ist jetzt der Standard.

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

#### `etcd --enable-v2=false` wird zum Standard {#make-etcd---enable-v2false-default}

[`etcd --enable-v2=false`](https://github.com/etcd-io/etcd/pull/10935) ist jetzt der Standard.

Das bedeutet, dass der etcd-v3.4-Server keine v2-API-Anfragen bedient, sofern nicht `etcd --enable-v2=true` angegeben wird.

Wenn die v2-API verwendet wurde, aktivieren Sie die v2-API unbedingt in v3.4:

```diff
-etcd
+etcd --enable-v2=true
```

Andere HTTP-APIs funktionieren weiterhin (z. B. `[CLIENT-URL]/metrics`, `[CLIENT-URL]/health`, v3-gRPC-Gateway).

#### Veraltete Flags `etcd --ca-file` und `etcd --peer-ca-file` {#deprecated-etcd---ca-file-and-etcd---peer-ca-file-flags}

Die Flags `--ca-file` und `--peer-ca-file` sind veraltet; sie sind bereits seit v2.1 veraltet.

Beachten Sie, dass das Setzen dieses Parameters auch die Client-Zertifikatsauthentifizierung automatisch aktiviert, unabhängig vom Wert von `--client-cert-auth`.

```diff
-etcd --ca-file ca-client.crt
+etcd --trusted-ca-file ca-client.crt
```

```diff
-etcd --peer-ca-file ca-peer.crt
+etcd --peer-trusted-ca-file ca-peer.crt
```

#### Veralteter Fehler `grpc.ErrClientConnClosing` {#deprecated-grpcerrclientconnclosing-error}

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

#### `grpc.WithBlock` für den Verbindungsaufbau des Clients erforderlich {#require-grpcwithblock-for-client-dial}

[Der neue Client-Balancer](/de/docs/etcd/learning/design-client/) verwendet einen asynchronen Resolver, um Endpunkte an die gRPC-Funktion zum Verbindungsaufbau zu übergeben. Daher benötigt der v3.4-Client die Option `grpc.WithBlock` beim Verbindungsaufbau, um zu warten, bis die zugrunde liegende Verbindung hergestellt ist.

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

#### Prometheus-Metrik `etcd_debugging_mvcc_db_total_size_in_bytes` wird als veraltet eingestuft {#deprecating-etcd_debugging_mvcc_db_total_size_in_bytes-prometheus-metrics}

v3.4 überführt die Prometheus-Metrik `etcd_debugging_mvcc_db_total_size_in_bytes` in `etcd_mvcc_db_total_size_in_bytes`, um die Überwachung des etcd-Speichers zu fördern.

`etcd_debugging_mvcc_db_total_size_in_bytes` wird in v3.4 aus Gründen der Abwärtskompatibilität weiterhin bereitgestellt. In v3.5 wird sie vollständig als veraltet eingestuft.

```diff
-etcd_debugging_mvcc_db_total_size_in_bytes
+etcd_mvcc_db_total_size_in_bytes
```

Beachten Sie, dass Metriken im Namensraum `etcd_debugging_*` als experimentell gekennzeichnet sind. Im Zuge der Verbesserung des Überwachungsleitfadens können wir weitere Metriken hochstufen.

#### Prometheus-Metrik `etcd_debugging_mvcc_put_total` wird als veraltet eingestuft {#deprecating-etcd_debugging_mvcc_put_total-prometheus-metrics}

v3.4 überführt die Prometheus-Metrik `etcd_debugging_mvcc_put_total` in `etcd_mvcc_put_total`, um die Überwachung des etcd-Speichers zu fördern.

`etcd_debugging_mvcc_put_total` wird in v3.4 aus Gründen der Abwärtskompatibilität weiterhin bereitgestellt. In v3.5 wird sie vollständig als veraltet eingestuft.

```diff
-etcd_debugging_mvcc_put_total
+etcd_mvcc_put_total
```

Beachten Sie, dass Metriken im Namensraum `etcd_debugging_*` als experimentell gekennzeichnet sind. Im Zuge der Verbesserung des Überwachungsleitfadens können wir weitere Metriken hochstufen.

#### Prometheus-Metrik `etcd_debugging_mvcc_delete_total` wird als veraltet eingestuft {#deprecating-etcd_debugging_mvcc_delete_total-prometheus-metrics}

v3.4 überführt die Prometheus-Metrik `etcd_debugging_mvcc_delete_total` in `etcd_mvcc_delete_total`, um die Überwachung des etcd-Speichers zu fördern.

`etcd_debugging_mvcc_delete_total` wird in v3.4 aus Gründen der Abwärtskompatibilität weiterhin bereitgestellt. In v3.5 wird sie vollständig als veraltet eingestuft.

```diff
-etcd_debugging_mvcc_delete_total
+etcd_mvcc_delete_total
```

Beachten Sie, dass Metriken im Namensraum `etcd_debugging_*` als experimentell gekennzeichnet sind. Im Zuge der Verbesserung des Überwachungsleitfadens können wir weitere Metriken hochstufen.

#### Prometheus-Metrik `etcd_debugging_mvcc_txn_total` wird als veraltet eingestuft {#deprecating-etcd_debugging_mvcc_txn_total-prometheus-metrics}

v3.4 überführt die Prometheus-Metrik `etcd_debugging_mvcc_txn_total` in `etcd_mvcc_txn_total`, um die Überwachung des etcd-Speichers zu fördern.

`etcd_debugging_mvcc_txn_total` wird in v3.4 aus Gründen der Abwärtskompatibilität weiterhin bereitgestellt. In v3.5 wird sie vollständig als veraltet eingestuft.

```diff
-etcd_debugging_mvcc_txn_total
+etcd_mvcc_txn_total
```

Beachten Sie, dass Metriken im Namensraum `etcd_debugging_*` als experimentell gekennzeichnet sind. Im Zuge der Verbesserung des Überwachungsleitfadens können wir weitere Metriken hochstufen.

#### Prometheus-Metrik `etcd_debugging_mvcc_range_total` wird als veraltet eingestuft {#deprecating-etcd_debugging_mvcc_range_total-prometheus-metrics}

v3.4 überführt die Prometheus-Metrik `etcd_debugging_mvcc_range_total` in `etcd_mvcc_range_total`, um die Überwachung des etcd-Speichers zu fördern.

`etcd_debugging_mvcc_range_total` wird in v3.4 aus Gründen der Abwärtskompatibilität weiterhin bereitgestellt. In v3.5 wird sie vollständig als veraltet eingestuft.

```diff
-etcd_debugging_mvcc_range_total
+etcd_mvcc_range_total
```

Beachten Sie, dass Metriken im Namensraum `etcd_debugging_*` als experimentell gekennzeichnet sind. Im Zuge der Verbesserung des Überwachungsleitfadens können wir weitere Metriken hochstufen.

#### Flag `etcd --log-output` wird als veraltet eingestuft (jetzt `--log-outputs`) {#deprecating-etcd---log-output-flag-now---log-outputs}

[`etcd --log-output` wird in `--log-outputs` umbenannt](https://github.com/etcd-io/etcd/pull/9624), um mehrere Protokollausgaben zu unterstützen. **`etcd --logger=capnslog` unterstützt nicht mehrere Protokollausgaben.**

**`etcd --log-output`** wird in v3.5 als veraltet eingestuft. **`etcd --logger=capnslog` wird in v3.5 als veraltet eingestuft**.

```diff
-etcd --log-output=stderr
+etcd --log-outputs=stderr

+# to write logs to stderr and a.log file at the same time
+# only "--logger=zap" supports multiple writers
+etcd --logger=zap --log-outputs=stderr,a.log
```

v3.4 unterstützt zusätzlich `etcd --logger=zap --log-outputs=stderr` für strukturierte Protokollierung und mehrere Protokollausgaben. Das Hauptziel ist, die automatisierte Überwachung von etcd zu fördern, statt erst bei auftretenden Fehlern die Serverprotokolle durchzusehen. Die künftige Entwicklung soll die Protokollausgabe von etcd auf ein Minimum reduzieren und die Überwachung mit Metriken und Alarmen erleichtern. **`etcd --logger=capnslog` wird in v3.5 als veraltet eingestuft**.

#### Feldtyp von `log-outputs` in `etcd --config-file` in `[]string` geändert {#changed-log-outputs-field-type-in-etcd---config-file-to-string}

Da `log-outputs` (früherer Feldname `log-output`) jetzt mehrere Ausgabeziele akzeptiert, muss das Feld `log-outputs` in der YAML-Konfigurationsdatei von etcd wie unten gezeigt auf den Typ `[]string` geändert werden:

```diff
 # Specify 'stdout' or 'stderr' to skip journald logging even when running under systemd.
-log-output: default
+log-outputs: [default]
```

#### `embed.Config.LogOutput` in `embed.Config.LogOutputs` umbenannt {#renamed-embedconfiglogoutput-to-embedconfiglogoutputs}

[**`embed.Config.LogOutput`** wurde in **`embed.Config.LogOutputs`** umbenannt](https://github.com/etcd-io/etcd/pull/9624), um mehrere Protokollausgaben zu unterstützen. Außerdem wurde der [Typ von `embed.Config.LogOutput` von `string` in `[]string` geändert](https://github.com/etcd-io/etcd/pull/9579), um mehrere Protokollausgaben zu unterstützen.

```diff
import "github.com/coreos/etcd/embed"

cfg := &embed.Config{Debug: false}
-cfg.LogOutput = "stderr"
+cfg.LogOutputs = []string{"stderr"}
```

#### v3.5 stuft `capnslog` als veraltet ein {#v35-deprecates-capnslog}

**v3.5 wird das Flag `etcd --log-package-levels` für `capnslog` als veraltet einstufen**; `etcd --logger=zap --log-outputs=stderr` wird zum Standard. **v3.5 wird den Endpunkt `[CLIENT-URL]/config/local/log` als veraltet einstufen.**

```diff
-etcd
+etcd --logger zap
```

#### Flag `etcd --debug` wird als veraltet eingestuft (jetzt `--log-level=debug`) {#deprecating-etcd---debug-flag-now---log-leveldebug}

v3.4 stuft das Flag [`etcd --debug`](https://github.com/etcd-io/etcd/pull/10947) als veraltet ein. Verwenden Sie stattdessen das Flag `etcd --log-level=debug`.

```diff
-etcd --debug
+etcd --logger zap --log-level debug
```

#### Veraltetes Feld `pkg/transport.TLSInfo.CAFile` {#deprecated-pkgtransporttlsinfocafile-field}

Das Feld `pkg/transport.TLSInfo.CAFile` ist veraltet.

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

#### `embed.Config.SnapCount` in `embed.Config.SnapshotCount` geändert {#changed-embedconfigsnapcount-to-embedconfigsnapshotcount}

Zur Übereinstimmung mit dem Flag-Namen `etcd --snapshot-count` wurde das Feld `embed.Config.SnapCount` in `embed.Config.SnapshotCount` umbenannt:

```diff
import "github.com/coreos/etcd/embed"

cfg := embed.NewConfig()
-cfg.SnapCount = 100000
+cfg.SnapshotCount = 100000
```

#### `etcdserver.ServerConfig.SnapCount` in `etcdserver.ServerConfig.SnapshotCount` geändert {#changed-etcdserverserverconfigsnapcount-to-etcdserverserverconfigsnapshotcount}

Zur Übereinstimmung mit dem Flag-Namen `etcd --snapshot-count` wurde das Feld `etcdserver.ServerConfig.SnapCount` in `etcdserver.ServerConfig.SnapshotCount` umbenannt:

```diff
import "github.com/coreos/etcd/etcdserver"

srvcfg := etcdserver.ServerConfig{
-  SnapCount: 100000,
+  SnapshotCount: 100000,
```

#### Geänderte Funktionssignatur im Paket `wal` {#changed-function-signature-in-package-wal}

Die Funktionssignaturen von `wal` wurden geändert, um einen strukturierten Logger zu unterstützen.

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

#### Geänderter Typ `IntervalTree` im Paket `pkg/adt` {#changed-intervaltree-type-in-package-pkgadt}

`pkg/adt.IntervalTree` ist jetzt als `interface` definiert.

```diff
import (
    "fmt"

    "go.etcd.io/etcd/pkg/adt"
)

func main() {
-    ivt := &adt.IntervalTree{}
+    ivt := adt.NewIntervalTree()
```

#### `embed.Config.SetupLogging` ist veraltet {#deprecated-embedconfigsetuplogging}

`embed.Config.SetupLogging` wurde entfernt, um fehlerhafte Protokollierungskonfigurationen zu verhindern; die Einrichtung erfolgt jetzt automatisch.

```diff
import "github.com/coreos/etcd/embed"

cfg := &embed.Config{Debug: false}
-cfg.SetupLogging()
```

#### Geänderte HTTP-Endpunkte des gRPC-Gateways (`/v3beta` durch `/v3` ersetzt) {#changed-grpc-gateway-http-endpoints-replaced-v3beta-with-v3}

Vorher

```bash
curl -L http://localhost:2379/v3beta/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

Nachher

```bash
curl -L http://localhost:2379/v3/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

Anfragen an `/v3beta`-Endpunkte werden an `/v3` umgeleitet; `/v3beta` wird im Release 3.5 entfernt.

#### Veraltete Container-Image-Tags {#deprecated-container-image-tags}

`latest` und Image-Tags für Nebenversionen sind veraltet:

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

### Checklisten für das Server-Upgrade {#server-upgrade-checklists}

#### Upgrade-Voraussetzungen {#upgrade-requirements}

Um eine bestehende etcd-Installation auf 3.4 zu aktualisieren, muss der laufende Cluster Version 3.3 oder höher verwenden. Falls er eine ältere Version als 3.3 verwendet, führen Sie vor dem Upgrade auf 3.4 zunächst ein [Upgrade auf 3.3](/de/docs/etcd/upgrades/upgrade_3_3/) durch.

Außerdem muss der laufende Cluster fehlerfrei sein, damit das Rolling Upgrade reibungslos verläuft. Prüfen Sie den Zustand des Clusters mit dem Befehl `etcdctl endpoint health`, bevor Sie fortfahren.

#### Vorbereitung {#preparation}

Testen Sie vor einem etcd-Upgrade immer die von etcd abhängigen Dienste in einer Staging-Umgebung, bevor Sie das Upgrade in der Produktionsumgebung durchführen.

[Laden Sie vor Beginn das Snapshot-Backup herunter](/de/docs/etcd/op-guide/maintenance/#snapshot-backup). Falls beim Upgrade etwas schiefgeht, können Sie mit diesem Backup ein [Downgrade](#downgrade) auf die bestehende etcd-Version durchführen. Beachten Sie, dass der Befehl `snapshot` nur die v3-Daten sichert. Informationen zu v2-Daten finden Sie unter [Backup des v2-Datenspeichers](https://etcd.io/docs/v2.3/admin_guide/#backing-up-the-datastore).

#### Gemischte Versionen {#mixed-versions}

Während des Upgrades unterstützt ein etcd-Cluster Mitglieder mit gemischten etcd-Versionen und verwendet das Protokoll der niedrigsten gemeinsamen Version. Der Cluster gilt erst als aktualisiert, wenn alle Mitglieder auf Version 3.4 aktualisiert wurden. Intern handeln die etcd-Mitglieder untereinander die Gesamtversion des Clusters aus, die die gemeldete Version und die unterstützten Funktionen bestimmt.

#### Einschränkungen {#limitations}

Hinweis: Wenn der Cluster nur v3-Daten und keine v2-Daten enthält, gilt diese Einschränkung nicht.

Wenn der Cluster einen v2-Datenbestand von mehr als 50MB bereitstellt, kann es bis zu zwei Minuten dauern, bis jedes neu aktualisierte Mitglied zum bestehenden Cluster aufgeschlossen hat. Prüfen Sie die Größe eines aktuellen Snapshots, um die Gesamtdatenmenge abzuschätzen. Anders ausgedrückt ist es am sichersten, zwischen den Upgrades der einzelnen Mitglieder jeweils 2 Minuten zu warten.

Bei einer deutlich größeren Gesamtdatenmenge von 100MB oder mehr kann dieser einmalige Vorgang noch länger dauern. Administratoren sehr großer etcd-Cluster dieser Größenordnung können vor dem Upgrade das [etcd-Team][etcd-contact] kontaktieren; wir beraten Sie gern zum Vorgehen.

#### Downgrade {#downgrade}

Wenn alle Mitglieder auf v3.4 aktualisiert wurden, wird der Cluster auf v3.4 aktualisiert; ein Downgrade aus diesem abgeschlossenen Zustand ist **nicht möglich**. Solange jedoch noch ein einziges Mitglied v3.3 verwendet, bleiben der Cluster und sein Betrieb auf „v3.3“. Aus diesem Zustand mit gemischten Versionen ist es möglich, auf allen Mitgliedern wieder eine etcd-v3.3-Binärdatei zu verwenden.

[Laden Sie das Snapshot-Backup herunter](/de/docs/etcd/op-guide/maintenance/#snapshot-backup), um ein Downgrade des Clusters auch nach einem vollständig abgeschlossenen Upgrade zu ermöglichen.

### Upgrade-Verfahren {#upgrade-procedure}

Dieses Beispiel zeigt das Upgrade eines etcd-v3.3-Clusters mit 3 Mitgliedern, der auf einem lokalen Rechner läuft.

#### Schritt 1: Upgrade-Voraussetzungen prüfen {#step-1-check-upgrade-requirements}

Ist der Cluster fehlerfrei und läuft er mit v3.3.x?

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

#### Schritt 2: Snapshot-Backup vom Leader herunterladen {#step-2-download-snapshot-backup-from-leader}

[Laden Sie das Snapshot-Backup herunter](/de/docs/etcd/op-guide/maintenance/#snapshot-backup), um bei Problemen ein Downgrade durchführen zu können.

Der etcd-Leader enthält garantiert die neuesten Anwendungsdaten. Rufen Sie den Snapshot daher vom Leader ab:

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

#### Schritt 3: Einen bestehenden etcd-Server stoppen {#step-3-stop-one-existing-etcd-server}

Wenn ein etcd-Prozess gestoppt wird, protokollieren die anderen Cluster-Mitglieder erwartete Fehler. Dies ist normal, da die Verbindung zu einem Cluster-Mitglied (vorübergehend) unterbrochen wurde:

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

#### Schritt 4: Den etcd-Server mit derselben Konfiguration neu starten {#step-4-restart-the-etcd-server-with-same-configuration}

Starten Sie den etcd-Server mit derselben Konfiguration, aber mit der neuen etcd-Binärdatei neu.

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

Das neue etcd v3.4 veröffentlicht seine Informationen im Cluster. Zu diesem Zeitpunkt verwendet der Cluster weiterhin das Protokoll von v3.3, der niedrigsten gemeinsamen Version.

> `{"level":"info","ts":1526586617.1647713,"caller":"membership/cluster.go:485","msg":"set initial cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1648536,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1649303,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","from":"3.0","from":"3.3"}`

> `{"level":"info","ts":1526586617.1649797,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.3"}`

> `{"level":"info","ts":1526586617.2107732,"caller":"etcdserver/server.go:1770","msg":"published local member to cluster through raft","local-member-id":"7339c4e5e833c029","local-member-attributes":"{Name:s1 ClientURLs:[http://localhost:2379]}","request-path":"/0/members/7339c4e5e833c029/attributes","cluster-id":"7dee9ba76d59ed53","publish-timeout":7}`

Prüfen Sie, ob jedes Mitglied und anschließend der gesamte Cluster mit der neuen etcd-v3.4-Binärdatei wieder fehlerfrei ist:

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:32379 is healthy: successfully committed proposal: took = 2.337471ms
localhost:22379 is healthy: successfully committed proposal: took = 1.130717ms
localhost:2379 is healthy: successfully committed proposal: took = 2.124843ms
COMMENT
```

Noch nicht aktualisierte Mitglieder protokollieren Warnungen wie die folgenden, bis der gesamte Cluster aktualisiert wurde.

Dies ist zu erwarten und endet, sobald alle etcd-Cluster-Mitglieder auf v3.4 aktualisiert wurden:

```
:41.942121 W | etcdserver: member 7339c4e5e833c029 has a higher version 3.4.0
:45.945154 W | etcdserver: the local etcd version 3.3.5 is not up-to-date
```

#### Schritt 5: *Schritt 3* und *Schritt 4* für die übrigen Mitglieder wiederholen {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

Sobald alle Mitglieder aktualisiert wurden, meldet der Cluster den erfolgreichen Abschluss des Upgrades auf 3.4:

Mitglied 1:

> `{"level":"info","ts":1526586949.0920913,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`
> `{"level":"info","ts":1526586949.0921566,"caller":"etcdserver/server.go:2272","msg":"cluster version is updated","cluster-version":"3.4"}`

Mitglied 2:

> `{"level":"info","ts":1526586949.092117,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"729934363faa4a24","from":"3.3","from":"3.4"}`
> `{"level":"info","ts":1526586949.0923078,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`

Mitglied 3:

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
