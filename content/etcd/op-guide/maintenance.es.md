---
title: Mantenimiento
weight: 4450
description: Guía de mantenimiento periódico del clúster de etcd
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/maintenance.md"
---

## Descripción general {#overview}

Un clúster de etcd necesita mantenimiento periódico para seguir siendo fiable. Según las necesidades de una aplicación de etcd, este mantenimiento normalmente puede automatizarse y realizarse sin tiempo de inactividad ni un rendimiento significativamente degradado.

Todo el mantenimiento de etcd gestiona los recursos de almacenamiento consumidos por el espacio de claves de etcd. El hecho de no controlar adecuadamente el tamaño del espacio de claves está protegido por cuotas de espacio de almacenamiento; si a un miembro de etcd le queda poco espacio, una cuota activará alarmas en todo el clúster que pondrán el sistema en un modo de mantenimiento de operación limitada. Para evitar quedarse sin espacio para escrituras en el espacio de claves, el historial del espacio de claves de etcd debe compactarse. El espacio de almacenamiento en sí puede recuperarse desfragmentando los miembros de etcd. Finalmente, las copias de seguridad periódicas en forma de instantáneas del estado de los miembros de etcd hacen posible recuperarse de cualquier pérdida lógica de datos no intencionada o de corrupción causada por un error operativo.

## Retención del registro de Raft {#raft-log-retention}

`etcd --snapshot-count` configura el número de entradas de Raft aplicadas que se mantienen en memoria antes de la compactación. Cuando se alcanza `--snapshot-count`, el servidor primero persiste los datos de la instantánea en el disco y luego trunca las entradas antiguas. Cuando una réplica lenta solicita registros anteriores a un índice compactado, el líder envía la instantánea forzando a la réplica a sobrescribir su estado.

