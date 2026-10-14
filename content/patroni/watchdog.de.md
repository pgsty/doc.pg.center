---
title: "Watchdog-Unterstützung"
weight: 90
icon: fa-solid fa-dog
description: "Watchdog-Integration und Hinweise zum Fencing für Patroni-Cluster."
module: [PATRONI]
categories: [Konzept]
upstream_link: "https://patroni.readthedocs.io/en/latest/watchdog.html"
---

<a id="watchdog"></a>

Laufen mehrere PostgreSQL-Server gleichzeitig als Primärserver, können durch auseinanderlaufende Zeitleisten Transaktionen verloren gehen. Diese Situation wird auch als Split-Brain bezeichnet. Um sie zu vermeiden, muss Patroni sicherstellen, dass PostgreSQL nach Ablauf des Leader-Schlüssels im DCS keine Transaktions-Commits mehr annimmt. Unter normalen Umständen versucht Patroni dies zu erreichen, indem es PostgreSQL stoppt, sobald die Aktualisierung der Leader-Sperre aus irgendeinem Grund fehlschlägt. Dies kann jedoch aus verschiedenen Gründen scheitern:

- Patroni ist aufgrund eines Fehlers oder Speichermangels abgestürzt oder wurde versehentlich von einem Systemadministrator beendet.
- PostgreSQL fährt zu langsam herunter.
- Patroni kommt wegen hoher Systemlast, einer vom Hypervisor pausierten VM oder anderer Infrastrukturprobleme nicht zur Ausführung.

Um auch unter diesen Bedingungen korrektes Verhalten zu gewährleisten, unterstützt Patroni Watchdog-Geräte. Dies sind Software- oder Hardwaremechanismen, die das gesamte System zurücksetzen, wenn innerhalb eines bestimmten Zeitraums kein Keepalive-Heartbeat eintrifft. Sie bieten eine zusätzliche Absicherung, falls die üblichen Split-Brain-Schutzmechanismen von Patroni versagen.

Patroni versucht, den Watchdog vor der Hochstufung von PostgreSQL zum Primärserver zu aktivieren. Schlägt dies fehl und steht der Watchdog-Modus auf `required`, verweigert der Knoten die Leader-Rolle. Auch bei der Entscheidung über die Teilnahme an einer Leader-Wahl prüft Patroni, ob die Watchdog-Konfiguration die Leader-Rolle überhaupt zulässt. Nach der Herabstufung von PostgreSQL (etwa bei einem manuellen Failover) deaktiviert Patroni den Watchdog wieder. Ebenso wird der Watchdog deaktiviert, während Patroni pausiert ist.

Standardmäßig stellt Patroni den Watchdog so ein, dass er 5 Sekunden vor Ablauf der TTL auslöst. Mit den Standardwerten `loop_wait=10` und `ttl=30` hat die HA-Schleife dadurch mindestens 15 Sekunden (`ttl` - `safety_margin` - `loop_wait`) Zeit zum Abschluss, bevor das System zwangsweise zurückgesetzt wird. Für DCS-Zugriffe ist standardmäßig eine Zeitüberschreitung von 10 Sekunden konfiguriert. Ist der DCS beispielsweise wegen Netzwerkproblemen nicht verfügbar, bleiben Patroni und PostgreSQL damit mindestens 5 Sekunden (`ttl` - `safety_margin` - `loop_wait` - `retry_timeout`), um alle Clientverbindungen zu beenden.

Der Sicherheitsabstand ist die Zeit, die Patroni zwischen der Aktualisierung des Leader-Schlüssels und dem Keepalive für den Watchdog reserviert. Patroni versucht, unmittelbar nach Bestätigung der Aktualisierung des Leader-Schlüssels ein Keepalive zu senden. Wird der Patroni-Prozess genau im entscheidenden Moment längere Zeit angehalten, kann sich das Keepalive um mehr als den Sicherheitsabstand verzögern, ohne den Watchdog auszulösen. Dadurch entsteht ein Zeitfenster, in dem der Watchdog nicht vor Ablauf des Leader-Schlüssels auslöst und die Garantie somit nicht mehr gilt. Damit der Watchdog unter allen Umständen sicher auslöst, `safety_margin` auf -1 setzen. Dadurch beträgt die Watchdog-Frist `ttl // 2`, also die Hälfte der TTL. Wird diese Garantie benötigt, sollte wahrscheinlich `ttl` erhöht und/oder `loop_wait` sowie `retry_timeout` verringert werden.

Derzeit werden Watchdogs nur über die Linux-Watchdog-Geräteschnittstelle unterstützt.

--------

## Software-Watchdog unter Linux einrichten {#setting-up-software-watchdog-on-linux}

Die Standardkonfiguration von Patroni versucht unter Linux, `/dev/watchdog` zu verwenden, sofern Patroni darauf zugreifen kann. Für die meisten Anwendungsfälle ist der im Linux-Kernel enthaltene Software-Watchdog ausreichend sicher.

Zum Aktivieren des Software-Watchdogs vor dem Start von Patroni folgende Befehle als root ausführen:

``` bash
modprobe softdog
# Replace postgres with the user you will be running patroni under
chown postgres /dev/watchdog
```

Für Tests kann es hilfreich sein, Neustarts durch das zusätzliche Argument `soft_noboot=1` in der modprobe-Befehlszeile zu deaktivieren. Dann schreibt der Watchdog lediglich eine über `dmesg` sichtbare Zeile in den Kernel-Ringpuffer.

Nach erfolgreicher Aktivierung protokolliert Patroni Informationen über den Watchdog.
