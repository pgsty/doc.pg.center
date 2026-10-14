---
title: "1. Kurzer Überblick über HTTP"
linkTitle: "1. HTTP-Grundlagen"
weight: 120
description: "HTTP-Transaktionen, Anfragen, Antworten, Header und Protokollbegriffe"
icon: fa-solid fa-globe
module: [HAPROXY]
categories: [Konzept]
aliases:
  - /haproxy/configuration/http-fundamentals/
  - /haproxy/configuration/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 1"
---

Dieses Dokument beschreibt die Konfigurationssprache der oben angegebenen Version. Es enthält keine Hinweise, Beispiele oder Empfehlungen. Dafür stehen das Referenzhandbuch und das Architekturhandbuch zur Verfügung. Die nummerierten Kapitel sind in der flachen HAProxy-Seitenleiste zur direkten Navigation angeordnet.

Im HTTP-Modus analysiert und indiziert HAProxy sowohl Anfragen als auch Antworten vollständig. Dadurch lassen sich Abgleichkriterien für nahezu jeden Bestandteil ihres Inhalts festlegen.

Dafür ist es wichtig, den Aufbau von HTTP-Anfragen und -Antworten sowie ihre Zerlegung durch HAProxy zu verstehen. Damit wird es leichter, korrekte Regeln zu schreiben und Fehler in vorhandenen Konfigurationen zu finden.

HTTP ist durch eine Reihe von RFCs standardisiert, denen HAProxy möglichst genau folgt:

- RFC 9110: HTTP-Semantik (Bedeutung der Protokollelemente)
- RFC 9111: HTTP-Caching (Regeln für HTTP-Caches)
- RFC 9112: HTTP/1.1 (Darstellung, Interoperabilitätsregeln, Sicherheit)
- RFC 9113: HTTP/2 (Darstellung, Interoperabilitätsregeln, Sicherheit)
- RFC 9114: HTTP/3 (Darstellung, Interoperabilitätsregeln, Sicherheit)

Außerdem spezifizieren RFC 8999 bis 9002 die QUIC-Transportschicht, die das HTTP/3-Protokoll verwendet.

## 1.1. Das HTTP-Transaktionsmodell {#section-1-1}

HTTP arbeitet transaktionsorientiert: Jede Anfrage führt zu genau einer Antwort. Ursprünglich gab es in Protokollversion 1.0 nur eine Anfrage je Verbindung. Der Client baut eine TCP-Verbindung zum Server auf und sendet darüber eine Anfrage. Der Server antwortet, anschließend wird die Verbindung geschlossen. Eine weitere Anfrage erfordert dann eine neue Verbindung:

```text
[CON1] [REQ1] ... [RESP1] [CLO1] [CON2] [REQ2] ... [RESP2] [CLO2] ...
```

In diesem oft "HTTP close" genannten Modus gibt es ebenso viele Verbindungsaufbauten wie HTTP-Transaktionen. Da der Server die Verbindung nach der Antwort schließt, muss der Client die Inhaltslänge nicht kennen. Mit dem Schließen der Verbindung betrachtet er die Antwort als vollständig. Werden Antworten wegen Netzwerkfehlern abgeschnitten, kann der Client sie deshalb irrtümlich für vollständig halten. Früher wurden dadurch gelegentlich unvollständige Bilder auf dem Bildschirm angezeigt.

Der transaktionsorientierte Aufbau ermöglichte eine Erweiterung, bei der die Verbindung zwischen aufeinanderfolgenden Transaktionen offen bleibt. Dabei muss der Server jedoch für jede Antwort die Inhaltslänge angeben, damit der Client nicht endlos wartet. Dazu dient der besondere Header "Content-length". Dieser "keep-alive" genannte Modus kam mit HTTP/1.1 hinzu; einige HTTP/1.0-Implementierungen unterstützen ihn ebenfalls. Zwischen Anfragen wiederverwendete Verbindungen heißen persistente Verbindungen:

