---
title: "3. HAProxy starten"
linkTitle: "3. HAProxy starten"
weight: 270
description: "Befehlszeilensyntax, Optionen, Laden der Konfiguration und Startverhalten"
icon: fa-solid fa-play
module: [HAPROXY]
categories: [Aufgabe]
aliases:
  - /haproxy/management/starting/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 3"
---

HAProxy wird durch Aufruf des Programms "haproxy" mit mehreren Befehlszeilenargumenten gestartet. Die Syntax lautet:

```shell
$ haproxy [<options>]*
```

Dabei steht [`<options>`]\* für eine beliebige Anzahl von Optionen. Eine Option beginnt immer mit '-', gefolgt von einem oder mehreren Buchstaben und gegebenenfalls einem oder mehreren weiteren Argumenten. Ohne Optionen zeigt HAProxy die Hilfe mit einer Übersicht der unterstützten Optionen an. Die verfügbaren Optionen können je nach Betriebssystem leicht variieren. Viele davon entsprechen einer Einstellung im Abschnitt "global". In diesem Fall hat die Befehlszeile immer Vorrang vor der Konfigurationsdatei. So lassen sich Einstellungen schnell erzwingen, ohne Konfigurationsdateien zu ändern. Folgende Optionen sind derzeit verfügbar:

<a id="entry-3-entry"></a>

**`-- <cfgfile>*`**

```haproxy
-- <cfgfile>*
```

Alle Argumente nach "--" sind Pfade zu Konfigurationsdateien oder -verzeichnissen, die in der angegebenen Reihenfolge geladen und verarbeitet werden. Dies ist vor allem nützlich, wenn die Shell zahlreiche numerisch geordnete Dateien laden soll. Siehe auch "-f". Der Unterschied zwischen "--" und "-f" besteht darin, dass "-f" vor jedem Dateinamen stehen muss, während ein einzelnes "--" vor allen Dateinamen genügt. Beide Optionen können gemeinsam verwendet werden; die Reihenfolge in der Befehlszeile gilt weiterhin. Werden mehrere Dateien angegeben, muss jede Datei an einer Abschnittsgrenze beginnen. Ihr erstes Schlüsselwort muss also etwa "global", "defaults", "peers", "listen", "frontend" oder "backend" sein. Eine Datei kann beispielsweise nicht nur eine Serverliste enthalten.

<a id="entry-3-f"></a>

**`-f <cfgfile|cfgdir>`**

```haproxy
-f <cfgfile|cfgdir>
```

Fügt `<cfgfile>` zur Liste der zu ladenden Konfigurationsdateien hinzu. Ist `<cfgdir>` ein Verzeichnis, werden alle darin enthaltenen Dateien (und nur Dateien) in lexikalischer Reihenfolge mit LC_COLLATE=C hinzugefügt. Berücksichtigt werden ausschließlich nicht versteckte Dateien, deren Name also nicht mit "." beginnt, mit der Endung ".cfg". Konfigurationsdateien werden in der angegebenen Reihenfolge geladen und verarbeitet. Die Option kann mehrfach angegeben werden, um mehrere Dateien zu laden. Siehe auch "--". Der Unterschied zwischen "--" und "-f" besteht darin, dass "-f" vor jedem Dateinamen stehen muss, während ein einzelnes "--" vor allen Dateinamen genügt. Beide Optionen können gemeinsam verwendet werden; die Reihenfolge in der Befehlszeile gilt weiterhin. Werden mehrere Dateien angegeben, muss jede Datei an einer Abschnittsgrenze beginnen. Ihr erstes Schlüsselwort muss also etwa "global", "defaults", "peers", "listen", "frontend" oder "backend" sein. Eine Datei kann beispielsweise nicht nur eine Serverliste enthalten.

<a id="entry-3-c"></a>

**`-C <dir>`**

```haproxy
-C <dir>
```

Wechselt vor dem Laden der Konfigurationsdateien in das Verzeichnis `<dir>`. Dies ist bei relativen Pfaden nützlich. Vorsicht bei Platzhaltern nach "--": Diese werden bereits vor dem Start von haproxy durch die Shell ersetzt.

<a id="entry-3-d"></a>

**`-D`**

```haproxy
-D
```

Startet als Daemon. Nach dem Fork löst sich der Prozess vom aktuellen Terminal; Fehler werden dort dann nicht mehr ausgegeben. Die Option entspricht dem Schlüsselwort "daemon" im Abschnitt "global" der Konfiguration. Es wird empfohlen, sie in jedem Init-Skript grundsätzlich zu erzwingen, damit eine fehlerhafte Konfiguration den Systemstart nicht verhindert.

<a id="entry-3-l"></a>

**`-L <name>`**

```haproxy
-L <name>
```

Ändert den lokalen Peer-Namen, der standardmäßig dem lokalen Hostnamen entspricht, in `<name>`. Dies wird nur für die Peer-Replikation verwendet. In der Konfigurationsdatei kann der Peer-Name mit der Variablen \$HAPROXY_LOCALPEER referenziert werden.

<a id="entry-3-n"></a>

**`-N <limit>`**

```haproxy
-N <limit>
```

Setzt den Standardwert für maxconn je Proxy auf `<limit>` statt auf den eingebauten Standardwert (gewöhnlich 2000). Nur zur Fehleranalyse nützlich.

<a id="entry-3-v"></a>

**`-V`**

```haproxy
-V
```

