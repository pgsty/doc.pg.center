---
title: "Pruebas de rendimiento de etcd v2.2.0-rc"
weight: 5625
description: Medidas de rendimiento para etcd v2.2.0-rc
categories: [Referencia]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/benchmarks/etcd-2-2-0-rc-benchmarks.md"
---

## Máquina física {#physical-machine}

Tipo de máquina GCE n1-highcpu-2

- 1x SSD local dedicado montado bajo /var/lib/etcd
- 1x disco lento dedicado para el sistema operativo
- 1.8 GB de memoria
- 2x CPUs

## Clúster de etcd {#etcd-cluster}

3 miembros de etcd 2.2.0-rc, cada uno ejecutándose en una sola máquina.

Versiones detalladas:

```
etcd Version: 2.2.0-alpha.1+git
Git SHA: 59a5a7e
Go Version: go1.4.2
Go OS/Arch: linux/amd64
```

Además, usamos 3 miembros de etcd 2.1.0 en fase alfa para formar el clúster y obtener el rendimiento base. La cabeza del commit de etcd está en [c7146bd5][c7146bd5], que es la misma que usamos en el [benchmark de etcd 2.1][etcd-2.1-benchmark].

## Pruebas {#testing}

Inicializa otra máquina y usa la herramienta de benchmark HTTP [hey][hey] para enviar solicitudes a cada miembro de etcd. Consulta la [guía de benchmark][hack-benchmark] para instrucciones detalladas.

## Rendimiento {#performance}

### lectura de una sola clave {#reading-one-single-key}

| tamaño de la clave en bytes | número de clientes | servidor etcd de destino | QPS de lectura | Latencia del percentil 90 (ms) |
|-------------------|-------------------|--------------------|----------|---------------|
| 64                | 1                 | solo el líder        | 2804 (-5%) | 0.4 (+0%) |
| 64                | 64                | solo el líder        | 17816 (+0%) | 5.7 (-6%) |
| 64                | 256               | solo el líder        | 18667 (-6%) | 20.4 (+2%) |
| 256               | 1                 | solo el líder        | 2181 (-15%) | 0.5 (+25%) |
| 256               | 64                | solo el líder        | 17435 (-7%) | 6.0 (+9%) |
| 256               | 256               | solo el líder        | 18180 (-8%) | 21.3 (+3%) |
| 64                | 64                | todos los servidores        | 46965 (-4%) | 2.1 (+0%) |
| 64                | 256               | todos los servidores        | 55286 (-6%) | 7.4 (+6%) |
| 256               | 64                | todos los servidores        | 46603 (-6%) | 2.1 (+5%) |
| 256               | 256               | todos los servidores        | 55291 (-6%) | 7.3 (+4%) |

### escritura de una sola clave {#writing-one-single-key}

| tamaño de la clave en bytes | número de clientes | servidor etcd de destino | QPS de escritura | Latencia del percentil 90 (ms) |
|-------------------|-------------------|--------------------|-----------|---------------|
| 64                | 1                 | solo el líder        | 76 (+22%)  | 19.4 (-15%) |
| 64                | 64                | solo el líder        | 2461 (+45%) | 31.8 (-32%) |
| 64                | 256               | solo el líder        | 4275 (+1%) | 69.6 (-10%) |
| 256               | 1                 | solo el líder        | 64 (+20%)  | 16.7 (-30%) |
| 256               | 64                | solo el líder        | 2385 (+30%) | 31.5 (-19%) |
| 256               | 256               | solo el líder        | 4353 (-3%) | 74.0 (+9%) |
| 64                | 64                | todos los servidores        | 2005 (+81%) | 49.8 (-55%) |
| 64                | 256               | todos los servidores        | 4868 (+35%) | 81.5 (-40%) |
| 256               | 64                | todos los servidores        | 1925 (+72%) | 47.7 (-59%) |
| 256               | 256               | todos los servidores        | 4975 (+36%) | 70.3 (-36%) |

### explicación de los cambios de rendimiento {#performance-changes-explanation}

- El QPS de lectura en la mayoría de los escenarios disminuye un 5~8%. La razón es que etcd registra métricas del almacén para cada operación del almacén. Estas métricas son importantes para la monitorización y la depuración, por lo que esto es aceptable.

- El QPS de escritura hacia el líder aumenta un 20~30%. Esto se debe a que desacoplamos el bucle principal de raft y el bucle de aplicación de entradas, lo que evita que se bloqueen mutuamente.

- El QPS de escritura hacia todos los servidores aumenta un 30~80% porque la réplica puede recibir el último índice de confirmación antes y confirmar las propuestas más rápido.

[c7146bd5]: https://github.com/etcd-io/etcd/commits/c7146bd5f2c73716091262edc638401bb8229144
[etcd-2.1-benchmark]: /es/etcd/benchmarks/etcd-2-1-0-alpha-benchmarks/
[hack-benchmark]: https://github.com/etcd-io/etcd/tree/v2.3.8/hack/benchmark
[hey]: https://github.com/rakyll/hey
