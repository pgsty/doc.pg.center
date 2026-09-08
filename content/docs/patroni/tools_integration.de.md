---
title: "Integration mit anderen Tools"
linkTitle: "Integrationstools"
weight: 150
icon: fas fa-puzzle-piece
description: "Integrieren von Patroni mit externen Backup- und Orchestrierungsinstrumenten."
module: [PATRONI]
categories: [Konzept]
aliases: [/patroni/tools_integration/]
upstream_link: "https://patroni.readthedocs.io/en/latest/tools_integration.html"
---

<a id="tools_integration"></a>
Patroni kann sich in andere Tools in Ihrer Umgebung integrieren. In diesem Abschnitt finden Sie eine Liste von Beispielen, die zwar keine vollständige Liste darstellen, aber Ihnen Ideen geben können, wie Patroni mit anderen Tools zusammenarbeiten kann.

--------

## Barman {#barman}
Patroni liefert eine Anwendung namens `patroni_barman`, die über Logik verfügt, um mit `pg-backup-api` zu kommunizieren, sodass Sie Barman-Operationen entfernt durchführen können.

Diese Anwendung verfügt derzeit über mehrere Unterkommandos: `recover` und `config-switch`.

### patroni_barman recover {#patroni_barman-recover}
Das Unterkommando `recover` kann als benutzerdefinierte Bootstrap-Methode oder als benutzerdefinierte Replikat-Erstellungsmethode verwendet werden. Weitere Informationen hierzu finden Sie in [replica_imaging_and_bootstrap](/de/docs/patroni/replica_bootstrap#replica_imaging_and_bootstrap).

### patroni_barman config-switch {#patroni_barman-config-switch}
Das Unterkommando `config-switch` ist als `on_role_change`-Callback in Patroni vorgesehen. Als Beispiel nehmen wir an, dass Sie WALs von Ihrem aktuellen Primärserver auf Ihren Barman-Host streamen. Im Falle eines Failovers im Cluster möchten Sie möglicherweise den WAL-Stream von dem neuen Primärserver starten. Dies erreichen Sie, indem Sie `patroni_barman config-switch` als `on_role_change`-Callback verwenden.

> [!NOTE]
> Dieser Unterbefehl basiert auf dem `barman config-switch`-Befehl, der dafür verantwortlich ist, die Konfiguration eines Barman-Servers durch Anwenden eines vordefinierten Modells auf ihn zu überschreiben. Dieser Befehl ist seit Barman 3.10 verfügbar. Weitere Einzelheiten finden Sie in der Barman-Dokumentation.

Dies ist ein Beispiel dafür, wie Sie Patroni konfigurieren können, um ein Konfigurationsmodell anzuwenden, falls dieser Patroni-Knoten zur Primärserver-Instanz befördert wird:

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
> `patroni_barman config-switch` erfordert, dass sowohl Barman als auch `pg-backup-api` auf dem Barman-Host konfiguriert sind, damit ein entfernter `barman config-switch` über die Backup-API ausgeführt werden kann. Außerdem erfordert es, dass vorab konfigurierte Barman-Modelle angewendet werden. Das obige Beispiel verwendet eine Teilmenge der verfügbaren Parameter. Weitere Informationen erhalten Sie durch Ausführen von `patroni_barman config-switch --help` und durch Konsultation der Barman-Dokumentation.
