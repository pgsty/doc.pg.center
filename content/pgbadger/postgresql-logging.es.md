---
title: "Configuración del registro de PostgreSQL"
linkTitle: "Registro de PostgreSQL"
weight: 40
description: "Configura el registro de consultas, log_line_prefix, la configuración regional y las estadísticas de apoyo para pgBadger"
search_keywords: [--prefix, lc_messages, log_autovacuum_min_duration, log_checkpoints, log_connections, log_disconnections, log_duration, log_error_verbosity, log_line_prefix, log_lock_waits, log_min_duration_statement, log_statement, log_temp_files, prefix, stderr, syslog]
icon: fa-solid fa-database
module: [PGBADGER]
categories: [Tarea]
upstream_link: "https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

pgBadger solo puede informar sobre la información que PostgreSQL escribe en el registro. Comienza con un prefijo analizable y una política deliberada de registro de sentencias, y luego añade los eventos operativos que quieras analizar.

## Registro mínimo de consultas {#minimum-query-logging}

Para incluir el texto y la duración de las consultas, activa el registro de sentencias basado en la duración:

```postgresql
log_min_duration_statement = 0
```

`0` registra cada sentencia completada. En un servidor con mucha carga, elige un umbral más alto en milisegundos para controlar el volumen del registro. Mide la sobrecarga y el crecimiento del almacenamiento antes de habilitar un umbral bajo en producción.

Si solo necesitas la duración y el número de consultas, y no el texto de las consultas, usa:

```postgresql
log_min_duration_statement = -1
log_duration = on
```

Prefiere `log_min_duration_statement` cuando necesites los informes de consultas más lentas y de tiempo total de consulta.

## Campos de prefijo obligatorios {#required-prefix-fields}

Un `log_line_prefix` personalizado debe incluir ambos:

- un campo de tiempo: `%t`, `%m` o `%n`;
- un campo de proceso o sesión: `%p` o `%c`.

Un prefijo `stderr` mínimo es:

```postgresql
log_line_prefix = '%t [%p]: '
```

Un prefijo más útil registra el usuario, la base de datos, la aplicación y el cliente:

```postgresql
log_line_prefix = '%t [%p]: user=%u,db=%d,app=%a,client=%h '
```

El prefijo equivalente para un destino syslog omite la marca de tiempo y los campos de proceso que syslog ya proporciona:

```postgresql
log_line_prefix = 'user=%u,db=%d,app=%a,client=%h '
```

Otro orden de claves admitido es:

```postgresql
log_line_prefix = '%t [%p]: db=%d,user=%u,app=%a,client=%h '
```

Cuando tu prefijo no sea una de las formas reconocidas por pgBadger, pasa el valor exacto con `--prefix`. No lo simplifiques ni lo reescribas de forma distinta a como aparece en `postgresql.conf`.

## Ajustes de eventos recomendados {#recommended-event-settings}

Activa las clases de eventos que quieras que aparezcan en el informe:

```postgresql
log_checkpoints = on
log_connections = on
log_disconnections = on
log_lock_waits = on
log_temp_files = 0
log_autovacuum_min_duration = 0
log_error_verbosity = default
```

Estos ajustes pueden generar un volumen considerable de registro. En particular, `log_temp_files = 0` y `log_autovacuum_min_duration = 0` registran cada evento que cumple los criterios; ajústalos para que se ajusten a la carga de trabajo y al presupuesto de retención.

## Mantén los mensajes del servidor en inglés {#message-locale}

El analizador reconoce los mensajes del servidor PostgreSQL en inglés. Usa:

```postgresql
lc_messages = 'en_US.UTF-8'
```

o:

```postgresql
lc_messages = 'C'
```

Las configuraciones regionales como `fr_FR.UTF-8` no son compatibles con el analizador del proyecto original.

## Evita conflictos entre los ajustes de sentencias {#statement-setting-conflicts}

No actives `log_min_duration_statement`, `log_duration` y `log_statement = 'all'` a la vez. Una misma ejecución puede registrarse más de una vez, lo que infla los contadores de pgBadger y aumenta considerablemente el volumen del registro.

| Objetivo | Ajuste recomendado |
|---|---|
| Texto de consulta con tiempos | `log_min_duration_statement = 0` o un umbral elegido |
| Solo duración y recuento | `log_min_duration_statement = -1`, `log_duration = on` |
| Auditoría amplia de sentencias | Trata `log_statement` como una política de registro separada; no combines los tres ajustes para las estadísticas de pgBadger |

Tras recargar PostgreSQL, inspecciona varias entradas reales del registro antes de ejecutar un análisis grande. Comprueba que los campos de marca de tiempo, identificador de proceso/sesión, usuario, base de datos, aplicación y cliente coinciden con el formato seleccionado.
