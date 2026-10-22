---
title: "Standardfunktionen"
linkTitle: "Standardfunktionen"
weight: 50
description: "Sample-Abrufe, Maps, ACLs, inhaltsabhängige Weiterleitung, Stick Tables, Umschreiben und Serverschutz"
icon: fa-solid fa-sliders
module: [HAPROXY]
categories: [Konzept]
aliases:
  - /haproxy/intro/standard-features/
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
upstream_name: "HAProxy 3.4 Starter Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, sections 3.4–3.4.8"
---

Dieser Abschnitt stellt einige Funktionen vor, die in HAProxy sehr häufig verwendet werden, aber nicht unbedingt in anderen Load-Balancern vorhanden sind.

## 3.4.1. Standardfunktionen: Informationen abrufen und konvertieren {#section-3-4-1}

HAProxy unterstützt den Abruf von Informationen mit zahlreichen „Sample-Abruffunktionen“. Dabei werden einzelne Informationen, sogenannte Samples, zur unmittelbaren Verwendung extrahiert. Dies dient der Sitzungsbindung, dem Aufbau von Bedingungen, der Ausgabe von Informationen in Protokollen oder der Ergänzung von HTTP-Headern.

Samples lassen sich aus verschiedenen Quellen abrufen:

- Konstanten: Ganzzahlen, Zeichenketten, IP-Adressen, Binärblöcke;

- dem Prozess: Datum, Umgebungsvariablen, Zustand von Server/Frontend/Backend/Prozess,
  Byte- und Verbindungszähler sowie -raten, Warteschlangenlänge, Zufallsgenerator, ...

- Variablen: Variablen je Sitzung, Anfrage oder Antwort;

- der Clientverbindung: Quell- und Zieladressen sowie -ports und alle zugehörigen
  Statistikzähler;

- der SSL-Clientsitzung: Protokoll, Version, Algorithmus, Cipher, Schlüssellänge, Sitzungs-ID,
  alle Felder der Client- und Serverzertifikate, Zertifikatsseriennummer, SNI, ALPN, NPN,
  Unterstützung bestimmter Erweiterungen durch den Client;

- dem Inhalt der Anfrage- und Antwortpuffer: beliebige Nutzdaten anhand von Offset und Länge,
  Datenlänge, RDP-Cookie, Dekodierung des SSL-Hello-Typs, Dekodierung von TLS-SNI;

- HTTP (Anfrage und Antwort): Methode, URI, Pfad, Query-String-Argumente, Statuscode,
  Header-Werte, Header-Wert an einer bestimmten Position, Cookies, erfasste Werte,
  Authentifizierung, Elemente des Nachrichtenkörpers;

Ein Sample kann anschließend mehrere Operatoren, sogenannte „Konverter“, zur Umwandlung durchlaufen. Ein Konverter nimmt ein Sample entgegen und erzeugt ein neues, möglicherweise mit einem völlig anderen Typ. Beispielsweise kann ein Konverter nur die ganzzahlige Länge der Eingabezeichenkette zurückgeben oder eine Zeichenkette in Großbuchstaben umwandeln. Vor der endgültigen Verwendung eines Samples lassen sich beliebig viele Konverter nacheinander anwenden. Von den verfügbaren Sample-Konvertern werden folgende besonders häufig verwendet:

- Arithmetische und logische Operatoren ermöglichen komplexe Berechnungen mit den
  Eingabedaten, etwa Verhältnisse und Prozentsätze oder einfache Umrechnungen zwischen Einheiten;

- IP-Adressmasken sind nützlich, um Adressen zu größeren Netzen zusammenzufassen;

- Datendarstellung: URL-Dekodierung, base64, hex, JSON-Zeichenketten, Hashing;

- Zeichenkettenumwandlung: Teilzeichenketten an festen Positionen und mit fester Länge
  extrahieren, bestimmte Felder anhand von Trennzeichen oder bestimmte Wörter extrahieren,
  Groß-/Kleinschreibung ändern, Ersetzungen anhand regulärer Ausdrücke vornehmen;

- Datumsumwandlung: in das HTTP-Datumsformat konvertieren, Ortszeit in UTC umrechnen und
  umgekehrt, einen Offset addieren oder subtrahieren;

- einen Eintrag in einer Stick Table nachschlagen, um Statistiken oder den zugewiesenen
  Server zu ermitteln;

- einen Schlüssel anhand einer Map-Datei in einen Wert umwandeln (vor allem für Geolokalisierung).