Aktiviert den ausführlichen Ausgabemodus und deaktiviert damit den stillen Modus. Hebt die Wirkung von "-q" oder "quiet" auf.

<a id="entry-3-w"></a>

**`-W`**

```haproxy
-W
```

Master-Worker-Modus. Entspricht dem Schlüsselwort "master-worker" im Abschnitt "global" der Konfiguration. Dieser Modus startet einen Master, der die Worker überwacht. HAProxy lässt sich dann unmittelbar durch Senden von SIGUSR2 an den Master neu laden. Der Master-Worker-Modus ist sowohl mit dem Vordergrund- als auch mit dem Daemon-Modus kompatibel. Er wird für den Betrieb mit mehreren Prozessen und mit systemd empfohlen.

<a id="entry-3-ws"></a>

**`-Ws`**

```haproxy
-Ws
```

Master-Worker-Modus mit Unterstützung für systemd-Dienste vom Typ `notify`.

<a id="entry-3-4"></a>

**`-4`**

```haproxy
-4
```

Zwingt DNS-Resolver, ausschließlich IPv4-Adressen ("A"-Records) abzufragen und zu akzeptieren. Dies kann bei Schwierigkeiten in Umgebungen ohne durchgängige Dual-Stack-Konnektivität helfen. Die Option überschreibt die globale Direktive "dns-accept-family" und erzwingt dafür "ipv4".

<a id="entry-3-c-2"></a>

**`-c`**

```haproxy
-c
```

Prüft nur die Konfigurationsdateien und beendet sich, bevor versucht wird, Sockets zu binden. Der Exit-Status ist null, wenn alles OK ist, und ungleich null, wenn ein Fehler auftritt. Auf vorhandene Warnungen wird hingewiesen. Standardmäßig gibt diese Option keine Erfolgsmeldung aus. Zusammen mit "-V" wird bei Erfolg "Configuration file is valid" ausgegeben.

Skripte müssen den Exit-Status verwenden, um den Erfolg des Befehls festzustellen.

<a id="entry-3-cc"></a>

**`-cc`**

```haproxy
-cc
```

Wertet eine Bedingung aus, wie sie in einem bedingten Konfigurationsblock verwendet wird. Der Exit-Status ist null, wenn die Bedingung wahr ist, 1, wenn sie falsch ist, und 2, wenn ein Fehler auftritt.

<a id="entry-3-d-2"></a>

**`-d`**

```haproxy
-d
```

Aktiviert den Debug-Modus. Dieser deaktiviert den Daemon-Modus, hält den Prozess im Vordergrund und zeigt eingehende sowie ausgehende Ereignisse an. Er darf niemals in einem Init-Skript verwendet werden.

<a id="entry-3-entry-2"></a>

**`-dA[file]`**

```haproxy
-dA[file]
```

Schreibt unmittelbar nach dem vollständigen Laden der Konfiguration alle beim Start erkannten Abhängigkeiten als tar-Archiv in die angegebene Datei. Dies entspricht "set-dumpable libs", legt die Bibliotheken aber in einer Datei ab, statt sie im Speicher zu halten. Nach einem Core-Dump können damit alle nötigen Bibliotheken für Entwickler bereitgestellt werden, damit sie den Core-Dump auswerten können. Die Option ist möglicherweise nicht auf allen Betriebssystemen verfügbar. Es wird dringend empfohlen, sie mit den regulären Konfigurationsdateien zu verwenden. Bei manueller Verwendung kann zusätzlich "-c" angegeben werden, damit haproxy unmittelbar nach der Ausgabe beendet wird, ohne zu starten. Beispiel:

```shell
$ haproxy -dA/tmp/libs.tar -c -f /etc/haproxy/haproxy.cfg
```

<a id="entry-3-entry-3"></a>

**`-dC[key]`**

```haproxy
-dC[key]
```

Gibt die Konfigurationsdatei aus. Dies geschieht nach der Zerlegung der Zeilen in Tokens; Kommentare werden daher entfernt und die Einrückung vereinheitlicht. Wird ein Schlüssel ungleich null angegeben, werden Zeilen vor sensiblen oder vertraulichen Feldern abgeschnitten. Kennungen und Adressen werden mit diesem Schlüssel gehasht ausgegeben, nach demselben Algorithmus wie im anonymisierten Modus der CLI. Die Ausgabe kann somit sicher mit einem Entwickler geteilt werden, der sie zur Untersuchung eines mit demselben Schlüssel anonymisierten Dumps benötigt. Siehe auch den CLI-Befehl "set anon".

<a id="entry-3-dd"></a>

**`-dD`**

```haproxy
-dD
```

Aktiviert den Diagnosemodus. Dieser gibt zusätzliche Warnungen zu verdächtigen Konfigurationsanweisungen aus. Einige Ausgaben verhindern im Modus "zero-warning" den Start.

Solche Diagnosen sollen Menschen auf mögliche verborgene Probleme aufmerksam machen, die durchaus beabsichtigt sein können. Sie können sich auch innerhalb eines stabilen Zweigs und zwischen Rechnern mit exakt gleicher Konfiguration ändern. Daher *werden* sie regelmäßig gültige Anweisungen als verdächtig melden und sollten nur zusammen mit "-c" für eine eingehendere Diagnose verwendet werden. Ihre Ergebnisse dürfen niemals dazu verwendet werden, den Start eines Dienstes zu verhindern; dies geschieht bei Kombination mit "zero-warning" oder "-dW".

