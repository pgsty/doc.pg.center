---
title: "Ergänzende Produkte und Alternativen"
linkTitle: "Ökosystem"
weight: 90
description: "Das Zusammenspiel von HAProxy mit Apache, NGINX, Varnish, LVS, Envoy und anderen Load-Balancern"
icon: fa-solid fa-puzzle-piece
module: [HAPROXY]
categories: [Konzept]
aliases:
  - /haproxy/intro/ecosystem/
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
upstream_name: "HAProxy 3.4 Starter Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, sections 4–4.4"
---

HAProxy lässt sich gut mit einigen der folgenden Produkte kombinieren. Deshalb werden sie hier erwähnt, auch wenn sie nicht direkt zu HAProxy gehören.

## 4.1. Apache HTTP Server {#section-4-1}

Apache ist der De-facto-Standard unter den HTTP-Servern. Das sehr umfangreiche, modulare Projekt unterstützt sowohl die Auslieferung von Dateien als auch dynamische Inhalte. Es kann als Frontend für Anwendungsserver dienen, Anfragen als Proxy weiterleiten und Antworten zwischenspeichern. In all diesen Fällen wird häufig ein vorgeschalteter Load-Balancer benötigt. Apache unterstützt verschiedene Betriebsarten mit unterschiedlichem Ressourcenbedarf. Manche Module verlangen weiterhin das aufwendigere Prefork-Modell und verhindern dadurch eine gute Skalierung bei vielen Verbindungen. HAProxy kann hier erheblich helfen, indem er die Verbindungszahl pro Server auf einen sicheren Wert begrenzt. Dadurch wird der Server deutlich schneller, und seine Ressourcen bleiben für die Anwendung verfügbar.

Apache kann die Clientadresse mit der Erweiterung "mod_rpaf" aus dem Header X-Forwarded-For auslesen. HAProxy setzt diesen Header automatisch, wenn "option forwardfor" konfiguriert ist. Außerdem kann HAProxy einen mit dem Internet verbundenen Apache gut schützen, da er vielen Arten von DoS-Angriffen besser standhält.

## 4.2. NGINX {#section-4-2}

NGINX ist der zweite De-facto-Standard unter den HTTP-Servern und deckt wie Apache viele Funktionen ab. Sein Modell ähnelt dem von HAProxy, sodass er problemlos Zehntausende gleichzeitige Verbindungen verarbeitet. Wird er als Gateway zu Anwendungen eingesetzt, etwa mit dem mitgelieferten PHP FPM, kann eine Begrenzung der Frontend-Verbindungen die PHP-Anwendung entlasten. HAProxy hilft dabei sowohl als gewöhnlicher Load-Balancer als auch bei der Regulierung des Datenverkehrs, um PHP durch weniger Überlastung zu beschleunigen. Da beide Produkte dank ihrer ereignisgesteuerten Architektur wenig CPU-Leistung benötigen, können sie oft problemlos auf demselben System installiert werden. NGINX implementiert das PROXY-Protokoll von HAProxy. So kann HAProxy die Verbindungsinformationen des Clients an NGINX weitergeben, damit die Anwendung alle relevanten Angaben erhält. Einige Benchmarks haben außerdem gezeigt, dass konsistentes Hashing in einem vor NGINX eingesetzten HAProxy bei der Auslieferung großer statischer Dateien vorteilhaft ist: Es verbessert die Cache-Trefferrate des Betriebssystems, die sich im Wesentlichen mit der Anzahl der Serverknoten vervielfacht.

## 4.3. Varnish {#section-4-3}

