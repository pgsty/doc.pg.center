---
title: "9. Statistiken und Überwachung"
linkTitle: "9. Statistiken & Überwachung"
weight: 330
description: "CSV- und typisierte Statistiken, Runtime-CLI-Befehle, Master-CLI und Statistikdateien"
icon: fa-solid fa-chart-line
module: [HAPROXY]
categories: [Aufgabe]
aliases:
  - /haproxy/management/statistics-and-monitoring/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 9"
---

Der Status von HAProxy lässt sich abfragen. Am häufigsten wird dafür die HTTP-Statistikseite verwendet. Diese Seite bietet zusätzlich ein CSV-Ausgabeformat für Überwachungswerkzeuge. Dasselbe Format steht über den Unix-Socket zur Verfügung.

Die Statistiken sind in Kategorien zusammengefasst, die als Domänen bezeichnet werden und den verschiedenen Komponenten von HAProxy entsprechen. Zwei Domänen stehen zur Verfügung: proxy und resolvers. Ohne ausdrückliche Angabe wird die Domäne proxy ausgewählt. Beachten Sie, dass auf der HTTP-Seite nur die Proxy-Statistiken ausgegeben werden.

## 9.1. CSV-Format {#section-9-1}

Die Statistiken können entweder über den Unix-Socket oder über die HTTP-Seite abgefragt werden. Beide Wege liefern ein CSV-Format mit den nachfolgend beschriebenen Feldern. Die erste Zeile beginnt mit einem Rautezeichen ('#') und enthält für jedes durch Komma getrennte Feld ein Wort als Spaltentitel. Alle weiteren Zeilen ab der zweiten verwenden ein klassisches CSV-Format mit Komma als Trennzeichen und dem doppelten Anführungszeichen ('"') als optionalem Textbegrenzer. Dieser wird nur verwendet, wenn der eingeschlossene Text mehrdeutig ist, also ein Anführungszeichen oder ein Komma enthält. Doppelte Anführungszeichen ('"') innerhalb des Textes werden verdoppelt ('""'); dieses Format erkennen die meisten Werkzeuge. Fügen Sie vor diesen Spalten keine weiteren ein, damit Werkzeuge mit fest kodierten Spaltenpositionen weiterhin funktionieren.

Bei den Proxy-Statistiken stehen hinter jedem Feldnamen in Klammern die Typen, für die dieses Feld einen Wert enthalten kann. Die Typen sind L (Listener), F (Frontends), B (Backends) und S (Server). Es gibt einen festen Satz statischer Felder, die stets in derselben Reihenfolge vorhanden sind. Eine Spalte mit dem Zeichen '-' markiert das Ende der statischen Felder. Für die darauf folgenden Felder sind weder Vorhandensein noch Reihenfolge garantiert.

Die statischen Felder der Statistikdomäne proxy sind:

```text
 0. pxname [LFBS]: Proxyname
 1. svname [LFBS]: Dienstname (FRONTEND für ein Frontend, BACKEND für ein Backend,
    beliebiger Name für einen Server/Listener)
 2. qcur [..BS]: Derzeit wartende Anfragen. Für das Backend wird die Anzahl
    der wartenden Anfragen angegeben, denen kein Server zugewiesen ist.
 3. qmax [..BS]: Höchstwert von qcur
 4. scur [LFBS]: Aktuelle Sitzungen
 5. smax [LFBS]: Höchstzahl an Sitzungen
 6. slim [LFBS]: Konfiguriertes Sitzungslimit
 7. stot [LFBS]: Kumulierte Anzahl an Sitzungen
 8. bin [LFBS]: Eingehende Bytes
 9. bout [LFBS]: Ausgehende Bytes
10. dreq [LFB.]: Aus Sicherheitsgründen abgelehnte Anfragen.
    - Bei tcp geschieht dies aufgrund einer zutreffenden tcp-request content-Regel.
    - Bei http geschieht dies aufgrund einer zutreffenden http-request- oder tarpit-Regel.
11. dresp [LFBS]: Aus Sicherheitsgründen abgelehnte Antworten.
    - Bei http geschieht dies aufgrund einer zutreffenden http-request-Regel
      oder "option checkcache".
12. ereq [LF..]: Anfragefehler. Mögliche Ursachen sind unter anderem:
    - Vorzeitiger Abbruch durch den Client, bevor die Anfrage gesendet wurde.
    - Lesefehler beim Client
    - Zeitüberschreitung beim Client
    - Der Client hat die Verbindung geschlossen
    - Verschiedene fehlerhafte Anfragen des Clients.
    - Die Anfrage wurde durch tarpit verzögert.
13. econ [..BS]: Anzahl der Anfragen, bei denen beim Verbindungsversuch zu
    einem Backend-Server ein Fehler auftrat. Der Backend-Wert ist die Summe
    der Werte aller Server dieses Backends, zuzüglich aller Verbindungsfehler,
    die keinem bestimmten Server zugeordnet sind (etwa wenn das Backend
    keine aktiven Server hat).
14. eresp [..BS]: Antwortfehler. Auch srv_abrt wird hier mitgezählt.
    Weitere Fehler sind unter anderem:
    - Schreibfehler am Client-Socket (wird nicht für die Serverstatistik gezählt)
    - Fehler beim Anwenden von Filtern auf die Antwort.
15. wretr [..BS]: Anzahl der wiederholten Verbindungsversuche zu einem Server.
16. wredis [..BS]: Anzahl der erneuten Zuweisungen einer Anfrage an einen
    anderen Server. Der Serverwert zählt, wie oft von diesem Server
    zu einem anderen gewechselt wurde.
17. status [LFBS]: Status (UP/DOWN/NOLB/MAINT/MAINT(via)/MAINT(resolution)...)
18. weight [..BS]: Effektives Gesamtgewicht (Backend), effektives Gewicht (Server)
19. act [..BS]: Anzahl aktiver Server (Backend), Server ist aktiv (Server)
20. bck [..BS]: Anzahl der Backup-Server (Backend), Server ist Backup (Server)
21. chkfail [...S]: Anzahl fehlgeschlagener Prüfungen. (Zählt nur Prüfungen,
    die fehlschlagen, während der Server verfügbar ist.)
22. chkdown [..BS]: Anzahl der UP->DOWN-Übergänge. Der Backend-Zähler zählt
    Übergänge, bei denen das gesamte Backend ausfällt, nicht die Summe
    der Zähler der einzelnen Server.
23. lastchg [..BS]: Sekunden seit dem letzten UP<->DOWN-Übergang
24. downtime [..BS]: Gesamte Ausfallzeit (in Sekunden). Der Backend-Wert ist
    die Ausfallzeit des gesamten Backends, nicht die Summe der Serverausfallzeiten.
25. qlimit [...S]: Für den Server konfigurierter maxqueue-Wert; leer, wenn
    der Wert 0 ist (Standard, bedeutet unbegrenzt)
26. pid [LFBS]: Prozess-ID (0 für die erste Instanz, 1 für die zweite, ...)
27. iid [LFBS]: Eindeutige Proxy-ID
28. sid [L..S]: Server-ID (innerhalb eines Proxys eindeutig)
29. throttle [...S]: Aktueller Drosselungsprozentsatz des Servers, wenn
    slowstart aktiv ist; kein Wert, wenn slowstart nicht aktiv ist.
30. lbtot [..BS]: Gesamtzahl der Serverauswahlen, sowohl für neue Sitzungen
    als auch bei erneuter Zuweisung. Der Server-Zähler gibt an, wie oft
    dieser Server ausgewählt wurde.
31. tracked [...S]: ID von Proxy/Server, wenn die Überwachung aktiviert ist.
32. type [LFBS]: (0=frontend, 1=backend, 2=server, 3=socket/listener)
33. rate [.FBS]: Sitzungen pro Sekunde während der zuletzt verstrichenen Sekunde
34. rate_lim [.F..]: Konfiguriertes Limit neuer Sitzungen pro Sekunde
35. rate_max [.FBS]: Höchstzahl neuer Sitzungen pro Sekunde
36. check_status [...S]: Status des letzten Health Checks, einer der folgenden:
       UNK     -> Unbekannt
       INI     -> Initialisierung
       SOCKERR -> Socket-Fehler
       L4OK    -> Prüfung auf Schicht 4 erfolgreich, Prüfung höherer Schichten deaktiviert
       L4TOUT  -> Zeitüberschreitung auf Schicht 1-4
       L4CON   -> Verbindungsproblem auf Schicht 1-4, beispielsweise
                  "Connection refused" (tcp rst) oder "No route to host" (icmp)
       L6OK    -> Prüfung auf Schicht 6 erfolgreich
       L6TOUT  -> Zeitüberschreitung auf Schicht 6 (SSL)
       L6RSP   -> Ungültige Antwort auf Schicht 6 - Protokollfehler
       L7OK    -> Prüfung auf Schicht 7 erfolgreich
       L7OKC   -> Prüfung auf Schicht 7 bedingt erfolgreich, beispielsweise 404 mit
                  disable-on-404
       L7TOUT  -> Zeitüberschreitung auf Schicht 7 (HTTP/SMTP)
       L7RSP   -> Ungültige Antwort auf Schicht 7 - Protokollfehler
       L7STS   -> Antwortfehler auf Schicht 7, beispielsweise HTTP 5xx
    Hinweis: Läuft gerade eine Prüfung, wird der letzte bekannte Status
    mit dem Präfix "* " gemeldet, z. B. "* L7OK".
37. check_code [...S]: Code der Schicht 5-7, falls verfügbar
38. check_duration [...S]: Dauer des letzten Health Checks in ms
39. hrsp_1xx [.FBS]: http-Antworten mit 1xx-Code
40. hrsp_2xx [.FBS]: http-Antworten mit 2xx-Code
41. hrsp_3xx [.FBS]: http-Antworten mit 3xx-Code
42. hrsp_4xx [.FBS]: http-Antworten mit 4xx-Code
43. hrsp_5xx [.FBS]: http-Antworten mit 5xx-Code
44. hrsp_other [.FBS]: http-Antworten mit anderen Codes (Protokollfehler)
45. hanafail [...S]: Details fehlgeschlagener Health Checks
46. req_rate [.F..]: HTTP-Anfragen pro Sekunde während der zuletzt verstrichenen Sekunde
47. req_rate_max [.F..]: Höchste beobachtete Anzahl an HTTP-Anfragen pro Sekunde
48. req_tot [.FB.]: Gesamtzahl empfangener HTTP-Anfragen
49. cli_abrt [..BS]: Anzahl der vom Client abgebrochenen Datenübertragungen
50. srv_abrt [..BS]: Anzahl der vom Server abgebrochenen Datenübertragungen
    (in eresp enthalten)
51. comp_in [.FB.]: Anzahl der dem Kompressor zugeführten HTTP-Antwortbytes
52. comp_out [.FB.]: Anzahl der vom Kompressor ausgegebenen HTTP-Antwortbytes
53. comp_byp [.FB.]: Anzahl der Bytes, die den HTTP-Kompressor umgangen haben
    (CPU/BW-Limit)
54. comp_rsp [.FB.]: Anzahl komprimierter HTTP-Antworten
55. lastsess [..BS]: Sekunden seit der letzten einem Server/Backend
    zugewiesenen Sitzung
56. last_chk [...S]: Inhalt des letzten Health Checks oder Fehlertext
57. last_agt [...S]: Inhalt der letzten Agentenprüfung oder Fehlertext
58. qtime [..BS]: Mittlere Wartezeit in der Warteschlange in ms über die letzten 1024 Anfragen
59. ctime [..BS]: Mittlere Verbindungsaufbauzeit in ms über die letzten 1024 Anfragen
60. rtime [..BS]: Mittlere Antwortzeit in ms über die letzten 1024 Anfragen
    (0 für TCP)
61. ttime [..BS]: Mittlere Gesamtdauer einer Sitzung in ms über die letzten
    1024 Anfragen
62. agent_status [...S]: Status der letzten Agentenprüfung, einer der folgenden:
       UNK     -> Unbekannt
       INI     -> Initialisierung
       SOCKERR -> Socket-Fehler
       L4OK    -> Prüfung auf Schicht 4 erfolgreich, Prüfung höherer Schichten deaktiviert
       L4TOUT  -> Zeitüberschreitung auf Schicht 1-4
       L4CON   -> Verbindungsproblem auf Schicht 1-4, beispielsweise
                  "Connection refused" (tcp rst) oder "No route to host" (icmp)
       L7OK    -> Agent meldete "up"
       L7STS   -> Agent meldete "fail", "stop" oder "down"
63. agent_code [...S]: Vom Agenten gemeldeter Zahlencode, falls vorhanden (derzeit ungenutzt)
64. agent_duration [...S]: Dauer der letzten Prüfung in ms
65. check_desc [...S]: Kurze, für Menschen lesbare Beschreibung von check_status
66. agent_desc [...S]: Kurze, für Menschen lesbare Beschreibung von agent_status
67. check_rise [...S]: Von Prüfungen verwendeter "rise"-Parameter des Servers
68. check_fall [...S]: Von Prüfungen verwendeter "fall"-Parameter des Servers
69. check_health [...S]: Health-Check-Wert des Servers zwischen 0 und rise+fall-1
70. agent_rise [...S]: "rise"-Parameter des Agenten, normalerweise 1
71. agent_fall [...S]: "fall"-Parameter des Agenten, normalerweise 1
72. agent_health [...S]: Zustandsparameter des Agenten zwischen 0 und rise+fall-1
73. addr [L..S]: address:port oder "unix". IPv6-Adressen stehen in Klammern.
74: cookie [..BS]: Cookie-Wert des Servers oder Cookie-Name des Backends
75: mode [LFBS]: Proxy-Modus (tcp, http, health, unknown)
76: algo [..B.]: Algorithmus zur Lastverteilung
77: conn_rate [.F..]: Anzahl der Verbindungen während der zuletzt verstrichenen Sekunde
78: conn_rate_max [.F..]: Höchster bekannter conn_rate-Wert
79: conn_tot [.F..]: Kumulierte Anzahl der Verbindungen
80: intercepted [.FB.]: Kumulierte Anzahl abgefangener Anfragen (monitor, stats)
81: dcon [LF..]: Durch "tcp-request connection"-Regeln abgelehnte Anfragen
82: dses [LF..]: Durch "tcp-request session"-Regeln abgelehnte Anfragen
83: wrew [LFBS]: Kumulierte Anzahl der Warnungen wegen fehlgeschlagener Header-Umschreibungen
84: connect [..BS]: Kumulierte Anzahl der Verbindungsaufbauversuche
85: reuse [..BS]: Kumulierte Anzahl der Wiederverwendungen von Verbindungen
86: cache_lookups [.FB.]: Kumulierte Anzahl der Cache-Abfragen
87: cache_hits [.FB.]: Kumulierte Anzahl der Cache-Treffer
88: srv_icur [...S]: Aktuelle Anzahl inaktiver Verbindungen, die zur Wiederverwendung verfügbar sind
89: src_ilim [...S]: Begrenzung der Anzahl verfügbarer inaktiver Verbindungen
90. qtime_max [..BS]: Höchste beobachtete Wartezeit in der Warteschlange in ms
91. ctime_max [..BS]: Höchste beobachtete Verbindungsaufbauzeit in ms
92. rtime_max [..BS]: Höchste beobachtete Antwortzeit in ms (0 für TCP)
93. ttime_max [..BS]: Höchste beobachtete Gesamtdauer einer Sitzung in ms
94. eint [LFBS]: Kumulierte Anzahl interner Fehler
95. idle_conn_cur [...S]: Aktuelle Anzahl unsicherer inaktiver Verbindungen
96. safe_conn_cur [...S]: Aktuelle Anzahl sicherer inaktiver Verbindungen
97. used_conn_cur [...S]: Aktuelle Anzahl verwendeter Verbindungen
98. need_conn_est [...S]: Geschätzte Anzahl benötigter Verbindungen
99. uweight [..BS]: Gesamtgewicht laut Benutzereinstellung (Backend), Servergewicht laut Benutzereinstellung (Server)
100. agg_server_status [..B.]: Im Backend aggregierter Momentanwert für den Serverstatus
101. agg_server_status_check [..B.]: (veraltet)
102. agg_check_status [..B.]: Im Backend aggregierter Momentanwert für den Status
     der Serverzustandsprüfung
103. srid [...S]: Revision der Server-ID
104. sess_other [.F..]: Gesamtzahl der Nicht-HTTP-Sitzungen seit dem
     Prozessstart
105. h1_sess [.F..]: Gesamtzahl der HTTP/1-Sitzungen seit dem Prozessstart
106. h2_sess [.F..]: Gesamtzahl der HTTP/2-Sitzungen seit dem Prozessstart
107. h3_sess [.F..]: Gesamtzahl der HTTP/3-Sitzungen seit dem Prozessstart
108. req_other [.F..]: Gesamtzahl der Nicht-HTTP-Sitzungen, die dieses Objekt
     seit dem Start des Worker-Prozesses verarbeitet hat
109. h1req [.F..]: Gesamtzahl der HTTP/1-Sitzungen, die dieses Objekt seit
     dem Start des Worker-Prozesses verarbeitet hat
110. h2req [.F..]: Gesamtzahl der hTTP/2-Sitzungen, die dieses Objekt seit
     dem Start des Worker-Prozesses verarbeitet hat
111. h3req [.F..]: Gesamtzahl der HTTP/3-Sitzungen, die dieses Objekt seit
     dem Start des Worker-Prozesses verarbeitet hat
112. proto [L...]: Protokoll
113. priv_idle_cur [...S]: Aktuelle Anzahl privater inaktiver Verbindungen
114. reqbin [LFBS]: Gesamtzahl empfangener Anfragebytes seit dem Start
     des Worker-Prozesses
115. reqbout [LFBS]: Gesamtzahl gesendeter Anfragebytes seit dem Start
     des Worker-Prozesses
116. resbin [LFBS]: Gesamtzahl empfangener Antwortbytes seit dem Start
     des Worker-Prozesses
117. resbout [LFBS]: Gesamtzahl gesendeter Antwortbytes seit dem Start
     des Worker-Prozesses
```

Für alle anderen Statistikdomänen sind weder das Vorhandensein noch die Reihenfolge der Felder garantiert. In diesem Fall sollte zum Auswerten der CSV-Daten immer die Kopfzeile verwendet werden.

## 9.2. Typisiertes Ausgabeformat {#section-9-2}

Sowohl "show info" als auch "show stat" unterstützen einen Modus, in dem jeder Ausgabewert zusammen mit seinem Typ und ausreichenden Informationen ausgegeben wird, um zu erkennen, wie der Wert über mehrere Prozesse hinweg aggregiert werden soll und wie er sich verändert.

In allen Fällen enthält die Ausgabe genau einen Wert pro Zeile. Sämtliche Informationen sind in Felder aufgeteilt, die durch Doppelpunkte (':') getrennt werden.

Die erste Spalte bezeichnet das ausgegebene Objekt oder die Metrik. Ihr Format hängt vom ausgebenden Befehl ab und wird in diesem Abschnitt nicht beschrieben. Üblicherweise besteht sie aus einer Folge von Kennungen und Feldnamen.

Die zweite Spalte enthält 4 Zeichen, die in dieser Reihenfolge Herkunft, Art, Gültigkeitsbereich und Persistenzstatus des gemeldeten Werts angeben. Das erste Zeichen (die Herkunft) gibt an, woher der Wert stammt. Mögliche Zeichen sind:

```text
M   Der Wert ist eine Metrik. Er gilt zu einem bestimmten Zeitpunkt und
    kann sich je nach seiner Art ändern.

S   Der Wert ist ein Status. Er stellt einen diskreten Wert dar, der
    definitionsgemäß nicht aggregiert werden kann. Dies kann der Status
    eines Servers ("UP" oder "DOWN"), die PID des Prozesses usw. sein.

K   Der Wert ist ein Sortierschlüssel. Er stellt einen Bezeichner dar, der
    zum Gruppieren von Werten verwendet werden kann, da er innerhalb
    seiner Klasse eindeutig ist. Alle internen Bezeichner sind Schlüssel.
    Manche Namen können als Schlüssel aufgeführt werden, wenn sie
    eindeutig sind (z. B. ist ein Frontend-Name eindeutig). Im Allgemeinen
    stammen Schlüssel aus der Konfiguration, auch wenn einige automatisch
    zugewiesen werden können. Für die meisten Zwecke können Schlüssel
    als gleichwertig mit Konfigurationswerten betrachtet werden.

C   Der Wert stammt aus der Konfiguration. Manche Konfigurationswerte sind
    in der Ausgabe sinnvoll, etwa ein Limit gleichzeitiger Verbindungen
    oder ein Cookie-Name. Definitionsgemäß sind diese Werte in allen
    Prozessen gleich, die mit derselben Konfigurationsdatei gestartet wurden.

P   Der Wert stammt aus dem Produkt selbst. Es gibt nur sehr wenige solche
    Werte; meist dienen sie zur Ausgabe des Produktnamens, der Version und
    des Veröffentlichungsdatums. Auch diese Angaben sind in allen Prozessen
    gleich.
```

Das zweite Zeichen (die Art) beschreibt die Art der im Feld enthaltenen Information, damit ein Aggregator entscheiden kann, mit welcher Operation mehrere Werte zusammenzufassen sind. Mögliche Zeichen sind:

```text
A   Der Wert stellt das Alter seit einem letzten Ereignis dar. Dies
    unterscheidet sich etwas von einer Dauer, da ein Alter automatisch
    anhand des aktuellen Datums berechnet wird. Ein typisches Beispiel
    ist, wie lange die letzte Sitzung auf einem Server zurückliegt.
    Alterswerte werden in der Regel durch Bildung des Minimums aggregiert
    und müssen nicht gespeichert werden.

a   Der Wert stellt einen bereits gemittelten Wert dar. Dazu gehören
    mittlere Antwortzeiten und Servergewichte. Mittelwerte können
    üblicherweise über mehrere Prozesse hinweg gemittelt werden.

C   Der Wert stellt einen kumulativen Zähler dar. Solche Messwerte steigen
    fortlaufend bis zum Überlauf. Einige Überwachungsprotokolle müssen
    zwischen Zählern und Momentanwerten unterscheiden, um einen anderen
    Typ zu melden. Im Allgemeinen lassen sich Zähler einfach summieren,
    da sie Ereignisse oder Mengen abbilden. Beispiele für solche Metriken
    sind Verbindungs- oder Bytezähler.

D   Der Wert stellt die Dauer eines Zustands dar. Es gibt einige
    Anwendungsfälle; meistens betreffen sie die Dauer des letzten Health
    Checks und die Ausfallzeit eines Servers. Dauern werden im Allgemeinen
    nicht summiert. Meist wird das Maximum für die Berechnung eines SLA
    beibehalten.

G   Der Wert stellt einen Momentanwert dar, also einen Messwert zu einem
    bestimmten Zeitpunkt. Dazu gehören die Speichernutzung oder die
    aktuelle Anzahl aktiver Verbindungen. Metriken dieses Typs werden
    bei der Aggregation üblicherweise summiert.

L   Der Wert stellt ein Limit dar (in der Regel ein konfiguriertes).
    Limits sind von Natur aus schwerer zu aggregieren, da sie sich auf
    die Stelle beziehen, an der sie ermittelt wurden. In bestimmten
    Situationen können sie summiert oder getrennt beibehalten werden.

M   Der Wert stellt ein Maximum dar. Im Allgemeinen bezieht es sich auf
    einen Momentanwert und hält den höchsten bekannten Wert fest. Ein
    Beispiel wäre die höchste Anzahl gleichzeitiger Verbindungen während
    der Laufzeit des Produkts. Zur korrekten Aggregation von Maxima
    sollten Sie einen Bereich vom größten aller Maxima bis zu ihrer
    Summe ausgeben. Es lässt sich nämlich nicht feststellen, ob die
    Werte gleichzeitig aufgetreten sind.

m   Der Wert stellt ein Minimum dar. Im Allgemeinen bezieht es sich auf
    einen Momentanwert und hält den niedrigsten bekannten Wert fest. Ein
    Beispiel wäre die niedrigste Anzahl freier Speicherpools während der
    Laufzeit des Produkts. Zur korrekten Aggregation von Minima sollten
    Sie einen Bereich vom kleinsten aller Minima bis zu ihrer Summe
    ausgeben. Es lässt sich nämlich nicht feststellen, ob die Werte
    gleichzeitig aufgetreten sind.

N   Der Wert stellt einen Namen dar und ist daher eine Zeichenfolge.
    Damit werden Proxynamen, Servernamen und Cookie-Namen ausgegeben.
    Namen stammen aus der Konfiguration oder aus Schlüsseln und sollten
    in allen Prozessen gleich sein.

O   Der Wert stellt eine Freitextausgabe dar. Dazu gehören die Ausgaben
    verschiedener Befehle, Rückgaben von Health Checks und
    Knotenbeschreibungen.

R   Der Wert stellt eine Ereignisrate dar. Es handelt sich um einen
    Messwert zu einem bestimmten Zeitpunkt. Er ähnelt einem Momentanwert;
    der Empfänger weiß jedoch, dass sich dieser Messwert langsam ändert,
    und kann entscheiden, nicht alle Werte zu speichern. Ein Beispiel
    ist die gemessene Anzahl an Verbindungen pro Sekunde. Metriken dieses
    Typs werden bei der Aggregation üblicherweise summiert.

T   Der Wert stellt ein Datum oder eine Uhrzeit dar. Ein Feld, das das
    aktuelle Datum ausgibt, hätte diesen Typ. Wie diese Informationen
    aggregiert werden, bleibt der Implementierung überlassen. Derzeit
    verwendet kein Feld diesen Typ.
```

Das dritte Zeichen (der Gültigkeitsbereich) gibt an, auf welchen Bereich sich der Wert bezieht. Manche Angaben gelten pro Prozess, andere pro Konfiguration oder für das gesamte System. Diese Unterscheidung ist wichtig, um zu entscheiden, ob bei der Aggregation ein einzelner Wert beibehalten werden sollte oder mehrere Werte zusammengefasst werden müssen. Derzeit werden folgende Zeichen unterstützt:

```text
C   Der Wert gilt für einen ganzen Cluster von Knoten, also die Menge
    der Knoten, die über das peers-Protokoll kommunizieren. Ein Beispiel
    wäre die Anzahl der Einträge in einer Stick Table, die mit anderen
    Peers repliziert wird. Derzeit verwendet keine Metrik diesen
    Geltungsbereich.

P   Der Wert gilt nur für den Prozess, der ihn meldet. Die meisten
    Metriken verwenden diesen Geltungsbereich.

S   Der Wert gilt für den gesamten Dienst, also die Menge der Prozesse,
    die gemeinsam mit derselben Konfigurationsdatei gestartet wurden.
    Alle Metriken aus der Konfiguration verwenden diesen Geltungsbereich.
    Einige andere Metriken können ihn ebenfalls für gemeinsam genutzte
    Ressourcen verwenden (z. B. Statistiken zum gemeinsamen SSL-Cache).

s   Der Wert gilt für das gesamte System, etwa für dessen Hostnamen,
    aktuelles Datum oder Ressourcennutzung. Derzeit wird dieser
    Geltungsbereich von keiner Metrik verwendet.
```

Das vierte Zeichen (der Persistenzstatus) gibt an, ob der Wert (die Metrik) flüchtig ist oder über Neuladungen hinweg erhalten bleibt. Folgende Zeichen sind vorgesehen:

```text
V   Die Metrik ist flüchtig, da sie nur im aktuellen Prozess vorliegt.
    Ihr Wert geht daher beim Neuladen verloren.

P   Die Metrik ist persistent, da sie mit anderen gleichzeitig laufenden
    Prozessen geteilt werden kann. Ihr Wert bleibt somit über das
    Neuladen hinweg erhalten.
```

Für die Nutzer dieser Informationen reichen diese 4 Zeichen in der Regel aus, um zu bestimmen, wie aggregierte Informationen über mehrere Prozesse hinweg korrekt dargestellt werden können.

Die darauf folgende dritte Spalte gibt den Feldtyp an: "s32" (vorzeichenbehaftete 32-Bit-Ganzzahl), "s64" (vorzeichenbehaftete 64-Bit-Ganzzahl), "u32" (vorzeichenlose 32-Bit-Ganzzahl), "u64" (vorzeichenlose 64-Bit-Ganzzahl) oder "str" (Zeichenkette). Der Typ muss vor dem Parsen des Werts bekannt sein, damit dieser korrekt gelesen wird. Beispielsweise bleibt eine Zeichenkette, die nur Ziffern enthält, eine Zeichenkette und ist keine Ganzzahl, etwa ein bei einer Prüfung extrahierter Fehlercode.

Die vierte Spalte enthält anschließend den Wert selbst, entsprechend seinem Typ kodiert. Zeichenketten werden unverändert unmittelbar nach dem Doppelpunkt ohne führendes Leerzeichen ausgegeben. Enthält eine Zeichenkette einen Doppelpunkt, erscheint dieser ganz normal. Die Ausgabe sollte daher nicht ausschließlich an Doppelpunkten aufgeteilt werden, da sonst manche Prüfausgaben oder Serveradressen abgeschnitten werden könnten.

## 9.3. Unix-Socket-Befehle {#section-9-3}

Der Statistik-Socket ist standardmäßig nicht aktiviert. Zum Aktivieren muss im Abschnitt global der haproxy-Konfiguration eine Zeile hinzugefügt werden. Eine zweite Zeile wird empfohlen, um eine längere Wartezeit festzulegen, was bei der manuellen Befehlseingabe hilfreich ist:

```text
global
    stats socket /var/run/haproxy.sock mode 600 level admin
    stats timeout 2m
```

Durch Wiederholen der Zeile lassen sich auch mehrere Statistik-Sockets hinzufügen und an einen TCP-Port statt an einen UNIX-Socket binden. Dies wird wegen der damit verbundenen Gefahr nie standardmäßig eingerichtet, kann aber in manchen Situationen praktisch sein:

```text
global
    stats socket /var/run/haproxy.sock mode 600 level admin
    stats socket ipv4@192.168.0.1:9999 level admin
    stats timeout 2m
```

Für den Zugriff auf den Socket wird ein externes Werkzeug wie "socat" benötigt. Socat ist ein vielseitiges Werkzeug zum Verbinden beliebiger Ein- und Ausgaben. Hier wird es verwendet, um Terminals oder für Skripte ein Paar stdin/stdout-Pipes mit dem Socket zu verbinden. Hauptsächlich werden die folgenden beiden Aufrufformen verwendet:

```shell
# socat /var/run/haproxy.sock stdio
# socat /var/run/haproxy.sock readline
```

Die erste Form wird mit Skripten verwendet. Die Ausgabe eines Skripts kann an haproxy gesendet und die Ausgabe von haproxy an ein anderes Skript weitergereicht werden. Das ist beispielsweise zum Abrufen von Zählern oder Angriffsspuren nützlich.

Die zweite Form dient ausschließlich der manuellen Befehlseingabe. Dabei wird das Terminal von der readline-Bibliothek verwaltet, die Zeilenbearbeitung und einen Befehlsverlauf unterstützt. Das ist bei wiederholten Befehlen sehr praktisch, etwa zum Beobachten eines Zählers.

Der Socket unterstützt drei Betriebsarten:

- nicht interaktiv, ohne Eingabeaufforderung
- interaktiv, ohne Eingabeaufforderung
- interaktiv mit Eingabeaufforderung

Wenn socat eine Verbindung zum Socket herstellt, ist standardmäßig der nicht interaktive Modus aktiv. In diesem Modus kann eine einzelne Zeile gesendet werden. Sie wird als Ganzes verarbeitet, die Antworten werden zurückgesendet und nach dem Ende der Antwort wird die Verbindung geschlossen. Skripte und Überwachungswerkzeuge verwenden diesen Modus. Darin können mehrere Befehle gesendet werden, wenn sie durch ein Semikolon (';') getrennt sind. Beispiel:

```shell
# echo "show info;show stat;show table" | socat /var/run/haproxy stdio
```

Wenn ein Befehl ein Semikolon oder einen umgekehrten Schrägstrich benötigt, etwa innerhalb eines Werts, muss diesem Zeichen ein umgekehrter Schrägstrich ('&#92;') vorangestellt werden.

