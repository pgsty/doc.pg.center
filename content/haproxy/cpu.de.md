---
title: "7. CPU-Auslastung"
linkTitle: "7. CPU"
weight: 310
description: "Threads, CPU-Affinität, Sättigung, Profiling und Leistungsverhalten"
icon: fa-solid fa-microchip
module: [HAPROXY]
categories: [Aufgabe]
aliases:
  - /haproxy/management/cpu/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 7"
---

> [!WARNING]
> Versionshinweis: Dieses Kapitel enthält historische Hinweise zum Mehrprozessbetrieb. Seit HAProxy 2.5 werden `nbproc` und `bind process` nicht mehr unterstützt. Konfigurieren Sie für diese Ausgabe Threads mit `nbthread`, `thread-groups` und `cpu-map` in den [globalen Einstellungen](/de/haproxy/global/#section-3-1).

HAProxy verbringt normalerweise den größten Teil seiner Zeit im System und einen kleineren Teil im Benutzerraum. Eine sorgfältig optimierte CPU mit 3.5 GHz kann auf einem einzelnen Kern bei 100% CPU-Auslastung etwa 80000 vollständige Verbindungsaufbauten und -abbauten pro Sekunde bewältigen. Bei vollständiger Auslastung eines Kerns sind folgende Anteile typisch:

- 95% System, 5% Benutzerraum bei langen TCP-Verbindungen oder großen HTTP-Objekten
- 85% System und 15% Benutzerraum bei kurzen TCP-Verbindungen oder kleinen HTTP-Objekten im Close-Modus
- 70% System und 30% Benutzerraum bei kleinen HTTP-Objekten im Keep-Alive-Modus

Viele Regeln und reguläre Ausdrücke erhöhen den Anteil im Benutzerraum. Firewall-Regeln, Verbindungsverfolgung und komplexe Routingtabellen erhöhen dagegen den Systemanteil.

Auf den meisten Systemen lässt sich die bei Netzwerkübertragungen beobachtete CPU-Zeit in 4 Teile gliedern:

- Interrupt-Zeit: Sie umfasst die gesamte Verarbeitung beim Eingang von I/O-Ereignissen, noch bevor
  der Zielprozess bekannt ist. Rx-Pakete werden typischerweise hier erfasst. Auf Systemen wie Linux,
  die die Interrupt-Verarbeitung an einen eigenen Thread delegieren können, erscheint dieser Anteil
  möglicherweise als softirq; der Thread heißt ksoftirqd/0 für CPU 0. Welche CPU diese Arbeit
  übernimmt, bestimmen in der Regel die Hardwareeinstellungen. Bei softirq lässt sich die Verarbeitung
  jedoch häufig auf eine andere CPU verlagern. Dieser Anteil wird oft als störende Zusatzlast
  wahrgenommen, weil er keinem Prozess zugeordnet ist. Tatsächlich bereitet er die Arbeit für den
  Prozess vor.

- Systemzeit: Sie umfasst die Verarbeitung durch Kernel-Code, der aus dem Benutzerraum aufgerufen
  wird. Beispielsweise zählen Systemaufrufe dazu. Alle synchron ausgelieferten Tx-Pakete werden als
  Systemzeit erfasst. Müssen Pakete wegen voller Warteschlangen zurückgestellt werden, können sie
  später im Interrupt-Kontext verarbeitet werden, etwa nach Eingang eines ACK, das ein TCP-Fenster öffnet.

- Benutzerzeit: Hier wird ausschließlich Anwendungscode im Benutzerraum ausgeführt. HAProxy läuft
  ausschließlich in diesem Bereich, nutzt aber intensiv Systemaufrufe. Regelverarbeitung, reguläre
  Ausdrücke, Komprimierung und Verschlüsselung erhöhen diesen Anteil der CPU-Auslastung.

- Leerlaufzeit: Sie fällt an, wenn die CPU nichts zu tun hat. Beispielsweise wartet HAProxy auf eine
  eingehende Verbindung oder darauf, dass Daten gesendet werden können, weil das System noch auf ein
  ACK des Clients wartet, um diese Daten zu übertragen.

Für die Tätigkeit von HAProxy ist in der Praxis meist die folgende, hinreichend brauchbare, aber keineswegs exakte Zuordnung möglich: Interrupt/softirq entsteht durch die Rx-Verarbeitung in Kernel-Treibern, Benutzerzeit durch die Verarbeitung auf Schicht 7 in HAProxy und Systemzeit durch die Netzwerkverarbeitung auf dem Tx-Pfad.

HAProxy arbeitet mit einer Ereignisschleife. Er wartet mit poll() oder einer Alternative auf neue Ereignisse, verarbeitet sie möglichst schnell und kehrt dann zu poll() zurück. Dabei misst er die Wartezeit in poll() im Verhältnis zur Zeit für die Ereignisverarbeitung. Der Anteil der Polling-Zeit an der Gesamtzeit heißt "idle" und bezeichnet die Zeit, in der auf ein Ereignis gewartet wird. Die Statistikseite zeigt ihn in der Zeile "idle", die CLI unter "Idle_pct". Ein Wert nahe 100% bedeutet sehr geringe Last; ein Wert nahe 0% bedeutet ständige Aktivität. Auf einem überlasteten System ist die Messung nicht besonders genau, weil andere Prozesse dem haproxy-Prozess die CPU entziehen können. Dennoch zeigt sie gut, wie HAProxy seine eigene Auslastung einschätzt: Sind sowohl die Systemlast als auch der Leerlaufanteil niedrig, hat HAProxy möglicherweise viel Arbeit zu erledigen, etwa durch sehr aufwendige Regeln. Meldet HAProxy dagegen nahezu 100% Leerlauf, obwohl die Verarbeitung langsam ist, kann er sie nicht beschleunigen, da er bereits auf eingehende Daten wartet. Im folgenden Beispiel ist haproxy vollständig im Leerlauf:

```shell
$ echo "show info" | socat - /var/run/haproxy.sock | grep ^Idle
Idle_pct: 100
```

Wird der Leerlaufanteil sehr klein, ist es wichtig, das System zu optimieren und Prozesse sowie Interrupts passend zuzuordnen, damit für alle Aufgaben möglichst viel CPU-Leistung verfügbar bleibt. Ist eine Firewall vorhanden, kann es sinnvoll sein, sie testweise zu deaktivieren oder zu optimieren, um auszuschließen, dass sie einen erheblichen Teil der Leistungsbegrenzung verursacht. Das Entladen einer zustandsbehafteten Firewall senkt im Allgemeinen sowohl Interrupt/softirq- als auch Systemzeit, da sie auf dem Rx- und dem Tx-Pfad eingreift. Unter Linux zeigt das Entladen der Module nf_conntrack und ip_conntrack, ob sich dadurch etwas gewinnen lässt. Ist dies der Fall, läuft das Modul mit Standardeinstellungen und muss für bessere Leistung optimiert werden. Meist bedeutet das eine deutlich größere Hashtabelle. Unter FreeBSD deaktiviert "pfctl -d" die Firewall "pf" samt zustandsbehafteter Verarbeitung.

Wird viel Zeit in Interrupt/softirq verbracht, ist sicherzustellen, dass diese Verarbeitung und haproxy nicht auf derselben CPU laufen. Die meisten Systeme binden Aufgaben bevorzugt an die CPU, die den Netzwerkverkehr empfängt, weil dies bestimmte Arbeitslasten beschleunigt. Bei stark netzwerkabhängigen Arbeitslasten wirkt es umgekehrt: Der haproxy-Prozess konkurriert mit der zugehörigen Kernel-Verarbeitung. HAProxy an einen Kern und die Interrupts an einen anderen Kern mit demselben L3-Cache zu binden, verbessert die Netzwerkleistung meist spürbar. In der Praxis ist der Arbeitsumfang von HAProxy und Netzwerk-Stack ähnlich, sodass jeder nahezu eine ganze CPU auslasten kann. Unter Linux erfolgt die Zuordnung für haproxy mit taskset oder cpu-map in der haproxy-Konfiguration, für Interrupts unter /proc/irq. Viele Netzwerkschnittstellen unterstützen mehrere Warteschlangen und Interrupts. Meist hilft es, sie auf wenige CPU-Kerne mit gemeinsamem L3-Cache zu verteilen. irq_balance bitte immer stoppen; bei solchen Arbeitslasten trifft es stets die ungünstigste Entscheidung.

Bei CPU-intensiven Arbeitslasten mit viel SSL-Datenverkehr oder Komprimierung können mehrere auf bestimmte Aufgaben spezialisierte Prozesse sinnvoll sein. Eine allgemeingültige Regel gibt es jedoch nicht; dies muss experimentell ermittelt werden.

Zur Erhöhung der verfügbaren CPU-Leistung lässt sich HAProxy mit der Direktive "nbproc" im Abschnitt global in mehreren Prozessen ausführen. Dabei gelten einige Einschränkungen:

- Health Checks werden pro Prozess ausgeführt. Die Zielserver erhalten daher so viele Prüfungen,
  wie Prozesse laufen;
- maxconn-Werte und Warteschlangen gelten pro Prozess. Der Wert muss deshalb passend gewählt
  werden, damit die Server nicht überlastet werden;
- ausgehende Verbindungen sollten keine Portbereiche verwenden, um Konflikte zu vermeiden
- Stick Tables gelten pro Prozess und werden nicht zwischen Prozessen geteilt;
- jeder peers-Abschnitt kann jeweils nur in einem Prozess laufen;
- CLI-Operationen wirken jeweils nur auf einen einzelnen Prozess.

Unter diesen Voraussetzungen ist häufig eine erste Schicht aus mehreren Prozessen am einfachsten, die die aufwendige Verarbeitung übernimmt und den Datenverkehr an eine zweite Schicht mit einem einzelnen Prozess weitergibt. Dieses Verfahren eignet sich für die beiden CPU-intensiven Funktionen SSL und Komprimierung. Instanzen lassen sich leicht über UNIX-Sockets verketten, die weniger Aufwand als TCP-Sockets verursachen und keine Ports verbrauchen. Mit dem Proxy-Protokoll können Clientinformationen an die nächste Stufe weitergegeben werden. Dabei ist es meist sinnvoll, alle Aufgaben für den Einzelprozessbetrieb an Prozess Nummer 1 und zusätzliche Aufgaben an die nachfolgenden Prozesse zu binden. So lassen sich ähnliche Konfigurationen für unterschiedliche Rechner leichter erzeugen.

Unter Linux ab Version 3.9 ist der Mehrprozessbetrieb von HAProxy erheblich effizienter, wenn jeder Prozess einen eigenen lauschenden Socket an derselben Kombination IP:port verwendet. Der Kernel verteilt die Last dann gleichmäßig auf die Prozesse, statt alle aufzuwecken. Weitere Informationen enthält die Option "process" der "bind"-Schlüsselwörter im Konfigurationshandbuch.