<a id="entry-3-df"></a>

**`-dF`**

```haproxy
-dF
```

Deaktiviert die schnelle Datenweiterleitung. Dieser Mechanismus optimiert die Weiterleitung, indem Daten direkt von einer Seite zur anderen gelangen, ohne den Stream aufzuwecken. Mit dieser Option lässt sich die Optimierung abschalten. Dabei wird auch jegliches TCP-Splicing im Kernel deaktiviert. Der Befehl ist nicht für den regulären Betrieb vorgesehen; Entwickler empfehlen ihn gewöhnlich nur bei komplexen Fehleranalysen.

<a id="entry-3-dg"></a>

**`-dG`**

```haproxy
-dG
```

Deaktiviert getaddrinfo() zur Auflösung von Hostnamen in Adressen. Dies kann helfen, wenn getaddrinfo() vermutlich nicht wie erwartet arbeitet. Die Option wurde eingeführt, weil auf verschiedenen Systemen zahlreiche fehlerhafte getaddrinfo()-Implementierungen existieren, die schwer zu untersuchende Auffälligkeiten verursachen.

<a id="entry-3-di"></a>

**`-dI`**

```haproxy
-dI
```

Aktiviert unsicheres Forken. Dies entspricht "insecure-fork-wanted" im globalen Abschnitt. Es kann nützlich sein, wenn alle Regressionstests mit ASAN ausgeführt werden, die addr2line per Fork starten müssen, um Adressen aufzulösen.

<a id="entry-3-entry-4"></a>

**`-dK<class[,class]*>`**

```haproxy
-dK<class[,class]*>
```

Gibt die Liste der registrierten Schlüsselwörter jeder Klasse aus. Die verfügbaren Klassen zeigt "-dKhelp". Mit "-dKall" lassen sich alle Klassen ausgeben; alternativ kann eine durch Kommas getrennte Auswahl der in der Hilfe genannten Klassen angegeben werden. Das Ausgabeformat hängt von der Schlüsselwortklasse ab: "cfg" zeigt bekannte Konfigurationsschlüsselwörter in einem der Konfigurationsdatei ähnlichen Format, während "smp" Sample-Abruffunktionen mit einer vorangestellten Kompatibilitätsmatrix für die jeweiligen Regelsätze ausgibt. Für Menschen ist diese Ausgabe selten unmittelbar brauchbar. Externe Werkzeuge können damit jedoch neue Schlüsselwörter an bestimmten Stellen erkennen, um Dokumentation, Syntaxhervorhebungsdateien, Konfigurationsparser, APIs usw. automatisch zu aktualisieren. Das Ausgabeformat kann sich im Laufe der Zeit etwas ändern. Es wird daher ausdrücklich empfohlen, damit hauptsächlich Unterschiede zu früheren Archiven zu erkennen. Nicht alle Schlüsselwörter sind aufgeführt: Viele gab es schon vor den verschiedenen Systemen zur Schlüsselwortregistrierung und erscheinen dort nicht. Da neue Schlüsselwörter aber ausschließlich über die modernen Mechanismen hinzugefügt werden, kann recht zuverlässig davon ausgegangen werden, dass sich Erweiterungen der Sprache mit dieser Ausgabe gut erkennen lassen. Die Schlüsselwörter werden erst nach vollständiger Auswertung der Konfiguration ausgegeben, sodass auch dynamisch erzeugte Schlüsselwörter erscheinen können. Um die Ausgabe zu erzeugen und anschließend zu beenden, eignet sich eine stille Konfigurationsprüfung mit einer vorhandenen Konfiguration:

```text
./haproxy -dKall -q -c -f foo.cfg
```

Ist keine Konfigurationsdatei verfügbar, lassen sich mit "-f /dev/null" ebenfalls alle Standardschlüsselwörter ausgeben. Da dann kein Listener vorhanden ist, ist der Rückgabestatus jedoch ungleich null und muss ignoriert werden.

<a id="entry-3-dl"></a>

**`-dL`**

```haproxy
-dL
```

Gibt die Liste der dynamisch eingebundenen Bibliotheken aus, die am Ende der Konfigurationsverarbeitung geladen sind. Sie enthält gewöhnlich auch indirekte Abhängigkeiten, etwa aus Lua-Code geladene Bibliotheken, sowie die ausführbare Datei selbst. Das Ausgabeformat lässt sich ausreichend einfach bereinigen, um daraus unmittelbar ein tar-Archiv aller Abhängigkeiten zu erstellen. Da die Option den Programmstart nicht beendet, wird empfohlen, sie nur zusammen mit "-c" und "-q" zu verwenden. Dann erscheint ausschließlich die Liste der geladenen Objekte, bei einem Fehler nichts. Wenn ein solches Paket zur Analyse einer Core-Datei bereitgestellt wird, ist außerdem zu beachten, dass die meisten Bibliotheken symbolische Links sind. Beim Erstellen des Archivs muss deren Zielinhalt aufgenommen werden:

```text
./haproxy -W -q -c -dL -f foo.cfg | tar -T - -hzcf archive.tgz
```

Beim Start im ausführlichen Modus (-V) werden zusätzlich die Adressbereiche der dynamisch eingebundenen Bibliotheken aufgelistet, sofern nicht der stille Modus (-q) verwendet wird.

<a id="entry-3-entry-5"></a>

**`-dM[<byte>[,]][help|options,...]`**

```haproxy
-dM[<byte>[,]][help|options,...]
```

