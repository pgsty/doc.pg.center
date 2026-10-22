---
title: "8. Protokollierung"
linkTitle: "8. Protokollierung"
weight: 320
description: "Syslog-Anbindung, Start- und Laufzeitprotokolle sowie Fehlerbehebung bei der Protokollierung"
icon: fa-solid fa-file-lines
module: [HAPROXY]
categories: [Aufgabe]
aliases:
  - /haproxy/management/logging/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 8"
---

Für die Protokollierung verwendet HAProxy immer einen syslog-Server, da er nicht auf das Dateisystem zugreift. Üblicherweise sendet er Protokollmeldungen über UDP an den Protokollserver, standardmäßig auf Port 514. Sehr häufig ist dafür 127.0.0.1 eingestellt, wo der lokale syslog-Daemon läuft. Ebenso können Meldungen über das Netzwerk an einen zentralen Server gesendet werden. Dieser bietet besonders im Aktiv/Aktiv-Betrieb Vorteile, wenn die Meldungen in ihrer Eingangsreihenfolge zusammengeführt werden sollen. HAProxy kann Protokollmeldungen auch über einen UNIX-Socket an den lokalen syslog-Daemon senden. Davon wird jedoch ausdrücklich abgeraten: Wird der syslog-Server neu gestartet, während haproxy läuft, wird der Socket ersetzt und neue Protokollmeldungen gehen verloren. Da HAProxy in einer chroot-Umgebung isoliert ist, kann er keine Verbindung zum neuen Socket herstellen. Im praktischen Betrieb wurde zudem beobachtet, dass die Protokollpuffer bei UNIX-Sockets sehr klein sind und selbst unter sehr geringer Last Meldungen verloren gehen. Für Tests kann dieses Verfahren dennoch ausreichen.

Es wird empfohlen, die folgende Direktive in den Abschnitt "global" aufzunehmen, damit HAProxy mit der Facility "local0" an den lokalen Daemon protokolliert:

```text
log 127.0.0.1:514 local0
```

Anschließend die folgende Direktive in jeden Abschnitt "defaults" oder in jeden Frontend- und Backend-Abschnitt aufnehmen:

```text
log global
```

Damit nutzen alle Protokolle die globale Festlegung des Protokollservers.

Einige syslog-Daemons empfangen standardmäßig keinen UDP-Datenverkehr. Die Syntax zum Aktivieren hängt daher vom verwendeten Daemon ab:

- Bei sysklogd muss das Argument "-r" in der Befehlszeile des Daemons angegeben werden, damit er
  auf einem UDP-Socket auf entfernte Protokollmeldungen lauscht. Dies lässt sich nicht auf die
  Adresse 127.0.0.1 beschränken; er empfängt daher auch Meldungen von entfernten Systemen.

- Bei rsyslogd müssen die folgenden Zeilen zur Konfigurationsdatei hinzugefügt werden:

```shell
$ModLoad imudp
$UDPServerAddress *
$UDPServerRun 514
```

- Bei syslog-ng lässt sich wie folgt eine neue Quelle anlegen. Sie muss anschließend in einer
  der "log"-Direktiven als gültige Quelle eingetragen werden:

```text
source s_udp {
  udp(ip(127.0.0.1) port(514));
};
```

Weitere Informationen enthält das Handbuch des jeweiligen syslog-Daemons. Wenn in den Protokolldateien des Systems keine Meldungen erscheinen, helfen folgende Tests:

- haproxy neu starten. Jedes Frontend und Backend protokolliert eine Zeile zu seinem Start.
  Werden diese Meldungen empfangen, funktioniert die Protokollierung.

- "strace -tt -s100 -etrace=sendmsg -p \<haproxy's pid\>" ausführen und eine Aktivität erzeugen,
  die voraussichtlich protokolliert wird. Die mit sendmsg() gesendeten Meldungen sollten sichtbar
  sein. Andernfalls haproxy unter strace neu starten. Sind weiterhin keine Meldungen zu sehen,
  liegt eindeutig ein Konfigurationsfehler vor.

- Mit tcpdump den Datenverkehr auf Port 514 beobachten, etwa auf der Loopback-Schnittstelle,
  wenn die Meldungen lokal gesendet werden: "tcpdump -As0 -ni lo port 514". Sind dort Pakete
  sichtbar, werden die Meldungen nachweislich gesendet; dann muss der syslogd-Daemon untersucht werden.

Während die Frontends, die eingehende Verbindungen annehmen, die Verkehrsprotokolle senden, müssen auch Backends protokollieren können, um Zustandsänderungen eines Servers nach einem Health Check zu melden. Alle verfügbaren Protokolleinstellungen sind im Konfigurationshandbuch von HAProxy beschrieben.

Zweckmäßig ist eine Facility, die kein anderer Daemon verwendet. HAProxy-Beispiele schlagen häufig "local0" für Verkehrsprotokolle und "local1" für Verwaltungsprotokolle vor, da diese im praktischen Betrieb sonst nicht vorkommen. Eine einzelne Facility würde ebenfalls ausreichen. Getrennte Protokolle erleichtern die Auswertung. Zu beachten ist aber auch, dass Protokolle vertrauliche Informationen enthalten können und deshalb nicht mit anderen Protokollen vermischt werden dürfen, die versehentlich an unbefugte Personen gelangen könnten.

Für die Fehlerbehebung im laufenden Betrieb bei möglichst geringer Beeinträchtigung der Serverkapazität wird das mit HAProxy gelieferte Werkzeug "halog" empfohlen. Es ähnelt grep und ist für die sehr schnelle Verarbeitung von HAProxy-Protokolldateien ausgelegt. Typische Durchsatzwerte liegen zwischen 1 und 2 GB Protokolldaten pro Sekunde. Es kann gezielt Meldungen auswählen, etwa nach HTTP-Statuscodeklassen, Verbindungsabschlussstatus, Antwortzeitbereichen oder ausschließlich nach Fehlern suchen, Zeilen zählen, die Ausgabe auf eine bestimmte Zeilenzahl begrenzen und weitergehende Statistiken erstellen. Dazu gehören das Sortieren von Servern nach Antwortzeit oder Fehleranzahl, von URLs nach Zeit oder Anzahl und von Clientadressen nach Zugriffszahl. Damit lassen sich Auffälligkeiten wie ein Bot, der die Website in einer Schleife aufruft, schnell erkennen und blockieren.
