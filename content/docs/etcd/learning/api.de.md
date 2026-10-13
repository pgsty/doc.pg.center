---
title: etcd-API
weight: 2625
description: Überblick über den grundlegenden Entwurf der etcd-API
categories: [Konzept]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/api.md"
aliases: [/etcd/learning/api/]
---

Dieses Dokument gibt einen Überblick über den grundlegenden Entwurf der etcd-v3-APIs.
Diese sind nicht mit der etcd-v2-API zu verwechseln, die seit etcd v3.5 veraltet ist.
Der Überblick ist keineswegs vollständig. Er konzentriert sich auf die Grundideen, die zum Verständnis von etcd nötig sind, ohne durch seltenere API-Aufrufe abzulenken.
Alle etcd-APIs sind in [gRPC-Diensten][grpc-service] definiert, die die vom etcd-Server verstandenen Remote Procedure Calls (RPCs) nach Funktionen gliedern.
Eine vollständige Liste aller etcd-RPCs ist in Markdown in der [gRPC-API-Übersicht][grpc-api] dokumentiert.

## gRPC-Dienste {#grpc-services}

Jede API-Anfrage an einen etcd-Server ist ein gRPC-Remote-Procedure-Call. Die RPCs von etcd werden nach ihrer Funktion in Dienste eingeteilt.

Für die Arbeit mit dem Schlüsselraum von etcd sind folgende Dienste wichtig:
* KV - Erstellt, aktualisiert, liest und löscht Schlüssel-Wert-Paare.
* Watch - Überwacht Änderungen an Schlüsseln.
* Lease - Grundoperationen zum Verarbeiten von Keepalive-Nachrichten der Clients.

Den Cluster selbst verwalten folgende Dienste:
* Auth - Rollenbasierter Authentifizierungsmechanismus zur Authentifizierung von Benutzern.
* Cluster - Liefert Mitgliedschaftsinformationen und Konfigurationsfunktionen.
* Maintenance - Erstellt Snapshots für die Wiederherstellung, defragmentiert den Speicher und liefert Statusinformationen pro Mitglied.

### Anfragen und Antworten {#requests-and-responses}

Alle RPCs in etcd folgen demselben Format. Jeder RPC hat eine Funktion `Name`, die `NameRequest` als Argument entgegennimmt und `NameResponse` als Antwort zurückgibt. Beispielsweise lautet die Beschreibung des RPC `Range`:

```protobuf
service KV {
  Range(RangeRequest) returns (RangeResponse)
  ...
}
```

### Antwortheader {#response-header}

Alle Antworten der etcd-API enthalten einen Antwortheader mit Clustermetadaten zur Antwort:

```proto
message ResponseHeader {
  uint64 cluster_id = 1;
  uint64 member_id = 2;
  int64 revision = 3;
  uint64 raft_term = 4;
}
```

* Cluster_ID - Die ID des Clusters, der die Antwort erzeugt.
* Member_ID - Die ID des Mitglieds, das die Antwort erzeugt.
* Revision - Die Revision des Schlüssel-Wert-Speichers beim Erzeugen der Antwort.
* Raft_Term - Der Raft-Term des Mitglieds beim Erzeugen der Antwort.

Eine Anwendung kann das Feld `Cluster_ID` oder `Member_ID` lesen, um sicherzustellen, dass sie mit dem beabsichtigten Cluster beziehungsweise Mitglied kommuniziert.

Anwendungen können über das Feld `Revision` die neueste Revision des Schlüssel-Wert-Speichers ermitteln. Das ist besonders nützlich, wenn sie eine historische Revision für eine `Zeitreiseabfrage` angeben und die zum Anfragezeitpunkt neueste Revision kennen möchten.

Mit `Raft_Term` können Anwendungen erkennen, wann der Cluster eine neue Leader-Wahl abgeschlossen hat.

## Schlüssel-Wert-API {#key-value-api}

Die Schlüssel-Wert-API bearbeitet die in etcd gespeicherten Schlüssel-Wert-Paare. Der Großteil der Anfragen an etcd sind üblicherweise Schlüssel-Wert-Anfragen.

### Grundoperationen des Systems {#system-primitives}

### Schlüssel-Wert-Paar {#key-value-pair}

