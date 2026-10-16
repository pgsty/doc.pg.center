---
title: Benchmarking de etcd v2.2.0-rc-memory
weight: 5500
description: Mediciones de rendimiento para etcd v2.2.0-rc-memory
categories: [Referencia]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/benchmarks/etcd-2-2-0-rc-memory-benchmarks.md"
---

## Máquina física {#physical-machine}

Tipo de máquina GCE n1-standard-2

- 1x SSD local dedicado montado bajo /var/lib/etcd
- 1x disco lento dedicado para el sistema operativo
- 7.5 GB de memoria
- 2x CPUs

## etcd {#etcd}

```
etcd Version: 2.2.0-rc.0+git
Git SHA: 103cb5c
Go Version: go1.5
Go OS/Arch: linux/amd64
```

## Prueba {#testing}

Inicia un clúster de etcd de 3 miembros, cada uno de los cuales usa 2 núcleos.

La longitud del nombre de la clave es siempre de 64 bytes, lo que constituye una longitud razonable para un promedio de bytes de clave.

## Uso máximo de memoria {#memory-maximal-usage}

- etcd puede usar la memoria máxima si una réplica está caída y el líder sigue enviando instantáneas.
- `max RSS` es el uso de memoria máximo registrado en 3 ejecuciones.

| bytes de valor | número de claves | tamaño de datos (MB) | RSS máximo (MB) | relación entre el RSS máximo y los datos en el líder |
|-------------|-------------|---------------|-------------|-----------------------------|
| 128  | 50000  | 6 | 433 | 72x |
| 128  | 100000 | 12 | 659 | 54x |
| 128  | 200000 | 24 | 1466 | 61x |
| 1024 | 50000  | 48 | 1253 | 26x |
| 1024 | 100000 | 96 | 2344 | 24x |
| 1024 | 200000 | 192 | 4361 | 22x |

## Umbral de tamaño de datos {#data-size-threshold}

- Cuando etcd alcanza el umbral de tamaño de datos, puede disparar fácilmente una elección de líder y descartar parte de las propuestas.
- En la mayoría de los casos, el clúster de etcd debería funcionar sin problemas si no alcanza el umbral. Si no funciona bien debido a recursos insuficientes, reduce el tamaño de sus datos.

| bytes de valor | límite del número de claves | umbral de tamaño de datos sugerido (MB) | RSS consumido (MB) |
|-------------|-----------------------|-----------------------------------|------------------|
| 128 | 400K | 48 | 2400 |
| 1024 | 300K | 292 | 6500 |