Erzwingt das Füllen von Speicher mit einem Prüfmuster und/oder ändert weitere Optionen zur Speicherfehleranalyse. Dabei wird jeder mit malloc() oder pool_alloc() reservierte Speicherbereich mit `<byte>` gefüllt, bevor er an den Aufrufer zurückgegeben wird. Ohne Angabe von `<byte>` gilt der Standardwert 0x50 ('P'). Dies verlangsamt den Betrieb etwas, hilft aber dabei, Fehler durch fehlende Initialisierung im Code zuverlässig auszulösen, die sonst zufällige Abstürze verursachen. -dM0 macht dabei aus jedem malloc() faktisch ein calloc(). Wenn ein Fehler mit dieser Option auftritt oder verschwindet, liegt in jedem Fall ein Fehler in haproxy vor; bitte melden Sie ihn. Weitere Optionen können allein oder nach einem Komma hinter dem Byte-Wert angegeben werden. Die besondere Option "help" listet die derzeit unterstützten Optionen und ihre aktuellen Werte auf. Jede Debug-Option kann ausdrücklich ein- oder ausgeschaltet werden. Die günstigsten Einstellungen werden gewöhnlich bereits beim Build abhängig vom Betriebssystem gewählt und brauchen nicht angepasst zu werden, sofern kein Entwickler dies empfiehlt. Unterstützt werden folgende Debug-Optionen (ein/aus):

- fail / no-fail:

```text
Aktiviert zusammen mit der globalen Einstellung "tune.fail-alloc"
zufällig fehlschlagende Speicherreservierungen. Damit werden fehlende
Fehlerprüfungen im Code erkannt. Das Aktivieren setzt den Anteil
fehlgeschlagener Reservierungen auf 1% vor.
```

- no-merge / merge:

```text
Standardmäßig werden Pools sehr ähnlicher Größe zusammengelegt.
Dies erhöht die Effizienz, erschwert aber die Analyse bestimmter
Speicherabbilder. Diese Option deaktiviert den Mechanismus und kann
den Speicherverbrauch geringfügig erhöhen.
```

- cold-first / hot-first:

```text
Um die CPU-Cache-Trefferrate zu optimieren, werden standardmäßig die
zuletzt freigegebenen, also „heißen“ Objekte für neue Reservierungen
wiederverwendet. Dies erschwert jedoch die Analyse von Speicherabbildern
und kann Zugriffe auf bereits freigegebenen Speicher verdecken. Mit
dieser Option werden stattdessen zuerst die „kältesten“ Objekte gewählt,
was die CPU-Auslastung leicht erhöhen kann.
```

- integrity / no-integrity:

```text
Aktiviert Integritätsprüfungen für den reservierten Speicherbereich,
um festzustellen, ob er seit seiner letzten Freigabe verändert wurde.
Dies funktioniert am besten mit "no-merge", "cold-first" und "tag".
Das Aktivieren erhöht die CPU-Auslastung geringfügig.
```

- backup / no-backup:

```text
Kopiert jedes freigegebene Objekt bei der Freigabe, damit Entwickler
es untersuchen können. Bei der Reservierung wird außerdem verglichen,
ob sich zwischenzeitlich etwas geändert hat, was auf einen Zugriff
nach der Freigabe hinweist. Dies verdoppelt den Speicherverbrauch und
erhöht die CPU-Auslastung geringfügig, ähnlich wie "integrity". In
Kombination mit "integrity" wird der Inhalt weiterhin kopiert, aber
kein Vergleich durchgeführt, da "integrity" diesen übernimmt. Wie
"integrity" funktioniert dies am besten mit "no-merge", "cold-first"
und "tag".
```

- no-global / global:

```text
Je nach Betriebssystem kann ein prozessweiter globaler Speichercache
aktiviert sein, wenn der Standardallokator als zu langsam oder im
Thread-Betrieb als ineffizient eingeschätzt wird. Diese Option erzwingt
seine Deaktivierung oder Aktivierung. Das Deaktivieren kann bei
ineffizienten Allokatoren die CPU-Auslastung erhöhen. Das Aktivieren
kann bei effizienten Allokatoren den Speicherverbrauch erhöhen.
```

- no-cache / cache:

```text
Jeder Thread verwendet für Reservierungen einen sehr schnellen lokalen
Objektcache, der standardmäßig immer aktiviert ist. Diese Option
deaktiviert ihn. Da auch der globale Cache über die lokalen Caches
arbeitet, werden damit effektiv sämtliche Caches deaktiviert und
Reservierungen direkt über den Standardallokator vorgenommen. Dies kann
die CPU-Auslastung deutlich erhöhen, auf sehr kleinen Systemen aber auch
etwas Speicher einsparen.
```

- caller / no-caller:

```text
Reserviert in jedem zugewiesenen Objekt zusätzlichen Platz für die
Adresse des letzten Aufrufers, der es reserviert oder freigegeben hat.
Dies hilft Entwicklern bei der Analyse von Speicherabbildern, frühere
Abläufe nachzuvollziehen und die Ursache unerwarteter Vorgänge zu vermuten.
```

- tag / no-tag:

```text
Reserviert in jedem zugewiesenen Objekt zusätzlichen Platz für eine
Markierung, mit der sich Fehler wie doppelte Freigaben, das Freigeben
ungültiger Objekte und Pufferüberläufe erkennen lassen. Gegen einen
Mehrbedarf von 4 oder 8 Bytes je Reservierung bietet dies wesentlich
stärkere Zuverlässigkeitsgarantien. Gewöhnlich ist dies der erste
Schritt zur Erkennung von Speicherbeschädigungen.
```