Ein Schlüssel-Wert-Paar ist die kleinste Einheit, die die Schlüssel-Wert-API bearbeiten kann. Jedes Paar hat mehrere Felder, die im [Protobuf-Format][kv-proto] definiert sind:

```protobuf
message KeyValue {
  bytes key = 1;
  int64 create_revision = 2;
  int64 mod_revision = 3;
  int64 version = 4;
  bytes value = 5;
  int64 lease = 6;
}
```

* Key - Schlüssel als Bytes. Ein leerer Schlüssel ist nicht zulässig.
* Value - Wert als Bytes.
* Version - Version ist die Version des Schlüssels. Eine Löschung setzt sie auf null zurück, und jede Änderung des Schlüssels erhöht sie.
* Create_Revision - Revision der letzten Erstellung des Schlüssels.
* Mod_Revision - Revision der letzten Änderung des Schlüssels.
* Lease - Die ID der dem Schlüssel zugeordneten Lease. Ist lease 0, ist dem Schlüssel keine Lease zugeordnet.


Zusätzlich zu Schlüssel und Wert fügt etcd der Schlüsselnachricht Revisionsmetadaten hinzu. Diese Informationen ordnen Schlüssel nach Erstellungs- und Änderungszeitpunkt, was für die Nebenläufigkeitskontrolle bei verteilter Synchronisierung nützlich ist. Die [verteilten gemeinsamen Sperren][locks] des etcd-Clients verwenden die Erstellungsrevision, um auf den Besitz einer Sperre zu warten. Entsprechend dient die Änderungsrevision dazu, Konflikte in der Lesemenge von [Software Transactional Memory][STM] zu erkennen und auf Aktualisierungen bei der [Leader-Wahl][elections] zu warten.

#### Revisionen {#revisions}

etcd verwaltet einen clusterweiten 64-Bit-Zähler, die Speicherrevision, der bei jeder Änderung des Schlüsselraums erhöht wird. Die Revision dient als globale logische Uhr und ordnet alle Speicheraktualisierungen sequenziell. Die durch eine neue Revision repräsentierte Änderung ist inkrementell: Einer Revision sind die Daten zugeordnet, die den Speicher geändert haben. Intern bedeutet eine neue Revision, die Änderungen mit der erhöhten Revision als Schlüssel in den B+-Baum des Backends zu schreiben.

Besonders nützlich sind Revisionen im Backend mit [Mehrversions-Nebenläufigkeitskontrolle][mvcc] von etcd. Das MVCC-Modell erlaubt eine Sicht auf den Schlüssel-Wert-Speicher aus früheren Revisionen, da historische Schlüsselrevisionen erhalten bleiben. Clusteradministratoren können die Aufbewahrungsrichtlinie für diesen Verlauf zur gezielten Speicherverwaltung konfigurieren. Üblicherweise verwirft etcd alte Schlüsselrevisionen zeitgesteuert. Ein typischer etcd-Cluster bewahrt ersetzte Schlüsseldaten mehrere Stunden auf. Das ermöglicht auch die zuverlässige Behandlung langer Client-Verbindungsunterbrechungen statt nur kurzer Netzwerkausfälle: Watcher setzen einfach ab der letzten beobachteten historischen Revision fort. Ebenso können Leseanfragen mit einer Revision versehen werden, um Schlüssel aus der Sicht des Schlüsselraums zu dem Zeitpunkt zurückzugeben, an dem diese Revision bestätigt wurde.

#### Schlüsselbereiche {#key-ranges}

Das Datenmodell von etcd indiziert alle Schlüssel in einem flachen binären Schlüsselraum. Es unterscheidet sich damit von anderen Schlüssel-Wert-Speichern, die Schlüssel hierarchisch in Verzeichnissen organisieren. Schlüssel werden über Schlüsselintervalle `[a, b)` statt nach Verzeichnissen aufgelistet.

Diese Intervalle werden in etcd häufig als Bereiche bezeichnet. Bereichsoperationen sind leistungsfähiger als Verzeichnisoperationen. Wie ein hierarchischer Speicher unterstützen Intervalle einzelne Schlüsselabfragen über `[a, a+1)`, etwa ['a', 'a\x00') zum Abrufen von 'a', und Verzeichnisabfragen durch Kodierung der Schlüssel nach Verzeichnistiefe. Darüber hinaus können Intervalle auch Präfixe abbilden: Das Intervall `['a', 'b')` ruft beispielsweise alle Schlüssel mit dem Präfix 'a' ab.

