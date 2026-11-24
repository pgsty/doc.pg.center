---
title: "Descarga e instalación"
linkTitle: "Descargar e instalar"
weight: 20
description: "Versiones oficiales, paquetes, requisitos e instalación desde el código fuente"
search_keywords: [--content-size, --help, --robot, --version, --zcat, JSON::XS, Text::CSV_XS, content, content-size, help, robot, size, version, zcat, zstdcat]
icon: fa-solid fa-cloud-arrow-down
module: [PGBADGER]
categories: [Tutorial]
upstream_link: "https://github.com/darold/pgbadger/blob/0514893e97296695c77755fa36c59288c3afef3e/README.md"
upstream_name: "pgBadger README.md"
---

## Elige un canal de distribución {#distribution-channels}

| Canal | Úsalo para | Ubicación |
|---|---|---|
| Versión oficial | Archivos fuente comprimidos y notas de versión | [GitHub Releases](https://github.com/darold/pgbadger/releases) |
| Paquete RPM | Distribuciones Linux basadas en RPM | [PostgreSQL Yum Repository](https://yum.postgresql.org/packages/) |
| Paquete Debian/Ubuntu | Distribuciones Linux basadas en APT | [PostgreSQL Apt Repository](https://wiki.postgresql.org/wiki/Apt) |
| Código fuente de desarrollo | Código actual aún no publicado | [darold/pgbadger](https://github.com/darold/pgbadger) |
{.wide .expand}

La última versión estable comprobada el 2026-11-21 es [pgBadger 13.3](https://github.com/darold/pgbadger/releases/tag/v13.3), publicada el 2026-11-03. Tanto el ejemplo con el archivo de versión como el checkout fijado que aparece más abajo instalan esta versión documentada.

## Requisitos {#requirements}

La ruta del informe HTML solo necesita:

- una distribución de Perl moderna;
- un navegador web para mostrar los gráficos JavaScript incrustados.

Las capacidades opcionales añaden las siguientes dependencias:

| Capacidad | Dependencia |
|---|---|
| Analizar registros CSV de PostgreSQL | `Text::CSV_XS` |
| Generar salida JSON | `JSON::XS` |
| Leer entrada `.gz`, `.bz2`, `.lz4`, `.xz`, `.zip` o `.zst` | la utilidad correspondiente: `zcat`, `bzcat`, `lz4cat`, `xz`, `unzip` o `zstdcat` |

Instala el soporte de JSON en Debian o Ubuntu:

```console
$ sudo apt-get install libjson-xs-perl
```

En un sistema basado en RPM:

```console
$ sudo yum install perl-JSON-XS
```

Usa `--zcat` para redefinir la ruta de un descompresor. Proporcionar un comando personalizado desactiva la combinación de distintos formatos comprimidos en la misma invocación.

La utilidad `xz` debe admitir `--robot` para que pgBadger pueda leer los metadatos del archivo. Comprime los registros lz4 con `--content-size` para que pgBadger pueda determinar su tamaño descomprimido.

## Instalar desde un archivo oficial {#install-from-tarball}

Descarga un archivo de versión y luego compila e instala el programa con el conjunto de herramientas estándar de Perl:

```console
$ tar xzf pgbadger-13.3.tar.gz
$ cd pgbadger-13.3
$ perl Makefile.PL
$ make
$ sudo make install
```

La distribución `site` predeterminada instala el programa como `/usr/local/bin/pgbadger` y la página del manual como `/usr/local/share/man/man1/pgbadger.1`.

Para una instalación al estilo de las distribuciones bajo `/usr`, genera el Makefile con:

```console
$ perl Makefile.PL INSTALLDIRS=vendor
$ make
$ sudo make install
```

`INSTALLDIRS=perl` es otra distribución admitida por el proyecto upstream. Inspecciona las rutas generadas antes de instalar en un sistema gestionado.

## Instalar desde la fuente fijada {#install-development-code}

```console
$ git clone https://github.com/darold/pgbadger.git
$ cd pgbadger
$ git checkout --detach 0514893e97296695c77755fa36c59288c3afef3e
$ perl Makefile.PL
$ make
$ make test
$ sudo make install
```

Este checkout corresponde a [la versión documentada v13.3](https://github.com/darold/pgbadger/releases/tag/v13.3), fijada en `0514893e97296695c77755fa36c59288c3afef3e`.

## Verifica la instalación {#verify-installation}

```console
$ pgbadger --version
$ pgbadger --help
```

Continúa con la [referencia de la línea de comandos](/es/pgbadger/command-line/) y la [configuración del registro de PostgreSQL](/es/pgbadger/postgresql-logging/).
