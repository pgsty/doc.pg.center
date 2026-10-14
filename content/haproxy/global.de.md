---
title: "3. Globaler Abschnitt"
linkTitle: "3. Globaler Abschnitt"
weight: 140
description: "Prozesssicherheit, Leistungsoptimierung, Fehlerbehebung und HTTP-Client-Einstellungen"
icon: fa-solid fa-earth-americas
module: [HAPROXY]
categories: [Referenz]
aliases:
  - /haproxy/configuration/global/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 3"
---

Parameter im Abschnitt "global" gelten für den gesamten Prozess und sind häufig vom Betriebssystem
(OS) abhängig. Sie werden in der Regel einmalig festgelegt und müssen nach korrekter Konfiguration
nicht mehr geändert werden. Für einige gibt es entsprechende Befehlszeilenoptionen.

Im Abschnitt "global" werden die folgenden Schlüsselwörter unterstützt:

- Prozessverwaltung und Sicherheit

  - 51degrees-allow-unmatched
  - 51degrees-cache-size
  - 51degrees-data-file
  - 51degrees-difference
  - 51degrees-drift
  - 51degrees-property-name-list
  - 51degrees-property-separator
  - 51degrees-use-performance-graph
  - 51degrees-use-predictive-graph
  - ca-base
  - chroot
  - cluster-secret
  - cpu-affinity
  - cpu-map
  - cpu-policy
  - cpu-set
  - crt-base
  - daemon
  - default-path
  - description
  - deviceatlas-json-file
  - deviceatlas-log-level
  - deviceatlas-properties-cookie
  - deviceatlas-separator
  - dns-accept-family
  - expose-deprecated-directives
  - expose-experimental-directives
  - external-check
  - fd-hard-limit
  - gid
  - grace
  - group
  - h1-accept-payload-with-any-method
  - h1-case-adjust
  - h1-case-adjust-file
  - h1-do-not-close-on-insecure-transfer-encoding
  - h2-workaround-bogus-websocket-clients
  - hard-stop-after
  - harden.reject-privileged-ports.tcp
  - harden.reject-privileged-ports.quic
  - insecure-fork-wanted
  - insecure-setuid-wanted
  - issuers-chain-path
  - jwt.allow_none_alg
  - jwt.decrypt_alg_list
  - jwt.decrypt_enc_list
  - key-base
  - limited-quic
  - localpeer
  - log
  - log-send-hostname
  - log-tag
  - lua-load
  - lua-load-per-thread
  - lua-prepend-path
  - max-threads-per-group
  - mworker-max-reloads
  - nbthread
  - node
  - numa-cpu-mapping
  - ocsp-update.disable
  - ocsp-update.maxdelay
  - ocsp-update.mindelay
  - ocsp-update.httpproxy
  - ocsp-update.mode
  - pidfile
  - pp2-never-send-local
  - presetenv
  - prealloc-fd
  - resetenv
  - set-dumpable
  - set-var
  - setenv
  - ssl-default-bind-ciphers
  - ssl-default-bind-ciphersuites
  - ssl-default-bind-client-sigalgs
  - ssl-default-bind-curves
  - ssl-default-bind-options
  - ssl-default-bind-sigalgs
  - ssl-default-server-ciphers
  - ssl-default-server-ciphersuites
  - ssl-default-server-client-sigalgs
  - ssl-default-server-curves
  - ssl-default-server-options
  - ssl-default-server-sigalgs
  - ssl-dh-param-file
  - ssl-propquery
  - ssl-provider
  - ssl-provider-path
  - ssl-security-level
  - ssl-server-verify
  - ssl-skip-self-issued-ca
  - stats
  - stats-file
  - strict-limits
  - uid
  - ulimit-n
  - unix-bind
  - unsetenv
  - user
  - wurfl-cache-size
  - wurfl-data-file
  - wurfl-information-list
  - wurfl-information-list-separator

- Leistungsoptimierung

  - busy-polling
  - max-spread-checks
  - maxcompcpuusage
  - maxcomprate
  - maxconn
  - maxconnrate
  - maxpipes
  - maxsessrate
  - maxsslconn
  - maxsslrate
  - maxzlibmem
  - no-memory-trimming
  - noepoll
  - noevports
  - nogetaddrinfo
  - nokqueue
  - noktls
  - nopoll
  - noreuseport
  - nosplice
  - profiling.memory
  - profiling.tasks
  - server-state-base
  - server-state-file
  - spread-checks
  - ssl-engine
  - ssl-mode-async
  - tune.applet.zero-copy-forwarding
  - tune.buffers.limit
  - tune.buffers.reserve
  - tune.bufsize
  - tune.bufsize.large
  - tune.bufsize.small
  - tune.cli.max-payload-size
  - tune.comp.maxlevel
  - tune.defaults.purge
  - tune.disable-fast-forward
  - tune.disable-zero-copy-forwarding
  - tune.epoll.mask-events
  - tune.events.max-events-at-once
  - tune.fail-alloc
  - tune.fd.edge-triggered
  - tune.h1.be.glitches-threshold
  - tune.h1.fe.glitches-threshold
  - tune.h1.zero-copy-fwd-recv
  - tune.h1.zero-copy-fwd-send
  - tune.h2.be.glitches-threshold
  - tune.h2.be.initial-window-size
  - tune.h2.be.max-concurrent-streams
  - tune.h2.be.max-frames-at-once
  - tune.h2.be.rxbuf
  - tune.h2.fe.glitches-threshold
  - tune.h2.fe.initial-window-size
  - tune.h2.fe.max-concurrent-streams
  - tune.h2.fe.max-frames-at-once
  - tune.h2.fe.max-rst-at-once
  - tune.h2.fe.max-total-streams
  - tune.h2.fe.rxbuf
  - tune.h2.header-table-size
  - tune.h2.initial-window-size
  - tune.h2.max-concurrent-streams
  - tune.h2.max-frame-size
  - tune.h2.zero-copy-fwd-send
  - tune.http.cookielen
  - tune.http.logurilen
  - tune.http.maxhdr
  - tune.idle-pool.shared
  - tune.idletimer
  - tune.lua.bool-sample-conversion
  - tune.lua.burst-timeout
  - tune.lua.forced-yield
  - tune.lua.log.loggers
  - tune.lua.log.stderr
  - tune.lua.maxmem
  - tune.lua.openlibs
  - tune.lua.service-timeout
  - tune.lua.session-timeout
  - tune.lua.task-timeout
  - tune.max-checks-per-thread
  - tune.maxaccept
  - tune.maxpollevents
  - tune.maxrewrite
  - tune.max-rules-at-once
  - tune.memory.hot-size
  - tune.pattern.cache-size
  - tune.peers.max-updates-at-once
  - tune.pipesize
  - tune.pool-high-fd-ratio
  - tune.pool-low-fd-ratio
  - tune.pt.zero-copy-forwarding
  - tune.quic.be.cc.cubic-min-losses
  - tune.quic.be.cc.hystart
  - tune.quic.be.cc.max-frame-loss
  - tune.quic.be.cc.max-win-size
  - tune.quic.be.cc.reorder-ratio
  - tune.quic.be.max-idle-timeout
  - tune.quic.be.sec.glitches-threshold
  - tune.quic.be.stream.data-ratio
  - tune.quic.be.stream.max-concurrent
  - tune.quic.be.stream.rxbuf
  - tune.quic.be.tx.pacing
  - tune.quic.be.tx.udp-gso
  - tune.quic.cc.cubic.min-losses (veraltet)
  - tune.quic.cc-hystart (veraltet)
  - tune.quic.disable-tx-pacing (veraltet)
  - tune.quic.disable-udp-gso (veraltet)
  - tune.quic.fe.cc.cubic-min-losses
  - tune.quic.fe.cc.hystart
  - tune.quic.fe.cc.max-frame-loss
  - tune.quic.fe.cc.max-win-size
  - tune.quic.fe.cc.reorder-ratio
  - tune.quic.fe.max-idle-timeout
  - tune.quic.fe.sec.glitches-threshold
  - tune.quic.fe.sec.retry-threshold
  - tune.quic.fe.sock-per-conn
  - tune.quic.fe.stream.data-ratio
  - tune.quic.fe.stream.max-concurrent
  - tune.quic.fe.stream.max-total
  - tune.quic.fe.stream.rxbuf
  - tune.quic.fe.tx.pacing
  - tune.quic.fe.tx.udp-gso
  - tune.quic.frontend.max-data-size (veraltet)
  - tune.quic.frontend.max-idle-timeout (veraltet)
  - tune.quic.frontend.max-streams-bidi (veraltet)
  - tune.quic.frontend.max-tx-mem (veraltet)
  - tune.quic.frontend.stream-data-ratio (veraltet)
  - tune.quic.frontend.default-max-window-size (veraltet)
  - tune.quic.listen
  - tune.quic.max-frame-loss (veraltet)
  - tune.quic.mem.tx-max
  - tune.quic.reorder-ratio (veraltet)
  - tune.quic.retry-threshold (veraltet)
  - tune.quic.socket-owner (veraltet)
  - tune.quic.zero-copy-fwd-send
  - tune.renice.runtime
  - tune.renice.startup
  - tune.rcvbuf.backend
  - tune.rcvbuf.client
  - tune.rcvbuf.frontend
  - tune.rcvbuf.server
  - tune.recv_enough
  - tune.ring.queues
  - tune.runqueue-depth
  - tune.sched.low-latency
  - tune.sndbuf.backend
  - tune.sndbuf.client
  - tune.sndbuf.frontend
  - tune.sndbuf.server
  - tune.streams-elasticity
  - tune.stick-counters
  - tune.ssl.cachesize
  - tune.ssl.capture-buffer-size
  - tune.ssl.capture-cipherlist-size (veraltet)
  - tune.ssl.certificate-compression
  - tune.ssl.default-dh-param
  - tune.ssl.force-private-cache
  - tune.ssl.hard-maxrecord
  - tune.ssl.keylog
  - tune.ssl.keyupdate-rate-limit
  - tune.ssl.lifetime
  - tune.ssl.maxrecord
  - tune.ssl.ssl-ctx-cache-size
  - tune.ssl.ocsp-update.maxdelay (veraltet)
  - tune.ssl.ocsp-update.mindelay (veraltet)
  - tune.takeover-other-tg-connections
  - tune.vars.global-max-size
  - tune.vars.proc-max-size
  - tune.vars.reqres-max-size
  - tune.vars.sess-max-size
  - tune.vars.txn-max-size
  - tune.zlib.memlevel
  - tune.zlib.windowsize

- Fehlerbehebung

  - anonkey
  - debug.counters
  - force-cfg-parser-pause
  - quiet
  - warn-blocked-traffic-after
  - zero-warning

- HTTPClient

  - httpclient.resolvers.disabled
  - httpclient.resolvers.id
  - httpclient.resolvers.prefer
  - httpclient.retries
  - httpclient.ssl.ca-file
  - httpclient.ssl.verify
  - httpclient.timeout.connect

## 3.1. Prozessverwaltung und Sicherheit {#section-3-1}

<a id="entry-3-1-51degrees-data-file"></a>

**`51degrees-data-file <file path>`**

```haproxy
51degrees-data-file <file path>
```

Der Pfad der 51Degrees-Datendatei für die Geräteerkennung. Die Datei sollte entpackt und für
HAProxy mit den erforderlichen Berechtigungen zugänglich sein.

Beachten Sie, dass diese Option nur verfügbar ist, wenn HAProxy mit USE_51DEGREES kompiliert wurde.

<a id="entry-3-1-51degrees-property-name-list"></a>

**`51degrees-property-name-list [<string> ...]`**

```haproxy
51degrees-property-name-list [<string> ...]
```

Eine Liste von 51Degrees-Eigenschaftsnamen, die aus dem Datensatz geladen werden sollen. Eine vollständige Liste ist auf der 51Degrees-Website verfügbar: <https://51degrees.com/resources/property-dictionary>

Bitte beachten Sie, dass diese Option nur verfügbar ist, wenn HAProxy mit USE_51DEGREES kompiliert wurde.

<a id="entry-3-1-51degrees-property-separator"></a>

**`51degrees-property-separator <char>`**

```haproxy
51degrees-property-separator <char>
```

Ein Zeichen, das an jeden Eigenschaftswert in einem Antwortheader angehängt wird, der 51Degrees-Ergebnisse enthält. Wenn nicht gesetzt, wird als Standardwert ',' verwendet.

Bitte beachten Sie, dass diese Option nur verfügbar ist, wenn HAProxy mit USE_51DEGREES kompiliert wurde.

<a id="entry-3-1-51degrees-cache-size"></a>

**`51degrees-cache-size <number>`**

```haproxy
51degrees-cache-size <number>
```

Legt die Größe des 51Degrees-Konverter-Caches auf `<number>` Einträge fest. Dies ist ein LRU-Cache, der vorherige Geräteerkennungen und deren Ergebnisse speichert. Standardmäßig ist dieser Cache deaktiviert.

Bitte beachten Sie, dass diese Option nur verfügbar ist, wenn HAProxy mit USE_51DEGREES kompiliert wurde.

<a id="entry-3-1-51degrees-use-performance-graph"></a>

**`51degrees-use-performance-graph { on | off }`**

```haproxy
51degrees-use-performance-graph { on | off }
```

Aktiviert ('on') oder deaktiviert ('off') die Verwendung des Leistungsgraphen im Erkennungsprozess. Der Standardwert hängt von der 51Degrees-Bibliothek ab.

Bitte beachten Sie, dass diese Option nur verfügbar ist, wenn HAProxy mit USE_51DEGREES und 51DEGREES_VER=4 kompiliert wurde.

<a id="entry-3-1-51degrees-use-predictive-graph"></a>

**`51degrees-use-predictive-graph { on | off }`**

```haproxy
51degrees-use-predictive-graph { on | off }
```

Aktiviert ('on') oder deaktiviert ('off') die Verwendung des Vorhersagegraphen im Erkennungsprozess. Der Standardwert hängt von der 51Degrees-Bibliothek ab.

Bitte beachten Sie, dass diese Option nur verfügbar ist, wenn HAProxy mit USE_51DEGREES und 51DEGREES_VER=4 kompiliert wurde.

<a id="entry-3-1-51degrees-drift"></a>

**`51degrees-drift <number>`**

```haproxy
51degrees-drift <number>
```

Legt den zulässigen Driftwert für eine Erkennung fest.

Bitte beachten Sie, dass diese Option nur verfügbar ist, wenn HAProxy mit USE_51DEGREES und 51DEGREES_VER=4 kompiliert wurde.

<a id="entry-3-1-51degrees-difference"></a>

**`51degrees-difference <number>`**

```haproxy
51degrees-difference <number>
```

Legt den zulässigen Differenzwert für eine Erkennung fest.

Bitte beachten Sie, dass diese Option nur verfügbar ist, wenn HAProxy mit USE_51DEGREES und 51DEGREES_VER=4 kompiliert wurde.

<a id="entry-3-1-51degrees-allow-unmatched"></a>

**`51degrees-allow-unmatched { on | off }`**

```haproxy
51degrees-allow-unmatched { on | off }
```

Aktiviert ('on') oder deaktiviert ('off') die Verwendung von nicht übereinstimmenden Knoten im Erkennungsprozess. Der Standardwert hängt von der 51Degrees-Bibliothek ab.

Bitte beachten Sie, dass diese Option nur verfügbar ist, wenn HAProxy mit USE_51DEGREES und 51DEGREES_VER=4 kompiliert wurde.

<a id="entry-3-1-acme-scheduler"></a>

**`acme.scheduler { auto | off }`**

```haproxy
acme.scheduler { auto | off }
```

Aktiviert oder deaktiviert den ACME-Scheduler.

Der ACME-Scheduler startet beim Start von HAProxy und durchläuft die Zertifikate. Er startet eine
ACME-Erneuerungsaufgabe, wenn der notAfter-Wert gegenüber curtime + (notAfter - notBefore) / 12
bereits verstrichen ist; ist notBefore nicht definiert, gilt ein Zeitraum von 7 Tagen. Anschließend
schläft der Scheduler und wacht nach 12 Stunden wieder auf.

Der Standardwert ist "auto".

Siehe auch: acme

<a id="entry-3-1-ca-base"></a>

**`ca-base <dir>`**

```haproxy
ca-base <dir>
```

Weist ein Standardverzeichnis zum Abrufen von SSL-CA-Zertifikaten und CRLs zu, wenn mit den Anweisungen "ca-file", "ca-verify-file" oder "crl-file" ein relativer Pfad verwendet wird. Absolute Pfade, die in "ca-file", "ca-verify-file" und "crl-file" angegeben sind, haben Vorrang und ignorieren "ca-base".

<a id="entry-3-1-chroot"></a>

**`chroot { <jail dir> | auto }`**

```haproxy
chroot { <jail dir> | auto }
```

Wechselt in das Verzeichnis `<jail dir>` und führt dort chroot() aus, bevor Privilegien abgegeben
werden. Dies erhöht die Sicherheit bei Ausnutzung einer unbekannten Schwachstelle, da ein Angriff
auf das System dadurch sehr erschwert wird. Es ist wichtig sicherzustellen, dass `<jail dir>` leer
und für niemanden beschreibbar ist. Wird der Prozess mit Superuser-Rechten gestartet, wird chroot()
direkt ausgeführt. Unter Linux versucht haproxy bei einem Start ohne Privilegien, dies innerhalb
eines mit unshare(CLONE_NEWUSER) neu erzeugten Benutzernamensraums auszuführen. Ist dieser Mechanismus
nicht verfügbar, schlägt chroot() mit der üblichen Fehlermeldung fehl.

Als Sonderfall kann `<jail dir>` auf "auto" gesetzt werden. Dann erzeugt haproxy ein anonymes
temporäres Verzeichnis, entfernt dessen Verzeichniseintrag und führt darin chroot() aus. Das
resultierende Jail hat keinen Namen im Dateisystem, ist leer und schreibgeschützt. Ein eigenes
Jail-Verzeichnis muss daher nicht vorbereitet werden.

Wenn mit Superuser-Berechtigungen gestartet wird, wird eine Warnung ausgegeben, wenn kein chroot verwendet wird, um Benutzer dazu zu ermutigen, stets dieses Verfahren zu nutzen. Falls aus irgendeinem Grund ein zwingender Grund besteht, chroot nicht zu verwenden (z. B. Zugriff auf einen Server über einen Unix-Socket mit unpassendem Pfad), bleibt es möglich, die Warnung zu unterdrücken, indem explizit "chroot /" hinzugefügt wird. Dies hat den Vorteil, dass es in der Konfiguration sichtbar ist.

<a id="entry-3-1-close-spread-time"></a>

**`close-spread-time <time>`**

```haproxy
close-spread-time <time>
```

Definiert ein Zeitfenster, über das beim geordneten Herunterfahren das Schließen ungenutzter und
aktiver Verbindungen verteilt wird. Nach Empfang von SIGUSR1 und Ablauf einer gegebenenfalls
vorhandenen Schonfrist werden ohne diese Option alle ungenutzten Verbindungen auf einmal geschlossen.
Aktive HTTP- oder HTTP2-Verbindungen werden nach Empfang der nächsten Anfrage beendet, entweder
mit einer zusätzlichen Zeile "Connection:
close" in der HTTP-Antwort oder einem GOAWAY-Frame bei HTTP2. Ist die Option gesetzt, wird das
Schließen über die angegebene Zeit `<time>` verteilt. Bei close-spread-time "infinite" wird das
aktive Schließen von Verbindungen während des geordneten Herunterfahrens deaktiviert. Der Header
"Connection: close" wird HTTP-Antworten nicht mehr hinzugefügt (ebenso wenig GOAWAY bei HTTP2).
Ungenutzte Verbindungen werden erst bei Erreichen ihrer Zeitüberschreitung geschlossen, entsprechend
den verschiedenen konfigurierten Zeitüberschreitungen.

Argumente:

```text
<time>  ist ein Zeitfenster (standardmäßig in Millisekunden), über das
        das Schließen von Verbindungen beim geordneten Beenden verteilt
        wird, oder "infinite", wenn das aktive Schließen von Verbindungen
        deaktiviert werden soll.
```

Es wird empfohlen, diesen Wert niedriger als den Wert in der "hard-stop-after"-Option einzustellen, falls diese verwendet wird, damit alle Verbindungen die Möglichkeit haben, vor dem Prozessende ordnungsgemäß zu schließen.

Siehe auch: grace, hard-stop-after, idle-close-on-response

<a id="entry-3-1-cluster-secret"></a>

**`cluster-secret <secret>`**

```haproxy
cluster-secret <secret>
```

Definiert eine ASCII-Zeichenkette als Geheimnis, das zwischen mehreren Knoten desselben Clusters geteilt wird. Es kann für verschiedene Zwecke verwendet werden. Es wird mindestens verwendet, um zustandslose Reset-Tokens für alle von diesem Prozess instanziierten QUIC-Verbindungen abzuleiten. Ebenso dient es zur Ableitung von Geheimnissen zum Verschlüsseln von Retry-Tokens.

Wenn dieser Parameter nicht gesetzt ist, wird beim Prozessstart ein zufälliger Wert gewählt. Dies ermöglicht die Nutzung von Funktionen, die darauf basieren, wenn auch mit gewissen Einschränkungen.

<a id="entry-3-1-cpu-map"></a>

**`cpu-map [auto:]<thread-group>[/<thread-set>] <cpu-set>[,...] [...]`**

```haproxy
cpu-map [auto:]<thread-group>[/<thread-set>] <cpu-set>[,...] [...]
```

Auf einigen Betriebssystemen ist es möglich, eine Thread-Gruppe oder einen Thread einer bestimmten CPU-Menge zuzuordnen. Das bedeutet, dass die zugewiesenen Threads niemals auf anderen CPUs ausgeführt werden. Die Anweisung "cpu-map" legt CPU-Mengen für einzelne Threads oder Thread-Gruppen fest. Das erste Argument ist ein Thread-Gruppenbereich, optional gefolgt von einem Thread-Menge. Diese Bereiche haben folgendes Format:

```text
all | odd | even | number[-[number]]
```

`<number>` muss je nach Wortbreite des Rechners zwischen 1 und 32 oder 64 liegen. Gruppen-IDs
oberhalb von 'thread-groups' und Thread-IDs oberhalb der Wortbreite des Rechners werden ignoriert.
Alle Thread-Nummern sind relativ zu ihrer jeweiligen Gruppe. Ein Bereich kann mit zwei durch einen
Bindestrich ('-') getrennten Nummern angegeben werden. Wie bei der bind-Direktive "thread" wählt
"all" alle Threads, "odd" nur ungerade und "even" nur gerade Nummern aus. Das zweite und alle
weiteren Argumente sind CPU-Mengen. Jede CPU-Menge ist entweder eine einzelne Nummer, beginnend
bei 0 für die erste CPU, oder ein Bereich aus zwei durch einen Bindestrich ('-') getrennten Nummern.
CPU-Nummern und Bereiche können durch Kommas getrennt oder als weitere Argumente in derselben
Zeile mehrfach angegeben werden. Außerhalb von Linux und BSD kann der maximale CPU-Index auf 31
oder 63 begrenzt sein. Mehrere "cpu-map"-Direktiven sind zulässig; jede ersetzt jedoch frühere
"cpu-map"-Angaben, soweit sie sich überschneiden.

Bereiche können teilweise definiert werden: Die obere Grenze darf fehlen. Dann wird sie durch
den entsprechenden Höchstwert ersetzt, je nach Wortbreite des Rechners 32 oder 64.

Vor die Thread-Menge kann das Präfix "auto:" gesetzt werden. HAProxy bindet die Threads dann
automatisch an CPUs, indem es die Thread- und CPU-Mengen schrittweise durchläuft. Dafür müssen beide
Mengen gleich groß sein. Unabhängig von der Deklarationsreihenfolge der CPU-Mengen erfolgt die
Bindung von der niedrigsten zur höchsten Grenze. Mit "auto:" werden nicht gleichzeitig ein
Gruppenbereich und ein Thread-Bereich unterstützt. Nur einer darf ein Bereich sein; der andere
muss eine feste Nummer sein.

Gruppenbereiche werden aus historischen Gründen unterstützt. Heute bezeichnet eine einzelne
Nummer eine Thread-Gruppe und muss 1 sein, wenn keine Thread-Gruppen verwendet werden. Ohne
Thread-Gruppen muss einem Thread-Bereich oder einer Thread-Nummer "1/" vorangestellt werden.
Schließlich ist "1" genau gleichbedeutend mit "1/all" und bezeichnet alle Threads der Gruppe.

Beispiele:

```shell
cpu-map 1/all 0-3 # bind all threads of the first group on the
                  # first 4 CPUs

cpu-map 1/1- 0-   # will be replaced by "cpu-map 1/1-64 0-63"
                  # or "cpu-map 1/1-32 0-31" depending on the machine's
                  # word size.

# all these lines bind thread 1 to the cpu 0, the thread 2 to cpu 1
# and so on.
cpu-map auto:1/1-4   0-3
cpu-map auto:1/1-4   0-1 2-3
cpu-map auto:1/1-4   3 2 1 0
cpu-map auto:1/1-4   3,2,1,0

# bind each thread to exactly one CPU using all/odd/even keyword
cpu-map auto:1/all   0-63
cpu-map auto:1/even  0-31
cpu-map auto:1/odd   32-63

# invalid cpu-map because thread and CPU sets have different sizes.
cpu-map auto:1/1-4   0    # invalid
cpu-map auto:1/1     0-3  # invalid

# map 40 threads of those 4 groups to individual CPUs
cpu-map auto:1/1-10   0-9
cpu-map auto:2/1-10   10-19
cpu-map auto:3/1-10   20-29
cpu-map auto:4/1-10   30-39

# Map 80 threads to one physical socket and 80 others to another socket
# without forcing assignment. These are split into 4 groups since no
# group may have more than 64 threads.
cpu-map 1/1-40   0-39,80-119    # node0, siblings 0 & 1
cpu-map 2/1-40   0-39,80-119
cpu-map 3/1-40   40-79,120-159  # node1, siblings 0 & 1
cpu-map 4/1-40   40-79,120-159

```

<a id="entry-3-1-cpu-affinity"></a>

**`cpu-affinity <affinity>`**

```haproxy
cpu-affinity <affinity>
```

Legt fest, wie Threads an CPUs gebunden werden sollen. Derzeit werden folgende Werte akzeptiert:

- per-core: Jeder Thread wird an alle Hardware-Threads eines Kerns gebunden.
- per-group: Jeder Thread wird an alle Hardware-Threads der Gruppe gebunden. Dies ist der Standard,
  sofern nicht "threads-per-core 1" in "cpu-policy" verwendet wird. "per-group" akzeptiert ein
  optionales Argument zur CPU-Zuweisung. Ist eine CPU-Liste größer als die maximal zulässige Anzahl
  von CPUs pro Gruppe und muss auf mehrere Gruppen aufgeteilt werden, bestimmt eine zusätzliche
  Option, wie die Gruppen an diese CPUs gebunden werden:
  - auto: Jede Thread-Gruppe erhält nur einen gleich großen Anteil zusammenhängender CPU-Kerne,
    die ausschließlich ihr zugeordnet sind und nicht mit anderen Gruppen geteilt werden. Dies ist
    der Standard, da es im Allgemeinen günstiger ist.
  - loose: Jede Gruppe darf weiterhin jede CPU der Liste verwenden. Das führt im Allgemeinen zu
    mehr Konkurrenz um Ressourcen, kann aber gelegentlich helfen, mit störender Zusatzlast auf
    denselben CPUs besser umzugehen.
- auto: Verwendet "per-group", sofern nicht "threads-per-core 1" in "cpu-policy" gesetzt ist;
  dann wird "per-core" verwendet. Dies ist der Standard.
- per-thread: Bindet einen Thread an genau einen Hardware-Thread. Bei "threads-per-core 1" in
  "cpu-policy" wird jeder Thread an einen Hardware-Thread eines anderen Kerns gebunden.
- per-ccx: Jeder Thread wird an alle Hardware-Threads eines CCX gebunden.

<a id="entry-3-1-cpu-policy"></a>

**`cpu-policy <policy> [threads-per-core 1 | auto]`**

```haproxy
cpu-policy <policy> [threads-per-core 1 | auto]
```

Wählt die zu verwendende Richtlinie für die CPU-Zuweisung.

Auf Systemen mit mehreren CPUs gibt es viele Gründe, nicht alle verfügbaren CPU-Kerne zu
verwenden oder sie auf verschiedene Thread-Gruppen aufzuteilen: Leistung, Latenz, Kosten oder die
systemweite Ressourcenverwaltung. Mit "cpu-set" können bereits einige Kerne ausgeschlossen
werden. Anschließend muss aber entschieden werden, wie die übrigen auf Threads und Thread-Gruppen
verteilt werden.

Diese Zuordnung erfolgt normalerweise mit "cpu-map", kann auf heterogenen Systemen jedoch
besonders schwer zu pflegen sein.

Die Direktive "cpu-policy" wählt stattdessen eine von wenigen Zuweisungsrichtlinien aus, wenn
"cpu-map" nicht verwendet wird. Derzeit werden die folgenden Richtlinien unterstützt;
"performance" ist der Standard:

- none Es erfolgt keine besondere nachgelagerte Auswahl. Alle aktivierten CPUs sind nutzbar.
  Ist die Thread-Anzahl nicht gesetzt, entspricht sie der Anzahl verfügbarer CPUs, jedoch pro
  Thread-Gruppe höchstens 32 auf 32-Bit-Systemen oder 64 auf 64-Bit-Systemen. Ist die Anzahl der
  Thread-Gruppen nicht gesetzt, wird sie auf 1 gesetzt.

- efficiency Wie "group-by-ccx" unten, allerdings werden CPU-Cluster ausgeschlossen, deren Kerne
  mehr als 25% leistungsfähiger sind als die des nächstleistungsschwächeren Typs. Dies sind
  typischerweise "big"- oder "performance"-Kerne. Werden mehrere CPU-Kerntypen erkannt, wird also
  nur der effiziente Typ verwendet. Bei mäßiger Last kann dies sinnvoll sein, wenn die
  leistungsstärksten Kerne für die Anwendung oder eine Sicherheitskomponente verfügbar bleiben
  sollen. Einige moderne CPUs haben viele solcher effizienten Kerne, die zusammen bei geringerem
  Energieverbrauch eine angemessene Leistung liefern können.

- first-usable-node Wenn die CPUs beim Start nicht bereits eingeschränkt wurden (etwa mit
  "taskset") und "nbthread" nicht gesetzt ist, wird der erste NUMA-Knoten mit aktivierten CPUs
  verwendet. Die Anzahl seiner CPUs wird zur Thread-Anzahl. Für alle wird eine einzige
  Thread-Gruppe aktiviert, innerhalb der systemabhängigen Grenze von 32 oder 64.

- group-by-2-ccx Wie "group-by-ccx" unten, erstellt aber für je zwei CCX eine Gruppe. Bei CPUs
  mit vielen CCX aus jeweils wenigen Kernen kann dies sinnvoll sein, um viele Gruppen zu vermeiden
  oder die Verteilung etwas zu glätten, wenn nicht alle Kerne verwendet werden. Beachten Sie,
  dass langsame Kommunikation zwischen CCX die Leistung dabei sehr stark beeinträchtigen kann.
  Im Allgemeinen wird davon abgeraten.

- group-by-2-clusters Wie "group-by-cluster", erstellt aber für je zwei Cluster eine Gruppe.
  Bei CPUs mit vielen Clustern aus jeweils wenigen Kernen kann dies sinnvoll sein, um viele
  Gruppen zu vermeiden oder die Verteilung etwas zu glätten, wenn nicht alle Kerne verwendet
  werden. Beachten Sie, dass langsame Kommunikation zwischen Clustern die Leistung dabei sehr
  stark beeinträchtigen kann. Im Allgemeinen wird davon abgeraten.

- group-by-3-ccx Wie "group-by-ccx" unten, erstellt aber für je drei CCX eine Gruppe. Bei CPUs
  mit vielen CCX aus jeweils wenigen Kernen kann dies sinnvoll sein, um viele Gruppen zu vermeiden
  oder die Verteilung etwas zu glätten, wenn nicht alle Kerne verwendet werden. Beachten Sie,
  dass langsame Kommunikation zwischen CCX die Leistung dabei sehr stark beeinträchtigen kann.
  Im Allgemeinen wird davon abgeraten.

- group-by-3-clusters Wie "group-by-cluster", erstellt aber für je drei Cluster eine Gruppe.
  Bei CPUs mit vielen Clustern aus jeweils wenigen Kernen kann dies sinnvoll sein, um viele
  Gruppen zu vermeiden oder die Verteilung etwas zu glätten, wenn nicht alle Kerne verwendet
  werden. Beachten Sie, dass langsame Kommunikation zwischen Clustern die Leistung dabei sehr
  stark beeinträchtigen kann. Im Allgemeinen wird davon abgeraten.

- group-by-4-ccx Wie "group-by-ccx" unten, erstellt aber für je vier CCX eine Gruppe.
  Bei CPUs mit vielen CCX aus jeweils wenigen Kernen kann dies sinnvoll sein, um viele
  Gruppen zu vermeiden oder die Verteilung etwas zu glätten, wenn nicht alle Kerne verwendet
  werden. Beachten Sie, dass langsame Kommunikation zwischen CCX die Leistung dabei sehr
  stark beeinträchtigen kann. Im Allgemeinen wird davon abgeraten.

- group-by-4-clusters Wie "group-by-cluster", erstellt aber für je vier Cluster eine Gruppe.
  Bei CPUs mit vielen Clustern aus jeweils wenigen Kernen kann dies sinnvoll sein, um viele
  Gruppen zu vermeiden oder die Verteilung etwas zu glätten, wenn nicht alle Kerne verwendet
  werden. Beachten Sie, dass langsame Kommunikation zwischen Clustern die Leistung dabei sehr
  stark beeinträchtigen kann. Im Allgemeinen wird davon abgeraten.

- group-by-ccx Wenn weder "nbthread" noch "nbtgroups" gesetzt ist, wird für jeden CPU Core Complex
  ("CCX") mit verfügbaren CPUs eine Thread-Gruppe erzeugt, mit ebenso vielen Threads wie CPUs.
  Ein CCX fasst CPUs mit ähnlich schnellem Zugriff auf den Last Level Cache ("LLC") zusammen,
  typischerweise den L3-Cache. Auf den meisten modernen Rechnern ist es für die Leistung
  entscheidend, CPUs aus entfernten CCX nicht in derselben Thread-Gruppe zu mischen. Alle Threads
  einer Gruppe werden an alle CPUs des CCX gebunden. So bleibt die Kommunikation innerhalb der
  Gruppe lokal im CCX, ohne eine zu enge Bindung zu erzwingen. Die Grenzen für Threads pro Gruppe
  und für die Anzahl der Thread-Gruppen werden eingehalten. Dies wird für Systeme mit mehreren
  Sockeln und NUMA-Systeme sowie für CPUs mit hohen Latenzen zwischen CCX empfohlen.

- group-by-cluster Wenn weder "nbthread" noch "nbtgroups" gesetzt ist, wird für jeden CPU-Cluster
  mit verfügbaren CPUs eine Thread-Gruppe erzeugt, mit ebenso vielen Threads wie CPUs. Alle Threads
  einer Gruppe werden an alle CPUs des Clusters gebunden. So bleibt die Kommunikation innerhalb
  der Gruppe lokal im Cluster, ohne eine zu enge Bindung zu erzwingen. Die Grenzen für Threads pro
  Gruppe und für die Anzahl der Thread-Gruppen werden eingehalten. Dies wird für Systeme mit
  mehreren Sockeln und NUMA-Systeme sowie für CPUs mit hohen Latenzen zwischen CCX empfohlen.
  Auf den meisten Servern sind Cluster und CCX identisch. Auf heterogenen Rechnern ("performance"
  gegenüber "efficiency" oder "big" gegenüber "little") besteht ein Cluster dagegen meist nur aus
  einem Teil eines CCX mit sehr ähnlichen CPUs (gleicher Typ, maximal +/-5% Frequenzunterschied).
  Der Unterschied zeigt sich auf modernen Laptops und Desktop-Rechnern, auf denen Entwickler und
  Administratoren Konfigurationen prüfen.

- performance Wie "group-by-ccx" oben, allerdings werden CPU-Cluster ausgeschlossen, deren Kerne
  weniger als 80% der Leistung des nächstleistungsstärkeren Typs erreichen. Das sind typischerweise
  "little"- oder "efficient"-Kerne. Ihr Hinzufügen bringt im Allgemeinen wenig und kann leicht
  nachteilig sein (z. B. bei TLS-Handshakes). Häufig ist es deutlich wirksamer, solche Kerne für
  andere Aufgaben wie die Netzwerkverarbeitung freizuhalten. Auf Entwicklungssystemen können sie
  auch Hilfsprogramme wie Lastgeneratoren und Überwachungswerkzeuge ausführen. Dies ist die
  Standardrichtlinie.

- resource Wie "group-by-cluster" oben, allerdings wird nur der kleinste und effizienteste
  CPU-Cluster verwendet; alle anderen werden ignoriert. Damit lässt sich der Ressourcenverbrauch
  auf das kleinste Maß begrenzen, das noch angemessene Leistung liefert. Beispielsweise kann so
  der Energieverbrauch weiter gesenkt oder bei einer Sidecar-Konfiguration auf gemieteten Systemen
  die Zahl benötigter Kerne minimiert werden, um das System leichter verkleinern zu können.
  Ist nur ein Cluster vorhanden, wird dieser weiterhin vollständig verwendet.

Optional kann das Schlüsselwort "threads-per-core" hinzugefügt werden. Es akzeptiert "1" und
"auto". Bei 1 wird pro Kern nur ein Thread erzeugt, unabhängig von der Anzahl der Hardware-Threads
des Kerns. Bei auto wird pro Hardware-Thread ein Thread erzeugt. Ist keine Affinität angegeben und
wird threads-per-core 1 verwendet, ist die Affinität standardmäßig per-core.

Siehe auch: "cpu-map", "cpu-set", "nbthread"

<a id="entry-3-1-cpu-set"></a>

**`cpu-set <directive>...`**

```haproxy
cpu-set <directive>...
```

Erlaubt eine symbolische Beschreibung der CPU-Mengen, auf denen ausgeführt werden soll. Die
Direktive unterstützt folgende Schlüsselwörter: - reset hebt frühere Einschränkungen auf, die
beispielsweise von einem Dienstmanager oder einem "taskset"-Befehl geerbt wurden. - drop-cpu
`<set>` bindet nicht an CPUs dieser Menge - only-cpu `<set>` bindet nicht an CPUs außerhalb dieser
Menge - drop-node `<set>` bindet nicht an CPUs dieses NUMA-Knotens - only-node `<set>` bindet nicht
an CPUs außerhalb dieses NUMA-Knotens - drop-cluster `<set>` bindet nicht an CPUs mit dieser
Hardware-Cluster-Nummer - only-cluster `<set>` bindet nicht an CPUs mit anderen
Hardware-Cluster-Nummern - drop-core `<set>` bindet nicht an CPUs mit dieser Hardware-Kernnummer -
only-core `<set>` bindet nicht an CPUs mit anderen Hardware-Kernnummern - drop-thread `<set>`
bindet nicht an CPUs mit dieser Hardware-Thread-Nummer - only-thread `<set>` bindet nicht an CPUs
mit anderen Hardware-Thread-Nummern. Siehe auch: "cpu-policy"

<a id="entry-3-1-crt-base"></a>

**`crt-base <dir>`**

```haproxy
crt-base <dir>
```

Legt ein Standardverzeichnis zum Laden von SSL-Zertifikaten fest, wenn "crtfile" oder "crt" einen
relativen Pfad verwendet. Angegebene absolute Pfade haben Vorrang und ignorieren "crt-base".

<a id="entry-3-1-daemon"></a>

**`daemon`**

```haproxy
daemon
```

Lässt den Prozess per fork in den Hintergrund wechseln. Dies ist die empfohlene Betriebsart und
entspricht dem Befehlszeilenargument "-D". Mit "-db" in der Befehlszeile kann sie deaktiviert werden.
Im systemd-Modus wird diese Option ignoriert.

<a id="entry-3-1-default-path"></a>

**`default-path { current | config | parent | origin <path> }`**

```haproxy
default-path { current | config | parent | origin <path> }
```

Standardmäßig lädt HAProxy Dateien mit relativen Pfaden aus dem Verzeichnis, in dem der Prozess
gestartet wurde. Manchmal sollen alle relativen Pfade stattdessen von einem anderen Verzeichnis
ausgehen, als wäre der Prozess dort gestartet worden. Dafür ist diese Direktive vorgesehen.
Technisch führt sie während der Verarbeitung jeder Konfigurationsdatei vorübergehend chdir() zum
angegebenen Verzeichnis aus und kehrt nach jeder Datei in das ursprüngliche Verzeichnis zurück.
Ihr Argument legt die Richtlinie zum Laden von Dateien fest, deren Pfad nicht mit einem
Schrägstrich ('/') beginnt: - "current" lädt alle relativen Dateien aus dem Startverzeichnis des
Prozesses; dies ist der Standard.

    - "config" lädt alle relativen Dateien aus dem Verzeichnis der
      Konfigurationsdatei. Enthält deren Pfad einen Schrägstrich ('/'), wird
      der längste Teil bis zum letzten Schrägstrich als Zielverzeichnis
      verwendet, andernfalls das aktuelle Verzeichnis. Damit lassen sich
      Maps, Fehlerdateien, Zertifikate und Lua-Skripte als verschiebbare
      Pakete bündeln. Werden mehrere Konfigurationsdateien geladen, wird
      das Verzeichnis für jede Datei aktualisiert.

    - "parent" lädt alle relativen Dateien aus dem übergeordneten Verzeichnis
      des Verzeichnisses der Konfigurationsdatei. Enthält deren Pfad einen
      Schrägstrich ('/'), wird ".." an den längsten Teil bis zum letzten
      Schrägstrich angehängt und als Zielverzeichnis verwendet; andernfalls
      ist das Verzeichnis "..". So lassen sich Maps, Fehlerdateien,
      Zertifikate und Lua-Skripte als verschiebbare Pakete bündeln, deren
      Bestandteile in verschiedenen Unterverzeichnissen liegen
      (z. B. "config/", "certs/", "maps/", ...).

    - "origin" lädt alle relativen Dateien aus dem angegebenen (erforderlichen)
      Pfad. Dies kann die Verwaltung verschiedener HAProxy-Instanzen
      erleichtern, die parallel auf einem System laufen. Jede Instanz
      verwendet dabei ein anderes Präfix, während die übrigen Abschnitte
      leicht verschiebbar bleiben.

Jede Direktive "default-path" ersetzt sofort jede frühere und kann einen Wechsel in ein anderes
Verzeichnis bewirken. Auch wenn dies stets das gewünschte Verhalten ergeben sollte, ist die
Verwendung mehrerer default-path-Direktiven keine gute Praxis. Werden dennoch mehrere verwendet,
sollte die Richtlinie in allen Konfigurationsdateien einheitlich bleiben.

Warnung: Einige Konfigurationselemente wie Maps oder Zertifikate werden eindeutig über ihren
konfigurierten Pfad identifiziert. Bei einer verschiebbaren Verzeichnisstruktur können mehrere davon
denselben eindeutigen Namen erhalten. Das erschwert Aktualisierungen zur Laufzeit, insbesondere
wenn mehrere Konfigurationsdateien aus verschiedenen Verzeichnissen geladen werden. Vor der
Verwendung relativer Pfade ist ein strikt kollisionsfreies Schema für Dateinamen unbedingt
erforderlich. Ein robuster Ansatz wäre, allen Dateinamen den jeweiligen Standortnamen
voranzustellen oder dies auf Verzeichnisebene zu tun.

<a id="entry-3-1-description"></a>

**`description <text>`**

```haproxy
description <text>
```

Fügt einen Text hinzu, der die Instanz beschreibt.

Bestimmte Zeichen (beispielsweise #) müssen maskiert werden. Da der Text in eine HTML-Seite
eingefügt wird, sollten Sie die Zeichen "\<" und "\>" vermeiden.

<a id="entry-3-1-deviceatlas-json-file"></a>

**`deviceatlas-json-file <path>`**

```haproxy
deviceatlas-json-file <path>
```

Legt den Pfad der DeviceAtlas-JSON-Datendatei fest, die über die API geladen wird. Der Pfad muss auf
eine gültige JSON-Datendatei verweisen, auf die der HAProxy-Prozess zugreifen kann.

<a id="entry-3-1-deviceatlas-log-level"></a>

**`deviceatlas-log-level <value>`**

```haproxy
deviceatlas-log-level <value>
```

Legt den Informationsumfang fest, den die API zurückgibt. Diese Direktive ist optional; ohne
Angabe gilt der Standardwert 0.

<a id="entry-3-1-deviceatlas-properties-cookie"></a>

**`deviceatlas-properties-cookie <name>`**

```haproxy
deviceatlas-properties-cookie <name>
```

Legt den Namen des Client-Cookies für die Erkennung fest, wenn bei der Anfrage die clientseitige
DeviceAtlas-Komponente verwendet wurde. Diese Direktive ist optional; ohne Angabe gilt der
Standardwert DAPROPS.

<a id="entry-3-1-deviceatlas-separator"></a>

**`deviceatlas-separator <char>`**

```haproxy
deviceatlas-separator <char>
```

Legt das Trennzeichen für die Ergebnisse der API-Eigenschaften fest. Diese Direktive ist optional;
ohne Angabe gilt der Standardwert \|.

<a id="entry-3-1-dns-accept-family"></a>

**`dns-accept-family <family>[,...]`**

```haproxy
dns-accept-family <family>[,...]
```

Standardmäßig akzeptieren DNS-Resolver sowohl IPv4- als auch IPv6-Adressen. Dies lässt sich mit
"resolve-prefer" in server-Zeilen und dem Adressfamilienargument der Aktion "do-resolve"
beeinflussen. Es ist jedoch nur eine Präferenz: Ist ausschließlich die andere Familie vorhanden,
bleibt ihre Verwendung möglich. In Umgebungen ohne nutzbares Dual-Stack kann ein unerreichbarer,
nur auf IPv6 verweisender DNS-Eintrag erhebliche Probleme verursachen. Er ersetzt einen früheren
IPv4-Eintrag, der bis zur nächsten Anfrage möglicherweise weiter funktioniert hätte. Die globale
Option "dns-accept-family" kann die Verwendung nur einer oder beider Adressfamilien erzwingen.
Ihr Argument ist eine durch Kommas getrennte Liste folgender Wörter: - "ipv4": IPv4-Adressen
abfragen und akzeptieren ("A"-Einträge) - "ipv6": IPv6-Adressen abfragen und akzeptieren
("AAAA"-Einträge) - "auto": IPv4 verwenden; IPv6 zusätzlich verwenden, wenn das System dafür ein
Standardgateway besitzt. Das Ergebnis der letzten Prüfung wird 30 Sekunden lang zwischengespeichert.

Wird nur eine Familie verwendet, werden für die andere weder Anfragen an Resolver gesendet noch
Antworten berücksichtigt. Seit 3.3 ist "auto" der Standardwert. Damit werden tatsächlich erst dann
beide Familien aktiviert, wenn die Routbarkeit von IPv6 feststeht; andernfalls bleibt es bei IPv4.
Siehe auch: "resolve-prefer", "do-resolve"

<a id="entry-3-1-expose-deprecated-directives"></a>

**`expose-deprecated-directives`**

```haproxy
expose-deprecated-directives
```

Diese Anweisung muss vor einigen als veraltet gekennzeichneten Direktiven stehen, damit Warnungen
unterdrückt werden und die Konfigurationsdatei nicht abgewiesen wird. Betroffen sind nicht alle
veralteten Direktiven, sondern nur solche ohne alternative Lösung.

<a id="entry-3-1-expose-experimental-directives"></a>

**`expose-experimental-directives`**

```haproxy
expose-experimental-directives
```

Diese Anweisung muss vor als experimentell gekennzeichneten Direktiven stehen, sonst wird die
Konfigurationsdatei abgewiesen. Die von dieser Option erfassten Funktionen arbeiten nicht garantiert
zuverlässig und können während des Wartungszyklus funktionsunfähig werden. Während der Arbeit an
der nächsten Version pflegen die Entwickler sie nach bestem Bemühen und unternehmen angemessene
Anstrengungen, ihre Funktionsfähigkeit zu erhalten, geben aber keine Garantie. Deshalb ist für
diese Funktionen keine Unterstützung über das Erscheinen der nächsten LTS-Version hinaus zu
erwarten. Von Benutzern, die experimentelle Funktionen erproben möchten, wird erwartet, dass sie
zeitnah aktualisieren, um deren Verbesserungen zu erhalten. Ob diese Direktive noch benötigt wird, lässt sich leicht erkennen:
Ist sie aktiviert, ohne von einer solchen Funktion verwendet zu werden, weist eine Warnung darauf
hin, sie zu deaktivieren. Bleibt die Warnung aus, wird sie also noch benötigt.

<a id="entry-3-1-external-check"></a>

**`external-check [preserve-env]`**

```haproxy
external-check [preserve-env]
```

Erlaubt einen externen Agenten für Health Checks. Als Sicherheitsmaßnahme ist dies standardmäßig
deaktiviert. Selbst bei Aktivierung können Prüfungen weiterhin fehlschlagen, wenn nicht auch
"insecure-fork-wanted" aktiviert ist. Verwendet das gestartete Programm eine ausführbare Datei
mit setuid (was es wirklich nicht tun sollte), muss möglicherweise auch "insecure-setuid-wanted"
im globalen Abschnitt gesetzt werden. Standardmäßig starten Prüfungen mit einer bereinigten Umgebung,
die nur Variablen aus dem Befehl "external-check" im Backend-Abschnitt enthält. Manchmal soll die
Umgebung dennoch erhalten bleiben, etwa wenn komplexe Skripte daraus zusätzliche Pfade oder
Informationen beziehen. Dafür kann das Schlüsselwort "preserve-env" angehängt werden. Dann wird
jedoch dringend davon abgeraten, setuid-Programme auszuführen oder Prüfungen unter einem
privilegierten Benutzer laufen zu lassen, da das Prüfprogramm sonst möglichen Angriffen ausgesetzt ist. Weitere Einzelheiten
finden Sie bei "option
external-check", "insecure-fork-wanted" und "insecure-setuid-wanted".

<a id="entry-3-1-fd-hard-limit"></a>

**`fd-hard-limit <number>`**

```haproxy
fd-hard-limit <number>
```

Setzt unabhängig von Systemgrenzen eine Obergrenze für die Anzahl der vom Prozess verwendeten
Dateideskriptoren. Mit "ulimit-n" und "maxconn" kann ein Wert erzwungen werden. Sind beide nicht
gesetzt, gilt die harte Grenze von RLIMIT_NOFILE, wie sie "ulimit -n -H" ausgibt. Einige moderne
Betriebssysteme erlauben hier jedoch extrem große Werte (in der Größenordnung von 1 Milliarde),
die im normalen Betrieb viel zu viel RAM verbrauchen würden. Mit fd-hard-limit kann eine
gegebenenfalls niedrigere Obergrenze durchgesetzt werden. Systemgrenzen unterhalb von `<number>`
werden also immer eingehalten; bei höheren Systemgrenzen gilt der angegebene Wert. Standardmäßig
ist fd-hard-limit auf 1048576 gesetzt. Dieser Standard kann beim Kompilieren über DEFAULT_MAXFD
geändert werden. Der Wert kann als maximale Systemgrenze (des Kernels) dienen, wenn die harte
RLIMIT_NOFILE-Grenze extrem groß ist. fd-hard-limit im globalen Abschnitt kann den beim Bauen über
DEFAULT_MAXFD vorgegebenen Wert vorübergehend überschreiben. Im folgenden Beispiel ist keine andere
Einstellung gesetzt; maxconn passt sich automatisch dem kleineren Wert aus "fd-hard-limit" und
der RLIMIT_NOFILE-Grenze an:

```text
global
    # use as many FDs as possible but no more than 50000
    fd-hard-limit 50000
```

Siehe auch: ulimit-n, maxconn

<a id="entry-3-1-gid"></a>

**`gid <number>`**

```haproxy
gid <number>
```

Ändert die Gruppen-ID des Prozesses auf `<number>`. Es wird empfohlen, diese Gruppen-ID
HAProxy oder einer kleinen Gruppe ähnlicher Daemons vorzubehalten. HAProxy muss unter einem
Benutzer dieser Gruppe oder mit Superuser-Rechten gestartet werden. Hat der startende Benutzer
zusätzliche Gruppen, kann HAProxy diese nur ablegen, wenn es mit Superuser-Rechten gestartet wurde.
Siehe auch "group" und "uid".

<a id="entry-3-1-grace"></a>

**`grace <time>`**

```haproxy
grace <time>
```

Definiert eine Verzögerung zwischen SIGUSR1 und dem tatsächlichen geordneten Herunterfahren.

Argumente:

```text
<time>  ist eine zusätzliche Wartezeit (standardmäßig in Millisekunden)
        nach dem Empfang des Signals SIGUSR1, die vor dem Fortsetzen
        des geordneten Beendens abgewartet wird.
```

Dies dient der Kompatibilität mit älteren Umgebungen, in denen der haproxy-Prozess gestoppt werden
muss, externe Komponenten den Status aber noch vor dem Freigeben der Listener erkennen müssen.
Dabei wird die interne Variable "stopping" (ausgegeben von der Sample-Abruffunktion "stopping")
auf true gesetzt, während die Listener weiterhin ungestört Verbindungen annehmen. Erst nach Ablauf
der Verzögerung beginnt das normale geordnete Herunterfahren. Dies darf nicht für Prozesse
verwendet werden, die neu geladen werden: Der alte Prozess wird seine Bindungen sonst nicht
freigeben; der neue kann möglicherweise nicht starten, oder es können andere Probleme entstehen.

Beispiel:

```shell
global
  grace 10s

# Returns 200 OK until stopping is set via SIGUSR1
frontend ext-check
  bind :9999
  monitor-uri /ext-check
  monitor fail if { stopping }
```

Ein flexiblerer und dauerhafterer Ansatz wäre, dass ein Orchestrierungssystem über die CLI eine
globale Variable setzt, diese für Antworten auf externe Prüfungen verwendet und erst nach einer
Verzögerung SIGUSR1 sendet.

Beispiel:

```shell
# Returns 200 OK until proc.stopping is set to non-zero. May be done
# from HTTP using set-var(proc.stopping) or from the CLI using:
# > set var proc.stopping int(1)
frontend ext-check
  bind :9999
  monitor-uri /ext-check
  monitor fail if { var(proc.stopping) -m int gt 0 }
```

Siehe auch: hard-stop-after, monitor

<a id="entry-3-1-group"></a>

**`group <group name>`**

```haproxy
group <group name>
```

Ähnlich wie "gid", verwendet aber die GID des Gruppennamens `<group name>` aus /etc/group.
Siehe auch "gid" und "user".

<a id="entry-3-1-h1-accept-payload-with-any-method"></a>

**`h1-accept-payload-with-any-method`**

```haproxy
h1-accept-payload-with-any-method
```

Weist HTTP/1.0-Anfragen mit GET/HEAD/DELETE und einer Nutzlast nicht mit der HTTP-Antwort
413 Payload Too Large zurück.

Während HTTP/1.1 dies ausdrücklich erlaubt, ist HTTP/1.0 hier nicht eindeutig. Einige ältere
Server erwarten keine Nutzlast und prüfen niemals die Länge des Inhalts (über Content-Length-
oder Transfer-Encoding-Header). Manche Zwischenstationen verarbeiten die Nutzlast von
HTTP/1.0-GET/HEAD/DELETE-Anfragen daher korrekt, andere ignorieren sie vollständig. Das kann
Sicherheitsprobleme verursachen, da Request-Smuggling-Angriffe möglich sind. Standardmäßig weist
HAProxy HTTP/1.0-GET/HEAD/DELETE-Anfragen mit Nutzlast deshalb zurück.

Bei einigen alten Clients kann dies jedoch Probleme verursachen. In diesem Fall kann diese
globale Option gesetzt werden.

<a id="entry-3-1-h1-do-not-close-on-insecure-transfer-encoding"></a>

**`h1-do-not-close-on-insecure-transfer-encoding`**

```haproxy
h1-do-not-close-on-insecure-transfer-encoding
```

Nach der HTTP/1.1-Spezifikation (RFC9112#6.1) stellt das gleichzeitige Vorhandensein von
Transfer-Encoding und Content-Length in derselben Nachricht ein erhebliches Risiko für
Content-Smuggling-Angriffe dar, wenn sich irgendwo in der vor- oder nachgelagerten Kette ein
HTTP/1.0-Agent befindet. Ein Agent muss die Verbindung in diesem Fall nach der Antwort unbedingt
schließen, um jede Ausnutzung zu verhindern. Das kann bei sehr alten Clients jedoch die Leistung
beeinträchtigen, insbesondere wenn sie für jede Anfrage eine TLS-Verbindung neu aushandeln müssen.
Diese Option weist HAProxy an, die Regel nicht durchzusetzen, sondern die Nachricht lediglich zu
bereinigen und die Verbindung nach der Antwort offen zu halten. Dies darf nur erfolgen, wenn
absolut sicher ist, dass keine HTTP/1.0-Agenten in der Kette vorhanden sind und alle Implementierungen
vor HAProxy die HTTP/1.1-Regeln zu diesen Header-Feldern vollständig einhalten. In jedem Fall
ignoriert und entfernt HAProxy weiterhin den überflüssigen Content-Length-Header, um die nächste
Station nicht zu verwirren.

Wird diese Option wegen eines alten fehlerhaften Clients oder Servers aktiviert, ist Folgendes
wichtig: Unabhängig davon, ob die Option nötig ist, riskiert ein Agent, der diese Regel verletzt,
dass ältere Agenten seine Nachrichten abschneiden. Diese würden Content-Length berücksichtigen
und Transfer-Encoding ignorieren, obwohl die summierte Größe der codierten Chunk-Längenangaben
nicht darin enthalten ist. Die obige Regel dient also nicht nur der Sicherheit, sondern auch dazu,
Agenten auszusondern, die wegen Inkompatibilitäten mit älteren Agenten Kommunikationsprobleme haben
können.

<a id="entry-3-1-h1-case-adjust"></a>

**`h1-case-adjust <from> <to>`**

```haproxy
h1-case-adjust <from> <to>
```

Definiert die Anpassung der Groß- und Kleinschreibung für den Header-Namen `<from>`, sofern
aktiviert. Vor dem Senden an HTTP/1-Clients oder -Server wird er in `<to>` geändert. `<from>` muss
kleingeschrieben sein; `<from>` und `<to>` dürfen sich nur in der Groß- und Kleinschreibung
unterscheiden. Für mehrere Header-Namen kann die Direktive wiederholt werden. Doppelte Einträge
sind nicht zulässig. Müssen viele Header-Namen angepasst werden, ist "h1-case-adjust-file"
möglicherweise praktischer. Beachten Sie, dass ohne "option h1-case-adjust-bogus-client" oder
"option h1-case-adjust-bogus-server" in einem Proxy keine Umwandlung erfolgt.

Es gibt keine standardisierte Groß- und Kleinschreibung für Header-Namen, da sie gemäß RFC7230
unabhängig davon verglichen werden. Anwendungen müssen sie daher ohne Unterscheidung der Groß- und
Kleinschreibung verarbeiten. Einige fehlerhafte Anwendungen verletzen jedoch die Standards und
verlassen sich auf die von Browsern meist verwendete Schreibweise. Bei HTTP/2 wird dies kritisch,
da alle Header-Namen kleingeschrieben übertragen werden müssen. HAProxy folgt derselben Konvention:
Unabhängig von der HTTP-Version werden alle Header-Namen kleingeschrieben an Clients und Server
gesendet.

Anwendungen, die Anfragen oder Antworten nicht korrekt verarbeiten, benötigen solche Umgehungslösungen
möglicherweise vorübergehend, um die an sie gesendeten Header-Namen bis zur Fehlerbehebung anzupassen.
Beachten Sie, dass eine Anwendung, die dies benötigt, für Content-Smuggling-Angriffe anfällig sein
könnte und unbedingt korrigiert werden muss.

Beispiel:

```text
global
  h1-case-adjust content-length Content-Length
```

Siehe "h1-case-adjust-file", "option h1-case-adjust-bogus-client" und "option
h1-case-adjust-bogus-server".

<a id="entry-3-1-h1-case-adjust-file"></a>

**`h1-case-adjust-file <hdrs-file>`**

```haproxy
h1-case-adjust-file <hdrs-file>
```

Definiert eine Datei mit Schlüssel-Wert-Paaren, um die Groß- und Kleinschreibung bestimmter
Header-Namen vor dem Senden an HTTP/1-Clients oder -Server anzupassen. Die Datei `<hdrs-file>` muss
pro Zeile 2 Header-Namen enthalten. Der erste muss kleingeschrieben sein; beide dürfen sich nur in
der Groß- und Kleinschreibung unterscheiden. Zeilen mit '#' am Anfang und Leerzeilen werden
ignoriert. Führende und abschließende Tabulatoren und Leerzeichen werden entfernt. Doppelte
Einträge sind nicht zulässig. Ohne "option h1-case-adjust-bogus-client" oder
"option h1-case-adjust-bogus-server" in einem Proxy erfolgt keine Umwandlung.

Wird diese Direktive wiederholt, wird nur die letzte verarbeitet. Sie ist eine Alternative zu
"h1-case-adjust", wenn viele Header-Namen angepasst werden müssen. Bitte lesen Sie die Hinweise
zu den damit verbundenen Risiken.

Siehe "h1-case-adjust", "option h1-case-adjust-bogus-client" und "option h1-case-adjust-bogus-server".

<a id="entry-3-1-h2-workaround-bogus-websocket-clients"></a>

**`h2-workaround-bogus-websocket-clients`**

```haproxy
h2-workaround-bogus-websocket-clients
```

Deaktiviert die Bekanntgabe der Unterstützung für h2-Websockets an Clients. Dies kann Probleme
mit Clients umgehen, die Schwierigkeiten mit der Implementierung des noch relativ neuen RFC8441
haben, etwa Firefox
88. Damit Clients für den Websocket-Tunnel automatisch auf http/1.1 zurückfallen
können, geben Sie h2-Unterstützung in der bind-Zeile mit "alpn" ohne explizites Schlüsselwort
"proto" an. Wurde diese Anweisung zuvor aktiviert, lässt sie sich mit dem vorangestellten
Schlüsselwort "no" deaktivieren.

<a id="entry-3-1-hard-stop-after"></a>

**`hard-stop-after <time>`**

```haproxy
hard-stop-after <time>
```

Definiert die maximal zulässige Zeit für ein sauberes, geordnetes Herunterfahren.

Argumente:

```text
<time>  ist die maximale Zeit (standardmäßig in Millisekunden), die die
        Instanz nach einer über das Signal SIGUSR1 empfangenen Aufforderung
        zum geordneten Beenden noch weiterläuft.
```

Damit lässt sich sicherstellen, dass die Instanz auch dann beendet wird, wenn während eines Soft-Stops Verbindungen offen bleiben (beispielsweise bei langen Zeitüberschreitungen für einen Proxy im TCP-Modus). Dies gilt sowohl im TCP- als auch im HTTP-Modus.

Beispiel:

```text
global
  hard-stop-after 30s
```

Siehe auch: grace

<a id="entry-3-1-harden-reject-privileged-ports-tcp"></a>

**`harden.reject-privileged-ports.tcp { on | off }`**

```haproxy
harden.reject-privileged-ports.tcp { on | off }
harden.reject-privileged-ports.quic { on | off }
```

Schaltet für jedes Protokoll einen Schutz ein oder aus, der die Kommunikation mit Clients verbietet, die privilegierte Ports als Quellport verwenden. Dieser Portbereich ist in RFC 6335 definiert. Standardmäßig ist der Schutz für das QUIC-Protokoll aktiv, da dieses Verhalten verdächtig ist und für Spoofing- oder DNS/NTP-Amplifikationsangriffe genutzt werden kann.

<a id="entry-3-1-http-err-codes"></a>

**`http-err-codes [+-]<range>[,...] [...]`**

```haproxy
http-err-codes [+-]<range>[,...] [...]
```

Ersetzt, verkleinert oder erweitert die Liste der Statuscodes, die für die Beendigungscodes und den Zähler "http_err_cnt" in Stick-Tabellen einen Fehler kennzeichnen. Der Standardbereich für Fehler reicht von 400 bis 499. In bestimmten Situationen ziehen es jedoch einige Benutzer vor, bestimmte Codes auszuschließen, insbesondere beim Erfassen von Clientfehlern (z. B. 404 auf Systemen mit dynamisch erzeugten Inhalten). Siehe auch "http-fail-codes" und "http_err_cnt".

Ein Bereich ohne vorangestelltes '+' oder '-' ersetzt den vorhandenen Bereich durch den neuen. Ein Bereich mit vorangestelltem '+' erweitert den vorhandenen Bereich um den angegebenen Bereich; dieser darf sich mit dem vorhandenen Bereich überschneiden, muss es aber nicht. Ein Bereich mit vorangestelltem '-' entfernt den angegebenen Bereich aus dem vorhandenen. Ein Bereich besteht aus einer Zahl von 100 bis 599, auf die optional "-" und eine weitere Zahl folgen, die mindestens so groß wie die erste ist und die Obergrenze des Bereichs angibt. Mehrere Bereiche für dieselbe Operation zum Hinzufügen, Entfernen oder Ersetzen können durch Kommas getrennt werden.

Beispiel:

```text
http-err-codes 400,402-444,446-480,490   # sets exactly these codes
http-err-codes 400-499 -450 +500         # sets 400 to 500 except 450
http-err-codes -450-459                  # removes 450 to 459 from range
http-err-codes +501,505                  # adds 501 and 505 to range
```

<a id="entry-3-1-http-fail-codes"></a>

**`http-fail-codes [+-]<range>[,...] [...]`**

```haproxy
http-fail-codes [+-]<range>[,...] [...]
```

Ersetzt, verkleinert oder erweitert die Liste der Statuscodes, die für die Beendigungscodes und den Zähler "http_fail_cnt" in Stick-Tabellen einen Fehlschlag kennzeichnen. Der Standardbereich für Fehlschläge reicht von 500 bis 599, mit Ausnahme von 501 und 505, die durch Clients ausgelöst werden können. Diese Codes zeigen normalerweise an, dass der Server die Anfrage nicht verarbeiten konnte. Einige Benutzer ziehen es vor, bestimmte Codes in Situationen auszuschließen, in denen diese bekanntermaßen nicht relevant sind, beispielsweise 500 in bestimmten SOAP-Umgebungen, wo dieser Code keinen Serverfehler ausdrückt. Die Syntax ist genau dieselbe wie bei http-err-codes oben. Siehe auch "http-err-codes" und "http_fail_cnt".

<a id="entry-3-1-insecure-fork-wanted"></a>

**`insecure-fork-wanted`**

```haproxy
insecure-fork-wanted
```

Standardmäßig versucht HAProxy mit allen verfügbaren Mitteln zu verhindern, dass nach dem Start weitere Threads oder Prozesse erzeugt werden. Dies ist besonders wichtig bei Lua-Dateien unklarer Herkunft und beim Experimentieren mit Entwicklungsversionen, die noch Fehler enthalten können, deren Ausnutzbarkeit unklar ist. Generell ist es eine sinnvolle Vorsichtsmaßnahme, sicherzustellen, dass Datenverkehr keine unerwarteten Hintergrundaktivitäten auslösen kann. Allerdings verhindert dies die Ausführung externer Prüfungen und kann bestimmte, sehr spezielle Lua-Skripte beeinträchtigen, die ausdrücklich auf die Möglichkeit zum Forken angewiesen sind. Diese Option dient dazu, den Schutz zu deaktivieren. Beachten Sie, dass dies keine gute Idee ist: Eine Schwachstelle in einer Bibliothek oder in HAProxy selbst lässt sich bei deaktiviertem Schutz leichter ausnutzen. Außerdem ist das Forken aus Lua oder an anderer Stelle unzuverlässig, da der durch Fork erzeugte Prozess zufällig eine von einem anderen Thread gesetzte Sperre übernehmen kann und dann einen Vorgang niemals abschließen kann. Daher wird dringend empfohlen, diese Option niemals zu verwenden und jede Arbeitslast, die einen solchen Fork benötigt, zu überdenken und auf eine sicherere Lösung umzustellen (beispielsweise Agenten anstelle externer Prüfungen). Diese Option unterstützt das Präfix "no", um sie zu deaktivieren. Sie kann auch mit "-dI" in der haproxy-Befehlszeile aktiviert werden.

<a id="entry-3-1-insecure-setuid-wanted"></a>

**`insecure-setuid-wanted`**

```haproxy
insecure-setuid-wanted
```

HAProxy muss zur Laufzeit keine ausführbaren Programme aufrufen (außer bei externen Prüfungen, von denen dringend abgeraten wird) und soll sich sogar in einer leeren chroot-Umgebung isolieren. Daher gibt es grundsätzlich keinen triftigen Grund, den Aufruf eines ausführbaren setuid-Programms zu erlauben, ohne dass sich der Benutzer der Risiken vollständig bewusst ist. Wenn HAProxy externe Prüfungen aufrufen und/oder chroot deaktivieren muss, könnte das Ausnutzen einer Schwachstelle in einer Bibliothek oder in HAProxy selbst zur Ausführung eines externen Programms führen. Unter Linux lässt sich der Prozess so einschränken, dass ein auf einem solchen Programm gesetztes setuid-Bit ignoriert wird. Dies verringert das Risiko einer Rechteausweitung in dieser Situation erheblich. HAProxy tut dies standardmäßig. Falls dies bei einer externen Prüfung Probleme verursacht (beispielsweise wenn sie den Befehl "ping" benötigt), kann dieser Schutz durch explizites Hinzufügen dieser Direktive im globalen Abschnitt deaktiviert werden. Ist die Direktive aktiviert, lässt sie sich durch Voranstellen des Schlüsselworts "no" wieder deaktivieren.

<a id="entry-3-1-issuers-chain-path"></a>

**`issuers-chain-path <dir>`**

```haproxy
issuers-chain-path <dir>
```

Legt ein Verzeichnis fest, aus dem Zertifikatsketten zur Vervollständigung der Ausstellerkette geladen werden. Alle Dateien müssen im PEM-Format vorliegen. Wenn bei Zertifikaten, die mit "crt" oder "crt-list" geladen werden, die Zertifikatskette (auch als Zwischenzertifikat bekannt) nicht in der PEM-Datei enthalten ist, vervollständigt HAProxy die Kette, sofern der Aussteller des Zertifikats dem ersten Zertifikat der mit "issuers-chain-path" geladenen Kette entspricht. Eine "crt"-Datei mit PrivateKey+Certificate+IntermediateCA2+IntermediateCA1 könnte durch PrivateKey+Certificate ersetzt werden. HAProxy vervollständigt die Kette, wenn im Verzeichnis "issuers-chain-path" eine Datei mit IntermediateCA2+IntermediateCA1 vorhanden ist. Alle anderen Zertifikate mit demselben Aussteller teilen sich die Kette im Speicher.

Die OCSP-Funktionen können die vervollständigte Kette verwenden, wenn keine .issuer-Datei verwendet wurde oder keine Kette in der PEM-Datei enthalten war.

<a id="entry-3-1-jwt-allow-none-alg"></a>

**`jwt.allow_none_alg`**

```haproxy
jwt.allow_none_alg
```

Erlaubt JWT-Token mit dem Algorithmus "none" im Konverter 'jwt_verify'. Wenn diese Option gesetzt ist, gelten diese Token immer als gültig. Standardmäßig werden unsignierte Token abgelehnt, da sie als unsicher gelten (siehe RFC8725 [Abschnitt 3.1](https://www.rfc-editor.org/rfc/rfc8725#section-3.1)).

<a id="entry-3-1-jwt-decrypt-alg-list"></a>

**`jwt.decrypt_alg_list <list>`**

```haproxy
jwt.decrypt_alg_list <list>
```

Legt die Liste der in den Konvertern jwt_decrypt_XXX erlaubten Algorithmen fest. JWT-Tokens mit einem nicht unterstützten oder deaktivierten Algorithmus werden niemals entschlüsselt. Die angegebenen Algorithmen müssen dasselbe Format wie in [Abschnitt 4.1](https://www.rfc-editor.org/rfc/rfc7518#section-4.1) von RFC7518 haben und durch Doppelpunkte getrennt werden. Mit dem besonderen Namen "ALL" können alle unterstützten Algorithmen aktiviert werden (eine vollständige Liste finden Sie beim Konverter "jwt_decrypt_jwk"); einem Algorithmusnamen kann ein '!' hinzugefügt werden, um ihn ausdrücklich zu deaktivieren. Beachten Sie, dass diese Option alle Algorithmen deaktiviert, die nicht ausdrücklich in der angegebenen Liste aufgeführt sind, sofern nicht "ALL" angegeben wird.

Beispiele:

```shell
# Enable all algorithms but the "ECDH-ES" one
jwt.decrypt_alg_list ALL:!ECDH-ES

# Only enable ECDH-ES algorithms
jwt.decrypt_alg_list ECDH-ES:ECDH-ES+A128KW:ECDH-ES+A192KW:ECDH-ES+A256KW
```

<a id="entry-3-1-jwt-decrypt-enc-list"></a>

**`jwt.decrypt_enc_list <list>`**

```haproxy
jwt.decrypt_enc_list <list>
```

Legt die Liste der in den Konvertern jwt_decrypt_XXX erlaubten Verschlüsselungsalgorithmen fest. JWT-Tokens mit einem nicht unterstützten oder deaktivierten Verschlüsselungsalgorithmus werden niemals entschlüsselt. Die angegebenen Algorithmen müssen dasselbe Format wie in [Abschnitt 5.1](https://www.rfc-editor.org/rfc/rfc7518#section-5.1) von RFC7518 haben und durch Doppelpunkte getrennt werden. Mit dem besonderen Namen "ALL" können alle unterstützten Algorithmen aktiviert werden (eine vollständige Liste finden Sie beim Konverter "jwt_decrypt_jwk"); einem Algorithmusnamen kann ein '!' hinzugefügt werden, um ihn ausdrücklich zu deaktivieren. Beachten Sie, dass diese Option alle Algorithmen deaktiviert, die nicht ausdrücklich in der angegebenen Liste aufgeführt sind, sofern nicht "ALL" angegeben wird.

Beispiele:

```shell
# Enable only AES GCM encrypting algorithms
jwt.decrypt_enc_list A128GCM:A192GCM:A256GCM
```

<a id="entry-3-1-key-base"></a>

**`key-base <dir>`**

```haproxy
key-base <dir>
```

Legt ein Standardverzeichnis fest, aus dem private SSL-Schlüssel geladen werden, wenn bei "key"-Direktiven ein relativer Pfad verwendet wird. Angegebene absolute Pfade haben Vorrang und ignorieren "key-base". Diese Option funktioniert nur mit einer load-Zeile in einem crt-store.

<a id="entry-3-1-limited-quic"></a>

**`limited-quic`**

```haproxy
limited-quic
```

Diese Einstellung muss verwendet werden, um QUIC-Listener-Bindungen ausdrücklich zu aktivieren, wenn haproxy mit einer OpenSSL-Version ohne QUIC-Unterstützung kompiliert wurde. Sie aktiviert eine interne Kompatibilitätsschicht von haproxy, die beim Kompilieren mit USE_QUIC_OPENSSL_COMPAT=1 ausgewählt worden sein muss. Diese Kompatibilitätsschicht unterstützt die meisten erforderlichen TLS-Operationen, allerdings ohne QUIC 0-RTT.

Diese Funktion richtet sich hauptsächlich an OpenSSL vor Version 3.5.2, wo die QUIC-API noch nicht oder nur teilweise implementiert war. Die Kompatibilitätsschicht lässt sich auch für Version 3.5.2 und höher aktivieren, was aber vermutlich unnötig ist.

Wenn limited-quic gesetzt ist, die Kompatibilitätsschicht beim Kompilieren aber nicht ausgewählt wurde, wird die Option ohne Meldung ignoriert, und die QUIC-TLS-Operationen verwenden die TLS-Bibliothek.

<a id="entry-3-1-localpeer"></a>

**`localpeer <name>`**

```haproxy
localpeer <name>
```

Legt den Peer-Namen der lokalen Instanz fest. Die Option wird ignoriert, wenn das Befehlszeilenargument "-L" angegeben wurde oder wenn sie nach "peers"-Abschnittsdefinitionen verwendet wird. In diesen Fällen wird beim Einlesen der Konfiguration eine Warnung ausgegeben.

Diese Option setzt außerdem die Umgebungsvariable HAPROXY_LOCALPEER. Siehe auch "-L" im Verwaltungshandbuch und den Abschnitt "peers" weiter unten.

<a id="entry-3-1-log"></a>

**`log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]`**

```haproxy
log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]
    [profile <prof>] <facility> [max level [min level]]
```

Fügt einen globalen Syslog-Server hinzu. Es können mehrere globale Server definiert werden. Sie erhalten Protokollmeldungen zu Starts und Beendigungen sowie alle Protokollmeldungen von Proxys, die mit "log global" konfiguriert sind. Weitere Einzelheiten finden Sie bei der Option "log" für Proxys.

<a id="entry-3-1-log-send-hostname"></a>

**`log-send-hostname [<string>]`**

```haproxy
log-send-hostname [<string>]
```

Legt das Hostnamenfeld im Syslog-Header fest. Wenn der optionale Parameter "string" gesetzt ist, erhält das Feld den Inhalt dieser Zeichenfolge; andernfalls wird der Hostname des Systems verwendet. Dies wird meist verwendet, wenn Protokollmeldungen nicht über einen zwischengeschalteten Syslog-Server weitergeleitet werden oder wenn lediglich der in den Protokollen ausgegebene Hostname angepasst werden soll.

<a id="entry-3-1-log-tag"></a>

**`log-tag <string>`**

```haproxy
log-tag <string>
```

Setzt das Tag-Feld im Syslog-Header auf diese Zeichenfolge. Standardmäßig wird der Programmname verwendet, mit dem das Programm über die Befehlszeile gestartet wurde; dieser ist üblicherweise "haproxy". Manchmal kann es sinnvoll sein, damit mehrere auf demselben Host laufende Prozesse zu unterscheiden. Siehe auch die pro Proxy einstellbare Direktive "log-tag".

<a id="entry-3-1-lua-load"></a>

**`lua-load <file> [ <arg1> [ <arg2> [ ... ] ] ]`**

```haproxy
lua-load <file> [ <arg1> [ <arg2> [ ... ] ] ]
```

Diese globale Direktive lädt eine Lua-Datei und führt sie im gemeinsamen Kontext aus, der für alle Threads sichtbar ist. Jede in diesem Kontext gesetzte Variable ist für jeden Thread sichtbar. Dies ist die einfachste und empfohlene Methode, Lua-Programme zu laden, skaliert bei vielen Lua-Aufrufen jedoch nicht gut, da jeweils nur ein Thread mit dem globalen Zustand arbeiten kann. Ein so geladenes Programm sieht in der Variablen "core.thread" immer den Wert 0. Diese Direktive kann mehrfach verwendet werden.

Die Argumente sind in der Lua-Datei über den folgenden Code im Dateirumpf verfügbar. Denken Sie daran, dass Lua-Arrays mit dem Index 1 beginnen. Eine in einer Datei deklarierte "local"-Variable ist in der gesamten Datei verfügbar, in anderen Dateien jedoch nicht.

     local args = table.pack(...)

<a id="entry-3-1-lua-load-per-thread"></a>

**`lua-load-per-thread <file> [ <arg1> [ <arg2> [ ... ] ] ]`**

```haproxy
lua-load-per-thread <file> [ <arg1> [ <arg2> [ ... ] ] ]
```

Diese globale Direktive lädt eine Lua-Datei in jeden gestarteten Thread und führt sie dort aus. Globale Variablen sind nur innerhalb des jeweiligen Threads sichtbar, sodass jeder Thread einen anderen Wert sehen kann. Daher wird dringend empfohlen, in so geladenen Programmen keine globalen Variablen zu verwenden. Für jeden Thread wird eine unabhängige Kopie geladen und initialisiert; alles erfolgt nacheinander und in der numerischen Reihenfolge der Threads von 1 bis nbthread. Falls bestimmte Operationen nur einmal ausgeführt werden müssen, sollte das Programm anhand der Variablen "core.thread" prüfen, welcher Thread gerade initialisiert wird. So geladene Programme laufen gleichzeitig auf allen Threads und sind sehr gut skalierbar. Dies ist die empfohlene Methode zum Laden einfacher Funktionen, die Sample-Fetches, Konverter, Aktionen oder Dienste registrieren, sobald feststeht, dass das Programm nicht von globalen Variablen abhängt. Der Einfachheit halber steht die Direktive auch dann zur Verfügung, wenn nur ein Thread verwendet wird oder Threads deaktiviert sind (in diesem Fall entspricht sie lua-load). Diese Direktive kann mehrfach verwendet werden.

Zur Verwendung von Argumenten siehe lua-load.

<a id="entry-3-1-lua-prepend-path"></a>

**`lua-prepend-path <string> [<type>]`**

```haproxy
lua-prepend-path <string> [<type>]
```

Stellt die angegebene Zeichenfolge, gefolgt von einem Semikolon, der Lua-Variablen package.`<type>` voran. `<type>` muss entweder "path" oder "cpath" sein. Wenn `<type>` nicht angegeben wird, ist der Standardwert "path".

Die Pfade von Lua sind durch Semikolons getrennte Listen von Mustern, die bestimmen, wie die Funktion `require` nach der Quelldatei einer Bibliothek sucht. Fragezeichen (?) innerhalb eines Musters werden durch den Modulnamen ersetzt. Der Pfad wird von links nach rechts ausgewertet. Somit werden später vorangestellte Pfade früher geprüft.

Beispielsweise bei Angabe des folgenden Pfads:

```text
lua-prepend-path /usr/share/haproxy-lua/?/init.lua
lua-prepend-path /usr/share/haproxy-lua/?.lua
```

Beim Aufruf von `require "example"` versucht Lua zunächst, das Skript /usr/share/haproxy-lua/example.lua zu laden. Falls es nicht vorhanden ist, wird /usr/share/haproxy-lua/example/init.lua versucht. Falls auch dieses nicht vorhanden ist, werden die Standardpfade geprüft.

Einzelheiten finden Sie in der Lua-Dokumentation unter <https://www.lua.org/pil/8.1.html>.

<a id="entry-3-1-master-worker"></a>

**`master-worker (deprecated)`**

```haproxy
master-worker (deprecated)
```

Master-Worker-Modus. Er entspricht dem Befehlszeilenargument "-W".

Dieses Schlüsselwort ist veraltet. Starten Sie den Master-Worker-Modus stattdessen mit "-W" oder "-Ws".

Dieser Modus startet einen "master", der nach dem Einlesen der Konfiguration mittels Fork einen "worker" zur Verarbeitung des Datenverkehrs erzeugt. Der Master dient als Prozessmanager, der die "workers" überwacht.

In diesem Modus können Sie HAProxy direkt neu laden, indem Sie dem Master das Signal SIGUSR2 senden. Beim Neuladen wird der Master aufgefordert, die Konfiguration erneut einzulesen und mittels Fork einen neuen Worker zu erzeugen. Der bisherige Worker bleibt bis zum Ende seiner Aufgaben erhalten.

Der Master-Worker-Modus ist sowohl mit dem Vordergrund- als auch mit dem Daemon-Modus kompatibel.

Wenn ein Worker mit einem Fehlercode beendet wird, etwa wegen eines Segmentierungsfehlers, werden standardmäßig alle Worker beendet, und der Master wird ebenfalls beendet. Es bietet sich an, dieses Verhalten mit Restart=on-failure in einer systemd-Unit-Datei zu kombinieren, um den gesamten Prozess neu zu starten. Falls Sie dieses Verhalten nicht wünschen, müssen Sie das Schlüsselwort "no-exit-on-failure" verwenden.

Siehe auch "-W" im Verwaltungshandbuch.

<a id="entry-3-1-master-worker-no-exit-on-failure"></a>

**`master-worker no-exit-on-failure`**

```haproxy
master-worker no-exit-on-failure
```

Wenn im Master-Worker-Modus ein Worker mit einem Fehlercode beendet wird, etwa wegen eines Segmentierungsfehlers, werden standardmäßig alle Worker beendet, und der Master wird ebenfalls beendet. Es bietet sich an, dieses Verhalten mit Restart=on-failure in einer systemd-Unit-Datei zu kombinieren, um den gesamten Prozess neu zu starten.

Dieses Schlüsselwort ermöglicht es, die übrigen Prozesse nach dem Absturz eines Workers weiterlaufen zu lassen, anstatt alle zu beenden. Es muss mit Vorsicht verwendet werden, da es ausschließlich zur Fehlerdiagnose vorgesehen ist und den Master-Prozess in einen abnormen Zustand versetzen könnte.

<a id="entry-3-1-max-threads-per-group"></a>

**`max-threads-per-group <number>`**

```haproxy
max-threads-per-group <number>
```

Legt die maximale Anzahl von Threads in einer Thread-Gruppe fest. Sofern die Anzahl der Thread-Gruppen nicht mit der Direktive "thread-groups" festgelegt ist, erstellt haproxy so viele Thread-Gruppen wie nötig, um die angeforderte Thread-Anzahl zu erreichen. Der Mindestwert ist 1, der Höchstwert 64 (auf 64-Bit-Systemen beziehungsweise 32 auf 32-Bit-Systemen). Niedrigere Werte verringern die Konkurrenz bei atomaren Operationen auf gemeinsam genutzten Zuständen, können jedoch die Anzahl der Sockets erhöhen, die zum Erstellen aller Listener und zum Vorhalten ungenutzter Backend-Verbindungen benötigt werden. Höhere Werte verringern diesen Aufwand, verursachen bei Konkurrenz jedoch eine höhere CPU-Auslastung und niedrigere Verbindungsraten. Der Standardwert ist 16. In Tests auf verschiedenen Systemen erwies sich dies als der beste Kompromiss, darunter x86_64-Prozessoren mehrerer Hersteller und große Arm64-Systeme, sowohl auf physischer Hardware als auch unter Hypervisoren.

<a id="entry-3-1-mworker-max-reloads"></a>

**`mworker-max-reloads <number>`**

```haproxy
mworker-max-reloads <number>
```

Im Master-Worker-Modus begrenzt diese Option, wie viele Neuladungen ein Worker überleben kann. Wenn der Worker nach einer Neuladung nicht beendet wurde und die Anzahl seiner Neuladungen diesen Wert überschreitet, erhält er ein SIGTERM-Signal. Diese Option hilft, die Anzahl der Worker unter Kontrolle zu halten. Siehe auch "show proc" im Verwaltungshandbuch.

Standardmäßig ist dieser Wert auf 50 gesetzt.

<a id="entry-3-1-nbthread"></a>

**`nbthread <number>`**

```haproxy
nbthread <number>
```

Diese Einstellung ist nur verfügbar, wenn die Unterstützung für Threads einkompiliert wurde. Sie lässt HAProxy mit `<number>` Threads laufen. "nbthread" funktioniert auch, wenn HAProxy im Vordergrund gestartet wird. Auf einigen Plattformen mit Unterstützung für CPU-Affinität wird der Standardwert von "nbthread" automatisch auf die Anzahl der CPUs gesetzt, an die der Prozess beim Start gebunden ist. Dadurch lässt sich die Thread-Anzahl vom aufrufenden Prozess aus mit Befehlen wie "taskset" oder "cpuset" einfach anpassen. Andernfalls ist der Standardwert 1. Der Standardwert wird in der Ausgabe von "haproxy -vv" angezeigt. Beachten Sie, dass sowohl hier gesetzte als auch automatisch ermittelte Werte der durch "thread-hard-limit" festgelegten Grenze unterliegen (sofern diese gesetzt ist).

<a id="entry-3-1-numa-cpu-mapping"></a>

**`numa-cpu-mapping`**

```haproxy
numa-cpu-mapping
```

Auf einer NUMA-fähigen Plattform ermöglicht dies der Direktive "cpu-policy", die Topologie zu untersuchen und die beste Auswahl an CPUs sowie die dazugehörige Thread-Anzahl zu ermitteln. Falls die angewendete Bindung auf einer bestimmten Architektur jedoch nicht optimal ist, kann sie mit der Anweisung 'no numa-cpu-mapping' deaktiviert werden. Diese automatische Bindung wird auch dann nicht angewendet, wenn eine 'nbthread'-Anweisung in der Konfiguration vorhanden ist, wenn die Prozessaffinität bereits festgelegt wurde, beispielsweise über die Direktive 'cpu-map' oder das Dienstprogramm taskset, oder wenn cpu-policy auf einen anderen Wert gesetzt ist. Siehe auch "cpu-map", "cpu-policy", "cpu-set".

<a id="entry-3-1-ocsp-update-disable"></a>

**`ocsp-update.disable [ on | off ]`**

```haproxy
ocsp-update.disable [ on | off ]
```

Deaktiviert ocsp-update in HAProxy vollständig. Sämtliche ocsp-update-Konfiguration wird ignoriert. Der Standardwert ist "off". Weitere Informationen zum automatischen Aktualisierungsmechanismus finden Sie bei der Option "ocsp-update".

<a id="entry-3-1-ocsp-update-httpproxy"></a>

**`ocsp-update.httpproxy <address>[:port]`**

```haproxy
ocsp-update.httpproxy <address>[:port]
```

Ermöglicht die Verwendung eines HTTP-Proxys für die OCSP-Aktualisierungen. Dies funktioniert nur mit HTTP; HTTPS wird nicht unterstützt. Mit dieser Option kann der OCSP-Aktualisierer eine absolute URI in der Anfrage an den Proxy senden.

<a id="entry-3-1-ocsp-update-maxdelay"></a>

**`ocsp-update.maxdelay <number>`**

```haproxy
ocsp-update.maxdelay <number>
tune.ssl.ocsp-update.maxdelay <number> (deprecated)
```

Legt das maximale Intervall zwischen zwei automatischen Aktualisierungen derselben OCSP-Antwort fest. Die Zeit wird in Sekunden angegeben und beträgt standardmäßig 3600 (1 Stunde). Der Wert muss höher als "ocsp-update.mindelay" sein. Weitere Informationen zum automatischen Aktualisierungsmechanismus finden Sie bei der Option "ocsp-update".

<a id="entry-3-1-ocsp-update-mindelay"></a>

**`ocsp-update.mindelay <number>`**

```haproxy
ocsp-update.mindelay <number>
tune.ssl.ocsp-update.mindelay <number> (deprecated)
```

Legt das minimale Intervall zwischen zwei automatischen Aktualisierungen derselben OCSP-Antwort fest. Die Zeit wird in Sekunden angegeben und beträgt standardmäßig 300 (5 Minuten). Dies ist besonders bei OCSP-Antworten ohne ausdrücklichen Ablaufzeitpunkt nützlich. Der Wert muss niedriger als "ocsp-update.maxdelay" sein. Weitere Informationen zum automatischen Aktualisierungsmechanismus finden Sie bei der Option "ocsp-update".

<a id="entry-3-1-ocsp-update-mode"></a>

**`ocsp-update.mode [ on | off ]`**

```haproxy
ocsp-update.mode [ on | off ]
```

Legt den standardmäßigen ocsp-update-Modus für alle in der Konfiguration verwendeten Zertifikate fest. Diese globale Option kann durch die crt-list-Option "ocsp-update" überschrieben werden. Standardmäßig ist sie auf "off" gesetzt. Weitere Informationen zum automatischen Aktualisierungsmechanismus finden Sie bei der Option "ocsp-update".

<a id="entry-3-1-pidfile"></a>

**`pidfile <pidfile>`**

```haproxy
pidfile <pidfile>
```

Schreibt im Daemon-Modus die PIDs aller Daemons in die Datei `<pidfile>` beziehungsweise im Master-Worker-Modus die PID des Master-Prozesses in die Datei `<pidfile>`. Diese Option entspricht dem Befehlszeilenargument "-p". Die Datei muss für den Benutzer zugänglich sein, der den Prozess startet. Siehe auch "daemon" und "master-worker".

<a id="entry-3-1-pp2-never-send-local"></a>

**`pp2-never-send-local`**

```haproxy
pp2-never-send-local
```

Bis einschließlich Version 2.1 enthielt HAProxy einen Fehler in der Implementierung des PROXY-Protokolls v2, durch den bei Zustandsprüfungen ein PROXY-Befehl anstelle eines LOCAL-Befehls gesendet wurde. Dies ist zwar geringfügig, führt aber in den Protokollen einiger Server zu Verwirrung. Leider wurde der Fehler erst sehr spät entdeckt. Dabei zeigte sich, dass einige Server, deren PROXY-Protokollimplementierung möglicherweise nur mit HAProxy getestet wurde, den LOCAL-Befehl nicht korrekt verarbeiten und dauerhaft im Zustand "down" verbleiben, wenn HAProxy sie prüft. In diesem Fall kann diese globale Option aktiviert werden, um zum alten (fehlerhaften) Verhalten zurückzukehren, bis die Hersteller der betroffenen Komponenten kontaktiert und die Komponenten korrigiert wurden. Diese Option ist standardmäßig deaktiviert und wirkt auf alle Server mit der Anweisung "send-proxy-v2".

<a id="entry-3-1-presetenv"></a>

**`presetenv <name> <value>`**

```haproxy
presetenv <name> <value>
```

Setzt die Umgebungsvariable `<name>` auf den Wert `<value>`. Wenn die Variable bereits existiert, wird sie NICHT überschrieben. Die Änderungen werden sofort wirksam, sodass bereits die nächste Zeile in der Konfigurationsdatei den neuen Wert sieht. Siehe auch "setenv", "resetenv" und "unsetenv".

<a id="entry-3-1-prealloc-fd"></a>

**`prealloc-fd`**

```haproxy
prealloc-fd
```

Öffnet einmalig den höchsten Dateideskriptor und bewirkt damit eine Vorabzuweisung der Datenstrukturen des Kernels. Dies verhindert kurze Pausen, wenn nbthread\>1 gilt und HAProxy einen Dateideskriptor öffnet, für den der Kernel seine Datenstrukturen erweitern muss.

<a id="entry-3-1-resetenv"></a>

**`resetenv [<name> ...]`**

```haproxy
resetenv [<name> ...]
```

Entfernt alle Umgebungsvariablen außer den als Argument angegebenen. Dies ermöglicht eine bereinigte, kontrollierte Umgebung, bevor mit setenv oder unsetenv neue Werte gesetzt werden. Beachten Sie, dass einige interne Funktionen Umgebungsvariablen verwenden können, etwa Funktionen zur Zeitverarbeitung, aber auch OpenSSL oder sogar externe Prüfungen. Dies darf nur mit äußerster Vorsicht und nach vollständiger Validierung verwendet werden. Die Änderungen werden sofort wirksam, sodass bereits die nächste Zeile in der Konfigurationsdatei die neue Umgebung sieht. Siehe auch "setenv", "presetenv" und "unsetenv".

<a id="entry-3-1-server-state-base"></a>

**`server-state-base <directory>`**

```haproxy
server-state-base <directory>
```

Legt das Verzeichnispräfix fest, das allen Namen von Serverzustandsdateien vorangestellt wird, die nicht mit '/' beginnen. Siehe auch "server-state-file", "load-server-state-from-file" und "server-state-file-name".

<a id="entry-3-1-server-state-file"></a>

**`server-state-file <file>`**

```haproxy
server-state-file <file>
```

Gibt den Pfad zur Datei mit den Serverzuständen an. Beginnt der Pfad mit einem Schrägstrich ('/'), gilt er als absolut; andernfalls wird er relativ zu dem mit "server-state-base" festgelegten Verzeichnis (falls gesetzt) oder zum aktuellen Verzeichnis interpretiert. Vor dem Neuladen von HAProxy können die aktuellen Serverzustände mit dem Statistikbefehl "show servers state" gespeichert werden. Die Ausgabe dieses Befehls muss in die durch `<file>` bezeichnete Datei geschrieben werden. Beim Start liest, lädt und übernimmt HAProxy vor der Verarbeitung von Datenverkehr den Zustand jedes Servers, der sowohl in der Datei als auch in der aktuellen laufenden Konfiguration vorhanden ist. Siehe auch "server-state-base" und "show servers state", "load-server-state-from-file" und "server-state-file-name"

<a id="entry-3-1-set-dumpable"></a>

**`set-dumpable [ on | off | libs ]`**

```haproxy
set-dumpable [ on | off | libs ]
```

Mit dieser Option lässt sich das Verhalten bei der Erstellung eines Speicherabbilds nach einem Prozessabsturz festlegen. Verfügbare Optionen sind:

- on aktiviert die Erstellung von Speicherabbildern auf Prozessebene, falls sie zuvor deaktiviert war.

- off deaktiviert eine zuvor aktivierte Erstellung von Speicherabbildern.

- libs aktiviert die Erstellung von Speicherabbildern mit einer eingebetteten Kopie der für die Fehlerdiagnose benötigten Programmdateien und Bibliotheken. Entwickler können dies anfordern. In diesem Fall versucht haproxy, die Bibliotheken, von denen es abhängt, in den Speicher zu laden und dort sorgfältig aufzubewahren. Falls der Prozess abstürzt, werden sie in das Speicherabbild aufgenommen, sodass sie nicht mehr aus dem Dateisystem beschafft werden müssen und keine Gefahr besteht, dass sie nicht zum Speicherabbild passen. Dafür werden einige bis einige zehn Megabyte zusätzlicher RAM benötigt, weshalb dies auf kleinen Systemen besser nicht verwendet werden sollte.

Diese Option sollte standardmäßig deaktiviert bleiben und nur auf Anforderung eines Entwicklers aktiviert werden. Standardmäßig ist sie deaktiviert. Ohne Argument ist der Standardwert "on". Wenn sie aktiviert wurde, kann sie dennoch durch Voranstellen des Schlüsselworts "no" oder durch Setzen auf "off" ausdrücklich deaktiviert werden. Sie hat keine Auswirkungen auf Leistung oder Stabilität, versucht aber mit allen verfügbaren Mitteln, Speicherabbilder wieder zu aktivieren, die möglicherweise durch Dateigrößenlimits (ulimit -f), Größenlimits für Speicherabbilder (ulimit -c) oder die Fähigkeit eines Prozesses zur Erstellung von Speicherabbildern nach Änderung seiner UID/GID (etwa /proc/sys/fs/suid_dumpable unter Linux) deaktiviert wurden. Speicherabbilder können weiterhin durch die Berechtigungen des aktuellen Verzeichnisses (prüfen Sie, aus welchem Verzeichnis die Datei gestartet wird), die Berechtigungen des chroot-Verzeichnisses (möglicherweise muss die chroot-Direktive vorübergehend deaktiviert oder das Verzeichnis an einen eigenen beschreibbaren Ort verlegt werden) oder andere systemspezifische Einschränkungen begrenzt sein. Einige Linux-Varianten sind beispielsweise dafür bekannt, die standardmäßige core-Datei durch den Pfad zu einem Programm zu ersetzen, das nicht einmal auf dem System installiert ist (prüfen Sie /proc/sys/kernel/core_pattern). Häufig lässt sich das Problem einfach durch Eintragen von "core", "core.%p" oder "/var/log/core/core.%p" beheben. Wenn Sie diese Option aktivieren und auf das erneute Auftreten eines seltenen Problems warten, ist es oft sinnvoll, zunächst ein solches Speicherabbild zu erzeugen, beispielsweise durch Senden von "kill -11" an den "haproxy"-Prozess, und zu prüfen, ob dieser beim Beenden ein Speicherabbild am erwarteten Ort hinterlässt.

<a id="entry-3-1-set-var"></a>

**`set-var <var-name> <expr>`**

```haproxy
set-var <var-name> <expr>
```

Setzt die prozessweite Variable '`<var-name>`' auf das Ergebnis der Auswertung des Sample-Ausdrucks `<expr>`. Die Variable '`<var-name>`' darf nur eine prozessweite Variable sein (mit dem Präfix 'proc.'). Dies funktioniert genau wie die Aktion 'set-var' in TCP- oder HTTP-Regeln, mit dem Unterschied, dass der Ausdruck beim Einlesen der Konfiguration ausgewertet und die Variable sofort gesetzt wird. Im Ausdruck sind nur Sample-Fetch-Funktionen und Konverter erlaubt, die interne Daten verwenden, typischerweise 'int(value)' oder 'str(value)'. Auch bereits angelegte Variablen können referenziert werden. Diese Variablen können anschließend aus den regulären Regelsätzen gelesen und geändert werden.

Beispiel:

```text
global
    set-var proc.current_state str(primary)
    set-var proc.prio int(100)
    set-var proc.threshold int(200),sub(proc.prio)
```

<a id="entry-3-1-set-var-fmt"></a>

**`set-var-fmt <var-name> <fmt>`**

```haproxy
set-var-fmt <var-name> <fmt>
```

Setzt die prozessweite Variable '`<var-name>`' auf die Zeichenfolge, die sich aus der Auswertung des Protokollformats `<fmt>` ergibt. Die Variable '`<var-name>`' darf nur eine prozessweite Variable sein (mit dem Präfix 'proc.'). Dies funktioniert genau wie die Aktion 'set-var-fmt' in TCP- oder HTTP-Regeln, mit dem Unterschied, dass der Ausdruck beim Einlesen der Konfiguration ausgewertet und die Variable sofort gesetzt wird. Im Ausdruck sind nur Sample-Fetch-Funktionen und Konverter erlaubt, die interne Daten verwenden, typischerweise 'int(value)' oder 'str(value)'. Auch bereits angelegte Variablen können referenziert werden. Diese Variablen können anschließend aus den regulären Regelsätzen gelesen und geändert werden. Einzelheiten zur Syntax benutzerdefinierter Protokollformate finden Sie in [Abschnitt 8.2.6](/de/haproxy/configuration-logging/#section-8-2-6).

Beispiel:

```text
global
    set-var-fmt proc.current_state "primary"
    set-var-fmt proc.bootid        "%pid|%t"
```

<a id="entry-3-1-setcap"></a>

**`setcap <name>[,<name>...]`**

```haproxy
setcap <name>[,<name>...]
```

Legt eine Liste von Capabilities fest, die erhalten bleiben müssen, wenn der Prozess entweder als Benutzer ohne Root-Rechte (uid \> 0) gestartet und ausgeführt wird oder zunächst mit uid 0 (root) startet und anschließend zu einem Benutzer ohne Root-Rechte wechselt. Standardmäßig gehen beim Wechsel der uid alle Berechtigungen verloren. Einige davon werden jedoch oft benötigt, etwa um sich beim transparenten Proxying von einer fremden Adresse aus mit einem Server zu verbinden oder einen Port unterhalb von 1024 zu binden, beispielsweise bei Verwendung von "tune.quic.fe.sock-per-conn default-on". Dies führt zu Konfigurationen, die vollständig unter uid 0 laufen. Das Setzen von Capabilities ist im Allgemeinen eine sicherere Alternative, da nur die benötigten Capabilities erhalten bleiben. Die Funktion ist OS-spezifisch und nur unter Linux aktiviert, wenn beim Kompilieren USE_LINUX_CAP=1 gesetzt wurde. Die Liste der unterstützten Capabilities hängt ebenfalls vom OS ab und wird in der Fehlermeldung aufgeführt, die bei Angabe eines ungültigen oder leeren Capability-Namens erscheint. Mehrere Capabilities können durch Kommas getrennt angegeben werden. Zu den häufig verwendeten gehören "cap_net_raw", das die transparente Bindung an eine fremde Adresse erlaubt, und "cap_net_bind_service", das die Bindung an einen privilegierten Port erlaubt und von QUIC verwendet werden kann. Wenn der Prozess unter demselben Benutzer ohne Root-Rechte gestartet und ausgeführt wird, sollten die benötigten Capabilities zusätzlich zu diesem Schlüsselwort mit setcap auf der haproxy-Programmdatei gesetzt werden. Weitere Einzelheiten zum Setzen von Capabilities auf der haproxy-Programmdatei finden Sie in Kapitel 13.1 zur Unterstützung von Linux-Capabilities im Verwaltungshandbuch.

Beispiel:

```text
global
    setcap cap_net_bind_service,cap_net_admin
```

<a id="entry-3-1-setenv"></a>

**`setenv <name> <value>`**

```haproxy
setenv <name> <value>
```

Setzt die Umgebungsvariable `<name>` auf den Wert `<value>`. Wenn die Variable bereits existiert, wird sie überschrieben. Die Änderungen werden sofort wirksam, sodass bereits die nächste Zeile in der Konfigurationsdatei den neuen Wert sieht. Siehe auch "presetenv", "resetenv" und "unsetenv".

<a id="entry-3-1-shm-stats-file"></a>

**`shm-stats-file <name>`**

```haproxy
shm-stats-file <name>
```

Wenn diese Direktive gesetzt ist, aktiviert sie die Verwendung gemeinsamen Speichers zum Speichern von Statistikzählern. `<name>` wird als Argument an shm_open() übergeben, um den gemeinsamen Speicher an einem eindeutigen Ort zu öffnen. Die Direktive ist daher nur auf Systemen verfügbar, die shm_open() unterstützen. Wenn SHM für Statistiken verwendet wird, werden alle gemeinsam nutzbaren Zähler für Frontends, Backends, Listener und Server im SHM gespeichert, sofern für diese Objekte eine GUID gesetzt ist. Beim Neuladen von haproxy versucht der neue Prozess, den SHM nach Objekten zu durchsuchen, die sich anhand ihrer GUID und ihres Typs den in der Konfiguration definierten Objekten zuordnen lassen. Damit sollen die Werte einiger Zähler beim Neuladen erhalten bleiben. Wird haproxy hingegen ordnungsgemäß beendet, werden die SHM-Objekte freigegeben, wodurch die Zähler tatsächlich zurückgesetzt werden. Die Datei kann auch vor dem Start eines neuen Prozesses manuell entfernt werden, um ein Zurücksetzen zu erzwingen.

Siehe auch "guid", "guid-prefix" und "shm-stats-file-max-objects"

<a id="entry-3-1-shm-stats-file-max-objects"></a>

**`shm-stats-file-max-objects <number>`**

```haproxy
shm-stats-file-max-objects <number>
```

Diese Einstellung legt fest, wie viele Objekte der für gemeinsame Zähler verwendete gemeinsame Speicher pro Thread-Gruppe maximal aufnehmen kann. Sie steht in direktem Zusammenhang mit der maximalen Speichergröße des shm und dient dazu, den shm vorab auf eine bestimmte Größe abzubilden, damit zur Laufzeit keine erneute Speicherabbildung nötig ist. Der Standardwert ist 2k. Dies sollte für die meisten Konfigurationen ausreichen, ohne einen unangemessenen Speicherverbrauch zu riskieren, lässt sich bei Bedarf aber einfach ändern. haproxy meldet beim Start, wenn der Wert zu niedrig ist, um alle Objekte zu registrieren, die im gemeinsamen Speicher abgelegt werden sollen. Diese Einstellung ist nur relevant, wenn "shm-stats-file" definiert wurde.

Siehe auch "thread-groups"

<a id="entry-3-1-ssl-default-bind-ciphers"></a>

**`ssl-default-bind-ciphers <ciphers>`**

```haproxy
ssl-default-bind-ciphers <ciphers>
```

Diese Einstellung ist nur verfügbar, wenn die Unterstützung für OpenSSL einkompiliert wurde. Sie legt für alle "bind"-Zeilen ohne eigene ausdrückliche Definition die standardmäßige Zeichenfolge fest, die die Liste der Verschlüsselungsalgorithmen ("cipher suite") beschreibt, die beim SSL/TLS-Handshake bis einschließlich TLSv1.2 ausgehandelt werden. Das Format der Zeichenfolge ist in "man 1 ciphers" der OpenSSL-Handbuchseiten definiert. Hintergrundinformationen und Empfehlungen finden Sie beispielsweise unter (<https://wiki.mozilla.org/Security/Server_Side_TLS>) und (<https://mozilla.github.io/server-side-tls/ssl-config-generator/>). Zur Konfiguration von TLSv1.3-Verschlüsselungsalgorithmen siehe das Schlüsselwort "ssl-default-bind-ciphersuites". Weitere Informationen finden Sie beim Schlüsselwort "bind".

<a id="entry-3-1-ssl-default-bind-ciphersuites"></a>

**`ssl-default-bind-ciphersuites <ciphersuites>`**

```haproxy
ssl-default-bind-ciphersuites <ciphersuites>
```

Diese Einstellung ist nur verfügbar, wenn die Unterstützung für OpenSSL einkompiliert wurde und HAProxy mit OpenSSL 1.1.1 oder höher erstellt wurde. Sie legt für alle "bind"-Zeilen ohne eigene ausdrückliche Definition die standardmäßige Zeichenfolge fest, die die Liste der Verschlüsselungsalgorithmen ("cipher suite") beschreibt, die beim TLSv1.3-Handshake ausgehandelt werden. Das Format der Zeichenfolge ist in "man 1 ciphers" der OpenSSL-Handbuchseiten im Abschnitt "ciphersuites" definiert. Zur Konfiguration von Verschlüsselungsalgorithmen für TLSv1.2 und frühere Versionen siehe das Schlüsselwort "ssl-default-bind-ciphers". Diese Einstellung akzeptiert möglicherweise auch TLSv1.2-Cipher-Suites. Dieses Verhalten ist jedoch nicht dokumentiert und wird nicht empfohlen, da es inkonsistent oder fehlerhaft sein könnte. Die standardmäßigen TLSv1.3-Cipher-Suites von OpenSSL sind:
"TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256"

TLSv1.3 unterstützt nur 5 Cipher-Suites:

- TLS_AES_128_GCM_SHA256
- TLS_AES_256_GCM_SHA384
- TLS_CHACHA20_POLY1305_SHA256
- TLS_AES_128_CCM_SHA256
- TLS_AES_128_CCM_8_SHA256

Weitere Informationen finden Sie beim Schlüsselwort "bind".

Beispiel:

```text
global
    ssl-default-bind-ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-RSA-AES128-GCM-SHA256
    ssl-default-bind-ciphersuites TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256
```

<a id="entry-3-1-ssl-default-bind-client-sigalgs"></a>

**`ssl-default-bind-client-sigalgs <sigalgs>`**

```haproxy
ssl-default-bind-client-sigalgs <sigalgs>
```

Diese Einstellung ist nur verfügbar, wenn die Unterstützung für OpenSSL einkompiliert wurde. Sie legt für alle "bind"-Zeilen ohne eigene ausdrückliche Definition die standardmäßige Zeichenfolge fest, die die Liste der Signaturalgorithmen für die Client-Authentifizierung beschreibt. Das Format ist eine durch Doppelpunkte getrennte Liste von Signaturalgorithmen. Jeder Signaturalgorithmus kann in einer von zwei Formen angegeben werden: als Name eines TLS1.3-Signaturschemas ("rsa_pss_rsae_sha256") oder als Kombination aus Public-Key-Algorithmus + Digest ("ECDSA+SHA256"). Eine Liste kann beide Formen enthalten. Weitere Informationen zum Format finden Sie unter SSL_CTX_set1_client_sigalgs(3). Eine Liste der Signaturalgorithmen ist außerdem in RFC8446, Abschnitt [4.2.3](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3), sowie in der OpenSSL-Datei ssl/t1_lib.c verfügbar. Diese Einstellung gilt nicht für TLSv1.1 und frühere Protokollversionen, da die Signaturalgorithmen in diesen Versionen nicht gesondert ausgehandelt werden. Es wird nicht empfohlen, diese Einstellung zu ändern, sofern keine Kompatibilität mit einer Middlebox erforderlich ist.

<a id="entry-3-1-ssl-default-bind-curves"></a>

**`ssl-default-bind-curves <curves>`**

```haproxy
ssl-default-bind-curves <curves>
```

Diese Einstellung ist nur verfügbar, wenn die Unterstützung für OpenSSL einkompiliert wurde. Sie legt die standardmäßige Zeichenfolge fest, die die Liste der Algorithmen für elliptische Kurven ("curve suite") beschreibt, die beim SSL/TLS-Handshake mit ECDHE ausgehandelt werden. Das Format ist eine durch Doppelpunkte getrennte Liste von Kurvennamen. Weitere Informationen finden Sie beim Schlüsselwort "bind".

<a id="entry-3-1-ssl-default-bind-options"></a>

**`ssl-default-bind-options [<option>]...`**

```haproxy
ssl-default-bind-options [<option>]...
```

Diese Einstellung ist nur verfügbar, wenn die Unterstützung für OpenSSL einkompiliert wurde. Sie legt standardmäßige ssl-options fest, die für alle "bind"-Zeilen erzwungen werden. Die verfügbaren Optionen finden Sie beim Schlüsselwort "bind".

Beispiel:

```text
global
   ssl-default-bind-options ssl-min-ver TLSv1.0 no-tls-tickets
```

<a id="entry-3-1-ssl-default-bind-sigalgs"></a>

**`ssl-default-bind-sigalgs <sigalgs>`**

```haproxy
ssl-default-bind-sigalgs <sigalgs>
```

Diese Einstellung ist nur verfügbar, wenn die Unterstützung für OpenSSL einkompiliert wurde. Sie legt für alle "bind"-Zeilen ohne eigene ausdrückliche Definition die standardmäßige Zeichenfolge fest, die die Liste der Signaturalgorithmen beschreibt, die beim TLSv1.2- und TLSv1.3-Handshake ausgehandelt werden. Das Format ist eine durch Doppelpunkte getrennte Liste von Signaturalgorithmen. Jeder Signaturalgorithmus kann in einer von zwei Formen angegeben werden: als Name eines TLS1.3-Signaturschemas ("rsa_pss_rsae_sha256") oder als Kombination aus Public-Key-Algorithmus + Digest ("ECDSA+SHA256"). Eine Liste kann beide Formen enthalten. Weitere Informationen zum Format finden Sie unter SSL_CTX_set1_sigalgs(3). Eine Liste der Signaturalgorithmen ist außerdem in RFC8446, Abschnitt [4.2.3](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3), sowie in der OpenSSL-Datei ssl/t1_lib.c verfügbar. Diese Einstellung gilt nicht für TLSv1.1 und frühere Protokollversionen, da die Signaturalgorithmen in diesen Versionen nicht gesondert ausgehandelt werden. Es wird nicht empfohlen, diese Einstellung zu ändern, sofern keine Kompatibilität mit einer Middlebox erforderlich ist.

<a id="entry-3-1-ssl-default-server-ciphers"></a>

**`ssl-default-server-ciphers <ciphers>`**

```haproxy
ssl-default-server-ciphers <ciphers>
```

Diese Einstellung ist nur verfügbar, wenn die Unterstützung für OpenSSL einkompiliert wurde. Sie legt für alle "server"-Zeilen ohne eigene ausdrückliche Definition die standardmäßige Zeichenfolge fest, die die Liste der Verschlüsselungsalgorithmen beschreibt, die beim SSL/TLS-Handshake bis einschließlich TLSv1.2 mit dem Server ausgehandelt werden. Das Format der Zeichenfolge ist in "man 1 ciphers" der OpenSSL-Handbuchseiten definiert. Hintergrundinformationen und Empfehlungen finden Sie beispielsweise unter (<https://wiki.mozilla.org/Security/Server_Side_TLS>) und (<https://mozilla.github.io/server-side-tls/ssl-config-generator/>). Zur Konfiguration von TLSv1.3-Verschlüsselungsalgorithmen siehe das Schlüsselwort "ssl-default-server-ciphersuites". Weitere Informationen finden Sie beim Schlüsselwort "server".

<a id="entry-3-1-ssl-default-server-ciphersuites"></a>

**`ssl-default-server-ciphersuites <ciphersuites>`**

```haproxy
ssl-default-server-ciphersuites <ciphersuites>
```

Diese Einstellung ist nur verfügbar, wenn die Unterstützung für OpenSSL einkompiliert wurde und HAProxy mit OpenSSL 1.1.1 oder höher erstellt wurde. Sie legt für alle "server"-Zeilen ohne eigene ausdrückliche Definition die standardmäßige Zeichenfolge fest, die die Liste der Verschlüsselungsalgorithmen beschreibt, die beim TLSv1.3-Handshake mit dem Server ausgehandelt werden. Das Format der Zeichenfolge ist in "man 1 ciphers" der OpenSSL-Handbuchseiten im Abschnitt "ciphersuites" definiert. Zur Konfiguration von Verschlüsselungsalgorithmen für TLSv1.2 und frühere Versionen siehe das Schlüsselwort "ssl-default-server-ciphers". Weitere Informationen finden Sie beim Schlüsselwort "server".

<a id="entry-3-1-ssl-default-server-client-sigalgs"></a>

**`ssl-default-server-client-sigalgs <sigalgs>`**

```haproxy
ssl-default-server-client-sigalgs <sigalgs>
```

Diese Einstellung ist nur verfügbar, wenn die Unterstützung für OpenSSL einkompiliert wurde. Sie legt für alle "server"-Zeilen ohne eigene ausdrückliche Definition die standardmäßige Zeichenfolge fest, die die Liste der Signaturalgorithmen für die Client-Authentifizierung beschreibt. Das Format ist eine durch Doppelpunkte getrennte Liste von Signaturalgorithmen. Jeder Signaturalgorithmus kann in einer von zwei Formen angegeben werden: als Name eines TLS1.3-Signaturschemas ("rsa_pss_rsae_sha256") oder als Kombination aus Public-Key-Algorithmus + Digest ("ECDSA+SHA256"). Eine Liste kann beide Formen enthalten. Weitere Informationen zum Format finden Sie unter SSL_CTX_set1_client_sigalgs(3). Eine Liste der Signaturalgorithmen ist außerdem in RFC8446, Abschnitt [4.2.3](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3), sowie in der OpenSSL-Datei ssl/t1_lib.c verfügbar. Diese Einstellung gilt nicht für TLSv1.1 und frühere Protokollversionen, da die Signaturalgorithmen in diesen Versionen nicht gesondert ausgehandelt werden. Es wird nicht empfohlen, diese Einstellung zu ändern, sofern keine Kompatibilität mit einer Middlebox erforderlich ist.

<a id="entry-3-1-ssl-default-server-curves"></a>

**`ssl-default-server-curves <curves>`**

```haproxy
ssl-default-server-curves <curves>
```

Diese Einstellung ist nur verfügbar, wenn die Unterstützung für OpenSSL einkompiliert wurde. Sie legt die standardmäßige Zeichenfolge fest, die die Liste der Algorithmen für elliptische Kurven ("curve suite") beschreibt, die beim SSL/TLS-Handshake mit ECDHE ausgehandelt werden. Das Format ist eine durch Doppelpunkte getrennte Liste von Kurvennamen. Weitere Informationen finden Sie beim Schlüsselwort "server".

<a id="entry-3-1-ssl-default-server-options"></a>

**`ssl-default-server-options [<option>]...`**

```haproxy
ssl-default-server-options [<option>]...
```

Diese Einstellung ist nur verfügbar, wenn die Unterstützung für OpenSSL einkompiliert wurde. Sie legt standardmäßige ssl-options fest, die für alle "server"-Zeilen erzwungen werden. Die verfügbaren Optionen finden Sie beim Schlüsselwort "server".

<a id="entry-3-1-ssl-default-server-sigalgs"></a>

**`ssl-default-server-sigalgs <sigalgs>`**

```haproxy
ssl-default-server-sigalgs <sigalgs>
```

Diese Einstellung ist nur verfügbar, wenn die Unterstützung für OpenSSL einkompiliert wurde. Sie legt für alle "server"-Zeilen ohne eigene ausdrückliche Definition die standardmäßige Zeichenfolge fest, die die Liste der Signaturalgorithmen beschreibt, die beim TLSv1.2- und TLSv1.3-Handshake ausgehandelt werden. Das Format ist eine durch Doppelpunkte getrennte Liste von Signaturalgorithmen. Jeder Signaturalgorithmus kann in einer von zwei Formen angegeben werden: als Name eines TLS1.3-Signaturschemas ("rsa_pss_rsae_sha256") oder als Kombination aus Public-Key-Algorithmus + Digest ("ECDSA+SHA256"). Eine Liste kann beide Formen enthalten. Weitere Informationen zum Format finden Sie unter SSL_CTX_set1_sigalgs(3). Eine Liste der Signaturalgorithmen ist außerdem in RFC8446, Abschnitt [4.2.3](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3), sowie in der OpenSSL-Datei ssl/t1_lib.c verfügbar. Diese Einstellung gilt nicht für TLSv1.1 und frühere Protokollversionen, da die Signaturalgorithmen in diesen Versionen nicht gesondert ausgehandelt werden. Es wird nicht empfohlen, diese Einstellung zu ändern, sofern keine Kompatibilität mit einer Middlebox erforderlich ist.

<a id="entry-3-1-ssl-dh-param-file"></a>

**`ssl-dh-param-file <file>`**

```haproxy
ssl-dh-param-file <file>
```

Diese Einstellung ist nur verfügbar, wenn die Unterstützung für OpenSSL einkompiliert wurde. Sie legt für alle "bind"-Zeilen ohne eigene ausdrückliche Definition die standardmäßigen DH-Parameter fest, die beim SSL/TLS-Handshake mit ephemerem Diffie-Hellman-Schlüsselaustausch (DHE) verwendet werden. Benutzerdefinierte DH-Parameter in einer bind-Zertifikatsdatei haben, sofern vorhanden, Vorrang. Wenn weder mit ssl-dh-param-file noch direkt in der Zertifikatsdatei benutzerdefinierte DH-Parameter angegeben sind, werden keine DHE-Verschlüsselungsverfahren verwendet, es sei denn, tune.ssl.default-dh-param ist gesetzt. Im letzteren Fall werden vordefinierte DH-Parameter der angegebenen Größe verwendet. Benutzerdefinierte Parameter gelten als sicherer, daher wird ihre Verwendung empfohlen. Sie können mit dem OpenSSL-Befehl "openssl dhparam `<size>`" erzeugt werden. Dabei sollte die Größe mindestens 2048 betragen, da DH-Parameter mit 1024 Bit nicht mehr als sicher gelten sollten.

<a id="entry-3-1-ssl-passphrase-cmd"></a>

**`ssl-passphrase-cmd <cmd> <args> ...`**

```haproxy
ssl-passphrase-cmd <cmd> <args> ...
```

Diese Einstellung ist nur verfügbar, wenn die Unterstützung für OpenSSL einkompiliert wurde. Sie ermöglicht die Definition einer vollständigen Befehlszeile, die aufgerufen wird, wenn während der Initialisierung ein verschlüsseltes Zertifikat geladen wird. Der Befehl kann ein Skript oder ein anderes Programm sein. Er erhält als ersten Parameter den Pfad des verschlüsselten privaten Schlüssels und anschließend die benutzerdefinierten "args"-Parameter. Er sollte die Passphrase zum Entschlüsseln des privaten Schlüssels auf der Standardausgabe ausgeben. Für jeden während der Initialisierung neu geladenen verschlüsselten privaten Schlüssel versucht HAProxy zunächst alle bereits bekannten Passphrasen zur Entschlüsselung und ruft den Passphrasenbefehl erst dann erneut auf, wenn keine davon funktioniert.

<a id="entry-3-1-ssl-propquery"></a>

**`ssl-propquery <query>`**

```haproxy
ssl-propquery <query>
```

Diese Einstellung ist nur verfügbar, wenn die Unterstützung für OpenSSL einkompiliert wurde und die OpenSSL-Version mindestens 3.0 ist. Sie ermöglicht die Definition einer standardmäßigen Eigenschaftszeichenfolge, die beim Abrufen von Algorithmen aus Providern verwendet wird. Sie verhält sich wie die openssl-Option propquery und verwendet dieselbe Syntax (beschrieben unter <https://www.openssl.org/docs/man3.0/man7/property.html>). Wenn beispielsweise zwei Provider geladen sind, foo und der Standardprovider, ermöglicht die propquery "?provider=foo", standardmäßig die vom Provider foo bereitgestellten Algorithmusimplementierungen auszuwählen und auf die des Standardproviders zurückzugreifen, wenn sie nicht gefunden wurden.

<a id="entry-3-1-ssl-provider"></a>

**`ssl-provider <name>`**

```haproxy
ssl-provider <name>
```

Diese Einstellung ist nur verfügbar, wenn die Unterstützung für OpenSSL einkompiliert wurde und die OpenSSL-Version mindestens 3.0 ist. Sie ermöglicht das Laden eines Providers während der Initialisierung. Bei erfolgreichem Laden kann HAProxy die vom geladenen Provider bereitgestellten Funktionen verwenden. In einer Konfigurationsdatei können mehrere 'ssl-provider'-Optionen angegeben werden. Die Provider werden in der Reihenfolge ihres Auftretens geladen.

Beachten Sie, dass das explizite Laden eines Providers verhindert, dass OpenSSL den Provider 'default' automatisch lädt. OpenSSL erlaubt es auch, die zu ladenden Provider direkt in seiner Konfigurationsdatei (beispielsweise openssl.cnf) festzulegen. Daher ist diese Option 'ssl-provider' zum Laden von Providern nicht erforderlich. Mit dem CLI-Befehl "show ssl providers" können alle erfolgreich geladenen Provider angezeigt werden.

Der Standardsuchpfad für OpenSSL-Provider ist in der Ausgabe des Befehls "openssl version -a" zu finden. Befindet sich der Provider in einem anderen Verzeichnis, können Sie die Umgebungsvariable OPENSSL_MODULES auf das Verzeichnis setzen, in dem der Provider liegt.

Siehe auch "ssl-propquery" und "ssl-provider-path".

<a id="entry-3-1-ssl-provider-path"></a>

**`ssl-provider-path <path>`**

```haproxy
ssl-provider-path <path>
```

Diese Einstellung ist nur verfügbar, wenn die Unterstützung für OpenSSL einkompiliert wurde und die OpenSSL-Version mindestens 3.0 ist. Sie ermöglicht die Angabe des Suchpfads, den OpenSSL bei der Suche nach Providern verwenden soll. Sie verhält sich wie die Umgebungsvariable OPENSSL_MODULES. Sie gilt für alle folgenden 'ssl-provider'-Optionen, bis ein neuer 'ssl-provider-path' definiert wird. Siehe auch "ssl-provider".

<a id="entry-3-1-ssl-load-extra-del-ext"></a>

**`ssl-load-extra-del-ext`**

```haproxy
ssl-load-extra-del-ext
```

Diese Einstellung konfiguriert, wie HAProxy nach zusätzlichen SSL-Dateien sucht. Standardmäßig fügt HAProxy dem Dateinamen eine neue Erweiterung hinzu (beispielsweise wird für "foobar.crt" die Datei "foobar.crt.key" geladen). Wenn diese Option aktiviert ist, entfernt HAProxy die Erweiterung, bevor es die neue hinzufügt (beispielsweise wird für "foobar.crt" die Datei "foobar.key" geladen).

Die crt-Datei muss die Erweiterung ".crt" haben, damit diese Option funktioniert.

Diese Option ist nicht mit Bundle-Erweiterungen (.ecdsa, .rsa. .dsa) kompatibel und versucht nicht, diese zu entfernen.

Diese Option ist standardmäßig deaktiviert. Siehe auch "ssl-load-extra-files".

<a id="entry-3-1-ssl-load-extra-files"></a>

**`ssl-load-extra-files <none|all|bundle|sctl|ocsp|issuer|key>*`**

```haproxy
ssl-load-extra-files <none|all|bundle|sctl|ocsp|issuer|key>*
```

Diese Einstellung verändert, wie HAProxy beim Laden von SSL-Zertifikaten nach nicht ausdrücklich angegebenen Dateien sucht. Die Option gilt sowohl für Zertifikate von "bind"-Zeilen als auch für solche von "server"-Zeilen. Einige der zusätzlichen Dateien haben bei Zertifikaten von "server"-Zeilen jedoch keine funktionalen Auswirkungen.

Standardmäßig erkennt HAProxy automatisch zahlreiche Dateien, die nicht in der Konfiguration angegeben sind. Wenn Sie die Startzeit optimieren möchten, können Sie dieses Verhalten deaktivieren.

"none": Lädt nur die in der Konfiguration angegebenen Dateien. Wenn eine Datei nicht existiert, wird nicht versucht, ein Zertifikatsbundle zu laden. Bei einem Verzeichnis wird nicht versucht, Zertifikate mit demselben Basisnamen zu einem Bundle zusammenzufassen.

"all": Dies ist das Standardverhalten. Es wird versucht, alles zu laden: Zertifikatsbundles, sctl, ocsp, issuer, key.

"bundle": Wenn eine in der Konfiguration angegebene Datei nicht existiert, versucht HAProxy, ein "Zertifikatsbundle" zu laden. Zertifikatsbundles werden nur auf der Frontend-Seite verwaltet und funktionieren nicht für Backend-Zertifikate.

Seit HAProxy 2.3 werden die Bundles nicht mehr in denselben OpenSSL-Zertifikatsspeicher geladen. Stattdessen wird jedes Zertifikat in einen eigenen Speicher geladen, was der Angabe mehrerer "crt" entspricht. Dafür ist OpenSSL 1.1.1 erforderlich. Bundles dienen somit nur noch der Abwärtskompatibilität und sind für eine hybride RSA/ECC-bind-Konfiguration nicht mehr erforderlich.

Damit HAProxy diese PEM-Dateien als "Zertifikatsbundle" erkennt, müssen sie wie folgt benannt werden: Alle zu einem Bundle zusammenzufassenden PEM-Dateien müssen denselben Basisnamen und ein Suffix haben, das den Schlüsseltyp angibt. Derzeit werden drei Suffixe unterstützt: rsa, dsa und ecdsa. Wenn beispielsweise [www.example.com](http://www.example.com) zwei PEM-Dateien hat, eine RSA-Datei und eine ECDSA-Datei, müssen sie "example.pem.rsa" und "example.pem.ecdsa" heißen. Der erste Teil des Dateinamens ist beliebig; nur das Suffix ist entscheidend. Um dieses Bundle in HAProxy zu laden, geben Sie nur den Basisnamen an:

Beispiel: bind :8443 ssl crt example.pem

Beachten Sie, dass das Suffix nicht an HAProxy übergeben wird. Dadurch wird HAProxy angewiesen, nach einem Zertifikatsbundle zu suchen.

HAProxy lädt alle PEM-Dateien des Bundles so, als wären sie einzeln mit mehreren "crt" konfiguriert worden.

Das Laden von Bundles hat keine Auswirkungen mehr auf das Laden von Verzeichnissen, da die Dateien einzeln geladen werden.

In der CLI werden Bundles als separate Dateien behandelt. Für ihren Commit ist die Bundle-Erweiterung erforderlich.

OCSP-Dateien (.ocsp), Ausstellerdateien (.issuer), Certificate Transparency (.sctl) sowie private Schlüssel (.key) werden beim Bündeln mehrerer Zertifikate unterstützt.

"sctl": Versucht, für jedes Schlüsselwort crt die Datei "`<basename>`.sctl" zu laden. Wenn sie für ein Backend-Zertifikat bereitgestellt wird, wird sie zwar geladen, hat aber keine funktionalen Auswirkungen.

"ocsp": Versucht, für jedes Schlüsselwort crt die Datei "`<basename>`.ocsp" zu laden. Wenn sie für ein Backend-Zertifikat bereitgestellt wird, wird sie zwar geladen, hat aber keine funktionalen Auswirkungen.

"issuer": Versucht, die Datei "`<basename>`.issuer" zu laden, wenn der Aussteller der OCSP-Datei nicht in der PEM-Datei enthalten ist. Wenn sie für ein Backend-Zertifikat bereitgestellt wird, wird sie zwar geladen, hat aber keine funktionalen Auswirkungen.

"key": Wenn die PEM-Datei keinen privaten Schlüssel enthält, wird versucht, eine Datei "`<basename>`.key" mit einem privaten Schlüssel zu laden.

Das Standardverhalten ist "all".

Beispiel:

```text
ssl-load-extra-files bundle sctl
ssl-load-extra-files sctl ocsp issuer
ssl-load-extra-files none
```

Siehe auch: "crt", [Abschnitt 5.1](/de/haproxy/bind-and-server-options/#section-5-1) zu bind-Optionen und [Abschnitt 5.2](/de/haproxy/bind-and-server-options/#section-5-2) zu Serveroptionen.

<a id="entry-3-1-ssl-security-level"></a>

**`ssl-security-level <number>`**

```haproxy
ssl-security-level <number>
```

Diese Direktive ermöglicht die Auswahl der OpenSSL-Sicherheitsstufe, wie unter <https://www.openssl.org/docs/man1.1.1/man3/SSL_CTX_set_security_level.html> beschrieben. Die Sicherheitsstufe wird auf alle SSL-Kontexte in HAProxy angewendet. Es werden nur Werte zwischen 0 und 5 unterstützt.

Der Standardwert hängt von Ihrer OpenSSL-Version, der Distribution und davon ab, wie die Bibliothek kompiliert wurde.

Diese Direktive erfordert mindestens OpenSSL 1.1.1.

<a id="entry-3-1-ssl-server-verify"></a>

**`ssl-server-verify [none|required]`**

```haproxy
ssl-server-verify [none|required]
```

Legt das Standardverhalten für die SSL-Verifizierung auf der Serverseite fest. Bei 'none' werden Serverzertifikate nicht geprüft. Der Standardwert ist 'required', sofern das Verhalten nicht mit der Befehlszeilenoption '-dV' erzwungen wird.

<a id="entry-3-1-ssl-skip-self-issued-ca"></a>

**`ssl-skip-self-issued-ca`**

```haproxy
ssl-skip-self-issued-ca
```

Eine selbstausgestellte CA, auch x509-Root-CA genannt, bildet den Vertrauensanker für die Kettenvalidierung. Sie als Server zu senden ist nutzlos; der Client muss sie bereits besitzen. In einer Standardkonfiguration darf eine solche CA nicht in der PEM-Datei enthalten sein. Mit dieser Option können Sie sie in der PEM-Datei behalten, ohne sie an den Client zu senden. Ein Anwendungsfall ist die Bereitstellung des Ausstellers für ocsp ohne eine '.issuer'-Datei, wobei er über 'issuers-chain-path' gemeinsam genutzt werden kann. Dies betrifft alle Zertifikate ohne Zwischenzertifikate. Für BoringSSL ist diese Option nutzlos; .issuer wird ignoriert, da die ocsp-Funktionen dies nicht benötigen. Erfordert mindestens OpenSSL 1.0.2.

<a id="entry-3-1-stats-calculate-max-counters"></a>

**`stats calculate-max-counters [on|off]`**

```haproxy
stats calculate-max-counters [on|off]
```

Aktiviert oder deaktiviert die Berechnung der Maximalwertzähler für die Statistik. Wenn Sie diese nicht benötigen, kann ihre Deaktivierung die Leistung etwas erhöhen. Der Standardwert ist on.

<a id="entry-3-1-stats-maxconn"></a>

**`stats maxconn <connections>`**

```haproxy
stats maxconn <connections>
```

Standardmäßig ist der Statistik-Socket auf 10 gleichzeitige Verbindungen begrenzt. Dieser Wert kann mit "stats maxconn" geändert werden.

<a id="entry-3-1-stats-socket"></a>

**`stats socket [<address:port>|<path>] [param*]`**

```haproxy
stats socket [<address:port>|<path>] [param*]
```

Bindet einen UNIX-Socket an `<path>` oder eine TCPv4/v6-Adresse an `<address:port>`. Verbindungen zu diesem Socket liefern verschiedene Statistikausgaben und ermöglichen sogar die Ausführung einiger Befehle, um bestimmte Laufzeiteinstellungen zu ändern. Weitere Einzelheiten finden Sie in [Abschnitt 9.3](/de/haproxy/statistics-and-monitoring/#section-9-3) "Unix-Socket-Befehle" des Verwaltungshandbuchs.

Alle von "bind"-Zeilen unterstützten Parameter werden unterstützt, beispielsweise um den Zugriff auf bestimmte Benutzer zu beschränken oder deren Zugriffsrechte einzuschränken. Weitere Informationen finden Sie in [Abschnitt 5.1](/de/haproxy/bind-and-server-options/#section-5-1).

<a id="entry-3-1-stats-timeout"></a>

**`stats timeout <timeout, in milliseconds>`**

```haproxy
stats timeout <timeout, in milliseconds>
```

Die standardmäßige Zeitüberschreitung des Statistik-Sockets beträgt 10 Sekunden. Dieser Wert kann mit "stats timeout" geändert werden. Der Wert muss in Millisekunden angegeben werden oder mit einer Zeiteinheit aus { us, ms, s, m, h, d } versehen sein.

<a id="entry-3-1-stats-file"></a>

**`stats-file <path>`**

```haproxy
stats-file <path>
```

Pfad zu einer erzeugten haproxy-Statistikdatei. Beim Start lädt haproxy die Werte in seine internen Zähler. Mit dem CLI-Befehl "dump stats-file" wird eine solche Statistikdatei erzeugt. Weitere Einzelheiten finden Sie im Verwaltungshandbuch.

<a id="entry-3-1-stress-level"></a>

**`stress-level <level>`**

```haproxy
stress-level <level>
```

Aktiviert alternativen Code, um die haproxy-Programmdatei gezielt zu belasten. Die Stufe ist eine ganze Zahl von 0 bis 9. Der Standardwert 0 deaktiviert jede belastende Ausführung. Die Stufen von 1 bis 9 erhöhen den Belastungsdruck auf die haproxy-Programmdatei. Beachten Sie, dass jede positive Stufe die Leistung erheblich beeinträchtigen kann. Daher sollte dies ausschließlich zur Fehlerdiagnose und auf Anforderung eines Entwicklers aktiviert werden.

<a id="entry-3-1-strict-limits"></a>

**`strict-limits`**

```haproxy
strict-limits
```

Lässt den Prozessstart fehlschlagen, wenn ein setrlimit-Aufruf fehlschlägt. HAProxy versucht, auf Grundlage seiner Berechnungen das bestmögliche setrlimit zu setzen. Schlägt dies fehl, wird eine Warnung ausgegeben. Diese Option stellt sicher, dass HAProxy ausdrücklich fehlschlägt, wenn das Setzen dieser Limits scheitert. Sie ist standardmäßig aktiviert. Durch Voranstellen des Schlüsselworts "no" kann sie dennoch ausdrücklich deaktiviert werden.

<a id="entry-3-1-thread-group"></a>

**`thread-group <group> [<thread-range>...]`**

```haproxy
thread-group <group> [<thread-range>...]
```

Diese Einstellung ist nur verfügbar, wenn die Unterstützung für Threads einkompiliert wurde. Sie führt die Threads auf, aus denen die Thread-Gruppe `<group>` bestehen soll. Thread- und Gruppennummern beginnen bei 1. Thread-Bereiche werden entweder durch einzelne Thread-Nummern oder durch eine Unter- und Obergrenze angegeben, die durch einen Bindestrich '-' getrennt sind (z. B. "1-16"). Nicht zugewiesene Threads werden automatisch nicht zugewiesenen Thread-Gruppen zugeordnet. Mit dieser Direktive definierte Thread-Gruppen erhalten niemals mehr Threads als angegeben. Wird dieselbe Gruppe mehrfach definiert, überschreibt die neue Definition die vorherigen. Siehe auch "nbthread" und "thread-groups".

<a id="entry-3-1-thread-groups"></a>

**`thread-groups <number>`**

```haproxy
thread-groups <number>
```

Diese Einstellung ist nur verfügbar, wenn die Unterstützung für Threads einkompiliert wurde. Sie teilt die Threads von HAProxy in `<number>` unabhängige Gruppen auf. Derzeit ist der Standardwert 1. Mit Thread-Gruppen lässt sich die gemeinsame Nutzung von Ressourcen zwischen Threads verringern, um Konkurrenz zu begrenzen; dies erfordert allerdings etwas zusätzlichen Konfigurationsaufwand. Es ist auch die einzige Möglichkeit, mehr als 64 Threads zu verwenden, da pro Gruppe bis zu 64 Threads konfiguriert werden können. Die maximale Anzahl von Gruppen wird beim Kompilieren festgelegt und beträgt standardmäßig 16. Siehe auch "nbthread".

<a id="entry-3-1-thread-hard-limit"></a>

**`thread-hard-limit <number>`**

```haproxy
thread-hard-limit <number>
```

Diese Einstellung erzwingt eine Obergrenze für die Anzahl der Threads, unabhängig davon, ob diese ermittelt oder konfiguriert wurde. Dies ist besonders auf Betriebssystemen mit automatischer Ermittlung der Thread-Anzahl nützlich, wenn in allgemeinen und portablen Konfigurationen weniger Threads als CPUs gewünscht sind. Während "nbthread" eine feste Thread-Anzahl erzwingt, die bei Überschreiten der verfügbaren CPUs zu einer Warnung und schlechter Leistung führt, begrenzt thread-hard-limit nur den Höchstwert. Es beschränkt die Thread-Anzahl automatisch auf diesen Wert, erhöht aber niedrigere Werte nicht. Wird "nbthread" auf einen höheren Wert festgelegt, hat thread-hard-limit Vorrang, und eine Warnung wird ausgegeben, damit die Unstimmigkeit in der Konfiguration behoben werden kann. Standardmäßig gibt es keine Begrenzung. Siehe auch "nbthread".

<a id="entry-3-1-uid"></a>

**`uid <number>`**

```haproxy
uid <number>
```

Ändert die Benutzer-ID des Prozesses auf `<number>`. Es wird empfohlen, diese Benutzer-ID ausschließlich für HAProxy oder eine kleine Gruppe ähnlicher Daemons zu verwenden. HAProxy muss mit Superuser-Rechten gestartet werden, um zu einer anderen Benutzer-ID wechseln zu können. Siehe auch "gid" und "user".

<a id="entry-3-1-ulimit-n"></a>

**`ulimit-n <number>`**

```haproxy
ulimit-n <number>
```

Setzt die maximale Anzahl von Dateideskriptoren pro Prozess auf `<number>`. Standardmäßig wird sie automatisch berechnet, weshalb empfohlen wird, diese Option nicht zu verwenden. Wenn lediglich die Anzahl der Dateideskriptoren begrenzt werden soll, verwenden Sie besser "fd-hard-limit".

Beachten Sie, dass dynamische Server bei dieser automatischen Ressourcenberechnung nicht berücksichtigt werden. Bei einer großen Anzahl solcher Server kann es erforderlich sein, den Wert manuell anzugeben.

Siehe auch: fd-hard-limit, maxconn

unix-bind [ prefix `<prefix>` ] [ mode `<mode>` ] [ user `<user>` ] [ uid `<uid>` ] [ group
`<group>` ] [ gid `<gid>` ]

Legt gemeinsame Einstellungen für UNIX-Listener-Sockets fest, die in "bind"-Anweisungen deklariert werden. Dies dient hauptsächlich dazu, die Deklaration dieser UNIX-Sockets zu vereinfachen und das Fehlerrisiko zu verringern, da diese Einstellungen meist erforderlich, aber zugleich prozessspezifisch sind. Mit `<prefix>` lässt sich erzwingen, dass alle Socket-Pfade relativ zu diesem Verzeichnis angegeben werden. Dies kann für den Zugriff auf die chroot-Umgebung einer anderen Komponente erforderlich sein. Beachten Sie, dass diese Pfade aufgelöst werden, bevor HAProxy selbst chroot ausführt; sie sind daher absolut. `<mode>`, `<user>`, `<uid>`, `<group>` und `<gid>` haben dieselbe Bedeutung wie die gleichnamigen Parameter der "bind"-Anweisung. Wenn beide angegeben sind, hat die "bind"-Anweisung Vorrang. Die "unix-bind"-Einstellungen können somit als prozessweite Standardwerte betrachtet werden.

<a id="entry-3-1-unsetenv"></a>

**`unsetenv [<name> ...]`**

```haproxy
unsetenv [<name> ...]
```

Entfernt die als Argumente angegebenen Umgebungsvariablen. Dies kann nützlich sein, um vertrauliche Informationen zu verbergen, die bei bestimmten Vorgängen gelegentlich aus der Umgebung des Benutzers übernommen werden. Nicht vorhandene Variablen werden ohne Meldung ignoriert, sodass nach dem Vorgang sicher keine dieser Variablen mehr vorhanden ist. Die Änderungen werden sofort wirksam, sodass bereits die nächste Zeile in der Konfigurationsdatei diese Variablen nicht mehr sieht. Siehe auch "setenv", "presetenv" und "resetenv".

<a id="entry-3-1-user"></a>

**`user <user name>`**

```haproxy
user <user name>
```

Ähnlich wie "uid", verwendet jedoch die UID des Benutzernamens `<user name>` aus /etc/passwd. Siehe auch "uid" und "group".

<a id="entry-3-1-node"></a>

**`node <name>`**

```haproxy
node <name>
```

Wie bei DNS-Namen sind nur Buchstaben, Ziffern, Bindestriche und Unterstriche erlaubt.

Diese Anweisung ist in HA-Konfigurationen nützlich, in denen mindestens zwei Prozesse oder Server dieselbe IP-Adresse nutzen. Durch unterschiedliche Knotennamen auf allen Knoten lässt sich sofort erkennen, welcher Server den Datenverkehr verarbeitet.

<a id="entry-3-1-wurfl-cache-size"></a>

**`wurfl-cache-size <size>`**

```haproxy
wurfl-cache-size <size>
```

Legt die Größe des WURFL-User-Agent-Caches fest. Für schnellere Abfragen werden bereits verarbeitete User-Agents in einem LRU-Cache vorgehalten:

- "0" : Es wird kein Cache verwendet.
- `<size>` : Größe des lru-Caches in Elementen.

Beachten Sie, dass diese Option nur verfügbar ist, wenn HAProxy mit USE_WURFL=1 kompiliert wurde.

<a id="entry-3-1-wurfl-data-file"></a>

**`wurfl-data-file <file path>`**

```haproxy
wurfl-data-file <file path>
```

Der Pfad der WURFL-Datendatei zur Bereitstellung von Geräteerkennungsdiensten. Die Datei sollte mit den entsprechenden Berechtigungen für HAProxy zugänglich sein.

Beachten Sie, dass diese Option nur verfügbar ist, wenn HAProxy mit USE_WURFL=1 kompiliert wurde.

<a id="entry-3-1-wurfl-information-list"></a>

**`wurfl-information-list [<capability>]*`**

```haproxy
wurfl-information-list [<capability>]*
```

Eine durch Leerzeichen getrennte Liste von WURFL-Capabilities, virtuellen Capabilities und Eigenschaftsnamen, die in eingefügten Headern verwendet werden sollen. Eine vollständige Liste der Namen von Capabilities und virtuellen Capabilities ist auf der Website von Scientiamobile verfügbar:

```text
https://www.scientiamobile.com/wurflCapability
```

Gültige WURFL-Eigenschaften sind:

- wurfl_id Enthält die Geräte-ID des gefundenen Geräts.

- wurfl_root_id Enthält die Root-Geräte-ID des gefundenen Geräts.

- wurfl_isdevroot Gibt an, ob das gefundene Gerät ein Root-Gerät ist. Mögliche Werte sind "TRUE" oder "FALSE".

- wurfl_useragent Der ursprüngliche User-Agent dieser konkreten Webanfrage.

- wurfl_api_version Enthält eine Zeichenfolge, die die aktuell verwendete Libwurfl-API-Version darstellt.

- wurfl_info Eine Zeichenfolge mit Informationen zur eingelesenen wurfl.xml und ihrem vollständigen Pfad.

- wurfl_last_load_time Enthält den UNIX-Zeitstempel des letzten erfolgreichen Ladens von WURFL.

- wurfl_normalized_useragent Der normalisierte User-Agent.

Beachten Sie, dass diese Option nur verfügbar ist, wenn HAProxy mit USE_WURFL=1 kompiliert wurde.

<a id="entry-3-1-wurfl-information-list-separator"></a>

**`wurfl-information-list-separator <char>`**

```haproxy
wurfl-information-list-separator <char>
```

Ein Zeichen, das Werte in einem Antwort-Header mit WURFL-Ergebnissen trennt. Falls es nicht gesetzt ist, wird standardmäßig ein Komma (',') verwendet.

Beachten Sie, dass diese Option nur verfügbar ist, wenn HAProxy mit USE_WURFL=1 kompiliert wurde.

<a id="entry-3-1-wurfl-patch-file"></a>

**`wurfl-patch-file [<file path>]`**

```haproxy
wurfl-patch-file [<file path>]
```

Eine Liste von Pfaden zu WURFL-Patchdateien. Beachten Sie, dass Patches beim Start und somit vor chroot geladen werden.

Beachten Sie, dass diese Option nur verfügbar ist, wenn HAProxy mit USE_WURFL=1 kompiliert wurde.

## 3.2. Leistungsoptimierung {#section-3-2}

<a id="entry-3-2-busy-polling"></a>

**`busy-polling`**

```haproxy
busy-polling
```

In manchen Situationen, insbesondere bei niedrigen Latenzanforderungen auf Prozessoren mit variabler Taktfrequenz oder beim Betrieb in virtuellen Maschinen, geht der Prozessor jedes Mal in den Ruhezustand oder wird für längere Zeit einer anderen VM zugeteilt, wenn der Prozess mit dem Poller auf I/O wartet. Dies verursacht übermäßig hohe Latenzen. Diese Option verhindert, dass der Prozessor in den Ruhezustand wechselt, indem sie für die Poller stets eine Zeitüberschreitung von null verwendet. Dies verringert die Latenz erheblich (beobachtet wurden 30 bis 100 Mikrosekunden), birgt jedoch das Risiko einer Überhitzung des Prozessors. Die Option kann auch mit Threads verwendet werden. In diesem Fall können falsch gebundene Threads stark miteinander konkurrieren, was zu schlechterer Leistung und hohen Werten in den Feldern für entzogene CPU-Zeit in der Ausgabe von "show info" führt; daran lassen sich die falsch konfigurierten Threads erkennen. Bei Verwendung dieser Option darf der Prozess nicht auf demselben Prozessor wie die Netzwerk-Interrupts laufen. Außerdem sollte die Option möglichst nicht auf mehreren CPU-Threads verwendet werden, die sich denselben Kern teilen. Sie ist standardmäßig deaktiviert. Wenn sie aktiviert wurde, kann sie dennoch durch Voranstellen des Schlüsselworts "no" ausdrücklich deaktiviert werden. Die Poller "select" und "poll" ignorieren sie.

Bei einem nahtlosen Neuladen wird diese Option für alte Prozesse automatisch deaktiviert. Dadurch wird übermäßige CPU-Konkurrenz vermieden, wenn mehrere Prozesse noch eine Zeit lang auf das Ende ihrer bestehenden Verbindungen warten.

<a id="entry-3-2-max-spread-checks"></a>

**`max-spread-checks <delay in milliseconds>`**

```haproxy
max-spread-checks <delay in milliseconds>
```

Standardmäßig versucht HAProxy, den Beginn der Zustandsprüfungen über das kleinste Prüfintervall aller Server einer Serverfarm zu verteilen. Damit soll eine geballte Belastung der auf demselben Server laufenden Dienste vermieden werden. Bei großen Prüfintervallen (10 Sekunden oder mehr) dauert es jedoch einige Zeit, bis die letzten Server der Serverfarm erstmals geprüft werden, was problematisch sein kann. Dieser Parameter erzwingt eine Obergrenze für die Verzögerung zwischen der ersten und der letzten Prüfung, auch wenn die Prüfintervalle der Server größer sind. Kürzere Prüfintervalle der Server werden jedoch weiterhin eingehalten.

<a id="entry-3-2-maxcompcpuusage"></a>

**`maxcompcpuusage <number>`**

```haproxy
maxcompcpuusage <number>
```

Legt die maximale CPU-Auslastung fest, die HAProxy erreichen darf, bevor die Komprimierung für neue Anfragen eingestellt oder die Komprimierungsstufe laufender Anfragen verringert wird. Dies funktioniert wie 'maxcomprate', misst jedoch die CPU-Auslastung anstelle der Bandbreite eingehender Daten. Der Wert wird als Prozentsatz der von HAProxy genutzten CPU angegeben. Der Wert 100 deaktiviert die Begrenzung. Der Standardwert ist 100. Ein niedrigerer Wert verhindert, dass die Komprimierungsarbeit den gesamten Prozess verlangsamt und hohe Latenzen verursacht.

<a id="entry-3-2-maxcomprate"></a>

**`maxcomprate <number>`**

```haproxy
maxcomprate <number>
```

Setzt die maximale Eingaberate für die Komprimierung pro Prozess auf `<number>` Kilobyte pro Sekunde. Wird das Maximum erreicht, wird die Komprimierungsstufe jedes Streams während seiner Verarbeitung verringert. Ist das Maximum bereits zu Beginn eines Streams erreicht, wird dieser überhaupt nicht komprimiert. Ist das Maximum nicht erreicht, wird die Komprimierungsstufe bis auf tune.comp.maxlevel erhöht. Der Wert null bedeutet, dass es keine Begrenzung gibt; dies ist der Standardwert.

<a id="entry-3-2-maxconn"></a>

**`maxconn <number>`**

```haproxy
maxconn <number>
```

Setzt die maximale Anzahl gleichzeitiger Verbindungen pro Prozess auf `<number>`. Dies entspricht dem Befehlszeilenargument "-n". Der über "-n" angegebene Wert hat Vorrang vor dem im globalen Abschnitt gesetzten maxconn-Wert. Der Haproxy-Prozess kann auch mit der Kompilierungsvariablen SYSTEM_MAXCONN erstellt werden, die dann als systemweiter Höchstwert für maxconn dient. Auch diese Grenze kann zur Laufzeit mit dem Befehlszeilenargument "-n" überschritten werden, falls SYSTEM_MAXCONN gesetzt ist. Proxys nehmen keine weiteren Verbindungen an, sobald maxconn erreicht ist. Das weiche Dateideskriptorlimit des Prozesses (abrufbar mit dem Befehl "ulimit -n") wird anhand des angegebenen maxconn-Werts automatisch angepasst. Siehe auch "ulimit-n". Hinweis: Der Poller "select" kann auf einigen Plattformen nicht zuverlässig mehr als 1024 Dateideskriptoren verwenden. Wenn Ihre Plattform nur select unterstützt und beim Start "select FAILED" meldet, müssen Sie maxconn so weit verringern, bis es funktioniert (im Allgemeinen auf etwas unter 500). Wenn maxconn nicht gesetzt ist, wird der Wert anhand der aktuellen Dateideskriptorlimits automatisch berechnet, die der Befehl "ulimit -nH" meldet (verwendet wird der größere der harten und weichen Werte). Anschließend wird der automatische Wert gegebenenfalls durch "fd-hard-limit" und durch ein mit der Befehlszeilenoption "-m" erzwungenes Speicherlimit verringert. Der automatische Wert hängt außerdem von der Puffergröße, dem für die Komprimierung zugewiesenen Speicher, der SSL-Cachegröße sowie der Verwendung von SSL und dem zugehörigen maxsslconn ab (das ebenfalls automatisch bestimmt werden kann).

Siehe auch: fd-hard-limit, ulimit-n

<a id="entry-3-2-maxconnrate"></a>

**`maxconnrate <number>`**

```haproxy
maxconnrate <number>
```

Setzt die maximale Anzahl von Verbindungen pro Sekunde und Prozess auf `<number>`. Proxys nehmen keine weiteren Verbindungen an, sobald diese Grenze erreicht ist. Damit lässt sich die Gesamtkapazität unabhängig von der Kapazität jedes einzelnen Frontends begrenzen. Beachten Sie, dass dies nur als Schutzmaßnahme für den Dienst eingesetzt werden kann: Bei Erreichen der Grenze ist eine faire Aufteilung zwischen den Frontends nicht unbedingt gewährleistet. Daher ist es sinnvoll, jedes Frontend zusätzlich auf einen Wert nahe seinem erwarteten Anteil zu begrenzen. Auch eine Verringerung von tune.maxaccept kann die Verteilung gerechter machen.

<a id="entry-3-2-maxpipes"></a>

**`maxpipes <number>`**

```haproxy
maxpipes <number>
```

Setzt die maximale Anzahl von Pipes pro Prozess auf `<number>`. Derzeit werden Pipes nur für kernelbasiertes TCP-Splicing verwendet. Da eine Pipe zwei Dateideskriptoren enthält, wird der Wert von "ulimit-n" entsprechend erhöht. Der Standardwert ist maxconn/4, was selbst für die meisten hohen Belastungen mehr als ausreichend erscheint. Der Splice-Code weist Pipes dynamisch zu, gibt sie wieder frei und kann auf normales Kopieren zurückfallen. Ein zu niedriger Wert kann daher lediglich die Leistung beeinträchtigen.

<a id="entry-3-2-maxsessrate"></a>

**`maxsessrate <number>`**

```haproxy
maxsessrate <number>
```

Setzt die maximale Anzahl von Sitzungen pro Sekunde und Prozess auf `<number>`. Proxys nehmen keine weiteren Verbindungen an, sobald diese Grenze erreicht ist. Damit lässt sich die Gesamtkapazität unabhängig von der Kapazität jedes einzelnen Frontends begrenzen. Beachten Sie, dass dies nur als Schutzmaßnahme für den Dienst eingesetzt werden kann: Bei Erreichen der Grenze ist eine faire Aufteilung zwischen den Frontends nicht unbedingt gewährleistet. Daher ist es sinnvoll, jedes Frontend zusätzlich auf einen Wert nahe seinem erwarteten Anteil zu begrenzen. Auch eine Verringerung von tune.maxaccept kann die Verteilung gerechter machen.

<a id="entry-3-2-maxsslconn"></a>

**`maxsslconn <number>`**

```haproxy
maxsslconn <number>
```

Setzt die maximale Anzahl gleichzeitiger SSL-Verbindungen pro Prozess auf `<number>`. Standardmäßig gibt es keine SSL-spezifische Begrenzung; die globale Einstellung maxconn gilt somit für alle Verbindungen. Diese Begrenzung verhindert, dass openssl zu viel Speicher verwendet und abstürzt, wenn malloc NULL zurückgibt (da dieser Fall leider nicht zuverlässig geprüft wird). Beachten Sie, dass die Grenze sowohl für eingehende als auch für ausgehende Verbindungen gilt. Eine Verbindung, die entschlüsselt und anschließend wieder verschlüsselt wird, zählt daher als 2 SSL-Verbindungen. Wenn dieser Wert nicht gesetzt ist, aber ein Speicherlimit erzwungen wird, wird er automatisch anhand des Speicherlimits, von maxconn, der Puffergröße, des für die Komprimierung zugewiesenen Speichers, der SSL-Cachegröße und der Verwendung von SSL in Frontends, Backends oder beiden berechnet. Wenn bei vorhandenem Speicherlimit weder maxconn noch maxsslconn angegeben sind, passt HAProxy diese Werte automatisch so an, dass 100% der Verbindungen gefahrlos über SSL erfolgen können. Dabei werden die Seiten berücksichtigt, auf denen SSL aktiviert ist (Frontend, Backend oder beide).

<a id="entry-3-2-maxsslrate"></a>

**`maxsslrate <number>`**

```haproxy
maxsslrate <number>
```

Setzt die maximale Anzahl von SSL-Sitzungen pro Sekunde und Prozess auf `<number>`. SSL-Listener nehmen keine weiteren Verbindungen an, sobald diese Grenze erreicht ist. Damit lässt sich die gesamte SSL-CPU-Auslastung unabhängig von der Kapazität jedes einzelnen Frontends begrenzen. Beachten Sie, dass dies nur als Schutzmaßnahme für den Dienst eingesetzt werden kann: Bei Erreichen der Grenze ist eine faire Aufteilung zwischen den Frontends nicht unbedingt gewährleistet. Daher ist es sinnvoll, jedes Frontend zusätzlich auf einen Wert nahe seinem erwarteten Anteil zu begrenzen. Beachten Sie außerdem, dass Sitzungen vor dem Eintritt in den SSL-Stack gezählt werden, nicht danach. Dies schützt den Stack auch vor fehlerhaften Handshakes. Auch eine Verringerung von tune.maxaccept kann die Verteilung gerechter machen.

<a id="entry-3-2-maxzlibmem"></a>

**`maxzlibmem <number>`**

```haproxy
maxzlibmem <number>
```

Legt die maximale Menge an RAM in Megabyte fest, die zlib pro Prozess verwenden darf. Sobald diese Menge erreicht ist, werden neue Streams nicht komprimiert, solange kein RAM verfügbar ist. Bei 0 gibt es keine Begrenzung. Der Standardwert ist 0. Der Wert kann in Byte über den UNIX-Socket mit "show info" in der Zeile "MaxZlibMemUsage" abgefragt werden; der von zlib verwendete Speicher wird unter "ZlibMemUsage" ebenfalls in Byte angezeigt.

<a id="entry-3-2-no-memory-trimming"></a>

**`no-memory-trimming`**

```haproxy
no-memory-trimming
```

Deaktiviert das Freigeben ungenutzten Speichers ("malloc_trim") zu den wenigen Zeitpunkten, an denen versucht wird, große Speichermengen zurückzugewinnen (bei Speichermangel oder beim Neuladen). Dabei wird der Speicherzuweiser des Systems gezwungen, alle ungenutzten Bereiche zu durchsuchen und freizugeben. Dies gilt im Allgemeinen als sinnvolle Maßnahme, um einem neuen Prozess mehr Speicher zu überlassen, den der alte voraussichtlich kaum noch nutzen wird. Auf einigen Systemen mit Zehntausenden bis Hunderttausenden gleichzeitigen Verbindungen kann jedoch starke Speicherfragmentierung auftreten, wodurch die Freigabe extrem lange dauert. Währenddessen fließt kein Datenverkehr mehr durch den Prozess, neue Verbindungen werden nicht mehr angenommen, einige Zustandsprüfungen können sogar fehlschlagen, und der Watchdog kann den nicht reagierenden Prozess beenden, wodurch ein riesiges Speicherabbild entsteht. Falls dies auftritt, wird empfohlen, mit dieser Option die Speicherbereinigung zu deaktivieren und nicht länger zu versuchen, dem neuen Prozess Speicher zu überlassen. Fortschrittliche Speicherzuweiser sind von diesem Problem normalerweise nicht betroffen.

<a id="entry-3-2-noepoll"></a>

**`noepoll`**

```haproxy
noepoll
```

Deaktiviert die Verwendung des Ereignisabfragesystems "epoll" unter Linux. Dies entspricht dem Befehlszeilenargument "-de". Als nächstes Abfragesystem wird im Allgemeinen "poll" verwendet. Siehe auch "nopoll".

<a id="entry-3-2-noevports"></a>

**`noevports`**

```haproxy
noevports
```

Deaktiviert die Verwendung des Ereignisabfragesystems event ports auf SunOS-Systemen, die von Solaris 10 oder höher abgeleitet sind. Dies entspricht dem Befehlszeilenargument "-dv". Als nächstes Abfragesystem wird im Allgemeinen "poll" verwendet. Siehe auch "nopoll".

<a id="entry-3-2-nogetaddrinfo"></a>

**`nogetaddrinfo`**

```haproxy
nogetaddrinfo
```

Deaktiviert die Verwendung von getaddrinfo(3) zur Namensauflösung. Dies entspricht dem Befehlszeilenargument "-dG". Stattdessen wird das veraltete gethostbyname(3) verwendet.

<a id="entry-3-2-nokqueue"></a>

**`nokqueue`**

```haproxy
nokqueue
```

Deaktiviert die Verwendung des Ereignisabfragesystems "kqueue" unter BSD. Dies entspricht dem Befehlszeilenargument "-dk". Als nächstes Abfragesystem wird im Allgemeinen "poll" verwendet. Siehe auch "nopoll".

<a id="entry-3-2-noktls"></a>

**`noktls`**

```haproxy
noktls
```

Deaktiviert die Verwendung von ktls. Dies entspricht dem Befehlszeilenargument "-dT".

<a id="entry-3-2-nopoll"></a>

**`nopoll`**

```haproxy
nopoll
```

Deaktiviert die Verwendung des Ereignisabfragesystems "poll". Dies entspricht dem Befehlszeilenargument "-dp". Als nächstes Abfragesystem wird "select" verwendet. Es sollte niemals erforderlich sein, "poll" zu deaktivieren, da es auf allen von HAProxy unterstützten Plattformen verfügbar ist. Siehe auch "nokqueue", "noepoll" und "noevports".

<a id="entry-3-2-noreuseport"></a>

**`noreuseport`**

```haproxy
noreuseport
```

Deaktiviert die Verwendung von SO_REUSEPORT; siehe socket(7). Dies entspricht dem Befehlszeilenargument "-dR".

<a id="entry-3-2-nosplice"></a>

**`nosplice`**

```haproxy
nosplice
```

Deaktiviert kernelbasiertes TCP-Splicing zwischen Sockets unter Linux. Dies entspricht dem Befehlszeilenargument "-dS". Daten werden dann mit herkömmlichen und portableren recv/send-Aufrufen kopiert. Kernelbasiertes TCP-Splicing ist auf einige sehr neue Varianten des Kernels 2.6 beschränkt. Die meisten Versionen zwischen 2.6.25 und 2.6.28 sind fehlerhaft und leiten beschädigte Daten weiter; sie dürfen daher nicht verwendet werden. Diese Option erleichtert es, Kernel-Splicing im Zweifelsfall global zu deaktivieren. Siehe auch "option splice-auto", "option splice-request" und "option splice-response".

<a id="entry-3-2-profiling-memory"></a>

**`profiling.memory { on | off }`**

```haproxy
profiling.memory { on | off }
```

Aktiviert ('on') oder deaktiviert ('off') die Speicherprofilierung pro Funktion. Dabei werden Nutzungsstatistiken der malloc/calloc/realloc/free-Aufrufe im gesamten Prozess einschließlich der Bibliotheken erfasst und über den CLI-Befehl "show profiling" ausgegeben. Dies ist vor allem für Fälle gedacht, in denen eine ungewöhnliche Speichernutzung beobachtet wird, die sich nicht durch die Pools erklären lässt, und weitere Informationen benötigt werden. Die Leistungseinbuße liegt typischerweise bei etwa 1%, auf Rechnern mit vielen Threads möglicherweise etwas höher; daher eignet sich dies normalerweise für den Produktionseinsatz. Dasselbe lässt sich zur Laufzeit mit dem CLI-Befehl "set profiling memory" erreichen; siehe das Verwaltungshandbuch.

<a id="entry-3-2-profiling-tasks"></a>

**`profiling.tasks { auto | on | off | lock | no-lock | memory | no-memory }*`**

```haproxy
profiling.tasks { auto | on | off | lock | no-lock | memory | no-memory }*
```

Aktiviert ('on') oder deaktiviert ('off') die CPU-Profilierung pro Task. Bei 'auto' wird die Profilierung auf einem Thread automatisch aktiviert, sobald dessen durchschnittliche Latenz im Aktivitätsfeld "avg_loop_us" 1000 Mikrosekunden oder mehr erreicht. Sie wird automatisch deaktiviert, wenn die Latenz wieder unter 990 Mikrosekunden fällt (dieser Wert ist ein Mittelwert über die letzten 1024 Schleifendurchläufe, verändert sich also nicht schnell und glättet kurze Spitzen deutlich). Die Profilierung kann sich auf überlasteten Systemen, in Containern oder virtuellen Maschinen auch gelegentlich von selbst aktivieren, ebenso wenn das System auslagert (was auf einem Load-Balancer unter keinen Umständen geschehen darf).

Bei aktivierter Task-Profilierung kann HAProxy zusätzlich erfassen, wie lange jeder Task eine Sperre hält oder auf eine Sperre wartet, sowie die Wartezeit auf eine erfolgreiche Speicherzuweisung bei einem Cache-Miss im Pool. Dies kann helfen, bestimmte Latenzursachen zu verstehen. Dazu können zusätzlich die Schlüsselwörter "lock" (Erfassung von Sperrzeiten aktivieren), "no-lock" (deaktivieren), "memory" (Erfassung der Speicherzuweisungszeiten aktivieren) oder "no-memory" (deaktivieren) angegeben werden. Standardmäßig sind diese nicht aktiviert, da sie auf stark ausgelasteten Systemen einen nicht unerheblichen CPU-Aufwand verursachen können (3-10%). Beachten Sie, dass dieser Zusatzaufwand nur entsteht, wenn die Profilierung tatsächlich läuft. Im Modus "auto" tritt er somit nur auf, wenn HAProxy die Profilierung aktiviert.

Die CPU-Profilierung pro Task kann sehr hilfreich sein, um festzustellen, wofür Zeit aufgewendet wird und welche Anfragen welche Auswirkungen auf andere Anfragen haben. Ihre Aktivierung beeinträchtigt die Gesamtleistung typischerweise um weniger als 1%. Daher wird empfohlen, den Standardwert 'auto' beizubehalten, sodass sie nur arbeitet, wenn ein Problem erkannt wird. Diese Funktion erfordert ein System, das den Systemaufruf clock_gettime(2) mit den Uhrenkennungen CLOCK_MONOTONIC und CLOCK_THREAD_CPUTIME_ID unterstützt; andernfalls beträgt die gemeldete Zeit null. Diese Option kann zur Laufzeit mit "set profiling" in der CLI geändert werden.

<a id="entry-3-2-spread-checks"></a>

**`spread-checks <0..50, in percent>`**

```haproxy
spread-checks <0..50, in percent>
```

Manchmal ist es sinnvoll, Agenten- und Zustandsprüfungen nicht in exakt gleichmäßigen Abständen an Server zu senden, beispielsweise wenn sich viele logische Server auf demselben physischen Server befinden. Mit diesem Parameter kann dem Prüfintervall eine zufällige Abweichung zwischen 0 und +/- 50% hinzugefügt werden. Werte zwischen 2 und 5 scheinen gute Ergebnisse zu liefern. Der Standardwert bleibt 0.

<a id="entry-3-2-ssl-engine"></a>

**`ssl-engine <name> [algo <comma-separated list of algorithms>]`**

```haproxy
ssl-engine <name> [algo <comma-separated list of algorithms>]
```

Setzt die OpenSSL-Engine auf `<name>`. Eine Liste gültiger Werte für `<name>` erhalten Sie mit dem Befehl "openssl engine". Diese Anweisung kann mehrfach verwendet werden; dadurch werden mehrere Kryptografie-Engines aktiviert. Die Angabe einer nicht unterstützten Engine verhindert den Start von HAProxy. Beachten Sie, dass viele Engines eine niedrigere HTTPS-Leistung liefern als reine Software auf modernen Prozessoren. Der optionale Befehl "algo" legt mit der OPENSSL-Funktion ENGINE_set_default_string() die Standardalgorithmen fest, die eine ENGINE bereitstellt. Der Wert "ALL" verwendet die Engine für sämtliche kryptografischen Operationen. Wird keine algo-Liste angegeben, wird "ALL" verwendet. Es kann eine durch Kommas getrennte Liste verschiedener Algorithmen angegeben werden, darunter RSA, DSA, DH, EC, RAND, CIPHERS, DIGESTS, PKEY, PKEY_CRYPTO, PKEY_ASN1. Dies ist dasselbe Format wie in der openssl-Konfigurationsdatei:
<https://www.openssl.org/docs/man1.0.2/apps/config.html>

Mit HAProxy Version 2.6 wurde die Engine-Unterstützung im Standard-Build deaktiviert. Diese Option ist nur verfügbar, wenn HAProxy mit entsprechender Unterstützung erstellt wurde. Falls ssl-engine benötigt wird, kann HAProxy mit dem Flag USE_ENGINE=1 neu kompiliert werden.

<a id="entry-3-2-ssl-mode-async"></a>

**`ssl-mode-async`**

```haproxy
ssl-mode-async
```

Fügt dem SSL-Kontext den Modus SSL_MODE_ASYNC hinzu. Dies ermöglicht asynchrone TLS-I/O-Operationen, wenn SSL-Engines mit entsprechender Unterstützung verwendet werden. Die aktuelle Implementierung unterstützt maximal 32 Engines. Die Openssl-ASYNC-API unterstützt keine verschiebbaren Lese-/Schreibpuffer und ist nicht mit der Pufferverwaltung von HAProxy vereinbar. Daher ist der asynchrone Modus für Lese-/Schreiboperationen deaktiviert (er ist nur während des anfänglichen Handshakes und bei Handshakes zur Neuverhandlung aktiviert).

<a id="entry-3-2-tune-applet-zero-copy-forwarding"></a>

**`tune.applet.zero-copy-forwarding { on | off }`**

```haproxy
tune.applet.zero-copy-forwarding { on | off }
```

Aktiviert ('on') oder deaktiviert ('off') die kopierfreie Datenweiterleitung für Applets. Sie ist standardmäßig aktiviert.

Siehe auch: tune.disable-zero-copy-forwarding.

<a id="entry-3-2-tune-buffers-limit"></a>

**`tune.buffers.limit <number>`**

```haproxy
tune.buffers.limit <number>
```

Legt eine harte Obergrenze für die Anzahl der Puffer fest, die pro Prozess zugewiesen werden dürfen. Der Standardwert ist null und bedeutet unbegrenzt. Die Grenze wird automatisch so angepasst, dass die für Notfälle reservierten Puffer berücksichtigt werden; der Benutzer muss daher keine komplizierten Berechnungen durchführen. Das Erzwingen dieses Werts kann besonders nützlich sein, um den Speicherverbrauch eines Prozesses zu begrenzen und zugleich ein vernünftiges Verhalten beizubehalten. Wird diese Grenze erreicht, wartet ein Task, der einen Puffer anfordert, zunächst auf die Freigabe eines anderen Puffers. Solange die Grenzen sinnvoll gewählt sind, ist die Wartezeit meist sehr kurz und nicht wahrnehmbar. Einige historische Einschränkungen haben diesen Mechanismus jedoch über mehrere Versionen hinweg geschwächt. Es ist bekannt, dass manche Tasks bei anhaltendem Mangel in bestimmten Situationen bis zum Ablauf ihrer Zeitüberschreitung blockieren können. Daher ist es sicherer, diese Einstellung nur zu verwenden, wenn sie unbedingt erforderlich ist.

<a id="entry-3-2-tune-buffers-reserve"></a>

**`tune.buffers.reserve <number>`**

```haproxy
tune.buffers.reserve <number>
```

Legt die Anzahl der Puffer pro Thread fest, die vorab zugewiesen und ausschließlich für Situationen mit Speichermangel reserviert werden, in denen Speicherzuweisungen fehlschlagen. Der Mindestwert ist 0, der Standardwert 4. Es gibt keinen Grund für Benutzer, diesen Wert zu ändern, sofern nicht ein Entwickler des Kernteams dies aus einem sehr speziellen Grund empfiehlt.

<a id="entry-3-2-tune-bufsize"></a>

**`tune.bufsize <size>`**

```haproxy
tune.bufsize <size>
```

Setzt die Puffergröße auf diesen Wert (in Byte). Niedrigere Werte ermöglichen mehr gleichzeitige Streams bei derselben RAM-Menge, höhere Werte ermöglichen den Betrieb einiger Anwendungen mit sehr großen Cookies. Der Standardwert ist 16384 und kann beim Kompilieren geändert werden. Es wird dringend empfohlen, den Standardwert beizubehalten: Sehr niedrige Werte führen dazu, dass einige Dienste wie die Statistikfunktion nicht mehr funktionieren, während höhere Werte den Speicherverbrauch erhöhen und möglicherweise den gesamten verfügbaren Systemspeicher aufbrauchen. Zumindest der globale Parameter maxconn sollte um denselben Faktor verringert werden, um den dieser Wert erhöht wird. Außerdem erfordert HTTP/2 einen Wert von mindestens 16384. Der Wert muss außerdem unter 256 MB (268435456 Byte) liegen. Ist der Headerblock einer HTTP-Anfrage größer als (tune.bufsize - tune.maxrewrite), gibt HAProxy den Fehler HTTP 400 (Bad Request) zurück. Ist entsprechend der Headerblock einer HTTP-Antwort größer als dieser Wert, gibt HAProxy HTTP 502 (Bad Gateway) zurück. Beachten Sie, dass der mit diesem Parameter gesetzte Wert auf 32-Bit-Rechnern automatisch auf das nächste Vielfache von 8 und auf 64-Bit-Rechnern auf das nächste Vielfache von 16 aufgerundet wird. Siehe auch: tune.bufsize.large, tune.bufsize.small.

<a id="entry-3-2-tune-bufsize-large"></a>

**`tune.bufsize.large <size>`**

```haproxy
tune.bufsize.large <size>
```

Legt die Größe großer Puffer in Byte fest. Standardmäßig ist die Unterstützung großer Puffer nicht aktiviert; sie muss ausdrücklich durch Setzen dieses Werts aktiviert werden.

Diese Puffer sind für bestimmte Situationen vorgesehen, in denen mehr Daten gepuffert werden müssen, ohne die Größe regulärer Puffer zu ändern. Große Puffer werden nicht implizit verwendet. Siehe auch: tune.bufsize.

Beachten Sie, dass bei konfigurierten großen Puffern beim Start für jeden Thread drei spezielle große Puffer zur internen Verwendung zugewiesen werden.

<a id="entry-3-2-tune-bufsize-small"></a>

**`tune.bufsize.small <size>`**

```haproxy
tune.bufsize.small <size>
```

Legt die Größe kleiner Puffer in Byte fest. Der Standardwert ist 1024.

Diese Puffer sind für bestimmte Situationen vorgesehen, in denen der Speicherverbrauch begrenzt ist, die Zuweisung eines vollständigen Puffers jedoch unnötig erscheint. Falls ein kleiner Puffer nicht ausreicht, wird automatisch eine erneute Zuweisung durchgeführt, um auf einen Puffer der Standardgröße zu wechseln.

Derzeit verwendet nur das HTTP/3-Protokoll kleine Puffer automatisch, um die Antwort-Header zu senden. Ansonsten kann ihre Unterstützung für bestimmte Proxys über die Option "use-small-buffers" aktiviert werden. Siehe auch: tune.bufsize.

Siehe auch: option use-small-buffers

<a id="entry-3-2-tune-cli-max-payload-size"></a>

**`tune.cli.max-payload-size <size>`**

```haproxy
tune.cli.max-payload-size <size>
```

Legt die maximal zulässige Größe der Nutzdaten fest, die einem Befehl in der CLI übergeben werden.

In der CLI ist eine Befehlszeile durch die Puffergröße begrenzt. Alle Befehle und ihre Argumente müssen daher zur Verarbeitung in einen Puffer passen. Ausgenommen sind die Nutzdaten, die dem letzten Befehl der Befehlszeile übergeben werden können. Für diese Nutzdaten kann bei Bedarf ein eigener Speicherbereich zugewiesen werden. Ihre Größe wird durch diesen Parameter begrenzt. Der Standardwert ist 128KB.

Obwohl dieser Wert für die meisten Anwendungen ausreichen sollte, muss ein neuer Wert bei einer Änderung sorgfältig gewählt werden. Ein sehr hoher Wert kann die Leistung von HAProxy beeinträchtigen. Je nach Befehl kann die Verarbeitung sehr großer Nutzdaten lange dauern und möglicherweise den Watchdog auslösen.

Einzelheiten zur CLI finden Sie im Verwaltungshandbuch.

<a id="entry-3-2-tune-comp-maxlevel"></a>

**`tune.comp.maxlevel <number>`**

```haproxy
tune.comp.maxlevel <number>
```

Legt die maximale Komprimierungsstufe fest. Die Komprimierungsstufe beeinflusst die CPU-Auslastung während der Komprimierung. Dieser Wert beeinflusst die CPU-Auslastung während der Komprimierung. Jeder Stream mit Komprimierung initialisiert den Komprimierungsalgorithmus mit diesem Wert. Der Standardwert ist 1.

<a id="entry-3-2-tune-defaults-purge"></a>

**`tune.defaults.purge`**

```haproxy
tune.defaults.purge
```

Zur Unterstützung dynamischer Backends bleiben nun alle benannten defaults-Abschnitte nach dem Einlesen im Speicher. Dies ist erforderlich, da ein zur Laufzeit hinzugefügtes Backend seine Konfiguration auf einem benannten defaults-Abschnitt aufbauen muss.

Bei vielen defaults-Instanzen kann dies erheblichen Speicher beanspruchen. Wenn die Funktion für dynamische Backends nicht benötigt wird, kann in diesem Fall mit dieser Option das Löschen der defaults-Abschnitte nach dem Einlesen erzwungen werden. Referenzierte defaults-Abschnitte müssen jedoch weiterhin erhalten bleiben, wenn sie Einstellungen enthalten, die von den referenzierenden Proxys nicht kopiert werden können. Dies ist beispielsweise der Fall, wenn der defaults-Abschnitt TCP/HTTP-Regeln oder einen tcpcheck-Regelsatz definiert.

<a id="entry-3-2-tune-disable-fast-forward"></a>

**`tune.disable-fast-forward`**

```haproxy
tune.disable-fast-forward
```

Deaktiviert die schnelle Datenweiterleitung. Dieser Mechanismus optimiert die Weiterleitung, indem Daten direkt von einer Seite zur anderen übertragen werden, ohne den Stream aufzuwecken. Mit dieser Direktive kann die Optimierung deaktiviert werden. Beachten Sie, dass dadurch auch jegliches kernelbasierte TCP-Splicing sowie die kopierfreie Weiterleitung deaktiviert werden. Dieser Befehl ist nicht für den regulären Einsatz vorgesehen und wird im Allgemeinen nur von Entwicklern bei komplexen Fehlerdiagnosen empfohlen.

<a id="entry-3-2-tune-disable-zero-copy-forwarding"></a>

**`tune.disable-zero-copy-forwarding`**

```haproxy
tune.disable-zero-copy-forwarding
```

Deaktiviert die kopierfreie Datenweiterleitung global. Dieser Mechanismus optimiert die schnelle Datenweiterleitung, indem er die Verwendung des Kanalpuffers vermeidet. Mit dieser Direktive kann die Optimierung deaktiviert werden. Beachten Sie, dass dadurch auch jegliches kernelbasierte TCP-Splicing deaktiviert wird.

Siehe auch: tune.pt.zero-copy-forwarding, tune.applet.zero-copy-forwarding,
tune.h1.zero-copy-fwd-recv, tune.h1.zero-copy-fwd-send, tune.h2.zero-copy-fwd-send,
tune.quic.zero-copy-fwd-send

<a id="entry-3-2-tune-epoll-mask-events"></a>

**`tune.epoll.mask-events <event[,...]>`**

```haproxy
tune.epoll.mask-events <event[,...]>
```

Im Laufe der Entwicklung von HAProxy traten einige komplexe Probleme auf, die durch Fehler im epoll-Mechanismus des Linux-Kernels verursacht wurden. Diese Probleme sind üblicherweise sehr selten und außerhalb der Umgebung des Meldenden nicht reproduzierbar. Sie lassen sich mitunter nur umgehen, indem epoll deaktiviert und stattdessen poll verwendet wird, was für Hochleistungsumgebungen nicht zufriedenstellend ist. Die Probleme betreffen jeweils nur sehr spezielle und seltene Ereignistypen. Eine Möglichkeit, diese zu maskieren, kann daher eine akzeptablere Umgehungslösung bieten. Diese Option erlaubt es, einige ungewöhnliche Ereignisse ohne Meldung zu ignorieren und durch ein Eingabeereignis zu ersetzen, das ein nicht näher bestimmtes eingehendes Ereignis meldet. Dadurch werden an bestimmten Stellen die schnellen Fehlerverarbeitungspfade vermieden und nur die üblichen Verarbeitungspfade verwendet. Dies sollte niemals verwendet werden, sofern nicht ein Experte zur Diagnose oder Umgehung eines Kernel-Fehlers dazu auffordert.

Die Option erwartet ein einziges Argument: eine durch Kommas getrennte Liste von Wörtern, die jeweils ein zu maskierendes Ereignis bezeichnen. Derzeit werden folgende Ereignisse unterstützt: - "err": maskiert das Ereignis EPOLLERR - "hup": maskiert EPOLLHUP-Ereignisse - "rdhup": maskiert EPOLLRDHUP-Ereignisse

Beispiel:

```shell
# mask all non-traffic epoll events:
tune.epoll.mask-events err,hup,rdhup
```

<a id="entry-3-2-tune-events-max-events-at-once"></a>

**`tune.events.max-events-at-once <number>`**

```haproxy
tune.events.max-events-at-once <number>
```

Legt die Anzahl von Ereignissen fest, die ein asynchroner Task-Handler (aus der event_hdl-API) auf einmal verarbeiten darf. `<number>` sollte zwischen 1 und 10000 liegen. Ein hoher Wert kann durch die ununterbrochene, umfangreiche Arbeit des Tasks zu Konkurrenz zwischen Threads führen. Ein niedriger Wert kann dagegen dazu führen, dass der Task ständig neu eingeplant wird, weil er pro Durchlauf nicht genügend Ereignisse verarbeiten kann und mit dem Ereigniserzeuger nicht Schritt hält. Der Standardwert kann beim Kompilieren festgelegt werden; andernfalls beträgt er 100.

<a id="entry-3-2-tune-fail-alloc"></a>

**`tune.fail-alloc`**

```haproxy
tune.fail-alloc
```

Wenn mit DEBUG_FAIL_ALLOC kompiliert oder mit "-dMfail" gestartet wurde, gibt dies die prozentuale Wahrscheinlichkeit an, mit der ein Zuweisungsversuch fehlschlägt. Der Wert muss zwischen 0 (keine Fehlschläge) und 100 (keine Erfolge) liegen. Dies ist zur Fehlerdiagnose nützlich und stellt sicher, dass Fehler bei der Speicherzuweisung angemessen behandelt werden. Ohne Einstellung beträgt der Anteil 0. Die Befehlszeilenoption "-dMfail" setzt ihn jedoch automatisch auf eine Fehlerquote von 1%, sodass zum Testen keine Konfigurationsänderung erforderlich ist.

<a id="entry-3-2-tune-fd-edge-triggered"></a>

**`tune.fd.edge-triggered { on | off }  [ EXPERIMENTAL ]`**

```haproxy
tune.fd.edge-triggered { on | off }  [ EXPERIMENTAL ]
```

Aktiviert ('on') oder deaktiviert ('off') den flankengesteuerten Abfragemodus für FDs, die ihn unterstützen. Derzeit wird dies nur mit epoll unterstützt. Es kann die Anzahl der epoll_ctl()-Aufrufe deutlich verringern und in bestimmten Szenarien die Leistung leicht verbessern. Die Funktion ist noch experimentell, kann bei verbleibenden Fehlern zum Stillstand von Verbindungen führen und ist standardmäßig deaktiviert.

<a id="entry-3-2-tune-glitches-kill-cpu-usage"></a>

**`tune.glitches.kill.cpu-usage <number>`**

```haproxy
tune.glitches.kill.cpu-usage <number>
```

Legt die minimale CPU-Auslastung zwischen 0 und 100 fest, ab der Verbindungen mit zu vielen Unregelmäßigkeiten beendet werden. Dies gilt für Verbindungen, die ihre glitches-threshold-Grenze erreicht haben. In Umgebungen, in denen sehr lange bestehende Verbindungen häufig fehlerhaftes Verhalten zeigen, ohne die Leistung zu beeinträchtigen, kann es sinnvoll sein, sie trotz dieses Verhaltens beizubehalten, solange sie keinen Schaden verursachen, und sie erst bei zunehmender CPU-Auslastung zu beenden. Dieser Parameter legt fest, dass eine Verbindung, die ihre Unregelmäßigkeitsschwelle erreicht, aktiv beendet wird, wenn die CPU-Auslastung mindestens diesen Wert erreicht, niemals jedoch darunter. Beachten Sie, dass die CPU-Auslastung pro Thread gemessen wird, sodass auch eine einzelne fehlerhaft arbeitende Verbindung beendet werden kann. Der Standardwert ist null; eine Verbindung wird dann beim Erreichen ihrer glitches-threshold-Grenze automatisch beendet. Als Faustregel kann der Wert auf das Doppelte der üblichen CPU-Auslastung oder auf die übliche CPU-Auslastung zuzüglich der Hälfte des ungenutzten Anteils gesetzt werden (wenn die CPU üblicherweise 60% erreicht, kann hier beispielsweise 80 sinnvoll sein). Dieser Parameter hat ohne tune.h2.fe.glitches-threshold, tune.quic.fe.sec.glitches-threshold oder tune.h1.fe.glitches-threshold keine Wirkung. Siehe auch die globalen Parameter "tune.h2.fe.glitches-threshold", "tune.h1.fe.glitches-threshold" und "tune.quic.fe.sec.glitches-threshold".

<a id="entry-3-2-tune-h1-be-glitches-threshold"></a>

**`tune.h1.be.glitches-threshold <number>`**

```haproxy
tune.h1.be.glitches-threshold <number>
```

Legt die Schwelle für die Anzahl von Unregelmäßigkeiten auf einer HTTP/1-Backend-Verbindung fest, nach deren Überschreiten die Verbindung automatisch beendet wird. Dadurch lassen sich fehlerhaft arbeitende Verbindungen automatisch beenden, ohne dafür explizite Regeln schreiben zu müssen. Der Standardwert ist null: Es wird keine Schwelle gesetzt, sodass kein Ereignis zum Schließen einer Verbindung führt. Typische Ereignisse sind fehlerhaft formatierte Header, die dennoch durch "accept-unsafe-violations-in-http-response" akzeptiert wurden. Ein von null verschiedener Wert sollte vermutlich im Hunderter- oder Tausenderbereich liegen, um wirksam zu sein, ohne Server mit geringfügigen Fehlern zu beeinträchtigen. Mit "tune.glitches.kill.cpu-usage" können Verbindungen auch erst dann beendet werden, wenn die CPU-Auslastung einen bestimmten Wert überschreitet. Beachten Sie, dass bei 75% der konfigurierten Schwelle ein geordnetes Schließen versucht wird, indem auf den Verbindungsmodus zum Schließen umgeschaltet und gegebenenfalls "Connection: close" angekündigt wird. Dadurch wird eine leicht fehlerhafte Verbindung nach einiger Zeit nicht mehr verwendet, ohne laufende Übertragungen zu gefährden.

Siehe auch: tune.h1.fe.glitches-threshold, bc_glitches und tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h1-fe-glitches-threshold"></a>

**`tune.h1.fe.glitches-threshold <number>`**

```haproxy
tune.h1.fe.glitches-threshold <number>
```

Legt die Schwelle für die Anzahl von Unregelmäßigkeiten auf einer HTTP/1-Frontend-Verbindung fest, nach deren Überschreiten die Verbindung automatisch beendet wird. Dadurch lassen sich fehlerhaft arbeitende Verbindungen automatisch beenden, ohne dafür explizite Regeln schreiben zu müssen. Der Standardwert ist null: Es wird keine Schwelle gesetzt, sodass kein Ereignis zum Schließen einer Verbindung führt. Typische Ereignisse sind fehlerhaft formatierte Header, die dennoch durch "accept-unsafe-violations-in-http-request" akzeptiert wurden. Ein von null verschiedener Wert sollte vermutlich im Hunderter- oder Tausenderbereich liegen, um wirksam zu sein, ohne Clients mit geringfügigen Fehlern zu beeinträchtigen. Mit "tune.glitches.kill.cpu-usage" können Verbindungen auch erst dann beendet werden, wenn die CPU-Auslastung einen bestimmten Wert überschreitet. Beachten Sie, dass bei 75% der konfigurierten Schwelle ein geordnetes Schließen versucht wird, indem auf den Verbindungsmodus zum Schließen umgeschaltet und gegebenenfalls "Connection: close" angekündigt wird. Dadurch kann ein Client mit geringfügigen Protokollabweichungen eine neue Verbindung aufbauen und unbeeinträchtigt weiterarbeiten, ohne jemals ein hartes Schließen auszulösen und damit laufende Übertragungen zu gefährden.

Siehe auch: tune.h1.be.glitches-threshold, fc_glitches und tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h1-zero-copy-fwd-recv"></a>

**`tune.h1.zero-copy-fwd-recv { on | off }`**

```haproxy
tune.h1.zero-copy-fwd-recv { on | off }
```

Aktiviert ('on') oder deaktiviert ('off') den kopierfreien Datenempfang für den H1-Multiplexer. Er ist standardmäßig aktiviert.

Siehe auch: tune.disable-zero-copy-forwarding, tune.h1.zero-copy-fwd-send

<a id="entry-3-2-tune-h1-zero-copy-fwd-send"></a>

**`tune.h1.zero-copy-fwd-send { on | off }`**

```haproxy
tune.h1.zero-copy-fwd-send { on | off }
```

Aktiviert ('on') oder deaktiviert ('off') das kopierfreie Senden von Daten für den H1-Multiplexer. Es ist standardmäßig aktiviert.

Siehe auch: tune.disable-zero-copy-forwarding, tune.h1.zero-copy-fwd-recv

<a id="entry-3-2-tune-h2-be-glitches-threshold"></a>

**`tune.h2.be.glitches-threshold <number>`**

```haproxy
tune.h2.be.glitches-threshold <number>
```

Legt die Schwelle für die Anzahl von Unregelmäßigkeiten auf einer Backend-Verbindung fest, bei deren Erreichen die Verbindung automatisch beendet wird. Dadurch lassen sich fehlerhaft arbeitende Verbindungen automatisch beenden, ohne dafür explizite Regeln schreiben zu müssen. Der Standardwert ist null: Es wird keine Schwelle gesetzt, sodass kein Ereignis zum Schließen einer Verbindung führt. Beachten Sie, dass manche H2-Server auf lange bestehenden Verbindungen gelegentlich einige Unregelmäßigkeiten verursachen können. Ein von null verschiedener Wert sollte daher vermutlich im Hunderter- oder Tausenderbereich liegen, um wirksam zu sein, ohne Server mit geringfügigen Fehlern zu beeinträchtigen. Mit "tune.glitches.kill.cpu-usage" können Verbindungen auch erst dann beendet werden, wenn die CPU-Auslastung einen bestimmten Wert überschreitet. Beachten Sie, dass bei 75% der konfigurierten Schwelle ein geordnetes Schließen versucht wird, indem ein GOAWAY für einen zukünftigen Stream angekündigt wird. Dadurch wird eine leicht fehlerhafte Verbindung nach einiger Zeit nicht mehr verwendet, ohne laufende Übertragungen zu gefährden.

Siehe auch: tune.h2.fe.glitches-threshold, bc_glitches und tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h2-be-initial-window-size"></a>

**`tune.h2.be.initial-window-size <number>`**

```haproxy
tune.h2.be.initial-window-size <number>
```

Legt die anfängliche HTTP/2-Fenstergröße für ausgehende Verbindungen fest, also die Anzahl von Bytes, die der Server als Antwort senden kann, bevor er auf eine Bestätigung von HAProxy warten muss. Diese Einstellung betrifft nur Nutzdaten, keine Header. Ohne Einstellung gilt der gemeinsame Standardwert von tune.h2.initial-window-size. Eine leichte Erhöhung kann sinnvoll sein, um schnellere Downloads zu ermöglichen oder die CPU-Auslastung der Server zu verringern, geht jedoch zulasten einer fairen Verteilung zwischen den Clients. Besser ist die Verwendung von tune.h2.be.rxbuf, das keine solche Ungleichverteilung verursacht. Die Einstellung hat keinen Einfluss auf den Ressourcenverbrauch.

Siehe auch: tune.h2.initial-window-size.

<a id="entry-3-2-tune-h2-be-max-concurrent-streams"></a>

**`tune.h2.be.max-concurrent-streams <number>`**

```haproxy
tune.h2.be.max-concurrent-streams <number>
```

Legt die maximale Anzahl gleichzeitiger HTTP/2-Streams pro ausgehender Verbindung fest (also die Anzahl ausstehender Anfragen auf einer einzelnen Verbindung zu einem Server). Ohne Einstellung gilt der Standardwert von tune.h2.max-concurrent-streams. Ein kleinerer Wert als der Standardwert 100 kann die Reaktionsfähigkeit einer Website verbessern, erfordert jedoch mehr bestehende Verbindungen zu den Servern. Wenn "http-reuse" auf "always" gesetzt ist, wird empfohlen, diesen Wert zu verringern, damit nicht zu viele verschiedene Clients dieselbe Verbindung nutzen. Ist ein Client langsamer als andere, führt ein als "Head-of-Line-Blocking" bekannter Mechanismus häufig zu einem Kaskadeneffekt auf die Downloadgeschwindigkeit aller Clients, die sich die Verbindung teilen (halten Sie tune.h2.be.initial-window-size in diesem Fall niedrig). Es wird dringend empfohlen, diesen Wert nicht zu erhöhen; für manche Anwendungen können niedrige Werte optimal sein (typischerweise 1..5).

<a id="entry-3-2-tune-h2-be-max-frames-at-once"></a>

**`tune.h2.be.max-frames-at-once <number>`**

```haproxy
tune.h2.be.max-frames-at-once <number>
```

Legt die maximale Anzahl eingehender HTTP/2-Frames fest, die auf einer Backend-Verbindung auf einmal verarbeitet werden. Bei sehr großen Puffern kann ein niedriger Wert (einige zehn bis einige hundert) sinnvoll sein, um geringe Latenz und eine gerechtere Verteilung zwischen mehreren Verbindungen zu gewährleisten. Der Standardwert ist null, das heißt, es wird keine Begrenzung erzwungen.

<a id="entry-3-2-tune-h2-be-rxbuf"></a>

**`tune.h2.be.rxbuf <size>`**

```haproxy
tune.h2.be.rxbuf <size>
```

Legt die Größe des HTTP/2-Empfangspuffers für ausgehende Verbindungen in Byte fest. Die Größe wird auf das nächste Vielfache von tune.bufsize aufgerundet und von allen Streams gemeinsam genutzt, die Daten hochladen (sowohl HEADERS- als auch DATA-Frames). Jeder Stream erhält in jedem Fall einen Puffer. Außerdem werden 7/8 der ungenutzten Puffer unter den Streams aufgeteilt, die Nutzdaten herunterladen. Dadurch lässt sich die Upload-Leistung deutlich verbessern und Head-of-Line-Blocking (HoL) auf Backend-Verbindungen vermeiden, die bei "always" für http-reuse von mehreren Clients gemeinsam genutzt werden. Das pro Stream angekündigte Fenster wird automatisch an den verfügbaren Platz angepasst, sodass es in der Praxis nicht nötig sein sollte, tune.h2.be.initial-window-size zu ändern. Wird weniger als die für alle Streams erforderliche Größe gesetzt, wird dieses Minimum verwendet. Der Standardwert beträgt etwa 1600k (100 Streams mit jeweils 16kB großen Puffern).

Siehe auch: tune.h2.be.initial-window-size, tune.h2.fe.rxbuf, http-reuse.

<a id="entry-3-2-tune-h2-fe-glitches-threshold"></a>

**`tune.h2.fe.glitches-threshold <number>`**

```haproxy
tune.h2.fe.glitches-threshold <number>
```

Legt die Schwelle für die Anzahl von Unregelmäßigkeiten auf einer Frontend-Verbindung fest, bei deren Erreichen die Verbindung automatisch beendet wird. Dadurch lassen sich fehlerhaft arbeitende Verbindungen automatisch beenden, ohne dafür explizite Regeln schreiben zu müssen. Der Standardwert ist null: Es wird keine Schwelle gesetzt, sodass kein Ereignis zum Schließen einer Verbindung führt. Beachten Sie, dass manche H2-Clients auf lange bestehenden Verbindungen gelegentlich einige Unregelmäßigkeiten verursachen können. Ein von null verschiedener Wert sollte daher vermutlich im Hunderter- oder Tausenderbereich liegen, um wirksam zu sein, ohne Clients mit geringfügigen Fehlern zu beeinträchtigen. Mit "tune.glitches.kill.cpu-usage" können Verbindungen auch erst dann beendet werden, wenn die CPU-Auslastung einen bestimmten Wert überschreitet. Beachten Sie, dass bei 75% der konfigurierten Schwelle ein geordnetes Schließen versucht wird, indem ein GOAWAY für einen zukünftigen Stream angekündigt wird. Dadurch kann ein Client mit geringfügigen Protokollabweichungen eine neue Verbindung aufbauen und unbeeinträchtigt weiterarbeiten, ohne jemals ein hartes Schließen auszulösen und damit laufende Übertragungen zu gefährden.

Siehe auch: tune.h2.be.glitches-threshold, fc_glitches und tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h2-fe-initial-window-size"></a>

**`tune.h2.fe.initial-window-size <number>`**

```haproxy
tune.h2.fe.initial-window-size <number>
```

Legt die anfängliche HTTP/2-Fenstergröße für eingehende Verbindungen fest, also die Anzahl von Bytes, die der Client hochladen kann, bevor er auf eine Bestätigung von HAProxy warten muss. Diese Einstellung betrifft nur Nutzdaten (also den Body von POST-Anfragen), keine Header. Ohne Einstellung gilt der gemeinsame Standardwert von tune.h2.initial-window-size. Eine Erhöhung kann sinnvoll sein, um schnellere Uploads zu ermöglichen. Der Standardwert entspricht tune.bufsize (16384) und ermöglicht pro Stream eine Bandbreite von mindestens 1.25 Mbps bei 100 ms Ping-Zeit sowie 125 Mbps bei 1 ms Ping-Zeit. Die Einstellung hat keinen Einfluss auf den Ressourcenverbrauch. Zu hohe Werte können dazu führen, dass Clients eine schlechtere Reaktionsfähigkeit erleben, wenn Seiten parallel zu großen Uploads abgerufen werden. Besser ist die Verwendung von tune.h2.fe.rxbuf, das keine Ungleichverteilung verursacht.

Siehe auch: tune.h2.initial-window-size.

<a id="entry-3-2-tune-h2-fe-max-concurrent-streams"></a>

**`tune.h2.fe.max-concurrent-streams <number> [args...]`**

```haproxy
tune.h2.fe.max-concurrent-streams <number> [args...]
```

Legt die maximale Anzahl gleichzeitiger HTTP/2-Streams pro eingehender Verbindung fest (also die Anzahl ausstehender Anfragen auf einer einzelnen Verbindung von einem Client). Ohne Einstellung gilt der Standardwert von tune.h2.max-concurrent-streams. Ein höherer Wert als der Standardwert 100 kann die Ladezeit komplexer Websites mit vielen kleinen Objekten über Netzwerke mit hoher Latenz gelegentlich etwas verbessern. Er kann aber auch den Speicherverbrauch erhöhen, da ein Client mehr Ressourcen auf einmal zuweisen kann. Der Standardwert 100 ist im Allgemeinen gut geeignet; es wird empfohlen, ihn nicht zu ändern. Eine höhere Parallelität beeinflusst außerdem die Verarbeitungslast und Latenz bei einer großen Anzahl von Verbindungen, die jeweils viele Streams verwenden, und kann Denial-of-Service-Angriffe erleichtern. Der Befehl unterstützt nach der Zahl folgende optionale Argumente:

- rq-load { `<number>` \| auto \| ignore }:

```text
Mit dem optionalen Argument "rq-load" kann die angekündigte Anzahl
gleichzeitiger Streams dynamisch an die Auslastung der Ausführungswarteschlange
des ausführenden Threads angepasst werden: Solange die Auslastung des
Threads unter dem angegebenen Schwellenwert bleibt, wird das konfigurierte
Stream-Limit angekündigt. Steigt die Thread-Auslastung über das konfigurierte
Limit, wird das angekündigte Stream-Limit proportional zum Quadrat des
Überschreitungsverhältnisses verringert. Zielauslastungen zwischen 50 und
100 bewirken bei hoher Last in der Regel eine sehr gute Drosselung.
Alternativ zu einer expliziten Zahl akzeptiert das Schlüsselwort "ignore"
als Standardwert: Dabei wird die Auslastung der Ausführungswarteschlange
des Threads bei der Drosselung des angekündigten Stream-Limits nicht
berücksichtigt. Mit "auto" wird das Limit auf den Wert von
"tune.runqueue-depth" gesetzt, was in der Regel ohne weitere Anpassungen
der Konfiguration gute Ergebnisse liefert.
```

- min `<number>`:

```text
Dies legt bei Verwendung von rq-load die mindestens angekündigte Anzahl
gleichzeitiger Streams fest, selbst wenn dadurch die konfigurierte
Zielauslastung überschritten wird. So bleibt eine Website auch bei sehr
hoher Last gut reaktionsfähig. Mindest- und Standardwert ist 1; Werte zwischen
5 und 15 können jedoch die Benutzererfahrung verbessern.
```

Beispiel:

```text
tune.h2.fe.max-concurrent-streams 100 rq-load auto min 15
```

<a id="entry-3-2-tune-h2-fe-max-frames-at-once"></a>

**`tune.h2.fe.max-frames-at-once <number>`**

```haproxy
tune.h2.fe.max-frames-at-once <number>
```

Legt die maximale Anzahl eingehender HTTP/2-Frames fest, die auf einer Frontend-Verbindung auf einmal verarbeitet werden. Bei sehr großen Puffern kann ein niedriger Wert (einige zehn bis einige hundert) sinnvoll sein, um geringe Latenz und eine gerechtere Verteilung zwischen mehreren Verbindungen zu gewährleisten. Der Standardwert ist null, das heißt, es wird keine Begrenzung erzwungen.

<a id="entry-3-2-tune-h2-fe-max-rst-at-once"></a>

**`tune.h2.fe.max-rst-at-once <number>`**

```haproxy
tune.h2.fe.max-rst-at-once <number>
```

Legt die maximale Anzahl eingehender HTTP/2-RST_STREAM-Frames fest, die auf einer Frontend-Verbindung auf einmal verarbeitet werden. Sobald die angegebene Anzahl von RST_STREAM-Frames empfangen wurde, wird der Verbindungshandler in eine Warteschlange mit niedriger Priorität gestellt und nach allen anderen Tasks verarbeitet. Ein sehr niedriger Wert (1 oder einige wenige) kann sinnvoll sein, um die Auswirkungen von RST_STREAM-Fluten deutlich zu verringern. RST_STREAM tritt auch auf, wenn ein Benutzer auf die Stopp-Schaltfläche seines Browsers klickt. Die wenigen zusätzlichen Millisekunden durch das erneute Einreihen sind jedoch im Allgemeinen nicht wahrnehmbar, verringern aber gewöhnlich die durch solche Fluten verursachte Last erheblich. Der Standardwert ist null, das heißt, es wird keine Begrenzung erzwungen.

<a id="entry-3-2-tune-h2-fe-max-total-streams"></a>

**`tune.h2.fe.max-total-streams <number>`**

```haproxy
tune.h2.fe.max-total-streams <number>
```

Legt die maximale Gesamtanzahl von HTTP/2-Streams fest, die pro eingehender Verbindung verarbeitet werden. Sobald diese Grenze erreicht ist, sendet HAProxy einen GOAWAY-Frame zum geordneten Schließen. Dieser informiert den Client darüber, dass die Verbindung geschlossen wird, sobald alle ausstehenden Streams geschlossen wurden. In der Praxis schließen Clients die Verbindung nach Empfang dieser Meldung meist so schnell wie möglich und bauen für weitere Anfragen eine neue auf. Dies ist in Situationen nützlich und erwünscht, in denen Clients sehr lange verbunden bleiben und ein Ungleichgewicht innerhalb einer Serverfarm verursachen. In manchen hochdynamischen Umgebungen werden beispielsweise zusätzliche Load-Balancer während des Betriebs instanziiert, um auf zunehmende Last zu reagieren. Wenn die Last wieder abnimmt, sollen sie beendet werden, ohne bestehende Verbindungen abzubrechen. Eine hier gesetzte Grenze beschränkt die Lebensdauer der Verbindungen und sorgt für ihre häufige Erneuerung. Einige neue Verbindungen können dabei zu anderen Knoten aufgebaut werden, sodass bestehende Ressourcen schnell freigegeben werden.

Beachten Sie den impliziten Zusammenhang zwischen dieser Grenze und "tune.h2.fe.max-concurrent-streams" oben. HAProxy akzeptiert stets die Verarbeitung möglicherweise ausstehender Streams, die sich noch auf dem Weg zwischen Client und Frontend befinden. Daher wird die angekündigte Grenze automatisch um den für max-concurrent-streams konfigurierten Wert erhöht. Dieser erhöhte Wert dient als harte Grenze; überschreitet ein nicht protokollkonformer Client sie, wird die Verbindung geschlossen. Beim Zählen der Anfragen pro Verbindung anhand der Protokolle kann daher je nach Geschwindigkeit, mit der der Client Streams erzeugt, jeder Wert zwischen max-total-streams und (max-total-streams + max-concurrent-streams) auftreten.

Der Standardwert ist null und erzwingt keine zusätzliche Grenze über die vom Protokoll vorgegebene hinaus (2^30 ~= 1.07 Milliarden). Werte um 1000 können bereits eine häufige Erneuerung der Verbindungen bewirken, ohne bei den meisten Clients eine wahrnehmbare Latenz zu verursachen. Ein zu niedriger Wert kann durch häufige TLS-Neuverbindungen die CPU-Auslastung erhöhen und zusätzlich die Ladezeit von Seiten verlängern. Beachten Sie, dass einige Lasttestwerkzeuge keine Neuverbindungen unterstützen und mit dieser Einstellung Fehler melden können. Daher kann es erforderlich sein, sie bei Leistungsmessungen zu deaktivieren. Siehe auch "tune.h2.fe.max-concurrent-streams".

<a id="entry-3-2-tune-h2-fe-rxbuf"></a>

**`tune.h2.fe.rxbuf <size>`**

```haproxy
tune.h2.fe.rxbuf <size>
```

Legt die Größe des HTTP/2-Empfangspuffers für eingehende Verbindungen in Byte fest. Die Größe wird auf das nächste Vielfache von tune.bufsize aufgerundet und von allen Streams gemeinsam genutzt, die Daten hochladen (sowohl HEADERS- als auch DATA-Frames). Jeder Stream erhält in jedem Fall einen Puffer. Außerdem werden 7/8 der ungenutzten Puffer unter den Streams aufgeteilt, die Nutzdaten hochladen, wodurch sich die Upload-Leistung deutlich verbessern lässt. Das pro Stream angekündigte Fenster wird automatisch an den verfügbaren Platz angepasst, sodass es in der Praxis nicht nötig sein sollte, tune.h2.fe.initial-window-size zu ändern. Wird weniger als die für alle Streams erforderliche Größe gesetzt, wird dieses Minimum verwendet. Der Standardwert 1600k (100 Streams mit jeweils 16kB großen Puffern) ermöglicht einem Client mit einer RTT von 100ms ungefähr 130 Mbps Uploadgeschwindigkeit.

Siehe auch: tune.h2.fe.initial-window-size und tune.h2.be.rxbuf.

<a id="entry-3-2-tune-h2-header-table-size"></a>

**`tune.h2.header-table-size <number>`**

```haproxy
tune.h2.header-table-size <number>
```

Legt die Größe der dynamischen HTTP/2-Headertabelle fest. Der Standardwert beträgt 4096 Byte; der Wert darf nicht größer als 65536 Byte sein. Ein höherer Wert kann es bestimmten Clients je nach ihren Fähigkeiten ermöglichen, kompaktere Anfragen zu senden. Diese Speichermenge wird für jede HTTP/2-Verbindung benötigt. Es wird empfohlen, den Wert nicht zu ändern.

<a id="entry-3-2-tune-h2-initial-window-size"></a>

**`tune.h2.initial-window-size <number>`**

```haproxy
tune.h2.initial-window-size <number>
```

Legt den Standardwert für die anfängliche HTTP/2-Fenstergröße sowohl eingehender als auch ausgehender Verbindungen fest. Dieser Wert gilt für eingehende Verbindungen, wenn tune.h2.fe.initial-window-size nicht gesetzt ist, und für ausgehende Verbindungen, wenn tune.h2.be.initial-window-size nicht gesetzt ist. Er dient sowohl als Anfangswert als auch als Mindestwert pro Stream. Der Standardwert beträgt 16384 (tune.bufsize). Für Uploads ermöglicht dies pro Stream ungefähr mindestens 1.25 Mbps Bandbreite über ein Netzwerk mit 100 ms Ping-Zeit beziehungsweise 125 Mbps über ein lokales Netzwerk mit 1 ms. Wenn innerhalb der durch tune.h2.be.rxbuf und tune.h2.fe.rxbuf festgelegten Grenzen weniger als die maximale Anzahl von Empfangspuffern verwendet wird, werden ungenutzte Puffer unter den empfangenden Streams aufgeteilt. Daher gibt es normalerweise keinen Grund, diese Standardeinstellung zu ändern. Da eine Änderung des Standardwerts sowohl die Uploadgeschwindigkeit erhöht als auch die Downloadkapazität ungerechter zwischen den Clients verteilt, wird empfohlen, stattdessen die seitenspezifischen Einstellungen tune.h2.fe.initial-window-size und tune.h2.be.initial-window-size zu verwenden.

<a id="entry-3-2-tune-h2-log-errors"></a>

**`tune.h2.log-errors { none | connection | stream }`**

```haproxy
tune.h2.log-errors { none | connection | stream }
```

Legt fest, welche Fehler im H2-Demultiplexer einen Protokolleintrag erzeugen. Der Standardwert ist "stream": Jeder beim Dekodieren im Demultiplexer auftretende Fehler führt zu einem Protokolleintrag. Der Wert "connection" bedeutet, dass nur Fehler protokolliert werden, die die Verbindung ungültig machen. "none" bedeutet schließlich, dass kein Dekodierfehler protokolliert wird. Es wird empfohlen, mindestens "connection" einzustellen, um Protokollabweichungen zu erkennen, auch wenn in schwierigen Phasen vorübergehend auf "none" umgeschaltet werden muss.

<a id="entry-3-2-tune-h2-max-concurrent-streams"></a>

**`tune.h2.max-concurrent-streams <number>`**

```haproxy
tune.h2.max-concurrent-streams <number>
```

Legt den Standardwert für die maximale Anzahl gleichzeitiger HTTP/2-Streams pro Verbindung fest (also die Anzahl ausstehender Anfragen auf einer einzelnen Verbindung). Dieser Wert gilt für eingehende Verbindungen, wenn tune.h2.fe.max-concurrent-streams nicht gesetzt ist, und für ausgehende Verbindungen, wenn tune.h2.be.max-concurrent-streams nicht gesetzt ist. Der Standardwert ist 100. Die Auswirkungen unterscheiden sich je nach Seite; Einzelheiten finden Sie daher bei den beiden oben genannten Einstellungen. Es wird empfohlen, diese Einstellung nicht zu verwenden und stattdessen zu den seitenspezifischen Einstellungen zu wechseln. Der Wert null deaktiviert die Begrenzung, sodass ein einzelner Client so viele Streams erzeugen kann, wie HAProxy zuweisen kann. Es wird dringend empfohlen, diesen Wert nicht zu ändern.

<a id="entry-3-2-tune-h2-max-frame-size"></a>

**`tune.h2.max-frame-size <number>`**

```haproxy
tune.h2.max-frame-size <number>
```

Legt die maximale HTTP/2-Framegröße fest, die HAProxy seinen Peers als akzeptierte Empfangsgröße ankündigt. Der Standardwert ist der größere Wert aus 16384 und der Puffergröße (tune.bufsize). HAProxy kündigt in keinem Fall Unterstützung für Frames an, die größer als seine Puffer sind. Diese Einstellung dient hauptsächlich dazu, bei großen Puffern die maximale Framegröße begrenzen zu können. Zu große Frames können die Leistung beeinträchtigen oder bei einigen Peers fehlerhaftes Verhalten auslösen. Es wird dringend empfohlen, diesen Wert nicht zu ändern.

<a id="entry-3-2-tune-h2-zero-copy-fwd-send"></a>

**`tune.h2.zero-copy-fwd-send { on | off }`**

```haproxy
tune.h2.zero-copy-fwd-send { on | off }
```

Aktiviert ('on') oder deaktiviert ('off') das kopierfreie Senden von Daten für den H2-Multiplexer. Es ist standardmäßig aktiviert.

Siehe auch: tune.disable-zero-copy-forwarding

<a id="entry-3-2-tune-http-cookielen"></a>

**`tune.http.cookielen <number>`**

```haproxy
tune.http.cookielen <number>
```

Legt die maximale Länge erfasster Cookies fest. Dies ist der höchste Wert, den "capture cookie xxx len yyy" annehmen darf; jeder höhere Wert wird automatisch auf diesen gekürzt. Der Wert sollte keinesfalls zu hoch gesetzt werden, da bei jeder Cookie-Erfassung unabhängig vom konfigurierten Wert stets diese Größe zugewiesen wird (alle verwenden denselben Pool). Dieser Wert gilt jeweils für Anfrage und Antwort, sodass pro Verbindung das Doppelte dieses Werts an Speicher zugewiesen wird. Ohne Angabe ist die Grenze auf 63 Zeichen gesetzt. Es wird empfohlen, diesen Wert nicht zu ändern.

<a id="entry-3-2-tune-http-logurilen"></a>

**`tune.http.logurilen <number>`**

```haproxy
tune.http.logurilen <number>
```

Legt die maximale Länge der Anfrage-URI in Protokollen fest. Dadurch lässt sich verhindern, dass lange Anfrage-URIs mit wertvollen Abfragezeichenfolgen in Protokollzeilen abgeschnitten werden. Dies hängt nicht mit Syslog-Grenzen zusammen. Wenn Sie diese Grenze erhöhen, können Sie auch den Parameter 'log ... len yyy' erhöhen. Ihr Syslog-Daemon benötigt möglicherweise ebenfalls spezielle Konfigurationsdirektiven. Der Standardwert ist 1024.

<a id="entry-3-2-tune-http-maxhdr"></a>

**`tune.http.maxhdr <number>`**

```haproxy
tune.http.maxhdr <number>
```

Legt die maximale Anzahl von Headern fest, die in empfangenen HTTP-Nachrichten erlaubt ist. Enthält eine Nachricht mehr Header als dieser Wert (einschließlich der ersten Zeile), wird sie bei einer Anfrage mit dem Statuscode "400 Bad Request" beziehungsweise bei einer Antwort mit "502 Bad Gateway" abgelehnt. Der Standardwert ist 101 und reicht für alle Anwendungsfälle aus, da der weit verbreitete Apache-Server dieselbe Grenze verwendet. Es kann sinnvoll sein, die Grenze vorübergehend zu erhöhen, damit eine fehlerhafte Anwendung bis zu ihrer Korrektur funktioniert. Der zulässige Bereich ist 1..32767. Beachten Sie, dass jeder zusätzliche Header pro Stream 32 Bit Speicher benötigt; setzen Sie die Grenze daher nicht zu hoch.

HTTP/1.1 ist ein Textprotokoll, weshalb beim Senden einer Nachricht keine besondere Begrenzung gilt. Die Begrenzung beim Einlesen der Nachricht genügt. HTTP/2 und HTTP/3 sind Binärprotokolle und erfordern einen Kodierungsschritt. Auch beim Kodieren der Header wird eine Grenze gesetzt, um die Beschränkungen dieser Protokolle einzuhalten. Diese Grenze ist ausreichend hoch, wird aber absichtlich nicht dokumentiert. Aus demselben Grund gilt dieselbe Grenze auch bei den ersten Schritten der Dekodierung.

<a id="entry-3-2-tune-idle-pool-shared"></a>

**`tune.idle-pool.shared { full | on | off }`**

```haproxy
tune.idle-pool.shared { full | on | off }
```

Steuert die gemeinsame Nutzung von Pools ungenutzter Verbindungen zu demselben Server durch mehrere Threads. Sie kann für alle Threads derselben Thread-Gruppe aktiviert werden ('on'), für alle Threads aktiviert werden ('full') oder deaktiviert werden ('off'). Standardmäßig werden die Pools innerhalb derselben Thread-Gruppe gemeinsam genutzt ('on'), um die Anzahl dauerhafter Verbindungen zu einem Server zu minimieren und die Wiederverwendungsrate zu optimieren. Die gemeinsame Nutzung mit Threads anderer Thread-Gruppen kann die Leistung beeinträchtigen und ist standardmäßig nicht aktiviert. Sie kann aber sinnvoll sein, wenn eine möglichst hohe Verbindungswiederverwendung Priorität hat. Zur Fehlerdiagnose oder bei Verdacht auf einen Fehler in HAProxy bei der Wiederverwendung von Verbindungen kann es hilfreich sein, die gemeinsame Nutzung dieser Pools durch mehrere Threads ausdrücklich zu deaktivieren und die Option auf "off" zu setzen. Es wird dringend davon abgeraten, diese Option zu deaktivieren, ohne für alle Server, die zur Erzielung hoher Leistung auf Verbindungswiederverwendung angewiesen sind, einen konservativen Wert für "pool-low-conn" zu setzen. Andernfalls können Verbindungen mit zunehmender Thread-Anzahl sehr häufig geschlossen werden.

<a id="entry-3-2-tune-idletimer"></a>

**`tune.idletimer <timeout>`**

```haproxy
tune.idletimer <timeout>
```

Legt die Zeitspanne fest, nach der HAProxy davon ausgeht, dass ein leerer Puffer wahrscheinlich zu einem inaktiven Stream gehört. Dies dient dazu, einige Paketgrößen optimal anzupassen, wenn abwechselnd große und kleine Datenmengen weitergeleitet werden. Der Parameter beeinflusst die Entscheidung, splice() zu verwenden oder große Puffer über SSL zu senden. Der Wert wird in Millisekunden zwischen 0 und 65535 angegeben. Der Wert null bedeutet, dass HAProxy nicht versucht, inaktive Streams zu erkennen. Der Standardwert ist 1000 und scheint Pausen von Endbenutzern korrekt zu erkennen (beispielsweise das Lesen einer Seite vor einem Klick). Es sollte keinen Grund geben, diesen Wert zu ändern. Siehe tune.ssl.maxrecord weiter unten.

<a id="entry-3-2-tune-listener-default-shards"></a>

**`tune.listener.default-shards { by-process | by-thread | by-group }`**

```haproxy
tune.listener.default-shards { by-process | by-thread | by-group }
```

Normalerweise erzeugt jede "bind"-Zeile einen einzigen Shard, also einen Socket, an dem alle Threads des Prozesses lauschen. Bei vielen Threads ist dies nicht sehr effizient und kann im Kernel erheblichen Aufwand beim Aktualisieren des Abfragestatus oder beim Verteilen von Ereignissen auf die verschiedenen Threads verursachen. Moderne Betriebssysteme unterstützen die Verteilung eingehender Verbindungen: Mehrere Sockets dürfen an dieselbe Adresse und denselben Port gebunden werden, und alle eingehenden Verbindungen werden gleichmäßig auf diese Sockets verteilt. Jeder Thread sieht dadurch nur die Verbindungen, die in dem Socket warten, an den er gebunden ist. Dies verringert den Aufwand im Kernel erheblich und verbessert die Leistung bei der Verarbeitung eingehender Verbindungen. In HAProxy wird dies üblicherweise über "shards" in "bind"-Zeilen aktiviert. Der Standardwert ist 1, sodass jeder Listener im Prozess nur einmal vorhanden ist. Auf Systemen mit vielen Prozessoren kann es bequemer sein, den Standardwert auf "by-thread" zu setzen, um stets einen Listener-Socket pro Thread zu erzeugen, oder auf "by-group", um stets einen Listener-Socket pro Thread-Gruppe zu erzeugen. Achten Sie bei "by-thread" auf den Dateideskriptorverbrauch, da jeder Listener so viele Sockets benötigt, wie Threads vorhanden sind. Einige Betriebssysteme (z. B. FreeBSD) erlauben außerdem höchstens 256 Sockets an derselben Adresse. "by-group" entspricht bei Standardkonfigurationen mit einer einzigen Thread-Gruppe weiterhin "by-process". Auf Systemen ohne Unterstützung dieses Mechanismus wird auf die gemeinsame Nutzung desselben Sockets zurückgefallen. Der Standardwert ist "by-group", mit Rückfall auf "by-process" für Systeme oder Socket-Familien, die keine Mehrfachbindungen unterstützen.

<a id="entry-3-2-tune-listener-multi-queue"></a>

**`tune.listener.multi-queue { on | fair | off }`**

```haproxy
tune.listener.multi-queue { on | fair | off }
```

Aktiviert ('on' / 'fair') oder deaktiviert ('off') die Annahme von Verbindungen über mehrere Warteschlangen am Listener. Dabei wird eingehender Datenverkehr auf alle Threads verteilt, auf denen eine "bind"-Zeile laufen darf, anstatt ihn vollständig selbst zu übernehmen. Dies sorgt für eine gleichmäßigere Verteilung des Datenverkehrs und skaliert deutlich besser, insbesondere wenn Threads aufgrund externer Aktivitäten ungleich ausgelastet sein können (beispielsweise wenn Netzwerk-Interrupts mit einem Thread konkurrieren). Der Standardmodus "on" optimiert die Thread-Auswahl, indem innerhalb einer Stichprobe der Thread mit den wenigsten Verbindungen gewählt wird. Dies ist bei langlebigen Verbindungen häufig die beste Wahl, da so alle Threads beschäftigt bleiben. Der zweite Modus "fair" durchläuft dagegen alle Threads unabhängig von ihrer momentanen Auslastung. Er kann für kurzlebige Verbindungen besser geeignet sein oder auf Rechnern mit sehr vielen Threads, auf denen die Wahrscheinlichkeit gering ist, im ersten Modus den am wenigsten ausgelasteten Thread zu finden. Schließlich lässt sich der Umverteilungsmechanismus mit "off" ausdrücklich deaktivieren, etwa zur Fehlerdiagnose oder bei kurzlebigen Verbindungen, wenn das Betriebssystem bereits eine ausreichend gute Verteilung bereitstellt. Der Standardwert ist "on".

<a id="entry-3-2-tune-lua-bool-sample-conversion"></a>

**`tune.lua.bool-sample-conversion { normal | pre-3.1-bug }`**

```haproxy
tune.lua.bool-sample-conversion { normal | pre-3.1-bug }
```

Gibt haproxy ausdrücklich vor, wie seine Sample-Objekte bei der Übergabe an Lua behandelt werden sollen. Wenn beispielsweise native Konverter, Sample-Fetches oder Variablen aus einem Lua-Skript verwendet werden, konvertiert haproxy den internen smp-Typ in den entsprechenden Lua-Typ. Aufgrund der historischen Implementierung gibt es Unklarheiten beim Umgang mit booleschen Werten: Bei der Konvertierung Lua -\> haproxy smp bleiben boolesche Werte korrekt erhalten, bei haproxy smp -\> Lua wurden sie dagegen irrtümlich in Ganzzahlen umgewandelt. Ein Sample-Fetch oder Konverter mit booleschem Rückgabewert gab bei Verwendung aus Lua daher die Ganzzahl 0 oder 1 zurück. In Lua sind boolesche Werte und Ganzzahlen jedoch nicht austauschbar. Um Mehrdeutigkeiten zu vermeiden, muss "tune.lua.bool-sample-conversion" deshalb ausdrücklich auf "normal" (Aufgabe des historischen Verhaltens zugunsten besserer Konsistenz) oder "pre-3.1-bug" (Erzwingen des historischen Verhaltens, damit die Logik bestehender Skripte nicht fehlerhaft arbeitet) gesetzt werden. Wenn die Option nicht ausdrücklich gesetzt ist und ein Lua-Skript aus der Konfiguration geladen wird, gibt haproxy eine Warnung aus und verwendet implizit "pre-3.1-bug", um das historische Verhalten beizubehalten. Es wird empfohlen, diese Option auf "normal" zu setzen, nachdem sichergestellt wurde, dass die verwendeten Lua-Skripte boolesche haproxy-Samples korrekt als boolesche Werte behandeln.

Diese Einstellung muss vor jeder "lua-load"- oder "lua-load-per-thread"-Direktive gesetzt werden, damit sie berücksichtigt wird; andernfalls wird sie ignoriert.

<a id="entry-3-2-tune-lua-burst-timeout"></a>

**`tune.lua.burst-timeout <timeout>`**

```haproxy
tune.lua.burst-timeout <timeout>
```

Das Ausführungszeitlimit "burst" gilt für jeden Lua-Handler. Wenn der Handler vor Erreichen des Limits weder fertig wird noch die Ausführung abgibt, wird er abgebrochen. Dies verhindert Thread-Konkurrenz, eine zu lange Unterbrechung der Datenverkehrsverarbeitung und letztlich einen Prozessabsturz durch den Watchdog. Anders als andere Lua-Zeitlimits, die die Laufzeit über mehrere durch Yield unterbrochene Ausführungsphasen aufsummieren, stellt burst-timeout sicher, dass die Zeit in einem einzelnen Lua-Ausführungsfenster das konfigurierte Limit nicht überschreitet.

Yield bedeutet hier, dass die Lua-Ausführung tatsächlich unterbrochen wird, entweder durch einen expliziten Aufruf einer entsprechenden Funktion wie core.(m)sleep() oder core.yield() oder durch eine automatische erzwungene Unterbrechung (siehe tune.lua.forced-yield). Sie wird später fortgesetzt, wenn der zugehörige Task erneut zur Ausführung eingeplant wird. Nicht alle Lua-Handler können ihre Ausführung abgeben: Es muss zwischen unterbrechbaren und nicht unterbrechbaren Handlern unterschieden werden.

Bei unterbrechbaren Handlern (Tasks, Aktionen usw.) kann das Erreichen des Zeitlimits bedeuten, dass "tune.lua.forced-yield" für das System zu hoch ist. Ein niedrigerer Wert könnte die Situation verbessern. Es kann aber auch sinnvoll sein zu prüfen, ob manuelle Yield-Aufrufe an wichtigen Stellen der Lua-Funktion helfen. Ebenso kann es darauf hinweisen, dass der Handler zu viel Zeit in einer bestimmten, nicht unterbrechbaren Lua-Bibliotheksfunktion verbringt.

Bei nicht unterbrechbaren Handlern (Lua-Konvertern, Sample-Fetches) kann es schlicht bedeuten, dass der Handler zu viele Berechnungen durchführt. Dies könnte auf einen ungeeigneten Entwurf zurückgehen, denn solche Handler blockieren häufig den Ablauf der Anfrageausführung und sollen schnell beendet werden, damit die Anfrageverarbeitung fortfahren kann. Ein üblicher Lösungsansatz ist, die Lua-Funktion stärker auf Geschwindigkeit zu optimieren, da eine Verringerung von "tune.lua.forced-yield" hier nicht hilft.

Dieses Zeitlimit zählt nur die reine Lua-Laufzeit. Führt Lua ein core.sleep aus, wird die Schlafzeit nicht berücksichtigt. Das Standardzeitlimit beträgt 1000ms.

Hinweis: Wenn der Handler einen Lua-GC-Zyklus auslöst (entweder explizit oder nach einiger Zeit automatisch durch Lua), wird dessen Dauer ebenfalls angerechnet.

Die Dauer des GC-Zyklus lässt sich nicht gesondert bestimmen. Daher kann dies auf ausgelasteten Systemen zu Fehlalarmen führen, wenn der GC kaum mit der Arbeit nachkommt und den größten Teil der verfügbaren Ausführungszeit verbraucht. In diesem Fall kommen folgende Lösungsansätze infrage:

    - prüfen, ob sich das Skript zur Verringerung des Lua-Speicherverbrauchs optimieren lässt
    - Lua-GC-Parameter feinabstimmen und/oder manuelle GC-Zyklen anfordern
      (siehe: https://www.lua.org/manual/5.4/manual.html#pdf-collectgarbage)
    - tune.lua.burst-timeout erhöhen

Der Wert 0 deaktiviert diesen Schutz vollständig.

<a id="entry-3-2-tune-lua-forced-yield"></a>

**`tune.lua.forced-yield <number>`**

```haproxy
tune.lua.forced-yield <number>
```

Diese Direktive zwingt die Lua-Engine, nach jeweils `<number>` ausgeführten Anweisungen die Ausführung abzugeben. Dadurch lässt sich ein langes Skript unterbrechen, sodass der HAProxy-Scheduler andere Tasks verarbeiten kann, etwa Verbindungen annehmen oder Datenverkehr weiterleiten. Der Standardwert beträgt 10000 Anweisungen für mit "lua-load-per-thread" geladene Skripte und MAX(500, 10000 / nbthread) Anweisungen für mit "lua-load" geladene Skripte. Dieser Wert erwies sich als optimal für die Leistung und vermeidet zugleich Konkurrenz zwischen mehreren Threads um die globale Lua-Sperre.

Wenn HAProxy häufig Lua-Code ausführt, aber eine höhere Reaktionsfähigkeit benötigt wird, kann dieser Wert verringert werden. Ist der Lua-Code recht lang und sein Ergebnis für die Datenverarbeitung unbedingt erforderlich, kann `<number>` erhöht werden. Der Wert sollte jedoch sorgfältig gewählt werden, da er bei mehreren Threads die Konkurrenz erhöhen kann.

<a id="entry-3-2-tune-lua-log-loggers"></a>

**`tune.lua.log.loggers { on | off }`**

```haproxy
tune.lua.log.loggers { on | off }
```

Aktiviert ('on') oder deaktiviert ('off') die Protokollierung der Ausgabe von LUA-Skripten über die für den aktuellen Proxy geltenden Logger, sofern vorhanden.

Der Standardwert ist 'on'.

<a id="entry-3-2-tune-lua-log-stderr"></a>

**`tune.lua.log.stderr { on | auto | off }`**

```haproxy
tune.lua.log.stderr { on | auto | off }
```

Aktiviert ('on') oder deaktiviert ('off') die Protokollierung der Ausgabe von LUA-Skripten über stderr. Bei 'auto' ist die Protokollierung über stderr unter folgenden Bedingungen aktiviert, wenn mindestens eine davon zutrifft:

    - tune.lua.log.loggers ist auf 'off' gesetzt
    - das Skript läuft außerhalb eines Proxy-Kontexts, und es gibt keinen globalen Logger
    - das Skript läuft in einem Proxy-Kontext ohne zugeordneten Logger

Beachten Sie, dass diese Protokollierung, sofern aktiviert, zusätzlich zur über tune.lua.log.loggers konfigurierten Protokollierung erfolgt.

Der Standardwert ist 'auto'.

<a id="entry-3-2-tune-lua-maxmem"></a>

**`tune.lua.maxmem <number>`**

```haproxy
tune.lua.maxmem <number>
```

Legt die maximale Menge an RAM in Megabyte fest, die Lua pro Prozess verwenden darf. Der Standardwert ist null und bedeutet unbegrenzt. Es ist wichtig, eine Grenze zu setzen, damit ein Skriptfehler nicht den gesamten verfügbaren Systemspeicher aufbraucht.

<a id="entry-3-2-tune-lua-openlibs"></a>

**`tune.lua.openlibs [all | none | <lib>[,<lib>...]]`**

```haproxy
tune.lua.openlibs [all | none | <lib>[,<lib>...]]
```

Wählt aus, welche Lua-Standardbibliotheken beim Initialisieren des Lua-Zustands geladen werden. Das Argument ist eine durch Kommas getrennte Liste von Bibliotheksnamen aus folgender Menge: table, io, os, string, math, utf8, package, debug. Anstelle einer Liste können die besonderen Werte "all" und "none" verwendet werden. "none" lässt sich nicht mit Bibliotheksnamen kombinieren. Der Standardwert ist "all".

Die Bibliotheken base und coroutine werden unabhängig von dieser Einstellung immer geladen: base stellt grundlegende Lua-Funktionen bereit, auf die HAProxy angewiesen ist, und coroutine ist erforderlich, weil HAProxy coroutine.create() durch eine eigene sichere Implementierung ersetzt.

Beachten Sie, dass fork() und die Erzeugung neuer Threads in HAProxy unabhängig von dieser Einstellung bereits standardmäßig blockiert sind. Sie können nur über die globale Direktive "insecure-fork-wanted" wieder aktiviert werden. Die Beschränkung der geladenen Bibliotheken verringert die für Lua-Skripte zugängliche Angriffsfläche weiter. Insbesondere gilt: - Das Weglassen von "os" verhindert os.execute() und os.exit() - Das Weglassen von "io" verhindert io.open() und io.popen() - Das Weglassen von "package" verhindert das Laden nativer C-Module über require() - Das Weglassen von "debug" verhindert die Untersuchung interner HAProxy-Strukturen über debug.getupvalue(), debug.getmetatable() oder debug.sethook()

Beispiele:

```text
tune.lua.openlibs none                    # only base + coroutine
tune.lua.openlibs string,math,table,utf8  # safe subset, no I/O or OS
tune.lua.openlibs all                     # default, load everything
```

Diese Einstellung muss vor jeder "lua-load"-, "lua-load-per-thread"- oder "lua-prepend-path"-Direktive gesetzt werden; andernfalls wird ein Fehler beim Einlesen der Konfiguration ausgegeben.

<a id="entry-3-2-tune-lua-service-timeout"></a>

**`tune.lua.service-timeout <timeout>`**

```haproxy
tune.lua.service-timeout <timeout>
```

Dies ist das Ausführungszeitlimit für Lua-Dienste. Es hilft, Endlosschleifen oder übermäßig lange Lua-Ausführungen zu verhindern. Dieses Zeitlimit zählt nur die reine Lua-Laufzeit. Führt Lua einen Schlafvorgang aus, wird dessen Dauer nicht berücksichtigt. Das Standardzeitlimit beträgt 4s.

<a id="entry-3-2-tune-lua-session-timeout"></a>

**`tune.lua.session-timeout <timeout>`**

```haproxy
tune.lua.session-timeout <timeout>
```

Dies ist das Ausführungszeitlimit für Lua-Sitzungen. Es hilft, Endlosschleifen oder übermäßig lange Lua-Ausführungen zu verhindern. Dieses Zeitlimit zählt nur die reine Lua-Laufzeit. Führt Lua einen Schlafvorgang aus, wird dessen Dauer nicht berücksichtigt. Das Standardzeitlimit beträgt 4s.

<a id="entry-3-2-tune-lua-task-timeout"></a>

**`tune.lua.task-timeout <timeout>`**

```haproxy
tune.lua.task-timeout <timeout>
```

Dient demselben Zweck wie "tune.lua.session-timeout", gilt jedoch speziell für Tasks. Standardmäßig ist dieses Zeitlimit nicht gesetzt, da ein Task während der gesamten Lebensdauer von HAProxy aktiv bleiben kann, beispielsweise ein Task zur Prüfung von Servern.

<a id="entry-3-2-tune-max-checks-per-thread"></a>

**`tune.max-checks-per-thread <number>`**

```haproxy
tune.max-checks-per-thread <number>
```

Legt die Anzahl aktiver Prüfungen pro Thread fest, ab deren Überschreiten ein Thread aktiv nach einem weniger ausgelasteten Thread für die Zustandsprüfung sucht oder sie in eine Warteschlange stellt, bis die Anzahl der auf ihm laufenden aktiven Prüfungen sinkt. Der Standardwert ist null, das heißt, es wird keine solche Grenze gesetzt. Dies kann in Umgebungen mit sehr vielen aufwendigen Prüfungen und vielen Threads erforderlich sein, wenn die Last ungleich verteilt erscheint und Zustandsprüfungen beim Start zufällig ihr Zeitlimit überschreiten. Dies tritt typischerweise mit OpenSSL 3.0 auf, das bei Zustandsprüfungen etwa 20-mal mehr CPU beansprucht als ältere Versionen. Die Einstellung versucht, die Arbeit für Zustandsprüfungen gleichmäßiger auf alle Threads zu verteilen. Die weitaus meisten Konfigurationen benötigen keine Änderung dieses Parameters. Beachten Sie, dass zu niedrige Werte die Zustandsprüfung erheblich verlangsamen können, wenn die Prüfungen lange dauern.

<a id="entry-3-2-tune-maxaccept"></a>

**`tune.maxaccept <number>`**

```haproxy
tune.maxaccept <number>
```

Legt fest, wie viele Verbindungen ein Prozess maximal unmittelbar nacheinander annehmen darf, bevor er sich anderer Arbeit zuwendet. Im Einzelprozessmodus lieferten höhere Werte bei hohen Verbindungsraten früher bessere Leistung; mit mehreren Warteschlangen gilt dies jedoch nicht mehr. Der Wert gilt für jeden Listener einzeln, wobei die Anzahl der Prozesse berücksichtigt wird, an die der Listener gebunden ist. Der Standardwert ist 4, womit die besten Ergebnisse erzielt wurden. Wurde ein deutlich höherer Wert aus einer sehr alten Konfiguration übernommen, kann es sich lohnen, ihn zu entfernen, da dies sowohl die Leistung verbessert als auch die Antwortzeit verringert. Im Mehrprozessmodus wird der Wert durch das Doppelte der Anzahl von Prozessen geteilt, an die der Listener gebunden ist. Der Wert -1 deaktiviert die Begrenzung vollständig. Normalerweise sollte es nicht nötig sein, diesen Wert anzupassen.

<a id="entry-3-2-tune-maxpollevents"></a>

**`tune.maxpollevents <number>`**

```haproxy
tune.maxpollevents <number>
```

Legt die maximale Anzahl von Ereignissen fest, die bei einem Aufruf des Abfragesystems auf einmal verarbeitet werden können. Der Standardwert wird an das Betriebssystem angepasst. Es wurde beobachtet, dass Werte unter 200 die Latenz tendenziell leicht verringern, jedoch zulasten der Netzwerkbandbreite. Werte über 200 erhöhen dagegen tendenziell die Latenz zugunsten etwas höherer Bandbreite. Der konfigurierte Wert muss kleiner oder gleich 1000000 sein.

<a id="entry-3-2-tune-maxrewrite"></a>

**`tune.maxrewrite <number>`**

```haproxy
tune.maxrewrite <number>
```

Setzt den reservierten Pufferbereich auf diese Größe in Byte. Der reservierte Bereich wird zum Umschreiben oder Hinzufügen von Headern verwendet. Die ersten Lesevorgänge auf Sockets füllen niemals mehr als bufsize-maxrewrite. Historisch war der Standardwert die Hälfte von bufsize, was jedoch wenig sinnvoll ist, da selten sehr viele Header hinzugefügt werden müssen. Ein zu hoher Wert verhindert die Verarbeitung großer Anfragen oder Antworten. Ein zu niedriger Wert verhindert das Hinzufügen neuer Header zu bereits großen Anfragen oder zu POST-Anfragen. Im Allgemeinen ist ein Wert von etwa 1024 sinnvoll. Ist er größer als die Hälfte von bufsize, wird er automatisch auf diese Hälfte angepasst. Daher müssen Sie sich bei einer Änderung von bufsize nicht darum kümmern.

<a id="entry-3-2-tune-max-rules-at-once"></a>

**`tune.max-rules-at-once <number>`**

```haproxy
tune.max-rules-at-once <number>
```

Legt die maximale Anzahl von Regeln fest, die Funktionen zur Regelsatzauswertung auf einmal auswerten dürfen, sofern diese Funktionen ihre Ausführung abgeben können. Konfigurationen mit vielen "tcp-request content"- oder "http-request"-Regeln sind beispielsweise nicht ungewöhnlich. Viele Regeln zusammen mit CPU-intensiven Aktionen (etwa Aktionen auf Inhalten) können Konkurrenz zwischen Threads verursachen, da ohne Unterbrechung alle Regeln eines Regelsatzes innerhalb desselben Abfrageschleifendurchlaufs ausgewertet werden. Diese Option stellt sicher, dass bei inhaltsbezogenen Regelsätzen (die wegen der Inhaltsprüfung bereits Yield unterstützen) höchstens `<number>` Regeln innerhalb desselben Abfrageschleifendurchlaufs ausgeführt werden. Dazu zwingt sie die auswertende Funktion, die Ausführung abzugeben und die Auswertung erst im nächsten Abfrageschleifendurchlauf fortzusetzen.

Betroffen sind folgende Regelsätze:

- "tcp-request content"
- "tcp-response content"
- "http-request"
- "http-response"

Der Standardwert ist 50.

<a id="entry-3-2-tune-memory-hot-size"></a>

**`tune.memory.hot-size <number>`**

```haproxy
tune.memory.hot-size <number>
```

Legt die Speichermenge pro Thread fest, die im lokalen Cache sofort verfügbar gehalten wird und niemals von anderen Threads zurückgewonnen werden kann. Der Zugriff auf diesen Speicher ist sehr schnell und benötigt keine Sperren. Eine ausreichende Menge ist entscheidend für gute Leistung bei extremer Konkurrenz zwischen Threads. Der Wert wird in Byte angegeben. Der Standardwert wird beim Kompilieren über CONFIG_HAP_POOL_CACHE_SIZE festgelegt und beträgt standardmäßig 524288 (512 kB). Ein höherer Wert kann die Leistung in bestimmten Szenarien verbessern, insbesondere wenn Leistungsprofile eine starke Belastung der Speicherzuweisung zeigen. Erfahrungsgemäß liegt ein guter Wert zwischen der einfachen und der doppelten Größe des L2-Caches pro CPU-Kern. Zu hohe Werte beeinträchtigen die Leistung durch ineffiziente Nutzung der L3-Caches der CPUs und verbrauchen mehr Speicher. Es wird empfohlen, den Wert nicht zu ändern oder nur in kleinen Schritten vorzugehen. Um die CPU-Caches pro Thread vollständig zu deaktivieren, könnte ein sehr kleiner Wert funktionieren; besser ist jedoch "-dMno-cache" in der Befehlszeile.

<a id="entry-3-2-tune-notsent-lowat-client"></a>

**`tune.notsent-lowat.client <size>`**

```haproxy
tune.notsent-lowat.client <size>
tune.notsent-lowat.server <size>
```

Passt die Pufferung des Kernels pro Socket so an, dass die Sendeseite eines Sockets als voll gemeldet wird, sobald die gepufferte Datenmenge diesem Wert zuzüglich der gemessenen Fenstergröße entspricht. Dabei sollen nur die unbedingt benötigten Bytes in den Socket-Puffern verbleiben, ergänzt um eine kleine Reserve für die Daten, die bis zum nächsten Sendeversuch von haproxy übertragen werden. Ein niedriger Wert (typischerweise etwa tune.bufsize) kann den Speicherverbrauch der Systempuffer erheblich verringern und die Latenz auf Anwendungsebene reduzieren, die durch das Leeren gepufferter Daten entsteht. Auf unterstützenden Systemen ist diese Einstellung im Allgemeinen wirksamer und genauer als tune.sndbuf.client und tune.sndbuf.client. Sie gilt pro Verbindung (je nach Einstellung für Verbindungen von einem Client oder zu einem Server) und wird nur für TCP-Verbindungen verwendet. Der Standardwert ist null und bedeutet unbegrenzt. Dies ist nur unter Linux verfügbar.

<a id="entry-3-2-tune-pattern-cache-size"></a>

**`tune.pattern.cache-size <number>`**

```haproxy
tune.pattern.cache-size <number>
```

Setzt die Größe des Caches für Mustersuchen auf `<number>` Einträge. Dieser LRU-Cache speichert frühere Suchen und deren Ergebnisse. Er wird von ACLs und Maps für langsame Mustersuchen verwendet, insbesondere mit den Vergleichsmethoden "sub", "reg", "dir", "dom", "end", "bin" sowie für Zeichenfolgenvergleiche ohne Beachtung der Groß-/Kleinschreibung. Er arbeitet auf Musterausdrücken und kann daher das Ergebnis einer Suche über alle in einer Konfigurationszeile angegebenen Muster speichern (einschließlich aller aus Dateien geladenen Muster). Einträge, die über HTTP-Aktionen oder die CLI aktualisiert werden, werden automatisch ungültig gemacht. Die Standardgröße beträgt 10000 Einträge. Dadurch bleibt der Speicherbedarf bei etwa 5 MB pro Prozess/Thread auf 32-Bit-Systemen und 8 MB pro Prozess/Thread auf 64-Bit-Systemen, da die Caches thread- beziehungsweise prozesslokal sind. Das Kollisionsrisiko in diesem Cache ist sehr gering und liegt in der Größenordnung der Cachegröße geteilt durch 2^64. Bei 10000 Anfragen pro Sekunde und der Standardgröße von 10000 Einträgen besteht typischerweise eine Wahrscheinlichkeit von 1%, dass ein Brute-Force-Angriff nach 60 Jahren eine einzige Kollision erzeugt, beziehungsweise von 0.1% nach 6 Jahren. Dies gilt als deutlich geringer als das Risiko einer Speicherbeschädigung durch alternde Komponenten. Falls dies nicht akzeptabel ist, kann der Cache durch Setzen dieses Parameters auf 0 deaktiviert werden.

<a id="entry-3-2-tune-peers-max-updates-at-once"></a>

**`tune.peers.max-updates-at-once <number>`**

```haproxy
tune.peers.max-updates-at-once <number>
```

Legt die maximale Anzahl von Stick-Tabellen-Aktualisierungen fest, die haproxy beim Senden von Nachrichten auf einmal zu verarbeiten versucht. Das Abrufen der Daten für diese Aktualisierungen erfordert Sperroperationen, die ohne Begrenzung auf Rechnern mit vielen Threads CPU-intensiv sein können. Sie können außerdem während der anfänglichen gebündelten Übertragung zwischen einem älteren und einem neueren Prozess die Latenz des Datenverkehrs erhöhen. Umgekehrt können niedrige Werte ebenfalls höheren CPU-Aufwand und eine längere Gesamtdauer verursachen. Der Standardwert ist 200; es wird empfohlen, ihn nicht zu ändern.

<a id="entry-3-2-tune-pipesize"></a>

**`tune.pipesize <size>`**

```haproxy
tune.pipesize <size>
```

Setzt die Größe der Kernel-Pipe-Puffer auf diesen Wert (in Byte). Standardmäßig verwenden Pipes die Standardgröße des Systems. Bei TCP-Splicing kann eine größere Pipe jedoch manchmal die Leistung verbessern, insbesondere wenn vermutet wird, dass die Pipes nicht vollständig gefüllt werden und viele splice()-Aufrufe erfolgen. Dies beeinflusst den Speicherbedarf des Kernels; der Wert darf daher nur geändert werden, wenn die Auswirkungen verstanden werden.

<a id="entry-3-2-tune-pool-high-fd-ratio"></a>

**`tune.pool-high-fd-ratio <number>`**

```haproxy
tune.pool-high-fd-ratio <number>
```

Legt den maximalen Anteil der von HAProxy global verwendeten Dateideskriptoren an der maximal nutzbaren Anzahl in Prozent fest, ab dem ungenutzte Verbindungen beendet werden, wenn keine Verbindung wiederverwendet werden kann und eine neue erstellt werden muss. Der Standardwert ist 25. Ein Viertel der Dateideskriptoren bedeutet, dass ungefähr die Hälfte der maximalen Anzahl von Frontend-Verbindungen eine ungenutzte Verbindung zum Backend vorhalten kann. Darüber hinauszugehen ist im allgemeinen Fall bei angestrebter Verbindungswiederverwendung vermutlich wenig sinnvoll.

<a id="entry-3-2-tune-pool-low-fd-ratio"></a>

**`tune.pool-low-fd-ratio <number>`**

```haproxy
tune.pool-low-fd-ratio <number>
```

Legt den maximalen Anteil der von HAProxy global verwendeten Dateideskriptoren an der maximal nutzbaren Anzahl in Prozent fest, ab dem keine weiteren Verbindungen zur Wiederverwendung in den Pool ungenutzter Verbindungen aufgenommen werden. Der Standardwert ist 20.

<a id="entry-3-2-tune-pt-zero-copy-forwarding"></a>

**`tune.pt.zero-copy-forwarding { on | off }`**

```haproxy
tune.pt.zero-copy-forwarding { on | off }
```

Aktiviert ('on') oder deaktiviert ('off') die kopierfreie Datenweiterleitung für den Pass-through-Multiplexer. Für ihre Verwendung muss auch Kernel-Splicing konfiguriert sein. Sie ist standardmäßig aktiviert.

Siehe auch: tune.disable-zero-copy-forwarding, option splice-auto, option splice-request und option splice-response

<a id="entry-3-2-tune-quic-be-cc-cubic-min-losses"></a>

**`tune.quic.be.cc.cubic-min-losses <number>`**

```haproxy
tune.quic.be.cc.cubic-min-losses <number>
tune.quic.fe.cc.cubic-min-losses <number>
```

Legt fest, wie viele verlorene Pakete erforderlich sind, damit der Cubic-Algorithmus zur Überlastungssteuerung tatsächlich ein Verlustereignis annimmt. Normalerweise gilt jedes Verlustereignis als Folge einer Überlastung und reicht aus, damit Cubic mit einem kleineren Fenster neu beginnt. Experimente zeigen jedoch zahlreiche Verlustursachen, die nichts mit Überlastung zu tun haben und als nicht überlastungsbedingte Verluste einzuordnen sind. Eine Anpassung des Fensters hat darauf keine Wirkung, außer die Kommunikation zu verlangsamen. Häufige Ursachen sind schwache Funksignale, Zustellung in falscher Reihenfolge, zufällige Verzögerungen durch hohe CPU-Auslastung auf einem Client oder ungenaue Systemzeitgeber. Diese Einstellung macht Cubic etwas toleranter gegenüber solchen Verlusten, indem sie die minimale Anzahl aufsummierter Verluste zwischen zwei ACKs ändert, die als Verlustereignis gilt. Der Standardwert ist 1. In Experimenten wurden teils deutliche Verbesserungen beobachtet, allerdings stets zusammen mit mehr durch erneute Übertragungen verschwendeter Bandbreite und einem erhöhten Risiko, bereits überlastete Verbindungen vollständig auszulasten. Der Wert 2 kann für kurze Zeit zum Vergleich einiger Messwerte verwendet werden. Überschreiten Sie niemals 2, ohne dass ein Experte die Situation zuvor analysiert hat. Standard- und Mindestwert sind 1. Verwenden Sie immer 1.

<a id="entry-3-2-tune-quic-cc-cubic-min-losses"></a>

**`tune.quic.cc.cubic.min-losses <number> (deprecated)`**

```haproxy
tune.quic.cc.cubic.min-losses <number> (deprecated)
```

Dieses Schlüsselwort ist seit 3.3 veraltet und wird in 3.5 entfernt. Dies ist Teil der Vereinheitlichung der QUIC-Konfiguration. Bei Verwendung gilt diese Einstellung nur für Frontend-Verbindungen.

<a id="entry-3-2-tune-quic-be-cc-hystart"></a>

**`tune.quic.be.cc.hystart { on | off }`**

```haproxy
tune.quic.be.cc.hystart { on | off }
tune.quic.fe.cc.hystart { on | off }
```

Aktiviert ('on') oder deaktiviert ('off') den Algorithmus HyStart++ (RFC 9406) für QUIC-Verbindungen. Er ersetzt die Slow-Start-Phase von Überlastungssteuerungsalgorithmen, die hohe Paketverluste verursachen kann. Standardmäßig ist er deaktiviert.

<a id="entry-3-2-tune-quic-cc-hystart"></a>

**`tune.quic.cc-hystart { on | off } (deprecated)`**

```haproxy
tune.quic.cc-hystart { on | off } (deprecated)
```

Dieses Schlüsselwort ist seit 3.3 veraltet und wird in 3.5 entfernt. Dies ist Teil der Vereinheitlichung der QUIC-Konfiguration. Bei Verwendung gilt diese Einstellung nur für Frontend-Verbindungen.

<a id="entry-3-2-tune-quic-be-cc-max-frame-loss"></a>

**`tune.quic.be.cc.max-frame-loss <number>`**

```haproxy
tune.quic.be.cc.max-frame-loss <number>
tune.quic.fe.cc.max-frame-loss <number>
```

Legt fest, wie oft ein einzelner QUIC-Frame maximal als verloren markiert werden darf. Wird die Grenze überschritten, gilt die Verbindung als fehlerhaft und wird sofort geschlossen.

Der Standardwert ist 10.

<a id="entry-3-2-tune-quic-max-frame-loss"></a>

**`tune.quic.max-frame-loss <number> (deprecated)`**

```haproxy
tune.quic.max-frame-loss <number> (deprecated)
```

Dieses Schlüsselwort ist seit 3.3 veraltet und wird in 3.5 entfernt. Dies ist Teil der Vereinheitlichung der QUIC-Konfiguration. Bei Verwendung gilt diese Einstellung nur für Frontend-Verbindungen.

<a id="entry-3-2-tune-quic-be-cc-max-win-size"></a>

**`tune.quic.be.cc.max-win-size <size>`**

```haproxy
tune.quic.be.cc.max-win-size <size>
tune.quic.fe.cc.max-win-size <size>
```

Legt die standardmäßige maximale Fenstergröße für die Überlastungssteuerung einer einzelnen QUIC-Verbindung auf der Frontend- oder Backend-Seite fest. Der Wert muss als ganze Zahl mit optionalem Suffix 'k', 'm' oder 'g' angegeben werden. Er muss zwischen 10k und 4g liegen.

Der QUIC-Multiplexer verwendet außerdem die aktuelle Größe des Überlastungsfensters, um zu entscheiden, ob beim Senden von Daten neue Stream-Puffer zugewiesen werden können. Die maximale Größe des Überlastungsfensters begrenzt somit auch diese Zuweisung.

Der Standardwert ist 480k.

Siehe auch die bind- und Serveroptionen "quic-cc-algo".

<a id="entry-3-2-tune-quic-frontend-default-max-window-size"></a>

**`tune.quic.frontend.default-max-window-size <size> (deprecated)`**

```haproxy
tune.quic.frontend.default-max-window-size <size> (deprecated)
```

Dieses Schlüsselwort ist seit 3.3 veraltet und wird in 3.5 entfernt. Dies ist Teil der Vereinheitlichung der QUIC-Konfiguration. Bei Verwendung gilt diese Einstellung nur für Frontend-Verbindungen.

<a id="entry-3-2-tune-quic-be-cc-reorder-ratio"></a>

**`tune.quic.be.cc.reorder-ratio <0..100, in percent>`**

```haproxy
tune.quic.be.cc.reorder-ratio <0..100, in percent>
tune.quic.fe.cc.reorder-ratio <0..100, in percent>
```

Der Faktor, der auf die berechnete Schwelle für die Umordnung von Paketen angewendet wird. Ein zu kleiner Wert kann dazu führen, dass viele Pakete als verloren erkannt werden.

Der Standardwert ist 50.

<a id="entry-3-2-tune-quic-reorder-ratio"></a>

**`tune.quic.reorder-ratio <0..100, in percent> (deprecated)`**

```haproxy
tune.quic.reorder-ratio <0..100, in percent> (deprecated)
```

Dieses Schlüsselwort ist seit 3.3 veraltet und wird in 3.5 entfernt. Dies ist Teil der Vereinheitlichung der QUIC-Konfiguration. Bei Verwendung gilt diese Einstellung nur für Frontend-Verbindungen.

<a id="entry-3-2-tune-quic-be-max-idle-timeout"></a>

**`tune.quic.be.max-idle-timeout <timeout>`**

```haproxy
tune.quic.be.max-idle-timeout <timeout>
tune.quic.fe.max-idle-timeout <timeout>
```

Legt den QUIC-Transportparameter max_idle_timeout auf der Frontend- oder Backend-Seite fest. Der Wert folgt dem HAProxy-Zeitformat und wird in Millisekunden angegeben. Er bestimmt die Zeitspanne, nach der eine Verbindung ohne Meldung geschlossen wird, wenn sie während der effektiven Zeitspanne inaktiv geblieben ist. Beide Endpunkte verwenden denselben ausgehandelten Wert: - den kleineren der beiden Parameter, wenn beide ungleich null sind, - den größeren, wenn nur einer ungleich null ist, - sind beide Parameter null, ist die Funktion deaktiviert.

Der Standardwert ist 30s.

<a id="entry-3-2-tune-quic-frontend-max-idle-timeout"></a>

**`tune.quic.frontend.max-idle-timeout <timeout> (deprecated)`**

```haproxy
tune.quic.frontend.max-idle-timeout <timeout> (deprecated)
```

Dieses Schlüsselwort ist seit 3.3 veraltet und wird in 3.5 entfernt. Dies ist Teil der Vereinheitlichung der QUIC-Konfiguration. Bei Verwendung gilt diese Einstellung nur für Frontend-Verbindungen.

<a id="entry-3-2-tune-quic-be-sec-glitches-threshold"></a>

**`tune.quic.be.sec.glitches-threshold <number>`**

```haproxy
tune.quic.be.sec.glitches-threshold <number>
tune.quic.fe.sec.glitches-threshold <number>
```

Legt die Schwelle für die Anzahl von Unregelmäßigkeiten pro Verbindung auf der Frontend- oder Backend-Seite fest, bei deren Erreichen die Verbindung automatisch beendet wird. Dadurch lassen sich fehlerhaft arbeitende Verbindungen automatisch beenden, ohne dafür explizite Regeln schreiben zu müssen. Der Standardwert ist null: Es wird keine Schwelle gesetzt, sodass kein Ereignis zum Schließen einer Verbindung führt. Beachten Sie, dass manche QUIC-Clients auf lange bestehenden Verbindungen gelegentlich einige Unregelmäßigkeiten verursachen können. Ein von null verschiedener Wert sollte daher vermutlich im Hunderter- oder Tausenderbereich liegen, um wirksam zu sein, ohne Clients mit geringfügigen Fehlern zu beeinträchtigen. Mit "tune.glitches.kill.cpu-usage" können Verbindungen auch erst dann beendet werden, wenn die CPU-Auslastung einen bestimmten Wert überschreitet.

Siehe auch: fc_glitches, tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-quic-frontend-glitches-threshold"></a>

**`tune.quic.frontend.glitches-threshold <number> (deprecated)`**

```haproxy
tune.quic.frontend.glitches-threshold <number> (deprecated)
```

Dieses Schlüsselwort ist seit 3.3 veraltet und wird in 3.5 entfernt. Dies ist Teil der Vereinheitlichung der QUIC-Konfiguration. Bei Verwendung gilt diese Einstellung nur für Frontend-Verbindungen.

<a id="entry-3-2-tune-quic-fe-sec-retry-threshold"></a>

**`tune.quic.fe.sec.retry-threshold <number>`**

```haproxy
tune.quic.fe.sec.retry-threshold <number>
```

Aktiviert die Retry-Funktion für alle konfigurierten QUIC-Listener dynamisch, sobald diese Anzahl halb offener Verbindungen erreicht ist. Eine halb offene Verbindung ist eine Verbindung, deren Handshake weder erfolgreich abgeschlossen noch fehlgeschlagen ist. Diese Einstellung erfordert ein gesetztes Cluster-Geheimnis, um zu funktionieren. Andernfalls wird sie ohne Meldung ignoriert (siehe "cluster-secret"). Sie wird ebenfalls ohne Meldung ignoriert, wenn die Verwendung von QUIC Retry erzwungen wurde (siehe "quic-force-retry").

Der Standardwert ist 100.

Weitere Informationen zu QUIC Retry finden Sie unter <https://www.rfc-editor.org/rfc/rfc9000.html#section-8.1.2>.

<a id="entry-3-2-tune-quic-retry-threshold"></a>

**`tune.quic.retry-threshold <number> (deprecated)`**

```haproxy
tune.quic.retry-threshold <number> (deprecated)
```

Dieses Schlüsselwort ist seit 3.3 veraltet und wird in 3.5 entfernt. Dies ist Teil der Vereinheitlichung der QUIC-Konfiguration. Bei Verwendung gilt diese Einstellung nur für Frontend-Verbindungen.

<a id="entry-3-2-tune-quic-fe-sock-per-conn"></a>

**`tune.quic.fe.sock-per-conn { default-on | force-off }`**

```haproxy
tune.quic.fe.sock-per-conn { default-on | force-off }
```

Legt global fest, welche Sockets QUIC-Frontend-Verbindungen für Empfangs- und Sendeoperationen verwenden. Verbindungen können den Listener-Socket gemeinsam nutzen oder jeweils einen eigenen Socket anlegen.

Der Standardwert ist "default-on". Dabei wird jeder QUIC-Verbindung ein eigener Socket zugewiesen. Dies ist die bevorzugte Option für bestmögliche Leistung bei hohem QUIC-Datenverkehr. Es ist auch die einzige Möglichkeit, einen ordnungsgemäßen Soft-Stop ohne Datenverlust für QUIC-Verbindungen sicherzustellen und vorübergehende Fehler bei sendto()-Operationen effizient zu behandeln. Dies setzt jedoch einige erweiterte Funktionen des UDP-Netzwerkstacks voraus. Wird Ihre Plattform als nicht kompatibel eingestuft, wechselt haproxy beim Start automatisch in den Modus "force-off". Beachten Sie, dass QUIC-Listener an privilegierten Ports möglicherweise unter uid 0 laufen müssen oder OS-spezifische Anpassungen wie System-Capabilities erfordern, damit die Ziel-uid solche Ports binden darf. Siehe auch die globale Direktive "setcap".

Der Wert "force-off" bedeutet, dass QUIC-Übertragungen über den gemeinsam genutzten Listener-Socket erfolgen. Bei geringem Datenverkehr kann dies ein guter Kompromiss sein, da der FD-Verbrauch sinkt. Die Leistung ist aufgrund höherer CPU-Auslastung jedoch nicht optimal, wenn viele Threads die Listener gemeinsam nutzen oder sehr viele QUIC-Verbindungen gleichzeitig verwendet werden können.

Diese Einstellung wirkt zusammen mit den jeweiligen bind-Optionen "quic-socket". Wenn global "default-on" eingestellt ist, wird dieser Modus für jeden Listener aktiviert, außer für solche mit "quic-socket listener". Wird dagegen global "force-off" verwendet, gilt dies für jede Listener-Instanz unabhängig von ihrer individuellen Konfiguration.

<a id="entry-3-2-tune-quic-socket-owner"></a>

**`tune.quic.socket-owner { connection | listener } (deprecated)`**

```haproxy
tune.quic.socket-owner { connection | listener } (deprecated)
```

Dieses Schlüsselwort ist seit 3.3 veraltet und wird in 3.5 entfernt. Dies ist Teil der Vereinheitlichung der QUIC-Konfiguration. Die neuere Option heißt "tune.quic.fe.sock-per-conn". Dabei entspricht der bisherige Wert "connection" dem neuen Wert "default-on" und "listener" dem Wert "force-off".

<a id="entry-3-2-tune-quic-be-stream-data-ratio"></a>

**`tune.quic.be.stream.data-ratio <0..100, in percent>`**

```haproxy
tune.quic.be.stream.data-ratio <0..100, in percent>
tune.quic.fe.stream.data-ratio <0..100, in percent>
```

Mit dieser Einstellung lässt sich die harte Obergrenze für die Anzahl der auf jedem Stream gleichzeitig unterwegs befindlichen Datenbytes festlegen. Sie wird als Prozentsatz der QUIC-Verbindungseinstellung stream rxbuf angegeben, wobei das Ergebnis auf bufsize aufgerundet wird.

Der Standardwert ist 90. Dies passt zum häufigsten Webszenario, in dem nur ein oder wenige Streams für Uploads verwendet werden, während die übrigen ausschließlich Downloads dienen. Bleibt die Verbindungsgrenze stream rxbuf auf einem angemessenen Niveau, stellt dies sicher, dass nur ein Teil der geöffneten Streams seine maximale Kapazität zuweisen kann.

Wenn eine Anwendung viele Upload-Streams parallel nutzt und diese ungleich bedient werden, kann eine Verringerung dieses Anteils sinnvoll sein, um die Verteilung gerechter zu machen und die Bandbreite pro Stream zu reduzieren.

Siehe auch: "tune.quic.be.stream.rxbuf", "tune.quic.fe.stream.rxbuf",
"tune.quic.be.stream.max-concurrent", "tune.quic.fe.stream.max-concurrent"

<a id="entry-3-2-tune-quic-frontend-stream-data-ratio"></a>

**`tune.quic.frontend.stream-data-ratio  <0..100, in percent> (deprecated)`**

```haproxy
tune.quic.frontend.stream-data-ratio  <0..100, in percent> (deprecated)
```

Dieses Schlüsselwort ist seit 3.3 veraltet und wird in 3.5 entfernt. Dies ist Teil der Vereinheitlichung der QUIC-Konfiguration. Bei Verwendung gilt diese Einstellung nur für Frontend-Verbindungen.

<a id="entry-3-2-tune-quic-be-stream-max-concurrent"></a>

**`tune.quic.be.stream.max-concurrent <number>`**

```haproxy
tune.quic.be.stream.max-concurrent <number>
tune.quic.fe.stream.max-concurrent <number>
```

Auf der Frontend-Seite wird dieser Wert für den angekündigten Transportparameter initial_max_streams_bidi verwendet. Er wird als maximale Anzahl bidirektionaler Streams erzwungen, die der entfernte Peer während der Lebensdauer der Verbindung gleichzeitig öffnen darf. Dadurch wird die Anzahl gleichzeitiger HTTP/3-Clientanfragen begrenzt.

Der Standardwert ist 100. Beachten Sie, dass eine Verringerung die Empfangspufferkapazität der Streams einschränken und dadurch den Uploaddurchsatz verschlechtern kann. Dies lässt sich durch Erhöhen der QUIC-Verbindungseinstellung stream rxbuf ausgleichen.

Auf der Backend-Seite erzwingt haproxy den Wert lokal, um die Anzahl gleichzeitiger Anfragen zu begrenzen, die über eine einzelne Verbindung gemultiplext werden. Die Flusskontrolle des Peers kann sie weiter einschränken. Es kann erforderlich sein, den Standardwert 100 zu verringern, um die Reaktionsfähigkeit einer Website zu verbessern, allerdings zulasten einer höheren Anzahl offener Backend-Verbindungen. Ähnlich wie auf der Frontend-Seite beeinflusst diese Einstellung direkt die Rx-Pufferkapazität, begrenzt hier jedoch die HTTP-Downloadkapazität. Die QUIC-Einstellung stream rxbuf kann erhöht werden, wenn überwiegend HTTP-Antworten verarbeitet werden, die größer als "tune.bufsize" sind.

Siehe auch: "tune.quic.be.stream.rxbuf", "tune.quic.fe.stream.rxbuf",
"tune.quic.be.stream.data-ratio", "tune.quic.fe.stream.data-ratio"

<a id="entry-3-2-tune-quic-fe-stream-max-total"></a>

**`tune.quic.fe.stream.max-total <number>`**

```haproxy
tune.quic.fe.stream.max-total <number>
```

Legt die maximale Anzahl von Anfragen fest, die eine einzelne QUIC-Verbindung verarbeiten kann. Sobald diese Gesamtzahl erreicht ist, wird die Verbindung geordnet beendet. Bei HTTP/3 geschieht dies durch einen GOAWAY-Frame. Endgültig geschlossen wird die Verbindung, wenn alle verbleibenden Übertragungen abgeschlossen sind.

Diese Einstellung wird über den QUIC-Flusskontrollmechanismus als harte Grenze für die Verbindung angewendet. Verletzt ein Peer sie, wird die Verbindung sofort geschlossen.

Mit dieser Einstellung können Clients dazu gezwungen werden, von Zeit zu Zeit neue Verbindungen zu öffnen, um weitere Anfragen zu senden, und Verbindungen nicht übermäßig lange aufrechtzuerhalten. Niedrige Werte erhöhen jedoch die Latenz auf Clientseite sowie den CPU-Verbrauch auf beiden Seiten durch TLS-Handshakes.

Der Standardwert ist 0. Damit gilt keine besondere Grenze außer der durch die Kodierung des QUIC-Protokolls vorgegebenen (2^60, mehr als eine Milliarde Milliarden).

<a id="entry-3-2-tune-quic-frontend-max-streams-bidi"></a>

**`tune.quic.frontend.max-streams-bidi <number> (deprecated)`**

```haproxy
tune.quic.frontend.max-streams-bidi <number> (deprecated)
```

Dieses Schlüsselwort ist seit 3.3 veraltet und wird in 3.5 entfernt. Dies ist Teil der Vereinheitlichung der QUIC-Konfiguration. Bei Verwendung gilt diese Einstellung nur für Frontend-Verbindungen.

<a id="entry-3-2-tune-quic-be-stream-rxbuf"></a>

**`tune.quic.be.stream.rxbuf <size>`**

```haproxy
tune.quic.be.stream.rxbuf <size>
tune.quic.fe.stream.rxbuf <size>
```

Diese Einstellung ist die harte Obergrenze für die Anzahl der auf einer QUIC-Frontend-Verbindung gleichzeitig unterwegs befindlichen Datenbytes. Sie wird als Wert für den Transportparameter initial_max_data verwendet. Abhängig von der Latenz beeinflusst sie direkt die Uploadbandbreite des Peers sowie den Speicherverbrauch pro Verbindung in haproxy.

Standardmäßig ist der Wert auf 0 gesetzt. Das bedeutet, dass er automatisch als Produkt aus max-concurrent und bufsize berechnet werden muss. Er kann beispielsweise erhöht werden, wenn eine Backend-Anwendung auf umfangreiche Uploads über Netzwerke mit hoher Latenz angewiesen ist.

Siehe auch: "tune.quic.be.stream.max-concurrent", "tune.quic.fe.stream.max-concurrent",
"tune.quic.be.stream.data-ratio", "tune.quic.fe.stream.data-ratio"

<a id="entry-3-2-tune-quic-frontend-max-data-size"></a>

**`tune.quic.frontend.max-data-size <size> (deprecated)`**

```haproxy
tune.quic.frontend.max-data-size <size> (deprecated)
```

Dieses Schlüsselwort ist seit 3.3 veraltet und wird in 3.5 entfernt. Dies ist Teil der Vereinheitlichung der QUIC-Konfiguration. Bei Verwendung gilt diese Einstellung nur für Frontend-Verbindungen.

<a id="entry-3-2-tune-quic-be-tx-pacing"></a>

**`tune.quic.be.tx.pacing { on | off }`**

```haproxy
tune.quic.be.tx.pacing { on | off }
tune.quic.fe.tx.pacing { on | off }
```

Aktiviert ('on') oder deaktiviert ('off') die Unterstützung für Pacing beim Senden über QUIC. Standardmäßig ist sie aktiv. Pacing soll die Datenausgabe gleichmäßiger verteilen, um Netzwerkverluste zu verringern. In den meisten Szenarien verbessert es den Netzwerkdurchsatz deutlich, indem erneute Übertragungen vermieden werden. Auf Netzwerken mit sehr hoher Bandbreite und niedriger Latenz kann eine Deaktivierung jedoch sinnvoll sein, um unerwünschte Verzögerungen zu vermeiden und den CPU-Verbrauch zu verringern.

Siehe auch die bind- und Serveroptionen "quic-cc-algo".

<a id="entry-3-2-tune-quic-disable-tx-pacing"></a>

**`tune.quic.disable-tx-pacing (deprecated)`**

```haproxy
tune.quic.disable-tx-pacing (deprecated)
```

Dieses Schlüsselwort ist seit 3.3 veraltet und wird in 3.5 entfernt. Dies ist Teil der Vereinheitlichung der QUIC-Konfiguration. Bei Verwendung gilt diese Einstellung nur für Frontend-Verbindungen.

<a id="entry-3-2-tune-quic-be-tx-udp-gso"></a>

**`tune.quic.be.tx.udp-gso { on | off }`**

```haproxy
tune.quic.be.tx.udp-gso { on | off }
tune.quic.fe.tx.udp-gso { on | off }
```

Aktiviert ('on') oder deaktiviert ('off') die Unterstützung für UDP GSO beim Senden über QUIC. Standardmäßig ist sie aktiv. Diese Kernel-Funktion ermöglicht das Senden mehrerer Datagramme mit einem einzigen Systemaufruf, was bei großen Übertragungen effizienter ist. Bei Verdacht auf ein Sendeproblem kann es sinnvoll sein, sie auf Empfehlung der Entwickler zu deaktivieren.

<a id="entry-3-2-tune-quic-disable-udp-gso"></a>

**`tune.quic.disable-udp-gso (deprecated)`**

```haproxy
tune.quic.disable-udp-gso (deprecated)
```

Dieses Schlüsselwort ist seit 3.3 veraltet und wird in 3.5 entfernt. Dies ist Teil der Vereinheitlichung der QUIC-Konfiguration. Bei Verwendung gilt diese Einstellung nur für Frontend-Verbindungen.

<a id="entry-3-2-tune-quic-listen"></a>

**`tune.quic.listen { on | off }`**

```haproxy
tune.quic.listen { on | off }
```

Deaktiviert das QUIC-Transportprotokoll auf der Frontend-Seite. Alle QUIC-Listener werden weiterhin erstellt, lauschen jedoch nicht auf eingehende Datagramme. Somit verarbeitet haproxy auf der Frontend-Seite keinen QUIC-Datenverkehr.

Der Standardwert ist "on". Bei Verdacht auf ein Problem mit QUIC-Datenverkehr lassen sich die QUIC-Listener mit dieser Option einfach ein- oder ausschalten, ohne jede einzelne Konfigurationszeile ändern zu müssen.

Siehe auch den Sample-Fetch "quic_enabled".

<a id="entry-3-2-tune-quic-mem-tx-max"></a>

**`tune.quic.mem.tx-max <size>`**

```haproxy
tune.quic.mem.tx-max <size>
```

Legt die maximale Speichermenge fest, die der QUIC-Stack auf der Transportschicht zum Senden verwenden darf. Dies begrenzt sowohl die gleichzeitig unterwegs befindlichen Bytes als auch die Ausgabepuffer des Multiplexers. Beachten Sie, dass diese Grenze zur Vermeidung von Konkurrenz zwischen Threads nicht strikt erzwungen wird und daher gelegentlich überschritten werden kann. Außerdem kann jede Verbindung stets ein Fenster von mindestens 2 Datagrammen verwenden. Daher sollte gleichzeitig ein passender maxconn-Wert gesetzt werden.

<a id="entry-3-2-tune-quic-frontend-max-tx-mem"></a>

**`tune.quic.frontend.max-tx-mem <size> (deprecated)`**

```haproxy
tune.quic.frontend.max-tx-mem <size> (deprecated)
```

Dieses Schlüsselwort ist seit 3.3 veraltet und wird in 3.5 entfernt. Dies ist Teil der Vereinheitlichung der QUIC-Konfiguration. Bei Verwendung gilt diese Einstellung nur für Frontend-Verbindungen.

<a id="entry-3-2-tune-quic-zero-copy-fwd-send"></a>

**`tune.quic.zero-copy-fwd-send { on | off }`**

```haproxy
tune.quic.zero-copy-fwd-send { on | off }
```

Aktiviert ('on') oder deaktiviert ('off') das kopierfreie Senden von Daten für den QUIC-Multiplexer. Es ist standardmäßig aktiviert.

Siehe auch: tune.disable-zero-copy-forwarding

<a id="entry-3-2-tune-renice-runtime"></a>

**`tune.renice.runtime <number>`**

```haproxy
tune.renice.runtime <number>
```

Diese Konfigurationsoption nimmt einen Wert zwischen -20 und 19 an. Sie setzt eine Scheduling-Priorität, wie in man 2 setpriority beschrieben. Die Priorität wird nach dem Einlesen der Konfiguration angewendet, also nur vom Worker oder vom eigenständig laufenden Prozess. Üblicherweise wird damit eine höhere Priorität als für einen Prozess festgelegt, der gerade die Konfiguration einliest (tune.renice.startup).

Siehe auch: tune.renice.startup

<a id="entry-3-2-tune-renice-startup"></a>

**`tune.renice.startup <number>`**

```haproxy
tune.renice.startup <number>
```

Diese Konfigurationsoption nimmt einen Wert zwischen -20 und 19 an. Sie setzt eine Scheduling-Priorität, wie in man 2 setpriority beschrieben. Die Priorität wird vor der übrigen Konfiguration angewendet, was nützlich sein kann, wenn die Priorität beim Einlesen der Konfiguration verringert werden soll. Dies betrifft den eigenständig laufenden Prozess oder den Worker vor dem Einlesen der Konfiguration. Sobald die Konfiguration eingelesen ist, wird die vorherige Priorität wiederhergestellt, sofern tune.renice.runtime nicht verwendet wird.

Siehe auch: tune.renice.runtime

<a id="entry-3-2-tune-rcvbuf-backend"></a>

**`tune.rcvbuf.backend  <size>`**

```haproxy
tune.rcvbuf.backend  <size>
tune.rcvbuf.frontend <size>
```

Setzt die Größe des Kernel-Empfangspuffers für nicht verbundene Sockets auf diesen Wert. Dies kann für QUIC im Listener-Modus und für log-forward im Frontend verwendet werden. Die Standardpuffer des Systems sind mitunter für Sockets mit viel gebündeltem Datenverkehr zu klein, was Verluste und gegebenenfalls erneute Übertragungen (bei QUIC) verursachen und den Verbindungsaufbau unter hoher Last verlangsamen kann. Der Wert wird in Byte angegeben und auf jeden Socket angewendet. Im Listener-Modus werden Sockets von allen Verbindungen gemeinsam genutzt; die Gesamtzahl der Sockets hängt vom "shards"-Wert der "bind"-Zeile ab. Es gibt keinen allgemeingültigen guten Wert. Ein geeigneter Wert entspricht der erwarteten Größe pro Verbindung multipliziert mit der erwarteten Anzahl von Verbindungen. Der Kernel kann große Werte begrenzen. Siehe auch "tune.rcvbuf.client" und "tune.rcvbuf.server" für die entsprechenden Einstellungen verbundener Sockets sowie "tune.sndbuf.backend" und "tune.sndbuf.frontend" für die Sendeseite.

<a id="entry-3-2-tune-rcvbuf-client"></a>

**`tune.rcvbuf.client <size>`**

```haproxy
tune.rcvbuf.client <size>
tune.rcvbuf.server <size>
```

Erzwingt die angegebene Größe in Byte für den Kernel-Empfangspuffer von Sockets auf der Client- oder Serverseite. Dieser Wert gilt für alle TCP/HTTP-Frontends und -Backends. Er sollte normalerweise niemals gesetzt werden. Die Standardgröße (0) lässt den Kernel den Wert anhand der verfügbaren Speichermenge automatisch anpassen. Manchmal können jedoch sehr niedrige Werte (z. B. 4096) helfen, Kernel-Speicher zu sparen, indem die Pufferung übermäßig großer empfangener Datenmengen verhindert wird. Niedrigere Werte erhöhen allerdings die CPU-Auslastung erheblich.

<a id="entry-3-2-tune-recv-enough"></a>

**`tune.recv_enough <size>`**

```haproxy
tune.recv_enough <size>
```

HAProxy verwendet einige Hinweise, um zu erkennen, ob ein kurzer Lesevorgang das Ende der Socket-Puffer anzeigt. Einer davon ist, dass ein Lesevorgang mehr als `<recv_enough>` Bytes zurückgibt. Der Standardwert ist 10136 (7 Segmente mit jeweils 1448). Mit dieser Einstellung lässt sich der Standardwert ändern, um Arbeitslasten mit vielen kurzen Nachrichten wie telnet- oder SSH-Sitzungen besser zu verarbeiten.

<a id="entry-3-2-tune-ring-queues"></a>

**`tune.ring.queues <number>`**

```haproxy
tune.ring.queues <number>
```

Legt die Anzahl der Schreibwarteschlangen vor Ringpuffern fest. Dies kann den CPU-Verbrauch von Traces bei der Fehlerdiagnose beeinflussen; sowohl zu niedrige als auch zu hohe Werte können erhebliche Auswirkungen haben. Ein geeigneter Wert wurde von den Entwicklern experimentell bestimmt. Daher sollte es keinen Grund geben, ihn zu ändern, sofern dies nicht zur Behebung bestimmter Probleme angefordert wird. Eine solche Einstellung sollte bei Versionsupgrades nicht dauerhaft in der Konfiguration verbleiben, da sich ihr optimaler Wert im Laufe der Zeit ändern kann.

<a id="entry-3-2-tune-runqueue-depth"></a>

**`tune.runqueue-depth <number>`**

```haproxy
tune.runqueue-depth <number>
```

Legt die maximale Anzahl von Tasks fest, die bei der Task-Ausführung auf einmal verarbeitet werden können. Der Standardwert hängt von der Thread-Anzahl ab, liegt aber zwischen 35 und 280, womit tendenziell die höchsten Anfrageraten und niedrigsten Latenzen erzielt werden. Eine Erhöhung kann die Latenz bei I/O-Operationen erhöhen; ein zu niedriger Wert kann zusätzlichen Aufwand verursachen. Bei höherer Thread-Anzahl sind niedrigere Werte vorteilhaft. Beim Experimentieren mit deutlich höheren Werten kann es sinnvoll sein, zusätzlich tune.sched.low-latency und gegebenenfalls tune.fd.edge-triggered zu aktivieren, um die maximale Latenz möglichst gering zu halten.

<a id="entry-3-2-tune-sched-low-latency"></a>

**`tune.sched.low-latency { on | off }`**

```haproxy
tune.sched.low-latency { on | off }
```

Aktiviert ('on') oder deaktiviert ('off') den Task-Scheduler für niedrige Latenz. Standardmäßig verarbeitet HAProxy Tasks aus mehreren Klassen jeweils klassenweise, da dies am effizientesten ist. Bei hohen Werten von tune.runqueue-depth kann dies jedoch messbare Auswirkungen auf die Anfrage- oder Verbindungslatenz haben. Ist diese Einstellung aktiviert, werden vorhandene Tasks aus Klassen mit niedrigerer Priorität immer vor den anderen ausgeführt. Dadurch lässt sich die maximale Latenz neuer Anfragen oder Verbindungen inmitten sehr hohen Datenverkehrs verringern, allerdings zulasten einer stärkeren Beeinträchtigung dieses umfangreichen Datenverkehrs. Für den regulären Einsatz sollte diese Option besser deaktiviert bleiben. Der Standardwert ist off.

<a id="entry-3-2-tune-sndbuf-backend"></a>

**`tune.sndbuf.backend  <size>`**

```haproxy
tune.sndbuf.backend  <size>
tune.sndbuf.frontend <size>
```

Setzt die Größe des Kernel-Sendepuffers für nicht verbundene Sockets auf diesen Wert. Dies kann für die Protokollierung über UNIX-Sockets und UDP auf der Backend-Seite sowie für QUIC im Listener-Modus auf der Frontend-Seite verwendet werden. Die Standardpuffer des Systems sind mitunter für Sockets, die von vielen Verbindungen oder Protokollsendern gemeinsam genutzt werden, zu klein. Dies verursacht Verluste und möglicherweise erneute Übertragungen und verlangsamt den Aufbau neuer Verbindungen bei hohem Datenverkehr. Der Wert wird in Byte angegeben und auf jeden Socket angewendet. Im Listener-Modus werden Sockets von allen Verbindungen gemeinsam genutzt; die Gesamtzahl der Sockets hängt vom "shards"-Wert der "bind"-Zeile ab. Es gibt keinen allgemeingültigen guten Wert. Ein geeigneter Wert entspricht der erwarteten Größe pro Verbindung multipliziert mit der erwarteten Anzahl von Verbindungen. Der Kernel kann große Werte begrenzen. Siehe auch "tune.sndbuf.client" und "tune.sndbuf.server" für die entsprechenden Einstellungen verbundener Sockets sowie "tune.rcvbuf.backend" und "tune.rcvbuf.frontend" für die Empfangsseite.

<a id="entry-3-2-tune-sndbuf-client"></a>

**`tune.sndbuf.client <size>`**

```haproxy
tune.sndbuf.client <size>
tune.sndbuf.server <size>
```

Erzwingt die angegebene Größe in Byte für den Kernel-Sendepuffer von Sockets auf der Client- oder Serverseite. Dieser Wert gilt für alle TCP/HTTP-Frontends und -Backends. Er sollte normalerweise niemals gesetzt werden. Die Standardgröße (0) lässt den Kernel den Wert anhand der verfügbaren Speichermenge automatisch anpassen. Manchmal können jedoch sehr niedrige Werte (z. B. 4096) helfen, Kernel-Speicher zu sparen, indem die Pufferung übermäßig großer empfangener Datenmengen verhindert wird. Niedrigere Werte erhöhen allerdings die CPU-Auslastung erheblich. Ein weiterer Anwendungsfall ist das Verhindern von Schreibzeitüberschreitungen bei extrem langsamen Clients, wenn der Kernel wartet, bis ein großer Teil des Puffers gelesen wurde, bevor er HAProxy erneut benachrichtigt. Siehe auch tune.notsent-lowat.client und tune.notsent-lowat.server für wirksamere Einstellungen, die unter Linux eine feinere Steuerung von Speicherverbrauch und Reaktionsfähigkeit ohne Leistungseinbußen ermöglichen.

<a id="entry-3-2-tune-ssl-cachesize"></a>

**`tune.ssl.cachesize <number>`**

```haproxy
tune.ssl.cachesize <number>
```

Legt die Größe des globalen SSL-Sitzungscaches in Blöcken fest. Ein Block ist groß genug, um eine kodierte Sitzung ohne Peer-Zertifikat aufzunehmen. Eine kodierte Sitzung mit Peer-Zertifikat wird abhängig von dessen Größe in mehreren Blöcken gespeichert. Ein Block benötigt ungefähr 200 Byte Speicher (basierend auf der Berechnung `sizeof(struct sh_ssl_sess_hdr) + SHSESS_BLOCK_MIN_SIZE`, die für die Funktion `shctx_init` verwendet wird). Der Standardwert kann beim Kompilieren festgelegt werden; andernfalls beträgt er 20000. Ist der Cache voll, werden die am längsten ungenutzten Einträge entfernt und neu vergeben. Höhere Werte verringern die Häufigkeit solcher Bereinigungen und damit die Anzahl CPU-intensiver SSL-Handshakes, indem die Sitzungen aller Benutzer möglichst lange erhalten bleiben. Alle Einträge werden beim Start vorab zugewiesen. Der Wert 0 deaktiviert den SSL-Sitzungscache.

<a id="entry-3-2-tune-ssl-capture-buffer-size"></a>

**`tune.ssl.capture-buffer-size <number>`**

```haproxy
tune.ssl.capture-buffer-size <number>
tune.ssl.capture-cipherlist-size <number> (deprecated)
```

Legt die maximale Größe des Puffers zur Erfassung der Verschlüsselungsalgorithmenliste, Erweiterungsliste, Liste elliptischer Kurven und Punktformate elliptischer Kurven aus dem ClientHello fest. Bei 0 (dem Standardwert) ist die Erfassung deaktiviert; andernfalls wird für jede SSL/TLS-Verbindung ein Puffer zugewiesen.

<a id="entry-3-2-tune-ssl-certificate-compression"></a>

**`tune.ssl.certificate-compression { auto | off }`**

```haproxy
tune.ssl.certificate-compression { auto | off }
```

Diese Einstellung konfiguriert die Unterstützung für Zertifikatskomprimierung, eine Erweiterung (RFC 8879) für TLS 1.3.

Bei "auto" wird der Standardwert der TLS-Bibliothek verwendet.

Bei "off" wird versucht, die Unterstützung für diese Funktion ausdrücklich zu deaktivieren. HAProxy versucht dann weder, komprimierte Zertifikate zu senden, noch akzeptiert es solche Zertifikate.

Konfiguriert sowohl die Backend- als auch die Frontend-Seite.

Dieses Schlüsselwort wird von OpenSSL \>= 3.2.0 unterstützt.

Der Standardwert ist auto.

<a id="entry-3-2-tune-ssl-default-dh-param"></a>

**`tune.ssl.default-dh-param <number>`**

```haproxy
tune.ssl.default-dh-param <number>
```

Legt die maximale Größe der Diffie-Hellman-Parameter fest, die beim DHE-Schlüsselaustausch zur Erzeugung des ephemeren beziehungsweise temporären Diffie-Hellman-Schlüssels verwendet werden. Für die endgültige Größe wird versucht, die Größe des RSA- oder DSA-Schlüssels des Servers zu übernehmen (z. B. einen temporären DH-Schlüssel mit 2048 Bit für einen RSA-Schlüssel mit 2048 Bit), ohne jedoch diesen Höchstwert zu überschreiten. Es sind nur Werte ab 1024 erlaubt. Höhere Werte erhöhen die CPU-Last; Werte über 1024 Bit werden von Java 7 und älteren Clients nicht unterstützt. Dieser Wert wird nicht verwendet, wenn statische Diffie-Hellman-Parameter entweder direkt in der Zertifikatsdatei oder über ssl-dh-param-file bereitgestellt werden. Sind weder default-dh-param noch ssl-dh-param-file definiert und enthält die PEM-Datei des Servers für ein bestimmtes Frontend keine eigenen DH-Parameter, stehen DHE-Verschlüsselungsverfahren für dieses Frontend nicht zur Verfügung.

<a id="entry-3-2-tune-ssl-force-private-cache"></a>

**`tune.ssl.force-private-cache`**

```haproxy
tune.ssl.force-private-cache
```

Diese Option deaktiviert die gemeinsame Nutzung des SSL-Sitzungscaches zwischen allen Prozessen. Sie sollte normalerweise nicht verwendet werden, da sie viele Neuverhandlungen erzwingt, wenn Clients zufällig bei unterschiedlichen Prozessen landen. Auf einigen Betriebssystemen, auf denen keine der Synchronisierungsmethoden für den SSL-Cache verwendet werden kann, ist sie jedoch möglicherweise erforderlich. In diesem Fall kann eine zusätzliche Ebene mit hashbasierter Lastverteilung vor der SSL-Ebene die Auswirkungen der fehlenden gemeinsamen Sitzungsnutzung begrenzen.

<a id="entry-3-2-tune-ssl-hard-maxrecord"></a>

**`tune.ssl.hard-maxrecord <number>`**

```haproxy
tune.ssl.hard-maxrecord <number>
```

Legt die maximale Anzahl von Bytes fest, die zu einem Zeitpunkt an SSL_write() übergeben werden. Der Standardwert 0 bedeutet, dass es keine Begrenzung gibt. Im Gegensatz zu tune.ssl.maxrecord wird diese Einstellung nicht dynamisch angepasst. Kleinere Records können den Durchsatz verringern, sind aber bei ressourcenarmen Clients möglicherweise erforderlich.

<a id="entry-3-2-tune-ssl-keylog"></a>

**`tune.ssl.keylog { on | off }`**

```haproxy
tune.ssl.keylog { on | off }
```

Diese Option aktiviert die Protokollierung der TLS-Schlüssel. Sie sollte mit Vorsicht verwendet werden, da sie pro SSL-Sitzung mehr Speicher verbraucht und die Leistung beeinträchtigen könnte. Standardmäßig ist sie deaktiviert.

Diese Sample-Fetches sollten verwendet werden, um die SSLKEYLOGFILE zu erzeugen, die zum Entschlüsseln des Datenverkehrs mit wireshark erforderlich ist.

<https://tlswg.org/sslkeylogfile/draft-ietf-tls-keylogfile.html>

SSLKEYLOG besteht aus einer Reihe von Zeilen mit folgendem Format:

```text
<Label> <space> <ClientRandom> <space> <Secret>
```

ClientRandom wird vom Sample-Fetch %[ssl_fc_client_random,hex] bereitgestellt. Das Geheimnis und das Label finden Sie in der folgenden Tabelle. Sie müssen eine SSLKEYLOGFILE mit allen Labels dieser Tabelle erzeugen.

Die folgenden Sample-Fetches liefern hexadezimale Zeichenfolgen und müssen nicht konvertiert werden.

```text
  SSLKEYLOGFILE-Bezeichnung       |  Sample-Abrufe für die geheimen Werte
  --------------------------------|-----------------------------------------
  CLIENT_EARLY_TRAFFIC_SECRET     |  %[ssl_xx_client_early_traffic_secret]
  CLIENT_HANDSHAKE_TRAFFIC_SECRET |  %[ssl_xx_client_handshake_traffic_secret]
  SERVER_HANDSHAKE_TRAFFIC_SECRET |  %[ssl_xx_server_handshake_traffic_secret]
  CLIENT_TRAFFIC_SECRET_0         |  %[ssl_xx_client_traffic_secret_0]
  SERVER_TRAFFIC_SECRET_0         |  %[ssl_xx_server_traffic_secret_0]
  EXPORTER_SECRET                 |  %[ssl_xx_exporter_secret]
  EARLY_EXPORTER_SECRET           |  %[ssl_xx_early_exporter_secret]
```

Diese Fetches stehen für die Frontend- (fc) und Backend-Seite (bc) zur Verfügung. Ersetzen Sie "xx" durch "fc" oder "bc", um die gewünschte Seite zu verwenden.

Dies ist nur mit OpenSSL 1.1.1 verfügbar und für TLS1.3-Sitzungen nützlich.

Wenn Sie den Inhalt einer SSLKEYLOGFILE für TLS \< 1.3 erzeugen möchten, benötigen Sie nur diese Zeile:

"CLIENT_RANDOM %[ssl_fc_client_random,hex] %[ssl_fc_session_key,hex]"

Ein vollständiges Schlüsselprotokoll lässt sich mit einem log-format wie folgt erzeugen, auch wenn dies für Syslog nicht ideal ist:

```text
log-format "CLIENT_EARLY_TRAFFIC_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_client_early_traffic_secret]\n
            CLIENT_HANDSHAKE_TRAFFIC_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_client_handshake_traffic_secret]\n
            SERVER_HANDSHAKE_TRAFFIC_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_server_handshake_traffic_secret]\n
            CLIENT_TRAFFIC_SECRET_0 %[ssl_bc_client_random,hex] %[ssl_bc_client_traffic_secret_0]\n
            SERVER_TRAFFIC_SECRET_0 %[ssl_bc_client_random,hex] %[ssl_bc_server_traffic_secret_0]\n
            EXPORTER_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_exporter_secret]\n
            EARLY_EXPORTER_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_early_exporter_secret]"
```

HAProxy stellt die obigen Formate auch als vordefinierte Umgebungsvariablen bereit, die direkt in einer "log-format"-Direktive verwendet werden können:

```shell
$HAPROXY_KEYLOG_FC_LOG_FMT   Verbindungsschlüssel für das Frontend (zum Client)
$HAPROXY_KEYLOG_BC_LOG_FMT   Verbindungsschlüssel für das Backend (zum Server)
```

<a id="entry-3-2-tune-ssl-keyupdate-rate-limit"></a>

**`tune.ssl.keyupdate-rate-limit <limit>`**

```haproxy
tune.ssl.keyupdate-rate-limit <limit>
```

Begrenzt die Anzahl von KeyUpdate-Nachrichten, die pro Sekunde akzeptiert werden, auf `<limit>`, bevor dies als Flut betrachtet und die Verbindung beendet wird. Die Verarbeitung von KeyUpdate ist CPU-intensiv, und es gibt kaum einen Grund, viele solcher Nachrichten zu empfangen. Der Wert "0" deaktiviert die Ratenbegrenzung. Der Standardwert ist 100. <a id="entry-3-2-tune-ssl-lifetime"></a>

**`tune.ssl.lifetime <timeout>`**

```haproxy
tune.ssl.lifetime <timeout>
```

Legt fest, wie lange eine zwischengespeicherte SSL-Sitzung gültig bleiben darf. Die Zeit wird in Sekunden angegeben und beträgt standardmäßig 300 (5 Minuten). Dies garantiert nicht, dass Sitzungen so lange erhalten bleiben: Ist der Cache voll, werden die am längsten ungenutzten Sitzungen unabhängig von ihrer konfigurierten Lebensdauer entfernt. Der eigentliche Zweck dieser Einstellung besteht darin, eine zu lange Verwendung von Sitzungen zu verhindern.

<a id="entry-3-2-tune-ssl-maxrecord"></a>

**`tune.ssl.maxrecord <number>`**

```haproxy
tune.ssl.maxrecord <number>
```

Legt die maximale Anzahl von Bytes fest, die zu Beginn der Datenübertragung an SSL_write() übergeben werden. Der Standardwert 0 bedeutet, dass es keine Begrenzung gibt. Bei SSL/TLS kann der Client Daten erst entschlüsseln, nachdem er einen vollständigen Record empfangen hat. Bei großen Records müssen Clients daher möglicherweise bis zu 16kB herunterladen, bevor sie mit der Verarbeitung beginnen können. Eine Begrenzung kann die Seitenladezeiten in Browsern verbessern, die über Netzwerke mit hoher Latenz oder niedriger Bandbreite verbunden sind. Es wird empfohlen, optimale Werte zu finden, die in 1 oder 2 TCP-Segmente passen (im Allgemeinen 1448 Byte über Ethernet mit aktivierten TCP-Zeitstempeln beziehungsweise 1460 bei deaktivierten Zeitstempeln). Dabei muss der zusätzliche Aufwand durch SSL/TLS berücksichtigt werden. Typische Werte von 1419 und 2859 lieferten in Tests gute Ergebnisse. Verwenden Sie "strace -e trace=write", um den besten Wert zu ermitteln. HAProxy wechselt automatisch zu dieser Einstellung, sobald ein inaktiver Stream erkannt wurde (siehe tune.idletimer oben). Siehe auch tune.ssl.hard-maxrecord.

<a id="entry-3-2-tune-ssl-ssl-ctx-cache-size"></a>

**`tune.ssl.ssl-ctx-cache-size <number>`**

```haproxy
tune.ssl.ssl-ctx-cache-size <number>
```

Setzt die Größe des Caches für erzeugte Zertifikate auf `<number>` Einträge. Dies ist ein LRU-Cache. Da die dynamische Erzeugung eines SSL-Zertifikats aufwendig ist, werden die Zertifikate zwischengespeichert. Die Standardgröße beträgt 1000 Einträge.

<a id="entry-3-2-tune-streams-elasticity"></a>

**`tune.streams-elasticity <number>`**

```haproxy
tune.streams-elasticity <number>
```

Definiert einen Zielprozentsatz für Streams pro Frontend-Verbindung im Verhältnis zur maximalen Anzahl gleichzeitiger Verbindungen (maxconn), wenn alle Verbindungen aufgebaut sind. Diese Kennzahl gilt für gemultiplexte Protokolle wie HTTP/2 oder QUIC, bei denen jede Verbindung mehrere Streams empfangen kann. Mindestens einer ist immer garantiert; der Prozentsatz muss daher mindestens 100% betragen. Während des Verbindungsaufbaus kündigt HAProxy dynamisch zusätzliche Streams bis zur konfigurierten Grenze an und hält dabei das Zielverhältnis ein. Beim Aufbau erhält jede Frontend-Verbindung mindestens einen Stream. Zusätzliche Streams werden anhand des Zielprozentsatzes und der konfigurierten Stream-Grenzen zugeteilt. Dies ermöglicht eine effiziente Stream-Zuweisung bei wechselnder Last: mehr Streams bei niedriger und weniger bei hoher Last.

Hochdynamische Websites mit vielen Objekten pro Seite profitieren von hohen Verhältnissen, die viele Streams pro Verbindung ermöglichen. Websites, die im Durchschnitt weniger Streams verwenden (WebSocket, Anwendungscode), können niedrigere Verhältnisse nahe 120 oder 150 bevorzugen (20 bis 50% mehr Streams als Verbindungen), um bei anhaltender Last übermäßige Stream-Anzahlen zu verhindern.

Der Standardwert ist 0 und bedeutet, dass auf dieser Ebene keine Begrenzung erzwungen wird. Es gelten nur die H2- und QUIC-Konfigurationen (bei der Standardeinstellung von 100 Streams pro Verbindung entspricht dies 10000%). Für kleine Installationen mit maxconn um tausend bleibt dies die empfohlene Einstellung. Mittelgroße Installationen mit einigen tausend bis einigen zehntausend Verbindungen setzen das Verhältnis typischerweise zwischen 1000 und 5000 und erlauben damit bei Volllast 10 bis 50 Streams pro Verbindung. Große Installationen mit Hunderttausenden bis Millionen Verbindungen können niedrigere Werte (120 bis 200) verwenden, um bei Volllast im Durchschnitt 1.2 bis 2 Streams pro Verbindung zu unterstützen.

Im Gegensatz zu HTTP/2 kann QUIC die Anzahl gleichzeitiger Streams während der Lebensdauer einer Verbindung dynamisch anpassen. Die QUIC-Flusskontrolle ist jedoch strenger als die von HTTP/2. Daher sollten bei ihrer Verwendung ausreichend hohe Werte angegeben werden, um zusätzliche Latenz auf der Verbindung zu vermeiden. Für QUIC-Listener mit aktiviertem 0-RTT gibt es eine weitere Einschränkung: Der dem Peer anfänglich angekündigte Wert ignoriert die Stream-Elastizität und richtet sich ausschließlich nach "tune.quic.fe.stream.max-concurrent". Nach dieser ersten Ankündigung bleibt das Prinzip der Stream-Elastizität während der Lebensdauer der Verbindung jedoch wirksam.

Die Überwachung der Gesamtzahl aktiver Streams in Backends einschließlich der Warteschlangen liefert einen praktischen Anhaltspunkt für eine dauerhaft tragbare Ziellast und hilft, übermäßige Kapazitätsbereitstellung zu vermeiden.

<a id="entry-3-2-tune-stick-counters"></a>

**`tune.stick-counters <number>`**

```haproxy
tune.stick-counters <number>
```

Legt die Anzahl von Stick-Zählern fest, die eine Verbindung oder Anfrage gleichzeitig über "track-sc\*"-Aktionen in "tcp-request"- oder "http-request"-Regeln verfolgen darf. Der Standardwert wird beim Kompilieren durch das Makro MAX_SESS_STK_CTR festgelegt und beträgt standardmäßig 3. Mit dieser Einstellung lässt sich der Wert ändern und der beim Kompilieren angegebene Wert ignorieren; er darf jedoch nicht größer als 100 sein. Eine Erhöhung kann beim Übertragen komplexer Konfigurationen auf haproxy erforderlich sein, verursacht jedoch Kosten: Jeder Eintrag benötigt 16 Byte pro Verbindung und 16 Byte pro Anfrage. Dieser Speicher muss für alle Anfragen zugewiesen und mit Nullen gefüllt werden, selbst wenn er nicht verwendet wird. Der Wert 10 erhöht daher den Speicherverbrauch pro Anfrage um 320 Byte und bewirkt, dass dieser Speicher für jede Anfrage gelöscht wird, was messbare CPU-Auswirkungen hat. Werden dagegen keine "track-sc"-Regeln verwendet, kann der Wert verringert werden (0 ist zulässig und deaktiviert Stick-Zähler vollständig).

<a id="entry-3-2-tune-takeover-other-tg-connections"></a>

**`tune.takeover-other-tg-connections <value>`**

```haproxy
tune.takeover-other-tg-connections <value>
```

Standardmäßig wird nicht versucht, ungenutzte Verbindungen aus anderen Thread-Gruppen zu verwenden. Dieses Verhalten lässt sich jedoch ändern. Gültige Werte für `<value>` sind: "none", der Standardwert, bei dem kein Versuch unternommen wird, ungenutzte Verbindungen aus anderen Thread-Gruppen zu verwenden; "restricted", bei dem nur dann eine ungenutzte Verbindung von einem anderen Thread angefordert wird, wenn Protokolle verwendet werden, die keine neuen Verbindungen aufbauen können, etwa Reverse HTTP, oder wenn strict-maxconn verwendet wird; und "full", bei dem immer auch in anderen Thread-Gruppen nach ungenutzten Verbindungen gesucht wird. Beachten Sie, dass Verbindungen aus anderen Thread-Gruppen Leistungseinbußen verursachen können und daher nur verwendet werden sollten, wenn dies wirklich erforderlich ist. Dieses Verhalten wird inzwischen durch tune.idle-pool.shared gesteuert. Dieses Schlüsselwort dient nur noch der Kompatibilität mit älteren Konfigurationen und wird künftig als veraltet eingestuft.

<a id="entry-3-2-tune-vars-global-max-size"></a>

**`tune.vars.global-max-size <size>`**

```haproxy
tune.vars.global-max-size <size>
tune.vars.proc-max-size <size>
tune.vars.reqres-max-size <size>
tune.vars.sess-max-size <size>
tune.vars.txn-max-size <size>
```

Diese fünf Einstellungen steuern die maximale Speichermenge, die das Variablensystem verwenden darf. "global" begrenzt den insgesamt für alle Gültigkeitsbereiche verfügbaren Speicher. "proc" begrenzt den Speicher für den Prozessbereich, "sess" für den Sitzungsbereich, "txn" für den Transaktionsbereich und "reqres" für die Verarbeitung jeder einzelnen Anfrage oder Antwort. Die Speicherabrechnung ist hierarchisch: Grenzen auf einer übergeordneten Ebene schließen die untergeordneten Ebenen ein. "proc" umfasst "sess", "sess" umfasst "txn" und "txn" umfasst "reqres".

Wenn beispielsweise "tune.vars.sess-max-size" auf 100 begrenzt ist, können auch "tune.vars.txn-max-size" und "tune.vars.reqres-max-size" den Wert 100 nicht überschreiten. Wird eine Variable "txn.var" angelegt, die 100 Bytes enthält, ist der gesamte verfügbare Platz verbraucht. Beachten Sie, dass eine Überschreitung der Grenzen zur Laufzeit keine Fehlermeldung auslöst, Werte aber abgeschnitten oder beschädigt werden können. Planen Sie deshalb den Platzbedarf für die Speicherung aller Variablen genau.

<a id="entry-3-2-tune-zlib-memlevel"></a>

**`tune.zlib.memlevel <number>`**

```haproxy
tune.zlib.memlevel <number>
```

Legt den Parameter memLevel bei der Initialisierung von zlib für jeden Stream fest. Er bestimmt, wie viel Speicher für den internen Kompressionszustand reserviert werden soll. Der Wert 1 verwendet am wenigsten Speicher, ist jedoch langsam und verschlechtert das Kompressionsverhältnis. Der Wert 9 verwendet für optimale Geschwindigkeit am meisten Speicher. Zulässig sind Werte zwischen 1 und 9. Der Standardwert ist 8.

<a id="entry-3-2-tune-zlib-windowsize"></a>

**`tune.zlib.windowsize <number>`**

```haproxy
tune.zlib.windowsize <number>
```

Legt die Fenstergröße (die Größe des Verlaufspuffers) als Parameter der zlib-Initialisierung für jeden Stream fest. Größere Werte verbessern die Kompression auf Kosten eines höheren Speicherverbrauchs. Zulässig sind Werte zwischen 8 und 15. Der Standardwert ist 15.

## 3.3. Fehlerbehebung {#section-3-3}

<a id="entry-3-3-anonkey"></a>

**`anonkey <key>`**

```haproxy
anonkey <key>
```

Legt den globalen Anonymisierungsschlüssel auf `<key>` fest. Dieser muss eine 32-Bit-Zahl zwischen 0 und 4294967295 sein. CLI-Befehle verwenden diesen Schlüssel standardmäßig, wenn der anonymisierte Modus aktiviert ist. Der Schlüssel kann auch zur Laufzeit mit dem CLI-Befehl "set anon global-key" gesetzt werden. Siehe auch das Kommandozeilenargument "-dC" im Verwaltungshandbuch.

<a id="entry-3-3-debug-counters"></a>

**`debug.counters { on | off }`**

```haproxy
debug.counters { on | off }
```

Aktiviert ('on') oder deaktiviert ('off') die Aktualisierung der Ereigniszähler im Code. Diese Zähler werden vom CLI-Befehl "debug counters" unter dem Typ "CNT" ausgegeben. Sie stehen nur zur Verfügung, wenn der Code mit DEBUG_COUNTERS auf einem Wert von mindestens 1 kompiliert wurde. Bei dem Wert 1 werden die Zähler standardmäßig nicht aktualisiert ("debug.counters off"), bei dem Wert 2 werden sie standardmäßig aktualisiert ("debug.counters on"). Normalerweise besteht kein Anlass, diese Einstellung zu ändern, sofern nicht ein Entwickler darum bittet oder der Verdacht besteht, dass sie ungewöhnlich viel CPU-Zeit beansprucht. Im letzteren Fall ist ein Bericht an die Entwickler mit einem Auszug der Zähler erforderlich. Der Zustand lässt sich auch zur Laufzeit mit dem CLI-Befehl "debug counters" ändern. Weitere Informationen finden Sie im Verwaltungshandbuch.

<a id="entry-3-3-force-cfg-parser-pause"></a>

**`force-cfg-parser-pause <timeout>`**

```haproxy
force-cfg-parser-pause <timeout>
```

Dieser Befehl hält den Konfigurationsparser für `<timeout>` Millisekunden an. Das ist bei der Entwicklung oder beim Testen von Zeitüberschreitungen in Init-Skripten hilfreich, insbesondere zur Simulation eines sehr langen Neuladens. Dafür muss expose-experimental-directives gesetzt sein.

`<timeout>` gibt die Wartezeit standardmäßig in Millisekunden an. Durch Anhängen einer Einheit an die Zahl kann jedoch auch jede andere Einheit verwendet werden, wie am Anfang dieses Dokuments erläutert.

Beispiel:

```text
global
    expose-experimental-directives
    force-cfg-parser-pause 10s
```

<a id="entry-3-3-quick-exit"></a>

**`quick-exit`**

```haproxy
quick-exit
```

Beschleunigt beim Neuladen das Beenden des alten Prozesses, indem die Freigabe von Speicherobjekten und Listenern übersprungen wird. Diese Ressourcen werden beim Beenden des Prozesses ohnehin vom Betriebssystem zurückgewonnen. Der Zeitgewinn ist nur gering und beträgt selbst bei sehr großen Konfigurationen höchstens einige hundert Millisekunden. Der eigentliche Haupteinsatzzweck besteht darin, einen gefundenen Fehler im deinit()-Code zu umgehen. Verwenden Sie diese Option möglichst nur auf Anweisung der Entwickler.

<a id="entry-3-3-quiet"></a>

**`quiet`**

```haproxy
quiet
```

Unterdrückt alle Meldungen während des Starts. Entspricht dem Kommandozeilenargument "-q".

<a id="entry-3-3-warn-blocked-traffic-after"></a>

**`warn-blocked-traffic-after <time>`**

```haproxy
warn-blocked-traffic-after <time>
```

Legt fest, nach welcher Verzögerung eine festhängende Task, die den Datenverkehr blockiert, eine Warnung auf der Standardfehlerausgabe auslöst. Die Verzögerung wird in Millisekunden angegeben und beträgt standardmäßig 100 ms. Zulässig sind Werte von einschließlich 1 ms bis einschließlich 1000 ms. Niedrigere Werte führen häufig, höhere Werte selten zu Warnungen. Der Watchdog beendet ohnehin eine außer Kontrolle geratene Task, die zweimal jeweils eine Sekunde lang nicht reagiert. Eine Warnverzögerung von 1000 ms löst daher normalerweise keine Warnung aus. Empfohlen werden Werte zwischen 10 und 100ms, um Konfigurationsfehler zu erkennen, die durch lange Antwortzeiten oder ruckelnde interaktive Sitzungen die Nutzung beeinträchtigen können. Solche Probleme können beispielsweise eine schlecht entworfene Lua-Sample-Fetch-Funktion mit aufwendigen Berechnungen oder eine sehr große map_reg- oder map_regm-Map-Datei mit hohen Auswertungskosten verursachen. Zum Vergleich: Ein TLS-Handshake kann zwischen einer und zwei Millisekunden beanspruchen, die Kompression eines 16kB großen HTTP-Antwortpuffers etwa eine Millisekunde. Die Ausgabe enthält einen Thread-Dump der verantwortlichen Task mit einem Backtrace und etwas Kontext, anhand dessen sich ermitteln lässt, wo die Zeit verbraucht wird.

<a id="entry-3-3-zero-warning"></a>

**`zero-warning`**

```haproxy
zero-warning
```

Wenn diese Option gesetzt ist, verweigert HAProxy den Start, sobald beim Verarbeiten und Anwenden der Konfiguration eine Warnung ausgegeben wurde. Warnungen über ungeeignete Parameterkombinationen, sehr hohe Grenzen, die nicht gesetzt werden konnten, und ähnliche Probleme führen dann dazu, dass sich der Prozess beim Start mit einem Fehler beendet. Einige spät beim Start auftretende Warnungen kann diese Option nicht erfassen, etwa wenn beim Ändern der Gruppen-ID im Modus "daemon" oder "master-worker" zusätzliche Gruppen nicht abgelegt werden können oder wenn der Prozess nach fork() nicht als dumpbar markiert werden kann. Die Option erfasst keine Warnungen, die zur Laufzeit ausgegeben werden. Für Konfigurationen, die selten geändert werden, wird diese Option nachdrücklich empfohlen: Sie hilft, subtile Fehler zu erkennen und die Konfiguration sauber und mit künftigen Versionen kompatibel zu halten. Beachten Sie, dass auch "haproxy -c" in diesem Fall Fehler meldet. Diese Option entspricht dem Kommandozeilenargument "-dW".

## 3.4. HTTPClient-Abstimmung {#section-3-4}

HTTPClient ist eine interne HTTP-Bibliothek, die von verschiedenen Subsystemen verwendet werden kann, beispielsweise in LUA-Skripten. HTTPClient wird nicht im Datenpfad eingesetzt und hat daher nichts mit dem HTTP-Datenverkehr zu tun, der HAProxy durchläuft.

<a id="entry-3-4-httpclient-resolvers-disabled"></a>

**`httpclient.resolvers.disabled <on|off>`**

```haproxy
httpclient.resolvers.disabled <on|off>
```

Deaktiviert die DNS-Auflösung des httpclient. Verhindert die Erstellung des resolvers-Abschnitts "default".

Der Standardwert ist off.

<a id="entry-3-4-httpclient-resolvers-id"></a>

**`httpclient.resolvers.id <resolvers id>`**

```haproxy
httpclient.resolvers.id <resolvers id>
```

Legt den resolvers-Abschnitt fest, mit dem der httpclient die Namensauflösung versucht.

Standardmäßig wird die resolvers-ID "default" verwendet. Wenn diese Option nicht gesetzt ist und der Abschnitt nicht gefunden wird, wird lediglich die Namensauflösung deaktiviert.

Wird diese Option hingegen ausdrücklich gesetzt, führt ein Fehler beim Laden zu einem Konfigurationsfehler.

<a id="entry-3-4-httpclient-resolvers-prefer"></a>

**`httpclient.resolvers.prefer <ipv4|ipv6>`**

```haproxy
httpclient.resolvers.prefer <ipv4|ipv6>
```

Mit dieser Option lässt sich die gewünschte IP-Adressfamilie für die Namensauflösung auswählen. Das ist nützlich, wenn IPv6 in Ihrem Netzwerk nicht verfügbar ist. Der Standardwert ist "ipv6".

<a id="entry-3-4-httpclient-retries"></a>

**`httpclient.retries <number>`**

```haproxy
httpclient.retries <number>
```

Legt fest, wie oft der httpclient eine fehlgeschlagene Anfrage erneut versucht. Die Wirkung entspricht der des Schlüsselworts "retries" in einem Backend.

Der Standardwert ist 3.

<a id="entry-3-4-httpclient-ssl-ca-file"></a>

**`httpclient.ssl.ca-file <cafile>`**

```haproxy
httpclient.ssl.ca-file <cafile>
```

Legt die ca-file fest, die zur Überprüfung des Serverzertifikats verwendet werden soll. Die Option akzeptiert dieselben Parameter wie die Option "ca-file" in einer server-Zeile.

Wenn diese Option nicht gesetzt ist, gilt standardmäßig der Wert "@system-ca", der versucht, die CA des Systems zu laden. Schlägt dies fehl, wird SSL für den httpclient deaktiviert.

Wird diese Option hingegen ausdrücklich gesetzt, führt ein Fehlschlag zu einem Konfigurationsfehler.

<a id="entry-3-4-httpclient-ssl-verify"></a>

**`httpclient.ssl.verify [none|required]`**

```haproxy
httpclient.ssl.verify [none|required]
```

Funktioniert wie die Option verify in server-Zeilen. Bei 'none' werden Serverzertifikate nicht überprüft. Der Standardwert ist "required".

Wenn diese Option nicht gesetzt ist, gilt standardmäßig der Wert "required". Schlägt dies fehl, wird SSL für den httpclient deaktiviert.

Wird diese Option hingegen ausdrücklich gesetzt, führt ein Fehlschlag zu einem Konfigurationsfehler.

<a id="entry-3-4-httpclient-timeout-connect"></a>

**`httpclient.timeout.connect <timeout>`**

```haproxy
httpclient.timeout.connect <timeout>
```

Legt die standardmäßige maximale Wartezeit für einen Verbindungsversuch des httpclient fest.

Argumente:

```text
<timeout> ist der Wert für die Zeitüberschreitung, standardmäßig in
          Millisekunden. Wird die Einheit an die Zahl angehängt, kann
          jedoch jede andere Einheit verwendet werden, wie am Anfang
          dieses Dokuments erläutert.
```

Der Standardwert ist 5000ms.
