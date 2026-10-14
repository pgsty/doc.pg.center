---
title: "Dokumentation und Community"
linkTitle: "Ressourcen"
weight: 100
description: "Upstream-Handbücher, Quellcode, Support, Kontakte und Lizenzierung"
icon: fa-solid fa-life-ring
module: [HAPROXY]
categories: [Referenz]
aliases:
  - /haproxy/intro/resources/
  - /docs/haproxy/intro/resources/
  - /haproxy/resources/
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
upstream_name: "HAProxy 3.4 Starter Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapters 1 and 5"
---

## 1. Verfügbare Dokumentation {#section-1}

Die vollständige HAProxy-Dokumentation besteht aus den folgenden Dokumenten. Die jeweils passende Dokumentation spart Zeit und liefert die genaueste Antwort auf die eigene Fragestellung. Bitte keine Fragen an die Mailingliste senden, deren Antworten bereits in diesen Dokumenten stehen.

- [`intro.txt`](/de/docs/haproxy/load-balancing/) (dieses Dokument): behandelt die Grundlagen der Lastverteilung,
  HAProxy als Produkt, seine Fähigkeiten und Grenzen, bekannte Fallstricke, Einschränkungen einzelner
  Betriebssysteme, Bezugsquellen, Weiterentwicklung, die Versorgung mit allen bekannten Fehlerkorrekturen,
  Aktualisierungen sowie Ergänzungen und Alternativen.

- [`management.txt`](/de/docs/haproxy/prerequisites/): erklärt den Start von haproxy, die Verwaltung zur Laufzeit
  und auf mehreren Knoten sowie die Durchführung nahtloser Upgrades.

- [`configuration.txt`](/de/docs/haproxy/http-fundamentals/): das Referenzhandbuch erläutert sämtliche
  Konfigurationsschlüsselwörter und ihre Optionen. Es dient als Nachschlagewerk für Konfigurationsänderungen.

- coding-style.txt: richtet sich an Entwickler, die Code zum Projekt beitragen möchten, und erläutert
  den einzuhaltenden Programmierstil. Er ist nicht besonders streng, und auch der vorhandene Code hält
  ihn nicht vollständig ein. Beiträge, die zu stark davon abweichen, werden jedoch abgelehnt.

- proxy-protocol.txt: die De-facto-Spezifikation des PROXY-Protokolls, das HAProxy und verschiedene
  Produkte von Drittanbietern implementieren.

- security.txt: beschreibt die Meldung von Sicherheitsproblemen und erläutert, was als Schwachstelle
  gilt und was nicht.

- README: beschreibt, wie HAProxy aus dem Quellcode gebaut wird

## 5. Kontakte {#section-5}

Entwickler und andere Mitglieder der Community sind in der Regel am besten über die Mailingliste unter <haproxy@formilux.org> zu erreichen. Die Liste und ihre Archive sind öffentlich; vertrauliche Informationen sollten daher nicht veröffentlicht werden. Dort sind etwa tausend Nutzer mit unterschiedlicher Erfahrung vertreten. Selbst sehr komplexe Fragen erhalten meist relativ schnell eine passende Antwort. Vorschläge sind ebenfalls willkommen. Wer Schwierigkeiten mit E-Mail hat, kann die Discourse-Plattform unter <http://discourse.haproxy.org/> nutzen. Dort lesen allerdings weniger Personen mit, und die meisten Fragen werden von einem sehr kleinen Team bearbeitet. Bitte in jedem Fall geduldig und respektvoll mit denjenigen umgehen, die ihre Freizeit dafür einsetzen, anderen zu helfen.

Ein vermuteter, aber noch nicht sicher bestätigter Fehler wird am besten auf der Mailingliste gemeldet. Wer überzeugt ist, einen Fehler gefunden zu haben, die aktuelle Version seines Zweigs verwendet und bereits ein GitHub-Konto besitzt, kann direkt unter <https://github.com/haproxy/haproxy/> ein Issue mit allen verfügbaren Einzelheiten anlegen. Auch dort sind die Informationen öffentlich; daher nichts veröffentlichen, was später bereut werden könnte. Da der Issue-Tracker die Diskussion als langen Verlauf darstellt, sehr umfangreiche Ausgaben von mehreren hundert Zeilen oder mehr bitte als Anhang beifügen, statt sie in den Text einzufügen.

Bei einem vermuteten Sicherheitsproblem ist die Datei doc/security.txt zu beachten. Sie erläutert, was bei HAProxy als Schwachstelle gilt und was nicht, und wie eine tatsächliche Schwachstelle vertraulich gemeldet wird. Die meisten Verdachtsfälle erweisen sich als gewöhnliche Fehler, die besser auf dem oben beschriebenen Weg gemeldet werden.

## Vollständige lokale Handbuchsammlung {#complete-local-manual-set}

- [Einsteigerhandbuch](/de/docs/haproxy/load-balancing/)
- [Konfigurationshandbuch](/de/docs/haproxy/http-fundamentals/)
- [Verwaltungshandbuch](/de/docs/haproxy/prerequisites/)

## Herkunft dieser Ausgabe {#edition-provenance}

- **Ausgabe:** HAProxy 3.4.6-66, Dokumentationsstand des Wartungszweigs
- **Neueste stabile Version:** HAProxy 3.4.6, Tag `v3.4.6`
- **Quell-Commit:** [`16acce1dac1d`](https://git.haproxy.org/?p=haproxy-3.4.git;a=commit;h=16acce1dac1dcf1ad5d654204af3a5d45d0e3de8)
- **Gerenderte Upstream-Handbücher:** [docs.haproxy.org/3.4/](https://docs.haproxy.org/3.4/)
- **Lokale Lizenzkopien:** [HAProxy-Lizenzhinweis](/third_party/haproxy/LICENSE) und [GPLv2](/third_party/haproxy/GPL-2.0)
