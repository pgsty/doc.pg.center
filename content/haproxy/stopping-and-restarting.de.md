---
title: "4. HAProxy stoppen und neu starten"
linkTitle: "4. Stoppen und Neustarten"
weight: 280
description: "Signale, geordnetes Stoppen, Neuladen und Neustarts im Master-Worker-Modus"
icon: fa-solid fa-rotate
module: [HAPROXY]
categories: [Aufgabe]
aliases:
  - /haproxy/management/stopping-and-restarting/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 4"
---

HAProxy unterstützt ein geordnetes und ein sofortiges Stoppen. Beim sofortigen Stoppen genügt das Signal SIGTERM an den haproxy-Prozess: Er beendet sich unmittelbar und schließt alle bestehenden Verbindungen. Das geordnete Stoppen wird durch SIGUSR1 ausgelöst. Dabei gibt HAProxy nur die lauschenden Ports frei und verarbeitet die bestehenden Verbindungen weiter, bis sie geschlossen werden. Sobald die letzte Verbindung geschlossen ist, beendet sich der Prozess.

Das Dienstverwaltungsskript verwendet das sofortige Stoppen für die Aktionen "stop" und "restart". Das geordnete Stoppen wird bei "reload" eingesetzt, um eine neue Konfiguration möglichst ohne Unterbrechung in einem neuen Prozess zu laden.

Beide Signale kann der neue haproxy-Prozess beim Neuladen oder Neustarten selbst senden. So werden sie zum spätestmöglichen Zeitpunkt und nur dann gesendet, wenn es unbedingt erforderlich ist. Dafür dienen die Optionen "-st" für sofortiges und "-sf" für geordnetes Stoppen.

Im Master-Worker-Modus muss zum Neuladen der Konfiguration kein neuer haproxy-Prozess gestartet werden. Der Master-Prozess reagiert auf SIGUSR2, indem er sich selbst mit dem Parameter -sf und den nachfolgenden PIDs der Worker erneut ausführt. Anschließend liest der Master die Konfigurationsdatei ein und erzeugt durch Fork neue Worker.

Um die Verwendung dieser Signale zu verstehen, ist der gesamte Neustartablauf wichtig.

Zunächst läuft bereits ein haproxy-Prozess. Die Administration fordert mit einem systemspezifischen Befehl wie "/etc/init.d/haproxy reload" an, die neue Konfigurationsdatei zu übernehmen. Das Dienstskript, also /etc/init.d/haproxy oder dessen Entsprechung, prüft zuerst mit "haproxy -c", ob die Datei korrekt eingelesen werden kann. Danach versucht es, haproxy mit dieser Konfiguration und "-st" oder "-sf" zu starten.

HAProxy versucht nun, sich an alle lauschenden Ports zu binden. Bei einem schwerwiegenden Fehler, etwa einer auf dem System nicht vorhandenen Adresse oder fehlenden Berechtigungen, beendet sich der Prozess mit einem Fehler. Scheitert eine Socket-Bindung, weil ein Port bereits belegt ist, sendet der Prozess zunächst SIGTTOU an alle in der PID-Liste von "-st" oder "-sf" angegebenen Prozesse. Dieses sogenannte Pausensignal weist alle bestehenden haproxy-Prozesse an, vorübergehend nicht mehr auf ihren Ports zu lauschen, damit der neue Prozess erneut versuchen kann, sich zu binden. Der alte Prozess verarbeitet währenddessen die bestehenden Verbindungen weiter. Scheitert die Bindung weiterhin, etwa weil ein anderer Daemon denselben Port verwendet, sendet der neue Prozess SIGTTIN an die alten Prozesse. Diese nehmen daraufhin ihren Betrieb wieder auf, als wäre nichts geschehen: Sie lauschen wieder auf den Ports und nehmen Verbindungen an. Dieses Verfahren ist systemabhängig und wird von manchen Betriebssystemen im Mehrprozessbetrieb möglicherweise nicht unterstützt.

Kann sich der neue Prozess erfolgreich an alle Ports binden, sendet er entweder SIGTERM für sofortiges Stoppen bei "-st" oder SIGUSR1 für geordnetes Stoppen bei "-sf" an alle alten Prozesse. Damit teilt er ihnen mit, dass er den Betrieb übernommen hat und sie sich entweder sofort oder nach Abschluss ihrer Arbeit beenden müssen.

Dabei gibt es zwei kurze Zeitfenster von jeweils wenigen Millisekunden, in denen unter hoher Last einzelne Verbindungsfehler auftreten können. Typischerweise wird pro Neuladen etwa 1 Fehler je 10000 neuer Verbindungen pro Sekunde beobachtet. Eine stark ausgelastete Website mit 30000 neuen Verbindungen pro Sekunde kann somit bei jedem Neuladen etwa 3 fehlgeschlagene Verbindungen aufweisen. Dies geschieht in folgenden zwei Situationen:

- Kann sich der neue Prozess wegen des alten Prozesses nicht binden, muss er zunächst die Folge
  SIGTTOU+SIGTTIN durchlaufen. Bei einigen Dutzend Frontends dauert dies typischerweise etwa eine
  Millisekunde. Währenddessen sind manche Ports weder an den alten noch an den neuen Prozess gebunden.
  Auf Systemen mit der Socket-Option SO_REUSEPORT umgeht HAProxy dies: Der neue Prozess kann sich
  binden, ohne den alten zuvor zur Freigabe aufzufordern. Die meisten BSD-Systeme unterstützen dies
  seit sehr langer Zeit. Linux unterstützte es in Version 2.0 und entfernte es etwa mit 2.2 wieder;
  damals waren jedoch einige Patches verfügbar. Mit Kernel 3.9 wurde es erneut eingeführt. Bei einer
  höheren als der oben genannten Fehlerrate daher sicherstellen, dass der Kernel mindestens 3.9
  verwendet oder die entsprechenden Patches rückportiert wurden, was weniger wahrscheinlich ist.

- Wenn die alten Prozesse ihre lauschenden Ports schließen, verteilt der Kernel noch im Socket-Backlog
  wartende Verbindungen möglicherweise nicht neu. Unter hoher Last kann unmittelbar vor dem Schließen
  ein SYN-Paket eintreffen, woraufhin der Client ein RST-Paket erhält. In kritischen Umgebungen, die
  selbst einen einzigen Verbindungsabbruch nicht tolerieren, werden deshalb manchmal Firewall-Regeln
  eingesetzt, die SYN-Pakete während des Neuladens blockieren und den Client zur erneuten Übertragung
  zwingen. Das ist vollständig systemabhängig: Manche Systeme können andere Warteschlangen lauschender
  Sockets berücksichtigen und das RST vermeiden. Ein zweiter Fall betrifft ein ACK des Clients für
  einen lokalen Socket, der unmittelbar vor dem Schließen im Zustand SYN_RECV war. Dieses ACK führt
  zu einem RST-Paket, ohne dass der haproxy-Prozess bereits von der Verbindung weiß. Dieser Fall ist
  schwieriger zu vermeiden. Die genannten Firewall-Regeln helfen jedoch, wenn sie etwa eine Sekunde
  vor dem Neustart des Prozesses angewendet werden.

Bei der überwiegenden Mehrheit der Nutzer treten solche Verbindungsabbrüche nie auf, da ihre Last nicht ausreicht, um diese Race Conditions auszulösen. Auch bei den meisten Nutzern mit hohem Datenverkehr liegt die Fehlerrate noch deutlich innerhalb der üblichen Schwankungen, sofern ihre Systeme zumindest SO_REUSEPORT korrekt unterstützen.
