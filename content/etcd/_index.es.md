---
title: "Documentación de etcd 3.7"
linkTitle: "etcd 3.7"
description: "Guías oficiales de etcd 3.7 para desarrolladores, operadores, actualizaciones, API y funcionamiento interno."
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
weight: 60
icon: fa-solid fa-gear
sidebar_root_for: self
sidebar_root_link_self: true
section_index: cards
section_index_columns: 3
upstream_source: etcd-20261121
categories: [Concepto]
search_keywords: [v3.7.4, "Go 1.26.11", force-new-cluster, NewJournalWriter]
upstream_link: "https://github.com/etcd-io/website/tree/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7"
cascade:
  upstream_source: etcd-20261121
  type: docs
  module: [ETCD]
---

etcd es un almacén distribuido de pares clave-valor con fuerte consistencia. Estas guías cubren la
instalación y operación de etcd, la construcción de aplicaciones sobre sus API, el entendimiento de
su diseño, la medición del rendimiento y la actualización o degradación de clústeres en la línea de
versiones 3.7.

Comienza con la [Guía de inicio rápido](/es/etcd/quickstart/) para un clúster local de un solo
miembro, [Instalación](/es/etcd/install/) para las rutas de instalación soportadas, o la [Guía de
operaciones](/es/etcd/op-guide/) para despliegues en producción.

## etcd v3.7.4 {#etcd-v3-7-4}

La versión de mantenimiento actual es [v3.7.4](https://github.com/etcd-io/etcd/releases/tag/v3.7.4), publicada el 19 de noviembre de 2026. Los ejemplos de instalación, Docker y Kubernetes de esta edición usan esta versión.

- Corrige la restauración con `--force-new-cluster` cuando el índice consistente del backend está por delante del WAL.
- Usa un puntero atómico para el almacén de alarmas para evitar una condición de carrera.
- Corrige un pánico durante el arranque al reproducir entradas WAL heredadas de atributos de miembro v2.
- Se compila con Go 1.26.11.

Consulta el [registro de cambios upstream fijado](https://github.com/etcd-io/etcd/blob/1ce5a2b779143279c89ed8c7e33a42e51fb697fa/CHANGELOG/CHANGELOG-3.7.md#v374-tbc). Su encabezado todavía dice «TBC»; la etiqueta de versión publicada confirma la disponibilidad.

## etcd v3.7.3 {#etcd-v3-7-3}

La versión de mantenimiento anterior era [v3.7.3](https://github.com/etcd-io/etcd/releases/tag/v3.7.3).

- Corrige condiciones de carrera entre `Hash` y `Restore` en el almacén MVCC y en las operaciones `RangeStream` que devuelven solo claves, además de una regresión del rendimiento de replicación causada por el envío de mensajes `MsgApp` en orden inverso por parte del líder.
- Se compila con Go 1.26.10 y actualiza las dependencias OpenTelemetry y `golang.org/x/net` para resolver los problemas de seguridad notificados.
- Marca como obsoleto `NewJournalWriter` en `client/pkg/v3/logutil`; su eliminación está prevista para v3.8.

Consulta el [registro de cambios del proyecto original](https://github.com/etcd-io/etcd/blob/f164b70fdf458a17aba05dfefc685d7de4c9ca37/CHANGELOG/CHANGELOG-3.7.md#v373-2026-10-22) para ver todos los cambios.
