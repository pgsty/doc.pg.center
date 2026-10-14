---
title: Authentifizierungsdesign von etcd v3
weight: 2500
description: Authentifizierung in etcd v3
categories: [Konzept]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/design-auth-v3.md"
---

## Warum das Authentifizierungssystem von v2 nicht wiederverwenden? {#why-not-reuse-the-v2-auth-system}

Das v3-Protokoll verwendet gRPC als Transport anstelle einer RESTful-Schnittstelle wie in v2. Das neue Protokoll bietet die Gelegenheit, den Entwurf von v2 weiterzuentwickeln und zu verbessern. Beispielsweise authentifiziert v3 pro Verbindung, während die langsamere Authentifizierung in v2 pro Anfrage erfolgt. Zudem erschwert die Semantik der v2-Authentifizierung in der Praxis Überlegungen zur Konsistenz, wie die nächsten Abschnitte erläutern. Für v3 gibt es eine klar definierte Beschreibung und Implementierung des Authentifizierungsmechanismus, die die Schwächen des v2-Systems behebt.

### Funktionale Anforderungen {#functionality-requirements}

* Authentifizierung pro Verbindung statt pro Anfrage
   * Auf Benutzer-ID und Passwort basierende Authentifizierung für die gRPC-API
   * Die Authentifizierung muss nach Änderungen der Authentifizierungsrichtlinie erneuert werden
* Die Funktionalität sollte so einfach und nützlich sein wie in v2
   * v3 bietet einen flachen Schlüsselraum statt der Verzeichnisstruktur von v2. Berechtigungen werden durch Intervallabgleich geprüft.
* Sie sollte stärkere Konsistenzgarantien als die v2-Authentifizierung bieten

### Wesentliche erforderliche Änderungen {#main-required-changes}

* Ein Client muss vor dem Senden authentifizierter Anfragen eine eigene Verbindung ausschließlich zur Authentifizierung aufbauen
* Berechtigungsinformationen (Benutzer-ID und autorisierte Revision) zu den Raft-Befehlen (`etcdserverpb.InternalRaftRequest`) hinzufügen
* Die Berechtigungen jeder Anfrage werden in der Zustandsmaschinenschicht statt in der API-Schicht geprüft

### Konsistenz der Berechtigungsmetadaten {#permission-metadata-consistency}

Die Authentifizierungsmetadaten sollten wie andere Daten in etcd im Speicher abgelegt und verwaltet werden, den das Raft-Protokoll von etcd kontrolliert. Das ist erforderlich, um Verfügbarkeit und Konsistenz des gesamten etcd-Clusters zu erhalten. Wenn das Lesen oder Schreiben der Metadaten, etwa von Berechtigungsinformationen, die Zustimmung jedes Knotens und damit mehr als ein Quorum benötigt, kann der Ausfall eines einzelnen Knotens den gesamten Cluster anhalten. Müssen alle Knoten gleichzeitig zustimmen, lässt sich die Prüfung gewöhnlicher Lese- und Schreibanfragen nicht abschließen, sobald ein Clustermitglied ausfällt, selbst wenn noch ein Quorum verfügbar ist. Dieses Einstimmigkeitsverfahren verschlechtert letztlich die Clusterverfügbarkeit. Der auf einem Quorum basierende Raft-Konsens sollte ausreichen, da die Übereinstimmung aus einer konsistenten Reihenfolge folgt.

Der Authentifizierungsmechanismus des etcd-v2-Protokolls hat eine problematische Eigenschaft: Die Metadatenkonsistenz sollte wie oben beschrieben funktionieren, tut es aber nicht. Jede Berechtigungsprüfung wird von dem etcd-Mitglied durchgeführt, das die Client-Anfrage empfängt (server/etcdserver/api/v2http/client.go), einschließlich Follower-Mitgliedern. Die Prüfung kann daher auf veralteten Metadaten beruhen.


