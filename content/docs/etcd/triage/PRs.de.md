---
title: "PR-Verwaltung"
weight: 8200
description: "Richtlinien zur Verwaltung von etcd-Pull-Requests"
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/triage/PRs.md"
aliases: [/etcd/triage/prs/]
---

## Zweck {#purpose}

Die PR-Verwaltung beschleunigen.

Die PRs für `etcd` sind unter https://github.com/etcd-io/etcd/pulls aufgeführt.
Ein PR kann verschiedene Labels, einen Meilenstein, Reviewer usw. haben. Die vollständige Liste der Labels steht unter
https://github.com/kubernetes/kubernetes/labels

Hier einige praktische Suchbeispiele für PRs:
* [Offene PRS für den Meilenstein etcd-v3.4](https://github.com/etcd-io/etcd/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aopen+milestone%3Aetcd-v3.4)
* [PRs in Untersuchung](https://github.com/etcd-io/etcd/labels/Investigating)

## Geltungsbereich {#scope}

Diese Richtlinien dienen als grundlegendes Dokument zur Verwaltung von PRs in `etcd`. Alle sind eingeladen, bei der PR-Verwaltung mitzuhelfen. Die hier beschriebenen Arbeiten und Verantwortlichkeiten richten sich jedoch an die Maintainer und aktiven Mitwirkenden von `etcd`.

## Inaktive PRs bearbeiten {#handle-inactive-prs}
Die verantwortliche Person für den PR erinnern, wenn Review-Kommentare innerhalb von 15 Tagen nicht bearbeitet wurden. Antwortet sie innerhalb von 90 Tagen nicht, den PR nach Möglichkeit mit einem neuen Commit aktualisieren. Ist das nicht möglich, sollte der inaktive PR nach 180 Tagen geschlossen werden.

## Bei Bedarf Reviewer erinnern {#poke-reviewer-if-needed}

Reviewer reagieren zeitnah. Da alle viel zu tun haben, nach einer Review-Anfrage jedoch etwas Zeit lassen, falls keine schnelle Antwort kommt. Bleibt die Antwort 10 Tage lang aus, können sie durch einen Kommentar im PR, eine E-Mail oder eine Slack-Nachricht kontaktiert werden.

## Wichtige Labels prüfen {#verify-important-labels-are-in-place}

Sicherstellen, dass dem PR geeignete Reviewer zugewiesen sind und ein Meilenstein festgelegt ist. Fehlende Zuweisungen oder andere wichtige Labels ergänzen. Lässt sich das richtige Label nicht bestimmen, einen Kommentar hinterlassen, damit die Maintainer es bei Bedarf festlegen können.
