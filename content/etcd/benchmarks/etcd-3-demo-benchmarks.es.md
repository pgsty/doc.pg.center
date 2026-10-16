---
title: Benchmarking de etcd v3
weight: 5375
description: Mediciones de rendimiento para etcd v3
categories: [Referencia]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/benchmarks/etcd-3-demo-benchmarks.md"
---

## Máquinas físicas {#physical-machines}

Tipo de máquina GCE n1-highcpu-2

- 1x SSD local dedicado montado bajo /var/lib/etcd
- 1x disco lento dedicado para el sistema operativo
- 1.8 GB de memoria
- 2x CPUs
- versión de etcd 2.2.0

## Clúster de etcd {#etcd-cluster}

1 miembro de etcd ejecutándose en modo de demostración v3

## Prueba {#testing}

Usa la [herramienta de benchmark de etcd v3][etcd-v3-benchmark].

## Rendimiento {#performance}

### lectura de una sola clave {#reading-one-single-key}

| tamaño de la clave en bytes | número de clientes | QPS de lectura | latencia del percentil 90 (ms) |
|-------------------|-------------------|----------|---------------|
| 256               | 1                 | 2716  | 0.4      |
| 256               | 64                | 16623 | 6.1      |
| 256               | 256               | 16622 | 21.7     |

El rendimiento es casi el mismo que el que se obtiene con un manejador de servidor vacío.

### lectura de una sola clave después de un put {#reading-one-single-key-after-putting}

| tamaño de la clave en bytes | número de clientes | QPS de lectura | latencia del percentil 90 (ms) |
|-------------------|-------------------|----------|---------------|
| 256               | 1                 | 2269  | 0.5      |
| 256               | 64                | 13582 | 8.6      |
| 256               | 256               | 13262 | 47.5     |

El rendimiento con un manejador de servidor vacío no se ve afectado por un put. Por lo
tanto, la degradación del rendimiento debería estar causada por el paquete de almacenamiento.

[etcd-v3-benchmark]: https://github.com/etcd-io/etcd/tree/main/tools/benchmark
