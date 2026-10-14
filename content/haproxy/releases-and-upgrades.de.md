---
title: "Versionen, Pakete und Upgrades"
linkTitle: "Versionen und Upgrades"
weight: 80
description: "Stabile Zweige, Bezugsquellen, Versionsbestimmung, Wartung und Upgrades"
icon: fa-solid fa-code-branch
module: [HAPROXY]
categories: [Aufgabe]
aliases:
  - /haproxy/intro/releases-and-upgrades/
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
upstream_name: "HAProxy 3.4 Starter Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 3.7"
---

HAProxy ist ein Open-Source-Projekt unter der GPLv2-Lizenz. Jeder darf es weiterverbreiten, sofern auf Anfrage auch Zugang zum Quellcode gewährt wird, insbesondere wenn Änderungen vorgenommen wurden.

Die Entwicklung von HAProxy erfolgt im Hauptzweig "master", auch "mainline" genannt. Sobald der Code als stabil gilt, werden daraus neue Zweige abgeleitet. Viele Websites setzen freiwillig Entwicklungszweige im Produktionsbetrieb ein, entweder um zum Projekt beizutragen oder weil sie eine besonders neue Funktion benötigen. Ihre Rückmeldungen sind sehr wertvoll, um Fehler zu beheben und die Gesamtqualität und Stabilität der entstehenden Version einzuschätzen.

Die aus ausreichend stabilem Code erzeugten neuen Zweige bilden eine stabile Version und werden im Allgemeinen mehrere Jahre gepflegt. Ein sofortiger Wechsel auf einen neueren Zweig ist daher auch dann nicht nötig, wenn nicht der neueste verwendet wird. Nach der Veröffentlichung eines stabilen Zweigs darf er nur Fehlerkorrekturen erhalten. Sehr selten kommen kleinere Funktionserweiterungen hinzu, wenn sie den Nutzern die Arbeit erleichtern. Alle Korrekturen eines stabilen Zweigs stammen zwingend aus dem master-Zweig. Dadurch geht beim Upgrade keine Korrektur verloren. Patches zur Fehlerbehebung bitte deshalb gegen master und nicht gegen einen stabilen Zweig erstellen. Möglicherweise ist der Fehler dort bereits behoben. Dieses Verfahren sorgt zudem dafür, dass Regressionen in stabilen Zweigen äußerst selten sind. Es gibt daher keinen Grund, nicht auf die neueste Version des verwendeten Zweigs zu aktualisieren.

Zweige tragen zwei durch einen Punkt getrennte Zahlen, etwa "1.6". Seit 1.9 konzentrieren sich Zweige mit ungerader zweiter Zahl vor allem auf sensible technische Änderungen und richten sich eher an erfahrene Nutzer, da sie wahrscheinlich mehr Fehler auslösen als die übrigen. Sie werden nur etwa ein Jahr gepflegt und dürfen nicht dort eingesetzt werden, wo im Notfall kein Rollback möglich ist. Eine vollständige Versionsnummer enthält eine oder zwei weitere Zahlen für den Korrekturstand. Beispielsweise ist 1.5.14 die 14. Korrekturversion im Zweig 1.5 nach der Veröffentlichung von 1.5.0. Sie enthält 126 Korrekturen einzelner Fehler, 24 Dokumentationsaktualisierungen und 75 weitere rückportierte Patches, von denen die meisten zur Behebung der genannten 126 Fehler benötigt wurden. Bestehende Funktionen dürfen in einem stabilen Zweig niemals geändert oder entfernt werden. So bleiben Upgrades innerhalb desselben Zweigs stets unbedenklich.

HAProxy ist aus verschiedenen Quellen mit unterschiedlichen Veröffentlichungsrhythmen verfügbar:

- Die offizielle Community-Website <http://www.haproxy.org/> bietet den Quellcode der neuesten
  Entwicklungsversion, sämtlicher stabiler Versionen sowie nächtliche Snapshots jedes Zweigs.
  Der Veröffentlichungsrhythmus ist langsam: Zwischen stabilen Versionen oder Entwicklungssnapshots
  liegen mehrere Monate. Auch sehr alte Versionen werden dort noch unterstützt. Alles wird nur
  als Quellcode bereitgestellt und muss daher selbst gebaut beziehungsweise paketiert werden;

- GitHub unter <https://github.com/haproxy/haproxy/> spiegelt ausschließlich den Entwicklungszweig
  und bindet Issue-Tracker, kontinuierliche Integration und Werkzeuge zur Messung der Codeabdeckung ein.
  Dieses Angebot richtet sich ausschließlich an Mitwirkende;

