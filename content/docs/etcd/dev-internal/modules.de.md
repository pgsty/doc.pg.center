---
title: Go-Module
weight: 1650
description: Aufbau der Go-Module des etcd-Projekts
categories: [Referenz]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-internal/modules.md"
aliases: [/etcd/dev-internal/modules/]
---

Das etcd-Projekt ist seit Version 3.5 in mehrere
[Go-Module](https://golang.org/ref/mod) gegliedert, die in einem [gemeinsamen Repository](https://golang.org/ref/mod#vcs-dir) liegen.

![Moduldiagramm](/docs/etcd/dev-internal/img/modules.svg)

Es gibt folgende Module:

  - **go.etcd.io/etcd/api/v3** - enthält API-Definitionen
  (wie Protos und daraus generierte Bibliotheken), die das Kommunikationsprotokoll
  zwischen etcd-Clients und -Servern festlegen.

  - **go.etcd.io/etcd/pkg/v3** - Sammlung von Hilfspaketen, die etcd verwendet,
  die jedoch nicht spezifisch für etcd sind. Ein Paket gehört nur dann hierher,
  wenn es künftig in ein eigenes Repository ausgelagert werden könnte.
  Hier sollte kein Code mit vielen eigenen Abhängigkeiten hinzugefügt werden, da
  diese automatisch zu Abhängigkeiten der Client-Bibliothek werden,
  die wir schlank halten möchten.

  - **go.etcd.io/etcd/client/v3** - Client-Bibliothek für den Zugriff auf etcd über
  das Netzwerk (grpc). Für alle neuen Anwendungen von etcd empfohlen.

  - **go.etcd.io/etcd/client/v2** - alte Client-Bibliothek für den Zugriff auf etcd
  über das HTTP-Protokoll. Veraltet. Alle neuen Anwendungen sollten die Bibliothek /v3 verwenden.

  - **go.etcd.io/etcd/raft/v3** - Implementierung des verteilten Konsensprotokolls.
  Sollte keinen etcd-spezifischen Code enthalten.

  - **go.etcd.io/etcd/server/v3** - etcd-Implementierung.
  Der Code in diesem Paket ist für den internen Gebrauch in etcd bestimmt und sollte
  von externen Projekten nicht verwendet werden. Der Paketaufbau und die API können sich innerhalb von Minor-Versionen ändern.

  - **go.etcd.io/etcd/etcdctl/v3** - ein Befehlszeilenwerkzeug für den Zugriff auf und die Verwaltung von etcd.

  - **go.etcd.io/etcd/tests/v3** - ein Modul mit allen Integrationstests von etcd.
    Hinweis: Alle Unit-Tests, die schnell sind und keine modulübergreifenden Abhängigkeiten benötigen,
    sollten in den jeweiligen Modulen beim getesteten Code liegen.

  - **go.etcd.io/bbolt** - Implementierung eines persistenten B-Baums.
    Liegt in einem separaten Repository: https://github.com/etcd-io/bbolt.


### Abläufe {#operations}

1. Alle etcd-Module sollten mit denselben Versionen veröffentlicht werden, z. B.
   muss `go.etcd.io/etcd/client/v3@v3.5.10` von `go.etcd.io/etcd/api/v3@v3.5.10` abhängen.

   Die Versionen lassen sich mit folgendem Befehl einheitlich aktualisieren:
   ```shell script
   % DRY_RUN=false TARGET_VERSION="v3.5.10" ./scripts/release_mod.sh update_versions
   ```
2. Veröffentlichte Module sollten gemäß den Regeln unter https://golang.org/ref/mod#vcs-version mit Tags versehen werden.
   Jedes Modul sollte also einen eigenen Tag erhalten.
   Die Tags lassen sich mit folgendem Befehl setzen:
   ```shell script
   % DRY_RUN=false REMOTE_REPO="origin" ./scripts/release_mod.sh push_mod_tags
   ```

3. Alle etcd-Module sollten dieselben Versionen ihrer zugrunde liegenden Abhängigkeiten verwenden.
   Dies lässt sich folgendermaßen überprüfen:
   ```shell script
   % PASSES="dep" ./test.sh
   ```

4. Die go.mod-Dateien dürfen keine ungenutzten Abhängigkeiten enthalten und müssen
   dem Format von `go mod tidy` entsprechen.
   Dies wird folgendermaßen überprüft:
   ```
   % PASSES="mod_tidy" ./test.sh
   ```

5. Um Aktionen über alle Module hinweg auszuführen, etwa alle Dateien automatisch zu formatieren,
   das folgende Skript verwenden oder erweitern:
   ```shell script
   % ./scripts/fix.sh
   ```

### Zukunft {#future}

Als langfristiges Ziel möchten wir die Entwicklung der etcd-Module hin zum folgenden Modell prüfen:

![Moduldiagramm](/docs/etcd/dev-internal/img/modules-future.svg)

Dies setzt Folgendes voraus:
  - etcdmigrate/etcdadm aus der etcdctl-Binärdatei ausgliedern.
    Dadurch würde etcdctl klar zu einer Befehlszeilenhülle
    für die Netzwerk-Client-API,
    während etcdmigrate/etcdadm direkte physische Operationen auf den
    Speicherdateien von etcd unterstützen würden.
  - etcd-proxy aus der Binärdatei ./etcd ausgliedern, da er mehr experimentellen Code
    und somit zusätzliche Risiken und Abhängigkeiten enthält.
  - Die Unterstützung des v2-Protokolls als veraltet einstufen.