Im interaktiven Modus können neue Befehle gesendet werden, nachdem die Befehle der vorherigen Zeilen abgeschlossen sind. Es gibt zwei Varianten: eine ohne Eingabeaufforderung, die wie der nicht interaktive Modus funktioniert, aber auf einen neuen Befehl wartet, statt den Socket zu schließen; und eine, bei der am Zeilenanfang eine Eingabeaufforderung ('\>') erscheint. Der interaktive Modus eignet sich für anspruchsvollere Werkzeuge, der Modus mit Eingabeaufforderung für die manuelle Bedienung.

Der Modus lässt sich mit dem Befehl "prompt" ändern. Standardmäßig schaltet er zwischen dem interaktiven Modus und dem Modus mit Eingabeaufforderung um. Die Eingabe von "prompt" im interaktiven Modus aktiviert die Eingabeaufforderung. Optional akzeptiert der Befehl einen bestimmten Modus:

- "n": nicht interaktiver Modus (ein einzelner Befehl, dann Ende)
- "i": interaktiver Modus (mehrere Befehle, ohne Eingabeaufforderung)
- "p": Modus mit Eingabeaufforderung (mehrere Befehle mit Eingabeaufforderung)

Da standardmäßig der nicht interaktive Modus aktiv ist, muss "prompt" als erster Befehl verwendet werden, um ihn zu ändern. Andernfalls bewirkt der vorherige Befehl das Schließen der Verbindung. Beim Wechsel in den nicht interaktiven Modus wird die Verbindung geschlossen, sobald alle Befehle derselben Zeile abgeschlossen sind.

Aus diesem Grund beginnt man bei der manuellen Fehlersuche häufig mit dem Befehl "prompt":

```haproxy
# socat /var/run/haproxy readline
prompt
```

> show info ...

Interaktive Werkzeuge können mit "prompt i" beginnen, um in den interaktiven Modus ohne Eingabeaufforderung zu wechseln.

Optional kann die Laufzeit des Prozesses in der Eingabeaufforderung angezeigt werden. Der Befehl "prompt timed" aktiviert die Eingabeaufforderung und schaltet die Zeitanzeige um. Die Laufzeit wird im Format "d:hh:mm:ss" angezeigt, wobei "d" die Anzahl der Tage und "hh", "mm" und "ss" die Anzahl der Stunden, Minuten beziehungsweise Sekunden mit jeweils zwei Ziffern angeben:

```haproxy
# socat /var/run/haproxy readline
prompt timed
```

[23:03:34:39]\> show version 2.8-dev9-e5e622-18

[23:03:34:41]\> quit

Wenn die Laufzeitanzeige an der Master-CLI aktiviert ist, zeigt die Eingabeaufforderung die Laufzeit des aktuell ausgewählten Prozesses an. Dies funktioniert also für den Master, den aktuellen Worker oder einen älteren Worker:

```shell
master> prompt timed
[0:00:00:50] master> show proc
(...)
[0:00:00:58] master> @!11955     <-- Master, zum aktuellen Worker wechseln
[0:00:01:03] 11955> @!11942      <-- aktueller Worker, zum älteren Worker wechseln
[0:00:02:17] 11942> @            <-- älterer Worker, zurück zum Master wechseln
[0:00:01:10] master>
```

Da mehrere Befehle gleichzeitig eingegeben werden können, verwendet haproxy eine Leerzeile als Trennzeichen für das Ende der Ausgabe jedes Befehls. Dabei wird sichergestellt, dass kein Befehl selbst eine Leerzeile ausgeben kann. Ein Skript kann die Ausgabe dadurch auch dann leicht auswerten, wenn mehrere Befehle in einer einzigen Zeile übermittelt wurden.

Manche Befehle akzeptieren optionale Nutzdaten. Um einem Befehl Nutzdaten hinzuzufügen, muss die erste Zeile mit dem Muster "\<\<&#92;n" enden. Die folgenden Zeilen werden als Nutzdaten behandelt; es können beliebig viele Zeilen sein. Zum Bestätigen eines Befehls mit Nutzdaten muss die Eingabe mit einer Leerzeile enden.

Das Nutzdatenmuster kann angepasst werden, um das Ende der Nutzdaten anders zu kennzeichnen. Sollen Nutzdaten mit etwas anderem als einer Leerzeile enden, kann zwischen '\<\<' und '&#92;n' ein eigenes Muster festgelegt werden. Zusätzlich zu '\<\<' sind bis zu 64 Zeichen zulässig; andernfalls wird die Eingabe nicht als Nutzdaten erkannt. Dies sollte für zufällige Nutzdatenmuster ausreichen. Beispiel für eine PEM-Datei mit Leerzeilen und Kommentaren:

```haproxy
# echo -e "set ssl cert common.pem <<%EOF%\n$(cat common.pem)\n%EOF%\n" | \
socat /var/run/haproxy.stat -
```

Es gibt Einschränkungen: Das Muster "\<\<" darf nicht unmittelbar an das letzte Wort der Zeile angehängt werden. Die Länge einer Befehlszeile darf tune.bufsize nicht überschreiten. Dabei wird das Muster, das die Nutzdaten einleitet, mitgezählt, die Nutzdaten selbst jedoch nicht. Die Nutzdatengröße ist standardmäßig auf 128KB begrenzt. Dies kann mit dem globalen Parameter "tune.cli.max-payload-size" unter Beachtung einiger Vorsichtsmaßnahmen geändert werden. Beachten Sie, dass das Muster zum Beenden der Nutzdaten in diese Grenze einbezogen wird.

Während der Eingabe von Nutzdaten im interaktiven Modus wechselt die Eingabeaufforderung von "\> " zu "+ ".

Beachten Sie, dass bei mehreren haproxy-Prozessen, die auf denselben Sockets gestartet wurden, jeder beliebige Prozess die Anfrage annehmen kann und seine eigenen Statistiken ausgibt.

Die derzeit auf dem Statistik-Socket unterstützten Befehle sind unten aufgeführt. Bei einem unbekannten Befehl zeigt haproxy eine Bedienungshilfe mit allen unterstützten Befehlen an. Einige Befehle haben eine komplexere Syntax; bei einem Fehler wird in der Regel erläutert, welcher Teil des Befehls ungültig ist.

Manche Befehle erfordern höhere Berechtigungen. Reichen Ihre Berechtigungen nicht aus, erhalten Sie den Fehler "Permission denied". Weitere Informationen finden Sie bei der Option "level" der "bind"-Zeilen im Konfigurationshandbuch.

<a id="entry-9-3-abort-ssl-ca-file"></a>

**`abort ssl ca-file <cafile>`**

```haproxy
abort ssl ca-file <cafile>
```

Bricht eine temporäre Aktualisierungstransaktion für eine CA-Datei ab und verwirft sie.

Siehe auch "set ssl ca-file" und "commit ssl ca-file".

<a id="entry-9-3-abort-ssl-cert"></a>

**`abort ssl cert <filename>`**

```haproxy
abort ssl cert <filename>
```

Bricht eine temporäre Aktualisierungstransaktion für ein SSL-Zertifikat ab und verwirft sie.

Siehe auch "set ssl cert" und "commit ssl cert".

<a id="entry-9-3-abort-ssl-crl-file"></a>

**`abort ssl crl-file <crlfile>`**

```haproxy
abort ssl crl-file <crlfile>
```

Bricht eine temporäre Aktualisierungstransaktion für eine CRL-Datei ab und verwirft sie.

Siehe auch "set ssl crl-file" und "commit ssl crl-file".

<a id="entry-9-3-acme-renew"></a>

**`acme renew <certificate>`**

```haproxy
acme renew <certificate>
```

