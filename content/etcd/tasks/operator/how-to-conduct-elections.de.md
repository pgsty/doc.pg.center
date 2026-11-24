---
title: "Eine Leader-Wahl in einem etcd-Cluster durchführen"
description: "Schritte zum Durchführen einer Leader-Wahl mit dem etcdctl-Client"
weight: 900
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7/tasks/operator/how-to-conduct-elections.md"
---

## Voraussetzungen {#prerequisites}

- Sicherstellen, dass [`etcd`](/de/etcd/install/) und [`etcdctl`](/de/etcd/install/) installiert sind.
- Prüfen, ob ein etcd-Cluster aktiv ist.

## Eine Leader-Wahl durchführen {#conduct-leader-election}

Mit dem Befehl `etcdctl` werden Leader-Wahlen in einem etcd-Cluster durchgeführt. Er stellt sicher, dass jeweils nur ein Client Leader werden kann.

`etcdctl --endpoints=$ENDPOINTS elect <election-name> [proposal]`

```shell
etcdctl --endpoints=$ENDPOINTS elect election-name p1
```

### Optionen {#options}

- `--endpoints : $ENDPOINTS`

Adresse jedes Mitglieds des etcd-Clusters.

- `election-name` Zeichenfolge

Eine Zeichenfolge als Kennung der Wahl. Alle Teilnehmer, die um die Leader-Rolle konkurrieren, müssen denselben Wahlnamen verwenden.

- `leader-name` Zeichenfolge

Vorschlagswert des neuen Leaders.

### Beispiel {#example}

```shell
./etcdctl elect my-election proposal1
my-election/694d99fafea88404
proposal1

another election:
./etcdctl elect new-election proposal1
new-election/694d99fafea8840f
proposal1
```
