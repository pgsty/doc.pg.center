---
title: Gestión de versiones
weight: 4900
description: Soporte de gestión de versiones por parte de etcd
categories: [Concepto]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/versioning.md"
---

Este documento describe las versiones que cuentan con soporte del proyecto etcd.

## Versionado de servicios y versiones con soporte {#service-versioning-and-supported-versions}

Las versiones de etcd se expresan como **x.y.z**, donde **x** es la versión principal, **y** es la versión secundaria y **z** es la versión de parche, siguiendo la terminología de [Semantic Versioning](https://semver.org/).
Las nuevas versiones secundarias pueden añadir funcionalidades adicionales a la API.

El proyecto etcd mantiene ramas de versión para la versión actual y la anterior. Por ejemplo, cuando v3.5 es la versión actual, v3.4 tiene soporte. Cuando se publica v3.6, v3.4 deja de recibir soporte.

Las correcciones aplicables, incluidas las correcciones de seguridad, pueden retroportarse (backport) a esas dos ramas de versión, según la gravedad y la viabilidad.
Las versiones de parche se generan a partir de esas ramas cuando es necesario.

Los [mantenedores](https://github.com/etcd-io/etcd/blob/main/OWNERS) del proyecto son quienes toman esta decisión.

Puedes comprobar la versión del clúster de etcd en ejecución con `etcdctl`:

```sh
etcdctl --endpoints=127.0.0.1:2379 endpoint status
```

## Versionado de la API {#api-versioning}

Las respuestas de la API `v3` no deberían cambiar tras la versión 3.0.0, pero se añadirán nuevas funcionalidades con el tiempo.
