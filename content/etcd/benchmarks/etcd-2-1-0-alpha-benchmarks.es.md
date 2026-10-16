---
title: "Pruebas de rendimiento de etcd v2.1.0"
weight: 5875
description: Medidas de rendimiento para etcd v2.1.0
categories: [Referencia]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/benchmarks/etcd-2-1-0-alpha-benchmarks.md"
---

## Máquinas físicas {#physical-machines}

Tipo de máquina GCE n1-highcpu-2

- 1x SSD local dedicado montado bajo /var/lib/etcd
- 1x disco lento dedicado para el sistema operativo
- 1.8 GB de memoria
- 2x CPUs
- versión de etcd 2.1.0 alpha

## Clúster de etcd {#etcd-cluster}

3 miembros de etcd, cada uno ejecutándose en una sola máquina

## Pruebas {#testing}

Inicializa otra máquina y usa la herramienta de benchmark HTTP [hey][hey] para enviar solicitudes a cada miembro de etcd. Consulta la [guía de benchmark][hack-benchmark] para instrucciones detalladas.

## Rendimiento {#performance}

### lectura de una sola clave {#reading-one-single-key}

| tamaño de la clave en bytes | número de clientes | servidor etcd de destino | QPS de lectura | Latencia del percentil 90 (ms) |
|-------------------|-------------------|--------------------|----------|---------------|
| 64                | 1                 | solo el líder        | 1534     | 0.7        |
| 64                | 64                | solo el líder        | 10125    | 9.1      |
| 64                | 256               | solo el líder        | 13892    | 27.1      |
| 256               | 1                 | solo el líder        | 1530     | 0.8       |
| 256               | 64                | solo el líder        | 10106    | 10.1      |
| 256               | 256               | solo el líder        | 14667    | 27.0      |
| 64                | 64                | todos los servidores        | 24200    | 3.9      |
| 64                | 256               | todos los servidores        | 33300    | 11.8      |
| 256               | 64                | todos los servidores        | 24800    | 3.9      |
| 256               | 256               | todos los servidores        | 33000    | 11.5      |

### escritura de una sola clave {#writing-one-single-key}

| tamaño de la clave en bytes | número de clientes | servidor etcd de destino | QPS de escritura | Latencia del percentil 90 (ms) |
|-------------------|-------------------|--------------------|-----------|---------------|
| 64                | 1                 | solo el líder        | 60        | 21.4 |
| 64                | 64                | solo el líder        | 1742      | 46.8 |
| 64                | 256               | solo el líder        | 3982      | 90.5 |
| 256               | 1                 | solo el líder        | 58        | 20.3 |
| 256               | 64                | solo el líder        | 1770      | 47.8 |
| 256               | 256               | solo el líder        | 4157      | 105.3 |
| 64                | 64                | todos los servidores        | 1028      | 123.4 |
| 64                | 256               | todos los servidores        | 3260      | 123.8 |
| 256               | 64                | todos los servidores        | 1033      | 121.5 |
| 256               | 256               | todos los servidores        | 3061      | 119.3 |

[hack-benchmark]: https://github.com/etcd-io/etcd/tree/main/hack/benchmark
[hey]: https://github.com/rakyll/hey
