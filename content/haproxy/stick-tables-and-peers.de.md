---
title: "11. Stick Tables und Peers"
linkTitle: "11. Stick Tables und Peers"
weight: 220
description: "Speicherung in Stick Tables und Deklaration der Peer-Replikation"
icon: fa-solid fa-table
module: [HAPROXY]
categories: [Referenz]
aliases:
  - /haproxy/configuration/stick-tables-and-peers/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 11"
---

Stick Tables verknüpfen in HAProxy Informationen und Metriken mit einem Schlüssel eines bestimmten Typs. Diese Zuordnung bleibt nach der letzten Aktualisierung für eine bestimmte Dauer bestehen. Man kann sich darunter eine Tabellenzeile mit mehreren Spalten vorstellen: Der Schlüsselwert bestimmt die Zeilennummer, und jede Spalte steht für ein eigenes Kriterium.

Ursprünglich dienten Stick Tables dazu, die Zuordnung von Clients zu Servern zu speichern und damit persistente Sitzungen zwischen ihnen zu erhalten. Ein Client stellte eine Verbindung her oder sendete eine Anfrage und wurde anhand eines Merkmals wie Quelladresse, Cookie oder URL-Parameter identifiziert. Der ausgewählte Server wurde zusammen mit diesem Merkmal für eine konfigurierbare Dauer in einer Stick Table gespeichert. Spätere Zugriffe desselben Clients konnten so automatisch zu dem Server gelangen, auf dem seine Anwendungssitzung bestand.

Heute können Stick Tables mehr als nur eine Servernummer speichern. Dazu gehören Aktivitätsmetriken eines bestimmten Clients, etwa Anzahl und Rate von Anfragen, Verbindungen oder Bytes, sowie beliebige Ereigniszähler ("gpc", allgemeine Zähler) und Markierungen zur Kennzeichnung bestimmter Client-Eigenschaften ("gpt", allgemeine Markierung).

Auf Stick Tables können die "stick"-Direktiven zur Zuordnung von Clients zu Servern zugreifen. Die "track-sc"-Regeln legen fest, welcher Schlüssel in welcher Tabelle zur Erfassung von Metriken verfolgt wird. Außerdem können zahlreiche Sample-Abruffunktionen und Konverter einen Schlüssel unmittelbar nachschlagen, um bestimmte Metriken oder Daten abzurufen. Grundsätzlich frischen Tabellenaktualisierungen (gpt/gpc/metrics) und Abfragen der Serverzuordnung den betroffenen Eintrag auf und verschieben seinen Ablaufzeitpunkt. Reine Abfragen durch Sample-Abruffunktionen und Konverter lesen dagegen nur die Daten aus, ohne den Ablaufzeitpunkt zu verschieben.

