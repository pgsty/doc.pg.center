---
title: "12. Fehlerdiagnose und Leistungsprobleme"
linkTitle: "12. Fehlerdiagnose"
weight: 360
description: "Untersuchung von Abstürzen, Stillständen, Latenz- und Durchsatzproblemen"
icon: fa-solid fa-bug
module: [HAPROXY]
categories: [Aufgabe]
aliases:
  - /haproxy/management/debugging-and-performance/
  - /docs/haproxy/management/debugging-and-performance/
  - /haproxy/debugging-and-performance/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 12"
---

Mit der Option "-d" bleibt HAProxy im Vordergrund und gibt für jedes Ereignis eine Zeile aus, etwa für eine eingehende oder beendete Verbindung sowie für jede erkannte Headerzeile einer Anfrage oder Antwort. Diese Diagnoseausgabe entsteht vor der Verarbeitung des Inhalts und berücksichtigt deshalb keine lokalen Änderungen. Sie dient hauptsächlich dazu, Anfragen und Antworten ohne Netzwerkmitschnitt anzuzeigen. Bei mehreren parallelen Verbindungen ist die Ausgabe schwerer lesbar. Die Skripte "debug2ansi" und "debug2html" im Verzeichnis examples/ helfen dann durch farbliche Hervorhebung.

Lehnt HAProxy eine HTTP/1.x-Anfrage oder -Antwort als fehlerhaft ab, sollte über die CLI der Befehl "show errors" ausgeführt werden. Er zeigt für jedes Frontend und Backend die zuletzt erfasste fehlerhafte HTTP/1.x-Anfrage und -Antwort mit allen Angaben, die das erste abgelehnte Zeichen des Eingabestroms genau bestimmen. Dies kann nötig sein, um Kunden oder Entwicklern einen Fehler in ihrem Code nachzuweisen. Häufig lassen sich die Prüfungen mit "option accept-unsafe-violations-in-http-request" beziehungsweise für Serverantworten mit "option accept-unsafe-violations-in-http-response" lockern, während die Erfassung erhalten bleibt. Weitere Einzelheiten stehen im Konfigurationshandbuch.

Beispiel:

```shell
> show errors
Total events captured on [13/Oct/2015:13:43:47.169]: 1

[13/Oct/2015:13:43:40.918] frontend HAProxyLocalStats (#2): invalid request
  backend <NONE> (#-1), server <NONE> (#-1), event #0
  src 127.0.0.1:51981, session #0, session flags 0x00000080
  HTTP msg state 26, msg flags 0x00000000, tx flags 0x00000000
  HTTP chunk len 0 bytes, HTTP body len 0 bytes
  buffer flags 0x00808002, out 0 bytes, total 31 bytes
  pending 31 bytes, wrapping at 8040, error at position 13:

  00000  GET /invalid request HTTP/1.1\r\n

```

Die CLI-Ausgabe von "show info" enthält hilfreiche Informationen über die bisher höchste Verbindungsrate, die höchste SSL-Schlüsselrate und allgemein Daten, mit denen sich vorübergehende Probleme bei CPU- oder Speichernutzung erklären lassen. Beispiel:

```shell
> show info
Name: HAProxy
Version: 1.6-dev7-e32d18-17
Release_date: 2015/10/12
Nbproc: 1
Process_num: 1
Pid: 7949
Uptime: 0d 0h02m39s
Uptime_sec: 159
Memmax_MB: 0
Ulimit-n: 120032
Maxsock: 120032
Maxconn: 60000
Hard_maxconn: 60000
CurrConns: 0
CumConns: 3
CumReq: 3
MaxSslConns: 0
CurrSslConns: 0
CumSslConns: 0
Maxpipes: 0
PipesUsed: 0
PipesFree: 0
ConnRate: 0
ConnRateLimit: 0
MaxConnRate: 1
SessRate: 0
SessRateLimit: 0
MaxSessRate: 1
SslRate: 0
SslRateLimit: 0
MaxSslRate: 0
SslFrontendKeyRate: 0
SslFrontendMaxKeyRate: 0
SslFrontendSessionReuse_pct: 0
SslBackendKeyRate: 0
SslBackendMaxKeyRate: 0
SslCacheLookups: 0
SslCacheMisses: 0
CompressBpsIn: 0
CompressBpsOut: 0
CompressBpsRateLim: 0
ZlibMemUsage: 0
MaxZlibMemUsage: 0
Tasks: 5
Run_queue: 1
Idle_pct: 100
node: wtap
description:
```

Tritt ein Problem mit einer neuen HAProxy-Version scheinbar zufällig auf, etwa der Abbruch jeder zweiten Anfrage oder gelegentliche Abstürze, kann eine gezielte Vorbelegung des Speichers helfen. Dabei wird nach jedem malloc()-Aufruf der Speicherbereich mit einem konfigurierbaren Byte gefüllt. Standardmäßig ist dies 0x50, der ASCII-Wert für 'P'. Jedes andere Byte ist ebenfalls möglich, auch Null, was wie calloc() wirkt und Probleme verschwinden lassen kann. Diese Speicherinitialisierung wird mit der Befehlszeilenoption "-dM" aktiviert. Sie beeinträchtigt die Leistung etwas und wird für den Produktionsbetrieb nicht empfohlen. Tritt ein Problem damit immer auf oder verschwindet es stets bei einer Vorbelegung mit Null, liegt eindeutig ein Fehler vor, der unbedingt gemeldet werden muss. Ändert sich dagegen nichts erkennbar, besteht kein Zusammenhang mit dieser Ursache.

