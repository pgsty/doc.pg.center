---
title: Comment obtenir des clés par préfixe
description: Guide de extraction des clés etcd par leur préfixe
weight: 300
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/developer/how-to-get-key-by-prefix.md"
aliases: [/etcd/tasks/developer/how-to-get-key-by-prefix/]
---

## Prérequis {#pre-requisites}

* [Installer etcdctl](/fr/docs/etcd/install/)
* [Configurer un cluster local](/fr/docs/etcd/dev-guide/local_cluster/)

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

![03_etcdctl_get_by_prefix_2016050501](/docs/etcd/tasks/img/get-by-prefix.gif)

```shell
etcdctl --endpoints=$ENDPOINTS put web1 value1
etcdctl --endpoints=$ENDPOINTS put web2 value2
etcdctl --endpoints=$ENDPOINTS put web3 value3

etcdctl --endpoints=$ENDPOINTS get web --prefix
```
