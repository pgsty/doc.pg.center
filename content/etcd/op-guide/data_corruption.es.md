---
title: Corrupción de datos
weight: 5000
description: Corrupción de datos y recuperación en etcd
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/data_corruption.md"
---

etcd incluye una detección automatizada de corrupción de datos integrada para evitar que el estado de los miembros diverja.

> [!NOTE]
> En etcd 3.7, usa las compuertas de funcionalidades y las opciones de duración que se indican a continuación. Las antiguas opciones experimentales de comprobación de corrupción se han eliminado; consulta las [opciones de configuración](/es/etcd/op-guide/configuration/#feature-gates).

## Activación de la detección de corrupción de datos {#enabling-data-corruption-detection}

La detección de corrupción de datos puede hacerse mediante:
* La comprobación inicial, activada con la opción `--feature-gates=InitialCorruptCheck=true`.
* La comprobación periódica de:
  * El hash de la revisión compactada, activado con la opción `--feature-gates=CompactHashCheck=true`.
  * El hash de la última revisión, activado con la opción `--corrupt-check-time`.

La comprobación inicial se ejecutará durante el arranque del miembro de etcd.
El miembro comparará su estado persistente con el de los demás miembros y saldrá si hay una discrepancia.

Ambas comprobaciones periódicas serán ejecutadas por el líder del clúster en un clúster que ya está en ejecución.
El líder comparará su estado persistente con el de los demás miembros y generará una alarma CORRUPT si hay una discrepancia.
Ambas comprobaciones sirven para el mismo propósito; sin embargo, merece la pena activar las dos para equilibrar el rendimiento y el tiempo de detección.
* Comprobación del hash de la revisión compactada - requiere compactación regular, coste mínimo de rendimiento, gestiona réplicas lentas.
* Comprobación del hash de la última revisión - coste alto de rendimiento, no gestiona réplicas lentas ni compactaciones frecuentes.

### Comprobación del hash de la revisión compactada {#compacted-revision-hash-check}

Cuando se activa con la opción `--feature-gates=CompactHashCheck=true`, la comprobación se ejecutará una vez por minuto.
Esto puede ajustarse con la opción `--compact-hash-check-time` usando el formato: `1m` - cada minuto, `1h` - cada hora.
Esta comprobación extiende la compactación para calcular también una suma de verificación que puede compararse entre los miembros del clúster.
No provoca ningún recorrido adicional de la base de datos, lo que la hace muy barata, pero requiere una compactación regular en el clúster.

### Comprobación del hash de la última revisión {#latest-revision-hash-check}

Se activa con la opción `--corrupt-check-time`, que requiere proporcionar un periodo de ejecución en el formato: `1m` - cada minuto, `1h` - cada hora.
Se recomienda un periodo de un par de horas debido a su alto coste de rendimiento.
Ejecutar una comprobación requiere calcular una suma de verificación recorriendo todo el contenido de etcd en la revisión indicada.

## Restauración de un miembro corrupto {#restoring-a-corrupted-member}

Hay tres formas de restaurar un miembro corrupto:
* Purgar el estado persistente del miembro
* Reemplazar el miembro
* Restaurar todo el clúster

Una vez restaurado el miembro corrupto, la alarma CORRUPT puede eliminarse.

### Purgar el estado persistente del miembro {#purge-member-persistent-state}

El estado de los miembros puede purgarse mediante:
1. Detener la instancia de etcd.
2. Hacer una copia de seguridad del directorio de datos de etcd.
3. Sacar el subdirectorio `snap` del directorio de datos de etcd.
6. Iniciar `etcd` con `--initial-cluster-state=existing` y los miembros del clúster enumerados en `--initial-cluster`.

Se espera que el miembro de etcd descargue una instantánea actualizada del líder.

### Reemplazar el miembro {#replace-member}

El miembro puede reemplazarse mediante:
1. Detener la instancia de etcd.
2. Hacer una copia de seguridad del directorio de datos de etcd.
3. Eliminar el directorio de datos.
4. Eliminar el miembro del clúster ejecutando `etcdctl member remove`.
5. Añadirlo de nuevo ejecutando `etcdctl member add`
6. Iniciar `etcd` con `--initial-cluster-state=existing` y los miembros del clúster enumerados en `--initial-cluster`.

### Restaurar todo el clúster {#restore-whole-cluster}

El clúster puede restaurarse guardando una instantánea del líder actual y restaurándola en todos los miembros.
Ejecuta `etcdctl snapshot save` contra el líder y sigue el [procedimiento de restauración de un clúster](/es/etcd/op-guide/recovery/).
