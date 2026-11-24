---
title: Cómo obtener claves por prefijo
description: Guía para extraer claves de etcd por su prefijo
weight: 300
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7/tasks/developer/how-to-get-key-by-prefix.md"
---

## Requisitos previos {#pre-requisites}

* [Instala etcdctl](/es/etcd/install/)
* [Configura un clúster local](/es/etcd/dev-guide/local_cluster/)

## Obtener claves por prefijo {#get-keys-by-prefix}

```bash
$ etcdctl --endpoints=$ENDPOINTS get PREFIX --prefix
```

### Opciones globales {#global-options}

```bash
--endpoints=[127.0.0.1:2379], gRPC endpoints
```

### Opciones {#options}

```bash
--prefix, get a range of keys with matching prefix
```

### Ejemplo {#example}

![03_etcdctl_get_by_prefix_2016050501](/etcd/tasks/img/get-by-prefix.gif)

```shell
etcdctl --endpoints=$ENDPOINTS put web1 value1
etcdctl --endpoints=$ENDPOINTS put web2 value2
etcdctl --endpoints=$ENDPOINTS put web3 value3

etcdctl --endpoints=$ENDPOINTS get web --prefix
```
