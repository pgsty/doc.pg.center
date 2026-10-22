---
title: "Documentación de la instantánea de desarrollo de pgBadger 13.2"
linkTitle: pgBadger
weight: 40
description: "Análisis rápido de registros de PostgreSQL y PgBouncer con informes detallados y autónomos"
search_keywords: [csvlog, jsonlog, logplex, stderr, syslog]
icon: fa-solid fa-otter
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
module: [PGBADGER]
categories: [Concepto]
aliases: [/pgbadger/documentation/]
upstream_source: pgbadger
upstream_ref: "v13.2 development snapshot, commit f373ac6 (unreleased)"
upstream_link: "https://github.com/darold/pgbadger/tree/f373ac678c756f66a785c5ab4773d1f05f468d67"
cascade:
  upstream_source: pgbadger
  upstream_ref: "v13.2 development snapshot, commit f373ac6 (unreleased)"
  type: docs
  module: [PGBADGER]
---

Este manual sigue la [instantánea de desarrollo no publicada `f373ac6`](https://github.com/darold/pgbadger/tree/f373ac678c756f66a785c5ab4773d1f05f468d67), cuyo commit se realizó el 2026-10-21 (UTC), después de la [versión estable 13.2](https://github.com/darold/pgbadger/releases/tag/v13.2) del 2025-12-29. Las funciones descritas para esta instantánea, como el filtrado remoto en modo de vigilancia y los directorios codificados de informes por base de datos, no forman parte del archivo de la versión 13.2.

![logo de pgBadger](/img/pgbadger/logo.png "pgBadger")

**pgBadger** es un analizador de registros de PostgreSQL rápido e independiente, escrito en Perl. Lee registros de PostgreSQL o PgBouncer y produce salidas detalladas en formato HTML, texto, binario, JSON o CSV sin procesar. Los informes HTML son autónomos, interactivos, con zoom, y solo necesitan un navegador web para visualizarse.

## Por qué pgBadger {#why-pgbadger}

pgBadger está diseñado para registros de gran tamaño y uso operativo:

- un solo programa en Perl, sin módulos obligatorios fuera de la biblioteca estándar de Perl;
- detección automática de entrada `stderr`, `syslog`, `csvlog`, `jsonlog`, RDS, Cloud SQL, logplex, Redshift y PgBouncer;
- lectura directa de archivos locales, entrada estándar, archivos remotos por SSH, y URL HTTP, FTP o SFTP;
- entrada comprimida con gzip, bzip2, lz4, xz, zip y zstd;
- análisis en paralelo de un archivo grande o de muchos archivos pequeños;
- informes incrementales diarios, semanales y mensuales a petición;
- filtros por fecha y hora, base de datos, usuario, cliente, aplicación, proceso, sesión y patrón de consulta.

## Qué contienen los informes {#report-coverage}

El conjunto de informes de PostgreSQL cubre:

- actividad general y estadísticas de consultas;
- consultas lentas, frecuentes, que consumen mucho tiempo, en espera y canceladas;
- archivos temporales, checkpoints, bloqueos, sesiones y conexiones;
- actividad de autovacuum y autoanalyze por tabla;
- errores y eventos por gravedad y clase;
- distribuciones por base de datos, usuario, cliente, aplicación y tipo de sentencia.

La entrada de PgBouncer añade rendimiento, duración promedio de las consultas, sesiones simultáneas, distribuciones de conexiones y sesiones, uso del pool reservado, e informes de errores y eventos más frecuentes.

## Mapa de la documentación {#documentation-map}

Lee el manual en este orden, o usa la barra lateral para saltar directamente a una tarea:

1. [Descarga e instala](/es/pgbadger/download/) pgBadger y sus módulos opcionales.
2. Revisa la referencia completa de la [línea de comandos](/es/pgbadger/command-line/).
3. Configura el [registro de PostgreSQL](/es/pgbadger/postgresql-logging/) con un prefijo analizable.
4. Elige el modo de [procesamiento en paralelo](/es/pgbadger/parallel-processing/) adecuado.
5. Genera [informes incrementales](/es/pgbadger/incremental-reports/) de forma segura.
6. Selecciona un [formato de salida](/es/pgbadger/output-formats/) e inspecciona los [ejemplos locales](/es/pgbadger/sample-reports/).
7. Sigue el [historial de versiones](/es/pgbadger/releases/), el [soporte](/es/pgbadger/support/) y la [licencia](/es/pgbadger/license/).

## Enlaces al proyecto upstream {#upstream-links}

- [Sitio web del proyecto](https://pgbadger.darold.net/)
- [Código fuente](https://github.com/darold/pgbadger)
- [Versiones](https://github.com/darold/pgbadger/releases)
- [Seguimiento de incidencias](https://github.com/darold/pgbadger/issues)
