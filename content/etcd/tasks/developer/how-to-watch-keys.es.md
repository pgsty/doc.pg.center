---
title: Cómo observar claves
description: Guía para observar claves de etcd
weight: 600
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-watch-keys.md"
---

## Requisitos previos {#prerequisites}

* Instala [`etcd` y `etcdctl`](/es/etcd/install/)

## Observación de claves {#watching-keys}
`watch` para recibir notificaciones de cambios futuros:

```bash
etcdctl watch $KEY [$END_KEY]
```

### Opciones {#options}

```bash
-i, --interactive[=false]: interactive mode
--prefix[=false]: watch on a prefix if prefix is set
--rev=0: Revision to start watching
--prev-kv[=false]: get the previous key-value pair before the event happens
--progress-notify[=false]: get periodic watch progress notification from server
```

### Opciones heredadas de los comandos padre {#options-inherited-from-parent-commands}

```bash
--endpoints="127.0.0.1:2379": gRPC endpoints
```

### Ejemplos {#examples}
![06_etcdctl_watch_2016050501](/etcd/tasks/img/watch-keys.gif)

```shell
etcdctl --endpoints=$ENDPOINTS watch stock1
etcdctl --endpoints=$ENDPOINTS put stock1 1000

etcdctl --endpoints=$ENDPOINTS watch stock --prefix
etcdctl --endpoints=$ENDPOINTS put stock1 10
etcdctl --endpoints=$ENDPOINTS put stock2 20
```
