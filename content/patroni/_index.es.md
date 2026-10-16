---
title: "Documentación de Patroni 4.1.5"
linkTitle: Patroni
weight: 10
icon: fa-solid fa-heart-pulse
description: "Descripción general de la documentación de alta disponibilidad de Patroni para PostgreSQL."
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
module: [PATRONI]
categories: [Concepto]
upstream_source: patroni
upstream_link: "https://patroni.readthedocs.io/en/latest/index.html"
cascade:
  upstream_source: patroni
  type: docs
  module: [PATRONI]
---

> [!WARNING]
> Ejecutar Patroni en **sistemas con memoria restringida con Python 3.11+**

Si ejecutas Patroni en un sistema con límites de memoria estrictos, por ejemplo con `vm.overcommit_memory=2` (recomendado para PostgreSQL), y usas Python 3.11 o más reciente, puedes observar un comportamiento inesperado:

- Patroni parece estar sano
- PostgreSQL sigue ejecutándose
- La **REST API de Patroni deja de responder**
- El sistema operativo informa de que Patroni está escuchando en el puerto de la REST API
- Los registros de Patroni parecen normales; sin embargo, los siguientes mensajes pueden aparecer una vez: `Exception ignored in thread started by: <object repr() failed>`, `MemoryError`
- Los registros del kernel pueden contener mensajes como `not enough memory for the allocation`

Este comportamiento está causado por un [error de Python 3.11+](https://github.com/python/cpython/issues/140746). Bajo condiciones de memoria estrictas, iniciar un nuevo hilo puede quedarse bloqueado indefinidamente cuando no hay suficiente memoria libre.

## Solución recomendada {#recommended-solution}

Las versiones recientes de Patroni (4.1.1+, 4.0.8+) reducen el impacto de este problema iniciando todos los hilos necesarios al principio del arranque, antes de que el sistema esté bajo presión de memoria.

## Recomendaciones adicionales (Linux, glibc) {#additional-recommendations-linux-glibc}

Al ejecutar con `vm.overcommit_memory=2` (recomendado para PostgreSQL), también recomendamos iniciar Patroni con las siguientes variables de entorno configuradas:

- `MALLOC_ARENA_MAX=1` - reduce la cantidad de memoria virtual asignada por glibc para aplicaciones multihilo
- `PG_MALLOC_ARENA_MAX=` - restablece el valor de `MALLOC_ARENA_MAX` para los procesos de PostgreSQL iniciados por Patroni.

Además, puedes ajustar los siguientes parámetros de configuración de Patroni:

- `thread_stack_size` - tamaño de pila utilizado por los hilos iniciados por Patroni. Reducir este valor disminuye el uso de memoria del proceso de Patroni. El valor predeterminado establecido por Patroni es `512kB`. Aumenta `thread_stack_size` si Patroni sufre caídas relacionadas con la pila; de lo contrario, el valor predeterminado es suficiente.
- `thread_pool_size` - tamaño del pool de hilos utilizado por Patroni para tareas asíncronas y la comunicación por REST API con otros miembros durante la carrera por el liderazgo o las comprobaciones failsafe. El valor predeterminado es `5`, suficiente para clústeres de tres nodos.
- `restapi.thread_pool_size` - tamaño del pool de hilos utilizado para procesar las solicitudes de la REST API. El valor predeterminado es `5`, lo que permite hasta cinco solicitudes REST API en paralelo. Ten en cuenta que las solicitudes que implican consultas SQL se serializan efectivamente porque se utiliza una única conexión a la base de datos, por lo que aumentar este valor normalmente no aporta ningún beneficio.

--------

Patroni es una plantilla para soluciones de alta disponibilidad (HA) de PostgreSQL utilizando Python. Para máxima accesibilidad, Patroni soporta una variedad de almacenes de configuración distribuidos como [ZooKeeper](https://zookeeper.apache.org/), [etcd](https://github.com/coreos/etcd), [Consul](https://github.com/hashicorp/consul) o [Kubernetes](https://kubernetes.io). Esperamos que resulte útil para ingenieros de bases de datos, DBAs, ingenieros DevOps y SREs que buscan desplegar rápidamente PostgreSQL con HA en centros de datos — o en cualquier otro lugar.

Llamamos a Patroni una «plantilla» porque está lejos de ser un sistema de replicación universal o plug-and-play. Tendrá sus propias advertencias. Úsalo con prudencia. Hay muchas formas de ejecutar alta disponibilidad con PostgreSQL; para ver una lista, consulta la [documentación de PostgreSQL](https://wiki.postgresql.org/wiki/Replication,_Clustering,_and_Connection_Pooling).

Versiones de PostgreSQL soportadas actualmente: de la 9.3 a la 18.

**Nota para usuarios de Citus**: A partir de la versión 3.0, Patroni se integra perfectamente con la extensión de base de datos [Citus](https://github.com/citusdata/citus) para Postgres. Consulta la [página de soporte de Citus](/es/patroni/citus#citus) en la documentación de Patroni para obtener más información sobre cómo utilizar la alta disponibilidad de Patroni junto con un clúster distribuido de Citus.

**Nota para usuarios de Kubernetes**: Patroni puede ejecutarse de forma nativa sobre Kubernetes. Echa un vistazo al capítulo [Kubernetes](/es/patroni/kubernetes#kubernetes) de la documentación de Patroni.

<img src="/img/patroni/patroni-logo.png" width="128" height="128" alt="imagen" />
