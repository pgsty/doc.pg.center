---
title: "2. HAProxy-Architektur"
linkTitle: "2. Architektur"
weight: 260
description: "Prozesse, Threads, Ereignisschleife, chroot, Protokolle, Uhren und das TCP-Proxy-Modell"
icon: fa-solid fa-diagram-project
module: [HAPROXY]
categories: [Konzept]
aliases:
  - /haproxy/management/architecture/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 2"
---

HAProxy ist ein ereignisgesteuerter, nicht blockierender Daemon mit mehreren Threads. Er plant sämtliche Aktivitäten über Ereignis-Multiplexing, statt die Umschaltung zwischen mehreren Aktivitäten dem System zu überlassen. Meist läuft er als einzelner Prozess. "ps aux" zeigt daher nur einen "haproxy"-Prozess an, außer während eines unterbrechungsfreien Neuladens, wenn ein älterer Prozess seine Arbeit parallel zum neuen beendet. Seine Aktivitäten lassen sich somit jederzeit leicht mit strace verfolgen. Um die verfügbaren Prozessoren zu nutzen, startet haproxy standardmäßig für jeden Prozessor, auf dem er laufen darf, einen Worker-Thread. Sofern nicht ausdrücklich anders konfiguriert, wird der eingehende Datenverkehr auf alle diese Threads verteilt, die dieselbe Ereignisschleife ausführen. Abhängigkeiten zwischen Threads werden sorgfältig auf das notwendige Minimum begrenzt, um eine annähernd lineare Skalierung zu erreichen. Das bedeutet unter anderem, dass eine bestimmte Verbindung von einem einzigen Thread bedient wird. Um die gesamte verfügbare Rechenleistung auszunutzen, müssen daher mindestens so viele Verbindungen wie Threads vorhanden sein, was fast immer gegeben ist.

HAProxy ist so ausgelegt, dass er sich beim Start in einer chroot-Umgebung isoliert, in der keinerlei Dateisystemzugriffe möglich sind. Dies gilt auch für seine Bibliotheken, etwa libc und libssl. Eine unmittelbare Folge ist, dass ein laufender Prozess keine Konfigurationsdatei neu laden kann, um Änderungen anzuwenden. Stattdessen wird ein neuer Prozess mit der aktualisierten Konfigurationsdatei gestartet. Weniger offensichtlich ist etwa, dass Zeitzonen- oder Resolver-Dateien, auf die libc zur Laufzeit zugreifen könnte, nicht gefunden werden. Das sollte allerdings normalerweise nicht vorkommen, da sie nach dem Start nicht mehr benötigt werden. Eine nützliche Folge dieses Prinzips ist, dass der HAProxy-Prozess vollständig zustandslos ist und nach seinem Beenden keine Aufräumarbeiten nötig sind. Jede funktionierende Methode zum Beenden des Prozesses ist daher geeignet.

HAProxy schreibt keine Protokolldateien. Er verwendet das standardisierte syslog-Protokoll, um Protokollmeldungen an einen entfernten Server zu senden, der sich häufig auf demselben System befindet.

Für Zeitüberschreitungen verwendet HAProxy eine interne Uhr, die aus der Systemzeit abgeleitet wird und unerwartete Abweichungen korrigiert. Dazu begrenzt er die Wartezeit auf ein Ereignis in poll() und misst die tatsächlich verstrichene Zeit. In der Praxis wartet er nie länger als eine Sekunde. Deshalb zeigt strace bei einem vollständig untätigen Prozess regelmäßig Aufrufe von poll() oder einer seiner Varianten, jeweils zwischen zwei gettimeofday()-Aufrufen. Diese sind normal, völlig harmlos und so kostengünstig, dass ihre Last auf Systemebene nicht messbar ist. Es handelt sich also nicht um eine Auffälligkeit. Beispiel:

```text
16:35:40.002320 gettimeofday({1442759740, 2605}, NULL) = 0
16:35:40.002942 epoll_wait(0, {}, 200, 1000) = 0
16:35:41.007542 gettimeofday({1442759741, 7641}, NULL) = 0
16:35:41.007998 gettimeofday({1442759741, 8114}, NULL) = 0
16:35:41.008391 epoll_wait(0, {}, 200, 1000) = 0
16:35:42.011313 gettimeofday({1442759742, 11411}, NULL) = 0
```

HAProxy ist ein TCP-Proxy, kein Router. Er verarbeitet bestehende, vom Kernel validierte Verbindungen, jedoch weder Pakete beliebiger Art noch Sockets in anderen Zuständen, etwa SYN_RECV oder TIME_WAIT. Deren Vorhandensein kann ihn allerdings daran hindern, sich an einen Port zu binden. Das Annehmen eingehender und das Herstellen ausgehender Verbindungen übernimmt das System. Deshalb gibt es keinen Zusammenhang zwischen den Paketen auf den beiden Seiten einer weitergeleiteten Verbindung: Größe, Anzahl und sogar Adressfamilie können unterschiedlich sein. Da eine Verbindung nur über einen Socket im Zustand LISTEN angenommen werden kann, sind alle Sockets, auf denen HAProxy lauscht, mit "netstat" zur Anzeige lauschender Sockets sichtbar. Beispiel:

```haproxy
# netstat -ltnp
```

Active Internet connections (only servers) Proto Recv-Q Send-Q Local Address Foreign Address State
PID/Program name tcp 0 0 0.0.0.0:22 0.0.0.0:\* LISTEN 1629/sshd tcp 0 0 0.0.0.0:80 0.0.0.0:\* LISTEN
2847/haproxy tcp 0 0 0.0.0.0:443 0.0.0.0:\* LISTEN 2847/haproxy
