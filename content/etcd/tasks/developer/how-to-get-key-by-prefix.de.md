---
title: Schlüssel anhand eines Präfixes abrufen
description: Anleitung zum Abrufen von etcd-Schlüsseln anhand ihres Präfixes
weight: 300
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/developer/how-to-get-key-by-prefix.md"
---

## Voraussetzungen {#pre-requisites}

* [etcdctl installieren](/de/etcd/install/)
* [Lokalen Cluster einrichten](/de/etcd/dev-guide/local_cluster/)

## Schlüssel anhand eines Präfixes abrufen {#get-keys-by-prefix}

```bash
$ etcdctl --endpoints=$ENDPOINTS get PREFIX --prefix
```

### Globale Optionen {#global-options}

```bash
--endpoints=[127.0.0.1:2379], gRPC endpoints
```

### Optionen {#options}

```bash
--prefix, get a range of keys with matching prefix
```

### Beispiel {#example}

![03_etcdctl_get_by_prefix_2016050501](/etcd/tasks/img/get-by-prefix.gif)

```shell
etcdctl --endpoints=$ENDPOINTS put web1 value1
etcdctl --endpoints=$ENDPOINTS put web2 value2
etcdctl --endpoints=$ENDPOINTS put web3 value3

etcdctl --endpoints=$ENDPOINTS get web --prefix
```