- poison / no-poison:

```text
Füllt reservierte Objekte mit einem festen Muster. Dadurch sind
zufällige Werte wie 0 nicht vorhanden, wenn ein neu hinzugefügtes Feld
versehentlich in einer Initialisierungsroutine vergessen wurde. Solche
Fehler lassen sich meist nur selten reproduzieren, insbesondere wenn
Pools nicht zusammengelegt werden. Normalerweise wird dies aktiviert,
indem der Byte-Wert direkt an -dM übergeben wird. Diese Option erlaubt
es dagegen, die Verwendung eines zuvor gesetzten Werts zu deaktivieren
oder zu aktivieren.
```

<a id="entry-3-dr"></a>

**`-dR`**

```haproxy
-dR
```

Deaktiviert die Socket-Option SO_REUSEPORT für lauschende Ports. Dies entspricht dem Schlüsselwort "noreuseport" im Abschnitt "global". Die Option kann beim Betrieb mit mehreren Threads eingesetzt werden, wenn sich Probleme mit der Lastverteilung zwischen den haproxy-Threads zeigen; diese lassen sich mit top beobachten.

<a id="entry-3-ds"></a>

**`-dS`**

```haproxy
-dS
```

Deaktiviert den Systemaufruf splice(). Dies entspricht dem Schlüsselwort "nosplice" im Abschnitt "global". Die Option kann helfen, wenn splice() vermutlich fehlerhaft arbeitet oder Leistungsprobleme verursacht, oder wenn die weitergeleiteten Daten mit strace sichtbar gemacht werden sollen. Bei Verwendung von splice() erscheinen sie dort nicht.

<a id="entry-3-dt"></a>

**`-dT`**

```haproxy
-dT
```

Deaktiviert ktls. Dies entspricht dem Schlüsselwort "noktls" im Abschnitt "global". Die Option ist hauptsächlich bei einem vermuteten Fehler im Zusammenhang mit ktls nützlich.

<a id="entry-3-dv"></a>

**`-dV`**

```haproxy
-dV
```

Deaktiviert die serverseitige SSL-Prüfung. Dies entspricht "ssl-server-verify none" im Abschnitt "global". Die Option ist nützlich, um Probleme aus dem Produktivbetrieb außerhalb der Produktivumgebung nachzustellen. Niemals in einem Init-Skript verwenden, da sie die Sicherheit der SSL-Verbindungen zu den Servern verringert.

<a id="entry-3-dw"></a>

**`-dW`**

```haproxy
-dW
```

Mit dieser Option verweigert haproxy den Start, sobald bei der Verarbeitung der Konfiguration eine Warnung ausgegeben wurde. Dies hilft, subtile Fehler zu erkennen und die Konfiguration sauber und über Versionsgrenzen hinweg portabel zu halten. Bei manuell verwalteten Konfigurationen wird die Option in Dienstskripten empfohlen. Bei generierten Konfigurationen, die häufig mehr Warnungen erzeugen, wird dagegen von ihr abgeraten. Zusammen mit "-c" führen Warnungen bei der Konfigurationsprüfung zu einem Fehlschlag. Dies entspricht der globalen Option "zero-warning".

<a id="entry-3-dz"></a>

**`-dZ`**

```haproxy
-dZ
```

Deaktiviert die Datenweiterleitung im Modus "zero-copy". Dies entspricht dem Schlüsselwort "tune.disable-zero-copy-forwarding" im Abschnitt "global". Die Option kann bei Datenverlust oder Problemen mit der Datenintegrität helfen oder dann, wenn die weitergeleiteten Daten mit strace sichtbar gemacht werden sollen, da sie auch jegliches TCP-Splicing im Kernel deaktiviert.

<a id="entry-3-db"></a>

**`-db`**

```haproxy
-db
```

Deaktiviert den Hintergrund- und Mehrprozessmodus. Der Prozess bleibt im Vordergrund. Dies wird hauptsächlich bei der Entwicklung oder kleinen Tests verwendet, da Ctrl-C zum Beenden des Prozesses genügt. Niemals in einem Init-Skript verwenden.

<a id="entry-3-dc"></a>

**`-dc`**

```haproxy
-dc
```

Aktiviert die Fehleranalyse für die CPU-Affinität. Vor dem Start werden die ausgewählten und ausgeschlossenen CPUs sowie deren Topologie ausgegeben.

<a id="entry-3-de"></a>

**`-de`**

```haproxy
-de
```

Deaktiviert den Poller "epoll". Dies entspricht dem Schlüsselwort "noepoll" im Abschnitt "global". Die Option ist hauptsächlich bei einem vermuteten Fehler dieses Pollers nützlich. Auf Systemen mit epoll-Unterstützung wird gewöhnlich auf den Poller "poll" zurückgegriffen.

<a id="entry-3-dk"></a>

**`-dk`**

```haproxy
-dk
```

Deaktiviert den Poller "kqueue". Dies entspricht dem Schlüsselwort "nokqueue" im Abschnitt "global". Die Option ist hauptsächlich bei einem vermuteten Fehler dieses Pollers nützlich. Auf Systemen mit kqueue-Unterstützung wird gewöhnlich auf den Poller "poll" zurückgegriffen.

<a id="entry-3-dp"></a>

**`-dp`**