Aufgrund dieser möglichen Veraltung wird die Authentifizierungskonfiguration nicht zwingend wirksam, sobald Betreiber etcdctl ausführen. Es lässt sich daher nicht feststellen, wie lange veraltete Metadaten noch gelten. In der Praxis wird die Konfigurationsänderung unmittelbar nach der Befehlsausführung wirksam. Unter hoher Last kann der inkonsistente Zustand jedoch länger anhalten und für Benutzer und Entwickler unerwartete Situationen verursachen. Dafür ist eine Umgehungslösung wie [diese](https://github.com/etcd-io/etcd/pull/4317#issuecomment-179037582) erforderlich.

### Inkonsistente Berechtigungen gefährden linearisierte Anfragen {#inconsistent-permissions-are-unsafe-for-linearized-requests}

Ein inkonsistenter Authentifizierungszustand ist bei Schreibvorgängen am schwerwiegendsten. Selbst wenn ein Betreiber einem Benutzer das Schreiben verbietet, kann ein Schreibvorgang erfolgreich abgeschlossen werden, sofern seine Reihenfolge nur gegenüber dem Schlüssel-Wert-Speicher, nicht aber gegenüber dem Authentifizierungssystem festgelegt ist. Ohne eine Reihenfolge über Authentifizierungsspeicher und Schlüssel-Wert-Speicher hinweg ist das System für Angriffe mit veralteten Berechtigungen anfällig.

Deshalb sollte die Berechtigungsprüfung in die Zustandsmaschine von etcd aufgenommen werden. Jede Zustandsmaschine sollte Anfragen in der Apply-Phase anhand ihrer Berechtigungsinformationen prüfen. Die Authentifizierungsinformationen dürfen dabei nicht veraltet sein.

## Entwurf und Implementierung {#design-and-implementation}

### Authentifizierung {#authentication}

Zunächst muss ein Client eine gRPC-Verbindung ausschließlich zur Authentifizierung seiner Benutzer-ID und seines Passworts aufbauen. Ein etcd-Server antwortet bei Erfolg mit einem Authentifizierungstoken, bei Fehlschlag mit einem Fehler. Der Client kann das Token verwenden, um sich bei API-Anfragen gegenüber etcd auszuweisen.

Die Client-Verbindung, über die das Authentifizierungstoken angefordert wurde, wird üblicherweise verworfen; sie kann die Anmeldedaten des neuen Tokens nicht übertragen. gRPC bietet nämlich keine Möglichkeit, nach dem Verbindungsaufbau durch `grpc.Dial()` Anmeldedaten pro RPC hinzuzufügen. Ein Client kann einer Verbindung daher kein Token zuweisen, das er über diese Verbindung erhalten hat. Zur Verwendung des Tokens benötigt er eine neue Verbindung.

#### Hinweise zur Implementierung des RPC `Authenticate()` {#notes-on-the-implementation-of-authenticate-rpc}

Der RPC `Authenticate()` erzeugt anhand eines angegebenen Benutzernamens und Passworts ein Authentifizierungstoken. etcd verwendet das Go-Paket `bcrypt`, um ein konfiguriertes Passwort zu speichern und ein angegebenes Passwort dagegen zu prüfen. Die Passwortprüfung von `bcrypt` ist absichtlich rechenaufwendig und dauert auf einem gewöhnlichen x64-Server fast 100ms. Diese Prüfung in der Apply-Phase der Zustandsmaschine würde daher Leistungsprobleme verursachen: Der gesamte etcd-Cluster könnte nur knapp 10 `Authenticate()`-Anfragen pro Sekunde verarbeiten.

Aus Leistungsgründen prüft der v3-Authentifizierungsmechanismus Passwörter in der API-Schicht von etcd, wo dies außerhalb von Raft parallelisiert werden kann. Dadurch können jedoch Berechtigungslücken zwischen Prüf- und Verwendungszeitpunkt entstehen (Time-of-check/Time-of-use, TOCTOU):
1. Client A sendet eine Anfrage `Authenticate()`
1. Die API-Schicht führt die Passwortprüfung von `Authenticate()` aus
1. Ein anderer Client B sendet eine Anfrage `ChangePassword()`, die der Server abschließt
1. Die Zustandsmaschinenschicht ermittelt die Revisionsnummer für `Authenticate()` von A
1. Der Server meldet A Erfolg
1. A ist nun mit einem veralteten Passwort authentifiziert

Um diese Situation zu vermeiden, führt die API-Schicht eine *Validierung der Versionsnummer* anhand der Revisionsnummer des Authentifizierungsspeichers durch. Während der Passwortprüfung speichert sie dessen Revisionsnummer. Nach erfolgreicher Prüfung vergleicht sie die gespeicherte mit der neuesten Revisionsnummer. Unterscheiden sich die Nummern, wurden die Authentifizierungsmetadaten zwischenzeitlich aktualisiert, und die Prüfung wird wiederholt. Dieser Mechanismus verhindert eine erfolgreiche Prüfung anhand eines veralteten Passworts.

### Ein Token in der API-Schicht auflösen {#resolving-a-token-in-the-api-layer}

Nach der Authentifizierung mit `Authenticate()` kann ein Client wie ohne Authentifizierung eine gRPC-Verbindung aufbauen. Zusätzlich zum bestehenden Initialisierungsablauf muss er das Token der neu erstellten Verbindung zuordnen. `grpc.WithPerRPCCredentials()` bietet die dafür erforderliche Funktion.

Jede authentifizierte Client-Anfrage enthält ein Token. Serverseitig lässt es sich mit `grpc.metadata.FromIncomingContext()` abrufen. Der Server kann daraus ermitteln, wer die Anfrage stellt und wann der Benutzer autorisiert wurde. Die API-Schicht trägt diese Informationen in den Header (`etcdserverpb.RequestHeader.Username` und `etcdserverpb.RequestHeader.AuthRevision`) eines Raft-Logeintrags (`etcdserverpb.InternalRaftRequest`) ein.

### Berechtigungen in der Zustandsmaschine prüfen {#checking-permission-in-the-state-machine}

Die Authentifizierungsinformationen in `etcdserverpb.RequestHeader` werden in der Apply-Phase der Zustandsmaschine geprüft. Dabei wird anhand der neuesten Revision des Authentifizierungsspeichers geprüft, ob der Benutzer Zugriff auf die angeforderten Schlüssel hat.

### Zwei Token-Typen: simple und JWT {#two-types-of-tokens-simple-and-jwt}

Es gibt zwei Token-Typen: simple und JWT. Das simple-Token ist nicht für den Produktivbetrieb vorgesehen. Diese Token sind nicht kryptografisch signiert, und die Server müssen die Zuordnung zwischen Token und Benutzern als Zustand verwalten. Sie sind für Entwicklungstests gedacht. Für produktive Bereitstellungen sollten JWT-Token verwendet werden, da sie kryptografisch signiert und geprüft werden. Aus Implementierungssicht ist JWT zustandslos. Ein JWT-Token kann Metadaten wie Benutzernamen und Revision enthalten, sodass Server die Zuordnung zwischen Token und Metadaten nicht speichern müssen.

> [!WARNING]
> Für simple-Token ist das Problem [#18437](https://github.com/etcd-io/etcd/issues/18437) bekannt. Auf etcd-Servern werden Token in der API-Schicht aufgelöst, und simple-Token sind zustandsbehaftet. Der Vorgang ist nicht durch eine linearisierbare Prüfung geschützt. Daher kann ein etcd-Mitglied die vorherige Authentifizierungsanfrage noch nicht vollständig verarbeitet haben, wenn die nächste eintrifft. In diesem Fall kann es dem Client den Fehler "invalid auth token" zurückgeben. Auf einem Knoten mit guten Netzwerkbedingungen tritt dieses Problem gewöhnlich selten auf; bei hoher Latenz ist es jedoch möglich. Als Umgehungslösung können Anwendungen bei diesem Fehler einen Wiederholungsmechanismus einsetzen.

### JWT-Token direkt setzen {#directly-setting-jwt-tokens}

Zusätzlich zum Standardablauf über den RPC `Authenticate()` unterstützt etcd das direkte Setzen von JWT-Token auf Client-Ebene. Dadurch können Anwendungen den gesamten Lebenszyklus von JWT-Token außerhalb von etcd verwalten, einschließlich Erzeugung, Validierung und Rotation.

#### Anwendungsfall und Ablauf {#use-case-and-workflow}

Dieser Ansatz ist sinnvoll, wenn:

* Ein separates Token-Verwaltungssystem außerhalb von etcd die Erzeugung und den Lebenszyklus der JWT-Token übernimmt
* Anwendungen bereits signierte JWT-Token über einen externen Mechanismus erhalten, etwa Umgebungsvariablen oder einen Konfigurationsdienst
* Der Token-Lebenszyklus vollständig von der Client-Anwendung statt durch die automatische Token-Erzeugung von etcd verwaltet werden muss

Der typische Ablauf ist:

1. Eine externe Instanz außerhalb von etcd erzeugt ein signiertes JWT-Token, das den Benutzernamen und weitere Claims enthält
2. Die Anwendung erhält das signierte Token und konfiguriert damit den etcd-Client
3. Der Client sendet das JWT-Token direkt mit den Anfragen, ohne `Authenticate()` aufzurufen
4. Der etcd-Server prüft die Token-Signatur mit seinem konfigurierten öffentlichen Schlüssel und gewährt Zugriff anhand des Benutzernamens im Token
5. Vor Ablauf des Tokens ruft die Anwendung ein neues Token von der externen Instanz ab
6. Die Anwendung erstellt einen neuen Client mit dem aktualisierten Token; Token-Aktualisierungen erfordern eine Neuerstellung des Clients

#### Unterschiede zur Standardauthentifizierung {#how-it-differs-from-standard-authentication}

Beim Standardablauf mit `Authenticate()`:

* Der Client ruft `Authenticate()` mit Benutzername und Passwort auf
* etcd erzeugt ein Token und gibt es zurück
* Der Client verwendet dieses Token automatisch für nachfolgende Anfragen
* Zum Erneuern des Tokens muss `Authenticate()` erneut aufgerufen werden

Beim direkten Setzen von JWT-Token:

* Der Client wird mit einem bereits signierten JWT-Token initialisiert
* Der Client ruft `Authenticate()` **nicht** auf
* Das Token wird direkt in allen Anfragen verwendet
* Die Client-Anwendung ist dafür verantwortlich, vor Ablauf neue Token zu beschaffen und den Lebenszyklus des Clients zu verwalten

#### AuthStatus ohne gültiges Token {#authstatus-without-valid-token}

Um Anwendungen mit eigener JWT-Token-Verwaltung zu unterstützen, ermöglicht der RPC `AuthStatus` Clients festzustellen, ob die Authentifizierung aktiviert ist, und die aktuelle `authRevision` abzurufen. Das ist für Wiederherstellungsszenarien wichtig, in denen ein Token abgelaufen ist und der Client die neueste Revision benötigt, um von seinem externen Token-Anbieter ein neues gültiges Token zu erhalten.

Ohne diese Möglichkeit könnte ein abgelaufenes Token verhindern, dass ein Client die aktuelle `authRevision` ermittelt. Dies könnte zu einer Blockade führen, in der kein neues Token erzeugt werden kann.

## Unterschiede zwischen KVS-Modellen und Dateisystemmodellen {#notes-on-the-difference-between-kvs-models-and-file-system-models}

etcd v3 ist ein KVS und kein Dateisystem. Daher können Benutzern Berechtigungen für einen exakten Schlüsselnamen oder einen Schlüsselbereich wie `["start key", "end key")` erteilt werden. Berechtigungen für nicht vorhandene Schlüssel sind somit möglich. Benutzer sollten auf unbeabsichtigt erteilte Berechtigungen achten. In dateisystemähnlichen Systemen wie Chubby oder ZooKeeper kann eine inode-ähnliche Datenstruktur die Berechtigungsinformationen enthalten. Dort können keine Berechtigungen für nicht vorhandene Schlüssel erteilt werden, abgesehen vom Fall der Sticky Bits.

Anders als dateisystemähnliche Systeme erfordert das Modell von etcd v3 mehrere Metadatenabfragen. Im ungünstigsten Fall entspricht der Suchaufwand der Summe aller Schlüssel und Intervalle, für die der Benutzer Berechtigungen hat. Dieser Aufwand lässt sich nicht vermeiden, weil sich der flache Schlüsselraum von v3 grundlegend vom Unix-Dateisystemmodell unterscheidet, bei dem jeder inode Berechtigungsmetadaten enthält. In der Praxis ist der Aufwand kein ernstes Problem, da die Metadaten klein genug sind, um vom Caching zu profitieren.
