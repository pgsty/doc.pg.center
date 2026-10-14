---
title: "Was HAProxy ist und wie es funktioniert"
linkTitle: "Architektur"
weight: 30
description: "Aufgaben, Grenzen, ereignisgesteuerte Architektur und Anfrageverarbeitung von HAProxy"
icon: fa-solid fa-diagram-project
module: [HAPROXY]
categories: [Konzept]
aliases:
  - /haproxy/introduction/
  - /haproxy/intro/architecture/
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
upstream_name: "HAProxy 3.4 Starter Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, sections 3–3.2"
---

Die Schreibweise "HAProxy" bezeichnet das Produkt, "haproxy" dagegen das ausführbare Programm, das Softwarepaket oder einen Prozess. Häufig werden beide Schreibweisen jedoch für beide Bedeutungen verwendet; ausgesprochen werden sie H-A-Proxy. Ursprünglich stand "haproxy" für „High Availability Proxy“, und der Name wurde in zwei getrennten Wörtern geschrieben. Heute bedeutet er ausschließlich "HAProxy".

## 3.1. Was HAProxy ist und was nicht {#section-3-1}

HAProxy ist:

- ein TCP-Proxy: Er nimmt TCP-Verbindungen über einen lauschenden Socket an, verbindet sich mit
  einem Server und verknüpft beide Sockets für die bidirektionale Datenübertragung. Auf beiden
  Seiten werden IPv4, IPv6 und sogar UNIX-Sockets unterstützt. Dadurch lassen sich Adressen
  verschiedener Familien einfach ineinander überführen.

- ein HTTP-Reverse-Proxy, in der HTTP-Terminologie ein „Gateway“: Er tritt als Server auf, empfängt
  HTTP-Anfragen über Verbindungen eines lauschenden TCP-Sockets und leitet sie über andere
  Verbindungen an Server weiter. Auf beiden Seiten ist jede Kombination aus HTTP/1.x und HTTP/2
  möglich. Bei ALPN über TLS erkennt er das verwendete Protokoll auf jeder Seite automatisch.

- ein System zum Terminieren, Initiieren und Auslagern von SSL: SSL/TLS kann auf der Verbindung
  vom Client, auf der Verbindung zum Server oder auf beiden verwendet werden. Viele Einstellungen
  lassen sich je Name über SNI festlegen und ohne Neustart zur Laufzeit ändern. Solche
  Konfigurationen skalieren sehr gut; es gibt Berichte über Zehntausende bis Hunderttausende
  eingesetzte Zertifikate.

- ein TCP-Normalisierer: Da das Betriebssystem die Verbindungen lokal terminiert, besteht kein
  Zusammenhang zwischen beiden Seiten. Ungültige Pakete, Flag-Kombinationen, Fensterankündigungen,
  Sequenznummern, unvollständige Verbindungen bei SYN-Floods und anderer ungewöhnlicher Datenverkehr
  gelangen daher nicht auf die Gegenseite. Dies schützt anfällige TCP-Stacks vor Protokollangriffen
  und erlaubt eine Optimierung der Verbindung zum Client, ohne den TCP-Stack der Server anzupassen.

- ein HTTP-Normalisierer: Bei aktivierter HTTP-Verarbeitung leitet er nur gültige, vollständige
  Anfragen weiter und schützt damit vor vielen Protokollangriffen. Außerdem korrigiert er
  Abweichungen, für die die Spezifikation Toleranz vorsieht, etwa mehrzeilige Header, damit sie
  auf den Servern keine Probleme verursachen.

- ein Werkzeug zur Korrektur von HTTP: Er kann die URL sowie beliebige Anfrage- oder Antwort-Header
  ändern, korrigieren, ergänzen, entfernen oder umschreiben. Das hilft bei
  Interoperabilitätsproblemen in komplexen Umgebungen.

- ein inhaltsabhängiger Verteiler: Anhand beliebiger Merkmale einer Anfrage entscheidet er, an
  welchen Server die Anfrage oder Verbindung geht. So können mehrere Protokolle wie HTTP, HTTPS
  und SSH über denselben Port verarbeitet werden.

- ein Load-Balancer für Server: Er verteilt TCP-Verbindungen und HTTP-Anfragen. Im TCP-Modus gilt
  die Entscheidung für die gesamte Verbindung, im HTTP-Modus für jede einzelne Anfrage.

- ein Regler für den Datenverkehr: Er begrenzt Raten an verschiedenen Stellen, schützt Server vor
  Überlastung und passt Prioritäten anhand des Inhalts an. Durch Paketmarkierungen kann er diese
  Informationen sogar an niedrigere Schichten und externe Netzwerkkomponenten weitergeben.