```haproxy
-dp
```

Deaktiviert den Poller "poll". Dies entspricht dem Schlüsselwort "nopoll" im Abschnitt "global". Die Option ist hauptsächlich bei einem vermuteten Fehler dieses Pollers nützlich. Auf Systemen mit poll-Unterstützung wird gewöhnlich auf den Poller "select" zurückgegriffen. Dieser lässt sich nicht deaktivieren und ist auf 1024 Dateideskriptoren begrenzt.

<a id="entry-3-dr-2"></a>

**`-dr`**

```haproxy
-dr
```

Ignoriert Fehler bei der Auflösung von Serveradressen. Beim Prüfen einer Konfiguration außerhalb der Produktivumgebung fehlen sehr häufig dieselben Resolver, sodass die Auflösung von Serveradressen fehlschlägt. Dies erschwert Konfigurationstests. Die Option hängt für alle Server die Methode "none" an die Liste der Adressauflösungsmethoden an. So wird der Start auch dann nicht unterbrochen, wenn libc eine Adresse nicht auflösen kann.

<a id="entry-3-dt-2"></a>

**`-dt [<trace_desc>,...]`**

```haproxy
-dt [<trace_desc>,...]
```

Aktiviert Traces auf stderr. Ohne Argument werden alle Trace-Quellen auf der Stufe error aktiviert. Damit lassen sich insbesondere Protokollverstöße von Clients oder Servern erkennen. Ein optionales Argument kann eine durch ',' getrennte Liste verschiedener Trace-Konfigurationen enthalten. Jedes Element aktiviert eine oder alle Trace-Quellen. Zusätzlich können je Element Stufe und Ausführlichkeit angegeben werden, getrennt vom Trace-Namen und voneinander durch ':'. Wird ein ungültiger Name für Ausführlichkeit oder Stufe eingegeben, erscheint die Liste der verfügbaren Schlüsselwörter. Beispielsweise kann für jedes Feld zunächst 'help' angegeben werden, um diese Liste einzusehen.

<a id="entry-3-dv-2"></a>

**`-dv`**

```haproxy
-dv
```

Deaktiviert den Poller "evports". Dies entspricht dem Schlüsselwort "noevports" im Abschnitt "global". Die Option ist hauptsächlich bei einem vermuteten Fehler dieses Pollers nützlich. Auf Systemen mit Event-Ports (von Solaris 10 und neuer abgeleitetes SunOS) wird gewöhnlich auf den Poller "poll" zurückgegriffen.

<a id="entry-3-m"></a>

**`-m <limit>`**

```haproxy
-m <limit>
```

Begrenzt den für Prozessdaten reservierbaren Speicher auf `<limit>` Megabyte. Je nach Speicherbedarf im Normalbetrieb können dadurch Verbindungen abgewiesen werden oder Verzögerungen entstehen. Die Option dient hauptsächlich dazu, den haproxy-Prozess unter begrenztem Ressourcenverbrauch zu betreiben. Der Speicher wird nicht zwischen haproxy-Prozessen geteilt. Ein mit fork() erzeugter Kindprozess erbt die Ressourcengrenzen seines Elternprozesses. Im Master-Worker-Modus gilt diese Speichergrenze daher jeweils getrennt für den Master und den von ihm geforkten Worker-Prozess.

<a id="entry-3-n-2"></a>

**`-n <limit>`**

```haproxy
-n <limit>
```

Setzt die Verbindungsgrenze je Prozess auf `<limit>`. Dies entspricht dem Schlüsselwort "maxconn" im globalen Abschnitt, hat aber Vorrang davor. Damit lässt sich schnell eine niedrigere Grenze erzwingen, um einen Dienstausfall auf Systemen mit zu niedrigen Ressourcengrenzen zu vermeiden.

<a id="entry-3-p"></a>

**`-p <file>`**

```haproxy
-p <file>
```

Schreibt beim Start die PIDs aller Prozesse in `<file>`. Dies entspricht dem Schlüsselwort "pidfile" im Abschnitt "global". Die Datei wird vor dem Eintritt in die chroot-Umgebung und nach dem durch "-C" ausgelösten chdir() geöffnet. Jede PID steht in einer eigenen Zeile.

<a id="entry-3-q"></a>

**`-q`**

```haproxy
-q
```

Aktiviert den Modus "quiet", der die Ausgabe von Meldungen unterdrückt. Zusammen mit "-c" kann damit lediglich geprüft werden, ob eine Konfigurationsdatei gültig ist.

<a id="entry-3-s"></a>

**`-S <bind>[,bind_options...]`**

```haproxy
-S <bind>[,bind_options...]
```

Bindet im Master-Worker-Modus eine Master-CLI, über die auf alle Prozesse zugegriffen werden kann, sowohl auf laufende als auch auf auslaufende. Aus Sicherheitsgründen wird empfohlen, die Master-CLI an einen lokalen UNIX-Socket zu binden. Die Bind-Optionen entsprechen denen des Schlüsselworts "bind" in der Konfigurationsdatei; die Wörter werden dabei durch Kommas statt durch Leerzeichen getrennt.

Dieser Socket kann bei einem unterbrechungsfreien Neuladen nicht dazu verwendet werden, die lauschenden Sockets eines alten Prozesses zu übernehmen.

<a id="entry-3-sf"></a>

**`-sf <pid>*`**

```haproxy
-sf <pid>*
```

