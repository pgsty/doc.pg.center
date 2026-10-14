---
title: "gRPC-Proxy"
weight: 4350
description: "Ein zustandsloser etcd-Reverse-Proxy auf der gRPC-Schicht"
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/grpc_proxy.md"
---

Der gRPC-Proxy ist ein zustandsloser etcd-Reverse-Proxy auf der gRPC-Schicht (L7). Er soll die gesamte Verarbeitungslast auf dem zentralen etcd-Cluster verringern. Für horizontale Skalierbarkeit führt er Watch- und Lease-API-Anfragen zusammen. Um den Cluster vor missbräuchlich arbeitenden Clients zu schützen, speichert er Anfragen für Schlüsselbereiche zwischen.

Der gRPC-Proxy unterstützt mehrere etcd-Serverendpunkte. Beim Start wählt er zufällig einen davon aus. Dieser Endpunkt bedient alle Anfragen, bis der Proxy einen Endpunktausfall erkennt. Dann wechselt der gRPC-Proxy zu einem anderen Endpunkt, sofern verfügbar, um Ausfälle vor seinen Clients zu verbergen. Weitere Wiederholungsstrategien, etwa gewichtetes Round-Robin, können künftig unterstützt werden.

## Skalierbare Watch-API {#scalable-watch-api}

Der gRPC-Proxy führt mehrere Client-Watcher (`c-watchers`) für denselben Schlüssel oder Bereich zu einem einzelnen Watcher (`s-watcher`) zusammen, der mit einem etcd-Server verbunden ist. Der Proxy verteilt alle Ereignisse des `s-watcher` an seine `c-watchers`.

Wenn N Clients denselben Schlüssel beobachten, kann ein gRPC-Proxy die Watch-Last auf dem etcd-Server von N auf 1 reduzieren. Durch den Einsatz mehrerer gRPC-Proxys lässt sich die Serverlast weiter verteilen.

Im folgenden Beispiel beobachten drei Clients den Schlüssel A. Der gRPC-Proxy führt die drei Watcher zusammen und erstellt einen einzelnen Watcher am etcd-Server.

```
            +-------------+
            | etcd server |
            +------+------+
                   ^ watch key A (s-watcher)
                   |
           +-------+-----+
           | gRPC proxy  | <-------+
           |             |         |
           ++-----+------+         |watch key A (c-watcher)
watch key A ^     ^ watch key A    |
(c-watcher) |     | (c-watcher)    |
    +-------+-+  ++--------+  +----+----+
    |  client |  |  client |  |  client |
    |         |  |         |  |         |
    +---------+  +---------+  +---------+
```

### Einschränkungen {#limitations}

Um mehrere Client-Watcher effizient zu einem einzelnen Watcher zusammenzuführen, ordnet der gRPC-Proxy neue `c-watchers` nach Möglichkeit einem vorhandenen `s-watcher` zu. Dieser gemeinsame `s-watcher` kann wegen Netzwerkverzögerungen oder gepufferter, noch nicht zugestellter Ereignisse hinter dem etcd-Server zurückliegen. Ist keine Watch-Revision angegeben, garantiert der gRPC-Proxy nicht, dass der `c-watcher` bei der neuesten Revision des Speichers zu beobachten beginnt. Beobachtet ein Client beispielsweise direkt über einen etcd-Server mit Revision 1000, beginnt dieser Watcher bei Revision 1000. Bei einem Watch über den gRPC-Proxy kann der Client hingegen bereits bei Revision 990 beginnen.

Ähnliche Einschränkungen gelten für den Abbruch. Beim Abbrechen eines Watchers kann die Revision des etcd-Servers höher sein als die Revision in der Abbruchantwort.

Diese beiden Einschränkungen sollten in den meisten Anwendungsfällen keine Probleme verursachen. Künftig kann es zusätzliche Optionen geben, die den Watcher zwingen, den gRPC-Proxy zu umgehen, um genauere Revisionen in Antworten zu erhalten.

## Skalierbare Lease-API {#scalable-lease-api}

Um seine Leases aufrechtzuerhalten, muss ein Client mindestens einen gRPC-Stream zu einem etcd-Server aufbauen und darüber regelmäßig Heartbeats senden. Bei einer etcd-Arbeitslast mit umfangreicher Lease-Aktivität über viele Clients hinweg können diese Streams zu einer übermäßigen CPU-Auslastung beitragen. Um die Gesamtzahl der Streams auf dem zentralen Cluster zu verringern, unterstützt der Proxy die Zusammenführung von Lease-Streams.

Wenn N Clients Leases aktualisieren, reduziert ein einzelner gRPC-Proxy die Stream-Last auf dem etcd-Server von N auf 1. Zusätzliche gRPC-Proxys können die Streams weiter auf mehrere Proxys verteilen.

