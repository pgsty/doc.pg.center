---
title: "Die Datenbank sichern"
description: "Anleitung zum Erstellen eines Snapshots der etcd-Datenbank"
weight: 1100
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/operator/how-to-save-database.md"
---

## Voraussetzungen {#pre-requisites}

* [etcdctl und etcdutl installieren](/de/etcd/install/)
* [Einen lokalen Cluster einrichten](/de/etcd/dev-guide/local_cluster/)

## Einen Snapshot der Datenbank erstellen {#snapshot-a-database}

`snapshot` zum Speichern eines Snapshots der etcd-Datenbank zu einem bestimmten Zeitpunkt:

```bash
etcdctl --endpoints=$ENDPOINT snapshot save DB_NAME
```

### Globale Optionen {#global-options}

#### etcdctl {#etcdctl}

```bash
--endpoints=[127.0.0.1:2379], gRPC endpoints
```

Ein Snapshot kann nur von einem einzelnen etcd-Knoten angefordert werden. Daher sollte die Option `--endpoints` nur einen Endpunkt enthalten.

#### etcdutl {#etcdutl}

```bash
-w, --write-out string   set the output format (fields, json, protobuf, simple, table) (default "simple")
```

### Beispiel {#example}

![11_etcdctl_snapshot_2016051001](/etcd/tasks/img/save-database.gif)

```shell
ENDPOINTS=$HOST_1:2379
etcdctl --endpoints=$ENDPOINTS snapshot save my.db

Snapshot saved at my.db
```

```shell
etcdutl --write-out=table snapshot status my.db

+---------+----------+------------+------------+
|  HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
+---------+----------+------------+------------+
| c55e8b8 |        9 |         13 | 25 kB      |
+---------+----------+------------+------------+
```
