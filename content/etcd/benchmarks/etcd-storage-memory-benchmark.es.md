---
title: Benchmark de uso de memoria del almacenamiento
weight: 5125
description: Mediciones de rendimiento del almacenamiento de etcd (índice en memoria y caché de páginas)
categories: [Referencia]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/benchmarks/etcd-storage-memory-benchmark.md"
---

<!---todo: link storage to storage design doc-->
Dos componentes del almacenamiento de etcd consumen memoria física. El proceso de etcd asigna un *índice en memoria* para acelerar la búsqueda de claves. La *caché de páginas* del proceso, gestionada por el sistema operativo, almacena los datos del disco a los que se ha accedido recientemente para su reutilización rápida.

El índice en memoria contiene todas las claves en una estructura de datos de [árbol B][btree], junto con punteros a los datos en disco (los valores). Cada clave del árbol B puede contener varios punteros que apuntan a diferentes versiones de sus valores. El consumo teórico de memoria del índice en memoria puede, por lo tanto, aproximarse con la fórmula:

`N * (c1 + avg_key_size) + N * (avg_versions_of_key) * (c2 + size_of_pointer)`

donde `c1` es la sobrecarga de metadatos de la clave y `c2` es la sobrecarga de metadatos de la versión.

El gráfico muestra la estructura detallada del árbol B del índice en memoria.

```


                                In mem index

                               +------------+
                               | key || ... |
  +--------------+             |     ||     |
  |              |             +------------+
  |              |             | v1  || ... |
  |   disk    <----------------|     ||     | Tree Node
  |              |             +------------+
  |              |             | v2  || ... |
  |           <----------------+     ||     |
  |              |             +------------+
  +--------------+       +-----+    |   |   |
                         |     |    |   |   |
                         |     +------------+
                         |
                         |
                         ^
                      ------+
                      | ... |
                      |     |
                      +-----+
                      | ... | Tree Node
                      |     |
                      +-----+
                      | ... |
                      |     |
                      ------+
```

La memoria de la [caché de páginas][pagecache] está gestionada por el sistema operativo y no se trata en detalle en este documento.

## Entorno de prueba {#testing-environment}

Versión de etcd
- git head https://github.com/etcd-io/etcd/commit/776e9fb7be7eee5e6b58ab977c8887b4fe4d48db

Tipo de máquina GCE n1-standard-2

- 7.5 GB de memoria
- 2x CPUs

## Uso de memoria del índice en memoria {#in-memory-index-memory-usage}

En esta prueba, solo medimos con el benchmark el uso de memoria del índice en memoria. El objetivo es encontrar los valores `c1` y `c2` mencionados anteriormente y comprender el límite estricto de consumo de memoria del almacenamiento.

Calculamos el consumo de memoria mediante la función Go runtime.ReadMemStats. Calculamos la diferencia entre los bytes totales asignados antes de crear el índice y después de crearlo. Esto no puede reflejar perfectamente el uso de memoria del propio índice en memoria, pero sí puede mostrar el patrón de consumo aproximado.

| N    | versiones | tamaño de clave | uso de memoria |
|------|----------|----------|--------------|
| 100K | 1        | 64bytes  | 22MB         |
| 100K | 5        | 64bytes  | 39MB         |
| 1M   | 1        | 64bytes  | 218MB        |
| 1M   | 5        | 64bytes  | 432MB        |
| 100K | 1        | 256bytes | 41MB         |
| 100K | 5        | 256bytes | 65MB         |
| 1M   | 1        | 256bytes | 409MB        |
| 1M   | 5        | 256bytes | 506MB        |


A partir del resultado, podemos calcular `c1=120bytes`, `c2=30bytes`. Solo necesitamos dos conjuntos de datos para calcular `c1` y `c2`, ya que son las únicas variables desconocidas de la fórmula. Los valores `c1=120bytes` y `c2=30bytes` son el valor promedio de los 4 conjuntos de `c1` y `c2` que calculamos. La sobrecarga de metadatos de la clave sigue siendo relativamente considerable (50%) para los pares clave-valor pequeños. Sin embargo, se trata de una mejora significativa con respecto al antiguo almacén, que tenía una sobrecarga de al menos 1000%.

## Uso de memoria global {#overall-memory-usage}

El uso de memoria global refleja cuánta memoria RSS consume etcd con el almacenamiento. El tamaño de los valores debería tener muy poco impacto en el uso de memoria global de etcd, ya que mantenemos los valores en disco y solo retenemos en memoria los valores calientes, gestionados por la caché de páginas del sistema operativo.

| N    | versiones | tamaño de clave | tamaño de valor | uso de memoria |
|------|----------|----------|------------|--------------|
| 100K | 1        | 64bytes  | 256bytes   | 40MB         |
| 100K | 5        | 64bytes  | 256bytes   | 89MB         |
| 1M   | 1        | 64bytes  | 256bytes   | 470MB        |
| 1M   | 5        | 64bytes  | 256bytes   | 880MB        |
| 100K | 1        | 64bytes  | 1KB        | 102MB        |
| 100K | 5        | 64bytes  | 1KB        | 164MB        |
| 1M   | 1        | 64bytes  | 1KB        | 587MB        |
| 1M   | 5        | 64bytes  | 1KB        | 836MB        |

A partir del resultado, sabemos que el tamaño de los valores no influye significativamente en el consumo de memoria. Existe un ligero aumento debido a la mayor cantidad de datos retenidos en la caché de páginas del sistema operativo.

[btree]: https://en.wikipedia.org/wiki/B-tree
[pagecache]: https://en.wikipedia.org/wiki/Page_cache