Un `--snapshot-count` más alto mantiene más entradas de Raft en memoria hasta la instantánea, lo que provoca un [uso recurrente de memoria más alto](https://github.com/kubernetes/kubernetes/issues/60589#issuecomment-371977156). Dado que el líder retiene las últimas entradas de Raft durante más tiempo, una réplica lenta dispone de más tiempo para ponerse al día antes de la instantánea del líder. `--snapshot-count` es un equilibrio entre un mayor uso de memoria y una mejor disponibilidad de las réplicas lentas.

En v3.2, el valor por defecto de `--snapshot-count` [cambió de 10,000 a 100,000](https://github.com/etcd-io/etcd/pull/7160). En v3.7.0, el valor por defecto es 10,000.

En términos de rendimiento, un `--snapshot-count` mayor que 100,000 puede afectar al rendimiento de escritura. Un número mayor de objetos en memoria puede ralentizar la [fase de marcado del GC de Go `runtime.scanobject`](https://golang.org/src/runtime/mgc.go), y una reclamación de memoria poco frecuente hace que la asignación sea lenta. El rendimiento varía según las cargas de trabajo y los entornos del sistema. Sin embargo, en general, una compactación demasiado frecuente afecta a la disponibilidad del clúster y al rendimiento de escritura. Una compactación demasiado poco frecuente también es perjudicial porque ejerce demasiada presión sobre el recolector de basura de Go. Consulta [Understanding Performance Aspects of etcd and Raft](https://www.slideshare.net/mitakeh/understanding-performance-aspects-of-etcd-and-raft) para más resultados de investigación.

## Compactación del historial: base de datos clave-valor de la API v3 {#history-compaction-v3-api-key-value-database}

Dado que etcd mantiene un historial exacto de su espacio de claves, este historial debe compactarse periódicamente para evitar la degradación del rendimiento y el agotamiento eventual del espacio de almacenamiento. Compactar el historial del espacio de claves descarta toda la información sobre las claves sustituidas antes de una revisión dada del espacio de claves. El espacio usado por esas claves queda entonces disponible para escrituras adicionales en el espacio de claves.

El espacio de claves puede compactarse automáticamente con la política de retención de historial por ventana de tiempo de `etcd`, o manualmente con `etcdctl`. El método con `etcdctl` proporciona un control fino sobre el proceso de compactación, mientras que la compactación automática se adapta a aplicaciones que solo necesitan el historial de claves durante cierto tiempo.

Una compactación iniciada con `etcdctl` funciona así:

```sh
# compact up to revision 3
$ etcdctl compact 3
```

Las revisiones anteriores a la revisión de compactación se vuelven inaccesibles:

```sh
$ etcdctl get --rev=2 somekey
Error:  rpc error: code = 11 desc = etcdserver: mvcc: required revision has been compacted
```

### Compactación automática {#auto-compaction}

`etcd` puede configurarse para compactar automáticamente el espacio de claves con las opciones `--auto-compaction-mode` y `--auto-compaction-retention`. Hay dos modos de compactación: `periodic` (por defecto) y `revision`.

#### Compactación periódica {#periodic-compaction}

La compactación periódica retiene una ventana basada en el tiempo del historial del espacio de claves:

```sh
# keep one hour of history
$ etcd --auto-compaction-retention=1h
```

El valor de retención especifica cuánto historial conservar. Un registro no se compactará hasta aproximadamente esa duración después de su creación. Esto garantiza que los watchers lentos aún puedan ponerse al día dentro de la ventana de retención.

Cuando el periodo de retención es mayor que 1 hora, etcd compacta cada hora manteniendo la ventana de retención completa. Cuando el periodo de retención es de 1 hora o menos, etcd compacta en el intervalo del periodo de retención.

Por ejemplo, con `--auto-compaction-retention=10h`, etcd espera 10 horas para la primera compactación y luego compacta cada hora a partir de entonces:

```text
0hr  (rev = 1)
1hr  (rev = 10)
...
8hr  (rev = 80)
9hr  (rev = 90)
10hr (rev = 100, Compact(1))
11hr (rev = 110, Compact(10))
...
```

Los valores recomendados dependen del caso de uso:

- Actualizaciones frecuentes de las mismas claves: un periodo corto como `1h` o `30m`
- Actualizaciones poco frecuentes: un periodo más largo como `24h`, `48h` o `72h`
- Valor por defecto de propósito general: `10h`

#### Compactación por revisión {#revision-compaction}

La compactación por revisión retiene un número fijo de revisiones:

```sh
# keep 1000 revisions
$ etcd --auto-compaction-mode=revision --auto-compaction-retention=1000
```

etcd comprueba cada 5 minutos y compacta sobre `"latest revision" - 1000`. Por ejemplo, cuando la última revisión es 30000, compacta sobre la revisión 29000.

## Desfragmentación {#defragmentation}

Tras compactar el espacio de claves, la base de datos del backend puede presentar fragmentación interna. Cualquier fragmentación interna es espacio que el backend puede usar libremente pero que sigue consumiendo espacio de almacenamiento. La compactación de revisiones antiguas fragmenta internamente `etcd` dejando huecos en la base de datos del backend. El espacio fragmentado está disponible para que lo use `etcd`, pero no está disponible para el sistema de archivos del host. En otras palabras, borrar datos de la aplicación no recupera el espacio en el disco.

El proceso de desfragmentación libera ese espacio de almacenamiento de vuelta al sistema de archivos. La desfragmentación se emite por miembro, de modo que se pueden evitar picos de latencia en todo el clúster.

Para desfragmentar un miembro de etcd, usa el comando `etcdctl defrag`:

```sh
$ etcdctl defrag
Finished defragmenting etcd member[127.0.0.1:2379]
```

> [!WARNING]
> Ten en cuenta que la desfragmentación de un miembro en vivo impide que el sistema lea y escriba datos mientras reconstruye sus estados

> [!WARNING]
> Ten en cuenta que la solicitud de desfragmentación no se replica por el clúster. Es decir, la solicitud solo se aplica al nodo local. Especifica todos los miembros en la opción `--endpoints` o usa la opción `--cluster` para encontrar automáticamente todos los miembros del clúster.

Ejecuta operaciones de desfragmentación para todos los puntos de acceso del clúster asociado con el punto de acceso por defecto:

```bash
$ etcdctl defrag --cluster
Finished defragmenting etcd member[http://127.0.0.1:2379]
Finished defragmenting etcd member[http://127.0.0.1:22379]
Finished defragmenting etcd member[http://127.0.0.1:32379]
```

Para desfragmentar un directorio de datos de etcd directamente, mientras etcd no está en ejecución, usa el comando:

```sh
etcdutl defrag --data-dir <path-to-etcd-data-dir>
```

## Cuota de espacio {#space-quota}

La cuota de espacio en `etcd` garantiza que el clúster opere de forma fiable. Sin una cuota de espacio, `etcd` puede sufrir un rendimiento deficiente si el espacio de claves crece en exceso, o puede simplemente quedarse sin espacio de almacenamiento, lo que lleva a un comportamiento impredecible del clúster. Si la base de datos del backend del espacio de claves de cualquier miembro supera la cuota de espacio, `etcd` genera una alarma en todo el clúster que pone el clúster en un modo de mantenimiento que solo acepta lecturas y borrados de claves. Solo después de liberar suficiente espacio en el espacio de claves y desfragmentar la base de datos del backend, junto con el despeje de la alarma de cuota de espacio, el clúster puede reanudar su operación normal.

Por defecto, `etcd` establece una cuota de espacio conservadora adecuada para la mayoría de las aplicaciones, pero puede configurarse en la línea de comandos, en bytes:

```sh
# set a very small 16 MiB quota
$ etcd --quota-backend-bytes=$((16*1024*1024))
```

La cuota de espacio puede activarse con un bucle:

```sh
# fill keyspace
$ while [ 1 ]; do dd if=/dev/urandom bs=1024 count=1024  | ETCDCTL_API=3 etcdctl put key  || break; done
...
Error:  rpc error: code = 8 desc = etcdserver: mvcc: database space exceeded
# confirm quota space is exceeded
$ ETCDCTL_API=3 etcdctl --write-out=table endpoint status
+----------------+------------------+-----------+---------+-----------+-----------+------------+
|    ENDPOINT    |        ID        |  VERSION  | DB SIZE | IS LEADER | RAFT TERM | RAFT INDEX |
+----------------+------------------+-----------+---------+-----------+-----------+------------+
| 127.0.0.1:2379 | bf9071f4639c75cc | 2.3.0+git | 18 MB   | true      |         2 |       3332 |
+----------------+------------------+-----------+---------+-----------+-----------+------------+
# confirm alarm is raised
$ ETCDCTL_API=3 etcdctl alarm list
memberID:13803658152347727308 alarm:NOSPACE
```

Eliminar los datos excesivos del espacio de claves y desfragmentar la base de datos del backend devolverá el clúster a los límites de la cuota:

```sh
# get current revision
$ rev=$(ETCDCTL_API=3 etcdctl --endpoints=:2379 endpoint status --write-out="json" | egrep -o '"revision":[0-9]*' | egrep -o '[0-9].*')
# compact away all old revisions
$ ETCDCTL_API=3 etcdctl compact $rev
compacted revision 1516
# defragment away excessive space
$ ETCDCTL_API=3 etcdctl defrag
Finished defragmenting etcd member[127.0.0.1:2379]
# disarm alarm
$ ETCDCTL_API=3 etcdctl alarm disarm
memberID:13803658152347727308 alarm:NOSPACE
# test puts are allowed again
$ ETCDCTL_API=3 etcdctl put newkey 123
OK
```

La métrica `etcd_mvcc_db_total_size_in_use_in_bytes` indica el uso real de la base de datos tras una compactación del historial, mientras que `etcd_debugging_mvcc_db_total_size_in_bytes` muestra el tamaño de la base de datos incluido el espacio libre que espera desfragmentación. Esta última solo aumenta cuando la primera está cerca de ella, lo que significa que cuando ambas métricas están cerca de la cuota se requiere una compactación del historial para evitar activar la cuota de espacio.

`etcd_debugging_mvcc_db_total_size_in_bytes` se renombró a `etcd_mvcc_db_total_size_in_bytes` a partir de v3.4.

> [!WARNING]
> Es posible obtener un error `ErrGRPCNoSpace` en una solicitud Put/Txn/LeaseGrant y que la solicitud de escritura aun así tenga éxito en el backend, porque etcd comprueba la cuota de espacio en la capa de la API y en la capa interna de Apply, y la capa de Apply solo activará la alarma `NOSPACE` sin bloquear el avance de la transacción.

## Copia de seguridad con instantáneas {#snapshot-backup}

Tomar instantáneas del clúster de `etcd` de forma regular sirve como una copia de seguridad duradera del espacio de claves de etcd. Al tomar instantáneas periódicas de la base de datos del backend de un miembro de etcd, un clúster de `etcd` puede recuperarse hasta un punto en el tiempo con un estado correcto conocido.

Se toma una instantánea con `etcdctl`:

```sh
$ etcdctl snapshot save backup.db
$ etcdutl --write-out=table snapshot status backup.db
+----------+----------+------------+------------+
|   HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
+----------+----------+------------+------------+
| fe01cf57 |       10 |          7 | 2.1 MB     |
+----------+----------+------------+------------+
```
