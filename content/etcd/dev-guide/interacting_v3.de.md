---
title: Mit etcd arbeiten
weight: 3250
description: "etcdctl: ein Befehlszeilenwerkzeug zur Interaktion mit dem etcd-Server"
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/interacting_v3.md"
---

Benutzer arbeiten mit etcd meist, indem sie den Wert eines Schlüssels schreiben oder lesen. Dieser Abschnitt beschreibt dies anhand von etcdctl, einem Befehlszeilenwerkzeug zur Interaktion mit dem etcd-Server. Die erläuterten Konzepte sollten auch für die gRPC-APIs und die APIs der Client-Bibliotheken gelten.

etcdctl v3.7 verwendet die v3-API. Die v2-API und die Versionsauswahl über `ETCDCTL_API` wurden entfernt.

> [!NOTE]
> Die folgenden Beispiele enthalten historische Befehlsausgaben; die angezeigten Versionsnummern können daher von Ihrer Installation abweichen. Frühere etcd-Versionen hielten v2- und v3-Schlüssel in getrennten Speichern. Migrieren Sie vorhandene v2-Daten vor dem Upgrade auf v3.7.

## Versionen ermitteln {#find-versions}

Die etcdctl-Version und die API-Version des Servers helfen dabei, die passenden Befehle für verschiedene etcd-Operationen zu bestimmen.

Mit folgendem Befehl lassen sich die Versionen ermitteln:

```bash
$ etcdctl version
etcdctl version: 3.1.0-alpha.0+git
API version: 3.1
```

## Einen Schlüssel schreiben {#write-a-key}

Anwendungen speichern Schlüssel im etcd-Cluster, indem sie Werte unter diesen Schlüsseln schreiben. Jeder gespeicherte Schlüssel wird über das Raft-Protokoll auf alle Mitglieder des etcd-Clusters repliziert, um Konsistenz und Zuverlässigkeit zu gewährleisten.

Mit folgendem Befehl wird der Wert des Schlüssels `foo` auf `bar` gesetzt:

```bash
$ etcdctl put foo bar
OK
```

Ein Schlüssel kann durch Zuordnen einer Lease auch für einen festgelegten Zeitraum gesetzt werden.

Mit folgendem Befehl wird der Wert des Schlüssels `foo1` für 10s auf `bar1` gesetzt.

```bash
$ etcdctl put foo1 bar1 --lease=1234abcd
OK
```

> [!NOTE]
> Die Lease-ID `1234abcd` im obigen Befehl ist die ID, die beim Erstellen der Lease mit 10s Laufzeit zurückgegeben wird. Diese ID kann anschließend dem Schlüssel zugeordnet werden.

## Schlüssel lesen {#read-keys}

Anwendungen können Schlüsselwerte aus einem etcd-Cluster lesen. Abfragen können einen einzelnen Schlüssel oder einen Schlüsselbereich lesen.

Angenommen, im etcd-Cluster sind folgende Schlüssel gespeichert:

```bash
foo = bar
foo1 = bar1
foo2 = bar2
foo3 = bar3
```

Mit folgendem Befehl wird der Wert des Schlüssels `foo` gelesen:

```bash
$ etcdctl get foo
foo
bar
```

Mit folgendem Befehl wird der Wert des Schlüssels `foo` im Hexadezimalformat gelesen:

```bash
$ etcdctl get foo --hex
\x66\x6f\x6f          # Key
\x62\x61\x72          # Value
```

Mit folgendem Befehl wird nur der Wert des Schlüssels `foo` gelesen:

```bash
$ etcdctl get foo --print-value-only
bar
```

Mit folgendem Befehl werden die Schlüssel von `foo` bis `foo3` abgefragt:

```bash
$ etcdctl get foo foo3
foo
bar
foo1
bar1
foo2
bar2
```

> [!NOTE]
> `foo3` ist ausgeschlossen, da der Bereich dem halboffenen Intervall `[foo, foo3)` entspricht, das `foo3` nicht enthält.

Mit folgendem Befehl werden alle Schlüssel mit dem Präfix `foo` abgefragt:

```bash
$ etcdctl get --prefix foo
foo
bar
foo1
bar1
foo2
bar2
foo3
bar3
```

Mit folgendem Befehl werden alle Schlüssel mit dem Präfix `foo` abgefragt und die Ergebnisse auf 2 begrenzt:

```bash
$ etcdctl get --prefix --limit=2 foo
foo
bar
foo1
bar1
```

