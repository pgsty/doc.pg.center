---
title: "Grundlagen der Lastverteilung"
linkTitle: "Lastverteilung"
weight: 20
description: "Grundlagen der Lastverteilung auf Paket-, Netzwerk- und Serverebene sowie auf L4 und L7"
icon: fa-solid fa-scale-balanced
module: [HAPROXY]
categories: [Konzept]
aliases:
  - /haproxy/intro/load-balancing/
  - /haproxy/intro/
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
upstream_name: "HAProxy 3.4 Starter Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 2"
---

Dieses Dokument führt in HAProxy ein, sowohl für neue Nutzer als auch für diejenigen, die ältere Versionen kennen und sich erneut damit vertraut machen möchten. Es liefert vor allem die Informationen, mit denen sich beurteilen lässt, ob HAProxy für die eigenen Anforderungen geeignet ist. Erfahrene Nutzer finden hier möglicherweise Lösungsansätze für bisherige Ideen, weil ihnen eine neue Funktion noch nicht bekannt war. Darüber hinaus behandelt das Dokument die Dimensionierung und den Produktlebenszyklus und vergleicht HAProxy mit Produkten, deren Funktionen sich teilweise überschneiden.

Das Dokument bietet keine Hilfe oder Hinweise zur Konfiguration, verweist aber auf die dafür geeignete Dokumentation. Der Leitfaden ist in der HAProxy-Seitenleiste als flache Folge von Themenseiten angeordnet.

Lastverteilung fasst mehrere Komponenten so zusammen, dass ihre gesamte Verarbeitungskapazität die Kapazität jeder einzelnen übersteigt. Dies erfolgt skalierbar und ohne Eingriff des Endnutzers. In der Zeit, die eine Komponente für eine Operation benötigt, können dadurch mehrere Operationen gleichzeitig ausgeführt werden. Eine einzelne Operation läuft jedoch weiterhin jeweils auf nur einer Komponente und wird durch die Lastverteilung nicht schneller. Um alle Komponenten zu nutzen und vollständig von der Lastverteilung zu profitieren, müssen stets mindestens so viele Operationen wie Komponenten sowie ein effizientes Verteilungsverfahren vorhanden sein. Ein anschauliches Beispiel sind mehrere Fahrspuren einer Autobahn: In derselben Zeit können mehr Autos passieren, ohne dass sich ihre individuelle Geschwindigkeit erhöht.

Beispiele für Lastverteilung:

- Prozessplanung in Mehrprozessorsystemen
- Lastverteilung auf Verbindungen, etwa EtherChannel oder Bonding
- Lastverteilung über IP-Adressen, etwa ECMP oder DNS-Round-Robin
- Lastverteilung auf Server durch Load-Balancer

Das Verfahren oder die Komponente, die die Last verteilt, heißt Load-Balancer. In Webumgebungen spricht man von einem Netzwerk-Load-Balancer oder meist einfach von einem Load-Balancer, da dies der mit Abstand bekannteste Anwendungsfall der Lastverteilung ist.

Ein Load-Balancer kann auf verschiedenen Ebenen arbeiten:

- auf Verbindungsebene: Er wählt aus, über welche Netzwerkverbindung ein Paket gesendet wird;

- auf Netzwerkebene: Er bestimmt die Route, der eine Folge von Paketen folgt;

- auf Serverebene: Er entscheidet, welcher Server eine Verbindung oder Anfrage verarbeitet.

Es gibt zwei unterschiedliche Technologien für verschiedene, teilweise überlappende Anforderungen. In beiden Fällen ist zu beachten, dass Lastverteilung den Datenverkehr von seinem natürlichen Weg ablenkt. Dies verlangt stets eine gewisse Sorgfalt, damit alle Routingentscheidungen ausreichend konsistent bleiben.

Die erste Technologie arbeitet auf Paketebene und verarbeitet Pakete mehr oder weniger einzeln. Zwischen eingehenden und ausgehenden Paketen besteht eine 1:1-Beziehung, sodass sich der Datenverkehr auf beiden Seiten des Load-Balancers mit einem gewöhnlichen Netzwerkmitschnitt verfolgen lässt. Dieses Verfahren kann sehr günstig und extrem schnell sein. Meist wird es in Hardware mit ASICs umgesetzt und erreicht Leitungsgeschwindigkeit, etwa in Switches mit ECMP. Gewöhnlich ist es zustandslos, kann aber auch die Sitzung berücksichtigen, zu der ein Paket gehört, und damit zustandsbehaftet arbeiten; dies wird als layer4-LB oder L4 bezeichnet. Wenn die Pakete unverändert bleiben, kann DSR unterstützt werden: Der Server antwortet direkt, ohne erneut den LB zu durchlaufen. Den Inhalt kennt dieses Verfahren jedoch kaum. Es eignet sich sehr gut zur Lastverteilung auf Netzwerkebene, wird aber gelegentlich auch für sehr einfache, schnelle Lastverteilung auf Server verwendet.

