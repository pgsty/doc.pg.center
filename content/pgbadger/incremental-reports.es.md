---
title: "Informes incrementales"
linkTitle: "Informes incrementales"
weight: 60
description: "Genera informes diarios y semanales, controla la retención, reconstruye la salida y añade resúmenes mensuales"
search_keywords: [--day-report, --explode, --extra-files, --incremental, --iso-week-number, --last-parsed, --month-report, --no-week, --noreport, --outdir, --rebuild, --retention, --start-monday, day, day-report, explode, extra, extra-files, files, incremental, iso, iso-week-number, last, last-parsed, monday, month, month-report, no, no-week, noreport, number, outdir, parsed, rebuild, report, retention, start, start-monday, week]
icon: fa-solid fa-calendar-days
module: [PGBADGER]
categories: [Tarea]
upstream_link: "https://github.com/darold/pgbadger/blob/f373ac678c756f66a785c5ab4773d1f05f468d67/README.md"
upstream_name: "pgBadger README.md"
---

El modo incremental almacena las estadísticas analizadas en formato binario y luego genera un informe HTML por día, un informe acumulativo por semana y un índice de estilo calendario que los enlaza. Está pensado para el procesamiento repetido de registros rotados sin contar de nuevo las mismas entradas.

## Genera informes diarios y semanales {#daily-and-weekly}

Ejecuta pgBadger después de la rotación diaria del registro y proporciona un directorio de salida persistente:

```cron {title="crontab"}
0 4 * * * /usr/bin/pgbadger -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

`-I` activa el modo incremental y `-O` selecciona el directorio que contiene el estado binario, el índice de calendario y los informes generados. pgBadger mantiene su propio estado incremental en ese directorio, por lo que `--last-parsed` no es necesario salvo que deliberadamente quieras el archivo de estado en otro lugar.

Usa un directorio HTML separado conservando el estado binario en el directorio original:

```console
$ pgbadger -I -O /var/lib/pgbadger/data -H /var/www/pg_reports postgresql.log.1
```

Trata los archivos binarios como datos de origen para reconstrucciones futuras. Haz una copia de seguridad de ellos o conserva los registros originales si te importa poder regenerar los informes.

## Retención {#retention}

Conserva solo un número elegido de semanas:

```console
$ pgbadger --incremental --retention 8 \
    --outdir /var/www/pg_reports \
    /var/log/postgresql/postgresql.log.1
```

Los directorios de semanas y días más antiguos se eliminan automáticamente. Prueba la política sobre una copia que no sea de producción antes de activarla en torno a tu único historial de informes.

## Escribe los recursos compartidos por separado {#shared-assets}

De forma predeterminada, los informes HTML incrustan su JavaScript y su CSS. En un directorio que contenga muchos informes incrementales, `-X` / `--extra-files` escribe los recursos compartidos por separado y reduce la salida duplicada:

```console
$ pgbadger -X -I -O /var/www/pg_reports postgresql.log.1
```

Todos los informes y su directorio de recursos versionado deben moverse juntos.

## Informes por base de datos {#per-database-reports}

Con `-E` / `--explode`, los informes de cada base de datos se almacenan en un subdirectorio del directorio de salida que lleva el nombre de la base de datos. En la instantánea de desarrollo posterior a 13.2 documentada aquí, los nombres de bases de datos que no son seguros como rutas se codifican con porcentajes: `/`, `\`, `%` y los caracteres de control; un punto inicial; los nombres puramente numéricos; y los nombres de archivos que pgBadger escribe en el directorio de salida, como `LAST_PARSED`. Los nombres habituales de bases de datos no cambian.

Por ejemplo, la base de datos `2025` usa el directorio `%32025`, y la base de datos `../foo` usa `%2E.%2Ffoo`. Como estos nombres de directorio contienen signos de porcentaje, cada `%` debe escribirse como `%25` en la URL del informe:

```text
https://myserver/pg_reports/%2532025/index.html
```

pgBadger muestra una advertencia con el directorio y la ruta de la URL cuando crea uno de estos directorios por primera vez. En las ejecuciones posteriores, el mensaje solo aparece en el modo de depuración, para evitar mensajes repetidos en los trabajos incrementales programados.

## Reconstruye informes existentes {#rebuild}

Tras actualizar pgBadger o aplicar una corrección en la generación de informes, reconstruye el HTML a partir de los datos binarios conservados:

```console
$ rm /var/www/pg_reports/*.js
$ rm /var/www/pg_reports/*.css
$ pgbadger -X -I -O /var/www/pg_reports --rebuild
```

Usa de nuevo `-E` / `--explode` si los informes originales se generaron por base de datos.

> Usa la opción larga `--rebuild`. En la referencia de comandos actual, `-R` significa `--retention`; tratar `-R` como un atajo de reconstrucción aplicaría la opción equivocada.

## Añade un informe mensual {#monthly-reports}

Los informes diarios y semanales son automáticos. La agregación mensual es explícita porque puede resultar costosa para un historial grande:

```console
$ pgbadger -X --month-report 2026-07 /var/www/pg_reports/
```

El mes generado se añade al índice de calendario. Volver a ejecutar el comando reconstruye ese mes a partir de los datos binarios disponibles. Para un historial por base de datos, repite `-E`:

```console
$ pgbadger -E -X --month-report 2026-07 /var/www/pg_reports/
```

La referencia completa de comandos también proporciona `--day-report YYYY-MM-DD`, `--no-week`, `--noreport`, `--start-monday` y `--iso-week-number` para programaciones más especializadas.

Abre el [ejemplo de informe incremental incluido](/third_party/pgbadger/examples/report/index.html) para inspeccionar el calendario, los enlaces semanales y la jerarquía de informes diarios sin conexión de red.

