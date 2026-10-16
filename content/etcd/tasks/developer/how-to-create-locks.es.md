---
title: Cómo crear bloqueos
description: Guía para crear bloqueos distribuidos en etcd
weight: 800
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-create-locks.md"
---

LOCK adquiere una exclusión mutua distribuida con un nombre determinado. Una vez adquirido el bloqueo, este se mantiene hasta que etcdctl finaliza.

## Requisitos previos {#prerequisites}

* Instala [`etcd` y `etcdctl`](/es/etcd/install/)

## Creación de un bloqueo {#creating-a-lock}

`lock` para bloqueo distribuido:

![08_etcdctl_lock_2016050501](/etcd/tasks/img/create-lock.gif)

```shell
etcdctl --endpoints=$ENDPOINTS lock mutex1
```

### Opciones {#options}
- endpoints - define una lista separada por comas de direcciones de máquinas en el clúster.
- ttl - tiempo de expiración en segundos de la sesión de bloqueo.
