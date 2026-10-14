---
title: Glossar
weight: 2900
description: Begriffe in der etcd-Dokumentation, der Befehlszeile und dem Quellcode
categories: [Referenz]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/glossary.md"
---

Dieses Dokument definiert die verschiedenen Begriffe, die in der etcd-Dokumentation, der Befehlszeile und dem Quellcode verwendet werden.

## Alarm {#alarm}

Der etcd-Server löst einen Alarm aus, wenn ein Eingriff des Betreibers erforderlich ist, damit der Cluster zuverlässig bleibt.

## Authentifizierung {#authentication}

Die Authentifizierung verwaltet die Zugriffsberechtigungen von Benutzern auf etcd-Ressourcen.

## Client {#client}

Ein Client verbindet sich mit dem etcd-Cluster, um Dienstanfragen zu stellen, etwa zum Abrufen von Schlüssel-Wert-Paaren, zum Schreiben von Daten oder zum Beobachten von Änderungen.

## Cluster {#cluster}

Ein Cluster besteht aus mehreren Mitgliedern.

Der Knoten in jedem Mitglied folgt dem Raft-Konsensprotokoll, um Logs zu replizieren. Der Cluster empfängt Vorschläge von Mitgliedern, bestätigt sie und wendet sie auf den lokalen Speicher an.

## Kompaktierung {#compaction}

Die Kompaktierung verwirft den gesamten etcd-Ereignisverlauf und die ersetzten Schlüssel vor einer bestimmten Revision. Sie dient dazu, Speicherplatz in der Backend-Datenbank von etcd zurückzugewinnen.

## Wahl {#election}

Der etcd-Cluster hält im Rahmen des Raft-Konsensprotokolls Wahlen unter seinen Mitgliedern ab, um einen Leader zu bestimmen.

## Endpunkt {#endpoint}

Eine URL, die auf einen etcd-Dienst oder eine etcd-Ressource verweist.

## Schlüssel {#key}

Ein benutzerdefinierter Bezeichner zum Speichern und Abrufen benutzerdefinierter Werte in etcd.

## Schlüsselbereich {#key-range}

Eine Schlüsselmenge, die entweder einen einzelnen Schlüssel, ein lexikalisches Intervall für alle x mit a <= x < b oder alle Schlüssel größer als ein bestimmter Schlüssel enthält.

## Schlüsselraum {#keyspace}

Die Menge aller Schlüssel in einem etcd-Cluster.

## Lease {#lease}

Eine kurzlebige, verlängerbare Vereinbarung, die bei ihrem Ablauf die ihr zugeordneten Schlüssel löscht.

## Mitglied {#member}

Ein logischer etcd-Server, der am Betrieb eines etcd-Clusters beteiligt ist.

## Änderungsrevision {#modification-revision}

Die erste Revision, die den letzten Schreibvorgang für einen bestimmten Schlüssel enthält.

## Peer {#peer}

Ein Peer ist ein anderes Mitglied desselben Clusters.

## Vorschlag {#proposal}

Ein Vorschlag ist eine Anfrage, etwa eine Schreibanfrage oder eine Anfrage zur Konfigurationsänderung, die das Raft-Protokoll durchlaufen muss.

## Quorum {#quorum}

Die Anzahl aktiver Mitglieder, die für einen Konsens zur Änderung des Clusterzustands benötigt wird. etcd benötigt eine Mehrheit der Mitglieder, um ein Quorum zu erreichen.

## Revision {#revision}

Ein clusterweiter 64-Bit-Zähler, der bei 1 beginnt und bei jeder Änderung des Schlüsselraums erhöht wird.

## Rolle {#role}

Eine Einheit von Berechtigungen für eine Menge von Schlüsselbereichen, die zur Zugriffskontrolle einer Menge von Benutzern zugewiesen werden kann.

## Snapshot {#snapshot}

Ein Backup des etcd-Clusterzustands zu einem bestimmten Zeitpunkt.

## Speicher {#store}

Der physische Speicher, in dem der Schlüsselraum des Clusters abgelegt ist.

## Term {#term}

Ein Term ist eine monoton steigende Ganzzahl, die im Raft-Algorithmus jeder Leader-Wahl zugeordnet wird.
Pro Term kann es nur einen gewählten Leader geben. Bei einem Leader-Wechsel wird der Term erhöht.

## Transaktion {#transaction}

Eine atomar ausgeführte Menge von Operationen. Alle in einer Transaktion geänderten Schlüssel haben dieselbe Änderungsrevision.

## Schlüsselversion {#key-version}

Die Anzahl der Schreibvorgänge für einen Schlüssel seit seiner Erstellung, beginnend bei 1. Die Version eines nicht vorhandenen oder gelöschten Schlüssels ist 0.

## Watcher {#watcher}

Ein Client öffnet einen Watcher, um Änderungen in einem bestimmten Schlüsselbereich zu beobachten.
