---
title: "Citus-Unterstützung"
weight: 130
icon: fas fa-lemon
description: "Einzelheiten zur Patroni-Integration für Citus-Koordinator- und Worker-Gruppen."
module: [PATRONI]
categories: [Konzept]
aliases: [/patroni/citus/]
upstream_link: "https://patroni.readthedocs.io/en/latest/citus.html"
---

<a id="citus"></a>
Patroni vereinfacht die Bereitstellung von [Citus-Clustern mit mehreren Knoten](https://docs.citusdata.com/en/stable/installation/multi_node.html) erheblich.

--------

## Kurzüberblick (TL;DR) {#tldr}

Es müssen nur wenige einfache Regeln beachtet werden:

1.  Die PostgreSQL-Datenbankerweiterung [Citus](https://github.com/citusdata/citus) muss auf allen Knoten verfügbar sein. Die älteste unterstützte Citus-Version ist 10.0. Um alle Vorteile transparenter Switchover und Worker-Neustarts zu nutzen, wird jedoch mindestens Citus 11.2 empfohlen.
2.  Der Cluster-Name (`scope`) muss auf allen Citus-Knoten identisch sein!
3.  Die Superuser-Zugangsdaten müssen auf dem Koordinator und allen Worker-Knoten identisch sein, und `pg_hba.conf` sollte den Superuser-Zugriff zwischen allen Knoten erlauben.
4.  Der Zugriff auf die [REST API](/de/docs/patroni/config/yaml#restapi_settings) des Koordinators sollte von den Worker-Knoten aus erlaubt sein. Beispielsweise sollten die Zugangsdaten identisch sein, und sofern Client-Zertifikate konfiguriert sind, muss der Koordinator die Zertifikate der Worker-Knoten akzeptieren.
5.  Den folgenden Abschnitt zu `patroni.yaml` hinzufügen:

```yaml
citus:
  group: X  # 0 for coordinator and 1, 2, 3, etc for workers
  database: citus  # must be the same on all nodes
```

Anschließend muss nur noch Patroni gestartet werden; es übernimmt den Rest:

0.  Patroni setzt `bootstrap.dcs.synchronous_mode` auf [quorum](/de/docs/patroni/replication_modes#quorum_mode), sofern nicht ausdrücklich ein anderer Wert festgelegt ist.
1.  Die Erweiterung [citus](/de/docs/patroni/citus#citus) wird automatisch zu `shared_preload_libraries` hinzugefügt.
2.  Wenn `max_prepared_transactions` in der globalen [dynamischen Konfiguration](/de/docs/patroni/config/dynamic#dynamic) nicht ausdrücklich gesetzt ist, setzt Patroni den Wert automatisch auf `2*max_connections`.
3.  Der GUC-Wert `citus.local_hostname` wird von `localhost` auf den Wert geändert, den Patroni für die Verbindung zur lokalen PostgreSQL-Instanz verwendet. Dieser Wert sollte in manchen Fällen von `localhost` abweichen, da PostgreSQL dort möglicherweise nicht lauscht.
4.  Die mit `citus.database` angegebene Datenbank wird automatisch erstellt; anschließend wird `CREATE EXTENSION citus` ausgeführt.
5.  Die aktuellen Superuser-[Zugangsdaten](/de/docs/patroni/config/yaml#postgresql_settings) werden zur Tabelle `pg_dist_authinfo` hinzugefügt, um die Kommunikation zwischen Knoten zu ermöglichen. Diese Daten müssen ebenfalls aktualisiert werden, wenn später username/password/sslcert/sslkey des Superusers geändert werden!
6.  Der Primärserver des Koordinators erkennt die Primärserver der Worker automatisch und fügt sie mit der Funktion `citus_add_node()` zur Tabelle `pg_dist_node` hinzu.
7.  Patroni pflegt `pg_dist_node` auch dann, wenn auf dem Koordinator- oder einem Worker-Cluster ein Failover oder Switchover erfolgt.

--------

## patronictl {#patronictl}

Koordinator- und Worker-Cluster sind physisch getrennte PostgreSQL-/Patroni-Cluster, die lediglich mithilfe der PostgreSQL-Datenbankerweiterung [Citus](https://github.com/citusdata/citus) logisch zusammengefasst werden. Daher lassen sie sich in den meisten Fällen nicht als eine einzige Einheit verwalten.

Im Verhalten von [patronictl](/de/docs/patroni/patronictl#patronictl) ergeben sich zwei wesentliche Unterschiede zum üblichen Verhalten, wenn `patroni.yaml` den Abschnitt [citus](/de/docs/patroni/citus#citus) enthält:

1.  `list` und `topology` geben standardmäßig alle Mitglieder des Citus-Verbunds aus (Koordinatoren und Worker). Die neue Spalte `Group` zeigt an, zu welcher Citus-Gruppe sie gehören.
2.  Für alle Befehle von [patronictl](/de/docs/patroni/patronictl#patronictl) gibt es die neue Option `--group`. Bei einigen Befehlen kann der Standardwert für die Gruppe aus `patroni.yaml` übernommen werden. Beispielsweise aktiviert [`patronictl pause`](/de/docs/patroni/patronictl#patronictl_pause) den Wartungsmodus standardmäßig für die `group`, die im Abschnitt [citus](/de/docs/patroni/citus#citus) festgelegt ist. Bei [`patronictl switchover`](/de/docs/patroni/patronictl#patronictl_switchover) oder [`patronictl remove`](/de/docs/patroni/patronictl#patronictl_remove) muss die Gruppe hingegen ausdrücklich angegeben werden.

Beispiel einer Ausgabe von [`patronictl list`](/de/docs/patroni/patronictl#patronictl_list) für einen Citus-Cluster:

    postgres@coord1:~$ patronictl list demo
    + Citus cluster: demo ----------+----------------+---------+----+-------------+-----+------------+-----+
    | Group | Member  | Host        | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+
    |     0 | coord1  | 172.27.0.10 | Replica        | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord2  | 172.27.0.6  | Quorum Standby | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord3  | 172.27.0.4  | Leader         | running |  1 |             |     |            |     |
    |     1 | work1-1 | 172.27.0.8  | Quorum Standby | running |  1 |   0/31D3198 |   0 |  0/31D3198 |   0 |
    |     1 | work1-2 | 172.27.0.2  | Leader         | running |  1 |             |     |            |     |
    |     2 | work2-1 | 172.27.0.5  | Quorum Standby | running |  1 |   0/31CDFC0 |   0 |  0/31CDFC0 |   0 |
    |     2 | work2-2 | 172.27.0.7  | Leader         | running |  1 |             |     |            |     |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+

Mit der zusätzlichen Option `--group` ändert sich die Ausgabe wie folgt:

    postgres@coord1:~$ patronictl list demo --group 0
    + Citus cluster: demo (group: 0, 7179854923829112860) -+-------------+-----+------------+-----+
    | Member | Host        | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +--------+-------------+----------------+---------+----+-------------+-----+------------+-----+
    | coord1 | 172.27.0.10 | Replica        | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    | coord2 | 172.27.0.6  | Quorum Standby | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    | coord3 | 172.27.0.4  | Leader         | running |  1 |             |     |            |     |
    +--------+-------------+----------------+---------+----+-------------+-----+------------+-----+

    postgres@coord1:~$ patronictl list demo --group 1
    + Citus cluster: demo (group: 1, 7179854923881963547) -+-------------+-----+------------+-----+
    | Member  | Host       | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +---------+------------+----------------+---------+----+-------------+-----+------------+-----+
    | work1-1 | 172.27.0.8 | Quorum Standby | running |  1 |   0/31D3198 |   0 |  0/31D3198 |   0 |
    | work1-2 | 172.27.0.2 | Leader         | running |  1 |             |     |            |     |
    +---------+------------+----------------+---------+----+-------------+-----+------------+-----+

--------

## Switchover eines Citus-Workers {#citus-worker-switchover}

Bei einem Switchover eines Citus-Worker-Knotens bietet Citus die Möglichkeit, diesen für die Anwendung nahezu transparent durchzuführen. Da sich die Anwendung mit dem Koordinator verbindet, der wiederum Verbindungen zu den Worker-Knoten herstellt, kann Citus den SQL-Datenverkehr auf dem Koordinator für die Shards eines Worker-Knotens pausieren. Der Switchover erfolgt dann, während der Datenverkehr auf dem Koordinator zurückgehalten wird. Der Datenverkehr wird fortgesetzt, sobald ein neuer Primärserver des Workers bereit ist, lesende und schreibende Abfragen anzunehmen.

Beispiel für [`patronictl switchover`](/de/docs/patroni/patronictl#patronictl_switchover) auf einem Worker-Cluster:

    postgres@coord1:~$ patronictl switchover demo
    + Citus cluster: demo ----------+----------------+---------+----+-------------+-----+------------+-----+
    | Group | Member  | Host        | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+
    |     0 | coord1  | 172.27.0.10 | Replica        | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord2  | 172.27.0.6  | Quorum Standby | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord3  | 172.27.0.4  | Leader         | running |  1 |             |     |            |     |
    |     1 | work1-1 | 172.27.0.8  | Leader         | running |  1 |             |     |            |     |
    |     1 | work1-2 | 172.27.0.2  | Quorum Standby | running |  1 |   0/31D3198 |   0 |  0/31D3198 |   0 |
    |     2 | work2-1 | 172.27.0.5  | Quorum Standby | running |  1 |   0/31CDFC0 |   0 |  0/31CDFC0 |   0 |
    |     2 | work2-2 | 172.27.0.7  | Leader         | running |  1 |             |     |            |     |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+
    Citus group: 2
    Primary [work2-2]:
    Candidate ['work2-1'] []:
    When should the switchover take place (e.g. 2024-08-26T08:02 )  [now]:
    Current cluster topology
    + Citus cluster: demo (group: 2, 7179854924063375386) -+-------------+-----+------------+-----+
    | Member  | Host       | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +---------+------------+----------------+---------+----+-------------+-----+------------+-----+
    | work2-1 | 172.27.0.5 | Quorum Standby | running |  1 |   0/31CDFC0 |   0 |  0/31CDFC0 |   0 |
    | work2-2 | 172.27.0.7 | Leader         | running |  1 |             |     |            |     |
    +---------+------------+----------------+---------+----+-------------+-----+------------+-----+
    Are you sure you want to switchover cluster demo, demoting current primary work2-2? [y/N]: y
    2024-08-26 07:02:40.33003 Successfully switched over to "work2-1"
    + Citus cluster: demo (group: 2, 7179854924063375386) --------+---------+------------+---------+
    | Member  | Host       | Role    | State   | TL | Receive LSN |     Lag | Replay LSN |     Lag |
    +---------+------------+---------+---------+----+-------------+---------+------------+---------+
    | work2-1 | 172.27.0.5 | Leader  | running |  1 |             |         |            |         |
    | work2-2 | 172.27.0.7 | Replica | stopped |    |     unknown | unknown |    unknown | unknown |
    +---------+------------+---------+---------+----+-------------+---------+------------+---------+

    postgres@coord1:~$ patronictl list demo
    + Citus cluster: demo ----------+----------------+---------+----+-------------+-----+------------+-----+
    | Group | Member  | Host        | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+
    |     0 | coord1  | 172.27.0.10 | Replica        | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord2  | 172.27.0.6  | Quorum Standby | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord3  | 172.27.0.4  | Leader         | running |  1 |             |     |            |     |
    |     1 | work1-1 | 172.27.0.8  | Leader         | running |  1 |             |     |            |     |
    |     1 | work1-2 | 172.27.0.2  | Quorum Standby | running |  1 |   0/31D3198 |   0 |  0/31D3198 |   0 |
    |     2 | work2-1 | 172.27.0.5  | Leader         | running |  2 |             |     |            |     |
    |     2 | work2-2 | 172.27.0.7  | Quorum Standby | running |  2 |   0/31CDFC0 |   0 |  0/31CDFC0 |   0 |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+

Auf der Koordinatorseite sieht das wie folgt aus:

    # The worker primary notifies the coordinator that it is going to execute "pg_ctl stop".
    2024-08-26 07:02:38,636 DEBUG: query(BEGIN, ())
    2024-08-26 07:02:38,636 DEBUG: query(SELECT pg_catalog.citus_update_node(%s, %s, %s, true, %s), (3, '172.19.0.7-demoted', 5432, 10000))
    # From this moment all application traffic on the coordinator to the worker group 2 is paused.

    # The old worker primary is assigned as a secondary.
    2024-08-26 07:02:40,084 DEBUG: query(SELECT pg_catalog.citus_update_node(%s, %s, %s, true, %s), (7, '172.19.0.7', 5432, 10000))

    # The future worker primary notifies the coordinator that it acquired the leader lock in DCS and about to run "pg_ctl promote".
    2024-08-26 07:02:40,085 DEBUG: query(SELECT pg_catalog.citus_update_node(%s, %s, %s, true, %s), (3, '172.19.0.5', 5432, 10000))

    # The new worker primary just finished promote and notifies coordinator that it is ready to accept read-write traffic.
    2024-08-26 07:02:41,485 DEBUG: query(COMMIT, ())
    # From this moment the application traffic on the coordinator to the worker group 2 is unblocked.

--------

## Sekundärknoten {#secondary-nodes}

Ab Patroni v4.0.0 werden auch Citus-Sekundärknoten ohne das [Tag](/de/docs/patroni/config/yaml#tags_settings) `noloadbalance` in `pg_dist_node` registriert. Um Sekundärknoten für schreibgeschützte Abfragen zu verwenden, müssen Anwendungen jedoch den GUC [citus.use_secondary_nodes](https://docs.citusdata.com/en/latest/develop/api_guc.html#citus-use-secondary-nodes-enum) ändern.

--------

## Ein Blick in den DCS {#peek-into-dcs}

Der Citus-Cluster (Koordinator und Worker) wird im DCS als Verbund logisch zusammengehörender Patroni-Cluster gespeichert:

    /service/batman/              # scope=batman
    /service/batman/0/            # citus.group=0, coordinator
    /service/batman/0/initialize
    /service/batman/0/leader
    /service/batman/0/members/
    /service/batman/0/members/m1
    /service/batman/0/members/m2
    /service/batman/1/            # citus.group=1, worker
    /service/batman/1/initialize
    /service/batman/1/leader
    /service/batman/1/members/
    /service/batman/1/members/m3
    /service/batman/1/members/m4
    ...

Dieser Ansatz wurde gewählt, weil sich bei den meisten DCS damit der gesamte Citus-Cluster mit einer einzigen rekursiven Leseanfrage abrufen lässt. Nur die Citus-Koordinatorknoten lesen den gesamten Baum, da sie die Worker-Knoten erkennen müssen. Worker-Knoten lesen lediglich den Teilbaum ihrer eigenen Gruppe und können in manchen Fällen auch den Teilbaum der Koordinatorgruppe lesen.

--------

## Citus auf Kubernetes {#citus-on-kubernetes}

Da Kubernetes keine hierarchischen Strukturen unterstützt, muss die Citus-Gruppe in alle K8s-Objekte aufgenommen werden, die Patroni erstellt:

    batman-0-leader  # the leader config map for the coordinator
    batman-0-config  # the config map holding initialize, config, and history "keys"
    ...
    batman-1-leader  # the leader config map for worker group 1
    batman-1-config
    ...

Das Namensschema lautet also: `${scope}-${citus.group}-${type}`.

Patroni erkennt alle Kubernetes-Objekte über den [Label-Selektor](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors). Daher müssen alle Pods mit Patroni&Citus sowie Endpoints/ConfigMaps Labels, die dem gemeinsamen Label-Selektor entsprechen haben, und Patroni muss über die Kubernetes-[Einstellungen](/de/docs/patroni/config/yaml#kubernetes_settings) oder [Umgebungsvariablen](/de/docs/patroni/config/env#kubernetes_environment) für ihre Verwendung konfiguriert werden.

Einige Beispiele für die Konfiguration von Patroni über Umgebungsvariablen der Pods:

1.  Für den Koordinator-Cluster

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    application: patroni
    citus-group: "0"
    citus-type: coordinator
    cluster-name: citusdemo
  name: citusdemo-0-0
  namespace: default
spec:
  containers:
  - env:
    - name: PATRONI_SCOPE
      value: citusdemo
    - name: PATRONI_NAME
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.name
    - name: PATRONI_KUBERNETES_POD_IP
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: status.podIP
    - name: PATRONI_KUBERNETES_NAMESPACE
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.namespace
    - name: PATRONI_KUBERNETES_LABELS
      value: '{application: patroni}'
    - name: PATRONI_CITUS_DATABASE
      value: citus
    - name: PATRONI_CITUS_GROUP
      value: "0"
```

2.  Für den Worker-Cluster der Gruppe 2

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    application: patroni
    citus-group: "2"
    citus-type: worker
    cluster-name: citusdemo
  name: citusdemo-2-0
  namespace: default
spec:
  containers:
  - env:
    - name: PATRONI_SCOPE
      value: citusdemo
    - name: PATRONI_NAME
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.name
    - name: PATRONI_KUBERNETES_POD_IP
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: status.podIP
    - name: PATRONI_KUBERNETES_NAMESPACE
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.namespace
    - name: PATRONI_KUBERNETES_LABELS
      value: '{application: patroni}'
    - name: PATRONI_CITUS_DATABASE
      value: citus
    - name: PATRONI_CITUS_GROUP
      value: "2"
```

In beiden Beispielen ist das Label `citus-group` gesetzt. Anhand dieses Labels erkennt Patroni, zu welcher Citus-Gruppe ein Objekt gehört. Zusätzlich gibt es die Umgebungsvariable `PATRONI_CITUS_GROUP` mit demselben Wert wie das Label `citus-group`. Wenn Patroni neue Kubernetes-Objekte (ConfigMaps oder Endpoints) erstellt, versieht es diese automatisch mit dem Label `citus-group: ${env.PATRONI_CITUS_GROUP}`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: citusdemo-0-leader  # Is generated as ${env.PATRONI_SCOPE}-${env.PATRONI_CITUS_GROUP}-leader
  labels:
    application: patroni    # Is set from the ${env.PATRONI_KUBERNETES_LABELS}
    cluster-name: citusdemo # Is automatically set from the ${env.PATRONI_SCOPE}
    citus-group: '0'        # Is automatically set from the ${env.PATRONI_CITUS_GROUP}
```

Ein vollständiges Beispiel für die Bereitstellung von Patroni auf Kubernetes mit Citus-Unterstützung findet sich im Ordner [kubernetes](https://github.com/patroni/patroni/tree/master/kubernetes) des Patroni-Repositories.

Dabei sind zwei Dateien relevant:

1.  Dockerfile.citus
2.  citus_k8s.yaml

--------

## Citus-Upgrades und PostgreSQL-Hauptversions-Upgrades {#citus-upgrades-and-postgresql-major-upgrades}

Zunächst die [Dokumentation](https://docs.citusdata.com/en/latest/admin_guide/upgrading_citus.html) zum Aktualisieren der Citus-Version lesen. Im Ablauf gibt es eine kleine Änderung: Beim Upgrade muss PostgreSQL mit [`patronictl restart`](/de/docs/patroni/patronictl#patronictl_restart) anstelle von `systemctl restart` neu gestartet werden.

Ein PostgreSQL-Hauptversions-Upgrade mit Citus ist etwas komplexer. Dafür müssen die Verfahren aus der Citus-Dokumentation zu Hauptversions-Upgrades mit denen aus der Patroni-Dokumentation zu [PostgreSQL-Hauptversionsupgrade](/de/docs/patroni/existing_data#major_upgrade) kombiniert werden. Dabei ist zu beachten, dass ein Citus-Cluster aus mehreren Patroni-Clustern (Koordinator und Worker) besteht, die alle unabhängig voneinander aktualisiert werden müssen.
