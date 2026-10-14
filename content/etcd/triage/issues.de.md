---
title: "Richtlinien zur Issue-Triage"
weight: 8100
description: "Richtlinien zur Sichtung und Einordnung von etcd-Issues"
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/triage/issues.md"
---

## Zweck {#purpose}

Die Verwaltung von Issues beschleunigen.

Die Issues für `etcd` sind unter https://github.com/etcd-io/etcd/issues aufgeführt
und werden mit Labels gekennzeichnet. Ein als Fehler erkanntes Issue erhält beispielsweise das Label `area/bug `. Neue Issues haben zunächst keine Labels; üblicherweise ergänzen die Maintainer und aktiven Mitwirkenden von `etcd` sie anhand ihrer Erkenntnisse. Die vollständige Liste der Labels steht unter
https://github.com/kubernetes/kubernetes/labels

Hier einige praktische vordefinierte Suchen nach Issues:
* [Fehler](https://github.com/etcd-io/etcd/labels/area%2Fbug)
* [Hilfe gesucht](https://github.com/etcd-io/etcd/labels/Help%20Wanted)
* [Am längsten nicht eingeordnete Issues](https://github.com/etcd-io/etcd/issues?utf8=%E2%9C%93&q=is%3Aopen+sort%3Aupdated-asc+)
* [Treffen zur Issue-Triage](https://etcd.io/community/#community-meetings)

## Geltungsbereich {#scope}

Diese Richtlinien dienen als grundlegendes Dokument zur Sichtung und Einordnung neuer Issues in `etcd`. Alle sind eingeladen, bei der Verwaltung von Issues und PRs mitzuhelfen. Die hier beschriebenen Arbeiten und Verantwortlichkeiten richten sich jedoch an die Maintainer und aktiven Mitwirkenden von `etcd`.

## Prüfen, ob ein Issue einen Fehler beschreibt {#validate-if-an-issue-is-a-bug}

Prüfen, ob tatsächlich ein Fehler vorliegt. Falls nicht, die Erkenntnisse in einem Kommentar festhalten und triviale Issues schließen. Bei nicht trivialen Issues die Rückmeldung der meldenden Person abwarten, um mögliche Einwände zu berücksichtigen. Antwortet sie innerhalb von 30 Tagen nicht, das Issue schließen. Lässt sich das Problem nicht reproduzieren oder werden weitere Informationen benötigt, einen Kommentar für die meldende Person hinterlassen.

## Inaktive Issues {#inactive-issues}

Issues mit unzureichenden Angaben sollten geschlossen werden, wenn die meldende Person innerhalb von 60 Tagen keine Informationen nachliefert.

## Doppelte Issues {#duplicate-issues}

Bei einem doppelten Issue einen entsprechenden Kommentar mit einem Verweis auf das ursprüngliche Issue hinterlassen und das Duplikat schließen.

## Issues außerhalb von etcd {#issues-that-dont-belong-to-etcd}

Manche gemeldeten Issues betreffen tatsächlich andere Projekte, die `etcd` verwendet, etwa `grpc` oder `golang`. In solchen Fällen sollte die meldende Person gebeten werden, ein Issue im zuständigen Projekt zu eröffnen. Das Issue schließen, sofern nicht ein Maintainer und die meldende Person es zur Nachverfolgung offen halten möchten.

## Wichtige Labels prüfen {#verify-important-labels-are-in-place}

Sicherstellen, dass das Issue Labels für die betroffenen Bereiche hat, geeignete Verantwortliche zugewiesen sind und ein Meilenstein festgelegt ist. Fehlende Labels ergänzen. Lassen sich Labels wegen fehlender Berechtigungen nicht zuweisen oder lässt sich das richtige Label nicht bestimmen, ist das in Ordnung; bei Bedarf die Maintainer kontaktieren.

## Bei Bedarf die verantwortliche Person erinnern {#poke-issue-owner-if-needed}

Wenn für ein von einem Entwickler übernommenes Issue innerhalb von 30 Tagen kein PR erstellt wurde, die verantwortliche Person kontaktieren und sie bei Bedarf bitten, einen PR zu erstellen oder die Zuständigkeit freizugeben.