Vereinbarungsgemäß werden Bereiche einer Anfrage durch die Felder `key` und `range_end` angegeben. Das Feld `key` ist der erste Schlüssel des Bereichs und sollte nicht leer sein. `range_end` ist der Schlüssel nach dem letzten Schlüssel des Bereichs. Ist `range_end` nicht angegeben oder leer, enthält der Bereich nur das Argument key. Ist `range_end` gleich `key` plus eins, etwa "aa"+1 == "ab" oder "a\xff"+1 == "b", umfasst der Bereich alle Schlüssel mit dem Präfix key. Sind `key` und `range_end` beide '\0', umfasst der Bereich alle Schlüssel. Ist `range_end` '\0', umfasst der Bereich alle Schlüssel größer oder gleich dem Argument key.

### Range {#range}

Schlüssel werden mit dem API-Aufruf `Range` aus dem Schlüssel-Wert-Speicher abgerufen. Er nimmt eine `RangeRequest` entgegen:

```protobuf
message RangeRequest {
  enum SortOrder {
	NONE = 0; // default, no sorting
	ASCEND = 1; // lowest target value first
	DESCEND = 2; // highest target value first
  }
  enum SortTarget {
	KEY = 0;
	VERSION = 1;
	CREATE = 2;
	MOD = 3;
	VALUE = 4;
  }

  bytes key = 1;
  bytes range_end = 2;
  int64 limit = 3;
  int64 revision = 4;
  SortOrder sort_order = 5;
  SortTarget sort_target = 6;
  bool serializable = 7;
  bool keys_only = 8;
  bool count_only = 9;
  int64 min_mod_revision = 10;
  int64 max_mod_revision = 11;
  int64 min_create_revision = 12;
  int64 max_create_revision = 13;
}
```

* Key, Range_End - Der abzurufende Schlüsselbereich.
* Limit - Die maximale Anzahl der für die Anfrage zurückgegebenen Schlüssel. Der Wert 0 bedeutet keine Begrenzung.
* Revision - Der für den Bereich zu verwendende Zeitpunkt im Schlüssel-Wert-Speicher. Ist revision kleiner oder gleich null, bezieht sich der Bereich auf den neuesten Stand. Wurde die Revision kompaktiert, wird ErrCompacted zurückgegeben.
* Sort_Order - Die Reihenfolge für sortierte Anfragen.
* Sort_Target - Das Schlüssel-Wert-Feld, nach dem sortiert wird.
* Serializable - Legt fest, dass die Bereichsanfrage serialisierbare, auf das Mitglied beschränkte Lesezugriffe verwendet. Standardmäßig ist Range linearisierbar und spiegelt den aktuellen Konsens des Clusters wider. Für bessere Leistung und Verfügbarkeit auf Kosten möglicherweise veralteter Leseergebnisse wird eine serialisierbare Bereichsanfrage lokal bearbeitet, ohne einen Konsens mit anderen Clusterknoten herstellen zu müssen.
* Keys_Only - Gibt nur die Schlüssel, nicht die Werte zurück.
* Count_Only - Gibt nur die Anzahl der Schlüssel im Bereich zurück.
* Min_Mod_Revision - Die Untergrenze für Änderungsrevisionen von Schlüsseln; kleinere Änderungsrevisionen werden herausgefiltert.
* Max_Mod_Revision - Die Obergrenze für Änderungsrevisionen von Schlüsseln; größere Änderungsrevisionen werden herausgefiltert.
* Min_Create_Revision - Die Untergrenze für Erstellungsrevisionen von Schlüsseln; kleinere Erstellungsrevisionen werden herausgefiltert.
* Max_Create_Revision - Die Obergrenze für Erstellungsrevisionen von Schlüsseln; größere Erstellungsrevisionen werden herausgefiltert.

Der Client erhält vom Aufruf `Range` eine Nachricht `RangeResponse`:

```protobuf
message RangeResponse {
  ResponseHeader header = 1;
  repeated mvccpb.KeyValue kvs = 2;
  bool more = 3;
  int64 count = 4;
}
```