```text
[CON] [REQ1] ... [RESP1] [REQ2] ... [RESP2] [CLO] ...
```

Vorteile sind die geringere Latenz zwischen Transaktionen, der geringere Rechenaufwand auf dem Server und die Möglichkeit, abgeschnittene Antworten zu erkennen. Der Modus ist meist schneller als das Schließen nach jeder Antwort, aber nicht immer: Manche Clients begrenzen die Zahl gleichzeitiger Verbindungen stärker, wodurch eine schlechte Netzwerkverbindung weniger gut ausgeglichen wird. Zudem müssen manche Server Verbindungen lange offen halten, um auf eine mögliche weitere Anfrage zu warten. Viele Verbindungen können dann viel Speicher belegen. Zu frühes Schließen kann dagegen Anfragen unterbrechen, die genau in diesem Moment eintreffen.

In diesem Modus muss die Antwortgröße vorab bekannt sein. Bei dynamisch erzeugten oder komprimierten Inhalten ist das nicht immer möglich. Deshalb wurde der "chunked mode" eingeführt. Statt sofort die Gesamtgröße anzukündigen, meldet der Sender nur die Größe des nächsten bereits gepufferten Antwortblocks, des sogenannten Chunks. Mit einem Block der Größe null kann er die Übertragung jederzeit beenden. Der Header Content-Length wird in diesem Modus nicht verwendet.

Eine weitere Verbesserung ist Pipelining. Dabei bleibt Keep-Alive aktiv, der Client wartet jedoch nicht auf die erste Antwort, bevor er die zweite Anfrage sendet. Das ist beim Abruf vieler Bilder einer Seite nützlich:

```text
[CON] [REQ1] [REQ2] ... [RESP1] [RESP2] [CLO] ...
```

Dies kann die Leistung erheblich verbessern, da die Netzwerklatenz zwischen aufeinanderfolgenden Anfragen entfällt. Viele HTTP-Implementierungen unterstützen Pipelining nicht korrekt, weil HTTP keine Möglichkeit bietet, eine Antwort der zugehörigen Anfrage zuzuordnen. Deshalb muss der Server genau in der Reihenfolge der eingegangenen Anfragen antworten. Nach mehreren Einführungsversuchen verschiedener Clients wurde Pipelining in der Praxis wegen seiner Unzuverlässigkeit auf manchen Servern vollständig aufgegeben. Server müssen es dennoch unterstützen.

Die nächste Verbesserung ist Multiplexing, wie es HTTP/2 und HTTP/3 verwenden. Mehrere Transaktionen, also Anfrage-Antwort-Paare, laufen parallel über eine einzige Verbindung und kommen unabhängig voneinander mit ihrer jeweiligen Geschwindigkeit voran. Multiplex-Protokolle führen dafür den Begriff Stream ein: eine dieser parallelen Kommunikationen über dieselbe Verbindung. Jeder Stream erhält normalerweise eine innerhalb der Verbindung eindeutige Kennung. Beide Endpunkte erkennen daran, wohin die Daten gehören. Clients starten häufig viele Streams gleichzeitig, bis zu 100 und manchmal mehr, und lassen den Server die Anfragen bearbeiten und je nach Verfügbarkeit der Antworten in beliebiger Reihenfolge beantworten. Multiplexing verringert vor allem die Anzahl der Hin- und Rückläufe deutlich und beschleunigt das Laden von Seiten über Netzwerke mit hoher Latenz. Bei bildreichen Websites ist bisweilen zu sehen, wie alle Bilder gleichzeitig geladen werden.

Diese Protokolle komprimieren außerdem Header-Felder, um weniger Bytes übertragen zu müssen. Das verbessert ihre Effizienz, macht sie ohne geeignete Werkzeuge jedoch praktisch weder von Hand bearbeitbar noch mit bloßem Auge lesbar, wie es bei HTTP/1 möglich war. Deshalb stellt die Fachliteratur einschließlich dieses Dokuments HTTP-Nachrichten weiterhin in HTTP/1-Syntax dar, auch für neuere Protokollversionen.

