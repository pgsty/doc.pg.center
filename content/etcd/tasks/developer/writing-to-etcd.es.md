---
title: Escritura en etcd
description: "Adición de un par clave-valor a un clúster etcd"
weight: 250
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7/tasks/developer/writing-to-etcd.md"
---

## Prerrequisitos {#prerequisites}

- Instala `etcdctl`

## Procedimiento {#procedure}

Usa el subcomando `put` para escribir un par clave-valor:

```shell
etcdctl --endpoints=$ENDPOINTS put foo "Hello World!"
```
donde:
- `foo` es el nombre de la clave
- `"Hello World!"` es el valor delimitado por comillas
