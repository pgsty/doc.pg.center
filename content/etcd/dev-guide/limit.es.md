---
title: Límites del sistema
weight: 3625
description: "límites de etcd: solicitudes y almacenamiento"
categories: [Referencia]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/limit.md"
---

## Límite de tamaño de solicitud {#request-size-limit}

etcd está diseñado para manejar pares clave-valor pequeños, típicos de metadatos. Las solicitudes más grandes funcionan, pero pueden aumentar la latencia de otras solicitudes. Por defecto, el tamaño máximo de cualquier solicitud es de 1.5 MiB. Este límite es configurable mediante la opción `--max-request-bytes` del servidor etcd.

## Límite de tamaño de almacenamiento {#storage-size-limit}

El límite de tamaño de almacenamiento por defecto es de 2 GiB, configurable con la opción `--quota-backend-bytes`. Se sugiere un tamaño máximo de 8 GiB para entornos normales, y etcd muestra una advertencia al iniciar si el valor configurado lo supera.
