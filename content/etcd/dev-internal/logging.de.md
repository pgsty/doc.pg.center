---
title: Konventionen für die Protokollierung
weight: 1600
description: Kategorien der Protokollierungsstufen
categories: [Referenz]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-internal/logging.md"
---

etcd verwendet die Bibliothek [zap][zap], um Anwendungsausgaben nach *Stufen* gegliedert zu protokollieren. Die Stufe einer Protokollmeldung richtet sich nach diesen Konventionen:

* DebugLevel-Meldungen sind meist umfangreich und im Produktivbetrieb üblicherweise deaktiviert.
  * Beispiele:
    * Eine normale Nachricht an einen entfernten Peer senden
    * Einen Protokolleintrag auf den Datenträger schreiben

* InfoLevel ist die standardmäßige Protokollierungspriorität.
  * Beispiele:
    * Startkonfiguration
    * Einen Snapshot beginnen
    * Einen neuen Knoten zum Cluster hinzufügen
    * Einen neuen Benutzer zum Authentifizierungssubsystem hinzufügen

* WarnLevel-Meldungen sind wichtiger als Info-Meldungen, müssen aber nicht einzeln von einer Person geprüft werden.
  * Beispiele:
    * Fehler beim Senden einer Raft-Nachricht an einen entfernten Peer
    * Keine Heartbeat-Nachricht innerhalb des konfigurierten Wahlzeitlimits empfangen

* ErrorLevel-Meldungen haben hohe Priorität. Wenn eine Anwendung störungsfrei läuft, sollte sie keine Meldungen dieser Stufe erzeugen.
  * Beispiele:
    * Fehler beim Zuweisen von Datenträgerspeicher für das WAL

* PanicLevel protokolliert eine Meldung und löst anschließend eine Panic aus.
  * Beispiele:
    * Fehler beim Kodieren von Raft-Nachrichten

* FatalLevel protokolliert eine Meldung und ruft anschließend os.Exit(1) auf.
  * Beispiele:
    * Fehler beim Speichern eines Raft-Snapshots

[zap]: https://github.com/uber-go/zap