Im folgenden Beispiel aktualisieren drei Clients drei unabhängige Leases (`L1`, `L2` und `L3`). Der gRPC-Proxy führt die drei Lease-Streams der Clients (`c-streams`) zu einem einzelnen Stream zur Aufrechterhaltung von Leases (`s-stream`) zusammen, der mit einem etcd-Server verbunden ist. Der Proxy leitet die clientseitigen Lease-Heartbeats von den c-streams an den s-stream weiter und sendet die Antworten anschließend an die jeweiligen c-streams zurück.

```
          +-------------+
          | etcd server |
          +------+------+
                 ^
                 | heartbeat L1, L2, L3
                 | (s-stream)
                 v
         +-------+-----+
         | gRPC proxy  +<-----------+
         +---+------+--+            | heartbeat L3
             ^      ^               | (c-stream)
heartbeat L1 |      | heartbeat L2  |
(c-stream)   v      v (c-stream)    v
      +------+-+  +-+------+  +-----+--+
      | client |  | client |  | client |
      +--------+  +--------+  +--------+
```

## Schutz vor missbräuchlich arbeitenden Clients {#abusive-clients-protection}

Der gRPC-Proxy speichert Antworten auf Anfragen zwischen, sofern dies keine Konsistenzanforderungen verletzt. Dadurch kann er den etcd-Server vor missbräuchlich arbeitenden Clients schützen, die Anfragen in engen for-Schleifen senden.

## Den etcd-gRPC-Proxy starten {#start-etcd-grpc-proxy}

Als Beispiel dient ein etcd-Cluster mit folgenden statischen Endpunkten:

|Name|Adresse|Hostname|
|------|---------|------------------|
|infra0|10.0.1.10|infra0.example.com|
|infra1|10.0.1.11|infra1.example.com|
|infra2|10.0.1.12|infra2.example.com|

Den etcd-gRPC-Proxy mit folgendem Befehl für diese statischen Endpunkte starten:

```bash
$ etcd grpc-proxy start --endpoints=infra0.example.com,infra1.example.com,infra2.example.com --listen-addr=127.0.0.1:2379
```

Der etcd-gRPC-Proxy startet und lauscht auf Port 2379. Er leitet Clientanfragen an einen der drei oben angegebenen Endpunkte weiter.

Anfragen über den Proxy senden:

```bash
$ ETCDCTL_API=3 etcdctl --endpoints=127.0.0.1:2379 put foo bar
OK
$ ETCDCTL_API=3 etcdctl --endpoints=127.0.0.1:2379 get foo
foo
bar
```

## Synchronisierung der Clientendpunkte und Namensauflösung {#client-endpoint-synchronization-and-name-resolution}

Der Proxy kann seine Endpunkte zur Diensterkennung registrieren, indem er an einen benutzerdefinierten Endpunkt schreibt. Dies dient zwei Zwecken. Erstens können Clients ihre Endpunkte mit einer Menge von Proxyendpunkten synchronisieren, um Hochverfügbarkeit zu erreichen. Zweitens stellt dies Endpunkte für die [gRPC-Namensauflösung](/de/etcd/dev-guide/grpc_naming/) von etcd bereit.

Proxys durch Angabe eines benutzerdefinierten Präfixes registrieren:

```bash
$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23790 \
  --advertise-client-url=127.0.0.1:23790 \
  --resolver-prefix="___grpc_proxy_endpoint" \
  --resolver-ttl=60

$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23791 \
  --advertise-client-url=127.0.0.1:23791 \
  --resolver-prefix="___grpc_proxy_endpoint" \
  --resolver-ttl=60
```

Der Proxy führt bei der Abfrage der Mitgliederliste alle seine Mitglieder auf:

```bash
ETCDCTL_API=3 etcdctl --endpoints=http://localhost:23790 member list --write-out table

+----+---------+--------------------------------+------------+-----------------+
| ID | STATUS  |              NAME              | PEER ADDRS |  CLIENT ADDRS   |
+----+---------+--------------------------------+------------+-----------------+
|  0 | started | Gyu-Hos-MBP.sfo.coreos.systems |            | 127.0.0.1:23791 |
|  0 | started | Gyu-Hos-MBP.sfo.coreos.systems |            | 127.0.0.1:23790 |
+----+---------+--------------------------------+------------+-----------------+
```

Dadurch können Clients Proxyendpunkte automatisch über Sync erkennen:

```go
cli, err := clientv3.New(clientv3.Config{
    Endpoints: []string{"http://localhost:23790"},
})
if err != nil {
    log.Fatal(err)
}
defer cli.Close()

// fetch registered grpc-proxy endpoints
if err := cli.Sync(context.Background()); err != nil {
    log.Fatal(err)
}
```

Wird ein Proxy ohne Resolver-Präfix konfiguriert,

```bash
$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23792 \
  --advertise-client-url=127.0.0.1:23792
```

gibt die Mitgliederlisten-API des grpc-proxy dessen eigene `advertise-client-url` zurück:

```bash
ETCDCTL_API=3 etcdctl --endpoints=http://localhost:23792 member list --write-out table

+----+---------+--------------------------------+------------+-----------------+
| ID | STATUS  |              NAME              | PEER ADDRS |  CLIENT ADDRS   |
+----+---------+--------------------------------+------------+-----------------+
|  0 | started | Gyu-Hos-MBP.sfo.coreos.systems |            | 127.0.0.1:23792 |
+----+---------+--------------------------------+------------+-----------------+
```

## Namensräume {#namespacing}

Angenommen, eine Anwendung erwartet die volle Kontrolle über den gesamten Schlüsselraum, der etcd-Cluster wird aber mit anderen Anwendungen geteilt. Damit alle Anwendungen ohne gegenseitige Beeinträchtigung laufen können, kann der Proxy den etcd-Schlüsselraum so aufteilen, dass Clients scheinbar auf den vollständigen Schlüsselraum zugreifen. Wird dem Proxy die Option `--namespace` übergeben, werden alle eingehenden Clientanfragen so umgeschrieben, dass die Schlüssel ein benutzerdefiniertes Präfix erhalten. Zugriffe auf den etcd-Cluster erfolgen unter diesem Präfix; der Proxy entfernt es aus den Antworten. Für den Client wirkt es, als gäbe es überhaupt kein Präfix.

Um einen Namensraum für einen Proxy festzulegen, ihn mit `--namespace` starten:

```bash
$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23790 \
  --namespace=my-prefix/
```

Bei Zugriffen auf den Proxy wird nun im etcd-Cluster transparent das Präfix vorangestellt:

```bash
$ ETCDCTL_API=3 etcdctl --endpoints=localhost:23790 put my-key abc
# OK
$ ETCDCTL_API=3 etcdctl --endpoints=localhost:23790 get my-key
# my-key
# abc
$ ETCDCTL_API=3 etcdctl --endpoints=localhost:2379 get my-prefix/my-key
# my-prefix/my-key
# abc
```

## TLS-Terminierung {#tls-termination}

Der gRPC-Proxy kann TLS zu einem abgesicherten etcd-Cluster terminieren und dafür einen unverschlüsselten lokalen Endpunkt bereitstellen.

Zum Ausprobieren einen Ein-Mitglied-Cluster von etcd mit HTTPS für Clients starten:

```sh
$ etcd --listen-client-urls https://localhost:2379 --advertise-client-urls https://localhost:2379 --cert-file=peer.crt --key-file=peer.key --trusted-ca-file=ca.crt --client-cert-auth
```

Prüfen, ob der Clientport HTTPS bereitstellt:

```sh
# fails
$ ETCDCTL_API=3 etcdctl --endpoints=http://localhost:2379 endpoint status
# works
$ ETCDCTL_API=3 etcdctl --endpoints=https://localhost:2379 --cert=client.crt --key=client.key --cacert=ca.crt endpoint status
```

Anschließend einen gRPC-Proxy auf `localhost:12379` starten, der sich mithilfe der Clientzertifikate mit dem etcd-Endpunkt `https://localhost:2379` verbindet:

```sh
$ etcd grpc-proxy start --endpoints=https://localhost:2379 --listen-addr localhost:12379 --cert client.crt --key client.key --cacert=ca.crt --insecure-skip-tls-verify &
```

Abschließend die TLS-Terminierung testen, indem über HTTP ein Schlüssel in den Proxy geschrieben wird:

```sh
$ ETCDCTL_API=3 etcdctl --endpoints=http://localhost:12379 put abc def
# OK
```

## Metriken und Zustandsprüfung {#metrics-and-health}

Der gRPC-Proxy stellt für die durch `--endpoints` definierten etcd-Mitglieder die Endpunkte `/health` und Prometheus `/metrics` bereit. Alternativ lässt sich mit der Option `--metrics-addr` eine zusätzliche URL definieren, die sowohl auf `/metrics` als auch auf `/health` antwortet.

```bash
$ etcd grpc-proxy start \
  --endpoints https://localhost:2379 \
  --metrics-addr https://0.0.0.0:4443 \
  --listen-addr 127.0.0.1:23790 \
  --key client.key \
  --key-file proxy-server.key \
  --cert client.crt \
  --cert-file proxy-server.crt \
  --cacert ca.pem \
  --trusted-ca-file proxy-ca.pem
 ```

### Bekanntes Problem {#known-issue}

Die Hauptschnittstelle des Proxys bedient sowohl HTTP2 als auch HTTP/1.1. Ist der Proxy wie im obigen Beispiel mit TLS eingerichtet, muss bei Anfragen eines Clients wie cURL an die lauschende Schnittstelle ausdrücklich HTTP/1.1 als Protokoll eingestellt werden, damit `/metrics` oder `/health` zurückgegeben werden. Die mit `--metrics-addr` eingerichtete zweite Schnittstelle hat diese Anforderung nicht.

```bash
 $ curl --cacert proxy-ca.pem --key proxy-client.key --cert proxy-client.crt https://127.0.0.1:23790/metrics --http1.1
```