HTTP/2 hat konstruktionsbedingte Einschränkungen. Paketverluste betreffen beispielsweise alle Streams gleichzeitig. Benötigt ein Client viel Zeit zum Abruf eines Objekts, etwa weil er es auf die Festplatte schreiben muss, kann er den Abruf verlangsamen und währenddessen den Zugriff auf dahinter wartende Daten unmöglich machen. Dies heißt Head-of-Line-Blocking, kurz HoL-Blocking oder auch nur HoL.

HTTP/3 verwendet QUIC, das seinerseits auf UDP aufsetzt. QUIC beseitigt Head-of-Line-Blocking auf der Transportebene durch unabhängig behandelte Streams. Bei Paketverlusten beeinträchtigt ein betroffener Stream die anderen nicht; auf alle lässt sich parallel zugreifen. QUIC unterstützt auch die Migration von Verbindungen, die HAProxy derzeit jedoch nicht unterstützt.

Für persistente Verbindungen verwendet HAProxy standardmäßig Keep-Alive. Es verarbeitet jede Anfrage und Antwort und lässt die Verbindung auf beiden Seiten zwischen dem Ende einer Antwort und der nächsten Anfrage ruhen. Bei einer HTTP/2-Verbindung vom Client verarbeitet es alle Anfragen parallel und lässt die Verbindung bis zu weiteren Anfragen offen und inaktiv, wie bei einer HTTP-Verbindung mit Keep-Alive.

HAProxy unterstützt im Wesentlichen 3 Verbindungsmodi:

- keep alive: Alle Anfragen und Antworten werden verarbeitet. Die Verbindungen zum
  Client und zum Server bleiben für weitere Anfragen offen. Dies ist der Standard
  und passt zum modernen Web sowie zu HTTP/2 und HTTP/3.

- server close: Die Verbindung zum Server wird nach der Antwort geschlossen.

- close: Nach dem Ende der Antwort wird die Verbindung auf beiden Seiten aktiv geschlossen.

Außerdem kann die serverseitige Verbindung standardmäßig für jede Anfrage eines beliebigen Clients wiederverwendet werden, wie es die HTTP-Spezifikation verlangt. Benötigte Informationen zu einem bestimmten Client, etwa seine Quelladresse, müssen daher mit jeder Anfrage übertragen werden. Bei HTTP/2 zum Server ordnet HAProxy die Verbindung standardmäßig demselben Client zu, um Head-of-Line-Blocking zwischen Clients zu vermeiden.

## 1.2. Begriffe {#section-1-2}

Die Begriffe in HAProxy haben sich mit dem HTTP-Protokoll und dessen Verwendung weiterentwickelt. Anfangs unterschieden sich Verbindung, Sitzung, Stream und Transaktion kaum. Mit der Zeit wurden diese Begriffe genauer abgegrenzt, um den modernen HTTP-Versionen zu entsprechen. Einige ältere Bezeichnungen bleiben aus Kompatibilitätsgründen in der Konfiguration oder der Befehlszeilenschnittstelle sichtbar.

Für die aktuelle HAProxy-Version gelten folgende Definitionen:

- Verbindung: Ein einzelner bidirektionaler Kommunikationskanal zwischen einem
  entfernten Teilnehmer, also Client oder Server, und HAProxy auf der niedrigsten
  möglichen Ebene. Meist entspricht er einem TCP-Socket zwischen einem Paar aus
  IP-Adressen und Ports. Clientseitig sind Verbindungen die ersten Objekte, die beim
  Verbindungsaufbau zu HAProxy entstehen. Regeln auf Verbindungsebene werden zuerst
  angewendet.