Startet eine ACME-Aufgabe zur Zertifikatserzeugung mit dem angegebenen Zertifikatsnamen. Das Zertifikat muss einem acme-Abschnitt zugeordnet sein; siehe Abschnitt [12.8](/de/haproxy/other-sections/#section-12-8) „ACME“ des Konfigurationshandbuchs. Siehe auch "acme status".

<a id="entry-9-3-acme-status"></a>

**`acme status`**

```haproxy
acme status
```

Zeigt den Status aller Zertifikate an, die mit ACME konfiguriert wurden.

Dieser Befehl gibt folgende Werte, durch Tabulatoren getrennt, aus:

- Den Namen des in HAProxy konfigurierten Zertifikats
- Den in der Konfiguration verwendeten acme-Abschnitt
- Den Status der acme-Aufgabe: "Running", "Scheduled" oder "Stopped"
- Das UTC-Ablaufdatum des Zertifikats im ISO8601-Format
- Die relative Zeit bis zum Ablauf (0d, falls abgelaufen)
- Den geplanten UTC-Termin des Zertifikats im ISO8601-Format
- Die relative Zeit bis zum geplanten Termin (0d bei Running)

Beispiel:

```shell
$ echo "@1; acme status" | socat /tmp/master.sock - | column -t -s $'\t'
# certificate   section  state      expiration date (UTC)  expires in        scheduled date (UTC)  scheduled in
ecdsa.pem       LE       Running    2020-01-18T09:31:12Z   0d 0h00m00s       2020-01-15T21:31:12Z  0d 0h00m00s
foobar.pem.rsa  LE       Scheduled  2025-08-04T11:50:54Z   89d 23h01m13s     2025-07-27T23:50:55Z  82d 11h01m14s
```

<a id="entry-9-3-add-acl"></a>

**`add acl [@<ver>] <acl> <pattern>`**

```haproxy
add acl [@<ver>] <acl> <pattern>
```

Fügt der ACL `<acl>` einen Eintrag hinzu. `<acl>` ist die von "show acl" zurückgegebene \#`<id>` oder der zurückgegebene `<name>`. Dieser Befehl prüft nicht, ob der Eintrag bereits vorhanden ist. Einträge werden der aktuellen Version der ACL hinzugefügt, sofern nicht mit "@`<ver>`" eine bestimmte Version angegeben wird. Diese Versionsnummer muss zuvor mit "prepare acl" zugewiesen worden sein und liegt zwischen den Versionen, die in der Ausgabe von "show acl" als "curr_ver" und "next_ver" gemeldet werden. Einträge, die mit einer bestimmten Versionsnummer hinzugefügt wurden, ergeben erst nach einer "commit acl"-Operation einen Treffer. Sie können jedoch mit dem Befehl "show acl @`<ver>`" eingesehen und mit "clear acl @`<ver>`" gelöscht werden. Dieser Befehl kann nicht verwendet werden, wenn die Referenz `<acl>` ein Name ist, der auch für eine Map verwendet wird. In diesem Fall muss stattdessen der Befehl "add map" verwendet werden.

<a id="entry-9-3-add-backend"></a>

**`add backend <name> from <defproxy> [mode <mode>] [guid <guid>]`**

```haproxy
add backend <name> from <defproxy> [mode <mode>] [guid <guid>]
```

Erzeugt eine neue Backend-Proxy-Instanz mit dem Namen `<name>`.

Es können nur TCP- oder HTTP-Proxys erzeugt werden. Alle Einstellungen werden von der Standard-Proxy-Instanz `<defproxy>` geerbt. Standardmäßig muss der Backend-Modus über das gleichnamige Argument angegeben werden, sofern `<defproxy>` ihn nicht bereits ausdrücklich festlegt. Bei Bedarf kann auch ein optionales GUID-Argument verwendet werden.

Server können mit dem Befehl "add server" hinzugefügt werden. Das Backend wird im unveröffentlichten Zustand initialisiert. Sobald es für den Datenverkehr bereit ist, kann die neu erzeugte Instanz mit "publish backend" verfügbar gemacht werden.

Alle benannten Standard-Proxys können verwendet werden, sofern sie dieselben Vererbungsregeln erfüllen, die beim Einlesen der Konfiguration gelten. Es gibt jedoch Ausnahmen, etwa wenn der Modus weder TCP noch HTTP ist.

Dieser Befehl ist eingeschränkt und kann nur über Sockets ausgeführt werden, die für die Berechtigungsstufe "admin" konfiguriert sind.

<a id="entry-9-3-add-map"></a>

**`add map [@<ver>] <map> <key> <value>`**

```haproxy
add map [@<ver>] <map> <key> <value>
add map [@<ver>] <map> <payload>
```

Fügt der Map `<map>` einen Eintrag hinzu, der dem Schlüssel `<key>` den Wert `<value>` zuordnet. Dieser Befehl prüft nicht, ob der Eintrag bereits vorhanden ist. Er dient hauptsächlich dazu, eine Map nach einer "clear"- oder "prepare"-Operation zu füllen. Einträge werden der aktuellen Version der ACL hinzugefügt, sofern nicht mit "@`<ver>`" eine bestimmte Version angegeben wird. Diese Versionsnummer muss zuvor mit "prepare acl" zugewiesen worden sein und liegt zwischen den Versionen, die in der Ausgabe von "show acl" als "curr_ver" und "next_ver" gemeldet werden. Einträge, die mit einer bestimmten Versionsnummer hinzugefügt wurden, ergeben erst nach einer "commit map"-Operation einen Treffer. Sie können jedoch mit dem Befehl "show map @`<ver>`" eingesehen und mit "clear acl @`<ver>`" gelöscht werden. Wird die bezeichnete Map auch als ACL verwendet, berücksichtigt die ACL nur den Teil `<key>` und ignoriert den Teil `<value>`. Mit der Nutzdatensyntax können mehrere Schlüssel-Wert-Paare hinzugefügt werden, indem jedes Paar in einer eigenen Zeile eingegeben wird. In jeder neuen Zeile ist das erste Wort der Schlüssel; der Rest der Zeile wird als Wert betrachtet und kann auch Leerzeichen enthalten.

Beispiel:

```shell
# socat /tmp/sock1 -
prompt

> add map #-1 <<
+ key1 value1
+ key2 value2 with spaces
+ key3 value3 also with spaces
+ key4 value4

>
```

<a id="entry-9-3-add-server"></a>

**`add server <backend>/<server> [args]*`**

```haproxy
add server <backend>/<server> [args]*
```

Erzeugt eine neue Serverinstanz im Backend `<backend>`.

Der Name `<server>` darf im Backend noch nicht verwendet werden. Für das Backend gilt die besondere Einschränkung, dass es einen dynamischen Lastverteilungsalgorithmus verwenden muss. Eine Teilmenge der Schlüsselwörter der server-Anweisung in der Konfigurationsdatei kann zur Konfiguration des Serververhaltens verwendet werden ("add server help" listet sie auf). Einstellungen einer eventuell vorhandenen 'default-server'-Anweisung im selben Backend werden nicht übernommen.

Derzeit wird ein dynamischer Server statisch mit der init-addr-Methode "none" initialisiert. Das bedeutet, dass keine Namensauflösung erfolgt, wenn als Adresse ein FQDN angegeben wird, auch wenn die Servererzeugung akzeptiert wird.

Damit Neuladevorgänge unterstützt werden, wird erwartet, dass der über die CLI erzeugte Server auch manuell in die entsprechende HAProxy-Konfigurationsdatei eingetragen wird. Ein dynamischer Server, der nicht in der Konfiguration vorhanden ist, wird nach einem Neuladevorgang nicht wiederhergestellt.

Ein dynamischer Server kann mit dem Schlüsselwort "track" den Prüfstatus eines anderen Servers aus der Konfiguration verfolgen. Es ist jedoch nicht möglich, einen anderen dynamischen Server zu verfolgen. Dadurch bleibt die Verfolgungskette auch dann konsistent, wenn dynamische Server gelöscht werden.

Mit dem Schlüsselwort "check" wird die Unterstützung für Health Checks aktiviert. Der Health Check ist standardmäßig deaktiviert und muss unabhängig vom Server mit dem Befehl "enable health" aktiviert werden. Für Agent-Prüfungen dienen das Schlüsselwort "agent-check" und der Befehl "enable agent". In diesem Fall kann der Agent den Server je nach gemeldetem Status aktivieren, ohne dass ausdrücklich "enable server" ausgeführt wird. Daher ist beim Entfernen eines dynamischen Servers mit Agent-Prüfung besondere Vorsicht erforderlich. Der Agent sollte zuerst mit "disable agent" deaktiviert werden, damit der Server vor dem Entfernen in den erforderlichen Wartungsmodus versetzt werden kann.

Bei einer großen Anzahl dynamischer Server kann die fd-Grenze erreicht werden. Siehe in diesem Fall die Dokumentation des globalen Schlüsselworts "u-limit".

<a id="entry-9-3-add-server-help"></a>

**`add server help`**

```haproxy
add server help
```

Listet die Schlüsselwörter auf, die die aktuelle HAProxy-Version für dynamische Server unterstützt. Die Syntax der Schlüsselwörter ähnelt der server-Zeile der Konfigurationsdatei; Einzelheiten stehen in der jeweiligen Dokumentation.

<a id="entry-9-3-add-ssl-ca-file"></a>

**`add ssl ca-file <cafile> <payload>`**

```haproxy
add ssl ca-file <cafile> <payload>
```

Fügt einer ca-file ein neues Zertifikat hinzu. Dieser Befehl ist nützlich, wenn die Puffergrößengrenze der CLI erreicht wurde und mehrere Zertifikate hinzugefügt werden sollen. Statt mit "set" alle Zertifikate auf einmal zu setzen, kann jedes Zertifikat einzeln hinzugefügt werden. "set ssl ca-file" setzt die ca-file zurück.

Beispiel:

```text
echo -e "set ssl ca-file cafile.pem <<\n$(cat rootCA.crt)\n" | \
socat /var/run/haproxy.stat -
echo -e "add ssl ca-file cafile.pem <<\n$(cat intermediate1.crt)\n" | \
socat /var/run/haproxy.stat -
echo -e "add ssl ca-file cafile.pem <<\n$(cat intermediate2.crt)\n" | \
socat /var/run/haproxy.stat -
echo "commit ssl ca-file cafile.pem" | socat /var/run/haproxy.stat -
```

<a id="entry-9-3-add-ssl-crt-list"></a>

**`add ssl crt-list <crtlist> <certificate>`**

```haproxy
add ssl crt-list <crtlist> <certificate>
add ssl crt-list <crtlist> <payload>
```

Fügt einer crt-list ein Zertifikat hinzu. Der Befehl kann auch für Verzeichnisse verwendet werden, da Verzeichnisse inzwischen auf dieselbe Weise wie crt-lists geladen werden. Mit diesem Befehl kann ein Zertifikatsname als Parameter angegeben werden. Für SSL-Optionen oder Filter muss stattdessen eine crt-list-Zeile als Nutzdaten gesendet werden. Die Nutzdaten unterstützen nur eine einzige crt-list-Zeile. Der Befehl lädt das Zertifikat für alle bind-Zeilen, die die crt-list verwenden. Um ein neues Zertifikat an HAProxy zu übertragen, müssen die Befehle "new ssl cert" und "set ssl cert" verwendet werden.

Beispiel:

```shell
$ echo "new ssl cert foobar.pem" | socat /tmp/sock1 -
$ echo -e "set ssl cert foobar.pem <<\n$(cat foobar.pem)\n" | socat
/tmp/sock1 -
$ echo "commit ssl cert foobar.pem" | socat /tmp/sock1 -
$ echo "add ssl crt-list certlist1 foobar.pem" | socat /tmp/sock1 -

$ echo -e 'add ssl crt-list certlist1 <<\nfoobar.pem [allow-0rtt] foo.bar.com
!test1.com\n' | socat /tmp/sock1 -
```

<a id="entry-9-3-add-ssl-ech"></a>

**`add ssl ech <bind> <payload>`**

```haproxy
add ssl ech <bind> <payload>
```

Fügt einer `<bind>`-Zeile einen ECH-Schlüssel hinzu. Die Nutzdaten müssen im PEM-for-ECH-Format vorliegen.
(<https://datatracker.ietf.org/doc/html/draft-farrell-tls-pemesni>)

Das Format der bind-Zeile ist `<frontend>`/@`<filename>`:`<linenum>` (Beispiel: frontend1/@haproxy.conf:19) oder `<frontend>`/`<name>`, wenn die bind-Zeile mit dem Schlüsselwort "name" benannt wurde.

Erfordert eine OpenSSL-Version mit ECH-Unterstützung. HAProxy muss mit USE_ECH=1 kompiliert sein. Dieser Befehl wird nur auf einer CLI-Verbindung im experimentellen Modus unterstützt (siehe "experimental-mode on").

Siehe auch "show ssl ech" und "ech" in [Abschnitt 5.1](/de/haproxy/bind-and-server-options/#section-5-1) des Konfigurationshandbuchs.

Beispiel:

```shell
$ openssl ech -public_name foobar.com -out foobar3.com.ech
$ echo -e "experimental-mode on; add ssl ech frontend1/@haproxy.conf:19 <<%EOF%\n$(cat foobar3.com.ech)\n%EOF%\n" | \
  socat /tmp/haproxy.sock -
added a new ECH config to frontend1
```

<a id="entry-9-3-add-ssl-jwt"></a>

**`add ssl jwt <filename>`**

```haproxy
add ssl jwt <filename>
```

Fügt ein bereits geladenes Zertifikat der Liste der Zertifikate hinzu, die für die JWT-Validierung verwendet werden können (siehe Konverter "jwt_verify_cert"). Dieser Befehl funktioniert nicht bei laufenden Transaktionen. Siehe auch die Befehle "del ssl jwt" und "show ssl jwt". Weitere Informationen stehen bei der Zertifikatsoption "jwt".

<a id="entry-9-3-clear-counters"></a>

**`clear counters`**

```haproxy
clear counters
```

Setzt die Höchstwerte der Statistikzähler in jedem Proxy (Frontend und Backend) und in jedem Server zurück. Die kumulierten Zähler bleiben unverändert. Die von "show activity" gemeldeten internen Aktivitätszähler werden ebenfalls zurückgesetzt. Damit lassen sich nach einem Vorfall die Zähler zurücksetzen, ohne neu starten oder die Verkehrszähler löschen zu müssen. Dieser Befehl ist eingeschränkt und kann nur über Sockets ausgeführt werden, die für die Berechtigungsstufen "operator" oder "admin" konfiguriert sind.

<a id="entry-9-3-clear-counters-all"></a>

**`clear counters all`**

```haproxy
clear counters all
```

Setzt alle Statistikzähler in jedem Proxy (Frontend und Backend) und in jedem Server zurück. Dies hat dieselbe Wirkung wie ein Neustart. Dieser Befehl ist eingeschränkt und kann nur über Sockets ausgeführt werden, die für die Berechtigungsstufe "admin" konfiguriert sind.

<a id="entry-9-3-clear-acl"></a>

**`clear acl [@<ver>] <acl>`**

```haproxy
clear acl [@<ver>] <acl>
```

Entfernt alle Einträge aus der ACL `<acl>`. `<acl>` ist die von "show acl" zurückgegebene \#`<id>` oder der zurückgegebene `<name>`. Wenn die Referenz `<acl>` ein Name ist, der auch für eine Map verwendet wird, wird diese Map ebenfalls geleert. Standardmäßig wird nur die aktuelle Version der ACL geleert (die Version, gegen die geprüft wird). Es kann jedoch eine andere Version angegeben werden, indem auf '@' die Versionsnummer folgt.

<a id="entry-9-3-clear-map"></a>

**`clear map [@<ver>] <map>`**

```haproxy
clear map [@<ver>] <map>
```

Entfernt alle Einträge aus der Map `<map>`. `<map>` ist die von "show map" zurückgegebene \#`<id>` oder der zurückgegebene `<name>`. Wenn die Referenz `<map>` ein Name ist, der auch für eine ACL verwendet wird, wird diese ACL ebenfalls geleert. Standardmäßig wird nur die aktuelle Version der Map geleert (die Version, gegen die geprüft wird). Es kann jedoch eine andere Version angegeben werden, indem auf '@' die Versionsnummer folgt.

<a id="entry-9-3-clear-table"></a>

**`clear table <table> [ data.<type> <operator> <value> ] | [ key <key> ] |`**

```haproxy
clear table <table> [ data.<type> <operator> <value> ] | [ key <key> ] |
                    [ ptr <ptr> ]
```

Entfernt Einträge aus der Stick Table `<table>`.

Dies wird üblicherweise verwendet, um die Sperre für Benutzer aufzuheben, die sich über einen ungerechtfertigt verweigerten Zugriff auf einen Dienst beschweren. Es können aber auch Einträge zur Sitzungsbindung gelöscht werden, die einem zu ersetzenden Server zugeordnet sind (Einzelheiten siehe "show table" weiter unten). Manchmal wird das Entfernen eines Eintrags verweigert, weil er gerade von einer Sitzung verfolgt wird. Üblicherweise genügt es, einige Sekunden später nach dem Ende der Sitzung einen neuen Versuch zu unternehmen.

Werden keine Optionsargumente angegeben, werden alle Einträge entfernt.

Bei der Form "data." werden Einträge entfernt, auf die ein Filter anhand der gespeicherten Daten zutrifft (siehe "stick-table" in Abschnitt 4.2). In `<type>` muss ein gespeicherter Datentyp angegeben werden. Dieser Datentyp muss in der Tabelle gespeichert sein, andernfalls wird ein Fehler gemeldet. Die Daten werden gemäß `<operator>` mit der 64-Bit-Ganzzahl `<value>` verglichen. Es gelten dieselben Operatoren wie bei ACLs:

    - eq: erfasst Einträge, deren Daten diesem Wert entsprechen
    - ne: erfasst Einträge, deren Daten diesem Wert nicht entsprechen
    - le: erfasst Einträge, deren Daten kleiner oder gleich diesem Wert sind
    - ge: erfasst Einträge, deren Daten größer oder gleich diesem Wert sind
    - lt: erfasst Einträge, deren Daten kleiner als dieser Wert sind
    - gt: erfasst Einträge, deren Daten größer als dieser Wert sind

Bei der key-Form wird der Eintrag `<key>` entfernt. Der Schlüssel muss denselben Typ wie die Tabelle haben; derzeit sind nur IPv4, IPv6, Ganzzahl und Zeichenfolge möglich.

Bei der ptr-Form wird der Eintrag `<ptr>` entfernt. `<ptr>` wird in der Form 0xffff geschrieben und muss der Adresse entsprechen, die ein zuvor ausgeführter "show table"-Befehl zurückgegeben hat. Das Identifizieren eines Eintrags über seinen Zeiger kann sinnvoll sein, wenn dies über den Schlüssel wegen eines leeren Schlüssels oder mit der CLI inkompatibler Zeichen nicht möglich ist.

Wenn data.`<type>` ein Array-Typ ist, kann mit "[]" auf einen bestimmten Index im Array zugegriffen werden, etwa so: data.gpt[1]

Beispiel:

```shell
    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a4c: key=127.0.0.1 use=0 exp=3594729 gpc0=0 conn_rate(30000)=1 \
      bytes_out_rate(60000)=187
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191
>>> 0x80e6b40: key=127.0.0.3 use=0 exp=3594743 gpc0=2 conn_rate(30000)=10 \
      bytes_out_rate(60000)=200

    $ echo "clear table http_proxy key 127.0.0.1" | socat stdio /tmp/sock1

    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:1
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
>>> 0x80e6b40: key=127.0.0.3 use=0 exp=3594743 gpc0=2 conn_rate(30000)=10 \
      bytes_out_rate(60000)=200
      bytes_out_rate(60000)=191
    $ echo "clear table http_proxy data.gpc0 eq 1" | socat stdio /tmp/sock1
    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:1
>>> 0x80e6b40: key=127.0.0.3 use=0 exp=3594743 gpc0=2 conn_rate(30000)=10 \
      bytes_out_rate(60000)=200

    $ echo "clear table http_proxy ptr 0x80e6b40" | socat stdio /tmp/sock1
    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:0
```

<a id="entry-9-3-commit-acl"></a>

**`commit acl @<ver> <acl>`**

```haproxy
commit acl @<ver> <acl>
```

Übernimmt alle Änderungen an Version `<ver>` der ACL `<acl>` und löscht alle früheren Versionen. `<acl>` ist die von "show acl" zurückgegebene \#`<id>` oder der zurückgegebene `<name>`. Die Versionsnummer muss zwischen "curr_ver"+1 und "next_ver" liegen, wie von "show acl" gemeldet. Der zu übernehmende ACL-Inhalt kann bei Bedarf mit "show acl @`<ver>` `<acl>`" eingesehen werden. Die angegebene Versionsnummer wurde normalerweise mit dem Befehl "prepare acl" erzeugt. Die Ersetzung erfolgt atomar: Die aktuelle Version wird atomar auf die angegebene Version gesetzt. Dadurch werden alle Einträge anderer Versionen sofort unsichtbar und alle Einträge der neuen Version sichtbar. Mit diesem Befehl können auch sämtliche sichtbaren Einträge einer ACL atomar entfernt werden, indem zuerst "prepare acl" aufgerufen wird und anschließend die Version übernommen wird, ohne Einträge hinzuzufügen. Dieser Befehl kann nicht verwendet werden, wenn die Referenz `<acl>` ein Name ist, der auch für eine Map verwendet wird. In diesem Fall muss stattdessen der Befehl "commit map" verwendet werden.

<a id="entry-9-3-commit-map"></a>

**`commit map @<ver> <map>`**

```haproxy
commit map @<ver> <map>
```

Übernimmt alle Änderungen an Version `<ver>` der Map `<map>` und löscht alle früheren Versionen. `<map>` ist die von "show map" zurückgegebene \#`<id>` oder der zurückgegebene `<name>`. Die Versionsnummer muss zwischen "curr_ver"+1 und "next_ver" liegen, wie von "show map" gemeldet. Der zu übernehmende Map-Inhalt kann bei Bedarf mit "show map @`<ver>` `<map>`" eingesehen werden. Die angegebene Versionsnummer wurde normalerweise mit dem Befehl "prepare map" erzeugt. Die Ersetzung erfolgt atomar: Die aktuelle Version wird atomar auf die angegebene Version gesetzt. Dadurch werden alle Einträge anderer Versionen sofort unsichtbar und alle Einträge der neuen Version sichtbar. Mit diesem Befehl können auch sämtliche sichtbaren Einträge einer Map atomar entfernt werden, indem zuerst "prepare map" aufgerufen wird und anschließend die Version übernommen wird, ohne Einträge hinzuzufügen.

<a id="entry-9-3-commit-ssl-ca-file"></a>

**`commit ssl ca-file <cafile>`**

```haproxy
commit ssl ca-file <cafile>
```

Übernimmt eine temporäre Transaktion zur Aktualisierung einer SSL-CA-Datei.

Bei einer bestehenden CA-Datei (Status "Used" in "show ssl ca-file") wird der neue CA-Dateieintrag in den CA-Dateibaum eingefügt. Jede Instanz, die den CA-Dateieintrag verwendet hat, wird zusammen mit den benötigten SSL-Kontexten neu aufgebaut. Alle zuvor von den neu aufgebauten Instanzen verwendeten Kontexte werden entfernt. Bei Erfolg wird der bisherige CA-Dateieintrag aus dem Baum entfernt. Bei einem Fehlschlag wird nichts entfernt oder gelöscht; alle ursprünglichen SSL-Kontexte bleiben erhalten und werden weiterhin verwendet. Sobald die temporäre Transaktion übernommen wurde, wird sie zerstört.

Bei einer neuen CA-Datei (nach "new ssl ca-file", Status "Unused" in "show ssl ca-file") wird die CA-Datei in den CA-Dateibaum eingefügt, aber nirgendwo in HAProxy verwendet. Um sie zu verwenden und SSL-Kontexte zu erzeugen, die sie nutzen, muss sie mit "add ssl crt-list" einer crt-list hinzugefügt werden.

Siehe auch "new ssl ca-file", "set ssl ca-file", "add ssl ca-file", "abort ssl ca-file" und "add ssl crt-list".

<a id="entry-9-3-commit-ssl-cert"></a>

**`commit ssl cert <filename>`**

```haproxy
commit ssl cert <filename>
```

Übernimmt eine temporäre Transaktion zur Aktualisierung eines SSL-Zertifikats.

Bei einem bestehenden Zertifikat (Status "Used" in "show ssl cert") werden alle benötigten SSL-Kontexte und SNIs erzeugt und eingefügt; die bisherigen werden entfernt. Die bisherigen SSL-Zertifikate werden im Speicher überall dort ersetzt, wo `<filename>` in der Konfiguration verwendet wurde. Bei einem Fehlschlag wird nichts entfernt oder eingefügt. Sobald die temporäre Transaktion übernommen wurde, wird sie zerstört.

Bei einem neuen Zertifikat (nach "new ssl cert", Status "Unused" in "show ssl cert") wird das Zertifikat in einen Zertifikatsspeicher übernommen, aber nirgendwo in HAProxy verwendet. Um es zu verwenden und seine SNIs zu erzeugen, muss es mit "add ssl crt-list" einer crt-list oder einem Verzeichnis hinzugefügt werden.

Siehe auch "new ssl cert", "set ssl cert", "abort ssl cert" und "add ssl crt-list".

<a id="entry-9-3-commit-ssl-crl-file"></a>

**`commit ssl crl-file <crlfile>`**

```haproxy
commit ssl crl-file <crlfile>
```

Übernimmt eine temporäre Transaktion zur Aktualisierung einer SSL-CRL-Datei.

Bei einer bestehenden CRL-Datei (Status "Used" in "show ssl crl-file") wird der neue CRL-Dateieintrag in den CA-Dateibaum eingefügt, der sowohl CA-Dateien als auch CRL-Dateien enthält. Jede Instanz, die den CRL-Dateieintrag verwendet hat, wird zusammen mit den benötigten SSL-Kontexten neu aufgebaut. Alle zuvor von den neu aufgebauten Instanzen verwendeten Kontexte werden entfernt. Bei Erfolg wird der bisherige CRL-Dateieintrag aus dem Baum entfernt. Bei einem Fehlschlag wird nichts entfernt oder gelöscht; alle ursprünglichen SSL-Kontexte bleiben erhalten und werden weiterhin verwendet. Sobald die temporäre Transaktion übernommen wurde, wird sie zerstört.

Bei einer neuen CRL-Datei (nach "new ssl crl-file", Status "Unused" in "show ssl crl-file") wird die CRL-Datei in den CRL-Dateibaum eingefügt, aber nirgendwo in HAProxy verwendet. Um sie zu verwenden und SSL-Kontexte zu erzeugen, die sie nutzen, muss sie mit "add ssl crt-list" einer crt-list hinzugefügt werden.

Siehe auch "new ssl crl-file", "set ssl crl-file", "abort ssl crl-file" und "add ssl crt-list".

<a id="entry-9-3-debug-counters"></a>

**`debug counters [reset|show|on|off|all|bug|chk|cnt|glt|?]*`**

```haproxy
debug counters [reset|show|on|off|all|bug|chk|cnt|glt|?]*
```

Listet interne, im Code platzierte Zähler auf, die je nach Build-Optionen unterschiedlich sein können. Einige hängen von DEBUG_STRICT ab, andere von DEBUG_COUNTERS. Der Befehl akzeptiert eine Kombination mehrerer Argumente, von denen manche Aktionen und andere Filter festlegen: - bug aktiviert die Auflistung der Zähler für BUG_ON()-Anweisungen - cnt aktiviert die Auflistung der Zähler für COUNT_IF()-Anweisungen - chk aktiviert die Auflistung der Zähler für CHECK_IF()-Anweisungen - glt aktiviert die Auflistung der Zähler für COUNT_GLITCH()-Anweisungen - all zeigt auch Zähler an, die nie ausgelöst wurden (Wert 0) - Aktion off: deaktiviert die Aktualisierung der COUNT_IF()-Zähler - Aktion on: aktiviert die Aktualisierung der COUNT_IF()-Zähler - Aktion reset: setzt alle angegebenen Zähler zurück - Aktion show: zeigt alle angegebenen Zähler an

Standardmäßig gilt die Aktion "show", um Zähler anzuzeigen; aufgelistet werden alle Zählertypen mit einem Wert ungleich null. Der Befehl "show" gilt implizit, wenn keine andere Aktion angegeben ist. Er ist nur vorhanden, um das Erzeugen von Befehlen aus Skripten zu erleichtern.

Die Ausgabe beginnt mit einem ganzzahligen Zähler, gefolgt vom Zählertyp in Großbuchstaben, seiner Position im Code (file:line), dem Funktionsnamen und optional ": " samt einer Beschreibung. Das Ausgabeformat kann sich zwischen Hauptversionen ändern. Neue Typen und Einträge können zur Verbesserung der Fehlerdiagnose in stabile Versionen zurückportiert werden. Eine Überwachung dieser Zähler sollte nur mit sehr großzügiger und toleranter Auswertung erfolgen, vorzugsweise überhaupt nicht.

Normalerweise verwenden Endbenutzer diesen Befehl nicht. Ein Entwickler, der die Ursache eines Problems ermittelt und nach CNT- oder GLT-Einträgen sucht, kann sie jedoch darum bitten. "CHK"-Einträge mit einem Wert ungleich null sollten nicht auftreten und sollten den Entwicklern gemeldet werden, da sie auf falsche Annahmen im Code hindeuten können.

<a id="entry-9-3-debug-dev"></a>

**`debug dev <command> [args]*`**

```haproxy
debug dev <command> [args]*
```

Ruft einen entwicklerspezifischen Befehl auf. Dies wird nur auf einer CLI-Verbindung im Expertenmodus unterstützt (siehe "expert-mode on"). Solche Befehle sind äußerst gefährlich und verzeihen keine Fehler; jede Fehlanwendung kann den Prozess zum Absturz bringen. Sie sind ausschließlich für Experten vorgesehen und dürfen keinesfalls verwendet werden, sofern keine entsprechende Anweisung vorliegt. Einige sind nur verfügbar, wenn HAProxy mit definiertem DEBUG_DEV gebaut wurde, da sie Auswirkungen auf die Sicherheit haben können. Alle diese Befehle erfordern admin-Berechtigungen. Sie sind bewusst nicht dokumentiert, um ihre Verwendung durch Personen zu vermeiden, die mit dem Quellcode nicht vertraut sind.

<a id="entry-9-3-del-acl"></a>

**`del acl <acl> [<key>|#<ref>]`**

```haproxy
del acl <acl> [<key>|#<ref>]
```

Löscht alle Einträge der ACL `<acl>`, die dem Schlüssel `<key>` entsprechen. `<acl>` ist die von "show acl" zurückgegebene \#`<id>` oder der zurückgegebene `<name>`. Wenn `<ref>` verwendet wird, löscht dieser Befehl nur die angegebene Referenz. Die Referenz lässt sich durch Auflisten des ACL-Inhalts ermitteln. Wenn die Referenz `<acl>` ein Name ist, der auch für eine Map verwendet wird, wird der Eintrag auch aus der Map gelöscht.

<a id="entry-9-3-del-backend"></a>

**`del backend <name>`**

```haproxy
del backend <name>
```

Entfernt den Backend-Proxy mit dem Namen `<name>`.

Diese Operation ist nur für TCP- oder HTTP-Proxys möglich. Damit sie gelingt, muss zuvor die Veröffentlichung der Backend-Instanz aufgehoben worden sein. Außerdem müssen zuerst alle ihre Server entfernt werden (über den CLI-Befehl "del server"). Schließlich darf kein Stream mehr mit der Backend-Instanz verbunden sein.

Weitere Einschränkungen verhindern das Entfernen eines Backends. Ein Backend kann nicht entfernt werden, wenn Konfigurationselemente ausdrücklich darauf verweisen, etwa eine use_backend-Regel oder Sample-Ausdrücke. Manche Proxy-Optionen sind ebenfalls mit dem Löschen zur Laufzeit inkompatibel. Derzeit gilt dies, wenn das veraltete dispatch oder option transparent verwendet wird. Ein Backend kann auch nicht entfernt werden, wenn darin eine stick-table deklariert ist. Schließlich ist es derzeit unmöglich, ein Backend zu entfernen, in dem QUIC-Server vorhanden waren.

Es kann sinnvoll sein, vor diesem Befehl "wait be-removable" zu verwenden, um die genannten Voraussetzungen zu prüfen. Damit lässt sich auch auf das endgültige Schließen der Streams warten, die mit dem Ziel-Backend verbunden sind.

Dieser Befehl ist eingeschränkt und kann nur über Sockets ausgeführt werden, die für die Berechtigungsstufe "admin" konfiguriert sind.

<a id="entry-9-3-del-map"></a>

**`del map <map> [<key>|#<ref>]`**

```haproxy
del map <map> [<key>|#<ref>]
```

Löscht alle Einträge der Map `<map>`, die dem Schlüssel `<key>` entsprechen. `<map>` ist die von "show map" zurückgegebene \#`<id>` oder der zurückgegebene `<name>`. Wenn `<ref>` verwendet wird, löscht dieser Befehl nur die angegebene Referenz. Die Referenz lässt sich durch Auflisten des Map-Inhalts ermitteln. Wenn die Referenz `<map>` ein Name ist, der auch für eine ACL verwendet wird, wird der Eintrag auch aus der Map gelöscht.

<a id="entry-9-3-del-ssl-ca-file"></a>

**`del ssl ca-file <cafile>`**

```haproxy
del ssl ca-file <cafile>
```

Löscht einen CA-Dateibaumeintrag aus HAProxy. Die CA-Datei muss unbenutzt und aus allen crt-lists entfernt sein. "show ssl ca-file" zeigt den Status der CA-Dateien an. Das Löschen funktioniert nicht bei einem Zertifikat, auf das in der Konfiguration direkt mit den Direktiven "ca-file" oder "ca-verify-file" verwiesen wird.

<a id="entry-9-3-del-ssl-cert"></a>

**`del ssl cert <certfile>`**

```haproxy
del ssl cert <certfile>
```

Löscht einen Zertifikatsspeicher aus HAProxy. Das Zertifikat muss unbenutzt sein (auch für die JWT-Validierung) und aus allen crt-lists oder Verzeichnissen entfernt sein. "show ssl cert" zeigt den Status des Zertifikats an. Das Löschen funktioniert nicht bei einem Zertifikat, auf das in der Konfiguration direkt mit der Direktive "crt" verwiesen wird.

<a id="entry-9-3-del-ssl-crl-file"></a>

**`del ssl crl-file <crlfile>`**

```haproxy
del ssl crl-file <crlfile>
```

Löscht einen CRL-Dateibaumeintrag aus HAProxy. Die CRL-Datei muss unbenutzt und aus allen crt-lists entfernt sein. "show ssl crl-file" zeigt den Status der CRL-Dateien an. Das Löschen funktioniert nicht bei einem Zertifikat, auf das in der Konfiguration direkt mit der Direktive "crl-file" verwiesen wird.

<a id="entry-9-3-del-ssl-crt-list"></a>

**`del ssl crt-list <filename> <certfile[:line]>`**

```haproxy
del ssl crt-list <filename> <certfile[:line]>
```

Löscht einen Eintrag aus einer crt-list. Dabei werden alle in den Frontends für diesen Eintrag verwendeten SNIs gelöscht. Wird ein Zertifikat mehrmals in einer crt-list verwendet, muss angegeben werden, welche Zeile gelöscht werden soll. Die Zeilennummern werden mit "show ssl crt-list -n `<crtlist>`" angezeigt.

<a id="entry-9-3-del-ssl-ech"></a>

**`del ssl ech <bind>`**

```haproxy
del ssl ech <bind>
```

Löscht die ECH-Schlüssel einer bind-Zeile.

Das Format der bind-Zeile ist `<frontend>`/@`<filename>`:`<linenum>` (Beispiel: frontend1/@haproxy.conf:19) oder `<frontend>`/`<name>`, wenn die bind-Zeile mit dem Schlüsselwort "name" benannt wurde.

Erfordert eine OpenSSL-Version mit ECH-Unterstützung. HAProxy muss mit USE_ECH=1 kompiliert sein. Dieser Befehl wird nur auf einer CLI-Verbindung im experimentellen Modus unterstützt (siehe "experimental-mode on").

Siehe auch "show ssl ech", "add ssl ech" und "ech" in [Abschnitt 5.1](/de/haproxy/bind-and-server-options/#section-5-1) des Konfigurationshandbuchs.

Beispiel:

```shell
$ echo "experimental-mode on; del ssl ech frontend1/@haproxy.conf:19" | socat /tmp/haproxy.sock -
deleted all ECH configs from frontend1/@haproxy.conf:19
```

<a id="entry-9-3-del-ssl-jwt"></a>

**`del ssl jwt <filename>`**

```haproxy
del ssl jwt <filename>
```

Entfernt ein bereits geladenes Zertifikat aus der Liste der Zertifikate, die für die JWT-Validierung verwendet werden können (siehe Konverter "jwt_verify_cert"). Dieser Befehl funktioniert nicht bei laufenden Transaktionen. Siehe auch die Befehle "add ssl jwt" und "show ssl jwt". Weitere Informationen stehen bei der Zertifikatsoption "jwt".

<a id="entry-9-3-del-server"></a>

**`del server <backend>/<server>`**

```haproxy
del server <backend>/<server>
```

Löscht einen entfernbaren Server aus dem Backend `<backend>`. Ein Server ist entfernbar, wenn er alle folgenden Bedingungen erfüllt:

- Andere Konfigurationselemente verweisen nicht auf ihn
- Er muss bereits im Wartungsmodus sein (siehe "disable server")
- Er darf keine aktiven oder inaktiven Verbindungen haben

Ist eine dieser Bedingungen nicht erfüllt, schlägt der Befehl fehl.

Aktive Verbindungen haben mindestens eine laufende Anfrage. Ihr Beenden lässt sich mit "shutdown sessions server" beschleunigen. Es wird dringend empfohlen, vor "del server" den Befehl "wait srv-removable" zu verwenden, um sicherzustellen, dass alle aktiven oder inaktiven Verbindungen geschlossen sind und der Befehl gelingt.

<a id="entry-9-3-disable-agent"></a>

**`disable agent <backend>/<server>`**

```haproxy
disable agent <backend>/<server>
```

Kennzeichnet die zusätzliche Agent-Prüfung als vorübergehend angehalten.

Wird aufgrund des Parameters agent-check einer server-Direktive eine Agent-Prüfung als zusätzliche Prüfung ausgeführt, werden neue Prüfungen nur initialisiert, wenn der Agent aktiviert ist. Daher verhindert disable agent das Starten neuer Agent-Prüfungen, bis der Agent mit enable agent wieder aktiviert wird.

Wenn ein Agent deaktiviert wird, werden zusätzliche Agent-Prüfungen, die noch bei aktiviertem Agenten gestartet wurden, wie folgt verarbeitet: Alle Ergebnisse, die das Gewicht ändern würden, insbesondere "drain" oder ein vom Agenten zurückgegebenes Gewicht, werden ignoriert. Ansonsten bleibt die Verarbeitung der Agent-Prüfung unverändert.

Diese Funktion soll die gewichtsändernde Wirkung der Agent-Prüfungen anhalten, damit das Gewicht eines Servers mit set weight eingestellt werden kann, ohne vom Agenten überschrieben zu werden.

Dieser Befehl ist eingeschränkt und kann nur über Sockets ausgeführt werden, die für die Berechtigungsstufe "admin" konfiguriert sind.

<a id="entry-9-3-disable-dynamic-cookie-backend"></a>

**`disable dynamic-cookie backend <backend>`**

```haproxy
disable dynamic-cookie backend <backend>
```

Deaktiviert die Erzeugung dynamischer Cookies für das Backend `<backend>`

<a id="entry-9-3-disable-frontend"></a>

**`disable frontend <frontend>`**

```haproxy
disable frontend <frontend>
```

Kennzeichnet das Frontend als vorübergehend angehalten. Dies entspricht dem bei einem sanften Neustart verwendeten Modus: Das Frontend gibt den Port frei, kann bei Bedarf aber wieder aktiviert werden. Dies sollte mit Vorsicht verwendet werden, da einige Betriebssysteme außer Linux es nicht wieder aktivieren können. Diese Funktion ist für Umgebungen vorgesehen, in denen das Anhalten eines Proxys undenkbar ist, aber ein falsch konfigurierter Proxy korrigiert werden muss. So lässt sich der Port freigeben und von einem anderen Prozess binden, um den Betrieb wiederherzustellen. Das Frontend wird auf der Statistikseite mit dem Status "STOP" angezeigt.

Das Frontend kann entweder über seinen Namen oder über seine numerische ID mit vorangestelltem Rautezeichen ('#') angegeben werden.

Dieser Befehl ist eingeschränkt und kann nur über Sockets ausgeführt werden, die für die Berechtigungsstufe "admin" konfiguriert sind.

<a id="entry-9-3-disable-health"></a>

**`disable health <backend>/<server>`**

```haproxy
disable health <backend>/<server>
```

Kennzeichnet den primären Health Check als vorübergehend angehalten. Dadurch werden keine Health Checks mehr gesendet, und das Ergebnis des letzten Health Checks wird ignoriert. Der Server befindet sich im ungeprüften Zustand und gilt als UP, sofern eine zusätzliche Agent-Prüfung ihn nicht auf DOWN setzt.

Dieser Befehl ist eingeschränkt und kann nur über Sockets ausgeführt werden, die für die Berechtigungsstufe "admin" konfiguriert sind.

<a id="entry-9-3-disable-server"></a>

**`disable server <backend>/<server>`**

```haproxy
disable server <backend>/<server>
```

Kennzeichnet den Server für Wartungsarbeiten als DOWN. In diesem Modus werden keine weiteren Prüfungen auf dem Server ausgeführt, bis er den Wartungsmodus verlässt. Wird der Server von anderen Servern verfolgt, werden auch diese während der Wartung auf DOWN gesetzt.

Auf der Statistikseite wird ein wegen Wartung auf DOWN gesetzter Server mit dem Status "MAINT" angezeigt; Server, die ihn verfolgen, erscheinen mit "MAINT(via)".

Sowohl das Backend als auch der Server können entweder über ihren Namen oder über ihre numerische ID mit vorangestelltem Rautezeichen ('#') angegeben werden.

Dieser Befehl ist eingeschränkt und kann nur über Sockets ausgeführt werden, die für die Berechtigungsstufe "admin" konfiguriert sind.

<a id="entry-9-3-dump-ssl-cert"></a>

**`dump ssl cert <certfile>`**

```haproxy
dump ssl cert <certfile>
```

Gibt ein in den HAProxy-Speicher geladenes Zertifikat aus. Die Ausgabe erfolgt im PEM-Format: zuerst der private Schlüssel, dann das Endzertifikat und schließlich die Zertifikatskette. Auch eine Transaktion kann ausgegeben werden, indem dem Dateinamen ein Sternchen vorangestellt wird. Dies ist nützlich, um Zertifikate im Dateisystem zu speichern, wenn sie über die CLI und nicht im Dateisystem aktualisiert wurden.

Dieser Befehl ist eingeschränkt und kann nur über Sockets ausgeführt werden, die für die Berechtigungsstufe "admin" konfiguriert sind.

Beispiele:

```shell
$ echo "dump ssl cert cert1.pem" | socat /tmp/sock1 -

$ echo "dump ssl cert cert1.pem" | socat /tmp/sock1 - | openssl storeutl -noout -text /dev/stdin
```

<a id="entry-9-3-dump-stats-file"></a>

**`dump stats-file`**

```haproxy
dump stats-file
```

Erzeugt eine Statistikdatei (stats-file), mit der die HAProxy-Zählerwerte beim Start vorgeladen werden können. Weitere Einzelheiten stehen im Abschnitt „Statistikdatei“.

<a id="entry-9-3-echo"></a>

**`echo <text>`**

```haproxy
echo <text>
```

Gibt Text über die CLI aus. Dies kann nützlich sein, um Kommentare zwischen Befehlen auszugeben, wenn die Ergebnisse mehrerer Befehle ausgegeben werden.

Beispiel:

```text
echo "expert-mode on; echo FDs from fdtab; show fd; echo wild FDs; debug dev fd" | socat /var/run/haproxy.sock -

```

<a id="entry-9-3-enable-agent"></a>

**`enable agent <backend>/<server>`**

```haproxy
enable agent <backend>/<server>
```

Setzt eine vorübergehend angehaltene zusätzliche Agent-Prüfung fort.

Einzelheiten zu den Auswirkungen des vorübergehenden Startens und Anhaltens eines zusätzlichen Agenten stehen unter "disable agent".

Dieser Befehl ist eingeschränkt und kann nur über Sockets ausgeführt werden, die für die Berechtigungsstufe "admin" konfiguriert sind.

<a id="entry-9-3-enable-dynamic-cookie-backend"></a>

**`enable dynamic-cookie backend <backend>`**

```haproxy
enable dynamic-cookie backend <backend>
```

Aktiviert die Erzeugung dynamischer Cookies für das Backend `<backend>`. Außerdem muss ein geheimer Schlüssel bereitgestellt werden.

<a id="entry-9-3-enable-frontend"></a>

**`enable frontend <frontend>`**

```haproxy
enable frontend <frontend>
```

Setzt ein vorübergehend angehaltenes Frontend fort. Einige der lauschenden Ports können möglicherweise nicht mehr gebunden werden (etwa wenn ein anderer Prozess sie seit der Operation 'disable frontend' belegt hat). In diesem Fall wird ein Fehler angezeigt. Manche Betriebssysteme können ein deaktiviertes Frontend möglicherweise nicht wieder aktivieren.

Das Frontend kann entweder über seinen Namen oder über seine numerische ID mit vorangestelltem Rautezeichen ('#') angegeben werden.

Dieser Befehl ist eingeschränkt und kann nur über Sockets ausgeführt werden, die für die Berechtigungsstufe "admin" konfiguriert sind.

<a id="entry-9-3-enable-health"></a>

**`enable health <backend>/<server>`**

```haproxy
enable health <backend>/<server>
```

Setzt einen vorübergehend angehaltenen primären Health Check fort. Dadurch werden wieder Health Checks gesendet. Einzelheiten stehen unter "disable health".

Dieser Befehl ist eingeschränkt und kann nur über Sockets ausgeführt werden, die für die Berechtigungsstufe "admin" konfiguriert sind.

<a id="entry-9-3-enable-server"></a>

**`enable server <backend>/<server>`**

```haproxy
enable server <backend>/<server>
```

Wenn der Server zuvor für Wartungsarbeiten als DOWN gekennzeichnet wurde, wird er als UP gekennzeichnet und die Prüfungen werden wieder aktiviert.

Sowohl das Backend als auch der Server können entweder über ihren Namen oder über ihre numerische ID mit vorangestelltem Rautezeichen ('#') angegeben werden.

Dieser Befehl ist eingeschränkt und kann nur über Sockets ausgeführt werden, die für die Berechtigungsstufe "admin" konfiguriert sind.

<a id="entry-9-3-experimental-mode"></a>

**`experimental-mode [on|off]`**

```haproxy
experimental-mode [on|off]
```

Ohne Optionen zeigt dieser Befehl an, ob der experimentelle Modus für die aktuelle Verbindung aktiviert oder deaktiviert ist. Mit "on" wird der experimentelle Modus nur für die aktuelle CLI-Verbindung aktiviert, mit "off" deaktiviert.

Der experimentelle Modus ermöglicht den Zugriff auf zusätzliche Funktionen, die sich noch in Entwicklung befinden. Diese Funktionen sind derzeit nicht stabil und sollten mit Vorsicht verwendet werden. Zwischen Versionen können inkompatible Änderungen auftreten.

Bei Verwendung über die Master-CLI sollte dieser Befehl kein Präfix erhalten, da er den Modus für jeden Worker setzt, wenn eine Verbindung zu dessen CLI hergestellt wird.

Beispiel:

```text
echo "@1; experimental-mode on; <experimental_cmd>..." | socat /var/run/haproxy.master -
echo "experimental-mode on; @1 <experimental_cmd>..." | socat /var/run/haproxy.master -
```

<a id="entry-9-3-expert-mode"></a>

**`expert-mode [on|off]`**

```haproxy
expert-mode [on|off]
```

Dieser Befehl ähnelt experimental-mode, schaltet jedoch den Expertenmodus um.

Der Expertenmodus zeigt Expertenbefehle an, die für den Prozess äußerst gefährlich sein können und Entwicklern gelegentlich helfen, wichtige Informationen über komplexe Fehler zu sammeln. Eine Fehlanwendung dieser Funktionen führt wahrscheinlich zu einem Prozessabsturz. Diese Option darf nur nach entsprechender Aufforderung verwendet werden. Dieser Befehl wird bewusst nicht in der Hilfemeldung aufgelistet. Er ist nur auf der Berechtigungsstufe admin zugänglich. Ein Wechsel auf eine andere Stufe setzt den Expertenmodus automatisch zurück.

Bei Verwendung über die Master-CLI sollte dieser Befehl kein Präfix erhalten, da er den Modus für jeden Worker setzt, wenn eine Verbindung zu dessen CLI hergestellt wird.

Beispiel:

```text
echo "@1; expert-mode on; debug dev exit 1" | socat /var/run/haproxy.master -
echo "expert-mode on; @1 debug dev exit 1" | socat /var/run/haproxy.master -
```

<a id="entry-9-3-get-map"></a>

**`get map <map> <value>`**

```haproxy
get map <map> <value>
get acl <acl> <value>
```

Sucht den Wert `<value>` in der Map `<map>` oder in der ACL `<acl>`. `<map>` oder `<acl>` stehen für die von "show map" oder "show acl" zurückgegebene \#`<id>` oder den zurückgegebenen `<name>`. Dieser Befehl gibt alle übereinstimmenden Muster zurück, die dieser Map zugeordnet sind. Dies ist bei der Fehlerdiagnose von Maps und ACLs nützlich. Das Ausgabeformat besteht aus einer Zeile pro Abgleichstyp. Jede Zeile besteht aus einer Folge von Wörtern, die durch Leerzeichen getrennt sind.

Die ersten beiden Wörter sind:

```text
<match method>:   Die angewendete Abgleichmethode. Möglich sind "found", "bool",
                  "int", "ip", "bin", "len", "str", "beg", "sub", "dir",
                  "dom", "end" oder "reg".

<match result>:   Das Ergebnis. Möglich sind "match" oder "no-match".
```

Die folgenden Wörter werden nur zurückgegeben, wenn das Muster auf einen Eintrag zutrifft.

     `<index type>`:     "tree" oder "list". Der interne Suchalgorithmus.

     `<case>`:           "case-insensitive" oder "case-sensitive". Die
                       Berücksichtigung der Groß-/Kleinschreibung.

     `<entry matched>`:  match="`<entry>`". Gibt das übereinstimmende Muster zurück.
                       Dies ist bei regulären Ausdrücken nützlich.

Die letzten beiden Wörter zeigen den zurückgegebenen Wert und seinen Typ an. Im Fall "acl" existiert das Muster nicht.

     return=nothing:        Keine Rückgabe, da es keine "map" gibt.
     return="`<value>`":      Der als Zeichenfolge zurückgegebene Wert.
     return=cannot-display: Der Wert kann nicht in eine Zeichenfolge umgewandelt werden.

     type="`<type>`":         Der Typ des zurückgegebenen Samples.

<a id="entry-9-3-get-var"></a>

**`get var <name>`**

```haproxy
get var <name>
```

Zeigt Existenz, Typ und Inhalt der prozessweiten Variablen 'name' an. Nur prozessweite Variablen sind lesbar, daher muss der Name mit 'proc.' beginnen; andernfalls wird keine Variable gefunden. Dieser Befehl erfordert die Berechtigungsstufe "operator" oder "admin".

<a id="entry-9-3-get-weight"></a>

**`get weight <backend>/<server>`**

```haproxy
get weight <backend>/<server>
```

Meldet das aktuelle und das anfängliche Gewicht des Servers `<server>` im Backend `<backend>`, oder einen Fehler, wenn eines von beiden nicht existiert. Das anfängliche Gewicht ist das in der Konfigurationsdatei angegebene. Beide sind normalerweise gleich, sofern das aktuelle Gewicht nicht geändert wurde. Sowohl das Backend als auch der Server können entweder über ihren Namen oder über ihre numerische ID mit vorangestelltem Rautezeichen ('#') angegeben werden.

<a id="entry-9-3-help"></a>

**`help [<command>]`**

```haproxy
help [<command>]
```

Gibt die Liste bekannter Schlüsselwörter und ihrer grundlegenden Verwendung oder die zum angeforderten Befehl passenden Befehle aus. Dieselbe Hilfeanzeige erscheint auch bei unbekannten Befehlen.

<a id="entry-9-3-httpclient"></a>

**`httpclient [--htx] <method> <URI>`**

```haproxy
httpclient [--htx] <method> <URI>
```

Startet eine HTTP-Client-Anfrage und gibt die Antwort über die CLI aus. Dies wird nur auf einer CLI-Verbindung im Expertenmodus unterstützt (siehe "expert-mode on") und ist ausschließlich für die Fehlerdiagnose vorgesehen. Der httpclient kann einen Servernamen in der URL über den resolvers-Abschnitt "default" auflösen, der standardmäßig mit den DNS-Servern aus /etc/resolv.conf befüllt wird. Einen Host aus /etc/hosts kann er jedoch nicht auflösen, sofern kein lokaler dns-Daemon verwendet wird, der solche Namen auflösen kann.

Die Option --htx ermöglicht es, mit der Funktion htx_dump() die interne htx-Darstellung von HAProxy zu verwenden, die hauptsächlich der Fehlerdiagnose dient.

<a id="entry-9-3-new-ssl-ca-file"></a>

**`new ssl ca-file <cafile>`**

```haproxy
new ssl ca-file <cafile>
```

Erzeugt einen neuen leeren CA-Dateibaumeintrag, der mit einem Satz von CA-Zertifikaten befüllt und einer crt-list hinzugefügt werden soll. Dieser Befehl sollte in Kombination mit "set ssl ca-file", "add ssl ca-file" und "add ssl crt-list" verwendet werden.

<a id="entry-9-3-new-ssl-cert"></a>

**`new ssl cert <filename>`**

```haproxy
new ssl cert <filename>
```

Erzeugt einen neuen leeren SSL-Zertifikatsspeicher, der mit einem Zertifikat befüllt und einem Verzeichnis oder einer crt-list hinzugefügt werden soll. Dieser Befehl sollte in Kombination mit "set ssl cert" und "add ssl crt-list" verwendet werden.

<a id="entry-9-3-new-ssl-crl-file"></a>

**`new ssl crl-file <crlfile>`**

```haproxy
new ssl crl-file <crlfile>
```

Erzeugt einen neuen leeren CRL-Dateibaumeintrag, der mit einem Satz von CRLs befüllt und einer crt-list hinzugefügt werden soll. Dieser Befehl sollte in Kombination mit "set ssl crl-file" und "add ssl crt-list" verwendet werden.

<a id="entry-9-3-prepare-acl"></a>

**`prepare acl <acl>`**

```haproxy
prepare acl <acl>
```

Weist in der ACL `<acl>` eine neue Versionsnummer für eine atomare Ersetzung zu. `<acl>` ist die von "show acl" zurückgegebene \#`<id>` oder der zurückgegebene `<name>`. Die neue Versionsnummer wird in der Antwort nach "New version created:" angezeigt. Mit dieser Nummer lässt sich anschließend das Hinzufügen neuer ACL-Einträge vorbereiten, die nach ihrer Übernahme die aktuellen Einträge atomar ersetzen. Sie wird in "show acl" als "next_ver" gemeldet. Das Zuweisen neuer Versionen hat keine Auswirkungen, da ungenutzte Versionen automatisch entfernt werden, sobald eine neuere Version übernommen wird. Versionsnummern sind vorzeichenlose 32-Bit-Werte, die am Ende ihres Wertebereichs wieder am Anfang beginnen; beim Vergleich in einem externen Programm ist daher Vorsicht erforderlich. Dieser Befehl kann nicht verwendet werden, wenn die Referenz `<acl>` ein Name ist, der auch für eine Map verwendet wird. In diesem Fall muss stattdessen der Befehl "prepare map" verwendet werden.

<a id="entry-9-3-prepare-map"></a>

**`prepare map <map>`**

```haproxy
prepare map <map>
```

Weist in der Map `<map>` eine neue Versionsnummer für eine atomare Ersetzung zu. `<map>` ist die von "show map" zurückgegebene \#`<id>` oder der zurückgegebene `<name>`. Die neue Versionsnummer wird in der Antwort nach "New version created:" angezeigt. Mit dieser Nummer lässt sich anschließend das Hinzufügen neuer Map-Einträge vorbereiten, die nach ihrer Übernahme die aktuellen Einträge atomar ersetzen. Sie wird in "show map" als "next_ver" gemeldet. Das Zuweisen neuer Versionen hat keine Auswirkungen, da ungenutzte Versionen automatisch entfernt werden, sobald eine neuere Version übernommen wird. Versionsnummern sind vorzeichenlose 32-Bit-Werte, die am Ende ihres Wertebereichs wieder am Anfang beginnen; beim Vergleich in einem externen Programm ist daher Vorsicht erforderlich.

<a id="entry-9-3-prompt"></a>

**`prompt [help | n | i | p | timed]*`**

```haproxy
prompt [help | n | i | p | timed]*
```

Ändert das Verhalten des interaktiven Modus und die am Zeilenanfang angezeigte Eingabeaufforderung: - "help": zeigt die Verwendung des Befehls an - "n": wechselt in den nicht interaktiven Modus - "i": wechselt in den interaktiven Modus - "p": wechselt in den interaktiven Modus mit Eingabeaufforderung - "timed": schaltet die Zeitanzeige in der Eingabeaufforderung um

Ohne Option wird zwischen dem Modus mit Eingabeaufforderung und dem nicht interaktiven Modus gewechselt. Im nicht interaktiven Modus wird die Verbindung geschlossen, sobald der letzte Befehl der aktuellen Zeile abgeschlossen ist. Im interaktiven Modus wird die Verbindung nach Abschluss eines Befehls nicht geschlossen, sodass ein weiterer eingegeben werden kann. Im Modus mit Eingabeaufforderung bleibt der interaktive Modus aktiv; am Zeilenanfang erscheint eine Eingabeaufforderung, die anzeigt, dass der Interpreter auf einen neuen Befehl wartet. Die Eingabeaufforderung besteht aus einer schließenden spitzen Klammer mit nachfolgendem Leerzeichen "\> ".

Der Modus mit Eingabeaufforderung eignet sich eher für menschliche Benutzer, der interaktive Modus für fortgeschrittene Skripte und der nicht interaktive Modus (Standard) für einfache Skripte. Der nicht interaktive Modus ist für den Master-Socket nicht verfügbar.

<a id="entry-9-3-publish-backend"></a>

**`publish backend <backend>`**

```haproxy
publish backend <backend>
```

Aktiviert die Weiterleitung von Inhalten zu einer Backend-Instanz. Dies ist die Umkehrung des Befehls "unpublish backend". Dieser Befehl ist eingeschränkt und kann nur über Sockets ausgeführt werden, die für die Berechtigungsstufen "operator" oder "admin" konfiguriert sind.

<a id="entry-9-3-quit"></a>

**`quit`**

```haproxy
quit
```

Schließt die Verbindung im interaktiven Modus.

<a id="entry-9-3-set-anon"></a>

**`set anon [on|off] [<key>]`**

```haproxy
set anon [on|off] [<key>]
```

Dieser Befehl aktiviert oder deaktiviert den „anonymisierten Modus“ für die aktuelle CLI-Sitzung. Dabei werden bestimmte als sensibel oder vertraulich eingestufte Felder in Befehlsausgaben durch Hashes ersetzt. Diese erhalten genügend Konsistenz zwischen den Elementen, damit Entwickler bei der Fehlersuche Beziehungen zwischen ihnen erkennen können. Zugleich ist ihre Bitzahl (24) niedrig genug, um sie wegen der großen Anzahl möglicher Treffer nicht umkehrbar zu machen. Wird der Modus ohne Angabe eines Schlüssels aktiviert, wird der globale Schlüssel verwendet (entweder in der Konfigurationsdatei mit "anonkey" angegeben oder über den CLI-Befehl "set anon global-key" gesetzt). Wurde kein solcher Schlüssel gesetzt, wird ein zufälliger erzeugt. Andernfalls kann der für die aktuelle Sitzung zu verwendende 32-Bit-Schlüssel angegeben werden, etwa um den Schlüssel einer früheren Ausgabe wiederzuverwenden und Ausgaben leichter zu vergleichen. Entwickler benötigen diesen Schlüssel nie. Es wird empfohlen, ihn niemals weiterzugeben, da er es ermöglichen könnte, Vermutungen darüber zu bestätigen oder zu widerlegen, was bestimmte Hashes verbergen.

<a id="entry-9-3-set-dynamic-cookie-key-backend"></a>

**`set dynamic-cookie-key backend <backend> <value>`**

```haproxy
set dynamic-cookie-key backend <backend> <value>
```

Ändert den geheimen Schlüssel, der zur Erzeugung dynamischer Cookies für die Sitzungsbindung verwendet wird. Dadurch werden bestehende Sitzungen unterbrochen.

<a id="entry-9-3-set-anon-global-key"></a>

**`set anon global-key <key>`**

```haproxy
set anon global-key <key>
```

Setzt den globalen Anonymisierungsschlüssel auf `<key>`. Dieser muss eine 32-Bit-Ganzzahl zwischen 0 und 4294967295 sein (0 deaktiviert den globalen Schlüssel). Dieser Befehl erfordert admin-Berechtigungen.

<a id="entry-9-3-set-map"></a>

**`set map <map> [<key>|#<ref>] <value>`**

```haproxy
set map <map> [<key>|#<ref>] <value>
```

Ändert den Wert, der jedem Schlüssel `<key>` in einer Map `<map>` entspricht. `<map>` ist die von "show map" zurückgegebene \#`<id>` oder der zurückgegebene `<name>`. Wird anstelle von `<key>` die Referenz `<ref>` verwendet, wird nur der Eintrag geändert, auf den `<ref>` verweist. Der neue Wert ist `<value>`.

<a id="entry-9-3-set-maxconn-frontend"></a>

**`set maxconn frontend <frontend> <value>`**

```haproxy
set maxconn frontend <frontend> <value>
```

Ändert die maxconn-Einstellung des angegebenen Frontends dynamisch. Jeder positive Wert einschließlich null ist zulässig; Werte oberhalb des globalen maxconn sind jedoch wenig sinnvoll. Wird die Grenze erhöht und warten Verbindungen, werden sie sofort angenommen. Wird sie auf einen Wert unterhalb der aktuellen Verbindungszahl gesenkt, wird die Annahme neuer Verbindungen verzögert, bis der Schwellenwert erreicht ist. Das Frontend kann entweder über seinen Namen oder über seine numerische ID mit vorangestelltem Rautezeichen ('#') angegeben werden.

<a id="entry-9-3-set-maxconn-server"></a>

**`set maxconn server <backend/server> <value>`**

```haproxy
set maxconn server <backend/server> <value>
```

Ändert die maxconn-Einstellung des angegebenen Servers dynamisch. Jeder positive Wert einschließlich null ist zulässig; Werte oberhalb des globalen maxconn sind jedoch wenig sinnvoll.

<a id="entry-9-3-set-maxconn-global"></a>

**`set maxconn global <maxconn>`**

```haproxy
set maxconn global <maxconn>
```

Ändert die globale maxconn-Einstellung dynamisch innerhalb des Bereichs, den die anfängliche globale maxconn-Einstellung vorgibt. Wird sie erhöht und warten Verbindungen, werden sie sofort angenommen. Wird sie auf einen Wert unterhalb der aktuellen Verbindungszahl gesenkt, wird die Annahme neuer Verbindungen verzögert, bis der Schwellenwert erreicht ist. Der Wert null stellt die anfängliche Einstellung wieder her.

<a id="entry-9-3-set-profiling-memory"></a>

**`set profiling memory { on | off }`**

```haproxy
set profiling memory { on | off }
set profiling tasks { auto | on | off | lock | no-lock | memory | no-memory }
```

Aktiviert oder deaktiviert CPU- oder Speicher-Profiling für das angegebene Teilsystem. Dies entspricht dem Setzen oder Löschen der "profiling"-Einstellungen im Abschnitt "global" der Konfigurationsdatei. Siehe auch "show profiling". Wird das Aufgaben-Profiling manuell auf "on" gesetzt, werden die Scheduler-Statistiken automatisch zurückgesetzt. So lässt sich die Aktivität über ein bestimmtes Zeitintervall prüfen. Das Speicher-Profiling ist auf bestimmte Betriebssysteme beschränkt (funktioniert bekanntermaßen auf dem Ziel linux-glibc) und erfordert, dass USE_MEMORY_PROFILING beim Kompilieren gesetzt ist.

Beim Aufgaben-Profiling lässt sich das Erfassen der Sperr- und Speicherzeiten pro Aufgabe zur Laufzeit aktivieren oder deaktivieren. Die Änderung wird jedoch erst berücksichtigt, wenn das Profiling das nächste Mal von off/auto auf on wechselt (automatisch oder manuell). Wird mit "no-lock" das Sperr-Profiling pro Aufgabe deaktiviert, um CPU-Zyklen zu sparen, wird daher empfohlen, das Aufgaben-Profiling aus- und wieder einzuschalten, um die Änderung zu übernehmen.

<a id="entry-9-3-set-rate-limit-connections-global"></a>

**`set rate-limit connections global <value>`**

```haproxy
set rate-limit connections global <value>
```

Ändert die prozessweite Begrenzung der Verbindungsrate, die durch die globale Einstellung 'maxconnrate' festgelegt wird. Der Wert null deaktiviert die Begrenzung. Diese Grenze gilt für alle Frontends, und die Änderung wirkt sofort. Der Wert wird als Anzahl der Verbindungen pro Sekunde angegeben.

<a id="entry-9-3-set-rate-limit-http-compression-global"></a>

**`set rate-limit http-compression global <value>`**

```haproxy
set rate-limit http-compression global <value>
```

Ändert die maximale Eingangsrate der Komprimierung, die durch die globale Einstellung 'maxcomprate' festgelegt wird. Der Wert null deaktiviert die Begrenzung. Der Wert wird in Kilobytes pro Sekunde angegeben. In "show info" ist er in der Zeile "CompressBpsRateLim" in Bytes verfügbar.

<a id="entry-9-3-set-rate-limit-sessions-global"></a>

**`set rate-limit sessions global <value>`**

```haproxy
set rate-limit sessions global <value>
```

Ändert die prozessweite Begrenzung der Sitzungsrate, die durch die globale Einstellung 'maxsessrate' festgelegt wird. Der Wert null deaktiviert die Begrenzung. Diese Grenze gilt für alle Frontends, und die Änderung wirkt sofort. Der Wert wird als Anzahl der Sitzungen pro Sekunde angegeben.

<a id="entry-9-3-set-rate-limit-ssl-sessions-global"></a>

**`set rate-limit ssl-sessions global <value>`**

```haproxy
set rate-limit ssl-sessions global <value>
```

Ändert die prozessweite Begrenzung der SSL-Sitzungsrate, die durch die globale Einstellung 'maxsslrate' festgelegt wird. Der Wert null deaktiviert die Begrenzung. Diese Grenze gilt für alle Frontends, und die Änderung wirkt sofort. Der Wert wird als Anzahl der pro Sekunde an den SSL-Stack übergebenen Sitzungen angegeben. Die Begrenzung greift vor dem Handshake, um den Stack vor Handshake-Missbrauch zu schützen.

<a id="entry-9-3-set-server"></a>

**`set server <backend>/<server> addr <ip4 or ip6 address> [port <port>]`**

```haproxy
set server <backend>/<server> addr <ip4 or ip6 address> [port <port>]
```

Ersetzt die aktuelle IP-Adresse eines Servers durch die angegebene. Optional kann mit dem Parameter 'port' auch der Port geändert werden. Eine Portänderung unterstützt auch den Wechsel zur oder von der Portzuordnung (Schreibweise mit +X oder -Y), allerdings nur, wenn für den Health Check ein Port konfiguriert ist.

<a id="entry-9-3-set-server-2"></a>

**`set server <backend>/<server> agent [ up | down ]`**

```haproxy
set server <backend>/<server> agent [ up | down ]
```

Erzwingt einen neuen Status für den Agenten eines Servers. Dies kann beispielsweise nützlich sein, um den Serverstatus sofort unabhängig von langsamen Agent-Prüfungen zu ändern. Die Änderung wird gegebenenfalls an Server weitergegeben, die diesen Server verfolgen.

<a id="entry-9-3-set-server-3"></a>

**`set server <backend>/<server> agent-addr <addr> [port <port>]`**

```haproxy
set server <backend>/<server> agent-addr <addr> [port <port>]
```

Ändert die Adresse für Agent-Prüfungen eines Servers. Dadurch können Agent-Prüfungen zur Laufzeit auf eine andere Adresse umgestellt werden. Es können sowohl eine IP-Adresse als auch ein Hostname angegeben werden; letzterer wird aufgelöst. Optional kann auch der Agent-Port geändert werden.

<a id="entry-9-3-set-server-4"></a>

**`set server <backend>/<server> agent-port <port>`**

```haproxy
set server <backend>/<server> agent-port <port>
```

Ändert den für Agent-Prüfungen verwendeten Port.

<a id="entry-9-3-set-server-5"></a>

**`set server <backend>/<server> agent-send <value>`**

```haproxy
set server <backend>/<server> agent-send <value>
```

Ändert die Zeichenfolge, die an das Ziel der Agent-Prüfung gesendet wird. Damit kann die Zeichenfolge zusammen mit der Serveradresse aktualisiert werden, sodass beide weiterhin zusammenpassen.

<a id="entry-9-3-set-server-6"></a>

**`set server <backend>/<server> health [ up | stopping | down ]`**

```haproxy
set server <backend>/<server> health [ up | stopping | down ]
```

Erzwingt einen neuen Gesundheitsstatus für einen Server. Dies kann beispielsweise nützlich sein, um den Serverstatus sofort unabhängig von langsamen Health Checks zu ändern. Die Änderung wird gegebenenfalls an Server weitergegeben, die diesen Server verfolgen.

<a id="entry-9-3-set-server-7"></a>

**`set server <backend>/<server> check-addr <ip4 | ip6> [port <port>]`**

```haproxy
set server <backend>/<server> check-addr <ip4 | ip6> [port <port>]
```

Ändert die IP-Adresse für die Health Checks des Servers. Optional kann auch der für diese Health Checks verwendete Port geändert werden.

<a id="entry-9-3-set-server-8"></a>

**`set server <backend>/<server> check-port <port>`**

```haproxy
set server <backend>/<server> check-port <port>
```

Ändert den für Health Checks verwendeten Port auf `<port>`

<a id="entry-9-3-set-server-9"></a>

**`set server <backend>/<server> state [ ready | drain | maint ]`**

```haproxy
set server <backend>/<server> state [ ready | drain | maint ]
```

Erzwingt einen neuen administrativen Status für einen Server. Dies kann nützlich sein, um die Lastverteilung und/oder jeglichen Datenverkehr zu einem Server zu deaktivieren. Der Status "ready" versetzt den Server in den normalen Modus; dies entspricht dem Befehl "enable server". Der Status "maint" deaktiviert jeglichen Datenverkehr zum Server und sämtliche Health Checks; dies entspricht dem Befehl "disable server". Der Modus "drain" nimmt den Server nur aus der Lastverteilung heraus, erlaubt aber weiterhin Prüfungen und neue Verbindungen mit Sitzungsbindung. Änderungen werden gegebenenfalls an Server weitergegeben, die diesen Server verfolgen.

<a id="entry-9-3-set-server-10"></a>

**`set server <backend>/<server> weight <weight>[%]`**

```haproxy
set server <backend>/<server> weight <weight>[%]
```

Ändert das Gewicht eines Servers auf den als Argument angegebenen Wert. Dies entspricht genau dem weiter unten beschriebenen Befehl "set weight".

<a id="entry-9-3-set-server-11"></a>

**`set server <backend>/<server> fqdn <FQDN>`**

```haproxy
set server <backend>/<server> fqdn <FQDN>
```

Ändert den FQDN eines Servers auf den als Argument angegebenen Wert. Dafür muss der zur Laufzeit verwendete interne DNS-Resolver für diesen Server konfiguriert und aktiviert sein.

<a id="entry-9-3-set-server-12"></a>

**`set server <backend>/<server> ssl [ on | off ]  (deprecated)`**

```haproxy
set server <backend>/<server> ssl [ on | off ]  (deprecated)
```

Diese Option konfiguriert die SSL-Verschlüsselung ausgehender Verbindungen zum Server. Wird sie ausgeschaltet, wird der gesamte Datenverkehr als Klartext übertragen; der Pfad der Health Checks bleibt unverändert.

Dieser Befehl ist veraltet. Stattdessen mit dem Befehl "add server" dynamisch einen neuen Server mit oder ohne SSL erzeugen.

<a id="entry-9-3-set-severity-output"></a>

**`set severity-output [ none | number | string ]`**

```haproxy
set severity-output [ none | number | string ]
```

Ändert für die Dauer der aktuellen Sitzung das Format der Schweregradangabe in der Ausgabe des verbundenen Statistik-Sockets.

<a id="entry-9-3-set-ssl-ca-file"></a>

**`set ssl ca-file <cafile> <payload>`**

```haproxy
set ssl ca-file <cafile> <payload>
```

Dieser Befehl ist Teil eines Transaktionssystems; die Befehle "commit ssl ca-file" und "abort ssl ca-file" können erforderlich sein. Wenn keine Transaktion läuft, wird ein CA-Dateibaumeintrag erzeugt, in dem die in den Nutzdaten enthaltenen Zertifikate gespeichert werden. Der CA-Dateieintrag wird nicht im CA-Dateibaum gespeichert, sondern nur in einer temporären Transaktion gehalten. Existiert bereits eine Transaktion mit demselben Dateinamen, wird der bisherige CA-Dateieintrag gelöscht und durch den neuen ersetzt. Sobald die Änderungen abgeschlossen sind, muss die Transaktion mit "commit ssl ca-file" übernommen werden. Um mehrere Zertifikate einzeln hinzuzufügen, kann der Befehl "add ssl ca-file" verwendet werden.

Beispiel:

```text
echo -e "set ssl ca-file cafile.pem <<\n$(cat rootCA.crt)\n" | \
socat /var/run/haproxy.stat -
echo "commit ssl ca-file cafile.pem" | socat /var/run/haproxy.stat -
```

<a id="entry-9-3-set-ssl-cert"></a>

**`set ssl cert <filename> <payload>`**

```haproxy
set ssl cert <filename> <payload>
```

Dieser Befehl ist Teil eines Transaktionssystems; die Befehle "commit ssl cert" und "abort ssl cert" können erforderlich sein. Das gesamte Transaktionssystem funktioniert mit jedem Zertifikat, das vom Befehl "show ssl cert" angezeigt wird, also mit jedem Frontend- oder Backend-Zertifikat. Wenn keine Transaktion läuft, wird das Zertifikat `<filename>` im Speicher in eine temporäre Transaktion dupliziert. Diese Transaktion wird anschließend mit der PEM-Datei aus den Nutzdaten aktualisiert. Existiert eine Transaktion mit demselben Dateinamen, wird sie aktualisiert. Auch mit einem Zertifikat verknüpfte Dateien (.issuer, .sctl, .ocsp usw.) können aktualisiert werden. Sobald die Änderungen abgeschlossen sind, muss die Transaktion mit "commit ssl cert" übernommen werden.

Dateien müssen über die CLI mit Vorsicht eingespielt werden, da eine Leerzeile das Ende der Nutzdaten signalisiert. Es wird empfohlen, eine bereinigte PEM-Datei einzuspielen. Eine einfache Methode ist, alle Leerzeilen zu entfernen und nur den Inhalt der PEM-Abschnitte beizubehalten. Dies lässt sich mit einem sed-Befehl erreichen.

Beispiel:

```haproxy
# With some simple sanitizing
 echo -e "set ssl cert localhost.pem <<\n$(sed -n '/^$/d;/-BEGIN/,/-END/p' 127.0.0.1.pem)\n" | \
 socat /var/run/haproxy.stat -

 # Complete example with commit
 echo -e "set ssl cert localhost.pem <<\n$(cat 127.0.0.1.pem)\n" | \
 socat /var/run/haproxy.stat -
 echo -e \
 "set ssl cert localhost.pem.issuer <<\n $(cat 127.0.0.1.pem.issuer)\n" | \
 socat /var/run/haproxy.stat -
 echo -e \
 "set ssl cert localhost.pem.ocsp <<\n$(base64 -w 1000 127.0.0.1.pem.ocsp)\n" | \
 socat /var/run/haproxy.stat -
 echo "commit ssl cert localhost.pem" | socat /var/run/haproxy.stat -
```

<a id="entry-9-3-set-ssl-crl-file"></a>

**`set ssl crl-file <crlfile> <payload>`**

```haproxy
set ssl crl-file <crlfile> <payload>
```

Dieser Befehl ist Teil eines Transaktionssystems; die Befehle "commit ssl crl-file" und "abort ssl crl-file" können erforderlich sein. Wenn keine Transaktion läuft, wird ein CRL-Dateibaumeintrag erzeugt, in dem die in den Nutzdaten enthaltenen Sperrlisten gespeichert werden. Der CRL-Dateieintrag wird nicht im CRL-Dateibaum gespeichert, sondern nur in einer temporären Transaktion gehalten. Existiert bereits eine Transaktion mit demselben Dateinamen, wird der bisherige CRL-Dateieintrag gelöscht und durch den neuen ersetzt. Sobald die Änderungen abgeschlossen sind, muss die Transaktion mit "commit ssl crl-file" übernommen werden.

Beispiel:

```text
echo -e "set ssl crl-file crlfile.pem <<\n$(cat rootCRL.pem)\n" | \
socat /var/run/haproxy.stat -
echo "commit ssl crl-file crlfile.pem" | socat /var/run/haproxy.stat -
```

<a id="entry-9-3-set-ssl-ech"></a>

**`set ssl ech <bind> <payload>`**

```haproxy
set ssl ech <bind> <payload>
```

Ersetzt die ECH-Schlüssel einer bind-Zeile durch diesen Schlüssel. Die Nutzdaten müssen im PEM-for-ECH-Format vorliegen.
(<https://datatracker.ietf.org/doc/html/draft-farrell-tls-pemesni>)

Das Format der bind-Zeile ist `<frontend>`/@`<filename>`:`<linenum>` (Beispiel: frontend1/@haproxy.conf:19) oder `<frontend>`/`<name>`, wenn die bind-Zeile mit dem Schlüsselwort "name" benannt wurde.

Erfordert eine OpenSSL-Version mit ECH-Unterstützung. HAProxy muss mit USE_ECH=1 kompiliert sein. Dieser Befehl wird nur auf einer CLI-Verbindung im experimentellen Modus unterstützt (siehe "experimental-mode on").

Siehe auch "show ssl ech", "add ssl ech" und "ech" in [Abschnitt 5.1](/de/haproxy/bind-and-server-options/#section-5-1) des Konfigurationshandbuchs.

    $ openssl ech -public_name foobar.com -out foobar3.com.ech
    $ echo -e "experimental-mode on;
               set ssl ech frontend1/@haproxy.conf:19 <<%EOF%&#92;n$(cat foobar3.com.ech)&#92;n%EOF%&#92;n" | &#92;
      socat /tmp/haproxy.sock -
    set new ECH configs for frontend1/@haproxy.conf:19

<a id="entry-9-3-set-ssl-ocsp-response"></a>

**`set ssl ocsp-response <response | payload>`**

```haproxy
set ssl ocsp-response <response | payload>
```

Dieser Befehl aktualisiert eine OCSP-Antwort für ein Zertifikat (siehe "crt" in "bind"-Zeilen). Dabei werden dieselben Prüfungen durchgeführt wie beim erstmaligen Laden der Antwort. `<response>` muss als base64-kodierte Zeichenfolge der DER-kodierten Antwort des OCSP-Servers übergeben werden. Dieser Befehl wird mit BoringSSL nicht unterstützt.

Beispiel:

```text
openssl ocsp -issuer issuer.pem -cert server.pem \
             -host ocsp.issuer.com:80 -respout resp.der
echo "set ssl ocsp-response $(base64 -w 10000 resp.der)" | \
             socat stdio /var/run/haproxy.stat

mit der Nutzlastsyntax:
echo -e "set ssl ocsp-response <<\n$(base64 resp.der)\n" | \
             socat stdio /var/run/haproxy.stat
```

<a id="entry-9-3-set-ssl-tls-key"></a>

**`set ssl tls-key <id> <tlskey>`**

```haproxy
set ssl tls-key <id> <tlskey>
```

Setzt den nächsten TLS-Schlüssel für den Listener `<id>` auf `<tlskey>`. Dieser Schlüssel wird zum letzten Schlüssel, während der vorletzte zur Verschlüsselung verwendet wird (die anderen dienen nur der Entschlüsselung). Der älteste vorhandene TLS-Schlüssel wird überschrieben. `<id>` ist entweder eine numerische \#`<id>` oder der von "show tls-keys" zurückgegebene `<file>`. `<tlskey>` ist ein base64-kodierter TLS-Ticket-Schlüssel mit 48 oder 80 Bytes (z. B. openssl rand 80 \| openssl base64 -A).

<a id="entry-9-3-set-table"></a>

**`set table <table> key <key> [data.<data_type> <value>]*`**

```haproxy
set table <table> key <key> [data.<data_type> <value>]*
set table <table> ptr <ptr> [data.<data_type> <value>]*
```

Erzeugt oder aktualisiert einen Stick-Table-Eintrag in der Tabelle. Ist der Schlüssel nicht vorhanden, wird ein Eintrag eingefügt. Alle möglichen Werte für `<data_type>` stehen unter stick-table in Abschnitt 4.2. Die wahrscheinlich häufigste Verwendung ist das dynamische Eintragen von Quell-IP-Adressen mit einem Flag in gpc0, um eine IP-Adresse dynamisch zu sperren oder ihre Dienstqualität zu beeinflussen. In einem einzigen Aufruf können mehrere data_types übergeben werden.

Für einen bestehenden Eintrag kann optional statt der Suche über den Schlüssel eine Suche über ptr verwendet werden: `<ptr>` wird in der Form 0xffff geschrieben und muss der Adresse entsprechen, die ein zuvor ausgeführter "show table"-Befehl zurückgegeben hat. Das Identifizieren eines Eintrags über seinen Zeiger kann sinnvoll sein, wenn dies über den Schlüssel wegen eines leeren Schlüssels oder mit der CLI inkompatibler Zeichen nicht möglich ist.

Wenn data.`<data_type>` ein Array-Typ ist, kann mit "[]" auf einen bestimmten Index im Array zugegriffen werden, etwa so: data.gpt[1]

<a id="entry-9-3-set-timeout-cli"></a>

**`set timeout cli <delay>`**

```haproxy
set timeout cli <delay>
```

Ändert die Zeitüberschreitung der CLI-Schnittstelle für die aktuelle Verbindung. Dies kann bei langen Diagnosesitzungen nützlich sein, in denen fortlaufend bestimmte Indikatoren geprüft werden müssen, ohne dass die Verbindung getrennt wird. Die Dauer wird in Sekunden angegeben.

<a id="entry-9-3-set-var"></a>

**`set var <name> <expression>`**

```haproxy
set var <name> <expression>
set var <name> expr <expression>
set var <name> fmt <format>
```

Ermöglicht es, die prozessweite Variable 'name' mit dem Ergebnis des Ausdrucks `<expression>` oder der Formatzeichenfolge `<format>` zu setzen oder zu überschreiben. Nur prozessweite Variablen können verwendet werden, daher muss der Name mit 'proc.' beginnen; andernfalls wird keine Variable gesetzt. `<expression>` und `<format>` dürfen nur „interne“ Sample-Abruf-Schlüsselwörter und Konverter enthalten. Am ehesten nützlich sind dabei str('something'), int(), einfache Zeichenfolgen oder Verweise auf andere Variablen. Der Befehlszeilenparser berücksichtigt keine Anführungszeichen, daher muss jedem Leerzeichen im Ausdruck ein umgekehrter Schrägstrich vorangestellt werden. Dieser Befehl erfordert die Berechtigungsstufe "operator" oder "admin". Er wird nur auf einer CLI-Verbindung im experimentellen Modus unterstützt (siehe "experimental-mode on").

<a id="entry-9-3-set-weight"></a>

**`set weight <backend>/<server> <weight>[%]`**

```haproxy
set weight <backend>/<server> <weight>[%]
```

Ändert das Gewicht eines Servers auf den als Argument angegebenen Wert. Endet der Wert mit dem Zeichen '%', ist das neue Gewicht relativ zum ursprünglich konfigurierten Gewicht. Absolute Gewichte zwischen 0 und 256 sind zulässig. Relative Gewichte müssen positiv sein; das resultierende absolute Gewicht wird begrenzt auf
256. Für Server einer Servergruppe mit statischem Lastverteilungsalgorithmus gelten strengere Einschränkungen, da das einmal gesetzte Gewicht nicht mehr geändert werden kann. Für diese Server sind daher nur die Werte 0 und 100% zulässig (oder 0 und das anfängliche Gewicht). Änderungen wirken sofort, manche LB-Algorithmen benötigen jedoch eine bestimmte Anzahl von Anfragen, um die Änderungen zu berücksichtigen. Typischerweise wird mit diesem Befehl ein Server während einer Aktualisierung deaktiviert, indem sein Gewicht auf null gesetzt wird. Nach der Aktualisierung wird er wieder aktiviert, indem das Gewicht auf 100% zurückgesetzt wird. Dieser Befehl ist eingeschränkt und kann nur über Sockets ausgeführt werden, die für die Berechtigungsstufe "admin" konfiguriert sind. Sowohl das Backend als auch der Server können entweder über ihren Namen oder über ihre numerische ID mit vorangestelltem Rautezeichen ('#') angegeben werden.

<a id="entry-9-3-show-acl"></a>

**`show acl [[@<ver>] <acl>]`**

```haproxy
show acl [[@<ver>] <acl>]
```

Gibt Informationen über ACL-Konverter aus. Ohne Argument wird die Liste aller verfügbaren ACLs zurückgegeben. Wird eine `<acl>` angegeben, wird ihr Inhalt ausgegeben. `<acl>` ist die \#`<id>` oder der `<name>`. Standardmäßig wird die aktuelle Version der ACL angezeigt (die Version, gegen die derzeit geprüft wird und die in der ACL-Liste als 'curr_ver' gemeldet wird). Andere Versionen können ausgegeben werden, indem '@`<ver>`' vor den ACL-Bezeichner gesetzt wird. Die Version wirkt als Filter; nicht vorhandene Versionen liefern einfach kein Ergebnis. Das Ausgabeformat ist dasselbe wie bei Maps, auch für die Sample-Werte. Die zurückgegebenen Daten sind keine Liste verfügbarer ACLs, sondern eine Liste aller Muster, aus denen ACLs bestehen. Viele dieser Muster können auch von Maps verwendet werden. Der Wert 'entry_cnt' zählt alle ACL-Einträge, nicht nur die aktiven. Er enthält daher auch Einträge, die gerade hinzugefügt werden.

<a id="entry-9-3-show-anon"></a>

**`show anon`**

```haproxy
show anon
```

Zeigt den aktuellen Zustand des anonymisierten Modus (aktiviert oder deaktiviert) und den Schlüssel der aktuellen Sitzung an.

<a id="entry-9-3-show-backend"></a>

**`show backend`**

```haproxy
show backend
```

Gibt die Liste der im laufenden Prozess verfügbaren Backends aus

<a id="entry-9-3-show-cli-level"></a>

**`show cli level`**

```haproxy
show cli level
```

Zeigt die CLI-Berechtigungsstufe der aktuellen CLI-Sitzung an. Das Ergebnis kann 'admin', 'operator' oder 'user' sein. Siehe auch die Befehle 'operator' und 'user'.

Beispiel:

```shell
$ socat /tmp/sock1 readline
prompt
> operator
> show cli level
operator
> user
> show cli level
user
> operator
Permission denied
```

<a id="entry-9-3-operator"></a>

**`operator`**

```haproxy
operator
```

Senkt die CLI-Berechtigungsstufe der aktuellen CLI-Sitzung auf operator. Sie kann nicht erhöht werden. Außerdem werden Expertenmodus und experimenteller Modus deaktiviert. Siehe auch "show cli level".

<a id="entry-9-3-unpublish-backend"></a>

**`unpublish backend <backend>`**

```haproxy
unpublish backend <backend>
```

Schließt das Backend von der Auswahl für künftigen Datenverkehr aus. Dadurch werden use_backend- / default_backend-Regeln, die darauf verweisen, ignoriert und die nächsten Regeln zur inhaltsabhängigen Weiterleitung ausgewertet. Anders als bei deaktivierten Backends bleiben die Health Checks der Server aktiv. Dieser Befehl ist eingeschränkt und kann nur über Sockets ausgeführt werden, die für die Berechtigungsstufen "operator" oder "admin" konfiguriert sind.

<a id="entry-9-3-user"></a>

**`user`**

```haproxy
user
```

Senkt die CLI-Berechtigungsstufe der aktuellen CLI-Sitzung auf user. Sie kann nicht erhöht werden. Außerdem werden Expertenmodus und experimenteller Modus deaktiviert. Siehe auch "show cli level".

<a id="entry-9-3-show-activity"></a>

**`show activity [-1 | 0 | thread_num]`**

```haproxy
show activity [-1 | 0 | thread_num]
```

Meldet einige Zähler zu internen Ereignissen, die Entwicklern und allgemein Personen mit ausreichender HAProxy-Kenntnis helfen, die Ursachen gemeldeten ungewöhnlichen Verhaltens einzugrenzen. Ein typisches Beispiel wäre ein korrekt laufender Prozess, der nie schläft und 100% der CPU beansprucht. Die Ausgabe enthält eine Zeile pro Metrik mit den Zählern der einzelnen Threads in derselben Zeile. Diese Zähler haben 32 Bit und laufen während der Prozesslebensdauer über, was kein Problem ist, da dieser Befehl normalerweise zweimal aufgerufen wird. Die Felder sind bewusst nicht dokumentiert, damit ihre genaue Bedeutung im Code geprüft wird, der die Zähler aktualisiert. Diese Werte werden auch durch den Befehl "clear counters" zurückgesetzt. Bei Bereitstellungen mit mehreren Threads gibt die erste Spalte die Summe aller Threads an (oder je nach Art der Metrik den Durchschnitt). Die Werte aller Threads folgen in Thread-Reihenfolge in eckigen Klammern. Optional kann die Nummer des auszugebenden Threads als Argument angegeben werden. Der Sonderwert "0" meldet den aggregierten Wert (erste Spalte); "-1", der Standardwert, zeigt alle Spalten an. Wie im Modus mit einem einzelnen Thread werden keine Klammern ausgegeben, wenn nur eine Spalte angefordert wird.

<a id="entry-9-3-show-cli-sockets"></a>

**`show cli sockets`**

```haproxy
show cli sockets
```

Listet CLI-Sockets auf. Das Ausgabeformat besteht aus 3 durch Leerzeichen getrennten Feldern. Das erste Feld ist die Socket-Adresse: ein Unix-Socket, ein Paar aus ipv4-Adresse und Port oder ein entsprechendes ipv6-Paar. Sockets anderer Typen werden nicht ausgegeben. Das zweite Feld beschreibt die Berechtigungsstufe des Sockets: 'admin', 'user' oder 'operator'. Das letzte Feld listet die Prozesse, an die der Socket gebunden ist, durch Kommas getrennt auf; es kann Nummern oder 'all' enthalten.

Beispiel:

```shell
$ echo 'show cli sockets' | socat stdio /tmp/sock1
# socket lvl processes
/tmp/sock1 admin all
127.0.0.1:9999 user 2,3,4
127.0.0.2:9969 user 2
[::1]:9999 operator 2
```

<a id="entry-9-3-show-cache"></a>

**`show cache`**

```haproxy
show cache
```

Listet die konfigurierten Caches und die in jedem Cache-Baum gespeicherten Objekte auf.

\$ echo 'show cache' \| socat stdio /tmp/sock1 0x7f6ac6c5b03a: foobar (shctx:0x7f6ac6c5b000,
available blocks:3918) 1 2 3 4

1.  Zeiger auf die Cache-Struktur
2.  Cache-Name
3.  Zeiger auf den mmap-Bereich (shctx)
4.  Anzahl der im shctx zur Wiederverwendung verfügbaren Blöcke

0x7f6ac6c5b4cc hash:286881868 vary:0x0011223344556677 size:39114 (39 blocks), refcount:9, expire:237
1 2 3 4 5 6 7

1.  Zeiger auf den Cache-Eintrag
2.  Die ersten 32 Bit des Hashes
3.  Sekundärer Hash des Eintrags bei vary
4.  Größe des Objekts in Bytes
5.  Anzahl der für das Objekt verwendeten Blöcke
6.  Anzahl der Transaktionen, die den Eintrag verwenden
7.  Ablaufzeit; kann negativ sein, wenn der Eintrag bereits abgelaufen ist

<a id="entry-9-3-show-dev"></a>

**`show dev`**

```haproxy
show dev
```

Dieser Befehl bündelt Informationen, die HAProxy-Entwickler benötigen könnten, um die Ursachen eines bestimmten Problems besser zu verstehen. Für den Benutzer sind sie im Allgemeinen nicht nützlich, ermöglichen Entwicklern aber das Ausschließen bestimmter Hypothesen. Das Format besteht ungefähr aus einer Reihe von Abschnitten mit eingerückten Zeilen und jeweils einem Element pro Zeile, etwa Betriebssystemtyp und -version, CPU-Typ oder FD-Grenzen beim Start. Manche Felder werden weggelassen, um Wiederholungen oder unnötige Ausgaben zu vermeiden, wenn sie keinen Mehrwert liefern (z. B. unbegrenzte Werte). Künftig können weitere Felder hinzukommen oder sich einige ändern. Diese Ausgabe ist nicht zur Auswertung durch Skripte gedacht und sollte nicht als besonders zuverlässig angesehen werden. Sie soll im Wesentlichen denen Zeit sparen, die sie lesen können.

Technisch werden diese Informationen unverändert aus einer internen Struktur entnommen, die sie beim Start zusammen speichert, damit sie auch nach einem Absturz in einer Core-Datei zu finden sind. Daher können Entwickler um eine frühzeitige Ausgabe eines normal arbeitenden Prozesses bitten, um sie mit einem Core-Dump oder zwischen mehreren Neuladevorgängen zu vergleichen (beispielsweise können sich manche Grenzwerte ändern). Ist die Anonymisierung aktiviert, werden auch alle möglicherweise sensiblen Werte anonymisiert (z. B. der Knotenname).

Beispielausgabe:

```shell
$ socat stdio /tmp/sock1 <<< "show dev"
Platform info
  machine vendor: To be filled by O.E.M
  machine family: Altra
  cpu model: Impl 0x41 Arch 8 Part 0xd0c r3p1
  virtual machine: no
  container: no
  OS name: Linux
  OS release: 6.2.0-36-generic
  OS version: #37~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  9 18:01:07 UTC 2
  OS architecture: aarch64
  node name: 489aaf
Process info
  pid: 1735846
  boot uid: 509
  boot gid: 1002
  fd limit (soft): 1024
  fd limit (hard): 1048576
```

<a id="entry-9-3-show-env"></a>

**`show env [<name>]`**

```haproxy
show env [<name>]
```

Gibt eine oder alle dem Prozess bekannten Umgebungsvariablen aus. Ohne Argument werden alle Variablen ausgegeben. Mit einem Argument wird nur die angegebene Variable ausgegeben, sofern sie existiert. Andernfalls erscheint "Variable not found". Die Variablen werden in demselben Format ausgegeben, in dem sie gespeichert oder vom Dienstprogramm "env" zurückgegeben werden, also "`<name>`=`<value>`". Dies kann bei der Fehlerdiagnose von Konfigurationsdateien mit vielen Umgebungsvariablen hilfreich sein, um sicherzustellen, dass diese die erwarteten Werte enthalten. Dieser Befehl ist eingeschränkt und kann nur über Sockets ausgeführt werden, die für die Berechtigungsstufen "operator" oder "admin" konfiguriert sind.

<a id="entry-9-3-show-errors"></a>

**`show errors [<iid>|<proxy>] [request|response]`**

```haproxy
show errors [<iid>|<proxy>] [request|response]
```

Gibt die zuletzt bekannten, von Frontends und Backends erfassten HTTP/1.x-Anfrage- und Antwortfehler aus. Wird `<iid>` angegeben, beschränkt sich die Ausgabe auf Fehler des Frontends oder Backends mit der ID `<iid>`. Die Proxy-ID "-1" bewirkt die Ausgabe aller Instanzen. Wird stattdessen ein Proxy-Name angegeben, wird dessen ID als Filter verwendet. Wird nach dem Proxy-Namen oder der ID "request" oder "response" hinzugefügt, werden nur Anfrage- oder Antwortfehler ausgegeben. Dieser Befehl ist eingeschränkt und kann nur über Sockets ausgeführt werden, die für die Berechtigungsstufen "operator" oder "admin" konfiguriert sind.

Erfasst werden können die letzten Anfrage- und Antwortfehler durch Protokollverletzungen, häufig aufgrund ungültiger Zeichen in Header-Namen. Der Bericht gibt genau an, welches Zeichen das Protokoll verletzt hat. Weitere wichtige Informationen werden ebenfalls gemeldet: der genaue Zeitpunkt der Fehlererkennung, die Namen von Frontend und Backend, der Servername (falls bekannt), die interne Transaktions-ID und die Quelladresse, von der die Sitzung gestartet wurde.

Alle Zeichen werden zurückgegeben; nicht druckbare Zeichen werden kodiert. Die häufigsten (&#92;t = 9, &#92;n = 10, &#92;r = 13 und &#92;e = 27) werden als ein Buchstabe nach einem umgekehrten Schrägstrich kodiert. Der umgekehrte Schrägstrich selbst wird als '&#92;&#92;' kodiert, um Verwechslungen zu vermeiden. Andere nicht druckbare Zeichen werden als '&#92;xNN' kodiert, wobei NN die zweistellige hexadezimale Darstellung des ASCII-Codes des Zeichens ist.

Den Zeilen wird die Position ihres ersten Zeichens vorangestellt, beginnend bei 0 für den Pufferanfang. Pro Ausgabezeile wird höchstens eine Eingabezeile ausgegeben. Lange Zeilen werden auf mehrere aufeinanderfolgende Ausgabezeilen verteilt, sodass die Ausgabe nie breiter als 79 Zeichen ist. Ein solcher Zeilenumbruch ist leicht zu erkennen: Die Zeile endet nicht mit '&#92;n', und auf den Offset der nächsten Zeile folgt ein '+'-Zeichen, das die Fortsetzung der vorherigen Zeile kennzeichnet.

Beispiel:

```shell
    $ echo "show errors -1 response" | socat stdio /tmp/sock1
>>> [04/Mar/2009:15:46:56.081] backend http-in (#2): invalid response
      src 127.0.0.1, session #54, frontend fe-eth0 (#1), server s2 (#1)
      response length 213 bytes, error at position 23:

      00000  HTTP/1.0 200 OK\r\n
      00017  header/bizarre:blah\r\n
      00038  Location: blah\r\n
      00054  Long-line: this is a very long line which should b
      00104+ e broken into multiple lines on the output buffer,
      00154+  otherwise it would be too large to print in a ter
      00204+ minal\r\n
      00211  \r\n

Im obigen Beispiel hat das Backend "http-in" mit der internen ID 2 eine
ungültige Antwort seines Servers s2 mit der internen ID 1 blockiert.
Die Anfrage gehörte zur Transaktion 54 (hier "session" genannt), die von
127.0.0.1 ausging und vom Frontend fe-eth0 mit der ID 1 empfangen wurde.
Bei Erkennung des Fehlers war die Antwort insgesamt 213 Bytes lang.
Der Fehler lag an Byte 23: dem Schrägstrich ('/') im Headernamen
"header/bizarre", einem für HTTP-Headernamen ungültigen Zeichen.
```

<a id="entry-9-3-show-events"></a>

**`show events [<sink>] [-w] [-n] [-0] [-s]`**

```haproxy
show events [<sink>] [-w] [-n] [-0] [-s]
```

Ohne Option werden alle bekannten Ereignissenken und ihre Typen aufgelistet. Mit einer Option werden alle verfügbaren Ereignisse der angegebenen Senke ausgegeben, sofern sie vom Typ buffer ist. Wird nach dem Namen der Senke die Option "-w" übergeben, wartet der Befehl nach Erreichen des Pufferendes auf neue Ereignisse und zeigt sie an. Die Operation kann durch eine beliebige Eingabe (die verworfen wird) oder durch Schließen der Sitzung beendet werden. Die Option "-n" springt direkt an das Pufferende. Dies ist oft in Kombination mit "-w" nützlich, um nur neue Ereignisse zu melden. Der Einfachheit halber können mit "-wn" oder "-nw" beide Optionen gleichzeitig aktiviert werden. Standardmäßig werden alle Ereignisse durch ein Zeilenvorschubzeichen ('&#92;n' oder 10 oder 0x0A) getrennt. Mit dem Argument "-0" kann stattdessen das NUL-Zeichen ('&#92;0' oder 0) verwendet werden. Die Option "-s" bereinigt die Ausgabe, damit Binärinhalte aus erfassten oder dekodierten Daten die Darstellung im Terminal nicht verändern. Leerraumzeichen (Leerzeichen und Tabulator) werden durch ein Leerzeichen ersetzt, sodass jeder Datensatz auf einer Zeile bleibt. Andere Steuerzeichen (0x00 bis 0x1F und 0x7F) sowie Nicht-ASCII-Zeichen (0x80 und darüber) werden durch ein '?' ersetzt. Die Ausgabelänge bleibt erhalten. So können beim Ausgeben eines Rings weder ANSI-Escape-Sequenzen noch Codes für die Schreibrichtung in das Terminal des Operators eingeschleust werden. Dies ist nützlich beim Ausgeben in ein Terminal oder an ein Programm, dessen Eingabe nicht als Sonderzeichen interpretiert werden darf, etwa Überwachungsskripte, deren Ausgabe unverändert in Berichte übernommen wird.

<a id="entry-9-3-show-fd"></a>

**`show fd [-!plcfbsd]* [[<tgid>]/[<fd>] | <fd>]`**

```haproxy
show fd [-!plcfbsd]* [[<tgid>]/[<fd>] | <fd>]
```

Gibt entweder die Liste aller offenen Dateideskriptoren oder nur den Dateideskriptor mit der Nummer `<fd>` aus, wenn diese angegeben ist. Auch die Form "`<tgid>`/`<fd>`" ist zulässig. Dabei kann jede Seite als Platzhalter leer bleiben ("/`<fd>`" für fd `<fd>` über alle Thread-Gruppen hinweg, "`<tgid>`/" für alle fds von `<tgid>`). `<tgid>` wird derzeit eingelesen, aber ignoriert, bis künftig fd-Tabellen pro Thread-Gruppe unterstützt werden. Optional kann ein Satz von Flags übergeben werden, um die Ausgabe auf bestimmte FD-Typen zu beschränken oder bestimmte FD-Typen auszuschließen. Bei '-' oder '!' wird die Auswahl für die folgenden Zeichen desselben Arguments umgekehrt. Vor jedem durch Leerraum getrennten Argumentwort wird diese Umkehrung zurückgesetzt. Wählbare FD-Typen sind 'p' für Pipes, 'l' für Listener, 'c' für Verbindungen (jeden Typs), 'f' für Frontend-Verbindungen, 'b' für Backend-Verbindungen (jeden Typs), 's' für Verbindungen zu Servern und 'd' für Verbindungen zur "dispatch"-Adresse oder zur transparenten Adresse des Backends. Dabei ist 'b' eine Kurzform für 'sd' und 'c' für 'fb' oder 'fsd'. 'c!f' entspricht 'b' (alle Verbindungen außer Frontend-Verbindungen sind tatsächlich Backend-Verbindungen). Dies richtet sich ausschließlich an Entwickler, die interne Zustände beobachten müssen, um komplexe Probleme wie ungewöhnliche CPU-Auslastung zu untersuchen. Pro Zeile wird ein fd gemeldet. Sein Zustand im Poller wird mit Großbuchstaben für aktivierte und Kleinbuchstaben für deaktivierte Flags ausgegeben: "P" für „abgefragt“, "R" für „bereit“ und "A" für „aktiv“. Der Ereignisstatus verwendet "H" für „Verbindungsende“, "E" für „Fehler“, "O" für „Ausgabe“, "P" für „Priorität“ und "I" für „Eingabe“. Weitere Flags sind etwa "N" für „neu“ (gerade dem fd-Cache hinzugefügt), "U" für „aktualisiert“ (eine Aktualisierung im fd-Cache erhalten), "L" für "linger_risk" und "C" für „geklont“. Anschließend folgen die Position des Cache-Eintrags, der Zeiger auf den internen Eigentümer sowie der Zeiger auf den I/O-Callback und dessen Name, falls bekannt. Ist der Eigentümer eine Verbindung, werden die Verbindungsflags und das Ziel gemeldet (Frontend, Proxy oder Server). Ist der Eigentümer ein Listener, werden dessen Zustand und Frontend gemeldet. Ohne gute Kenntnis der Interna ist die Verwendung dieses Befehls nicht sinnvoll. Das Ausgabeformat kann sich im Laufe der Zeit weiterentwickeln, daher darf diese Ausgabe nicht von Werkzeugen ausgewertet werden, die dauerhaft funktionieren sollen. Manche internen Strukturzustände können der auflistenden Funktion verdächtig erscheinen; in diesem Fall wird der Ausgabezeile ein Ausrufezeichen ('!') angehängt. Dies kann bei der Diagnose eines Vorfalls einen Ausgangspunkt liefern.

<a id="entry-9-3-show-info"></a>

**`show info [typed|json] [desc] [float]`**

```haproxy
show info [typed|json] [desc] [float]
```

Gibt Informationen über den HAProxy-Status im aktuellen Prozess aus. Wird "typed" als optionales Argument übergeben, werden auch Feldnummern, -namen und -typen ausgegeben. So können externe Überwachungsprodukte Informationen aus ihnen unbekannten Feldern leicht abrufen, gegebenenfalls aggregieren und anschließend melden. Jedes Feld wird in einer eigenen Zeile ausgegeben. Wird "json" als optionales Argument übergeben, werden die Informationen der "typed"-Ausgabe im JSON-Format als Liste von JSON-Objekten bereitgestellt. Standardmäßig enthält das Format nur zwei durch einen Doppelpunkt (':') getrennte Spalten: links den Feldnamen, rechts den Wert. Im typisierten Ausgabeformat ist die Ausgabe eines einzelnen Objekts zusammenhängend, sodass der Empfänger nicht alles auf einmal speichern muss. Dies ist besonders zu beachten. Wird "float" als optionales Argument übergeben, können einige normalerweise als Ganzzahlen ausgegebene Felder für höhere Genauigkeit als Gleitkommazahlen ausgegeben werden. Welche Felder betroffen sind, ist bewusst nicht festgelegt, da sich dies im Laufe der Zeit ändern kann. Die Verwendung dieser Option setzt voraus, dass der Empfänger Gleitkommazahlen verarbeiten kann. Das verwendete Ausgabeformat ist sprintf("%f").

Beim typisierten Ausgabeformat besteht jede Zeile aus 4 durch Doppelpunkte (':') getrennten Spalten. Die erste Spalte enthält eine durch Punkte getrennte Folge von 3 Elementen. Das erste Element ist die numerische Position des Felds in der Liste (beginnend bei null). Diese Position darf sich im Laufe der Zeit nicht ändern. Je nach Build-Optionen oder wenn künftig Felder gelöscht werden, sind jedoch Lücken zu erwarten. Das zweite Element ist der Feldname, wie er in der Standardausgabe von "show info" erscheint. Das dritte Element ist die relative Prozessnummer, beginnend bei 1.

Der Rest der Zeile nach dem ersten Doppelpunkt folgt dem weiter oben beschriebenen „typisierten Ausgabeformat“. Die zweite Spalte (nach dem ersten ':') gibt Herkunft, Art und Geltungsbereich der Variablen an. Die dritte Spalte enthält den Feldtyp, einen der Werte "s32", "s64", "u32", "u64" und "str". Die vierte Spalte enthält den Wert selbst, den der Empfänger anhand von Spalte 3 einlesen und anhand von Spalte 2 verarbeiten kann.

Damit lautet das gesamte Zeilenformat im typisierten Modus:

```text
<field_pos>.<field_name>.<process_num>:<tags>:<type>:<value>
```

Wird "desc" an den Befehl angehängt, folgen ein weiterer Doppelpunkt und eine Zeichenfolge in Anführungszeichen mit einer Beschreibung der Metrik. Zum Zeitpunkt der Erstellung wird dies nur für das Ausgabeformat "typed" und das Standardformat unterstützt.

Beispiel:

```shell
> show info
Name: HAProxy
Version: 1.7-dev1-de52ea-146
Release_date: 2016/03/11
Nbproc: 1
Process_num: 1
Pid: 28105
Uptime: 0d 0h00m04s
Uptime_sec: 4
Memmax_MB: 0
PoolAlloc_MB: 0
PoolUsed_MB: 0
PoolFailed: 0
(...)

> show info typed
0.Name.1:POSV:str:HAProxy
1.Version.1:POSV:str:3.1-dev0-7c653d-2466
2.Release_date.1:POSV:str:2025/07/01
3.Nbthread.1:CGSV:u32:1
4.Nbproc.1:CGSV:u32:1
5.Process_num.1:KGPV:u32:1
6.Pid.1:SGPV:u32:638069
7.Uptime.1:MDPV:str:0d 0h00m07s
8.Uptime_sec.1:MDPV:u32:7
9.Memmax_MB.1:CLPV:u32:0
10.PoolAlloc_MB.1:MGPV:u32:0
11.PoolUsed_MB.1:MGPV:u32:0
12.PoolFailed.1:MCPV:u32:0
(...)
```

Im typisierten Format erleichtert die Prozess-ID am Ende der ersten Spalte das visuelle Zusammenführen der Ausgaben mehrerer Prozesse. Beispiel:

```shell
$ ( echo show info typed | socat /var/run/haproxy.sock1;    \
    echo show info typed | socat /var/run/haproxy.sock2 ) |  \
  sort -t . -k 1,1n -k 2,2 -k 3,3n
0.Name.1:POS:str:HAProxy
0.Name.2:POS:str:HAProxy
1.Version.1:POS:str:1.7-dev1-868ab3-148
1.Version.2:POS:str:1.7-dev1-868ab3-148
2.Release_date.1:POS:str:2016/03/11
2.Release_date.2:POS:str:2016/03/11
3.Nbproc.1:CGS:u32:2
3.Nbproc.2:CGS:u32:2
4.Process_num.1:KGP:u32:1
4.Process_num.2:KGP:u32:2
5.Pid.1:SGP:u32:30120
5.Pid.2:SGP:u32:30121
6.Uptime.1:MDP:str:0d 0h01m28s
6.Uptime.2:MDP:str:0d 0h01m28s
(...)
```

Das Format der JSON-Ausgabe ist in einem Schema beschrieben, das mit "show schema json" ausgegeben werden kann.

Die JSON-Ausgabe enthält keinen zusätzlichen Leerraum, um den Umfang der Ausgabe zu verringern. Für die menschliche Lesbarkeit kann es hilfreich sein, die Ausgabe durch ein Formatierungsprogramm zu leiten. Beispiel:

\$ echo "show info json" \| socat /var/run/haproxy.sock stdio \| &#92; python
-m json.tool

Die JSON-Ausgabe enthält keinen zusätzlichen Leerraum, um den Umfang der Ausgabe zu verringern. Für die menschliche Lesbarkeit kann es hilfreich sein, die Ausgabe durch ein Formatierungsprogramm zu leiten. Beispiel:

\$ echo "show info json" \| socat /var/run/haproxy.sock stdio \| &#92; python
-m json.tool

<a id="entry-9-3-show-libs"></a>

**`show libs`**

```haproxy
show libs
```

Gibt auf Systemen, die dies unterstützen, die Liste geladener gemeinsam genutzter dynamischer Bibliotheken und Objektdateien aus. Soweit verfügbar, werden für jedes gemeinsam genutzte Objekt der Bereich virtueller Adressen, die Größe und der Pfad zum Objekt angegeben. So lässt sich beispielsweise abschätzen, welche Bibliothek eine in einer Ausgabe erscheinende Funktion bereitstellt. Auf vielen Systemen ändern sich die Adressen bei jedem Neustart (Adressraumrandomisierung). Diese Liste müsste daher beim Start abgerufen werden, wenn sie zur Analyse einer Core-Datei verwendet werden soll. Dieser Befehl kann nur über Sockets ausgeführt werden, die für die Berechtigungsstufen "operator" oder "admin" konfiguriert sind. Das Ausgabeformat kann zwischen Betriebssystemen, Architekturen und sogar HAProxy-Versionen variieren; Skripte sollten sich nicht darauf verlassen.

<a id="entry-9-3-show-map"></a>

**`show map [[@<ver>] <map>]`**

```haproxy
show map [[@<ver>] <map>]
```

Gibt Informationen über Map-Konverter aus. Ohne Argument wird die Liste aller verfügbaren Maps zurückgegeben. Wird eine `<map>` angegeben, wird ihr Inhalt ausgegeben. `<map>` ist die \#`<id>` oder der `<name>`. Standardmäßig wird die aktuelle Version der Map angezeigt (die Version, gegen die derzeit geprüft wird und die in der Map-Liste als 'curr_ver' gemeldet wird). Andere Versionen können ausgegeben werden, indem '@`<ver>`' vor den Map-Bezeichner gesetzt wird. Die Version wirkt als Filter; nicht vorhandene Versionen liefern einfach kein Ergebnis. Der Wert 'entry_cnt' zählt alle Map-Einträge, nicht nur die aktiven. Er enthält daher auch Einträge, die gerade hinzugefügt werden.

In der Ausgabe ist die erste Spalte eine eindeutige Eintragskennung, die als Referenz für die Operationen "del map" und "set map" verwendet werden kann. Die zweite Spalte ist das Muster, die dritte das Sample, sofern verfügbar. Die zurückgegebenen Daten sind keine unmittelbare Liste verfügbarer Maps, sondern eine Liste aller Muster, aus denen Maps bestehen. Viele dieser Muster können auch von ACLs verwendet werden.

<a id="entry-9-3-show-peers"></a>

**`show peers [dict|-] [<peers section>]`**

```haproxy
show peers [dict|-] [<peers section>]
```

Gibt Informationen über die in "peers"-Abschnitten konfigurierten Peers aus. Ohne Argument werden die Peers aus allen "peers"-Abschnitten aufgelistet. Wird `<peers section>` angegeben, werden nur Informationen über die Peers dieses "peers"-Abschnitts ausgegeben. Wird vor dem Namen des peers-Abschnitts "dict" angegeben, werden auch die vollständigen Tx/Rx-Wörterbuch-Caches ausgegeben (sehr umfangreich). Um einen peers-Abschnitt namens "dict" auszugeben, muss möglicherweise "-" übergeben werden.

Hier folgen zwei Beispielausgaben, in denen die Peers hostA, hostB und hostC zu "sharedlb"-peers-Abschnitten gehören. Nur hostA und hostB sind verbunden. Nur hostA hat Daten an hostB gesendet.

\$ echo "show peers" \| socat - /tmp/hostA 0x55deb0224320: [15/Apr/2019:11:28:01] id=sharedlb
state=0 flags=0x3 &#92; resync_timeout=`<PAST>` task_calls=45122
0x55deb022b540: id=hostC(remote) addr=127.0.0.12:10002 status=CONN &#92;
reconnect=4s confirm=0 flags=0x0 0x55deb022a440: id=hostA(local) addr=127.0.0.10:10000 status=NONE
&#92; reconnect=`<NEVER>` confirm=0 flags=0x0 0x55deb0227d70: id=hostB(remote)
addr=127.0.0.11:10001 status=ESTA reconnect=2s confirm=0 flags=0x20000200 appctx:0x55deb028fba0
st0=7 st1=0 task_calls=14456 &#92; state=EST xprt=RAW src=127.0.0.1:37257
addr=127.0.0.10:10000 remote_table:0x55deb0224a10 id=stkt local_id=1 remote_id=1
last_local_table:0x55deb0224a10 id=stkt local_id=1 remote_id=1 shared tables:

```text
0x55deb0224a10 local_id=1 remote_id=1 flags=0x0 remote_data=0x65
  last_acked=0 last_pushed=3 last_get=0 teaching_origin=0 update=3
  table:0x55deb022d6a0 id=stkt update=3 localupdate=3 \
    commitupdate=3 syncing=0
```

\$ echo "show peers" \| socat - /tmp/hostB 0x55871b5ab320: [15/Apr/2019:11:28:03] id=sharedlb
state=0 flags=0x3 &#92; resync_timeout=`<PAST>` task_calls=3 0x55871b5b2540:
id=hostC(remote) addr=127.0.0.12:10002 status=CONN &#92; reconnect=3s
confirm=0 flags=0x0 0x55871b5b1440: id=hostB(local) addr=127.0.0.11:10001 status=NONE
&#92; reconnect=`<NEVER>` confirm=0 flags=0x0 0x55871b5aed70: id=hostA(remote)
addr=127.0.0.10:10000 status=ESTA &#92; reconnect=2s confirm=0
flags=0x20000200 appctx:0x7fa46800ee00 st0=7 st1=0 task_calls=62356 &#92;
state=EST remote_table:0x55871b5ab960 id=stkt local_id=1 remote_id=1 last_local_table:0x55871b5ab960
id=stkt local_id=1 remote_id=1 shared tables:

```text
0x55871b5ab960 local_id=1 remote_id=1 flags=0x0 remote_data=0x65
  last_acked=3 last_pushed=0 last_get=3 teaching_origin=0 update=0
  table:0x55871b5b46a0 id=stkt update=1 localupdate=0 \
    commitupdate=0 syncing=0
```

<a id="entry-9-3-show-pools"></a>

**`show pools [byname|bysize|byusage] [detailed] [match <pfx>] [<nb>]`**

```haproxy
show pools [byname|bysize|byusage] [detailed] [match <pfx>] [<nb>]
```

Den Status der internen Speicherpools ausgeben. Dies ist beispielsweise hilfreich, um bei Verdacht auf ein Speicherleck die Speichernutzung zu verfolgen. Der Befehl bewirkt genau dasselbe wie SIGQUIT im Vordergrundbetrieb, leert jedoch die Pools nicht. Standardmäßig wird die Ausgabe nicht sortiert. Bei Angabe von "byname" wird nach Poolnamen sortiert; bei "bysize" nach der Größe der Elemente in absteigender Reihenfolge; bei "byusage" nach der Gesamtnutzung in absteigender Reihenfolge, wobei nur verwendete Einträge angezeigt werden. Die Ausgabe kann auch auf die ersten `<nb>` Einträge beschränkt werden (beispielsweise beim Sortieren nach Nutzung). Mit "detailed" lassen sich weitere interne Details ausgeben, einschließlich der Liste aller zusammengeführten Pools. Wird schließlich "match" mit einem nachfolgenden Präfix angegeben, werden nur Pools angezeigt, deren Name mit diesem Präfix beginnt. Die angegebene Gesamtsumme bezieht sich nur auf Pools, die den Filterkriterien entsprechen. Beispiel:

```shell
$ socat - /tmp/haproxy.sock <<< "show pools match quic byusage"
Dumping pools usage. Use SIGQUIT to flush them.
  - Pool quic_conn_r (65560 bytes): 1337 allocated (87653720 bytes), ...
  - Pool quic_crypto (1048 bytes): 6685 allocated (7005880 bytes), ...
  - Pool quic_conn (4056 bytes): 1337 allocated (5422872 bytes), ...
  - Pool quic_rxbuf (262168 bytes): 8 allocated (2097344 bytes), ...
  - Pool quic_conne (184 bytes): 9359 allocated (1722056 bytes), ...
  - Pool quic_frame (184 bytes): 7938 allocated (1460592 bytes), ...
  - Pool quic_tx_pac (152 bytes): 6454 allocated (981008 bytes), ...
  - Pool quic_tls_ke (56 bytes): 12033 allocated (673848 bytes), ...
  - Pool quic_rx_pac (408 bytes): 1596 allocated (651168 bytes), ...
  - Pool quic_tls_se (88 bytes): 6685 allocated (588280 bytes), ...
  - Pool quic_cstrea (88 bytes): 4011 allocated (352968 bytes), ...
  - Pool quic_tls_iv (24 bytes): 12033 allocated (288792 bytes), ...
  - Pool quic_dgram (344 bytes): 732 allocated (251808 bytes), ...
  - Pool quic_arng (56 bytes): 4011 allocated (224616 bytes), ...
  - Pool quic_conn_c (152 bytes): 1337 allocated (203224 bytes), ...
Total: 15 pools, 109578176 bytes allocated, 109578176 used ...
```

<a id="entry-9-3-show-profiling"></a>

**`show profiling [{all | status | tasks | memory}] [byaddr|bytime|byctx|aggr|<max_lines>]*`**

```haproxy
show profiling [{all | status | tasks | memory}] [byaddr|bytime|byctx|aggr|<max_lines>]*
```

Die aktuellen Profiling-Einstellungen zeilenweise sowie den zu ihrer Änderung erforderlichen Befehl ausgeben. Wenn das Task-Profiling aktiviert ist, werden auch einige vom Scheduler erfasste Statistiken je Funktion ausgegeben, zusammen mit einer Zusammenfassung der Anzahl der Aufrufe, der gesamten und durchschnittlichen CPU-Zeit sowie der gesamten und durchschnittlichen Latenz. Wenn das Speicher-Profiling aktiviert ist, werden beispielsweise die Anzahl der Speicherzuweisungen und -freigaben sowie ihre Größen gemeldet. Mit den entsprechenden Schlüsselwörtern kann die Ausgabe auf den Profiling-Status, die Tasks oder das Speicher-Profiling beschränkt werden; standardmäßig werden sämtliche Profiling-Informationen ausgegeben. Mit einem numerischen Grenzwert lässt sich auch die Anzahl der Ausgabezeilen je Kategorie beschränken. Die Ausgabe kann nach Adresse, gesamter Ausführungszeit oder Aufrufkontext statt nach Nutzung sortiert werden, etwa um aufeinanderfolgende Aufrufe leichter zu vergleichen oder Optimierungsbedarf zu ermitteln. Außerdem lässt sich die Task-Aktivität nach aufgerufener Funktion zusammenfassen, statt die Details anzuzeigen. Profiling richtet sich hauptsächlich an Entwickler, da es Hinweise darauf liefert, wo der Code CPU-Zyklen oder Speicher verschwendet. Für die Überwachung liefert diese Ausgabe keine nützlichen Informationen.

<a id="entry-9-3-show-resolvers"></a>

**`show resolvers [<resolvers section id>]`**

```haproxy
show resolvers [<resolvers section id>]
```

Statistiken für den angegebenen resolvers-Abschnitt ausgeben, oder für alle resolvers-Abschnitte, wenn kein Abschnitt angegeben wird.

Für jeden Nameserver werden die folgenden Zähler ausgegeben:

```text
sent: Anzahl der an diesen Server gesendeten DNS-Anfragen
valid: Anzahl der von diesem Server empfangenen gültigen DNS-Antworten
update: Anzahl der DNS-Antworten, mit denen die IP-Adresse des Servers aktualisiert wurde
cname: Anzahl der CNAME-Antworten
cname_error: Bei diesem Server aufgetretene CNAME-Fehler
any_err: Anzahl der leeren Antworten (d. h.: der Server unterstützt den Typ ANY nicht)
nx: Von diesem Server empfangene Antwort, dass die Domain nicht existiert
timeout: Anzahl der Fälle, in denen dieser Server nicht rechtzeitig geantwortet hat
refused: Anzahl der von diesem Server abgelehnten Anfragen
other: Alle anderen DNS-Fehler
invalid: Ungültige DNS-Antwort (aus Protokollsicht)
too_big: Zu große Antwort
outdated: Anzahl der zu spät eingetroffenen Antworten (nach einem anderen Nameserver)
```

<a id="entry-9-3-show-quic"></a>

**`show quic [<format>] [<filter>]`**

```haproxy
show quic [<format>] [<filter>]
```

Informationen zu allen aktiven QUIC-Frontend-Verbindungen ausgeben. Dieser Befehl ist zugriffsbeschränkt und kann nur über Sockets ausgeführt werden, die für die Berechtigungsstufen "operator" oder "admin" konfiguriert sind.

Ein optionales Argument steuert den Detailgrad der Ausgabe. Sein Wert lässt sich auf verschiedene Weise interpretieren. Als erste Möglichkeit können vordefinierte Werte verwendet werden: "oneline" für das Standardformat, "stream" für die Auflistung aller aktiven Streams und "full" für die Anzeige sämtlicher Informationen. Alternativ kann eine kommagetrennte Liste von Feldern angegeben werden, um die Ausgabe zu beschränken. Derzeit werden die Werte "tp", "sock", "pktns", "cc" und "mux" unterstützt. Schließlich zeigt "help" im Formatargument stattdessen eine ausführlichere Hilfe an.

Das letzte Argument beschränkt oder erweitert die Verbindungsliste. Standardmäßig werden nur aktive Frontend-Verbindungen angezeigt. Mit dem zusätzlichen Argument "clo" werden stattdessen Frontend-Verbindungen angezeigt, die gerade geschlossen werden, mit "be" Backend-Verbindungen und mit "all" alle Kategorien. Durch Angabe der hexadezimalen Adresse kann die Ausgabe auch auf eine einzelne Verbindung beschränkt werden.

<a id="entry-9-3-show-servers-conn"></a>

**`show servers conn [<backend>]`**

```haproxy
show servers conn [<backend>]
```

Den Zustand der aktuellen und ungenutzten Verbindungen der Server ausgeben, die zum angegebenen Backend gehören (oder zu allen Backends, wenn keines angegeben wird). Es kann ein Backendname oder eine Kennung verwendet werden.

Die Ausgabe besteht aus einer Kopfzeile mit den Feldbezeichnungen und anschließend einer Zeile je Server mit Backendname und -ID, Servername und -ID, Adresse, Port sowie einer Reihe von Werten. Die Anzahl der Felder hängt von der Anzahl der Threads ab. Das genaue Ausgabeformat kann sich je nach Version und Threadanzahl geringfügig unterscheiden. Beim Extrahieren von Ausgabewerten muss die Kopfzeile beachtet werden, um die Spalten zuzuordnen. Auch die Threadanzahl ist zu berücksichtigen, da die letzten Spalten Werte je Thread enthalten:

```text
bkname/svname         Backend-Name '/' Servername
bkid/svid             Backend-ID '/' Server-ID
addr                  IP-Adresse des Servers
port                  Port des Servers (oder null, falls keiner vorhanden)
-                     Unbenutztes Feld, dient als optisches Trennzeichen
purge_delay           Intervall zwischen Verbindungsbereinigungen, in Millisekunden
served                Anzahl der derzeit verwendeten Verbindungen
used_cur              Anzahl der derzeit verwendeten Verbindungen;
                      an eine Sitzung gebundene Verbindungen sind ausgenommen
used_max              Höchster Wert von used_cur seit dem Prozessstart
need_est              Gleitende Schätzung der insgesamt benötigten Verbindungen
idle_sess             Anzahl der als privat gekennzeichneten inaktiven Verbindungen
unsafe_nb             Anzahl der als "unsafe" betrachteten inaktiven Verbindungen
safe_nb               Anzahl der als "safe" betrachteten inaktiven Verbindungen
idle_lim              Konfigurierte Höchstzahl inaktiver Verbindungen
idle_cur              Summe der derzeit inaktiven Verbindungen aller Threads
idle_per_thr[NB]      Inaktive Verbindungen pro Thread für jeden der NB Threads
```

HAProxy beendet alle `<purge_delay>` einen Teil von `<idle_cur>`, wenn die Summe aus `<idle_cur>` und `<used_cur>` den Schätzwert `<need_est>` überschreitet. Dieser Schätzwert ändert sich abhängig von der Verbindungsaktivität.

Da ungenutzte Verbindungen auf mehrere Threads verteilt sind, können sich einige Werte bereits nach dem Lesen ändern. Daher ist die Konsistenz innerhalb einer Zeile nicht gewährleistet. Diese Ausgabe dient hauptsächlich der Fehlersuche und eignet sich weder für die regelmäßige Überwachung noch für die grafische Darstellung.

<a id="entry-9-3-show-servers-state"></a>

**`show servers state [<backend>]`**

```haproxy
show servers state [<backend>]
```

Den Zustand der Server ausgeben, die in der laufenden Konfiguration enthalten sind. Mit einem Backendnamen oder einer Kennung kann die Ausgabe auf dieses Backend beschränkt werden.

Die Ausgabe hat das folgende Format:

- Die erste Zeile enthält die Formatversion (1 in dieser Spezifikation);
- die zweite Zeile enthält die Spaltenüberschriften mit einem vorangestellten Rautezeichen ('#');
- die dritte und alle weiteren Zeilen enthalten Daten;
- jede Zeile, die mit einem Rautezeichen ('#') beginnt, gilt als Kommentar.

Da mehrere Ausgabeversionen nebeneinander existieren können, sind nachfolgend die Felder und ihre Reihenfolge je Dateiformatversion aufgeführt:

```text
1:
  be_id:                       Eindeutige Backend-ID.
  be_name:                     Backend-Bezeichnung.
  srv_id:                      Eindeutige Server-ID (im Backend).
  srv_name:                    Serverbezeichnung.
  srv_addr:                    IP-Adresse des Servers.
  srv_op_state:                Betriebszustand des Servers (UP/DOWN/...).
                                 0 = SRV_ST_STOPPED
                                   Der Server ist ausgefallen.
                                 1 = SRV_ST_STARTING
                                   Der Server läuft an (aktiv, aber
                                   gedrosselt).
                                 2 = SRV_ST_RUNNING
                                   Der Server ist vollständig aktiv.
                                 3 = SRV_ST_STOPPING
                                   Der Server ist aktiv, wird aber geordnet
                                   beendet (z. B.: 404).
  srv_admin_state:             Verwaltungszustand des Servers (MAINT/DRAIN/...).
                               Der Zustand ist eine Maske aus Werten:
                                 0x01 = SRV_ADMF_FMAINT
                                   Der Server wurde explizit in den
                                   Wartungszustand gezwungen.
                                 0x02 = SRV_ADMF_IMAINT
                                   Der Server hat den Wartungszustand von
                                   einem überwachten Server übernommen.
                                 0x04 = SRV_ADMF_CMAINT
                                   Der Server ist aufgrund der
                                   Konfiguration im Wartungszustand.
                                 0x08 = SRV_ADMF_FDRAIN
                                   Der Server wurde explizit in den
                                   Drain-Zustand gezwungen.
                                 0x10 = SRV_ADMF_IDRAIN
                                   Der Server hat den Drain-Zustand von
                                   einem überwachten Server übernommen.
                                 0x20 = SRV_ADMF_RMAINT
                                   Der Server ist wegen einer fehlgeschlagenen
                                   IP-Adressauflösung im Wartungszustand.
                                 0x40 = SRV_ADMF_HMAINT
                                   Der FQDN des Servers wurde über den
                                   Statistik-Socket gesetzt.

  srv_uweight:                 Für den Benutzer sichtbares Servergewicht.
  srv_iweight:                 Anfängliches Servergewicht.
  srv_time_since_last_change:  Zeit seit der letzten Änderung des Betriebszustands.
  srv_check_status:            Status des letzten Health Checks.
  srv_check_result:            Letztes Prüfergebnis (FAILED/PASSED/...).
                                 0 = CHK_RES_UNKNOWN
                                   Wird standardmäßig damit initialisiert.
                                 1 = CHK_RES_NEUTRAL
                                   Gültige Prüfung ohne Statusinformation.
                                 2 = CHK_RES_FAILED
                                   Prüfung fehlgeschlagen.
                                 3 = CHK_RES_PASSED
                                   Prüfung erfolgreich; der Server ist
                                   wieder vollständig aktiv.
                                 4 = CHK_RES_CONDPASS
                                   Die Prüfung meldet, dass der Server
                                   keine neuen Sitzungen annehmen möchte.
  srv_check_health:            Aktueller Zähler für rise / fall der Prüfungen.
  srv_check_state:             Zustand der Prüfung (ENABLED/PAUSED/...).
                               Der Zustand ist eine Maske aus Werten:
                                 0x01 = CHK_ST_INPROGRESS
                                   Eine Prüfung läuft derzeit.
                                 0x02 = CHK_ST_CONFIGURED
                                   Diese Prüfung ist konfiguriert und
                                   kann aktiviert werden.
                                 0x04 = CHK_ST_ENABLED
                                   Diese Prüfung ist derzeit administrativ
                                   aktiviert.
                                 0x08 = CHK_ST_PAUSED
                                   Prüfungen sind wegen Wartung angehalten
                                   (nur Health Checks).
  srv_agent_state:             Zustand der Agentenprüfung (ENABLED/PAUSED/...).
                               Dieser Zustand verwendet dieselben Maskenwerte
                               wie "srv_check_state", ergänzt um diesen Wert:
                                 0x10 = CHK_ST_AGENT
                                   Die Prüfung ist eine Agentenprüfung
                                   (andernfalls ein Health Check).
  bk_f_forced_id:              Flag, das angibt, ob die Backend-ID durch
                               die Konfiguration erzwungen wird.
  srv_f_forced_id:             Flag, das angibt, ob die Server-ID durch
                               die Konfiguration erzwungen wird.
  srv_fqdn:                    FQDN des Servers.
  srv_port:                    Port des Servers.
  srvrecord:                   DNS-SRV-Eintrag, der diesem SRV zugeordnet ist.
  srv_use_ssl:                 ssl für Serververbindungen verwenden.
  srv_check_port:              Port für den Health Check des Servers.
  srv_check_addr:              Adresse für den Health Check des Servers.
  srv_agent_addr:              Adresse des Health-Agenten des Servers.
  srv_agent_port:              Port des Health-Agenten des Servers.
```

<a id="entry-9-3-show-sess"></a>

**`show sess [<options>*]`**

```haproxy
show sess [<options>*]
```

Alle bekannten aktiven Streams ausgeben (früher als „Sitzungen“ bezeichnet). Dies bei langsamen Verbindungen vermeiden, da die Ausgabe sehr groß sein kann. Dieser Befehl ist zugriffsbeschränkt und kann nur über Sockets ausgeführt werden, die für die Berechtigungsstufen "operator" oder "admin" konfiguriert sind. Auf Rechnern, deren Verbindungen schnell erneuert werden, kann die Ausgabe weniger Einträge enthalten, als tatsächlich vorhanden sind: Ausgegeben werden alle bestehenden Streams bis zu dem letzten, der vor der Befehlseingabe angelegt wurde; Streams, die zwischenzeitlich beendet werden, erscheinen nicht. Die unterstützten Optionen sind weiter unten aufgeführt.

<a id="entry-9-3-show-sess-2"></a>

**`show sess [<id> | all | help] [<options>*]`**

```haproxy
show sess [<id> | all | help] [<options>*]
```

Viele interne Informationen zu den passenden Streams anzeigen. Der Befehl kennt zwei Ausgabeformate: ein kurzes, das standardmäßig verwendet wird, wenn keine bestimmte Streamkennung angefordert wird, und ein erweitertes für die Auflistung bestimmter Streams. Das kurze Format, das "show sess" standardmäßig verwendet, gibt nur einen Stream je Zeile mit wenigen Informationen aus. Am Zeilenanfang steht die Streamkennung in hexadezimaler Form (sie entspricht dem Zeiger auf den Stream).

In der erweiterten Form, die "show sess `<id>`" oder "show sess all" verwendet, werden Streams mit sehr vielen Details zur Fehlersuche über mehrere Zeilen ausgegeben (jeweils etwa 20), weiterhin beginnend mit ihrer Kennung. Als Trennzeichen zwischen Streams dient hier die Kennung am Zeilenanfang; zusätzliche Zeilen desselben Streams beginnen mit einem oder mehreren Leerzeichen (die Streamausgabe ist eingerückt). Die Ausgabe vieler Streams kann sehr groß werden, viel Zeit beanspruchen und die CPU stark belasten. Daher ist es stets besser, nur das erforderliche Minimum auszugeben. Für die meisten Benutzer sind diese Informationen nutzlos, HAProxy-Entwickler können sie jedoch zur Untersuchung komplexer Fehler verwenden. Das genaue Ausgabeformat ist absichtlich nicht dokumentiert, damit es sich entsprechend den Anforderungen frei weiterentwickeln kann, auch in stabilen Entwicklungszweigen. Zur Interpretation dieser Ausgabe soll die Funktion strm_dump_to_buffer() in src/stream.c herangezogen werden, um die genaue Bedeutung bestimmter Felder zu ermitteln.

Das Argument "help" zeigt ausführliche Hinweise zur Verwendung des Befehls an, statt Streams auszugeben.

Mit Optionen lässt sich die Ausgabe anpassen oder filtern. Folgende Optionen werden unterstützt: - backend `<b>` zeigt nur Streams an, die diesem Backend zugeordnet sind - frontend `<f>` zeigt nur Streams an, die diesem Frontend zugeordnet sind - older `<age>` zeigt nur Streams an, die älter als `<age>` Sekunden sind - server `<b/s>` zeigt nur Streams an, die dieser Kombination aus Backend und Server zugeordnet sind - show-uri gibt die URI der Transaktion aus, wie sie während der Anfrageanalyse erfasst wurde. Sie wird nur angezeigt, wenn sie erfasst wurde. - susp zeigt nur Streams an, die Entwickler anhand von Kriterien als verdächtig einstufen, die sich im Laufe der Zeit oder zwischen Versionen ändern können.

<a id="entry-9-3-show-stat"></a>

**`show stat [domain <resolvers|proxy>] [{<iid>|<proxy>} <type> <sid>] \`**

```haproxy
show stat [domain <resolvers|proxy>] [{<iid>|<proxy>} <type> <sid>] \
          [typed|json] [desc] [up|no-maint]
```

Statistiken ausgeben. Die Domäne bestimmt, welche Statistiken ausgegeben werden; derzeit stehen resolvers und proxy zur Verfügung. Standardmäßig wird das CSV-Format verwendet. Das oben beschriebene erweiterte typisierte Ausgabeformat lässt sich aktivieren, indem "typed" nach den übrigen Argumenten angegeben wird; mit "json" nach den übrigen Argumenten erfolgt die Ausgabe in JSON. Durch Angabe von `<id>`, `<type>` und `<sid>` lassen sich nur ausgewählte Elemente ausgeben: - `<iid>` ist eine Proxy-ID; -1 gibt alles aus. Alternativ kann ein Proxyname `<proxy>` angegeben werden. In diesem Fall dient die ID dieses Proxys zur Auswahl. - `<type>` wählt den Typ der ausgebbaren Objekte: 1 für Frontends, 2 für Backends, 4 für Server, -1 für alles. Diese Werte können durch ein bitweises ODER verknüpft werden, beispielsweise:

```text
1 + 2     = 3   -> frontend + backend.
1 + 2 + 4 = 7   -> frontend + backend + server.
```

    - `<sid>` ist eine Server-ID; -1 gibt alles aus dem ausgewählten Proxy aus.

Beispiel:

```shell
    $ echo "show info;show stat" | socat stdio unix-connect:/tmp/sock1
>>> Name: HAProxy
    Version: 1.4-dev2-49
    Release_date: 2009/09/23
    Nbproc: 1
    Process_num: 1
    (...)

    # pxname,svname,qcur,qmax,scur,smax,slim,stot,bin,bout,dreq,  (...)
    stats,FRONTEND,,,0,0,1000,0,0,0,0,0,0,,,,,OPEN,,,,,,,,,1,1,0, (...)
    stats,BACKEND,0,0,0,0,1000,0,0,0,0,0,,0,0,0,0,UP,0,0,0,,0,250,(...)
    (...)
    www1,BACKEND,0,0,0,0,1000,0,0,0,0,0,,0,0,0,0,UP,1,1,0,,0,250, (...)

    $
```

In diesem Beispiel wurden zwei Befehle gleichzeitig ausgeführt. So lässt sich im Mehrprozessbetrieb leicht erkennen, auf welchen Prozess sich die Statistiken beziehen. Beim typisierten Ausgabeformat ist dies nicht erforderlich, da die Prozessnummer in jeder Zeile ausgegeben wird. Die Leerzeile nach der Informationsausgabe kennzeichnet das Ende des ersten Blocks. Eine ähnliche Leerzeile erscheint am Ende des zweiten Blocks (Statistiken), damit erkennbar ist, dass die Ausgabe nicht abgeschnitten wurde.

Mit "typed" eignet sich das Ausgabeformat besser für Überwachungswerkzeuge, da es numerische Positionen liefert und den Typ jedes Ausgabefelds angibt. Jeder Wert steht in einer eigenen Zeile mit Prozessnummer, Elementnummer, Art, Herkunft und Geltungsbereich. Dasselbe Format ist über die HTTP-Statistiken verfügbar, indem ";typed" an die URI angehängt wird. Besonders zu beachten ist, dass beim typisierten Ausgabeformat die Daten eines einzelnen Objekts zusammenhängend ausgegeben werden, sodass ein verarbeitendes Programm nicht alles gleichzeitig speichern muss.

Mit dem Modifikator "up" werden nur Server aufgelistet, die als verfügbar gemeldet oder nicht geprüft werden. Nicht verfügbare Server sowie solche mit nicht aufgelöster Adresse oder im Wartungsmodus werden nicht aufgelistet. Dies entspricht der Option ";up" der HTTP-Statistiken. Ebenso verhält sich der Modifikator "no-maint" wie der HTTP-Modifikator ";no-maint" und schließt deaktivierte Server aus der Liste aus. Der Unterschied besteht darin, dass aktivierte, aber nicht verfügbare Server weiterhin aufgeführt werden.

Beim typisierten Ausgabeformat besteht jede Zeile aus 4 durch Doppelpunkte (':') getrennten Spalten. Die erste Spalte ist eine durch Punkte getrennte Folge von 5 Elementen. Das erste Element ist ein Buchstabe, der den Typ des beschriebenen Objekts angibt. Derzeit sind folgende Objekttypen bekannt: 'F' für ein Frontend, 'B' für ein Backend, 'L' für einen Listener und 'S' für einen Server. Das zweite Element ist eine positive Ganzzahl, die die eindeutige Kennung des Proxys darstellt, zu dem das Objekt gehört. Es entspricht der Spalte "iid" der CSV-Ausgabe und stimmt mit dem Wert der optionalen Direktive "id" im Frontend- oder Backend-Abschnitt überein. Das dritte Element ist eine positive Ganzzahl mit der eindeutigen Objektkennung innerhalb des Proxys und entspricht der Spalte "sid" der CSV-Ausgabe. Bei der Ausgabe eines Frontends oder Backends wird die ID 0 gemeldet. Bei einem Listener oder Server entspricht sie dessen jeweiliger ID innerhalb des Proxys. Das vierte Element ist die numerische Position des Felds in der Liste (beginnend bei null). Diese Position darf sich im Laufe der Zeit nicht ändern; abhängig von den Build-Optionen oder bei einer künftigen Entfernung von Feldern sind jedoch Lücken zu erwarten. Das fünfte Element ist der Feldname, wie er in der CSV-Ausgabe erscheint. Das sechste Element ist eine positive Ganzzahl und gibt die relative Prozessnummer an, beginnend bei 1.

Der Rest der Zeile nach dem ersten Doppelpunkt folgt dem oben beschriebenen „typisierten Ausgabeformat“. Die zweite Spalte (nach dem ersten ':') gibt Herkunft, Art, Geltungsbereich und Persistenzstatus der Variablen an. Die dritte Spalte gibt den Feldtyp an: "s32", "s64", "u32", "u64", "flt" oder "str". Die vierte Spalte enthält den Wert selbst, den ein verarbeitendes Programm anhand von Spalte 3 parsen und anhand von Spalte 2 verarbeiten kann.

Wird "desc" an den Befehl angehängt, werden ein weiterer Doppelpunkt und eine Zeichenkette in Anführungszeichen mit einer Beschreibung der Metrik angefügt. Zum Zeitpunkt der Erstellung dieser Dokumentation wird dies nur für das Ausgabeformat "typed" unterstützt.

Das gesamte Zeilenformat im typisierten Modus lautet somit:

```text
<obj>.<px_id>.<id>.<fpos>.<fname>.<process_num>:<tags>:<type>:<value>
```

Ein Beispiel für das typisierte Ausgabeformat:

```shell
$ echo "show stat typed" | socat stdio unix-connect:/tmp/sock1
F.2.0.0.pxname.1:KNSV:str:dummy
F.2.0.1.svname.1:KNSV:str:FRONTEND
F.2.0.4.scur.1:MGPV:u32:0
F.2.0.5.smax.1:MMPV:u32:0
F.2.0.6.slim.1:CLPV:u32:524269
F.2.0.7.stot.1:MCPP:u64:0
F.2.0.8.bin.1:MCPP:u64:0
F.2.0.9.bout.1:MCPP:u64:0
F.2.0.10.dreq.1:MCPP:u64:0
F.2.0.11.dresp.1:MCPP:u64:0
F.2.0.12.ereq.1:MCPP:u64:0
F.2.0.17.status.1:SGPV:str:OPEN
F.2.0.26.pid.1:KGPV:u32:1
F.2.0.27.iid.1:KGSV:u32:2
F.2.0.28.sid.1:KGSV:u32:0
F.2.0.32.type.1:CGSV:u32:0
F.2.0.33.rate.1:MRPP:u32:0
F.2.0.34.rate_lim.1:CLPV:u32:0
F.2.0.35.rate_max.1:MMPV:u32:0
F.2.0.46.req_rate.1:MRPP:u32:0
F.2.0.47.req_rate_max.1:MMPV:u32:0
F.2.0.48.req_tot.1:MCPP:u64:0
F.2.0.51.comp_in.1:MCPP:u64:0
F.2.0.52.comp_out.1:MCPP:u64:0
F.2.0.53.comp_byp.1:MCPP:u64:0
F.2.0.54.comp_rsp.1:MCPP:u64:0
(...)
```

Im typisierten Format erleichtert die Prozess-ID am Ende der ersten Spalte das visuelle Zusammenführen der Ausgaben mehrerer Prozesse. Dies zeigt das folgende Beispiel, in dem jede Zeile für jeden Prozess erscheint:

```shell
$ ( echo show stat typed | socat /var/run/haproxy.sock1 -; \
    echo show stat typed | socat /var/run/haproxy.sock2 - ) | \
  sort -t . -k 1,1 -k 2,2n -k 3,3n -k 4,4n -k 5,5 -k 6,6n
B.3.0.0.pxname.1:KNSV:str:private-backend
B.3.0.0.pxname.2:KNSV:str:private-backend
B.3.0.1.svname.1:KNSV:str:BACKEND
B.3.0.1.svname.2:KNSV:str:BACKEND
B.3.0.2.qcur.1:MGPV:u32:0
B.3.0.2.qcur.2:MGPV:u32:0
B.3.0.3.qmax.1:MMPV:u32:0
B.3.0.3.qmax.2:MMPV:u32:0
B.3.0.4.scur.1:MGPV:u32:0
B.3.0.4.scur.2:MGPV:u32:0
B.3.0.5.smax.1:MMPV:u32:0
B.3.0.5.smax.2:MMPV:u32:0
B.3.0.6.slim.1:CLPV:u32:1000
B.3.0.6.slim.2:CLPV:u32:1000
(...)
```

Das Format der JSON-Ausgabe ist in einem Schema beschrieben, das mit "show schema json" ausgegeben werden kann.

Die JSON-Ausgabe enthält keine zusätzlichen Leerraumzeichen, um ihr Volumen zu verringern. Für das Lesen durch Menschen kann es hilfreich sein, die Ausgabe durch ein Werkzeug zur lesbaren Formatierung zu leiten. Beispiel:

\$ echo "show stat json" \| socat /var/run/haproxy.sock stdio \| &#92; python
-m json.tool

Die JSON-Ausgabe enthält keine zusätzlichen Leerraumzeichen, um ihr Volumen zu verringern. Für das Lesen durch Menschen kann es hilfreich sein, die Ausgabe durch ein Werkzeug zur lesbaren Formatierung zu leiten. Beispiel:

\$ echo "show stat json" \| socat /var/run/haproxy.sock stdio \| &#92; python
-m json.tool

<a id="entry-9-3-show-ssl-ca-file"></a>

**`show ssl ca-file [[*][\]<cafile>[:<index>]]`**

```haproxy
show ssl ca-file [[*][\]<cafile>[:<index>]]
```

Die Liste der in den Prozess geladenen CA-Dateien und die jeweilige Anzahl ihrer Zertifikate anzeigen. Die Zertifikate werden von keinem Frontend oder Backend verwendet, solange ihr Status nicht "Used" lautet. In der Liste kann ein Eintrag "@system-ca" erscheinen, den der httpclient standardmäßig lädt. Er enthält die von OpenSSL zurückgegebene Liste der vertrauenswürdigen CAs des Systems. Ist einem Dateinamen ein Sternchen vorangestellt, handelt es sich um eine noch nicht festgeschriebene Transaktion. Wird eine `<cafile>` ohne `<index>` angegeben, werden der Status der CA-Datei ("Used"/"Unused") und anschließend Details zu allen in der CA-Datei enthaltenen Zertifikaten angezeigt. Die angezeigten Details entsprechen für jedes Zertifikat denen des Befehls "show ssl cert". Wird eine `<cafile>` mit einem nachfolgenden `<index>` angegeben, werden nur die Details des Zertifikats mit dem angegebenen Index angezeigt. Die Indizes beginnen bei 1. Ist der Index ungültig (beispielsweise zu groß), wird nichts angezeigt. Dieser Befehl kann helfen zu prüfen, ob eine CA-Datei korrekt aktualisiert wurde. Die Details einer laufenden Transaktion lassen sich ebenfalls anzeigen, indem dem Dateinamen ein '*' vorangestellt wird. Ist das erste Zeichen des Dateinamens ein '*', kann es mit '&#92;\*' maskiert werden.

Beispiel:

```shell
$ echo "show ssl ca-file" | socat /var/run/haproxy.master -
# transaction
*cafile.crt - 2 certificate(s)
# filename
cafile.crt - 1 certificate(s)

$ echo "show ssl ca-file cafile.crt" | socat /var/run/haproxy.master -
Filename: /home/tricot/work/haproxy/reg-tests/ssl/set_cafile_ca2.crt
Status: Used

Certificate #1:
Serial: 11A4D2200DC84376E7D233CAFF39DF44BF8D1211
notBefore: Apr  1 07:40:53 2021 GMT
notAfter: Aug 17 07:40:53 2048 GMT
Subject Alternative Name:
Algorithm: RSA4096
SHA1 FingerPrint: A111EF0FEFCDE11D47FE3F33ADCA8435EBEA4864
Subject: /C=FR/ST=Some-State/O=HAProxy Technologies/CN=HAProxy Technologies CA
Issuer: /C=FR/ST=Some-State/O=HAProxy Technologies/CN=HAProxy Technologies CA

$ echo "show ssl ca-file *cafile.crt:2" | socat /var/run/haproxy.master -
Filename: */home/tricot/work/haproxy/reg-tests/ssl/set_cafile_ca2.crt
Status: Unused

Certificate #2:
Serial: 587A1CE5ED855040A0C82BF255FF300ADB7C8136
[...]
```

<a id="entry-9-3-show-ssl-cert"></a>

**`show ssl cert [[*][\]<filename>]`**

```haproxy
show ssl cert [[*][\]<filename>]
```

Die Liste der in den Prozess geladenen Zertifikate anzeigen. Sie werden von keinem Frontend oder Backend verwendet, solange ihr Status nicht "Used" lautet. Ist einem Dateinamen ein Sternchen vorangestellt, handelt es sich um eine noch nicht festgeschriebene Transaktion. Wird ein Dateiname angegeben, werden Details zum Zertifikat angezeigt. Dieser Befehl kann helfen zu prüfen, ob ein Zertifikat korrekt aktualisiert wurde. Details zu einer Transaktion lassen sich ebenfalls anzeigen, indem dem Dateinamen ein '*' vorangestellt wird. Ist das erste Zeichen des Dateinamens ein '*', kann es mit '&#92;\*' maskiert werden. Mit diesem Befehl lassen sich auch die Details der OCSP-Antwort eines Zertifikats anzeigen, indem die Erweiterung ".ocsp" an den Dateinamen angehängt wird. Dies funktioniert sowohl für bereits festgeschriebene als auch für laufende Transaktionen. Bei einem Zertifikat aus einer festgeschriebenen Transaktion entspricht dieser Befehl dem Aufruf von "show ssl ocsp-response" mit der zugehörigen OCSP-Antwort-ID des Zertifikats.

Beispiel:

```shell
$ echo "@1 show ssl cert" | socat /var/run/haproxy.master -
# transaction
*test.local.pem
# filename
test.local.pem

$ echo "@1 show ssl cert test.local.pem" | socat /var/run/haproxy.master -
Filename: test.local.pem
Status: Used
Serial: 03ECC19BA54B25E85ABA46EE561B9A10D26F
notBefore: Sep 13 21:20:24 2019 GMT
notAfter: Dec 12 21:20:24 2019 GMT
Issuer: /C=US/O=Let's Encrypt/CN=Let's Encrypt Authority X3
Subject: /CN=test.local
Subject Alternative Name: DNS:test.local, DNS:imap.test.local
Algorithm: RSA2048
SHA1 FingerPrint: 417A11CAE25F607B24F638B4A8AEE51D1E211477

$ echo "@1 show ssl cert *test.local.pem" | socat /var/run/haproxy.master -
Filename: *test.local.pem
Status: Unused
[...]

$ echo "@1 show ssl cert \*.local.pem" | socat /var/run/haproxy.master -
Filename: *.local.pem
Status: Used
[...]
```

<a id="entry-9-3-show-ssl-crl-file"></a>

**`show ssl crl-file [[*][\]<crlfile>[:<index>]]`**

```haproxy
show ssl crl-file [[*][\]<crlfile>[:<index>]]
```

Die Liste der in den Prozess geladenen CRL-Dateien anzeigen. Sie werden von keinem Frontend oder Backend verwendet, solange ihr Status nicht "Used" lautet. Ist einem Dateinamen ein Sternchen vorangestellt, handelt es sich um eine noch nicht festgeschriebene Transaktion. Wird eine `<crlfile>` ohne `<index>` angegeben, werden der Status der CRL-Datei ("Used"/"Unused") und anschließend Details zu allen in der CRL-Datei enthaltenen Sperrlisten angezeigt. Die Details jeder Liste beruhen auf der Ausgabe von "openssl crl -text -noout -in `<file>`". Wird eine `<crlfile>` mit einem nachfolgenden `<index>` angegeben, werden nur die Details der Liste mit dem angegebenen Index angezeigt. Die Indizes beginnen bei 1. Ist der Index ungültig (beispielsweise zu groß), wird nichts angezeigt. Dieser Befehl kann helfen zu prüfen, ob eine CRL-Datei korrekt aktualisiert wurde. Die Details einer laufenden Transaktion lassen sich ebenfalls anzeigen, indem dem Dateinamen ein '*' vorangestellt wird. Ist das erste Zeichen des Dateinamens ein '*', kann es mit '&#92;\*' maskiert werden.

Beispiel:

```shell
$ echo "show ssl crl-file" | socat /var/run/haproxy.master -
# transaction
*crlfile.pem
# filename
crlfile.pem

$ echo "show ssl crl-file crlfile.pem" | socat /var/run/haproxy.master -
Filename: /home/tricot/work/haproxy/reg-tests/ssl/crlfile.pem
Status: Used

Certificate Revocation List #1:
Version 1
Signature Algorithm: sha256WithRSAEncryption
Issuer: /C=FR/O=HAProxy Technologies/CN=Intermediate CA2
Last Update: Apr 23 14:45:39 2021 GMT
Next Update: Sep  8 14:45:39 2048 GMT
Revoked Certificates:
    Serial Number: 1008
        Revocation Date: Apr 23 14:45:36 2021 GMT

Certificate Revocation List #2:
Version 1
Signature Algorithm: sha256WithRSAEncryption
Issuer: /C=FR/O=HAProxy Technologies/CN=Root CA
Last Update: Apr 23 14:30:44 2021 GMT
Next Update: Sep  8 14:30:44 2048 GMT
No Revoked Certificates.
```

<a id="entry-9-3-show-ssl-crt-list"></a>

**`show ssl crt-list [-n] [<filename>]`**

```haproxy
show ssl crt-list [-n] [<filename>]
```

Die Liste der crt-list-Dateien und Verzeichnisse anzeigen, die in der HAProxy-Konfiguration verwendet werden. Wird ein Dateiname angegeben, wird der Inhalt einer crt-list-Datei oder eines Verzeichnisses ausgegeben. Die Ausgabe kann anschließend als crt-list-Datei verwendet werden. Mit der Option '-n' lassen sich die Zeilennummern anzeigen. Dies ist zusammen mit der Option 'del ssl crt-list' hilfreich, wenn ein Eintrag mehrfach vorkommt. Die Ausgabe mit der Option '-n' ist mit dem crt-list-Format nicht kompatibel und kann von haproxy nicht geladen werden.

Beispiel:

```shell
echo "show ssl crt-list -n localhost.crt-list" | socat /tmp/sock1 -
# localhost.crt-list
common.pem:1 !not.test1.com *.test1.com !localhost
common.pem:2
ecdsa.pem:3 [verify none allow-0rtt ssl-min-ver TLSv1.0 ssl-max-ver TLSv1.3] localhost !www.test1.com
ecdsa.pem:4 [verify none allow-0rtt ssl-min-ver TLSv1.0 ssl-max-ver TLSv1.3]
```

<a id="entry-9-3-show-ssl-ech"></a>

**`show ssl ech [<name>]`**

```haproxy
show ssl ech [<name>]
```

Die Liste der im HAProxy-Prozess geladenen ECH-Schlüssel anzeigen.

Wird `<name>` angegeben, werden die Schlüssel für eine bestimmte bind-Zeile angezeigt. Das Format der bind-Zeile lautet `<frontend>`/@`<filename>`:`<linenum>` (Beispiel: frontend1/@haproxy.conf:19) oder `<frontend>`/`<name>`, wenn die bind-Zeile mit dem Schlüsselwort "name" benannt wurde.

Der Eintrag 'age' gibt die Zeit in Sekunden an, die seit dem Laden des Schlüssels in die bind-Zeile vergangen ist. Dieser Wert wird beim Starten, Neuladen oder Neustarten von HAProxy zurückgesetzt.

Eine OpenSSL-Version mit ECH-Unterstützung ist erforderlich, und HAProxy muss mit USE_ECH=1 kompiliert werden. Dieser Befehl wird nur auf einer CLI-Verbindung im experimentellen Modus unterstützt (siehe "experimental-mode on").

Siehe auch "ech" in [Abschnitt 5.1](/de/haproxy/bind-and-server-options/#section-5-1) des Konfigurationshandbuchs.

Beispiel:

```shell
$ echo "experimental-mode on; show ssl ech" | socat /tmp/haproxy.sock -
 ***
 frontend: frontend1

 bind: frontend1/@haproxy.conf:19

 ECH entry: 0 public_name: example.com age: 557 (has private key)
      [fe0d,94,example.com,[0020,0001,0001],c39285b774bf61c071864181c5292a012b30adaf767e39369a566af05573ef2b,00,00]

 ECH entry: 1 public_name: example.com age: 557 (has private key)
      [fe0d,ee,example.com,[0020,0001,0001],6572191131b5cabba819f8cacf2d2e06fa0b87b30d9b793644daba7b8866d511,00,00]

 bind: frontend1/@haproxy.conf:20

 ECH entry: 0 public_name: example.com age: 557 (has private key)
      [fe0d,94,example.com,[0020,0001,0001],c39285b774bf61c071864181c5292a012b30adaf767e39369a566af05573ef2b,00,00]

 ECH entry: 1 public_name: example.com age: 557 (has private key)
      [fe0d,ee,example.com,[0020,0001,0001],6572191131b5cabba819f8cacf2d2e06fa0b87b30d9b793644daba7b8866d511,00,00]

$ echo "experimental-mode on; show ssl ech frontend1/@haproxy.conf:19" | socat /tmp/haproxy.sock -
***
ECH for frontend1/@haproxy.conf:19
ECH entry: 0 public_name: example.com age: 786 (has private key)
      [fe0d,94,example.com,[0020,0001,0001],c39285b774bf61c071864181c5292a012b30adaf767e39369a566af05573ef2b,00,00]

ECH entry: 1 public_name: example.com age: 786 (has private key)
      [fe0d,ee,example.com,[0020,0001,0001],6572191131b5cabba819f8cacf2d2e06fa0b87b30d9b793644daba7b8866d511,00,00]
```

<a id="entry-9-3-show-ssl-jwt"></a>

**`show ssl jwt`**

```haproxy
show ssl jwt
```

Die Liste der Zertifikate anzeigen, die zur JWT-Validierung verwendet werden können. Siehe auch die Befehle "add ssl jwt" und "del ssl jwt". Weitere Informationen enthält die Zertifikatsoption "jwt".

Beispiel:

```shell
echo "show ssl jwt"  | socat /tmp/sock1 -
#filename
jwt.pem
```

<a id="entry-9-3-show-ssl-ocsp-response"></a>

**`show ssl ocsp-response [[text|base64] <id|path>]`**

```haproxy
show ssl ocsp-response [[text|base64] <id|path>]
```

Die IDs der OCSP-Baumeinträge für alle in HAProxy verwendeten OCSP-Antworten anzeigen, zusammen mit dem Pfad des zugehörigen Frontend-Zertifikats, dem Namen und Schlüssel-Hash des Ausstellers sowie der Seriennummer des Zertifikats, für das die OCSP-Antwort erstellt wurde. Wird eine gültige `<id>` oder der `<path>` eines gültigen Frontend-Zertifikats angegeben, wird der Inhalt der zugehörigen OCSP-Antwort angezeigt. Bei Angabe einer `<id>` kann das Ausgabeformat der Daten festgelegt werden. Die Standardoption 'text' zeigt detaillierte Informationen zur OCSP-Antwort wie bei einem Aufruf von "openssl ocsp -respin `<ocsp-response>` -text". Das Format 'base64' gibt den Inhalt einer OCSP-Antwort in base64 aus.

Beispiel:

```shell
$ echo "show ssl ocsp-response" | socat /var/run/haproxy.master -
# Certificate IDs
  Certificate ID key: 303b300906052b0e03021a050004148a83e0060faff709ca7e9b95522a2e81635fda0a0414f652b0e435d5ea923851508f0adbe92d85de007a0202100a
  Certificate path: /path_to_cert/foo.pem
    Certificate ID:
      Issuer Name Hash: 8A83E0060FAFF709CA7E9B95522A2E81635FDA0A
      Issuer Key Hash: F652B0E435D5EA923851508F0ADBE92D85DE007A
      Serial Number: 100A

$ echo "show ssl ocsp-response 303b300906052b0e03021a050004148a83e0060faff709ca7e9b95522a2e81635fda0a0414f652b0e435d5ea923851508f0adbe92d85de007a0202100a" | socat /var/run/haproxy.master -
OCSP Response Data:
  OCSP Response Status: successful (0x0)
  Response Type: Basic OCSP Response
  Version: 1 (0x0)
  Responder Id: C = FR, O = HAProxy Technologies, CN = ocsp.haproxy.com
  Produced At: May 27 15:43:38 2021 GMT
  Responses:
  Certificate ID:
    Hash Algorithm: sha1
    Issuer Name Hash: 8A83E0060FAFF709CA7E9B95522A2E81635FDA0A
    Issuer Key Hash: F652B0E435D5EA923851508F0ADBE92D85DE007A
    Serial Number: 100A
  Cert Status: good
  This Update: May 27 15:43:38 2021 GMT
  Next Update: Oct 12 15:43:38 2048 GMT
  [...]

$ echo "show ssl ocsp-response base64 /path_to_cert/foo.pem" | socat /var/run/haproxy.sock -
  MIIB8woBAKCCAewwggHoBgkrBgEFBQcwAQEEggHZMIIB1TCBvqE[...]
```

<a id="entry-9-3-show-ssl-ocsp-updates"></a>

**`show ssl ocsp-updates`**

```haproxy
show ssl ocsp-updates
```

Informationen zu den Einträgen anzeigen, die der OCSP-Aktualisierungsmechanismus betrifft. Der Befehl gibt eine Zeile je OCSP-Antwort aus. Sie enthält den erwarteten Aktualisierungszeitpunkt der Antwort, den Zeitpunkt der letzten erfolgreichen Aktualisierung sowie Zähler für erfolgreiche und fehlgeschlagene Aktualisierungen. Auch der Status der letzten Aktualisierung (erfolgreich oder nicht) wird numerisch und als Text angegeben. Eine vollständige Liste der möglichen Fehler folgt weiter unten. Die Zeilen werden aufsteigend nach dem Zeitpunkt 'Next Update' sortiert. Sie enthalten außerdem den Pfad des ersten Frontend-Zertifikats, das die OCSP-Antwort verwendet. Weitere Informationen zur automatischen OCSP-Aktualisierung enthalten der Befehl "show ssl ocsp-response" und die Option "ocsp-update".

Folgende Fehlercodes und Fehlermeldungen sind für die Aktualisierung möglich:

```text
  +----+-------------------------------------+
  | ID | Meldung                             |
  +----+-------------------------------------+
  |  0 | "Unknown"                           |
  |  1 | "Update successful"                 |
  |  2 | "HTTP error"                        |
  |  3 | "Missing \"ocsp-response\" header"  |
  |  4 | "OCSP response check failure"       |
  |  5 | "Error during insertion"            |
  +----+-------------------------------------+
```

Beispiel:

```shell
$ echo "show ssl ocsp-updates" | socat /tmp/haproxy.sock -
  OCSP Certid | Path | Next Update | Last Update | Successes | Failures | Last Update Status | Last Update Status (str)
      303b300906052b0e03021a050004148a83e0060faff709ca7e9b95522a2e81635fda0a0414f652b0e435d5ea923851508f0adbe92d85de007a02021015 | /path_to_cert/cert.pem | 30/Jan/2023:00:08:09 +0000 | - | 0 | 1 | 2 | HTTP error
      304b300906052b0e03021a0500041448dac9a0fb2bd32d4ff0de68d2f567b735f9b3c40414142eb317b75856cbae500940e61faf9d8b14c2c6021203e16a7aa01542f291237b454a627fdea9c1 | /path_to_cert/other_cert.pem | 30/Jan/2023:01:07:09 +0000 | 30/Jan/2023:00:07:09 +0000 | 1 | 0 | 1 | Update successful
```

<a id="entry-9-3-show-ssl-providers"></a>

**`show ssl providers`**

```haproxy
show ssl providers
```

Die Namen der Provider anzeigen, die OpenSSL bei der Initialisierung geladen hat. Das Laden von Providern kann über die OpenSSL-Konfigurationsdatei konfiguriert werden. Mit dieser Option lässt sich prüfen, ob die richtigen Provider geladen wurden. Dieser Befehl ist nur mit OpenSSL v3 verfügbar.

Beispiel:

```shell
$ echo "show ssl providers" | socat /var/run/haproxy.master -
Loaded providers:
    - fips
    - base
```

<a id="entry-9-3-show-ssl-sni"></a>

**`show ssl sni [-f <frontend>] [-A] [-t <offset>]`**

```haproxy
show ssl sni [-f <frontend>] [-A] [-t <offset>]
```

Alle für das angegebene Frontend konfigurierten SNIs ausgeben, oder für alle Frontends, wenn keines angegeben wird. So lässt sich erkennen, welche SNIs ein Frontend anbietet und ob eine SNI für dasselbe Frontend durch mehrere Zertifikate mehrfach definiert ist.

Die Option -A filtert die Liste so, dass nur Zertifikate angezeigt werden, deren notAfter-Datum überschritten ist, also nur abgelaufene Zertifikate.

Die Option -t akzeptiert einen Zeitversatz in Sekunden oder mit einer Zeiteinheit (s, m, h, d), der zur aktuellen Zeit addiert wird. Zusammen mit -A lässt sich damit prüfen, welche Zertifikate nach Anwendung des Zeitversatzes abgelaufen sind. Um beispielsweise zu prüfen, welche Zertifikate in 30d abgelaufen wären, genügt "show ssl sni -A -t 30d".

Die Spalten sind durch ein einzelnes &#92;t getrennt und lassen sich daher einfach parsen.

Die Spalte 'Frontend/Bind' zeigt den Frontendnamen, gefolgt von der Position der bind-Zeile in der Konfiguration (frontend/file:linenum).

Die Spalte 'SNI' zeigt die SNI; sie kann ein CN, ein SAN oder ein Filter aus einer crt-list sein. Für die Standardzertifikate einer bind-Zeile (entweder ausdrücklich mit 'default-crt' deklariert oder, wenn kein 'strict-sni' verwendet wird, implizit das erste Zertifikat der bind-Zeile) wird das Zeichen '\*' in der Spalte SNI angezeigt.

Die Spalte 'Negative Filter' enthält die Liste der negativen Filter, die einem Platzhaltermuster zugeordnet sind. Sie zeigt alle negativen Filter derselben crt-list-Zeile. Sind keine vorhanden, wird ein Bindestrich angezeigt.

Die Spalte 'Type' zeigt den Typ des Verschlüsselungsalgorithmus: "rsa", "ecdsa" oder "dsa".

Die Spalte 'Filename' kann entweder einen Dateinamen aus der Konfiguration oder einen in einem crt-store deklarierten Alias enthalten.

Die Spalten 'NotAfter' und 'NotBefore' werden direkt aus dem X509-Endzertifikat ausgelesen.

Beispiel:

```shell
$ echo "@1 show ssl sni -A -t 30d" | socat /var/run/haproxy-master.sock - | column -t -s $'\t'
# Frontend/Bind        SNI        Negative Filter  Type   Filename             NotAfter                  NotBefore
li1/haproxy.cfg:10021  *.ex.lan   !m1.ex.lan       rsa    example.lan.pem      Jun 13 13:37:21 2024 GMT  May 14 13:37:21 2024 GMT
li1/haproxy.cfg:10021  machine10  -                ecdsa  machine10.pem.ecdsa  Jun 13 13:37:21 2024 GMT  May 14 13:37:21 2024 GMT
li1/haproxy.cfg:10021  machine10  -                rsa    machine10.pem.rsa    Jun 13 13:37:21 2024 GMT  May 14 13:37:21 2024 GMT
li1/haproxy.cfg:10021  machine10  -                ecdsa  machine10.pem.ecdsa  Jun 13 13:37:21 2024 GMT  May 14 13:37:21 2024 GMT
li1/haproxy.cfg:10021  localhost  -                rsa    localhost.pem.rsa    Jun 13 13:37:11 2024 GMT  May 14 13:37:11 2024 GMT
li1/haproxy.cfg:10021  localhost  -                ecdsa  localhost.pem.ecdsa  Jun 13 13:37:10 2024 GMT  May 14 13:37:10 2024 GMT
li1/haproxy.cfg:10021  *          -                rsa    localhost.pem.rsa    Jun 13 13:37:11 2024 GMT  May 14 13:37:11 2024 GMT
```

<a id="entry-9-3-show-startup-logs"></a>

**`show startup-logs`**

```haproxy
show startup-logs
```

Alle beim Start des aktuellen haproxy-Prozesses ausgegebenen Meldungen ausgeben. Jeder startup-logs-Puffer gehört ausschließlich zu seinem jeweiligen haproxy-Worker.

Dieses Schlüsselwort ist auch auf der Master-CLI verfügbar und zeigt dort den letzten Start- oder Neuladeversuch an.

<a id="entry-9-3-show-table"></a>

**`show table`**

```haproxy
show table
```

Allgemeine Informationen zu allen bekannten Stick Tables ausgeben: ihren Namen (den Namen des Proxys, der sie enthält), ihren Typ (derzeit null, immer IP), ihre Größe als maximal mögliche Anzahl von Einträgen sowie die Anzahl der derzeit verwendeten Einträge.

Beispiel:

```shell
    $ echo "show table" | socat stdio /tmp/sock1
>>> # table: front_pub, type: ip, size:204800, used:171454
>>> # table: back_rdp, type: ip, size:204800, used:0
```

<a id="entry-9-3-show-table-2"></a>

**`show table <name> [ data.<type> <operator> <value> [data.<type> ...]] |`**

```haproxy
show table <name> [ data.<type> <operator> <value> [data.<type> ...]] |
                  [ key <key> ] | [ ptr <ptr> ]
```

Den Inhalt der Stick Table `<name>` ausgeben. In diesem Modus werden wie bei "show table" zunächst allgemeine Informationen zur Tabelle in einer Zeile ausgegeben, anschließend alle Einträge. Da dies sehr aufwendig sein kann, lässt sich mit einem Filter festlegen, welche Einträge angezeigt werden.

Bei Verwendung der Form "data." wird der Filter auf die gespeicherten Daten angewendet (siehe "stick-table" in Abschnitt 4.2). In `<type>` muss ein gespeicherter Datentyp angegeben werden. Dieser Datentyp muss in der Tabelle gespeichert sein, sonst wird ein Fehler gemeldet. Die Daten werden gemäß `<operator>` mit der 64-Bit-Ganzzahl `<value>` verglichen. Es gelten dieselben Operatoren wie bei ACLs:

    - eq: Einträge auswählen, deren Daten diesem Wert entsprechen
    - ne: Einträge auswählen, deren Daten diesem Wert nicht entsprechen
    - le: Einträge auswählen, deren Daten kleiner oder gleich diesem Wert sind
    - ge: Einträge auswählen, deren Daten größer oder gleich diesem Wert sind
    - lt: Einträge auswählen, deren Daten kleiner als dieser Wert sind
    - gt: Einträge auswählen, deren Daten größer als dieser Wert sind

In dieser Form können mehrere Datenfilter angegeben werden, bis zu einer beim Kompilieren festgelegten Höchstzahl (standardmäßig 4).

Bei Verwendung der key-Form wird der Eintrag `<key>` angezeigt. Der Schlüssel muss denselben Typ wie die Tabelle haben; zulässig sind derzeit nur IPv4, IPv6, Ganzzahlen und Zeichenketten.

Bei Verwendung der ptr-Form wird der Eintrag `<ptr>` angezeigt. `<ptr>` wird in der Form 0xffff geschrieben und muss der Adresse entsprechen, die ein vorheriger Befehl "show table" zurückgegeben hat. Die Auswahl eines Eintrags über seinen Zeiger kann hilfreich sein, wenn der Eintrag wegen eines leeren Schlüssels oder mit der CLI inkompatibler Zeichen nicht über den Schlüssel ausgewählt werden kann.

Wenn data.`<type>` ein Arraytyp ist, kann "[]" verwendet werden, um auf einen bestimmten Index im Array zuzugreifen, beispielsweise so: data.gpt[1]

Beispiel:

```shell
    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a4c: key=127.0.0.1 use=0 exp=3594729 gpc0=0 conn_rate(30000)=1  \
      bytes_out_rate(60000)=187
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191

    $ echo "show table http_proxy data.gpc0 gt 0" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191

    $ echo "show table http_proxy data.conn_rate gt 5" | \
        socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191

    $ echo "show table http_proxy key 127.0.0.2" | \
        socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191

    $ echo "show table http_proxy ptr 0x80e6a80" | \
        socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191
```

Bezieht sich das Datenkriterium auf einen dynamischen, zeitabhängigen Wert wie eine Byterate, wird der Wert bei der Auswertung des Eintrags dynamisch berechnet, um zu entscheiden, ob er ausgegeben werden muss. Ein solcher Filter kann daher eine Zeit lang zutreffen und anschließend nicht mehr, da die durchschnittliche Ereignisrate mit der Zeit sinkt.

Damit lassen sich Listen von IP-Adressen extrahieren, die den Dienst missbräuchlich nutzen, um sie zu überwachen oder sogar in einer Firewall zu sperren. Beispiel:

```shell
$ echo "show table http_proxy data.gpc0 gt 0" \
  | socat stdio /tmp/sock1 \
  | fgrep 'key=' | cut -d' ' -f2 | cut -d= -f2 > abusers-ip.txt
  ( oder | awk '/key/{ print a[split($2,a,"=")]; }' )
```

Wenn die Stick Table mit einem peers-Abschnitt synchronisiert wird, der Sharding unterstützt, wird für jeden Schlüssel die Shardnummer angezeigt (andernfalls wird '0' gemeldet). So lässt sich erkennen, welche Peers diesen Schlüssel erhalten. Beispiel:

```shell
$ echo "show table http_proxy" | socat stdio /tmp/sock1 | fgrep shard=
  0x7f23b0c822a8: key=10.0.0.2 use=0 exp=296398 shard=9 gpc0=0
  0x7f23a063f948: key=10.0.0.6 use=0 exp=296075 shard=12 gpc0=0
  0x7f23b03920b8: key=10.0.0.8 use=0 exp=296766 shard=1 gpc0=0
  0x7f23a43c09e8: key=10.0.0.12 use=0 exp=295368 shard=8 gpc0=0
```

<a id="entry-9-3-show-tasks"></a>

**`show tasks`**

```haproxy
show tasks
```

Die Anzahl der derzeit in der Ausführungswarteschlange befindlichen Tasks ausgeben, zusammen mit der Anzahl der Vorkommen je Funktion und ihrer durchschnittlichen Latenz, sofern bekannt (bei reinen Tasks mit aktiviertem Task-Profiling). Die Ausgabe ist eine Momentaufnahme zum Zeitpunkt ihrer Erstellung. Sie kann abhängig davon variieren, welche Tasks in diesem Moment noch in der Warteschlange stehen. Dies gilt besonders im Einzelthreadbetrieb, da E/A-Vorgänge die Warteschlange seltener wieder füllen können (außer wenn die Warteschlange voll ist). Dieser Befehl greift exklusiv auf den Prozess zu und kann bei einem stark ausgelasteten Prozess geringe, aber messbare Latenzen verursachen. Daher darf er von automatischen Überwachungswerkzeugen nicht übermäßig verwendet werden.

<a id="entry-9-3-show-threads"></a>

**`show threads`**

```haproxy
show threads
```

Einige interne Zustände und Strukturen je Thread ausgeben, die Entwicklern helfen können, ein Problem zu verstehen. Für eine lesbare Darstellung wird je Thread ein Block ausgegeben. Wenn haproxy mit USE_THREAD_DUMP=1 gebaut wurde, kommt ein erweiterter Ausgabemechanismus mit Threadsignalen zum Einsatz, damit jeder Thread nacheinander seinen eigenen Zustand ausgeben kann. Ohne diese Option zeigt der Thread, der den Befehl verarbeitet, alle eigenen Details an; die anderen Threads werden weniger detailliert dargestellt. Vor dem Thread, der den Befehl bearbeitet, steht ein Sternchen ('\*'). Vor Threads, die seit dem letzten Aufruf dieses Befehls keinen Fortschritt gemacht haben, kann außerdem eine schließende Winkelklammer ('\>') erscheinen. Dies weist auf einen Fehler im Code hin, der unbedingt gemeldet werden muss. Tritt dies zwischen zwei Threads auf, weist es gewöhnlich auf einen Deadlock hin. Ist ein Thread allein betroffen, handelt es sich um einen anderen Fehler, etwa eine beschädigte Liste. In jedem Fall ist der Prozess nicht mehr vollständig funktionsfähig und muss neu gestartet werden.

Das Ausgabeformat ist absichtlich nicht dokumentiert, damit es sich bei neuem Bedarf leicht weiterentwickeln kann, ohne irgendeine Form von Abwärtskompatibilität gewährleisten zu müssen. Wie bei "show activity" sind die Werte ohne den zugehörigen Code nicht aussagekräftig.

<a id="entry-9-3-show-tls-keys"></a>

**`show tls-keys [id|*]`**

```haproxy
show tls-keys [id|*]
```

Alle geladenen Referenzen auf TLS-Ticketschlüssel ausgeben. Angezeigt werden die Referenz-ID des TLS-Ticketschlüssels und die Datei, aus der die Schlüssel geladen wurden. Beide können verwendet werden, um die TLS-Schlüssel mit "set ssl tls-key" zu aktualisieren. Wird eine ID als Parameter angegeben, werden die Tickets ausgegeben; mit \* werden alle Schlüssel aller Referenzen ausgegeben.

<a id="entry-9-3-show-schema-json"></a>

**`show schema json`**

```haproxy
show schema json
```

Das Schema ausgeben, das für die Ausgabe von "show info json" und "show stat json" verwendet wird.

Die Ausgabe enthält keine zusätzlichen Leerraumzeichen, um ihr Volumen zu verringern. Für das Lesen durch Menschen kann es hilfreich sein, die Ausgabe durch ein Werkzeug zur lesbaren Formatierung zu leiten. Beispiel:

\$ echo "show schema json" \| socat /var/run/haproxy.sock stdio \| &#92;
python -m json.tool

Das Schema folgt "JSON Schema" (json-schema.org). Entsprechende Prüfwerkzeuge können daher die Ausgabe von "show info json" und "show stat json" anhand des Schemas überprüfen.

<a id="entry-9-3-show-trace"></a>

**`show trace [<source>]`**

```haproxy
show trace [<source>]
```

Den aktuellen Tracestatus anzeigen. Für jede Quelle wird eine Zeile mit einem Status aus einem einzelnen Zeichen ausgegeben, der angibt, ob der Trace gestoppt ist, wartet oder läuft. Angezeigt werden das vom Trace verwendete Ausgabeziel (oder "none", wenn keines festgelegt wurde) und die Anzahl der dort verworfenen Ereignisse, gefolgt von einer kurzen Beschreibung der Quelle. Wird ein Quellenname angegeben, erscheint eine detaillierte Liste aller von dieser Quelle unterstützten Ereignisse sowie ihres Status für jede Aktion (report, start, pause, stop): "+" bedeutet aktiviert, "-" bedeutet deaktiviert. Alle diese Ereignisse sind unabhängig voneinander. Ein Ereignis kann daher einen Start auslösen, ohne gemeldet zu werden, und umgekehrt.

<a id="entry-9-3-show-version"></a>

**`show version`**

```haproxy
show version
```

Die Version des aktuellen HAProxy-Prozesses anzeigen. Dieser Befehl ist auf der Master- und der Worker-CLI verfügbar. Beispiel:

```shell
$ echo "show version" | socat /var/run/haproxy.sock stdio
2.4.9

$ echo "show version" | socat /var/run/haproxy-master.sock stdio
2.5.0
```

<a id="entry-9-3-shutdown-frontend"></a>

**`shutdown frontend <frontend>`**

```haproxy
shutdown frontend <frontend>
```

Das angegebene Frontend vollständig löschen. Alle Ports, an die es gebunden war, werden freigegeben. Nach diesem Vorgang lässt sich das Frontend nicht mehr aktivieren. Dies ist für Umgebungen vorgesehen, in denen das Anhalten eines Proxys ausgeschlossen ist, eine fehlerhafte Proxykonfiguration aber korrigiert werden muss. Auf diese Weise kann der Port freigegeben und in einem anderen Prozess gebunden werden, um den Betrieb wiederherzustellen. Nach seiner Beendigung erscheint das Frontend überhaupt nicht mehr auf der Statistikseite.

Das Frontend kann entweder durch seinen Namen oder durch seine numerische ID mit vorangestelltem Rautezeichen ('#') angegeben werden.

Dieser Befehl ist zugriffsbeschränkt und kann nur über Sockets ausgeführt werden, die für die Berechtigungsstufe "admin" konfiguriert sind.

<a id="entry-9-3-shutdown-session"></a>

**`shutdown session <id>`**

```haproxy
shutdown session <id>
```

Den Stream mit der angegebenen Streamkennung sofort beenden. Diese Kennung steht als erstes Feld am Zeilenanfang der Ausgaben von "show sess" (sie entspricht dem Zeiger auf den Stream). Damit lässt sich ein lang laufender Stream beenden, ohne auf eine Zeitüberschreitung zu warten, oder eine endlose Übertragung abbrechen. Auf diese Weise beendete Streams werden in den Protokollen mit einem 'K'-Flag gekennzeichnet.

<a id="entry-9-3-shutdown-sessions-server"></a>

**`shutdown sessions server <backend>/<server>`**

```haproxy
shutdown sessions server <backend>/<server>
```

Alle dem angegebenen Server zugeordneten Streams sofort beenden. Damit lassen sich beispielsweise lang laufende Streams beenden, nachdem ein Server in den Wartungsmodus versetzt wurde. Auf diese Weise beendete Streams werden in den Protokollen mit einem 'K'-Flag gekennzeichnet.

Backend-Verbindungen bleiben im Leerlauf, außer wenn sich der Server bereits im Wartungsmodus befindet. In diesem Fall werden sie sofort zur Löschung vorgemerkt.

<a id="entry-9-3-trace"></a>

**`trace`**

```haproxy
trace
```

Der Befehl "trace" ohne weitere Argumente listet die Tracequellen, ihren aktuellen Status und ihre kurzen Beschreibungen auf. Er dient nur als Menü für den Einstieg in die nächsten Ebenen; siehe die weiteren "trace"-Befehle unten.

<a id="entry-9-3-trace-0"></a>

**`trace 0`**

```haproxy
trace 0
```

Alle Traces sofort stoppen. Dies ist als schnelle Möglichkeit zum Beenden einer Sitzung zur Fehlersuche gedacht oder als Notfallmaßnahme, wenn komplexe Traces für mehrere Quellen aktiviert wurden und den Dienst beeinträchtigen.

<a id="entry-9-3-trace-2"></a>

**`trace <source> [<args...>]`**

```haproxy
trace <source> [<args...>]
```

Traces für die Quelle `<source>` konfigurieren. Ohne Argument werden alle von dieser Quelle unterstützten Unterbefehle aufgelistet. Mehrere Unterbefehle können verkettet werden. Folgende Unterbefehle werden unterstützt:

event [ [+\|-\|!]`<name>` ] Ohne Argument werden alle Ereignisse aufgelistet, die die angegebene Quelle unterstützt. Ihnen wird ein "-" vorangestellt, wenn sie deaktiviert sind, oder ein "+", wenn sie aktiviert sind. Zu beachten ist, dass ein einzelner Trace mit mehreren Ereignissen gekennzeichnet sein kann. Sobald eines der aktivierten Ereignisse mit einem der Ereignisse am Trace übereinstimmt, wird das Ereignis an das Trace-Subsystem übergeben. Beispielsweise kann der Empfang eines HTTP/2-Frames vom Typ HEADERS ein Frameereignis und ein Streamereignis auslösen, da der Frame einen neuen Stream erzeugt. Ist entweder das Frameereignis oder das Streamereignis für diese Quelle aktiviert, wird der Frame an das Trace-Framework übergeben.

    Mit einem Argument lässt sich der Zustand jedes Ereignisses umschalten,
    um es einzeln zu aktivieren oder zu deaktivieren. Zwei spezielle Schlüsselwörter
    werden unterstützt: "none" passt auf kein Ereignis und deaktiviert alle
    Ereignisse gleichzeitig; "any" passt auf alle Ereignisse und aktiviert sie
    gleichzeitig. Andere Ereignisse hängen von der Ereignisquelle ab. Ein Ereignis
    lässt sich durch Angabe seines Namens aktivieren, optional mit einem
    vorangestellten '+' zur besseren Lesbarkeit. Zur Deaktivierung wird sein
    Name mit einem vorangestellten '-' oder '!' angegeben.

    Eine Tracequelle lässt sich vollständig deaktivieren, indem "event none"
    angegeben wird. Die Quelle wird dann sofort vollständig ignoriert.

follow `<other_source>` Damit kann die Quelle `<source>` auch dann Traces ausgeben, wenn die andere Quelle `<other_source>` auf ein Kriterium fixiert ist und dasselbe Kriterium auch auf die aktuelle Quelle zutrifft. Ist beispielsweise eine Quelle auf eine Sitzung fixiert, bewirkt das Folgen dieser Quelle von einer anderen Quelle aus, dass die andere Quelle Traces für alle Ereignisse dieser Sitzung ausgibt. Damit lassen sich in gewissem Umfang Backend-Anfragen zusammen mit den zugehörigen Frontend-Verbindungen verfolgen. Die Quelle "session" erleichtert dies mit den Ereignissen "new" und "end", die zur Verarbeitung der Fixierung verwendet werden können. Die Traces der Quelle `<source>` müssen in diesem Fall nicht aktiviert sein; ihr Tracestatus wird ebenfalls nicht beeinflusst. Einige Ereignisse können jedoch fehlen, wenn sie keine Informationen enthalten, die eine Zuordnung zum verfolgten Element ermöglichen. Mit diesem Befehl kann auch die Metaquelle "all" verwendet werden: Dann folgen alle Quellen `<other_source>`.

Beispiel:

```text
trace h1 lock session start sess_new pause sess_end follow session
```

level [`<level>`] Ohne Argument werden alle Tracestufen dieser Quelle aufgelistet; die aktuelle Stufe wird durch ein vorangestelltes Sternchen ('\*') gekennzeichnet. Mit einem Argument wird die Tracestufe auf die angegebene Stufe geändert. Detailstufen sind eine Form von Filtern, die vor der Meldung der Ereignisse angewendet werden. Diese Filter schließen Ereignisse je nach ihrer Bedeutung gezielt ein oder aus. Ein Entwickler muss beispielsweise möglicherweise genau wissen, an welcher Stelle im Code ein HTTP-Header als ungültig angesehen wurde, während seine Gültigkeit für den Endbenutzer vielleicht überhaupt nicht relevant ist. Derzeit gibt es 5 verschiedene Tracestufen:

```text
user       Meldet Informationen, die sich für einen normalen haproxy-Benutzer
           eignen, der seinen Datenverkehr beobachten möchte. Typischerweise
           werden einige HTTP-Anfragen und -Antworten ohne viele Details
           ausgegeben. Die meisten Quellen verwenden diese Stufe als
           Standard, um den Betrieb zu erleichtern.

proto      Zeigt zusätzlich zu den Informationen der Stufe "user" auch
           Aktualisierungen auf Protokollebene an. Dies können beispielsweise
           Frame-Typen oder HTTP-Header nach der Dekodierung sein.

state      Zeigt zusätzlich zu den Informationen der Stufe "proto" auch
           Zustandsübergänge (oder fehlgeschlagene Übergänge) in Parsern an.
           Damit werden Versuche sichtbar, eine Operation auszuführen,
           während die Stufe "proto" nur die endgültige Operation zeigt.

data       Zeigt zusätzlich zu den Informationen der Stufe "state" auch
           Datenübertragungen zwischen den verschiedenen Schichten an.

developer  Meldet alle verfügbaren Informationen. Dazu können detaillierte
           Angaben wie "breaking out of this loop" gehören, die nur für
           Entwickler relevant sind, die einen im praktischen Einsatz
           nur gelegentlich auftretenden Fehler verstehen möchten.
           Funktionsnamen werden nur auf dieser Stufe ausgegeben.
```

    Es wird dringend empfohlen, stets nur die Stufe "user" zu verwenden und
    nur auf Anweisung eines Entwicklers zu anderen Stufen zu wechseln. Außerdem
    ist es sinnvoll, vor dem Wechsel zu höheren Stufen zunächst die Ereignisse
    zu konfigurieren, um die Ausgabe vieler Zeilen ohne angewendeten Filter zu
    vermeiden. Mit diesem Befehl kann auch die Metaquelle "all" verwendet werden:
    Dann wird die Stufe gleichzeitig auf alle vorhandenen Quellen angewendet.

lock [criterion] Ohne Argument werden alle Kriterien aufgelistet, die diese Quelle für die Fixierung unterstützt. Die aktuelle Auswahl wird durch ein vorangestelltes Sternchen ('\*') angezeigt. Fixierung bedeutet, dass sich die Quelle auf das erste passende Ereignis konzentriert und nur an dem Kriterium festhält, das dieses Ereignis ausgelöst hat; alles andere wird ignoriert, bis der Trace stoppt. So lässt sich beispielsweise ein Trace für eine einzelne Verbindung oder einen einzelnen Stream erfassen. Einige Traces unterstützen die folgenden Kriterien, jedoch nicht unbedingt alle, da manche Kriterien der Quelle möglicherweise nicht zur Verfügung stehen:

```text
backend      Auf das Backend beschränken, das den Trace gestartet hat
connection   Auf die Verbindung beschränken, die den Trace gestartet hat
frontend     Auf das Frontend beschränken, das den Trace gestartet hat
listener     Auf den Listener beschränken, der den Trace gestartet hat
nothing      Auf nichts beschränken
server       Auf den Server beschränken, der den Trace gestartet hat
session      Auf die Sitzung beschränken, die den Trace gestartet hat
thread       Auf den Thread beschränken, der den Trace gestartet hat
```

    Zusätzlich kann jede Quelle bis zu 4 spezifische Kriterien bereitstellen,
    etwa interne Zustände oder Verbindungs-IDs. Bei HTTP/2 lässt sich beispielsweise
    auf den H2-Stream fixieren und andere Streams ignorieren, sobald ein Trace startet.

    Wird ein Kriterium als Argument übergeben, wird es anstelle der anderen
    verwendet. Jede bestehende Verfolgung wird sofort beendet, damit sie mit dem
    neuen Kriterium neu starten kann. Alle Quellen unterstützen das spezielle
    Schlüsselwort "nothing", um die Verfolgung dauerhaft zu deaktivieren.

{ pause \| start \| stop } [ [+\|-\|!]event] Ohne Argument werden die Ereignisse aufgelistet, die für das automatische Pausieren, Starten oder Stoppen eines Traces dieser Quelle aktiviert sind. Diese Ereignisse hängen von der jeweiligen Tracequelle ab. Mit einem Argument wird das Ereignis entweder für die angegebene Aktion aktiviert (optional mit vorangestelltem '+') oder deaktiviert (mit vorangestelltem '-' oder '!'). Das spezielle Schlüsselwort "now" ist kein Ereignis, sondern fordert die sofortige Ausführung der Aktion an. Die Schlüsselwörter "none" und "any" werden wie bei "trace event" unterstützt.

    Die 3 unterstützten Aktionen sind "pause", "start" und "stop". Die Aktion
    "pause" zählt Ereignisse auf, die einen laufenden Trace anhalten und auf ein
    neues Startereignis warten lassen, um ihn erneut zu starten. Die Aktion
    "start" zählt Ereignisse auf, die den Trace in den Wartemodus versetzen, bis
    eines der Startereignisse auftritt. Die Aktion "stop" zählt Ereignisse auf,
    die den Trace endgültig stoppen, bis er wieder manuell aktiviert wird. In der
    Praxis ist es sinnvoll, einen Trace mit "start now" manuell zu starten, ohne
    sich um Ereignisse zu kümmern, und ihn mit "stop now" zu stoppen. Um subtilere
    Ereignisfolgen zu erfassen, kann "start" auf ein gewöhnliches Ereignis gesetzt
    werden (etwa den Empfang einer HTTP-Anfrage) und "stop" auf ein sehr seltenes
    Ereignis wie die Ausgabe eines bestimmten Fehlers. Dadurch entsprechen die
    zuletzt erfassten Ereignisse den gewünschten Kriterien. Das Pausenereignis
    ist hilfreich, um das Ende einer Folge zu erkennen, die Fixierung aufzuheben
    und auf eine weitere Gelegenheit zur Erfassung zu warten. In diesem Fall kann
    es sinnvoll sein, die Fixierung zu aktivieren, um nur ein bestimmtes Kriterium
    (etwa einen Stream) zu verfolgen. "start" wird auf alles gesetzt, was dieses
    Kriterium beginnen lässt (etwa alle Ereignisse, die einen Stream erzeugen),
    "stop" auf die erwartete Anomalie und "pause" auf alles, was dieses Kriterium
    beendet (etwa jedes Ereignis zum Streamende). Das Traceprotokoll enthält dann
    vollständige Folgen fehlerfreier Serien, die jeweils ein einzelnes Objekt
    betreffen, bis zur letzten Folge mit allem vom Beginn bis zur Anomalie.

sink [`<sink>`] Ohne Argument werden alle für diese Quelle verfügbaren Ereignisausgabeziele aufgelistet; das aktuell konfigurierte wird durch ein vorangestelltes Sternchen ('\*') gekennzeichnet. Das Ausgabeziel "none" ist immer verfügbar und bedeutet, dass alle Ereignisse einfach verworfen werden. Ihre Verarbeitung wird jedoch nicht ignoriert (beispielsweise findet eine Fixierung statt). Andere Ausgabeziele stehen abhängig von Konfiguration und Build-Optionen zur Verfügung; typischerweise sind "stdout" und "stderr" im Debugmodus nutzbar, und Ringpuffer im Speicher sollten ebenfalls verfügbar sein. Wird ein Name angegeben, ändert sich das Ausgabeziel für die angegebene Quelle sofort. Ein Wechsel des Ausgabeziels ändert die Ereignisse nicht. Im schlimmsten Fall gehen einige verloren, wenn ein ungültiges Ausgabeziel (oder "none") verwendet wird; die Vorgänge werden jedoch an einem anderen Ziel fortgesetzt. Mit diesem Befehl kann auch die Metaquelle "all" verwendet werden: Dann wird das Ausgabeziel gleichzeitig auf alle vorhandenen Quellen angewendet.

verbosity [`<level>`] Ohne Argument werden alle Stufen des Detailgrads dieser Quelle aufgelistet; die aktuelle wird durch ein vorangestelltes Sternchen ('\*') gekennzeichnet. Mit einem Argument wird der Detailgrad auf die angegebene Stufe geändert.

    Die Stufen des Detailgrads geben an, wie weit der Tracedekoder gehen sollte,
    um detaillierte Informationen bereitzustellen. Dies hängt von der Tracequelle
    ab, da einige Quellen nicht einmal einen spezifischen Dekoder bereitstellen.
    Die Stufe "quiet" ist immer verfügbar und deaktiviert jede Dekodierung. Sie
    kann helfen, zunächst festzustellen, was geschieht, bevor die Details
    untersucht werden, da sie Leistung und Tracegröße nur sehr wenig beeinflusst.
    Deklariert eine Quelle keine Stufen des Detailgrads, steht die Stufe "default"
    zur Verfügung. Sie bewirkt den Aufruf eines Dekoders, wenn dies in den Traces
    angegeben ist. Dies ist eine opportunistische Dekodierung. Deklariert
    eine Quelle Stufen des Detailgrads, werden diese mit einer Beschreibung ihrer
    Bedeutung aufgelistet. In diesem Fall arbeitet der von der Quelle
    bereitgestellte Tracedekoder anhand der am Tracepunkt verfügbaren Informationen
    so genau wie möglich. Standardmäßig ist die erste Stufe oberhalb von "quiet"
    eingestellt.

<a id="entry-9-3-update-ssl-ocsp-response"></a>

**`update ssl ocsp-response <certfile>`**

```haproxy
update ssl ocsp-response <certfile>
```

Eine OCSP-Anfrage für die angegebene `<certfile>` erstellen und an den OCSP-Responder senden, dessen URI im Abschnitt "Authority Information Access" des Zertifikats angegeben sein sollte. Nur die erste URI wird berücksichtigt. Die als Antwort erwartete OCSP-Antwort wird anschließend geprüft und in den lokalen OCSP-Antwortbaum eingefügt. Dieser Befehl funktioniert nur für Zertifikate, für die bereits eine OCSP-Antwort gespeichert war, entweder bei der Initialisierung bereitgestellt oder zuvor über die Befehle "set ssl cert" oder "set ssl ocsp-response" gesetzt. Ist die empfangene OCSP-Antwort gültig und wurde sie korrekt in den lokalen Baum eingefügt, wird ihr Inhalt auf der Standardausgabe angezeigt. Das Format entspricht dem unter "show ssl ocsp-response" beschriebenen.

<a id="entry-9-3-wait"></a>

**`wait { -h | <delay> } [<condition> [<args>...]]`**

```haproxy
wait { -h | <delay> } [<condition> [<args>...]]
```

In der einfachsten Form ohne Bedingung wartet der Befehl lediglich die angegebene Zeit, bevor er fortfährt. Damit lassen sich Metriken über ein bestimmtes Zeitintervall erfassen.

Mit einer Bedingung und optionalen Argumenten wartet der Befehl, bis die angegebene Bedingung erfüllt ist, endgültig fehlschlägt oder während der gesamten Dauer `<delay>` unerfüllt bleibt. Folgende Bedingungen werden unterstützt:

- be-removable `<proxy>`: Wartet, bis das angegebene Proxybackend mit dem Befehl "del backend" entfernt werden kann. Manche Zustände werden niemals akzeptiert (beispielsweise ein noch veröffentlichtes Backend oder eines mit Servern darin). Sie führen zu einer spezifischen Fehlermeldung, die angibt, welche Bedingung nicht erfüllt ist. Ist vor Ablauf der Wartezeit alles OK, wird Erfolg zurückgegeben und der Vorgang beendet.

- srv-removable `<proxy>`/`<server>`: Wartet, bis der angegebene Server mit dem Befehl "del server" entfernt werden kann, also im Wartungsmodus ist und keine Verbindungen mehr hat (weder aktive noch ungenutzte). Manche Zustände werden niemals akzeptiert (beispielsweise ein Server außerhalb des Wartungsmodus). Sie führen zu einer spezifischen Fehlermeldung, die angibt, welche Bedingung nicht erfüllt ist. Der Server kann sogar parallel bereits entfernt worden sein und nicht mehr existieren. Ist vor Ablauf der Wartezeit alles OK, wird Erfolg zurückgegeben und der Vorgang beendet.

Standardmäßig wird die Wartezeit in Millisekunden angegeben. Andere Einheiten werden ebenfalls akzeptiert, wenn sie mit den üblichen Zeiteinheiten (us, ms, s, m, h, d) als Suffix angegeben werden. Bei Verwendung mit dem Werkzeug 'socat' muss dessen Zeitüberschreitung zum Schließen verlängert werden, damit sie die Wartezeit abdeckt. Mit "-h" als erstem oder zweitem Argument werden Hinweise zur Verwendung des Befehls angezeigt. Beispiel:

```shell
$ socat -t20 /path/to/socket - <<< "show activity; wait 10s; show activity"

$ socat -t5 /path/to/socket - <<< "
    disable server px/srv1
    shutdown sessions server px/srv1
    wait 2s srv-removable px/srv1
    del server px/srv1"
```

## 9.4. Master-CLI {#section-9-4}

Die Master-CLI ist ein Socket, der im Master-Worker-Modus an den Masterprozess gebunden ist. Diese CLI ermöglicht den Zugriff auf die Unix-Socket-Befehle aller laufenden oder sich beendenden Prozesse und eine grundlegende Überwachung dieser Prozesse.

Die Master-CLI lässt sich ausschließlich über die Programmargumente von haproxy mit der Option -S konfigurieren. Diese Option akzeptiert auch kommagetrennte bind-Optionen.

Beispiel:

```haproxy
# haproxy -W -S 127.0.0.1:1234 -f test1.cfg
# haproxy -Ws -S /tmp/master-socket,uid,1000,gid,1000,mode,600 -f test1.cfg
# haproxy -W -S /tmp/master-socket,level,user -f test1.cfg
```

### 9.4.1. Befehle der Master-CLI {#section-9-4-1}

<a id="entry-9-4-1-entry"></a>

**`@<[!]pid>`**

```haproxy
@<[!]pid>
```

Die Master-CLI verwendet eine besondere Präfixnotation, um auf die verschiedenen Prozesse zuzugreifen. Diese Notation ist leicht erkennbar, da sie mit einem @ beginnt.

Auf ein @-Präfix kann eine relative Prozessnummer oder ein Ausrufezeichen mit einer PID folgen (beispielsweise @1 oder @!1271). Ein einzelnes @ kann den Master angeben. Sich beendende Prozesse sind nur über die PID erreichbar, da relative Prozessnummern nur für die aktuellen Prozesse verwendbar sind.

Dieses Präfix kann einem Befehl vorangestellt werden, um anzugeben, dass dieser und nur dieser Befehl an den bezeichneten Prozess gesendet wird. In diesem Fall endet der vollständige Befehl wie jeder reguläre Befehl am Zeilenende oder an einem Semikolon.

Fehler: Das Protokoll sockpair@ zur Kommunikation zwischen Master und Worker ist auf macOS bekanntermaßen unzuverlässig, da die macOS-Implementierung von sendmsg(2) fehlerhaft ist. Ein Befehl kann daher ohne Antwort bleiben.

Beispiele:

```shell
$ socat /var/run/haproxy-master.sock readline
prompt
master> @1 show info; @2 show info
[...]
Process_num: 1
Pid: 1271
[...]
Process_num: 2
Pid: 1272
[...]
master>

$ echo '@!1271 show info; @!1272 show info' | socat /var/run/haproxy-master.sock -
[...]
```

Das Präfix kann auch als eigenständiger Befehl verwendet werden, um den Standardausführungskontext auf den bezeichneten Prozess umzuschalten. Alle nachfolgenden Befehle werden dann in diesem Prozess ausgeführt, bis ein neuer '@'-Befehl den Ausführungskontext erneut ändert.

Beispiele:

```shell
$ socat /var/run/haproxy-master.sock readline
prompt
master> @1
1271> show info
[...]
1271> show stat
[...]
1271> @
master>

$ echo '@1; show info; show stat; @2; show info; show stat' | socat /var/run/haproxy-master.sock -
[...]
```

Hinweis zu Einschränkungen: Einige wenige Befehle ändern den Zustand einer CLI-Sitzung (beispielsweise "set anon", "set timeout") und verhalten sich bei einem Aufruf über die Master-CLI möglicherweise nicht genau gleich, da die Befehle einzeln in jeweils einer eigenen CLI-Sitzung gesendet werden. Ebenso überwachen einige wenige Befehle ("show events", "wait") die CLI aktiv auf Eingaben oder das Schließen der Verbindung und werden sofort unterbrochen, wenn die CLI geschlossen wird. Diese Befehle funktionieren über die Master-CLI nicht wie erwartet, da die Befehlseingabe nach jedem Befehl geschlossen wird. Für solche seltenen Fälle kann die unten beschriebene Variante "@@" besser geeignet sein.

<a id="entry-9-4-1-entry-2"></a>

**`@@<[!]pid> [command...]`**

```haproxy
@@<[!]pid> [command...]
```

Dieses Präfix beziehungsweise dieser Befehl ähnelt dem oben dokumentierten Präfix "@", wechselt jedoch in den Workerprozess, übergibt ihm die gesamte Befehlszeile unverändert und bleibt dort, bis der Befehl endet. Auch Semikolons werden übergeben, sodass eine vollständige verkettete Befehlsfolge in einem Workerprozess ausgeführt werden kann. Die Verbindung zum Worker bleibt offen, bis die Befehlsliste abgeschlossen ist. Alle nach den Befehlen gesendeten Daten werden an die CLI des Workerprozesses weitergeleitet. Sie können von den ausgeführten Befehlen verarbeitet werden und gehen für die CLI des Masterprozesses verloren. So entsteht eine tatsächlich bidirektionale Verbindung mit dem Workerprozess. Bei Verwendung solcher Befehle muss daher sehr sorgfältig auf deren Abschluss gewartet werden, bevor neue Befehle an die Master-CLI gesendet werden.

Statt einen einzelnen Befehl auszuführen, kann auch eine vollständig interaktive Sitzung auf dem Workerprozess geöffnet werden, indem kein Befehl angegeben wird (also "@@1" in einer eigenen Zeile). Diese Sitzung lässt sich entweder durch Schließen der Verbindung oder durch Verlassen der CLI des Workerprozesses (mit dem Befehl "quit") beenden. In diesem Fall wird der Eingabeaufforderungsmodus des Mastersockets (interactive, prompt, timed) an den Workerprozess weitergegeben.

Fehler: Das Protokoll sockpair@ zur Kommunikation zwischen Master und Worker ist auf macOS bekanntermaßen unzuverlässig, da die macOS-Implementierung von sendmsg(2) fehlerhaft ist. Ein Befehl kann daher ohne Antwort bleiben.

Beispiele:

```shell
# gracefully close connections and delete a server once idle (wait max 10s)
$ socat -t 11 /var/run/haproxy-master.sock - <<< \
   "@@1 disable server app2/srv36; \
   wait 10000 srv-removable app2/srv36; \
   del server app2/srv36"

# forcefully close connections and quickly delete a server
$ socat /var/run/haproxy-master.sock - <<< \
   "@@1 disable server app2/srv36; \
   shutdown sessions server app2/srv36; \
   wait 100 srv-removable app2/srv36; \
   del server app2/srv36"

# show messages arriving to this ring in real time ("tail -f" equivalent)
$ (echo "show events buf0 -w"; read) | socat /var/run/haproxy-master.sock -
```

<a id="entry-9-4-1-expert-mode"></a>

**`expert-mode [on|off]`**

```haproxy
expert-mode [on|off]
```

Dieser Befehl aktiviert "expert-mode" für jeden Worker, auf den über die Master-CLI zugegriffen wird. Zusammen mit "mcli-debug-mode" aktiviert er den Befehl auch auf dem Master. Er zeigt das Flag "e" in der Eingabeaufforderung der Master-CLI an.

Siehe auch "expert-mode" in [Abschnitt 9.3](/de/haproxy/statistics-and-monitoring/#section-9-3) und "mcli-debug-mode" in 9.4.1.

<a id="entry-9-4-1-experimental-mode"></a>

**`experimental-mode [on|off]`**

```haproxy
experimental-mode [on|off]
```

Dieser Befehl aktiviert "experimental-mode" für jeden Worker, auf den über die Master-CLI zugegriffen wird. Zusammen mit "mcli-debug-mode" aktiviert er den Befehl auch auf dem Master. Er zeigt das Flag "x" in der Eingabeaufforderung der Master-CLI an.

Siehe auch "experimental-mode" in [Abschnitt 9.3](/de/haproxy/statistics-and-monitoring/#section-9-3) und "mcli-debug-mode" in 9.4.1.

<a id="entry-9-4-1-hard-reload"></a>

**`hard-reload`**

```haproxy
hard-reload
```

Dieser Befehl verhält sich wie der Befehl "reload" über die Master-CLI, beendet den vorherigen Prozess jedoch sofort (-st), statt ihn geordnet anzuhalten (-sf). Der vorherige Prozess wartet also vor dem Beenden auf keinen Abschluss, sodass alle Verbindungen geschlossen werden.

Siehe auch den Befehl "reload".

<a id="entry-9-4-1-mcli-debug-mode"></a>

**`mcli-debug-mode [on|off]`**

```haproxy
mcli-debug-mode [on|off]
```

Dieses Schlüsselwort ermöglicht einen besonderen Modus der Master-CLI, der dort alle für eine Worker-CLI vorgesehenen Schlüsselwörter aktiviert und so die Fehlersuche im Masterprozess ermöglicht. Nach der Aktivierung lassen sich die neu verfügbaren Schlüsselwörter mit "help" auflisten. Zusammen mit "experimental-mode" oder "expert-mode" werden noch weitere Schlüsselwörter aktiviert. Das Flag "d" wird in der Eingabeaufforderung der Master-CLI angezeigt.

<a id="entry-9-4-1-prompt"></a>

**`prompt`**

```haproxy
prompt
```

Wenn die Eingabeaufforderung aktiviert ist (über den Befehl "prompt"), zeigt sie den Kontext an, in dem die CLI arbeitet. Der Master wird durch die Zeichenkette "master" gekennzeichnet, andere Prozesse durch ihre PID. Ist das letzte Neuladen fehlgeschlagen, wird die Eingabeaufforderung des Masters zu "master[ReloadFailed]\>" geändert. Dadurch wird sichtbar, dass der Prozess weiterhin mit der vorherigen Konfiguration läuft und die neue Konfiguration nicht betriebsbereit ist.

Die Eingabeaufforderung der Master-CLI kann mehrere Flags anzeigen, die die aktivierten Modi kennzeichnen: "d" für mcli-debug-mode, "e" für expert-mode und "x" für experimental-mode.

Beispiel:

```shell
$ socat /var/run/haproxy-master.sock -
prompt
master> expert-mode on
master(e)> experimental-mode on
master(xe)> mcli-debug-mode on
master(xed)> @1
95191(xed)>
```

<a id="entry-9-4-1-reload"></a>

**`reload`**

```haproxy
reload
```

Der HAProxy-Masterprozess kann auch mit dem Befehl "reload" neu geladen werden. Dies entspricht einem `kill -USR2` auf den Masterprozess, sofern der Benutzer mindestens über die Berechtigungsstufe "operator" oder "admin" verfügt.

Dieser Befehl ermöglicht ein synchrones Neuladen und gibt nach dessen Ausführung den Status zurück. Wenn die Ausgabe mit einem Werkzeug geparst wird, ist die Zeitüberschreitung zu beachten: Der Status wird erst zurückgegeben, nachdem die Konfiguration geparst und der neue Worker durch fork erzeugt wurde. Der Befehl "socat" verwendet standardmäßig eine Zeitüberschreitung von 0.5s. Dauert das Neuladen zu lange, beendet er sich daher, bevor die Meldung angezeigt wird. "ncat" hat standardmäßig keine Zeitüberschreitung. Bei Kompilierung mit USE_SHM_OPEN=1 kann der Befehl reload außerdem die startup-logs des Masters ausgeben.

Beispiel:

```shell
$ echo "reload" | socat -t300 /var/run/haproxy-master.sock stdin
Success=1
--
[NOTICE]   (482713): haproxy version is 2.7-dev7-4827fb-69
[NOTICE]   (482713): path to executable is ./haproxy
[WARNING]  (482713): config: 'http-request' rules ignored for proxy 'frt1' as they require HTTP mode.
[NOTICE]   (482713): New worker (482720) forked
[NOTICE]   (482713): Loading success.

$ echo "reload" | socat -t300 /var/run/haproxy-master.sock stdin
Success=0
--
[NOTICE]   (482886): haproxy version is 2.7-dev7-4827fb-69
[NOTICE]   (482886): path to executable is ./haproxy
[ALERT]    (482886): config: parsing [test3.cfg:1]: unknown keyword 'Aglobal' out of section.
[ALERT]    (482886): config: Fatal errors found in configuration.
[WARNING]  (482886): Loading failure!

$
```

Der Befehl reload ist der letzte, der auf der Master-CLI ausgeführt wird; alle nachfolgenden Befehle werden ignoriert. Sobald der Befehl reload seinen Status zurückgibt, schließt er die Verbindung zur CLI.

Ein Neuladen schließt alle Verbindungen zur Master-CLI. Siehe auch den Befehl "hard-reload".

<a id="entry-9-4-1-show-proc"></a>

**`show proc [debug]`**

```haproxy
show proc [debug]
```

Die Master-CLI stellt den Befehl 'show proc' zur Überwachung der Prozesse bereit.

Beispiel:

```shell
$ echo 'show proc' | socat /var/run/haproxy-master.sock -
#<PID>          <type>          <reloads>       <uptime>        <version>
1162            master          5 [failed: 0]   0d00h02m07s     2.5-dev13
# workers
1271            worker          1               0d00h00m00s     2.5-dev13
# old workers
1233            worker          3               0d00h00m43s     2.0-dev3-6019f6-289
```

In diesem Beispiel wurde der Master 5 Mal neu geladen, aber einer der alten Worker läuft noch und hat 3 Neuladevorgänge überlebt. Über die CLI dieses Workers lässt sich untersuchen, was geschieht.

Der Parameter 'debug' zeigt Details zur Fehlersuche an, derzeit die FDs der IPC-Kommunikation. Zwischen haproxy-Versionen ist die Stabilität der Debugausgabe nicht gewährleistet.

<a id="entry-9-4-1-show-startup-logs"></a>

**`show startup-logs`**

```haproxy
show startup-logs
```

Für die korrekte Verwendung auf der Master-CLI muss HAProxy mit USE_SHM_OPEN=1 kompiliert werden; andernfalls sind nicht alle Meldungen sichtbar.

Wie sein Gegenstück auf dem Statistiksocket kann dieser Befehl die Startmeldungen von HAProxy anzeigen. Er gibt jedoch nicht die Startmeldungen des aktuellen Workers aus, sondern die des letzten Start- oder Neuladeversuchs. Damit kann er auch die Parsingmeldungen eines fehlgeschlagenen Neuladens ausgeben.

Diese Meldungen werden auch mit dem Befehl "reload" ausgegeben.

## 9.5. Statistikdatei (Stats-file) {#section-9-5}

Eine sogenannte Statistikdatei (stats-file) kann verwendet werden, um interne haproxy-Zähler beim Prozessstart mit Werten ungleich null vorzubelegen. Ihr Hauptzweck ist es, Statistiken von Workerprozessen über Neuladevorgänge hinweg zu erhalten. Eine stats-file enthält nur einen Teil aller von haproxy bereitgestellten Statistiken, da nur das Vorbelegen von Metrikwerten sinnvoll ist.

Derzeit unterstützt stats-file nur Proxyzähler. So lassen sich Werte für Frontends, Backends, Server und Listener vorbelegen. In einer stats-file werden jedoch nur Objektinstanzen mit einer nicht leeren GUID gespeichert. Dies stellt sicher, dass Werte für Objekte mit übereinstimmendem Typ und übereinstimmender GUID vorbelegt werden, auch wenn andere Parameter abweichen.

Der CLI-Befehl "dump stats-file" dient dazu, eine stats-file zu erzeugen. Das Format der stats-file ist intern definiert und kann künftig frei geändert und erweitert werden. Es ist auf Kompatibilität mindestens zwischen aufeinanderfolgenden stabilen haproxy-Versionszweigen ausgelegt. Wird eine stats-file in einen Prozess geladen, der eine ältere Version ausführt, kann jedoch eine optionale zusätzliche Konfiguration erforderlich sein.