Sendet nach abgeschlossenem Start das Signal "finish" (SIGUSR1) an ältere Prozesse, damit sie ihre laufenden Arbeiten abschließen und sich beenden. `<pid>` ist eine Liste der zu benachrichtigenden PIDs, eine je Argument. Die Liste endet mit jeder Option, die mit "-" beginnt. Eine leere PID-Liste ist zulässig. Sie kann daher während der Ausführung aus dem Ergebnis eines Befehls wie "pidof" oder "pgrep" erzeugt werden.

<a id="entry-3-st"></a>

**`-st <pid>*`**

```haproxy
-st <pid>*
```

Sendet nach abgeschlossenem Start das Signal "terminate" (SIGTERM) an ältere Prozesse, um sie sofort zu beenden, ohne ihre laufenden Arbeiten abzuschließen. `<pid>` ist eine Liste der zu benachrichtigenden PIDs, eine je Argument. Die Liste endet mit jeder Option, die mit "-" beginnt. Eine leere PID-Liste ist zulässig. Sie kann daher während der Ausführung aus dem Ergebnis eines Befehls wie "pidof" oder "pgrep" erzeugt werden.

<a id="entry-3-v-2"></a>

**`-v`**

```haproxy
-v
```

Gibt Version und Build-Datum aus.

<a id="entry-3-vv"></a>

**`-vv`**

```haproxy
-vv
```

Zeigt Version, Build-Optionen, Bibliotheksversionen und verwendbare Poller an. Diese Ausgabe wird bei Fehlermeldungen grundsätzlich angefordert.

<a id="entry-3-x"></a>

**`-x <unix_socket>`**

```haproxy
-x <unix_socket>
```

Verbindet sich mit dem angegebenen Socket und versucht, die lauschenden Sockets des alten Prozesses zu übernehmen und zu verwenden, statt neue zu binden. Unter Linux hilft dies, beim Neuladen der Konfiguration keine neue Verbindung zu verpassen.

Ohne Master-Worker-Modus muss diese Fähigkeit in der Konfiguration mit "expose-fd listeners" für den Statistik-Socket aktiviert werden.

Im Master-Worker-Modus ist "expose-fd listeners" nicht nötig. Beim Neuladen verwendet der Master diese Option automatisch mit der Syntax "sockpair@". Damit verbindet er sich direkt mit einem Worker, ohne einen in der Konfiguration deklarierten Statistik-Socket zu nutzen. Zum Deaktivieren kann -x /dev/null übergeben werden.

Eine sichere Methode zum Starten von HAProxy aus einer Init-Datei besteht darin, den Daemon-Modus zu erzwingen, vorhandene PIDs in einer PID-Datei abzulegen und ältere Prozesse anhand dieser Datei zum Abschließen ihrer Arbeit und anschließenden Beenden aufzufordern:

```text
haproxy -f /etc/haproxy.cfg \
        -D -p /var/run/haproxy.pid -sf $(cat /var/run/haproxy.pid)
```

Ist die Konfiguration auf wenige bestimmte Dateien aufgeteilt, etwa getrennt nach tcp und http, wird die Option "-f" empfohlen:

```text
haproxy -f /etc/haproxy/global.cfg -f /etc/haproxy/stats.cfg \
        -f /etc/haproxy/default-tcp.cfg -f /etc/haproxy/tcp.cfg \
        -f /etc/haproxy/default-http.cfg -f /etc/haproxy/http.cfg \
        -D -p /var/run/haproxy.pid -sf $(cat /var/run/haproxy.pid)
```

Ist die Zahl der Dateien unbekannt, etwa bei kundenspezifischen Dateien, wird empfohlen, ihre Namen mit einer Folgenummer fester Breite zu beginnen und sie mit "--" zu laden, gegebenenfalls nach dem Laden von Standardeinstellungen:

```text
haproxy -f /etc/haproxy/global.cfg -f /etc/haproxy/stats.cfg \
        -f /etc/haproxy/default-tcp.cfg -f /etc/haproxy/tcp.cfg \
        -f /etc/haproxy/default-http.cfg -f /etc/haproxy/http.cfg \
        -D -p /var/run/haproxy.pid -sf $(cat /var/run/haproxy.pid) \
        -f /etc/haproxy/default-customers.cfg -- /etc/haproxy/customers/*
```

Gelegentlich schlägt der Start aus irgendeinem Grund fehl. Dann sollte geprüft werden, ob die aufgerufene HAProxy-Version der erwarteten entspricht und die benötigten Funktionen wie SSL, PCRE, Komprimierung oder Lua unterstützt. Dies lässt sich mit "haproxy -vv" prüfen. Die Ausgabe enthält wichtige Angaben wie bestimmte Build-Optionen, das Zielsystem und die Versionen der verwendeten Bibliotheken. Sie wird auch bei Fehlermeldungen grundsätzlich angefordert:

```shell
$ haproxy -vv
```

HAProxy version 1.6-dev7-a088d3-4 2015/10/08 Copyright 2000-2015 Willy Tarreau <willy@haproxy.org>

Build options:

```text
TARGET  = linux2628
CPU     = generic
CC      = gcc
CFLAGS  = -pg -O0 -g -fno-strict-aliasing -Wdeclaration-after-statement \
          -DBUFSIZE=8030 -DMAXREWRITE=1030 -DSO_MARK=36 -DTCP_REPAIR=19
OPTIONS = USE_ZLIB=1 USE_DLMALLOC=1 USE_OPENSSL=1 USE_LUA=1 USE_PCRE=1
```