Zur Untersuchung von Latenzproblemen sind sowohl strace und tcpdump auf dem lokalen Rechner als auch ein weiteres tcpdump auf dem entfernten System wichtig. Überall in der Verarbeitungskette können Verzögerungen entstehen. Nur wenn die Ursache bekannt ist, lässt sich gezielt eingreifen. Das lokale tcpdump zeigt, wann Eingabedaten eintreffen. strace zeigt, wann haproxy sie mit recv/recvfrom entgegennimmt. Achtung: OpenSSL verwendet read()/write() statt recv()/send(). strace zeigt außerdem, wann haproxy Daten sendet; tcpdump zeigt, wann das System sie an die Schnittstelle übergibt. Das entfernte tcpdump zeigt schließlich, wann die gesendeten Daten tatsächlich eintreffen, während der lokale Mitschnitt nur das Einreihen der Pakete in die Warteschlange erfasst. Der lokale Mitschnitt hat den Vorteil, dass strace und tcpdump dieselbe Referenzuhr verwenden. strace sollte mit "-tts200" ausgeführt werden, um vollständige Zeitstempel und ausreichend große, lesbare Datenausschnitte zu erhalten. tcpdump sollte mit "-nvvttSs0" ausgeführt werden, damit vollständige Pakete, tatsächliche Sequenznummern und vollständige Zeitstempel angezeigt werden.

In der Praxis nimmt haproxy eingehende Daten fast immer sofort entgegen, außer bei ausgelasteter CPU oder ungültigen Daten, die nicht zugestellt werden. Werden Daten empfangen, aber nicht gesendet, ist meist der Ausgabepuffer voll, weil der Empfänger die Daten nicht schnell genug verarbeitet. Bestätigen lässt sich dies daran, dass das Polling eine Zeit lang keine Schreibbereitschaft für den Ausgabedateideskriptor meldet. In der strace-Ausgabe ist es oft einfacher, zunächst das spätere Senden zu finden und dann rückwärts nach der Meldung der Schreibbereitschaft zu suchen. Dies fällt meist mit einem ACK des Empfängers zusammen, das tcpdump erfasst. Nach dem Senden können Daten noch eine Zeit lang untätig im System verbleiben. Auch hier kann das TCP-Überlastungsfenster die Übertragung begrenzen und auf ein ACK warten, das es öffnet. Ist der Datenverkehr ansonsten untätig und dauert das Senden 40 ms oder 200 ms, liegt eine andere, eigentlich normale Situation vor: Der Nagle-Algorithmus hält leere Pakete zurück, damit sie mit späteren Daten zusammengefasst werden können. Im reinen TCP-Modus und in Tunneln deaktiviert HAProxy Nagle automatisch. Beim Weiterleiten eines HTTP-Nachrichtenkörpers bleibt Nagle dagegen aktiviert, was durch weniger Pakete die Leistung verbessert. Manche nicht HTTP-konformen Anwendungen reagieren empfindlich auf diese Verzögerung bei der Übertragung unvollständiger HTTP-Antworten. Dann muss "option http-no-delay" aktiviert werden, um Nagle zu deaktivieren und die Einschränkung dieser Anwendungen zu umgehen. Andere Proxys in der Verarbeitungskette können jedoch ebenso betroffen sein. Zeigt tcpdump ein sofortiges Senden, während die Gegenseite die Daten erst später erhält, kann eine überlastete WAN-Verbindung oder ein überlastetes LAN mit aktiver Flusskontrolle die Ursache sein. Häufiger läuft HAProxy in einer virtuellen Maschine, und der Hypervisor hat aus irgendeinem Grund entschieden, die Daten nicht sofort zu senden. In virtualisierten Umgebungen verursacht fast immer die Virtualisierungsschicht solche Latenzprobleme. Um Zeit zu sparen, sollten daher zuerst tcpdump-Mitschnitte in der VM und auf den externen Komponenten verglichen werden. Jede Abweichung ist dem Hypervisor und seinen Treibern zuzurechnen.

Sind im tcpdump-Mitschnitt mit -vv TCP-SACK-Segmente sichtbar, hat die sendende Seite nachweislich einen Paketverlust festgestellt. Ihr Ausbleiben beweist nicht, dass keine Verluste auftreten; ihr Auftreten beweist jedoch, dass das Netzwerk Pakete verliert. Verluste sind in Netzwerken normal, allerdings in einem Ausmaß, bei dem SACKs mit bloßem Auge nicht auffallen. Treten sie häufig auf, sollte genau untersucht werden, was geschieht und wo Pakete verloren gehen. HTTP kommt mit TCP-Verlusten schlecht zurecht, da sie große Latenzen verursachen.

"netstat -i" zeigt Statistiken je Schnittstelle. Ein steigender Zähler Rx-Ovr bedeutet, dass dem System die Ressourcen fehlen, um alle eingehenden Pakete anzunehmen; sie gehen bereits vor der Verarbeitung durch den Netzwerktreiber verloren. Rx-Drp zeigt, dass empfangene Pakete im Netzwerk-Stack verloren gingen, weil die Anwendung sie nicht schnell genug verarbeitet. Dies kann auch bei Angriffen auftreten. Tx-Drp bedeutet, dass die Ausgabewarteschlangen voll waren und Pakete verworfen werden mussten. Bei TCP sollte dies sehr selten sein, kann aber auf eine ausgelastete ausgehende Verbindung hinweisen.