Die zweite Technologie verarbeitet den Inhalt von Sitzungen. Dazu muss sie eingehende Datenströme zusammensetzen und als Ganzes verarbeiten. Der Inhalt kann geändert werden; der ausgehende Datenstrom wird anschließend in neue Pakete zerlegt. Deshalb übernehmen meist Proxys diese Aufgabe, die oft Load-Balancer für Schicht 7 oder L7 genannt werden. Auf beiden Seiten bestehen getrennte Verbindungen. Zwischen Größe und Anzahl der eingehenden und ausgehenden Pakete gibt es keinen Zusammenhang. Clients und Server müssen nicht dasselbe Protokoll verwenden, etwa IPv4 statt IPv6 oder Klartext statt SSL. Die Verarbeitung ist immer zustandsbehaftet, und der Rückverkehr muss den Load-Balancer durchlaufen. Der zusätzliche Aufwand kann verhindern, dass Leitungsgeschwindigkeit erreicht wird, besonders bei kleinen Paketen. Dafür bietet das Verfahren viele Möglichkeiten und wird meist vollständig in Software umgesetzt, auch innerhalb von Hardware-Appliances. Es eignet sich sehr gut zur Lastverteilung auf Server.

Paketbasierte Load-Balancer werden meist im Durchleitungsmodus eingesetzt: Sie liegen auf dem normalen Verkehrsweg und lenken Pakete gemäß ihrer Konfiguration um. Der Rückverkehr muss sie nicht zwingend passieren. Wird jedoch die Netzwerkzieladresse geändert, um den Datenverkehr zum richtigen Ziel zu führen, muss der Rückverkehr durch den Load-Balancer laufen. Erlaubt das Routing dies nicht, kann der Load-Balancer zusätzlich die Quelladresse der Pakete durch seine eigene ersetzen und den Rückweg dadurch erzwingen.

Proxy-basierte Load-Balancer werden ohne Architekturänderung als Server mit eigenen IP-Adressen und Ports eingesetzt. Manchmal müssen Anwendungen angepasst werden, damit Clients die IP-Adresse des Load-Balancers statt direkt die des Servers verwenden. Dafür müssen manche Load-Balancer Serverantworten verändern, etwa das HTTP-Headerfeld Location bei HTTP-Weiterleitungen. Einige Proxy-basierte Load-Balancer können auch Datenverkehr für fremde Adressen abfangen und beim Verbindungsaufbau zum Server die Clientadresse verwenden. Dadurch lassen sie sich wie gewöhnliche Router oder Firewalls im Durchleitungsmodus einsetzen, ähnlich paketbasierten Load-Balancern. Dies ist besonders bei Produkten beliebt, die Paket- und Proxy-Modus kombinieren. DSR ist dabei selbstverständlich weiterhin nicht möglich; der Rückverkehr muss zum Load-Balancer geroutet werden.

Ein sehr gut skalierbarer Schichtenaufbau kann mit einem vorgeschalteten Router beginnen, der Datenverkehr über mehrere lastverteilte Verbindungen empfängt. Über ECMP verteilt er diesen auf eine erste Schicht mehrerer zustandsbehafteter, paketbasierter L4-Load-Balancer. Diese L4-Load-Balancer leiten ihn an eine noch größere Anzahl Proxy-basierter L7-Load-Balancer weiter, die den Inhalt auswerten und den endgültigen Zielserver bestimmen.

Mit der Anzahl der Komponenten und möglichen Verkehrswege steigt das Ausfallrisiko. In sehr großen Umgebungen ist es sogar normal, dass ständig einige defekte Komponenten repariert oder ersetzt werden. Lastverteilung ohne Kenntnis des Zustands des gesamten Systems verschlechtert die Verfügbarkeit erheblich. Jeder sinnvoll ausgelegte Load-Balancer prüft deshalb, ob seine Zielkomponenten noch aktiv und erreichbar sind, und sendet keinen Datenverkehr mehr an fehlerhafte Komponenten. Dafür gibt es verschiedene Verfahren.