Default settings:

```text
maxconn = 2000, bufsize = 8030, maxrewrite = 1030, maxpollevents = 200
```

Encrypted password support via crypt(3): yes Built with zlib version: 1.2.6 Compression algorithms
supported: identity("identity"), deflate("deflate"), &#92;
raw-deflate("deflate"), gzip("gzip") Built with OpenSSL version: OpenSSL 1.0.1o 12 Jun 2015 Running
on OpenSSL version: OpenSSL 1.0.1o 12 Jun 2015 OpenSSL library supports TLS extensions: yes OpenSSL
library supports SNI: yes OpenSSL library supports prefer-server-ciphers: yes Built with PCRE
version: 8.12 2011-01-15 PCRE library supports JIT: no (USE_PCRE_JIT not set) Built with Lua
version: Lua 5.3.1 Built with transparent proxy support using: IP_TRANSPARENT IP_FREEBIND

Available polling systems:

```text
 epoll: pref=300,  test result OK
  poll: pref=200,  test result OK
select: pref=150,  test result OK
```

Total: 3 (3 usable), will use epoll.

Auch ohne Entwicklerkenntnisse lassen sich hier folgende wichtige Angaben prüfen:
<a id="entry-3-the-version"></a>

**`- die Version`**

```haproxy
- die Version
```

1.6-dev7-a088d3-4 bedeutet im obigen Beispiel, dass der Code auf Commit-ID "a088d3" steht, dem 4. Commit nach der offiziellen Version "1.6-dev7". Version 1.6-dev7 würde als "1.6-dev7-8c1ad7" erscheinen. Entscheidend ist hier "1.6-dev7": die 7. Entwicklungsversion der späteren Version 1.6. Eine Entwicklungsversion eignet sich nicht für den Produktivbetrieb, außer wenn genau bekannt ist, was man tut. Eine stabile Version wird mit 3 Zahlen angezeigt, etwa "1.5.14-16f863". Dies bezeichnet den 14. Korrekturstand zu Version 1.5 und ist eine für den Produktivbetrieb geeignete Version.

<a id="entry-3-the-release-date"></a>

**`- das Veröffentlichungsdatum`**

```haproxy
- das Veröffentlichungsdatum
```

2015/10/08. Das Datum folgt dem universellen Format Jahr/Monat/Tag. Hier bedeutet dies den 8. Oktober 2015. Stabile Versionen erscheinen alle paar Monate, anfangs alle 1-2 Monate und bei sehr ausgereiften Produkten mitunter erst nach 6 Monaten. Ein altes Datum deutet daher darauf hin, dass wahrscheinlich mehrere inzwischen behobene Fehler oder Sicherheitsprobleme vorliegen. Ein Blick auf die offizielle Website kann sich deshalb lohnen.

<a id="entry-3-build-options"></a>

**`- Build-Optionen`**

```haproxy
- Build-Optionen
```

Sie sind für Anwender relevant, die ihre Pakete selbst bauen, und können unerwartetes Verhalten erklären. Die obige Entwicklungsversion wurde beispielsweise für Linux 2.6.28 oder neuer und eine generische CPU ohne CPU-spezifische Optimierungen erstellt. Außerdem fehlt jede Codeoptimierung (-O0), sodass die Leistung schlecht ausfallen wird.

<a id="entry-3-libraries-versions"></a>

**`- Bibliotheksversionen`**

```haproxy
- Bibliotheksversionen
```

Die zlib-Version wird aus der Bibliothek selbst ermittelt. zlib gilt allgemein als sehr stabil und benötigt fast nie ein Upgrade. OpenSSL meldet zwei Versionen: die beim Build verwendete und die aktuell im System verwendete. Diese können sich im letzten Buchstaben, niemals aber in den Zahlen unterscheiden. Auch das Build-Datum wird ausgegeben, da die meisten OpenSSL-Fehler Sicherheitsprobleme darstellen und ernst genommen werden müssen. Diese Bibliothek muss daher unbedingt aktuell gehalten werden. Eine 4 Monate alte Version ist hier höchst verdächtig; offenbar wurde ein Update versäumt. PCRE bietet sehr schnelle reguläre Ausdrücke und wird dringend empfohlen. Manche Erweiterungen wie JIT sind nicht in allen Versionen vorhanden und noch jung, weshalb einige Anwender beim Build darauf verzichten. Deshalb wird auch dieser Build-Status ausgegeben. Bei der Skriptsprache Lua erwartet HAProxy Version 5.3, die noch sehr jung ist, da sie kurz vor HAProxy 1.6 veröffentlicht wurde. Es ist wichtig, auf der Lua-Website nach Korrekturen für diesen Zweig zu sehen.

<a id="entry-3-available-polling-systems"></a>

**`- Die verfügbaren Abfragesysteme beeinflussen die Skalierbarkeit des Prozesses, wenn`**

```haproxy
- Die verfügbaren Abfragesysteme beeinflussen die Skalierbarkeit des Prozesses, wenn
```

mehr als etwa tausend gleichzeitige Verbindungen verarbeitet werden. Sie stehen nur bereit, wenn beim Build das richtige System in der Variablen TARGET angegeben wurde. Unter Linux wird der Mechanismus "epoll" dringend empfohlen, unter BSD kqueue. Fehlen diese, wird poll() oder sogar select() verwendet, was bei vielen Verbindungen zu hoher CPU-Auslastung führt.