## 3.4.2. Standardfunktionen: Maps {#section-3-4-2}

Maps sind leistungsfähige Konverter: Beim Start wird eine Datei mit zwei Spalten in den Speicher geladen. Anschließend wird jedes Eingabe-Sample in der ersten Spalte gesucht. Wird der Eintrag gefunden, liefert die Map das zugehörige Muster aus der zweiten Spalte, andernfalls einen Standardwert. Die Ausgabe ist ebenfalls ein Sample und lässt sich daher weiter umwandeln, auch durch zusätzliche Map-Abfragen. Maps werden am häufigsten eingesetzt, um die IP-Adresse eines Clients einer AS-Nummer oder einem Ländercode zuzuordnen, da sie für Netzwerkadressen die längste Übereinstimmung unterstützen. Sie lassen sich aber auch für zahlreiche andere Zwecke verwenden.

Eine ihrer Stärken ist die Aktualisierbarkeit im laufenden Betrieb: über die CLI oder über bestimmte Aktionen, die andere Samples verwenden. Damit können Maps Informationen zwischen aufeinanderfolgenden Zugriffen speichern und wieder abrufen. Eine weitere Stärke ist die Indexierung mit Binärbäumen. Dadurch bleiben sie selbst mit Hunderttausenden von Einträgen äußerst schnell, sodass sich Geolokalisierung mit geringem Aufwand und Ressourcenbedarf einrichten lässt.

## 3.4.3. Standardfunktionen: ACLs und Bedingungen {#section-3-4-3}

Die meisten Vorgänge in HAProxy können an Bedingungen geknüpft werden. Bedingungen entstehen durch Verknüpfen mehrerer ACLs mit logischen Operatoren (AND, OR, NOT). Jede ACL besteht aus einer Reihe von Prüfungen mit folgenden Elementen:

- einer Sample-Abrufmethode, die das zu prüfende Element abruft;

- einer optionalen Folge von Konvertern, die das Element umwandeln;

- einer Liste von Mustern für den Abgleich;

- einer Abgleichmethode, die festlegt, wie die Muster mit dem Sample verglichen werden

Beispielsweise kann das Sample aus dem HTTP-Header "Host" stammen, dann in Kleinbuchstaben umgewandelt und schließlich mit der Methode für reguläre Ausdrücke gegen mehrere entsprechende Muster geprüft werden.

Technisch basieren ACLs und Maps auf demselben Kern. Sie verwenden genau dieselbe interne Struktur und dieselben Musterabgleichmethoden und bieten dieselbe Leistung. Der einzige wesentliche Unterschied ist, dass ACLs statt eines Samples lediglich „gefunden“ oder „nicht gefunden“ zurückgeben. ACL-Muster können direkt in der Konfigurationsdatei angegeben werden und benötigen keine eigene Datei. ACLs lassen sich benennen, um ihre Verwendung zu vereinfachen oder Konfigurationen verständlicher zu machen. Eine benannte ACL kann mehrmals definiert werden; ihre Definitionen werden nacheinander ausgewertet, bis eine davon zutrifft.

Es stehen etwa 13 verschiedene Musterabgleichmethoden bereit, darunter IP-Adressmasken, Ganzzahlbereiche, Teilzeichenketten und reguläre Ausdrücke. Sie arbeiten wie Funktionen. Wie in einer Programmiersprache wird nur das Nötige ausgewertet: Ist eine mit OR verknüpfte Bedingung bereits wahr, werden die folgenden nicht mehr ausgewertet. Ist eine mit AND verknüpfte Bedingung bereits falsch, wird der Rest der Bedingung ebenfalls nicht mehr ausgewertet.

Die Anzahl definierter ACLs ist praktisch unbegrenzt; einige häufig verwendete ACLs sind bereits vorgegeben. Die Erfahrung zeigt jedoch, dass die Fehlerbehebung bei Konfigurationen mit vielen benannten ACLs recht schwierig ist. Mitunter sind anonyme, direkt angegebene ACLs einfacher, weil weniger Verweise außerhalb des gerade untersuchten Abschnitts verfolgt werden müssen.

## 3.4.4. Standardfunktionen: Inhaltsabhängige Weiterleitung {#section-3-4-4}

