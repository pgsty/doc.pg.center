---
title: Benchmark del uso de memoria de watch
weight: 5250
description: Mediciones de rendimiento de los watchers de etcd
categories: [Referencia]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/benchmarks/etcd-3-watch-memory-benchmark.md"
---

> [!NOTE]
> Las funciones de watch están en desarrollo activo y su uso de memoria puede cambiar a medida que progrese ese desarrollo. No esperamos que aumente significativamente más allá de las cifras indicadas a continuación.

Un objetivo principal de etcd es dar soporte a un número muy grande de watchers que realizan una cantidad masiva de observaciones. etcd apunta a soportar O(10k) clientes, O(100K) flujos de watch (O(10) flujos por cliente) y O(10M) observaciones en total (O(100) observaciones por flujo). La memoria consumida por cada observación individual representa la mayor parte del uso global de etcd y es, por lo tanto, el foco de las optimizaciones actuales y futuras.


Tres componentes relacionados del watch de etcd consumen memoria física: cada `grpc.Conn`, cada flujo de watch y cada instancia de la actividad de observación. `grpc.Conn` mantiene la conexión TCP real y el resto del estado de conexión gRPC. Cada `grpc.Conn` consume O(10kb) de memoria y puede tener varios flujos de watch adjuntos.

Cada flujo de watch es una conexión HTTP2 independiente que consume otros O(10kb) de memoria.
Varias observaciones pueden compartir un mismo flujo de watch.

La observación es la estructura real que realiza el seguimiento de los cambios en el almacén de clave-valor. Cada observación debería consumir solo < O(1kb).

```
                                          +-------+
                                          | watch |
                              +---------> | foo   |
                              |           +-------+
                       +------+-----+
                       |   stream   |
      +--------------> |            |
      |                +------+-----+     +-------+
      |                       |           | watch |
      |                       +---------> | bar   |
+-----+------+                            +-------+
|            |         +------------+
|   conn     +-------> |   stream   |
|            |         |            |
+-----+------+         +------------+
      |
      |
      |
      |                +------------+
      +--------------> |   stream   |
                       |            |
                       +------------+
```

El consumo teórico de memoria del watch puede aproximarse con la fórmula:
`memory = c1 * number_of_conn + c2 * avg_number_of_stream_per_conn + c3 * avg_number_of_watch_stream`

## Entorno de prueba {#testing-environment}

Versión de etcd
- git head https://github.com/etcd-io/etcd/commit/185097ffaa627b909007e772c175e8fefac17af3

Tipo de máquina GCE n1-standard-2
- 7.5 GB de memoria
- 2x CPUs

## Uso de memoria global {#overall-memory-usage}

El uso de memoria global refleja cuánto [RSS][rss] consume etcd con los watchers de los clientes. Aunque el resultado puede variar hasta en un 10%, sigue siendo significativo, ya que el objetivo es conocer el uso de memoria aproximado y el patrón de las asignaciones.

Con el resultado del benchmark, podemos calcular aproximadamente que `c1 = 17kb`, `c2 = 18kb` y `c3 = 350bytes`. Así, cada conexión de cliente adicional consume 17kb de memoria, cada flujo adicional consume 18kb de memoria y cada observación adicional solo consume 350bytes. Un único servidor etcd puede mantener millones de observaciones con unos pocos GB de memoria en condiciones normales.


| clientes | flujos por cliente | observaciones por flujo | observaciones totales | uso de memoria |
|---------|---------|-----------|----------------|--------------|
| 1k |  1 |   1 |   1k |   50MB |
| 2k |  1 |   1 |   2k |   90MB |
| 5k |  1 |   1 |   5k |  200MB |
| 1k | 10 |   1 |  10k |  217MB |
| 2k | 10 |   1 |  20k |  417MB |
| 5k | 10 |   1 |  50k |  980MB |
| 1k | 50 |   1 |  50k | 1001MB |
| 2k | 50 |   1 | 100k | 1960MB |
| 5k | 50 |   1 | 250k | 4700MB |
| 1k | 50 |  10 | 500k | 1171MB |
| 2k | 50 |  10 |   1M | 2371MB |
| 5k | 50 |  10 | 2.5M | 5710MB |
| 1k | 50 | 100 |   5M | 2380MB |
| 2k | 50 | 100 |  10M | 4672MB |
| 5k | 50 | 100 |  25M |  *OOM* |

[rss]: https://en.wikipedia.org/wiki/Resident_set_size