Am häufigsten werden regelmäßig Prüfanfragen gesendet, um die Funktionsfähigkeit einer Komponente festzustellen. Diese Prüfungen heißen Health Checks und müssen die zu erkennenden Fehler abbilden. Ein Ping erkennt beispielsweise nicht, dass ein Webserver abgestürzt ist und nicht mehr auf einem Port lauscht. Ein Verbindungsversuch zu diesem Port erkennt dies dagegen. Eine weitergehende Anfrage kann sogar prüfen, ob der Server noch funktioniert und auf seine Datenbank zugreifen kann. Health Checks wiederholen die Prüfung oft einige Male, um gelegentliche Messfehler abzufangen. Das Prüfintervall muss kurz genug sein, damit eine fehlerhafte Komponente nach einem Ausfall nicht zu lange weiterverwendet wird.

Andere Verfahren beobachten Stichproben des an ein Ziel gesendeten Produktionsverkehrs und entfernen Komponenten, die unpassende Antworten liefern. Dabei wird allerdings ein Teil des Produktionsverkehrs beeinträchtigt, was nicht immer akzeptabel ist. Die Kombination beider Verfahren verbindet ihre Vorteile: Beide erkennen Fehler, aber nur Health Checks erkennen deren Behebung. Ein weiteres Verfahren nutzt zentrale Zustandsmeldungen. Ein zentraler Überwachungsagent informiert alle Load-Balancer regelmäßig über den Zustand sämtlicher Komponenten. Alle erhalten damit eine Gesamtsicht auf die Infrastruktur, allerdings mitunter weniger genau oder verzögert. Dieses Verfahren eignet sich besonders für Umgebungen mit vielen Load-Balancern und Servern.

Load-Balancer für Schicht 7 müssen außerdem Sitzungspersistenz gewährleisten, auch als Stickiness bezeichnet. Mehrere aufeinanderfolgende Anfragen oder Verbindungen derselben Quelle, etwa eines Endnutzers, müssen dabei meist dasselbe Ziel erreichen. Das bekannteste Beispiel ist der Warenkorb eines Onlineshops. Erzeugt jeder Klick eine neue Verbindung, muss der Nutzer stets zu dem Server gelangen, auf dem sein Warenkorb liegt. Die Auswertung des Inhalts erleichtert es, Merkmale der Anfrage zur Bestimmung des Zielservers zu verwenden, reicht aber nicht immer aus. Wird beispielsweise die Quelladresse als Schlüssel verwendet, kann ein Hash-Verfahren jede IP-Adresse anhand einer Division durch die Anzahl verfügbarer Server stets demselben Server zuordnen. Fällt jedoch ein Server aus, ändert sich das Ergebnis. Plötzlich gelangen alle Nutzer zu einem anderen Server und verlieren ihren Warenkorb. Die Lösung besteht darin, das gewählte Ziel zu speichern und denselben Besucher unabhängig von der Anzahl verfügbarer Server immer dorthin zu leiten. Diese Information kann im Speicher des Load-Balancers liegen und muss bei mehreren Load-Balancern gegebenenfalls repliziert werden. Alternativ kann sie auf verschiedene Weise beim Client gespeichert werden, sofern dieser sie bei jeder Anfrage wieder übermittelt, etwa durch eingefügte Cookies oder eine Weiterleitung auf eine Subdomain. Zusätzlich entfällt damit die Abhängigkeit von instabilen oder ungleich verteilten Merkmalen wie der Quell-IP-Adresse. Dies ist der wichtigste Grund für einen Load-Balancer auf Schicht 7 statt auf Schicht 4.

Um Cookies, das Host-Headerfeld, URLs oder andere Informationen auszulesen, muss ein Load-Balancer SSL/TLS-Datenverkehr möglicherweise entschlüsseln und beim Weiterleiten an den Server wieder verschlüsseln. Dieser hohe Aufwand erklärt, weshalb manche stark ausgelasteten Infrastrukturen sehr viele Load-Balancer benötigen.

Ein Load-Balancer für Schicht 7 führt zahlreiche komplexe Operationen aus, etwa Entschlüsselung, Auswertung und Änderung des Inhalts, Cookie-Abgleich und Serverauswahl. Dabei kann er durchaus Probleme verursachen. Häufig wird er jedoch für Probleme verantwortlich gemacht, die er lediglich sichtbar gemacht hat. Oft stellt sich heraus, dass Server instabil sind und regelmäßig ausfallen, dass Webseiten fest eingebaute Links enthalten, die Clients am Load-Balancer vorbei direkt zu einem bestimmten Server führen, oder dass Server unter hoher Last so langsam antworten, dass Zeitüberschreitungen entstehen. Deshalb ist die Protokollierung bei Lastverteilung auf Schicht 7 äußerst wichtig. Sobald ein Problem gemeldet wird, ist es wichtig zu klären, ob der Load-Balancer falsch entschieden hat und gegebenenfalls warum, damit es nicht erneut passiert.