HAProxy unterstützt einen Mechanismus zur inhaltsabhängigen Weiterleitung. Eine Verbindung oder Anfrage trifft an einem Frontend ein, und die darin enthaltenen Informationen werden verarbeitet. Mit ACL-basierten Bedingungen lässt sich anhand dieser Informationen entscheiden, welches Backend die Anfrage bearbeitet. Der Datenverkehr wird somit je nach Anfrageinhalt an das eine oder andere Backend geleitet. Am häufigsten wird anhand des Host-Headers und/oder von Pfadbestandteilen (Unterverzeichnissen oder Dateiendungen) entschieden, ob eine HTTP-Anfrage ein statisches Objekt oder die Anwendung betrifft. Zugriffe auf statische Objekte gehen an ein Backend mit schnellen, schlanken Servern, alle übrigen an einen komplexeren Anwendungsserver. So entsteht eine fein abgestufte Lösung für virtuelles Hosting. Damit können mehrere Technologien bequem innerhalb einer Gesamtlösung zusammenarbeiten.

Ein weiterer Anwendungsfall der inhaltsabhängigen Weiterleitung ist die Wahl verschiedener Lastverteilungsalgorithmen anhand unterschiedlicher Kriterien. Ein Cache kann beispielsweise einen URI-Hash verwenden, während eine Anwendung Round-Robin nutzt.

Außerdem können mehrere Kunden jeweils einen kleinen Anteil einer gemeinsamen Ressource nutzen, indem Verbindungsgrenzen je Backend und damit je Kunde durchgesetzt werden.

Regeln zur inhaltsabhängigen Weiterleitung skalieren sehr gut, wobei ihre Leistung von Anzahl und Komplexität der verwendeten ACLs abhängen kann. Es lassen sich aber auch dynamische Regeln schreiben, bei denen ein Sample-Wert unmittelbar zum Backend-Namen wird und überhaupt keine ACLs nötig sind. Solche Konfigurationen funktionieren Berichten zufolge im Produktivbetrieb mit mindestens 300000 Backends problemlos.

## 3.4.5. Standardfunktionen: Stick Tables {#section-3-4-5}

Stick Tables speichern üblicherweise Informationen zur Sitzungsbindung, also einen Verweis auf den Server, an den ein bestimmter Besucher geleitet wurde. Als Schlüssel dient die dem Besucher zugeordnete Kennung (seine Quelladresse, die SSL-ID der Verbindung, ein HTTP- oder RDP-Cookie, die aus der URL oder den Nutzdaten extrahierte Kundennummer, ...). Der gespeicherte Wert ist die Kennung des Servers.

Stick Tables können 3 verschiedene Sample-Typen als Schlüssel verwenden: Ganzzahlen, Zeichenketten und Adressen. In einem Proxy kann nur eine Stick Table referenziert werden; sie wird überall mit dem Namen des Proxys bezeichnet. Bis zu 8 Schlüssel lassen sich parallel verfolgen. Die Serverkennung wird während der Verarbeitung der Anfrage oder Antwort eingetragen, sobald sowohl Schlüssel als auch Server bekannt sind.

Der Inhalt einer Stick Table kann im Aktiv/Aktiv-Betrieb mit anderen HAProxy-Knoten, den sogenannten „Peers“, sowie beim Neuladen mit dem neuen Prozess repliziert werden. Dadurch verfügen alle Lastverteilungsknoten über dieselben Informationen und treffen dieselbe Weiterleitungsentscheidung, wenn die Anfragen eines Clients auf mehrere Knoten verteilt werden.

Da Stick Tables nach einem Merkmal zur Erkennung des Clients indiziert sind, speichern sie oft zusätzliche Informationen, etwa Statistiken je Client. Diese zusätzlichen Statistiken benötigen weiteren Speicherplatz und müssen ausdrücklich deklariert werden. Gespeichert werden können beispielsweise ein- und ausgehende Bandbreite, Anzahl gleichzeitiger Verbindungen, Verbindungsrate und -anzahl innerhalb eines Zeitraums, Anzahl und Häufigkeit von Fehlern sowie bestimmte Markierungen und Zähler. Damit solche Informationen ohne Bindung an einen bestimmten Server geführt werden können, gibt es eine spezielle Funktion zur Nachverfolgung. Sie verfolgt unabhängig von den Regeln zur Sitzungsbindung bis zu 3 Schlüssel aus verschiedenen Tabellen gleichzeitig. Jede gespeicherte Statistik lässt sich über die CLI suchen, ausgeben und löschen. Dies erweitert die Möglichkeiten zur Fehlerbehebung im laufenden Betrieb.

