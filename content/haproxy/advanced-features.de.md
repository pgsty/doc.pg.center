---
title: "Erweiterte Funktionen"
linkTitle: "Erweiterte Funktionen"
weight: 60
description: "Verwaltung zur Laufzeit, Betriebssystemfunktionen, Lua-Skripte und Live-Tracing"
icon: fa-solid fa-wand-magic-sparkles
module: [HAPROXY]
categories: [Konzept]
aliases:
  - /haproxy/intro/advanced-features/
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
upstream_name: "HAProxy 3.4 Starter Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, sections 3.5–3.5.4"
---

## 3.5.1. Erweiterte Funktionen: Verwaltung {#section-3-5-1}

HAProxy ist für einen äußerst stabilen Betrieb und eine sichere Verwaltung in üblichen Produktionsumgebungen ausgelegt. Er wird als einzelne ausführbare Datei bereitgestellt und benötigt keinen Installationsvorgang. Mehrere Versionen können problemlos nebeneinander bestehen. Instanzen lassen sich daher nach ihrer Wichtigkeit schrittweise aktualisieren, statt alle gleichzeitig umzustellen; dieses Vorgehen wird empfohlen. Konfigurationsdateien können leicht versioniert werden. Die Konfigurationsprüfung erfolgt unabhängig vom laufenden Betrieb, ohne einen Dienst neu starten zu müssen, der anschließend möglicherweise nicht mehr startet. Dabei lassen sich auch komplexere Fehler erkennen, etwa eine Regel, die eine andere verdeckt, oder eine nicht funktionierende Sitzungspersistenz. Ausführliche Warnungen und Konfigurationshinweise helfen bei der Behebung. Die Rückwärtskompatibilität von Konfigurationsdateien reicht weit zurück: Version 1.5 unterstützt noch vollständig Konfigurationen für Version 1.1, die 13 Jahre zuvor geschrieben wurden. Version 1.6 entfernt lediglich kaum verwendete, veraltete Schlüsselwörter, deren Aufgaben anders gelöst werden können. Das Aktualisieren von Konfiguration und Software erfolgt ohne Betriebsunterbrechung, indem alte und neue Prozesse nebeneinander laufen und jeweils ihre eigenen Verbindungen bedienen. Beim Start werden Systemzustand, Build-Optionen und Bibliothekskompatibilität gemeldet.

Erweiterte Funktionen erlauben es Anwendungsadministratoren, einen Server geordnet außer Betrieb zu nehmen: Sie können feststellen, wann keine Aktivität mehr vorhanden ist, ihn aus dem Betrieb nehmen, stoppen und aktualisieren, dabei sicherstellen, dass er keinen Datenverkehr erhält, und ihn anschließend über den normalen Zugriffspfad testen, ohne ihn bereits öffentlich freizugeben. Dafür muss HAProxy nicht verändert werden. So können selbst komplexe Arbeiten im Produktionsbetrieb während der Geschäftszeiten durchgeführt werden, wenn alle technischen Ressourcen verfügbar sind.

Der Prozess geht möglichst sparsam mit Ressourcen um. Speicherpools verkürzen die Zuteilungszeit und begrenzen Fragmentierung. Nutzdatenpuffer werden freigegeben, sobald ihr Inhalt gesendet ist. Außerdem lassen sich feste Speichergrenzen erzwingen: Bei Erreichen der Grenze müssen Verbindungen auf einen freien Puffer warten, statt weiteren Speicher zuzuteilen. Damit lässt sich der Speicherverbrauch in Umgebungen mit strengen Vorgaben begrenzen.