- ein Schutz gegen DDoS und Dienstmissbrauch: Er führt zahlreiche Statistiken etwa je IP-Adresse,
  URL oder Cookie, erkennt Missbrauch und reagiert darauf, indem er Verursacher verlangsamt,
  blockiert oder auf veraltete Inhalte umleitet.

- ein Beobachtungspunkt für die Netzwerkdiagnose: Die präzisen Protokollangaben werden häufig
  verwendet, um Netzwerkprobleme einzugrenzen.

- ein System zum Auslagern der HTTP-Komprimierung: Er komprimiert Antworten, die der Server
  unkomprimiert liefert, und verkürzt dadurch die Ladezeit bei schlechter Anbindung oder in
  Mobilfunknetzen mit hoher Latenz.

- ein Proxy mit Cache: Er kann Antworten im RAM zwischenspeichern. Solange ein Objekt vorhanden
  und gültig ist, entfällt bei weiteren Anfragen die erneute Netzwerkübertragung vom Server.
  Auf dauerhaftem Speicher legt er jedoch keine Objekte ab. Diese Cache-Funktion ist wartungsfrei
  ausgelegt und soll ausschließlich die wertvollen Ressourcen von haproxy schonen, nicht die des
  Servers. Caches zur Serveroptimierung benötigen erheblich mehr Einstellmöglichkeiten und
  Flexibilität. Wird ein solcher umfassender Cache benötigt, sollte Varnish Cache verwendet
  werden. Es lässt sich besonders bei SSL/TLS auf einer der beiden Seiten hervorragend mit
  haproxy kombinieren.

- ein FastCGI-Gateway: FastCGI lässt sich als andere Darstellung von HTTP auffassen. HAProxy kann
  deshalb die Last direkt auf eine beliebige Kombination von FastCGI-Anwendungsservern verteilen,
  ohne eine weitere Gateway-Schicht einzufügen. Das spart Ressourcen und senkt den Wartungsaufwand.

HAProxy ist nicht:

- ein expliziter HTTP-Proxy, über den Browser auf das Internet zugreifen. Dafür gibt es sehr gute
  Open-Source-Programme wie Squid. HAProxy kann jedoch davor eingesetzt werden, um Lastverteilung
  und Hochverfügbarkeit bereitzustellen.

- ein Werkzeug zur Bereinigung von Daten: Es ändert weder Anfrage- noch Antwortkörper.

- ein Server für statische Webseiten: Beim Start isoliert es sich in einer chroot-Umgebung und
  gibt Berechtigungen ab. Danach greift es nicht mehr auf das Dateisystem zu und kann deshalb
  nicht als statischer Webserver eingesetzt werden. Dynamische Server werden jedoch über FastCGI
  unterstützt. Für statische Inhalte gibt es sehr gute Open-Source-Programme wie Apache oder NGINX.
  HAProxy lässt sich einfach davor einsetzen, um Lastverteilung, Hochverfügbarkeit und Beschleunigung
  bereitzustellen.

- ein paketbasierter Load-Balancer: Es sieht weder IP-Pakete noch UDP-Datagramme und führt weder
  NAT noch DSR aus. Das sind Aufgaben niedrigerer Schichten. Kernel-Komponenten wie IPVS,
  Linux Virtual Server, erledigen dies bereits sehr gut und ergänzen HAProxy hervorragend.

## 3.2. Wie HAProxy arbeitet {#section-3-2}

HAProxy arbeitet ereignisgesteuert und nicht blockierend. Es verbindet eine sehr schnelle I/O-Schicht mit einem prioritätsgesteuerten Scheduler für mehrere Threads. Seine auf Datenweiterleitung ausgerichtete Architektur bewegt Daten mit möglichst wenigen Operationen so schnell wie möglich. Um CPU-Caches effizient zu nutzen, bleiben Verbindungen möglichst lange derselben CPU zugeordnet. Ein Schichtenmodell mit Umgehungsmöglichkeiten auf jeder Ebene sorgt dafür, dass Daten höhere Ebenen nur bei Bedarf erreichen. Der Großteil der Verarbeitung findet im Kernel statt. HAProxy unterstützt ihn dabei durch Hinweise und verzichtet auf manche Operationen, wenn sie voraussichtlich später zusammengefasst werden können. Typischerweise entfallen daher im TCP- oder HTTP-Close-Modus 15% der Verarbeitungszeit auf HAProxy und 85% auf den Kernel; im HTTP-Keep-Alive-Modus sind es etwa 30% für HAProxy und 70% für den Kernel.