Mit diesem Mechanismus können wiederkehrende Besucher bevorzugt oder die bereitgestellte Dienstqualität an gutes oder schlechtes Verhalten angepasst werden. Meist dient er jedoch der Bekämpfung von Dienstmissbrauch und allgemein von DDoS-Angriffen, da sich damit komplexe Modelle erstellen lassen, die bestimmtes Fehlverhalten mit hoher Verarbeitungsgeschwindigkeit erkennen.

## 3.4.6. Standardfunktionen: Formatierte Zeichenketten {#section-3-4-6}

HAProxy muss an vielen Stellen Zeichenketten verarbeiten, etwa in Protokollen, Weiterleitungen oder beim Hinzufügen von Headern. Für größtmögliche Flexibilität wurden formatierte Zeichenketten eingeführt, ursprünglich für die Protokollierung. Daher heißen sie weiterhin "log-format". Diese Zeichenketten enthalten Escape-Zeichen, über die sich verschiedene dynamische Daten wie Variablen und Sample-Abrufausdrücke einfügen lassen. Auch die Kodierung kann beim Umwandeln des Ergebnisses in eine Zeichenkette angepasst werden, etwa durch Hinzufügen von Anführungszeichen. Damit lassen sich Header-Inhalte, Antwortdaten und sogar Antwortvorlagen erzeugen oder Protokollzeilen anpassen. Damit häufig benötigte Zeichenketten einfach aufgebaut werden können, stehen außerdem etwa 50 spezielle Kürzel für oft protokollierte Informationen bereit.

## 3.4.7. Standardfunktionen: HTTP-Umschreiben und -Weiterleiten {#section-3-4-7}

Einen Load-Balancer vor eine dafür nicht vorgesehene Anwendung zu setzen, kann ohne geeignete Werkzeuge schwierig sein. Häufig müssen Anfrage- und Antwort-Header angepasst werden, damit der Load-Balancer als Ursprungsserver erscheint und fest codierte Angaben korrigiert werden. Dazu gehören Änderungen am Anfragepfad (von denen dringend abgeraten wird), am Host-Header-Feld, am Location-Header-Feld von Weiterleitungsantworten sowie an den Attributen für Pfad und Domain von Cookies. Manche Server geben in ihren Antworten auch zu viele Informationen preis und werden dadurch anfälliger für gezielte Angriffe. Theoretisch ist es zwar nicht Aufgabe eines Load-Balancers, dies zu bereinigen; praktisch befindet er sich jedoch an der günstigsten Stelle der Infrastruktur, um eine vollständige Bereinigung sicherzustellen.

Gelegentlich muss der Load-Balancer auch Anfragen abfangen und mit einer Weiterleitung an eine neue Ziel-URL beantworten. Weiterleiten und Umschreiben werden zwar mitunter verwechselt, sind aber völlig unterschiedliche Konzepte: Beim Umschreiben sehen Client und Server unterschiedliche Inhalte und sind sich über den Ort der besuchten Seite uneinig. Eine Weiterleitung fordert den Client dagegen auf, die neue URL aufzurufen, sodass er denselben Ort wie der Server sieht.

HAProxy bietet dafür verschiedene Möglichkeiten zum Umschreiben und Weiterleiten, darunter:

- Umschreiben von URLs und Headern in Anfragen und Antworten anhand regulärer Ausdrücke.
  Reguläre Ausdrücke sind das häufigste Werkzeug zum Ändern von Header-Werten, weil sie
  sich leicht handhaben lassen und gut verstanden werden;

- Header lassen sich auch anhand formatierter Zeichenketten anhängen, löschen oder ersetzen.
  Dadurch können Informationen wie der clientseitige TLS-Algorithmus und Cipher übermittelt werden;

- HTTP-Weiterleitungen können jeden 3xx-Code mit einer relativen, absoluten oder vollständig
  dynamischen URI (formatierte Zeichenkette) verwenden;

- HTTP-Weiterleitungen unterstützen zusätzliche Optionen, etwa das Setzen oder Löschen eines
  bestimmten Cookies, das Entfernen des Query-Strings oder das Ergänzen eines fehlenden Schrägstrichs;

- Eine leistungsfähige "return"-Direktive ermöglicht es, jeden Teil einer Antwort wie Status,
  Header oder Nachrichtenkörper mit dynamischen Inhalten oder sogar Vorlagendateien anzupassen.

- Alle Vorgänge unterstützen ACL-basierte Bedingungen;

## 3.4.8. Standardfunktionen: Serverschutz {#section-3-4-8}