Eine Befehlszeilenschnittstelle (CLI) steht über einen UNIX- oder TCP-Socket bereit, um Operationen auszuführen und Diagnoseinformationen abzurufen. Alle Aktionen über diesen Socket kommen ohne Konfigurationsänderung aus und dienen deshalb vorwiegend vorübergehenden Anpassungen. Über die Schnittstelle lassen sich Adresse, Gewicht und Status eines Servers ändern, Statistiken abfragen und Zähler zurücksetzen, Tabellen zur Sitzungspersistenz ausgeben und leeren, bei Bedarf anhand von Schlüsselkriterien gezielt auswählen, Verbindungen auf Client- und Serverseite ausgeben und beenden sowie erfasste Fehler mit genauer Ursachen- und Positionsanalyse anzeigen. Außerdem können ACL- und Map-Einträge ausgegeben, hinzugefügt und entfernt, gemeinsame TLS-Geheimnisse aktualisiert und Verbindungs- sowie Ratenbegrenzungen für beliebige Frontends zur Laufzeit angewendet werden, was bei gemeinsam genutztem Hosting nützlich ist. Ein einzelnes Frontend kann deaktiviert werden, um einen lauschenden Port freizugeben, etwa wenn tagsüber keine Betriebsänderungen erlaubt sind, aber dennoch eine Korrektur nötig ist. Auch Zertifikate und ihre Konfiguration lassen sich zur Laufzeit aktualisieren. Zudem können Traces aller Verarbeitungsschritte des Datenverkehrs aktiviert und eingesehen werden.

Für Umgebungen, die SNMP verlangen, gibt es mindestens zwei Agenten. Einer wird mit dem HAProxy-Quellcode geliefert und verwendet das Perl-Modul Net-SNMP. Ein weiterer gehört zu den kommerziellen Paketen und benötigt kein Perl. Ihr Funktionsumfang ist ungefähr gleich.

Häufig wird empfohlen, auf dem Rechner mit HAProxy 4 Werkzeuge zu installieren:

- socat für den Zugriff auf die CLI; manche netcat-Varianten können dies ebenfalls in gewissem Umfang;

- halog aus der neuesten HAProxy-Version: Das Werkzeug analysiert native TCP- und HTTP-Protokolle
  äußerst schnell, mit 1 bis 2 GB pro Sekunde. Es gewinnt daraus Informationen und Statistiken,
  etwa Anfragen pro URL oder Quelladresse, nach Antwortzeit oder Fehlerrate sortierte URLs und
  Abschlusscodes. Es wurde für Produktionsserver entwickelt, um Probleme im laufenden Betrieb
  zu untersuchen, und muss deshalb bereits einsatzbereit installiert sein;

- tcpdump wird dringend empfohlen, um Netzwerkmitschnitte für die Untersuchung von Problemen
  anzufertigen, die in den Protokollen sichtbar wurden. Irgendwann können sich die Sicht der
  Anwendung und die Analyse von haproxy widersprechen. Dann zeigen nur Netzwerkmitschnitte,
  welche Seite recht hat. Auch Fehler in Netzwerk-Stacks und Hypervisoren werden häufig mit
  tcpdump aufgedeckt;

- strace ergänzt tcpdump. Es zeigt, was HAProxy tatsächlich sieht, und hilft, Ursachen im
  Betriebssystem von Ursachen in HAProxy zu unterscheiden. Bei einem vermuteten HAProxy-Fehler
  wird häufig eine strace-Ausgabe angefordert;

## 3.5.2. Erweiterte Funktionen: Systemspezifische Fähigkeiten {#section-3-5-2}

Je nach Betriebssystem stehen zusätzliche Funktionen zur Verfügung oder werden benötigt. HAProxy unterstützt mehrere Plattformen, wird aber hauptsächlich unter Linux entwickelt. Deshalb sind einige Funktionen nur dort verfügbar.

Transparente Bindung und Verbindungsherstellung, die Bindung von Verbindungen an eine bestimmte Netzwerkschnittstelle sowie das Binden mehrerer Prozesse an dieselbe IP-Adresse und dieselben Ports stehen nur unter Linux und BSD zur Verfügung. Nur Linux verteilt eingehende Anfragen jedoch im Kernel auf die verfügbaren Prozesse.

