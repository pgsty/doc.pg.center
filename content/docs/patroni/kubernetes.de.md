---
title: "Patroni mit Kubernetes verwenden"
linkTitle: "Einsatz mit Kubernetes"
weight: 120
icon: fas fa-dharmachakra
description: "Patroni mit Kubernetes-Objekten, Labels und Diensterkennung verwenden."
module: [PATRONI]
categories: [Aufgabe]
aliases: [/patroni/kubernetes/]
upstream_link: "https://patroni.readthedocs.io/en/latest/kubernetes.html"
---

<a id="kubernetes"></a>
Patroni kann Kubernetes-Objekte verwenden, um den Clusterzustand zu speichern und den Leader-Schlüssel zu verwalten. Damit kann Postgres in einer Kubernetes-Umgebung ohne zusätzlichen Konsistenzspeicher betrieben werden; insbesondere ist keine zusätzliche etcd-Installation nötig. Patroni kann zwei verschiedene Arten von Kubernetes-Objekten zum Speichern der Leader- und Konfigurationsschlüssel verwenden. Die Auswahl erfolgt über `kubernetes.use_endpoints` oder die Umgebungsvariable `PATRONI_KUBERNETES_USE_ENDPOINTS`.

--------

## Endpoints verwenden {#use-endpoints}

Obwohl dieser Modus empfohlen wird, ist er aus Kompatibilitätsgründen standardmäßig deaktiviert. Ist er aktiviert, speichert Patroni die Clusterkonfiguration und den Leader-Schlüssel in den Feldern `metadata: annotations` der jeweils angelegten `Endpoints`. Der Wechsel des Leaders ist sicherer als mit `ConfigMaps`, weil sowohl die Annotationen mit den Leader-Informationen als auch die tatsächlichen Adressen des laufenden Leader-Pods gleichzeitig in einem Schritt aktualisiert werden.

--------

## ConfigMaps verwenden {#use-configmaps}

In diesem Modus erstellt Patroni ConfigMaps anstelle von Endpoints und speichert die Schlüssel in deren Metadaten. Der Wechsel des Leaders erfordert mindestens zwei Aktualisierungen: eine für die Leader-ConfigMap und eine weitere für den jeweiligen Endpoint.

Um den Datenverkehr zum Postgres-Leader zu leiten, muss der Kubernetes-Service für Postgres einen Label-Selektor mit dem in der Patroni-Konfiguration festgelegten `role_label` verwenden.

In einigen Fällen, etwa unter OpenShift, gibt es keine Alternative zu ConfigMaps.

--------

## Konfiguration {#configuration}

Die Kubernetes-[Einstellungen](/de/docs/patroni/config/yaml#kubernetes_settings) und -[Umgebungsvariablen](/de/docs/patroni/config/env#kubernetes_environment) von Patroni werden in den allgemeinen Kapiteln der Dokumentation beschrieben.

<a id="kubernetes_role_values"></a>

### Rollen-Label anpassen {#customize-role-label}

Standardmäßig setzt Patroni auf dem Pod, in dem es läuft, zur Rolle des Knotens passende Labels, beispielsweise `role=primary`. Schlüssel und Wert des Labels lassen sich mit `kubernetes.role_label`, `kubernetes.leader_label_value`, `kubernetes.follower_label_value` und `kubernetes.standby_leader_label_value` anpassen.

Beim Wechsel von den standardmäßigen Rollen-Labels zu eigenen Labels lässt sich die Ausfallzeit mit folgenden Migrationsschritten verringern:

1.  Dem Pod mit `kubernetes.tmp_role_label` ein temporäres Label (etwa `tmp_role`) hinzufügen, das den ursprünglichen Rollenwert verwendet. Nach dem Neustart der Pods setzt Patroni folgende Labels:

> ```yaml
> labels:
>   cluster-name: foo
>   role: primary
>   tmp_role: primary
> ```

2.  Nachdem alle Pods aktualisiert wurden, den Service-Selektor auf das temporäre Label umstellen.

> ```yaml
> selector:
>   cluster-name: foo
>   tmp_role: primary
> ```

3.  Das eigene Rollen-Label hinzufügen (z. B. `kubernetes.leader_label_value=leader` setzen). Nach dem Neustart der Pods setzt Patroni folgende neue Labels:

> ```yaml
> labels:
>   cluster-name: foo
>   role: leader
>   tmp_role: primary
> ```

4.  Nachdem alle Pods erneut aktualisiert wurden, den Service-Selektor auf den neuen Rollenwert umstellen.

> ```yaml
> selector:
>   cluster-name: foo
>   role: leader
> ```

5.  Abschließend das temporäre Label aus der Konfiguration entfernen und alle Pods aktualisieren.

> ```yaml
> labels:
>   cluster-name: foo
>   role: leader
> ```

--------

## Beispiele {#examples}

- Der Ordner [kubernetes](https://github.com/patroni/patroni/tree/master/kubernetes) im Patroni-Repository enthält Beispiele für das Docker-Image und das Kubernetes-Manifest zum Testen einer Patroni-Installation mit Kubernetes. Im aktuellen Zustand können wegen Berechtigungsproblemen keine PersistentVolumes verwendet werden.
- Ein voll ausgestattetes Docker-Image mit Unterstützung für Persistent Volumes bietet das [Spilo-Projekt](https://github.com/zalando/spilo).
- Es gibt außerdem ein [Helm-Chart](https://github.com/kubernetes/charts/tree/master/incubator/patroni) zur Bereitstellung des Spilo-Images mit Patroni unter Kubernetes.
- Für den Betrieb vieler Datenbankcluster mit Patroni und Spilo bietet sich das Projekt [postgres-operator](https://github.com/zalando/postgres-operator) an. Es implementiert das Operator-Muster zur Verwaltung von Spilo-Clustern.
