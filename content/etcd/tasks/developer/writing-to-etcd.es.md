---
title: Escritura en etcd
description: "Adición de un par clave-valor a un clúster etcd"
weight: 250
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/writing-to-etcd.md"
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
