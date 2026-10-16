---
title: "Documentación de PgBouncer 1.26.0"
linkTitle: PgBouncer
weight: 30
description: >
  PgBouncer - Pool de conexiones ligero para PostgreSQL
icon: fa-solid fa-arrows-turn-to-dots
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
module: [PGBOUNCER]
categories: [Concepto]
upstream_source: pgbouncer
upstream_ref: v1.26.0
upstream_link: "https://www.pgbouncer.org/"
cascade:
  upstream_source: pgbouncer
  upstream_ref: v1.26.0
  type: docs
  module: [PGBOUNCER]
---

Este manual está basado en [PgBouncer 1.26.0](https://github.com/pgbouncer/pgbouncer/releases/tag/pgbouncer_1_26_0), publicado el 2026-09-23. Consulta las [notas de la versión](/es/pgbouncer/changelog/#pgbouncer-126x) para ver los cambios respecto a las versiones anteriores.

**pgbouncer** es un pool de conexiones de PostgreSQL. Cualquier aplicación de destino
puede conectarse a **pgbouncer** como si fuera un servidor PostgreSQL, y **pgbouncer**
creará una conexión al servidor real, o bien reutilizará una de sus conexiones
existentes.

El objetivo de **pgbouncer** es reducir el impacto en el rendimiento que supone abrir
nuevas conexiones a PostgreSQL.

Para no comprometer la semántica transaccional en la agrupación de conexiones,
**pgbouncer** admite varios tipos de agrupación al rotar las conexiones:

- **Agrupación por sesiones**: el método más cortés. Cuando un cliente se conecta, se le asigna una conexión de servidor durante todo el tiempo que permanezca conectado. Cuando el cliente se desconecta, la conexión de servidor se devuelve al pool. Este es el método predeterminado.
- **Agrupación por transacciones**: una conexión de servidor se asigna a un cliente solo durante una transacción. Cuando PgBouncer detecta que la transacción ha terminado, la conexión de servidor se devuelve al pool.
- **Agrupación por instrucciones**: el método más agresivo. La conexión de servidor se devuelve al pool inmediatamente después de que se completa una consulta. En este modo no se permiten transacciones de varias instrucciones.
