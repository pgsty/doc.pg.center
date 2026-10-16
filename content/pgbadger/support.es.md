---
title: "Soporte y contribución"
linkTitle: "Soporte"
weight: 100
description: "Reporta errores, solicita funcionalidades, contribuye parches y encuentra soporte profesional de PostgreSQL"
search_keywords: [--help, help]
icon: fa-solid fa-life-ring
module: [PGBADGER]
categories: [Tarea]
upstream_link: "https://pgbadger.darold.net/#support"
upstream_name: "pgBadger website"
upstream_ref: "site snapshot of 2026-08-15"
---

pgBadger se mantiene como un proyecto abierto. Los informes de errores, las propuestas de funcionalidades, las correcciones de documentación y los parches se gestionan a través del repositorio GitHub upstream.

## Errores y solicitudes de funcionalidades {#bugs-and-features}

1. Actualiza a la versión publicada más reciente y confirma que el comportamiento sigue produciéndose.
2. Busca una respuesta existente en las [incidencias abiertas](https://github.com/darold/pgbadger/issues) y las [incidencias cerradas](https://github.com/darold/pgbadger/issues?q=is%3Aissue+is%3Aclosed).
3. Reduce el problema a la muestra de registro segura más pequeña y a la línea de comandos que aún lo reproducen.
4. Elimina las credenciales, el SQL sensible, los valores de enlace, los nombres de host, las direcciones y los datos de negocio.
5. Abre una [nueva incidencia](https://github.com/darold/pgbadger/issues/new) con la versión de pgBadger, el sistema operativo, el formato de entrada, las opciones exactas, el resultado observado y el resultado esperado.

En caso de caídas o errores del analizador, incluye solo las líneas de registro mínimas y depuradas necesarias para reproducir el caso límite. Un registro de producción completo o un informe generado rara vez resulta adecuado para una incidencia pública.

## Contribuir con un parche {#contribute-a-patch}

El proyecto incluye un archivo `.editorconfig` para un espaciado coherente. Mantén alineadas la ayuda de los comandos, la documentación POD y la documentación Markdown generada cuando un cambio afecte a un comportamiento visible para el usuario.

El flujo de trabajo de la documentación upstream es:

```console
$ perl Makefile.PL
$ make README
```

`doc/pgBadger.pod` es la fuente principal de la documentación extensa. `pgbadger --help` proporciona la sinopsis, mientras que los archivos README son vistas generadas. Ejecuta las pruebas pertinentes antes de enviar un pull request.

- [Repositorio de código fuente](https://github.com/darold/pgbadger)
- [Pull requests](https://github.com/darold/pgbadger/pulls)
- [Guía de contribución](https://github.com/darold/pgbadger/blob/master/CONTRIBUTING.md)
- [Notas de desarrollo](https://github.com/darold/pgbadger/blob/master/HACKING.md)

## Soporte comercial {#commercial-support}

El proyecto pgBadger no promete mantenimiento ni soporte según su licencia. Para obtener ayuda de pago con el registro de PostgreSQL, el análisis de rendimiento o la automatización de informes, consulta el [directorio de servicios profesionales de PostgreSQL](https://www.postgresql.org/support/professional_support/).

