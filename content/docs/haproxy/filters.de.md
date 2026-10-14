---
title: "9. Unterstützte Filter"
linkTitle: "9. Filter"
weight: 200
description: "Filter für Tracing, Komprimierung, SPOE, Cache, FastCGI, OpenTracing und Bandbreite"
icon: fa-solid fa-layer-group
module: [HAPROXY]
categories: [Referenz]
aliases:
  - /haproxy/configuration/filters/
  - /docs/haproxy/configuration/filters/
  - /haproxy/filters/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 9"
---

Im Folgenden sind die offiziell unterstützten Filter und ihre Parameter aufgeführt. Je nach Build-Optionen sind manche Filter möglicherweise nicht verfügbar. haproxy -vv zeigt die verfügbaren Filter an.

Siehe auch "filter".

## 9.1. Trace {#section-9-1}

filter trace [name `<name>`] [random-forwarding] [max-fwd `<max>`] [hexdump]

Argumente:

```text
<name>               ist ein frei wählbarer Name für die Meldungen.
                     Ohne Angabe wird "TRACE" verwendet.

<quiet>              unterdrückt Trace-Meldungen.

<random-forwarding>  aktiviert die zufällige Weiterleitung analysierter
                     Daten. Standardmäßig leitet der Filter alle zuvor
                     analysierten Daten weiter. Mit diesem Parameter
                     gibt er nur eine zufällige Menge davon weiter.

<max>                ist die maximale Datenmenge, die auf einmal
                     weitergeleitet werden kann. "max-fwd" lässt sich
                     mit zufälliger Weiterleitung kombinieren. <max>
                     muss eine positive Ganzzahl sein.
                     0 bedeutet keine Begrenzung.

<hexdump>            gibt alle an Server und Client weitergeleiteten
                     Daten aus.
```

Dieser Filter kann als Grundlage für die Entwicklung neuer Filter dienen. Er definiert alle Rückruffunktionen und gibt für jede eine Meldung mit nützlichen Informationen auf der Standardfehlerausgabe (stderr) aus. Damit lässt sich die Aktivität anderer Filter oder von HAProxy selbst untersuchen.

Mit `<random-parsing>` und/oder `<random-forwarding>` lässt sich das Verhalten eines Filters testen, der die zwischen Client und Server übertragenen Daten analysiert. Die Parameter fügen der Verarbeitung Verzögerungen hinzu.

## 9.2. HTTP-Komprimierung {#section-9-2}

filter comp-req

Aktiviert einen Filter, der ausdrücklich versucht, HTTP-Anfragen gemäß "compression" zu komprimieren. Setzt implizit "compression direction request".

filter comp-res

Aktiviert einen Filter, der ausdrücklich versucht, HTTP-Antworten gemäß "compression" zu komprimieren. Setzt implizit "compression direction response".

filter compression (veraltet)

Alias zur Abwärtskompatibilität, der funktional der Aktivierung beider Filter "comp-req" und "comp-res" entspricht. Das gewünschte Verhalten muss mit "compression" konfiguriert werden:

Seit HAProxy 1.7 ist die HTTP-Komprimierung als Filter umgesetzt. Zum Aktivieren und Konfigurieren muss weiterhin "compression" verwendet werden. Solange keine anderen Filter eingesetzt werden, genügt dies. Das gilt auch zusammen mit aktiviertem Cache oder fcgi-app. In diesem Fall wird die Antwort immer erst nach dem Speichern im Cache komprimiert. Sobald für denselben Listener, dasselbe Frontend oder Backend jedoch mindestens ein anderer Filter als Cache oder fcgi-app verwendet wird, muss die HTTP-Komprimierung ausdrücklich durch eine filter-Zeile aktiviert werden. Dadurch ist die Auswertungsreihenfolge der Filter festgelegt.

