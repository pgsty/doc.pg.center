---
title: Einen lokalen Cluster einrichten
weight: 3125
description: Lokale Cluster für Tests und Entwicklung konfigurieren
categories: [Tutorial]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/local_cluster.md"
---

Für Test- und Entwicklungsumgebungen ist die Konfiguration eines lokalen Clusters der schnellste und einfachste Weg. Für eine produktive Bereitstellung siehe den Abschnitt [Cluster einrichten][clustering].

## Lokaler eigenständiger Cluster {#local-standalone-cluster}

### Einen Cluster starten {#starting-a-cluster}

Mit folgendem Befehl wird ein eigenständiger etcd-Cluster bereitgestellt:

```
$ ./etcd
...
```

Wenn die Binärdatei `etcd` nicht im aktuellen Arbeitsverzeichnis liegt, befindet sie sich möglicherweise unter `$GOPATH/bin/etcd` oder `/usr/local/bin/etcd`. Den Befehl entsprechend ausführen.

Das laufende etcd-Mitglied nimmt unter `localhost:2379` Client-Anfragen entgegen.

### Mit dem Cluster arbeiten {#interacting-with-the-cluster}

Mit `etcdctl` lässt sich mit dem laufenden Cluster arbeiten:

1. Ein beispielhaftes Schlüssel-Wert-Paar im Cluster speichern:

    ```
      $ ./etcdctl put foo bar
      OK
    ```

    Wenn OK ausgegeben wird, wurde das Schlüssel-Wert-Paar erfolgreich gespeichert.

2. Den Wert von `foo` abrufen:

    ```
    $ ./etcdctl get foo
    bar
    ```

    Wenn `bar` zurückgegeben wird, funktioniert die Interaktion mit dem etcd-Cluster wie erwartet.

## Lokaler Cluster mit mehreren Mitgliedern {#local-multi-member-cluster}

### Einen Cluster starten {#starting-a-cluster-1}

Im Stammverzeichnis des etcd-Git-Repositorys liegt eine `Procfile`, mit der sich ein lokaler Cluster mit mehreren Mitgliedern einfach konfigurieren lässt. Zum Starten eines solchen Clusters in das Stammverzeichnis des etcd-Quellbaums wechseln und Folgendes ausführen:

1. `goreman` installieren, um auf Procfile basierende Anwendungen zu steuern:

    ```
    $ go install github.com/mattn/goreman@latest
    ```

2. Einen Cluster mit `goreman` und der mitgelieferten Procfile von etcd starten:

    ```
    $ goreman -f Procfile start
    ```

    Die Mitglieder starten. Sie nehmen Client-Anfragen unter `localhost:2379`, `localhost:22379` beziehungsweise `localhost:32379` entgegen.

### Mit dem Cluster arbeiten {#interacting-with-the-cluster-1}

Mit `etcdctl` lässt sich mit dem laufenden Cluster arbeiten:

1. Die Mitgliederliste ausgeben:

    ```
    $ etcdctl --write-out=table --endpoints=localhost:2379 member list
    ```
    Die Liste der etcd-Mitglieder wird wie folgt angezeigt:

    ```
    +------------------+---------+--------+------------------------+------------------------+
    |        ID        | STATUS  |  NAME  |       PEER ADDRS       |      CLIENT ADDRS      |
    +------------------+---------+--------+------------------------+------------------------+
    | 8211f1d0f64f3269 | started | infra1 | http://127.0.0.1:2380  | http://127.0.0.1:2379  |
    | 91bc3c398fb3c146 | started | infra2 | http://127.0.0.1:22380 | http://127.0.0.1:22379 |
    | fd422379fda50e48 | started | infra3 | http://127.0.0.1:32380 | http://127.0.0.1:32379 |
    +------------------+---------+--------+------------------------+------------------------+
    ```

2. Ein beispielhaftes Schlüssel-Wert-Paar im Cluster speichern:

    ```
    $ etcdctl put foo bar
    OK
    ```

    Wenn OK ausgegeben wird, wurde das Schlüssel-Wert-Paar erfolgreich gespeichert.

### Fehlertoleranz testen {#testing-fault-tolerance}

Um die Fehlertoleranz von etcd zu testen, ein Mitglied beenden und versuchen, den Schlüssel abzurufen.

1. Den Prozessnamen des Mitglieds ermitteln, das angehalten werden soll.

    Die `Procfile` enthält die Eigenschaften des Clusters mit mehreren Mitgliedern. Als Beispiel dient das Mitglied mit dem Prozessnamen `etcd2`.

2. Das Mitglied anhalten:

    ```
    # kill etcd2
    $ goreman run stop etcd2
    ```

3. Einen Schlüssel speichern:

    ```
    $ etcdctl put key hello
    OK
    ```

4.  Den im vorherigen Schritt gespeicherten Schlüssel abrufen:

    ```
    $ etcdctl get key
    hello
    ```

5. Einen Schlüssel vom angehaltenen Mitglied abrufen:

    ```
    $ etcdctl --endpoints=localhost:22379 get key
    ```

    Der Befehl sollte wegen der fehlgeschlagenen Verbindung eine Fehlermeldung anzeigen:

    ```
    2017/06/18 23:07:35 grpc: Conn.resetTransport failed to create client transport: connection error: desc = "transport: dial tcp 127.0.0.1:22379: getsockopt: connection refused"; Reconnecting to "localhost:22379"
    Error:  grpc: timed out trying to connect
    ```
6. Das angehaltene Mitglied neu starten:

    ```
    $ goreman run restart etcd2
    ```

7. Den Schlüssel vom neu gestarteten Mitglied abrufen:

    ```
    $ etcdctl --endpoints=localhost:22379 get key
    hello
    ```

    Der Neustart des Mitglieds stellt die Verbindung wieder her. `etcdctl` kann den Schlüssel nun erfolgreich abrufen. Weitere Informationen zur Arbeit mit etcd enthält der Abschnitt [Mit etcd arbeiten][interacting].

[clustering]: /de/etcd/op-guide/clustering/
[interacting]: /de/etcd/dev-guide/interacting_v3/