- Sitzung: Ergänzt eine Verbindung um Kontextinformationen, etwa transportbezogene
  Daten wie TLS-Schlüssel oder Variablen. In HAProxy bezeichnete der Begriff lange
  durchgehende HTTP/1.0-Kommunikation zwischen zwei Endpunkten. Deshalb erscheint
  er noch in Namen mancher CLI-Befehle oder Statistiken, obwohl heute Streams gemeint
  sind. Hilfetexte und Beschreibungen versuchen, dies eindeutig zu machen. Auf
  Netzwerkebene ist der Begriff weiterhin gültig, etwa für TCP-Sitzungen im
  Betriebssystem oder durch eine Firewall, ebenso für Anwendungen außerhalb von
  HTTP, etwa eine telnet- oder SSH-Sitzung. Er darf nicht mit Anwendungssitzungen
  verwechselt werden, die einen vollständigen Benutzerkontext in einem Cookie
  speichern und demselben Server zugeleitet werden müssen.

- Stream: Entspricht genau einer durchgehenden bidirektionalen Kommunikation auf
  Anwendungsebene, auf die Analysen und Änderungen angewendet werden können.
  Bei HTTP enthält er eine einzelne Anfrage und die zugehörige Antwort. Er entsteht
  beim Eingang der Anfrage und endet mit der vollständigen Auslieferung der Antwort.
  In diesem Zusammenhang besteht eine 1:1-Beziehung zum Stream eines
  Multiplex-Protokolls. Bei TCP-Kommunikation gibt es einen Stream je Verbindung.

- Transaktion: Besteht nur aus einer Anfrage und der zugehörigen Antwort. Vor der
  Einführung von Streams wurde der Begriff zusammen mit Sitzungen verwendet;
  heute besteht eine 1:1-Beziehung zwischen Transaktion und Stream. Sichtbar ist
  er vor allem im Variablengültigkeitsbereich "txn", der während der gesamten
  Transaktion und damit des Streams gilt.

- Anfrage: Bezeichnet den Datenverkehr vom Client zum Server. Der Begriff wird
  vorwiegend bei HTTP verwendet, um anzugeben, wo Operationen ausgeführt werden,
  bei TCP aber ebenso zur Angabe der Verarbeitungsrichtung. In Zählern dienen
  Anfragen oft als Einheit für Verkehr oder Aktivität. Sie führen nicht immer zu
  einer Antwort, etwa bei Fehlern. Da es jedoch keine unaufgeforderten Antworten
  ohne Anfragen gibt, bleiben Anfragen ein sinnvolles Maß für die Gesamtaktivität.
  Bei TCP gibt es ebenso viele Anfragen wie Verbindungen.

- Antwort: Bezeichnet den Datenverkehr vom Server zum Client oder von HAProxy zum
  Client, wenn HAProxy die Antwort selbst erzeugt, etwa bei einer HTTP-Weiterleitung.

- Dienst: Bezeichnet meist eine interne Verarbeitung in HAProxy, für die kein Server
  erforderlich ist, etwa die Statistikseite, der Cache oder Lua-Code für eine kleine
  Anwendung. Ein Dienst liest normalerweise eine Anfrage, führt Operationen aus
  und erzeugt eine Antwort.

## 1.3. HTTP-Anfrage {#section-1-3}

Als Beispiel dient folgende HTTP-Anfrage:

```text
Zeilen-  Inhalt
nummer
   1     GET /serv/login.php?lang=en&profile=2 HTTP/1.1
   2     Host: www.mydomain.com
   3     User-agent: my small browser
   4     Accept: image/jpeg, image/gif
   5     Accept: image/png
```

### 1.3.1. Die Anfragezeile {#section-1-3-1}

Zeile 1 ist die Anfragezeile. Sie besteht immer aus 3 Feldern:

- einer Methode: GET
- einer URI: /serv/login.php?lang=en&profile=2
- einer Versionsangabe: HTTP/1.1