Varnish ist ein intelligenter Reverse-Proxy mit Cache, der sich am besten als Beschleuniger für Webanwendungen beschreiben lässt. Varnish implementiert kein SSL/TLS und konzentriert seine gesamte CPU-Leistung auf seine Kernaufgabe. Da auch Varnish das PROXY-Protokoll von HAProxy implementiert, lässt sich HAProxy einfach davor einsetzen, um SSL-Verarbeitung und Lastverteilung zu übernehmen und alle relevanten Clientinformationen weiterzugeben. Varnish kann komprimierte Objekte aus dem Cache dekomprimieren, wenn ein Server sie komprimiert geliefert hat, komprimiert sie aber nicht selbst. Unterstützen die Backend-Server keine Komprimierung, kann HAProxy die ausgehenden Daten komprimieren. Bei mehr als geringem Datenverkehr ist die Komprimierung auf dem Load-Balancer allerdings selten sinnvoll.

Bei großen Cache-Farmen mit mehreren Knoten kann HAProxy die Last durch konsistentes URL-Hashing gezielt auf die Cache-Knoten verteilen und doppelte Cache-Inhalte vermeiden. Die gesamte Cache-Kapazität entspricht dann der Summe aller Knoten. Zusätzlich kann das kurzzeitige Zwischenspeichern sehr kleiner, einfacher Objekte in HAProxy Netzwerk-Roundtrips einsparen und die CPU-Last auf HAProxy- und Varnish-Knoten senken. Dies ist nur möglich, wenn Varnish diese Objekte nicht weiter verarbeitet. Häufig wird dies als „Favicon-Cache“ bezeichnet; damit lässt sich unter Umständen ein erheblicher Anteil unnötiger nachgelagerter Anfragen vermeiden. Vor einem anderen Cache darf HAProxy jedoch nicht für längere Zeit, also mehr als wenige Sekunden, zwischenspeichern. Das würde die Fehlerbehebung erheblich erschweren, ohne nennenswerte zusätzliche Einsparungen zu bringen.

## 4.4. Alternativen {#section-4-4}

Linux Virtual Server, kurz LVS oder IPVS, ist der in den Linux-Kernel integrierte Load-Balancer für Schicht 4. Er arbeitet auf Paketebene und verarbeitet TCP und UDP. Meist ist er eher eine Ergänzung als eine Alternative, da er keinerlei Kenntnis von Schicht 7 hat.

Pound ist ein weiterer bekannter Load-Balancer. Er ist wesentlich einfacher und hat deutlich weniger Funktionen als HAProxy. Für viele sehr einfache Konfigurationen eignen sich jedoch beide. Sein Autor legt den Schwerpunkt seit jeher auf gut prüfbaren Code und möchte den Funktionsumfang klein halten. Die Architektur mit Threads skaliert bei hohen Verbindungszahlen weniger gut, dennoch ist Pound ein gutes Produkt.

Pen ist ein recht schlanker Load-Balancer. Er unterstützt SSL und hält Clientzuordnungen in einer Tabelle fester Größe mit den IP-Adressen der Clients. Ein paketorientierter Modus ermöglicht Direct Server Return und in gewissem Umfang UDP. Pen ist für geringe Last ausgelegt; die Zuordnungstabelle enthält nur 2048 Einträge.

NGINX kann in gewissem Umfang Last verteilen, auch wenn dies eindeutig nicht seine Hauptaufgabe ist. Serverausfälle werden anhand des Produktionsverkehrs erkannt, die Verfahren zur Lastverteilung sind eingeschränkter, und die Sitzungspersistenz ist sehr begrenzt. In einfachen Bereitstellungen, in denen NGINX bereits vorhanden ist, kann dies dennoch sinnvoll sein. Da NGINX gut mit HAProxy zusammenarbeitet, lässt sich HAProxy problemlos später ergänzen, wenn die Grenzen erreicht sind.

Auch Varnish verteilt Last auf seine Backend-Server und unterstützt echte Health Checks. Sitzungspersistenz implementiert es jedoch nicht. Wie bei NGINX kann dies für den Anfang ausreichen, solange keine Sitzungspersistenz benötigt wird. Da HAProxy und Varnish sehr gut zusammenarbeiten, lässt sich HAProxy auch hier später leicht ergänzen, um den Funktionsumfang zu erweitern.
