---
title: "Características"
weight: 10
description: "Características de PgBouncer — modos de agrupación y compatibilidad SQL"
icon: fa-solid fa-wand-magic-sparkles
module: [PGBOUNCER]
categories: [Concepto]
upstream_link: "https://www.pgbouncer.org/features.html"
---

- Varios niveles de dureza al rotar las conexiones:

  **Agrupación de sesiones**
  : El método más cortés. Cuando un cliente se conecta, se le asigna una conexión de servidor durante todo el tiempo que permanezca conectado. Cuando el cliente se desconecta, la conexión de servidor se devuelve al pool. Este modo admite todas las características de PostgreSQL.

  **Agrupación de transacciones**
  : Una conexión de servidor se asigna a un cliente solo durante una transacción. Cuando PgBouncer detecta que la transacción ha terminado, el servidor se devuelve al pool. Este modo rompe algunas características de PostgreSQL basadas en sesión. Solo puedes usarlo cuando la aplicación coopera no utilizando las características que se rompen. Consulta la tabla siguiente para ver las características incompatibles.

  **Agrupación de instrucciones**
  : El método más agresivo. Es la agrupación de transacciones con un matiz: las transacciones de múltiples instrucciones no están permitidas. Está pensado para imponer el modo «autocommit» en el cliente, dirigido principalmente a PL/Proxy.

- Requisitos de memoria bajos (2 kB por conexión de forma predeterminada). Esto se debe a que PgBouncer no necesita ver los paquetes completos de una sola vez.

- No está ligado a un único servidor backend. Las bases de datos de destino pueden residir en hosts diferentes.

- Admite reconfiguración en línea para la mayoría de los parámetros.

- Admite [reinicios y actualizaciones progresivos](/es/pgbouncer/usage/#shutdown-wait_for_clients) mediante varios procesos con [`so_reuseport`](/es/pgbouncer/config/#so_reuseport). El antiguo reinicio en línea (`-R`) se eliminó en 1.26.0.

--------

## Mapa de características SQL para los modos de agrupación {#sql-feature-map-for-pooling-modes}

La siguiente tabla enumera diversas características de PostgreSQL y su compatibilidad con los modos de agrupación de PgBouncer. Ten en cuenta que la agrupación de *transacciones* rompe *por diseño* las expectativas del cliente sobre el servidor y solo puede usarse si la aplicación coopera evitando las características que no funcionan.

| Característica                    | Agrupación de sesiones | Agrupación de transacciones |
|-----------------------------------|:---------------------:|:---------------------------:|
| Parámetros de inicio [^0]         | Sí                    | Sí                          |
| SET/RESET                         | Sí                    | Para los parámetros con seguimiento [^0] |
| LISTEN                            | Sí                    | Nunca                       |
| NOTIFY                            | Sí                    | Sí                          |
| Cursor WITHOUT HOLD               | Sí                    | Sí                          |
| Cursor WITH HOLD                  | Sí                    | Nunca                       |
| Planes preparados a nivel de protocolo | Sí               | Sí [^1]                     |
| PREPARE / DEALLOCATE              | Sí                    | Nunca                       |
| Tablas temporales ON COMMIT DROP  | Sí                    | Sí                          |
| Tablas temporales PRESERVE/DELETE ROWS | Sí                | Nunca                       |
| Restablecimiento de planes en caché | Sí                  | Sí                          |
| Instrucción LOAD                  | Sí                    | Nunca                       |
| Bloqueos consultivos a nivel de sesión | Sí                | Nunca                       |

[^0]: Desde la versión 1.26.0, PgBouncer realiza un seguimiento de todos los parámetros reportados por el servidor que los clientes pueden modificar: `application_name`, `client_encoding`, `DateStyle`, `default_transaction_read_only` (PostgreSQL 14+), `IntervalStyle`, `scram_iterations` (PostgreSQL 16+), `search_path` (PostgreSQL 18+), `session_authorization`, `standard_conforming_strings` y `TimeZone`. Para los parámetros que el servidor no reporta, solo se realiza el seguimiento de los valores de inicio; los cambios posteriores con `SET` no se rastrean. Consulta [`track_extra_parameters`](/es/pgbouncer/config/#track_extra_parameters) e [`ignore_startup_parameters`](/es/pgbouncer/config/#ignore_startup_parameters) para más detalles y para los parámetros proporcionados por extensiones.

[^1]: La compatibilidad con instrucciones preparadas a nivel de protocolo se activa cuando [`max_prepared_statements`](/es/pgbouncer/config/#max_prepared_statements) es distinto de cero. El valor predeterminado es 200; establecerlo en 0 desactiva esta compatibilidad. `PREPARE` / `DEALLOCATE` a nivel SQL sigue siendo incompatible con la agrupación de transacciones, excepto `DEALLOCATE ALL` y `DISCARD ALL` cuando el seguimiento está activado.
