---
title: "Funktionsschalter"
weight: 1175
icon: fa-solid fa-toggle-on
categories: [Referenz]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/feature-gates/index.md"
aliases: [/etcd/feature-gates/]
---

<!-- overview -->
Diese Seite gibt einen Überblick über die verschiedenen Funktionsschalter, die Administratoren für etcd festlegen können.

Die Entwicklungsphasen einer Funktion werden unter [Funktionsphasen](#feature-stages) erläutert.

<!-- body -->
## Überblick {#overview}

Funktionsschalter sind eine Menge von key=value-Paaren, die etcd-Funktionen beschreiben.
Mit der Befehlszeilenoption `--feature-gates` lassen sich diese Funktionen in etcd ein- oder ausschalten.

etcd ermöglicht das Aktivieren oder Deaktivieren einer Gruppe von Funktionsschaltern.
Mit der Option `-h` lässt sich die vollständige Liste der Funktionsschalter anzeigen.
Zum Festlegen der Funktionsschalter der Option `--feature-gates` auf der Befehlszeile eine Liste von Funktionspaaren zuweisen:

```shell
--feature-gates=...,StopGRPCServiceOnDefrag=true
```

Alternativ `feature-gates` in der YAML-Konfigurationsdatei angeben:

```shell
feature-gates: ...,StopGRPCServiceOnDefrag=true
```

### Änderung an der Struktur `embed.Config` {#change-in-embedetcdserver-struct}

In 3.6 wird das Feld `ServerFeatureGate` zu `embed.Config` hinzugefügt. Es sollte die unten aufgeführten experimentellen Felder ersetzen:

```diff
package embed

type Config struct {
  // Deprecated: Use CompactHashCheck Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalCompactHashCheckEnabled bool `json:"experimental-compact-hash-check-enabled"`

  // Deprecated: Use InitialCorruptCheck Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalInitialCorruptCheck bool `json:"experimental-initial-corrupt-check"`

  // Deprecated: Use TxnModeWriteWithSharedBuffer Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalTxnModeWriteWithSharedBuffer bool `json:"experimental-txn-mode-write-with-shared-buffer"`

  // Deprecated: Use StopGRPCServiceOnDefrag Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalStopGRPCServiceOnDefrag bool `json:"experimental-stop-grpc-service-on-defrag"`

  // Deprecated: Use LeaseCheckpoint Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalEnableLeaseCheckpoint bool `json:"experimental-enable-lease-checkpoint"`
  
  // Deprecated: Use LeaseCheckpointPersist Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalEnableLeaseCheckpointPersist bool `json:"experimental-enable-lease-checkpoint-persist"`

+ // ServerFeatureGate is a server level feature gate
+ ServerFeatureGate featuregate.FeatureGate
  ...
```

### Funktionsschalter für Alpha- oder Beta-Funktionen {#feature-gates-for-alpha-or-beta-features}

Die folgenden Tabellen fassen die Funktionsschalter zusammen, die für etcd gesetzt werden können.

| Funktion                          | Standardwert | Phase | Einzelheiten                                                                               |
|----------------------------------|---------|-------|--------------------------------------------------------------------------------------|
| CompactHashCheck                 | false   | Alpha |Ermöglicht dem Leader, die Kompaktierungs-Hashes der Follower regelmäßig zu prüfen.                                                                              |
| InitialCorruptCheck              | false   | Alpha |Ermöglicht die Prüfung auf Datenkorruption, bevor Client- oder Peer-Verkehr bedient wird.                                                                           |
| LeaseCheckpoint                  | false   | Alpha |Ermöglicht dem Leader, regelmäßig Checkpoints an andere Mitglieder zu senden, damit die verbleibende TTL bei einem Leader-Wechsel nicht zurückgesetzt wird.                                              |
| LeaseCheckpointPersist           | false   | Alpha |Ermöglicht das dauerhafte Speichern von remainingTTL, um eine unbegrenzte automatische Verlängerung langlebiger Leases zu verhindern.                                                                         |
| SetMemberLocalAddr               | false   | Alpha |Ermöglicht es, die erste in initial-advertise-peer-urls angegebene lokale Adresse, die keine Loopback-Adresse ist, bei der Kommunikation mit einem Peer als lokale Adresse zu verwenden.      |
| StopGRPCServiceOnDefrag          | false   | Alpha |Ermöglicht es dem gRPC-Dienst von etcd, während der Defragmentierung keine Clientanfragen mehr zu bedienen.                                                                      |
| TxnModeWriteWithSharedBuffer     | true    | Beta  |Ermöglicht einer Schreibtransaktion, für ihre schreibgeschützten Prüfoperationen einen gemeinsamen Puffer zu verwenden.                                                                                |

## Eine Funktion verwenden {#using-a-feature}

### Funktionsphasen {#feature-stages}

Eine Funktion kann sich in der Phase *Alpha*, *Beta*, *GA* oder *Veraltet* befinden.
Eine *Alpha*-Funktion bedeutet:

* Standardmäßig deaktiviert.
* Möglicherweise fehlerhaft. Durch das Aktivieren der Funktion können Fehler auftreten.
* Die Unterstützung der Funktion kann jederzeit ohne Ankündigung eingestellt werden.
* Die API kann sich in einer späteren Softwareversion ohne Ankündigung inkompatibel ändern.
* Aufgrund des erhöhten Fehlerrisikos und der fehlenden langfristigen Unterstützung nur für kurzlebige Testcluster empfohlen.

Eine *Beta*-Funktion bedeutet:

* Standardmäßig aktiviert.
* Die Funktion ist gründlich getestet. Ihre Aktivierung gilt als sicher.
* Die Unterstützung der Funktion insgesamt wird nicht eingestellt, Einzelheiten können sich jedoch ändern.
* Nur für nicht geschäftskritische Einsatzzwecke empfohlen, da bei breiterer Nutzung neue, schwer erkennbare Fehler entdeckt werden können.

> [!NOTE]
> Bitte *Beta*-Funktionen ausprobieren und Rückmeldungen dazu geben!
> Nach dem Ende der Beta-Phase lassen sich weitere Änderungen möglicherweise nicht mehr sinnvoll umsetzen.

Eine Funktion mit *allgemeiner Verfügbarkeit* (GA) wird auch als *stabile* Funktion bezeichnet. Das bedeutet:

* Die Funktion ist immer aktiviert und lässt sich nicht deaktivieren.
* Der zugehörige Funktionsschalter wird nicht mehr benötigt.
* Stabile Versionen von Funktionen werden in vielen nachfolgenden Softwareversionen enthalten sein.

Eine *veraltete* Funktion bedeutet:

* Der Funktionsschalter wird nicht mehr verwendet.
* Die Funktion hat den Status GA erreicht oder wurde entfernt.