* Kvs - Die Liste der Schlüssel-Wert-Paare, die der Bereichsanfrage entsprechen. Wenn `Count_Only` gesetzt ist, ist `Kvs` leer.
* More - Gibt bei gesetztem `limit` an, ob im angeforderten Bereich weitere Schlüssel zurückzugeben sind.
* Count - Die Gesamtzahl der Schlüssel, die die Bereichsanfrage erfüllen.

Für große Schlüsselbereiche, deren vollständige Antwort nicht zwischengespeichert werden soll, siehe [RangeStream](#rangestream).

### RangeStream {#rangestream}

`RangeStream` liefert dieselbe Ergebnismenge wie `Range`, der Server teilt die Antwort jedoch in eine Folge von Blöcken auf und überträgt sie als Stream an den Client. So muss keine Seite große Bereiche vollständig im Arbeitsspeicher zwischenspeichern. `RangeStream` akzeptiert dieselbe `RangeRequest` wie `Range`.

Der Client erhält vom Aufruf `RangeStream` einen Stream von `RangeStreamResponse`-Nachrichten:

```protobuf
message RangeStreamResponse {
  RangeResponse range_response = 1;
}
```

Belegung der Felder über die Blöcke hinweg:

* Kvs - Jeder Block enthält einen disjunkten Teil des Ergebnisses. Werden die `kvs` aller Blöcke in ihrer Empfangsreihenfolge aneinandergehängt, ergibt sich dieselbe Schlüsselmenge wie bei einem einzelnen `Range`-Aufruf.
* Header, More, Count - Werden nur im letzten Block gesetzt, und nur wenn der Stream ohne Fehler endet. In früheren Blöcken behalten diese Felder ihre Nullwerte. Wird `proto.Merge` auf die `range_response` jedes Blocks angewendet, entsteht eine `RangeResponse`, die der Antwort von `Range` entspricht.

Endet der Stream mit einem Fehler, enthält kein Block einen gültigen Wert für `header`, `more` oder `count`.

Alle Blöcke des Streams werden anhand derselben Revision bereitgestellt. Ist `Revision` in der Anfrage nicht gesetzt, erfasst der Server beim Start des Streams die neueste bestätigte Revision und verwendet sie für den restlichen Stream weiter.

`RangeStream` unterstützt weder benutzerdefinierte Sortierreihenfolgen noch Revisionsfilter (`min_mod_revision`, `max_mod_revision`, `min_create_revision`, `max_create_revision`). Anfragen, die eines davon verwenden, liefern `Unimplemented`. Auch der gRPC-Proxy von etcd unterstützt `RangeStream` nicht.

Es gibt zwei übliche Arten, einen `RangeStream` zu verarbeiten:

1. **Jeden Block unabhängig verarbeiten.** Geeignet für Szenarien mit hohen Leistungsanforderungen, in denen der Client Schlüssel beim Eintreffen dekodieren und verarbeiten möchte, statt zuerst das gesamte Ergebnis zu sammeln. Der Client durchläuft die Blöcke und verarbeitet die jeweiligen `kvs`. Nachdem der Stream fehlerfrei beendet wurde, liest er `header`, `more` oder `count` aus dem letzten Block.
2. **Eine einzelne Antwort zusammensetzen.** Geeignet, wenn der Client ein Ergebnis wie bei einem unären `Range`-Aufruf benötigt. Er führt die `range_response` jedes Blocks zu einer `RangeResponse` zusammen, etwa mit `proto.Merge`. Das Ergebnis enthält die vollständigen `kvs` sowie `header`, `more` und `count` aus dem letzten Block. Der Go-Client bietet dafür die Hilfsfunktion `clientv3.GetStreamToGetResponse`.

### Put {#put}

Schlüssel werden mit dem Aufruf `Put` im Schlüssel-Wert-Speicher gespeichert. Er nimmt eine `PutRequest` entgegen:

```protobuf
message PutRequest {
  bytes key = 1;
  bytes value = 2;
  int64 lease = 3;
  bool prev_kv = 4;
  bool ignore_value = 5;
  bool ignore_lease = 6;
}
```

* Key - Der Name des Schlüssels, der in den Schlüssel-Wert-Speicher geschrieben werden soll.
* Value - Der Wert als Bytes, der dem Schlüssel im Schlüssel-Wert-Speicher zugeordnet werden soll.
* Lease - Die Lease-ID, die dem Schlüssel im Schlüssel-Wert-Speicher zugeordnet werden soll. Der Lease-Wert 0 bedeutet keine Lease.
* Prev_Kv - Wenn gesetzt, enthält die Antwort die Daten des Schlüssel-Wert-Paars vor der Aktualisierung durch diese `Put`-Anfrage.
* Ignore_Value - Wenn gesetzt, wird der Schlüssel aktualisiert, ohne seinen aktuellen Wert zu ändern. Existiert der Schlüssel nicht, wird ein Fehler zurückgegeben.
* Ignore_Lease - Wenn gesetzt, wird der Schlüssel aktualisiert, ohne seine aktuelle Lease zu ändern. Existiert der Schlüssel nicht, wird ein Fehler zurückgegeben.

Der Client erhält vom Aufruf `Put` eine Nachricht `PutResponse`:

```protobuf
message PutResponse {
  ResponseHeader header = 1;
  mvccpb.KeyValue prev_kv = 2;
}
```

* Prev_Kv - Das durch `Put` überschriebene Schlüssel-Wert-Paar, wenn `Prev_Kv` in der `PutRequest` gesetzt war.

### Schlüsselbereich löschen {#delete-range}

Schlüsselbereiche werden mit dem Aufruf `DeleteRange` gelöscht. Er nimmt eine `DeleteRangeRequest` entgegen:

```protobuf
message DeleteRangeRequest {
  bytes key = 1;
  bytes range_end = 2;
  bool prev_kv = 3;
}
```

* Key, Range_End - Der zu löschende Schlüsselbereich.
* Prev_Kv - Wenn gesetzt, wird der Inhalt der gelöschten Schlüssel-Wert-Paare zurückgegeben.

Der Client erhält vom Aufruf `DeleteRange` eine Nachricht `DeleteRangeResponse`:

```protobuf
message DeleteRangeResponse {
  ResponseHeader header = 1;
  int64 deleted = 2;
  repeated mvccpb.KeyValue prev_kvs = 3;
}
```

* Deleted - Anzahl der gelöschten Schlüssel.
* Prev_Kv - Eine Liste aller durch die Operation `DeleteRange` gelöschten Schlüssel-Wert-Paare.

### Transaktion {#transaction}

Eine Transaktion ist ein atomares If/Then/Else-Konstrukt über dem Schlüssel-Wert-Speicher. Sie bietet eine Grundoperation, die Anfragen zu atomaren Blöcken, also then/else, zusammenfasst und deren Ausführung anhand des Speicherinhalts bedingt, also if. Transaktionen können Schlüssel vor unbeabsichtigten gleichzeitigen Aktualisierungen schützen, Compare-and-swap-Operationen bilden und als Grundlage einer übergeordneten Nebenläufigkeitskontrolle dienen.

Eine Transaktion kann mehrere Anfragen atomar in einer einzigen Anfrage verarbeiten. Bei Änderungen des Schlüssel-Wert-Speichers bedeutet dies, dass die Speicherrevision für die Transaktion nur einmal erhöht wird und alle erzeugten Ereignisse dieselbe Revision haben. Derselbe Schlüssel darf innerhalb einer einzelnen Transaktion jedoch nicht mehrfach geändert werden.

Alle Transaktionen werden durch eine Konjunktion von Vergleichen abgesichert, ähnlich einer `If`-Anweisung. Jeder Vergleich prüft einen einzelnen Schlüssel im Speicher. Er kann prüfen, ob ein Wert fehlt oder vorhanden ist, ihn mit einem angegebenen Wert vergleichen oder die Revision beziehungsweise Version eines Schlüssels prüfen. Zwei verschiedene Vergleiche können denselben oder unterschiedliche Schlüssel betreffen. Alle Vergleiche werden atomar angewendet. Sind alle wahr, gilt die Transaktion als erfolgreich, und etcd wendet ihren then- beziehungsweise `success`-Anfrageblock an. Andernfalls gilt sie als fehlgeschlagen, und der else- beziehungsweise `failure`-Anfrageblock wird angewendet.

Jeder Vergleich wird als Nachricht `Compare` kodiert:

```protobuf
message Compare {
  enum CompareResult {
    EQUAL = 0;
    GREATER = 1;
    LESS = 2;
    NOT_EQUAL = 3;
  }
  enum CompareTarget {
    VERSION = 0;
    CREATE = 1;
    MOD = 2;
    VALUE= 3;
  }
  CompareResult result = 1;
  // target is the key-value field to inspect for the comparison.
  CompareTarget target = 2;
  // key is the subject key for the comparison operation.
  bytes key = 3;
  oneof target_union {
    int64 version = 4;
    int64 create_revision = 5;
    int64 mod_revision = 6;
    bytes value = 7;
  }
}
```

* Result - Die Art der logischen Vergleichsoperation, etwa gleich oder kleiner als.
* Target - Das zu vergleichende Schlüssel-Wert-Feld: Version, Erstellungsrevision, Änderungsrevision oder Wert des Schlüssels.
* Key - Der Schlüssel für den Vergleich.
* Target_Union - Die vom Benutzer angegebenen Daten für den Vergleich.

Nach dem Verarbeiten des Vergleichsblocks wendet die Transaktion einen Anfrageblock an. Ein Block ist eine Liste von `RequestOp`-Nachrichten:

```protobuf
message RequestOp {
  // request is a union of request types accepted by a transaction.
  oneof request {
    RangeRequest request_range = 1;
    PutRequest request_put = 2;
    DeleteRangeRequest request_delete_range = 3;
  }
}
```

* Request_Range - Eine `RangeRequest`.
* Request_Put - Eine `PutRequest`. Die Schlüssel müssen eindeutig sein. Sie darf keine Schlüssel mit anderen Put- oder Delete-Anfragen gemeinsam haben.
* Request_Delete_Range - Eine `DeleteRangeRequest`. Sie darf keine Schlüssel mit Put- oder Delete-Anfragen gemeinsam haben.

Zusammengesetzt wird eine Transaktion mit dem API-Aufruf `Txn` ausgeführt, der eine `TxnRequest` entgegennimmt:

```protobuf
message TxnRequest {
  repeated Compare compare = 1;
  repeated RequestOp success = 2;
  repeated RequestOp failure = 3;
}
```

* Compare - Eine Liste von Prädikaten, die eine Konjunktion von Bedingungen zur Absicherung der Transaktion repräsentiert.
* Success - Eine Liste von Anfragen, die verarbeitet werden, wenn alle Vergleiche true ergeben.
* Failure - Eine Liste von Anfragen, die verarbeitet werden, wenn ein Vergleich false ergibt.

Der Client erhält vom Aufruf `Txn` eine Nachricht `TxnResponse`:

```protobuf
message TxnResponse {
  ResponseHeader header = 1;
  bool succeeded = 2;
  repeated ResponseOp responses = 3;
}
```

* Succeeded - Gibt an, ob `Compare` true oder false ergab.
* Responses - Eine Liste von Antworten auf die Ergebnisse der Anwendung des Blocks `Success`, wenn succeeded true ist, beziehungsweise `Failure`, wenn succeeded false ist.

Die Liste `Responses` entspricht den Ergebnissen der angewendeten Liste `RequestOp`. Jede Antwort ist als `ResponseOp` kodiert:

```protobuf
message ResponseOp {
  oneof response {
    RangeResponse response_range = 1;
    PutResponse response_put = 2;
    DeleteRangeResponse response_delete_range = 3;
  }
}
```

Der in jeder inneren Antwort enthaltene `ResponseHeader` sollte in keiner Weise ausgewertet werden.
Wenn Clients die neueste Revision benötigen, sollten sie immer den obersten `ResponseHeader` in `TxnResponse` prüfen.


## Watch-API {#watch-api}

Die API `Watch` bietet eine ereignisbasierte Schnittstelle zur asynchronen Überwachung von Schlüsseländerungen. Ein etcd-Watch wartet auf Änderungen, indem er ab einer angegebenen aktuellen oder historischen Revision fortlaufend beobachtet und Schlüsselaktualisierungen an den Client zurückstreamt.

### Ereignisse {#events}

Jede Änderung an jedem Schlüssel wird durch `Event`-Nachrichten dargestellt. Eine `Event`-Nachricht enthält sowohl die Daten als auch die Art der Aktualisierung:

```protobuf
message Event {
  enum EventType {
    PUT = 0;
    DELETE = 1;
  }
  EventType type = 1;
  KeyValue kv = 2;
  KeyValue prev_kv = 3;
}
```

* Type - Die Art des Ereignisses. PUT zeigt an, dass neue Daten unter dem Schlüssel gespeichert wurden. DELETE zeigt an, dass der Schlüssel gelöscht wurde.
* KV - Der dem Ereignis zugeordnete KeyValue. Ein PUT-Ereignis enthält das aktuelle kv-Paar. Ein PUT-Ereignis mit kv.Version=1 zeigt die Erstellung eines Schlüssels an. Ein DELETE-Ereignis enthält den gelöschten Schlüssel, dessen Änderungsrevision auf die Revision der Löschung gesetzt ist.
* Prev_KV - Das Schlüssel-Wert-Paar aus der Revision unmittelbar vor dem Ereignis. Um Bandbreite zu sparen, wird es nur gesetzt, wenn der Watch dies ausdrücklich aktiviert hat.

### Watch-Streams {#watch-streams}

Watches sind lang laufende Anfragen und übertragen Ereignisdaten über gRPC-Streams. Ein Watch-Stream ist bidirektional: Der Client schreibt in den Stream, um Watches einzurichten, und liest daraus, um Watch-Ereignisse zu empfangen. Ein einzelner Stream kann viele verschiedene Watches multiplexen, indem er Ereignisse mit einer Kennung pro Watch versieht. Dieses Multiplexing verringert den Speicherbedarf und den Verbindungsaufwand im eigentlichen etcd-Cluster.

Garantien für Watch-Ereignisse sind unter [Garantien der etcd-API][watch-api-guarantees] beschrieben.

Ein Client erstellt einen Watch, indem er eine `WatchCreateRequest` über einen von `Watch` zurückgegebenen Stream sendet:

```protobuf
message WatchCreateRequest {
  bytes key = 1;
  bytes range_end = 2;
  int64 start_revision = 3;
  bool progress_notify = 4;

  enum FilterType {
    NOPUT = 0;
    NODELETE = 1;
  }
  repeated FilterType filters = 5;
  bool prev_kv = 6;
}
```

* Key, Range_End - Der zu beobachtende Schlüsselbereich.
* Start_Revision - Eine optionale Revision, ab der einschließlich beobachtet wird. Ist sie nicht angegeben, werden Ereignisse nach der Revision im Antwortheader der Watch-Erstellung gestreamt. Der gesamte verfügbare Ereignisverlauf kann ab der letzten Kompaktierungsrevision beobachtet werden.
* Progress_Notify - Wenn gesetzt und keine aktuellen Ereignisse vorliegen, erhält der Watch regelmäßig eine WatchResponse ohne Ereignisse. Das ist nützlich, wenn Clients einen unterbrochenen Watcher ab einer kürzlich bekannt gewordenen Revision wiederherstellen möchten. Der etcd-Server entscheidet anhand der aktuellen Serverlast, wie häufig er Benachrichtigungen sendet.
* Filters - Eine Liste von Ereignistypen, die serverseitig herausgefiltert werden sollen.
* Prev_Kv - Wenn gesetzt, erhält der Watch die Schlüssel-Wert-Daten vor dem Ereignis. So lässt sich erkennen, welche Daten überschrieben wurden.

Als Antwort auf eine `WatchCreateRequest` oder bei einem neuen Ereignis für einen eingerichteten Watch erhält der Client eine `WatchResponse`:

```protobuf
message WatchResponse {
  ResponseHeader header = 1;
  int64 watch_id = 2;
  bool created = 3;
  bool canceled = 4;
  int64 compact_revision = 5;

  repeated mvccpb.Event events = 11;
}
```

* Watch_ID - Die ID des Watches, zu dem die Antwort gehört.
* Created - Wird auf true gesetzt, wenn die Antwort zu einer Anfrage zum Erstellen eines Watches gehört. Der Client sollte die ID speichern und die Ereignisse für den Watch im Stream erwarten. Alle an den erstellten Watcher gesendeten Ereignisse haben dieselbe watch_id.
* Canceled - Wird auf true gesetzt, wenn die Antwort zu einer Anfrage zum Abbrechen eines Watches gehört. An den abgebrochenen Watcher werden keine weiteren Ereignisse gesendet.
* Compact_Revision - Wird auf die kleinste in etcd verfügbare historische Revision gesetzt, wenn ein Watcher versucht, eine kompaktierte Revision zu beobachten. Dies geschieht beim Erstellen eines Watchers an einer kompaktierten Revision oder wenn er den Fortschritt des Schlüssel-Wert-Speichers nicht einholen kann. Der Watcher wird abgebrochen; das Erstellen neuer Watches mit derselben start_revision schlägt fehl.
* Events - Eine geordnete Liste neuer Ereignisse für die angegebene Watch-ID.

Wenn der Client keine weiteren Ereignisse für einen Watch empfangen möchte, sendet er eine `WatchCancelRequest`:

```protobuf
message WatchCancelRequest {
   int64 watch_id = 1;
}
```

* Watch_ID - Die ID des abzubrechenden Watches, damit keine weiteren Ereignisse übertragen werden.

## Lease-API {#lease-api}

Leases sind ein Mechanismus zur Erkennung, ob Clients noch aktiv sind. Der Cluster gewährt Leases mit einer Lebensdauer. Eine Lease läuft ab, wenn der etcd-Cluster innerhalb eines angegebenen TTL-Zeitraums kein keepAlive empfängt.

Um Leases mit dem Schlüssel-Wert-Speicher zu verknüpfen, kann jeder Schlüssel höchstens einer Lease zugeordnet werden. Läuft eine Lease ab oder wird sie widerrufen, werden alle ihr zugeordneten Schlüssel gelöscht. Jeder abgelaufene Schlüssel erzeugt ein Löschereignis im Ereignisverlauf.

### Leases erhalten {#obtaining-leases}

Leases werden mit dem API-Aufruf `LeaseGrant` angefordert. Er nimmt eine `LeaseGrantRequest` entgegen:

```protobuf
message LeaseGrantRequest {
  int64 TTL = 1;
  int64 ID = 2;
}
```

* TTL - Die als Richtwert angegebene Lebensdauer in Sekunden.
* ID - Die angeforderte ID der Lease. Ist ID auf 0 gesetzt, wählt etcd eine ID aus.

Der Client erhält vom Aufruf `LeaseGrant` eine `LeaseGrantResponse`:

```protobuf
message LeaseGrantResponse {
  ResponseHeader header = 1;
  int64 ID = 2;
  int64 TTL = 3;
}
```

* ID - Die Lease-ID der gewährten Lease.
* TTL - Die vom Server gewählte Lebensdauer der Lease in Sekunden.

```protobuf
message LeaseRevokeRequest {
  int64 ID = 1;
}
```

* ID - Die Lease-ID der zu widerrufenden Lease. Beim Widerruf werden alle zugeordneten Schlüssel gelöscht.

### Keepalives {#keep-alives}

Leases werden über einen bidirektionalen Stream erneuert, der mit dem API-Aufruf `LeaseKeepAlive` erstellt wird. Möchte der Client eine Lease erneuern, sendet er eine `LeaseKeepAliveRequest` über den Stream:

```protobuf
message LeaseKeepAliveRequest {
  int64 ID = 1;
}
```

* ID - Die Lease-ID der am Leben zu haltenden Lease.

Der Keepalive-Stream antwortet mit einer `LeaseKeepAliveResponse`:

```protobuf
message LeaseKeepAliveResponse {
  ResponseHeader header = 1;
  int64 ID = 2;
  int64 TTL = 3;
}
```

* ID - Die Lease, die mit einer neuen TTL erneuert wurde.
* TTL - Die neue verbleibende Lebensdauer der Lease in Sekunden.

[watch-api-guarantees]: /de/docs/etcd/learning/api_guarantees/#watch-apis
[elections]: https://github.com/etcd-io/etcd/blob/main/client/v3/concurrency/election.go
[grpc-api]: /de/docs/etcd/dev-guide/api_reference_v3/
[grpc-service]: https://github.com/etcd-io/etcd/blob/main/api/etcdserverpb/rpc.proto
[kv-proto]: https://github.com/etcd-io/etcd/blob/main/api/mvccpb/kv.proto
[locks]: https://github.com/etcd-io/etcd/blob/main/client/v3/concurrency/mutex.go
[mvcc]: https://en.wikipedia.org/wiki/Multiversion_concurrency_control
[stm]: https://github.com/etcd-io/etcd/blob/main/client/v3/concurrency/stm.go
