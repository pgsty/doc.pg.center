---
title: "Watchdog-Unterstützung"
weight: 90
icon: fa-solid fa-dog
description: "Watchdog-Integration und Fencing-Betrachtungen für Patroni-Clustereinstellungen."
module: [PATRONI]
categories: [Konzept]
aliases: [/docs/patroni/watchdog/]
upstream_link: "https://patroni.readthedocs.io/en/latest/watchdog.html"
---

<a id="watchdog"></a>

Das gleichzeitige Ausführen mehrerer PostgreSQL-Server als primäre Server kann zu Datenverlusten aufgrund von unterschiedlichen Zeitlinien führen. Diese Situation wird auch als "Split-Brain"-Problem bezeichnet. Um das Split-Brain-Problem zu vermeiden, muss Patroni sicherstellen, dass PostgreSQL keine Transaktionsbestätigungen akzeptiert, nachdem der Schlüssel für den primären Server in der DCS abgelaufen ist. Unter normalen Umständen versucht Patroni, dies durch das Stoppen von PostgreSQL zu erreichen, falls der Update-Vorgang für den primären Schlüssel aus irgendeinem Grund fehlschlägt. Dies kann jedoch aus verschiedenen Gründen fehlschlagen:

- Patroni ist aufgrund eines Fehlers, eines Zustands mit unzureichendem Arbeitsspeicher oder durch versehentliches Abschalten durch einen Systemadministrator abgestürzt.
- Das Herunterfahren von PostgreSQL ist zu langsam.
- Patroni kann aufgrund hoher Systemlast, durch den Hypervisor pausierte VM oder anderer Infrastrukturprobleme nicht ausgeführt werden.

Um ein korrektes Verhalten unter diesen Bedingungen zu gewährleisten, unterstützt Patroni Überwachungsgeräte. Überwachungsgeräte sind Software- oder Hardware-Mechanismen, die das gesamte System zurücksetzen, wenn sie innerhalb eines bestimmten Zeitrahmens kein "Keepalive"-Heartbeat erhalten. Dies bietet eine zusätzliche Schutzschicht, falls die üblichen Patroni-Split-Brain-Schutzmechanismen ausfallen.

Patroni wird versuchen, den Watchdog vor der Beförderung von PostgreSQL zum Primärserver zu aktivieren. Falls die Aktivierung des Watchdogs fehlschlägt und der Watchdog-Modus `required` ist, wird der Knoten ablehnen, Leader zu werden. Bei der Entscheidung, an der Leader-Wahl teilzunehmen, wird Patroni auch überprüfen, ob die Watchdog-Konfiguration es zulassen würde, Leader zu werden. Nach der Demotion von PostgreSQL (z.B. aufgrund eines manuellen Failovers) wird Patroni den Watchdog erneut deaktivieren. Der Watchdog wird auch während der pausierten Zustands von Patroni deaktiviert.

Standardmäßig wird Patroni den Watchdog so einrichten, dass er 5 Sekunden vor TTL abläuft. Mit der standardmäßigen Konfiguration von `loop_wait=10` und `ttl=30` erhält der HA-Loop mindestens 15 Sekunden (`ttl` - `safety_margin` - `loop_wait`) zur Abschließung, bevor der Systemzustand durch eine zwingende Neustart verloren geht. Standardmäßig wird der Zugriff auf das DCS nach 10 Sekunden ablaufen. Dies bedeutet, dass wenn das DCS nicht verfügbar ist, z.B. aufgrund von Netzwerkproblemen, Patroni und PostgreSQL mindestens 5 Sekunden (`ttl` - `safety_margin` - `loop_wait` - `retry_timeout`) haben, um in einen Zustand zu gelangen, in dem alle Clientverbindungen beendet sind.

Der Sicherheitsabstand ist die Zeit, die Patroni für den Zeitraum zwischen dem Aktualisieren des Leiterschlüssels und dem Senden von "Keepalive"-Signalen reserviert. Patroni wird versuchen, sofort nach der Bestätigung des Aktualisierens des Leiterschlüssels ein "Keepalive"-Signal zu senden. Wenn der Patroni-Prozess über einen längeren Zeitraum genau zum richtigen Zeitpunkt angehalten wird, kann das "Keepalive"-Signal verzögert werden, ohne dass der "Watchdog" ausgelöst wird. Dies führt zu einem Zeitraum, in dem der "Watchdog" nicht ausgelöst wird, bevor der Leiterschlüssel abläuft, wodurch die Garantie ungültig wird. Um sicherzustellen, dass der "Watchdog" unter allen Umständen ausgelöst wird, sollten Sie den "Watchdog" so konfigurieren, dass er nach der Hälfte der TTL-Zeit abläuft, indem Sie `safety_margin` auf -1 setzen, um die "Watchdog"-Timeout-Zeit auf `ttl // 2` zu setzen. Wenn Sie diese Garantie benötigen, sollten Sie möglicherweise `ttl` erhöhen und/oder `loop_wait` und `retry_timeout` verringern.

Derzeit werden "Watchdogs" ausschließlich über die Linux-Watchdog-Geräte-Schnittstelle unterstützt.

--------

## Einrichtung eines Software-Überwachers unter Linux {#setting-up-software-watchdog-on-linux}
Die Standard-Patroni-Konfiguration versucht, `/dev/watchdog` unter Linux zu verwenden, falls dies für Patroni zugänglich ist. Für die meisten Anwendungsfälle ist die Verwendung eines Software-Überwachers, der in den Linux-Kernel integriert ist, ausreichend sicher.

Um den Software-Überwacher zu aktivieren, führen Sie die folgenden Befehle als Root aus, bevor Sie Patroni starten:

``` bash
modprobe softdog
# Replace postgres with the user you will be running patroni under
chown postgres /dev/watchdog
```

Für Tests kann es hilfreich sein, das Neustarten zu deaktivieren, indem man `soft_noboot=1` zur Befehlszeile von modprobe hinzufügt. In diesem Fall protokolliert der Watchdog lediglich eine Zeile im Kernel-Ring-Puffer, die über `dmesg` sichtbar ist.

Patroni protokolliert Informationen über den Watchdog, wenn dieser erfolgreich aktiviert wurde.
