---
title: "Procesamiento en paralelo"
linkTitle: "Procesamiento en paralelo"
weight: 50
description: "Elige entre fragmentos en paralelo de un registro y el procesamiento en paralelo de muchos registros"
search_keywords: [--Jobs, --jobs, --tempdir, Jobs, jobs, tempdir]
icon: fa-solid fa-gauge-high
module: [PGBADGER]
categories: [Tarea]
upstream_link: "https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

pgBadger tiene dos modos de multiprocesamiento complementarios. Elige según la forma de la entrada, no simplemente según el número de CPU.

| Opción | Unidad en paralelo | Mejor encaje | Restricción principal |
|---|---|---|---|
| `-j N` / `--jobs N` | fragmentos de un archivo de registro | un registro grande, con acceso aleatorio (seekable) | los límites de los fragmentos pueden duplicar u omitir un pequeño número de consultas |
| `-J N` / `--Jobs N` | archivos de registro completos | muchos registros independientes | solo resulta útil cuando hay suficientes archivos para mantener ocupados a los trabajadores |

## Divide un archivo grande con `-j` {#single-file-jobs}

```console
$ pgbadger -j 8 /var/log/postgresql/postgresql.log
```

El algoritmo upstream divide cada archivo en `N` rangos de bytes, crea (fork) un analizador por rango, escribe estadísticas binarias temporales y luego combina esas estadísticas en el informe final.

```text
para cada archivo de registro
    dividir el archivo en N fragmentos
    encontrar los desplazamientos de inicio y fin de cada fragmento
    crear (fork) N analizadores en esos desplazamientos
    escribir un archivo temporal de estadísticas binarias por analizador
esperar a los trabajadores
fusionar los archivos binarios y generar el informe
```

Como los registros del log y las sentencias multilínea no se alinean perfectamente con los desplazamientos de bytes, hasta aproximadamente `N` consultas por archivo pueden quedar truncadas, omitirse o —lo más común— contarse dos veces en los límites de los fragmentos. Usa este modo para el análisis agregado de archivos muy grandes, no para un flujo de trabajo que requiera un recuento forense exacto de cada registro.

## Procesa muchos archivos con `-J` {#multiple-file-jobs}

```console
$ pgbadger -J 8 /var/log/postgresql/postgresql-*.log
```

Cada trabajador posee un archivo completo, por lo que este modo evita el hueco de los límites de fragmentos. Resulta más útil con cientos de archivos pequeños y suficiente capacidad de CPU y de E/S. La documentación upstream también permite `-J` para archivos comprimidos independientes; la división de un único archivo con `-j` requiere una entrada sin comprimir y con acceso aleatorio.

## Prueba de rendimiento upstream {#benchmark}

El manual upstream reporta estas mediciones en un host de 8 CPU. Tómalas como una comparación de los dos algoritmos, no como una predicción para el hardware actual.

Un archivo de 9.5 GB:

| Opción | 1 CPU | 2 CPU | 4 CPU | 8 CPU |
|---|---:|---:|---:|---:|
| `-j` | 1h41m18 | 50m25 | 25m39 | 15m58 |
| `-J` | 1h41m18 | 54m28 | 41m16 | 34m45 |

Doscientos archivos de 10 MB, 2 GB en total:

| Opción | 1 CPU | 2 CPU | 4 CPU | 8 CPU |
|---|---:|---:|---:|---:|
| `-j` | 20m15 | 9m56 | 5m20 | 4m20 |
| `-J` | 20m15 | 9m49 | 5m00 | 2m40 |

El valor predeterminado práctico es `-j` para pocos archivos grandes y `-J` para muchos archivos pequeños. Ambos modos pueden combinarse cuando la entrada y la plataforma lo admiten, pero haz una prueba de rendimiento de la combinación: el análisis de registros puede quedar limitado por el rendimiento del almacenamiento antes que por la CPU.

## Límites y archivos temporales {#limits-and-temporary-files}

- `-j` no está disponible para entrada comprimida o CSV y depende del fork de procesos, por lo que no es un modo para Windows.
- El análisis de CSV remoto no está admitido por la ruta de entrada remota upstream.
- El análisis en paralelo crea archivos temporales con nombres como `tmp_pgbadgerXXXX.bin` bajo el directorio temporal seleccionado (por defecto, el directorio temporal del sistema).
- No limpies esos archivos mientras pgBadger se está ejecutando. Usa `--tempdir` para ubicarlos en un almacenamiento con capacidad suficiente.
- Comienza con un número modesto de trabajadores y vigila la CPU, el rendimiento de lectura, el consumo de espacio temporal y el tiempo transcurrido.