Unter Linux gibt es weitere Funktionen und Optimierungen. Netzwerk-Namespaces, auch „Container“ genannt, erlauben es HAProxy, als Gateway zwischen allen Containern zu arbeiten. Für clientseitige Verbindungen können MSS, Netfilter-Markierungen und das IP-TOS-Feld gesetzt werden. Auf der lauschenden Seite wird TCP FastOpen unterstützt. TCP-User-Timeouts erlauben dem Kernel, Verbindungen schnell zu beenden, wenn er vor Ablauf der konfigurierten Zeitüberschreitung erkennt, dass der Client nicht mehr erreichbar ist. TCP-Splicing lässt den Kernel Daten zwischen den beiden Seiten einer Verbindung weiterleiten und vermeidet dadurch mehrere Kopien im Speicher. Mit der Bind-Option "defer-accept" wird eine eingehende Verbindung erst gemeldet, wenn Daten in den Kernel-Puffern vorliegen. Die Option "tcp-smart-connect" ermöglicht es, die Anfrage zusammen mit dem ACK zu senden, das den Verbindungsaufbau bestätigt; dies wird manchmal „Piggybacking“ genannt. Unter Linux steuert HAProxy zudem verzögerte TCP-ACKs sorgfältig, um möglichst viele Netzwerkpakete einzusparen.

Manche Systeme haben eine unzuverlässige Uhr, die vor- und zurückspringt. Früher trat dies bei einigen NUMA-Systemen auf, deren Prozessoren nicht dieselbe Uhrzeit sahen. In jüngerer Zeit ist es in virtualisierten Umgebungen häufiger geworden, in denen die virtuelle Uhr keinen Bezug zur tatsächlichen Uhr hat. Dadurch entstehen große Zeitsprünge, gelegentlich wurden bis zu 30 Sekunden beobachtet. Das verursacht generell erhebliche Probleme bei der Durchsetzung von Zeitüberschreitungen. HAProxy führt deshalb eine eigene monotone Uhr auf Grundlage der Systemuhr, misst aber deren Abweichungen und gleicht sie aus. Selbst mit einer sehr schlechten Systemuhr bleiben Timer so hinreichend genau, und Zeitüberschreitungen funktionieren weiterhin. Das Problem betrifft sämtliche Software auf solchen Systemen und ist nicht HAProxy-spezifisch. Typische Folgen sind unbegründete Zeitüberschreitungen oder eingefrorene Anwendungen. Wird dieses Verhalten festgestellt, muss es behoben werden, auch wenn HAProxy sich selbst dagegen schützt.

Unter Linux kann ein neu startender Prozess mit seinem Vorgänger kommunizieren und dessen lauschende Dateideskriptoren übernehmen. Dadurch werden die lauschenden Sockets beim Austausch des Prozesses zu keinem Zeitpunkt unterbrochen.

## 3.5.3. Erweiterte Funktionen: Skripte {#section-3-5-3}

HAProxy kann mit Unterstützung für die eingebettete Sprache Lua gebaut werden. Damit eröffnen sich viele Möglichkeiten für komplexe Änderungen an Anfragen und Antworten, Routingentscheidungen, Statistikverarbeitung und mehr. Mit Lua lassen sich sogar parallele Verbindungen zu anderen Servern aufbauen, um Informationen auszutauschen. So kann beispielsweise ein Authentifizierungssystem entwickelt werden, auch wenn dies aufwendig ist. Weitere Informationen zur Verwendung von Lua stehen in der Dokumentation in "doc/lua-api/index.rst".

## 3.5.4. Erweiterte Funktionen: Tracing {#section-3-5-4}

Administratoren können sich jederzeit über die CLI verbinden und Tracing für verschiedene interne Teilsysteme aktivieren. Mehrere voreingestellte Detailstufen erlauben in der Praxis Ausgaben von einer Zeile bis zu 500 Zeilen pro Anfrage. Filter und ein automatischer Mechanismus zum Starten, Stoppen und Pausieren der Erfassung ermöglichen es, gezielt auf ein Ereignis zu warten und es im Detail zu beobachten. Das ist besonders hilfreich bei Protokollverstößen fehlerhafter Server und Clients sowie bei Denial-of-Service-Angriffen.