Die Felder werden durch sogenannte LWS getrennt, linearen Leerraum nach dem Standard. Meist sind das Leerzeichen; möglich sind aber auch Tabulatoren oder Zeilenumbrüche beziehungsweise Wagenrückläufe, gefolgt von Leerzeichen oder Tabulatoren. Die Methode selbst darf keinen Doppelpunkt (':') enthalten und besteht ausschließlich aus Buchstaben. Wegen dieser vielfältigen Kombinationen ist es sinnvoll, die Zerlegung HAProxy zu überlassen, statt selbst einen komplexen oder ungenauen regulären Ausdruck zu schreiben.

Die URI kann verschiedene Formen haben:

- Eine relative URI:

```text
  /serv/login.php?lang=en&profile=2

Dies ist eine vollständige URL ohne Host-Teil. Diese Form empfangen
normalerweise Server, Reverse-Proxys und transparente Proxys.
```

- Eine absolute URI, auch URL genannt:

```text
  http://192.168.0.12:8080/serv/login.php?lang=en&profile=2

Sie besteht aus einem Schema (Protokollname gefolgt von '://'), einem
Hostnamen oder einer Adresse, optional einem Doppelpunkt (':') mit
Portnummer und einer relativen URI ab dem ersten Schrägstrich ('/')
nach der Adresse. Meist empfangen Proxys diese Form. Ein Server,
der HTTP/1.1 unterstützt, muss sie jedoch ebenfalls akzeptieren.
```

- Ein Stern ('\*'): Diese Form ist nur zusammen mit OPTIONS zulässig und kann nicht
  weitergeleitet werden. Sie dient dazu, die Fähigkeiten des nächsten Netzknotens
  abzufragen.

- Eine Kombination aus Adresse und Port, etwa 192.168.0.12:80. Sie wird mit CONNECT
  verwendet, um TCP-Tunnel durch HTTP-Proxys aufzubauen, meist für HTTPS,
  gelegentlich auch für andere Protokolle.

Eine relative URI besteht aus zwei Teilen. Vor dem Fragezeichen steht der Pfad, normalerweise der relative Pfad zu statischen Objekten auf dem Server. Danach folgt die Abfragezeichenfolge. Sie wird hauptsächlich bei GET-Anfragen an dynamische Skripte verwendet und hängt stark von der eingesetzten Sprache, dem Framework oder der Anwendung ab.

HTTP/2 und HTTP/3 übertragen keine Versionsinformation mit der Anfrage. Daher wird die Version des zugrunde liegenden Protokolls angenommen, also "HTTP/2". Außerdem senden diese Protokolle keine zusammenhängende Anfragezeile. Sie zerlegen sie in einzelne Pseudo-Header, deren Namen mit einem Doppelpunkt beginnen. HAProxy setzt daraus wieder eine entsprechende Anfragezeile zusammen. Deshalb können sich protokollierte Anfragezeilen zwischen HTTP/1.x und HTTP/2 oder HTTP/3 leicht unterscheiden.

### 1.3.2. Die Anfrage-Header {#section-1-3-2}

Die Header beginnen in der zweiten Zeile. Am Zeilenanfang steht ein Name, unmittelbar gefolgt von einem Doppelpunkt (':'). Üblicherweise folgt danach LWS, vorgeschrieben ist das jedoch nicht. Anschließend stehen die Werte. Mehrere gleichnamige Header können in einer Zeile zusammengefasst und ihre Werte durch Kommas getrennt werden, sofern die Reihenfolge erhalten bleibt. Dies kommt häufig beim Feld "Cookie:" vor. Ein Header kann mehrere Zeilen umfassen, wenn die Folgezeilen mit LWS beginnen. Im Beispiel aus 1.3 enthalten die Zeilen 4 und 5 insgesamt 3 Werte für "Accept:". Gemäß Spezifikation wird LWS am Anfang und Ende eines Headers ignoriert und gehört nicht zum Wert.