- Zahlreiche Betriebssysteme, etwa Linux-Distributionen und BSD-Ports, liefern langfristig gepflegte
  Versionen. Diese enthalten nicht immer alle Korrekturen der offiziellen Versionen, aber zumindest
  die kritischen. Für die meisten Nutzer, die keine anspruchsvollen Konfigurationen benötigen und
  Aktualisierungen einfach halten möchten, ist dies häufig eine gute Wahl;

- Kommerzielle Versionen von <http://www.haproxy.com/> bieten professionell unterstützte Pakete
  für verschiedene Betriebssysteme oder Appliances. Sie basieren auf aktuellen stabilen Versionen
  und enthalten zusätzlich stark nachgefragte Funktionen, die aus der nächsten Version rückportiert
  wurden. Sie sind die beste Wahl für Nutzer, die neue Funktionen mit der Zuverlässigkeit eines
  stabilen Zweigs, sehr schnelle Fehlerbehebung oder einfach einen Supportvertrag für ein
  Open-Source-Produkt suchen;

Um festzustellen, ob die eingesetzte Version die neueste ihres Zweigs ist, wie folgt vorgehen:

- Prüfen, welche ausführbare HAProxy-Datei verwendet wird. Manche Systeme liefern HAProxy bereits
  mit, während die Administration eine eigene Version an anderer Stelle installiert. Daher in den
  Startskripten nachsehen, welche Datei tatsächlich aufgerufen wird;

- Die Herkunft der HAProxy-Version bestimmen. Meist genügt "haproxy -v". Eine Entwicklungsversion
  sieht wie folgt aus; hinter der Zweignummer steht "dev":

```text
HAProxy version 2.4-dev18-a5357c-137 2021/05/09 - https://haproxy.org/
```

    Eine stabile Version sieht wie folgt aus. Dasselbe gilt für unveränderte stabile

Versionen der Betriebssystemanbieter:

```text
HAProxy version 1.5.14 2015/07/02
```

    Ein nächtlicher Snapshot einer stabilen Version enthält dagegen eine hexadezimale
    Zeichenfolge hinter der Versionsnummer und statt des Veröffentlichungsdatums

das Datum des Snapshots:

```text
HAProxy version 1.5.14-e4766ba 2015/07/29
```

    Jedes andere Format kann auf ein systemspezifisches Paket mit eigenen Patches hinweisen.
    HAProxy-Enterprise-Versionen verwenden beispielsweise

folgendes Format (`<branch>`-`<latest commit>`-`<revision>`):

```text
HAProxy version 1.5.0-994126-357 2015/07/02
```

    Frühere Versionen vor 2.4 gaben den Prozessnamen mit einem Bindestrich zwischen "HA" und
    "Proxy" aus. Dies gilt auch für die oben gezeigten Beispiele, die nur zur Darstellung des
    korrekten Formats angepasst wurden. In Skripten dieses Wort daher besser ignorieren oder
    einen weniger strengen Abgleich verwenden. Neuere Versionen ergänzen zudem eine URL zur
    Projektwebsite.

    Ab Version 2.1 gibt es außerdem eine Zeile "Status". Sie nennt, ob die Version für den
    Produktionsbetrieb geeignet ist und gegebenenfalls bis wann, sowie einen Link zur Liste
    bekannter Fehler dieser Version.

- Bei systemspezifischen Paketen im Paket-Repository oder Aktualisierungssystem des Anbieters
  prüfen, ob das System noch unterstützt wird und der verwendete Zweig weiterhin Korrekturen erhält.
  Bei Community-Versionen von haproxy.org die Website besuchen, den Status des Zweigs prüfen und
  die neueste Version mit der installierten vergleichen. Ist die eigene Version älter, kann sie
  aktualisiert werden. Wird der Zweig nicht mehr gepflegt, ist ein Upgrade bereits deutlich
  überfällig. Dann muss ein Wechsel auf einen neueren Zweig erwogen werden; dabei die README
  sorgfältig lesen.

HAProxy muss entsprechend seiner Bezugsquelle aktualisiert werden. Üblicherweise erfolgt dies über das Paketaktualisierungsverfahren des Systemanbieters. Bei einer Installation aus dem Quellcode nach dem Entpacken die README im Quellverzeichnis lesen und den Anweisungen für das verwendete Betriebssystem folgen.
