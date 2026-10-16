---
title: "Referencia de comandos"
linkTitle: "Comandos"
weight: 40
description: "Referencia de comandos de pgBackRest con todas las opciones para operaciones de copia de seguridad, restauración, archivado y gestión."
icon: fa-solid fa-terminal
sidebar_expanded: true
module: [PGBACKREST]
categories: [Referencia]
upstream_link: "https://pgbackrest.org/command.html"
---

## Introducción {#introduction}

Los comandos se utilizan para ejecutar las diversas funciones de pgBackRest. Aquí las opciones de los comandos se listan de manera exhaustiva, es decir, cada opción aplicable a un comando se lista con ese comando aunque también se aplique a uno o más comandos. Esto incluye todas las opciones que también pueden configurarse en `pgbackrest.conf`.

Las opciones no booleanas configuradas en `pgbackrest.conf` pueden restablecerse a su valor predeterminado en la línea de comandos usando el prefijo `reset-`. Esta función puede utilizarse para restaurar una copia de seguridad directamente en un host del repositorio. Normalmente, pgBackRest dará un error porque detecta que el host de la base de datos es remoto y las restauraciones no pueden realizarse de forma remota. Al añadir `--reset-pg1-host` en la línea de comandos, pgBackRest ignorará el host remoto de la base de datos y restaurará localmente. Puede ser necesario pasar un nuevo `--pg1-path` para forzar que la restauración se realice en una ruta específica, es decir, no la ruta utilizada en el host de la base de datos.

El prefijo `no-` puede usarse para establecer una opción booleana en false en la línea de comandos.

Cualquier opción puede establecerse en una variable de entorno usando el prefijo `PGBACKREST_` y el nombre de la opción en mayúsculas sustituyendo `-` por `_`, por ejemplo, `pg1-path` se convierte en `PGBACKREST_PG1_PATH` y `stanza` se convierte en `PGBACKREST_STANZA`. Las opciones booleanas se representan tal como lo estarían en un archivo de configuración, por ejemplo, `PGBACKREST_COMPRESS="n"`, y las variantes `reset-*` no están permitidas. Las opciones que pueden especificarse varias veces en la línea de comandos o en un archivo de configuración pueden representarse separando los valores con dos puntos, por ejemplo, `PGBACKREST_DB_INCLUDE="db1:db2"`.

Las opciones de la línea de comandos prevalecen sobre las opciones de entorno, que a su vez prevalecen sobre las opciones del archivo de configuración.

Consulta la [Introducción a la configuración](/es/pgbackrest/configuration/#introduction) para obtener información sobre los tipos de opciones

## Comandos {#commands}

| Comando                                                          | Resumen                                                                                 |
|------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| [**`annotate`**](/es/pgbackrest/command/annotate/)             | Añadir, modificar o eliminar anotaciones de copias de seguridad después de crear la copia de seguridad.                  |
| [**`archive-get`**](/es/pgbackrest/command/archive-get/)       | Obtener segmentos WAL archivados para restauración, PITR o recuperación de una réplica.                     |
| [**`archive-push`**](/es/pgbackrest/command/archive-push/)     | Aceptar segmentos WAL de PostgreSQL y enviarlos a los repositorios configurados.           |
| [**`backup`**](/es/pgbackrest/command/backup/)                 | Crear copias de seguridad en el repositorio de destino (por defecto, el repositorio de mayor prioridad).      |
| [**`check`**](/es/pgbackrest/command/check/)                   | Validar la configuración de copia de seguridad/archivado del stanza y el estado del archivado de WAL.                  |
| [**`expire`**](/es/pgbackrest/command/expire/)                 | Expirar copias de seguridad y WAL archivado según las políticas de retención configuradas.                 |
| [**`help`**](/es/pgbackrest/command/help/)                     | Mostrar la ayuda de comandos y opciones a nivel general, de comando o de opción.                      |
| [**`info`**](/es/pgbackrest/command/info/)                     | Mostrar el estado y los metadatos del stanza y de las copias de seguridad en formato texto o JSON.                       |
| [**`repo-get`**](/es/pgbackrest/command/repo-get/)             | Leer archivos del repositorio (como `cat`) para administración, investigación y pruebas.      |
| [**`repo-ls`**](/es/pgbackrest/command/repo-ls/)               | Listar archivos y rutas del repositorio (como `ls`) para administración, investigación y pruebas. |
| [**`restore`**](/es/pgbackrest/command/restore/)               | Restaurar a partir de una copia de seguridad (la más reciente por defecto) con recuperación a un punto en el tiempo opcional.           |
| [**`server`**](/es/pgbackrest/command/server/)                 | Ejecutar el servidor TLS de pgBackRest para acceso a hosts remotos sin SSH.                       |
| [**`server-ping`**](/es/pgbackrest/command/server-ping/)       | Hacer ping a un servidor TLS de pgBackRest para verificar que acepta conexiones.                     |
| [**`stanza-create`**](/es/pgbackrest/command/stanza-create/)   | Crear los metadatos del stanza en todos los repositorios configurados.                                  |
| [**`stanza-delete`**](/es/pgbackrest/command/stanza-delete/)   | Eliminar permanentemente todas las copias de seguridad y archivos archivados de un stanza.                               |
| [**`stanza-upgrade`**](/es/pgbackrest/command/stanza-upgrade/) | Actualizar los metadatos del stanza después de una actualización de versión mayor de PostgreSQL.                       |
| [**`start`**](/es/pgbackrest/command/start/)                   | Permitir de nuevo la ejecución de procesos de pgBackRest después de un `stop` previo.                           |
| [**`stop`**](/es/pgbackrest/command/stop/)                     | Impedir nuevos procesos de pgBackRest y, opcionalmente, forzar la detención de los que están en ejecución.                |
| [**`verify`**](/es/pgbackrest/command/verify/)                 | Verificar que los datos de copia de seguridad y archivado del repositorio son válidos.                         |
| [**`version`**](/es/pgbackrest/command/version/)               | Mostrar la versión instalada de pgBackRest.                                               |
{.full-width}