Entgegen einer verbreiteten Annahme wird bei Header-Namen nicht zwischen Groß- und Kleinschreibung unterschieden. Das gilt auch für Werte, die andere Header-Namen bezeichnen, etwa bei "Connection:". HTTP/2 und HTTP/3 übertragen Header-Namen immer in Kleinbuchstaben, was im Debug-Modus zu sehen ist. Intern werden sämtliche Header-Namen in Kleinbuchstaben normalisiert, damit HTTP/1.x und HTTP/2 oder HTTP/3 dieselbe Darstellung verwenden. Auf der anderen Seite werden sie unverändert gesendet. Deshalb kommt eine mit Binnenmajuskeln geschriebene HTTP/1.x-Anfrage mit kleingeschriebenen Header-Namen an.

Die erste leere Zeile beendet die Header. Oft wird von einem doppelten Zeilenumbruch gesprochen. Das ist ungenau, auch wenn ein doppelter Zeilenumbruch eine gültige Form einer Leerzeile ist.

HAProxy berücksichtigt diese komplexen Kombinationen beim Indizieren, Prüfen und Zählen der Header-Werte. Über ihre mögliche Schreibweise muss man sich daher keine Gedanken machen. Eine Anwendung sollte aber nicht als fehlerhaft gelten, nur weil sie ungewöhnliche, jedoch gültige Konstrukte verwendet.

Wichtiger Hinweis:

```text
Wie in RFC7231 vorgeschlagen, normalisiert HAProxy Header, indem es
Zeilenumbrüche innerhalb eines Headers durch LWS ersetzt und so
mehrzeilige Header zusammenführt. Das ist für eine korrekte Analyse
nötig und hilft weniger leistungsfähigen HTTP-Parsern, korrekt zu
arbeiten und sich nicht durch solche komplexen Konstrukte täuschen
zu lassen.
```

## 1.4. HTTP-Antwort {#section-1-4}

Eine HTTP-Antwort ähnelt einer HTTP-Anfrage stark. Beide heißen HTTP-Nachrichten. Als Beispiel dient folgende Antwort:

```text
Zeilen-  Inhalt
nummer
   1     HTTP/1.1 200 OK
   2     Content-length: 350
   3     Content-Type: text/html
```

Als Sonderfall unterstützt HTTP sogenannte Informationsantworten mit Statuscodes 1xx. Sie enthalten keinen Teil der eigentlichen Antwort, sondern dienen als Signalisierung, etwa um einen Client zum weiteren Senden seiner Anfrage aufzufordern. Bei einer Antwort mit Status 100 stehen die angeforderten Informationen in der nächsten folgenden Antwort, deren Status nicht 100 ist. Auf eine Anfrage können somit mehrere Antworten folgen. Das funktioniert nur mit aktiviertem Keep-Alive; 1xx-Nachrichten wurden mit HTTP/1.1 eingeführt. HAProxy kann diese Nachrichten korrekt weiterleiten und überspringen und verarbeitet nur die nächste Antwort mit einem anderen Status als 100. Sofern nicht ausdrücklich anders angegeben, werden diese Nachrichten weder protokolliert noch verändert. Status 101 bedeutet, dass das Protokoll auf derselben Verbindung wechselt. HAProxy muss dann wie nach CONNECT in den Tunnelmodus wechseln. Der Header Upgrade enthält zusätzliche Informationen zum neuen Protokoll.

### 1.4.1. Die Antwortzeile {#section-1-4-1}

Zeile 1 ist die Antwortzeile. Sie besteht immer aus 3 Feldern:

- einer Versionsangabe: HTTP/1.1
- einem Statuscode: 200
- einer Begründung: OK

Der Statuscode hat immer 3 Stellen. Die erste Ziffer bezeichnet die allgemeine Statusklasse:

- 1xx = zu überspringende Informationsnachricht, etwa 100 oder 101
- 2xx = OK, Inhalt folgt, etwa 200 oder 206
- 3xx = OK, kein Inhalt folgt, etwa 302 oder 304
- 4xx = vom Client verursachter Fehler, etwa 401, 403 oder 404
- 5xx = vom Server verursachter Fehler, etwa 500, 502 oder 503

Statuscodes über 599 dürfen nicht übertragen werden. Manche Implementierungen verwenden sie jedoch in Protokollen, um interne Zustände zu melden. Die genaue Bedeutung der Codes beschreibt RFC9110. HTTP/2 und neuere Versionen haben keine Versionsangabe und übermitteln den Statuscode im Pseudo-Header ":status".

Das Feld "reason" ist nur ein Hinweis und wird von Clients nicht ausgewertet. Es kann beliebigen Inhalt haben; üblich sind jedoch die etablierten Meldungen. Das Feld kann aus einem oder mehreren Wörtern bestehen, etwa "OK", "Found" oder "Authentication Required". Ab HTTP/2 existiert es nicht und wird nicht übertragen. Leitet HAProxy eine Antwort von HTTP/2 oder neuer an einen HTTP/1-Client weiter, erzeugt es ein solches übliches, zum Statuscode passendes Begründungsfeld.

HAProxy kann selbst folgende Statuscodes ausgeben:

```text
Code  Anlass / Grund
 200  Zugriff auf die Statistikseite und Antworten auf Überwachungsanfragen
 301  Weiterleitung, abhängig vom konfigurierten Code
 302  Weiterleitung, abhängig vom konfigurierten Code
 303  Weiterleitung, abhängig vom konfigurierten Code
 307  Weiterleitung, abhängig vom konfigurierten Code
 308  Weiterleitung, abhängig vom konfigurierten Code
 400  Ungültige oder zu große Anfrage
 401  Die Aktion erfordert eine Authentifizierung, etwa beim Zugriff
      auf die Statistikseite.
 403  Eine Regel "http-request deny" verbietet die Anfrage.
 404  Die angeforderte Ressource wurde nicht gefunden.
 408  Die Zeitüberschreitung für Anfragen tritt ein, bevor die Anfrage
      vollständig ist.
 410  Die angeforderte Ressource ist nicht mehr verfügbar und wird
      auch künftig nicht mehr verfügbar sein.
 413  Eine HTTP/1.0-Anfrage mit GET/HEAD/DELETE enthält Nutzdaten;
      siehe auch "h1-accept-payload-with-any-method".
 500  HAProxy hat einen nicht behebbaren internen Fehler festgestellt,
      etwa eine fehlgeschlagene Speicherreservierung. Dies sollte
      niemals vorkommen.
 501  HAProxy kann eine Client-Anfrage wegen einer nicht unterstützten
      Funktion nicht erfüllen.
 502  Der Server liefert eine leere, ungültige oder unvollständige
      Antwort, oder eine Regel "http-response deny" blockiert sie.
 503  Kein Server konnte die Anfrage bearbeiten, oder eine
      Überwachungsanfrage erfüllt die Bedingung "monitor fail".
 504  Die Zeitüberschreitung für Antworten tritt ein, bevor der
      Server antwortet.
```

Die oben aufgeführten Fehlercodes 4xx und 5xx lassen sich anpassen; siehe "errorloc" in [Abschnitt 4.2](/de/haproxy/proxies/#section-4-2). Andere Statuscodes können gezielt durch bestimmte Aktionen ausgegeben werden, etwa "deny", "return" und "redirect" in [Abschnitt 4.3](/de/haproxy/proxies/#section-4-3).

### 1.4.2. Die Antwort-Header {#section-1-4-2}

Antwort-Header funktionieren genauso wie Anfrage-Header. HAProxy verwendet daher dieselbe Analysefunktion für beide. Einzelheiten stehen in Abschnitt 1.3.2.