HAProxy unternimmt viel, um die Verfügbarkeit von Diensten zu maximieren. Dazu schützt er Server umfassend vor Überlastung und Angriffen. Der erste und wichtigste Punkt ist, dass nur vollständige und gültige Anfragen an die Server weitergeleitet werden. Zum einen muss HAProxy die Protokollelemente finden, die er zur Synchronisierung mit dem Bytestrom benötigt. Zum anderen lässt sich erst bei einer vollständigen Anfrage feststellen, ob einzelne Elemente ihre Bedeutung verändern. Der unmittelbare Vorteil ist, dass die Server keinen ungültigen oder unvollständigen Anfragen ausgesetzt sind. Dies schützt sehr wirksam vor Slowloris-Angriffen, die auf HAProxy fast keine Auswirkungen haben.

Ein weiterer wichtiger Punkt sind die Puffer für Anfragen und Antworten in HAProxy. Eine Anfrage wird erst dann an den Server gesendet, wenn sie vollständig vorliegt; die gesamte Antwort wird sehr schnell aus dem lokalen Netzwerk gelesen. Dadurch wird die serverseitige Verbindung nur sehr kurz genutzt, was die Serverressourcen möglichst weitgehend schont.

Darauf aufbauend kann HAProxy die Zahl gleichzeitiger Verbindungen oder ausstehender Anfragen an einen Server gezielt begrenzen. So wird der Server nie überlastet, selbst wenn er bei Verkehrsspitzen durchgehend mit 100% seiner Kapazität arbeitet. Überschüssige Anfragen warten einfach in einer Warteschlange, bis ein Platz frei wird. Diese erhebliche Ressourcenersparnis verkürzt die Antwortzeiten meist so stark, dass die Verarbeitung letztlich tatsächlich schneller ist als bei Überlastung des Servers. Wartende Anfragen können an andere Server umverteilt oder bereits in der Warteschlange abgebrochen werden, wenn der Client abbricht. Dies schützt die Server auch vor dem „Neuladeeffekt“: Klickt ein Besucher bei einer langsam ladenden Seite auf „Neu laden“, entsteht gewöhnlich bei jedem Klick eine weitere Anfrage, die den Server im überlasteten Zustand hält.

Der Slow-Start-Mechanismus schützt außerdem neu startende Server vor hohem Verkehrsaufkommen, solange sie noch ihren Start abschließen oder Klassen kompilieren.

Für den Schutz auf Protokollebene kann der HTTP-Parser so gelockert werden, dass er nicht standardkonforme, aber harmlose Anfragen oder Antworten akzeptiert und sogar korrigiert. Fehlerhafte Anwendungen bleiben dadurch erreichbar, während eine Korrektur entwickelt wird. Gleichzeitig werden die betreffenden Nachrichten vollständig erfasst und mit einem ausführlichen Bericht versehen, der Entwicklern hilft, den Fehler in der Anwendung zu finden. Die gefährlichsten Protokollverstöße werden zuverlässig erkannt, behandelt und behoben. So werden fehlerhafte Anfragen oder Antworten mit zwei Content-length-Headern korrigiert, wenn deren Werte exakt übereinstimmen. Unterscheiden sie sich, werden die Nachrichten abgewiesen, da daraus ein Sicherheitsproblem entsteht. Die Protokollprüfung ist nicht auf HTTP beschränkt, sondern auch für andere Protokolle wie TLS oder RDP verfügbar.

Wird ein Protokollverstoß oder ein Angriff erkannt, gibt es verschiedene Reaktionsmöglichkeiten: die übliche Antwort "HTTP 400 bad request", das Schließen der Verbindung mit einem TCP-Reset oder das Vortäuschen eines Fehlers nach langer Verzögerung ("tarpit"), um den Angreifer zu verwirren. All dies schützt die Server, weil der angreifende Client von einem Angriff abgehalten wird, dessen Fortsetzung sehr aufwendig wird.

HAProxy bietet außerdem weitergehende Möglichkeiten zum Schutz vor versehentlichen Datenlecks und der Vermischung von Sitzungen. Er kann verdächtige Serverantworten protokollieren und protokolliert außerdem Antworten, die die Vertraulichkeit eines Besuchers beeinträchtigen könnten; optional kann er sie auch blockieren. Ein Beispiel ist ein zwischenspeicherbares Cookie in einer zwischenspeicherbaren Antwort. Ein zwischengeschalteter Cache könnte es an einen anderen Besucher ausliefern, sodass beide versehentlich dieselbe Sitzung verwenden.
