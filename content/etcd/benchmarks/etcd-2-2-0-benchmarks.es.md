---
title: "Pruebas de rendimiento de etcd v2.2.0"
weight: 5750
description: Medidas de rendimiento para etcd v2.2.0
categories: [Referencia]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/benchmarks/etcd-2-2-0-benchmarks.md"
---

## Máquinas físicas {#physical-machines}

Tipo de máquina GCE n1-highcpu-2

- 1x SSD local dedicado montado como directorio de datos de etcd
- 1x disco lento dedicado para el sistema operativo
- 1.8 GB de memoria
- 2x CPUs

## Clúster de etcd {#etcd-cluster}

3 miembros de etcd 2.2.0, cada uno ejecutándose en una sola máquina.

Versiones detalladas:

```
etcd Version: 2.2.0
Git SHA: e4561dd
Go Version: go1.5
Go OS/Arch: linux/amd64
```

## Pruebas {#testing}

Inicializa otra máquina, fuera del clúster de etcd, y ejecuta la herramienta de benchmark HTTP [`hey` con un parche de reutilización de conexión](https://github.com/rakyll/hey) para enviar solicitudes a cada miembro del clúster de etcd. Consulta las [instrucciones del benchmark](https://github.com/etcd-io/etcd/tree/v2.3.8/hack/benchmark) para obtener el parche y los pasos para reproducir nuestros procedimientos.

El rendimiento se calcula a partir de los resultados de 100 rondas de benchmark.

## Rendimiento {#performance}

### Rendimiento de lectura de una sola clave {#single-key-read-performance}

| tamaño de la clave en bytes | número de clientes | servidor etcd de destino | QPS medio de lectura | desviación estándar del QPS de lectura | Latencia media del percentil 90 (ms) | desviación estándar de la latencia |
|-------------------|-------------------|--------------------|------------------|-----------------|--------------------------------------|----------------|
| 64 | 1 | solo el líder | 2303 | 200 | 0.49 | 0.06 |
| 64 | 64 | solo el líder | 15048 | 685 | 7.60 | 0.46 |
| 64 | 256 | solo el líder | 14508 | 434 | 29.76 | 1.05 |
| 256 | 1 | solo el líder | 2162 | 214 | 0.52 | 0.06 |
| 256 | 64 | solo el líder | 14789 | 792 | 7.69| 0.48 |
| 256 | 256 | solo el líder | 14424 | 512 | 29.92 | 1.42 |
| 64 | 64 | todos los servidores | 45752 | 2048 | 2.47 | 0.14 |
| 64 | 256 | todos los servidores | 46592 | 1273 | 10.14 | 0.59 |
| 256 | 64 | todos los servidores | 45332 | 1847 | 2.48| 0.12 |
| 256 | 256 | todos los servidores | 46485 | 1340 | 10.18 | 0.74 |

### Rendimiento de escritura de una sola clave {#single-key-write-performance}

| tamaño de la clave en bytes | número de clientes | servidor etcd de destino | QPS medio de escritura | desviación estándar del QPS de escritura | Latencia media del percentil 90 (ms) | desviación estándar de la latencia |
|-------------------|-------------------|--------------------|------------------|-----------------|--------------------------------------|----------------|
| 64 | 1 | solo el líder | 55 | 4 | 24.51 | 13.26 |
| 64 | 64 | solo el líder | 2139 | 125 | 35.23 | 3.40 |
| 64 | 256 | solo el líder | 4581 | 581 | 70.53 | 10.22 |
| 256 | 1 | solo el líder | 56 | 4 | 22.37| 4.33 |
| 256 | 64 | solo el líder | 2052 | 151 | 36.83 | 4.20 |
| 256 | 256 | solo el líder | 4442 | 560 | 71.59 | 10.03 |
| 64 | 64 | todos los servidores | 1625 | 85 | 58.51 | 5.14 |
| 64 | 256 | todos los servidores | 4461 | 298 | 89.47 | 36.48 |
| 256 | 64 | todos los servidores | 1599 | 94 | 60.11| 6.43 |
| 256 | 256 | todos los servidores | 4315 | 193 | 88.98 | 7.01 |

## Cambios en el rendimiento {#performance-changes}

- Como etcd ahora registra métricas para cada llamada a la API, el rendimiento en QPS de lectura parece sufrir una ligera disminución en la mayoría de los escenarios. Este impacto mínimo en el rendimiento se consideró una inversión razonable a cambio de la amplitud de la información de monitorización y depuración obtenida.

- El QPS de escritura hacia los líderes del clúster parece haber aumentado por un pequeño margen. Esto se debe a que el bucle principal y los bucles de aplicación de entradas se desacoplaron en la lógica raft de etcd, eliminando varios bloqueos entre ellos.

- El QPS de escritura hacia todos los miembros parece haber aumentado de forma significativa, porque las réplicas ahora reciben el último índice de confirmación antes y confirman las propuestas más rápidamente.
