---
title: "Formatos de salida"
linkTitle: "Formatos de salida"
weight: 70
description: "Elige salida HTML, texto, binaria, JSON o CSV sin procesar y combina archivos intermedios"
search_keywords: [--anonymize, --csv-separator, --dump-all-queries, --dump-raw-csv, --extension, --extra-files, --last-parsed, --normalized-only, --outfile, --prettify-json, --query-numbering, JSON::XS, all, anonymize, csv, csv-separator, dump, dump-all-queries, dump-raw-csv, extension, extra, extra-files, files, json, last, last-parsed, normalized, normalized-only, numbering, only, outfile, parsed, prettify, prettify-json, queries, query, query-numbering, raw, separator]
icon: fa-solid fa-file-export
module: [PGBADGER]
categories: [Referencia]
upstream_link: "https://github.com/darold/pgbadger/blob/f373ac678c756f66a785c5ab4773d1f05f468d67/README.md"
upstream_name: "pgBadger README.md"
---

pgBadger selecciona la salida a partir de la extensión del nombre de archivo o de `-x` / `--extension`. Usa `-o` / `--outfile` más de una vez para crear varios formatos a partir del mismo análisis.

| Formato | Extensión habitual | Mejor uso |
|---|---|---|
| HTML | `.html` | informe interactivo y legible por humanos, con gráficos |
| Texto | `.txt` | revisión en terminal y salida de archivo plano |
| Binario | `.bin` | estadísticas intermedias combinables y reconstrucción de informes |
| JSON | `.json` | integración con otro software; requiere `JSON::XS` |
| CSV sin procesar | archivo de salida elegido | extracción orientada a filas con `--dump-raw-csv` |

## HTML y texto {#html-and-text}

La salida predeterminada es `out.html`:

```console
$ pgbadger postgresql.log -o report.html
```

HTML normalmente incrusta los scripts, estilos, fuentes y datos del informe necesarios para una visualización autónoma. `-X` / `--extra-files` saca el JavaScript y el CSS compartidos de los informes incrementales; conserva esos recursos junto al árbol HTML.

Genera texto de forma explícita:

```console
$ pgbadger -x text -o report.txt postgresql.log
```

Usa `-` como nombre del archivo de salida para escribir un formato admitido en la salida estándar.

## Datos intermedios binarios {#binary-format}

La salida binaria separa el análisis de la presentación. Genera incrementos por hora a partir de un registro diario creciente:

```console
$ pgbadger --last-parsed .pgbadger_last_state \
    -o sunday/hour01.bin \
    /var/log/pgsql/postgresql-Sun.log
```

Combina uno o más archivos binarios en un informe nuevo:

```console
$ pgbadger -o sunday.html sunday/*.bin
```

Cuando el servidor escribe un archivo de registro por hora, crea un archivo binario por cada rotación y reconstruye el HTML acumulativo cuando sea necesario:

```console
$ pgbadger -o day1/hour01.bin postgresql-2026-08-15_01.log
$ pgbadger -o day1/hour02.bin postgresql-2026-08-15_02.log
$ pgbadger -o day1/hour03.bin postgresql-2026-08-15_03.log
$ pgbadger -o day1.html day1/*.bin
```

Conserva juntos los archivos binarios de versiones de pgBadger compatibles. Lee las notas de versión sobre compatibilidad del formato incremental antes de actualizar un directorio de informes de larga vida.

## JSON {#json-format}

La salida JSON está pensada para consumidores programáticos, como canalizaciones de monitorización o de informes:

```console
$ pgbadger -o report.json postgresql.log
```

Instala primero `JSON::XS`. Añade `--prettify-json` para mejorar la legibilidad cuando el tamaño del archivo y el tiempo de generación sean secundarios.

## Exportaciones sin procesar y orientadas a consultas {#raw-exports}

La referencia de comandos también proporciona exportaciones especializadas:

- `--dump-raw-csv` analiza el registro y escribe CSV orientado a filas sin generar un informe;
- `--csv-separator` cambia el delimitador del CSV sin procesar, que por defecto es una coma en 13.2;
- `--dump-all-queries` emite cada consulta tras sustituir los parámetros de enlace;
- `--normalized-only` escribe las consultas normalizadas;
- `--query-numbering` numera la salida de texto orientada a consultas.

Estos modos pueden contener SQL de aplicaciones, identificadores, usuarios, direcciones de clientes o valores literales. Revisa la salida antes de compartirla y usa `--anonymize` cuando el análisis previsto no requiera literales.

