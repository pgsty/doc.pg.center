---
title: "Integration mit anderen Werkzeugen"
linkTitle: "Werkzeugintegration"
weight: 150
icon: fas fa-puzzle-piece
description: "Integration von Patroni mit externen Backup- und Orchestrierungswerkzeugen."
module: [PATRONI]
categories: [Konzept]
aliases: [/patroni/tools_integration/]
upstream_link: "https://patroni.readthedocs.io/en/latest/tools_integration.html"
---

<a id="tools_integration"></a>
Patroni lässt sich mit anderen Werkzeugen der eigenen Umgebung integrieren. Die Liste der Beispiele in diesem Abschnitt ist nicht abschließend, gibt aber Anregungen für solche Integrationen.

--------

## Barman {#barman}
Patroni liefert die Anwendung `patroni_barman`, die mit `pg-backup-api` kommuniziert und so Barman-Operationen aus der Ferne ermöglicht.

Diese Anwendung verfügt derzeit über die Unterbefehle: `recover` und `config-switch`.

### patroni_barman recover {#patroni_barman-recover}
Der Unterbefehl `recover` kann als benutzerdefinierte Bootstrap-Methode oder als benutzerdefinierte Replikat-Erstellungsmethode verwendet werden. Weitere Informationen hierzu finden Sie in [Replikaterstellung und Cluster-Initialisierung](/de/docs/patroni/replica_bootstrap#replica_imaging_and_bootstrap).

### patroni_barman config-switch {#patroni_barman-config-switch}
Der Unterbefehl `config-switch` ist als `on_role_change`-Callback in Patroni vorgesehen. Als Beispiel nehmen wir an, dass Sie WALs von Ihrem aktuellen Primärserver auf Ihren Barman-Host streamen. Im Falle eines Failovers im Cluster möchten Sie möglicherweise den WAL-Stream von dem neuen Primärserver starten. Dies erreichen Sie, indem Sie `patroni_barman config-switch` als `on_role_change`-Callback verwenden.

> [!NOTE]
> Dieser Unterbefehl basiert auf dem `barman config-switch`-Befehl, der dafür verantwortlich ist, die Konfiguration eines Barman-Servers durch Anwenden eines vordefinierten Modells auf ihn zu überschreiben. Dieser Befehl ist seit Barman 3.10 verfügbar. Weitere Einzelheiten finden Sie in der Barman-Dokumentation.

Dies ist ein Beispiel dafür, wie Sie Patroni konfigurieren können, um ein Konfigurationsmodell anzuwenden, falls dieser Patroni-Knoten zum Primärserver hochgestuft wird:

```yaml
postgresql:
    callbacks:
        on_role_change: >
            patroni_barman
                --api-url YOUR_API_URL
                config-switch
                --barman-server YOUR_BARMAN_SERVER_NAME
                --barman-model YOUR_BARMAN_MODEL_NAME
                --switch-when promoted
```

> [!NOTE]
> `patroni_barman config-switch` erfordert, dass sowohl Barman als auch `pg-backup-api` auf dem Barman-Host konfiguriert sind, damit ein entfernter `barman config-switch` über die Backup-API ausgeführt werden kann. Außerdem müssen die anzuwendenden Barman-Modelle bereits konfiguriert sein. Das obige Beispiel verwendet eine Teilmenge der verfügbaren Parameter. Weitere Informationen erhalten Sie durch Ausführen von `patroni_barman config-switch --help` und durch Konsultation der Barman-Dokumentation.