Siehe auch "compression", [Abschnitt 9.4](/de/docs/haproxy/filters/#section-9-4) zum Cache-Filter und [Abschnitt 9.5](/de/docs/haproxy/filters/#section-9-5) zum fcgi-app-Filter.

## 9.3. Stream Processing Offload Engine (SPOE) {#section-9-3}

filter spoe [engine `<name>`] config `<file>`

Argumente:

```text
<name>      ist der Engine-Name zur Auswahl des richtigen Bereichs
            in der Konfigurationsdatei. Ohne Angabe wird die gesamte
            Datei eingelesen.

<file>      ist der Pfad zur Engine-Konfigurationsdatei. Diese kann
            mehrere Engines konfigurieren. Dann muss jeder Teil
            in einem eigenen Bereich stehen.
```

Die Stream Processing Offload Engine (SPOE) ist ein Filter, der mit externen Komponenten kommuniziert. Er ermöglicht, bestimmte Verarbeitungsschritte für Streams in mehrschichtigen Anwendungen auszulagern. Die externen Komponenten und die mit ihnen ausgetauschten Informationen werden größtenteils in eigenen Dateien konfiguriert. Zusätzlich sind eigene Backends in der HAProxy-Konfiguration erforderlich.

SPOE kommuniziert mit externen Komponenten über ein eigenes Binärprotokoll, das Stream Processing Offload Protocol (SPOP).

Wird SPOE auf einen Stream angewendet, entsteht ein eigener Stream für die Kommunikation mit der externen Komponente. Der Hauptstream ist der übergeordnete Stream dieses "SPOE"-Streams. Daher lassen sich aus dem "SPOE"-Stream Variablen des Hauptstreams abrufen. Einzelheiten zu Variablen stehen in [Abschnitt 2.8](/de/docs/haproxy/configuration-basics/#section-2-8).

Alle Angaben zur SPOE-Konfiguration und zur SPOP-Spezifikation stehen in "doc/SPOE.txt".

## 9.4. Cache {#section-9-4}

filter cache `<name>`

Argumente:

```text
<name>      ist der Name des Cache-Abschnitts, den dieser Filter nutzt.
```

Der Cache verwendet einen Filter zum Speichern cachefähiger Antworten. Mit den HTTP-Regeln "cache-store" und "cache-use" muss festgelegt werden, wie und wann der Cache verwendet wird. Der zugehörige Filter ist standardmäßig implizit definiert. Werden außer fcgi-app oder compression keine weiteren Filter verwendet, genügt das. In diesem Fall wird der Komprimierungsfilter immer nach dem Cache-Filter ausgewertet. Sobald für denselben Listener, dasselbe Frontend oder Backend mindestens ein anderer Filter als compression oder fcgi-app verwendet wird, muss der Cache jedoch ausdrücklich durch eine filter-Zeile eingebunden werden. Dadurch ist die Auswertungsreihenfolge der Filter festgelegt.

Siehe auch [Abschnitt 9.2](/de/docs/haproxy/filters/#section-9-2) zum Komprimierungsfilter, [Abschnitt 9.5](/de/docs/haproxy/filters/#section-9-5) zum fcgi-app-Filter und [Abschnitt 6](/de/docs/haproxy/cache/) zum Cache.

## 9.5. Fcgi-app {#section-9-5}

filter fcgi-app `<name>`

Argumente:

```text
<name>      ist der Name des fcgi-app-Abschnitts, den dieser Filter nutzt.
```

Die FastCGI-Anwendung verwendet einen Filter, um bei Anfragen alle benutzerdefinierten Parameter auszuwerten und bei Antworten die Header zu verarbeiten. `<name>` muss auf einen vorhandenen fcgi-app-Abschnitt verweisen. Die zu verwendende Anwendung sollte mit "use-fcgi-app" festgelegt werden. Der zugehörige Filter ist standardmäßig implizit definiert. Werden außer cache oder compression keine weiteren Filter verwendet, genügt das. Sobald für dasselbe Backend mindestens ein anderer Filter als compression oder cache verwendet wird, muss fcgi-app jedoch ausdrücklich durch eine filter-Zeile eingebunden werden. Dadurch ist die Auswertungsreihenfolge der Filter festgelegt.

Siehe auch "use-fcgi-app", [Abschnitt 9.2](/de/docs/haproxy/filters/#section-9-2) zum Komprimierungsfilter, [Abschnitt 9.4](/de/docs/haproxy/filters/#section-9-4) zum Cache-Filter und [Abschnitt 10](/de/docs/haproxy/fastcgi/) zu FastCGI-Anwendungen.

## 9.6. OpenTracing {#section-9-6}

Der OpenTracing-Filter unterstützt verteiltes Tracing direkt in HAProxy. Dazu sendet er eine OpenTracing-konforme Anfrage an einen unterstützten Tracer, etwa Datadog, Jaeger, Lightstep oder Zipkin. Die Tracer sind alphabetisch und nicht nach einer Rangfolge aufgeführt.

Die Funktion ist nur verfügbar, wenn HAProxy mit USE_OT=1 gebaut wurde.

Der OpenTracing-Filter muss ausdrücklich in der HAProxy-Konfiguration aktiviert werden. Andernfalls beteiligt er sich in keiner Weise an der Verarbeitung von HAProxy.

filter opentracing [id `<id>`] config `<file>`

Argumente:

```text
<id>        ist die Kennung des OpenTracing-Filters zur Auswahl des
            richtigen Bereichs in der Konfigurationsdatei. Ohne Angabe
            gilt 'ot-filter'. Ist in der Konfigurationsdatei kein
            Bereich festgelegt, gilt sie für alle definierten
            OpenTracing-Filter.

<file>      ist der Pfad zur OpenTracing-Konfigurationsdatei. Dieselbe
            Datei kann mehrere OpenTracing-Filter zugleich konfigurieren.
            Ohne Bereich gilt dieselbe Konfiguration für alle Filter;
            andernfalls muss jeder Filter einen eigenen Bereich haben.
```

Ausführliche Dokumentation zu Betrieb, Konfiguration und Verwendung des Filters steht im Verzeichnis addons/ot.

Hinweis: Der OpenTracing-Filter sollte für neue Entwürfe nicht verwendet werden, da die Autoren OpenTracing nicht mehr pflegen oder unterstützen. OpenTracing wird daher in 3.3 als veraltet markiert und in 3.5 entfernt. Seit 3.4 ist ein Ersatzfilter auf Basis von OpenTelemetry verfügbar. Vollständige Build-Anweisungen stehen derzeit unter:

```text
https://github.com/haproxytech/haproxy-opentelemetry/
```

## 9.7. Bandbreitenbegrenzung {#section-9-7}

```haproxy
filter bwlim-in  <name> default-limit <size> default-period <time> [min-size <sz>]
filter bwlim-out <name> default-limit <size> default-period <time> [min-size <sz>]
filter bwlim-in  <name> limit <size> key <pattern> [table <table>] [min-size <sz>]
filter bwlim-out <name> limit <size> key <pattern> [table <table>] [min-size <sz>]
```

Argumente:

```text
<name>      ist der Filtername, mit dem Aktionen 'set-bandwidth-limit'
            auf einen bestimmten Bandbreitenfilter verweisen.

<size>      ist die maximale Byte-Anzahl, die innerhalb des Zeitraums
            weitergeleitet werden kann. Der Wert muss sowohl für Filter
            je Stream als auch für gemeinsam genutzte Bandbreitenfilter
            angegeben werden. Er verwendet das HAProxy-Größenformat
            und wird in Bytes ausgedrückt.

<pattern>   ist ein Sample-Ausdruck gemäß Abschnitt 7.3. Er legt fest,
            welche Elemente analysiert, extrahiert und kombiniert
            werden, um den Tabelleneintrag für die Aktualisierung der
            Zähler auszuwählen. Er muss ausschließlich für gemeinsam
            genutzte Bandbreitenfilter angegeben werden.

<table>     ist eine optionale Tabelle anstelle der standardmäßigen
            stick-table des aktuellen Proxys. Sie kann nur für
            gemeinsam genutzte Bandbreitenfilter angegeben werden.

<time>      ist der Standardzeitraum zur Berechnung der Bandbreitenrate.
            Er kann nur für Bandbreitenfilter je Stream angegeben
            werden, verwendet das HAProxy-Zeitformat und wird in
            Millisekunden ausgedrückt.

<min-size>  ist die optionale Mindestanzahl von Bytes, die ein Stream
            auf einmal weiterleitet. Das letzte Paket darf kleiner
            sein. Der Wert kann für Filter je Stream und gemeinsam
            genutzte Bandbreitenfilter angegeben werden. Er verwendet
            das HAProxy-Größenformat und wird in Bytes ausgedrückt.
```

Filter zur Bandbreitenbegrenzung sollten eingesetzt werden, um die Weiterleitungsgeschwindigkeit auf Stream-Ebene zu beschränken. Damit begrenzen sie die Netzwerkbandbreite, die eine Ressource belegt. Mehrere solche Filter lassen sich kombinieren. Beispielsweise kann eine Grenze pro Quelladresse verhindern, dass ein Client die gesamte Bandbreite beansprucht und andere Clients benachteiligt. Eine weitere Grenze pro Stream ermöglicht, mehrere Verbindungen desselben Clients gerecht zu behandeln.

Die Definitionsreihenfolge ist wichtig. Sind mehrere Bandbreitenfilter auf einem Stream aktiviert, werden sie in dieser Reihenfolge angewendet. Auch die Position anderer Filter spielt eine Rolle. Je nachdem, ob der HTTP-Komprimierungsfilter vor oder nach dem Bandbreitenfilter definiert ist, gilt die Grenze für die komprimierten oder die unkomprimierten Nutzdaten. Dasselbe gilt für den Cache-Filter.

Es gibt zwei Arten von Bandbreitenfiltern. Die erste setzt eine Standardgrenze je Stream durch. Die zweite verwendet eine Zuordnungstabelle, um eine Grenze gleichmäßig auf alle Streams aufzuteilen, die denselben Tabelleneintrag verwenden.

Je nach Filter-Schlüsselwort gilt die Begrenzung für eingehende Daten vom Client zum Server oder für ausgehende Daten vom Server zum Client. Für eingehende Daten muss "bwlim-in", für ausgehende "bwlim-out" verwendet werden. In beiden Fällen greift die Bandbreitenbegrenzung bei der Datenweiterleitung auf Stream-Ebene.

Die Begrenzung gilt für Streams, nicht für Verbindungen. Bei Multiplex-Protokollen wie H2, H3 und FastCGI können Streams derselben Verbindung unterschiedliche Grenzen haben.

Für einen Bandbreitenfilter je Stream müssen Standardzeitraum und Standardgrenze definiert werden. Sie legen die standardmäßige Bandbreitenrate eines Streams fest. Nur bei dieser Filterart lassen sich die Werte mit Sample-Ausdrücken überschreiben, wenn der Filter durch eine TCP/HTTP-Aktion "set-bandwidth-limit" aktiviert wird.

Bei einem gemeinsam genutzten Bandbreitenfilter muss die Zuordnungstabelle die zur Richtung passende Byte-Rate speichern. Für eingehende Daten ist der Zähler "bytes_in_rate(`<period>`)" erforderlich, für ausgehende "bytes_out_rate(`<period>`)".

Außerdem lässt sich die Mindestanzahl von Bytes festlegen, die ein Bandbreitenfilter für einen Stream auf einmal weiterleitet. Sie sollte verhindern, dass zu kleine Datenmengen übertragen werden, und so die CPU-Last verringern. Der Wert muss sorgfältig gewählt werden: Ist er zu klein, kann die CPU-Last steigen; ist er zu groß, kann die Latenz zunehmen. Er hängt auch eng mit der Bandbreitengrenze zusammen. Liegt er zu nahe an dieser Grenze, können Pausen nötig werden, um sie nicht zu überschreiten, weil auf einmal zu viele Bytes verbraucht werden. Der passende Wert hängt stark von der Filterkonfiguration ab. Ein sinnvoller Ausgangspunkt sind etwa 2 TCP MSS, normalerweise 2896 Bytes. Anschließend lässt sich der Wert anhand von Versuchen optimieren.

Beispiel:

```text
frontend http
    bind *:80
    mode http

    # If this filter is enabled, the stream will share the download limit
    # of 10m/s with all other streams with the same source address.
    filter bwlim-out limit-by-src key src table limit-by-src limit 10m

    # If this filter is enabled, the stream will be limited to download at 1m/s,
    # independently of all other streams.
    filter bwlim-out limit-by-strm default-limit 1m default-period 1s

    # Limit all streams to 1m/s (the default limit) and those accessing the
    # internal API to 100k/s. Limit each source address to 10m/s. The shared
    # limit is applied first. Both are limiting the download rate.
    http-request set-bandwidth-limit limit-by-strm
    http-request set-bandwidth-limit limit-by-strm limit 100k if { path_beg /internal }
    http-request set-bandwidth-limit limit-by-src
    ...

backend limit-by-src
    # The stickiness table used by <limit-by-src> filter
    stick-table type ip size 1m expire 3600s store bytes_out_rate(1s)
```

Siehe auch "tcp-request content set-bandwidth-limit", "tcp-response content set-bandwidth-limit", "http-request set-bandwidth-limit" und "http-response set-bandwidth-limit".