Ein einzelner Prozess kann viele Proxy-Instanzen ausführen. Berichten zufolge funktionieren selbst Konfigurationen mit 300000 verschiedenen Proxys in einem Prozess problemlos. Ein System mit einer CPU und einem Kern reicht für mehr als 99% der Nutzer deutlich aus. Für Container und virtuelle Maschinen werden deshalb die kleinstmöglichen Images empfohlen, um Betriebskosten zu sparen und die Fehlerbehebung zu vereinfachen. Der Rechner, auf dem HAProxy läuft, darf jedoch niemals auslagern. Seine CPU darf weder künstlich gedrosselt werden, etwa durch Zuweisung eines CPU-Anteils im Hypervisor, noch mit rechenintensiven Prozessen geteilt werden, die eine hohe Latenz bei Kontextwechseln verursachen.

Mit einem Thread pro CPU-Kern kann HAProxy die gesamte verfügbare Rechenleistung nutzen. Dies ist vor allem für SSL oder Weiterleitungsraten über 40 Gbps hilfreich. Dabei muss Kommunikation zwischen mehreren physischen CPUs unbedingt vermieden werden, da sie starke Engpässe im Netzwerk-Stack und in HAProxy selbst verursachen kann. Auch wenn es zunächst widersprüchlich erscheint, sollte bei Leistungsproblemen oft zuerst die Anzahl der von HAProxy verwendeten CPUs reduziert werden.

Zum Betrieb benötigt HAProxy nur die ausführbare Datei haproxy und eine Konfigurationsdatei. Für die Protokollierung werden ein korrekt eingerichteter syslog-Daemon und eine Protokollrotation dringend empfohlen. Protokolle können auch an stdout/stderr gesendet werden, was in Containern nützlich ist. HAProxy liest die Konfigurationsdateien vor dem Start ein und versucht anschließend, alle lauschenden Sockets zu binden. Scheitert etwas, verweigert er den Start. Danach kann HAProxy nicht mehr fehlschlagen. Es treten also keine Laufzeitfehler auf: Wenn HAProxy startet, arbeitet es, bis es gestoppt wird.

Nach dem Start erledigt HAProxy genau 3 Aufgaben:

- eingehende Verbindungen verarbeiten;

- regelmäßig den Zustand der Server prüfen, die sogenannten Health Checks;

- Informationen mit anderen haproxy-Knoten austauschen.

Die Verarbeitung eingehender Verbindungen ist wegen der vielen Konfigurationsmöglichkeiten mit Abstand die komplexeste Aufgabe. Sie lässt sich aber in die folgenden 9 Schritte zusammenfassen:

- Eingehende Verbindungen über lauschende Sockets annehmen. Diese gehören zu einer
  Konfigurationseinheit namens "frontend", die eine oder mehrere lauschende Adressen referenziert;

- die Regeln des Frontends auf diese Verbindungen anwenden. Dabei können Verbindungen blockiert,
  Header geändert oder Verbindungen für interne Applets wie die Statistikseite oder CLI abgefangen werden;

- die eingehenden Verbindungen an eine weitere Konfigurationseinheit namens "backend" übergeben.
  Sie stellt eine Serverfarm dar und enthält deren Serverliste und Lastverteilungsstrategie;

- die Regeln des Backends auf diese Verbindungen anwenden;

- anhand der Lastverteilungsstrategie den Zielserver für die Verbindung wählen;

- die Regeln des Backends auf die Antwortdaten anwenden;

- die Regeln des Frontends auf die Antwortdaten anwenden;

- den Ablauf detailliert protokollieren;

- bei HTTP zum zweiten Schritt zurückkehren und auf eine neue Anfrage warten, andernfalls die
  Verbindung schließen.

Frontends und Backends werden manchmal als halbe Proxys betrachtet, weil sie jeweils nur eine Seite einer durchgehenden Verbindung abdecken: Das Frontend kümmert sich um die Clients, das Backend um die Server. HAProxy unterstützt außerdem vollständige Proxys, die Frontend und Backend exakt vereinen. Für HTTP wird die Konfiguration meist in Frontends und Backends aufgeteilt. Da jedes Frontend eine Verbindung an jedes Backend übergeben kann, eröffnet dies viele Möglichkeiten. Bei reinen TCP-Proxys bringt diese Trennung selten Vorteile; vollständige Proxys können die Konfiguration dann übersichtlicher machen.
