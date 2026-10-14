---
title: Comment obtenir des clés par préfixe
description: Guide d'extraction des clés etcd par leur préfixe
weight: 300
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-get-key-by-prefix.md"
---

## Prérequis {#pre-requisites}

* [Installer etcdctl](/fr/etcd/install/)
* [Configurer un cluster local](/fr/etcd/dev-guide/local_cluster/)

## Obtenir les clés par préfixe {#get-keys-by-prefix}

```bash
$ etcdctl --endpoints=$ENDPOINTS get PREFIX --prefix
```

### Options globales {#global-options}

```bash
--endpoints=[127.0.0.1:2379], gRPC endpoints
```

### Options {#options}

```bash
--prefix, get a range of keys with matching prefix
```

### Exemple {#example}

![03_etcdctl_get_by_prefix_2016050501](/etcd/tasks/img/get-by-prefix.gif)

```shell
etcdctl --endpoints=$ENDPOINTS put web1 value1
etcdctl --endpoints=$ENDPOINTS put web2 value2
etcdctl --endpoints=$ENDPOINTS put web3 value3

etcdctl --endpoints=$ENDPOINTS get web --prefix
```