Damit der Mechanismus skaliert und das Neuladen von HAProxy sowie Failover übersteht, können Aktualisierungen von Stick Tables über den in [Abschnitt 11.2](/de/haproxy/stick-tables-and-peers/#section-11-2) beschriebenen "Peers"-Mechanismus mit anderen Knoten, den "peers", ausgetauscht werden. Zur Feinabstimmung dieser Kommunikation lässt sich auch festlegen, dass bestimmte Tabellen nur Informationen von Peers empfangen oder dass Aktualisierungen von Peers an eine andere Tabelle weitergeleitet werden.

Stick Tables lassen sich in Proxy-Abschnitten (Frontends und Backends) mit "stick-table" deklarieren. Pro Abschnitt ist nur eine Tabelle möglich; sie erhält den Namen des Abschnitts. In Peers-Abschnitten dient dazu "table", gefolgt vom Tabellennamen. Damit können mehrere Stick Tables im selben "peers"-Abschnitt deklariert werden. Werden mehrere Tabellen benötigt, empfiehlt sich in der Regel die Deklaration in einem Peers-Abschnitt, wenn sie gemeinsam genutzt werden sollen. Andernfalls können zusätzliche Backend-Abschnitte angelegt werden, die jeweils nur die "stick-table"-Definition enthalten.

## 11.1. stick-table deklarieren {#section-11-1}

Die Deklaration einer Stick Table in einem Proxy-Abschnitt ("frontend", "backend", "listen") ähnelt der in einem "peers"-Abschnitt. Der Unterschied: Im Peers-Abschnitt ist ein Name erforderlich, und die Option "peers" entfällt.

In einem "frontend"-, "backend"- oder "listen"-Abschnitt:

stick-table type `<type>` size `<size>` [expire `<expire>`] [nopurge] [recv-only] [write-to
`<wtable>`] [srvkey `<srvkey>`] [store `<data_type>`]\* [brates-factor `<factor>`] [peers
`<peersect>`]

In einem "peers"-Abschnitt:

table `<name>` type `<type>` size `<size>` [expire `<expire>`] [nopurge] [recv-only]
[write-to `<wtable>`] [srvkey `<srvkey>`] [store `<data_type>`]\* [brates-factor `<factor>`]

Argumente, zunächst die Pflichtargumente, danach alphabetisch sortiert:

- type `<type>` Dieses Pflichtargument legt den Schlüsseltyp auf `<type>` fest. Er besteht
  meist aus einem einzelnen Wort, kann aber auch eigene Argumente haben:

  - ip Dieser Typ sollte zugunsten eines eindeutigen Typs wie "ipv4" oder "ipv6" vermieden
    werden. Vor Version 3.2 war er die einzige Möglichkeit, IPv4 zu konfigurieren. In 3.2 ist
    "ip" ein Alias für "ipv4"; "ipv4" wird bevorzugt. In einer künftigen Version wird "ip"
    stattdessen "ipv6" entsprechen. Der Typ soll lediglich den Übergang von Versionen vor
    3.2 zu Versionen nach 3.2 erleichtern.

  - ipv4 Eine so deklarierte Tabelle speichert ausschließlich IPv4-Adressen. Diese Form
    benötigt wenig Speicher, etwa 50 Bytes pro Eintrag, und ermöglicht sehr schnelle
    Such- und Speichervorgänge mit fast keinem Zusatzaufwand. Sie wird hauptsächlich
    zum Speichern der Quell-IP-Adressen von Clients verwendet.

  - ipv6 Eine mit "type ipv6" deklarierte Tabelle speichert ausschließlich IPv6-Adressen.
    Diese Form benötigt wenig Speicher, etwa 60 Bytes pro Eintrag, und ermöglicht sehr
    schnelle Such- und Speichervorgänge mit fast keinem Zusatzaufwand. Sie wird
    hauptsächlich zum Speichern der Quell-IP-Adressen von Clients verwendet.

  - integer Eine mit "type integer" deklarierte Tabelle speichert 32bit-Ganzzahlen, die
    beispielsweise eine Client-Kennung aus einer Anfrage darstellen können.

  - string [len `<len>`] Eine mit "type string" deklarierte Tabelle speichert Teilzeichenketten
    mit bis zu `<len>` Zeichen. Liefert die Musterextraktion eine längere Zeichenkette als
    `<len>`, wird sie vor dem Speichern gekürzt. Beim Abgleich werden höchstens `<len>`
    Zeichen der gespeicherten Zeichenkette mit dem extrahierten Muster verglichen.
    Ohne Angabe gilt eine Grenze von 32 Zeichen. Eine größere Länge kann den
    Speicherbedarf erheblich erhöhen.

  - binary [len `<len>`] Eine mit "type binary" deklarierte Tabelle speichert Binärblöcke mit
    `<len>` Bytes. Liefert die Musterextraktion einen längeren Block als `<len>`, wird er vor
    dem Speichern gekürzt. Liefert der Sample-Ausdruck einen kürzeren Block als `<len>`,
    wird er mit 0 aufgefüllt. Ohne Angabe gilt eine Grenze von 32 Bytes. Eine größere
    Länge kann den Speicherbedarf erheblich erhöhen.

- size `<size>` Dieses Pflichtargument legt die maximale Anzahl der Tabelleneinträge auf
  `<size>` fest und beeinflusst den Speicherbedarf unmittelbar. Pro Eintrag sind etwa
  50 Bytes zusätzlich zur oben angegebenen Schlüsselgröße, den optional gespeicherten
  Metriken und gegebenenfalls der Zeichenkette einzuplanen. Die Suffixe "k", "m", "g"
  stehen für die Faktoren 2^10, 2^20 und 2^30.

- expire `<delay>` Legt die maximale Lebensdauer eines Eintrags seit seiner letzten
  Erstellung, Auffrischung durch 'track-sc' oder einem Treffer durch 'stick match' oder
  'stick on' fest. Die Ablaufdauer `<delay>` verwendet wie die verschiedenen
  Zeitüberschreitungen das Standardzeitformat, standardmäßig Millisekunden.
  Die Höchstdauer liegt knapp über 24 Tagen. Einzelheiten stehen in
  [Abschnitt 2.5](/de/haproxy/configuration-basics/#section-2-5). Ohne Angabe laufen Sitzungen
  nicht automatisch ab. Ist die Tabelle voll, werden beim Anlegen neuer Einträge jedoch
  die ältesten entfernt. Ohne Ablaufdauer darf "nopurge" daher nicht verwendet werden.
  Hinweis: 'table\_\*'-Konverter schlagen Einträge nach, verschieben aber deren
  Ablaufzeitpunkt nicht, da sie kein 'track-sc' benötigen.

- brates-factor `<factor>` Legt einen Faktor für die Rate eingehender und ausgehender Bytes
  fest. Statt einzelner Bytes werden Byte-Blöcke gezählt. Intern verwenden Raten
  32-Bit-Zähler und sind daher auf etwa 4 Milliarden pro Zeitraum begrenzt. Mit diesem
  Parameter können Raten die Grenze von 4G innerhalb des festgelegten Zeitraums
  überschreiten. Der Faktor muss größer als 0 und kleiner oder gleich 1024 sein.

- nopurge verhindert, dass bei voller Tabelle ältere Einträge gelöscht werden. Ohne diese
  Option entfernt HAProxy beim Speichern in einer vollen Tabelle einige der ältesten
  Einträge, um Platz für neue zu schaffen. Das ist meist das gewünschte Verhalten.
  In bestimmten Fällen ist es jedoch sinnvoll, neue Einträge abzulehnen und die alten
  zu behalten. Das kann etwa zutreffen, wenn die Datenmenge die Hardware-Kapazität
  weit übersteigt und neuen Clients lieber der Zugriff verweigert werden soll als
  bereits verbundenen. Bei Verwendung dieses Parameters muss "expire" richtig
  eingestellt werden; siehe oben.

- recv-only gibt an, dass die Tabelle ausschließlich zum Abrufen der gewünschten Daten
  von einem entfernten Peer und nicht für eigene Aktualisierungen verwendet werden
  soll. Das Schlüsselwort ermöglicht den Abruf rein lokaler Werte wie "conn_cur".
  Diese werden standardmäßig nicht übernommen, da sie mit den Änderungen des
  lokalen Peers an der Tabelle kollidieren würden. Die Option ist nur für Tabellen
  sinnvoll, die weder in Tracking-Regeln noch in Verfahren zur Tabellenaktualisierung
  verwendet werden; einfacher gesagt: für entfernte Tabellen, aus denen nur
  Informationen abgerufen werden.

- peers `<peersect>` Neu angelegte, aktualisierte oder aufgefrischte Einträge werden zur
  Synchronisierung an die Peers im Abschnitt `<peersect>` gesendet. Von diesen Peers
  übernommene Schlüssel werden ebenfalls in der Tabelle eingefügt oder aktualisiert.
  Beim Start kann außerdem versucht werden, Einträge von einer älteren Prozessinstanz
  zu übernehmen, die über diesen Abschnitt als lokaler Peer bezeichnet wird.

- srvkey `<srvkey>` Legt fest, wie die einzelnen Server für die Stick Table identifiziert
  werden. Gültig sind "name" und "addr". Bei "name" wird das Serverargument `<name>`
  verwendet, das auch aus einer Vorlage stammen kann. Bei "addr" dient die aktuelle
  Netzwerkadresse einschließlich Port als Kennung. "addr" ist besonders nützlich,
  wenn die Serveradressen für über Peers abgeglichene Stick Tables durch
  Diensterkennung erzeugt werden und ein Zuordnungstoken bei allen Peers
  zuverlässig denselben Host bezeichnen soll.

- store `<data_type>` Speichert zusätzliche Informationen in der Stick Table. ACLs können
  damit verschiedene Kriterien zur Aktivität des Clients prüfen, der dem Eintrag in
  der Stick Table entspricht. Jeder hier angegebene Datentyp vergrößert die Einträge
  um den Platz für die zusätzlichen Daten. Ein Eintrag kann mehrere Datentypen
  speichern. Dazu können nach "store" mehrere Typen als kommagetrennte Liste stehen.
  Alternativ lässt sich "store" mit jeweils einem oder mehreren Datentypen wiederholen.
  Alle zu speichernden Datentypen müssen ausdrücklich deklariert werden; nur
  "server_id" wird automatisch erkannt und aktiviert. Verweist eine ACL auf einen
  nicht gespeicherten Datentyp, trifft sie nicht zu. Einige Typen benötigen ein
  Argument, das unmittelbar nach dem Typ in runden Klammern stehen muss.
  Die unterstützten Typen und ihre Argumente sind unten aufgeführt.

- write-to `<wtable>` Gibt eine weitere Stick Table an, in die Aktualisierungen von Peers
  zusätzlich zur Quelltabelle geschrieben werden. `<wtable>` muss denselben Typ und
  dieselbe Schlüssellänge wie die deklarierte Tabelle haben. Die Quelltabelle kann
  nicht selbst als Ziel dienen. Bei jeder über einen Peer empfangenen Aktualisierung
  versucht HAProxy, den zugehörigen Eintrag in `<wtable>` aufzufrischen. Fehlt er, wird
  er angelegt; andernfalls werden seine Werte und sein Timer aktualisiert. In
  `<wtable>` werden nur Typen wie server_id, server_key und gpt geschrieben, die nicht
  an arithmetischen Operationen beteiligt sind. So beeinflussen bereits verarbeitete
  Werte einer entfernten Tabelle nicht die Rechenoperationen in der lokalen
  Zieltabelle; etwa ein gemeinsam genutzter kumulativer Zähler würde sonst endlos
  anwachsen. Ein häufiger Einsatz ist die Verwendung von Zuordnungsregeln für
  Server-Persistenz in einem Peers-Cluster, da passende Schlüssel aus entfernten
  Tabellen übernommen werden.

Die folgenden Datentypen können über "store" mit einem Eintrag verknüpft werden. Werden viele Typen gespeichert, kann der Speicherbedarf erheblich steigen. Alle unten genannten Werte zusammen können Hunderte von Bytes je Eintrag benötigen, bei 1 Million Einträgen also Hunderte von MB. Deshalb steht der ungefähre Speicherbedarf jedes Typs in eckigen Klammern hinter dem Argument.

Argumente:

- bytes_in_cnt [8 bytes] Zählt die Bytes vom Client zum Server. Diese positive
  64-Bit-Ganzzahl enthält die Gesamtzahl der Bytes, die von Clients empfangen wurden,
  die diesem Eintrag entsprechen. Header zählen mit. Damit lässt sich der Missbrauch
  von Upload-Funktionen auf Foto- oder Videoservern begrenzen. Gemessen wird beim
  Eingang der Daten in HAProxy; die Komprimierung beeinflusst den Zähler daher nicht.

- bytes_in_rate(`<period>`) [12 bytes] Misst die Byte-Rate vom Client zum Server. Der
  ganzzahlige Parameter `<period>` gibt in Millisekunden an, über welchen Zeitraum
  der Mittelwert berechnet wird. Gemeldet wird die durchschnittliche Eingangsrate
  in Bytes pro Zeitraum. Damit lassen sich Benutzer erkennen, die zu viel und zu
  schnell hochladen. Warnung: Bei großen Uploads kann die gesamte Datenmenge erst
  bei deren Abschluss gezählt werden. Dadurch entstehen Spitzen in der mittleren
  Übertragungsgeschwindigkeit statt eines gleichmäßigen Verlaufs. "option contstats"
  kann dies teilweise glätten, allerdings nicht vollständig. Für eine gerechtere
  Bewertung wird byte_in_cnt empfohlen.

- bytes_out_cnt [8 bytes] Zählt die Bytes vom Server zum Client. Diese positive
  64-Bit-Ganzzahl enthält die Gesamtzahl der Bytes, die an Clients gesendet wurden,
  die diesem Eintrag entsprechen. Header zählen mit. Damit lässt sich Missbrauch
  durch Bots begrenzen, die die gesamte Website herunterladen. Gemessen wird beim
  Eingang der Daten in HAProxy; die Komprimierung beeinflusst den Zähler daher nicht.

- bytes_out_rate(`<period>`) [12 bytes] Misst die Byte-Rate vom Server zum Client. Der
  ganzzahlige Parameter `<period>` gibt in Millisekunden an, über welchen Zeitraum
  der Mittelwert berechnet wird. Gemeldet wird die durchschnittliche Ausgangsrate
  in Bytes pro Zeitraum. Damit lassen sich Benutzer erkennen, die zu viel und zu
  schnell herunterladen. Warnung: Bei großen Übertragungen kann die gesamte
  Datenmenge erst bei deren Abschluss gezählt werden. Dadurch entstehen Spitzen
  in der mittleren Übertragungsgeschwindigkeit statt eines gleichmäßigen Verlaufs.
  "option contstats" kann dies teilweise glätten, allerdings noch nicht vollständig.
  Für eine gerechtere Bewertung wird byte_out_cnt empfohlen.

- conn_cnt [4 bytes] Zählt die Verbindungen. Diese positive 32-Bit-Ganzzahl enthält die
  absolute Anzahl der Verbindungen, die von Clients eingegangen sind, die diesem
  Eintrag entsprechen. Sie müssen nicht angenommen worden sein; gezählt wird
  bereits ihr Eingang.

- conn_cur [4 bytes] Zählt die aktuellen Verbindungen. Diese positive 32-Bit-Ganzzahl
  enthält die Anzahl gleichzeitig bestehender Verbindungen für den Eintrag. Sobald
  eine eingehende Verbindung dem Eintrag entspricht, wird der Zähler erhöht; beim
  Ende der Verbindung wird er verringert. So lässt sich jederzeit die genaue Anzahl
  gleichzeitiger Verbindungen für einen Eintrag ermitteln. Der Wert wird
  standardmäßig nicht von anderen Peers übernommen: Er wäre nicht aussagekräftig,
  da er den lokalen Zähler ignorieren würde. Zusammen mit recv-only lässt sich
  damit jedoch die Anzahl gleichzeitiger Verbindungen anderer Peers übernehmen.

- conn_rate(`<period>`) [12 bytes] Misst die Verbindungshäufigkeit. Der ganzzahlige Parameter
  `<period>` gibt in Millisekunden an, über welchen Zeitraum der Mittelwert berechnet
  wird. Gemeldet wird die durchschnittliche Rate eingehender Verbindungen in
  Verbindungen pro Zeitraum. Das Ergebnis ist eine Ganzzahl, die sich mit ACLs
  prüfen lässt. Ob Verbindungen angenommen oder abgelehnt werden, beeinflusst
  die Messung nicht.

- glitch_cnt [4 bytes] Zählt Protokollauffälligkeiten auf Frontend-Verbindungen. Diese
  positive 32-Bit-Ganzzahl enthält die Gesamtzahl der auf einer Frontend-Verbindung
  gemeldeten Auffälligkeiten. Dabei handelt es sich um ungewöhnliche oder aus
  Protokollsicht unerwartete Client-Aktionen. Sie können auf einen stark fehlerhaften
  Client oder einen Angreifer hinweisen. Der Zähler kann helfen, in solchen Fällen
  über den Umgang mit dem Client zu entscheiden.

- glitch_rate(`<period>`) [12 bytes] Misst die Häufigkeit von Protokollauffälligkeiten. Der
  ganzzahlige Parameter `<period>` gibt in Millisekunden an, über welchen Zeitraum
  der Mittelwert berechnet wird. Gemeldet wird die durchschnittliche Rate von
  Auffälligkeiten auf Frontend-Verbindungen in diesem Zeitraum. Damit lassen sich
  fehlerhafte Clients oder mögliche Angreifer erkennen, die aus Protokollsicht
  ungewöhnliche oder unerwartete Aktionen ausführen, sofern HAProxy diese
  entsprechend gekennzeichnet hat.

- gpc(`<nb>`) [4 \* `<nb>` bytes] Ist ein Array aus `<nb>` allgemeinen Zählern. Die positiven
  32-Bit-Ganzzahlen können beliebige Werte zählen. Meist werden sie als fortlaufende
  Zähler für bestimmte Einträge verwendet, etwa um das Erreichen einer Grenze
  festzuhalten und Aktionen auszulösen. Das Array ist auf 100 Elemente begrenzt,
  gpc0 bis gpc99, damit eine erzeugte Peer-Aktualisierungsnachricht in den Puffer
  passt. Es sollte berücksichtigt werden, dass viele Zähler die Datenmenge und die
  Last des Peers-Protokolls erhöhen: Jede Änderung eines Werts überträgt sämtliche
  Daten und Zähler. Dieser data_type schließt die älteren data_types 'gpc0' und
  'gpc1' in derselben Tabelle aus. Beim Array-data_type 'gpc' wirken alle auf
  'gpc0' und 'gpc1' bezogenen Sample-Abruffunktionen und Aktionen auf die
  ersten beiden Array-Elemente.

- gpc_rate(`<nb>`,`<period>`) [12 \* `<nb>` bytes] Ist ein Array mit den Erhöhungsraten
  allgemeiner Zähler über einen Zeitraum. Die Elemente sind positive
  32-Bit-Ganzzahlen zur freien Verwendung. Wie `<gpc>` zählen sie Ereignisse;
  statt einer Summe speichern sie jedoch die Rate, mit der der Zähler erhöht wird.
  Meist dient dies zur Messung der Häufigkeit bestimmter Ereignisse, etwa Anfragen
  an eine bestimmte URL. Das Array ist auf 100 Elemente begrenzt: gpc_rate(100,`<period>`)
  ermöglicht das Speichern von gpc0_rate bis gpc99_rate. So passt eine erzeugte
  Peer-Aktualisierungsnachricht in den Puffer. Das Array kann nicht weniger als
  1 Element enthalten; zum Speichern nur der Rate gpc0_rate dient gpc_rate(1,`<period>`).
  Es sollte berücksichtigt werden, dass viele Zähler die Datenmenge und die Last
  des Peers-Protokolls erhöhen: Jede Änderung eines Werts überträgt sämtliche
  Daten und Zähler. Dieser data_type schließt die älteren data_types 'gpc0_rate'
  und 'gpc1_rate' in derselben Tabelle aus. Beim Array-data_type 'gpc_rate'
  wirken alle auf 'gpc0' und 'gpc1' bezogenen Abruffunktionen und Aktionen
  auf die ersten beiden Array-Elemente.

- gpc0 [4 bytes] Ist der erste allgemeine Zähler, eine positive 32-Bit-Ganzzahl zur
  freien Verwendung. Meist dient er dazu, bestimmte Einträge zu markieren, etwa
  wenn ein Verhalten erkannt wurde, das bei späteren Abgleichen bekannt sein muss.

- gpc0_rate(`<period>`) [12 bytes] Ist die Erhöhungsrate des ersten allgemeinen Zählers
  über einen Zeitraum, eine positive 32-Bit-Ganzzahl zur freien Verwendung. Wie
  `<gpc0>` zählt sie Ereignisse, speichert jedoch statt einer Summe die Rate der
  Zählererhöhung. Meist dient dies zur Messung der Häufigkeit bestimmter Ereignisse,
  etwa Anfragen an eine bestimmte URL.

- gpc1 [4 bytes] Ist der zweite allgemeine Zähler, eine positive 32-Bit-Ganzzahl zur
  freien Verwendung. Meist dient er dazu, bestimmte Einträge zu markieren, etwa
  wenn ein Verhalten erkannt wurde, das bei späteren Abgleichen bekannt sein muss.

- gpc1_rate(`<period>`) [12 bytes] Ist die Erhöhungsrate des zweiten allgemeinen Zählers
  über einen Zeitraum, eine positive 32-Bit-Ganzzahl zur freien Verwendung. Wie
  `<gpc1>` zählt sie Ereignisse, speichert jedoch statt einer Summe die Rate der
  Zählererhöhung. Meist dient dies zur Messung der Häufigkeit bestimmter Ereignisse,
  etwa Anfragen an eine bestimmte URL.

- gpt(`<nb>`) [4 \* `<nb>` bytes] Ist ein Array aus `<nb>` allgemeinen Markierungen, jeweils
  positiven 32-Bit-Ganzzahlen zur freien Verwendung. Meist werden damit bestimmte
  Einträge markiert, etwa wenn ein Verhalten erkannt wurde, das bei späteren
  Abgleichen bekannt sein muss. Das Array ist auf 100 Elemente begrenzt:
  gpt(100) ermöglicht das Speichern von gpt0 bis gpt99. So passt eine erzeugte
  Peer-Aktualisierungsnachricht in den Puffer. Das Array kann nicht weniger als
  1 Element enthalten; zum Speichern nur der Markierung gpt0 dient gpt(1).
  Es sollte berücksichtigt werden, dass viele Zähler die Datenmenge und die Last
  des Peers-Protokolls erhöhen: Jede Änderung eines Werts überträgt sämtliche
  Daten und Zähler. Dieser data_type schließt den älteren data_type 'gpt0'
  in derselben Tabelle aus. Beim Array-data_type 'gpt' wirken alle auf 'gpt0'
  bezogenen Abruffunktionen und Aktionen auf das erste Array-Element.

- gpt0 [4 bytes] Ist die erste allgemeine Markierung, eine positive 32-Bit-Ganzzahl
  zur freien Verwendung. Meist dient sie dazu, bestimmte Einträge zu markieren,
  etwa wenn ein Verhalten erkannt wurde, das bei späteren Abgleichen bekannt
  sein muss.

- http_req_cnt [4 bytes] Zählt HTTP-Anfragen. Diese positive 32-Bit-Ganzzahl enthält
  die absolute Anzahl der HTTP-Anfragen von Clients, die diesem Eintrag
  entsprechen. Dabei spielt es keine Rolle, ob die Anfragen gültig sind.
  Bei clientseitigem Keep-Alive unterscheidet sich dieser Wert von der
  Anzahl der Sitzungen.

- http_req_rate(`<period>`) [12 bytes] Misst die Anfragehäufigkeit. Der ganzzahlige
  Parameter `<period>` gibt in Millisekunden an, über welchen Zeitraum der
  Mittelwert berechnet wird. Gemeldet wird die durchschnittliche HTTP-Anfragerate
  in Anfragen pro Zeitraum. Das Ergebnis ist eine Ganzzahl, die sich mit ACLs
  prüfen lässt. Dabei spielt es keine Rolle, ob die Anfragen gültig sind.
  Bei clientseitigem Keep-Alive unterscheidet sich dieser Wert von Sitzungen.

- http_err_cnt [4 bytes] Zählt Fehler bei HTTP-Anfragen. Diese positive
  32-Bit-Ganzzahl enthält die absolute Anzahl der HTTP-Anfragefehler, die von
  Clients verursacht wurden, die diesem Eintrag entsprechen. Als Fehler zählen
  ungültige oder abgeschnittene Anfragen, abgelehnte oder durch Tarpitting
  verzögerte Anfragen und fehlgeschlagene Authentifizierungen. Antwortet der
  Server mit 4xx, gilt die Anfrage ebenfalls als Fehler, da der Client ihn
  ausgelöst hat, etwa bei der Suche nach Schwachstellen.

- http_err_rate(`<period>`) [12 bytes] Misst die Häufigkeit von HTTP-Anfragen. Der
  ganzzahlige Parameter `<period>` gibt in Millisekunden an, über welchen Zeitraum
  der Mittelwert berechnet wird. Gemeldet wird die durchschnittliche Fehlerrate
  bei HTTP-Anfragen in Anfragen pro Zeitraum. Was als Fehler gilt, beschreibt
  http_err_cnt oben. Das Ergebnis ist eine Ganzzahl, die sich mit ACLs prüfen lässt.

- http_fail_cnt [4 bytes] Zählt fehlerhafte HTTP-Antworten. Diese positive
  32-Bit-Ganzzahl enthält die absolute Anzahl der von Servern verursachten
  HTTP-Antwortfehler, die diesem Eintrag entsprechen. Als Fehler zählen ungültige
  oder abgeschnittene Antworten sowie alle 5xx-Antworten außer 501 und 505.
  Der Zähler ist zur Erkennung von Dienstausfällen zusammen mit Pfad oder URI gedacht.

- http_fail_rate(`<period>`) [12 bytes] Misst die Häufigkeit fehlerhafter HTTP-Antworten.
  Der ganzzahlige Parameter `<period>` gibt in Millisekunden an, über welchen Zeitraum
  der Mittelwert berechnet wird. Gemeldet wird die durchschnittliche Fehlerrate
  bei HTTP-Antworten in Anfragen pro Zeitraum. Was als Fehler gilt, beschreibt
  http_fail_cnt oben. Das Ergebnis ist eine Ganzzahl, die sich mit ACLs prüfen lässt.

- server_id [4 bytes] Speichert als Ganzzahl die numerische ID des Servers, dem eine
  Anfrage zugewiesen wurde. Die Regeln "stick match", "stick store" und "stick on"
  verwenden diesen Wert; beim Verweis darauf wird er automatisch aktiviert.
  Die Serverzuordnung anhand gelernter Informationen unterliegt Einschränkungen:
  Insbesondere gehen alle gelernten Zuordnungen bei einem Neustart verloren,
  sofern Peers nicht richtig zur Übertragung dieser Informationen beim Neustart
  konfiguriert sind, was empfohlen wird. Als Ergänzung anderer Zuordnungsverfahren
  kann dieses Verfahren sinnvoll sein, als alleiniger Mechanismus jedoch nicht immer.

- sess_cnt [4 bytes] Zählt Sitzungen. Diese positive 32-Bit-Ganzzahl enthält die
  absolute Anzahl eingehender Sitzungen von Clients, die diesem Eintrag entsprechen.
  Eine Sitzung ist eine Verbindung, die von den Regeln auf Schicht 4
  ("tcp-request connection") angenommen wurde.

- sess_rate(`<period>`) [12 bytes] Misst die Sitzungshäufigkeit. Der ganzzahlige
  Parameter `<period>` gibt in Millisekunden an, über welchen Zeitraum der Mittelwert
  berechnet wird. Gemeldet wird die durchschnittliche Rate eingehender Sitzungen
  in Sitzungen pro Zeitraum. Das Ergebnis ist eine Ganzzahl, die sich mit ACLs
  prüfen lässt.

Beispiel:

```shell
# Keep track of counters of up to 1 million IP addresses over 5 minutes
# and store a general purpose counter and the average connection rate
# computed over a sliding window of 30 seconds.
stick-table type ip size 1m expire 5m store gpc0,conn_rate(30s)
```

Siehe auch "stick match", "stick on", "stick store-request", "track-sc", [Abschnitt 2.5](/de/haproxy/configuration-basics/#section-2-5) zum Zeitformat, [Abschnitt 11.2](/de/haproxy/stick-tables-and-peers/#section-11-2) zu Peers, [Abschnitt 9.7](/de/haproxy/filters/#section-9-7) zur Bandbreitenbegrenzung und [Abschnitt 7](/de/haproxy/acls-and-samples/) zu ACLs.

## 11.2. Peers deklarieren {#section-11-2}

Stick-Table-Einträge beliebiger Datentypen können über TCP-Verbindungen zwischen mehreren HAProxy-Instanzen nach dem Multi-Master-Prinzip verteilt werden. Jede Instanz sendet ihre lokalen Änderungen und neuen Einträge an entfernte Peers. Die übertragenen Werte überschreiben die entfernten Werte ohne Zusammenfassung.

Eine Ausnahme ist "conn_cur": Dieser Datentyp wird standardmäßig nie von Peers übernommen, da er lokale Werte abbilden soll. Frühere Versionen synchronisierten ihn standardmäßig. In Aktiv-Aktiv-Konfigurationen konnte das zu negativen Werten führen. Beim Neuladen oder beim Wechsel zwischen aktiver und passiver Rolle wuchsen die Werte immer weiter, weil der lokale Wert mehr Verbindungen auswies, als vor Ort bestanden. In manchen Konfigurationen kann die Übernahme von Peers dennoch sinnvoll sein, etwa bei einer passiven entfernten Tabelle, aus der ausschließlich Daten übernommen oder überwacht werden, ohne sie für Schreibvorgänge oder Aktualisierungen zu verwenden. Dazu lässt sich "recv-only" zur Tabellendeklaration hinzufügen. Die Informationen zu "conn_cur" werden in jedem Fall immer gesendet, damit Überwachungssysteme sie beobachten können.

Unterbrochener Datenaustausch wird automatisch erkannt und am letzten bekannten Stand fortgesetzt. Bei einem unterbrechungsfreien Neustart verbindet sich der alte Prozess außerdem über eine solche TCP-Verbindung mit dem neuen und überträgt alle Einträge, bevor der neue Prozess versucht, andere Peers zu erreichen. Dies ermöglicht eine sehr schnelle Replikation beim Neuladen: Selbst große Tabellen benötigen normalerweise nur einen Sekundenbruchteil.

Server werden auf entfernten Instanzen über ihre IDs identifiziert. Deshalb ist es wichtig, dass die Konfigurationen ähnlich aufgebaut sind oder zumindest für jeden Server bei allen Teilnehmern dieselbe ID fest vorgegeben wird.

<a id="entry-11-2-peers"></a>

**`peers <peersect>`**

```haproxy
peers <peersect>
```

Erstellt eine neue Peer-Liste namens `<peersect>`. Sie bildet einen eigenständigen Abschnitt, auf den eine oder mehrere Stick Tables verweisen.

<a id="entry-11-2-bind"></a>

**`bind [<address>]:port [param*]`**

```haproxy
bind [<address>]:port [param*]
bind /<path> [param*]
```

Legt die Bindungsparameter des lokalen Peers dieses "peers"-Abschnitts fest. Solche Zeilen werden nicht zusammen mit einer "peer"-Zeile im selben "peers"-Abschnitt unterstützt.

<a id="entry-11-2-disabled"></a>

**`disabled`**

```haproxy
disabled
```

Deaktiviert einen Peers-Abschnitt. Sowohl das Lauschen auf Verbindungen als auch jede Synchronisierung dieses Abschnitts werden abgeschaltet. Damit lässt sich die Synchronisierung von Stick Tables deaktivieren, ohne sämtliche "peers"-Verweise auszukommentieren.

<a id="entry-11-2-default-bind"></a>

**`default-bind [param*]`**

```haproxy
default-bind [param*]
```

Legt die Bindungsparameter des lokalen Peers mit Ausnahme seiner Adresse fest.

<a id="entry-11-2-default-server"></a>

**`default-server [param*]`**

```haproxy
default-server [param*]
```

Ändert die Standardoptionen für einen Server in einem "peers"-Abschnitt.

Argumente:

```text
<param*>  ist eine Parameterliste für diesen Server. "default-server"
          unterstützt zahlreiche Optionen und wird in einem eigenen
          Abschnitt beschrieben. In einem Peers-Abschnitt sind die
          Transportparameter einer "default-server"-Zeile zulässig.
          Einzelheiten stehen in Abschnitt 5; Einschränkungen werden
          unten beim Schlüsselwort "server" erläutert.
```

Siehe auch "server" und [Abschnitt 5](/de/haproxy/bind-and-server-options/) zu Serveroptionen.

<a id="entry-11-2-enabled"></a>

**`enabled`**

```haproxy
enabled
```

Aktiviert einen zuvor mit "disabled" deaktivierten Peers-Abschnitt erneut.

<a id="entry-11-2-log"></a>

**`log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]`**

```haproxy
log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]
    <facility> [<level> [<minlevel>]]
```

"peers"-Abschnitte unterstützen dasselbe "log"-Schlüsselwort wie Proxys, um Informationen zum "peers"-Listener zu protokollieren. Einzelheiten stehen bei der Proxy-Option "log".

<a id="entry-11-2-peer"></a>

**`peer <peername> [<address>]:port [param*]`**

```haproxy
peer <peername> [<address>]:port [param*]
peer <peername> /<path> [param*]
```

Definiert einen Peer innerhalb eines Peers-Abschnitts. Entspricht `<peername>` dem lokalen Peer-Namen, lauscht HAProxy an der angegebenen Adresse auf Verbindungen entfernter Peers. Der lokale Name ist standardmäßig der Hostname; er lässt sich mit der Befehlszeilenoption "-L" oder der globalen Einstellung "localpeer" festlegen. Andernfalls gibt die Adresse das Ziel für die Verbindung zum entfernten Peer an. `<peername>` dient dann auf Protokollebene dazu, den entfernten Peer auf der Serverseite zu identifizieren und zu überprüfen.

Bei einem unterbrechungsfreien Neustart verwendet die alte Instanz die lokale Peer-Adresse, um sich mit der neuen zu verbinden und eine vollständige Replikation einzuleiten, den sogenannten Lernvorgang.

Es wird dringend empfohlen, auf allen Peers genau dieselbe Peers-Deklaration zu verwenden und den lokalen Peer-Namen ausschließlich über das Befehlszeilenargument "-L" oder die globale Einstellung "localpeer" festzulegen. So lassen sich konsistente Konfigurationsdateien für alle Peers leichter pflegen.

Im Adressparameter können Umgebungsvariablen verwendet werden; siehe [Abschnitt 2.3](/de/haproxy/configuration-basics/#section-2-3).

Hinweis: "peer" lässt sich ohne weitere Änderungen durch "server" ersetzen; siehe die Erklärung zu "server" unten.

<a id="entry-11-2-server"></a>

**`server <peername> [<address>:<port>] [param*]`**

```haproxy
server <peername> [<address>:<port>] [param*]
server <peername> [/<path>] [param*]
```

Wie bereits erwähnt, kann "server" anstelle von "peer" verwendet werden. Dabei werden alle transportbezogenen "server"-Parameter aus Abschnitt 5.2 unterstützt. Ist der betreffende Peer lokal, darf kein Adressparameter angegeben werden. Die Adresse muss stattdessen in einer "bind"-Zeile stehen; siehe "bind" in diesem "peers"-Abschnitt.

Einige "server"-Parameter sind für "peers"-Abschnitte nicht relevant. Peers unterstützen weder dynamische Hostnamenauflösung noch Health Checks. Parameter wie "init_addr", "resolvers", "check", "agent-check" oder "track" werden daher nicht unterstützt. Ebenso gibt es weder Lastverteilung noch feste Serverzuordnung; "weight" und "cookie" haben deshalb keine Wirkung.

Beispiel:

```text
 # The old way.
 peers mypeers
     peer haproxy1 192.168.0.1:1024
     peer haproxy2 192.168.0.2:1024
     peer haproxy3 10.2.0.1:1024

 backend mybackend
     mode tcp
     balance roundrobin
     stick-table type ip size 20k peers mypeers
     stick on src

     server srv1 192.168.0.30:80
     server srv2 192.168.0.31:80

Beispiel:
  peers mypeers
     bind 192.168.0.1:1024 ssl crt mycerts/pem
     default-server ssl verify none
     server haproxy1 #local peer
     server haproxy2 192.168.0.2:1024
     server haproxy3 10.2.0.1:1024
```

shards `<shards>`

In manchen Konfigurationen soll der Inhalt von Stick Tables auf einige Peers verteilt werden, statt den gesamten Inhalt an jeden Peer im "peers"-Abschnitt zu senden. "shards" gibt in diesem Fall die Anzahl der an der Verteilung beteiligten Peers an. Siehe auch den Serverparameter "shard".

<a id="entry-11-2-table"></a>

**`table <tablename> type {ip | integer | string [len <length>] | binary [len <length>]}`**

```haproxy
table <tablename> type {ip | integer | string [len <length>] | binary [len <length>]}
```

      size `<size>` [expire `<expire>`] [write-to `<wtable>`] [nopurge] [store `<data_type>`]*
      [recv-only]

Konfiguriert eine Zuordnungstabelle für den aktuellen Abschnitt. Die Zeile wird genauso wie "stick-table" in anderen Abschnitten verarbeitet. Allerdings entfällt hier das Argument "peers", und ein zusätzliches erstes Pflichtargument benennt die Stick Table. Anders als in anderen Abschnitten sind in "peers" mehrere "table"-Zeilen möglich. Die vollständige Definition von "table" und "stick-table" steht oben in [Abschnitt 11.1](/de/haproxy/stick-tables-and-peers/#section-11-1).

"peers"-Abschnitte haben eigene Namensräume für Stick Tables, damit gleiche Tabellennamen in verschiedenen "peers"-Abschnitten nicht kollidieren. Intern wird dem Tabellennamen der Name des "peers"-Abschnitts, gefolgt von '/', vorangestellt. Wird an anderer Stelle der Konfiguration auf eine in "peers" deklarierte Stick Table verwiesen, muss dieser Name mit Präfix verwendet werden:

```text
peers mypeers
    peer A ...
    peer B ...
    table t1 ...

frontend fe1
    tcp-request content track-sc0 src table mypeers/t1
```

Auch beim Zugriff auf Stick Tables über die CLI muss dieser Name mit Präfix verwendet werden.

Im "peers"-Protokoll ist diese Unterscheidung nicht erforderlich, da nur "peers" desselben Abschnitts miteinander kommunizieren können. Mehrere "peers"-Abschnitte können Stick Tables gleichen Namens deklarieren. Über das Netzwerk wird der kürzere Tabellenname gesendet, lediglich mit einem vorangestellten '/'. Das verhindert Kollisionen zwischen Tabellen aus Backends und solchen aus "peers"-Abschnitten, wie in folgender ungewöhnlichen, aber unterstützten Konfiguration:

```text
peers mypeers
    peer A ...
    peer B ...
    table t1 type string size 10m store gpc0

backend t1
    stick-table type string size 10m store gpc0 peers mypeers
```

Die Tabelle "t1" im Abschnitt "mypeers" hat hier den globalen Namen "mypeers/t1". Die im Backend deklarierte Tabelle "t1" heißt global "t1". Im Peers-Protokoll heißt die erste Tabelle dagegen "/t1" und die zweite wiederum "t1".