Mit folgendem Befehl werden alle Schlüssel mit dem Präfix `foo` über den RPC [`RangeStream`](/de/etcd/learning/api/#rangestream) abgefragt. Das Ergebnis ist mit dem eines unären `Range`-Aufrufs identisch:

```bash
$ etcdctl get --stream --prefix foo
foo
bar
foo1
bar1
foo2
bar2
foo3
bar3
```

`--stream` unterstützt weder `--order` noch `--sort-by` noch Revisionsfilter.

## Frühere Schlüsselversionen lesen {#read-past-version-of-keys}

Anwendungen möchten möglicherweise ersetzte Versionen eines Schlüssels lesen. Beispielsweise kann eine Anwendung durch Zugriff auf eine frühere Schlüsselversion zu einer alten Konfiguration zurückkehren. Oder sie kann durch den Schlüsselverlauf über mehrere Anfragen hinweg eine konsistente Sicht auf mehrere Schlüssel erhalten.
Da jede Änderung am Schlüssel-Wert-Speicher des etcd-Clusters dessen globale Revision erhöht, kann eine Anwendung ersetzte Schlüssel durch Angabe einer älteren etcd-Revision lesen.

Angenommen, im etcd-Cluster sind bereits folgende Schlüssel gespeichert:

```bash
foo = bar         # revision = 2
foo1 = bar1       # revision = 3
foo = bar_new     # revision = 4
foo1 = bar1_new   # revision = 5
```

Das folgende Beispiel zeigt den Zugriff auf frühere Schlüsselversionen:

```bash
$ etcdctl get --prefix foo # access the most recent versions of keys
foo
bar_new
foo1
bar1_new

$ etcdctl get --prefix --rev=4 foo # access the versions of keys at revision 4
foo
bar_new
foo1
bar1

$ etcdctl get --prefix --rev=3 foo # access the versions of keys at revision 3
foo
bar
foo1
bar1

$ etcdctl get --prefix --rev=2 foo # access the versions of keys at revision 2
foo
bar

$ etcdctl get --prefix --rev=1 foo # access the versions of keys at revision 1
```

## Schlüssel lesen, deren Bytewert größer oder gleich dem angegebenen Schlüssel ist {#read-keys-which-are-greater-than-or-equal-to-the-byte-value-of-the-specified-key}

Anwendungen möchten möglicherweise Schlüssel lesen, deren Bytewert größer oder gleich dem des angegebenen Schlüssels ist.

Angenommen, im etcd-Cluster sind bereits folgende Schlüssel gespeichert:

```bash
a = 123
b = 456
z = 789
```

Mit folgendem Befehl werden Schlüssel gelesen, deren Bytewert größer oder gleich dem des Schlüssels `b` ist:

```bash
$ etcdctl get --from-key b
b
456
z
789
```

## Schlüssel löschen {#delete-keys}

Anwendungen können einen einzelnen Schlüssel oder einen Schlüsselbereich aus einem etcd-Cluster löschen.

Angenommen, im etcd-Cluster sind bereits folgende Schlüssel gespeichert:

```bash
foo = bar
foo1 = bar1
foo3 = bar3
zoo = val
zoo1 = val1
zoo2 = val2
a = 123
b = 456
z = 789
```

Mit folgendem Befehl wird der Schlüssel `foo` gelöscht:

```bash
$ etcdctl del foo
1 # one key is deleted
```

Mit folgendem Befehl werden die Schlüssel von `foo` bis `foo9` gelöscht:

```bash
$ etcdctl del foo foo9
2 # two keys are deleted
```

Mit folgendem Befehl wird der Schlüssel `zoo` gelöscht und das gelöschte Schlüssel-Wert-Paar zurückgegeben:

```bash
$ etcdctl del --prev-kv zoo
1   # one key is deleted
zoo # deleted key
val # the value of the deleted key
```

Mit folgendem Befehl werden Schlüssel mit dem Präfix `zoo` gelöscht:

```bash
$ etcdctl del --prefix zoo
2 # two keys are deleted
```

Mit folgendem Befehl werden Schlüssel gelöscht, deren Bytewert größer oder gleich dem des Schlüssels `b` ist:

```bash
$ etcdctl del --from-key b
2 # two keys are deleted
```

## Schlüsseländerungen beobachten {#watch-key-changes}

Anwendungen können einen Schlüssel oder einen Schlüsselbereich beobachten, um sämtliche Aktualisierungen zu überwachen.

Mit folgendem Befehl wird der Schlüssel `foo` beobachtet:

```bash
$ etcdctl watch foo
# in another terminal: etcdctl put foo bar
PUT
foo
bar
```

Mit folgendem Befehl wird der Schlüssel `foo` im Hexadezimalformat beobachtet:

```bash
$ etcdctl watch foo --hex
# in another terminal: etcdctl put foo bar
PUT
\x66\x6f\x6f          # Key
\x62\x61\x72          # Value
```

Mit folgendem Befehl wird der Schlüsselbereich von `foo` bis `foo9` beobachtet:

```bash
$ etcdctl watch foo foo9
# in another terminal: etcdctl put foo bar
PUT
foo
bar
# in another terminal: etcdctl put foo1 bar1
PUT
foo1
bar1
```

Mit folgendem Befehl werden Schlüssel mit dem Präfix `foo` beobachtet:

```bash
$ etcdctl watch --prefix foo
# in another terminal: etcdctl put foo bar
PUT
foo
bar
# in another terminal: etcdctl put fooz1 barz1
PUT
fooz1
barz1
```

Mit folgendem Befehl werden die beiden Schlüssel `foo` und `zoo` beobachtet:

```bash
$ etcdctl watch -i
$ watch foo
$ watch zoo
# in another terminal: etcdctl put foo bar
PUT
foo
bar
# in another terminal: etcdctl put zoo val
PUT
zoo
val
```

## Historische Schlüsseländerungen beobachten {#watch-historical-changes-of-keys}

Anwendungen möchten möglicherweise historische Änderungen an Schlüsseln in etcd beobachten. Beispielsweise kann eine Anwendung alle Änderungen eines Schlüssels empfangen wollen. Solange sie mit etcd verbunden bleibt, genügt dafür `watch`. Fällt jedoch die Anwendung oder etcd aus, kann während des Ausfalls eine Änderung auftreten, die die Anwendung nicht in Echtzeit empfängt. Um die Zustellung der Aktualisierung zu garantieren, muss die Anwendung historische Schlüsseländerungen beobachten können. Dazu kann sie wie beim Lesen früherer Schlüsselversionen eine historische Revision für einen Watch angeben.

Angenommen, die folgende Folge von Operationen wurde ausgeführt:

```bash
$ etcdctl put foo bar         # revision = 2
OK
$ etcdctl put foo1 bar1       # revision = 3
OK
$ etcdctl put foo bar_new     # revision = 4
OK
$ etcdctl put foo1 bar1_new   # revision = 5
OK
```

Das folgende Beispiel zeigt die Beobachtung historischer Änderungen:

```bash
# watch for changes on key `foo` since revision 2
$ etcdctl watch --rev=2 foo
PUT
foo
bar
PUT
foo
bar_new
```

```bash
# watch for changes on key `foo` since revision 3
$ etcdctl watch --rev=3 foo
PUT
foo
bar_new
```

Das folgende Beispiel beobachtet erst ab der letzten historischen Änderung:

```bash
# watch for changes on key `foo` and return last revision value along with modified value
$ etcdctl watch --prev-kv foo
# in another terminal: etcdctl put foo bar_latest
PUT
foo         # key
bar_new     # last value of foo key before modification
foo         # key
bar_latest  # value of foo key after modification
```

## Watch-Fortschritt {#watch-progress}

Anwendungen möchten möglicherweise den Fortschritt eines Watches prüfen, um die Aktualität seines Streams zu bestimmen. Wird ein Watch beispielsweise zur Aktualisierung eines Caches verwendet, kann es hilfreich sein zu wissen, ob der Cache gegenüber der Revision eines Quorum-Lesezugriffs veraltet ist.

In einer interaktiven Watch-Sitzung kann mit dem Befehl "progress" eine Fortschrittsanfrage gestellt werden. Sie fordert den etcd-Server auf, eine Fortschrittsbenachrichtigung im Watch-Stream zu senden:

```bash
$ etcdctl watch -i
$ watch a
$ progress
progress notify: 1
# in another terminal: etcdctl put x 0
# in another terminal: etcdctl put y 1
$ progress
progress notify: 3
```

> [!NOTE]
> Die Revisionsnummer in der Fortschrittsantwort stammt vom lokalen etcd-Serverknoten, mit dem der Watch-Stream verbunden ist. Ist dieser Knoten durch eine Netzwerkpartition abgetrennt und nicht Teil des Quorums, kann diese Revision niedriger sein als die Revision eines Quorum-Lesezugriffs auf einen nicht abgetrennten etcd-Serverknoten.

## Kompaktierte Revisionen {#compacted-revisions}

Wie erwähnt, bewahrt etcd Revisionen auf, damit Anwendungen frühere Schlüsselversionen lesen können. Damit sich jedoch kein unbegrenzt großer Verlauf ansammelt, ist es wichtig, frühere Revisionen zu kompaktieren. Nach der Kompaktierung entfernt etcd historische Revisionen und gibt Ressourcen für die spätere Nutzung frei. Alle ersetzten Daten mit Revisionen vor der Kompaktierungsrevision sind dann nicht mehr verfügbar.

Mit folgendem Befehl werden die Revisionen kompaktiert:

```bash
$ etcdctl compact 5
compacted revision 5

# any revisions before the compacted one are not accessible
$ etcdctl get --rev=4 foo
Error:  rpc error: code = 11 desc = etcdserver: mvcc: required revision has been compacted
```

> [!NOTE]
> Die aktuelle Revision des etcd-Servers lässt sich mit einem get-Befehl im JSON-Format für einen beliebigen vorhandenen oder nicht vorhandenen Schlüssel ermitteln. Das folgende Beispiel verwendet mykey, das im etcd-Server nicht existiert:

```bash
$ etcdctl get mykey -w=json
{"header":{"cluster_id":14841639068965178418,"member_id":10276657743932975437,"revision":15,"raft_term":4}}
```

## Leases gewähren {#grant-leases}

Anwendungen können vom etcd-Cluster Leases für Schlüssel anfordern. Wird ein Schlüssel einer Lease zugeordnet, ist seine Lebensdauer an die der Lease gebunden, die ihrerseits durch eine Time-to-live (TTL) bestimmt wird. Jede Lease hat eine Mindest-TTL, die die Anwendung bei der Anforderung angibt. Ihre tatsächliche TTL ist mindestens so groß wie die Mindest-TTL und wird vom etcd-Cluster gewählt. Sobald sie verstrichen ist, läuft die Lease ab, und alle zugeordneten Schlüssel werden gelöscht.

Mit folgendem Befehl wird eine Lease gewährt:

```bash
# grant a lease with 60 second TTL
$ etcdctl lease grant 60
lease 32695410dcc0ca06 granted with TTL(60s)

# attach key foo to lease 32695410dcc0ca06
$ etcdctl put --lease=32695410dcc0ca06 foo bar
OK
```

## Leases widerrufen {#revoke-leases}

Anwendungen widerrufen Leases anhand ihrer Lease-ID. Dabei werden alle der Lease zugeordneten Schlüssel gelöscht.

Angenommen, die folgende Folge von Operationen wurde ausgeführt:

```bash
$ etcdctl lease grant 60
lease 32695410dcc0ca06 granted with TTL(60s)
$ etcdctl put --lease=32695410dcc0ca06 foo bar
OK
```

Mit folgendem Befehl wird dieselbe Lease widerrufen:

```bash
$ etcdctl lease revoke 32695410dcc0ca06
lease 32695410dcc0ca06 revoked

$ etcdctl get foo
# empty response since foo is deleted due to lease revocation
```

## Leases am Leben halten {#keep-leases-alive}

Anwendungen können eine Lease am Leben halten, indem sie deren TTL erneuern und so ihren Ablauf verhindern.

Angenommen, die folgende Folge von Operationen wurde ausgeführt:

```bash
$ etcdctl lease grant 60
lease 32695410dcc0ca06 granted with TTL(60s)
```

Mit folgendem Befehl wird dieselbe Lease am Leben gehalten:

```bash
$ etcdctl lease keep-alive 32695410dcc0ca06
lease 32695410dcc0ca06 keepalived with TTL(60)
lease 32695410dcc0ca06 keepalived with TTL(60)
lease 32695410dcc0ca06 keepalived with TTL(60)
...
```

## Lease-Informationen abrufen {#get-lease-information}

Anwendungen möchten möglicherweise Informationen über Leases abrufen, um sie zu erneuern oder zu prüfen, ob eine Lease noch existiert oder bereits abgelaufen ist. Sie möchten möglicherweise auch wissen, welchen Schlüsseln eine bestimmte Lease zugeordnet ist.

Angenommen, die folgende Folge von Operationen wurde ausgeführt:

```bash
# grant a lease with 500 second TTL
$ etcdctl lease grant 500
lease 694d5765fc71500b granted with TTL(500s)

# attach key zoo1 to lease 694d5765fc71500b
$ etcdctl put zoo1 val1 --lease=694d5765fc71500b
OK

# attach key zoo2 to lease 694d5765fc71500b
$ etcdctl put zoo2 val2 --lease=694d5765fc71500b
OK
```

Mit folgendem Befehl werden Informationen zur Lease abgerufen:

```bash
$ etcdctl lease timetolive 694d5765fc71500b
lease 694d5765fc71500b granted with TTL(500s), remaining(258s)
```

Mit folgendem Befehl werden Informationen zur Lease einschließlich der ihr zugeordneten Schlüssel abgerufen:

```bash
$ etcdctl lease timetolive --keys 694d5765fc71500b
lease 694d5765fc71500b granted with TTL(500s), remaining(132s), attached keys([zoo2 zoo1])

# if the lease has expired or does not exist it will give the below response:
Error:  etcdserver: requested lease not found
```
